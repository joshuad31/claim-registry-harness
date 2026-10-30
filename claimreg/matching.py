"""Phase V - semantic matching (spec 28, 28.1, 28.2).

* Two structurally different review passes (A: unit-centric; B: element-wise,
  reversed witness order) judge every shortlisted witness-unit pair.  They run
  in separate contexts and never see each other's output.
* Agreement -> approved relation (basis AGREED).
* Disagreement -> ``matching.dispute_policy``:
    - "adjudicate": a third, separate context decides or abstains
      (basis MODEL_ADJUDICATED - reported as such, never as agreement);
    - "abstain": the pair is ABSTAIN (basis DISPUTED), the spec's default when
      no human reviewer is available.
* Pairs outside the shortlist are NOT_ASSESSED (treated as no relation for
  coverage, and counted and disclosed in the report).  Crux identification
  later runs "completion matching" so that every witness it relies on has been
  judged against every rival unit (no prefilter there).
* Matcher qualification runs the production prompts on adversarial fixtures
  and reports results pattern by pattern.
"""

from __future__ import annotations

import random
import re

from .llm.base import LLMRequest
from .llm.jsonparse import as_list
from .util import chunked, read_json, tokens, truncate_words, utcnow

RELATIONS = ("EQUIVALENT", "WITNESS_ENTAILS_UNIT", "UNIT_ENTAILS_WITNESS", "PARTIALLY_COVERS",
             "CONTRADICTS", "NO_SEMANTIC_RELATION", "ABSTAIN")
COMPLETE = ("EQUIVALENT", "WITNESS_ENTAILS_UNIT")
PARTIAL = ("UNIT_ENTAILS_WITNESS", "PARTIALLY_COVERS")

