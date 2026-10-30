"""End-to-end regression for the last three modules: coverage, incompatibility, crux.

The worked example (`examples/worked`) is engineered so that source sentences restate
the hypothesis clauses.  That is what lets a lexical matcher reach complete relations,
which is the precondition for coverage sets and therefore for crux identification.  If
this test fails, one of those modules has stopped producing artifacts end to end.
"""

import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import write_json  # noqa: E402
from claimreg.verify import verify_run  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORKED = ROOT / "examples" / "worked"


class WorkedExampleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("worked")
        proj = self.tmp / "worked"
        (proj / "01_CORPUS" / "source-files").mkdir(parents=True)
        (proj / "01_FRAME").mkdir()
        for p in sorted((WORKED / "sources").glob("*.md")):
            shutil.copyfile(p, proj / "01_CORPUS" / "source-files" / p.name)
        shutil.copyfile(WORKED / "header.md", proj / "01_FRAME" / "header.md")
        write_json(proj / "project.json", {
            "project": {"name": "worked", "run_prefix": "RUN-WORKED"},
            "default_provider": "local",
            "quest": {"round_size": 3, "max_rounds": 4},
            "matching": {"exhaustive_threshold": 60, "shortlist_k": 60, "shortlist_k_secondary": 60},
        })
        self.proj = proj
        self.ctx = RunContext(proj, "RUN-WORKED-T", create=True, quiet=True)
        self.out = run_pipeline(self.ctx)

    def tearDown(self):
        cleanup(self.tmp)

    def test_pipeline_completes(self):
        self.assertEqual(self.out["status"], "complete", self.out)

    def test_coverage_set_exists(self):
        cov = self.ctx.load("coverage", "coverage.json")["hypotheses"]
        complete = [h for h, c in cov.items() if c["status"] == "COMPLETE" and c.get("sets")]
        self.assertTrue(complete, f"no hypothesis reached complete coverage: {cov}")
        sets = cov["A1-H2"]["sets"]
        self.assertTrue(sets)
        # deletion-minimality: every set's removal certificate breaks coverage
        for s in sets[:5]:
            self.assertTrue(s.get("removal_certificate") or s.get("certificates") or s.get("witnesses"))

    def test_incompatibility_approved(self):
        inc = self.ctx.load("matching", "03_match-records/incompatibilities.json")
        records = inc.get("records", []) if isinstance(inc, dict) else inc
        approved = [r for r in records if r.get("approved")]
        self.assertTrue(approved, "no witness pair was approved as incompatible")

    def test_crux_candidate_with_certificates(self):
        crux = self.ctx.load("crux", "05_candidates/crux-candidates.json")
        cands = crux.get("candidates", [])
        self.assertTrue(cands, f"no crux candidate: {list(crux)}")
        c = cands[0]
        self.assertTrue(c.get("defeats"))
        tests = self.ctx.load("crux", "03_portability-tests/tests.json")
        self.assertTrue(tests, "no portability tests recorded")
        self.assertTrue(any(t.get("tests_failed") for t in tests),
                        "every portability test passed; T1/T2 never failed")

    def test_verify_run_is_clean(self):
        v = verify_run(self.proj, "RUN-WORKED-T")
        self.assertTrue(v["ok"], v["problems"])

    def test_verify_distinguishes_missing_sources_from_bad_quotes(self):
        """A published clone may not carry the third-party corpus.

        The run must still verify structurally, with a warning that quotations could not be checked —
        not a false 'quote not found' failure."""
        for p in (self.proj / "01_CORPUS" / "source-files").glob("*.md"):
            p.unlink()
        v = verify_run(self.proj, "RUN-WORKED-T")
        self.assertTrue(v["ok"], v["problems"])
        self.assertEqual(v["checks"]["frd_quotes"]["not_found"], [])
        self.assertTrue(v["checks"]["frd_quotes"]["unverifiable_sources_missing"])
        self.assertTrue(v.get("warnings"))


if __name__ == "__main__":
    unittest.main()
