"""Phase II - the Coordinator-led discovery quest (spec modules 10-15).

Roles and information boundaries
--------------------------------
* Investigator - sees the frozen header, the ranked index, its own ledger, the
  saved answers and the feedback packet; writes 1-3-source questions.
* Firewall     - deterministic: strips hypothesis labels, enforces 1-3 named
  sources, records every repair.  The Archivist never sees the header.
* Archivist    - the project's custom instructions + passages retrieved from
  the local corpus database (named sources first) + one question.
* Coordinator  - runs ACH_Eval (verbatim) once per round on the cumulative
  fragment and the round's new records; returns allocations and the feedback
  packet.  The harness applies the gauge-keyed stop rule to the allocations.

The loop is a resumable state machine (investigate -> ask -> assess); every
model call is cached, so an interrupted or queued run continues exactly where
it stopped.
"""

from __future__ import annotations

import re
from statistics import mean

from .header import HYPOTHESIS_LABEL_RE
from .index import _FILE, compact_index, parse_index
from .llm.base import LLMRequest
from .llm.jsonparse import JSONExtractError, as_list, extract_json
from .util import read_text, truncate_words, utcnow, word_count, write_json, atomic_write_text

STOP_TABLE = [  # (max gauge, branch1 mean over 3 rounds, branch2 mean over 4 rounds)
    (60, 0.0, 0.5),
    (64, 0.334, 0.75),
    (76, 0.667, 1.2),
    (100, 1.0, 1.2),
]

JARGON = re.compile(r"\b(ACH|FRDs?|crux(?:es)?|allocation|unit vector)\b", re.I)


def stop_thresholds(gauge: int) -> tuple[float, float]:
    row = STOP_TABLE[0]
    for g, t1, t2 in STOP_TABLE:
        if gauge >= g:
            row = (g, t1, t2)
    return row[1], row[2]


def delta_units(prev: dict, cur: dict) -> float:
    """x = half the sum of absolute per-hypothesis unit changes on one axis."""
    keys = set(prev) | set(cur)
    return 0.5 * sum(abs(int(cur.get(k, 0)) - int(prev.get(k, 0))) for k in keys)


def evaluate_stop(history: list[dict], gauge: int, axes: list[str], ab_covered: bool,
                  substantive_ok: bool) -> dict:
    """Apply the gauge-keyed stop rule (header template v2, 'The stop-rule table').

    ``history`` is the per-round list of {"round": r, "allocations": {axis: {hid: n}}}.
    Round 1 has no prior comparable assessment; its delta is undefined (never zero).
    """
    t1, t2 = stop_thresholds(gauge)
    per_axis = {}
    all_ok = True
    for ax in axes:
        xs = []
        for i in range(1, len(history)):
            a0 = history[i - 1]["allocations"].get(ax)
            a1 = history[i]["allocations"].get(ax)
            if a0 and a1:
                xs.append(delta_units(a0, a1))
        b1 = len(xs) >= 3 and mean(xs[-3:]) <= t1 + 1e-9
        b2 = ab_covered and len(xs) >= 4 and mean(xs[-4:]) <= t2 + 1e-9
        per_axis[ax] = {"deltas": xs, "branch1": b1, "branch2": b2,
                        "mean3": round(mean(xs[-3:]), 3) if len(xs) >= 3 else None,
                        "mean4": round(mean(xs[-4:]), 3) if len(xs) >= 4 else None}
        all_ok = all_ok and (b1 or b2)
    return {"gauge": gauge, "thresholds": {"branch1_mean3": t1, "branch2_mean4": t2},
            "axes": per_axis, "numeric_rule_met": all_ok,
            "substantive_conditions_met": substantive_ok, "ab_covered": ab_covered,
            "stop": all_ok and substantive_ok}


# --------------------------------------------------------------------------- #
# firewall
# --------------------------------------------------------------------------- #

