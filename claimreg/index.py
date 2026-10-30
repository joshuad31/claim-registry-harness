"""Ranked index: parse an existing index, or build one with the indexer role.

Ranks guide attention; they are never evidence (spec module 6).
"""

from __future__ import annotations

import re
from pathlib import Path

from .llm.base import LLMRequest
from .util import read_text, truncate_words, word_count

_RANK_HEAD = re.compile(r"^#{1,6}\s+.*?\bRank\s+([ABCF])\b", re.I)
_ENTRY_HEAD = re.compile(r"^(#{3,6})\s+(\S.*)$")
_FILE = re.compile(r"([\w@().,'&+\- ]+?\.(?:pdf\.md|md|markdown|txt))", re.I)   # \w: accented names too


def parse_index(text: str, corpus=None) -> dict:
    """Return {"ranks": {filename: rank}, "entries": {filename: entry_text}}.

    Works with the PTX index layout (rank sections containing #### entries
    with a **Source:** link) and with simple tables "| filename | rank | ...".
    Filenames are resolved against the corpus when one is supplied.
    """
    ranks: dict[str, str] = {}
    entries: dict[str, str] = {}
    cur_rank = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = _RANK_HEAD.match(line)
        if m:
            cur_rank = m.group(1).upper()
            i += 1
            continue
        e = _ENTRY_HEAD.match(line)
        top = re.match(r"^(#{1,2})\s", line)
        if top and cur_rank:
            cur_rank = None          # a new top-level section ends the ranked list
        if e and cur_rank:
            level = len(e.group(1))
            j = i + 1
            while j < len(lines):
                e2 = _ENTRY_HEAD.match(lines[j]) or re.match(r"^(#{1,6})\s", lines[j])
                if e2 and len(re.match(r"^(#+)", lines[j]).group(1)) <= level:
                    break
                j += 1
            body = "\n".join(lines[i:j])
            fn = None
            src_line = next((ln for ln in lines[i:j] if "source" in ln.lower() and ".md" in ln.lower()), "")
            for cand in _FILE.findall(src_line or body):
                cand = cand.strip(" [(<")
                if corpus is not None:
                    r = corpus.resolve(cand)
                    if r:
                        fn = r
                        break
                else:
                    fn = cand
                    break
            if fn:
                ranks.setdefault(fn, cur_rank)
                entries.setdefault(fn, body.strip())
            i = j
            continue
        i += 1
    # table form
    for line in lines:
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2:
                fn = None
                rank = None
                for c in cells:
                    mm = _FILE.search(c)
                    if mm and not fn:
                        fn = mm.group(1).strip()
                    if re.fullmatch(r"\**[ABCF]\**", c):
                        rank = c.strip("*")
                if fn and rank:
                    if corpus is not None:
                        fn = corpus.resolve(fn) or fn
                    ranks.setdefault(fn, rank)
                    entries.setdefault(fn, line)
    return {"ranks": ranks, "entries": entries}


def compact_index(parsed: dict, corpus=None, max_words_per_entry: int = 45) -> str:
    """One line per source: rank, filename, short gist. Used in prompts."""
    rows = []
    order = {"A": 0, "B": 1, "C": 2, "F": 3}
    names = list(parsed["ranks"])
    if corpus is not None:
        for fn in corpus.filenames:
            if fn not in parsed["ranks"]:
                names.append(fn)
    for fn in sorted(set(names), key=lambda f: (order.get(parsed["ranks"].get(f, "C"), 4), f.lower())):
        rk = parsed["ranks"].get(fn, "unranked")
        ent = parsed["entries"].get(fn, "")
        gist = ""
        if ent:
            t = re.search(r"\*\*Title:\*\*\s*(.+)", ent)
            task = re.search(r"\*\*(?:Retrieval task|Relevance):\*\*\s*(.+)", ent)
            scope = re.search(r"\*\*Scope:\*\*\s*(.+)", ent)
            bits = [x.group(1).strip() for x in (t, scope, task) if x]
            gist = " | ".join(bits) if bits else re.sub(r"\s+", " ", ent)
        rows.append(f"[{rk}] {fn} :: {truncate_words(gist, max_words_per_entry)}")
    return "\n".join(rows)


def build_index_requests(ctx, question: str, max_words: int = 6000) -> list[LLMRequest]:
    reqs = []
    for fn in ctx.corpus.filenames:
        text = ctx.corpus.text(fn)
        wc = word_count(text)
        note = "complete" if wc <= max_words else f"first {max_words} words of {wc}"
        body = text if wc <= max_words else truncate_words(text, max_words)
        system, user, _ = ctx.prompts.render("index_entry.md", QUESTION=question, FILENAME=fn,
                                             WORDS=wc, NOTE=note, TEXT=body)
        reqs.append(LLMRequest(role="indexer", system=system, user=user, tag=f"index:{fn}",
                               meta={"filename": fn}))
    return reqs


def render_index(entries: list[dict], title: str) -> str:
    order = {"A": 0, "B": 1, "C": 2, "F": 3}
    out = [f"# {title} — Ranked Source Index", "",
           "> Ranks guide retrieval attention only. They are never evidence.", ""]
    for rank in "ABCF":
        group = [e for e in entries if (e.get("rank") or "C").upper().startswith(rank)]
        if not group:
            continue
        out += [f"### Rank {rank} — {len(group)} sources", ""]
        for e in sorted(group, key=lambda x: x["filename"].lower()):
            out += [f"#### {e['filename']}", "",
                    f"- **Title:** {e.get('author_year_title','')}",
                    f"- **Relevance:** {e.get('relevance','')}",
                    f"- **Summary:** {e.get('summary','')}",
                    f"- **Contradictions and gaps:** {e.get('contradictions_and_gaps','')}",
                    f"- **Source:** {e['filename']}", ""]
    return "\n".join(out)
