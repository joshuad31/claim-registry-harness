"""Axis databases: one evidence database per axis (docs/AXIS-DATABASES.md).

The rules this module enforces:

1. A question belongs to exactly one axis.  The Investigator chooses the axis when it writes the
   question; a question with no single axis is refused.  Questions are never shared.
2. Everything that descends from a question inherits its axis: the answer, the FRDs made from the
   answer, their validations, the witnesses.  Everything that descends from a hypothesis takes the
   hypothesis's axis: units, coverage, the premise ledger, crux, the assessment, the reports.
3. A record that joins two axes (a relation between one axis's witness and another axis's unit, the
   Manager's cross-axis quest state and feedback) lives in the SHARED database, never in an axis's.
4. No file under an axis folder holds material of another axis.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from .llm.base import LLMRequest
from .runctx import SHARED_FOLDER, AxisContext, RunContext
from .util import atomic_write_text, ensure_dir, read_json, write_json

AXIS_LABEL_RE = re.compile(r"\bA(\d+)\b")
RELS = {
    "witnesses": ("witnesses", "05_released/witnesses.json"),
    "relations": ("matching", "03_match-records/relations.json"),
    "units": ("matching", "01_hypothesis-units/units.json"),
    "qualification": ("matching", "02_match-fixtures/qualification.json"),
    "transcoded": ("transcoding", "transcoded.json"),
    "questions": ("discovery", "01_issued-questions/questions.json"),
    "responses": ("discovery", "02_query-responses/responses.json"),
}
# record lists an axis may read another axis's rows from, when one of that axis's witnesses bears
# on this axis's units: (folder key, file) -> the field that ties a row to a witness
FOREIGN_LISTS = {
    ("witnesses", "05_released/witnesses.json"): "witness_id",
    ("discovery", "01_issued-questions/questions.json"): "qid",
    ("discovery", "02_query-responses/responses.json"): "qid",
    ("frds", "01_candidates/candidates.json"): "frd_id",
    ("frds", "05_validated/validated-frds.json"): "frd_id",
    ("frds", "05_validated/retained-frds.json"): "frd_id",
}
def bears(row: dict) -> bool:
    """True when a relation says the witness covers, partly covers or contradicts the unit."""
    from .matching import COMPLETE, PARTIAL
    f = row.get("final")
    return f in COMPLETE or f in PARTIAL or f == "CONTRADICTS"


# --------------------------------------------------------------------------- #
# which axis a question belongs to
# --------------------------------------------------------------------------- #

def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z0-9-]{3,}", (text or "").lower())}


def axis_text(axis: dict, frame: dict) -> str:
    parts = [axis.get("name", ""), axis.get("question", ""), axis.get("scope", "")]
    for h in axis.get("hypotheses", []):
        parts += [h.get("title", ""), h.get("statement", ""), h.get("corroboration", ""), h.get("falsification", "")]
    for t in frame.get("decisive_tests", []):
        if axis["axis_id"] in AXIS_LABEL_RE.sub(lambda m: "A" + m.group(1), str(t.get("test", ""))).split():
            parts += [t.get("test", ""), t.get("question", "")]
    return " ".join(p for p in parts if p)


def labelled_axis(text: str, ids: list[str]) -> str | None:
    """The single axis a label such as 'A2 trial results' names, or None."""
    named = {"A" + n for n in AXIS_LABEL_RE.findall(text or "")} & set(ids)
    return next(iter(named)) if len(named) == 1 else None


def lexical_axis(frame: dict, text: str) -> str:
    """The axis whose own wording a question shares most with (words every axis uses do not count)."""
    axes = frame.get("axes", [])
    toks = {a["axis_id"]: _tokens(axis_text(a, frame)) for a in axes}
    common = set.intersection(*toks.values()) if len(toks) > 1 else set()
    q = _tokens(text)
    best, score = axes[0]["axis_id"], -1.0
    for a in axes:
        own = toks[a["axis_id"]] - common
        s = len(q & own) / (len(own) ** 0.5 or 1.0)
        if s > score:
            best, score = a["axis_id"], s
    return best


def assign_axes(ctx, questions: list[dict]) -> dict[str, dict]:
    """qid -> {"axis", "axis_source"} for every question.  Sources, best first: the Investigator's own
    choice; a single axis label in the question's stated target; a model's reading of the question
    against the axes (API providers only); shared wording."""
    frame = ctx.frame
    ids = [a["axis_id"] for a in frame.get("axes", [])]
    out: dict[str, dict] = {}
    todo: list[dict] = []
    for q in questions:
        if len(ids) == 1:
            out[q["qid"]] = {"axis": ids[0], "axis_source": "single-axis header"}
        elif q.get("axis") in ids:
            out[q["qid"]] = {"axis": q["axis"], "axis_source": q.get("axis_source") or "investigator"}
        elif labelled_axis(str(q.get("target") or ""), ids):
            out[q["qid"]] = {"axis": labelled_axis(str(q.get("target") or ""), ids), "axis_source": "target-label"}
        else:
            todo.append(q)
    if todo and ctx.llm.is_api_role("match_router"):
        axes_txt = "\n".join(f"{a['axis_id']}: {a.get('name') or ''} - {a.get('question', '')}" for a in frame["axes"])
        reqs = []
        for i in range(0, len(todo), 20):
            batch = todo[i:i + 20]
            listing = "\n".join(f"{q['qid']} | target: {q.get('target') or '(none)'} | {' '.join(str(q.get('text', '')).split())[:500]}"
                                for q in batch)
            system, user, _ = ctx.prompts.render("axis_route.md", AXES=axes_txt, QUESTIONS=listing)
            reqs.append(LLMRequest(role="match_router", system=system, user=user, tag=f"axis-route:{i // 20 + 1}",
                                   meta={"qids": [q["qid"] for q in batch]}))
        try:
            results = ctx.llm.call_many(reqs)
        except Exception as e:  # noqa: BLE001 - assignment must never stop a run; wording decides instead
            ctx.log(f"   axis assignment by model failed ({type(e).__name__}); using shared wording")
            results = []
        for res in results:
            rows = (res.parsed or {}).get("assignments") if res and isinstance(res.parsed, dict) else None
            for r in rows or []:
                if isinstance(r, dict) and r.get("axis") in ids and r.get("qid"):
                    out.setdefault(str(r["qid"]), {"axis": r["axis"], "axis_source": "assigned-after-the-fact (model)"})
    for q in todo:
        if q["qid"] not in out:
            out[q["qid"]] = {"axis": lexical_axis(frame, f"{q.get('target') or ''} {q.get('text', '')}"),
                             "axis_source": "assigned-after-the-fact (wording)"}
    return out


# --------------------------------------------------------------------------- #
# filing the quest's questions and answers into their axes
# --------------------------------------------------------------------------- #

def ensure_axis_folders(ctx: RunContext) -> None:
    for sc in ctx.scopes():
        ensure_dir(sc.root)
    ensure_dir(ctx.axis_dir(SHARED_FOLDER))


def partition_discovery(ctx: RunContext) -> dict:
    """Move every question and answer the quest left in SHARED into its own axis's database.

    The quest runs across axes (one Manager, one set of notebook lanes), so its working records are
    written together; a question and its answer are single-axis and are filed by axis as soon as the
    quest stage ends.  Afterwards SHARED/02_DISCOVERY holds only the Manager's cross-axis records."""
    if not ctx.axis_layout:
        return {}
    ensure_axis_folders(ctx)
    d = ctx.shared().p("discovery")
    qp = d / "01_issued-questions" / "questions.json"
    rp = d / "02_query-responses" / "responses.json"
    ap = d / "02_query-responses" / "attempts.json"
    counts: dict[str, dict] = {}
    if qp.exists():
        questions = read_json(qp, default=[]) or []
        responses = read_json(rp, default=[]) or []
        attempts = read_json(ap, default=[]) or []
        assign = assign_axes(ctx, questions)
        for sc in ctx.scopes():
            ax = sc.axis_id
            mine = {q["qid"] for q in questions if assign[q["qid"]]["axis"] == ax}
            ad = sc.p("discovery")
            ensure_dir(ad / "01_issued-questions")
            ensure_dir(ad / "02_query-responses")
            write_json(ad / "01_issued-questions" / "questions.json",
                       [{**q, **assign[q["qid"]]} for q in questions if q["qid"] in mine])
            write_json(ad / "02_query-responses" / "responses.json",
                       [{**r, "axis": ax} for r in responses if r.get("qid") in mine])
            write_json(ad / "02_query-responses" / "attempts.json",
                       [{**a, "axis": ax} for a in attempts if a.get("qid") in mine])
            for sub, suffix in (("01_issued-questions", "__issued-question.md"),
                                ("02_query-responses", "__query-response.md")):
                for qid in sorted(mine):
                    src = d / sub / f"{qid}{suffix}"
                    if src.exists():
                        text = src.read_text(encoding="utf-8")
                        atomic_write_text(ad / sub / src.name,
                                          text.replace("\n", f"\n\nAxis: {ax} ({assign[qid]['axis_source']})\n", 1))
                        src.unlink()
        for p in (qp, rp, ap):
            if p.exists():
                p.unlink()
        for sub in ("01_issued-questions", "02_query-responses"):
            if (d / sub).exists() and not any((d / sub).iterdir()):
                (d / sub).rmdir()
    for sc in ctx.scopes():
        qs = sc.load("discovery", "01_issued-questions/questions.json", default=[]) or []
        rs = sc.load("discovery", "02_query-responses/responses.json", default=[]) or []
        src: dict[str, int] = {}
        for q in qs:
            src[q.get("axis_source", "?")] = src.get(q.get("axis_source", "?"), 0) + 1
        counts[sc.axis_id] = {"questions": len(qs), "usable_answers": sum(1 for r in rs if r.get("usable")),
                              "axis_chosen_by": src}
    return counts


