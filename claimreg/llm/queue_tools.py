"""Export queued requests in batches and import answers.

Pending requests live in ``<project>/queue/pending/<key>.json``.  ``export``
packs them into batch files an operator can work through:

* ``queue/batches/<BATCH>.json`` - machine-friendly list of requests
* ``queue/batches/<BATCH>.md``   - the same requests formatted for a person
                                   pasting into a chat window or NotebookLM

The operator writes answers to ``queue/batches/<BATCH>.response.json`` as an
object ``{"<key>": "<answer text>", ...}`` or to ``<BATCH>.response.md`` with
blocks headed ``=== RESPONSE <key> ===``.  ``import`` validates each answer
(JSON-expecting requests must parse) and files accepted answers under
``queue/done``.  The harness then resumes where it stopped.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..util import ensure_dir, read_json, read_text, utcnow, write_json, atomic_write_text
from .jsonparse import JSONExtractError, extract_json

BATCH_INSTRUCTIONS = """You are acting as the language model for the Claim Registry harness.
Each request below has a SYSTEM prompt and a USER prompt.  Answer each request
independently, exactly as a model given only that system and user prompt would.
Do not use any information outside the request itself.  When "expect_json" is
true, the answer must be a single valid JSON value and nothing else."""


def queue_dir(project_dir: Path, qcfg_dir: str = "queue") -> Path:
    d = Path(qcfg_dir)
    return d if d.is_absolute() else Path(project_dir) / d


def list_pending(qdir: Path, role: str | None = None) -> list[dict]:
    out = []
    for p in sorted((qdir / "pending").glob("*.json")):
        rec = read_json(p)
        if not rec:
            continue
        key = rec["key"]
        if any((qdir / "done" / f"{key}{e}").exists() for e in (".txt", ".md", ".json", ".skip.json")):
            continue
        if role and rec.get("role") != role:
            continue
        out.append(rec)
    return out


def export_batches(qdir: Path, size: int | dict = 10, role: str | None = None,
                   max_chars: int = 120_000, repack: bool = False) -> list[Path]:
    """``size`` may be one number or a map ``{"<role>": n, "default": n}``.
    ``repack=True`` first withdraws open batches (of ``role``, if given) that have no response
    file yet, so their requests can be packed again in a different size."""
    pend = list_pending(qdir, role)
    already = set()
    for bj in (qdir / "batches").glob("*.json"):
        if bj.name.endswith(".response.json"):
            continue
        b = read_json(bj) or {}
        if b.get("status") == "open":
            has_resp = any((qdir / "batches" / f"{bj.stem}.response{e}").exists() for e in (".json", ".md"))
            if repack and not has_resp and (role is None or b.get("role") == role):
                bj.unlink()
                md = bj.with_suffix(".md")
                if md.exists():
                    md.unlink()
                continue
            already.update(r["key"] for r in b.get("requests", []))
    pend = [r for r in pend if r["key"] not in already]
    # group by role, and by pass within a role (the salt: pass-a / pass-b / verify), so one operator
    # context handles one kind of task and independent passes never share a context
    by_role: dict[str, list[dict]] = {}
    for r in pend:
        name = r.get("role", "?") + (f"-{r['salt']}" if r.get("salt") and r.get("role") in
                                     ("incompat_checker", "joint_checker") else "")
        by_role.setdefault(name, []).append(r)
    made: list[Path] = []
    ensure_dir(qdir / "batches")
    n_existing = len([p for p in (qdir / "batches").glob("BATCH-*.json")
                      if not p.name.endswith(".response.json")])
    for role_name, items in sorted(by_role.items()):
        base_role = items[0].get("role", role_name)
        rsize = (int(size.get(role_name, size.get(base_role, size.get("default", 10))))
                 if isinstance(size, dict) else int(size))
        cur: list[dict] = []
        cur_chars = 0
        groups: list[list[dict]] = []
        for r in items:
            c = len(r["system"]) + len(r["user"])
            if cur and (len(cur) >= rsize or cur_chars + c > max_chars):
                groups.append(cur)
                cur, cur_chars = [], 0
            cur.append(r)
            cur_chars += c
        if cur:
            groups.append(cur)
        for g in groups:
            n_existing += 1
            bid = f"BATCH-{n_existing:04d}-{role_name}"
            body = {"batch_id": bid, "role": role_name, "created": utcnow(),
                    "status": "open", "instructions": BATCH_INSTRUCTIONS,
                    "response_file": f"{bid}.response.json",
                    "requests": [{k: r.get(k) for k in
                                  ("key", "role", "tag", "expect_json", "schema_hint",
                                   "system", "user")} for r in g]}
            jp = qdir / "batches" / f"{bid}.json"
            write_json(jp, body)
            md = [f"# {bid}\n", BATCH_INSTRUCTIONS, "",
                  f"Write answers to `{bid}.response.md` as blocks headed "
                  f"`=== RESPONSE <key> ===`, or to `{bid}.response.json`.", ""]
            for r in g:
                md += [f"=== REQUEST {r['key']} ===", f"role: {r['role']}   tag: {r.get('tag','')}",
                       f"expect_json: {r.get('expect_json')}", "", "--- SYSTEM ---",
                       r["system"], "", "--- USER ---", r["user"], ""]
            atomic_write_text(qdir / "batches" / f"{bid}.md", "\n".join(md))
            made.append(jp)
    return made


_RESP_BLOCK = re.compile(r"^=== RESPONSE ([0-9a-f]{8,64}) ===\s*$", re.M)


def _parse_md_responses(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    marks = list(_RESP_BLOCK.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[m.group(1)] = text[m.end():end].strip()
    return out


def import_responses(qdir: Path, operator_model: str = "queue-operator") -> dict:
    """File every answer found in batch response files. Returns an import report."""
    accepted, rejected = [], []
    pending_index = {p.stem: read_json(p) for p in (qdir / "pending").glob("*.json")}
    for rp in sorted((qdir / "batches").glob("*.response.*")):
        if rp.suffix == ".json":
            try:
                data = read_json(rp) or {}
            except ValueError as e:      # a hand-edited file that is not valid JSON
                rejected.append({"key": "*", "file": rp.name, "why": f"file is not valid JSON: {e}"})
                continue
            if isinstance(data, dict) and "responses" in data and isinstance(data["responses"], dict):
                data = data["responses"]
            answers = {k: (v if isinstance(v, str) else __import__("json").dumps(v, ensure_ascii=False))
                       for k, v in (data.items() if isinstance(data, dict) else [])}
        else:
            answers = _parse_md_responses(read_text(rp))
        for key, text in answers.items():
            done_p = qdir / "done" / f"{key}.txt"
            if done_p.exists():
                continue
            req = pending_index.get(key)
            if req is None:
                rejected.append({"key": key, "file": rp.name, "why": "no pending request with this key"})
                continue
            if req.get("expect_json"):
                try:
                    extract_json(text)
                except JSONExtractError as e:
                    rejected.append({"key": key, "file": rp.name, "why": f"not JSON: {e}"})
                    continue
            atomic_write_text(done_p, text)
            write_json(qdir / "done" / f"{key}.meta.json",
                       {"model": operator_model, "finished": utcnow(), "batch_file": rp.name,
                        "role": req.get("role"), "tag": req.get("tag")})
            accepted.append(key)
    # close batches whose every request is answered
    for bj in (qdir / "batches").glob("BATCH-*.json"):
        if bj.name.endswith(".response.json"):
            continue
        b = read_json(bj) or {}
        if b.get("status") != "open":
            continue
        keys = [r["key"] for r in b.get("requests", [])]
        if keys and all((qdir / "done" / f"{k}.txt").exists() or (qdir / "done" / f"{k}.skip.json").exists()
                        for k in keys):
            b["status"] = "answered"
            b["answered"] = utcnow()
            write_json(bj, b)
    report = {"time": utcnow(), "accepted": len(accepted), "rejected": rejected}
    ensure_dir(qdir)
    hist = read_json(qdir / "import-log.json", default=[]) or []
    hist.append(report)
    write_json(qdir / "import-log.json", hist)
    return report


def queue_status(qdir: Path) -> dict:
    pend = list_pending(qdir)
    by_role: dict[str, int] = {}
    for r in pend:
        by_role[r.get("role", "?")] = by_role.get(r.get("role", "?"), 0) + 1
    open_batches = []
    for bj in sorted((qdir / "batches").glob("BATCH-*.json")):
        if bj.name.endswith(".response.json"):
            continue
        b = read_json(bj) or {}
        if b.get("status") == "open":
            open_batches.append(bj.name)
    return {"pending": len(pend), "pending_by_role": by_role, "open_batches": open_batches}


def skip_requests(qdir: Path, keys: list[str], reason: str, operator: str = "queue-operator") -> dict:
    """Mark pending requests as deliberately unanswered.  The harness then treats each
    one as a failed call (recorded, never invented): the affected item is held, abstained
    or reported missing by its stage.  Delete ``done/<key>.skip.json`` to ask again."""
    done, unknown = [], []
    pend = {p.stem for p in (qdir / "pending").glob("*.json")}
    for k in keys:
        if k not in pend:
            unknown.append(k)
            continue
        if (qdir / "done" / f"{k}.txt").exists():
            continue
        write_json(qdir / "done" / f"{k}.skip.json", {"key": k, "reason": reason, "operator": operator,
                                                      "time": utcnow()})
        done.append(k)
    for bj in (qdir / "batches").glob("BATCH-*.json"):
        if bj.name.endswith(".response.json"):
            continue
        b = read_json(bj) or {}
        ks = [r["key"] for r in b.get("requests", [])]
        if b.get("status") == "open" and ks and all(
                (qdir / "done" / f"{x}.txt").exists() or (qdir / "done" / f"{x}.skip.json").exists() for x in ks):
            b["status"] = "answered"
            b["answered"] = utcnow()
            write_json(bj, b)
    return {"skipped": done, "unknown": unknown}

