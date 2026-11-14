"""Regressions for the defects found in the 2026-11-14 review (ChatGPT's six, and the four that
were measured on a real run): the quotation check, matching with a dropped row or a failed
qualification pattern, scope-conditioned contradictions, T2 on the whole rival, `cr verify` on an
empty run, the assessment parser, stale stages, and redundancy in retention.

Every case here is topic-neutral: nothing in the harness knows what a run is about.
"""

import json
import shutil
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg import matching  # noqa: E402
from claimreg.assess import _parse_assessment, check_vector  # noqa: E402
from claimreg.corpus import find_quote  # noqa: E402
from claimreg.coverage import build_problem  # noqa: E402
from claimreg.crux import _assumptions, compile_theory, test_t1, test_t2  # noqa: E402
from claimreg.frd import same_finding  # noqa: E402
from claimreg.llm.base import LLMResponse  # noqa: E402
from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.prompts import PromptLibrary  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import read_json, write_json  # noqa: E402
from claimreg.verify import verify_run  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- #
class QuoteCheckTest(unittest.TestCase):
    SRC = ("In the randomized trial, compound Z did not improve maximum urinary flow rate at twelve weeks "
           "compared with placebo. Mean residual volume rose from 1.6 to 5.4 units when iron was taken "
           "together with the tablet in this cohort.")

    def rejected(self, quote, *needles, src=None):
        r = find_quote(src or self.SRC, quote)
        self.assertFalse(r["found"], r)
        for n in needles:
            self.assertIn(n, r.get("why", ""), r)
        return r

    def test_a_dropped_negation_is_not_a_quotation(self):
        r = self.rejected("In the randomized trial, compound Z did improve maximum urinary flow rate at twelve "
                          "weeks compared with placebo.", "not")
        self.assertTrue(r["located"])                 # the passage was found; the quotation misstates it

    def test_a_changed_number_is_not_a_quotation(self):
        self.rejected("Mean residual volume rose from 1.6 to 1.6 units when iron was taken together with the "
                      "tablet in this cohort.", "number")

    def test_a_dropped_hedge_or_limiter_is_not_a_quotation(self):
        src = ("Bedtime administration may lower thyrotropin in selected patients with documented morning "
               "interference, but only when the evening meal ended three hours earlier in every case.")
        self.rejected("Bedtime administration lower thyrotropin in selected patients with documented morning "
                      "interference, but only when the evening meal ended three hours earlier in every case.",
                      "may", src=src)
        self.rejected("Bedtime administration may lower thyrotropin in selected patients with documented morning "
                      "interference, when the evening meal ended three hours earlier in every case.", src=src)

    def test_words_the_source_does_not_have(self):
        self.rejected("In the randomized trial, compound Z did not significantly improve maximum urinary flow "
                      "rate at twelve weeks compared with placebo.")

    def test_a_fabricated_passage_in_an_ellipsis_quotation(self):
        src = ("Group A received the drug for twelve weeks at the full dose. The primary endpoint was flow rate at "
               "week twelve. Adverse events were similar between the two arms. No patient withdrew because of harm "
               "during the study. Baseline residual volume was higher in the control arm at entry.")
        q = ("Group A received the drug for twelve weeks at the full dose ... The primary endpoint was flow rate at "
             "week twelve ... Adverse events were similar between the two arms ... No patient withdrew because of "
             "harm during the study ... the drug cured every patient")
        self.rejected(q, "the drug cured every patient", src=src)
        # a locator label the validator added is not a claim about the source
        ok = q.replace("the drug cured every patient", "(Results section, the second paragraph on harms):")
        self.assertEqual(find_quote(src, ok)["method"], "segments_partial")

    def test_formatting_differences_still_pass(self):
        src = ("Calcium carbonate reduced absorption in three crossover studies17,25 and one cohort study3 of "
               "adults, and the AUC0-48h fell by a fifth in the larger of the two groups that were studied.")
        q = ("Calcium carbonate reduced absorption in three crossover studies and one cohort study of adults, "
             "and the AUC 0-48h fell by a fifth in the larger of the two groups that were studied.")
        r = find_quote(src, q)
        self.assertEqual((r["found"], r["method"]), (True, "fuzzy"), r)   # citation markers and spacing only
        # the same tolerance does not let a real number go: "in 90 patients" -> "in patients"
        self.rejected("The trial enrolled adult patients with hypothyroidism on a stable dose for six months or more.",
                      "number", src="The trial enrolled 90 adult patients with hypothyroidism on a stable dose "
                                    "for six months or more.")
        # a superscript the model wrote as a literal escape
        self.assertTrue(find_quote("Take it after drugs that interfere with absorption.<sup>23</sup> Then wait.",
                                   "Take it after drugs that interfere with absorption.\\u00b2\\u00b3 Then wait.")["found"])

    def test_a_sentence_the_layout_split_is_still_a_quotation(self):
        caption = " ".join(f"Figure 2 panel {i} shows thyrotropin of {i}.5 units and does not differ." for i in range(12))
        src = ("Thirty-one patients preferred the period of bedtime intake. At 1 year " + caption +
               " after completion of the trial, more than half of the patients still preferred bedtime intake.")
        r = find_quote(src, "At 1 year after completion of the trial, more than half of the patients still "
                            "preferred bedtime intake.")
        self.assertEqual((r["found"], r["method"], r["spans"]), (True, "spans", 2), r)
        # but a SHORT skip that hides a negation is the quotation leaving something out
        self.rejected("The switch to bedtime dosing lowered thyrotropin in the second period of the crossover.",
                      src="The switch to bedtime dosing, the authors found, never lowered thyrotropin in the second "
                          "period of the crossover.")

    def test_fragments_stitched_from_all_over_are_not_a_quotation(self):
        src = " ".join(f"Sentence {i} says the measured value stayed flat in group {i} throughout." for i in range(40))
        q = ("Sentence 1 says the group 7 throughout. Sentence 12 says the group 19 throughout. Sentence 23 says "
             "the group 31 throughout. Sentence 33 says the group 38 throughout. Sentence 39 says the measured")
        self.assertFalse(find_quote(src, q)["found"])


