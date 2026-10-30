# 03_FRDS

## Purpose
Candidate FRDs, blind validation, retained validated FRDs.

## Allowed inputs
Usable query-response records (generation); one FRD + its named source only (validation).

## Expected outputs
candidates.json, harvest.json, validations.json, validated-frds.json, retained-frds.json, retention.json

## Current status
frd_generate: imported; frd_validate: imported; frd_retain: done

## How to verify this stage
Each validated FRD's source_text was searched for in the named source file (quote_check).

## Next handoff
Witness construction (05).

## What this stage does not establish
Faithful representation of a source is not the truth of that source.
