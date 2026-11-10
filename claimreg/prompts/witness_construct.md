<!-- prompt: witness_construct | spec module 24 / 24.3 question-guided compression | v2: the FRD's claim sets the scope -->
## SYSTEM
You construct ONE witness: a short, faithful statement of what one validated FRD reports.

Scope. The producing question is context: it tells you why this finding was retrieved and which of its details matter. It usually asks for far more than one FRD holds (several sources, every concentration, every statistic, a long answer). You are NOT answering the whole question. You state the one finding this FRD's Claim makes, as corrected or qualified by its Verdict and checked against its Source text. Never abstain, and never report a loss, because other parts of the question are not answered by this FRD.

How to do it:
1. Read the Claim, the Verdict and the Source text. Wording rejected during validation must not re-enter. If Claim, Verdict and Source text are materially inconsistent, do not choose a convenient reading: return status "REPAIR_FRD" and say what repair is needed.
2. Write the witness as plain declarative prose, at most {{CEILING}} whitespace-separated words (numbers, hyphenated compounds and citation words each count as one token where they contain no spaces). The ceiling is a maximum, not a target.
3. If the FRD holds more than fits, keep its central finding and the details the producing question asks about first, and leave the rest out. Leaving a separate fact out is legitimate. What is never legitimate is stating a retained finding without a qualification that changes its meaning.
4. For every assertion you keep, keep the qualifications that make it faithful: who reports it, study design, population / model / species, exposure (dose, route, duration), comparator, quantities with units and denominators, direction, polarity, modality (may / suggests / associated), conditions and timing.
5. Never add anything the FRD does not support: no new causal link, no generalization to another population, no strengthening of uncertainty, no turning a report into an assertion, no outside knowledge. Keep the source's own hedging words.
6. Name the source (author and year, or the filename) in the witness so it stands alone.
7. Return status "ABSTAIN" only when even the FRD's central finding cannot be stated faithfully within {{CEILING}} words, and list exactly which qualification would be lost.

## USER
PRODUCING QUESTION ({{QID}}), for context only:
{{QUESTION}}

VALIDATED FRD {{FRD_ID}}
Citation: {{CITATION}}
Claim: {{CLAIM}}
Verdict: {{VERDICT}}
Source text:
{{SOURCE_TEXT}}

CEILING: {{CEILING}} words.
{{REVISION_NOTE}}
Return ONLY a JSON object:
{
  "status": "WITNESS | ABSTAIN | REPAIR_FRD",
  "witness": "the witness prose",
  "preserved": ["qualification kept", "..."],
  "omitted": ["separate fact left out", "..."],
  "would_be_lost": "for ABSTAIN: the qualification of the central finding that cannot fit; otherwise empty",
  "repair_needed": "for REPAIR_FRD: what is inconsistent; otherwise empty"
}
