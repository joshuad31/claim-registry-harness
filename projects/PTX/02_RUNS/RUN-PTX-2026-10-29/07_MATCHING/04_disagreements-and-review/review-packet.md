# Matching review packet

Each entry is one witness judged against one coverage unit. To overrule a relation, add an entry to `human-decisions.json` in this folder (a blank template is next to this file) and run `cr run <project> --from coverage`. Relations: EQUIVALENT, WITNESS_ENTAILS_UNIT (these two give complete coverage), UNIT_ENTAILS_WITNESS, PARTIALLY_COVERS, CONTRADICTS, NO_SEMANTIC_RELATION, ABSTAIN.

## Complete relations (these build coverage sets) (6)

### A1-H3-R1 x W-FRD-Q0001-01-Q0001
- Unit (REQUIRED_SUPPORT): Existing evidence affirmatively supports some components of H1, that is, at least one link in the chain from clinically attainable PTX or metabolite exposure, through a relevant biological target and tissue effect, to changed voiding function, an identifiable patient subgroup, and a measurable trial prediction.
- Witness: Shirazi et al. (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md): single-center randomized double-blind trial, 30 men per arm (all analyzed) with BPH/LUTS, giving pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day or placebo plus tamsulosin, 12 weeks. Post-void residual fell more with combination (−32.93±16.33 versus −13.17±9.23 mL; p<.001), but baseline residual differed (77.27 versus 50.37 mL; p=.18). Reported values, not validated or baseline-equivalent.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; 2 | METHODS; 2.3 | Study design; FIGURE 1; TABLE 1, PVR row; TABLE 4, PVR row
- Pass A: WITNESS_ENTAILS_UNIT - In a randomized double-blind trial, PTX 400 mg every eight hours (a clinical regimen) added to tamsulosin in men with BPH/LUTS was reported to lower post-void residual more than placebo plus tamsulosin (p<.001), affirmatively supporting the PTX-to-changed-voiding-function link the unit lists; the baseline-imbalance caveat weakens but does not remove that support.
- Pass B: PARTIALLY_COVERS - PTX-associated emptying improvement in BPH men supports a urinary-function link, but combination with baseline imbalance.
- Final: **WITNESS_ENTAILS_UNIT** (MODEL_ADJUDICATED) - The unit asks only that existing evidence 'affirmatively supports' at least one link from 'clinically attainable' exposure to 'changed voiding function'; a randomized double-blind trial of 'pentoxifylline 400 mg every eight hours' reporting a larger post-void residual fall than placebo plus tamsulosin (p<.001) meets those stated exposure and outcome conditions. The 'baseline residual differed' and 'not validated or baseline-equivalent' caveats weaken the support but do not reverse its polarity, and the unit requires support, not proof.

### A2-H3-E2 x W-FRD-Q0001-02-r3-Q0001
- Unit (CORROBORATING_EXPECTATION): Available findings lack onset or withdrawal timing.
- Witness: Shirazi et al. (2024, Lower Urinary Tract Symptoms) reported mean Qmax changes of 4.48 versus 2.67 mL/s; their arithmetic difference, 1.81 mL/s, is an analyst-derived unadjusted contrast favoring pentoxifylline-plus-tamsulosin over placebo-plus-tamsulosin, not a separately reported adjusted estimate. This BPH add-on trial does not establish pentoxifylline monotherapy or psychogenic-voiding efficacy.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Shirazi M et al. Lower Urinary Tract Symptoms. 2024;16(1):e12509. doi:10.1111/luts.12509. Exact source filename: `Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md`. Locations: TABLE 4; 2 | METHODS; 2.3 | Study design. Original locator: TABLE 4. Page numbers are unavailable in the supplied text.
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - In-scope BPH-men PTX outcome reported with no onset or post-withdrawal timing — an instance of findings lacking onset/withdrawal timing.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] In-scope BPH-men PTX outcome reported with no onset or post-withdrawal timing — an instance of findings lacking onset/withdrawal timing.

### A2-H3-E3 x W-FRD-Q0019-01-Q0019
- Unit (CORROBORATING_EXPECTATION): Available findings rest on models whose timing does not transfer to this cohort.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - Pretreatment-only PTX efficacy in an acute rat renal-ischemia model; witness explicitly states within-timing acute-model results do not transfer to chronic bladder disease.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] Pretreatment-only PTX efficacy in an acute rat renal-ischemia model; witness explicitly states within-timing acute-model results do not transfer to chronic bladder disease.

### A2-H3-R2 x W-FRD-Q0001-01-Q0001
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: Shirazi et al. (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md): single-center randomized double-blind trial, 30 men per arm (all analyzed) with BPH/LUTS, giving pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day or placebo plus tamsulosin, 12 weeks. Post-void residual fell more with combination (−32.93±16.33 versus −13.17±9.23 mL; p<.001), but baseline residual differed (77.27 versus 50.37 mL; p=.18). Reported values, not validated or baseline-equivalent.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; 2 | METHODS; 2.3 | Study design; FIGURE 1; TABLE 1, PVR row; TABLE 4, PVR row
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - In-scope PTX emptying outcome at endpoint only; onset/persistence not specifiable from it.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] In-scope PTX emptying outcome at endpoint only; onset/persistence not specifiable from it.

### A2-H3-R2 x W-FRD-Q0001-02-r3-Q0001
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: Shirazi et al. (2024, Lower Urinary Tract Symptoms) reported mean Qmax changes of 4.48 versus 2.67 mL/s; their arithmetic difference, 1.81 mL/s, is an analyst-derived unadjusted contrast favoring pentoxifylline-plus-tamsulosin over placebo-plus-tamsulosin, not a separately reported adjusted estimate. This BPH add-on trial does not establish pentoxifylline monotherapy or psychogenic-voiding efficacy.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Shirazi M et al. Lower Urinary Tract Symptoms. 2024;16(1):e12509. doi:10.1111/luts.12509. Exact source filename: `Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md`. Locations: TABLE 4; 2 | METHODS; 2.3 | Study design. Original locator: TABLE 4. Page numbers are unavailable in the supplied text.
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - In-scope PTX voiding outcome with no onset or withdrawal timing; shows persistence/onset not derivable from this premise.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] In-scope PTX voiding outcome with no onset or withdrawal timing; shows persistence/onset not derivable from this premise.

### A2-H3-R2 x W-FRD-Q0011-01-Q0011
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: In Shirazi et al.'s single-center, randomized, double-blind 12-week BPH trial (60 men, 30/group), pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day versus placebo plus tamsulosin showed no significant between-group voided-volume change (0.80 versus +1.34 mL; p=.22) and no statistically significant within-group change (p=.90, .89). Baseline-to-endpoint voided-volume only—not residual or flow; visit schedule, onset, post-withdrawal persistence unestablished (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md, §3.3).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; §2.3 Study design; §3 Results; §3.3 Voided volume; Tables 2–4, voided-volume rows
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - Witness states visit schedule, onset and post-withdrawal persistence unestablished — directly shows onset/persistence not specifiable from this premise.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] Witness states visit schedule, onset and post-withdrawal persistence unestablished — directly shows onset/persistence not specifiable from this premise.

## Contradictions (these drive crux tests) (1)

### A2-H2-C2 x W-FRD-Q0019-01-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): PTX can reverse or limit that structural change rather than merely prevent it.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: CONTRADICTS - Affirmative prevention-only pattern (benefit only pre-ischemia, not during/after) — the finding the unit says contradicts 'PTX can reverse established change.'
- Final: **CONTRADICTS** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] Affirmative prevention-only pattern (benefit only pre-ischemia, not during/after) — the finding the unit says contradicts 'PTX can reverse established change.'

## Disagreements between pass A and pass B (82)

### A1-H1-A2 x W-FRD-Q0001-01-Q0001
- Unit (ADVERSE_TEST): The proposed target is absent or incidental in impaired voiding relevant to this cohort.
- Witness: Shirazi et al. (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md): single-center randomized double-blind trial, 30 men per arm (all analyzed) with BPH/LUTS, giving pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day or placebo plus tamsulosin, 12 weeks. Post-void residual fell more with combination (−32.93±16.33 versus −13.17±9.23 mL; p<.001), but baseline residual differed (77.27 versus 50.37 mL; p=.18). Reported values, not validated or baseline-equivalent.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; 2 | METHODS; 2.3 | Study design; FIGURE 1; TABLE 1, PVR row; TABLE 4, PVR row
- Pass A: NO_SEMANTIC_RELATION - Reports a larger PVR fall with PTX add-on in BPH/LUTS men, with baseline imbalance, but names and tests no target or process; it does not show the target absent or incidental, and with an unnamed target and the stated baseline caveat it does not contradict the unit at the same scope.
- Pass B: CONTRADICTS - Emptying improvement implies consequential target, contradicting absence/incidental.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports a larger PVR fall with PTX add-on in BPH/LUTS men but names no target, so it neither shows the proposed target absent or incidental nor affirmatively shows it consequential. CONTRADICTS would need unstated assumptions that the PVR change runs through the proposed target and that BPH/LUTS voiding is the cohort-relevant voiding, and 'baseline residual differed' further weakens attribution.

### A1-H1-A2 x W-FRD-Q0001-02-r3-Q0001
- Unit (ADVERSE_TEST): The proposed target is absent or incidental in impaired voiding relevant to this cohort.
- Witness: Shirazi et al. (2024, Lower Urinary Tract Symptoms) reported mean Qmax changes of 4.48 versus 2.67 mL/s; their arithmetic difference, 1.81 mL/s, is an analyst-derived unadjusted contrast favoring pentoxifylline-plus-tamsulosin over placebo-plus-tamsulosin, not a separately reported adjusted estimate. This BPH add-on trial does not establish pentoxifylline monotherapy or psychogenic-voiding efficacy.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Shirazi M et al. Lower Urinary Tract Symptoms. 2024;16(1):e12509. doi:10.1111/luts.12509. Exact source filename: `Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md`. Locations: TABLE 4; 2 | METHODS; 2.3 | Study design. Original locator: TABLE 4. Page numbers are unavailable in the supplied text.
- Pass A: NO_SEMANTIC_RELATION - An unadjusted, analyst-derived Qmax contrast favoring PTX add-on; no target or process is assessed, so absence or incidence of the proposed target is not addressed.
- Pass B: CONTRADICTS - Improvement implies the target is consequential, contradicting absence/incidental.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - An 'analyst-derived unadjusted contrast' in Qmax favouring PTX add-on assesses no target or process, and the witness says the trial 'does not establish pentoxifylline monotherapy or psychogenic-voiding efficacy'; reading it as contradicting the adverse claim rests on unstated mediation and scope assumptions.

### A1-H1-A2 x W-FRD-Q0004-01-Q0004
- Unit (ADVERSE_TEST): The proposed target is absent or incidental in impaired voiding relevant to this cohort.
- Witness: He et al. retrospectively studied 21 men with nonbacterial chronic prostatitis and dysfunctional voiding (2007-2009), selected after antibiotics and alpha-blockers over six months gave poor effects. Diagnostic criteria required no neurological abnormality plus transient, intermittent external-sphincter closure during voiding on EMG and fluoroscopic cysto-urethrography, with raised external-sphincter EMG activity without abdominal-pressure increase (he2010.pdf.md, Patients and Methods).
- Source: he2010.pdf.md He W, Chen M, Zu X, Li Y, Ning K and Qi L. “Chronic prostatitis presenting with dysfunctional voiding and effects of pelvic floor biofeedback treatment.” Exact source: `he2010.pdf.md`, body **PATIENTS AND METHODS**, paragraphs beginning “Between July 2007” and “The diagnostic criteria of DV included”; **DISCUSSION**, paragraph beginning “The diagnosis of DV mainly depends”; **RESULTS**, TABLE 1; **Abbreviations**. The supplied text gives acceptance on 9 June 2009 but does not supply the article’s journal, publication year, volume or pages. Original locator: PATIENTS AND METHODS; repaired locator distinguishes the body section from the identically headed abstract section.
- Pass A: NO_SEMANTIC_RELATION - Diagnostic criteria for sphincter-type dysfunctional voiding in men with chronic prostatitis; it does not assess the proposed PTX target or state that it is absent, incidental or confined elsewhere.
- Pass B: PARTIALLY_COVERS - Defines a non-PTX-target mechanism in cohort-relevant men.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness gives diagnostic criteria ('transient, intermittent external-sphincter closure during voiding') for dysfunctional voiding in men with chronic prostatitis; it neither examines the proposed target nor states it is absent or incidental, and the existence of an alternative mechanism does not entail the target's absence without an unstated exclusivity assumption.

### A1-H1-A2 x W-FRD-Q0004-02-Q0004
- Unit (ADVERSE_TEST): The proposed target is absent or incidental in impaired voiding relevant to this cohort.
- Witness: He et al. (he2010.pdf.md, PATIENTS AND METHODS; RESULTS, TABLE 1) report a retrospective, uncontrolled series of 21 men with nonbacterial chronic prostatitis and dysfunctional voiding whose Qmax rose 8.2 (SD 4.1) to 15.1 (SD 7.3) mL/s after ~10 weeks of relaxation/coordination biofeedback, not strengthening (P<0.05); antibiotics, α-blockers, anticholinergics suspended. Lacking a placebo control, this within-cohort change isn't a controlled effect.
- Source: he2010.pdf.md Main-text PATIENTS AND METHODS; RESULTS, TABLE 1; DISCUSSION, paragraph beginning “Based on these results”
- Pass A: NO_SEMANTIC_RELATION - Biofeedback-associated Qmax rise in an uncontrolled series; no PTX target is examined, so the adverse claim is neither supported nor refuted.
- Pass B: PARTIALLY_COVERS - Non-inflammatory functional mechanism in men; partial support.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - An uncontrolled Qmax rise after 'relaxation/coordination biofeedback' shows a behaviourally modifiable component but says nothing about the proposed target; response to another treatment does not make the target absent or incidental unless exclusivity is assumed, which the witness does not state.

### A1-H1-A2 x W-FRD-Q0004-03-r2-Q0004
- Unit (ADVERSE_TEST): The proposed target is absent or incidental in impaired voiding relevant to this cohort.
- Witness: Kaplan et al. (kaplan1997.pdf.md): retrospective series of 43 men with urodynamically diagnosed pseudodyssynergia, previously treated as chronic nonbacterial prostatitis. Success was ≥50% symptom reduction on two consecutive visits. After behavior modification and biofeedback, 35 (printed 83%) responded; responders' mean AUA score fell 18.4→7.6 (three months), 8.1 (six months). RESULTS gives the three-month count; the abstract reports six-month success.
- Source: kaplan1997.pdf.md Kaplan et al., “Pseudodyssynergia (Contraction of the External Sphincter During Voiding) Misdiagnosed as Chronic Nonbacterial Prostatitis and the Role of Biofeedback as a Therapeutic Option”; `kaplan1997.pdf.md`, MATERIALS AND METHODS, RESULTS, and ABSTRACT—Results. The supplied text does not provide the article’s journal volume, issue, or page range. Original locator: RESULTS; repaired locator adds MATERIALS AND METHODS and ABSTRACT—Results.
- Pass A: NO_SEMANTIC_RELATION - Biofeedback response in pseudodyssynergia; no statement about the proposed PTX target or process.
- Pass B: PARTIALLY_COVERS - Alternative sphincter-dyscoordination mechanism in cohort-like men; partial support target incidental.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Biofeedback response in urodynamically diagnosed pseudodyssynergia ('35 (printed 83%) responded') concerns an alternative treatment's effect; the witness makes no statement about the proposed target being absent or incidental, so support would rest on an unstated exclusivity assumption.

