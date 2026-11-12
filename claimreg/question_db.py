"""The question database: every question a run asked, in one file at the top of the run.

The questions, not the answers, show how far a quest distilled the corpus.  ``QUESTIONS.md`` lists
every question with the sources it named and how many FRDs it yielded, lists the indexed sources
no question has named, and carries a ready prompt.  A person hands that one file and the source
index (``01_FRAME/index.md``) to another model and asks whether the questioning was thorough
enough.  The reviewer does not need the answers.

Everything here is read from the run's own records; nothing is judged and no model is called.
``QUESTIONS.json`` holds the same rows as data.
"""

from __future__ import annotations

import re
from pathlib import Path

from .util import atomic_write_text, read_json, read_text, utcnow, write_json

QUESTIONS_MD = "QUESTIONS.md"
QUESTIONS_JSON = "QUESTIONS.json"

_QUESTIONS = "02_DISCOVERY/01_issued-questions/questions.json"
_CANDIDATES = "03_FRDS/01_candidates/candidates.json"
_VALIDATIONS = "03_FRDS/04_validation-results/validations.json"
_RETAINED = "03_FRDS/05_validated/retained-frds.json"
_AXIS_DIR = re.compile(r"^AXIS-([^_]+)__")

AUDIT_PROMPT = """\
You are checking whether a research quest asked enough questions of its corpus.

You have two files: this question database (QUESTIONS.md) and the source index
(01_FRAME/index.md). You do not need the answers. Work from the questions, the
sources they named, the "FRDs kept" counts and the index.

For each axis:
1. Which indexed sources that matter to the axis question has no question named?
   Give the exact filenames, most important first.
2. Which issues that the axis question turns on has no question asked about?
3. Which questions were asked but yielded little (see "FRDs kept" and "Flags")
   and should be asked again or split?
4. Is the questioning thorough enough to stop? Answer yes or no, with the reason.
5. If no, write the next questions. Each names one to three exact source
   filenames from the index and asks for facts, not for a verdict."""


def _list(path: Path) -> list | None:
    """The rows of a JSON list file, or None when the file has not been made yet."""
    if not path.exists():
        return None
    d = read_json(path, default=None)
    return d if isinstance(d, list) else []


def _count_by_qid(rows: list | None, keep=lambda r: True) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in rows or []:
        if isinstance(r, dict) and r.get("qid") and keep(r):
            out[r["qid"]] = out.get(r["qid"], 0) + 1
    return out


def _question_sources(q: dict) -> tuple[list[str], list[str]]:
    """(source files the question named, names it sent that matched no corpus file)."""
    resolved = q.get("sources_resolved")
    named, unresolved = [], []
    if isinstance(resolved, dict) and resolved:
        for sent, real in resolved.items():
            (named if real else unresolved).append(real or sent)
    else:
        named = [s for s in (q.get("sources_as_sent") or []) if s]
    return named, unresolved


def _first_question(text) -> str:
    """The axis question itself: a parsed header can run the question on into its commentary."""
    text = " ".join(str(text or "").split())
    cut = text.find("?")
    return text[:cut + 1] if 0 <= cut < len(text) - 1 and len(text) > 300 else text


def _axis_scopes(run_dir: Path) -> list[tuple[str, Path]]:
    """[(axis id, folder)] for a run with one database per axis, else [("", run folder)]."""
    axes = [(m.group(1), p) for p in sorted(run_dir.iterdir()) if p.is_dir()
            for m in [_AXIS_DIR.match(p.name)] if m]
    return axes or [("", run_dir)]


def _index_sources(run_dir: Path) -> dict[str, dict]:
    """{filename: {"rank", "title"}} from the run's frozen index; {} when there is none."""
    path = run_dir / "01_FRAME" / "index.md"
    if not path.exists():
        return {}
    from .index import parse_index
    try:
        parsed = parse_index(read_text(path))
    except Exception:
        return {}
    out = {}
    for fn, body in parsed.get("entries", {}).items():
        m = re.search(r"\*\*Title:\*\*\s*(.+)", body)
        out[fn] = {"rank": parsed.get("ranks", {}).get(fn, ""), "title": (m.group(1).strip() if m else "")}
    return out


