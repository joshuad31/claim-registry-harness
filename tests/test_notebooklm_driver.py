"""End-to-end test of the NotebookLM driver against a local mock notebook page.

Run directly:  python tests/test_notebooklm_driver.py   (cr selftest skips it unless CR_BROWSER_TESTS=1)
It needs Playwright and its bundled Chromium. The test is skipped when Playwright is missing.
It checks:
  * every queued question gets exactly one answer file, and no question is claimed twice;
  * the chat box is used and the "Discover sources" box never receives text;
  * tool-output answers are flagged; tool-call-only answers become FAILED in quest_tool ingest;
  * the backlog hold stops new questions until answers are marked assessed;
  * a page reload in the middle of a question is recovered (the answer is re-read, not re-sent);
  * a STOP file ends the run.
"""
import http.server, json, os, shutil, socketserver, sys, tempfile, threading, time, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
MOCK = ROOT / "tests" / "notebooklm_mock" / "notebook.html"
NBS = {"lane-a": "11111111-1111-1111-1111-111111111111",
       "lane-b": "22222222-2222-2222-2222-222222222222",
       "lane-c": "33333333-3333-3333-3333-333333333333"}

try:
    from playwright.sync_api import sync_playwright  # noqa: F401
    HAVE_PW = True
except Exception:
    HAVE_PW = False


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = MOCK.read_bytes()
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def log_message(self, *a):
        pass


