# Rules for evaluating bedtime levothyroxine dosing

The evaluation must compare the schedules patients can actually follow. A benefit produced by avoiding food, coffee, supplements, or missed doses remains a benefit of the scheduling strategy. Models must preserve that causal pathway when estimating the strategy's total effect.

This addendum governs evidence use and report acceptance. It specifies no winning hypothesis, minimum H1 allocation, maximum H3 allocation, or numerical bonus. It does not replace the existing frozen hypotheses silently. See [the audit and implementation plan](A2-AUDIT-AND-REPAIR-PLAN.md) for the proposed new frame and the defects in the previous assessment.

## Specify the comparison before judging evidence

Every assessment must declare which question it answers:

| Comparison | Question | What counts as benefit |
|---|---|---|
| Practical strategy | Switching from the patient's documented morning routine to an achievable bedtime routine | The total outcome change, including changes caused by food separation, convenience and adherence |
| Optimized schedules | Properly fasted morning dosing versus properly separated bedtime dosing, with comparable support | Comparative outcomes when both schedules are implemented well |
| Clock time | Morning versus nighttime while food, medicines, adherence and other relevant conditions are held comparable | The effect attributed to clock time under those conditions |
| Decision to offer a trial | Whether a monitored bedtime option is reasonable for an eligible patient | Expected benefits, burdens, alternatives and monitoring; this is distinct from established population efficacy |

An optimized-morning trial cannot by itself settle the practical-strategy comparison. A practical improvement cannot by itself establish an intrinsic nighttime advantage. A reasonable monitored option does not require proof that every refractory patient improves.

## Mandatory reasoning rules

**R1 Preserve the exact frame.** Print population, comparator, formulation, dose policy, meal and medicine separation, endpoints and follow-up. A new subgroup, question or success criterion receives a new frame version. Never describe a narrower proposed question as the original frozen A2.

**R2 Keep the intervention's mechanisms.** If assignment to a schedule causes better adherence or fewer near-dose interferents, those changes are mediators of its total effect. Do not adjust them away, relabel them as evidence of no benefit, or dismiss the outcome as merely behavioral. If additional counseling or a dose change differs between groups, identify that cointervention and the effect the study can actually estimate.

**R3 Distinguish an alternative from a rebuttal.** Evidence that correcting the morning routine might also help establishes an alternative intervention. It does not disprove a benefit from moving to bedtime. Comparative preference needs evidence about achievable adherence, outcomes and burdens under both options. A hypothetical dose increase is a third intervention; equivalent TSH correction would not establish equivalent burden, variability or patient preference.

**R4 Record the actual tested schedules.** Before using a study diagnostically, extract its prescribed and achieved food gaps, coffee and supplement gaps, dose changes, instructions and adherence measures. A trial permitting bedtime at one or two hours after food is not a direct test of a target requiring at least three hours. Keep its findings as indirect evidence or evidence about feasibility and shorter gaps. Apply the same restriction when a favorable trial used a different morning comparator.

**R5 Separate meal gaps from medicine gaps.** A three-hour dinner interval does not certify adequate separation from an iron or calcium dose. Record each relevant interval. The proposed target schedule uses a three-hour minimum after the last food and a separately specified interval for interacting medicines; drug-specific advice governs the latter.

**R6 Distinguish local from persistent interactions.** Do not put coffee co-ingestion and chronic acid suppression into one generic count. Identify which exposure the switch removes, which it changes partly and which persists. Moving LT4 away from the time of a PPI dose does not establish that acid suppression has ended. Avoid the converse assumption that persistent acid suppression makes every scheduling benefit impossible.

**R7 Compare exposure on both schedules.** Complete the two-column exposure ledger before allocating. Include breakfast and coffee, supplements and other medicines, late dinner or snacks, missed doses, irregular work or sleep, and background gastrointestinal disease. Record measured, reported, inferred or unknown status for each. Bedtime has no default zero-risk assumption; morning has no default perfect-adherence assumption.

