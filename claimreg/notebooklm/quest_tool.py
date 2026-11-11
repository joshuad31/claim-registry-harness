"""NotebookLM quest tool: the mechanical steps between the lane runner, the two agents and the recorder.

The lane runner (lane-runner.js, one per notebook tab) reads question files from
<answers>/queue/ and writes one answer file per question to <answers>/.
This tool does the mechanical work around it, so neither agent hand-copies files:

  enqueue BATCH.json   reserve each question in the recorder and write its queue file
  ingest  ANSWERS_DIR  record every new answer file (submission + capture), once
  status CFG           counts, rate, first-hour result
  assessed FILE QID..  add QIDs to the assessed list the local driver uses for pacing
  stage   ANSWERS_DIR OUT_DIR [QID ...]
                       write driver answers as the Manager's Markdown answer files
  packet  PACKET_FILE ANSWERS_DIR [--index INDEX] [--start N] [--dry-run]
                       turn a packet's "## Ready questions" into driver queue files,
                       checking each against the header's query firewall
  sync    LEDGER ASSESSED_FILE
                       copy the Manager's per-round grading times into assessed-qids.json
                       so the driver releases the next questions and the scorecard can score

Configuration lives in quest-tool.json next to the run's state folder:

  {"project_root": ".", "run_id": "MY-RUN", "state": "artifacts/quest-state",
   "header_version": "my_header.md", "manifest_csv": "corpus/SOURCE-MANIFEST.csv",
   "queue_out": "outbox/queue", "round_size": 6, "since": "2026-10-30T10:25:47-05:00"}

The recorder is the deployment's quest_io.py (single writer, immutable records). A batch file is
a JSON list of {"query", "sources": [exact filenames], "target", "packet": optional priority id}.
"""
import csv, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

CITE = re.compile(r"\(([^()\n]{3,160}?\.(?:md|txt|pdf))\s*,\s*([^()\n]{1,160})\)")
THOUGHTS = re.compile(r"^\s*Thoughts\s*\n(?:[\s\S]*?\n)?\s*expand_(more|less)\s*\n")

READY = re.compile(r"^##\s+Ready questions\s*$", re.I | re.M)
NUMBERED = re.compile(r"^\s*(\d+)[.)]\s+(.*)$")
# a ready question is filed under exactly one axis: "[axis: A2] [target: ...] question"
AXIS_PREFIX = re.compile(r"^\[\s*axis\s*:?\s*(?P<axis>A\d+)\s*\]\s*", re.I)
TARGET_PREFIX = re.compile(r"^\[\s*target\s*:\s*(?P<target>.+?)\]\s*", re.I)
HEADING2 = re.compile(r"^##\s+", re.M)
SOURCE_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\.(?:md|pdf|txt)\b", re.I)
JARGON = re.compile(r"\b(?:H[123]|A[12]-H[123]|hypothes[ie]s|hypothesis|allocation\s+vectors?|"
                    r"stop_eligible|gauge)\b", re.I)
WORDS_OR_LESS = re.compile(r"\b900\s+words?\s+(?:or\s+less|maximum|max)\b", re.I)
WORDS_ANY = re.compile(r"\b(?:900|nine\s+hundred)\s+words?\b", re.I)


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
    """Add QIDs to the assessed list, stamping when each was first marked (the scorecard's grading time).
    Reads the older plain-list format too; the driver reads either."""
    from datetime import datetime, timezone
    p = Path(path)
    d = json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else {}
    if isinstance(d, list):
        d = {"assessed": d, "times": {}}
    have, times = set(d.get("assessed", [])), dict(d.get("times", {}))
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for q in qids:
        have.add(q)
        times.setdefault(q, now)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps({"assessed": sorted(have), "times": times}, indent=1), encoding="utf-8")
    tmp.replace(p)
    print(json.dumps({"assessed": len(have)}))


# --------------------------------------------------------------------------- #
# stage: driver answer files -> the Manager's Markdown answer files
# --------------------------------------------------------------------------- #

STAGE_FIELDS = ("qid", "attempt", "lane", "notebook_url", "outcome", "submitted_at", "captured_at",
                "generation_seconds", "contains_tool_output", "answer_names_requested_source",
                "query_seen_in_user_message", "capture_method", "note", "duplicate_note")


def _shown(value):
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "not recorded"
    return str(value)


