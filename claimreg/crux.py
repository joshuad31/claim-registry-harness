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
  premise constraint or corroborating expectation) or realizes one of r's recorded
  falsifiers.  Certificate: the conflicting rule bundle (units + match records).
  A BOUNDARY constraint (what r is about: its population, intervention, comparator ...)
  asserts nothing a finding could refute, so it is not part of T1: a study from outside
  r's boundary is out of r's scope, not in conflict with r.  The certificate lists such
  units under ``outside_rival_scope``.
* T2 (coverage) FAILS when, once w is established, r can no longer reach complete
  coverage: (a) w contradicts one of r's REQUIRED_SUPPORT units, so no option for that
  unit can be held alongside w; or (b) after removing every option that contains a
  witness approved-incompatible with w, no jointly valid arrangement remains.  (b) is
  decided by the coverage solver on the whole of B_r (options, incompatibilities and
  constraint vetoes together), not unit by unit: options that each survive may still be
  unable to coexist.  T2 is a counterfactual about what w removes: when r has no valid
  arrangement regardless of w, that is reported in the certificate and is not attributed
  to w.  PASS certificates give a valid arrangement.
* A CONTRADICTS relation may be conditional: it holds only if the finding transfers to
  the unit's scope (matching records this as gap_type SCOPE with the transfer named).  A
  test that fails only through conditional contradictions still fails, and the candidate
  is reported as a crux WITH ASSUMPTIONS, the transfers listed - the same treatment a
  hypothesis gets when it is covered only with assumptions.
* UNKNOWN is returned when a needed relation was never judged (the completion-matching
  step exists to prevent this), when the option list of a required unit was cut at
  ``coverage.max_options_per_unit`` and the cut could change a FAIL, or when the solver
  hit its search limit without finding an arrangement.  It is never converted into PASS
  or FAIL.
* Crux candidate: w is in at least one deletion-minimal set of its home
  hypothesis, appears in none of the rival's formed sets (membership
  screening), and FAILS both T1 and T2 against that rival.

