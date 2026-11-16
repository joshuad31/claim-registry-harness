"""`cr next`: where a project stands on the way to its first quest, the one next step, and why.

Claim Registry is operated through whatever AI assistant the person already uses (Codex, Cursor,
Claude, ...).  That assistant is the interface.  What no chat window gives the person is a steady
sense of where they are, so this module computes it from the project's files:

    cr next                      no project yet: the path, and the first step
    cr next <project>            checklist with a bar per step, the next step and its reason
    cr next <project> --json     the same, for the assistant to read
    cr next <project> --md       the same as a Markdown table, for the assistant to show
    cr next <project> --window   writes <project>/CHECKLIST.html and opens it; the page reloads itself
    cr next <project> --watch    keeps that page current until interrupted
    cr next <project> --done sources | notebook     records something only the person can confirm
    cr next <project> --undo sources | notebook

Progress lives in the files, never in an assistant's memory, so any assistant that asks gets the
same answer.  A step is done because its files say so.  Two things files cannot show (that the
collection of sources is complete, and that every notebook copy is set to Custom and Longer) are
recorded as the person's own confirmation and labelled that way.

This is a reading aid.  It makes no model call, contacts nothing, changes no setting, and is not a
gate: `cr quest` decides for itself what it needs.
"""

from __future__ import annotations

import html
import importlib.util
import re
import sys
import time
from pathlib import Path

from .util import atomic_write_text, read_json, read_text, utcnow, write_json

HARNESS_ROOT = Path(__file__).resolve().parent.parent
GUIDE_DIR = HARNESS_ROOT / "docs" / "guide"
GUIDE_PAGES = ("what-it-does", "how-it-differs", "the-work", "what-you-get", "worth-it", "distillation", "roles",
               "hypotheses", "getting-papers", "sources", "notebooklm")
CONFIRMABLE = ("sources", "notebook")
STATE_FILE = "CHECKLIST.json"
PAGE_FILE = "CHECKLIST.html"

# id, title, why (the motivation), guide page
STEPS = (
    ("question", "Say what you want to research",
     "Everything after this is aimed at your question. A vague question gives a vague search and a result "
     "you cannot use.", "what-it-does"),
    ("hypotheses", "Draft the competing answers",
     "Claim Registry does not answer a question. It tests rival answers against each other, so without a "
     "serious rival there is nothing to test.", "hypotheses"),
    ("sources", "Collect your sources",
     "The result can only be as good as what is in the pile. A source you leave out cannot count for or "
     "against anything.", "getting-papers"),
    ("convert", "Convert the sources to text and check them",
     "Every quotation in the result is checked word for word against these files. A table that breaks here "
     "is a finding that goes missing later.", "sources"),
    ("index", "Map the sources",
     "The map tells the question-writer which source to ask about, and the Archivist prompt makes NotebookLM "
     "answer from your sources only, with a citation beside each number.", "roles"),
    ("frame", "Settle the wording of your claim",
     "The wording decides what the run can find. This is the one place you may lean toward the answer you "
     "hope for, in the open. After it, the evidence steps cannot be steered.", "hypotheses"),
    ("notebook", "Set up NotebookLM",
     "NotebookLM is the Archivist: it holds your sources and answers one cited question at a time, without "
     "knowing what you hope to find.", "notebooklm"),
    ("tools", "Check the tools",
     "A quest runs by itself for up to three hours. A missing piece found now costs a minute; found "
     "mid-quest it costs the run.", "the-work"),
    ("launch", "Launch your first quest",
     "This is where the distilling happens: narrow questions pull the passages that bear on your rival "
     "answers out of the pile.", "distillation"),
)
ORDER = [s[0] for s in STEPS]


# --------------------------------------------------------------------------- #
# reading the project
# --------------------------------------------------------------------------- #