def reset_axis_discovery(ctx: RunContext, stamp: str) -> list[str]:
    """Move the axes' filed questions and answers aside when the quest is redone (never deleted)."""
    moved = []
    if not ctx.axis_layout:
        return moved
    try:
        scopes = ctx.scopes()
    except FileNotFoundError:
        return moved
    for sc in scopes:
        ad = sc.p("discovery")
        for sub in ("01_issued-questions", "02_query-responses"):
            src = ad / sub
            if src.exists() and any(src.iterdir()):
                dst = ad / "99_superseded" / stamp / sub
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                moved.append(f"{sc.axis_id}/{sub}")
    return moved


# --------------------------------------------------------------------------- #
# cross-axis evidence (the SHARED database)
# --------------------------------------------------------------------------- #

def cross_enabled(ctx) -> bool:
    return bool((ctx.cfg.get("axes") or {}).get("cross_axis_evidence", True))


def cross_dir(base: RunContext, axis_id: str) -> Path:
    return base.axis_dir(SHARED_FOLDER) / f"CROSS-AXIS-into-{axis_id}"


class CrossContext(AxisContext):
    """The matching pass that asks whether another axis's witnesses bear on this axis's units.

    Its witnesses are every released witness of the OTHER axes; its units are this axis's.  All it
    writes goes to SHARED/CROSS-AXIS-into-<axis>/, because a relation between two axes belongs to
    neither."""

    def p(self, folder_key: str, *parts: str) -> Path:
        from .runctx import RUN_FOLDERS
        if RUN_FOLDERS.get(folder_key, folder_key) == "07_MATCHING":
            b = cross_dir(self._base, self.axis_id) / "07_MATCHING"
            return b.joinpath(*parts) if parts else b
        return super().p(folder_key, *parts)

    def _own(self) -> AxisContext:
        return self._base.for_axis(self.axis_id)

    def load(self, folder_key: str, rel: str, default=None):
        own = self._own()
        if (folder_key, rel) == RELS["witnesses"]:
            return foreign_rows(self._base, self.axis_id, folder_key, rel)
        if (folder_key, rel) in (RELS["units"], RELS["qualification"]):
            return own.load(folder_key, rel, default)
        if (folder_key, rel) == RELS["transcoded"]:
            mine = own.load(folder_key, rel, default={}) or {}
            items = [i for i in mine.get("items", []) if i.get("type") != "WITNESS"]
            for o in other_axes(self._base, self.axis_id):
                tc = self._base.for_axis(o).load(folder_key, rel, default={}) or {}
                items += [{**i, "home_axis": o} for i in tc.get("items", []) if i.get("type") == "WITNESS"]
            return {**mine, "items": items}
        return read_json(self.p(folder_key, rel), default=default)

    def save(self, folder_key: str, rel: str, obj, kind: str | None = None, parents: list[str] | None = None) -> Path:
        path = self.p(folder_key, rel)
        write_json(path, obj)
        self._base.register(path, f"{SHARED_FOLDER}:into-{self.axis_id}:{kind or rel}", parents)
        return path


