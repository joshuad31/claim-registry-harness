"""One study, one voice: which findings are the same study told again.

A corpus holds trials, reviews that restate those trials, guidelines that cite the reviews, and
sometimes a second copy of a paper.  Witnesses are never merged (spec 28.2) and coverage is decided
from text alone (spec 28, 29), so none of that changes here.  What this module adds is the unit of
independence: each validated finding is attributed to the study it rests on, so that eight witnesses
are not read, counted or scored as eight studies when they are two.

Two layers
----------
* ``01_FRAME/STUDY-MAP.json`` (one per project, written by ``cr studies`` and editable by hand):
  every source file with the study it belongs to and the kind of source it is.  A second copy of a
  paper belongs to the first copy's study (``corpus.duplicates``).  The kind of source is a first
  guess from the file's title ("... : a review") and is there to be corrected.
* Per finding, computed from the run's own records: a finding from a primary source is that study.
  A finding from a secondary source (a review, a guideline, or a finding the validator labelled
  DERIVED_FROM / DERIVATIVE_UNKNOWN) that names exactly one other study of this corpus, by author
  and year, is that study restated.  One that names several is a summary; one that names none is a
  secondary report whose original is not identified.  Neither is counted as a study of its own.

Everything is topic-neutral: file names, title words, provenance labels and author-year citations.
Nothing here knows what a run is about, and nothing here can add or remove support for a hypothesis;
it only says which support is the same support twice.

Overrides (in the same file, kept when the map is rebuilt)::

    "overrides": {"files":    {"geer2015.pdf.md": {"kind": "review"},
                               "trial-preprint.md": {"study": "STUDY-smith2020"}},
                  "findings": {"FRD-Q0037-01-c3": "STUDY-bolk2010"}}
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from .util import atomic_write_text, read_json, utcnow, write_json

MAP_JSON = "STUDY-MAP.json"
MAP_MD = "STUDY-MAP.md"

PRIMARY = "primary"
# kinds of source that report other people's results; a finding from one is not a study of its own
SECONDARY_KINDS = ("review", "meta-analysis", "guideline", "commentary", "synthesis")
_KIND_WORDS = [
    ("meta-analysis", r"meta-?analys[ie]s|pooled analysis|network meta"),
    ("review", r"\breview\b|\boverview\b|state of the art|narrative synthesis"),
    ("guideline", r"guidelines?\b|consensus statement|position statement|recommendations? of the|practice bulletin"),
    ("commentary", r"\beditorial\b|\bcommentary\b|letter to the editor|\bperspective\b|\bviewpoint\b"),
]
_STEM = re.compile(r"^([A-Za-z][A-Za-z\-']+?)[\s_\-]*((?:19|20)\d{2})[a-z]?(?![0-9])")
_PROV = re.compile(r"^\s*(OWN_RESULT|DERIVED_FROM|DERIVATIVE_UNKNOWN)\s*(?:\(\s*(.*?)\s*\))?", re.I | re.S)


def study_id_for(filename: str) -> str:
    stem = Path(filename).name
    stem = re.sub(r"(\.pdf)?\.(md|markdown|txt)$", "", stem, flags=re.I)
    return "STUDY-" + (re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-") or "source")


def guess_kind(text: str) -> str:
    """A first guess at the kind of source, from its title lines only.  A human corrects it in the map."""
    head = []
    for line in (text or "").splitlines()[:60]:
        s = re.sub(r"!\[[^\]]*\]\([^)]*\)|<[^>]+>", " ", line).strip()
        if not s:
            continue
        if s.startswith("#") or len(head) < 3:
            head.append(s.lstrip("# ").strip())
        if len(head) >= 4:
            break
    title = " ".join(head)[:400].lower()
    for kind, rx in _KIND_WORDS:
        if re.search(rx, title):
            return kind
    return PRIMARY


def _author_year(filename: str):
    m = _STEM.match(Path(filename).name)
    return (m.group(1).lower(), m.group(2)) if m else None


# --------------------------------------------------------------------------- #
# the project's study map
# --------------------------------------------------------------------------- #

def map_path(project_dir) -> Path:
    return Path(project_dir) / "01_FRAME" / MAP_JSON


def build_map(project_dir, corpus, cfg: dict, existing: dict | None = None) -> dict:
    """Every source file with its study and kind.  Overrides in ``existing`` are kept and applied."""
    ccfg = cfg.get("corpus", {}) or {}
    dups = dict(ccfg.get("duplicates") or {})
    synth = list(ccfg.get("synthesis_sources") or [])
    over = (existing or {}).get("overrides") or {}
    f_over = over.get("files") or {}
    files: dict = {}
    for fn in sorted(corpus.filenames):
        target = corpus.resolve(dups[fn]) if fn in dups else None
        kind, basis = PRIMARY, "title"
        if any(fnmatch.fnmatch(fn, pat) or fn == pat for pat in synth):
            kind, basis = "synthesis", "corpus.synthesis_sources"
        else:
            try:
                kind = guess_kind(corpus.text(fn))
            except Exception:  # noqa: BLE001 - an unreadable file is still a source
                kind = PRIMARY
        rec = {"study": study_id_for(target or fn), "kind": kind, "basis": basis}
        if target and target != fn:
            rec.update(duplicate_of=target, basis="corpus.duplicates")
        o = f_over.get(fn)
        if isinstance(o, str):
            o = {"study": o}
        if isinstance(o, dict):
            rec.update({k: v for k, v in o.items() if k in ("study", "kind", "cited_as")}, basis="override")
        files[fn] = rec
    studies: dict = {}
    for fn, rec in files.items():
        s = studies.setdefault(rec["study"], {"files": [], "kind": rec["kind"]})
        s["files"].append(fn)
        if rec["kind"] == PRIMARY:
            s["kind"] = PRIMARY
    return {"about": "Which source files are which study. Edit 'overrides' to correct it; 'files' and 'studies' "
                     "are rebuilt by `cr studies`. See claimreg/studies.py.",
            "updated": utcnow(), "files": files, "studies": studies,
            "overrides": {"files": f_over, "findings": over.get("findings") or {}}}


def load_map(ctx, write: bool = True) -> dict:
    """The project's study map, built on first use.  Files added to the corpus since are filled in."""
    cache = getattr(ctx, "_study_map", None)
    if cache is not None:
        return cache
    path = map_path(ctx.project_dir)
    existing = read_json(path, default=None)
    corpus = ctx.corpus
    if not existing or set(corpus.filenames) - set(existing.get("files", {})):
        smap = build_map(ctx.project_dir, corpus, ctx.cfg, existing)
        if write:
            try:
                write_json(path, smap)
                atomic_write_text(path.with_name(MAP_MD), render_map(smap))
            except OSError:
                pass
    else:
        smap = existing
    try:
        ctx._study_map = smap
    except Exception:  # noqa: BLE001
        pass
    return smap


