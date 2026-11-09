# Matching review packet

Each entry is one witness judged against one coverage unit. To overrule a relation, add an entry to `human-decisions.json` in this folder (a blank template is next to this file) and run `cr run <project> --from coverage`. Relations: EQUIVALENT, WITNESS_ENTAILS_UNIT (these two give complete coverage), UNIT_ENTAILS_WITNESS, PARTIALLY_COVERS, CONTRADICTS, NO_SEMANTIC_RELATION, ABSTAIN.

## Complete relations (these build coverage sets) (0)

## Contradictions (these drive crux tests) (0)

## Disagreements between pass A and pass B (727)

### A1-H1-A1 x W-FRD-Q0003-04-c1-Q0003
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness proposes mechanistic explanations for PTX’s beneficial effects in cardiac ischemic injury (“PDE inhibitor… NOS activator… increases NO/cGMP”) rather than reporting a negative finding that would falsify H1 (no claim of unattainable exposure, absent target, or failure of modulation to improve function).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only offers proposed mechanisms for PTX benefit (“phosphodiesterase inhibitor and nitric oxide synthase activator… increases tissue NO and intracellular cGMP”) and does not report any falsifying/against-H1 finding such as “unattainable relevant exposure,” “absent/incidental target,” or “failure… to improve relevant function.”

### A1-H1-A1 x W-FRD-Q0003-04-c3-Q0003
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX improved detrusor contractions to electric stimulation but not to carbachol; this is not a falsifier of H1 (it is not 'failure of target modulation to improve relevant function' and is not a source-attributed negative outcome on voiding-relevant function under informative conditions).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports mixed functional results in an obstructed bladder model (“improved detrusor contractions to electric stimulation… did not improve responses to carbachol”) and a pathway interpretation (“assumed… not via cholinergic nerves”), but does not assert any of the unit’s adverse-test falsifiers (no claim of exposure unattainability, absent target, or that target modulation fails to improve the relevant function under informative conditions).

### A1-H1-A1 x W-FRD-Q0013-01-c4-Q0013
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns diagnostic criteria for pseudodyssynergia and minimizing bashful voiding artifacts (“private-setting uroflowmetry… minimize false-positives”), not any negative finding about PTX exposure, target presence, or lack of functional improvement.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-A1 x W-FRD-Q0019-02-Q0019
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: PARTIALLY_COVERS - Witness gives a potentially H1-undermining exposure constraint: many in vitro PTX studies use concentrations 'much higher than obtained clinically' and 'combined level… unlikely to exceed 10 µmol/l'; this supports the 'unattainable relevant exposure' falsifier type in general, but it does not specify required exposure in relevant tissue for the voiding mechanism, so it does not by itself establish unattainability under H1’s conditions.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-A1 x W-FRD-Q0019-03-c3-Q0019
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness shows an effect at clinically plausible concentrations (5 µmol/l inhibited FMLP-stimulated burst), which is not a negative/falsifying finding of the types listed (no claim of unattainable exposure, absent target, or failure of modulation to improve relevant function).
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-A1 x W-FRD-Q0044-04-c2-Q0044
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - Witness reports absence of adverse effects (“Adverse effects were not reported… No adverse effects… observed”), which is not one of the listed falsifiers against H1 (it is not a negative finding about exposure feasibility, target presence, or functional non-improvement).
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-A1 x W-FRD-Q0090-04-c3-Q0090
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Reports a negative mechanistic result in neutrophils ("up to 50 µmol/l did not change... [Ca2+]i"), but does not connect to voiding-relevant function or claim clinically plausible dosing cannot reach needed exposure in relevant tissue.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-A1 x W-FRD-Q0098-01-Q0098
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is a rat hemorrhage/shock pretreatment experiment ("male rats... IV PTX 40 mg/kg... decreased MAP... then 'they all died' in shock"), not an informative negative test of PTX improving voiding in the unit’s scoped men or a statement that required exposure is unattainable clinically.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-A1 x W-FRD-Q0131-03-c3-Q0131
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - States only that "PTX has short half-life about 1.6 h"; it does not assert unattainable exposure, absent target, or failure of modulation to improve relevant (voiding) function.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-A1 x W-FRD-Q0131-03-c4-Q0131
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Reports "PTX toxicity was reported at 80 mg/kg" with specific adverse effects, but does not state clinically plausible dosing cannot reach required exposure or that target modulation fails to improve voiding-related function.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-A1 x W-FRD-Q0156-03-c1-Q0156
- Unit (ADVERSE_TEST): Findings that would falsify or strongly count against H1 include unattainable relevant exposure, absent/incidental target, failure of target modulation to improve relevant function under informative conditions, or stronger evidence breaking a necessary link shared by non-speculative routes.
- Witness: Roberts1993.pdf.md (Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend): purified neutrophils preincubated 15 min: 1 µmol/L pentoxifylline did not inhibit FMLP superoxide rate or total; ≥5 µmol/L inhibited both. At 10 µmol/L: Rate FMLP 85% and Total FMLP 75% vs control (p<0.05).
- Source: roberts1993.pdf.md Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The unit asks for a source-attributed negative finding that would falsify H1 (e.g., clinically plausible dosing cannot reach needed exposure in relevant tissue, or target modulation fails to improve voiding-relevant function). This witness only reports in-vitro neutrophil superoxide inhibition thresholds ("1 µmol/L ... did not inhibit"; ">=5 µmol/L inhibited"), not a falsifier tied to voiding-relevant function or clinically attainable exposure in target tissue.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C1 x W-FRD-Q0009-04-Q0009
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Chuang2015.pdf.md (EPIDEMIOLOGY) says Thomas et al. reported that, in men with untreated detrusor underactivity and minimum 10-year urodynamic follow-up, detrusor underactivity was not progressive in most nonneurogenic male patients and often did not result in chronic urinary retention.
- Source: chuang2015.pdf.md EPIDEMIOLOGY section (paragraph beginning “Thomas and colleagues9 reported…”)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns long-term progression of "detrusor underactivity" ("not progressive"; often not leading to retention) rather than whether dysfunction exists in the target cohort, PTX reaches tissue, or whether modulating processes improves urinary function.
- Pass B: PARTIALLY_COVERS - Witness reports detrusor underactivity “was not progressive in most… and often did not result in chronic urinary retention,” which is compatible with (and mildly supportive of) reversibility assumptions, but it does not address PTX exposure/tissue reach or treatment-driven improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness says detrusor underactivity in men was “not progressive in most” and “often did not result in chronic urinary retention,” which concerns natural history/progression, not the unit’s assumptions about drug effects reaching tissue or that changing processes improves urinary function.

### A1-H1-C1 x W-FRD-Q0013-03-c6-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), patients were considered to have an acontractile detrusor if they had no detrusor contraction during pressure-flow analysis and were unable to generate an uncatheterized urine flow (in private).
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness only defines "acontractile detrusor" diagnostically (no contraction during analysis and no uncatheterized flow), without claiming dysfunction exists in the cohort, PTX reaches tissue, or that modulation improves urinary function.
- Pass B: PARTIALLY_COVERS - Witness defines acontractile detrusor as “no detrusor contraction… and… unable to generate… urine flow,” which is consistent with the unit’s assumption that relevant dysfunction can exist, but it does not address PTX reaching tissue or improving function.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only provides a diagnostic definition (“no detrusor contraction… unable to generate… urine flow”) and does not assert that the dysfunction occurs in the cohort, that drug effects reach urinary tissue, or that modifying processes improves urinary function.

### A1-H1-C1 x W-FRD-Q0034-04-bortnick20-c1-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: bortnick2020.pdf.md (“Medical therapy”→“Combination therapy” MTOPS paragraph) reports MTOPS studied finasteride+doxazosin in 3000 men (mean age 62.6 years, SD 7.3) and found combination therapy improved voiding symptoms and maximum urinary flow rate more than either alone, prevented BPH progression better, and reduced the long-term risk of acute urinary retention and need for invasive therapy.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (MTOPS paragraph)
- Pass A: PARTIALLY_COVERS - Witness reports in MTOPS that combination therapy "improved voiding symptoms and maximum urinary flow rate" and reduced retention/progression, supporting the general premise that modulating relevant processes can improve urinary function, but it is not about PTX or the specified cohort and does not address PTX tissue reach.
- Pass B: NO_SEMANTIC_RELATION - Witness reports MTOPS findings for “finasteride+doxazosin” improving symptoms/flow and reducing AUR/invasive therapy, which does not bear on PTX exposure, PTX mechanisms, or the unit’s assumptions specific to PTX.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports MTOPS combination therapy “improved voiding symptoms and maximum urinary flow rate” and reduced retention/progression, supporting the unit’s general premise that changing relevant processes can improve urinary function, though it does not address PTX or tissue reach in the target cohort.

### A1-H1-C1 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: PARTIALLY_COVERS - Witness reports CombAT combination therapy reduced risk of AUR/surgery and clinical progression more than monotherapy, which aligns with the general assumption that changing processes can improve urinary outcomes, but it does not involve PTX, the cohort, or PTX tissue exposure.
- Pass B: NO_SEMANTIC_RELATION - Witness discusses “combination therapy” in CombAT and risk reduction for AUR/BPH surgery versus monotherapy, but it is not about PTX, tissue reach, or the unit’s PTX-related assumptions.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states in CombAT combination therapy produced greater risk reduction in “acute urinary retention or BPH-related surgery” and “clinical progression,” which is partial support for the assumption that interventions can improve urinary outcomes, but it does not establish PTX tissue exposure or the specified cohort.

### A1-H1-C1 x W-FRD-Q0042-03-c2-Q0042
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: NO_SEMANTIC_RELATION - Witness reports side effects (epigastric pain treated with omeprazole) and does not speak to dysfunction presence, PTX reaching relevant urinary tissue, or urinary function improvement.
- Pass B: PARTIALLY_COVERS - Witness reports only two patients had “epigastric pain” over “24 weeks of treatment,” consistent with tolerability under treatment conditions but not addressing urinary tissue reach or improvement of urinary function.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is limited to side effects/completion (“all 12 patients completed… two reported epigastric pain… complete remission”) and does not speak to urinary dysfunction presence, PTX reaching relevant urinary tissue, or urinary function improvement mechanisms.

### A1-H1-C1 x W-FRD-Q0044-04-c2-Q0044
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - Witness reports "No adverse effects" of PTX treatment; tolerability does not address urinary dysfunction existence, tissue penetration to relevant urinary tissue, or improvement of urinary function.
- Pass B: PARTIALLY_COVERS - Witness states “Adverse effects were not reported… No adverse effects of pentoxifylline treatment were observed,” supporting tolerability/plausible use, but it does not address urinary dysfunction presence, tissue exposure, or urinary function improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only claims tolerability (“Adverse effects were not reported… No adverse effects of pentoxifylline treatment were observed”) and does not address whether dysfunction exists in the cohort, whether effects reach relevant tissue, or whether changing processes improves urinary function.

### A1-H1-C1 x W-FRD-Q0063-01-c4-Q0063
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: PARTIALLY_COVERS - Shows PTX reduces FMLP-stimulated superoxide in PMNs at 100 µg/ml (a drug effect on an inflammatory/oxidative process), which is consistent with modulating a process, but says nothing about the target cohort, tissue reach under plausible treatment, or improvement in urinary function.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports a drug effect in vitro (“Pentoxifylline… reduced… superoxide… in PMNs”), supporting that PTX can modulate a biological process, but it does not establish plausible in-vivo tissue reach or urinary function improvement in the cohort.

### A1-H1-C1 x W-FRD-Q0085-01-c3-Q0085
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety): During the study, no severe adverse effects were reported, including no threatening hypotension or syncope; vital signs remained almost stable; no urinary retention occurred; and therapy did not stop for TEAEs (not explicitly phrased as zero TEAE dropouts).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: PARTIALLY_COVERS - Safety findings in a tamsulosin+PTX study (no severe adverse effects, no urinary retention) are consistent with 'plausible treatment conditions' but do not establish tissue reach, presence of the dysfunction in the cohort, or that modulating processes improves urinary function.
- Pass B: NO_SEMANTIC_RELATION - Reported absence of severe AEs (“no threatening hypotension or syncope… no urinary retention”) does not address whether the relevant dysfunction exists, whether PTX reaches relevant tissue, or whether modulation improves urinary function.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports treatment safety/feasibility (“no severe adverse effects… vital signs… stable… no urinary retention… therapy did not stop”), which is at most consistent with ‘plausible treatment conditions’ but does not show tissue reach or that changing processes improves urinary function.

### A1-H1-C1 x W-FRD-Q0089-04-c2-Q0089
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - This is a qualifying/negative speculation (“may have no potent anti-inflammatory effect… may be too weak”) that bears on the plausibility of meaningful process modulation, but it is not scoped to the urinary cohort/tissue and is hedged (“speculates,” “may”).
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness speculates PTX “may have no potent anti-inflammatory effect” and “may be too weak,” which bears on (and qualifies) the unit’s assumption that changing processes can improve function, but it is hedged and not tied to the urinary tissue/cohort conditions.

### A1-H1-C1 x W-FRD-Q0090-04-c3-Q0090
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness gives mechanistic concentration-response info (“up to 50 µmol/l did not change… 500 µmol/l reduced”), relevant to whether meaningful cellular effects occur at attainable exposures, but it does not establish urinary tissue exposure or urinary function improvement in the cohort.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness provides concentration-dependent mechanistic effects in neutrophils (“up to 50 µmol/l did not change… 500 µmol/l reduced”), partially informing whether PTX can change processes at some exposures, but does not establish urinary tissue exposure under treatment or urinary functional improvement.

### A1-H1-C1 x W-FRD-Q0092-03-c4-Q0092
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Side-effect completion data (“all 12 patients completed… only 2… epigastric pain”) does not support or contradict the unit’s assumptions about urinary dysfunction, tissue reach, or urinary function improvement via modulation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness repeats side-effect/completion details (“all 12 patients completed… only 2… epigastric pain”), which do not address the unit’s assumptions about urinary dysfunction, tissue reach, or improvement in urinary function via process change.

### A1-H1-C1 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - This indicates PTX can be administered chronically at a defined oral dose (“pentoxifylline 800 mg/day… 24-week trial”), consistent with plausible treatment exposure generally, but it is a different disease population and does not address urinary tissue or urinary function improvement.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states an open-label study dosing/exposure (“pentoxifylline 800 mg/day… 24-week trial”), which supports plausibility of treatment exposure in general, but in a different population and without evidence of urinary-tissue reach or urinary function improvement.

### A1-H1-C1 x W-FRD-Q0098-01-Q0098
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness shows PTX has systemic physiological effects in vivo (“decreased MAP… increased HR…”) but in rats at IV 40 mg/kg in a hemorrhage/shock context (“then ‘they all died’”), which does not match plausible human urinary-treatment conditions or support urinary-function improvement.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The unit assumes drug effects reach relevant tissue under plausible treatment and that changing processes can improve urinary function. The witness only shows systemic in-vivo physiological/hematologic effects of IV pentoxifylline in male rats in a hemorrhage/shock pilot ("decreased MAP… increased HR…"; "then 'they all died'"), which supports only that PTX has biological effects, not the urinary-function/tissue/plausible-treatment assumptions.

### A1-H1-C1 x W-FRD-Q0104-03-c6-Q0104
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about infliximab and hs-CRP (“significant treatment effect… no time effect… no interaction”) and does not address PTX, urinary tissue exposure, or urinary function improvement assumptions.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness is about infliximab vs placebo effects on hs-CRP ("significant treatment effect… no time effect… no treatment×time interaction") and does not mention the cohort dysfunction, drug reaching urinary-relevant tissue, or process changes improving urinary function as required by the unit.

### A1-H1-C1 x W-FRD-Q0131-03-c3-Q0131
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Pharmacokinetic property (“short half-life about 1.6 h”) bears on whether effects/exposure are plausible, but it does not establish reaching urinary-relevant tissue nor link modulation to improved urinary function or confirm dysfunction in the cohort.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The unit includes assumptions about plausible treatment conditions and drug effects reaching tissue. The witness provides a pharmacokinetic fact about PTX ("short half-life about 1.6 h"), which is relevant to plausibility/exposure but does not establish urinary-tissue delivery, cohort dysfunction, or that modulating processes improves urinary function.

### A1-H1-C1 x W-FRD-Q0131-03-c4-Q0131
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - A toxicity report at a high dose (“toxicity… at 80 mg/kg, causing hypotension… convulsion”) does not address the unit’s assumptions about relevant dysfunction in the cohort, urinary-tissue exposure under plausible treatment, or improvement of urinary function by modulating processes.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports toxicity at a high dose ("toxicity… at 80 mg/kg, causing hypotension, flushing, and convulsion") and does not address the unit’s assumptions about relevant dysfunction in the cohort, urinary-tissue exposure under plausible treatment, or improving urinary function by changing processes.

### A1-H1-C1 x W-FRD-Q0131-04-c3-Q0131
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: In bortnick2019.pdf.md (Review of Medications > Alpha Blockers), the review reports FORTA labeled alfuzosin, doxazosin, and terazosin “avoid” because of increased risk for orthostatic hypotension, vasodilatory effects, cardiac arrhythmias, and syncope.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness concerns risks of alfuzosin/doxazosin/terazosin (“avoid… orthostatic hypotension… syncope”) and does not address PTX reaching tissue, the dysfunction, or process modification improving urinary function.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness concerns FORTA labeling of alpha blockers ("alfuzosin, doxazosin, and terazosin 'avoid'" due to hypotension/syncope risks) and is not about the unit’s PTX/urinary-tissue exposure or urinary-function improvement assumptions.

### A1-H1-C1 x W-FRD-Q0144-01-c3-Q0144
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: In Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety), mild adverse events occurred in 11 intervention vs 13 control patients; most were mild dyspepsia requiring no treatment. No severe adverse effects (no threatening hypotension or syncope) and no urinary retention episodes; vital signs remained almost stable.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Safety/vitals (“No severe adverse effects… vital signs remained almost stable”) does not speak to whether the relevant dysfunction exists, whether PTX reaches relevant tissue, or whether modulating any process can improve urinary function.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports safety/vitals in a tamsulosin+PTX study ("No severe adverse effects… vital signs remained almost stable"; "no urinary retention") but does not support the unit’s assumptions that relevant dysfunction exists, that PTX reaches the relevant urinary tissue, or that changing processes improves urinary function.

### A1-H1-C1 x W-FRD-Q0156-03-c1-Q0156
- Unit (CONTEXTUAL_CONSTRAINT): Assume the relevant dysfunction occurs in this cohort; drug effects reach the relevant tissue under plausible treatment conditions; and changing those processes can improve urinary function.
- Witness: Roberts1993.pdf.md (Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend): purified neutrophils preincubated 15 min: 1 µmol/L pentoxifylline did not inhibit FMLP superoxide rate or total; ≥5 µmol/L inhibited both. At 10 µmol/L: Rate FMLP 85% and Total FMLP 75% vs control (p<0.05).
- Source: roberts1993.pdf.md Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness shows a plausible biological effect of PTX on an inflammatory/oxidative process (“≥5 µmol/L inhibited [superoxide] rate and total”) but it is in purified neutrophils in vitro and does not address urinary tissue delivery, the specific cohort, or urinary function improvement.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The unit assumes that changing relevant processes can improve urinary function (a mechanistic plausibility component). The witness shows PTX can inhibit an inflammatory/oxidative process in vitro ("≥5 µmol/L inhibited" neutrophil superoxide production), but it does not establish in-vivo urinary-tissue exposure, the cohort context, or urinary-function improvement.

### A1-H1-C2 x W-FRD-Q0013-03-c4-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness defines bladder outlet obstruction criteria (>45 cm water detrusor contraction, <12 ml/s flow, radiographic obstruction) and says nothing about vitamin E or any cointervention being explicit in a rationale/trial specification.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only defines bladder outlet obstruction criteria (“sustained detrusor contraction >45 cm water… flow rate <12 ml/s… radiographic evidence”) and says nothing about vitamin E/any cointervention being explicitly specified as necessary in the trial rationale/specification.

### A1-H1-C2 x W-FRD-Q0018-03-Q0018
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Bortnick2020.pdf.md reports AUA guidelines recommend alpha-blocker plus 5-ARI combination therapy for men with moderate-severe LUTS, advanced age, and prostate size >40 g (bortnick2020.pdf.md, “Medical therapy > Combination therapy”).
- Source: bortnick2020.pdf.md Medical therapy > Combination therapy
- Pass A: NO_SEMANTIC_RELATION - Witness reports AUA guideline recommendation for alpha-blocker + 5-ARI combination therapy; it does not discuss PTX trials or any requirement to explicitly specify vitamin E or other cointerventions in a rationale.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an AUA guideline recommendation for “alpha-blocker plus 5-ARI combination therapy” in men with LUTS; it does not address vitamin E or any cointervention contribution being explicit in a trial’s rationale/specification.

### A1-H1-C2 x W-FRD-Q0019-03-c3-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX inhibits neutrophil oxidative burst at 5 µmol/L in whole blood; no mention of vitamin E/cointervention dependence or any trial-specification/rationale explicitness requirement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states PTX at “5 µmol/l significantly inhibited” neutrophil burst and reports percent-of-control values; it contains no statement about vitamin E/cointerventions or any requirement that such contributions be explicit in trial rationale/specification.

### A1-H1-C2 x W-FRD-Q0020-02-c1-Q0020
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness describes PTX dosing regimens in healthy volunteers and notes crossover not explicit; it does not address whether vitamin E or any cointervention is necessary or must be explicit in a rationale/trial spec.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes PTX oral dosing in volunteers (“5×400 mg/day for 2 days… or… 7 days”) and notes crossover not explicit; it does not mention vitamin E or the need to explicitly specify cointervention contributions in rationale/trial specification.

### A1-H1-C2 x W-FRD-Q0029-04-c4-Q0029
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.5.2. Fecal Calprotectin), fecal calprotectin <100 µg/g occurred in 18 patients (66.7%) on PTX vs 14 (53.8%) on placebo; <50 µg/g occurred in 6 (20%) on PTX vs 2 (6%) on placebo. Denominators are not explicitly stated.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.5.2. Fecal Calprotectin
- Pass A: NO_SEMANTIC_RELATION - Witness reports fecal calprotectin outcomes comparing PTX vs placebo; it does not state any cointervention (vitamin E or otherwise) is necessary or should be explicitly specified.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C2 x W-FRD-Q0029-04-c5-Q0029
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: NO_SEMANTIC_RELATION - Witness reports loss to follow-up and switching to steroid therapy; this is about attrition/adjuvant therapy after severe disease, not an explicit rationale/trial-spec dependency on vitamin E or other cointerventions.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C2 x W-FRD-Q0034-02-bortnick20-c3-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Bortnick et al. (2020) report that risk of self-harm was elevated significantly during the initial 18 months on a 5-ARI, though there was no increased risk of suicide (bortnick2020.pdf.md, Medical therapy → 5-alpha reductase inhibitors).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → subsection “5-alpha reductase inhibitors”
- Pass A: NO_SEMANTIC_RELATION - Witness concerns 5-ARI self-harm risk timing; unrelated to PTX and to explicit identification of vitamin E/cointervention contributions in trial rationale/specification.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C2 x W-FRD-Q0034-03-c4-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Saw palmetto 320 mg daily may cause GI upset and headache and “may enhance the anticoagulation effect of warfarin” (fdp03812573_1.pdf.md, TABLE “Benign Prostatic Enlargement Medications”).
- Source: fdp03812573_1.pdf.md TABLE “Benign Prostatic Enlargement Medications” → Natural Products → Saw palmetto row (Daily Doses and Comments columns).
- Pass A: NO_SEMANTIC_RELATION - Witness lists saw palmetto adverse effects and warfarin interaction; it does not discuss PTX benefit depending on vitamin E or other cointerventions or any explicitness requirement.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C2 x W-FRD-Q0050-03-Q0050
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only states “pentoxifylline inhibits PDE 1–5” with IC50 values; it does not discuss vitamin E or any cointervention, nor any need to make such a dependency explicit.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C2 x W-FRD-Q0063-01-c5-Q0063
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports in vitro PMN degranulation changes with "Pentoxifylline 1 or 100 µg/ml" and does not discuss vitamin E or cointervention dependence/explicitness.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C2 x W-FRD-Q0064-04-c1-Q0064
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: In male Wistar–Kyoto rats (230–300 g), after baseline haemodynamics, investigators gave saline or pentoxifylline 3 mg/kg i.v., then 30 min later saline or E. coli LPS 10 mg/kg i.v., monitoring for 240 min (wu1999.pdf.md, Methods 2.1 Endotoxic shock).
- Source: wu1999.pdf.md Methods 2.1 Endotoxic shock
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness specifies PTX "3 mg/kg i.v." and LPS challenge timing in rats; it does not mention vitamin E or any cointervention rationale/specification.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C2 x W-FRD-Q0078-02-c1-Q0078
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: desouza2009.pdf.md (Patients and methods > Study design): open-label 24-week-per-patient trial; all treated SSc patients received pentoxiphylline 800 mg/day associated with vitamin E 800 UI/day; results compared with a historical control group. desouza2009.pdf.md (Patients and methods > Historical control group): 9 diffuse SSc patients retrospectively used as controls received cyclophosphamide 0.5–1 g/m^2 during 6 months.
- Source: desouza2009.pdf.md Patients and methods > Study design; Patients and methods > Historical control group
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness explicitly states the cointervention in the specification: "all treated SSc patients received pentoxiphylline 800 mg/day associated with vitamin E 800 UI/day"; however it does not say vitamin E is necessary for benefit nor that the rationale explicitly identifies dependency vs PTX alone.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-C2 x W-FRD-Q0079-04-c3-Q0079
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness describes PTX up to "50 µmol/L" vs "500 µmol/L" effects on [Ca2+]i and contains no mention of vitamin E or cointervention dependence/explicitness.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX concentration effects on neutrophil [Ca2+]i after FMLP (e.g., "PTX up to 50 µmol/L...; 500 µmol/L reduced...") and does not mention vitamin E, any cointervention, or any requirement that such contributions be explicit in rationale/trial specification.

### A1-H1-C2 x W-FRD-Q0085-01-c3-Q0085
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety): During the study, no severe adverse effects were reported, including no threatening hypotension or syncope; vital signs remained almost stable; no urinary retention occurred; and therapy did not stop for TEAEs (not explicitly phrased as zero TEAE dropouts).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness addresses "no severe adverse effects" and stable vital signs; it does not address vitamin E or whether any benefit depends on a cointervention that must be explicitly specified.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses safety outcomes ("no severe adverse effects... vital signs remained almost stable") and contains no statement about vitamin E/cointerventions or that any necessary contribution must be explicitly stated in the rationale or trial specification.

### A1-H1-C2 x W-FRD-Q0089-04-c2-Q0089
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness speculates about PTX anti-inflammatory potency once inflammation is triggered and does not mention vitamin E or trial rationale/specification about cointervention dependence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness speculates about PTX anti-inflammatory potency once inflammation is triggered; it does not address vitamin E or whether any cointervention contribution must be explicit in the trial rationale/specification.

### A1-H1-C2 x W-FRD-Q0090-04-c3-Q0090
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports neutrophil [Ca2+]i changes with PTX concentrations and does not discuss vitamin E, cointerventions, or any requirement to specify their contribution.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports purified neutrophil [Ca2+]i changes with PTX up to 50 vs 500 µmol/L and has no mention of vitamin E, cointerventions, or explicit trial specification of cointervention contributions.

### A1-H1-C2 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness explicitly specifies a cointervention regimen: "pentoxifylline 800 mg/day plus vitamin E 800 UI/day" in the trial design, but it does not state that vitamin E is a necessary contributor or that any rationale explicitly attributes dependency vs PTX-alone.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness explicitly includes a cointervention in the study design ("pentoxifylline 800 mg/day plus vitamin E 800 UI/day"), which relates to trial specification, but it does not state that vitamin E's contribution is necessary or that such necessity was made explicit in the rationale/specification.

### A1-H1-C2 x W-FRD-Q0098-01-Q0098
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness describes "IV PTX 40 mg/kg" in rats and outcomes (MAP/HR/WBC; "they all died"), with no mention of vitamin E or cointervention dependence/explicitness.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports IV PTX dosing in rats and physiologic outcomes (MAP/HR/WBC; "they all died") with no discussion of vitamin E, cointerventions, or explicit rationale/specification requirements for cointerventions.

### A1-H1-C2 x W-FRD-Q0104-03-c6-Q0104
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about hs-CRP longitudinal statistics for "infliximab vs placebo" and does not address vitamin E or any cointervention requirements in a PTX intervention rationale/specification.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns infliximab vs placebo effects on hs-CRP (t-tests, P-values) and does not mention vitamin E/cointerventions or any requirement that cointervention contributions be explicit in rationale/trial specification.

### A1-H1-C2 x W-FRD-Q0131-03-c3-Q0131
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only states "PTX has short half-life about 1.6 h" and contains no claim about vitamin E or cointervention dependence/explicitness.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states a pharmacokinetic fact ("PTX has short half-life about 1.6 h") and provides no content about vitamin E or explicit specification of necessary cointerventions.

### A1-H1-C2 x W-FRD-Q0131-03-c4-Q0131
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports "PTX toxicity... at 80 mg/kg" and adverse effects; it does not mention vitamin E, cointerventions, or any need to specify cointervention dependency.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX toxicity at a dose ("toxicity... at 80 mg/kg" with hypotension/flushing/convulsion) and does not address vitamin E, cointerventions, or explicit rationale/specification of their necessary contribution.

### A1-H1-C2 x W-FRD-Q0149-04-c4-Q0149
- Unit (CONTEXTUAL_CONSTRAINT): Any necessary contribution from vitamin E or another cointervention must be explicit in the rationale and trial specification.
- Witness: Raison2013 (raison2013.pdf.md, RESULTS): in subgroup mixed-effects models for repeated measures, standardized effect size difference at 12 weeks was “moderate to large, in opposite directions”: 0.41 favoring infliximab for baseline hs-CRP >5 mg/L, versus −0.82 favoring placebo for baseline hs-CRP ≤5 mg/L.
- Source: raison2013.pdf.md RESULTS (paragraph containing standardized effect sizes); Figure 4
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness discusses "infliximab" and "placebo" effect sizes by hs-CRP subgroup and says nothing about pentoxifylline, vitamin E, or cointervention dependency/explicitness.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses subgroup effect sizes for infliximab vs placebo by baseline hs-CRP and contains no mention of vitamin E/cointerventions or any requirement that cointervention contributions be explicit in trial rationale/specification.

### A1-H1-E1 x W-FRD-Q0013-01-c4-Q0013
- Unit (CORROBORATING_EXPECTATION): Corroboration would consist of converging findings linking attainable exposure to target engagement, physiological improvement, and improved relevant function, with discrimination by timing, dose-response, predictors, and contrary results; and identifying measurable patient characteristics and trial outcomes that should reveal benefit.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: NO_SEMANTIC_RELATION - Witness is about diagnostic protocol for pseudodyssynergia using private-setting uroflowmetry to reduce false positives from performance anxiety; it does not link PTX exposure to target engagement/physiology/function or provide trial benefit discriminators/predictors.
- Pass B: PARTIALLY_COVERS - Witness specifies a measurable diagnostic discriminator: pseudodyssynergia diagnosis required uroflowmetry showing 'intermittent increases and decreases in flow' in an 'undulating fashion' under private conditions. It helps define patient characteristics/outcome measurement but does not provide PTX exposure→engagement→benefit linkage.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The unit includes “identifying measurable patient characteristics and trial outcomes that should reveal benefit.” The witness specifies a measurable diagnostic discriminator for pseudodyssynergia—private-setting uroflowmetry showing flow “in an undulating fashion”—which contributes to outcome/phenotype measurement, but it does not link any exposure to target engagement, physiological improvement, or functional benefit.

### A1-H1-E1 x W-FRD-Q0013-03-c4-Q0013
- Unit (CORROBORATING_EXPECTATION): Corroboration would consist of converging findings linking attainable exposure to target engagement, physiological improvement, and improved relevant function, with discrimination by timing, dose-response, predictors, and contrary results; and identifying measurable patient characteristics and trial outcomes that should reveal benefit.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Defines bladder outlet obstruction criteria (detrusor pressure, flow rate, radiographic obstruction) but makes no claims about PTX exposure→engagement→physiology→function linkage or discriminating predictions of benefit.
- Pass B: PARTIALLY_COVERS - Witness provides measurable clinical criteria: BOO defined as 'detrusor contraction >45 cm water' + 'flow rate <12 ml/s' + imaging evidence. This contributes to phenotype/outcome specification but not the unit’s required PTX exposure→engagement→physiology→function corroboration.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness provides explicit measurable criteria defining a patient/phenotype state: “sustained detrusor contraction >45 cm water” plus “flow rate <12 ml/s” plus radiographic prostatic obstruction. This supports the unit’s measurement/characterization component but does not provide the unit’s required exposure→target engagement→physiology/function improvement chain.

### A1-H1-E1 x W-FRD-Q0014-02-Q0014
- Unit (CORROBORATING_EXPECTATION): Corroboration would consist of converging findings linking attainable exposure to target engagement, physiological improvement, and improved relevant function, with discrimination by timing, dose-response, predictors, and contrary results; and identifying measurable patient characteristics and trial outcomes that should reveal benefit.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns ultrasound DWT and bladder capacity as noninvasive predictors of detrusor underactivity; it does not address PTX, target engagement, or an exposure→physiology→function chain for PTX benefit.
- Pass B: PARTIALLY_COVERS - Witness identifies measurable patient characteristics and discriminative prediction: 'DWT ≤1.23 mm plus bladder capacity >445 ml' to detect/predict DU with 'PPV 100%, NPV 85%'. It does not link PTX exposure to target engagement or improvement, so it covers only the predictor/measurement component of the unit.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The unit expects “discrimination by…predictors” and “identifying measurable patient characteristics.” The witness supplies noninvasive predictive characteristics—“DWT ≤1.23 mm plus bladder capacity >445 ml” predicting DU with “PPV 100%, NPV 85%”—but says nothing about PTX exposure, target engagement, or improvement.

### A1-H1-E1 x W-FRD-Q0044-04-c2-Q0044
- Unit (CORROBORATING_EXPECTATION): Corroboration would consist of converging findings linking attainable exposure to target engagement, physiological improvement, and improved relevant function, with discrimination by timing, dose-response, predictors, and contrary results; and identifying measurable patient characteristics and trial outcomes that should reveal benefit.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - States no adverse effects were observed with pentoxifylline treatment, which is safety/tolerability only; it does not provide exposure→engagement→physiology→function linkage or discriminators/predictors of benefit.
- Pass B: PARTIALLY_COVERS - Witness contributes a trial outcome expectation about tolerability: 'Adverse effects were not reported' / 'No adverse effects ... observed' for pentoxifylline. It does not provide the unit’s required exposure→engagement→physiology→function corroboration or discriminators.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only reports safety/tolerability (“No adverse effects…observed” with pentoxifylline) and does not address the unit’s corroboration elements: linking attainable exposure to target engagement, physiological improvement, improved function, or discriminating predictors/contrary results revealing benefit.

### A1-H1-E1 x W-FRD-Q0078-02-c1-Q0078
- Unit (CORROBORATING_EXPECTATION): Corroboration would consist of converging findings linking attainable exposure to target engagement, physiological improvement, and improved relevant function, with discrimination by timing, dose-response, predictors, and contrary results; and identifying measurable patient characteristics and trial outcomes that should reveal benefit.
- Witness: desouza2009.pdf.md (Patients and methods > Study design): open-label 24-week-per-patient trial; all treated SSc patients received pentoxiphylline 800 mg/day associated with vitamin E 800 UI/day; results compared with a historical control group. desouza2009.pdf.md (Patients and methods > Historical control group): 9 diffuse SSc patients retrospectively used as controls received cyclophosphamide 0.5–1 g/m^2 during 6 months.
- Source: desouza2009.pdf.md Patients and methods > Study design; Patients and methods > Historical control group
- Pass A: NO_SEMANTIC_RELATION - Describes an open-label systemic-sclerosis trial design and dosing (PTX 800 mg/day + vitamin E) with historical controls; it does not report converging findings linking exposure to target engagement, physiology, and relevant function with discriminators/predictors.
- Pass B: PARTIALLY_COVERS - Witness provides dose/timing and a comparative design element ('results compared with a historical control group' with cyclophosphamide controls). It still lacks the unit’s required linkage to target engagement and to urinary physiology/function outcomes.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - This is trial design/exposure description (open-label 24-week; “pentoxiphylline 800 mg/day…vitamin E”; historical controls) without any findings about target engagement, physiological/functional improvement, or discriminating dose-response/timing/predictors as required by the unit.

### A1-H1-E1 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (CORROBORATING_EXPECTATION): Corroboration would consist of converging findings linking attainable exposure to target engagement, physiological improvement, and improved relevant function, with discrimination by timing, dose-response, predictors, and contrary results; and identifying measurable patient characteristics and trial outcomes that should reveal benefit.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: NO_SEMANTIC_RELATION - States enrollment and dosing regimen for an open-label systemic-sclerosis study; without findings on engagement/physiology/function and discriminators, it does not satisfy or materially cover the unit’s required linkage/predictions.
- Pass B: PARTIALLY_COVERS - Witness establishes an attainable clinical exposure regimen and timing: 'open-label 24-week study' with 'pentoxifylline 800 mg/day plus vitamin E'. It does not supply target engagement, voiding physiology improvement, or functional urinary outcomes/discriminators.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only states enrollment and regimen (“open-label 24-week… pentoxifylline 800 mg/day plus vitamin E 800 UI/day”) and provides no converging findings linking exposure to target engagement and improved physiology/function or any discriminators/predictors of benefit.

### A1-H1-E1 x W-FRD-Q0102-04-c2-Q0102
- Unit (CORROBORATING_EXPECTATION): Corroboration would consist of converging findings linking attainable exposure to target engagement, physiological improvement, and improved relevant function, with discrimination by timing, dose-response, predictors, and contrary results; and identifying measurable patient characteristics and trial outcomes that should reveal benefit.
- Witness: Chung2014 reports detrusor biopsy in UAB showed ~4× more disruptive cells than normal bladder function, and no significant correlation between patient age and disruptive-cell number in the detrusor wall, interpreted as suggesting it is not aging per se (chung2014.pdf.md, “## Making the Diagnosis”).
- Source: chung2014.pdf.md ## Making the Diagnosis (paragraph beginning “Electron microscopic examination may reveal…”)
- Pass A: NO_SEMANTIC_RELATION - Reports detrusor biopsy disruptive-cell counts and lack of correlation with age; it does not connect PTX exposure to engagement or to physiological/functional improvement, nor provide discriminators/predictors for PTX benefit.
- Pass B: PARTIALLY_COVERS - Witness gives a measurable bladder characteristic: detrusor biopsy showed '~4× more disruptive cells' and 'no significant correlation' with age, suggesting not aging. This is a potential phenotype/predictor element but lacks PTX exposure→engagement and voiding improvement linkage required by the unit.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The unit includes “identifying measurable patient characteristics.” The witness reports a measurable bladder tissue characteristic (“~4× more disruptive cells” in detrusor biopsy; “no significant correlation…with age”), which could contribute to patient characterization, but it does not connect any exposure to target engagement or improvement in function.

### A1-H1-R1 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Defines detrusor underactivity (reduced contraction strength/duration causing prolonged/incomplete emptying) but says nothing about reversibility, an identifiable subgroup of the specified men, or inadequacy of tamsulosin and pelvic-floor intervention.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only provides the ICS definition of detrusor underactivity (“contraction of reduced strength and/or duration... prolonged bladder emptying... failure to achieve complete bladder emptying”). It does not mention an identifiable subgroup of the men in question, reversibility, or inadequate response to tamsulosin plus pelvic-floor intervention.

### A1-H1-R1 x W-FRD-Q0007-04-c4-Q0007
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: PARTIALLY_COVERS - Mentions a potential transition to 'irreversible bladder decompensation and failure' after a 'point of no return,' which implies earlier stages may be more reversible, but it does not state reversibility in a subgroup of the cohort nor that tamsulosin and prescribed pelvic-floor intervention inadequately address the component.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness warns about a “point of no return” after which “irreversible bladder decompensation and failure occur,” which is related to (ir)reversibility of bladder physiology. It still does not state that, in an identifiable subgroup of the target men, a reversible component contributes to persistent voiding difficulty and is not adequately addressed by tamsulosin and pelvic-floor intervention.

### A1-H1-R1 x W-FRD-Q0009-02-c2-Q0009
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Chuang2015.pdf.md (## EPIDEMIOLOGY) summarizes Abarbanel & Marcus: in 181 LUTS patients aged ≥70 (82 men, 99 women), impaired detrusor contractility was defined urodynamically as Qmax <10 mL/s plus detrusor pressure <30 cm H2O, and was reported in 48% of men and 12% of women.
- Source: chuang2015.pdf.md ## EPIDEMIOLOGY (paragraph beginning “In men, detrusor underactivity may be caused… Abarbanel and Marcus…”)
- Pass A: NO_SEMANTIC_RELATION - Reports prevalence of impaired detrusor contractility in older LUTS patients (48% of men ≥70) under specific urodynamic criteria, but does not address reversibility or treatment inadequacy (tamsulosin/PF intervention) in the hypothesis cohort.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports prevalence of “impaired detrusor contractility” in LUTS patients aged ≥70 (e.g., “48% of men”), under a urodynamic definition. It does not address reversibility, persistent difficulty voiding despite tamsulosin/pelvic-floor intervention, or any inadequacy of those treatments.

### A1-H1-R1 x W-FRD-Q0018-03-Q0018
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Bortnick2020.pdf.md reports AUA guidelines recommend alpha-blocker plus 5-ARI combination therapy for men with moderate-severe LUTS, advanced age, and prostate size >40 g (bortnick2020.pdf.md, “Medical therapy > Combination therapy”).
- Source: bortnick2020.pdf.md Medical therapy > Combination therapy
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is a guideline recommendation for 'alpha-blocker plus 5-ARI combination therapy' and does not claim a reversible physiological component or failure of tamsulosin plus pelvic-floor intervention.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states AUA guidelines “recommend alpha-blocker plus 5-ARI combination therapy” for certain men with LUTS. It makes no claim about a reversible physiological component causing persistent voiding difficulty, nor that tamsulosin and a prescribed pelvic-floor intervention inadequately address it.

### A1-H1-R1 x W-FRD-Q0027-01-c3-Q0027
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): According to Osman et al. [4] review, DU was reported in 9%–28% of men aged <50 years, 48% of men aged >70 years, and 12%–45% of women aged >70 years.
- Source: 2020ICU_icu-58-S68.pdf.md PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (paragraph beginning 'According to the recent review from Osman et al. [4], ...')
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Witness gives prevalence ranges where 'DU was reported' in older men/women, which relates to physiological voiding dysfunction, but it does not address reversibility or inadequate response to 'tamsulosin' plus pelvic-floor intervention in the specified cohort.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness provides prevalence ranges where “DU was reported” in men by age group (e.g., “48% of men aged >70 years”), which relates to a physiological contributor to voiding difficulty. It does not establish reversibility or inadequate response to tamsulosin plus pelvic-floor intervention in an identifiable subgroup of the unit’s men.

### A1-H1-R1 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Witness reports many diabetic men with LUTS had 'detrusor underactivity (DU)' (a physiological dysfunction relevant to voiding difficulty), but it does not state reversibility nor that DU is 'not adequately addressed by tamsulosin' or 'pelvic-floor intervention,' and the population differs from the unit scope.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports that among “52 men with diabetes ... with bothersome LUTS,” “79% had detrusor underactivity (DU),” which is a physiological voiding dysfunction relevant to the unit’s general topic. It does not state reversibility or that this component is not adequately addressed by tamsulosin and prescribed pelvic-floor intervention, and the population is specifically diabetic men.

### A1-H1-R1 x W-FRD-Q0029-04-c5-Q0029
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only states patients were 'lost to follow-up' in mesalamine and PTX groups; it does not concern voiding, tamsulosin, pelvic-floor therapy, or reversibility.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only discusses study follow-up attrition (patients “lost to follow-up” in mesalamine/placebo and PTX groups). It contains no content about voiding difficulty, bladder physiology, reversibility, tamsulosin, or pelvic-floor intervention.

### A1-H1-R1 x W-FRD-Q0034-01-bortnick20-c3-Q0034
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: bortnick2019.pdf.md (Review of Medications > Alpha Blockers) reports Duan et al. used 2006–2012 Medicare data in a cohort of 253,136 men >65 with BPH; dementia (ICD-9 codes) risk after mean 19.8 months was significantly higher with tamsulosin versus no BPH meds and versus doxazosin, terazosin, alfuzosin, dutasteride, or finasteride.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about 'dementia ... risk ... higher with tamsulosin' and contains no claim about a reversible component of voiding difficulty or about pelvic-floor interventions being inadequate.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns “dementia ... risk ... higher with tamsulosin” versus other groups. It does not address persistent difficulty voiding, a reversible physiological component, or inadequacy of tamsulosin with pelvic-floor intervention.

### A1-H1-R1 x W-FRD-Q0034-02-bortnick20-c2-Q0034
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Bortnick2020.pdf.md (“Medical therapy” → “5-alpha reductase inhibitors”): Welk et al. report a population-based, retrospective, propensity-matched Canadian cohort of 93,000 men >66 years on 5-ARIs (median 1.57 years) in which depression risk was elevated during the initial 18 months after starting a 5-ARI and remained elevated, less so, thereafter.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → subsection “5-alpha reductase inhibitors”
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports 'depression risk was elevated' after starting a '5-ARI'; it does not address voiding physiology, reversibility, or nonresponse to 'tamsulosin' and 'pelvic-floor intervention.'
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports “depression risk was elevated” after starting a “5-ARI.” No claim is made about voiding physiology, reversibility, or nonresponse to tamsulosin plus pelvic-floor intervention.

### A1-H1-R1 x W-FRD-Q0034-02-bortnick20-c3-Q0034
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Bortnick et al. (2020) report that risk of self-harm was elevated significantly during the initial 18 months on a 5-ARI, though there was no increased risk of suicide (bortnick2020.pdf.md, Medical therapy → 5-alpha reductase inhibitors).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → subsection “5-alpha reductase inhibitors”
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses 'risk of self-harm' and 'no increased risk of suicide' during 5-ARI use, not 'reversible physiological component' of voiding difficulty nor failure of 'tamsulosin and ... pelvic-floor intervention.'
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states “risk of self-harm was elevated” during initial 18 months on a “5-ARI,” with “no increased risk of suicide.” This does not concern voiding difficulty, reversible physiology, or tamsulosin/pelvic-floor intervention adequacy.

### A1-H1-R1 x W-FRD-Q0034-03-c1-Q0034
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Tadalafil 5 mg daily includes the comment “avoid nitrates” (fdp03812573_1.pdf.md, TABLE “Benign Prostatic Enlargement Medications”).
- Source: fdp03812573_1.pdf.md TABLE “Benign Prostatic Enlargement Medications” → Phosphodiesterase-5 Inhibitors → Tadalafil row (Comments column).
- Pass A: NO_SEMANTIC_RELATION - Witness only states tadalafil 5 mg daily has a safety comment “avoid nitrates”; it does not address persistent difficulty voiding, a reversible physiological component, or inadequacy of tamsulosin plus pelvic-floor intervention.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R1 x W-FRD-Q0034-03-c5-Q0034
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: fdp03812573_1.pdf.md (Medication Management → Phosphodiesterase-5 enzyme inhibitors): Daily tadalafil should not be prescribed in men with creatinine clearance <30 mL/min.
- Source: fdp03812573_1.pdf.md Medication Management section → Phosphodiesterase-5 enzyme inhibitors paragraph (narrative text following the medication table).
- Pass A: NO_SEMANTIC_RELATION - Witness is a prescribing restriction (tadalafil not for men with creatinine clearance <30 mL/min) and contains no claim about a reversible voiding dysfunction or failure of tamsulosin and prescribed pelvic-floor intervention to address it.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R1 x W-FRD-Q0034-04-bortnick20-c1-Q0034
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: bortnick2020.pdf.md (“Medical therapy”→“Combination therapy” MTOPS paragraph) reports MTOPS studied finasteride+doxazosin in 3000 men (mean age 62.6 years, SD 7.3) and found combination therapy improved voiding symptoms and maximum urinary flow rate more than either alone, prevented BPH progression better, and reduced the long-term risk of acute urinary retention and need for invasive therapy.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (MTOPS paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness reports MTOPS results for finasteride+doxazosin improving BPH outcomes; it does not mention pelvic-floor intervention or an identifiable subgroup with a reversible physiological component not adequately addressed by tamsulosin plus pelvic-floor therapy.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes MTOPS findings on finasteride+doxazosin improving BPH outcomes (voiding symptoms, max flow, progression, AUR/surgery). It does not mention an identifiable subgroup, reversibility, pelvic-floor intervention, or inadequacy of tamsulosin plus pelvic-floor therapy for persistent voiding difficulty.

### A1-H1-R1 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: NO_SEMANTIC_RELATION - Witness summarizes CombAT combination therapy benefits vs monotherapy; it does not address pelvic-floor treatment, reversibility of a physiological component, or inadequacy of tamsulosin plus pelvic-floor intervention in a subgroup.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness summarizes CombAT: combination therapy reduced AUR/BPH surgery and clinical progression vs monotherapy. No content about pelvic-floor intervention, persistent difficulty voiding despite tamsulosin, or a reversible physiological component in any subgroup.

### A1-H1-R1 x W-FRD-Q0045-03-c1-Q0045
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: In Glazener2011 (glazener2011.pdf.md, Table 2), radical-prostatectomy intervention-group men (N=205) attended therapy visits: 189 (92%) visit 1, 186 (91%) visit 2, 177 (86%) visit 3, and 175 (85%) visit 4.
- Source: glazener2011.pdf.md Table 2 (Radical prostatectomy; intervention group attendance)
- Pass A: NO_SEMANTIC_RELATION - Witness gives attendance rates for therapy visits among radical-prostatectomy intervention-group men; it does not claim pelvic-floor intervention was ineffective or that voiding difficulty includes a reversible physiological component not addressed by tamsulosin plus pelvic-floor therapy.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports attendance rates at therapy visits among radical-prostatectomy intervention-group men (visit 1–4 percentages). It does not address voiding difficulty mechanisms, reversibility, tamsulosin, or whether pelvic-floor intervention is inadequate.

### A1-H1-R1 x W-FRD-Q0052-04-c1-Q0052
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: In nihms-1048633.pdf.md (Fig. 1 CONSORT diagram), 981 were assessed; 958 female patients were included; 23 were excluded, including “Male / transgender” (n=8).
- Source: nihms-1048633.pdf.md Fig. 1 CONSORT diagram (participant flow/exclusions)
- Pass A: NO_SEMANTIC_RELATION - Witness reports a study inclusion flowchart dominated by female patients and exclusion of males/transgender; it provides no information about men with BPH, persistent voiding difficulty, reversibility, or failure of tamsulosin plus pelvic-floor intervention.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is a CONSORT flow detail: mostly female patients included and exclusion of “Male/transgender (n=8).” It provides no claim about men with persistent voiding difficulty, tamsulosin response, pelvic-floor intervention, or reversible physiology.

### A1-H1-R1 x W-FRD-Q0053-02-c4-Q0053
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: NO_SEMANTIC_RELATION - Witness concerns PFME questionnaire timing and generalizability in women after ≥6 weeks PFME; it does not address the unit’s male BPH cohort, persistent difficulty voiding, or inadequacy of tamsulosin plus prescribed pelvic-floor intervention.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses questionnaire timing after ≥6 weeks PFME and cautions on generalizing findings to women at different PFME stages. The unit is about men with persistent voiding difficulty and inadequacy of tamsulosin plus prescribed pelvic-floor intervention with a reversible component; none of these are stated.

### A1-H1-R1 x W-FRD-Q0053-04-c4-Q0053
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: In s12912-023-01326-5.pdf.md (Results → Characteristics of the study participants → Table 4), among 123 participants, gender was male 88 (71.5%) and female 35 (28.5%); history of pelvic surgery was yes 122 (99.2%) and no 1 (0.8%).
- Source: s12912-023-01326-5.pdf.md Results → Characteristics of the study participants → Table 4
- Pass A: NO_SEMANTIC_RELATION - Witness only reports participant gender mix and near-universal pelvic surgery history in a 123-person sample; it does not establish a reversible physiological voiding component or failure of tamsulosin and prescribed pelvic-floor intervention.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only lists sample characteristics (gender counts; history of pelvic surgery 99.2%). It does not state persistent difficulty voiding, reversibility, use of tamsulosin, pelvic-floor intervention, or inadequacy in any identifiable subgroup.

### A1-H1-R1 x W-FRD-Q0072-04-c1-Q0072
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (METHODS > Subjects) reports that, during a two-year period after unilateral adrenalectomy in 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, symptomatic thyroid dysfunction developed in 3 of 24 patients.
- Source: Takasu1990_Cushings_Syndrome_Due.md METHODS > Subjects
- Pass A: NO_SEMANTIC_RELATION - Witness is about thyroid dysfunction developing after unilateral adrenalectomy in Cushing’s syndrome patients; it is unrelated to male voiding difficulty, tamsulosin response, or pelvic-floor intervention adequacy.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports thyroid dysfunction developing after unilateral adrenalectomy in Cushing’s syndrome patients. This is unrelated in population and topic to male voiding difficulty, tamsulosin, pelvic-floor intervention, or reversible physiological components.

### A1-H1-R1 x W-FRD-Q0072-04-c2-Q0072
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (DISCUSSION) reports that among 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, 5 patients (including the 3 who later developed thyroid dysfunction) had increased antimicrosomal-antibody titers: 5/24 (21%), described as high versus 8.5% in normal women in Japan.
- Source: Takasu1990_Cushings_Syndrome_Due.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Witness reports antimicrosomal-antibody titers in Cushing’s syndrome patients; it contains no claim about urinary voiding physiology, reversibility, or treatment failure with tamsulosin and pelvic-floor intervention.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R1 x W-FRD-Q0085-01-c3-Q0085
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety): During the study, no severe adverse effects were reported, including no threatening hypotension or syncope; vital signs remained almost stable; no urinary retention occurred; and therapy did not stop for TEAEs (not explicitly phrased as zero TEAE dropouts).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: NO_SEMANTIC_RELATION - Witness is a safety finding (no severe adverse effects, no urinary retention, no stopping for TEAEs) in a tamsulosin±pentoxifylline study; it does not assert that an identifiable subgroup has a reversible physiological component of persistent voiding difficulty not adequately addressed by tamsulosin plus pelvic-floor intervention.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R1 x W-FRD-Q0131-04-Q0131
- Unit (REQUIRED_SUPPORT): In an identifiable subgroup of these men, there is a reversible physiological component contributing to persistent difficulty voiding that is not adequately addressed by tamsulosin and their prescribed pelvic-floor intervention.
- Witness: Bortnick2019.pdf.md (Review of Medications > Alpha Blockers) reports FORTA for men >65: silodosin and tamsulosin are “caution” because no older-adult efficacy/safety data and hypotension risk, especially with other antihypertensive medications; alfuzosin, doxazosin, and terazosin are “avoid” due to orthostatic hypotension, vasodilatory effects, cardiac arrhythmias, and syncope.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: NO_SEMANTIC_RELATION - Witness reports FORTA safety/caution ratings for alpha blockers in men >65; it does not address whether persistent voiding difficulty includes a reversible physiological component or whether pelvic-floor intervention plus tamsulosin is inadequate.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R2 x W-FRD-Q0007-04-c1-Q0007
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness discusses “afferent dysfunction… altered… P2X3… diminished… ATP” in BOO/DU but does not mention PTX/metabolites, exposures, or sufficiency of action at attainable exposures.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness discusses BOO/DU mechanisms (“afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP”) but does not mention PTX/metabolites or any “clinically attainable exposures,” so it provides no support for PTX acting on the proposed reversible physiological component at such exposures.

### A1-H1-R2 x W-FRD-Q0019-02-Q0019
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness provides the “clinically attainable” exposure element (“peak plasma… <5 μmol/l… combined… unlikely… exceed 10 μmol/l”) but does not link those exposures to being sufficient to act on the specific proposed reversible physiological component.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness gives clinically attainable systemic exposure bounds (“peak plasma PTX levels are <5 μmol/l… combined level of all active forms… unlikely to exceed 10 μmol/l”) but does not state that PTX/metabolites at those exposures act on the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness shows PTX “as low as 5 µmol/l significantly inhibited” a biological effect, which is evidence of activity at a stated concentration, but it is in neutrophil oxidative burst (not the proposed reversible voiding physiology component) and does not itself establish that 5 µmol/L is clinically attainable in the relevant tissue/component.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - It shows PTX has biological activity at a low stated concentration (“as low as 5 µmol/l significantly inhibited… burst”), but this effect is in neutrophil oxidative activity (not the proposed reversible physiological component) and does not establish that such concentrations are clinically attainable at the target component/tissue.

### A1-H1-R2 x W-FRD-Q0020-02-c1-Q0020
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness establishes plausible human oral dosing (“treated orally… 5×400 mg/day”) but does not report concentrations achieved or that such exposures are sufficient to act on the proposed reversible physiological component.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness establishes human oral dosing (“treated orally with pentoxifylline 5×400 mg/day”) but does not report achieved exposures/concentrations or any action on the proposed reversible physiological component at clinically attainable exposures.

### A1-H1-R2 x W-FRD-Q0029-04-c4-Q0029
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.5.2. Fecal Calprotectin), fecal calprotectin <100 µg/g occurred in 18 patients (66.7%) on PTX vs 14 (53.8%) on placebo; <50 µg/g occurred in 6 (20%) on PTX vs 2 (6%) on placebo. Denominators are not explicitly stated.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.5.2. Fecal Calprotectin
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports fecal calprotectin proportions on PTX vs placebo, but does not mention achieved PTX exposures or action on the specific reversible physiological component relevant to voiding/DU/BOO.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports outcomes on fecal calprotectin under PTX vs placebo (“<100 µg/g… <50 µg/g”) but contains no statement about PTX/metabolite exposures being clinically attainable or about acting on the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0029-04-c5-Q0029
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Loss to follow-up (“did not return”, “shifted to… steroid therapy”) provides neither exposure levels nor evidence PTX/metabolites act on the proposed reversible physiological component.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only describes attrition (“lost to follow-up… shifted to… steroid therapy… did not return”) and provides no information about PTX/metabolite exposure levels or mechanistic action on the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0034-02-bortnick20-c3-Q0034
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Bortnick et al. (2020) report that risk of self-harm was elevated significantly during the initial 18 months on a 5-ARI, though there was no increased risk of suicide (bortnick2020.pdf.md, Medical therapy → 5-alpha reductase inhibitors).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → subsection “5-alpha reductase inhibitors”
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about “risk of self-harm… on a 5-ARI” and contains no information on PTX exposures or action on the proposed reversible physiological component.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness is about 5-ARI-associated self-harm risk (“elevated… on a 5-ARI”) and does not mention PTX/metabolites, exposures, or action on the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness discusses “CombAT” combination therapy effects in BPH, with no PTX/metabolite exposure or mechanism acting on the proposed reversible physiological component.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness describes CombAT combination therapy outcomes in BPH (“greater risk reduction… than either monotherapy”) with no mention of PTX/metabolites, clinically attainable exposures, or action on the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Statements like “No adverse effects… observed” address tolerability, not whether clinically attainable exposures are sufficient to act on the reversible physiological component.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Statements that “No adverse effects… were observed” speak to tolerability and do not address whether PTX or metabolites act on the proposed reversible physiological component at clinically attainable exposures.

### A1-H1-R2 x W-FRD-Q0048-02-c1-Q0048
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In 10.1016@s0041-13450001266-5.pdf.md (PATIENTS AND METHODS), pentoxifylline was dosed 150 mg IV 2 hours pre-op, 150 mg IV after graft reperfusion, and 300 mg IV 8 hours after grafting; then 1200 mg/day in three oral doses for 7 days.
- Source: 10.1016@s0041-13450001266-5.pdf.md PATIENTS AND METHODS
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness provides clinically plausible dosing amounts/timing (e.g., “150 mg IV… 1200 mg/day… for 7 days”) but gives no achieved concentrations/exposures and no evidence those exposures are sufficient to act on the proposed reversible physiological component.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness provides clinically plausible dosing regimens (“150 mg IV… then 1200 mg/day… for 7 days”) but does not report achieved exposure levels nor that PTX/metabolites at those exposures act on the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness says PTX is “very safe” and “usually well tolerated” with GI symptoms and dizziness; it does not state what exposures are achieved nor that those exposures act on the specific proposed reversible physiological component.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness addresses safety/tolerability (“very safe… usually well tolerated… dizziness in ~3%”) and does not state clinically attainable exposure levels or that PTX/metabolites act on the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: PARTIALLY_COVERS - Witness states PTX inhibits PDE1–5 with IC50 50–200 μmol/L, addressing that PTX can act on a physiological target at certain concentrations, but it does not establish these concentrations are clinically attainable nor that the target matches the proposed reversible component in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness indicates PTX can act on a biochemical target (“inhibits PDE 1–5, with IC50 values 50–200 μmol/L”), but it does not establish these concentrations are clinically attainable nor link PDE1–5 inhibition to the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0061-02-c2-Q0061
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In siu2003.pdf.md (RESULTS), the authors report: “The mean time between the first and fourth visits was 213.40 days (30.50 weeks).”
- Source: siu2003.pdf.md RESULTS
- Pass A: NO_SEMANTIC_RELATION - Witness only reports the mean time between study visits (213.40 days) and says nothing about PTX/metabolites, exposure levels, or action on a reversible physiological component.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states: “The mean time between the first and fourth visits was 213.40 days,” with no mention of pentoxifylline/metabolites, exposures, or any physiological component being acted upon.

### A1-H1-R2 x W-FRD-Q0061-02-c5-Q0061
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In siu2003.pdf.md (Abstract (Results)), the authors report the pelvic muscle training program “appears to be able to reduce the overall urinary incontinence episodes by 85.2%.”
- Source: siu2003.pdf.md Abstract (Results)
- Pass A: NO_SEMANTIC_RELATION - Witness is about pelvic muscle training reducing incontinence episodes, not about PTX/metabolites reaching clinically attainable exposures or acting on the proposed reversible physiological component.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about a “pelvic muscle training program” reducing urinary incontinence episodes “by 85.2%,” not about PTX/metabolites acting on a reversible physiological component at clinically attainable exposures.

### A1-H1-R2 x W-FRD-Q0063-01-c1-Q0063
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Sullivan-et-al-1988: Human PMNs incubated 30 min at 37°C with pentoxifylline 300 µg/ml decreased adherence to nylon vs diluent: 64.1±2.7% (n=16) vs 54.0±3.9% (n=6; P=0.031) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → PMN adherence).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → PMN adherence (opening paragraph)
- Pass A: PARTIALLY_COVERS - Witness reports an in-vitro effect of PTX at 300 µg/ml on human PMN adherence, showing PTX can act on immune-cell physiology at a stated concentration, but does not link to clinically attainable exposure in men or to the specific reversible voiding component.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports an in-vitro instance where “pentoxifylline 300 µg/ml decreased adherence” of human PMNs, supporting that PTX can act on a physiological process at a stated concentration, but it does not establish “clinically attainable exposures” or action on the unit’s proposed reversible component.

### A1-H1-R2 x W-FRD-Q0063-01-c4-Q0063
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: PARTIALLY_COVERS - Witness reports PTX (100 µg/ml) reduced FMLP-stimulated superoxide in PMNs, demonstrating action at a given concentration, but provides no evidence that such exposure is clinically attainable in vivo or that this mechanism is the proposed reversible component affecting voiding.
- Pass B: NO_SEMANTIC_RELATION - It reports “Pentoxifylline (100 µg/ml) reduced… superoxide” in PMNs, but gives no link to clinically attainable exposures or action on the specific reversible physiological component relevant to voiding.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states “Pentoxifylline (100 µg/ml) reduced… superoxide” in PMNs, which is evidence of PTX acting on a physiological response at a specified exposure, but it does not show that exposure is clinically attainable or that it targets the proposed reversible component.

### A1-H1-R2 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: PARTIALLY_COVERS - Witness indicates PTX (1 or 100 µg/ml) reduced LPS-MCM–augmented lysozyme release in PMNs, showing an effect at stated concentrations, but does not establish clinical attainability of these exposures or relevance to the specific reversible physiological component in the cohort.
- Pass B: NO_SEMANTIC_RELATION - The witness is an in vitro PMN result where “Pentoxifylline 1 or 100 µg/ml reduced” lysozyme release; it does not state such exposures are clinically attainable or that this corresponds to the proposed reversible physiological component in the cohort.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports PTX “1 or 100 µg/ml reduced” LPS-MCM–augmented lysozyme release in PMNs, showing action at stated concentrations, but provides no statement that these are clinically attainable exposures or that this is the proposed reversible physiological component.

### A1-H1-R2 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: PARTIALLY_COVERS - Witness reports PTX up to 50 µmol/L had no effect on neutrophil calcium transients while 500 µmol/L did, giving concentration-dependent action/inaction on a physiological process, but does not show these exposures are clinically attainable or tied to the proposed reversible voiding component.
- Pass B: NO_SEMANTIC_RELATION - Reports that PTX “up to 50 µmol/L changed neither” Ca2+ and “500 µmol/L reduced” Ca2+, but does not state these are clinically attainable exposures or that this acts on the unit’s proposed reversible physiological component.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports PTX effects on neutrophil calcium transients only at “500 µmol/L” (not “up to 50 µmol/L”), demonstrating concentration-dependent physiological action/inaction, but does not connect to “clinically attainable exposures” or the proposed reversible component.

### A1-H1-R2 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: PARTIALLY_COVERS - Witness reports neutrophils showed no calcium effect at PTX ≤50 µmol/L and an effect at 500 µmol/L, which bears on what concentrations are sufficient to act on a physiological pathway, but does not establish clinical attainability or match to the proposed reversible component.
- Pass B: NO_SEMANTIC_RELATION - The witness gives in vitro effects at “500 µmol/l” on neutrophil [Ca2+]i but does not connect to clinically attainable PTX/metabolite exposures or to action on the proposed reversible physiological component for voiding.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states in purified neutrophils PTX “500 µmol/l reduced” resting and stimulated [Ca2+]i (while ≤50 µmol/l did not), supporting PTX can act on a physiological pathway at certain exposures, but does not establish clinical attainability or relevance to the proposed reversible component.

### A1-H1-R2 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: NO_SEMANTIC_RELATION - Witness describes a clinical trial dosing regimen (PTX 800 mg/day plus vitamin E) but provides no pharmacokinetic exposure levels and no evidence that those exposures are sufficient to act on the proposed reversible physiological component.
- Pass B: PARTIALLY_COVERS - It reports a clinical regimen “pentoxifylline 800 mg/day” (plausible clinical dosing), but does not state what exposures/concentrations were achieved nor that those exposures are sufficient to act on the specific reversible physiological component proposed.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports a clinical regimen “pentoxifylline 800 mg/day plus vitamin E” in patients, which is consistent with a clinically used dose (exposure plausibility), but it does not state achieved exposure levels nor that PTX/metabolites act on the proposed reversible physiological component at those exposures.

### A1-H1-R2 x W-FRD-Q0098-01-Q0098
- Unit (REQUIRED_SUPPORT): PTX or its metabolites can act on the proposed reversible physiological component at clinically attainable exposures.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: PARTIALLY_COVERS - Witness reports effects after IV PTX 40 mg/kg in rats (changes in MAP/HR/WBC with fatal shock), which shows PTX can have physiological effects at a dose, but it is not clinically attainable dosing in humans and does not address action on the proposed reversible voiding component.
- Pass B: NO_SEMANTIC_RELATION - This is a rat hemorrhage-shock pilot with “IV PTX 40 mg/kg” causing MAP/HR/WBC changes; it does not report clinically attainable human exposures nor action on the proposed reversible physiological component in men with voiding difficulty.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports an in-vivo instance where “IV PTX 40 mg/kg” in male rats altered MAP/HR/WBC, showing PTX can have physiological effects at a given dose, but it does not address clinically attainable human exposures or action on the proposed reversible component.

### A1-H1-R3 x W-FRD-Q0009-02-c2-Q0009
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Chuang2015.pdf.md (## EPIDEMIOLOGY) summarizes Abarbanel & Marcus: in 181 LUTS patients aged ≥70 (82 men, 99 women), impaired detrusor contractility was defined urodynamically as Qmax <10 mL/s plus detrusor pressure <30 cm H2O, and was reported in 48% of men and 12% of women.
- Source: chuang2015.pdf.md ## EPIDEMIOLOGY (paragraph beginning “In men, detrusor underactivity may be caused… Abarbanel and Marcus…”)
- Pass A: NO_SEMANTIC_RELATION - Witness only gives epidemiology/definition of impaired detrusor contractility in LUTS patients (prevalence in men vs women) and does not mention PTX exposure, mechanisms, or improvement in voiding.
- Pass B: PARTIALLY_COVERS - Helps identify a potential physiological subgroup ('impaired detrusor contractility... reported in 48% of men') but does not connect PTX exposure to mechanism or demonstrate improved voiding.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports an identifiable physiological subgroup within LUTS patients—“impaired detrusor contractility… reported in 48% of men”—but provides no PTX exposure/effect and no causal/mechanistic link to improved voiding; it only supports the ‘identifiable subgroup’ component of the unit.

### A1-H1-R3 x W-FRD-Q0020-02-c1-Q0020
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness reports an in vivo dosing regimen in "four healthy volunteers" (5×400 mg/day) without any findings about mechanisms linked to voiding or improvement in urinary function/subgroups.
- Pass B: PARTIALLY_COVERS - Provides human exposure regimen ('four healthy volunteers... treated orally... 5×400 mg/day') relevant to attainability, but contains no claim about voiding-relevant physiology or subgroup applicability.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states a dosing regimen in “four healthy volunteers… treated orally with pentoxifylline 5×400 mg/day for 2 days… or… 7 days” and contains no claims about pharmacological/physiological mechanisms relevant to voiding or improvement in a male LUTS/BPH subgroup.

### A1-H1-R3 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Supports a plausible target/process ('inhibits PDE 1–5, with IC50 50–200 μmol/L') but does not link to voiding improvement, a defined subgroup, or establish clinical attainability in the specified cohort.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states a mechanistic pharmacology fact—“pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L”—which is mechanistic evidence but does not by itself support a coherent causal explanation for improved voiding in an identifiable subgroup of men.

### A1-H1-R3 x W-FRD-Q0052-02-c3-Q0052
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Alewijnse2003 (Results > Table III) reports sequential longitudinal multiple linear regression with adherence behavior at 12-month follow-up as dependent variable, analyzed on n=75.
- Source: alewijnse2003.pdf.md Results > Table III (title/caption)
- Pass A: NO_SEMANTIC_RELATION - Talks about a regression on 'adherence behavior at 12-month follow-up' in n=75; does not mention pentoxifylline (PTX), voiding physiology, or causal mechanisms for improved voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes a statistical model—“multiple linear regression with adherence behavior… at 12-month follow-up… n=75”—without mentioning PTX, voiding physiology, mechanisms, or any subgroup of men; it provides no support for the unit’s causal-mechanistic claim.

### A1-H1-R3 x W-FRD-Q0053-02-c4-Q0053
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: NO_SEMANTIC_RELATION - Describes PFME questionnaire timing and generalizability cautions in women; no PTX exposure or mechanistic/physiological link to improved voiding in men.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns PFME questionnaire timing and generalizability in women—“after… at least six weeks… PFME… generalized cautiously to women”—and contains no PTX-related pharmacology/physiology/mechanism or voiding-improvement claim in men/subgroups.

### A1-H1-R3 x W-FRD-Q0063-01-c1-Q0063
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Sullivan-et-al-1988: Human PMNs incubated 30 min at 37°C with pentoxifylline 300 µg/ml decreased adherence to nylon vs diluent: 64.1±2.7% (n=16) vs 54.0±3.9% (n=6; P=0.031) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → PMN adherence).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → PMN adherence (opening paragraph)
- Pass A: PARTIALLY_COVERS - Shows PTX (300 µg/ml) decreases human PMN adherence to nylon; provides a mechanistic anti-inflammatory effect of PTX but does not connect to urinary/voiding function, men with BPH, or an identifiable subgroup.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports an immunomodulatory effect of PTX in human PMNs—“pentoxifylline 300 µg/ml decreased adherence to nylon”—which is mechanistic evidence, but it does not connect this to improved voiding or to a defined subgroup of men with LUTS/BPH.

### A1-H1-R3 x W-FRD-Q0063-01-c4-Q0063
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: PARTIALLY_COVERS - Reports PTX (100 µg/ml) reduced FMLP-stimulated superoxide in human PMNs; this supports a plausible anti-inflammatory mechanism but does not link to voiding-relevant physiology or improvement in the target male cohort/subgroup.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports PTX reduces an inflammatory effector readout in human PMNs—“Pentoxifylline (100 µg/ml) reduced… superoxide”—providing mechanistic evidence but no stated linkage to urinary/voiding outcomes or an identifiable subgroup of men.

### A1-H1-R3 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: PARTIALLY_COVERS - PTX (1 or 100 µg/ml) reduced LPS-MCM–enhanced lysozyme release (PMN degranulation proxy); mechanistic immune modulation is relevant but no evidence of improved voiding or applicability to a defined subgroup of men with BPH/shy bladder.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports PTX modulates PMN degranulation—“Pentoxifylline 1 or 100 µg/ml reduced [lysozyme release]”—a mechanistic immune effect, but it does not state any consequence for voiding improvement or specify applicability to a male LUTS subgroup.

### A1-H1-R3 x W-FRD-Q0064-04-c1-Q0064
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: In male Wistar–Kyoto rats (230–300 g), after baseline haemodynamics, investigators gave saline or pentoxifylline 3 mg/kg i.v., then 30 min later saline or E. coli LPS 10 mg/kg i.v., monitoring for 240 min (wu1999.pdf.md, Methods 2.1 Endotoxic shock).
- Source: wu1999.pdf.md Methods 2.1 Endotoxic shock
- Pass A: NO_SEMANTIC_RELATION - Only states an animal endotoxic shock protocol (male rats, PTX 3 mg/kg i.v. before LPS) without reporting any mechanistic outcome tied to urinary function or improved voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only outlines an animal protocol—“male Wistar–Kyoto rats… pentoxifylline 3 mg/kg i.v… then… LPS 10 mg/kg”—and provides no results or mechanistic/physiological evidence tied to voiding improvement in men or any subgroup.

### A1-H1-R3 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: PARTIALLY_COVERS - Finds PTX up to 50 µmol/L did not alter neutrophil Ca2+ transients (only 500 µmol/L reduced them); this is mechanistic information about PTX and inflammation signaling but does not provide a coherent causal explanation for improved voiding in men.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness provides mechanistic data on PTX and neutrophil signaling—“PTX up to 50 µmol/L changed neither… [Ca2+]i; 500 µmol/L reduced…”—which is mechanistic evidence (including limits) but does not support a coherent causal explanation for improved voiding in an identifiable subgroup of men.

### A1-H1-R3 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Is a speculation that PTX 'may have no potent anti-inflammatory effect once inflammation has been triggered'; it neither supports a coherent causal explanation for improved voiding nor addresses voiding physiology/subgroup applicability.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is speculative and negative about anti-inflammatory potency—“speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered”—and does not provide affirmative pharmacological/physiological/mechanistic support for PTX improving voiding in any male subgroup.

### A1-H1-R3 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: PARTIALLY_COVERS - Same neutrophil Ca2+ result: no change up to 50 µmol/L, effect at 500 µmol/L; contributes mechanistic detail but does not link PTX to improved voiding-relevant function in the specified men/subgroup.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness repeats mechanistic findings in neutrophils—“preincubation with PTX up to 50 µmol/l did not change… [Ca2+]i; 500 µmol/l reduced…”—which contributes mechanistic evidence about PTX action/limits but not a causal explanation of meaningful voiding improvement in an identifiable subgroup of men.

### A1-H1-R3 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: NO_SEMANTIC_RELATION - Describes an open-label systemic-sclerosis trial of PTX+vitamin E (dose/duration) but provides no finding about voiding improvement or a mechanistic chain relevant to male voiding dysfunction.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only describes study design/population/dose (“12 systemic-sclerosis patients… open-label 24-week… pentoxifylline 800 mg/day plus vitamin E”), and makes no claim about “improve voiding,” men, or any mechanistic/physiological rationale linking PTX to voiding outcomes in an identifiable subgroup.

### A1-H1-R3 x W-FRD-Q0131-03-c3-Q0131
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: NO_SEMANTIC_RELATION - States PTX half-life (~1.6 h); pharmacokinetic fact alone does not link PTX to voiding-relevant physiology or improved voiding in an identifiable subgroup.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness states a pharmacokinetic fact (“PTX has short half-life about 1.6 h”) but provides no mechanistic/physiological evidence about voiding, no subgroup, and no causal explanation for improving voiding.

### A1-H1-R3 x W-FRD-Q0156-03-c1-Q0156
- Unit (REQUIRED_SUPPORT): The available pharmacological, physiological, and mechanistic evidence supports a coherent causal explanation for why PTX could meaningfully improve voiding in an identifiable subgroup of these men.
- Witness: Roberts1993.pdf.md (Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend): purified neutrophils preincubated 15 min: 1 µmol/L pentoxifylline did not inhibit FMLP superoxide rate or total; ≥5 µmol/L inhibited both. At 10 µmol/L: Rate FMLP 85% and Total FMLP 75% vs control (p<0.05).
- Source: roberts1993.pdf.md Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend
- Pass A: PARTIALLY_COVERS - Shows PTX at ≥5 µmol/L inhibits neutrophil superoxide production (NADPH oxidase activity), a mechanistic anti-inflammatory effect; does not connect to improved voiding function, clinically attainable exposure in men, or a defined benefiting subgroup.
- Pass B: NO_SEMANTIC_RELATION - Witness is an in-vitro neutrophil finding ('≥5 µmol/L inhibited' FMLP superoxide) with no mention of men with BPH/shy bladder, no voiding-relevant physiology, and no subgroup-specific causal chain to improved voiding.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0019-02-Q0019
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: NO_SEMANTIC_RELATION - Witness only states clinically attainable PTX plasma levels (<5 μmol/L; active forms unlikely >10 μmol/L). It does not specify all four targeted-trial elements (intervention, phenotype, outcome direction/timing, comparator).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states clinically attained PTX plasma levels (“peak plasma PTX levels are <5 μmol/l… combined level… unlikely to exceed 10 μmol/l”) and does not specify a targeted clinical trial package (phenotype, measurement direction/timing, comparator).

### A1-H1-R4 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness reports an in vitro neutrophil assay where 5 μmol/L PTX inhibits FMLP-stimulated oxidative burst. This is not a package specifying a clinical trial’s intervention/phenotype/outcome/comparator for voiding in men.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an ex vivo/in vitro whole-blood neutrophil assay where “5 µmol/l significantly inhibited” FMLP-stimulated oxidative burst; it does not specify the four targeted-trial elements (clinical phenotype, outcome direction/timing in patients, comparator) claimed sufficient by the unit.

### A1-H1-R4 x W-FRD-Q0020-02-c1-Q0020
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness describes an oral dosing regimen in four healthy volunteers (5×400 mg/day for 2 or 7 days). It does not provide phenotype subgroup definition, voiding outcome direction/timing, or discriminating comparator.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides only an oral dosing regimen in “four healthy volunteers… 5×400 mg/day for 2 days… or… 7 days” and does not specify phenotype, measurement direction/timing, or comparator needed to show premises/predictions are sufficient to fully specify a targeted clinical trial.

### A1-H1-R4 x W-FRD-Q0025-03-Q0025
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In delanian2005.pdf.md (RESULTS → Primary Analyses → “After stopping PTX-vitE: Rebound effect.”), after stopping PTX-vitE, RIF surface area showed a significant initial increase (P = .037). The fibrotic increase was significantly lower and asymptomatic in LPE: 8.5%/yr (95% CI, 1–16) vs SPE: 40%/yr (95% CI, 24–56); P = .0012.
- Source: delanian2005.pdf.md RESULTS → Primary Analyses → “After stopping PTX-vitE: Rebound effect.”
- Pass A: NO_SEMANTIC_RELATION - Witness reports rebound increase in radiation-induced fibrosis surface area after stopping PTX-vitE and differences between LPE vs SPE. This is not about designing a targeted PTX trial for voiding/BPH (no required four trial-spec elements in scope).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes a rebound effect in radiation-induced fibrosis after stopping “PTX-vitE” and compares “LPE vs SPE”; it does not assert that supported premises/predictions are sufficient to specify intervention/phenotype/measurement/comparator for a targeted clinical trial as in the unit.

### A1-H1-R4 x W-FRD-Q0029-04-c4-Q0029
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.5.2. Fecal Calprotectin), fecal calprotectin <100 µg/g occurred in 18 patients (66.7%) on PTX vs 14 (53.8%) on placebo; <50 µg/g occurred in 6 (20%) on PTX vs 2 (6%) on placebo. Denominators are not explicitly stated.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.5.2. Fecal Calprotectin
- Pass A: NO_SEMANTIC_RELATION - Witness gives fecal calprotectin proportions on PTX vs placebo in a GI/inflammatory context. It does not specify a urinary-voiding targeted trial with phenotype, functional outcome direction/timing, and comparator for mechanism discrimination.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports fecal calprotectin thresholds achieved “on PTX vs… placebo” in a GI context, but does not provide the unit’s claim that premises/predictions suffice to specify all four trial-specification elements for a targeted clinical trial.

### A1-H1-R4 x W-FRD-Q0029-04-c5-Q0029
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: NO_SEMANTIC_RELATION - Witness describes differential loss to follow-up in placebo vs PTX groups due to severe disease or non-return. This does not contribute to specifying intervention/phenotype/outcome/comparator for the hypothesized targeted voiding trial.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only notes attrition (“lost to follow-up… developed severe disease… shifted to… steroid therapy”); it does not specify or support sufficiency to specify intervention/phenotype/measurement/comparator for a targeted trial.

### A1-H1-R4 x W-FRD-Q0034-03-c4-Q0034
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Saw palmetto 320 mg daily may cause GI upset and headache and “may enhance the anticoagulation effect of warfarin” (fdp03812573_1.pdf.md, TABLE “Benign Prostatic Enlargement Medications”).
- Source: fdp03812573_1.pdf.md TABLE “Benign Prostatic Enlargement Medications” → Natural Products → Saw palmetto row (Daily Doses and Comments columns).
- Pass A: NO_SEMANTIC_RELATION - Witness concerns saw palmetto adverse effects and warfarin interaction, not PTX trial design or the four required trial-specification elements.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: NO_SEMANTIC_RELATION - Witness summarizes CombAT results for BPH combination therapy vs monotherapy. It does not specify a PTX targeted trial package (intervention, phenotype, outcome direction/timing, comparator to distinguish mechanisms).
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - Witness reports no adverse effects observed with PTX in Staubach1998. Safety reporting alone does not specify all four trial-design elements required by the unit.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0048-02-c1-Q0048
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In 10.1016@s0041-13450001266-5.pdf.md (PATIENTS AND METHODS), pentoxifylline was dosed 150 mg IV 2 hours pre-op, 150 mg IV after graft reperfusion, and 300 mg IV 8 hours after grafting; then 1200 mg/day in three oral doses for 7 days.
- Source: 10.1016@s0041-13450001266-5.pdf.md PATIENTS AND METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness provides a PTX dosing schedule (perioperative IV then 1200 mg/day orally for 7 days) in a transplant/grafting setting. It lacks the phenotype subgroup, primary voiding outcome direction/timing, and discriminating comparator needed by the unit.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness states PTX is generally safe/well tolerated with ~3% GI symptoms/dizziness. This does not establish sufficiency of premises/predictions to specify intervention+phenotype+outcome direction/timing+comparator for a targeted trial.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX inhibits PDE 1–5 with IC50 50–200 μmol/L. This mechanistic note does not specify the four trial-specification elements or show that the premises/predictions are sufficient to do so.
- Pass B: PARTIALLY_COVERS - By stating 'pentoxifylline inhibits PDE 1–5' with quantitative 'IC50 values', the witness contributes mechanistic rationale relevant to a comparator/mechanism element, but it does not specify the clinical phenotype subgroup, primary functional outcome with timing/direction, nor an explicit comparator design.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Witness reports an in-vitro PMN degranulation result (PTX reduced lysozyme release). It does not specify any targeted clinical trial design elements (intervention details for men with voiding difficulty, phenotype subgroup, functional outcome direction/timing, or comparator).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in-vitro PMN degranulation result (“Pentoxifylline 1 or 100 µg/ml reduced [lysozyme release]”) with no statement about specifying a targeted clinical trial’s intervention/exposure + phenotype + measurement (direction/timing) + comparator.

### A1-H1-R4 x W-FRD-Q0064-04-c1-Q0064
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In male Wistar–Kyoto rats (230–300 g), after baseline haemodynamics, investigators gave saline or pentoxifylline 3 mg/kg i.v., then 30 min later saline or E. coli LPS 10 mg/kg i.v., monitoring for 240 min (wu1999.pdf.md, Methods 2.1 Endotoxic shock).
- Source: wu1999.pdf.md Methods 2.1 Endotoxic shock
- Pass A: NO_SEMANTIC_RELATION - Witness describes an animal endotoxic shock protocol (rats, IV PTX and LPS, haemodynamic monitoring). It contains no clinical trial-specification package for the scoped men or the required phenotype/outcome/comparator elements.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only describes an animal endotoxic shock dosing/monitoring protocol (“male Wistar–Kyoto rats… pentoxifylline 3 mg/kg i.v.… LPS 10 mg/kg i.v.… monitoring for 240 min”), not a package sufficient to specify all four targeted clinical trial elements.

### A1-H1-R4 x W-FRD-Q0078-02-c1-Q0078
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: desouza2009.pdf.md (Patients and methods > Study design): open-label 24-week-per-patient trial; all treated SSc patients received pentoxiphylline 800 mg/day associated with vitamin E 800 UI/day; results compared with a historical control group. desouza2009.pdf.md (Patients and methods > Historical control group): 9 diffuse SSc patients retrospectively used as controls received cyclophosphamide 0.5–1 g/m^2 during 6 months.
- Source: desouza2009.pdf.md Patients and methods > Study design; Patients and methods > Historical control group
- Pass A: NO_SEMANTIC_RELATION - Witness describes an open-label systemic-sclerosis trial (PTX+vitamin E) with historical controls (cyclophosphamide). It does not provide a defensible targeted trial design for PTX improving voiding in the specified male subgroup, nor the required phenotype/outcome/comparator for that mechanism.
- Pass B: PARTIALLY_COVERS - Witness contributes intervention details (“pentoxiphylline 800 mg/day…”) and a comparator structure (“historical control group… cyclophosphamide”), but not the required voiding-related phenotype/outcome direction/timing, and the comparator is not a discriminating alternative in the hypothesized BPH/shy-bladder setting.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness gives some trial-spec elements (intervention regimen “pentoxiphylline 800 mg/day… 24-week” and comparator structure “historical control group… cyclophosphamide”), but it is in systemic sclerosis and does not specify the target phenotype nor measurement direction/timing for the hypothesized targeted clinical trial.

### A1-H1-R4 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: NO_SEMANTIC_RELATION - Witness states deSouza2009 was an open-label 24-week study of PTX 800 mg/day plus vitamin E in systemic sclerosis patients. It does not specify a targeted clinical trial for voiding in the scoped men, nor the phenotype/outcome/comparator elements.
- Pass B: PARTIALLY_COVERS - Witness supplies an intervention regimen (“pentoxifylline 800 mg/day plus vitamin E… 24-week study”), but not the required BPH/shy-bladder measurable phenotype, primary voiding functional outcome direction/timing, or discriminating comparator.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness provides intervention and timing (“open-label, 24-week… pentoxifylline 800 mg/day plus vitamin E 800 UI/day”) but lacks a specified phenotype, outcome measurement direction/timing, and comparator adequate to meet the unit’s ‘all four trial-specification elements’ requirement.

### A1-H1-R4 x W-FRD-Q0098-01-Q0098
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: NO_SEMANTIC_RELATION - Witness reports a pilot rat hemorrhage/shock pretreatment experiment where IV PTX altered MAP/HR/WBC and animals died. It does not support specifying a targeted clinical trial design for PTX and voiding outcomes in the scoped men.
- Pass B: PARTIALLY_COVERS - Witness includes specific exposure details (“IV PTX 40 mg/kg over 15 min…”) and physiological effects (MAP decrease, HR increase), but it is in “male rats” with shock and death, not a human voiding phenotype/outcome or comparator that discriminates mechanisms in BPH/shy bladder.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness specifies an exposure (“IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage”) and measured physiological changes, but in male rats with hemorrhagic shock (“they all died”) and no clinical-trial phenotype/outcome/comparator; thus it only contributes a fragment of the trial-spec elements.

### A1-H1-R4 x W-FRD-Q0131-03-c3-Q0131
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: NO_SEMANTIC_RELATION - Witness states PTX has a short half-life (~1.6 h). This single PK fact does not amount to an evidence package sufficient to specify all four targeted clinical trial elements (including phenotype, outcome direction/timing, and comparator).
- Pass B: PARTIALLY_COVERS - Witness states only that “PTX has short half-life about 1.6 h,” which can support dosing/timing considerations but does not provide the phenotype, primary outcome direction/timing, or comparator needed by the unit.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness supplies only a PK/timing-relevant fact (“PTX has short half-life about 1.6 h”), which can inform measurement/dosing timing but does not specify phenotype, comparator, or full measurement direction/timing package required by the unit.

### A1-H1-R4 x W-FRD-Q0131-03-c4-Q0131
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: NO_SEMANTIC_RELATION - Witness reports toxicity at 80 mg/kg causing hypotension/flushing/convulsion. Safety/toxicity mention alone does not specify the required trial design elements (phenotype subgroup, outcome direction/timing, comparator) for the scoped clinical question.
- Pass B: PARTIALLY_COVERS - Witness gives an intervention-relevant constraint (“PTX toxicity… at 80 mg/kg, causing hypotension…”), which can inform exposure safety, but it does not specify subgroup phenotype, primary functional outcome direction/timing, or a discriminating comparator.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0138-04-Q0138
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: nihms496647.pdf.md (“Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome”): unpublished extended data using proposed criteria: among 132 patients enrolled and referred for suspected or confirmed disease over four years, 58 met WHO systemic mastocytosis criteria, 7 MMAS, 19 IA; 42 had mast cell activation symptoms without evidence of clonal mast cells; 6 had unrelated diagnoses.
- Source: nihms496647.pdf.md Section: “Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome” (paragraph beginning “Using the approach outlined above…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness addresses “idiopathic mast cell activation syndrome” enrollment/diagnostic categories, not PTX intervention details, voiding phenotype, outcomes, or comparator for the hypothesized trial.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0144-01-c3-Q0144
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: In Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety), mild adverse events occurred in 11 intervention vs 13 control patients; most were mild dyspepsia requiring no treatment. No severe adverse effects (no threatening hypotension or syncope) and no urinary retention episodes; vital signs remained almost stable.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Witness provides a relevant comparator context (“intervention vs control” in a “combination of tamsulosin and Pentoxifylline versus tamsulosin alone”) and safety observations (“No severe adverse effects”), but does not supply the required pre-treatment phenotype definition or primary outcome direction/timing.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0149-04-c4-Q0149
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Raison2013 (raison2013.pdf.md, RESULTS): in subgroup mixed-effects models for repeated measures, standardized effect size difference at 12 weeks was “moderate to large, in opposite directions”: 0.41 favoring infliximab for baseline hs-CRP >5 mg/L, versus −0.82 favoring placebo for baseline hs-CRP ≤5 mg/L.
- Source: raison2013.pdf.md RESULTS (paragraph containing standardized effect sizes); Figure 4
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness concerns “infliximab” and hs-CRP-defined subgroups with effects at “12 weeks,” not a PTX intervention nor voiding outcomes/comparators for the hypothesized trial.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H1-R4 x W-FRD-Q0156-03-c1-Q0156
- Unit (REQUIRED_SUPPORT): The supported premises and discriminating predictions are sufficient to specify all four trial-specification elements—intervention/exposure, phenotype, measurement (direction and timing), and comparator—for a targeted clinical trial.
- Witness: Roberts1993.pdf.md (Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend): purified neutrophils preincubated 15 min: 1 µmol/L pentoxifylline did not inhibit FMLP superoxide rate or total; ≥5 µmol/L inhibited both. At 10 µmol/L: Rate FMLP 85% and Total FMLP 75% vs control (p<0.05).
- Source: roberts1993.pdf.md Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only reports that “≥5 µmol/L [PTX] inhibited” neutrophil superoxide and 1 µmol/L did not, in purified neutrophils after 15 min; it does not specify a BPH/shy-bladder trial phenotype, clinical measurement timing, or comparator arm.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-A1 x W-FRD-Q0003-04-c1-Q0003
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: PARTIALLY_COVERS - Witness only "propose[s]" a mechanism (PDE inhibition/NOS activation → ↑NO/↑cGMP) to "describe" beneficial effects on contractile function after ischemic injury, citing cardiac papillary muscle; it does not show clinically attainable exposure, target engagement in relevant urinary tissues/conditions, or predictive voiding-function improvement.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness says the authors "propose" PTX as a "phosphodiesterase inhibitor and nitric oxide synthase activator" increasing "tissue NO and intracellular cGMP" as mechanisms to "describe PTX’s beneficial effects on contractile function after ischemic injury"; this is a hypothesized mechanistic link but does not, as written, establish an exposure-compatible causal chain that survives objections or supported functional predictions in the unit’s relevant conditions.

### A1-H2-A1 x W-FRD-Q0013-01-c4-Q0013
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: NO_SEMANTIC_RELATION - This concerns diagnostic criteria for pseudodyssynergia using private-setting uroflowmetry to reduce "bashful voiding" artifacts; it makes no claim about PTX exposure/target engagement or functional predictions from PTX.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about diagnosing pseudodyssynergia via "private-setting uroflowmetry" to reduce false positives from "performance anxiety"/"bashful voiding"; it contains no claim about PTX, causal chains, objections, or functional predictions from exposure.

### A1-H2-A1 x W-FRD-Q0019-02-Q0019
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: PARTIALLY_COVERS - Witness states a key objection: in vitro PTX experiments often use concentrations higher than clinically obtained, giving oral peak plasma PTX "<5 μmol/l" and combined active forms "unlikely to exceed 10 μmol/l"; it addresses exposure-compatibility but not a surviving causal chain or voiding-related functional predictions.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states an exposure-compatibility objection: in vitro PTX often uses concentrations "much higher than obtained clinically" and gives oral peak plasma "<5 μmol/l" with combined active forms "unlikely to exceed 10 μmol/l"; this bears on exposure-compatibility but does not itself show the unit’s surviving causal chain or supported functional predictions in relevant conditions.

### A1-H2-A1 x W-FRD-Q0019-03-c3-Q0019
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: PARTIALLY_COVERS - Witness shows an effect at "as low as 5 µmol/l" (clinically plausible per other context) inhibiting neutrophil oxidative burst; this supports possible biologic activity at attainable exposure but does not connect to the specific urinary target/conditions or supported predictions for voiding function.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports an in-blood assay where PTX "as low as 5 µmol/l" significantly inhibited FMLP-stimulated oxidative burst (DCF H2O2 to "76 ± 5%" of control); this supports some biological activity at a stated concentration but does not establish the unit’s overall coherent causal chain with supported functional predictions in the relevant conditions.

### A1-H2-A1 x W-FRD-Q0044-04-c2-Q0044
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - Reporting "No adverse effects" concerns tolerability/safety, not whether an exposure-compatible causal chain survives objections and yields supported functional predictions in voiding-related outcomes.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states tolerability only ("Adverse effects were not reported" / "No adverse effects ... were observed"); it does not address whether a causal chain survives objections or generates supported functional predictions in relevant conditions.

### A1-H2-A1 x W-FRD-Q0050-03-Q0050
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Reporting 'pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L' is mechanistic potency information, not evidence of clinically attainable exposure producing supported voiding-functional predictions under relevant conditions.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-A1 x W-FRD-Q0063-01-c5-Q0063
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness: 'Pentoxifylline 1 or 100 µg/ml reduced' lysozyme release in PMNs in vitro; this does not show clinically attainable exposure producing supported, predictive voiding-related functional improvements in relevant BPH/shy-bladder conditions.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-A1 x W-FRD-Q0079-04-c3-Q0079
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports neutrophil '[Ca2+]i' unchanged 'up to 50 µmol/L' and reduced only at '500 µmol/L'; it does not address urinary/voiding function or demonstrate the unit’s requested supported functional predictions in relevant conditions.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-A1 x W-FRD-Q0089-04-c2-Q0089
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - This is speculative ('speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered') and does not supply the unit’s required affirmative finding of exposure-compatible target engagement plus supported voiding-functional predictions.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-A1 x W-FRD-Q0090-04-c3-Q0090
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about '[Ca2+]i' in 'purified neutrophils' and reports no effect up to 50 µmol/L; it does not provide target engagement + supported predictive voiding-related functional improvement under relevant conditions.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-A1 x W-FRD-Q0098-01-Q0098
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - In 'male rats' given 'IV PTX 40 mg/kg', physiologic changes and death in shock are reported; this does not show a clinically attainable exposure yielding supported voiding-functional improvements in relevant BPH/shy-bladder conditions.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-A1 x W-FRD-Q0131-03-c3-Q0131
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Statement 'PTX has short half-life about 1.6 h' provides pharmacokinetics but not evidence that 'clinically attainable exposure engages the relevant target and produces ... improvements in voiding-related function.'
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-A1 x W-FRD-Q0131-03-c4-Q0131
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports 'PTX toxicity ... at 80 mg/kg' with adverse effects, which does not establish clinically attainable target engagement plus supported voiding-functional predictions under relevant conditions.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only reports that “PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion.” It does not address whether a “coherent, exposure-compatible causal chain survives objections” or whether it “generates supported functional predictions in relevant conditions,” so it provides no material support for the unit.

### A1-H2-A1 x W-FRD-Q0156-03-c1-Q0156
- Unit (ADVERSE_TEST): A coherent, exposure-compatible causal chain survives the proposed objections and generates supported functional predictions in relevant conditions.
- Witness: Roberts1993.pdf.md (Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend): purified neutrophils preincubated 15 min: 1 µmol/L pentoxifylline did not inhibit FMLP superoxide rate or total; ≥5 µmol/L inhibited both. At 10 µmol/L: Rate FMLP 85% and Total FMLP 75% vs control (p<0.05).
- Source: roberts1993.pdf.md Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Witness shows target/biological engagement at exposure levels (≥5 µmol/L inhibited; 10 µmol/L reduced rate/total) in 'purified neutrophils' in vitro, but does not show 'predictive improvements in voiding-related function' or relevant BPH/shy-bladder conditions.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness states that in vitro “purified neutrophils” exposed to pentoxifylline (≥5 µmol/L) showed reduced FMLP-stimulated superoxide (e.g., “At 10 µmol/L… 85%… 75% vs control”). This does not speak to surviving “proposed objections,” nor does it provide or test “supported functional predictions in relevant conditions,” so it is not materially responsive to the unit’s causal-chain/prediction claim.

### A1-H2-C1 x W-FRD-Q0003-04-c1-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: PARTIALLY_COVERS - Witness discusses PTX mechanisms explaining “beneficial effects… after ischemic injury” and explicitly cites “cardiac papillary muscle data,” which is a different tissue/model than the urinary/BPH voiding-dysfunction context required for relevance to testing H1; it highlights a potential model mismatch but does not itself state the relevance requirement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness proposes PTX mechanisms in cardiac papillary muscle/ischemic injury context (“offered as mechanisms… after ischemic injury”) but does not state any methodological constraint that mismatch evidence must be sufficiently relevant to test H1 or that unrelated models/exposures do not suffice.

### A1-H2-C1 x W-FRD-Q0006-04-c1-Q0006
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: NO_SEMANTIC_RELATION - Witness is about an in vitro vascular relaxation experiment design detail (“did not add NO blockers… denuding vascular endothelial cells”) and makes no claim about whether mismatch evidence is sufficiently relevant to test H1 in the BPH/voiding cohort.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only reports an experimental design detail (“did not add NO blockers such as L-NAME… instead… denuding vascular endothelial cells”) and makes no claim about relevance of mismatch evidence for testing H1.

### A1-H2-C1 x W-FRD-Q0009-04-Q0009
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: Chuang2015.pdf.md (EPIDEMIOLOGY) says Thomas et al. reported that, in men with untreated detrusor underactivity and minimum 10-year urodynamic follow-up, detrusor underactivity was not progressive in most nonneurogenic male patients and often did not result in chronic urinary retention.
- Source: chuang2015.pdf.md EPIDEMIOLOGY section (paragraph beginning “Thomas and colleagues9 reported…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports the natural history of detrusor underactivity (“not progressive… often did not result in chronic urinary retention”) and does not address the methodological constraint that H2’s supporting mismatch evidence must be relevant rather than from unrelated models/exposures.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes clinical course of detrusor underactivity (“not progressive… often did not result in chronic urinary retention”) without addressing whether mismatch evidence must be relevant to test H1.

### A1-H2-C1 x W-FRD-Q0010-03-Q0010
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, Figure 2 (“Figure 2. The percentage of referrals made for PFPT by diagnosis”), PFPT referral percentages by diagnosis are: Pelvic Floor Dysfunction 49.5%, CPPS 39.6%, Testicular Pain/Groin Pain 28.4%, LUTS 3.6%; the denominator is not stated.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18, Figure 2 ("Figure 2. The percentage of referrals made for PFPT by diagnosis"), including the table "Diagnosis | Percentage of Patients Referred"
- Pass A: NO_SEMANTIC_RELATION - Witness reports PFPT referral percentages by diagnosis (e.g., “LUTS 3.6%”) and does not speak to whether mismatch evidence used for H2 is drawn from relevant models/exposures to test H1.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C1 x W-FRD-Q0010-04-c1-Q0010
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness describes a retrospective chart review identified by ICD codes; it does not address the constraint that evidence used to support H2 must be relevant to testing H1 (no discussion of model/exposure relevance).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes a retrospective chart review identified via ICD codes and does not discuss whether mismatch evidence must be sufficiently relevant (or that unrelated models/exposures do not suffice) to test H1.

### A1-H2-C1 x W-FRD-Q0013-01-c4-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns diagnostic methodology for pseudodyssynergia and minimizing “performance anxiety or ‘bashful voiding’,” not the relevance/appropriateness of mismatch evidence supporting H2 vis-a-vis H1.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns diagnostic procedures for pseudodyssynergia (“private-setting uroflowmetry… minimize false-positive… ‘bashful voiding’”) rather than any requirement about relevance of mismatch evidence for testing H1.

### A1-H2-C1 x W-FRD-Q0013-03-c4-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness defines bladder outlet obstruction using urodynamic/radiographic criteria; it does not assert anything about the relevance of evidence models/exposures for testing H1.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness defines bladder outlet obstruction using urodynamic/radiographic criteria (“>45 cm water… <12 ml/s… radiographic evidence”) and does not address relevance constraints on mismatch evidence for testing H1.

### A1-H2-C1 x W-FRD-Q0014-02-Q0014
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: NO_SEMANTIC_RELATION - Witness is about using ultrasound DWT and bladder capacity to predict detrusor underactivity (PPV/NPV) and does not address whether mismatch evidence for H2 is sufficiently relevant (model/exposure constraint).
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C1 x W-FRD-Q0018-01-Q0018
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: Bortnick et al. 2020 says surgical therapy is recommended for recurrent UTIs secondary to BPH, renal insufficiency secondary to BPH, recurrent bladder stones or gross hematuria from BOO due to BPH, refractory urinary retention secondary to BPH, and/or LUTS that have failed or unwillingness to consider other therapies (bortnick2020.pdf.md, “Alternative minimally invasive/surgical procedures to TURP”).
- Source: bortnick2020.pdf.md Section: “Alternative minimally invasive/surgical procedures to TURP” (paragraph beginning “Overall, surgical therapy is recommended…”)
- Pass A: NO_SEMANTIC_RELATION - Witness lists when surgical therapy is recommended for BPH complications and does not concern evidentiary relevance/mismatch constraints for testing H1.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C1 x W-FRD-Q0034-01-bortnick20-c3-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: bortnick2019.pdf.md (Review of Medications > Alpha Blockers) reports Duan et al. used 2006–2012 Medicare data in a cohort of 253,136 men >65 with BPH; dementia (ICD-9 codes) risk after mean 19.8 months was significantly higher with tamsulosin versus no BPH meds and versus doxazosin, terazosin, alfuzosin, dutasteride, or finasteride.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about “dementia… risk… higher with tamsulosin,” which is unrelated to PTX mechanism/translation or evidentiary relevance of mismatch models/exposures for H1 testing.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an association between tamsulosin and dementia risk in an older BPH cohort (“dementia… significantly higher with tamsulosin”) and does not state anything about whether mismatch evidence must be relevant to test H1.

### A1-H2-C1 x W-FRD-Q0034-04-bortnick20-c1-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: bortnick2020.pdf.md (“Medical therapy”→“Combination therapy” MTOPS paragraph) reports MTOPS studied finasteride+doxazosin in 3000 men (mean age 62.6 years, SD 7.3) and found combination therapy improved voiding symptoms and maximum urinary flow rate more than either alone, prevented BPH progression better, and reduced the long-term risk of acute urinary retention and need for invasive therapy.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (MTOPS paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports MTOPS combination therapy “improved voiding symptoms… prevented BPH progression,” but makes no claim about PTX evidence relevance/mismatch or about testing the PTX rationale for the cohort.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness summarizes MTOPS outcomes for finasteride+doxazosin (“improved voiding symptoms… prevented BPH progression”) but does not mention any requirement that mismatch evidence be sufficiently relevant to test H1.

### A1-H2-C1 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses that “combination therapy had greater risk reduction… than either monotherapy” in CombAT; it does not address PTX nor whether a given model/exposure is relevant enough to test H1.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness summarizes CombAT outcomes (“greater risk reduction… than either monotherapy”) without addressing the unit’s methodological constraint about relevance of mismatch evidence for testing H1.

### A1-H2-C1 x W-FRD-Q0036-02-c3-Q0036
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: Stokes2022.pdf.md (STUDY DESIGN, MATERIALS AND METHODS) reports analyses used the 1st diaries returned (at the 2nd appointment), so only a subset contributed data: women who attended first follow-up, returned a completed diary, and had available prescription data.
- Source: stokes2022.pdf.md STUDY DESIGN, MATERIALS AND METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about analyses using only “women who attended first follow-up… returned a completed diary… had available prescription data,” which is about sample inclusion/attrition, not about whether mismatch evidence is relevant to testing PTX in the specified male BPH/voiding cohort.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes analysis inclusion/attrition criteria (“used the 1st diaries returned… only a subset contributed data”), but says nothing about whether mismatch evidence is sufficiently relevant to test H1 or that unrelated models/exposures do not suffice.

### A1-H2-C1 x W-FRD-Q0043-03-Q0043
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: ladi-seyedian2017.pdf.md (7.4. Electrical stimulation) says sacral neuromodulation (SNM) could be an effective option for non-obstructive urinary retention; it reports Lombardi et al. assessed SNM for neurogenic non-obstructive urinary retention in patients with incomplete spinal cord lesions and found 42.4% (36/85) improved during the percutaneous first stage of SNM.
- Source: ladi-seyedian2017.pdf.md Section 7.4. Electrical stimulation
- Pass A: PARTIALLY_COVERS - Witness concerns sacral neuromodulation effectiveness in neurogenic non-obstructive urinary retention with incomplete spinal cord lesions, which is a urinary-voiding model but not the cohort context (men with BPH/shy bladder, PTX rationale). It supports the idea that model relevance matters (different disease mechanism), but does not itself state the contextual constraint about relevance for testing H1.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness claims SNM “could be an effective option” for neurogenic non-obstructive urinary retention and reports an improvement rate in spinal cord lesion patients, but it does not state the methodological constraint that mismatch evidence must be relevant to testing H1 or that unrelated models/exposures are insufficient.

### A1-H2-C1 x W-FRD-Q0050-02-Q0050
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness is about PTX safety/tolerability in general (GI symptoms, dizziness) and does not address whether mismatch evidence is relevant (model/tissue/exposure) to testing H1 in the specified urinary-voiding cohort.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness addresses pentoxifylline safety/tolerability (“very safe”, “usually well tolerated”, common GI symptoms/dizziness) rather than any claim about relevance of mismatch evidence/models/exposures for testing H1.

### A1-H2-C1 x W-FRD-Q0050-03-Q0050
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX inhibits PDE 1–5 with IC50 50–200 μmol/L (mechanism potency), but does not discuss evidentiary relevance/mismatch of models or exposures for testing H1 in this cohort.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a mechanistic potency detail (PTX inhibits “PDE 1–5” with “IC50 50–200 μmol/L”) without any statement about whether evidence is sufficiently relevant to test H1 or about excluding unrelated models/exposures.

### A1-H2-C1 x W-FRD-Q0069-02-c3-Q0069
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: refsum1994.pdf.md (RESULTS) reports ANOVA differences between study groups for intracellular sodium (P<.001), intracellular potassium (P<.05), and intracellular chloride (P<.001), but not intracellular water; the Bonferroni test compared the means of the groups receiving PTF to those of the CLP group at each time point.
- Source: refsum1994.pdf.md RESULTS
- Pass A: NO_SEMANTIC_RELATION - Witness reports intracellular electrolyte differences between study groups receiving PTF vs CLP; it provides no statement about relevance of evidence to testing H1, nor ties to urinary function or the cohort conditions.
- Pass B: PARTIALLY_COVERS - Witness concerns an exposure/group comparison involving "PTF" and intracellular ions, which could represent mechanistic evidence potentially disconnected from urinary outcomes; but it does not state the urinary cohort/disease context nor explicitly address whether such evidence is sufficiently relevant to test H1.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports intracellular electrolyte differences between study groups (“ANOVA differences… sodium/potassium/chloride”) and comparisons of “PTF” vs “CLP”, but contains no assertion about evidentiary relevance for testing H1 or that unrelated models/exposures do not suffice.

### A1-H2-C1 x W-FRD-Q0105-04-c4-Q0105
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: In shah2016.pdf.md (RESULTS: Regression Analysis), after controlling for age, gender, and BMI, visceral, subcutaneous, and total adipose mass did not predict plasma IL-6 or IL-1β in Crohn’s disease patients at v1 or v2; likewise hepatic fat fraction and inter-muscular fat did not predict IL-6 or IL-1β at v1 or v2.
- Source: shah2016.pdf.md RESULTS: Regression Analysis
- Pass A: NO_SEMANTIC_RELATION - Witness reports null associations between adipose measures and cytokines in Crohn’s disease patients; it does not discuss the relevance constraint for mismatch evidence to test H1 in the urinary-voiding cohort.
- Pass B: PARTIALLY_COVERS - Witness provides a biomarker non-association ("adipose mass did not predict plasma IL-6 or IL-1β")—a type of mismatch between marker and clinical context—but it is in "Crohn’s disease" and does not connect to PTX exposure, urinary function, or BPH/shy bladder cohort relevance, so it only partially speaks to the unit’s relevance requirement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports null regression results in Crohn’s disease patients (“adipose mass did not predict plasma IL-6 or IL-1β”), which is not a statement about a relevance requirement for mismatch evidence to test H1, nor about unrelated models/exposures being inadequate.

### A1-H2-C1 x W-FRD-Q0148-01-c1-Q0148
- Unit (CONTEXTUAL_CONSTRAINT): The mismatch evidence must be sufficiently relevant to test H1; unrelated models or exposures do not suffice.
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports long-term follow-up showing no significant LUTS or voiding-parameter improvement after TURP versus preoperative; it is an outcome claim, not a statement about the evidentiary relevance constraint for testing H1.
- Pass B: PARTIALLY_COVERS - Witness is in a urologic context ("TURP", "LUTS", "Qmax", "PVR", "BCI") and thus closer to the unit’s disease/organ domain, but it does not speak to PTX or to whether specific mismatch evidence is "sufficiently relevant to test H1" versus being unrelated.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports long-term TURP outcomes (“no significant LUTS improvement… no significant change in Qmax, PVR… BCI”), but does not articulate the contextual constraint that mismatch evidence must be sufficiently relevant to test H1 or that unrelated models/exposures are insufficient.

### A1-H2-C2 x W-FRD-Q0003-04-c1-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses proposed PTX mechanisms (PDE inhibition/NOS activation increasing NO/cGMP) to explain beneficial effects in ischemic injury (cardiac papillary muscle data), but does not address whether any mismatch defeats the central, materially supported therapeutic rationale versus only a subsidiary route.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness proposes PTX mechanisms ("phosphodiesterase inhibitor and nitric oxide synthase activator" increasing "NO" and "cGMP") to explain benefits after ischemic injury, but it does not address the unit’s scoping claim about refuting only the "materially supported rationale" rather than "every imaginable route."

### A1-H2-C2 x W-FRD-Q0003-04-c3-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX improved detrusor contractions to electrical stimulation but not carbachol responses and speculates on non-cholinergic pathways; it does not claim that a mismatch defeats the central therapeutic rationale (as opposed to a single mechanistic route).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports PTX improved detrusor contractions to electrical stimulation but not to carbachol and speculates about "purinergic or other non-cholinergic" pathways; it does not discuss whether criticism/refutation should target the central, materially supported rationale vs other routes.

### A1-H2-C2 x W-FRD-Q0005-04-c2-Q0005
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: In han1990.pdf.md (Materials and Methods—CAT Assay), the authors state that the CAT assay “was performed according to the thin-layer chromatography method of Gorman et al. (9).”
- Source: han1990.pdf.md Materials and Methods — CAT Assay
- Pass A: NO_SEMANTIC_RELATION - Witness only states the CAT assay method followed Gorman et al.; no content about defeating a therapeutic rationale or about central vs speculative routes.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only states the CAT assay "was performed according to" Gorman et al.’s TLC method, with no content about scoping a refutation to the "materially supported rationale" vs "every imaginable route."

### A1-H2-C2 x W-FRD-Q0006-04-c1-Q0006
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: NO_SEMANTIC_RELATION - Witness says NO blockers (e.g., L-NAME) were not used to test NO-dependence of PTX-induced vascular relaxation; this is a methodological limitation, not a claim that a mismatch defeats the central, materially supported rationale.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness says they did not use NO blockers ("such as L-NAME") to test NO-dependence and instead tested endothelium dependence by "denuding" endothelium; it is methodological and does not address the unit’s constraint about what H2 is scoped to defeat.

### A1-H2-C2 x W-FRD-Q0007-03-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports in men with DU+BPH that urothelial ATP decreased while nitric oxide showed no significant change; this does not state that such a mismatch defeats the central, materially supported therapeutic rationale rather than a particular mechanistic route.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports findings in men with DU+BPH (urothelial ATP decreased; NO "no significant change"), which is about biomarkers and does not speak to whether H2 targets defeating the "materially supported rationale" rather than all possible routes.

### A1-H2-C2 x W-FRD-Q0010-04-c1-Q0010
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports study design ('retrospective chart review' and ICD codes for BPH/OAB/LUTS/etc.); it contains no claim about defeating a therapeutic rationale or distinguishing central vs speculative routes.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C2 x W-FRD-Q0013-01-c4-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about how 'diagnosing pseudodyssynergia also required' a specific test setup to minimize 'performance anxiety' artifacts; it does not speak to PTX rationale or whether refutation targets a central/necessary link.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C2 x W-FRD-Q0013-03-c3-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: Kaplan1997 (kaplan1997.pdf.md, MATERIALS AND METHODS [definitions paragraph]) defined detrusor instability as a nonvolitional, phasic detrusor-pressure increase of at least 15 cm water, or a detrusor-pressure increase associated with increased sensation of urgency.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only 'defined detrusor instability' with pressure/urgency criteria; it does not address whether any mismatch defeats a 'central, materially supported therapeutic rationale' versus 'one route among many.'
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C2 x W-FRD-Q0013-03-c4-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness only defines bladder outlet obstruction criteria (“sustained detrusor contraction >45 cm water… flow rate <12 ml/s… radiographic evidence”), not whether any mismatch defeats the central, materially supported therapeutic rationale.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C2 x W-FRD-Q0013-03-c6-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), patients were considered to have an acontractile detrusor if they had no detrusor contraction during pressure-flow analysis and were unable to generate an uncatheterized urine flow (in private).
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness provides a definition of acontractile detrusor (“no detrusor contraction… unable to generate… urine flow”), but does not address whether a mismatch defeats the key therapeutic rationale versus merely one possible route.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C2 x W-FRD-Q0014-02-Q0014
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns noninvasive detection of detrusor underactivity using ultrasound DWT and bladder capacity (predictive values), not the hypothesis-scoping claim about refuting the central therapeutic rationale for PTX.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C2 x W-FRD-Q0015-04-c2-Q0015
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: Osman2018 (osman2018.pdf.md, “Diagnostic aspects > Detrusor contraction strength > 2. Projected isovolumetric pressure (PIP)”) provides a PIP calculation formula (K varies by population/sex; usually 5 in men) and suggested contractility groupings: >150 strong, 100–150 normal, 50–100 weak, <50 very weak; these formulae may overestimate PIP and have less test–retest reliability than direct isovolumetric measurement.
- Source: osman2018.pdf.md ## Diagnostic aspects > ### Detrusor contraction strength > #### 2. Projected isovolumetric pressure (PIP)
- Pass A: NO_SEMANTIC_RELATION - Witness gives a PIP formula and contractility groupings and notes reliability issues; it does not state anything about PTX rationale being defeated or about focusing on the materially supported rationale rather than “every imaginable route.”
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-C2 x W-FRD-Q0018-01-Q0018
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: Bortnick et al. 2020 says surgical therapy is recommended for recurrent UTIs secondary to BPH, renal insufficiency secondary to BPH, recurrent bladder stones or gross hematuria from BOO due to BPH, refractory urinary retention secondary to BPH, and/or LUTS that have failed or unwillingness to consider other therapies (bortnick2020.pdf.md, “Alternative minimally invasive/surgical procedures to TURP”).
- Source: bortnick2020.pdf.md Section: “Alternative minimally invasive/surgical procedures to TURP” (paragraph beginning “Overall, surgical therapy is recommended…”)
- Pass A: NO_SEMANTIC_RELATION - Witness lists when surgical therapy is recommended for BPH/BOO complications; it does not speak to whether a mismatch defeats the central rationale for PTX or the scoping constraint in the unit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only reports that “surgical therapy is recommended” for specific BPH/BOO-related indications (recurrent UTIs, renal insufficiency, stones, hematuria, refractory retention, failed LUTS therapies). It does not address how H2 is scoped (i.e., “defeating the materially supported rationale as it stands” vs “every imaginable route”).

### A1-H2-C2 x W-FRD-Q0018-03-Q0018
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: Bortnick2020.pdf.md reports AUA guidelines recommend alpha-blocker plus 5-ARI combination therapy for men with moderate-severe LUTS, advanced age, and prostate size >40 g (bortnick2020.pdf.md, “Medical therapy > Combination therapy”).
- Source: bortnick2020.pdf.md Medical therapy > Combination therapy
- Pass A: NO_SEMANTIC_RELATION - Witness reports AUA guideline recommendation for alpha-blocker + 5-ARI combination therapy in certain men; it is unrelated to whether H2’s mismatch targets the materially supported PTX rationale rather than a speculative route.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports AUA guidelines “recommend alpha-blocker plus 5-ARI combination therapy” for certain men with LUTS and prostate size >40 g. This is a treatment recommendation and does not speak to the contextual scoping constraint that H2 targets only the materially supported rationale rather than all possible routes.

### A1-H2-C2 x W-FRD-Q0019-02-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): H2 is scoped to defeating the materially supported rationale as it stands, not every imaginable route.
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: NO_SEMANTIC_RELATION - Witness states in vitro PTX concentrations are often higher than clinically achievable (“peak plasma <5 µmol/l… unlikely to exceed 10 µmol/l”), which is about exposure levels, not about whether H2’s refutation is aimed at the central, materially supported rationale vs only a non-material subsidiary route.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness states clinical exposure limits (“peak plasma PTX levels are <5 μmol/l… combined level… unlikely to exceed 10 μmol/l”) and that in vitro studies often use higher concentrations. This concerns pharmacokinetic plausibility, not whether H2’s rebuttal is scoped to the “materially supported rationale as it stands” rather than “every imaginable route.”

### A1-H2-E1 x W-FRD-Q0007-01-c1-Q0007
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness only provides the ICS definition of detrusor underactivity (“contraction of reduced strength...”), not an experiment showing affirmative failure of exposure/target engagement/functional translation/timing.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only quotes the ICS definition of detrusor underactivity (“a contraction of reduced strength and/or duration...”), and reports no experiment or affirmative failure of a necessary mechanistic link (e.g., insufficient exposure, absent target engagement, incompatible timing, or dysfunction despite modulation).

### A1-H2-E1 x W-FRD-Q0007-04-c4-Q0007
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: NO_SEMANTIC_RELATION - Witness states a general need for markers to avoid a “point of no return” and mentions possible irreversible failure, but reports no relevant experiment demonstrating a necessary-link failure (exposure/engagement/translation/timing).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states a general concern about needing markers to avoid surpassing a “point of no return” with “irreversible bladder decompensation and failure,” but does not describe relevant experiments demonstrating any affirmative failure of exposure/engagement/translation/timing.

### A1-H2-E1 x W-FRD-Q0009-04-Q0009
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Chuang2015.pdf.md (EPIDEMIOLOGY) says Thomas et al. reported that, in men with untreated detrusor underactivity and minimum 10-year urodynamic follow-up, detrusor underactivity was not progressive in most nonneurogenic male patients and often did not result in chronic urinary retention.
- Source: chuang2015.pdf.md EPIDEMIOLOGY section (paragraph beginning “Thomas and colleagues9 reported…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports a natural-history observation that DU “was not progressive” and often did not cause chronic retention; it does not test PTX or demonstrate an affirmative failure of a necessary mechanistic link.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a natural-history observation (“not progressive in most... and often did not result in chronic urinary retention”) and does not test an intervention or demonstrate an affirmative failure of a necessary mechanistic link (exposure, target engagement, timing, or persistence despite modulation).

### A1-H2-E1 x W-FRD-Q0010-03-Q0010
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, Figure 2 (“Figure 2. The percentage of referrals made for PFPT by diagnosis”), PFPT referral percentages by diagnosis are: Pelvic Floor Dysfunction 49.5%, CPPS 39.6%, Testicular Pain/Groin Pain 28.4%, LUTS 3.6%; the denominator is not stated.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18, Figure 2 ("Figure 2. The percentage of referrals made for PFPT by diagnosis"), including the table "Diagnosis | Percentage of Patients Referred"
- Pass A: NO_SEMANTIC_RELATION - Witness is about PFPT referral percentages by diagnosis (e.g., LUTS 3.6%) and does not report an experiment about PTX exposure, target engagement, timing, or dysfunction persistence despite modulation.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness gives PFPT referral percentages by diagnosis (e.g., “LUTS 3.6%”) and contains no experimental evidence about insufficient exposure, absent target engagement, incompatible timing, or persistent dysfunction despite modulation.

### A1-H2-E1 x W-FRD-Q0010-04-c1-Q0010
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness describes a retrospective chart review cohort identification via ICD codes; no experimental result is presented showing any necessary-link failure relevant to PTX’s rationale.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes study design/cohort identification (“retrospective chart review... identified using ICD codes...”) but provides no results demonstrating an affirmative failure of any necessary link (exposure/engagement/translation/timing).

### A1-H2-E1 x W-FRD-Q0013-01-c4-Q0013
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns diagnostic methodology for pseudodyssynergia (private-setting uroflowmetry to reduce anxiety effects), not an experiment demonstrating insufficient exposure, absent engagement, incompatible timing, or persistent dysfunction despite modulation.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns diagnostic methodology for pseudodyssynergia (private-setting uroflowmetry to reduce “performance anxiety”/“bashful voiding”) and does not report an experiment showing insufficient exposure, absent engagement, incompatible timing, or dysfunction persistence despite modulation.

### A1-H2-E1 x W-FRD-Q0050-03-Q0050
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Witness provides target engagement requirements (“inhibits PDE 1–5, with IC50 values 50–200 μmol/L”) but does not itself show a failure (e.g., that achievable exposure is below this) or demonstrate persistent dysfunction despite modulation; it is only one component of a potential necessary-link failure.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states a pharmacologic property (“pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L”) but does not provide experimental evidence of a failure condition (e.g., insufficient achievable exposure vs IC50, absent engagement in vivo, or persistent dysfunction despite modulation).

### A1-H2-E1 x W-FRD-Q0072-04-c1-Q0072
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (METHODS > Subjects) reports that, during a two-year period after unilateral adrenalectomy in 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, symptomatic thyroid dysfunction developed in 3 of 24 patients.
- Source: Takasu1990_Cushings_Syndrome_Due.md METHODS > Subjects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports thyroid dysfunction after adrenalectomy (“symptomatic thyroid dysfunction developed in 3 of 24”), not PTX or voiding-function translation failure.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports post-adrenalectomy thyroid dysfunction incidence in Cushing’s patients (“developed in 3 of 24”) and does not address experiments about a necessary-link failure for the hypothesis (exposure/engagement/translation/timing).

### A1-H2-E1 x W-FRD-Q0072-04-c2-Q0072
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (DISCUSSION) reports that among 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, 5 patients (including the 3 who later developed thyroid dysfunction) had increased antimicrosomal-antibody titers: 5/24 (21%), described as high versus 8.5% in normal women in Japan.
- Source: Takasu1990_Cushings_Syndrome_Due.md DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about thyroid autoantibodies in Cushing’s syndrome (“increased antimicrosomal-antibody titers”), unrelated to PTX exposure/engagement or urinary function translation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports antimicrosomal-antibody titers in Cushing’s patients (“5/24 (21%)”) and provides no experimental evidence about insufficient exposure, absent target engagement, incompatible timing, or persistent dysfunction despite modulation relevant to the unit.

### A1-H2-E1 x W-FRD-Q0098-01-Q0098
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - This is an experiment with PTX exposure producing marked systemic effects and death (“IV PTX 40 mg/kg… decreased MAP… then ‘they all died’”), which can evidence problematic timing/toxicity/mismatch, but it is in hemorrhagic shock rats and not a voiding-dysfunction setting tied to the unit’s necessary-link failures for urinary function translation.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-E1 x W-FRD-Q0107-02-c4-Q0107
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Chung2014.pdf.md (Conclusions): Chung (2014) says post-void residual measurement may indicate underlying detrusor failure if BOO is excluded, but at present urodynamic study should be conducted to consolidate the diagnosis of UAB by functionally demonstrating the presence of DU.
- Source: chung2014.pdf.md Conclusions
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses diagnosis (“urodynamic study should be conducted… demonstrating… DU”), not PTX exposure/engagement or translation failure.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns diagnostic recommendations (“urodynamic study should be conducted... demonstrating... DU”) and does not report experiments demonstrating affirmative failure of exposure, target engagement, functional translation, or timing.

### A1-H2-E1 x W-FRD-Q0148-01-c1-Q0148
- Unit (CORROBORATING_EXPECTATION): Relevant experiments demonstrate insufficient exposure, absent target engagement, persistent dysfunction despite target modulation, incompatible timing, or another affirmative failure of a necessary link.
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about TURP outcomes after 10+ years (“no significant LUTS improvement… no significant change… including BCI”), not an experiment about PTX exposure/target engagement or failure of PTX’s rationale.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports long-term clinical outcomes showing lack of improvement (“no significant LUTS improvement... no significant change... in Qmax, PVR... including BCI”) after TURP, which is an affirmative instance of persistent dysfunction despite a major intervention; but it is not target modulation of the hypothesis’ mechanism and not an exposure/engagement test, so it only partially matches the unit’s failure-of-necessary-link concept.

### A1-H2-R1 x W-FRD-Q0010-04-c1-Q0010
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness describes study methods and ICD-code identification, not any PTX exposure limits or a failure of PTX biological effects to translate into voiding improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only describes a retrospective chart review cohort identified by ICD codes (BPH, OAB, LUTS, etc.) and contains no statement about PTX exposure levels, mismatch, or failure of PTX biological effects to translate into a remedy for impaired voiding.

### A1-H2-R1 x W-FRD-Q0013-03-c4-Q0013
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only defines BOO (“sustained detrusor contraction >45 cm… flow rate <12 ml/s… evidence of prostatic obstruction”) and contains no PTX exposure/tissue-translation claim.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0014-02-Q0014
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about diagnostic prediction (“DWT ≤1.23 mm plus… capacity >445 ml… predict DU”) and does not discuss PTX exposure or failure of PTX effects to translate due to exposure mismatch.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0018-01-Q0018
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Bortnick et al. 2020 says surgical therapy is recommended for recurrent UTIs secondary to BPH, renal insufficiency secondary to BPH, recurrent bladder stones or gross hematuria from BOO due to BPH, refractory urinary retention secondary to BPH, and/or LUTS that have failed or unwillingness to consider other therapies (bortnick2020.pdf.md, “Alternative minimally invasive/surgical procedures to TURP”).
- Source: bortnick2020.pdf.md Section: “Alternative minimally invasive/surgical procedures to TURP” (paragraph beginning “Overall, surgical therapy is recommended…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness lists when “surgical therapy is recommended… secondary to BPH” and makes no claims about PTX exposure/penetration or undermining PTX’s mechanism-based rationale.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0019-02-Q0019
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness provides exposure-limitation evidence (“peak plasma PTX levels are <5 μmol/l… combined… unlikely to exceed 10 μmol/l”) but does not state that urinary/pelvic tissue fails to reach needed concentrations/duration, nor that this defeats the supported rationale for impaired voiding in the specified cohort.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is an in vitro neutrophil finding (“PTX… 5 µmol/l significantly inhibited… hydrogen peroxide production”), with no statement about urinary/pelvic tissue exposure or an exposure mismatch defeating PTX’s voiding-related rationale.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports epidemiology (“79% had detrusor underactivity”) and does not address PTX dosing, clinically attainable concentrations, pelvic/urinary tissue exposure, or translation failure due to exposure mismatch.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0042-03-c2-Q0042
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about a side effect (epigastric pain) and treatment with “omeprazole 40 mg per day,” not PTX exposure/tissue concentrations or voiding dysfunction mechanisms.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0043-03-Q0043
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: ladi-seyedian2017.pdf.md (7.4. Electrical stimulation) says sacral neuromodulation (SNM) could be an effective option for non-obstructive urinary retention; it reports Lombardi et al. assessed SNM for neurogenic non-obstructive urinary retention in patients with incomplete spinal cord lesions and found 42.4% (36/85) improved during the percutaneous first stage of SNM.
- Source: ladi-seyedian2017.pdf.md Section 7.4. Electrical stimulation
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness discusses sacral neuromodulation outcomes (“42.4% improved… SNM…”) and contains no claim about PTX exposure levels, tissue penetration, or undermining PTX’s rationale.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - Witness only states that no adverse effects of pentoxifylline were reported/observed; it makes no claim about tissue exposure, concentration/duration adequacy, or exposure mismatch undermining urinary-voiding rationale.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness characterizes PTX as “very safe” and “usually well tolerated” with common side effects; it does not address whether clinically attainable exposure reaches relevant urinary/pelvic tissues or defeats the proposed mechanism.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0061-02-c5-Q0061
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: In siu2003.pdf.md (Abstract (Results)), the authors report the pelvic muscle training program “appears to be able to reduce the overall urinary incontinence episodes by 85.2%.”
- Source: siu2003.pdf.md Abstract (Results)
- Pass A: NO_SEMANTIC_RELATION - Witness reports pelvic muscle training reduced urinary incontinence episodes; it does not mention PTX exposure, PK/PD mismatch, urinary/pelvic tissue concentrations, or undermining PTX’s rationale for impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R1 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Witness reports in-vitro PMN lysozyme release modulation and PTX effects at 1 or 100 µg/ml; it does not connect to clinically attainable tissue exposure in urinary/pelvic tissues nor claim an exposure mismatch defeating urinary-voiding rationale.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only reports an in-vitro PMN degranulation result (“Pentoxifylline 1 or 100 µg/ml reduced [lysozyme release]”) without any statement about an exposure mismatch, clinically attainable exposure, urinary/pelvic tissue concentrations, or impaired-voiding cohort rationale.

### A1-H2-R1 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: PARTIALLY_COVERS - Witness shows PTX had no effect on neutrophil Ca2+ responses up to 50 µmol/L and only at 500 µmol/L reduced responses; this suggests required concentrations may be high for one cellular effect, but it does not state clinically attainable urinary/pelvic tissue exposure is insufficient or that this undermines the cohort’s voiding-dysfunction rationale.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports lack of effect “PTX up to 50 µmol/L changed neither” neutrophil Ca2+ and effect only at “500 µmol/L,” which is relevant to required concentration for a cellular effect, but it does not state any mismatch between achievable exposure and needed exposure in the impaired-voiding cohort or that this defeats the rationale.

### A1-H2-R1 x W-FRD-Q0085-01-c3-Q0085
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety): During the study, no severe adverse effects were reported, including no threatening hypotension or syncope; vital signs remained almost stable; no urinary retention occurred; and therapy did not stop for TEAEs (not explicitly phrased as zero TEAE dropouts).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: NO_SEMANTIC_RELATION - Witness reports safety observations (no severe adverse effects, stable vitals, no urinary retention) during a study; it does not address inadequate exposure in target tissues or exposure mismatch defeating PTX’s proposed biological remedy.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about safety (“no severe adverse effects… vital signs remained almost stable… no urinary retention occurred”) and does not discuss exposure levels, exposure mismatch, or PTX biological effects failing as a remedy for the cohort’s voiding dysfunction.

### A1-H2-R1 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: PARTIALLY_COVERS - Witness speculates PTX “may have no potent anti-inflammatory effect once inflammation has been triggered” and “may be too weak” for an ongoing cascade, which speaks to insufficient potency/effect; however it is not an exposure/tissue concentration finding and does not establish clinically attainable exposure failure in urinary/pelvic tissues for this cohort.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness speculates PTX “may have no potent anti-inflammatory effect once inflammation has been triggered” and “may be too weak,” which partially aligns with ineffectiveness, but it does not provide affirmative evidence of an exposure mismatch (insufficient achievable exposure vs required exposure) or tie it to impaired voiding in the cohort.

### A1-H2-R1 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: PARTIALLY_COVERS - Witness reports neutrophil Ca2+ transients unchanged up to 50 µmol/L and only changed at 500 µmol/L; this implies effects may require high concentrations, but it does not state that clinically attainable PTX exposure in relevant urinary/pelvic tissues is inadequate or that it defeats the voiding-rationale in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports neutrophil Ca2+ effects only at high concentration (“up to 50 µmol/l did not change…; 500 µmol/l reduced”), relevant to potency/concentration, but it does not state that PTX exposure in urinary/pelvic tissues is mismatched/insufficient in the impaired-voiding cohort or that this defeats the rationale.

### A1-H2-R1 x W-FRD-Q0092-03-c4-Q0092
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: NO_SEMANTIC_RELATION - Witness reports side effects/completion in 12 patients (epigastric pain in 2) over 24 weeks; it provides tolerability information, not evidence of target-tissue underexposure or exposure mismatch undermining urinary effects.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports tolerability/completion (“all 12 patients completed… 2 patients reported epigastric pain”) without addressing exposure mismatch, PTX biological-effect exposure requirements, or impaired voiding mechanism/rationale.

### A1-H2-R1 x W-FRD-Q0104-03-c6-Q0104
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns infliximab vs placebo effects on hs-CRP; it is not about pentoxifylline exposure, urinary/pelvic tissue concentrations, or rationale for impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about infliximab vs placebo effects on hs-CRP (“significant treatment effect… no time effect”) and contains no claim about pentoxifylline exposure, exposure mismatch, or impaired voiding cohort rationale.

### A1-H2-R1 x W-FRD-Q0131-03-c3-Q0131
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: PARTIALLY_COVERS - Witness states PTX has a “short half-life about 1.6 h,” which is relevant to duration of exposure; but it does not claim that clinically attainable exposure fails to reach/maintain needed concentrations in urinary/pelvic tissues or that this defeats the supported mechanism in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states a pharmacokinetic property (“PTX has short half-life about 1.6 h”), which is relevant to exposure duration, but it does not assert a consequential exposure mismatch preventing PTX biological effects from being a meaningful remedy for impaired voiding in the cohort.

### A1-H2-R1 x W-FRD-Q0131-03-c4-Q0131
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: NO_SEMANTIC_RELATION - Witness reports toxicity at 80 mg/kg (hypotension, flushing, convulsion); it does not address clinically attainable therapeutic exposure failing in urinary/pelvic tissue or an exposure mismatch undermining PTX’s rationale for voiding dysfunction.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports toxicity at a dose (“PTX toxicity… at 80 mg/kg, causing hypotension… convulsion”) and does not state that therapeutic/clinically attainable exposure is mismatched to required exposure for biological effects relevant to impaired voiding.

### A1-H2-R1 x W-FRD-Q0156-03-c1-Q0156
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in exposure that prevents PTX’s reported biological effects from becoming a meaningful remedy for the dysfunction driving impaired voiding in this cohort, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend): purified neutrophils preincubated 15 min: 1 µmol/L pentoxifylline did not inhibit FMLP superoxide rate or total; ≥5 µmol/L inhibited both. At 10 µmol/L: Rate FMLP 85% and Total FMLP 75% vs control (p<0.05).
- Source: roberts1993.pdf.md Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend
- Pass A: PARTIALLY_COVERS - Witness reports neutrophil superoxide inhibition requires ≥5 µmol/L (no inhibition at 1 µmol/L); this bears on concentration needed for a cellular effect, but it does not establish that clinically attainable PTX (or metabolite) exposure in urinary/pelvic tissues is insufficient nor that such insufficiency defeats the supported voiding-dysfunction rationale.
- Pass B: NO_SEMANTIC_RELATION - The witness only reports neutrophil superoxide inhibition at specified in vitro PTX concentrations (e.g., “1 µmol/L ... did not inhibit...; ≥5 µmol/L inhibited”). It does not address clinical exposure attainability, pelvic/urinary tissue levels, voiding dysfunction mechanism, or a rationale being defeated.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports an in-vitro concentration threshold for neutrophil superoxide inhibition (“1 µmol/L… did not inhibit…; ≥5 µmol/L inhibited”), which partially informs required concentrations for an effect, but it does not provide affirmative evidence of a consequential exposure mismatch in the impaired-voiding cohort or that this defeats the rationale.

### A1-H2-R2 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness proposes PTX mechanisms ("phosphodiesterase inhibitor and nitric oxide synthase activator" increasing "NO"/"cGMP") to explain beneficial effects in cardiac papillary muscle after ischemic injury; it does not report a urinary/pelvic tissue access/engagement mismatch nor that such a mismatch defeats a voiding-dysfunction rationale.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only proposes PTX mechanisms (“phosphodiesterase inhibitor and nitric oxide synthase activator” increasing “NO”/“cGMP”) to explain beneficial effects in cardiac papillary muscle after ischemic injury; it does not discuss a mismatch in target tissue access/presence/engagement in the voiding-dysfunction cohort or failure to translate into a meaningful remedy.

### A1-H2-R2 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: PARTIALLY_COVERS - Witness reports in an obstructed bladder model PTX "did not improve responses to carbachol" and authors infer effects were "not via cholinergic nerves"; this suggests a mechanistic non-engagement (cholinergic pathway) but does not establish target absence/irrelevance in urinary tissues nor that this defeats translation into a meaningful remedy for the cohort’s voiding dysfunction.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports PTX improved detrusor contraction to electrical stimulation but “did not improve responses to carbachol,” and authors infer effects were “not via cholinergic nerves”; this is partial evidence of non-engagement of one pathway, but it does not establish a consequential tissue access/presence/engagement mismatch that defeats translation into a meaningful voiding remedy for the cohort.

### A1-H2-R2 x W-FRD-Q0007-04-c1-Q0007
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: NO_SEMANTIC_RELATION - Witness discusses BOO/DU pathophysiology (afferent dysfunction; altered receptor expression/ATP) and does not address PTX tissue access/engagement or a mismatch that breaks PTX’s mechanism for improving voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes BOO/DU pathophysiology (“altered muscarinic and purinergic P2X3 receptor expression”/“diminished urothelial ATP”) without mentioning PTX, its tissue access/engagement, or any mismatch defeating a PTX rationale for treating voiding dysfunction.

### A1-H2-R2 x W-FRD-Q0010-03-Q0010
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, Figure 2 (“Figure 2. The percentage of referrals made for PFPT by diagnosis”), PFPT referral percentages by diagnosis are: Pelvic Floor Dysfunction 49.5%, CPPS 39.6%, Testicular Pain/Groin Pain 28.4%, LUTS 3.6%; the denominator is not stated.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18, Figure 2 ("Figure 2. The percentage of referrals made for PFPT by diagnosis"), including the table "Diagnosis | Percentage of Patients Referred"
- Pass A: NO_SEMANTIC_RELATION - Witness reports PFPT referral percentages by diagnosis; it contains no claims about PTX target presence/engagement in urinary/pelvic tissues or failure of PTX’s biological effects to translate due to tissue mismatch.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PFPT referral percentages by diagnosis (e.g., “Pelvic Floor Dysfunction 49.5%... LUTS 3.6%”) and contains no statement about PTX, target tissue access/presence/engagement, or translation failure for voiding dysfunction.

### A1-H2-R2 x W-FRD-Q0019-02-Q0019
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - By stating oral PTX yields “peak plasma PTX levels… <5 μmol/l” and combined actives “unlikely to exceed 10 μmol/l,” the witness provides exposure-limitation context, but it does not specifically show urinary/pelvic tissue non-engagement or that this defeats the voiding-mechanism rationale.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states clinically achieved exposures are limited (“peak plasma PTX levels are <5 μmol/l... combined level... unlikely to exceed 10 μmol/l”), which can bear on whether biological effects translate, but it does not specifically show urinary/pelvic target tissue access/presence/engagement mismatch defeating the voiding-dysfunction rationale.

### A1-H2-R2 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness shows PTX “significantly inhibited” FMLP-stimulated neutrophil burst in blood in vitro, not that PTX fails to engage a proposed urinary/pelvic tissue target or that such failure defeats a voiding rationale.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness shows an in-vitro whole-blood neutrophil effect (“5 µmol/l significantly inhibited... burst”), not a failure of PTX to access/engage a urinary/pelvic target tissue nor evidence that PTX’s effects fail to translate into a meaningful remedy for voiding dysfunction.

### A1-H2-R2 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports proportions with DU (e.g., “79% had detrusor underactivity”) and does not mention PTX, tissue target engagement, or any mechanism translation failure.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports epidemiologic findings in diabetics with LUTS (e.g., “79% had detrusor underactivity”) and does not mention PTX or any tissue access/presence/engagement mismatch that would defeat PTX’s rationale for treating voiding dysfunction.

### A1-H2-R2 x W-FRD-Q0042-03-c2-Q0042
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Side effects (epigastric pain treated with PPI) do not speak to PTX target presence/engagement in urinary tissues or to failure of biological effects to translate into meaningful voiding remedy.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes side effects and management (“two reported epigastric pain... omeprazole 40 mg per day... complete remission”) and provides no information about PTX target tissue access/presence/engagement or translation failure for voiding dysfunction.

### A1-H2-R2 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - “Adverse effects were not reported”/“No adverse effects… were observed” is about tolerability, not about tissue engagement in urinary/pelvic tissues or a mechanistic mismatch defeating voiding improvement rationale.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states tolerability (“Adverse effects were not reported...”, “No adverse effects... were observed”) and does not address PTX’s tissue access/presence/engagement or any mismatch defeating a voiding-dysfunction remedy rationale.

### A1-H2-R2 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only states PTX is “very safe”/“well tolerated” with common adverse effects (GI symptoms, dizziness) and does not address urinary/pelvic tissue target access/engagement or failure of mechanism-to-voiding translation.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R2 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in tissue (target tissue access, presence, or engagement) such that PTX’s reported biological effects do not translate into a meaningful remedy for the cohort’s voiding dysfunction, defeating the materially supported rationale.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: PARTIALLY_COVERS - Witness speculates PTX 'may have no potent anti-inflammatory effect once inflammation has been triggered' and may be 'too weak' for an ongoing cascade, suggesting a mechanism not translating in established disease; however it does not specify a 'tissue (target tissue access, presence, or engagement)' mismatch in urinary/pelvic tissues or link explicitly to voiding dysfunction in the cohort.
- Pass B: NO_SEMANTIC_RELATION - The witness is speculation ('may have no potent anti-inflammatory effect once inflammation has been triggered') and does not identify urinary/pelvic tissue access/target absence or link to voiding dysfunction in the cohort.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R3 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness proposes PTX mechanisms (PDE inhibition, NOS activation increasing NO/cGMP) to explain beneficial effects after ischemic injury; it does not assert a mismatch between the cohort’s voiding dysfunction drivers and PTX’s effects or that rationale is defeated.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only "propose[s] PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator... offered as mechanisms" for beneficial effects after ischemic injury; it does not state that the cohort’s impaired-voiding dysfunction is not addressed by PTX’s effects or that the rationale is defeated.

### A1-H2-R3 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: PARTIALLY_COVERS - Witness reports PTX improved detrusor contractions to electric stimulation but not to carbachol and speculates effects are not via cholinergic nerves; this suggests a pathway-specific limitation, but does not establish that the main driver of impaired voiding in the defined cohort is not meaningfully addressed by PTX or that the therapeutic rationale is defeated.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness reports PTX improved detrusor contractions to electric stimulation but "did not improve responses to carbachol" and speculates effects were "not via cholinergic nerves"; this is a pathway-specific limitation but does not establish a consequential disease-process mismatch defeating rationale for the cohort.

### A1-H2-R3 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness gives a definition of detrusor underactivity (reduced strength/duration causing prolonged/incomplete emptying) and makes no claim about PTX effects or a disease-process mismatch.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only quotes the ICS definition of detrusor underactivity ("contraction of reduced strength and/or duration..."); it makes no claim about PTX’s biological effects failing to address the driver of impaired voiding.

### A1-H2-R3 x W-FRD-Q0007-03-Q0007
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: PARTIALLY_COVERS - Witness reports that in men with DU+BPH, urothelial ATP decreased while nitric oxide showed no significant change; this bears on whether NO-related pathways are implicated, but does not connect to PTX’s effects or show the cohort’s voiding driver is not meaningfully addressed by PTX such that rationale is defeated.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness reports in men with DU+BPH that "urothelial ATP was significantly decreased" while "nitric oxide showed no significant change"; this bears on mechanisms but does not link to PTX’s reported effects or conclude a mismatch defeating rationale.

### A1-H2-R3 x W-FRD-Q0009-02-c2-Q0009
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: Chuang2015.pdf.md (## EPIDEMIOLOGY) summarizes Abarbanel & Marcus: in 181 LUTS patients aged ≥70 (82 men, 99 women), impaired detrusor contractility was defined urodynamically as Qmax <10 mL/s plus detrusor pressure <30 cm H2O, and was reported in 48% of men and 12% of women.
- Source: chuang2015.pdf.md ## EPIDEMIOLOGY (paragraph beginning “In men, detrusor underactivity may be caused… Abarbanel and Marcus…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports prevalence/definition of impaired detrusor contractility in elderly LUTS patients; it does not address PTX mechanisms or mismatch defeating therapeutic rationale.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R3 x W-FRD-Q0014-02-Q0014
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is diagnostic/prognostic: “detect detrusor underactivity… could replace pressure-flow studies… predict DU,” not a claim about PTX effects failing to address the main driver.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R3 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states “PTX… inhibited… hydrogen peroxide production to 76 ± 5%,” which is an immune/oxidative marker finding and does not assert a voiding-driver mismatch or failure of PTX pathways for impaired voiding.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R3 x W-FRD-Q0025-03-Q0025
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: In delanian2005.pdf.md (RESULTS → Primary Analyses → “After stopping PTX-vitE: Rebound effect.”), after stopping PTX-vitE, RIF surface area showed a significant initial increase (P = .037). The fibrotic increase was significantly lower and asymptomatic in LPE: 8.5%/yr (95% CI, 1–16) vs SPE: 40%/yr (95% CI, 24–56); P = .0012.
- Source: delanian2005.pdf.md RESULTS → Primary Analyses → “After stopping PTX-vitE: Rebound effect.”
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about “RIF surface area… after stopping PTX-vitE” and rebound rates, not urinary voiding physiology nor whether PTX-relevant pathways miss the main driver of impaired voiding.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R3 x W-FRD-Q0027-01-c3-Q0027
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): According to Osman et al. [4] review, DU was reported in 9%–28% of men aged <50 years, 48% of men aged >70 years, and 12%–45% of women aged >70 years.
- Source: 2020ICU_icu-58-S68.pdf.md PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (paragraph beginning 'According to the recent review from Osman et al. [4], ...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness provides prevalence ranges (“DU… 9%–28%… 48%… 12%–45%”) and makes no claim about PTX or mechanistic non-addressing of the driver.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R3 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports epidemiology only: “52 men with diabetes… 79% had detrusor underactivity,” without any PTX intervention or claim that PTX pathways fail to affect the driver.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R3 x W-FRD-Q0029-04-c5-Q0029
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness concerns follow-up loss: “developed severe disease and shifted… steroid therapy” / “did not return,” not any statement about voiding pathophysiology or PTX mechanism mismatch.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R3 x W-FRD-Q0042-03-c2-Q0042
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in disease process: the dysfunction driving impaired voiding in this cohort is not meaningfully addressed by PTX’s reported biological effects, defeating the materially supported rationale.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only reports adverse event management: “two reported epigastric pain… omeprazole 40 mg per day… complete remission,” with no mention of voiding dysfunction drivers or PTX biological pathways vs disease process.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness proposes PTX mechanisms (PDE inhibition/NO synthase activation increasing NO/cGMP) to explain beneficial contractile effects after ischemic injury; it does not address timing, reversibility, or an incompatibility with meaningful recovery in impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only proposes PTX mechanisms (“phosphodiesterase inhibitor and nitric oxide synthase activator… increases tissue NO and intracellular cGMP”) to describe “beneficial effects on contractile function after ischemic injury”; it makes no claim about timing/reversibility mismatch vs meaningful recovery in impaired voiding.

### A1-H2-R4 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports pathway inference (improved electric-stimulation contractions but not carbachol responses) about PTX’s protective mechanism; it makes no claim about timescale, non-reversal, or timing mismatch defeating a therapeutic rationale.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a mechanistic inference (improved detrusor contractions to “electric stimulation” but not “carbachol,” hence not cholinergic); it does not address PTX effect timescale, non-reversal/preventive-only action, or any incompatibility with recovery in voiding.

### A1-H2-R4 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness provides a definition of detrusor underactivity (reduced strength/duration causing prolonged emptying); it contains no statement about PTX timing/reversibility or a mismatch with recovery.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is a definition of detrusor underactivity (“reduced strength and/or duration… prolonged bladder emptying”); it contains nothing about PTX or a timing/reversibility mismatch defeating a rationale.

### A1-H2-R4 x W-FRD-Q0007-04-c1-Q0007
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: PARTIALLY_COVERS - Witness says afferent dysfunction may play a role in the 'initial and reversible stages of DU' in BOO; this speaks to reversibility stage-dependence but does not mention PTX, its effect timing, or that PTX is incompatible with meaningful improvement/recovery.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0007-04-c4-Q0007
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: PARTIALLY_COVERS - Witness notes a 'point of no return' after which irreversible bladder decompensation/failure occur, implying timing/reversibility can matter; however it does not attribute any timing mismatch to PTX or conclude PTX’s effects occur on an incompatible timescale defeating the rationale.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0009-04-Q0009
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Chuang2015.pdf.md (EPIDEMIOLOGY) says Thomas et al. reported that, in men with untreated detrusor underactivity and minimum 10-year urodynamic follow-up, detrusor underactivity was not progressive in most nonneurogenic male patients and often did not result in chronic urinary retention.
- Source: chuang2015.pdf.md EPIDEMIOLOGY section (paragraph beginning “Thomas and colleagues9 reported…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports long-term follow-up where DU was not progressive in most nonneurogenic men and often did not lead to chronic retention; it does not discuss PTX effects, timing of action, reversibility, or mismatch versus recovery.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Discusses dutasteride+tamsulosin combination therapy risk reduction in CombAT; does not mention PTX or any claim about PTX effect timing/reversibility undermining a rationale.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0042-03-c2-Q0042
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: NO_SEMANTIC_RELATION - Witness discusses side effects and completion of 24 weeks of treatment (epigastric pain treated with omeprazole) but says nothing about PTX effect timing/reversibility relative to voiding recovery or any timing mismatch defeating rationale.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - Witness is only about absence of adverse effects of pentoxifylline; it makes no claim about the timescale or reversibility of PTX effects in relation to meaningful improvement in impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness addresses PTX safety/tolerability and common side effects; it does not state PTX has an incompatible timescale/non-reversal-only effect relative to recovery of voiding impairment.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX inhibits PDE 1–5 with IC50 values; no timing/duration or reversibility claim about voiding improvement is made.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0052-04-c1-Q0052
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: In nihms-1048633.pdf.md (Fig. 1 CONSORT diagram), 981 were assessed; 958 female patients were included; 23 were excluded, including “Male / transgender” (n=8).
- Source: nihms-1048633.pdf.md Fig. 1 CONSORT diagram (participant flow/exclusions)
- Pass A: NO_SEMANTIC_RELATION - Witness is about study participant sex exclusions (female-only cohort); it does not discuss PTX timing/reversibility or voiding recovery.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R4 x W-FRD-Q0060-02-c2-Q0060
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Gülen2024_MCAS.md (“Diagnosis of MCAS”) says serum tryptase usually rises during acute systemic mast cell activation (e.g., anaphylaxis, MCAS), peaks about 1 h after clinical onset, then declines with ~2 h half-life; it may remain elevated 3 h, 5 h, or longer depending on initial elevation magnitude, which correlates best with mean arterial pressure drop magnitude.
- Source: Gulen2024_MCAS.md Section: "Diagnosis of MCAS" (laboratory criterion paragraph containing tryptase kinetics)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses serum tryptase kinetics during mast cell activation (peaks ~1h, half-life ~2h); it is not about PTX nor about voiding impairment recovery timescales.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states serum tryptase kinetics during acute mast cell activation (“peaks about 1 h… declines with ~2 h half-life”), with no mention of pentoxifylline (PTX), voiding impairment, or any timing/reversibility mismatch vs clinical recovery in the cohort.

### A1-H2-R4 x W-FRD-Q0072-04-c1-Q0072
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (METHODS > Subjects) reports that, during a two-year period after unilateral adrenalectomy in 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, symptomatic thyroid dysfunction developed in 3 of 24 patients.
- Source: Takasu1990_Cushings_Syndrome_Due.md METHODS > Subjects
- Pass A: NO_SEMANTIC_RELATION - Witness concerns thyroid dysfunction after adrenalectomy in Cushing’s syndrome patients; it does not mention PTX or timing mismatch with voiding improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports incidence of “symptomatic thyroid dysfunction” after unilateral adrenalectomy in Cushing’s syndrome patients, and does not address PTX effects, voiding outcomes, or relative timescales/reversibility.

### A1-H2-R4 x W-FRD-Q0072-04-c2-Q0072
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (DISCUSSION) reports that among 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, 5 patients (including the 3 who later developed thyroid dysfunction) had increased antimicrosomal-antibody titers: 5/24 (21%), described as high versus 8.5% in normal women in Japan.
- Source: Takasu1990_Cushings_Syndrome_Due.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Witness reports antimicrosomal-antibody titers in Cushing’s syndrome patients; no content about PTX timing/reversibility or voiding recovery.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses “increased antimicrosomal-antibody titers” in Cushing’s syndrome patients (5/24) versus normal women; it contains no claims about PTX, voiding recovery, or timing/reversibility incompatibility.

### A1-H2-R4 x W-FRD-Q0085-01-c3-Q0085
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety): During the study, no severe adverse effects were reported, including no threatening hypotension or syncope; vital signs remained almost stable; no urinary retention occurred; and therapy did not stop for TEAEs (not explicitly phrased as zero TEAE dropouts).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: NO_SEMANTIC_RELATION - Witness is limited to safety outcomes (no severe adverse effects, no urinary retention); it does not provide affirmative evidence of PTX effect timing being incompatible with meaningful voiding recovery.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is confined to safety findings (“no severe adverse effects… no urinary retention occurred; vital signs remained almost stable”) and provides no affirmative evidence about PTX efficacy timing, non-reversibility, or mismatch with meaningful improvement in impaired voiding.

### A1-H2-R4 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports an in vitro neutrophil preincubation experiment on calcium transients at specific PTX concentrations; it does not address clinical timing/reversibility of PTX effects versus voiding recovery in the specified cohort.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in vitro neutrophil preincubation study where PTX at specified concentrations affected calcium transients (e.g., “500 µmol/l reduced resting [Ca2+]i…”), which does not speak to clinical timing/reversibility of PTX effects relative to voiding recovery in the cohort.

### A1-H2-R4 x W-FRD-Q0092-03-c4-Q0092
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch in timing/reversibility: PTX’s effects occur on an incompatible timescale (or are non-reversal/preventive only) relative to meaningful improvement/recovery in impaired voiding for this cohort, defeating the materially supported rationale.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: NO_SEMANTIC_RELATION - Witness repeats side-effect information from desouza2009 (epigastric pain treated with omeprazole) and does not speak to PTX timing mismatch or non-reversal-only effects relative to voiding improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports treatment completion and side effects (“2 patients reported epigastric pain… complete remission” with omeprazole) without any claim about PTX effect timescale, reversibility, or mismatch with voiding improvement.

### A1-H2-R5 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: PARTIALLY_COVERS - Witness reports mixed functional results in an obstructed bladder model: PTX improved detrusor contractions to electric stimulation but did not improve carbachol responses; this suggests a pathway-specific dissociation (cholinergic response not improved) but does not establish that a PTX-modulated biomarker/marker change fails to translate into improved voiding/urodynamic function overall.
- Pass B: NO_SEMANTIC_RELATION - Witness reports mixed contractile findings (improved electrical-stimulation contractions, no improvement to carbachol) and a mechanistic inference, but does not state a biomarker was modulated while voiding/urodynamic function failed to improve.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX changed detrusor contractile responses in an obstructed bladder model (“improved detrusor contractions to electric stimulation… but did not improve responses to carbachol”) and offers a mechanistic assumption about pathways; it does not mention a PTX-affected biological marker nor “actual urinary function/voiding” failing to improve despite marker modulation.

### A1-H2-R5 x W-FRD-Q0014-02-Q0014
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about diagnostic prediction (DWT/capacity predicting DU) and does not mention PTX, biomarker modulation by PTX, or lack of functional improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about ultrasound DWT and bladder capacity predicting detrusor underactivity (diagnostic accuracy, PPV/NPV) and contains no PTX exposure, no PTX-affected marker, and no claim about marker modulation not translating into improved voiding.

### A1-H2-R5 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness shows a blood neutrophil functional/PD effect (“inhibited ... hydrogen peroxide production to 76±5%”) but contains no statement about voiding/urodynamic function not improving.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a pharmacodynamic effect in blood neutrophils (“PTX… inhibited… hydrogen peroxide production to 76±5%”) but says nothing about urinary/voiding function or a mismatch between a PTX-modulated marker and voiding outcomes.

### A1-H2-R5 x W-FRD-Q0029-04-c4-Q0029
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.5.2. Fecal Calprotectin), fecal calprotectin <100 µg/g occurred in 18 patients (66.7%) on PTX vs 14 (53.8%) on placebo; <50 µg/g occurred in 6 (20%) on PTX vs 2 (6%) on placebo. Denominators are not explicitly stated.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.5.2. Fecal Calprotectin
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports fecal calprotectin (a GI inflammation marker) proportions on PTX vs placebo, but provides no urinary function/voiding outcome showing non-translation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports fecal calprotectin proportions on PTX vs placebo (<100 µg/g, <50 µg/g) and does not address urinary function/voiding, nor any claim that a PTX-modulated marker failed to translate into improved voiding.

### A1-H2-R5 x W-FRD-Q0034-04-bortnick20-c1-Q0034
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: bortnick2020.pdf.md (“Medical therapy”→“Combination therapy” MTOPS paragraph) reports MTOPS studied finasteride+doxazosin in 3000 men (mean age 62.6 years, SD 7.3) and found combination therapy improved voiding symptoms and maximum urinary flow rate more than either alone, prevented BPH progression better, and reduced the long-term risk of acute urinary retention and need for invasive therapy.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (MTOPS paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports MTOPS benefits of finasteride+doxazosin on symptoms/flow and progression, not PTX biomarker effects failing to improve voiding.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness summarizes MTOPS findings for finasteride+doxazosin improving LUTS/flow and reducing BPH progression; it does not involve PTX, a PTX-affected biological marker, or evidence of marker–voiding mismatch.

### A1-H2-R5 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about BPH combo therapy outcomes (risk reduction) and does not mention PTX, biomarkers, or a failure of urinary functional improvement despite marker change.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes CombAT outcomes (reduced risk of AUR/surgery and progression) for BPH combination therapy, not PTX; no biomarker-vs-voiding non-translation is stated.

### A1-H2-R5 x W-FRD-Q0043-03-Q0043
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: ladi-seyedian2017.pdf.md (7.4. Electrical stimulation) says sacral neuromodulation (SNM) could be an effective option for non-obstructive urinary retention; it reports Lombardi et al. assessed SNM for neurogenic non-obstructive urinary retention in patients with incomplete spinal cord lesions and found 42.4% (36/85) improved during the percutaneous first stage of SNM.
- Source: ladi-seyedian2017.pdf.md Section 7.4. Electrical stimulation
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses SNM effectiveness (42.4% improved) and does not mention PTX, biomarkers, or a biomarker–voiding mismatch.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports sacral neuromodulation effectiveness in non-obstructive urinary retention (“42.4%… improved”) and does not mention PTX, any PTX-affected marker, or a marker modulation failing to improve voiding.

### A1-H2-R5 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness says “Adverse effects were not reported” / “No adverse effects ... observed,” which is about tolerability, not biomarker modulation or lack of improvement in voiding-related function.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states tolerability only (“Adverse effects were not reported…”, “No adverse effects… observed”) and contains no claim about biomarkers or urinary/voiding function outcomes.

### A1-H2-R5 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness is about PTX safety/tolerability (GI symptoms, dizziness) and does not mention any biomarker modulation vs urinary/voiding functional outcomes.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R5 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - Witness reports a mechanism (PTX inhibits PDE1–5 with IC50 50–200 μmol/L) but provides no evidence about urinary function or a mismatch between biomarker changes and voiding outcomes.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R5 x W-FRD-Q0061-02-c5-Q0061
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: In siu2003.pdf.md (Abstract (Results)), the authors report the pelvic muscle training program “appears to be able to reduce the overall urinary incontinence episodes by 85.2%.”
- Source: siu2003.pdf.md Abstract (Results)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns pelvic muscle training reducing urinary incontinence episodes; it is not about PTX, biomarker modulation, or failure to improve voiding.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R5 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX reducing lysozyme release in PMNs under inflammatory stimulation; it does not address urinary function or a biomarker–voiding mismatch in relevant urinary conditions.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H2-R5 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX effects (mostly none up to 50 µmol/L; reduction at 500 µmol/L) on neutrophil calcium transients; no urinary biomarker/urodynamic or voiding outcomes are discussed.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports PTX effects on neutrophil intracellular calcium transients (e.g., 'PTX up to 50 µmol/L changed neither... [Ca2+]i; 500 µmol/L reduced...'), but the unit requires evidence of a mismatch between a PTX-affected biological marker and 'actual urinary function'/'improved voiding'; no urinary/voiding outcomes or urinary biomarkers are mentioned.

### A1-H2-R5 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): Affirmative evidence demonstrates a consequential mismatch between a biological marker affected by PTX and actual urinary function, such that marker modulation does not translate into improved voiding in relevant conditions, defeating the materially supported rationale.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: PARTIALLY_COVERS - Witness speculates PTX may be too weak to suppress ongoing inflammation ('may have no potent anti-inflammatory effect once inflammation has been triggered'), which gestures at a biomarker/PD-to-clinical ineffectiveness gap, but it does not report biomarker modulation alongside unchanged urinary/voiding functional measures.
- Pass B: NO_SEMANTIC_RELATION - Witness 'speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered' but does not discuss voiding outcomes or an observed biomarker-versus-urinary-function mismatch.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only offers a general speculation about anti-inflammatory potency ('may have no potent anti-inflammatory effect once inflammation has been triggered' and 'may be too weak to suppress...'), without reporting any PTX-driven biomarker modulation alongside unchanged urinary function/voiding; thus it does not support the unit’s required biomarker-versus-voiding mismatch.

### A1-H3-A1 x W-FRD-Q0006-04-c1-Q0006
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: NO_SEMANTIC_RELATION - Witness is about whether NO blockers (e.g., L-NAME) were used to test pentoxifylline-induced vascular relaxation mechanism in vitro; it does not specify trial slots for the BPH/shy-bladder voiding context nor does it defeat/resolve the therapeutic rationale described in the unit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states they "did not add NO blockers such as L-NAME" and instead tested "endothelium dependence by denuding" in vitro; it neither resolves decisive links to "specify all four trial slots" nor "defeats the supported therapeutic rationale" for the unit.

### A1-H3-A1 x W-FRD-Q0013-03-c4-Q0013
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Defines bladder outlet obstruction using detrusor pressure, flow rate, and radiographic evidence; this is a diagnostic definition and does not resolve the decisive links to complete all four trial slots or provide mechanistic defeat/endorsement of the supported therapeutic rationale in the unit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness defines "bladder outlet obstruction" via pressure/flow/radiographic criteria; the unit is about evidence sufficient to specify all four trial slots or defeat the therapeutic rationale, which this diagnostic definition does not address.

### A1-H3-A1 x W-FRD-Q0015-04-c2-Q0015
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: Osman2018 (osman2018.pdf.md, “Diagnostic aspects > Detrusor contraction strength > 2. Projected isovolumetric pressure (PIP)”) provides a PIP calculation formula (K varies by population/sex; usually 5 in men) and suggested contractility groupings: >150 strong, 100–150 normal, 50–100 weak, <50 very weak; these formulae may overestimate PIP and have less test–retest reliability than direct isovolumetric measurement.
- Source: osman2018.pdf.md ## Diagnostic aspects > ### Detrusor contraction strength > #### 2. Projected isovolumetric pressure (PIP)
- Pass A: NO_SEMANTIC_RELATION - Provides a PIP formula and contractility groupings plus reliability caveats; it concerns measurement of detrusor contractility but does not, as written, enable completion of the full intervention/phenotype/measurement/comparator trial design or defeat the therapeutic rationale.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides a PIP formula and contractility groupings ("strong/normal/weak") plus reliability caveats; it does not claim decisive evidence that completes the unit’s four trial slots or defeats the therapeutic rationale.

### A1-H3-A1 x W-FRD-Q0020-02-c1-Q0020
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Reports a dosing regimen of pentoxifylline in four healthy volunteers (5×400 mg/day for 2 days or 7 days) without linking to BPH/shy bladder outcomes or resolving/defeating the therapeutic rationale needed to specify the trial slots in the unit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports dosing of pentoxifylline in "four healthy volunteers" for "2 days" or "7 days"; it does not speak to resolving decisive links for the hypothesis’ trial-slot specification or defeating the therapeutic rationale.

### A1-H3-A1 x W-FRD-Q0029-04-c5-Q0029
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: NO_SEMANTIC_RELATION - Describes differential loss to follow-up in a mesalamine/placebo vs PTX group due to severe disease or non-return; it is about attrition and does not resolve trial-slot specification or mechanistically defeat/endorse the therapeutic rationale for the unit’s BPH context.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes attrition (patients "lost to follow-up" due to severe disease or non-return) in a mesalamine/placebo vs PTX group; this is not evidence resolving trial-slot design for the hypothesis nor defeating its rationale.

### A1-H3-A1 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: NO_SEMANTIC_RELATION - States that combination therapy in CombAT reduced risk of urinary retention/surgery and progression vs monotherapy; while BPH-related, it does not address the unit’s requirement of resolving decisive links for the specific hypothesized rationale/trial slots (including PTX/pelvic-floor history/shy bladder context) nor defeat it mechanistically.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness claims CombAT combination therapy reduced risk of "acute urinary retention or BPH-related surgery" vs monotherapy; it does not, as written, resolve the unit’s decisive links to specify all four trial slots for the stated hypothesis or defeat its therapeutic rationale.

### A1-H3-A1 x W-FRD-Q0050-03-Q0050
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - Reports that pentoxifylline inhibits PDE 1–5 with IC50 50–200 μmol/L; this is a biochemical mechanism note but does not, as written, resolve the decisive links to specify the four trial slots in the stated BPH population nor provide affirmative mechanistic evidence defeating the supported rationale.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a mechanism note (pentoxifylline "inhibits PDE 1–5" with "IC50 50–200 μmol/L"); it does not provide decisive evidence sufficient to specify the unit’s four trial slots or to defeat the therapeutic rationale.

### A1-H3-A1 x W-FRD-Q0053-02-c4-Q0053
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: NO_SEMANTIC_RELATION - Notes questionnaire timing after ≥6 weeks PFME and cautions generalization to other PFME stages; it does not provide decisive-link resolution to specify intervention/phenotype/measurement/comparator for the unit’s male BPH/shy-bladder trial, nor does it mechanistically defeat the rationale.
- Pass B: PARTIALLY_COVERS - Witness addresses measurement/timing considerations (“questionnaire after… at least six weeks”; “generalized cautiously to women at different stages”), which is one piece of trial-slot specification, but it is not scoped to the unit’s men-with-BPH context and does not resolve all four slots or defeat the rationale.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness says questionnaires were completed after "at least six weeks" of PFME and cautions generalization to "women at different stages"; this does not claim evidence that resolves decisive links to specify all four trial slots or defeats the therapeutic rationale in the unit.

### A1-H3-A1 x W-FRD-Q0107-02-c4-Q0107
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: Chung2014.pdf.md (Conclusions): Chung (2014) says post-void residual measurement may indicate underlying detrusor failure if BOO is excluded, but at present urodynamic study should be conducted to consolidate the diagnosis of UAB by functionally demonstrating the presence of DU.
- Source: chung2014.pdf.md Conclusions
- Pass A: NO_SEMANTIC_RELATION - Says PVR may indicate detrusor failure if BOO excluded and urodynamics should consolidate UAB diagnosis; this is clinical diagnostic guidance but does not complete the unit’s required trial-slot specification nor provide mechanistic defeat/endorsement of the therapeutic rationale.
- Pass B: PARTIALLY_COVERS - Witness informs the measurement/phenotyping slot by stating PVR “may indicate… detrusor failure if BOO is excluded” and recommending urodynamics to demonstrate DU, but it does not specify intervention/exposure/comparator for the hypothesized PTX+tamsulosin+PFME context nor provide mechanistic defeat/endorsement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides diagnostic guidance (PVR "may indicate" detrusor failure if BOO excluded; urodynamics "should" consolidate UAB diagnosis by demonstrating DU); it does not resolve decisive links for full trial-slot specification nor defeat the therapeutic rationale stated in the unit.

### A1-H3-A1 x W-FRD-Q0138-04-Q0138
- Unit (ADVERSE_TEST): Evidence resolves the decisive links sufficiently to specify all four trial slots (favoring H1) or instead defeats the supported therapeutic rationale (favoring H2).
- Witness: nihms496647.pdf.md (“Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome”): unpublished extended data using proposed criteria: among 132 patients enrolled and referred for suspected or confirmed disease over four years, 58 met WHO systemic mastocytosis criteria, 7 MMAS, 19 IA; 42 had mast cell activation symptoms without evidence of clonal mast cells; 6 had unrelated diagnoses.
- Source: nihms496647.pdf.md Section: “Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome” (paragraph beginning “Using the approach outlined above…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness concerns mast cell activation syndrome criteria and patient breakdown (“58 met WHO systemic mastocytosis…”) and has no content on BPH, voiding, pelvic-floor history, PTX/tamsulosin trial-slot completion, or mechanistic defeat.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-C1 x W-FRD-Q0003-04-c1-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses proposed PTX mechanisms (PDE inhibition/NOS activation) and cites cardiac data; it says nothing about whether retrieval and adverse testing have been completed or whether uncertainty is due to unfinished investigation.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only discusses proposed PTX mechanisms (“phosphodiesterase inhibitor and nitric oxide synthase activator… mechanisms… beneficial effects”) and does not address whether “meaningful retrieval” or “adverse testing” have been completed or whether uncertainty is due to “unfinished investigation.”

### A1-H3-C1 x W-FRD-Q0005-04-c2-Q0005
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: In han1990.pdf.md (Materials and Methods—CAT Assay), the authors state that the CAT assay “was performed according to the thin-layer chromatography method of Gorman et al. (9).”
- Source: han1990.pdf.md Materials and Methods — CAT Assay
- Pass A: NO_SEMANTIC_RELATION - Witness only states the CAT assay method used (TLC method of Gorman et al.); it does not address completeness of literature retrieval or completion of adverse testing relevant to the hypothesis uncertainty.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states only the lab method (“CAT assay ‘was performed according to… Gorman et al.’”) and contains no claim about completeness of investigation, retrieval, or adverse testing versus remaining uncertainty.

### A1-H3-C1 x W-FRD-Q0010-04-c1-Q0010
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness reports a retrospective chart review and ICD-code identification; it does not indicate whether investigation is complete or whether remaining uncertainty is due to unfinished retrieval/testing.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes a retrospective chart review and identification via ICD codes (“retrospective chart review… identified using ICD codes…”) but does not speak to whether investigation is completed or whether uncertainty is not due to unfinished work.

### A1-H3-C1 x W-FRD-Q0013-03-c4-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness gives a definition for bladder outlet obstruction (pressure/flow/radiographic criteria); it does not speak to whether meaningful retrieval and adverse testing have been completed.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides only a definitional criterion for bladder outlet obstruction (“defined as sustained detrusor contraction >45 cm… flow rate <12 ml/s… radiographic evidence”) and does not address completion of retrieval/adverse testing or the source of remaining uncertainty.

### A1-H3-C1 x W-FRD-Q0014-02-Q0014
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: NO_SEMANTIC_RELATION - Witness claims ultrasound DWT and bladder capacity can predict detrusor underactivity and potentially replace pressure-flow studies; it does not address whether uncertainty remains due to incomplete searching/retrieval or unfinished adverse tests.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness claims diagnostic performance of ultrasound DWT and bladder capacity (“can safely… detect… could replace pressure-flow studies… predict DU”) but does not state that retrieval/testing is complete or that uncertainty is not due to unfinished investigation.

### A1-H3-C1 x W-FRD-Q0036-02-c3-Q0036
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: Stokes2022.pdf.md (STUDY DESIGN, MATERIALS AND METHODS) reports analyses used the 1st diaries returned (at the 2nd appointment), so only a subset contributed data: women who attended first follow-up, returned a completed diary, and had available prescription data.
- Source: stokes2022.pdf.md STUDY DESIGN, MATERIALS AND METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness describes a study subset/data availability limitation (only women returning diaries etc.); it is about sample inclusion, not about whether investigation is complete or uncertainty stems from incomplete retrieval/testing.
- Pass B: CONTRADICTS - Witness: “only a subset contributed data… attended first follow-up, returned a completed diary, and had… prescription data,” indicating incomplete data collection/availability. This conflicts with the unit’s requirement that uncertainty is not due to incomplete/unfinished investigation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness notes an analysis inclusion subset (“only a subset contributed data… returned a completed diary… available prescription data”), which is a study-design/data-availability detail and does not make any claim about whether overall ‘meaningful retrieval and adverse testing have been completed’ or about the cause of remaining uncertainty.

### A1-H3-C1 x W-FRD-Q0052-02-c2-Q0052
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: Alewijnse2003.pdf.md (Results > Participants and non-response) reports: of the 103 women who completed 12-month follow-up measurements, 15 did not return the post-test measurement and 2 did not return the 3-month follow-up measurement; reasons were unknown.
- Source: alewijnse2003.pdf.md Results > Participants and non-response
- Pass A: NO_SEMANTIC_RELATION - Witness discusses missing follow-up measurements and unknown reasons for non-response, which concerns study attrition, not whether key sources were searched/retrieved or adverse tests were attempted/completed for the hypothesis.
- Pass B: CONTRADICTS - The witness indicates incomplete data collection (“15 did not return the post-test measurement… reasons were unknown”), which points to uncertainty arising from uncompleted/unfinished measurement rather than fully completed investigation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports follow-up non-response (“15 did not return the post-test… 2 did not return the 3-month… reasons were unknown”) but does not address the unit’s meta-claim about completion of meaningful retrieval/adverse testing or whether remaining uncertainty is due to unfinished investigation.

### A1-H3-C1 x W-FRD-Q0053-02-c4-Q0053
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: NO_SEMANTIC_RELATION - Witness describes PFME exposure duration and cautions about generalizing cross-sectional findings; it does not indicate anything about completeness of evidence retrieval or completion of adverse testing.
- Pass B: PARTIALLY_COVERS - The witness implies limits in evidence scope (“findings should be generalized cautiously to women at different stages of PFME training”), which speaks to residual uncertainty, but it does not specifically establish that retrieval/adverse testing has been completed (it could still be due to missing studies).
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes timing and generalizability limits (“after… at least six weeks… findings should be generalized cautiously”) but does not state that retrieval/adverse testing is completed nor that remaining uncertainty is not due to unfinished investigation.

### A1-H3-C1 x W-FRD-Q0107-02-c4-Q0107
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: Chung2014.pdf.md (Conclusions): Chung (2014) says post-void residual measurement may indicate underlying detrusor failure if BOO is excluded, but at present urodynamic study should be conducted to consolidate the diagnosis of UAB by functionally demonstrating the presence of DU.
- Source: chung2014.pdf.md Conclusions
- Pass A: NO_SEMANTIC_RELATION - Witness recommends urodynamic study to consolidate diagnosis (a clinical recommendation), not whether the hypothesis uncertainty stems from unfinished investigation or incomplete adverse testing.
- Pass B: CONTRADICTS - The witness explicitly indicates investigation is still needed (“at present urodynamic study should be conducted… to consolidate the diagnosis”), which conflicts with the unit’s constraint that uncertainty is not due to unfinished investigation/testing.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness gives a clinical recommendation (“urodynamic study should be conducted to consolidate the diagnosis”) rather than a statement that the evidence base has completed meaningful retrieval/adverse testing or that remaining uncertainty is not due to unfinished investigation.

### A1-H3-C1 x W-FRD-Q0138-04-Q0138
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: nihms496647.pdf.md (“Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome”): unpublished extended data using proposed criteria: among 132 patients enrolled and referred for suspected or confirmed disease over four years, 58 met WHO systemic mastocytosis criteria, 7 MMAS, 19 IA; 42 had mast cell activation symptoms without evidence of clonal mast cells; 6 had unrelated diagnoses.
- Source: nihms496647.pdf.md Section: “Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome” (paragraph beginning “Using the approach outlined above…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports enrollment/diagnostic categorization (“unpublished extended data… among 132 patients…”) but says nothing about completeness of retrieval or completion of adverse testing relevant to the hypothesis uncertainty.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports patient categorization in “unpublished extended data… among 132 patients… met WHO systemic mastocytosis… MMAS… IA…” but does not mention completion of retrieval/adverse testing or attribute remaining uncertainty to anything other than study findings.

### A1-H3-C1 x W-FRD-Q0144-01-c3-Q0144
- Unit (CONTEXTUAL_CONSTRAINT): Meaningful retrieval and adverse testing have been completed; remaining uncertainty is not due to unfinished investigation.
- Witness: In Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety), mild adverse events occurred in 11 intervention vs 13 control patients; most were mild dyspepsia requiring no treatment. No severe adverse effects (no threatening hypotension or syncope) and no urinary retention episodes; vital signs remained almost stable.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only states study safety findings (“mild adverse events… No severe adverse effects…”) and does not address whether evidence retrieval/testing is complete or whether uncertainty is due to unfinished investigation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports safety outcomes (“mild adverse events… No severe adverse effects… no urinary retention… vital signs… stable”) but does not claim that adverse testing (as a completeness constraint) and meaningful retrieval are fully completed or that uncertainty is not due to unfinished investigation.

### A1-H3-E1 x W-FRD-Q0006-04-c1-Q0006
- Unit (CORROBORATING_EXPECTATION): Competing explanations remain compatible because key discriminators (exposure, tissue effects, functional consequences, response predictors) are unmeasured or not distinguished, blocking at least one trial-specification slot; and the investigation identifies the experiment that would resolve the uncertainty, recording which slot is blocked and by which link.
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: PARTIALLY_COVERS - Witness explicitly notes a key discriminator was not measured: they 'did not add NO blockers such as L-NAME to test whether' relaxation was NO-dependent, which leaves NO-dependence vs alternatives compatible; however it does not identify a trial-specification slot blocked, nor a proposed experiment to resolve it (beyond implying adding NO blockers).
- Pass B: NO_SEMANTIC_RELATION - Witness says they “did not add NO blockers such as L-NAME to test whether… relaxation… was NO-dependent”; it does not frame this as competing explanations remaining compatible with a blocked trial-spec slot, nor does it identify a future experiment to resolve uncertainty (it states what they did instead).
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness explicitly flags an untested discriminator: they "did not add NO blockers such as L-NAME to test whether" the relaxation "was NO-dependent," which leaves NO-dependence vs alternatives unresolved due to an unmeasured test. However, it does not explicitly record a blocked trial-specification slot/link or clearly identify the resolving experiment as such (it only contrasts with what they "instead did").

### A1-H3-R1 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: PARTIALLY_COVERS - Witness proposes mechanistic links for PTX ("phosphodiesterase inhibitor" and "nitric oxide synthase activator" increasing "NO" and "cGMP") to explain beneficial contractile effects after ischemic injury, which supports components of an H1-type rationale; it does not state that evidence is insufficient to distinguish therapeutic mechanism vs H2-type failure.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness says the authors "propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator" increasing "NO" and "cGMP" as mechanisms for beneficial contractile effects—this supports components of an H1-type mechanistic rationale, but does not address whether evidence is "not enough to distinguish" H1 from an H2-type failure.

### A1-H3-R1 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness only provides a definitional quote for detrusor underactivity (reduced strength/duration contraction leading to prolonged/incomplete emptying) and does not address PTX mechanistic evidence nor inability to discriminate mechanism vs failure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only quotes a definition of detrusor underactivity ("reduced strength and/or duration" leading to prolonged/incomplete emptying) and makes no claim about evidence supporting mechanistic components or inability to distinguish therapeutic mechanism from failure.

### A1-H3-R1 x W-FRD-Q0007-04-c1-Q0007
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: NO_SEMANTIC_RELATION - Witness reports hypotheses about afferent dysfunction in BOO/DU (receptor expression, urothelial ATP) with implications, but does not discuss PTX evidence or the specific synthesis claim about supporting some H1 components yet not distinguishing from H2-type failure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports that "recent findings" suggest afferent dysfunction in BOO/DU (muscarinic/P2X3 changes, diminished ATP), but it does not discuss PTX mechanistic rationale evidence nor whether evidence is insufficient to distinguish H1 vs H2-type failure.

### A1-H3-R1 x W-FRD-Q0007-04-c4-Q0007
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: NO_SEMANTIC_RELATION - Witness says markers are needed to avoid passing a "point of no return" to irreversible decompensation; it does not mention PTX mechanistic rationale evidence or uncertainty distinguishing therapeutic mechanism vs failure mode.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness says reliable bladder markers are needed to avoid a "point of no return" to irreversible decompensation; it does not address the evidentiary balance about H1 mechanistic rationale vs H2-type failure.

### A1-H3-R1 x W-FRD-Q0053-02-c4-Q0053
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: NO_SEMANTIC_RELATION - Talks about timing/generalizability of PFME questionnaire data in women after ≥6 weeks PFME; does not synthesize whether evidence supports parts of an H1 rationale yet cannot distinguish therapeutic mechanism vs H2-type failure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses PFME questionnaire timing (after "at least six weeks") and cautions about generalizing to other training stages; it contains no mechanistic-evidence synthesis about H1 components vs H2-type failure.

### A1-H3-R1 x W-FRD-Q0063-01-c1-Q0063
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Sullivan-et-al-1988: Human PMNs incubated 30 min at 37°C with pentoxifylline 300 µg/ml decreased adherence to nylon vs diluent: 64.1±2.7% (n=16) vs 54.0±3.9% (n=6; P=0.031) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → PMN adherence).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → PMN adherence (opening paragraph)
- Pass A: NO_SEMANTIC_RELATION - Reports an in-vitro finding (PTX 300 µg/ml reduces PMN adherence to nylon); does not address the meta-level claim that existing evidence supports some H1 links but is insufficient to discriminate mechanism vs failure.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R1 x W-FRD-Q0063-01-c4-Q0063
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: NO_SEMANTIC_RELATION - Reports PTX reducing FMLP-stimulated superoxide in PMNs; provides a mechanistic datapoint but no synthesis about evidence being insufficient to distinguish therapeutic mechanism from H2-type failure.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R1 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Reports PTX reducing LPS-MCM–enhanced lysozyme release in PMNs; does not claim that the overall evidence base supports some H1 components yet cannot discriminate against an H2-type failure.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R1 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - States dose-dependent effects (none up to 50 µmol/L; effect at 500 µmol/L) of PTX on neutrophil calcium transients; not a source-attributed synthesis about partial support and inability to distinguish H1 vs H2.
- Pass B: PARTIALLY_COVERS - The reported finding that PTX 'up to 50 µmol/L changed neither' Ca2+ but '500 µmol/L reduced' Ca2+ provides mechanistic evidence with limits, yet does not state that the evidence set is insufficient to distinguish a therapeutically consequential mechanism from H2-type failure.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R1 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Wystrychowski2014 'speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered'—a synthesis suggesting a failure mode/insufficient potency—but it does not also assert that existing evidence supports some H1 links while remaining unable to discriminate between H1 and H2.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R1 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Roberts1993 reports PTX 'up to 50 µmol/l did not change' Ca2+ responses, while '500 µmol/l reduced' them—evidence bearing on mechanism strength/limits—without concluding the evidence base cannot distinguish therapeutic mechanism from failure.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R1 x W-FRD-Q0092-04-delanian20-c1-Q0092
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Delanian 2005 reports “44 eligible treated women” with complete long-term data; “All 44 patients were women” (delanian2005.pdf.md, PATIENTS AND METHODS → Population).
- Source: delanian2005.pdf.md PATIENTS AND METHODS → Population
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The statement 'All 44 patients were women' is purely demographic and contains no mechanistic/pharmacological synthesis about PTX supporting-but-insufficient evidence.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R1 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - deSouza2009 only states an 'open-label, 24-week' trial of 'pentoxifylline 800 mg/day plus vitamin E'; it does not provide a synthesis about mechanistic evidence sufficiency/insufficiency.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only describes study logistics: '12 systemic-sclerosis patients' in an 'open-label, 24-week-per-patient trial' of 'pentoxifylline 800 mg/day plus vitamin E 800 UI/day'. It does not assess whether evidence supports mechanistic components or whether it is insufficient to distinguish H1 mechanism from H2-type failure.

### A1-H3-R1 x W-FRD-Q0098-01-Q0098
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The rat pilot shows PTX administration 'decreased MAP' and 'increased HR/WBC/PMN' and 'they all died'—mechanistic/physiologic observations—but it does not state that overall evidence supports some components yet remains unable to discriminate H1 therapeutic mechanism from H2-type failure.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports rat physiologic effects of IV PTX (e.g., 'decreased MAP', 'increased HR/WBC/PMN' and 'they all died'). The unit is about the state of 'existing evidence' being partially supportive yet insufficient to discriminate between mechanistic explanations (H1 vs H2); the witness does not make any evidence-synthesis or discrimination claim.

### A1-H3-R1 x W-FRD-Q0107-02-c4-Q0107
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Chung2014.pdf.md (Conclusions): Chung (2014) says post-void residual measurement may indicate underlying detrusor failure if BOO is excluded, but at present urodynamic study should be conducted to consolidate the diagnosis of UAB by functionally demonstrating the presence of DU.
- Source: chung2014.pdf.md Conclusions
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Chung (2014) discusses that urodynamic study 'should be conducted' to demonstrate DU for diagnosing UAB; no mention of pentoxifylline or H1/H2 mechanistic discrimination.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses diagnosis of UAB/DU ('urodynamic study should be conducted') and does not mention the H1 mechanistic rationale, H2-type failure, or evidentiary sufficiency about any mechanism.

### A1-H3-R1 x W-FRD-Q0131-03-c3-Q0131
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The claim 'PTX has short half-life about 1.6 h' supports a PK component of a mechanistic rationale but does not address (or conclude) that the evidence base cannot distinguish a consequential mechanism from a failure mode.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states only a pharmacokinetic fact: 'PTX has short half-life about 1.6 h'. The unit requires an evaluation that evidence supports some mechanistic components but is not enough to distinguish H1 vs H2-type failure, which is not addressed.

### A1-H3-R1 x W-FRD-Q0131-03-c4-Q0131
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The statement that 'PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion' provides one pharmacological/physiologic link (adverse hemodynamic effects) but does not synthesize that evidence is insufficient to distinguish therapeutic mechanism from H2-type failure.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a toxicity observation ('PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion'). This does not speak to whether the overall evidence base supports some H1 mechanistic components yet remains insufficient to distinguish a therapeutic mechanism from H2-type failure.

### A1-H3-R1 x W-FRD-Q0138-04-Q0138
- Unit (REQUIRED_SUPPORT): Existing evidence supports some components of the H1 mechanistic rationale, but not enough to distinguish a therapeutically consequential mechanism from the H2-type failure.
- Witness: nihms496647.pdf.md (“Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome”): unpublished extended data using proposed criteria: among 132 patients enrolled and referred for suspected or confirmed disease over four years, 58 met WHO systemic mastocytosis criteria, 7 MMAS, 19 IA; 42 had mast cell activation symptoms without evidence of clonal mast cells; 6 had unrelated diagnoses.
- Source: nihms496647.pdf.md Section: “Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome” (paragraph beginning “Using the approach outlined above…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports proportions meeting WHO systemic mastocytosis/MMAS/IA criteria among 132 referred patients; it does not mention pentoxifylline, mechanisms, or inability to distinguish H1 vs H2.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports proportions of patients meeting mastocytosis-related diagnostic categories (e.g., '58 met WHO systemic mastocytosis criteria...'). It is unrelated to the unit’s claim about mechanistic-evidence sufficiency and distinguishing H1 vs H2-type failure.

### A1-H3-R2 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - This witness proposes mechanisms for PTX’s beneficial effects ("phosphodiesterase inhibitor and nitric oxide synthase activator"), but it does not state that any trial-specification slot (intervention/exposure, phenotype, measurement, comparator) cannot be specified due to an unresolved decisive link.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only proposes mechanisms for PTX’s beneficial effects (“phosphodiesterase inhibitor and nitric oxide synthase activator… increases tissue NO and intracellular cGMP”) and does not state that any trial-specification slot (intervention/exposure, phenotype, measurement, comparator) cannot be specified due to an unresolved decisive link.

### A1-H3-R2 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - The witness reports a specific experimental pattern (improved electric stimulation responses but not carbachol) and an assumed pathway implication, but it does not conclude that trial-specification elements are non-defensible to specify because a decisive link remains unresolved.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports an experimental pattern (PTX improved responses to “electric stimulation” but not “carbachol”) and an inferred pathway (“assumed…not via cholinergic nerves”), but it does not claim that a decisive link remains unresolved such that any trial-specification slot cannot be specified from supported premises.

### A1-H3-R2 x W-FRD-Q0005-04-c2-Q0005
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In han1990.pdf.md (Materials and Methods—CAT Assay), the authors state that the CAT assay “was performed according to the thin-layer chromatography method of Gorman et al. (9).”
- Source: han1990.pdf.md Materials and Methods — CAT Assay
- Pass A: NO_SEMANTIC_RELATION - The witness only states a procedural detail about how a CAT assay was performed ("according to... Gorman et al."), with no claim about unresolved causal links preventing specification of intervention/phenotype/measurement/comparator.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness is purely a methods citation (“CAT assay was performed according to… Gorman et al.”) and contains no statement about unresolved links preventing specification of intervention/exposure, phenotype, measurement, or comparator.

### A1-H3-R2 x W-FRD-Q0006-04-c1-Q0006
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: NO_SEMANTIC_RELATION - This witness says they did not add NO blockers like L-NAME to test NO-dependence, but it does not connect that omission to an inability to specify any trial-design slot from supported premises due to an unresolved decisive link.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness says they “did not add NO blockers such as L-NAME” to test NO-dependence and instead tested endothelium dependence by denudation; it does not assert that trial-specification slots cannot be specified because a decisive link remains unresolved.

### A1-H3-R2 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - The witness provides a definition of detrusor underactivity from ICS; it does not state that phenotype/measurement/comparator/intervention cannot be specified because a decisive link remains unresolved.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0007-03-Q0007
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - The witness reports findings in men with DU and BPH (urothelial ATP decreased, NO unchanged), but it does not assert that any trial-specification slot is non-defensible to specify due to an unresolved link.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0007-04-c1-Q0007
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: NO_SEMANTIC_RELATION - The witness suggests afferent dysfunction "may play a role" and has diagnostic/therapeutic implications, but it does not state that trial-specification cannot be completed (any of the four slots) because a decisive link remains unresolved.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0007-04-c4-Q0007
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: NO_SEMANTIC_RELATION - The witness says reliable bladder markers are urgently needed to avoid a "point of no return," but it does not explicitly conclude that measurement (or any other slot) cannot be specified from supported premises due to a named unresolved causal link.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0009-02-c2-Q0009
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Chuang2015.pdf.md (## EPIDEMIOLOGY) summarizes Abarbanel & Marcus: in 181 LUTS patients aged ≥70 (82 men, 99 women), impaired detrusor contractility was defined urodynamically as Qmax <10 mL/s plus detrusor pressure <30 cm H2O, and was reported in 48% of men and 12% of women.
- Source: chuang2015.pdf.md ## EPIDEMIOLOGY (paragraph beginning “In men, detrusor underactivity may be caused… Abarbanel and Marcus…”)
- Pass A: NO_SEMANTIC_RELATION - This witness gives an epidemiologic definition and prevalence of impaired detrusor contractility (Qmax and detrusor pressure thresholds), not a conclusion that trial design slots cannot be specified because a decisive link is unresolved.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0010-03-Q0010
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, Figure 2 (“Figure 2. The percentage of referrals made for PFPT by diagnosis”), PFPT referral percentages by diagnosis are: Pelvic Floor Dysfunction 49.5%, CPPS 39.6%, Testicular Pain/Groin Pain 28.4%, LUTS 3.6%; the denominator is not stated.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18, Figure 2 ("Figure 2. The percentage of referrals made for PFPT by diagnosis"), including the table "Diagnosis | Percentage of Patients Referred"
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness provides referral percentages (e.g., “Pelvic Floor Dysfunction 49.5%… LUTS 3.6%”) and notes denominator not stated. It does not assert trial-design indeterminacy from unresolved causal links.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0010-04-c1-Q0010
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states the study “report a retrospective chart review… identified using ICD codes…” with dates. No claim that any trial-specification slot cannot be specified or that any decisive link is unresolved.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness says diagnosing pseudodyssynergia required “private-setting uroflowmetry… intended to minimize false-positive results.” This is about measurement procedure validity, not an unresolved link that blocks specifying phenotype/measurement/comparator/intervention for a trial.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0013-03-c3-Q0013
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Kaplan1997 (kaplan1997.pdf.md, MATERIALS AND METHODS [definitions paragraph]) defined detrusor instability as a nonvolitional, phasic detrusor-pressure increase of at least 15 cm water, or a detrusor-pressure increase associated with increased sensation of urgency.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only provides a definition: “defined detrusor instability as… at least 15 cm water… or… urgency.” It does not discuss inability to specify any trial design slot or any unresolved causal link preventing specification.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only states a definitional criterion: “defined detrusor instability as… at least 15 cm water… or… urgency.” It does not say any trial-specification slot (intervention/exposure, phenotype, measurement, comparator) cannot be specified due to an “unresolved” decisive link.

### A1-H3-R2 x W-FRD-Q0013-03-c4-Q0013
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness only defines bladder outlet obstruction using specific urodynamic/radiographic criteria; it does not state that any trial-specification slot (intervention/exposure, phenotype, measurement, comparator) cannot be specified due to an unresolved decisive link.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The text merely defines “bladder outlet obstruction” using thresholds (“>45 cm water… <12 ml/s… radiographic evidence”) and does not assert an inability to specify any trial-design slot from supported premises or that a decisive link remains unresolved.

### A1-H3-R2 x W-FRD-Q0015-04-c2-Q0015
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Osman2018 (osman2018.pdf.md, “Diagnostic aspects > Detrusor contraction strength > 2. Projected isovolumetric pressure (PIP)”) provides a PIP calculation formula (K varies by population/sex; usually 5 in men) and suggested contractility groupings: >150 strong, 100–150 normal, 50–100 weak, <50 very weak; these formulae may overestimate PIP and have less test–retest reliability than direct isovolumetric measurement.
- Source: osman2018.pdf.md ## Diagnostic aspects > ### Detrusor contraction strength > #### 2. Projected isovolumetric pressure (PIP)
- Pass A: PARTIALLY_COVERS - Witness notes PIP contractility groupings and that the formulae "may overestimate PIP" and have lower test–retest reliability than direct measurement, which partially supports difficulty/uncertainty in specifying a measurement; it does not conclude that a trial slot cannot be specified from supported premises because a decisive causal link remains unresolved.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Although it notes PIP formulae “may overestimate PIP” and have “less test–retest reliability,” the witness does not claim that any of the four trial-specification slots cannot be specified from supported premises because a decisive link is unresolved.

### A1-H3-R2 x W-FRD-Q0018-01-Q0018
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Bortnick et al. 2020 says surgical therapy is recommended for recurrent UTIs secondary to BPH, renal insufficiency secondary to BPH, recurrent bladder stones or gross hematuria from BOO due to BPH, refractory urinary retention secondary to BPH, and/or LUTS that have failed or unwillingness to consider other therapies (bortnick2020.pdf.md, “Alternative minimally invasive/surgical procedures to TURP”).
- Source: bortnick2020.pdf.md Section: “Alternative minimally invasive/surgical procedures to TURP” (paragraph beginning “Overall, surgical therapy is recommended…”)
- Pass A: NO_SEMANTIC_RELATION - Witness provides clinical recommendations for when surgical therapy is recommended in BPH-related conditions; it does not address inability to specify trial intervention/exposure, phenotype, measurement, or comparator due to unresolved links.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness gives clinical recommendations (“surgical therapy is recommended for…”) but does not discuss missing premises or an unresolved decisive link preventing specification of intervention/exposure, phenotype, measurement, or comparator.

### A1-H3-R2 x W-FRD-Q0020-02-c1-Q0020
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness describes a pentoxifylline dosing schedule in healthy volunteers and notes lack of explicit crossover; it does not claim that trial-specification slots are non-defensible due to unresolved decisive links.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0053-02-c4-Q0053
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: NO_SEMANTIC_RELATION - Witness states questionnaires were completed after ≥6 weeks PFME and cautions generalization to other PFME stages; it does not claim inability to specify trial slots from supported premises due to an unresolved decisive link.
- Pass B: PARTIALLY_COVERS - The witness explicitly flags a limitation (“findings should be generalized cautiously to women at different stages of PFME training”), which relates to uncertainty in specifying phenotype/exposure timing/measurement generalizability, but it does not assert that a decisive unresolved causal link makes a trial-specification slot non-defensible.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0131-04-Q0131
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: Bortnick2019.pdf.md (Review of Medications > Alpha Blockers) reports FORTA for men >65: silodosin and tamsulosin are “caution” because no older-adult efficacy/safety data and hypotension risk, especially with other antihypertensive medications; alfuzosin, doxazosin, and terazosin are “avoid” due to orthostatic hypotension, vasodilatory effects, cardiac arrhythmias, and syncope.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: NO_SEMANTIC_RELATION - Witness reports FORTA categorizations and cautions/avoidance of specific alpha blockers in men >65; it does not state any unresolved decisive link preventing specification of intervention, phenotype, measurement, or comparator.
- Pass B: PARTIALLY_COVERS - The witness notes an evidence gap (“no older-adult efficacy/safety data” and “hypotension risk”), which could contribute to uncertainty about intervention choice, but it does not state that after reviewing supported premises a specific trial-specification slot is non-defensible due to a decisive unresolved causal link.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R2 x W-FRD-Q0138-04-Q0138
- Unit (REQUIRED_SUPPORT): At least one of the four trial-specification slots cannot be specified from supported premises because a decisive link remains unresolved (intervention/exposure, phenotype, measurement, or comparator).
- Witness: nihms496647.pdf.md (“Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome”): unpublished extended data using proposed criteria: among 132 patients enrolled and referred for suspected or confirmed disease over four years, 58 met WHO systemic mastocytosis criteria, 7 MMAS, 19 IA; 42 had mast cell activation symptoms without evidence of clonal mast cells; 6 had unrelated diagnoses.
- Source: nihms496647.pdf.md Section: “Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome” (paragraph beginning “Using the approach outlined above…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about mast cell activation syndrome criteria and enrollment breakdown (“58 met WHO… 42 had symptoms without evidence of clonal mast cells”), not about inability to specify intervention/phenotype/measurement/comparator for the hypothesized BPH-related trial.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness proposes specific PTX mechanisms ("phosphodiesterase inhibitor and nitric oxide synthase activator"), but does not state that uncertainty is localized to unresolved links nor that evidence is insufficient to endorse or reject the mechanism.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness says the authors “propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator… offered as mechanisms,” but does not state that uncertainty is localized to specific links or that neither mechanistic endorsement nor rejection is determined.

### A1-H3-R3 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: PARTIALLY_COVERS - Witness identifies a specific mechanistic link that is unlikely ("did not improve responses to carbachol" → assumed "not via cholinergic nerves"), and suggests alternative pathways (purinergic/NANC), but it does not explicitly frame uncertainty as localized unresolved links while also stating neither mechanistic endorsement nor rejection is determined.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports PTX “did not improve responses to carbachol” and therefore they “assumed… not via cholinergic nerves” and instead “related to purinergic or other” pathways, which localizes uncertainty to particular mechanistic pathways without explicitly stating that neither H1 nor H2 is determined.

### A1-H3-R3 x W-FRD-Q0005-04-c2-Q0005
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: In han1990.pdf.md (Materials and Methods—CAT Assay), the authors state that the CAT assay “was performed according to the thin-layer chromatography method of Gorman et al. (9).”
- Source: han1990.pdf.md Materials and Methods — CAT Assay
- Pass A: NO_SEMANTIC_RELATION - Witness only states a methods detail about how a CAT assay was performed ("according to... Gorman et al."), with no content about localized uncertainty or indeterminate mechanistic endorsement/rejection.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0006-04-c1-Q0006
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: PARTIALLY_COVERS - Witness explicitly names an unresolved mechanistic test (they "did not add NO blockers such as L-NAME" to test NO-dependence), which localizes uncertainty to the NO-dependence link, but it does not also state that neither mechanistic go-ahead (H1) nor mechanistic defeat (H2) is determined.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness provides a definition of detrusor underactivity from ICS, not an explicit statement about localized uncertainty in identified causal links or indeterminate mechanistic endorsement/rejection.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0007-03-Q0007
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports empirical findings (ATP decreased; NO no significant change) in a specific population, but does not state that uncertainty is localized to unresolved links or that neither mechanistic endorsement nor rejection is determined.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0007-04-c1-Q0007
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: PARTIALLY_COVERS - Witness proposes possible mechanisms with uncertainty markers ("suggest afferent dysfunction... may play a role"), which gestures to localized candidate links, but it does not explicitly state that evidence warrants neither mechanistic endorsement (H1) nor mechanistic rejection (H2).
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0009-02-c2-Q0009
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: Chuang2015.pdf.md (## EPIDEMIOLOGY) summarizes Abarbanel & Marcus: in 181 LUTS patients aged ≥70 (82 men, 99 women), impaired detrusor contractility was defined urodynamically as Qmax <10 mL/s plus detrusor pressure <30 cm H2O, and was reported in 48% of men and 12% of women.
- Source: chuang2015.pdf.md ## EPIDEMIOLOGY (paragraph beginning “In men, detrusor underactivity may be caused… Abarbanel and Marcus…”)
- Pass A: NO_SEMANTIC_RELATION - Witness provides epidemiologic prevalence/definition statistics for impaired detrusor contractility, without any statement about localized mechanistic uncertainty or inability to endorse/reject a mechanism.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0010-03-Q0010
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, Figure 2 (“Figure 2. The percentage of referrals made for PFPT by diagnosis”), PFPT referral percentages by diagnosis are: Pelvic Floor Dysfunction 49.5%, CPPS 39.6%, Testicular Pain/Groin Pain 28.4%, LUTS 3.6%; the denominator is not stated.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18, Figure 2 ("Figure 2. The percentage of referrals made for PFPT by diagnosis"), including the table "Diagnosis | Percentage of Patients Referred"
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only provides 'PFPT referral percentages by diagnosis' and does not address uncertainty, causal links, or mechanistic endorsement/rejection.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0010-04-c1-Q0010
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness describes study design ('retrospective chart review' and ICD codes for BPH/OAB/LUTS/etc.) without any statement about mechanistic uncertainty or specific unresolved causal links.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports a diagnostic requirement to 'minimize false-positive results' from 'performance anxiety'/'bashful voiding' and does not name unresolved causal links or state that evidence cannot determine mechanistic endorsement vs rejection.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R3 x W-FRD-Q0013-03-c3-Q0013
- Unit (REQUIRED_SUPPORT): The uncertainty is localized to identified links (not diffuse), and neither mechanistic endorsement (H1) nor mechanistic rejection (H2) is determined.
- Witness: Kaplan1997 (kaplan1997.pdf.md, MATERIALS AND METHODS [definitions paragraph]) defined detrusor instability as a nonvolitional, phasic detrusor-pressure increase of at least 15 cm water, or a detrusor-pressure increase associated with increased sensation of urgency.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only 'defined detrusor instability' with pressure criteria (≥15 cm water or associated with urgency) and does not discuss uncertainty, unresolved causal links, or any mechanistic go-ahead/defeat.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R4 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness proposes PTX mechanisms (PDE inhibition/NOS activation) to explain beneficial effects after ischemic injury, but does not assess whether unresolved links block designing a targeted clinical trial or failing a trial-specification test.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses proposed PTX mechanisms (“phosphodiesterase inhibitor and nitric oxide synthase activator… increases tissue NO and intracellular cGMP”) to explain beneficial effects after ischemic injury, but does not address “unresolved links” preventing a rationale from being “specific enough” to design a targeted clinical trial under a trial-specification test.

### A1-H3-R4 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX effects on detrusor contractions and an assumed non-cholinergic pathway; it does not state that unresolved links prevent specifying intervention/exposure, phenotype/measurement/comparator for trial design under a trial-specification test.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX effects on detrusor contractions and an inference about mechanism (“assumed… not via cholinergic nerves… related to purinergic or other… pathways”), but makes no claim about inability to specify/design a targeted clinical trial or failure of any “trial-specification test.”

### A1-H3-R4 x W-FRD-Q0005-04-c2-Q0005
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: In han1990.pdf.md (Materials and Methods—CAT Assay), the authors state that the CAT assay “was performed according to the thin-layer chromatography method of Gorman et al. (9).”
- Source: han1990.pdf.md Materials and Methods — CAT Assay
- Pass A: NO_SEMANTIC_RELATION - Witness only states the CAT assay followed a cited TLC method; it contains no assessment about unresolved links or inability to design a specific targeted clinical trial.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states a lab method (“CAT assay was performed according to… Gorman et al.”) and contains nothing about unresolved links, rationale specificity, or clinical trial design constraints.

### A1-H3-R4 x W-FRD-Q0006-04-c1-Q0006
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: NO_SEMANTIC_RELATION - Witness notes they did not use NO blockers (e.g., L-NAME) to test NO-dependence of pentoxifylline-induced relaxation; this is a methodological limitation but not an attributed judgment that identified unresolved links prevent satisfying a trial-specification test for targeted trial design.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness notes a specific experimental choice/omission (“did not add NO blockers such as L-NAME… instead… denuding vascular endothelial cells”) about an in vitro study, but does not state that unresolved links prevent designing a targeted clinical trial or that a trial-specification test cannot be met.

### A1-H3-R4 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness provides the ICS definition of detrusor underactivity; it does not claim that unresolved links block clinical trial specification or that a trial-specification test cannot be satisfied.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides a definitional quote of detrusor underactivity (“contraction of reduced strength… resulting in… failure to achieve complete bladder emptying…”), with no mention of unresolved links or inability to design a targeted clinical trial.

### A1-H3-R4 x W-FRD-Q0007-03-Q0007
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports findings in men with DU and BPH (ATP decreased; NO no significant change) without any assessment that unresolved links prevent designing a targeted clinical trial or meeting a trial-specification test.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports observational findings (“urothelial ATP… significantly decreased… nitric oxide… no significant change”) in men with DU and BPH, but does not discuss trial-design specificity or claim that unresolved links block targeted clinical trial design under a trial-specification test.

### A1-H3-R4 x W-FRD-Q0010-04-c1-Q0010
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only reports a 'retrospective chart review' and how patients were 'identified using ICD codes'; it contains no evaluation about unresolved mechanistic links or trial-specification test failure.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R4 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports that diagnosing pseudodyssynergia 'required private-setting uroflowmetry' to minimize 'false-positive results'; no claim that unresolved links prevent specifying intervention/exposure/phenotype/measurement/comparator for a trial.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A1-H3-R4 x W-FRD-Q0013-03-c3-Q0013
- Unit (REQUIRED_SUPPORT): The unresolved links prevent the rationale from becoming specific enough to design the targeted clinical trial under the trial-specification test.
- Witness: Kaplan1997 (kaplan1997.pdf.md, MATERIALS AND METHODS [definitions paragraph]) defined detrusor instability as a nonvolitional, phasic detrusor-pressure increase of at least 15 cm water, or a detrusor-pressure increase associated with increased sensation of urgency.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only states Kaplan1997 'defined detrusor instability as...' with specific diagnostic criteria; it does not discuss unresolved links, rationale specificity, or inability to design a targeted clinical trial.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H1-A1 x W-FRD-Q0089-04-c2-Q0089
- Unit (ADVERSE_TEST): Findings against this hypothesis include no early functional change at informative exposures, benefit only after prolonged treatment in humans, or a route that requires structural change before function can improve.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Speculates PTX may be too weak to suppress ongoing inflammation once triggered; does not provide a result showing no early functional improvement at informative exposures, delayed-only human benefit, or a structural-change-first route to functional improvement.
- Pass B: PARTIALLY_COVERS - The witness is explicitly speculative (“speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered… too weak to suppress…”) and does not report timing of voiding improvement, but it aligns directionally with an argument against rapid functional benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The unit concerns evidence against a hypothesis such as “no early functional change at informative exposures,” “benefit only after prolonged treatment in humans,” or a “route that requires structural change before function can improve.” The witness only “speculates” that pentoxifylline “may have no potent anti-inflammatory effect once inflammation has been triggered” and is “too weak to suppress” an ongoing cascade, without reporting early vs prolonged functional outcomes, exposure informativeness, or any structural-change-first route.

### A2-H1-A1 x W-FRD-Q0090-04-c3-Q0090
- Unit (ADVERSE_TEST): Findings against this hypothesis include no early functional change at informative exposures, benefit only after prolonged treatment in humans, or a route that requires structural change before function can improve.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Reports PTX effects on neutrophil calcium transients at specific micromolar concentrations; does not address urinary functional improvement timing in humans or necessity of prior structural change.
- Pass B: PARTIALLY_COVERS - The witness shows no cellular functional effect “up to 50 µmol/l” with effect only at “500 µmol/l,” which is suggestive of needing high exposure, but it is neutrophil [Ca2+]i rather than human voiding function/early clinical response, so it only partially maps to “no early functional change at informative exposures.”
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports neutrophil intracellular calcium results: PTX “up to 50 µmol/l did not change” [Ca2+]i and “500 µmol/l reduced” it, which is a cellular/mechanistic assay in purified neutrophils. The unit is about (lack of) early functional change at informative exposures, delayed-only human benefit, or structural change preceding functional improvement; none of these clinical/timing/route claims are addressed by the neutrophil [Ca2+]i finding.

### A2-H1-C1 x W-FRD-Q0003-04-c3-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: PARTIALLY_COVERS - Witness reports PTX improved detrusor contractions to electric stimulation in an obstructed bladder model and proposes a functional (non-cholinergic) pathway; this suggests a modifiable functional component, but it is not explicitly in the cohort under consideration.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness says PTX "improved detrusor contractions to electric stimulation" in an "obstructed bladder" model and discusses a non-cholinergic functional pathway; this supports existence of a modifiable functional component, but not explicitly "in this cohort" referenced by the unit.

### A2-H1-C1 x W-FRD-Q0007-01-c1-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - This is only a definitional quote of detrusor underactivity (reduced strength/duration causing prolonged/incomplete emptying) and does not address whether an impaired-voiding component is modifiable or functional in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only quotes the ICS definition of detrusor underactivity ("contraction of reduced strength and/or duration") and does not state that impaired voiding is present-and-modifiable in any cohort.

### A2-H1-C1 x W-FRD-Q0007-03-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: PARTIALLY_COVERS - Witness reports decreased urothelial ATP (and unchanged NO) in men with DU+BPH, indicating a physiological signaling abnormality, but does not state it is modifiable or reversible in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports in men with DU+BPH that "urothelial ATP was significantly decreased" (physiologic dysfunction), but does not say this impaired voiding component is "modifiable" or reversible in the cohort.

### A2-H1-C1 x W-FRD-Q0007-04-c1-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: WITNESS_ENTAILS_UNIT - Witness states in BOO that afferent dysfunction (altered receptor expression or diminished urothelial ATP) may contribute to 'initial and reversible stages of DU,' directly asserting a functional contributor that is modifiable/reversible in the relevant DU/BOO context.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states afferent dysfunction "may play a role" in "initial and reversible stages of DU" (suggesting potential modifiability), but it is framed as suggestive/diagnostic/therapeutic implications rather than asserting that a modifiable functional component "must be present" in the unit’s cohort.

### A2-H1-C1 x W-FRD-Q0009-02-c2-Q0009
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: Chuang2015.pdf.md (## EPIDEMIOLOGY) summarizes Abarbanel & Marcus: in 181 LUTS patients aged ≥70 (82 men, 99 women), impaired detrusor contractility was defined urodynamically as Qmax <10 mL/s plus detrusor pressure <30 cm H2O, and was reported in 48% of men and 12% of women.
- Source: chuang2015.pdf.md ## EPIDEMIOLOGY (paragraph beginning “In men, detrusor underactivity may be caused… Abarbanel and Marcus…”)
- Pass A: NO_SEMANTIC_RELATION - This is prevalence/definition of impaired detrusor contractility in an elderly LUTS population (percent with DU by sex) and does not speak to modifiability or a functional vs fixed structural component.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness gives epidemiologic prevalence/definition (e.g., "reported in 48% of men") and does not address whether impaired voiding is functionally modifiable in the cohort.

### A2-H1-C1 x W-FRD-Q0013-03-c6-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), patients were considered to have an acontractile detrusor if they had no detrusor contraction during pressure-flow analysis and were unable to generate an uncatheterized urine flow (in private).
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness provides a definitional criterion (“no detrusor contraction…unable to generate…flow”), without any claim about reversibility/modifiability of impaired voiding.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides only a definition/criterion for acontractile detrusor ("no detrusor contraction" and "unable to generate...flow"), not modifiability of impaired voiding.

### A2-H1-C1 x W-FRD-Q0014-02-Q0014
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness says ultrasound DWT ≤1.23 mm plus capacity >445 ml can “detect”/“predict DU” (PPV/NPV) and “could replace pressure-flow studies,” but does not address whether impaired voiding is functionally modifiable.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about noninvasive detection/prediction of DU ("can safely...detect"; "predict DU" with PPV/NPV) and does not state a functional component of impaired voiding is present and modifiable.

### A2-H1-C1 x W-FRD-Q0027-01-c3-Q0027
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): According to Osman et al. [4] review, DU was reported in 9%–28% of men aged <50 years, 48% of men aged >70 years, and 12%–45% of women aged >70 years.
- Source: 2020ICU_icu-58-S68.pdf.md PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (paragraph beginning 'According to the recent review from Osman et al. [4], ...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only reports that “DU was reported in 9%–28%…48%…12%–45%” by age/sex groups; it makes no claim about modifiability or functional mechanism.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports only prevalence ranges of DU by age/sex ("DU was reported in 9%–28%...") and makes no claim about modifiability or functional mechanisms in a cohort.

### A2-H1-C1 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports proportions with DU, delayed first voiding sense, and increased bladder capacity in “52 men with diabetes…with LUTS,” but does not state anything about modifiability or a functional vs fixed structural contributor.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness lists proportions of DU and sensory/capacity findings in "52 men with diabetes" but does not indicate that impaired voiding is modifiable or that a modifiable functional component must be present.

### A2-H1-C1 x W-FRD-Q0034-04-bortnick20-c1-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: bortnick2020.pdf.md (“Medical therapy”→“Combination therapy” MTOPS paragraph) reports MTOPS studied finasteride+doxazosin in 3000 men (mean age 62.6 years, SD 7.3) and found combination therapy improved voiding symptoms and maximum urinary flow rate more than either alone, prevented BPH progression better, and reduced the long-term risk of acute urinary retention and need for invasive therapy.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (MTOPS paragraph)
- Pass A: PARTIALLY_COVERS - Reports that combination medical therapy (finasteride+doxazosin) in men with BPH improved voiding symptoms and maximum urinary flow rate vs either alone, implying impaired voiding can be modified via pharmacologic (functional) effects; but the cohort is BPH and the mechanism includes structural prostate shrinkage (finasteride), not strictly a modifiable functional component in the target cohort.
- Pass B: NO_SEMANTIC_RELATION - Although it reports symptom/Qmax improvement in BPH (“improved voiding symptoms and maximum urinary flow rate”), it pertains to BPH management and does not specifically support the unit’s claim about a modifiable functional component in the cohort relevant to A2-H1 (PTX/underactive bladder mechanism).
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports MTOPS combination therapy "improved voiding symptoms and maximum urinary flow rate" showing impaired voiding can be modified, but it is in BPH management (finasteride+doxazosin) and does not establish the required modifiable functional component in the unit’s cohort.

### A2-H1-C1 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: PARTIALLY_COVERS - States combination therapy in CombAT reduced AUR/surgery and clinical progression more than monotherapy, showing symptoms/progression are modifiable with medication; however it is about BPH management (different cohort) and does not specifically establish a modifiable functional (non-structural) contributor in the unit’s cohort.
- Pass B: NO_SEMANTIC_RELATION - The witness addresses BPH clinical progression and retention/surgery risk reduction in CombAT, not whether impaired voiding in the unit’s cohort has a modifiable functional component (and is largely about BPH disease progression).
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports CombAT combination therapy reduced risk of AUR/surgery and clinical progression (modifiability of voiding-related outcomes), but this is BPH-focused and does not directly support that a modifiable functional component "must be present" in the unit’s cohort.

### A2-H1-C1 x W-FRD-Q0061-02-c5-Q0061
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: In siu2003.pdf.md (Abstract (Results)), the authors report the pelvic muscle training program “appears to be able to reduce the overall urinary incontinence episodes by 85.2%.”
- Source: siu2003.pdf.md Abstract (Results)
- Pass A: NO_SEMANTIC_RELATION - Pelvic muscle training is reported to reduce urinary incontinence episodes, which concerns incontinence frequency rather than impaired voiding/retention and does not address a functional component of impaired voiding in the specified cohort.
- Pass B: PARTIALLY_COVERS - The witness indicates urinary symptoms can be modified via functional intervention (“pelvic muscle training… reduce… incontinence episodes by 85.2%”), supporting modifiability of a functional component, but it concerns incontinence (not impaired voiding/UAB cohort specifically) and does not match the cohort/scope required.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness says pelvic muscle training reduced "urinary incontinence episodes"; it does not address impaired voiding/underactive bladder or a modifiable functional component of impaired voiding in the relevant cohort.

### A2-H1-C1 x W-FRD-Q0095-02-c1-Q0095
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: Ladi-Seyedian2017 (ladi-seyedian2017.pdf.md, “5. Diagnosis”) reports suggested UAB diagnostic parameters: Qmax <12 ml/s; Pdet at Qmax <30 mmH2O; bladder contractility index (PdetQmax + 5Qmax) <100; and bladder outlet obstruction index (PdetQmax − 2Qmax) <20.
- Source: ladi-seyedian2017.pdf.md Section 5. Diagnosis
- Pass A: NO_SEMANTIC_RELATION - Lists suggested diagnostic parameters for underactive bladder (e.g., Qmax, PdetQmax, indices), which define/diagnose functional impairment but do not state that a modifiable functional component exists in the cohort.
- Pass B: PARTIALLY_COVERS - The parameters include functional urodynamic measures (e.g., “Pdet at Qmax <30… BCI <100… BOOI <20”), which align with a functional voiding impairment construct, but they do not claim the impairment is modifiable in this cohort.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only "reports suggested UAB diagnostic parameters" (e.g., "Qmax <12 ml/s", "Pdet at Qmax <30 mmH2O", "BCI <100", "BOOI <20"). It does not state that, in the cohort, impaired voiding is present (as an observed cohort property) nor that any functional component is "modifiable."

### A2-H1-C1 x W-FRD-Q0148-01-c1-Q0148
- Unit (CONTEXTUAL_CONSTRAINT): A functional component of impaired voiding must be present and modifiable in this cohort.
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: PARTIALLY_COVERS - Reports that after long-term follow-up TURP patients had no significant LUTS or voiding-parameter improvement vs preoperative status, suggesting lack of durable modification via a structural intervention; but it does not negate the existence of a modifiable functional component in the cohort (and is specific to TURP-treated BPH), so it is not a direct contradiction.
- Pass B: NO_SEMANTIC_RELATION - The witness is about lack of change after TURP over ~10+ years (“no significant LUTS improvement… no significant change… including BCI”) and does not address whether a modifiable functional component is present in the cohort relevant to PTX/functional mechanism.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness says that after long-term follow-up "patients with TURP showed no significant LUTS improvement" and "no significant change ... in Qmax, PVR, voiding efficiency ... including BCI" versus preoperative status. This addresses a lack of measured improvement after TURP, not the unit's requirement that a "functional component of impaired voiding" is "present and modifiable" in the cohort.

### A2-H1-C2 x W-FRD-Q0003-04-c3-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): Clinically attainable exposure must reach the relevant tissue quickly enough to act within the days-to-weeks window.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports functional effects of PTX on detrusor responses and speculates on neural pathways, but does not address exposure levels being clinically attainable nor the timescale of tissue reaching/acting within days-to-weeks.
- Pass B: PARTIALLY_COVERS - The witness says “PTX improved detrusor contractions to electric stimulation in obstructed bladder,” indicating functional effects on contractility, but provides no statement that clinically attainable dosing achieves relevant tissue levels quickly or that effects occur within days-to-weeks.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness discusses that “PTX improved detrusor contractions” and speculates about “purinergic or other…pathways,” but says nothing about “clinically attainable exposure,” reaching “relevant tissue,” speed (“quickly enough”), or an action window of “days-to-weeks.”

### A2-H1-C2 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (CONTEXTUAL_CONSTRAINT): Clinically attainable exposure must reach the relevant tissue quickly enough to act within the days-to-weeks window.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: PARTIALLY_COVERS - Witness describes an open-label 24-week study with PTX 800 mg/day, showing a clinically used dosing regimen over weeks, but does not state that exposure reaches the relevant tissue quickly enough or that effects occur within days-to-weeks (it only provides study duration).
- Pass B: NO_SEMANTIC_RELATION - Witness describes an “open-label, 24-week-per-patient trial” with PTX “800 mg/day,” but provides no statement that exposure reaches the relevant tissue quickly or that effects occur within “days-to-weeks.”
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only reports an “open-label 24-week” trial and dosing “pentoxifylline 800 mg/day,” which does not state or imply that clinically attainable exposure reaches the relevant tissue “quickly enough” or that it acts within a “days-to-weeks” window.

### A2-H1-R1 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: PARTIALLY_COVERS - Witness describes a proposed functional mechanism ("phosphodiesterase inhibitor and nitric oxide synthase activator" increasing "NO" and "cGMP") affecting "contractile function," which aligns with acting on current physiological function; but it is speculative ("propose") and in a different context (cardiac papillary muscle after ischemic injury), not specifically improved voiding in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness says the authors "propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator" increasing "NO" and "cGMP" to explain "beneficial effects on contractile function"—a current-function mechanism; but it is explicitly speculative ("propose") and framed for "cardiac papillary muscle" after ischemic injury rather than improved voiding in the cohort or an explicit contrast against structural tissue change.

### A2-H1-R1 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: PARTIALLY_COVERS - Witness reports PTX "improved detrusor contractions to electric stimulation" (a functional physiological effect) and discusses neural pathway involvement (not via "cholinergic nerves"), supporting function-based action; however it is in an obstructed-bladder model and does not directly establish the mechanism for improved voiding in the target cohort nor explicitly contrasts against structural tissue change.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports PTX "improved detrusor contractions to electric stimulation" and discusses presumed pathway involvement ("not via cholinergic nerves"; possibly "purinergic or other"), which supports action on physiological function; but it is in an "obstructed bladder" context and does not itself establish that the cohort’s improved voiding is via current function rather than tissue structure.

### A2-H1-R1 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns diagnostic criteria for pseudodyssynergia using uroflowmetry patterns and does not mention PTX or a mechanism of improved voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns diagnostic uroflowmetry patterns for "pseudodyssynergia" and minimizing "bashful voiding" artifacts; it does not mention PTX or any mechanism for improved voiding via function vs tissue structure.

### A2-H1-R1 x W-FRD-Q0014-02-Q0014
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: NO_SEMANTIC_RELATION - Witness is about ultrasound detrusor wall thickness and bladder capacity to detect detrusor underactivity, not about PTX mechanisms or functional vs structural effects of PTX.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses ultrasound detrusor wall thickness and bladder capacity to "detect detrusor underactivity" and potentially replace pressure-flow studies; it does not address PTX or a mechanism acting on current physiological voiding function vs structural change.

### A2-H1-R1 x W-FRD-Q0019-02-Q0019
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: NO_SEMANTIC_RELATION - Witness provides clinically attainable plasma concentration ranges for PTX/metabolites ("<5 μmol/l"; combined "unlikely to exceed 10 μmol/l") but does not state any mechanism for improved voiding or distinguish functional vs structural action.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only gives clinically attained PTX/metabolite levels ("peak plasma" "<5 μmol/l"; combined "unlikely to exceed 10 μmol/l") and makes no claim about improved voiding mechanism or functional-vs-structural action.

### A2-H1-R1 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX at "5 µmol/l" inhibits neutrophil oxidative burst (hydrogen peroxide production), an immunologic functional effect, but not a physiological process relevant to voiding (perfusion/smooth muscle/neural signaling) or improved voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX "5 µmol/l" inhibited neutrophil oxidative burst (reduced intracellular hydrogen peroxide to "76 ± 5%"), which is unrelated to the unit’s claim about PTX’s mechanism for improved voiding acting on current physiological voiding function rather than tissue structure.

### A2-H1-R1 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses PTX safety/tolerability and side effects (GI symptoms, dizziness), not a mechanism acting on physiological voiding function vs tissue structure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness addresses PTX tolerability/safety ("very safe," "usually well tolerated," GI symptoms, dizziness) and does not discuss any mechanism for improved voiding or functional-vs-structural action.

### A2-H1-R1 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: PARTIALLY_COVERS - Witness says PTX inhibits PDE1–5 (IC50 50–200 μmol/L), which is a functional biochemical mechanism, but it does not connect this to voiding-related physiological function or specify that improved voiding is via function rather than structural tissue change.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness states PTX "inhibits PDE 1–5" with "IC50 values 50–200 μmol/L," a biochemical mechanism consistent with acting on ongoing physiology; but it does not tie this specifically to improved voiding in the cohort nor rule out tissue-structure mechanisms.

### A2-H1-R1 x W-FRD-Q0061-02-c5-Q0061
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: In siu2003.pdf.md (Abstract (Results)), the authors report the pelvic muscle training program “appears to be able to reduce the overall urinary incontinence episodes by 85.2%.”
- Source: siu2003.pdf.md Abstract (Results)
- Pass A: NO_SEMANTIC_RELATION - Witness is about pelvic muscle training reducing incontinence episodes, not PTX or its mechanism for improved voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about "pelvic muscle training" reducing "urinary incontinence episodes" and does not mention PTX or any mechanism for improved voiding via current physiological function vs tissue structure.

### A2-H1-R1 x W-FRD-Q0063-01-c4-Q0063
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: PARTIALLY_COVERS - Witness shows PTX reduced FMLP-stimulated superoxide production in PMNs, indicating an acute functional physiological effect (immune cell oxidative burst), but it is not tied to voiding improvement or the cohort/mechanism distinction of function vs tissue structure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX reduced PMN "superoxide" production after FMLP stimulation; it does not address voiding improvement in the cohort or the specific functional-vs-structural mechanism for voiding.

### A2-H1-R1 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism for improved voiding in this cohort acts on current physiological function (not established tissue structure).
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: PARTIALLY_COVERS - Witness reports PTX reduced lysozyme release (PMN degranulation) under inflammatory conditioning, a functional effect, but it does not address voiding physiology or whether voiding improvement is via current function rather than structural tissue alteration.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX reduced PMN lysozyme release under LPS-conditioned medium; this concerns inflammatory cell degranulation and does not speak to PTX’s mechanism for improved voiding (current physiological function vs tissue structure) in the cohort.

### A2-H1-R2 x W-FRD-Q0020-02-c1-Q0020
- Unit (REQUIRED_SUPPORT): At clinically attainable exposures, PTX or its metabolites produce measurable improvement in voiding within days to a few weeks.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness describes an oral PTX dosing regimen in healthy volunteers (5×400 mg/day for 2 or 7 days) but gives no voiding measures or reported improvement within days to weeks.
- Pass B: PARTIALLY_COVERS - The witness establishes a clinically relevant PTX oral exposure window (“treated orally with pentoxifylline… for 2 days… or… 7 days”) but provides no “measurable improvement in voiding,” so it only matches the exposure/timing component, not the improvement predicate.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only describes dosing/exposure timing in “four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days… or… 7 days” and contains no statement about voiding outcomes or any “measurable improvement in voiding within days to a few weeks.”

### A2-H1-R2 x W-FRD-Q0039-02-Q0039
- Unit (REQUIRED_SUPPORT): At clinically attainable exposures, PTX or its metabolites produce measurable improvement in voiding within days to a few weeks.
- Witness: In SILODOSING (s00345-024-04974-7.pdf.md), both groups continued silodosin 8 mg once daily for 12 weeks (Patients and methods > Procedures > Experimental and control groups). The experimental group also did PFMT 30 min/day, 5 days/week for 12 weeks, supervised by a physiotherapist weekly (same). Anticholinergics/β3-mimetics use within 4 weeks pre–visit 1 and during study excluded (Patients and methods > Exclusion criteria).
- Source: s00345-024-04974-7.pdf.md Patients and methods > Procedures > Experimental and control groups; Patients and methods > Exclusion criteria; Patients and methods > Allocation
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - This witness specifies “both groups continued silodosin… 12 weeks” and PFMT/exclusion criteria, with no mention of PTX or PTX-related voiding improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness is about “silodosin 8 mg… for 12 weeks” plus PFMT and exclusions, and does not mention PTX/pentoxifylline, its metabolites, or voiding improvement attributable to PTX.

### A2-H1-R2 x W-FRD-Q0043-01-c1-Q0043
- Unit (REQUIRED_SUPPORT): At clinically attainable exposures, PTX or its metabolites produce measurable improvement in voiding within days to a few weeks.
- Witness: In ladi-seyedian2017.pdf.md (7.3.1 Parasympathomimetics), the review reports Bougas et al. studied distigmine bromide in 27 UAB patients: 5 mg three times daily for 4 weeks significantly reduced PVR and obviated the need for CIC in 11 patients [76].
- Source: ladi-seyedian2017.pdf.md Section 7.3.1 Parasympathomimetics (distigmine paragraph; ref [76])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about “distigmine bromide… reduced PVR… obviated the need for CIC,” not PTX or its metabolites.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports Bougas et al. using “distigmine bromide… for 4 weeks” with reduced PVR/CIC need, which is a different drug and provides no claim about PTX or PTX metabolite effects on voiding within days to weeks.

### A2-H1-R2 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): At clinically attainable exposures, PTX or its metabolites produce measurable improvement in voiding within days to a few weeks.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only says “Adverse effects were not reported” and “No adverse effects of pentoxifylline treatment were observed,” which addresses safety, not “measurable improvement in voiding within days to a few weeks.”
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only states safety findings—“No adverse effects of pentoxifylline treatment were observed” / “Adverse effects were not reported”—and does not assert any improvement in voiding or timing of such improvement.

### A2-H1-R3 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses mechanism of PTX effects on detrusor contractions (electric stimulation vs carbachol) and inferred pathways; it does not report any change in voiding benefit after stopping PTX or during washout.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses PTX effects on detrusor contractions to “electric stimulation” vs “carbachol” and infers non-cholinergic pathways; it does not mention stopping treatment, withdrawal, or any change in voiding benefit after discontinuation.

### A2-H1-R3 x W-FRD-Q0007-04-c4-Q0007
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: NO_SEMANTIC_RELATION - Witness asserts that after a “point of no return” bladder decompensation becomes irreversible; it does not describe PTX-related voiding improvement diminishing after PTX discontinuation.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness warns about a “point of no return” leading to “irreversible bladder decompensation and failure,” but does not describe any treatment being stopped or a voiding benefit diminishing with withdrawal.

### A2-H1-R3 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: NO_SEMANTIC_RELATION - Witness is about diagnostic uroflowmetry patterns in pseudodyssynergia and controlling for anxiety (“bashful voiding”), not PTX treatment withdrawal or reversibility of voiding benefit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes uroflowmetry criteria for diagnosing pseudodyssynergia and controlling for “performance anxiety”/“bashful voiding,” with no statement about PTX treatment, discontinuation, or reversibility of voiding benefit.

### A2-H1-R3 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX inhibition of neutrophil oxidative burst in whole blood at 5 µmol/L; it contains no information about voiding outcomes or what happens when PTX is stopped.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX (5 µmol/l) inhibiting FMLP-stimulated neutrophil oxidative burst (DCF-assayed H2O2); it contains no information about voiding outcomes or what happens when treatment stops.

### A2-H1-R3 x W-FRD-Q0020-02-c1-Q0020
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness describes dosing regimens in healthy volunteers (2 days vs 7 days) but does not report voiding improvement nor whether any benefit diminishes after discontinuation.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only describes PTX dosing regimens in “four healthy volunteers” for “2 days” or “7 days” and does not report any voiding benefit or diminution after stopping treatment.

### A2-H1-R3 x W-FRD-Q0063-01-c1-Q0063
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Sullivan-et-al-1988: Human PMNs incubated 30 min at 37°C with pentoxifylline 300 µg/ml decreased adherence to nylon vs diluent: 64.1±2.7% (n=16) vs 54.0±3.9% (n=6; P=0.031) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → PMN adherence).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → PMN adherence (opening paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness reports an in-vitro effect of pentoxifylline on human PMN adherence to nylon after 30 min incubation; it says nothing about voiding benefits in patients or whether any benefit diminishes after stopping treatment.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports in-vitro incubation of human PMNs with PTX (300 µg/ml) altering adherence to nylon; it does not address voiding benefit, treatment withdrawal, or reversibility.

### A2-H1-R3 x W-FRD-Q0063-01-c4-Q0063
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX reducing FMLP-stimulated superoxide production in PMNs; no mention of urinary voiding outcomes or reversibility upon withdrawal.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX (100 µg/ml) reducing FMLP-stimulated superoxide production in PMNs; no urinary/voiding outcomes or withdrawal effects are mentioned.

### A2-H1-R3 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Witness concerns PMN degranulation/lysozyme release in response to LPS-conditioned media and modulation by PTX; it does not address voiding improvement or what happens when PTX is discontinued.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes LPS-MCM increasing PMN lysozyme release and PTX reducing it; there is no claim about voiding benefit or that benefits diminish when treatment stops.

### A2-H1-R3 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states PTX “up to 50 µmol/l did not change… [Ca2+]i” and “500 µmol/l reduced” calcium signals; no clinical voiding effect or treatment withdrawal is addressed.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX effects on neutrophil calcium transients (“up to 50 µmol/l did not change… [Ca2+]i”; “500 µmol/l reduced”); it does not mention voiding outcomes or reversibility after withdrawal.

### A2-H1-R3 x W-FRD-Q0092-03-c4-Q0092
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports tolerability (“2 patients reported epigastric pain… complete remission”); it contains no claim about voiding benefit or reversibility after stopping PTX.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states “2 patients reported epigastric pain… complete remission” while completing 24 weeks; it provides no information about voiding benefit changing after stopping treatment.

### A2-H1-R3 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness specifies enrollment and regimen (“pentoxifylline 800 mg/day plus vitamin E… open-label 24-week”); it does not report voiding improvements nor what happens after discontinuation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes an “open-label 24-week” regimen of “pentoxifylline 800 mg/day plus vitamin E”; it does not report any voiding benefit or its diminution upon withdrawal.

### A2-H1-R3 x W-FRD-Q0098-01-Q0098
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness describes hemodynamic/immune changes after “IV PTX 40 mg/kg… before hemorrhage” and mortality (“they all died”); no voiding outcomes or withdrawal/washout are mentioned.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports IV PTX pretreatment effects on MAP/HR/WBC and that “they all died” after hemorrhage; there is no mention of voiding benefit or what happens when treatment stops.

### A2-H1-R3 x W-FRD-Q0104-03-c6-Q0104
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports hs-CRP statistics (“significant treatment effect… no time effect… no treatment×time interaction”) for infliximab vs placebo; it does not address PTX, voiding, or stopping treatment.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports hs-CRP longitudinal statistics for infliximab vs placebo ("significant treatment effect... no time effect... no treatment×time interaction"); it says nothing about voiding benefit, withdrawal, or benefit diminishing after stopping treatment.

### A2-H1-R3 x W-FRD-Q0131-03-c3-Q0131
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only says “PTX has short half-life about 1.6 h,” which is pharmacokinetics and not an observation that voiding benefits “lessen or disappear after PTX is discontinued.”
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states a pharmacokinetic fact ("PTX has short half-life about 1.6 h"); it does not report any change in voiding benefit after treatment stops (reversibility with withdrawal).

### A2-H1-R3 x W-FRD-Q0131-03-c4-Q0131
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states “PTX toxicity was reported at 80 mg/kg” with acute adverse effects; it provides no observation of voiding improvement or reversibility upon discontinuation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes toxicity at a dose ("PTX toxicity was reported at 80 mg/kg" with adverse effects); it provides no information about voiding benefit or its diminution upon discontinuation.

### A2-H1-R3 x W-FRD-Q0148-01-c1-Q0148
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness concerns TURP outcomes after “minimum 10-year follow-up” and says “no significant LUTS improvement… no significant change… including BCI”; it is not about PTX treatment or withdrawal effects.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about long-term TURP follow-up showing "no significant LUTS improvement" and "no significant change" in voiding parameters; it does not address stopping a treatment and subsequent loss of a voiding benefit.

### A2-H1-R3 x W-FRD-Q0149-04-c4-Q0149
- Unit (REQUIRED_SUPPORT): If treatment stops, the voiding benefit diminishes (reversibility with withdrawal).
- Witness: Raison2013 (raison2013.pdf.md, RESULTS): in subgroup mixed-effects models for repeated measures, standardized effect size difference at 12 weeks was “moderate to large, in opposite directions”: 0.41 favoring infliximab for baseline hs-CRP >5 mg/L, versus −0.82 favoring placebo for baseline hs-CRP ≤5 mg/L.
- Source: raison2013.pdf.md RESULTS (paragraph containing standardized effect sizes); Figure 4
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports “standardized effect size difference at 12 weeks” for infliximab vs placebo by baseline hs-CRP; it does not mention pentoxifylline, voiding outcomes, or stopping/withdrawal.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports effect size differences at 12 weeks for infliximab vs placebo by baseline hs-CRP subgroup; it does not mention withdrawal/cessation or diminishing voiding benefit after stopping treatment.

### A2-H2-A1 x W-FRD-Q0019-03-c3-Q0019
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX inhibiting neutrophil oxidative burst (hydrogen peroxide production) at 5 µmol/L in whole blood; it does not mention voiding outcomes, timing of symptom improvement, or rapid clinical benefit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in-vitro/whole-blood neutrophil effect: “5 µmol/l significantly inhibited the FMLP-stimulated burst… hydrogen peroxide… to 76 ± 5% of no-PTX control.” The unit concerns whether “meaningful benefit appears too quickly to be structurally mediated,” i.e., timing/mechanism of clinical benefit; no benefit/timing is stated.

### A2-H2-A1 x W-FRD-Q0020-02-c1-Q0020
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness only describes dosing regimen in healthy volunteers (PTX 5×400 mg/day for 2 or 7 days) and does not report any voiding improvement or symptom change within days/weeks.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only describes dosing in “four healthy volunteers… pentoxifylline 5×400 mg/day for 2 days… or… 7 days” and explicitly is in Methods; it provides no claim about benefit, speed of benefit, or structural mediation.

### A2-H2-A1 x W-FRD-Q0034-04-bortnick20-c1-Q0034
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: bortnick2020.pdf.md (“Medical therapy”→“Combination therapy” MTOPS paragraph) reports MTOPS studied finasteride+doxazosin in 3000 men (mean age 62.6 years, SD 7.3) and found combination therapy improved voiding symptoms and maximum urinary flow rate more than either alone, prevented BPH progression better, and reduced the long-term risk of acute urinary retention and need for invasive therapy.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (MTOPS paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness is about MTOPS combination therapy (finasteride+doxazosin) effects on LUTS and flow, not about pentoxifylline or speed of PTX benefit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns MTOPS results for “finasteride+doxazosin… improved voiding symptoms and maximum urinary flow rate,” not pentoxifylline and not the question of benefit appearing “too quickly to be structurally mediated.”

### A2-H2-A1 x W-FRD-Q0039-02-Q0039
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: In SILODOSING (s00345-024-04974-7.pdf.md), both groups continued silodosin 8 mg once daily for 12 weeks (Patients and methods > Procedures > Experimental and control groups). The experimental group also did PFMT 30 min/day, 5 days/week for 12 weeks, supervised by a physiotherapist weekly (same). Anticholinergics/β3-mimetics use within 4 weeks pre–visit 1 and during study excluded (Patients and methods > Exclusion criteria).
- Source: s00345-024-04974-7.pdf.md Patients and methods > Procedures > Experimental and control groups; Patients and methods > Exclusion criteria; Patients and methods > Allocation
- Pass A: NO_SEMANTIC_RELATION - Witness describes silodosin ± PFMT trial procedures and exclusions; it does not involve PTX or report rapid voiding improvement attributable to PTX.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes trial procedures for “silodosin 8 mg once daily for 12 weeks” ± PFMT and exclusion criteria; it does not address pentoxifylline or any claim about benefit occurring too quickly for structural mediation.

### A2-H2-A1 x W-FRD-Q0048-02-c1-Q0048
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: In 10.1016@s0041-13450001266-5.pdf.md (PATIENTS AND METHODS), pentoxifylline was dosed 150 mg IV 2 hours pre-op, 150 mg IV after graft reperfusion, and 300 mg IV 8 hours after grafting; then 1200 mg/day in three oral doses for 7 days.
- Source: 10.1016@s0041-13450001266-5.pdf.md PATIENTS AND METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness provides perioperative/7-day PTX dosing (IV then oral) but contains no finding of 'meaningful voiding improvement within days to a few weeks' or any voiding endpoints.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is perioperative PTX dosing (“150 mg IV… then 1200 mg/day… for 7 days”) without reporting any benefit, timing of benefit, or whether any benefit is non-structural/too rapid.

### A2-H2-A1 x W-FRD-Q0050-02-Q0050
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness claims PTX is generally safe/well tolerated with ~3% GI symptoms/dizziness; it does not address voiding improvement timing or mechanism (functional vs structural).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states tolerability/safety (“very safe… well tolerated… ~3%… gastrointestinal… dizziness”) and does not discuss meaningful benefit, how fast it appears, or whether it is structurally mediated.

### A2-H2-A1 x W-FRD-Q0061-02-c2-Q0061
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: In siu2003.pdf.md (RESULTS), the authors report: “The mean time between the first and fourth visits was 213.40 days (30.50 weeks).”
- Source: siu2003.pdf.md RESULTS
- Pass A: NO_SEMANTIC_RELATION - Witness only reports the time between study visits (~213 days/30.5 weeks) and does not report any PTX-related voiding improvement within days to weeks.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports only study scheduling: “mean time between the first and fourth visits was 213.40 days (30.50 weeks),” which does not assert rapid benefit nor any mechanism (structural vs non-structural).

### A2-H2-A1 x W-FRD-Q0063-01-c5-Q0063
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX reducing FMLP-stimulated lysozyme release in PMNs under LPS-conditioned medium; no clinical voiding outcomes or rapid symptom improvement are mentioned.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is an in-vitro PMN degranulation finding: PTX “reduced” LPS-MCM/FMLP-induced “lysozyme release.” The unit is about meaningful clinical benefit appearing too quickly to be structurally mediated; no benefit timing/mechanism is mentioned.

### A2-H2-A1 x W-FRD-Q0079-04-c3-Q0079
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX effects on neutrophil calcium transients at various concentrations; it is mechanistic immunology data unrelated to voiding improvement timing.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports mechanistic neutrophil calcium data (“PTX up to 50 µmol/L changed neither… [Ca2+]i; 500 µmol/L reduced…”). It does not address meaningful benefit, its timing, or structural mediation.

### A2-H2-A1 x W-FRD-Q0089-04-c2-Q0089
- Unit (ADVERSE_TEST): A2-H2 is undermined if meaningful benefit appears too quickly to be structurally mediated.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Witness is speculation about PTX anti-inflammatory potency once inflammation is triggered; it does not report meaningful voiding improvement within days/weeks at attainable exposure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is speculation about anti-inflammatory potency (“may have no potent anti-inflammatory effect once inflammation has been triggered… may be too weak…”), not an observation that benefit appears quickly or too quickly to be structurally mediated.

### A2-H2-A2 x W-FRD-Q0003-04-c1-Q0003
- Unit (ADVERSE_TEST): A2-H2 is undermined if structural effects appear only when treatment precedes injury (prevention rather than reversal).
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Discusses proposed biochemical mechanisms (PDE inhibition/NOS activation) for beneficial effects on contractile function after ischemic injury, but says nothing about structural endpoints or a before-vs-after injury treatment timing dependency.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness proposes biochemical mechanisms ("phosphodiesterase inhibitor"/"nitric oxide synthase activator") for "beneficial effects on contractile function after ischemic injury" but does not discuss structural effects or whether effects appear only when treatment precedes injury (prevention vs reversal).

### A2-H2-A2 x W-FRD-Q0003-04-c3-Q0003
- Unit (ADVERSE_TEST): A2-H2 is undermined if structural effects appear only when treatment precedes injury (prevention rather than reversal).
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Reports functional findings (detrusor contractions to electric stimulation vs carbachol) and infers neural pathway involvement; does not address structural changes or whether effects occur only with pre-injury treatment and fail post-injury.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports functional responses (improved detrusor contractions to electric stimulation but not to carbachol) and speculates about neural pathways; it provides no statement about structural effects nor any dependence on pre-injury vs post-injury treatment timing.

### A2-H2-A2 x W-FRD-Q0019-03-c3-Q0019
- Unit (ADVERSE_TEST): A2-H2 is undermined if structural effects appear only when treatment precedes injury (prevention rather than reversal).
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - In vitro neutrophil oxidative burst inhibition by PTX at specific concentrations; unrelated to bladder structural endpoints or timing (pre-treatment vs post-injury) requirements.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is an in vitro/whole-blood neutrophil assay where PTX (5 µmol/l) inhibits FMLP-stimulated oxidative burst; it does not address structural outcomes in an injury model or whether effects require treatment before injury.

### A2-H2-A2 x W-FRD-Q0029-04-c5-Q0029
- Unit (ADVERSE_TEST): A2-H2 is undermined if structural effects appear only when treatment precedes injury (prevention rather than reversal).
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: NO_SEMANTIC_RELATION - Describes loss to follow-up in PTX vs placebo groups; provides no claim about structural effects depending on whether treatment precedes injury.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes loss to follow-up reasons in placebo vs PTX groups (severe disease shift to steroids; did not return) and makes no claim about structural effects or the necessity of pre-injury treatment for such effects.

### A2-H2-A2 x W-FRD-Q0042-03-c2-Q0042
- Unit (ADVERSE_TEST): A2-H2 is undermined if structural effects appear only when treatment precedes injury (prevention rather than reversal).
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: NO_SEMANTIC_RELATION - Reports side effects/epigastric pain management during 24 weeks; does not mention structural endpoints or pre- vs post-injury initiation effects.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports side effects (epigastric pain treated with omeprazole) during 24 weeks of treatment; it does not mention structural endpoints or compare pre-injury versus post-injury treatment effects.

### A2-H2-A2 x W-FRD-Q0044-04-c2-Q0044
- Unit (ADVERSE_TEST): A2-H2 is undermined if structural effects appear only when treatment precedes injury (prevention rather than reversal).
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - States no adverse effects were reported/observed; unrelated to whether PTX improves structural endpoints only when given before injury and not after established dysfunction.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states "Adverse effects were not reported" / "No adverse effects ... were observed"; this concerns tolerability, not whether structural effects occur only with pre-injury treatment rather than reversal after injury.

### A2-H2-A2 x W-FRD-Q0050-02-Q0050
- Unit (ADVERSE_TEST): A2-H2 is undermined if structural effects appear only when treatment precedes injury (prevention rather than reversal).
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - General safety/tolerability statements and common complaints; no information about structural outcomes or dependence on treatment timing relative to injury.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness claims PTX is "very safe"/"usually well tolerated" with common GI symptoms and dizziness; it contains no information about structural effects or timing dependence (treatment before vs after injury).

### A2-H2-A3 x W-FRD-Q0003-04-c3-Q0003
- Unit (ADVERSE_TEST): A2-H2 is undermined if structural improvement does not accompany functional improvement.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports mixed functional pharmacologic responses (improved electric-stimulation contractions but not carbachol responses) and an inferred neural-pathway explanation; it does not compare functional improvement vs lack of structural improvement (fibrosis/remodeling/damage).
- Pass B: PARTIALLY_COVERS - Witness contains functional improvement ('PTX improved detrusor contractions to electric stimulation') but reports no measured structural endpoints (fibrosis/remodeling/damage) or their lack of improvement, so it only matches the 'functional improves' component, not the required 'no structural improvement' condition.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness states only functional findings ("PTX improved detrusor contractions to electric stimulation" but "did not improve responses to carbachol") and a proposed mechanism; it does not mention any structural outcomes (e.g., fibrosis/remodeling) nor that "structural improvement does not accompany functional improvement," which is required by the unit.

### A2-H2-C1 x W-FRD-Q0003-04-c1-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness proposes acute biochemical mechanisms (PDE inhibition/NO synthase activation increasing NO/cGMP) to explain beneficial effects, but gives no timing of improvement (days vs weeks-months) or statement about attainable exposure/onset.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness proposes biochemical mechanisms (“phosphodiesterase inhibitor and nitric oxide synthase activator… increases… NO… cGMP”) but gives no claim about onset timing (“weeks to months” vs “within days to a few weeks”) nor about “attainable exposure.”

### A2-H2-C1 x W-FRD-Q0003-04-c3-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses which pathway PTX acts through (not cholinergic; possibly purinergic/NANC) based on contraction responses, but provides no onset timeline (days/weeks/months) or exposure attainability constraint.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness contrasts pathways (“did not improve responses to carbachol… not via cholinergic… related to purinergic or other… pathways”) without addressing the unit’s timing discriminator (weeks–months vs days–weeks) or exposure attainability.

### A2-H2-C1 x W-FRD-Q0005-04-c2-Q0005
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In han1990.pdf.md (Materials and Methods—CAT Assay), the authors state that the CAT assay “was performed according to the thin-layer chromatography method of Gorman et al. (9).”
- Source: han1990.pdf.md Materials and Methods — CAT Assay
- Pass A: NO_SEMANTIC_RELATION - Witness only states the CAT assay followed a published TLC method; it does not address timing of clinical/functional improvement or exposure levels.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states a lab protocol detail (“CAT assay was performed according to… Gorman et al.”) and makes no statement about time-to-improvement or “attainable exposure.”

### A2-H2-C1 x W-FRD-Q0006-04-c1-Q0006
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns experimental design about testing NO dependence of in vitro vascular relaxation (no L-NAME; endothelium denuding) and does not mention time-to-improvement in vivo or delayed onset at attainable exposure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses experimental controls in vitro (“did not add NO blockers… instead… denuding… endothelial cells”) and does not speak to delayed onset (weeks–months) vs rapid onset (days–weeks) at attainable exposure.

### A2-H2-C1 x W-FRD-Q0007-01-c1-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness gives a definition of detrusor underactivity (ICS definition) without any claim about treatment onset timing (weeks-months vs days-weeks) or exposure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides only a definition of detrusor underactivity (“a contraction of reduced strength…”) and contains no claim about timing of improvement or exposure constraints.

### A2-H2-C1 x W-FRD-Q0010-02-Q0010
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md (MP75-18 > RESULTS), the mean wait time between referral and appointment was 54.7 days (SD 37.3; range 1–215).
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18 > RESULTS
- Pass A: NO_SEMANTIC_RELATION - Witness reports wait time between referral and appointment (mean 54.7 days), which is unrelated to whether the mechanism’s improvement occurs only after weeks-months at attainable exposure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports administrative timing (“mean wait time… 54.7 days”) rather than biological/therapeutic onset timing or “attainable exposure” for the mechanism classification constraint.

### A2-H2-C1 x W-FRD-Q0019-02-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: PARTIALLY_COVERS - Witness addresses the 'attainable exposure' constraint by stating clinically obtained peak plasma PTX is <5 µmol/L and total active forms unlikely >10 µmol/L, but it does not address the unit’s required delayed onset (weeks-to-months) or exclude improvement within days-to-weeks.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness directly addresses attainability (“peak plasma PTX levels are <5 μmol/l… combined level… unlikely to exceed 10 μmol/l”) but does not address whether improvement occurs only after “weeks to months” versus “within days to a few weeks.”

### A2-H2-C1 x W-FRD-Q0020-02-c1-Q0020
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: PARTIALLY_COVERS - Witness describes short PTX dosing regimens (2 days or 7 days), which relates to the 'days to a few weeks' timeframe, but it does not state that meaningful improvement occurs within that period (or only after weeks-months) at attainable exposure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only describes dosing durations (“treated… 5×400 mg/day for 2 days, or… 7 days”) and does not claim any improvement onset (nor that improvement cannot occur within days–weeks) at attainable exposure.

### A2-H2-C1 x W-FRD-Q0025-03-Q0025
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In delanian2005.pdf.md (RESULTS → Primary Analyses → “After stopping PTX-vitE: Rebound effect.”), after stopping PTX-vitE, RIF surface area showed a significant initial increase (P = .037). The fibrotic increase was significantly lower and asymptomatic in LPE: 8.5%/yr (95% CI, 1–16) vs SPE: 40%/yr (95% CI, 24–56); P = .0012.
- Source: delanian2005.pdf.md RESULTS → Primary Analyses → “After stopping PTX-vitE: Rebound effect.”
- Pass A: PARTIALLY_COVERS - Witness discusses fibrosis surface area changes after stopping PTX-vitE and reports annualized fibrotic increase rates, aligning with a long-term structural/fibrotic timeframe (weeks-months/years), but it does not explicitly rule out primary improvement within days-to-weeks or specify onset timing at clinically attainable exposure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a rebound after stopping PTX-vitE and long-term fibrosis rates (“8.5%/yr… 40%/yr”) but does not state the unit’s discriminator that improvement occurs “only after weeks to months, not within days to a few weeks, at attainable exposure.”

### A2-H2-C1 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: NO_SEMANTIC_RELATION - Witness reports prevalence of detrusor underactivity in men with diabetes and related urodynamic features; it does not address treatment onset timing or exposure attainability.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is epidemiology/prevalence (“79% had detrusor underactivity…”) and contains no statements about treatment mechanism timing or exposure attainability.

### A2-H2-C1 x W-FRD-Q0034-01-bortnick20-c3-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: bortnick2019.pdf.md (Review of Medications > Alpha Blockers) reports Duan et al. used 2006–2012 Medicare data in a cohort of 253,136 men >65 with BPH; dementia (ICD-9 codes) risk after mean 19.8 months was significantly higher with tamsulosin versus no BPH meds and versus doxazosin, terazosin, alfuzosin, dutasteride, or finasteride.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: NO_SEMANTIC_RELATION - Witness concerns dementia risk associated with tamsulosin over ~19.8 months; it does not speak to onset of improvement for A2-H2 or to clinically attainable exposure producing delayed benefit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns dementia risk with tamsulosin after “mean 19.8 months,” not a claim about mechanism classification requiring improvement only after weeks–months (and not within days–weeks) at attainable exposure.

### A2-H2-C1 x W-FRD-Q0034-02-bortnick20-c2-Q0034
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: Bortnick2020.pdf.md (“Medical therapy” → “5-alpha reductase inhibitors”): Welk et al. report a population-based, retrospective, propensity-matched Canadian cohort of 93,000 men >66 years on 5-ARIs (median 1.57 years) in which depression risk was elevated during the initial 18 months after starting a 5-ARI and remained elevated, less so, thereafter.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → subsection “5-alpha reductase inhibitors”
- Pass A: NO_SEMANTIC_RELATION - Witness reports depression risk timing on 5-ARIs (initial 18 months); it is about adverse outcomes, not delayed therapeutic improvement onset at attainable exposure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports depression risk timing on 5-ARIs (“elevated during the initial 18 months…”) and does not address A2-H2’s improvement-onset discriminator or attainable exposure for the mechanism.

### A2-H2-C1 x W-FRD-Q0039-02-Q0039
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In SILODOSING (s00345-024-04974-7.pdf.md), both groups continued silodosin 8 mg once daily for 12 weeks (Patients and methods > Procedures > Experimental and control groups). The experimental group also did PFMT 30 min/day, 5 days/week for 12 weeks, supervised by a physiotherapist weekly (same). Anticholinergics/β3-mimetics use within 4 weeks pre–visit 1 and during study excluded (Patients and methods > Exclusion criteria).
- Source: s00345-024-04974-7.pdf.md Patients and methods > Procedures > Experimental and control groups; Patients and methods > Exclusion criteria; Patients and methods > Allocation
- Pass A: PARTIALLY_COVERS - Witness specifies a 12-week treatment duration (silodosin ± PFMT), which is within 'weeks to months', but it does not state that improvement occurs only after weeks-months (nor that there is little/no improvement within days-to-a-few-weeks) or address 'attainable exposure' in the unit’s mechanistic sense.
- Pass B: NO_SEMANTIC_RELATION - The witness specifies the regimen “for 12 weeks” and exclusions, but contains no claim about when improvement occurs (days vs weeks/months) or about clinically attainable exposure effects.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states the intervention duration and regimen (“continued silodosin 8 mg once daily for 12 weeks” and PFMT schedule) plus exclusions; it makes no claim about when improvement occurs (“only after weeks to months” vs “within days to a few weeks”) or about onset at attainable exposure.

### A2-H2-C1 x W-FRD-Q0042-03-c2-Q0042
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: PARTIALLY_COVERS - Witness reports all patients completed 24 weeks of treatment (a weeks-to-months timeframe), but provides only side-effect information and does not assert delayed onset of meaningful improvement or exclude early improvement within days-to-weeks at attainable exposure.
- Pass B: NO_SEMANTIC_RELATION - The witness only states “24 weeks of treatment” and that epigastric pain had “complete remission” on omeprazole; it does not address onset timing of the hypothesized therapeutic improvement mechanism.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports completion of “24 weeks of treatment” and a side effect (epigastric pain) with “complete remission” on omeprazole; it does not address timing of therapeutic improvement onset or exclude early improvement.

### A2-H2-C1 x W-FRD-Q0043-01-c1-Q0043
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In ladi-seyedian2017.pdf.md (7.3.1 Parasympathomimetics), the review reports Bougas et al. studied distigmine bromide in 27 UAB patients: 5 mg three times daily for 4 weeks significantly reduced PVR and obviated the need for CIC in 11 patients [76].
- Source: ladi-seyedian2017.pdf.md Section 7.3.1 Parasympathomimetics (distigmine paragraph; ref [76])
- Pass A: CONTRADICTS - Unit requires improvement only after weeks-to-months and not primarily within days-to-a-few-weeks at attainable exposure; witness reports distigmine 5 mg TID for 4 weeks (a few weeks) significantly reduced PVR and stopped CIC in 11 patients, i.e., meaningful improvement within 4 weeks.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Unit is a mechanistic timing constraint (“improvement only after weeks to months, not within days to a few weeks, at attainable exposure”), while the witness reports a 4-week outcome (“for 4 weeks significantly reduced PVR... in 11 patients”) but does not state improvement occurred only within days–few weeks nor compare against later-onset-only; it also lacks the unit’s “only after weeks to months” discriminator.

### A2-H2-C1 x W-FRD-Q0048-02-c1-Q0048
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In 10.1016@s0041-13450001266-5.pdf.md (PATIENTS AND METHODS), pentoxifylline was dosed 150 mg IV 2 hours pre-op, 150 mg IV after graft reperfusion, and 300 mg IV 8 hours after grafting; then 1200 mg/day in three oral doses for 7 days.
- Source: 10.1016@s0041-13450001266-5.pdf.md PATIENTS AND METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness only describes pentoxifylline dosing schedule peri-operatively and for 7 days; it does not report timing of clinical improvement in UAB/LUTS or whether effects occur only after weeks-to-months.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is solely a dosing schedule (“then 1200 mg/day... for 7 days”) and contains no statement about improvement timing or about weeks-to-months vs days-to-weeks onset at attainable exposure.

### A2-H2-C1 x W-FRD-Q0050-02-Q0050
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses safety/tolerability and common side effects of PTX, not onset timing of functional improvement (days/weeks vs weeks/months) at attainable exposure.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes safety/tolerability (“very safe,” “usually well tolerated,” ~3% dizziness/GI symptoms) and does not mention timing of improvement (days vs weeks/months) or the unit’s delayed-onset-only constraint.

### A2-H2-C1 x W-FRD-Q0061-02-c2-Q0061
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: In siu2003.pdf.md (RESULTS), the authors report: “The mean time between the first and fourth visits was 213.40 days (30.50 weeks).”
- Source: siu2003.pdf.md RESULTS
- Pass A: NO_SEMANTIC_RELATION - Witness reports visit spacing ('mean time between the first and fourth visits was 213.40 days') but makes no claim about when improvement occurs or whether early improvement is absent.
- Pass B: PARTIALLY_COVERS - Witness gives a follow-up interval of "213.40 days (30.50 weeks)," which is within weeks-to-months, but it does not mention any improvement onset or whether changes occur earlier than a few weeks.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness gives only a follow-up/visit interval (“mean time between the first and fourth visits was 213.40 days (30.50 weeks)”) without any claim about when improvement occurs or that improvement is only after weeks-to-months.

### A2-H2-C1 x W-FRD-Q0067-03-c1-Q0067
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: Vogel2023_Glucocorticoid_Withdrawal.md (Figure 4): 3 months after successful surgery for Cushing’s syndrome, CRP (mg dL−1) inversely correlated with 12-month age- and gender-corrected grip strength (“normalized grip strength,” % of normal controls) (N=50, Spearman −0.371, R2=0.155, P=.008) and with 12-month SF-36 Physical Component Summary (N=38, Spearman −0.356, R2=0.127, P=.028).
- Source: Vogel2023_Glucocorticoid_Withdrawal.md Figure 4
- Pass A: NO_SEMANTIC_RELATION - Witness reports correlations between CRP at 3 months post-surgery and 12-month grip strength/SF-36 outcomes; it does not address onset timing of improvement after treatment at attainable exposure for A2-H2.
- Pass B: PARTIALLY_COVERS - Witness uses "3 months" and "12-month" outcomes (weeks-to-months timescale), but it is correlational and does not claim that improvement occurs only after weeks–months or that there is little/no improvement within days–few weeks.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports correlations between CRP at “3 months” and outcomes at “12-month” after surgery; it does not state a delayed onset of improvement (only after weeks–months) nor rule out improvement within days–few weeks at attainable exposure.

### A2-H2-C1 x W-FRD-Q0123-01-c5-Q0123
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: Vogel2023_Glucocorticoid_Withdrawal.md (Figure 4 caption (panel A)): Relationship between C-reactive protein (mg dL-1) 3 months after successful Cushing’s surgery and age- and gender-corrected grip strength at 12 months (normalized grip strength, % of normal controls); line is estimated linear regression. N=50, Spearman’s coefficient -0.371, R2=0.155, P=.008.
- Source: Vogel2023_Glucocorticoid_Withdrawal.md Figure 4 caption (panel A)
- Pass A: NO_SEMANTIC_RELATION - Witness is a figure-caption restating CRP at 3 months vs grip strength at 12 months after Cushing’s surgery; it does not address delayed onset of improvement from a treatment at attainable exposure.
- Pass B: PARTIALLY_COVERS - Witness explicitly references timepoints "3 months" and "12 months," consistent with a weeks-to-months frame, but it is a correlational relationship (CRP vs strength) and does not speak to treatment onset or rule out early (days–few weeks) improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is a caption about a correlation between CRP “3 months” after surgery and grip strength at “12 months,” which does not assert anything about timing of improvement onset (only after weeks–months) or negate early improvement.

### A2-H2-C1 x W-FRD-Q0149-04-c4-Q0149
- Unit (CONTEXTUAL_CONSTRAINT): The mechanism classification must align with the axis discriminator: A2-H2 corresponds to improvement only after weeks to months, not within days to a few weeks, at attainable exposure.
- Witness: Raison2013 (raison2013.pdf.md, RESULTS): in subgroup mixed-effects models for repeated measures, standardized effect size difference at 12 weeks was “moderate to large, in opposite directions”: 0.41 favoring infliximab for baseline hs-CRP >5 mg/L, versus −0.82 favoring placebo for baseline hs-CRP ≤5 mg/L.
- Source: raison2013.pdf.md RESULTS (paragraph containing standardized effect sizes); Figure 4
- Pass A: NO_SEMANTIC_RELATION - Witness reports effect-size differences at 12 weeks for infliximab vs placebo stratified by hs-CRP; it is not about the A2-H2 delayed-onset constraint and does not address absence of improvement within days-to-a-few-weeks.
- Pass B: WITNESS_ENTAILS_UNIT - Witness reports a standardized effect size difference specifically "at 12 weeks" (weeks-to-months timeframe) and contains no claim of improvement within days to a few weeks.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an effect size difference “at 12 weeks” for infliximab vs placebo by hs-CRP subgroup, but does not claim improvement occurs only after weeks–months or that it does not occur within days–few weeks (the unit’s discriminator).

### A2-H2-C2 x W-FRD-Q0003-04-c1-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses proposed PTX mechanisms (PDE inhibition/NOS activation) and beneficial effects after ischemic injury; it does not address whether prevention-only evidence can or cannot be treated as supporting a reversal/limitation-of-established-change claim.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness proposes PTX mechanisms (“phosphodiesterase inhibitor and nitric oxide synthase activator… increases tissue NO and intracellular cGMP”) to explain “beneficial effects… after ischemic injury,” but it does not mention prevention-only models nor any rule about how such evidence relates to “reversal/limitation-of-established-change.”

### A2-H2-C2 x W-FRD-Q0010-03-Q0010
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, Figure 2 (“Figure 2. The percentage of referrals made for PFPT by diagnosis”), PFPT referral percentages by diagnosis are: Pelvic Floor Dysfunction 49.5%, CPPS 39.6%, Testicular Pain/Groin Pain 28.4%, LUTS 3.6%; the denominator is not stated.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18, Figure 2 ("Figure 2. The percentage of referrals made for PFPT by diagnosis"), including the table "Diagnosis | Percentage of Patients Referred"
- Pass A: NO_SEMANTIC_RELATION - Witness reports PFPT referral percentages by diagnosis; it says nothing about prevention-only vs post-injury treatment evidence or how such evidence should be interpreted for reversal of established change.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PFPT referral percentages by diagnosis (e.g., “Pelvic Floor Dysfunction 49.5%… LUTS 3.6%”) and says nothing about prevention-only models or evidentiary constraints for reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0013-03-c4-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness defines bladder outlet obstruction criteria; it does not concern whether prevention-only models can be used to support a reversal/limitation-of-established-change claim.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only defines bladder outlet obstruction criteria (“sustained detrusor contraction >45 cm… flow rate <12 ml/s… radiographic evidence”), with no discussion of prevention-only evidence or how to interpret it for a reversal/limitation claim.

### A2-H2-C2 x W-FRD-Q0019-03-c3-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness reports in vitro PTX inhibition of neutrophil oxidative burst at 5 µmol/L; it does not discuss prevention-only models or evidentiary constraints for reversal of established structural change.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes an in vitro/whole-blood finding (“PTX… 5 µmol/l… inhibited… burst… to 76 ± 5% of control”) but does not address prevention-only models or any limitation on treating such evidence as supporting reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0020-02-c1-Q0020
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness describes dosing regimens of PTX in healthy volunteers; it does not address injury models, prevention-only vs post-injury treatment, or rules for treating prevention-only evidence as support for reversal.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports dosing in healthy volunteers (“treated orally… 5×400 mg/day for 2 days… or… 7 days”) without any claim about prevention-only models or whether such evidence can support reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0029-04-c4-Q0029
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.5.2. Fecal Calprotectin), fecal calprotectin <100 µg/g occurred in 18 patients (66.7%) on PTX vs 14 (53.8%) on placebo; <50 µg/g occurred in 6 (20%) on PTX vs 2 (6%) on placebo. Denominators are not explicitly stated.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.5.2. Fecal Calprotectin
- Pass A: NO_SEMANTIC_RELATION - Witness reports fecal calprotectin outcomes in PTX vs placebo; it does not speak to whether evidence limited to prevention-only models can support a reversal/limitation-of-established-change claim.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports fecal calprotectin outcomes under PTX vs placebo (“<100 µg/g… 66.7%… vs 53.8%”) but makes no statement about prevention-only models or an interpretive constraint regarding reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0029-04-c5-Q0029
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: NO_SEMANTIC_RELATION - Witness reports loss to follow-up reasons in PTX vs placebo groups; it does not concern prevention-only models or evidentiary treatment regarding reversal of established change.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes attrition (“lost to follow-up… developed severe disease… shifted to… steroid therapy”) and does not mention prevention-only models or any rule about what evidence supports a reversal/limitation-of-established-change claim.

### A2-H2-C2 x W-FRD-Q0048-02-c1-Q0048
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In 10.1016@s0041-13450001266-5.pdf.md (PATIENTS AND METHODS), pentoxifylline was dosed 150 mg IV 2 hours pre-op, 150 mg IV after graft reperfusion, and 300 mg IV 8 hours after grafting; then 1200 mg/day in three oral doses for 7 days.
- Source: 10.1016@s0041-13450001266-5.pdf.md PATIENTS AND METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness provides peri-operative and post-op PTX dosing schedule; it does not state anything about prevention-only models or whether such evidence can be treated as supporting reversal of established structural change.
- Pass B: PARTIALLY_COVERS - The regimen explicitly includes a prevention component (“150 mg IV 2 hours pre-op”) but also includes post-grafting dosing (“after graft reperfusion… 8 hours after grafting… then… for 7 days”); it bears on prevention-only vs post-injury timing but does not itself state whether reversal/limitation of established change was demonstrated.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only gives a clinical dosing schedule including pre-op and post-op dosing (“150 mg IV 2 hours pre-op… after graft reperfusion… then… for 7 days”) but does not state that prevention-only models cannot support reversal/limitation-of-established-change; it does not address the evidentiary-interpretation constraint in the unit.

### A2-H2-C2 x W-FRD-Q0063-01-c1-Q0063
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Sullivan-et-al-1988: Human PMNs incubated 30 min at 37°C with pentoxifylline 300 µg/ml decreased adherence to nylon vs diluent: 64.1±2.7% (n=16) vs 54.0±3.9% (n=6; P=0.031) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → PMN adherence).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → PMN adherence (opening paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness describes an in-vitro human PMN incubation with pentoxifylline reducing adherence to nylon; it does not discuss prevention-only vs post-injury treatment models or whether evidence supports a reversal/limitation-of-established-change claim.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in vitro incubation result (“PMNs incubated… with pentoxifylline… decreased adherence to nylon”) and contains no discussion of prevention-only models or whether such evidence can/cannot support reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0063-01-c4-Q0063
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: NO_SEMANTIC_RELATION - Witness reports pentoxifylline reducing FMLP-stimulated superoxide in PMNs in vitro; it contains no statements about prevention-only models, post-injury treatment, or evidentiary limits for reversal of established changes.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX reducing stimulated superoxide in PMNs (“reduced… superoxide… P=0.038”) but does not address prevention-only models or any evidentiary constraint about supporting reversal/limitation-of-established-change.

### A2-H2-C2 x W-FRD-Q0064-04-c1-Q0064
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In male Wistar–Kyoto rats (230–300 g), after baseline haemodynamics, investigators gave saline or pentoxifylline 3 mg/kg i.v., then 30 min later saline or E. coli LPS 10 mg/kg i.v., monitoring for 240 min (wu1999.pdf.md, Methods 2.1 Endotoxic shock).
- Source: wu1999.pdf.md Methods 2.1 Endotoxic shock
- Pass A: NO_SEMANTIC_RELATION - Witness gives an endotoxic shock protocol timing (PTX given before LPS); it does not make any claim about how prevention-only models should/should not be treated as evidence for reversal/limitation of established change.
- Pass B: PARTIALLY_COVERS - Witness describes pretreatment timing ('gave ... pentoxifylline ... then 30 min later ... LPS'), which is prevention-only relative to the insult; this aligns with the unit’s prevention-only concept but does not itself state the interpretive constraint, so it only partially covers.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-C2 x W-FRD-Q0072-04-c1-Q0072
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (METHODS > Subjects) reports that, during a two-year period after unilateral adrenalectomy in 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, symptomatic thyroid dysfunction developed in 3 of 24 patients.
- Source: Takasu1990_Cushings_Syndrome_Due.md METHODS > Subjects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness concerns postoperative thyroid dysfunction incidence ('3 of 24 patients') and is unrelated to prevention-only model evidence or reversal/limitation of established structural change.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-C2 x W-FRD-Q0078-02-c1-Q0078
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: desouza2009.pdf.md (Patients and methods > Study design): open-label 24-week-per-patient trial; all treated SSc patients received pentoxiphylline 800 mg/day associated with vitamin E 800 UI/day; results compared with a historical control group. desouza2009.pdf.md (Patients and methods > Historical control group): 9 diffuse SSc patients retrospectively used as controls received cyclophosphamide 0.5–1 g/m^2 during 6 months.
- Source: desouza2009.pdf.md Patients and methods > Study design; Patients and methods > Historical control group
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness describes an open-label clinical design with historical controls and dosing; it does not characterize evidence as prevention-only nor state any rule about interpreting prevention-only models.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only describes an "open-label 24-week-per-patient trial" with a "historical control group" and dosing; it does not mention prevention-only models nor any rule that such evidence cannot support reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0089-04-c2-Q0089
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is a speculative statement about potency after inflammation is triggered; it does not assert the unit’s methodological rule about how to treat prevention-only evidence supporting reversal/limitation-of-established-change.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness speculates PTX "may have no potent anti-inflammatory effect once inflammation has been triggered"; it does not discuss prevention-only models or the methodological constraint about treating prevention-only evidence as support for reversal/limitation claims.

### A2-H2-C2 x W-FRD-Q0090-04-c3-Q0090
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - An in vitro mechanistic finding ('preincubation with PTX... [Ca2+]i') does not discuss injury timing (pre vs post) in a prevention-only model or evidentiary interpretation for reversal of established change.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in vitro neutrophil result about "preincubation with PTX" affecting "[Ca2+]i" at certain concentrations; it contains no statement about prevention-only experimental models or how such evidence should be interpreted for reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0092-03-c4-Q0092
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports tolerability ('2 patients reported epigastric pain... complete remission') and contains no content about prevention-only models or reversal/limitation of established change.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about side effects/tolerability ("2 patients reported epigastric pain...") and does not address prevention-only models or any constraint on using prevention-only evidence to support reversal/limitation claims.

### A2-H2-C2 x W-FRD-Q0092-04-delanian20-c1-Q0092
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Delanian 2005 reports “44 eligible treated women” with complete long-term data; “All 44 patients were women” (delanian2005.pdf.md, PATIENTS AND METHODS → Population).
- Source: delanian2005.pdf.md PATIENTS AND METHODS → Population
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only specifies cohort sex/completeness ('All 44 patients were women') and does not address prevention-only vs post-injury treatment evidence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states cohort composition ("All 44 patients were women") and has no content about prevention-only models or evidentiary limits for reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is a clinical treatment study description ('open-label 24-week... pentoxifylline 800 mg/day plus vitamin E'), not a prevention-only model statement and not a methodological constraint about interpreting prevention-only evidence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes a treatment study design ("open-label, 24-week-per-patient trial" of PTX + vitamin E) but does not mention prevention-only models nor any rule about interpreting prevention-only evidence for reversal/limitation claims.

### A2-H2-C2 x W-FRD-Q0098-01-Q0098
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Witness is explicitly prevention-only timing ('45 min before hemorrhage' pretreatment), matching the unit’s concept of prevention-only evidence; however it does not state the normative constraint that such evidence cannot be treated as supporting reversal/limitation, so it only supplies a relevant example rather than entailing the unit.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness is an explicit pretreatment setup (PTX given "45 min before hemorrhage" under "Pentoxifylline Pretreatment"), which exemplifies prevention-only timing; but it does not state the unit's methodological conclusion that prevention-only evidence "cannot be treated as supporting" reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0131-03-c3-Q0131
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - A pharmacokinetic statement ('short half-life about 1.6 h') does not address whether evidence is prevention-only or includes post-injury reversal/limitation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports pharmacokinetics ("short half-life about 1.6 h") and does not address prevention-only models or constraints on using such evidence to support reversal/limitation claims.

### A2-H2-C2 x W-FRD-Q0131-03-c4-Q0131
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness describes toxicity ('80 mg/kg... hypotension, flushing, and convulsion') and contains no claim about prevention-only experimental design or reversal/limitation of established injury.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports toxicity ("PTX toxicity was reported at 80 mg/kg") and does not mention prevention-only model designs or the evidentiary rule about reversal/limitation of established change.

### A2-H2-C2 x W-FRD-Q0149-04-c4-Q0149
- Unit (CONTEXTUAL_CONSTRAINT): Evidence limited to prevention-only models cannot be treated as supporting A2-H2’s reversal/limitation-of-established-change claim.
- Witness: Raison2013 (raison2013.pdf.md, RESULTS): in subgroup mixed-effects models for repeated measures, standardized effect size difference at 12 weeks was “moderate to large, in opposite directions”: 0.41 favoring infliximab for baseline hs-CRP >5 mg/L, versus −0.82 favoring placebo for baseline hs-CRP ≤5 mg/L.
- Source: raison2013.pdf.md RESULTS (paragraph containing standardized effect sizes); Figure 4
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports effect sizes in Raison2013 at 12 weeks by hs-CRP subgroup; it does not mention prevention-only vs post-injury treatment timing or whether an established structural change is reversed/limited.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports subgroup effect sizes at 12 weeks by hs-CRP level; it does not discuss prevention-only models nor any limitation on treating prevention-only evidence as supporting reversal/limitation of established change.

### A2-H2-E1 x W-FRD-Q0003-04-c3-Q0003
- Unit (CORROBORATING_EXPECTATION): In established dysfunction, structural endpoints (e.g., stereology/collagen measures) should improve with PTX treatment.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX effects on detrusor contraction responses (functional physiology) and speculation about neural pathways; it does not report any structural endpoints (collagen/stereology) improving after dysfunction is established.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX effects on detrusor contractions to electric stimulation and lack of improvement to carbachol, plus a mechanistic assumption about cholinergic vs non-cholinergic pathways; it does not mention any structural endpoints (e.g., collagen/stereology) improving with PTX in established dysfunction.

### A2-H2-E1 x W-FRD-Q0007-03-Q0007
- Unit (CORROBORATING_EXPECTATION): In established dysfunction, structural endpoints (e.g., stereology/collagen measures) should improve with PTX treatment.
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns urothelial ATP and nitric oxide findings in men with detrusor underactivity/BPH and does not involve PTX treatment or any structural (collagen/stereology) improvement outcomes.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports urothelial ATP decreased and nitric oxide unchanged in men with detrusor underactivity/BPH; there is no PTX treatment and no claim about structural endpoint improvement in established dysfunction.

### A2-H2-E1 x W-FRD-Q0019-03-c3-Q0019
- Unit (CORROBORATING_EXPECTATION): In established dysfunction, structural endpoints (e.g., stereology/collagen measures) should improve with PTX treatment.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness states PTX inhibits neutrophil oxidative burst in whole blood at specific concentrations; it does not address established dysfunction in an organ or show improvement in structural endpoints with PTX treatment.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states PTX (5 µmol/l) inhibited FMLP-stimulated neutrophil oxidative burst (hydrogen peroxide production) in whole blood; it does not address PTX improving bladder/organ structural endpoints (collagen/stereology) in established dysfunction.

### A2-H2-E1 x W-FRD-Q0020-02-c1-Q0020
- Unit (CORROBORATING_EXPECTATION): In established dysfunction, structural endpoints (e.g., stereology/collagen measures) should improve with PTX treatment.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: NO_SEMANTIC_RELATION - Witness describes dosing regimens of PTX in healthy volunteers (methods only) and provides no report of structural endpoint improvement after established dysfunction.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes oral PTX dosing regimens in four healthy volunteers in Methods; it provides no outcomes and no report of structural endpoint improvement with PTX after established dysfunction.

### A2-H2-E1 x W-FRD-Q0044-04-c2-Q0044
- Unit (CORROBORATING_EXPECTATION): In established dysfunction, structural endpoints (e.g., stereology/collagen measures) should improve with PTX treatment.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - Witness reports absence of adverse effects in patients; it does not mention structural measures (e.g., collagen/stereology) or improvement after established dysfunction with PTX.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states adverse effects were not reported/observed with pentoxifylline; it makes no claim about improvement of structural endpoints (collagen/stereology) in established dysfunction with PTX treatment.

### A2-H2-E1 x W-FRD-Q0050-02-Q0050
- Unit (CORROBORATING_EXPECTATION): In established dysfunction, structural endpoints (e.g., stereology/collagen measures) should improve with PTX treatment.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses PTX safety/tolerability and common side effects; it does not report structural endpoint improvement with PTX started after dysfunction is established.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness characterizes PTX as safe/well tolerated and lists common side effects; it does not discuss established dysfunction or any structural endpoint improvement (stereology/collagen measures) with PTX.

### A2-H2-E2 x W-FRD-Q0003-04-c1-Q0003
- Unit (CORROBORATING_EXPECTATION): Functional improvement should follow structural change in time (structure improves first, then voiding improves).
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - The witness proposes biochemical mechanisms (NO/cGMP) for PTX’s beneficial effects on contractile function after ischemic injury, but provides no time-course showing structural change preceding later voiding/functional improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness proposes PTX mechanisms (“phosphodiesterase inhibitor and nitric oxide synthase activator… increases tissue NO and intracellular cGMP”) to explain “beneficial effects on contractile function after ischemic injury,” but contains no statement about temporal ordering where “structural change” occurs before later “voiding improves.”

### A2-H2-E2 x W-FRD-Q0007-01-c1-Q0007
- Unit (CORROBORATING_EXPECTATION): Functional improvement should follow structural change in time (structure improves first, then voiding improves).
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - This is a definitional quote of detrusor underactivity (reduced strength/duration causing prolonged/incomplete emptying), not evidence about temporal ordering of structural vs functional improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only quotes a definition of detrusor underactivity (“reduced strength and/or duration… prolonged bladder emptying… failure to achieve complete bladder emptying”), not a claim that structural improvement precedes functional/voiding improvement over time.

### A2-H2-E2 x W-FRD-Q0007-03-Q0007
- Unit (CORROBORATING_EXPECTATION): Functional improvement should follow structural change in time (structure improves first, then voiding improves).
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Reports cross-sectional biomarker differences (urothelial ATP decreased; NO no change) in men with DU and BPH, without any treatment time-course or structural-then-functional sequence.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports cross-sectional biomarker findings (“urothelial ATP… decreased” and “nitric oxide… no significant change”) in men with DU and BPH, with no longitudinal or temporal sequence relating structural change to later voiding/function improvement.

### A2-H2-E2 x W-FRD-Q0069-02-c3-Q0069
- Unit (CORROBORATING_EXPECTATION): Functional improvement should follow structural change in time (structure improves first, then voiding improves).
- Witness: refsum1994.pdf.md (RESULTS) reports ANOVA differences between study groups for intracellular sodium (P<.001), intracellular potassium (P<.05), and intracellular chloride (P<.001), but not intracellular water; the Bonferroni test compared the means of the groups receiving PTF to those of the CLP group at each time point.
- Source: refsum1994.pdf.md RESULTS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports group differences for intracellular sodium/potassium/chloride (“ANOVA differences…”) but does not describe structural remodeling improving before later voiding improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports electrolyte group differences and comparisons “at each time point” (intracellular sodium/potassium/chloride by ANOVA/Bonferroni) but does not mention bladder structure or voiding/function outcomes, nor that structure improves before function.

### A2-H2-E2 x W-FRD-Q0090-04-c3-Q0090
- Unit (CORROBORATING_EXPECTATION): Functional improvement should follow structural change in time (structure improves first, then voiding improves).
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is an in vitro neutrophil [Ca2+]i pharmacology result (“500 µmol/l reduced…”) and does not mention tissue structural change or delayed functional/voiding improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness is an in vitro neutrophil calcium result (“preincubation with PTX… 500 µmol/l reduced resting… and stimulated [Ca2+]i”), which does not address structural change or a delayed subsequent improvement in voiding/function.

### A2-H2-E2 x W-FRD-Q0102-04-c2-Q0102
- Unit (CORROBORATING_EXPECTATION): Functional improvement should follow structural change in time (structure improves first, then voiding improves).
- Witness: Chung2014 reports detrusor biopsy in UAB showed ~4× more disruptive cells than normal bladder function, and no significant correlation between patient age and disruptive-cell number in the detrusor wall, interpreted as suggesting it is not aging per se (chung2014.pdf.md, “## Making the Diagnosis”).
- Source: chung2014.pdf.md ## Making the Diagnosis (paragraph beginning “Electron microscopic examination may reveal…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses disruptive cells in detrusor and lack of correlation with age (“no significant correlation…suggesting it is not aging per se”) but provides no structural-vs-functional time-course or subsequent voiding improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness describes detrusor biopsy findings (“~4× more disruptive cells… no significant correlation… with age”) and an interpretation about aging, but provides no time-course linking earlier structural improvement to later voiding/functional improvement.

### A2-H2-E2 x W-FRD-Q0104-03-c6-Q0104
- Unit (CORROBORATING_EXPECTATION): Functional improvement should follow structural change in time (structure improves first, then voiding improves).
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The text is about hs-CRP longitudinal effects (“significant treatment effect…no time effect…no treatment×time interaction”) and does not address bladder structure or voiding function time-ordering.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports longitudinal hs-CRP statistics (“significant treatment effect… no time effect… no treatment×time interaction”) and does not discuss bladder structural changes or whether such changes precede voiding/functional improvement.

### A2-H2-E2 x W-FRD-Q0148-01-c1-Q0148
- Unit (CORROBORATING_EXPECTATION): Functional improvement should follow structural change in time (structure improves first, then voiding improves).
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports only long-term lack of LUTS/Qmax/PVR/BCI improvement after TURP (“no significant LUTS improvement…no significant change…including BCI”) and says nothing about structural change occurring earlier than function.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-E3 x W-FRD-Q0098-01-Q0098
- Unit (CORROBORATING_EXPECTATION): Benefit should accumulate with longer duration of treatment and persist after withdrawal.
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports acute IV PTX “40 mg/kg over 15 min…decreased MAP…increased HR…then ‘they all died’”; it does not address longer treatment duration yielding greater benefit nor persistence after withdrawal.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes an acute IV PTX pretreatment in rats with short-term physiologic changes and that "they all died"; it makes no claim that benefit increases with longer treatment duration or that any benefit persists after withdrawal.

### A2-H2-E3 x W-FRD-Q0108-03-Q0108
- Unit (CORROBORATING_EXPECTATION): Benefit should accumulate with longer duration of treatment and persist after withdrawal.
- Witness: alewijnse2003.pdf.md (Results → Participants and non-response): Loss to follow-up numbers were not significantly different between study groups. Twenty-six women (20% of 129) withdrew: n=10 before therapy started, n=4 during treatment, n=12 during follow-up measurements. Questionnaire data: those lost had more frequent (U=978.5, P=0.029) and more severe (U=1036.5, P=0.045) wet episodes at pre-test.
- Source: alewijnse2003.pdf.md Results → Participants and non-response
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses “Loss to follow-up…not significantly different” and baseline wet episodes; no claims about treatment duration effects or sustained benefit after stopping PTX.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports loss-to-follow-up and baseline symptom differences ("withdrew...during treatment...during follow-up measurements"; "those lost had more frequent...wet episodes"); it does not address treatment-duration-dependent benefit or persistence after stopping treatment.

### A2-H2-E3 x W-FRD-Q0131-03-c3-Q0131
- Unit (CORROBORATING_EXPECTATION): Benefit should accumulate with longer duration of treatment and persist after withdrawal.
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only reports “PTX has short half-life about 1.6 h,” which does not state treatment-duration-dependent benefit or post-withdrawal persistence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states a pharmacokinetic fact: "PTX has short half-life about 1.6 h"; this does not support that benefits accumulate with longer treatment or persist after withdrawal.

### A2-H2-E3 x W-FRD-Q0131-03-c4-Q0131
- Unit (CORROBORATING_EXPECTATION): Benefit should accumulate with longer duration of treatment and persist after withdrawal.
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states “PTX toxicity was reported at 80 mg/kg” causing adverse effects; nothing about accumulating benefit with longer treatment or persistence after withdrawal.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns toxicity at a high dose ("PTX toxicity...at 80 mg/kg" causing hypotension/flushing/convulsion) and provides no statement about increasing benefit with longer treatment or persistence after withdrawal.

### A2-H2-E3 x W-FRD-Q0148-01-c1-Q0148
- Unit (CORROBORATING_EXPECTATION): Benefit should accumulate with longer duration of treatment and persist after withdrawal.
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about “patients with TURP showed no significant LUTS improvement” and voiding parameters after 10+ years; it is not about PTX duration effects or post-withdrawal persistence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about long-term outcomes after TURP ("no significant LUTS improvement" after 10+ years) and is not about PTX treatment duration or post-withdrawal persistence of benefit.

### A2-H2-E3 x W-FRD-Q0149-04-c2-Q0149
- Unit (CORROBORATING_EXPECTATION): Benefit should accumulate with longer duration of treatment and persist after withdrawal.
- Witness: In the full sample, response (≥50% reduction in HAM-D at any point) was 50% in each group, with no between-group difference (χ2=0.00, P=.99) (raison2013.pdf.md, RESULTS; Figure 6 caption).
- Source: raison2013.pdf.md RESULTS; Figure 6 caption (definition of response)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports “50% in each group, with no between-group difference” in HAM-D response; it does not address PTX exposure duration, accumulation of benefit, or persistence after withdrawal.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports equal HAM-D response rates between groups ("50% in each group") without mentioning treatment duration effects or whether benefits persist after withdrawal.

### A2-H2-R1 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness proposes PTX mechanisms via “increases tissue NO and intracellular cGMP” to explain “beneficial effects on contractile function after ischemic injury” (cardiac papillary muscle), not reversal/limitation of bladder structural pathology (fibrosis/remodeling) linked to impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness proposes PTX mechanisms ("phosphodiesterase inhibitor and nitric oxide synthase activator" increasing "tissue NO and intracellular cGMP") to explain "beneficial effects on contractile function after ischemic injury" in cardiac papillary muscle; it does not mention voiding or PTX reversing/limiting bladder structural change (fibrosis/remodeling/tissue damage) contributing to impaired voiding.

### A2-H2-R1 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports functional changes (“improved detrusor contractions to electric stimulation”) and a pathway inference (not cholinergic), but does not mention measured structural change (fibrosis/remodeling/tissue damage) being reversed/limited by PTX.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0007-03-Q0007
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports biomarkers (urothelial ATP decreased; NO no significant change) in men with DU+BPH, with no PTX treatment and no claim about structural pathology reversal/limitation improving voiding.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0007-04-c4-Q0007
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: NO_SEMANTIC_RELATION - Witness discusses need for markers to avoid an irreversible “point of no return” in bladder decompensation, but makes no claim about PTX reversing/limiting fibrosis/remodeling/tissue damage contributing to impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0010-04-c1-Q0010
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness is a methods description of a retrospective chart review identified by ICD codes; it contains no PTX mechanism or structural-change (fibrosis/remodeling) reversal/limitation claim.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns diagnostic criteria for pseudodyssynergia using uroflowmetry patterns; it does not involve PTX treatment or structural pathology reversal/limitation.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0014-02-Q0014
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: NO_SEMANTIC_RELATION - Witness reports ultrasound parameters (DWT ≤1.23 mm, capacity >445 ml) to detect DU; it does not mention PTX or any PTX-driven reversal/limitation of fibrosis/remodeling/tissue damage.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX inhibits neutrophil oxidative burst (hydrogen peroxide production) in whole blood in vitro; it does not address voiding impairment or PTX reversing/limiting bladder structural changes (fibrosis/remodeling).
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: NO_SEMANTIC_RELATION - Witness provides prevalence data for DU in diabetic men with LUTS; no PTX intervention and no statement about reversing/limiting structural pathology contributing to impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0029-04-c4-Q0029
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.5.2. Fecal Calprotectin), fecal calprotectin <100 µg/g occurred in 18 patients (66.7%) on PTX vs 14 (53.8%) on placebo; <50 µg/g occurred in 6 (20%) on PTX vs 2 (6%) on placebo. Denominators are not explicitly stated.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.5.2. Fecal Calprotectin
- Pass A: NO_SEMANTIC_RELATION - Witness reports fecal calprotectin outcomes in a PTX vs placebo context (GI inflammation marker), not bladder/voiding or PTX reversing/limiting bladder structural change (fibrosis/remodeling) contributing to impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0029-04-c5-Q0029
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: NO_SEMANTIC_RELATION - Witness reports loss to follow-up and switching to steroids in trial groups; it contains no claim about PTX improving voiding via reversal/limitation of structural bladder pathology.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0034-02-bortnick20-c3-Q0034
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Bortnick et al. (2020) report that risk of self-harm was elevated significantly during the initial 18 months on a 5-ARI, though there was no increased risk of suicide (bortnick2020.pdf.md, Medical therapy → 5-alpha reductase inhibitors).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → subsection “5-alpha reductase inhibitors”
- Pass A: NO_SEMANTIC_RELATION - Witness concerns 5-ARI self-harm risk and suicide; unrelated to PTX, voiding mechanisms, or reversal/limitation of bladder structural changes.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R1 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: NO_SEMANTIC_RELATION - Witness describes CombAT outcomes for combination BPH therapy; it does not discuss PTX or structural pathology reversal/limitation as a voiding mechanism.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses CombAT outcomes for BPH combination therapy (“greater risk reduction in acute urinary retention or BPH-related surgery…clinical progression”) and does not mention PTX or any mechanism involving reversing/limiting structural change (fibrosis/remodeling/tissue damage) to improve voiding.

### A2-H2-R1 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses PTX safety/tolerability and side effects (GI symptoms, dizziness) but says nothing about voiding, structural change (fibrosis/remodeling), or reversal/limitation of pathology.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX safety/tolerability (“very safe”, “usually well tolerated”, GI symptoms, dizziness) but makes no claim about voiding improvement or reversing/limiting structural pathology (fibrosis/remodeling/tissue damage).

### A2-H2-R1 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX inhibits PDE 1–5 with IC50 values, which is a pharmacologic property and does not address reversing/limiting structural pathology contributing to impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states a pharmacologic property (“pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L”) without linking it to voiding improvement via reversal/limitation of structural change.

### A2-H2-R1 x W-FRD-Q0061-02-c2-Q0061
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: In siu2003.pdf.md (RESULTS), the authors report: “The mean time between the first and fourth visits was 213.40 days (30.50 weeks).”
- Source: siu2003.pdf.md RESULTS
- Pass A: NO_SEMANTIC_RELATION - Witness only reports the time between study visits (213.40 days) and makes no claim about PTX, voiding improvement, or structural changes like fibrosis/remodeling.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only reports study timing (“mean time between the first and fourth visits was 213.40 days”) and contains no content about PTX, voiding, or structural changes such as fibrosis/remodeling.

### A2-H2-R1 x W-FRD-Q0061-02-c5-Q0061
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: In siu2003.pdf.md (Abstract (Results)), the authors report the pelvic muscle training program “appears to be able to reduce the overall urinary incontinence episodes by 85.2%.”
- Source: siu2003.pdf.md Abstract (Results)
- Pass A: NO_SEMANTIC_RELATION - Witness concerns pelvic muscle training reducing incontinence episodes; it does not involve PTX or structural reversal/limitation related to impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness attributes reduction in urinary incontinence episodes to a “pelvic muscle training program” and does not involve PTX or any structural-change reversal/limitation mechanism affecting voiding.

### A2-H2-R1 x W-FRD-Q0063-01-c4-Q0063
- Unit (REQUIRED_SUPPORT): PTX’s materially supported mechanism improves voiding by reversing or limiting structural change (e.g., fibrosis/remodeling/tissue damage) that contributes to impaired voiding.
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX reduced FMLP-stimulated superoxide in PMNs (an in vitro neutrophil function measure), not structural pathology (fibrosis/remodeling) in a voiding-impaired cohort/model.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in vitro immune-cell effect (“Pentoxifylline…reduced…superoxide…in…PMNs”) and does not address voiding outcomes or structural pathology reversal/limitation (fibrosis/remodeling/tissue damage).

### A2-H2-R2 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness only gives the ICS definition of detrusor underactivity (reduced strength/duration causing prolonged/incomplete emptying) and says nothing about pentoxifylline (PTX) treatment timing or onset of voiding improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only provides the ICS definition of detrusor underactivity (“contraction of reduced strength and/or duration… prolonged bladder emptying… failure to achieve complete bladder emptying”) and does not mention PTX or any timing/onset of voiding improvement.

### A2-H2-R2 x W-FRD-Q0007-04-c4-Q0007
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: NO_SEMANTIC_RELATION - Witness discusses a need for markers to avoid a “point of no return” for irreversible bladder decompensation, but does not mention PTX or any timeline for voiding improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses needing markers to avoid a “point of no return” for “irreversible bladder decompensation and failure,” but says nothing about PTX treatment or whether voiding improvement occurs only after weeks to months vs within days/weeks.

### A2-H2-R2 x W-FRD-Q0009-04-Q0009
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Chuang2015.pdf.md (EPIDEMIOLOGY) says Thomas et al. reported that, in men with untreated detrusor underactivity and minimum 10-year urodynamic follow-up, detrusor underactivity was not progressive in most nonneurogenic male patients and often did not result in chronic urinary retention.
- Source: chuang2015.pdf.md EPIDEMIOLOGY section (paragraph beginning “Thomas and colleagues9 reported…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports long-term natural history (10-year follow-up) of untreated detrusor underactivity being often non-progressive, which does not address PTX effects or whether improvement occurs only after weeks to months.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports natural history in “untreated detrusor underactivity” over “10-year urodynamic follow-up” (often not progressive), which does not address PTX or the timing of improvement with PTX.

### A2-H2-R2 x W-FRD-Q0039-02-Q0039
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In SILODOSING (s00345-024-04974-7.pdf.md), both groups continued silodosin 8 mg once daily for 12 weeks (Patients and methods > Procedures > Experimental and control groups). The experimental group also did PFMT 30 min/day, 5 days/week for 12 weeks, supervised by a physiotherapist weekly (same). Anticholinergics/β3-mimetics use within 4 weeks pre–visit 1 and during study excluded (Patients and methods > Exclusion criteria).
- Source: s00345-024-04974-7.pdf.md Patients and methods > Procedures > Experimental and control groups; Patients and methods > Exclusion criteria; Patients and methods > Allocation
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness concerns silodosin and pelvic floor muscle training and excludes other drugs; it does not mention pentoxifylline or voiding improvement timing with PTX.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0042-03-c2-Q0042
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Reports only side effects and completion of treatment; no claim about measurable voiding improvement or when it occurs.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness statements are about safety/side effects (“Adverse effects were not reported…”, “No adverse effects…”) and do not mention voiding improvement or its timing.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0048-02-c1-Q0048
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In 10.1016@s0041-13450001266-5.pdf.md (PATIENTS AND METHODS), pentoxifylline was dosed 150 mg IV 2 hours pre-op, 150 mg IV after graft reperfusion, and 300 mg IV 8 hours after grafting; then 1200 mg/day in three oral doses for 7 days.
- Source: 10.1016@s0041-13450001266-5.pdf.md PATIENTS AND METHODS
- Pass A: NO_SEMANTIC_RELATION - Describes PTX dosing regimen around transplant and then 7 days oral dosing, but makes no claim about timing of voiding improvement (days vs weeks/months) or any functional outcomes.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Reports safety/tolerability (GI symptoms, dizziness) of PTX; does not address voiding improvement or the timeline to improvement.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - States PTX inhibits PDE 1–5 with IC50 50–200 µmol/L; provides no information about voiding outcomes or when improvement occurs.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0061-02-c2-Q0061
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In siu2003.pdf.md (RESULTS), the authors report: “The mean time between the first and fourth visits was 213.40 days (30.50 weeks).”
- Source: siu2003.pdf.md RESULTS
- Pass A: PARTIALLY_COVERS - Gives a follow-up/visit interval of 213.40 days (30.50 weeks), which is consistent with a weeks-to-months observation timeline, but it does not state that voiding improvement with PTX occurs only after weeks/months nor that it does not occur within days-to-weeks.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - In vitro PMN lysozyme release changes with PTX; not about voiding improvement timing in patients/clinically attainable exposure for voiding outcomes.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0065-02-c3-Q0065
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In peritonitis induction (PI), PTF pretreatment reduced neutrophil adhesiveness: half-clearance time increased significantly by 100% before PI and by a further 238% at 30 min after PI; groups differed significantly both before and at 30 min (10.1097@00003246-199002000-00012.pdf.md, RESULTS > Neutrophil Adhesiveness).
- Source: 10.1097@00003246-199002000-00012.pdf.md RESULTS > Neutrophil Adhesiveness
- Pass A: NO_SEMANTIC_RELATION - Reports acute (30 min) changes in neutrophil adhesiveness after PTF pretreatment in peritonitis induction; unrelated to voiding improvement timeline with PTX.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R2 x W-FRD-Q0098-01-Q0098
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness describes IV PTX 40 mg/kg effects on “MAP/HR/WBC” and that “they all died,” with no voiding endpoints or improvement timeline.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports acute IV PTX effects in male rats on MAP/HR/WBC/PMN and that “they all died” in shock; it contains no statement about urinary voiding outcomes or any timing of voiding improvement (days vs weeks/months).

### A2-H2-R2 x W-FRD-Q0104-03-c6-Q0104
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports “significant treatment effect… on hs-CRP… but no time effect and no treatment×time interaction,” which is unrelated to PTX or voiding improvement timing.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses infliximab vs placebo effects on hs-CRP (treatment effect; no time effect/interaction), not pentoxifylline and not any voiding/LUTS endpoint or time-to-improvement claim.

### A2-H2-R2 x W-FRD-Q0131-03-c3-Q0131
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only reports “PTX has short half-life about 1.6 h,” not when voiding improves with treatment.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states “PTX has short half-life about 1.6 h,” which does not address whether meaningful voiding improvement occurs only after weeks to months vs within days/weeks.

### A2-H2-R2 x W-FRD-Q0131-03-c4-Q0131
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states “PTX toxicity was reported at 80 mg/kg… hypotension, flushing, and convulsion,” which is unrelated to voiding improvement timing.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX toxicity at 80 mg/kg (hypotension, flushing, convulsion) and does not mention voiding improvement or the timing of any therapeutic effect.

### A2-H2-R2 x W-FRD-Q0148-01-c1-Q0148
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about “patients with TURP showed no significant LUTS improvement… and no significant change… in Qmax, PVR… including BCI,” which does not address PTX or timing of PTX effects.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about long-term (10+ years) TURP follow-up showing no significant LUTS/voiding parameter improvement; it is unrelated to PTX treatment and provides no support about PTX effect timing.

### A2-H2-R2 x W-FRD-Q0149-04-c2-Q0149
- Unit (REQUIRED_SUPPORT): Meaningful voiding improvement with PTX should occur only after weeks to months of treatment (not within days to a few weeks).
- Witness: In the full sample, response (≥50% reduction in HAM-D at any point) was 50% in each group, with no between-group difference (χ2=0.00, P=.99) (raison2013.pdf.md, RESULTS; Figure 6 caption).
- Source: raison2013.pdf.md RESULTS; Figure 6 caption (definition of response)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses “≥50% reduction in HAM-D” with “no between-group difference” (infliximab vs placebo), not PTX and not voiding improvement or its time course.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports depression response (≥50% HAM-D reduction) with no between-group difference for infliximab vs placebo; it does not involve PTX or urinary voiding improvement timing.

### A2-H2-R3 x W-FRD-Q0003-04-c1-Q0003
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses proposed biochemical mechanisms for PTX’s beneficial effects on contractile function after ischemic injury (NO/cGMP), but does not report early (days–weeks) voiding-function timecourse or lack of early functional change.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness proposes PTX biochemical mechanisms ("phosphodiesterase inhibitor"; "nitric oxide synthase activator"; increases "NO"/"cGMP") to explain beneficial effects on "contractile function after ischemic injury"; it does not mention voiding function or an early (days–weeks) timecourse of change during PTX.

### A2-H2-R3 x W-FRD-Q0007-03-Q0007
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Witness is about urothelial ATP and nitric oxide levels in men with DU/BPH (Cho et al.), not PTX treatment effects or early voiding-function changes during PTX.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0010-02-Q0010
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md (MP75-18 > RESULTS), the mean wait time between referral and appointment was 54.7 days (SD 37.3; range 1–215).
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18 > RESULTS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports “mean wait time… was 54.7 days” for PFPT scheduling, unrelated to pentoxifylline or early voiding functional change.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about diagnosing pseudodyssynergia requiring uroflowmetry patterns, not pentoxifylline treatment or early voiding improvement.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports PTX “inhibited… burst… hydrogen peroxide production to 76 ± 5%,” which is an immune assay, not voiding function or early clinical change.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0020-02-c1-Q0020
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only states dosing timing (“treated orally with pentoxifylline… for 2 days… or… 7 days”) but provides no report about voiding function or lack of early change.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports “79% had detrusor underactivity (DU)” in diabetics, without any pentoxifylline treatment or early treatment-response claim.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0029-04-c4-Q0029
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.5.2. Fecal Calprotectin), fecal calprotectin <100 µg/g occurred in 18 patients (66.7%) on PTX vs 14 (53.8%) on placebo; <50 µg/g occurred in 6 (20%) on PTX vs 2 (6%) on placebo. Denominators are not explicitly stated.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.5.2. Fecal Calprotectin
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports fecal calprotectin thresholds (“<100 µg/g… on PTX vs placebo”), which is not voiding function and does not address early voiding change.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0034-02-bortnick20-c3-Q0034
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Bortnick et al. (2020) report that risk of self-harm was elevated significantly during the initial 18 months on a 5-ARI, though there was no increased risk of suicide (bortnick2020.pdf.md, Medical therapy → 5-alpha reductase inhibitors).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → subsection “5-alpha reductase inhibitors”
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness concerns “risk of self-harm… during the initial 18 months on a 5-ARI,” not pentoxifylline or early voiding improvement.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0034-03-c4-Q0034
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Saw palmetto 320 mg daily may cause GI upset and headache and “may enhance the anticoagulation effect of warfarin” (fdp03812573_1.pdf.md, TABLE “Benign Prostatic Enlargement Medications”).
- Source: fdp03812573_1.pdf.md TABLE “Benign Prostatic Enlargement Medications” → Natural Products → Saw palmetto row (Daily Doses and Comments columns).
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness states “Saw palmetto… may cause GI upset… may enhance… warfarin,” unrelated to PTX or early voiding function change.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0034-04-bortnick20-c1-Q0034
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: bortnick2020.pdf.md (“Medical therapy”→“Combination therapy” MTOPS paragraph) reports MTOPS studied finasteride+doxazosin in 3000 men (mean age 62.6 years, SD 7.3) and found combination therapy improved voiding symptoms and maximum urinary flow rate more than either alone, prevented BPH progression better, and reduced the long-term risk of acute urinary retention and need for invasive therapy.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (MTOPS paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports MTOPS findings for “finasteride+doxazosin,” not pentoxifylline or early (days–weeks) voiding response on PTX.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0034-04-bortnick20-c2-Q0034
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In CombAT, 58% of patients were over 65; combination therapy had greater risk reduction in acute urinary retention or BPH-related surgery, and a greater reduction in relative risk of clinical progression, than either monotherapy (bortnick2020.pdf.md, “Medical therapy” → “Combination therapy”).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (CombAT sentences)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness discusses “combination therapy… risk reduction in acute urinary retention or BPH-related surgery,” with no mention of PTX or early timepoints of voiding change.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R3 x W-FRD-Q0039-02-Q0039
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In SILODOSING (s00345-024-04974-7.pdf.md), both groups continued silodosin 8 mg once daily for 12 weeks (Patients and methods > Procedures > Experimental and control groups). The experimental group also did PFMT 30 min/day, 5 days/week for 12 weeks, supervised by a physiotherapist weekly (same). Anticholinergics/β3-mimetics use within 4 weeks pre–visit 1 and during study excluded (Patients and methods > Exclusion criteria).
- Source: s00345-024-04974-7.pdf.md Patients and methods > Procedures > Experimental and control groups; Patients and methods > Exclusion criteria; Patients and methods > Allocation
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about “silodosin 8 mg… for 12 weeks” and PFMT procedures, not pentoxifylline or early voiding response.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses silodosin 8 mg daily, PFMT regimen, and exclusion of anticholinergics/β3-mimetics; it does not mention pentoxifylline (PTX) or any early voiding/urinary functional change in the first days–weeks of PTX treatment.

### A2-H2-R3 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness states only “Adverse effects were not reported” / “No adverse effects… were observed,” which concerns safety, not early voiding function or lack of early improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states only that “Adverse effects were not reported” / “No adverse effects of pentoxifylline treatment were observed,” which addresses safety, not early voiding function or early functional change during PTX treatment.

### A2-H2-R3 x W-FRD-Q0048-02-c1-Q0048
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In 10.1016@s0041-13450001266-5.pdf.md (PATIENTS AND METHODS), pentoxifylline was dosed 150 mg IV 2 hours pre-op, 150 mg IV after graft reperfusion, and 300 mg IV 8 hours after grafting; then 1200 mg/day in three oral doses for 7 days.
- Source: 10.1016@s0041-13450001266-5.pdf.md PATIENTS AND METHODS
- Pass A: NO_SEMANTIC_RELATION - Witness only reports PTX dosing schedule (IV peri-op then oral for 7 days) and says nothing about early voiding functional change or lack of improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides a PTX dosing schedule (peri-operative IV doses and “1200 mg/day… for 7 days”) but makes no claim about voiding function or whether there is little early functional change in voiding.

### A2-H2-R3 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - Witness describes safety/tolerability (GI symptoms, dizziness) and does not address voiding function outcomes or timing of functional change.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness characterizes PTX as “very safe”/“well tolerated” and lists adverse symptoms; it does not discuss voiding function outcomes or their timing (first days to weeks).

### A2-H2-R3 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - Witness reports PDE inhibition and IC50 values; no claim about voiding function or early vs late treatment effects.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX inhibits “PDE 1–5” with “IC50 values 50–200 μmol/L,” which is mechanistic and does not address early voiding functional changes during PTX treatment.

### A2-H2-R3 x W-FRD-Q0061-02-c2-Q0061
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In siu2003.pdf.md (RESULTS), the authors report: “The mean time between the first and fourth visits was 213.40 days (30.50 weeks).”
- Source: siu2003.pdf.md RESULTS
- Pass A: NO_SEMANTIC_RELATION - Witness gives visit timing (mean 213.40 days between first and fourth visits) but makes no claim about PTX or early voiding functional change.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports only visit spacing (“mean time between the first and fourth visits was 213.40 days”); it does not mention PTX or early voiding function changes.

### A2-H2-R3 x W-FRD-Q0061-02-c5-Q0061
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In siu2003.pdf.md (Abstract (Results)), the authors report the pelvic muscle training program “appears to be able to reduce the overall urinary incontinence episodes by 85.2%.”
- Source: siu2003.pdf.md Abstract (Results)
- Pass A: NO_SEMANTIC_RELATION - Witness is about pelvic muscle training reducing urinary incontinence episodes; it is not about PTX or early lack of voiding improvement during PTX treatment.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness says pelvic muscle training “appears to be able to reduce… urinary incontinence episodes by 85.2%,” which is not about PTX and not about lack of early voiding change during PTX treatment.

### A2-H2-R3 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX reducing lysozyme release in PMNs under LPS-conditioned medium; no mention of voiding function or early clinical response timing.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX reduced lysozyme release in PMNs under LPS-conditioned medium; it contains no information on urinary voiding function or early functional change in patients taking PTX.

### A2-H2-R3 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX effects on neutrophil calcium transients at various concentrations; does not address voiding outcomes or early functional change during PTX treatment.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes PTX effects on neutrophil calcium transients at given concentrations (e.g., “up to 50 µmol/L changed neither…; 500 µmol/L reduced…”); it does not address voiding function or early clinical urinary changes during PTX treatment.

### A2-H2-R3 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Witness is speculation about anti-inflammatory potency once inflammation is triggered; it does not report early voiding function being unchanged in the first days to weeks of PTX.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness speculates PTX “may have no potent anti-inflammatory effect once inflammation has been triggered”; this is not a statement about early voiding functional change in the first days to weeks of PTX treatment.

### A2-H2-R3 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): There should be little early functional change in voiding during the first days to few weeks of PTX treatment.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports neutrophil [Ca2+]i changes (or lack thereof) with PTX; no claim about urinary voiding function or early treatment timepoints.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports neutrophil [Ca2+]i findings with PTX preincubation (no change up to 50 µmol/L; reduction at 500 µmol/L); it provides no evidence about early voiding functional change during PTX treatment.

### A2-H2-R4 x W-FRD-Q0007-01-c1-Q0007
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness only gives the ICS definition of detrusor underactivity (reduced strength/duration causing prolonged/failed emptying) and does not mention structural pathology (fibrosis/remodeling/tissue damage) or a causal/consequential link to impaired voiding in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only quotes the ICS definition of detrusor underactivity as “contraction of reduced strength and/or duration” leading to prolonged/failure of emptying; it does not mention any structural change (e.g., remodeling/fibrosis) nor that such change is functionally consequential in the cohort.

### A2-H2-R4 x W-FRD-Q0007-03-Q0007
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports biochemical marker differences (urothelial ATP decreased; nitric oxide unchanged) in men with DU+BPH, not structural change, and does not claim structural pathology is functionally relevant to impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports biochemical findings (“urothelial ATP was significantly decreased… nitric oxide showed no significant change”) in men with DU+BPH, without any claim about structural change being present or contributing to impaired voiding.

### A2-H2-R4 x W-FRD-Q0007-04-c4-Q0007
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: PARTIALLY_COVERS - Witness mentions a 'point of no return' with 'irreversible bladder decompensation and failure,' implying irreversible/structural-type deterioration could matter, but it does not show or argue that specific structural pathology (fibrosis/remodeling/tissue damage) is consequentially linked to impaired voiding in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness mentions a “point of no return” with “irreversible bladder decompensation and failure,” which gestures toward lasting/possibly structural deterioration being relevant to dysfunction, but it does not state that structural change is present and consequentially contributes to impaired voiding in the specified cohort.

### A2-H2-R4 x W-FRD-Q0009-02-c2-Q0009
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: Chuang2015.pdf.md (## EPIDEMIOLOGY) summarizes Abarbanel & Marcus: in 181 LUTS patients aged ≥70 (82 men, 99 women), impaired detrusor contractility was defined urodynamically as Qmax <10 mL/s plus detrusor pressure <30 cm H2O, and was reported in 48% of men and 12% of women.
- Source: chuang2015.pdf.md ## EPIDEMIOLOGY (paragraph beginning “In men, detrusor underactivity may be caused… Abarbanel and Marcus…”)
- Pass A: NO_SEMANTIC_RELATION - Witness provides epidemiologic prevalence and a urodynamic definition of impaired detrusor contractility in older LUTS patients, with no statement about structural pathology being present or causally contributing to impaired voiding.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides prevalence and a urodynamic definition (Qmax <10 mL/s plus detrusor pressure <30 cm H2O) of impaired detrusor contractility in older LUTS patients; it does not assert structural change or a causal/functional contribution of structure to impaired voiding.

### A2-H2-R4 x W-FRD-Q0014-02-Q0014
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness says 'DWT ≤1.23 mm plus bladder capacity >445 ml' can 'detect' or 'predict DU' (PPV/NPV), but does not describe fibrosis/remodeling/tissue damage or argue such structural pathology contributes causally to impaired voiding.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness claims ultrasound “DWT ≤1.23 mm plus bladder capacity >445 ml” can “detect”/“predict DU” (PPV/NPV), but does not state that structural change must be present and functionally consequential to impaired voiding in the cohort (prediction ≠ structural causation).

### A2-H2-R4 x W-FRD-Q0018-01-Q0018
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: Bortnick et al. 2020 says surgical therapy is recommended for recurrent UTIs secondary to BPH, renal insufficiency secondary to BPH, recurrent bladder stones or gross hematuria from BOO due to BPH, refractory urinary retention secondary to BPH, and/or LUTS that have failed or unwillingness to consider other therapies (bortnick2020.pdf.md, “Alternative minimally invasive/surgical procedures to TURP”).
- Source: bortnick2020.pdf.md Section: “Alternative minimally invasive/surgical procedures to TURP” (paragraph beginning “Overall, surgical therapy is recommended…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness lists when 'surgical therapy is recommended' (recurrent UTIs, renal insufficiency, stones, hematuria, refractory retention, failed LUTS therapy) without asserting bladder structural remodeling/fibrosis causing impaired voiding.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R4 x W-FRD-Q0023-01-c1-Q0023
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: Osman2018.pdf.md (## Diagnostic aspects → ### Detrusor contraction strength → #### 2. Projected isovolumetric pressure (PIP)) suggests PIP groupings: >150 strong contractility; 100–150 normal; 50–100 weak; <50 very weak.
- Source: osman2018.pdf.md ## Diagnostic aspects → ### Detrusor contraction strength → #### 2. Projected isovolumetric pressure (PIP)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only 'suggests PIP groupings' for contractility strength (>150 strong ... <50 very weak) and does not address structural change (fibrosis/remodeling) or its functional contribution to impaired voiding.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R4 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports percentages with DU, delayed first voiding sense, and increased bladder capacity in diabetic men with LUTS, but says nothing about fibrosis/remodeling/tissue damage or that any structural change is functionally/causally linked to impaired voiding.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R4 x W-FRD-Q0148-04-Q0148
- Unit (REQUIRED_SUPPORT): Structural change must contribute consequentially to impaired voiding in this cohort (i.e., it is present and functionally relevant).
- Witness: Li 2018 (li2018.pdf.md, Methods > 2.2. Patient evaluation) excluded UAB patients with acute urinary tract infection; bladder tumor or stone before operations; SCI in spinal shock period; urethral stricture; therapies to artificially increase bladder capacity (augmentation cystoplasty, recent (in 6 months) botulinum toxin injection, sacral neuromodulation, etc.); and pure bladder outflow obstruction (BOO).
- Source: li2018.pdf.md Methods > 2.2. Patient evaluation
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only lists exclusion criteria (e.g., “bladder tumor or stone… urethral stricture… pure BOO”) and does not mention structural change (fibrosis/remodeling) or any causal/functional link to impaired voiding.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R5 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness claims PTX is 'very safe'/'usually well tolerated' with GI symptoms/dizziness; no mention of structural pathology reduction after established injury.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses PTX tolerability/safety (“very safe”, “usually well tolerated”, GI symptoms, dizziness) and does not mention PTX reversing/limiting existing structural change after injury.

### A2-H2-R5 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states Lin et al. report PTX inhibits PDE 1–5 (IC50 50–200 μmol/L); this is mechanism-of-action data, not evidence of post-injury structural reversal/limitation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a mechanism property (PTX inhibits PDE 1–5 with IC50 50–200 μmol/L) but provides no evidence about reversing/limiting established structural pathology.

### A2-H2-R5 x W-FRD-Q0052-02-c3-Q0052
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Alewijnse2003 (Results > Table III) reports sequential longitudinal multiple linear regression with adherence behavior at 12-month follow-up as dependent variable, analyzed on n=75.
- Source: alewijnse2003.pdf.md Results > Table III (title/caption)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about a longitudinal regression analysis of adherence behavior at 12 months; it contains no claim about PTX given after established injury reducing structural pathology.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes a regression analysis of adherence behavior at 12-month follow-up (n=75) and contains no claim about PTX or post-injury structural change reversal/limitation.

### A2-H2-R5 x W-FRD-Q0063-01-c4-Q0063
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports PTX (100 µg/ml) acutely reduced FMLP-stimulated superoxide production in PMNs; it does not describe any established structural injury/dysfunction or reduction of structural pathology.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX reduced FMLP-stimulated superoxide production in PMNs in vitro; it does not address existing structural change in tissue or its reversal/limitation after injury.

### A2-H2-R5 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Witness is an in-vitro PMN degranulation assay (lysozyme release) with PTX reducing release; it does not involve administering PTX after established structural injury nor measuring reversal/limitation of structural pathology.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX reduced LPS-MCM–augmented FMLP lysozyme release in PMNs (degranulation assay) and does not mention any established structural injury or its reversal/limitation by PTX.

### A2-H2-R5 x W-FRD-Q0065-02-c3-Q0065
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: In peritonitis induction (PI), PTF pretreatment reduced neutrophil adhesiveness: half-clearance time increased significantly by 100% before PI and by a further 238% at 30 min after PI; groups differed significantly both before and at 30 min (10.1097@00003246-199002000-00012.pdf.md, RESULTS > Neutrophil Adhesiveness).
- Source: 10.1097@00003246-199002000-00012.pdf.md RESULTS > Neutrophil Adhesiveness
- Pass A: NO_SEMANTIC_RELATION - Witness describes PTF pretreatment effects on neutrophil adhesiveness around peritonitis induction; it is pretreatment (pre-injury) and reports no structural pathology reversal/limitation endpoints.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes PTF pretreatment effects on neutrophil adhesiveness around peritonitis induction (pre-injury/early timing) and provides no evidence of reversing/limiting existing structural change.

### A2-H2-R5 x W-FRD-Q0072-04-c1-Q0072
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Takasu1990_Cushings_Syndrome_Due.md (METHODS > Subjects) reports that, during a two-year period after unilateral adrenalectomy in 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, symptomatic thyroid dysfunction developed in 3 of 24 patients.
- Source: Takasu1990_Cushings_Syndrome_Due.md METHODS > Subjects
- Pass A: NO_SEMANTIC_RELATION - Witness is about thyroid dysfunction after adrenalectomy in Cushing’s patients; it does not mention PTX or structural injury reversal/limitation by PTX.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports thyroid dysfunction developing after unilateral adrenalectomy in Cushing’s patients and does not mention PTX or structural change reversal/limitation.

### A2-H2-R5 x W-FRD-Q0072-04-c2-Q0072
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Takasu1990_Cushings_Syndrome_Due.md (DISCUSSION) reports that among 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, 5 patients (including the 3 who later developed thyroid dysfunction) had increased antimicrosomal-antibody titers: 5/24 (21%), described as high versus 8.5% in normal women in Japan.
- Source: Takasu1990_Cushings_Syndrome_Due.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Witness reports antimicrosomal-antibody titers in Cushing’s syndrome patients; there is no PTX intervention and no claim about reversing established structural change.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports increased antimicrosomal-antibody titers in Cushing’s patients and includes no PTX intervention or claim about reversing/limiting established structural pathology.

### A2-H2-R5 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX effects on neutrophil calcium transients during FMLP stimulation; it does not address post-injury PTX administration or changes in established structural pathology.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX effects on neutrophil calcium transients during FMLP stimulation; this mechanistic signaling result does not address reversal/limitation of existing structural change after injury.

### A2-H2-R5 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness 'speculates' PTX 'may have no potent anti-inflammatory effect once inflammation has been triggered'; it does not address structural pathology reversal/limitation and is not evidence of post-injury structural improvement.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R5 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states PTX up to 50 µmol/L did not change [Ca2+]i and 500 µmol/L reduced it; this is mechanistic cell signaling, not reversal/limitation of established structural tissue change.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R5 x W-FRD-Q0092-03-c4-Q0092
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports 'only 2 patients reported epigastric pain' with remission on omeprazole; no mention of structural injury or its reversal/limitation by PTX.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H2-R5 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only describes enrollment and that it was an open-label 24-week trial of 'pentoxifylline 800 mg/day plus vitamin E'; it does not report any reduction/limitation of established structural pathology.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only describes an “open-label 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E” in “12 systemic-sclerosis patients” and gives no outcomes about reversing/limiting existing structural change after injury.

### A2-H2-R5 x W-FRD-Q0098-01-Q0098
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness explicitly describes 'PTX 40 mg/kg ... 45 min before hemorrhage' (pre-injury prophylaxis) and reports MAP/HR/WBC changes and death in shock, not reversal/limitation of existing structural change.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports “PTX 40 mg/kg…45 min before hemorrhage” with hemodynamic/WBC changes and that “they all died”; it is pretreatment and contains no claim about reversing/limiting existing structural tissue change.

### A2-H2-R5 x W-FRD-Q0123-01-c1-Q0123
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Vogel2023_Glucocorticoid_Withdrawal.md (Abstract > Results) reports that 1 month post-surgery, median (IQR) C-reactive protein was 0.48 mg dL−1 (0.14–0.90) versus 0.10 mg dL−1 (0.06–0.39) during active Cushing’s syndrome (P ≤ .001).
- Source: Vogel2023_Glucocorticoid_Withdrawal.md Abstract > Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports C-reactive protein values at different timepoints in Cushing’s syndrome; it contains no PTX administration and no structural pathology reversal claim.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness compares C-reactive protein levels “1 month post-surgery” versus “during active Cushing’s syndrome” and does not mention PTX or any reversal/limitation of established structural change.

### A2-H2-R5 x W-FRD-Q0131-03-c3-Q0131
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only states 'PTX has short half-life about 1.6 h' and does not address structural change or its reversal/limitation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states “PTX has short half-life about 1.6 h,” which does not address reversal/limitation of existing structural pathology.

### A2-H2-R5 x W-FRD-Q0131-03-c4-Q0131
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports 'PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion'—adverse effects, not reduction of established structural pathology.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports toxicity (“PTX toxicity…80 mg/kg, causing hypotension, flushing, and convulsion”) and provides no evidence of reversing/limiting existing structural change.

### A2-H2-R5 x W-FRD-Q0147-01-c5-Q0147
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Staubach1998.pdf.md (Results, PAHR paragraph) reports pressure-adjusted heart rate was significantly different on day 6 after diagnosis (P<.05) and “remained decreased” versus placebo thereafter; significance at later timepoints is not specified.
- Source: staubach1998.pdf.md Results (PAHR paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states PAHR was decreased on day 6 and remained decreased versus placebo; it provides no evidence about PTX reversing or limiting established structural tissue change.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports “pressure-adjusted heart rate…remained decreased versus placebo,” which is a physiologic measure and does not state PTX reverses/limits established structural tissue change after injury.

### A2-H2-R5 x W-FRD-Q0156-03-c1-Q0156
- Unit (REQUIRED_SUPPORT): PTX must be capable of reversing or limiting existing structural change (not merely preventing it when given before injury).
- Witness: Roberts1993.pdf.md (Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend): purified neutrophils preincubated 15 min: 1 µmol/L pentoxifylline did not inhibit FMLP superoxide rate or total; ≥5 µmol/L inhibited both. At 10 µmol/L: Rate FMLP 85% and Total FMLP 75% vs control (p<0.05).
- Source: roberts1993.pdf.md Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only reports that purified neutrophils preincubated with PTX (1–10 µmol/L) changed FMLP-stimulated superoxide production; it does not involve established structural change in tissue or reversal/limitation of pathology after injury.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes in vitro neutrophil preincubation with PTX affecting FMLP-stimulated superoxide production; it does not involve in vivo established structural pathology nor reversal/limitation after injury.

### A2-H2-R6 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness describes PTX as "very safe"/"well tolerated" with GI symptoms and dizziness; nothing about post-discontinuation persistence of improvements.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only discusses PTX safety/tolerability ("very safe", "well tolerated", GI symptoms, dizziness) and says nothing about benefit persisting after stopping PTX treatment.

### A2-H2-R6 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states pentoxifylline "inhibits PDE 1–5" with IC50 values; no claims about voiding/structural improvements or durability after stopping treatment.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a pharmacologic mechanism ("inhibits PDE 1–5" with IC50 values) but makes no statement about persistence of any clinical benefit after PTX discontinuation.

### A2-H2-R6 x W-FRD-Q0052-02-c2-Q0052
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: Alewijnse2003.pdf.md (Results > Participants and non-response) reports: of the 103 women who completed 12-month follow-up measurements, 15 did not return the post-test measurement and 2 did not return the 3-month follow-up measurement; reasons were unknown.
- Source: alewijnse2003.pdf.md Results > Participants and non-response
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only reports that some women "did not return" follow-up measurements and reasons were unknown; it does not mention PTX-related voiding/structural improvement or persistence after discontinuation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about follow-up measurement non-response ("did not return" post-test/3-month measurements) and provides no claim about PTX benefit persistence after stopping treatment.

### A2-H2-R6 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness “speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered,” which does not report sustained voiding/structural improvements after PTX discontinuation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness speculates about lack of anti-inflammatory potency once inflammation is triggered, not about any benefit persisting after stopping PTX treatment.

### A2-H2-R6 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness describes in vitro finding “preincubation with PTX… did not change… [Ca2+]i; 500 µmol/l reduced…” which is unrelated to persistent voiding improvements after stopping PTX.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in vitro neutrophil calcium finding (PTX at 50–500 µmol/l affecting [Ca2+]i), which does not address persistence of benefit after stopping PTX in any clinical context.

### A2-H2-R6 x W-FRD-Q0092-03-c4-Q0092
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports only that “all 12 patients completed 24 weeks… only 2 patients reported epigastric pain,” which does not address persistence of benefit after stopping PTX.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports side effects during a 24-week treatment period ("epigastric pain" in 2 patients) and does not mention benefits persisting after PTX is stopped.

### A2-H2-R6 x W-FRD-Q0092-04-desouza200-c2-Q0092
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: deSouza2009 reports: 12 systemic-sclerosis patients enrolled in an open-label 24-week study (desouza2009.pdf.md, Abstract). It was an open-label, 24-week-per-patient trial of pentoxifylline 800 mg/day plus vitamin E 800 UI/day (desouza2009.pdf.md, Patients and methods – Study design).
- Source: desouza2009.pdf.md Abstract; Patients and methods – Study design
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness specifies an “open-label, 24-week… trial of pentoxifylline 800 mg/day plus vitamin E,” but provides no report of voiding/structural improvements persisting after PTX discontinuation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes study design/dosing (open-label 24-week PTX + vitamin E) but provides no statement about any benefit persisting after stopping PTX.

### A2-H2-R6 x W-FRD-Q0098-01-Q0098
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: In male rats (pilot n=6), IV PTX 40 mg/kg over 15 min, 45 min before hemorrhage, decreased MAP 112±2.0→84.4±14.0 mmHg (p<0.05) and increased HR 365±79→437±38 bpm (p<0.05); WBC 7,140±1,460→12,700±2,980/mm3 (p<0.05); PMN 1,825±280→4,055±225/mm3 (p<0.05); %NBT+ PMN 12.0±9.7→15.0±12.3 (NS); absolute NBT+ PMN 220±218→609±635/mm3 (p<0.05); then “they all died” in shock (barroso-aranda1990.pdf.md, MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment).
- Source: barroso-aranda1990.pdf.md MATERIALS, METHODS AND PILOT EXPERIMENTS > Pentoxifylline Pretreatment
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness describes IV PTX effects on “MAP…HR…WBC” and that “they all died,” with no mention of voiding improvements or persistence after stopping PTX.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports acute physiologic effects and mortality in rats given IV PTX before hemorrhage (MAP/HR/WBC changes; "they all died"), not persistence of benefit after discontinuation.

### A2-H2-R6 x W-FRD-Q0108-03-Q0108
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: alewijnse2003.pdf.md (Results → Participants and non-response): Loss to follow-up numbers were not significantly different between study groups. Twenty-six women (20% of 129) withdrew: n=10 before therapy started, n=4 during treatment, n=12 during follow-up measurements. Questionnaire data: those lost had more frequent (U=978.5, P=0.029) and more severe (U=1036.5, P=0.045) wet episodes at pre-test.
- Source: alewijnse2003.pdf.md Results → Participants and non-response
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness concerns “Loss to follow-up… withdrew” and baseline severity differences among those lost, not persistence of PTX-related voiding improvements after stopping treatment.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses loss to follow-up and baseline severity among those lost (withdrawals; wet episode frequency/severity), not persistence of PTX benefit after treatment ends.

### A2-H2-R6 x W-FRD-Q0131-03-c3-Q0131
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: Mostafa-Hedeab2022 reports: “PTX has short half-life about 1.6 h” (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX has short half-life...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only reports “PTX has short half-life about 1.6 h,” which is not evidence that any benefit persists after discontinuation.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states a pharmacokinetic fact ("short half-life about 1.6 h") and does not claim that any benefit persists after stopping PTX treatment.

### A2-H2-R6 x W-FRD-Q0131-03-c4-Q0131
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: Mostafa-Hedeab2022 (mostafa-hedeab2022.pdf.md, Pharmacology of pentoxifylline) states that PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion, citing Dianey et al. (2021).
- Source: mostafa-hedeab2022.pdf.md Section: Pharmacology of pentoxifylline (sentence beginning 'PTX toxicity was reported...')
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states “PTX toxicity was reported at 80 mg/kg, causing hypotension, flushing, and convulsion,” which does not address persistent voiding/structural improvements after stopping PTX.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports toxicity at a dose ("toxicity ... at 80 mg/kg" causing hypotension/flushing/convulsion) and does not address persistence of benefit after PTX discontinuation.

### A2-H2-R6 x W-FRD-Q0148-01-c1-Q0148
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about “patients with TURP” with “no significant LUTS improvement… and no significant change… including BCI,” not about PTX treatment or whether benefits persist after PTX is stopped.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns long-term outcomes after TURP (no significant LUTS/voiding parameter improvements) and does not mention PTX treatment or persistence of benefit after stopping PTX.

### A2-H2-R6 x W-FRD-Q0149-04-c2-Q0149
- Unit (REQUIRED_SUPPORT): If benefit occurs, it may persist after stopping PTX treatment (consistent with structural recovery).
- Witness: In the full sample, response (≥50% reduction in HAM-D at any point) was 50% in each group, with no between-group difference (χ2=0.00, P=.99) (raison2013.pdf.md, RESULTS; Figure 6 caption).
- Source: raison2013.pdf.md RESULTS; Figure 6 caption (definition of response)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses “≥50% reduction in HAM-D…50% in each group” with “no between-group difference”; it contains no mention of pentoxifylline, voiding improvement, or persistence after stopping PTX.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports that response (≥50% reduction in HAM-D) was 50% in each group with "no between-group difference"; it does not mention PTX, stopping PTX, or whether any benefit persists after stopping treatment.

### A2-H3-A1 x W-FRD-Q0007-01-c1-Q0007
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness provides a definition of detrusor underactivity including “duration” and “normal time span,” but it does not report treatment timing evidence (onset, persistence, or duration-response) that would favor rapid vs slow benefit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only quotes a definitional description of detrusor underactivity (“reduced strength and/or duration… within a normal time span”) and provides no evidence about treatment onset, duration-response, or persistence that would favor A2-H1 or A2-H2.

### A2-H3-A1 x W-FRD-Q0039-02-Q0039
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: In SILODOSING (s00345-024-04974-7.pdf.md), both groups continued silodosin 8 mg once daily for 12 weeks (Patients and methods > Procedures > Experimental and control groups). The experimental group also did PFMT 30 min/day, 5 days/week for 12 weeks, supervised by a physiotherapist weekly (same). Anticholinergics/β3-mimetics use within 4 weeks pre–visit 1 and during study excluded (Patients and methods > Exclusion criteria).
- Source: s00345-024-04974-7.pdf.md Patients and methods > Procedures > Experimental and control groups; Patients and methods > Exclusion criteria; Patients and methods > Allocation
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Describes regimen duration (“continued silodosin…for 12 weeks…PFMT…for 12 weeks”) and exclusions, but contains no findings about when benefits begin or persist.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness specifies the intervention schedule (“continued silodosin…for 12 weeks” and PFMT “for 12 weeks”) and exclusions, but reports no outcome timing (onset/persistence/duration-response) evidence.

### A2-H3-A1 x W-FRD-Q0042-03-c2-Q0042
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Only reports side effects management (“omeprazole 40 mg per day…complete remission”), not timing of treatment benefit onset/persistence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses only side effects and their management (“epigastric pain…omeprazole 40 mg per day—with complete remission”), not onset, persistence, or duration-response of the relevant treatment effect.

### A2-H3-A1 x W-FRD-Q0043-01-c1-Q0043
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: In ladi-seyedian2017.pdf.md (7.3.1 Parasympathomimetics), the review reports Bougas et al. studied distigmine bromide in 27 UAB patients: 5 mg three times daily for 4 weeks significantly reduced PVR and obviated the need for CIC in 11 patients [76].
- Source: ladi-seyedian2017.pdf.md Section 7.3.1 Parasympathomimetics (distigmine paragraph; ref [76])
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - States that 4 weeks of dosing “significantly reduced PVR and obviated…CIC,” which gives a timescale (weeks) but does not distinguish onset within days vs gradual recovery or persistence after stopping.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports an outcome after a stated duration (“5 mg three times daily for 4 weeks significantly reduced PVR and obviated…CIC in 11 patients”), which is time-related, but it does not establish onset timing, persistence after stopping, or a duration-response clearly enough to favor A2-H1 vs A2-H2.

### A2-H3-A1 x W-FRD-Q0048-02-c1-Q0048
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: In 10.1016@s0041-13450001266-5.pdf.md (PATIENTS AND METHODS), pentoxifylline was dosed 150 mg IV 2 hours pre-op, 150 mg IV after graft reperfusion, and 300 mg IV 8 hours after grafting; then 1200 mg/day in three oral doses for 7 days.
- Source: 10.1016@s0041-13450001266-5.pdf.md PATIENTS AND METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Provides dosing times (“2 hours pre-op…after graft reperfusion…8 hours…then…for 7 days”) without any finding about onset or persistence of benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides dosing times (“2 hours pre-op…after graft reperfusion…then…for 7 days”) without any reported evidence of effect onset, persistence, or duration-response.

### A2-H3-A1 x W-FRD-Q0061-02-c2-Q0061
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: In siu2003.pdf.md (RESULTS), the authors report: “The mean time between the first and fourth visits was 213.40 days (30.50 weeks).”
- Source: siu2003.pdf.md RESULTS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Only states visit spacing (“mean time between the first and fourth visits was 213.40 days”), not onset, duration-response, or persistence of benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only states the spacing of study visits (“mean time between the first and fourth visits was 213.40 days”), not onset, persistence, or duration-response of any treatment effect.

### A2-H3-A1 x W-FRD-Q0065-02-c3-Q0065
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: In peritonitis induction (PI), PTF pretreatment reduced neutrophil adhesiveness: half-clearance time increased significantly by 100% before PI and by a further 238% at 30 min after PI; groups differed significantly both before and at 30 min (10.1097@00003246-199002000-00012.pdf.md, RESULTS > Neutrophil Adhesiveness).
- Source: 10.1097@00003246-199002000-00012.pdf.md RESULTS > Neutrophil Adhesiveness
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Shows rapid timing (“before PI” and “30 min after PI” changes), but it is about neutrophil adhesiveness in a peritonitis model, not therapeutic functional benefit onset/persistence at clinically relevant scope.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Although the witness includes time points (“before PI” and “30 min after PI”), it reports changes in “neutrophil adhesiveness” in a peritonitis model, not evidence about onset/duration-response/persistence of the clinical effect at issue for A2-H3 favoring A2-H1 or A2-H2.

### A2-H3-A1 x W-FRD-Q0069-02-c3-Q0069
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: refsum1994.pdf.md (RESULTS) reports ANOVA differences between study groups for intracellular sodium (P<.001), intracellular potassium (P<.05), and intracellular chloride (P<.001), but not intracellular water; the Bonferroni test compared the means of the groups receiving PTF to those of the CLP group at each time point.
- Source: refsum1994.pdf.md RESULTS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Reports statistical differences for intracellular sodium/potassium/chloride and Bonferroni comparisons, but provides no clear time-course of clinically relevant benefit onset/persistence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports statistical group differences for intracellular ions and that comparisons were made “at each time point,” but does not state any onset, persistence, or duration-response pattern clearly enough to favor A2-H1 or A2-H2.

### A2-H3-A1 x W-FRD-Q0092-03-c4-Q0092
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Discusses side effects only (“2 patients reported epigastric pain…complete remission”), not timing of benefit onset or persistence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is limited to adverse-event handling (“2 patients reported epigastric pain…complete remission”), providing no evidence on onset, persistence, or duration-response of benefit.

### A2-H3-A1 x W-FRD-Q0104-03-c6-Q0104
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Mentions “no time effect… and no treatment×time interaction,” which pertains to time-course, but it does not establish onset/persistence of clinical benefit (and is biomarker-specific), so it doesn’t decisively favor rapid vs slow benefit.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness explicitly addresses time effects for hs-CRP (“no time effect…no treatment×time interaction”), which is time-course related, but it is biomarker-specific and does not clearly establish onset, duration-response, or persistence of the relevant clinical benefit to favor A2-H1 or A2-H2.

### A2-H3-A1 x W-FRD-Q0149-04-c4-Q0149
- Unit (ADVERSE_TEST): Evidence establishes onset, duration-response, or persistence clearly enough to favor A2-H1 or A2-H2.
- Witness: Raison2013 (raison2013.pdf.md, RESULTS): in subgroup mixed-effects models for repeated measures, standardized effect size difference at 12 weeks was “moderate to large, in opposite directions”: 0.41 favoring infliximab for baseline hs-CRP >5 mg/L, versus −0.82 favoring placebo for baseline hs-CRP ≤5 mg/L.
- Source: raison2013.pdf.md RESULTS (paragraph containing standardized effect sizes); Figure 4
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Reports a 12-week effect size difference (“standardized effect size difference at 12 weeks…0.41… vs −0.82”), which is timing-relevant but does not pin onset (days–weeks) or persistence/duration-response clearly enough to decide rapid vs slow time course.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - Witness reports an effect size “at 12 weeks,” providing a single timepoint, but does not establish onset timing, persistence, or a duration-response trend clearly enough to favor A2-H1 vs A2-H2.

### A2-H3-C1 x W-FRD-Q0044-04-c2-Q0044
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: NO_SEMANTIC_RELATION - Witness reports clinical safety outcome (“Adverse effects were not reported…”, “No adverse effects…”) but does not address whether timing evidence was actively sought or whether uncertainty about timing is due to incomplete search/analysis.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only reports clinical safety outcomes (“Adverse effects were not reported in any patient”, “No adverse effects ... were observed”) and says nothing about whether timing evidence was searched/analyzed or whether timing uncertainty is due to unfinished retrieval/testing.

### A2-H3-C1 x W-FRD-Q0052-02-c2-Q0052
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: Alewijnse2003.pdf.md (Results > Participants and non-response) reports: of the 103 women who completed 12-month follow-up measurements, 15 did not return the post-test measurement and 2 did not return the 3-month follow-up measurement; reasons were unknown.
- Source: alewijnse2003.pdf.md Results > Participants and non-response
- Pass A: NO_SEMANTIC_RELATION - Witness is about missing follow-up measurements and unknown reasons for non-response; it provides no meta-level documentation about completion of retrieval/testing of timing evidence or whether timing uncertainty is due to unfinished investigation.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness describes missing follow-up measurements (“15 did not return the post-test ... 2 did not return the 3-month ... reasons were unknown”) rather than completion of retrieval/analysis or adverse testing of timing evidence.

### A2-H3-C1 x W-FRD-Q0052-04-c1-Q0052
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: In nihms-1048633.pdf.md (Fig. 1 CONSORT diagram), 981 were assessed; 958 female patients were included; 23 were excluded, including “Male / transgender” (n=8).
- Source: nihms-1048633.pdf.md Fig. 1 CONSORT diagram (participant flow/exclusions)
- Pass A: NO_SEMANTIC_RELATION - Witness is a CONSORT flow detail about inclusion/exclusion counts (“981 assessed…23 excluded…”); it does not discuss searching/analyzing timing evidence or adverse testing of timing links.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness is a CONSORT-style inclusion/exclusion count (“981 assessed ... 23 were excluded ... ‘Male / transgender’”) and does not address whether timing evidence has been meaningfully retrieved and adversarially tested.

### A2-H3-C1 x W-FRD-Q0053-02-c4-Q0053
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: NO_SEMANTIC_RELATION - Witness describes when questionnaires were completed (after ≥6 weeks PFME) and cautions about generalization to other stages; it is not documentation that timing-relevant evidence has been comprehensively retrieved and adversarially tested.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness states when data were collected (“after ... at least six weeks”) and cautions about generalizing to other stages, but it does not claim that timing evidence retrieval/analysis is complete or that remaining timing uncertainty is not due to unfinished work.

### A2-H3-C1 x W-FRD-Q0057-04-c2-Q0057
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: VanHouten2026_Cushings_syndrome.md reports that, to account for PBMC composition changes, monocyte-derived cytokine production after 24 h stimulation was normalized by dividing cytokine concentration (pg/mL) by monocyte counts, expressed per 1×10^5 monocytes (VanHouten2026_Cushings_syndrome.md, Materials and methods > Statistical analysis).
- Source: VanHouten2026_Cushings_syndrome.md Materials and methods > Statistical analysis
- Pass A: NO_SEMANTIC_RELATION - Witness concerns normalization of cytokine production by monocyte counts (statistical method); it does not address completion of searching/analyzing timing evidence or uncertainty sources about timing.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness concerns a normalization method (“normalized ... by dividing ... by monocyte counts”) and contains no statement about completing searches/analysis or adverse testing of timing evidence.

### A2-H3-C1 x W-FRD-Q0072-04-c1-Q0072
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (METHODS > Subjects) reports that, during a two-year period after unilateral adrenalectomy in 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, symptomatic thyroid dysfunction developed in 3 of 24 patients.
- Source: Takasu1990_Cushings_Syndrome_Due.md METHODS > Subjects
- Pass A: NO_SEMANTIC_RELATION - Witness reports an incidence over time (“during a two-year period… developed in 3 of 24”); it does not speak to whether timing uncertainty is not due to unfinished retrieval/analysis of timing evidence.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports an outcome over a time window (“during a two-year period ... developed in 3 of 24”) but does not address whether uncertainty about timing is not due to incomplete retrieval/analysis or whether timing evidence has been adversarially tested.

### A2-H3-C1 x W-FRD-Q0072-04-c2-Q0072
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: Takasu1990_Cushings_Syndrome_Due.md (DISCUSSION) reports that among 24 patients with Cushing’s syndrome due to a hyperfunctioning adrenocortical adenoma, 5 patients (including the 3 who later developed thyroid dysfunction) had increased antimicrosomal-antibody titers: 5/24 (21%), described as high versus 8.5% in normal women in Japan.
- Source: Takasu1990_Cushings_Syndrome_Due.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Witness reports antibody titer prevalence (5/24) and comparison to normal women; it is not meta-level evidence about completion of timing-evidence retrieval/adverse testing.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports prevalence/comparison of antibody titers (“5/24 ... described as high versus 8.5%”) and does not make any meta-level claim about completed retrieval/testing of timing evidence or the source of timing uncertainty.

### A2-H3-C1 x W-FRD-Q0085-01-c3-Q0085
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety): During the study, no severe adverse effects were reported, including no threatening hypotension or syncope; vital signs remained almost stable; no urinary retention occurred; and therapy did not stop for TEAEs (not explicitly phrased as zero TEAE dropouts).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: NO_SEMANTIC_RELATION - Witness reports safety findings (“no severe adverse effects… vital signs… no urinary retention”); it does not address searching/testing timing evidence or whether timing uncertainty remains despite completed investigation.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports safety findings (“no severe adverse effects ... vital signs remained almost stable ... no urinary retention”) and does not state that timing evidence has been fully retrieved/analyzed or adversarially tested.

### A2-H3-C1 x W-FRD-Q0092-03-c4-Q0092
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: NO_SEMANTIC_RELATION - Witness reports side effects over 24 weeks and completion of treatment; it provides no information about whether timing-relevant evidence has been meaningfully retrieved and adversarially tested to rule out incomplete analysis as the reason for timing uncertainty.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness describes treatment completion and side effects (“all 12 patients completed 24 weeks ... 2 patients reported epigastric pain”) but provides no information about completion of timing-evidence retrieval/analysis or adverse testing.

### A2-H3-C1 x W-FRD-Q0097-03-c1-Q0097
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: In Villa-Del-Pino et al. (2025), 1431 articles were identified (life-15-00613.pdf.md, Results > 3.1. Flow of Trials Through the Review). During screening, 255 studies were excluded for not measuring adherence/compliance, and 106 were excluded because adherence/compliance was measured via patient diary, verbal reports, or clinician-approved information, not scales/questionnaires (life-15-00613.pdf.md, Discussion > 4.3. The Challenge of Adherence).
- Source: life-15-00613.pdf.md Results > 3.1 Flow of Trials Through the Review (Figure 1 PRISMA flow diagram); Discussion > 4.3 The Challenge of Adherence
- Pass A: NO_SEMANTIC_RELATION - Witness is about systematic review screening/exclusion criteria regarding adherence measurement, not about timing evidence retrieval or adverse/negative tests of timing links.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports review screening/exclusion details (“1431 articles were identified ... excluded for not measuring adherence/compliance ... measured via diary/verbal reports”) rather than any statement that timing evidence has been meaningfully retrieved and adversarially tested.

### A2-H3-C1 x W-FRD-Q0105-04-c4-Q0105
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: In shah2016.pdf.md (RESULTS: Regression Analysis), after controlling for age, gender, and BMI, visceral, subcutaneous, and total adipose mass did not predict plasma IL-6 or IL-1β in Crohn’s disease patients at v1 or v2; likewise hepatic fat fraction and inter-muscular fat did not predict IL-6 or IL-1β at v1 or v2.
- Source: shah2016.pdf.md RESULTS: Regression Analysis
- Pass A: NO_SEMANTIC_RELATION - Witness reports null regression results (adipose measures did not predict cytokines at v1/v2); it does not document completion of timing-evidence search/analysis or explain why timing uncertainty persists.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports null regression results (“did not predict plasma IL-6 or IL-1β ... at v1 or v2”) and does not claim that timing uncertainty is not due to an unfinished search/analysis or that timing evidence testing is complete.

### A2-H3-C1 x W-FRD-Q0131-04-c3-Q0131
- Unit (CONTEXTUAL_CONSTRAINT): Uncertainty about timing is not due to an unfinished search or analysis; meaningful retrieval and adverse testing of timing evidence have been completed.
- Witness: In bortnick2019.pdf.md (Review of Medications > Alpha Blockers), the review reports FORTA labeled alfuzosin, doxazosin, and terazosin “avoid” because of increased risk for orthostatic hypotension, vasodilatory effects, cardiac arrhythmias, and syncope.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: NO_SEMANTIC_RELATION - Witness repeats the FORTA “avoid” rationale (orthostatic hypotension, arrhythmias, syncope); it does not address completeness of timing-evidence retrieval/analysis.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports FORTA’s recommendation (“labeled ... ‘avoid’ because of increased risk for orthostatic hypotension ... syncope”) and does not address completion of retrieval/analysis or adversarial testing of timing evidence.

### A2-H3-C2 x W-FRD-Q0003-04-c1-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses proposed biochemical mechanisms (PDE inhibition/NOS activation increasing NO/cGMP) for PTX benefits, but does not identify any unresolved timing link(s) (onset, duration-response, persistence) or localize uncertainty to timing.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only proposes biochemical mechanisms (“phosphodiesterase inhibitor and nitric oxide synthase activator… increases tissue NO and intracellular cGMP”) and does not discuss uncertainty or localize it to any “timing links” in a causal chain.

### A2-H3-C2 x W-FRD-Q0003-04-c3-Q0003
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness attributes pathway inference (not cholinergic; possibly purinergic/other) from differential responses, but makes no analytic statement about uncertainty being localized to specific timing links.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports pathway inference from results (“did not improve responses to carbachol… assumed… not via cholinergic nerves… related to purinergic… pathways”) but makes no statement about uncertainty being localized to identified timing links versus generalized across a chain.

### A2-H3-C2 x W-FRD-Q0005-04-c2-Q0005
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: In han1990.pdf.md (Materials and Methods—CAT Assay), the authors state that the CAT assay “was performed according to the thin-layer chromatography method of Gorman et al. (9).”
- Source: han1990.pdf.md Materials and Methods — CAT Assay
- Pass A: NO_SEMANTIC_RELATION - Witness is a methodological note about how a CAT assay was performed; it contains no claim about timing-related uncertainty or where uncertainty is localized in a causal chain.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is purely methodological (“CAT assay was performed according to… Gorman et al.”) and contains no claim about uncertainty or its localization to timing links.

### A2-H3-C2 x W-FRD-Q0006-04-c1-Q0006
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: In wang1996.pdf.md (DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle), Dr. Wang reports they did not add NO blockers such as L-NAME to test whether pentoxifylline-induced vascular relaxation in vitro was NO-dependent; they instead did studies of endothelium dependence by denuding vascular endothelial cells.
- Source: wang1996.pdf.md DISCUSSION (Q&A) Dr. Wang response to Dr. William G. Cheadle (second question re: L-NAME)
- Pass A: NO_SEMANTIC_RELATION - Witness states they did not test NO-dependence with blockers (L-NAME) and instead tested endothelium dependence; this is a mechanistic-testing gap, not identification of unresolved timing links (onset/duration/persistence).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states a mechanistic test was not performed (“did not add NO blockers such as L-NAME… instead… denuding… endothelial cells”) but does not address timing-link uncertainty (onset/duration/persistence) or its localization within a causal chain.

### A2-H3-C2 x W-FRD-Q0007-01-c1-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Vale2019.pdf.md (## 1 | INTRODUCTION) quotes the ICS urodynamic definition of detrusor underactivity: “a contraction of reduced strength and/or duration, resulting in prolonged bladder emptying and/or a failure to achieve complete bladder emptying within a normal time span” (Vale et al., 2019).
- Source: vale2019.pdf.md ## 1 | INTRODUCTION
- Pass A: NO_SEMANTIC_RELATION - Witness quotes a definition of detrusor underactivity including reduced strength/duration, but does not discuss uncertainty localized to specific timing links in a causal chain.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness quotes a definition of detrusor underactivity (“reduced strength and/or duration… prolonged bladder emptying… normal time span”) but does not discuss uncertainty localized to identified timing links in a causal chain.

### A2-H3-C2 x W-FRD-Q0007-03-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Vale et al. 2019 (vale2019.pdf.md, Section 3.1.4 Bladder outlet obstruction) report Cho et al. investigated urothelial ATP and nitric oxide in men with detrusor underactivity and benign prostatic hyperplasia: urothelial ATP was significantly decreased, while nitric oxide showed no significant change.
- Source: vale2019.pdf.md Section 3.1.4 | Bladder outlet obstruction (paragraph beginning “Cho et al. investigated changes in the levels of ATP and nitric oxide (NO) ...”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports findings on urothelial ATP decrease and no significant NO change; it does not characterize uncertainty as localized to particular timing link(s) versus generalized.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports biomarker findings (“ATP… decreased… nitric oxide… no significant change”) without any statement about uncertainty structure or timing-link localization in a causal chain.

### A2-H3-C2 x W-FRD-Q0007-04-c1-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: NO_SEMANTIC_RELATION - Witness suggests afferent dysfunction may play a role in 'initial and reversible stages' of DU, but does not state that uncertainty is specifically confined to identified timing links (nor specify unresolved onset/persistence links).
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness suggests stage-related involvement (“may play a role in the initial and reversible stages of DU”) but does not characterize uncertainty as being confined/localized to identified timing links (nor contrasts with generalized uncertainty across the chain).

### A2-H3-C2 x W-FRD-Q0007-04-c4-Q0007
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Vale2019.pdf.md (Section 4 “CONCLUSION”) says reliable bladder markers are urgently needed to avoid surpassing a “point of no return,” after which irreversible bladder decompensation and failure occur.
- Source: vale2019.pdf.md Section 4 “CONCLUSION”
- Pass A: NO_SEMANTIC_RELATION - Witness mentions a 'point of no return' and irreversible decompensation concept, but does not explicitly localize uncertainty to specific timing-related causal links remaining unresolved.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness mentions a threshold concept (“point of no return… irreversible bladder decompensation”) but does not state that uncertainty is localized to identified timing links rather than generalized across the causal chain.

### A2-H3-C2 x W-FRD-Q0009-02-c2-Q0009
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Chuang2015.pdf.md (## EPIDEMIOLOGY) summarizes Abarbanel & Marcus: in 181 LUTS patients aged ≥70 (82 men, 99 women), impaired detrusor contractility was defined urodynamically as Qmax <10 mL/s plus detrusor pressure <30 cm H2O, and was reported in 48% of men and 12% of women.
- Source: chuang2015.pdf.md ## EPIDEMIOLOGY (paragraph beginning “In men, detrusor underactivity may be caused… Abarbanel and Marcus…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports epidemiologic prevalence/definition of impaired detrusor contractility in older LUTS patients; it does not address uncertainty structure or timing-link localization.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides an epidemiologic definition/prevalence (“Qmax <10… detrusor pressure <30… reported in 48%… 12%”) with no discussion of uncertainty or localization to timing links in a causal chain.

### A2-H3-C2 x W-FRD-Q0013-01-c4-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness discusses minimizing “false-positive results” via “private-setting uroflowmetry” and does not identify any unresolved timing-related causal link(s).
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns diagnostic procedure validity (“minimize false-positive results… private-setting uroflowmetry… undulating fashion”) and does not identify any uncertainty localized to timing links in a causal chain.

### A2-H3-C2 x W-FRD-Q0013-03-c3-Q0013
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Kaplan1997 (kaplan1997.pdf.md, MATERIALS AND METHODS [definitions paragraph]) defined detrusor instability as a nonvolitional, phasic detrusor-pressure increase of at least 15 cm water, or a detrusor-pressure increase associated with increased sensation of urgency.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only “defined detrusor instability” by pressure/urgency criteria and contains no statement about uncertainty or timing links (onset, duration-response, persistence).
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only defines a condition (“defined detrusor instability as… phasic… increase of at least 15 cm… or… associated with urgency”) and makes no claim about uncertainty localized to timing links.

### A2-H3-C2 x W-FRD-Q0018-01-Q0018
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Bortnick et al. 2020 says surgical therapy is recommended for recurrent UTIs secondary to BPH, renal insufficiency secondary to BPH, recurrent bladder stones or gross hematuria from BOO due to BPH, refractory urinary retention secondary to BPH, and/or LUTS that have failed or unwillingness to consider other therapies (bortnick2020.pdf.md, “Alternative minimally invasive/surgical procedures to TURP”).
- Source: bortnick2020.pdf.md Section: “Alternative minimally invasive/surgical procedures to TURP” (paragraph beginning “Overall, surgical therapy is recommended…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness lists surgical indications (e.g., 'recurrent UTIs... renal insufficiency...'), with no claim about timing uncertainty or its localization.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness lists clinical indications for surgery (“recommended for recurrent UTIs… renal insufficiency… retention… LUTS…”) and does not address uncertainty or localize it to identified timing links in a causal chain.

### A2-H3-C2 x W-FRD-Q0018-03-Q0018
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Bortnick2020.pdf.md reports AUA guidelines recommend alpha-blocker plus 5-ARI combination therapy for men with moderate-severe LUTS, advanced age, and prostate size >40 g (bortnick2020.pdf.md, “Medical therapy > Combination therapy”).
- Source: bortnick2020.pdf.md Medical therapy > Combination therapy
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - A treatment recommendation ('AUA guidelines recommend...') does not discuss uncertainty or timing links (onset vs persistence) at all.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only reports a treatment recommendation (“AUA guidelines recommend alpha-blocker plus 5-ARI...”) and contains no statement about where uncertainty lies or that it is “localized to identified timing links” versus generalized across a causal chain.

### A2-H3-C2 x W-FRD-Q0019-02-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Roberts1993.pdf.md (Introduction) says in vitro PTX experiments often use concentrations much higher than obtained clinically; with oral preparations, peak plasma PTX levels are <5 μmol/l, and although PTX is converted to active metabolites, the combined level of all active forms is unlikely to exceed 10 μmol/l.
- Source: roberts1993.pdf.md Introduction (paragraph beginning "The interpretation of the effects of PTX on phagocyte function are confused...")
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness concerns concentration realism ('peak plasma... <5 μmol/l'), not timing (onset/duration/persistence) and does not localize uncertainty to timing links.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness discusses dose/concentration realism (“peak plasma PTX levels are <5 μmol/l... unlikely to exceed 10 μmol/l”), not uncertainty localization to timing links in a causal chain.

### A2-H3-C2 x W-FRD-Q0019-03-c2-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: roberts1993.pdf.md (Materials and methods > NADPH-oxidase activity > a) Superoxide production: purified neutrophils (1×10^6/ml) were incubated in spectrophotometer cuvettes for 5 min at 37°C; PTX or diluent was added and incubation continued 15 min before adding stimulant (1 µmol/l FMLP or 0.17 µmol/l TPA).
- Source: roberts1993.pdf.md Materials and methods > NADPH-oxidase activity > a) Superoxide production
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Method timing ('incubated... 5 min... continued 15 min') is procedural and does not assert uncertainty nor identify unresolved timing-related causal links.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - This is procedural timing (“incubated... 5 min... continued 15 min before adding stimulant”), not a claim about uncertainty being localized to timing links (or any uncertainty statement at all).

### A2-H3-C2 x W-FRD-Q0019-03-c3-Q0019
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - This is an in vitro dose-effect result ('5 µmol/l significantly inhibited...'), with no discussion of timing uncertainty or which timing links remain unresolved.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports an effect size at a concentration (“5 µmol/l significantly inhibited... to 76 ± 5%”), with no mention of uncertainty or of uncertainty being confined to timing links in the causal chain.

### A2-H3-C2 x W-FRD-Q0020-02-c1-Q0020
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: In immunology00076-0102.pdf.md (MATERIALS AND METHODS > Human volunteers), after informed consent, four healthy volunteers were treated orally with pentoxifylline 5×400 mg/day for 2 days, or continuously for 7 days (“in vivo” application); the methods do not explicitly state a crossover (same volunteers in both regimens).
- Source: immunology00076-0102.pdf.md MATERIALS AND METHODS > Human volunteers
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness flags an uncertainty tied to timing/regimen structure ('2 days, or ... 7 days' and 'does not explicitly state a crossover'), but it is about study design ambiguity, not an analytic localization of unresolved timing links in a causal chain (onset/duration-response/persistence).
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness flags an ambiguity tied to regimen timing/design (“treated... for 2 days, or continuously for 7 days” and “does not explicitly state a crossover”), which is a timing-related uncertainty, but it does not assert that uncertainty is localized to identified timing links (nor contrast with uncertainty across the whole causal chain).

### A2-H3-C2 x W-FRD-Q0023-01-c1-Q0023
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Osman2018.pdf.md (## Diagnostic aspects → ### Detrusor contraction strength → #### 2. Projected isovolumetric pressure (PIP)) suggests PIP groupings: >150 strong contractility; 100–150 normal; 50–100 weak; <50 very weak.
- Source: osman2018.pdf.md ## Diagnostic aspects → ### Detrusor contraction strength → #### 2. Projected isovolumetric pressure (PIP)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only lists diagnostic groupings for PIP (e.g., '>150 strong') and contains no statement about timing uncertainty or unresolved timing links.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only provides diagnostic cutoffs (“>150 strong... <50 very weak”) and says nothing about uncertainty or timing links in a causal chain.

### A2-H3-C2 x W-FRD-Q0053-02-c4-Q0053
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness explicitly raises a timing/stage limitation ('after... at least six weeks' and 'generalized cautiously to women at different stages'), which localizes uncertainty to training-stage timing, but it does not identify specific causal timing links like onset vs persistence in the hypothesis’ causal chain.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness explicitly limits generalization by intervention stage (“after... at least six weeks” and “generalized cautiously to women at different stages”), which localizes uncertainty to timing/stage, but it does not specify that uncertainty is confined to particular timing links within an identified causal chain.

### A2-H3-C2 x W-FRD-Q0060-02-c2-Q0060
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: Gülen2024_MCAS.md (“Diagnosis of MCAS”) says serum tryptase usually rises during acute systemic mast cell activation (e.g., anaphylaxis, MCAS), peaks about 1 h after clinical onset, then declines with ~2 h half-life; it may remain elevated 3 h, 5 h, or longer depending on initial elevation magnitude, which correlates best with mean arterial pressure drop magnitude.
- Source: Gulen2024_MCAS.md Section: "Diagnosis of MCAS" (laboratory criterion paragraph containing tryptase kinetics)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Although the witness contains timing details ('peaks about 1 h... half-life ~2 h'), it does not express uncertainty or identify unresolved timing links; it states expected kinetics.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness states expected kinetics (“peaks about 1 h... declines with ~2 h half-life... may remain elevated...”), not uncertainty localization to timing links or any claim about uncertainty being non-generalized across a causal chain.

### A2-H3-C2 x W-FRD-Q0097-03-c1-Q0097
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: In Villa-Del-Pino et al. (2025), 1431 articles were identified (life-15-00613.pdf.md, Results > 3.1. Flow of Trials Through the Review). During screening, 255 studies were excluded for not measuring adherence/compliance, and 106 were excluded because adherence/compliance was measured via patient diary, verbal reports, or clinician-approved information, not scales/questionnaires (life-15-00613.pdf.md, Discussion > 4.3. The Challenge of Adherence).
- Source: life-15-00613.pdf.md Results > 3.1 Flow of Trials Through the Review (Figure 1 PRISMA flow diagram); Discussion > 4.3 The Challenge of Adherence
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about screening/exclusion for 'not measuring adherence/compliance' or measuring it via diaries/verbal reports, not about timing (onset/duration/persistence) uncertainty localization.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness concerns review screening/exclusion based on adherence measurement methods (“excluded for not measuring adherence... or measured via diary/verbal reports”), unrelated to timing-link uncertainty in a causal chain.

### A2-H3-C2 x W-FRD-Q0104-03-c6-Q0104
- Unit (CONTEXTUAL_CONSTRAINT): The uncertainty is localized to identified timing links (not generalized across the entire causal chain).
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness gives results ('no time effect' and 'no treatment×time interaction') for hs-CRP in Raison2013, but it does not attribute or discuss 'uncertainty' nor identify which timing links in a broader causal chain remain unresolved.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports statistical results on time effects (“no time effect... no treatment×time interaction”) but does not discuss uncertainty or that uncertainty is localized to specific timing links rather than across the causal chain.

### A2-H3-E1 x W-FRD-Q0003-04-c1-Q0003
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: In shirazi2015.pdf.md (Discussion), the authors propose PTX is a phosphodiesterase inhibitor and nitric oxide synthase activator that increases tissue NO and intracellular cGMP, offered as mechanisms that can describe PTX’s beneficial effects on contractile function after ischemic injury (citing cardiac papillary muscle data).
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “In the present study, we assessed the protective effect of PTX…”)
- Pass A: PARTIALLY_COVERS - Mentions proposed PTX mechanisms affecting functional contractility via NO/cGMP (“beneficial effects on contractile function”), but does not report both functional and structural/tissue effects nor address onset/withdrawal timing or inability to attribute benefit between functional vs structural effects in the cohort.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only proposes a PTX mechanism for “beneficial effects on contractile function after ischemic injury” (cardiac papillary muscle), and does not report findings of both functional and structural effects in the relevant cohort, nor any lack of onset/withdrawal timing.

### A2-H3-E1 x W-FRD-Q0007-04-c1-Q0007
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: Vale et al. (2019) report that “recent findings” in BOO suggest afferent dysfunction—altered muscarinic and purinergic P2X3 receptor expression or diminished urothelial ATP—may play a role in the initial and reversible stages of DU, with potential diagnostic and therapeutic implications (vale2019.pdf.md, Abstract).
- Source: vale2019.pdf.md Abstract
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses "afferent dysfunction" (muscarinic/P2X3, urothelial ATP) in BOO and DU stages; it does not report PTX-associated functional+structural changes or timing uncertainty about PTX benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses “afferent dysfunction” (muscarinic/P2X3 expression, urothelial ATP) in BOO/DU stages, not findings about functional vs structural effects, timing (onset/withdrawal), or model transfer issues as stated in the unit.

### A2-H3-E1 x W-FRD-Q0013-01-c4-Q0013
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness addresses "diagnosing pseudodyssynergia" and minimizing false positives from "bashful voiding"; does not address PTX effects or timing/structural-vs-functional benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about diagnostic criteria for pseudodyssynergia (“uroflowmetry… undulating fashion”) and avoiding “bashful voiding” artifacts; it does not address reported functional/structural effects or timing/transfer limitations described in the unit.

### A2-H3-E1 x W-FRD-Q0014-02-Q0014
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness claims ultrasound DWT ≤1.23 mm + capacity >445 ml can "predict DU" (PPV/NPV); no PTX intervention effects, nor discussion of functional-vs-structural benefit timing.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness claims ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can “predict DU” (PPV/NPV), which is unrelated to the unit’s claim about findings reporting functional and structural effects and uncertainty about which drives benefit and about timing/model transfer.

### A2-H3-E1 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports "79% had detrusor underactivity" in diabetics with LUTS; does not mention PTX, functional/structural PTX effects, or timing of benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports prevalence/features of DU in diabetic men with LUTS (“79% had detrusor underactivity… delayed first voiding sense… increased bladder capacity”), not intervention findings about functional+structural effects, timing, or model-transfer caveats in the unit.

### A2-H3-E1 x W-FRD-Q0042-03-c2-Q0042
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is limited to side effects ("epigastric pain"; omeprazole) and completion; no claim about functional vs structural effects or onset/withdrawal.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only reports side effects/completion (“two reported epigastric pain… omeprazole… complete remission”) and contains no content about functional/structural effects, benefit attribution, or onset/withdrawal timing as in the unit.

### A2-H3-E1 x W-FRD-Q0044-04-c2-Q0044
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states "Adverse effects were not reported" / "No adverse effects ... observed"; it does not discuss functional/structural effects or timing of benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states “Adverse effects were not reported” / “No adverse effects… observed,” which does not speak to reported functional and structural effects, their relative contribution to benefit, or timing/model transfer limitations in the unit.

### A2-H3-E1 x W-FRD-Q0085-01-c3-Q0085
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety): During the study, no severe adverse effects were reported, including no threatening hypotension or syncope; vital signs remained almost stable; no urinary retention occurred; and therapy did not stop for TEAEs (not explicitly phrased as zero TEAE dropouts).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports "no severe adverse effects" and stable vital signs; it does not report PTX-related functional changes, structural changes, or timing/mechanistic ambiguity about benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is limited to safety (“no severe adverse effects… vital signs remained almost stable… no urinary retention”), not to findings about functional+structural effects or uncertainty about onset/withdrawal timing or model transfer stated in the unit.

### A2-H3-E1 x W-FRD-Q0090-04-c3-Q0090
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness concerns "purified neutrophils" and PTX concentrations affecting "[Ca2+]i"; unit is about functional vs structural effects mediating voiding benefit, which this does not address.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX effects on neutrophil intracellular calcium at specific concentrations (“purified neutrophils… 500 µmol/l reduced resting [Ca2+]i”), which is unrelated to the unit’s claims about functional vs structural effects mediating benefit and missing onset/withdrawal timing in the cohort.

### A2-H3-E1 x W-FRD-Q0092-03-c4-Q0092
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only states "only 2 patients reported epigastric pain" with PPI remission; it does not address functional or structural effects or onset/withdrawal timing of benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports only epigastric pain side effects and treatment with PPIs (“omeprazole 40 mg per day”), without any mention of functional/structural effects, their attribution to benefit, or onset/withdrawal timing/model transfer issues in the unit.

### A2-H3-E1 x W-FRD-Q0104-03-c6-Q0104
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports statistical effects on "hs-CRP" for "infliximab vs placebo" (treatment effect, no time or interaction). No PTX, no structural/functional voiding effects.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns infliximab vs placebo effects on hs-CRP (“significant treatment effect… no time effect”), not findings about functional/structural effects, benefit attribution, or onset/withdrawal timing/model transfer limitations stated in the unit.

### A2-H3-E1 x W-FRD-Q0148-01-c1-Q0148
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness is about "patients with TURP" and "no significant LUTS improvement" and no change in Qmax/PVR/BCI after 10+ years; it does not report PTX effects nor functional-vs-structural ambiguity for PTX.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports long-term TURP follow-up showing “no significant LUTS improvement” and no changes in voiding parameters (Qmax, PVR, BCI); it does not address findings about functional+structural effects, uncertainty about which drives benefit, or onset/withdrawal timing/model transfer as in the unit.

### A2-H3-E1 x W-FRD-Q0149-04-c4-Q0149
- Unit (CORROBORATING_EXPECTATION): Available findings report both functional and structural effects without establishing which carries the benefit, lack onset or withdrawal timing, or rest on models whose timing does not transfer to this cohort.
- Witness: Raison2013 (raison2013.pdf.md, RESULTS): in subgroup mixed-effects models for repeated measures, standardized effect size difference at 12 weeks was “moderate to large, in opposite directions”: 0.41 favoring infliximab for baseline hs-CRP >5 mg/L, versus −0.82 favoring placebo for baseline hs-CRP ≤5 mg/L.
- Source: raison2013.pdf.md RESULTS (paragraph containing standardized effect sizes); Figure 4
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses "infliximab" antidepressant outcomes moderated by hs-CRP at "12 weeks"; unit is about PTX functional/structural voiding effects and timing/mediation uncertainty. Different intervention and domain.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports a subgroup antidepressant outcome for infliximab vs placebo at 12 weeks moderated by baseline hs-CRP (“0.41 favoring infliximab… versus −0.82 favoring placebo”), but says nothing about ‘functional and structural effects,’ mediation of benefit, onset/withdrawal timing gaps, or transferability of model timing to a specific cohort.

### A2-H3-R1 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness says PTX is “very safe” and “usually well tolerated” with common complaints listed; it does not address onset/timing of benefit or whether evidence distinguishes rapid functional vs slow structural mechanisms.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports PTX is “very safe” and “usually well tolerated” and lists adverse effects; it says nothing about whether evidence can/cannot “distinguish rapid functional benefit from slow structural recovery.”

### A2-H3-R1 x W-FRD-Q0050-03-Q0050
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: Lin et al. report that pentoxifylline inhibits PDE 1–5, with IC50 values 50–200 μmol/L (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning "Pentoxifylline inhibits PDE 1–5")
- Pass A: NO_SEMANTIC_RELATION - Witness only states PTX inhibits PDE 1–5 with IC50 values; it does not address whether evidence can/cannot distinguish rapid functional benefit vs slow structural recovery for voiding improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states pentoxifylline inhibits “PDE 1–5, with IC50 values 50–200 μmol/L,” which does not address (in)distinguishability between rapid functional benefit and slow structural recovery in existing evidence.

### A2-H3-R1 x W-FRD-Q0053-02-c4-Q0053
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: NO_SEMANTIC_RELATION - Witness is about PFME questionnaire timing and generalizability across stages of PFME training, not about PTX evidence or distinguishing rapid functional vs slow structural mechanisms of voiding improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about PFME questionnaire timing (“after… at least six weeks”) and cautions generalizing across “different stages of PFME training,” not about inability to distinguish rapid functional vs slow structural recovery.

### A2-H3-R1 x W-FRD-Q0063-01-c1-Q0063
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: Sullivan-et-al-1988: Human PMNs incubated 30 min at 37°C with pentoxifylline 300 µg/ml decreased adherence to nylon vs diluent: 64.1±2.7% (n=16) vs 54.0±3.9% (n=6; P=0.031) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → PMN adherence).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → PMN adherence (opening paragraph)
- Pass A: NO_SEMANTIC_RELATION - Witness reports an in-vitro neutrophil adherence change after 30 min PTX incubation; it does not compare or claim inability to distinguish rapid functional benefit vs slow structural recovery for voiding improvement.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R1 x W-FRD-Q0063-01-c4-Q0063
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: Pentoxifylline (100 µg/ml) reduced FMLP (100 nM)-stimulated superoxide from 1.68±0.37 to 0.67±0.11 nmol/10 min per 10^6 PMNs (n=5; P=0.038) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Superoxide production).
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Superoxide production (paragraph beginning 'Pentoxifylline (100 µg/ml) did not affect...')
- Pass A: NO_SEMANTIC_RELATION - Witness reports reduced superoxide production in PMNs with PTX in vitro; it provides no synthesis about ambiguity between rapid functional onset and slow structural recovery for voiding outcomes.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R1 x W-FRD-Q0063-01-c5-Q0063
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: In PMNs, 20% LPS-MCM increased 100 nM FMLP lysozyme release to 2.31±0.11 µg/ml (n=10; P<0.001 vs LPS nonconditioned medium) (sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md, RESULTS → Degranulation → (i) PMNs treated with LPS-MCM). Pentoxifylline 1 or 100 µg/ml reduced this (P<0.050); PTX lysozyme values not stated.
- Source: sullivan-et-al-1988-inhibition-of-the-inflammatory-action-of-interleukin-1-and-tumor-necrosis-factor-(alpha)-on.pdf.md RESULTS → Degranulation → (i) PMNs treated with LPS-MCM
- Pass A: NO_SEMANTIC_RELATION - Witness describes PTX reducing LPS-MCM–increased lysozyme release in PMNs; it does not address timing/mechanistic indistinguishability of voiding improvement evidence.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R1 x W-FRD-Q0064-04-c1-Q0064
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: In male Wistar–Kyoto rats (230–300 g), after baseline haemodynamics, investigators gave saline or pentoxifylline 3 mg/kg i.v., then 30 min later saline or E. coli LPS 10 mg/kg i.v., monitoring for 240 min (wu1999.pdf.md, Methods 2.1 Endotoxic shock).
- Source: wu1999.pdf.md Methods 2.1 Endotoxic shock
- Pass A: NO_SEMANTIC_RELATION - Witness is a rat endotoxic shock protocol with PTX dosing/timing; it does not speak to whether existing PTX evidence for voiding improvement cannot distinguish rapid functional vs slow structural recovery.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R1 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports PTX effects (or lack thereof) on neutrophil calcium transients at certain concentrations; it does not concern evidence ambiguity about onset/persistence of voiding benefit mechanisms.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R1 x W-FRD-Q0089-04-c2-Q0089
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: Wystrychowski2014.pdf.md (DISCUSSION) speculates that pentoxifylline may have no potent anti-inflammatory effect once inflammation has been triggered and may be too weak to suppress an ongoing, self-propagating inflammatory cascade.
- Source: wystrychowski2014.pdf.md DISCUSSION
- Pass A: NO_SEMANTIC_RELATION - Witness is speculation about PTX anti-inflammatory potency once inflammation is triggered; it does not claim that existing evidence cannot distinguish rapid functional benefit from slow structural recovery for voiding improvement.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R1 x W-FRD-Q0090-04-c3-Q0090
- Unit (REQUIRED_SUPPORT): Existing evidence cannot distinguish rapid functional benefit from slow structural recovery.
- Witness: Roberts1993.pdf.md (Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients): in purified neutrophils, preincubation with PTX up to 50 µmol/l did not change resting or stimulated [Ca2+]i; 500 µmol/l reduced resting [Ca2+]i to 73 ± 12 nmol/l and stimulated to 571 ± 144 nmol/l (p<0.05).
- Source: roberts1993.pdf.md Results → Mechanism of action of pentoxifylline (a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports neutrophil [Ca2+]i findings with PTX preincubation; it does not address distinguishing rapid functional onset vs slow structural recovery for voiding improvement evidence.
- Pass B: MISSING - no judgment returned
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R2 x W-FRD-Q0010-02-Q0010
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md (MP75-18 > RESULTS), the mean wait time between referral and appointment was 54.7 days (SD 37.3; range 1–215).
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18 > RESULTS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports “mean wait time…54.7 days” for pelvic floor PT appointments, unrelated to measurement timing resolution of PTX effects.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states a measured scheduling interval: “mean wait time between referral and appointment was 54.7 days (SD 37.3; range 1–215).” The unit claims “Timing evidence is unmeasured,” which is not asserted or implied by this appointment-wait metric.

### A2-H3-R2 x W-FRD-Q0013-03-c4-Q0013
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness provides a BOO definition (pressure/flow/radiographic evidence) and does not discuss PTX outcomes or timing of measurement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only defines bladder outlet obstruction using physiologic criteria (“sustained detrusor contraction >45 cm water… flow rate <12 ml/s… radiographic evidence”). It does not address whether any timing evidence was unmeasured.

### A2-H3-R2 x W-FRD-Q0014-02-Q0014
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness claims DWT ≤1.23 mm plus capacity >445 ml can “predict DU,” but says nothing about PTX treatment outcomes or whether their timing was unmeasured/insufficiently resolved.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses diagnostic prediction of detrusor underactivity via ultrasound/urodynamic parameters (“DWT ≤1.23 mm… capacity >445 ml… predict DU”). It makes no claim that timing evidence is unmeasured.

### A2-H3-R2 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness shows PTX at “5 µmol/l” inhibited an FMLP-stimulated burst (hydrogen peroxide production), but does not address timing resolution of PTX-relevant bladder functional/structural outcomes (days–weeks vs weeks–months).
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in-vitro/whole-blood assay result at a stated concentration (“PTX… 5 µmol/l… inhibited… reducing… hydrogen peroxide production”). The unit is about timing evidence being unmeasured, which the witness does not mention.

### A2-H3-R2 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports “79% had detrusor underactivity” in a diabetic cohort, which is unrelated to whether PTX outcomes were measured with sufficient timing resolution.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports prevalence/clinical features in a cohort (“79% had detrusor underactivity… 21%… delayed first voiding sense”). It does not speak to whether timing evidence is unmeasured.

### A2-H3-R2 x W-FRD-Q0029-04-c5-Q0029
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports patients “lost to follow-up” (shifted to steroids / did not return), but does not state that PTX-relevant outcomes were not measured with timing resolution to distinguish days–weeks onset from weeks–months improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes attrition (“four patients were lost to follow-up… three patients were lost in the PTX group”). Loss to follow-up is not the same as claiming timing evidence is unmeasured.

### A2-H3-R2 x W-FRD-Q0034-01-bortnick20-c3-Q0034
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: bortnick2019.pdf.md (Review of Medications > Alpha Blockers) reports Duan et al. used 2006–2012 Medicare data in a cohort of 253,136 men >65 with BPH; dementia (ICD-9 codes) risk after mean 19.8 months was significantly higher with tamsulosin versus no BPH meds and versus doxazosin, terazosin, alfuzosin, dutasteride, or finasteride.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness concerns “tamsulosin” and dementia risk over “mean 19.8 months,” not whether PTX functional/structural outcomes were measured with inadequate timing resolution.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns dementia risk associated with tamsulosin over “mean 19.8 months.” It does not claim that timing evidence is unmeasured.

### A2-H3-R2 x W-FRD-Q0036-02-c3-Q0036
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: Stokes2022.pdf.md (STUDY DESIGN, MATERIALS AND METHODS) reports analyses used the 1st diaries returned (at the 2nd appointment), so only a subset contributed data: women who attended first follow-up, returned a completed diary, and had available prescription data.
- Source: stokes2022.pdf.md STUDY DESIGN, MATERIALS AND METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness limits analysis to “1st diaries returned (at the 2nd appointment),” but makes no statement about PTX outcomes being unmeasured or insufficiently time-resolved for onset vs delayed effects.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states analyses used “the 1st diaries returned (at the 2nd appointment)” and thus a subset contributed data. This is a sampling/availability constraint, not a statement that timing evidence is unmeasured.

### A2-H3-R2 x W-FRD-Q0052-02-c2-Q0052
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: Alewijnse2003.pdf.md (Results > Participants and non-response) reports: of the 103 women who completed 12-month follow-up measurements, 15 did not return the post-test measurement and 2 did not return the 3-month follow-up measurement; reasons were unknown.
- Source: alewijnse2003.pdf.md Results > Participants and non-response
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness states some women “did not return” measurements and reasons were “unknown,” but it does not claim PTX-relevant outcomes lacked timing resolution to determine onset vs delayed improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports missing measurements (“15 did not return the post-test measurement… 2 did not return the 3-month follow-up measurement; reasons were unknown”). It does not assert that timing evidence, as such, is unmeasured.

### A2-H3-R2 x W-FRD-Q0052-02-c3-Q0052
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: Alewijnse2003 (Results > Table III) reports sequential longitudinal multiple linear regression with adherence behavior at 12-month follow-up as dependent variable, analyzed on n=75.
- Source: alewijnse2003.pdf.md Results > Table III (title/caption)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports a regression on “adherence behavior at 12-month follow-up,” which does not address whether PTX functional/structural outcomes were measured with sufficient timing resolution.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes a regression analysis at “12-month follow-up” on n=75. The unit’s claim (“Timing evidence is unmeasured”) is not addressed.

### A2-H3-R2 x W-FRD-Q0053-02-c4-Q0053
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness discusses PFME questionnaire completion after “at least six weeks” and cautions generalizing across “different stages of PFME training,” not whether PTX outcomes were measured with timing resolution to distinguish onset vs delayed improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states questionnaire timing relative to PFME (“after… at least six weeks… end of an intensive… period”). This provides timing context, not a claim that timing evidence is unmeasured.

### A2-H3-R2 x W-FRD-Q0060-02-c2-Q0060
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: Gülen2024_MCAS.md (“Diagnosis of MCAS”) says serum tryptase usually rises during acute systemic mast cell activation (e.g., anaphylaxis, MCAS), peaks about 1 h after clinical onset, then declines with ~2 h half-life; it may remain elevated 3 h, 5 h, or longer depending on initial elevation magnitude, which correlates best with mean arterial pressure drop magnitude.
- Source: Gulen2024_MCAS.md Section: "Diagnosis of MCAS" (laboratory criterion paragraph containing tryptase kinetics)
- Pass A: NO_SEMANTIC_RELATION - Witness gives measured timing kinetics of serum tryptase ("peaks about 1 h after clinical onset"; "~2 h half-life"), not that PTX-relevant outcomes were unmeasured or lacked timing resolution for onset vs delayed improvement.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness provides explicit timing kinetics (“peaks about 1 h… declines with ~2 h half-life… may remain elevated 3 h, 5 h, or longer”). That does not support the unit’s statement that timing evidence is unmeasured.

### A2-H3-R2 x W-FRD-Q0061-02-c2-Q0061
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: In siu2003.pdf.md (RESULTS), the authors report: “The mean time between the first and fourth visits was 213.40 days (30.50 weeks).”
- Source: siu2003.pdf.md RESULTS
- Pass A: NO_SEMANTIC_RELATION - Witness reports only a scheduling interval ("mean time between the first and fourth visits was 213.40 days"), without stating that key PTX-relevant functional/structural outcomes were not measured with sufficient timing resolution.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness states a measured scheduling interval: “mean time between the first and fourth visits was 213.40 days (30.50 weeks).” The unit claims “Timing evidence is unmeasured,” i.e., timing was not measured; the witness instead reports a timing measurement and does not assert any lack of timing evidence.

### A2-H3-R2 x W-FRD-Q0065-02-c3-Q0065
- Unit (REQUIRED_SUPPORT): Timing evidence is unmeasured.
- Witness: In peritonitis induction (PI), PTF pretreatment reduced neutrophil adhesiveness: half-clearance time increased significantly by 100% before PI and by a further 238% at 30 min after PI; groups differed significantly both before and at 30 min (10.1097@00003246-199002000-00012.pdf.md, RESULTS > Neutrophil Adhesiveness).
- Source: 10.1097@00003246-199002000-00012.pdf.md RESULTS > Neutrophil Adhesiveness
- Pass A: NO_SEMANTIC_RELATION - Witness reports a measured acute timepoint effect ("at 30 min after PI"), which does not claim timing evidence is unmeasured/insufficient for PTX-relevant outcomes.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports timing-specific measurements (“before PI” and “at 30 min after PI”) and significant differences at those timepoints. The unit asserts timing evidence is unmeasured; the witness does not claim timing was unmeasured or missing, and instead provides explicit timepoint data.

### A2-H3-R3 x W-FRD-Q0010-02-Q0010
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md (MP75-18 > RESULTS), the mean wait time between referral and appointment was 54.7 days (SD 37.3; range 1–215).
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18 > RESULTS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Reporting "mean wait time... 54.7 days" is not evidence that improvement occurs early vs late, nor a conflict between onset timings.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports administrative scheduling timing only: “mean wait time between referral and appointment was 54.7 days (SD 37.3; range 1–215).” It does not address timing of outcomes/improvement nor any conflicting timing evidence.

### A2-H3-R3 x W-FRD-Q0010-04-c1-Q0010
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In MP75-18 (MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md, METHODS), the authors report a retrospective chart review of patients seen by benign urologists at one of their ambulatory clinics from April 2022 to September 2022, identified using ICD codes for BPH, OAB, LUTS, CP/CPPS, Pelvic Pain/PFD, Chronic Bladder Pain, and Urinary Urgency.
- Source: MP75-18-RATES-AND-ADHERENCE-TO-PELVIC-FLOOR-PHYSICAL-THERAPY-FOR-MALE-PATIENTS-WITH-BENIGN.pdf.md MP75-18; METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is purely methodological ("retrospective chart review... identified using ICD codes") and contains no early/delayed improvement evidence or conflict.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness is purely study design/population identification (“retrospective chart review… identified using ICD codes…”). It contains no claims about outcome timing or conflicts in timing evidence.

### A2-H3-R3 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness addresses diagnostic methodology ("private-setting uroflowmetry... minimize false-positive") and provides no evidence about early vs delayed functional improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness describes diagnostic procedure/criteria (“private-setting uroflowmetry… intended to minimize false-positive results…”), not when treatment effects occur or whether timing evidence conflicts.

### A2-H3-R3 x W-FRD-Q0013-03-c4-Q0013
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness defines obstruction using pressure/flow/radiographic criteria (">45 cm water... <12 ml/s") and does not discuss improvement timing or conflicts.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness defines “bladder outlet obstruction” using pressure/flow/radiographic thresholds (“>45 cm water… <12 ml/s…”). No statements relate to timing of improvement or conflicting timing evidence.

### A2-H3-R3 x W-FRD-Q0029-04-c5-Q0029
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In pharmaceuticals-19-00552.pdf.md (Section 2.2. Effect of Treatment on Clinical Markers), during follow-up, four patients were lost to follow-up in the mesalamine (placebo) group because they developed severe disease and shifted to adjuvant steroid therapy, and three patients were lost in the PTX group because they did not return for follow-up.
- Source: pharmaceuticals-19-00552.pdf.md Section 2.2. Effect of Treatment on Clinical Markers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness concerns attrition ("lost to follow-up... developed severe disease... did not return") and contains no claims about early vs delayed functional improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports attrition reasons (“lost to follow-up… developed severe disease… did not return”), not any temporal pattern of benefit or conflict about timing evidence.

### A2-H3-R3 x W-FRD-Q0032-04-c1-Q0032
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Fitzgerald et al. report 47 participants randomized (GTM n=24; MPT n=23) (fitzgerald2009.pdf.md, RESULTS); 44 (94%) completed, with 2 withdrawing from GTM and 1 from MPT (fitzgerald2009.pdf.md, RESULTS).
- Source: fitzgerald2009.pdf.md RESULTS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only reports participant flow ("47 participants randomized... 44 (94%) completed") without any early/delayed improvement findings, so it cannot evidence a timing conflict.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports participant flow/completion (“47 participants randomized… 44 (94%) completed… withdrawing”). It provides no evidence about when effects appear or whether timing evidence is conflicting.

### A2-H3-R3 x W-FRD-Q0034-02-bortnick20-c3-Q0034
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Bortnick et al. (2020) report that risk of self-harm was elevated significantly during the initial 18 months on a 5-ARI, though there was no increased risk of suicide (bortnick2020.pdf.md, Medical therapy → 5-alpha reductase inhibitors).
- Source: bortnick2020.pdf.md Section: “Medical therapy” → subsection “5-alpha reductase inhibitors”
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about adverse mental-health risk timing ("elevated... during the initial 18 months") and not about early vs delayed functional improvement, so it is unrelated to the unit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness concerns timing of an adverse outcome (“risk of self-harm… elevated… during the initial 18 months”), not timing of therapeutic improvement nor conflicts in timing-of-improvement evidence.

### A2-H3-R3 x W-FRD-Q0036-02-c3-Q0036
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Stokes2022.pdf.md (STUDY DESIGN, MATERIALS AND METHODS) reports analyses used the 1st diaries returned (at the 2nd appointment), so only a subset contributed data: women who attended first follow-up, returned a completed diary, and had available prescription data.
- Source: stokes2022.pdf.md STUDY DESIGN, MATERIALS AND METHODS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness describes data inclusion ("analyses used the 1st diaries returned") but does not report any improvement timing or conflicting onset evidence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness describes inclusion/data source timing (“analyses used the 1st diaries returned (at the 2nd appointment)”). It does not report any outcome timing findings or conflicts.

### A2-H3-R3 x W-FRD-Q0042-03-c2-Q0042
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only reports side effects and completion ("all 12 patients completed 24 weeks... two reported epigastric pain") and provides no evidence about onset/persistence of functional benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports side effects and completion (“all 12 patients completed 24 weeks… two reported epigastric pain… complete remission”). This is about adverse effects, not conflicting evidence on timing of treatment benefit.

### A2-H3-R3 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Statements like "Adverse effects were not reported" and "No adverse effects... were observed" address safety, not timing of functional improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness states absence of adverse effects (“Adverse effects were not reported…”, “No adverse effects… were observed”). It does not address timing of outcomes or any conflict in timing evidence.

### A2-H3-R3 x W-FRD-Q0052-02-c2-Q0052
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Alewijnse2003.pdf.md (Results > Participants and non-response) reports: of the 103 women who completed 12-month follow-up measurements, 15 did not return the post-test measurement and 2 did not return the 3-month follow-up measurement; reasons were unknown.
- Source: alewijnse2003.pdf.md Results > Participants and non-response
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports follow-up measurement return rates ("15 did not return the post-test... 2 did not return the 3-month") but does not report improvement at any timepoint, so it does not bear on timing conflict.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports missing measurements at timepoints (“15 did not return the post-test… 2 did not return the 3-month follow-up”). It does not state anything about when improvement occurs or conflicting timing evidence.

### A2-H3-R3 x W-FRD-Q0052-02-c3-Q0052
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Alewijnse2003 (Results > Table III) reports sequential longitudinal multiple linear regression with adherence behavior at 12-month follow-up as dependent variable, analyzed on n=75.
- Source: alewijnse2003.pdf.md Results > Table III (title/caption)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness concerns an analysis setup ("adherence behavior at 12-month follow-up as dependent variable") and does not provide early-vs-delayed improvement evidence or any timing conflict.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness describes an analysis specification (“regression… with adherence behavior at 12-month follow-up as dependent variable”). No outcome timing results or conflicts are asserted.

### A2-H3-R3 x W-FRD-Q0053-04-c4-Q0053
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In s12912-023-01326-5.pdf.md (Results → Characteristics of the study participants → Table 4), among 123 participants, gender was male 88 (71.5%) and female 35 (28.5%); history of pelvic surgery was yes 122 (99.2%) and no 1 (0.8%).
- Source: s12912-023-01326-5.pdf.md Results → Characteristics of the study participants → Table 4
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only reports baseline characteristics ("male 88 (71.5%)... history of pelvic surgery yes 122 (99.2%)") and contains no statements about improvement or timing, so it cannot support or conflict with "Timing evidence is conflicting."
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only reports participant characteristics ("gender was male 88... female 35"; "history of pelvic surgery was yes 122... no 1") and makes no claim about timing or whether timing evidence is conflicting.

### A2-H3-R3 x W-FRD-Q0065-02-c3-Q0065
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In peritonitis induction (PI), PTF pretreatment reduced neutrophil adhesiveness: half-clearance time increased significantly by 100% before PI and by a further 238% at 30 min after PI; groups differed significantly both before and at 30 min (10.1097@00003246-199002000-00012.pdf.md, RESULTS > Neutrophil Adhesiveness).
- Source: 10.1097@00003246-199002000-00012.pdf.md RESULTS > Neutrophil Adhesiveness
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness describes changes “before PI” and “at 30 min after PI” with significant differences; it provides no opposing early vs delayed improvement results.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes two timepoints ("before PI" and "30 min after PI") both showing significant changes/differences ("increased significantly"; "groups differed significantly") but does not report conflicting timing evidence (no inconsistency across studies or measures).

### A2-H3-R3 x W-FRD-Q0069-02-c3-Q0069
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: refsum1994.pdf.md (RESULTS) reports ANOVA differences between study groups for intracellular sodium (P<.001), intracellular potassium (P<.05), and intracellular chloride (P<.001), but not intracellular water; the Bonferroni test compared the means of the groups receiving PTF to those of the CLP group at each time point.
- Source: refsum1994.pdf.md RESULTS
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports ANOVA differences for intracellular sodium/potassium/chloride; it does not address onset/persistence of functional improvement or conflicting timing evidence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports ANOVA group differences for intracellular ions and that comparisons were made "at each time point," but it does not state that timing evidence is conflicting (no opposed early vs late pattern described).

### A2-H3-R3 x W-FRD-Q0092-03-c4-Q0092
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only 2 patients reported epigastric pain, treated with proton pump inhibitors with complete remission (omeprazole 40 mg per day).
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states “all 12 patients completed 24 weeks” and only side effect details; it does not report early vs delayed improvement timing conflict.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about treatment completion and side effects ("completed 24 weeks"; "2 patients reported epigastric pain") and contains no statement about outcome timing or conflicting timing evidence.

### A2-H3-R3 x W-FRD-Q0098-04-c3-Q0098
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Staubach1998.pdf.md, RESULTS (paragraph following Figure 4): total bilirubin, serum creatinine, and platelet count “showed no differences throughout the evaluation.” Serum endotoxin concentrations and IL-6 and TNF-α bioactivity were not significantly different between groups during the study.
- Source: staubach1998.pdf.md RESULTS (paragraph following Figure 4)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness says markers “showed no differences throughout the evaluation” and cytokines were “not significantly different”; no opposing early vs delayed improvement evidence is presented.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports no differences over time for several markers ("showed no differences throughout the evaluation"; "not significantly different") but does not assert any conflict in timing evidence; it is simply null over the evaluation period.

### A2-H3-R3 x W-FRD-Q0104-03-c6-Q0104
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports “significant treatment effect… but no time effect… and no treatment×time interaction,” which does not establish a conflict between early vs delayed functional improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports "no time effect" and "no treatment×time interaction" for hs-CRP; it does not describe conflicting timing evidence (it indicates lack of time dependence rather than conflicting timing findings).

### A2-H3-R3 x W-FRD-Q0108-03-Q0108
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: alewijnse2003.pdf.md (Results → Participants and non-response): Loss to follow-up numbers were not significantly different between study groups. Twenty-six women (20% of 129) withdrew: n=10 before therapy started, n=4 during treatment, n=12 during follow-up measurements. Questionnaire data: those lost had more frequent (U=978.5, P=0.029) and more severe (U=1036.5, P=0.045) wet episodes at pre-test.
- Source: alewijnse2003.pdf.md Results → Participants and non-response
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness discusses “Loss to follow-up… not significantly different” and baseline wet episode severity among those lost; no timing-conflict evidence about improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses attrition timing ("withdrew... before therapy started... during treatment... during follow-up") and baseline differences among those lost, not conflicts in timing of treatment effects or outcomes.

### A2-H3-R3 x W-FRD-Q0109-01-c3-Q0109
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Siu2003 reports 171/214 (80.7%) women attended the third visit and 111/214 (51.9%) attended the fourth visit (siu2003.pdf.md, RESULTS, paragraph beginning “Only 171 (80.7%) women attended...” ).
- Source: siu2003.pdf.md RESULTS, paragraph beginning 'Only 171 (80.7%) women attended...'
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports visit attendance rates (e.g., “171/214… attended the third visit”); it contains no results about early vs delayed improvement.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports visit attendance ("171/214... attended the third visit"; "111/214... attended the fourth visit") and says nothing about outcome timing or conflicting timing evidence.

### A2-H3-R3 x W-FRD-Q0114-03-c3-Q0114
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In Hafez2012 (hafez2012.pdf.md, Results > Mortality), 2 animals in group II (IR) died during the 24 h reperfusion period and 1 animal in group III died; these animals were excluded from the study.
- Source: hafez2012.pdf.md Results > Mortality
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness only says animals “died during the 24 h reperfusion period” and were excluded; no evidence about timing of improvement or conflicting onset.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports mortality/exclusion during "24 h reperfusion" and does not address timing of any measured effect or any conflict in timing evidence.

### A2-H3-R3 x W-FRD-Q0123-01-c1-Q0123
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Vogel2023_Glucocorticoid_Withdrawal.md (Abstract > Results) reports that 1 month post-surgery, median (IQR) C-reactive protein was 0.48 mg dL−1 (0.14–0.90) versus 0.10 mg dL−1 (0.06–0.39) during active Cushing’s syndrome (P ≤ .001).
- Source: Vogel2023_Glucocorticoid_Withdrawal.md Abstract > Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports CRP “1 month post-surgery… versus… during active Cushing’s syndrome”; it does not compare early vs delayed functional improvements nor present conflicting timing results.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness gives a single comparison at "1 month post-surgery" versus "during active Cushing’s syndrome" for CRP, without discussing multiple timings or any conflict in timing evidence.

### A2-H3-R3 x W-FRD-Q0147-01-c5-Q0147
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Staubach1998.pdf.md (Results, PAHR paragraph) reports pressure-adjusted heart rate was significantly different on day 6 after diagnosis (P<.05) and “remained decreased” versus placebo thereafter; significance at later timepoints is not specified.
- Source: staubach1998.pdf.md Results (PAHR paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness states PAHR was “significantly different on day 6” and “remained decreased”; this is a single time-course direction, not conflicting early vs delayed improvement evidence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes one trajectory (PAHR "significantly different on day 6" and "remained decreased") but does not indicate conflicting timing evidence (no opposed findings at different times).

### A2-H3-R3 x W-FRD-Q0148-01-c1-Q0148
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness reports that after “minimum 10-year follow-up” there was “no significant LUTS improvement compared with the preoperative situation,” providing no early-vs-late conflicting pattern.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports long-term follow-up results only ("minimum 10-year follow-up"; "no significant LUTS improvement"), without any comparison to earlier timepoints or any claim that timing evidence is conflicting.

### A2-H3-R3 x W-FRD-Q0149-04-c2-Q0149
- Unit (REQUIRED_SUPPORT): Timing evidence is conflicting.
- Witness: In the full sample, response (≥50% reduction in HAM-D at any point) was 50% in each group, with no between-group difference (χ2=0.00, P=.99) (raison2013.pdf.md, RESULTS; Figure 6 caption).
- Source: raison2013.pdf.md RESULTS; Figure 6 caption (definition of response)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Witness says response was 50% in each group with “no between-group difference”; it does not present early vs delayed onset/persistence patterns or any conflicting timing evidence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports an overall response rate "at any point" and "no between-group difference" (χ2=0.00, P=.99), but it does not discuss response timing (early vs late), onset, persistence, or any conflict in timing evidence; therefore it provides no support for "Timing evidence is conflicting."

### A2-H3-R4 x W-FRD-Q0050-02-Q0050
- Unit (REQUIRED_SUPPORT): Timing evidence is poorly transferable to this cohort.
- Witness: Lin et al. report PTX is “very safe” and “usually well tolerated” when given as the conventional controlled release formulation; most common complaints are gastrointestinal symptoms (nausea, dyspepsia) and dizziness in ~3% of patients (lin2004.pdf.md, RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE: “Pentoxifylline is used clinically…”).
- Source: lin2004.pdf.md Review Article → RATIONALE OF PENTOXIFYLLINE IN THE TREATMENT OF CHRONIC KIDNEY DISEASE (paragraph beginning “Pentoxifylline is used clinically to treat patients with peripheral vascular diseases.”)
- Pass A: NO_SEMANTIC_RELATION - This witness reports PTX safety/tolerability and common complaints; it does not report any time-to-effect/onset/persistence timing or transferability of timing evidence.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness only reports PTX safety/tolerability ("very safe", "usually well tolerated") and adverse complaints; it makes no claim about timing evidence or that timing findings are poorly transferable to any cohort.

### A2-H3-R4 x W-FRD-Q0053-02-c4-Q0053
- Unit (REQUIRED_SUPPORT): Timing evidence is poorly transferable to this cohort.
- Witness: In chen2004.pdf.md, Data Collection: participants completed the questionnaire after practicing PFME as prescribed for at least six weeks. In chen2004.pdf.md, Discussion: the cross-sectional data were obtained at the end of an intensive PFME intervention period, so findings should be generalized cautiously to women at different stages of PFME training.
- Source: chen2004.pdf.md Data Collection; Discussion
- Pass A: PARTIALLY_COVERS - It specifies a timing context (questionnaire after 'at least six weeks' of PFME) and explicitly warns findings 'should be generalized cautiously to women at different stages of PFME training,' which flags poor transferability of timing/stage; however it is about PFME training stage rather than the cohort/timing-of-effect uncertainty described in the unit.
- Pass B: WITNESS_ENTAILS_UNIT - Witness explicitly flags transferability limits tied to timing/training stage: data collected "after ... at least six weeks" and "findings should be generalized cautiously to women at different stages of PFME training." This supports the unit’s claim that timing evidence is poorly transferable to the cohort.
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - The witness specifies timing/stage (questionnaire after "at least six weeks" of PFME) and explicitly cautions generalization to "women at different stages of PFME training," which gestures at limited transferability by stage; it does not directly assert that "timing evidence is poorly transferable to this cohort" in general.

### A2-H3-R4 x W-FRD-Q0060-02-c2-Q0060
- Unit (REQUIRED_SUPPORT): Timing evidence is poorly transferable to this cohort.
- Witness: Gülen2024_MCAS.md (“Diagnosis of MCAS”) says serum tryptase usually rises during acute systemic mast cell activation (e.g., anaphylaxis, MCAS), peaks about 1 h after clinical onset, then declines with ~2 h half-life; it may remain elevated 3 h, 5 h, or longer depending on initial elevation magnitude, which correlates best with mean arterial pressure drop magnitude.
- Source: Gulen2024_MCAS.md Section: "Diagnosis of MCAS" (laboratory criterion paragraph containing tryptase kinetics)
- Pass A: NO_SEMANTIC_RELATION - This provides biomarker kinetics for serum tryptase (peaks ~1h, half-life ~2h) during acute mast cell activation, but does not state that such timing is poorly transferable to the cohort in scope.
- Pass B: PARTIALLY_COVERS - Witness explicitly reports timing: tryptase "peaks about 1 h after clinical onset" and declines with "~2 h half-life" and may remain elevated longer. However, it does not assert poor transferability to the hypothesis cohort; it is general physiology/diagnostic timing rather than timing of the cohort’s treatment benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - It provides general kinetics (tryptase "peaks about 1 h" and declines with "~2 h half-life") but does not say timing evidence is poorly transferable to any cohort, so it does not support the unit’s transferability claim.

### A2-H3-R4 x W-FRD-Q0069-02-c3-Q0069
- Unit (REQUIRED_SUPPORT): Timing evidence is poorly transferable to this cohort.
- Witness: refsum1994.pdf.md (RESULTS) reports ANOVA differences between study groups for intracellular sodium (P<.001), intracellular potassium (P<.05), and intracellular chloride (P<.001), but not intracellular water; the Bonferroni test compared the means of the groups receiving PTF to those of the CLP group at each time point.
- Source: refsum1994.pdf.md RESULTS
- Pass A: NO_SEMANTIC_RELATION - This concerns ANOVA/BONFERRONI comparisons of intracellular ions across time points; it does not discuss time-to-effect timing transferability limitations across models/cohorts.
- Pass B: PARTIALLY_COVERS - Witness includes repeated-measures context ("at each time point") and reports differences (e.g., intracellular sodium P<.001). But it does not state that such timing evidence is poorly transferable to the cohort; a transferability judgment would require additional model/cohort mismatch information not in the witness.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Although it mentions comparisons "at each time point," the witness only reports statistical differences between groups; it does not address whether timing evidence is poorly transferable to the cohort.

### A2-H3-R4 x W-FRD-Q0138-04-Q0138
- Unit (REQUIRED_SUPPORT): Timing evidence is poorly transferable to this cohort.
- Witness: nihms496647.pdf.md (“Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome”): unpublished extended data using proposed criteria: among 132 patients enrolled and referred for suspected or confirmed disease over four years, 58 met WHO systemic mastocytosis criteria, 7 MMAS, 19 IA; 42 had mast cell activation symptoms without evidence of clonal mast cells; 6 had unrelated diagnoses.
- Source: nihms496647.pdf.md Section: “Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome” (paragraph beginning “Using the approach outlined above…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports patient numbers meeting criteria (e.g., "58 met WHO systemic mastocytosis criteria") with no time-to-effect/onset/persistence information and no claim about timing transferability.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports diagnostic-category counts (e.g., "58 met WHO systemic mastocytosis criteria") without any timing or transferability statement, so it does not bear on timing evidence transferability.

### A2-H3-R4 x W-FRD-Q0147-01-c5-Q0147
- Unit (REQUIRED_SUPPORT): Timing evidence is poorly transferable to this cohort.
- Witness: Staubach1998.pdf.md (Results, PAHR paragraph) reports pressure-adjusted heart rate was significantly different on day 6 after diagnosis (P<.05) and “remained decreased” versus placebo thereafter; significance at later timepoints is not specified.
- Source: staubach1998.pdf.md Results (PAHR paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - Witness provides timing/onset language: "significantly different on day 6" and "remained decreased ... thereafter" vs placebo. But it does not itself state non-transferability to the hypothesis cohort; transferability would depend on cohort/model mismatch not specified in the witness text.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The witness reports timing of an observed effect ("day 6"; "remained decreased ... thereafter") but makes no statement that such timing evidence is poorly transferable to the relevant cohort; transferability is not addressed.

### A2-H3-R5 x W-FRD-Q0003-04-c3-Q0003
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: In shirazi2015.pdf.md (Discussion), authors report PTX improved detrusor contractions to electric stimulation in obstructed bladder, but did not improve responses to carbachol; therefore they assumed PTX’s protective effects were not via cholinergic nerves, but related to purinergic or other non-cholinergic, non-purinergic pathways.
- Source: shirazi2015.pdf.md Discussion (paragraph beginning “The findings of the present study showed…”)
- Pass A: NO_SEMANTIC_RELATION - Witness reports differential effects on detrusor responses (improved to electric stimulation, not to carbachol) and infers non-cholinergic pathways; it does not address onset/persistence or whether evidence supports both rapid and slow benefit.
- Pass B: PARTIALLY_COVERS - The witness reports functional modulation of contraction ('improved detrusor contractions to electric stimulation... did not improve responses to carbachol') suggesting an acute/functional mechanism, but it does not provide timing comparisons vs slower structural recovery or state that onset/persistence cannot be specified.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness discusses mechanism inference from differential responses ("improved detrusor contractions to electric stimulation" but "did not improve responses to carbachol"; assumed "not via cholinergic nerves"). It does not mention onset, persistence, or inability to specify timing of benefit.

### A2-H3-R5 x W-FRD-Q0013-01-c4-Q0013
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Kaplan et al. (kaplan1997.pdf.md, “MATERIALS AND METHODS”) report that diagnosing pseudodyssynergia also required private-setting uroflowmetry showing intermittent increases and decreases in flow “in an undulating fashion,” intended to minimize false-positive results from performance anxiety or “bashful voiding” during urodynamic evaluation.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (paragraph following diagnostic criteria)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - This concerns diagnostic methodology ('private-setting uroflowmetry... minimize false-positive') and does not address timing of therapeutic benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is about diagnostic criteria/method to avoid false positives ("private-setting uroflowmetry" to minimize "performance anxiety"/"bashful voiding"), not timing of therapeutic benefit or its persistence.

### A2-H3-R5 x W-FRD-Q0013-03-c4-Q0013
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: In kaplan1997.pdf.md (MATERIALS AND METHODS, definitions paragraph), bladder outlet obstruction was defined as sustained detrusor contraction >45 cm water plus catheterized urine flow rate <12 ml/s plus radiographic evidence of prostatic obstruction.
- Source: kaplan1997.pdf.md MATERIALS AND METHODS (definitions paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only defines BOO ('sustained detrusor contraction >45 cm... flow rate <12 ml/s...') and provides no information on treatment benefit timing.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only defines bladder outlet obstruction using pressure/flow/radiographic thresholds (">45 cm water", "<12 ml/s", "radiographic evidence"), with no claims about onset/persistence of benefit.

### A2-H3-R5 x W-FRD-Q0014-02-Q0014
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Rademakers2016.pdf.md says ultrasound DWT ≤1.23 mm plus bladder capacity >445 ml can safely, noninvasively detect detrusor underactivity and could replace pressure-flow studies (rademakers2016.pdf.md, KEY POINTS). Oelke et al. [30*] showed this thin-wall + large-capacity combination can sufficiently predict DU (PPV 100%, NPV 85%) with or without BOO/BPO (rademakers2016.pdf.md, NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION).
- Source: rademakers2016.pdf.md KEY POINTS (bullet on ultrasound DWT and bladder capacity); section “NONINVASIVE PARAMETERS FOR PREOPERATIVE CHARACTERIZATION OF PATIENTS WITH VOIDING DYSFUNCTION” (sentence reporting DWT ≤1.23 mm + capacity >445 ml with PPV/NPV and applicability with/without BOO/BPO)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about detecting/predicting DU ('DWT ≤1.23 mm... predict DU') and does not discuss treatment onset or persistence of benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness concerns noninvasive detection/prediction of detrusor underactivity ("DWT ≤1.23 mm" and "capacity >445 ml"; "predict DU"), not timing evidence about benefit onset/persistence.

### A2-H3-R5 x W-FRD-Q0019-03-c3-Q0019
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Roberts1993.pdf.md (Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend): PTX concentrations as low as 5 µmol/l significantly inhibited the FMLP (1 µmol/l)-stimulated burst, reducing DCF-assayed intracellular hydrogen peroxide production to 76 ± 5% of no-PTX control (n=10; p<0.025; paired Student’s t-test).
- Source: roberts1993.pdf.md Results > Effects of pentoxifylline on neutrophil function > NADPH-oxidase activity > b) Neutrophil oxidative activity measured in whole blood; Fig. 1b legend
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness shows an acute functional effect ('PTX concentrations as low as 5 µmol/l significantly inhibited... burst') consistent with rapid modulation, but it provides no evidence about voiding benefit, persistence, or concurrent slow/structural change, so it cannot establish the unit’s “both rapid and slow” compatibility/unspecified onset.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in vitro/whole-blood neutrophil assay effect ("5 µmol/l significantly inhibited" FMLP-stimulated burst to "76 ± 5%"), which is not evidence about clinical benefit timing (onset/persistence) in the target context.

### A2-H3-R5 x W-FRD-Q0027-03-2020ICUicu-c3-Q0027
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: 2020ICU_icu-58-S68.pdf.md (“PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY”): Bansal et al. [20] studied 52 men with diabetes presenting with bothersome LUTS (mean age 61) and reported 79% had detrusor underactivity (DU); 21% had delayed first voiding sense; 25% had increased bladder capacity (percentages reported; numerators not stated).
- Source: 2020ICU_icu-58-S68.pdf.md ## PREVALENCE AND EPIDEMIOLOGY OF DETRUSOR UNDERACTIVITY (sentence citing Bansal et al. [20])
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - This is epidemiology ('79% had detrusor underactivity') and does not address treatment effects, onset, persistence, or rapid vs slow benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports epidemiologic proportions in diabetic men ("79% had detrusor underactivity"; "delayed first voiding sense"; "increased bladder capacity"), not timing of treatment benefit or inability to specify onset/persistence.

### A2-H3-R5 x W-FRD-Q0034-03-c2-Q0034
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Mirabegron is listed at 25 mg daily (max 50 mg daily), with adverse effects “Hypertension, tachycardia” and comments “BP monitoring, renal and hepatic adjustments, inhibits CYP2D6” (fdp03812573_1.pdf.md, TABLE “Benign Prostatic Enlargement Medications”).
- Source: fdp03812573_1.pdf.md TABLE “Benign Prostatic Enlargement Medications” → β-agonists → Mirabegron row (Comments column).
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only lists dose and adverse effects ('Hypertension, tachycardia' and 'BP monitoring...') and contains no timing-of-benefit evidence.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is a medication table listing dosing and adverse effects/monitoring for mirabegron ("25 mg daily"; "Hypertension, tachycardia"; "BP monitoring"), with no mention of benefit onset or persistence.

### A2-H3-R5 x W-FRD-Q0034-03-c3-Q0034
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: 1. (fdp03812573_1.pdf.md, TABLE “Benign Prostatic Enlargement Medications”) The tamsulosin row lists adverse effects (headache, dizziness, abnormal ejaculation, rhinitis, floppy iris syndrome) and comments: “No BP monitoring, avoid with QTc prolonging agents.”
- Source: fdp03812573_1.pdf.md TABLE “Benign Prostatic Enlargement Medications” → α-blockers → Tamsulosin row (Comments column).
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The table lists adverse effects and monitoring ('No BP monitoring...') without any claim about onset or persistence of therapeutic benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness lists adverse effects and monitoring comments for tamsulosin ("No BP monitoring"; adverse effects list) and does not address timing of symptomatic benefit or its persistence.

### A2-H3-R5 x W-FRD-Q0034-04-bortnick20-c1-Q0034
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: bortnick2020.pdf.md (“Medical therapy”→“Combination therapy” MTOPS paragraph) reports MTOPS studied finasteride+doxazosin in 3000 men (mean age 62.6 years, SD 7.3) and found combination therapy improved voiding symptoms and maximum urinary flow rate more than either alone, prevented BPH progression better, and reduced the long-term risk of acute urinary retention and need for invasive therapy.
- Source: bortnick2020.pdf.md Section: “Medical therapy” → “Combination therapy” (MTOPS paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: PARTIALLY_COVERS - The witness includes 'long-term risk' reduction and symptom/flow improvements from combination therapy, which is consistent with benefits measured over time, but it does not report ambiguous timing evidence or inability to distinguish rapid functional vs slow structural mechanisms needed for the unit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports that combination therapy "improved voiding symptoms"/"maximum urinary flow rate" and reduced "long-term risk" of AUR/invasive therapy, but it does not discuss ambiguity between rapid vs slow benefit or inability to specify onset/persistence from the evidence.

### A2-H3-R5 x W-FRD-Q0042-03-c2-Q0042
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: In desouza2009.pdf.md (Results > Side effects), all 12 patients completed 24 weeks of treatment; only two reported epigastric pain, treated with proton pump inhibitors—specified as omeprazole 40 mg per day—with complete remission.
- Source: desouza2009.pdf.md Results > Side effects
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports side effects during 24 weeks ('two reported epigastric pain... complete remission') but provides no evidence about when voiding benefits begin or persist.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0044-04-c2-Q0044
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Staubach1998 states: “Adverse effects were not reported in any patient” (staubach1998.pdf.md, Results). It also reports: “No adverse effects of pentoxifylline treatment were observed” (staubach1998.pdf.md, Abstract).
- Source: staubach1998.pdf.md Results
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - Statements are limited to safety ('Adverse effects were not reported'/'No adverse effects... observed') and do not address benefit timing, onset, persistence, or mechanism.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0052-02-c2-Q0052
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Alewijnse2003.pdf.md (Results > Participants and non-response) reports: of the 103 women who completed 12-month follow-up measurements, 15 did not return the post-test measurement and 2 did not return the 3-month follow-up measurement; reasons were unknown.
- Source: alewijnse2003.pdf.md Results > Participants and non-response
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness only reports missing follow-up measurements ('15 did not return the post-test... 2 did not return the 3-month... reasons unknown') and makes no claim about timing of benefit or mechanisms, so it does not bear on specifying onset/persistence.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0052-04-c1-Q0052
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: In nihms-1048633.pdf.md (Fig. 1 CONSORT diagram), 981 were assessed; 958 female patients were included; 23 were excluded, including “Male / transgender” (n=8).
- Source: nihms-1048633.pdf.md Fig. 1 CONSORT diagram (participant flow/exclusions)
- Pass A: NO_SEMANTIC_RELATION - Witness is about trial screening/inclusion counts and exclusion of “Male / transgender”; it gives no information on timing of benefit (onset/persistence) or whether effects are compatible with rapid vs slow mechanisms.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness only reports CONSORT inclusion/exclusion counts (e.g., “958 female patients were included… ‘Male / transgender’ (n=8)”), with no statements about timing of benefit onset/persistence or ambiguity between rapid vs slow benefit.

### A2-H3-R5 x W-FRD-Q0060-02-c2-Q0060
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Gülen2024_MCAS.md (“Diagnosis of MCAS”) says serum tryptase usually rises during acute systemic mast cell activation (e.g., anaphylaxis, MCAS), peaks about 1 h after clinical onset, then declines with ~2 h half-life; it may remain elevated 3 h, 5 h, or longer depending on initial elevation magnitude, which correlates best with mean arterial pressure drop magnitude.
- Source: Gulen2024_MCAS.md Section: "Diagnosis of MCAS" (laboratory criterion paragraph containing tryptase kinetics)
- Pass A: NO_SEMANTIC_RELATION - Witness discusses kinetics of serum tryptase rise/peak/half-life after acute mast cell activation; it does not address voiding benefit timing evidence or inability to specify onset/persistence of such benefit.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness describes biomarker kinetics (“tryptase… peaks about 1 h after clinical onset… ~2 h half-life… may remain elevated 3 h, 5 h, or longer”), not timing evidence about treatment benefit onset/persistence or inability to specify them.

### A2-H3-R5 x W-FRD-Q0079-04-c3-Q0079
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: roberts1993.pdf.md (Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients): Purified neutrophils: resting [Ca2+]i 88±10 nmol/L (±1 SE; n=6) rose to 799±197 (±1 SE) after 1 µmol/L FMLP. PTX up to 50 µmol/L changed neither resting nor FMLP-stimulated [Ca2+]i; 500 µmol/L reduced resting to 73±12 and FMLP-stimulated to 571±144 vs control (paired t-test p<0.05).
- Source: roberts1993.pdf.md Results > Mechanism of action of pentoxifylline > a) Effect on FMLP-stimulated calcium transients
- Pass A: NO_SEMANTIC_RELATION - Witness reports pentoxifylline effects on neutrophil calcium transients after FMLP stimulation; it contains no claims about clinical voiding benefit timing (rapid vs slow) or uncertainty in onset/persistence.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports an in vitro neutrophil calcium response to FMLP and pentoxifylline concentrations (no change up to 50 µmol/L; reduction at 500 µmol/L), which does not address clinical benefit timing or uncertainty about onset/persistence.

### A2-H3-R5 x W-FRD-Q0085-01-c3-Q0085
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety): During the study, no severe adverse effects were reported, including no threatening hypotension or syncope; vital signs remained almost stable; no urinary retention occurred; and therapy did not stop for TEAEs (not explicitly phrased as zero TEAE dropouts).
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: NO_SEMANTIC_RELATION - Witness is limited to safety outcomes (no severe adverse effects; vital signs stable; no urinary retention) and does not mention onset/persistence of benefit or timing evidence compatible with rapid and slow effects.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness is limited to safety outcomes (“no severe adverse effects… vital signs remained almost stable… no urinary retention”), not timing of therapeutic benefit onset or persistence, nor compatibility with rapid vs slow benefit.

### A2-H3-R5 x W-FRD-Q0085-04-Q0085
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: bortnick2019.pdf.md (Review of Medications > Alpha Blockers): Most common alpha-blocker side effects include dizziness, orthostatic hypotension, retrograde ejaculation, and rhinitis; in older adults dizziness/orthostatic hypotension can lead to falls/injuries. It reports FORTA: silodosin/tamsulosin “caution” for no older-person efficacy/safety data and hypotension risk, especially with other antihypertensives; alfuzosin/doxazosin/terazosin “avoid” for orthostatic hypotension, vasodilatory effects, cardiac arrhythmias, syncope.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: NO_SEMANTIC_RELATION - Witness summarizes alpha-blocker side effects and FORTA cautions/avoidance in older adults; it does not discuss timing of voiding benefit or inability to specify onset/persistence.
- Pass B: MISSING - no judgment returned
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness summarizes alpha-blocker side effects and geriatric prescribing cautions/avoidance (dizziness, orthostatic hypotension, FORTA categories) without any claims about onset/persistence of benefit or indeterminacy of timing.

### A2-H3-R5 x W-FRD-Q0104-03-c6-Q0104
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: In Raison2013 (raison2013.pdf.md, RESULTS (hs-CRP longitudinal paragraph)), regarding infliximab vs placebo effects on hs-CRP across treatment, there was a significant treatment effect (t57=2.25, P=.03), but no time effect (t433=0.10, P=.92) and no treatment×time interaction (t433=0.27, P=.78).
- Source: raison2013.pdf.md RESULTS (hs-CRP longitudinal paragraph)
- Pass A: PARTIALLY_COVERS - Witness states there was a significant treatment effect on hs-CRP but “no time effect” and “no treatment×time interaction,” implying the data do not resolve temporal change patterns; however this pertains to hs-CRP in an infliximab study, not voiding benefit or rapid-vs-slow benefit mechanisms, so it only weakly/indirectly maps to timing-uncertainty.
- Pass B: NO_SEMANTIC_RELATION - The witness reports statistical effects on hs-CRP (treatment effect; no time or treatment×time interaction), not timing of voiding benefit or distinguishing rapid functional vs slow structural mechanisms.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - Witness reports statistical results for hs-CRP (“significant treatment effect… no time effect… no treatment×time interaction”) in an infliximab study, but does not discuss timing evidence being compatible with both rapid and slow benefit, nor inability to specify onset/persistence of the target benefit.

### A2-H3-R5 x W-FRD-Q0131-04-Q0131
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Bortnick2019.pdf.md (Review of Medications > Alpha Blockers) reports FORTA for men >65: silodosin and tamsulosin are “caution” because no older-adult efficacy/safety data and hypotension risk, especially with other antihypertensive medications; alfuzosin, doxazosin, and terazosin are “avoid” due to orthostatic hypotension, vasodilatory effects, cardiac arrhythmias, and syncope.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about geriatric prescribing categories and hypotension risk ('caution'/'avoid'), not evidence about when voiding benefits begin or how long they persist or whether timing is compatible with rapid+slow mechanisms.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0131-04-c3-Q0131
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: In bortnick2019.pdf.md (Review of Medications > Alpha Blockers), the review reports FORTA labeled alfuzosin, doxazosin, and terazosin “avoid” because of increased risk for orthostatic hypotension, vasodilatory effects, cardiac arrhythmias, and syncope.
- Source: bortnick2019.pdf.md Review of Medications > Alpha Blockers
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness addresses adverse-effect risk labeling ('avoid' due to orthostatic hypotension, arrhythmias, syncope), not timing of voiding benefit or inability to specify onset/persistence.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0138-04-Q0138
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: nihms496647.pdf.md (“Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome”): unpublished extended data using proposed criteria: among 132 patients enrolled and referred for suspected or confirmed disease over four years, 58 met WHO systemic mastocytosis criteria, 7 MMAS, 19 IA; 42 had mast cell activation symptoms without evidence of clonal mast cells; 6 had unrelated diagnoses.
- Source: nihms496647.pdf.md Section: “Proposed Criteria for the diagnosis of idiopathic mast cell activation syndrome” (paragraph beginning “Using the approach outlined above…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - This is about numbers of patients meeting systemic mastocytosis/MMAS/IA criteria vs symptoms without clonal mast cells, not about treatment benefit timing or voiding outcomes.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0144-01-c3-Q0144
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: In Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md (3.4 | Safety), mild adverse events occurred in 11 intervention vs 13 control patients; most were mild dyspepsia requiring no treatment. No severe adverse effects (no threatening hypotension or syncope) and no urinary retention episodes; vital signs remained almost stable.
- Source: Comparison-between-combination-of-tamsulosin-and-Pentoxifylline-versus-tamsulosin-alone-in.pdf.md 3.4 | Safety
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness reports 'No severe adverse effects' and stable vital signs, with no urinary retention, but provides no evidence about timing of voiding benefit onset or persistence or mechanistic ambiguity.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0147-01-c5-Q0147
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Staubach1998.pdf.md (Results, PAHR paragraph) reports pressure-adjusted heart rate was significantly different on day 6 after diagnosis (P<.05) and “remained decreased” versus placebo thereafter; significance at later timepoints is not specified.
- Source: staubach1998.pdf.md Results (PAHR paragraph)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness concerns PAHR 'significantly different on day 6' and 'remained decreased' (cardiovascular metric), not onset/persistence of voiding benefit or ambiguity between rapid functional vs slow structural voiding mechanisms.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0148-01-c1-Q0148
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Rademakers2016 (rademakers2016.pdf.md, INTRODUCTION): After minimum 10-year follow-up (mean 14.5±3.2y TURP; 13.6±3.3y untreated), patients with TURP showed no significant LUTS improvement compared with the preoperative situation and no significant change (vs preoperative) in Qmax, PVR, voiding efficiency, or any other voiding parameter, including BCI (BCI=Pdet,qmax+5Qmax).
- Source: rademakers2016.pdf.md INTRODUCTION (paragraph beginning “The fate of men with detrusor underactivity after prostatic surgery (TURP)…”)
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - This reports that TURP patients had 'no significant LUTS improvement' and no significant change in Qmax/PVR/BCI after long follow-up, but it does not discuss rapid vs slow mechanisms nor uncertainty about onset/persistence of a treatment benefit in the unit’s sense.
- Final: **ABSTAIN** (MODEL_ADJUDICATED) - adjudicator returned no decision

### A2-H3-R5 x W-FRD-Q0156-03-c1-Q0156
- Unit (REQUIRED_SUPPORT): Timing evidence is compatible with both rapid and slow benefit, so onset and persistence cannot be specified from supported premises.
- Witness: Roberts1993.pdf.md (Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend): purified neutrophils preincubated 15 min: 1 µmol/L pentoxifylline did not inhibit FMLP superoxide rate or total; ≥5 µmol/L inhibited both. At 10 µmol/L: Rate FMLP 85% and Total FMLP 75% vs control (p<0.05).
- Source: roberts1993.pdf.md Results → Effects of pentoxifylline on neutrophil function → NADPH-oxidase activity → a) Superoxide production by purified neutrophils; Fig. 1a table and Fig. 1 legend
- Pass A: MISSING - no judgment returned
- Pass B: NO_SEMANTIC_RELATION - The witness is about pentoxifylline inhibiting FMLP-stimulated superoxide in purified neutrophils after 15 min, not about urinary/voiding outcomes or persistence/onset of voiding benefit; it does not address timing uncertainty for voiding benefit.
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - The unit is about uncertainty in "onset and persistence" of a "benefit" (timing evidence compatible with rapid and slow benefit). The witness only reports an in-vitro neutrophil experiment with a specific "preincubated 15 min" condition and whether pentoxifylline "did not inhibit" or "inhibited" FMLP-induced superoxide; it makes no statement about benefit onset/persistence or inability to specify timing from supported premises.

## Judged by one pass only (needs confirmation) (0)
