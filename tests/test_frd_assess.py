"""The preliminary evaluation of the validated FRDs, and the researcher's stop after it."""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from scratch import cleanup, scratch_dir  # noqa: E402
from test_axes import by_parity, two_axis_project  # noqa: E402
from claimreg import axes, frd_assess as fa  # noqa: E402
from claimreg.pipeline import STAGE_NAMES, run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import read_json  # noqa: E402
from claimreg.verify import verify_run  # noqa: E402

GATE = {"pipeline": {"stop_after": "frd_assess"}}


def project(tmp, **extra):
    return two_axis_project(tmp, extra={**GATE, **extra})


def frd(i, words=10):
    return {"vfrd_id": f"FRD-Q{i:04d}-01", "source_file": "s.md", "verdict": "RIGHT", "claim": "w " * words}


class ArithmeticTest(unittest.TestCase):
    def test_partitions_do_not_depend_on_the_order_the_frds_arrive_in(self):
        fs = [frd(i) for i in range(1, 30)]
        a = fa.partition(fs, 60)
        b = fa.partition(list(reversed(fs)), 60)
        self.assertEqual([[fa.frd_id(f) for f in p] for p in a], [[fa.frd_id(f) for f in p] for p in b])
        self.assertGreater(len(a), 1)
        self.assertEqual(sum(len(p) for p in a), 29)
        self.assertEqual(len(fa.partition(fs, 10 ** 6)), 1)

    def test_rounding_always_sums_to_the_gauge(self):
        for w in ({"H1": 1, "H2": 1, "H3": 1}, {"H1": 0, "H2": 0, "H3": 0}, {"H1": 5, "H2": 0.1, "H3": 2.2}):
            v = fa.largest_remainder(w, 64)
            self.assertEqual(sum(v.values()), 64)
            self.assertTrue(all(x >= 0 for x in v.values()))
        self.assertEqual(fa.largest_remainder({"H1": 1, "H2": 1, "H3": 1}, 64), {"H1": 22, "H2": 21, "H3": 21})

    def test_mechanical_mean_weights_partitions_by_their_frd_count(self):
        v = fa.mechanical_mean([{"H1": 64, "H2": 0}, {"H1": 0, "H2": 64}], [30, 10], ["H1", "H2"], 64)
        self.assertEqual(v, {"H1": 48, "H2": 16})
        same = fa.mechanical_mean([{"H1": 40, "H2": 24}] * 3, [5, 9, 2], ["H1", "H2"], 64)
        self.assertEqual(same, {"H1": 40, "H2": 24})          # identical partitions: cutting changes nothing

    def test_the_combined_set_must_be_a_disjoint_union(self):
        rows = fa.combined_rows({"A1": [frd(1), frd(2)], "A2": [frd(3)]})
        self.assertEqual([r["home_axis"] for r in rows], ["A1", "A1", "A2"])
        with self.assertRaises(ValueError):
            fa.combined_rows({"A1": [frd(1)], "A2": [frd(1)]})


class FrdAssessPipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("frd-assess")

    def tearDown(self):
        cleanup(self.tmp)

    def run_it(self, ctx, **kw):
        with mock.patch.object(axes, "assign_axes", by_parity):
            return run_pipeline(ctx, **kw)

    def test_the_run_halts_after_the_evaluation_and_continues_only_when_released(self):
        proj = project(self.tmp)
        ctx = RunContext(proj, "RUN-G", create=True, quiet=True)
        out = self.run_it(ctx)
        self.assertEqual(out["status"], "halted", out)
        self.assertEqual(out["ran"][-1], "frd_assess")
        self.assertIn("--continue", out["continue_with"])
        state = ctx.stage_state()
        self.assertEqual(state["frd_assess"]["status"], "done")
        for later in STAGE_NAMES[STAGE_NAMES.index("frd_assess") + 1:]:
            self.assertNotIn(state.get(later, {}).get("status"), ("done", "running"), later)
        status = (ctx.run_dir / "RUN-STATUS.md").read_text(encoding="utf-8")
        self.assertIn("Halted for researcher decision", status)
        self.assertTrue((ctx.run_dir / "RUN-MAP.md").exists())
        v = verify_run(proj, "RUN-G")                      # a halted run is still a coherent record
        self.assertFalse([p for p in v["problems"] if "axis" in p.lower() or "frd" in p.lower()], v["problems"])

        again = self.run_it(RunContext(proj, "RUN-G", quiet=True))       # a plain resume halts again, redoing nothing
        self.assertEqual((again["status"], again["ran"]), ("halted", []))

        done = self.run_it(RunContext(proj, "RUN-G", quiet=True), release=True)
        self.assertEqual(done["status"], "complete", done)
        self.assertEqual(done["ran"][0], "language")
        self.assertNotIn("frd_assess", done["ran"])
        self.assertTrue((ctx.run_dir / "00_RUN-CONTROL" / "model-and-human-decisions" /
                         "released-after-frd_assess.json").exists())
        self.assertNotIn("Halted", (ctx.run_dir / "RUN-STATUS.md").read_text(encoding="utf-8"))

    def test_each_axis_gets_an_axis_only_and_a_combined_vector_with_attribution(self):
        proj = project(self.tmp)
        ctx = RunContext(proj, "RUN-E", create=True, quiet=True)
        self.run_it(ctx)
        rec = read_json(ctx.run_dir / "frd-evaluation.json")
        counts = rec["frd_counts"]
        self.assertEqual(counts["combined"], counts["A1"] + counts["A2"])
        self.assertTrue(rec["combined_is_disjoint_union"])
        combined = read_json(ctx.run_dir / "SHARED" / "03_FRDS-COMBINED" / "combined-validated-frds.json")
        self.assertEqual(len({fa.frd_id(r) for r in combined}), counts["combined"])
        home = {fa.frd_id(r): r["home_axis"] for r in combined}
        for a in ("A1", "A2"):
            t = rec["table"][a]
            for key in ("axis_only", "combined", "equal_weight_for_comparison_only"):
                self.assertEqual(sum(t[key].values()), rec["gauge"], (a, key))
                self.assertTrue(all(h.startswith(a + "-") for h in t[key]))
            own, comb = rec["results"][a]["axis-only"], rec["results"][a]["combined"]
            self.assertTrue(own["drivers"])
            self.assertTrue(all(d["home_axis"] == a and d["source_file"] for d in own["drivers"]))
            self.assertTrue(comb["other_axis_drivers"])                       # which other-axis FRDs were material
            self.assertTrue(all(home[d["frd_id"]] != a for d in comb["other_axis_drivers"]))
            sc = ctx.for_axis(a)
            self.assertEqual(read_json(sc.p("frds", "06_evaluation/evaluation.json"))["allocations"], t["axis_only"])
            other = "A2" if a == "A1" else "A1"                               # the axis folder stays single-axis
            for f in sc.p("frds", "06_evaluation").iterdir():
                self.assertNotIn(f"{other}-H", f.read_text(encoding="utf-8"), f)
        page = (ctx.run_dir / "FRD-EVALUATION.md").read_text(encoding="utf-8")
        for needle in ("Preliminary", "not a probability", "comparison only", "--continue", "Measured"):
            self.assertIn(needle, page)
        self.assertFalse(rec["provisional"])                 # every question in this run named its axis when asked

    def test_axis_filing_done_after_the_fact_is_printed_as_provisional(self):
        proj = project(self.tmp)
        ctx = RunContext(proj, "RUN-P", create=True, quiet=True)
        self.run_it(ctx, stop="frd_retain")
        sc = ctx.for_axis("A1")
        qs = sc.load("discovery", "01_issued-questions/questions.json")
        for q in qs[:3]:
            q["axis_source"] = "assigned-after-the-fact (model)"
        sc.save("discovery", "01_issued-questions/questions.json", qs, "test")
        self.run_it(RunContext(proj, "RUN-P", quiet=True))
        rec = read_json(ctx.run_dir / "frd-evaluation.json")
        self.assertTrue(rec["provisional"])
        self.assertEqual(rec["axis_filing"]["A1"]["assigned_after_the_fact"], 3)
        self.assertIn("PROVISIONAL", (ctx.run_dir / "FRD-EVALUATION.md").read_text(encoding="utf-8"))

    def test_a_large_set_is_partitioned_and_the_partitioning_is_recorded(self):
        proj = project(self.tmp, frd_assess={"partition_words": 60})
        ctx = RunContext(proj, "RUN-S", create=True, quiet=True)
        self.run_it(ctx)
        rec = read_json(ctx.run_dir / "frd-evaluation.json")
        self.assertFalse(rec["problems"], rec["problems"])
        s = rec["results"]["A1"]["combined"]
        self.assertGreater(s["partition_count"], 1)
        self.assertEqual(sum(p["frd_count"] for p in s["partitions"]), s["frd_count"])
        self.assertEqual(sum(s["mechanical_mean_of_partitions"].values()), rec["gauge"])
        self.assertEqual(s["result_vs_mechanical_mean_units"], 0)   # the mock gives every partition the same vector
        self.assertEqual(s["calls"][-1]["partition"], "synthesis")
        d = ctx.run_dir / "SHARED" / "03_FRDS-COMBINED" / "for-A1"
        self.assertEqual(len(list(d.glob("partition-*.md"))), s["partition_count"])
        self.assertTrue((d / "evaluation.md").exists())

    def test_each_axis_database_file_matches_its_json_records(self):
        proj = project(self.tmp)
        ctx = RunContext(proj, "RUN-D", create=True, quiet=True)
        self.run_it(ctx)
        for sc in ctx.scopes():
            db = fa.axis_db_counts(Path(sc.root) / "axis.db")
            for table, (rel, _) in fa.DB_TABLES.items():
                self.assertEqual(db[table], len(fa._rows(sc, rel)), (sc.axis_id, table))
            self.assertGreater(db["questions"], 0)
            self.assertGreater(db["retained_frds"], 0)
            import sqlite3
            con = sqlite3.connect(Path(sc.root) / "axis.db")
            try:
                self.assertEqual({r[0] for r in con.execute("SELECT DISTINCT axis FROM questions")}, {sc.axis_id})
                self.assertTrue(con.execute("SELECT axis_source FROM questions LIMIT 1").fetchone()[0])
            finally:
                con.close()

    def test_frds_from_synthesis_files_and_duplicate_copies_are_left_out(self):
        proj = project(self.tmp)
        ctx = RunContext(proj, "RUN-C", create=True, quiet=True)
        self.run_it(ctx, stop="frd_retain")
        rows = fa._rows(ctx.for_axis("A1"), fa.REL_RETAINED)
        files = sorted({r["source_file"] for r in rows})
        self.assertGreater(len(files), 1)
        ctx2 = RunContext(proj, "RUN-C", quiet=True)
        ctx2.cfg["corpus"]["synthesis_sources"] = [files[0]]
        ctx2.cfg["frd_assess"]["axis_only"] = ["A2"]
        self.run_it(ctx2)
        rec = read_json(ctx.run_dir / "frd-evaluation.json")
        gone = [fa.frd_id(r) for r in rows if r["source_file"] == files[0]]
        self.assertEqual(sorted(rec["excluded_frd_ids"]["A1"]["synthesis"]), sorted(gone))
        self.assertEqual(rec["frd_counts"]["A1"], len(rows) - len(gone))
        self.assertTrue(all(d["source_file"] != files[0] for d in rec["results"]["A1"]["axis-only"]["drivers"]))
        self.assertIn("not citable", (ctx.run_dir / "FRD-EVALUATION.md").read_text(encoding="utf-8"))
        self.assertNotIn("combined", rec["results"]["A2"])           # axis_only: no other axis's FRDs reach A2
        self.assertIn("combined", rec["results"]["A1"])

    def test_a_single_database_run_gets_the_whole_set_reading_only(self):
        proj = project(self.tmp, axes={"separate_databases": False})
        ctx = RunContext(proj, "RUN-O", create=True, quiet=True)
        out = run_pipeline(ctx)
        self.assertEqual(out["status"], "halted", out)
        rec = read_json(ctx.run_dir / "frd-evaluation.json")
        self.assertIsNone(rec["table"]["A1"]["axis_only"])
        self.assertEqual(sum(rec["table"]["A1"]["combined"].values()), rec["gauge"])


if __name__ == "__main__":
    unittest.main()
