"""Finding-sized units, gap-typed partial matches, model routing, the assumption-labelled coverage
tier and the premise ledger."""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fakes  # noqa: E402
from claimreg.coverage import build_problem, solve  # noqa: E402
from claimreg.ledger import build_ledger  # noqa: E402
from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.units import verdict_sized  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402
from test_pipeline_mock import make_project  # noqa: E402

SCRIPTED = {"type": "scripted", "model": "scripted-1", "script": "s"}


def _quote(h: dict) -> str:
    return " ".join(h["statement"].split()[:8])


class VerdictLintTest(unittest.TestCase):
    def test_verdicts_are_flagged_and_findings_are_not(self):
        for t in ("The available pharmacological evidence supports a coherent causal explanation.",
                  "The supported premises are sufficient to specify the trial.",
                  "Affirmative evidence demonstrates a mismatch in exposure.",
                  "The uncertainty is localized to identified links.",
                  "Existing evidence cannot distinguish H1 from H2."):
            self.assertTrue(verdict_sized(t), t)
        for t in ("Drug X reaches bladder tissue at doses used clinically.",
                  "Histological evidence of fibrosis is reported in obstructed bladders.",
                  "A randomized trial demonstrates improved flow with drug X.",
                  "In men with outlet obstruction, adding drug X improved maximum flow rate."):
            self.assertFalse(verdict_sized(t), t)


class UnitRevisionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("premises-units")
        fakes.reset()

    def tearDown(self):
        cleanup(self.tmp)

    def run_units(self, script):
        fakes.SCRIPTS["s"] = script
        proj = make_project(self.tmp, extra={"roles": {"unit_deriver": "scripted"},
                                             "providers": {"scripted": SCRIPTED}})
        ctx = RunContext(proj, "RUN-U", create=True, quiet=True)
        out = run_pipeline(ctx, stop="units")
        self.assertEqual(out["status"], "complete", out)
        return ctx, ctx.load("matching", "01_hypothesis-units/units.json"), ctx.stage_state()["units"]["summary"]

    def test_verdict_sized_units_get_one_revision(self):
        def script(req, prov):
            h = req.meta["hypothesis"]
            q = _quote(h)
            if "REVISION REQUESTED" not in req.user:
                return {"units": [{"code": "R1", "type": "REQUIRED_SUPPORT", "source_quote": q,
                                   "text": "The available evidence supports a coherent explanation of the effect."}]}
            return {"units": [
                {"code": "R1", "type": "REQUIRED_SUPPORT", "source_quote": q, "serves": "functional link",
                 "text": "The treatment increases yield in at least one field trial."},
                {"code": "J1", "type": "EVALUATIVE_JUDGMENT", "source_quote": q,
                 "text": "The available evidence supports a coherent explanation of the effect."}]}
        ctx, units, summ = self.run_units(script)
        req = [u for u in units if u["type"] == "REQUIRED_SUPPORT"]
        self.assertTrue(req and all(u["active"] for u in req))
        self.assertFalse(any(verdict_sized(u["text"]) for u in req))
        self.assertEqual(req[0]["serves"], "functional link")
        self.assertTrue(summ["revised_hypotheses"])
        self.assertEqual(summ["verdict_sized_demoted"], 0)
        self.assertTrue(any(u["type"] == "EVALUATIVE_JUDGMENT" and not u["active"] for u in units))

    def test_a_unit_still_verdict_sized_after_revision_is_demoted_not_required(self):
        def script(req, prov):
            return {"units": [{"code": "R1", "type": "REQUIRED_SUPPORT", "source_quote": _quote(req.meta["hypothesis"]),
                               "text": "The available evidence supports a coherent explanation of the effect."}]}
        ctx, units, summ = self.run_units(script)
        self.assertFalse(any(u["type"] == "REQUIRED_SUPPORT" for u in units))
        self.assertTrue(all(u["type"] == "EVALUATIVE_JUDGMENT" and u["derived_type"] == "REQUIRED_SUPPORT"
                            for u in units))
        self.assertGreater(summ["verdict_sized_demoted"], 0)
        self.assertTrue(summ["hypotheses_without_required_units"])