def stage_markdown(answer, filename):
    """One driver answer as the Markdown file the Manager brief expects: query, answer, capture flags."""
    rows = ["| field | value |", "|---|---|"]
    for key in STAGE_FIELDS:
        if key in answer:
            rows.append("| %s | %s |" % (key, _shown(answer[key]).replace("|", "\\|")))
    return "\n".join(["# " + Path(filename).stem, ""] + rows + [
        "", "## Query", "", str(answer.get("query", "")), "",
        "## Answer", "", str(answer.get("answer", "")), ""])


def stage(answers_dir, out_dir, qids=None):
    """Write each driver answer file as a Manager-workspace Markdown file (idempotent)."""
    answers_dir, out_dir = Path(answers_dir), Path(out_dir)
    wanted = {q.strip().upper() for q in (qids or []) if q.strip()}
    out_dir.mkdir(parents=True, exist_ok=True)
    staged = []
    for f in sorted(answers_dir.glob("Q*-A*.json")):
        try:
            answer = json.loads(f.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        qid = str(answer.get("qid") or f.name.split("-")[0])
        if wanted and qid.upper() not in wanted:
            continue
        target = out_dir / (f.stem + ".md")
        target.write_text(stage_markdown(answer, f.name), encoding="utf-8")
        staged.append({"qid": qid, "attempt": answer.get("attempt", "A01"), "file": str(target)})
    print(json.dumps({"staged": staged, "count": len(staged), "out": str(out_dir)}, indent=1))
    return staged


# --------------------------------------------------------------------------- #
# packet: a Manager packet's "## Ready questions" -> driver queue files
# --------------------------------------------------------------------------- #

def _next_qid(answers_dir, start=None):
    if start:
        return int(start)
    nums = []
    for p in list(answers_dir.glob("Q*-A*.json")) + list((answers_dir / "queue").glob("Q*.json")):
        m = re.match(r"Q(\d+)", p.name)
        if m:
            nums.append(int(m.group(1)))
    return max(nums) + 1 if nums else 1


def _known_filenames(index_path):
    if not index_path:
        return None
    text = Path(index_path).read_text(encoding="utf-8", errors="replace").lower()
    return {m.group(0) for m in SOURCE_TOKEN.finditer(text)}


def _ready_items(text):
    """The numbered items under '## Ready questions', joined across wrapped lines."""
    m = READY.search(text)
    if not m:
        return None
    body = text[m.end():]
    stop = HEADING2.search(body)
    if stop:
        body = body[:stop.start()]
    items, current = [], None
    for line in body.splitlines():
        num = NUMBERED.match(line)
        if num:
            if current:
                items.append(current)
            current = [num.group(2).strip()]
        elif current is not None:
            if not line.strip():
                items.append(current)
                current = None
            else:
                current.append(line.strip())
    if current:
        items.append(current)
    return [" ".join(parts).strip() for parts in items if " ".join(parts).strip()]


def firewall_warnings(question, known=None, asked=None):
    """Mechanical checks for the header's query firewall. Warnings only, never a rewrite."""
    warnings = []
    names = sorted({m.group(0) for m in SOURCE_TOKEN.finditer(question)})
    if not names:
        warnings.append("no source filename in the question")
    if known is not None:
        unknown = [n for n in names if n.lower() not in known]
        if unknown:
            warnings.append("filename(s) not in the index: " + ", ".join(unknown))
    if JARGON.search(question):
        warnings.append("contains a hypothesis label or project jargon")
    if WORDS_OR_LESS.search(question):
        warnings.append("asks for a length ceiling; questions never ask for fewer than 900 words")
    if len(names) > 1 and WORDS_ANY.search(question):
        warnings.append("a multi-source question must not state a length")
    if asked and question.strip().lower() in asked:
        warnings.append("identical question is already in the queue")
    return warnings


def packet(packet_path, answers_dir, index=None, start=None, dry_run=False):
    """Turn a packet's ready questions into Qnnnn.json queue files; print the mapping and warnings."""
    packet_path, answers_dir = Path(packet_path), Path(answers_dir)
    text = packet_path.read_text(encoding="utf-8", errors="replace")
    items = _ready_items(text)
    if items is None:
        raise SystemExit("packet: no '## Ready questions' section in %s" % packet_path)
    known = _known_filenames(index)
    asked = set()
    queue = answers_dir / "queue"
    for f in (queue.glob("Q*.json") if queue.exists() else []):
        try:
            j = json.loads(f.read_text(encoding="utf-8-sig"))
            if j.get("text"):
                asked.add(str(j["text"]).strip().lower())
        except (OSError, ValueError):
            continue
    queue.mkdir(parents=True, exist_ok=True)
    nxt = _next_qid(answers_dir, start)
    queued = []
    for i, item in enumerate(items):
        target = axis = None
        match = AXIS_PREFIX.match(item)
        if match:
            axis = match.group("axis").upper()
            item = item[match.end():].strip()
        match = TARGET_PREFIX.match(item)
        if match:
            target = match.group("target").strip()
            item = item[match.end():].strip()
        qid = "Q%04d" % (nxt + i)
        entry = {"qid": qid, "axis": axis, "target": target, "text": item,
                 "warnings": firewall_warnings(item, known, asked)}
        queued.append(entry)
        if not dry_run:
            # the queue file is what reaches the notebook page: the question and nothing else
            (queue / (qid + ".json")).write_text(
                json.dumps({"qid": qid, "attempt": "A01", "text": item}, ensure_ascii=False, indent=1),
                encoding="utf-8")
    print(json.dumps({"packet": str(packet_path), "start": nxt, "dry_run": bool(dry_run),
                      "queued": queued}, indent=1))
    return queued


# --------------------------------------------------------------------------- #
# sync: the Manager's grading times -> assessed-qids.json (driver pacing + scorecard)
# --------------------------------------------------------------------------- #

def _utc_iso(value):
    if not value:
        return None
    try:
        t = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t.astimezone(timezone.utc).isoformat(timespec="seconds")


def sync(ledger_path, assessed_file):
    """Merge every assessment member's committed_at into assessed-qids.json (idempotent)."""
    ledger = json.loads(Path(ledger_path).read_text(encoding="utf-8-sig"))
    p = Path(assessed_file)
    data = json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else {}
    if isinstance(data, list):
        data = {"assessed": data, "times": {}}
    have, times = set(data.get("assessed", [])), dict(data.get("times", {}))
    stamped = []
    for assessment in ledger.get("assessments", []):
        when = _utc_iso(assessment.get("committed_at"))
        for member in assessment.get("members", []):
            qid = member.get("qid")
            if not qid:
                continue
            have.add(qid)
            if when and qid not in times:
                times[qid] = when
                stamped.append(qid)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps({"assessed": sorted(have), "times": times}, indent=1), encoding="utf-8")
    tmp.replace(p)
    print(json.dumps({"assessed": len(have), "times": len(times), "stamped": stamped, "file": str(p)}, indent=1))
    return {"assessed": sorted(have), "times": times}


