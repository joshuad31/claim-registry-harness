"""One study, one voice (claimreg/studies.py), the second reader, and the control run (claimreg/control.py).

Every fixture is topic-neutral: file names, titles, provenance labels and author-year citations.
"""

import json
import shutil
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg import control, studies  # noqa: E402
from claimreg.assess import _second_reading  # noqa: E402
from claimreg.llm.base import LLMRequest, LLMResponse  # noqa: E402
from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import read_json, write_json  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

TEXTS = {
    "smith2010.pdf.md": "# A randomized crossover trial of compound Z in 90 adults\n\nMethods ...",
    "smith2006.pdf.md": "# Compound Z at night: a pilot study\n\nEleven patients ...",
    "jones2015.pdf.md": "![](x.jpg)\n\n# Alternative schedules of compound Z\n\nJONES, LEE AND PARK\n\nCompound Z is ...",
    "lee2017.pdf.md": "# Factors affecting absorption of compound Z: a review\n\nLee et al.",
    "jama-12345.pdf.md": "# Compound Z and diet: a systematic review and meta-analysis\n\n...",
    "smith2010-preprint.md": "# A randomized crossover trial of compound Z in 90 adults (preprint)\n\n...",
    "notes-ai.md": "# My synthesis of the compound Z papers\n\n...",
}


class Corpus:
    filenames = sorted(TEXTS)

    def text(self, f):
        return TEXTS[f]

    def resolve(self, name):
        n = (name or "").strip().strip("`'\"()[] ").lower()
        for f in self.filenames:
            if f.lower() == n or f.lower().split(".")[0] == n.split(".")[0]:
                return f
        return None


CFG = {"corpus": {"duplicates": {"smith2010-preprint.md": "smith2010.pdf.md"}, "synthesis_sources": ["notes-*.md"]}}


def frd(i, src, claim, prov="OWN_RESULT", quote=""):
    return {"vfrd_id": f"FRD-{i}", "source_file": src, "claim": claim, "provenance": prov, "source_text": quote}


