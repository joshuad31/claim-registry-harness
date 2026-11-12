# Rules for evaluating bedtime levothyroxine dosing

The evaluation must compare the schedules patients can actually follow. A benefit produced by avoiding food, coffee, supplements, or missed doses remains a benefit of the scheduling strategy. Models must preserve that causal pathway when estimating the strategy's total effect.

This addendum governs evidence use and report acceptance. It specifies no winning hypothesis, minimum H1 allocation, maximum H3 allocation, or numerical bonus. It does not replace the existing frozen hypotheses silently. See [the audit and implementation plan](A2-AUDIT-AND-REPAIR-PLAN.md) for the proposed new frame and the defects in the previous assessment.

**Current axis question (2026-11-12).** The frozen Axis-two question is `A2-C-v1`: should patients whose TSH stays above target be offered the option of bedtime dosing — should they and their clinicians think about it, ask about it and discuss it. Some rules below explain themselves with the earlier efficacy frame (`A2-P-v1`); the evidence-use principle in each rule still applies, but the approved header's hypothesis statements control what H1, H2 and H3 mean. Evidence that a trial average was null is not evidence that no patient gains, and evidence about following the morning instructions is evidence about the alternative, not a rebuttal of the option (R3).

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

**R2 Keep the intervention's mechanisms.** If assignment to a schedule causes better adherence or fewer near-dose interferents, those changes are mediators of its total effect. Do not adjust them away, relabel them as evidence of no benefit, or dismiss the outcome as merely behavioral. If additional counseling or a dose change differs between groups, identify that cointervention and the effect the study can actually estimate. A schedule-caused *harm* (for example, nocturnal food or supplement contamination that reduces absorption, or worse bedtime adherence) is evidence against H1 and may be declared `"direction": "harm"`; R2 forbids erasing a schedule-caused benefit, not recording a schedule-caused harm.

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

## Addendum rules R16–R22

*Installed 2026-11-11 from the pre-run audit; `bedtime_gate_v2.py` enforces R16–R21 and the harness enforces R22.*

* **R16 — AI-synthesis and secondary-dossier exclusion:** Documents flagged in `corpus.synthesis_sources` (including AI-generated research memos, Google Docs, and compiled label dossiers) and uncanonicalized duplicate copies (`corpus.duplicates`) are **non-citable leads, never empirical evidence**. Citing any synthesis or duplicate file as an allocation driver triggers automatic gate rejection.

* **R17 — Allocation-to-gate driver bijection:** Every `frd_id` listed in the primary `allocations` JSON `drivers` array **must** appear in `gate_report.drivers` with a matching directional assignment (`favors == A2-H1` ↔ `"favors_bedtime"`; `favors in (A2-H2, A2-H3)` ↔ `"against_bedtime"` or `"neither"`), and `gate_report` is verified against the harness's true FRD `source_file` registry and frozen `frame`. A report that names fewer than three allocation drivers is rejected: an allocation must say what moved it.

* **R18 — Stratum conditioning for pooled and enforced-fasting trial averages:** Unconditioned meta-analyses (`Pang 2020`, `Bianchini 2024`, `da Rocha 2025`) and trials enforcing strict `60-minute` morning fasting (`Bach-Huynh 2009`) or short `< 180-minute` bedtime food gaps (`de Mello 2022` at `60 min`; `Bach-Huynh 2009` / `Skelin 2018` / `Rajput 2011` at `120 min`) estimate effects conditional on their tested protocols and baseline strata.
  1. Pooled null averages refute *unconditional population superiority*, **not** conditional benefit in the timing-removable morning-interference stratum (`S1`).
  2. Any driver from a pooled analysis or protocol-mismatched trial used against (or for) bedtime must be declared `"indirect"` and must explicitly name both the protocol gap and the exposure stratum (`documented_removable_morning_interference`, `persistent_non_timing_cause`, or `no_documented_interference`) to which it applies. Never invent joint population prevalence weights (`R8`).

