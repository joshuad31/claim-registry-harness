"""Quest throughput scorecard: did the quest meet the throughput standard, measured honestly?

The standard is the Ready-Fire-Aim throughput protocol's:

* count **unique usable QIDs** (a question counts once however many attempts it took; failed,
  unusable and duplicate attempts are reported separately and never counted);
* measure over the **whole active interval**, from the go-ahead (not the first send) until every
  answer is **graded**, excluding only disclosed intervals when the person was away;
* starting target **45 per hour**, aspiration **60**.

PASS needs all of these:

| Check | Pass when |
|---|---|
| Start-up | first question sent within 4 minutes of the go-ahead |
| 20-minute check | at least 15 usable QIDs saved by minute 20 |
| First hour | at least 45 usable QIDs captured **and graded** in the first hour |
| Whole quest | at least 45 usable graded QIDs per active hour, go-ahead to grading complete |
| Steering | captured-but-ungraded answers never exceed 12 (two six-answer rounds) |

60 per hour is reported as the aspiration. Without grading times, the graded checks read UNKNOWN,
never PASS.

Usage::

    python -m claimreg.notebooklm.scorecard <quest folder> [--start 2026-11-10T09:00-06:00]
           [--exclude 2026-11-10T09:20-06:00/2026-11-10T09:35-06:00] [--json]

Where it reads from:

* **The quest folder:** a `quest_tool` recording, a driver answers folder, or a harness run's
  `02_DISCOVERY` folder.
* **Grading times:** `assessment-ledger.json` (`committed_at` per round) or `assessed-qids.json`
  (`quest_tool.py assessed` stamps a time per QID).
* **The go-ahead:** `--start`, else the recording's `requested_at`, else the driver's
  `quest-clock.json`, else the first send. The last of these is labelled, because it hides start-up
  time.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TARGET, ASPIRATION, STARTUP_MIN, CHECK20, MAX_BACKLOG = 45, 60, 4, 15, 12


def ts(s) -> datetime | None:
    if not s:
        return None
    try:
        t = datetime.fromisoformat(str(s).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


# --------------------------------------------------------------------------- #
# reading a record into attempts + grading times + a start time
# --------------------------------------------------------------------------- #

def _discovery_folder(root: Path) -> Path | None:
    for p in [root, *root.rglob("02_query-responses")]:
        if (p / "responses.json").exists():
            return p
        if (p / "02_query-responses" / "responses.json").exists():
            return p / "02_query-responses"
    return None


def read_record(folder: Path) -> dict:
    folder = Path(folder)
    rec = {"source": str(folder), "attempts": [], "graded": {}, "start": None, "start_basis": None,
           "grading_basis": None}
    disc = _discovery_folder(folder)
    from ..quest_import import QuestImportError, find_layout, load_record
    try:
        layout = find_layout(folder)
    except QuestImportError:
        layout = None
    if layout and not (disc and layout["mode"] == "driver" and disc in layout["answers"].parents):
        _, atts = load_record(layout)
        for qid, lst in atts.items():
            for a in lst:
                rec["attempts"].append({"qid": qid, "attempt": a["attempt"], "submitted": ts(a["submitted_at"]),
                                        "captured": ts(a["captured_at"]), "usable": a["usable"],
                                        "outcome": a["outcome"], "lane": a["lane"]})
        rec["layout"] = layout["mode"]
        root = layout.get("recording") or layout.get("answers")
        run_json = (root / "run.json") if layout["mode"] == "recorder" else None
        if run_json and run_json.exists():
            rj = json.loads(run_json.read_text(encoding="utf-8"))
            if ts(rj.get("requested_at")):
                rec["start"], rec["start_basis"] = ts(rj["requested_at"]), "recorded go-ahead (run.json requested_at)"
        clock = next(iter(sorted(folder.rglob("quest-clock.json"))), None)
        if rec["start"] is None and clock:
            c = json.loads(clock.read_text(encoding="utf-8"))
            t = ts(c.get("go_ahead")) or ts(c.get("driver_started"))
            if t:
                rec["start"] = t
                rec["start_basis"] = ("recorded go-ahead (quest-clock.json)" if c.get("go_ahead")
                                      else "driver first started (quest-clock.json)")
    elif disc:
        rec["layout"] = "harness run"
        qf = disc.parent / "01_issued-questions" / "questions.json"
        q_lane = ({q["qid"]: q.get("notebook_lane") or "" for q in json.loads(qf.read_text(encoding="utf-8"))}
                  if qf.exists() else {})
        for r in json.loads((disc / "responses.json").read_text(encoding="utf-8")):
            sub = None
            md = disc / f"{r['qid']}__query-response.md"
            if md.exists():
                m = re.search(r"^Submitted:\s*(\S+)", md.read_text(encoding="utf-8", errors="replace"), re.M)
                sub = ts(m.group(1)) if m else None
            rec["attempts"].append({"qid": r["qid"], "attempt": r.get("attempt", "A01"),
                                    "submitted": sub or ts(r.get("submitted")), "captured": ts(r.get("captured")),
                                    "usable": bool(r.get("usable")), "outcome": r.get("outcome", ""),
                                    "lane": (r.get("retrieval") or {}).get("lane") or q_lane.get(r["qid"], "")})
    else:
        raise SystemExit(f"no quest record found in {folder}")

    # grading times
    led = next(iter(sorted(folder.rglob("assessment-ledger.json"))), None)
    if led:
        d = json.loads(led.read_text(encoding="utf-8"))
        for a in d.get("assessments", []):
            t = ts(a.get("committed_at"))
            for m in a.get("members", []):
                if t and m.get("qid") not in rec["graded"]:
                    rec["graded"][m["qid"]] = t
        rec["grading_basis"] = f"assessment ledger ({led.name}, committed_at per round)"
    if not rec["graded"]:
        af = next(iter(sorted(folder.rglob("assessed-qids.json"))), None)
        if af:
            d = json.loads(af.read_text(encoding="utf-8"))
            times = d.get("times", {}) if isinstance(d, dict) else {}
            rec["graded"] = {q: ts(t) for q, t in times.items() if ts(t)}
            if rec["graded"]:
                rec["grading_basis"] = f"{af.name} (time per QID from quest_tool.py assessed)"
            elif d:
                rec["grading_basis"] = f"{af.name} has no times (written by an older quest_tool)"
    return rec


# --------------------------------------------------------------------------- #
# the scorecard
# --------------------------------------------------------------------------- #

def _active_end(start: datetime, minutes: float, excludes) -> datetime:
    """The wall-clock time at which `minutes` of non-excluded time have passed since `start`."""
    t, left = start, timedelta(minutes=minutes)
    for a, b in sorted(excludes):
        if b <= t:
            continue
        if a > t and a - t >= left:
            break
        if a > t:
            left -= a - t
        t = max(t, b)
    return t + left


def _active_hours(a: datetime, b: datetime, excludes) -> float:
    total = (b - a).total_seconds()
    for x, y in excludes:
        lo, hi = max(a, x), min(b, y)
        if hi > lo:
            total -= (hi - lo).total_seconds()
    return max(total, 1.0) / 3600


def _pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else None


def score(rec: dict, start: datetime | None = None, excludes=()) -> dict:
    att = [a for a in rec["attempts"] if a["submitted"] or a["captured"]]
    if not att:
        raise SystemExit("the record has no timed attempts")
    first_send = min(a["submitted"] or a["captured"] for a in att)
    basis = rec.get("start_basis")
    if start is not None:
        basis = "given with --start"
    else:
        start = rec.get("start")
    if start is None:
        start, basis = first_send, "FIRST SEND (no go-ahead recorded: start-up time is hidden)"
    excludes = [(a, b) for a, b in excludes if b > a]
    # records from before the go-ahead (earlier test questions, a previous quest) are not this quest
    before = sorted({a["qid"] for a in att if (a["submitted"] or a["captured"]) < start})
    att = [a for a in att if (a["submitted"] or a["captured"]) >= start] or att
    first_send = min(a["submitted"] or a["captured"] for a in att)

    usable_at: dict[str, datetime] = {}
    for a in att:
        if a["usable"] and a["captured"]:
            usable_at[a["qid"]] = min(a["captured"], usable_at.get(a["qid"], a["captured"]))
    graded = {q: t for q, t in rec["graded"].items() if q in usable_at}
    have_grading = bool(graded)
    done = graded if have_grading else usable_at
    end = max(done.values()) if done else first_send
    hours = _active_hours(start, end, excludes)

    t20, t60 = _active_end(start, 20, excludes), _active_end(start, 60, excludes)
    n = lambda d, until: sum(1 for t in d.values() if t <= until)
    first_hour_cap, first_hour_graded = n(usable_at, t60), (n(graded, t60) if have_grading else None)
    saved20 = n(usable_at, t20)
    rate = len(done) / hours

    backlog, lag = None, []
    if have_grading:
        pts = sorted(set(usable_at.values()) | set(graded.values()))
        backlog = max((n(usable_at, x) - n(graded, x)) for x in pts)
        lag = [(graded[q] - usable_at[q]).total_seconds() / 60 for q in graded]

    lanes: dict[str, list] = {}
    for a in att:
        if a["submitted"] and a["captured"]:
            lanes.setdefault(a["lane"] or "?", []).append((a["submitted"], a["captured"]))
    refill, busy = [], 0.0
    for v in lanes.values():
        v.sort()
        busy += sum((c - s).total_seconds() for s, c in v)
        refill += [(s2 - c1).total_seconds() for (s1, c1), (s2, c2) in zip(v, v[1:]) if s2 >= c1]
    cap_end = max(usable_at.values()) if usable_at else end
    lane_window = max((cap_end - first_send).total_seconds(), 1.0) * max(len(lanes), 1)
    latency = [(a["captured"] - a["submitted"]).total_seconds() for a in att if a["submitted"] and a["captured"]]

    def verdict(ok, unknown=False):
        return "UNKNOWN" if unknown else ("PASS" if ok else "FAIL")

    startup_min = _active_hours(start, first_send, excludes) * 60 if first_send > start else 0.0
    checks = [
        {"check": "Start-up", "result": f"first send {startup_min:.1f} min after the go-ahead",
         "target": f"<= {STARTUP_MIN} min", "verdict": verdict(startup_min <= STARTUP_MIN,
                                                               unknown=basis.startswith("FIRST SEND"))},
        {"check": "20-minute check", "result": f"{saved20} usable QIDs saved",
         "target": f">= {CHECK20}", "verdict": verdict(saved20 >= CHECK20)},
        {"check": "First hour", "result": (f"{first_hour_graded} graded ({first_hour_cap} captured)" if have_grading
                                           else f"{first_hour_cap} captured; grading times not recorded"),
         "target": f">= {TARGET} graded (aspiration {ASPIRATION})",
         "verdict": verdict((first_hour_graded or 0) >= TARGET, unknown=not have_grading)},
        {"check": "Whole quest", "result": f"{len(done)} {'graded' if have_grading else 'captured'} in "
                                           f"{hours * 60:.0f} active min = {rate:.0f}/h",
         "target": f">= {TARGET}/h (aspiration {ASPIRATION}/h)",
         "verdict": verdict(rate >= TARGET, unknown=not have_grading)},
        {"check": "Steering", "result": (f"up to {backlog} captured answers waiting for grading; median "
                                         f"{statistics.median(lag):.0f} min capture-to-graded" if have_grading
                                         else "grading times not recorded"),
         "target": f"backlog <= {MAX_BACKLOG}", "verdict": verdict((backlog or 0) <= MAX_BACKLOG, unknown=not have_grading)},
    ]
    overall = ("PASS" if all(c["verdict"] == "PASS" for c in checks)
               else "FAIL" if any(c["verdict"] == "FAIL" for c in checks) else "INCOMPLETE")

    qids = {a["qid"] for a in att}
    bins, k = [], 0
    while start + timedelta(minutes=10 * k) < end and k < 60:
        lo, hi = start + timedelta(minutes=10 * k), start + timedelta(minutes=10 * k + 10)
        bins.append({"minutes": f"{10 * k}-{10 * k + 10}",
                     "captured": sum(1 for t in usable_at.values() if lo <= t < hi),
                     "graded": sum(1 for t in graded.values() if lo <= t < hi) if have_grading else None})
        k += 1
    return {
        "source": rec["source"], "layout": rec.get("layout"), "overall": overall,
        "clock": {"start": start.isoformat(), "start_basis": basis,
                  "first_send": first_send.astimezone(start.tzinfo).isoformat(timespec="seconds"),
                  "end": end.astimezone(start.tzinfo).isoformat(timespec="seconds"), "end_basis": "last grading" if have_grading else "last usable capture",
                  "excluded_minutes": round(sum((b - a).total_seconds() for a, b in excludes) / 60, 1),
                  "grading_basis": rec.get("grading_basis") or "none found"},
        "checks": checks,
        "counts": {"ignored_saved_before_go_ahead": before, "questions": len(qids), "attempts": len(att), "repeat_attempts": len(att) - len(qids),
                   "usable_qids": len(usable_at), "graded_qids": len(graded) if have_grading else None,
                   "questions_without_usable_answer": len(qids - set(usable_at)),
                   "failed_or_unusable_attempts": sum(1 for a in att if not a["usable"])},
        "diagnostics": {
            "lanes": len(lanes),
            "lane_busy_fraction": round(busy / lane_window, 2) if lanes else None,
            "answer_seconds_median": round(statistics.median(latency)) if latency else None,
            "answer_seconds_p90": round(_pct(latency, 0.9)) if latency else None,
            "save_to_refill_seconds_median": round(statistics.median(refill)) if refill else None,
            "save_to_refill_seconds_p90": round(_pct(refill, 0.9)) if refill else None,
            "refills_over_60s": f"{sum(1 for g in refill if g > 60)}/{len(refill)}" if refill else None,
            "capture_to_graded_minutes_median": round(statistics.median(lag)) if lag else None,
            "capture_to_graded_minutes_max": round(max(lag)) if lag else None,
            "bottleneck": _bottleneck(backlog, busy / lane_window if lanes else None, refill, startup_min, basis),
        },
        "per_10_minutes": bins,
    }


def _bottleneck(backlog, busy, refill, startup_min, basis) -> str:
    notes = []
    if not basis.startswith("FIRST SEND") and startup_min > STARTUP_MIN:
        notes.append(f"start-up ({startup_min:.0f} min before the first send)")
    if backlog is not None and backlog > MAX_BACKLOG:
        notes.append("grading (the Manager fell behind the lanes)")
    if busy is not None and busy < 0.6:
        notes.append("question supply or pacing (lanes idle most of the time)")
    if refill and statistics.median(refill) > 60:
        notes.append("capture/refill (lanes slow to get their next question)")
    return "; ".join(notes) or "none evident"


def render(sc: dict) -> str:
    c = sc["clock"]
    out = [f"# Quest throughput scorecard: {sc['overall']}", "",
           f"Record: `{sc['source']}` ({sc['layout']})",
           f"Clock: {c['start']} ({c['start_basis']}) to {c['end']} ({c['end_basis']})"
           + (f", {c['excluded_minutes']} min excluded as disclosed away time" if c["excluded_minutes"] else ""),
           f"Grading times: {c['grading_basis']}", "",
           "| Check | Result | Target | Verdict |", "|---|---|---|---|"]
    out += [f"| {x['check']} | {x['result']} | {x['target']} | **{x['verdict']}** |" for x in sc["checks"]]
    k = sc["counts"]
    out += ["", f"Counted once each: {k['usable_qids']} usable QIDs of {k['questions']} questions "
                f"({k['attempts']} attempts, {k['repeat_attempts']} repeats, {k['failed_or_unusable_attempts']} "
                f"failed or unusable attempts, {k['questions_without_usable_answer']} questions with no usable answer).",
            "", "| Diagnostic | Value |", "|---|---|"]
    out += [f"| {key.replace('_', ' ')} | {v} |" for key, v in sc["diagnostics"].items() if v is not None]
    out += ["", "| Minutes from go-ahead | Usable captured | Graded |", "|---|---:|---:|"]
    out += [f"| {b['minutes']} | {b['captured']} | {'' if b['graded'] is None else b['graded']} |"
            for b in sc["per_10_minutes"]]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Quest throughput scorecard (Ready-Fire-Aim standard).")
    ap.add_argument("folder", help="quest_tool recording, driver answers folder, or a run's 02_DISCOVERY")
    ap.add_argument("--start", help="the go-ahead time, e.g. 2026-11-10T09:00-06:00")
    ap.add_argument("--exclude", action="append", default=[], metavar="START/END",
                    help="a disclosed interval when the person was away (repeatable)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    a = ap.parse_args(argv)
    ex = []
    for e in a.exclude:
        x, _, y = e.partition("/")
        if not (ts(x) and ts(y)):
            ap.error(f"--exclude expects START/END ISO times, not {e!r}")
        ex.append((ts(x), ts(y)))
    if a.start and not ts(a.start):
        ap.error(f"--start is not an ISO time: {a.start!r}")
    sc = score(read_record(Path(a.folder)), start=ts(a.start), excludes=ex)
    print(json.dumps(sc, indent=1) if a.json else render(sc))
    return 0 if sc["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
