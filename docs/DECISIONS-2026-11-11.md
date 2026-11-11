# Decisions, 2026-11-11: one evidence database per axis

Full specification: [AXIS-DATABASES.md](AXIS-DATABASES.md).

**Requirement (Joshua Davis).** Every axis needs its own database for questions, query responses,
FRDs, validated FRDs, witnesses and everything after. No file may hold several axes. Items that
belong to more than one axis may go in a shared database. Questions are never multi-axis: the
Investigator chooses one axis for each question on purpose.

## 1. Partition by running each stage per axis, not by splitting files afterwards

Each stage from `units` to `report` runs once per axis with an axis-scoped context
(`AxisContext`): the frame it sees contains only that axis and every path resolves inside that
axis's folder. Stage code is unchanged. **Why:** splitting combined files after the fact would
leave reports, ledgers and audit pages that still mix axes; running per axis makes every artifact,
documents included, single-axis by construction. **Risk:** an axis no longer sees the other axes'
evidence unless the cross-axis pass finds it (decision 3).

## 2. One axis per question, enforced where questions are written

The relay refuses a question that does not name exactly one axis. The Investigator prompt and the
Manager's packet format now ask for the axis. **Why:** the axis of every later record follows from
its question, so this one rule decides where everything is filed. **Risk:** a model that omits the
axis loses that question; the refusal is logged with its reason and the Investigator writes more.

## 3. Cross-axis evidence is kept, as SHARED records

After own-axis matching, each axis's units are matched against the other axes' witnesses and the
relations are stored in `SHARED/CROSS-AXIS-into-<axis>/`. Later stages of the axis read them, with
each foreign witness labelled by its home axis. **Why:** a finding gathered for one axis often bears
on another (for example absorption interference for both timing and formulation), and dropping it
would weaken coverage for no reason. **Risk:** extra matching calls; `axes.cross_axis_evidence:
false` turns the pass off.

## 4. The Manager's state stays one document, filed as SHARED

One Manager coordinates the quest across axes, so its state, checkpoints and packets cover all of
them. They are SHARED records. **Not done:** one Manager state per axis. That would need one
assessment call per axis per round and would change the quest's throughput; it can be added if the
shared state proves hard to audit.

## 4a. The dictionary and canonicalizer are SHARED (corrected the same day)

The first version ran the language stage per axis. Joshua Davis corrected this: the databases are
separated so that ACH_Eval can be run on one axis alone, and nobody runs ACH_Eval on a dictionary or
a canonicalizer, so they must be shared resources. The stage now runs once, reads every axis's
validated FRDs, and writes to `SHARED/04_LANGUAGE-TOOLS/`.

## 4b. Review points from DeepSeek, same day

- **Matcher qualification is shared too** (accepted). It ran per axis; it now runs once into
  `SHARED/07_MATCHING/02_match-fixtures/`. `RUN-CONFIG.json` declares `shared_resources` and
  `cr verify` checks each exists once with no copy in an axis folder.
- **Cross-axis witnesses are staged as records, not only relations** (accepted, placed in SHARED, not
  in the consuming axis): `SHARED/CROSS-AXIS-into-<axis>/EVIDENCE/`. Putting copies inside the axis
  folder would break "no file in an axis folder holds another axis's material".
- **Membership list** (accepted): `SHARED/MEMBERSHIP.jsonl`.
- **Reconciliation** (accepted as a check in `cr verify`); **unassigned bucket** (rejected: under the
  one-axis-per-question rule nothing is unassigned).
- **Post-hoc backfill of old runs without model calls** (not built): filing an old run by axis is done
  by importing its quest into a new run. A backfill that only splits files would leave coverage,
  crux and reports computed across axes.

## 5. Old quests are filed after the fact, and say so

Questions asked before this rule carry no axis. On import a model reads each against the axes (or,
with no model, shared wording decides), and the question is marked `assigned-after-the-fact`.
**Why:** the alternative is to discard completed quests. **Risk:** a question that served two
axes is filed under one; the cross-axis pass recovers its evidence for the other.

## 6. Layout marker and compatibility

New runs record `"layout": "axis-databases-v1"`. Runs without the marker keep the single-database
layout and are read as before; `axes.separate_databases: false` makes new runs that way. Legacy
ChatGPT imports stay single-database because they record no axis.

## Tests

`tests/test_axes.py` (10 tests): two-axis pipeline end to end; no file in an axis folder names the
other axis's hypotheses; no question in two databases; cross-axis relations are SHARED and reach the
axis they bear on; the pass can be turned off; an axis nobody asked about still gets an empty
database; the relay refuses questions with no single axis and files the rest per axis; import keeps
the Investigator's axis; the old layout still works. Suite: 119 tests.

## 5. Evaluate the validated FRDs before building the machinery

Josh's order of work puts an evaluation after the validated FRDs and before the dictionary,
canonicalizer, transcoding, witnesses and matching. DeepSeek's review found the harness had no such
step. Decisions:

- Stage `frd_assess` runs after `frd_retain`; the run then halts until `cr run --continue`.
- Per axis, two readings: that axis's FRDs only, and the combined set (a disjoint union).
- Partition aggregation: one ACH_Eval call over the partition fragments, with the count-weighted
  mechanical mean recorded beside it and a warning above an eighth of the gauge.
- Final score: none chosen yet. Both vectors are reported, with an equal-weight row for comparison
  only. Open decision, Josh's.
- Each axis gets `axis.db` (SQLite), generated from the JSON records.
- Spec 10 and the `10a` amendment stay separate while the design is moving; they link to each other.

Details: `docs/FRD-EVALUATION.md`. Suite: 129 tests.
