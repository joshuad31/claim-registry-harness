"""The new-user path end to end: cr new -> cr frame -> cr approve -> cr doctor -> cr quest -> report."""

import io
import shutil
import sys
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

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

    def test_doctor_flags_a_typoed_notebook_link(self):
        # the 2026-11-10 failure: one typo in a link silently cost one lane for the whole quest
        bad = "https://notebook.gooogle.com/notebook/00000000-0000-0000-0000-000000000000"
        rc, out = run(["new", str(self.proj), "--notebook", bad])
        self.assertEqual(rc, 0, out)
        rc, out = run(["doctor", str(self.proj), "--offline"])
        self.assertEqual(rc, 2, out)
        self.assertIn("NotebookLM: 1 notebook link(s) saved", out)      # the cheap count line is unchanged
        self.assertIn("[FAIL] notebook 1: link is not usable", out)
        self.assertIn("the host is not notebook.google.com or notebooklm.google.com", out)

    def test_doctor_online_notebook_check_is_opt_in(self):
        rc, out = run(["new", str(self.proj), "--notebook", NOTEBOOK])
        self.assertEqual(rc, 0, out)
        args = SimpleNamespace(project=str(self.proj), offline=False, fix=False, models=False, notebooks=True)
        calls: list[list[str]] = []

        def fake_online(links, profile):
            calls.append(list(links))
            return [(True, "title: LEVO notebook")]

        with mock.patch.object(onramp, "check_notebooks_online", fake_online):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                rc = onramp.cmd_doctor(args)
        text = out.getvalue() + err.getvalue()
        self.assertEqual(rc, 2)                     # no corpus/header yet; the notebook link itself is fine
        self.assertEqual(calls, [[NOTEBOOK]])
        self.assertIn("[PASS] notebook 1: opens in NotebookLM", text)
        self.assertIn("title: LEVO notebook", text)

        # --offline: the same link is checked offline and never opened
        args.offline = True
        with mock.patch.object(onramp, "check_notebooks_online", fake_online):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                onramp.cmd_doctor(args)
        text = out.getvalue() + err.getvalue()
        self.assertIn("[PASS] notebook 1: link looks valid", text)
        self.assertEqual(len(calls), 1)

        # Playwright missing: WARN and the offline structural row, never a crash
        args.offline = False
        with mock.patch.object(onramp, "check_notebooks_online", lambda links, profile: None):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                onramp.cmd_doctor(args)
        text = out.getvalue() + err.getvalue()
        self.assertIn("[WARN] notebook online check skipped", text)
        self.assertIn("[PASS] notebook 1: link looks valid", text)

    def test_quest_refuses_to_start_the_relay_when_a_lane_never_comes_up(self):
        rc, out = run(["new", str(self.proj), "--notebook", NOTEBOOK])
        self.assertEqual(rc, 0, out)
        (self.proj / "01_FRAME" / "header.md").write_text("# header\n", encoding="utf-8")
        profile = self.tmp / "profile"
        profile.mkdir()
        (profile / "keep.txt").write_text("signed in", encoding="utf-8")
        args = SimpleNamespace(project=str(self.proj), id=None, new=False, notebook=[], hours="1",
                               max_questions="10", profile=str(profile), no_driver=False, then_run=False)
        starts, stops = [], []

        class FakeProc:
            """A driver process that starts and immediately exits: one lane never opened."""

            def __init__(self, argv, cwd=None, stdout=None, stderr=None, env=None):
                starts.append({"argv": argv, "env": env})

            def poll(self):
                return 1

            def terminate(self):
                stops.append("terminate")

            def wait(self, timeout=None):
                return 1

        with mock.patch.object(onramp, "check_header", lambda text: (True, "parsed")), \
                mock.patch.object(onramp.subprocess, "Popen", FakeProc):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                rc = onramp.cmd_quest(args)
        text = out.getvalue() + err.getvalue()
        self.assertEqual(rc, 2)
        self.assertEqual(len(starts), 1)
        self.assertEqual(starts[0]["env"]["PYTHONUNBUFFERED"], "1")
        self.assertIn("claimreg.notebooklm.driver", starts[0]["argv"])
        self.assertEqual(stops, ["terminate"])
        self.assertIn("Keep the driver's Chrome window unminimized", text)
        self.assertIn("only 0 of 1 notebook lane(s) came up", text)
        self.assertIn("driver.log", text)
        quests = [d for d in (self.proj / "quest").iterdir() if d.is_dir()]
        self.assertEqual(len(quests), 1)
        self.assertFalse((quests[0] / "relay-status.json").exists())     # the relay never started
        clock = quests[0] / "answers" / "quest-clock.json"
        self.assertFalse((read_json(clock, default={}) or {}).get("go_ahead"),
                         "a failed preflight must not stamp the go-ahead clock")

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
        self.assertIn("[PASS] notebook 1: link looks valid", out)

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
        # one evidence database per axis: the report is in the axis folder
        self.assertTrue(list(runs[0].glob("AXIS-*/10_REPORTS/CRUX-REPORT.md")))
        self.assertTrue(list(runs[0].glob("AXIS-*/08_COVERAGE/PREMISE-LEDGER.md")))
        filed = list(runs[0].glob("AXIS-*/02_DISCOVERY/01_issued-questions/questions.json"))
        self.assertEqual(sum(len(read_json(f)) for f in filed), 12)
        self.assertFalse((runs[0] / "02_DISCOVERY").exists())          # nothing is kept outside an axis or SHARED


