"""Final assessment: ACH_Eval (verbatim) applied once to the validated witness registry.

This answers a different question from crux identification (spec 33: never
claim one validates the other).  Allocations are uncalibrated working
judgments about what the record warrants, not probabilities.

The assessment spec is written for ONE enabled axis per pass ("use one axis unless a second
distinct question warrants another").  Frames created by the v2 generator can carry more than
two axes, and a single multi-axis call silently wrote allocations for only the first two axes
(the 2026-11-11 LEVO run: A3 and A4 each summed to 0).  So each axis is assessed in its own
pass — the axis's own question and hypotheses, with the coverage summary filtered to that
axis — and the per-axis vectors are merged into one record.
"""

from __future__ import annotations

import re

from .header import hypothesis_text
from .llm.base import LLMRequest
from .llm.jsonparse import JSONExtractError, extract_json
from .util import atomic_write_text, utcnow


def coverage_summary_text(ctx, axis_id: str | None = None) -> str:
    cov = (ctx.load("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
    if axis_id:
        cov = {hid: c for hid, c in cov.items() if str(hid).startswith(str(axis_id) + "-")}
    crux = ctx.load("crux", "05_candidates/crux-candidates.json", default={}) or {}
    units = {u["unit_id"]: u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])}
    lines = []
    for hid, c in cov.items():
        lines.append(f"{hid}: {c['status']}; required units covered {c.get('units_covered', 0)}/"
                     f"{len(c.get('required_units', []))}; deletion-minimal sets {len(c.get('sets', []))} "
                     f"({c.get('search_status')})")
        for u in c.get("uncovered_units", []):
            lines.append(f"   uncovered: {u} - {units.get(u, {}).get('text', '')}")
    if not axis_id:
        for cand in crux.get("candidates", []):
            lines.append(f"CRUX CANDIDATE {cand['witness_id']} (home {cand['home']}) defeats "
                         f"{', '.join(cand['defeats'])}"
                         + ("".join(f" [vs {r}: only if {a['assumption']}]"
                                    for r, asm in (cand.get("assumptions") or {}).items() for a in asm[:2])))
    for d in (crux.get("diagnostic_witnesses", []) or [])[:20]:
        if axis_id and not str(d.get("home", "")).startswith(str(axis_id) + "-"):
            continue
        lines.append(f"diagnostic (home incomplete) {d['witness_id']} home {d['home']} fails T1+T2 vs "
                     f"{d['rival']}")
    return "\n".join(lines) or "(no coverage records)"


def _axis_context(axis: dict) -> str:
    """The frozen axis definition plus its hypotheses, as the assessment prompt expects it."""
    head = f"AXIS {axis['axis_id']} ({axis.get('approval', 'UNKNOWN')}): {axis.get('question', '')}"
    if axis.get("boundary"):
        head += f"\nGoverning boundary: {axis['boundary']}"
    if axis.get("scope"):
        head += f"\nScope: {axis['scope']}"
    body = "\n\n".join(hypothesis_text(h) for h in axis.get("hypotheses", []))
    return head + ("\n\n" + body if body else "")


def check_vector(vec, ids: list[str], gauge: int, label: str) -> tuple[dict, list[str]]:
    """An allocation is usable when it names exactly this axis's hypotheses, gives each a whole
    number from 0 to the gauge, and sums to the gauge.  Returns (vector, problems); the vector is
    empty when any problem was found, so a broken allocation is never carried into a report."""
    if not isinstance(vec, dict) or not vec:
        return {}, [f"{label}: no allocation for this axis"]
    problems = []
    unknown = sorted(k for k in vec if k not in ids)
    if unknown:
        problems.append(f"{label}: units given to {', '.join(map(str, unknown))}, which this axis does not have")
    missing = [i for i in ids if i not in vec]
    if missing:
        problems.append(f"{label}: no units stated for {', '.join(missing)}")
    out = {}
    for i in ids:
        if i not in vec:
            continue
        v = vec[i]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or int(v) != v:
            problems.append(f"{label}: {i} is not a whole number ({v!r})")
            continue
        if not 0 <= int(v) <= gauge:
            problems.append(f"{label}: {i} has {int(v)} units; each hypothesis takes 0 to {gauge}")
        out[i] = int(v)
    if not problems and sum(out.values()) != gauge:
        problems.append(f"{label}: units sum to {sum(out.values())}, not {gauge}")
    return ({} if problems else out), problems


