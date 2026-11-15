# How each hypothesis was compiled into requirements

Coverage sets and crux tests are decided against the *units* below, not against the hypothesis sentences. Read this before the coverage and crux results: a sentence no unit represents is invisible to both, and a unit stricter than its sentence makes coverage harder than the author asked for. This page is computed from saved records. It makes no model call, it is not an approval step and it changes no result.

## Axis A2: Should patients on levothyroxine tablets whose TSH stays above target be told that taking the same tablet at bedtime might help them — should they and their doctors think about it, ask about it, discuss it, and be given the option to try it? Frame …

### A2-H1 - Offer the option

5 required, 3 constraint, 4 adverse-test, 4 expected and 1 evaluative unit(s).

This is the compiled theory the crux tests are run against when a witness of A2-H2, A2-H3 is tested against A2-H1.

#### The hypothesis as written, and what each sentence produced

*Statement*

1. Yes.
   - `A2-H1-J1` (not a requirement (judged in the final assessment)), anchored on: "Yes. Patients should be offered the option of taking the same tablet at bedtime, and should be encouraged to think about it, ask about it and discuss it with their …"
2. Patients should be offered the option of taking the same tablet at bedtime, and should be encouraged to think about it, ask about it and discuss it with their clinician.
   - `A2-H1-J1` (not a requirement (judged in the final assessment)), anchored on: "Yes. Patients should be offered the option of taking the same tablet at bedtime, and should be encouraged to think about it, ask about it and discuss it with their …"
3. This applies in particular to two groups: (i) patients who do not follow the instructions on the label — for example, they drink coffee within one hour of waking — and are complaining of hypothyroid symptoms, and (ii) patients who do follow the label instructions but still complain of hypothyroid symptoms.
   - *no unit*
4. The switch is the same tablet at the same dose, costs nothing beyond a follow-up TSH test, can be reversed, and with that recheck the risk is low.
   - `A2-H1-R3` (must be supported), anchored on: "with that recheck the risk is low."
   - `A2-H1-R4` (must be supported), anchored on: "can be reversed"
   - `A2-H1-C2` (must not be contradicted), anchored on: "The switch is the same tablet at the same dose"

*Assumptions and antecedents*

5. Some patients' morning routines put food, coffee, a PPI or supplements near the dose, and they do not or cannot change them; other patients follow the label instructions exactly and still have above-target TSH and hypothyroid symptoms; at least some patients in both groups can keep a clean evening window; a TSH recheck at 6–8 weeks is available; the tablet and dose stay the same at the switch.
   - *no unit*

*Potential falsification*

6. Evidence that bedtime dosing gives no patient of either group a better TSH or absorption than their own morning routine.
   - `A2-H1-A1` (visible, not required (would count against)), anchored on: "Evidence that bedtime dosing gives no patient of either group a better TSH or absorption than their own morning routine."
7. Evidence that a switch commonly causes harm a 6–8 week recheck would not catch.
   - `A2-H1-A2` (visible, not required (would count against)), anchored on: "Evidence that a switch commonly causes harm a 6–8 week recheck would not catch."
8. Evidence that patients in both groups cannot keep an evening window clean.
   - `A2-H1-A3` (visible, not required (would count against)), anchored on: "Evidence that patients in both groups cannot keep an evening window clean."
9. Evidence that correct label adherence, rather than a schedule change, removes every symptom and every raised TSH in these patients.
   - `A2-H1-A4` (visible, not required (would count against)), anchored on: "Evidence that correct label adherence, rather than a schedule change, removes every symptom and every raised TSH in these patients."

*Potential corroboration*

10. Trials or case series in which bedtime dosing lowered TSH or raised free T4 at the same dose.
   - `A2-H1-R1` (must be supported), anchored on: "Trials or case series in which bedtime dosing lowered TSH or raised free T4 at the same dose."
   - `A2-H1-E1` (visible, not required (expected)), anchored on: "Trials or case series in which bedtime dosing lowered TSH or raised free T4 at the same dose."
11. Evidence that patients in either group — those not following the label or drinking coffee soon after waking, and those following the label but still symptomatic — report or show improvement after a bedtime switch.
   - `A2-H1-E2` (visible, not required (expected)), anchored on: "Evidence that patients in either group — those not following the label or drinking coffee soon after waking, and those following the label but still symptomatic — report or show …"
