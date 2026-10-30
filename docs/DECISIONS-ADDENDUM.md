# Decisions taken in the final build

*DeepSeek, 2026-10-30. A continuation of `DECISIONS.md`, which records the first build's choices. Read
that first; this file records only what changed or was added.*

The owner's instruction for this build was: no blockers, complete agency, and a harness that actually
exists is worth more than a perfect one that does not. Every choice below follows that instruction.

---

## 1. A local engine is the default provider

**Decision.** Ship `local-rules-v1.8` (`claimreg/llm/local.py`) as the default for all 19 roles. It is
a deterministic, offline, lexical-structural analyst that answers the same prompts the model roles read
and emits the same JSON shapes. It needs no key, network, queue or operator.

**Why.** Every earlier attempt stalled because an investigation needs hundreds of external model
answers. That is not a specification problem; it is a dependency problem, and it is the one thing that
made "finished" impossible. With the local engine, `cr run` on a project with a corpus and a header
always reaches a report.

**Cost, disclosed everywhere.** It does not understand language. Its judgments are approximations, the
run log records it as the provider for every call, and the report says the matching and assessment came
from it. Routing a real model to any role replaces it incrementally: cached local answers stay keyed to
the local identity and are never presented as model answers.

## 2. The witness is a declarative statement with a citation suffix

**Decision.** `"Foliar silicate increased yield by 18 percent (field2023)."`, not
`"Field2023 reports that foliar silicate increased yield by 18 percent."`

**Why.** The first build's framing made every witness look like a second-hand report, which the
matcher is required to distinguish from a first-hand finding; every witness was therefore downgraded to
`PARTIALLY_COVERS` and no complete relation could ever exist. The suffix keeps the attribution the
specification requires without changing the epistemic form of the claim.

**Where to change it.** `LocalProvider._role_witness_constructor`; the mechanical numeral check already
allows digits from the source filename.

## 3. Contradiction is judged at the predicate, not at the sentence

**Decision.** A witness contradicts a unit only when they assert the same predicate family (increase /
decrease / differ / reach / report) with opposite polarity, the negator sits within four words of the
predicate, coverage is at least 0.55, and the witness is not an aim sentence ("we tested whether ...").

**Why.** Sentence-level negation produced false contradictions by the dozen: "some report no yield
difference" was read as the negation of "reviews report inconsistent results", and a methods sentence
was read as contradicting a finding. Predicate-level polarity reduces that class to cases where the
same assertion is made with opposite sign. It still cannot handle quantifier scope or double negation,
which is one reason the engine's matching is labelled an approximation.

## 4. Jointly sufficient groups are a union-coverage construction

**Decision.** The local joint checker proposes a group when its members together supply at least 0.85
of a unit's weighted content, each member adds something the others do not, and no member alone reaches
0.85. The verification pass applies the same rule and records that it is a lexical construction, not
logical entailment.

**Why.** Requiring a single witness to entail a whole hypothesis clause makes coverage nearly
unreachable for a lexical matcher. Joint groups are the specification's own mechanism for exactly this
situation, and using them exercises the coverage solver and crux tests that the earlier builds never
reached. Every approved group is visible in `03_match-records/joint-groups.json` and revocable.

## 5. Unit derivation is clause splitting with verbatim anchors

**Decision.** Split the human-written hypothesis at sentence boundaries, semicolons, commas before a
conjunction, and subordinating conjunctions — **never** at a bare "and", which usually joins nouns
inside one requirement. Keep clauses of six words or more, drop the rest, and verify every resulting
`source_quote` is a contiguous substring. Caps: 8 required, 4 constraint, 3 adverse, 3 corroborating,
1 evaluative.

**Why.** Units must be atomic enough for one source finding to establish them, and every quote must be
mechanically checkable. An earlier version split at "and" and produced fragments such as "…a
reversible physiological component that tamsulosin", which are verbatim but not requirements.

**Known limitation.** Clause-level units can still bundle several ideas, and hypothesis prose is more
abstract than source prose. On the PTX corpus this is why no required unit reaches complete coverage:
the engine declines to claim it understands a sentence it only overlaps with.

## 6. The quest can end at the operational ceiling, and says so

**Decision.** The local Coordinator's allocations are a cumulative bookkeeping split of the gauge,
moved by the number and strength of answer blocks that share terminology with each hypothesis. Its four
substantive conditions are computed from the evidence (decisive tests touched, falsification contexts
touched, assumptions touched, corroboration contexts touched), not asserted. If the allocation never
stabilises, the quest ends at `quest.max_rounds` with `OPERATIONAL_LIMIT`, and the report states that
this is an operational stop, not a scientific completion finding.

**Why.** A constant or arbitrary allocation would have made the gauge-keyed stop rule fire at round 4
for no scientific reason. This version lets the rule fire only when the bookkeeping really stops
moving, and reports the ceiling honestly when it does not.

## 7. Two synthetic artifacts ship with the harness

- `examples/demo/` — a realistic five-source corpus, where the harness honestly finds no complete
  coverage. `cr demo` runs it from an empty folder in about a minute. It is labelled synthetic on every
  page and must never be cited as evidence.
- `examples/worked/` — a deliberately worded corpus where source sentences restate hypothesis clauses,
  so complete relations, coverage sets, approved incompatibilities and crux candidates actually occur.
  It is the end-to-end regression test for the last three modules (`tests/test_worked_example.py`).

**Why.** The realistic corpora reach no complete coverage, which means the coverage and crux modules
would never be exercised end to end. The worked example proves they produce artifacts and fails loudly
if they stop. It is a test fixture, not a finding.

## 8. Tests use a checkout-local scratch directory

**Decision.** `tests/scratch.py` creates a plainly named directory under `<checkout>/.tmp`.

**Why.** `tempfile.mkdtemp()` produces a directory that the Windows sandbox used for this build cannot
write inside (a restrictive ACL lands on the 0o700 directory). Plain directories work, the tests run
everywhere, and `CR_TEST_TMP` moves the directory if needed.

## 9. The PTX offline run is a second run in a copied project

**Decision.** `projects/PTX-LOCAL/` is a copy of the PTX corpus and header, with its own
`RUN-PTX-LOCAL-OFFLINE` run produced entirely by the local engine. The earlier queue-based run
(`projects/PTX/`) is untouched, with its model-answer cache restored from its own release archive.

**Why.** The two runs are different evidence contracts (model answers through a queue vs. a local
lexical engine). Keeping both lets the reader compare them, and keeps the earlier run's audit trail
intact. Neither is presented as the other.

## 10. What this build did not attempt

- Re-running the ChatGPT-era NotebookLM discovery. The PTX corpus is the local copy; discovery in the
  offline run is the harness's own quest over that copy.
- Reconstructing the missing dictionary release. The language layer remains off by default.
- Making the local matcher good. It is a floor, not a ceiling: it guarantees a finished run, and the
  review packet, the human-decision file and per-role model routing are the ways to improve on it.