def build(run_dir: Path, run_id: str | None = None) -> dict:
    """Collect the question database of one run from its records."""
    run_dir = Path(run_dir)
    frame = read_json(run_dir / "01_FRAME" / "frame.json", default={}) or {}
    frame_axes = {a.get("axis_id"): a for a in frame.get("axes", []) if isinstance(a, dict)}
    axes, named_by = [], {}
    for axis_id, root in _axis_scopes(run_dir):
        questions = _list(root / _QUESTIONS) or []
        candidates, validations, retained = (_list(root / rel) for rel in (_CANDIDATES, _VALIDATIONS, _RETAINED))
        n_cand = _count_by_qid(candidates)
        n_kept = _count_by_qid(retained)
        n_quote = _count_by_qid(validations, lambda r: str(r.get("readiness_reason", "")).startswith("mechanical check"))
        n_nosrc = _count_by_qid(validations, lambda r: "needs-source" in str(r.get("readiness_reason", "")))
        rows = []
        for q in sorted((x for x in questions if isinstance(x, dict)), key=lambda x: str(x.get("qid", ""))):
            qid = str(q.get("qid", ""))
            named, unresolved = _question_sources(q)
            for s in named:
                named_by.setdefault(s, []).append(qid)
            answered = bool(q.get("response_ids")) or str(q.get("status", "")).upper() == "ANSWERED"
            row = {"qid": qid, "axis": axis_id or q.get("axis") or "", "text": " ".join(str(q.get("text", "")).split()),
                   "sources": named, "sources_not_resolved": unresolved, "answered": answered,
                   "attempts": len(q.get("attempts") or []), "issued": q.get("issued") or "",
                   "filed_by": q.get("axis_source") or "",
                   "frd_candidates": None if candidates is None else n_cand.get(qid, 0),
                   "frds_kept": None if retained is None else n_kept.get(qid, 0),
                   "dropped_by_quote_check": n_quote.get(qid, 0), "dropped_no_source": n_nosrc.get(qid, 0)}
            flags = []
            if not answered:
                flags.append("no answer")
            if unresolved:
                flags.append("source not found: " + ", ".join(unresolved))
            if answered and row["frds_kept"] == 0:
                flags.append("no FRDs kept")
            if row["dropped_by_quote_check"]:
                flags.append(f"quote check dropped {row['dropped_by_quote_check']}")
            if row["dropped_no_source"]:
                flags.append(f"{row['dropped_no_source']} dropped: source not found")
            row["flags"] = flags
            rows.append(row)
        fa = frame_axes.get(axis_id, {}) if axis_id else {}
        axes.append({"axis_id": axis_id, "name": fa.get("name", ""), "question": _first_question(fa.get("question", "")),
                     "frds_built": retained is not None, "questions": rows})
    index = _index_sources(run_dir)
    lower = {s.casefold() for s in named_by}
    never = [{"file": fn, **meta} for fn, meta in index.items() if fn.casefold() not in lower]
    never.sort(key=lambda r: (r["rank"] or "~", r["file"].casefold()))
    by_rank: dict[str, list[int]] = {}
    for fn, meta in index.items():
        cell = by_rank.setdefault(meta["rank"] or "unranked", [0, 0])
        cell[1] += 1
        cell[0] += fn.casefold() in lower
    all_rows = [r for a in axes for r in a["questions"]]
    return {"run_id": run_id or run_dir.name, "generated": utcnow(), "axes": axes,
            "totals": {"questions": len(all_rows), "answered": sum(r["answered"] for r in all_rows),
                       "frds_kept": sum(r["frds_kept"] or 0 for r in all_rows),
                       "flagged": sum(bool(r["flags"]) for r in all_rows)},
            "sources": {"indexed": len(index), "named": {s: sorted(set(q)) for s, q in sorted(named_by.items())},
                        "named_by_rank": {k: {"named": v[0], "indexed": v[1]} for k, v in sorted(by_rank.items())},
                        "never_named": never}}


