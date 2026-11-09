"""NotebookLM quest tool: the Investigator's helper between the lane runner and a recorder.

The lane runner (lane-runner.js, one per notebook tab) reads question files from
<answers>/queue/ and writes one answer file per question to <answers>/.
This tool does the two mechanical steps around it, so the Investigator only writes questions:

  enqueue BATCH.json   reserve each question in the recorder and write its queue file
  ingest  ANSWERS_DIR  record every new answer file (submission + capture), once
  status               counts, rate, first-hour result
  assessed FILE QID..  add QIDs to the assessed list the local driver uses for pacing

Configuration lives in quest-tool.json next to the run's state folder:

  {"project_root": ".", "run_id": "MY-RUN", "state": "artifacts/quest-state",
   "header_version": "my_header.md", "manifest_csv": "corpus/SOURCE-MANIFEST.csv",
   "queue_out": "outbox/queue", "round_size": 6, "since": "2026-10-30T10:25:47-05:00"}

The recorder is the deployment's quest_io.py (single writer, immutable records). A batch file is
a JSON list of {"query", "sources": [exact filenames], "target", "packet": optional priority id}.
"""
import csv, json, re, sys
from pathlib import Path

CITE = re.compile(r"\(([^()\n]{3,160}?\.(?:md|txt|pdf))\s*,\s*([^()\n]{1,160})\)")
THOUGHTS = re.compile(r"^\s*Thoughts\s*\n(?:[\s\S]*?\n)?\s*expand_(more|less)\s*\n")


def load(cfg_path):
    cfg = json.loads(Path(cfg_path).read_text(encoding="utf-8"))
    root = Path(cfg_path).resolve().parent / cfg.get("project_root", ".")
    sys.path.insert(0, str(Path(__file__).resolve().parent))   # bundled copy
    sys.path.insert(0, str(root / "runtime"))                   # a deployment's own recorder wins
    import quest_io  # single-writer recorder (from the PTX deployment)
    rec = quest_io.Recorder(str(root), cfg["run_id"], cfg["state"])
    ledger = root / cfg["state"] / "quest-tool-ledger.json"
    return cfg, root, rec, ledger


def manifest(root, cfg):
    p = root / cfg.get("manifest_csv", "corpus/SOURCE-MANIFEST.csv")
    if not p.exists():
        return {}
    with open(p, encoding="utf-8-sig") as f:
        return {r["filename"]: r["id"] for r in csv.DictReader(f)}


def read_ledger(path):
    return json.loads(path.read_text()) if path.exists() else {"reserved": [], "ingested": []}


def enqueue(cfg_path, batch):
    cfg, root, rec, lpath = load(cfg_path)
    man, led = manifest(root, cfg), read_ledger(lpath)
    out = (root / cfg.get("queue_out", "outbox/queue")); out.mkdir(parents=True, exist_ok=True)
    size = int(cfg.get("round_size", 6)); made = []
    for it in json.loads(Path(batch).read_text(encoding="utf-8")):
        n = len(led["reserved"])
        voices = it["sources"]
        r = rec.reserve({"qid": "NEXT", "query": it["query"], "source_voices": voices, "metadata": {
            "header_version": cfg["header_version"], "round_number": n // size + 1, "order_in_round": n % size + 1,
            "notebook_lane": "assigned by lane runner on claim (actual lane in submission event)",
            "target_ledger_row_or_test": it["target"], "packet_priority_id": it.get("packet"),
            "resolved_source_ids": {v: man.get(v, "UNRESOLVED_NAME") for v in voices},
            "descended_frd_ids": [], "witness_ids": []}})
        (out / (r["qid"] + ".json")).write_text(json.dumps({"qid": r["qid"], "attempt": "A01", "text": it["query"]}, ensure_ascii=False), encoding="utf-8")
        led["reserved"].append(r["qid"]); made.append(r["qid"])
    lpath.write_text(json.dumps(led, indent=1))
    print(json.dumps({"reserved": made, "queue_dir": str(out)}))