12. Absorption studies showing that morning food, coffee, calcium or iron cut absorption.
   - `A2-H1-R2` (must be supported), anchored on: "Absorption studies showing that morning food, coffee, calcium or iron cut absorption."
13. Surveys showing that patients often take the tablet near breakfast, coffee or supplements, or find the morning fast a burden.
   - `A2-H1-E3` (visible, not required (expected)), anchored on: "Surveys showing that patients often take the tablet near breakfast, coffee or supplements, or find the morning fast a burden."
14. Guidelines or product labels that accept bedtime dosing.
   - `A2-H1-R5` (must be supported), anchored on: "Guidelines or product labels that accept bedtime dosing."
15. Few adverse events reported for bedtime dosing.
   - `A2-H1-E4` (visible, not required (expected)), anchored on: "Few adverse events reported for bedtime dosing."

**Written by you, checked by nothing.** No unit is anchored on these sentences, so neither coverage nor the crux tests see them: sentence 3, sentence 5.

Units anchored on header passages or another hypothesis's text, not on this hypothesis: `A2-H1-C1`, `A2-H1-C3`.

#### Requirements

| Unit | Role | Text | Serves | Satisfied by | State | Options | Active |
|---|---|---|---|---|---|---|---|
| `A2-H1-R1` | must be supported | In at least some adults on levothyroxine tablet monotherapy with persistently above-target TSH, switching dosing time from morning to bedtime while keeping the same tablet and dose lowers TSH and/or raises free T4 compared with their own morning routine. | effect on TSH/absorption (bedtime switch can help some) | a trial or case series reporting that after switching from morning to bedtime at the same levothyroxine tablet dose, TSH decreased and/or free T4 increased in at least some patients | supported with assumption | 0 direct, 10 with a transfer | yes |
| `A2-H1-R2` | must be supported | Morning co-exposures near the levothyroxine tablet dose (food, coffee, calcium, iron, or multivitamins) reduce levothyroxine absorption or worsen thyroid hormone labs compared with a separated/fasted condition. | mechanistic/PK basis for offering bedtime to patients with interfering morning routines | a pharmacokinetic or absorption study showing reduced levothyroxine absorption or worse thyroid labs when taken with/near food, coffee, calcium, iron, or multivitamins versus separated/fasted dosing | established | 12 direct, 0 with a transfer | yes |
| `A2-H1-R3` | must be supported | A bedtime-switch strategy (same levothyroxine tablet and same dose) is low-risk when followed by a TSH recheck at 6–8 weeks, with no commonly reported serious harms that this monitoring would fail to detect. | safety/monitoring premise for offering the option | a clinical study or guideline statement reporting that bedtime dosing at the same dose has few/limited adverse events and is managed with follow-up TSH testing around 6–8 weeks | supported with assumption | 0 direct, 1 with a transfer | yes |
| `A2-H1-R4` | must be supported | Switching from morning to bedtime can be reversed while keeping the same levothyroxine tablet and dose (i.e., patients can return to morning dosing if needed). | reversibility premise for offering the option | a study protocol, clinical report, or guideline noting that patients can change timing back (bedtime to morning) without changing the levothyroxine tablet or dose | supported with assumption | 0 direct, 1 with a transfer | yes |
| `A2-H1-R5` | must be supported | Bedtime dosing is accepted as an option in at least one clinical guideline or product label for levothyroxine tablets (i.e., bedtime administration is presented as an allowable alternative to morning dosing). | practical offerability (endorsed/accepted option) | a guideline or product label stating that levothyroxine may be taken at bedtime/evening (under specified conditions) as an alternative to morning dosing | contested | 1 direct, 0 with a transfer | yes |
| `A2-H1-C1` | must not be contradicted | The population in scope is adults on levothyroxine tablet monotherapy whose TSH has stayed between 4.5 and 10.0 mIU/L for three months or longer, whether or not they follow label instructions. | scope / population definition (refractory cohort) | a study or report explicitly describing (or allowing identification of) adults on levothyroxine tablet monotherapy with TSH 4.5–10 mIU/L persisting for ≥3 months | partial only | - | yes |
| `A2-H1-C2` | must not be contradicted | The intervention is only a timing change to bedtime using the same levothyroxine tablet at the same dose (no formulation change and no dose increase as part of the switch). | intervention definition (same tablet, same dose) | a trial or observational report in which levothyroxine tablet dose and formulation are held constant while switching dosing time to bedtime | contested | - | yes |
| `A2-H1-C3` | must not be contradicted | Whether patients actually follow morning label instructions is not assumed; adherence to morning instructions is itself part of the evidence. | no-adherence-assumption boundary | a survey, cohort study, or trial baseline assessment measuring how patients take levothyroxine relative to food/coffee/supplements rather than assuming perfect adherence | established | - | yes |
| `A2-H1-A1` | visible, not required (would count against) | Evidence shows that bedtime dosing gives no patient in either group (those not following label instructions, and those following them but still symptomatic) a better TSH or absorption than their own morning routine. | potential falsification: no benefit in any relevant subgroup | a study explicitly reporting that no participants (including relevant subgroups) improved TSH/absorption after switching to bedtime compared with their own morning routine | supported with assumption | - | yes |
| `A2-H1-A2` | visible, not required (would count against) | A switch to bedtime dosing commonly causes harm that a 6–8 week TSH recheck would not catch (e.g., clinically important problems occurring before monitoring or not reflected in TSH). | potential falsification: harms not mitigated by planned monitoring | a trial, cohort, or pharmacovigilance report showing frequent clinically significant harms after switching to bedtime that occur despite, or prior to, routine 6–8 week TSH monitoring | unaddressed | - | yes |
| `A2-H1-A3` | visible, not required (would count against) | Evidence shows that patients in both groups cannot keep an evening window clean (i.e., evening food, supplements, or other routine factors regularly prevent separated bedtime dosing). | potential falsification: feasibility of clean evening window | a survey or adherence study reporting that most patients (including those with problematic mornings and those otherwise adherent) cannot maintain adequate separation for bedtime levothyroxine | supported with assumption | - | yes |
| `A2-H1-A4` | visible, not required (would count against) | Evidence shows that correct label adherence (fasting, avoiding coffee, and separating from interfering drugs/supplements) rather than a timing change removes every symptom and every raised TSH in these patients. | potential falsification: fixing morning routine solves all cases | an intervention study showing that ensuring correct morning-label adherence normalizes TSH and resolves symptoms for all (or essentially all) patients in the defined refractory cohort | partial only | - | yes |
| `A2-H1-E1` | visible, not required (expected) | In adults who switch to bedtime dosing at the same levothyroxine tablet dose, thyroid labs (TSH and/or free T4) improve on average and/or a clinically meaningful subset improves. | corroboration: clinical lab improvement after bedtime switch | a timing trial or case series reporting improved TSH/free T4 after switching to bedtime at unchanged dose, either on average or in a defined responder subgroup | contested | - | yes |
| `A2-H1-E2` | visible, not required (expected) | After a bedtime switch, patients who were taking levothyroxine near morning coffee/food/supplements and symptomatic report or show improvement (symptoms, quality of life, or related patient-reported outcomes). | corroboration: patient-centered improvement in the nonadherent-morning group | a trial, observational study, or case series reporting symptom/QoL improvement after switching to bedtime in patients whose morning routine placed coffee/food/supplements near the dose | supported with assumption | - | yes |
| `A2-H1-E3` | visible, not required (expected) | Patient surveys show that many patients take levothyroxine near breakfast, coffee, or supplements, or report the morning fasting requirement as burdensome. | corroboration: real-world need/feasibility driver for offering an option | a patient survey or real-world adherence study quantifying how often levothyroxine is taken near breakfast/coffee/supplements or reporting difficulty with morning fasting instructions | established | - | yes |
| `A2-H1-E4` | visible, not required (expected) | Few adverse events are reported with bedtime dosing in timing trials or observational reports. | corroboration: low observed harm profile | a timing trial or observational study reporting low rates of adverse events with bedtime dosing | supported with assumption | - | yes |

