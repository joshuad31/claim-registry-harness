"""The frame coach: the researcher sets the frame knowingly, and accepts the likely outcome before the quest."""

import io
import re
import shutil
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg import frame_gate as fg  # noqa: E402
from claimreg import onramp  # noqa: E402
from claimreg.cli import main  # noqa: E402
from claimreg.header import parse_header  # noqa: E402
from claimreg.util import read_json, read_text, write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "mini"

RESTATED = {
    "question": "Should adult men with bladder outlet obstruction be offered compound Z to improve urinary flow?",
    "statements": {
        "A1-H1": "Compound Z, at standard oral doses, raises maximum urinary flow rate in adult men with bladder "
                 "outlet obstruction, so these men should be offered it.",
        "A1-H2": "Compound Z, at standard oral doses, does not raise maximum urinary flow rate in adult men with "
                 "bladder outlet obstruction, so offering it achieves nothing.",
        "A1-H3": "The trials in this corpus cannot decide between A1-H1 and A1-H2 for these men.",
    },
    "changes": ["Named the outcome (maximum urinary flow rate), which the typed wording left implicit."],
    "cannot_be_tested": ["'feel better': no source in the index reports a symptom score"],
}
WHY = ["My father was told nothing could be done and I want to know if that was true",   # motivation
       "To take the studies to his urologist and ask for a trial of compound Z"]         # goal
TYPED = ["a1-h1",                                                                           # the one I want to win
         "He took compound Z for another reason and his flow improved within a month",     # experience
         "I want to say that men with a blocked bladder should be offered compound Z",      # what I want to say
         "That the trials do not show it works",                                            # what I would concede
         "Should men with obstruction be offered compound Z to help their flow?",
         "Yes they should be offered it because it helps flow and they feel better",
         "No it does nothing for flow so there is no reason to offer it",
         "The trials cannot tell us one way or the other"]


class FakeModel:
    """Stands in for the model.  Forecasts depend on the wording, so that a weaker claim scores higher."""

    def __init__(self, fail=(), restated=None):
        self.tags, self.fail, self.restated = [], set(fail), restated or RESTATED

    def __call__(self, tag, system, user, salt=""):
        self.tags.append(tag)
        kind = tag.split(":")[0]
        if kind in self.fail:
            raise RuntimeError("model unavailable")
        if kind in ("corner", "openings"):
            return self.corner(kind, user)
        if kind == "forecast":
            h1 = 50 if "offered" in user.split("A1-H1:")[1].split("A1-H2:")[0] else 30
            h1 += {"forecast-1": -2, "forecast-2": 0, "forecast-3": 2}[salt]
            return {"allocations": {"A1-H1": h1, "A1-H2": 54 - h1, "A1-H3": 10}, "why": "the trials favour it"}
        if kind == "ladder":
            self.ladder_prompt = user
            return {"rungs": [{"label": "offer it", "question": RESTATED["question"], "statements": RESTATED["statements"],
                               "rival_held_by": "urologists who follow the current guideline",
                               "win_lets_you_say": "Men with obstruction should be offered compound Z.",
                               "leaves_out": "Whether the gain is large enough to matter."},
                              {"label": "beats a strawman", "question": RESTATED["question"],
                               "statements": RESTATED["statements"], "rival_held_by": "nobody",
                               "win_lets_you_say": "x", "leaves_out": "y"}]}
        if kind == "restate":
            return dict(self.restated)
        if kind == "back-translate":
            self.back_prompt = user
            return {"if_it_wins_you_may_say": ["Compound Z raises flow, so men with obstruction should be offered it."],
                    "you_may_not_say": ["That compound Z relieves symptoms."],
                    "worst_case": {"allocations": {"A1-H1": 20, "A1-H2": 30, "A1-H3": 14},
                                   "then_you_would_have_to_say": "The trials do not support offering compound Z."},
                    "rival_is_held_by": "no identifiable holder", "a_critic_will_say": ["The rival is a strawman."],
                    "left_out": ["Harms of compound Z."],
                    "conflicts": ["The governing boundary speaks of improvement, the hypotheses of offering."]}
        if kind == "judge":
            return {"match": True, "gap": ""}
        raise AssertionError(tag)

    def corner(self, kind, user):
        if kind == "openings":
            return self("ladder", "", user)
        self.corner_prompt = user
        return {"why_it_came_in_low": ["No trial enrolled men like the ones you describe."],
                "not_covered": ["Symptom relief: no source reports a symptom score."],
                "on_your_side": ["Two trials show a rise in flow rate."],
                "your_experience": "Your father was older than the men in the trials.",
                "ask_next": ["Ask smith2020 for results in men over 70."]}


