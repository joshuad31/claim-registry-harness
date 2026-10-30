"""Import the ChatGPT-era PTX full run (2026-10-24) into a Claim Registry project.

What is imported, and how it is labelled
----------------------------------------
* corpus (111 Markdown files), header v4.1, ranked index, Archivist prompt;
* discovery: 62 issued questions and their exact NotebookLM answers, the 12
  feedback packets, and the Coordinator's recorded scientific STOP;
* FRDs: the 77 candidate records and the 73 READY validations that the
  earlier run retained (its post-validation selection).

These stages are marked ``imported`` in the run's stage state, with the
source file and its sha256.  Nothing upstream is re-judged; the harness's own
mechanical quote check is still applied to every imported validation.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from .util import (atomic_write_text, ensure_dir, read_json, read_text, sha256_file, utcnow,
                   write_json)


def _block(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*\n+```(?:text)?\n(.*?)\n```", text, re.M | re.S)
    return m.group(1) if m else ""


def _meta(text: str) -> dict:
    raw = _block(text, "Recording metadata")
    try:
        return json.loads(raw) if raw else {}
    except Exception:
        return {}


def import_chatgpt_ptx(chatgpt_run: Path, project_dir: Path, run_id: str, copy_corpus: bool = True) -> dict:
    from .pipeline import stage_corpus, stage_frame
    from .runctx import RunContext
    chatgpt_run = Path(chatgpt_run)
    hr = chatgpt_run / "Human Review"
    quest = chatgpt_run / "ChatGPTs folder" / "04 Quest"
    project_dir = ensure_dir(project_dir)
    # ---- project files
    src_dir = project_dir / "01_CORPUS" / "source-files"
    if copy_corpus:
        ensure_dir(src_dir)
        for p in sorted((chatgpt_run / "Corpus" / "source-files").glob("*")):
            if p.is_file() and not (src_dir / p.name).exists():
                shutil.copyfile(p, src_dir / p.name)
    man_csv = chatgpt_run / "Corpus" / "SOURCE-MANIFEST.csv"
    if man_csv.exists():
        ensure_dir(project_dir / "01_CORPUS" / "provenance")
        shutil.copyfile(man_csv, project_dir / "01_CORPUS" / "provenance" / "SOURCE-MANIFEST-chatgpt-run.csv")
    fdir = ensure_dir(project_dir / "01_FRAME")
    shutil.copyfile(hr / "PTX_for_urination_header_v4.1.md", fdir / "header.md")
    shutil.copyfile(hr / "PTX_for_urination index.md", fdir / "index.md")
    shutil.copyfile(chatgpt_run / "ChatGPTs folder" / "03 Prompts" / "archivist" / "custom-prompt.txt",
                    fdir / "archivist-custom-prompt.txt")
    if not (project_dir / "project.json").exists():
        write_json(project_dir / "project.json", {
            "project": {"name": "PTX for urination", "run_prefix": "RUN-PTX"},
            "frame": {"approval_note": "Axis 1 approved by Josh on 2026-09-12 (header v4.1); axis 2 is "
                                       "TEST-ONLY per the header and is reported as such."},
            "default_provider": "queue",
        })
    ctx = RunContext(project_dir, run_id, create=True)
    ctx.set_stage("corpus", "running")
    ctx.set_stage("corpus", "done", stage_corpus(ctx))
    ctx.set_stage("index", "done", {"index": "supplied (imported)"})
    ctx.set_stage("archivist_prompt", "done", {"archivist_prompt": "supplied (imported)"})
    ctx.set_stage("frame", "done", stage_frame(ctx))
    corpus = ctx.corpus

    # ---- discovery
    d = ctx.p("discovery")
    questions, responses = [], []
    qfiles = sorted((quest / "questions").glob("*-Q*.md"))
    for qf in qfiles:
        t = read_text(qf)
        qid = re.search(r"(Q\d{4})", qf.name).group(1)
        meta = _meta(t)
        exact = _block(t, "Exact query")
        sv = re.search(r"Source voices:\s*(\[.*?\])", t)
        voices = json.loads(sv.group(1)) if sv else []
        resolved = {v: (corpus.resolve(v) or "UNRESOLVED_NAME") for v in voices}
        rf = quest / "query-responses" / f"{qf.stem}-A01.md"
        rt = read_text(rf) if rf.exists() else ""
        rmeta = _meta(rt)
        answer = _block(rt, "Exact answer")
        cap = rmeta.get("capture", {})
        usable = bool(cap.get("usable")) and bool(answer.strip())
        cited = [corpus.resolve(c.get("source_voice", "")) or c.get("source_voice", "")
                 for c in cap.get("cited_sources", []) if isinstance(c, dict)]
        rid = f"R-{qid}-A01"
        questions.append({
            "qid": qid, "run_id": "PTX-Full-Run-2026-10-24", "round": meta.get("round_number"),
            "order_in_round": meta.get("order_in_round"), "text": exact.strip(),
            "firewall": {"status": "IMPORTED", "repairs": [], "original_text": exact.strip()},
            "sources_as_sent": voices, "sources_resolved": resolved,
            "target": meta.get("target_ledger_row_or_test", ""), "packet_priority_id": meta.get("packet_priority_id"),
            "header_version": meta.get("header_version", ""), "issued": "", "status": "ANSWERED" if usable else "UNUSABLE",
            "response_ids": [rid], "frd_ids": [], "witness_ids": [], "notebook_lane": meta.get("notebook_lane"),
            "imported_from": str(qf.relative_to(chatgpt_run))})
        oc = re.search(r"^Outcome:\s*(\S+)", rt, re.M)
        responses.append({
            "response_id": rid, "qid": qid, "attempt": "A01", "outcome": oc.group(1) if oc else "UNKNOWN",
            "usable": usable, "text": answer, "cited_sources": cited,
            "requested_sources_cited": [s for s in resolved.values() if s in cited],
            "requested_sources_absent": [s for s in resolved.values() if s not in cited and s != "UNRESOLVED_NAME"],
            "retrieval": {"system": "NotebookLM (111 sources)", "notebook": re.search(r"^Notebook:\s*(\S+)", rt, re.M).group(1)
                          if re.search(r"^Notebook:\s*(\S+)", rt, re.M) else ""},
            "capture_limitations": cap.get("capture_limitations", ""), "model": "NotebookLM",
            "captured": (re.search(r"^Captured:\s*(\S+)", rt, re.M).group(1) if re.search(r"^Captured:\s*(\S+)", rt, re.M) else ""),
            "imported_from": str(rf.relative_to(chatgpt_run)) if rf.exists() else ""})
        atomic_write_text(d / "01_issued-questions" / f"{qid}__issued-question.md", t)
        if rt:
            atomic_write_text(d / "02_query-responses" / f"{qid}__query-response.md", rt)
    write_json(d / "01_issued-questions" / "questions.json", questions)
    write_json(d / "02_query-responses" / "responses.json", responses)
    for pf in sorted((quest / "feedback-packets").glob("R*.md")):
        shutil.copyfile(pf, d / "05_feedback" / f"{pf.stem}-packet.md")
    if (quest / "quest-state" / "Quest-State.md").exists():
        shutil.copyfile(quest / "quest-state" / "Quest-State.md", d / "03_quest-state" / "Quest-State-imported.md")
    if (quest / "quest-state" / "saved-evidence.json").exists():
        shutil.copyfile(quest / "quest-state" / "saved-evidence.json", d / "03_quest-state" / "saved-evidence-imported.json")
    rounds = sorted({q["round"] for q in questions if q["round"]})
    write_json(d / "03_quest-state" / "state.json", {"status": "imported", "round": max(rounds) if rounds else 0,
                                                    "phase": "done"})
    closeout = {"status": "SCIENTIFIC_STOP (imported)", "rounds": len(rounds), "questions_issued": len(questions),
                "usable_answers": sum(1 for r in responses if r["usable"]),
                "note": "Imported from the ChatGPT-era run: the Coordinator's R012 packet directed STOP. "
                        "Its ACH_Eval fragments were kept private by that run and are not part of this import.",
                "closed": utcnow()}
    write_json(d / "06_closeout" / "closeout.json", closeout)
    ctx.set_stage("quest", "imported", {"questions": len(questions), "usable": closeout["usable_answers"],
                                        "packets": len(list((quest / 'feedback-packets').glob('R*.md'))),
                                        "source": str(quest)})

    # ---- FRDs
    dbp = hr / "FRD database.json"
    db = read_json(dbp)
    srcmap = {s["id"]: s["filename"] for s in db["sources"]}
    recs = db["records"]
    cands = [r for r in recs if r["kind"] == "candidate"]
    vals = {r["id"]: r for r in recs if r["kind"] == "validation"}
    cand_by_id = {c["id"]: c for c in cands}
    used_ids = set()
    our_cands = []
    for c in cands:
        fid = c.get("frd_id") or f"FRD-{c['qid']}-{int(c.get('ordinal') or c.get('frd_slot') or 1):02d}"
        base, k = fid, 2
        while fid in used_ids:
            fid = f"{base}-r{k}"
            k += 1
        used_ids.add(fid)
        c["_our_id"] = fid
        loc = c.get("locator") or {}
        our_cands.append({
            "frd_id": fid, "qid": c["qid"], "response_id": f"R-{c['qid']}-A01", "origin_ref": c.get("origin", ""),
            "ordinal": c.get("ordinal"), "cluster": "", "label": c.get("source_act", ""),
            "source_files": [srcmap.get(s, s) for s in c.get("sources", [])],
            "locator": loc.get("heading", "") if isinstance(loc, dict) else str(loc),
            "claim": c["claim"], "verification_instruction": c.get("verification_instruction", ""),
            "evidence_label": c.get("evidence_label", ""), "provenance": c.get("provenance", ""),
            "status": c.get("source_status", "ordinary"), "speaker": c.get("authorial_voice", ""),
            "imported_id": c["id"]})
    write_json(ctx.p("frds", "01_candidates/candidates.json"), our_cands)
    from .corpus import find_quote
    from .frd import is_ready, norm_verdict
    retained_ids = db["post_validation_relevance"]["selection"]["retained_validation_ids"]
    validations, validated = [], []
    for vid, v in vals.items():
        c = cand_by_id.get(v.get("candidate_id"), {})
        fn = (v.get("citation") or {}).get("filename") or srcmap.get((v.get("sources") or [None])[0], "")
        fn = corpus.resolve(fn) or fn
        qc = find_quote(corpus.text(fn), v.get("source_text") or "") if fn in corpus.by_name else \
            {"found": False, "method": "none", "why": "source not in corpus"}
        ready = is_ready(v.get("readiness", "")) and vid in retained_ids
        rec = {"validation_id": vid, "vfrd_id": c.get("_our_id", vid), "frd_id": c.get("_our_id", vid),
               "qid": v.get("qid") or c.get("qid"), "child": False, "source_file": fn,
               "citation": {"filename": fn, "locator": (v.get("citation") or {}).get("locator", "")},
               "claim": v.get("claim", ""), "source_text": v.get("source_text", ""),
               "verdict": norm_verdict(v.get("verdict", "")), "verdict_explanation": v.get("explanation", ""),
               "evidence_label": v.get("evidence_label", ""), "provenance": v.get("provenance", ""),
               "readiness": v.get("readiness", ""), "readiness_reason": ("" if vid in retained_ids else
                                                                         "not in the earlier run's retained selection"),
               "quote_check": qc, "original_claim": v.get("original_claim", c.get("claim", "")),
               "reviewer": v.get("reviewer", ""), "imported_id": vid}
        validations.append(rec)
        if ready and qc.get("found"):
            validated.append(rec)
    write_json(ctx.p("frds", "04_validation-results/validations.json"), validations)
    write_json(ctx.p("frds", "05_validated/validated-frds.json"), validated)
    write_json(ctx.p("frds", "02_harvest-accounting/harvest.json"),
               {"imported": True, "candidates": len(our_cands), "per_response": [
                   {"qid": q["qid"], "frds": sum(1 for c in our_cands if c["qid"] == q["qid"])} for q in questions]})
    prov = {"source": str(dbp), "sha256": sha256_file(dbp)}
    ctx.set_stage("frd_generate", "imported", {"candidates": len(our_cands), **prov})
    ctx.set_stage("frd_validate", "imported", {"validations": len(validations), "ready_retained": len(validated),
                                               "quote_verified": sum(1 for v in validations if v["quote_check"].get("found")),
                                               **prov})
    write_json(ctx.run_dir / "IMPORT-RECORD.json", {
        "imported": utcnow(), "from": str(chatgpt_run), "frd_database": prov,
        "header_sha256": sha256_file(fdir / "header.md"), "questions": len(questions),
        "usable_answers": closeout["usable_answers"], "candidates": len(our_cands),
        "validated_ready": len(validated)})
    return {"run_id": ctx.run_id, "questions": len(questions), "usable": closeout["usable_answers"],
            "candidates": len(our_cands), "validated": len(validated)}
