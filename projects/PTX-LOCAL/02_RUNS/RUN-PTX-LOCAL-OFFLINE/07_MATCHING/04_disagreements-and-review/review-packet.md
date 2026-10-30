# Matching review packet

Each entry is one witness judged against one coverage unit. To overrule a relation, add an entry to `human-decisions.json` in this folder (a blank template is next to this file) and run `cr run <project> --from coverage`. Relations: EQUIVALENT, WITNESS_ENTAILS_UNIT (these two give complete coverage), UNIT_ENTAILS_WITNESS, PARTIALLY_COVERS, CONTRADICTS, NO_SEMANTIC_RELATION, ABSTAIN.

## Complete relations (these build coverage sets) (0)

## Contradictions (these drive crux tests) (0)

## Disagreements between pass A and pass B (2)

### A1-H2-E2 x W-FRD-Q0029-02-Q0029
- Unit (CORROBORATING_EXPECTATION): Missing clinical trials alone do not corroborate H2
- Witness: fibroblast proliferation and extracellular matrix production<sup>26,27</sup> and increases collagenase activity.<sup>26,27</sup> However, in our experimental pig study, we did not observe any clinical or histologic changes in RIF after 6 months of treatment with PTX alone.<sup>13</sup> The high concentration of PTX necessary to suppress fibroblast collagen synthesis or to increase collagenase activity (delanian2003.pdf).
- Source: delanian2003.pdf.md Randomized, Placebo-Controlled Trial of Combined Pentoxifylline and Tocopherol f
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

### A2-H1-A2 x W-FRD-Q0005-04-Q0005
- Unit (ADVERSE_TEST): human benefit, where reported, appears only after prolonged treatment
- Witness: Despite these limitations, the consistency of findings across multiple clinical and biochemical outcomes, as well as across subgroup and adjusted analyses, supports the robustness of the observed treatment effect (pharmaceuticals-19-00552.pdf).
- Source: pharmaceuticals-19-00552.pdf.md Results
- Pass A: PARTIALLY_COVERS - partial content coverage 0.46; at least one required element missing [local-rules 1.8 pass A]
- Pass B: NO_SEMANTIC_RELATION - content coverage 0.46 is too low [local-rules 1.8 pass B]
- Final: **NO_SEMANTIC_RELATION** (MODEL_ADJUDICATED) - local adjudicator kept the weaker relation (PARTIALLY_COVERS vs NO_SEMANTIC_RELATION); a conflict outranks an entailment, and the pair is labelled MODEL_ADJUDICATED

## Judged by one pass only (needs confirmation) (0)
