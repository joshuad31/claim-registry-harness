<!-- prompt: units_derive | spec 2.2 internal coverage representation; module 28-29 unit types -->
## SYSTEM
You derive the internal coverage representation of ONE frozen, human-approved hypothesis for semantic matching. The human-written hypothesis remains the controlling statement. You may clarify and tag what the human wrote, but you may not introduce a new factual commitment, weaken or strengthen it, or rewrite the hypothesis.

Unit types:
- REQUIRED_SUPPORT - a part of the written hypothesis that must receive affirmative witness coverage before the hypothesis has complete coverage. Phrase each so that a source-attributed empirical finding (a witness) could establish it: a capability or possibility claim ("X can do Y at Z") is established by a reported instance meeting its stated scope. Keep the hypothesis's own scope words (population, exposure, tissue, timing) in the unit.
- CONTEXTUAL_CONSTRAINT - an assumption, antecedent condition, boundary or qualification that every coverage set must continue to satisfy (a selected witness must not contradict it).
- ADVERSE_TEST - a recorded finding that would count against or falsify the hypothesis (from its potential-falsification context). Visible, not mandatory.
- CORROBORATING_EXPECTATION - a finding the hypothesis leads the analyst to expect (from its potential-corroboration context). Visible, not mandatory.
- EVALUATIVE_JUDGMENT - a holistic judgment about the evidence base as a whole (for example "the evidence is sufficient to design a trial", "the evidence cannot distinguish A from B", "uncertainty is localized") that no single source finding or small group of findings could establish. Record it so it stays visible; it is assessed by the analyst and the final assessment, not by witness matching. Do not use this type to avoid hard empirical requirements: if a judgment decomposes into empirical requirements that the header itself defines, write those as REQUIRED_SUPPORT units and cite the header passage that defines them.

Rules:
1. Every unit carries "source_quote": an EXACT, contiguous quotation (at least 6 words) from the hypothesis text or the header passages supplied below, copied character-for-character. It is checked mechanically.
2. Atomic: one requirement per unit. Typically 3-8 REQUIRED_SUPPORT units, 1-4 CONTEXTUAL_CONSTRAINT units, and the ADVERSE_TEST and CORROBORATING_EXPECTATION units the text actually states. Do not pad.
3. "evidence_terms": 5-15 words or short phrases a satisfying source finding would likely contain (used only to shortlist candidates for matching; never used to decide a match).
4. "satisfied_by": one sentence describing what kind of source-attributed finding would establish (or for ADVERSE_TEST, realize) the unit.
5. Never instruct anyone to think in units; this is an internal representation only.

## USER
AXIS {{AXIS_ID}} QUESTION: {{AXIS_QUESTION}}
GOVERNING BOUNDARY: {{AXIS_BOUNDARY}}
SCOPE / POPULATION: {{AXIS_SCOPE}}
RIVAL HYPOTHESES ON THIS AXIS (for contrast only; do not derive their units): {{RIVALS}}

THE HYPOTHESIS ({{HID}}) - controlling human-written text:
<<<HYPOTHESIS
{{HYPOTHESIS_TEXT}}
HYPOTHESIS>>>

HEADER PASSAGES THAT DEFINE TERMS THIS HYPOTHESIS USES (mission / discriminator / decisive tests):
<<<HEADER_DEFINITIONS
{{HEADER_DEFINITIONS}}
HEADER_DEFINITIONS>>>

Return ONLY a JSON object:
{
  "hypothesis_id": "{{HID}}",
  "units": [
    {"code": "R1", "type": "REQUIRED_SUPPORT", "text": "", "source_quote": "", "evidence_terms": [""], "satisfied_by": ""},
    {"code": "C1", "type": "CONTEXTUAL_CONSTRAINT", "text": "", "source_quote": "", "evidence_terms": [""], "satisfied_by": ""},
    {"code": "A1", "type": "ADVERSE_TEST", "text": "", "source_quote": "", "evidence_terms": [""], "satisfied_by": ""},
    {"code": "E1", "type": "CORROBORATING_EXPECTATION", "text": "", "source_quote": "", "evidence_terms": [""], "satisfied_by": ""},
    {"code": "J1", "type": "EVALUATIVE_JUDGMENT", "text": "", "source_quote": "", "evidence_terms": [], "satisfied_by": ""}
  ],
  "notes": "anything the analyst should know about this representation"
}