def render_map(smap: dict, attributions: list[dict] | None = None) -> str:
    out = ["# Study map", "",
           "Which source files are which study. Witnesses are never merged; this only says which findings are the "
           "same study told again, so that a count of witnesses is not read as a count of studies.", "",
           "The kind of each source is a first guess from its title. Correct it under `overrides` in "
           f"`{MAP_JSON}` and run `cr studies` again.", "",
           "| Study | Kind | Source file(s) | How this was decided |", "|---|---|---|---|"]
    for sid, s in sorted(smap.get("studies", {}).items()):
        basis = sorted({smap["files"][f].get("basis", "") for f in s["files"]})
        out.append(f"| `{sid}` | {s['kind']} | {'<br>'.join('`' + f + '`' for f in s['files'])} | {', '.join(basis)} |")
    if attributions is not None:
        moved = [a for a in attributions if a["role"] != "direct"]
        out += ["", "## Findings that are not a study of their own", "",
                f"{len(moved)} of {len(attributions)} retained findings come from a secondary source or restate "
                "another study.", "", "| Finding | From | Counts as | Why |", "|---|---|---|---|"]
        for a in sorted(moved, key=lambda a: (a["study"], a["vfrd_id"])):
            what = {"restated": f"`{a['study']}` restated", "summary": "a summary of " + ", ".join(
                        f"`{s}`" for s in a.get("summarises", [])),
                    "secondary": "a secondary report; original not identified"}[a["role"]]
            out.append(f"| `{a['vfrd_id']}` | `{a['via']}` | {what} | {a['basis']} |")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- #
