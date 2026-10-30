"""Jointly sufficient groups and approved incompatibilities (spec 28, 29).

Joint sufficiency: for a REQUIRED_SUPPORT unit with no complete single-witness
option but at least two partial witnesses, one context proposes small groups
whose combined content entails the unit; a second, independent context must
approve each group.  Witnesses stay separate artifacts.

Incompatibility (the spec leaves the approval process open; this is the
harness's definition): two witnesses are incompatible only when two
independent passes both find SAME_QUANTITY_CONFLICT or OPPOSITE_POLARITY at
the same scope.  Only pairs that could matter are checked: witnesses that
appear in some coverage option.
"""

from __future__ import annotations

import itertools

from .llm.base import LLMRequest
from .llm.jsonparse import as_list
from .matching import COMPLETE, PARTIAL, matching_texts, relations_index
from .util import chunked, tokens, utcnow


def _active_units(ctx) -> dict:
    return {u["unit_id"]: u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or [])
            if u.get("active")}


def joint_stage(ctx) -> dict:
    ccfg = ctx.cfg["coverage"]
    rel = relations_index(ctx)
    units = _active_units(ctx)
    wtexts, utexts, _ = matching_texts(ctx)
    max_c = int(ccfg.get("max_joint_candidates", 10))
    max_size = int(ccfg.get("max_group_size", 3))

    # ---------------- joint sufficiency ----------------
    proposals_req, prop_idx = [], []
    for uid, u in sorted(units.items()):
        if u["type"] != "REQUIRED_SUPPORT":
            continue
        complete = [w for (w, x), r in rel.items() if x == uid and r["final"] in COMPLETE]
        partial = [(w, r) for (w, x), r in rel.items() if x == uid and r["final"] in PARTIAL]
        if complete or len(partial) < 2:
            continue
        # strongest partial witnesses first: UNIT_ENTAILS_WITNESS before PARTIALLY_COVERS, agreed before
        # adjudicated or one-pass judgments, then word overlap with the unit
        ut = set(tokens(utexts.get(uid, u["text"]) + " " + u.get("satisfied_by", "")))
        brank = {"HUMAN": 0, "AGREED": 1, "MODEL_ADJUDICATED": 2}
        partial.sort(key=lambda wr: (0 if wr[1]["final"] == "UNIT_ENTAILS_WITNESS" else 1,
                                     brank.get(wr[1].get("basis"), 3),
                                     -len(ut & set(tokens(wtexts.get(wr[0], "")))), wr[0]))
        cand = [w for w, _ in partial][:max_c]
        system, user, _ = ctx.prompts.render(
            "joint_check.md", MAX_GROUPS=4, MAX_SIZE=max_size, UNIT_ID=uid, UNIT_TYPE=u["type"],
            HID=u["hypothesis_id"], UNIT_TEXT=utexts.get(uid, u["text"]),
            SATISFIED_BY=u.get("satisfied_by", "") or "(not stated)",
            WITNESSES="\n".join(f"[{w}] {wtexts[w]}" for w in cand if w in wtexts))
        proposals_req.append(LLMRequest(role="joint_checker", system=system, user=user,
                                        tag=f"joint:{uid}", meta={"unit": u, "partials": cand}))
        prop_idx.append((uid, cand))
    props = ctx.llm.call_many(proposals_req) if proposals_req else []
    proposed = []
    for (uid, cand), res in zip(prop_idx, props):
        data = res.parsed if res and isinstance(res.parsed, dict) else {}
        for g in as_list(data.get("groups") if data else [], "groups"):
            if not isinstance(g, dict):
                continue
            ws = sorted({w for w in (g.get("witness_ids") or []) if w in cand})
            if 2 <= len(ws) <= max_size:
                proposed.append({"unit_id": uid, "witnesses": ws, "contributions": g.get("contributions", {}),
                                 "trace": g.get("trace", ""), "proposal_key": res.key})
    # dedupe
    seen, uniq = set(), []
    for p in proposed:
        k = (p["unit_id"], tuple(p["witnesses"]))
        if k not in seen:
            seen.add(k)
            uniq.append(p)
    ver_req = []
    for p in uniq:
        u = units[p["unit_id"]]
        system, user, _ = ctx.prompts.render(
            "joint_verify.md", UNIT_ID=p["unit_id"], HID=u["hypothesis_id"],
            UNIT_TEXT=utexts.get(p["unit_id"], u["text"]),
            WITNESSES="\n".join(f"[{w}] {wtexts[w]}" for w in p["witnesses"]))
        ver_req.append(LLMRequest(role="joint_checker", system=system, user=user, salt="verify",
                                  tag=f"joint-verify:{p['unit_id']}:{'+'.join(p['witnesses'])}",
                                  meta={"group": p}))
    vers = ctx.llm.call_many(ver_req) if ver_req else []
    groups = []
    for p, res in zip(uniq, vers):
        data = res.parsed if res and isinstance(res.parsed, dict) else {}
        ok = bool(data.get("approve")) if data else False
        groups.append({**p, "approved": ok, "verification": data.get("reason", "") if data else "no answer",
                       "member_contributions_verified": data.get("member_contributions", {}) if data else {},
                       "verify_key": res.key if res else ""})
    ctx.save("matching", "03_match-records/joint-groups.json", groups, "joint-groups")

    # ---------------- incompatibilities ----------------
    option_w = set()
    for (w, uid), r in rel.items():
        if uid in units and units[uid]["type"] == "REQUIRED_SUPPORT" and r["final"] in COMPLETE:
            option_w.add(w)
    for g in groups:
        if g["approved"]:
            option_w.update(g["witnesses"])
    ws = sorted(w for w in option_w if w in wtexts)
    released = {w["witness_id"]: w for w in (ctx.load("witnesses", "05_released/witnesses.json", default=[]) or [])}
    toks = {w: set(tokens(wtexts[w])) for w in ws}
    scored = []
    for a, b in itertools.combinations(ws, 2):
        ta, tb = toks[a], toks[b]
        sim = len(ta & tb) / max(1, len(ta | tb))
        same_src = released.get(a, {}).get("source_file") == released.get(b, {}).get("source_file")
        if sim >= 0.12 or same_src:
            scored.append((sim + (0.5 if same_src else 0), a, b))
    scored.sort(key=lambda x: (-x[0], x[1], x[2]))
    cap = int(ccfg.get("max_incompat_pairs", 200))
    cand_pairs = [(a, b) for _, a, b in scored[:cap]]
    passes = {}
    reqs, idx = [], []
    for pas in ("a", "b"):
        for bno, batch in enumerate(chunked(cand_pairs, 15)):
            order = batch if pas == "a" else [(b, a) for a, b in reversed(batch)]
            txt = "\n\n".join(f"PAIR {i + 1}: a = {x}; b = {y}\n  [{x}] {wtexts[x]}\n  [{y}] {wtexts[y]}"
                              for i, (x, y) in enumerate(order))
            system, user, _ = ctx.prompts.render("incompat_check.md", PAIRS=txt)
            reqs.append(LLMRequest(role="incompat_checker", system=system, user=user, salt=f"pass-{pas}",
                                   tag=f"incompat:{pas}:{bno}",
                                   meta={"pairs": order, "texts": {w: wtexts[w] for p in order for w in p}}))
            idx.append((pas, order))
    res_all = ctx.llm.call_many(reqs) if reqs else []
    for (pas, order), res in zip(idx, res_all):
        data = res.parsed if res and isinstance(res.parsed, dict) else {}
        for p in as_list(data.get("pairs") if data else [], "pairs"):
            if not isinstance(p, dict):
                continue
            a, b = p.get("a"), p.get("b")
            if not a or not b:
                continue
            key = tuple(sorted((a, b)))
            passes.setdefault(key, {})[pas] = {
                "incompatible": bool(p.get("incompatible")), "basis": p.get("basis", "NONE"),
                "trace": p.get("trace", "")}
    incompat = []
    for key in sorted(passes):
        pa, pb = passes[key].get("a"), passes[key].get("b")
        approved = bool(pa and pb and pa["incompatible"] and pb["incompatible"]
                        and str(pa["basis"]).upper() != "NONE" and str(pb["basis"]).upper() != "NONE")
        if (pa and pa["incompatible"]) or (pb and pb["incompatible"]):
            incompat.append({"a": key[0], "b": key[1], "approved": approved, "pass_a": pa, "pass_b": pb})
    ctx.save("matching", "03_match-records/incompatibilities.json",
             {"checked_pairs": len(cand_pairs), "candidate_witnesses": len(ws),
              "definition": "SAME_QUANTITY_CONFLICT or OPPOSITE_POLARITY at the same scope, found by both "
                            "independent passes", "records": incompat, "time": utcnow()},
             "incompatibilities")
    return {"joint_proposed": len(uniq), "joint_approved": sum(1 for g in groups if g["approved"]),
            "incompat_pairs_checked": len(cand_pairs),
            "incompat_approved": sum(1 for r in incompat if r["approved"])}