#### How the text was read

The solver requires every "must be supported" unit together (a conjunction); alternatives inside one unit count as one requirement. That is how the text was compiled for the solver, not a finding that the text means it.

- Sentence 4 was read as requiring ALL of: `A2-H1-R3`, `A2-H1-R4`.
- All 5 active required units must be covered for complete coverage.
- Why each sentence was divided as it was: NOT RECORDED (the unit compiler returns no rationale).

#### Not requirements

These are judged in the final assessment, not by witness matching.

- `A2-H1-J1` Patients should be offered the option of taking the same levothyroxine tablet at bedtime and be encouraged to consider, ask about, and discuss this option with their clinician; it is presented as especially applicable to (i) patients who do not follow label instructions (e.g., drink coffee within one hour of waking) and have hypothyroid symptoms, and (ii) patients who do follow label instructions but still have hypothyroid symptoms; the switch is described as same tablet/same dose, low cost beyond follow-up TSH testing, reversible, and low risk with a 6–8 week recheck.

#### What complete coverage of this hypothesis would let a reader conclude

State in this run: **COMPLETE_WITH_ASSUMPTIONS**; 2 of 5 required parts have a direct match, 3 only with a transfer; 120 minimal set(s).

It means:

- Each of the 5 parts listed as "must be supported" is made true by at least one released witness, accepted as written, or under a transfer the set names.
- No witness in the set is known to contradict a listed premise outright. "No known contradiction" is not "shown to hold": a premise nobody tested is not thereby satisfied.
- The set contains no pair of witnesses approved as incompatible.
- As it stands, the example set grants 3 transfer(s) for support and assumes 0 contrary finding(s) from another scope do not transfer. Coverage holds only if those are accepted.