def other_axes(base: RunContext, axis_id: str) -> list[str]:
    return [a for a in base.axis_ids() if a != axis_id]


def foreign_rows(base: RunContext, axis_id: str, folder_key: str, rel: str, keep: set | None = None,
                 field: str | None = None) -> list[dict]:
    """Rows of the same record list in the other axes' databases, each marked with its home axis."""
    out = []
    for o in other_axes(base, axis_id):
        for row in base.for_axis(o).load(folder_key, rel, default=[]) or []:
            if keep is None or row.get(field) in keep:
                out.append({**row, "home_axis": o})
    return out


def cross_relations(base: RunContext, axis_id: str) -> list[dict]:
    return read_json(cross_dir(base, axis_id) / "07_MATCHING" / "03_match-records" / "relations.json", default=[]) or []


def foreign_refs(base: RunContext, axis_id: str) -> dict[str, set]:
    """The other-axis witnesses that bear on this axis's units, and the questions and FRDs behind them."""
    wids = {r["witness_id"] for r in cross_relations(base, axis_id) if bears(r)}
    refs = {"witness_id": wids, "qid": set(), "frd_id": set()}
    if wids:
        for w in foreign_rows(base, axis_id, *RELS["witnesses"], keep=wids, field="witness_id"):
            refs["qid"].add(w.get("qid"))
            refs["frd_id"].add(w.get("frd_id"))
    return refs


