"""Parse a frozen Discovery Quest Header into a machine-readable frame.

The human-written header is the controlling statement.  This parser only
locates what the header already says: axes, the approved hypothesis
statements, each hypothesis's assumptions / falsification / corroboration
sections, the decisive-test map, the gauge, and approval status.

Two input forms are accepted:

1. A Markdown header following the ACH 2.0 Quest Header template (v2), or the
   PTX v4.x layout.  Hypotheses are identified by IDs such as ``A1-H1``.
2. A ``frame.json`` written by hand (see ``FRAME_JSON_EXAMPLE`` below), which
   bypasses parsing entirely.
"""

from __future__ import annotations

import re
from pathlib import Path

from .util import norm_ws, read_json, read_text, sha256_text, utcnow

HID_RE = re.compile(r"\b([A-Z][A-Za-z]?\d+-H\d+)\b")

FRAME_JSON_EXAMPLE = {
    "title": "Investigation title",
    "gauge": 64,
    "mission": "What the investigation is for, and the operational discriminator.",
    "axes": [{
        "axis_id": "A1",
        "question": "The approved axis question",
        "boundary": "Governing boundary text, if any",
        "scope": "Population / scope",
        "approval": "APPROVED",
        "hypotheses": [{
            "id": "A1-H1", "title": "short title",
            "statement": "complete approved statement",
            "assumptions": "assumptions and antecedents",
            "falsification": "potential falsification context",
            "corroboration": "potential corroboration context",
        }],
    }],
    "decisive_tests": [{"test": "Exposure", "question": "..."}],
}

_FIELD_PATTERNS = {
    "assumptions": re.compile(r"\*\*\s*Assumptions(?: and antecedents)?\s*:?\s*\*\*\s*:?", re.I),
    "falsification": re.compile(r"\*\*\s*Potential falsification[^*]*\*\*\s*:?", re.I),
    "corroboration": re.compile(r"\*\*\s*Potential corroboration[^*]*\*\*\s*:?", re.I),
}


def _clean(s: str) -> str:
    s = re.sub(r"\*\*|__", "", s or "")
    s = s.replace("\\|", "|")
    return norm_ws(s)


def _sections(text: str) -> list[tuple[int, str, int, int]]:
    """(level, heading text, start, end) for every Markdown heading."""
    heads = [(len(m.group(1)), m.group(2).strip(), m.start(), m.end())
             for m in re.finditer(r"^(#{1,6})\s+(.*?)\s*$", text, re.M)]
    out = []
    for i, (lvl, h, s, e) in enumerate(heads):
        end = len(text)
        for lvl2, _, s2, _ in heads[i + 1:]:
            if lvl2 <= lvl:
                end = s2
                break
        out.append((lvl, h, s, end))
    return out


def _table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        if line.strip().startswith("|") and not re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def _extract_fields(block: str) -> dict:
    out = {}
    marks = []
    for k, pat in _FIELD_PATTERNS.items():
        m = pat.search(block)
        if m:
            marks.append((m.start(), m.end(), k))
    marks.sort()
    for i, (s, e, k) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(block)
        val = block[e:end]
        val = re.split(r"\n#{1,6}\s", val)[0]
        out[k] = _clean(val)
    return out