def _rel(final, basis="AGREED", **kw):
    return {"final": final, "basis": basis, "trace": "t", **kw}


class ConditionalCoverageTest(unittest.TestCase):
    UNITS = [{"unit_id": f"H1-R{i}", "hypothesis_id": "H1", "axis_id": "A1", "type": "REQUIRED_SUPPORT",
              "text": f"premise {i}", "active": True} for i in (1, 2, 3)] + [
        {"unit_id": "H1-A1", "hypothesis_id": "H1", "axis_id": "A1", "type": "ADVERSE_TEST",
         "text": "adverse", "active": True}]

    def rel(self):
        return {("W1", "H1-R1"): _rel("WITNESS_ENTAILS_UNIT"),
                ("W9", "H1-R1"): _rel("CONTRADICTS"),
                ("W2", "H1-R2"): _rel("PARTIALLY_COVERS", gap_type="SCOPE", gap="the rat result transfers to men"),
                ("W3", "H1-R2"): _rel("PARTIALLY_COVERS", gap_type="ELEMENT", gap="one link only"),
                ("W4", "H1-R3"): _rel("EQUIVALENT"),
                ("W5", "H1-R3"): _rel("PARTIALLY_COVERS", gap_type="SCOPE", gap="not needed")}

    def test_strict_tier_is_unchanged_and_incomplete(self):
        pb, _ = build_problem("H1", self.UNITS, self.rel(), [], [])
        res = solve(pb)
        self.assertEqual(res["status"], "NO_COMPLETE_COVERAGE")
        self.assertEqual(res["uncovered_units"], ["H1-R2"])

    def test_scope_gap_covers_conditionally_and_names_its_assumption(self):
        pb, _ = build_problem("H1", self.UNITS, self.rel(), [], [], assume_gaps=("SCOPE",))
        # only the unit with no complete option gets conditional options, and only SCOPE gaps qualify
        self.assertEqual([o.witnesses for o in pb.options["H1-R2"]], [("W2",)])
        self.assertTrue(pb.options["H1-R2"][0].assumption.startswith("the rat result"))
        self.assertEqual([o.witnesses for o in pb.options["H1-R3"]], [("W4",)])
        res = solve(pb)
        self.assertEqual([s["witnesses"] for s in res["sets"]], [["W1", "W2", "W4"]])
        from claimreg.coverage import _set_assumptions
        self.assertEqual(_set_assumptions(pb, {"W1", "W2", "W4"}),
                         [{"unit_id": "H1-R2", "witness_id": "W2", "assumption": "the rat result transfers to men"}])

    def test_ledger_statuses(self):
        led = build_ledger(self.UNITS, self.rel(), [], {"H1": {"status": "COMPLETE_WITH_ASSUMPTIONS"}})
        st = {r["unit_id"]: r["status"] for r in led["hypotheses"]["H1"]}
        self.assertEqual(st, {"H1-R1": "CONTESTED", "H1-R2": "SUPPORTED_WITH_ASSUMPTION",
                              "H1-R3": "ESTABLISHED", "H1-A1": "UNADDRESSED"})
        self.assertEqual(led["summary"]["H1"]["required"]["CONTESTED"], 1)


