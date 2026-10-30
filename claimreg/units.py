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


def derive_units(ctx) -> dict:
    frame = ctx.frame
    header_text = read_text(ctx.p("frame", "header.md")) if ctx.p("frame", "header.md").exists() else ""
    defs = header_definitions(frame, header_text)
    hyps = all_hypotheses(frame)
    reqs = []
    for h in hyps:
        rivals = [x for x in hyps if x["axis_id"] == h["axis_id"] and x["id"] != h["id"]]
        system, user, _ = ctx.prompts.render(
            "units_derive.md", AXIS_ID=h["axis_id"], AXIS_QUESTION=h.get("axis_question", ""),
            AXIS_BOUNDARY=h.get("axis_boundary", "") or "(none)", AXIS_SCOPE=h.get("axis_scope", "") or "(none)",
            RIVALS="; ".join(f"{r['id']}: {truncate_words(r.get('statement', ''), 40)}" for r in rivals) or "(none)",
            HID=h["id"], HYPOTHESIS_TEXT=hypothesis_text(h), HEADER_DEFINITIONS=defs)
        reqs.append(LLMRequest(role="unit_deriver", system=system, user=user, tag=f"units:{h['id']}",
                               meta={"hypothesis": h}))
    results = ctx.llm.call_many(reqs)
    anchor_text = "\n".join(hypothesis_text(h) for h in hyps) + "\n" + header_text + "\n" + defs
    units = []
    for h, res in zip(hyps, results):
        data = res.parsed if res and isinstance(res.parsed, dict) else {}
        seen = set()
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
            active = typ in MATCHABLE and qc["found"]
            units.append({
                "unit_id": uid, "hypothesis_id": h["id"], "axis_id": h["axis_id"], "type": typ,
                "text": u["text"].strip(), "source_quote": quote, "quote_check": qc,
                "evidence_terms": [t for t in (u.get("evidence_terms") or []) if isinstance(t, str)],
                "satisfied_by": u.get("satisfied_by", ""), "active": active,
                "inactive_reason": ("" if active else ("evaluative judgment: reported, not matched"
                                                       if typ == "EVALUATIVE_JUDGMENT"
                                                       else "source_quote not found verbatim in the frozen "
                                                            "hypothesis/header text (unanchored)")),
                "call_key": res.key if res else ""})
    ctx.save("frame", "coverage-units.json", units, "coverage-units")
    ctx.save("matching", "01_hypothesis-units/units.json", units, "coverage-units")
    by_h = {}
    for u in units:
        by_h.setdefault(u["hypothesis_id"], {}).setdefault(u["type"], 0)
        by_h[u["hypothesis_id"]][u["type"]] += 1
    return {"units": len(units), "active": sum(1 for u in units if u["active"]),
            "unanchored": sum(1 for u in units if u["type"] != "EVALUATIVE_JUDGMENT" and not u["active"]),
            "by_hypothesis": by_h}
