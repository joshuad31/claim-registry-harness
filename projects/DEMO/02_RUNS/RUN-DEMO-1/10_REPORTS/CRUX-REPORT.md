# Crux report — Foliar silicate and drought-stressed wheat (SYNTHETIC DEMO)

Run `RUN-DEMO-1` · generated 2026-10-30T03:39:08+00:00 · harness claimreg

> Everything below is **best understood from this corpus and this run**. The protocol does not guarantee that every relevant item was extracted from the corpus, and a crux result does not establish a witness's truth, authority, independence or dispositive weight.

## Analyst summary (generated from the run record; adds no evidence)

This run used 24 usable discovery answers to build 77 released witnesses, then judged every shortlisted witness-unit pair against 9 required coverage units across 3 frozen hypotheses. No hypothesis reached complete coverage: 0 of 9 required units were established by at least one approved option. The evidence packets name, for every uncovered part, the nearest judged evidence and mark it as not a match, so the gap can be reviewed rather than assumed. No witness qualified as a crux candidate. A crux candidate must first belong to a deletion-minimal coverage set of its home hypothesis, so an uncovered hypothesis produces none by construction, not by a silent failure. Discovery stopped at its operational ceiling (6 rounds, 24 questions); that is an operational limit, not a scientific completion finding. Every quotation behind a witness was checked against its named source file, so each row of the evidence packets can be followed back to a passage. These conclusions are best understood from this corpus and this run: the local engine judges meaning by explicit lexical and structural rules, so its matching is a stated approximation, not model understanding, and the final assessment is a bookkeeping count, not ACH_Eval judgment.

## The run at a glance

| Stage | Result |
|---|---|
| Corpus | 5 sources, 7,854 bytes |
| Discovery | 24 questions, 24 usable answers (OPERATIONAL_LIMIT) |
| FRDs | 96 candidates → 77 retained READY |
| Witnesses | 77 released, 0 held |
| Matching | 690 pairs judged (642 agreed, 48 model-adjudicated) |
| Coverage | A1-H1: no complete coverage (0/3 units, 0 sets); A1-H2: no complete coverage (0/3 units, 0 sets); A1-H3: no complete coverage (0/3 units, 0 sets) |
| Crux | 0 candidates; 0 diagnostic witnesses (extended review) |

## Crux candidates

No witness qualified as a crux candidate against any rival. A crux candidate must belong to a deletion-minimal coverage set of its home hypothesis; see the coverage section for which hypotheses reached complete coverage and which required parts remain uncovered.

## Coverage of each hypothesis

**Axis A1** (unknown): Does foliar silicate treatment improve grain yield of drought-stressed wheat in the field?

- **A1-H1** — NO_COMPLETE_COVERAGE; required units covered 0/3; 0 deletion-minimal set(s) [NOT_RUN]
  - uncovered `A1-H1-R1`: Foliar silicate treatment increases grain yield of drought-stressed wheat in field conditions
  - uncovered `A1-H1-R2`: The effect is large enough and repeatable enough to justify a field trial
  - uncovered `A1-H1-R3`: the mechanism reported in controlled studies transfers to field-grown wheat
- **A1-H2** — NO_COMPLETE_COVERAGE; required units covered 0/3; 0 deletion-minimal set(s) [NOT_RUN]
  - uncovered `A1-H2-R1`: Foliar silicate treatment does not increase grain yield of drought-stressed wheat in the field
  - uncovered `A1-H2-R2`: The positive results come from greenhouse or model-organism work that does not transfer
  - uncovered `A1-H2-R3`: field trials show no yield benefit
- **A1-H3** — NO_COMPLETE_COVERAGE; required units covered 0/3; 0 deletion-minimal set(s) [NOT_RUN]
  - uncovered `A1-H3-R1`: Existing evidence cannot determine whether foliar silicate increases field grain yield under drought
  - uncovered `A1-H3-R2`: Some controlled studies report benefits, field results are mixed or null
  - uncovered `A1-H3-R3`: the decisive field comparison has not been made

## Final assessment (ACH_Eval on the validated witness registry)

Uncalibrated working judgments, not probabilities; they answer a different question from crux identification.

- Axis A1: A1-H1 22/64, A1-H2 21/64, A1-H3 21/64 — basis/confidence: local bookkeeping only: count of witnesses sharing terminology with each hypothesis
  - strongest objection: see the evidence packets: no hypothesis reaches complete coverage

## Compression against the Problems-note targets

| Metric | Value | Target | Met |
|---|---|---|---|
| FRD database / corpus | 10.5029 | <= 0.250 | no |
| validated FRD db / FRD db | 1.078 | < 2.0 | yes |
| witness db / validated FRD db | 0.765 | <= 0.25 | no |
| witnesses used by deletion-minimal sets | 0.0 | < 0.33 | n/a |
| final witness text / corpus | 0.0 | about 0.01 | n/a |
| FRDs per response (max) | 4 | <= 4 | yes |

## Limitations and disclosures

- Engines that answered calls in this run: local:local-rules-v1.8 (see `00_RUN-CONTROL/model-and-human-decisions/llm-calls.jsonl`). A local engine judges by explicit lexical and structural rules, not model understanding; every relation is labelled with its basis and can be overruled.
- Semantic matching is judged by the configured matcher. 642 relations were approved by agreement of two independent passes; 48 disagreements were settled by a third independent context (not a human); 0 remain ABSTAIN.
- 1620 witness-unit pairs were outside the lexical shortlist and count as no relation; missed matches are the main source of false cruxes (spec 29.1). Every witness used in crux testing was judged against every rival unit.
- Matcher qualification: pass A 22/22, pass B 22/22 fixtures; unqualified patterns: none.
- Language layer: off (identity transcoder: matching used raw witness and unit text).
- Witness ceiling: 60 words, with 0 recorded per-witness exceptions up to 80 words; 0 witnesses held.
- Incompatibility approval uses the harness definition (two passes agree on same-quantity conflict or opposite polarity at the same scope): 0 approved.
- Coverage units are an internal representation derived by the configured engine from the human-written hypotheses; each unit's anchor quotation was checked verbatim against the frozen text.

## Audit trail

- `EVIDENCE-PACKETS.md` in this folder: per hypothesis, the controlling claims, strongest objections, material qualifications and gaps, each tied to witnesses and source files.
- `report.html` in this folder: click any crux or witness to see its FRD, the verbatim source quote, the producing question and the Archivist answer.
- Machine records: `07_MATCHING/03_match-records/relations.json`, `08_COVERAGE/coverage.json`, `09_CRUX/03_portability-tests/tests.json`, `00_RUN-CONTROL/model-and-human-decisions/llm-calls.jsonl`.
- Every model call's exact prompt and answer is in the project's `cache/llm` folder, keyed by the call log.