It does not mean:

- that the hypothesis is true, or that its rivals are false;
- that the judgments listed under "Not requirements" are right: those are made in the final assessment;
- that the adverse tests came out negative: they are shown, not required;
- that the witnesses are independent studies (see the study map), or that the studies are sound;
- that the units are a faithful reading of the hypothesis: check that against the sentences above.

#### Worth a look

Mechanical hints; none of them changes a result.

- `A2-H1-R1` is a requirement, but its anchor is in the "Potential corroboration" text, which says what would be expected or would count against, not what the hypothesis asserts. Check that the hypothesis needs it.
- `A2-H1-R2` is a requirement, but its anchor is in the "Potential corroboration" text, which says what would be expected or would count against, not what the hypothesis asserts. Check that the hypothesis needs it.
- `A2-H1-R5` is a requirement, but its anchor is in the "Potential corroboration" text, which says what would be expected or would count against, not what the hypothesis asserts. Check that the hypothesis needs it.
- `A2-H1-R4` is anchored on 3 words; the unit compiler is asked for at least six, so most of this unit's content is the compiler's elaboration.
- Content words each required unit uses that its anchor sentence does not (a rough count of how far the unit was elaborated, not a judgment): `A2-H1-R1` 15, `A2-H1-R2` 15, `A2-H1-R3` 14, `A2-H1-R5` 14, `A2-H1-R4` 9.

### A2-H2 - Follow the morning instructions instead

2 required, 2 constraint, 3 adverse-test, 3 expected and 1 evaluative unit(s).

This is the compiled theory the crux tests are run against when a witness of A2-H1, A2-H3 is tested against A2-H2.

#### The hypothesis as written, and what each sentence produced

*Statement*

1. No. The studies show no patient benefits from bedtime dosing beyond what following the morning instructions achieves: fasting, no coffee, no PPI or multivitamin near the dose.
   - `A2-H2-R1` (must be supported), anchored on: "The studies show no patient benefits from bedtime dosing beyond what following the morning instructions achieves"
   - `A2-H2-C1` (must not be contradicted), anchored on: "beyond what following the morning instructions achieves: fasting, no coffee, no PPI or multivitamin near the dose"
   - `A2-H2-J1` (not a requirement (judged in the final assessment)), anchored on: "No. The studies show no patient benefits from bedtime dosing beyond what following the morning instructions achieves"
2. Patients should follow those instructions instead.
   - *no unit*

*Assumptions and antecedents*

