"""`cr funnel`: where a run loses material, stage by stage.

Everything is read from the run's saved records.  It answers the question "why did this run end
with no coverage?" by showing the largest drop and the reasons recorded for it.
"""

from __future__ import annotations

from collections import Counter


def funnel(ctx) -> dict:
    ld = ctx.load
    responses = ld("discovery", "02_query-responses/responses.json", default=[]) or []
    cands = ld("frds", "01_candidates/candidates.json", default=[]) or []
    vals = ld("frds", "04_validation-results/validations.json", default=[]) or []
    retained = ld("frds", "05_validated/retained-frds.json", default=None)
    if retained is None:
        retained = ld("frds", "05_validated/validated-frds.json", default=[]) or []
    released = ld("witnesses", "05_released/witnesses.json", default=[]) or []
    held = ld("witnesses", "04_repaired-or-held/held.json", default=[]) or []
    units = ld("matching", "01_hypothesis-units/units.json", default=[]) or []
    rels = ld("matching", "03_match-records/relations.json", default=[]) or []
    msum = ld("matching", "03_match-records/summary.json", default={}) or {}
    groups = ld("matching", "03_match-records/joint-groups.json", default=[]) or []
    cov = (ld("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
    crux = ld("crux", "05_candidates/crux-candidates.json", default={}) or {}
    active = [u for u in units if u.get("active")]
    req = [u for u in active if u["type"] == "REQUIRED_SUPPORT"]
    from .units import verdict_sized
    verdicts = [u["unit_id"] for u in req if verdict_sized(u["text"])]
    held_why = Counter()
    for h in held:
        why = str(h.get("held_reason", "held"))
        held_why["audit asked for a revision" if "REVISE" in why else
                 "constructor abstained" if why.startswith("ABSTAIN") else
                 "FRD needs repair" if "REPAIR_FRD" in why else
                 "over the word ceiling or an unlicensed number" if "mechanical" in why else why[:40]] += 1
    out = {
        "run": ctx.run_id,
        "stages": [
            ("usable answers", sum(1 for r in responses if r.get("usable", True)) if responses else None),
            ("candidate FRDs", len(cands)),
            ("FRDs that passed source validation (READY)",
             sum(1 for v in vals if str(v.get("readiness", "")).startswith("READY")) if vals else None),
            ("FRDs retained", len(retained)),
            ("witnesses released", len(released)),
            ("witnesses held", len(held)),
            ("active units", len(active)),
            ("required units", len(req)),
            ("witness-unit pairs judged", len(rels)),
            ("pairs never judged (outside the shortlist)", msum.get("pairs_not_assessed_prefilter")),
            ("complete relations", sum(1 for r in rels if r.get("final") in ("EQUIVALENT", "WITNESS_ENTAILS_UNIT"))),
            ("partial relations", sum(1 for r in rels if r.get("final") in ("PARTIALLY_COVERS", "UNIT_ENTAILS_WITNESS"))),
            ("contradictions", sum(1 for r in rels if r.get("final") == "CONTRADICTS")),
            ("approved joint groups", sum(1 for g in groups if g.get("approved"))),
            ("hypotheses with a coverage set", sum(1 for c in cov.values() if c.get("sets"))),
            ("crux candidates", len(crux.get("candidates", []))),
        ],
        "held_reasons": dict(held_why.most_common()),
        "relations": dict(Counter(r.get("final") for r in rels).most_common()),
        "coverage": {h: {"status": c.get("status"), "required_units": len(c.get("required_units", [])),
                         "covered": c.get("units_covered", 0), "sets": len(c.get("sets", []))}
                     for h, c in cov.items()},
        "verdict_sized_required_units": verdicts,
    }
    findings = []
    if retained and len(released) < 0.5 * len(retained):
        findings.append(f"Witness stage: only {len(released)} of {len(retained)} retained FRDs became witnesses. "
                        f"Largest recorded reasons: " + "; ".join(f"{k} ({v})" for k, v in held_why.most_common(3)) + ".")
    if verdicts:
        findings.append(f"Units: {len(verdicts)} of {len(req)} required units are verdict-sized (they describe the "
                        f"evidence base, which no single finding can establish): {', '.join(verdicts[:8])}"
                        + (" ..." if len(verdicts) > 8 else "") + ". Re-derive units with a model "
                        "(`cr run <project> --from units`).")
    na = msum.get("pairs_not_assessed_prefilter") or 0
    if rels and na > 2 * len(rels):
        findings.append(f"Matching: {na} witness-unit pairs were never judged because the shortlist left them out "
                        f"({len(rels)} were judged). With a model matcher, model routing judges the relevant ones.")
    if rels and not any(r.get("final") in ("EQUIVALENT", "WITNESS_ENTAILS_UNIT") for r in rels):
        findings.append("Matching: no pair was judged a complete match, so no required unit has an option and no "
                        "coverage set can form.")
    out["findings"] = findings
    return out


def render(f: dict) -> str:
    L = [f"Funnel for run {f['run']}", ""]
    for name, n in f["stages"]:
        if n is not None:
            L.append(f"  {n:>7,}  {name}")
    if f["held_reasons"]:
        L += ["", "Held witnesses, by recorded reason:"] + [f"  {v:>7,}  {k}" for k, v in f["held_reasons"].items()]
    if f["coverage"]:
        L += ["", "Coverage:"] + [f"  {h}: {c['status']} ({c['covered']}/{c['required_units']} required units, "
                                  f"{c['sets']} set(s))" for h, c in f["coverage"].items()]
    L += ["", "What is limiting this run:"] + ([f"  - {x}" for x in f["findings"]] or ["  - nothing flagged"])
    return "\n".join(L) + "\n"
