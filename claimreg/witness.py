"""Phase IV - question-guided witness construction and fidelity audit (spec 24-25, 27).

Steps (each a batch of independent model calls, all cached):

1. Applications: the origin question for every retained validated FRD (required
   origin reuse); optionally the cluster-best question (spec 24.4 experiment).
2. Construct v1 at the raw ceiling (60 words).
3. Ceiling exception: a constructor ABSTAIN at 60 words is retried once at the
   exception ceiling (80 words) and recorded as CEILING_EXCEPTION.  This is a
   harness decision taken under the owner's authorization; it keeps material
   qualifications instead of discarding the witness.
4. Mechanical checks: word count, numerals not present in the parent FRD,
   negation dropped from a negative FRD.
5. Independent audit (separate context; never the constructor).
6. One repair round for REVISE_WITNESS (or a mechanical failure), then re-audit.

A witness is RELEASED to matching only when its final audit is PASS and its
mechanical checks pass.  Everything else is HELD with its reason; nothing is
deleted.
"""

from __future__ import annotations

from .llm.base import LLMRequest
from .util import NEGATION_RE, numerals, tokens, utcnow, word_count


def _wid(vfrd_id: str, qid: str, kind: str) -> str:
    return f"W-{vfrd_id}-{qid}" + ("" if kind == "origin" else "-CB")


def build_applications(ctx, retained: list[dict], questions: dict) -> list[dict]:
    apps = []
    for v in retained:
        apps.append({"app_id": f"APP-{v['vfrd_id']}-{v['qid']}", "vfrd_id": v["vfrd_id"],
                     "qid": v["qid"], "kind": "origin",
                     "witness_id": _wid(v["vfrd_id"], v["qid"], "origin")})
    if ctx.cfg["witness"].get("cluster_best"):
        from .header import all_hypotheses, hypothesis_text
        hyp_toks = set(tokens(" ".join(hypothesis_text(h) for h in all_hypotheses(ctx.frame))))
        clusters: dict = {}
        for v in retained:
            clusters.setdefault(v["source_file"], []).append(v)
        for src, vs in clusters.items():
            qids = sorted({v["qid"] for v in vs})
            if len(qids) < 2:
                continue

            def rel(q):
                t = set(tokens(questions.get(q, {}).get("text", "")))
                return len(t & hyp_toks) / max(1, len(t))
            scored = sorted(qids, key=lambda q: (-rel(q), q))
            if len(scored) > 1 and abs(rel(scored[0]) - rel(scored[1])) < 1e-9:
                continue   # material tie: hold the additional lens (spec Still Open 4)
            best = scored[0]
            for v in vs:
                if v["qid"] != best:
                    apps.append({"app_id": f"APP-{v['vfrd_id']}-{best}-CB", "vfrd_id": v["vfrd_id"],
                                 "qid": best, "kind": "cluster_best",
                                 "witness_id": _wid(v["vfrd_id"], best, "cluster_best")})
    return apps


_NUMBER_WORDS = {w: str(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
    "seventeen eighteen nineteen twenty".split())}
_NUMBER_WORDS.update({"thirty": "30", "forty": "40", "fifty": "50", "sixty": "60", "seventy": "70",
                      "eighty": "80", "ninety": "90", "hundred": "100", "half": "50", "twice": "2",
                      "single": "1", "once": "1", "double": "2", "triple": "3"})


def _bare(n: str) -> str:
    """A number without sign or percent: '12-16' yields '-16' as a token, which is a range, not a sign."""
    return n.replace("\u2212", "-").lstrip("+-").rstrip("%").strip()


def parent_numbers(parent: str) -> set[str]:
    """Every number the parent record licenses: numerals, digit runs inside words or file names
    (author-year citations such as 'raison2013'), and number words ('nine' -> 9)."""
    import re as _re
    out = {_bare(x) for x in numerals(parent)}
    out |= set(_re.findall(r"\d+(?:\.\d+)?", parent))
    low = parent.lower()
    out |= {d for w, d in _NUMBER_WORDS.items() if _re.search(rf"\b{w}\b", low)}
    return out


