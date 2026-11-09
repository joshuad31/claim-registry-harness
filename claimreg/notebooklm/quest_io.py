"""Dependency-free, single-writer Discovery recording. No browser or scoring engine."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile


class RecordingError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RecordingError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamps require a timezone.")
    return parsed


def identifier(value, pattern, label):
    require(isinstance(value, str) and re.fullmatch(pattern, value), "Invalid " + label)
    return value


def within(root, relative):
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts,
            "Output paths must be relative, with no '..'.")
    result = (root / path).resolve()
    require(result.is_relative_to(root) and result != root, "Path escapes the project.")
    return result


def exact_write(path, content):
    """Publish complete bytes atomically without replacing an existing destination."""
    data = content.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        require(path.read_bytes() == data, "Collision; existing file preserved: " + str(path))
        return
    fd, temporary = tempfile.mkstemp(prefix=".quest-record-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            require(path.read_bytes() == data, "Collision; existing file preserved: " + str(path))
    finally:
        os.unlink(temporary)


def serialized(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def capture_input(recorder, data, answer_file=None, use_reserved_query=False):
    """Avoid retranscribing saved answer/query text; the capture schema is unchanged."""
    result = dict(data)
    if answer_file is not None:
        require("answer" not in result, "Use either answer or --answer-file, not both.")
        result["answer"] = Path(answer_file).read_bytes().decode("utf-8-sig")
    if use_reserved_query:
        require("query" not in result, "Omit query when using --use-reserved-query.")
        qid, _ = recorder.key(result)
        result["query"] = recorder.reservation(qid)["query"]
    return result


def first_hour_report(attempts, events, since, current):
    """A fixed restart window, not a projected or warm-pipeline rate."""
    start = timestamp(since)
    require(start <= current, "Restart timestamp is in the future.")
    end = start + timedelta(hours=1)
    eligible = {e["qid"] for e in events if timestamp(e["submitted_at"]) >= start}
    eligible -= {e["qid"] for e in events if timestamp(e["submitted_at"]) < start}
    recorded, usable = set(), set()
    for attempt in attempts:
        if (attempt["qid"] in eligible and
                start <= timestamp(attempt["submitted_at"]) <= timestamp(attempt["captured_at"]) <= min(end, current)):
            recorded.add(attempt["qid"])
            if attempt["usable"]:
                usable.add(attempt["qid"])
    return {"restart_requested_at": since, "deadline": end.isoformat(),
            "recorded_qids": sorted(recorded), "recorded_count": len(recorded),
            "usable_candidate_count": len(usable),
            "usable_candidate_fraction": len(usable) / len(recorded) if recorded else None,
            "required_count": 41,
            "count_result": "PENDING" if current < end else "PASS" if len(recorded) >= 41 else "FAIL",
            "note": "Counts distinct query/answer pairs newly submitted and captured in the fixed first hour; "
                    "excludes pre-restart QIDs and retries as extra credit. "
                    "Usability is an acquisition judgment, not downstream FRD validation."}


def required_text(data, key):
    value = data.get(key)
    require(isinstance(value, str) and bool(value.strip()), key + " must be nonempty text.")
    return value


def metadata(data):
    value = data.get("metadata", {})
    require(isinstance(value, dict), "metadata must be a JSON object.")
    return value


def question_metadata(data, voices):
    value = metadata(data)
    for key in ("header_version", "notebook_lane", "target_ledger_row_or_test"):
        required_text(value, key)
    for key in ("round_number", "order_in_round"):
        require(type(value.get(key)) is int and value[key] >= 1, key + " must be a positive integer.")
    require("packet_priority_id" in value and (value["packet_priority_id"] is None or
            isinstance(value["packet_priority_id"], str) and bool(value["packet_priority_id"].strip())),
            "packet_priority_id must be text or null for a self-originated question.")
    resolved = value.get("resolved_source_ids")
    require(isinstance(resolved, dict) and set(resolved) == set(voices),
            "resolved_source_ids must map every source voice as sent to its manifest ID or UNRESOLVED_NAME.")
    for source_id in resolved.values():
        require(isinstance(source_id, str) and bool(source_id.strip()), "Source IDs must be nonempty text.")
    for key in ("descended_frd_ids", "witness_ids"):
        require(value.get(key) == [], key + " must be an empty reserved list during discovery.")
    return value


def capture_metadata(data):
    value = metadata(data)
    require(type(value.get("usable")) is bool, "Capture metadata requires explicit usable true/false.")
    require(not value["usable"] or data.get("outcome") in ("COMPLETE", "INCOMPLETE"),
            "A FAILED transport attempt cannot be marked usable; partial scientific answers may be usable.")
    cited = value.get("cited_sources")
    require(isinstance(cited, list), "cited_sources must be a structured list (empty if none cited).")
    for source in cited:
        require(isinstance(source, dict), "Each cited source must be an object.")
        for key in ("source_voice", "manifest_id"):
            required_text(source, key)
        anchors = source.get("passage_anchors")
        require(isinstance(anchors, list) and bool(anchors) and
                all(isinstance(anchor, str) and bool(anchor.strip()) for anchor in anchors),
                "Each cited source needs passage_anchors; use ANCHOR_NOT_PROVIDED explicitly if absent.")
    return value


def fenced(text):
    longest = max((len(match[0]) for match in re.finditer(r"\x60+", text)), default=0)
    fence = "\x60" * max(3, longest + 1)
    return fence + "text\n" + text + "\n" + fence


def question_md(record):
    return ("# " + record["run_id"] + "-" + record["qid"] + "\n\n"
            "Reservation status: RESERVED (immutable; later submission/failure events are separate).\n\n"
            "Reserved UTC: " + record["reserved_at"] + "\n\n"
            "Source voices: " + json.dumps(record["source_voices"], ensure_ascii=False) +
            "\n\n## Recording metadata\n\n" + fenced(serialized(record["metadata"])) +
            "\n\n## Exact query\n\n" + fenced(record["query"]) + "\n")


def capture_md(record):
    return ("# " + record["run_id"] + "-" + record["qid"] + "-" + record["attempt"] +
            "\n\nOutcome: " + record["outcome"] + "\n\nNotebook: " + record["notebook_url"] +
            "\n\nSubmitted: " + record["submitted_at"] +
            "\n\nSubmission evidence: " + record["submission_evidence"] +
            "\n\nCaptured: " + record["captured_at"] +
            "\n\nSource voices: " + json.dumps(record["source_voices"], ensure_ascii=False) +
            "\n\n## Recording metadata\n\n" +
            fenced(serialized({"question": record["question_metadata"], "capture": record["metadata"]})) +
            "\n\n## Exact query\n\n" + fenced(record["query"]) +
            "\n\n## Exact answer\n\n" + fenced(record["answer"]) + "\n")


class Recorder:
    def __init__(self, project_root, run_id, state):
        self.root = Path(project_root).resolve()
        require(self.root.is_dir(), "Project root must already exist.")
        self.run = identifier(run_id, r"[A-Za-z0-9][A-Za-z0-9_-]{0,99}", "run-id")
        self.state = within(self.root, state)
        self.base = within(self.root, str(self.state.relative_to(self.root) / "recording"))
        self.config_path = self.base / "run.json"

    def init(self, questions, responses, requested_at=None):
        for folder in (questions, responses):
            within(self.root, folder)
        if requested_at is not None:
            timestamp(requested_at)
        config = {"run_id": self.run, "questions": questions, "responses": responses,
                  "started_at": now(), "requested_at": requested_at, "format": 1}
        if self.config_path.exists():
            old = read_json(self.config_path)
            require(all(old[k] == config[k] for k in ("run_id", "questions", "responses", "format")),
                    "Different configuration already exists; preserved.")
            require(requested_at is None or old["requested_at"] == requested_at,
                    "Initial request timestamp is already frozen; preserved.")
            config = old
        exact_write(self.config_path, serialized(config))
        for folder in (questions, responses):
            within(self.root, folder).mkdir(parents=True, exist_ok=True)
        return {"initialized": True, "run_id": self.run, "state": str(self.state)}

    def config(self):
        require(self.config_path.is_file(), "Run init first.")
        config = read_json(self.config_path)
        require(config["run_id"] == self.run, "Run-id does not match state configuration.")
        return config

    def folder(self, key):
        return within(self.root, self.config()[key])

    def key(self, data):
        qid = identifier(data.get("qid"), r"Q[0-9]{4,}", "qid")
        attempt = identifier(data.get("attempt"), r"A[0-9]{2,}", "attempt")
        return qid, attempt

    def reservation(self, qid):
        return read_json(self.base / "questions" / (qid + ".json"))

    def named_files(self, key):
        return list(self.folder(key).rglob(self.run + "-Q*.md"))

    def next_qid(self):
        numbers = []
        for path in self.named_files("questions") + self.named_files("responses"):
            match = re.match(re.escape(self.run) + r"-Q([0-9]+)(?:-A[0-9]+)?\.md$", path.name)
            if match:
                numbers.append(int(match[1]))
        for path in (self.base / "questions").glob("Q*.json"):
            if re.fullmatch(r"Q[0-9]+", path.stem):
                numbers.append(int(path.stem[1:]))
        return "Q" + str(max(numbers, default=0) + 1).zfill(4)

    def commit(self, path, record, volatile_key=None):
        if path.exists():
            previous = read_json(path)
            compare = dict(record)
            if volatile_key:
                compare[volatile_key] = previous[volatile_key]
            require(previous == compare, "Conflicting record; original preserved: " + str(path))
            record = previous
        exact_write(path, serialized(record))
        return record

    def reserve(self, data):
        qid = self.next_qid() if data.get("qid", "NEXT") == "NEXT" else data["qid"]
        identifier(qid, r"Q[0-9]{4,}", "qid")
        query = required_text(data, "query")
        voices = data.get("source_voices")
        require(isinstance(voices, list) and 1 <= len(voices) <= 3,
                "Specify one to three source voices.")
        require(all(isinstance(v, str) and v.strip() for v in voices),
                "Source voices must be nonempty text.")
        require(len(set(voices)) == len(voices), "Source voices must be distinct.")
        record_path = self.base / "questions" / (qid + ".json")
        name = self.run + "-" + qid + ".md"
        mirror_path = self.folder("questions") / name
        collisions = [p for p in self.named_files("questions") if p.name == name]
        responses = [p for p in self.named_files("responses")
                     if p.name.startswith(self.run + "-" + qid + "-")]
        require(not collisions and not responses or record_path.exists(),
                "QID already exists outside this recorder; use NEXT.")
        require(all(p == mirror_path for p in collisions), "QID exists in another folder.")
        record = {"run_id": self.run, "qid": qid, "query": query,
                  "source_voices": voices, "metadata": question_metadata(data, voices), "reserved_at": now()}
        record = self.commit(record_path, record, "reserved_at")
        exact_write(mirror_path, question_md(record))
        return {"qid": qid, "question_file": str(mirror_path), "query": query}

    def submitted(self, data):
        qid, attempt = self.key(data)
        self.reservation(qid)
        submitted_at = data.get("submitted_at", now())
        timestamp(submitted_at)
        record = {"run_id": self.run, "qid": qid, "attempt": attempt,
                  "notebook_url": required_text(data, "notebook_url"),
                  "evidence": required_text(data, "evidence"), "submitted_at": submitted_at}
        path = self.base / "events" / (qid + "-" + attempt + "-submitted.json")
        resolve = data.get("resolves_ambiguity", False)
        require(isinstance(resolve, bool), "resolves_ambiguity must be true or false.")
        if resolve:
            failure_path = self.base / "events" / (qid + "-" + attempt + "-failed.json")
            require(failure_path.is_file(), "No ambiguous event exists to resolve.")
            failure = read_json(failure_path)
            require(failure["status"] == "AMBIGUOUS", "Only AMBIGUOUS events can be confirmed.")
            if path.exists():
                require(read_json(path)["notebook_url"] == record["notebook_url"],
                        "Confirmation must refer to the original notebook.")
            else:
                self.commit(path, record)
            confirmation = {"qid": qid, "attempt": attempt, "evidence": record["evidence"],
                            "ambiguous_event_recorded_at": failure["recorded_at"], "confirmed_at": now()}
            self.commit(self.base / "events" / (qid + "-" + attempt + "-confirmed.json"),
                        confirmation, "confirmed_at")
        else:
            self.commit(path, record, None if "submitted_at" in data else "submitted_at")
        return {"qid": qid, "attempt": attempt, "submission_recorded": True}

    def failed(self, data):
        qid, attempt = self.key(data)
        self.reservation(qid)
        status = data.get("status", "FAILED")
        require(status in ("FAILED", "AMBIGUOUS"), "Failure status must be FAILED or AMBIGUOUS.")
        record = {"run_id": self.run, "qid": qid, "attempt": attempt,
                  "status": status, "reason": required_text(data, "reason"), "recorded_at": now()}
        self.commit(self.base / "events" / (qid + "-" + attempt + "-failed.json"),
                    record, "recorded_at")
        return {"qid": qid, "attempt": attempt, "status": status}

    def capture(self, data):
        qid, attempt = self.key(data)
        question = self.reservation(qid)
        submitted_path = self.base / "events" / (qid + "-" + attempt + "-submitted.json")
        require(submitted_path.is_file(), "Record an observed submission before capturing.")
        submission = read_json(submitted_path)
        outcome = data.get("outcome")
        require(outcome in ("COMPLETE", "INCOMPLETE", "FAILED"),
                "Explicit outcome required: COMPLETE, INCOMPLETE or FAILED.")
        captured_at = data.get("captured_at", now())
        require(timestamp(captured_at) >= timestamp(submission["submitted_at"]),
                "Capture timestamp precedes submission.")
        record = {"run_id": self.run, "qid": qid, "attempt": attempt,
                  "query": question["query"], "source_voices": question["source_voices"],
                  "question_metadata": question["metadata"], "metadata": capture_metadata(data),
                  "answer": required_text(data, "answer"), "outcome": outcome,
                  "notebook_url": submission["notebook_url"],
                  "submitted_at": submission["submitted_at"],
                  "submission_evidence": submission["evidence"], "captured_at": captured_at}
        record_path = self.base / "captures" / (qid + "-" + attempt + ".json")
        mirror_path = self.folder("responses") / (self.run + "-" + qid + "-" + attempt + ".md")
        require(not mirror_path.exists() or record_path.exists(),
                "Existing response was not created by recorder; preserved.")
        record = self.commit(record_path, record, None if "captured_at" in data else "captured_at")
        exact_write(mirror_path, capture_md(record))
        return {"qid": qid, "attempt": attempt, "response_file": str(mirror_path)}

    def status(self, deadline=None, target=None, since=None):
        config = self.config()
        reservations = {p.stem: read_json(p) for p in (self.base / "questions").glob("Q*.json")}
        events = [read_json(p) for p in (self.base / "events").glob("*-submitted.json")]
        failed = {(r["qid"], r["attempt"]): r for r in
                  (read_json(p) for p in (self.base / "events").glob("*-failed.json"))}
        resolved = set()
        for path in (self.base / "events").glob("*-confirmed.json"):
            record = read_json(path)
            pair = record["qid"], record["attempt"]
            if (pair in failed and failed[pair]["status"] == "AMBIGUOUS"
                    and record["ambiguous_event_recorded_at"] == failed[pair]["recorded_at"]
                    and record["evidence"].strip()):
                resolved.add(pair)
        excluded = set(failed) - resolved
        submitted = {(r["qid"], r["attempt"]): r for r in events}
        issues, captures, usable_qids, usable_attempts = [], {}, set(), []
        recorded_attempts = []
        for path in (self.base / "captures").glob("Q*-A*.json"):
            record = read_json(path)
            pair = record["qid"], record["attempt"]
            captures[pair] = record
            mirror = self.folder("responses") / (self.run + "-" + path.stem + ".md")
            if (pair in submitted and pair not in excluded and pair[0] in reservations
                    and record["outcome"] in ("COMPLETE", "INCOMPLETE")):
                recorded_attempts.append({"qid": pair[0], "submitted_at": record["submitted_at"],
                                          "captured_at": record["captured_at"],
                                          "usable": record["metadata"].get("usable") is True})
                if record["metadata"].get("usable") is True:
                    usable_qids.add(pair[0])
                    usable_attempts.append({"qid": pair[0], "attempt": pair[1],
                                            "outcome": record["outcome"],
                                            "response_file": str(mirror.relative_to(self.root)).replace("\\", "/"),
                                            "captured_at": record["captured_at"]})
        for pair, event in failed.items():
            if event["status"] == "AMBIGUOUS" and pair not in resolved:
                issues.append("-".join(pair) + ": ambiguous submission; inspect before retry")
        pending = ["-".join(pair) for pair in submitted if pair not in captures and pair not in excluded]
        reserved_only = sorted(set(reservations) - {p[0] for p in submitted} - {p[0] for p in failed})
        issues.extend(key + ": submitted without capture" for key in pending)
        tracked_questions = {self.run + "-" + qid + ".md" for qid in reservations}
        tracked_responses = {self.run + "-" + qid + "-" + attempt + ".md" for qid, attempt in captures}
        legacy_q = [str(p) for p in self.named_files("questions") if p.name not in tracked_questions]
        legacy_a = [str(p) for p in self.named_files("responses") if p.name not in tracked_responses]
        current = datetime.now(timezone.utc)
        started = timestamp(config["started_at"])
        first = min((timestamp(e["submitted_at"]) for e in events), default=None)
        elapsed = max((current - first).total_seconds(), 0) if first else 0
        requested = timestamp(config["requested_at"]) if config["requested_at"] else None
        full_elapsed = max((current - requested).total_seconds(), 0) if requested else None
        recorded_qids = {item["qid"] for item in recorded_attempts}
        result = {"run_id": self.run, "recorded_qids": sorted(recorded_qids),
                  "recorded_pair_count": len(recorded_qids),
                  "usable_qids": sorted(usable_qids), "usable_qid_count": len(usable_qids),
                  "reserved_count": len(reservations),
                  "submitted_attempts": len(submitted), "captured_attempts": len(captures),
                  "failed_or_ambiguous_attempts": len(failed), "reserved_without_attempt": reserved_only,
                  "resolved_ambiguous_attempts": len(resolved),
                  "pending_captures": pending, "reconciliation": issues, "next_qid": self.next_qid(),
                  "usable_attempts": usable_attempts,
                  "seconds_init_to_first_submission": max((first - started).total_seconds(), 0) if first else None,
                  "seconds_request_to_first_submission": (first - requested).total_seconds() if first and requested else None,
                  "recorded_per_hour_since_request": round(len(recorded_qids) * 3600 / full_elapsed, 2) if full_elapsed else None,
                  "recorded_per_hour_since_first_submission": round(len(recorded_qids) * 3600 / elapsed, 2) if elapsed else 0,
                  "legacy_question_files_unverified": legacy_q,
                  "legacy_response_files_unverified": legacy_a,
                  "legacy_note": "Legacy files are preserved and excluded from live recorder counts."}
        if since:
            result["first_hour"] = first_hour_report(recorded_attempts, events, since, current)
        if deadline:
            remaining = (timestamp(deadline) - current).total_seconds()
            result.update({"deadline": deadline, "seconds_remaining": round(remaining, 1)})
            if target is not None:
                needed = max(target - len(recorded_qids), 0)
                result.update({"target": target, "additional_recorded_pairs_needed": needed,
                               "required_pairs_per_hour": round(needed * 3600 / remaining, 2) if remaining > 0 else None,
                               "target_met": needed == 0})
        return result

    def record(self, qid):
        """Read a complete question record without mutating its reserved wording."""
        identifier(qid, r"Q[0-9]{4,}", "qid")
        question = self.reservation(qid)
        events = [read_json(path) for path in sorted((self.base / "events").glob(qid + "-*.json"))]
        captures = [read_json(path) for path in sorted((self.base / "captures").glob(qid + "-*.json"))]
        attempt_status = {}
        for event in events:
            attempt_status.setdefault(event["attempt"], {})
            if "status" in event:
                attempt_status[event["attempt"]]["failure"] = event["status"]
            if "submitted_at" in event:
                attempt_status[event["attempt"]]["submitted"] = True
            if "confirmed_at" in event:
                attempt_status[event["attempt"]]["confirmed"] = True
        for capture in captures:
            attempt_status.setdefault(capture["attempt"], {})["outcome"] = capture["outcome"]
        for attempt, details in attempt_status.items():
            unresolved_failure = details.get("failure") and not details.get("confirmed")
            details["status"] = (details["failure"] if unresolved_failure else
                                 details.get("outcome", "SUBMITTED" if details.get("submitted") else "RESERVED"))
        return {**question, "submission_events": events,
                "submission_status": "RESERVED" if not attempt_status else "SEE_ATTEMPTS",
                "attempts": attempt_status,
                "attempt_list": sorted({event["attempt"] for event in events}),
                "query_response_records": [
                    {"attempt": capture["attempt"], "outcome": capture["outcome"],
                     "response_file": str((self.folder("responses") /
                        (self.run + "-" + qid + "-" + capture["attempt"] + ".md")).relative_to(self.root)),
                     "cited_sources": capture["metadata"]["cited_sources"],
                     "usable": capture["metadata"]["usable"]} for capture in captures]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--state", required=True, help="Quest-state directory relative to project root.")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--questions", default="artifacts/questions")
    init.add_argument("--responses", default="artifacts/query-responses")
    init.add_argument("--requested-at", help="Actual initial request timestamp with timezone; preserved after init.")
    for name in ("reserve", "submitted", "failed", "capture"):
        command = sub.add_parser(name)
        command.add_argument("--input", required=True, help="JSON file path, or - for standard input.")
        if name == "capture":
            command.add_argument("--answer-file", help="Read an existing UTF-8 answer file without retyping it in JSON.")
            command.add_argument("--use-reserved-query", action="store_true",
                                 help="Use reserved wording after the operator has checked the actual answer pairing.")
    status = sub.add_parser("status")
    status.add_argument("--deadline", help="ISO 8601 time with timezone; performance deadline only.")
    status.add_argument("--target", type=int)
    status.add_argument("--since", help="Actual restart request time: report its fixed first-hour count without resetting state.")
    record = sub.add_parser("record", help="Read full question, attempt, and citation record.")
    record.add_argument("--qid", required=True)
    args = parser.parse_args()
    try:
        recorder = Recorder(args.project_root, args.run_id, args.state)
        if args.command == "init":
            result = recorder.init(args.questions, args.responses, args.requested_at)
        elif args.command == "status":
            require(args.target is None or args.target >= 0, "Target must be nonnegative.")
            result = recorder.status(args.deadline, args.target, args.since)
        elif args.command == "record":
            result = recorder.record(args.qid)
        else:
            data = json.load(sys.stdin) if args.input == "-" else read_json(Path(args.input))
            require(isinstance(data, dict), "Input must be one JSON object.")
            if args.command == "capture":
                data = capture_input(recorder, data, args.answer_file, args.use_reserved_query)
            result = getattr(recorder, args.command)(data)
        print(serialized(result), end="")
        return 0
    except (RecordingError, OSError, ValueError, KeyError, TypeError) as error:
        print(serialized({"error": str(error)}), file=sys.stderr, end="")
        return 2


if __name__ == "__main__":
    sys.exit(main())
