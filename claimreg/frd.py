"""Phase III - FRD generation, blind validation, retention (spec 16-19; Problems note).

Generation: one query-response file at a time; every FRD carries exactly one
producing QID; at most ``frd.max_per_response`` FRDs per response (the
Problems note: "Every proper query response must produce four or less FRDs").

Validation: one candidate FRD + only its named source; no frame.  The
validator must copy its supporting source text verbatim; the harness then
checks that text against the source file mechanically.  A quotation that
cannot be found blocks READY status (``frd.quote_gate``), which is what makes
every downstream witness auditable against a real passage.

Retention: READY FRDs are ranked; the lowest-ranked are archived (never
deleted) only when the validated database exceeds the corpus-size budget,
and never more than ``1 - keep_fraction`` of them.
"""

from __future__ import annotations

import json
import re

from .corpus import find_quote
from .llm.base import LLMRequest
from .llm.jsonparse import as_list
from .runctx import extract_labels
from .util import digest, read_json, tokens, utcnow, word_count

VERDICT_RANK = {"RIGHT": 4, "MOSTLY RIGHT": 3, "PARTLY RIGHT": 2, "WRONG": 0,
                "NOT FOUND": 0, "SOURCE UNAVAILABLE": 0}


def norm_verdict(v: str) -> str:
    v = (v or "").upper().replace("_", " ").strip()
    for k in ("MOSTLY RIGHT", "PARTLY RIGHT", "SOURCE UNAVAILABLE", "NOT FOUND", "RIGHT", "WRONG"):
        if k in v:
            return k
    return v or "UNKNOWN"


def is_ready(s: str) -> bool:
    s = (s or "").upper()
    return "READY" in s and "NOT READY" not in s


# --------------------------------------------------------------------------- #
# generation
# --------------------------------------------------------------------------- #

def generate_frds(ctx) -> dict:
    d = ctx.p("discovery")
    questions = {q["qid"]: q for q in read_json(d / "01_issued-questions" / "questions.json", default=[]) or []}
    responses = read_json(d / "02_query-responses" / "responses.json", default=[]) or []
    usable = [r for r in responses if r.get("usable")]
    labels = extract_labels(ctx.archivist_instructions())
    subject = ctx.frame.get("title", "the investigation subject")
    cap = int(ctx.cfg["frd"].get("max_per_response", 4))
    reqs = []
    for r in sorted(usable, key=lambda x: x["qid"]):
        q = questions.get(r["qid"], {})
        origin = "RESP-" + digest(r["response_id"], 8)
        system, user, _ = ctx.prompts.render(
            "frd_generate.md", SUBJECT=subject, LABELS=labels, ORIGIN_REF=origin, QID=r["qid"],
            NAMED_SOURCES=", ".join(v for v in q.get("sources_resolved", {}).values()) or "(none)",
            QUESTION=q.get("text", ""), RESPONSE=r["text"])
        reqs.append((r, origin, LLMRequest(role="frd_generator", system=system, user=user,
                                           tag=f"frd-gen:{r['qid']}",
                                           meta={"qid": r["qid"], "response": r["text"],
                                                 "sources": r.get("cited_sources", [])})))
    results = ctx.llm.call_many([x[2] for x in reqs])
    candidates, harvest, over = [], [], []
    for (r, origin, _), res in zip(reqs, results):
        data = res.parsed if res and isinstance(res.parsed, dict) else {}
        items = [x for x in as_list(data.get("frds") if data else (res.parsed if res else []), "frds")
                 if isinstance(x, dict) and (x.get("claim") or "").strip()]
        kept, extra = items[:cap], items[cap:]
        for i, it in enumerate(kept, 1):
            files = [f for f in (it.get("source_files") or []) if isinstance(f, str)]
            resolved = [ctx.corpus.resolve(f) or f"UNRESOLVED:{f}" for f in files]
            status = (it.get("status") or "ordinary").lower()
            if not files:
                status = "needs-source"
            candidates.append({
                "frd_id": f"FRD-{r['qid']}-{i:02d}", "qid": r["qid"], "response_id": r["response_id"],
                "origin_ref": origin, "ordinal": i, "cluster": it.get("cluster", ""),
                "label": it.get("label", ""), "source_files": resolved,
                "locator": it.get("locator", ""), "claim": it["claim"].strip(),
                "verification_instruction": it.get("verification_instruction", ""),
                "evidence_label": it.get("evidence_label", ""),
                "provenance": it.get("provenance", "DERIVATIVE_UNKNOWN"), "status": status,
                "speaker": it.get("speaker", ""), "call_key": res.key if res else ""})
        for it in extra:
            over.append({"qid": r["qid"], "claim": it.get("claim", ""), "why": f"over the {cap}-FRD limit"})
        harvest.append({"qid": r["qid"], "response_id": r["response_id"], "origin_ref": origin,
                        "frds": len(kept), "over_limit": len(extra),
                        "review": data.get("harvest_review", {}) if data else {},
                        "parse_error": res.parse_error if res else "no response"})
    ctx.save("frds", "01_candidates/candidates.json", candidates, "candidate-frds")
    cited_all = sorted({s for r in usable for s in r.get("cited_sources", [])})
    producing = sorted({s for c in candidates for s in c["source_files"]})
    acct = {"responses_processed": len(usable), "candidates": len(candidates),
            "over_limit_not_extracted": over,
            "sources_cited_in_answers": len(cited_all), "sources_producing_frds": len(producing),
            "under_harvested_sources": [s for s in cited_all if s not in producing],
            "per_response": harvest,
            "provenance_counts": _count(c["provenance"].split("(")[0] for c in candidates)}
    ctx.save("frds", "02_harvest-accounting/harvest.json", acct, "harvest-accounting")
    return {"responses": len(usable), "candidates": len(candidates), "over_limit": len(over)}


