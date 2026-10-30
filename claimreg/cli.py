"""Command-line interface:  python cr.py <command> ...   (or  cr.cmd on Windows)."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from . import __version__
from .util import ensure_dir, read_json, read_text, utcnow, write_json


def _print(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


def cmd_init(a) -> int:
    proj = Path(a.project)
    ensure_dir(proj)
    for sub in ("01_CORPUS/source-files", "01_CORPUS/manifests", "01_FRAME", "02_RUNS", "04_RELEASES",
                "90_METHOD/prompts", "99_ARCHIVE"):
        ensure_dir(proj / sub)
    cfg = read_json(proj / "project.json", default={}) or {}
    cfg.setdefault("project", {})["name"] = a.name or cfg.get("project", {}).get("name", proj.name)
    if a.corpus:
        src = Path(a.corpus)
        if a.copy_corpus:
            for p in sorted(src.rglob("*")):
                if p.is_file() and p.suffix.lower() in (".md", ".markdown", ".txt"):
                    dest = proj / "01_CORPUS" / "source-files" / p.relative_to(src)
                    ensure_dir(dest.parent)
                    shutil.copyfile(p, dest)
        else:
            cfg.setdefault("corpus", {})["source_dir"] = str(src.resolve())
    for flag, target in ((a.header, "header.md"), (a.index, "index.md"), (a.archivist, "archivist-custom-prompt.txt")):
        if flag:
            shutil.copyfile(flag, proj / "01_FRAME" / target)
    if a.provider:
        cfg["default_provider"] = a.provider
    write_json(proj / "project.json", cfg)
    for name, text in (("README.md", _domain_readme(cfg["project"]["name"])),
                       ("START-HERE.md", _start_here(proj))):
        if not (proj / name).exists():
            (proj / name).write_text(text, encoding="utf-8")
    print(f"project ready: {proj.resolve()}")
    print("next: put the approved header in 01_FRAME/header.md (and optionally index.md and "
          "archivist-custom-prompt.txt), then run:  cr run " + str(proj) + "\n"
          "The local engine answers every role by default. To use a model instead, set "
          "\"default_provider\" in project.json (see docs/USER-GUIDE.md section 2).")
    return 0


def _domain_readme(name: str) -> str:
    return (f"# {name} — Claim Registry domain\n\nThis folder is one Claim Registry (ACH 2.0) investigation "
            "domain: its corpus (01_CORPUS), frozen frame (01_FRAME), runs (02_RUNS) and releases "
            "(04_RELEASES).\n\nIt makes no claim beyond 'best understood from this corpus and this run'.\n")


def _start_here(proj: Path) -> str:
    return (f"# START HERE\n\n1. Check `01_FRAME/header.md` (the human-approved header).\n"
            f"2. `cr run \"{proj}\"` runs every stage; it stops cleanly when queued answers or budget are needed.\n"
            f"3. Read `02_RUNS/<run>/RUN-STATUS.md`, then `10_REPORTS/CRUX-REPORT.md` and `report.html`.\n")


def cmd_corpus(a) -> int:
    from .config import load_config, resolve_path
    from .corpus import ingest
    cfg = load_config(a.project)
    src = resolve_path(cfg, cfg["corpus"]["source_dir"])
    man = ingest(Path(a.project), src, tuple(cfg["corpus"].get("extensions", [".md"])))
    _print({k: man[k] for k in ("manifest_id", "files", "bytes")} |
           {"flagged": [(s["filename"], s["flags"]) for s in man["sources"] if s["flags"]]})
    return 0


def cmd_new_run(a) -> int:
    from .runctx import RunContext, new_run_id
    from .config import load_config
    cfg = load_config(a.project)
    rid = a.run_id or new_run_id(cfg["project"].get("run_prefix", "RUN"))
    ctx = RunContext(a.project, rid, create=True)
    print(ctx.run_id)
    return 0


def cmd_run(a) -> int:
    from .pipeline import run_pipeline
    from .runctx import RunContext
    ctx = RunContext(a.project, a.run, create=True)
    out = run_pipeline(ctx, start=a.from_stage, stop=a.to_stage,
                       only=a.only.split(",") if a.only else None,
                       force=a.force.split(",") if a.force else None)
    _print(out)
    if out["status"] == "waiting":
        print(f"\n{out['pending']} model request(s) are queued. Batch files are in {Path(out['queue_dir']) / 'batches'} "
              f"(one .json and one .md per batch). Write each answer to <BATCH>.response.json "
              f"({{\"<key>\": \"<answer>\"}}) or <BATCH>.response.md, then run:\n"
              f"  cr queue import \"{a.project}\"\n  cr run \"{a.project}\"")
    return 0 if out["status"] in ("complete", "waiting") else 2


def cmd_status(a) -> int:
    from .runctx import RunContext, list_runs
    ctx = RunContext(a.project, a.run, quiet=True)
    st = ctx.stage_state()
    _print({"run": ctx.run_id, "runs": list_runs(Path(a.project)),
            "stages": {k: {"status": v.get("status"), "summary": v.get("summary")} for k, v in st.items()},
            "usage": ctx.llm.usage_summary()})
    return 0


def cmd_queue(a) -> int:
    from .config import load_config
    from .llm.queue_tools import export_batches, import_responses, queue_dir, queue_status
    cfg = load_config(a.project)
    qd = queue_dir(Path(a.project), cfg["providers"].get("queue", {}).get("dir", "queue"))
    if a.action == "status":
        _print(queue_status(qd))
    elif a.action == "export":
        made = export_batches(qd, size=a.size, role=a.role, repack=True)
        _print({"batches": [str(m) for m in made]})
    elif a.action == "import":
        model = a.operator_model or cfg["providers"].get("queue", {}).get("model", "queue-operator")
        _print(import_responses(qd, operator_model=model))
    elif a.action == "skip":
        from .llm.queue_tools import skip_requests
        keys = list(a.key or [])
        if a.batch:
            b = read_json(qd / "batches" / (a.batch if a.batch.endswith(".json") else a.batch + ".json")) or {}
            keys += [r["key"] for r in b.get("requests", [])
                     if not (qd / "done" / f"{r['key']}.txt").exists()]
        model = a.operator_model or cfg["providers"].get("queue", {}).get("model", "queue-operator")
        _print(skip_requests(qd, keys, a.reason, model))
    return 0


def cmd_import_chatgpt(a) -> int:
    from .legacy import import_chatgpt_ptx
    out = import_chatgpt_ptx(Path(a.chatgpt_run), Path(a.project), a.run_id or "RUN-PTX-IMPORT",
                             copy_corpus=not a.no_copy)
    _print(out)
    return 0


def cmd_publish(a) -> int:
    from .publish import publish
    out = publish(Path(a.project), a.run, include_corpus=True if a.include_corpus else None)
    print(f"release written: {out}")
    return 0


def cmd_fork(a) -> int:
    from .publish import fork
    over: dict = {}
    for kv in a.set or []:
        k, v = kv.split("=", 1)
        try:
            v = json.loads(v)
        except Exception:
            pass
        cur = over
        parts = k.split(".")
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = v
    rid = fork(Path(a.project), a.parent, a.name, over, a.note or "")
    print(f"fork created: {rid}  (run 'cr run \"{a.project}\" --run {rid}' to re-run affected stages)")
    return 0


def cmd_diff(a) -> int:
    from .publish import diff_runs
    _print(diff_runs(Path(a.project), a.run_a, a.run_b))
    return 0


def cmd_verify(a) -> int:
    from .verify import verify_run
    out = verify_run(Path(a.project), a.run)
    _print(out)
    return 0 if out.get("ok") else 3


def cmd_header_draft(a) -> int:
    from .llm.base import LLMRequest
    from .runctx import RunContext
    ctx = RunContext(a.project, a.run, create=True)
    frame_txt = read_text(a.frame_file)
    ip = Path(a.project) / "01_FRAME" / "index.md"
    ap = Path(a.project) / "01_FRAME" / "archivist-custom-prompt.txt"
    system, user, _ = ctx.prompts.render(
        "header_draft.md", FRAME=frame_txt, INDEX=read_text(ip) if ip.exists() else "(no index yet)",
        ARCHIVIST=read_text(ap) if ap.exists() else "(no Archivist prompt yet)", RUN_ID=ctx.run_id,
        GAUGE=a.gauge, AXES=a.axes)
    res = ctx.llm.call(LLMRequest(role="investigator", system=system, user=user, expect_json=False,
                                  tag="header-draft", max_output_tokens=32000))
    text = res.text
    inv, _, coord = text.partition("=====COORDINATOR=====")
    out = Path(a.project) / "01_FRAME" / "header-DRAFT.md"
    out.write_text(inv.strip() + "\n", encoding="utf-8")
    (Path(a.project) / "01_FRAME" / "coordinator-handoff-DRAFT.md").write_text(coord.strip() + "\n", encoding="utf-8")
    print(f"draft written to {out}. A human must review and approve it, then save it as 01_FRAME/header.md.")
    return 0


def cmd_demo(a) -> int:
    """Copy the bundled synthetic domain into a project and run it end to end offline."""
    from .pipeline import run_pipeline
    from .runctx import RunContext
    root = Path(__file__).resolve().parent.parent
    src = root / "examples" / "demo"
    if not src.exists():
        print(f"demo corpus not found: {src}", file=sys.stderr)
        return 2
    if a.project:
        dst = Path(a.project)
        if dst.exists() and any(dst.iterdir()):
            if not a.force:
                print(f"{dst} already exists and is not empty. Use --force to replace it, or pass "
                      f"another project path.", file=sys.stderr)
                return 2
            shutil.rmtree(dst)
    else:
        # never overwrite the shipped demonstration: pick the first free name
        base = Path.cwd() / "projects"
        dst = base / "DEMO"
        n = 2
        while dst.exists() and any(dst.iterdir()):
            dst = base / f"DEMO-{n}"
            n += 1
    for sub in ("01_CORPUS/source-files", "01_FRAME", "02_RUNS", "04_RELEASES"):
        ensure_dir(dst / sub)
    for p in sorted((src / "sources").glob("*.md")):
        shutil.copyfile(p, dst / "01_CORPUS" / "source-files" / p.name)
    shutil.copyfile(src / "header.md", dst / "01_FRAME" / "header.md")
    shutil.copyfile(src / "README.md", dst / "README.md")
    write_json(dst / "project.json", {
        "project": {"name": "DEMO - synthetic silicate/wheat corpus", "run_prefix": "RUN-DEMO"},
        "default_provider": "local",
        "providers": {"local": {"type": "local", "model": "local-rules-v1.8"}},
        "quest": {"round_size": 4, "max_rounds": 6},
    })
    ctx = RunContext(dst, a.run_id or "RUN-DEMO-1", create=True)
    out = run_pipeline(ctx)
    _print(out)
    if out["status"] == "complete":
        print(f"\nreport:  {ctx.p('reports', 'CRUX-REPORT.md')}")
        print(f"browser: {ctx.p('reports', 'report.html')}")
    return 0 if out["status"] in ("complete", "waiting") else 2


def cmd_selftest(a) -> int:
    import unittest
    here = Path(__file__).resolve().parent.parent / "tests"
    suite = unittest.defaultTestLoader.discover(str(here))
    r = unittest.TextTestRunner(verbosity=1).run(suite)
    return 0 if r.wasSuccessful() else 1


def main(argv=None) -> int:
    # Windows consoles and redirected output default to a legacy code page; never crash on a
    # source name or quotation outside it
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(prog="cr", description=f"Claim Registry harness {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create a project folder")
    s.add_argument("project")
    s.add_argument("--name")
    s.add_argument("--corpus", help="folder of Markdown sources")
    s.add_argument("--copy-corpus", action="store_true", help="copy sources into the project")
    s.add_argument("--header")
    s.add_argument("--index")
    s.add_argument("--archivist")
    s.add_argument("--provider", help="default provider for every role (openai, anthropic, deepseek, queue, mock)")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("corpus", help="hash the corpus and write a manifest")
    s.add_argument("project")
    s.set_defaults(fn=cmd_corpus)

    s = sub.add_parser("new-run", help="create a new run")
    s.add_argument("project")
    s.add_argument("--run-id")
    s.set_defaults(fn=cmd_new_run)

    s = sub.add_parser("run", help="run (or resume) the pipeline")
    s.add_argument("project")
    s.add_argument("--run")
    s.add_argument("--from", dest="from_stage")
    s.add_argument("--to", dest="to_stage")
    s.add_argument("--only")
    s.add_argument("--force")
    s.set_defaults(fn=cmd_run)

    s = sub.add_parser("status", help="show stage status")
    s.add_argument("project")
    s.add_argument("--run")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("queue", help="queued model requests: status | export | import")
    s.add_argument("action", choices=["status", "export", "import", "skip"])
    s.add_argument("--key", action="append", help="skip: request key (repeatable)")
    s.add_argument("--batch", help="skip: every unanswered request in this batch file name")
    s.add_argument("--reason", default="operator could not answer")
    s.add_argument("project")
    s.add_argument("--size", type=int, default=8)
    s.add_argument("--role")
    s.add_argument("--operator-model")
    s.set_defaults(fn=cmd_queue)

    s = sub.add_parser("import-chatgpt", help="import the ChatGPT-era PTX full run")
    s.add_argument("chatgpt_run")
    s.add_argument("project")
    s.add_argument("--run-id")
    s.add_argument("--no-copy", action="store_true")
    s.set_defaults(fn=cmd_import_chatgpt)

    s = sub.add_parser("publish", help="write a release with hashes")
    s.add_argument("project")
    s.add_argument("--run")
    s.add_argument("--include-corpus", action="store_true")
    s.set_defaults(fn=cmd_publish)

    s = sub.add_parser("fork", help="fork a run with declared changes")
    s.add_argument("project")
    s.add_argument("--from", dest="parent", required=True)
    s.add_argument("--name")
    s.add_argument("--set", action="append", help="config override, e.g. witness.raw_ceiling=80")
    s.add_argument("--note")
    s.set_defaults(fn=cmd_fork)

    s = sub.add_parser("diff", help="compare two runs")
    s.add_argument("project")
    s.add_argument("run_a")
    s.add_argument("run_b")
    s.set_defaults(fn=cmd_diff)

    s = sub.add_parser("verify", help="re-check a run's records mechanically")
    s.add_argument("project")
    s.add_argument("--run")
    s.set_defaults(fn=cmd_verify)

    s = sub.add_parser("header-draft", help="draft a quest header (human approval required)")
    s.add_argument("project")
    s.add_argument("frame_file", help="text file: question, scope, approved hypotheses")
    s.add_argument("--run")
    s.add_argument("--gauge", type=int, default=64)
    s.add_argument("--axes", default="1")
    s.set_defaults(fn=cmd_header_draft)

    s = sub.add_parser("demo", help="run the bundled synthetic domain end to end offline")
    s.add_argument("--project", help="where to put it (default: projects/DEMO)")
    s.add_argument("--run-id")
    s.add_argument("--force", action="store_true", help="replace an existing non-empty folder")
    s.set_defaults(fn=cmd_demo)

    s = sub.add_parser("selftest", help="run the test suite")
    s.set_defaults(fn=cmd_selftest)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
