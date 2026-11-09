"""`quest_tool.py` sync commands: stage (answers -> Manager workspace), packet (packet -> queue),
sync (Manager ledger -> assessed-qids.json). The three hand-copies the 11-09 run needed."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.notebooklm import quest_tool  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

ANSWER = {
    "qid": "Q0001", "attempt": "A01", "lane": "clone-2",
    "notebook_url": "https://notebooklm.google.com/notebook/test",
    "query": "Using smith2020.md, report the flow results.",
    "query_seen_in_user_message": True,
    "outcome": "COMPLETE",
    "answer": "Flow rose by 3.1 mL/s (smith2020.md, Results).",
    "answer_names_requested_source": True,
    "contains_tool_output": False,
    "generation_seconds": 84,
    "submitted_at": "2026-11-09T19:04:34.575Z",
    "captured_at": "2026-11-09T19:05:59.593Z",
}

PACKET = """# R001

Direction: CONTINUE. Open priorities: tissue exposure.

## Ready questions

1. [target: exposure] Using smith2020.md, report every dose and the measured plasma concentration with (exact source filename, actual section heading) beside each number. Answer in about 900 words or more.
2. [target: time course] Using jones2021.md and lee2019.md, report the time course of the flow change and the tissue concentration, citing (exact source filename, actual section heading) beside each number.
3. Report whether the trial measured this at all, with (exact source filename, actual section heading) beside each number.

## Private notes

