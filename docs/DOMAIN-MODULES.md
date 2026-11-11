# Domain modules

*2026-11-11. Code: `claimreg/domains/`.*

Rules that belong to one investigation live in a domain module, not in the general harness. A
project that does not name a module never loads it and its prompts are unchanged
(`tests/test_domain_levo.py`, `test_a_project_that_does_not_name_the_module_never_sees_it`).

Turn one on in `project.json`, or for one run in that run's `RUN-OVERRIDES.json`:

    "domain_modules": {"levo": {"bedtime_axis": "A2"}}

A module may supply, per axis:

- `axis_rules`: text added to the preliminary FRD assessment prompt (`frd_assess`).
- `gate_contract` and `gate`: a structured declaration the assessor must append, and a check on it.
  A report the gate rejects is **returned for correction**: its allocation is withheld, recorded as
  `allocation_withheld_pending_correction`, and no units are moved to any hypothesis. Rerun with
  `cr run <project> --run <id> --only frd_assess --force frd_assess`; the assessor is then shown
  what the gate found.

A gate checks what the assessor declares. It cannot tell whether the declaration is faithful, so a
person still reads the drivers against their sources.

## `levo`

- `bedtime_ruleset.md`: rules R1 to R15 for the bedtime-dosing axis. They govern evidence use and
  name no winning hypothesis.
- `bedtime_gate.py`: the acceptance gate, with a catalog of three trial protocols (Bolk 2010,
  Bach-Huynh 2009, de Mello 2022) and 16 reference cases in `gate_examples.json`.
- Applies only to the axis named by `bedtime_axis` (default `A2`).
- Not in the module yet: the new practical-strategy and decision-to-offer frames. Those are header
  changes and need the researcher's approval.