def _sections(text: str) -> dict[str, str]:
    """question.md by its "## " headings (lower-cased heading -> body)."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*\S)\s*$", line)
        if m:
            cur = m.group(1).lower()
            out[cur] = ""
        elif cur is not None:
            out[cur] += line + "\n"
    return out


def _filled(body: str | None) -> bool:
    return bool(body and body.strip() and not re.search(r"^REPLACE\b", body, re.M))


def _find(secs: dict, *needles: str) -> str | None:
    for k, v in secs.items():
        if any(n in k for n in needles):
            return v
    return None


def _question(proj: Path) -> dict:
    """What 01_FRAME/question.md holds: {exists, decide, scope, rivals (count), tell_apart, freeform}."""
    qf = proj / "01_FRAME" / "question.md"
    if not qf.exists():
        return {"exists": False, "decide": False, "scope": False, "rivals": 0, "tell_apart": False, "freeform": False}
    text = read_text(qf)
    secs = _sections(text)
    decide, scope = _find(secs, "want to decide", "want to find", "question"), _find(secs, "scope", "about")
    rivals, apart = _find(secs, "competing", "hypothes", "rival"), _find(secs, "tell them apart", "evidence")
    if decide is None and rivals is None:
        # not the template: it can be read as "something was written", nothing finer
        written = len(text.split()) >= 30 and not re.search(r"^REPLACE\b", text, re.M)
        return {"exists": True, "decide": written, "scope": written, "rivals": 0, "tell_apart": False,
                "freeform": written}
    n = len(re.findall(r"^\s*(?:\d+[.)]|[-*])\s+\S", rivals or "", re.M)) if _filled(rivals) else 0
    return {"exists": True, "decide": _filled(decide), "scope": _filled(scope), "rivals": n,
            "tell_apart": _filled(apart), "freeform": False}


def _stem(name: str) -> str:
    s = name.lower()
    for ext in (".md", ".markdown", ".txt", ".pdf"):
        while s.endswith(ext):
            s = s[: -len(ext)]
    return s


def _corpus(proj: Path, cfg: dict) -> dict:
    from .config import resolve_path
    try:
        src = Path(resolve_path(cfg, cfg["corpus"]["source_dir"]))
    except Exception:  # noqa: BLE001
        src = proj / "01_CORPUS" / "source-files"
    exts = tuple(e.lower() for e in cfg.get("corpus", {}).get("extensions", [".md", ".markdown", ".txt"]))
    texts = [p for p in src.rglob("*") if p.is_file() and p.suffix.lower() in exts
             and not p.name.startswith(".")] if src.is_dir() else []
    roots = {proj / "01_CORPUS"} | ({src} if src.is_dir() else set())
    pdfs = {p.resolve() for r in roots if r.is_dir() for p in r.rglob("*.pdf") if p.is_file()}
    have = {_stem(p.name) for p in texts}
    waiting = sorted(p.name for p in pdfs if _stem(p.name) not in have)
    man = None
    try:
        from .corpus import current_manifest
        man = current_manifest(proj)
    except Exception:  # noqa: BLE001
        man = None
    flagged = [s["filename"] for s in (man or {}).get("sources", []) if s.get("flags")]
    return {"texts": len(texts), "pdfs_waiting": waiting, "manifest_files": (man or {}).get("files"),
            "flagged": flagged, "source_dir": str(src)}


def _launched(proj: Path) -> tuple[bool, str]:
    qd = proj / "quest"
    quests = sorted(p.parent.name for p in qd.glob("*/quest.json")) if qd.is_dir() else []
    if quests:
        return True, f"quest {quests[-1]} was started"
    for f in sorted((proj / "02_RUNS").glob("*/00_RUN-CONTROL/stage-state.json")) if (proj / "02_RUNS").is_dir() else []:
        st = read_json(f, default={}) or {}
        if (st.get("quest") or {}).get("status") == "done":
            return True, f"run {f.parent.parent.name} has a finished quest"
    return False, ""


def _n(k: int, word: str) -> str:
    return f"{k} {word}" + ("" if k == 1 else "s")


def _today() -> str:
    """The person's own date, for a confirmation they will read back."""
    return time.strftime("%Y-%m-%d")


def _item(sid: str, parts: list[tuple[bool, str]], detail: str, do: str, agent: str, basis: str = "checked from files",
          force_done: bool = False) -> dict:
    title, why, guide = next((t, w, g) for i, t, w, g in STEPS if i == sid)
    n_ok = sum(1 for ok, _ in parts if ok)
    progress = 100 if force_done or (parts and n_ok == len(parts)) else int(round(100 * n_ok / max(1, len(parts))))
    state = "done" if progress == 100 else ("started" if progress > 0 else "todo")
    return {"id": sid, "n": ORDER.index(sid) + 1, "title": title, "state": state, "progress": progress,
            "detail": detail, "missing": [label for ok, label in parts if not ok] if state != "done" else [],
            "basis": basis, "why": why, "do": do, "for_the_assistant": agent,
            "guide": f"docs/guide/{guide}.md"}