def mechanical(text: str, v: dict, ceiling: int, extra: str = "") -> dict:
    """Deterministic gates.  ``extra`` is the source file's opening text (title,
    authors, year) so that an author-year citation is not mistaken for an
    invented number."""
    wc = word_count(text)
    parent = (v.get("claim", "") + " " + v.get("source_text", "") + " " + v.get("source_file", "")
              + " " + str(v.get("citation", {}).get("locator", "")) + " " + extra)
    allowed = parent_numbers(parent)
    invented = sorted(n for n in numerals(text) if _bare(n) not in allowed)
    neg_dropped = bool(NEGATION_RE.search(v.get("claim", ""))) and not NEGATION_RE.search(text)
    ok = wc <= ceiling and not invented
    return {"words": wc, "ceiling": ceiling, "within_ceiling": wc <= ceiling,
            "numerals_not_in_parent": invented, "negation_dropped_warning": neg_dropped, "ok": ok}


def _construct_req(ctx, app, v, q, ceiling, note=""):
    system, user, _ = ctx.prompts.render(
        "witness_construct.md", QID=app["qid"], QUESTION=q.get("text", ""), FRD_ID=v["vfrd_id"],
        CITATION=f"{v['source_file']} - {v.get('citation', {}).get('locator', '')}",
        CLAIM=v["claim"], VERDICT=f"{v['verdict']}: {v.get('verdict_explanation', '')}",
        SOURCE_TEXT=v.get("source_text", ""), CEILING=ceiling, REVISION_NOTE=note)
    return LLMRequest(role="witness_constructor", system=system, user=user,
                      tag=f"witness:{app['witness_id']}:c{ceiling}{':rev' if note else ''}",
                      meta={"vfrd": v, "ceiling": ceiling, "question": q.get("text", "")})


def _audit_req(ctx, app, v, q, text):
    system, user, _ = ctx.prompts.render(
        "witness_audit.md", QID=app["qid"], QUESTION=q.get("text", ""), FRD_ID=v["vfrd_id"],
        CITATION=f"{v['source_file']} - {v.get('citation', {}).get('locator', '')}",
        CLAIM=v["claim"], VERDICT=f"{v['verdict']}: {v.get('verdict_explanation', '')}",
        SOURCE_TEXT=v.get("source_text", ""), WITNESS_ID=app["witness_id"],
        WORDS=word_count(text), WITNESS=text)
    return LLMRequest(role="witness_auditor", system=system, user=user,
                      tag=f"audit:{app['witness_id']}:{word_count(text)}w",
                      meta={"vfrd": v, "witness": text})


def _cw(res) -> dict:
    d = res.parsed if res and isinstance(res.parsed, dict) else {}
    st = (d.get("status") or ("WITNESS" if d.get("witness") else "ERROR")).upper()
    if "ABSTAIN" in st:
        st = "ABSTAIN"
    elif "REPAIR" in st:
        st = "REPAIR_FRD"
    elif st != "ERROR":
        st = "WITNESS"
    return {"status": st, "text": (d.get("witness") or "").strip(), "preserved": d.get("preserved", []),
            "omitted": d.get("omitted", []), "would_be_lost": d.get("would_be_lost", ""),
            "repair_needed": d.get("repair_needed", ""), "call_key": res.key if res else "",
            "parse_error": res.parse_error if res else "no response"}


def _av(res) -> dict:
    d = res.parsed if res and isinstance(res.parsed, dict) else {}
    v = (d.get("verdict") or "ERROR").upper()
    for k in ("REVISE_WITNESS", "REPAIR_FRD", "HUMAN_REVIEW", "PASS"):
        if k in v:
            v = k
            break
    return {"verdict": v, "unsupported": d.get("unsupported_assertions", []),
            "omissions": d.get("material_omissions", []),
            "forbidden_reading": d.get("strongest_forbidden_reading", ""),
            "reader_recovers": d.get("reader_recovers", ""), "reason": d.get("reason", ""),
            "fix": d.get("fix", ""), "call_key": res.key if res else "",
            "parse_error": res.parse_error if res else "no response"}