3. Patients can and do follow the morning instructions; following them removes the interference completely; no group of patients has a morning schedule that fails them.
   - `A2-H2-R2` (must be supported), anchored on: "following them removes the interference completely; no group of patients has a morning schedule that fails them"
   - `A2-H2-C2` (must not be contradicted), anchored on: "Patients can and do follow the morning instructions"

*Potential falsification*

4. Evidence that a meaningful share of patients do not or cannot follow the morning instructions.
   - `A2-H2-A2` (visible, not required (would count against)), anchored on: "Evidence that a meaningful share of patients do not or cannot follow the morning instructions."
5. Any trial or case series in which bedtime dosing did better than the patient's own morning routine.
   - `A2-H2-A1` (visible, not required (would count against)), anchored on: "Any trial or case series in which bedtime dosing did better than the patient's own morning routine."
6. A guideline that endorses bedtime dosing as an option.
   - `A2-H2-A3` (visible, not required (would count against)), anchored on: "A guideline that endorses bedtime dosing as an option."

*Potential corroboration*

7. Trials in which bedtime dosing was worse than a correctly fasted morning dose.
   - `A2-H2-E1` (visible, not required (expected)), anchored on: "Trials in which bedtime dosing was worse than a correctly fasted morning dose."
8. Evidence that correcting the morning routine achieves everything bedtime dosing achieves, for every kind of patient.
   - `A2-H2-E2` (visible, not required (expected)), anchored on: "Evidence that correcting the morning routine achieves everything bedtime dosing achieves, for every kind of patient."
9. Evidence of harm from switching to bedtime.
   - `A2-H2-E3` (visible, not required (expected)), anchored on: "Evidence of harm from switching to bedtime."

**Written by you, checked by nothing.** No unit is anchored on these sentences, so neither coverage nor the crux tests see them: sentence 2.

#### Requirements

| Unit | Role | Text | Serves | Satisfied by | State | Options | Active |
|---|---|---|---|---|---|---|---|
| `A2-H2-R1` | must be supported | In adults on levothyroxine tablet monotherapy with persistently above-target TSH (the refractory cohort), switching from their existing morning routine to taking the same tablet at bedtime at the same dose does not improve TSH or thyroid hormone measures (free T4 and/or T3) in any patients beyond what correct morning label adherence would achieve. | core claim: no incremental benefit from bedtime dosing | a trial or case series in the refractory cohort comparing morning vs bedtime at the same dose, showing no individuals (or no subgroup) improve on bedtime compared with what correct morning adherence provides | supported with assumption | 0 direct, 2 with a transfer | yes |
| `A2-H2-R2` | must be supported | Among refractory-cohort adults on levothyroxine tablets, following the morning label instructions (fasting and separation from interfering items) eliminates timing-related interference such that a morning schedule does not fail any group of patients. | assumptions/antecedents needed for 'follow morning instructions instead' | a study in refractory patients showing that enforcing/achieving correct morning administration resolves elevated TSH (and/or improves free T4) without needing bedtime dosing | supported with assumption | 0 direct, 9 with a transfer | yes |
| `A2-H2-C1` | must not be contradicted | The relevant comparison is bedtime dosing versus correct morning label adherence (fasting, no coffee, and avoiding PPIs or multivitamins near the dose), not bedtime dosing versus an improperly taken morning dose. | comparison definition | a study design or analysis that explicitly defines and verifies correct morning-administration conditions when comparing to bedtime dosing | partial only | - | yes |
| `A2-H2-C2` | must not be contradicted | The hypothesis presumes patients can and do follow the morning instructions (fasting and separation from coffee/PPIs/multivitamins near the dose). | assumptions/antecedents boundary | an adherence/feasibility study or trial run-in demonstrating that patients in this cohort can and do comply with the morning instructions | partial only | - | yes |
| `A2-H2-A1` | visible, not required (would count against) | A trial or case series reports that bedtime dosing at the same dose yields better TSH (or higher free T4) than the patient's own morning routine in refractory-cohort adults. | potential falsification: bedtime better than own morning routine | a within-subject or cross-over timing study in refractory patients reporting improved thyroid labs after switching to bedtime without dose increase | supported with assumption | - | yes |
| `A2-H2-A2` | visible, not required (would count against) | A study finds that a meaningful share of patients do not or cannot follow the morning instructions (fasting and separation from coffee/PPIs/supplements). | potential falsification: morning adherence not feasible for many | a patient survey, observational study, or trial adherence report quantifying inability/nonadherence to required morning timing/separation | established | - | yes |
| `A2-H2-A3` | visible, not required (would count against) | A guideline or product label endorses bedtime dosing as an acceptable option for levothyroxine tablets. | potential falsification: endorsed option contradicts 'should not be offered' | a clinical guideline or manufacturer label statement explicitly allowing or recommending bedtime dosing | established | - | yes |
| `A2-H2-E1` | visible, not required (expected) | In a controlled comparison where the morning condition is correctly fasted and separated from interferents, bedtime dosing produces worse thyroid control (e.g., higher TSH or lower free T4) than morning dosing at the same dose. | potential corroboration: bedtime worse than correctly fasted morning | a randomized or cross-over timing trial that verifies correct morning administration and reports worse outcomes on bedtime dosing | supported with assumption | - | yes |
| `A2-H2-E2` | visible, not required (expected) | Correcting the morning routine (fasting and separation from coffee/PPIs/multivitamins/calcium/iron near the dose) achieves the same improvements in TSH or thyroid hormone measures that bedtime dosing achieves, across patient types. | potential corroboration: morning correction matches bedtime gains for all | a study showing that enforcing correct morning dosing yields improvements comparable to those seen with bedtime dosing, without residual subgroup benefit from bedtime | supported with assumption | - | yes |
| `A2-H2-E3` | visible, not required (expected) | Switching to bedtime dosing causes harm (e.g., over-replacement, worsened adherence, sleep problems, or evening food/supplements interfering) in a way that makes the switch a worse overall choice than simply following morning instructions. | potential corroboration: harms from switching to bedtime | an RCT, cohort study, or pharmacovigilance report linking bedtime dosing to adverse outcomes or adherence deterioration versus morning dosing | supported with assumption | - | yes |

