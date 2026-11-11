"""The quest relay: one command runs a whole NotebookLM discovery quest, unattended.

    python cr.py quest <project>            (starts the NotebookLM driver and this relay)
    python -m claimreg.notebooklm.relay run <quest.json>

A quest has exactly two research roles and the relay is neither of them:

* the **Investigator** (role ``quest_investigator``) writes the questions;
* the **Manager** (role ``quest_manager``) runs ACH_Eval on every round of answers and writes the
  feedback packet with ready-to-send questions.

Both are plain model calls made through the harness router, so each can have an ordered list of
providers in ``project.json`` and a refusal, outage or bad answer from one provider moves the call
to the next.  The relay itself is ordinary Python.  It moves files between the two roles and the
NotebookLM driver, applies the query firewall, commits each round, paces to the Manager, and
writes its status.  It makes no research judgment.

What goes where (all under the quest folder)::

    quest.json                       this quest's settings (also the driver's config)
    answers/                         the driver's folder: Qnnnn-A01.json, queue/, assessed-qids.json
    manager-workspace/answers/       each answer as Markdown, as the Manager reads it
    manager-workspace/packets/       Rnnn.md public feedback packets
    manager-workspace/private/       assessment-ledger.json, state/Rnnn.md, fragments/Rnnn-new.md, record.md
    asked.jsonl                      every question queued: QID, text, where it came from
    rejected.jsonl                   questions the firewall refused, with the reason
    relay-status.json, relay.log     what the relay is doing right now, and its history

Information barrier: the Investigator's prompt is built only from the header, the index, the
public packets and the list of questions asked.  Nothing under ``private/`` is ever read for it.

Restart safety: a round is committed by appending its entry to the ledger.  On restart, committed
rounds are skipped, the pacing file is re-synced from the ledger, and the quest clock's go-ahead
time is never overwritten.
"""

from __future__ import annotations

import json
import re
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from ..config import load_config
from ..header import parse_header
from ..index import compact_index, parse_index
from ..llm.base import BudgetExceeded, LLMRequest, Pending, ProviderError
from ..llm.router import LLM
from ..prompts import PromptLibrary
from ..quest_import import _attempt
from . import quest_tool

BLOCK = {name: re.compile(r"<<<%s\s*\n(.*?)\n?\s*%s>>>" % (name, name), re.S) for name in ("FRAGMENT", "STATE", "JSON")}
LEAK = re.compile(r"\b(?:A\d+-)?H[1-9]\b|\ballocation\s+(?:vector|units?)\b|\b\d{1,3}\s*/\s*64\b|stop_eligible|\bgauge\b",
                  re.I)
DIRECTIONS = ("CONTINUE", "REDIRECT", "HOLD", "STOP")
DEFAULTS = {"round_size": 6, "max_hours": 3.0, "max_questions": 400, "queue_ahead": 12,
            "max_wait_seconds": 240, "drain_minutes": 12, "poll_seconds": 3, "investigator_batch": 12,
            "investigator_min_interval": 20, "status_log_seconds": 60, "max_backlog": 12}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def local_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path: Path, default=None):
    """A JSON file, or ``default`` when it is missing or (after a short wait) still unreadable.
    Another process may be writing it at this instant, so a failed read is retried."""
    path = Path(path)
    for n in range(6):
        try:
            return json.loads(path.read_text(encoding="utf-8-sig"))
        except FileNotFoundError:
            return default
        except (OSError, ValueError):
            time.sleep(0.05)
    return default


def read_json_strict(path: Path, default):
    """Like read_json, but a file that exists and cannot be read is an error, never ``default``:
    used for the ledger, where treating an unreadable file as empty would lose committed rounds."""
    path = Path(path)
    if not path.exists():
        return default
    last: Exception | None = None
    for n in range(40):
        try:
            return json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as e:
            last = e
            time.sleep(0.05)
    raise RuntimeError(f"cannot read {path}: {last}")


def write_text(path: Path, text: str) -> None:
    from ..util import replace_file
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{threading.get_ident()}.tmp")
    tmp.write_text(text, encoding="utf-8")
    replace_file(tmp, path)


def write_json(path: Path, obj) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=1))


def norm_q(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()


# --------------------------------------------------------------------------- #
# parsing and validating the two Manager answers and the Investigator answer
# --------------------------------------------------------------------------- #

def parse_assessment(text: str) -> dict:
    """The three blocks of a Manager assessment.  Raises ValueError naming what is missing."""
    out = {}
    for name in ("FRAGMENT", "STATE", "JSON"):
        m = BLOCK[name].search(text or "")
        if not m:
            raise ValueError(f"the <<<{name} ... {name}>>> block is missing")
        out[name.lower()] = m.group(1).strip()
    try:
        raw = out["json"]
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
        out["data"] = json.loads(raw)
    except ValueError as e:
        raise ValueError(f"the JSON block does not parse ({e})") from e
    if not isinstance(out["data"], dict):
        raise ValueError("the JSON block must be an object")
    return out


def assessment_problem(text: str, gauge: int | None, axes: list[str]) -> str:
    """Why a Manager assessment cannot be committed, or ""."""
    try:
        a = parse_assessment(text)
    except ValueError as e:
        return str(e)
    d = a["data"]
    vec = d.get("vectors")
    if not isinstance(vec, dict) or not vec:
        return "JSON 'vectors' must give units for at least one axis"
    for ax, row in vec.items():
        if not isinstance(row, dict) or not row:
            return f"vectors[{ax}] must map hypothesis ids to integer units"
        if not all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in row.values()):
            return f"vectors[{ax}] must contain nonnegative integers"
        if gauge and sum(row.values()) != gauge:
            return f"vectors[{ax}] sums to {sum(row.values())}, but the gauge is {gauge}"
    if axes and not any(ax in vec for ax in axes):
        return "vectors names none of the enabled axes: " + ", ".join(axes)
    if str(d.get("direction", "")).upper() not in DIRECTIONS:
        return "JSON 'direction' must be CONTINUE, REDIRECT, HOLD or STOP"
    if len(a["state"].split()) < 30:
        return "the STATE block is too short to be a usable state"
    return ""


