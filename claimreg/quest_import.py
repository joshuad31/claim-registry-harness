"""Import a recorded NotebookLM quest into a run, so `cr run` continues at FRD generation.

A quest (docs/WALKTHROUGH.md steps 7-10) leaves one of two records. This module reads either:

* the recorder layout that `quest_tool.py` / `quest_io.py` write:
  ``<state>/recording/questions/Qnnnn.json`` and ``<state>/recording/captures/Qnnnn-Ann.json``;
* the driver layout alone, when questions were queued straight into the driver:
  ``<answers_dir>/Qnnnn-Ann.json``, with the questions in ``<answers_dir>/queue/``.

What it writes into the run (folder 02_DISCOVERY) is what the harness's own quest stage writes, so
every later stage runs unchanged:

* ``01_issued-questions/questions.json``, plus a Markdown copy of each question;
* ``02_query-responses/responses.json``, with **one selected attempt per question**, plus
  ``attempts.json``, which lists every attempt and why each one was or was not selected;
* ``05_feedback/``: the Manager's public feedback packets, if any;
* ``06_closeout/closeout.json``: an operational stop unless the caller says otherwise.

The Manager's private files (ACH_Eval fragments, the assessment ledger) are never imported. The
run's own ``assess`` stage makes the final assessment.

Choosing among re-asks (A01, A02, ...)
--------------------------------------
1. An explicit selection wins. It can come from ``--select Q0101-A03`` or from the closeout's
   "Selected repair attempts ..." line.
2. Otherwise the newest usable attempt that is not flagged for tool output is selected.
3. Otherwise the newest usable attempt is selected, and it keeps its flag.
4. Otherwise the question has no usable answer.

A selected answer flagged for NotebookLM tool output stays usable but is labelled
``evidence_status: CANDIDATE_UNVERIFIED``. FRD validation then checks every quotation word for word
against the real source file, which clears or rejects it. Pass ``exclude_tool_output=True`` to
drop such answers instead.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from .util import atomic_write_text, ensure_dir, read_json, read_text, sha256_file, utcnow, write_json

QID_ATT = re.compile(r"\b(Q\d{4})-(A\d{2})\b")
TOOL_OUTPUT = re.compile(r"Tool response for|exit_code:|Tool call:default_api")
THOUGHTS = re.compile(r"^\s*Thoughts\s*\n(?:[\s\S]*?\n)?\s*expand_(?:more|less)\s*\n")
MIN_ANSWER_CHARS = 400   # same floor as quest_tool.py ingest


class QuestImportError(RuntimeError):
    pass


# --------------------------------------------------------------------------- #
# locating the record
# --------------------------------------------------------------------------- #

def _first_dir(root: Path, name: str, must_contain: str | None = None) -> Path | None:
    cands = [root] if root.name == name else []
    cands += sorted(p for p in root.rglob(name) if p.is_dir())
    for p in cands:
        if must_contain is None or (p / must_contain).is_dir():
            return p
    return None


def find_layout(src: Path) -> dict:
    """Work out which record `src` holds. `src` may be the quest folder, its state folder, the
    recording folder itself, or a driver answers folder."""
    src = Path(src)
    if not src.is_dir():
        raise QuestImportError(f"quest folder not found: {src}")
    rec = _first_dir(src, "recording", must_contain="captures")
    if rec is not None:
        layout = {"mode": "recorder", "recording": rec, "root": src}
    else:
        answers = [p for p in src.rglob("Q*-A*.json") if "queue" not in p.parts]
        if not answers:
            raise QuestImportError(
                f"no quest record in {src}: expected recording/captures/ (quest_tool) or "
                f"Qnnnn-Ann.json answer files (driver)")
        layout = {"mode": "driver", "answers": sorted({p.parent for p in answers})[0], "root": src}
    layout["packets"] = _first_dir(src, "feedback-packets") or _first_dir(src, "packets")
    flags = sorted(src.rglob("capture-flags.json"))
    layout["flags"] = flags[0] if flags else None
    return layout


# --------------------------------------------------------------------------- #
# reading attempts
# --------------------------------------------------------------------------- #

def _flagged_in_file(flags_path: Path | None) -> set[tuple[str, str]]:
    if not flags_path:
        return set()
    d = read_json(flags_path, default={}) or {}
    out = set()
    for f in d.get("flags", []) if isinstance(d, dict) else []:
        if "TOOL_OUTPUT" in str(f.get("flag", "")).upper():
            out.add((f.get("qid", ""), f.get("attempt", "A01")))
    return out


def _attempt(qid, att, query, answer, outcome, meta, source_file, flagged_file) -> dict:
    answer = THOUGHTS.sub("", answer or "")
    tool_only = bool(re.match(r"\s*Tool call:", answer)) and len(answer) < 3000
    if tool_only:
        outcome = "FAILED"
    on_target = meta.get("answer_names_requested_source", True) is not False
    if not on_target:
        # older lane runners missed citations under a truncated filename: accept a 30-char stem prefix
        wanted = re.findall(r"[\w@().,\-]+\.(?:pdf\.md|md|txt)", query or "")
        on_target = any(re.sub(r"(\.pdf)?\.(md|txt)$", "", w)[:30] in answer for w in wanted)
    tool_output = bool(meta.get("contains_tool_output")) or bool(TOOL_OUTPUT.search(answer)) \
        or (qid, att) in flagged_file
    recorded_usable = meta.get("usable")
    usable = (outcome in ("COMPLETE", "INCOMPLETE") and len(answer.strip()) >= MIN_ANSWER_CHARS
              and on_target and recorded_usable is not False)
    return {"qid": qid, "attempt": att, "query": query, "answer": answer, "outcome": outcome,
            "usable": usable, "contains_tool_output": tool_output, "on_target": on_target,
            "lane": meta.get("lane", ""), "notebook_url": meta.get("notebook_url", ""),
            "submitted_at": meta.get("submitted_at", ""), "captured_at": meta.get("captured_at", ""),
            "generation_seconds": meta.get("generation_seconds"),
            "recorded_cited": [c.get("source_voice", "") if isinstance(c, dict) else str(c)
                               for c in meta.get("cited_sources", []) or []],
            "source_file": str(source_file)}


def load_record(layout: dict) -> tuple[dict, dict]:
    """Return (questions by qid, attempts by qid) in one normalised shape for both layouts."""
    flagged = _flagged_in_file(layout.get("flags"))
    questions: dict[str, dict] = {}
    attempts: dict[str, list[dict]] = {}
    if layout["mode"] == "recorder":
        rec = layout["recording"]
        for p in sorted((rec / "questions").glob("Q*.json")):
            q = read_json(p)
            m = q.get("metadata", {}) or {}
            questions[q["qid"]] = {
                "qid": q["qid"], "run_id": q.get("run_id", ""), "text": q.get("query", ""),
                "sources_as_sent": q.get("source_voices", []) or [],
                "round": m.get("round_number"), "order_in_round": m.get("order_in_round"),
                "target": m.get("target_ledger_row_or_test", ""),
                "packet_priority_id": m.get("packet_priority_id"),
                "header_version": m.get("header_version", ""), "issued": q.get("reserved_at", ""),
                "source_file": str(p)}
        for p in sorted((rec / "captures").glob("Q*-A*.json")):
            c = read_json(p)
            meta = dict(c.get("metadata", {}) or {})
            for k in ("notebook_url", "submitted_at", "captured_at"):
                meta.setdefault(k, c.get(k, ""))
            attempts.setdefault(c["qid"], []).append(_attempt(
                c["qid"], c.get("attempt", "A01"), c.get("query", ""), c.get("answer", ""),
                c.get("outcome", "UNKNOWN"), meta, p, flagged))
    else:
        ans = layout["answers"]
        queue = ans / "queue"
        for p in sorted(ans.glob("Q*-A*.json")):
            a = read_json(p)
            qid = a.get("qid") or QID_ATT.search(p.name).group(1)
            att = a.get("attempt") or QID_ATT.search(p.name).group(2)
            meta = {k: a.get(k) for k in ("lane", "notebook_url", "submitted_at", "captured_at",
                                          "generation_seconds", "contains_tool_output",
                                          "answer_names_requested_source") if k in a}
            if a.get("query_seen_in_user_message") is False:
                meta["usable"] = False
            attempts.setdefault(qid, []).append(_attempt(
                qid, att, a.get("query", ""), a.get("answer", ""), a.get("outcome", "UNKNOWN"),
                meta, p, flagged))
            if qid not in questions:
                qf = queue / f"{qid}.json"
                qtext = (read_json(qf, default={}) or {}).get("text") if qf.exists() else None
                questions[qid] = {"qid": qid, "run_id": a.get("run_id", ""),
                                  "text": qtext or a.get("query", ""), "sources_as_sent": [],
                                  "round": None, "order_in_round": None, "target": "",
                                  "packet_priority_id": None, "header_version": "",
                                  "issued": a.get("submitted_at", ""),
                                  "source_file": str(qf if qf.exists() else p)}
    for qid, atts in attempts.items():
        atts.sort(key=lambda x: x["attempt"])
        questions.setdefault(qid, {"qid": qid, "run_id": "", "text": atts[0]["query"],
                                   "sources_as_sent": [], "round": None, "order_in_round": None,
                                   "target": "", "packet_priority_id": None, "header_version": "",
                                   "issued": atts[0]["submitted_at"], "source_file": ""})
    return questions, attempts


# --------------------------------------------------------------------------- #
# choosing one attempt per question
# --------------------------------------------------------------------------- #

def parse_closeout_selections(text: str) -> dict[str, str]:
    """QID -> attempt from the closeout's 'Selected repair attempts ...' sentence, if present."""
    m = re.search(r"Selected repair attempts[^:\n]*:([^\n]*)", text or "", re.I)
    return {q: a for q, a in QID_ATT.findall(m.group(1))} if m else {}


