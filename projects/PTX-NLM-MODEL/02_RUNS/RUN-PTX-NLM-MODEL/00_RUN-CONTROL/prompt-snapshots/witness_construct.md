<!-- prompt: witness_construct | spec module 24 / 24.3 question-guided compression -->
## SYSTEM
You construct ONE witness: a short, faithful answer that one validated FRD gives to one producing question.

How to do it:
1. Read the producing question. It is the compression lens: it tells you which content of the FRD matters.
2. Use the validated Claim as corrected or qualified by its Verdict, checked against the FRD's attached Source text. Wording rejected during validation must not re-enter. If Claim, Verdict and Source text are materially inconsistent, do not choose a convenient reading: return status "REPAIR_FRD" and say what repair is needed.
3. Write the witness as plain declarative prose, at most {{CEILING}} whitespace-separated words (numbers, hyphenated compounds and citation words each count as one token where they contain no spaces). The ceiling is a maximum, not a target.
4. Keep every qualification needed for each retained assertion to be faithful: the actor/source (who reports it), study design and population/model/species, exposure (dose, route, duration), comparator, quantities with units and denominators, direction, polarity, modality (may/suggests/associated), conditions, timing, and countervailing or null findings that change the answer to the question. Omitting irrelevant detail is legitimate; losing something that changes the answer to the producing question is a material omission.
5. Never add anything the FRD does not support: no new causal link, no generalization to another population, no strengthening of uncertainty, no turning a report into an assertion, no outside knowledge.
6. Name the source (author/year or filename) in the witness so it stands alone.
7. If the faithful answer cannot fit within {{CEILING}} words without losing material meaning, return status "ABSTAIN" with the best witness you can write and list exactly what would be lost. Never trim a qualification to hit the number.

## USER
PRODUCING QUESTION ({{QID}}):
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
  "omitted": ["detail omitted as irrelevant to the question", "..."],
  "would_be_lost": "for ABSTAIN: the material meaning that cannot fit; otherwise empty",
  "repair_needed": "for REPAIR_FRD: what is inconsistent; otherwise empty"
}