#### How the text was read

The solver requires every "must be supported" unit together (a conjunction); alternatives inside one unit count as one requirement. That is how the text was compiled for the solver, not a finding that the text means it.

- All 2 active required units must be covered for complete coverage.
- Why each sentence was divided as it was: NOT RECORDED (the unit compiler returns no rationale).

#### Not requirements

These are judged in the final assessment, not by witness matching.

- `A2-H2-J1` Patients should not be offered bedtime dosing as an option; instead, they should follow the morning instructions (fasting, no coffee, and avoiding PPIs or multivitamins near the dose) because bedtime offers no additional benefit.

#### What complete coverage of this hypothesis would let a reader conclude

State in this run: **COMPLETE_WITH_ASSUMPTIONS**; 0 of 2 required parts have a direct match, 2 only with a transfer; 18 minimal set(s).

It means:

- Each of the 2 parts listed as "must be supported" is made true by at least one released witness, accepted as written, or under a transfer the set names.
- No witness in the set is known to contradict a listed premise outright. "No known contradiction" is not "shown to hold": a premise nobody tested is not thereby satisfied.
- The set contains no pair of witnesses approved as incompatible.
- As it stands, the example set grants 2 transfer(s) for support and assumes 0 contrary finding(s) from another scope do not transfer. Coverage holds only if those are accepted.

It does not mean:

- that the hypothesis is true, or that its rivals are false;
- that the judgments listed under "Not requirements" are right: those are made in the final assessment;
- that the adverse tests came out negative: they are shown, not required;
- that the witnesses are independent studies (see the study map), or that the studies are sound;
- that the units are a faithful reading of the hypothesis: check that against the sentences above.

#### Worth a look

Mechanical hints; none of them changes a result.

- Content words each required unit uses that its anchor sentence does not (a rough count of how far the unit was elaborated, not a judgment): `A2-H2-R1` 25, `A2-H2-R2` 13.

### A2-H3 - The evidence cannot decide

0 required, 1 constraint, 1 adverse-test, 2 expected and 1 evaluative unit(s).

This is the compiled theory the crux tests are run against when a witness of A2-H1, A2-H2 is tested against A2-H3.

