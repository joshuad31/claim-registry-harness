"""Preliminary, evidence-level assessment: ACH_Eval (verbatim) on the validated FRDs.

This is the researcher's first look at what the quest found.  It runs right after FRD
retention and BEFORE the dictionary, canonicalizer, transcoding, witnesses and matching, and the
run then halts until the researcher releases it (docs/FRD-EVALUATION.md).

For every axis it produces two allocation vectors over that axis's hypotheses:

  axis-only   ACH_Eval over the validated FRDs filed under that axis
  combined    ACH_Eval over the validated FRDs of every axis (a disjoint union: the combined
              count equals the sum of the axis counts, and every row keeps its home axis)

and reports them side by side.  No blended score is chosen here: an equal-weight row is printed
for comparison only.

Partition rule (fixed, recorded, tested).  The FRDs are sorted by id and packed, in that order,
into partitions of at most `frd_assess.partition_words` registry words.  One partition: its
vector is the result.  Several partitions: each is assessed alone, then one further ACH_Eval call
receives only the partition fragments (no evidence a partition did not see) and returns the
result.  Beside it the harness records the mechanical mean of the partition vectors, weighted by
FRD count and rounded to the gauge by largest remainder, and the largest difference between the
two; a difference above an eighth of the gauge is reported as a warning, because it means the
conclusion depends on where the partitions were cut.

This is not the final assessment.  The witness-level `assess` stage remains the later one.
"""

from __future__ import annotations

import re
import sqlite3
import time
from collections import Counter
from pathlib import Path

from .assess import _axis_context
from .llm.base import LLMRequest
from .llm.jsonparse import JSONExtractError, extract_json
from .runctx import SHARED_FOLDER
from .util import atomic_write_text, read_json, utcnow, write_json

REL_RETAINED = ("frds", "05_validated/retained-frds.json")
EVAL_DIR = "06_evaluation"
COMBINED_DIR = "03_FRDS-COMBINED"
CAVEAT = ("Preliminary, evidence-level reading of the validated FRDs. Uncalibrated working judgment, "
          "not a probability, and not the final (witness-level) assessment.")
WARN_FRACTION = 8          # warn when partition handling moves a hypothesis by more than gauge / 8


# --------------------------------------------------------------------------- #
# deterministic arithmetic
# --------------------------------------------------------------------------- #

def frd_id(f: dict) -> str:
    return str(f.get("vfrd_id") or f.get("frd_id"))


def registry_line(f: dict, combined: bool) -> str:
    claim = " ".join(str(f.get("claim", "")).split())
    cols = [frd_id(f)] + ([str(f.get("home_axis", "-"))] if combined else []) + \
           [str(f.get("source_file", "-")), str(f.get("verdict", "-")), claim]
    return " | ".join(cols)


def partition(frds: list[dict], max_words: int, combined: bool = False) -> list[list[dict]]:
    """Sorted by id, packed in order; a partition closes when the next FRD would pass the limit."""
    parts: list[list[dict]] = []
    cur: list[dict] = []
    words = 0
    for f in sorted(frds, key=frd_id):
        n = len(registry_line(f, combined).split())
        if cur and words + n > max_words:
            parts.append(cur)
            cur, words = [], 0
        cur.append(f)
        words += n
    if cur:
        parts.append(cur)
    return parts


def largest_remainder(weights: dict[str, float], gauge: int) -> dict[str, int]:
    """Nonnegative integers summing to the gauge, proportional to the weights; ties go to the
    hypothesis listed first."""
    ids = list(weights)
    total = sum(max(0.0, float(weights[i])) for i in ids)
    if not ids:
        return {}
    if total <= 0:
        shares = {i: gauge / len(ids) for i in ids}
    else:
        shares = {i: gauge * max(0.0, float(weights[i])) / total for i in ids}
    out = {i: int(shares[i]) for i in ids}
    order = sorted(ids, key=lambda i: (-(shares[i] - out[i]), ids.index(i)))
    for i in order[:gauge - sum(out.values())]:
        out[i] += 1
    return out


