"""Final outputs: metrics, the analyst-facing crux report (< 4,000 words), and an
HTML audit browser that walks crux -> witness -> FRD -> verbatim source quote ->
producing question -> Archivist answer.
"""

from __future__ import annotations

import html
import json
import re

from .header import all_hypotheses
from .llm.base import LLMRequest
from .util import (atomic_write_text, read_jsonl, read_text, tokens, truncate_words, utcnow,
                   word_count)


def providers_used(ctx) -> list[str]:
    """Every provider:model that answered a call in this run, from the run's own call log."""
    log = ctx.run_dir / "00_RUN-CONTROL" / "model-and-human-decisions" / "llm-calls.jsonl"
    try:
        rows = read_jsonl(log)
    except OSError:
        return []
    return sorted({f"{r.get('provider')}:{r.get('model')}" for r in rows if r.get("provider")})


def _bytes(obj) -> int:
    return len(json.dumps(obj, ensure_ascii=False).encode("utf-8"))


def compute_metrics(ctx) -> dict:
    corpus_bytes = ctx.corpus.total_bytes()
    cands = ctx.load("frds", "01_candidates/candidates.json", default=[]) or []
    vals = ctx.load("frds", "04_validation-results/validations.json", default=[]) or []
    retained = ctx.load("frds", "05_validated/retained-frds.json", default=None)
    if retained is None:
        retained = ctx.load("frds", "05_validated/validated-frds.json", default=[]) or []
    ws = ctx.load("witnesses", "05_released/witnesses.json", default=[]) or []
    cov = (ctx.load("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
    crux = ctx.load("crux", "05_candidates/crux-candidates.json", default={}) or {}
    responses = ctx.load("discovery", "02_query-responses/responses.json", default=[]) or []
    set_ws = sorted({w for c in cov.values() for s in c.get("sets", []) for w in s["witnesses"]})
    crux_ws = sorted({c["witness_id"] for c in crux.get("candidates", [])})
    wtext = {w["witness_id"]: w["text"] for w in ws}
    per_resp: dict = {}
    for c in cands:
        per_resp[c["qid"]] = per_resp.get(c["qid"], 0) + 1
    m = {
        "corpus_bytes": corpus_bytes,
        "responses_usable": sum(1 for r in responses if r.get("usable")),
        "frd_candidates": len(cands), "validations": len(vals), "frds_retained": len(retained),
        "witnesses_released": len(ws), "witnesses_in_sets": len(set_ws), "crux_witnesses": len(crux_ws),
        "frd_db_bytes": _bytes(cands), "validated_db_bytes": _bytes(retained),
        "witness_db_bytes": _bytes(ws),
        "set_witness_text_bytes": sum(len(wtext.get(w, "").encode("utf-8")) for w in set_ws),
        "frds_per_response_max": max(per_resp.values()) if per_resp else 0,
        "responses_over_4_frds": sum(1 for v in per_resp.values() if v > 4),
    }
    small, large = 1e6, 12e6
    if corpus_bytes <= small:
        frd_target = 0.25
    elif corpus_bytes >= large:
        frd_target = 0.08
    else:
        frd_target = 0.25 + (corpus_bytes - small) / (large - small) * (0.08 - 0.25)
    t = []

    def tgt(name, value, target, ok, note=""):
        t.append({"metric": name, "value": value, "target": target, "met": ok, "note": note})

    r1 = m["frd_db_bytes"] / max(1, corpus_bytes)
    tgt("FRD database / corpus", round(r1, 4), f"<= {frd_target:.3f}", r1 <= frd_target)
    r2 = m["validated_db_bytes"] / max(1, m["frd_db_bytes"])
    tgt("validated FRD db / FRD db", round(r2, 3), "< 2.0", r2 < 2.0,
        "validated records carry the validator's explanation and the quotation check")
    r3 = m["witness_db_bytes"] / max(1, m["validated_db_bytes"])
    tgt("witness db / validated FRD db", round(r3, 3), "<= 0.25", r3 <= 0.25)
    r4 = m["witnesses_in_sets"] / max(1, m["witnesses_released"])
    tgt("witnesses used by deletion-minimal sets", round(r4, 3), "< 0.33", (r4 < 0.33) if set_ws else None,
        "not applicable: no hypothesis has complete coverage" if not set_ws else "")
    if set_ws:
        r5 = 1 - m["crux_witnesses"] / max(1, len(set_ws))
        tgt("set witnesses eliminated by crux identification", round(r5, 3), ">= 0.50", r5 >= 0.5)
    r6 = m["set_witness_text_bytes"] / max(1, corpus_bytes)
    tgt("final witness text / corpus", round(r6, 5), "about 0.01", (r6 <= 0.02) if set_ws else None,
        "not applicable: no coverage sets" if not set_ws else "")
    tgt("FRDs per response (max)", m["frds_per_response_max"], "<= 4", m["frds_per_response_max"] <= 4)
    m["targets"] = t
    m["note"] = ("Targets come from 'Problems with the ACH architecture' and are design goals, not "
                 "demonstrated properties. Byte sizes are of the complete JSON databases.")
    return m


# --------------------------------------------------------------------------- #
# report
# --------------------------------------------------------------------------- #

def _load_all(ctx) -> dict:
    d = {}
    d["frame"] = ctx.frame
    d["units"] = {u["unit_id"]: u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])}
    d["witnesses"] = {w["witness_id"]: w for w in (ctx.load("witnesses", "05_released/witnesses.json", default=[]) or [])}
    d["held"] = ctx.load("witnesses", "04_repaired-or-held/held.json", default=[]) or []
    ret = ctx.load("frds", "05_validated/retained-frds.json", default=None)
    if ret is None:
        ret = ctx.load("frds", "05_validated/validated-frds.json", default=[]) or []
    d["vfrds"] = {v["vfrd_id"]: v for v in ret}
    d["questions"] = {q["qid"]: q for q in (ctx.load("discovery", "01_issued-questions/questions.json", default=[]) or [])}
    d["responses"] = {r["qid"]: r for r in (ctx.load("discovery", "02_query-responses/responses.json", default=[]) or [])}
    d["coverage"] = (ctx.load("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
    d["crux"] = ctx.load("crux", "05_candidates/crux-candidates.json", default={}) or {}
    d["tests"] = ctx.load("crux", "03_portability-tests/tests.json", default=[]) or []
    from .matching import relations_index
    d["relations"] = list(relations_index(ctx).values())   # includes human decisions, if any
    d["match_summary"] = ctx.load("matching", "03_match-records/summary.json", default={}) or {}
    d["qualification"] = ctx.load("matching", "02_match-fixtures/qualification.json", default={}) or {}
    d["assessment"] = ctx.load("reports", "assessment.json", default={}) or {}
    d["closeout"] = ctx.load("discovery", "06_closeout/closeout.json", default={}) or {}
    d["stages"] = ctx.stage_state()
    d["retention"] = ctx.load("frds", "06_source-assignment-audit/retention.json", default={}) or {}
    d["transcoding"] = ctx.load("transcoding", "transcoded.json", default={}) or {}
    d["joint"] = ctx.load("matching", "03_match-records/joint-groups.json", default=[]) or []
    from .joint import incompatibility_records
    d["incompat"] = {"records": incompatibility_records(ctx)}
    return d


def _skipped_requests(ctx) -> dict:
    """Queued requests the operator marked skipped, counted by role."""
    from .llm.queue_tools import queue_dir
    from .util import read_json as _rj
    qd = queue_dir(ctx.project_dir, ctx.cfg["providers"].get("queue", {}).get("dir", "queue"))
    out: dict = {}
    for f in sorted((qd / "done").glob("*.skip.json")) if (qd / "done").exists() else []:
        key = f.name[:-len(".skip.json")]
        rec = _rj(qd / "pending" / f"{key}.json", default=None) or {}
        role = rec.get("role", "?")
        out[role] = out.get(role, 0) + 1
    return out


def _held_reasons(held: list[dict]) -> list[tuple[str, int]]:
    """Held witnesses grouped by a short reason."""
    c: dict = {}
    for h in held:
        r = str(h.get("held_reason", "held"))
        if "skipped by the queue operator" in r:
            r = "not audited (the audit request was not answered)"
        elif "no usable audit answer" in r:
            r = "not audited (no usable audit answer)"
        else:
            r = r.split(" - ")[0]
        c[r] = c.get(r, 0) + 1
    return sorted(c.items(), key=lambda x: -x[1])


def _lineage(d, wid) -> str:
    w = d["witnesses"].get(wid, {})
    v = d["vfrds"].get(w.get("vfrd_id"), {})
    q = d["questions"].get(w.get("qid"), {})
    quote = truncate_words(v.get("source_text", ""), 45)
    return (f"FRD `{w.get('vfrd_id', '?')}` · QID `{w.get('qid', '?')}` · source `{w.get('source_file', '?')}`"
            f" ({w.get('locator', '')})\n  - question: {truncate_words(q.get('text', ''), 35)}\n"
            f"  - source quote (checked against the file): \"{quote}\"")


# --------------------------------------------------------------------------- #
# evidence packets: a compact per-hypothesis reading of the witness registry
# (useful before, and independent of, complete coverage or crux results)
# --------------------------------------------------------------------------- #

_COMPLETE = ("EQUIVALENT", "WITNESS_ENTAILS_UNIT")
_PARTIAL = ("UNIT_ENTAILS_WITNESS", "PARTIALLY_COVERS")
_BASIS_RANK = {"HUMAN": 0, "AGREED": 1, "MODEL_ADJUDICATED": 2}


def evidence_packets(d: dict) -> list[dict]:
    """For every hypothesis: controlling claims, strongest objections, material
    qualifications and gaps, each tied to witnesses and their source passages."""
    by_h: dict = {}
    for r in d["relations"]:
        by_h.setdefault(r.get("hypothesis_id"), []).append(r)
    alloc = {}
    for ax, vec in ((d.get("assessment") or {}).get("allocations") or {}).items():
        alloc.update(vec or {})

    def wref(wid):
        w = d["witnesses"].get(wid, {})
        return {"witness_id": wid, "text": w.get("text", ""), "source_file": w.get("source_file", ""),
                "locator": w.get("locator", ""), "vfrd_id": w.get("vfrd_id", "")}

    def ranked(rows):
        return sorted(rows, key=lambda r: (_BASIS_RANK.get(r.get("basis"), 3), r["unit_id"], r["witness_id"]))

    def nearest(rows, unit_text, k=2):
        """The judged witnesses closest to a unit by word overlap, for a gap with no partial.

        This is a reading aid only: overlap is not a relation, and the line is labelled as such.
        It exists so that an uncovered part says what the nearest evidence says, instead of
        telling the reader that nothing in the registry is near it."""
        ut = set(tokens(unit_text))
        scored = []
        for r in rows:
            w = d["witnesses"].get(r["witness_id"], {})
            wt = set(tokens(w.get("text", "")))
            ov = len(ut & wt) / max(1, len(ut))
            if ov > 0:
                scored.append((ov, r, w))
        scored.sort(key=lambda x: (-x[0], x[1]["witness_id"]))
        return [{**wref(r["witness_id"]), "relation": r["final"], "basis": r.get("basis"),
                 "overlap": round(ov, 2)} for ov, r, w in scored[:k]]

    out = []
    for ax in d["frame"]["axes"]:
        for h in ax["hypotheses"]:
            hid = h["id"]
            units = [u for u in d["units"].values() if u["hypothesis_id"] == hid and u.get("active")]
            rows = by_h.get(hid, [])
            rel_of = {}
            for r in rows:
                rel_of.setdefault(r["unit_id"], []).append(r)
            cov = d["coverage"].get(hid, {})
            pk = {"hypothesis_id": hid, "axis_id": ax["axis_id"], "approval": ax.get("approval", ""),
                  "title": h.get("title", ""), "statement": h.get("statement", ""),
                  "coverage_status": cov.get("status", "n/a"),
                  "required_covered": f"{cov.get('units_covered', 0)}/{len(cov.get('required_units', []))}",
                  "allocation": alloc.get(hid), "controlling": [], "objections": [], "qualifications": [],
                  "corroboration": [], "gaps": []}
            for u in sorted(units, key=lambda u: u["unit_id"]):
                rs = rel_of.get(u["unit_id"], [])
                full = ranked([r for r in rs if r["final"] in _COMPLETE])
                part = ranked([r for r in rs if r["final"] in _PARTIAL])
                contra = ranked([r for r in rs if r["final"] == "CONTRADICTS"])
                base = {"unit_id": u["unit_id"], "unit_type": u["type"], "unit_text": u["text"]}
                if u["type"] == "REQUIRED_SUPPORT":
                    if full:
                        pk["controlling"].append({**base, "witnesses": [
                            {**wref(r["witness_id"]), "relation": r["final"], "basis": r.get("basis")} for r in full[:2]],
                            "more": max(0, len(full) - 2)})
                    else:
                        pk["gaps"].append({**base, "partly": [
                            {**wref(r["witness_id"]), "relation": r["final"], "basis": r.get("basis")} for r in part[:2]],
                            "nearest": nearest(rs, u["text"]) if not part else []})
                    for r in contra[:2]:
                        pk["objections"].append({**base, "kind": "contradicts a required part", "rank": 0,
                                                 **wref(r["witness_id"]), "basis": r.get("basis"),
                                                 "trace": r.get("trace", "")})
                elif u["type"] == "ADVERSE_TEST":
                    for r in full[:2]:
                        pk["objections"].append({**base, "kind": "meets an adverse test", "rank": 1,
                                                 **wref(r["witness_id"]), "basis": r.get("basis"),
                                                 "trace": r.get("trace", "")})
                elif u["type"] == "CONTEXTUAL_CONSTRAINT":
                    pk["qualifications"].append({**base, "supported_by": [wref(r["witness_id"]) for r in full[:2]],
                                                 "contradicted_by": [wref(r["witness_id"]) for r in contra[:2]]})
                elif u["type"] == "CORROBORATING_EXPECTATION":
                    if full or contra:
                        pk["corroboration"].append({**base, "met_by": [wref(r["witness_id"]) for r in full[:2]],
                                                    "contradicted_by": [wref(r["witness_id"]) for r in contra[:2]]})
                    for r in contra[:1]:
                        pk["objections"].append({**base, "kind": "contradicts an expected corollary", "rank": 2,
                                                 **wref(r["witness_id"]), "basis": r.get("basis"),
                                                 "trace": r.get("trace", "")})
            pk["objections"].sort(key=lambda o: (o["rank"], _BASIS_RANK.get(o.get("basis"), 3), o["unit_id"]))
            out.append(pk)
    return out


def render_packets(ctx, packets: list[dict]) -> str:
    def src(x):
        return f"`{x.get('source_file', '')}`" + (f" ({x['locator']})" if x.get("locator") else "")

    L = [f"# Evidence packets — {ctx.frame.get('title', 'investigation')}", "",
         f"Run `{ctx.run_id}` · generated {utcnow()}", "",
         "> One compact packet per hypothesis, read off the validated witness registry: what establishes each "
         "required part, the strongest evidence against, the conditions the hypothesis depends on, and what no "
         "witness establishes. Every witness traces to a validated FRD and a verbatim source quotation (open "
         "`report.html` and click the witness). Relations are the matching record's judgments "
         "(model or local engine, per the run's call log) unless marked HUMAN. "
         "**Best understood from this corpus and this run**; a listed witness is a faithful extract of its "
         "source, not a finding that the source is right.", ""]
    for pk in packets:
        al = f" · ACH_Eval allocation {pk['allocation']}" if pk.get("allocation") is not None else ""
        L += [f"## {pk['hypothesis_id']} — {pk['title']}", "",
              f"*Axis {pk['axis_id']} ({pk['approval'].replace('_', '-').lower()}) · coverage "
              f"{pk['coverage_status'].replace('_', ' ').lower()} · required parts established "
              f"{pk['required_covered']}{al}*", "",
              f"{truncate_words(pk['statement'], 60)}", ""]
        L.append("**Controlling claims** — witnesses that fully establish a required part")
        if not pk["controlling"]:
            L.append("- none")
        for c in pk["controlling"]:
            L.append(f"- `{c['unit_id']}` {truncate_words(c['unit_text'], 30)}")
            for w in c["witnesses"]:
                L.append(f"  - `{w['witness_id']}` [{w['relation']}, {w['basis']}]: {w['text']} — {src(w)}")
            if c.get("more"):
                L.append(f"  - *{c['more']} more in the registry*")
        L += ["", "**Strongest objections**"]
        if not pk["objections"]:
            L.append("- none found among the judged pairs")
        for o in pk["objections"][:5]:
            L.append(f"- `{o['witness_id']}` {o['kind']} `{o['unit_id']}` ({truncate_words(o['unit_text'], 22)}) "
                     f"[{o['basis']}]: {o['text']} — {src(o)}")
        L += ["", "**Material qualifications** — conditions the hypothesis depends on"]
        if not pk["qualifications"]:
            L.append("- none stated")
        for q in pk["qualifications"]:
            sup = ", ".join(f"`{w['witness_id']}`" for w in q["supported_by"]) or "no witness"
            con = ", ".join(f"`{w['witness_id']}`" for w in q["contradicted_by"])
            L.append(f"- `{q['unit_id']}` {truncate_words(q['unit_text'], 30)} — supported by {sup}"
                     + (f"; contradicted by {con}" if con else ""))
        if pk["corroboration"]:
            L += ["", "**Expected corollaries**"]
            for c in pk["corroboration"]:
                met = ", ".join(f"`{w['witness_id']}`" for w in c["met_by"]) or "not met"
                con = ", ".join(f"`{w['witness_id']}`" for w in c["contradicted_by"])
                L.append(f"- `{c['unit_id']}` {truncate_words(c['unit_text'], 25)} — met by {met}"
                         + (f"; contradicted by {con}" if con else ""))
        L += ["", "**Gaps** — required parts no witness establishes"]
        if not pk["gaps"]:
            L.append("- none")
        for g in pk["gaps"]:
            L.append(f"- `{g['unit_id']}` {truncate_words(g['unit_text'], 30)}"
                     + ("" if (g["partly"] or g.get("nearest")) else " — no witness in the registry establishes it"))
            for w in g["partly"]:
                L.append(f"  - partly: `{w['witness_id']}` [{w['relation'].replace('_', ' ').lower()}, "
                         f"{w.get('basis', '')}] {truncate_words(w['text'], 35)} — {src(w)}")
            for w in g.get("nearest", []):
                L.append(f"  - nearest judged evidence, **not a match** (word overlap {w['overlap']:.2f}, "
                         f"relation {w['relation'].replace('_', ' ').lower()}): `{w['witness_id']}` "
                         f"{truncate_words(w['text'], 35)} — {src(w)}")
        L.append("")
    return "\n".join(L)


def build_report(ctx, metrics: dict, summary_text: str | None, stamp: bool = True,
                 summary_record: bool = False) -> str:
    """``stamp=False`` leaves out the generation time, so the text given to the summary model is
    identical on every rerun (and its cached answer is reused).  ``summary_record=True`` builds the
    record the summary model reads; reader-only details are left out of it."""
    d = _load_all(ctx)
    frame = d["frame"]
    L = []
    L.append(f"# Crux report — {frame.get('title', 'investigation')}")
    L.append("")
    L.append(f"Run `{ctx.run_id}`" + (f" · generated {utcnow()}" if stamp else "") + " · harness claimreg")
    L.append("")
    L.append("> Everything below is **best understood from this corpus and this run**. The protocol does "
             "not guarantee that every relevant item was extracted from the corpus, and a crux result does "
             "not establish a witness's truth, authority, independence or dispositive weight.")
    L.append("")
    if summary_text:
        L += ["## Analyst summary (generated from the run record; adds no evidence)", "", summary_text, ""]
    # pipeline table
    m = metrics
    L += ["## The run at a glance", "",
          "| Stage | Result |", "|---|---|",
          f"| Corpus | {len(ctx.corpus.filenames)} sources, {m['corpus_bytes']:,} bytes |",
          f"| Discovery | {len(d['questions'])} questions, {m['responses_usable']} usable answers "
          f"({d['closeout'].get('status', 'n/a')}) |",
          f"| FRDs | {m['frd_candidates']} candidates → {m['frds_retained']} retained READY |",
          f"| Witnesses | {m['witnesses_released']} released, {len(d['held'])} held |",
          f"| Matching | {d['match_summary'].get('pairs_assessed', 0)} pairs judged "
          f"({d['match_summary'].get('agreed', 0)} agreed, {d['match_summary'].get('model_adjudicated', 0)} "
          f"model-adjudicated) |",
          f"| Coverage | " + "; ".join(f"{h}: {c['status'].replace('_', ' ').lower()} "
                                       f"({c.get('units_covered', 0)}/{len(c.get('required_units', []))} units, "
                                       f"{len(c.get('sets', []))} sets)" for h, c in d["coverage"].items()) + " |",
          f"| Crux | {len(d['crux'].get('candidates', []))} candidates; "
          f"{len(d['crux'].get('diagnostic_witnesses', []))} diagnostic witnesses (extended review) |", ""]
    # crux candidates
    L += ["## Crux candidates", ""]
    cands = d["crux"].get("candidates", [])
    if not cands:
        L += ["No witness qualified as a crux candidate against any rival. A crux candidate must belong to a "
              "deletion-minimal coverage set of its home hypothesis; see the coverage section for which "
              "hypotheses reached complete coverage and which required parts remain uncovered.", ""]
    for c in cands[:12]:
        w = d["witnesses"].get(c["witness_id"], {})
        L += [f"### {c['witness_id']} — home {c['home']}, defeats {', '.join(c['defeats'])}", "",
              f"> {w.get('text', '')}", ""]
        for r in c["defeats"]:
            t = next((x for x in d["tests"] if x["witness_id"] == c["witness_id"] and x["rival"] == r), None)
            if not t:
                continue
            hits = t["t1_certificate"].get("conflicting_rule_bundle", [])
            for h in hits[:3]:
                u = d["units"].get(h["unit_id"], {})
                L.append(f"- **vs {r}** — T1 FAIL: conflicts with `{h['unit_id']}` ({h['unit_group']}): "
                         f"\"{truncate_words(u.get('text', ''), 40)}\" — trace: {truncate_words(h.get('trace', ''), 45)} "
                         f"[{h.get('basis', '')}]")
            t2 = t["t2_certificate"]
            forb = [x["unit_id"] for x in t2.get("required_units_forbidden", [])]
            blk = [x["unit_id"] for x in t2.get("required_units_blocked_by_incompatibility", [])]
            L.append(f"  - T2 FAIL: required units forbidden {forb or 'none'}; blocked by incompatibility "
                     f"{blk or 'none'}")
        L += ["", "- Lineage: " + _lineage(d, c["witness_id"]), ""]
    if len(cands) > 12:
        L += [f"*{len(cands) - 12} further candidates are listed in `09_CRUX/05_candidates/crux-candidates.json`.*", ""]
    # coverage
    L += ["## Coverage of each hypothesis", ""]
    for ax in frame["axes"]:
        L.append(f"**Axis {ax['axis_id']}** ({ax.get('approval', 'UNKNOWN').replace('_', '-').lower()}): "
                 f"{truncate_words(ax.get('question', ''), 40)}")
        L.append("")
        for h in ax["hypotheses"]:
            c = d["coverage"].get(h["id"], {})
            L.append(f"- **{h['id']}** — {c.get('status', 'n/a')}; required units covered "
                     f"{c.get('units_covered', 0)}/{len(c.get('required_units', []))}; "
                     f"{len(c.get('sets', []))} deletion-minimal set(s) [{c.get('search_status', '')}]")
            for uid in c.get("required_units", []):
                opts = c.get("options", {}).get(uid)
                if not opts:
                    L.append(f"  - uncovered `{uid}`: {truncate_words(d['units'].get(uid, {}).get('text', ''), 35)}")
                elif not summary_record:
                    basis = {(r["witness_id"], r["unit_id"]): r.get("basis", "") for r in d["relations"]}
                    ws = ", ".join(" + ".join(f"`{w}`" for w in o["witnesses"])
                                   + (f" [{basis.get((o['witnesses'][0], uid), 'joint group')}]"
                                      if len(o["witnesses"]) == 1 else " [joint group]") for o in opts[:3])
                    L.append(f"  - covered `{uid}` by {ws}"
                             + (f" and {len(opts) - 3} more" if len(opts) > 3 else ""))
            if c.get("sets"):
                s = c["sets"][0]
                L.append(f"  - example set `{s['set_id']}`: " + ", ".join(f"`{w}`" for w in s["witnesses"]))
            ev = [u for u in d["units"].values() if u["hypothesis_id"] == h["id"] and u["type"] == "EVALUATIVE_JUDGMENT"]
            if ev:
                L.append(f"  - evaluative judgments left to the analyst: " +
                         "; ".join(truncate_words(u["text"], 18) for u in ev[:3]))
        L.append("")
    # diagnostic
    diag = d["crux"].get("diagnostic_witnesses", [])
    if diag:
        L += ["## Diagnostic witnesses (extended review, spec Route B — not crux candidates)", "",
              "These witnesses fully cover at least one required part of a hypothesis that lacks complete "
              "coverage, and fail both portability tests against a rival. They show where the evidence "
              "discriminates even though no complete coverage set exists.", ""]
        seen = set()
        for x in diag:
            if len(seen) >= int(ctx.cfg["crux"].get("diagnostic_top_n", 15)):
                break
            key = (x["witness_id"], x["rival"])
            if key in seen:
                continue
            seen.add(key)
            w = d["witnesses"].get(x["witness_id"], {})
            hits = x["t1_certificate"].get("conflicting_rule_bundle", [])
            L.append(f"- `{x['witness_id']}` (supports {x['home']}; conflicts with {x['rival']} unit "
                     f"{', '.join(h['unit_id'] for h in hits[:2])}): {truncate_words(w.get('text', ''), 45)}")
        L.append("")
    # assessment
    a = d["assessment"]
    if a.get("allocations"):
        L += ["## Final assessment (ACH_Eval on the validated witness registry)", "",
              "Uncalibrated working judgments, not probabilities; they answer a different question from "
              "crux identification.", ""]
        for ax, vec in a["allocations"].items():
            L.append(f"- Axis {ax}: " + ", ".join(f"{k} {v}/{a.get('gauge', '')}" for k, v in vec.items())
                     + (f" — basis/confidence: {a.get('basis_confidence', {}).get(ax, '')}" if a.get("basis_confidence") else ""))
            for drv in (a.get("drivers", {}) or {}).get(ax, [])[:3]:
                L.append(f"  - driver: {truncate_words(str(drv), 40)}")
            if (a.get("strongest_objection") or {}).get(ax):
                L.append(f"  - strongest objection: {truncate_words(a['strongest_objection'][ax], 45)}")
        L.append("")
    # metrics
    L += ["## Compression against the Problems-note targets", "", "| Metric | Value | Target | Met |",
          "|---|---|---|---|"]
    for t in metrics["targets"]:
        met = "n/a" if t["met"] is None else ("yes" if t["met"] else "no")
        L.append(f"| {t['metric']} | {t['value']} | {t['target']} | {met} |")
    L.append("")
    # limitations
    q = d["qualification"]
    ms = d["match_summary"]
    lim = [
        f"Engines that answered calls in this run: {', '.join(providers_used(ctx)) or 'not recorded'} "
        f"(see `00_RUN-CONTROL/model-and-human-decisions/llm-calls.jsonl`). A local engine judges by "
        f"explicit lexical and structural rules, not model understanding; every relation is labelled "
        f"with its basis and can be overruled.",
        f"Semantic matching is judged by the configured matcher. {ms.get('agreed', 0)} relations were approved "
        f"by agreement of two independent passes; {ms.get('model_adjudicated', 0)} disagreements were settled "
        f"by a third independent context (not a human); {ms.get('disputed_abstain', 0)} remain ABSTAIN"
        + (f"; {ms.get('missing_both_passes')} pairs got no judgment from either pass"
           if ms.get('missing_both_passes') else "")
        + ((f"; {ms.get('one_pass_only')} pairs were judged by one pass only (the other pass's batch was not "
            f"answered) and count as ABSTAIN until a human confirms them"
            if ctx.cfg['matching'].get('one_pass_policy', 'abstain') != 'accept' else
            f"; {ms.get('one_pass_only')} pairs were judged by ONE pass only (the other pass's batch was not "
            f"answered); under the declared one_pass_policy=accept their single judgment is used and labelled "
            f"ONE_PASS_ONLY wherever it appears") if ms.get('one_pass_only') else "")
        + (f"; {sum(1 for r in d['relations'] if r.get('basis') == 'HUMAN')} relations were set by a human reviewer"
           if any(r.get('basis') == 'HUMAN' for r in d['relations']) else "") + ".",
        f"{ms.get('pairs_not_assessed_prefilter', 0)} witness-unit pairs were outside the lexical shortlist and "
        f"count as no relation; missed matches are the main source of false cruxes (spec 29.1). Every witness "
        f"used in crux testing was judged against every rival unit.",
        f"Matcher qualification: pass A {q.get('pass_a_correct', '?')}/{q.get('fixtures', '?')}, pass B "
        f"{q.get('pass_b_correct', '?')}/{q.get('fixtures', '?')} fixtures; unqualified patterns: "
        f"{', '.join(q.get('unqualified_patterns', [])) or 'none'}.",
        f"Language layer: {d['transcoding'].get('mode', 'off')}"
        + (" (identity transcoder: matching used raw witness and unit text)." if d['transcoding'].get('mode', 'off') == 'off'
           else f"; {sum(1 for i in d['transcoding'].get('items', []) if i.get('status') == 'REVIEW')} items withheld as REVIEW."),
        f"Witness ceiling: {ctx.cfg['witness']['raw_ceiling']} words, with "
        f"{sum(1 for w in d['witnesses'].values() if w.get('ceiling_exception'))} recorded per-witness "
        f"exceptions up to {ctx.cfg['witness']['exception_ceiling']} words; {len(d['held'])} witnesses held"
        + (" (" + "; ".join(f"{n} {why}" for why, n in _held_reasons(d['held'])) + ")" if d['held'] else "") + ".",
        "Incompatibility approval uses the harness definition (two passes agree on same-quantity conflict or "
        f"opposite polarity at the same scope): {sum(1 for r in d['incompat'].get('records', []) if r.get('approved'))} approved.",
        "Coverage units are an internal representation derived by the configured engine from the "
        "human-written hypotheses; each unit's anchor quotation was checked verbatim against the frozen text.",
    ]
    for ax in frame["axes"]:
        if ax.get("approval") == "TEST_ONLY":
            lim.append(f"Axis {ax['axis_id']} is marked TEST-ONLY in the header (not human-approved).")
    imported = [k for k, v in d["stages"].items() if str(v.get("status")) == "imported"]
    if imported:
        lim.append("Stages imported from an earlier run rather than executed here: " + ", ".join(imported) + ".")
    if not summary_record:
        from .matching import rejected_human_decisions
        rej = rejected_human_decisions(ctx)
        if rej:
            lim.append(f"{len(rej)} human relation decision(s) were ignored because they name a witness or unit "
                       f"this run does not have: " + "; ".join(f"{r['witness_id']} x {r['unit_id']} "
                                                                f"({r['rejected_because']})" for r in rej[:5]) + ".")
        sk = _skipped_requests(ctx)
        if sk:
            lim.append(f"{sum(sk.values())} queued model requests were never answered and were marked skipped "
                       f"(by role: " + ", ".join(f"{k} {v}" for k, v in sorted(sk.items())) + "). Each counts as a "
                       "failed call: nothing was invented in its place. Reasons are in the project's "
                       "`queue/done/*.skip.json` files and `queue/OPERATOR-NOTES.md`.")
    L += ["## Limitations and disclosures", ""] + [f"- {x}" for x in lim] + [""]
    L += ["## Audit trail", "",
          "- `EVIDENCE-PACKETS.md` in this folder: per hypothesis, the controlling claims, strongest objections, "
          "material qualifications and gaps, each tied to witnesses and source files.",
          "- `report.html` in this folder: click any crux or witness to see its FRD, the verbatim source quote, "
          "the producing question and the Archivist answer.",
          "- Machine records: `07_MATCHING/03_match-records/relations.json`, `08_COVERAGE/coverage.json`, "
          "`09_CRUX/03_portability-tests/tests.json`, `00_RUN-CONTROL/model-and-human-decisions/llm-calls.jsonl`.",
          "- Every model call's exact prompt and answer is in the project's `cache/llm` folder, keyed by the "
          "call log.", ""]
    text = "\n".join(L)
    maxw = int(ctx.cfg["report"].get("max_words", 3900))
    toks = list(re.finditer(r"\S+", text))
    if len(toks) > maxw - 15:                     # leave room for the truncation note itself
        text = (text[:toks[maxw - 16].end()]
                + "\n\n*(Report truncated at the word limit; see the JSON records.)*\n")
    return text


def _html(ctx, d, report_md: str, metrics: dict) -> str:
    def slim_v(v):
        return {k: v.get(k) for k in ("vfrd_id", "frd_id", "qid", "source_file", "citation", "claim",
                                      "source_text", "verdict", "verdict_explanation", "quote_check",
                                      "evidence_label")}
    rel = [r for r in d["relations"] if r.get("final") not in ("NO_SEMANTIC_RELATION",)]
    data = {
        "run": ctx.run_id, "frame": d["frame"], "units": list(d["units"].values()),
        "witnesses": list(d["witnesses"].values()), "held": d["held"],
        "vfrds": [slim_v(v) for v in d["vfrds"].values()],
        "questions": [{k: q.get(k) for k in ("qid", "round", "text", "sources_as_sent", "status")}
                      for q in d["questions"].values()],
        "responses": [{"qid": r["qid"], "usable": r.get("usable"), "cited": r.get("cited_sources", []),
                       "text": r.get("text", "")} for r in d["responses"].values()],
        "coverage": d["coverage"], "crux": d["crux"], "relations": rel,
        "tests": [t for t in d["tests"] if t.get("tests_failed")], "metrics": metrics,
        "assessment": d["assessment"], "report": report_md, "packets": d.get("packets", []),
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return HTML_TEMPLATE.replace("__TITLE__", html.escape(d["frame"].get("title", "Claim Registry run"))) \
        .replace("__DATA__", payload)


def report_stage(ctx) -> dict:
    metrics = compute_metrics(ctx)
    ctx.save("reports", "metrics.json", metrics, "metrics")
    summary_text = None
    if ctx.cfg["report"].get("llm_summary", True):
        d = _load_all(ctx)
        record = build_report(ctx, metrics, None, stamp=False, summary_record=True)
        system, user, _ = ctx.prompts.render("report_summary.md", MAX_WORDS=350, RECORD=truncate_words(record, 3500))
        from .llm.base import ProviderError
        try:
            res = ctx.llm.call(LLMRequest(role="reporter", system=system, user=user, tag="report-summary",
                                          meta={"record": record, "metrics": metrics,
                                                "coverage": d["coverage"],
                                                "quest": (ctx.stage_state().get("quest", {}) or {}).get(
                                                    "summary", {}),
                                                "crux": {"candidates": len((d["crux"] or {}).get(
                                                    "candidates", []))}}))
        except ProviderError as e:
            if "skipped by the queue operator" not in str(e):
                raise
            res = None
        if res is not None and isinstance(res.parsed, dict):
            summary_text = str(res.parsed.get("summary", "")).strip() or None
    md = build_report(ctx, metrics, summary_text)
    atomic_write_text(ctx.p("reports", "CRUX-REPORT.md"), md)
    ctx.register(ctx.p("reports", "CRUX-REPORT.md"), "crux-report")
    d = _load_all(ctx)
    packets = evidence_packets(d)
    ctx.save("reports", "evidence-packets.json", packets, "evidence-packets")
    atomic_write_text(ctx.p("reports", "EVIDENCE-PACKETS.md"), render_packets(ctx, packets))
    ctx.register(ctx.p("reports", "EVIDENCE-PACKETS.md"), "evidence-packets-md")
    d["packets"] = packets
    atomic_write_text(ctx.p("reports", "report.html"), _html(ctx, d, md, metrics))
    ctx.register(ctx.p("reports", "report.html"), "audit-browser")
    return {"report_words": word_count(md), "crux_candidates": len(d["crux"].get("candidates", []))}


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — Claim Registry audit browser</title>
<style>
:root{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--line:#dedbd3;--acc:#7a3e12;--card:#fff;--ok:#2f6b3a;--bad:#9b2c2c;--warn:#8a6d1a}
@media (prefers-color-scheme:dark){:root{--bg:#161614;--fg:#ecebe6;--mut:#a3a199;--line:#33322e;--acc:#e0a46b;--card:#1f1e1b;--ok:#7fc28d;--bad:#e58b8b;--warn:#d9bd62}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 Georgia,'Iowan Old Style',serif}
header{padding:20px 24px;border-bottom:1px solid var(--line)}h1{font-size:22px;margin:0 0 4px}small,.mut{color:var(--mut)}
nav{display:flex;gap:4px;flex-wrap:wrap;padding:8px 24px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg)}
nav button{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--fg);padding:5px 12px;border-radius:14px;cursor:pointer}
nav button.on{background:var(--acc);color:var(--bg);border-color:var(--acc)}
main{padding:16px 24px;max-width:1100px}.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:10px 0}
.k{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}.tag{display:inline-block;font:12px ui-monospace,monospace;padding:1px 6px;border-radius:9px;border:1px solid var(--line);margin-right:4px}
.ok{color:var(--ok)}.bad{color:var(--bad)}.warn{color:var(--warn)}a{color:var(--acc);cursor:pointer;text-decoration:underline}
blockquote{margin:6px 0;padding:4px 10px;border-left:3px solid var(--acc);background:rgba(127,127,127,.06)}
pre{white-space:pre-wrap;font:13px/1.45 ui-monospace,Menlo,Consolas,monospace;background:rgba(127,127,127,.07);padding:10px;border-radius:6px;max-height:420px;overflow:auto}
input{font:inherit;padding:6px 10px;width:100%;max-width:420px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg)}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top;font-size:14px}
#detail{position:fixed;right:0;top:0;bottom:0;width:min(560px,100%);background:var(--bg);border-left:1px solid var(--line);overflow:auto;padding:16px;display:none;box-shadow:-6px 0 18px rgba(0,0,0,.15)}
#detail .x{float:right;cursor:pointer;font-size:20px}
</style></head><body>
<header><h1>__TITLE__</h1><small id="sub"></small></header>
<nav id="nav"></nav><main id="main"></main><div id="detail"><span class="x" onclick="hide()">×</span><div id="dbody"></div></div>
<script>
const D=__DATA__;const REPORT=D.report||'';
const W=Object.fromEntries(D.witnesses.concat(D.held).map(w=>[w.witness_id,w]));const V=Object.fromEntries(D.vfrds.map(v=>[v.vfrd_id,v]));
const Q=Object.fromEntries(D.questions.map(q=>[q.qid,q]));const R=Object.fromEntries(D.responses.map(r=>[r.qid,r]));const U=Object.fromEntries(D.units.map(u=>[u.unit_id,u]));
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
document.getElementById('sub').textContent=`Run ${D.run} · ${D.witnesses.length} released witnesses · ${D.vfrds.length} validated FRDs · ${D.questions.length} questions`;
const tabs={Report:showReport,Evidence:showP,Cruxes:showCrux,Coverage:showCov,Witnesses:showW,FRDs:showF,Questions:showQ,Metrics:showM};
const nav=document.getElementById('nav');for(const t in tabs){const b=document.createElement('button');b.textContent=t;b.onclick=()=>{[...nav.children].forEach(x=>x.classList.remove('on'));b.classList.add('on');tabs[t]()};nav.appendChild(b)}nav.children[0].click();
function M(h){document.getElementById('main').innerHTML=h}
function hide(){document.getElementById('detail').style.display='none'}
function detail(h){document.getElementById('dbody').innerHTML=h;document.getElementById('detail').style.display='block'}
function wl(id){return `<a onclick="openW('${id}')" class="k">${esc(id)}</a>`}
function showReport(){M(`<div class="card"><pre>${esc(REPORT)}</pre></div>`)}
function wit(w){return `${wl(w.witness_id)}${w.relation?` <small class="mut">${esc(w.relation)} · ${esc(w.basis)}</small>`:''}<blockquote>${esc(w.text)}</blockquote><small class="mut">${esc(w.source_file)}${w.locator?' · '+esc(w.locator):''}</small>`}
function showP(){M((D.packets||[]).map(p=>`<div class="card"><h2>${esc(p.hypothesis_id)} <small class="mut">${esc(p.title)}</small></h2><p class="mut">Axis ${esc(p.axis_id)} (${esc(p.approval)}) · coverage ${esc(p.coverage_status)} · required parts established ${esc(p.required_covered)}${p.allocation!=null?' · allocation '+esc(p.allocation):''}</p><p>${esc(p.statement)}</p>
<h4>Controlling claims</h4>${p.controlling.length?p.controlling.map(c=>`<div><span class="k">${esc(c.unit_id)}</span> ${esc(c.unit_text)}${c.witnesses.map(wit).join('')}</div>`).join(''):'<p class="mut">none</p>'}
<h4>Strongest objections</h4>${p.objections.length?p.objections.slice(0,5).map(o=>`<div><span class="tag bad">${esc(o.kind)}</span> <span class="k">${esc(o.unit_id)}</span> ${esc(o.unit_text)}${wit(o)}</div>`).join(''):'<p class="mut">none found among judged pairs</p>'}
<h4>Material qualifications</h4>${p.qualifications.length?p.qualifications.map(q=>`<div><span class="k">${esc(q.unit_id)}</span> ${esc(q.unit_text)} — supported by ${q.supported_by.map(w=>wl(w.witness_id)).join(', ')||'<span class="warn">no witness</span>'}${q.contradicted_by.length?' · contradicted by '+q.contradicted_by.map(w=>wl(w.witness_id)).join(', '):''}</div>`).join(''):'<p class="mut">none stated</p>'}
<h4>Gaps</h4>${p.gaps.length?p.gaps.map(g=>`<div><span class="k">${esc(g.unit_id)}</span> ${esc(g.unit_text)} ${g.partly.length?'— partly: '+g.partly.map(w=>wl(w.witness_id)).join(', '):'<span class="bad">— nothing addresses it</span>'}</div>`).join(''):'<p class="mut">none</p>'}</div>`).join('')||'<p class="mut">No packets.</p>')}
function showCrux(){const c=D.crux.candidates||[];const g=D.crux.diagnostic_witnesses||[];
M(`<h2>Crux candidates (${c.length})</h2>`+(c.length?c.map(x=>`<div class="card">${wl(x.witness_id)} <span class="tag">home ${esc(x.home)}</span> defeats ${x.defeats.map(r=>`<span class="tag bad">${esc(r)}</span>`).join('')}<blockquote>${esc((W[x.witness_id]||{}).text)}</blockquote></div>`).join(''):'<p class="mut">None. See Coverage for uncovered required units.</p>')+
`<h2>Diagnostic witnesses — extended review (${g.length})</h2>`+g.slice(0,80).map(x=>`<div class="card">${wl(x.witness_id)} <span class="tag">supports ${esc(x.home)}</span><span class="tag bad">vs ${esc(x.rival)}</span><div class="mut">T1: ${(x.t1_certificate.conflicting_rule_bundle||[]).map(h=>esc(h.unit_id+' '+h.relation)).join('; ')}</div><blockquote>${esc((W[x.witness_id]||{}).text)}</blockquote></div>`).join(''))}
function showCov(){let h='';for(const ax of D.frame.axes){h+=`<h2>Axis ${esc(ax.axis_id)} <small class="mut">${esc(ax.approval)}</small></h2><p>${esc(ax.question)}</p>`;for(const hy of ax.hypotheses){const c=D.coverage[hy.id]||{};h+=`<div class="card"><b>${esc(hy.id)}</b> — <span class="${c.status=='COMPLETE'?'ok':'bad'}">${esc(c.status)}</span> · ${c.units_covered||0}/${(c.required_units||[]).length} required units covered · ${(c.sets||[]).length} sets <small>${esc(c.search_status||'')}</small><p class="mut">${esc(hy.statement)}</p><table><tr><th>unit</th><th>type</th><th>options</th></tr>`;for(const u of D.units.filter(u=>u.hypothesis_id==hy.id)){const o=(c.options||{})[u.unit_id]||[];h+=`<tr><td><span class="k">${esc(u.unit_id)}</span><br>${esc(u.text)}${u.active?'':' <span class="warn">(inactive: '+esc(u.inactive_reason)+')</span>'}</td><td class="k">${esc(u.type)}</td><td>${u.type=='REQUIRED_SUPPORT'?(o.length?o.map(x=>x.witnesses.map(wl).join(' + ')).join('<br>'):'<span class="bad">uncovered</span>'):''}</td></tr>`}h+=`</table>`+((c.sets||[]).slice(0,5).map(s=>`<div class="mut">set ${esc(s.set_id)}: ${s.witnesses.map(wl).join(', ')}</div>`).join(''))+`</div>`}}M(h)}
function showW(){M(`<input id="f" placeholder="filter witnesses…" oninput="fw()"><div id="wl"></div>`);fw()}
function fw(){const q=(document.getElementById('f').value||'').toLowerCase();document.getElementById('wl').innerHTML=Object.values(W).filter(w=>!q||JSON.stringify(w).toLowerCase().includes(q)).map(w=>`<div class="card">${wl(w.witness_id)} <span class="tag ${w.status=='RELEASED'?'ok':'warn'}">${esc(w.status)}</span>${w.ceiling_exception?'<span class="tag warn">ceiling exception</span>':''}<blockquote>${esc(w.text)}</blockquote><small class="mut">${esc(w.source_file)} · ${esc(w.qid)}</small></div>`).join('')}
function showF(){M(D.vfrds.map(v=>`<div class="card"><a onclick="openF('${v.vfrd_id}')" class="k">${esc(v.vfrd_id)}</a> <span class="tag">${esc(v.verdict)}</span> <span class="tag ${v.quote_check&&v.quote_check.found?'ok':'bad'}">quote ${v.quote_check&&v.quote_check.found?'verified':'unverified'}</span><p>${esc(v.claim)}</p></div>`).join(''))}
function showQ(){M(D.questions.map(q=>`<div class="card"><a onclick="openQ('${q.qid}')" class="k">${esc(q.qid)}</a> <small class="mut">round ${q.round} · ${esc((q.sources_as_sent||[]).join(', '))}</small><p>${esc(q.text)}</p></div>`).join(''))}
function showM(){const m=D.metrics;M(`<table><tr><th>metric</th><th>value</th><th>target</th><th>met</th></tr>`+m.targets.map(t=>`<tr><td>${esc(t.metric)}</td><td>${esc(t.value)}</td><td>${esc(t.target)}</td><td class="${t.met==null?'mut':(t.met?'ok':'bad')}">${t.met==null?'n/a':(t.met?'yes':'no')}</td></tr>`).join('')+`</table><pre>${esc(JSON.stringify(Object.fromEntries(Object.entries(m).filter(([k])=>k!='targets')),null,1))}</pre>`)}
function openW(id){const w=W[id]||{};const v=V[w.vfrd_id]||{};const rels=D.relations.filter(r=>r.witness_id==id);const tests=D.tests.filter(t=>t.witness_id==id);
detail(`<h3 class="k">${esc(id)}</h3><blockquote>${esc(w.text)}</blockquote><small class="mut">${w.words} words · ceiling ${w.ceiling} · audit ${esc(w.audit_verdict)}</small>
<h4>Parent FRD <a onclick="openF('${w.vfrd_id}')">${esc(w.vfrd_id)}</a></h4><p>${esc(v.claim)}</p><h4>Verbatim source text (${esc(w.source_file)})</h4><blockquote>${esc(v.source_text)}</blockquote>
<h4>Producing question <a onclick="openQ('${w.qid}')">${esc(w.qid)}</a></h4><p>${esc((Q[w.qid]||{}).text)}</p>
<h4>Match relations (${rels.length})</h4>${rels.map(r=>`<div><span class="k">${esc(r.unit_id)}</span> <b>${esc(r.final)}</b> <small class="mut">${esc(r.basis)}</small><br><small>${esc(r.trace)}</small></div>`).join('')}
<h4>Portability tests with a failure (${tests.length})</h4>${tests.map(t=>`<div>${esc(t.home)} vs ${esc(t.rival)}: T1 <b>${esc(t.t1)}</b>, T2 <b>${esc(t.t2)}</b>${t.crux?' <span class="bad">CRUX</span>':''}</div>`).join('')}`)}
function openF(id){const v=V[id]||{};detail(`<h3 class="k">${esc(id)}</h3><p><span class="tag">${esc(v.verdict)}</span> ${esc(v.evidence_label)}</p><h4>Claim</h4><p>${esc(v.claim)}</p><h4>Citation</h4><p>${esc(v.source_file)} — ${esc((v.citation||{}).locator)}</p><h4>Source text (mechanically checked: ${esc(JSON.stringify(v.quote_check))})</h4><blockquote>${esc(v.source_text)}</blockquote><h4>Validator explanation</h4><p>${esc(v.verdict_explanation)}</p><p>QID: <a onclick="openQ('${v.qid}')">${esc(v.qid)}</a></p>`)}
function openQ(id){const q=Q[id]||{};const r=R[id]||{};detail(`<h3 class="k">${esc(id)}</h3><h4>Question</h4><p>${esc(q.text)}</p><h4>Archivist answer ${r.usable?'':'(not usable)'}</h4><pre>${esc(r.text)}</pre><small class="mut">cited: ${esc((r.cited||[]).join(', '))}</small>`)}
</script></body></html>
"""
