"""Domain modules: investigation-specific evidence rules, kept out of the general harness.

A domain module is a package under `claimreg/domains/`.  It is used only by a project or run whose
configuration names it:

    "domain_modules": {"levo": {"bedtime_axis": "A2"}}

Nothing here is loaded, and no prompt changes, for a project that does not name a module.  A
module may define any of:

    axis_rules(axis: dict, options: dict) -> str     text added to the preliminary FRD assessment
                                                     prompt for that axis ("" = nothing)
    gate_contract(axis: dict, options: dict) -> str  what the assessor must append for the gate
    gate(axis: dict, report: dict, options: dict) -> list[{"rule", "message"}]
                                                     an acceptance check on the assessor's declared
                                                     evidence uses; an empty list accepts
"""

from __future__ import annotations

import importlib


def active(cfg: dict) -> list[tuple[str, object, dict]]:
    out = []
    for name, options in (cfg.get("domain_modules") or {}).items():
        if options is False:
            continue
        out.append((name, importlib.import_module(f"{__name__}.{name}"), options if isinstance(options, dict) else {}))
    return out


def axis_rules(cfg: dict, axis: dict) -> str:
    return "\n\n".join(t for _, m, o in active(cfg) if hasattr(m, "axis_rules") for t in [m.axis_rules(axis, o)] if t)


def gate_contract(cfg: dict, axis: dict) -> str:
    return "\n\n".join(t for _, m, o in active(cfg) if hasattr(m, "gate_contract") for t in [m.gate_contract(axis, o)] if t)


def run_gates(cfg: dict, axis: dict, report: dict | None) -> dict | None:
    """None when no module gates this axis; else {"modules", "accepted", "errors"}."""
    mods = [(n, m, o) for n, m, o in active(cfg) if hasattr(m, "gate") and hasattr(m, "gate_contract") and m.gate_contract(axis, o)]
    if not mods:
        return None
    errors = []
    for n, m, o in mods:
        errors += [dict(e, module=n) for e in m.gate(axis, report, o)]
    return {"modules": [n for n, _, _ in mods], "accepted": not errors, "errors": errors}
