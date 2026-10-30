"""Crux identification: frozen rival theories, membership screening, T1/T2 (spec 29.1-30).

Definitions used by this harness (the specification leaves some of them
open; each is stated so it can be attacked):

* Rivals are the other hypotheses on the same axis.
* Frozen rival theory B_r: r's active REQUIRED_SUPPORT units with their
  approved options, CONTEXTUAL_CONSTRAINT units, CORROBORATING_EXPECTATION and
  ADVERSE_TEST units, approved incompatibilities and joint-group dependencies.
  It is compiled once, hashed, and frozen before any test runs.
* "w contradicts X" means the approved matching record holds CONTRADICTS for
  (w, X).  "w realizes a falsifier of r" means EQUIVALENT/WITNESS_ENTAILS_UNIT
  for (w, an ADVERSE_TEST unit of r).
* T1 (consistency) FAILS when w contradicts any unit r asserts (required,
  constraint or corroborating expectation) or realizes one of r's recorded
  falsifiers.  Certificate: the conflicting rule bundle (units + match records).
* T2 (coverage) FAILS when, once w is established, r loses coverage it needs:
  (a) w contradicts one of r's REQUIRED_SUPPORT units, so no option for that
  unit can be held alongside w; or (b) every existing option for some required
  unit of r contains a witness approved-incompatible with w.  T2 is a
  counterfactual about what w removes: when r already lacks options for a unit
  regardless of w, that incompleteness is reported in the certificate and is
  not attributed to w.  PASS certificates give an example arrangement.
* UNKNOWN is returned when a needed relation was never judged (the
  completion-matching step exists to prevent this); it is never converted
  into PASS or FAIL.
* Crux candidate: w is in at least one deletion-minimal set of its home
  hypothesis, appears in none of the rival's formed sets (membership
  screening), and FAILS both T1 and T2 against that rival.

Extended review (spec Optional Route B, clearly separated in the report):
when the home hypothesis has no complete coverage, witnesses that fully cover
at least one of its required units are tested the same way and reported as
"diagnostic witnesses" - never as crux candidates.
"""

from __future__ import annotations

from .matching import COMPLETE, completion_match, relations_index
from .util import digest, utcnow

PASS, FAIL, UNKNOWN = "PASS", "FAIL", "UNKNOWN"


def compile_theory(hid: str, units: list[dict], cov: dict, incompat: list[dict]) -> dict:
    mine = [u for u in units if u["hypothesis_id"] == hid and u.get("active")]
    body = {
        "hypothesis_id": hid,
        "required": [u["unit_id"] for u in mine if u["type"] == "REQUIRED_SUPPORT"],
        "constraints": [u["unit_id"] for u in mine if u["type"] == "CONTEXTUAL_CONSTRAINT"],
        "corroborating": [u["unit_id"] for u in mine if u["type"] == "CORROBORATING_EXPECTATION"],
        "adverse": [u["unit_id"] for u in mine if u["type"] == "ADVERSE_TEST"],
        "options": cov.get("options", {}),
        "incompatibilities": sorted([sorted([r["a"], r["b"]]) for r in incompat if r.get("approved")]),
        "dependencies": [o["witnesses"] for opts in cov.get("options", {}).values() for o in opts if o.get("joint")],
    }
    body["theory_id"] = "BTHEORY-" + digest(body)
    return body


def _rel(rel, w, u):
    """The approved relation, or None when it is unknown: never judged, or judged ABSTAIN
    (undecidable, disputed without adjudication, missing, or one pass only under 'abstain')."""
    r = rel.get((w, u))
    if not r or r.get("final") in (None, "ABSTAIN", "MISSING"):
        return None
    return r["final"]


def test_t1(w: str, th: dict, rel: dict, missing_is_none: bool = False) -> tuple[str, dict]:
    hits, unknown, checked = [], [], []
    for group, units in (("required", th["required"]), ("constraint", th["constraints"]),
                         ("corroborating", th["corroborating"])):
        for u in units:
            f = _rel(rel, w, u)
            checked.append(u)
            if f is None:
                unknown.append(u)
            elif f == "CONTRADICTS":
                r = rel[(w, u)]
                hits.append({"unit_id": u, "unit_group": group, "relation": f, "basis": r["basis"],
                             "trace": r.get("trace", "")})
    for u in th["adverse"]:
        f = _rel(rel, w, u)
        checked.append(u)
        if f is None:
            unknown.append(u)
        elif f in COMPLETE:
            r = rel[(w, u)]
            hits.append({"unit_id": u, "unit_group": "adverse_test_realized", "relation": f,
                         "basis": r["basis"], "trace": r.get("trace", "")})
    if hits:
        return FAIL, {"kind": "T1_cannot_be_accommodated", "conflicting_rule_bundle": hits,
                      "why": "the witness contradicts content the rival asserts or realizes one of its "
                             "recorded falsifiers"}
    if unknown and not missing_is_none:
        return UNKNOWN, {"kind": "T1_unknown", "unjudged_units": unknown,
                         "why": "relations needed for this test were never judged"}
    return PASS, {"kind": "T1_accommodated", "units_checked": checked,
                  "unjudged_treated_as_no_relation": unknown,
                  "why": "no CONTRADICTS relation with any asserted unit and no realized falsifier"
                         + ("; some rival units were outside the diagnostic shortlist" if unknown else "")}


