"""Prompt library loader.

Each role prompt is a Markdown file in ``claimreg/prompts/`` with two
sections, ``## SYSTEM`` and ``## USER``.  ``{{NAME}}`` placeholders are filled
by ``render``.  ``{{> spec/FILE.md}}`` includes a specification document
verbatim (the user's own prompts, e.g. ACH_Eval_NLM_Super, are used unchanged).

A project may override any prompt by placing a file with the same name in
``<project>/90_METHOD/prompts/``.  Every run snapshots the exact prompt texts
it used (with sha256) into ``00_RUN-CONTROL/prompt-snapshots``.
"""

from __future__ import annotations

import re
from pathlib import Path

from .util import read_text, sha256_text

PROMPT_DIR = Path(__file__).parent / "prompts"
_INCLUDE = re.compile(r"\{\{>\s*([^}]+?)\s*\}\}")
_VAR = re.compile(r"\{\{\s*([A-Z0-9_]+)\s*\}\}")


class PromptLibrary:
    def __init__(self, project_dir: str | Path | None = None):
        self.override_dir = (Path(project_dir) / "90_METHOD" / "prompts") if project_dir else None
        self.used: dict[str, str] = {}   # name -> sha256 of raw template

    def raw(self, name: str) -> str:
        if self.override_dir:
            p = self.override_dir / name
            if p.exists():
                return read_text(p)
        p = PROMPT_DIR / name
        if not p.exists():
            raise FileNotFoundError(f"prompt template not found: {name}")
        return read_text(p)

    def _expand(self, text: str, depth: int = 0) -> str:
        if depth > 3:
            return text
        return _INCLUDE.sub(lambda m: self._expand(self.raw(m.group(1)), depth + 1), text)

    def render(self, name: str, **vars) -> tuple[str, str, str]:
        """Return (system, user, template_sha256)."""
        raw = self.raw(name)
        self.used[name] = sha256_text(raw)
        text = self._expand(raw)
        m_sys = re.search(r"^## SYSTEM\s*$", text, re.M)
        m_usr = re.search(r"^## USER\s*$", text, re.M)
        if not (m_sys and m_usr):
            raise ValueError(f"prompt {name} must contain '## SYSTEM' and '## USER' sections")
        system = text[m_sys.end():m_usr.start()].strip()
        user = text[m_usr.end():].strip()

        def sub(s: str) -> str:
            def rep(m):
                k = m.group(1)
                if k not in vars:
                    raise KeyError(f"prompt {name}: missing variable {k}")
                v = vars[k]
                return v if isinstance(v, str) else str(v)
            return _VAR.sub(rep, s)

        return sub(system), sub(user), self.used[name]

    def snapshot(self, dest_dir: Path) -> dict:
        """Write every prompt used so far, with hashes, to ``dest_dir``."""
        from .util import atomic_write_text, write_json
        dest_dir.mkdir(parents=True, exist_ok=True)
        index = {}
        for name, h in sorted(self.used.items()):
            safe = name.replace("/", "__")
            atomic_write_text(dest_dir / safe, self.raw(name))
            index[name] = {"sha256": h, "file": safe}
        write_json(dest_dir / "PROMPT-INDEX.json", index)
        return index
