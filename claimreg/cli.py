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


def _frame_gate(project, action: str, always: bool = False) -> bool:
    """Remind the researcher of the coach when the frame has not been through `cr sign`.  A run that
    uses no model (the offline engine, the tests) gets no reminder.  Only a quest waits for it."""
    from . import frame_gate
    from .config import load_config
    if not always and not frame_gate.uses_models(load_config(project)):
        return True
    ok, msg = frame_gate.gate(Path(project), action)
    if msg and not frame_gate.accepted(Path(project))[0]:
        print(msg, file=sys.stderr)
    return ok


def cmd_run(a) -> int:
    from .pipeline import run_pipeline
    from .runctx import RunContext
    if not _frame_gate(a.project, "run"):
        return 2
    ctx = RunContext(a.project, a.run, create=True)
    out = run_pipeline(ctx, start=a.from_stage, stop=a.to_stage,
                       only=a.only.split(",") if a.only else None,
                       force=a.force.split(",") if a.force else None, release=getattr(a, "release", False))
    _print(out)
    if out["status"] == "halted":
        print(f"\nHalted for your decision after {out['gate']}. Read {ctx.run_dir / out['read']}\n"
              f"To run the later stages:\n  {out['continue_with']}")
        for n in (1, 2):
            if (ctx.run_dir / f"COACH-CHECKPOINT-{n}.md").exists() and out["read"] != f"COACH-CHECKPOINT-{n}.md":
                print(f"The coach's reading of where you stand: {ctx.run_dir / f'COACH-CHECKPOINT-{n}.md'}")
        if (ctx.run_dir / "QUESTIONS.md").exists():
            print(f"Before you continue: {ctx.run_dir / 'QUESTIONS.md'} lists every question this run asked. Give it "
                  f"and the source index to another model to check whether the questioning was thorough enough.")
    if out["status"] == "waiting":
        print(f"\n{out['pending']} model request(s) are queued. Batch files are in {Path(out['queue_dir']) / 'batches'} "
              f"(one .json and one .md per batch). Write each answer to <BATCH>.response.json "
              f"({{\"<key>\": \"<answer>\"}}) or <BATCH>.response.md, then run:\n"
              f"  cr queue import \"{a.project}\"\n  cr run \"{a.project}\"")
    return 0 if out["status"] in ("complete", "waiting", "halted") else 2


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


def cmd_import_quest(a) -> int:
    from .quest_import import QuestImportError, import_quest
    if not _frame_gate(a.project, "import", always=True):
        return 2
    try:
        out = import_quest(Path(a.project), Path(a.quest), run_id=a.run,
                           closeout=Path(a.closeout) if a.closeout else None, select=a.select,
                           stop=a.stop, exclude_tool_output=a.exclude_tool_output, force=a.force)
    except QuestImportError as e:
        print(f"import-quest: {e}", file=sys.stderr)
        return 2
    _print(out)
    return 0


def cmd_questions(a) -> int:
    """Write the question database (QUESTIONS.md) of a run and say where it is."""
    from .question_db import QUESTIONS_MD, write_question_database
    from .runctx import RunContext
    ctx = RunContext(a.project, a.run, quiet=True)
    db = write_question_database(ctx.run_dir, ctx.run_id)
    if not db:
        print(f"{ctx.run_id} has asked no questions yet; nothing written.")
        return 0
    t, src = db["totals"], db["sources"]
    print(f"{ctx.run_dir / QUESTIONS_MD}\n{t['questions']} questions, {t['answered']} answered, {t['flagged']} flagged; "
          f"{len(src['named'])} source file(s) named" + (f" of {src['indexed']} indexed" if src["indexed"] else "") + ".\n"
          f"To check the questioning, give that file and {ctx.run_dir / '01_FRAME' / 'index.md'} to another model. "
          f"The prompt is inside the file.")
    return 0


