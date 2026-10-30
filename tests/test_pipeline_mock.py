"""End-to-end pipeline on a synthetic mini corpus with the deterministic mock provider."""

import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.pipeline import run_pipeline  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402
from claimreg.util import read_json, write_json  # noqa: E402
from claimreg.verify import verify_run  # noqa: E402
from scratch import cleanup, scratch_dir  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "mini"


def make_project(tmp: Path, provider: str = "mock", extra: dict | None = None) -> Path:
    proj = tmp / "mini"
    (proj / "01_CORPUS").mkdir(parents=True)
    shutil.copytree(FIX / "sources", proj / "01_CORPUS" / "source-files")
    (proj / "01_FRAME").mkdir()
    shutil.copyfile(FIX / "header.md", proj / "01_FRAME" / "header.md")
    shutil.copyfile(FIX / "index.md", proj / "01_FRAME" / "index.md")
    shutil.copyfile(FIX / "archivist.txt", proj / "01_FRAME" / "archivist-custom-prompt.txt")
    cfg = {"project": {"name": "mini"}, "default_provider": provider,
           "quest": {"round_size": 3, "max_rounds": 6}, "budget": {"concurrency": 2}}
    if extra:
        cfg.update(extra)
    write_json(proj / "project.json", cfg)
    return proj