FIXTURES = [
    # (id, pattern, unit, witness, accepted relations)
    ("FX-01", "actor_object_reversal", "Drug A reduced fibrosis in obstructed rat bladders.",
     "Fibrosis in obstructed rat bladders reduced drug A exposure.",
     {"NO_SEMANTIC_RELATION", "CONTRADICTS", "ABSTAIN"}),
    ("FX-02", "actor_object_reversal", "Tamsulosin improved maximum flow rate in men with BPH.",
     "Improvements in maximum flow rate in men with BPH increased tamsulosin absorption.",
     {"NO_SEMANTIC_RELATION", "CONTRADICTS", "ABSTAIN"}),
    ("FX-03", "active_passive_actor_kept", "Shirazi measured detrusor tension after four weeks.",
     "Detrusor tension was measured by Shirazi after four weeks.", {"EQUIVALENT"}),
    ("FX-04", "active_passive_actor_kept", "The trial randomized sixty men to two treatment arms.",
     "Sixty men were randomized to two treatment arms by the trial investigators.",
     {"EQUIVALENT", "WITNESS_ENTAILS_UNIT"}),
    ("FX-05", "affirmation_vs_denial", "Drug A increased evoked detrusor tension compared with control.",
     "Drug A produced no significant increase in evoked detrusor tension compared with control.",
     {"CONTRADICTS"}),
    ("FX-06", "affirmation_vs_denial", "Carbachol-induced tension did not differ between the groups.",
     "Carbachol-induced tension differed significantly between the groups.", {"CONTRADICTS"}),
    ("FX-07", "possibility_vs_necessity", "Drug A must improve voiding in this cohort.",
     "The authors suggest that drug A may improve voiding in this cohort.",
     {"UNIT_ENTAILS_WITNESS", "PARTIALLY_COVERS"}),
    ("FX-08", "possibility_vs_necessity",
     "Drug A can reach human bladder tissue at clinically attainable oral doses.",
     "After standard clinical oral doses, drug A was measured in human bladder tissue samples.",
     {"WITNESS_ENTAILS_UNIT", "EQUIVALENT"}),
    ("FX-09", "report_vs_assertion", "Drug A reduces fibrosis in obstructed bladders.",
     "A narrative review reports, without new data, that drug A reduces fibrosis in obstructed bladders.",
     {"PARTIALLY_COVERS", "UNIT_ENTAILS_WITNESS"}),
    ("FX-10", "report_vs_assertion",
     "Chung's review reports that drug A reduces fibrosis in obstructed bladders.",
     "According to Chung's review, drug A reduces fibrosis in obstructed bladders.", {"EQUIVALENT"}),
    ("FX-11", "condition_vs_unconditional", "Drug A reaches the detrusor and contractility improves.",
     "If drug A reaches the detrusor, contractility may improve.",
     {"PARTIALLY_COVERS", "UNIT_ENTAILS_WITNESS"}),
    ("FX-12", "condition_vs_unconditional", "In obstructed rats, drug A increased evoked tension.",
     "Drug A increased evoked tension in obstructed rats.", {"EQUIVALENT"}),
    ("FX-13", "high_overlap_changed_roles",
     "Drug A plus tamsulosin increased flow more than tamsulosin alone in men with BPH.",
     "Tamsulosin plus placebo increased flow more than drug A alone in men with BPH.",
     {"NO_SEMANTIC_RELATION", "ABSTAIN", "PARTIALLY_COVERS"}),
    ("FX-14", "high_overlap_changed_roles", "Drug A 400 mg three times daily increased maximum flow rate.",
     "Drug A 400 mg once daily increased maximum flow rate.", {"PARTIALLY_COVERS", "NO_SEMANTIC_RELATION",
                                                               "ABSTAIN"}),
    ("FX-15", "must_keep_reordered", "Paruresis is characterized by difficulty urinating when others are present.",
     "Difficulty urinating when others are present characterizes paruresis.", {"EQUIVALENT"}),
    ("FX-16", "must_keep_specific_entails_general", "Drug A improved detrusor contractility in obstructed rats.",
     "After four weeks of oral dosing, drug A improved detrusor contractility in obstructed rats (12 per group).",
     {"WITNESS_ENTAILS_UNIT", "EQUIVALENT"}),
    ("FX-17", "unrelated", "Drug A reduced collagen deposition in obstructed rat bladders.",
     "Beta-blockers reduce mortality after myocardial infarction.", {"NO_SEMANTIC_RELATION"}),
    ("FX-18", "unrelated", "Adherence was assessed by returned diaries.",
     "Peak plasma concentration occurred at two hours.", {"NO_SEMANTIC_RELATION"}),
    ("FX-19", "scope_transfer", "Drug A improves voiding function in men with BPH.",
     "Drug A improved detrusor contractility in obstructed rats.", {"PARTIALLY_COVERS", "NO_SEMANTIC_RELATION"}),
    ("FX-20", "scope_transfer_null_is_not_contradiction", "Drug A improves bladder perfusion in humans.",
     "In healthy dogs, drug A did not change renal blood flow.", {"NO_SEMANTIC_RELATION", "PARTIALLY_COVERS",
                                                                  "ABSTAIN"}),
    ("FX-21", "quantity_conflict", "Mean maximum flow rate rose by 4.5 mL/s in the drug A arm of the trial.",
     "Mean maximum flow rate rose by 1.2 mL/s in the drug A arm of the trial.", {"CONTRADICTS"}),
    ("FX-22", "instance_establishes_capability",
     "At least one study reports drug A reducing serum TNF-alpha in human subjects.",
     "In 20 patients, oral drug A 400 mg three times daily reduced serum TNF-alpha by 30% after four weeks.",
     {"WITNESS_ENTAILS_UNIT", "EQUIVALENT"}),
]


def norm_rel(r: str) -> str:
    """Map an answer to one relation label.  Only an exact label, or a label followed by a
    qualifier ("EQUIVALENT (strong)"), counts; anything else ("not equivalent", "does not
    contradict", free prose) is ABSTAIN rather than a guess."""
    r = (r or "").upper().strip().strip("`'\".,;:*").replace("-", "_")
    r = re.sub(r"\s+", "_", r)
    if r in RELATIONS:
        return r
    for k in sorted(RELATIONS, key=len, reverse=True):
        if r.startswith(k) and (len(r) == len(k) or not r[len(k)].isalnum()):
            return k
    return "ABSTAIN"


