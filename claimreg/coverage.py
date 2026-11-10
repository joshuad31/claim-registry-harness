"""Deletion-minimal hypothesis coverage sets (spec 29; technical specification 4).

Options per REQUIRED_SUPPORT unit come only from the approved matching record:
a single witness with EQUIVALENT / WITNESS_ENTAILS_UNIT, or an approved
jointly-sufficient group (one option; its witnesses stay separate).

Enumeration
-----------
Instead of the literal cross product of options, the solver enumerates the
minimal transversals of the option hypergraph (Berge's algorithm with
superset pruning; units ordered from fewest to most options, as the spec
directs).  Every deletion-minimal set S is the witness-union of some minimal
transversal: the options contained in S form a transversal, it contains a
minimal one T, and union(T) is a covering subset of S; if it were a proper
subset, some witness of S could be deleted, contradicting minimality.  This
holds because the validity conditions used here are monotone (a subset of a
valid set never violates a constraint or completes an incompatibility).  So
the same sets are found with far less search.  Every candidate still goes
through the literal deletion pass, to a fixed point, with a removal
certificate per surviving witness.  Brute-force agreement is tested in
tests/test_coverage.py.

Validity
--------
* contextual constraints: a set is invalid if a member has an approved
  CONTRADICTS relation to one of the hypothesis's CONTEXTUAL_CONSTRAINT units
  (``coverage.constraint_veto``);
* approved incompatibilities: a set containing both members of an approved
  incompatible pair is invalid;
* necessary dependencies: only those of jointly-sufficient groups (all
  members needed) - the spec leaves other dependency approval open.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

from .matching import COMPLETE
from .util import make_id, utcnow

# Second tier (coverage.assume_gaps): when a required unit has no complete option, a witness that
# reports the unit's own effect in another population, species, model or dose (PARTIALLY_COVERS with
# gap_type SCOPE, agreed by both matching passes or adjudicated) may cover it CONDITIONALLY.  The
# transfer it relies on is written into the set as a named assumption, and the hypothesis is reported
# as COMPLETE_WITH_ASSUMPTIONS, never as COMPLETE.  Mechanistic and animal evidence can then carry a
# hypothesis, with exactly what has to be granted listed beside it.


@dataclass
class Option:
    option_id: str
    unit_id: str
    witnesses: tuple
    relation: str
    joint: bool = False
    assumption: str = ""       # non-empty: a conditional option; this is what has to be granted


@dataclass
class Problem:
    hypothesis_id: str
    required: list[str]
    options: dict[str, list[Option]]
    constraint_violators: dict[str, list[str]] = field(default_factory=dict)   # witness -> constraint ids
    incompatible: set = field(default_factory=set)                             # frozenset({a,b})


def build_problem(hid: str, units: list[dict], rel: dict, groups: list[dict], incompat: list[dict],
                  veto: bool = True, max_options: int = 12, assume_gaps: tuple = ()) -> tuple[Problem, dict]:
    req = [u["unit_id"] for u in units if u["hypothesis_id"] == hid and u.get("active")
           and u["type"] == "REQUIRED_SUPPORT"]
    cons = [u["unit_id"] for u in units if u["hypothesis_id"] == hid and u.get("active")
            and u["type"] == "CONTEXTUAL_CONSTRAINT"]
    opts: dict[str, list[Option]] = {}
    truncated = {}
    for uid in req:
        lst = []
        for (w, x), r in sorted(rel.items()):
            if x == uid and r["final"] in COMPLETE:
                lst.append(Option(make_id("OPT", {"u": uid, "w": [w]}), uid, (w,), r["final"]))
        for g in groups:
            if g.get("approved") and g["unit_id"] == uid:
                ws = tuple(sorted(g["witnesses"]))
                lst.append(Option(make_id("OPT", {"u": uid, "w": list(ws)}), uid, ws, "JOINTLY_SUFFICIENT", True))
        if not lst and assume_gaps:
            brank = {"HUMAN": 0, "AGREED": 1, "MODEL_ADJUDICATED": 2}
            cond = [(brank.get(r.get("basis"), 3), w, r) for (w, x), r in rel.items()
                    if x == uid and r["final"] == "PARTIALLY_COVERS" and r.get("gap_type") in assume_gaps]
            for _, w, r in sorted(cond, key=lambda t: (t[0], t[1])):
                lst.append(Option(make_id("OPT", {"u": uid, "w": [w], "c": 1}), uid, (w,), "PARTIALLY_COVERS",
                                  assumption=(r.get("gap") or r.get("trace") or "the finding transfers to the "
                                              "scope this unit requires").strip()))
        if len(lst) > max_options:
            rank = {"EQUIVALENT": 0, "WITNESS_ENTAILS_UNIT": 1, "JOINTLY_SUFFICIENT": 2}
            lst = sorted(lst, key=lambda o: (rank.get(o.relation, 3), len(o.witnesses), o.witnesses))
            truncated[uid] = len(lst)
            lst = lst[:max_options]
        opts[uid] = lst
    violators: dict[str, list[str]] = {}
    if veto:
        for (w, x), r in rel.items():
            if x in cons and r["final"] == "CONTRADICTS":
                violators.setdefault(w, []).append(x)
    inc = {frozenset((r["a"], r["b"])) for r in incompat if r.get("approved")}
    return Problem(hid, req, opts, violators, inc), {"options_truncated": truncated,
                                                     "constraints": cons}


def _valid(ws: set, pb: Problem) -> tuple[bool, str]:
    bad = sorted(w for w in ws if w in pb.constraint_violators)
    if bad:
        return False, f"constraint violated by {bad[0]} ({', '.join(pb.constraint_violators[bad[0]])})"
    for a, b in itertools.combinations(sorted(ws), 2):
        if frozenset((a, b)) in pb.incompatible:
            return False, f"approved incompatibility {a} x {b}"
    return True, ""


def covers(pb: Problem, ws: set, uid: str) -> bool:
    return any(set(o.witnesses) <= ws for o in pb.options.get(uid, []))


def complete(pb: Problem, ws: set) -> bool:
    return all(covers(pb, ws, u) for u in pb.required) and _valid(ws, pb)[0]


def prune(sets: set) -> list:
    ordered = sorted(sets, key=lambda s: (len(s), sorted(s)))
    kept: list = []
    for s in ordered:
        if not any(k <= s for k in kept):
            kept.append(s)
    return kept


def minimal_transversals(edges: list[frozenset], max_states: int) -> tuple[list[frozenset], bool]:
    edges = sorted([e for e in edges if e], key=lambda e: (len(e), sorted(e)))
    cur: set = {frozenset()}
    exhaustive = True
    for e in edges:
        nxt = set()
        for t in cur:
            if t & e:
                nxt.add(t)
            else:
                for o in e:
                    nxt.add(t | {o})
        cur = set(prune(nxt))
        if len(cur) > max_states:
            exhaustive = False
            cur = set(sorted(cur, key=lambda s: (len(s), sorted(s)))[:max_states])
    return sorted(cur, key=lambda s: (len(s), sorted(s))), exhaustive


def deletion_pass(pb: Problem, ws: set) -> tuple[set, list[dict]]:
    sel = set(ws)
    changed = True
    while changed:
        changed = False
        for w in sorted(sel):
            trial = sel - {w}
            if complete(pb, trial):
                sel = trial
                changed = True
    certs = []
    for w in sorted(sel):
        trial = sel - {w}
        broken = [u for u in pb.required if not covers(pb, trial, u)]
        groups_broken = [o.option_id for u in pb.required for o in pb.options[u]
                         if o.joint and w in o.witnesses and set(o.witnesses) <= sel]
        alternatives = {u: [o.option_id for o in pb.options[u] if set(o.witnesses) <= trial]
                        for u in pb.required}
        certs.append({"witness_id": w,
                      "removal_breaks": "required unit(s) uncovered" if broken else
                      "jointly-sufficient group / dependency",
                      "uncovered_units": broken, "joint_groups_broken": groups_broken,
                      "options_that_cover_each_unit_without_it": {u: alternatives[u] for u in broken}})
    return sel, certs


def solve(pb: Problem, max_states: int = 3000, max_sets: int = 200) -> dict:
    uncovered = [u for u in pb.required if not pb.options.get(u)]
    if not pb.required:
        return {"status": "NO_REQUIRED_UNITS", "sets": [], "uncovered_units": [],
                "search_status": "NOT_RUN", "note": "the hypothesis has no active REQUIRED_SUPPORT unit"}
    if uncovered:
        return {"status": "NO_COMPLETE_COVERAGE", "sets": [], "uncovered_units": uncovered,
                "search_status": "NOT_RUN",
                "note": "At least one required unit has no coverage option; no complete set can be built."}
    opt_list = []
    for u in pb.required:
        for o in pb.options[u]:
            if o.option_id not in {x.option_id for x in opt_list}:
                opt_list.append(o)
    pos = {o.option_id: i for i, o in enumerate(opt_list)}
    edges = [frozenset(pos[o.option_id] for o in pb.options[u]) for u in pb.required]
    trans, exhaustive = minimal_transversals(edges, max_states)
    seen, sets, rejected = set(), [], []
    for t in trans:
        ws = set().union(*(set(opt_list[i].witnesses) for i in t)) if t else set()
        ok, why = _valid(ws, pb)
        if not ok:
            rejected.append({"witnesses": sorted(ws), "reason": why})
            continue
        sel, certs = deletion_pass(pb, ws)
        key = frozenset(sel)
        if key in seen or not complete(pb, sel):
            continue
        seen.add(key)
        used = sorted(o.option_id for o in opt_list if set(o.witnesses) <= sel)
        sets.append({"set_id": make_id("SET", {"h": pb.hypothesis_id, "w": sorted(sel)}),
                     "witnesses": sorted(sel), "option_ids": used, "certificates": certs})
        if len(sets) >= max_sets:
            exhaustive = False
            break
    status = "COMPLETE" if sets else "NO_COMPLETE_COVERAGE"
    return {"status": status, "sets": sets, "uncovered_units": [],
            "search_status": "EXHAUSTIVE" if exhaustive else "RESOURCE_BOUNDED",
            "transversals": len(trans), "rejected_candidates": rejected[:50],
            "note": ("" if sets else "Every candidate combination violated a constraint or an incompatibility.")}


def _set_assumptions(pb: Problem, ws: set) -> list[dict]:
    """The transfers a set relies on: one entry per required unit that only a conditional option covers."""
    out = []
    for u in pb.required:
        inside = [o for o in pb.options.get(u, []) if set(o.witnesses) <= ws]
        if inside and all(o.assumption for o in inside):
            o = inside[0]
            out.append({"unit_id": u, "witness_id": o.witnesses[0], "assumption": o.assumption})
    return out


def coverage_stage(ctx) -> dict:
    ccfg = ctx.cfg["coverage"]
    from .matching import relations_index
    rel = relations_index(ctx)
    units = ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or []
    groups = ctx.load("matching", "03_match-records/joint-groups.json", default=[]) or []
    from .joint import incompatibility_records
    inc = incompatibility_records(ctx)
    assume = tuple(g for g in (ccfg.get("assume_gaps") or []) if g)
    veto = bool(ccfg.get("constraint_veto", True))
    max_opt = int(ccfg.get("max_options_per_unit", 12))
    out = {}
    for ax in ctx.frame["axes"]:
        for h in ax["hypotheses"]:
            pb, info = build_problem(h["id"], units, rel, groups, inc, veto=veto, max_options=max_opt)
            res = solve(pb, int(ccfg.get("max_states", 3000)), int(ccfg.get("max_sets", 200)))
            strict_covered = sum(1 for u in pb.required if pb.options.get(u))
            if res["status"] == "NO_COMPLETE_COVERAGE" and assume:
                pb2, info2 = build_problem(h["id"], units, rel, groups, inc, veto=veto, max_options=max_opt,
                                           assume_gaps=assume)
                if any(o.assumption for opts in pb2.options.values() for o in opts):
                    res2 = solve(pb2, int(ccfg.get("max_states", 3000)), int(ccfg.get("max_sets", 200)))
                    pb, info = pb2, info2       # the conditional options are shown either way
                    if res2["sets"]:
                        res = res2
                        res["status"] = "COMPLETE_WITH_ASSUMPTIONS"
                        for s in res["sets"]:
                            s["assumptions"] = _set_assumptions(pb, set(s["witnesses"]))
                        res["note"] = ("No set of complete matches covers every required unit. The sets listed "
                                       "cover the remaining units with findings from another population, species, "
                                       "model or dose; each set names the transfer it assumes.")
                    else:
                        res["uncovered_units"] = [u for u in pb.required if not pb.options.get(u)]
            if info["options_truncated"] and res.get("search_status") == "EXHAUSTIVE":
                res["search_status"] = "RESOURCE_BOUNDED"
            evaluative = [u["unit_id"] for u in units if u["hypothesis_id"] == h["id"]
                          and u["type"] == "EVALUATIVE_JUDGMENT"]
            if res["status"] == "NO_REQUIRED_UNITS" and evaluative:
                res["residual"] = True
                res["note"] = ("This hypothesis makes no finding-sized requirement of its own: it is a judgment "
                               "about the state of the evidence. It holds to the extent that its rivals' required "
                               "parts remain uncovered or contested; see the premise ledger.")
            res.update({
                "hypothesis_id": h["id"], "axis_id": ax["axis_id"], "required_units": pb.required,
                "constraints": info["constraints"], "options_truncated": info["options_truncated"],
                "options": {u: [{"option_id": o.option_id, "witnesses": list(o.witnesses),
                                 "relation": o.relation, "joint": o.joint,
                                 **({"assumption": o.assumption} if o.assumption else {})}
                                for o in pb.options[u]]
                            for u in pb.required},
                "constraint_violators": pb.constraint_violators,
                "units_covered": sum(1 for u in pb.required if pb.options.get(u)),
                "units_covered_strict": strict_covered,
                "evaluative_units": evaluative,
            })
            out[h["id"]] = res
    ctx.save("coverage", "coverage.json", {"hypotheses": out, "time": utcnow()}, "coverage-sets")
    from .ledger import write_ledger
    led = write_ledger(ctx, out)
    return {**{h: {"status": r["status"], "sets": len(r["sets"]), "search": r["search_status"],
                   "covered_units": f"{r['units_covered']}/{len(r['required_units'])}"} for h, r in out.items()},
            "ledger": led}