def parse_header(text: str, default_gauge: int = 64) -> dict:
    secs = _sections(text)
    title = next((h for lvl, h, _, _ in secs if lvl == 1), "Untitled investigation")
    gm = re.search(r"\bG\s*=\s*\**\s*(\d{2,3})", text)
    gauge = int(gm.group(1)) if gm else default_gauge

    # hypothesis statements from tables
    statements: dict[str, str] = {}
    for row in _table_rows(text):
        if len(row) >= 2:
            m = HID_RE.search(_clean(row[0]))
            if m and len(_clean(row[1])) > 30:
                statements.setdefault(m.group(1), _clean(row[1]))

    # per-hypothesis sections
    hyp_sections: dict[str, dict] = {}
    for lvl, h, s, e in secs:
        m = HID_RE.search(h)
        if m and lvl >= 3:
            hid = m.group(1)
            block = text[s:e]
            title_txt = _clean(re.sub(r"^.*?" + re.escape(hid) + r"\s*[—–:-]*\s*", "", h))
            f = _extract_fields(block)
            if f:
                hyp_sections[hid] = {"title": title_txt, **f}

    ids = sorted(set(statements) | set(hyp_sections),
                 key=lambda x: (x.split("-")[0], int(re.sub(r"\D", "", x.split("-H")[1]) or 0)))
    if not ids:
        raise ValueError("No hypotheses found. The header must label hypotheses with IDs such "
                         "as A1-H1, A1-H2, A1-H3 (a table row '| **A1-H1** | statement |' and a "
                         "section '#### A1-H1 — title' with Assumptions / Potential falsification "
                         "/ Potential corroboration paragraphs), or supply 01_FRAME/frame.json.")

    # axes
    axis_ids = sorted({i.split("-")[0] for i in ids}, key=lambda a: int(re.sub(r"\D", "", a) or 0))
    axis_blocks: dict[str, str] = {}
    axis_heads = [(lvl, h, s, e) for lvl, h, s, e in secs if re.search(r"\baxis\b", h, re.I)]
    word_num = {"one": 1, "two": 2, "three": 3, "four": 4, "1": 1, "2": 2, "3": 3, "4": 4}
    for lvl, h, s, e in axis_heads:
        m = re.search(r"axis\s*(one|two|three|four|\d)", h, re.I)
        if m:
            n = word_num[m.group(1).lower()]
            # the block runs to the next axis heading (they are siblings)
            nxt = [s2 for _, _, s2, _ in axis_heads if s2 > s]
            end = min(nxt) if nxt else e
            axis_blocks[f"A{n}"] = text[s:end]
    axes = []
    for a in axis_ids:
        block = axis_blocks.get(a, "")
        q = ""
        if block:
            body = re.sub(r"^#{1,6}.*\n", "", block, count=1).strip()
            q = _clean(body.split("\n\n")[0])
        bm = re.search(r"\*\*Governing boundary\.?\*\*\s*(.*?)(?:\n\s*\n)", block + "\n\n", re.S)
        cm = re.search(r"\*\*Cohort:?\*\*\s*:?\s*(.*?)(?:\n\s*\n)", block + "\n\n", re.S)
        approval = "UNKNOWN"
        if re.search(r"TEST-ONLY|not been reviewed or approved|must not govern", block, re.I):
            approval = "TEST_ONLY"
        elif re.search(r"\b(reviewed and approved|approved this)\b", block, re.I):
            approval = "APPROVED"
        hyps = []
        for hid in [i for i in ids if i.split("-")[0] == a]:
            sec = hyp_sections.get(hid, {})
            hyps.append({
                "id": hid, "title": sec.get("title", ""),
                "statement": statements.get(hid, ""),
                "assumptions": sec.get("assumptions", ""),
                "falsification": sec.get("falsification", ""),
                "corroboration": sec.get("corroboration", ""),
            })
        axes.append({"axis_id": a, "question": q,
                     "boundary": _clean(bm.group(1)) if bm else "",
                     "scope": _clean(cm.group(1)) if cm else "",
                     "approval": approval, "hypotheses": hyps})

    # decisive tests
    tests = []
    for lvl, h, s, e in secs:
        if lvl <= 3 and re.search(r"decisive[- ]test", h, re.I):
            for row in _table_rows(text[s:e]):
                if len(row) == 2 and not re.match(r"^\s*test\s*$", _clean(row[0]), re.I):
                    t, qq = _clean(row[0]), _clean(row[1])
                    if t and qq and not t.startswith("["):
                        tests.append({"test": t, "question": qq})
            break
    mission = ""
    for lvl, h, s, e in secs:
        if re.search(r"\bmission\b", h, re.I):
            mission = text[s:e].strip()
            break
    return {
        "title": _clean(title), "gauge": gauge, "axes": axes, "decisive_tests": tests,
        "mission": mission, "header_sha256": sha256_text(text), "parsed": utcnow(),
    }


def load_frame(project_dir: Path, header_path: Path | None, default_gauge: int = 64) -> dict:
    fj = Path(project_dir) / "01_FRAME" / "frame.json"
    if fj.exists():
        frame = read_json(fj)
        frame.setdefault("gauge", default_gauge)
        frame.setdefault("decisive_tests", [])
        frame.setdefault("mission", "")
        frame["source"] = "frame.json"
        if header_path and Path(header_path).exists():
            frame["header_sha256"] = sha256_text(read_text(header_path))
        return frame
    if not header_path or not Path(header_path).exists():
        raise FileNotFoundError(f"header not found: {header_path}")
    text = read_text(header_path)
    frame = parse_header(text, default_gauge)
    frame["source"] = str(header_path)
    return frame


def all_hypotheses(frame: dict) -> list[dict]:
    out = []
    for ax in frame["axes"]:
        for h in ax["hypotheses"]:
            out.append({**h, "axis_id": ax["axis_id"], "axis_question": ax.get("question", ""),
                        "axis_boundary": ax.get("boundary", ""), "axis_scope": ax.get("scope", ""),
                        "axis_approval": ax.get("approval", "UNKNOWN")})
    return out


def hypothesis_text(h: dict) -> str:
    """The full human-written hypothesis (the controlling statement)."""
    parts = [f"{h['id']}: {h.get('statement','')}"]
    if h.get("assumptions"):
        parts.append(f"Assumptions and antecedents: {h['assumptions']}")
    if h.get("falsification"):
        parts.append(f"Potential falsification: {h['falsification']}")
    if h.get("corroboration"):
        parts.append(f"Potential corroboration: {h['corroboration']}")
    return "\n".join(parts)


def rivals_of(frame: dict, hid: str) -> list[str]:
    """Rivals are the other hypotheses on the same axis."""
    for ax in frame["axes"]:
        ids = [h["id"] for h in ax["hypotheses"]]
        if hid in ids:
            return [i for i in ids if i != hid]
    return []


HYPOTHESIS_LABEL_RE = re.compile(r"\b[A-Z][A-Za-z]?\d+-H\d+\b|\bH[1-9]\b")