def mechanical_mean(vectors: list[dict], counts: list[int], ids: list[str], gauge: int) -> dict[str, int]:
    """The partition vectors averaged with FRD counts as weights, rounded by largest remainder."""
    return largest_remainder({i: sum(c * float(v.get(i, 0)) for v, c in zip(vectors, counts)) for i in ids}, gauge)


def max_diff(a: dict | None, b: dict | None) -> int | None:
    if not a or not b:
        return None
    return max(abs(int(a.get(i, 0)) - int(b.get(i, 0))) for i in set(a) | set(b))


def combined_rows(per_axis: dict[str, list[dict]]) -> list[dict]:
    """The disjoint union of the axes' validated FRDs, each row labelled with its home axis."""
    rows = [dict(f, home_axis=a) for a, fs in per_axis.items() for f in fs]
    ids = [frd_id(r) for r in rows]
    dup = sorted(i for i, n in Counter(ids).items() if n > 1)
    if dup or len(rows) != sum(len(fs) for fs in per_axis.values()):
        raise ValueError(f"the combined FRD set is not a disjoint union of the axis sets; filed twice: {dup[:5]}")
    return sorted(rows, key=frd_id)


# --------------------------------------------------------------------------- #
# model calls
# --------------------------------------------------------------------------- #

def _parse(res, ids: list[str], gauge: int, axis_id: str, label: str) -> tuple[dict, list[str]]:
    if res is None:
        return {}, [f"{label}: no response"]
    if str(getattr(res, "parse_error", "") or "").startswith("provider error"):
        return {}, [f"{label}: {res.parse_error}"]
    data: dict = {}
    for block in reversed(re.findall(r"```json\s*\n(.*?)\n?```", res.text or "", re.S)):
        try:
            cand = extract_json(block)
        except JSONExtractError:
            continue
        if isinstance(cand, dict) and "allocations" in cand:
            data = cand
            break
    if not data:
        return {}, [f"{label}: no allocation JSON block"]
    vec = data.get("allocations") or {}
    if isinstance(vec.get(axis_id), dict):          # a model that nested the vector under the axis id
        vec = vec[axis_id]
    try:
        vec = {i: int(vec.get(i, 0)) for i in ids}
    except (TypeError, ValueError):
        return {}, [f"{label}: non-integer units"]
    problems = [] if sum(vec.values()) == gauge else [f"{label}: units sum to {sum(vec.values())}, not {gauge}"]
    for k in ("basis_confidence", "strongest_objection", "reversal_finding"):
        if isinstance(data.get(k), dict):
            data[k] = data[k].get(axis_id, "")
    drivers = data.get("drivers") or []
    if isinstance(drivers, dict):
        drivers = drivers.get(axis_id) or [d for v in drivers.values() if isinstance(v, list) for d in v]
    norm = []
    for d in drivers if isinstance(drivers, list) else []:
        if isinstance(d, dict) and d.get("frd_id"):
            norm.append({"frd_id": str(d["frd_id"]).strip(), "favors": str(d.get("favors", "")), "why": str(d.get("why", ""))})
        elif isinstance(d, str) and d.strip():
            head, _, why = d.partition(":")
            norm.append({"frd_id": head.strip(), "favors": "", "why": why.strip()})
    return {**data, "allocations": vec, "drivers": norm}, problems


