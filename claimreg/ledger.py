"""The premise ledger: what each hypothesis rests on, and where each part stands.

It is computed mechanically from the approved matching record; nothing here is a model judgment.
For every active unit of every hypothesis it lists the witnesses that establish it, cover it under a
named transfer assumption, cover it partly, or contradict it, and gives the unit one status:

* ESTABLISHED               at least one complete match (or approved joint group), no contradiction
* CONTESTED                 at least one complete match AND at least one contradiction
* SUPPORTED_WITH_ASSUMPTION no complete match; a finding with the same effect in another population,
                            species, model or dose (gap_type SCOPE)
* PARTIAL_ONLY              only partial matches of another kind
* CONTRADICTED              contradictions only
* UNADDRESSED               nothing judged relevant

A CONTESTED required unit is where the evidence itself disagrees: those are the places to look for a
crux.  An UNADDRESSED or assumption-dependent unit of an affirmative hypothesis is what an
"unresolved" rival rests on.
"""

from __future__ import annotations

from .matching import COMPLETE, relations_index
from .util import atomic_write_text, truncate_words, utcnow

STATUSES = ("ESTABLISHED", "CONTESTED", "SUPPORTED_WITH_ASSUMPTION", "PARTIAL_ONLY", "CONTRADICTED",
            "UNADDRESSED")


def build_ledger(units: list[dict], rel: dict, groups: list[dict], coverage: dict,
                 assume_gaps: tuple = ("SCOPE",)) -> dict:
    by_unit: dict = {}
    for (w, uid), r in rel.items():
        by_unit.setdefault(uid, []).append((w, r))
    out: dict = {}
    for u in units:
        if not u.get("active"):
            continue
        uid = u["unit_id"]
        rows = sorted(by_unit.get(uid, []), key=lambda t: t[0])
        full = [w for w, r in rows if r["final"] in COMPLETE]
        joint = [g["witnesses"] for g in groups if g.get("approved") and g["unit_id"] == uid]
        assumed = [{"witness_id": w, "assumption": r.get("gap") or r.get("trace", "")} for w, r in rows
                   if r["final"] == "PARTIALLY_COVERS" and r.get("gap_type") in assume_gaps]
        partial = [{"witness_id": w, "gap_type": r.get("gap_type", ""), "gap": r.get("gap", "")} for w, r in rows
                   if r["final"] in ("PARTIALLY_COVERS", "UNIT_ENTAILS_WITNESS")
                   and not (r["final"] == "PARTIALLY_COVERS" and r.get("gap_type") in assume_gaps)]
        against = [w for w, r in rows if r["final"] == "CONTRADICTS"]
        if (full or joint) and against:
            status = "CONTESTED"
        elif full or joint:
            status = "ESTABLISHED"
        elif assumed:
            status = "SUPPORTED_WITH_ASSUMPTION"
        elif against:
            status = "CONTRADICTED"
        elif partial:
            status = "PARTIAL_ONLY"
        else:
            status = "UNADDRESSED"
        out.setdefault(u["hypothesis_id"], []).append({
            "unit_id": uid, "type": u["type"], "text": u["text"], "serves": u.get("serves", ""),
            "status": status, "established_by": full, "joint_groups": joint, "assumed_from": assumed,
            "partial": partial, "contradicted_by": against, "pairs_judged": len(rows)})
    summary = {}
    for hid, rows in out.items():
        req = [r for r in rows if r["type"] == "REQUIRED_SUPPORT"]
        summary[hid] = {
            "coverage_status": (coverage.get(hid) or {}).get("status", ""),
            "required": {s: sum(1 for r in req if r["status"] == s) for s in STATUSES},
            "adverse_findings_realized": [r["unit_id"] for r in rows if r["type"] == "ADVERSE_TEST"
                                          and r["status"] in ("ESTABLISHED", "CONTESTED")],
            "expectations_met": [r["unit_id"] for r in rows if r["type"] == "CORROBORATING_EXPECTATION"
                                 and r["status"] in ("ESTABLISHED", "CONTESTED")],
            "constraints_contradicted": [r["unit_id"] for r in rows if r["type"] == "CONTEXTUAL_CONSTRAINT"
                                         and r["contradicted_by"]]}
    return {"hypotheses": out, "summary": summary, "time": utcnow(),
            "statuses": "see claimreg/ledger.py module docstring"}


