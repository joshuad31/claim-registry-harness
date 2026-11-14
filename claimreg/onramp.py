"""The new-user path: from a folder of Markdown sources to a finished quest and report.

    cr new     <project> --corpus <folder> [--keys <folder>] [--notebook <url> ...]
    cr frame   <project>            index, Archivist prompt and a header DRAFT from 01_FRAME/question.md
    cr approve <project> --by NAME  a person approves the header (required before a quest)
    cr doctor  [<project>]          checks everything a quest needs, including each model key
    cr quest   <project>            runs the NotebookLM quest unattended, then imports it
    cr run     <project>            evidence pipeline: FRDs, witnesses, matching, coverage, report

Nothing here makes a research judgment.  `cr frame` drafts with your own generator prompts
(Quest Header Generator v2, Archivist Custom Prompt Generator v4) and a draft stays a draft
until a person approves it.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from .config import DEFAULT_CONFIG, load_config
from .util import ensure_dir, read_json, read_text, utcnow, write_json

HARNESS_ROOT = Path(__file__).resolve().parent.parent

# How each provider is reached.  Model names change often: `cr doctor` checks the configured name
# against the provider's own model list and `cr doctor --fix` picks from that list by these
# preferences (first pattern that matches an available model wins).
PRESETS = {
    "openai": {"type": "openai", "base_url": "https://api.openai.com/v1", "model": "gpt-5.2",
               "env": "OPENAI_API_KEY", "hints": ("openai", "chatgpt", "gpt"),
               "prefer": (r"^gpt-5\.2$", r"^gpt-5\.5$", r"^gpt-5(\.\d+)?$", r"^gpt-[5-9]"),
               "max_output_tokens": 16000, "price_per_mtok_in": 2.0, "price_per_mtok_out": 10.0},
    "deepseek": {"type": "openai", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat",
                 "env": "DEEPSEEK_API_KEY", "hints": ("deepseek",),
                 "prefer": (r"^deepseek-chat$", r"^deepseek-reasoner$", r"^deepseek"),
                 "max_output_tokens": 32000, "price_per_mtok_in": 0.3, "price_per_mtok_out": 1.2},
    "gemini": {"type": "openai", "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
               "model": "gemini-3.8-flash", "env": "GEMINI_API_KEY", "hints": ("gemini", "google"),
               "prefer": (r"gemini-[3-9][.\d]*-flash$", r"gemini-[3-9][.\d]*-pro$", r"gemini-[\d.]+-flash$",
                          r"gemini-[\d.]+-pro", r"^(models/)?gemini"),
               "max_output_tokens": 16000, "price_per_mtok_in": 0.5, "price_per_mtok_out": 3.0},
    "anthropic": {"type": "anthropic", "base_url": "https://api.anthropic.com/v1", "model": "claude-sonnet-5-5",
                  "env": "ANTHROPIC_API_KEY", "hints": ("anthropic", "claude"),
                  "prefer": (r"^claude-sonnet-5", r"^claude-opus-5", r"^claude-sonnet", r"^claude"),
                  "max_output_tokens": 16000, "price_per_mtok_in": 3.0, "price_per_mtok_out": 15.0},
}
DEFAULT_ORDER = ("openai", "deepseek", "gemini", "anthropic")

QUESTION_TEMPLATE = """# The question for this investigation

Replace every line that starts with REPLACE. Plain prose is fine; `cr frame` turns this into a
draft quest header for you to review. Keep the hypotheses as rivals: each should predict something
the others do not.

## What I want to decide

REPLACE: one or two sentences. Example: "Does the published evidence make a strong enough case
that drug X treats condition Y in population Z to justify a targeted clinical trial?"

## Who or what it is about (scope)

REPLACE: the population, setting, exposure or product, and what is out of scope.

## The competing answers (hypotheses)

REPLACE: list two to four rival answers, including the boring one and the adverse one. Example:
1. The mechanism is real and reaches the people who matter.
2. The mechanism fails at a necessary step (dose, tissue, timing, or the wrong disease process).
3. The evidence cannot yet tell 1 from 2.

## What evidence would tell them apart

