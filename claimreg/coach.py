"""The coach between rounds: where the researcher stands, why, and what the next move is.

The frame session (`cr sign`, frame_gate.py) is the talk before the fight.  This module is the
corner between rounds.  At two points a run scores the evidence against the hypothesis the
researcher wants to win:

1. after the quest, on the notebook's answers (cheap, early, provisional);
2. after the findings are validated, on the validated FRDs (three scorings, averaged, because one
   scoring moves by several units on its own).

When the hypothesis is short of its target the run stops there, and the coach writes a corner
talk: why it came in low, what the evidence does support, weaker claims the same evidence covers
(each against a rival someone really holds), and what to ask the corpus next.  Nothing here says
"give up".  The researcher runs in good faith and may know things the published record does not.

`cr rescore` scores a run's validated findings under a different header for a dollar or two: the
corpus, the questions, the answers and the validated findings are the expensive part, and they are
built once.  Every frame tried and its score is kept in ``01_FRAME/FRAME-LADDER.md``, so the result
is the ladder: the strongest claim this evidence supports, shown beside the stronger ones it does not.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from . import frame_gate
from .util import atomic_write_text, read_json, read_text, sha256_text, utcnow, write_json

LADDER_JSON = "FRAME-LADDER.json"
LADDER_MD = "FRAME-LADDER.md"
DEFAULTS = {"enabled": True, "target_share": frame_gate.TARGET_SHARE, "times": 3, "require_acceptance": True,
            "preferred": {}}
NOISE = 2                     # a mean this many units under the target is too close to call
HOLD_BEFORE = {"frd_generate": 1, "language": 2}      # the stage a checkpoint is decided in front of
BASIS = {1: "the quest's answers (not yet validated)", 2: "the validated findings"}


def settings(cfg: dict) -> dict:
    return {**DEFAULTS, **(cfg.get("coach") or {})}


def preferred(project: Path, cfg: dict) -> dict[str, str]:
    """{axis id: the hypothesis the researcher wants to win}, from the frame session, or from
    coach.preferred in project.json where there has been no session."""
    out = {str(a).upper(): str(h) for a, h in (settings(cfg).get("preferred") or {}).items()}
    out.update({a: r["preferred"] for a, r in ((frame_gate.load_certificate(project) or {}).get("axes") or {}).items()
                if r.get("preferred")})                 # what the researcher chose in the session wins
    return out


def about(project: Path, axis_id: str) -> dict:
    """What the researcher told the coach in the frame session."""
    cert = frame_gate.load_certificate(project) or {}
    r = (cert.get("axes") or {}).get(axis_id) or {}
    text = lambda k: (r.get(k) or {}).get("text", "")
    return {**(cert.get("who") or {}), "experience": text("experience"), "intent": text("intent"), "concede": text("concede")}


def target_units(cfg: dict, gauge: int) -> int:
    return math.ceil(float(settings(cfg)["target_share"]) * gauge)


def _key(axis: dict) -> str:
    """A short name for one wording of an axis, so that scorings of different wordings are kept apart."""
    return sha256_text(frame_gate.canonical_json(frame_gate._wording(axis)))[:8]


# --------------------------------------------------------------------------- #
# Evidence and scoring.

def frd_rows(ctx, axis_id: str) -> list[dict]:
    from .frd_assess import REL_RETAINED, _rows, citable, frd_id
    sc = ctx.for_axis(axis_id) if ctx.axis_layout else ctx
    rows, _ = citable(ctx, _rows(sc, REL_RETAINED))
    return sorted(rows, key=frd_id)


def answer_rows(ctx, axis_id: str) -> list[dict]:
    rel = "02_query-responses/responses.json"
    sc = ctx.for_axis(axis_id) if ctx.axis_layout else ctx
    rs = sc.load("discovery", rel, default=None) or ctx.discovery_ctx().load("discovery", rel, default=[]) or []
    return [{"frd_id": str(r.get("qid")), "source_file": "; ".join(r.get("cited_sources") or []) or "-",
             "verdict": "unvalidated answer", "claim": r.get("text", "")}
            for r in rs if isinstance(r, dict) and r.get("usable", True) and str(r.get("text", "")).strip()]


def score(ctx, axis: dict, rows: list[dict], out_dir: Path, times: int, evidence: str, label: str,
          gauge: int | None = None) -> dict:
    """Score `rows` against one axis `times` times.  Returns the vectors, their mean and what the
    assessments said."""
    from .frd_assess import _Job
    gauge = int(gauge or ctx.frame.get("gauge") or ctx.cfg["quest"].get("gauge", 64))
    words = int((ctx.cfg.get("frd_assess", {}) or {}).get("partition_words", 30000))
    ids = [h["id"] for h in axis["hypotheses"]]
    jobs = [_Job(ctx, axis, rows, "axis-only", Path(out_dir) / f"scoring-{n}", gauge, words,
                 label=f"{label}-{n}", evidence=evidence) for n in range(1, times + 1)] if rows else []
    reqs = [(j, r) for j in jobs for r in j.partition_requests()]
    resp = ctx.llm.call_many([r for _, r in reqs]) if reqs else []
    pos = 0
    for j in jobs:
        j.take_partitions(resp[pos:pos + len(j.parts)])
        pos += len(j.parts)
    syn = [(j, j.synthesis_request()) for j in jobs]
    syn = [(j, r) for j, r in syn if r is not None]
    syn_resp = dict(zip([id(j) for j, _ in syn], ctx.llm.call_many([r for _, r in syn]) if syn else []))
    recs = [j.finish(syn_resp.get(id(j))) for j in jobs]
    return summarize([r for r in recs if r.get("allocations")], ids, gauge,
                     problems=[p for r in recs for p in r.get("problems", [])], rows=len(rows))


def summarize(recs: list[dict], ids: list[str], gauge: int, problems=(), rows: int = 0) -> dict:
    from .frd_assess import largest_remainder
    vectors = [{i: int(r["allocations"].get(i, 0)) for i in ids} for r in recs]
    return {"vectors": vectors, "rows": rows, "problems": list(problems),
            "mean": largest_remainder({i: sum(v[i] for v in vectors) for i in ids}, gauge) if vectors else None,
            "said": [{"strongest_objection": r.get("strongest_objection", ""), "reversal_finding": r.get("reversal_finding", ""),
                      "drivers": [{k: d.get(k) for k in ("frd_id", "favors", "why", "source_file")}
                                  for d in (r.get("drivers") or [])[:25]]} for r in recs]}


def standing(vectors: list[dict], mean: dict | None, pref: str, target: int) -> str:
    if not mean:
        return "no score"
    if mean[pref] >= target:
        return "at target"
    return "within noise of target" if target - mean[pref] <= NOISE else "below target"


# --------------------------------------------------------------------------- #
# The ladder: every frame tried and how it scored.

def ladder_add(project: Path, entry: dict) -> None:
    """Every scoring is kept; nothing is replaced."""
    path = Path(project) / "01_FRAME" / LADDER_JSON
    log = (read_json(path, default=[]) or []) + [entry]
    write_json(path, log)
    atomic_write_text(Path(project) / "01_FRAME" / LADDER_MD, ladder_render(log))


def ladder_render(log: list[dict]) -> str:
    out = ["# Frame ladder", "",
           "Every frame that has been scored against this project's evidence, and how it scored. The result of an "
           "investigation is the ladder: the claims the evidence supports, shown beside the stronger claims it does "
           "not support.", "",
           "- Scores are units of a gauge divided among the hypotheses. They are not probabilities.",
           "- One scoring moves by several units on its own, so each scoring is listed.",
           "- The target is a guide for the researcher, not a pass mark.",
           "- Scores can be compared only within one run and one kind of evidence. Findings-level and final "
           "(witness-level) scores of the same run differ by several units.", ""]
    cell = lambda t: " ".join(str(t).split()).replace("|", "\\|")
    for axis in sorted({e["axis"] for e in log}):
        rows = [e for e in log if e["axis"] == axis]
        out += [f"## Axis {axis}", "", "| When | Run | Scored on | The claim (hypothesis the researcher wants) | Score | Each scoring | Standing |",
                "|---|---|---|---|---|---|---|"]
        for e in rows:
            pref = e.get("preferred", "")
            mean = e.get("mean") or {}
            out.append(f"| {str(e.get('time', ''))[:16].replace('T', ' ')} | {e.get('run', '')} | {e.get('basis', '')} | "
                       f"{cell((e.get('statements') or {}).get(pref, ''))} | "
                       f"**{mean.get(pref, '-')}** of {e.get('gauge', 64)} ({', '.join(f'{k} {v}' for k, v in mean.items())}) | "
                       f"{', '.join(str(v.get(pref)) for v in e.get('vectors', []))} | {e.get('standing', '')} |")
        out.append("")
        # one line per run and kind of evidence: which claims reached the target and which fell short
        latest: dict = {}
        for e in rows:
            if e.get("mean"):
                latest[(e.get("run"), e.get("basis"), e.get("frame_key"))] = e
        groups: dict = {}
        for (run, basis, _), e in latest.items():
            groups.setdefault((run, basis), []).append(e)
        for (run, basis), es in groups.items():
            if len(es) < 2:
                continue
            say = lambda e: f"\"{cell(e['statements'].get(e['preferred'], ''))}\" ({e['mean'][e['preferred']]})"
            up = [say(e) for e in es if e["standing"] != "below target"]
            down = [say(e) for e in es if e["standing"] == "below target"]
            out.append(f"On {run}, scored on {basis}: " + ("at or near target: " + "; ".join(up) + ". " if up else
                       "no claim reached the target. ") + ("Fell short: " + "; ".join(down) + "." if down else ""))
            out.append("")
    return "\n".join(out) + "\n"


def _entry(ctx_run: str, axis: dict, pref: str, gauge: int, target: int, basis: str, res: dict, note: str = "") -> dict:
    w = frame_gate._wording(axis)
    return {"time": utcnow(), "run": ctx_run, "axis": axis["axis_id"], "frame_key": _key(axis), "basis": basis,
            "question": w["question"], "statements": w["statements"], "preferred": pref, "gauge": gauge,
            "target": target, "vectors": res["vectors"], "mean": res["mean"],
            "standing": standing(res["vectors"], res["mean"], pref, target), "note": note}


# --------------------------------------------------------------------------- #
# The corner talk.

def _ask(ctx):
    from .llm.base import LLMRequest

    def ask(tag: str, system: str, user: str, salt: str = "") -> dict:
        resp = ctx.llm.call(LLMRequest(role=frame_gate.ROLE, system=system, user=user, expect_json=True,
                                       tag=f"coach:{tag}", salt=salt))
        if not isinstance(resp.parsed, dict):
            raise ValueError(resp.parse_error or "the answer was not a JSON object")
        return resp.parsed
    return ask


def _questions_asked(ctx, cap: int = 12_000) -> str:
    db = read_json(ctx.run_dir / "QUESTIONS.json", default={}) or {}
    rows = db.get("questions") or []
    return "\n".join(f"- {q.get('qid')}: " + " ".join(str(q.get("text", "")).split())[:260] for q in rows)[:cap]


def corner_talk(model, who: dict, axis: dict, pref: str, gauge: int, target: int, res: dict, basis: str,
                evidence: str, asked: str) -> dict:
    """Why the hypothesis came in low, what the evidence does support, weaker claims it covers, and
    what to ask next.  Each part degrades to empty when the model cannot be reached."""
    w = frame_gate._wording(axis)
    mean = res["mean"] or {}
    result = (f"Scored on {basis}. Units of {gauge}: " + ", ".join(f"{k} {v}" for k, v in mean.items()) +
              f". Each scoring gave {pref}: " + ", ".join(str(v[pref]) for v in res["vectors"]) +
              f". The researcher's target for {pref} is {target}.")
    said = "\n".join(f"- strongest objection: {s['strongest_objection']}\n- what would reverse it: {s['reversal_finding']}\n"
                     + "\n".join(f"- driver {d['frd_id']} ({d.get('source_file') or '-'}) favours {d['favors']}: "
                                 f"{' '.join(str(d['why']).split())[:240]}" for d in s["drivers"][:14])
                     for s in res["said"][:2])
    user = (frame_gate._own(who) + f"\nTHE HYPOTHESIS THEY WANT TO WIN: {pref}\n\nTHE FRAME\n"
            + frame_gate._frame_text(w["question"], w["statements"]) + "\n\nTHE RESULT\n" + result
            + "\n\nWHAT THE ASSESSMENT SAID\n" + (said or "(nothing recorded)")
            + "\n\nEVIDENCE THE RUN HOLDS\n" + (evidence or "(none supplied)")
            + "\n\nQUESTIONS ALREADY PUT TO THE CORPUS\n" + (asked or "(not recorded)")
            + "\n\nTASK: this is the talk in the corner between rounds. The researcher's hypothesis came in under "
            "their target. Tell them, plainly and without discouragement: which parts of their claim the evidence "
            "did not cover (be specific: which population, comparison or outcome is missing); what the evidence "
            "DOES show that is on their side; how their own experience fits with that (for example, why people like "
            "them may differ from the people studied); and which questions to put to the corpus next that nobody has "
            "asked yet and that could cover the gap. Do not tell them to stop. "
            'Return {"why_it_came_in_low": ["..."], "not_covered": ["the part of the claim, and what evidence would '
            'cover it"], "on_your_side": ["what the evidence does show for them"], "your_experience": "one or two '
            'sentences", "ask_next": ["a question to put to the corpus, naming the source or kind of study"]}.')
    strs = lambda v, n=8: [" ".join(str(x).split()) for x in (v or []) if str(x).strip()][:n]
    out = {"result": result, "why_it_came_in_low": [], "not_covered": [], "on_your_side": [], "your_experience": "",
           "ask_next": [], "openings": [], "steps": {}}
    try:
        got = model("corner", frame_gate.SYSTEM, user, "")
        out.update({k: strs(got.get(k)) for k in ("why_it_came_in_low", "not_covered", "on_your_side", "ask_next")})
        out["your_experience"] = " ".join(str(got.get("your_experience", "")).split())
        out["steps"]["corner"] = "ok"
    except Exception as e:
        out["steps"]["corner"] = f"failed: {type(e).__name__}: {e}"[:300]
    try:
        out["openings"] = frame_gate.ladder(model, who, pref, w["question"], w["statements"], evidence,
                                            tag="openings", result=result + "\n" + said)
        out["steps"]["openings"] = "ok"
    except Exception as e:
        out["steps"]["openings"] = f"failed: {type(e).__name__}: {e}"[:300]
    return out


def render_checkpoint(ctx, n: int, rec: dict) -> str:
    proj, run = ctx.project_dir, ctx.run_id
    out = [f"# Coach checkpoint {n}: where you stand after " + ("the quest" if n == 1 else "the findings were validated"), "",
           f"Scored on {BASIS[n]}. Scores are units of the gauge divided among the hypotheses. They are not "
           "probabilities, and one scoring moves by several units on its own. The target is a guide for you, not a pass mark."
           + (" This early reading is provisional: nothing has been checked against the sources yet." if n == 1 else
              " This is the findings-level score. The final score is made later, from the witnesses, and can differ from "
              "this one by several units; the frame ladder shows both once the run is finished."), ""]
    for aid, a in rec["axes"].items():
        pref, mean = a["preferred"], a.get("mean") or {}
        out += [f"## Axis {aid}", "",
                f"**{pref}: {mean.get(pref, '-')} of {a['gauge']}** (target {a['target']}). Standing: **{a['standing']}**.",
                "", "All hypotheses: " + ", ".join(f"{k} {v}" for k, v in mean.items()) + ". Each scoring gave "
                + pref + ": " + ", ".join(str(v[pref]) for v in a.get("vectors", [])) + ".", "",
                f"Your claim: {a['statements'].get(pref, '')}", ""]
        if a["standing"] == "at target":
            out += ["You are where you wanted to be. Nothing to change.", ""]
            continue
        if a["standing"] == "within noise of target":
            out += [f"The mean is within {NOISE} units of your target, and one scoring moves by more than that on its own. "
                    "This is too close to call. You can go on as you are.", ""]
        t = a.get("talk") or {}
        if a["standing"] == "no score":
            out += ["No score could be made: " + "; ".join(a.get("problems") or ["no evidence was found for this axis"]), ""]
            continue
        sect = lambda title, items: ([f"### {title}", ""] + [f"- {x}" for x in items] + [""]) if items else []
        out += sect("Why it came in low", t.get("why_it_came_in_low"))
        out += sect("What the evidence did not cover", t.get("not_covered"))
        out += sect("What the evidence does show for you", t.get("on_your_side"))
        if t.get("your_experience"):
            out += ["### Your own experience", "", t["your_experience"], ""]
        if t.get("openings"):
            out += ["### Openings: claims this evidence is more likely to support", "",
                    "Listed from the strongest claim to the weakest. Each is tested against a rival that someone really holds.", ""]
            for k, r in enumerate(t["openings"], 1):
                out += [f"**{k}. {r['label']}**", "", f"- Question: {r['question']}"]
                out += [f"- {h}: {s}" for h, s in r["statements"].items()]
                out += [f"- The rival is held by: {r['rival_held_by']}", f"- A win lets you say: {r['win_lets_you_say']}",
                        f"- It gives up: {r['leaves_out']}", ""]
        out += sect("Questions to put to the corpus next", t.get("ask_next"))
        bad = {k: v for k, v in (t.get("steps") or {}).items() if v != "ok"}
        out += [f"(The model could not do the `{k}` part: {v})" for k, v in bad.items()] + ([""] if bad else [])
    if rec["hold"]:
        out += ["## Your next move", "",
                "The run has stopped here so that you can choose. Nothing is lost: the corpus, the questions, the "
                "answers" + (" and the validated findings" if n == 2 else "") + " stay as they are.", "",
                f"- **Take an opening.** Go through that axis with the coach again and type the new claim "
                f"(`cr sign \"{proj}\" --axis <AXIS>`), then score "
                + ("the same findings under it for a dollar or two " if n == 2 else "the same answers under it ")
                + f"(`cr rescore \"{proj}\" --run {run}" + (" --answers" if n == 1 else "") + "`). "
                "The earlier claim and its score stay on the ladder.",
                "- **Ask more.** Put the questions above to the corpus, import the answers, and run again."
                if n == 1 else
                "- **Ask more.** Put the questions above to the corpus in a further quest round; new answers become new findings.",
                f"- **Go on as you are.** `cr run \"{proj}\" --run {run} --continue`. A result below target is still a "
                "result: it says which claim this evidence does not support.", "",
                f"Every frame scored so far: `{Path('01_FRAME') / LADDER_MD}` in the project folder.", ""]
    return "\n".join(x for x in out if x is not None) + "\n"


# --------------------------------------------------------------------------- #
# The two checkpoints.

def _record_path(ctx, n: int) -> Path:
    return ctx.p("control", "model-and-human-decisions") / f"coach-checkpoint-{n}.json"


def checkpoint(ctx, n: int, model=None, scorer=None) -> dict | None:
    """Score the evidence for every axis whose preferred hypothesis is known, write the corner talk,
    and say whether the run should stop for the researcher.  None when the coach has nothing to do."""
    st = settings(ctx.cfg)
    if not st["enabled"]:
        return None
    prefs = preferred(ctx.project_dir, ctx.cfg)
    axes = [a for a in ctx.frame["axes"] if prefs.get(a["axis_id"]) in [h["id"] for h in a["hypotheses"]]]
    if ctx.axis_layout:
        axes = [a for a in axes if a["axis_id"] in ctx.axis_ids()]
    if not axes:
        return None
    model, scorer = model or _ask(ctx), scorer or score
    gauge = int(ctx.frame.get("gauge") or ctx.cfg["quest"].get("gauge", 64))
    target = target_units(ctx.cfg, gauge)
    out_base = ctx.p("control", "model-and-human-decisions") / f"coach-checkpoint-{n}"
    stage = (read_json(ctx.run_dir / "frd-evaluation.json", default={}) or {}).get("results", {}) if n == 2 else {}
    rec = {"checkpoint": n, "time": utcnow(), "target": target, "gauge": gauge, "axes": {}, "released": None}
    for ax in axes:
        aid, pref = ax["axis_id"], prefs[ax["axis_id"]]
        ids = [h["id"] for h in ax["hypotheses"]]
        rows = answer_rows(ctx, aid) if n == 1 else frd_rows(ctx, aid)
        label = f"coach{n}-{_key(ax)}"
        if n == 1:
            res = scorer(ctx, ax, rows, out_base / aid, 1, "answers", label)
        else:
            own = (stage.get(aid) or {}).get("axis-only") or (stage.get(aid) or {}).get("combined") or {}
            first = [own] if own.get("allocations") else []
            res = summarize(first, ids, gauge, rows=len(rows))
            more = max(0, int(st["times"]) - len(first))
            if more and not (first and res["mean"][pref] >= target):       # at target on the first scoring: no need
                extra = scorer(ctx, ax, rows, out_base / aid, more, "frds", label)
                res = {**extra, "vectors": res["vectors"] + extra["vectors"], "said": res["said"] + extra["said"]}
                from .frd_assess import largest_remainder
                res["mean"] = largest_remainder({i: sum(v[i] for v in res["vectors"]) for i in ids}, gauge) if res["vectors"] else None
        entry = _entry(ctx.run_id, ax, pref, gauge, target, BASIS[n], res)
        a = {k: entry[k] for k in ("preferred", "gauge", "target", "vectors", "mean", "standing", "statements", "question")}
        a["problems"] = res.get("problems", [])
        if a["standing"] in ("below target", "within noise of target"):
            evidence = "\n".join(f"- [{r['source_file']}] " + " ".join(str(r["claim"]).split())[:300] for r in rows)[:60_000]
            a["talk"] = corner_talk(model, about(ctx.project_dir, aid), ax, pref, gauge, target, res, BASIS[n],
                                    evidence, _questions_asked(ctx))
        rec["axes"][aid] = a
        if res["vectors"]:
            ladder_add(ctx.project_dir, entry)
    rec["hold"] = any(a["standing"] == "below target" for a in rec["axes"].values())
    write_json(_record_path(ctx, n), rec)
    atomic_write_text(ctx.run_dir / f"COACH-CHECKPOINT-{n}.md", render_checkpoint(ctx, n, rec))
    ctx.log(f"   coach checkpoint {n}: " + "; ".join(
        f"{aid} {a['preferred']} {(a.get('mean') or {}).get(a['preferred'], '-')} of {gauge} ({a['standing']})"
        for aid, a in rec["axes"].items()))
    return rec


def hold_before(ctx, stage: str) -> dict | None:
    """Called in front of the stage that follows a checkpoint.  Runs checkpoint 1 if it has not been
    run.  Returns a halt record while the researcher has a decision to make there."""
    n = HOLD_BEFORE.get(stage)
    if not n or not settings(ctx.cfg)["enabled"]:
        return None
    rec = read_json(_record_path(ctx, n), default=None)
    if rec is None and n == 1:
        try:
            rec = checkpoint(ctx, 1)
        except Exception as e:  # noqa: BLE001 - the coach never stops a run by failing
            ctx.log(f"   coach checkpoint 1 could not be made ({type(e).__name__}: {e}); going on without it")
            return None
    if not rec or not rec.get("hold") or rec.get("released"):
        return None
    return {"gate": "the quest" if n == 1 else "frd_assess", "next_stage": stage, "read": f"COACH-CHECKPOINT-{n}.md",
            "continue_with": f'cr run "{ctx.project_dir}" --run {ctx.run_id} --continue'}


def release(ctx) -> None:
    """`cr run --continue`: the researcher has read the corner talk and wants to go on."""
    for n in (1, 2):
        rec = read_json(_record_path(ctx, n), default=None)
        if rec and rec.get("hold") and not rec.get("released"):
            rec["released"] = utcnow()
            write_json(_record_path(ctx, n), rec)
            ctx.log(f"coach checkpoint {n}: the researcher chose to go on as they are")


# --------------------------------------------------------------------------- #
# cr rescore

def record_final(ctx) -> None:
    """After the final assessment: put the witness-level score on the ladder beside the findings-level one."""
    prefs = preferred(ctx.project_dir, ctx.cfg)
    for sc in ctx.scopes():
        data = sc.load("reports", "assessment.json", default={}) or {}
        gauge = int(data.get("gauge") or ctx.frame.get("gauge") or 64)
        for ax in ctx.frame["axes"]:
            ids = [h["id"] for h in ax["hypotheses"]]
            vec = (data.get("allocations") or {}).get(ax["axis_id"])
            pref = prefs.get(ax["axis_id"])
            if not isinstance(vec, dict) or pref not in ids or getattr(sc, "axis_id", ax["axis_id"]) != ax["axis_id"]:
                continue
            res = summarize([{"allocations": vec}], ids, gauge)
            ladder_add(ctx.project_dir, _entry(ctx.run_id, ax, pref, gauge, target_units(ctx.cfg, gauge),
                                               "the witnesses (final assessment)", res))


def question_check(model, ctx, axis: dict, pref: str) -> dict:
    """What a new claim needs from the corpus that the quest never asked about.  Advice, not a gate."""
    w = frame_gate._wording(axis)
    user = ("THE NEW CLAIM\n" + frame_gate._frame_text(w["question"], w["statements"]) + f"\nThe researcher wants {pref} to win."
            "\n\nQUESTIONS ALREADY PUT TO THE CORPUS (they were written for an earlier wording of this axis)\n"
            + (_questions_asked(ctx) or "(not recorded)") + "\n\nSOURCE INDEX\n"
            + (frame_gate.index_digest(ctx.project_dir, axis["axis_id"], cap=40_000) or "(none)") +
            "\n\nTASK: the questions above were aimed at an earlier claim. List what this new claim needs evidence on, "
            "say for each whether a question already asked covers it, and write the questions still to ask, each "
            'naming the source or kind of study to ask about. Return {"needs": [{"evidence_on": "...", "covered_by": '
            '"question ids, or the words: not asked"}], "ask_next": ["..."]}.')
    got = model("question-check", frame_gate.SYSTEM, user, "")
    flat = lambda t: " ".join(str(t).split())
    return {"needs": [{"evidence_on": flat(n.get("evidence_on", "")), "covered_by": flat(n.get("covered_by", ""))}
                      for n in (got.get("needs") or []) if isinstance(n, dict) and flat(n.get("evidence_on", ""))][:12],
            "ask_next": [flat(x) for x in (got.get("ask_next") or []) if flat(x)][:12]}


def rescore(ctx, header: Path | None = None, axis: str | None = None, answers: bool = False,
            times: int | None = None, scorer=None, model=None) -> list[dict]:
    """Score this run's evidence under the project's header as it reads now (or another header file).
    Nothing in the run is changed; the scores go on the ladder.  Where the claim is not the one the
    run's questions were written for, `model` is asked what the new claim still needs."""
    from .header import normalize_hypothesis_ids, parse_header
    src = Path(header) if header else frame_gate.header_path(ctx.project_dir)
    text, _ = normalize_hypothesis_ids(frame_gate._norm(read_text(src)))
    frame = parse_header(text)
    prefs = preferred(ctx.project_dir, ctx.cfg)
    gauge = int(frame.get("gauge") or ctx.frame.get("gauge") or ctx.cfg["quest"].get("gauge", 64))    # the header's own gauge
    target = target_units(ctx.cfg, gauge)
    have = set(ctx.axis_ids()) if ctx.axis_layout else {a["axis_id"] for a in frame["axes"]}
    ran_on = {a["axis_id"]: _key(a) for a in ctx.frame["axes"]}
    out = []
    for ax in frame["axes"]:
        aid = ax["axis_id"]
        if (axis and aid != axis.upper()) or aid not in have:
            continue
        ids = [h["id"] for h in ax["hypotheses"]]
        warning = ""
        if prefs.get(aid) in ids:
            pref = prefs[aid]
        else:
            pref = ids[0]
            warning = (f"the coach does not know which hypothesis of {aid} you want to win"
                       + (f" ({prefs[aid]} is not in this header)" if prefs.get(aid) else "")
                       + f"; reporting {pref}. Go through `cr sign`, or set coach.preferred in project.json")
        rows = answer_rows(ctx, aid) if answers else frd_rows(ctx, aid)
        if not rows and not axis:
            continue                                 # this run gathered nothing for that axis
        n = 1 if answers and not times else int(times or settings(ctx.cfg)["times"])
        res = (scorer or score)(ctx, ax, rows, ctx.p("control", "model-and-human-decisions") / "rescore" / f"{aid}-{_key(ax)}",
                                n, "answers" if answers else "frds", f"rescore-{_key(ax)}", gauge=gauge)
        entry = _entry(ctx.run_id, ax, pref, gauge, target, BASIS[1 if answers else 2], res,
                       note=f"cr rescore, header {src.name}")
        entry["rows"], entry["problems"], entry["warning"] = res.get("rows", len(rows)), res.get("problems", []), warning
        if res["vectors"]:
            ladder_add(ctx.project_dir, entry)
        if model and ran_on.get(aid) != _key(ax):    # a claim the quest's questions were not written for
            path = ctx.project_dir / "01_FRAME" / f"QUESTION-CHECK-{aid}.md"
            try:
                qc = question_check(model, ctx, ax, pref)
                atomic_write_text(path, "\n".join(
                    [f"# Question check for axis {aid}", "",
                     f"The questions of {ctx.run_id} were written for an earlier wording of this axis. This is what the "
                     "claim below needs from the corpus, and whether anyone asked. It is advice: nothing waits on it.", "",
                     f"Claim ({pref}): {entry['statements'][pref]}", "", "| The claim needs evidence on | Covered by |", "|---|---|"]
                    + [f"| {n['evidence_on']} | {n['covered_by']} |" for n in qc["needs"]]
                    + ["", "## Questions still to ask", ""] + [f"- {q}" for q in qc["ask_next"]]) + "\n")
                entry["question_check"] = str(path)
            except Exception as e:  # noqa: BLE001 - advice only
                entry["question_check"] = f"not made ({type(e).__name__}: {e})"[:200]
        out.append(entry)
    return out