# --------------------------------------------------------------------------- #
# texts used for matching (transcoded when the language layer produced PASS)
# --------------------------------------------------------------------------- #

def matching_texts(ctx) -> tuple[dict, dict, dict]:
    witnesses = ctx.load("witnesses", "05_released/witnesses.json", default=[]) or []
    units = ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or []
    tc = ctx.load("transcoding", "transcoded.json", default={}) or {}
    titems = {it["item_id"]: it for it in tc.get("items", [])}
    wtext, utext = {}, {}
    # only a PASS transcoding replaces the raw text; IDENTITY (language layer off) and
    # REVIEW use the current raw text, so a hand-edited unit is matched as edited
    for w in witnesses:
        it = titems.get(w["witness_id"])
        wtext[w["witness_id"]] = it["transcoded"] if it and it.get("status") == "PASS" else w["text"]
    for u in units:
        it = titems.get(u["unit_id"])
        utext[u["unit_id"]] = it["transcoded"] if it and it.get("status") == "PASS" else u["text"]
    meta = {"mode": tc.get("mode", "off"), "witness_items": len(wtext), "unit_items": len(utext),
            "excluded_review": [k for k, it in titems.items() if it.get("status") == "REVIEW"]}
    return wtext, utext, meta


def eligible_witnesses(ctx) -> list[dict]:
    ws = ctx.load("witnesses", "05_released/witnesses.json", default=[]) or []
    tc = ctx.load("transcoding", "transcoded.json", default={}) or {}
    review = {it["item_id"] for it in tc.get("items", []) if it.get("status") == "REVIEW"}
    return [w for w in ws if w["witness_id"] not in review]


def expand_synonyms(toks: set, groups: list) -> set:
    """Add every member of a synonym group (``matching.synonyms``) that shares a token with ``toks``."""
    out = set(toks)
    for g in groups or []:
        gs = {t for x in g for t in tokens(str(x))}
        if gs & out:
            out |= gs
    return out


def shortlist(unit: dict, utext: str, wtexts: dict, k: int, synonyms: list | None = None) -> list[str]:
    q = set(tokens(" ".join([utext, unit.get("satisfied_by", ""), " ".join(unit.get("evidence_terms", []))])))
    q = expand_synonyms(q, synonyms)
    scored = []
    for wid, t in wtexts.items():
        tt = set(tokens(t))
        s = len(q & tt) / (1 + len(tt) ** 0.5)
        scored.append((s, wid))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [wid for _, wid in scored[:k]]


def _wlist(wids: list[str], wtexts: dict) -> str:
    return "\n".join(f"[{wid}] {wtexts[wid]}" for wid in wids)


def _hyp_brief(frame: dict, hid: str) -> str:
    for ax in frame["axes"]:
        for h in ax["hypotheses"]:
            if h["id"] == hid:
                return truncate_words(h.get("statement", ""), 70) + (
                    f" [Scope: {truncate_words(ax.get('scope', ''), 40)}]" if ax.get("scope") else "")
    return ""


