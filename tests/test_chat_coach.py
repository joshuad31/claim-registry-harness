"""Chat-native coaching: real saved states, no keyboard simulation or live model calls."""
import contextlib
import io
import json
import shutil
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from claimreg import chat_coach as cc, frame_gate as fg, cli, onramp
from claimreg.header import parse_header
from claimreg.util import read_json, read_text, write_json
from scratch import scratch_dir, cleanup
from test_frame_gate import FakeModel

FIX = Path(__file__).parent / "fixtures" / "mini"


class ChatCoachTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("chat-coach")
        self.project = self.tmp / "research"
        self.frame = self.project / "01_FRAME"
        self.frame.mkdir(parents=True)
        self.draft = self.frame / "header-DRAFT.md"
        shutil.copyfile(FIX / "header.md", self.draft)
        shutil.copyfile(FIX / "index.md", self.frame / "index.md")
        write_json(self.project / "project.json", {"project": {"name": "Chat fixture"},
                                                   "coach": {"require_acceptance": True}})
        self.current = None

    def tearDown(self):
        cleanup(self.tmp)

    def start(self, **kwargs):
        self.current = cc.act(self.project, **kwargs)
        return self.current

    def send(self, action="reply", text="Yes, that says what I mean.", model=None, **kwargs):
        data = {"revision": self.current["revision"], "session_id": self.current["session_id"], "text": text, **kwargs}
        self.current = cc.act(self.project, action, data, model=model)
        return self.current

    def options(self, preferred=None, model=None):
        self.start()
        self.send(text="I want to understand which explanation the published evidence supports.")
        self.send(text="I am keeping an open mind." if preferred is None else "I favor the first explanation.", choice=preferred)
        self.send(text="My experience led me to ask, but it is not source evidence.")
        self.send(text="I would accept a different explanation or an unresolved result.")
        self.assertEqual(self.current["step"], "prepare")
        return self.send("prepare", model=model)

    def review(self, preferred=None, model=None):
        self.options(preferred, model)
        return self.send("select", choice=0, model=model)

    def finish(self):
        while self.current["step"] in ("wording", "scope", "consequences"):
            self.send(confirmed=True)
        self.assertEqual(self.current["step"], "approval")
        return self.send("accept", text="Yes, use the wording we just reviewed.", confirmed=True)

    def test_complete_draft_only_review_needs_no_name_keyboard_or_model(self):
        original = self.draft.read_bytes()
        with patch.object(fg, "Terminal", side_effect=AssertionError("No terminal")), \
                patch.object(fg, "model_for", side_effect=AssertionError("No API")):
            self.review()
            self.assertFalse((self.frame / "header.md").exists())
            self.assertFalse(fg.accepted(self.project)[0])
            self.assertEqual(self.finish()["status"], "completed")
        self.assertEqual(self.draft.read_bytes(), original)
        self.assertTrue(fg.accepted(self.project)[0])
        self.assertTrue(fg.gate(self.project, "quest")[0])
        certificate = fg.load_certificate(self.project)
        self.assertEqual(certificate["name"], "the researcher")
        self.assertEqual(certificate["channel"], "chat")
        rec = certificate["axes"]["A1"]
        self.assertFalse(rec["preferred"])
        self.assertFalse(rec["read"])                    # no invented timing or keyboard evidence
        self.assertEqual(rec["accepted"][-1]["typed"], "Yes, use the wording we just reviewed.")
        self.assertIn("in chat", read_text(self.frame / fg.CERT_MD))

    def test_status_resume_preserves_the_actual_reply(self):
        self.start()
        text = "My existing answer can be pasted here."
        self.send(text=text)
        saved = (self.frame / cc.SESSION).read_bytes()
        resumed = cc.act(self.project)
        self.assertEqual(resumed, self.current)
        self.assertEqual((self.frame / cc.SESSION).read_bytes(), saved)
        self.assertEqual(read_json(self.frame / cc.SESSION)["events"][0]["text"], text)

    def test_opening_the_coach_is_not_approval(self):
        self.start()
        with self.assertRaises(cc.PreparationNeeded):
            self.send("accept", text="Yes, open the coach.", confirmed=True)
        self.assertFalse((self.frame / fg.CERT_JSON).exists())
        self.assertFalse((self.frame / "header.md").exists())

    def test_every_explanation_and_limits_are_reviewed_before_approval(self):
        self.review()
        shown = []
        while self.current["step"] == "wording":
            shown.append(self.current["show"]["explanation"])
            self.assertFalse(self.current["can_accept"])
            self.send(confirmed=True)
        self.assertEqual(shown, [h["statement"] for h in parse_header(read_text(self.draft))["axes"][0]["hypotheses"]])
        self.assertEqual(self.current["step"], "scope")
        self.send(confirmed=True)
        self.assertEqual(self.current["step"], "consequences")
        self.assertEqual(self.current["show"]["forecast"]["ok"], 0)
        self.send(confirmed=True)
        self.assertTrue(self.current["can_accept"])

    def test_stale_response_and_previous_session_cannot_advance_current_review(self):
        self.start()
        old = {"revision": self.current["revision"], "session_id": self.current["session_id"], "text": "Earlier answer"}
        self.send(text="My current research purpose")
        with self.assertRaises(cc.PreparationNeeded):
            cc.act(self.project, "reply", old)
        self.start(action="restart")
        with self.assertRaises(cc.PreparationNeeded):
            cc.act(self.project, "reply", old)
        self.assertEqual(cc.act(self.project)["step"], "purpose")

    def test_a_decline_keeps_review_pending_and_does_not_write_approval(self):
        self.review()
        before = (self.frame / cc.SESSION).read_bytes()
        with self.assertRaises(cc.PreparationNeeded):
            self.send(text="No, I want to change this.", confirmed=False)
        self.assertEqual((self.frame / cc.SESSION).read_bytes(), before)
        self.assertFalse(fg.accepted(self.project)[0])

    def test_requested_edit_clears_confirmations_and_requires_another_review(self):
        self.review()
        self.send(confirmed=True)
        candidate = cc._original(parse_header(read_text(self.draft))["axes"][0])
        candidate["statements"]["A1-H1"] += " This claim is limited to the studied groups."
        self.send("revise", text="Please limit this to the studied groups.", candidate=candidate)
        self.assertEqual(self.current["step"], "wording")
        self.assertEqual(read_json(self.frame / cc.SESSION)["confirmations"], [])
        self.finish()
        self.assertIn("limited to the studied groups", read_text(self.frame / "header.md"))

    def test_external_header_map_and_config_changes_require_a_fresh_review(self):
        for name in ("header-DRAFT.md", "index.md"):
            with self.subTest(name=name):
                self.start(action="restart")
                with (self.frame / name).open("a", encoding="utf-8") as f:
                    f.write("\nExternal change\n")
                with self.assertRaises(cc.PreparationNeeded):
                    cc.act(self.project)
        self.start(action="restart")
        cfg = read_json(self.project / "project.json")
        cfg["frame"] = {"header_file": "another-header.md"}
        write_json(self.project / "project.json", cfg)
        with self.assertRaises(cc.PreparationNeeded):
            cc.act(self.project)

    def test_scope_changes_after_acceptance_invalidate_chat_acceptance(self):
        self.review()
        self.finish()
        path = self.frame / "header.md"
        path.write_text(read_text(path).replace("**Cohort:** Adult men", "**Cohort:** Older men"), encoding="utf-8")
        self.assertFalse(fg.accepted(self.project)[0])

    def test_full_draft_revision_can_correct_scope_before_acceptance(self):
        self.review()
        revised = self.tmp / "proposal.md"
        revised.write_text(read_text(self.draft).replace("**Cohort:** Adult men", "**Cohort:** Older men"), encoding="utf-8")
        self.send("revise", text="Use older men as the target group.", draft_file=str(revised))
        self.finish()
        self.assertIn("**Cohort:** Older men", read_text(self.frame / "header.md"))
        self.assertTrue(fg.accepted(self.project)[0])

    def test_model_assisted_options_reuse_forecasts_without_claiming_a_result(self):
        model = FakeModel()
        self.options("A1-H1", model)
        self.assertGreater(len(self.current["options"]), 1)
        self.assertEqual(self.current["options"][0]["forecast"]["ok"], fg.FORECAST_CALLS)
        self.send("select", choice=0, model=model)
        self.finish()
        rec = fg.load_certificate(self.project)["axes"]["A1"]
        self.assertTrue(rec["forecast"]["ok"])
        self.assertEqual(rec["judge"]["match"], True)
        self.assertTrue(any(tag.startswith("forecast:") for tag in model.tags))

    def test_selected_alternative_is_the_context_shown_during_wording_review(self):
        self.options("A1-H1", FakeModel())
        proposed = self.current["options"][1]
        self.send("select", text="Use the clearer wording.", choice=1)
        self.assertEqual(self.current["comparison"]["question"], proposed["question"])
        self.assertEqual(self.current["show"]["explanation"], proposed["statements"]["A1-H1"])

    def test_assistant_can_submit_a_normal_chat_reply_through_the_cli(self):
        self.start()
        data = {**self.current["next_request"]["base_payload"], "text": "I want a comparison guide for discussing the research."}
        path = self.tmp / "reply.json"
        write_json(path, data)
        out = io.StringIO()
        with patch.object(fg, "Terminal", side_effect=AssertionError("No terminal")), contextlib.redirect_stdout(out):
            code = cli.main(["coach", str(self.project), "--action", "reply", "--response-file", str(path)])
        self.assertEqual(code, 0, out.getvalue())
        self.assertEqual(json.loads(out.getvalue())["step"], "preference")

    def test_model_failure_keeps_original_wording_and_discloses_missing_forecast(self):
        model = lambda *args: (_ for _ in ()).throw(RuntimeError("Model unavailable"))
        self.options("A1-H1", model)
        self.assertEqual(len(self.current["options"]), 1)
        self.assertEqual(self.current["options"][0]["forecast"]["ok"], 0)
        self.send("select", choice=0, model=model)
        self.finish()
        self.assertIn("No forecast could be made", read_text(self.frame / fg.CERT_MD))

    def test_multiple_questions_commit_separately_and_resume(self):
        text = read_text(self.draft)
        self.draft.write_text(text + "\n" + text.replace("A1", "A2").replace("axis one", "axis two"), encoding="utf-8")
        self.review()
        self.assertEqual(self.finish()["step"], "preference")
        self.assertFalse(fg.accepted(self.project)[0])
        self.assertIn("A1", fg.load_certificate(self.project)["axes"])
        self.send(text="No preference", choice=None)
        self.send(text="I want to understand the second comparison too.")
        self.send(text="I would accept whatever the sources support.")
        self.send("prepare")
        self.send("select", choice=0)
        self.assertEqual(self.finish()["status"], "completed")
        self.assertTrue(fg.accepted(self.project)[0])

    def test_default_commands_never_open_a_terminal_interview(self):
        for alias in ("coach", "sign"):
            out = io.StringIO()
            with patch.object(fg, "Terminal", side_effect=AssertionError("No terminal")), \
                    patch.object(fg, "model_for", side_effect=AssertionError("No API")), contextlib.redirect_stdout(out):
                code = cli.main([alias, str(self.project)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out.getvalue())["step"], "purpose")

    def test_missing_draft_is_a_plain_repair_task_not_a_raw_header_error(self):
        self.draft.unlink()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cli.main(["coach", str(self.project)])
        self.assertEqual(code, 2)
        result = json.loads(out.getvalue())
        self.assertEqual(result["status"], "needs_preparation")
        self.assertNotIn("header", result["message"])
        self.assertFalse((self.frame / fg.CERT_JSON).exists())

    def test_axis_heading_variants_and_unambiguous_single_axis_layout(self):
        text = read_text(self.draft)
        for heading, aid in (("Axis A1", "A1"), ("Axis 10", "A10")):
            with self.subTest(heading=heading):
                adapted = text.replace("axis one", heading).replace("A1-", aid + "-")
                normalized = cc.normalize_draft(adapted)
                self.assertIn(aid, fg.axis_spans(normalized))
                self.assertTrue(onramp.check_header(normalized)[0])
        headless = text.replace("### **axis one:**\n", "")
        self.assertFalse(onramp.check_header(headless)[0])
        repaired = cc.normalize_draft(headless, "Does compound Z improve flow in the studied population?")
        self.assertEqual([h["statement"] for h in parse_header(repaired)["axes"][0]["hypotheses"]],
                         [h["statement"] for h in parse_header(text)["axes"][0]["hypotheses"]])
        self.assertTrue(onramp.check_header(repaired)[0])

    def test_configured_paths_and_previous_header_backup_are_respected(self):
        custom = self.project / "custom"
        custom.mkdir()
        shutil.copyfile(FIX / "index.md", custom / "map.md")
        shutil.copyfile(self.draft, custom / "question.md")
        prior = (custom / "question.md").read_bytes()
        cfg = read_json(self.project / "project.json")
        cfg["frame"] = {"header_file": "custom/question.md", "index_file": "custom/map.md"}
        write_json(self.project / "project.json", cfg)
        self.review()
        self.finish()
        self.assertTrue(fg.accepted(self.project)[0])
        backups = list((self.project / "99_ARCHIVE").rglob("question.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), prior)
        self.assertFalse((self.frame / "header.md").exists())


if __name__ == "__main__":
    unittest.main()