class StudyMapTest(unittest.TestCase):
    def setUp(self):
        self.smap = studies.build_map("unused", Corpus(), CFG)

    def test_files_become_studies_and_copies_do_not(self):
        f = self.smap["files"]
        self.assertEqual({k: v["kind"] for k, v in f.items()}, {
            "smith2010.pdf.md": "primary", "smith2006.pdf.md": "primary", "jones2015.pdf.md": "primary",
            "lee2017.pdf.md": "review", "jama-12345.pdf.md": "meta-analysis", "smith2010-preprint.md": "primary",
            "notes-ai.md": "synthesis"})
        self.assertEqual(f["smith2010-preprint.md"]["study"], f["smith2010.pdf.md"]["study"])      # one study, two files
        self.assertEqual(sorted(self.smap["studies"]["STUDY-smith2010"]["files"]),
                         ["smith2010-preprint.md", "smith2010.pdf.md"])
        self.assertEqual(len(self.smap["studies"]), 6)

    def test_a_person_can_correct_the_map_and_the_correction_survives_a_rebuild(self):
        self.smap["overrides"] = {"files": {"jones2015.pdf.md": {"kind": "review"}},
                                  "findings": {"FRD-9": "STUDY-smith2006"}}
        again = studies.build_map("unused", Corpus(), CFG, self.smap)
        self.assertEqual((again["files"]["jones2015.pdf.md"]["kind"], again["files"]["jones2015.pdf.md"]["basis"]),
                         ("review", "override"))
        a = studies.attribute(frd(9, "smith2010.pdf.md", "anything"), again, Corpus())
        self.assertEqual((a["study"], a["role"]), ("STUDY-smith2006", "restated"))

    def attr(self, *a, **k):
        return studies.attribute(frd(*a, **k), self.smap, Corpus())

    def test_a_finding_is_attributed_to_the_study_it_rests_on(self):
        # a trial's own result, even when it mentions another study in passing
        a = self.attr(1, "smith2010.pdf.md", "TSH fell by 1.25 units, in line with Smith et al. (2006).")
        self.assertEqual((a["study"], a["role"]), ("STUDY-smith2010", "direct"))
        # a paper restating a trial, labelled by validation; the label names the paper itself (a known mislabel)
        a = self.attr(2, "jones2015.pdf.md", "Jones et al. (2015) report that in Smith et al. (2010) (n=90) TSH fell.",
                      prov="DERIVED_FROM(jones2015.pdf.md)")
        self.assertEqual((a["study"], a["role"], a["via"]), ("STUDY-smith2010", "restated", "jones2015.pdf.md"))
        # a review mislabelled OWN_RESULT: the source's kind decides, and the quoted passage names the trial
        a = self.attr(3, "lee2017.pdf.md", "A randomized crossover study of 90 patients found better absorption.",
                      quote='Table I: "Smith et al<sup>23</sup> (2010) ... Outcome: lower TSH"')
        self.assertEqual((a["study"], a["role"]), ("STUDY-smith2010", "restated"))
        # a label that names the ancestor by file
        a = self.attr(4, "jones2015.pdf.md", "The pilot found lower TSH.", prov="DERIVED_FROM(smith2006.pdf.md)")
        self.assertEqual((a["study"], a["role"]), ("STUDY-smith2006", "restated"))
        # a review summarising several studies is not a study of its own, and is not either of them
        a = self.attr(5, "lee2017.pdf.md", "Smith 2006 and Smith et al., 2010 both found lower TSH; others did not.")
        self.assertEqual((a["role"], a["summarises"]), ("summary", ["STUDY-smith2006", "STUDY-smith2010"]))
        # a secondary report whose original cannot be identified
        a = self.attr(6, "jones2015.pdf.md", "Four studies gave conflicting results.", prov="DERIVATIVE_UNKNOWN")
        self.assertEqual((a["study"], a["role"]), ("STUDY-jones2015", "secondary"))
        # similar author, different year: not the same study
        a = self.attr(7, "lee2017.pdf.md", "Smith et al. (2012) found no difference.")
        self.assertEqual(a["role"], "secondary")

    def test_witnesses_are_counted_as_the_studies_they_are(self):
        attrs = [self.attr(1, "smith2010.pdf.md", "a"), self.attr(2, "smith2010.pdf.md", "b"),
                 self.attr(3, "lee2017.pdf.md", "As Smith et al. (2010) showed, c."),
                 self.attr(4, "smith2006.pdf.md", "d"),
                 self.attr(5, "jones2015.pdf.md", "Studies conflict.", prov="DERIVATIVE_UNKNOWN")]
        c = studies.count(attrs)
        self.assertEqual((c["items"], c["studies"], c["secondary_reports"]),
                         (5, ["STUDY-smith2006", "STUDY-smith2010"], ["jones2015.pdf.md"]))
        self.assertEqual(studies.phrase(c), "5 witnesses from 2 studies and 1 secondary report")
        block = studies.studies_block({f"W{i}": a for i, a in enumerate(attrs, 1)})
        self.assertIn("STUDY-smith2010: W1, W2, W3  (some restated in lee2017.pdf.md)", block)
        self.assertIn("STUDY-jones2015 [secondary report]: W5", block)

    def test_drivers_that_lean_on_one_study_twice_are_noticed(self):
        attrs = {"W-A-1": self.attr(1, "smith2010.pdf.md", "a"), "W-A-10": self.attr(2, "smith2010.pdf.md", "b"),
                 "W-B-1": self.attr(3, "smith2006.pdf.md", "c")}
        au = studies.driver_audit([{"frd_id": "W-A-1", "favors": "H1", "why": "x"},
                                   {"frd_id": "W-A-10", "favors": "H1", "why": "y"}, "W-B-1: supports H1"], attrs)
        self.assertEqual((au["rows_cited"], au["effective_studies"]), (3, 2))
        self.assertEqual(au["one_study_cited_as_several_drivers"],
                         [{"study": "STUDY-smith2010", "favors": "H1", "drivers": 2, "rows": ["W-A-1", "W-A-10"]}])

    def test_drivers_that_name_studies_instead_of_rows_are_audited_too(self):
        attrs = {"W-A-1": self.attr(1, "smith2010.pdf.md", "a"), "W-A-10": self.attr(2, "smith2010.pdf.md", "b"),
                 "W-B-1": self.attr(3, "smith2006.pdf.md", "c")}
        au = studies.driver_audit([{"study": "STUDY-smith2010", "favors": "H1", "why": "the crossover"},
                                   {"study": "STUDY-smith2010", "favors": "H1", "why": "its TSH result"},
                                   {"study": "STUDY-smith2006", "favors": "H1", "why": "x"},
                                   {"favors": "H2", "why": "general clinical experience"}], attrs)
        self.assertTrue(au["checked"])
        self.assertEqual((au["rows_cited"], au["effective_studies"], au["drivers_naming_no_row_or_study"]), (0, 2, [4]))
        self.assertEqual(au["one_study_cited_as_several_drivers"],
                         [{"study": "STUDY-smith2010", "favors": "H1", "drivers": 2, "rows": []}])
        # one driver that cites two rows of one study is one driver, and is not flagged
        self.assertEqual(studies.driver_audit(["W-A-1 and W-A-10 agree"], attrs)["one_study_cited_as_several_drivers"], [])
        # drivers that name nothing are reported as unchecked, never as clean
        self.assertFalse(studies.driver_audit(["the weight of the evidence"], attrs)["checked"])

    def test_a_label_or_a_regulators_document_is_not_a_study(self):
        self.assertEqual(studies.guess_kind("# HIGHLIGHTS OF PRESCRIBING INFORMATION\nSynthroid tablets"), "label")
        self.assertEqual(studies.guess_kind("# FDA Clinical Pharmacology Review\nNDA 021402"), "regulatory")
        self.assertEqual(studies.guess_kind("# An open-label crossover trial of bedtime dosing"), "primary")
        self.assertIn("label", studies.SECONDARY_KINDS)