class _Job:
    """One assessment of one axis's hypotheses over one FRD set."""

    def __init__(self, ctx, axis: dict, frds: list[dict], scope: str, out_dir: Path, gauge: int, words: int):
        self.ctx, self.axis, self.frds, self.scope, self.out, self.gauge = ctx, axis, frds, scope, out_dir, gauge
        self.combined = scope == "combined"
        self.aid = axis["axis_id"]
        self.ids = [h["id"] for h in axis.get("hypotheses", [])]
        self.parts = partition(frds, words, self.combined)
        self.part_results: list[dict] = []
        self.problems: list[str] = []
        self.calls: list[dict] = []
        self.final: dict = {}

    def _request(self, registry: str, fragments: str, tag: str, meta: dict) -> LLMRequest:
        note = ("SCOPE OF THIS PASS: the registry holds the validated FRDs of EVERY axis of this investigation, "
                "each labelled with its home axis; assess only the axis named below, and use an FRD from "
                "another axis only where it really bears on this axis's hypotheses."
                if self.combined else
                "SCOPE OF THIS PASS: the registry holds only the validated FRDs filed under the axis named below.")
        system, user, _ = self.ctx.prompts.render(
            "frd_assess.md", GAUGE=self.gauge, GOAL=self.axis.get("question", ""), SCOPE_NOTE=note,
            INVESTIGATION_ID=f"{self.ctx.run_id}:{self.aid}:frd-{self.scope}:{tag}",
            FRAGMENTS=fragments, HYPOTHESES=_axis_context(self.axis),
            REGISTRY_COLUMNS="frd id | home axis | source | validation verdict | claim" if self.combined
            else "frd id | source | validation verdict | claim",
            REGISTRY=registry)
        return LLMRequest(role="frd_assessor", system=system, user=user, expect_json=False,
                          tag=f"frd-assess-{self.aid}-{self.scope}-{tag}", max_output_tokens=24000,
                          meta={"axis": self.axis, "gauge": self.gauge, "hypothesis_ids": self.ids, **meta})

    def partition_requests(self) -> list[LLMRequest]:
        n = len(self.parts)
        return [self._request(
            "\n".join(registry_line(f, self.combined) for f in part),
            "none" if n == 1 else f"none; this is partition {k} of {n} of the registry, assessed alone",
            f"p{k:02d}", {"frd_ids": [frd_id(f) for f in part]}) for k, part in enumerate(self.parts, 1)]

    def take_partitions(self, responses: list) -> None:
        self.out.mkdir(parents=True, exist_ok=True)
        for k, (part, res) in enumerate(zip(self.parts, responses), 1):
            data, probs = _parse(res, self.ids, self.gauge, self.aid, f"{self.aid} {self.scope} partition {k}")
            self.problems += probs
            if res is not None:
                atomic_write_text(self.out / f"partition-{k:02d}.md", res.text or "")
                self.calls.append({"partition": k, "call_key": res.key, "model": res.model})
            self.part_results.append({**data, "partition": k, "frd_count": len(part),
                                      "first_frd": frd_id(part[0]), "last_frd": frd_id(part[-1])})

    def synthesis_request(self) -> LLMRequest | None:
        good = [p for p in self.part_results if p.get("allocations")]
        if len(self.parts) < 2 or len(good) != len(self.parts):
            return None
        frag = [f"{len(good)} partition fragments follow. Together the partitions held all {len(self.frds)} "
                f"validated FRDs. Produce the single assessment of this axis from these fragments alone."]
        for p, part in zip(good, self.parts):
            text = read_text(self.out / f"partition-{p['partition']:02d}.md")
            body = " ".join(re.sub(r"```json.*?```", "", text, flags=re.S).split()[:1200])
            frag.append(f"--- PARTITION {p['partition']} ({p['frd_count']} FRDs, {p['first_frd']} to {p['last_frd']}) ---\n"
                        f"allocation: {p['allocations']}\n"
                        f"drivers: {[(d['frd_id'], d['favors'], d['why'][:160]) for d in p.get('drivers', [])]}\n"
                        f"strongest objection: {p.get('strongest_objection', '')}\n"
                        f"reversal finding: {p.get('reversal_finding', '')}\n"
                        f"commentary (start): {body}")
        return self._request("(none in this pass: the evidence was assessed in the partitions above; cite drivers by "
                             "the FRD ids the fragments name)", "\n\n".join(frag), "synthesis",
                             {"frd_ids": [frd_id(f) for f in self.frds],
                              "partition_vectors": [p["allocations"] for p in good],
                              "partition_counts": [p["frd_count"] for p in good]})

    def finish(self, synthesis) -> dict:
        good = [p for p in self.part_results if p.get("allocations")]
        mech = mechanical_mean([p["allocations"] for p in good], [p["frd_count"] for p in good], self.ids,
                               self.gauge) if good and len(good) == len(self.parts) else None
        rule = "no validated FRDs: nothing to assess"
        if len(self.parts) == 1:
            self.final, rule = (good[0] if good else {}), "one partition: its vector is the result"
            if good:
                atomic_write_text(self.out / "evaluation.md", read_text(self.out / "partition-01.md"))
        elif len(self.parts) > 1:
            rule = "one ACH_Eval call over the partition fragments"
            if synthesis is not None:
                data, probs = _parse(synthesis, self.ids, self.gauge, self.aid, f"{self.aid} {self.scope} synthesis")
                self.problems += probs
                atomic_write_text(self.out / "evaluation.md", synthesis.text or "")
                self.calls.append({"partition": "synthesis", "call_key": synthesis.key, "model": synthesis.model})
                self.final = data
                if data and not data.get("drivers"):
                    data["drivers"] = [d for p in good for d in p.get("drivers", [])]
        by_id = {frd_id(f): f for f in self.frds}
        drivers, unknown = [], []
        for d in self.final.get("drivers", []) or []:
            f = by_id.get(d["frd_id"])
            if f is None:
                unknown.append(d["frd_id"])
                continue
            drivers.append({**d, "source_file": f.get("source_file"), "qid": f.get("qid"),
                            "home_axis": f.get("home_axis", self.aid), "claim": f.get("claim")})
        vec = self.final.get("allocations") or None
        spread = max((max(p["allocations"].get(i, 0) for p in good) - min(p["allocations"].get(i, 0) for p in good)
                      for i in self.ids), default=0) if len(good) > 1 else 0
        diff = max_diff(vec, mech) if len(self.parts) > 1 else 0
        warnings = []
        if diff is not None and diff > self.gauge // WARN_FRACTION:
            warnings.append(f"{self.aid} {self.scope}: the result differs from the mechanical mean of its partitions by "
                            f"{diff} units; the conclusion depends on how the FRDs were partitioned")
        rec = {"axis": self.aid, "scope": self.scope, "label": "PRELIMINARY, evidence-level (validated FRDs)",
               "gauge": self.gauge, "frd_count": len(self.frds), "allocations": vec,
               "partition_rule": rule, "partition_count": len(self.parts),
               "partitions": [{k: p.get(k) for k in ("partition", "frd_count", "first_frd", "last_frd", "allocations")}
                              for p in self.part_results],
               "mechanical_mean_of_partitions": mech if len(self.parts) > 1 else None,
               "partition_spread_units": spread, "result_vs_mechanical_mean_units": diff,
               "basis_confidence": self.final.get("basis_confidence", ""),
               "strongest_objection": self.final.get("strongest_objection", ""),
               "reversal_finding": self.final.get("reversal_finding", ""),
               "drivers": drivers, "driver_ids_not_in_registry": unknown,
               "other_axis_drivers": [d for d in drivers if d["home_axis"] != self.aid] if self.combined else [],
               "problems": self.problems, "warnings": warnings, "calls": self.calls, "time": utcnow(),
               "caveat": CAVEAT}
        if self.frds or self.out.exists():
            write_json(self.out / "evaluation.json", rec)
        return rec


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


