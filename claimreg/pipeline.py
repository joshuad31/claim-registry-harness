"""Stage registry and the resumable pipeline runner."""

from __future__ import annotations

import shutil
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .config import resolve_path
from .corpus import current_manifest, ingest
from .llm.base import BudgetExceeded, LLMRequest, Pending, ProviderError
from .llm.queue_tools import export_batches, queue_dir, queue_status
from .runctx import RUN_FOLDERS, RunContext
from .util import atomic_write_text, read_json, read_text, utcnow, write_json


# --------------------------------------------------------------------------- #
# setup stages
# --------------------------------------------------------------------------- #

def stage_corpus(ctx: RunContext) -> dict:
    man = current_manifest(ctx.project_dir)
    src = resolve_path(ctx.cfg, ctx.cfg["corpus"]["source_dir"])
    if man is None or ctx.cfg["corpus"].get("reingest"):
        if not src or not src.exists():
            raise FileNotFoundError(f"corpus source folder not found: {src}")
        man = ingest(ctx.project_dir, src, tuple(ctx.cfg["corpus"].get("extensions", [".md"])))
    rc = ctx.run_config
    if rc.get("manifest_id") and rc["manifest_id"] != man["manifest_id"]:
        ctx.log(f"note: run pins manifest {rc['manifest_id']}; current project manifest is {man['manifest_id']}")
    else:
        write_json(ctx.run_dir / "RUN-CONFIG.json", {**rc, "run_id": ctx.run_id, "manifest_id": man["manifest_id"]})
    _ = ctx.corpus.chunks  # build the retrieval index once to validate it
    flagged = [s["filename"] for s in man["sources"] if s["flags"]]
    return {"manifest_id": man["manifest_id"], "files": man["files"], "bytes": man["bytes"],
            "chunks": len(ctx.corpus.chunks), "flagged_sources": flagged}


def stage_index(ctx: RunContext) -> dict:
    ip = resolve_path(ctx.cfg, ctx.cfg["frame"]["index_file"])
    if ip and ip.exists():
        return {"index": "supplied", "path": str(ip)}
    from .index import build_index_requests, render_index
    hp = resolve_path(ctx.cfg, ctx.cfg["frame"]["header_file"])
    question = ""
    if hp and hp.exists():
        from .header import parse_header
        fr = parse_header(read_text(hp))
        question = "\n".join(a.get("question", "") for a in fr["axes"]) or fr["title"]
    reqs = build_index_requests(ctx, question or ctx.cfg["project"]["name"])
    res = ctx.llm.call_many(reqs)
    entries = []
    for r, x in zip(reqs, res):
        d = x.parsed if x and isinstance(x.parsed, dict) else {}
        entries.append({"filename": r.meta["filename"], "rank": (d.get("rank") or "C").strip()[:1].upper(),
                        "author_year_title": d.get("author_year_title", ""), "relevance": d.get("relevance", ""),
                        "summary": d.get("summary", ""), "contradictions_and_gaps": d.get("contradictions_and_gaps", "")})
    atomic_write_text(ip, render_index(entries, ctx.cfg["project"]["name"]))
    return {"index": "generated", "entries": len(entries),
            "ranks": {k: sum(1 for e in entries if e["rank"] == k) for k in "ABCF"}}


def stage_archivist_prompt(ctx: RunContext) -> dict:
    ap = resolve_path(ctx.cfg, ctx.cfg["frame"]["archivist_prompt_file"])
    if ap and ap.exists():
        return {"archivist_prompt": "supplied"}
    hp = resolve_path(ctx.cfg, ctx.cfg["frame"]["header_file"])
    ip = resolve_path(ctx.cfg, ctx.cfg["frame"]["index_file"])
    from .index import compact_index, parse_index
    idx = compact_index(parse_index(read_text(ip), ctx.corpus), ctx.corpus) if ip and ip.exists() else \
        "\n".join(ctx.corpus.filenames)
    system, user, _ = ctx.prompts.render("archivist_writer.md", HEADER=read_text(hp), INDEX=idx)
    res = ctx.llm.call(LLMRequest(role="archivist_writer", system=system, user=user, expect_json=False,
                                  tag="archivist-prompt"))
    text = res.text.strip()
    banned = [w for w in ("ACH", "hypothesis", "Investigator", "Coordinator", "FRD", "witness", "crux")
              if w.lower() in text.lower()]
    atomic_write_text(ap, text + "\n")
    return {"archivist_prompt": "generated", "words": len(text.split()), "chars": len(text),
            "forbidden_words_present": banned}


