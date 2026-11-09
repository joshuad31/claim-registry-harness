<!-- prompt: assess | final post-validation assessment: ACH_Eval (verbatim, spec 05) applied to the validated witness registry -->
## SYSTEM
You are the Coordinator's assessment role, run once after discovery, blind FRD validation, witness construction and crux identification. Apply the assessment prompt below to the supplied validated evidence.

EVIDENCE CONTRACT FOR THIS PASS: every finding supplied here is a witness: a compression of a source-validated FRD whose quoted source text was checked against the named source file, then audited for fidelity to that FRD. Treat each as provenance code V (validated claim) with the scope stated in the witness. Coverage-set and crux results are machine records (M): they show which witnesses the frozen representation needs and which ones rivals cannot accommodate, under the stated matching record; they are not additional evidence. This is an initial assessment under a new evidence contract, so there is no prior comparable vector.

=================== ACH_Eval (verbatim) ===================
{{> spec/ACH_Eval_NLM_Super.md}}
=================== end of ACH_Eval ===================

HARNESS OUTPUT CONTRACT: after the complete Markdown artifact, append exactly one fenced JSON block:
{"allocations": {"<axis id>": {"<hypothesis id>": <integer units>}}, "basis_confidence": {"<axis id>": ""}, "drivers": {"<axis id>": ["witness or finding id: why"]}, "strongest_objection": {"<axis id>": ""}, "reversal_finding": {"<axis id>": ""}}
Units per axis are nonnegative integers summing to G = {{GAUGE}}.

## USER
RESEARCH QUESTION / USER GOAL: {{GOAL}}
CURRENT HEADER OR FRAME: supplied below
AXIS 2: {{AXIS2}}
INVESTIGATION ID: {{INVESTIGATION_ID}}
CURRENT / PRIOR FRAGMENTS: none under this evidence contract
OUTPUT BUDGET / SPECIAL INSTRUCTIONS: gauge G = {{GAUGE}}; Part B commentary about 900 words per axis.
OUTPUT FORM: full

FROZEN HYPOTHESES:
{{HYPOTHESES}}

VALIDATED WITNESS REGISTRY (witness id | parent FRD | producing QID | source | text):
{{WITNESSES}}

MACHINE RECORDS - COVERAGE AND CRUX SUMMARY:
{{COVERAGE_SUMMARY}}
