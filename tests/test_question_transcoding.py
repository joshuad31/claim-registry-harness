"""Questions are transcoded before witnesses are built (technical specification 1, step 11).

The witness constructor and the fidelity audit read the transcoded question when its transcoding
passed and the raw question otherwise; each witness records which.  With the language layer off
the transcoded question is the raw question and nothing changes.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fakes  # noqa: E402
from claimreg.llm.router import LLM  # noqa: E402
from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402
from test_pipeline_mock import make_project  # noqa: E402

MARK = "CONTROLLED-FORM"
SCRIPTED = {"type": "scripted", "model": "scripted-1", "script": "tc"}


def transcoder(fail_qids=()):
    """A transcoder that marks every question it rewrites, and returns REVIEW for ``fail_qids``."""
    def run(req, provider):
        out = []
        for it in req.meta.get("items", []):
            new = f"{MARK} {it['raw']}" if it["type"] == "QUESTION" else it["raw"]
            st = "REVIEW" if it["item_id"] in fail_qids else "PASS"
            out.append(f"### {it['item_id']} · {it['type']} · {st}\nOriginal: {it['raw']}\nTranscoded: {new}\n"
                       f"Bindings: none\nRules: none\nCheck: {st}")
        return "\n\n".join(out)
    return run


class QuestionTranscodingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("question-transcode")
        fakes.reset()
        self.seen = []
        self._orig = LLM.call_many
        seen, orig = self.seen, self._orig

        def spy(llm, reqs, *a, **kw):
            seen.extend(reqs)
            return orig(llm, reqs, *a, **kw)
        LLM.call_many = spy

    def tearDown(self):
        LLM.call_many = self._orig
        cleanup(self.tmp)

    def run_to_transcode(self, extra, fail_first=False):
        proj = make_project(self.tmp, extra=extra)
        ctx = RunContext(proj, "RUN-QT", create=True, quiet=True)
        if fail_first:
            # learn which questions exist, then script a failure for the first one that is applied
            out = run_pipeline(ctx, stop="frd_retain")
            self.assertEqual(out["status"], "complete", out)
            sc = ctx.scopes()[0]
            retained = sc.load("frds", "05_validated/retained-frds.json") or sc.load("frds", "05_validated/validated-frds.json")
            self.bad = sorted({v["qid"] for v in retained})[0]
            fakes.SCRIPTS["tc"] = transcoder({self.bad})
        out = run_pipeline(ctx, stop="transcode")
        self.assertEqual(out["status"], "complete", out)
        return ctx, ctx.scopes()[0]

    def by_question(self, role):
        return [(r.tag, r.user) for r in self.seen if r.role == role]

    def test_off_is_the_identity_and_changes_nothing(self):
        ctx, sc = self.run_to_transcode({})
        rec = sc.load("witnesses", "01_question-applications/transcoded-questions.json")
        self.assertEqual(rec["mode"], "off")
        self.assertTrue(rec["items"])
        self.assertTrue(all(i["status"] == "IDENTITY" and i["transcoded"] == i["raw"] and i["type"] == "QUESTION"
                            for i in rec["items"]))
        self.assertFalse([r for r in self.seen if r.role == "transcoder"])           # no model was asked
        ws = sc.load("witnesses", "05_released/witnesses.json")
        self.assertTrue(ws and all(w["question_form"] == "raw" for w in ws))
        tc = sc.load("transcoding", "transcoded.json")
        self.assertEqual(len(tc["questions"]), len(rec["items"]))
        # the questions are listed apart from the items that go to matching
        self.assertFalse([i for i in tc["items"] if i["type"] == "QUESTION"])

    def test_labels_the_constructor_and_the_auditor_read_the_transcoded_question(self):
        fakes.SCRIPTS["tc"] = transcoder()
        ctx, sc = self.run_to_transcode({"language": {"mode": "labels"}, "roles": {"transcoder": "scripted"},
                                         "providers": {"scripted": SCRIPTED}})
        rec = sc.load("witnesses", "01_question-applications/transcoded-questions.json")
        self.assertTrue(all(i["status"] == "PASS" and i["transcoded"].startswith(MARK) for i in rec["items"]))
        cons, aud = self.by_question("witness_constructor"), self.by_question("witness_auditor")
        self.assertTrue(cons and aud)
        self.assertTrue(all(MARK in user for _, user in cons + aud))
        ws = sc.load("witnesses", "05_released/witnesses.json")
        self.assertTrue(ws and all(w["question_form"] == "transcoded" and w["question_transcode_status"] == "PASS"
                                   for w in ws))
        # the question of record is still the raw one, under the same QID
        qs = {q["qid"]: q["text"] for q in sc.load("discovery", "01_issued-questions/questions.json")}
        self.assertTrue(all(i["raw"] == qs[i["item_id"]] and MARK not in qs[i["item_id"]] for i in rec["items"]))
        # the matcher is given witness and unit texts, never a question
        tc = sc.load("transcoding", "transcoded.json")
        self.assertEqual({i["type"] for i in tc["items"]}, {"WITNESS", "HYPOTHESIS"})
        self.assertEqual(ctx.stage_state()["witnesses"]["summary"]["A1"]["question_forms"]["raw_fallback"], 0)

    def test_a_question_that_did_not_pass_falls_back_to_raw_and_says_so(self):
        ctx, sc = self.run_to_transcode({"language": {"mode": "labels"}, "roles": {"transcoder": "scripted"},
                                         "providers": {"scripted": SCRIPTED}}, fail_first=True)
        cons = self.by_question("witness_constructor")
        own = [user for tag, user in cons if f"-{self.bad}:" in tag]
        rest = [user for tag, user in cons if f"-{self.bad}:" not in tag]
        self.assertTrue(own and all(MARK not in u for u in own))                     # raw question
        self.assertTrue(all(MARK in u for u in rest))
        every = sc.load("witnesses", "05_released/witnesses.json") + sc.load("witnesses", "04_repaired-or-held/held.json")
        forms = {w["qid"]: (w["question_form"], w["question_transcode_status"]) for w in every}
        self.assertEqual(forms[self.bad], ("raw", "REVIEW"))
        self.assertTrue(all(f == ("transcoded", "PASS") for q, f in forms.items() if q != self.bad))

    def test_hold_keeps_the_application_for_review_instead(self):
        ctx, sc = self.run_to_transcode({"language": {"mode": "labels", "question_fallback": "hold"},
                                         "roles": {"transcoder": "scripted"},
                                         "providers": {"scripted": SCRIPTED}}, fail_first=True)
        self.assertFalse([t for t, _ in self.by_question("witness_constructor") if f"-{self.bad}:" in t])
        held = [h for h in sc.load("witnesses", "04_repaired-or-held/held.json") if h["qid"] == self.bad]
        self.assertTrue(held and all("transcoding needs review" in h["held_reason"] for h in held))
        self.assertFalse([w for w in sc.load("witnesses", "05_released/witnesses.json") if w["qid"] == self.bad])
        self.assertEqual(ctx.stage_state()["witnesses"]["summary"]["A1"]["question_forms"]["held_for_question"], len(held))


if __name__ == "__main__":
    unittest.main()
