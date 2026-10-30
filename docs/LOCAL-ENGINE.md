# The local engine: what answers the model calls when nothing else does

Every earlier attempt at this harness stalled on the same dependency: an investigation needs several
hundred model answers, and when no operator was available the run stopped half-finished. The local
engine removes that dependency. It is the default provider for every role, it runs in-process, and it
needs no network, API key, queue or operator.

```
provider type: local        model identity: local-rules-v1.8
```

## The guarantee, and what it costs

**Guarantee.** With `default_provider = "local"`, `cr run` on a project with a corpus and a header
reaches `10_REPORTS/CRUX-REPORT.md` without ever returning `waiting`. There is no pending state,
because there is nothing external to wait for. Every answer is deterministic: the same project run
twice produces byte-identical artifacts, and a rerun is served entirely from the cache.

**Cost.** It is a *lexical-structural analyst*, not a language model. It reads the same prompt the
model roles read and applies explicit rules to the words in it. It does not understand a sentence.
Everything it concludes is an approximation of the judgment the prompt asks for, and the artifacts say
so: the run log records `local:local-rules-v1.8` as the provider and model for every call, and the
report discloses that the matching and assessment came from this engine.

This is the trade the owner authorized: a mediocre harness that always finishes, with every step
auditable and overrulable, instead of a better harness that stops.

## Role by role

| Role | What the local engine does | Where to check it |
|---|---|---|
| `indexer` | Reads the source file, ranks it A/B/C by design words (randomized/placebo, patients/trial, animal/model, review), summarises the opening | `01_FRAME/index.md` |
| `archivist_writer` | Emits a fixed evidence-discipline instruction set for the Archivist | `01_FRAME/archivist-custom-prompt.txt` |
| `investigator` | Rotates the ranked sources across the hypothesis clauses and decisive tests, one to two sources per question | `02_DISCOVERY/01_issued-questions/` |
| `archivist` | **Extractive**: scores the supplied passages against the question, quotes the best sentences with their file and heading, and never composes a new claim | `02_DISCOVERY/02_query-responses/` |
| `coordinator` | Cumulative bookkeeping split of the gauge over the hypotheses; substantive conditions computed from whether the round's answer blocks touch the decisive tests, falsification, assumptions and corroboration contexts | `04_ach-eval-checkpoints/` |
| `frd_generator` | Turns each `[SOURCE] "quote" (file, section)` line into one FRD, at most four per response | `03_FRDS/01_candidates/` |
| `frd_validator` | Finds the source sentence that best supports the candidate claim and copies it **verbatim**; if nothing supports it, NOT FOUND | `03_FRDS/04_validation-results/` |
| `unit_deriver` | Splits the human-written hypothesis into clause-level units, each anchored to an exact substring; caps 8 required / 4 constraint / 3 adverse / 3 corroborating / 1 evaluative | `01_FRAME/coverage-units.json` |
| `witness_constructor` | States the validated claim declaratively and appends the source as a citation suffix, within the word ceiling | `05_WITNESSES/` |
| `witness_auditor` | Checks for content the parent FRD does not license, dropped negation and dropped numerals | `03_fidelity-reviews/audits.json` |
| `matcher_a`, `matcher_b` | Weighted content coverage plus explicit checks (below); pass B is stricter by 0.05 | `03_match-records/relations.json` |
| `match_adjudicator` | On disagreement, keeps the weaker relation (a contradiction outranks an entailment) and labels the pair `MODEL_ADJUDICATED` | same file, `basis` |
| `joint_checker` | Proposes and verifies groups whose members *together* supply ≥ 0.85 of a unit's content, with each member contributing | `03_match-records/joint-groups.json` |
| `incompat_checker` | Approves a pair only if both passes find a quantity conflict or opposite polarity on the same predicate | `03_match-records/incompatibilities.json` |
| `assessor` | Counts released witnesses that share terminology with each hypothesis; splits the gauge accordingly | `10_REPORTS/assessment.json` |
| `reporter` | Writes the opening summary from the run record only | `10_REPORTS/CRUX-REPORT.md` |

## The matching rules, stated

Let `cov(unit, witness)` be the share of the unit's weighted content terms that the witness's terms
cover. Terms are normalised (case, plural, light stemming) and folded through a small synonym table
(PTX/pentoxifylline, human/patients, improve/ameliorate, ...); research-reporting words
(study, report, finding) carry 0.35 weight instead of 1.0.