def _count(it) -> dict:
    out: dict = {}
    for x in it:
        out[x] = out.get(x, 0) + 1
    return out


# --------------------------------------------------------------------------- #
# validation
# --------------------------------------------------------------------------- #

def _source_payload(ctx, filename: str, query: str) -> tuple[str, str]:
    maxw = int(ctx.cfg["frd"].get("validator_source_words", 14000))
    text = ctx.corpus.text(filename)
    wc = word_count(text)
    if wc <= maxw:
        return text, f"complete source, {wc} words"
    ex = ctx.corpus.excerpt(filename, query, maxw)
    return (f"Headings: {'; '.join(h.strip() for h in ex['outline'][:60])}\n\n{ex['text']}",
            f"EXCERPTS ONLY: {ex['words']} of {wc} words, selected by relevance to the claim")


def validate_frds(ctx) -> dict:
    cands = ctx.load("frds", "01_candidates/candidates.json", default=[]) or []
    labels = extract_labels(ctx.archivist_instructions())
    jobs = []
    for c in cands:
        files = [f for f in c["source_files"] if not f.startswith("UNRESOLVED:")]
        if c["status"] == "needs-source" or not files:
            jobs.append((c, None, None))
            continue
        per_source = files if c["status"] == "disambiguate" else files[:1]
        for f in per_source:
            q = " ".join([c["claim"], c.get("locator", ""), c.get("verification_instruction", "")])
            src_text, note = _source_payload(ctx, f, q)
            system, user, _ = ctx.prompts.render(
                "frd_validate.md", LABELS=labels, FRD_ID=c["frd_id"], ORIGIN_REF=c["origin_ref"],
                QID=c["qid"], SOURCE_FILES=f, LOCATOR=c.get("locator", ""), LABEL=c.get("evidence_label", ""),
                PROVENANCE=c.get("provenance", ""), STATUS=c["status"], CLAIM=c["claim"],
                VERIFICATION=c.get("verification_instruction", ""), SOURCE_NOTE=note, SOURCE_TEXT=src_text)
            jobs.append((c, f, LLMRequest(role="frd_validator", system=system, user=user,
                                          tag=f"validate:{c['frd_id']}:{f}",
                                          meta={"frd": c, "source": f, "source_text": src_text})))
    reqs = [j[2] for j in jobs if j[2] is not None]
    results = iter(ctx.llm.call_many(reqs))
    validations, validated = [], []
    gate = ctx.cfg["frd"].get("quote_gate", "block")
    min_ratio = float(ctx.cfg["frd"].get("quote_min_ratio", 0.92))
    for c, f, req in jobs:
        if req is None:
            validations.append({"validation_id": f"VAL-{c['frd_id']}", "frd_id": c["frd_id"], "qid": c["qid"],
                                "verdict": "SOURCE UNAVAILABLE", "readiness": "NOT READY FOR WITNESS CONSTRUCTION",
                                "readiness_reason": "no resolvable named source (needs-source)",
                                "original_claim": c["claim"]})
            continue
        res = next(results)
        data = res.parsed if res and isinstance(res.parsed, dict) else {}
        recs = [data] + [ch for ch in (data.get("children") or []) if isinstance(ch, dict)]
        full = ctx.corpus.text(f)
        for k, rdat in enumerate(recs):
            child = k > 0
            vid = f"VAL-{c['frd_id']}" + (f"-{_short(f)}" if c["status"] == "disambiguate" else "") + (f"-c{k}" if child else "")
            vfrd_id = c["frd_id"] + (f"-{_short(f)}" if c["status"] == "disambiguate" else "") + (f"-c{k}" if child else "")
            st = rdat.get("source_text") or ""
            qc = find_quote(full, st, min_ratio) if st.strip() else {"found": False, "method": "none",
                                                                    "why": "no source text returned"}
            verdict = norm_verdict(rdat.get("verdict") or data.get("verdict"))
            ready = is_ready(rdat.get("readiness") or "")
            reason = rdat.get("readiness_reason", "")
            if res and res.parse_error and not data:
                ready, reason = False, f"validator output unusable: {res.parse_error}"
            if ready and not qc["found"] and gate == "block":
                ready = False
                reason = ("mechanical check: the validator's source_text was not found in the named source "
                          "file (" + qc.get("why", qc.get("method", "")) + "); " + reason)
            cit = rdat.get("citation") or data.get("citation") or {}
            rec = {"validation_id": vid, "vfrd_id": vfrd_id, "frd_id": c["frd_id"], "qid": c["qid"],
                   "child": child, "source_file": f,
                   "citation": {"filename": f, "locator": (cit.get("locator") if isinstance(cit, dict) else str(cit))},
                   "claim": (rdat.get("claim") or "").strip(), "source_text": st,
                   "verdict": verdict,
                   "verdict_explanation": rdat.get("verdict_explanation") or data.get("verdict_explanation", ""),
                   "evidence_label": rdat.get("evidence_label") or c.get("evidence_label", ""),
                   "provenance": rdat.get("provenance") or c.get("provenance", ""),
                   "readiness": "READY FOR WITNESS CONSTRUCTION" if ready else "NOT READY FOR WITNESS CONSTRUCTION",
                   "readiness_reason": reason, "quote_check": qc, "original_claim": c["claim"],
                   "call_key": res.key if res else "", "model": res.model if res else ""}
            validations.append(rec)
            if ready and rec["claim"]:
                validated.append(rec)
    ctx.save("frds", "04_validation-results/validations.json", validations, "validations")
    ctx.save("frds", "05_validated/validated-frds.json", validated, "validated-frds")
    return {"candidates": len(cands), "validations": len(validations), "ready": len(validated),
            "quote_unverified": sum(1 for v in validations if v.get("quote_check") and not v["quote_check"].get("found"))}


