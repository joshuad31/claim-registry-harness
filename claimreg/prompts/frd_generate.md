<!-- prompt: frd_generate | adapted from 08_FRD_Generation_Prompt_Generator_Template_v3.1 embedded template + Problems-note output limits -->
## SYSTEM
# FRD GENERATION INSTRUCTIONS

The quest is complete. Extract candidate claims about {{SUBJECT}} from the supplied Archivist query-response file for later source validation. Responses are discovery material, not evidence.

Process this one query-response file only. Harvest its relevant claims. One FRD states one claim and carries exactly one producing QID (the QID of this file). Never combine material from different response files into one FRD. If the QID is missing, report it; do not invent one.

Anchor each FRD to one source wherever the response permits. Split separately attributed clauses into individual claims. When the response explicitly attributes the same claim separately to multiple sources, create one candidate FRD per source. When a passage cites multiple sources without revealing which supports which clause, record one FRD naming every candidate source and set status to "disambiguate". Do not guess an attribution, and do not drop a claim because its attribution is unresolved. Record exact cited parts; file boundaries alone do not establish independent evidence. Preserve the actual speaker.

Preserve the actual speaker, qualifications, conditions, numbers, adverse findings, nulls, and limitations. Separate a source's own findings from its reports of other authorities. Do not turn response synthesis into source testimony or invent filenames and locators.

## Labels and categories

The Archivist used these evidence labels:
{{LABELS}}

Source-attributed findings and interpretations are candidates. An analyst extrapolation ([INFERRED] or equivalent) is not itself a source claim; extract its individually sourced premises where available. Retrieval gaps ([NO SOURCE] or equivalent) belong in the harvest review, never in an FRD; they do not establish corpus-wide absence. Retain the response's label as provisional metadata. Do not discard a source-attributed claim merely because its label appears wrong; flag it for validation.

## Selectivity (compression is the purpose)

Every proper response produces FOUR OR FEWER FRDs. A response naming two sources usually yields two or three good FRDs; a response naming one source usually yields one or two. Choose the claims that carry the most decision-relevant, source-attributed content (findings with their numbers, designs, denominators, comparators, adverse or null results, and limitations). Fold closely related details from the same source passage into one FRD claim rather than splitting them into many small FRDs. Record what you did not extract, and why, in the harvest review.

## Entry fields

- cluster: a neutral topic cluster name (e.g. "exposure-pharmacokinetics", "bladder-function-animal", "clinical-trial-outcomes")
- label: a short label
- source_files: exact source filename(s) as cited in the response
- locator: heading, table, or best search terms
- claim: one or two sentences stating one source-attributed proposition without strengthening it
- verification_instruction: what passage, number, attribution, or qualification to check; include the original evidence label and any suspected labeling error
- evidence_label: the response's label for this claim
- provenance: OWN_RESULT, DERIVED_FROM(<ancestor>), or DERIVATIVE_UNKNOWN (provisional, from the response)
- status: ordinary | disambiguate | needs-source
- speaker: who makes the claim (the source authors, a cited authority, a review)

## USER
QUERY-RESPONSE FILE: {{ORIGIN_REF}}
PRODUCING QID: {{QID}}
SOURCES NAMED IN THE QUESTION: {{NAMED_SOURCES}}

QUESTION:
{{QUESTION}}

ARCHIVIST RESPONSE:
{{RESPONSE}}

Return ONLY a JSON object:
{
  "qid": "{{QID}}",
  "frds": [ {"cluster": "", "label": "", "source_files": [""], "locator": "", "claim": "", "verification_instruction": "", "evidence_label": "", "provenance": "", "status": "ordinary", "speaker": ""} ],
  "harvest_review": {
    "sources_cited_in_response": [""],
    "cited_sources_without_frd": [{"source": "", "why": ""}],
    "not_extracted": [{"content": "", "why": ""}],
    "unresolved_citations_or_labels": [""],
    "gaps_and_unsupported_synthesis": [""]
  }
}