def firewall(q: dict, corpus) -> dict:
    """Return a firewall record and the text to send.  Never invents a source."""
    text = (q.get("text") or "").strip()
    original = text
    repairs = []
    if HYPOTHESIS_LABEL_RE.search(text):
        text = HYPOTHESIS_LABEL_RE.sub("", text)
        text = re.sub(r"\s{2,}", " ", text).strip()
        repairs.append("removed hypothesis identifiers")
    if JARGON.search(text):
        text = JARGON.sub("", text)
        text = re.sub(r"\s{2,}", " ", text).strip()
        repairs.append("removed internal pipeline jargon")
    names = [s for s in (q.get("sources") or []) if isinstance(s, str) and s.strip()]
    if not names:
        names = [m.strip() for m in _FILE.findall(text)]
    names = list(dict.fromkeys(names))
    if len(names) > 3:
        repairs.append(f"trimmed named sources from {len(names)} to 3")
        names = names[:3]
    resolved = {n: (corpus.resolve(n) or "UNRESOLVED_NAME") for n in names}
    status = "PASS" if not repairs else "REPAIRED"
    if not names:
        status = "REJECTED"
        repairs.append("no source named: the firewall never sends a source-agnostic question")
    else:
        missing_in_text = [n for n, r in resolved.items()
                           if r != "UNRESOLVED_NAME" and r.lower() not in text.lower()
                           and n.lower() not in text.lower()]
        if missing_in_text:
            text = text.rstrip() + " Sources: " + ", ".join(resolved[n] for n in missing_in_text) + "."
            repairs.append("appended named sources to the question text")
            status = "REPAIRED"
    return {"status": status, "repairs": repairs, "original_text": original, "text": text,
            "sources_as_sent": names, "sources_resolved": resolved}


# --------------------------------------------------------------------------- #
# archivist retrieval
# --------------------------------------------------------------------------- #