# attribution of one finding
# --------------------------------------------------------------------------- #

def _citation_index(smap: dict) -> list[tuple]:
    """(regex, study id, source file) for every corpus source that can be cited by author and year."""
    out = []
    for fn, rec in smap.get("files", {}).items():
        keys = [_author_year(fn)] if _author_year(fn) else []
        for c in rec.get("cited_as") or []:
            m = re.match(r"\s*([A-Za-z][A-Za-z\-' ]+?)\s*,?\s*((?:19|20)\d{2})", str(c))
            if m:
                keys.append((m.group(1).strip().lower(), m.group(2)))
        for author, year in keys:
            rx = re.compile(rf"(?<![A-Za-z]){re.escape(author)}(?![A-Za-z])"
                            rf"(?:\s+et\s+al\.?|\s+(?:and|&)\s+[A-Z][\w\-']+)?[^A-Za-z]{{0,14}}{year}(?!\d)", re.I)
            out.append((rx, rec["study"], fn))
    return out


def _named(text: str, index: list[tuple], own: str) -> list[str]:
    clean = re.sub(r"<[^>]+>|[*_`]", "", text or "")
    return sorted({sid for rx, sid, _ in index if sid != own and rx.search(clean)})


def attribute(v: dict, smap: dict, corpus=None, index: list[tuple] | None = None) -> dict:
    """The study one validated finding rests on.  ``v`` needs vfrd_id, source_file, provenance, claim, source_text."""
    src = v.get("source_file") or "?"
    frec = smap.get("files", {}).get(src, {"study": study_id_for(src), "kind": PRIMARY})
    own = frec["study"]
    base = {"vfrd_id": v.get("vfrd_id"), "via": src, "kind": frec.get("kind", PRIMARY)}
    forced = (smap.get("overrides", {}).get("findings") or {}).get(v.get("vfrd_id"))
    if forced:
        return {**base, "study": forced, "role": "direct" if forced == own else "restated",
                "basis": "override in the study map"}
    m = _PROV.match(str(v.get("provenance") or ""))
    label = m.group(1).upper() if m else ""
    secondary_source = frec.get("kind", PRIMARY) in SECONDARY_KINDS
    if label != "DERIVED_FROM" and label != "DERIVATIVE_UNKNOWN" and not secondary_source:
        return {**base, "study": own, "role": "direct", "basis": "the source's own result"}
    why = (f"the source is a {frec['kind']}" if secondary_source else f"validation labelled it {label}")
    index = _citation_index(smap) if index is None else index
    named = set()
    if label == "DERIVED_FROM" and m.group(2) and corpus is not None:
        anc = corpus.resolve(m.group(2))
        if anc and smap.get("files", {}).get(anc, {}).get("study", own) != own:
            named.add(smap["files"][anc]["study"])
    named |= set(_named(v.get("claim", ""), index, own))
    where = "the finding"
    if not named:
        named |= set(_named(v.get("source_text", ""), index, own))
        where = "the quoted passage"
    if len(named) == 1:
        sid = next(iter(named))
        return {**base, "study": sid, "role": "restated", "basis": f"{why}; {where} names one study of this corpus"}
    if len(named) > 1:
        return {**base, "study": own, "role": "summary", "summarises": sorted(named),
                "basis": f"{why}; {where} names {len(named)} studies of this corpus"}
    return {**base, "study": own, "role": "secondary", "basis": f"{why}; no study of this corpus is named"}


def frd_studies(ctx, frds: list[dict] | None = None) -> dict:
    """{vfrd_id: attribution} for a run's retained findings (or the list given)."""
    if frds is None:
        frds = ctx.load("frds", "05_validated/retained-frds.json", default=None)
        if frds is None:
            frds = ctx.load("frds", "05_validated/validated-frds.json", default=[]) or []
    smap = load_map(ctx)
    index = _citation_index(smap)
    return {v["vfrd_id"]: attribute(v, smap, ctx.corpus, index) for v in frds if v.get("vfrd_id")}


