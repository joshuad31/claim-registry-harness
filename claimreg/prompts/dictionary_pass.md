<!-- prompt: dictionary_pass | Superior Mr. Dictionary v5.1 (verbatim, spec 14), run unattended -->
## SYSTEM
{{> spec/Superior_Mr_Dictionary_v5.1.md}}

HARNESS NOTES (unattended run): No one is available to answer interview questions. Take the goal from the trusted fragment, mark it INFERRED, and continue (section 1). Do not ask questions; emit the artifact. This is pass {{PASS}} of at most {{MAX_PASSES}}; if this is the last allowed pass, emit the ACH Custom Dictionary (the compiled current state) - the analyst has declared that the last pass is good enough (section 11).

## USER
GOAL (INFERRED from the frozen frame): {{GOAL}}

HYPOTHESES (verbatim):
{{HYPOTHESES}}

TRUSTED FRAGMENT:
<<<FRAGMENT
{{TRUSTED_FRAGMENT}}
FRAGMENT>>>

PRIOR MR. DICTIONARY FRAGMENT (base for this pass, or "none"):
<<<PRIOR
{{PRIOR}}
PRIOR>>>

VALIDATED FRDS (claim text and verbatim source text; tier VFRD; source sentences quoted in source_text count as primary with the source's index rank):
{{FRDS}}

INDEX RANKS:
{{RANKS}}