def cmd_rescore(a) -> int:
    from .runctx import RunContext
    ctx = RunContext(a.project, a.run)
    try:
        got = rescore(ctx, header=Path(a.header) if a.header else None, axis=a.axis, answers=a.answers, times=a.times,
                      model=_ask(ctx))
    except (ValueError, OSError) as e:
        print(f"rescore: {e}", file=sys.stderr)
        return 2
    if not got:
        print("rescore: this run holds no evidence for the axes of that header", file=sys.stderr)
        return 2
    for e in got:
        pref, mean = e["preferred"], e["mean"] or {}
        print(f"Axis {e['axis']}, scored on {e['basis']} ({e['rows']} rows) of {e['run']}:")
        if e.get("warning"):
            print(f"  NOTE: {e['warning']}")
        print(f"  claim ({pref}): {e['statements'][pref]}")
        if not mean:
            print("  no score: " + "; ".join(e["problems"] or ["no evidence for this axis"]))
            continue
        print(f"  {pref}: {mean[pref]} of {e['gauge']} (target {e['target']}; each scoring: "
              f"{', '.join(str(v[pref]) for v in e['vectors'])}).  All: " + ", ".join(f"{k} {v}" for k, v in mean.items()))
        print(f"  standing: {e['standing']}")
        if e.get("question_check"):
            print(f"  this claim is not the one the run's questions were written for. What it still needs: {e['question_check']}")
    print(f"\nEvery frame scored so far: {Path(a.project) / '01_FRAME' / LADDER_MD}")
    print("These are findings-level scores; the target is a guide, not a pass mark. To carry a new frame through "
          "witnesses and the final report, fork the run (`cr fork`) and run it.")
    return 0