def cited(answer, man):
    found = {}
    for fn, anchor in CITE.findall(answer):
        fn = fn.strip().strip("\"'`")
        found.setdefault(fn, [])
        if anchor.strip() and anchor.strip() not in found[fn]:
            found[fn].append(anchor.strip()[:160])
    return [{"source_voice": f, "manifest_id": man.get(f, "UNRESOLVED_NAME"), "passage_anchors": a or ["ANCHOR_NOT_PROVIDED"]} for f, a in found.items()]


def ingest(cfg_path, folder):
    cfg, root, rec, lpath = load(cfg_path)
    man, led = manifest(root, cfg), read_ledger(lpath)
    done = []
    for f in sorted(Path(folder).glob("Q*-A*.json")):
        if f.stem in led["ingested"]:
            continue
        a = json.loads(f.read_text(encoding="utf-8-sig"))
        qid, att = a["qid"], a.get("attempt", "A01")
        if not a.get("query_seen_in_user_message"):
            rec.failed({"qid": qid, "attempt": att, "status": "AMBIGUOUS", "reason": "Lane runner could not match the user message to the reserved query."})
        else:
            rec.submitted({"qid": qid, "attempt": att, "notebook_url": a["notebook_url"], "submitted_at": a["submitted_at"],
                           "evidence": "Lane runner (%s) found the exact reserved query as the matching user message, then waited for the finished answer card." % a["lane"]})
            answer = THOUGHTS.sub("", a["answer"]) or "<!-- NotebookLM returned no visible response body. -->"
            outcome = a["outcome"]
            tool_output = bool(re.search(r"Tool response for|exit_code:|Tool call:default_api", answer))
            if re.match(r"\s*Tool call:", answer) and len(answer) < 3000:
                outcome = "FAILED"   # the card holds only NotebookLM's own tool-call text, no answer prose
            on_target = a.get("answer_names_requested_source", True)
            meta = {"usable": outcome in ("COMPLETE", "INCOMPLETE") and len(answer) >= 400 and on_target, "lane": a["lane"],
                    "answer_names_requested_source": on_target,
                    "contains_tool_output": tool_output,
                    "generation_seconds": a.get("generation_seconds"), "capture_method": a.get("capture_method"),
                    "cited_sources": cited(answer, man)}
            for k in ("note", "duplicate_note"):
                if a.get(k):
                    meta[k] = a[k]
            rec.capture({"qid": qid, "attempt": att, "query": rec.reservation(qid)["query"], "answer": answer,
                         "outcome": outcome, "captured_at": a["captured_at"], "metadata": meta})
        led["ingested"].append(f.stem); done.append(f.stem)
    lpath.write_text(json.dumps(led, indent=1))
    print(json.dumps({"ingested": done, "total": len(led["ingested"])}))


def status(cfg_path):
    cfg, root, rec, lpath = load(cfg_path)
    s = rec.status(None, None, cfg.get("since"))
    keep = ("recorded_pair_count", "usable_qid_count", "reserved_count", "recorded_per_hour_since_first_submission", "first_hour")
    print(json.dumps({k: s.get(k) for k in keep}, indent=1, default=str)[:4000])


def mark_assessed(path, qids):
    p = Path(path)
    have = set(json.loads(p.read_text(encoding="utf-8"))) if p.exists() else set()
    have |= set(qids)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(sorted(have)), encoding="utf-8")
    print(json.dumps({"assessed": len(have)}))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "assessed":
        sys.exit(mark_assessed(sys.argv[2], sys.argv[3:]))
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, cfgp = sys.argv[1], sys.argv[2]
    {"enqueue": lambda: enqueue(cfgp, sys.argv[3]), "ingest": lambda: ingest(cfgp, sys.argv[3]), "status": lambda: status(cfgp)}[cmd]()