def run_passes(ctx, plan: list[tuple[dict, list[str]]], utexts: dict, wtexts: dict,
               stage_tag: str) -> dict:
    """plan: [(unit, [witness ids])].  Returns {(wid, uid): {a, trace_a, b, trace_b}}."""
    bs = int(ctx.cfg["matching"].get("batch_size", 15))
    reqs, index = [], []
    for unit, wids in plan:
        brief = _hyp_brief(ctx.frame, unit["hypothesis_id"])
        for bno, batch in enumerate(chunked(sorted(wids), bs)):
            for pas, tmpl, order in (("a", "match_a.md", batch), ("b", "match_b.md", list(reversed(batch)))):
                system, user, _ = ctx.prompts.render(
                    tmpl, UNIT_ID=unit["unit_id"], UNIT_TYPE=unit["type"], HID=unit["hypothesis_id"],
                    UNIT_TEXT=utexts[unit["unit_id"]], SATISFIED_BY=unit.get("satisfied_by", "") or "(not stated)",
                    HYP_BRIEF=brief, WITNESSES=_wlist(order, wtexts))
                role = "matcher_a" if pas == "a" else "matcher_b"
                reqs.append(LLMRequest(role=role, system=system, user=user,
                                       tag=f"{stage_tag}:{pas}:{unit['unit_id']}:{bno}",
                                       salt=f"pass-{pas}",
                                       meta={"unit": unit, "unit_text": utexts[unit["unit_id"]],
                                             "witnesses": {w: wtexts[w] for w in order}, "pass": pas}))
                index.append((pas, unit["unit_id"], order))
    results = ctx.llm.call_many(reqs)
    out: dict = {}
    for (pas, uid, order), res in zip(index, results):
        data = res.parsed if res and isinstance(res.parsed, dict) else {}
        js = as_list(data.get("judgments") if data else (res.parsed if res else []), "judgments")
        got = {}
        for j in js:
            if isinstance(j, dict) and j.get("witness_id") in order:
                got[j["witness_id"]] = j
        for wid in order:
            j = got.get(wid)
            rec = out.setdefault((wid, uid), {})
            rec[pas] = norm_rel(j.get("relation")) if j else "MISSING"
            rec["trace_" + pas] = (j.get("trace") or "") if j else "no judgment returned"
            rec["key_" + pas] = res.key if res else ""
            if not j and res is not None and "skipped by the queue operator" in str(res.parse_error or ""):
                rec["skipped_" + pas] = True
    return out


def adjudicate(ctx, pairs: dict, units: dict, utexts: dict, wtexts: dict, stage_tag: str) -> dict:
    """pairs: {(wid, uid): rec} with disagreement.  Returns {(wid, uid): (relation, trace)}."""
    by_unit: dict = {}
    for (wid, uid), rec in pairs.items():
        by_unit.setdefault(uid, []).append((wid, rec))
    reqs, idx = [], []
    for uid, items in sorted(by_unit.items()):
        u = units[uid]
        for bno, batch in enumerate(chunked(sorted(items), 12)):
            disp = "\n\n".join(
                f"[{wid}] \"{wtexts[wid]}\"\n  PASS A: {rec.get('a')} - {rec.get('trace_a', '')}\n"
                f"  PASS B: {rec.get('b')} - {rec.get('trace_b', '')}" for wid, rec in batch)
            system, user, _ = ctx.prompts.render(
                "match_adjudicate.md", UNIT_ID=uid, UNIT_TYPE=u["type"], HID=u["hypothesis_id"],
                UNIT_TEXT=utexts[uid], DISPUTES=disp)
            reqs.append(LLMRequest(role="match_adjudicator", system=system, user=user,
                                   tag=f"{stage_tag}:adj:{uid}:{bno}",
                                   meta={"unit_text": utexts[uid],
                                         "disputes": {wid: rec for wid, rec in batch}}))
            idx.append((uid, [wid for wid, _ in batch]))
    results = ctx.llm.call_many(reqs)
    out = {}
    for (uid, wids), res in zip(idx, results):
        data = res.parsed if res and isinstance(res.parsed, dict) else {}
        ds = {d.get("witness_id"): d for d in as_list(data.get("decisions") if data else [], "decisions")
              if isinstance(d, dict)}
        skipped = res is not None and "skipped by the queue operator" in str(res.parse_error or "")
        for wid in wids:
            d = ds.get(wid)
            if skipped:
                continue        # no adjudication happened: the pair stays DISPUTED (ABSTAIN)
            out[(wid, uid)] = ((norm_rel(d.get("relation")), d.get("trace", ""), res.key if res else "")
                               if d else ("ABSTAIN", "adjudicator returned no decision", res.key if res else ""))
    return out