* **R19 — Symmetric mechanistic transport and mandatory 3-stratum conclusions (direction-neutral):** When no single RCT combines every target eligibility clause simultaneously, `H3` does **not** win by default. Evaluate causal transportability **symmetrically**:
  * If primary human studies quantify (i) the TSH/absorption penalty of the baseline exposure AND (ii) the effect of the tested schedule separation, weight `H1` vs `H2` according to the empirical direction, magnitude, and protocol fidelity of both links — applying the exact same `"indirect"` bridge requirement to favorable trials (`Bolk 2010` 30-min morning comparator; `Bolk 2007` non-randomized switch) and unfavorable trials (`de Mello 2022` 60-min bedtime gap; `Bach-Huynh 2009` 120-min bedtime gap).
  * Every report must output explicit `stratified_conclusions` across all three clinical strata:
    1. `documented_removable_morning_interference` (with clean `>= 3h` evening window),
    2. `persistent_non_timing_cause` (chronic PPIs, *H. pylori*/atrophic gastritis, celiac/bariatric malabsorption, or true pill-omission pseudo-malabsorption), and
    3. `no_documented_interference` (already adherent `60-min` morning fasters, or patients with `< 3h` late dinners / nocturnal cation supplements / shift work).

* **R20 — Persistent acid-suppression routing (Axis A3 boundary) and mandatory 5-point patient safety block:** Proton-pump inhibitors irreversibly inactivate gastric H+/K+-ATPase across 24 hours (`Awasthi 2023`, `Centanni 2006`); **never claim that moving an LT4 tablet to bedtime overcomes PPI-induced hypochlorhydria** (route persistent PPI/gastritis malabsorption to Axis A3 liquid/softgel formulations or GI management). Furthermore, every report must populate the `safety` block addressing all five clinical hazards:
  1. `overreplacement_recheck_weeks`: Mandatory `6–8 week` TSH recheck because removing a chronic morning chelator in previously up-titrated patients (`> 1.6–2.0 mcg/kg/day`) can abruptly jump absorption and cause iatrogenic thyrotoxicosis (`Bugdaci 2011`).
  2. `bedtime_interferents_checked`: Explicit `>= 3h` post-meal/snack rule (no bedtime cow's milk [`Chon 2018`] or soy) and `>= 4h` separation from bedtime calcium (carbonate, citrate, or acetate [`Zamfirescu 2011`]), magnesium sleep supplements, iron, sucralfate, antacids, or bile-acid binders; caution on GLP-1 RAs/gastroparesis and rotating shift work.
  3. `sampling_time_standardised`: Anchor titration to morning TSH drawn at a consistent clock hour; warn clinicians not to misread the ~9-hour post-dose serum FT4 elevation (`Ain 1993`) on an 8 AM lab draw after a 10–11 PM bedtime dose.
  4. `no_dose_change_at_switch`: Do not escalate tablet mcg simultaneously when switching to bedtime (and consider proactive clinician dose review if baseline dose was markedly supraphysiologic).
  5. `high_risk_groups_named`: Explicit supervision precautions for elderly (`>= 65–70y`), atrial fibrillation / coronary disease, severe osteoporosis, pregnancy, and thyroid-cancer TSH-suppression patients.

* **R21 — Explicit separation of efficacy (A2-P-v1) and decision-to-offer (A2-D-v1):** Every report must state a separate `decision_to_offer` conclusion evaluating whether a monitored `6–8 week` bedtime trial is warranted in eligible patients, distinct from unstratified population efficacy.

* **R22 — Gate retry cap and audit preservation:** Automated or manual gate-correction retries for any axis are capped at **`max_gate_attempts = 2`**, with every rejected allocation and error list preserved in `evaluation-history.jsonl`. Re-running an axis to shop for a preferred allocation vector is prohibited; if Attempt 2 fails the gate, execution halts for human audit.

## Enforcement and its limits

Use a source protocol catalog whose key facts are extracted and checked before judging. The included [evaluation gate](evaluation_gate.py) rejects direct-rebuttal claims that contradict that catalog, endpoint cancellation, dismissal of mediated benefits, invented equivalence, invented prevalence and invalid vectors. [Examples](gate_examples.json) exercise both favorable and unfavorable directions.

The deterministic guarantee is narrow: a report declaring one of those prohibited uses cannot pass the gate. A model could still misdescribe an inference or omit a material fact; source inspection and semantic review remain necessary. JSON compliance alone does not certify sound judgment. A rejected report is an evaluation failure, not evidence favoring H3.

The defensible positive strategy is to specify the practical comparison, identify patients whose morning interference can actually be removed, and assess the resulting outcomes and burdens. If the evidence supports H1 under that question, the model must credit it. A guaranteed H1 allocation would specify the answer before examining the evidence.