def _cell(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def render(db: dict) -> str:
    t, src = db["totals"], db["sources"]
    n_named = len(src["named"])
    out = [f"# Question database: {db['run_id']}", "",
           f"*Written {db['generated']} from the run's own records. No model wrote or judged anything here.*", "",
           "The questions, not the answers, show how far this run distilled the corpus. "
           "To check whether the questioning was thorough enough, give another model this file and the source "
           "index (`01_FRAME/index.md`) with the prompt below. It does not need the answers.", "",
           f"- **Questions:** {t['questions']} asked, {t['answered']} answered, {t['flagged']} flagged."]
    if any(a["frds_built"] for a in db["axes"]):
        out.append(f"- **FRDs kept:** {t['frds_kept']}.")
    if src["indexed"]:
        ranks = "; ".join(f"Rank {k} {v['named']} of {v['indexed']}" if len(k) == 1 else f"{k} {v['named']} of {v['indexed']}"
                          for k, v in src["named_by_rank"].items())
        out.append(f"- **Sources:** questions named {n_named} source file(s). The index lists {src['indexed']}"
                   f"{' (' + ranks + ')' if ranks else ''}.")
    else:
        out.append(f"- **Sources:** questions named {n_named} source file(s). This run has no source index to compare with.")
    out += ["", "## The prompt for the reviewing model", "", "```text", AUDIT_PROMPT, "```", "", "## Questions asked", ""]
    for a in db["axes"]:
        if a["axis_id"]:
            out += [f"### Axis {a['axis_id']}" + (f": {a['name']}" if a["name"] else ""), ""]
            if a["question"]:
                out += [f"Axis question: {a['question']}", ""]
        if not a["questions"]:
            out += ["No questions were asked" + (" for this axis." if a["axis_id"] else " yet."), ""]
            continue
        out += ["| QID | Sources named | Question | FRDs kept | Flags |", "|---|---|---|---|---|"]
        for r in a["questions"]:
            kept = "not built yet" if r["frds_kept"] is None else str(r["frds_kept"])
            sources = "<br>".join(f"`{_cell(s)}`" for s in r["sources"]) or "none"
            out.append(f"| {r['qid']} | {sources} | {_cell(r['text'])} | {kept} | {_cell('; '.join(r['flags']))} |")
        out.append("")
    out += ["## Sources the questions named", ""]
    if src["named"]:
        out += ["| Source file | Questions |", "|---|---|"]
        out += [f"| `{_cell(s)}` | {', '.join(q)} |" for s, q in src["named"].items()]
    else:
        out.append("None yet.")
    out += ["", "## Indexed sources no question has named", ""]
    if not src["indexed"]:
        out.append("This run has no source index, so this list cannot be made.")
    elif not src["never_named"]:
        out.append("None: every indexed source was named by at least one question.")
    else:
        out += [f"{len(src['never_named'])} of {src['indexed']} indexed sources. Not every source matters to every "
                "question; this list is for the reviewer to judge.", "", "| Rank | Source file | Title |", "|---|---|---|"]
        out += [f"| {r['rank'] or ''} | `{_cell(r['file'])}` | {_cell(r['title'][:140])} |" for r in src["never_named"]]
    return "\n".join(out) + "\n"


def write_question_database(run_dir: Path, run_id: str | None = None) -> dict | None:
    """Write QUESTIONS.md and QUESTIONS.json at the top of the run.  Returns the database, or None
    when the run has asked no questions yet (nothing is written)."""
    run_dir = Path(run_dir)
    db = build(run_dir, run_id)
    if not db["totals"]["questions"]:
        return None
    atomic_write_text(run_dir / QUESTIONS_MD, render(db))
    write_json(run_dir / QUESTIONS_JSON, db)
    return db
