"""LEVO (levothyroxine) domain module.  Used only when a project names it under `domain_modules`.

Contents:
  * the bedtime-dosing evidence rules R1-R15 (`bedtime_ruleset.md`) plus the R16-R22 addendum
    installed from the 2026-11-11 pre-run audit;
  * the v2 acceptance gate (`bedtime_gate_v2.py`), which the harness feeds facts the assessor
    cannot change: the frozen frame, each allocation driver's real source file, the non-citable
    synthesis list and the duplicate-copy map;
  * the frozen A2-P-v1 practical-strategy frame values (the approved header supplies the wording).

They apply to one axis, named by the option `bedtime_axis` (default "A2").  They fix no result: the
rules govern how evidence may be used, and a rejected report is sent back for correction, never
scored.
"""

from __future__ import annotations

from pathlib import Path

from . import bedtime_gate

try:  # installed 2026-11-11 (Grok Bot / Gemini Carbon audit); absent in older checkouts
    from . import bedtime_gate_v2 as _v2
except ImportError:  # pragma: no cover - keeps the module importable without the v2 file
    _v2 = None

HERE = Path(__file__).resolve().parent

# The approved A2-P-v1 practical-strategy frame.  A run may override these under `domain_modules.levo`
# in project.json (or RUN-OVERRIDES.json); the gate supplies them to the assessor's report so the
# model can never widen the population or move the target gaps.
FRAME_DEFAULTS = {
    "comparison_type": "practical_strategy",
    "target_bedtime_min_gap_minutes": 180,
    "target_morning_min_gap_minutes": 60,
    "target_population": "persistent_high_tsh_boundary",
    "success_logic": "any",
    "accepted_outcomes": ["tsh_target", "ft4", "symptoms"],
}


def _applies(axis: dict, options: dict) -> bool:
    return axis.get("axis_id") == options.get("bedtime_axis", "A2")


def _ids(axis: dict, facts: dict) -> list[str]:
    ids = facts.get("hypothesis_ids") or [h.get("id") for h in (axis.get("hypotheses") or []) if h.get("id")]
    return list(ids) or ["A2-H1", "A2-H2", "A2-H3"]


def frozen_frame(axis: dict, options: dict, facts: dict | None = None) -> dict:
    """The frame the harness supplies; the approved header remains the controlling human statement."""
    facts = facts or {}
    frame = {k: options.get(k, FRAME_DEFAULTS[k]) for k in FRAME_DEFAULTS}
    frame["hypothesis_ids"] = _ids(axis, facts)
    frame["gauge"] = int(options.get("gauge", facts.get("gauge", 64)))
    return frame


def axis_rules(axis: dict, options: dict) -> str:
    if not _applies(axis, options):
        return ""
    return ("AXIS-SPECIFIC EVIDENCE-USE RULES (LEVO bedtime dosing). These rules govern how evidence may be used. "
            "They name no winning hypothesis. Mechanistic and exposure evidence (for example, what coffee, calcium or "
            "iron taken with the tablet does to absorption and TSH) is evidence that discriminates between the "
            "hypotheses and must be scored as such, with its transfer argument stated.\n\n"
            + (HERE / "bedtime_ruleset.md").read_text(encoding="utf-8"))


def gate_contract(axis: dict, options: dict) -> str:
    if not _applies(axis, options):
        return ""
    return _v2.CONTRACT if _v2 is not None else bedtime_gate.CONTRACT


def gate(axis: dict, report: dict | None, options: dict, facts: dict | None = None) -> list[dict]:
    """The v2 acceptance gate, fed with facts the harness knows and the assessor cannot change.

    `facts` carries the allocation drivers with each FRD's real source file, the non-citable
    synthesis list, the duplicate-copy map and the unknown driver ids (see frd_assess._Job.finish).
    A checkout without `bedtime_gate_v2.py` falls back to the interim 2026-11-11 checks.
    """
    if not _applies(axis, options):
        return []
    facts = facts or {}
    ids = _ids(axis, facts)
    if _v2 is not None:
        ctx = {
            "frame": frozen_frame(axis, options, facts),
            "allocation_drivers": [
                {"frd_id": d.get("frd_id", ""), "favors": d.get("favors", ""), "source_file": d.get("source_file", "")}
                for d in (facts.get("drivers") or []) if isinstance(d, dict)
            ],
            "synthesis_sources": list(facts.get("synthesis_sources") or []),
            "duplicates": dict(facts.get("duplicates") or {}),
            "h1_id": ids[0],
            "min_drivers": int(options.get("min_drivers", 3)),
            "unknown_driver_ids": list(facts.get("unknown_driver_ids")
                                       or facts.get("driver_ids_not_in_registry") or []),
        }
        return _v2.check(report, ctx)

    # Fallback: the interim checks written before the v2 gate was available.
    errors = []
    if isinstance(report, dict):
        report = {**report, "frame": {**(report.get("frame") or {}),
                                      "target_population": options.get("target_population", "persistent_high_tsh_boundary"),
                                      "target_bedtime_min_gap_minutes": int(options.get("bedtime_gap_minutes", 180)),
                                      "target_morning_min_gap_minutes": int(options.get("morning_gap_minutes", 60))}}
        declared = {str(d.get("frd_id", "")).strip() for d in report.get("drivers", []) if isinstance(d, dict)}
        missing = [d["frd_id"] for d in facts.get("drivers", []) if d["frd_id"] not in declared]
        if missing:
            errors.append({"rule": "R17", "message": "Allocation drivers not declared in the gate report: "
                                                     + ", ".join(missing[:8])})
    synth = [d["frd_id"] for d in facts.get("drivers", []) if d.get("is_synthesis")]
    if synth:
        errors.append({"rule": "R16", "message": "Allocation drivers drawn from non-citable synthesis files: "
                                                 + ", ".join(synth[:8])})
    return bedtime_gate.check(report) + errors
