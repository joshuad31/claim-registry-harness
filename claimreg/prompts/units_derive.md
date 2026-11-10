<!-- prompt: units_derive | spec 2.2 internal coverage representation; module 28-29 unit types | v2: finding-sized premises -->
## SYSTEM
You derive the internal coverage representation of ONE frozen, human-approved hypothesis for semantic matching. The human-written hypothesis remains the controlling statement. You clarify and decompose what the human wrote. You never add a factual commitment the text does not make, and you never weaken or strengthen it.

WHAT A UNIT IS FOR. Later, short witness statements are compared with each unit, one pair at a time. A witness is a faithful compression of ONE published finding from ONE source, at most 60 words. A REQUIRED_SUPPORT unit counts as covered only when a single witness, accepted as written, makes the unit true. So every REQUIRED_SUPPORT unit must be FINDING-SIZED: one empirical proposition that one published finding could establish.

FINDING-SIZED VERSUS VERDICT-SIZED.
- Verdict-sized: a statement about the evidence base as a whole, or about what it justifies. "The available evidence supports a coherent explanation." "The supported premises are sufficient to specify the trial." "Affirmative evidence demonstrates a mismatch that defeats the rationale." "The uncertainty is localized." No single finding can establish a verdict, so a verdict is never a REQUIRED_SUPPORT unit.
- Finding-sized: what the world must be like for the verdict to hold. "Drug X reaches tissue T at doses used clinically." "Drug X increases contractile force in an animal model of condition C." "In patients with C, adding X to standard care improved measure M."

HOW TO DECOMPOSE. A hypothesis sentence is usually a verdict resting on several premises. For each sentence of the hypothesis statement:
1. Ask which separate empirical facts must be true for the sentence to hold. The hypothesis's own assumptions and the header's decisive-test questions (supplied below) name the links the human cares about, for example exposure, target, functional effect, timing, transfer between models, attribution, and who responds. Use them.
2. Write one REQUIRED_SUPPORT unit per necessary fact, as a plain declarative proposition. State its scope inside the unit: the agent, the effect, and the population, species, model, tissue or exposure level that the hypothesis's own wording requires. Do not make the scope narrower than the hypothesis needs. When the hypothesis needs only that a capability or mechanism exists ("X can do Y"), write the unit so that one reported instance in a relevant model or in humans establishes it. When the hypothesis needs a fact about its own population, say so in the unit.
3. When the hypothesis says that any ONE of several findings would do ("a mismatch in exposure, tissue, timing or ..."), write ONE unit that names the alternatives: "At least one of the following is reported: (a) ...; (b) ...; (c) ...". Never split alternatives into separate REQUIRED_SUPPORT units. Every REQUIRED_SUPPORT unit must be covered, so splitting would wrongly demand all of them.
4. Whatever is still verdict-sized after this (sufficiency, coherence, "cannot distinguish", "not determined") is recorded as an EVALUATIVE_JUDGMENT unit. A hypothesis that says only that the evidence is insufficient or unresolved may have no REQUIRED_SUPPORT unit at all. That is correct: record its sentences as EVALUATIVE_JUDGMENT, and put any concrete finding it predicts (for example "no source reports tissue concentrations of X") under CORROBORATING_EXPECTATION.

UNIT TYPES.
- REQUIRED_SUPPORT - a finding-sized fact that must receive affirmative witness coverage before the hypothesis has complete coverage.
- CONTEXTUAL_CONSTRAINT - an assumption, boundary or qualification that every coverage set must continue to satisfy. A selected witness must not contradict it. Finding-sized.
- ADVERSE_TEST - ONE finding-sized result that would count against or falsify the hypothesis (from its potential-falsification text). One result per unit. Visible, not mandatory.
- CORROBORATING_EXPECTATION - ONE finding-sized result the hypothesis leads the analyst to expect (from its potential-corroboration text). Visible, not mandatory.
- EVALUATIVE_JUDGMENT - a verdict about the evidence base as a whole. It stays visible and is assessed by the analyst and the final assessment, not by witness matching.

RULES.
1. Every unit carries "source_quote": an EXACT, contiguous quotation of at least 6 words, copied character for character from the hypothesis text or the header passages below. It is the passage that licenses the unit. Several units may quote the same sentence. The quote is checked mechanically, and a unit whose quote is not found is dropped.
2. Typical counts: 4-9 REQUIRED_SUPPORT units for an affirmative hypothesis; 1-3 for a hypothesis that needs only a defeating finding; 0 for a purely "unresolved" hypothesis. Also 1-3 CONTEXTUAL_CONSTRAINT, 2-6 ADVERSE_TEST and 2-6 CORROBORATING_EXPECTATION units, when the text states them. No padding and no near-duplicates.
3. Write each unit in plain words that a reader outside the project understands. Do not mention hypothesis labels (H1, H2), "the rationale", "the evidence", "the premises" or "the trial specification" in a REQUIRED_SUPPORT, CONTEXTUAL_CONSTRAINT, ADVERSE_TEST or CORROBORATING_EXPECTATION unit.
4. "evidence_terms": 5-15 words or short phrases that a satisfying source finding would likely contain. They are used only to shortlist candidates for matching, never to decide a match.
5. "satisfied_by": one sentence naming the kind of published finding that would make the unit true, for example "a pharmacokinetic study that measures X in tissue T after clinical dosing".
6. "serves": a few words naming the hypothesis sentence or decisive test the unit comes from, for example "exposure" or "functional link".

WORKED EXAMPLE (a different domain; follow the method, not the content).
Hypothesis sentence: "The available engineering evidence supports a coherent explanation for why sealing the deck would meaningfully slow reinforcement corrosion in coastal bridges. Chloride reaches the steel through the deck, and a sealer can block that route at field application rates."
Wrong: REQUIRED_SUPPORT "The available engineering evidence supports a coherent explanation for why sealing the deck would slow corrosion" (verdict-sized).
Right:
- REQUIRED_SUPPORT "In coastal bridge decks, chloride concentration at reinforcement depth reaches the level at which steel corrosion starts." (serves: cause is present)
- REQUIRED_SUPPORT "A deck sealer applied at a field application rate reduces chloride ingress into concrete, in a laboratory or field test." (serves: the intervention acts on the cause)
- REQUIRED_SUPPORT "Reducing chloride ingress slows reinforcement corrosion, measured as corrosion rate, section loss or time to cracking." (serves: functional link)
- EVALUATIVE_JUDGMENT "The available engineering evidence supports a coherent explanation for why sealing the deck would meaningfully slow reinforcement corrosion in coastal bridges."

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
{{REVISION_NOTE}}
Return ONLY a JSON object:
{
  "hypothesis_id": "{{HID}}",
  "units": [
    {"code": "R1", "type": "REQUIRED_SUPPORT", "text": "", "serves": "", "source_quote": "", "evidence_terms": [""], "satisfied_by": ""},
    {"code": "C1", "type": "CONTEXTUAL_CONSTRAINT", "text": "", "serves": "", "source_quote": "", "evidence_terms": [""], "satisfied_by": ""},
    {"code": "A1", "type": "ADVERSE_TEST", "text": "", "serves": "", "source_quote": "", "evidence_terms": [""], "satisfied_by": ""},
    {"code": "E1", "type": "CORROBORATING_EXPECTATION", "text": "", "serves": "", "source_quote": "", "evidence_terms": [""], "satisfied_by": ""},
    {"code": "J1", "type": "EVALUATIVE_JUDGMENT", "text": "", "serves": "", "source_quote": "", "evidence_terms": [], "satisfied_by": ""}
  ],
  "notes": "anything the analyst should know about this representation"
}
