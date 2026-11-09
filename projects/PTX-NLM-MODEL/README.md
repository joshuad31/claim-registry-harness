# PTX-NLM-MODEL — the first run whose reasoning roles all ran on a frontier model

This project is a **demonstration run**, not a new research result. It imports the same 156-answer
NotebookLM quest as `Claude output\quests\PTX-NLM-2026-11-09\` (the 2026-11-09 timed quest, which
passed all five throughput checks) and runs the evidence pipeline with `gpt-5.2` in place of the
deterministic local engine.

Every model-facing reasoning role was routed to OpenAI GPT-5.2 through the `openai` provider:
`unit_deriver`, `frd_generator`, `frd_validator`, `witness_constructor`, `witness_auditor`,
`matcher_a`, `matcher_b`, `match_adjudicator`, `joint_checker`, `incompat_checker`, `assessor` and
`reporter`. The provider block in `project.json` names `OPENAI_API_KEY`; it does not contain a key.

- Run: `02_RUNS\RUN-PTX-NLM-MODEL\`
- Upstream quest record: `Claude output\quests\PTX-NLM-2026-11-09\` (answers, manager workspace,
  closeout, scorecard). The third-party papers are not distributed; the corpus manifests are here.

## What the model changed

| Stage | Local engine (156 answers, same quest) | GPT-5.2 |
|---|---:|---:|
| Candidate FRDs | 605 | 558 |
| Validation records | 605 | 1,374 (558 unique FRDs, multi-source citations) |
| READY (source-validated) | 424 | **655** (570 records failed the verbatim quote gate) |
| Retained after budget | 424 | 527 |
| Witnesses released | 327 | 114 |
| Complete relations | 0 | 0 |
| Coverage sets | 0 | **0** |
| Crux candidates | 0 | **0** |
| Report words | 1,529 | 2,124 |
| Model calls / cost | 0 / $0 | 2,698 / **$41.91** |

## The honest reading

1. **A frontier model raises FRD quality.** It produced 655 source-validated FRDs against the local
   engine's 424, and the mechanical quote gate still blocked 570 records where the model's
   "quotation" was not verbatim in the source. Nothing was accepted on the model's word alone.
2. **It does not break the zero-coverage wall.** Two independent engines — a lexical one and
   GPT-5.2 — both reach no complete relations, no deletion-minimal coverage sets and no crux
   candidates on this corpus and header. The matching/witness stage is therefore the next place to
   look: relation distribution, the 413 witnesses held back by the fidelity audit, and the strictness
   of the `witness`/`matching` configuration, compared with `projects\WORKED\`, where 42 coverage
   sets and 7 crux candidates are produced.
3. **The throughput result is independent.** This run does not re-test the quest; the quest was
   already timed and scored by `cr quest-score` before the evidence pipeline ran.

`cr verify` on this project checks everything except the quotations, because the third-party source
files are not in the repository; the warnings say so rather than failing.