def packet_problem(text: str) -> str:
    items = quest_tool._ready_items(text or "")
    if items is None:
        return "there is no '## Ready questions' section"
    if len(items) < 4:
        return f"only {len(items)} ready question(s); 8 to 10 are needed"
    m = LEAK.search(text)
    if m:
        return f"the packet contains private assessment vocabulary (\"{m.group(0)}\"); remove every score and label"
    return ""


def ready_questions(packet_text: str) -> list[dict]:
    out = []
    for item in quest_tool._ready_items(packet_text or "") or []:
        target = axis = None
        m = quest_tool.AXIS_PREFIX.match(item)
        if m:
            axis, item = m.group("axis").upper(), item[m.end():].strip()
        m = quest_tool.TARGET_PREFIX.match(item)
        if m:
            target, item = m.group("target").strip(), item[m.end():].strip()
        if item:
            out.append({"text": item, "target": target, "axis": axis})
    return out


# --------------------------------------------------------------------------- #
# the relay
# --------------------------------------------------------------------------- #

class Relay:
    def __init__(self, quest_json: str | Path, llm: LLM | None = None, echo: bool = True):
        self.cfg_path = Path(quest_json).resolve()
        cfg = read_json(self.cfg_path)
        if not isinstance(cfg, dict):
            raise SystemExit(f"relay: cannot read {self.cfg_path}")
        self.cfg = {**DEFAULTS, **cfg}
        self.q = self.cfg_path.parent
        self.answers = (self.q / self.cfg.get("answers_dir", "answers")).resolve()
        self.queue = self.answers / "queue"
        self.ws = (self.q / self.cfg.get("workspace", "manager-workspace")).resolve()
        self.private = self.ws / "private"
        self.ledger_path = self.private / "assessment-ledger.json"
        self.assessed_path = ((self.q / self.cfg["assessed_file"]).resolve() if self.cfg.get("assessed_file")
                              else self.answers / "assessed-qids.json")
        for d in (self.queue, self.ws / "answers", self.ws / "packets", self.private / "state",
                  self.private / "fragments"):
            d.mkdir(parents=True, exist_ok=True)
        self.project = (self.q / self.cfg.get("project", "../..")).resolve()
        self.pcfg = load_config(self.project)
        self.llm = llm or LLM(self.pcfg, log_name="quest-llm-calls.jsonl")
        self.prompts = PromptLibrary(self.project)
        self.echo = echo
        self.run_id = str(self.cfg.get("run_id") or self.q.name)

        frame = self.pcfg.get("frame", {})
        hp = self._first([self.project / frame.get("header_file", "01_FRAME/header.md"),
                          self.project / "01_FRAME" / "header.md"])
        ip = self._first([self.project / frame.get("index_file", "01_FRAME/index.md"),
                          self.project / "01_FRAME" / "index.md"])
        if not hp:
            raise SystemExit(f"relay: no header found in {self.project / '01_FRAME'} (the header must be approved "
                             f"before a quest starts)")
        self.header = hp.read_text(encoding="utf-8", errors="replace")
        self.index_text = ip.read_text(encoding="utf-8", errors="replace") if ip else ""
        self.index_path = ip
        try:
            self.index_compact = compact_index(parse_index(self.index_text, None)) if self.index_text else ""
        except Exception:
            self.index_compact = ""
        if len(self.index_compact.splitlines()) < 2:
            self.index_compact = self.index_text[:60000]
        self.known = quest_tool._known_filenames(ip) if ip else None
        try:
            fr = parse_header(self.header)
        except Exception:
            fr = {"axes": [], "gauge": None}
        self.gauge = int(self.cfg.get("gauge") or fr.get("gauge") or 64)
        self.axes_enabled = [ax["axis_id"] for ax in fr.get("axes", [])
                             if str(ax.get("approval", "")).upper() != "TEST_ONLY"] or \
                            [ax["axis_id"] for ax in fr.get("axes", [])]
        # every question is filed under exactly one of these axes (docs/AXIS-DATABASES.md)
        self.axis_ids = [ax["axis_id"] for ax in fr.get("axes", [])]
        self.axis_names = {ax["axis_id"]: (ax.get("name") or ax.get("question") or "") for ax in fr.get("axes", [])}
        self.axes_list = "\n".join(f"{a}: {n}" for a, n in self.axis_names.items()) or "(one axis)"
        self.axes_text = "; ".join(f"{ax['axis_id']} ({str(ax.get('approval') or 'approval not stated').lower()})"
                                   for ax in fr.get("axes", [])) or "as the header defines"

        self.lock = threading.RLock()
        self.stop_event = threading.Event()
        self.stop_reason = ""
        self.manager_stop = False
        self.t0 = time.time()
        self.errors: list[str] = []
        self.last = {"quest_manager": "", "quest_investigator": ""}
        self.manager_failures = 0
        self.investigator_backoff_until = 0.0
        self.repair_requests: dict[str, str] = {}
        self.round_times: list[float] = []

    @staticmethod
    def _first(paths):
        for p in paths:
            if p and Path(p).is_file():
                return Path(p)
        return None

    # ---------------------------------------------------------------- log
    def log(self, msg: str) -> None:
        line = f"{local_now()}  {msg}"
        with self.lock:
            with open(self.q / "relay.log", "a", encoding="utf-8") as f:
                f.write(line + "\n")
        if self.echo:
            try:
                print(line, flush=True)
            except Exception:
                pass

    def note_error(self, msg: str) -> None:
        self.errors.append(f"{local_now()} {msg}")
        self.errors = self.errors[-20:]
        self.log("ERROR " + msg)

    # ---------------------------------------------------------------- records on disk
    def ledger(self) -> dict:
        d = read_json_strict(self.ledger_path, default=None)
        if d is None:
            d = {"run_id": self.run_id, "assessments": []}
        if not isinstance(d, dict):
            raise RuntimeError(f"{self.ledger_path} is not a ledger object; fix or move it before continuing")
        d.setdefault("assessments", [])
        return d

    def graded(self) -> set[str]:
        return {m.get("qid") for a in self.ledger()["assessments"] for m in a.get("members", [])}

    def attempts(self) -> dict[str, list[dict]]:
        out: dict[str, list[dict]] = {}
        for f in sorted(self.answers.glob("Q*-A*.json")):
            d = read_json(f)
            if not isinstance(d, dict):
                continue
            qid = str(d.get("qid") or f.name.split("-")[0])
            att = str(d.get("attempt") or f.stem.split("-")[-1])
            a = _attempt(qid, att, d.get("query", ""), d.get("answer", ""), d.get("outcome", ""), d, f, set())
            a["file"] = f
            out.setdefault(qid, []).append(a)
        for lst in out.values():
            lst.sort(key=lambda a: a["attempt"])
        return out

    @staticmethod
    def best(atts: list[dict]) -> dict | None:
        """The newest usable attempt without tool output, else the newest usable attempt."""
        for a in reversed(atts):
            if a["usable"] and not a["contains_tool_output"]:
                return a
        for a in reversed(atts):
            if a["usable"]:
                return a
        return None

    def axis_dir(self, axis: str | None) -> Path:
        """Where one axis's questions and answers are kept in the quest folder (the quest folder
        itself for a single-axis quest, or for a question with no axis recorded)."""
        return self.q / f"AXIS-{axis}" if axis and len(self.axis_ids) > 1 else self.q

    def resolve_axis(self, axis, target) -> str | None:
        """The one axis a question is asked for: stated by its author, else named by a single axis
        label in its target ("A2 trial results").  None when neither gives exactly one axis."""
        if len(self.axis_ids) == 1:
            return self.axis_ids[0]
        a = str(axis or "").strip().upper()
        if a in self.axis_ids:
            return a
        named = {"A" + n for n in re.findall(r"\bA(\d+)\b", str(target or ""))} & set(self.axis_ids)
        return next(iter(named)) if len(named) == 1 else None

    def axis_of(self, qid: str) -> str | None:
        for r in self.asked():
            if r.get("qid") == qid and r.get("axis"):
                return r["axis"]
        return None

    def answer_md(self, stem: str) -> Path:
        """The staged Markdown of one answer, kept under its question's axis."""
        axis = self.axis_of(stem.split("-")[0])
        base = self.ws / "answers"
        return (base / f"AXIS-{axis}" if axis and len(self.axis_ids) > 1 else base) / (stem + ".md")

    def asked(self) -> list[dict]:
        rows = []
        for p in [self.q / "asked.jsonl"] + sorted(self.q.glob("AXIS-*/asked.jsonl")):
            if p.exists():
                for line in p.read_text(encoding="utf-8").splitlines():
                    try:
                        rows.append(json.loads(line))
                    except ValueError:
                        pass
        rows.sort(key=lambda r: (str(r.get("qid")), str(r.get("attempt", "A01"))))
        have = {(r.get("qid"), r.get("attempt", "A01")) for r in rows}
        # questions queued by hand or by an earlier tool are part of the record too
        for f in sorted(self.queue.glob("Q*.json")):
            j = read_json(f)
            if isinstance(j, dict) and j.get("qid") and (j["qid"], j.get("attempt", "A01")) not in have:
                rows.append({"qid": j["qid"], "attempt": j.get("attempt", "A01"), "text": j.get("text", ""),
                             "origin": "queue file"})
        return rows

    def driver_pushed(self) -> set[str]:
        d = read_json(self.answers / "driver-state.json", default={}) or {}
        return set(d.get("pushed", []))

    def queue_state(self) -> dict:
        saved = {f.stem for f in self.answers.glob("Q*-A*.json")}           # "Q0001-A01"
        pushed = self.driver_pushed()
        unsent, in_flight = [], []
        for f in sorted(self.queue.glob("Q*.json")):
            stem = f.stem if "-A" in f.stem else f.stem + "-A01"
            if stem in saved:
                continue
            (in_flight if f.name in pushed else unsent).append(f.name)
        return {"unsent": unsent, "in_flight": in_flight}

    def lanes(self) -> dict:
        st = read_json(self.answers / "driver-status.json", default={}) or {}
        lanes = st.get("lanes", {}) if isinstance(st, dict) else {}
        return {"feed": st.get("feed", ""), "at": st.get("at", ""), "count": len(lanes) or len(self.cfg.get("notebooks", {})) or 1,
                "busy": sum(1 for v in lanes.values() if v.get("state") not in ("FREE", None))}

    # ---------------------------------------------------------------- clock
    def stamp_go_ahead(self) -> None:
        clock = self.answers / "quest-clock.json"
        c = read_json(clock, default={}) or {}
        if not c.get("go_ahead"):
            c.update({"run_id": c.get("run_id") or self.run_id, "go_ahead": local_now(),
                      "note": "go-ahead = the moment the relay first started for this quest"})
            write_json(clock, c)
        try:
            t = datetime.fromisoformat(str(c["go_ahead"]))
            self.t0 = t.timestamp()
        except (ValueError, KeyError):
            pass

    def elapsed_hours(self) -> float:
        return max(0.0, (time.time() - self.t0) / 3600.0)

    # ---------------------------------------------------------------- staging
    def stage(self) -> None:
        for f in sorted(self.answers.glob("Q*-A*.json")):
            target = self.answer_md(f.stem)
            if target.exists() and target.stat().st_mtime >= f.stat().st_mtime:
                continue
            d = read_json(f)
            if isinstance(d, dict):
                write_text(target, quest_tool.stage_markdown(d, f.name))

    # ---------------------------------------------------------------- Manager
    def ready_to_grade(self) -> list[dict]:
        graded = self.graded()
        out = []
        for qid, atts in self.attempts().items():
            if qid in graded:
                continue
            b = self.best(atts)
            if b:
                out.append(b)
        out.sort(key=lambda a: (a.get("captured_at") or "", a["qid"]))
        return out

    def state_text(self) -> tuple[str, str]:
        led = self.ledger()["assessments"]
        for a in reversed(led):
            p = self.private / "state" / f"{a['assessment_id']}.md"
            if p.exists():
                return a["assessment_id"], p.read_text(encoding="utf-8")
        legacy = self.private / "state.md"
        if led and legacy.exists():
            return led[-1]["assessment_id"], legacy.read_text(encoding="utf-8")
        return "", "(none: this is the first assessment round; set the baseline)"

    def next_round_id(self) -> str:
        nums = [int(m.group(1)) for a in self.ledger()["assessments"]
                if (m := re.match(r"R(\d+)$", str(a.get("assessment_id", ""))))]
        return "R%03d" % ((max(nums) + 1) if nums else 1)

    def run_round(self, members: list[dict]) -> bool:
        rid = self.next_round_id()
        _, state = self.state_text()
        blocks = []
        for a in members:
            md = self.answer_md(a["file"].stem)
            body = md.read_text(encoding="utf-8") if md.exists() else quest_tool.stage_markdown(
                read_json(a["file"]) or {}, a["file"].name)
            blocks.append(f"=== {a['qid']}-{a['attempt']} ===\n{body}")
        mem_txt = ", ".join(f"{a['qid']}-{a['attempt']}" for a in members)
        system, user, _ = self.prompts.render(
            "quest_assess.md", ROUND=rid, INVESTIGATION_ID=self.run_id, GAUGE=self.gauge, AXES=self.axes_text,
            HEADER=self.header, STATE=state, MEMBERS=mem_txt, ANSWERS="\n\n".join(blocks))
        req = LLMRequest(role="quest_manager", system=system, user=user, expect_json=False, tag=f"assess:{rid}",
                         meta={"round": rid, "members": mem_txt})
        t = time.time()
        self.log(f"{rid}: grading {mem_txt}")
        try:
            resp = self.llm.call(req, validate=lambda txt: assessment_problem(txt, self.gauge, self.axes_enabled))
        except (ProviderError, BudgetExceeded, Pending) as e:
            self.manager_failures += 1
            self.note_error(f"{rid}: the Manager call failed on every provider ({type(e).__name__}: {str(e)[:300]})")
            return False
        problem = resp.parse_error or assessment_problem(resp.text, self.gauge, self.axes_enabled)
        if problem:
            self.manager_failures += 1
            self.note_error(f"{rid}: the Manager's answer could not be committed ({problem[:300]})")
            return False
        a = parse_assessment(resp.text)
        d = a["data"]
        self.last["quest_manager"] = f"{resp.provider}:{resp.model}" + (" (after failover)" if resp.failover else "")
        # 1. the grow-only record and the new state (safe to redo: the commit is the ledger entry)
        write_text(self.private / "fragments" / f"{rid}-new.md", f"# {rid} new material ({mem_txt})\n\n{a['fragment']}\n")
        with open(self.private / "record.md", "a", encoding="utf-8") as f:
            f.write(f"\n\n# {rid} ({mem_txt})\n\n{a['fragment']}\n")
        write_text(self.private / "state" / f"{rid}.md", a["state"] + "\n")
        write_text(self.private / "state.md", a["state"] + "\n")
        # 2. commit
        direction = str(d.get("direction", "CONTINUE")).upper()
        entry = {"assessment_id": rid, "committed_at": utc_now(),
                 "members": [{"qid": m["qid"], "attempt": m["attempt"]} for m in members],
                 "vectors": d["vectors"], "stop_eligible": bool(d.get("stop_eligible")), "direction": direction,
                 "provider": resp.provider, "model": resp.model,
                 "failover": resp.failover, "seconds": round(time.time() - t, 1)}
        with self.lock:
            led = self.ledger()
            led["assessments"].append(entry)
            write_json(self.ledger_path, led)
            self.sync()
            for r in d.get("repairs") or []:
                if isinstance(r, dict) and re.match(r"Q\d+$", str(r.get("qid", ""))):
                    self.repair_requests.setdefault(r["qid"], str(r.get("reason", ""))[:200])
        self.manager_failures = 0
        self.round_times.append(time.time() - t)
        self.log(f"{rid}: committed in {entry['seconds']:.0f}s by {resp.provider} ({direction})")
        if direction == "STOP" and entry["stop_eligible"]:
            self.manager_stop = True
        # 3. the public packet (a failure here never loses the round)
        self.write_packet(rid, a["state"], direction)
        return True

    def write_packet(self, rid: str, state: str, direction: str) -> None:
        asked_txt, n = self.asked_summary()
        system, user, _ = self.prompts.render(
            "quest_packet.md", ROUND=rid, DIRECTION=direction, HEADER=self.header, STATE=state,
            INDEX=self.index_compact, ASKED=asked_txt, ASKED_COUNT=n)
        req = LLMRequest(role="quest_manager", system=system, user=user, expect_json=False, tag=f"packet:{rid}",
                         meta={"round": rid})
        try:
            resp = self.llm.call(req, validate=packet_problem)
        except (ProviderError, BudgetExceeded, Pending) as e:
            self.note_error(f"{rid}: no packet (the call failed on every provider: {str(e)[:200]}); the "
                            f"Investigator will fill the gap")
            return
        problem = resp.parse_error or packet_problem(resp.text)
        if problem:
            self.note_error(f"{rid}: packet rejected ({problem[:200]}); the Investigator will fill the gap")
            return
        write_text(self.ws / "packets" / f"{rid}.md", resp.text.strip() + "\n")
        self.log(f"{rid}: packet written with {len(ready_questions(resp.text))} ready questions")

    def sync(self) -> None:
        """Ledger -> assessed-qids.json (the driver's pacing file and the scorecard's grading times)."""
        ledger = self.ledger()
        data = read_json(self.assessed_path, default={}) or {}
        if isinstance(data, list):
            data = {"assessed": data, "times": {}}
        have, times = set(data.get("assessed", [])), dict(data.get("times", {}))
        for a in ledger["assessments"]:
            when = quest_tool._utc_iso(a.get("committed_at"))
            for m in a.get("members", []):
                if m.get("qid"):
                    have.add(m["qid"])
                    if when:
                        times.setdefault(m["qid"], when)
        write_json(self.assessed_path, {"assessed": sorted(have), "times": times})

    def manager_loop(self) -> None:
        size = int(self.cfg["round_size"])
        while True:
            try:
                ready = self.ready_to_grade()
                qs = self.queue_state()
                stopping = self.stop_event.is_set()
                if stopping and self._hard_expired():
                    # a wedged provider or driver must not hold the relay open: close out with what is graded
                    self.note_error("manager loop: hard deadline reached after stop; closing with rounds graded so far")
                    return
                idle = not qs["unsent"] and not qs["in_flight"]
                lanes = self.lanes()
                # A driver HOLD means its backlog (answers waiting for grading + in-flight) is at the
                # limit.  If no lane is busy and answers are ready, the hold is what is stopping the
                # queue: take a short round now instead of waiting for max_wait_seconds, so grading
                # releases the driver and it can push more questions (the LEVO deadlock).
                holding = str(lanes.get("feed", "")).startswith("HOLD") and int(lanes.get("busy") or 0) == 0
                waited = 0.0
                if ready:
                    try:
                        t = datetime.fromisoformat(str(ready[0].get("captured_at")).replace("Z", "+00:00"))
                        waited = time.time() - t.timestamp()
                    except ValueError:
                        waited = 0.0
                # a short round is graded only when no full round is coming: the quest is stopping, the
                # question budget is spent and the lanes are empty, or an answer has waited too long
                spent = len({r["qid"] for r in self.asked()}) >= int(self.cfg["max_questions"])
                take = []
                if len(ready) >= size:
                    take = ready[:size]
                elif ready and ((stopping and (idle or self._drain_expired())) or (idle and spent)
                                or (holding and ready) or waited > float(self.cfg["max_wait_seconds"])):
                    take = ready
                if take:
                    ok = self.run_round(take)
                    if not ok:
                        time.sleep(min(60, 5 * self.manager_failures))
                    continue
                if stopping and (idle or self._drain_expired()):
                    return
            except Exception as e:  # noqa: BLE001 - the relay must keep running
                self.note_error(f"manager loop: {type(e).__name__}: {e}")
                time.sleep(5)
            time.sleep(1.0)

    def _hard_expired(self) -> bool:
        limit = float(self.cfg["drain_minutes"]) + float(self.cfg.get("hard_stop_minutes", 10))
        return bool(self.stop_at) and time.time() - self.stop_at > 60 * limit

    def _drain_expired(self) -> bool:
        return bool(self.stop_at) and time.time() - self.stop_at > 60 * float(self.cfg["drain_minutes"])

    # ---------------------------------------------------------------- questions
    def asked_summary(self) -> tuple[str, int]:
        rows = [r for r in self.asked() if r.get("attempt", "A01") == "A01"]
        counts: dict[str, int] = {}
        for r in rows:
            for m in quest_tool.SOURCE_TOKEN.finditer(r.get("text", "")):
                counts[m.group(0)] = counts.get(m.group(0), 0) + 1
        lines = [f"{r['qid']}{' [' + r['axis'] + ']' if r.get('axis') else ''}: "
                 f"{' '.join(str(r.get('text', '')).split()[:32])}" for r in rows[-150:]]
        if len(self.axis_ids) > 1:
            per = {a: sum(1 for r in rows if r.get("axis") == a) for a in self.axis_ids}
            lines.append("Questions asked so far per axis: " + ", ".join(f"{a} {n}" for a, n in per.items()))
        cnt = ", ".join(f"{k} x{v}" for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:80])
        return ("\n".join(lines) or "(none yet)") + ("\n\nTimes each source has been named: " + cnt if cnt else ""), len(rows)

    def pool(self) -> list[dict]:
        """Ready questions from the public packets that have not been asked, newest packet first."""
        asked = {norm_q(r.get("text", "")) for r in self.asked()}
        out = []
        for p in sorted((self.ws / "packets").glob("R*.md"), reverse=True):
            for i, q in enumerate(ready_questions(p.read_text(encoding="utf-8", errors="replace"))):
                if norm_q(q["text"]) not in asked:
                    out.append({**q, "origin": f"packet {p.stem} #{i + 1}"})
        return out

    def enqueue(self, text: str, origin: str, target: str | None = None, qid: str | None = None,
                attempt: str = "A01", axis: str | None = None) -> str | None:
        """Queue one question if it passes the firewall.  Returns its QID, or None when refused.

        A question belongs to exactly one axis, chosen by whoever wrote it.  A question that does
        not name one axis is refused: questions are never shared between axes."""
        with self.lock:
            asked_rows = self.asked()
            if attempt == "A01":
                axis = self.resolve_axis(axis, target)
                asked = {norm_q(r.get("text", "")) for r in asked_rows}
                warnings = quest_tool.firewall_warnings(text, self.known, asked)
                if norm_q(text) in asked and "identical question is already in the queue" not in warnings:
                    warnings.append("identical question is already in the queue")
                if not axis and len(self.axis_ids) > 1:
                    warnings.append("the question is not filed under exactly one axis (give \"axis\": one of "
                                    + ", ".join(self.axis_ids) + ")")
                if warnings:
                    d = self.axis_dir(axis)
                    d.mkdir(parents=True, exist_ok=True)
                    with open(d / "rejected.jsonl", "a", encoding="utf-8") as f:
                        f.write(json.dumps({"at": utc_now(), "axis": axis, "text": text, "origin": origin,
                                            "warnings": warnings}, ensure_ascii=False) + "\n")
                    return None
                qid = "Q%04d" % quest_tool._next_qid(self.answers)
                name = qid + ".json"
            else:
                name = f"{qid}-{attempt}.json"
                axis = axis or next((r.get("axis") for r in asked_rows if r.get("qid") == qid and r.get("axis")), None)
            # the queue file is what reaches the notebook page: the question and nothing else.  The
            # axis and target are recorded in the axis's own asked.jsonl below.
            write_json(self.queue / name, {"qid": qid, "attempt": attempt, "text": text})
            d = self.axis_dir(axis)
            d.mkdir(parents=True, exist_ok=True)
            with open(d / "asked.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps({"qid": qid, "attempt": attempt, "axis": axis, "text": text, "target": target,
                                    "origin": origin, "queued_at": utc_now()}, ensure_ascii=False) + "\n")
            return qid

    def queue_repairs(self) -> int:
        """Re-ask once (A02) any question whose first answer failed, was off-target, carries tool
        output, or that the Manager asked to have repaired."""
        n = 0
        for qid, why, text in self.pending_repairs():
            self.enqueue(text, f"repair of {qid}-A01: {why}", qid=qid, attempt="A02")
            self.log(f"repair queued: {qid}-A02 ({why})")
            n += 1
        return n

    def pending_repairs(self) -> list[tuple[str, str, str]]:
        out = []
        asked = {(r.get("qid"), r.get("attempt", "A01")): r for r in self.asked()}
        for qid, atts in self.attempts().items():
            if (qid, "A02") in asked or any(a["attempt"] != "A01" for a in atts):
                continue
            first = atts[0]
            why = ""
            if not first["usable"]:
                why = f"first answer not usable ({first['outcome'] or 'no answer'})"
            elif first["contains_tool_output"]:
                why = "first answer carries notebook tool output"
            elif qid in self.repair_requests:
                why = "Manager request: " + self.repair_requests[qid]
            text = first.get("query") or (asked.get((qid, "A01")) or {}).get("text", "")
            if why and text:
                out.append((qid, why, text))
        return out

    def ask_investigator(self, n: int) -> int:
        packets = sorted((self.ws / "packets").glob("R*.md"))
        packet = packets[-1].read_text(encoding="utf-8", errors="replace") if packets else \
            "(none yet: this is the opening batch. Cover the highest-ranked sources and each decisive test.)"
        asked_txt, count = self.asked_summary()
        system, user, _ = self.prompts.render(
            "quest_questions.md", HEADER=self.header, INDEX=self.index_compact, PACKET=packet,
            ASKED=asked_txt, ASKED_COUNT=count, N=n, AXES=self.axes_list)
        self.last_investigator_prompt = system + "\n" + user          # kept for the information-barrier test
        req = LLMRequest(role="quest_investigator", system=system, user=user, tag=f"questions:{count}",
                         meta={"asked": count, "n": n})

        def problem(parsed) -> str:
            qs = parsed.get("questions") if isinstance(parsed, dict) else None
            return "" if isinstance(qs, list) and any(isinstance(q, dict) and q.get("text") for q in qs) \
                else "return {\"questions\": [{\"axis\", \"target\", \"sources\", \"text\"}]} with at least one question"
        try:
            resp = self.llm.call(req, validate=problem)
        except (ProviderError, BudgetExceeded, Pending) as e:
            self.note_error(f"the Investigator call failed on every provider ({str(e)[:200]})")
            return 0
        if resp.parse_error or not isinstance(resp.parsed, dict):
            self.note_error(f"the Investigator's answer could not be used ({resp.parse_error[:200]})")
            return 0
        self.last["quest_investigator"] = f"{resp.provider}:{resp.model}" + (" (after failover)" if resp.failover else "")
        made = 0
        for q in resp.parsed.get("questions", []):
            if isinstance(q, dict) and str(q.get("text", "")).strip():
                if self.enqueue(str(q["text"]).strip(), "investigator", q.get("target"), axis=q.get("axis")):
                    made += 1
        self.log(f"Investigator wrote {made} usable question(s) of {len(resp.parsed.get('questions', []))}")
        return made

    def top_up(self) -> None:
        if self.stop_event.is_set():
            return
        n_asked = len({r["qid"] for r in self.asked()})
        room_total = int(self.cfg["max_questions"]) - n_asked
        self.queue_repairs()
        qs = self.queue_state()
        need = min(int(self.cfg["queue_ahead"]) - len(qs["unsent"]), room_total)
        if need <= 0:
            return
        for q in self.pool():
            if need <= 0:
                break
            if self.enqueue(q["text"], q["origin"], q.get("target"), axis=q.get("axis")):
                need -= 1
        if need <= 0:
            return
        # nothing ready from the Manager: the Investigator writes questions when the lanes would
        # otherwise run dry (always true for the opening batch)
        qs = self.queue_state()
        lanes = self.lanes()["count"]
        if len(qs["unsent"]) < lanes and time.time() >= self.investigator_backoff_until:
            made = self.ask_investigator(min(max(need, lanes), int(self.cfg["investigator_batch"])))
            gap = float(self.cfg["investigator_min_interval"])
            self.investigator_backoff_until = time.time() + (gap if made else 3 * gap)

    def feeder_loop(self) -> None:
        while not self.stop_event.is_set():
            try:
                self.stage()
                self.top_up()
            except Exception as e:  # noqa: BLE001
                self.note_error(f"feeder loop: {type(e).__name__}: {e}")
            time.sleep(float(self.cfg["poll_seconds"]))
        # after STOP the lanes finish their current answers; keep staging them for the last rounds
        while not self.done_event.is_set():
            try:
                self.stage()
            except Exception:
                pass
            time.sleep(float(self.cfg["poll_seconds"]))

    # ---------------------------------------------------------------- status and stop
    def by_axis(self, usable: set, graded: set) -> dict:
        rows = [r for r in self.asked() if r.get("attempt", "A01") == "A01"]
        out = {}
        for a in self.axis_ids:
            qids = {r["qid"] for r in rows if r.get("axis") == a}
            out[a] = {"asked": len(qids), "usable": len(qids & usable), "graded": len(qids & graded)}
        return out

    def status(self) -> dict:
        atts = self.attempts()
        usable = {q for q, a in atts.items() if self.best(a)}
        graded = self.graded() & set(atts)
        qs = self.queue_state()
        hours = self.elapsed_hours()
        led = self.ledger()["assessments"]
        st = {"at": local_now(), "run_id": self.run_id, "elapsed_minutes": round(hours * 60, 1),
              "questions_asked": len({r["qid"] for r in self.asked()}),
              "by_axis": self.by_axis(usable, graded),
              "answers_usable": len(usable), "answers_graded": len(graded),
              "grading_backlog": len(usable - graded), "graded_per_hour": round(len(graded) / hours, 1) if hours > 0.02 else None,
              "rounds_committed": len(led), "last_round": led[-1]["assessment_id"] if led else None,
              "median_round_seconds": (sorted(self.round_times)[len(self.round_times) // 2] if self.round_times else None),
              "queue_unsent": len(qs["unsent"]), "queue_in_flight": len(qs["in_flight"]),
              "driver": self.lanes(), "providers_last_used": self.last,
              "failovers": self.llm.failovers, "model_calls": self.llm.calls_made,
              "estimated_usd": round(self.llm.usd_spent, 4),
              "manager_consecutive_failures": self.manager_failures,
              "stopping": self.stop_reason or None, "recent_errors": self.errors[-5:]}
        write_json(self.q / "relay-status.json", st)
        return st

    def check_stop(self) -> str:
        if (self.q / "STOP").exists() or (self.queue / "STOP").exists():
            return "STOP file"
        if self.manager_stop:
            return "the Manager directed STOP (stop-eligible)"
        if self.elapsed_hours() >= float(self.cfg["max_hours"]):
            return f"time limit ({self.cfg['max_hours']} h)"
        if self.manager_failures >= 6:
            return "the Manager failed six times in a row on every provider"
        n_asked = len({r["qid"] for r in self.asked()})
        if n_asked >= int(self.cfg["max_questions"]):
            qs = self.queue_state()
            if not qs["unsent"] and not qs["in_flight"] and not self.ready_to_grade() \
                    and not self.pending_repairs():
                return f"question limit ({self.cfg['max_questions']}) reached and everything graded"
        return ""

    stop_at = 0.0

    def run(self, max_seconds: float | None = None) -> dict:
        self.stamp_go_ahead()
        with self.lock:
            self.sync()                      # restart safety: the pacing file always matches the ledger
        self.done_event = threading.Event()
        self.log(f"relay started for {self.run_id}: Manager -> {self.llm.chain_for('quest_manager')}, "
                 f"Investigator -> {self.llm.chain_for('quest_investigator')}; gauge {self.gauge}; "
                 f"{len(self.ledger()['assessments'])} round(s) already committed")
        threads = [threading.Thread(target=self.manager_loop, name="manager", daemon=True),
                   threading.Thread(target=self.feeder_loop, name="feeder", daemon=True)]
        for t in threads:
            t.start()
        started = last_log = time.time()
        try:
            while threads[0].is_alive():
                st = self.status()
                if not self.stop_event.is_set():
                    why = self.check_stop()
                    if not why and max_seconds is not None and time.time() - started > max_seconds:
                        why = "relay max_seconds reached"
                    if why:
                        self.stop_reason, self.stop_at = why, time.time()
                        (self.queue / "STOP").write_text("stop: " + why, encoding="utf-8")
                        self.stop_event.set()
                        self.log(f"stopping: {why}. The lanes finish their current answers; grading continues "
                                 f"until the record is closed.")
                if time.time() - last_log >= float(self.cfg["status_log_seconds"]):
                    last_log = time.time()
                    self.log(f"status: asked {st['questions_asked']}, usable {st['answers_usable']}, graded "
                             f"{st['answers_graded']}, backlog {st['grading_backlog']}, unsent {st['queue_unsent']}, "
                             f"rate {st['graded_per_hour']}/h")
                time.sleep(float(self.cfg["poll_seconds"]))
        except KeyboardInterrupt:
            self.stop_reason = self.stop_reason or "interrupted (Ctrl+C)"
            (self.queue / "STOP").write_text("stop: interrupted", encoding="utf-8")
            self.stop_event.set()
            self.log("interrupted: answers and committed rounds are on disk; run the same command to resume.")
        self.done_event.set()
        self.stage()
        st = self.status()
        self.closeout(st)
        return st

    def closeout(self, st: dict) -> None:
        atts = self.attempts()
        selected = sorted(f"{q}-{b['attempt']}" for q, a in atts.items() if (b := self.best(a)) and b["attempt"] != "A01")
        scientific = self.manager_stop
        led = self.ledger()["assessments"]
        lines = [f"# Closeout - {self.run_id}", "",
                 ("**Scientific stop directed by the Manager.**" if scientific else
                  "**This is an operational closeout, not a scientific completion.**"),
                 "", f"- Stop reason: {self.stop_reason or 'not recorded'}",
                 f"- Questions asked: {st['questions_asked']}; usable answers: {st['answers_usable']}; graded: "
                 f"{st['answers_graded']} in {st['rounds_committed']} round(s)",
                 "- By axis (asked / usable / graded): " + ("; ".join(
                     f"{a} {v['asked']} / {v['usable']} / {v['graded']}" for a, v in st.get("by_axis", {}).items())
                     or "one axis"),
                 f"- Elapsed: {st['elapsed_minutes']} minutes; graded per hour: {st['graded_per_hour']}",
                 f"- Provider failovers: {st['failovers']}; model calls: {st['model_calls']}; estimated cost: "
                 f"${st['estimated_usd']}",
                 "- Selected repair attempts used where flagged: " + (", ".join(selected) if selected else "none") + ".",
                 "", "FRD construction and source-only validation are separate later stages; nothing here certifies "
                 "source fidelity.", ""]
        if led:
            lines += ["## Last committed assessment", "", f"Round {led[-1]['assessment_id']}, committed "
                      f"{led[-1]['committed_at']}. The allocation is in the private ledger, not in this file.", ""]
        write_text(self.q / "CLOSEOUT.md", "\n".join(lines))
        try:
            from .scorecard import read_record, render, score
            sc = render(score(read_record(self.q)))
            write_text(self.q / "SCORECARD.txt", sc)
            self.log("scorecard: " + sc.splitlines()[0])
        except BaseException as e:  # noqa: BLE001 - a scorecard problem must not lose the closeout
            self.log(f"scorecard not written ({type(e).__name__}: {e})")
        self.log(f"closed: {self.stop_reason}. Next: python cr.py import-quest \"{self.project}\" \"{self.q}\" "
                 f"--closeout \"{self.q / 'CLOSEOUT.md'}\"" + (" --stop scientific" if scientific else ""))


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) < 2 or argv[0] != "run":
        print(__doc__)
        return 2
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    Relay(argv[1]).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
