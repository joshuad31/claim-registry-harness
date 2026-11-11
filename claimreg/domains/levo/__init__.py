"""LEVO (levothyroxine) domain module.  Used only when a project names it under `domain_modules`.

Contents: the bedtime-dosing evidence rules (R1-R15, `bedtime_ruleset.md`) and their acceptance
gate (`bedtime_gate.py`), written after the audit of the first bedtime-axis assessment.  They apply
to one axis, named by the option `bedtime_axis` (default "A2").  They fix no result: the rules
govern how evidence may be used, and a rejected report is sent back for correction, never scored.
"""

from __future__ import annotations

from pathlib import Path

from . import bedtime_gate

HERE = Path(__file__).resolve().parent


def _applies(axis: dict, options: dict) -> bool:
    return axis.get("axis_id") == options.get("bedtime_axis", "A2")


def axis_rules(axis: dict, options: dict) -> str:
    if not _applies(axis, options):
        return ""
    return ("AXIS-SPECIFIC EVIDENCE-USE RULES (LEVO bedtime dosing). These rules govern how evidence may be used. "
            "They name no winning hypothesis. Mechanistic and exposure evidence (for example, what coffee, calcium or "
            "iron taken with the tablet does to absorption and TSH) is evidence that discriminates between the "
            "hypotheses and must be scored as such, with its transfer argument stated.\n\n"
            + (HERE / "bedtime_ruleset.md").read_text(encoding="utf-8"))


def gate_contract(axis: dict, options: dict) -> str:
    return bedtime_gate.CONTRACT if _applies(axis, options) else ""


def gate(axis: dict, report: dict | None, options: dict, facts: dict | None = None) -> list[dict]:
    """The declared-use gate, plus three checks against facts the harness supplies (interim, until
    the fuller harness-side gate is installed):

    - the frame's target population and food gaps come from the module options, not the assessor;
    - R16: no allocation driver may be an FRD drawn from a non-citable synthesis file;
    - R17: every FRD named as an allocation driver must also be declared in the gate report.
    """
    if not _applies(axis, options):
        return []
    facts = facts or {}
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