def _parse_assessment(res, gauge: int, axis_id: str, ids: list[str] | None = None) -> tuple[dict, list[str]]:
    """The fenced JSON block from one axis's assessment, plus any problems with its vector."""
    data: dict = {}
    for block in reversed(re.findall(r"```json\s*\n(.*?)\n?```", res.text or "", re.S)):
        try:
            candidate = extract_json(block)
            if isinstance(candidate, dict) and "allocations" in candidate:
                data = candidate
                break
        except JSONExtractError:
            continue
    if not data:
        return {}, [f"{axis_id}: no allocation JSON block in the assessment"]
    vec = (data.get("allocations") or {}).get(axis_id) or {}
    if ids is None:                       # no frame to check against: range and sum only
        ids = list(vec) if isinstance(vec, dict) else []
    good, problems = check_vector(vec, ids, gauge, axis_id)
    if problems:
        data = {**data, "rejected_allocations": {axis_id: vec},
                "allocations": {k: v for k, v in (data.get("allocations") or {}).items() if k != axis_id}}
    return data, problems


def assess_stage(ctx) -> dict:
    if not ctx.cfg.get("assess", {}).get("enabled", True):
        return {"skipped": True}
    frame = ctx.frame
    gauge = int(frame.get("gauge") or ctx.cfg["quest"].get("gauge", 64))
    # Large registries (300+ witnesses) make the Markdown artifact run past the provider's output
    # cap before the contract block at the end. Ask for the block first and allow more room.
    max_out = int((ctx.cfg.get("assess") or {}).get("max_output_tokens") or 48000)
    ws = ctx.load("witnesses", "05_released/witnesses.json", default=[]) or []
    reg = "\n".join(f"{w['witness_id']} | {w['vfrd_id']} | {w['qid']} | {w['source_file']} | {w['text']}" for w in ws)
    axes = frame["axes"]
    merged = {key: {} for key in ("allocations", "basis_confidence", "drivers", "strongest_objection",
                                  "reversal_finding")}
    problems: list[str] = []
    fragments: list[str] = []
    call_keys: dict[str, str] = {}
    models: dict[str, str] = {}
    requests: list[LLMRequest] = []
    axis_order: list[str] = []
    ids_of = {a["axis_id"]: [h["id"] for h in a.get("hypotheses", [])] for a in axes}
    rejected: dict = {}
    for axis in axes:
        ax_id = axis["axis_id"]
        system, user, _ = ctx.prompts.render(
            "assess.md", GAUGE=gauge, GOAL=axis.get("question", frame.get("title", "")),
            AXIS2="disabled (this pass assesses exactly one axis)",
            INVESTIGATION_ID=f"{ctx.run_id}:{ax_id}",
            HYPOTHESES=_axis_context(axis),
            WITNESSES=reg or "(no released witnesses)",
            COVERAGE_SUMMARY=coverage_summary_text(ctx, ax_id))
        user = (user + "\n\nORDER OVERRIDE (must follow): put the required fenced JSON contract block "
                "FIRST in your response, before the Markdown artifact. The witness registry is long and "
                "the artifact may be cut off; the allocation block must not be lost. One fenced ```json "
                "block, allocations for this axis only, integer units summing to the gauge.")
        requests.append(LLMRequest(role="assessor", system=system, user=user, expect_json=False,
                                   tag=f"final-assessment-{ax_id}", max_output_tokens=max_out,
                                   meta={"frame": frame, "gauge": gauge, "axis": ax_id}))
        axis_order.append(ax_id)
    # The axes are independent, so ask for all of them at once instead of one slow call after another.
    responses = ctx.llm.call_many(requests) if requests else []
    for ax_id, res in zip(axis_order, responses):
        if res is None:
            problems.append(f"{ax_id}: no assessment response")
            continue
        if str(getattr(res, "parse_error", "") or "").startswith("provider error"):
            problems.append(f"{ax_id}: {res.parse_error}")
            continue
        fragments.append(f"<!-- axis {ax_id} -->\n{res.text}")
        call_keys[ax_id], models[ax_id] = res.key, res.model
        data, axis_problems = _parse_assessment(res, gauge, ax_id, ids_of[ax_id])
        problems.extend(axis_problems)
        if (data or {}).get("rejected_allocations"):
            rejected.update(data["rejected_allocations"])
        for key in merged:
            value = (data or {}).get(key) or {}
            if isinstance(value, dict) and value.get(ax_id) not in (None, ""):
                merged[key][ax_id] = value[ax_id]
    atomic_write_text(ctx.p("reports", "assessment-fragment.md"),
                      "\n\n".join(fragments) or "(no assessment fragment was produced)")
    out = {"gauge": gauge, **merged, "problems": problems,
           **({"rejected_allocations": rejected} if rejected else {}), "call_keys": call_keys, "models": models,
           "time": utcnow(),
           "caveat": "Uncalibrated working judgments about what this run's validated record warrants; "
                     "not probabilities of truth and not validated by the crux result."}
    ctx.save("reports", "assessment.json", out, "final-assessment")
    return {"allocations": merged["allocations"], "problems": problems}
