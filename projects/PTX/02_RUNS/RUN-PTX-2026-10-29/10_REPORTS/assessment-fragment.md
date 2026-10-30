---
artifact_type: CUMULATIVE-ACH-FUSION-FRAGMENT
schema_version: ACH-EVAL-NLM-1.0
prompt_id: ACH_Eval_NLM_Super_patched_min
base_prompt: ACH_Eval_v6.1
evidence_contract: notebooklm_and_dcp
gauge: 64
allocation_rule: normalized_units
fixed_additions: [0, 0, 0]
investigation_id: RUN-PTX-2026-10-29
fragment_id: RUN-PTX-2026-10-29-r1
revision: 1
parents: none
sibling_runs: none
status: open
frame_versions: A1 v1 (approved); A2 v1 (test_only, enabled)
axes_enabled: 2
run_mode: initial
self_contained: true
required_base: none
input_processing: complete-for-supplied-inputs
carry_forward_fidelity: complete
---

# Part A — Cumulative Fusion state

## 1. Foundation

**Research question / goal.** Does the existing mechanistic evidence make a compelling case that PTX can address an *untreated* cause of impaired voiding in this cohort, and therefore warrants a targeted clinical trial?

**Cohort (frame).** Men with BPH, shy bladder (paruresis) and difficulty voiding, with inadequate benefit from tamsulosin and failed or abandoned prescribed pelvic-floor treatment. The cohort is heterogeneous: possible contributors include bladder-outlet obstruction, detrusor underactivity/ischemic-remodeling, and a psychogenic/coordination (paruresis / pseudodyssynergia) component.

**Evidence contract / provenance.** All supplied findings arrive as *validated witnesses* (explicit source-fidelity check against the named file); each is treated as provenance **V** at the scope its text states. Coverage-set and crux results are machine records (**M**): they state which witnesses the frozen representation needs and which rivals cannot accommodate, not additional evidence. Initial assessment under this contract: **no prior comparable vector.**

**Essential distinctions / conventions carried.**
- Trial *warrant* (supported premises sufficient to specify an informative test) vs *demonstrated efficacy*. Completion of the proposed study is not a prerequisite for warranting it.
- Functional (perfusion/microcirculation/smooth-muscle/neural) vs structural (fibrosis/remodeling) mechanism; *treatment of established* dysfunction vs *prevention/pretreatment*.
- Electrically-evoked (neurogenic) vs carbachol-induced (muscarinic-max) detrusor contractility.
- Storage symptoms (urgency/frequency/incontinence) vs voiding/emptying (Qmax, PVR, initiation).
- Add-on (PTX + tamsulosin) vs monotherapy; cointervention (vitamin E) explicit.
- Transfer: cerebral / skin / renal / sepsis / depression models vs bladder-voiding in these men.
- Four trial-specification slots: (a) intervention & exposure, (b) phenotype, (c) measurement, (d) comparator.

**Full verbatim operative axes and hypotheses.**

AXIS A1 (APPROVED): Does the existing mechanistic evidence make a compelling case that PTX can address an untreated cause of impaired voiding in this cohort—and therefore warrants a targeted clinical trial?

A1-H1: The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men. Their persistent difficulty includes a reversible physiological component that tamsulosin and their prescribed pelvic-floor intervention do not adequately address. PTX or its metabolites can act on that component at clinically attainable exposures. The supported premises and their discriminating predictions are sufficient to specify intervention, phenotype, measurement, and comparator for a targeted clinical trial, whether or not every intermediate link is resolved.
Assumptions and antecedents: The relevant dysfunction occurs in this cohort; the proposed drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function. Any necessary contribution from vitamin E or another cointervention is explicit.
Potential falsification: Relevant exposure is unattainable; the proposed target is absent or incidental; target modulation fails to improve the relevant function under informative conditions; or stronger evidence breaks a link necessary to every route that is not speculative.
Potential corroboration: Converging findings connect attainable exposure, target engagement, physiological improvement, and relevant function. Timing, dose-response relationships, response predictors, and contrary results discriminate this explanation from alternatives. The evidence identifies measurable patient characteristics and trial outcomes that should reveal benefit. H1 is supported when the four trial-specification elements form a coherent, source-grounded test of a materially supported therapeutic rationale that survives serious adverse testing. Merely filling the elements is insufficient; unresolved links are permissible when the proposed experiment can discriminate them.

A1-H2: H1 is wrong because PTX's reported biological effects do not translate into a meaningful remedy for the dysfunction driving impaired voiding in this cohort. Affirmative evidence demonstrates a consequential mismatch in exposure, tissue, disease process, timing, or the relationship between a biological marker and urinary function—and that mismatch defeats the materially supported rationale, not merely one route among many. Favorable findings therefore do not provide the proposed causal justification for this intervention.
Assumptions and antecedents: The evidence demonstrating the mismatch is sufficiently relevant to test H1; failure in an unrelated model or exposure does not suffice. H2 targets the materially supported rationale as it currently stands in the ledger, not every route that could be imagined.
Potential falsification: A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
Potential corroboration: Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link. Missing clinical trials alone do not corroborate H2. Breaking one route among several independently supported routes damages that route in proportion to the share of the case it carried; it does not by itself corroborate H2.

A1-H3: Existing evidence supports some components of H1 but cannot distinguish a therapeutically consequential mechanism from the failure described by H2. The unresolved links prevent the rationale from becoming specific enough to design the trial: at least one of intervention and exposure, phenotype, measurement, or comparator cannot be specified from supported premises. The uncertainty is localized to identified links, and neither a compelling mechanistic endorsement nor a mechanistic rejection is presently determined.
Assumptions and antecedents: Meaningful retrieval and adverse testing have been completed; uncertainty is not merely an artifact of an unfinished investigation.
Potential falsification: Evidence resolves the decisive links sufficiently to fill all four trial-specification slots (favoring H1) or to defeat the supported rationale (favoring H2).
Potential corroboration: Plausible competing explanations remain compatible with the observations because relevant exposure, tissue effects, functional consequences, or response predictors are unmeasured or inadequately distinguished, and the resulting gap blocks at least one of the four specification slots. The investigation identifies the experiment that would resolve that uncertainty. Record which slot is blocked and by which link.

AXIS A2 (TEST_ONLY): If PTX can improve voiding in this cohort, is the proposed benefit predominantly a rapid functional effect or a slow structural recovery?

A2-H1: The materially supported mechanism acts on current physiological function—such as perfusion, microcirculation, smooth-muscle behavior, or neural signaling—rather than on established tissue structure. At clinically attainable exposures, PTX or its metabolites should produce measurable improvement in voiding within days to a few weeks, and benefit should diminish if treatment stops.
Assumptions and antecedents: A functional component of impaired voiding is present and modifiable in this cohort; attainable exposure reaches the relevant tissue quickly enough to act within the proposed window.
Potential falsification: Relevant models show no early functional change at informative exposures; human benefit, where reported, appears only after prolonged treatment; or the supported route requires structural change before function can improve.
Potential corroboration: Functional endpoints such as contractility or flow improve early after exposure; onset tracks dosing; benefit fades on withdrawal; and early change is not explained by concurrent structural recovery.

