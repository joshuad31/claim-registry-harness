# Preliminary evaluation of the validated FRDs

*Specification, 2026-11-11. Implemented in `claimreg/frd_assess.py` and `claimreg/pipeline.py`
(stage `frd_assess`). Companion to `docs/AXIS-DATABASES.md`.*

## 1. Why this stage exists

The researcher's order of work is:

1. header, index, sources added or removed, Archivist prompt; the researcher deploys the notebook
   and pastes the prompt personally;
2. the automated quest; questions and answers logged per axis; FRDs and validated FRDs per axis;
3. **an evaluation of the validated FRDs, per axis and combined** (this stage);
4. only then, if the researcher asks: dictionary, canonicalizer, transcoding, witnesses, matching,
   coverage, crux, final assessment, report.

Before this stage existed the first ACH_Eval reading came at the very end, after hours of
matching. Now it comes straight after FRD retention, and the run halts there.

## 2. What is assessed

For each axis, ACH_Eval (verbatim, the same text the Coordinator uses) is applied twice:

| Reading | Evidence set | Where the records go |
|---|---|---|
| axis-only | the retained validated FRDs filed under that axis | `AXIS-<id>/03_FRDS/06_evaluation/` |
| combined | the retained validated FRDs of every axis | `SHARED/03_FRDS-COMBINED/for-<axis>/` |

- The combined set is a **disjoint union**: its count equals the sum of the axis counts, no FRD
  appears twice, and every row keeps its `home_axis`. The stage refuses to run otherwise. The set
  is written once to `SHARED/03_FRDS-COMBINED/combined-validated-frds.json`.
- The combined reading lives in SHARED, not in the axis folder, because it names other axes'
  material. An axis folder stays single-axis.
- Each reading must list its **drivers**: the FRDs that moved the allocation, by id. The harness
  checks every id against the registry, attaches the source file and home axis, and for the
  combined reading lists the drivers that came from other axes (`other_axis_drivers`). An id that
  is not in the registry is reported and ignored.
- A single-axis run has no combined reading (it would be the same set). A single-database run
  (`axes.separate_databases: false`) has only the whole-set reading.

## 3. Partition rule

1. Sort the FRDs by id.
2. Pack them in that order into partitions of at most `frd_assess.partition_words` registry words
   (default 30,000). The partitions therefore do not depend on the order the records arrive in.
3. One partition: its vector is the result.
4. Several partitions: each is assessed alone; then one more ACH_Eval call receives only the
   partition fragments (allocation, drivers, objection, reversal finding, start of the commentary)
   and returns the result. It sees no evidence the partitions did not see.
5. Cross-check, always recorded: the mean of the partition vectors, weighted by FRD count and
   rounded to the gauge by largest remainder (ties to the hypothesis listed first). The record
   holds that mean, the largest difference between it and the result, and the largest difference
   between partitions.
6. If the result differs from the mechanical mean by more than an eighth of the gauge (8 units of
   64), `cr verify` and the page carry a warning: the conclusion depends on where the set was cut.

## 4. Final score

No blended score is chosen. The page prints, per axis, the axis-only vector, the combined vector
and an equal-weight row marked "comparison only". How much the combined set should count is the
researcher's decision, to be made after seeing real output; when it is made it is recorded in
`docs/DECISIONS-2026-11-11.md` (or its successor) and implemented as `frd_assess.final_rule`.

## 5. Outputs

- `FRD-EVALUATION.md` at the run root: the table per axis, drivers with FRD id and source file,
  other-axis drivers, partition notes, measured time, calls and cost, and the continue command.
- `frd-evaluation.json` at the run root: the same as data.
- `AXIS-<id>/axis.db`: a SQLite file with tables `questions`, `responses`, `candidate_frds`,
  `validations`, `validated_frds`, `retained_frds`. Each row has key columns plus the whole record
  as `record_json`. It is generated from the JSON files, which remain the source of record;
  `cr verify` warns when the two are out of step.
- **Provisional banner.** The page counts each axis's questions by `axis_source`. If any question
  was filed under its axis after the fact, the page says the axis-only vectors are provisional.
- Every file says "preliminary, evidence-level". The witness-level `assess` stage is still the
  final assessment and is not replaced.

## 6. The researcher's stop

- `pipeline.stop_after` (default `"frd_assess"`; `""` never halts). After that stage is done a
  plain `cr run` halts with status `halted`; `RUN-STATUS.md` says "Halted for researcher decision"
  and gives the command.
- `cr run <project> --run <id> --continue` writes
  `00_RUN-CONTROL/model-and-human-decisions/released-after-frd_assess.json` and runs the later
  stages. Nothing already done is recomputed, on the halt or on the release.
- An explicit `--from` or `--only` is itself a decision and is not halted.
- `frd_assess` is read-only for the pipeline: running or re-running it does not mark later stages
  stale. To redo it: `cr run <project> --run <id> --only frd_assess --force frd_assess`.
- The model is the role `frd_assessor`, which follows `assessor` unless routed.
- `cr demo` sets `stop_after` to `""` so the demonstration shows every stage.