def stage_frame(ctx: RunContext) -> dict:
    from .header import load_frame
    hp = resolve_path(ctx.cfg, ctx.cfg["frame"]["header_file"])
    ip = resolve_path(ctx.cfg, ctx.cfg["frame"]["index_file"])
    ap = resolve_path(ctx.cfg, ctx.cfg["frame"]["archivist_prompt_file"])
    frame = load_frame(ctx.project_dir, hp, int(ctx.cfg["quest"].get("gauge", 64)))
    fdir = ctx.p("frame")
    if hp and hp.exists():
        shutil.copyfile(hp, fdir / "header.md")
    if ip and ip.exists():
        shutil.copyfile(ip, fdir / "index.md")
    if ap and ap.exists():
        shutil.copyfile(ap, fdir / "archivist-custom-prompt.txt")
    write_json(fdir / "frame.json", frame)
    ctx._frame = frame
    man = current_manifest(ctx.project_dir)
    ctx.freeze_run_config(frame.get("header_sha256", ""), man["manifest_id"] if man else "",
                          {"approval": {ax["axis_id"]: ax.get("approval") for ax in frame["axes"]},
                           "approval_note": ctx.cfg["frame"].get("approval_note", "")})
    return {"axes": len(frame["axes"]), "hypotheses": sum(len(a["hypotheses"]) for a in frame["axes"]),
            "decisive_tests": len(frame.get("decisive_tests", [])), "gauge": frame.get("gauge"),
            "approval": {ax["axis_id"]: ax.get("approval") for ax in frame["axes"]}}


def _wrap(fn_path: str) -> Callable:
    mod, fn = fn_path.rsplit(".", 1)

    def call(ctx):
        import importlib
        return getattr(importlib.import_module(f"claimreg.{mod}"), fn)(ctx)
    return call


@dataclass
class Stage:
    name: str
    folder: str
    func: Callable
    title: str
    reset: Callable | None = None   # called before a stage is redone from scratch (not on resume)


def _reset_quest(ctx: RunContext) -> list[str]:
    """Move the quest's saved state aside (never deleted) so a forced, forked or upstream-changed
    quest starts again from round 1.  Cached model answers make identical rounds free."""
    import shutil
    d = ctx.p("discovery")
    moved = []
    stamp = utcnow().replace(":", "").replace("-", "")
    for sub in ("01_issued-questions", "02_query-responses", "03_quest-state", "04_ach-eval-checkpoints",
                "05_feedback", "06_closeout"):
        src = d / sub
        if src.exists() and any(src.iterdir()):
            dst = d / "99_superseded" / stamp / sub
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            src.mkdir(parents=True, exist_ok=True)
            moved.append(sub)
    return moved


STAGES = [
    Stage("corpus", "frame", stage_corpus, "Ingest, hash and index the corpus"),
    Stage("index", "frame", stage_index, "Ranked index (supplied or generated)"),
    Stage("archivist_prompt", "frame", stage_archivist_prompt, "Archivist custom prompt (supplied or generated)"),
    Stage("frame", "frame", stage_frame, "Parse and freeze the header, hypotheses and run configuration"),
    Stage("units", "matching", _wrap("units.derive_units"), "Internal coverage units (verbatim-anchored)"),
    Stage("quest", "discovery", _wrap("quest.run_quest"), "Coordinator-led discovery quest", _reset_quest),
    Stage("frd_generate", "frds", _wrap("frd.generate_frds"), "Candidate FRDs (one response at a time)"),
    Stage("frd_validate", "frds", _wrap("frd.validate_frds"), "Blind source-only validation + quote check"),
    Stage("frd_retain", "frds", _wrap("frd.retain_frds"), "Retention and archival (Problems-note budgets)"),
    Stage("language", "language", _wrap("language.language_stage"), "Custom dictionary and canonicalizer"),
    Stage("witnesses", "witnesses", _wrap("witness.build_witnesses"), "Question-guided witnesses + fidelity audit"),
    Stage("transcode", "transcoding", _wrap("language.transcode_stage"), "Transcode witnesses and units"),
    Stage("qualify", "matching", _wrap("matching.qualify"), "Matcher qualification on adversarial fixtures"),
    Stage("match", "matching", _wrap("matching.match_stage"), "Two-pass semantic matching"),
    Stage("joint", "matching", _wrap("joint.joint_stage"), "Jointly sufficient groups and incompatibilities"),
    Stage("coverage", "coverage", _wrap("coverage.coverage_stage"), "Deletion-minimal coverage sets"),
    Stage("crux", "crux", _wrap("crux.crux_stage"), "Frozen rival theories, T1/T2, crux candidates"),
    Stage("assess", "reports", _wrap("assess.assess_stage"), "Final ACH_Eval assessment of the witness registry"),
    Stage("report", "reports", _wrap("report.report_stage"), "Crux report and HTML audit browser"),
]
STAGE_NAMES = [s.name for s in STAGES]


