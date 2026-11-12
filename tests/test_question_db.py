"""The question database: QUESTIONS.md at the top of a run."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.question_db import AUDIT_PROMPT, build, render, write_question_database  # noqa: E402
from claimreg.util import write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

INDEX = """# Index

### Rank A — 2 sources

#### alpha2020.pdf.md
- **Title:** Alpha 2020. A trial.
- **Source:** alpha2020.pdf.md

#### beta2021.pdf.md
- **Title:** Beta 2021. Another trial | with a pipe.
- **Source:** beta2021.pdf.md

### Rank B — 1 sources

#### gamma2019.pdf.md
- **Title:** Gamma 2019. A review.
- **Source:** gamma2019.pdf.md
"""


def question(qid, source, resolved=True, answered=True, text=None):
    return {"qid": qid, "text": text or f"In `{source}`, what did the study report?\nGive numbers.",
            "sources_as_sent": [source], "sources_resolved": {source: source if resolved else None},
            "status": "ANSWERED" if answered else "ISSUED", "response_ids": [f"R-{qid}-A01"] if answered else [],
            "attempts": ["A01"] if answered else [], "axis_source": "investigator"}


def axis_run(tmp: Path) -> Path:
    run = tmp / "RUN-T"
    (run / "01_FRAME").mkdir(parents=True)
    (run / "01_FRAME" / "index.md").write_text(INDEX, encoding="utf-8")
    write_json(run / "01_FRAME" / "frame.json", {"axes": [
        {"axis_id": "A1", "name": "first axis", "question": "Does X help?"},
        {"axis_id": "A2", "name": "second axis", "question": "Does Y help?"}]})
    a1 = run / "AXIS-A1__first-axis"
    write_json(a1 / "02_DISCOVERY" / "01_issued-questions" / "questions.json", [
        question("Q0002", "beta2021.pdf.md"), question("Q0001", "alpha2020.pdf.md"),
        question("Q0003", "nosuch.md", resolved=False), question("Q0004", "alpha2020.pdf.md", answered=False)])
    write_json(a1 / "03_FRDS" / "01_candidates" / "candidates.json",
               [{"frd_id": f"FRD-Q0001-0{i}", "qid": "Q0001"} for i in (1, 2, 3)] + [{"frd_id": "FRD-Q0002-01", "qid": "Q0002"}])
    write_json(a1 / "03_FRDS" / "04_validation-results" / "validations.json", [
        {"vfrd_id": "FRD-Q0001-01", "qid": "Q0001", "readiness_reason": "Directly stated."},
        {"vfrd_id": "FRD-Q0001-02", "qid": "Q0001", "readiness_reason": "Directly stated."},
        {"vfrd_id": "FRD-Q0001-03", "qid": "Q0001",
         "readiness_reason": "mechanical check: the validator's source_text was not found in the named source file (none)"},
        {"vfrd_id": "FRD-Q0002-01", "qid": "Q0002", "readiness_reason": "no resolvable named source (needs-source)"}])
    write_json(a1 / "03_FRDS" / "05_validated" / "retained-frds.json", [
        {"vfrd_id": "FRD-Q0001-01", "qid": "Q0001"}, {"vfrd_id": "FRD-Q0001-02", "qid": "Q0001"}])
    write_json(run / "AXIS-A2__second-axis" / "02_DISCOVERY" / "01_issued-questions" / "questions.json", [])
    return run


class QuestionDatabaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("question-db")

    def tearDown(self):
        cleanup(self.tmp)

    def test_rows_counts_and_flags(self):
        db = build(axis_run(self.tmp))
        self.assertEqual(db["totals"], {"questions": 4, "answered": 3, "frds_kept": 2, "flagged": 4})
        a1, a2 = db["axes"]
        self.assertEqual([r["qid"] for r in a1["questions"]], ["Q0001", "Q0002", "Q0003", "Q0004"])
        self.assertEqual((a1["axis_id"], a1["name"], a1["question"]), ("A1", "first axis", "Does X help?"))
        self.assertEqual(a2["questions"], [])
        q1, q2, q3, q4 = a1["questions"]
        self.assertEqual((q1["frd_candidates"], q1["frds_kept"], q1["flags"]), (3, 2, ["quote check dropped 1"]))
        self.assertEqual(q2["flags"], ["no FRDs kept", "1 dropped: source not found"])
        self.assertEqual((q3["sources"], q3["flags"]), ([], ["source not found: nosuch.md", "no FRDs kept"]))
        self.assertEqual(q4["flags"], ["no answer"])
        self.assertNotIn("\n", q1["text"])

    def test_sources_never_named_come_from_the_index(self):
        db = build(axis_run(self.tmp))
        src = db["sources"]
        self.assertEqual(src["indexed"], 3)
        self.assertEqual(src["named"], {"alpha2020.pdf.md": ["Q0001", "Q0004"], "beta2021.pdf.md": ["Q0002"]})
        self.assertEqual(src["named_by_rank"], {"A": {"named": 2, "indexed": 2}, "B": {"named": 0, "indexed": 1}})
        self.assertEqual(src["never_named"], [{"file": "gamma2019.pdf.md", "rank": "B", "title": "Gamma 2019. A review."}])

    def test_markdown_is_self_contained(self):
        run = axis_run(self.tmp)
        db = write_question_database(run, "RUN-T")
        text = (run / "QUESTIONS.md").read_text(encoding="utf-8")
        self.assertTrue((run / "QUESTIONS.json").exists())
        self.assertEqual(text, render(db))
        self.assertIn(AUDIT_PROMPT, text)
        self.assertIn("### Axis A2: second axis", text)
        self.assertIn("No questions were asked for this axis.", text)
        self.assertIn("| Q0001 | `alpha2020.pdf.md` | In `alpha2020.pdf.md`, what did the study report? Give numbers. | 2 | quote check dropped 1 |", text)
        self.assertIn("| B | `gamma2019.pdf.md` | Gamma 2019. A review. |", text)
        self.assertIn("Rank A 2 of 2; Rank B 0 of 1", text)
        for line in text.splitlines():                       # no cell breaks a table row
            if line.startswith("| Q0"):
                self.assertEqual(line.replace("\\|", "").count("|"), 6, line)

    def test_before_frds_and_without_axes_or_index(self):
        run = self.tmp / "RUN-FLAT"
        write_json(run / "02_DISCOVERY" / "01_issued-questions" / "questions.json",
                   [question("Q0001", "alpha2020.pdf.md", text="Does a | b hold in `alpha2020.pdf.md`?")])
        db = write_question_database(run)
        self.assertEqual(db["run_id"], "RUN-FLAT")
        row = db["axes"][0]["questions"][0]
        self.assertEqual((row["frd_candidates"], row["frds_kept"], row["flags"]), (None, None, []))
        text = (run / "QUESTIONS.md").read_text(encoding="utf-8")
        self.assertIn("| not built yet |", text)
        self.assertIn("Does a \\| b hold", text)
        self.assertIn("This run has no source index", text)
        self.assertNotIn("### Axis", text)

    def test_nothing_written_before_any_question(self):
        run = self.tmp / "RUN-EMPTY"
        run.mkdir()
        self.assertIsNone(write_question_database(run))
        self.assertFalse((run / "QUESTIONS.md").exists())

    def test_pipeline_writes_it_and_the_run_map_points_to_it(self):
        from claimreg.pipeline import run_pipeline
        from claimreg.runctx import RunContext
        from test_pipeline_mock import make_project
        proj = make_project(self.tmp)
        ctx = RunContext(proj, "RUN-TEST", create=True, quiet=True)
        self.assertEqual(run_pipeline(ctx)["status"], "complete")
        text = (ctx.run_dir / "QUESTIONS.md").read_text(encoding="utf-8")
        asked = ctx.load_whole_run("discovery", "01_issued-questions/questions.json") or []
        self.assertTrue(asked)
        for q in asked:
            self.assertIn(f"| {q['qid']} |", text)
        self.assertIn("[QUESTIONS.md](QUESTIONS.md)", (ctx.run_dir / "RUN-MAP.md").read_text(encoding="utf-8"))
        self.assertIn("Question database: [QUESTIONS.md]", (ctx.run_dir / "RUN-STATUS.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