def build(project: str | Path | None) -> dict:
    """The checklist for a project folder (or for nobody yet when ``project`` is None or not a project)."""
    proj = Path(project).resolve() if project else None
    has = bool(proj and (proj / "project.json").exists())
    P = f'"{project}"' if project else '"projects/<ShortName>"'
    cr = "python cr.py"
    if not has:
        items = [_item("question", [(False, "")], "no project yet",
                       "Tell your assistant what you want to find out, and what you would do with the answer.",
                       f"Ask: \"What do you want to research?\" Then create the project with `{cr} new {P} --name "
                       f"\"<topic>\"` and write what they said under \"What I want to decide\" and \"Who or what "
                       f"it is about\" in 01_FRAME/question.md, in their words.")]
        for sid in ORDER[1:]:
            items.append(_item(sid, [(False, "")], "not started", "", ""))
        return _finish(None, None, items, {})

    from .config import load_config
    cfg = load_config(proj)
    saved = read_json(proj / STATE_FILE, default={}) or {}
    confirmed = dict(saved.get("confirmed") or {})
    launched, launch_note = _launched(proj)
    frame = proj / "01_FRAME"
    q = _question(proj)
    header_ok, header_msg = False, ""
    if (frame / "header.md").exists():
        from .onramp import check_header
        header_ok, header_msg = check_header(read_text(frame / "header.md"))
    draft = (frame / "header-DRAFT.md").exists()
    items = []

    # 1 question
    items.append(_item(
        "question", [(q["decide"], "what you want to decide"), (q["scope"], "who or what it is about")],
        "written" if (q["decide"] and q["scope"]) or header_ok else
        ("started" if q["exists"] and (q["decide"] or q["scope"]) else "not written yet"),
        "Tell your assistant what you want to find out, who or what it is about, and what you would do with the answer.",
        f"Write their answer, in their words, under \"What I want to decide\" and \"Who or what it is about\" in "
        f"{frame / 'question.md'}. Ask one thing at a time.", force_done=header_ok))

    # 2 hypotheses
    if q["freeform"] and not (header_ok or draft):
        hyp_parts = [(True, ""), (False, "the rival answers, as a list"), (False, "what evidence would tell them apart")]
        hyp_detail = "question.md is not in the template form, so the rival answers could not be counted"
    else:
        hyp_parts = [(q["rivals"] >= 1, "your own answer"), (q["rivals"] >= 2, "a serious rival answer"),
                     (q["tell_apart"], "what evidence would tell them apart")]
        hyp_detail = (_n(q["rivals"], "answer") + " listed" + ("" if q["tell_apart"] else "; what would tell them apart "
                                                           "is not written yet"))
    items.append(_item(
        "hypotheses", hyp_parts, "a header exists" if (header_ok or draft) else hyp_detail,
        "Say what you think the answer is, what a serious sceptic would say instead, and what evidence would "
        "tell the two apart.",
        f"Use one of the three ways in from docs/guide/hypotheses.md. Offer wordings as candidates only; the person "
        f"chooses and may keep a preferred answer. Include \"the evidence cannot decide\". Write the result under "
        f"\"The competing answers\" (a numbered list) and \"What evidence would tell them apart\" in "
        f"{frame / 'question.md'}.", force_done=header_ok or draft))

    # 3 sources
    c = _corpus(proj, cfg)
    total = c["texts"] + len(c["pdfs_waiting"])
    src_confirmed = bool(confirmed.get("sources")) or launched
    items.append(_item(
        "sources", [(total > 0, "at least one source"), (src_confirmed, "your word that the collection is complete")],
        (_n(total, "source") + " collected" if total else "none yet")
        + (f"; you said the collection is complete on {confirmed['sources']}" if confirmed.get("sources") else
           ("" if launched or not total else "; not yet confirmed complete")),
        "Decide with your assistant which sources belong in the pile, including the ones that disagree with you. "
        "It downloads the ones that are free to read and gives you a link for each of the others. Say when the "
        "collection is complete.",
        f"Do the legwork (AGENTS.md, \"Helping them get the papers\"). From their rival answers, search for sources "
        f"for and against each one and propose a short list; they decide what goes in. Download every paper that has "
        f"a free, lawful copy into {proj / '01_CORPUS' / 'pdf'}; text files go in {c['source_dir']}. For each one you "
        f"cannot download, tell them the exact reason and the way round it, and keep the list in {proj / 'SOURCES.md'}. "
        f"Never a pirate site. Keep search notes and reference lists out of both corpus folders. When they say "
        f"the collection is complete: `{cr} next {P} --done sources`.",
        basis="files counted; completeness is your own confirmation" if not launched else "checked from files"))

    # 4 convert
    stale = c["manifest_files"] is not None and c["manifest_files"] != c["texts"]
    items.append(_item(
        "convert", [(c["texts"] > 0, "at least one converted source"),
                    (c["texts"] > 0 and not c["pdfs_waiting"], _n(len(c["pdfs_waiting"]), "PDF") + " still to convert"),
                    (c["texts"] > 0 and c["manifest_files"] == c["texts"], "the sources registered with the project"),
                    (c["texts"] > 0 and c["manifest_files"] == c["texts"] and not c["flagged"],
                     _n(len(c["flagged"]), "file") + " that may be damaged or duplicated")],
        f"{c['texts']} converted" + (", " + _n(len(c["pdfs_waiting"]), "PDF") + " waiting" if c["pdfs_waiting"] else "")
        + (f", {len(c['flagged'])} flagged for a look" if c["flagged"] else "")
        + ("; the project's list of sources is out of date" if stale else ""),
        "Convert each PDF to text and look at a few with tables to see that the tables survived.",
        f"Read kits/research-paper-converter/AGENT-GUIDE.md. Preview with `{cr} convert {P} --dry-run`. "
        f"When conversion is requested and a Datalab key is available, explain the external upload/cost and run "
        f"`{cr} convert {P}` (accurate mode); otherwise help import their conversions into {c['source_dir']}. "
        f"Review extraction fidelity before `{cr} corpus {P}` and show them "
        f"any file it flags. Never print or copy an API key; refer to its file by path."))

    # 5 index
    idx, arch = (frame / "index.md").exists(), (frame / "archivist-custom-prompt.txt").exists()
    items.append(_item(
        "index", [(idx, "the map of the sources (index)"), (arch, "the Archivist prompt")],
        ", ".join(x for x in ("index written" if idx else "no index", "Archivist prompt written" if arch
                              else "no Archivist prompt")),
        "Nothing for you to do but read the short map your assistant shows you and say if a source is misdescribed.",
        f"`{cr} frame {P}` (it needs the question written and the sources registered; it also drafts the header). "
        f"Show them the ranks in {frame / 'index.md'} in a few lines, not the whole file."))

    # 6 frame
    from . import frame_gate
    try:
        acc, acc_why = frame_gate.accepted(proj)
    except Exception as e:  # noqa: BLE001
        acc, acc_why = False, f"could not be read ({type(e).__name__})"
    need_coach = bool((cfg.get("coach") or {}).get("require_acceptance", True))
    parts = [(draft or header_ok, "a drafted header"), (header_ok, "the header approved by you")]
    if need_coach:
        parts.append((acc, "the session with the coach"))
    items.append(_item(
        "frame", parts,
        ("accepted with the coach" if acc else "approved; not yet through the coach") if header_ok
        else ("draft written; not yet approved" if draft else "no header yet"),
        "Read your hypotheses as they will be tested, change the wording until it says what you mean, then go "
        "through them with the coach.",
        f"Walk them through {frame / ('header.md' if header_ok else 'header-DRAFT.md')} one hypothesis at a time, in "
        f"short pieces. Try the claim ladder (docs/guide/hypotheses.md). Edit to their wording. Only when they say "
        f"they accept it: `{cr} approve {P} --by \"<their name>\"`. The coach session is a terminal conversation "
        f"they have themselves: `{cr} sign {P}`. Do not answer it for them.",
        force_done=launched and header_ok))

    # 7 notebook
    nbs = (cfg.get("notebooklm") or {}).get("notebooks") or []
    from .onramp import notebook_link_problems
    bad = notebook_link_problems(nbs) if nbs else []
    nb_confirmed = bool(confirmed.get("notebook")) or launched
    items.append(_item(
        "notebook", [(bool(nbs) and not bad, "a working link to each notebook copy"),
                     (nb_confirmed, "your word that every copy is set to Custom and Longer")],
        (_n(len(nbs), "notebook link") + " saved" if nbs else "no notebook link saved")
        + (f"; {len(bad)} of them look wrong" if bad else "")
        + ("; 3 to 6 copies are recommended" if 0 < len(nbs) < 3 else "")
        + (f"; you confirmed the settings on {confirmed['notebook']}" if confirmed.get("notebook") else ""),
        "Create the notebook, upload your sources, paste the Archivist prompt under Configure Chat (Custom, Longer), "
        "make copies, and give your assistant each link.",
        f"Give them the five steps in docs/guide/notebooklm.md one at a time, and the text of "
        f"{frame / 'archivist-custom-prompt.txt'} to paste. Save the links in {proj / 'project.json'} under "
        f"\"notebooklm\": {{\"notebooks\": [...]}}. When they say every copy shows Custom and Longer: "
        f"`{cr} next {P} --done notebook`. They sign in to Google themselves; never ask for a password.",
        basis="links checked; the notebook settings are your own confirmation" if not launched else "checked from files",
        force_done=launched))

    # 8 tools
    py = sys.version_info >= (3, 11)
    pw = importlib.util.find_spec("playwright") is not None
    try:
        from .notebooklm.driver import find_chrome
        chrome = bool(find_chrome())
    except Exception:  # noqa: BLE001
        chrome = False
    keys = _keys(cfg)
    items.append(_item(
        "tools", [(py, "Python 3.11 or newer"), (pw, "Playwright (it drives the browser)"), (chrome, "Google Chrome")],
        ", ".join(x for x in (None if py else "Python is too old", "Playwright ready" if pw else "Playwright missing",
                              "Chrome found" if chrome else "Chrome not found") if x)
        + ("; " + (f"model keys found for {', '.join(keys)}" if keys else
                   "no model key, so your assistant writes the questions and scores the answers itself")),
        "Nothing, unless your assistant asks you to install Google Chrome.",
        f"`{cr} doctor {P}` and fix what it reports (`pip install playwright`). With no model key, run the quest by "
        f"hand with two separate contexts, one for each role: claimreg/notebooklm/INVESTIGATOR.md and MANAGER.md.",
        force_done=launched))

    # 9 launch
    items.append(_item(
        "launch", [(launched, "the quest")], launch_note or "not started",
        "Say go. The first time, a Chrome window opens for you to sign in to Google; then leave it open and visible.",
        f"`{cr} quest {P}`. It runs for up to three hours. Never put the hypotheses, the index or the scores into "
        f"NotebookLM, and keep the Investigator and the Manager in separate contexts."))
    if launched:
        # a quest has already run on this project: the steps before it are history, not open work.
        # What each one found stays in its detail line.
        for i in items:
            i.update(state="done", progress=100, missing=[])
    return _finish(proj, cfg, items, {"launched": launched})


