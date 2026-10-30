# FRD generation prompt generator and template v3.1

## Generator instructions

Produce one custom FRD generation prompt by lightly adapting the embedded template. Return only the finished prompt. Do not generate FRDs during initialization.

**Required input:** the actual custom instructions used by the Archivist for this quest. These establish the evidence labels, category meanings, topical distinctions, source restrictions, and citation rules.

**Reject a quest header as initialization input.** If a header is supplied, respond: “incorrect for initialization. Please supply the actual custom instructions given to the Archivist, without the quest header.” Stop without generating a prompt. Do not extract or sanitize the header, even if valid instructions accompany it. An Archivist prompt generator or its embedded example also cannot substitute for the actual deployed instructions. If those instructions are missing, request them.

Adapt only the subject, neutral cluster examples, and the label-handling paragraph. Preserve supplied labels and meanings exactly. State how each category affects extraction: source-attributed findings and interpretations are candidates; analyst extrapolations require separately extractable source premises; retrieval gaps belong in the harvest review. Follow the supplied meanings, not assumptions about label names. Labels do not establish truth or a universal ranking. Do not invent labels, exclusions, or priorities.

Carry over applicable source, language, and citation restrictions. Do not import the Archivist's answer format or length limit. Add at most two short topic-specific cautions where necessary. Preserve the template's lineage and source-support rules. Remove placeholders. Keep the finished prompt within 500 words where possible; if mandatory requirements cannot fit, report the conflict rather than omit them.

## Embedded template

# FRD GENERATION INSTRUCTIONS

The quest is complete. Extract candidate claims about [SUBJECT] from the supplied Archivist query-response files for later source validation. Responses are discovery material, not evidence.

Process one query-response file at a time. Harvest its relevant claims before moving on. One FRD states one claim and carries exactly one producing QID. Never combine material from different response files into one FRD. If a QID is missing, report it; do not invent one.

Anchor each FRD to one source wherever the response permits. Split separately attributed clauses into individual claims. When the response explicitly attributes the same claim separately to multiple sources, create one candidate FRD per source. When a passage cites multiple sources without revealing which supports which clause, record one FRD naming every candidate source and set Status to `disambiguate`. Do not guess an attribution, and do not drop a claim because its attribution is unresolved. Record exact cited parts; file boundaries alone do not establish independent evidence. Preserve the actual speaker.

Preserve the actual speaker, qualifications, conditions, numbers, adverse findings, nulls, and limitations. Separate a source's own findings from its reports of other authorities. Do not turn response synthesis into source testimony or invent filenames and locators.

## Labels and categories

[INSERT THE SUPPLIED LABELS, THEIR MEANINGS, AND CONCISE EXTRACTION CONSEQUENCES.]

Retain the response's label as provisional metadata. Do not discard a source-attributed claim merely because its label appears wrong; flag it for validation. Extract individually sourced premises of analyst inferences where available. Record unsupported synthesis and retrieval gaps in the review; they do not establish source claims or corpus-wide absence.

## Entry format

Group entries into neutral topic clusters such as [CLUSTERS]. Number sequentially as **FRD-[CLUSTER]-[##] — [short label]**.

1. **Origin** — query-response filename or mapped opaque reference, and one producing QID.
2. **File and location** — exact source filename; heading, table, or best search terms. For a `disambiguate` entry, list every candidate source filename with its locator.
3. **Candidate claim** — one or two sentences stating one source-attributed proposition without strengthening it.
4. **Verification instruction** — what passage, number, attribution, or qualification to check; include the original evidence label and any suspected labeling error.
5. **Provenance** — `OWN_RESULT`, `DERIVED_FROM(ancestor)`, or `DERIVATIVE_UNKNOWN`, provisionally based on the response.
6. **Status** — `ordinary`; `disambiguate` (candidate sources named, attribution unresolved in the response); or `needs-source` (claim carries no usable citation).

## Harvest review

List each response file processed, counts of FRDs, counts of `disambiguate` and `needs-source` entries, unresolved citations or labels, and candidates not extracted with reasons. List every required source filename by cluster. Flag cited sources yielding no FRDs. Keep gaps and unsupported synthesis distinguishable from extracted claims.