# --------------------------------------------------------------------------- #
class FakeLLM:
    """Answers matcher and adjudicator requests from a script; counts what it was asked."""

    def __init__(self, judge, adjudicate=None, drop_first=()):
        self.judge, self.adj, self.drop = judge, adjudicate, set(drop_first)
        self.calls = []

    def call_many(self, reqs):
        out = []
        for r in reqs:
            self.calls.append(r)
            if r.role == "match_adjudicator":
                ds = [{"witness_id": w, **self.adj(w, rec)} for w, rec in r.meta["disputes"].items()]
                out.append(LLMResponse(text="", parsed={"decisions": ds}, key=f"k{len(self.calls)}"))
                continue
            pas = r.meta["pass"]
            js = []
            for w in r.meta["witnesses"]:
                if (pas, w) in self.drop and ":reask" not in r.tag:
                    continue                                   # the long answer left this row out
                j = self.judge(pas, w)
                if j is not None:
                    js.append({"witness_id": w, "trace": "t", **(j if isinstance(j, dict) else {"relation": j})})
            out.append(LLMResponse(text="", parsed={"judgments": js}, key=f"k{len(self.calls)}"))
        return out


def fake_ctx(tmp, llm, **mcfg):
    cfg = {"matching": {"batch_size": 15, "dispute_policy": "adjudicate", "one_pass_policy": "abstain", **mcfg}}
    return types.SimpleNamespace(cfg=cfg, llm=llm, prompts=PromptLibrary(None), frame={"axes": []},
                                 p=lambda *parts: Path(tmp).joinpath(*parts), log=lambda *_: None)


UNIT = {"unit_id": "U1", "hypothesis_id": "H", "axis_id": "A1", "type": "REQUIRED_SUPPORT", "text": "unit text"}


class MatchingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("review-match")

    def tearDown(self):
        cleanup(self.tmp)

    def match(self, llm, wids, **mcfg):
        ctx = fake_ctx(self.tmp, llm, **mcfg)
        wt = {w: f"text of {w}" for w in wids}
        raw = matching.run_passes(ctx, [(UNIT, wids)], {"U1": "unit text"}, wt, "match")
        return {r["witness_id"]: r for r in matching.combine(ctx, raw, {"U1": UNIT}, {"U1": "unit text"}, wt, "match")}

    def test_a_row_a_pass_left_out_is_asked_for_again(self):
        llm = FakeLLM(lambda pas, w: "WITNESS_ENTAILS_UNIT", drop_first={("b", "w2")})
        rows = self.match(llm, ["w1", "w2", "w3"])
        self.assertEqual((rows["w2"]["final"], rows["w2"]["basis"]), ("WITNESS_ENTAILS_UNIT", "AGREED"))
        again = [c for c in llm.calls if ":reask" in c.tag]
        self.assertEqual([(c.meta["pass"], list(c.meta["witnesses"])) for c in again], [("b", ["w2"])])

    def test_one_judgment_is_not_a_dispute(self):
        # pass B never answers for w2, also when asked again: the pair is not adjudicated
        llm = FakeLLM(lambda pas, w: None if (pas, w) == ("b", "w2") else "CONTRADICTS",
                      adjudicate=lambda w, rec: {"relation": "CONTRADICTS"})
        rows = self.match(llm, ["w1", "w2"])
        self.assertEqual((rows["w2"]["final"], rows["w2"]["basis"], rows["w2"]["single_pass_relation"]),
                         ("ABSTAIN", "ONE_PASS_ONLY", "CONTRADICTS"))
        self.assertFalse([c for c in llm.calls if c.role == "match_adjudicator"])
        self.assertEqual(sum(":reask" in c.tag for c in llm.calls), 2)      # asked again twice, then left

    def test_the_adjudicator_chooses_between_the_two_passes(self):
        judge = lambda pas, w: "NO_SEMANTIC_RELATION" if pas == "a" else "PARTIALLY_COVERS"   # noqa: E731
        third = self.match(FakeLLM(judge, lambda w, rec: {"relation": "CONTRADICTS"}), ["w1"])["w1"]
        self.assertEqual((third["final"], third["basis"], third["adjudicator_relation"]),
                         ("ABSTAIN", "DISPUTED", "CONTRADICTS"))
        ok = self.match(FakeLLM(judge, lambda w, rec: {"relation": "PARTIALLY_COVERS", "gap_type": "SCOPE"}), ["w1"])["w1"]
        self.assertEqual((ok["final"], ok["basis"]), ("PARTIALLY_COVERS", "MODEL_ADJUDICATED"))

    def test_a_failed_qualification_pattern_stops_approval_by_adjudication(self):
        judge = lambda pas, w: "WITNESS_ENTAILS_UNIT" if pas == "a" else "NO_SEMANTIC_RELATION"   # noqa: E731
        adj = lambda w, rec: {"relation": "WITNESS_ENTAILS_UNIT"}                                    # noqa: E731
        self.assertEqual(self.match(FakeLLM(judge, adj), ["w1"])["w1"]["basis"], "MODEL_ADJUDICATED")
        write_json(Path(self.tmp) / "matching" / "02_match-fixtures" / "qualification.json",
                   {"unqualified_patterns": ["actor_object_reversal"]})
        held = self.match(FakeLLM(judge, adj), ["w1"])["w1"]
        self.assertEqual((held["final"], held["basis"], held["adjudicator_relation"]),
                         ("ABSTAIN", "UNQUALIFIED_MATCHER", "WITNESS_ENTAILS_UNIT"))
        # what both passes agree on is still approved, and the rule can be switched to disclosure only
        agreed = self.match(FakeLLM(lambda pas, w: "WITNESS_ENTAILS_UNIT"), ["w1"])["w1"]
        self.assertEqual((agreed["final"], agreed["basis"]), ("WITNESS_ENTAILS_UNIT", "AGREED"))
        self.assertEqual(self.match(FakeLLM(judge, adj), ["w1"], unqualified_policy="disclose")["w1"]["basis"],
                         "MODEL_ADJUDICATED")

    def test_a_contradiction_can_depend_on_a_transfer_of_scope(self):
        def judge(pas, w):
            if w == "w1":      # one reviewer says it holds only under a transfer: it is conditional
                return {"relation": "CONTRADICTS", **({"gap_type": "SCOPE", "gap": "volunteers stand for patients"}
                                                      if pas == "b" else {})}
            return "CONTRADICTS"
        rows = self.match(FakeLLM(judge), ["w1", "w2"])
        self.assertEqual((rows["w1"]["gap_type"], rows["w1"]["gap"]), ("SCOPE", "volunteers stand for patients"))
        self.assertNotIn("gap_type", rows["w2"])

    def test_scope_fixtures_are_part_of_qualification(self):
        ids = {f[0]: f for f in matching.FIXTURES}
        self.assertEqual(matching.FIXTURE_CONTRADICTION_GAP, {"FX-23": "SCOPE", "FX-24": ""})
        self.assertEqual(ids["FX-23"][1], ids["FX-24"][1])                  # two fixtures for the pattern (spec 28.1)
        # the local rule engine passes both, so an offline run is not held back by them
        from claimreg.llm.local import _judge
        for fid, need in (("FX-23", "SCOPE"), ("FX-24", "")):
            for strict in (False, True):
                rel, _ = _judge(ids[fid][2], ids[fid][3], strict=strict)
                self.assertIn(rel, ids[fid][4], fid)
                self.assertFalse(rel == "CONTRADICTS" and need == "SCOPE", fid)


