"""One evidence database per axis (docs/AXIS-DATABASES.md)."""

import json
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fakes  # noqa: E402
from claimreg import axes  # noqa: E402
from claimreg.header import parse_header  # noqa: E402
from claimreg.notebooklm.relay import Relay, ready_questions  # noqa: E402
from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.quest_import import import_quest  # noqa: E402
from claimreg.runctx import AXIS_LAYOUT, RunContext, axis_folder_name  # noqa: E402
from claimreg.util import read_json, write_json  # noqa: E402
from claimreg.verify import verify_run  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402
from test_pipeline_mock import FIX, make_project  # noqa: E402
from test_relay import SECRET, FakeDriver, question  # noqa: E402


def two_axis_header() -> str:
    text = (FIX / "header.md").read_text(encoding="utf-8")
    start, end = text.index("### **axis one:**"), text.index("## 3. Decisive-test map")
    block = text[start:end]
    one = block.replace("### **axis one:**", "### Axis one — flow improvement")
    two = block.replace("### **axis one:**", "### Axis two — tissue exposure").replace("A1-", "A2-")
    return text[:start] + one + two + text[end:]


def two_axis_project(tmp: Path, **kw) -> Path:
    proj = make_project(tmp, **kw)
    (proj / "01_FRAME" / "header.md").write_text(two_axis_header(), encoding="utf-8")
    return proj


def by_parity(ctx, questions):
    """Stand-in for the Investigator's choice: odd questions were asked for A1, even ones for A2."""
    return {q["qid"]: {"axis": "A1" if int(q["qid"][1:]) % 2 else "A2", "axis_source": "investigator"}
            for q in questions}


class AxisHelpersTest(unittest.TestCase):
    def test_header_gives_each_axis_a_name_and_a_folder(self):
        fr = parse_header(two_axis_header())
        self.assertEqual([a["axis_id"] for a in fr["axes"]], ["A1", "A2"])
        self.assertEqual(fr["axes"][1]["name"], "tissue exposure")
        self.assertEqual(axis_folder_name(fr["axes"][0]), "AXIS-A1__flow-improvement")
        self.assertEqual(axis_folder_name(fr["axes"][1], {"A2": "Exposure in tissue"}), "AXIS-A2__exposure-tissue")

    def test_a_question_is_filed_under_exactly_one_axis(self):
        self.assertEqual(axes.labelled_axis("A2 trial results", ["A1", "A2"]), "A2")
        self.assertIsNone(axes.labelled_axis("A1 and A2 overlap", ["A1", "A2"]))      # two axes named: not a label
        self.assertIsNone(axes.labelled_axis("exposure", ["A1", "A2"]))
        fr = {"axes": [{"axis_id": "A1", "name": "bedtime dosing", "question": "Does bedtime dosing lower TSH?",
                        "hypotheses": []},
                       {"axis_id": "A2", "name": "oral solution", "question": "Does the liquid formulation help?",
                        "hypotheses": []}], "decisive_tests": []}
        self.assertEqual(axes.lexical_axis(fr, "TSH after evening or bedtime dosing in the crossover trial"), "A1")
        self.assertEqual(axes.lexical_axis(fr, "absorption of the liquid formulation versus tablets"), "A2")

    def test_ready_questions_carry_their_axis_and_never_show_it_to_the_notebook(self):
        qs = ready_questions("## Ready questions\n1. [axis: A2] [target: exposure] " + question(1) + "\n"
                             "2. [target: A1 flow] " + question(2) + "\n")
        self.assertEqual([(q["axis"], q["target"]) for q in qs], [("A2", "exposure"), (None, "A1 flow")])
        self.assertFalse(any("[axis" in q["text"] or "[target" in q["text"] for q in qs))


class AxisPipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("axes-pipe")

    def tearDown(self):
        cleanup(self.tmp)

    def run_two_axes(self, **extra):
        proj = two_axis_project(self.tmp, **extra)
        ctx = RunContext(proj, "RUN-AX", create=True, quiet=True)
        with mock.patch.object(axes, "assign_axes", by_parity):
            out = run_pipeline(ctx)
        self.assertEqual(out["status"], "complete", out)
        return ctx

    def test_every_axis_has_its_own_database_and_no_file_mixes_axes(self):
        ctx = self.run_two_axes()
        self.assertEqual(ctx.run_config["layout"], AXIS_LAYOUT)
        top = sorted(p.name for p in ctx.run_dir.iterdir())
        self.assertEqual(top, ["00_RUN-CONTROL", "01_FRAME", "AXIS-A1__flow-improvement", "AXIS-A2__tissue-exposure",
                               "FRD-EVALUATION.md", "RUN-CONFIG.json", "RUN-MAP.md", "RUN-STATUS.md", "SHARED",
                               "frd-evaluation.json"])
        a1, a2 = ctx.scopes()
        owners = {}
        for sc in (a1, a2):
            me = sc.axis_id
            qs = sc.load("discovery", "01_issued-questions/questions.json")
            self.assertTrue(qs)
            self.assertEqual({q["axis"] for q in qs}, {me})
            qids = {q["qid"] for q in qs}
            for qid in qids:
                owners.setdefault(qid, set()).add(me)
            self.assertTrue(all(r["qid"] in qids and r["axis"] == me
                                for r in sc.load("discovery", "02_query-responses/responses.json")))
            for rel in ("01_candidates/candidates.json", "04_validation-results/validations.json",
                        "05_validated/validated-frds.json", "05_validated/retained-frds.json"):
                rows = sc.load("frds", rel)
                self.assertTrue(rows, rel)
                self.assertTrue(all(r["qid"] in qids for r in rows), rel)
            ws = sc.load("witnesses", "05_released/witnesses.json")
            self.assertTrue(ws)
            self.assertTrue(all(w["qid"] in qids for w in ws))
            units = sc.load("matching", "01_hypothesis-units/units.json")
            self.assertTrue(all(u["hypothesis_id"].startswith(me + "-") for u in units))
            own_w = {w["witness_id"] for w in ws}
            rels = sc.load("matching", "03_match-records/relations.json")
            self.assertTrue(all(r["witness_id"] in own_w and r["axis_id"] == me for r in rels))
            self.assertEqual(set(sc.load("coverage", "coverage.json")["hypotheses"]), {f"{me}-H1", f"{me}-H2", f"{me}-H3"})
            for doc in (("reports", "CRUX-REPORT.md"), ("reports", "report.html"), ("coverage", "PREMISE-LEDGER.md")):
                self.assertTrue(sc.p(*doc).exists(), doc)
            self.assertIn(f"belongs to axis {me} and to no other axis", (sc.root / "AXIS.md").read_text(encoding="utf-8"))
            # nothing in an axis folder names the other axis's hypotheses
            other = "A2-H" if me == "A1" else "A1-H"
            for f in sc.root.rglob("*"):
                if f.is_file() and f.suffix in (".json", ".md", ".html"):
                    self.assertNotIn(other, f.read_text(encoding="utf-8", errors="replace"), f)
        self.assertTrue(all(len(v) == 1 for v in owners.values()))            # no question is in two databases
        # the quest's cross-axis records are SHARED, and no question or answer is left there
        sh = ctx.shared().p("discovery")
        self.assertTrue((sh / "06_closeout" / "closeout.json").exists())
        self.assertFalse(list(sh.rglob("questions.json")) + list(sh.rglob("responses.json")) + list(sh.rglob("Q0*")))

    def test_cross_axis_relations_are_shared_records_and_reach_the_axis_they_bear_on(self):
        ctx = self.run_two_axes()
        a1, a2 = ctx.scopes()
        own = {sc.axis_id: {w["witness_id"] for w in sc.load("witnesses", "05_released/witnesses.json")} for sc in (a1, a2)}
        for me, other in (("A1", "A2"), ("A2", "A1")):
            cross = axes.cross_relations(ctx, me)
            self.assertTrue(cross, "the other axis's witnesses were matched against this axis's units")
            self.assertTrue(all(r["witness_id"] in own[other] and r["axis_id"] == me for r in cross))
            self.assertTrue((ctx.axis_dir("SHARED") / f"CROSS-AXIS-into-{me}" / "07_MATCHING").is_dir())
        # the two axes share their wording in this fixture, so cross-axis witnesses do bear on the units:
        # a later stage of A1 sees them, labelled with their home axis, without A1's own files holding them
        a1.merge_shared = True
        merged = a1.load("witnesses", "05_released/witnesses.json")
        foreign = [w for w in merged if w.get("home_axis")]
        self.assertTrue(foreign)
        self.assertEqual({w["home_axis"] for w in foreign}, {"A2"})
        a1.merge_shared = False
        self.assertFalse([w for w in a1.load("witnesses", "05_released/witnesses.json") if w.get("home_axis")])
        # "A1's folder + SHARED/CROSS-AXIS-into-A1" is everything that bears on A1: the foreign
        # witnesses' records are staged there (not only their relations), labelled with their home
        ev = ctx.axis_dir("SHARED") / "CROSS-AXIS-into-A1" / "EVIDENCE"
        staged = read_json(ev / "witnesses.json")
        self.assertEqual({w["witness_id"] for w in staged}, {w["witness_id"] for w in foreign})
        self.assertEqual({w["home_axis"] for w in staged}, {"A2"})
        self.assertTrue(read_json(ev / "retained-frds.json") and read_json(ev / "questions.json")
                        and read_json(ev / "query-responses.json"))
        # which axes does a record belong to?  One file answers it.
        mem = [json.loads(x) for x in (ctx.axis_dir("SHARED") / "MEMBERSHIP.jsonl").read_text(encoding="utf-8").splitlines()]
        wm = {m["item_id"]: m for m in mem if m["kind"] == "witness"}
        self.assertEqual(wm[staged[0]["witness_id"]]["home_axis"], "A2")
        self.assertEqual(sorted(wm[staged[0]["witness_id"]]["axes"]), ["A1", "A2"])
        self.assertEqual(sum(1 for m in mem if m["kind"] == "shared-resource"), 5)
        self.assertEqual(ctx.stage_state()["match"]["summary"]["SHARED"]["into-A1"]["units"] > 0, True)

    def test_the_dictionary_and_canonicalizer_are_one_shared_resource(self):
        ctx = self.run_two_axes(extra={"language": {"mode": "labels"}})
        shared = ctx.axis_dir("SHARED") / "04_LANGUAGE-TOOLS"
        self.assertEqual(read_json(shared / "LANGUAGE-STATUS.json")["mode"], "labels")
        self.assertTrue((shared / "02_dictionary" / "dictionary-entries.json").exists())
        self.assertTrue((shared / "03_canonicalizer" / "rulebook.md").exists())
        self.assertFalse(list(ctx.run_dir.glob("AXIS-*/04_LANGUAGE-TOOLS")))        # no per-axis copies
        self.assertNotIn("A1", ctx.stage_state()["language"]["summary"])           # the stage ran once
        for sc in ctx.scopes():                                                    # every axis used it
            tc = sc.load("transcoding", "transcoded.json")
            self.assertEqual(tc["mode"], "labels")
            self.assertTrue(tc["items"])

    def test_cross_axis_evidence_can_be_turned_off(self):
        ctx = self.run_two_axes(extra={"axes": {"cross_axis_evidence": False}})
        self.assertFalse(list(ctx.axis_dir("SHARED").glob("CROSS-AXIS-*")))
        self.assertNotIn("SHARED", ctx.stage_state()["match"]["summary"])

    def test_whole_run_tools_read_across_the_axis_databases(self):
        ctx = self.run_two_axes()
        n = sum(len(sc.load("witnesses", "05_released/witnesses.json")) for sc in ctx.scopes())
        self.assertEqual(len(ctx.load("witnesses", "05_released/witnesses.json")), n)
        v = verify_run(ctx.project_dir, ctx.run_id)
        self.assertTrue(v["ok"], v.get("problems"))
        self.assertIn("report_words_A1", v["checks"])
        # the databases add up to the run: nothing is unassigned and nothing is counted twice
        ax = v["checks"]["axis_databases"]
        self.assertEqual(ax["unassigned"], 0)
        self.assertIn(ax["quest_questions"], (None, ax["totals"]["questions"]))   # None: this quest kept no count
        self.assertEqual(ax["totals"]["witnesses"], n)
        self.assertEqual(ax["totals"]["questions"], sum(d["questions"] for d in ax["by_axis"].values()))
        # shared resources are declared, exist once, and no axis folder holds a copy
        declared = ctx.run_config["shared_resources"]
        self.assertEqual(len(declared), 5)
        self.assertEqual(ax["shared_resource_copies_in_axis_folders"], [])
        self.assertTrue((ctx.axis_dir("SHARED") / "07_MATCHING" / "02_match-fixtures" / "qualification.json").exists())
        self.assertFalse(list(ctx.run_dir.glob("AXIS-*/07_MATCHING/02_match-fixtures")))
        self.assertNotIn("A1", ctx.stage_state()["qualify"]["summary"])            # qualified once, not per axis
        # a record filed twice, or a shared tool copied into an axis, is reported
        a1, a2 = ctx.scopes()
        ws = a1.load("witnesses", "05_released/witnesses.json")
        write_json(a2.p("witnesses", "05_released/witnesses.json"),
                   a2.load("witnesses", "05_released/witnesses.json") + [ws[0]])
        (a1.root / "04_LANGUAGE-TOOLS").mkdir()
        bad = verify_run(ctx.project_dir, ctx.run_id)
        self.assertTrue(any("is in both A1 and A2" in p for p in bad["problems"]))
        self.assertTrue(any("shared resource copied into an axis folder" in p for p in bad["problems"]))

    def test_an_axis_nobody_asked_about_still_gets_an_empty_database(self):
        proj = two_axis_project(self.tmp)
        ctx = RunContext(proj, "RUN-AX", create=True, quiet=True)
        everything_a1 = lambda c, qs: {q["qid"]: {"axis": "A1", "axis_source": "investigator"} for q in qs}  # noqa: E731
        with mock.patch.object(axes, "assign_axes", everything_a1):
            out = run_pipeline(ctx)
        self.assertEqual(out["status"], "complete", out)
        a2 = ctx.for_axis("A2")
        self.assertEqual(a2.load("discovery", "01_issued-questions/questions.json"), [])
        self.assertTrue(a2.p("reports", "CRUX-REPORT.md").exists())

    def test_single_database_layout_is_still_available_and_old_runs_still_read(self):
        proj = make_project(self.tmp, extra={"axes": {"separate_databases": False}})
        ctx = RunContext(proj, "RUN-OLD", create=True, quiet=True)
        self.assertFalse(ctx.axis_layout)
        out = run_pipeline(ctx)
        self.assertEqual(out["status"], "complete", out)
        self.assertTrue(ctx.p("reports", "CRUX-REPORT.md").exists())
        self.assertFalse(list(ctx.run_dir.glob("AXIS-*")))