def combine(ctx, raw: dict, units: dict, utexts: dict, wtexts: dict, stage_tag: str) -> list[dict]:
    policy = ctx.cfg["matching"].get("dispute_policy", "adjudicate")
    # when one pass's request was never answered: "abstain" (default) or "accept" the single
    # judgment, labelled ONE_PASS_ONLY everywhere it is used
    one_pass = ctx.cfg["matching"].get("one_pass_policy", "abstain")
    # a pass whose request was deliberately left unanswered (cr queue skip) is not re-judged by the
    # adjudicator: the pair keeps its single judgment for the human review packet and counts as ABSTAIN
    disputes = {k: v for k, v in raw.items() if v.get("a") != v.get("b")
                and not (v.get("skipped_a") or v.get("skipped_b"))}
    adj = adjudicate(ctx, disputes, units, utexts, wtexts, stage_tag) if (disputes and policy == "adjudicate") else {}
    rows = []
    for (wid, uid), rec in sorted(raw.items()):
        u = units[uid]
        row = {"witness_id": wid, "unit_id": uid, "hypothesis_id": u["hypothesis_id"], "axis_id": u["axis_id"],
               "unit_type": u["type"], "a": rec.get("a"), "trace_a": rec.get("trace_a", ""),
               "b": rec.get("b"), "trace_b": rec.get("trace_b", ""), "stage": stage_tag}
        if rec.get("a") == rec.get("b") and rec.get("a") not in ("MISSING",):
            row.update(final=rec["a"], basis="AGREED", trace=rec.get("trace_a", ""))
        elif rec.get("a") == "MISSING" and rec.get("b") == "MISSING":
            row.update(final="ABSTAIN", basis="MISSING", trace="neither pass returned a judgment for this pair")
        elif rec.get("skipped_a") or rec.get("skipped_b"):
            single = rec.get("b") if rec.get("skipped_a") else rec.get("a")
            tr = rec.get("trace_b", "") if rec.get("skipped_a") else rec.get("trace_a", "")
            if one_pass == "accept" and single not in ("MISSING", None):
                row.update(final=single, basis="ONE_PASS_ONLY", single_pass_relation=single,
                           trace=f"[one pass only; the other pass's request was not answered] {tr}")
            else:
                row.update(final="ABSTAIN", basis="ONE_PASS_ONLY", single_pass_relation=single,
                           trace=f"only one pass judged this pair ({single}); the other pass's request was not "
                                 f"answered. Not used for coverage; a human can confirm it in human-decisions.json")
        elif (wid, uid) in adj:
            rel, tr, key = adj[(wid, uid)]
            row.update(final=rel, basis="MODEL_ADJUDICATED", trace=tr, key_adj=key)
        else:
            row.update(final="ABSTAIN", basis="DISPUTED",
                       trace="pass A and pass B disagree; no adjudication" + (
                           " (the adjudication request was not answered)" if policy == "adjudicate" else ""))
        rows.append(row)
    return rows