# --------------------------------------------------------------------------- #
class CruxTest(unittest.TestCase):
    UNITS = [{"unit_id": u, "hypothesis_id": "R", "active": True, "type": "REQUIRED_SUPPORT"} for u in ("U1", "U2")]

    def rel(self, d, **extra):
        return {k: {"final": v, "basis": "AGREED", "trace": "t", **extra.get(k[0], {})} for k, v in d.items()}

    def theory(self, rel, inc, units=None, **kw):
        units = units or self.UNITS
        pb, info = build_problem("R", units, rel, [], inc, **kw)
        cov = {"options": {u: [{"option_id": o.option_id, "witnesses": list(o.witnesses), "relation": o.relation,
                                "joint": o.joint} for o in pb.options[u]] for u in pb.required},
               "options_truncated": info["options_truncated"], "constraint_violators": pb.constraint_violators}
        return compile_theory("R", units, cov, inc)

    def test_t2_asks_whether_the_surviving_options_can_coexist(self):
        # R needs U1 (a or b) and U2 (c or d); a x d and b x c are incompatible, so R's valid sets
        # are {a, c} and {b, d}.  w is incompatible with a and with d: each unit keeps an option
        # (b for U1, c for U2) but those two cannot be held together.
        rel = self.rel({("a", "U1"): "EQUIVALENT", ("b", "U1"): "EQUIVALENT", ("c", "U2"): "EQUIVALENT",
                        ("d", "U2"): "EQUIVALENT", ("w", "U1"): "NO_SEMANTIC_RELATION",
                        ("w", "U2"): "NO_SEMANTIC_RELATION"})
        inc = [{"a": "a", "b": "d", "approved": True}, {"a": "b", "b": "c", "approved": True},
               {"a": "w", "b": "a", "approved": True}, {"a": "w", "b": "d", "approved": True}]
        pairs = {frozenset((r["a"], r["b"])) for r in inc}
        t2, cert = test_t2("w", self.theory(rel, inc), rel, pairs)
        self.assertEqual((t2, cert["no_joint_arrangement"]), ("FAIL", True))
        # a witness that removes only one of the two sets is accommodated, with a VALID arrangement
        inc2 = inc[:3]
        pairs2 = {frozenset((r["a"], r["b"])) for r in inc2}
        t2, cert = test_t2("w", self.theory(rel, inc2), rel, pairs2)
        self.assertEqual((t2, cert["arrangement_witnesses"]), ("PASS", ["b", "d"]))

    def test_a_cut_option_list_cannot_fail_a_rival(self):
        ws = [f"x{i:02d}" for i in range(13)]
        units = [self.UNITS[0]]
        rel = self.rel({**{(x, "U1"): "EQUIVALENT" for x in ws}, ("w", "U1"): "NO_SEMANTIC_RELATION"})
        inc = [{"a": "w", "b": x, "approved": True} for x in ws[:12]]       # the 13th is compatible with w
        th = self.theory(rel, inc, units=units, max_options=12)
        self.assertEqual(th["options_truncated"], {"U1": 13})
        t2, cert = test_t2("w", th, rel, {frozenset((r["a"], r["b"])) for r in inc})
        self.assertEqual((t2, cert["options_cut_at_cap"]), ("UNKNOWN", {"U1": 13}))
        # without the cap the 13th option is seen and the rival accommodates the witness
        th = self.theory(rel, inc, units=units, max_options=50)
        self.assertEqual(test_t2("w", th, rel, {frozenset((r["a"], r["b"])) for r in inc})[0], "PASS")

    def test_a_rival_with_no_valid_arrangement_is_not_the_witness_s_doing(self):
        rel = self.rel({("a", "U1"): "EQUIVALENT", ("c", "U2"): "EQUIVALENT", ("w", "U1"): "NO_SEMANTIC_RELATION",
                        ("w", "U2"): "NO_SEMANTIC_RELATION"})
        inc = [{"a": "a", "b": "c", "approved": True}]                       # R's only options exclude each other
        t2, cert = test_t2("w", self.theory(rel, inc), rel, {frozenset(("a", "c"))})
        self.assertEqual((t2, cert["rival_has_no_valid_arrangement_regardless"]), ("PASS", True))

    def test_a_crux_that_rests_on_a_transfer_says_so(self):
        gap = {"gap_type": "SCOPE", "gap": "the finding in volunteers holds in the patients the unit is about"}
        rel = self.rel({("a", "U1"): "EQUIVALENT", ("c", "U2"): "EQUIVALENT", ("w", "U1"): "CONTRADICTS",
                        ("w", "U2"): "NO_SEMANTIC_RELATION", ("v", "U1"): "CONTRADICTS",
                        ("v", "U2"): "NO_SEMANTIC_RELATION"}, w=gap)
        th = {**self.theory(rel, []), "constraints": [], "corroborating": [], "adverse": []}
        for wid, expect in (("w", [{"unit_id": "U1", "assumption": gap["gap"]}]), ("v", [])):
            (t1, c1), (t2, c2) = test_t1(wid, th, rel), test_t2(wid, th, rel, set())
            self.assertEqual((t1, t2), ("FAIL", "FAIL"))                    # it still fails both tests
            self.assertEqual(_assumptions(c1, c2), expect)                  # and names what it depends on