def record_config_amendments(ctx: RunContext) -> list[str]:
    """If the scientific configuration changed after the run froze it, record the change
    (time, keys, old and new values) in RUN-CONFIG.json instead of letting it pass silently."""
    from .config import scientific_config
    from .util import canonical_json, read_json, utcnow, write_json
    path = ctx.run_dir / "RUN-CONFIG.json"
    rc = read_json(path, default=None)
    if not rc or "scientific_config" not in rc:
        return []
    cur = scientific_config(ctx.cfg)
    old = rc["scientific_config"]
    if canonical_json(cur) == canonical_json(old):
        return []

    def flat(d, pre=""):
        out = {}
        for k, v in (d or {}).items():
            if isinstance(v, dict):
                out.update(flat(v, f"{pre}{k}."))
            else:
                out[f"{pre}{k}"] = v
        return out
    fo, fn = flat(old), flat(cur)
    changed = sorted(k for k in set(fo) | set(fn) if canonical_json(fo.get(k)) != canonical_json(fn.get(k)))
    stages = {k: v.get("status") for k, v in ctx.stage_state().items()}
    rc.setdefault("amendments", []).append({
        "time": utcnow(), "changed": {k: {"before": fo.get(k), "after": fn.get(k)} for k in changed},
        "stage_status_at_amendment": stages,
        "note": "configuration changed after the run was frozen; stages finished before this time used the "
                "earlier values"})
    rc["scientific_config"] = cur
    write_json(path, rc)
    ctx.log("RUN-CONFIG amended: " + ", ".join(changed))
    return changed


def run_pipeline(ctx: RunContext, start: str | None = None, stop: str | None = None,
                 only: list[str] | None = None, force: list[str] | None = None) -> dict:
    force = set(force or [])
    record_config_amendments(ctx)
    names = STAGE_NAMES
    i0 = names.index(start) if start else 0
    i1 = names.index(stop) if stop else len(names) - 1
    state = ctx.stage_state()
    # "--from X" means: redo X and everything after it (imported stages stay imported, and the
    # stages after them are redone)
    dirty = False
    if start and state.get(start, {}).get("status") != "imported":
        force.add(start)
    elif start:
        dirty = True
    outcome = {"status": "complete", "ran": [], "skipped": []}
    for st in STAGES[i0:i1 + 1]:
        if only and st.name not in only:
            continue
        prev = state.get(st.name, {})
        if prev.get("status") in ("done", "imported") and not dirty and st.name not in force:
            outcome["skipped"].append(st.name)
            continue
        if prev.get("status") == "imported" and st.name not in force:
            outcome["skipped"].append(st.name)
            continue
        ctx.log(f"== stage {st.name}: {st.title}")
        # redo from scratch unless this is a resume (waiting for answers, interrupted, failed, partial)
        if st.reset and prev.get("status") in (None, "not started", "done"):
            moved = st.reset(ctx)
            if moved:
                ctx.log(f"   {st.name}: earlier state moved to 99_superseded ({', '.join(moved)})")
        ctx.set_stage(st.name, "running")
        errors_before = ctx.llm.error_count
        try:
            summary = st.func(ctx)
        except Pending as p:
            qd = queue_dir(ctx.project_dir, ctx.cfg["providers"].get("queue", {}).get("dir", "queue"))
            bs = ctx.cfg.get("queue_batch_size", 8)
            made = export_batches(qd, size=bs if isinstance(bs, dict) else int(bs),
                                  max_chars=int(ctx.cfg.get("queue_batch_max_chars", 120_000)))
            qs = queue_status(qd)
            ctx.set_stage(st.name, "waiting", {"pending": qs["pending"], "batches": [m.name for m in made]})
            ctx.log(f"stage {st.name}: waiting for {qs['pending']} queued model answer(s) "
                    f"({len(qs['open_batches'])} open batch file(s) in {qd / 'batches'}).")
            outcome.update(status="waiting", stage=st.name, pending=qs["pending"], queue_dir=str(qd))
            break
        except BudgetExceeded as e:
            ctx.set_stage(st.name, "budget", {"error": str(e)})
            ctx.log(f"stage {st.name}: stopped by budget: {e}")
            outcome.update(status="budget", stage=st.name, error=str(e))
            break
        except Exception as e:  # noqa: BLE001 - record and surface every failure
            msg = f"{type(e).__name__}: {e}"
            if "skipped by the queue operator" in str(e):
                msg += (" - this stage cannot continue without that answer; delete its "
                        "queue/done/<key>.skip.json to have it asked again")
            ctx.set_stage(st.name, "error", {"error": msg, "trace": traceback.format_exc()[-3000:]})
            ctx.log(f"stage {st.name}: ERROR {msg}")
            outcome.update(status="error", stage=st.name, error=msg)
            break
        failed = ctx.llm.error_count - errors_before
        if failed:
            # model calls that failed (not deliberately skipped) are not cached: the next
            # 'cr run' redoes this stage and asks them again
            summary = {**(summary or {}), "failed_model_calls": failed}
            ctx.set_stage(st.name, "partial", summary)
            ctx.log(f"   {st.name}: {summary}  [PARTIAL: {failed} model call(s) failed; run again to retry]")
            outcome.setdefault("partial", []).append(st.name)
        else:
            ctx.set_stage(st.name, "done", summary)
            ctx.log(f"   {st.name}: {summary}")
        dirty = True
        outcome["ran"].append(st.name)
    try:
        from .prompts import PromptLibrary  # noqa: F401
        ctx.prompts.snapshot(ctx.p("control", "prompt-snapshots"))
    except Exception:
        pass
    write_navigation(ctx)
    outcome["usage"] = ctx.llm.usage_summary()
    return outcome