class FakeConsole:
    """A person at a keyboard: scripted free text, and honest answers to what the screen asks for."""

    def __init__(self, script, gap=0.2, stop_at=None, paste_first=False, keep=("KEEP",)):
        self.script, self.gap, self.keep = list(script), gap, list(keep)
        self.out, self.t, self.stop_at, self.paste = [], 0.0, stop_at, paste_first
        self.reading = ""

    def say(self, text=""):
        self.out.append(text)

    def now(self):
        return self.t

    def sleep(self, seconds):
        self.t += seconds

    def screen(self):
        return "\n".join(self.out)

    def line(self, prompt):
        last = next((x for x in reversed(self.out) if x.strip()), "")
        if prompt.startswith("Press Enter"):
            # the text to read is everything since the "--- ... Read it. ---" line
            start = max(i for i, x in enumerate(self.out) if x.startswith("--- "))
            self.reading = " ".join(" ".join(self.out[start + 1:]).split())
            text = ""
        elif last.startswith("Which word is missing?"):
            before, after = (x.split() for x in last.split("...")[1].split("_____"))
            words = self.reading.split()
            text = next(words[i] for i in range(len(words))
                        if words[max(0, i - len(before)):i] == before and words[i + 1:i + 1 + len(after)] == after)
        elif last.startswith("Type: "):
            text = last[len("Type: "):]
            if self.stop_at and self.stop_at in text:
                text = "CHANGE"
        elif last.startswith("Type KEEP"):
            text = self.keep.pop(0) if len(self.keep) > 1 else self.keep[0]
        else:
            text = self.script.pop(0)
        gap = self.gap
        if self.paste and len(text) > 20:
            self.paste, gap = False, 0.001
            self.script.insert(0, text)                     # typed properly the second time
        stamps = [self.t + i * gap for i in range(len(text))]
        self.t += len(text) * gap + 1
        return text, stamps, True


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = main(argv)
    return rc, out.getvalue() + err.getvalue()


class TypingTest(unittest.TestCase):
    def test_paste_is_told_from_typing(self):
        typed = [i * 0.12 for i in range(40)]
        pasted = [i * 0.0005 for i in range(40)]
        self.assertFalse(fg.looks_pasted(typed))
        self.assertTrue(fg.looks_pasted(pasted))
        self.assertFalse(fg.looks_pasted(pasted[:5]))                      # too short to judge
        self.assertTrue(fg.looks_pasted(typed[:10] + [1.2 + i * 0.0005 for i in range(30)]))   # a pasted tail

    def test_paste_too_few_words_and_the_drafts_wording_are_refused(self):
        draft = "Compound Z improves maximum urinary flow rate in adult men."
        con = FakeConsole(["too short", draft.upper(), draft.replace("adult men", "grown men"),      # one word changed
                           "It helps men pass water more easily than before"], paste_first=True)
        got = fg.hand_typed(con, "H1:", min_words=6, forbid=(draft,))
        self.assertEqual(got["text"], "It helps men pass water more easily than before")
        screen = con.screen()
        self.assertIn("At least 6 words", screen)
        self.assertEqual(screen.count("That is the draft's wording. Type it in your own words."), 2)
        self.assertIn("Paste is not accepted", screen)
        self.assertTrue(got["timed"] and got["keystrokes"] == len(got["text"]))

    def test_a_script_or_a_pipe_cannot_sign(self):
        with mock.patch.object(sys, "stdin", io.StringIO("yes\n")):
            with self.assertRaises(fg.NotAPerson):
                fg.Terminal()

    def test_the_reading_check_takes_time_and_asks_for_missing_words(self):
        text = RESTATED["statements"]["A1-H1"]
        con = FakeConsole([])
        got = fg.read_check(con, "A1-H1", text)
        self.assertEqual(con.reading, text)
        self.assertEqual(len(got["blanks"]), 2)
        self.assertTrue(all(b in text for b in got["blanks"]))
        self.assertGreaterEqual(got["seconds_on_screen"], 5)
        self.assertIn("Read it; the next question opens", con.screen())        # Enter was pressed at once
        self.assertEqual(con.out[-1], "Type: I have read A1-H1")


