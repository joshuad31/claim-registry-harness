# Matching review packet

Each entry is one witness judged against one coverage unit. To overrule a relation, add an entry to `human-decisions.json` in this folder (a blank template is next to this file) and run `cr run <project> --from coverage`. Relations: EQUIVALENT, WITNESS_ENTAILS_UNIT (these two give complete coverage), UNIT_ENTAILS_WITNESS, PARTIALLY_COVERS, CONTRADICTS, NO_SEMANTIC_RELATION, ABSTAIN.

## Complete relations (these build coverage sets) (4)

### A1-H2-E3 x W-FRD-Q0009-02-Q0009
- Unit (CORROBORATING_EXPECTATION): and reviews report inconsistent field results
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass A]
- Pass B: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass B]
- Final: **WITNESS_ENTAILS_UNIT** (AGREED) - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass A]

### A1-H2-E3 x W-FRD-Q0011-04-Q0011
- Unit (CORROBORATING_EXPECTATION): and reviews report inconsistent field results
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md Results
- Pass A: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass A]
- Pass B: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass B]
- Final: **WITNESS_ENTAILS_UNIT** (AGREED) - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass A]

### A1-H2-E3 x W-FRD-Q0017-04-Q0017
- Unit (CORROBORATING_EXPECTATION): and reviews report inconsistent field results
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md Results
- Pass A: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass A]
- Pass B: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass B]
- Final: **WITNESS_ENTAILS_UNIT** (AGREED) - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass A]

### A1-H2-E3 x W-FRD-Q0019-02-Q0019
- Unit (CORROBORATING_EXPECTATION): and reviews report inconsistent field results
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass A]
- Pass B: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass B]
- Final: **WITNESS_ENTAILS_UNIT** (AGREED) - witness supplies every unit element and adds detail; coverage 0.89 [local-rules 1.8 pass A]

## Contradictions (these drive crux tests) (2)

### A1-H2-E1 x W-FRD-Q0006-02-Q0006
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Because the trial used pots and a single cultivar, the yield difference should not be extrapolated to field conditions without a field test (alvarez2021).
- Source: alvarez2021.md SYNTHETIC — Foliar silicate and wheat water relations in a controlled pot trial
- Pass A: CONTRADICTS - predicate ['DIFF'] asserted with opposite polarity (coverage 0.66) [local-rules 1.8 pass A]
- Pass B: CONTRADICTS - predicate ['DIFF'] asserted with opposite polarity (coverage 0.66) [local-rules 1.8 pass B]
- Final: **CONTRADICTS** (AGREED) - predicate ['DIFF'] asserted with opposite polarity (coverage 0.66) [local-rules 1.8 pass A]

### A1-H2-E1 x W-FRD-Q0020-01-Q0020
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Because the trial used pots and a single cultivar, the yield difference should not be extrapolated to field conditions without a field test (alvarez2021).
- Source: alvarez2021.md SYNTHETIC — Foliar silicate and wheat water relations in a controlled pot trial
- Pass A: CONTRADICTS - predicate ['DIFF'] asserted with opposite polarity (coverage 0.66) [local-rules 1.8 pass A]
- Pass B: CONTRADICTS - predicate ['DIFF'] asserted with opposite polarity (coverage 0.66) [local-rules 1.8 pass B]
- Final: **CONTRADICTS** (AGREED) - predicate ['DIFF'] asserted with opposite polarity (coverage 0.66) [local-rules 1.8 pass A]

## Disagreements between pass A and pass B (48)

