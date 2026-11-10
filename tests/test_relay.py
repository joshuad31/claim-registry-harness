"""The quest relay with scripted model roles and a stand-in driver: rounds, pacing, firewall,
information barrier, provider failover, repairs, restart safety and the closeout."""

import json
import re
import sys
import threading
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fakes  # noqa: E402
from claimreg.llm.base import LLMResponse  # noqa: E402
from claimreg.notebooklm import relay as relay_mod  # noqa: E402
from claimreg.notebooklm.relay import Relay, assessment_problem, packet_problem  # noqa: E402
from claimreg.notebooklm.relay import read_json, write_json  # noqa: E402  (tolerate Windows file locking)
from scratch import cleanup, scratch_dir  # noqa: E402
from test_pipeline_mock import make_project  # noqa: E402

SOURCES = ["smith2020.md", "jones2021.md", "lee2019.md", "park2018.md"]
SECRET = "PRIVATE-STATE-SENTINEL-7731"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class FakeDriver(threading.Thread):
    """Answers queue files like the NotebookLM driver does, including backlog pacing and STOP."""

    def __init__(self, answers: Path, max_backlog=12, bad=(), tool_output=()):
        super().__init__(daemon=True)
        self.answers, self.queue = answers, answers / "queue"
        self.max_backlog, self.bad, self.tool_output = max_backlog, set(bad), set(tool_output)
        self.pushed, self.max_seen_backlog, self.halt = [], 0, False

    def run(self):
        while not self.halt:
            stop = (self.queue / "STOP").exists()
            saved = {f.name.split("-")[0] for f in self.answers.glob("Q*-A*.json")}
            assessed = set((read_json(self.answers / "assessed-qids.json", default={}) or {}).get("assessed", []))
            backlog = len(saved - assessed)
            self.max_seen_backlog = max(self.max_seen_backlog, backlog)
            if not stop and backlog < self.max_backlog:
                for f in sorted(self.queue.glob("Q*.json")):
                    if f.name in self.pushed:
                        continue
                    # the relay may be writing/replacing queue files at the same time; on Windows a
                    # transient PermissionError must not kill the stand-in driver thread
                    try:
                        j = json.loads(f.read_text(encoding="utf-8"))
                    except (OSError, ValueError):
                        continue
                    self.pushed.append(f.name)
                    write_json(self.answers / "driver-state.json", {"pushed": self.pushed})
                    att = j.get("attempt", "A01")
                    key = f"{j['qid']}-{att}"
                    names = re.findall(r"[a-z0-9]+\.md", j["text"])
                    body = ("Outline. " + " ".join(f"The source reports a measured effect ({n}, Results)." for n in names)
                            + " detail" * 120)
                    if key in self.tool_output:
                        body = "Tool response for file_read: exit_code: 0 " + body
                    rec = {"run_id": "T", "qid": j["qid"], "attempt": att, "lane": "primary", "query": j["text"],
                           "submitted_at": now(), "captured_at": now(),
                           "outcome": "INCOMPLETE" if key in self.bad else "COMPLETE",
                           "answer": "Assessing..." if key in self.bad else body,
                           "contains_tool_output": key in self.tool_output, "requested_sources": names,
                           "answer_names_requested_source": key not in self.bad, "generation_seconds": 1}
                    write_json(self.answers / f"{key}.json", rec)
                    break
            write_json(self.answers / "driver-status.json",
                       {"at": now(), "feed": "STOP" if stop else "idle", "lanes": {"primary": {"state": "FREE"}}})
            time.sleep(0.01)


def question(i, n_sources=1):
    names = [SOURCES[(i + k) % 4] for k in range(n_sources)]
    tail = " Answer in about 900 words or more." if n_sources == 1 else ""
    return (f"Using {' and '.join(names)}, report design item {i}, each measured effect with variance, and put "
            f"(exact source filename, actual section heading) beside each number.{tail}")


