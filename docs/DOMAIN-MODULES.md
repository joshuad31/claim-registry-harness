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

## Added 2026-11-11 (evening), from the pre-run audit

- A gate now receives `facts` from the harness: the allocation drivers with each FRD's real source
  file, and the non-citable synthesis list. The `levo` gate uses them for three interim checks:
  the frame's population and food gaps come from the module options, not the assessor; R16 (no
  driver from a synthesis file); R17 (every allocation driver must be declared).
- `corpus.synthesis_sources` and `corpus.duplicates`: FRDs from those files are left out of the FRD
  evaluation and counted on the page.
- `frd_assess.axis_only`: axes that get no combined reading.
- `frd_assess.max_output_tokens` (default 32000); a cut-off answer is asked for once more.
- `frd_assess.gate_retry_cap` (default 2): after that many corrections a person must look. Every
  earlier evaluation is kept in `evaluation-history.jsonl` beside `evaluation.json`.
- Still to install: the fuller harness-side gate (`bedtime_gate_v2.py`), rules R16 to R22 and the
  A2-P-v1 / A2-D-v1 frames from the audit's `proposed/` folder.
