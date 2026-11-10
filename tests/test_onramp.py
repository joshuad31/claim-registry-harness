"""The new-user path end to end: cr new -> cr frame -> cr approve -> cr doctor -> cr quest -> report."""

import io
import shutil
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fakes  # noqa: E402
from claimreg import onramp  # noqa: E402
from claimreg.cli import main  # noqa: E402
from claimreg.util import read_json, write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402
from test_relay import FakeDriver, Script  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "mini"
NOTEBOOK = "https://notebook.google.com/notebook/00000000-0000-0000-0000-000000000000"


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = main(argv)
    return rc, out.getvalue() + err.getvalue()


class OnrampTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("onramp")
        fakes.reset()
        self.drivers = []
        self.keys = self.tmp / "keys"
        self.keys.mkdir()
        for n in ("deepseek API key.txt", "chatgpt api key.txt", "New ChatGPT API key.txt", "notes.txt"):
            (self.keys / n).write_text("sk-test-not-a-real-key", encoding="utf-8")
        self.proj = self.tmp / "LEVO"

    def tearDown(self):
        for d in self.drivers:
            d.halt = True
        cleanup(self.tmp)

    def test_keys_are_found_by_file_name_only(self):
        found = onramp.find_keys(self.keys)
        self.assertEqual(set(found), {"deepseek", "openai"})
        names, blocks = onramp.choose_providers(self.keys, [], ["deepseek", "openai"])
        self.assertEqual(names, ["deepseek", "openai"])
        self.assertTrue(blocks["openai"]["api_key_file"].endswith(".txt"))
        self.assertNotIn("sk-test", str(blocks))                      # the key itself is never copied

    def test_model_pick_prefers_listed_models(self):
        self.assertEqual(onramp.pick_model("openai", ["gpt-4o", "gpt-5.2", "gpt-5.5"]), "gpt-5.2")
        self.assertEqual(onramp.pick_model("deepseek", ["deepseek-reasoner", "deepseek-chat"]), "deepseek-chat")
        self.assertIsNone(onramp.pick_model("openai", ["text-embedding-3"]))

    def test_new_frame_approve_doctor_quest_report(self):
        rc, out = run(["new", str(self.proj), "--name", "Levo test", "--corpus", str(FIX / "sources"),
                       "--keys", str(self.keys), "--notebook", NOTEBOOK])
        self.assertEqual(rc, 0, out)
        cfg = read_json(self.proj / "project.json")
        self.assertEqual(cfg["default_provider"], ["openai", "deepseek"])
        self.assertEqual(cfg["notebooklm"]["notebooks"], [NOTEBOOK])
        self.assertTrue((self.proj / "01_CORPUS" / "manifests" / "CURRENT.json").exists())
        self.assertIn("openai (gpt-5.2) -> deepseek (deepseek-chat)", out)

        # the template must be filled in before anything is drafted
        rc, out = run(["frame", str(self.proj)])
        self.assertEqual(rc, 2)
        self.assertIn("REPLACE", out)
        (self.proj / "01_FRAME" / "question.md").write_text(
            "# Question\nDoes compound Z improve outcome Y?\n## Hypotheses\n1. It does.\n2. It does not.\n",
            encoding="utf-8")

        # from here on the model roles are scripted (no network in tests)
        quest_script = Script()
        header = (FIX / "header.md").read_text(encoding="utf-8")

        def script(req, prov):
            if req.role == "indexer":
                return {"filename": req.meta["filename"], "rank": "A", "author_year_title": "t", "relevance": "r",
                        "summary": "s", "contradictions_and_gaps": "none"}
            if req.role == "archivist_writer":
                return "You are a precision researcher working from a fixed notebook.\nOUTPUT:\n* Cite sources."
            if req.role == "investigator":
                return header + "\n=====COORDINATOR=====\nhandoff"
            return quest_script(req, prov)
        fakes.SCRIPTS["s"] = script
        cfg["providers"] = {"scripted": {"type": "scripted", "model": "scripted-1", "script": "s"}}
        cfg["default_provider"] = "mock"
        cfg["roles"] = {r: "scripted" for r in ("indexer", "archivist_writer", "investigator", "quest_manager",
                                                 "quest_investigator")}
        cfg["quest"] = {"round_size": 3, "max_rounds": 4}
        write_json(self.proj / "project.json", cfg)

        rc, out = run(["frame", str(self.proj)])
        self.assertEqual(rc, 0, out)
        for f in ("index.md", "archivist-custom-prompt.txt", "header-DRAFT.md", "coordinator-handoff-DRAFT.md"):
            self.assertTrue((self.proj / "01_FRAME" / f).exists(), f)
        self.assertFalse((self.proj / "01_FRAME" / "header.md").exists())      # a draft is not an approval
        self.assertIn("smith2020.md", (self.proj / "01_FRAME" / "index.md").read_text())

        rc, out = run(["quest", str(self.proj)])
        self.assertEqual(rc, 2)                                             # no approved header yet
        rc, out = run(["approve", str(self.proj), "--by", "Test Person"])
        self.assertEqual(rc, 0, out)
        self.assertIn("Test Person", read_json(self.proj / "project.json")["frame"]["approval_note"])

        rc, out = run(["doctor", str(self.proj), "--offline"])
        self.assertEqual(rc, 0, out)
        self.assertIn("[PASS] Header approved and parsed", out)
        self.assertIn("1 notebook link(s) saved", out)

        # the quest: pre-seed fast timings, stand in for the browser driver, then run for real
        q = self.proj / "quest" / "T1"
        (q / "answers" / "queue").mkdir(parents=True)
        write_json(q / "quest.json", {
            "run_id": "LEVO-T1", "project": "../..", "notebooks": {"primary": NOTEBOOK}, "answers_dir": "answers",
            "assessed_file": "answers/assessed-qids.json", "round_size": 6, "max_questions": 12, "queue_ahead": 6,
            "poll_seconds": 0.02, "max_wait_seconds": 5, "drain_minutes": 0.05, "max_hours": 1,
            "investigator_min_interval": 0})
        d = FakeDriver(q / "answers")
        self.drivers.append(d)
        d.start()
        rc, out = run(["quest", str(self.proj), "--id", "T1", "--no-driver", "--then-run"])
        self.assertEqual(rc, 0, out[-3000:])
        self.assertIn("Quest imported as run", out)
        self.assertTrue((q / "CLOSEOUT.md").exists())
        runs = [p for p in (self.proj / "02_RUNS").iterdir() if p.is_dir()]
        self.assertEqual(len(runs), 1)
        st = read_json(runs[0] / "00_RUN-CONTROL" / "stage-state.json")
        self.assertEqual(st["quest"]["status"], "imported")
        self.assertEqual(st["report"]["status"], "done")
        self.assertTrue((runs[0] / "10_REPORTS" / "CRUX-REPORT.md").exists())
        self.assertTrue((runs[0] / "08_COVERAGE" / "PREMISE-LEDGER.md").exists())
        self.assertEqual(len(read_json(runs[0] / "02_DISCOVERY" / "01_issued-questions" / "questions.json")), 12)


if __name__ == "__main__":
    unittest.main()