# --------------------------------------------------------------------------- #
# navigation files required by the workspace standard (spec 10, s.5)
# --------------------------------------------------------------------------- #

README_TEXT = {
    "01_FRAME": ("Frozen frame: header, hypotheses, ranked index, Archivist instructions, coverage units.",
                 "The human-approved header and index; the corpus manifest.",
                 "frame.json, header.md, index.md, archivist-custom-prompt.txt, coverage-units.json",
                 "Compare header.md's sha256 with RUN-CONFIG.json; every unit's source_quote is checked verbatim.",
                 "Discovery (02) and matching (07) read this frame.",
                 "It does not establish that the hypotheses are complete, fair, or true."),
    "02_DISCOVERY": ("Coordinator-led quest: issued questions, exact Archivist answers, ACH_Eval checkpoints, "
                     "feedback packets, closeout.",
                     "Frozen header and index (Investigator, Coordinator); corpus passages (Archivist only).",
                     "01_issued-questions, 02_query-responses, 03_quest-state, 04_ach-eval-checkpoints, "
                     "05_feedback, 06_closeout",
                     "Every question has one QID and 1-3 named sources; every answer is stored verbatim with "
                     "the passages the Archivist saw.",
                     "FRD generation (03) processes one usable answer at a time.",
                     "Answers are discovery material, not evidence; allocations are uncalibrated judgments."),
    "03_FRDS": ("Candidate FRDs, blind validation, retained validated FRDs.",
                "Usable query-response records (generation); one FRD + its named source only (validation).",
                "candidates.json, harvest.json, validations.json, validated-frds.json, retained-frds.json, "
                "retention.json",
                "Each validated FRD's source_text was searched for in the named source file (quote_check).",
                "Witness construction (05).",
                "Faithful representation of a source is not the truth of that source."),
    "04_LANGUAGE-TOOLS": ("Custom dictionary and canonicalizer rulebook (when language.mode = labels).",
                          "Validated FRDs, the trusted ACH_Eval fragment, the index ranks.",
                          "dictionary-entries.json, rulebook.md, LANGUAGE-STATUS.json",
                          "Inspect LANGUAGE-STATUS.json for the mode and sources of each tool.",
                          "Transcoding (06).", "Conformance is compliance with language rules, not truth."),
    "05_WITNESSES": ("Question applications, every witness version, fidelity audits, held and released witnesses.",
                     "The producing question and one retained validated FRD per witness.",
                     "applications.json, witness-versions.json, audits.json, held.json, witnesses.json",
                     "Released witnesses passed an independent two-direction audit and mechanical checks.",
                     "Transcoding (06) and matching (07).",
                     "A PASS is a best-effort judgment, not proof of losslessness."),
    "06_TRANSCODING": ("Raw and transcoded witness and unit texts with conformance results.",
                       "Released witnesses, active units, the dictionary and rulebook.",
                       "transcoded.json", "Every item records its status (PASS / REVIEW / IDENTITY).",
                       "Matching (07).", "Transcoding standardizes representation; it does not decide meaning."),
    "07_MATCHING": ("Coverage units, matcher qualification, two-pass relations, disputes, joint groups, "
                    "incompatibilities.",
                    "Transcoded (or identity) witness and unit texts only; metadata never supplies coverage.",
                    "units.json, qualification.json, relations.json, disputes.json, joint-groups.json, "
                    "incompatibilities.json",
                    "Each relation shows pass A, pass B, the final relation and its basis "
                    "(AGREED / MODEL_ADJUDICATED / DISPUTED).",
                    "Coverage (08).", "Passing fixtures does not prove general language understanding."),
    "08_COVERAGE": ("Deletion-minimal hypothesis coverage sets with removal certificates and search status.",
                    "The approved matching record, joint groups, incompatibilities.",
                    "coverage.json", "Recheck any set by deleting each witness: every deletion must break coverage.",
                    "Crux identification (09).",
                    "Deletion-minimal is not smallest, unique, or strongest."),
    "09_CRUX": ("Frozen rival theories, portability tests (T1/T2) with certificates, crux candidates.",
                "Coverage sets, the matching record, incompatibilities.",
                "theories.json, tests.json, crux-candidates.json",
                "Every candidate's certificates name the conflicting units and match traces.",
                "The report (10).", "A crux does not establish truth, authority or dispositive weight."),
    "10_REPORTS": ("Analyst-facing crux report (< 4,000 words), HTML audit browser, metrics, final assessment.",
                   "Every earlier stage's records.", "CRUX-REPORT.md, report.html, metrics.json, assessment.json",
                   "Open report.html and follow any crux to its source quote.",
                   "Publication (04_RELEASES) or a fork.",
                   "Conclusions are 'best understood from this corpus and this run', never settled."),
}