# --------------------------------------------------------------------------- #
# one SQLite database per axis, generated from the JSON records (which stay the source of record)
# --------------------------------------------------------------------------- #

DB_TABLES = {
    "questions": (("discovery", "01_issued-questions/questions.json"),
                  ("qid", "axis", "axis_source", "round", "target", "status", "text")),
    "responses": (("discovery", "02_query-responses/responses.json"),
                  ("response_id", "qid", "attempt", "status", "text")),
    "candidate_frds": (("frds", "01_candidates/candidates.json"),
                       ("frd_id", "qid", "source_file", "claim")),
    "validations": (("frds", "04_validation-results/validations.json"),
                    ("validation_id", "frd_id", "qid", "source_file", "verdict", "readiness")),
    "validated_frds": (("frds", "05_validated/validated-frds.json"),
                       ("vfrd_id", "frd_id", "qid", "source_file", "citation", "verdict", "readiness", "claim")),
    "retained_frds": (REL_RETAINED,
                      ("vfrd_id", "frd_id", "qid", "source_file", "citation", "verdict", "readiness", "claim")),
}


def _rows(sc, rel) -> list[dict]:
    data = sc.load(*rel, default=[]) or []
    if isinstance(data, dict):
        data = next((v for v in data.values() if isinstance(v, list)), [])
    return [r for r in data if isinstance(r, dict)]