# --------------------------------------------------------------------------- #
class ParserTest(unittest.TestCase):
    IDS = ["A1-H1", "A1-H2", "A1-H3"]

    def parse(self, vec):
        res = types.SimpleNamespace(text="```json\n" + json.dumps({"allocations": {"A1": vec}}) + "\n```\n")
        return _parse_assessment(res, 64, "A1", self.IDS)

    def test_only_a_real_division_of_the_gauge_is_accepted(self):
        data, problems = self.parse({"A1-H1": 40, "A1-H2": 14, "A1-H3": 10})
        self.assertEqual((problems, data["allocations"]["A1"]["A1-H1"]), ([], 40))
        for vec, needle in (({"A1-H1": 74, "A1-H2": -10, "A1-H3": 0}, "0 to 64"),
                            ({"A1-H1": 74, "A1-H9": -10}, "does not have"),
                            ({"A1-H1": 64}, "no units stated"),
                            ({"A1-H1": 40.5, "A1-H2": 13.5, "A1-H3": 10}, "whole number"),
                            ({"A1-H1": 40, "A1-H2": 14, "A1-H3": 9}, "sum to 63")):
            data, problems = self.parse(vec)
            self.assertTrue(any(needle in p for p in problems), (vec, problems))
            self.assertNotIn("A1", data["allocations"])                     # never carried into a report
            self.assertEqual(data["rejected_allocations"]["A1"], vec)
        self.assertEqual(check_vector({"A1-H1": 64, "A1-H2": 0, "A1-H3": 0}, self.IDS, 64, "A1")[1], [])


class RetentionTest(unittest.TestCase):
    def test_an_opposing_claim_is_not_a_duplicate(self):
        a = "Bedtime dosing lowered mean TSH compared with morning dosing in the crossover trial of 90 patients."
        self.assertTrue(same_finding(a, "In the crossover trial of 90 patients, bedtime dosing lowered mean TSH "
                                        "compared with morning dosing."))
        for b in ("Bedtime dosing did not lower mean TSH compared with morning dosing in the crossover trial of 90 patients.",
                  "Bedtime dosing raised mean TSH compared with morning dosing in the crossover trial of 90 patients.",
                  "Bedtime dosing lowered mean TSH compared with morning dosing in the crossover trial of 152 patients."):
            self.assertFalse(same_finding(a, b), b)