def _keys(cfg: dict) -> list[str]:
    out = []
    try:
        from .llm.providers import _api_key
        for name, p in (cfg.get("providers") or {}).items():
            if p.get("type") in ("openai", "anthropic") and (p.get("api_key_env") or p.get("api_key_file")):
                try:
                    _api_key(p)
                    out.append(name)
                except Exception:  # noqa: BLE001
                    pass
    except Exception:  # noqa: BLE001
        pass
    return out


def _finish(proj, cfg, items, extra) -> dict:
    nxt = next((i for i in items if i["state"] != "done"), None)
    name = ((cfg or {}).get("project") or {}).get("name") if cfg else None
    out = {"project": str(proj) if proj else None, "name": name or (proj.name if proj else None),
           "percent": int(round(sum(i["progress"] for i in items) / len(items))),
           "steps_done": sum(1 for i in items if i["state"] == "done"), "steps": len(items),
           "items": items, "guide": "docs/guide/README.md", "time": utcnow(), **extra}
    if nxt:
        out["next"] = {k: nxt[k] for k in ("id", "n", "title", "why", "do", "missing", "for_the_assistant", "guide")}
    else:
        out["next"] = {"id": "after-launch", "n": len(items) + 1, "title": "Let the quest finish, then build the evidence",
                       "why": "The quest collects answers. The findings, the checks and the report are built from "
                              "them afterwards.",
                       "do": "Wait for the quest to end, then ask your assistant to build and show the result.",
                       "missing": [], "guide": "docs/guide/what-you-get.md",
                       "for_the_assistant": f"When the quest has closed: `python cr.py run \"{proj}\"`. Lead with "
                                            f"HYPOTHESIS-REQUIREMENTS.md and the premise ledger, a little at a time."}
    return out


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #

def _bar(pct: int, width: int = 10) -> str:
    k = int(round(width * pct / 100))
    return "[" + "#" * k + "-" * (width - k) + "]"


def _headline(st: dict) -> str:
    who = st["name"] or "no project yet"
    return f"Claim Registry: {who} - {st['steps_done']} of {st['steps']} steps done before your first quest"


def render_text(st: dict) -> str:
    L = [_headline(st), ""]
    for i in st["items"]:
        mark = {"done": "done", "started": f"{i['progress']}%", "todo": ""}[i["state"]]
        arrow = ">" if i["id"] == st["next"]["id"] else " "
        L.append(f"{arrow}{i['n']} {_bar(i['progress'])} {i['title']}" + (f"  ({mark})" if mark else ""))
    n = st["next"]
    L += ["", f"Next: {n['title']}", f"Why:  {n['why']}", f"You:  {n['do']}"]
    if any(n.get("missing") or []):
        L.append("Still needed: " + "; ".join(m for m in n["missing"] if m))
    L += [f"More: {n['guide']}"]
    return "\n".join(L) + "\n"


def render_markdown(st: dict) -> str:
    L = [f"**{_headline(st)}**", "", "| | Step | Progress | |", "|---|---|---|---|"]
    for i in st["items"]:
        here = "**next**" if i["id"] == st["next"]["id"] else ("done" if i["state"] == "done" else "")
        L.append(f"| {i['n']} | {i['title']} | `{_bar(i['progress'])}` {i['progress']}% | {here} |")
    n = st["next"]
    L += ["", f"**Next:** {n['title']}", "", f"**Why:** {n['why']}", "", f"**What you do:** {n['do']}"]
    if any(n.get("missing") or []):
        L += ["", "**Still needed:** " + "; ".join(m for m in n["missing"] if m)]
    L += ["", f"More: [{Path(n['guide']).stem.replace('-', ' ')}]({n['guide']})"]
    return "\n".join(L) + "\n"