A2-H2: The materially supported mechanism acts by reversing or limiting structural change—such as fibrosis, remodeling, or other tissue damage—that contributes to impaired voiding. Meaningful improvement should appear only after weeks to months of treatment, with little early functional change, and may persist after treatment stops.
Assumptions and antecedents: Structural change contributes consequentially to impaired voiding in this cohort, and PTX can reverse or limit that change rather than merely prevent it.
Potential falsification: Structural effects appear only when treatment precedes injury (prevention, not reversal); structural improvement does not accompany functional improvement; or meaningful benefit appears too quickly to be structurally mediated.
Potential corroboration: Structural endpoints such as stereology or collagen measures improve with treatment of established dysfunction; functional improvement follows structural change in time; benefit accumulates with duration and persists after withdrawal. Evidence limited to prevention models does not by itself support A2-H2.

A2-H3: Existing evidence cannot distinguish rapid functional benefit from slow structural recovery. Timing evidence is unmeasured, conflicting, poorly transferable, or compatible with both, so the expected onset and persistence of benefit cannot be specified from supported premises. The uncertainty is localized to identified timing links.
Assumptions and antecedents: Meaningful retrieval and adverse testing of timing evidence have been completed; uncertainty is not merely an artifact of an unfinished investigation.
Potential falsification: Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
Potential corroboration: Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort. Record which timing link is unresolved and what measurement would distinguish rapid from slow benefit.

**Intuitions / references.** User goal (patient-advocacy trial warrant) is distinguished from what the evidence supports. No human/model disagreement is invented.

## 2. Input / anchor register

All inputs are supplied validated witnesses (provenance V); disposition `integrated` unless noted. This-pass footprint = 47 source families across 40 named source files; cumulative = same (initial run). No inputs inaccessible or unprocessed. Machine records (coverage/crux) imported as M (continuity, not evidence).