HUMAN_INCOMPAT_FILE = "04_disagreements-and-review/human-incompatibilities.json"


def incompatibility_records(ctx) -> list[dict]:
    """Model incompatibility records with any human decisions applied.

    File: ``07_MATCHING/04_disagreements-and-review/human-incompatibilities.json``::

        {"decisions": [{"a": "W-...", "b": "W-...", "approved": true,
                        "reviewer": "Josh", "note": "same outcome, opposite direction"}]}

    ``approved: true`` makes the pair incompatible, ``false`` clears a model
    approval.  Re-run from coverage afterwards."""
    recs = [dict(r) for r in ((ctx.load("matching", "03_match-records/incompatibilities.json", default={}) or {})
                              .get("records", []) or [])]
    data = ctx.load("matching", HUMAN_INCOMPAT_FILE, default=None)
    if not data:
        return recs
    items = data.get("decisions", []) if isinstance(data, dict) else data
    idx = {frozenset((r["a"], r["b"])): r for r in recs}
    for d in items or []:
        if not (isinstance(d, dict) and d.get("a") and d.get("b") and "approved" in d):
            continue
        key = frozenset((d["a"], d["b"]))
        note = f"human decision ({d.get('reviewer') or 'reviewer not named'}): {d.get('note', '')}".strip()
        r = idx.get(key)
        if r is None:
            r = {"a": min(key), "b": max(key), "pass_a": None, "pass_b": None}
            recs.append(r)
            idx[key] = r
        r["model_approved"] = r.get("approved")
        r.update(approved=bool(d["approved"]), basis="HUMAN", trace=note)
    return recs

