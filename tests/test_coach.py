"""The coach between rounds: score the evidence after the quest and after validation, and when the
researcher's hypothesis is short of its target, stop and show them the next move."""

import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg import coach  # noqa: E402
from claimreg.cli import main  # noqa: E402
from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import read_json, write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402
from test_frame_gate import FakeModel  # noqa: E402
from test_pipeline_mock import make_project  # noqa: E402

IDS = ["A1-H1", "A1-H2", "A1-H3"]


def scorer(*h1_values):
    """A stand-in for the scoring calls: each scoring gives A1-H1 the next value."""
    seen = []

    def fake(ctx, axis, rows, out_dir, times, evidence, label):
        seen.append({"axis": axis["axis_id"], "rows": len(rows), "times": times, "evidence": evidence,
                     "claim": axis["hypotheses"][0]["statement"]})
        vals = [h1_values[min(len(seen) - 1 + k, len(h1_values) - 1)] for k in range(times)]
        recs = [{"allocations": {"A1-H1": v, "A1-H2": 54 - v, "A1-H3": 10}, "strongest_objection": "small trials",
                 "reversal_finding": "a large null trial",
                 "drivers": [{"frd_id": "X1", "favors": "A1-H2", "why": "no change in flow", "source_file": "smith2020.md"}]}
                for v in vals]
        return coach.summarize(recs, IDS, 64, rows=len(rows))
    fake.seen = seen
    return fake


class CoachTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("coach")
        self.proj = make_project(self.tmp, extra={"coach": {"preferred": {"A1": "A1-H1"}}})
        self.model = FakeModel()

    def tearDown(self):
        cleanup(self.tmp)

    def run_it(self, fake, **kw):
        ctx = RunContext(self.proj, "RUN-C", create=True, quiet=True)
        with mock.patch.object(coach, "score", fake), mock.patch.object(coach, "_ask", lambda ctx: self.model):
            return ctx, run_pipeline(ctx, **kw)

    def test_without_a_preferred_hypothesis_the_coach_stays_out_of_the_way(self):
        cfg = read_json(self.proj / "project.json")
        cfg["coach"] = {}
        write_json(self.proj / "project.json", cfg)
        ctx, out = self.run_it(scorer(10), stop="frd_assess")
        self.assertEqual(out["status"], "complete", out)
        self.assertFalse((ctx.run_dir / "COACH-CHECKPOINT-1.md").exists())
        self.assertFalse((ctx.run_dir / "COACH-CHECKPOINT-2.md").exists())

    def test_below_target_after_the_quest_the_run_stops_and_the_coach_talks(self):
        fake = scorer(30)
        ctx, out = self.run_it(fake)
        self.assertEqual(out["status"], "halted", out)
        self.assertEqual((out["gate"], out["read"], out["next_stage"]), ("the quest", "COACH-CHECKPOINT-1.md", "frd_generate"))
        self.assertNotEqual(ctx.stage_state().get("frd_generate", {}).get("status"), "done")   # nothing was spent on FRDs
        self.assertEqual((fake.seen[0]["evidence"], fake.seen[0]["times"]), ("answers", 1))    # the quest's answers, scored once
        self.assertGreater(fake.seen[0]["rows"], 0)

        talk = (ctx.run_dir / "COACH-CHECKPOINT-1.md").read_text(encoding="utf-8")
        for needle in ("**A1-H1: 30 of 64** (target 43). Standing: **below target**.",
                       "This early reading is provisional",
                       "### Why it came in low", "No trial enrolled men like the ones you describe.",
                       "### What the evidence did not cover", "### What the evidence does show for you",
                       "Two trials show a rise in flow rate.",
                       "### Your own experience", "### Openings: claims this evidence is more likely to support",
                       "**1. offer it**", "The rival is held by: urologists who follow the current guideline",
                       "### Questions to put to the corpus next", "Ask smith2020 for results in men over 70.",
                       "## Your next move", "**Take an opening.**", "--answers", "**Ask more.**", "**Go on as you are.**",
                       "A result below target is still a result"):
            self.assertIn(needle, talk)
        self.assertNotIn("beats a strawman", talk)                         # a rival nobody holds is never offered
        self.assertNotIn("give up", talk.lower())
        # the coach was told what the assessment said and which questions were already asked
        self.assertIn("driver X1 (smith2020.md) favours A1-H2", self.model.corner_prompt)
        self.assertIn("QUESTIONS ALREADY PUT TO THE CORPUS", self.model.corner_prompt)

        ladder = (self.proj / "01_FRAME" / coach.LADDER_MD).read_text(encoding="utf-8")
        self.assertIn("| RUN-C | the quest's answers (not yet validated) |", ladder)
        self.assertIn("**30** of 64", ladder)
        self.assertIn("COACH-CHECKPOINT-1.md", (ctx.run_dir / "RUN-MAP.md").read_text(encoding="utf-8"))

        # run again without a decision: still stopped, and nothing is scored twice
        ctx, out = self.run_it(fake)
        self.assertEqual(out["status"], "halted")
        self.assertEqual(len(fake.seen), 1)

        # the researcher goes on as they are; the findings are validated and scored (three scorings in all)
        ctx, out = self.run_it(fake, release=True, stop="frd_assess")
        self.assertEqual(out["status"], "complete", out)
        rec = read_json(coach._record_path(ctx, 2))["axes"]["A1"]
        first = read_json(ctx.run_dir / "frd-evaluation.json")["results"]["A1"]
        first = (first.get("axis-only") or first.get("combined"))["allocations"]["A1-H1"]
        if first >= 43:
            self.assertEqual((rec["standing"], len(rec["vectors"])), ("at target", 1))
        else:
            self.assertEqual([v["A1-H1"] for v in rec["vectors"]], [first, 30, 30])
            self.assertEqual((fake.seen[-1]["evidence"], fake.seen[-1]["times"]), ("frds", 2))
        self.assertTrue((ctx.run_dir / "COACH-CHECKPOINT-2.md").exists())

    def checkpoint_2(self, first, *more):
        ctx, out = self.run_it(scorer(60), stop="frd_assess")              # the quest's answers look fine: no stop
        self.assertEqual(out["status"], "complete", out)
        ev = read_json(ctx.run_dir / "frd-evaluation.json")
        scope = "axis-only" if ev["results"]["A1"].get("axis-only") else "combined"
        ev["results"]["A1"][scope]["allocations"] = {"A1-H1": first, "A1-H2": 54 - first, "A1-H3": 10}
        write_json(ctx.run_dir / "frd-evaluation.json", ev)
        fake = scorer(*more) if more else scorer(0)
        rec = coach.checkpoint(ctx, 2, model=self.model, scorer=fake)
        return ctx, rec, fake

    def test_after_validation_three_scorings_are_averaged(self):
        ctx, rec, fake = self.checkpoint_2(46)
        a = rec["axes"]["A1"]
        self.assertEqual((a["standing"], len(a["vectors"]), rec["hold"]), ("at target", 1, False))
        self.assertEqual(fake.seen, [])                                    # at target on the first scoring: no more calls
        self.assertIn("You are where you wanted to be.", (ctx.run_dir / "COACH-CHECKPOINT-2.md").read_text(encoding="utf-8"))

        ctx, rec, fake = self.checkpoint_2(40, 41, 44)                     # mean 42, but one scoring reached 43
        a = rec["axes"]["A1"]
        self.assertEqual(([v["A1-H1"] for v in a["vectors"]], a["mean"]["A1-H1"]), ([40, 41, 44], 42))
        self.assertEqual((a["standing"], rec["hold"]), ("within noise of target", False))
        self.assertIn("too close to call", (ctx.run_dir / "COACH-CHECKPOINT-2.md").read_text(encoding="utf-8"))

        ctx, rec, fake = self.checkpoint_2(36, 34, 35)
        a = rec["axes"]["A1"]
        self.assertEqual((a["mean"]["A1-H1"], a["standing"], rec["hold"]), (35, "below target", True))
        self.assertEqual((fake.seen[0]["evidence"], fake.seen[0]["times"]), ("frds", 2))
        talk = (ctx.run_dir / "COACH-CHECKPOINT-2.md").read_text(encoding="utf-8")
        self.assertIn("score the same findings under it for a dollar or two", talk)
        self.assertIn("Each scoring gave A1-H1: 36, 34, 35.", talk)
        # the run now waits in front of the stages that build on the findings
        hold = coach.hold_before(ctx, "language")
        self.assertEqual((hold["gate"], hold["read"]), ("frd_assess", "COACH-CHECKPOINT-2.md"))
        coach.release(ctx)
        self.assertIsNone(coach.hold_before(ctx, "language"))

    def test_the_same_findings_can_be_scored_under_another_frame(self):
        ctx, out = self.run_it(scorer(60), stop="frd_assess")
        self.assertEqual(out["status"], "complete", out)
        hp = self.proj / "01_FRAME" / "header.md"
        old = ctx.frame["axes"][0]["hypotheses"][0]["statement"]
        new = "Men with bladder outlet obstruction should be offered compound Z as a monitored trial."
        alt = self.tmp / "header-offer.md"
        alt.write_text(hp.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
        before = {p: p.stat().st_mtime_ns for p in ctx.run_dir.rglob("*") if p.is_file() and "00_RUN-CONTROL" not in p.parts}

        fake = scorer(47, 49, 51)
        got = coach.rescore(ctx, header=alt, scorer=fake)
        self.assertEqual(len(got), 1)
        e = got[0]
        self.assertEqual((e["mean"]["A1-H1"], e["standing"], e["statements"]["A1-H1"]), (49, "at target", new))
        self.assertEqual((fake.seen[0]["claim"], fake.seen[0]["evidence"], fake.seen[0]["times"]), (new, "frds", 3))
        self.assertGreater(fake.seen[0]["rows"], 0)
        after = {p: p.stat().st_mtime_ns for p in before}
        self.assertEqual(before, after)                                    # the run's own records are untouched

        coach.rescore(ctx, scorer=scorer(33, 35, 34))                      # and the header as it stands, for comparison
        ladder = (self.proj / "01_FRAME" / coach.LADDER_MD).read_text(encoding="utf-8")
        rows = [ln for ln in ladder.splitlines() if "| the validated findings |" in ln]
        self.assertTrue(any(new in ln and "**49** of 64" in ln and "47, 49, 51" in ln and "at target" in ln for ln in rows), ladder)
        self.assertTrue(any(old[:40] in ln and "**34** of 64" in ln and "below target" in ln for ln in rows), ladder)

        out, err = io.StringIO(), io.StringIO()                            # the command, with the offline engine
        with redirect_stdout(out), redirect_stderr(err):
            rc = main(["rescore", str(self.proj), "--run", "RUN-C", "--header", str(alt), "--times", "1"])
        self.assertEqual(rc, 0, err.getvalue())
        self.assertIn(f"claim (A1-H1): {new}", out.getvalue())
        self.assertIn("standing:", out.getvalue())
        self.assertIn("FRAME-LADDER.md", out.getvalue())


if __name__ == "__main__":
    unittest.main()