def witness_studies(ctx) -> dict:
    """{witness_id: attribution} for a run's released witnesses."""
    by_frd = frd_studies(ctx)
    ws = ctx.load("witnesses", "05_released/witnesses.json", default=[]) or []
    smap = load_map(ctx)
    out = {}
    for w in ws:
        a = by_frd.get(w.get("vfrd_id"))
        if a is None:
            a = attribute({"vfrd_id": w.get("vfrd_id"), "source_file": w.get("source_file")}, smap, ctx.corpus)
        out[w["witness_id"]] = a
    return out


# --------------------------------------------------------------------------- #
# counting
# --------------------------------------------------------------------------- #

def count(attrs) -> dict:
    """How many studies a group of findings is.  A direct or restated finding counts as its study;
    a summary or an unidentified secondary report is listed but is not a study of its own."""
    attrs = [a for a in attrs if a]
    studies = sorted({a["study"] for a in attrs if a["role"] in ("direct", "restated")})
    other = sorted({a["via"] for a in attrs if a["role"] in ("summary", "secondary")})
    return {"items": len(attrs), "studies": studies, "n_studies": len(studies),
            "secondary_reports": other, "n_secondary_reports": len(other),
            "independence_ratio": round(len(studies) / len(attrs), 3) if attrs else None}


def phrase(c: dict, noun: str = "witness") -> str:
    """'8 witnesses from 2 studies (and 1 secondary report)'"""
    n, s, o = c["items"], c["n_studies"], c["n_secondary_reports"]
    plural = noun + ("es" if noun.endswith("s") else "s")
    return (f"{n} {noun if n == 1 else plural} from {s} stud{'y' if s == 1 else 'ies'}"
            + (f" and {o} secondary report{'s' if o != 1 else ''}" if o else ""))


def studies_block(attrs: dict, id_label: str = "witness") -> str:
    """The STUDIES block an assessor is given: which rows are the same study."""
    groups: dict = {}
    for wid, a in sorted(attrs.items()):
        key = a["study"] if a["role"] in ("direct", "restated") else f"{a['study']} [{a['role']} report]"
        groups.setdefault(key, []).append((wid, a))
    lines = []
    for key, items in sorted(groups.items()):
        via = sorted({a["via"] for _, a in items if a["role"] == "restated"})
        lines.append(f"{key}: {', '.join(w for w, _ in items)}"
                     + (f"  (some restated in {', '.join(via)})" if via else ""))
    return "\n".join(lines) or f"(no {id_label} rows)"


STUDY_NOTE = ("STUDY IDENTITY: the rows of the registry are not independent of one another. The STUDIES list below "
              "says which rows rest on the same study; a study told in several rows, or restated by a review, is ONE "
              "study and is weighed once. A summary or secondary report adds no study of its own to the studies it "
              "reports. This says nothing about how strong any study is; that judgment is yours. Where you name a "
              "driver, name its study.")


def driver_audit(drivers, attrs: dict) -> dict:
    """After an assessment: do its drivers lean on one study more than once?

    ``drivers``: the assessment's drivers for one axis (strings or dicts that mention row ids)."""
    ids = sorted(attrs, key=len, reverse=True)
    seen: dict = {}
    for d in drivers or []:
        text = d if isinstance(d, str) else " ".join(str(x) for x in d.values())
        favors = (d.get("favors") if isinstance(d, dict) else "") or ""
        for wid in ids:
            if wid in text:
                a = attrs[wid]
                seen.setdefault((a["study"], favors), []).append(wid)
                text = text.replace(wid, " ")
    repeated = [{"study": s, "favors": f, "rows": sorted(set(w))} for (s, f), w in sorted(seen.items())
                if len(set(w)) > 1]
    cited = sorted({w for ws in seen.values() for w in ws})
    return {"drivers": len(drivers or []), "rows_cited": len(cited),
            "effective_studies": len({s for s, _ in seen}),
            "one_study_cited_as_several_drivers": repeated}
