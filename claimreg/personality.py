"""Load the complete user-supplied research personality for the host mentor only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "agent" / "research-personality"
PART_CHARS = 6000


def source_files(package=None):
    package = Path(package) if package else PACKAGE
    manifest = json.loads((package / "INTEGRATION.json").read_text(encoding="utf-8"))
    expected = [row["path"] for row in manifest["files"]]
    for name in expected:
        path = package / name
        if not path.resolve().is_relative_to(package.resolve()) or not path.is_file():
            raise ValueError(f"Required research-personality file missing or invalid: {name}")
    # Include additions too. A rebuild must not revert to the previous five-file subset.
    extra = sorted(p.relative_to(package).as_posix() for p in package.rglob("*")
                   if p.is_file() and not p.is_symlink() and "__pycache__" not in p.parts
                   and p.name not in ("PERSONALITY.md", "INTEGRATION.json")
                   and p.suffix not in (".pyc", ".pyo") and p.relative_to(package).as_posix() not in expected)
    return [(name, package / name) for name in expected + extra]


def render(package=None):
    package = Path(package) if package else PACKAGE
    chunks = [(package / "PERSONALITY.md").read_text(encoding="utf-8")]
    for name, path in source_files(package):
        # Bodies are complete, including code and historical examples. Nothing is summarized out.
        chunks.append(f"\n\n===== COMPLETE PACKAGE FILE: {name} =====\n" + path.read_text(encoding="utf-8-sig"))
    return "\n".join(chunks)


def parts(package=None):
    text = render(package)
    return [text[i:i + PART_CHARS] for i in range(0, len(text), PART_CHARS)]


def preamble(package=None):
    count = len(parts(package))
    commands = "\n".join(f"  python cr.py personality --part {i}" for i in range(1, count + 1))
    return ("REQUIRED HOST-AGENT PERSONALITY: complete profile, skills, implementation, and restored memory.\n"
            "Apply throughout research mentoring. Keep historical context distinct from current actions.\n"
            "If this output is truncated, load ALL lossless parts before continuing:\n" + commands + "\n\n")


def cmd_personality(a):
    try:
        text = render()
        if getattr(a, "part", None) is not None:
            chunks = parts()
            if not 1 <= a.part <= len(chunks):
                raise ValueError(f"part must be between 1 and {len(chunks)}")
            print(f"Research personality part {a.part}/{len(chunks)}\n" + chunks[a.part - 1], end="")
        else:
            print(preamble() + text, end="")
        return 0
    except (ValueError, OSError) as e:
        print(f"Research personality could not be loaded: {e}")
        return 2