def select_attempt(atts: list[dict], override: str | None = None) -> tuple[dict | None, str]:
    if override:
        for a in atts:
            if a["attempt"] == override:
                return a, f"selected explicitly ({override})"
    newest_first = sorted(atts, key=lambda a: a["attempt"], reverse=True)
    for a in newest_first:
        if a["usable"] and not a["contains_tool_output"]:
            return a, "newest usable attempt without tool output"
    for a in newest_first:
        if a["usable"]:
            return a, "newest usable attempt; every usable attempt carries tool output"
    return (newest_first[0] if newest_first else None), "no usable attempt"


# --------------------------------------------------------------------------- #
# the import
# --------------------------------------------------------------------------- #

def import_quest(project_dir: Path, quest_dir: Path, run_id: str | None = None,
                 closeout: Path | None = None, select: list[str] | None = None,
                 stop: str = "operational", exclude_tool_output: bool = False,
                 force: bool = False) -> dict:
    from .pipeline import run_pipeline
    from .quest import cited_sources
    from .runctx import RunContext, new_run_id
    from .config import load_config

    if stop not in ("operational", "scientific"):
        raise QuestImportError("--stop must be 'operational' or 'scientific'")
    project_dir = Path(project_dir)
    if not (project_dir / "01_FRAME" / "header.md").exists():
        raise QuestImportError(f"{project_dir} has no 01_FRAME/header.md. Create the project with "
                               f"`cr init` (corpus, header, index) before importing a quest.")
    layout = find_layout(Path(quest_dir))
    questions, attempts = load_record(layout)
    if not attempts:
        raise QuestImportError(f"the quest record in {quest_dir} holds no answers")

    overrides: dict[str, str] = {}
    closeout_text = read_text(closeout) if closeout else ""
    overrides.update(parse_closeout_selections(closeout_text))
    for s in select or []:
        m = QID_ATT.fullmatch(s.strip())
        if not m:
            raise QuestImportError(f"--select expects QID-ATTEMPT such as Q0101-A03, not {s!r}")
        overrides[m.group(1)] = m.group(2)

    if run_id is None:
        run_id = new_run_id(load_config(project_dir)["project"].get("run_prefix", "RUN") + "-QUEST")
    ctx = RunContext(project_dir, run_id, create=True)
    prev = ctx.stage_state().get("quest", {}).get("status")
    if prev in ("done", "imported") and not force:
        raise QuestImportError(f"run {run_id} already has a {prev} quest; pick another --run or use --force")

    # corpus, index, Archivist prompt and frame run exactly as in `cr run`
    pre = run_pipeline(ctx, stop="frame")
    if pre.get("status") not in ("complete", "done"):
        st = ctx.stage_state()
        if any(st.get(s, {}).get("status") not in ("done", "imported")
               for s in ("corpus", "index", "archivist_prompt", "frame")):
            raise QuestImportError(f"the stages before the quest did not finish ({pre.get('status')}); "
                                   f"run `cr run {project_dir} --run {run_id} --to frame` and fix what it reports")
    corpus = ctx.corpus

    d = ctx.p("discovery")
    for sub in ("01_issued-questions", "02_query-responses", "03_quest-state", "05_feedback", "06_closeout"):
        ensure_dir(d / sub)

    q_out, r_out, a_out = [], [], []
    for qid in sorted(set(questions) | set(attempts)):
        q = questions[qid]
        atts = attempts.get(qid, [])
        voices = q["sources_as_sent"] or cited_sources(q["text"], corpus)
        resolved = {v: (corpus.resolve(v) or "UNRESOLVED_NAME") for v in voices}
        chosen, reason = select_attempt(atts, overrides.get(qid))
        usable = bool(chosen and chosen["usable"])
        if usable and exclude_tool_output and chosen["contains_tool_output"]:
            usable, reason = False, reason + "; excluded because it carries tool output"
        if chosen and chosen["usable"] is False and overrides.get(qid) == chosen["attempt"]:
            reason += " (that attempt is not usable)"
        for a in atts:
            a_out.append({k: v for k, v in a.items() if k != "answer"} | {
                "selected": chosen is not None and a["attempt"] == chosen["attempt"],
                "answer_chars": len(a["answer"])})
        status = "UNANSWERED" if not atts else ("ANSWERED" if usable else "UNUSABLE")
        rid = f"R-{qid}-{chosen['attempt']}" if chosen else ""
        q_out.append({
            "qid": qid, "run_id": q["run_id"], "round": q["round"], "order_in_round": q["order_in_round"],
            "text": q["text"],
            "firewall": {"status": "IMPORTED", "repairs": [], "original_text": q["text"]},
            "sources_as_sent": voices, "sources_resolved": resolved, "target": q["target"],
            "packet_priority_id": q["packet_priority_id"], "header_version": q["header_version"],
            "issued": q["issued"], "status": status, "response_ids": [rid] if rid else [],
            "attempts": [a["attempt"] for a in atts], "frd_ids": [], "witness_ids": [],
            "notebook_lane": chosen["lane"] if chosen else "", "imported_from": q["source_file"]})
        atomic_write_text(d / "01_issued-questions" / f"{qid}__issued-question.md",
                          f"# {qid}\n\nSources as sent: {json.dumps(voices)}\n\nTarget: {q['target']}\n\n"
                          f"## Exact query\n\n```text\n{q['text']}\n```\n")
        if not chosen:
            continue
        cites = []
        for c in chosen["recorded_cited"] + cited_sources(chosen["answer"], corpus):
            r = corpus.resolve(c)
            if r and r not in cites:
                cites.append(r)
        req = [s for s in resolved.values() if s != "UNRESOLVED_NAME"]
        r_out.append({
            "response_id": rid, "qid": qid, "attempt": chosen["attempt"], "outcome": chosen["outcome"],
            "usable": usable, "text": chosen["answer"], "cited_sources": cites,
            "requested_sources_cited": [s for s in req if s in cites],
            "requested_sources_absent": [s for s in req if s not in cites],
            "contains_tool_output": chosen["contains_tool_output"],
            "evidence_status": "CANDIDATE_UNVERIFIED" if chosen["contains_tool_output"] else "RETRIEVED",
            "selection": reason, "other_attempts": [a["attempt"] for a in atts if a is not chosen],
            "retrieval": {"system": "NotebookLM", "notebook": chosen["notebook_url"], "lane": chosen["lane"]},
            "model": "NotebookLM", "captured": chosen["captured_at"], "submitted": chosen["submitted_at"],
            "generation_seconds": chosen["generation_seconds"], "imported_from": chosen["source_file"]})
        atomic_write_text(d / "02_query-responses" / f"{qid}__query-response.md",
                          f"# {rid}\n\nOutcome: {chosen['outcome']}\n\nUsable: {usable}\n\n"
                          f"Evidence status: {r_out[-1]['evidence_status']}\n\nSelection: {reason}\n\n"
                          f"Notebook: {chosen['notebook_url']} (lane {chosen['lane']})\n\n"
                          f"Captured: {chosen['captured_at']}\n\n## Exact query\n\n```text\n{chosen['query']}\n```\n\n"
                          f"## Exact answer\n\n```text\n{chosen['answer']}\n```\n")

    write_json(d / "01_issued-questions" / "questions.json", q_out)
    write_json(d / "02_query-responses" / "responses.json", r_out)
    write_json(d / "02_query-responses" / "attempts.json", a_out)

    packets = []
    if layout.get("packets"):
        for pf in sorted(layout["packets"].glob("*.md")):
            dst = d / "05_feedback" / (f"{pf.stem}-packet.md" if re.fullmatch(r"R\d+", pf.stem) else pf.name)
            shutil.copyfile(pf, dst)
            packets.append(pf.name)
    if layout.get("flags"):
        shutil.copyfile(layout["flags"], d / "03_quest-state" / "capture-flags-imported.json")

    rounds = sorted({q["round"] for q in q_out if q["round"]})
    n_usable = sum(1 for r in r_out if r["usable"])
    n_candidate = sum(1 for r in r_out if r["usable"] and r["evidence_status"] == "CANDIDATE_UNVERIFIED")
    write_json(d / "03_quest-state" / "state.json",
               {"status": "imported", "round": max(rounds) if rounds else 0, "phase": "done"})
    write_json(d / "03_quest-state" / "import-record.json", {
        "imported": utcnow(), "from": str(Path(quest_dir).resolve()), "layout": layout["mode"],
        "closeout": str(closeout) if closeout else None,
        "selection_overrides": overrides, "exclude_tool_output": exclude_tool_output,
        "files": {str(Path(a["source_file"]).name): sha256_file(a["source_file"])
                  for a in a_out if a.get("source_file") and Path(a["source_file"]).exists()}})

    stop_label = "SCIENTIFIC_STOP (imported)" if stop == "scientific" else "OPERATIONAL_STOP (imported)"
    if closeout:
        shutil.copyfile(closeout, d / "06_closeout" / Path(closeout).name)
    closeout_rec = {
        "status": stop_label, "rounds": len(rounds), "questions_issued": len(q_out),
        "usable_answers": n_usable, "candidate_answers_tool_output": n_candidate,
        "note": ("Imported NotebookLM quest. The stop type was declared by the person importing it "
                 f"(--stop {stop}); the Manager's private ACH_Eval files are not part of this import, "
                 "and the run's own assess stage makes the final assessment."),
        "closeout_document": Path(closeout).name if closeout else None, "closed": utcnow()}
    write_json(d / "06_closeout" / "closeout.json", closeout_rec)

    summary = {"questions": len(q_out), "usable": n_usable, "candidates_tool_output": n_candidate,
               "attempts": len(a_out), "repairs_selected": {q: a for q, a in overrides.items()},
               "packets": len(packets), "layout": layout["mode"], "stop": stop_label,
               "source": str(Path(quest_dir).resolve())}
    ctx.set_stage("quest", "imported", summary)
    try:
        from .pipeline import write_navigation
        write_navigation(ctx)
    except Exception:
        pass
    return {"run_id": run_id, **summary,
            "next": f"cr run {project_dir} --run {run_id}   (continues at frd_generate)"}
