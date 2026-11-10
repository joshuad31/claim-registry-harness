"""Coverage units: the internal matching representation of each hypothesis (spec 2.2).

One model call per hypothesis.  Every unit must quote the human-written text
(or a header passage that defines a term the hypothesis uses) verbatim; the
quote is checked mechanically.  A unit whose quote cannot be found is kept
for audit but excluded from coverage (``active: false``), because an
unanchored unit may introduce a commitment the human never approved.
"""

from __future__ import annotations

import re

from .corpus import find_quote
from .header import all_hypotheses, hypothesis_text
from .llm.base import LLMRequest
from .llm.jsonparse import as_list
from .util import read_text, truncate_words

TYPES = ("REQUIRED_SUPPORT", "CONTEXTUAL_CONSTRAINT", "ADVERSE_TEST",
         "CORROBORATING_EXPECTATION", "EVALUATIVE_JUDGMENT")
MATCHABLE = ("REQUIRED_SUPPORT", "CONTEXTUAL_CONSTRAINT", "ADVERSE_TEST", "CORROBORATING_EXPECTATION")


def _norm_type(t: str) -> str:
    t = (t or "").upper().replace(" ", "_")
    for k in TYPES:
        if k in t or t in k:
            return k
    if t.startswith("REQ"):
        return "REQUIRED_SUPPORT"
    if t.startswith("CON"):
        return "CONTEXTUAL_CONSTRAINT"
    if t.startswith("ADV"):
        return "ADVERSE_TEST"
    if t.startswith("COR"):
        return "CORROBORATING_EXPECTATION"
    if t.startswith("EVA"):
        return "EVALUATIVE_JUDGMENT"
    return "REQUIRED_SUPPORT"


def header_definitions(frame: dict, header_text: str, max_words: int = 1600) -> str:
    parts = []
    if frame.get("mission"):
        parts.append(truncate_words(re.sub(r"\s+", " ", frame["mission"]), max_words))
    if frame.get("decisive_tests"):
        parts.append("Decisive-test map:\n" + "\n".join(f"- {t['test']}: {t['question']}"
                                                        for t in frame["decisive_tests"]))
    return "\n\n".join(parts) or "(none)"


# A REQUIRED_SUPPORT unit is matched against single witnesses (one published finding each), so it
# must be finding-sized.  These phrases mark a verdict about the evidence base instead; no single
# finding can establish one, and a required verdict would make complete coverage impossible.
_VERDICT = re.compile(
    r"\b(?:(?:available|existing|affirmative|current|the)\s+(?:\w+\s+){0,4}?evidence\s+"
    r"(?:supports?|demonstrates?|shows?|establish\w*|leaves?|cannot|does not|is (?:in)?sufficient|makes?)"
    r"|(?:supported|materially supported)\s+(?:premises?|rationale)"
    r"|(?:the|a|this)\s+(?:therapeutic\s+|mechanistic\s+|causal\s+)?rationale\b"
    r"|sufficient(?:ly)?\s+to\s+(?:specify|design|justify|warrant|fill)"
    r"|coherent\s+(?:causal\s+|mechanistic\s+)?(?:explanation|account|case)"
    r"|trial[- ]specification|specification\s+slots?"
    r"|(?:un)?resolved\s+links?|decisive\s+links?"
    r"|not\s+(?:presently\s+|yet\s+|currently\s+)?determined"
    r"|cannot\s+(?:be\s+)?(?:distinguish|specif|discriminat)\w*"
    r"|uncertainty\s+is\s+locali[sz]ed"
    r"|\bevidence\s+(?:is|are|remains?)\s+(?:un\w+|conflicting|poorly|compatible|insufficient|lacking|absent|missing)"
    r"|\bH[1-9]\b)", re.I)


def verdict_sized(text: str) -> str:
    """The phrase that marks ``text`` as a verdict about the evidence base, or ""."""
    m = _VERDICT.search(text or "")
    return m.group(0) if m else ""


def _parse_units(h: dict, res, anchor_text: str) -> list[dict]:
    data = res.parsed if res and isinstance(res.parsed, dict) else {}
    seen: set = set()
    out = []
    for i, u in enumerate(as_list(data.get("units") if data else [], "units"), 1):
        if not isinstance(u, dict) or not (u.get("text") or "").strip():
            continue
        typ = _norm_type(u.get("type", ""))
        code = re.sub(r"[^A-Za-z0-9]", "", str(u.get("code") or f"U{i}")) or f"U{i}"
        uid = f"{h['id']}-{code}"
        while uid in seen:
            uid += "x"
        seen.add(uid)
        quote = (u.get("source_quote") or "").strip()
        qc = find_quote(anchor_text, quote, 0.9) if quote else {"found": False, "method": "none"}
        out.append({
            "unit_id": uid, "hypothesis_id": h["id"], "axis_id": h["axis_id"], "type": typ,
            "text": u["text"].strip(), "serves": str(u.get("serves") or "").strip(),
            "source_quote": quote, "quote_check": qc,
            "evidence_terms": [t for t in (u.get("evidence_terms") or []) if isinstance(t, str)],
            "satisfied_by": u.get("satisfied_by", ""),
            "call_key": res.key if res else ""})
    return out


