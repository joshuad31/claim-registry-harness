"""Publication (spec 34) and forking (spec 34.1)."""

from __future__ import annotations

import shutil
from pathlib import Path

from .runctx import RunContext, new_run_id
from .util import (atomic_write_text, ensure_dir, read_json, read_jsonl, sha256_file, utcnow,
                   write_json)

AFFECTS = [  # config prefix -> first stage that must rerun
    ("frame.", "frame"), ("quest.", "quest"), ("frd.", "frd_generate"), ("retention.", "frd_retain"),
    ("language.", "language"), ("witness.", "witnesses"), ("units.", "units"), ("matching.", "match"),
    ("coverage.", "joint"),   # joint groups and incompatibility checks read coverage.* settings too
    ("crux.", "crux"), ("assess.", "assess"), ("report.", "report"),
    ("roles.", "units"), ("providers.", "units"),
]


def publish(project_dir: Path, run_id: str | None = None, include_corpus: bool | None = None) -> Path:
    ctx = RunContext(project_dir, run_id)
    stamp = utcnow().replace("-", "").replace(":", "")[:15]          # e.g. 20261029T183745
    rel_id = f"RELEASE-{ctx.run_id}-{stamp}"
    out = Path(project_dir) / "04_RELEASES" / rel_id
    if out.exists():                                                  # never mix two releases
        shutil.rmtree(out)
    ensure_dir(out)
    # the run itself (without transient control files)
    for p in ctx.run_dir.rglob("*"):
        if p.is_file() and ".tmp-" not in p.name:
            dest = out / "run" / p.relative_to(ctx.run_dir)
            ensure_dir(dest.parent)
            shutil.copyfile(p, dest)
    # exact prompts and answers for every model call this run used
    calls = read_jsonl(ctx.p("control", "model-and-human-decisions", "llm-calls.jsonl"))
    keys = sorted({c["key"] for c in calls if c.get("status") in ("ok", "cache", "parse_error") and c.get("key")})
    n = 0
    for k in keys:
        src = Path(project_dir) / "cache" / "llm" / k[:2] / f"{k}.json"
        if src.exists():
            dest = out / "model-calls" / k[:2] / f"{k}.json"
            ensure_dir(dest.parent)
            shutil.copyfile(src, dest)
            n += 1
    # corpus manifest (+ corpus only when publishable)
    mdir = Path(project_dir) / "01_CORPUS" / "manifests"
    for p in mdir.glob("*.json"):
        ensure_dir(out / "corpus-manifest")
        shutil.copyfile(p, out / "corpus-manifest" / p.name)
    pub = ctx.cfg["project"].get("publishable", False) if include_corpus is None else include_corpus
    copied = 0
    if pub:
        src = Path(ctx.corpus.manifest["source_dir"])     # the corpus folder this run actually used
        if src.exists():
            for sp in sorted(src.rglob("*")):
                if sp.is_file() and sp.name in {Path(x["filename"]).name for x in ctx.corpus.manifest["sources"]}:
                    dest = out / "corpus" / sp.relative_to(src)
                    ensure_dir(dest.parent)
                    shutil.copyfile(sp, dest)
                    copied += 1
        pub = copied > 0
    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file():
            files[p.relative_to(out).as_posix()] = sha256_file(p)
    write_json(out / "RELEASE-MANIFEST.json", {
        "release_id": rel_id, "run_id": ctx.run_id, "created": utcnow(), "model_call_records": n,
        "corpus_included": bool(pub), "files": files})
    atomic_write_text(out / "README.md", f"""# {rel_id}

Release of run `{ctx.run_id}` of the Claim Registry project `{ctx.cfg['project']['name']}`.

* Start with `run/10_REPORTS/CRUX-REPORT.md`, then open `run/10_REPORTS/report.html` in a browser.
* `model-calls/` holds the exact prompt and answer of every model call ({n} records).
* `RELEASE-MANIFEST.json` lists every file with its sha256.
* Corpus included: {f'yes ({copied} files)' if pub else 'no (manifest with hashes only; supply the source files to rebuild)'}.

Rebuild without asking any model: make a project folder; put the corpus files in `01_CORPUS/source-files`,
the files of `run/01_FRAME` in `01_FRAME`, the whole `run` folder as `02_RUNS/{ctx.run_id}`, and the
`model-calls` folder as `cache/llm`. In its `project.json`, route every role to the `replay` provider and set
`"cache_fallback_providers"` to the provider names this run used, with the same provider settings
(see `run/RUN-CONFIG.json`). Then `cr run <project> --from units` reproduces every stage from the
recorded answers, and `cr verify <project>` re-checks them. With a live provider instead, the same
command re-runs the analysis.

Conclusions are best understood from this corpus and this run. Disagreement is demonstrated by forking and
re-running, not by appending criticism.
""")
    return out