STAGE_FOLDER = {s.name: RUN_FOLDERS[s.folder] for s in STAGES}


def write_navigation(ctx: RunContext) -> None:
    st = ctx.stage_state()
    for folder, (purpose, inputs, outputs, verify, nxt, notest) in README_TEXT.items():
        stages = [s.name for s in STAGES if RUN_FOLDERS[s.folder] == folder]
        status = "; ".join(f"{n}: {st.get(n, {}).get('status', 'not started')}" for n in stages) or "n/a"
        text = (f"# {folder}\n\n## Purpose\n{purpose}\n\n## Allowed inputs\n{inputs}\n\n## Expected outputs\n"
                f"{outputs}\n\n## Current status\n{status}\n\n## How to verify this stage\n{verify}\n\n"
                f"## Next handoff\n{nxt}\n\n## What this stage does not establish\n{notest}\n")
        atomic_write_text(ctx.run_dir / folder / "README.md", text)
    rows = ["| Stage | Status | Summary | Next action |", "|---|---|---|---|"]
    next_set = False
    for s in STAGES:
        rec = st.get(s.name, {})
        stat = rec.get("status", "not started")
        summ = rec.get("summary", {})
        short = ", ".join(f"{k}={v}" for k, v in list(summ.items())[:5]) if isinstance(summ, dict) else str(summ)
        nxt = ""
        if not next_set and stat not in ("done", "imported"):
            nxt = {"waiting": "answer queued requests, then `cr queue import` and `cr run`",
                   "error": "read the error in 00_RUN-CONTROL/stage-state.json, fix, rerun",
                   "budget": "raise the budget in project.json, rerun",
                   "partial": "some model calls failed; `cr run` asks them again"}.get(stat, "`cr run`")
            next_set = True
        rows.append(f"| {s.name} | {stat} | {short[:160]} | {nxt} |")
    atomic_write_text(ctx.run_dir / "RUN-STATUS.md",
                      f"# RUN-STATUS — {ctx.run_id}\n\nUpdated {utcnow()}\n\n" + "\n".join(rows) + "\n")
    links = "\n".join(f"- [{f}]({f}/README.md)" for f in README_TEXT)
    atomic_write_text(ctx.run_dir / "RUN-MAP.md",
                      f"# RUN-MAP — {ctx.run_id}\n\n- [RUN-STATUS.md](RUN-STATUS.md)\n- [RUN-CONFIG.json](RUN-CONFIG.json)\n"
                      f"- [Crux report](10_REPORTS/CRUX-REPORT.md) · [Audit browser](10_REPORTS/report.html)\n{links}\n"
                      f"- [Model call log](00_RUN-CONTROL/model-and-human-decisions/llm-calls.jsonl)\n"
                      f"- [Artifact registry](00_RUN-CONTROL/artifact-registry.jsonl)\n")
