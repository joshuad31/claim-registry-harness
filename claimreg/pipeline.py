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
from .runctx import RUN_FOLDERS, SHARED_FOLDER, RunContext
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
    from . import frame_gate
    signed, signed_why = frame_gate.verify(ctx.project_dir)
    for name in (frame_gate.CERT_MD, frame_gate.CERT_JSON):       # the signed frame certificate travels with the run
        src = ctx.project_dir / "01_FRAME" / name
        if signed and src.exists():
            shutil.copyfile(src, fdir / name)
    write_json(fdir / "frame.json", frame)
    ctx._frame = frame
    man = current_manifest(ctx.project_dir)
    ctx.freeze_run_config(frame.get("header_sha256", ""), man["manifest_id"] if man else "",
                          {"approval": {ax["axis_id"]: ax.get("approval") for ax in frame["axes"]},
                           "approval_note": ctx.cfg["frame"].get("approval_note", ""),
                           "frame_signed": signed, "frame_signature": signed_why})
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
    from .axes import reset_axis_discovery
    d = ctx.discovery_ctx().p("discovery")
    stamp = utcnow().replace(":", "").replace("-", "")
    moved = reset_axis_discovery(ctx, stamp)
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
    Stage("frd_assess", "frds", _wrap("frd_assess.frd_assess_stage"),
          "Preliminary ACH_Eval on the validated FRDs: per axis, then combined"),
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
# In a run that keeps one evidence database per axis, these stages run once per axis, each inside
# that axis's own folder and seeing only that axis's part of the frame (docs/AXIS-DATABASES.md).
# The language stage is not per axis: the dictionary and canonicalizer are SHARED resources.
PER_AXIS_STAGES = {"units", "frd_generate", "frd_validate", "frd_retain", "witnesses", "transcode",
                   "match", "joint", "coverage", "crux", "assess", "report"}
# run once for the whole run, into SHARED: tools nobody assesses (spec 10, 6.4 rule 7)
SHARED_STAGES = {"language", "qualify"}
# ... and these read the SHARED cross-axis evidence that bears on the axis's units
MERGE_SHARED_STAGES = {"joint", "coverage", "crux", "assess", "report"}


# A stage nothing downstream reads: running it does not make the later stages stale.
READ_ONLY_STAGES = {"frd_assess"}


def release_path(ctx: RunContext, gate: str):
    return ctx.p("control", "model-and-human-decisions") / f"released-after-{gate}.json"


def gate_state(ctx: RunContext) -> dict | None:
    """The researcher's stop: after `pipeline.stop_after` the run halts until it is released with
    `cr run --continue`.  Returns the halt record while the run is halted there, else None."""
    gate = (ctx.cfg.get("pipeline", {}) or {}).get("stop_after") or ""
    if gate not in STAGE_NAMES:
        return None
    if gate == "frd_assess" and not (ctx.cfg.get("frd_assess", {}) or {}).get("enabled", True):
        return None
    state = ctx.stage_state()
    later = STAGE_NAMES[STAGE_NAMES.index(gate) + 1:]
    if state.get(gate, {}).get("status") != "done" or release_path(ctx, gate).exists():
        return None
    if all(state.get(n, {}).get("status") in ("done", "imported") for n in later):
        return None
    return {"gate": gate, "next_stage": next(n for n in later if state.get(n, {}).get("status") not in ("done", "imported")),
            "read": "FRD-EVALUATION.md" if gate == "frd_assess" else "RUN-MAP.md",
            "continue_with": f'cr run "{ctx.project_dir}" --run {ctx.run_id} --continue'}


