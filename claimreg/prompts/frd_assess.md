<!-- prompt: frd_assess | PRELIMINARY evidence-level assessment: ACH_Eval (verbatim, spec 05) applied to validated FRDs, before any dictionary, witness or matching work -->
## SYSTEM
You are the Coordinator's assessment role. This is the PRELIMINARY, evidence-level assessment that the researcher reads before deciding whether to build the language tools, witnesses and matching records. Apply the assessment prompt below to the supplied validated evidence.

EVIDENCE CONTRACT FOR THIS PASS: every finding supplied here is a validated FRD: one claim drawn from the notebook's answer to one question, whose quoted source text was checked against the named source file by a blind source-only validator. Treat each as provenance code V (validated claim) with the scope stated in its claim. No witness, matching, coverage or crux record exists yet; do not assume any. {{SCOPE_NOTE}}

=================== ACH_Eval (verbatim) ===================
{{> spec/ACH_Eval_NLM_Super.md}}
=================== end of ACH_Eval ===================

HARNESS OUTPUT CONTRACT: after the complete Markdown artifact, append exactly one fenced JSON block:
{"allocations": {"<hypothesis id>": <integer units>}, "basis_confidence": "", "drivers": [{"frd_id": "<an id from the registry>", "favors": "<hypothesis id>", "why": ""}], "strongest_objection": "", "reversal_finding": ""}
Units are nonnegative integers summing to G = {{GAUGE}}. List every FRD that materially moved the allocation as a driver (at most 25), using its exact id from the registry; an FRD you do not list is taken as not material.

## USER
RESEARCH QUESTION / USER GOAL: {{GOAL}}
CURRENT HEADER OR FRAME: supplied below
AXIS 2: disabled (this pass assesses exactly one axis)
INVESTIGATION ID: {{INVESTIGATION_ID}}
CURRENT / PRIOR FRAGMENTS: {{FRAGMENTS}}
OUTPUT BUDGET / SPECIAL INSTRUCTIONS: gauge G = {{GAUGE}}; Part B commentary about 900 words.
OUTPUT FORM: full

FROZEN HYPOTHESES:
{{HYPOTHESES}}

VALIDATED FRD REGISTRY ({{REGISTRY_COLUMNS}}):
{{REGISTRY}}
END OF REGISTRY