def test_t2(w: str, th: dict, rel: dict, incompat: set, missing_is_none: bool = False) -> tuple[str, dict]:
    forbidden, blocked, rival_gaps, unknown = [], [], [], []
    for u in th["required"]:
        f = _rel(rel, w, u)
        if f is None:
            unknown.append(u)
        if f == "CONTRADICTS":
            r = rel[(w, u)]
            forbidden.append({"unit_id": u, "trace": r.get("trace", ""), "basis": r["basis"]})
            continue
        opts = th["options"].get(u, [])
        if not opts:
            rival_gaps.append(u)
            continue
        surviving = [o for o in opts if not any(frozenset((w, x)) in incompat for x in o["witnesses"])]
        if not surviving:
            blocked.append({"unit_id": u, "options_removed": [o["option_id"] for o in opts],
                            "why": "every option contains a witness approved-incompatible with this witness"})
    if forbidden or blocked:
        return FAIL, {"kind": "T2_cannot_be_accommodated", "required_units_forbidden": forbidden,
                      "required_units_blocked_by_incompatibility": blocked,
                      "rival_units_already_without_options": rival_gaps,
                      "why": "once the witness is established the rival cannot cover these required units"}
    if unknown and not missing_is_none:
        return UNKNOWN, {"kind": "T2_unknown", "unjudged_required_units": unknown,
                         "rival_units_already_without_options": rival_gaps,
                         "why": "whether the witness contradicts these required units was never decided"}
    example = {u: next((o["option_id"] for o in th["options"].get(u, [])
                        if not any(frozenset((w, x)) in incompat for x in o["witnesses"])), None)
               for u in th["required"]}
    return PASS, {"kind": "T2_accommodated", "example_arrangement": example,
                  "rival_units_already_without_options": rival_gaps,
                  "why": "the witness removes no option the rival needs"
                         + ("; the rival is already incomplete on the listed units, independent of this witness"
                            if rival_gaps else "")}


def _home_sets(cov_all: dict) -> tuple[dict, dict]:
    home_sets = {h: [w for s in c.get("sets", []) for w in s["witnesses"]] for h, c in cov_all.items()}
    partial_home = {}
    for h, c in cov_all.items():
        if c.get("status") != "COMPLETE":
            ws = set()
            for u in c.get("required_units", []):
                for o in c.get("options", {}).get(u, []):
                    ws.update(o["witnesses"])
            partial_home[h] = sorted(ws)
    return home_sets, partial_home


