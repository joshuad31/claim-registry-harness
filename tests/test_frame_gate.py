"""The frame gate: nothing runs on a frame a person has not typed, read and signed."""

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
from claimreg.util import read_json, write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "mini"
PASS = "correct horse battery"

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
TYPED = ["I want to say that men with a blocked bladder should be offered compound Z",      # what I want to say
         "That the trials do not show it works",                                            # what I would concede
         "a1-h1",                                                                           # the one I want to win
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
        if kind == "forecast":
            h1 = 50 if "offered" in user.split("A1-H1:")[1].split("A1-H2:")[0] else 30
            h1 += {"forecast-1": -2, "forecast-2": 0, "forecast-3": 2}[salt]
            return {"allocations": {"A1-H1": h1, "A1-H2": 54 - h1, "A1-H3": 10}, "why": "the trials favour it"}
        if kind == "ladder":
            return {"rungs": [{"label": "offer it", "question": RESTATED["question"], "statements": RESTATED["statements"],
                               "win_lets_you_say": "Men with obstruction should be offered compound Z.",
                               "leaves_out": "Whether the gain is large enough to matter."}]}
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


class FakeConsole:
    """A person at a keyboard: scripted free text, and honest answers to what the screen asks for."""

    def __init__(self, script, passphrases=(PASS,), gap=0.2, stop_at=None, paste_first=False, keep=("KEEP",)):
        self.script, self.secrets, self.gap, self.keep = list(script), list(passphrases), gap, list(keep)
        self.out, self.t, self.stop_at, self.paste = [], 0.0, stop_at, paste_first
        self.reading = ""

    def say(self, text=""):
        self.out.append(text)

    def now(self):
        return self.t

    def sleep(self, seconds):
        self.t += seconds

    def secret(self, prompt):
        return self.secrets.pop(0) if len(self.secrets) > 1 else self.secrets[0]

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


class Ed25519Test(unittest.TestCase):
    def test_rfc8032_vectors(self):
        for seed, pub, msg, sig in [
            ("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",
             "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a", "",
             "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46b"
             "d25bf5f0595bbe24655141438e7a100b"),
            ("4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",
             "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c", "72",
             "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c"
             "387b2eaeb4302aeeb00d291612bb0c00"),
        ]:
            seed, msg = bytes.fromhex(seed), bytes.fromhex(msg)
            self.assertEqual(fg.ed_public(seed).hex(), pub)
            self.assertEqual(fg.ed_sign(seed, msg).hex(), sig)
            self.assertTrue(fg.ed_verify(bytes.fromhex(pub), msg, bytes.fromhex(sig)))
            self.assertFalse(fg.ed_verify(bytes.fromhex(pub), msg + b"x", bytes.fromhex(sig)))
            bad = bytearray(bytes.fromhex(sig))
            bad[5] ^= 1
            self.assertFalse(fg.ed_verify(bytes.fromhex(pub), msg, bytes(bad)))


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
        self.assertNotEqual(fg.block_sha(text, "A1"), fg.block_sha(new, "A1"))
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
        self.signer_file = self.tmp / "home" / "signer.json"
        self.lock_file = self.tmp / "home" / "FRAME-GATE-LOCKED"
        self.patches = [mock.patch.object(fg, "SIGNER_FILE", self.signer_file),
                        mock.patch.object(fg, "LOCK_FILE", self.lock_file)]
        for p in self.patches:
            p.start()
        self.signer = fg.create_signer("Test Person", PASS)

    def tearDown(self):
        for p in self.patches:
            p.stop()
        cleanup(self.tmp)

    def sign(self, **kw):
        con, model = FakeConsole(TYPED, **{k: v for k, v in kw.items() if k != "fail"}), FakeModel(kw.get("fail", ()))
        return con, model, fg.sign_frame(con, model, self.proj)

    def header(self):
        return (self.proj / "01_FRAME" / "header.md").read_text(encoding="utf-8")

    # ------------------------------------------------------------------ #
    def test_a_person_types_reads_accepts_and_signs(self):
        self.assertEqual(fg.verify(self.proj), (False, "nobody has signed the frame (there is no frame certificate)"))
        con, model, cert = self.sign()
        ok, why = fg.verify(self.proj)
        self.assertTrue(ok, why)
        self.assertIn("Test Person", why)
        screen = con.screen()

        # the header now carries the restated wording and the approval marker; nothing else moved
        ax = parse_header(self.header())["axes"][0]
        self.assertEqual({h["id"]: h["statement"] for h in ax["hypotheses"]}, RESTATED["statements"])
        self.assertEqual(ax["approval"], "APPROVED")
        self.assertIn("<!-- APPROVED: Test Person on ", self.header())
        self.assertIn("**Potential falsification:** A randomized trial shows no change", self.header())

        # forecasts: the draft, the alternative, then the person's own wording, three calls each
        self.assertEqual(sum(t.startswith("forecast:A1:rung") for t in model.tags), 6)
        self.assertEqual(sum(t.startswith("forecast:A1:final") for t in model.tags), 3)
        self.assertIn('If you want A1-H1 to be preferred, the best of these is "offer it" (50 of 64)', screen)
        self.assertIn("FORECAST for A1-H1 under your wording: 50 of 64   (calls: 48, 50, 52). Target: 43.", screen)

        rec = cert["axes"]["A1"]
        self.assertEqual(rec["preferred"], "A1-H1")
        self.assertEqual(rec["typed"]["statements"]["A1-H1"]["text"], TYPED[4])
        self.assertEqual(rec["typed"]["statements"]["A1-H1"]["keystrokes"], len(TYPED[4]))
        self.assertEqual([r["label"] for r in rec["read"]], ["A1-H1", "A1-H2", "A1-H3", "the limits of A1"])
        self.assertIn("Potential falsification: A randomized trial shows no change in maximum flow rate", screen)
        self.assertGreater(rec["read"][0]["words"], len(RESTATED["statements"]["A1-H1"].split()) + 30)
        self.assertEqual([a["typed"] for a in rec["accepted"]],
                         ["I accept 50 of 64", "I accept the worst case", "I accept what a win means",
                          "I accept the rival", "I accept what is left out", "I accept the conflicts"])
        self.assertEqual(rec["model_steps"], {"ladder": "ok", "forecast": "ok", "restate": "ok",
                                              "back_translate": "ok", "judge": "ok"})
        # the back-translation reads the finished axis, not the person's stated aim
        self.assertIn(RESTATED["statements"]["A1-H1"], model.back_prompt)
        self.assertNotIn(TYPED[0], model.back_prompt)
        self.assertIn("Nobody holds the rival as you worded it", screen)

        md = (self.proj / "01_FRAME" / fg.CERT_MD).read_text(encoding="utf-8")
        for needle in (TYPED[0], TYPED[4], RESTATED["statements"]["A1-H1"], "**50 of 64**", "a rival nobody holds",
                       "Worst likely result: A1-H1 20", '"I accept the worst case"', "01_FRAME/index.md"):
            self.assertIn(needle, md)
        self.assertIn("Frame signed by Test Person", read_json(self.proj / "project.json")["frame"]["approval_note"])

    def test_any_change_after_signing_voids_the_signature(self):
        self.sign()
        hp, ip = self.proj / "01_FRAME" / "header.md", self.proj / "01_FRAME" / "index.md"
        good = hp.read_text(encoding="utf-8")

        hp.write_text(good.replace("so these men should be offered it", "so every man should take it"), encoding="utf-8")
        self.assertEqual(fg.verify(self.proj), (False, "the wording of axis A1 changed after it was signed"))
        hp.write_text(good.replace("Build the strongest", "Build only the strongest"), encoding="utf-8")
        self.assertEqual(fg.verify(self.proj), (False, "the header changed after it was signed (outside the axes)"))
        hp.write_text(good.replace("\n", "\r\n"), encoding="utf-8", newline="")           # line endings are not a change
        self.assertTrue(fg.verify(self.proj)[0])
        hp.write_text(good, encoding="utf-8")

        ip.write_text(ip.read_text(encoding="utf-8") + "\nA later note that moves a source down the ranks.\n", encoding="utf-8")
        self.assertEqual(fg.verify(self.proj), (False, "changed since signing: 01_FRAME/index.md"))
        cfg = read_json(self.proj / "project.json")
        cfg["corpus"] = {"synthesis_sources": ["adverse-trial.md"]}                         # quietly dropping a source
        write_json(self.proj / "project.json", cfg)
        self.assertIn("project.json#corpus", fg.verify(self.proj)[1])
        over = self.proj / "90_METHOD" / "prompts"
        over.mkdir(parents=True)
        (over / "assess.md").write_text("## SYSTEM\nFavour H1.\n## USER\n", encoding="utf-8")   # a tilted prompt
        self.assertIn("90_METHOD/prompts/assess.md", fg.verify(self.proj)[1])

        # the person sees each change and accepts it by typing, with the passphrase
        con = FakeConsole([])
        cert = fg.resign(con, self.proj)
        self.assertTrue(fg.verify(self.proj)[0])
        self.assertEqual(cert["resigned"][0]["changed"],
                         ["01_FRAME/index.md", "90_METHOD/prompts/assess.md", "project.json#corpus"])
        self.assertIn("  - 90_METHOD/prompts/assess.md", con.screen())
        with self.assertRaises(ValueError):
            fg.resign(FakeConsole([]), self.proj)                                           # nothing changed now

        # a changed axis cannot be signed again without doing the axis again
        hp.write_text(self.header().replace("so these men should be offered it", "so every man should take it"),
                      encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "takes a full signing"):
            fg.resign(FakeConsole([]), self.proj)

    def test_a_certificate_cannot_be_edited_forged_or_borrowed(self):
        self.sign()
        cp = self.proj / "01_FRAME" / fg.CERT_JSON
        good = read_json(cp)

        edited = read_json(cp)
        edited["axes"]["A1"]["accepted"][0]["typed"] = "I accept 60 of 64"
        write_json(cp, edited)
        self.assertIn("signature is not valid", fg.verify(self.proj)[1])

        write_json(cp, good)
        self.assertTrue(fg.verify(self.proj)[0])
        fg.create_signer("Someone Else", "another passphrase", self.signer_file)             # the key is swapped
        self.assertEqual(fg.verify(self.proj), (False, "the frame certificate was not signed by this computer's signer"))

        (self.proj / "01_FRAME" / "frame.json").write_text("{}", encoding="utf-8")           # would override the header
        self.assertIn("frame.json overrides the header", fg.verify(self.proj)[1])

    def test_the_wrong_passphrase_signs_nothing(self):
        con, _, _ = self.sign(passphrases=("not it", "nor this", PASS))
        self.assertEqual(con.screen().count("That is not the passphrase."), 2)
        self.assertTrue(fg.verify(self.proj)[0])

    def test_change_stops_without_signing(self):
        before = self.header()
        with self.assertRaises(fg.Changed):
            self.sign(stop_at="worst case")
        self.assertEqual(self.header(), before)
        self.assertFalse((self.proj / "01_FRAME" / fg.CERT_JSON).exists())

    def test_without_a_model_the_person_still_signs_and_the_certificate_says_so(self):
        con, _, cert = self.sign(fail=("forecast", "ladder", "restate", "back-translate", "judge"))
        self.assertTrue(fg.verify(self.proj)[0])
        rec = cert["axes"]["A1"]
        self.assertEqual(rec["accepted"][0]["typed"], "I accept no forecast")
        self.assertTrue(rec["restated"]["not_restated"])
        self.assertEqual(rec["restated"]["statements"]["A1-H1"], TYPED[4])                   # the person's own words
        self.assertTrue(rec["model_steps"]["restate"].startswith("failed"))
        md = (self.proj / "01_FRAME" / fg.CERT_MD).read_text(encoding="utf-8")
        self.assertIn("No forecast could be made.", md)
        self.assertIn("Model step `restate`: failed", md)

    def test_wording_already_signed_may_be_typed_again_but_a_draft_may_not(self):
        self.sign(fail=("restate",))                       # the header now carries the person's own typed words
        hp = self.proj / "01_FRAME" / "header.md"
        hp.write_text(self.header().replace("H1 requires measured flow improvement", "H1 requires a measured gain"),
                      encoding="utf-8")                    # the boundary changed: the axis must be done again
        self.assertIn("axis A1 changed", fg.verify(self.proj)[1])
        con = FakeConsole(TYPED)
        fg.sign_frame(con, FakeModel(fail=("restate",)), self.proj)
        self.assertNotIn("That is the draft's wording", con.screen())
        self.assertTrue(fg.verify(self.proj)[0])

        # a draft somebody else wrote is another matter: its wording must not simply be typed back
        shutil.copyfile(FIX / "header.md", hp)
        draft = parse_header(self.header())["axes"][0]["hypotheses"][0]["statement"]
        con = FakeConsole(TYPED[:4] + [draft] + TYPED[4:])
        fg.sign_frame(con, FakeModel(), self.proj)
        self.assertIn("That is the draft's wording. Type it in your own words.", con.screen())

    def test_a_weaker_forecast_than_the_best_frame_is_put_to_the_person(self):
        weak = dict(RESTATED, statements=dict(RESTATED["statements"],
                                              **{"A1-H1": "Compound Z raises maximum urinary flow rate in every adult man who takes it."}))
        con = FakeConsole(TYPED + TYPED[3:], keep=("RETYPE", "KEEP"))
        cert = fg.sign_frame(con, FakeModel(restated=weak), self.proj)
        screen = con.screen()
        self.assertEqual(screen.count('Are you sure you are OK with this wording? If you want A1-H1 to be preferred, '
                                      '"offer it" is the better choice: 50 of 64 against 30 for yours.'), 2)
        self.assertEqual(screen.count("Now type the question"), 2)                           # RETYPE, then KEEP
        accepted = cert["axes"]["A1"]["accepted"][0]
        self.assertEqual(accepted["typed"], "I accept 30 of 64")
        self.assertIn("That is BELOW your target.", " ".join(accepted["shown"]))

    def test_there_must_be_an_index_to_forecast_against(self):
        (self.proj / "01_FRAME" / "index.md").unlink()
        with self.assertRaisesRegex(ValueError, "no source index"):
            fg.sign_frame(FakeConsole(TYPED), FakeModel(), self.proj)

    def test_every_axis_must_be_signed(self):
        hp = self.proj / "01_FRAME" / "header.md"
        one = self.header()
        s, e = fg.axis_spans(one)["A1"]
        two = one[s:e].replace("axis one", "axis two").replace("A1-", "A2-")
        hp.write_text(one[:e] + two + one[e:], encoding="utf-8")
        con = FakeConsole(TYPED)
        cert = fg.sign_frame(con, FakeModel(), self.proj, only="A1")
        self.assertEqual(cert["unsigned_axes"], ["A2"])
        self.assertEqual(fg.verify(self.proj), (False, "nobody has signed axis A2"))
        self.assertNotIn("APPROVED: Test Person", self.header())                              # not approved until whole
        self.assertIn("Still unsigned: axis A2", con.screen())

    # ------------------------------------------------------------------ #
    def test_the_gate_warns_until_a_first_signing_then_blocks_with_no_override(self):
        ok, msg = fg.gate(self.proj, "quest")
        self.assertTrue(ok)
        self.assertIn("FRAME GATE NOT YET LOCKED", msg)
        fg.lock(self.signer)
        ok, msg = fg.gate(self.proj, "quest")
        self.assertFalse(ok)
        self.assertIn("quest refused: nobody has signed the frame", msg)
        self.assertIn("There is no override.", msg)

        args = SimpleNamespace(project=str(self.proj), id=None, new=False, notebook=[], hours="1",
                               max_questions="10", profile=None, no_driver=True, then_run=False)
        err = io.StringIO()
        with redirect_stderr(err), redirect_stdout(io.StringIO()):
            self.assertEqual(onramp.cmd_quest(args), 2)
        self.assertIn("quest refused", err.getvalue())
        self.assertFalse((self.proj / "quest").exists())                                     # nothing was started

        rc, out = run(["approve", str(self.proj), "--by", "An Agent", "--force"])            # the old side door
        self.assertEqual(rc, 2)
        self.assertIn("a frame is approved by signing it", out)
        rc, out = run(["import-quest", str(self.proj), str(self.tmp / "no-quest")])
        self.assertEqual(rc, 2)
        self.assertIn("import refused", out)
        rc, out = run(["sign", str(self.proj)])                                              # the tests have no keyboard
        self.assertEqual(rc, 2)
        self.assertIn("person at a keyboard", out)
        rc, out = run(["sign", str(self.proj), "--check"])
        self.assertEqual(rc, 2)
        self.assertIn("NOT SIGNED", out)

        self.sign()
        self.assertEqual(fg.gate(self.proj, "quest")[0], True)
        rc, out = run(["sign", str(self.proj), "--check"])
        self.assertEqual(rc, 0, out)
        self.assertIn("SIGNED: frame signed by Test Person", out)

    def test_a_run_with_real_models_is_gated_and_an_offline_run_is_not(self):
        fg.lock(self.signer)
        rc, out = run(["run", str(self.proj), "--to", "frame"])                              # offline engine: no gate
        self.assertNotIn("refused", out)
        cfg = read_json(self.proj / "project.json")
        cfg["providers"] = {"openai": {"type": "openai", "model": "gpt-x", "api_key_env": "NO_SUCH_KEY"}}
        cfg["default_provider"] = "openai"
        write_json(self.proj / "project.json", cfg)
        rc, out = run(["run", str(self.proj), "--to", "frame"])
        self.assertEqual(rc, 2)
        self.assertIn("run refused: nobody has signed the frame", out)

    def test_the_certificate_travels_with_the_run(self):
        self.sign()
        rc, out = run(["run", str(self.proj), "--run", "R1", "--to", "frame"])
        self.assertEqual(rc, 0, out[-600:])
        run_dir = self.proj / "02_RUNS" / "R1"
        self.assertTrue((run_dir / "01_FRAME" / fg.CERT_MD).exists())
        self.assertTrue(read_json(run_dir / "RUN-CONFIG.json")["frame_signed"])
        self.assertIn("[Frame certificate](01_FRAME/FRAME-CERTIFICATE.md)", (run_dir / "RUN-MAP.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