### A1-H1-A2 x W-FRD-Q0049-01-Q0049
- Unit (ADVERSE_TEST): The proposed target is absent or incidental in impaired voiding relevant to this cohort.
- Witness: Chung 2014's review characterizes paruresis (bashful bladder) as psychogenic inhibition of micturition—difficulty or inability to urinate when others are present or may soon be present—citing Boschen (2008), and suggests it may contribute to underactive bladder long-term. This is review-level proposed-mechanism description, not demonstrated psychogenic causation, a prevalence estimate, or treatment-response data.
- Source: chung2014.pdf.md Exact Definition and Proposed Pathophysiologic Mechanisms, sentence beginning “Psychogenic inhibition of micturition”; References, item 14
- Pass A: NO_SEMANTIC_RELATION - Review proposes paruresis as psychogenic inhibition that 'may contribute' to underactive bladder; it is a mechanism description, not a finding that the proposed PTX target is absent or incidental.
- Pass B: PARTIALLY_COVERS - Proposes an alternative (psychogenic) mechanism relevant to shy bladder; partial support that the physiological target may be incidental; review-level.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The review 'characterizes' paruresis as psychogenic inhibition and 'suggests it may contribute to underactive bladder long-term', explicitly 'not demonstrated psychogenic causation'; this hedged mechanism description does not state that the proposed target is absent or incidental, and its suggested physiological sequel cuts against that reading.

