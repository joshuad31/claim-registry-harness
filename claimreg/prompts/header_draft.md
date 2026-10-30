<!-- prompt: header_draft | Quest Header generator and template v2 (verbatim, spec 03). Produces a DRAFT for human approval. -->
## SYSTEM
{{> spec/Quest_Header_Generator_v2.md}}

## USER
INVESTIGATION QUESTION, SCOPE AND HUMAN-APPROVED HYPOTHESES:
<<<FRAME
{{FRAME}}
FRAME>>>

RANKED INDEX / MANIFEST SUMMARY:
<<<INDEX
{{INDEX}}
INDEX>>>

ACTUAL ARCHIVIST CUSTOM PROMPT:
<<<ARCHIVIST
{{ARCHIVIST}}
ARCHIVIST>>>

DEPLOYMENT AND ASSESSMENT SETTINGS:
run id: {{RUN_ID}}; Archivist: local retrieval database driven by the Claim Registry harness (the harness carries each query and saves exact captures); assessment prompt: ACH_Eval_NLM_Super; evidence contract: notebooklm_only; gauge G = {{GAUGE}}; enabled axes: {{AXES}}; output locations: managed by the harness.

Return the complete Investigator header (title and sections 1-8), then a line containing only "=====COORDINATOR=====", then the Part III Coordinator handoff.
