"""One standard for support and contradiction from another scope, and boundaries that are not claims.

A finding from another population, species, model or dose supports a unit only if a transfer is
granted.  The same has to hold when it counts against a unit: in coverage validity, in the premise
ledger and in the report, as it already did in the crux tests.  And a constraint that only says what
the hypothesis is about cannot be contradicted by a study of something else.
"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.coverage import Option, Problem, build_problem, cover_hypothesis, solve  # noqa: E402
from claimreg.crux import compile_theory, test_t1, test_t2  # noqa: E402
from claimreg.ledger import build_ledger, render_ledger  # noqa: E402
from claimreg.units import constraint_kind  # noqa: E402
from test_core import brute_force_sets  # noqa: E402

GAP = "the result in healthy volunteers also holds in the patients the premise is about"
CFG = {"assume_gaps": ["SCOPE"]}


def unit(uid, typ, **kw):
    return {"unit_id": uid, "hypothesis_id": "H1", "axis_id": "A1", "type": typ, "text": f"text of {uid}",
            "active": True, **kw}


def rel(d):
    out = {}
    for (w, u), v in d.items():
        v = v if isinstance(v, dict) else {"final": v}
        out[(w, u)] = {"basis": "AGREED", "trace": "t", **v}
    return out


UNITS = [unit("H1-R1", "REQUIRED_SUPPORT"), unit("H1-R2", "REQUIRED_SUPPORT"),
         unit("H1-C1", "CONTEXTUAL_CONSTRAINT")]
SCOPE_CONTRA = {"final": "CONTRADICTS", "gap_type": "SCOPE", "gap": GAP}


class PremiseTest(unittest.TestCase):
    def test_a_conditional_contradiction_becomes_a_named_assumption(self):
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W2", "H1-R2"): "EQUIVALENT", ("W1", "H1-C1"): SCOPE_CONTRA})
        pb, info, res, strict, _ = cover_hypothesis("H1", UNITS, r, [], [], CFG)
        self.assertEqual(pb.constraint_violators, {})                       # not a veto
        self.assertEqual([s["witnesses"] for s in res["sets"]], [["W1", "W2"]])
        s = res["sets"][0]
        self.assertEqual(s["contrary_assumed_not_to_transfer"],
                         [{"constraint_id": "H1-C1", "witness_id": "W1", "transfer": GAP}])
        self.assertNotIn("assumptions", s)                                  # every part is covered directly
        # all support is direct, yet the hypothesis is not reported as complete without assumptions
        self.assertEqual((res["status"], strict), ("COMPLETE_WITH_ASSUMPTIONS", 2))

    def test_a_set_that_avoids_the_witness_needs_no_assumption(self):
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W3", "H1-R1"): "EQUIVALENT", ("W2", "H1-R2"): "EQUIVALENT",
                 ("W1", "H1-C1"): SCOPE_CONTRA})
        _, _, res, _, _ = cover_hypothesis("H1", UNITS, r, [], [], CFG)
        need = {tuple(s["witnesses"]): s["needs_assumptions"] for s in res["sets"]}
        self.assertEqual(need, {("W1", "W2"): True, ("W2", "W3"): False})
        self.assertEqual(res["status"], "COMPLETE")

    def test_an_outright_contradiction_still_invalidates_the_set(self):
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W2", "H1-R2"): "EQUIVALENT", ("W1", "H1-C1"): "CONTRADICTS"})
        pb, _, res, _, _ = cover_hypothesis("H1", UNITS, r, [], [], CFG)
        self.assertEqual(pb.constraint_violators, {"W1": ["H1-C1"]})
        self.assertEqual((res["status"], res["sets"]), ("NO_COMPLETE_COVERAGE", []))

    def test_the_rule_does_not_depend_on_the_assumption_tier(self):
        # with the conditional-support tier switched off, a conditional contradiction is still not a veto
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W2", "H1-R2"): "EQUIVALENT", ("W1", "H1-C1"): SCOPE_CONTRA})
        _, _, res, _, _ = cover_hypothesis("H1", UNITS, r, [], [], {"assume_gaps": []})
        self.assertEqual(res["status"], "COMPLETE_WITH_ASSUMPTIONS")
        self.assertEqual(len(res["sets"][0]["contrary_assumed_not_to_transfer"]), 1)

    def test_a_missing_transfer_text_is_marked(self):
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W2", "H1-R2"): "EQUIVALENT",
                 ("W1", "H1-C1"): {"final": "CONTRADICTS", "gap_type": "SCOPE"}})
        _, _, res, _, _ = cover_hypothesis("H1", UNITS, r, [], [], CFG)
        self.assertTrue(res["sets"][0]["contrary_assumed_not_to_transfer"][0]["assumption_text_missing"])

    def test_records_without_gap_data_decide_as_before(self):
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W2", "H1-R2"): "EQUIVALENT", ("W3", "H1-R2"): "EQUIVALENT",
                 ("W2", "H1-C1"): "CONTRADICTS"})
        pb, _, res, _, _ = cover_hypothesis("H1", UNITS, r, [], [], CFG)
        self.assertEqual((res["status"], [s["witnesses"] for s in res["sets"]]), ("COMPLETE", [["W1", "W3"]]))
        self.assertEqual((pb.constraint_violators, pb.conditional_hits), ({"W2": ["H1-C1"]}, {}))


class TransferConflictTest(unittest.TestCase):
    """One finding cannot both transfer (to support) and not transfer (against a premise)."""
    R = {("W1", "H1-R1"): "EQUIVALENT",
         ("W2", "H1-R2"): {"final": "PARTIALLY_COVERS", "gap_type": "SCOPE", "gap": "the rat result transfers to men"},
         ("W2", "H1-C1"): SCOPE_CONTRA}

    def test_rejected_by_default(self):
        pb, info, res, _, conflicts = cover_hypothesis("H1", UNITS, rel(self.R), [], [], CFG)
        self.assertEqual((res["status"], res["sets"], res["uncovered_units"]), ("NO_COMPLETE_COVERAGE", [], ["H1-R2"]))
        self.assertEqual([(c["reason"], c["unit_id"], c["witness_id"], c["option_offered"]) for c in conflicts],
                         [("TRANSFER_CONFLICT", "H1-R2", "W2", False)])
        self.assertIn("TRANSFER_CONFLICT", res["note"])

    def test_flag_keeps_the_set_and_lists_both_transfers(self):
        _, _, res, _, _ = cover_hypothesis("H1", UNITS, rel(self.R), [], [], {**CFG, "transfer_conflict": "flag"})
        self.assertEqual(res["status"], "COMPLETE_WITH_ASSUMPTIONS")
        s = res["sets"][0]
        self.assertEqual(s["assumptions"][0]["assumption"], "the rat result transfers to men")
        self.assertEqual(s["contrary_assumed_not_to_transfer"][0]["transfer"], GAP)
        self.assertEqual(s["transfer_conflicts"][0]["contrary"], [{"constraint_id": "H1-C1", "transfer": GAP}])

    def test_another_witness_can_still_cover_the_unit_conditionally(self):
        r = {**self.R, ("W4", "H1-R2"): {"final": "PARTIALLY_COVERS", "gap_type": "SCOPE", "gap": "the dog result transfers"}}
        _, _, res, _, _ = cover_hypothesis("H1", UNITS, rel(r), [], [], CFG)
        self.assertEqual([s["witnesses"] for s in res["sets"]], [["W1", "W4"]])
        self.assertNotIn("contrary_assumed_not_to_transfer", res["sets"][0])

    def test_a_direct_match_of_the_same_witness_is_not_a_conflict(self):
        # W2 covers R2 as written (same scope) and is contrary to the premise only from another scope:
        # nothing is granted for support, so there is one assumption and no conflict
        r = {**self.R, ("W2", "H1-R2"): "EQUIVALENT"}
        _, _, res, _, conflicts = cover_hypothesis("H1", UNITS, rel(r), [], [], CFG)
        self.assertEqual((conflicts, res["status"]), ([], "COMPLETE_WITH_ASSUMPTIONS"))


class BoundaryTest(unittest.TestCase):
    """A constraint that says what the hypothesis is about is enforced through scope, not by contradiction."""
    BOUNDARY = [unit("H1-R1", "REQUIRED_SUPPORT"), unit("H1-C1", "CONTEXTUAL_CONSTRAINT", constraint_kind="BOUNDARY"),
                unit("H1-C2", "CONTEXTUAL_CONSTRAINT")]

    def test_kind_comes_from_the_compiler_or_a_recorded_override(self):
        c1, c2 = self.BOUNDARY[1], self.BOUNDARY[2]
        self.assertEqual((constraint_kind(c1), constraint_kind(c2)), ("BOUNDARY", "PREMISE"))   # unclassified = premise
        self.assertEqual(constraint_kind(c2, {"H1-C2": "boundary"}), "BOUNDARY")
        self.assertEqual(constraint_kind(c1, {"H1-C1": "PREMISE"}), "PREMISE")
        self.assertEqual(constraint_kind(self.BOUNDARY[0]), "")

    def test_a_boundary_is_neither_a_veto_nor_a_t1_conflict(self):
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W1", "H1-C1"): "CONTRADICTS", ("X", "H1-C1"): "CONTRADICTS",
                 ("X", "H1-R1"): "NO_SEMANTIC_RELATION", ("X", "H1-C2"): "NO_SEMANTIC_RELATION"})
        pb, info, res, _, _ = cover_hypothesis("H1", self.BOUNDARY, r, [], [], CFG)
        self.assertEqual((res["status"], pb.constraint_violators), ("COMPLETE", {}))
        self.assertEqual(info["outside_scope"], {"W1": ["H1-C1"], "X": ["H1-C1"]})
        cov = {"options": {"H1-R1": [{"option_id": "o", "witnesses": ["W1"], "relation": "EQUIVALENT"}]},
               "constraint_violators": pb.constraint_violators}
        th = compile_theory("H1", self.BOUNDARY, cov, [])
        self.assertEqual((th["constraints"], th["boundaries"]), (["H1-C2"], ["H1-C1"]))
        t1, cert = test_t1("X", th, r)
        self.assertEqual((t1, cert["outside_rival_scope"]), ("PASS", ["H1-C1"]))
        self.assertEqual(test_t2("X", th, r, set())[0], "PASS")
        # the same record with the constraint read as a premise is a veto and a T1 failure: today's rule
        kinds = {"H1-C1": "PREMISE"}
        pb, _, res, _, _ = cover_hypothesis("H1", self.BOUNDARY, r, [], [], {**CFG, "constraint_kinds": kinds})
        self.assertEqual((res["status"], pb.constraint_violators), ("NO_COMPLETE_COVERAGE", {"W1": ["H1-C1"], "X": ["H1-C1"]}))
        self.assertEqual(test_t1("X", compile_theory("H1", self.BOUNDARY, cov, [], kinds), r)[0], "FAIL")

    def test_a_theory_without_boundaries_keeps_its_id(self):
        plain = [unit("H1-R1", "REQUIRED_SUPPORT"), unit("H1-C2", "CONTEXTUAL_CONSTRAINT")]
        th = compile_theory("H1", plain, {}, [])
        self.assertNotIn("boundaries", th)

    def test_the_ledger_and_its_text_call_it_out_of_scope(self):
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("X", "H1-C1"): "CONTRADICTS"})
        led = build_ledger(self.BOUNDARY, r, [], {})
        row = {x["unit_id"]: x for x in led["hypotheses"]["H1"]}["H1-C1"]
        self.assertEqual((row["status"], row["outside_scope"], row["contradicted_by"]), ("BOUNDARY", ["X"], []))
        self.assertEqual(led["summary"]["H1"]["constraints_contradicted"], [])
        frame = {"axes": [{"axis_id": "A1", "question": "q", "hypotheses": [{"id": "H1", "title": "t"}]}]}
        text = render_ledger(frame, led, {}, {}, self.BOUNDARY)
        self.assertIn("**The hypothesis is about** `H1-C1`", text)
        self.assertIn("outside this hypothesis's scope: `X`", text)


class LedgerTest(unittest.TestCase):
    def test_conditional_contradictions_have_their_own_statuses(self):
        units = [unit(f"H1-R{i}", "REQUIRED_SUPPORT") for i in (1, 2, 3, 4)]
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W9", "H1-R1"): SCOPE_CONTRA,          # full + conditional only
                 ("W1", "H1-R2"): "EQUIVALENT", ("W9", "H1-R2"): SCOPE_CONTRA, ("W8", "H1-R2"): "CONTRADICTS",
                 ("W9", "H1-R3"): SCOPE_CONTRA,                                         # conditional only
                 ("W8", "H1-R4"): "CONTRADICTS"})
        led = build_ledger(units, r, [], {})
        rows = {x["unit_id"]: x for x in led["hypotheses"]["H1"]}
        self.assertEqual({u: x["status"] for u, x in rows.items()},
                         {"H1-R1": "CONTESTED_IF_TRANSFERRED", "H1-R2": "CONTESTED",
                          "H1-R3": "CONTRADICTED_IF_TRANSFERRED", "H1-R4": "CONTRADICTED"})
        self.assertEqual(rows["H1-R1"]["contradicted_by"], [])
        self.assertEqual(rows["H1-R1"]["contradicted_if_transferred"], [{"witness_id": "W9", "transfer": GAP}])
        self.assertEqual(rows["H1-R2"]["contradicted_by"], ["W8"])
        frame = {"axes": [{"axis_id": "A1", "question": "q", "hypotheses": [{"id": "H1", "title": "t"}]}]}
        self.assertIn("counts against it if the finding transfers", render_ledger(frame, led, {}, {}, units))


class SolverTest(unittest.TestCase):
    def test_conditional_hits_never_change_which_sets_exist(self):
        """Validity stays monotone: the brute-force agreement holds with conditional hits in the
        problem, and the sets are the ones the same problem has without them."""
        rng = random.Random(11)
        for trial in range(150):
            ws = [f"W{i}" for i in range(rng.randint(1, 6))]
            units = [f"U{j}" for j in range(rng.randint(1, 4))]
            opts = {}
            for u in units:
                lst = []
                for k in range(rng.randint(0, 3)):
                    size = 1 if rng.random() < 0.7 else 2
                    mem = tuple(sorted(rng.sample(ws, min(size, len(ws)))))
                    lst.append(Option(f"{u}-{k}", u, mem, "EQUIVALENT" if size == 1 else "JOINTLY_SUFFICIENT", size > 1))
                opts[u] = lst
            viol = {rng.choice(ws): ["C1"]} if rng.random() < 0.3 else {}
            inc = {frozenset(rng.sample(ws, 2))} if rng.random() < 0.3 and len(ws) >= 2 else set()
            cond = {w: [{"constraint_id": "C2", "witness_id": w, "transfer": GAP}] for w in ws if rng.random() < 0.4}
            pb = Problem("H", units, opts, viol, inc, cond)
            got = {frozenset(s["witnesses"]) for s in solve(pb, max_states=10000, max_sets=10000)["sets"]}
            self.assertEqual(got, brute_force_sets(pb), f"trial {trial}")
            plain = {frozenset(s["witnesses"])
                     for s in solve(Problem("H", units, opts, viol, inc), max_states=10000, max_sets=10000)["sets"]}
            self.assertEqual(got, plain, f"trial {trial}")

    def test_assumptions_are_read_off_the_final_set(self):
        # W5 is in a candidate but is deleted from the minimal set; its conditional hit must not be listed
        units = [unit("H1-R1", "REQUIRED_SUPPORT"), unit("H1-C1", "CONTEXTUAL_CONSTRAINT")]
        r = rel({("W1", "H1-R1"): "EQUIVALENT", ("W5", "H1-C1"): SCOPE_CONTRA})
        groups = [{"approved": True, "unit_id": "H1-R1", "witnesses": ["W1", "W5"]}]
        _, _, res, _, _ = cover_hypothesis("H1", units, r, groups, [], CFG)
        self.assertEqual([s["witnesses"] for s in res["sets"]], [["W1"]])
        self.assertNotIn("contrary_assumed_not_to_transfer", res["sets"][0])
        self.assertEqual(res["status"], "COMPLETE")


if __name__ == "__main__":
    unittest.main()