def _short(f: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", f.split(".")[0])[:10]


# --------------------------------------------------------------------------- #
# retention (Problems note)
# --------------------------------------------------------------------------- #

def budget_pct(corpus_mb: float, rcfg: dict) -> float:
    s_mb, l_mb = float(rcfg["small_corpus_mb"]), float(rcfg["large_corpus_mb"])
    s_pct, l_pct = float(rcfg["small_budget_pct"]), float(rcfg["large_budget_pct"])
    if corpus_mb <= s_mb:
        return s_pct
    if corpus_mb >= l_mb:
        return l_pct
    f = (corpus_mb - s_mb) / (l_mb - s_mb)
    return s_pct + f * (l_pct - s_pct)


def _jacc(a: str, b: str) -> float:
    sa, sb = set(tokens(a)), set(tokens(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def retain_frds(ctx) -> dict:
    rcfg = ctx.cfg["retention"]
    validated = ctx.load("frds", "05_validated/validated-frds.json", default=[]) or []
    cands = ctx.load("frds", "01_candidates/candidates.json", default=[]) or []
    corpus_bytes = ctx.corpus.total_bytes()
    pct = budget_pct(corpus_bytes / 1e6, rcfg)
    # redundancy: same source file and near-identical claim
    redundant = {}
    by_src: dict = {}
    for v in validated:
        by_src.setdefault(v["source_file"], []).append(v)
    for src, vs in by_src.items():
        vs = sorted(vs, key=lambda x: (-VERDICT_RANK.get(x["verdict"], 0), x["vfrd_id"]))
        for i, a in enumerate(vs):
            if a["vfrd_id"] in redundant:
                continue
            for b in vs[i + 1:]:
                if b["vfrd_id"] not in redundant and _jacc(a["claim"], b["claim"]) >= 0.72:
                    redundant[b["vfrd_id"]] = a["vfrd_id"]

    def score(v):
        s = VERDICT_RANK.get(v["verdict"], 0) * 10
        s += {"exact": 4, "segments": 3, "segments_partial": 2, "fuzzy": 2}.get(
            (v.get("quote_check") or {}).get("method", ""), 0)
        s += min(5, word_count(v.get("source_text", "")) // 40)
        if v["vfrd_id"] in redundant:
            s -= 30
        return s

    ranked = sorted(validated, key=lambda v: (-score(v), v["vfrd_id"]))
    db_bytes = len(json.dumps(validated, ensure_ascii=False).encode("utf-8"))
    cand_bytes = len(json.dumps(cands, ensure_ascii=False).encode("utf-8"))
    budget = corpus_bytes * pct / 100.0
    max_archive = int(len(ranked) * (1 - float(rcfg.get("keep_fraction", 0.8))))
    archived = []
    kept = list(ranked)
    over_budget = len(json.dumps(kept, ensure_ascii=False).encode("utf-8")) > budget
    if over_budget and rcfg.get("archive_redundant_first", True):     # only ever to meet the budget
        for v in list(reversed(kept)):
            if len(archived) >= max_archive or len(json.dumps(kept, ensure_ascii=False).encode("utf-8")) <= budget:
                break
            if v["vfrd_id"] in redundant:
                kept.remove(v)
                archived.append({**v, "archive_reason": f"REDUNDANT_WITH {redundant[v['vfrd_id']]}"})
    cur = len(json.dumps(kept, ensure_ascii=False).encode("utf-8"))
    while cur > budget and len(archived) < max_archive and kept:
        v = kept.pop()
        archived.append({**v, "archive_reason": "lowest-ranked READY FRD archived to meet the "
                                                f"{pct:.1f}% FRD-database budget"})
        cur = len(json.dumps(kept, ensure_ascii=False).encode("utf-8"))
    kept_ids = {v["vfrd_id"] for v in kept}
    retained = [v for v in validated if v["vfrd_id"] in kept_ids]
    archived_qids = sorted({a["qid"] for a in archived} - {v["qid"] for v in retained})
    out = {"corpus_bytes": corpus_bytes, "budget_pct": round(pct, 2), "budget_bytes": int(budget),
           "candidate_db_bytes": cand_bytes, "validated_db_bytes_before": db_bytes,
           "validated_db_bytes_after": cur, "ready": len(validated), "retained": len(retained),
           "archived": archived, "archived_questions": archived_qids,
           "redundant_pairs": redundant, "max_archivable": max_archive,
           "ratios": {"candidate_db_over_corpus": round(cand_bytes / max(1, corpus_bytes), 4),
                      "validated_over_candidate_db": round(db_bytes / max(1, cand_bytes), 3)},
           "within_budget": cur <= budget, "time": utcnow()}
    ctx.save("frds", "06_source-assignment-audit/retention.json", out, "retention")
    ctx.save("frds", "05_validated/retained-frds.json", retained, "retained-frds")
    return {"ready": len(validated), "retained": len(retained), "archived": len(archived),
            "within_budget": out["within_budget"], "budget_pct": out["budget_pct"]}
