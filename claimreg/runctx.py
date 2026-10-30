"""Run context: paths, artifact registry, stage state, shared resources."""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from .config import load_config, scientific_config
from .corpus import Corpus, current_manifest
from .llm.router import LLM
from .prompts import PromptLibrary
from .util import (append_jsonl, ensure_dir, read_json, read_text, sha256_file, utcnow,
                   write_json)

RUN_FOLDERS = {
    "control": "00_RUN-CONTROL",
    "frame": "01_FRAME",
    "discovery": "02_DISCOVERY",
    "frds": "03_FRDS",
    "language": "04_LANGUAGE-TOOLS",
    "witnesses": "05_WITNESSES",
    "transcoding": "06_TRANSCODING",
    "matching": "07_MATCHING",
    "coverage": "08_COVERAGE",
    "crux": "09_CRUX",
    "reports": "10_REPORTS",
}


RUN_SUBFOLDERS = [
    "00_RUN-CONTROL/model-and-human-decisions", "00_RUN-CONTROL/prompt-snapshots",
    "02_DISCOVERY/01_issued-questions", "02_DISCOVERY/02_query-responses", "02_DISCOVERY/03_quest-state",
    "02_DISCOVERY/04_ach-eval-checkpoints", "02_DISCOVERY/05_feedback", "02_DISCOVERY/06_closeout",
    "03_FRDS/01_candidates", "03_FRDS/02_harvest-accounting", "03_FRDS/04_validation-results",
    "03_FRDS/05_validated", "03_FRDS/06_source-assignment-audit",
    "04_LANGUAGE-TOOLS/02_dictionary", "04_LANGUAGE-TOOLS/03_canonicalizer",
    "05_WITNESSES/01_question-applications", "05_WITNESSES/02_raw-witnesses", "05_WITNESSES/03_fidelity-reviews",
    "05_WITNESSES/04_repaired-or-held", "05_WITNESSES/05_released",
    "07_MATCHING/01_hypothesis-units", "07_MATCHING/02_match-fixtures", "07_MATCHING/03_match-records",
    "07_MATCHING/04_disagreements-and-review", "09_CRUX/01_frozen-rival-theories", "09_CRUX/03_portability-tests",
    "09_CRUX/05_candidates",
]


def new_run_id(prefix: str = "RUN") -> str:
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{ts}"


def list_runs(project_dir: Path) -> list[str]:
    d = Path(project_dir) / "02_RUNS"
    if not d.exists():
        return []
    return sorted(p.name for p in d.iterdir() if p.is_dir() and not p.name.startswith("."))


def latest_run(project_dir: Path) -> str | None:
    cur = read_json(Path(project_dir) / "02_RUNS" / "CURRENT.json")
    if cur and (Path(project_dir) / "02_RUNS" / cur.get("run_id", "")).exists():
        return cur["run_id"]
    runs = list_runs(project_dir)
    return runs[-1] if runs else None


