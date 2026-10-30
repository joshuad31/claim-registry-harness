# 01_FRAME

## Purpose
Frozen frame: header, hypotheses, ranked index, Archivist instructions, coverage units.

## Allowed inputs
The human-approved header and index; the corpus manifest.

## Expected outputs
frame.json, header.md, index.md, archivist-custom-prompt.txt, coverage-units.json

## Current status
corpus: done; index: done; archivist_prompt: done; frame: done

## How to verify this stage
Compare header.md's sha256 with RUN-CONFIG.json; every unit's source_quote is checked verbatim.

## Next handoff
Discovery (02) and matching (07) read this frame.

## What this stage does not establish
It does not establish that the hypotheses are complete, fair, or true.
