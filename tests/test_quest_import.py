"""`cr import-quest`: a recorded NotebookLM quest becomes a run that continues at FRD generation."""

import json
import shutil
import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.quest_import import QuestImportError, import_quest  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "mini"
PAD = (" The trial was described in the Methods and Results sections with the numbers given above, and "
       "the authors discussed limitations including sample size and short follow-up in the Discussion.")


def nb_answer(lines: list[str]) -> str:
    """A NotebookLM-style answer: paraphrased statements, each cited (filename, heading)."""
    return "Thoughts\nexpand_more\n" + "\n".join(f"[CLINICAL] {l}" for l in lines) + "\n" + PAD * 2


ANSWERS = {
    ("Q0001", "A01"): nb_answer([
        "Sixty adult men with bladder outlet obstruction were randomized to compound Z 400 mg twice "
        "daily or placebo for twelve weeks (smith2020.md, Methods).",
        "Maximum urinary flow rate increased by 3.1 mL/s with compound Z and by 0.4 mL/s with "
        "placebo, a significant difference (smith2020.md, Results)."]),
    ("Q0002", "A01"): "Tool response for view_file: exit_code: 0\n" + nb_answer([
        "Maximum urinary flow rate did not differ significantly between compound Z and placebo "
        "after eight weeks (jones2021.md, Results)."]),
    ("Q0002", "A02"): nb_answer([
        "Maximum urinary flow rate did not differ significantly between the compound Z and placebo "
        "groups after eight weeks of treatment (jones2021.md, Results)."]),
    ("Q0003", "A01"): nb_answer([
        "Compound Z was detected in prostate tissue at concentrations comparable to plasma "
        "concentrations in all twelve men (lee2019.md, Results)."])
        + "\nTool response for view_file: lee2019.md (title as the tool reported it)\n",
    ("Q0004", "A01"): "Tool call:default_api:view_file{AbsolutePath:/workspace/knowledge/park2018.md}",
}
SOURCES = {"Q0001": "smith2020.md", "Q0002": "jones2021.md", "Q0003": "lee2019.md", "Q0004": "park2018.md"}


def make_project(tmp: Path) -> Path:
    proj = tmp / "proj"
    (proj / "01_CORPUS").mkdir(parents=True)
    shutil.copytree(FIX / "sources", proj / "01_CORPUS" / "source-files")
    (proj / "01_FRAME").mkdir()
    shutil.copyfile(FIX / "header.md", proj / "01_FRAME" / "header.md")
    shutil.copyfile(FIX / "index.md", proj / "01_FRAME" / "index.md")
    shutil.copyfile(FIX / "archivist.txt", proj / "01_FRAME" / "archivist-custom-prompt.txt")
    write_json(proj / "project.json", {"project": {"name": "mini", "run_prefix": "RUN-MINI"},
                                       "default_provider": "local"})
    return proj


def make_recorder_quest(tmp: Path) -> Path:
    """The layout quest_tool.py / quest_io.py write: <state>/recording/{questions,captures}."""
    root = tmp / "quest"
    rec = root / "artifacts" / "quest-state" / "recording"
    (rec / "questions").mkdir(parents=True)
    (rec / "captures").mkdir()
    (root / "artifacts" / "feedback-packets").mkdir()
    (root / "artifacts" / "feedback-packets" / "R001.md").write_text("# R001\n\nReady questions ...\n")
    for i, (qid, src) in enumerate(SOURCES.items()):
        q = f"Using {src}, report the design, the dose and the flow results with (exact source filename, actual section heading) beside each number."
        write_json(rec / "questions" / f"{qid}.json", {
            "run_id": "MINI-NLM", "qid": qid, "query": q, "source_voices": [src],
            "metadata": {"round_number": 1, "order_in_round": i + 1, "target_ledger_row_or_test": "flow",
                         "header_version": "header.md", "packet_priority_id": None},
            "reserved_at": "2026-11-09T10:00:00+00:00"})
    for (qid, att), ans in ANSWERS.items():
        write_json(rec / "captures" / f"{qid}-{att}.json", {
            "run_id": "MINI-NLM", "qid": qid, "attempt": att, "query": f"Using {SOURCES[qid]}, ...",
            "metadata": {"usable": True, "lane": "primary", "cited_sources": [{"source_voice": SOURCES[qid]}]},
            "answer": ans, "outcome": "COMPLETE", "notebook_url": "https://notebooklm.google.com/notebook/x",
            "submitted_at": "2026-11-09T10:01:00Z", "captured_at": "2026-11-09T10:02:00Z"})
    return root


def make_driver_quest(tmp: Path) -> Path:
    """The driver's own layout: <answers>/Qnnnn-Ann.json, questions in <answers>/queue/."""
    ans = tmp / "nlm-answers"
    (ans / "queue").mkdir(parents=True)
    for (qid, att), text in ANSWERS.items():
        write_json(ans / f"{qid}-{att}.json", {
            "run_id": "MINI-DRIVER", "qid": qid, "attempt": att, "lane": "clone-1",
            "notebook_url": "https://notebooklm.google.com/notebook/y", "query": f"Using {SOURCES[qid]}, report the results.",
            "query_seen_in_user_message": True, "outcome": "COMPLETE", "answer": text,
            "submitted_at": "2026-11-09T10:01:00Z", "captured_at": "2026-11-09T10:02:00Z"})
    return ans


class QuestImportTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("quest-import")
        self.proj = make_project(self.tmp)

    def tearDown(self):
        cleanup(self.tmp)

    def _responses(self, run):
        ctx = RunContext(self.proj, run, quiet=True)
        return ctx, {r["qid"]: r for r in ctx.load("discovery", "02_query-responses/responses.json")}

    def test_recorder_layout_selection_flags_and_continuation(self):
        out = import_quest(self.proj, make_recorder_quest(self.tmp), run_id="RUN-A")
        self.assertEqual(out["questions"], 4)
        self.assertEqual(out["layout"], "recorder")
        ctx, r = self._responses("RUN-A")
        # clean answer
        self.assertEqual(r["Q0001"]["attempt"], "A01")
        self.assertEqual(r["Q0001"]["evidence_status"], "RETRIEVED")
        self.assertNotIn("Thoughts", r["Q0001"]["text"])
        # the clean re-ask wins over the contaminated original
        self.assertEqual(r["Q0002"]["attempt"], "A02")
        self.assertEqual(r["Q0002"]["other_attempts"], ["A01"])
        # only a contaminated answer: kept, usable, labelled candidate
        self.assertTrue(r["Q0003"]["usable"])
        self.assertTrue(r["Q0003"]["contains_tool_output"])
        self.assertEqual(r["Q0003"]["evidence_status"], "CANDIDATE_UNVERIFIED")
        # tool-call-only card: FAILED and not usable
        self.assertEqual(r["Q0004"]["outcome"], "FAILED")
        self.assertFalse(r["Q0004"]["usable"])
        self.assertIn("smith2020.md", r["Q0001"]["cited_sources"])
        # stage state and closeout
        st = ctx.stage_state()
        self.assertEqual(st["quest"]["status"], "imported")
        for s in ("corpus", "index", "archivist_prompt", "frame"):
            self.assertEqual(st[s]["status"], "done", s)
        co = ctx.load("discovery", "06_closeout/closeout.json")
        self.assertEqual(co["status"], "OPERATIONAL_STOP (imported)")
        self.assertTrue((ctx.p("discovery") / "05_feedback" / "R001-packet.md").exists())
        qs = ctx.load("discovery", "01_issued-questions/questions.json")
        self.assertEqual({q["qid"]: q["status"] for q in qs}["Q0004"], "UNUSABLE")
        # cr run continues at FRDs, and the local engine reads NotebookLM's (file, heading) citations
        res = run_pipeline(ctx, stop="frd_validate")
        self.assertEqual(res["status"], "complete", res)
        self.assertIn("quest", res["skipped"])
        cands = ctx.load("frds", "01_candidates/candidates.json")
        self.assertTrue(cands)
        self.assertTrue(all(c["source_files"] for c in cands), cands)
        vals = ctx.load("frds", "04_validation-results/validations.json")
        self.assertTrue(any(v["readiness"].startswith("READY") for v in vals))

    def test_closeout_selection_exclusion_and_scientific_stop(self):
        quest = make_recorder_quest(self.tmp)
        co = self.tmp / "CLOSEOUT.md"
        co.write_text("# Closeout\n\nSelected repair attempts used where flagged: Q0002-A01.\n")
        import_quest(self.proj, quest, run_id="RUN-B", closeout=co, exclude_tool_output=True,
                     stop="scientific")
        ctx, r = self._responses("RUN-B")
        self.assertEqual(r["Q0002"]["attempt"], "A01")          # the closeout's choice wins
        self.assertIn("explicitly", r["Q0002"]["selection"])
        self.assertFalse(r["Q0002"]["usable"])                  # ... but it carries tool output
        self.assertFalse(r["Q0003"]["usable"])
        self.assertEqual(ctx.load("discovery", "06_closeout/closeout.json")["status"],
                         "SCIENTIFIC_STOP (imported)")
        # --select overrides the closeout
        import_quest(self.proj, quest, run_id="RUN-C", closeout=co, select=["Q0002-A02"])
        _, r = self._responses("RUN-C")
        self.assertEqual(r["Q0002"]["attempt"], "A02")

    def test_driver_layout(self):
        out = import_quest(self.proj, make_driver_quest(self.tmp), run_id="RUN-D")
        self.assertEqual(out["layout"], "driver")
        ctx, r = self._responses("RUN-D")
        self.assertEqual(r["Q0002"]["attempt"], "A02")
        qs = {q["qid"]: q for q in ctx.load("discovery", "01_issued-questions/questions.json")}
        self.assertEqual(qs["Q0001"]["sources_as_sent"], ["smith2020.md"])   # parsed from the query

    def test_refuses_reimport_and_bad_input(self):
        quest = make_recorder_quest(self.tmp)
        import_quest(self.proj, quest, run_id="RUN-E")
        with self.assertRaises(QuestImportError):
            import_quest(self.proj, quest, run_id="RUN-E")
        import_quest(self.proj, quest, run_id="RUN-E", force=True)
        with self.assertRaises(QuestImportError):
            import_quest(self.proj, self.tmp / "nowhere", run_id="RUN-F")
        with self.assertRaises(QuestImportError):
            import_quest(self.proj, quest, run_id="RUN-G", select=["Q2-A1"])

    def test_resolve_is_fast_on_long_phrases(self):
        # regression: Corpus.resolve once retried every tail recursively, doubling per word
        ctx = RunContext(self.proj, "RUN-R", create=True, quiet=True)
        run_pipeline(ctx, stop="corpus")
        phrase = " ".join(["word"] * 40) + " smith2020.md"
        t = time.time()
        self.assertEqual(ctx.corpus.resolve(phrase), "smith2020.md")
        self.assertIsNone(ctx.corpus.resolve(" ".join(["nothing"] * 60) + ".md"))
        self.assertLess(time.time() - t, 2.0)


if __name__ == "__main__":
    unittest.main()