#### The hypothesis as written, and what each sentence produced

*Statement*

1. The evidence does not allow a decision between A2-H1 and A2-H2.
   - `A2-H3-J1` (not a requirement (judged in the final assessment)), anchored on: "The evidence does not allow a decision between A2-H1 and A2-H2."

*Assumptions and antecedents*

2. The main timing trials, the absorption studies, the patient surveys, and the guideline and label statements on timing have been retrieved.
   - `A2-H3-C1` (must not be contradicted), anchored on: "The main timing trials, the absorption studies, the patient surveys, and the guideline and label statements on timing have been retrieved."

*Potential falsification*

3. Consistent evidence in either direction, from trials, absorption studies and surveys together.
   - `A2-H3-A1` (visible, not required (would count against)), anchored on: "Consistent evidence in either direction, from trials, absorption studies and surveys together."

*Potential corroboration*

4. Results that contradict each other and cannot be reconciled.
   - `A2-H3-E1` (visible, not required (expected)), anchored on: "Results that contradict each other and cannot be reconciled."
5. No evidence on how patients actually take their morning dose, or on the harms of switching.
   - `A2-H3-E2` (visible, not required (expected)), anchored on: "No evidence on how patients actually take their morning dose, or on the harms of switching."

Every sentence has at least one unit anchored on it.

#### Requirements

| Unit | Role | Text | Serves | Satisfied by | State | Options | Active |
|---|---|---|---|---|---|---|---|
| `A2-H3-C1` | must not be contradicted | The body of evidence considered includes the main timing trials, absorption studies, patient surveys, and guideline and label statements on timing. | antecedent condition (what has been retrieved/considered) | a methods/review statement documenting retrieval/consideration of timing trials, absorption studies, patient surveys, and guidelines/labels on dosing time | partial only | - | yes |
| `A2-H3-A1` | visible, not required (would count against) | Across trials, absorption studies, and surveys taken together, the results are consistent in one direction (either clearly favoring offering bedtime dosing or clearly favoring morning-instruction adherence), such that a decision between the two becomes possible. | potential falsification (consistent evidence in either direction) | a published synthesis (or a single study explicitly integrating multiple evidence streams) reporting that timing trials + absorption studies + surveys converge consistently toward one option | contradicted | - | yes |
| `A2-H3-E1` | visible, not required (expected) | Results from the relevant trials, absorption studies, and surveys contradict each other and cannot be reconciled. | potential corroboration (irreconcilable contradictions) | a review or comparative discussion that documents materially conflicting findings across timing trials/absorption studies/surveys and states they cannot be reconciled | partial only | - | yes |
| `A2-H3-E2` | visible, not required (expected) | There is no evidence describing how patients actually take their morning levothyroxine dose and/or no evidence describing harms of switching dosing to bedtime. | potential corroboration (missing evidence on morning behavior or harms) | a paper or review explicitly noting absence of evidence on real-world morning dosing behavior and/or absence of evidence on harms/adverse effects of switching to bedtime dosing | unaddressed | - | yes |

#### How the text was read

The solver requires every "must be supported" unit together (a conjunction); alternatives inside one unit count as one requirement. That is how the text was compiled for the solver, not a finding that the text means it.

- Why each sentence was divided as it was: NOT RECORDED (the unit compiler returns no rationale).

#### Not requirements

These are judged in the final assessment, not by witness matching.

- `A2-H3-J1` The evidence available does not allow choosing between offering bedtime dosing as an option and advising patients to follow the morning instructions instead.

#### What complete coverage of this hypothesis would let a reader conclude

State in this run: **NO_REQUIRED_UNITS**.

It means:

- This hypothesis has no finding-sized requirement of its own, so there is nothing for witnesses to cover. It holds to the extent its rivals' required parts stay uncovered or contested.

It does not mean:

- that the hypothesis is true, or that its rivals are false;
- that the judgments listed under "Not requirements" are right: those are made in the final assessment;
- that the adverse tests came out negative: they are shown, not required;
- that the witnesses are independent studies (see the study map), or that the studies are sound;
- that the units are a faithful reading of the hypothesis: check that against the sentences above.