Extended review (spec Optional Route B, clearly separated in the report):
when the home hypothesis has no complete coverage, witnesses that fully cover
at least one of its required units are tested the same way and reported as
"diagnostic witnesses" - never as crux candidates.
"""

from __future__ import annotations

from .coverage import Option, Problem, solve
from .matching import COMPLETE, completion_match, relations_index
from .util import digest, utcnow

PASS, FAIL, UNKNOWN = "PASS", "FAIL", "UNKNOWN"


def compile_theory(hid: str, units: list[dict], cov: dict, incompat: list[dict],
                   constraint_kinds: dict | None = None) -> dict:
    from .units import constraint_kind
    mine = [u for u in units if u["hypothesis_id"] == hid and u.get("active")]
    boundaries = [u["unit_id"] for u in mine if constraint_kind(u, constraint_kinds) == "BOUNDARY"]
    body = {
        "hypothesis_id": hid,
        "required": [u["unit_id"] for u in mine if u["type"] == "REQUIRED_SUPPORT"],
        # premise constraints only: what r assumes about the world.  Boundaries are listed apart.
        "constraints": [u["unit_id"] for u in mine if u["type"] == "CONTEXTUAL_CONSTRAINT"
                        and u["unit_id"] not in boundaries],
        "corroborating": [u["unit_id"] for u in mine if u["type"] == "CORROBORATING_EXPECTATION"],
        "adverse": [u["unit_id"] for u in mine if u["type"] == "ADVERSE_TEST"],
        "options": cov.get("options", {}),
        # units whose option list was cut at coverage.max_options_per_unit ({unit: options before the cut}):
        # B_r does not contain every option for these, so a FAIL that rests on them is UNKNOWN
        "options_truncated": cov.get("options_truncated", {}),
        "constraint_violators": cov.get("constraint_violators", {}),
        "incompatibilities": sorted([sorted([r["a"], r["b"]]) for r in incompat if r.get("approved")]),
        "dependencies": [o["witnesses"] for opts in cov.get("options", {}).values() for o in opts if o.get("joint")],
    }
    if boundaries:      # added only when there are any, so a theory without boundaries keeps its id
        body["boundaries"] = boundaries
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
                             "trace": r.get("trace", ""), **_conditional(r)})
    for u in th["adverse"]:
        f = _rel(rel, w, u)
        checked.append(u)
        if f is None:
            unknown.append(u)
        elif f in COMPLETE:
            r = rel[(w, u)]
            hits.append({"unit_id": u, "unit_group": "adverse_test_realized", "relation": f,
                         "basis": r["basis"], "trace": r.get("trace", "")})
    # a contrary relation to a boundary of r: the witness is about something r is not about
    outside = [u for u in th.get("boundaries", []) if _rel(rel, w, u) == "CONTRADICTS"]
    scope = {"outside_rival_scope": outside} if outside else {}
    if hits:
        return FAIL, {"kind": "T1_cannot_be_accommodated", "conflicting_rule_bundle": hits, **scope,
                      "holds_only_with_assumptions": all(h.get("conditional") for h in hits),
                      "why": "the witness contradicts content the rival asserts or realizes one of its "
                             "recorded falsifiers"}
    if unknown and not missing_is_none:
        return UNKNOWN, {"kind": "T1_unknown", "unjudged_units": unknown, **scope,
                         "why": "relations needed for this test were never judged"}
    return PASS, {"kind": "T1_accommodated", "units_checked": checked, **scope,
                  "unjudged_treated_as_no_relation": unknown,
                  "why": "no CONTRADICTS relation with any asserted unit and no realized falsifier"
                         + ("; some rival units were outside the diagnostic shortlist" if unknown else "")}


def _conditional(r: dict) -> dict:
    """{'conditional': True, 'assumption': ...} for a CONTRADICTS that holds only under a transfer of scope."""
    if r.get("final") == "CONTRADICTS" and r.get("gap_type") == "SCOPE":
        return {"conditional": True, "assumption": r.get("gap") or "the finding transfers to the scope this unit is about"}
    return {}


def _arrangement(th: dict, units: list[str], options: dict, incompat: set, limits: dict) -> dict:
    """Ask the coverage solver whether ``units`` can all be covered from ``options`` at once."""
    pb = Problem(th.get("hypothesis_id", ""), list(units),
                 {u: [Option(o["option_id"], u, tuple(o["witnesses"]), o.get("relation", ""), bool(o.get("joint")))
                      for o in options.get(u, [])] for u in units},
                 {w: list(v) for w, v in (th.get("constraint_violators") or {}).items()},
                 {frozenset(p) for p in (th.get("incompatibilities") or [])} | set(incompat))
    res = solve(pb, int(limits.get("max_states", 3000)), 1)
    if res["sets"]:
        ws = set(res["sets"][0]["witnesses"])
        return {"found": True, "witnesses": sorted(ws),
                "example": {u: next(o["option_id"] for o in options[u] if set(o["witnesses"]) <= ws) for u in units}}
    # no set was found, so RESOURCE_BOUNDED here can only mean the state limit cut the search
    return {"found": False, "bounded": res.get("search_status") == "RESOURCE_BOUNDED",
            "rejected": res.get("rejected_candidates", [])[:5]}


def test_t2(w: str, th: dict, rel: dict, incompat: set, missing_is_none: bool = False,
            limits: dict | None = None) -> tuple[str, dict]:
    limits = limits or {}
    forbidden, blocked, rival_gaps, unknown = [], [], [], []
    truncated = th.get("options_truncated") or {}
    surviving: dict = {}
    for u in th["required"]:
        f = _rel(rel, w, u)
        if f is None:
            unknown.append(u)
        if f == "CONTRADICTS":
            r = rel[(w, u)]
            forbidden.append({"unit_id": u, "trace": r.get("trace", ""), "basis": r["basis"], **_conditional(r)})
            continue
        opts = th["options"].get(u, [])
        if not opts:
            rival_gaps.append(u)
            continue
        surviving[u] = [o for o in opts if not any(frozenset((w, x)) in incompat for x in o["witnesses"])]
        if not surviving[u]:
            blocked.append({"unit_id": u, "options_removed": [o["option_id"] for o in opts],
                            "why": "every option contains a witness approved-incompatible with this witness"})
    base = {"rival_units_already_without_options": rival_gaps}
    if forbidden:
        # a contradicted required unit cannot be covered alongside w whatever options exist, so
        # neither the option cap nor the search limit bears on this result
        return FAIL, {"kind": "T2_cannot_be_accommodated", "required_units_forbidden": forbidden,
                      "required_units_blocked_by_incompatibility": blocked, **base,
                      "holds_only_with_assumptions": all(x.get("conditional") for x in forbidden) and not blocked,
                      "why": "once the witness is established the rival cannot cover these required units"}
    covered = [u for u in th["required"] if u not in rival_gaps]
    cut = sorted(u for u in covered if u in truncated)
    joint = None
    if not blocked and covered:
        removed_any = any(len(surviving[u]) < len(th["options"][u]) for u in covered)
        joint = _arrangement(th, covered, surviving, incompat, limits)
        if not joint["found"] and not joint.get("bounded"):
            # is the loss w's doing?  the rival may have had no valid arrangement to begin with
            before = _arrangement(th, covered, {u: th["options"][u] for u in covered}, set(), limits) \
                if removed_any else joint
            if not before["found"]:
                return PASS, {"kind": "T2_accommodated", "example_arrangement": None, **base,
                              "rival_has_no_valid_arrangement_regardless": True,
                              "why": "the rival's options cannot be combined into a valid arrangement with or "
                                     "without this witness; the witness removes nothing the rival had"}
    if blocked or (joint is not None and not joint["found"] and not joint.get("bounded")):
        cert = {"kind": "T2_cannot_be_accommodated", "required_units_forbidden": [],
                "required_units_blocked_by_incompatibility": blocked, **base,
                "no_joint_arrangement": bool(joint is not None and not joint["found"]),
                "rejected_arrangements": (joint or {}).get("rejected", []),
                "why": "once the witness is established the rival cannot cover its required units together"}
        if cut:
            return UNKNOWN, {**cert, "kind": "T2_unknown", "options_cut_at_cap": {u: truncated[u] for u in cut},
                             "why": "the rival's surviving options cannot cover it, but the option list of "
                                    f"{', '.join(cut)} was cut at coverage.max_options_per_unit and an option "
                                    "outside the cut might; raise the cap and rerun from coverage"}
        return FAIL, cert
    if joint is not None and joint.get("bounded"):
        return UNKNOWN, {"kind": "T2_unknown", **base, "search_limit": int(limits.get("max_states", 3000)),
                         "why": "the search limit (coverage.max_states) was reached before a valid arrangement "
                                "was found or ruled out"}
    if unknown and not missing_is_none:
        return UNKNOWN, {"kind": "T2_unknown", "unjudged_required_units": unknown, **base,
                         "why": "whether the witness contradicts these required units was never decided"}
    example = {u: None for u in th["required"]}
    example.update((joint or {}).get("example", {}))
    return PASS, {"kind": "T2_accommodated", "example_arrangement": example,
                  "arrangement_witnesses": (joint or {}).get("witnesses", []), **base,
                  "why": "a valid arrangement of the rival's options exists alongside the witness"
                         + ("; the rival is already incomplete on the listed units, independent of this witness"
                            if rival_gaps else "")}


def _assumptions(c1: dict, c2: dict) -> list[dict]:
    """The transfers a crux result rests on, when it would not hold without them."""
    out, seen = [], set()
    if c1.get("holds_only_with_assumptions") or c2.get("holds_only_with_assumptions"):
        for h in c1.get("conflicting_rule_bundle", []) + c2.get("required_units_forbidden", []):
            if h.get("conditional") and h["unit_id"] not in seen:
                seen.add(h["unit_id"])
                out.append({"unit_id": h["unit_id"], "assumption": h["assumption"]})
    return out


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

    kinds = dict(ctx.cfg["coverage"].get("constraint_kinds") or {})
    theories = {h: compile_theory(h, units, cov_all.get(h, {}), inc_recs, kinds) for h in rivals}
    ctx.save("crux", "01_frozen-rival-theories/theories.json", theories, "frozen-rival-theories")

    limits = {"max_states": int(ctx.cfg["coverage"].get("max_states", 3000))}
    rival_members = {h: set(home_sets.get(h, [])) for h in rivals}
    tests, candidates, conflict_recorded, diagnostic = [], [], [], []
    for home in rivals:
        for kind, wlist in (("crux", sorted(set(home_sets.get(home, [])))),
                            ("diagnostic", partial_home.get(home, []))):
            for w in wlist:
                defeats, needs = [], {}
                for r in rivals[home]:
                    th = theories[r]
                    t1, c1 = test_t1(w, th, rel, missing_is_none=(kind == "diagnostic"))
                    t2, c2 = test_t2(w, th, rel, incompat, missing_is_none=(kind == "diagnostic"), limits=limits)
                    member = w in rival_members.get(r, set())
                    is_crux = (kind == "crux") and (not member) and t1 == FAIL and t2 == FAIL
                    row = {"witness_id": w, "home": home, "rival": r, "axis": axis_of[home], "kind": kind,
                           "membership_screen_passes": not member, "t1": t1, "t2": t2,
                           "t1_certificate": c1, "t2_certificate": c2, "crux": is_crux,
                           "tests_failed": int(t1 == FAIL) + int(t2 == FAIL), "theory_id": th["theory_id"]}
                    if t1 == FAIL and t2 == FAIL:
                        row["assumptions"] = _assumptions(c1, c2)
                    tests.append(row)
                    if is_crux:
                        defeats.append(r)
                        if row["assumptions"]:
                            needs[r] = row["assumptions"]
                    elif kind == "crux" and not member and row["tests_failed"] == 1:
                        conflict_recorded.append(row)
                    if kind == "diagnostic" and not member and t1 == FAIL and t2 == FAIL:
                        diagnostic.append(row)
                if defeats:
                    candidates.append({"witness_id": w, "home": home, "axis": axis_of[home],
                                       "defeats": defeats, "crux_strength": len(defeats),
                                       # rivals it defeats only if a finding transfers to the rival
                                       # unit's scope, with the transfers; empty = no assumption needed
                                       "defeats_only_with_assumptions": sorted(needs),
                                       "assumptions": needs,
                                       "home_coverage": cov_all[home].get("status"),
                                       "home_sets": [s["set_id"] for s in cov_all[home]["sets"]
                                                     if w in s["witnesses"]]})
    candidates.sort(key=lambda c: (len(c["defeats_only_with_assumptions"]) == len(c["defeats"]),
                                   -c["crux_strength"], c["axis"], c["home"], c["witness_id"]))
    by_study: dict = {}
    try:
        from . import studies
        of = studies.witness_studies(ctx)
        for c in candidates:
            a = of.get(c["witness_id"])
            if a:
                c["study"], c["study_role"] = a["study"], a["role"]
                if a["role"] != "direct":
                    c["study_via"] = a["via"]
        cc = studies.count(of.get(c["witness_id"]) for c in candidates)
        by_study = {"candidates": cc["items"], "studies": cc["studies"], "secondary_reports": cc["secondary_reports"],
                    "note": "candidates sharing a study are one study told more than once; none is merged"}
    except Exception as e:  # noqa: BLE001
        ctx.log(f"   crux: study identity not recorded ({type(e).__name__}: {e})")
    H = {ax["axis_id"]: len(ax["hypotheses"]) for ax in frame["axes"]}
    cost = sum(2 * len(set(home_sets.get(h, []))) * (H[axis_of[h]] - 1) for h in rivals)
    ctx.save("crux", "03_portability-tests/tests.json", tests, "portability-tests")
    ctx.save("crux", "05_candidates/crux-candidates.json",
             {"candidates": candidates, "candidates_by_study": by_study, "conflict_recorded": conflict_recorded,
              "diagnostic_witnesses": diagnostic,
              "cost": {"formula": "C = 2 x sum_h W_h x (H_axis - 1)", "tests": cost},
              "definitions": "see claimreg/crux.py module docstring", "time": utcnow()},
             "crux-candidates")
    return {"coverage_recomputed": recomputed,
            "crux_candidates": len(candidates),
            "crux_candidate_studies": len(by_study.get("studies", [])),
            "crux_candidates_with_assumptions": sum(1 for c in candidates
                                                    if len(c["defeats_only_with_assumptions"]) == len(c["defeats"])), "conflict_recorded": len(conflict_recorded),
            "diagnostic_witnesses": len(diagnostic), "tests": len(tests),
            "unknown_tests": sum(1 for t in tests if UNKNOWN in (t["t1"], t["t2"]))}
