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
    from .corpus_intake import normalize_corpus, part_map, logical_count
    normalize_corpus(source_dir)
    parts = part_map(source_dir)
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
            **({"split_origin": parts[rel], "logical_source_id": parts[rel]["logical_source_id"]} if rel in parts else {}),
        })
    body = {"source_dir": str(source_dir), "files": len(sources), "bytes": total_bytes,
            "sources": sources, "logical_sources": logical_count(Path(source_dir), files)}
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
        from .corpus_intake import MAX_SOURCE_BYTES
        for source in manifest["sources"]:
            path = Path(manifest["source_dir"]) / source["filename"]
            if path.is_file() and path.stat().st_size > MAX_SOURCE_BYTES:
                raise ValueError("Corpus file exceeds 210,000 bytes; run cr corpus before continuing: " + source["filename"])
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
        r = self._resolve_exactish(n)
        if r:
            return r
        # a citation pattern may have swallowed preceding words ("see Sánchez 2019.md"): try each
        # shorter tail once.  (Each tail is checked directly, not recursively; the recursive form
        # doubled its work per word and never finished on long NotebookLM answer phrases.)
        words = n.split(" ")
        for i in range(1, len(words)):
            r = self._resolve_exactish(" ".join(words[i:]).strip("`'\"()[] "))
            if r:
                return r
        # NotebookLM truncates long source filenames in its citations (e.g. "...the-bioava.md").
        # Accept a unique prefix of one known filename, so a long-name citation still resolves.
        return self._resolve_truncated_prefix(n)

    def _resolve_truncated_prefix(self, n: str) -> str | None:
        low = (n or "").lower().strip().strip("`'\"()[] ").rsplit("/", 1)[-1]
        if len(low) < 24:
            return None
        stem = re.sub(r"(\.pdf)?\.(md|markdown|txt)$", "", low)
        if len(stem) < 20:
            return None
        hits = []
        for k, v in self._lower.items():
            kb = k.rsplit("/", 1)[-1]
            ks = re.sub(r"(\.pdf)?\.(md|markdown|txt)$", "", kb)
            if len(ks) > len(stem) and ks.startswith(stem):
                hits.append(v)
                if len(hits) > 1:
                    return None  # ambiguous prefix: never guess
        return hits[0] if hits else None

    def _resolve_exactish(self, n: str) -> str | None:
        if not n:
            return None
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


# --------------------------------------------------------------------------- #
# quotation check
# --------------------------------------------------------------------------- #
# A quotation is accepted when it is in the source word for word (after the formatting
# normalisation of ``norm_for_match``), or when every difference from the source is one that
# cannot change what the passage says.  Finding a similar passage is not enough: "did improve"
# is 100% contained in "did not improve".  So a near match only LOCATES the passage; each
# difference is then examined, and a quotation that drops or changes a negation, a number, a
# hedge or a limiting word, or that contains words the source does not have, is rejected.

_LIMITER_RE = re.compile(r"\b(?:only|unless|except|if|but|however|although|though|whereas)\b", re.I)
_DIGITS = re.compile(r"\d+(?:\.\d+)?")
# a citation marker stuck to the word before it once superscripts are flattened: "study28", "al.32"
_GLUED_CITE = re.compile(r"(?:(?<=[a-z])|(?<=[a-z][.)]))\d[\d,\-]*")
_LOCATOR_RE = re.compile(r"^[(\[]?\s*(?:fig(?:ure)?|table|section|abstract|results?|methods?|discussion|"
                         r"introduction|conclusions?|summary|opening|page|p\.|para(?:graph)?|appendix|"
                         r"supplement|box|panel|footnote|caption|heading|title)\b", re.I)


def _protected_words(s: str) -> list[str]:
    from .util import MODAL_RE, NEGATION_RE
    return [m.group(0) for rx in (NEGATION_RE, MODAL_RE, _LIMITER_RE) for m in rx.finditer(s)]