# --------------------------------------------------------------------------- #
class RunLevelTest(unittest.TestCase):
    """Against a real finished run of the bundled demonstration (offline, no model)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = scratch_dir("review-run")
        cls.proj = cls.tmp / "demo"
        for sub in ("01_CORPUS/source-files", "01_FRAME", "02_RUNS"):
            (cls.proj / sub).mkdir(parents=True)
        for f in sorted((ROOT / "examples" / "demo" / "sources").glob("*.md")):
            shutil.copyfile(f, cls.proj / "01_CORPUS" / "source-files" / f.name)
        shutil.copyfile(ROOT / "examples" / "demo" / "header.md", cls.proj / "01_FRAME" / "header.md")
        write_json(cls.proj / "project.json", {"project": {"name": "review", "run_prefix": "RUN-R"},
                                               "default_provider": "local",
                                               "providers": {"local": {"type": "local", "model": "local-rules"}},
                                               "quest": {"round_size": 4, "max_rounds": 6}})
        out = run_pipeline(RunContext(cls.proj, "RUN-R", create=True, quiet=True))
        assert out["status"] == "complete", out

    @classmethod
    def tearDownClass(cls):
        cleanup(cls.tmp)

    def test_1_a_finished_run_verifies_and_an_empty_one_does_not(self):
        ok = verify_run(self.proj, "RUN-R")
        self.assertEqual((ok["ok"], ok["status"]), (True, "VERIFIED"), ok.get("problems"))
        (self.proj / "02_RUNS" / "RUN-EMPTY").mkdir()
        empty = verify_run(self.proj, "RUN-EMPTY")
        self.assertEqual((empty["ok"], empty["status"]), (False, "NOTHING TO VERIFY"))

    def test_2_a_recorded_file_that_is_gone_is_a_problem(self):
        copy = self.proj / "02_RUNS" / "RUN-COPY"
        shutil.copytree(self.proj / "02_RUNS" / "RUN-R", copy)
        victim = next(p for p in copy.rglob("witnesses.json") if "05_released" in str(p))
        victim.unlink()
        out = verify_run(self.proj, "RUN-COPY")
        self.assertFalse(out["ok"])
        self.assertTrue(any("recorded file is missing" in p and "witnesses.json" in p for p in out["problems"]))

    def test_3_the_report_groups_candidates_by_study_and_shows_direct_coverage(self):
        ctx = RunContext(self.proj, "RUN-R", quiet=True)
        from claimreg import report
        for sc in ctx.scopes():
            d = report._load_all(sc)
            wid = next(iter(d["witnesses"]))
            st = report.study_of(sc, d, wid)
            self.assertEqual((st["study"], st["secondary"]), (d["witnesses"][wid]["source_file"], False))
            # a review restating another file of the corpus is that study; one naming itself is not
            other = next(f for f in sc.corpus.filenames if f != st["study"])
            v = d["vfrds"][d["witnesses"][wid]["vfrd_id"]]
            v["provenance"] = f"DERIVED_FROM({other})"
            self.assertEqual(report.study_of(sc, d, wid), {"study": other, "via": st["study"], "secondary": True,
                                                           "identified": True})
            v["provenance"] = f"DERIVED_FROM({st['study']})"
            self.assertFalse(report.study_of(sc, d, wid)["identified"])
            d["crux"] = {"candidates": [{"witness_id": w, "home": "H", "defeats": ["R"]} for w in list(d["witnesses"])[:3]]}
            groups = report.crux_groups(sc, d)
            self.assertEqual(sum(len(g["candidates"]) for g in groups), 3)
            self.assertIn("required parts covered directly",
                          (Path(sc.p("reports", "CRUX-REPORT.md"))).read_text(encoding="utf-8"))

    def test_4_a_changed_setting_marks_the_stages_it_bears_on(self):
        pj = read_json(self.proj / "project.json")
        pj["retention"] = {"keep_fraction": 0.5}
        pj["providers"]["local"]["model"] = "local-rules-other"            # a model change marks nothing
        write_json(self.proj / "project.json", pj)
        ctx = RunContext(self.proj, "RUN-R", quiet=True)
        out = run_pipeline(ctx)
        st = ctx.stage_state()
        self.assertEqual(out["ran"], [])                                    # nothing is redone unasked
        self.assertNotIn("stale", st["frd_validate"])
        self.assertEqual(st["frd_retain"]["stale"]["because"], ["retention.keep_fraction"])
        self.assertIn("stale", st["report"])
        v = verify_run(self.proj, "RUN-R")
        self.assertIn("frd_retain", v["checks"]["stale_stages"])
        self.assertTrue(any("--from frd_retain" in w for w in v["warnings"]))
        out = run_pipeline(RunContext(self.proj, "RUN-R", quiet=True), start="frd_retain")
        self.assertEqual(out["status"], "complete", out)
        self.assertFalse([n for n, r in RunContext(self.proj, "RUN-R", quiet=True).stage_state().items() if r.get("stale")])


if __name__ == "__main__":
    unittest.main()