### A1-H2-E1 x W-FRD-Q0002-04-Q0002
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Grain yield was 8.12 tonnes per hectare in treated plots and 7.94 tonnes per hectare in controls; the difference was not significant (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0003-02-Q0003
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Grain yield was 8.12 tonnes per hectare in treated plots and 7.94 tonnes per hectare in controls; the difference was not significant (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0008-04-Q0008
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Grain yield was 8.12 tonnes per hectare in treated plots and 7.94 tonnes per hectare in controls; the difference was not significant (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0009-02-Q0009
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.73 [local-rules 1.8 pass A]
- Pass B: PARTIALLY_COVERS - partial content coverage 0.73; at least one required element missing [local-rules 1.8 pass B]
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (WITNESS_ENTAILS_UNIT vs PARTIALLY_COVERS); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0011-04-Q0011
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md Results
- Pass A: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.73 [local-rules 1.8 pass A]
- Pass B: PARTIALLY_COVERS - partial content coverage 0.73; at least one required element missing [local-rules 1.8 pass B]
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (WITNESS_ENTAILS_UNIT vs PARTIALLY_COVERS); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0012-03-Q0012
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Grain yield was 8.12 tonnes per hectare in treated plots and 7.94 tonnes per hectare in controls; the difference was not significant (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0016-01-Q0016
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: The absence of a yield response in the field contrasts with positive greenhouse reports (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0017-04-Q0017
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md Results
- Pass A: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.73 [local-rules 1.8 pass A]
- Pass B: PARTIALLY_COVERS - partial content coverage 0.73; at least one required element missing [local-rules 1.8 pass B]
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (WITNESS_ENTAILS_UNIT vs PARTIALLY_COVERS); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0018-03-Q0018
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Grain yield was 8.12 tonnes per hectare in treated plots and 7.94 tonnes per hectare in controls; the difference was not significant (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-E1 x W-FRD-Q0019-02-Q0019
- Unit (CORROBORATING_EXPECTATION): Multi-site field trials report no significant yield difference
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: WITNESS_ENTAILS_UNIT - witness supplies every unit element and adds detail; coverage 0.73 [local-rules 1.8 pass A]
- Pass B: PARTIALLY_COVERS - partial content coverage 0.73; at least one required element missing [local-rules 1.8 pass B]
- Final: **PARTIALLY_COVERS** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (WITNESS_ENTAILS_UNIT vs PARTIALLY_COVERS); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0001-03-Q0001
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0001-04-Q0001
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: A two-season field experiment tested foliar silicate for lodging resistance and grain yield in irrigated wheat (smidt2020).
- Source: smidt2020.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0003-01-Q0003
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: A two-season field experiment tested foliar silicate for lodging resistance and grain yield in irrigated wheat (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0003-03-Q0003
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0004-03-Q0004
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: This narrative review summarises reported effects of silicon application on yield and drought tolerance in cereal crops, with attention to the gap between controlled and field studies (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0005-03-Q0005
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0006-04-Q0006
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0007-01-Q0007
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0007-04-Q0007
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: A two-season field experiment tested foliar silicate for lodging resistance and grain yield in irrigated wheat (smidt2020).
- Source: smidt2020.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0008-01-Q0008
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: This narrative review summarises reported effects of silicon application on yield and drought tolerance in cereal crops, with attention to the gap between controlled and field studies (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0009-02-Q0009
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0009-03-Q0009
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0011-03-Q0011
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0011-04-Q0011
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0012-02-Q0012
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0013-01-Q0013
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: A two-season field experiment tested foliar silicate for lodging resistance and grain yield in irrigated wheat (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0013-03-Q0013
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0014-01-Q0014
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: This narrative review summarises reported effects of silicon application on yield and drought tolerance in cereal crops, with attention to the gap between controlled and field studies (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0015-03-Q0015
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0016-01-Q0016
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: The absence of a yield response in the field contrasts with positive greenhouse reports (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0017-01-Q0017
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0017-04-Q0017
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H2-R3 x W-FRD-Q0019-02-Q0019
- Unit (REQUIRED_SUPPORT): field trials show no yield benefit
- Witness: Among the field studies we located, results are inconsistent: some report no yield difference, while others report small increases that were not significant (brennan2022).
- Source: brennan2022.md SYNTHETIC — Silicon in cereals: a narrative review of yield evidence (brennan202
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0001-03-Q0001
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0001-04-Q0001
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: A two-season field experiment tested foliar silicate for lodging resistance and grain yield in irrigated wheat (smidt2020).
- Source: smidt2020.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0003-01-Q0003
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: A two-season field experiment tested foliar silicate for lodging resistance and grain yield in irrigated wheat (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0003-03-Q0003
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0005-03-Q0005
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0006-04-Q0006
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0007-01-Q0007
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0007-04-Q0007
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: A two-season field experiment tested foliar silicate for lodging resistance and grain yield in irrigated wheat (smidt2020).
- Source: smidt2020.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0009-03-Q0009
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0011-03-Q0011
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0012-02-Q0012
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0013-01-Q0013
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: A two-season field experiment tested foliar silicate for lodging resistance and grain yield in irrigated wheat (smidt2020).
- Source: smidt2020.md SYNTHETIC — Foliar silicate, lodging and yield in irrigated wheat (smidt2020
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0013-03-Q0013
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0015-03-Q0015
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A1-H3-E3 x W-FRD-Q0017-01-Q0017
- Unit (CORROBORATING_EXPECTATION): and no study measures both the water-relations mechanism and grain yield in the field
- Witness: Foliar silicate was tested at three rainfed field sites over two seasons to determine whether it improves wheat grain yield under water-limited conditions (okafor2019).
- Source: okafor2019.md SYNTHETIC — Multi-site field trial of foliar silicate in rainfed wheat (okafor20
- Pass A: PARTIALLY_COVERS - partial content coverage 0.47; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.47 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

## Judged by one pass only (needs confirmation) (0)
