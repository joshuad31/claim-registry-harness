"""The premise ledger: what each hypothesis rests on, and where each part stands.

It is computed mechanically from the approved matching record; nothing here is a model judgment.
For every active unit of every hypothesis it lists the witnesses that establish it, cover it under a
named transfer assumption, cover it partly, or contradict it, and gives the unit one status:

* ESTABLISHED               at least one complete match (or approved joint group), no contradiction
* CONTESTED                 at least one complete match AND at least one contradiction
* CONTESTED_IF_TRANSFERRED  at least one complete match, and contradictions that all hold only if a
                            finding from another population, species, model or dose transfers
* SUPPORTED_WITH_ASSUMPTION no complete match; a finding with the same effect in another population,
                            species, model or dose (gap_type SCOPE)
* PARTIAL_ONLY              only partial matches of another kind
* CONTRADICTED              contradictions only
* CONTRADICTED_IF_TRANSFERRED  only contradictions that hold if a finding from another scope transfers
* BOUNDARY                  a constraint that says what the hypothesis is about.  Nothing can refute
                            it; findings from outside it are listed as outside the hypothesis's scope
* UNADDRESSED               nothing judged relevant

A CONTESTED required unit is where the evidence itself disagrees: those are the places to look for a
crux.  An UNADDRESSED or assumption-dependent unit of an affirmative hypothesis is what an
"unresolved" rival rests on.

Support and contradiction are held to one standard: a finding from another scope supports a unit
only if a transfer is granted (SUPPORTED_WITH_ASSUMPTION) and counts against it only if a transfer
is granted (the two ..._IF_TRANSFERRED statuses).  ``contradicted_by`` lists outright contradictions
only; conditional ones are in ``contradicted_if_transferred`` with the transfer each depends on.
"""

from __future__ import annotations

from .matching import COMPLETE, relations_index
from .util import atomic_write_text, truncate_words, utcnow

STATUSES = ("ESTABLISHED", "CONTESTED", "CONTESTED_IF_TRANSFERRED", "SUPPORTED_WITH_ASSUMPTION", "PARTIAL_ONLY",
            "CONTRADICTED", "CONTRADICTED_IF_TRANSFERRED", "UNADDRESSED")


def build_ledger(units: list[dict], rel: dict, groups: list[dict], coverage: dict,
                 assume_gaps: tuple = ("SCOPE",), constraint_kinds: dict | None = None) -> dict:
    from .units import constraint_kind
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
        contra = [(w, r) for w, r in rows if r["final"] == "CONTRADICTS"]
        kind = constraint_kind(u, constraint_kinds)
        outside = []
        if kind == "BOUNDARY":
            # nothing refutes a boundary: a finding "contrary" to it is about something else
            outside, contra = [w for w, _ in contra], []
        against = [w for w, r in contra if r.get("gap_type") != "SCOPE"]
        against_if = [{"witness_id": w, "transfer": (r.get("gap") or "").strip()
                       or "the finding transfers to the scope this unit is about"}
                      for w, r in contra if r.get("gap_type") == "SCOPE"]
        if kind == "BOUNDARY":
            status = "BOUNDARY"
        elif (full or joint) and against:
            status = "CONTESTED"
        elif (full or joint) and against_if:
            status = "CONTESTED_IF_TRANSFERRED"
        elif full or joint:
            status = "ESTABLISHED"
        elif assumed:
            status = "SUPPORTED_WITH_ASSUMPTION"
        elif against:
            status = "CONTRADICTED"
        elif against_if:
            status = "CONTRADICTED_IF_TRANSFERRED"
        elif partial:
            status = "PARTIAL_ONLY"
        else:
            status = "UNADDRESSED"
        out.setdefault(u["hypothesis_id"], []).append({
            "unit_id": uid, "type": u["type"], "text": u["text"], "serves": u.get("serves", ""),
            "status": status, "established_by": full, "joint_groups": joint, "assumed_from": assumed,
            "partial": partial, "contradicted_by": against, "contradicted_if_transferred": against_if,
            **({"constraint_kind": kind, "outside_scope": outside} if kind else {}),
            "pairs_judged": len(rows)})
    summary = {}
    for hid, rows in out.items():
        req = [r for r in rows if r["type"] == "REQUIRED_SUPPORT"]
        summary[hid] = {
            "coverage_status": (coverage.get(hid) or {}).get("status", ""),
            "required": {s: sum(1 for r in req if r["status"] == s) for s in STATUSES},
            "adverse_findings_realized": [r["unit_id"] for r in rows if r["type"] == "ADVERSE_TEST"
                                          and r["status"] in ("ESTABLISHED", "CONTESTED", "CONTESTED_IF_TRANSFERRED")],
            "expectations_met": [r["unit_id"] for r in rows if r["type"] == "CORROBORATING_EXPECTATION"
                                 and r["status"] in ("ESTABLISHED", "CONTESTED", "CONTESTED_IF_TRANSFERRED")],
            "constraints_contradicted": [r["unit_id"] for r in rows if r["type"] == "CONTEXTUAL_CONSTRAINT"
                                         and r["contradicted_by"]],
            "constraints_contradicted_if_transferred": [
                r["unit_id"] for r in rows if r["type"] == "CONTEXTUAL_CONSTRAINT"
                and r["contradicted_if_transferred"] and not r["contradicted_by"]],
            "boundaries": [r["unit_id"] for r in rows if r.get("constraint_kind") == "BOUNDARY"]}
    return {"hypotheses": out, "summary": summary, "time": utcnow(),
            "statuses": "see claimreg/ledger.py module docstring"}