_LABEL = {"ESTABLISHED": "established", "CONTESTED": "CONTESTED", "SUPPORTED_WITH_ASSUMPTION":
          "supported if a transfer is granted", "PARTIAL_ONLY": "partly supported", "CONTRADICTED":
          "contradicted", "UNADDRESSED": "not addressed by any released witness"}
_TYPE = {"REQUIRED_SUPPORT": "Required", "CONTEXTUAL_CONSTRAINT": "Constraint", "ADVERSE_TEST":
         "Would count against", "CORROBORATING_EXPECTATION": "Expected"}


def render_ledger(frame: dict, ledger: dict, coverage: dict, witnesses: dict, units: list[dict]) -> str:
    L = ["# Premise ledger", "",
         "What each hypothesis rests on, and where each part stands in this run. It is computed from the "
         "matching record; nothing here is a model's overall judgment. A *required* part must be covered for the "
         "hypothesis to have complete coverage. A part marked CONTESTED has both a finding that establishes it and "
         "a finding that contradicts it: that is where the sources disagree.", ""]

    def wtxt(w):
        x = witnesses.get(w, {})
        return f"`{w}` ({x.get('source_file', '?')}): {truncate_words(x.get('text', ''), 45)}"
    for ax in frame["axes"]:
        L += [f"## Axis {ax['axis_id']}: {truncate_words(ax.get('question', ''), 45)}", ""]
        for h in ax["hypotheses"]:
            cov = coverage.get(h["id"], {})
            L += [f"### {h['id']} - {h.get('title', '')}", "",
                  f"Coverage: **{cov.get('status', 'n/a')}**" + (f" ({len(cov.get('sets', []))} minimal set(s))"
                                                                   if cov.get("sets") else ""), ""]
            if cov.get("note"):
                L += [cov["note"], ""]
            rows = ledger["hypotheses"].get(h["id"], [])
            for typ in ("REQUIRED_SUPPORT", "CONTEXTUAL_CONSTRAINT", "ADVERSE_TEST", "CORROBORATING_EXPECTATION"):
                for r in [x for x in rows if x["type"] == typ]:
                    L.append(f"- **{_TYPE[typ]}** `{r['unit_id']}` - {_LABEL[r['status']]}: {r['text']}")
                    for w in r["established_by"][:3]:
                        L.append(f"  - establishes it: {wtxt(w)}")
                    for g in r["joint_groups"][:2]:
                        L.append("  - jointly establish it: " + " + ".join(f"`{w}`" for w in g))
                    if not r["established_by"]:
                        for a in r["assumed_from"][:3]:
                            L.append(f"  - supports it if you grant \"{truncate_words(a['assumption'], 40)}\": "
                                     f"{wtxt(a['witness_id'])}")
                    for w in r["contradicted_by"][:3]:
                        L.append(f"  - contradicts it: {wtxt(w)}")
                    if r["status"] == "PARTIAL_ONLY":
                        for p in r["partial"][:2]:
                            L.append(f"  - partly: {wtxt(p['witness_id'])}"
                                     + (f" (missing: {truncate_words(p['gap'], 30)})" if p.get("gap") else ""))
            ev = [u for u in units if u["hypothesis_id"] == h["id"] and u["type"] == "EVALUATIVE_JUDGMENT"]
            for u in ev:
                L.append(f"- **Judgment left to the analyst** `{u['unit_id']}`: {u['text']}")
            if cov.get("sets"):
                s = cov["sets"][0]
                L += ["", f"Example minimal set `{s['set_id']}`: " + ", ".join(f"`{w}`" for w in s["witnesses"])]
                for a in s.get("assumptions", []):
                    L.append(f"  - assumes for `{a['unit_id']}`: {truncate_words(a['assumption'], 45)}")
            L.append("")
    return "\n".join(L) + "\n"


def write_ledger(ctx, coverage: dict) -> dict:
    units = ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or []
    groups = ctx.load("matching", "03_match-records/joint-groups.json", default=[]) or []
    assume = tuple(ctx.cfg["coverage"].get("assume_gaps") or [])
    led = build_ledger(units, relations_index(ctx), groups, coverage, assume)
    ctx.save("coverage", "premise-ledger.json", led, "premise-ledger")
    ws = {w["witness_id"]: w for w in (ctx.load("witnesses", "05_released/witnesses.json", default=[]) or [])}
    atomic_write_text(ctx.p("coverage", "PREMISE-LEDGER.md"), render_ledger(ctx.frame, led, coverage, ws, units))
    return {h: {k: v for k, v in s["required"].items() if v} for h, s in led["summary"].items()}