### A1-H1-A3 x W-FRD-Q0001-02-r3-Q0001
- Unit (ADVERSE_TEST): Target modulation fails to improve the relevant urinary function under informative conditions.
- Witness: Shirazi et al. (2024, Lower Urinary Tract Symptoms) reported mean Qmax changes of 4.48 versus 2.67 mL/s; their arithmetic difference, 1.81 mL/s, is an analyst-derived unadjusted contrast favoring pentoxifylline-plus-tamsulosin over placebo-plus-tamsulosin, not a separately reported adjusted estimate. This BPH add-on trial does not establish pentoxifylline monotherapy or psychogenic-voiding efficacy.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Shirazi M et al. Lower Urinary Tract Symptoms. 2024;16(1):e12509. doi:10.1111/luts.12509. Exact source filename: `Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md`. Locations: TABLE 4; 2 | METHODS; 2.3 | Study design. Original locator: TABLE 4. Page numbers are unavailable in the supplied text.
- Pass A: PARTIALLY_COVERS - Flow improved with a PTX-containing regimen in the cohort, running against 'fails to improve', but combination therapy prevents attributing target modulation to PTX; adverse-partial.
- Pass B: CONTRADICTS - PTX-attributed voiding improvement where the adverse test applies; opposite polarity to 'fails to improve'.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-A3 x W-FRD-Q0027-01-Q0027
- Unit (ADVERSE_TEST): Target modulation fails to improve the relevant urinary function under informative conditions.
- Witness: Neuner et al. (immunology00076-0102.pdf.md) studied four healthy volunteers overall; the two-day-regimen subgroup size is unspecified. Oral PTX 5×400 mg/day for two days significantly suppressed TNF-α, IL-1β, IL-6 and IL-8 release from day-7 PBMC cultured 24 hours, with or without LPS 1 µg/mL. These are ex-vivo endpoints after in-vivo dosing; plasma/tissue exposure and clinical urinary efficacy were unmeasured.
- Source: immunology00076-0102.pdf.md P. Neuner et al., “Pentoxifylline in vivo down-regulates the release of IL-1 β, IL-6, IL-8 and tumour necrosis factor-α by human peripheral blood mononuclear cells.” Exact source: `immunology00076-0102.pdf.md`; MATERIALS AND METHODS → Human volunteers; Preparation of PBMC; RESULTS → In vivo effects of orally applied PTX on cytokine production by PBMC, first paragraph; Figure 1 original caption. The original results locator is correct. Journal, volume, pagination and publication date are not established by the supplied article metadata; receipt and acceptance dates are supplied but are not publication dates.
- Pass A: PARTIALLY_COVERS - Confirms PTX target modulation (ex vivo cytokine suppression) at a tolerated oral dose, supplying the 'target modulated' half, but urinary function was not assessed, so 'no urinary improvement' is unestablished.
- Pass B: NO_SEMANTIC_RELATION - Target modulated but urinary function unmeasured; cannot establish non-improvement.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-A3 x W-FRD-Q0044-01-Q0044
- Unit (ADVERSE_TEST): Target modulation fails to improve the relevant urinary function under informative conditions.
- Witness: Fukabori-1996-uninhibited-bladder.pdf.md (English abstract, 'A CASE OF UNINHIBITED BLADDER...') reports one 60-year-old woman with pollakisuria, urge incontinence and urodynamic uninhibited contractions; after a failed anticholinergic, pentoxifylline (dose/route unstated) resolved incontinence and reduced pollakisuria by two weeks, with contractions absent and increased capacity by four weeks. Storage symptoms only; single case, not comparative efficacy.
- Source: Fukabori-1996-uninhibited-bladder.pdf.md English abstract under “A CASE OF UNINHIBITED BLADDER SUCCESSFULLY TREATED WITH PENTOXIFYLLINE”, paragraph beginning “A 60-year-old woman with pollakisuria and urge incontinence”
- Pass A: PARTIALLY_COVERS - PTX improved urinary (storage) symptoms in a single case, contrary to 'fails to improve', but storage not emptying, a single non-cohort case.
- Pass B: NO_SEMANTIC_RELATION - PTX improved a urinary (storage) function off-scope; does not establish non-improvement in cohort voiding.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-C1 x W-FRD-Q0005-01-Q0005
- Unit (CONTEXTUAL_CONSTRAINT): The relevant dysfunction occurs in this cohort.
- Witness: Masterson et al. (masterson2017.pdf.md, Methods; Results) prospectively studied an uncontrolled pilot of multimodal pelvic-floor physical therapy (manual therapy, therapeutic exercise, biofeedback, neuromodulation; nonstandardized frequency) in 14 men with idiopathic CPPS, assessed at the tenth visit. Ten completed ten visits; the remaining four had completed five-to-nine and were reported as still ongoing, not dropouts or completed-treatment failures.
- Source: masterson2017.pdf.md Abstract Methods and Results; body Methods, Results, and Discussion
- Pass A: PARTIALLY_COVERS - A cohort of men with idiopathic CPPS undergoing pelvic-floor therapy, consistent with pelvic-floor voiding dysfunction occurring in men, though this snippet reports visit completion.
- Pass B: NO_SEMANTIC_RELATION - About visit completion in CPPS men, not the voiding dysfunction occurring in the scope cohort.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-C1 x W-FRD-Q0005-02-Q0005
- Unit (CONTEXTUAL_CONSTRAINT): The relevant dysfunction occurs in this cohort.
- Witness: Anderson et al. (anderson2011.pdf.md), a prospective open-label UCPPS pilot, report 113 of 157 (72%; 106 men, 7 women) completed six months of internal therapeutic-wand use within a multimodal self-treatment program (prescribed 3–4×/week; withdrawal threshold <1×/week). Of 44 withdrawn, 10 noncompliant, 10 failed questionnaires, rest unspecified. Completion is not verified per-session adherence and not a male-only clinic-PFPT cohort.
- Source: anderson2011.pdf.md RESULTS; MATERIALS AND METHODS; TABLE 2, Subjects Under Evaluation; Pelvic Muscle TrP Sensitivity; DISCUSSION
- Pass A: PARTIALLY_COVERS - A predominantly male UCPPS cohort, consistent with the relevant pelvic/voiding dysfunction occurring, though the snippet reports completion not characterization.
- Pass B: NO_SEMANTIC_RELATION - Reports wand-therapy completion, not the dysfunction's presence in the cohort.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-C1 x W-FRD-Q0022-01-Q0022
- Unit (CONTEXTUAL_CONSTRAINT): The relevant dysfunction occurs in this cohort.
- Witness: Clemens et al. 2000: cohort of 19 men with chronic pelvic pain syndrome receiving combined biofeedback-directed pelvic-floor re-education and bladder training over six biweekly sessions. Ten completed all six, five completed three to five, four completed fewer than three; the four non-completers' reasons were sufficient improvement (2), insurance issues (1), unknown (1). Complete follow-up covered 16 patients, not all enrolled.
- Source: clemens2000.pdf.md RESULTS, paragraph beginning “Ten patients completed all six biofeedback sessions”; MATERIAL AND METHODS, paragraph beginning “The biofeedback program is a standardized protocol”
- Pass A: PARTIALLY_COVERS - A cohort of men with chronic pelvic pain receiving pelvic-floor retraining, consistent with the relevant dysfunction occurring in men, though the snippet reports completion.
- Pass B: NO_SEMANTIC_RELATION - Reports completion/dropout counts, not whether the voiding dysfunction occurs in the cohort.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-C3 x W-FRD-Q0031-01-Q0031
- Unit (CONTEXTUAL_CONSTRAINT): Changing those processes can improve urinary function.
- Witness: van Reijn-Baggen 2022 review's Table 2 lists FitzGerald et al. (2009), a 47-participant mixed-population randomized trial comparing pelvic-floor physical therapy against full-body Western massage: CP/CPPS NIH-urinary pre-to-post P<.001 and PFPT-versus-control P<.01, with no stated between-group direction or magnitude; the narrative reports equal urinary improvement. This review-transmitted symptom-index result is not independent replication or improved bladder emptying.
- Source: vanreijn-baggen2022.pdf.md Table 2, Fitzgerald et al. (2009) entry and continuation, NIH-urinary row; RESULTS → Outcome assessments → Improvement of pelvic floor symptoms; REFERENCES, item 51
- Pass A: NO_SEMANTIC_RELATION - PFPT improves urinary symptom indices, but pelvic-floor therapy is not the PTX-proposed process (the unit's 'those processes'), so it does not bear on modulating that process.
- Pass B: PARTIALLY_COVERS - Review-transmitted PFPT improved a urinary symptom index; modulation->urinary measure, symptom-level, review.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-C3 x W-FRD-Q0047-01-Q0047
- Unit (CONTEXTUAL_CONSTRAINT): Changing those processes can improve urinary function.
- Witness: Kim 2017's review of underactive bladder reports that, although parasympathomimetics have been widely used, the evidence does not support clinical benefit; it describes conflicting clinical results and relays Barendrecht et al.'s conclusion that evidence does not support their use, particularly given potential adverse effects.
- Source: kim2017.pdf.md Opening abstract; PHARMACOLOGICAL THERAPY > 1. Parasympathomimetics; Table 1. Randomized controlled trials of parasympathomimetics for underactive bladder
- Pass A: NO_SEMANTIC_RELATION - Parasympathomimetics lack supported benefit, but cholinergic stimulation is not shown to be the proposed process, so this null neither supports nor contradicts the unit.
- Pass B: PARTIALLY_COVERS - Review: modulating cholinergic signaling not shown to benefit UAB; bears on the claim's negative side, review-transmitted, different lever.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-C3 x W-FRD-Q0055-01-Q0055
- Unit (CONTEXTUAL_CONSTRAINT): Changing those processes can improve urinary function.
- Witness: Glazener et al. 2011, UK randomized TURP trial: 442 men with incontinence six weeks post-surgery were offered four one-to-one PFMT (plus bladder training) sessions (n=220) or standard care (n=222). At 12 months, self-reported any incontinence (ICIQ-UI SF) was 126/194 (65%) versus 125/203 (62%); adjusted intention-to-treat risk ratio 1.06 (95% CI 0.91–1.23; p=0.47)—no significant benefit. Post-surgical leakage, not difficult emptying.
- Source: glazener2011.pdf.md Table 3: Outcomes at 12 months, Trial 2, Men with any incontinence and footnotes; Table 4, adjusted intention-to-treat row; Figure 1B; Methods—Procedures; Summary—Methods
- Pass A: NO_SEMANTIC_RELATION - Post-TURP PFMT incontinence null; not the proposed process and not voiding difficulty.
- Pass B: PARTIALLY_COVERS - PFMT left post-surgical incontinence unchanged in men; bears on modulation-vs-function but storage/leakage, not voiding.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-C3 x W-FRD-Q0056-01-Q0056
- Unit (CONTEXTUAL_CONSTRAINT): Changing those processes can improve urinary function.
- Witness: In a study its authors call a retrospective case–control of 180 men with BPH after TURP (11255_2025_Article_4454.pdf.md, Table 6; Grouping and intervention methods), Table 6 reports post-intervention urinary control (fewer than one pad/day) in 31/83 (37.35%) given HBM-guided PFMT plus standard care versus 24/97 (24.74%) standard care alone, between-group P=0.067 (nonsignificant). This combination-program continence comparison isn't emptying, PFMT-monotherapy, or six-month-defined.
- Source: 11255_2025_Article_4454.pdf.md Xiao et al. (2025), “Application effect of pelvic floor function exercise based on health belief model in patients with benign prostatic hyperplasia after electrocautery.” Exact source: `11255_2025_Article_4454.pdf.md`. Locations: Table 6; Materials and methods → Case selection, Inclusion criteria, Grouping and intervention methods, Treatment approach, and Urinary control rate evaluation. Published online 25 April 2025. Journal, volume, pagination, and DOI are not established by the supplied text.
- Pass A: NO_SEMANTIC_RELATION - PFMT-program continence comparison; not the proposed process.
- Pass B: PARTIALLY_COVERS - PFMT+care changed a pelvic-floor process with a continence outcome (ns) in men; partial, storage endpoint and nonsignificant.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-C3 x W-FRD-SHIRAZI2015-02-Q0002
- Unit (CONTEXTUAL_CONSTRAINT): Changing those processes can improve urinary function.
- Witness: Shirazi 2015: in male Sprague-Dawley rats with partial bladder outlet obstruction, pentoxifylline 100 mg/kg/day by oral gavage for four weeks, begun after obstruction induction, produced no significant improvement in maximum carbachol-induced detrusor-strip contractile tension versus water-treated obstructed controls (20 animals per group; all completed). Treatment addressed established obstruction, not prevention; this is a functional contractility null.
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Abstract → Results; Results and Fig. 2
- Pass A: NO_SEMANTIC_RELATION - PTX gave 'no significant improvement' in carbachol-induced tension in obstructed rats, but target modulation was not measured and a rat-model null is not a contradiction of a 'can improve' claim at this cohort's scope.
- Pass B: PARTIALLY_COVERS - PTX modulation gave a carbachol-contractility null in rat BOO; bears on the modulation->urinary-function claim but species/model mismatch, so partial, not a cohort contradiction.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R2 x W-FRD-Q0020-01-Q0020
- Unit (REQUIRED_SUPPORT): That reversible physiological component is one that tamsulosin does not adequately address in these men.
- Witness: Yu and Jeong's clinical literature review (2020ICU_icu-58-S68.pdf.md, PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY) reports most published detrusor-underactivity prevalence data came from community-dwelling cohorts with significant LUTS judged by arbitrary urodynamic criteria (25%–48% elderly men, 12%–24% women), with limited general-population applicability. Community-based research is described as rare, not absent; one study used free Qmax and post-void residual, not pressure-flow parameters.
- Source: 2020ICU_icu-58-S68.pdf.md Author byline; opening abstract; PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY, concluding two paragraphs and paragraph beginning “Unlike other researchers, Groutz et al.”
- Pass A: PARTIALLY_COVERS - Documents detrusor underactivity (a contractility component outside an alpha-blocker's outlet-relaxing action) in men with LUTS, bearing on 'a component outside tamsulosin's action', but it is prevalence only and does not establish persistence under tamsulosin or reversibility.
- Pass B: NO_SEMANTIC_RELATION - Prevalence/epidemiology, no tamsulosin-response link; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The unit's predicate is that tamsulosin 'does not adequately address' the component in these men; the witness reports detrusor-underactivity prevalence only and never mentions tamsulosin or alpha-blockers. That underactivity lies outside tamsulosin's action is an imported pharmacological assumption, not witness text.

### A1-H1-R2 x W-FRD-Q0023-01-Q0023
- Unit (REQUIRED_SUPPORT): That reversible physiological component is one that tamsulosin does not adequately address in these men.
- Witness: In Cornel et al.'s uncontrolled pre/post study of men with type III CP/CPPS, 31 of 33 enrolled remained after two dropped out. The mean NIH-CPSI micturition score fell from 5.1 (range 0-10) before to 2.2 (range 0-6) after pelvic-floor biofeedback and re-education (p<0.001). These are symptom scores, not measured urinary flow or residual volume (cornel2005.pdf.md, Results).
- Source: cornel2005.pdf.md §2 Methods; §3 Results, opening paragraph and Table 1, Results pre- and post-treatment; §4 Discussion, paragraph beginning Although we realize
- Pass A: PARTIALLY_COVERS - Micturition symptoms improved with pelvic-floor retraining in men, indicating a reversible functional component lying outside tamsulosin's prostate action, but no tamsulosin-response linkage and only symptom scores.
- Pass B: NO_SEMANTIC_RELATION - Behavioral-therapy outcome, no tamsulosin-response data; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Micturition-score improvement after pelvic-floor biofeedback in men with CP/CPPS suggests a modifiable component but contains no tamsulosin exposure, comparison or response data; tamsulosin inadequacy, the unit's actual predicate, would have to be assumed.

### A1-H1-R2 x W-FRD-Q0053-01-Q0053
- Unit (REQUIRED_SUPPORT): That reversible physiological component is one that tamsulosin does not adequately address in these men.
- Witness: Chuang and colleagues' review reports, secondhand from Jeong and colleagues, that among 1,179 adults over 65 with non-neurogenic voiding dysfunction presenting with urinary symptoms, 'more than 40.2%' of men had detrusor underactivity (male criterion: bladder contractility index below 100). The 1,179 is the mixed-sex total, not the male denominator, which is not supplied (chuang2015.pdf.md, Epidemiology).
- Source: chuang2015.pdf.md EPIDEMIOLOGY, paragraph beginning “Jeong and colleagues”; REFERENCES, Jeong SJ et al. entry (reference 6 in the text)
- Pass A: PARTIALLY_COVERS - Documents detrusor underactivity in older men (a contractility component outside outlet relaxation), bearing on 'outside tamsulosin's action', but epidemiologic only, with no tamsulosin-response or reversibility data.
- Pass B: NO_SEMANTIC_RELATION - Prevalence of detrusor underactivity, but no stated relation to tamsulosin response; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The review reports 'more than 40.2%' detrusor underactivity among older men with voiding dysfunction, with no statement about tamsulosin; linking this to tamsulosin's inadequacy depends on an unstated mechanism-of-action assumption.

### A1-H1-R2 x W-FRD-RADEMAKERS-01-Q0003
- Unit (REQUIRED_SUPPORT): That reversible physiological component is one that tamsulosin does not adequately address in these men.
- Witness: Rademakers et al.'s review (rademakers2016.pdf.md, Preoperative characterization; Figure 1) reports a retrospective urodynamic analysis attributed to Oelke et al. of 786 treatment-naïve men ≥40 with LUTS: median BCI rose with obstruction grade from 73 (Schäfer 0) to 188 (grade 6), median Wmax from 9.6 to 23 W/m². The review suggests thresholds BCI<100 and Wmax<7 be grade-adjusted—cross-sectional association, not within-man change.
- Source: rademakers2016.pdf.md PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION, paragraphs beginning “Three urodynamic parameters” and “Oelke”; FIGURE 1 caption; REFERENCES AND RECOMMENDED READING, reference 22 and annotation
- Pass A: PARTIALLY_COVERS - Urodynamic characterization of detrusor contractility relative to obstruction in men with LUTS identifies a contractility component distinct from outlet obstruction (tamsulosin's target), but it is cross-sectional and not tied to tamsulosin response.
- Pass B: NO_SEMANTIC_RELATION - Cross-sectional urodynamics, no tamsulosin-response data; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - A 'cross-sectional association' of BCI and Wmax with obstruction grade in 'treatment-naïve men' contains no tamsulosin data; that contractility lies outside what tamsulosin addresses is the reader's assumption, not the witness's statement.

### A1-H1-R2 x W-FRD-RADEMAKERS-02-Q0003
- Unit (REQUIRED_SUPPORT): That reversible physiological component is one that tamsulosin does not adequately address in these men.
- Witness: Rademakers et al. (rademakers2016.pdf.md), a narrative review, report that Oelke developed the Hannover–Maastricht nomogram from urodynamic data of 822 treatment-naïve men aged ≥40 with LUTS/BPO. It plots bladder-outlet-obstruction index against maximum Watts factor to classify outlet resistance and detrusor contractility simultaneously; values below the 25th-percentile line indicate detrusor underactivity relative to outlet resistance, including when obstruction coexists. Validation remained ongoing.
- Source: rademakers2016.pdf.md PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION, development and verification paragraphs; FIGURE 2 caption; FIGURE 3 caption; Recent findings; REFERENCES AND RECOMMENDED READING, reference 23 annotation
- Pass A: PARTIALLY_COVERS - Nomogram classifying detrusor contractility versus outlet resistance distinguishes a contractility/underactivity component from the outlet that tamsulosin relaxes, bearing partially on 'outside tamsulosin's action' but methodological, not a tamsulosin-refractory finding.
- Pass B: NO_SEMANTIC_RELATION - Classifies detrusor vs outlet but in treatment-naive men with no tamsulosin link stated; relation to tamsulosin's action is only inferential; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The nomogram classifies 'detrusor underactivity relative to outlet resistance' in 'treatment-naïve men' and states nothing about tamsulosin; connecting it to tamsulosin's inadequacy requires an unstated assumption about tamsulosin's site of action.

### A1-H1-R4 x W-FRD-Q0019-01-Q0019
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on that reversible physiological component at clinically attainable exposures.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - PTX improved rat renal function only 'when given 60 minutes before ischemia'; kidney tissue, acute prophylactic timing and unshown clinical attainability fall outside the unit, and the results 'don't transfer to chronic bladder disease'.
- Pass B: PARTIALLY_COVERS - PTX engaged an ischemia/perfusion-related protection, but in rat kidney, pretreatment-only, at a dose not shown clinically attainable.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R6 x W-FRD-BOWTON-02-Q0006
- Unit (REQUIRED_SUPPORT): Trial slot (a), intervention and exposure, is specifiable from supported premises: agent, any required cointervention, route, dose, and duration at a clinically attainable exposure.
- Witness: Bowton et al. (bowton1989.pdf.md): in a randomized two-dose study of 10 patients with prior cerebrovascular disease, four given single oral 400 mg sustained-release pentoxifylline showed no statistically significant overall increase in normocarbic global cerebral blood flow across 2, 4, 6 hours (p=0.29); means were 101±8%, 101±15%, 110±15% of baseline (baseline 55.5±13.9 ml/100g/min). Cerebral bed, measured flow—not pelvic tissue function.
- Source: bowton1989.pdf.md Subjects and Methods; Results; TABLE 1, low-dose Air and CO₂ rows and footnotes
- Pass A: NO_SEMANTIC_RELATION - A single lower oral dose 'showed no statistically significant overall increase' in cerebral flow in four patients; it gives no evidence that a regimen yields the exposure a voiding effect requires, and the cerebral bed is outside scope.
- Pass B: PARTIALLY_COVERS - Specifies an oral PTX dose but single-dose in cerebrovascular patients with a null cerebral endpoint.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R6 x W-FRD-Q0001-01-Q0001
- Unit (REQUIRED_SUPPORT): Trial slot (a), intervention and exposure, is specifiable from supported premises: agent, any required cointervention, route, dose, and duration at a clinically attainable exposure.
- Witness: Shirazi et al. (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md): single-center randomized double-blind trial, 30 men per arm (all analyzed) with BPH/LUTS, giving pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day or placebo plus tamsulosin, 12 weeks. Post-void residual fell more with combination (−32.93±16.33 versus −13.17±9.23 mL; p<.001), but baseline residual differed (77.27 versus 50.37 mL; p=.18). Reported values, not validated or baseline-equivalent.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; 2 | METHODS; 2.3 | Study design; FIGURE 1; TABLE 1, PVR row; TABLE 4, PVR row
- Pass A: PARTIALLY_COVERS - Specifies agent, cointervention, dosing interval and duration (PTX every eight hours 'plus tamsulosin', 12 weeks) in BPH/LUTS men with a residual-volume effect, a material part of slot (a). Route and measured exposure are not stated, the population is not the specified cohort, and the effect is baseline-imbalanced.
- Pass B: WITNESS_ENTAILS_UNIT - Fully specifies agent, tamsulosin cointervention, oral route, dose (400mg q8h), 12-week duration at a clinical exposure in these men.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R6 x W-FRD-Q0011-01-Q0011
- Unit (REQUIRED_SUPPORT): Trial slot (a), intervention and exposure, is specifiable from supported premises: agent, any required cointervention, route, dose, and duration at a clinically attainable exposure.
- Witness: In Shirazi et al.'s single-center, randomized, double-blind 12-week BPH trial (60 men, 30/group), pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day versus placebo plus tamsulosin showed no significant between-group voided-volume change (0.80 versus +1.34 mL; p=.22) and no statistically significant within-group change (p=.90, .89). Baseline-to-endpoint voided-volume only—not residual or flow; visit schedule, onset, post-withdrawal persistence unestablished (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md, §3.3).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; §2.3 Study design; §3 Results; §3.3 Voided volume; Tables 2–4, voided-volume rows
- Pass A: PARTIALLY_COVERS - Specifies the regimen tested in BPH men (PTX every eight hours 'plus tamsulosin', 12 weeks), informing agent, cointervention, dosing and duration. The voided-volume endpoint was null and exposure unmeasured, so it does not show the regimen achieves the required effect.
- Pass B: WITNESS_ENTAILS_UNIT - Fully specifies agent, cointervention (tamsulosin), oral route, dose (400mg q8h), and 12-week duration at a clinically used exposure in these men; satisfies intervention/exposure specification.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R6 x W-FRD-Q0015-01-Q0015
- Unit (REQUIRED_SUPPORT): Trial slot (a), intervention and exposure, is specifiable from supported premises: agent, any required cointervention, route, dose, and duration at a clinically attainable exposure.
- Witness: In Parker et al.'s randomized, investigator-blinded porcine haemorrhage-plus-E.-coli-peritonitis experiment (female Large White pigs; n=5 per group), pentoxifylline plus colloid (20 mg/kg bolus, then 20 mg/kg over 60 minutes) gave lower median 2-hour MAP than colloid-plus-saline placebo: 62(10) versus 92(10) mmHg (P<0.01); by 6 hours groups did not differ. This is acute resuscitation, not chronic oral treatment (parker2000.pdf.md).
- Source: parker2000.pdf.md Abstract; §2.1 Animal preparation; §2.3 Experimental procedure; §3.1 Cardiovascular parameters, Table 1 caption, MAP rows and footnotes
- Pass A: NO_SEMANTIC_RELATION - IV bolus-plus-infusion in acutely septic, haemorrhaged pigs ('acute resuscitation, not chronic oral treatment') does not inform a clinically attainable regimen for the cohort.
- Pass B: PARTIALLY_COVERS - Weight-based IV animal regimen in acute resuscitation; not a clinically attainable human oral exposure for voiding.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R6 x W-FRD-Q0028-01-Q0028
- Unit (REQUIRED_SUPPORT): Trial slot (a), intervention and exposure, is specifiable from supported premises: agent, any required cointervention, route, dose, and duration at a clinically attainable exposure.
- Witness: Kruuse 2000, double-blind crossover in 10 healthy subjects: pentoxifylline 300 mg intravenously over 60 minutes versus saline, SPECT before and 55 and 115 minutes after infusion began. No significant over-time change in middle-cerebral-artery or global cerebral blood flow, corrected or uncorrected. pCO2-corrected changes did not differ between treatments; uncorrected changes did. Tests healthy cerebral perfusion, not ischemic bladder.
- Source: kruuse2000.pdf.md Material and methods; Procedure on the day of the study (Table 1); Results → Main study; Statistics; Figure 1 caption
- Pass A: NO_SEMANTIC_RELATION - IV PTX produced no significant cerebral-flow change in healthy subjects; it shows no regimen yielding the required effect and 'Tests healthy cerebral perfusion, not ischemic bladder'.
- Pass B: PARTIALLY_COVERS - Specifies PTX route/dose/duration (IV 300mg over 60min) but IV in healthy subjects with a cerebral endpoint; not the oral exposure the proposed bladder effect requires.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R7 x W-FRD-Q0044-01-Q0044
- Unit (REQUIRED_SUPPORT): Trial slot (b), phenotype, is specifiable from supported premises: measurable baseline characteristics, ascertainable before treatment, that identify the subgroup of these men proposed to respond.
- Witness: Fukabori-1996-uninhibited-bladder.pdf.md (English abstract, 'A CASE OF UNINHIBITED BLADDER...') reports one 60-year-old woman with pollakisuria, urge incontinence and urodynamic uninhibited contractions; after a failed anticholinergic, pentoxifylline (dose/route unstated) resolved incontinence and reduced pollakisuria by two weeks, with contractions absent and increased capacity by four weeks. Storage symptoms only; single case, not comparative efficacy.
- Source: Fukabori-1996-uninhibited-bladder.pdf.md English abstract under “A CASE OF UNINHIBITED BLADDER SUCCESSFULLY TREATED WITH PENTOXIFYLLINE”, paragraph beginning “A 60-year-old woman with pollakisuria and urge incontinence”
- Pass A: NO_SEMANTIC_RELATION - A single responding case cannot show that a baseline characteristic predicts PTX response (no comparison), and it concerns female storage symptoms, not this cohort's voiding difficulty.
- Pass B: PARTIALLY_COVERS - Measurable baseline urodynamic finding marked PTX response, but wrong sex and storage (not voiding) domain; single case.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The unit needs baseline characteristics that 'identify the subgroup of these men proposed to respond'; a 'single case, not comparative efficacy' has no non-responder comparison, so no baseline finding is shown to identify responders. The case is also a '60-year-old woman' with 'Storage symptoms only', so using uninhibited contractions as a phenotype premise for men with voiding difficulty would need unstated sex and symptom-domain transfers.

### A1-H1-R9 x W-FRD-Q0001-01-Q0001
- Unit (REQUIRED_SUPPORT): Trial slot (d), comparator, is specifiable from supported premises: a control or contrast that would distinguish the proposed PTX mechanism from the leading alternative explanation (for example tamsulosin, vitamin E, pelvic-floor treatment, combination effects, adherence, or contextual change).
- Witness: Shirazi et al. (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md): single-center randomized double-blind trial, 30 men per arm (all analyzed) with BPH/LUTS, giving pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day or placebo plus tamsulosin, 12 weeks. Post-void residual fell more with combination (−32.93±16.33 versus −13.17±9.23 mL; p<.001), but baseline residual differed (77.27 versus 50.37 mL; p=.18). Reported values, not validated or baseline-equivalent.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; 2 | METHODS; 2.3 | Study design; FIGURE 1; TABLE 1, PVR row; TABLE 4, PVR row
- Pass A: PARTIALLY_COVERS - 'placebo plus tamsulosin' versus PTX-plus-tamsulosin is the tamsulosin-only add-on contrast the unit names, isolating PTX from tamsulosin. But scope is general BPH/LUTS men (not the tamsulosin-inadequate, pelvic-floor-failure cohort), 'baseline residual differed', and pelvic-floor/contextual alternatives are uncontrolled, so coverage is partial.
- Pass B: WITNESS_ENTAILS_UNIT - Design identifies the placebo+tamsulosin comparator isolating PTX; baseline imbalance is an execution flaw, not absence of the comparator.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R9 x W-FRD-Q0001-02-r3-Q0001
- Unit (REQUIRED_SUPPORT): Trial slot (d), comparator, is specifiable from supported premises: a control or contrast that would distinguish the proposed PTX mechanism from the leading alternative explanation (for example tamsulosin, vitamin E, pelvic-floor treatment, combination effects, adherence, or contextual change).
- Witness: Shirazi et al. (2024, Lower Urinary Tract Symptoms) reported mean Qmax changes of 4.48 versus 2.67 mL/s; their arithmetic difference, 1.81 mL/s, is an analyst-derived unadjusted contrast favoring pentoxifylline-plus-tamsulosin over placebo-plus-tamsulosin, not a separately reported adjusted estimate. This BPH add-on trial does not establish pentoxifylline monotherapy or psychogenic-voiding efficacy.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Shirazi M et al. Lower Urinary Tract Symptoms. 2024;16(1):e12509. doi:10.1111/luts.12509. Exact source filename: `Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md`. Locations: TABLE 4; 2 | METHODS; 2.3 | Study design. Original locator: TABLE 4. Page numbers are unavailable in the supplied text.
- Pass A: PARTIALLY_COVERS - Supplies the same placebo-plus-tamsulosin contrast for Qmax, a tamsulosin-only control separating the PTX add-on effect. It is an 'analyst-derived unadjusted contrast' in BPH that 'does not establish ... monotherapy or psychogenic-voiding efficacy', so it does not fully specify the comparator for this cohort's leading alternative.
- Pass B: WITNESS_ENTAILS_UNIT - Same trial structure provides the tamsulosin-controlled PTX contrast, so the comparator is specifiable.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R9 x W-FRD-Q0009-02-Q0009
- Unit (REQUIRED_SUPPORT): Trial slot (d), comparator, is specifiable from supported premises: a control or contrast that would distinguish the proposed PTX mechanism from the leading alternative explanation (for example tamsulosin, vitamin E, pelvic-floor treatment, combination effects, adherence, or contextual change).
- Witness: Delanian et al. 2003, single-center randomized double-blind placebo-controlled 2×2 factorial trial in women with superficial radiation-induced fibrosis >6 months after breast radiotherapy (24 eligible, 22 with 6-month data). Combination pentoxifylline 800 mg/day plus vitamin E 1000 U/day gave −60.2% versus double-placebo −42.6% surface-area change (P=.038, Wilcoxon). Two-way ANOVA found no significant main effects, only a PTX×vitamin-E interaction trend (P=.09).
- Source: delanian2003.pdf.md PATIENTS AND METHODS; Randomization; Outcome Measures; Statistical Analysis; RESULTS; Primary Analyses; Table 3, surface Index 6 months, % row and boxhead note
- Pass A: PARTIALLY_COVERS - The 'randomized double-blind placebo-controlled 2×2 factorial' design is the vitamin-E-alone/combination contrast the unit names, and its result ('no significant main effects, only a PTX×vitamin-E interaction trend') shows it separates PTX from vitamin-E and combination effects. It is in women with breast radiation fibrosis, not voiding men, so transfer is required.
- Pass B: WITNESS_ENTAILS_UNIT - A 2x2 factorial with placebo and vitamin-E arms identifies the vitamin-E-/placebo-controlled contrast that isolates PTX, the comparator the unit names.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R9 x W-FRD-Q0011-01-Q0011
- Unit (REQUIRED_SUPPORT): Trial slot (d), comparator, is specifiable from supported premises: a control or contrast that would distinguish the proposed PTX mechanism from the leading alternative explanation (for example tamsulosin, vitamin E, pelvic-floor treatment, combination effects, adherence, or contextual change).
- Witness: In Shirazi et al.'s single-center, randomized, double-blind 12-week BPH trial (60 men, 30/group), pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day versus placebo plus tamsulosin showed no significant between-group voided-volume change (0.80 versus +1.34 mL; p=.22) and no statistically significant within-group change (p=.90, .89). Baseline-to-endpoint voided-volume only—not residual or flow; visit schedule, onset, post-withdrawal persistence unestablished (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md, §3.3).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; §2.3 Study design; §3 Results; §3.3 Voided volume; Tables 2–4, voided-volume rows
- Pass A: PARTIALLY_COVERS - The arms 'plus tamsulosin ... versus placebo plus tamsulosin' form a tamsulosin-only control for the PTX add-on effect (voided volume, p=.22). Population is general BPH men and pelvic-floor/contextual alternatives are not addressed, so it only partly specifies the comparator.
- Pass B: WITNESS_ENTAILS_UNIT - This design is exactly a tamsulosin-controlled comparison isolating PTX in BPH men, so a comparator separating PTX from tamsulosin is specifiable.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R9 x W-FRD-Q0013-01-Q0013
- Unit (REQUIRED_SUPPORT): Trial slot (d), comparator, is specifiable from supported premises: a control or contrast that would distinguish the proposed PTX mechanism from the leading alternative explanation (for example tamsulosin, vitamin E, pelvic-floor treatment, combination effects, adherence, or contextual change).
- Witness: Kassar et al.'s systematic review/meta-analysis of four depression RCTs (318 participants) found no significant difference in all-cause discontinuation between pentoxifylline and placebo: 14/159 versus 16/159; pooled RR 0.88 (95% CI 0.45-1.74; P=0.72). Dosing was 400 mg twice daily (one trial thrice), mostly added to an SSRI; no follow-up limited long-term safety; alpha-blocker-specific safety was not assessed (s00210-025-03845-1.pdf.md).
- Source: s00210-025-03845-1.pdf.md Kassar O et al. (2025), “Efficacy, safety and mechanistic insights of pentoxifylline in major depressive disorder: a systematic review and meta-analysis of randomized controlled trials,” DOI: 10.1007/s00210-025-03845-1. Exact source: `s00210-025-03845-1.pdf.md`, Results → “Discontinuation rate”; Fig. 6, “All causes of discontinuation rates”; Table 1, “Summary of the included studies” and its continuation; “Characteristics of the included studies”; “Limitations.” Original locator, Fig. 6, is correct. Reliable page numbers are not supplied in the markdown.
- Pass A: NO_SEMANTIC_RELATION - Pooled placebo-controlled discontinuation in depression trials ('mostly added to an SSRI') is a tolerability contrast; it does not identify a control separating a PTX voiding effect from the unit's alternatives.
- Pass B: PARTIALLY_COVERS - Identifies a PTX-vs-placebo comparator, but outcome is tolerability in depression.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R9 x W-FRD-Q0015-01-Q0015
- Unit (REQUIRED_SUPPORT): Trial slot (d), comparator, is specifiable from supported premises: a control or contrast that would distinguish the proposed PTX mechanism from the leading alternative explanation (for example tamsulosin, vitamin E, pelvic-floor treatment, combination effects, adherence, or contextual change).
- Witness: In Parker et al.'s randomized, investigator-blinded porcine haemorrhage-plus-E.-coli-peritonitis experiment (female Large White pigs; n=5 per group), pentoxifylline plus colloid (20 mg/kg bolus, then 20 mg/kg over 60 minutes) gave lower median 2-hour MAP than colloid-plus-saline placebo: 62(10) versus 92(10) mmHg (P<0.01); by 6 hours groups did not differ. This is acute resuscitation, not chronic oral treatment (parker2000.pdf.md).
- Source: parker2000.pdf.md Abstract; §2.1 Animal preparation; §2.3 Experimental procedure; §3.1 Cardiovascular parameters, Table 1 caption, MAP rows and footnotes
- Pass A: NO_SEMANTIC_RELATION - A colloid-plus-saline placebo in acute porcine haemorrhage/peritonitis ('acute resuscitation, not chronic oral treatment') is a hemodynamic control unrelated to distinguishing a PTX voiding effect from the named alternatives.
- Pass B: PARTIALLY_COVERS - Placebo-controlled PTX add-on design isolating PTX, but porcine sepsis.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R9 x W-FRD-Q0019-01-Q0019
- Unit (REQUIRED_SUPPORT): Trial slot (d), comparator, is specifiable from supported premises: a control or contrast that would distinguish the proposed PTX mechanism from the leading alternative explanation (for example tamsulosin, vitamin E, pelvic-floor treatment, combination effects, adherence, or contextual change).
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Saline-controlled timing arms in rat renal ischemia ('don't transfer to chronic bladder disease') identify no comparator for separating PTX from the voiding alternatives in the unit.
- Pass B: PARTIALLY_COVERS - Provides a PTX-vs-control design isolating PTX, but renal ischemia model.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H1-R9 x W-FRD-Q0028-01-Q0028
- Unit (REQUIRED_SUPPORT): Trial slot (d), comparator, is specifiable from supported premises: a control or contrast that would distinguish the proposed PTX mechanism from the leading alternative explanation (for example tamsulosin, vitamin E, pelvic-floor treatment, combination effects, adherence, or contextual change).
- Witness: Kruuse 2000, double-blind crossover in 10 healthy subjects: pentoxifylline 300 mg intravenously over 60 minutes versus saline, SPECT before and 55 and 115 minutes after infusion began. No significant over-time change in middle-cerebral-artery or global cerebral blood flow, corrected or uncorrected. pCO2-corrected changes did not differ between treatments; uncorrected changes did. Tests healthy cerebral perfusion, not ischemic bladder.
- Source: kruuse2000.pdf.md Material and methods; Procedure on the day of the study (Table 1); Results → Main study; Statistics; Figure 1 caption
- Pass A: NO_SEMANTIC_RELATION - A saline-controlled crossover of IV PTX on healthy cerebral flow ('Tests healthy cerebral perfusion, not ischemic bladder') does not identify a comparator distinguishing a PTX voiding mechanism from the unit's alternatives.
- Pass B: PARTIALLY_COVERS - Demonstrates a placebo (saline)-controlled PTX contrast, but in healthy cerebral perfusion, not the named alternatives.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H2-C2 x W-FRD-Q0027-01-Q0027
- Unit (CONTEXTUAL_CONSTRAINT): H2 targets the materially supported rationale as it currently stands in the ledger, not every route that could be imagined.
- Witness: Neuner et al. (immunology00076-0102.pdf.md) studied four healthy volunteers overall; the two-day-regimen subgroup size is unspecified. Oral PTX 5×400 mg/day for two days significantly suppressed TNF-α, IL-1β, IL-6 and IL-8 release from day-7 PBMC cultured 24 hours, with or without LPS 1 µg/mL. These are ex-vivo endpoints after in-vivo dosing; plasma/tissue exposure and clinical urinary efficacy were unmeasured.
- Source: immunology00076-0102.pdf.md P. Neuner et al., “Pentoxifylline in vivo down-regulates the release of IL-1 β, IL-6, IL-8 and tumour necrosis factor-α by human peripheral blood mononuclear cells.” Exact source: `immunology00076-0102.pdf.md`; MATERIALS AND METHODS → Human volunteers; Preparation of PBMC; RESULTS → In vivo effects of orally applied PTX on cytokine production by PBMC, first paragraph; Figure 1 original caption. The original results locator is correct. Journal, volume, pagination and publication date are not established by the supplied article metadata; receipt and acceptance dates are supplied but are not publication dates.
- Pass A: PARTIALLY_COVERS - Documents a reported PTX biological effect (cytokine suppression after oral dosing) with 'clinical urinary efficacy ... unmeasured', so a marker-function mismatch built on it would bear on an evidenced anti-inflammatory route. Whether that route is materially supported for voiding is not shown in the text.
- Pass B: NO_SEMANTIC_RELATION - A finding, not about supported-route scope; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The unit is a scope rule whose actor is H2 ('H2 targets the materially supported rationale as it currently stands in the ledger'); the witness is an empirical PTX cytokine finding with 'clinical urinary efficacy were unmeasured' and states nothing about H2's target or which routes the ledger supports. Calling the anti-inflammatory route materially supported for voiding is an inference the witness does not make.

### A1-H2-C2 x W-FRD-Q0029-01-Q0029
- Unit (CONTEXTUAL_CONSTRAINT): H2 targets the materially supported rationale as it currently stands in the ledger, not every route that could be imagined.
- Witness: Dezube et al. 1993, pilot study of seven adult cancer patients treated on eight occasions for 1–3 weeks with oral controlled-release pentoxifylline 400 mg every eight hours. On all three occasions when baseline PBMC TNF/β-actin RNA ratios exceeded the healthy-volunteer normal range, ratios fell within one week; on five occasions within normal range, no reduction. Target-engagement, not clinical benefit.
- Source: dezube1993.pdf.md Materials and methods → Patient characteristics, Treatment plan, TNF RNA assay; Results → TNF/actin ratios in vivo → Normal volunteers; Results → Suppression of TNF/actin ratios by pentoxifylline in vivo; Fig. 3 caption; Discussion, paragraph beginning “In this pilot study, TNF was measured”
- Pass A: PARTIALLY_COVERS - Reports PTX target engagement on PBMC TNF RNA, 'not clinical benefit', bearing on an evidenced anti-inflammatory route that a marker-function mismatch would target. Material support of that route for voiding is not established by the text.
- Pass B: NO_SEMANTIC_RELATION - A finding, not a statement about supported routes; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports PBMC TNF RNA reduction in cancer patients, labelled 'Target-engagement, not clinical benefit'; it makes no statement about H2's scope or the ledger's supported rationale (different actor and predicate), so it neither supports nor contradicts the scope rule.

### A1-H2-C2 x W-FRD-Q0044-01-Q0044
- Unit (CONTEXTUAL_CONSTRAINT): H2 targets the materially supported rationale as it currently stands in the ledger, not every route that could be imagined.
- Witness: Fukabori-1996-uninhibited-bladder.pdf.md (English abstract, 'A CASE OF UNINHIBITED BLADDER...') reports one 60-year-old woman with pollakisuria, urge incontinence and urodynamic uninhibited contractions; after a failed anticholinergic, pentoxifylline (dose/route unstated) resolved incontinence and reduced pollakisuria by two weeks, with contractions absent and increased capacity by four weeks. Storage symptoms only; single case, not comparative efficacy.
- Source: Fukabori-1996-uninhibited-bladder.pdf.md English abstract under “A CASE OF UNINHIBITED BLADDER SUCCESSFULLY TREATED WITH PENTOXIFYLLINE”, paragraph beginning “A 60-year-old woman with pollakisuria and urge incontinence”
- Pass A: PARTIALLY_COVERS - A human PTX bladder response (absent uninhibited contractions, increased capacity) bears on a bladder route with case-level support; as mismatch evidence it would bear on the disease-process difference ('Storage symptoms only'). Single case, so material support is limited.
- Pass B: NO_SEMANTIC_RELATION - A finding, not a scope statement; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - A single case of PTX response in a woman with 'Storage symptoms only' is an empirical finding; the unit is a rule about which rationale H2 addresses, and the witness says nothing about H2, the ledger, or which routes are materially supported.

### A1-H2-C2 x W-FRD-SHIRAZI2015-01-Q0002
- Unit (CONTEXTUAL_CONSTRAINT): H2 targets the materially supported rationale as it currently stands in the ledger, not every route that could be imagined.
- Witness: In male Sprague-Dawley rats with surgically induced partial bladder outlet obstruction, Shirazi et al. gave pentoxifylline 100 mg/kg/day by oral gavage for four weeks after obstruction induction, associated with higher electrically evoked isolated-detrusor-strip tension than water controls (approximately 4.0 ± 1.0 versus 1.8 ± 0.4 g per 100 mg tissue; reported P=0.023). These figure-derived values are approximate (shirazi2015.pdf.md, Results).
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Results; Fig. 3
- Pass A: PARTIALLY_COVERS - PTX-associated higher detrusor-strip tension in obstructed rats identifies a bladder-contractility route with material preclinical support that H2 would need to target. It is supportive, not itself a mismatch finding.
- Pass B: NO_SEMANTIC_RELATION - A finding, not a claim about supported-route scope; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Higher 'electrically evoked isolated-detrusor-strip tension' in obstructed rats is evidence about PTX, not about what H2 targets; the unit's actor is H2 and its predicate is a scoping commitment, which the witness neither asserts nor denies. Whether this route belongs to the ledger's supported rationale is bookkeeping outside the witness text.

### A1-H2-C2 x W-FRD-SHIRAZI2015-02-Q0002
- Unit (CONTEXTUAL_CONSTRAINT): H2 targets the materially supported rationale as it currently stands in the ledger, not every route that could be imagined.
- Witness: Shirazi 2015: in male Sprague-Dawley rats with partial bladder outlet obstruction, pentoxifylline 100 mg/kg/day by oral gavage for four weeks, begun after obstruction induction, produced no significant improvement in maximum carbachol-induced detrusor-strip contractile tension versus water-treated obstructed controls (20 animals per group; all completed). Treatment addressed established obstruction, not prevention; this is a functional contractility null.
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Abstract → Results; Results and Fig. 2
- Pass A: PARTIALLY_COVERS - A four-week PTX null on carbachol-induced detrusor tension in obstructed rats is mismatch-type evidence on the same evidenced bladder-contractility route, so it bears on the supported rationale rather than an imagined one; it is preclinical and one functional measure.
- Pass B: NO_SEMANTIC_RELATION - An empirical finding, not a statement about which routes are materially supported in the ledger; no relation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - A four-week 'functional contractility null' on carbachol-induced detrusor tension in obstructed rats is an empirical finding; it says nothing about H2's scope or which routes the ledger treats as materially supported (different actor and predicate), so it cannot support or contradict the rule.

### A1-H2-C3 x W-FRD-Q0009-02-Q0009
- Unit (CONTEXTUAL_CONSTRAINT): The absence of clinical trials alone does not corroborate H2.
- Witness: Delanian et al. 2003, single-center randomized double-blind placebo-controlled 2×2 factorial trial in women with superficial radiation-induced fibrosis >6 months after breast radiotherapy (24 eligible, 22 with 6-month data). Combination pentoxifylline 800 mg/day plus vitamin E 1000 U/day gave −60.2% versus double-placebo −42.6% surface-area change (P=.038, Wilcoxon). Two-way ANOVA found no significant main effects, only a PTX×vitamin-E interaction trend (P=.09).
- Source: delanian2003.pdf.md PATIENTS AND METHODS; Randomization; Outcome Measures; Statistical Analysis; RESULTS; Primary Analyses; Table 3, surface Index 6 months, % row and boxhead note
- Pass A: NO_SEMANTIC_RELATION - This constraint requires every H2 coverage set to rest on affirmative mismatch findings rather than mere absence of trials; a single source finding does not establish or refute that bookkeeping rule.
- Pass B: PARTIALLY_COVERS - Affirmative PTX structural effect in skin fibrosis; mismatch fragment, combination/women.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The unit is an epistemic rule that 'absence of clinical trials alone does not corroborate H2'; the witness reports a positive randomized PTX-plus-vitamin-E trial in breast radiation fibrosis (P=.038) and says nothing about trial absence or what corroborates H2, so it neither supports nor contradicts the rule.

### A1-H2-C3 x W-FRD-Q0009-03-Q0009
- Unit (CONTEXTUAL_CONSTRAINT): The absence of clinical trials alone does not corroborate H2.
- Witness: Delanian et al.'s follow-up of women with superficial breast radiation-induced fibrosis on pentoxifylline 800 mg/day plus vitamin E 1,000 U/day found that, after stopping, fibrosis surface area rebounded more after short (6-12-month) treatment than long (24-48-month) treatment: 40%/year (95% CI 24-56) versus 8.5%/year (95% CI 1-16); P=.0012. Duration was not randomized; follow-up lasted two years (delanian2005.pdf.md).
- Source: delanian2005.pdf.md Modalities of Combined PTX-vitE Treatment; Statistical Analysis; Primary Analyses, paragraph beginning “After stopping PTX-vitE: Rebound effect”; DISCUSSION, paragraph beginning “Long-term follow-up of our patients”
- Pass A: NO_SEMANTIC_RELATION - This constraint requires every H2 coverage set to rest on affirmative mismatch findings rather than mere absence of trials; a single source finding does not establish or refute that bookkeeping rule.
- Pass B: PARTIALLY_COVERS - Affirmative PTX action on skin fibrosis; a tissue/disease mismatch fragment requiring transfer.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - A follow-up comparison of fibrosis rebound after short versus long PTX-plus-vitamin-E treatment ('Duration was not randomized') is an empirical finding with no statement about whether absence of clinical trials corroborates H2; the rule's predicate is untouched.

### A1-H2-C3 x W-FRD-Q0011-01-Q0011
- Unit (CONTEXTUAL_CONSTRAINT): The absence of clinical trials alone does not corroborate H2.
- Witness: In Shirazi et al.'s single-center, randomized, double-blind 12-week BPH trial (60 men, 30/group), pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day versus placebo plus tamsulosin showed no significant between-group voided-volume change (0.80 versus +1.34 mL; p=.22) and no statistically significant within-group change (p=.90, .89). Baseline-to-endpoint voided-volume only—not residual or flow; visit schedule, onset, post-withdrawal persistence unestablished (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md, §3.3).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; §2.3 Study design; §3 Results; §3.3 Voided volume; Tables 2–4, voided-volume rows
- Pass A: NO_SEMANTIC_RELATION - This constraint requires every H2 coverage set to rest on affirmative mismatch findings rather than mere absence of trials; a single source finding does not establish or refute that bookkeeping rule.
- Pass B: PARTIALLY_COVERS - Affirmative in-scope null (no voided-volume benefit) is a qualifying affirmative mismatch finding; combination limits attribution, so partial.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports a clinical trial's voided-volume null (p=.22), which is neither an absence of trials nor a claim about what corroborates H2; whether that null is itself mismatch evidence is a separate question from this rule.

### A1-H2-C3 x W-FRD-Q0015-01-Q0015
- Unit (CONTEXTUAL_CONSTRAINT): The absence of clinical trials alone does not corroborate H2.
- Witness: In Parker et al.'s randomized, investigator-blinded porcine haemorrhage-plus-E.-coli-peritonitis experiment (female Large White pigs; n=5 per group), pentoxifylline plus colloid (20 mg/kg bolus, then 20 mg/kg over 60 minutes) gave lower median 2-hour MAP than colloid-plus-saline placebo: 62(10) versus 92(10) mmHg (P<0.01); by 6 hours groups did not differ. This is acute resuscitation, not chronic oral treatment (parker2000.pdf.md).
- Source: parker2000.pdf.md Abstract; §2.1 Animal preparation; §2.3 Experimental procedure; §3.1 Cardiovascular parameters, Table 1 caption, MAP rows and footnotes
- Pass A: NO_SEMANTIC_RELATION - This constraint requires every H2 coverage set to rest on affirmative mismatch findings rather than mere absence of trials; a single source finding does not establish or refute that bookkeeping rule.
- Pass B: PARTIALLY_COVERS - Affirmative finding of acute-only action (lowers MAP acutely, gone by 6h); a disease-process/timing mismatch fragment, wrong model.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - An acute porcine resuscitation result (lower 2-hour MAP; 'by 6 hours groups did not differ') does not address the rule's subject, the evidential weight of an 'absence of clinical trials', so it neither establishes nor refutes the constraint.

### A1-H2-C3 x W-FRD-Q0019-01-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): The absence of clinical trials alone does not corroborate H2.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - This constraint requires every H2 coverage set to rest on affirmative mismatch findings rather than mere absence of trials; a single source finding does not establish or refute that bookkeeping rule.
- Pass B: PARTIALLY_COVERS - Affirmative finding (benefit only pre-injury) is the kind of mismatch the constraint requires H2 to rest on; non-bladder model, so partial.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - A renal-protection result in rats seen 'only when given 60 minutes before ischemia' makes no statement about trial absence or about what corroborates H2; the unit is a corroboration rule and the witness is unrelated to its predicate.

### A1-H2-E1 x W-FRD-Q0016-01-Q0016
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate an affirmative failure of a necessary link: insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another necessary-link failure.
- Witness: In Ridings et al.'s nonrandomized controlled porcine sepsis experiment (ridings1994.pdf.md, COMMENT), intravenous pentoxifylline (20 mg/kg bolus, 6 mg/kg/h) begun two hours after Pseudomonas infusion (established, uncorrected shock) was followed by fatal hypotension within one hour in 2/4 animals; two survivors resembled 1-hour-treated protection (data not shown). Authors attributed deaths to pentoxifylline but said n=4 precluded statistics; untransferable to bladder dysfunction.
- Source: ridings1994.pdf.md Abstract: Design, Interventions, Results; MATERIALS AND METHODS → THE PORCINE MODEL and EXPERIMENTAL DESIGN; RESULTS opening paragraph; COMMENT, “In our studies, the administration of pentoxifylline 2 hours” and “If pentoxifylline is administered to animals in uncorrected septic shock”
- Pass A: NO_SEMANTIC_RELATION - Late-IV-PTX hypotension in porcine sepsis, n=4 without statistics and described as 'untransferable to bladder dysfunction'; not a necessary-link failure in a relevant model.
- Pass B: PARTIALLY_COVERS - Affirmative finding that PTX given to an established condition fails/harms (fatal hypotension); incompatible-timing failure but sepsis model, n=4, transfer needed.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H2-R1 x W-FRD-BOWTON-01-Q0006
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between PTX's reported biological effects and the dysfunction driving impaired voiding in this cohort, in at least one of: exposure, tissue, disease process, timing, or the relationship between a biological marker and urinary function.
- Witness: Bowton et al. (bowton1989.pdf.md): in a ten-patient study of prior cerebrovascular disease, six given single oral 800 mg sustained-release pentoxifylline showed increased normocarbic global cerebral blood flow (xenon-133) from 52.5±15.2 to 59.4, 58.2, 62.4 mL/100g/min at 2, 4, 6 hours (p≤0.01–0.02; overall p=0.017). No concurrent placebo arm. Cerebral measured flow, not pelvic tissue function.
- Source: bowton1989.pdf.md TABLE 1, high-dose (800 mg), Air rows and statistical footnote; Subjects and Methods; Results; Discussion
- Pass A: NO_SEMANTIC_RELATION - Reports a PTX-associated cerebral-flow increase; 'not pelvic tissue function' marks a scope limit, not affirmative evidence that PTX's effect fails to reach the voiding dysfunction.
- Pass B: PARTIALLY_COVERS - PTX 800mg raised cerebral blood flow; PTX acts on perfusion but in brain, not the voiding dysfunction - tissue-mismatch component, transfer needed.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports a PTX-associated increase in cerebral blood flow (affirmed effect, cerebral tissue); 'not pelvic tissue function' marks an unmeasured tissue, not affirmative evidence that PTX's effect fails to reach or matter for the cohort's voiding dysfunction. A tissue-mismatch reading would need an unstated assumption that cerebral findings do not apply to pelvic tissue.

### A1-H2-R1 x W-FRD-BOWTON-02-Q0006
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between PTX's reported biological effects and the dysfunction driving impaired voiding in this cohort, in at least one of: exposure, tissue, disease process, timing, or the relationship between a biological marker and urinary function.
- Witness: Bowton et al. (bowton1989.pdf.md): in a randomized two-dose study of 10 patients with prior cerebrovascular disease, four given single oral 400 mg sustained-release pentoxifylline showed no statistically significant overall increase in normocarbic global cerebral blood flow across 2, 4, 6 hours (p=0.29); means were 101±8%, 101±15%, 110±15% of baseline (baseline 55.5±13.9 ml/100g/min). Cerebral bed, measured flow—not pelvic tissue function.
- Source: bowton1989.pdf.md Subjects and Methods; Results; TABLE 1, low-dose Air and CO₂ rows and footnotes
- Pass A: NO_SEMANTIC_RELATION - A nonsignificant cerebral-flow result after a single lower dose in four patients is not affirmative evidence of an exposure mismatch and comes from a cerebral bed, not a cohort-relevant model.
- Pass B: PARTIALLY_COVERS - PTX 400mg produced no cerebral-flow rise; a PTX perfusion effect absent in a non-bladder tissue - partial tissue-mismatch component.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - A nonsignificant (p=0.29) cerebral-flow result after a single 400 mg dose in four patients is an underpowered null in a different tissue and exposure pattern, not affirmative evidence that 'demonstrates a consequential mismatch' with the cohort's dysfunction. The witness itself limits scope to 'Cerebral bed, measured flow—not pelvic tissue function'.

### A1-H2-R1 x W-FRD-Q0007-01-Q0007
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between PTX's reported biological effects and the dysfunction driving impaired voiding in this cohort, in at least one of: exposure, tissue, disease process, timing, or the relationship between a biological marker and urinary function.
- Witness: Nisi et al. (nisi2013.pdf.md, Table 2; Methods) gave 20 chronic-heart-failure patients one sustained-release 600-mg oral PTX tablet fasting. Parent-PTX plasma Tpeak was 1.64 ± 0.92 versus 3.89 ± 1.90 h (NYHA II, n=11; III/IV, n=9; P=.0077); Cmax 719 ± 403 versus 833 ± 524 ng/mL (NS), mean ± SD. Plasma values only—no tissue, unbound, metabolite or half-life—not urinary-benefit timing.
- Source: nisi2013.pdf.md Results, Table 2, PTX block, Tpeak row and Mean/SD headers; Methods → Patients and Treatments, Pharmacokinetic Study; Methods, Pharmacokinetic Analysis
- Pass A: NO_SEMANTIC_RELATION - Reports plasma PTX kinetics; 'Plasma values only—no tissue' is missing information, not affirmative evidence that tissue exposure is inadequate.
- Pass B: PARTIALLY_COVERS - Plasma PK only (CHF), no tissue/metabolite/function; bears on the exposure dimension but does not itself demonstrate failure to reach bladder.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Single-dose plasma kinetics in heart-failure patients show plasma exposure was reached (Cmax 719-833 ng/mL); 'Plasma values only—no tissue' records missing information, not an affirmative finding that exposure at the voiding-relevant tissue is inadequate. No mismatch with the cohort's dysfunction is asserted on any of the unit's dimensions.

### A1-H2-R1 x W-FRD-Q0009-02-Q0009
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between PTX's reported biological effects and the dysfunction driving impaired voiding in this cohort, in at least one of: exposure, tissue, disease process, timing, or the relationship between a biological marker and urinary function.
- Witness: Delanian et al. 2003, single-center randomized double-blind placebo-controlled 2×2 factorial trial in women with superficial radiation-induced fibrosis >6 months after breast radiotherapy (24 eligible, 22 with 6-month data). Combination pentoxifylline 800 mg/day plus vitamin E 1000 U/day gave −60.2% versus double-placebo −42.6% surface-area change (P=.038, Wilcoxon). Two-way ANOVA found no significant main effects, only a PTX×vitamin-E interaction trend (P=.09).
- Source: delanian2003.pdf.md PATIENTS AND METHODS; Randomization; Outcome Measures; Statistical Analysis; RESULTS; Primary Analyses; Table 3, surface Index 6 months, % row and boxhead note
- Pass A: NO_SEMANTIC_RELATION - A significant combination effect with nonsignificant main effects in breast radiation fibrosis is not affirmative evidence that PTX's effect fails to reach or translate into the cohort's voiding dysfunction.
- Pass B: PARTIALLY_COVERS - PTX+vitE acts on skin radiation-fibrosis in women; PTX effect in a different tissue/disease with cointervention - a mismatch component, transfer needed.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports a PTX-plus-vitamin-E combination effect on breast radiation fibrosis with 'no significant main effects' and says nothing about the dysfunction driving impaired voiding in this cohort. Treating it as a tissue or disease-process mismatch needs an unstated link from skin fibrosis to the cohort, and a nonsignificant main effect in 22 women is not affirmative evidence of an absent effect.

### A1-H2-R1 x W-FRD-Q0016-01-Q0016
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between PTX's reported biological effects and the dysfunction driving impaired voiding in this cohort, in at least one of: exposure, tissue, disease process, timing, or the relationship between a biological marker and urinary function.
- Witness: In Ridings et al.'s nonrandomized controlled porcine sepsis experiment (ridings1994.pdf.md, COMMENT), intravenous pentoxifylline (20 mg/kg bolus, 6 mg/kg/h) begun two hours after Pseudomonas infusion (established, uncorrected shock) was followed by fatal hypotension within one hour in 2/4 animals; two survivors resembled 1-hour-treated protection (data not shown). Authors attributed deaths to pentoxifylline but said n=4 precluded statistics; untransferable to bladder dysfunction.
- Source: ridings1994.pdf.md Abstract: Design, Interventions, Results; MATERIALS AND METHODS → THE PORCINE MODEL and EXPERIMENTAL DESIGN; RESULTS opening paragraph; COMMENT, “In our studies, the administration of pentoxifylline 2 hours” and “If pentoxifylline is administered to animals in uncorrected septic shock”
- Pass A: NO_SEMANTIC_RELATION - Timing-dependent hypotension in porcine sepsis, where 'n=4 precluded statistics' and the result is 'untransferable to bladder dysfunction'; not affirmative mismatch evidence from a cohort-relevant model.
- Pass B: PARTIALLY_COVERS - PTX in porcine sepsis caused harm and is explicitly untransferable to bladder; a disease-process/model mismatch component, transfer needed.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Fatal hypotension after late intravenous PTX in porcine sepsis, where 'n=4 precluded statistics', is not affirmative mismatch evidence about the cohort's voiding dysfunction. The witness itself calls the finding 'untransferable to bladder dysfunction', blocking the transfer that partial coverage would require.

### A1-H2-R1 x W-FRD-Q0027-01-Q0027
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between PTX's reported biological effects and the dysfunction driving impaired voiding in this cohort, in at least one of: exposure, tissue, disease process, timing, or the relationship between a biological marker and urinary function.
- Witness: Neuner et al. (immunology00076-0102.pdf.md) studied four healthy volunteers overall; the two-day-regimen subgroup size is unspecified. Oral PTX 5×400 mg/day for two days significantly suppressed TNF-α, IL-1β, IL-6 and IL-8 release from day-7 PBMC cultured 24 hours, with or without LPS 1 µg/mL. These are ex-vivo endpoints after in-vivo dosing; plasma/tissue exposure and clinical urinary efficacy were unmeasured.
- Source: immunology00076-0102.pdf.md P. Neuner et al., “Pentoxifylline in vivo down-regulates the release of IL-1 β, IL-6, IL-8 and tumour necrosis factor-α by human peripheral blood mononuclear cells.” Exact source: `immunology00076-0102.pdf.md`; MATERIALS AND METHODS → Human volunteers; Preparation of PBMC; RESULTS → In vivo effects of orally applied PTX on cytokine production by PBMC, first paragraph; Figure 1 original caption. The original results locator is correct. Journal, volume, pagination and publication date are not established by the supplied article metadata; receipt and acceptance dates are supplied but are not publication dates.
- Pass A: NO_SEMANTIC_RELATION - Shows a marker change after oral PTX with 'clinical urinary efficacy ... unmeasured'; an unmeasured urinary outcome is not the affirmative marker-change-without-urinary-change the unit requires.
- Pass B: PARTIALLY_COVERS - PTX engages cytokine markers ex vivo in healthy volunteers with tissue exposure and urinary efficacy unmeasured; supplies a marker-without-urinary-function component of a mismatch, not in-cohort.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The unit's marker-function dimension requires an affirmative dissociation between a marker and urinary function, but here cytokine release changed while 'clinical urinary efficacy were unmeasured', which is missing data, not a demonstrated mismatch. The population (healthy volunteers) and ex-vivo PBMC endpoints are also outside the cohort.

### A1-H3-C1 x W-FRD-Q0020-01-Q0020
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; the uncertainty is not merely an artifact of an unfinished investigation.
- Witness: Yu and Jeong's clinical literature review (2020ICU_icu-58-S68.pdf.md, PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY) reports most published detrusor-underactivity prevalence data came from community-dwelling cohorts with significant LUTS judged by arbitrary urodynamic criteria (25%–48% elderly men, 12%–24% women), with limited general-population applicability. Community-based research is described as rare, not absent; one study used free Qmax and post-void residual, not pressure-flow parameters.
- Source: 2020ICU_icu-58-S68.pdf.md Author byline; opening abstract; PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY, concluding two paragraphs and paragraph beginning “Unlike other researchers, Groutz et al.”
- Pass A: PARTIALLY_COVERS - A review-level statement that detrusor-underactivity prevalence data rest on 'arbitrary urodynamic criteria' and that community research is 'rare' indicates a literature-level rather than retrieval-artifact gap on a phenotype link. But 'rare, not absent' signals further retrieval could add data, so it bears only partly on the constraint.
- Pass B: NO_SEMANTIC_RELATION - Unit is a process claim about whether retrieval and adverse testing are complete; this substantive finding says nothing about the completeness of the investigation.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A1-H3-E3 x W-FRD-Q0017-01-Q0017
- Unit (CORROBORATING_EXPECTATION): The investigation identifies the experiment that would resolve the localized uncertainty.
- Witness: In Kaplan et al.'s retrospective study of 43 men with pseudodyssynergia previously misdiagnosed as chronic nonbacterial prostatitis, success of biofeedback was defined as a decrease in symptoms of at least 50% on two consecutive office visits, using the American Urological Association symptom score. This definition measures symptom response, not attendance, completion, or abandonment (kaplan1997.pdf.md, Materials and Methods).
- Source: kaplan1997.pdf.md MATERIALS AND METHODS; paragraphs beginning “A retrospective analysis,” “Patient symptoms were evaluated,” and “Biofeedback training”
- Pass A: PARTIALLY_COVERS - Names a specific source-defined measurement, biofeedback success as 'a decrease in symptoms of at least 50% on two consecutive office visits' on the AUA score, that could operationalize pelvic-floor treatment failure for the phenotype link. It is not proposed as resolving the PTX uncertainty and 'measures symptom response, not attendance, completion, or abandonment', so it covers only part.
- Pass B: NO_SEMANTIC_RELATION - Not an experiment recommendation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness gives Kaplan's biofeedback success definition ('a decrease in symptoms of at least 50% on two consecutive office visits'); it names no experiment and no uncertainty, and the unit's actor is 'the investigation', not this source. Treating it as part of a resolving PTX experiment needs unstated assumptions about what the localized uncertainty is and that this endpoint would be used.

### A1-H3-E3 x W-FRD-Q0029-01-Q0029
- Unit (CORROBORATING_EXPECTATION): The investigation identifies the experiment that would resolve the localized uncertainty.
- Witness: Dezube et al. 1993, pilot study of seven adult cancer patients treated on eight occasions for 1–3 weeks with oral controlled-release pentoxifylline 400 mg every eight hours. On all three occasions when baseline PBMC TNF/β-actin RNA ratios exceeded the healthy-volunteer normal range, ratios fell within one week; on five occasions within normal range, no reduction. Target-engagement, not clinical benefit.
- Source: dezube1993.pdf.md Materials and methods → Patient characteristics, Treatment plan, TNF RNA assay; Results → TNF/actin ratios in vivo → Normal volunteers; Results → Suppression of TNF/actin ratios by pentoxifylline in vivo; Fig. 3 caption; Discussion, paragraph beginning “In this pilot study, TNF was measured”
- Pass A: NO_SEMANTIC_RELATION - Reports PBMC TNF RNA target engagement in cancer patients, 'not clinical benefit'; it does not identify a measurement or experiment to resolve the voiding-trial uncertainty.
- Pass B: PARTIALLY_COVERS - Names a candidate stratifying measurement (baseline TNF) for the response/phenotype link; cancer context.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports baseline-dependent PBMC TNF RNA reduction in cancer patients ('Target-engagement, not clinical benefit') and proposes no experiment; using baseline TNF to stratify a voiding trial is the reader's inference, not the witness's statement, and does not show the investigation identifying a resolving experiment.

### A1-H3-E3 x W-FRD-Q0048-01-Q0048
- Unit (CORROBORATING_EXPECTATION): The investigation identifies the experiment that would resolve the localized uncertainty.
- Witness: Shirazi et al.'s double-blind randomized 12-week BPH trial reports comparisons by t-test, Wilcoxon, and Mann–Whitney tests, with significance at p≤0.05; no ANCOVA or baseline-PVR-adjusted model is reported. The analysis set was participants receiving medication throughout (60 randomized, 30 per group, no exclusions). Whether change dispersion is SD or SE is not stated in this methods text.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md §2.4 | Statistical analyses; §2.3 | Study design, Figure 1; §3 | RESULTS; Abstract, Materials and Methods
- Pass A: PARTIALLY_COVERS - Names the specific missing analysis ('no ANCOVA or baseline-PVR-adjusted model is reported') for the PTX-plus-tamsulosin trial, an analysis capable of resolving the baseline-imbalance uncertainty in its residual contrast. It is a reported absence rather than a source recommendation and addresses one link only.
- Pass B: NO_SEMANTIC_RELATION - Does not name an experiment to resolve mechanism uncertainty.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports an analytic absence ('no ANCOVA or baseline-PVR-adjusted model is reported') in one trial's methods, not an experiment, and the unit's actor is 'the investigation'. Linking this absence to 'the localized uncertainty' and counting a reanalysis as 'the experiment' both rest on assumptions the witness does not state.

### A1-H3-R1 x W-FRD-Q0001-01-Q0001
- Unit (REQUIRED_SUPPORT): Existing evidence affirmatively supports some components of H1, that is, at least one link in the chain from clinically attainable PTX or metabolite exposure, through a relevant biological target and tissue effect, to changed voiding function, an identifiable patient subgroup, and a measurable trial prediction.
- Witness: Shirazi et al. (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md): single-center randomized double-blind trial, 30 men per arm (all analyzed) with BPH/LUTS, giving pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day or placebo plus tamsulosin, 12 weeks. Post-void residual fell more with combination (−32.93±16.33 versus −13.17±9.23 mL; p<.001), but baseline residual differed (77.27 versus 50.37 mL; p=.18). Reported values, not validated or baseline-equivalent.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; 2 | METHODS; 2.3 | Study design; FIGURE 1; TABLE 1, PVR row; TABLE 4, PVR row
- Pass A: WITNESS_ENTAILS_UNIT - In a randomized double-blind trial, PTX 400 mg every eight hours (a clinical regimen) added to tamsulosin in men with BPH/LUTS was reported to lower post-void residual more than placebo plus tamsulosin (p<.001), affirmatively supporting the PTX-to-changed-voiding-function link the unit lists; the baseline-imbalance caveat weakens but does not remove that support.
- Pass B: PARTIALLY_COVERS - PTX-associated emptying improvement in BPH men supports a urinary-function link, but combination with baseline imbalance.
- Final: **WITNESS_ENTAILS_UNIT** (MODEL_ADJUDICATED) - The unit asks only that existing evidence 'affirmatively supports' at least one link from 'clinically attainable' exposure to 'changed voiding function'; a randomized double-blind trial of 'pentoxifylline 400 mg every eight hours' reporting a larger post-void residual fall than placebo plus tamsulosin (p<.001) meets those stated exposure and outcome conditions. The 'baseline residual differed' and 'not validated or baseline-equivalent' caveats weaken the support but do not reverse its polarity, and the unit requires support, not proof.

### A1-H3-R1 x W-FRD-Q0019-01-Q0019
- Unit (REQUIRED_SUPPORT): Existing evidence affirmatively supports some components of H1, that is, at least one link in the chain from clinically attainable PTX or metabolite exposure, through a relevant biological target and tissue effect, to changed voiding function, an identifiable patient subgroup, and a measurable trial prediction.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Renal protection occurred only with pretreatment in an acute rat ischemia model, which the witness says does not 'transfer to chronic bladder disease'; not affirmative support for an H1 link.
- Pass B: PARTIALLY_COVERS - Supports a PTX tissue/ischemia effect link, but kidney not bladder, acute prophylactic timing, transfer needed.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The effect is on renal '48-hour creatinine clearance' after subcutaneous 100 mg/kg in rats and appears 'only when given 60 minutes before ischemia', so neither the unit's 'clinically attainable' exposure nor a voiding-relevant tissue effect is shown. The witness states the results 'don't transfer to chronic bladder disease', so partial coverage would rest on a transfer the witness explicitly denies.

### A2-H1-A1 x W-FRD-Q0028-01-Q0028
- Unit (ADVERSE_TEST): Relevant models show no early functional change at informative exposures.
- Witness: Kruuse 2000, double-blind crossover in 10 healthy subjects: pentoxifylline 300 mg intravenously over 60 minutes versus saline, SPECT before and 55 and 115 minutes after infusion began. No significant over-time change in middle-cerebral-artery or global cerebral blood flow, corrected or uncorrected. pCO2-corrected changes did not differ between treatments; uncorrected changes did. Tests healthy cerebral perfusion, not ischemic bladder.
- Source: kruuse2000.pdf.md Material and methods; Procedure on the day of the study (Table 1); Results → Main study; Statistics; Figure 1 caption
- Pass A: NO_SEMANTIC_RELATION - Cerebral-perfusion null in healthy subjects; not a voiding endpoint in a relevant model.
- Pass B: PARTIALLY_COVERS - A PTX functional null soon after exposure, but on cerebral perfusion in healthy subjects, not a voiding endpoint in a relevant model; transfer needed.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H1-A1 x W-FRD-Q0044-01-Q0044
- Unit (ADVERSE_TEST): Relevant models show no early functional change at informative exposures.
- Witness: Fukabori-1996-uninhibited-bladder.pdf.md (English abstract, 'A CASE OF UNINHIBITED BLADDER...') reports one 60-year-old woman with pollakisuria, urge incontinence and urodynamic uninhibited contractions; after a failed anticholinergic, pentoxifylline (dose/route unstated) resolved incontinence and reduced pollakisuria by two weeks, with contractions absent and increased capacity by four weeks. Storage symptoms only; single case, not comparative efficacy.
- Source: Fukabori-1996-uninhibited-bladder.pdf.md English abstract under “A CASE OF UNINHIBITED BLADDER SUCCESSFULLY TREATED WITH PENTOXIFYLLINE”, paragraph beginning “A 60-year-old woman with pollakisuria and urge incontinence”
- Pass A: PARTIALLY_COVERS - Single case shows early bladder functional change (storage symptoms resolved) after PTX, i.e. a change rather than 'no change', bearing adversely, but storage not emptying, a single non-cohort case.
- Pass B: NO_SEMANTIC_RELATION - Shows early functional change (improvement) and in a storage not voiding-emptying domain; does not provide a voiding functional null.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H1-C1 x W-FRD-Q0020-01-Q0020
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding is present and modifiable in this cohort.
- Witness: Yu and Jeong's clinical literature review (2020ICU_icu-58-S68.pdf.md, PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY) reports most published detrusor-underactivity prevalence data came from community-dwelling cohorts with significant LUTS judged by arbitrary urodynamic criteria (25%–48% elderly men, 12%–24% women), with limited general-population applicability. Community-based research is described as rare, not absent; one study used free Qmax and post-void residual, not pressure-flow parameters.
- Source: 2020ICU_icu-58-S68.pdf.md Author byline; opening abstract; PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY, concluding two paragraphs and paragraph beginning “Unlike other researchers, Groutz et al.”
- Pass A: PARTIALLY_COVERS - Documents detrusor underactivity (a functional contractility component) in men with LUTS, consistent with a functional component present, though prevalence only and modifiability not shown.
- Pass B: NO_SEMANTIC_RELATION - Epidemiology; not evidence of a modifiable component.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The review reports detrusor underactivity, a urodynamically defined contractility (functional) component of impaired voiding, in '25%–48% elderly men' with significant LUTS, supplying the 'present' half of the unit in a population that needs transfer to this cohort. It says nothing about the 'modifiable' half, and the 'arbitrary urodynamic criteria' limit the estimate, so coverage is partial.

### A2-H1-E1 x W-FRD-Q0019-01-Q0019
- Unit (CORROBORATING_EXPECTATION): Functional endpoints such as contractility or flow improve early after exposure.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: PARTIALLY_COVERS - Creatinine clearance (a functional endpoint) improved soon after PTX, matching 'functional improvement after PTX', but in a rat renal-ischaemia model with pre-injury dosing, not bladder flow/contractility, so partial.
- Pass B: NO_SEMANTIC_RELATION - Renal function, not voiding contractility/flow, and benefit only pre-ischemia; does not corroborate early voiding improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Creatinine clearance is a renal endpoint, not voiding 'contractility or flow', and benefit came 'only when given 60 minutes before ischemia' (injury prevention), with none when given '1 minute into ischemia or 60 minutes post-release', so it does not show improvement early after exposure in existing dysfunction. The witness also states the results 'don't transfer to chronic bladder disease'.

### A2-H1-E1 x W-FRD-SHIRAZI2015-02-Q0002
- Unit (CORROBORATING_EXPECTATION): Functional endpoints such as contractility or flow improve early after exposure.
- Witness: Shirazi 2015: in male Sprague-Dawley rats with partial bladder outlet obstruction, pentoxifylline 100 mg/kg/day by oral gavage for four weeks, begun after obstruction induction, produced no significant improvement in maximum carbachol-induced detrusor-strip contractile tension versus water-treated obstructed controls (20 animals per group; all completed). Treatment addressed established obstruction, not prevention; this is a functional contractility null.
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Abstract → Results; Results and Fig. 2
- Pass A: PARTIALLY_COVERS - Directly on the contractility endpoint after PTX in a relevant bladder-obstruction model, but shows no improvement (carbachol-max) at 4 weeks; a non-cohort null that bears on the expectation adversely rather than corroborating it.
- Pass B: NO_SEMANTIC_RELATION - A functional null does not corroborate early improvement; different model and no improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports 'no significant improvement' in carbachol-induced detrusor tension measured only at 'four weeks', so it supplies no part of an early-improvement claim and has no early time point. As a null in rats it is not a contradiction under the stated rules, and PARTIALLY_COVERS would misstate adverse evidence as partial support.

### A2-H1-R1 x W-FRD-SHIRAZI2015-01-Q0002
- Unit (REQUIRED_SUPPORT): PTX's materially supported mechanism acts on current physiological function, such as perfusion, microcirculation, smooth-muscle behavior, or neural signaling (examples, not an exhaustive list).
- Witness: In male Sprague-Dawley rats with surgically induced partial bladder outlet obstruction, Shirazi et al. gave pentoxifylline 100 mg/kg/day by oral gavage for four weeks after obstruction induction, associated with higher electrically evoked isolated-detrusor-strip tension than water controls (approximately 4.0 ± 1.0 versus 1.8 ± 0.4 g per 100 mg tissue; reported P=0.023). These figure-derived values are approximate (shirazi2015.pdf.md, Results).
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Results; Fig. 3
- Pass A: PARTIALLY_COVERS - Four weeks of oral PTX in obstructed rats was 'associated with higher electrically evoked isolated-detrusor-strip tension', a change in smooth-muscle behavior in voiding-relevant tissue. It is a rat model with approximate values, and a four-week course cannot separate action on current function from limitation of structural change.
- Pass B: WITNESS_ENTAILS_UNIT - PTX changed detrusor (smooth-muscle) contractile function in bladder tissue, which satisfies the unit's requirement that PTX act on a current physiological function in tissue relevant to voiding.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H2-A1 x W-FRD-SHIRAZI2015-02-Q0002
- Unit (ADVERSE_TEST): Structural effects appear only when treatment precedes injury (prevention, not reversal).
- Witness: Shirazi 2015: in male Sprague-Dawley rats with partial bladder outlet obstruction, pentoxifylline 100 mg/kg/day by oral gavage for four weeks, begun after obstruction induction, produced no significant improvement in maximum carbachol-induced detrusor-strip contractile tension versus water-treated obstructed controls (20 animals per group; all completed). Treatment addressed established obstruction, not prevention; this is a functional contractility null.
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Abstract → Results; Results and Fig. 2
- Pass A: PARTIALLY_COVERS - PTX begun after established obstruction gave no contractility improvement in a relevant bladder model, supporting the 'does not reverse established change' half of the unit, but the endpoint is functional contractility (not structural) and it is a rat model, so partial.
- Pass B: NO_SEMANTIC_RELATION - Post-injury administration with a functional null; does not establish a structural prevention-only vs reversal contrast.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H2-C3 x W-FRD-Q0009-02-Q0009
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention models does not by itself support A2-H2.
- Witness: Delanian et al. 2003, single-center randomized double-blind placebo-controlled 2×2 factorial trial in women with superficial radiation-induced fibrosis >6 months after breast radiotherapy (24 eligible, 22 with 6-month data). Combination pentoxifylline 800 mg/day plus vitamin E 1000 U/day gave −60.2% versus double-placebo −42.6% surface-area change (P=.038, Wilcoxon). Two-way ANOVA found no significant main effects, only a PTX×vitamin-E interaction trend (P=.09).
- Source: delanian2003.pdf.md PATIENTS AND METHODS; Randomization; Outcome Measures; Statistical Analysis; RESULTS; Primary Analyses; Table 3, surface Index 6 months, % row and boxhead note
- Pass A: NO_SEMANTIC_RELATION - This constraint concerns the composition of coverage sets (whether any rests solely on prevention-model findings); a single source finding does not establish or refute that bookkeeping property.
- Pass B: PARTIALLY_COVERS - Treatment of established structure, not prevention; relevant non-prevention structural fragment, wrong tissue/population.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H2-C3 x W-FRD-Q0009-03-Q0009
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention models does not by itself support A2-H2.
- Witness: Delanian et al.'s follow-up of women with superficial breast radiation-induced fibrosis on pentoxifylline 800 mg/day plus vitamin E 1,000 U/day found that, after stopping, fibrosis surface area rebounded more after short (6-12-month) treatment than long (24-48-month) treatment: 40%/year (95% CI 24-56) versus 8.5%/year (95% CI 1-16); P=.0012. Duration was not randomized; follow-up lasted two years (delanian2005.pdf.md).
- Source: delanian2005.pdf.md Modalities of Combined PTX-vitE Treatment; Statistical Analysis; Primary Analyses, paragraph beginning “After stopping PTX-vitE: Rebound effect”; DISCUSSION, paragraph beginning “Long-term follow-up of our patients”
- Pass A: NO_SEMANTIC_RELATION - This constraint concerns the composition of coverage sets (whether any rests solely on prevention-model findings); a single source finding does not establish or refute that bookkeeping property.
- Pass B: PARTIALLY_COVERS - Non-prevention structural evidence (treatment of established fibrosis) — the kind the constraint says is needed beyond prevention; wrong tissue, partial.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H2-C3 x W-FRD-Q0019-01-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention models does not by itself support A2-H2.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - This constraint concerns the composition of coverage sets (whether any rests solely on prevention-model findings); a single source finding does not establish or refute that bookkeeping property.
- Pass B: PARTIALLY_COVERS - Prevention-timing PTX finding — exactly the prevention-only evidence the constraint flags as insufficient on its own; renal/acute, so partial.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H2-E2 x W-FRD-Q0009-02-Q0009
- Unit (CORROBORATING_EXPECTATION): Functional improvement follows structural change in time.
- Witness: Delanian et al. 2003, single-center randomized double-blind placebo-controlled 2×2 factorial trial in women with superficial radiation-induced fibrosis >6 months after breast radiotherapy (24 eligible, 22 with 6-month data). Combination pentoxifylline 800 mg/day plus vitamin E 1000 U/day gave −60.2% versus double-placebo −42.6% surface-area change (P=.038, Wilcoxon). Two-way ANOVA found no significant main effects, only a PTX×vitamin-E interaction trend (P=.09).
- Source: delanian2003.pdf.md PATIENTS AND METHODS; Randomization; Outcome Measures; Statistical Analysis; RESULTS; Primary Analyses; Table 3, surface Index 6 months, % row and boxhead note
- Pass A: NO_SEMANTIC_RELATION - Reports a single 6-month fibrosis surface-area change with PTX plus vitamin E in irradiated breast tissue; there is no voiding-function measure and no serial ordering of structural versus functional change, which is the unit's core requirement.
- Pass B: PARTIALLY_COVERS - Supplies the structural-change half (skin fibrosis reduced) but no serial precedence over voiding function; one link only, wrong tissue.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The unit asserts a temporal order ('Functional improvement follows structural change in time'); the witness reports one structural endpoint (fibrosis surface area) for PTX plus vitamin E in irradiated breast tissue, with no functional measure and no serial timing. With 'no significant main effects' for PTX and a different tissue, even the structural half would need unstated attribution and transfer assumptions.

### A2-H2-R3 x W-FRD-Q0044-01-Q0044
- Unit (REQUIRED_SUPPORT): Meaningful improvement appears only after weeks to months of treatment.
- Witness: Fukabori-1996-uninhibited-bladder.pdf.md (English abstract, 'A CASE OF UNINHIBITED BLADDER...') reports one 60-year-old woman with pollakisuria, urge incontinence and urodynamic uninhibited contractions; after a failed anticholinergic, pentoxifylline (dose/route unstated) resolved incontinence and reduced pollakisuria by two weeks, with contractions absent and increased capacity by four weeks. Storage symptoms only; single case, not comparative efficacy.
- Source: Fukabori-1996-uninhibited-bladder.pdf.md English abstract under “A CASE OF UNINHIBITED BLADDER SUCCESSFULLY TREATED WITH PENTOXIFYLLINE”, paragraph beginning “A 60-year-old woman with pollakisuria and urge incontinence”
- Pass A: NO_SEMANTIC_RELATION - PTX 'resolved incontinence and reduced pollakisuria by two weeks', with urodynamic change 'by four weeks', in one woman with storage symptoms; this does not show improvement appearing only after weeks to months (the two-week response is early), and the different sex and storage scope rule out a contradiction.
- Pass B: PARTIALLY_COVERS - Weeks-range PTX urinary improvement but on the fast side and storage/female; partial.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The phrase 'by two weeks' is an upper bound on onset, so the case cannot show that improvement appears 'only after weeks to months'; it is equally compatible with earlier onset. It also concerns one woman with 'Storage symptoms only', so it neither supports the delayed-onset restriction nor, given the scope difference, contradicts it.

### A2-H2-R3 x W-FRD-SHIRAZI2015-01-Q0002
- Unit (REQUIRED_SUPPORT): Meaningful improvement appears only after weeks to months of treatment.
- Witness: In male Sprague-Dawley rats with surgically induced partial bladder outlet obstruction, Shirazi et al. gave pentoxifylline 100 mg/kg/day by oral gavage for four weeks after obstruction induction, associated with higher electrically evoked isolated-detrusor-strip tension than water controls (approximately 4.0 ± 1.0 versus 1.8 ± 0.4 g per 100 mg tissue; reported P=0.023). These figure-derived values are approximate (shirazi2015.pdf.md, Results).
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Results; Fig. 3
- Pass A: NO_SEMANTIC_RELATION - Higher detrusor-strip tension after 'four weeks' of PTX in obstructed rats is a single post-treatment time point; with no earlier measurement it cannot show improvement appearing only after weeks, and the outcome is ex-vivo rat strip tension, not voiding.
- Pass B: PARTIALLY_COVERS - Improvement at 4wk in rat, but single endpoint cannot show 'only after weeks' and species/measure mismatch.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Higher strip tension measured only after 'four weeks' of PTX gives no earlier time point, so it cannot show improvement emerging 'only after weeks to months', the unit's core timing restriction. The outcome is ex-vivo rat detrusor-strip tension, not meaningful voiding improvement.

### A2-H3-R1 x W-FRD-Q0027-01-Q0027
- Unit (REQUIRED_SUPPORT): For at least one identified timing link (onset, duration-response, persistence after withdrawal, or which effect carries the benefit), the timing evidence is unmeasured, conflicting, poorly transferable, or compatible with both rapid functional benefit and slow structural recovery.
- Witness: Neuner et al. (immunology00076-0102.pdf.md) studied four healthy volunteers overall; the two-day-regimen subgroup size is unspecified. Oral PTX 5×400 mg/day for two days significantly suppressed TNF-α, IL-1β, IL-6 and IL-8 release from day-7 PBMC cultured 24 hours, with or without LPS 1 µg/mL. These are ex-vivo endpoints after in-vivo dosing; plasma/tissue exposure and clinical urinary efficacy were unmeasured.
- Source: immunology00076-0102.pdf.md P. Neuner et al., “Pentoxifylline in vivo down-regulates the release of IL-1 β, IL-6, IL-8 and tumour necrosis factor-α by human peripheral blood mononuclear cells.” Exact source: `immunology00076-0102.pdf.md`; MATERIALS AND METHODS → Human volunteers; Preparation of PBMC; RESULTS → In vivo effects of orally applied PTX on cytokine production by PBMC, first paragraph; Figure 1 original caption. The original results locator is correct. Journal, volume, pagination and publication date are not established by the supplied article metadata; receipt and acceptance dates are supplied but are not publication dates.
- Pass A: WITNESS_ENTAILS_UNIT - Reports a PTX effect (cytokine suppression after two days) whose timing comes from ex-vivo PBMC of healthy volunteers, with 'clinical urinary efficacy ... unmeasured': timing from a non-transferable model and unmeasured for which effect carries benefit, meeting the unit's stated condition.
- Pass B: PARTIALLY_COVERS - Ex-vivo endpoint after brief dosing; onset/persistence of any voiding benefit unmeasured.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness supplies one instance of the unit's condition: two-day ex-vivo PBMC cytokine timing in healthy volunteers (poorly transferable) with benefit unmeasured ('clinical urinary efficacy were unmeasured'), bearing on 'which effect carries the benefit'. The unit characterizes 'the timing evidence' for a link as a whole, so entailment would need the unstated assumption that this source is all of that evidence.

### A2-H3-R1 x W-FRD-Q0029-01-Q0029
- Unit (REQUIRED_SUPPORT): For at least one identified timing link (onset, duration-response, persistence after withdrawal, or which effect carries the benefit), the timing evidence is unmeasured, conflicting, poorly transferable, or compatible with both rapid functional benefit and slow structural recovery.
- Witness: Dezube et al. 1993, pilot study of seven adult cancer patients treated on eight occasions for 1–3 weeks with oral controlled-release pentoxifylline 400 mg every eight hours. On all three occasions when baseline PBMC TNF/β-actin RNA ratios exceeded the healthy-volunteer normal range, ratios fell within one week; on five occasions within normal range, no reduction. Target-engagement, not clinical benefit.
- Source: dezube1993.pdf.md Materials and methods → Patient characteristics, Treatment plan, TNF RNA assay; Results → TNF/actin ratios in vivo → Normal volunteers; Results → Suppression of TNF/actin ratios by pentoxifylline in vivo; Fig. 3 caption; Discussion, paragraph beginning “In this pilot study, TNF was measured”
- Pass A: WITNESS_ENTAILS_UNIT - TNF RNA fell 'within one week' in cancer patients but is 'Target-engagement, not clinical benefit', with no withdrawal data: onset timing comes from a non-transferable marker model and which effect carries benefit is unmeasured.
- Pass B: PARTIALLY_COVERS - Timing for target engagement, not benefit; leaves 'which effect carries the benefit' and urinary onset unresolved.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - TNF RNA fell 'within one week' in cancer patients but this is 'Target-engagement, not clinical benefit', giving marker-onset timing from a different population with benefit timing unmeasured, an instance of the unit's condition. One source does not establish the state of the whole timing evidence for that link, so coverage is partial.

### A2-H3-R1 x W-FRD-Q0044-01-Q0044
- Unit (REQUIRED_SUPPORT): For at least one identified timing link (onset, duration-response, persistence after withdrawal, or which effect carries the benefit), the timing evidence is unmeasured, conflicting, poorly transferable, or compatible with both rapid functional benefit and slow structural recovery.
- Witness: Fukabori-1996-uninhibited-bladder.pdf.md (English abstract, 'A CASE OF UNINHIBITED BLADDER...') reports one 60-year-old woman with pollakisuria, urge incontinence and urodynamic uninhibited contractions; after a failed anticholinergic, pentoxifylline (dose/route unstated) resolved incontinence and reduced pollakisuria by two weeks, with contractions absent and increased capacity by four weeks. Storage symptoms only; single case, not comparative efficacy.
- Source: Fukabori-1996-uninhibited-bladder.pdf.md English abstract under “A CASE OF UNINHIBITED BLADDER SUCCESSFULLY TREATED WITH PENTOXIFYLLINE”, paragraph beginning “A 60-year-old woman with pollakisuria and urge incontinence”
- Pass A: WITNESS_ENTAILS_UNIT - Improvement 'by two weeks' and urodynamic change 'by four weeks' in one woman with storage symptoms gives onset timing from a population that does not transfer to men with voiding difficulty, with no withdrawal data and a course compatible with rapid or slower benefit.
- Pass B: PARTIALLY_COVERS - Reports an onset (2-4wk) but storage symptoms, single case — poorly transferable and compatible with both rapid/slow mechanisms.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Onset 'by two weeks' and urodynamic change 'by four weeks' in one woman with 'Storage symptoms only' is onset evidence of doubtful transfer to the cohort, with no withdrawal data. The unit concerns the state of 'the timing evidence' for a link, which a single case cannot fix without assuming no better-transferable evidence exists.

### A2-H3-R1 x W-FRD-SHIRAZI2015-01-Q0002
- Unit (REQUIRED_SUPPORT): For at least one identified timing link (onset, duration-response, persistence after withdrawal, or which effect carries the benefit), the timing evidence is unmeasured, conflicting, poorly transferable, or compatible with both rapid functional benefit and slow structural recovery.
- Witness: In male Sprague-Dawley rats with surgically induced partial bladder outlet obstruction, Shirazi et al. gave pentoxifylline 100 mg/kg/day by oral gavage for four weeks after obstruction induction, associated with higher electrically evoked isolated-detrusor-strip tension than water controls (approximately 4.0 ± 1.0 versus 1.8 ± 0.4 g per 100 mg tissue; reported P=0.023). These figure-derived values are approximate (shirazi2015.pdf.md, Results).
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Results; Fig. 3
- Pass A: WITNESS_ENTAILS_UNIT - A single measurement after 'four weeks' of PTX in obstructed rats reports a PTX effect without onset or withdrawal timing, from a model that does not transfer to the cohort, satisfying the unit's unmeasured/poorly-transferable condition.
- Pass B: PARTIALLY_COVERS - Positive rat effect without time course; poorly transferable timing.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - A single post-treatment measurement after 'four weeks' in obstructed rats gives no onset or post-withdrawal timing and comes from an ex-vivo rat model, an instance of unmeasured and poorly transferable timing. Entailing the unit's claim about 'the timing evidence' for a link would need the unstated assumption that this is all the timing evidence for that link.

### A2-H3-R1 x W-FRD-SHIRAZI2015-02-Q0002
- Unit (REQUIRED_SUPPORT): For at least one identified timing link (onset, duration-response, persistence after withdrawal, or which effect carries the benefit), the timing evidence is unmeasured, conflicting, poorly transferable, or compatible with both rapid functional benefit and slow structural recovery.
- Witness: Shirazi 2015: in male Sprague-Dawley rats with partial bladder outlet obstruction, pentoxifylline 100 mg/kg/day by oral gavage for four weeks, begun after obstruction induction, produced no significant improvement in maximum carbachol-induced detrusor-strip contractile tension versus water-treated obstructed controls (20 animals per group; all completed). Treatment addressed established obstruction, not prevention; this is a functional contractility null.
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Abstract → Results; Results and Fig. 2
- Pass A: WITNESS_ENTAILS_UNIT - A PTX outcome at a single four-week time point in obstructed rats, with onset and post-withdrawal persistence unmeasured and a non-transferable model, meets the unit's condition.
- Pass B: PARTIALLY_COVERS - PTX timing from a non-transferable rat model with no onset/withdrawal course; poorly transferable timing link.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The carbachol null in obstructed rats is measured at a single 'four weeks' time point with onset and post-withdrawal persistence unmeasured, in a model needing transfer, so it supplies an instance of the unit's 'unmeasured' or 'poorly transferable' condition. It does not by itself establish the state of the whole timing evidence for any link.

### A2-H3-R2 x W-FRD-Q0015-01-Q0015
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: In Parker et al.'s randomized, investigator-blinded porcine haemorrhage-plus-E.-coli-peritonitis experiment (female Large White pigs; n=5 per group), pentoxifylline plus colloid (20 mg/kg bolus, then 20 mg/kg over 60 minutes) gave lower median 2-hour MAP than colloid-plus-saline placebo: 62(10) versus 92(10) mmHg (P<0.01); by 6 hours groups did not differ. This is acute resuscitation, not chronic oral treatment (parker2000.pdf.md).
- Source: parker2000.pdf.md Abstract; §2.1 Animal preparation; §2.3 Experimental procedure; §3.1 Cardiovascular parameters, Table 1 caption, MAP rows and footnotes
- Pass A: NO_SEMANTIC_RELATION - A 2-hour versus 6-hour MAP difference in acute IV porcine resuscitation, 'not chronic oral treatment'; it does not bear on whether voiding-benefit onset or persistence can be specified.
- Pass B: PARTIALLY_COVERS - Non-transferable acute PTX timing datum.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H3-R2 x W-FRD-Q0016-01-Q0016
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: In Ridings et al.'s nonrandomized controlled porcine sepsis experiment (ridings1994.pdf.md, COMMENT), intravenous pentoxifylline (20 mg/kg bolus, 6 mg/kg/h) begun two hours after Pseudomonas infusion (established, uncorrected shock) was followed by fatal hypotension within one hour in 2/4 animals; two survivors resembled 1-hour-treated protection (data not shown). Authors attributed deaths to pentoxifylline but said n=4 precluded statistics; untransferable to bladder dysfunction.
- Source: ridings1994.pdf.md Abstract: Design, Interventions, Results; MATERIALS AND METHODS → THE PORCINE MODEL and EXPERIMENTAL DESIGN; RESULTS opening paragraph; COMMENT, “In our studies, the administration of pentoxifylline 2 hours” and “If pentoxifylline is administered to animals in uncorrected septic shock”
- Pass A: NO_SEMANTIC_RELATION - Porcine sepsis hypotension; unrelated to benefit timing.
- Pass B: PARTIALLY_COVERS - Non-transferable acute PTX timing datum.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H3-R2 x W-FRD-Q0029-01-Q0029
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: Dezube et al. 1993, pilot study of seven adult cancer patients treated on eight occasions for 1–3 weeks with oral controlled-release pentoxifylline 400 mg every eight hours. On all three occasions when baseline PBMC TNF/β-actin RNA ratios exceeded the healthy-volunteer normal range, ratios fell within one week; on five occasions within normal range, no reduction. Target-engagement, not clinical benefit.
- Source: dezube1993.pdf.md Materials and methods → Patient characteristics, Treatment plan, TNF RNA assay; Results → TNF/actin ratios in vivo → Normal volunteers; Results → Suppression of TNF/actin ratios by pentoxifylline in vivo; Fig. 3 caption; Discussion, paragraph beginning “In this pilot study, TNF was measured”
- Pass A: NO_SEMANTIC_RELATION - Gives a one-week onset for PBMC TNF reduction, explicitly 'target-engagement, not clinical benefit'; it neither resolves nor shows unresolvable the onset and persistence of voiding benefit.
- Pass B: PARTIALLY_COVERS - PTX rapid marker (not voiding) timing; non-transferable evidence feeding the unresolved link.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

### A2-H3-R2 x W-FRD-SHIRAZI2015-02-Q0002
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: Shirazi 2015: in male Sprague-Dawley rats with partial bladder outlet obstruction, pentoxifylline 100 mg/kg/day by oral gavage for four weeks, begun after obstruction induction, produced no significant improvement in maximum carbachol-induced detrusor-strip contractile tension versus water-treated obstructed controls (20 animals per group; all completed). Treatment addressed established obstruction, not prevention; this is a functional contractility null.
- Source: shirazi2015.pdf.md Animals and methods → Study design; Surgical technique; Evaluation of detrusor muscle contractility; Statistical analysis; Abstract → Results; Results and Fig. 2
- Pass A: NO_SEMANTIC_RELATION - A single 4-week functional null in rats gives no onset or persistence data and does not show that the timing link is unresolved.
- Pass B: PARTIALLY_COVERS - Non-transferable single-timepoint rat datum contributing to unresolved voiding-timing.
- Final: **ABSTAIN** (DISPUTED) - pass A and pass B disagree; no adjudication (the adjudication request was not answered)

## Judged by one pass only (needs confirmation) (6)

### A2-H2-C2 x W-FRD-Q0019-01-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): PTX can reverse or limit that structural change rather than merely prevent it.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: CONTRADICTS - Affirmative prevention-only pattern (benefit only pre-ischemia, not during/after) — the finding the unit says contradicts 'PTX can reverse established change.'
- Final: **CONTRADICTS** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] Affirmative prevention-only pattern (benefit only pre-ischemia, not during/after) — the finding the unit says contradicts 'PTX can reverse established change.'

### A2-H3-E2 x W-FRD-Q0001-02-r3-Q0001
- Unit (CORROBORATING_EXPECTATION): Available findings lack onset or withdrawal timing.
- Witness: Shirazi et al. (2024, Lower Urinary Tract Symptoms) reported mean Qmax changes of 4.48 versus 2.67 mL/s; their arithmetic difference, 1.81 mL/s, is an analyst-derived unadjusted contrast favoring pentoxifylline-plus-tamsulosin over placebo-plus-tamsulosin, not a separately reported adjusted estimate. This BPH add-on trial does not establish pentoxifylline monotherapy or psychogenic-voiding efficacy.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Shirazi M et al. Lower Urinary Tract Symptoms. 2024;16(1):e12509. doi:10.1111/luts.12509. Exact source filename: `Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md`. Locations: TABLE 4; 2 | METHODS; 2.3 | Study design. Original locator: TABLE 4. Page numbers are unavailable in the supplied text.
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - In-scope BPH-men PTX outcome reported with no onset or post-withdrawal timing — an instance of findings lacking onset/withdrawal timing.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] In-scope BPH-men PTX outcome reported with no onset or post-withdrawal timing — an instance of findings lacking onset/withdrawal timing.

### A2-H3-E3 x W-FRD-Q0019-01-Q0019
- Unit (CORROBORATING_EXPECTATION): Available findings rest on models whose timing does not transfer to this cohort.
- Witness: Wystrychowski et al. (wystrychowski2014.pdf.md, Table 1; RESULTS) randomized 58 male Sprague-Dawley rats; after right nephrectomy, solitary left pedicle was clamped 45 minutes. Subcutaneous pentoxifylline 100 mg/kg versus saline improved 48-hour creatinine clearance only when given 60 minutes before ischemia (10/arm; P<.001), not 1 minute into ischemia or 60 minutes post-release. These within-timing acute-model results don't transfer to chronic bladder disease.
- Source: wystrychowski2014.pdf.md ABSTRACT (Methods); METHODS; RESULTS; Table 1, “Renal Function Parameters at 48 Hours After Ischemia/Reperfusion of the Solitary Left Kidney”; DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - Pretreatment-only PTX efficacy in an acute rat renal-ischemia model; witness explicitly states within-timing acute-model results do not transfer to chronic bladder disease.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] Pretreatment-only PTX efficacy in an acute rat renal-ischemia model; witness explicitly states within-timing acute-model results do not transfer to chronic bladder disease.

### A2-H3-R2 x W-FRD-Q0001-01-Q0001
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: Shirazi et al. (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md): single-center randomized double-blind trial, 30 men per arm (all analyzed) with BPH/LUTS, giving pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day or placebo plus tamsulosin, 12 weeks. Post-void residual fell more with combination (−32.93±16.33 versus −13.17±9.23 mL; p<.001), but baseline residual differed (77.27 versus 50.37 mL; p=.18). Reported values, not validated or baseline-equivalent.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; 2 | METHODS; 2.3 | Study design; FIGURE 1; TABLE 1, PVR row; TABLE 4, PVR row
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - In-scope PTX emptying outcome at endpoint only; onset/persistence not specifiable from it.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] In-scope PTX emptying outcome at endpoint only; onset/persistence not specifiable from it.