def merged_load(ax: AxisContext, folder_key: str, rel: str, default=None):
    """What a later stage of an axis reads: its own records plus the SHARED cross-axis evidence that
    bears on its units.  Rows that come from another axis carry "home_axis"."""
    own = read_json(ax.p(folder_key, rel), default=default)
    base = ax._base
    if (folder_key, rel) == RELS["relations"]:
        return list(own or []) + [{**r, "cross_axis": True} for r in cross_relations(base, ax.axis_id)]
    if (folder_key, rel) in FOREIGN_LISTS or (folder_key, rel) == RELS["transcoded"]:
        refs = foreign_refs(base, ax.axis_id)
        if not refs["witness_id"]:
            return own
        if (folder_key, rel) == RELS["transcoded"]:
            items = list((own or {}).get("items", []))
            for o in other_axes(base, ax.axis_id):
                tc = base.for_axis(o).load(folder_key, rel, default={}) or {}
                items += [{**i, "home_axis": o} for i in tc.get("items", [])
                          if i.get("type") == "WITNESS" and i.get("item_id") in refs["witness_id"]]
            return {**(own or {}), "items": items}
        field = FOREIGN_LISTS[(folder_key, rel)]
        return list(own or []) + foreign_rows(base, ax.axis_id, folder_key, rel, keep=refs[field], field=field)
    return own