class NotebookLinkTest(unittest.TestCase):
    """`cr doctor` validates every saved notebook link, not just counts them."""

    def test_usable_links_pass(self):
        links = [NOTEBOOK,
                 "https://notebooklm.google.com/notebook/3b728d29-628f-4c3e-9b0d-ce485d37d24a",
                 "https://notebooklm.google.com/notebook/4ffdb7f0-b402-4f08-92da-ab34503a9f01/",
                 "https://notebook.google.com/notebook/5c481b42-32cd-4f53-bec9-4f11b664282f?authuser=1"]
        self.assertEqual(onramp.notebook_link_problems(links), [])
        self.assertEqual(onramp.notebook_link_problems([]), [])

    def test_each_kind_of_bad_link_is_named_with_its_index(self):
        cases = {
            "wrong host": ("https://notebook.gooogle.com/notebook/00000000-0000-0000-0000-000000000000", "host"),
            "no /notebook/ path": ("https://notebooklm.google.com/00000000-0000-0000-0000-000000000000", "/notebook/"),
            "malformed id": ("https://notebooklm.google.com/notebook/short-id", "not plausible"),
            "not https": ("http://notebooklm.google.com/notebook/00000000-0000-0000-0000-100000000000", "https"),
        }
        for name, (link, needle) in cases.items():
            problems = onramp.notebook_link_problems([link])
            self.assertEqual(len(problems), 1, name)
            self.assertEqual(problems[0][0], 1, name)
            self.assertIn(needle, problems[0][1], name)

    def test_a_duplicated_id_is_reported_on_the_later_link(self):
        clone = "https://notebooklm.google.com/notebook/00000000-0000-0000-0000-000000000000?authuser=2"
        problems = onramp.notebook_link_problems([NOTEBOOK, clone])
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0][0], 2)
        self.assertIn("duplicate of notebook 1", problems[0][1])

    def test_an_opened_notebook_page_is_recognised(self):
        url = "https://notebooklm.google.com/notebook/3b728d29-628f-4c3e-9b0d-ce485d37d24a"
        self.assertIsNone(onramp._notebook_page_problem("NotebookLM", url, "Sources 4  Chat  Studio"))
        self.assertIn("couldn't find", onramp._notebook_page_problem(
            "NotebookLM", url, "Couldn't find that notebook"))
        self.assertIn("request access", onramp._notebook_page_problem(
            "NotebookLM", url, "You need permission. Request access."))
        self.assertIn("not a notebook URL", onramp._notebook_page_problem(
            "Sign in", "https://accounts.google.com/signin", ""))


class _Proc:
    """Stands in for the driver subprocess: poll() is None while alive, the exit code once it ends."""

    def __init__(self, rc=None):
        self.rc = rc

    def poll(self):
        return self.rc


class DriverPreflightTest(unittest.TestCase):
    """`cr quest` waits for every configured lane to report ready before it starts the relay."""

    def setUp(self):
        self.tmp = scratch_dir("preflight")
        self.log = self.tmp / "driver.log"

    def tearDown(self):
        cleanup(self.tmp)

    def test_ready_lines_are_parsed_and_other_lines_ignored(self):
        text = ("NotebookLM driver starting for 6 lanes\nlane primary ready\n"
                "lane clone-1 ready - recovered 3 saved answers\nlane clone-2: reloading\n"
                "lane clone-3 ready\n")
        self.assertEqual(onramp._ready_lanes(text), {"primary", "clone-1", "clone-3"})

    def test_all_lanes_up_passes(self):
        self.log.write_text("".join(f"lane {n} ready\n" for n in ("primary", "clone-1")), encoding="utf-8")
        ready, ok, tail = onramp._preflight_lanes(_Proc(), self.log, 2, timeout=1, poll=0.01)
        self.assertTrue(ok)
        self.assertEqual(ready, {"primary", "clone-1"})
        self.assertIn("lane clone-1 ready", "\n".join(tail))

    def test_lines_from_a_previous_run_do_not_pass_a_resumed_quest(self):
        old = "".join(f"lane clone-{n} ready\n" for n in range(3))
        self.log.write_text(old, encoding="utf-8")
        ready, ok, _tail = onramp._preflight_lanes(_Proc(0), self.log, 3, timeout=1, poll=0.01,
                                                   start_lines=old.count("\n"))
        self.assertFalse(ok)
        self.assertEqual(ready, set())

    def test_a_driver_that_exits_is_a_shortfall_with_the_log_tail(self):
        self.log.write_text("lane primary ready\nTraceback (most recent call last):\n"
                            "playwright._impl._errors.TimeoutError: page.goto: Timeout 45000ms exceeded\n",
                            encoding="utf-8")
        ready, ok, tail = onramp._preflight_lanes(_Proc(1), self.log, 3, timeout=5, poll=0.01)
        self.assertFalse(ok)
        self.assertEqual(ready, {"primary"})
        self.assertIn("page.goto: Timeout", "\n".join(tail))

    def test_the_timeout_is_a_shortfall_not_a_hang(self):
        self.log.write_text("lane primary ready\n", encoding="utf-8")
        started = time.time()
        ready, ok, _tail = onramp._preflight_lanes(_Proc(), self.log, 3, timeout=0.1, poll=0.01)
        self.assertLess(time.time() - started, 5)
        self.assertFalse(ok)
        self.assertEqual(ready, {"primary"})

    def test_the_driver_environment_is_unbuffered(self):
        env = onramp._driver_env({"PATH": "C:\\bin"})
        self.assertEqual(env["PYTHONUNBUFFERED"], "1")
        self.assertEqual(env["PATH"], "C:\\bin")


if __name__ == "__main__":
    unittest.main()