def crux_stage(ctx) -> dict:
    frame = ctx.frame
    units = ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or []
    from .joint import incompatibility_records
    inc_recs = incompatibility_records(ctx)
    incompat = {frozenset((r["a"], r["b"])) for r in inc_recs if r.get("approved")}
    axis_of = {h["id"]: ax["axis_id"] for ax in frame["axes"] for h in ax["hypotheses"]}
    rivals = {h["id"]: [x["id"] for x in ax["hypotheses"] if x["id"] != h["id"]]
              for ax in frame["axes"] for h in ax["hypotheses"]}

    # completion matching: crux-candidate witnesses are judged against EVERY rival unit;
    # diagnostic (extended-review) witnesses against a lexical shortlist of rival units.
    # A newly judged pair can add a coverage option or a constraint veto, so coverage is
    # recomputed and completion repeated until nothing changes (sets never go stale).
    recomputed = 0
    for _round in range(4):
        cov_all = (ctx.load("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
        home_sets, partial_home = _home_sets(cov_all)
        if not ctx.cfg["crux"].get("completion_matching", True):
            break
        from .matching import matching_texts
        from .util import tokens as _tok
        wtexts, utexts, _ = matching_texts(ctx)
        need = set()
        rival_units = {h: [u["unit_id"] for u in units if u["hypothesis_id"] == h and u.get("active")]
                       for h in rivals}
        m = int(ctx.cfg["crux"].get("diagnostic_units_per_rival", 8))
        for h in rivals:
            for w in set(home_sets.get(h, [])):
                for r in rivals[h]:
                    for uid in rival_units.get(r, []):
                        need.add((w, uid))
            for w in set(partial_home.get(h, [])) - set(home_sets.get(h, [])):
                wt = set(_tok(wtexts.get(w, "")))
                for r in rivals[h]:
                    ranked = sorted(rival_units.get(r, []),
                                    key=lambda uid: (-len(wt & set(_tok(utexts.get(uid, "")))), uid))
                    for uid in ranked[:m]:
                        need.add((w, uid))
        new = completion_match(ctx, need) if need else []
        if not new:
            break
        ctx.log(f"crux: completion matching judged {len(new)} additional witness-unit pairs")
        from .matching import write_review_packet
        write_review_packet(ctx)
        if not any(r.get("final") in COMPLETE + ("CONTRADICTS",) for r in new):
            break
        from .coverage import coverage_stage
        coverage_stage(ctx)
        recomputed += 1
        ctx.log("crux: coverage recomputed with the newly judged pairs")
    cov_all = (ctx.load("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
    home_sets, partial_home = _home_sets(cov_all)
    rel = relations_index(ctx)

    theories = {h: compile_theory(h, units, cov_all.get(h, {}), inc_recs) for h in rivals}
    ctx.save("crux", "01_frozen-rival-theories/theories.json", theories, "frozen-rival-theories")

    rival_members = {h: set(home_sets.get(h, [])) for h in rivals}
    tests, candidates, conflict_recorded, diagnostic = [], [], [], []
    for home in rivals:
        for kind, wlist in (("crux", sorted(set(home_sets.get(home, [])))),
                            ("diagnostic", partial_home.get(home, []))):
            for w in wlist:
                defeats = []
                for r in rivals[home]:
                    th = theories[r]
                    t1, c1 = test_t1(w, th, rel, missing_is_none=(kind == "diagnostic"))
                    t2, c2 = test_t2(w, th, rel, incompat, missing_is_none=(kind == "diagnostic"))
                    member = w in rival_members.get(r, set())
                    is_crux = (kind == "crux") and (not member) and t1 == FAIL and t2 == FAIL
                    row = {"witness_id": w, "home": home, "rival": r, "axis": axis_of[home], "kind": kind,
                           "membership_screen_passes": not member, "t1": t1, "t2": t2,
                           "t1_certificate": c1, "t2_certificate": c2, "crux": is_crux,
                           "tests_failed": int(t1 == FAIL) + int(t2 == FAIL), "theory_id": th["theory_id"]}
                    tests.append(row)
                    if is_crux:
                        defeats.append(r)
                    elif kind == "crux" and not member and row["tests_failed"] == 1:
                        conflict_recorded.append(row)
                    if kind == "diagnostic" and not member and t1 == FAIL and t2 == FAIL:
                        diagnostic.append(row)
                if defeats:
                    candidates.append({"witness_id": w, "home": home, "axis": axis_of[home],
                                       "defeats": defeats, "crux_strength": len(defeats),
                                       "home_sets": [s["set_id"] for s in cov_all[home]["sets"]
                                                     if w in s["witnesses"]]})
    candidates.sort(key=lambda c: (-c["crux_strength"], c["axis"], c["home"], c["witness_id"]))
    H = {ax["axis_id"]: len(ax["hypotheses"]) for ax in frame["axes"]}
    cost = sum(2 * len(set(home_sets.get(h, []))) * (H[axis_of[h]] - 1) for h in rivals)
    ctx.save("crux", "03_portability-tests/tests.json", tests, "portability-tests")
    ctx.save("crux", "05_candidates/crux-candidates.json",
             {"candidates": candidates, "conflict_recorded": conflict_recorded,
              "diagnostic_witnesses": diagnostic,
              "cost": {"formula": "C = 2 x sum_h W_h x (H_axis - 1)", "tests": cost},
              "definitions": "see claimreg/crux.py module docstring", "time": utcnow()},
             "crux-candidates")
    return {"coverage_recomputed": recomputed,
            "crux_candidates": len(candidates), "conflict_recorded": len(conflict_recorded),
            "diagnostic_witnesses": len(diagnostic), "tests": len(tests),
            "unknown_tests": sum(1 for t in tests if UNKNOWN in (t["t1"], t["t2"]))}
