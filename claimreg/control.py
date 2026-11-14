"""A control run with no preferred answer, and the structural comparison that reads it.

Everything measured about the method so far comes from questions the researcher cared about the
answer to.  A control asks a question nobody is rooting for, with the coach switched off, so that
what is seen is the pipeline and not the preference.  Two commands:

* ``cr control <project> <new project folder>`` sets the control up beside an existing project:
  the same corpus (by reference, not copied), the same index, Archivist prompt and study map, the
  coach off, no preferred hypothesis, a blank question file, no notebook links (the parent's
  notebooks hold the parent's conversation), and a dated note of what was decided before any evidence
  was seen.  The header is NOT copied: a control needs its own question, written by the researcher.
* ``cr structure <project> --run RUN [--against <project> --against-run RUN]`` reports the shape of
  a run - how much survives each stage, how many studies stand behind the witnesses, how often the
  two matching passes agree, how the gauge is divided - and sets two runs side by side.  Scores of
  different questions are not comparable; shapes are.
"""

from __future__ import annotations

import shutil
from collections import Counter
from pathlib import Path

from .util import atomic_write_text, ensure_dir, read_json, utcnow, write_json

NOTE = "CONTROL-NOTE.md"


# --------------------------------------------------------------------------- #
# setting a control up
# --------------------------------------------------------------------------- #

def make_control(src: Path, dst: Path, name: str | None = None) -> dict:
    src, dst = Path(src).resolve(), Path(dst).resolve()
    if not (src / "project.json").exists():
        raise FileNotFoundError(f"{src} is not a project folder (no project.json)")
    if dst.exists() and any(dst.iterdir()):
        raise FileExistsError(f"{dst} already exists and is not empty")
    for sub in ("01_CORPUS/manifests", "01_FRAME", "02_RUNS", "04_RELEASES", "90_METHOD/prompts"):
        ensure_dir(dst / sub)
    cfg = read_json(src / "project.json", default={}) or {}
    parent_name = (cfg.get("project") or {}).get("name", src.name)
    cfg.setdefault("project", {})
    cfg["project"]["name"] = name or f"{parent_name} - control (no preferred answer)"
    cfg["project"]["run_prefix"] = (cfg["project"].get("run_prefix") or "RUN") + "-CONTROL"
    cfg["project"]["control_of"] = str(src)
    # the same corpus, read where it is: a control must not get a different or stale copy
    csrc = Path((cfg.get("corpus") or {}).get("source_dir") or "01_CORPUS/source-files")
    cfg.setdefault("corpus", {})["source_dir"] = str(csrc if csrc.is_absolute() else (src / csrc).resolve())
    # no hypothesis to win, so nothing for a coach to aim at; switching it off makes that explicit
    cfg["coach"] = {**(cfg.get("coach") or {}), "enabled": False, "preferred": {}, "require_acceptance": False}
    for key in ("api_key_file",):                       # key files named relative to the parent project
        for p in (cfg.get("providers") or {}).values():
            v = p.get(key)
            if v and not Path(v).is_absolute():
                p[key] = str((src / v).resolve())
    # the parent's notebooks hold the parent's conversation: an Archivist that has already been asked
    # about the parent's question is not a fresh reader, so the control starts with no notebook saved
    nb = cfg.get("notebooklm") or {}
    dropped = len(nb.get("notebooks") or [])
    if "notebooks" in nb:
        nb["notebooks"] = []
    write_json(dst / "project.json", cfg)
    from .onramp import QUESTION_TEMPLATE
    atomic_write_text(dst / "01_FRAME" / "question.md", QUESTION_TEMPLATE)
    copied = []
    for f in ("index.md", "archivist-custom-prompt.txt", "STUDY-MAP.json", "STUDY-MAP.md", "match-fixtures.json"):
        if (src / "01_FRAME" / f).exists():
            shutil.copyfile(src / "01_FRAME" / f, dst / "01_FRAME" / f)
            copied.append(f)
    if (src / "90_METHOD" / "prompts").exists():
        for f in sorted((src / "90_METHOD" / "prompts").glob("*.md")):
            shutil.copyfile(f, dst / "90_METHOD" / "prompts" / f.name)
            copied.append(f"90_METHOD/prompts/{f.name}")
    atomic_write_text(dst / "01_FRAME" / NOTE, f"""# Control run: what was decided before any evidence was seen

Set up {utcnow()} from `{src}`. Fill this in BEFORE the quest. It is a plain note for you and for a
reader of the result; nothing checks it.

## The question

(Write the axis question here. Choose one you do not care about the answer to. If you notice you
are hoping for one of the hypotheses, pick another question: the control is only worth running if
you have no stake in it.)

## The hypotheses

- H1:
- H2:
- H3 (the evidence cannot decide):

## Why I have no preferred answer

## What will count as "the method worked"

Not a score for any hypothesis. For example: the questions reach the A and B sources of the index;
the findings pass the quote check at about the rate they did in the parent project; the two
matching passes agree about as often; the witnesses stand on several studies; the two readers of
the final assessment land near each other.

## What was fixed in advance

- No preferred hypothesis, and the coach is off (`coach.enabled: false` in `project.json`).
- The corpus is the parent project's, read in place: `{cfg["corpus"]["source_dir"]}`.
- The stop rule for the quest:
- The notebook(s): new ones, made for this control from the same sources. The parent project's notebooks
  hold its conversation and were not carried over.
- The second reader of the final assessment (`roles.assessor_b` in `project.json`):
""")
    atomic_write_text(dst / "README.md", f"""# {cfg["project"]["name"]}

A control for `{src}`: the same corpus and index, a different question, and nobody rooting for an answer.

A control is optional. It costs a quest and a pipeline run on a question you have no stake in, and it
buys one thing: evidence that the method behaves the same way when nobody wants a particular answer.
Run it if that is worth the cost to you; nothing in the parent project depends on it.

1. Fill in `01_FRAME/{NOTE}`.
2. Write your control question in `01_FRAME/question.md` (it starts as the blank template).
3. Draft the header: `cr frame "{dst}"`, edit the draft, then `cr approve "{dst}"`.
   The parent project's header was deliberately not copied; its index and Archivist prompt were, and are kept.
4. Make NEW NotebookLM notebook(s) with the same sources and pass them to the quest:
   `cr quest "{dst}" --notebook <link>`. The parent's notebook links were removed from this project because
   those notebooks hold the parent's conversation.
5. Run the pipeline as usual. The coach will not stop the run.
6. Compare the shape of the two runs (not their scores):
   `cr structure "{dst}" --against "{src}"`

A control on a different topic needs its own corpus, so it is an ordinary new project (`cr new`) with
`coach.enabled` set to false, compared with `cr structure` in the same way.
""")
    return {"control": str(dst), "of": str(src), "corpus": cfg["corpus"]["source_dir"], "copied": copied,
            "notebook_links_not_carried_over": dropped,
            "notebooks": "make new notebook(s) from the same sources for the control; the parent's hold its conversation",
            "next": f'fill in {dst / "01_FRAME" / NOTE} and {dst / "01_FRAME" / "question.md"}, then cr frame "{dst}"'}