def fork(project_dir: Path, parent_run: str, new_run: str | None = None,
         overrides: dict | None = None, note: str = "") -> str:
    parent = RunContext(project_dir, parent_run)
    child_id = new_run or new_run_id(parent.cfg["project"].get("run_prefix", "RUN") + "-FORK")
    child_dir = Path(project_dir) / "02_RUNS" / child_id
    if child_dir.exists():
        raise FileExistsError(child_dir)
    shutil.copytree(parent.run_dir, child_dir, ignore=shutil.ignore_patterns(".tmp-*"))
    overrides = overrides or {}
    # a fork of a fork keeps everything its parent declared, plus the new changes
    from .config import deep_merge
    inherited = read_json(parent.run_dir / "RUN-OVERRIDES.json", default={}) or {}
    write_json(child_dir / "RUN-OVERRIDES.json", deep_merge(inherited, overrides))
    flat = _flatten(overrides)
    from .pipeline import STAGE_NAMES
    first = None
    for key in flat:
        for pre, stage in AFFECTS:
            if key.startswith(pre):
                i = STAGE_NAMES.index(stage)
                first = i if first is None else min(first, i)
    st = read_json(child_dir / "00_RUN-CONTROL" / "stage-state.json", default={}) or {}
    reset = []
    if first is not None:
        for name in STAGE_NAMES[first:]:
            if name in st and st[name].get("status") != "imported":
                st[name]["status"] = "not started"
                reset.append(name)
    write_json(child_dir / "00_RUN-CONTROL" / "stage-state.json", st)
    write_json(child_dir / "FORK-RECORD.json", {"parent_run": parent.run_id, "child_run": child_id,
                                                "created": utcnow(), "declared_changes": flat,
                                                "stages_to_rerun": reset, "note": note})
    write_json(Path(project_dir) / "02_RUNS" / "CURRENT.json", {"run_id": child_id, "updated": utcnow()})
    return child_id


def _flatten(d: dict, pre: str = "") -> dict:
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(_flatten(v, f"{pre}{k}."))
        else:
            out[f"{pre}{k}"] = v
    return out


def diff_runs(project_dir: Path, a: str, b: str) -> dict:
    ca, cb = RunContext(project_dir, a, quiet=True), RunContext(project_dir, b, quiet=True)

    def summary(ctx):
        cov = (ctx.load("coverage", "coverage.json", default={}) or {}).get("hypotheses", {})
        crux = ctx.load("crux", "05_candidates/crux-candidates.json", default={}) or {}
        return {"coverage": {h: (c["status"], len(c.get("sets", [])), c.get("units_covered")) for h, c in cov.items()},
                "crux": sorted((c["witness_id"], c["home"], tuple(c["defeats"])) for c in crux.get("candidates", [])),
                "assessment": (ctx.load("reports", "assessment.json", default={}) or {}).get("allocations", {})}
    sa, sb = summary(ca), summary(cb)
    return {"run_a": a, "run_b": b,
            "coverage_changed": {h: (sa["coverage"].get(h), sb["coverage"].get(h))
                                 for h in set(sa["coverage"]) | set(sb["coverage"])
                                 if sa["coverage"].get(h) != sb["coverage"].get(h)},
            "crux_only_in_a": [x for x in sa["crux"] if x not in sb["crux"]],
            "crux_only_in_b": [x for x in sb["crux"] if x not in sa["crux"]],
            "assessment_a": sa["assessment"], "assessment_b": sb["assessment"],
            "conclusion_moved": sa["crux"] != sb["crux"] or sa["coverage"] != sb["coverage"]}
