"""The LEVO domain module: used only when a project names it, and never by other research."""
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from scratch import cleanup, scratch_dir  # noqa: E402
from test_axes import by_parity, two_axis_project  # noqa: E402
from claimreg import axes, domains  # noqa: E402
from claimreg.domains.levo import bedtime_gate  # noqa: E402
from claimreg.llm.mock import MockProvider  # noqa: E402
from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import read_json  # noqa: E402

LEVO = {"domain_modules": {"levo": {"bedtime_axis": "A2"}}}


class GateTest(unittest.TestCase):
    def test_the_gate_accepts_and_rejects_its_reference_cases(self):
        r = bedtime_gate.self_test()
        self.assertEqual((r["tests"], r["passed"]), (17, 17))

    def test_the_gate_does_not_care_which_hypothesis_leads(self):
        fx = json.loads((Path(bedtime_gate.HERE) / "gate_examples.json").read_text(encoding="utf-8"))
        for vec in ({"A2-H1": 60, "A2-H2": 2, "A2-H3": 2}, {"A2-H1": 2, "A2-H2": 60, "A2-H3": 2},
                    {"A2-H1": 2, "A2-H2": 2, "A2-H3": 60}):
            self.assertEqual(bedtime_gate.check(bedtime_gate.merge(fx["base_report"], {"allocations": vec})), [])

    def test_an_uncatalogued_source_may_be_indirect_but_not_a_direct_test(self):
        fx = json.loads((Path(bedtime_gate.HERE) / "gate_examples.json").read_text(encoding="utf-8"))
        ok = {"drivers": [{"source_id": "campbell_1992_iron", "direction": "favors_bedtime", "inference_type": "indirect",
                           "transfer_justification": "co-ingested iron raised TSH into the target band; bedtime removes it"}]}
        bad = {"drivers": [{"source_id": "campbell_1992_iron", "direction": "favors_bedtime",
                            "inference_type": "direct_target_estimate"}]}
        self.assertEqual(bedtime_gate.check(bedtime_gate.merge(fx["base_report"], ok)), [])
        self.assertEqual({e["rule"] for e in bedtime_gate.check(bedtime_gate.merge(fx["base_report"], bad))}, {"R4"})


class IsolationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("domain-levo")
        self.seen = []
        real = MockProvider._frd_assessor

        def spy(provider, req):
            self.seen.append((req.meta["axis"]["axis_id"], req.system))
            return real(provider, req)
        self.patches = [mock.patch.object(MockProvider, "_frd_assessor", spy),
                        mock.patch.object(axes, "assign_axes", by_parity)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        cleanup(self.tmp)

    def test_a_project_that_does_not_name_the_module_never_sees_it(self):
        self.assertEqual(domains.active({}), [])
        proj = two_axis_project(self.tmp)
        ctx = RunContext(proj, "RUN-N", create=True, quiet=True)
        run_pipeline(ctx, stop="frd_assess")
        self.assertTrue(self.seen)
        for _, system in self.seen:
            self.assertNotIn("bedtime", system.lower())
            self.assertNotIn("GATE REPORT", system)
        rec = read_json(ctx.run_dir / "frd-evaluation.json")
        self.assertIsNone(rec["results"]["A2"]["axis-only"]["gate"])
        self.assertTrue(rec["table"]["A2"]["axis_only"])

    def test_the_named_axis_gets_the_rules_and_a_report_without_a_gate_report_is_withheld(self):
        proj = two_axis_project(self.tmp, extra=LEVO)
        ctx = RunContext(proj, "RUN-L", create=True, quiet=True)
        run_pipeline(ctx, stop="frd_assess")
        by_axis = {}
        for aid, system in self.seen:
            by_axis.setdefault(aid, []).append(system)
        self.assertTrue(all("R4 Record the actual tested schedules" in s and "GATE REPORT" in s for s in by_axis["A2"]))
        self.assertTrue(all("bedtime" not in s.lower() for s in by_axis["A1"]))      # the other axis is untouched
        rec = read_json(ctx.run_dir / "frd-evaluation.json")
        a2 = rec["results"]["A2"]["axis-only"]
        self.assertFalse(a2["gate"]["accepted"])                 # the mock assessor declares nothing
        self.assertIsNone(a2["allocations"])                     # withheld, and not turned into H3
        self.assertEqual(sum(a2["allocation_withheld_pending_correction"].values()), rec["gauge"])
        self.assertTrue(any("returned for correction" in p for p in rec["problems"]))
        self.assertTrue(rec["table"]["A1"]["axis_only"])         # the other axis is scored as usual

    def test_corrections_are_capped_and_every_rejected_evaluation_is_kept(self):
        proj = two_axis_project(self.tmp, extra=LEVO)
        ctx = RunContext(proj, "RUN-K", create=True, quiet=True)
        run_pipeline(ctx, stop="frd_assess")
        for _ in range(4):
            run_pipeline(RunContext(proj, "RUN-K", quiet=True), only=["frd_assess"], force=["frd_assess"])
        d = ctx.for_axis("A2").p("frds", "06_evaluation")
        kept = (d / "evaluation-history.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(kept), 2)                         # first report + 2 corrections, then it stops asking
        self.assertTrue((d / "evaluation-attempt-01.md").exists())
        rec = read_json(ctx.run_dir / "frd-evaluation.json")
        self.assertTrue(any("no further automatic correction" in p for p in rec["problems"]))

    def test_the_gate_checks_the_declaration_against_what_the_harness_knows(self):
        from claimreg.domains import levo
        fx = json.loads((Path(bedtime_gate.HERE) / "gate_examples.json").read_text(encoding="utf-8"))
        axis, opt = {"axis_id": "A2"}, {"bedtime_axis": "A2"}
        report = bedtime_gate.merge(fx["base_report"], {"frame": {"target_population": "broad_adults"}, "drivers": [
            {"source_id": "bolk_2010", "frd_id": "FRD-1", "direction": "favors_bedtime", "inference_type": "direct_target_estimate"}]})
        facts = {"drivers": [{"frd_id": "FRD-1", "favors": "A2-H1", "source_file": "bolk2010.pdf.md", "is_synthesis": False},
                             {"frd_id": "FRD-2", "favors": "A2-H2", "source_file": "ai-summary.md", "is_synthesis": True}],
                 "synthesis_sources": ["ai-summary.md"], "duplicates": {}}
        rules = {e["rule"] for e in levo.gate(axis, report, opt, facts)}
        self.assertIn("R9", rules)        # the assessor cannot widen the target population to dodge the boundary check
        self.assertIn("R16", rules)       # a driver from a synthesis file
        self.assertIn("R17", rules)       # an allocation driver left out of the declaration
        self.assertEqual(levo.gate({"axis_id": "A1"}, None, opt, facts), [])

    def test_a_rerun_tells_the_assessor_what_the_gate_found(self):
        proj = two_axis_project(self.tmp, extra=LEVO)
        ctx = RunContext(proj, "RUN-R", create=True, quiet=True)
        run_pipeline(ctx, stop="frd_assess")
        self.seen.clear()
        run_pipeline(RunContext(proj, "RUN-R", quiet=True), only=["frd_assess"], force=["frd_assess"])
        self.assertTrue(any("RETURNED FOR CORRECTION" in s for aid, s in self.seen if aid == "A2"))


if __name__ == "__main__":
    unittest.main()