def split_relations_on_save(ax: AxisContext, rows: list) -> list:
    """Keep an axis's relations file free of other axes' witnesses: rows that join a foreign witness
    to this axis's units are written back to SHARED, and only the axis's own rows are returned."""
    own_w = {w["witness_id"] for w in (read_json(ax.p(*RELS["witnesses"]), default=[]) or [])}
    mine, foreign = [], []
    for r in rows:
        (mine if r.get("witness_id") in own_w else foreign).append(r)
    if foreign:
        path = cross_dir(ax._base, ax.axis_id) / "07_MATCHING" / "03_match-records" / "relations.json"
        write_json(path, [{k: v for k, v in r.items() if k != "cross_axis"} for r in foreign])
        ax._base.register(path, f"{SHARED_FOLDER}:into-{ax.axis_id}:match-relations", None)
    return [{k: v for k, v in r.items() if k != "cross_axis"} for r in mine]


def stage_cross_evidence(ctx: RunContext) -> dict:
    """Make "this axis's folder + SHARED/CROSS-AXIS-into-<axis>" the complete evidence for assessing
    that axis alone.

    For every other-axis witness that bears on the axis's units, a read-only copy of the witness,
    its FRD, its question and the notebook's answer is placed in SHARED/CROSS-AXIS-into-<axis>/EVIDENCE/,
    each labelled with its home axis.  The canonical record stays in the home axis's database.
    SHARED/MEMBERSHIP.jsonl then answers "which axes does this record belong to?" without walking
    folders: one line per record that belongs to more than one axis."""
    out: dict[str, dict] = {}
    if not ctx.axis_layout or len(ctx.axis_ids()) < 2:
        return out
    member: dict[tuple, dict] = {}
    for a in ctx.axis_ids():
        rows = cross_relations(ctx, a)
        if not rows:
            continue
        refs = foreign_refs(ctx, a)
        ev = cross_dir(ctx, a) / "EVIDENCE"
        staged = {}
        for name, (fk, rel), field in (("witnesses", RELS["witnesses"], "witness_id"),
                                       ("retained-frds", ("frds", "05_validated/retained-frds.json"), "frd_id"),
                                       ("questions", RELS["questions"], "qid"),
                                       ("query-responses", RELS["responses"], "qid")):
            recs = foreign_rows(ctx, a, fk, rel, keep=refs[field], field=field) if refs[field] else []
            write_json(ev / f"{name}.json", recs)
            staged[name] = len(recs)
            kind = {"witnesses": "witness", "retained-frds": "frd", "questions": "question",
                    "query-responses": "query-response"}[name]
            for r in recs:
                key = (kind, r.get(field) if kind != "frd" else r.get("vfrd_id", r.get(field)))
                m = member.setdefault(key, {"kind": kind, "item_id": key[1], "home_axis": r["home_axis"],
                                            "axes": [r["home_axis"]]})
                if a not in m["axes"]:
                    m["axes"].append(a)
        atomic_write_text(ev / "README.md", (
            f"# Evidence from other axes that bears on axis {a}\n\n"
            f"Read-only copies, each labelled `home_axis`. The canonical record is in the home axis's folder. "
            f"To assess axis {a} alone, read that axis's folder plus this one: together they hold every "
            f"witness with a judged relation to {a}'s units.\n\n"
            + "\n".join(f"- `{k}.json`: {n}" for k, n in staged.items()) + "\n"))
        out[a] = staged
    lines = sorted(member.values(), key=lambda m: (m["kind"], str(m["item_id"])))
    from .runctx import SHARED_RESOURCES
    lines += [{"kind": "shared-resource", "item_id": r["path"], "home_axis": None, "axes": ctx.axis_ids(),
               "note": r["resource"]} for r in SHARED_RESOURCES]
    import json as _json
    atomic_write_text(ctx.axis_dir(SHARED_FOLDER) / "MEMBERSHIP.jsonl",
                      "".join(_json.dumps(m, ensure_ascii=False) + "\n" for m in lines))
    return out