def _inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)

    def link(m):
        text, url = m.group(1), m.group(2)
        if url.endswith(".md") and "/" not in url:
            page = url[:-3]
            return f'<a href="#g-{"index" if page == "README" else page}" data-open="{page}">{text}</a>'
        return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)


def md_to_html(text: str) -> tuple[str, str]:
    """(title, body html) of one short guide page: headings, paragraphs, bulleted and numbered lists,
    bold, italic, code and links.  The guide pages use nothing else."""
    title, out, lst, para = "", [], None, []

    def flush():
        nonlocal lst, para
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para = []
        if lst:
            out.append(f"</{lst}>")
            lst = None
    for line in text.splitlines():
        if m := re.match(r"^#\s+(.*)", line):
            flush()
            title = m.group(1).strip()
        elif m := re.match(r"^#{2,}\s+(.*)", line):
            flush()
            out.append("<h4>" + _inline(m.group(1)) + "</h4>")
        elif m := re.match(r"^\s*(?:(\d+)[.)]|[-*])\s+(.*)", line):
            kind = "ol" if m.group(1) else "ul"
            if para:
                out.append("<p>" + _inline(" ".join(para)) + "</p>")
                para = []
            if lst != kind:
                if lst:
                    out.append(f"</{lst}>")
                out.append(f"<{kind}>")
                lst = kind
            out.append("<li>" + _inline(m.group(2)) + "</li>")
        elif not line.strip():
            flush()
        else:
            if lst:
                out.append(f"</{lst}>")
                lst = None
            para.append(line.strip())
    flush()
    return title, "\n".join(out)


