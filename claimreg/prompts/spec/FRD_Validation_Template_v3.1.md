# FRD validation prompt generator and template v3.1

## Generator instructions

Produce one custom FRD validation prompt by lightly adapting the embedded template. Return only the finished prompt. Do not validate FRDs during initialization.

Use the actual custom instructions given to the Archivist to recover the evidence-label meanings and applicable source, language, and citation restrictions. An Archivist generator or embedded example is insufficient. Request the deployed instructions if missing. A quest header is “incorrect for initialization”; request the Archivist instructions without the header and stop.

Customize only the label-check paragraph and, if needed, one short domain-specific caution. Preserve the five output fields, Deliverable section, and source-only checking rules. Do not add a disposition taxonomy beyond the readiness flag, a scoring system, or an external appendix. Preserve supplied label meanings exactly; do not create a hierarchy or add categories. A provisional response label must be checked against the source, not accepted as evidence.

Exclude hypotheses, preferred conclusions, source rankings, and downstream relevance judgments. The generated prompt runs in a fresh context with candidate FRDs and their named source files. The context preparing it does not perform validation. Keep the finished prompt within 400 words where possible. Report any mandatory requirement that cannot fit rather than silently drop it.

Before deploying the generated prompt, replace revealing origin filenames with opaque references in the validation copy; retain the filename mapping outside the kit. Check other metadata for disclosure of the research frame. Preserve QIDs and traceability.

## Embedded template

# FRD VALIDATION INSTRUCTIONS

Check each FRD against only its named source or sources. Exclude query responses, summaries, indexes, and outside knowledge. Use a fresh context without the header or intended conclusion.

Check every clause, attribution, qualification, and locator. Transmitted claims establish only the transmitter’s report. Never recruit an unnamed source to rescue failure.

For `disambiguate`, check each named candidate separately and record its result. Produce one repaired FRD per supported claim per source; retain unresolved attribution as NOT READY. One source may span named parts of the same work; preserve exact locations and speaker.

## Labels

[INSERT THE SUPPLIED LABEL MEANINGS AND ONE BRIEF INSTRUCTION TO CHECK THEM AGAINST THE SOURCE.]

Correct mistaken evidence labels in Verdict. Retrieval gaps cannot prove absence. Separate analyst inference from source statements.

## Output for each FRD

**[Original FRD ID]** — preserve its supplied origin reference and producing QID.

1. **Citation** — reference, exact source filename(s), and location(s); note missing metadata.
2. **Claim** — corrected, supported wording; otherwise state that support is unestablished.
3. **Source text** — exact supporting or contradicting text. Include whole paragraphs where needed, or table/figure context with labels and units. Never silently repair quotations.
4. **Verdict** — RIGHT / MOSTLY RIGHT / PARTLY RIGHT / WRONG / NOT FOUND / SOURCE UNAVAILABLE, with a brief explanation. Evaluate the original candidate; preserve its wording when changed and explain material repairs.
5. **Provenance** — `OWN_RESULT` / `DERIVED_FROM(ancestor)` / `DERIVATIVE_UNKNOWN`, as confirmed or corrected against the source.

## Deliverable

Produce a repaired, source-supported FRD. Correct known defects in claim, citation, attribution, scope, labels, and provenance. Mark **READY FOR WITNESS CONSTRUCTION** only when claim and evidence support faithful compression without unresolved material defects. Otherwise mark **NOT READY FOR WITNESS CONSTRUCTION**; retain for audit. Readiness evaluates the repaired FRD independently of Verdict.

If the locator fails, search throughout each named candidate using wording variants before NOT FOUND. Repair mistaken locators. Use SOURCE UNAVAILABLE for inaccessible sources; report incomplete searches without a blanket NOT FOUND. Split compound claims as needed; children retain the parent's origin and QID. Each output contains its own evidence and explanation.