def _difference_problem(q: str, s: str) -> str:
    """'' when the quotation stretch ``q`` and the source stretch ``s`` it stands for differ only in
    ways that cannot change the meaning; otherwise what is wrong, in words."""
    import difflib
    from collections import Counter
    if re.sub(r"\s+", "", q) == re.sub(r"\s+", "", s):
        return ""
    dq, ds = Counter(_DIGITS.findall(q)), Counter(_DIGITS.findall(s))
    if dq != ds:
        extra_s = ds - dq
        glued = Counter(d for m in _GLUED_CITE.finditer(s) for d in _DIGITS.findall(m.group(0)))
        # the one tolerated case: the source carries citation markers the quotation left out
        if (dq - ds) or (extra_s - glued):
            return f"a number differs (quotation \"{q.strip()[:60]}\", source \"{s.strip()[:60]}\")"
    pq, ps = Counter(w.lower() for w in _protected_words(q)), Counter(w.lower() for w in _protected_words(s))
    if pq != ps:
        words = sorted(((ps - pq) + (pq - ps)).elements())
        return (f"the quotation changes or leaves out \"{', '.join(words)}\" "
                f"(quotation \"{q.strip()[:60]}\", source \"{s.strip()[:60]}\")")
    lq, ls = re.sub(r"[^a-z]", "", q), re.sub(r"[^a-z]", "", s)
    same = sum(b.size for b in difflib.SequenceMatcher(None, lq, ls, autojunk=False).get_matching_blocks())
    if len(lq) - same > 3:
        return f"the quotation has words the source does not have here (\"{q.strip()[:60]}\")"
    return ""


def _checked_differences(nq: str, window: str) -> tuple[bool, str, int]:
    """Compare a located passage with the quotation, difference by difference.
    Returns (acceptable, first problem, number of differences examined)."""
    import difflib
    ops = [o for o in difflib.SequenceMatcher(None, nq, window, autojunk=False).get_opcodes() if o[0] != "equal"]
    spans = []
    for tag, i1, i2, j1, j2 in ops:
        if i1 == i2 and i1 in (0, len(nq)):
            continue                      # source text before or after the quoted passage
        if i1 == i2 and (nq[i1 - 1] == " " or nq[i1] == " "):
            a = b = i1                    # the source has whole words here that the quotation skips
        else:
            a = nq.rfind(" ", 0, i1) + 1
            b = nq.find(" ", i2)
            b = len(nq) if b == -1 else b
        c = window.rfind(" ", 0, j1) + 1
        d = window.find(" ", j2)
        d = len(window) if d == -1 else d
        if spans and (a <= spans[-1][1] or c <= spans[-1][3]):
            spans[-1] = (spans[-1][0], max(b, spans[-1][1]), spans[-1][2], max(d, spans[-1][3]))
        else:
            spans.append((a, b, c, d))
    for a, b, c, d in spans:
        why = _difference_problem(nq[a:b], window[c:d])
        if why:
            return False, why, len(spans)
    return True, "", len(spans)


def _find_bounded(ns: str, text: str, pos: int) -> int:
    """First occurrence of ``text`` in ``ns`` at or after ``pos`` that does not start or end inside a word."""
    at = ns.find(text, pos)
    while at != -1:
        end = at + len(text)
        left = at == 0 or not (ns[at - 1].isalnum() and text[0].isalnum())
        right = end == len(ns) or not (ns[end].isalnum() and text[-1].isalnum())
        if left and right:
            return at
        at = ns.find(text, at + 1)
    return -1


def _span_cover(ns: str, nq: str, max_spans: int = 4, min_words: int = 3, short_gap: int = 40) -> dict:
    """A quotation the source's layout broke up (a figure, a caption or a table between two halves
    of a sentence): every word of it must be in the source, in order, in at most a few verbatim
    spans.  Source text skipped between two spans without an ellipsis is examined: a short skip that
    contains a negation, a number, a hedge or a limiting word is the quotation leaving out
    something that matters, and is rejected."""
    words = nq.split()
    i, pos, spans, skipped = 0, 0, [], []
    while i < len(words):
        if len(words) - i < min_words:
            return {"found": False, "why": "the last words of the quotation were not found after the rest"}
        lo, hi, hit = i + min_words, len(words), None
        at = _find_bounded(ns, " ".join(words[i:lo]), pos)
        if at == -1:
            return {"found": False, "why": f"\"{' '.join(words[i:i + 6])} ...\" was not found in the source"
                    + (" after the preceding words" if spans else "")}
        hit = (lo, at)
        while lo < hi:                    # longest run of words found verbatim at or after pos
            mid = (lo + hi + 1) // 2
            at = _find_bounded(ns, " ".join(words[i:mid]), pos)
            if at != -1:
                lo, hit = mid, (mid, at)
            else:
                hi = mid - 1
        j, at = hit
        if spans:
            gap = ns[pos:at]
            n_gap = len(gap.split())
            if n_gap <= short_gap:
                bad = _protected_words(gap) + [d for d in _DIGITS.findall(_GLUED_CITE.sub("", gap))]
                if bad:
                    return {"found": False, "why": f"the quotation skips \"{gap.strip()[:80]}\" without an ellipsis; "
                                                   f"the skipped words include \"{bad[0]}\""}
            skipped.append(n_gap)
        spans.append(j - i)
        pos = at + len(" ".join(words[i:j]))
        i = j
    if len(spans) > max_spans or len(spans) > 1 + len(words) // 6:
        return {"found": False, "why": f"the quotation is stitched from {len(spans)} separate fragments of the source"}
    return {"found": True, "method": "spans", "spans": len(spans), "skipped_source_words": skipped}