_CSS = """
:root{--ink:#1f2328;--mut:#667085;--line:#e4e7ec;--bg:#f7f8fa;--card:#fff;--acc:#2f6f4f;--bar:#dfe5ea}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:760px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:30px 0 10px}h4{margin:14px 0 4px}
.mut{color:var(--mut)}.small{font-size:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:14px 0}
.next{border-color:var(--acc);border-width:2px}
.next h3{margin:0 0 6px;font-size:19px}.label{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--acc);font-weight:600}
.row{display:grid;grid-template-columns:26px 1fr 150px 54px;gap:10px;align-items:center;padding:9px 0;border-top:1px solid var(--line)}
.row:first-child{border-top:0}.row.cur{font-weight:600}
.num{color:var(--mut);text-align:right}.pct{color:var(--mut);font-size:14px;text-align:right}
.bar{height:10px;background:var(--bar);border-radius:6px;overflow:hidden}.bar>i{display:block;height:100%;background:var(--acc)}
.big{height:14px;margin:10px 0 2px}
.detail{grid-column:2/5;color:var(--mut);font-size:14px;font-weight:400;margin-top:-4px}
details{border-top:1px solid var(--line);padding:10px 0}details:first-of-type{border-top:0}
summary{cursor:pointer;font-weight:600}details p,details li{font-size:15px}
a{color:var(--acc)}code{background:#eef1f4;border-radius:4px;padding:1px 4px;font-size:14px}
@media(max-width:560px){.row{grid-template-columns:22px 1fr 70px 44px}}
"""

_JS = """
// reload to pick up progress, but never while a guide page is open for reading
setInterval(function(){ if(!document.querySelector('details[open]')) location.reload(); }, 5000);
document.addEventListener('click', function(e){
  var a = e.target.closest('a[data-open]'); if(!a) return;
  var d = document.getElementById('g-' + (a.dataset.open === 'README' ? 'index' : a.dataset.open));
  if(d){ e.preventDefault(); document.querySelectorAll('details[open]').forEach(function(x){ if(x!==d) x.open=false; });
         d.open = true; d.scrollIntoView({behavior:'smooth', block:'start'}); }
});
"""


def render_html(st: dict) -> str:
    e = html.escape
    n = st["next"]
    rows = []
    for i in st["items"]:
        cur = " cur" if i["id"] == n["id"] else ""
        rows.append(f'<div class="row{cur}"><div class="num">{i["n"]}</div><div>{e(i["title"])}</div>'
                    f'<div class="bar"><i style="width:{i["progress"]}%"></i></div>'
                    f'<div class="pct">{"done" if i["state"] == "done" else str(i["progress"]) + "%"}</div>'
                    f'<div class="detail">{e(i["detail"])}</div></div>')
    guide = []
    for page in GUIDE_PAGES:
        f = GUIDE_DIR / f"{page}.md"
        if f.exists():
            title, body = md_to_html(read_text(f))
            guide.append(f'<details id="g-{page}"><summary>{e(title)}</summary>{body}</details>')
    missing = "; ".join(m for m in n.get("missing", []) if m)
    who = e(st["name"] or "Getting started")
    page = n["guide"].rsplit("/", 1)[-1][:-3]
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Claim Registry checklist</title>
<style>{_CSS}</style></head><body><main>
<h1>{who}</h1>
<div class="mut">{st["steps_done"]} of {st["steps"]} steps done before your first quest</div>
<div class="bar big"><i style="width:{st["percent"]}%"></i></div>
<div class="card next"><div class="label">Next step</div><h3>{e(n["title"])}</h3>
<p><b>Why:</b> {e(n["why"])}</p><p><b>What you do:</b> {e(n["do"])}</p>
{f'<p class="mut small">Still needed: {e(missing)}</p>' if missing else ''}
<p class="small"><a href="#g-{page}" data-open="{page}">Read more about this step</a></p></div>
<div class="card">{''.join(rows)}</div>
<h2 id="g-index">The short guide</h2>
<div class="mut small">Each page takes about a minute. This checklist stops refreshing while a page is open.</div>
<div class="card">{''.join(guide)}</div>
<div class="mut small">Progress is read from your project's files. Ask your assistant "what is next?" at any time.
Updated {e(time.strftime("%H:%M"))}.</div>
</main><script>{_JS}</script></body></html>
"""


# --------------------------------------------------------------------------- #
# command
# --------------------------------------------------------------------------- #

def write_page(proj: Path, st: dict | None = None) -> Path:
    p = Path(proj) / PAGE_FILE
    atomic_write_text(p, render_html(st or build(proj)))
    return p


START_TEXT = """CLAIM REGISTRY - instructions for the AI assistant (there is no program to launch; you are the interface)