def qualify(ctx) -> dict:
    if not ctx.cfg["matching"].get("qualify", True):
        return {"skipped": True, "note": "matching.qualify is false: the matcher was not qualified"}
    extra = read_json(ctx.project_dir / "01_FRAME" / "match-fixtures.json", default=None)
    fixtures = list(FIXTURES)
    if extra:
        fixtures += [(f["id"], f["pattern"], f["unit"], f["witness"], set(f["accept"])) for f in extra]
    units, utexts, wtexts, plan = {}, {}, {}, []
    for fid, pat, unit, wit, acc in fixtures:
        uid = f"{fid}-U"
        wid = f"{fid}-W"
        u = {"unit_id": uid, "hypothesis_id": "FIXTURE", "axis_id": "FIXTURE",
             "type": "REQUIRED_SUPPORT", "text": unit, "satisfied_by": ""}
        units[uid] = u
        utexts[uid] = unit
        wtexts[wid] = wit
        plan.append((u, [wid]))
    frame_backup = ctx._frame
    ctx._frame = {"axes": []}
    try:
        raw = run_passes(ctx, plan, utexts, wtexts, "qualify")
    finally:
        ctx._frame = frame_backup
    rows, per = [], {}
    for fid, pat, unit, wit, acc in fixtures:
        rec = raw.get((f"{fid}-W", f"{fid}-U"), {})
        a_ok, b_ok = rec.get("a") in acc, rec.get("b") in acc
        rows.append({"fixture": fid, "pattern": pat, "accept": sorted(acc), "pass_a": rec.get("a"),
                     "pass_b": rec.get("b"), "a_ok": a_ok, "b_ok": b_ok,
                     "trace_a": rec.get("trace_a", ""), "trace_b": rec.get("trace_b", "")})
        p = per.setdefault(pat, {"n": 0, "a_ok": 0, "b_ok": 0})
        p["n"] += 1
        p["a_ok"] += int(a_ok)
        p["b_ok"] += int(b_ok)
    qualified = sorted(p for p, d in per.items() if d["a_ok"] == d["n"] and d["b_ok"] == d["n"])
    out = {"fixtures": len(rows), "pass_a_correct": sum(r["a_ok"] for r in rows),
           "pass_b_correct": sum(r["b_ok"] for r in rows), "per_pattern": per,
           "qualified_patterns": qualified,
           "unqualified_patterns": sorted(set(per) - set(qualified)), "rows": rows,
           "disclosure": ("Fixtures use generic 'drug A' vocabulary plus any project fixtures in "
                          "01_FRAME/match-fixtures.json. Passing them qualifies the matcher only for "
                          "these tested patterns; it does not prove general language understanding."),
           "time": utcnow()}
    ctx.save("matching", "02_match-fixtures/qualification.json", out, "matcher-qualification")
    return {k: out[k] for k in ("fixtures", "pass_a_correct", "pass_b_correct", "unqualified_patterns")}


def match_stage(ctx) -> dict:
    mcfg = ctx.cfg["matching"]
    wtexts_all, utexts, meta = matching_texts(ctx)
    elig = {w["witness_id"] for w in eligible_witnesses(ctx)}
    wtexts = {k: v for k, v in wtexts_all.items() if k in elig}
    units = {u["unit_id"]: u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])
             if u.get("active")}
    k = int(mcfg.get("shortlist_k", 30))
    k2 = int(mcfg.get("shortlist_k_secondary", 15))
    exhaustive = len(wtexts) <= int(mcfg.get("exhaustive_threshold", 45))
    plan = []
    for uid, u in sorted(units.items()):
        kk = k if u["type"] in ("REQUIRED_SUPPORT", "CONTEXTUAL_CONSTRAINT") else k2
        wids = sorted(wtexts) if exhaustive else shortlist(u, utexts[uid], wtexts, kk, mcfg.get("synonyms"))
        plan.append((u, wids))
    raw = run_passes(ctx, plan, utexts, wtexts, "match")
    rows = combine(ctx, raw, units, utexts, wtexts, "match")
    assessed = {(r["witness_id"], r["unit_id"]) for r in rows}
    not_assessed = len(units) * len(wtexts) - len(assessed)
    ctx.save("matching", "03_match-records/relations.json", rows, "match-relations")
    disputes = [r for r in rows if r["basis"] != "AGREED"]
    ctx.save("matching", "04_disagreements-and-review/disputes.json", disputes, "match-disputes")
    summary = {"units": len(units), "witnesses": len(wtexts), "pairs_assessed": len(rows),
               "pairs_not_assessed_prefilter": not_assessed, "exhaustive": exhaustive,
               "agreed": sum(1 for r in rows if r["basis"] == "AGREED"),
               "model_adjudicated": sum(1 for r in rows if r["basis"] == "MODEL_ADJUDICATED"),
               "disputed_abstain": sum(1 for r in rows if r["basis"] == "DISPUTED"),
               "missing_both_passes": sum(1 for r in rows if r["basis"] == "MISSING"),
               "one_pass_only": sum(1 for r in rows if r["basis"] == "ONE_PASS_ONLY"),
               "complete_relations": sum(1 for r in rows if r["final"] in COMPLETE),
               "contradictions": sum(1 for r in rows if r["final"] == "CONTRADICTS"),
               "text_mode": meta["mode"]}
    ctx.save("matching", "03_match-records/summary.json", summary, "match-summary")
    summary.update(write_review_packet(ctx))
    return summary