class RoutedMatchingPipelineTest(unittest.TestCase):
    """The whole pipeline with scripted API matchers: routing chooses the pairs, both passes return a
    SCOPE gap, and coverage forms with named assumptions."""

    def setUp(self):
        self.tmp = scratch_dir("premises-pipe")
        fakes.reset()

    def tearDown(self):
        cleanup(self.tmp)

    def test_scope_gaps_form_assumption_labelled_sets(self):
        seen = {"route": 0}

        def script(req, prov):
            wids = re.findall(r"^\[(W-[^\]]+)\]", req.user, re.M)
            if req.role == "match_router":
                seen["route"] += 1
                units = re.findall(r"^\[([^\]]+)\] \((?:REQUIRED_SUPPORT|CONTEXTUAL_CONSTRAINT)", req.user, re.M)
                return {"routes": [{"witness_id": w, "unit_ids": units} for w in wids]}
            if req.role in ("matcher_a", "matcher_b"):
                return {"judgments": [{"witness_id": w, "relation": "PARTIALLY_COVERS", "trace": "same effect, "
                                       "other model", "gap_type": "SCOPE", "gap": "the model result transfers"}
                                      for w in wids]}
            return {"decisions": [], "groups": [], "approve": False}
        fakes.SCRIPTS["s"] = script
        proj = make_project(self.tmp, extra={
            "roles": {r: "scripted" for r in ("matcher_a", "matcher_b", "match_adjudicator", "joint_checker")},
            "providers": {"scripted": SCRIPTED},
            "matching": {"exhaustive_threshold": 0, "qualify": False, "shortlist_k": 2, "shortlist_k_secondary": 2},
            "crux": {"completion_matching": False}})
        ctx = RunContext(proj, "RUN-P", create=True, quiet=True)
        out = run_pipeline(ctx)
        self.assertEqual(out["status"], "complete", out)
        self.assertGreater(seen["route"], 0)
        summ = ctx.load("matching", "03_match-records/summary.json")
        self.assertGreater(summ["routing"]["routed_pairs"], 0)
        self.assertGreater(summ["partial_scope_gap"], 0)
        rel = ctx.load("matching", "03_match-records/relations.json")
        self.assertTrue(all(r["gap_type"] == "SCOPE" for r in rel if r["final"] == "PARTIALLY_COVERS"))
        cov = ctx.load("coverage", "coverage.json")["hypotheses"]
        done = [c for c in cov.values() if c["status"] == "COMPLETE_WITH_ASSUMPTIONS"]
        self.assertTrue(done, {h: c["status"] for h, c in cov.items()})
        self.assertTrue(all(s["assumptions"] for c in done for s in c["sets"]))
        self.assertFalse(any(c["status"] == "COMPLETE" for c in cov.values()))
        led = ctx.load("coverage", "premise-ledger.json")
        self.assertTrue(any(r["status"] == "SUPPORTED_WITH_ASSUMPTION"
                            for rows in led["hypotheses"].values() for r in rows))
        self.assertTrue(ctx.p("coverage", "PREMISE-LEDGER.md").exists())
        report = ctx.p("reports", "CRUX-REPORT.md").read_text(encoding="utf-8")
        self.assertIn("What each hypothesis rests on", report)
        self.assertIn("supported if a transfer is granted", report)
        from claimreg.funnel import funnel
        self.assertEqual(funnel(ctx)["stages"][0][0], "usable answers")

    def test_turning_the_tier_off_restores_strict_coverage_only(self):
        def script(req, prov):
            wids = re.findall(r"^\[(W-[^\]]+)\]", req.user, re.M)
            if req.role in ("matcher_a", "matcher_b"):
                return {"judgments": [{"witness_id": w, "relation": "PARTIALLY_COVERS", "trace": "x",
                                       "gap_type": "SCOPE", "gap": "transfers"} for w in wids]}
            return {"routes": [], "decisions": [], "groups": [], "approve": False}
        fakes.SCRIPTS["s"] = script
        proj = make_project(self.tmp, extra={
            "roles": {r: "scripted" for r in ("matcher_a", "matcher_b", "match_adjudicator", "joint_checker")},
            "providers": {"scripted": SCRIPTED}, "coverage": {"assume_gaps": []},
            "matching": {"qualify": False}, "crux": {"completion_matching": False}})
        ctx = RunContext(proj, "RUN-S", create=True, quiet=True)
        self.assertEqual(run_pipeline(ctx)["status"], "complete")
        cov = ctx.load("coverage", "coverage.json")["hypotheses"]
        self.assertTrue(all(c["status"] in ("NO_COMPLETE_COVERAGE", "NO_REQUIRED_UNITS") for c in cov.values()))


if __name__ == "__main__":
    unittest.main()
