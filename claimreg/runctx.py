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


# --------------------------------------------------------------------------- #
# axis databases (docs/AXIS-DATABASES.md)
# --------------------------------------------------------------------------- #
# Every axis of the header has its own evidence database: one folder that holds that axis's
# questions, answers, FRDs, validations, witnesses, units, match records, coverage, crux and reports.
# No file in an axis folder holds material of another axis.  Records that belong to more than one
# axis by nature (the Manager's cross-axis quest state and feedback, and relations between one axis's
# witnesses and another axis's units) live in the SHARED database.  Run control and the frozen frame
# inputs (header, index, Archivist prompt) stay at run level.
AXIS_LAYOUT = "axis-databases-v1"
SHARED_FOLDER = "SHARED"
# What is never individualized per axis (spec 10, section 6.4, rule 7): tools and run machinery
# that no assessment is run on.  Recorded in RUN-CONFIG.json so a verifier can assert that each
# exists once and that no axis folder holds a copy.
SHARED_RESOURCES = [
    {"resource": "run control", "path": "00_RUN-CONTROL/"},
    {"resource": "frozen frame inputs (header, index, Archivist prompt, frame)", "path": "01_FRAME/"},
    {"resource": "quest machinery (Manager state, checkpoints, feedback, closeout)", "path": "SHARED/02_DISCOVERY/"},
    {"resource": "language tools (dictionary, canonicalizer rulebook)", "path": "SHARED/04_LANGUAGE-TOOLS/"},
    {"resource": "matcher qualification", "path": "SHARED/07_MATCHING/02_match-fixtures/"},
]
SHARED_FRAME_FILES = {"header.md", "index.md", "archivist-custom-prompt.txt", "frame.json", "README.md"}
SHARED_DISCOVERY = ("03_quest-state", "04_ach-eval-checkpoints", "05_feedback", "06_closeout", "99_superseded")
_SLUG_STOP = {"the", "a", "an", "of", "about", "for", "to", "and", "or", "in", "on", "with", "from", "by", "is",
              "does", "do", "should", "be", "that", "this", "at", "as"}


def axis_slug(axis: dict, labels: dict | None = None) -> str:
    """A short, readable label for an axis folder, e.g. 'bedtime-dosing'."""
    label = (labels or {}).get(axis.get("axis_id", "")) or axis.get("name") or axis.get("question") or ""
    words = [w for w in re.findall(r"[a-z0-9]+", label.lower()) if w not in _SLUG_STOP]
    out: list[str] = []
    for w in words:
        if len(out) >= 4 or len("-".join(out + [w])) > 34:
            break
        out.append(w)
    return "-".join(out)


def axis_folder_name(axis: dict, labels: dict | None = None) -> str:
    slug = axis_slug(axis, labels)
    return f"AXIS-{axis['axis_id']}" + (f"__{slug}" if slug else "")


def axis_of_hypothesis(hid: str) -> str:
    return str(hid).split("-")[0]


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
            if bool((self.cfg.get("axes") or {}).get("separate_databases", True)):
                # one evidence database per axis: only run control and the frame live at run level;
                # the axis folders are made when the frame is frozen
                for f in ("00_RUN-CONTROL", "01_FRAME", "00_RUN-CONTROL/model-and-human-decisions",
                          "00_RUN-CONTROL/prompt-snapshots"):
                    ensure_dir(self.run_dir / f)
                write_json(self.run_dir / "RUN-CONFIG.json",
                           {"run_id": run_id, "created": utcnow(), "project": self.cfg["project"],
                            "layout": AXIS_LAYOUT, "shared_resources": SHARED_RESOURCES})
            else:
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
    axis_id = None        # a RunContext is the whole run; AxisContext narrows it to one axis

    @property
    def axis_layout(self) -> bool:
        """True when this run keeps one evidence database per axis (new runs do; old runs do not)."""
        if getattr(self, "_axis_layout", None) is None:
            rc = self.run_config
            if not rc:
                return False
            self._axis_layout = rc.get("layout") == AXIS_LAYOUT
        return self._axis_layout

    def axis_ids(self) -> list[str]:
        return [a["axis_id"] for a in self.frame.get("axes", [])]

    def axis_dir(self, axis_id: str) -> Path:
        if axis_id == SHARED_FOLDER:
            return self.run_dir / SHARED_FOLDER
        labels = (self.cfg.get("axes") or {}).get("labels") or {}
        for a in self.frame.get("axes", []):
            if a["axis_id"] == axis_id:
                return self.run_dir / axis_folder_name(a, labels)
        raise KeyError(f"no axis {axis_id} in the frame")

    def for_axis(self, axis_id: str) -> "AxisContext":
        return AxisContext(self, axis_id)

    def shared(self) -> "AxisContext":
        return AxisContext(self, SHARED_FOLDER)

    def scopes(self) -> list:
        """The contexts a per-axis stage runs in: one per axis, or just this run for an old-layout run."""
        if not self.axis_layout:
            return [self]
        return [self.for_axis(a) for a in self.axis_ids()]

    def discovery_ctx(self):
        """Where the quest's cross-axis working records live (SHARED in an axis-database run)."""
        return self.shared() if self.axis_layout else self

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
        path = self.p(folder_key, rel)
        if path.exists() or not self.axis_layout:
            return read_json(path, default=default)
        return self.load_whole_run(folder_key, rel, default)

    def load_whole_run(self, folder_key: str, rel: str, default=None):
        """A read-only view of one record type across every axis database (plus SHARED), for tools
        that report on the whole run (`cr verify`, `cr funnel`, `cr status`).  Nothing is stored this
        way: on disk each axis keeps its own file."""
        sh = self.shared().p(folder_key, rel)
        if sh.exists():
            return read_json(sh, default=default)
        try:
            scopes = self.scopes()
        except FileNotFoundError:
            return default
        parts = [read_json(sc.p(folder_key, rel), default=None) for sc in scopes]
        if (folder_key, rel) == ("matching", "03_match-records/relations.json"):
            for a in self.axis_ids():
                parts.append(read_json(self.axis_dir(SHARED_FOLDER) / f"CROSS-AXIS-into-{a}" / "07_MATCHING"
                                       / "03_match-records" / "relations.json", default=None))
        parts = [x for x in parts if x is not None]
        if not parts:
            return default
        out = parts[0]
        for x in parts[1:]:
            out = _combine(out, x)
        return out

    def artifact_paths(self, folder_key: str, *parts: str) -> list[tuple[str, Path]]:
        """(axis, path) of the same document in every axis database - or the one path of an old-layout run."""
        if not self.axis_layout:
            return [("", self.p(folder_key, *parts))]
        return [(sc.axis_id, sc.p(folder_key, *parts)) for sc in self.scopes()]

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