def write_axis_db(sc) -> dict:
    """AXIS-<id>/axis.db: one table per record kind, key columns plus the full record as JSON."""
    import json
    path = Path(sc.root) / "axis.db"
    tmp = path.with_suffix(".db.tmp")
    if tmp.exists():
        tmp.unlink()
    con = sqlite3.connect(tmp)
    counts = {}
    try:
        con.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)")
        con.executemany("INSERT INTO meta VALUES (?, ?)", [
            ("axis", sc.axis_id), ("run", sc.run_id), ("generated", utcnow()),
            ("note", "Generated from this axis folder's JSON files, which remain the source of record.")])
        for table, (rel, cols) in DB_TABLES.items():
            rows = _rows(sc, rel)
            con.execute(f"CREATE TABLE {table} ({', '.join(c + ' TEXT' for c in cols)}, record_json TEXT)")
            con.executemany(
                f"INSERT INTO {table} VALUES ({', '.join('?' for _ in cols)}, ?)",
                [tuple(None if r.get(c) is None else (r[c] if isinstance(r[c], str) else json.dumps(r[c], ensure_ascii=False))
                       for c in cols) + (json.dumps(r, ensure_ascii=False),) for r in rows])
            counts[table] = len(rows)
        con.commit()
    finally:
        con.close()
    tmp.replace(path)
    return counts


def axis_db_counts(path: Path) -> dict:
    con = sqlite3.connect(path)
    try:
        return {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in DB_TABLES}
    finally:
        con.close()


# --------------------------------------------------------------------------- #
# the stage
# --------------------------------------------------------------------------- #

def _source_mix(sc) -> dict:
    return dict(Counter(str(q.get("axis_source") or "not recorded") for q in _rows(sc, DB_TABLES["questions"][0])))