def cmd_quest_score(a) -> int:
    from .notebooklm.scorecard import main as score_main
    argv = [a.folder] + (["--start", a.start] if a.start else []) + sum((["--exclude", e] for e in a.exclude), []) \
        + (["--json"] if a.json else [])
    return score_main(argv)


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
        "providers": {"local": {"type": "local", "model": "local-rules-v1.9"}},
        "quest": {"round_size": 4, "max_rounds": 6},
        "pipeline": {"stop_after": ""},      # the demo shows every stage; a real project halts after frd_assess
    })
    ctx = RunContext(dst, a.run_id or "RUN-DEMO-1", create=True)
    out = run_pipeline(ctx)
    _print(out)
    if out["status"] == "complete":
        from .pipeline import print_outputs
        print_outputs(ctx)
    return 0 if out["status"] in ("complete", "waiting") else 2


def cmd_funnel(a) -> int:
    from .funnel import funnel, render
    from .runctx import RunContext
    ctx = RunContext(a.project, a.run, quiet=True)
    if not ctx.axis_layout:
        f = funnel(ctx)
        _print(f) if a.json else print(render(f))
        return 0
    # one evidence database per axis: one funnel per axis, never a mixed one
    per = {}
    for sc in ctx.scopes():
        f = funnel(sc)
        f["run"] = f"{ctx.run_id} - axis {sc.axis_id}"
        per[sc.axis_id] = f
    if a.json:
        _print(per)
    else:
        print("\n\n".join(render(f) for f in per.values()))
    return 0


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
    s.add_argument("--continue", dest="release", action="store_true",
                   help="release the run past the researcher's stop (pipeline.stop_after) and run the later stages")
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

    s = sub.add_parser("import-quest", help="import a recorded NotebookLM quest; cr run then continues at FRDs")
    s.add_argument("project", help="project folder with corpus, header and index (made by cr init)")
    s.add_argument("quest", help="the quest folder (quest_tool state or the driver's answers folder)")
    s.add_argument("--run", help="run id to create (default: a new <prefix>-QUEST-... run)")
    s.add_argument("--closeout", help="the Manager's closeout .md; its 'Selected repair attempts' line is honoured")
    s.add_argument("--select", action="append", default=[], metavar="QNNNN-ANN",
                   help="use this attempt for its question (repeatable); overrides the closeout")
    s.add_argument("--stop", choices=["operational", "scientific"], default="operational",
                   help="how the quest ended (default: operational)")
    s.add_argument("--exclude-tool-output", action="store_true",
                   help="drop answers flagged for NotebookLM tool output instead of keeping them as candidates")
    s.add_argument("--force", action="store_true", help="re-import into a run that already has a quest")
    s.set_defaults(fn=cmd_import_quest)

    s = sub.add_parser("questions", help="write QUESTIONS.md: every question a run asked, for a coverage check by another model")
    s.add_argument("project")
    s.add_argument("--run")
    s.set_defaults(fn=cmd_questions)

    s = sub.add_parser("quest-score", help="throughput scorecard for a NotebookLM quest (45/h standard)")
    s.add_argument("folder", help="quest_tool recording, driver answers folder, or a run's 02_DISCOVERY")
    s.add_argument("--start", help="the go-ahead time, e.g. 2026-11-10T09:00-06:00")
    s.add_argument("--exclude", action="append", default=[], metavar="START/END",
                   help="a disclosed interval when you were away (repeatable)")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_quest_score)

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

    from . import coach, frame_gate, onramp
    s = sub.add_parser("new", help="start a project: copy sources in, find your model keys, write the question template")
    s.add_argument("project")
    s.add_argument("--name")
    s.add_argument("--corpus", help="folder of Markdown sources (copied into the project)")
    s.add_argument("--keys", help="folder that holds your API key files (one .txt per provider)")
    s.add_argument("--key", action="append", default=[], metavar="PROVIDER=FILE",
                   help="one key file, e.g. deepseek=C:\\keys\\deepseek.txt (repeatable)")
    s.add_argument("--prefer", help="provider order, e.g. deepseek,openai,gemini (default: openai,deepseek,gemini,anthropic)")
    s.add_argument("--notebook", action="append", default=[], help="NotebookLM notebook link (repeat for each copy)")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=onramp.cmd_new)

    s = sub.add_parser("frame", help="draft the index, the Archivist prompt and the quest header from 01_FRAME/question.md")
    s.add_argument("project")
    s.add_argument("--gauge", type=int, default=64)
    s.add_argument("--axes", default="1")
    s.add_argument("--force", action="store_true", help="redo files that already exist")
    s.set_defaults(fn=onramp.cmd_frame)

    s = sub.add_parser("sign", aliases=["coach"],
                       help="go through the frame with the coach: say what you want, see how each framing is likely to "
                            "score, type the hypotheses yourself and accept the likely outcome (before a quest)")
    s.add_argument("project")
    s.add_argument("--axis", help="this axis only (for example A2); default: every axis not yet accepted")
    s.add_argument("--header", help="work on this draft instead of the project's header")
    s.add_argument("--name", help="your name, for the record")
    s.add_argument("--check", action="store_true", help="only say whether the frame has been accepted")
    s.set_defaults(fn=frame_gate.cmd_sign)

    s = sub.add_parser("rescore", help="score a run's validated findings under the header as it reads now (or another "
                                       "header); nothing in the run changes, and the score goes on the frame ladder")
    s.add_argument("project")
    s.add_argument("--run", required=True)
    s.add_argument("--header", help="score under this header file instead of the project's header")
    s.add_argument("--axis", help="this axis only (for example A2)")
    s.add_argument("--answers", action="store_true", help="score the quest's answers instead of the validated findings")
    s.add_argument("--times", type=int, help="scorings to average (default 3; 1 with --answers)")
    s.set_defaults(fn=coach.cmd_rescore)

    s = sub.add_parser("approve", help="mark the header draft approved without the coach (`cr sign` is the usual way)")
    s.add_argument("project")
    s.add_argument("--by", required=True, help="who approves it")
    s.add_argument("--header", help="approve this file instead of 01_FRAME/header-DRAFT.md")
    s.add_argument("--force", action="store_true", help="replace an existing header.md")
    s.set_defaults(fn=onramp.cmd_approve)

    s = sub.add_parser("doctor", help="check everything a quest needs: Python, Chrome, header, notebooks, each model key")
    s.add_argument("project", nargs="?")
    s.add_argument("--offline", action="store_true", help="do not contact the model providers")
    s.add_argument("--fix", action="store_true", help="when a configured model name is not offered, pick one that is")
    s.add_argument("--models", action="store_true", help="also list the models each key offers")
    s.add_argument("--notebooks", action="store_true",
                   help="also open each saved notebook link in Chrome to check it resolves")
    s.set_defaults(fn=onramp.cmd_doctor)

    s = sub.add_parser("quest", help="run the NotebookLM discovery quest unattended, then import it")
    s.add_argument("project")
    s.add_argument("--notebook", action="append", default=[], help="NotebookLM notebook link (repeat for each copy)")
    s.add_argument("--id", help="quest folder name (default: resume the open quest, else a new dated one)")
    s.add_argument("--new", action="store_true", help="start a new quest even if one is open")
    s.add_argument("--hours", default="3", help="time limit in hours (default 3)")
    s.add_argument("--max-questions", dest="max_questions", default="400")
    s.add_argument("--profile", help="Chrome profile folder the driver signs in with")
    s.add_argument("--no-driver", dest="no_driver", action="store_true",
                   help="do not start the NotebookLM driver (it is already running on this quest folder)")
    s.add_argument("--then-run", dest="then_run", action="store_true",
                   help="continue straight into the evidence pipeline and the report")
    s.set_defaults(fn=onramp.cmd_quest)

    s = sub.add_parser("funnel", help="where a run loses material, stage by stage, and what limits it")
    s.add_argument("project")
    s.add_argument("--run")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_funnel)

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