class PipelineMockTest(unittest.TestCase):
    def setUp(self):
        self.tmp = scratch_dir("mock-pipe")

    def tearDown(self):
        cleanup(self.tmp)

    def test_full_pipeline(self):
        proj = make_project(self.tmp)
        ctx = RunContext(proj, "RUN-TEST", create=True, quiet=True)
        out = run_pipeline(ctx)
        self.assertEqual(out["status"], "complete", out)
        st = ctx.stage_state()
        for name in ("frame", "units", "quest", "frd_generate", "frd_validate", "frd_retain",
                     "witnesses", "match", "coverage", "crux", "report"):
            self.assertEqual(st[name]["status"], "done", (name, st[name]))
        qs = ctx.load("discovery", "01_issued-questions/questions.json")
        self.assertTrue(len(qs) >= 3)
        for q in qs:
            self.assertTrue(1 <= len(q["sources_as_sent"]) <= 3)
        closeout = ctx.load("discovery", "06_closeout/closeout.json")
        self.assertIn(closeout["status"], ("SCIENTIFIC_STOP", "OPERATIONAL_LIMIT"))
        cands = ctx.load("frds", "01_candidates/candidates.json")
        per = {}
        for c in cands:
            per[c["qid"]] = per.get(c["qid"], 0) + 1
        self.assertTrue(all(v <= 4 for v in per.values()))
        vals = ctx.load("frds", "05_validated/validated-frds.json")
        self.assertTrue(vals)
        self.assertTrue(all(v["quote_check"]["found"] for v in vals))
        ws = ctx.load("witnesses", "05_released/witnesses.json")
        self.assertTrue(ws)
        self.assertTrue(all(w["words"] <= w["ceiling"] for w in ws))
        rep = (ctx.p("reports", "CRUX-REPORT.md")).read_text(encoding="utf-8")
        self.assertIn("best understood from this corpus and this run", rep)
        self.assertTrue((ctx.p("reports", "report.html")).exists())
        v = verify_run(proj, "RUN-TEST")
        self.assertTrue(v["ok"], v["problems"])
        # rerun is free and identical (everything cached): no new model answer may be needed
        from claimreg.util import read_jsonl
        log = ctx.p("control", "model-and-human-decisions", "llm-calls.jsonl")
        fresh_before = sum(1 for c in read_jsonl(log) if c.get("status") == "ok")
        out2 = run_pipeline(RunContext(proj, "RUN-TEST", quiet=True), force=["report", "assess"])
        self.assertEqual(out2["status"], "complete")
        fresh_after = sum(1 for c in read_jsonl(log) if c.get("status") == "ok")
        self.assertEqual(fresh_before, fresh_after, "a rerun asked the model again (non-deterministic prompt)")
        # a human decision overrides the model relation from coverage onward
        from claimreg.matching import relations_index
        rows = ctx.load("matching", "03_match-records/relations.json")
        r0 = rows[0]
        flip = "CONTRADICTS" if r0["final"] != "CONTRADICTS" else "NO_SEMANTIC_RELATION"
        write_json(ctx.p("matching", "04_disagreements-and-review", "human-decisions.json"),
                   {"decisions": [{"witness_id": r0["witness_id"], "unit_id": r0["unit_id"],
                                   "relation": flip, "reviewer": "test", "note": "override"}]})
        self.assertTrue(ctx.p("matching", "04_disagreements-and-review", "review-packet.md").exists())
        out3 = run_pipeline(RunContext(proj, "RUN-TEST", quiet=True), start="coverage")
        self.assertEqual(out3["status"], "complete")
        self.assertIn("coverage", out3["ran"])        # --from reruns the named stage ...
        self.assertIn("report", out3["ran"])          # ... and everything after it
        idx = relations_index(RunContext(proj, "RUN-TEST", quiet=True))
        got = idx[(r0["witness_id"], r0["unit_id"])]
        self.assertEqual((got["final"], got["basis"], got["model_final"]), (flip, "HUMAN", r0["final"]))
        v = verify_run(proj, "RUN-TEST")
        self.assertTrue(v["ok"], v["problems"])

    def test_queue_roundtrip(self):
        from claimreg.llm.queue_tools import import_responses, list_pending, queue_dir
        proj = make_project(self.tmp, provider="queue")
        ctx = RunContext(proj, "RUN-Q", create=True, quiet=True)
        out = run_pipeline(ctx)
        self.assertEqual(out["status"], "waiting")
        self.assertEqual(out["stage"], "units")
        qd = queue_dir(proj)
        pend = list_pending(qd)
        self.assertTrue(pend)
        # answer the queued requests with the mock and import them
        from claimreg.llm.base import LLMRequest
        from claimreg.llm.mock import MockProvider
        mock = MockProvider("mock", {"model": "mock"}, proj)
        answers = {}
        for b in sorted((qd / "batches").glob("BATCH-*.json")):
            if b.name.endswith(".response.json"):
                continue
            body = read_json(b)
            for r in body["requests"]:
                # the mock needs meta; rebuild it from the frame for unit derivation
                frame = ctx.frame
                hid = r["tag"].split(":", 1)[1]
                h = next(dict(x, axis_id=a["axis_id"]) for a in frame["axes"] for x in a["hypotheses"] if x["id"] == hid)
                req = LLMRequest(role=r["role"], system=r["system"], user=r["user"], meta={"hypothesis": h})
                answers[r["key"]] = mock.complete(req, r["key"]).text
            write_json(b.with_name(b.stem + ".response.json"), {k: answers[k] for k in
                                                                [x["key"] for x in body["requests"]]})
        # leave one request unanswered on purpose and skip it: the stage must still finish
        from claimreg.llm.queue_tools import skip_requests
        skipped = sorted(answers)[0]
        for b in sorted((qd / "batches").glob("BATCH-*.response.json")):
            data = read_json(b)
            if skipped in data:
                data.pop(skipped)
                write_json(b, data)
        rep = import_responses(qd, "mock-via-queue")
        self.assertEqual(rep["accepted"], len(pend) - 1)
        self.assertEqual(skip_requests(qd, [skipped], "test skip")["skipped"], [skipped])
        self.assertFalse(list_pending(qd))
        out2 = run_pipeline(RunContext(proj, "RUN-Q", quiet=True), stop="units")
        self.assertEqual(out2["status"], "complete")
        units = RunContext(proj, "RUN-Q", quiet=True).load("matching", "01_hypothesis-units/units.json")
        self.assertTrue(any(u["active"] for u in units))


if __name__ == "__main__":
    unittest.main()