@unittest.skipUnless(HAVE_PW and (__name__ == "__main__" or os.environ.get("CR_BROWSER_TESTS")), "browser test: run this file directly, or set CR_BROWSER_TESTS=1")
class DriverTest(unittest.TestCase):
    def test_end_to_end(self):
        from claimreg.notebooklm import driver as D
        # Production runs on installed Chrome (`channel: "chrome"`); use it when present so the mock
        # notebook exercises the same browser, and fall back to Playwright's bundled Chromium.
        channel = "chrome" if D.find_chrome() else ""
        srv = socketserver.TCPServer(("127.0.0.1", 0), Handler)
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        tmp = Path(tempfile.mkdtemp(prefix="nlm-driver-"))
        try:
            cfg_path = tmp / "quest-driver.json"
            cfg_path.write_text(json.dumps({
                "run_id": "TEST-RUN", "channel": channel, "answers_dir": "answers", "profile_dir": "profile",
                "max_backlog": 4, "assessed_file": "assessed.json", "poll_seconds": 0.5,
                "notebooks": {n: "http://127.0.0.1:%d/notebook/%s" % (port, i) for n, i in NBS.items()}}))
            (tmp / "assessed.json").write_text("[]")
            cfg = D.load(cfg_path)
            texts = {"Q%04d" % k: "Using mock_source.pdf.md, test question %d about item %d?%s" % (k, k * 7, extra)
                     for k, extra in [(1, ""), (2, " TOOLOUTPUT"), (3, ""), (4, " TOOLCALLONLY"), (5, ""), (6, ""), (7, ""), (8, "")]}
            for q, t in texts.items():
                (cfg["_queue"] / (q + ".json")).write_text(json.dumps({"qid": q, "attempt": "A01", "text": t}))
            logs = []
            with sync_playwright() as p:
                d = D.Driver(cfg, headless=True, log=logs.append)
                d.start(p)
                # 1) the backlog hold: with nothing assessed, at most max_backlog questions are answered
                d.loop(max_seconds=25, poll=0.5)
                saved = d.saved_qids()
                self.assertGreaterEqual(len(saved), 4)
                self.assertLessEqual(len(saved), 4 + 3, "more answers than backlog + in-flight lanes")
                self.assertTrue(any("HOLD" in l for l in logs) or len(saved) >= 4)
                # 2) release the hold, reload one lane mid-question, then finish
                (tmp / "assessed.json").write_text(json.dumps(sorted(saved)))
                busy = []
                for _ in range(20):
                    d.loop(max_seconds=0.6, poll=0.3)
                    busy = [n for n, pg in d.pages.items() if pg.evaluate("() => window.CRL.state") == "GENERATING"]
                    if busy:
                        break
                self.assertTrue(busy, "a lane should be generating after the hold is released")
                d.pages[busy[0]].reload(wait_until="domcontentloaded")
                d.loop(max_seconds=30, poll=0.5)
                self.assertTrue(any("reloading" in l for l in logs), "driver noticed the reloaded lane")
                self.assertTrue(any("recapturing" in l for l in logs), "in-flight answer re-read after reload, not re-sent")
                # discover box never used
                for pg in d.pages.values():
                    self.assertEqual(pg.evaluate("() => document.querySelector('textarea[aria-label=\"Discover sources based on the inputted query\"]').value"), "")
                (cfg["_queue"] / "STOP").write_text("stop")
                d.loop(max_seconds=20, poll=0.5)
                d.ctx.close()
            files = sorted(cfg["_answers"].glob("Q*-A*.json"))
            qids = [f.name.split("-")[0] for f in files]
            self.assertEqual(sorted(set(qids)), sorted(texts), "every question answered")
            self.assertEqual(len(qids), len(set(qids)), "no question answered twice")
            recs = {f.name.split("-")[0]: json.loads(f.read_text()) for f in files}
            for q, r in recs.items():
                self.assertTrue(r["query_seen_in_user_message"], q)
                self.assertEqual(r["query"], texts[q])
                self.assertFalse(r["answer"].startswith("Thoughts"), "Thoughts panel stripped")
            self.assertTrue(recs["Q0002"]["contains_tool_output"])
            self.assertTrue(recs["Q0004"]["contains_tool_output"])
            self.assertFalse(recs["Q0001"]["contains_tool_output"])
            self.assertGreaterEqual(len({r["lane"] for r in recs.values()}), 2, "work spread across lanes")
            self.assertTrue(any("STOP" in l for l in logs))
            # 3) quest_tool ingest: tool-call-only answer becomes FAILED
            from claimreg.notebooklm import quest_tool, quest_io
            state = tmp / "rec"
            (state / "artifacts" / "questions").mkdir(parents=True); (state / "artifacts" / "query-responses").mkdir(parents=True)
            qt = state / "quest-tool.json"
            qt.write_text(json.dumps({"project_root": ".", "run_id": "TEST-RUN", "state": "artifacts/quest-state",
                                      "header_version": "h.md", "queue_out": "q", "since": "2026-01-01T00:00:00+00:00"}))
            quest_io.Recorder(str(state), "TEST-RUN", "artifacts/quest-state").init("artifacts/questions", "artifacts/query-responses", None)
            batch = state / "b.json"
            batch.write_text(json.dumps([{"query": texts[q], "sources": ["mock_source.pdf.md"], "target": "t"} for q in sorted(texts)]))
            quest_tool.enqueue(str(qt), str(batch))
            quest_tool.ingest(str(qt), str(cfg["_answers"]))
            cap = json.loads((state / "artifacts/quest-state/recording/captures/Q0004-A01.json").read_text())
            self.assertEqual(cap["outcome"], "FAILED")
            self.assertFalse(cap["metadata"]["usable"])
            cap1 = json.loads((state / "artifacts/quest-state/recording/captures/Q0001-A01.json").read_text())
            self.assertEqual(cap1["outcome"], "COMPLETE")
            self.assertTrue(cap1["metadata"]["cited_sources"])
            # 4) a NEW quest on the reused driver profile: stale lane-runner state must be cleared.
            #    Before the fix the old IndexedDB claims for Q0001-A01... idled every lane of the new
            #    quest (this is exactly what killed the first LEVO pilot on the 11-09 profile).
            cfg2_path = tmp / "quest-driver-2.json"
            cfg2_path.write_text(json.dumps({
                "run_id": "TEST-RUN-2", "channel": channel, "answers_dir": "answers2", "profile_dir": "profile",
                "max_backlog": 8, "assessed_file": "assessed2.json", "poll_seconds": 0.5,
                "notebooks": {n: "http://127.0.0.1:%d/notebook/%s" % (port, i) for n, i in NBS.items()}}))
            (tmp / "assessed2.json").write_text("[]")
            cfg2 = D.load(cfg2_path)
            for q in ("Q0001", "Q0002", "Q0003", "Q0004"):
                (cfg2["_queue"] / (q + ".json")).write_text(
                    json.dumps({"qid": q, "attempt": "A01",
                                "text": "Using mock_source.pdf.md, second quest question %s?" % q}))
            with sync_playwright() as p2:
                d2 = D.Driver(cfg2, headless=True, log=logs.append)
                d2.start(p2)
                d2.loop(max_seconds=30, poll=0.5)
                d2.ctx.close()
            self.assertEqual(sorted(d2.saved_qids()), ["Q0001", "Q0002", "Q0003", "Q0004"],
                             "a new run_id on a reused profile starts with a clean lane-runner state")
        finally:
            srv.shutdown()
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