| Source file | Witness IDs | Disposition |
|---|---|---|
| Comparison...tamsulosin...Pentoxifylline (Shirazi BPH RCT) | W-FRD-Q0001-01, W-FRD-Q0001-02-r3, W-FRD-Q0011-01, W-FRD-Q0048-01 | integrated |
| shirazi2015.pdf.md (rat pBOO) | W-FRD-SHIRAZI2015-01-Q0002, W-FRD-SHIRAZI2015-02-Q0002 | integrated |
| bowton1989.pdf.md | W-FRD-BOWTON-01-Q0006, W-FRD-BOWTON-02-Q0006 | integrated |
| nisi2013.pdf.md | W-FRD-Q0007-01 | integrated |
| roberts1993.pdf.md | W-FRD-Q0008-02 | integrated |
| delanian2003 / delanian2005 | W-FRD-Q0009-02, W-FRD-Q0009-03 | integrated |
| he2010.pdf.md | W-FRD-Q0004-01, W-FRD-Q0004-02 | integrated |
| kaplan1997.pdf.md | W-FRD-Q0017-01, W-FRD-Q0004-03-r2 | integrated |
| rademakers2016.pdf.md | W-FRD-RADEMAKERS-01, W-FRD-RADEMAKERS-02 | integrated |
| masterson2017 / anderson2011 | W-FRD-Q0005-01, W-FRD-Q0005-02 | integrated |
| MP75-18 (PFPT attendance) | W-FRD-Q0012-01 | integrated |
| s00210-025-03845-1 (Kassar PTX safety) | W-FRD-Q0013-01 | integrated |
| parker2000 / ridings1994 (porcine sepsis) | W-FRD-Q0015-01, W-FRD-Q0016-01 | integrated (transfer-limited) |
| Yu&Jeong 2020 / li2018 / chuang2015 / chung2016 (DU epi) | W-FRD-Q0020-01, W-FRD-Q0021-01, W-FRD-Q0053-01, W-FRD-Q0054-01 | integrated |
| clemens2000 / cornel2005 / fitzgerald2009 / vanreijn-baggen2022 (PFPT/biofeedback) | W-FRD-Q0022-01, W-FRD-Q0023-01, W-FRD-Q0025-01, W-FRD-Q0031-01 | integrated |
| immunology00076 (Neuner) / kruuse2000 / dezube1993 | W-FRD-Q0027-01, W-FRD-Q0028-01, W-FRD-Q0029-01 | integrated |
| raison2013 (infliximab TRD) | W-FRD-Q0033-01 | integrated (transfer-limited) |
| roerink2019 / shah2016 / vogel2023 / vanhouten2026 (Cushing's inflammation) | W-FRD-Q0034-01, W-FRD-Q0035-01, W-FRD-Q0041-01, W-FRD-Q0043-01 | integrated (context) |
| bortnick2019 / bortnick2020 (reviews) | W-FRD-Q0037-01, W-FRD-Q0040-01 | integrated (context) |
| fakioglu2004 (aminophylline) / spinas1991 (ibuprofen) | W-FRD-Q0042-01, W-FRD-Q0052-01 | integrated (class/transfer) |
| fukabori1996 (PTX bladder case) | W-FRD-Q0044-01 | integrated |
| gulen2024 (MCAS) | W-FRD-Q0045-01 | context |
| vale2019 (HIF/BOO review) | W-FRD-Q0046-01 | integrated |
| kim2017 / ladi-seyedian2017 (UAB pharmacology reviews) | W-FRD-Q0047-01, W-FRD-Q0050-01 | integrated |
| chung2014 (paruresis review) | W-FRD-Q0049-01 | integrated |
| wystrychowski2014 (renal ischemia timing) | W-FRD-Q0019-01 | integrated |
| glazener2011 / 11255_2025 / nihms-1048633 / siu2003 / stokes2022 (post-TURP & female PFMT) | W-FRD-Q0055-01, W-FRD-Q0056-01, W-FRD-Q0059-01, W-FRD-Q0061-01, W-FRD-Q0062-01 | integrated (transfer-limited) |


## 3. Evidence-family ledger

Compact cards; all provenance V at the scope stated. `Retained` = carried forward, not proven.

**F001 — Shirazi et al., single-centre randomized double-blind BPH/LUTS add-on trial (PTX 400 mg q8h + tamsulosin 0.4 mg/d vs placebo + tamsulosin, 12 wk; 30/arm, all analysed).**
- F001.a [observed] PVR fell more with combination: -32.93 +/- 16.33 vs -13.17 +/- 9.23 mL (p<.001). *Limit:* baseline PVR imbalanced 77.27 vs 50.37 mL (p=.18); add-on, not monotherapy. (W-FRD-Q0001-01)
- F001.b [analyst-derived] Qmax change 4.48 vs 2.67 mL/s; unadjusted difference 1.81 mL/s favouring PTX+tamsulosin (not a separately reported adjusted estimate; BPH add-on, not monotherapy/psychogenic). (W-FRD-Q0001-02-r3)
- F001.c [observed, null] Voided volume: no significant between-group change (0.80 vs +1.34 mL, p=.22); no significant within-group change (p=.90/.89). (W-FRD-Q0011-01)
- F001.d [method] Analysis by t-test / Wilcoxon / Mann-Whitney, alpha<=0.05; **no ANCOVA or baseline-PVR-adjusted model reported**; SD vs SE not stated. (W-FRD-Q0048-01)
- Status: retained; F001.a quarantined for baseline imbalance (G-01).

**F002 — Shirazi 2015, male Sprague-Dawley rat partial bladder outlet obstruction; PTX 100 mg/kg/d oral gavage x4 wk begun AFTER obstruction (treatment, not prevention); 20/group, all completed.**
- F002.a [observed, positive] Higher electrically-evoked isolated-detrusor-strip tension vs water controls: ~4.0 +/- 1.0 vs 1.8 +/- 0.4 g/100 mg tissue (P=0.023; figure-derived, approximate). (W-FRD-SHIRAZI2015-01-Q0002)
- F002.b [observed, null] No significant improvement in maximum carbachol-induced detrusor contractile tension vs obstructed controls. (W-FRD-SHIRAZI2015-02-Q0002)
- Status: retained. Key: effect is route-specific (neurogenic/evoked yes; muscarinic-max no). Bladder-specific functional treatment effect.

**F003 — Bowton 1989, prior-cerebrovascular-disease patients, single oral SR PTX, xenon-133 global CBF; no concurrent placebo arm.**
- F003.a [observed, positive] 800 mg (n=6): normocarbic global CBF rose 52.5 +/- 15.2 -> 59.4/58.2/62.4 mL/100g/min at 2/4/6 h (p<=0.01-0.02; overall p=0.017). Fast perfusion effect in a compromised bed. (W-FRD-BOWTON-01-Q0006)
- F003.b [observed, null] 400 mg (n=4): no significant overall increase (p=0.29; 101/101/110% of baseline). Dose threshold signal. (W-FRD-BOWTON-02-Q0006)
- Status: retained. Cerebral measured flow, not pelvic tissue.

**F004 — Nisi 2013, chronic-heart-failure patients, single 600 mg SR oral PTX, plasma PK (n=20).** Parent-PTX Tpeak 1.64 +/- 0.92 (NYHA II) vs 3.89 +/- 1.90 h (III/IV) (P=.0077); Cmax 719 +/- 403 vs 833 +/- 524 ng/mL (NS). Plasma only; no tissue/unbound/metabolite/half-life; not urinary-benefit timing. (W-FRD-Q0007-01) Status: retained.

**F005 — Roberts 1993, ex vivo whole blood, PTX 5 umol/L added (30-min preincubation).** FMLP-stimulated neutrophil intracellular oxidant (DCF H2O2) reduced to 76 +/- 5% of PTX-free response (n=10; p<0.025). Added parent-drug concentration, ex vivo; not plasma/metabolite exposure; no bladder response. (W-FRD-Q0008-02) Status: retained.

**F006 — Delanian, superficial radiation-induced fibrosis in women post-breast-RT; PTX 800 mg/d + vitamin E 1000 U/d.**
- F006.a [observed] 2003 RCT 2x2 factorial (24 eligible, 22 at 6 mo): combination -60.2% vs double-placebo -42.6% surface-area change (P=.038 Wilcoxon). **Two-way ANOVA: no significant main effects; only a PTX x vitamin-E interaction trend (P=.09).** (W-FRD-Q0009-02)
- F006.b [observed] 2005 follow-up: after stopping, fibrosis rebounded more after short (6-12 mo) than long (24-48 mo) treatment: 40%/yr (CI 24-56) vs 8.5%/yr (CI 1-16); P=.0012. Duration not randomized. Slow structural, duration-response, partial persistence. (W-FRD-Q0009-03)
- Status: retained. Requires vitamin E cointervention; skin, not bladder.

**F007 — He 2010, retrospective uncontrolled series, 21 men nonbacterial chronic prostatitis + dysfunctional voiding (EMG/fluoroscopic external-sphincter dyscoordination).** Qmax rose 8.2 (SD 4.1) -> 15.1 (SD 7.3) mL/s after ~10 wk relaxation/coordination biofeedback (P<0.05); meds suspended. No placebo control -> within-cohort change, not controlled effect. (W-FRD-Q0004-01, -02) Status: retained.

**F008 — Kaplan 1997, retrospective, 43 men pseudodyssynergia previously misdiagnosed as chronic nonbacterial prostatitis.** Success = >=50% AUA-symptom reduction on two consecutive visits (symptom response, not attendance/completion). After behaviour modification + biofeedback 35 (83%) responded; responders' mean AUA 18.4 -> 7.6 (3 mo), 8.1 (6 mo). (W-FRD-Q0017-01, W-FRD-Q0004-03-r2) Status: retained. Shows a coordination/behavioural component in a related male cohort responds to biofeedback.

**F009 — Rademakers 2016 narrative review (urodynamic nomograms).**
- F009.a Retrospective analysis attributed to Oelke, 786 treatment-naive men >=40 with LUTS: median BCI rose with obstruction grade 73 (Schaefer 0) -> 188 (grade 6); median Wmax 9.6 -> 23 W/m2; proposes grade-adjusted thresholds BCI<100, Wmax<7. Cross-sectional association. (W-FRD-RADEMAKERS-01)
- F009.b Hannover-Maastricht nomogram (Oelke, 822 treatment-naive men >=40): plots BOO index vs max Watts factor to classify outlet resistance and detrusor contractility simultaneously; <25th-percentile indicates detrusor underactivity relative to outlet resistance even with coexisting obstruction. Validation ongoing. (W-FRD-RADEMAKERS-02)
- Status: retained. Phenotyping instruments for slot (b).

**F010 — Masterson 2017, uncontrolled multimodal PFPT pilot, 14 men idiopathic CPPS; 10 completed 10 visits, 4 ongoing.** (W-FRD-Q0005-01) Status: retained (PFPT adherence/efficacy context).

**F011 — Anderson 2011, prospective open-label UCPPS self-treatment pilot; 113/157 (72%) completed 6 mo wand use (prescribed 3-4x/wk).** Completion not verified per-session adherence; not male-only clinic PFPT. (W-FRD-Q0005-02) Status: retained (context).

**F012 — MP75-18 retrospective chart review, male PFPT referrals (one clinic, 2022): 52/120 (43.3%) scheduled and attended >=1 visit.** Initial-attendance endpoint, not completion/abandonment/response. (W-FRD-Q0012-01) Status: retained (adherence context for "abandoned pelvic-floor treatment").

**F013 — Kassar systematic review/meta-analysis, 4 depression RCTs (318), PTX vs placebo all-cause discontinuation 14/159 vs 16/159; pooled RR 0.88 (CI 0.45-1.74; P=0.72); dosing 400 mg bid (one thrice), mostly SSRI add-on.** No long-term/alpha-blocker-specific safety. (W-FRD-Q0013-01) Status: retained. Tolerability support at the candidate oral dose.

**F014 — Parker 2000, randomized porcine haemorrhage+E.coli peritonitis (n=5/grp): PTX+colloid lower median 2-h MAP (62 vs 92 mmHg, P<0.01); equal by 6 h.** Acute resuscitation, not chronic oral. (W-FRD-Q0015-01) Status: retained (transfer-limited; hemodynamic caution).

**F015 — Ridings 1994, nonrandomized porcine Pseudomonas sepsis: IV PTX begun 2 h after infusion (established shock) followed by fatal hypotension within 1 h in 2/4; n=4 precludes statistics.** Untransferable to bladder. (W-FRD-Q0016-01) Status: retained (transfer-limited; timing/established-injury caution).

**F016 — Yu & Jeong 2020 review: most DU prevalence data from community cohorts with significant LUTS by arbitrary urodynamic criteria (25-48% elderly men, 12-24% women); community research rare, not absent.** (W-FRD-Q0020-01) Status: retained.

**F017 — Li 2018, single-centre retrospective, rehabilitation hospital: UAB cohort from 4,538 LUTS; 1,460/1,726 (84.6%) neurogenic UAB (etiologic distribution, not community prevalence).** No sex/age/criteria/prior-failure/shy-bladder data. (W-FRD-Q0021-01) Status: retained.

**F018 — Clemens 2000, 19 men CPPS, biofeedback-directed pelvic-floor re-education + bladder training x6 biweekly; 10 completed all six; follow-up covered 16.** (W-FRD-Q0022-01) Status: retained (context).

**F019 — Cornel 2005, uncontrolled pre/post, men type III CP/CPPS (31/33): NIH-CPSI micturition score 5.1 -> 2.2 after biofeedback/re-education (p<0.001).** Symptom scores, not flow/residual. (W-FRD-Q0023-01) Status: retained.

**F020 — FitzGerald 2009, randomized multicentre feasibility (47); male CP/CPPS subgroup (11 MPT, 10 global massage): NIH-CPSI urinary subscore change -3.9 vs -0.3 (Wilcoxon p=0.007), baselines imbalanced (8.9 +/- 1.4 vs 4.6 +/- 2.7); 10 weekly sessions; uroflow/PVR & prior PFPT history not reported.** Review-transmitted (van Reijn-Baggen 2022): pre-post P<.001, PFPT-vs-control P<.01, no between-group direction/magnitude, narrative "equal urinary improvement" (not independent replication). (W-FRD-Q0025-01, W-FRD-Q0031-01) Status: retained.

**F021 — Neuner, 4 healthy volunteers (two-day subgroup size unspecified): oral PTX 5x400 mg/d x2 d significantly suppressed TNF-alpha, IL-1beta, IL-6, IL-8 from day-7 PBMC (24-h culture, +/- LPS).** Ex vivo endpoints after in vivo dosing; plasma/tissue exposure & urinary efficacy unmeasured. (W-FRD-Q0027-01) Status: retained. In vivo-dosed target engagement.

**F022 — Kruuse 2000, double-blind crossover, 10 healthy subjects: PTX 300 mg IV vs saline, SPECT: no significant over-time change in MCA or global CBF (corrected or uncorrected); pCO2-corrected changes equal between treatments, uncorrected differed.** Healthy cerebral perfusion, not ischemic bladder. (W-FRD-Q0028-01) Status: retained. Contrast with F003: PTX perfusion effect appears in compromised, not healthy, beds.

**F023 — Dezube 1993, pilot, 7 cancer patients, 8 occasions, oral CR PTX 400 mg q8h x1-3 wk: on all 3 occasions with baseline PBMC TNF/beta-actin above normal, ratios fell within a week; on 5 within-range occasions, no reduction.** Target engagement, not clinical benefit. (W-FRD-Q0029-01) Status: retained.

**F024 — Raison 2013, 12-wk DBPC RCT, 60 treatment-resistant-depression outpatients: infliximab vs placebo, no significant overall HAM-D difference (t58=0.10, P=.92).** Nonsignificant, not proof of no benefit; infliximab for depression. (W-FRD-Q0033-01) Status: retained (transfer-limited; anti-cytokine-for-function analogy, negative).

**F025 — Cushing's persistent-inflammation set (context for "reversible physiological/inflammatory component" analogy; none bladder).**
- Roerink 2019 case-control: long-term Cushing's remission lower peak VO2 (28.0 +/- 7.0 vs 34.8 +/- 7.9 mL/kg/min, P<0.01). (W-FRD-Q0034-01)
- Shah 2016 (31): adiposity did not predict IL-6/IL-1beta in active disease or remission (nonassociations). (W-FRD-Q0035-01)
- Vogel 2023 (N=50): 3-mo postop CRP inversely associated with 12-mo normalized grip strength (rs=-0.371, P=.008); association, not mediation. (W-FRD-Q0041-01)
- van Houten 2026 (9): basal plasma IL-6/IL-8 no significant difference, CRP no trend, diagnosis vs remission. (W-FRD-Q0043-01)
- Status: retained as context; endocrine recovery, not bladder; mixed/weak support for a durable inflammatory-dysregulation premise.

**F026 — Bortnick reviews (context).** PDE5i contraindicated with nitrates (class guidance, interaction rationale, not quantified AE rate) (W-FRD-Q0037-01); alpha-blockers relax prostate/bladder-neck smooth muscle (alpha-1a) to relieve BOO (mechanism only) (W-FRD-Q0040-01). Status: retained.

**F027 — Class/pharmacodynamic transfer signals.** Fakioglu 2004: post-endotoxin IV aminophylline increased lung water in rats (81.41 vs 80.23%, P<0.05); serum unreported; class-transfer, not PTX-bladder (W-FRD-Q0042-01). Spinas 1991: ibuprofen pretreatment raised endotoxin TNF-alpha (627 vs 369 pg/mL) and IL-6 in healthy men -> anti-inflammatory pretreatment can paradoxically raise cytokines (W-FRD-Q0052-01). Status: retained (transfer-limited cautions).

**F028 — Fukabori 1996, single case (English abstract), 60-yo woman, uninhibited bladder (urge incontinence, pollakisuria, urodynamic uninhibited contractions): after failed anticholinergic, PTX (dose/route unstated) resolved incontinence and reduced pollakisuria by 2 wk; contractions absent, capacity increased by 4 wk.** Storage symptoms only; single case; not comparative; not voiding/emptying. (W-FRD-Q0044-01) Status: retained. Only direct human PTX-on-bladder observation; fast-ish onset (2-4 wk) but wrong symptom domain.

**F029 — Gulen 2024 MCAS diagnostic criteria review.** No bladder or PTX outcome. (W-FRD-Q0045-01) Status: context/noise for this question.

**F030 — Vale 2019 review (HIF/ischemia in BOO).** In BOO mice, daily 17-DMAG (pharmacological HIF-pathway inhibition) improved BOO morphology, suppressed HIF target genes, seemed to improve stimulated contractility (attrib. Iguchi/Malykhina/Wilcox 2016). Review-transmitted preclinical; implicates HIF/ischemia, not direct PTX. (W-FRD-Q0046-01) Status: retained. Supports a reversible ischemic/remodeling target in the bladder.

**F031 — UAB pharmacology reviews (unmet need).** Kim 2017: parasympathomimetics not supported for UAB; conflicting results; relays Barendrecht's negative conclusion (W-FRD-Q0047-01). Ladi-Seyedian 2017: some distigmine studies found no significant difference vs placebo (endpoints/sizes unspecified; review-transmitted) (W-FRD-Q0050-01). Status: retained. Establishes unmet need + difficulty of the target.

**F032 — Chung 2014 review: paruresis = psychogenic inhibition of micturition (cites Boschen 2008); may contribute to UAB long-term.** Review-level proposed mechanism, not demonstrated causation/prevalence/response. (W-FRD-Q0049-01) Status: retained. Directly relevant: the cohort's "shy bladder" component is characterized as psychogenic.

**F033 — Wystrychowski 2014, 58 male Sprague-Dawley rats, solitary-kidney 45-min warm ischemia: SC PTX 100 mg/kg vs saline improved 48-h creatinine clearance ONLY when given 60 min BEFORE ischemia (P<.001), NOT 1 min into ischemia or 60 min post-release.** Acute model; within-timing. (W-FRD-Q0019-01) Status: retained. Key adverse-timing signal: PTX protective as pretreatment, not as rescue of established injury.

**F034 — Population / epidemiology.** Chuang 2015 (secondhand from Jeong): among 1,179 adults >65 with non-neurogenic voiding dysfunction, ">40.2%" of men had DU (BCI<100); 1,179 is mixed-sex total, male denominator not supplied (W-FRD-Q0053-01). Chung 2016 (Rule population sample): men in their 70s, annual PVR change -3% (CI -19-19%), not significant; population-level, not treatment response (W-FRD-Q0054-01). Status: retained.

**F035 — Post-TURP & female PFMT (transfer-limited for male emptying).** Glazener 2011 (442 men, post-TURP incontinence): PFMT+bladder training vs standard care, 12-mo any incontinence 65% vs 62%, adjusted RR 1.06 (CI 0.91-1.23, p=0.47) -> no benefit; post-surgical leakage, not difficult emptying (W-FRD-Q0055-01). 11255_2025 (180 men post-TURP): HBM-PFMT+standard vs standard continence 37.35% vs 24.74%, P=0.067 (ns); combination, not emptying/monotherapy (W-FRD-Q0056-01). Brown (female urogyn, 335): same-day PT -> higher attendance (91 vs 61%, p<0.001) but equal completion (49 vs 41%, p=0.15) (W-FRD-Q0059-01). Siu 2003 (214 women SUI): dropouts had higher baseline strength (W-FRD-Q0061-01). Stokes 2022 (OPAL, women SUI/MUI): diary-return counts, not completion/response (W-FRD-Q0062-01). Status: retained; limited transfer to male voiding nonresponse/abandonment.


## 4. Gaps, conflicts, corrections

| G-ID | Affected findings | Exact issue | Status | Targeted query / resolving observation |
|---|---|---|---|---|
| G-01 | F001.a (PVR), F001.d | Baseline PVR imbalanced (77 vs 50 mL, p=.18) and no ANCOVA / baseline-adjusted model reported, so the between-group PVR effect is not baseline-equivalent. **Decision-blocking** for the strongest human signal. | blocked (within source: W-FRD-Q0048-01 states no adjusted model exists) | Request baseline-adjusted (ANCOVA) PVR/Qmax from the trial, or an independent monotherapy RCT; mechanistic data cannot resolve. |
| G-02 | A1-H1-R4; F003/F004/F021/F022 | No witness measures PTX exposure or a pharmacodynamic marker in bladder/prostate/pelvic tissue at oral doses. Perfusion (F003) is cerebral; PK (F004) is plasma only; target engagement (F021/F023) is PBMC. Bladder-tissue exposure is inferred, not shown. | open | NLM query for PTX tissue concentration or perfusion/inflammatory PD marker in lower-urinary-tract tissue; likely absent -> name as missing. |
| G-03 | A1-H1-R7 (phenotype); F009, F034 | Phenotyping instruments (BCI/Wmax) exist, but no witness links any measurable baseline characteristic to PTX voiding response. The "PTX-responsive subgroup" is hypothesized, not supported. | open | NLM query for PTX response-predictor in LUTS/DU; route likely blocked -> fold into trial design. |
| G-04 | A1-H1-R5; F002, F001, F028 vs F032 | Cohort-mechanism match: bladder-positive evidence is obstruction/pBOO/BPH; the cohort is defined partly by paruresis (psychogenic, F032) and PFPT-failure. Whether PTX's mechanism reaches the dysfunction driving THESE men's difficulty is unresolved. | open | Characterize the dominant voiding-dysfunction phenotype in the target men (urodynamics: DU vs BOO vs dyscoordination). |
| G-05 | A2 all; F002, F003, F006, F033, F028 | Timing: fast functional (F003 hours; F021 2 d; F028 2-4 wk, storage) vs slow structural (F006 months, duration-response/persistence) effects are in different tissues; bladder data (F002) is a single 4-wk endpoint with no onset or withdrawal kinetics; F033 shows prevention-not-rescue. Onset/persistence of any bladder-voiding benefit is unspecified. | open | A time-course bladder study with on-treatment and post-withdrawal functional endpoints. |
| G-06 | F002.b, F001.c | Functional nulls (carbachol-max contractility; voided volume) coexist with functional positives (evoked contractility; PVR). Which functional outcome, if any, tracks voiding benefit is unresolved. | open | Pre-specify the primary functional outcome and confirm against an independent cohort. |

Conflict notes. F002.a (positive evoked) vs F002.b (null carbachol-max): same source, different outcomes -> both retained, route-specific; not a contradiction. F003 (positive, compromised bed) vs F022 (null, healthy bed): reconciled by tissue state, not a conflict. F033 (prevention-only) partially conflicts with F002/F006 (treatment of established dysfunction): retained as a timing/established-injury caution across models. No disputed detail is settled by majority; no corrected value invented.


## 5. Pass changes and freeze

Initial run under the NotebookLM/DCP contract; no prior fragment, so no verbatim Part A carry-forward was required and none was shortened. All 47 supplied witnesses integrated once as V-coded findings; no supersessions. Superseded/inactive cards: none. Carry-forward fidelity: complete (no inherited content to lose). Omitted material: none inspected-but-omitted; no inputs inaccessible/unprocessed. Decision-blocking issue flagged: G-01 (prioritized in section 9). Stage A frozen before Stage B. Machine coverage/crux records imported as M for continuity only (they report NO_COMPLETE_COVERAGE / NOT_RUN across all hypothesis units and are not treated as evidence for any allocation).


# Part B — Attached ACH report

## 6. Frame and diagnostic map

Two axes enabled. A1 (approved) asks whether the mechanistic record warrants a targeted PTX trial in this cohort. A2 (test_only, conditional on PTX working) asks whether the supported mechanism is fast-functional or slow-structural. A2 is a genuinely distinct question that cannot fit inside A1's rivals (it concerns the *character and timing* of a benefit A1 only conditionally grants), so Axis 2 is warranted; its allocation is read against the same frozen record and is not multiplied with A1.

Full frame and verbatim hypotheses are in Part A section 1. Selective diagnostic map (reads the frozen record, not prior allocations):

| Finding IDs | Axis / condition | Effect | Why diagnostic | Main limitation |
|---|---|---|---|---|
| F002.a | A1 (R4/R5), A2 | H1 | Only bladder-specific functional improvement from PTX as *treatment of established* obstruction (evoked detrusor tension, P=.023) | Rat pBOO; figure-derived; obstruction model, not paruresis cohort |
| F001.a / F001.b | A1 (R5) | H1 | Human BPH signal: PVR fell more, Qmax rose, with PTX add-on | Baseline PVR imbalance (G-01); add-on not monotherapy; unadjusted |
| F030 | A1 (R1) | H1 | Independent bladder evidence that HIF/ischemia/remodeling is a reversible BOO target | Review-transmitted; 17-DMAG, not PTX |
| F003.a vs F022 | A1 (R4), A2-H1 | H1 | PTX raises perfusion in a compromised bed within hours; null in healthy bed -> targets ischemia, fast | Cerebral, not bladder; no tissue bridge (G-02) |
| F006.a/b | A2-H2 | H2 | PTX reverses *established* structure (fibrosis) with duration-response and partial persistence | Skin; required vitamin E; no ANOVA main effect |
| F002.b | A1-H2, A1-H3 | UNRESOLVED | Functional null (carbachol-max) beside the positive -> effect is route-specific | Same source; not a defeat of the evoked-contractility route |
| F001.c | A1-H3 | UNRESOLVED | Voided-volume null tempers the human signal | Add-on; one trial |
| F033 | A1-H2, A2 | H2 / UNRESOLVED | PTX protective only as *pretreatment*, failed as rescue of established ischemia | Acute renal; poor transfer to chronic bladder |
| F032 | A1-H3 (R2/R3), G-04 | FRAME PROBLEM | Cohort's "shy bladder" = psychogenic inhibition; PTX has no evidence here | Review-level proposed mechanism |
| F008 / F007 | A1 (comparator), G-04 | UNRESOLVED | A coordination/psychogenic component responds to biofeedback -> part of the dysfunction is non-pharmacological | Uncontrolled; symptom endpoints |
| F009.a/b | A1 (R7, slot b) | SHARED | Phenotyping instruments exist to enrich a trial | Cross-sectional; no PTX-response link (G-03) |
| F013 | A1 (slot a) | H1 | PTX tolerable at 400 mg bid (discontinuation RR 0.88) -> a trial is feasible/safe | Depression cohort; no alpha-blocker co-use safety |
| F021 / F023 | A1 (R4), A2-H1 | H1 | In vivo-dosed anti-inflammatory target engagement (fast) | PBMC ex vivo; no bladder/tissue link |
| F031 | A1 (R1/R2) | H1(context) | Existing UAB drugs fail -> genuine unmet, untreated target | Reviews; also shows target is hard |

Necessary conditions for A1-H1 (materially supported rationale): a reversible component in this cohort (partial: F030/F031/F034 support a plausible ischemic/underactive target; F032/G-04 leave the paruresis fraction unaddressed); attainable exposure reaching bladder tissue (unsupported at tissue level, G-02); target modulation improving relevant voiding function (partial: F002.a positive, F002.b/F001.c null; F001.a confounded). Surviving routes: (i) microcirculatory/anti-inflammatory support of detrusor function (fast; F002.a, F003, F021); (ii) antifibrotic reversal of remodeling (slow; F006, F030). Both share the unproven bladder-exposure premise (G-02); neither is defeated.


## 7. Assessment

### Axis A1 — units and percentages (gauge G = 64)

| Hypothesis | Units / gauge | Derived percentage |
|---|---|---|
| A1-H1 | 29 / 64 | 45.31% |
| A1-H2 | 8 / 64 | 12.50% |
| A1-H3 | 27 / 64 | 42.19% |
| Total | 64 / 64 | 100% |

Overall leader: A1-H1 (29). Substantive leader: A1-H1 over A1-H3 by **2 units** — one-to-two allocation steps, i.e. a weak lean, not robust discrimination; H1 and H3 are effectively co-leading. Basis: **mixed** (validation-grounded witnesses, one bladder-specific functional positive, a confounded human add-on signal, and mechanistic perfusion/anti-inflammatory/antifibrotic support). Confidence: **low-to-medium**, scoped to trial-warrant rather than efficacy.

A1-H1 earns a modest plurality because the record is better than merely speculative. There is a bladder-specific, functional, *treatment* (not prevention) effect in an established-obstruction model (F002.a), an independent bladder line implicating a reversible ischemic/HIF-remodeling target (F030), a plausible drug action on that target at an attainable oral dose (fast perfusion in a compromised bed, F003.a; dose threshold at 800 vs 400 mg, F003.b), in vivo-dosed anti-inflammatory target engagement (F021, F023), a documented human add-on signal (PVR, Qmax; F001.a/b), acceptable tolerability (F013), and a genuine unmet target where existing UAB drugs fail (F031). Against the warrant standard, three of four trial slots are specifiable from supported premises: (a) intervention/exposure — oral PTX 400 mg q8h (or 800 mg SR), vitamin E cointervention made explicit for the antifibrotic route; (c) measurement — Qmax and PVR with expected direction (PVR down, Qmax up), the convention used by F001 and F007; (d) comparator — randomized placebo add-on to standard tamsulosin, optionally a PTX x vitamin-E factorial (F006's design) to separate the antifibrotic contribution. Under the investigation-warrant rule, unresolved intermediate links are permissible if the proposed experiment can discriminate them, and a prior study's failure to enrol the proposed subgroup is not proof the subgroup cannot be specified.

A1-H3 sits almost level because the plurality is thin and at least one slot — (b) phenotype — cannot be filled from *supported* premises. Phenotyping instruments exist (BCI/Wmax, F009), but no witness links any baseline characteristic to PTX response (G-03); the "PTX-responsive subgroup" is hypothesized, so a *targeted* trial rests on an unsupported enrichment. Two further unresolved links localize the uncertainty rather than defeat the case: bladder-tissue exposure is never measured (G-02 — perfusion is cerebral, PK is plasma, engagement is PBMC), and the cohort-mechanism match is open (G-04) because the bladder-positive evidence is obstruction/BPH while the cohort is defined partly by paruresis, a psychogenic inhibition (F032) with no PTX evidence and a coordination component that responds to biofeedback (F007, F008). The functional nulls beside the positives (carbachol-max, F002.b; voided volume, F001.c) and the baseline-imbalanced, unadjusted human PVR result (G-01) keep the rationale short of "compelling." So H3's share reflects real, named, decision-relevant gaps, not a capacity limit or a residual-null surcharge, and not NLM/DCP provenance (the contract forbids a provenance penalty).

A1-H2 is low but nonzero. H2 requires *affirmative* evidence of a mismatch *necessary to the rationale*, not merely one route among many. The candidates are F033 (PTX protective only as pretreatment, failing to rescue established ischemia) and F002.b (carbachol-max null). F033 is an acute renal model with poor transfer to chronic bladder; F002.b is paired with a positive evoked result in the same study, so it damages one route, not the shared premise. Neither reaches a link required by *every* surviving route, so H2 cannot claim the rationale is defeated; its units register the genuine (if transfer-limited) adverse-timing and route-specificity signals.

Strongest objection (A1): the entire bladder-positive base is obstruction/BPH, whereas the target men are defined by paruresis + tamsulosin-inadequacy + PFPT-failure, whose dominant dysfunction may be psychogenic/coordination (biofeedback-responsive, F008) rather than ischemic/fibrotic — so PTX may target the wrong cause in these specific men (G-04). Reversal finding: a response-predictor or bladder-exposure study tying a measurable baseline phenotype in this cohort to PTX-induced voiding improvement would fill slot (b) and move H1 up; a well-powered PTX-monotherapy null in a specified subgroup would move H2 up. Stress-check: the H1 plurality does **not** depend on a quarantined value (G-01 supports, not drives — F002.a and F030 carry the lead), on a repeated-gap penalty, or on lost adverse evidence; it depends on one preclinical positive plus a mechanistic chain with an unproven tissue-exposure bridge, which is explicitly qualified. Result: lead retained but weak; H1/H3 co-leading is the honest state.

### Axis A2 — units and percentages (gauge G = 64)

| Hypothesis | Units / gauge | Derived percentage |
|---|---|---|
| A2-H1 (rapid functional) | 15 / 64 | 23.44% |
| A2-H2 (slow structural) | 13 / 64 | 20.31% |
| A2-H3 (cannot distinguish) | 36 / 64 | 56.25% |
| Total | 64 / 64 | 100% |

Overall and substantive leader: A2-H3 (36). Basis: **mixed / mechanistic**, confidence **medium that timing is undetermined, low in any substantive leader.**

A2-H3 clearly leads because, conditional on a benefit existing, the record cannot say whether it is fast-functional or slow-structural, and the uncertainty is localized to identified timing links (G-05). The fast-functional evidence and the slow-structural evidence live in different tissues and never meet in the bladder: PTX raises perfusion within hours (F003.a, cerebral), engages anti-inflammatory targets within 2 days ex vivo (F021) and a week (F023), and resolved storage symptoms by 2-4 weeks in one case (F028) — all consistent with A2-H1; while PTX reverses *established* fibrosis over months with duration-response and partial post-withdrawal persistence (F006.a/b, skin) and HIF-remodeling is implicated in BOO (F030) — consistent with A2-H2. The only bladder-specific PTX functional datum (F002.a) is a single 4-week endpoint with no onset kinetics and no withdrawal arm, so it is compatible with either mechanism. F033 adds a conflicting note (benefit as prevention, not rescue) that maps cleanly onto neither rapid-functional nor slow-structural reversal. No witness reports bladder onset timing or post-withdrawal persistence — the two measurements that would separate the rivals.

Between the minority hypotheses, A2-H1 edges A2-H2 (15 vs 13) on PTX's best-established human pharmacology: its licensed action is hemorheologic/microcirculatory (fast functional), the compromised-bed perfusion effect (F003.a) and its absence in healthy tissue (F022) fit a functional mechanism acting where perfusion is impaired, and the earliest signals are fast. A2-H2 is close behind because PTX's capacity to *reverse established* structure is directly demonstrated (F006) and a structural contributor to bladder dysfunction is independently supported (F030) — but that evidence needed vitamin E and does not transfer timing from skin to bladder, and F033 argues against reversal of established injury in at least one model. The near-parity of the minorities and the dominance of H3 together say: a trial should measure onset and withdrawal rather than assume either timing.

Strongest objection (A2): no bladder study measures onset or post-withdrawal kinetics, so attributing any (hypothetical) voiding benefit to a fast or slow mechanism is unsupported; the fast and slow effects are cross-tissue. Reversal finding: a time-course bladder study showing early improvement that fades on withdrawal (-> A2-H1) versus delayed improvement accumulating with duration and persisting after withdrawal (-> A2-H2). Stress-check: the H3 lead rests on an absence of bladder timing data plus a genuine cross-tissue conflict, not on a provenance surcharge or a quarantined value; it is robust to the one-source positives.


## 8. Checkpoint comparison

Initial assessment under the NotebookLM/DCP evidence contract: **no prior checkpoint**, no prior comparable vector, no sibling runs. Machine coverage/crux records (M) report NO_COMPLETE_COVERAGE on every hypothesis and deletion-minimal sets NOT_RUN; consistent with an initial pass and not used as evidence or as an allocation instruction. No due forecasts outstanding. Baselines established this pass: A1 = (29, 8, 27); A2 = (15, 13, 36), gauge 64, normalized units.

## 9. Forecast and acquisition

Horizon (prospective): the **next 25 newly encountered source families** under this evidence contract (no prior identifiable batch boundary). Endpoints expressed as integer-unit changes at that horizon, same frame/gauge/normalization.

| Event | ID | Observable condition | Probability | Anchored reason |
|---|---|---|---|---|
| Material diagnostic finding | P1 | A finding closes a decisive link: bladder-tissue PTX exposure/PD (G-02), a PTX response-predictor (G-03), or a baseline-adjusted/monotherapy voiding result (G-01) | 25-40% | Such data are sparse in this corpus; most additional families are epidemiology/PFPT/off-target. |
| A1 null (H3) falls >=2 units | P2 | A1-H3 <= 25 at horizon | 25-40% | Would require new exposure or response-predictor evidence filling slot (b)/(a). |
| A1 null (H3) rises >=2 units | P3 | A1-H3 >= 29 at horizon | 20-35% | Would require affirmative mismatch (G-04) or a monotherapy null strengthening H2/H3. |
| A1 substantive leader reverses | P4 | A1-H3 (or H2) overtakes A1-H1 at horizon | 25-40% | Margin is only 2 units; a single adverse human result or confirmed cohort-mismatch could flip it. |
| Mostly redundant batch | P5 | >half of inspected input units add only retained claims, no material diagnostic finding | 40-55% | Much reachable literature (sepsis, Cushing's, female PFMT, UAB reviews) is tangential/transfer-limited. |
| Useful insight before diminishing returns | P6 | A specified actionable insight (e.g., a defensible enrichment phenotype or exposure bound) before a low-yield run | 45-60% | Phenotyping instruments (F009) and dose thresholds (F003) are already near-actionable. |

Expected effect of more data: **rising** on A1 only if targeted at G-01/G-02/G-03; otherwise **diminishing** (breadth is largely exhausted for off-target families). Returns overall: **diminishing** for untargeted search, **too early** to call on the three decisive links. Posture: **target named gaps.**

Acquisition priorities (<=3):
1. **G-01 (quarantine priority).** Resolve the strongest human signal: obtain a baseline-adjusted (ANCOVA) PVR/Qmax estimate from the Shirazi add-on trial, or an independent PTX **monotherapy** voiding RCT. Source class: urology RCT / trial report. Success: a baseline-equivalent effect estimate. Affects A1-H1 vs H3/H2. *Route note:* W-FRD-Q0048-01 states no adjusted model exists in the source -> likely blocked within the notebook; mark blocked and carry to trial design.
2. **G-02 / G-04.** PTX exposure or a perfusion/inflammatory PD marker in lower-urinary-tract tissue at oral doses, and urodynamic characterization of the target men (DU vs BOO vs dyscoordination vs paruresis fraction). Source class: pharmacology / urodynamics. Success: a tissue-exposure bound and a dominant-phenotype estimate. Fills slot (b)/(a); affects A1-H1 and A2.
3. **G-03 / G-05 (the proposed trial itself).** A PTX (or PTX x vitamin-E factorial) voiding trial in a specified male LUTS/DU subgroup with on-treatment and post-withdrawal functional endpoints. Mechanistic evidence cannot substitute for this; it is the decisive test for A1 (H1 vs H2) and A2 (H1 vs H2). Investigation remains open.

## 10. Manifest

Provider/model/surface/settings/date: UNKNOWN (harness-mediated run; date of record 2026-10-29). Tools actually used: none beyond reading the supplied batch; no web search, no external retrieval, no primary-PDF access (all evidence consumed as supplied validated witnesses). Prior reports seen: none (initial run, no parents, no siblings). Reused vs recomputed: all judgments recomputed this pass from the frozen record; no inherited allocation reused. Elapsed time: not measured.

*Final seven-question check performed once against the assembled fragment (memory/verbatim-carry n/a for an initial run; reconstruction tiers n/a — all V; symmetry of transfer tests applied to F003/F006 and F033/F002.b; full frame and investigation-warrant honored; units nonnegative integers summing to 64 per axis with exact percentages; each allocation tied to named findings with no unchanged-gap surcharge; decision-blocking G-01 prioritized and marked blocked within source). No defects requiring repair found; emitted once.*


```json
{
  "allocations": {
    "A1": {
      "A1-H1": 29,
      "A1-H2": 8,
      "A1-H3": 27
    },
    "A2": {
      "A2-H1": 15,
      "A2-H2": 13,
      "A2-H3": 36
    }
  },
  "basis_confidence": {
    "A1": "mixed (validation-grounded witnesses + one bladder-specific preclinical functional positive + confounded human add-on signal + mechanistic perfusion/anti-inflammatory/antifibrotic support); confidence low-to-medium, scoped to trial-warrant not efficacy; H1 leads H3 by only 2 units (co-leading).",
    "A2": "mixed/mechanistic; medium confidence that timing is undetermined, low confidence in any substantive leader; fast-functional and slow-structural evidence are cross-tissue and never meet in the bladder."
  },
  "drivers": {
    "A1": [
      "F002.a (W-FRD-SHIRAZI2015-01-Q0002): PTX as treatment of established pBOO raised evoked detrusor tension (P=.023) - the only bladder-specific functional positive; favors H1.",
      "F030 (W-FRD-Q0046-01) + F031 (W-FRD-Q0047-01/Q0050-01): HIF/ischemia is a reversible BOO target and existing UAB drugs fail - supports an untreated, PTX-plausible target (H1).",
      "F001.a/b (W-FRD-Q0001-01/-02-r3): human BPH add-on PVR fall and Qmax rise - supports H1 but quarantined (G-01: baseline imbalance, no ANCOVA).",
      "G-02/G-03/G-04 (no bladder-tissue exposure; no response-predictor; obstruction evidence vs psychogenic/paruresis cohort F032): unresolved links blocking slot (b) - drive H3.",
      "F033 (W-FRD-Q0019-01) prevention-only + F002.b carbachol-max null: affirmative but transfer-limited/route-specific adverse signals - the only support for H2, insufficient to defeat the shared rationale."
    ],
    "A2": [
      "F003.a (W-FRD-BOWTON-01-Q0006) perfusion within hours + F021/F023 fast in-vivo-dosed engagement + F022 null in healthy bed: fast functional mechanism (A2-H1).",
      "F006.a/b (W-FRD-Q0009-02/-03): PTX reverses established fibrosis over months with duration-response and partial persistence (A2-H2); needed vitamin E, skin not bladder.",
      "F002.a single 4-week bladder endpoint with no onset/withdrawal kinetics + F033 prevention-not-rescue conflict: timing undetermined in the bladder - drives A2-H3."
    ]
  },
  "strongest_objection": {
    "A1": "The entire bladder-positive evidence base is obstruction/BPH, whereas the target men are defined partly by paruresis (psychogenic, F032) and PFPT-failure with a biofeedback-responsive coordination component (F007/F008); PTX's microcirculatory/antifibrotic mechanism may target the wrong cause in these specific men (G-04), and the strongest human signal is baseline-confounded and unadjusted (G-01).",
    "A2": "No bladder study measures onset or post-withdrawal kinetics; the fast (perfusion/anti-inflammatory) and slow (antifibrotic) effects are in different tissues, so attributing any voiding benefit to a fast or slow mechanism is presently unsupported."
  },
  "reversal_finding": {
    "A1": "A response-predictor or bladder-tissue exposure study linking a measurable baseline phenotype in this cohort to PTX-induced voiding improvement would fill slot (b) and raise H1; a well-powered PTX-monotherapy voiding null in a specified subgroup would raise H2.",
    "A2": "A time-course bladder study: early improvement that fades on withdrawal favors A2-H1 (rapid functional); delayed improvement accumulating with duration and persisting after withdrawal favors A2-H2 (slow structural)."
  }
}
```