def completion_match(ctx, pairs: set[tuple[str, str]]) -> list[dict]:
    """Judge additional (witness, unit) pairs (no prefilter) and merge them into relations.json."""
    rows = ctx.load("matching", "03_match-records/relations.json", default=[]) or []
    have = {(r["witness_id"], r["unit_id"]) for r in rows}
    need = sorted(p for p in pairs if p not in have)
    if not need:
        return []
    wtexts, utexts, _ = matching_texts(ctx)
    units = {u["unit_id"]: u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])}
    by_u: dict = {}
    for wid, uid in need:
        if wid in wtexts and uid in units:
            by_u.setdefault(uid, []).append(wid)
    plan = [(units[uid], wids) for uid, wids in sorted(by_u.items())]
    raw = run_passes(ctx, plan, utexts, wtexts, "complete")
    new = combine(ctx, raw, units, utexts, wtexts, "complete")
    rows.extend(new)
    ctx.save("matching", "03_match-records/relations.json", rows, "match-relations")
    return new


HUMAN_FILE = "04_disagreements-and-review/human-decisions.json"


def human_decisions(ctx) -> dict:
    """Human relation decisions, if a reviewer supplied any.

    File: ``07_MATCHING/04_disagreements-and-review/human-decisions.json``::

        {"decisions": [{"witness_id": "W-...", "unit_id": "A1-H1-R1",
                        "relation": "NO_SEMANTIC_RELATION", "reviewer": "Josh",
                        "note": "the witness reports a different population"}]}

    A human decision overrides the model relation for that pair (basis HUMAN) in
    every later stage; the model's relation is kept beside it.  After adding or
    editing the file, re-run from coverage:  cr run <project> --from coverage
    """
    data = ctx.load("matching", HUMAN_FILE, default=None)
    if not data:
        return {}
    items = data.get("decisions", []) if isinstance(data, dict) else data
    out = {}
    for d in items or []:
        if isinstance(d, dict) and d.get("witness_id") and d.get("unit_id") and d.get("relation"):
            rel = norm_rel(str(d["relation"]))
            out[(d["witness_id"], d["unit_id"])] = {**d, "relation": rel}
    return out


def rejected_human_decisions(ctx) -> list[dict]:
    """Human decisions that name a witness or unit this run does not have (typos, held witnesses,
    inactive units).  They are ignored, never applied, and listed in the report."""
    hd = human_decisions(ctx)
    if not hd:
        return []
    released = {w["witness_id"] for w in (ctx.load("witnesses", "05_released/witnesses.json", default=[]) or [])}
    active = {u["unit_id"] for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])
              if u.get("active")}
    out = []
    for (wid, uid), d in hd.items():
        why = []
        if wid not in released:
            why.append(f"no released witness {wid}")
        if uid not in active:
            why.append(f"no active unit {uid}")
        if why:
            out.append({**d, "rejected_because": "; ".join(why)})
    return out


def relations_index(ctx) -> dict:
    rows = ctx.load("matching", "03_match-records/relations.json", default=[]) or []
    idx = {(r["witness_id"], r["unit_id"]): r for r in rows}
    hd = human_decisions(ctx)
    if hd:
        units = {u["unit_id"]: u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])}
        bad = {(d["witness_id"], d["unit_id"]) for d in rejected_human_decisions(ctx)}
        hd = {k: v for k, v in hd.items() if k not in bad}
        for (wid, uid), d in hd.items():
            base = idx.get((wid, uid))
            note = f"human decision ({d.get('reviewer') or 'reviewer not named'}): {d.get('note', '')}".strip()
            if base:
                idx[(wid, uid)] = {**base, "model_final": base.get("final"), "model_basis": base.get("basis"),
                                   "final": d["relation"], "basis": "HUMAN", "trace": note}
            elif uid in units:
                u = units[uid]
                idx[(wid, uid)] = {"witness_id": wid, "unit_id": uid, "hypothesis_id": u["hypothesis_id"],
                                   "axis_id": u["axis_id"], "unit_type": u["type"], "final": d["relation"],
                                   "basis": "HUMAN", "trace": note, "stage": "human"}
    return idx


