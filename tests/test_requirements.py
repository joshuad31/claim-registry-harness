"""The hypothesis-to-requirements view: what each sentence of a hypothesis was compiled into.

It reads saved records only.  It makes no model call, it is not a gate, and it changes no result.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.requirements import build_view, locate, reading_of, render_view, split_sentences, write_view  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import read_jsonl  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402
from test_pipeline_mock import make_project  # noqa: E402

H1 = {"id": "H1", "title": "Sealing slows corrosion",
      "statement": "Yes. Chloride reaches the steel through the deck, a sealer blocks that route at field rates, "
                   "and less chloride means slower corrosion. Engineers should therefore seal coastal decks.",
      "assumptions": "The sealer is applied at the rate the maker states, e.g. two coats.",
      "falsification": "A field trial in which sealed decks corroded as fast as unsealed ones.",
      "corroboration": "Lower chloride at bar depth under sealed decks."}
FRAME = {"axes": [{"axis_id": "A1", "question": "Does sealing the deck slow corrosion?",
                   "hypotheses": [H1, {"id": "H2", "title": "No effect", "statement": "Sealing changes nothing."}]}],
         "mission": "Decide whether the agency should seal coastal bridge decks this decade."}


def unit(code, typ, text, quote, **kw):
    return {"unit_id": f"H1-{code}", "hypothesis_id": "H1", "axis_id": "A1", "type": typ, "text": text,
            "source_quote": quote, "quote_check": {"found": True, "method": "exact"},
            "serves": "", "satisfied_by": "", "active": typ != "EVALUATIVE_JUDGMENT", "inactive_reason": "", **kw}


UNITS = [
    unit("R1", "REQUIRED_SUPPORT", "Chloride reaches reinforcement depth in coastal decks.",
         "Chloride reaches the steel through the deck"),
    unit("R2", "REQUIRED_SUPPORT", "A sealer applied at a field rate reduces chloride ingress.",
         "a sealer blocks that route at field rates"),
    unit("R3", "REQUIRED_SUPPORT", "At least one of the following is reported: (a) a lower corrosion rate with less "
         "chloride; (b) less section loss with less chloride; (c) a longer time to cracking with less chloride.",
         "less chloride means slower corrosion"),
    unit("R4", "REQUIRED_SUPPORT", "Chloride at bar depth is lower under sealed decks.",
         "Lower chloride at bar depth under sealed decks."),
    unit("C1", "CONTEXTUAL_CONSTRAINT", "The sealer is applied at the maker's stated rate.",
         "The sealer is applied at the rate the maker states", constraint_kind="PREMISE"),
    unit("C2", "CONTEXTUAL_CONSTRAINT", "The question is about coastal bridge decks.",
         "seal coastal bridge decks this decade", constraint_kind="BOUNDARY"),
    unit("A1", "ADVERSE_TEST", "Sealed decks corroded as fast as unsealed ones in a field trial.",
         "A field trial in which sealed decks corroded as fast as unsealed ones."),
    unit("J1", "EVALUATIVE_JUDGMENT", "The evidence supports sealing as a policy.",
         "Yes. Chloride reaches the steel", derived_type="REQUIRED_SUPPORT",
         inactive_reason="verdict-sized after one revision (\"evidence supports\"): recorded as an evaluative "
                         "judgment; no single finding could establish it"),
    unit("X1", "REQUIRED_SUPPORT", "Sealers last ten years.", "sealers are durable for a decade", active=False,
         inactive_reason="source_quote not found verbatim in the frozen hypothesis/header text (unanchored)"),
]
COVERAGE = {"H1": {"status": "COMPLETE_WITH_ASSUMPTIONS", "options": {
    "H1-R1": [{"option_id": "o1", "witnesses": ["W1"], "relation": "EQUIVALENT"}],
    "H1-R2": [{"option_id": "o2", "witnesses": ["W2"], "relation": "PARTIALLY_COVERS", "assumption": "lab to field"}],
    "H1-R3": [{"option_id": "o3", "witnesses": ["W3"], "relation": "EQUIVALENT"}], "H1-R4": []},
    "sets": [{"set_id": "S1", "witnesses": ["W1", "W2", "W3"],
              "assumptions": [{"unit_id": "H1-R2", "witness_id": "W2", "assumption": "lab to field"}],
              "contrary_assumed_not_to_transfer": [{"constraint_id": "H1-C1", "witness_id": "W3", "transfer": "t"}]}]}}
LEDGER = {"hypotheses": {"H1": [{"unit_id": "H1-R1", "status": "ESTABLISHED"},
                                {"unit_id": "H1-R2", "status": "SUPPORTED_WITH_ASSUMPTION"}]}}


class TextTest(unittest.TestCase):
    def test_sentences(self):
        s = split_sentences(H1["statement"])
        self.assertEqual(len(s), 3)
        self.assertEqual(s[0], "Yes.")
        # an abbreviation does not end a sentence
        self.assertEqual(len(split_sentences(H1["assumptions"])), 1)
        self.assertEqual(split_sentences(""), [])

    def test_a_quotation_is_located_in_every_sentence_it_touches(self):
        sents = [{"n": i + 1, "text": t} for i, t in enumerate(split_sentences(H1["statement"]))]
        self.assertEqual(locate("Yes. Chloride reaches the steel", sents, "")["sentences"], [1, 2])
        self.assertEqual(locate("seal coastal decks", sents, "")["sentences"], [3])
        self.assertEqual(locate("not anywhere in the text at all", sents, "")["where"], "unanchored")
        self.assertEqual(locate("an agency decision this decade", sents, "an agency decision this decade")["where"], "header")

    def test_a_quotation_found_twice_is_reported_in_both_places(self):
        sents = [{"n": 1, "text": "The sealer blocks chloride at field rates."},
                 {"n": 2, "text": "In the laboratory the sealer blocks chloride as well."}]
        loc = locate("the sealer blocks chloride", sents, "")
        self.assertEqual((loc["occurrences"], loc["sentences"]), (2, [1, 2]))

    def test_alternatives_are_read_from_the_prescribed_form_only(self):
        r = reading_of(UNITS[2]["text"])
        self.assertEqual((r["reading"], [a["label"] for a in r["alternatives"]]), ("ANY_OF", ["a", "b", "c"]))
        self.assertEqual(r["alternatives"][1]["text"], "less section loss with less chloride")
        self.assertEqual(reading_of("Chloride reaches the steel.")["reading"], "SINGLE")
        # alternatives in another form are flagged for a person, not guessed at
        self.assertEqual(reading_of("Either corrosion slows or cracking is delayed.")["reading"], "UNCLEAR")


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.view = build_view(FRAME, UNITS, COVERAGE, LEDGER, "", {})
        self.v = self.view["hypotheses"]["H1"]
        self.md = render_view(self.view, FRAME)

    def test_a_sentence_with_no_unit_is_checked_by_nothing(self):
        # sentence 3 ("Engineers should therefore seal coastal decks.") produced no unit; "Yes." is not counted
        self.assertEqual(self.v["unmapped_sentences"], [3])
        self.assertIn("**Written by you, checked by nothing.**", self.md)
        self.assertIn("sentence 3", self.md)

    def test_one_sentence_three_required_units_is_all_of_three(self):
        self.assertEqual(self.v["how_read"]["conjunctions"], [{"sentence": 2, "units": ["H1-R1", "H1-R2", "H1-R3"]}])
        self.assertIn("Sentence 2 was read as requiring ALL of: `H1-R1`, `H1-R2`, `H1-R3`.", self.md)

    def test_an_at_least_one_of_unit_is_any_one(self):
        self.assertEqual([a["unit_id"] for a in self.v["how_read"]["alternatives"]], ["H1-R3"])
        self.assertIn("`H1-R3` was read as requiring ANY ONE of: (a) a lower corrosion rate", self.md)
        self.assertIn("It is one requirement", self.md)

    def test_a_demoted_verdict_is_not_a_requirement_and_says_why(self):
        ev = self.v["not_requirements"]["evaluative"]
        self.assertEqual((ev[0]["unit_id"], ev[0]["derived_type"]), ("H1-J1", "REQUIRED_SUPPORT"))
        self.assertIn("demoted: verdict-sized after one revision", self.md)
        self.assertEqual([x["unit_id"] for x in self.v["not_requirements"]["inactive"]], ["H1-X1"])
        # neither appears as a row of the requirements that coverage uses
        rows = [l for l in self.md.splitlines() if l.startswith("| `H1-J1`")]
        self.assertEqual(rows, [])

    def test_every_unit_is_in_the_view_with_its_role(self):
        self.assertEqual(len(self.v["units"]), len(UNITS))
        role = {u["unit_id"]: u["role"] for u in self.v["units"]}
        self.assertEqual(role["H1-R1"], "must be supported")
        self.assertEqual(role["H1-C1"], "must not be contradicted")
        self.assertEqual(role["H1-C2"], "the hypothesis is about")
        self.assertTrue(role["H1-A1"].startswith("visible, not required"))
        self.assertEqual(self.v["counts"]["REQUIRED_SUPPORT"], 5)
        # a recorded override changes the role and nothing else
        v2 = build_view(FRAME, UNITS, COVERAGE, LEDGER, "", {"H1-C1": "BOUNDARY"})["hypotheses"]["H1"]
        self.assertEqual({u["unit_id"]: u["role"] for u in v2["units"]}["H1-C1"], "the hypothesis is about")

    def test_what_is_not_recorded_is_not_reconstructed(self):
        self.assertEqual(self.v["how_read"]["why_divided_this_way"], "NOT RECORDED")
        self.assertIn("Why each sentence was divided as it was: NOT RECORDED", self.md)
        self.assertIn("not a finding that the text means it", self.md)

    def test_anchors_outside_the_hypothesis_and_missing_anchors(self):
        self.assertEqual(self.v["header_anchored_units"], ["H1-C2"])
        self.assertEqual(self.v["unanchored_units"], ["H1-X1"])

    def test_coverage_state_and_what_it_permits(self):
        c = self.v["coverage"]
        self.assertEqual((c["required"], c["covered_directly"], c["covered_only_with_a_transfer"]), (4, 2, 1))
        by = {u["unit_id"]: u for u in self.v["units"]}
        self.assertEqual(by["H1-R2"]["coverage"], {"strict_options": 0, "conditional_options": 1, "witnesses": ["W2"]})
        self.assertEqual((by["H1-R1"]["status"], by["H1-J1"]["status"]), ("ESTABLISHED", "NOT_MATCHED"))
        means = " ".join(self.v["complete_coverage"]["means"])
        self.assertIn("No witness in the set is known to contradict a listed premise outright", means)
        self.assertIn("grants 1 transfer(s) for support and assumes 1 contrary finding(s)", means)
        self.assertIn("that the hypothesis is true", " ".join(self.v["complete_coverage"]["does_not_mean"]))
        # a hypothesis with no required unit says so
        h2 = self.view["hypotheses"]["H2"]
        self.assertIn("no finding-sized requirement", h2["complete_coverage"]["means"][0])

    def test_diagnostics_are_shown(self):
        d = self.v["diagnostics"]
        self.assertEqual(d["required_units_without_an_option"], ["H1-R4"])
        # R4 is a requirement licensed only by "what would corroborate" text
        self.assertEqual(d["required_units_anchored_only_on_corroboration_or_falsification_text"],
                         [{"unit_id": "H1-R4", "part": "Potential corroboration"}])
        self.assertIn("`H1-R4` has no coverage option", self.md)
        self.assertIn("\"Potential corroboration\" text", self.md)
        dup = build_view(FRAME, UNITS + [unit("R9", "REQUIRED_SUPPORT", "Chloride gets to the bars.",
                                              "Chloride reaches the steel through the deck")], COVERAGE, LEDGER)
        self.assertEqual(dup["hypotheses"]["H1"]["diagnostics"]["required_units_anchored_on_the_same_words"],
                         [["H1-R1", "H1-R9"]])


class StageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("requirements")

    def tearDown(self):
        cleanup(self.tmp)

    def test_the_coverage_stage_writes_the_view_without_a_model_call(self):
        proj = make_project(self.tmp)
        ctx = RunContext(proj, "RUN-REQ", create=True, quiet=True)
        out = run_pipeline(ctx)
        self.assertEqual(out["status"], "complete", out)
        sc = ctx.scopes()[0]
        md = sc.p("coverage", "HYPOTHESIS-REQUIREMENTS.md")
        self.assertTrue(md.exists())
        view = sc.load("coverage", "HYPOTHESIS-REQUIREMENTS.json")
        units = sc.load("matching", "01_hypothesis-units/units.json")
        self.assertEqual(sum(len(v["units"]) for v in view["hypotheses"].values()), len(units))
        # the report leads with it, and the audit browser carries it
        rep = sc.p("reports", "CRUX-REPORT.md").read_text(encoding="utf-8")
        self.assertLess(rep.index("## How each hypothesis was compiled"), rep.index("## Crux candidates"))
        self.assertIn("Requirements:showReq", sc.p("reports", "report.html").read_text(encoding="utf-8"))
        # writing it again asks no model anything
        log = ctx.p("control", "model-and-human-decisions", "llm-calls.jsonl")
        before = len(read_jsonl(log))
        write_view(sc, sc.load("coverage", "coverage.json")["hypotheses"])
        self.assertEqual(len(read_jsonl(log)), before)


if __name__ == "__main__":
    unittest.main()