_LABEL = {"ESTABLISHED": "established", "CONTESTED": "CONTESTED", "CONTESTED_IF_TRANSFERRED":
          "established; contested only if a finding from another scope transfers",
          "SUPPORTED_WITH_ASSUMPTION": "supported if a transfer is granted", "PARTIAL_ONLY": "partly supported",
          "CONTRADICTED": "contradicted", "CONTRADICTED_IF_TRANSFERRED":
          "contradicted only if a finding from another scope transfers",
          "BOUNDARY": "defines the scope; nothing here can refute it",
          "UNADDRESSED": "not addressed by any released witness"}
_TYPE = {"REQUIRED_SUPPORT": "Required", "CONTEXTUAL_CONSTRAINT": "Constraint", "ADVERSE_TEST":
         "Would count against", "CORROBORATING_EXPECTATION": "Expected"}


def render_ledger(frame: dict, ledger: dict, coverage: dict, witnesses: dict, units: list[dict]) -> str:
    L = ["# Premise ledger", "",
         "What each hypothesis rests on, and where each part stands in this run. It is computed from the "
         "matching record; nothing here is a model's overall judgment. A *required* part must be covered for the "
         "hypothesis to have complete coverage. A part marked CONTESTED has both a finding that establishes it and "
         "a finding that contradicts it: that is where the sources disagree. A finding from another population, "
         "species, model or dose supports a part only if a transfer is granted, and counts against a part only if "
         "a transfer is granted; both are marked. A constraint labelled *the hypothesis is about* is a boundary: "
         "a study from outside it is out of scope, not a contradiction.", ""]

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
                    label = "The hypothesis is about" if r.get("constraint_kind") == "BOUNDARY" else _TYPE[typ]
                    L.append(f"- **{label}** `{r['unit_id']}` - {_LABEL[r['status']]}: {r['text']}")
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
                    for a in r.get("contradicted_if_transferred", [])[:3]:
                        L.append(f"  - counts against it if the finding transfers "
                                 f"(\"{truncate_words(a['transfer'], 40)}\"): {wtxt(a['witness_id'])}")
                    for w in r.get("outside_scope", [])[:3]:
                        L.append(f"  - outside this hypothesis's scope: {wtxt(w)}")
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
                for a in s.get("contrary_assumed_not_to_transfer", []):
                    L.append(f"  - assumes the contrary finding of `{a['witness_id']}` against `{a['constraint_id']}` "
                             f"does not transfer: {truncate_words(a['transfer'], 45)}")
                for a in s.get("transfer_conflicts", []):
                    L.append(f"  - TRANSFER CONFLICT, for a reader to judge: `{a['witness_id']}` is granted a "
                             f"transfer to cover `{a['unit_id']}` and denied one against "
                             + ", ".join(f"`{c['constraint_id']}`" for c in a["contrary"]))
            L.append("")
    return "\n".join(L) + "\n"


def write_ledger(ctx, coverage: dict) -> dict:
    units = ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or []
    groups = ctx.load("matching", "03_match-records/joint-groups.json", default=[]) or []
    assume = tuple(ctx.cfg["coverage"].get("assume_gaps") or [])
    led = build_ledger(units, relations_index(ctx), groups, coverage, assume,
                       dict(ctx.cfg["coverage"].get("constraint_kinds") or {}))
    ctx.save("coverage", "premise-ledger.json", led, "premise-ledger")
    ws = {w["witness_id"]: w for w in (ctx.load("witnesses", "05_released/witnesses.json", default=[]) or [])}
    atomic_write_text(ctx.p("coverage", "PREMISE-LEDGER.md"), render_ledger(ctx.frame, led, coverage, ws, units))
    return {h: {k: v for k, v in s["required"].items() if v} for h, s in led["summary"].items()}