def archivist_passages(corpus, question: str, sources: list[str], qcfg: dict) -> tuple[str, dict]:
    budget = int(qcfg.get("archivist_context_words", 9000))
    per = int(qcfg.get("named_source_words", 4500))
    k_other = int(qcfg.get("other_chunks", 6))
    blocks, rec = [], {"named": [], "other": [], "unresolved": []}
    used = 0
    good = [s for s in sources if s and s != "UNRESOLVED_NAME"]
    if good:
        per = max(800, min(per, budget // max(1, len(good))))
    for s in sources:
        if s == "UNRESOLVED_NAME" or not s:
            continue
        ex = corpus.excerpt(s, question, per)
        used += ex["words"]
        head = (f"=== SOURCE: {ex['filename']} (requested; "
                f"{'complete text' if ex['complete'] else 'retrieved passages'}) ===")
        outline_txt = "; ".join(x.strip() for x in ex["outline"][:40])
        blocks.append(f"{head}\nHeadings: {outline_txt}\n\n{ex['text']}")
        rec["named"].append({"filename": ex["filename"], "complete": ex["complete"],
                             "words": ex["words"]})
    if k_other > 0:
        for score, ch in corpus.search(question, k=k_other * 3, exclude=set(good)):
            if len(rec["other"]) >= k_other:
                break
            w = word_count(ch.text)
            if used + w > budget * 1.25:
                break
            used += w
            blocks.append(f"=== SOURCE: {ch.filename} (other notebook source; retrieved passage) | "
                          f"section: {ch.heading} ===\n{ch.text}")
            rec["other"].append({"filename": ch.filename, "heading": ch.heading,
                                 "score": round(score, 2)})
    if not blocks:
        blocks.append("(No passages were retrieved for this question.)")
    rec["words"] = used
    return "\n\n".join(blocks), rec


def cited_sources(text: str, corpus) -> list[str]:
    out = []
    for m in _FILE.findall(text or ""):
        r = corpus.resolve(m.strip(" ([<`'\""))
        if r and r not in out:
            out.append(r)
    return out


# --------------------------------------------------------------------------- #
# coverage
# --------------------------------------------------------------------------- #

def coverage_ledger(questions: list[dict], responses: dict, ranks: dict) -> dict:
    named_ok: dict[str, int] = {}
    cited: dict[str, int] = {}
    for q in questions:
        r = responses.get(q["qid"])
        if not r or not r.get("usable"):
            continue
        for s in q.get("sources_resolved", {}).values():
            if s != "UNRESOLVED_NAME":
                named_ok[s] = named_ok.get(s, 0) + 1
        for s in r.get("cited_sources", []):
            cited[s] = cited.get(s, 0) + 1
    rows = {}
    for fn, rk in ranks.items():
        n = named_ok.get(fn, 0)
        c = cited.get(fn, 0)
        status = "NOT_QUERIED"
        if n:
            status = "QUERIED"
            if c == 0 and n >= 2:
                status = "SOURCE_UNRESPONSIVE"
        rows[fn] = {"rank": rk, "named_in_usable": n, "cited": c, "status": status}
    ab = [fn for fn, r in rows.items() if r["rank"] in ("A", "B")]
    ab_done = all(rows[fn]["status"] != "NOT_QUERIED" for fn in ab) if ab else True
    return {"sources": rows, "ab_total": len(ab),
            "ab_queried": sum(1 for fn in ab if rows[fn]["status"] != "NOT_QUERIED"),
            "ab_covered": ab_done}


def coverage_text(cov: dict, max_rows: int = 200) -> str:
    rows = sorted(cov["sources"].items(), key=lambda kv: ({"A": 0, "B": 1}.get(kv[1]["rank"], 2), kv[0]))
    lines = [f"A+B priority sources queried: {cov['ab_queried']} of {cov['ab_total']}"]
    for fn, r in rows[:max_rows]:
        if r["rank"] in ("A", "B") or r["named_in_usable"]:
            lines.append(f"[{r['rank']}] {fn}: {r['status']} (named {r['named_in_usable']}, cited {r['cited']})")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# packet rendering (allocation-free by construction)
# --------------------------------------------------------------------------- #

_FORBIDDEN_PACKET = re.compile(r"(\b\d+\s*/\s*\d+\s*units?\b|\bunits?\b\s*[:=]|\ballocat\w*|"
                               r"\bleader\b|\bleading hypothesis\b|\bconfidence\b|\bvector\b)", re.I)


def render_packet(rnd: int, qids: list[str], direction: str, pk: dict) -> str:
    lines = [f"# Feedback packet R{rnd:03d}", "",
             f"Assessed QIDs: {', '.join(qids) or 'none'}", f"Direction: **{direction}**",
             f"Expected return from further work: {pk.get('expected_return', 'cannot judge')}",
             f"Posture: {pk.get('posture', 'cannot judge')}", ""]
    pri = pk.get("priorities") or []
    if pri:
        lines.append("## Acquisition priorities")
        for p in pri[:3]:
            if not isinstance(p, dict):
                continue
            lines += [f"- **{p.get('id', '')}** - {p.get('finding_or_gap', '')}",
                      f"  - missing: {p.get('missing_material', '')}",
                      f"  - suggested question: {p.get('question', '')}",
                      f"  - sources: {', '.join(p.get('sources') or [])}",
                      f"  - success criterion: {p.get('success_criterion', '')}",
                      f"  - affects: {p.get('affects', '')}"]
    qp = pk.get("quarantine_priority") or {}
    if isinstance(qp, dict) and qp.get("issue"):
        lines += ["", "## Quarantine priority", f"- {qp.get('issue')}",
                  f"  - question: {qp.get('question', '')}",
                  f"  - sources: {', '.join(qp.get('sources') or [])}"]
    lines += ["", "## Novelty", f"- substantial: {pk.get('substantial_novelty', '')}",
              f"- trivial: {pk.get('trivial_novelty', '')}"]
    gaps = pk.get("open_gaps_and_corrections") or []
    if gaps:
        lines += ["", "## Open gaps, conflicts and corrections"] + [f"- {g}" for g in gaps]
    rep = pk.get("answers_needing_repair") or []
    if rep:
        lines += ["", "## Answers needing repair"] + [f"- {g}" for g in rep]
    lines += ["", f"Holds: {pk.get('holds', 'none')}"]
    text = "\n".join(lines)
    # defence in depth: the packet must never carry the allocation record
    cleaned = []
    for ln in text.splitlines():
        cleaned.append("[line withheld: assessment-internal content]" if _FORBIDDEN_PACKET.search(ln) else ln)
    return "\n".join(cleaned)


# --------------------------------------------------------------------------- #
# coordinator output parsing
# --------------------------------------------------------------------------- #

def parse_coordinator(text: str, frame: dict, gauge: int) -> dict:
    blocks = re.findall(r"```json\s*\n(.*?)\n?```", text or "", re.S)
    data = None
    for b in reversed(blocks):
        try:
            data = extract_json(b)
            if isinstance(data, dict) and "allocations" in data:
                break
        except JSONExtractError:
            continue
    if not isinstance(data, dict):
        try:
            data = extract_json(text)
        except JSONExtractError:
            data = {}
    alloc = data.get("allocations") or {}
    problems = []
    clean = {}
    for ax in frame["axes"]:
        a = ax["axis_id"]
        got = alloc.get(a) or {}
        ids = [h["id"] for h in ax["hypotheses"]]
        vec = {}
        for hid in ids:
            v = got.get(hid)
            try:
                vec[hid] = int(v)
            except (TypeError, ValueError):
                vec[hid] = None
        if any(v is None for v in vec.values()):
            problems.append(f"axis {a}: missing units for {[k for k, v in vec.items() if v is None]}")
            continue
        if sum(vec.values()) != gauge:
            problems.append(f"axis {a}: units sum to {sum(vec.values())}, not G={gauge}")
        clean[a] = vec
    sc = data.get("substantive_conditions") or {}
    sub_ok = bool(sc) and all(bool(sc.get(k)) for k in (
        "decisive_tests_oriented", "every_live_hypothesis_adversely_tested",
        "weakest_and_shared_links_tested", "project_success_conditions_addressed"))
    return {"allocations": clean, "problems": problems, "direction": data.get("direction", "CONTINUE"),
            "packet": data.get("feedback_packet") or {}, "substantive": sc,
            "substantive_ok": sub_ok, "basis_confidence": data.get("basis_confidence", {})}


# --------------------------------------------------------------------------- #
# the loop
# --------------------------------------------------------------------------- #

def _qrecords_text(qs: list[dict], responses: dict, max_words: int = 1600) -> str:
    out = []
    for q in qs:
        r = responses.get(q["qid"], {})
        out.append(f"--- {q['qid']} (round {q['round']}) sources: {', '.join(q['sources_as_sent'])}\n"
                   f"QUESTION: {q['text']}\n"
                   f"ANSWER ({'usable' if r.get('usable') else 'NOT USABLE'}; cited: "
                   f"{', '.join(r.get('cited_sources', [])) or 'none'}):\n"
                   f"{truncate_words(r.get('text', ''), max_words)}")
    return "\n\n".join(out) if out else "(none)"


def run_quest(ctx) -> dict:
    qcfg = ctx.cfg["quest"]
    d = ctx.p("discovery")
    state_path = d / "03_quest-state" / "state.json"
    from .util import read_json
    state = read_json(state_path, default=None) or {
        "round": 1, "phase": "investigate", "status": "running", "history": [],
        "next_qid": 1, "created": utcnow()}
    if state.get("status") in ("stopped", "imported"):
        return {"status": state["status"], "rounds": state.get("round"),
                "questions": len(read_json(d / "01_issued-questions" / "questions.json", default=[]))}
    questions: list[dict] = read_json(d / "01_issued-questions" / "questions.json", default=[]) or []
    responses: dict = {r["qid"]: r for r in (read_json(d / "02_query-responses" / "responses.json",
                                                         default=[]) or [])}
    frame = ctx.frame
    gauge = int(frame.get("gauge") or qcfg.get("gauge", 64))
    header = read_text(ctx.p("frame", "header.md"))
    idx_path = ctx.p("frame", "index.md")
    index_text = read_text(idx_path) if idx_path.exists() else ""
    parsed_idx = parse_index(index_text, ctx.corpus)
    ranks = parsed_idx["ranks"]
    index_for_prompt = (index_text if word_count(index_text) <= int(qcfg.get("full_index_max_words", 6000))
                        else compact_index(parsed_idx, ctx.corpus))
    arch_instr = ctx.archivist_instructions()
    axes = [a["axis_id"] for a in frame["axes"]]
    n_q = int(qcfg.get("round_size", 5))
    max_rounds = int(qcfg.get("max_rounds", 12))

    def save_all():
        write_json(d / "01_issued-questions" / "questions.json", questions)
        write_json(d / "02_query-responses" / "responses.json", list(responses.values()))
        write_json(state_path, state)

    while state["status"] == "running":
        rnd = state["round"]
        if state["phase"] == "investigate":
            prev_round_qs = [q for q in questions if q["round"] == rnd - 1]
            ledger_prev = d / "03_quest-state" / f"ledger-R{rnd - 1:03d}.md"
            packet_prev = d / "05_feedback" / f"R{rnd - 1:03d}-packet.md"
            cov = coverage_ledger(questions, responses, ranks)
            issued = "\n".join(f"{q['qid']} [{', '.join(q['sources_as_sent'])}] {truncate_words(q['text'], 30)}"
                               for q in questions) or "(none yet)"
            system, user, _ = ctx.prompts.render(
                "investigator.md", HEADER=header, RUN_ID=ctx.run_id, ROUND=rnd, N_QUESTIONS=n_q,
                INDEX=index_for_prompt, COVERAGE=coverage_text(cov), ISSUED=issued,
                LEDGER=read_text(ledger_prev) if ledger_prev.exists() else "(empty: first round)",
                NEW_ANSWERS=_qrecords_text(prev_round_qs, responses),
                PACKET=read_text(packet_prev) if packet_prev.exists() else "(no packet yet: first round)")
            resp = ctx.llm.call(LLMRequest(role="investigator", system=system, user=user,
                                           tag=f"investigate:R{rnd:03d}",
                                           meta={"round": rnd, "n": n_q,
                                                 "sources": list(ranks) or ctx.corpus.filenames}))
            data = resp.parsed if isinstance(resp.parsed, dict) else {}
            qs = as_list(data.get("questions") if data else resp.parsed, "questions")
            atomic_write_text(d / "03_quest-state" / f"ledger-R{rnd:03d}.md",
                              str(data.get("ledger") or "(no ledger returned)"))
            write_json(d / "03_quest-state" / f"round-record-R{rnd:03d}.json",
                       {"round": rnd, "round_record": data.get("round_record", {}),
                        "call_key": resp.key, "packet_used": packet_prev.name if packet_prev.exists() else None})
            for order, q in enumerate(qs[:n_q], 1):
                if not isinstance(q, dict):
                    continue
                fw = firewall(q, ctx.corpus)
                qid = f"Q{state['next_qid']:04d}"
                state["next_qid"] += 1
                rec = {"qid": qid, "run_id": ctx.run_id, "round": rnd, "order_in_round": order,
                       "text": fw["text"], "firewall": {k: fw[k] for k in ("status", "repairs", "original_text")},
                       "sources_as_sent": fw["sources_as_sent"], "sources_resolved": fw["sources_resolved"],
                       "target": q.get("target", ""), "packet_priority_id": q.get("packet_priority_id"),
                       "rationale": q.get("rationale", ""), "header_version": frame.get("header_sha256", "")[:16],
                       "issued": utcnow(), "status": "REJECTED" if fw["status"] == "REJECTED" else "ISSUED",
                       "response_ids": [], "frd_ids": [], "witness_ids": []}
                questions.append(rec)
                atomic_write_text(d / "01_issued-questions" / f"{qid}__issued-question.md",
                                  f"# {qid}\n\nRound {rnd}, order {order}. Firewall: {fw['status']} "
                                  f"{'; '.join(fw['repairs'])}\n\nSources as sent: {', '.join(fw['sources_as_sent'])}\n\n"
                                  f"## Exact question\n\n{fw['text']}\n")
            state["phase"] = "ask"
            save_all()
            ctx.log(f"quest R{rnd}: issued {len([q for q in questions if q['round'] == rnd])} questions")

        if state["phase"] == "ask":
            open_qs = [q for q in questions if q["round"] == rnd and q["status"] == "ISSUED"
                       and q["qid"] not in responses]
            reqs = []
            for q in open_qs:
                srcs = [v for v in q["sources_resolved"].values()]
                passages, rrec = archivist_passages(ctx.corpus, q["text"], srcs, qcfg)
                system, user, _ = ctx.prompts.render("archivist.md", ARCHIVIST_INSTRUCTIONS=arch_instr,
                                                     PASSAGES=passages, QUESTION=q["text"])
                reqs.append((q, rrec, LLMRequest(role="archivist", system=system, user=user,
                                                 expect_json=False, tag=f"archivist:{q['qid']}",
                                                 meta={"qid": q["qid"], "sources": srcs})))
            results = ctx.llm.call_many([r for _, _, r in reqs])
            for (q, rrec, req), res in zip(reqs, results):
                text = (res.text if res else "") or ""
                cites = cited_sources(text, ctx.corpus)
                requested = [s for s in q["sources_resolved"].values() if s != "UNRESOLVED_NAME"]
                usable = word_count(text) >= 40 and bool(cites) and not (res and res.parse_error)
                rid = f"R-{q['qid']}-A01"
                responses[q["qid"]] = {
                    "response_id": rid, "qid": q["qid"], "attempt": "A01",
                    "outcome": "COMPLETE" if text.strip() else "EMPTY", "usable": usable,
                    "text": text, "cited_sources": cites,
                    "requested_sources_cited": [s for s in requested if s in cites],
                    "requested_sources_absent": [s for s in requested if s not in cites],
                    "retrieval": rrec, "call_key": res.key if res else "",
                    "model": res.model if res else "", "captured": utcnow()}
                q["response_ids"] = [rid]
                q["status"] = "ANSWERED" if usable else "UNUSABLE"
                atomic_write_text(d / "02_query-responses" / f"{q['qid']}__query-response.md",
                                  f"# {q['qid']} - {rid}\n\nUsable: {usable}\n\nCited: {', '.join(cites)}\n\n"
                                  f"## Exact question\n\n{q['text']}\n\n## Exact answer\n\n{text}\n")
            state["phase"] = "assess"
            save_all()
            ctx.log(f"quest R{rnd}: {sum(1 for q in open_qs if responses[q['qid']]['usable'])} usable answers")

        if state["phase"] == "assess":
            round_qs = [q for q in questions if q["round"] == rnd and q["status"] in ("ANSWERED", "UNUSABLE")]
            usable_qs = [q for q in round_qs if responses.get(q["qid"], {}).get("usable")]
            prev_frag = d / "04_ach-eval-checkpoints" / f"R{rnd - 1:03d}-fragment.md"
            cov = coverage_ledger(questions, responses, ranks)
            ax2 = "enabled with definition (see header)" if len(axes) > 1 else "disabled"
            system, user, _ = ctx.prompts.render(
                "coordinator.md", GOAL=frame["axes"][0].get("question", frame.get("title", "")),
                HEADER_VERSION=frame.get("header_sha256", "")[:16], AXIS2=ax2,
                INVESTIGATION_ID=ctx.run_id, PRIOR_FRAGMENT_ID=(f"R{rnd - 1:03d}" if prev_frag.exists() else "none"),
                ROUND_SIZE=n_q, GAUGE=gauge, ROUND=rnd, HEADER=header,
                PRIOR_FRAGMENT=read_text(prev_frag) if prev_frag.exists() else "none (initial assessment)",
                NEW_QIDS=", ".join(q["qid"] for q in usable_qs) or "none",
                NEW_RECORDS=_qrecords_text(usable_qs, responses, max_words=2000),
                COVERAGE=coverage_text(cov))
            resp = ctx.llm.call(LLMRequest(role="coordinator", system=system, user=user, expect_json=False,
                                           tag=f"assess:R{rnd:03d}",
                                           meta={"round": rnd, "frame": frame, "gauge": gauge}))
            parsed = parse_coordinator(resp.text, frame, gauge)
            atomic_write_text(d / "04_ach-eval-checkpoints" / f"R{rnd:03d}-fragment.md", resp.text)
            hist_entry = {"round": rnd, "allocations": parsed["allocations"], "problems": parsed["problems"],
                          "direction": parsed["direction"], "qids": [q["qid"] for q in usable_qs]}
            if parsed["allocations"]:
                state["history"].append(hist_entry)
            stop = evaluate_stop(state["history"], gauge, axes, cov["ab_covered"], parsed["substantive_ok"])
            write_json(d / "04_ach-eval-checkpoints" / f"R{rnd:03d}-assessment.json",
                       {**hist_entry, "substantive": parsed["substantive"], "stop_evaluation": stop,
                        "call_key": resp.key})
            direction = "STOP" if stop["stop"] else ("CONTINUE" if parsed["direction"] == "STOP"
                                                     else parsed["direction"])
            atomic_write_text(d / "05_feedback" / f"R{rnd:03d}-packet.md",
                              render_packet(rnd, hist_entry["qids"], direction, parsed["packet"]))
            ctx.log(f"quest R{rnd}: assessment {parsed['allocations']} stop={stop['stop']}")
            if stop["stop"]:
                state.update(status="stopped", phase="done", stop_basis="SCIENTIFIC_STOP",
                             stop_evaluation=stop, stopped=utcnow())
            elif rnd >= max_rounds:
                state.update(status="stopped", phase="done", stop_basis="OPERATIONAL_LIMIT",
                             stop_evaluation=stop, stopped=utcnow(),
                             note=f"max_rounds={max_rounds} reached; this is an operational stop, "
                                  f"not a scientific completion finding")
            else:
                state["round"] = rnd + 1
                state["phase"] = "investigate"
            save_all()

    closeout = {"status": state.get("stop_basis"), "rounds": state["round"],
                "questions_issued": len(questions),
                "usable_answers": sum(1 for r in responses.values() if r.get("usable")),
                "stop_evaluation": state.get("stop_evaluation"), "note": state.get("note", ""),
                "closed": utcnow()}
    write_json(d / "06_closeout" / "closeout.json", closeout)
    return closeout
