"""Quest throughput scorecard: the clock starts at the go-ahead, QIDs count once, grading lag shows."""

import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.notebooklm import quest_tool  # noqa: E402
from claimreg.notebooklm.scorecard import read_record, render, score  # noqa: E402
from claimreg.util import write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

GO = datetime(2026, 11, 10, 15, 0, tzinfo=timezone.utc)
ANSWER = "A usable answer (smith2020.md, Results). " * 20


def iso(t):
    return t.isoformat()


def recorder_quest(root: Path, n: int, every_s: int, grade_every: int, grade_delay_min: float,
                   startup_min: float = 2.0, lanes: int = 6, failed=()):
    """n questions, one usable capture every `every_s` seconds after a `startup_min` start-up;
    a grading round commits every `grade_every` captures, `grade_delay_min` after the last one."""
    rec = root / "state" / "recording"
    (rec / "questions").mkdir(parents=True)
    (rec / "captures").mkdir()
    write_json(rec / "run.json", {"run_id": "T", "requested_at": iso(GO)})
    caps = []
    for i in range(n):
        qid = f"Q{i + 1:04d}"
        sub = GO + timedelta(minutes=startup_min, seconds=i * every_s)
        cap = sub + timedelta(seconds=60 * lanes // 6 * 1)
        write_json(rec / "questions" / f"{qid}.json", {"qid": qid, "query": "q", "source_voices": [],
                                                        "metadata": {}, "reserved_at": iso(sub)})
        ok = qid not in failed
        write_json(rec / "captures" / f"{qid}-A01.json", {
            "qid": qid, "attempt": "A01", "query": "q", "answer": ANSWER if ok else "Tool call:default_api:x",
            "outcome": "COMPLETE", "metadata": {"usable": ok, "lane": f"L{i % lanes}"},
            "submitted_at": iso(sub), "captured_at": iso(cap)})
        caps.append((qid, cap))
    assessments = []
    for k in range(0, n, grade_every):
        batch = caps[k:k + grade_every]
        t = batch[-1][1] + timedelta(minutes=grade_delay_min)
        assessments.append({"committed_at": iso(t), "members": [{"qid": q, "attempt": "A01"} for q, _ in batch]})
    write_json(root / "state" / "assessment-ledger.json", {"assessments": assessments})
    return root


class ScorecardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("scorecard")

    def tearDown(self):
        cleanup(self.tmp)

    def verdicts(self, sc):
        return {c["check"]: c["verdict"] for c in sc["checks"]}

    def test_a_good_quest_passes(self):
        # 60 questions, one a minute, graded in rounds of 6 two minutes after the round fills
        q = recorder_quest(self.tmp / "good", n=60, every_s=60, grade_every=6, grade_delay_min=2)
        sc = score(read_record(q))
        self.assertEqual(sc["clock"]["start_basis"], "recorded go-ahead (run.json requested_at)")
        self.assertEqual(sc["overall"], "PASS", render(sc))
        self.assertLessEqual(max(b["captured"] for b in sc["per_10_minutes"]), 10)
        self.assertIn("graded", sc["checks"][2]["result"])

    def test_counting_from_first_send_is_refused_as_a_pass(self):
        q = recorder_quest(self.tmp / "late", n=60, every_s=60, grade_every=6, grade_delay_min=2, startup_min=30)
        sc = score(read_record(q))
        v = self.verdicts(sc)
        self.assertEqual(v["Start-up"], "FAIL")
        self.assertEqual(v["First hour"], "FAIL")          # only ~29 graded inside the first hour
        self.assertIn("start-up", sc["diagnostics"]["bottleneck"])

    def test_grading_lag_fails_steering(self):
        # fast lanes, Manager grades everything 40 minutes late: the 10-30 pattern
        q = recorder_quest(self.tmp / "lag", n=90, every_s=20, grade_every=6, grade_delay_min=40)
        sc = score(read_record(q))
        v = self.verdicts(sc)
        self.assertEqual(v["Steering"], "FAIL")
        self.assertIn("grading", sc["diagnostics"]["bottleneck"])
        self.assertGreater(sc["diagnostics"]["capture_to_graded_minutes_median"], 30)

    def test_failed_attempts_and_repeats_do_not_count(self):
        q = recorder_quest(self.tmp / "fail", n=20, every_s=60, grade_every=5, grade_delay_min=1,
                           failed={"Q0003", "Q0004"})
        cap = q / "state" / "recording" / "captures"
        # a re-ask of Q0003 that succeeds, and a duplicate re-ask of Q0001
        for qid, att in (("Q0003", "A02"), ("Q0001", "A02")):
            write_json(cap / f"{qid}-{att}.json", {
                "qid": qid, "attempt": att, "query": "q", "answer": ANSWER, "outcome": "COMPLETE",
                "metadata": {"usable": True, "lane": "L0"},
                "submitted_at": iso(GO + timedelta(minutes=30)), "captured_at": iso(GO + timedelta(minutes=31))})
        k = score(read_record(q))["counts"]
        self.assertEqual((k["questions"], k["attempts"], k["usable_qids"]), (20, 22, 19))
        self.assertEqual(k["questions_without_usable_answer"], 1)

    def test_no_grading_times_is_unknown_never_pass(self):
        q = recorder_quest(self.tmp / "nograde", n=60, every_s=60, grade_every=6, grade_delay_min=2)
        (q / "state" / "assessment-ledger.json").unlink()
        sc = score(read_record(q))
        v = self.verdicts(sc)
        self.assertEqual(v["First hour"], "UNKNOWN")
        self.assertEqual(sc["overall"], "INCOMPLETE")

    def test_away_time_is_excluded_only_when_disclosed(self):
        q = recorder_quest(self.tmp / "away", n=60, every_s=60, grade_every=6, grade_delay_min=2, startup_min=25)
        sc = score(read_record(q), excludes=[(GO + timedelta(minutes=1), GO + timedelta(minutes=24))])
        self.assertEqual(self.verdicts(sc)["Start-up"], "PASS")
        self.assertEqual(sc["clock"]["excluded_minutes"], 23.0)

    def test_driver_layout_with_timestamped_assessed_file(self):
        ans = self.tmp / "nlm-answers"
        (ans / "queue").mkdir(parents=True)
        write_json(ans / "quest-clock.json", {"driver_started": iso(GO)})
        for i in range(50):
            qid = f"Q{i + 1:04d}"
            sub = GO + timedelta(minutes=1, seconds=i * 60)
            write_json(ans / f"{qid}-A01.json", {
                "qid": qid, "attempt": "A01", "lane": f"L{i % 6}", "query": "q", "answer": ANSWER,
                "outcome": "COMPLETE", "query_seen_in_user_message": True,
                "submitted_at": iso(sub), "captured_at": iso(sub + timedelta(seconds=50))})
        af = ans / "assessed-qids.json"
        af.write_text(json.dumps(["Q0001"]))                       # the old plain-list format
        quest_tool.mark_assessed(af, ["Q0002", "Q0003"])
        d = json.loads(af.read_text())
        self.assertEqual(d["assessed"], ["Q0001", "Q0002", "Q0003"])
        self.assertIn("Q0002", d["times"])
        self.assertNotIn("Q0001", d["times"])                        # its time was never recorded
        rec = read_record(ans)
        self.assertEqual(rec["layout"], "driver")
        self.assertTrue(rec["start_basis"].startswith("driver first started"))
        self.assertEqual(set(rec["graded"]), {"Q0002", "Q0003"})


if __name__ == "__main__":
    unittest.main()
