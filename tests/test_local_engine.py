"""Tests for the local (offline, deterministic) analyst.

The fixture set is the same adversarial set the matching stage qualifies against
(``claimreg.matching.FIXTURES``), so a failure here is a real qualification
failure, not a test-only artifact.
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.llm.base import LLMRequest  # noqa: E402
from claimreg.llm.local import LocalProvider, _judge  # noqa: E402
from claimreg.matching import FIXTURES  # noqa: E402
from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import write_json  # noqa: E402

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures" / "mini"

from scratch import cleanup, scratch_dir  # noqa: E402


def scratch(tag: str = "local") -> Path:
    return scratch_dir(tag)


class LocalFixtureTest(unittest.TestCase):
    def setUp(self):
        self.prov = LocalProvider("local", {"model": "local-rules-v1"}, HERE.parent)

    def _ask(self, role, unit, witness):
        req = LLMRequest(role=role, system="", user="",
                         meta={"unit": {"unit_id": "U", "type": "REQUIRED_SUPPORT"},
                               "unit_text": unit, "witnesses": {"W": witness}})
        return json.loads(self.prov.complete(req, "k").text)["judgments"][0]["relation"]

    def test_every_adversarial_fixture_in_both_passes(self):
        bad = []
        for fid, pattern, unit, witness, accept in FIXTURES:
            a = self._ask("matcher_a", unit, witness)
            b = self._ask("matcher_b", unit, witness)
            if a not in accept:
                bad.append((fid, pattern, "A", a, sorted(accept)))
            if b not in accept:
                bad.append((fid, pattern, "B", b, sorted(accept)))
        self.assertEqual(bad, [], f"unqualified fixtures: {bad}")

    def test_polarity_and_quantity_conflicts_are_caught(self):
        rel, trace = _judge("Drug A increased flow by 4.5 mL/s.",
                            "Drug A produced no increase in flow.")
        self.assertEqual(rel, "CONTRADICTS", trace)
        rel, trace = _judge("Flow rose by 4.5 mL/s in the drug arm.",
                            "Flow rose by 1.2 mL/s in the drug arm.")
        self.assertEqual(rel, "CONTRADICTS", trace)

    def test_scope_mismatch_is_not_a_complete_match(self):
        rel, trace = _judge("Drug A improves voiding in men with BPH.",
                            "Drug A improved detrusor contractility in obstructed rats.")
        self.assertIn(rel, ("PARTIALLY_COVERS", "NO_SEMANTIC_RELATION"), trace)


class LocalPipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch("local-pipe")

    def tearDown(self):
        cleanup(self.tmp)

    def test_full_pipeline_offline(self):
        proj = self.tmp / "mini"
        (proj / "01_CORPUS").mkdir(parents=True)
        shutil.copytree(FIX / "sources", proj / "01_CORPUS" / "source-files")
        (proj / "01_FRAME").mkdir()
        shutil.copyfile(FIX / "header.md", proj / "01_FRAME" / "header.md")
        shutil.copyfile(FIX / "index.md", proj / "01_FRAME" / "index.md")
        shutil.copyfile(FIX / "archivist.txt", proj / "01_FRAME" / "archivist-custom-prompt.txt")
        write_json(proj / "project.json", {"project": {"name": "mini-local"},
                                           "quest": {"round_size": 3, "max_rounds": 6}})
        ctx = RunContext(proj, "RUN-LOCAL", create=True, quiet=True)
        out = run_pipeline(ctx)
        self.assertEqual(out["status"], "complete", out)
        st = ctx.stage_state()
        for name in ("units", "quest", "frd_generate", "frd_validate", "frd_retain",
                     "witnesses", "qualify", "match", "joint", "coverage", "crux",
                     "assess", "report"):
            self.assertEqual(st[name]["status"], "done", (name, st[name]))
        q = ctx.load("matching", "02_match-fixtures/qualification.json")
        self.assertEqual(q["pass_a_correct"], q["fixtures"], q["rows"])
        self.assertEqual(q["pass_b_correct"], q["fixtures"], q["rows"])
        ws = ctx.load("witnesses", "05_released/witnesses.json")
        self.assertTrue(ws, "the local engine released no witnesses")
        self.assertTrue(all(w["words"] <= w["ceiling"] for w in ws))
        self.assertTrue((ctx.p("reports", "report.html")).exists())
        # a rerun with the same inputs must not ask anything again
        from claimreg.util import read_jsonl
        log = ctx.p("control", "model-and-human-decisions", "llm-calls.jsonl")
        before = sum(1 for c in read_jsonl(log) if c.get("status") == "ok")
        out2 = run_pipeline(RunContext(proj, "RUN-LOCAL", quiet=True), force=["report"])
        self.assertEqual(out2["status"], "complete")
        after = sum(1 for c in read_jsonl(log) if c.get("status") == "ok")
        self.assertEqual(before, after, "a rerun asked the local engine again")


if __name__ == "__main__":
    unittest.main()