def write_review_packet(ctx) -> dict:
    """A reading packet for a human reviewer plus a blank decisions template.

    It lists every pair whose relation drives a result: complete relations (coverage),
    contradictions (crux), and every pair the two passes disagreed on."""
    rows = list(relations_index(ctx).values())
    ws = {w["witness_id"]: w for w in (ctx.load("witnesses", "05_released/witnesses.json", default=[]) or [])}
    units = {u["unit_id"]: u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])}
    groups = [
        ("Complete relations (these build coverage sets)", [r for r in rows if r.get("final") in COMPLETE]),
        ("Contradictions (these drive crux tests)", [r for r in rows if r.get("final") == "CONTRADICTS"]),
        ("Disagreements between pass A and pass B", [r for r in rows if r.get("basis") in ("MODEL_ADJUDICATED", "DISPUTED")]),
        ("Judged by one pass only (needs confirmation)", [r for r in rows if r.get("basis") == "ONE_PASS_ONLY"
                                                          and r.get("single_pass_relation") in COMPLETE + ("CONTRADICTS",)]),
    ]
    lines = ["# Matching review packet", "",
             "Each entry is one witness judged against one coverage unit. To overrule a relation, add an entry to "
             "`human-decisions.json` in this folder (a blank template is next to this file) and run "
             "`cr run <project> --from coverage`. Relations: EQUIVALENT, WITNESS_ENTAILS_UNIT (these two give "
             "complete coverage), UNIT_ENTAILS_WITNESS, PARTIALLY_COVERS, CONTRADICTS, NO_SEMANTIC_RELATION, ABSTAIN.",
             ""]
    seen = set()
    n = 0
    for title, items in groups:
        lines += [f"## {title} ({len(items)})", ""]
        for r in sorted(items, key=lambda x: (x["unit_id"], x["witness_id"])):
            u = units.get(r["unit_id"], {})
            w = ws.get(r["witness_id"], {})
            lines += [f"### {r['unit_id']} x {r['witness_id']}",
                      f"- Unit ({u.get('type', r.get('unit_type', ''))}): {u.get('text', '')}",
                      f"- Witness: {w.get('text', '')}",
                      f"- Source: {w.get('source_file', '')} {w.get('locator', '')}".rstrip(),
                      f"- Pass A: {r.get('a', '')} - {r.get('trace_a', '')}",
                      f"- Pass B: {r.get('b', '')} - {r.get('trace_b', '')}",
                      f"- Final: **{r.get('final')}** ({r.get('basis')}) - {r.get('trace', '')}", ""]
            if (r["witness_id"], r["unit_id"]) not in seen:
                seen.add((r["witness_id"], r["unit_id"]))
                n += 1
    from .util import atomic_write_text
    atomic_write_text(ctx.p("matching", "04_disagreements-and-review", "review-packet.md"), "\n".join(lines))
    tmpl = {"instructions": "Copy entries into human-decisions.json (same shape) to overrule a relation. "
                            "relation must be one of " + ", ".join(RELATIONS) + ".",
            "decisions": [{"witness_id": "W-...", "unit_id": "A1-H1-R1", "relation": "NO_SEMANTIC_RELATION",
                           "reviewer": "your name", "note": "why"}]}
    from .util import write_json
    write_json(ctx.p("matching", "04_disagreements-and-review", "human-decisions.template.json"), tmpl)
    return {"review_pairs": n, "human_decisions": len(human_decisions(ctx))}
