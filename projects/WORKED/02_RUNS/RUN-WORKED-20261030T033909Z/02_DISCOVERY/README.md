# 02_DISCOVERY

## Purpose
Coordinator-led quest: issued questions, exact Archivist answers, ACH_Eval checkpoints, feedback packets, closeout.

## Allowed inputs
Frozen header and index (Investigator, Coordinator); corpus passages (Archivist only).

## Expected outputs
01_issued-questions, 02_query-responses, 03_quest-state, 04_ach-eval-checkpoints, 05_feedback, 06_closeout

## Current status
quest: done

## How to verify this stage
Every question has one QID and 1-3 named sources; every answer is stored verbatim with the passages the Archivist saw.

## Next handoff
FRD generation (03) processes one usable answer at a time.

## What this stage does not establish
Answers are discovery material, not evidence; allocations are uncalibrated judgments.