def build_witnesses(ctx) -> dict:
    wcfg = ctx.cfg["witness"]
    raw_c = int(wcfg.get("raw_ceiling", 60))
    exc_c = int(wcfg.get("exception_ceiling", 80))
    allow_exc = bool(wcfg.get("allow_ceiling_exception", True))
    retained = ctx.load("frds", "05_validated/retained-frds.json", default=None)
    if retained is None:
        retained = ctx.load("frds", "05_validated/validated-frds.json", default=[]) or []
    vmap = {v["vfrd_id"]: v for v in retained}
    questions = {q["qid"]: q for q in ctx.load("discovery", "01_issued-questions/questions.json",
                                                 default=[]) or []}
    apps = build_applications(ctx, retained, questions)

    def head(a):
        try:
            return ctx.corpus.text(vmap[a["vfrd_id"]]["source_file"])[:3000]
        except Exception:
            return ""
    ctx.save("witnesses", "01_question-applications/applications.json", apps, "question-applications")
    versions: dict[str, list[dict]] = {a["witness_id"]: [] for a in apps}

    # step 1: construct at the raw ceiling
    reqs = [_construct_req(ctx, a, vmap[a["vfrd_id"]], questions.get(a["qid"], {}), raw_c) for a in apps]
    res1 = ctx.llm.call_many(reqs)
    for a, r in zip(apps, res1):
        rec = _cw(r)
        rec.update(version=1, ceiling=raw_c,
                   mechanical=mechanical(rec["text"], vmap[a["vfrd_id"]], raw_c, head(a)) if rec["text"] else {})
        versions[a["witness_id"]].append(rec)

    # step 2: ceiling exception / over-length repair
    retry = []
    for a in apps:
        last = versions[a["witness_id"]][-1]
        v = vmap[a["vfrd_id"]]
        q = questions.get(a["qid"], {})
        if last["status"] == "ABSTAIN" and allow_exc:
            retry.append((a, exc_c, _construct_req(
                ctx, a, v, q, exc_c,
                f"NOTE: at {raw_c} words the constructor abstained ({last['would_be_lost']}). Under a recorded "
                f"ceiling exception you may use up to {exc_c} words. Do not pad; keep every material qualification.")))
        elif last["status"] == "WITNESS" and last["mechanical"] and not last["mechanical"]["within_ceiling"]:
            retry.append((a, raw_c, _construct_req(
                ctx, a, v, q, raw_c,
                f"REVISION: the previous witness had {last['mechanical']['words']} words; the ceiling is "
                f"{raw_c}. Previous witness: \"{last['text']}\". Shorten it without losing material "
                f"qualifications, or ABSTAIN.")))
    if retry:
        res2 = ctx.llm.call_many([x[2] for x in retry])
        for (a, c, _), r in zip(retry, res2):
            rec = _cw(r)
            rec.update(version=len(versions[a["witness_id"]]) + 1, ceiling=c,
                       ceiling_exception=(c > raw_c),
                       mechanical=mechanical(rec["text"], vmap[a["vfrd_id"]], c, head(a)) if rec["text"] else {})
            versions[a["witness_id"]].append(rec)

    # step 3: audit the latest WITNESS version
    audits: dict[str, list[dict]] = {a["witness_id"]: [] for a in apps}

    def audit_round(round_no):
        todo = []
        for a in apps:
            last = versions[a["witness_id"]][-1]
            if last["status"] != "WITNESS" or not last["text"]:
                continue
            if audits[a["witness_id"]] and audits[a["witness_id"]][-1]["version"] == last["version"]:
                continue
            todo.append((a, last, _audit_req(ctx, a, vmap[a["vfrd_id"]], questions.get(a["qid"], {}),
                                             last["text"])))
        if not todo:
            return
        rs = ctx.llm.call_many([x[2] for x in todo])
        for (a, last, _), r in zip(todo, rs):
            au = _av(r)
            au.update(version=last["version"], round=round_no)
            audits[a["witness_id"]].append(au)

    audit_round(1)
    # step 4: one repair round
    max_rev = int(wcfg.get("max_revisions", 1))
    for rev in range(max_rev):
        fix = []
        for a in apps:
            vs, au = versions[a["witness_id"]], audits[a["witness_id"]]
            last = vs[-1]
            if last["status"] != "WITNESS" or not au:
                continue
            la = au[-1]
            mech_bad = last["mechanical"] and not last["mechanical"]["ok"]
            if la["version"] == last["version"] and (la["verdict"] == "REVISE_WITNESS" or
                                                     (la["verdict"] == "PASS" and mech_bad)):
                problems = []
                if la["verdict"] == "REVISE_WITNESS":
                    problems.append(f"Independent audit: {la['reason']} Fix: {la['fix']}")
                    problems += [f"Unsupported: {u.get('words', '')} - {u.get('problem', '')}"
                                 for u in la["unsupported"] if isinstance(u, dict)]
                    problems += [f"Omitted: {o.get('missing', '')} - {o.get('consequence', '')}"
                                 for o in la["omissions"] if isinstance(o, dict)]
                if mech_bad:
                    m = last["mechanical"]
                    if m["numerals_not_in_parent"]:
                        problems.append(f"Mechanical check: numbers not in the FRD: {m['numerals_not_in_parent']}")
                    if not m["within_ceiling"]:
                        problems.append(f"Mechanical check: {m['words']} words exceeds {m['ceiling']}")
                c = last["ceiling"]
                note = ("REVISION REQUESTED. Previous witness: \"" + last["text"] + "\"\nProblems:\n- "
                        + "\n- ".join(problems) + "\nWrite a corrected witness within the ceiling, or ABSTAIN.")
                fix.append((a, c, _construct_req(ctx, a, vmap[a["vfrd_id"]], questions.get(a["qid"], {}), c, note)))
        if not fix:
            break
        rs = ctx.llm.call_many([x[2] for x in fix])
        for (a, c, _), r in zip(fix, rs):
            rec = _cw(r)
            rec.update(version=len(versions[a["witness_id"]]) + 1, ceiling=c, ceiling_exception=(c > raw_c),
                       revision_of=versions[a["witness_id"]][-1]["version"],
                       mechanical=mechanical(rec["text"], vmap[a["vfrd_id"]], c, head(a)) if rec["text"] else {})
            versions[a["witness_id"]].append(rec)
        audit_round(2 + rev)

    # final disposition
    released, held = [], []
    all_versions, all_audits = [], []
    for a in apps:
        v = vmap[a["vfrd_id"]]
        vs, au = versions[a["witness_id"]], audits[a["witness_id"]]
        for x in vs:
            all_versions.append({"witness_id": a["witness_id"], **x})
        for x in au:
            all_audits.append({"witness_id": a["witness_id"], **x})
        last = vs[-1]
        la = au[-1] if au and au[-1]["version"] == last["version"] else None
        rec = {"witness_id": a["witness_id"], "app_id": a["app_id"], "application": a["kind"],
               "vfrd_id": a["vfrd_id"], "frd_id": v.get("frd_id", a["vfrd_id"]), "qid": a["qid"],
               "source_file": v["source_file"], "locator": v.get("citation", {}).get("locator", ""),
               "text": last["text"], "words": word_count(last["text"]), "version": last["version"],
               "ceiling": last["ceiling"], "ceiling_exception": bool(last.get("ceiling_exception")),
               "constructor_status": last["status"], "audit_verdict": la["verdict"] if la else None,
               "audit_reason": la["reason"] if la else "", "mechanical": last.get("mechanical", {})}
        if last["status"] == "WITNESS" and la and la["verdict"] == "PASS" and last["mechanical"].get("ok"):
            rec["status"] = "RELEASED"
            released.append(rec)
        else:
            why = (last["status"] if last["status"] != "WITNESS" else
                   (f"audit {la['verdict']}" if la else "not audited") +
                   ("" if last["mechanical"].get("ok", False) else "; mechanical check failed"))
            if la and la["verdict"] == "ERROR" and la.get("parse_error"):
                why += f" - no usable audit answer ({str(la['parse_error'])[:200]})"
            rec["status"] = "HELD"
            rec["held_reason"] = why
            held.append(rec)
    ctx.save("witnesses", "02_raw-witnesses/witness-versions.json", all_versions, "witness-versions")
    ctx.save("witnesses", "03_fidelity-reviews/audits.json", all_audits, "fidelity-audits")
    ctx.save("witnesses", "04_repaired-or-held/held.json", held, "held-witnesses")
    ctx.save("witnesses", "05_released/witnesses.json", released, "released-witnesses")
    return {"applications": len(apps), "released": len(released), "held": len(held),
            "ceiling_exceptions": sum(1 for r in released if r["ceiling_exception"]),
            "audit_pass_first_round": sum(1 for a in all_audits if a["round"] == 1 and a["verdict"] == "PASS"),
            "time": utcnow()}