class Script2:
    """A scripted Manager + Investigator for a two-axis quest."""

    def __init__(self):
        self.n = 100

    def __call__(self, req, prov):
        if req.role == "quest_investigator":
            self.prompt = req.system + req.user
            k = int(re.search(r"Write the next (\d+) questions", req.user).group(1))
            self.n += k
            qs = [{"axis": "A1" if i % 2 else "A2", "target": "exposure", "sources": [],
                   "text": question(self.n + i, 1 + i % 2)} for i in range(k)]
            # a question that names no axis, and one whose target names two: both must be refused
            qs.append({"target": "exposure", "sources": [], "text": question(self.n + 50, 1)})
            qs.append({"target": "A1 and A2 overlap", "sources": [], "text": question(self.n + 51, 1)})
            return {"questions": qs}
        rid = req.meta["round"]
        if req.tag.startswith("assess"):
            v = {"H1": 30, "H2": 14, "H3": 20}
            return (f"<<<FRAGMENT\nnew cards for {rid}\nFRAGMENT>>>\n<<<STATE\n{SECRET} " + "state word " * 40
                    + "\nSTATE>>>\n<<<JSON\n" + json.dumps({"round": rid, "vectors": {"A1": v, "A2": v},
                                                            "stop_eligible": False, "direction": "CONTINUE",
                                                            "repairs": []}) + "\nJSON>>>")
        self.n += 10
        qs = "\n".join(f"{k + 1}. [axis: A{1 + k % 2}] [target: functional link] {question(self.n + k, 1 + k % 2)}"
                       for k in range(8))
        return (f"# {rid} feedback packet\n\n**Direction: CONTINUE**\n\n## Novelty notes\n- new\n\n"
                f"## Open priorities\n1. gap\n\n## Answers needing a repair re-ask\nNone\n\n## Ready questions\n{qs}\n")


class AxisRelayTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("axes-relay")
        fakes.reset()
        self.driver = None

    def tearDown(self):
        if self.driver:
            self.driver.halt = True
        cleanup(self.tmp)

    def test_every_question_names_one_axis_and_is_filed_there(self):
        s = Script2()
        fakes.SCRIPTS.update({"m": s})
        proj = two_axis_project(self.tmp, extra={
            "roles": {"quest_manager": "m", "quest_investigator": "m"},
            "providers": {"m": {"type": "scripted", "model": "model-m", "script": "m"}},
            "budget": {"retries": 0, "concurrency": 2}})
        q = proj / "quest" / "Q1"
        q.mkdir(parents=True)
        write_json(q / "quest.json", {
            "run_id": "T-QUEST", "project": "../..", "answers_dir": "answers",
            "assessed_file": "answers/assessed-qids.json", "notebooks": {"primary": "https://x/notebook/abc"},
            "round_size": 6, "max_questions": 12, "queue_ahead": 6, "poll_seconds": 0.02, "max_wait_seconds": 5,
            "drain_minutes": 0.05, "max_hours": 1, "investigator_min_interval": 0})
        r = Relay(q / "quest.json", echo=False)
        self.driver = FakeDriver(r.answers)
        self.driver.start()
        st = r.run(max_seconds=60)
        self.assertEqual(st["questions_asked"], 12)
        self.assertEqual(sum(v["asked"] for v in st["by_axis"].values()), 12)
        self.assertTrue(all(v["asked"] > 0 for v in st["by_axis"].values()))
        # the Investigator is told to choose one axis, and is shown the axes
        self.assertIn("exactly ONE axis", s.prompt)
        self.assertIn("A2: tissue exposure", s.prompt)
        # questions are kept per axis; there is no mixed list
        self.assertFalse((q / "asked.jsonl").exists())
        for a in ("A1", "A2"):
            rows = [json.loads(x) for x in (q / f"AXIS-{a}" / "asked.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertTrue(rows)
            self.assertEqual({x["axis"] for x in rows}, {a})
            self.assertTrue(list((r.ws / "answers" / f"AXIS-{a}").glob("Q*.md")))
        # a question with no single axis was refused, and says why
        rej = [json.loads(x) for x in (q / "rejected.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertTrue(rej)
        self.assertTrue(all(any("exactly one axis" in w for w in x["warnings"]) for x in rej))
        # what reaches the notebook page is the question alone
        for f in r.queue.glob("Q*.json"):
            self.assertEqual(sorted(read_json(f)), ["attempt", "qid", "text"])
        # imported into a run, each question keeps the axis its author chose
        self.driver.halt = True
        res = import_quest(proj, q, run_id="RUN-IMP")
        ctx = RunContext(proj, "RUN-IMP", quiet=True)
        chosen = res["by_axis"]
        self.assertEqual(sum(v["questions"] for v in chosen.values()), 12)
        for sc in ctx.scopes():
            qs = sc.load("discovery", "01_issued-questions/questions.json")
            self.assertTrue(qs)
            self.assertEqual({(x["axis"], x["axis_source"]) for x in qs}, {(sc.axis_id, "investigator")})


if __name__ == "__main__":
    unittest.main()