def find_quote(source_text: str, quote: str, min_ratio: float = 0.92) -> dict:
    """Mechanical verbatim check of a quotation against its source.

    Returns {"found": bool, "method": "exact"|"segments"|"segments_partial"|"fuzzy"|"spans"|"none", ...}.

    * exact - the quotation is in the source word for word.
    * segments - the quotation joins passages with ellipses ("..."); every passage is in the source.
    * segments_partial - as above, and the few passages not found word for word are each a
      locator label the validator added ("Table 2:", "(abstract)") or differ from the source only
      in formatting.  A passage that is neither is a fabricated passage and the quotation fails.
    * fuzzy - a passage at least ``min_ratio`` similar was located AND every difference from it
      is harmless: spacing, markup residue, a citation marker.  A difference that drops or
      changes a negation, a number, a hedge or a limiting word, or adds words, fails.
    * spans - the source's layout split the passage; all of the quotation is in the source, in
      order, in a few verbatim spans, and nothing protected was skipped between them.
    A failed check says why in "why"; "located" tells a passage was found but did not pass.
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
            alnum = re.sub(r"[^a-z0-9]", "", ns)
            bad = [m for m in miss if not _segment_acceptable(ns, alnum, m, min_ratio)]
            if not bad:
                return {"found": True, "method": "segments_partial",
                        "segments": len(segs), "missing": miss[:3]}
            return {"found": False, "method": "none", "located": True,
                    "why": f"a quoted passage is not in the source: \"{bad[0][:100]}\""}
    words = nq.split()
    if len(words) < 6:
        return {"found": False, "method": "none", "why": "short quote not found verbatim"}
    ok, info = _fuzzy_checked(ns, nq, min_ratio)
    if ok:
        return {"found": True, "method": "fuzzy", **info}
    sp = _span_cover(ns, nq)
    if sp["found"]:
        return sp
    out = {"found": False, "method": "none", "best_ratio": info.get("ratio", 0.0)}
    if info.get("why"):
        out.update(located=True, why="a similar passage was located, but " + info["why"])
    elif sp.get("why"):
        out["why"] = sp["why"]
    return out


def _segment_acceptable(ns: str, ns_alnum: str, seg: str, min_ratio: float) -> bool:
    """May a passage of an ellipsis quotation that is not in the source word for word be let through?"""
    squeezed = re.sub(r"[^a-z0-9]", "", seg)
    if len(squeezed) >= 8 and squeezed in ns_alnum:
        return True                        # the same characters; only spacing or punctuation differs
    if len(seg.split()) <= 12 and not _protected_words(seg) and (
            _LOCATOR_RE.match(seg) or re.fullmatch(r"[(\[].*[)\]]:?", seg) or seg.endswith(":")):
        return True                        # a locator label, not a claim about the source
    if len(seg.split()) >= 6:
        return _fuzzy_checked(ns, seg, min_ratio)[0] or _span_cover(ns, seg)["found"]
    return False


def _fuzzy_checked(ns: str, nq: str, min_ratio: float) -> tuple[bool, dict]:
    """Locate candidate passages from 4-word anchors, then examine every difference."""
    import difflib
    words = nq.split()
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
    best, why = 0.0, ""
    for st in sorted(starts)[:60]:
        window = ns[st: st + len(nq) + 30]
        sm = difflib.SequenceMatcher(None, nq, window, autojunk=False)
        r = sum(b.size for b in sm.get_matching_blocks()) / max(1, len(nq))
        best = max(best, r)
        if r >= min_ratio:
            # the start was estimated from the quotation's own word lengths, so it is off by the
            # length of anything the quotation leaves out: examine a slightly wider passage
            ok, problem, n = _checked_differences(nq, ns[max(0, st - 40): st + len(nq) + 40])
            if ok:
                return True, {"ratio": round(r, 3), "differences_checked": n}
            why = why or problem
    return False, {"ratio": round(best, 3), "why": why}
