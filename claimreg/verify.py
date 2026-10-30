"""Mechanical re-verification of a finished run (no model calls)."""

from __future__ import annotations

from pathlib import Path

from .corpus import find_quote
from .coverage import build_problem, complete, covers
from .matching import relations_index
from .runctx import RunContext
from .util import read_jsonl, read_text, sha256_file, word_count


def verify_run(project_dir: Path, run_id: str | None = None) -> dict:
    ctx = RunContext(project_dir, run_id, quiet=True)
    out: dict = {"run": ctx.run_id, "checks": {}}
    problems = []
    # 1. artifact registry: latest record per path must match the file on disk
    reg = read_jsonl(ctx.p("control", "artifact-registry.jsonl"))
    latest = {}
    for r in reg:
        latest[r["path"]] = r
    mism = [p for p, r in latest.items()
            if (ctx.run_dir / p).exists() and sha256_file(ctx.run_dir / p) != r["sha256"]]
    # files the user guide invites people to edit by hand are reported, not counted as problems
    editable = ("07_MATCHING/01_hypothesis-units/units.json",)
    edited = [p for p in mism if p.endswith(editable)]
    mism = [p for p in mism if p not in edited]
    out["checks"]["artifact_registry"] = {"artifacts": len(latest), "hash_mismatches": mism,
                                          "edited_by_hand_after_the_run": edited}
    problems += [f"hash mismatch: {p}" for p in mism]
    # 2. validated FRD quotes.  A source file that is not present is reported as
    # unverifiable, not as a mismatch: an archive may legitimately separate a run
    # from its third-party corpus, and calling that "quote not found" is false.
    ret = ctx.load("frds", "05_validated/retained-frds.json", default=None)
    if ret is None:
        ret = ctx.load("frds", "05_validated/validated-frds.json", default=[]) or []
    bad_q, unverifiable = [], []
    for v in ret:
        try:
            qc = find_quote(ctx.corpus.text(v["source_file"]), v.get("source_text", ""))
        except (FileNotFoundError, KeyError):
            unverifiable.append({"vfrd_id": v["vfrd_id"], "source_file": v["source_file"]})
            continue
        if not qc.get("found"):
            bad_q.append(v["vfrd_id"])
    out["checks"]["frd_quotes"] = {
        "checked": len(ret) - len(unverifiable), "not_found": bad_q,
        "unverifiable_sources_missing": unverifiable}
    warnings = []
    if unverifiable:
        warnings.append(
            f"{len(unverifiable)} FRD quotation(s) could not be checked because their source files are "
            f"not in this project. Restore the corpus (projects/<domain>/01_CORPUS/source-files) to "
            f"check them; the other checks below did not need the corpus.")
    problems += [f"quote not found: {x}" for x in bad_q]
    # 3. witnesses
    ws = ctx.load("witnesses", "05_released/witnesses.json", default=[]) or []
    over = [w["witness_id"] for w in ws if word_count(w["text"]) > w.get("ceiling", 60)]
    notpass = [w["witness_id"] for w in ws if w.get("audit_verdict") != "PASS"]
    out["checks"]["witnesses"] = {"released": len(ws), "over_ceiling": over, "released_without_pass": notpass}
    problems += [f"witness over ceiling: {x}" for x in over] + [f"released without PASS: {x}" for x in notpass]
    # 4. coverage sets: completeness and deletion-minimality, recomputed from the relations
    rel = relations_index(ctx)
    units = ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or []
    groups = ctx.load("matching", "03_match-records/joint-groups.json", default=[]) or []
    from .joint import incompatibility_records
    inc = incompatibility_records(ctx)
    cov = (ctx.load("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
    set_issues = []
    n_sets = 0
    for hid, c in cov.items():
        pb, _ = build_problem(hid, units, rel, groups, inc,
                              veto=bool(ctx.cfg["coverage"].get("constraint_veto", True)),
                              max_options=int(ctx.cfg["coverage"].get("max_options_per_unit", 12)))
        for s in c.get("sets", []):
            n_sets += 1
            ws_set = set(s["witnesses"])
            if not complete(pb, ws_set):
                set_issues.append(f"{s['set_id']}: not complete")
            for w in ws_set:
                if complete(pb, ws_set - {w}):
                    set_issues.append(f"{s['set_id']}: {w} removable (not deletion-minimal)")
        for u in c.get("uncovered_units", []):
            if pb.options.get(u):
                set_issues.append(f"{hid}: {u} reported uncovered but has options")
    out["checks"]["coverage_sets"] = {"sets": n_sets, "issues": set_issues}
    problems += set_issues
    # 5. crux candidates
    crux = ctx.load("crux", "05_candidates/crux-candidates.json", default={}) or {}
    tests = ctx.load("crux", "03_portability-tests/tests.json", default=[]) or []
    c_issues = []
    for cand in crux.get("candidates", []):
        home = cov.get(cand["home"], {})
        if not any(cand["witness_id"] in s["witnesses"] for s in home.get("sets", [])):
            c_issues.append(f"{cand['witness_id']}: not in a home set")
        for r in cand["defeats"]:
            if any(cand["witness_id"] in s["witnesses"] for s in cov.get(r, {}).get("sets", [])):
                c_issues.append(f"{cand['witness_id']}: member of rival {r}'s sets")
            t = next((t for t in tests if t["witness_id"] == cand["witness_id"] and t["rival"] == r
                      and t["kind"] == "crux"), None)
            if not t or t["t1"] != "FAIL" or t["t2"] != "FAIL":
                c_issues.append(f"{cand['witness_id']} vs {r}: tests do not both fail")
                continue
            for h in t["t1_certificate"].get("conflicting_rule_bundle", []):
                rr = rel.get((cand["witness_id"], h["unit_id"]))
                if not rr or rr["final"] != h["relation"]:
                    c_issues.append(f"{cand['witness_id']} vs {r}: certificate relation not in the matching record")
    out["checks"]["crux"] = {"candidates": len(crux.get("candidates", [])), "issues": c_issues}
    problems += c_issues
    # 6. report length
    rp = ctx.p("reports", "CRUX-REPORT.md")
    if rp.exists():
        wc = word_count(read_text(rp))
        out["checks"]["report_words"] = wc
        if wc >= 4000:
            problems.append(f"report has {wc} words (limit 4,000)")
    out["problems"] = problems
    if warnings:
        out["warnings"] = warnings
    out["ok"] = not problems
    return out
