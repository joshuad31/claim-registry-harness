"""Final assessment: ACH_Eval (verbatim) applied once to the validated witness registry.

This answers a different question from crux identification (spec 33: never
claim one validates the other).  Allocations are uncalibrated working
judgments about what the record warrants, not probabilities.
"""

from __future__ import annotations

import re

from .header import all_hypotheses, hypothesis_text
from .llm.base import LLMRequest
from .llm.jsonparse import JSONExtractError, extract_json
from .util import atomic_write_text, utcnow


def coverage_summary_text(ctx) -> str:
    cov = (ctx.load("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
    crux = ctx.load("crux", "05_candidates/crux-candidates.json", default={}) or {}
    units = {u["unit_id"]: u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])}
    lines = []
    for hid, c in cov.items():
        lines.append(f"{hid}: {c['status']}; required units covered {c.get('units_covered', 0)}/"
                     f"{len(c.get('required_units', []))}; deletion-minimal sets {len(c.get('sets', []))} "
                     f"({c.get('search_status')})")
        for u in c.get("uncovered_units", []):
            lines.append(f"   uncovered: {u} - {units.get(u, {}).get('text', '')}")
    for cand in crux.get("candidates", []):
        lines.append(f"CRUX CANDIDATE {cand['witness_id']} (home {cand['home']}) defeats {', '.join(cand['defeats'])}")
    for d in crux.get("diagnostic_witnesses", [])[:20]:
        lines.append(f"diagnostic (home incomplete) {d['witness_id']} home {d['home']} fails T1+T2 vs {d['rival']}")
    return "\n".join(lines) or "(no coverage records)"


def assess_stage(ctx) -> dict:
    if not ctx.cfg.get("assess", {}).get("enabled", True):
        return {"skipped": True}
    frame = ctx.frame
    gauge = int(frame.get("gauge") or ctx.cfg["quest"].get("gauge", 64))
    ws = ctx.load("witnesses", "05_released/witnesses.json", default=[]) or []
    reg = "\n".join(f"{w['witness_id']} | {w['vfrd_id']} | {w['qid']} | {w['source_file']} | {w['text']}" for w in ws)
    axes = frame["axes"]
    system, user, _ = ctx.prompts.render(
        "assess.md", GAUGE=gauge, GOAL=axes[0].get("question", frame.get("title", "")),
        AXIS2=("enabled with definition (see hypotheses)" if len(axes) > 1 else "disabled"),
        INVESTIGATION_ID=ctx.run_id,
        HYPOTHESES="\n\n".join(f"AXIS {h['axis_id']} ({h.get('axis_approval', '')}): {h.get('axis_question', '')}\n"
                               + hypothesis_text(h) for h in all_hypotheses(frame)),
        WITNESSES=reg or "(no released witnesses)", COVERAGE_SUMMARY=coverage_summary_text(ctx))
    from .llm.base import ProviderError
    try:
        res = ctx.llm.call(LLMRequest(role="assessor", system=system, user=user, expect_json=False,
                                      tag="final-assessment", max_output_tokens=32000,
                                      meta={"frame": frame, "gauge": gauge}))
    except ProviderError as e:
        if "skipped by the queue operator" not in str(e):
            raise
        out = {"gauge": gauge, "allocations": {}, "problems": [f"no assessment: {e}"], "time": utcnow(),
               "caveat": "The assessment request was not answered; nothing was invented in its place."}
        ctx.save("reports", "assessment.json", out, "final-assessment")
        return {"allocations": {}, "problems": out["problems"]}
    atomic_write_text(ctx.p("reports", "assessment-fragment.md"), res.text)
    data = {}
    for b in reversed(re.findall(r"```json\s*\n(.*?)\n?```", res.text or "", re.S)):
        try:
            data = extract_json(b)
            if isinstance(data, dict) and "allocations" in data:
                break
        except JSONExtractError:
            continue
    alloc = (data or {}).get("allocations", {}) if isinstance(data, dict) else {}
    problems = []
    for ax in axes:
        vec = alloc.get(ax["axis_id"], {})
        try:
            s = sum(int(v) for v in vec.values())
            if s != gauge:
                problems.append(f"{ax['axis_id']}: units sum to {s}, not {gauge}")
        except (TypeError, ValueError):
            problems.append(f"{ax['axis_id']}: non-integer units")
    out = {"gauge": gauge, "allocations": alloc, "drivers": (data or {}).get("drivers", {}),
           "basis_confidence": (data or {}).get("basis_confidence", {}),
           "strongest_objection": (data or {}).get("strongest_objection", {}),
           "reversal_finding": (data or {}).get("reversal_finding", {}),
           "problems": problems, "call_key": res.key, "model": res.model, "time": utcnow(),
           "caveat": "Uncalibrated working judgments about what this run's validated record warrants; "
                     "not probabilities of truth and not validated by the crux result."}
    ctx.save("reports", "assessment.json", out, "final-assessment")
    return {"allocations": alloc, "problems": problems}
