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


def gate(axis: dict, report: dict | None, options: dict) -> list[dict]:
    return bedtime_gate.check(report) if _applies(axis, options) else []