def frd_assess_stage(ctx) -> dict:
    cfg = ctx.cfg.get("frd_assess", {}) or {}
    if not cfg.get("enabled", True):
        return {"skipped": True}
    t0, u0 = time.time(), ctx.llm.usage_summary()
    frame = ctx.frame
    gauge = int(frame.get("gauge") or ctx.cfg["quest"].get("gauge", 64))
    words = int(cfg.get("partition_words", 30000))
    axes = {a["axis_id"]: a for a in frame["axes"]}
    jobs: list[_Job] = []
    mix, dbs = {}, {}
    if ctx.axis_layout:
        scopes = {sc.axis_id: sc for sc in ctx.scopes()}
        per_axis = {a: _rows(sc, REL_RETAINED) for a, sc in scopes.items()}
        rows = combined_rows(per_axis)
        shared = ctx.axis_dir(SHARED_FOLDER) / COMBINED_DIR
        for a, sc in scopes.items():
            mix[a] = _source_mix(sc)
            jobs.append(_Job(ctx, axes[a], per_axis[a], "axis-only", sc.p("frds", EVAL_DIR), gauge, words))
        do_combined = bool(cfg.get("combined", True)) and len(axes) > 1
        if do_combined:
            write_json(shared / "combined-validated-frds.json", rows)
            atomic_write_text(shared / "README.md", (
                "# Combined validated FRDs\n\nThe validated FRDs of every axis in one set: a disjoint union, each row "
                "labelled `home_axis`. The canonical record is in the home axis's folder. `for-<axis>/` holds the "
                "preliminary assessment of that axis's hypotheses against this whole set.\n\n"
                + "\n".join(f"- {a}: {len(fs)}" for a, fs in per_axis.items()) + f"\n- combined: {len(rows)}\n"))
            jobs += [_Job(ctx, axes[a], rows, "combined", shared / f"for-{a}", gauge, words) for a in axes]
    else:
        # single-database run: the FRDs are not filed by axis, so only the whole-set reading exists
        rows = sorted(_rows(ctx, REL_RETAINED), key=frd_id)
        per_axis = {}
        jobs = [_Job(ctx, a, rows, "combined", ctx.p("frds", f"{EVAL_DIR}/for-{aid}"), gauge, words)
                for aid, a in axes.items()]
    live = [j for j in jobs if j.frds]
    reqs = [(j, r) for j in live for r in j.partition_requests()]
    resp = ctx.llm.call_many([r for _, r in reqs]) if reqs else []
    pos = 0
    for j in live:
        j.take_partitions(resp[pos:pos + len(j.parts)])
        pos += len(j.parts)
    syn = [(j, j.synthesis_request()) for j in live]
    syn = [(j, r) for j, r in syn if r is not None]
    syn_resp = dict(zip([id(j) for j, _ in syn], ctx.llm.call_many([r for _, r in syn]) if syn else []))
    results: dict = {a: {} for a in axes}
    for j in jobs:
        results[j.aid][j.scope] = j.finish(syn_resp.get(id(j)))
    if ctx.axis_layout:
        for a, sc in scopes.items():
            dbs[a] = write_axis_db(sc)
    u1 = ctx.llm.usage_summary()
    table = {}
    for a, r in results.items():
        own, comb = (r.get("axis-only") or {}).get("allocations"), (r.get("combined") or {}).get("allocations")
        ids = [h["id"] for h in axes[a].get("hypotheses", [])]
        table[a] = {"axis_only": own, "combined": comb,
                    "equal_weight_for_comparison_only": largest_remainder(
                        {i: own.get(i, 0) + comb.get(i, 0) for i in ids}, gauge) if own and comb else None}
    after_fact = {a: sum(n for k, n in m.items() if "after-the-fact" in k or k == "not recorded") for a, m in mix.items()}
    record = {
        "run": ctx.run_id, "label": "PRELIMINARY, evidence-level assessment of the validated FRDs", "gauge": gauge,
        "frd_counts": {**{a: len(fs) for a, fs in per_axis.items()}, "combined": len(rows)},
        "combined_is_disjoint_union": (len(rows) == sum(len(fs) for fs in per_axis.values())) if per_axis else None,
        "table": table,
        "final_score_rule": "none chosen: the axis-only and combined vectors are reported side by side; the "
                            "equal-weight row is for comparison only",
        "axis_filing": {a: {"questions_by_axis_source": m, "assigned_after_the_fact": after_fact[a]} for a, m in mix.items()},
        "provisional": any(after_fact.values()),
        "results": results, "axis_databases": dbs,
        "problems": [p for j in jobs for p in j.problems],
        "warnings": [w for r in results.values() for s in r.values() for w in s.get("warnings", [])],
        "measured": {"seconds": round(time.time() - t0, 1),
                     "billed_model_calls": u1.get("live_calls", 0) - u0.get("live_calls", 0),
                     "estimated_usd": round(u1.get("estimated_usd", 0) - u0.get("estimated_usd", 0), 4),
                     "note": "the dollar figure is the harness's own estimate from token counts; the provider's "
                             "dashboard is the authority"},
        "time": utcnow(), "caveat": CAVEAT}
    write_json(ctx.run_dir / "frd-evaluation.json", record)
    atomic_write_text(ctx.run_dir / "FRD-EVALUATION.md", render(ctx, record, axes))
    return {"frd_counts": record["frd_counts"],
            "vectors": {a: {k: v for k, v in t.items() if k != "equal_weight_for_comparison_only"} for a, t in table.items()},
            "provisional": record["provisional"], "problems": record["problems"], "warnings": record["warnings"]}