# --------------------------------------------------------------------------- #
# the shape of a run
# --------------------------------------------------------------------------- #

def _pct(a, b):
    return round(100.0 * a / b, 1) if b else None


def shape(sc) -> dict:
    """One axis's shape (or a whole old-layout run's), from its saved records only."""
    ld = sc.load
    resp = ld("discovery", "02_query-responses/responses.json", default=[]) or []
    cands = ld("frds", "01_candidates/candidates.json", default=[]) or []
    vals = ld("frds", "04_validation-results/validations.json", default=[]) or []
    ready = [v for v in vals if str(v.get("readiness", "")).startswith("READY")]
    retained = ld("frds", "05_validated/retained-frds.json", default=None)
    retained = ready if retained is None else retained
    ws = ld("witnesses", "05_released/witnesses.json", default=[]) or []
    held = ld("witnesses", "04_repaired-or-held/held.json", default=[]) or []
    rels = ld("matching", "03_match-records/relations.json", default=[]) or []
    cov = (ld("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
    crux = ld("crux", "05_candidates/crux-candidates.json", default={}) or {}
    assess = ld("reports", "assessment.json", default={}) or {}
    usable = sum(1 for r in resp if r.get("usable"))
    qm = Counter((v.get("quote_check") or {}).get("method", "none") for v in ready)
    both = [r for r in rels if "MISSING" not in (r.get("a"), r.get("b")) and r.get("a") and r.get("b")]
    out = {
        "answers_usable": usable, "frd_candidates": len(cands),
        "candidates_per_answer": round(len(cands) / usable, 2) if usable else None,
        "validated_findings": len(ready),
        "findings_per_answer": round(len(ready) / usable, 2) if usable else None,
        "findings_quoted_word_for_word_pct": _pct(qm.get("exact", 0) + qm.get("segments", 0), len(ready)),
        "candidate_claims_right_as_written_pct": _pct(sum(1 for v in ready if v.get("verdict") == "RIGHT"), len(ready)),
        "findings_retained": len(retained),
        "witnesses_released": len(ws),
        "witnesses_held_pct": _pct(len(held), len(ws) + len(held)),
        "pairs_judged": len(rels),
        "pairs_both_passes_answered_pct": _pct(len(both), len(rels)),
        "passes_agree_when_both_answer_pct": _pct(sum(1 for r in both if r.get("a") == r.get("b")), len(both)),
        "pairs_one_pass_only_pct": _pct(sum(1 for r in rels if r.get("basis") == "ONE_PASS_ONLY"), len(rels)),
        "complete_relations": sum(1 for r in rels if r.get("final") in ("EQUIVALENT", "WITNESS_ENTAILS_UNIT")),
        "contradictions": sum(1 for r in rels if r.get("final") == "CONTRADICTS"),
        "contradictions_conditional_on_scope": sum(1 for r in rels if r.get("final") == "CONTRADICTS"
                                                   and r.get("gap_type") == "SCOPE"),
        "coverage": {h: {"status": c.get("status"), "required_parts": len(c.get("required_units", [])),
                         "covered_directly": c.get("units_covered_strict", c.get("units_covered", 0)),
                         "covered_with_a_transfer": c.get("units_covered", 0), "sets": len(c.get("sets", []))}
                     for h, c in cov.items()},
        "crux_candidates": len(crux.get("candidates", [])),
    }
    try:
        from . import studies
        by_frd = studies.frd_studies(sc, retained)
        of = {w["witness_id"]: by_frd.get(w.get("vfrd_id")) for w in ws}
        cw = studies.count(of.values())
        cc = studies.count(of.get(c["witness_id"]) for c in crux.get("candidates", []))
        out.update(studies_behind_findings=studies.count(by_frd.values())["n_studies"],
                   studies_behind_witnesses=cw["n_studies"], witnesses_per_study=(
                       round(cw["items"] / cw["n_studies"], 2) if cw["n_studies"] else None),
                   crux_candidate_studies=cc["n_studies"])
    except Exception as e:  # noqa: BLE001
        out["studies_not_counted"] = f"{type(e).__name__}: {e}"
    gauge = assess.get("gauge") or 64
    alloc = assess.get("allocations") or {}
    out["allocation_pct"] = {h: _pct(v, gauge) for vec in alloc.values() for h, v in vec.items()}
    if out["allocation_pct"]:
        out["share_of_last_listed_hypothesis_pct"] = list(out["allocation_pct"].values())[-1]
    sr = assess.get("second_reading") or {}
    if sr.get("allocations"):
        out["second_reader_pct"] = {h: _pct(v, gauge) for vec in sr["allocations"].values() for h, v in vec.items()}
        out["readers_differ_by_units"] = max(sr.get("difference_from_first", {}).values() or [None])
    return out


def run_shape(ctx) -> dict:
    """{axis id (or run id): shape}; axes with no evidence of their own are left out."""
    if not ctx.axis_layout:
        return {ctx.run_id: shape(ctx)}
    out = {}
    for sc in ctx.scopes():
        s = shape(sc)
        if s["answers_usable"] or s["validated_findings"] or s["witnesses_released"]:
            out[sc.axis_id] = s
    return out


_ROWS = [
    ("answers_usable", "Usable answers"), ("candidates_per_answer", "Candidate findings per answer"),
    ("findings_per_answer", "Validated findings per answer"),
    ("findings_quoted_word_for_word_pct", "Findings quoted word for word, %"),
    ("candidate_claims_right_as_written_pct", "Candidate claims right as written, %"),
    ("witnesses_released", "Witnesses released"), ("witnesses_held_pct", "Witnesses held, %"),
    ("studies_behind_witnesses", "Studies behind the witnesses"), ("witnesses_per_study", "Witnesses per study"),
    ("pairs_judged", "Witness-unit pairs judged"),
    ("pairs_both_passes_answered_pct", "Pairs both passes answered, %"),
    ("passes_agree_when_both_answer_pct", "Passes agree when both answer, %"),
    ("pairs_one_pass_only_pct", "Pairs with one judgment only, %"),
    ("complete_relations", "Complete relations"), ("contradictions", "Contradictions"),
    ("contradictions_conditional_on_scope", "... of which depend on a transfer of scope"),
    ("crux_candidates", "Crux candidates"), ("crux_candidate_studies", "Studies behind the crux candidates"),
    ("share_of_last_listed_hypothesis_pct", "Share given to the last-listed hypothesis, %"),
    ("readers_differ_by_units", "Two readers differ by, units"),
]


def render(cols: list[tuple[str, dict]]) -> str:
    """cols: [(column title, shape)].  One table; hypothesis-level detail underneath."""
    show = lambda v: "-" if v is None else str(v)
    out = ["# The shape of the run" + ("s" if len(cols) > 1 else ""), "",
           "What survives each stage and how the evidence is distributed. Scores for different questions cannot be "
           "compared; these shapes can. Nothing here says which hypothesis is right.", "",
           "| | " + " | ".join(t for t, _ in cols) + " |", "|---|" + "---|" * len(cols)]
    for key, label in _ROWS:
        if any(s.get(key) is not None for _, s in cols):
            out.append(f"| {label} | " + " | ".join(show(s.get(key)) for _, s in cols) + " |")
    for title, s in cols:
        out += ["", f"## {title}", ""]
        for h, c in (s.get("coverage") or {}).items():
            out.append(f"- {h}: {str(c['status']).replace('_', ' ').lower()}; {c['covered_directly']} of "
                       f"{c['required_parts']} required parts covered directly, {c['covered_with_a_transfer']} with a "
                       f"named transfer; {c['sets']} sets")
        if s.get("allocation_pct"):
            out.append("- Final assessment, % of the gauge: " + ", ".join(f"{h} {v}" for h, v in s["allocation_pct"].items()))
        if s.get("second_reader_pct"):
            out.append("- Second reader, % of the gauge: " + ", ".join(f"{h} {v}" for h, v in s["second_reader_pct"].items()))
    return "\n".join(out) + "\n"