REPLACE: the findings that would move you. Example: "tissue concentrations at clinical doses;
a controlled human trial with a functional endpoint; a null result in a relevant model."
"""


# --------------------------------------------------------------------------- #
# keys and providers
# --------------------------------------------------------------------------- #

def find_keys(keys_dir: str | Path | None) -> dict[str, Path]:
    """Key files in a folder, recognised by file name (the file's content is never read here).
    When several files match one provider, the most recently modified wins."""
    out: dict[str, Path] = {}
    if not keys_dir:
        return out
    d = Path(os.path.expanduser(str(keys_dir)))
    if not d.is_dir():
        raise SystemExit(f"keys folder not found: {d}")
    for name, preset in PRESETS.items():
        hits = [p for p in d.iterdir() if p.is_file() and any(h in p.name.lower() for h in preset["hints"])]
        if hits:
            out[name] = max(hits, key=lambda p: p.stat().st_mtime)
    return out


def provider_block(name: str, key_file: Path | None, model: str | None = None) -> dict:
    p = PRESETS[name]
    block = {"type": p["type"], "base_url": p["base_url"], "model": model or p["model"],
             "max_output_tokens": p["max_output_tokens"], "timeout_s": 900,
             "price_per_mtok_in": p["price_per_mtok_in"], "price_per_mtok_out": p["price_per_mtok_out"]}
    if key_file:
        block["api_key_file"] = str(key_file)
    else:
        block["api_key_env"] = p["env"]
    return block


def choose_providers(keys_dir=None, key_args=(), prefer=()) -> tuple[list[str], dict]:
    """(ordered provider names, provider blocks) from a keys folder, --key name=path pairs and
    environment variables."""
    files = find_keys(keys_dir)
    for kv in key_args or ():
        name, _, path = str(kv).partition("=")
        name = name.strip().lower()
        if name not in PRESETS or not path:
            raise SystemExit(f"--key expects provider=path with provider in {', '.join(PRESETS)}; got {kv!r}")
        if not Path(os.path.expanduser(path)).is_file():
            raise SystemExit(f"--key {name}: file not found: {path}")
        files[name] = Path(os.path.expanduser(path)).resolve()
    names = [n for n in PRESETS if n in files or os.environ.get(PRESETS[n]["env"])]
    order = [n.strip().lower() for n in prefer if n.strip()] or list(DEFAULT_ORDER)
    names.sort(key=lambda n: (order.index(n) if n in order else 99, n))
    return names, {n: provider_block(n, files.get(n)) for n in names}


# --------------------------------------------------------------------------- #
# cr new
# --------------------------------------------------------------------------- #

def cmd_new(a) -> int:
    from .corpus import ingest
    proj = Path(a.project)
    if (proj / "project.json").exists() and not a.force:
        print(f"{proj} already has a project.json. Use --force to rewrite its provider settings, or pick "
              f"another folder.", file=sys.stderr)
        return 2
    for sub in ("01_CORPUS/source-files", "01_CORPUS/manifests", "01_FRAME", "02_RUNS", "04_RELEASES",
                "90_METHOD/prompts", "99_ARCHIVE", "quest"):
        ensure_dir(proj / sub)
    cfg = read_json(proj / "project.json", default={}) or {}
    cfg.setdefault("project", {})["name"] = a.name or cfg.get("project", {}).get("name") or proj.name
    cfg["project"].setdefault("run_prefix", "RUN-" + re.sub(r"[^A-Za-z0-9]+", "-", proj.name).strip("-").upper())
    copied = 0
    if a.corpus:
        src = Path(os.path.expanduser(a.corpus))
        if not src.is_dir():
            print(f"corpus folder not found: {src}", file=sys.stderr)
            return 2
        for p in sorted(src.rglob("*")):
            if p.is_file() and p.suffix.lower() in (".md", ".markdown", ".txt") and not p.name.startswith("."):
                dest = proj / "01_CORPUS" / "source-files" / p.relative_to(src)
                ensure_dir(dest.parent)
                shutil.copyfile(p, dest)
                copied += 1
    names, blocks = choose_providers(a.keys, a.key, (a.prefer or "").split(","))
    if names:
        cfg.setdefault("providers", {}).update(blocks)
        cfg["default_provider"] = names if len(names) > 1 else names[0]
        cfg.setdefault("budget", {"max_calls": 12000, "max_usd": 150.0, "concurrency": 6, "retries": 2})
    if a.notebook:
        cfg.setdefault("notebooklm", {})["notebooks"] = list(a.notebook)
    write_json(proj / "project.json", cfg)
    q = proj / "01_FRAME" / "question.md"
    if not q.exists():
        q.write_text(QUESTION_TEMPLATE, encoding="utf-8")
    man = None
    if any((proj / "01_CORPUS" / "source-files").iterdir()):
        man = ingest(proj, proj / "01_CORPUS" / "source-files")
    print(f"Project ready: {proj.resolve()}")
    if man:
        flagged = [(s["filename"], s["flags"]) for s in man["sources"] if s["flags"]]
        print(f"  Sources: {man['files']} files, {man['bytes']:,} bytes" + (f" ({copied} copied in)" if copied else ""))
        for fn, fl in flagged[:12]:
            print(f"    check {fn}: {', '.join(fl)}")
    else:
        print("  Sources: none yet. Put your Markdown files in 01_CORPUS/source-files and run `cr new` again "
              "with --force, or `cr corpus`.")
    if names:
        print("  Models: " + " -> ".join(f"{n} ({blocks[n]['model']})" for n in names)
              + ("   (tried in this order; a refusal or outage moves to the next)" if len(names) > 1 else ""))
    else:
        print("  Models: no API key found. The offline local engine will be used. To use models, run again with "
              "--keys <folder of key files> or set OPENAI_API_KEY / DEEPSEEK_API_KEY / GEMINI_API_KEY.")
    print("\nNext:")
    print(f"  1. Write your question in {q}")
    print(f"  2. python cr.py frame \"{proj}\"")
    return 0


# --------------------------------------------------------------------------- #
# cr frame / cr approve
# --------------------------------------------------------------------------- #

class _Setup:
    """The few things the index and prompt builders need, without creating a run."""

    def __init__(self, project: Path):
        from .corpus import Corpus, current_manifest, ingest
        from .llm.router import LLM
        from .prompts import PromptLibrary
        self.project_dir = Path(project).resolve()
        self.cfg = load_config(self.project_dir)
        self.prompts = PromptLibrary(self.project_dir)
        self.llm = LLM(self.cfg, log_name="setup-llm-calls.jsonl")
        man = current_manifest(self.project_dir)
        src = self.project_dir / "01_CORPUS" / "source-files"
        if man is None:
            man = ingest(self.project_dir, src)
        sd = Path(man["source_dir"])
        if not sd.is_absolute():
            sd = self.project_dir / sd
        if not sd.exists():
            sd = src
        c = self.cfg["corpus"]
        self.corpus = Corpus({**man, "source_dir": str(sd)}, c.get("chunk_words", 320), c.get("chunk_overlap_words", 40))


def cmd_frame(a) -> int:
    from .index import build_index_requests, compact_index, parse_index, render_index
    from .llm.base import LLMRequest
    proj = Path(a.project)
    frame = proj / "01_FRAME"
    qf = frame / "question.md"
    if not qf.exists():
        print(f"No {qf}. Run `cr new` first.", file=sys.stderr)
        return 2
    question = read_text(qf)
    if re.search(r"^REPLACE\b", question, re.M):
        print(f"{qf} still has REPLACE lines. Write your question, scope, rival answers and discriminating "
              f"evidence there, then run this again.", file=sys.stderr)
        return 2
    s = _Setup(proj)
    if not s.llm.is_model_role("indexer"):
        print("Note: no model is configured (see `cr new --keys`). The offline local engine will draft the "
              "index and prompts; expect rough drafts.")
    name = s.cfg["project"]["name"]
    # 1. index
    ip = frame / "index.md"
    if ip.exists() and not a.force:
        print(f"index: kept {ip}")
    else:
        reqs = build_index_requests(s, question)
        print(f"index: reading {len(reqs)} sources ...")
        res = s.llm.call_many(reqs)
        entries = []
        for r, x in zip(reqs, res):
            d = x.parsed if x and isinstance(x.parsed, dict) else {}
            entries.append({"filename": r.meta["filename"], "rank": (str(d.get("rank") or "C").strip()[:1] or "C").upper(),
                            "author_year_title": d.get("author_year_title", ""), "relevance": d.get("relevance", ""),
                            "summary": d.get("summary", ""),
                            "contradictions_and_gaps": d.get("contradictions_and_gaps", "")})
        ip.write_text(render_index(entries, name), encoding="utf-8")
        ranks = {k: sum(1 for e in entries if e["rank"] == k) for k in "ABCF"}
        print(f"index: written ({', '.join(f'{k}: {v}' for k, v in ranks.items() if v)}) -> {ip}")
    idx = compact_index(parse_index(read_text(ip), s.corpus), s.corpus)
    # 2. Archivist custom prompt
    ap = frame / "archivist-custom-prompt.txt"
    if ap.exists() and not a.force:
        print(f"Archivist prompt: kept {ap}")
    else:
        system, user, _ = s.prompts.render("archivist_writer.md", HEADER=question, INDEX=idx)
        res = s.llm.call(LLMRequest(role="archivist_writer", system=system, user=user, expect_json=False,
                                    tag="archivist-prompt"))
        text = res.text.strip()
        ap.write_text(text + "\n", encoding="utf-8")
        banned = [w for w in ("ACH", "hypothesis", "Investigator", "Coordinator", "FRD", "witness", "crux")
                  if re.search(rf"\b{w}\b", text, re.I)]
        print(f"Archivist prompt: written ({len(text.split())} words) -> {ap}"
              + (f"   WARNING: it contains project words the notebook must not see: {', '.join(banned)}"
                 if banned else ""))
    # 3. header draft
    hd = frame / "header-DRAFT.md"
    if (frame / "header.md").exists() and not a.force:
        print(f"header: {frame / 'header.md'} already exists and was left alone")
    else:
        system, user, _ = s.prompts.render("header_draft.md", FRAME=question, INDEX=idx, ARCHIVIST=read_text(ap),
                                           RUN_ID=name, GAUGE=a.gauge, AXES=a.axes)
        res = s.llm.call(LLMRequest(role="investigator", system=system, user=user, expect_json=False,
                                    tag="header-draft", max_output_tokens=32000))
        inv, _, coord = res.text.partition("=====COORDINATOR=====")
        from .header import normalize_hypothesis_ids
        inv, id_map = normalize_hypothesis_ids(inv.strip() + "\n")
        if id_map:
            print("header: normalised axis ids for parsing: "
                  + ", ".join(f"{k} -> {v}" for k, v in id_map.items()))
        hd.write_text(inv, encoding="utf-8")
        if coord.strip():
            (frame / "coordinator-handoff-DRAFT.md").write_text(coord.strip() + "\n", encoding="utf-8")
        ok, msg = check_header(inv)
        print(f"header: DRAFT written -> {hd}\n        {msg}")
    print("\nNext:")
    print(f"  1. Read {hd}. Edit it until the hypotheses say what you mean. It is a draft until you approve it.")
    print(f"  2. python cr.py approve \"{proj}\" --by \"Your Name\"")
    print(f"  3. In each NotebookLM notebook copy: Configure Chat -> Custom, paste {ap.name}, choose Longer, Save.")
    print(f"  4. python cr.py doctor \"{proj}\"   then   python cr.py quest \"{proj}\"")
    return 0


def check_header(text: str) -> tuple[bool, str]:
    from .header import parse_header
    try:
        fr = parse_header(text)
    except Exception as e:  # noqa: BLE001
        return False, f"the header could not be parsed ({type(e).__name__}: {e})"
    axes = fr.get("axes", [])
    if not axes:
        return False, "no axis with hypotheses was found; the header needs at least one axis with rival hypotheses"
    thin = [ax["axis_id"] for ax in axes if len(ax.get("hypotheses", [])) < 2]
    if thin:
        return False, f"axis {', '.join(thin)} has fewer than two hypotheses"
    return True, ("parsed: " + "; ".join(f"axis {ax['axis_id']} with {len(ax['hypotheses'])} hypotheses "
                                           f"({str(ax.get('approval') or 'approval not stated').lower()})"
                                           for ax in axes) + f"; gauge {fr.get('gauge')}; "
                  f"{len(fr.get('decisive_tests', []))} decisive tests")


def cmd_approve(a) -> int:
    proj = Path(a.project)
    frame = proj / "01_FRAME"
    src = Path(a.header) if a.header else frame / "header-DRAFT.md"
    dst = frame / "header.md"
    if not src.exists() and not dst.exists():
        print(f"Nothing to approve: {src} does not exist. Run `cr frame` first.", file=sys.stderr)
        return 2
    if dst.exists() and src.exists() and not a.force and read_text(src) != read_text(dst):
        print(f"{dst} already exists and differs from {src.name}. Use --force to replace it.", file=sys.stderr)
        return 2
    from .header import normalize_hypothesis_ids
    text, id_map = normalize_hypothesis_ids(read_text(src if src.exists() else dst))
    if id_map:
        print("normalised axis ids for parsing: " + ", ".join(f"{k} -> {v}" for k, v in id_map.items()))
    ok, msg = check_header(text)
    print(msg)
    if not ok:
        print("Not approved: fix the draft and run this again.", file=sys.stderr)
        return 2
    # machine-readable approval marker: the parser trusts this, never a model's prose
    if not re.search(r"<!--\s*APPROVED[:\s].*?-->", text, re.S | re.I):
        marker = f"<!-- APPROVED: {a.by} on {utcnow()[:10]} -->"
        lines = text.splitlines()
        lines.insert(1 if lines and lines[0].startswith("#") else 0, marker)
        text = "\n".join(lines) + "\n"
    dst.write_text(text, encoding="utf-8")
    cfg = read_json(proj / "project.json", default={}) or {}
    cfg.setdefault("frame", {})["approval_note"] = f"Header approved by {a.by} on {utcnow()[:10]}."
    write_json(proj / "project.json", cfg)
    print(f"Approved by {a.by}: {dst}")
    return 0


# --------------------------------------------------------------------------- #
# cr doctor
# --------------------------------------------------------------------------- #

def _get_json(url: str, headers: dict, timeout: float = 30) -> tuple[int, object]:
    req = urllib.request.Request(url, method="GET")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")[:300]
    except Exception as e:  # noqa: BLE001
        return 0, f"{type(e).__name__}: {e}"


def list_models(pcfg: dict) -> tuple[list[str], str]:
    """The provider's own list of model ids ([] with a reason when it cannot be read)."""
    from .llm.providers import _api_key
    try:
        key = _api_key(pcfg)
    except Exception as e:  # noqa: BLE001
        return [], str(e)
    base = str(pcfg.get("base_url", "")).rstrip("/")
    if pcfg.get("type") == "anthropic":
        code, data = _get_json(base + "/models?limit=1000", {"x-api-key": key, "anthropic-version": "2023-06-01"})
    else:
        code, data = _get_json(base + "/models", {"Authorization": f"Bearer {key}"})
        if code != 200 and "generativelanguage" in base:
            code, data = _get_json("https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000",
                                   {"x-goog-api-key": key})
    if code != 200 or not isinstance(data, dict):
        return [], f"HTTP {code}: {str(data)[:160]}"
    rows = data.get("data") or data.get("models") or []
    ids = [str(m.get("id") or m.get("name") or "") for m in rows if isinstance(m, dict)]
    return sorted({i.split("/")[-1] for i in ids if i}), ""


def pick_model(name: str, available: list[str]) -> str | None:
    for pat in PRESETS.get(name, {}).get("prefer", ()):
        hits = sorted(m for m in available if re.search(pat, m))
        if hits:
            return hits[-1]
    return None


# NotebookLM notebook links.  One notebook copy is one lane, so a link that silently fails to open
# costs a quarter of a six-lane quest's throughput for the whole run.  These checks are offline and
# cheap; `cr doctor --notebooks` additionally opens each link with Playwright.

NOTEBOOK_HOSTS = ("notebook.google.com", "notebooklm.google.com")
_NOTEBOOK_PATH_RE = re.compile(r"/notebook/([^/?#]+)")
_NOTEBOOK_ID_RE = re.compile(r"[0-9a-f-]{16,}", re.I)


def notebook_link_problems(links) -> list[tuple[int, str]]:
    """What is wrong with each saved notebook link, checked without any network call.

    Returns ``[(1-based index, problem), ...]``; an empty list means every link looks usable.  A
    usable link is an https URL on ``notebook.google.com`` or ``notebooklm.google.com``, with
    ``/notebook/<id>`` in its path where the id has at least 16 hex/dash characters, and no id is
    repeated (a repeated id means two lanes would open the same notebook).
    """
    problems: list[tuple[int, str]] = []
    seen: dict[str, int] = {}
    for i, raw in enumerate(links or [], 1):
        bad: list[str] = []
        link = "" if raw is None else str(raw).strip()
        try:
            parts = urllib.parse.urlsplit(link)
        except ValueError as e:
            bad.append(f"not a URL ({e})")
            parts = None
        if parts is not None:
            if parts.scheme.lower() != "https":
                bad.append("not an https URL")
            host = (parts.hostname or "").lower()
            if host not in NOTEBOOK_HOSTS:
                bad.append("the host is not notebook.google.com or notebooklm.google.com"
                           + (f" (got {host})" if host else " (no host in the link)"))
            m = _NOTEBOOK_PATH_RE.search(parts.path or "")
            if not m:
                bad.append("the path has no /notebook/<id>")
            else:
                nb_id = m.group(1)
                if not _NOTEBOOK_ID_RE.fullmatch(nb_id) or not re.search(r"[0-9a-f]", nb_id, re.I):
                    bad.append(f"the notebook id {nb_id!r} is not plausible (needs 16+ hex/dash characters)")
                elif nb_id.lower() in seen:
                    bad.append(f"duplicate of notebook {seen[nb_id.lower()]} (id {nb_id})")
                else:
                    seen[nb_id.lower()] = i
        if bad:
            problems.append((i, "; ".join(bad)))
    return problems


_NOT_FOUND_PHRASES = ("not found", "couldn't find", "could not find", "request access", "requesting access",
                      "you need permission", "you don't have permission", "access denied",
                      "no longer available", "doesn't exist", "does not exist")


def _notebook_page_problem(title: str, url: str, body: str) -> str | None:
    """Why an opened page does not look like the notebook the link named, or None when it does.

    NotebookLM answers a bad or unshared id with an error page ("Couldn't find that notebook",
    "Request access") or by sending the browser to the Google sign-in page.  Either way the page is
    not the notebook, so the link is not usable for a quest.
    """
    text = f"{title or ''}\n{(body or '')[:20000]}".lower()
    for phrase in _NOT_FOUND_PHRASES:
        if phrase in text:
            return f"the page says the notebook is unavailable ({phrase!r})"
    if not re.search(r"/notebook/[0-9a-f-]{16,}", url or "", re.I):
        return f"the final URL is not a notebook URL: {url}"
    return None


def check_notebooks_online(notebooks, profile_dir, timeout_ms: int = 45000):
    """Open each notebook link in the driver's own Chrome profile and see whether it resolves.

    Returns ``[(ok, detail), ...]`` aligned with *notebooks*, or ``None`` when Playwright is not
    importable (the caller prints a warning and skips).  The context is a persistent one on
    ``profile_dir`` so the saved Google sign-in is used; installed Chrome is used via
    ``channel="chrome"`` and headless is tried first, then a visible window.  The context is always
    closed.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    profile = str(Path(os.path.expanduser(str(profile_dir))).resolve())
    results: list[tuple[bool, str]] = []
    with sync_playwright() as p:
        ctx = None
        failure = ""
        try:
            for headless in (True, False):
                try:
                    ctx = p.chromium.launch_persistent_context(
                        profile, headless=headless, channel="chrome",
                        args=["--disable-background-timer-throttling", "--disable-backgrounding-occluded-windows",
                              "--disable-renderer-backgrounding"],
                        ignore_default_args=["--enable-automation"], bypass_csp=True)
                    break
                except Exception as e:  # noqa: BLE001
                    failure = f"{type(e).__name__}: {e}"[:300]
            if ctx is None:
                return [(False, f"could not open Chrome with the driver profile: {failure}")] * len(notebooks)
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            for url in notebooks:
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                    # A page with the notebook's chat box is the notebook, whatever its text says: its
                    # body holds the chat history, and Archivist answers often say "not found in the
                    # sources", which must not read as an error page.
                    try:
                        page.wait_for_selector('textarea[aria-label="Query box"]', timeout=20000)
                        results.append((True, f"title: {(page.title() or '').strip()}"))
                        continue
                    except Exception:  # noqa: BLE001 - no chat box: look for the error page below
                        pass
                    title = (page.title() or "").strip()
                    final = page.url or ""
                    try:
                        body = page.locator("body").inner_text(timeout=10000)
                    except Exception:  # noqa: BLE001
                        body = ""
                    problem = _notebook_page_problem(title, final, body)
                    results.append((problem is None, f"title: {title}" if problem is None else problem))
                except Exception as e:  # noqa: BLE001
                    results.append((False, f"{type(e).__name__}: {str(e)[:180]}"))
        finally:
            if ctx is not None:
                try:
                    ctx.close()
                except Exception:  # noqa: BLE001
                    pass
    return results


def cmd_doctor(a) -> int:
    rows: list[tuple[str, str, str]] = []

    def add(status, what, detail=""):
        rows.append((status, what, detail))
    v = sys.version_info
    add("PASS" if v >= (3, 11) else "FAIL", f"Python {v.major}.{v.minor}", "" if v >= (3, 11) else "3.11 or newer is needed")
    try:
        import playwright  # noqa: F401
        add("PASS", "Playwright is installed")
    except ImportError:
        add("WARN", "Playwright is not installed", "needed for the NotebookLM quest: pip install playwright")
    from .notebooklm.driver import find_chrome
    add("PASS" if find_chrome() else "WARN", "Google Chrome " + ("found" if find_chrome() else "not found"),
        "" if find_chrome() else "install Chrome, or set \"channel\": \"\" in quest.json and run: playwright install chromium")
    if not a.project:
        if getattr(a, "notebooks", False):
            add("WARN", "notebook link check skipped", "pass a project folder so its saved notebook links can be read")
        return _doctor_print(rows)
    proj = Path(a.project)
    if not (proj / "project.json").exists():
        add("FAIL", f"{proj} is not a project", "run `cr new` first")
        return _doctor_print(rows)
    cfg = load_config(proj)
    frame = proj / "01_FRAME"
    from .corpus import current_manifest
    man = current_manifest(proj)
    add("PASS" if man else "FAIL", f"Corpus: {man['files']} sources" if man else "Corpus: no manifest",
        "" if man else "put Markdown sources in 01_CORPUS/source-files and run `cr corpus`")
    if man:
        flagged = [s["filename"] for s in man["sources"] if s["flags"]]
        if flagged:
            add("WARN", f"{len(flagged)} source(s) look like bad conversions or duplicates",
                ", ".join(flagged[:6]) + (" ..." if len(flagged) > 6 else ""))
    if (frame / "header.md").exists():
        ok, msg = check_header(read_text(frame / "header.md"))
        add("PASS" if ok else "FAIL", "Header " + ("approved and parsed" if ok else "does not parse"), msg)
        from . import frame_gate
        signed, why = frame_gate.accepted(proj)
        add("PASS" if signed else "WARN", "Frame accepted with the coach" if signed else "Frame not yet through the coach",
            why if signed else f"{why}; run `cr sign \"{proj}\"`")
    else:
        add("FAIL", "No approved header (01_FRAME/header.md)", "run `cr frame`, review the draft, then `cr approve`")
    add("PASS" if (frame / "index.md").exists() else "FAIL", "Index " + ("present" if (frame / "index.md").exists() else "missing"),
        "" if (frame / "index.md").exists() else "run `cr frame`")
    add("PASS" if (frame / "archivist-custom-prompt.txt").exists() else "WARN",
        "Archivist prompt " + ("present" if (frame / "archivist-custom-prompt.txt").exists() else "missing"),
        "paste it into every notebook copy: Configure Chat -> Custom + Longer")
    nbs = (cfg.get("notebooklm") or {}).get("notebooks") or []
    add("PASS" if nbs else "WARN", f"NotebookLM: {len(nbs)} notebook link(s) saved" if nbs else "NotebookLM: no notebook link saved",
        "one link = one lane; 3 to 6 copies of the notebook give the 45+ answers an hour the method assumes"
        if len(nbs) < 3 else "")
    if nbs:
        # one row per link: the offline shape check always runs; --notebooks also opens each link
        bad = dict(notebook_link_problems(nbs))
        online = bool(getattr(a, "notebooks", False)) and not bool(getattr(a, "offline", False))
        opened: dict[int, tuple[bool, str]] = {}
        if online:
            to_open = [(i, str(u)) for i, u in enumerate(nbs, 1) if i not in bad]
            if to_open:
                profile = (cfg.get("notebooklm") or {}).get("profile_dir") or str(HARNESS_ROOT / ".notebooklm-profile")
                results = check_notebooks_online([u for _, u in to_open], profile)
                if results is None:
                    add("WARN", "notebook online check skipped", "Playwright is not installed: pip install playwright")
                else:
                    for (i, _), (ok, detail) in zip(to_open, results):
                        opened[i] = (ok, detail)
        for i in range(1, len(nbs) + 1):
            if i in bad:
                add("FAIL", f"notebook {i}: link is not usable", bad[i])
            elif i in opened:
                ok, detail = opened[i]
                add("PASS" if ok else "FAIL",
                    f"notebook {i}: " + ("opens in NotebookLM" if ok else "does not open in NotebookLM"), detail)
            else:
                add("PASS", f"notebook {i}: link looks valid")
    # providers actually used by the roles that matter
    from .llm.router import LLM
    llm = LLM(cfg, log_name="doctor-llm-calls.jsonl")
    used: list[str] = []
    for role in ("quest_manager", "quest_investigator", "frd_generator", "frd_validator", "witness_constructor",
                 "matcher_a", "unit_deriver"):
        for n in llm.chain_for(role):
            if n not in used:
                used.append(n)
    add("PASS" if any(cfg["providers"].get(n, {}).get("type") in ("openai", "anthropic") for n in used) else "WARN",
        "Model routing: " + " -> ".join(used),
        "" if len([n for n in used if cfg["providers"].get(n, {}).get("type") in ("openai", "anthropic")]) > 1
        else "only one model provider: a refusal or outage will stop the run; add a second key for failover")
    changed = False
    user_cfg = read_json(proj / "project.json", default={}) or {}
    for n in used:
        pcfg = cfg["providers"].get(n, {})
        if pcfg.get("type") not in ("openai", "anthropic"):
            continue
        if a.offline:
            from .llm.providers import _api_key
            try:
                _api_key(pcfg)
                add("PASS", f"{n}: key present", "not contacted (--offline)")
            except Exception as e:  # noqa: BLE001
                add("FAIL", f"{n}: no key", str(e))
            continue
        models, why = list_models(pcfg)
        model = pcfg.get("model")
        if getattr(a, "models", False) and models:
            add("INFO", f"{n}: {len(models)} models offered", ", ".join(models[:60]))
        if models and model not in models:
            pick = pick_model(n, models)
            if a.fix and pick:
                user_cfg.setdefault("providers", {}).setdefault(n, {})["model"] = pick
                pcfg = {**pcfg, "model": pick}
                changed = True
                add("PASS", f"{n}: model set to {pick}", f"{model} is not offered by this key")
                model = pick
            else:
                add("FAIL", f"{n}: model {model} is not offered by this key",
                    (f"`cr doctor --fix` would use {pick}. " if pick else "") + "Available: " + ", ".join(models[:25]))
                continue
        ok, detail = _smoke(n, pcfg, proj)
        if not ok and a.fix and re.search(r"HTTP 404|not found|no longer available", detail, re.I):
            # the provider lists the model but will not serve it: take the model its own error
            # message recommends, or the best other model on its list
            hinted = [m for m in re.findall(r"models/([A-Za-z0-9.\-]+)", detail) if m != model]
            for cand in hinted + [pick_model(n, [m for m in models if m != model])]:
                if not cand:
                    continue
                ok2, detail2 = _smoke(n, {**pcfg, "model": cand}, proj)
                if ok2:
                    user_cfg.setdefault("providers", {}).setdefault(n, {})["model"] = cand
                    changed = True
                    add("PASS", f"{n}: model set to {cand}", f"{model} is no longer served")
                    model, ok, detail = cand, True, detail2
                    break
        add("PASS" if ok else "FAIL", f"{n}: {model} " + ("answers" if ok else "does not answer"),
            detail or ((why and f"(model list unavailable: {why})") or ""))
    if changed:
        write_json(proj / "project.json", user_cfg)
    return _doctor_print(rows)


SMOKE_USER = """COVERAGE UNIT U1: "Drug A improves detrusor contractility in obstructed rats."

WITNESSES:
[W1] After four weeks of oral dosing, drug A improved detrusor contractility in obstructed rats (12 per group).
[W2] Drug A produced no significant change in detrusor contractility in obstructed rats.
[W3] Beta-blockers reduce mortality after myocardial infarction.

For each witness say whether, accepted as written, it makes the unit true (ENTAILS), makes it false (CONTRADICTS) or is unrelated (NONE).
Return ONLY a JSON object: {"judgments": [{"witness_id": "", "relation": "", "trace": "one sentence"}]}"""


def _smoke(name: str, pcfg: dict, proj: Path) -> tuple[bool, str]:
    """One small, realistic JSON task.  Reports whether the answer parsed, how long it took and how
    the model spent its output budget, so an empty or slow provider shows up before a long run."""
    from .llm.base import LLMRequest
    from .llm.jsonparse import extract_json
    from .llm.providers import make_provider
    t = time.time()
    try:
        prov = make_provider(name, {**pcfg, "timeout_s": 180}, proj)
        r = prov.complete(LLMRequest(role="doctor", system="You are a careful reviewer. Reply with JSON only.",
                                     user=SMOKE_USER), "doctor")
    except Exception as e:  # noqa: BLE001
        return False, str(e)[:400]
    secs = time.time() - t
    info = (f"{secs:.0f}s, finish {r.finish_reason or '?'}, {r.usage.get('output_tokens', '?')} output tokens"
            + (f" ({r.usage['reasoning_tokens']} spent reasoning)" if r.usage.get("reasoning_tokens") else ""))
    if not (r.text or "").strip():
        return False, f"empty answer ({info}); raise max_output_tokens for this provider in project.json"
    try:
        js = extract_json(r.text)
        rel = [str(j.get("relation", "")).upper() for j in js.get("judgments", [])]
    except Exception:  # noqa: BLE001
        return False, f"the answer was not the JSON asked for ({info}): {r.text[:120]!r}"
    right = rel[:3] == ["ENTAILS", "CONTRADICTS", "NONE"]
    return True, f"test task answered in {info}" + ("" if right else f"; judgments {rel} (expected ENTAILS, CONTRADICTS, NONE)")


def _doctor_print(rows) -> int:
    for status, what, detail in rows:
        print(f"[{status}] {what}" + (f"\n       {detail}" if detail else ""))
    fails = sum(1 for r in rows if r[0] == "FAIL")
    warns = sum(1 for r in rows if r[0] == "WARN")
    print(f"\n{'Ready.' if not fails else 'Not ready:'} {fails} problem(s), {warns} warning(s).")
    return 0 if not fails else 2


# --------------------------------------------------------------------------- #
# cr quest
# --------------------------------------------------------------------------- #

def _quest_dir(proj: Path, quest_id: str | None, new: bool) -> Path:
    base = ensure_dir(proj / "quest")
    if quest_id:
        return base / quest_id
    if not new:
        open_q = [d for d in sorted(base.iterdir()) if d.is_dir() and (d / "quest.json").exists()
                  and not (d / "CLOSEOUT.md").exists()]
        if open_q:
            return open_q[-1]
    stamp = time.strftime("%Y-%m-%d")
    n, d = 1, base / f"QUEST-{stamp}"
    while d.exists():
        n += 1
        d = base / f"QUEST-{stamp}-{n}"
    return d


# The driver prints "lane <name> ready" once per notebook once its tab has the runner in it.  The
# quest fits as many lanes as there are notebooks, so a missing lane line means a link did not open.
DRIVER_PREFLIGHT_S = 150.0
MINIMIZED_WINDOW_WARNING = (
    "Keep the driver's Chrome window unminimized for the whole quest; a minimized window throttles the "
    "notebook tabs. The driver now tries to restore a minimized window automatically.")
_LANE_READY_RE = re.compile(r"lane (.+?) ready(?:\s|$)")


def _driver_env(environ=None) -> dict:
    """The driver's environment: unbuffered stdout so driver.log is live while the quest runs."""
    return {**(os.environ if environ is None else environ), "PYTHONUNBUFFERED": "1"}


def _driver_log_lines(log_path) -> list[str]:
    try:
        return Path(log_path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def _ready_lanes(text: str) -> set[str]:
    """The distinct lane names that have printed ``lane <name> ready`` in a chunk of driver log."""
    return {m.group(1).strip() for line in (text or "").splitlines()
            if (m := _LANE_READY_RE.match(line.strip()))}


def _preflight_lanes(proc, log_path, expected: int, timeout: float = DRIVER_PREFLIGHT_S,
                     poll: float = 1.0, start_lines: int = 0) -> tuple[set[str], bool, list[str]]:
    """Wait until the driver has brought up *expected* lanes, or it exits, or the timeout passes.

    *start_lines* is the number of lines already in the log before this driver started, so lines
    left by an earlier run of the same quest do not count (a resume would otherwise pass at once).
    Returns ``(ready lane names, whether every lane came up, last 30 log lines)``.
    """
    deadline = time.time() + float(timeout)
    while True:
        lines = _driver_log_lines(log_path)
        new_lines = lines[int(start_lines):] if int(start_lines) <= len(lines) else lines
        ready = _ready_lanes("\n".join(new_lines))
        if len(ready) >= expected:
            return ready, True, lines[-30:]
        if proc is not None and proc.poll() is not None:
            return ready, False, lines[-30:]
        if time.time() >= deadline:
            return ready, False, lines[-30:]
        time.sleep(poll)


def _stop_process(proc, wait: float = 10.0) -> None:
    """Stop the driver process without letting a failure to stop it hide the original problem."""
    if proc is None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=wait)
    except Exception:  # noqa: BLE001
        try:
            proc.kill()
            proc.wait(timeout=5)
        except Exception:  # noqa: BLE001
            pass


def cmd_quest(a) -> int:
    from .notebooklm import driver as drv
    from .notebooklm.relay import Relay, local_now
    proj = Path(a.project).resolve()
    cfg = load_config(proj)
    ok, msg = check_header(read_text(proj / "01_FRAME" / "header.md")) if (proj / "01_FRAME" / "header.md").exists() \
        else (False, "there is no approved header (01_FRAME/header.md); run `cr frame` and `cr approve` first")
    if not ok:
        print(f"quest: {msg}", file=sys.stderr)
        return 2
    from . import frame_gate
    ok, msg = frame_gate.gate(proj, "quest")
    if msg:
        print(msg if ok else f"quest: {msg}", file=sys.stderr if not ok else sys.stdout)
    if not ok:
        return 2
    q = _quest_dir(proj, a.id, a.new)
    qj = q / "quest.json"
    go = local_now()
    if not qj.exists():
        nbs = list(a.notebook or []) or (cfg.get("notebooklm") or {}).get("notebooks") or []
        if not nbs:
            print("quest: no NotebookLM notebook link. Pass --notebook <url> (repeat it for each copy of the "
                  "notebook), or save them with `cr new --notebook`.", file=sys.stderr)
            return 2
        notebooks = {("primary" if i == 0 else f"clone-{i}"): u for i, u in enumerate(nbs)}
        profile = a.profile or (cfg.get("notebooklm") or {}).get("profile_dir") or str(HARNESS_ROOT / ".notebooklm-profile")
        ensure_dir(q)
        write_json(qj, {"run_id": f"{cfg['project'].get('run_prefix', proj.name)}-{q.name}", "project": "../..",
                        "notebooks": notebooks, "answers_dir": "answers", "profile_dir": str(Path(profile).resolve()),
                        "channel": "chrome", "max_backlog": 12, "assessed_file": "answers/assessed-qids.json",
                        "poll_seconds": 3, "round_size": 6, "max_hours": float(a.hours),
                        "max_questions": int(a.max_questions)})
        print(f"quest folder: {q}")
    else:
        print(f"resuming quest: {q}")
    qcfg = read_json(qj)
    ensure_dir(q / "answers" / "queue")
    clock = q / "answers" / "quest-clock.json"
    stale = q / "answers" / "queue" / "STOP"
    if stale.exists():
        stale.unlink()
    proc = None
    if not a.no_driver:
        try:
            import playwright  # noqa: F401
        except ImportError:
            print("quest: Playwright is not installed. Run:  pip install playwright", file=sys.stderr)
            return 2
        profile = Path(qcfg["profile_dir"])
        if not profile.exists() or not any(profile.iterdir()):
            print("First use: a Chrome window will open. Sign in to the Google account that owns the notebooks, "
                  "check that a notebook opens, then CLOSE the window. The quest starts after that.")
            drv.login(drv.load(qj))
            write_json(clock, {**(read_json(clock, default={}) or {}), "go_ahead": local_now(),
                               "note": "go-ahead = after the one-time Google sign-in"})
        print(MINIMIZED_WINDOW_WARNING)
        driver_log = q / "driver.log"
        start_lines = len(_driver_log_lines(driver_log))
        log = open(driver_log, "a", encoding="utf-8")
        try:
            proc = subprocess.Popen([sys.executable, "-m", "claimreg.notebooklm.driver", "run", str(qj)],
                                    cwd=str(HARNESS_ROOT), stdout=log, stderr=subprocess.STDOUT,
                                    env=_driver_env())
        finally:
            log.close()
        print(f"NotebookLM driver started (log: {driver_log}). A Chrome window opens with one tab per notebook; "
              f"leave it open.")
        expected = len(qcfg.get("notebooks") or {})
        if expected:
            print(f"Waiting up to {int(DRIVER_PREFLIGHT_S)}s for {expected} notebook lane(s) to be ready "
                  f"(log: {driver_log}) ...")
            ready, ok, tail = _preflight_lanes(proc, driver_log, expected, start_lines=start_lines)
            if not ok:
                print(f"quest: only {len(ready)} of {expected} notebook lane(s) came up within "
                      f"{int(DRIVER_PREFLIGHT_S)}s. Check {driver_log}: a typo in a notebook link is the usual "
                      f"cause (run `cr doctor --notebooks` to open each link online).", file=sys.stderr)
                if tail:
                    print(f"--- {driver_log} (last {len(tail)} lines) ---", file=sys.stderr)
                    for line in tail:
                        print(line, file=sys.stderr)
                    print("--- end of log ---", file=sys.stderr)
                _stop_process(proc)
                return 2
            print(f"All {len(ready)} notebook lane(s) ready: {', '.join(sorted(ready))}")
    # Stamp the go-ahead only now: the driver (and, with a profile, every lane) is up, so a failed
    # preflight cannot leave an early clock behind that would make a later, fixed attempt look slow.
    c = read_json(clock, default={}) or {}
    if not c.get("go_ahead"):
        write_json(clock, {**c, "run_id": qcfg.get("run_id", ""), "go_ahead": go,
                           "note": "go-ahead = the moment `cr quest` started the quest"})
    print(f"Status file: {q / 'relay-status.json'}.  To stop early: create an empty file named STOP in {q}.")
    relay = Relay(qj)
    try:
        st = relay.run()
    finally:
        if proc is not None:
            try:
                proc.wait(timeout=240)
            except subprocess.TimeoutExpired:
                proc.terminate()
    if proc is not None and st["answers_usable"] == 0:
        print(f"quest: no answer was captured. Check {q / 'driver.log'} (is the notebook signed in and on "
              f"Custom + Longer?).", file=sys.stderr)
        return 2
    # import into a run so `cr run` continues at FRD generation
    from .quest_import import QuestImportError, import_quest
    try:
        out = import_quest(proj, q, run_id=None, closeout=q / "CLOSEOUT.md", select=[],
                           stop="scientific" if relay.manager_stop else "operational",
                           exclude_tool_output=False, force=False)
    except QuestImportError as e:
        print(f"quest finished, but the import failed: {e}", file=sys.stderr)
        return 2
    run_id = out.get("run_id") if isinstance(out, dict) else None
    print(f"\nQuest imported as run {run_id}: {st['answers_graded']} graded answers.")
    cmd = f"python cr.py run \"{proj}\"" + (f" --run {run_id}" if run_id else "")
    if a.then_run:
        from .pipeline import run_pipeline
        from .runctx import RunContext
        ctx = RunContext(proj, run_id, create=True)
        res = run_pipeline(ctx)
        print(json.dumps(res, indent=2, default=str))
        if res.get("status") == "complete":
            from .pipeline import print_outputs
            print_outputs(ctx)
        if res.get("status") == "halted":
            print(f"\nHalted for your decision after {res['gate']}. Read {ctx.run_dir / res['read']}\n"
                  f"To run the later stages:\n  {res['continue_with']}")
        return 0 if res.get("status") in ("complete", "waiting", "halted") else 2
    print(f"Next: {cmd}")
    return 0
