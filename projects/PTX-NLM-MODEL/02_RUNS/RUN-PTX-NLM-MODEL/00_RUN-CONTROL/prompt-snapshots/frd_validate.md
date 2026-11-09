<!-- prompt: frd_validate | adapted from 09_FRD_Validation_Prompt_Generator_Template_v3.1 embedded template; blind (no frame) -->
## SYSTEM
# FRD VALIDATION INSTRUCTIONS

Check the FRD against only its named source text supplied below. Exclude query responses, summaries, indexes, and outside knowledge. You have no access to, and must not speculate about, any research question, hypothesis or intended conclusion.

Check every clause, attribution, qualification, and locator. Transmitted claims establish only the transmitter's report. Never recruit an unnamed source to rescue failure.

For a "disambiguate" FRD, check each named candidate separately and record its result. Produce one repaired FRD per supported claim per source; retain unresolved attribution as NOT READY. One source may span named parts of the same work; preserve exact locations and speaker.

## Labels

Evidence labels used in this project:
{{LABELS}}
Check the provisional label against the source; correct a mistaken label in the verdict explanation. Retrieval gaps cannot prove absence. Separate analyst inference from source statements.

## Output for the FRD

1. citation - reference, exact source filename, and location(s); note missing metadata.
2. claim - corrected, supported wording; otherwise state that support is unestablished.
3. source_text - EXACT supporting or contradicting text copied character-for-character from the source (whole sentences or paragraphs where needed; table rows with their labels and units). Several passages may be joined with " ... ". Never paraphrase, silently repair, or reconstruct a quotation: this text is mechanically checked against the source file.
4. verdict - RIGHT / MOSTLY RIGHT / PARTLY RIGHT / WRONG / NOT FOUND / SOURCE UNAVAILABLE, with a brief explanation. Evaluate the ORIGINAL candidate; preserve its wording when changed and explain material repairs.
5. provenance - OWN_RESULT / DERIVED_FROM(ancestor) / DERIVATIVE_UNKNOWN, as confirmed or corrected against the source.

## Deliverable

Produce a repaired, source-supported FRD. Correct known defects in claim, citation, attribution, scope, labels, and provenance. Mark READY FOR WITNESS CONSTRUCTION only when claim and evidence support faithful compression without unresolved material defects. Otherwise mark NOT READY FOR WITNESS CONSTRUCTION; it is retained for audit. Readiness evaluates the repaired FRD independently of the verdict.

If the locator fails, search the whole supplied text using wording variants before NOT FOUND. Repair mistaken locators. Use SOURCE UNAVAILABLE when the source text is missing; if only excerpts of a long source were supplied and the passage is not among them, say so rather than issuing a blanket NOT FOUND. Split compound claims as needed (children); children retain the parent's origin and QID. Each output contains its own evidence and explanation.

## USER
FRD ID: {{FRD_ID}}    ORIGIN REF: {{ORIGIN_REF}}    PRODUCING QID: {{QID}}
CANDIDATE SOURCE(S): {{SOURCE_FILES}}
LOCATOR: {{LOCATOR}}
PROVISIONAL LABEL: {{LABEL}}    PROVISIONAL PROVENANCE: {{PROVENANCE}}    STATUS: {{STATUS}}
CANDIDATE CLAIM:
{{CLAIM}}
VERIFICATION INSTRUCTION:
{{VERIFICATION}}

NAMED SOURCE TEXT ({{SOURCE_NOTE}}):
<<<SOURCE
{{SOURCE_TEXT}}
SOURCE>>>

Return ONLY a JSON object:
{
  "frd_id": "{{FRD_ID}}",
  "citation": {"filename": "", "locator": ""},
  "claim": "",
  "source_text": "",
  "verdict": "RIGHT | MOSTLY RIGHT | PARTLY RIGHT | WRONG | NOT FOUND | SOURCE UNAVAILABLE",
  "verdict_explanation": "",
  "evidence_label": "",
  "provenance": "",
  "readiness": "READY FOR WITNESS CONSTRUCTION | NOT READY FOR WITNESS CONSTRUCTION",
  "readiness_reason": "",
  "children": [ {"claim": "", "source_text": "", "citation": {"filename": "", "locator": ""}, "evidence_label": "", "provenance": "", "readiness": "", "readiness_reason": ""} ]
}
Use an empty list for "children" unless you split the claim.
