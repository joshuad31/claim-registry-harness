# Queue operator notes (PTX demonstration run)

Who answered: Claude Opus 5.5, one fresh agent context per batch file, each instructed to read only its batch
file (prompt quoted in docs/AGENT-OPERATOR.md). Pass A / pass B and constructor / auditor batches always went to
different contexts.

## Incidents

* 2026-10-29 ~10:22 (separate smoke-test project, since removed): the single Investigator request of a live
  quest round was not answered; the operator context was stopped by a safety classifier. The request was not
  re-attempted and the smoke test was abandoned. The PTX run uses the imported discovery record instead.
* 2026-10-29 ~11:00 BATCH-0011-witness_auditor (16 audit requests): the operator context was stopped by a
  safety classifier before writing any answer. The batch was not re-attempted; its 16 requests were marked
  skipped (`cr queue skip`), so those 16 witnesses are HELD as "not audited" and never enter matching.
* 2026-10-29 ~11:13 BATCH-0008 / BATCH-0010 (witness audits): two contexts running in parallel saved helper
  scripts under the same file name in a shared scratch folder, so the BATCH-0008 context once executed the
  BATCH-0010 context's script (which rewrote BATCH-0010's own answers, unchanged). Checked afterwards: each
  response file holds exactly its own batch's keys, and its verdict counts match the report of the context
  that owned that batch (0008: 19 PASS; 0009: 17 PASS, 2 REVISE_WITNESS; 0010: 18 PASS, 1 REVISE_WITNESS).
  From then on operator contexts were told to run Python inline and never save shared script files.
* BATCH-0009 was first returned with 16 of 19 answers; the same context was asked for the 3 missing keys.
* 2026-10-29 ~11:50 BATCH-0026-matcher_b, BATCH-0014-matcher_a, BATCH-0017-matcher_a, BATCH-0018-matcher_a, BATCH-0019-matcher_a and BATCH-0020-matcher_a (14 matching requests each): the operator
  contexts were stopped by a safety classifier before writing any answer. Neither batch was re-attempted; their
  requests were marked skipped. A witness-unit pair judged by only one pass is recorded as ONE_PASS_ONLY: it
  counts as ABSTAIN for coverage, is not sent to the model adjudicator, and is listed in the matching review
  packet for a human to confirm. Pairs with no judgment from either pass are recorded as MISSING.
* Several contexts (e.g. BATCH-0004, BATCH-0015, BATCH-0027) reported that one early turn was interrupted by a
  safety classifier, for example while echoing batch content in prose, and that they then completed the task by
  writing the answers directly with Python, without reproducing source passages. Those answers were accepted:
  the completed answers themselves were not stopped.
* BATCH-0031-match_adjudicator (13 adjudication requests): stopped by a safety classifier before any answer;
  skipped, not re-attempted. Those disputed pairs stay DISPUTED (ABSTAIN).
* BATCH-0033-joint_checker (the independent verification of the 2 proposed joint groups): stopped by a safety
  classifier before any answer; skipped, not re-attempted. Unverified groups are not approved, so they create no
  coverage option.
* Report summary: the first summary request (f9409d20105f2fe4f8c71337) was answered, but its prompt contained
  the report's generation time, so each rerun asked a new question. The harness was fixed to leave the time out of
  the summary input; the request was asked once more (BATCH-0040) and that answer is the one used. The first answer
  stays in done/ for the record but is not used.
* Totals for this run's queue: 511 requests (396 answered, 115 skipped). 18 requests that a harness fix made
  obsolete before anyone answered them (17 witness revisions triggered by a false-positive number check, 1 report
  summary) were deleted from pending/ and never answered.