class SecondReaderTest(unittest.TestCase):
    def ctx(self, same: bool, mode: str = "auto"):
        prov = lambda n, m: types.SimpleNamespace(name=n, model=m)                                      # noqa: E731
        asked = []

        def call_many(reqs):
            asked.extend(reqs)
            return [LLMResponse(text='```json\n{"allocations": {"A1": {"A1-H1": 30, "A1-H2": 14, "A1-H3": 20}}}\n```')
                    for _ in reqs]
        llm = types.SimpleNamespace(call_many=call_many, provider_for=lambda role: prov("deepseek", "d1") if (
            same or role == "assessor") else prov("gemini", "g1"))
        return types.SimpleNamespace(cfg={"assess": {"second_reader": mode}}, llm=llm), asked

    def read(self, ctx):
        reqs = [LLMRequest(role="assessor", system="s", user="u", tag="final-assessment-A1")]
        return _second_reading(ctx, reqs, ["A1"], {"A1": ["A1-H1", "A1-H2", "A1-H3"]}, 64,
                               {"A1": {"A1-H1": 40, "A1-H2": 14, "A1-H3": 10}}, [])

    def test_a_different_model_reads_the_same_assessment(self):
        ctx, asked = self.ctx(same=False)
        out = self.read(ctx)
        self.assertEqual((asked[0].role, asked[0].system, asked[0].user), ("assessor_b", "s", "u"))     # identical question
        self.assertEqual((out["model"], out["allocations"]["A1"]["A1-H1"], out["difference_from_first"]["A1"]),
                         ("gemini/g1", 30, 10))

    def test_no_second_reading_when_no_second_model_is_set_up(self):
        ctx, asked = self.ctx(same=True)
        out = self.read(ctx)
        self.assertEqual((asked, list(out)), ([], ["skipped"]))            # one reader, and it says so
        self.assertIn("same model", out["skipped"])
        ctx, asked = self.ctx(same=False, mode="off")
        self.assertEqual((self.read(ctx), asked), ({}, []))
        ctx, asked = self.ctx(same=True, mode="on")                       # asked for explicitly: the same model twice
        self.assertEqual(len(asked) + (1 if self.read(ctx) else 0), 1)


class RunLevelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = scratch_dir("studies-run")
        cls.proj = cls.tmp / "demo"
        for sub in ("01_CORPUS/source-files", "01_FRAME", "02_RUNS"):
            (cls.proj / sub).mkdir(parents=True)
        for f in sorted((ROOT / "examples" / "demo" / "sources").glob("*.md")):
            shutil.copyfile(f, cls.proj / "01_CORPUS" / "source-files" / f.name)
        shutil.copyfile(ROOT / "examples" / "demo" / "header.md", cls.proj / "01_FRAME" / "header.md")
        write_json(cls.proj / "project.json", {"project": {"name": "studies", "run_prefix": "RUN-S"},
                                               "default_provider": "local",
                                               "providers": {"local": {"type": "local", "model": "local-rules"}},
                                               "quest": {"round_size": 4, "max_rounds": 6}})
        out = run_pipeline(RunContext(cls.proj, "RUN-S", create=True, quiet=True))
        assert out["status"] == "complete", out
        pj = read_json(cls.proj / "project.json")                # the parent project has a hypothesis it wants
        pj["coach"] = {"preferred": {"A1": "A1-H1"}}
        write_json(cls.proj / "project.json", pj)

    @classmethod
    def tearDownClass(cls):
        cleanup(cls.tmp)

    def test_a_run_records_studies_beside_witnesses_everywhere(self):
        ctx = RunContext(self.proj, "RUN-S", quiet=True)
        self.assertTrue((self.proj / "01_FRAME" / studies.MAP_JSON).exists())      # built on first use
        for sc in ctx.scopes():
            of = studies.witness_studies(sc)
            ws = sc.load("witnesses", "05_released/witnesses.json")
            self.assertEqual(set(of), {w["witness_id"] for w in ws})
            cov = sc.load("coverage", "coverage.json")["hypotheses"]
            for res in cov.values():
                self.assertIn("coverage is decided from text", res["studies"]["note"])
            self.assertIn("candidates_by_study", sc.load("crux", "05_candidates/crux-candidates.json"))
            a = sc.load("reports", "assessment.json")
            self.assertTrue(a["study_identity"]["given_to_assessor"])
            self.assertNotIn("second_reading", a)                                  # one model: one reading
            m = json.loads(Path(sc.p("reports", "metrics.json")).read_text(encoding="utf-8"))
            self.assertEqual(m["studies_behind_witnesses"], studies.count(of.values())["n_studies"])
            self.assertLessEqual(m["studies_behind_witnesses"], len(sc.corpus.filenames))
            self.assertIn("they rest on", Path(sc.p("reports", "CRUX-REPORT.md")).read_text(encoding="utf-8"))

    def test_study_identity_never_changes_coverage(self):
        ctx = RunContext(self.proj, "RUN-S", quiet=True)
        from claimreg.coverage import coverage_stage
        for sc in ctx.scopes():
            before = {h: (c["status"], sorted(tuple(s["witnesses"]) for s in c["sets"]))
                      for h, c in sc.load("coverage", "coverage.json")["hypotheses"].items()}
            # call every witness a restatement of one study: the sets must be exactly the same
            smap = studies.load_map(sc)
            smap["overrides"]["findings"] = {v["vfrd_id"]: "STUDY-one" for v in sc.load("frds", "05_validated/retained-frds.json")}
            sc._study_map = smap
            coverage_stage(sc)
            after = sc.load("coverage", "coverage.json")["hypotheses"]
            self.assertEqual(before, {h: (c["status"], sorted(tuple(s["witnesses"]) for s in c["sets"]))
                                      for h, c in after.items()})

    def test_a_control_has_the_same_corpus_and_no_one_to_root_for(self):
        dst = self.tmp / "control"
        parent = read_json(self.proj / "project.json")
        parent["notebooklm"] = {"notebooks": ["https://notebooklm.google.com/notebook/parent-conversation-0001"],
                                "profile_dir": "p"}
        write_json(self.proj / "project.json", parent)
        out = control.make_control(self.proj, dst)
        cfg = read_json(dst / "project.json")
        # the parent's notebooks hold the parent's conversation, so the control starts without them
        self.assertEqual((cfg["notebooklm"], out["notebook_links_not_carried_over"]), ({"notebooks": [], "profile_dir": "p"}, 1))
        self.assertEqual(len(read_json(self.proj / "project.json")["notebooklm"]["notebooks"]), 1)
        # `cr frame` needs a question file, and must refuse until the researcher has written one
        self.assertIn("REPLACE", (dst / "01_FRAME" / "question.md").read_text(encoding="utf-8"))
        self.assertEqual((cfg["coach"]["enabled"], cfg["coach"]["preferred"], cfg["coach"]["require_acceptance"]),
                         (False, {}, False))
        self.assertEqual(Path(cfg["corpus"]["source_dir"]), (self.proj / "01_CORPUS" / "source-files").resolve())
        self.assertFalse((dst / "01_FRAME" / "header.md").exists())                # its own question, not the parent's
        self.assertTrue((dst / "01_FRAME" / control.NOTE).exists())
        self.assertIn("STUDY-MAP.json", out["copied"])
        self.assertEqual(read_json(self.proj / "project.json")["coach"]["preferred"], {"A1": "A1-H1"})   # parent untouched
        with self.assertRaises(FileExistsError):
            control.make_control(self.proj, dst)

    def test_the_shape_of_two_runs_can_be_set_side_by_side(self):
        ctx = RunContext(self.proj, "RUN-S", quiet=True)
        shapes = control.run_shape(ctx)
        s = next(iter(shapes.values()))
        self.assertEqual(s["pairs_both_passes_answered_pct"], 100.0)
        self.assertGreater(s["witnesses_per_study"], 1)
        text = control.render([("parent", s), ("control", s)])
        self.assertIn("| Studies behind the witnesses |", text)
        self.assertIn("Scores for different questions cannot be compared", text)