Allocation vectors and hypothesis labels must never appear in a packet.
"""


class StageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("quest-tool-stage")

    def tearDown(self):
        cleanup(self.tmp)

    def _answer_file(self, name="Q0001-A01.json", **over):
        answers = self.tmp / "answers"
        answers.mkdir(exist_ok=True)
        payload = dict(ANSWER, **over)
        (answers / name).write_text(json.dumps(payload), encoding="utf-8")
        return answers

    def test_stage_writes_the_manager_markdown(self):
        answers = self._answer_file()
        out = self.tmp / "ws" / "answers"
        staged = quest_tool.stage(answers, out, ["q0001"])
        self.assertEqual(len(staged), 1)
        self.assertEqual(staged[0]["qid"], "Q0001")
        md = (out / "Q0001-A01.md").read_text(encoding="utf-8")
        self.assertIn("## Query", md)
        self.assertIn(ANSWER["query"], md)
        self.assertIn("## Answer", md)
        self.assertIn("Flow rose by 3.1 mL/s", md)
        self.assertIn("| contains_tool_output | false |", md)
        self.assertIn("| answer_names_requested_source | true |", md)
        self.assertIn("| generation_seconds | 84 |", md)

    def test_stage_qid_filter_and_bom_tolerance(self):
        answers = self.tmp / "answers"
        answers.mkdir()
        (answers / "Q0001-A01.json").write_text("\ufeff" + json.dumps(ANSWER), encoding="utf-8")
        (answers / "Q0002-A01.json").write_text(json.dumps(dict(ANSWER, qid="Q0002")), encoding="utf-8")
        (answers / "broken.json").write_text("{not json", encoding="utf-8")
        out = self.tmp / "out"
        staged = quest_tool.stage(answers, out, ["Q0002"])
        self.assertEqual([s["qid"] for s in staged], ["Q0002"])
        self.assertEqual(sorted(p.name for p in out.glob("*.md")), ["Q0002-A01.md"])

    def test_stage_is_idempotent(self):
        answers = self._answer_file()
        out = self.tmp / "out"
        quest_tool.stage(answers, out)
        first = (out / "Q0001-A01.md").read_text(encoding="utf-8")
        quest_tool.stage(answers, out)
        self.assertEqual(first, (out / "Q0001-A01.md").read_text(encoding="utf-8"))


class PacketTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("quest-tool-packet")
        self.answers = self.tmp / "answers"
        (self.answers / "queue").mkdir(parents=True)
        self.packet = self.tmp / "R001.md"
        self.packet.write_text(PACKET, encoding="utf-8")

    def tearDown(self):
        cleanup(self.tmp)

    def _queue(self):
        return {p.name: json.loads(p.read_text(encoding="utf-8"))
                for p in sorted((self.answers / "queue").glob("Q*.json"))}

    def test_parses_ready_questions_and_writes_queue_files(self):
        queued = quest_tool.packet(self.packet, self.answers)
        self.assertEqual(len(queued), 3)
        self.assertEqual([q["qid"] for q in queued], ["Q0001", "Q0002", "Q0003"])
        self.assertEqual(queued[0]["target"], "exposure")
        self.assertTrue(queued[0]["text"].startswith("Using smith2020.md"))
        self.assertNotIn("[target:", queued[0]["text"])
        # the "## Private notes" section is never treated as questions
        self.assertNotIn("Allocation vectors", json.dumps(queued))
        files = self._queue()
        self.assertEqual(sorted(files), ["Q0001.json", "Q0002.json", "Q0003.json"])
        self.assertEqual(files["Q0002.json"], {"qid": "Q0002", "attempt": "A01",
                                               "text": queued[1]["text"]})

    def test_firewall_warnings_name_the_problem(self):
        queued = quest_tool.packet(self.packet, self.answers)
        self.assertEqual(queued[0]["warnings"], [])                       # single source, 900 words or more
        self.assertEqual(queued[1]["warnings"], [])                       # multi source, no length
        self.assertEqual(queued[2]["warnings"], ["no source filename in the question"])

    def test_index_membership_length_ceiling_and_multi_source_length(self):
        index = self.tmp / "index.md"
        index.write_text("- **Source:** [smith2020.pdf.md](<C:/x/smith2020.pdf.md>)\n"
                         "- **Source:** [jones2021.pdf.md](<C:/x/jones2021.pdf.md>)\n", encoding="utf-8")
        self.packet.write_text("## Ready questions\n\n"
                               "1. Using smith2020.md and jones2021.md, report the results in 900 words or less, "
                               "with (exact source filename, actual section heading) beside each number.\n"
                               "2. Using smith2020.md and jones2021.md, report the results in about 900 words, "
                               "with (exact source filename, actual section heading) beside each number.\n",
                               encoding="utf-8")
        queued = quest_tool.packet(self.packet, self.answers, index=index)
        self.assertIn("asks for a length ceiling", " ".join(queued[0]["warnings"]))
        self.assertIn("must not state a length", " ".join(queued[1]["warnings"]))
        # unknown filenames are flagged when an index is supplied
        self.packet.write_text("## Ready questions\n\n"
                               "1. Using nowhere2025.md, report the dose with (exact source filename, "
                               "actual section heading) beside each number.\n", encoding="utf-8")
        queued = quest_tool.packet(self.packet, self.answers, index=index)
        self.assertIn("not in the index", " ".join(queued[0]["warnings"]))

    def test_numbering_continues_and_can_be_forced(self):
        quest_tool.packet(self.packet, self.answers)
        queued = quest_tool.packet(self.packet, self.answers, start=42)
        self.assertEqual([q["qid"] for q in queued], ["Q0042", "Q0043", "Q0044"])
        # a repeat enqueue of identical text is flagged, never silently sent twice
        self.assertTrue(any("already in the queue" in w for w in queued[0]["warnings"]))

    def test_dry_run_writes_nothing(self):
        queued = quest_tool.packet(self.packet, self.answers, dry_run=True)
        self.assertEqual(len(queued), 3)
        self.assertEqual(self._queue(), {})

    def test_wrapped_question_lines_are_joined(self):
        self.packet.write_text("## Ready questions\n\n"
                               "1. [target: exposure] Using smith2020.md, report every dose\n"
                               "   and the measured plasma concentration with (exact source filename,\n"
                               "   actual section heading) beside each number.\n", encoding="utf-8")
        queued = quest_tool.packet(self.packet, self.answers, dry_run=True)
        self.assertEqual(len(queued), 1)
        self.assertIn("report every dose and the measured plasma", queued[0]["text"])

    def test_missing_ready_section_is_an_error(self):
        self.packet.write_text("# R001\n\nDirection: CONTINUE.\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            quest_tool.packet(self.packet, self.answers)


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("quest-tool-sync")

    def tearDown(self):
        cleanup(self.tmp)

    def _ledger(self, assessments):
        path = self.tmp / "ws" / "private" / "assessment-ledger.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"run_id": "PTX-NLM", "assessments": assessments}), encoding="utf-8")
        return path

    def test_stamps_grading_times_from_rounds(self):
        ledger = self._ledger([
            {"assessment_id": "R001", "committed_at": "2026-11-09T20:15:00Z",
             "members": [{"qid": "Q0001", "attempt": "A01"}, {"qid": "Q0002", "attempt": "A01"}]},
            {"assessment_id": "R002", "committed_at": "2026-11-09T20:23:30+00:00",
             "members": [{"qid": "Q0003", "attempt": "A01"}]}])
        assessed = self.tmp / "answers" / "assessed-qids.json"
        quest_tool.sync(ledger, assessed)
        data = json.loads(assessed.read_text(encoding="utf-8"))
        self.assertEqual(data["assessed"], ["Q0001", "Q0002", "Q0003"])
        self.assertEqual(data["times"]["Q0001"], "2026-11-09T20:15:00+00:00")
        self.assertEqual(data["times"]["Q0003"], "2026-11-09T20:23:30+00:00")

    def test_merges_with_existing_times_and_is_idempotent(self):
        assessed = self.tmp / "answers" / "assessed-qids.json"
        assessed.parent.mkdir(parents=True)
        assessed.write_text(json.dumps({"assessed": ["Q0000"], "times": {"Q0000": "2026-11-09T20:00:00+00:00"}}),
                            encoding="utf-8")
        ledger = self._ledger([{"assessment_id": "R001", "committed_at": "2026-11-09T20:15:00Z",
                                "members": [{"qid": "Q0000"}, {"qid": "Q0001"}]}])
        quest_tool.sync(ledger, assessed)
        data = json.loads(assessed.read_text(encoding="utf-8"))
        self.assertEqual(data["assessed"], ["Q0000", "Q0001"])
        self.assertEqual(data["times"]["Q0000"], "2026-11-09T20:00:00+00:00")   # first stamp wins
        self.assertEqual(data["times"]["Q0001"], "2026-11-09T20:15:00+00:00")
        before = assessed.read_text(encoding="utf-8")
        quest_tool.sync(ledger, assessed)
        self.assertEqual(before, assessed.read_text(encoding="utf-8"))

    def test_reads_old_plain_list_format_and_naive_times(self):
        assessed = self.tmp / "answers" / "assessed-qids.json"
        assessed.parent.mkdir(parents=True)
        assessed.write_text(json.dumps(["Q0005"]), encoding="utf-8")
        ledger = self._ledger([{"assessment_id": "R001", "committed_at": "2026-11-09T20:15:00",
                                "members": [{"qid": "Q0006"}]}])
        quest_tool.sync(ledger, assessed)
        data = json.loads(assessed.read_text(encoding="utf-8"))
        self.assertEqual(data["assessed"], ["Q0005", "Q0006"])
        self.assertEqual(data["times"]["Q0006"], "2026-11-09T20:15:00+00:00")


if __name__ == "__main__":
    unittest.main()
