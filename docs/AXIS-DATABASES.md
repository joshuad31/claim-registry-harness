# Axis databases: one evidence database per axis

*Specification, 2026-11-11. Amends the workspace standard (spec 10, section 4, "Canonical run tree").
Implemented in `claimreg/runctx.py`, `claimreg/axes.py` and `claimreg/pipeline.py`.*

A header may ask several questions at once. Each is an **axis** (`A1`, `A2`, ...), with its own
rival hypotheses. From now on every axis has its own evidence database, and no file holds material
of two axes.

## 1. The rules

1. **A question belongs to exactly one axis.** Whoever writes the question (the Investigator, or the
   Manager when it writes ready questions) chooses the axis and states it. A question that does not
   name exactly one axis is refused and logged. Questions are never shared between axes.
2. **A record inherits its axis.** What descends from a question takes the question's axis: the
   query response, the FRD candidates made from it, their validations, the validated and retained
   FRDs, the witnesses, their audits and transcodings. What descends from a hypothesis takes the
   hypothesis's axis: coverage units, match records, joint groups, coverage sets, the premise
   ledger, crux candidates, the assessment and the reports.
3. **A record that joins two axes is a SHARED record.** It lives in the `SHARED` database and in no
   axis's. There are two kinds:
   - the Manager's quest state, assessment checkpoints, feedback packets and closeout (one quest
     serves every axis);
   - relations between one axis's witnesses and another axis's units (evidence found while asking
     about one axis that bears on another);
   - the custom dictionary and the canonicalizer rulebook. They are shared resources by definition:
     the reason for separate databases is that someone can run ACH_Eval on one axis alone, and
     nobody runs ACH_Eval on a dictionary. One vocabulary serves every axis;
   - the matcher qualification (the matcher is tested once on adversarial fixtures, for every axis).

   Shared resources are never individualized (spec 10, section 6.4, rule 7). `RUN-CONFIG.json` lists
   them under `shared_resources`; `cr verify` fails if one is missing or if an axis folder holds a copy.
4. **No file under an axis folder holds another axis's material.** The test suite checks this: no
   file in `AXIS-A1...` may even name an `A2` hypothesis.
5. **Run-level files are not evidence.** Run control (log, model-call log, artifact registry, stage
   state) and the frozen frame inputs (the approved header, the source index, the Archivist prompt)
   belong to the run. The header is one human-approved document and is not split.

## 2. The run tree

```text
02_RUNS/<run>/
  RUN-MAP.md                      start here: lists every database with links
  RUN-STATUS.md                   one line per stage, one sub-line per axis
  RUN-CONFIG.json                 "layout": "axis-databases-v1"
  00_RUN-CONTROL/                 log, model calls, artifact registry, stage state
  01_FRAME/                       header.md, index.md, archivist-custom-prompt.txt, frame.json
  AXIS-A1__<label>/               everything for axis A1, and nothing else
    AXIS.md                       what this axis asks, where each thing is, how many records
    01_FRAME/coverage-units.json
    02_DISCOVERY/01_issued-questions/   questions.json + one .md per question
    02_DISCOVERY/02_query-responses/    responses.json, attempts.json + one .md per answer
    03_FRDS/                      candidates, harvest, validations, validated, retained
    05_WITNESSES/                 applications, versions, audits, held, released
    06_TRANSCODING/
    07_MATCHING/                  this axis's units; this axis's witnesses against them
    08_COVERAGE/                  coverage.json, premise-ledger.json, PREMISE-LEDGER.md
    09_CRUX/
    10_REPORTS/                   CRUX-REPORT.md, EVIDENCE-PACKETS.md, report.html, assessment
  AXIS-A2__<label>/               the same tree for axis A2
  SHARED/                         records that belong to more than one axis
    README.md
    02_DISCOVERY/                 03_quest-state, 04_ach-eval-checkpoints, 05_feedback, 06_closeout
    04_LANGUAGE-TOOLS/            the one dictionary and canonicalizer rulebook every axis uses
    07_MATCHING/02_match-fixtures/    the one matcher qualification
    MEMBERSHIP.jsonl              every record that belongs to more than one axis: kind, id, home_axis, axes
    CROSS-AXIS-into-A1/07_MATCHING/   the other axes' witnesses against A1's units
    CROSS-AXIS-into-A1/EVIDENCE/      read-only copies of those witnesses, their FRDs, questions and answers
    CROSS-AXIS-into-A2/...
```

The folder label comes from the axis heading in the header ("### Axis two — bedtime dosing" gives
`AXIS-A2__bedtime-dosing`). `axes.labels` in `project.json` overrides it, for example
`{"A1": "antidepressant-gap"}`.

Every record also carries its axis as a field (`"axis": "A2"` on questions and answers; units and
relations carry `axis_id`). Identifiers are unchanged (`Q0001`, `FRD-Q0001-01`, `W-...`).

## 3. How a question gets its axis