def render(ctx, rec: dict, axes: dict) -> str:
    g = rec["gauge"]
    out = [f"# Preliminary evaluation of the validated FRDs — {rec['run']}", "",
           f"*{rec['time']}. {CAVEAT}*", ""]
    if rec["provisional"]:
        tot = {a: sum(f["questions_by_axis_source"].values()) for a, f in rec["axis_filing"].items()}
        out += ["> **PROVISIONAL.** " + "; ".join(
            f"{a}: {f['assigned_after_the_fact']} of {tot[a]} questions were filed under the axis after the fact"
            for a, f in rec["axis_filing"].items()) +
            ". The axis filing is provisional, so the axis-only vectors below are provisional too.", ""]
    out += [f"Each row sums to the gauge, G = {g}. No blended score is chosen: read the first two rows; the third is "
            f"for comparison only.", ""]
    for a, t in rec["table"].items():
        ax = axes[a]
        ids = [h["id"] for h in ax.get("hypotheses", [])]
        r = rec["results"][a]
        n_own = rec["frd_counts"].get(a)
        out += [f"## {a}: {ax.get('name') or ax.get('question', '')}", ""]
        if rec["axis_filing"].get(a):
            out += ["Questions by how they got this axis: " + ", ".join(
                f"{k} {n}" for k, n in rec["axis_filing"][a]["questions_by_axis_source"].items()) + ".", ""]
        out += ["| Evidence set | Validated FRDs | " + " | ".join(ids) + " |", "|---|---|" + "---|" * len(ids)]
        for label, key, n in (("This axis's FRDs only", "axis_only", n_own),
                              ("Combined (all axes' FRDs)", "combined", rec["frd_counts"]["combined"]),
                              ("Equal weight of the two (comparison only)", "equal_weight_for_comparison_only", "")):
            v = t.get(key)
            if (key == "axis_only" and "axis-only" not in r) or (key != "axis_only" and "combined" not in r):
                continue
            out.append(f"| {label} | {'' if n is None else n} | " +
                       " | ".join(str(v.get(i, "")) if v else "not produced" for i in ids) + " |")
        out.append("")
        if "combined" not in r:
            out += ["This run has one axis, so the combined set is the same as this axis's set.", ""]
        if "axis-only" not in r:
            out += ["This run keeps one database for all axes, so only the whole-set reading exists.", ""]
        for scope, title in (("axis-only", "This axis's FRDs only"), ("combined", "Combined set")):
            s = r.get(scope)
            if not s:
                continue
            out += [f"### {title}", ""]
            if not s["frd_count"]:
                out += ["No validated FRDs: nothing was assessed.", ""]
                continue
            out.append(f"- Partitions: {s['partition_count']} ({s['partition_rule']})." + (
                f" Mechanical mean of the partitions: {s['mechanical_mean_of_partitions']}; the result differs from it by "
                f"at most {s['result_vs_mechanical_mean_units']} units; partitions differ from each other by at most "
                f"{s['partition_spread_units']}." if s["partition_count"] > 1 else ""))
            for k, lab in (("basis_confidence", "Basis and confidence"), ("strongest_objection", "Strongest objection"),
                           ("reversal_finding", "What would reverse it")):
                if s.get(k):
                    out.append(f"- {lab}: {s[k]}")
            if s["drivers"]:
                out.append("- Drivers:")
                out += [f"  - `{d['frd_id']}` (home {d['home_axis']}, {d['source_file']})"
                        f"{' favors ' + d['favors'] if d['favors'] else ''}: {d['why']}" for d in s["drivers"][:12]]
            if scope == "combined":
                oth = s["other_axis_drivers"]
                out.append(f"- FRDs from other axes that were material here: {len(oth)}" + (
                    " (" + ", ".join(f"`{d['frd_id']}` from {d['home_axis']}" for d in oth[:12]) + ")" if oth else ""))
            if s["driver_ids_not_in_registry"]:
                out.append(f"- Cited ids that are not in the registry (ignored): {s['driver_ids_not_in_registry'][:8]}")
            for p in s["problems"] + s["warnings"]:
                out.append(f"- **Problem:** {p}")
            out.append("")
    m = rec["measured"]
    out += ["## Measured", "", f"- {m['seconds']} seconds, {m['billed_model_calls']} billed model calls, "
            f"${m['estimated_usd']} by the harness's estimate ({m['note']}).", "",
            "## Where the records are", "",
            "- Per axis: `AXIS-<id>/03_FRDS/06_evaluation/` (`evaluation.json`, `evaluation.md`, one file per partition) "
            "and `AXIS-<id>/axis.db`.",
            f"- Combined set: `{SHARED_FOLDER}/{COMBINED_DIR}/combined-validated-frds.json`; per-axis readings of it in "
            f"`{SHARED_FOLDER}/{COMBINED_DIR}/for-<axis>/`.",
            "- Everything on this page as data: `frd-evaluation.json`.", "",
            ]
    if (ctx.cfg.get("pipeline", {}) or {}).get("stop_after") == "frd_assess":
        out += ["## Next", "",
                "The run halts here. The dictionary, canonicalizer, transcoding, witnesses and matching are not "
                "started until you ask for them:", "", f"    cr run \"{ctx.project_dir}\" --run {ctx.run_id} --continue", ""]
    return "\n".join(out)
