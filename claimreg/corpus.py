"""Corpus ingest, manifest and local retrieval (the Archivist's database).

The specification's Archivist is "one retrieval database" holding the whole
logical corpus.  This module is that database for API-driven runs: every
admitted Markdown source is hashed into a manifest, split into
heading-aware chunks, and indexed with Okapi BM25.  Retrieval is used for

* the Archivist (named sources first, then any other admitted source), and
* blind FRD validation of long sources (the validator still sees only the one
  named source; retrieval just selects which parts of it to show).

Nothing here interprets evidence.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .util import (digest, ensure_dir, norm_for_match, read_json, read_text, sha256_file,
                   tokens, utcnow, word_count, write_json, text_encoding)

_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


@dataclass
class Chunk:
    cid: int
    filename: str
    heading: str
    start: int
    end: int
    text: str
    toks: list[str] = field(default_factory=list, repr=False)


def outline(text: str, max_items: int = 80) -> list[str]:
    out = []
    for line in text.splitlines():
        m = _HEADING.match(line)
        if m:
            out.append(("  " * (len(m.group(1)) - 1)) + m.group(2)[:120])
            if len(out) >= max_items:
                break
    return out


def split_chunks(filename: str, text: str, chunk_words: int = 320,
                 overlap: int = 40, start_id: int = 0) -> list[Chunk]:
    """Heading-aware chunking.  Each chunk remembers the nearest heading."""
    lines = text.splitlines(keepends=True)
    blocks: list[tuple[str, int, int]] = []    # (heading, start_char, end_char)
    pos = 0
    heading = "(start of document)"
    cur_start = 0
    cur_heading = heading
    for line in lines:
        m = _HEADING.match(line.rstrip("\n"))
        if m:
            if pos > cur_start:
                blocks.append((cur_heading, cur_start, pos))
            heading = m.group(2)[:160]
            cur_start = pos
            cur_heading = heading
        pos += len(line)
    if pos > cur_start:
        blocks.append((cur_heading, cur_start, pos))
    chunks: list[Chunk] = []
    cid = start_id
    for head, s, e in blocks:
        seg = text[s:e]
        words = list(re.finditer(r"\S+", seg))
        if not words:
            continue
        i = 0
        while i < len(words):
            j = min(len(words), i + chunk_words)
            cs = s + words[i].start()
            ce = s + words[j - 1].end()
            chunks.append(Chunk(cid, filename, head, cs, ce, text[cs:ce]))
            cid += 1
            if j >= len(words):
                break
            i = max(i + 1, j - overlap)
    return chunks


def _quality_flags(text: str) -> list[str]:
    flags = []
    wc = word_count(text)
    if wc < 150:
        flags.append("LOW_WORD_COUNT")
    if text:
        alnum = sum(ch.isalnum() for ch in text)
        if alnum / max(1, len(text)) < 0.55:
            flags.append("POSSIBLE_OCR_OR_TABLE_NOISE")
    return flags


def ingest(project_dir: Path, source_dir: Path, extensions=(".md", ".markdown", ".txt")) -> dict:
    """Hash every admitted source and write a versioned manifest."""
    if not Path(source_dir).is_dir():
        raise FileNotFoundError(f"corpus folder not found: {source_dir}")
    files = sorted(p for p in Path(source_dir).rglob("*")
                   if p.is_file() and p.suffix.lower() in extensions
                   and not p.name.startswith("."))
    if not files:
        raise FileNotFoundError(f"no {', '.join(extensions)} files in the corpus folder {source_dir}")
    sources = []
    by_hash: dict[str, str] = {}
    head_map: dict[str, str] = {}
    total_bytes = 0
    for p in files:
        rel = p.relative_to(source_dir).as_posix()
        h = sha256_file(p)
        text = read_text(p)
        b = p.stat().st_size
        total_bytes += b
        flags = _quality_flags(text)
        if text_encoding(p) != "utf-8":
            flags.append("NOT_UTF8_DECODED_AS_CP1252")
        dup_of = by_hash.get(h)
        head = norm_for_match(text[:3000])
        near = head_map.get(head) if len(head) > 400 else None
        if dup_of:
            flags.append(f"DUPLICATE_OF:{dup_of}")
        elif near:
            flags.append(f"NEAR_DUPLICATE_OF:{near}")
        by_hash.setdefault(h, rel)
        if len(head) > 400:
            head_map.setdefault(head, rel)
        title = next((ln.lstrip("# ").strip() for ln in text.splitlines()
                      if ln.strip().startswith("#")), p.stem)
        sources.append({
            "source_id": f"SRC-{h[:12]}", "filename": rel, "bytes": b,
            "words": word_count(text), "sha256": h, "title_guess": title[:200],
            "flags": flags,
        })
    body = {"source_dir": str(source_dir), "files": len(sources), "bytes": total_bytes,
            "sources": sources}
    mid = "MANIFEST-" + digest([(s["filename"], s["sha256"]) for s in sources])
    manifest = {"manifest_id": mid, "created": utcnow(), **body}
    mdir = ensure_dir(Path(project_dir) / "01_CORPUS" / "manifests")
    write_json(mdir / f"{mid}.json", manifest)
    write_json(mdir / "CURRENT.json", {"manifest_id": mid, "path": f"{mid}.json",
                                       "updated": utcnow()})
    return manifest


def current_manifest(project_dir: Path) -> dict | None:
    mdir = Path(project_dir) / "01_CORPUS" / "manifests"
    cur = read_json(mdir / "CURRENT.json")
    if not cur:
        return None
    return read_json(mdir / cur["path"])


class Corpus:
    """In-memory view of the manifest's sources with a BM25 index over chunks."""

    def __init__(self, manifest: dict, chunk_words: int = 320, overlap: int = 40):
        self.manifest = manifest
        self.source_dir = Path(manifest["source_dir"])
        self.by_name = {s["filename"]: s for s in manifest["sources"]}
        self._lower = {s["filename"].lower(): s["filename"] for s in manifest["sources"]}
        self._texts: dict[str, str] = {}
        self.chunk_words = chunk_words
        self.overlap = overlap
        self._chunks: list[Chunk] | None = None
        self._by_file: dict[str, list[Chunk]] = defaultdict(list)
        self._df: Counter = Counter()
        self._avgdl = 1.0
        self._tf: list[Counter] = []

    # -------------------------------------------------------------- #
    @property
    def filenames(self) -> list[str]:
        return list(self.by_name)

    def text(self, filename: str) -> str:
        fn = self.resolve(filename) or filename
        if fn not in self._texts:
            self._texts[fn] = read_text(self.source_dir / fn)
        return self._texts[fn]

    def resolve(self, name: str) -> str | None:
        """Map a cited name (exact, case-folded, basename, or stem) to a filename."""
        if not name:
            return None
        n = name.strip().strip("`'\"()[] ")
        if n in self.by_name:
            return n
        low = n.lower()
        if low in self._lower:
            return self._lower[low]
        base = low.rsplit("/", 1)[-1]
        for k, v in self._lower.items():
            if k.rsplit("/", 1)[-1] == base:
                return v
        stem = re.sub(r"(\.pdf)?\.(md|markdown|txt)$", "", base)
        if len(stem) >= 4:
            for k, v in self._lower.items():
                ks = re.sub(r"(\.pdf)?\.(md|markdown|txt)$", "", k.rsplit("/", 1)[-1])
                if ks == stem:
                    return v
        # a citation pattern may have swallowed preceding words ("see Sánchez 2019.md")
        words = n.split(" ")
        for i in range(1, len(words)):
            r = self.resolve(" ".join(words[i:]))
            if r:
                return r
        return None

    # -------------------------------------------------------------- #
    def _build(self) -> None:
        if self._chunks is not None:
            return
        chunks: list[Chunk] = []
        for fn in self.filenames:
            cs = split_chunks(fn, self.text(fn), self.chunk_words, self.overlap,
                              start_id=len(chunks))
            chunks.extend(cs)
        for c in chunks:
            c.toks = tokens(c.heading + " " + c.text)
            self._by_file[c.filename].append(c)
        self._tf = [Counter(c.toks) for c in chunks]
        for tf in self._tf:
            self._df.update(tf.keys())
        self._avgdl = sum(len(c.toks) for c in chunks) / max(1, len(chunks))
        self._chunks = chunks

    @property
    def chunks(self) -> list[Chunk]:
        self._build()
        return self._chunks or []

    def _score(self, q: list[str], idx: int, k1: float = 1.4, b: float = 0.75) -> float:
        tf = self._tf[idx]
        dl = len(self._chunks[idx].toks)  # type: ignore[index]
        n = len(self._chunks)  # type: ignore[arg-type]
        s = 0.0
        for t in q:
            f = tf.get(t)
            if not f:
                continue
            df = self._df.get(t, 0)
            idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
            s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * dl / self._avgdl))
        return s

    def search(self, query: str, k: int = 8, restrict: set[str] | None = None,
               exclude: set[str] | None = None) -> list[tuple[float, Chunk]]:
        self._build()
        q = list(dict.fromkeys(tokens(query)))
        if not q:
            return []
        if restrict is not None:
            cand = [c.cid for fn in restrict for c in self._by_file.get(fn, [])]
        else:
            cand = range(len(self._chunks))  # type: ignore[arg-type]
        scored = []
        for i in cand:
            c = self._chunks[i]  # type: ignore[index]
            if exclude and c.filename in exclude:
                continue
            s = self._score(q, i)
            if s > 0:
                scored.append((s, c))
        scored.sort(key=lambda x: (-x[0], x[1].cid))
        return scored[:k]

    def excerpt(self, filename: str, query: str, max_words: int) -> dict:
        """Best parts of one source for a query, in document order.

        If the whole source fits in ``max_words`` it is returned whole.
        """
        fn = self.resolve(filename) or filename
        text = self.text(fn)
        if word_count(text) <= max_words:
            return {"filename": fn, "complete": True, "words": word_count(text),
                    "outline": outline(text), "text": text}
        self._build()
        ranked = self.search(query, k=400, restrict={fn})
        chosen, used = [], 0
        for _, c in ranked:
            w = word_count(c.text)
            if used + w > max_words:
                continue
            chosen.append(c)
            used += w
            if used >= max_words * 0.95:
                break
        if not chosen:  # nothing matched: give the opening of the document
            chosen = [c for c in self._by_file.get(fn, [])][:max(1, max_words // max(1, self.chunk_words))]
        chosen.sort(key=lambda c: c.start)
        parts, last_head = [], None
        for c in chosen:
            if c.heading != last_head:
                parts.append(f"[section: {c.heading}]")
                last_head = c.heading
            parts.append(c.text)
        return {"filename": fn, "complete": False, "words": used,
                "outline": outline(text), "text": "\n\n".join(parts)}

    def total_bytes(self) -> int:
        return int(self.manifest.get("bytes", 0))


def find_quote(source_text: str, quote: str, min_ratio: float = 0.92) -> dict:
    """Mechanical verbatim check of a quotation against its source.

    Returns {"found": bool, "method": "exact"|"segments"|"fuzzy"|"none", ...}.
    Quotations may contain ellipses ("...") joining several passages; each
    segment of 6+ words must be present.  For long single passages a
    character-level fuzzy match over a sliding window is the fallback.
    """
    ns = norm_for_match(source_text)
    nq = norm_for_match(quote)
    if not nq:
        return {"found": False, "method": "none", "why": "empty quote"}
    if nq in ns:
        return {"found": True, "method": "exact"}
    raw_segs = re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\]|\[…\]|\n)\s*", quote or "")
    segs = [norm_for_match(x).strip(" .") for x in raw_segs]
    segs = [x for x in segs if len(x.split()) >= 3]
    if len(segs) >= 2 or (len(segs) == 1 and len(raw_segs) > 1):
        long_segs = [x for x in segs if len(x.split()) >= 5]
        miss = [x for x in segs if x not in ns]
        if long_segs and not miss:
            return {"found": True, "method": "segments", "segments": len(segs)}
        if long_segs and len(miss) <= len(segs) // 4 and all(len(m.split()) < 12 for m in miss):
            return {"found": True, "method": "segments_partial",
                    "segments": len(segs), "missing": miss[:3]}
    # fuzzy: locate candidate start positions from 4-word anchors, then compare
    # the quote with the source window at each candidate using difflib.
    import difflib
    words = nq.split()
    if len(words) < 6:
        return {"found": False, "method": "none", "why": "short quote not found verbatim"}
    starts: set[int] = set()
    step = max(1, len(words) // 12)
    for i in range(0, max(1, len(words) - 3), step):
        g = " ".join(words[i:i + 4])
        offset = len(" ".join(words[:i])) + (1 if i else 0)
        pos = ns.find(g)
        n_hits = 0
        while pos != -1 and n_hits < 8:
            starts.add(max(0, pos - offset))
            n_hits += 1
            pos = ns.find(g, pos + 1)
    best = 0.0
    for st in sorted(starts)[:60]:
        window = ns[st: st + len(nq) + 30]
        sm = difflib.SequenceMatcher(None, nq, window, autojunk=False)
        matched = sum(b.size for b in sm.get_matching_blocks())
        r = matched / max(1, len(nq))
        best = max(best, r)
        if best >= min_ratio:
            return {"found": True, "method": "fuzzy", "ratio": round(best, 3)}
    return {"found": False, "method": "none", "best_ratio": round(best, 3)}