| Source, best first | Recorded as `axis_source` |
|---|---|
| The Investigator states it: `{"axis": "A2", ...}` | `investigator` |
| A Manager ready question carries it: `1. [axis: A2] [target: ...] question` | `investigator` |
| Its target names exactly one axis ("A2 trial results") | `target-label` |
| The header has one axis | `single-axis header` |
| **Old quests only:** a model reads the question against the axes | `assigned-after-the-fact (model)` |
| **Old quests only, no model:** shared wording | `assigned-after-the-fact (wording)` |

In a live quest (`cr quest`) only the first three exist: a question without a single axis is
refused and written to `rejected.jsonl` with the reason. The last two rows exist so a quest that was
run before this rule can still be filed; `AXIS.md` says how many questions were filed that way.

The notebook never sees the axis. The queue file that reaches the notebook page holds the question
text and nothing else.

## 4. The quest folder

```text
quest/<id>/
  AXIS-A1/asked.jsonl             the questions asked for A1 (and rejected.jsonl, if any)
  AXIS-A2/asked.jsonl
  rejected.jsonl                  questions refused for naming no single axis
  answers/                        the driver's inbox: one raw capture per answer (each single-axis)
  manager-workspace/answers/AXIS-A1/   each answer as Markdown, under its question's axis
  manager-workspace/packets/, private/   the Manager's cross-axis records (SHARED by nature)
  relay-status.json               includes "by_axis": asked / usable / graded
```

The Manager still assesses every axis in one state document: one Manager coordinates the quest.
Those documents are SHARED records and are imported into `SHARED/02_DISCOVERY/`.

## 5. How the pipeline runs

The `language` stage runs once for the whole run: it builds one dictionary and one rulebook from
every axis's validated FRDs and stores them in `SHARED/04_LANGUAGE-TOOLS/`; each axis's transcoding
reads them from there. The other stages from `units` to `report` run once per axis. Each run sees a frame that contains only
that axis and reads and writes only inside that axis's folder, so the stage code itself never
mentions axes. The `quest` stage runs once for the whole run; when it ends, every question and
answer is filed into its axis and removed from the shared working area.

After each axis has matched its own witnesses to its own units, a **cross-axis pass** asks, for
each axis, whether the other axes' witnesses bear on its units. The results are written to
`SHARED/CROSS-AXIS-into-<axis>/`. The later stages of an axis (joint groups, coverage, premise
ledger, crux, assessment, report) read their own records plus the shared relations that bear on
their units; a witness that comes from another axis is labelled with its `home_axis`. Set
`axes.cross_axis_evidence` to `false` to make every axis fully independent.

**Assessing one axis alone.** The complete evidence for axis `A2` is `AXIS-A2__.../` plus
`SHARED/CROSS-AXIS-into-A2/`. The second folder holds the relations and, under `EVIDENCE/`, a
read-only copy of every other-axis witness that bears on A2's units with its FRD, question and
answer, each labelled `home_axis`. The canonical record stays in its home axis (one canonical home).
The harness's own assessment and report stages read both. What neither folder contains: other-axis
witnesses that were never judged against A2's units (outside the matcher's shortlist), and those
judged to have no relation. `SHARED/CROSS-AXIS-into-A2/07_MATCHING/03_match-records/summary.json`
gives the number of pairs judged and not judged.

**No unassigned bucket.** Every question names one axis and every later record inherits it, so no
record is left without an axis. A witness that relates to no unit stays in its question's axis. A
question refused for naming no single axis was never asked; it is in the quest folder's
`rejected.jsonl`. `cr verify` prints the per-axis counts, checks that they add up to the quest's
questions, that no record is in two axes, and that every record sits in its question's axis.

Consequences worth knowing:

- Retention budgets and reports are per axis. The dictionary and rulebook are not.
- Matching compares far fewer pairs per axis than a whole-run match, so more of them are judged.
- A source asked about for one axis does not count for another unless the cross-axis pass finds
  that its witness bears on that axis's units.

## 6. Reading a run

- People: open `RUN-MAP.md`, then the axis's `AXIS.md`.
- Tools: `ctx.for_axis("A2")` gives one axis's database; `ctx.scopes()` gives them all.
  `ctx.load(...)` on the run itself is a read-only whole-run view used by `cr verify` and
  `cr status`; nothing is stored that way.
- `cr funnel` prints one funnel per axis. `cr verify` checks every axis.

## 7. Old runs

A run made before this specification has no `"layout"` in `RUN-CONFIG.json` and keeps the single
database it was made with; every command still reads it. To put an old quest into axis databases,
import it into a new run (`cr import-quest <project> <quest folder> --run <new id>`, then
`cr run`). Model calls already made are reused from the cache where the request is unchanged. Set
`axes.separate_databases` to `false` to make new runs in the old layout.

See also `docs/FRD-EVALUATION.md`: the preliminary evaluation of each axis's validated FRDs, the combined set in
`SHARED/03_FRDS-COMBINED/`, the `axis.db` file in each axis folder, and the researcher's stop.