**R8 Use joint exposure patterns.** Do not add separate prevalences or percentages of absorption loss as if independent. A multivitamin and its calcium ingredient are not two independent events. A population claim needs the relevant joint distribution and effect modification, or an explicit statement that these inputs are unknown. A known patient profile can still support a conditional conclusion when population frequencies are unknown.

**R9 Apply transfer standards in both directions.** For each principal driver, state the population, actual regimen, endpoint, mismatch and bridge to the target. Stable-cohort null findings do not directly establish no benefit in refractory patients; stable-cohort positive findings do not directly establish refractory efficacy. Mechanistic and exposure evidence can support a reasoned bridge, with remaining uncertainty identified.

**R10 Respect the endpoint's logic.** The original A2 H1 permits biochemical OR symptom benefit. Unchanged quality of life does not cancel a supported TSH or FT4 result; it limits the symptom claim. A lower TSH is favorable only relative to the patient's treatment target and without inappropriate suppression. Do not infer clinical symptom improvement from laboratory improvement alone.

**R11 Distinguish nonsignificance from equivalence.** A nonsignificant difference is not proof of equality. Record confidence intervals, precision, relevant clinical margins, study purpose and population. Support for no meaningful benefit requires evidence capable of excluding a meaningful effect in the comparison being assessed.

**R12 Make H3 specific and nonrepetitive.** Name the unresolved transport or identification problem that warrants uncertainty. Missing a trial with an identical eligibility sentence is not sufficient by itself to declare that no transfer is warranted. Repeated mentions of the same missing subgroup are one gap, not independent adverse findings. Background material in isolated partitions must not dilute the cumulative diagnostic record.

**R13 Preserve repaired validated claims.** A legacy verdict on an original candidate does not invalidate a repaired retained claim. Keep the current claim, its source support and restrictions. Unsupported superseded numbers remain excluded. Source fidelity, study quality and target applicability are separate judgments.

**R14 Account for study dependence.** Multiple FRDs, reviews or summaries of the same cohort do not become independent replications. Preserve conflicting findings and the strongest adverse evidence. A model must explain actual discrimination among the hypotheses, not count favorable sentences or study titles.

**R15 Require evidence for weighting.** Weight by causal identification, relevance to the specified comparison, exposure change, precision, consistency and harms. Use no fixed per-confound bonuses, automatic H1 minimum, repeated-gap penalty or default penalty for validated summaries. When numerical prevalence or effect inputs are unavailable, give a qualitative or conditional conclusion instead of invented arithmetic.

## Required report fields

Each report must contain:

1. The exact frame and the comparison type from the first table.
2. A morning-versus-bedtime exposure ledger with sources, time intervals and unknowns.
3. A study table with actual protocols, target applicability, effects, precision and dependence.
4. A causal account distinguishing baseline confounders, intervention-mediated changes and cointerventions.
5. A diagnostic map explaining why each principal driver favors the hypothesis claimed, with symmetric transfer restrictions.
6. Separate conclusions about biochemical benefit, symptoms, safety, practical feasibility and the warrant to offer a monitored option.
7. The G=64 vector, exact hypothesis IDs, strongest objection, reversal finding, unresolved gaps and provenance of any newly added evidence.
8. Every rule violation found and its repair. A report with an unresolved prohibited inference is rejected for correction before its allocation is released.

## Enforcement and its limits

Use a source protocol catalog whose key facts are extracted and checked before judging. The included [evaluation gate](evaluation_gate.py) rejects direct-rebuttal claims that contradict that catalog, endpoint cancellation, dismissal of mediated benefits, invented equivalence, invented prevalence and invalid vectors. [Examples](gate_examples.json) exercise both favorable and unfavorable directions.

The deterministic guarantee is narrow: a report declaring one of those prohibited uses cannot pass the gate. A model could still misdescribe an inference or omit a material fact; source inspection and semantic review remain necessary. JSON compliance alone does not certify sound judgment. A rejected report is an evaluation failure, not evidence favoring H3.

The defensible positive strategy is to specify the practical comparison, identify patients whose morning interference can actually be removed, and assess the resulting outcomes and burdens. If the evidence supports H1 under that question, the model must credit it. A guaranteed H1 allocation would specify the answer before examining the evidence.