# --------------------------------------------------------------------------- #
# command line
# --------------------------------------------------------------------------- #

def _parse_flags(argv):
    flags, rest, i = {}, [], 0
    while i < len(argv):
        a = argv[i]
        if a in ("--index", "--start"):
            if i + 1 >= len(argv):
                raise SystemExit("quest_tool: %s needs a value" % a)
            flags[a[2:]] = argv[i + 1]
            i += 2
        elif a == "--dry-run":
            flags["dry_run"] = True
            i += 1
        else:
            rest.append(a)
            i += 1
    return flags, rest


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "assessed":
        if len(args) < 2:
            raise SystemExit("quest_tool: assessed FILE QID [QID ...]")
        mark_assessed(args[0], args[1:])
        return 0
    if cmd in ("enqueue", "ingest", "status"):
        if len(args) < 2:
            print(__doc__)
            return 2
        if cmd == "status":
            status(args[0])
        else:
            {"enqueue": lambda: enqueue(args[0], args[1]),
             "ingest": lambda: ingest(args[0], args[1])}[cmd]()
        return 0
    if cmd == "stage":
        if len(args) < 2:
            raise SystemExit("quest_tool: stage ANSWERS_DIR OUT_DIR [QID ...]")
        stage(args[0], args[1], args[2:])
        return 0
    if cmd == "packet":
        flags, rest = _parse_flags(args)
        if len(rest) < 2:
            raise SystemExit("quest_tool: packet PACKET_FILE ANSWERS_DIR [--index INDEX] [--start N] [--dry-run]")
        packet(rest[0], rest[1], index=flags.get("index"), start=flags.get("start"),
               dry_run=flags.get("dry_run", False))
        return 0
    if cmd == "sync":
        if len(args) < 2:
            raise SystemExit("quest_tool: sync LEDGER ASSESSED_FILE")
        sync(args[0], args[1])
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