class SplitPiecesTest(unittest.TestCase):
    """A source split into ``-pNN`` pieces is one study, with or without the harness's split metadata."""

    def test_pieces_group_by_file_name_when_metadata_is_absent(self):
        texts = {"briggs2008-p01.md": "# Alpha\n\n...", "briggs2008-p02.md": "# Alpha\n\n...",
                 "briggs2008-p03.md": "# Alpha\n\n...", "solo2011.md": "# Beta\n\n..."}
        corpus = types.SimpleNamespace(filenames=sorted(texts), text=lambda f: texts[f],
                                       resolve=lambda name: None)
        smap = studies.build_map("unused", corpus, {})
        self.assertEqual(smap["files"]["briggs2008-p02.md"]["study"], "STUDY-briggs2008")
        self.assertEqual(smap["files"]["briggs2008-p02.md"]["study_basis"], "file name")
        self.assertEqual(smap["files"]["solo2011.md"]["study"], "STUDY-solo2011")
        self.assertNotIn("study_basis", smap["files"]["solo2011.md"])
        self.assertIn("STUDY-briggs2008", smap["studies"])
        self.assertEqual(len(smap["studies"]["STUDY-briggs2008"]["files"]), 3)

    def test_split_metadata_wins_over_the_name(self):
        texts = {"a-part-p01.md": "# Gamma\n\n...", "a-part-p02.md": "# Gamma\n\n..."}
        by_name = {"a-part-p01.md": {"split_origin": {"original_filename": "a-part.md", "part": 1}},
                   "a-part-p02.md": {"split_origin": {"original_filename": "a-part.md", "part": 2}}}
        corpus = types.SimpleNamespace(filenames=sorted(texts), text=lambda f: texts[f],
                                       resolve=lambda name: None, by_name=by_name)
        smap = studies.build_map("unused", corpus, {})
        self.assertEqual({v["study"] for v in smap["files"].values()}, {"STUDY-a-part"})
        self.assertEqual(smap["files"]["a-part-p02.md"]["study_basis"], "split metadata")


if __name__ == "__main__":
    unittest.main()