def assessment(round_id, vectors=None, direction="CONTINUE", stop=False, repairs=()):
    return (f"<<<FRAGMENT\nnew cards for {round_id}\nFRAGMENT>>>\n<<<STATE\n{SECRET} "
            + "state word " * 40 + f"\nSTATE>>>\n<<<JSON\n"
            + json.dumps({"round": round_id, "vectors": vectors or {"A1": {"H1": 30, "H2": 14, "H3": 20}},
                          "stop_eligible": stop, "direction": direction, "repairs": list(repairs)})
            + "\nJSON>>>")


def packet(round_id, start):
    qs = "\n".join(f"{k + 1}. [target: functional link] {question(start + k, 1 + k % 2)}" for k in range(8))
    return (f"# {round_id} feedback packet\n\n**Direction: CONTINUE**\n\n## Novelty notes\n- new\n\n"
            f"## Open priorities\n1. gap\n\n## Answers needing a repair re-ask\nNone\n\n## Ready questions\n{qs}\n")


class Script:
    """A scripted Manager + Investigator.  Counters make every question distinct."""

    def __init__(self, stop_at_round=None, repairs_in=None):
        self.n = 100
        self.inv_prompts, self.assess_calls, self.packet_calls = [], [], []
        self.stop_at_round, self.repairs_in = stop_at_round, repairs_in or {}

    def __call__(self, req, prov):
        if req.role == "quest_investigator":
            self.inv_prompts.append(req.system + req.user)
            k = int(re.search(r"Write the next (\d+) questions", req.user).group(1))
            self.n += k
            return {"questions": [{"target": "exposure", "sources": [], "text": question(self.n + i, 1 + i % 2)}
                                  for i in range(k)]}
        rid = req.meta["round"]
        if req.tag.startswith("assess"):
            self.assess_calls.append((rid, req.meta["members"]))
            stop = self.stop_at_round == rid
            return assessment(rid, direction="STOP" if stop else "CONTINUE", stop=stop,
                              repairs=self.repairs_in.get(rid, ()))
        self.packet_calls.append(rid)
        self.n += 10
        return packet(rid, self.n)


class RelayTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("relay")
        fakes.reset()
        self.drivers = []

    def tearDown(self):
        for d in self.drivers:
            d.halt = True
        cleanup(self.tmp)

    def make(self, scripts, roles=None, quest=None, driver=None):
        fakes.SCRIPTS.update(scripts)
        proj = make_project(self.tmp, extra={
            "roles": roles or {"quest_manager": "m", "quest_investigator": "m"},
            "providers": {n: {"type": "scripted", "model": f"model-{n}", "script": n} for n in scripts},
            "budget": {"retries": 0, "concurrency": 2}})
        q = proj / "quest" / "Q1"
        q.mkdir(parents=True)
        cfg = {"run_id": "T-QUEST", "project": "../..", "answers_dir": "answers",
               "assessed_file": "answers/assessed-qids.json", "notebooks": {"primary": "https://x/notebook/abc"},
               "round_size": 6, "max_questions": 18, "queue_ahead": 6, "poll_seconds": 0.02,
               "max_wait_seconds": 5, "drain_minutes": 0.05, "max_hours": 1, "investigator_min_interval": 0}
        cfg.update(quest or {})
        write_json(q / "quest.json", cfg)
        r = Relay(q / "quest.json", echo=False)
        d = FakeDriver(r.answers, **(driver or {}))
        self.drivers.append(d)
        d.start()
        return r, d

    def test_full_quest_grades_everything_and_closes(self):
        s = Script()
        # the Investigator opens; after that it waits long enough for the Manager's packets to arrive
        r, d = self.make({"m": s}, quest={"investigator_min_interval": 4})
        st = r.run(max_seconds=60)
        led = read_json(r.ledger_path)["assessments"]
        self.assertEqual(st["questions_asked"], 18)
        self.assertEqual(st["answers_graded"], 18)
        self.assertEqual(st["grading_backlog"], 0)
        self.assertEqual([a["assessment_id"] for a in led], ["R001", "R002", "R003"])
        self.assertTrue(all(len(a["members"]) == 6 for a in led))
        graded = [m["qid"] for a in led for m in a["members"]]
        self.assertEqual(len(graded), len(set(graded)))                       # nothing graded twice
        self.assertIn("question limit", st["stopping"])
        self.assertTrue((r.queue / "STOP").exists())
        # pacing file and scorecard inputs
        assessed = read_json(r.assessed_path)
        self.assertEqual(len(assessed["assessed"]), 18)
        self.assertEqual(set(assessed["times"]), set(assessed["assessed"]))
        self.assertLessEqual(d.max_seen_backlog, 12)
        # records
        self.assertTrue((r.private / "state" / "R003.md").exists())
        self.assertEqual((r.private / "record.md").read_text().count("new cards for"), 3)
        self.assertTrue((r.ws / "packets" / "R001.md").exists())
        self.assertIn("operational closeout", (r.q / "CLOSEOUT.md").read_text())
        self.assertTrue((r.q / "SCORECARD.txt").exists())
        self.assertTrue(read_json(r.answers / "quest-clock.json")["go_ahead"])
        # the opening batch came from the Investigator, later questions from the Manager's packets
        origins = [json.loads(x)["origin"] for x in (r.q / "asked.jsonl").read_text().splitlines()]
        self.assertEqual(origins[0], "investigator")
        self.assertTrue(any(o.startswith("packet R001") for o in origins))

    def test_investigator_never_sees_private_state(self):
        s = Script()
        # no packets are accepted, so the Investigator has to write every batch
        r, d = self.make({"m": s})
        orig = s.__call__

        def no_packets(req, prov):
            if req.tag.startswith("packet"):
                return "no ready section here"
            return orig(req, prov)
        fakes.SCRIPTS["m"] = no_packets
        r.run(max_seconds=60)
        self.assertGreaterEqual(len(s.inv_prompts), 2)
        self.assertTrue((r.private / "state.md").read_text().startswith(SECRET))
        for p in s.inv_prompts:
            self.assertNotIn(SECRET, p)
            self.assertNotIn("vectors", p)
            self.assertNotIn("new cards for", p)

    def test_manager_refusal_fails_over_and_the_quest_continues(self):
        s = Script()

        def refusing(req, prov):
            return LLMResponse(text="", finish_reason="content_filter")
        r, d = self.make({"a": refusing, "b": s},
                         roles={"quest_manager": ["a", "b"], "quest_investigator": ["a", "b"]},
                         quest={"max_questions": 12})
        st = r.run(max_seconds=60)
        self.assertEqual(st["answers_graded"], 12)
        self.assertGreater(st["failovers"], 0)
        led = read_json(r.ledger_path)["assessments"]
        self.assertTrue(all(a["provider"] == "b" and a["failover"][0]["provider"] == "a" for a in led))
        self.assertIn("after failover", st["providers_last_used"]["quest_manager"])

    def test_firewall_refuses_bad_questions(self):
        s = Script()
        bad = ["Using smith2020.md, give a brief answer in 900 words or less.",          # length ceiling
               "Using nosuchfile2020.md, report the design.",                               # not in the index
               "Using smith2020.md and lee2019.md, test H1 against H2.",                    # jargon
               "Report everything about the drug.",                                         # no filename
               "Using smith2020.md and lee2019.md, report the design. Answer in about 900 words or more."]
        r, d = self.make({"m": s})
        for b in bad:
            self.assertIsNone(r.enqueue(b, "test"), b)
        ok = "Using smith2020.md, report the percentage change in the primary endpoint with its variance."
        self.assertEqual(r.enqueue(ok, "test"), "Q0001")
        self.assertIsNone(r.enqueue(ok.upper(), "test"))                               # duplicate, normalized
        rej = (r.q / "rejected.jsonl").read_text().splitlines()
        self.assertEqual(len(rej), 6)

    def test_failed_and_tool_output_answers_are_re_asked_once(self):
        s = Script(repairs_in={"R001": [{"qid": "Q0003", "reason": "numbers conflict with the table"}]})
        r, d = self.make({"m": s}, quest={"max_questions": 12},
                         driver={"bad": {"Q0001-A01"}, "tool_output": {"Q0002-A01"}})
        st = r.run(max_seconds=60)
        names = {f.name for f in r.answers.glob("Q*-A02.json")}
        self.assertEqual(names, {"Q0001-A02.json", "Q0002-A02.json", "Q0003-A02.json"})
        self.assertFalse(list(r.answers.glob("Q*-A03.json")))
        self.assertEqual(st["answers_graded"], 12)                                  # Q0001 graded on its repair
        led = read_json(r.ledger_path)["assessments"]
        m = {x["qid"]: x["attempt"] for a in led for x in a["members"]}
        self.assertEqual(m["Q0001"], "A02")
        self.assertIn("Q0001-A02", (r.q / "CLOSEOUT.md").read_text())

    def test_restart_does_not_regrade_or_reset_the_clock(self):
        s = Script()
        r, d = self.make({"m": s}, quest={"max_questions": 12})
        r.run(max_seconds=60)
        clock = read_json(r.answers / "quest-clock.json")["go_ahead"]
        led1 = read_json(r.ledger_path)["assessments"]
        # simulate a crash between the ledger append and the pacing sync
        (r.assessed_path).unlink()
        (r.queue / "STOP").unlink()
        calls_before = len(s.assess_calls)
        r2 = Relay(r.cfg_path, echo=False)
        st = r2.run(max_seconds=60)
        self.assertEqual(read_json(r2.answers / "quest-clock.json")["go_ahead"], clock)
        self.assertEqual(read_json(r2.ledger_path)["assessments"], led1)
        self.assertEqual(len(s.assess_calls), calls_before)
        self.assertEqual(len(read_json(r2.assessed_path)["assessed"]), 12)
        self.assertEqual(st["answers_graded"], 12)

    def test_manager_stop_is_recorded_as_scientific(self):
        s = Script(stop_at_round="R002")
        r, d = self.make({"m": s}, quest={"max_questions": 60})
        st = r.run(max_seconds=60)
        self.assertIn("Manager directed STOP", st["stopping"])
        self.assertIn("Scientific stop", (r.q / "CLOSEOUT.md").read_text())
        self.assertLess(st["questions_asked"], 60)
        self.assertEqual(st["grading_backlog"], 0)

    def test_malformed_assessment_is_repaired_once_then_committed(self):
        s = Script()
        seen = {"n": 0}

        def flaky(req, prov):
            if req.tag.startswith("assess") and not req.tag.endswith(":repair"):
                seen["n"] += 1
                return assessment(req.meta["round"], vectors={"A1": {"H1": 30, "H2": 14, "H3": 19}})   # sums to 63
            return s(req, prov)
        r, d = self.make({"m": flaky}, quest={"max_questions": 6})
        st = r.run(max_seconds=60)
        self.assertEqual(st["answers_graded"], 6)
        self.assertEqual(sum(read_json(r.ledger_path)["assessments"][0]["vectors"]["A1"].values()), 64)

    def test_validators(self):
        self.assertEqual(assessment_problem(assessment("R001"), 64, ["A1"]), "")
        self.assertIn("sums to 63", assessment_problem(
            assessment("R001", vectors={"A1": {"H1": 63}}), 64, ["A1"]))
        self.assertIn("STATE", assessment_problem("<<<FRAGMENT\nx\nFRAGMENT>>>", 64, ["A1"]))
        self.assertEqual(packet_problem(packet("R001", 1)), "")
        self.assertIn("private assessment vocabulary", packet_problem(packet("R001", 1) + "\nH1 leads 40/64"))
        self.assertIn("Ready questions", packet_problem("# packet\nnothing"))


if __name__ == "__main__":
    unittest.main()