class RunContext:
    def __init__(self, project_dir: str | Path, run_id: str | None = None, create: bool = False,
                 quiet: bool = False):
        self.project_dir = Path(project_dir).resolve()
        self.cfg = load_config(self.project_dir)
        if run_id is None:
            run_id = latest_run(self.project_dir)
            if run_id is None:
                if not create:
                    raise FileNotFoundError(f"no run exists in {self.project_dir}; use 'cr new-run'")
                run_id = new_run_id(self.cfg["project"].get("run_prefix", "RUN"))
        self.run_id = run_id
        self.run_dir = self.project_dir / "02_RUNS" / run_id
        if not self.run_dir.exists():
            if not create:
                raise FileNotFoundError(f"run not found: {self.run_dir}")
            ensure_dir(self.run_dir)
            for f in RUN_FOLDERS.values():
                ensure_dir(self.run_dir / f)
            for sub in RUN_SUBFOLDERS:
                ensure_dir(self.run_dir / sub)
            write_json(self.project_dir / "02_RUNS" / "CURRENT.json",
                       {"run_id": run_id, "updated": utcnow()})
        # a run may pin its own config overrides (forks use this)
        run_over = read_json(self.run_dir / "RUN-OVERRIDES.json")
        if run_over:
            from .config import deep_merge
            pd = self.cfg["_project_dir"]
            self.cfg = deep_merge(self.cfg, run_over)
            self.cfg["_project_dir"] = pd
        self.quiet = quiet
        self.prompts = PromptLibrary(self.project_dir)
        self.llm = LLM(self.cfg, self.run_dir)
        self._corpus: Corpus | None = None
        self._frame: dict | None = None

    # ------------------------------------------------------------------ #
    def p(self, folder_key: str, *parts: str) -> Path:
        base = self.run_dir / RUN_FOLDERS.get(folder_key, folder_key)
        return base.joinpath(*parts) if parts else base

    def log(self, msg: str) -> None:
        line = f"[{utcnow()}] {msg}"
        if not self.quiet:
            print(msg, flush=True)
        append_text(self.p("control", "run-log.txt"), line + "\n")

    # ------------------------------------------------------------------ #
    @property
    def run_config(self) -> dict:
        return read_json(self.run_dir / "RUN-CONFIG.json", default={}) or {}

    def freeze_run_config(self, frame_sha: str, manifest_id: str, extra: dict | None = None) -> dict:
        rc = self.run_config
        if not rc:
            rc = {"run_id": self.run_id, "created": utcnow(), "project": self.cfg["project"]}
        rc.update({
            "manifest_id": manifest_id, "frame_sha256": frame_sha,
            "scientific_config": scientific_config(self.cfg), "frozen": utcnow(),
        })
        if extra:
            rc.update(extra)
        write_json(self.run_dir / "RUN-CONFIG.json", rc)
        return rc

    @property
    def corpus(self) -> Corpus:
        if self._corpus is None:
            mid = self.run_config.get("manifest_id")
            mdir = self.project_dir / "01_CORPUS" / "manifests"
            man = read_json(mdir / f"{mid}.json") if mid else current_manifest(self.project_dir)
            if not man:
                raise FileNotFoundError("no corpus manifest; run 'cr corpus <project>' first")
            src = Path(man["source_dir"])
            if not src.is_absolute():
                src = self.project_dir / src
            if not src.exists():
                # manifests written on another machine: fall back to the project corpus folder
                alt = self.project_dir / "01_CORPUS" / "source-files"
                if alt.exists():
                    src = alt
            man = {**man, "source_dir": str(src)}
            c = self.cfg["corpus"]
            self._corpus = Corpus(man, c.get("chunk_words", 320), c.get("chunk_overlap_words", 40))
        return self._corpus

    @property
    def frame(self) -> dict:
        if self._frame is None:
            f = read_json(self.p("frame", "frame.json"))
            if not f:
                raise FileNotFoundError("frame not frozen yet; run the 'frame' stage")
            self._frame = f
        return self._frame

    # ------------------------------------------------------------------ #
    def save(self, folder_key: str, rel: str, obj, kind: str | None = None,
             parents: list[str] | None = None) -> Path:
        path = self.p(folder_key, rel)
        write_json(path, obj)
        self.register(path, kind or rel, parents)
        return path

    def load(self, folder_key: str, rel: str, default=None):
        return read_json(self.p(folder_key, rel), default=default)

    def register(self, path: Path, kind: str, parents: list[str] | None = None) -> None:
        rel = path.relative_to(self.run_dir).as_posix()
        append_jsonl(self.p("control", "artifact-registry.jsonl"), {
            "time": utcnow(), "kind": kind, "path": rel, "sha256": sha256_file(path),
            "parents": parents or []})

    # ------------------------------------------------------------------ #
    def stage_state(self) -> dict:
        return read_json(self.p("control", "stage-state.json"), default={}) or {}

    def set_stage(self, name: str, status: str, summary: dict | None = None) -> None:
        st = self.stage_state()
        rec = st.get(name, {})
        rec.update({"status": status, "updated": utcnow()})
        if status == "running":
            rec["started"] = utcnow()
        if summary is not None:
            rec["summary"] = summary
        st[name] = rec
        write_json(self.p("control", "stage-state.json"), st)

    def archivist_instructions(self) -> str:
        p = self.p("frame", "archivist-custom-prompt.txt")
        return read_text(p) if p.exists() else ""


def append_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(text)


_LABEL_LINE = re.compile(r"^\s*\*?\s*(\[[A-Z][A-Z ]+\])\s*=\s*(.+)$", re.M)


def extract_labels(archivist_text: str) -> str:
    """Evidence labels and their meanings from the Archivist's instructions."""
    rows = [f"{m.group(1)} = {m.group(2).strip()}" for m in _LABEL_LINE.finditer(archivist_text or "")]
    if rows:
        return "\n".join(rows)
    found = sorted(set(re.findall(r"\[[A-Z][A-Z ]{2,}\]", archivist_text or "")))
    if found:
        return "\n".join(f"{f} (meaning as defined in the Archivist instructions)" for f in found)
    return ("[SOURCE] = source-reported finding\n[INFERRED] = extrapolation from cited premises\n"
            "[NO SOURCE] = support not located; a retrieval gap, not proof of absence")