class HeaderEditTest(unittest.TestCase):
    def test_only_the_question_and_statements_of_the_axis_change(self):
        text = (FIX / "header.md").read_text(encoding="utf-8")
        new = fg.replace_axis(text, "A1", RESTATED["question"], RESTATED["statements"])
        ax = parse_header(new)["axes"][0]
        self.assertEqual(ax["question"], RESTATED["question"])
        self.assertEqual({h["id"]: h["statement"] for h in ax["hypotheses"]}, RESTATED["statements"])
        old_lines, new_lines = text.splitlines(), new.splitlines()
        self.assertEqual(len(old_lines), len(new_lines))
        changed = [i for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
        self.assertEqual(len(changed), 4)                                   # the question and three table rows
        with self.assertRaises(ValueError):
            fg.replace_axis(text, "A2", "q", {})


class GateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("framegate")
        self.proj = self.tmp / "MINI"
        (self.proj / "01_FRAME").mkdir(parents=True)
        shutil.copyfile(FIX / "header.md", self.proj / "01_FRAME" / "header.md")
        shutil.copyfile(FIX / "index.md", self.proj / "01_FRAME" / "index.md")
        shutil.copyfile(FIX / "archivist.txt", self.proj / "01_FRAME" / "archivist-custom-prompt.txt")
        shutil.copytree(FIX / "sources", self.proj / "01_CORPUS" / "source-files")
        write_json(self.proj / "project.json", {"project": {"name": "MINI"}})

    def tearDown(self):
        cleanup(self.tmp)

    def sign(self, script=None, **kw):
        con = FakeConsole(WHY + TYPED if script is None else script, **{k: v for k, v in kw.items() if k not in ("fail", "restated")})
        model = FakeModel(kw.get("fail", ()), kw.get("restated"))
        return con, model, fg.sign_frame(con, model, self.proj, name="Test Person")

    def header(self):
        return (self.proj / "01_FRAME" / "header.md").read_text(encoding="utf-8")

    # ------------------------------------------------------------------ #
    def test_the_coach_asks_forecasts_and_the_researcher_types_reads_and_accepts(self):
        self.assertEqual(fg.accepted(self.proj), (False, "nobody has been through the frame with the coach yet"))
        con, model, cert = self.sign()
        ok, why = fg.accepted(self.proj)
        self.assertTrue(ok, why)
        self.assertIn("Test Person", why)
        screen = con.screen()

        # the three things the coach must ask: motivation, goal, and the experience behind the view
        self.assertIn("What is your motivation? Why are you running this analysis?", screen)
        self.assertIn("What is your goal, and how do you hope this analysis will help you reach it?", screen)
        self.assertIn("What experience shaped your view? Why do you think A1-H1 is right, even where published", screen)
        self.assertEqual(cert["who"], {"motivation": WHY[0], "goal": WHY[1]})
        rec = cert["axes"]["A1"]
        self.assertEqual(rec["experience"]["text"], TYPED[1])
        # ... and the model that proposes frames is told all of it, with the calibration method
        for needle in (WHY[0], WHY[1], TYPED[1], "weakest claim", "strongest position that real people actually hold"):
            self.assertIn(needle, model.ladder_prompt)

        # the header now carries the restated wording and the approval marker; nothing else moved
        ax = parse_header(self.header())["axes"][0]
        self.assertEqual({h["id"]: h["statement"] for h in ax["hypotheses"]}, RESTATED["statements"])
        self.assertEqual(ax["approval"], "APPROVED")
        self.assertIn("<!-- APPROVED: Test Person on ", self.header())
        self.assertIn("**Potential falsification:** A randomized trial shows no change", self.header())

        # forecasts: the draft and the one usable alternative (a rival nobody holds is not offered)
        self.assertEqual([r["label"] for r in rec["ladder"]], ["the draft as written", "offer it"])
        self.assertEqual(sum(t.startswith("forecast:A1:rung") for t in model.tags), 6)
        self.assertEqual(sum(t.startswith("forecast:A1:final") for t in model.tags), 3)
        self.assertIn('If you want A1-H1 to be preferred, the best of these is "offer it" (50 of 64)', screen)
        self.assertIn("The rival is held by: urologists who follow the current guideline", screen)
        self.assertIn("FORECAST for A1-H1 under your wording: 50 of 64   (calls: 48, 50, 52). Target: 43.", screen)
        self.assertIn("It is not a probability that you are right.", screen)

        self.assertEqual(rec["preferred"], "A1-H1")
        self.assertEqual(rec["typed"]["statements"]["A1-H1"]["text"], TYPED[5])
        self.assertEqual([r["label"] for r in rec["read"]], ["A1-H1", "A1-H2", "A1-H3", "the limits of A1"])
        self.assertIn("Potential falsification: A randomized trial shows no change in maximum flow rate", screen)
        self.assertEqual([a["typed"] for a in rec["accepted"]],
                         ["I accept 50 of 64", "I accept the worst case", "I accept what a win means",
                          "I accept the rival", "I accept what is left out", "I accept the conflicts"])
        self.assertEqual(rec["model_steps"], {"ladder": "ok", "forecast": "ok", "restate": "ok",
                                              "back_translate": "ok", "judge": "ok"})
        # the reading of the finished axis is made without the researcher's stated aim
        self.assertIn(RESTATED["statements"]["A1-H1"], model.back_prompt)
        self.assertNotIn(TYPED[2], model.back_prompt)

        md = (self.proj / "01_FRAME" / fg.CERT_MD).read_text(encoding="utf-8")
        for needle in (WHY[0], TYPED[1], TYPED[5], RESTATED["statements"]["A1-H1"], "**50 of 64**",
                       "Worst likely result: A1-H1 20", '"I accept the worst case"'):
            self.assertIn(needle, md)
        self.assertNotIn("signature", read_text(self.proj / "01_FRAME" / fg.CERT_JSON))    # a plain record, no cryptography
        self.assertIn("Frame accepted by Test Person", read_json(self.proj / "project.json")["frame"]["approval_note"])

    def test_changed_wording_has_not_been_accepted(self):
        self.sign()
        hp = self.proj / "01_FRAME" / "header.md"
        good = hp.read_text(encoding="utf-8")
        hp.write_text(good.replace("so these men should be offered it", "so every man should take it"), encoding="utf-8")
        self.assertEqual(fg.accepted(self.proj), (False, "the wording of axis A1 changed since it was accepted"))
        hp.write_text(good.replace("Build the strongest", "Build only the strongest"), encoding="utf-8")   # not the hypotheses
        self.assertTrue(fg.accepted(self.proj)[0])
        hp.write_text(good.replace("\n", "\r\n"), encoding="utf-8", newline="")
        self.assertTrue(fg.accepted(self.proj)[0])

    def test_change_stops_without_saving(self):
        before = self.header()
        with self.assertRaises(fg.Changed):
            self.sign(stop_at="worst case")
        self.assertEqual(self.header(), before)
        self.assertFalse((self.proj / "01_FRAME" / fg.CERT_JSON).exists())

    def test_without_a_model_the_session_still_works_and_the_record_says_so(self):
        con, _, cert = self.sign(fail=("forecast", "ladder", "restate", "back-translate", "judge"))
        self.assertTrue(fg.accepted(self.proj)[0])
        rec = cert["axes"]["A1"]
        self.assertEqual(rec["accepted"][0]["typed"], "I accept no forecast")
        self.assertTrue(rec["restated"]["not_restated"])
        self.assertEqual(rec["restated"]["statements"]["A1-H1"], TYPED[5])                   # the person's own words
        md = (self.proj / "01_FRAME" / fg.CERT_MD).read_text(encoding="utf-8")
        self.assertIn("No forecast could be made.", md)
        self.assertIn("Model step `restate`: failed", md)

    def test_wording_already_accepted_may_be_typed_again_but_a_draft_may_not(self):
        self.sign(fail=("restate",))                       # the header now carries the person's own typed words
        con = FakeConsole(TYPED)                           # the coach remembers why they are running this
        fg.sign_frame(con, FakeModel(fail=("restate",)), self.proj, only="A1")
        self.assertNotIn("That is the draft's wording", con.screen())
        self.assertIn("You told the coach earlier:", con.screen())
        self.assertNotIn("What is your motivation?", con.screen())

        shutil.copyfile(FIX / "header.md", self.proj / "01_FRAME" / "header.md")       # a draft somebody else wrote
        draft = parse_header(self.header())["axes"][0]["hypotheses"][0]["statement"]
        con = FakeConsole(TYPED[:5] + [draft] + TYPED[5:])
        fg.sign_frame(con, FakeModel(), self.proj)
        self.assertIn("That is the draft's wording. Type it in your own words.", con.screen())

    def test_a_weaker_forecast_than_the_best_frame_is_put_to_the_researcher(self):
        weak = dict(RESTATED, statements=dict(RESTATED["statements"],
                                              **{"A1-H1": "Compound Z raises maximum urinary flow rate in every adult man who takes it."}))
        con, _, cert = self.sign(WHY + TYPED + TYPED[4:], keep=("RETYPE", "KEEP"), restated=weak)
        screen = con.screen()
        self.assertEqual(screen.count('Are you sure you are OK with this wording? If you want A1-H1 to be preferred, '
                                      '"offer it" is the better choice: 50 of 64 against 30 for yours.'), 2)
        self.assertEqual(screen.count("Now type the question"), 2)                           # RETYPE, then KEEP
        accepted = cert["axes"]["A1"]["accepted"][0]
        self.assertEqual(accepted["typed"], "I accept 30 of 64")
        self.assertIn("That is BELOW your target.", " ".join(accepted["shown"]))
        self.assertIn("show you a claim this evidence does support", " ".join(accepted["shown"]))

    def test_there_must_be_an_index_to_forecast_against(self):
        (self.proj / "01_FRAME" / "index.md").unlink()
        with self.assertRaisesRegex(ValueError, "no source index"):
            fg.sign_frame(FakeConsole(WHY + TYPED), FakeModel(), self.proj, name="T")

    def test_every_axis_is_coached(self):
        hp = self.proj / "01_FRAME" / "header.md"
        one = self.header()
        s, e = fg.axis_spans(one)["A1"]
        two = one[s:e].replace("axis one", "axis two").replace("A1-", "A2-")
        hp.write_text(one[:e] + two + one[e:], encoding="utf-8")
        con = FakeConsole(WHY + TYPED)
        cert = fg.sign_frame(con, FakeModel(), self.proj, only="A1", name="T")
        self.assertEqual(cert["unaccepted_axes"], ["A2"])
        self.assertEqual(fg.accepted(self.proj), (False, "axis A2 has not been through the coach"))
        self.assertNotIn("APPROVED: T ", self.header())                                       # not approved until whole
        self.assertIn("Still to do: axis A2", con.screen())

    # ------------------------------------------------------------------ #
    def test_a_quest_waits_for_the_coach_and_nothing_else_does(self):
        cfg = read_json(self.proj / "project.json")
        cfg["coach"] = {"require_acceptance": True}                  # the default; the test suite turns it off globally
        write_json(self.proj / "project.json", cfg)
        ok, msg = fg.gate(self.proj, "quest")
        self.assertFalse(ok)
        self.assertIn("quest not started: nobody has been through the frame with the coach yet", msg)
        self.assertEqual(fg.gate(self.proj, "run")[0], True)
        self.assertEqual(fg.gate(self.proj, "import")[0], True)

        args = SimpleNamespace(project=str(self.proj), id=None, new=False, notebook=[], hours="1",
                               max_questions="10", profile=None, no_driver=True, then_run=False)
        err = io.StringIO()
        with redirect_stderr(err), redirect_stdout(io.StringIO()):
            self.assertEqual(onramp.cmd_quest(args), 2)
        self.assertIn("quest not started", err.getvalue())
        self.assertFalse((self.proj / "quest").exists())

        rc, out = run(["sign", str(self.proj)])                       # the tests have no keyboard
        self.assertEqual(rc, 2)
        self.assertIn("person at a keyboard", out)
        rc, out = run(["sign", str(self.proj), "--check"])
        self.assertEqual(rc, 2)
        self.assertIn("NOT YET", out)

        cfg["coach"] = {"require_acceptance": False}                  # the plain switch, should the session misbehave
        write_json(self.proj / "project.json", cfg)
        self.assertEqual(fg.gate(self.proj, "quest")[0], True)
        cfg["coach"] = {"require_acceptance": True}
        write_json(self.proj / "project.json", cfg)
        self.sign()
        self.assertEqual(fg.gate(self.proj, "quest")[0], True)
        rc, out = run(["coach", str(self.proj), "--check"])           # `cr coach` is the same command
        self.assertEqual(rc, 0, out)
        self.assertIn("ACCEPTED: frame accepted by Test Person", out)

    def test_the_record_travels_with_the_run(self):
        self.sign()
        rc, out = run(["run", str(self.proj), "--run", "R1", "--to", "frame"])
        self.assertEqual(rc, 0, out[-600:])
        run_dir = self.proj / "02_RUNS" / "R1"
        self.assertTrue((run_dir / "01_FRAME" / fg.CERT_MD).exists())
        self.assertTrue(read_json(run_dir / "RUN-CONFIG.json")["frame_accepted"])
        self.assertIn("[Frame record](01_FRAME/FRAME-CERTIFICATE.md)", (run_dir / "RUN-MAP.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
