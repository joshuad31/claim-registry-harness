# 04_LANGUAGE-TOOLS

## Purpose
Custom dictionary and canonicalizer rulebook (when language.mode = labels).

## Allowed inputs
Validated FRDs, the trusted ACH_Eval fragment, the index ranks.

## Expected outputs
dictionary-entries.json, rulebook.md, LANGUAGE-STATUS.json

## Current status
language: done

## How to verify this stage
Inspect LANGUAGE-STATUS.json for the mode and sources of each tool.

## Next handoff
Transcoding (06).

## What this stage does not establish
Conformance is compliance with language rules, not truth.