You are now the person's research coach and mentor for Claim Registry. They are at home on the internet,
new to research, and do not program. Your chat is the only interface: you run every command and edit every file.

"Launch", "start", "open" or "use" Claim Registry always means this, even if you have worked on this
code before or know of a recent change to it. Do not verify, test, fix or report on the harness.

DO NOW
  1. Do not run the tests or the demo. Do not read the rest of the repository first.
  2. Say only this, plus at most two short sentences: "What do you want to research?"
  3. When they answer, read AGENTS.md before you reply. Your second reply decides whether they stay:
     show you understood what makes their question hard, name what they already brought, say what
     Claim Registry would give them for it and what it honestly costs, then ask one easy question.
     Never open with what it cannot do.
  4. Then run:  python cr.py next            (later: python cr.py next "<project folder>" --json)
     It gives the next step, why it matters, what they do and what you do. Never track progress yourself.

EVERY REPLY
  About 150 words. One next step and one line on why. One question at a time. Plain words.
  Encourage with specifics: what they just finished and what it unlocks. Be honest about the effort.
  Offer more (a page in docs/guide/) instead of pouring it out.

PAPERS
  You search for them and download the ones that are free to read, by lawful routes only. When you
  cannot download one, say exactly why and what to do instead (AGENTS.md).

Only if they ask in so many words for the harness itself to be changed, read HANDOFF.md instead.

YOUR ENTIRE FIRST REPLY IS THE QUESTION IN STEP 2. No summary of what you checked or read.
The complete standing research personality follows. Load every file, including restored memories.
If the tool truncates it, read ALL numbered parts listed below before substantive research help.
"""


def cmd_start(a) -> int:
    from . import personality
    # Assemble before printing: a missing memory must not produce a seemingly complete startup.
    try:
        context = personality.preamble() + personality.render()
    except (ValueError, OSError) as e:
        print(f"Research personality could not be loaded: {e}", file=sys.stderr)
        return 2
    print(START_TEXT, end="")
    print(context, end="")
    return 0


def cmd_next(a) -> int:
    import json
    proj = Path(a.project) if a.project else None
    is_project = bool(proj and (proj / "project.json").exists())
    if proj and not is_project and (a.done or a.undo or a.window or a.watch):
        print(f"{proj} is not a project yet. Create it first: python cr.py new \"{proj}\" --name \"<topic>\"",
              file=sys.stderr)
        return 2
    for sid, on in [(s, True) for s in (a.done or [])] + [(s, False) for s in (a.undo or [])]:
        if sid not in CONFIRMABLE:
            print(f"only these can be confirmed by hand: {', '.join(CONFIRMABLE)}. Every other step is read from "
                  f"the project's files.", file=sys.stderr)
            return 2
        saved = read_json(proj / STATE_FILE, default={}) or {}
        conf = dict(saved.get("confirmed") or {})
        if on:
            conf[sid] = _today()
        else:
            conf.pop(sid, None)
        write_json(proj / STATE_FILE, {**saved, "confirmed": conf,
                                       "note": "what the person confirmed by hand; every other step is read from the files"})
    st = build(proj if is_project else None)
    if proj and not is_project:
        st["name"] = None
    if is_project and (a.window or a.watch or (proj / PAGE_FILE).exists()):
        page = write_page(proj, st)          # an open checklist window stays current
        if a.window:
            import webbrowser
            webbrowser.open(page.resolve().as_uri())
    if a.json:
        print(json.dumps(st, indent=2, ensure_ascii=False))
    elif a.md:
        print(render_markdown(st), end="")
    else:
        print(render_text(st), end="")
    if a.window:
        print(f"\nChecklist window: {(proj / PAGE_FILE).resolve()}  (it refreshes each time `cr next` is run)")
    if a.watch:
        print("Keeping the checklist window current. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(max(2.0, float(a.every)))
                write_page(proj)
        except KeyboardInterrupt:
            pass
    return 0