def run_stage(ctx: RunContext, st: Stage) -> dict:
    """Run one stage: once for an old-layout run, or once per axis database."""
    if not ctx.axis_layout or (st.name not in PER_AXIS_STAGES | SHARED_STAGES and st.name != "quest"):
        return st.func(ctx)
    from . import axes
    axes.ensure_axis_folders(ctx)
    if st.name in SHARED_STAGES:
        # one dictionary, one rulebook and one matcher qualification for the whole run
        return st.func(ctx.shared())
    if st.name == "quest":
        # one quest serves every axis, so its working records are SHARED; each question and answer
        # is then filed in the database of the one axis the question was asked for
        out = st.func(ctx.shared()) or {}
        return {**out, "by_axis": axes.partition_discovery(ctx)}
    use_shared = st.name in MERGE_SHARED_STAGES and axes.cross_enabled(ctx) and len(ctx.axis_ids()) > 1
    per: dict = {}
    for sc in ctx.scopes():
        sc.merge_shared = use_shared
        ctx.log(f"   [{sc.axis_id}] {st.name}")
        per[sc.axis_id] = st.func(sc) or {}
    if st.name == "match":
        shared = axes.cross_axis_match(ctx)
        if shared:
            per[SHARED_FOLDER] = shared
    if st.name == "match" or use_shared:
        axes.stage_cross_evidence(ctx)        # keep SHARED's copies and membership list current
    return per


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
                 only: list[str] | None = None, force: list[str] | None = None,
                 release: bool = False) -> dict:
    force = set(force or [])
    gate = (ctx.cfg.get("pipeline", {}) or {}).get("stop_after") or ""
    if release and gate in STAGE_NAMES and ctx.stage_state().get(gate, {}).get("status") == "done":
        from .util import utcnow, write_json
        if not release_path(ctx, gate).exists():
            write_json(release_path(ctx, gate), {"gate": gate, "released": utcnow(), "by": "cr run --continue",
                                                 "meaning": "the researcher read the results and asked for the later stages"})
            ctx.log(f"released after {gate}: the later stages may run")
    # an explicit --from or --only is itself the researcher's decision; a plain run or resume halts at the gate
    gated = bool(gate) and not start and not only
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
        halt = gate_state(ctx) if gated and gate in STAGE_NAMES and STAGE_NAMES.index(st.name) > STAGE_NAMES.index(gate) else None
        if halt:
            ctx.log(f"== halted for researcher decision after {gate}. Read {halt['read']}, then continue with: "
                    f"{halt['continue_with']}")
            outcome.update(status="halted", stage=gate, **halt)
            break
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
            summary = run_stage(ctx, st)
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
        if st.name not in READ_ONLY_STAGES:
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
    "08_COVERAGE": ("Deletion-minimal hypothesis coverage sets with removal certificates and search status, and "
                    "the premise ledger: where every required part of every hypothesis stands.",
                    "The approved matching record, joint groups, incompatibilities.",
                    "coverage.json, premise-ledger.json, PREMISE-LEDGER.md",
                    "Recheck any set by deleting each witness: every deletion must break coverage. A set marked "
                    "COMPLETE_WITH_ASSUMPTIONS lists each transfer it relies on.",
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


AXIS_CONTENTS = [   # what a reader looks for -> where it is inside an axis folder
    ("Questions asked for this axis", "02_DISCOVERY/01_issued-questions/questions.json"),
    ("Query responses (the notebook's exact answers)", "02_DISCOVERY/02_query-responses/responses.json"),
    ("FRD candidates", "03_FRDS/01_candidates/candidates.json"),
    ("FRD validations", "03_FRDS/04_validation-results/validations.json"),
    ("Validated FRDs", "03_FRDS/05_validated/validated-frds.json"),
    ("Retained validated FRDs", "03_FRDS/05_validated/retained-frds.json"),
    ("Preliminary evaluation of this axis's validated FRDs", "03_FRDS/06_evaluation/evaluation.json"),
    ("Database file of the questions, answers and FRDs (generated from the JSON records)", "axis.db"),
    ("Witnesses (released)", "05_WITNESSES/05_released/witnesses.json"),
    ("Witnesses held back by the audit", "05_WITNESSES/04_repaired-or-held/held.json"),
    ("Transcoded witnesses and units", "06_TRANSCODING/transcoded.json"),
    ("Coverage units of this axis's hypotheses", "07_MATCHING/01_hypothesis-units/units.json"),
    ("Match records (this axis's witnesses against this axis's units)", "07_MATCHING/03_match-records/relations.json"),
    ("Coverage sets", "08_COVERAGE/coverage.json"),
    ("Premise ledger", "08_COVERAGE/PREMISE-LEDGER.md"),
    ("Crux candidates", "09_CRUX/05_candidates/crux-candidates.json"),
    ("Assessment", "10_REPORTS/assessment.json"),
    ("Report", "10_REPORTS/CRUX-REPORT.md"),
    ("Evidence packets", "10_REPORTS/EVIDENCE-PACKETS.md"),
    ("Audit browser", "10_REPORTS/report.html"),
]


def _count(path) -> str:
    if not path.exists():
        return "not made yet"
    if path.suffix != ".json":
        return "written"
    d = read_json(path, default=None)
    if isinstance(d, list):
        return str(len(d))
    if isinstance(d, dict):
        for k in ("items", "hypotheses", "candidates"):
            if isinstance(d.get(k), (list, dict)):
                return str(len(d[k]))
    return "written"


def print_outputs(ctx: RunContext) -> None:
    """Tell the person where the results are: one report per axis in an axis-database run."""
    if not ctx.axis_layout:
        print(f"\nreport:  {ctx.p('reports', 'CRUX-REPORT.md')}\nledger:  {ctx.p('coverage', 'PREMISE-LEDGER.md')}"
              f"\nbrowser: {ctx.p('reports', 'report.html')}")
        return
    print(f"\nEach axis has its own database. Map of the run: {ctx.run_dir / 'RUN-MAP.md'}")
    for sc in ctx.scopes():
        print(f"\n{sc.axis_id}  {sc.root}\n  report:  {sc.p('reports', 'CRUX-REPORT.md')}"
              f"\n  ledger:  {sc.p('coverage', 'PREMISE-LEDGER.md')}\n  browser: {sc.p('reports', 'report.html')}")


def write_axis_navigation(ctx: RunContext, st: dict) -> str:
    """AXIS.md in every axis folder, a README in each of its stage folders and in SHARED.  Returns
    the lines RUN-MAP.md lists the databases with."""
    from .axes import cross_dir
    lines = []
    for sc in ctx.scopes():
        ax = sc.frame["axes"][0]
        root, a = sc.root, sc.axis_id
        if not root.exists():
            continue
        rows = ["| What | File | Records |", "|---|---|---|"]
        for label, rel in AXIS_CONTENTS:
            rows.append(f"| {label} | `{rel}` | {_count(root / rel)} |")
        hyps = "\n".join(f"- **{h['id']}** {h.get('title', '')}" for h in ax.get("hypotheses", []))
        how: dict = {}
        for q in read_json(root / "02_DISCOVERY" / "01_issued-questions" / "questions.json", default=[]) or []:
            how[q.get("axis_source", "not recorded")] = how.get(q.get("axis_source", "not recorded"), 0) + 1
        filed = ("; ".join(f"{n} by {k}" for k, n in sorted(how.items())) or "no questions yet") + \
            (". \"Assigned after the fact\" means the question was asked before questions carried an axis, "
             "and was filed here afterwards by reading it against the axes."
             if any("after-the-fact" in k for k in how) else ".")
        cross = cross_dir(ctx, a)
        atomic_write_text(root / "AXIS.md", (
            f"# Axis {a}: {ax.get('name') or root.name.split('__')[-1].replace('-', ' ')}\n\n"
            f"**Everything in this folder belongs to axis {a} and to no other axis.**\n\n"
            f"Question: {ax.get('question', '')}\n\nHypotheses:\n{hyps}\n\n"
            f"How this axis's questions were filed here: {filed}\n\n"
            f"## Where things are\n\n" + "\n".join(rows) + "\n\n"
            f"## What is not here\n\n"
            f"- Findings from another axis's questions that bear on this axis's hypotheses are SHARED records: "
            f"`../{SHARED_FOLDER}/{cross.name}/`"
            f"{'' if cross.exists() else ' (none recorded)'}. This axis's coverage, ledger and report read them and "
            f"label them with their home axis.\n"
            f"- The Manager's quest state and feedback packets cover every axis: `../{SHARED_FOLDER}/02_DISCOVERY/`.\n"
            f"- The dictionary and canonicalizer rulebook are one shared resource: `../{SHARED_FOLDER}/04_LANGUAGE-TOOLS/`.\n"
            f"- The header, source index and Archivist prompt are the run's shared inputs: `../01_FRAME/`.\n"))
        for folder, (purpose, inputs, outputs, verify, nxt, notest) in README_TEXT.items():
            if not (root / folder).exists():
                continue
            stages = [s.name for s in STAGES if RUN_FOLDERS[s.folder] == folder]
            status = "; ".join(f"{n}: {st.get(n, {}).get('status', 'not started')}" for n in stages) or "n/a"
            atomic_write_text(root / folder / "README.md", (
                f"# {folder} - axis {a} only\n\n## Purpose\n{purpose}\n\n## Allowed inputs\n{inputs}\n\n"
                f"## Expected outputs\n{outputs}\n\n## Current status\n{status}\n\n## How to verify this stage\n"
                f"{verify}\n\n## Next handoff\n{nxt}\n\n## What this stage does not establish\n{notest}\n"))
        lines.append(f"- **{a}: {ax.get('name') or root.name.split('__')[-1].replace('-', ' ')}** - [{root.name}/AXIS.md]({root.name}/AXIS.md) · "
                     f"[report]({root.name}/10_REPORTS/CRUX-REPORT.md) · "
                     f"[premise ledger]({root.name}/08_COVERAGE/PREMISE-LEDGER.md) · "
                     f"[audit browser]({root.name}/10_REPORTS/report.html)")
    sh = ctx.axis_dir(SHARED_FOLDER)
    if sh.exists():
        cross = sorted(p.name for p in sh.glob("CROSS-AXIS-into-*"))
        atomic_write_text(sh / "README.md", (
            f"# SHARED - records that belong to more than one axis\n\n"
            f"Nothing here is a question: every question is asked for exactly one axis and is kept, with its "
            f"answer, FRDs and witnesses, in that axis's own folder.\n\n"
            f"- `02_DISCOVERY/` - the Manager's quest state, assessment checkpoints, feedback packets and closeout. "
            f"One quest serves every axis, so these cover all of them.\n"
            f"- `04_LANGUAGE-TOOLS/` - the custom dictionary and canonicalizer rulebook. They are tools, not "
            f"evidence: one vocabulary serves every axis, and no assessment is run on them.\n"
            f"- `CROSS-AXIS-into-<axis>/07_MATCHING/` - relations between the OTHER axes' witnesses and that axis's "
            f"units: evidence found while asking about one axis that bears on another."
            f"{' Present: ' + ', '.join(cross) + '.' if cross else ' None recorded.'}\n"))
        lines.append(f"- **SHARED** (records that belong to more than one axis) - [{SHARED_FOLDER}/README.md]({SHARED_FOLDER}/README.md)")
    return "\n".join(lines)


def write_question_db(ctx: RunContext) -> str:
    """QUESTIONS.md at the top of the run: every question asked, the sources it named and what it
    yielded.  Returns the line RUN-MAP.md and RUN-STATUS.md point to it with ("" before any question)."""
    try:
        from .question_db import QUESTIONS_MD, write_question_database
        db = write_question_database(ctx.run_dir, ctx.run_id)
    except Exception as e:                # navigation must never stop a run
        ctx.log(f"   question database not written: {e}")
        return ""
    if not db:
        return ""
    return (f"[{QUESTIONS_MD}]({QUESTIONS_MD}): all {db['totals']['questions']} questions this run asked, the sources "
            f"they named and what each yielded. Give it and `01_FRAME/index.md` to another model to check whether "
            f"the questioning was thorough enough")


def write_navigation(ctx: RunContext) -> None:
    st = ctx.stage_state()
    qdb = write_question_db(ctx)
    qdb_line = f"- {qdb}\n" if qdb else ""
    qdb_line += ("- [Frame certificate](01_FRAME/FRAME-CERTIFICATE.md): what the signer typed, read and accepted "
                 "before this run\n" if ctx.p("frame", "FRAME-CERTIFICATE.md").exists()
                 else "- Frame certificate: none. Nobody signed the frame of this run.\n")
    axis_lines = None
    if ctx.axis_layout:
        try:
            axis_lines = write_axis_navigation(ctx, st)
        except FileNotFoundError:        # the frame is not frozen yet: there are no axis folders to describe
            axis_lines = ""
    for folder, (purpose, inputs, outputs, verify, nxt, notest) in README_TEXT.items():
        if axis_lines is not None and folder != "01_FRAME":
            continue
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
        if axis_lines is not None and isinstance(summ, dict) and summ and all(isinstance(v, dict) for v in summ.values()):
            # a per-axis stage: one short line per axis database
            short = "<br>".join(f"**{a}** " + ", ".join(f"{k}={v}" for k, v in list(s.items())[:4])[:150]
                                for a, s in summ.items())
        nxt = ""
        if not next_set and stat not in ("done", "imported"):
            nxt = {"waiting": "answer queued requests, then `cr queue import` and `cr run`",
                   "error": "read the error in 00_RUN-CONTROL/stage-state.json, fix, rerun",
                   "budget": "raise the budget in project.json, rerun",
                   "partial": "some model calls failed; `cr run` asks them again"}.get(stat, "`cr run`")
            next_set = True
        rows.append(f"| {s.name} | {stat} | {short[:160] if '<br>' not in short else short} | {nxt} |")
    halt = gate_state(ctx)
    banner = (f"**Halted for researcher decision** after `{halt['gate']}`. Read `{halt['read']}`, then continue with "
              f"`{halt['continue_with']}`\n\n") if halt else ""
    atomic_write_text(ctx.run_dir / "RUN-STATUS.md",
                      f"# RUN-STATUS — {ctx.run_id}\n\nUpdated {utcnow()}\n\n" + banner
                      + (f"Question database: {qdb}.\n\n" if qdb else "") + "\n".join(rows) + "\n")
    if axis_lines is not None:
        atomic_write_text(ctx.run_dir / "RUN-MAP.md", (
            f"# RUN-MAP - {ctx.run_id}\n\n"
            f"This run keeps **one evidence database per axis**. Each axis folder holds only that axis's questions, "
            f"answers, FRDs, validated FRDs, witnesses, units, match records, coverage, crux and reports. "
            f"No file holds two axes; records that belong to more than one axis are in SHARED.\n\n"
            f"## The databases\n\n{axis_lines or '(made when the frame is frozen)'}\n\n## The run\n\n"
            f"- [RUN-STATUS.md](RUN-STATUS.md)\n{qdb_line}- [RUN-CONFIG.json](RUN-CONFIG.json)\n- [FRD-EVALUATION.md](FRD-EVALUATION.md): preliminary ACH_Eval on the validated FRDs, per axis and combined\n"
            f"- [01_FRAME](01_FRAME/README.md) - the approved header, source index and Archivist prompt (shared inputs)\n"
            f"- [Model call log](00_RUN-CONTROL/model-and-human-decisions/llm-calls.jsonl)\n"
            f"- [Artifact registry](00_RUN-CONTROL/artifact-registry.jsonl)\n"))
        return
    links = "\n".join(f"- [{f}]({f}/README.md)" for f in README_TEXT)
    atomic_write_text(ctx.run_dir / "RUN-MAP.md",
                      f"# RUN-MAP — {ctx.run_id}\n\n- [RUN-STATUS.md](RUN-STATUS.md)\n{qdb_line}- [RUN-CONFIG.json](RUN-CONFIG.json)\n- [FRD-EVALUATION.md](FRD-EVALUATION.md): preliminary ACH_Eval on the validated FRDs, per axis and combined\n"
                      f"- [Crux report](10_REPORTS/CRUX-REPORT.md) · [Audit browser](10_REPORTS/report.html)\n{links}\n"
                      f"- [Model call log](00_RUN-CONTROL/model-and-human-decisions/llm-calls.jsonl)\n"
                      f"- [Artifact registry](00_RUN-CONTROL/artifact-registry.jsonl)\n")