def _problems(units: list[dict]) -> list[str]:
    """What a model-written unit list still gets wrong: verdict-sized required units and
    quotations that are not in the frozen text."""
    out = []
    for u in units:
        if u["type"] == "EVALUATIVE_JUDGMENT":
            continue
        v = verdict_sized(u["text"]) if u["type"] == "REQUIRED_SUPPORT" else ""
        if v:
            out.append(f"{u['unit_id'].split('-')[-1]} is verdict-sized (\"{v}\"): rewrite it as the finding-sized "
                       f"facts it rests on, or record it as EVALUATIVE_JUDGMENT.")
        if not u["quote_check"]["found"]:
            out.append(f"{u['unit_id'].split('-')[-1]}: source_quote is not an exact quotation of the hypothesis "
                       f"or header text; copy at least 6 consecutive words character for character.")
    if units and not any(u["type"] != "EVALUATIVE_JUDGMENT" for u in units):
        pass   # a purely evaluative hypothesis is allowed
    return out


def derive_units(ctx) -> dict:
    frame = ctx.frame
    header_text = read_text(ctx.p("frame", "header.md")) if ctx.p("frame", "header.md").exists() else ""
    defs = header_definitions(frame, header_text)
    hyps = all_hypotheses(frame)
    ucfg = ctx.cfg.get("units", {}) or {}
    # the lint and the revision round apply to units written by a model API only; the local engine's
    # clause-level units are verbatim anchors and are left exactly as they are, and a file-queue
    # operator is not sent a second request
    lint = bool(ucfg.get("finding_sized", True)) and ctx.llm.is_api_role("unit_deriver")

    def request(h, note=""):
        rivals = [x for x in hyps if x["axis_id"] == h["axis_id"] and x["id"] != h["id"]]
        system, user, _ = ctx.prompts.render(
            "units_derive.md", AXIS_ID=h["axis_id"], AXIS_QUESTION=h.get("axis_question", ""),
            AXIS_BOUNDARY=h.get("axis_boundary", "") or "(none)", AXIS_SCOPE=h.get("axis_scope", "") or "(none)",
            RIVALS="; ".join(f"{r['id']}: {truncate_words(r.get('statement', ''), 40)}" for r in rivals) or "(none)",
            HID=h["id"], HYPOTHESIS_TEXT=hypothesis_text(h), HEADER_DEFINITIONS=defs, REVISION_NOTE=note)
        return LLMRequest(role="unit_deriver", system=system, user=user,
                          tag=f"units:{h['id']}" + (":rev" if note else ""), meta={"hypothesis": h})

    results = ctx.llm.call_many([request(h) for h in hyps])
    anchor_text = "\n".join(hypothesis_text(h) for h in hyps) + "\n" + header_text + "\n" + defs
    per_h = {h["id"]: _parse_units(h, res, anchor_text) for h, res in zip(hyps, results)}
    revised = []
    if lint:
        todo = [(h, _problems(per_h[h["id"]])) for h in hyps]
        todo = [(h, pr) for h, pr in todo if pr or not per_h[h["id"]]]
        if todo:
            reqs = []
            for h, pr in todo:
                prev = [{"code": u["unit_id"].split("-")[-1], "type": u["type"], "text": u["text"]}
                        for u in per_h[h["id"]]]
                note = ("\nREVISION REQUESTED. Your previous unit list was:\n" + str(prev)[:6000]
                        + "\nProblems found mechanically:\n- " + "\n- ".join(pr or ["no usable units were returned"])
                        + "\nReturn the complete corrected unit list.\n")
                reqs.append(request(h, note))
            for (h, pr), res in zip(todo, ctx.llm.call_many(reqs)):
                second = _parse_units(h, res, anchor_text)
                if second and len(_problems(second)) <= len(pr):
                    per_h[h["id"]] = second
                    revised.append(h["id"])
    units = []
    demoted = 0
    for h in hyps:
        for u in per_h[h["id"]]:
            typ, qc = u["type"], u["quote_check"]
            reason = ""
            if lint and typ == "REQUIRED_SUPPORT" and verdict_sized(u["text"]):
                # still a verdict after one revision: it stays visible but cannot be a coverage requirement
                u["derived_type"] = typ
                typ = u["type"] = "EVALUATIVE_JUDGMENT"
                reason = ("verdict-sized after one revision (\"" + verdict_sized(u["text"]) + "\"): recorded as an "
                          "evaluative judgment; no single finding could establish it")
                demoted += 1
            active = typ in MATCHABLE and qc["found"]
            u["active"] = active
            u["inactive_reason"] = ("" if active else reason or (
                "evaluative judgment: reported, not matched" if typ == "EVALUATIVE_JUDGMENT"
                else "source_quote not found verbatim in the frozen hypothesis/header text (unanchored)"))
            units.append(u)
    ctx.save("frame", "coverage-units.json", units, "coverage-units")
    ctx.save("matching", "01_hypothesis-units/units.json", units, "coverage-units")
    by_h = {}
    for u in units:
        by_h.setdefault(u["hypothesis_id"], {}).setdefault(u["type"], 0)
        by_h[u["hypothesis_id"]][u["type"]] += 1
    no_required = [h["id"] for h in hyps
                   if not any(u["active"] and u["type"] == "REQUIRED_SUPPORT" for u in per_h[h["id"]])]
    return {"units": len(units), "active": sum(1 for u in units if u["active"]),
            "unanchored": sum(1 for u in units if u["type"] != "EVALUATIVE_JUDGMENT" and not u["active"]),
            "revised_hypotheses": revised, "verdict_sized_demoted": demoted,
            "hypotheses_without_required_units": no_required,
            "by_hypothesis": by_h}