### A2-H3-R2 x W-FRD-Q0001-02-r3-Q0001
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: Shirazi et al. (2024, Lower Urinary Tract Symptoms) reported mean Qmax changes of 4.48 versus 2.67 mL/s; their arithmetic difference, 1.81 mL/s, is an analyst-derived unadjusted contrast favoring pentoxifylline-plus-tamsulosin over placebo-plus-tamsulosin, not a separately reported adjusted estimate. This BPH add-on trial does not establish pentoxifylline monotherapy or psychogenic-voiding efficacy.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Shirazi M et al. Lower Urinary Tract Symptoms. 2024;16(1):e12509. doi:10.1111/luts.12509. Exact source filename: `Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md`. Locations: TABLE 4; 2 | METHODS; 2.3 | Study design. Original locator: TABLE 4. Page numbers are unavailable in the supplied text.
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - In-scope PTX voiding outcome with no onset or withdrawal timing; shows persistence/onset not derivable from this premise.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] In-scope PTX voiding outcome with no onset or withdrawal timing; shows persistence/onset not derivable from this premise.

### A2-H3-R2 x W-FRD-Q0011-01-Q0011
- Unit (REQUIRED_SUPPORT): As a result, the expected onset and persistence of benefit cannot be specified from supported premises.
- Witness: In Shirazi et al.'s single-center, randomized, double-blind 12-week BPH trial (60 men, 30/group), pentoxifylline 400 mg every eight hours plus tamsulosin 0.4 mg/day versus placebo plus tamsulosin showed no significant between-group voided-volume change (0.80 versus +1.34 mL; p=.22) and no statistically significant within-group change (p=.90, .89). Baseline-to-endpoint voided-volume only—not residual or flow; visit schedule, onset, post-withdrawal persistence unestablished (Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md, §3.3).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md Abstract, Materials and Methods; §2.3 Study design; §3 Results; §3.3 Voided volume; Tables 2–4, voided-volume rows
- Pass A: MISSING - no judgment returned
- Pass B: WITNESS_ENTAILS_UNIT - Witness states visit schedule, onset and post-withdrawal persistence unestablished — directly shows onset/persistence not specifiable from this premise.
- Final: **WITNESS_ENTAILS_UNIT** (ONE_PASS_ONLY) - [one pass only; the other pass's request was not answered] Witness states visit schedule, onset and post-withdrawal persistence unestablished — directly shows onset/persistence not specifiable from this premise.