def reconcile(ctx: RunContext) -> dict:
    """Do the axis databases add up to the run?  Every question is in exactly one axis; every answer,
    FRD and witness is in the axis of its question; nothing is left outside an axis."""
    kinds = {"questions": (RELS["questions"], "qid"), "responses": (RELS["responses"], "qid"),
             "candidate_frds": (("frds", "01_candidates/candidates.json"), "frd_id"),
             "validated_frds": (("frds", "05_validated/validated-frds.json"), "vfrd_id"),
             "retained_frds": (("frds", "05_validated/retained-frds.json"), "vfrd_id"),
             "witnesses": (RELS["witnesses"], "witness_id")}
    per: dict[str, dict] = {}
    problems: list[str] = []
    seen: dict[tuple, str] = {}
    for sc in ctx.scopes():
        a = sc.axis_id
        qids = {q["qid"] for q in (sc.load(*RELS["questions"], default=[]) or [])}
        per[a] = {}
        for kind, ((fk, rel), field) in kinds.items():
            rows = read_json(sc.p(fk, rel), default=[]) or []
            per[a][kind] = len(rows)
            for r in rows:
                key = (kind, r.get(field))
                if key in seen and seen[key] != a:
                    problems.append(f"{kind} {r.get(field)} is in both {seen[key]} and {a}")
                seen[key] = a
                if r.get("qid") not in qids:
                    problems.append(f"{kind} {r.get(field)} in {a} descends from {r.get('qid')}, which is not {a}'s question")
        per[a]["cross_axis_witnesses_bearing_on_this_axis"] = len(foreign_refs(ctx, a)["witness_id"]) \
            if len(ctx.axis_ids()) > 1 else 0
    totals = {k: sum(p[k] for p in per.values()) for k in kinds}
    sh = ctx.shared().p("discovery")
    left = [p.name for sub in ("01_issued-questions", "02_query-responses") if (sh / sub).exists()
            for p in (sh / sub).iterdir()]
    if left:
        problems.append(f"{len(left)} question/answer file(s) were left outside any axis in SHARED/02_DISCOVERY")
    quest = (ctx.stage_state().get("quest", {}).get("summary") or {})
    expected = next((quest[k] for k in ("questions", "questions_issued", "issued") if isinstance(quest.get(k), int)), None)
    if isinstance(expected, int) and expected != totals["questions"]:
        problems.append(f"the quest recorded {expected} questions; the axis databases hold {totals['questions']}")
    return {"by_axis": per, "totals": totals, "quest_questions": expected, "unassigned": 0 if not left else len(left),
            "note": "every question names one axis, so there is no unassigned bucket: a record with no "
                    "relation to any unit stays in its question's axis; a question refused for naming no "
                    "single axis was never asked and is listed in the quest folder's rejected.jsonl",
            "problems": problems}


def cross_axis_match(ctx: RunContext) -> dict:
    """After every axis has matched its own witnesses to its own units, ask of each axis whether the
    other axes' witnesses bear on its units.  Results are SHARED records."""
    from . import matching
    out: dict[str, dict] = {}
    if len(ctx.axis_ids()) < 2 or not cross_enabled(ctx):
        return out
    for a in ctx.axis_ids():
        cc = CrossContext(ctx, a)
        if not cc.load(*RELS["witnesses"]) or not cc.load(*RELS["units"], default=[]):
            continue
        ctx.log(f"   [SHARED] do the other axes' witnesses bear on {a}'s units?")
        s = matching.match_stage(cc)
        out[f"into-{a}"] = {k: s.get(k) for k in ("units", "witnesses", "pairs_assessed", "complete_relations",
                                                   "contradictions", "partial_relations")}
    return out