def _combine(a, b):
    """Join two axes' copies of the same record type for a whole-run view."""
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    if isinstance(a, dict) and isinstance(b, dict):
        out = dict(a)
        for k, v in b.items():
            out[k] = _combine(out[k], v) if k in out else v
        return out
    if isinstance(a, bool) or isinstance(b, bool):
        return a and b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + b
    return a


class AxisContext:
    """One axis's view of a run (or the SHARED database's).

    Stage code is written against a RunContext and never mentions axes.  Given an AxisContext it
    reads and writes only inside that axis's folder, and sees a frame that contains only that axis,
    so its questions, FRDs, witnesses, units, matches, coverage, crux and reports all land in the
    axis's own database.  Run control (log, registry, model calls, stage state) and the frozen frame
    inputs stay with the run."""

    def __init__(self, base: RunContext, axis_id: str):
        self._base = base
        self.axis_id = axis_id
        self._frame: dict | None = None
        # True while a later stage of this axis runs (joint, coverage, crux, assess, report): reads
        # then include the SHARED cross-axis evidence that bears on this axis's units
        self.merge_shared: bool = False

    def __getattr__(self, name):            # cfg, llm, prompts, corpus, log, run_dir, project_dir, ...
        return getattr(self._base, name)

    @property
    def axis_layout(self) -> bool:
        return True

    @property
    def is_shared(self) -> bool:
        return self.axis_id == SHARED_FOLDER

    @property
    def root(self) -> Path:
        return self._base.axis_dir(self.axis_id)

    @property
    def frame(self) -> dict:
        if self._frame is None:
            full = self._base.frame
            if self.is_shared:
                self._frame = full
            else:
                ids = {a["axis_id"] for a in full.get("axes", [])}

                def mine(test: dict) -> bool:
                    named = set(re.findall(r"\bA\d+\b", str(test.get("test", "")))) & ids
                    return not named or self.axis_id in named
                self._frame = {**full, "axes": [a for a in full.get("axes", []) if a["axis_id"] == self.axis_id],
                               "decisive_tests": [t for t in full.get("decisive_tests", []) if mine(t)],
                               "axis_scope": self.axis_id}
        return self._frame

    def p(self, folder_key: str, *parts: str) -> Path:
        folder = RUN_FOLDERS.get(folder_key, folder_key)
        if folder_key == "control" or folder == "00_RUN-CONTROL":
            return self._base.p(folder_key, *parts)
        if folder == "01_FRAME" and parts and parts[0] in SHARED_FRAME_FILES:
            return self._base.p(folder_key, *parts)
        root = self.root
        if folder == "02_DISCOVERY" and parts and str(parts[0]).split("/")[0] in SHARED_DISCOVERY:
            root = self._base.axis_dir(SHARED_FOLDER)      # the Manager's cross-axis records
        if folder == "07_MATCHING" and parts and str(parts[0]).split("/")[0] == "02_match-fixtures":
            root = self._base.axis_dir(SHARED_FOLDER)      # the matcher is qualified once, for every axis
        if folder == "04_LANGUAGE-TOOLS":
            # the dictionary and the canonicalizer rulebook are one shared resource for every axis:
            # nobody assesses them, and one vocabulary must serve all the axes' witnesses and units
            root = self._base.axis_dir(SHARED_FOLDER)
        base = root / folder
        return base.joinpath(*parts) if parts else base

    def save(self, folder_key: str, rel: str, obj, kind: str | None = None,
             parents: list[str] | None = None) -> Path:
        if self.merge_shared and (folder_key, rel) == ("matching", "03_match-records/relations.json"):
            from .axes import split_relations_on_save
            obj = split_relations_on_save(self, obj)
        path = self.p(folder_key, rel)
        write_json(path, obj)
        self._base.register(path, f"{self.axis_id}:{kind or rel}", parents)
        return path

    def load(self, folder_key: str, rel: str, default=None):
        if self.merge_shared:
            from .axes import merged_load
            return merged_load(self, folder_key, rel, default)
        path = self.p(folder_key, rel)
        if self.is_shared and not path.exists():
            # a shared stage (the language tools) reads every axis's records together
            return self._base.load_whole_run(folder_key, rel, default)
        return read_json(path, default=default)

    def register(self, path: Path, kind: str, parents: list[str] | None = None) -> None:
        self._base.register(path, f"{self.axis_id}:{kind}", parents)

    def archivist_instructions(self) -> str:
        return self._base.archivist_instructions()

    def scopes(self) -> list:
        return [self]

    def discovery_ctx(self):
        return self._base.discovery_ctx()


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