1. **Quantity conflict** — the same measure with different values (`4.5 mL/s` vs `1.2 mL/s`) →
   `CONTRADICTS`.
2. **Same quantities, different frequency** (`three times daily` vs `once daily`) → `PARTIALLY_COVERS`.
3. **Actor/object reversal** — both sentences active, disjoint subjects, each subject appearing as an
   object in the other → `NO_SEMANTIC_RELATION`. Passive voice is exempt, because "X measured Y" and
   "Y was measured by X" are the same proposition.
4. **Scope mismatch** — human vs animal, or human vs in vitro → at most `PARTIALLY_COVERS`.
5. **Opposite polarity** — the same predicate family asserted with opposite polarity, negator within
   four words of the predicate, coverage ≥ 0.55, and the witness is not an aim sentence
   ("we tested whether ...") → `CONTRADICTS`. Sentence-level negation is deliberately *not* enough;
   "some report no yield difference" is not the negation of "reviews report inconsistent results".
6. **Combination partners differ** (`drug A plus tamsulosin` vs `tamsulosin plus placebo`) →
   `PARTIALLY_COVERS`.
7. **Stronger unit modality** (`must`) against weaker witness modality (`may`, `suggests`) →
   `UNIT_ENTAILS_WITNESS`.
8. **Second-hand witness** ("a review reports that ...") against a first-hand unit →
   `PARTIALLY_COVERS`; a witness stated only conditionally ("if ... may ...") → `PARTIALLY_COVERS`.
9. **Existential or capability unit** ("at least one study reports ...", "can ...") established by a
   concrete instance → `WITNESS_ENTAILS_UNIT`.
10. Otherwise by coverage: ≥ 0.72 with at least 0.55 of the witness's own content echoed back →
    `EQUIVALENT`; ≥ 0.72 one way → `WITNESS_ENTAILS_UNIT`; ≥ 0.45 → `PARTIALLY_COVERS`; below that →
    `NO_SEMANTIC_RELATION`. Pass B raises the complete threshold by 0.05 and the partial threshold by
    0.03, which is what produces the disagreements the adjudicator sees.

The 22 adversarial fixtures in `claimreg/matching.py` test exactly these distinctions (negation, actor
reversal, possibility vs necessity, report vs assertion, scope transfer, quantity conflict, and so
on). The engine passes all 22 in both passes; the run records that pattern by pattern. Passing them
qualifies the engine for those patterns only.

## Known failure modes

- **Hypothesis language vs source language.** Hypotheses are written in argumentative prose
  ("the materially supported rationale"), source findings in concrete prose ("flow rose by 1.2 mL/s").
  Lexical overlap between them is often too low for a complete relation. This is why the realistic
  PTX run reports `NO_COMPLETE_COVERAGE`: the matcher is not claiming a knowledge it does not have.
  Use a model for the `matcher_a`/`matcher_b` roles if you want model judgment.
- **No real negation scope, quantifier scope or anaphora.** The rules approximate them.
- **Duplicates.** The same source sentence can reach the run through several questions, producing
  near-identical witnesses. Retention only archives redundant FRDs when the database is over budget,
  so duplicates persist, and coverage sets multiply combinatorially.
- **Bookkeeping is not assessment.** The coordinator's and assessor's numbers are counts, not ACH_Eval
  judgment. The artifacts say so in their own text.

## Switching to a model

Any role can be routed independently. Nothing in the cache is lost: local answers stay keyed to the
local identity and are never presented as model answers.

```json
{
  "roles": {"matcher_a": "anthropic", "matcher_b": "anthropic", "match_adjudicator": "anthropic"},
  "providers": {"anthropic": {"model": "claude-opus-5-5", "api_key_env": "ANTHROPIC_API_KEY"}},
  "cache_fallback_providers": ["local"]
}
```

Then `cr run <project>` asks only the roles you moved, and reuses every local answer for the rest.

## Versioning

The model identity is `local-rules-<version>`. It is part of the cache key, so changing the engine's
behaviour without changing the version would silently reuse old answers. **Bump `VERSION` in
`claimreg/llm/local.py` whenever the engine's output changes**, then rerun; the run log will show both
identities side by side, which is the honest record.
