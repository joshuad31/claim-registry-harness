"""Small shared helpers: hashing, ids, atomic JSON io, text normalisation."""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from pathlib import Path
from typing import Any, Iterable, Iterator


# --------------------------------------------------------------------------- #
# time, hashing, ids
# --------------------------------------------------------------------------- #

def utcnow() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_text(s: str) -> str:
    return sha256_bytes(s.encode("utf-8"))


def sha256_file(path: str | os.PathLike) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                      default=str)


def digest(obj: Any, n: int = 12) -> str:
    return sha256_text(canonical_json(obj))[:n]


def make_id(prefix: str, obj: Any, n: int = 12) -> str:
    """Content-addressed identifier: PREFIX-<first n hex of sha256>."""
    return f"{prefix}-{digest(obj, n)}"


# --------------------------------------------------------------------------- #
# file io
# --------------------------------------------------------------------------- #

def ensure_dir(p: str | os.PathLike) -> Path:
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


def replace_file(tmp: str | os.PathLike, path: str | os.PathLike, tries: int = 40, wait: float = 0.05) -> None:
    """os.replace that waits out a reader.  On Windows a file cannot be replaced while another
    process or thread has it open, even for reading; the reader is done within milliseconds."""
    import time
    for n in range(tries):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if n == tries - 1:
                raise
            time.sleep(wait)


def atomic_write_text(path: str | os.PathLike, text: str) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        replace_file(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def write_json(path: str | os.PathLike, obj: Any) -> None:
    atomic_write_text(path, json.dumps(obj, indent=2, ensure_ascii=False,
                                       sort_keys=False, default=str) + "\n")


def read_json(path: str | os.PathLike, default: Any = None) -> Any:
    """Read JSON; tolerates a UTF-8 byte-order mark (Windows Notepad / PowerShell 5.1 add one)."""
    path = Path(path)
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_jsonl(path: str | os.PathLike, rows: Iterable[Any]) -> None:
    lines = [json.dumps(r, ensure_ascii=False, default=str) for r in rows]
    atomic_write_text(path, "\n".join(lines) + ("\n" if lines else ""))


def append_jsonl(path: str | os.PathLike, row: Any) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def read_jsonl(path: str | os.PathLike) -> list:
    path = Path(path)
    if not path.exists():
        return []
    out = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def read_text(path: str | os.PathLike) -> str:
    """Read text as UTF-8 (a byte-order mark is dropped).  A file that is not valid UTF-8 is
    decoded as Windows-1252 instead of being silently mangled; ``text_encoding`` tells which."""
    data = Path(path).read_bytes()
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("cp1252", errors="replace")


def text_encoding(path: str | os.PathLike) -> str:
    """'utf-8' or 'cp1252 (not UTF-8)' - used to flag sources saved in a legacy encoding."""
    try:
        Path(path).read_bytes().decode("utf-8-sig")
        return "utf-8"
    except UnicodeDecodeError:
        return "cp1252 (not UTF-8)"


# --------------------------------------------------------------------------- #
# text helpers
# --------------------------------------------------------------------------- #

_WS = re.compile(r"\s+")


def norm_ws(s: str) -> str:
    return _WS.sub(" ", s or "").strip()


def word_count(s: str) -> int:
    """Whitespace-separated token count (the spec's witness-ceiling unit)."""
    return len((s or "").split())


# --- math / HTML markup folding --------------------------------------------- #
# PDF -> markdown conversion leaves LaTeX math ($36.3 \pm 16.7$) and inline HTML
# (<sub>, <sup>, <i>, <br>) in the corpus, while validators quote the rendered
# text (36.3 ± 16.7, T4).  Fold both sides to the same plain form before the
# markdown strip.  This is representation-only: no numeral is added or removed.
_TAG_BR = re.compile(r"<br\s*/?>", re.I)
# Inline tags carry no word boundary: "T<sub>4</sub>" must fold to "T4".
_TAG_INLINE = re.compile(
    r"</?(?:sub|sup|i|b|u|em|strong|math|span|small|big|tt|del|ins|font)\s*/?>", re.I)
# Any remaining HTML-shaped tag.  Autolinks such as <https://...> are not tags
# (the ':' after the scheme fails the identifier pattern), so URLs survive.
_TAG_OTHER = re.compile(r"</?[A-Za-z][A-Za-z0-9]*(?:\s[^<>]*)?/?>")

_LATEX_MAP = {
    # operators / relations
    "pm": "±", "mp": "∓", "times": "×", "cdot": "·", "div": "÷",
    "le": "<=", "leq": "<=", "ge": ">=", "geq": ">=",
    "approx": "~", "sim": "~", "simeq": "~", "cong": "~", "propto": "~",
    "ne": "!=", "neq": "!=",
    # greek / symbols (the corpus uses these for ΔT4, µg and degrees)
    "mu": "μ", "Delta": "Δ", "delta": "Δ", "alpha": "α", "beta": "β",
    "tau": "τ", "chi": "χ", "circ": "°",
    # layout-only commands: drop the command name, keep the argument text
    "text": "", "textrm": "", "textit": "", "textbf": "", "mathrm": "",
    "mathit": "", "mathbf": "", "left": "", "right": "",
    # genuine spacing commands become a word break
    "quad": " ", "qquad": " ",
}
_LATEX_CMD = re.compile(r"\\([A-Za-z]+)")
# LaTeX unit commands leave a space the rendered text does not have
# ("$\mu$ g" -> " μ g", quoted as "μg"); bind Greek symbols and degree signs to
# the following unit.  Applied before the quote map (for Δ) and again after the
# markdown strip (bold markers such as "**2.34 ± 1.3**" re-introduce the space).
_SYMBOL_SPACE = re.compile(
    r"\s*([\u00b5\u03bc\u03b1\u03b2\u03c4\u03c7\u0394\u00b0])\s*")

# Validators prefix a quotation with the section it came from ("Abstract - Results:",
# "Results - Evening administration:", "Footnote c:", "Section 3.5. Results of
# syntheses:").  That label is the validator's own scaffolding, not source text, so
# it is folded away on both sides.  Word labels may not carry digits (a numeral in a
# label is data, not scaffolding); section/table/figure/case/footnote labels may.
_LOCATOR_WORD_LABEL = re.compile(
    r"(^|[\n.;:!?\u2026])[ \t]*(?:abstract|results?|methods?|discussion|conclusions?|"
    r"background|objectives?|aims?|design|study design|patients and methods|subjects|"
    r"interventions?|outcomes?|measurements|statistical analysis)"
    r"(?![A-Za-z0-9_-])(?:[ \t]+[A-Za-z()\-\u2010-\u2015]+){0,6}[ \t]*:[ \t]*", re.I)
_LOCATOR_NUM_LABEL = re.compile(
    r"(^|[\n.;:!?\u2026])[ \t]*(?:section|appendix|table|figure|fig|footnote|case|"
    r"panel|part|phase|supplementary)(?![A-Za-z0-9_-])(?:[ \t]+[^\s:]{1,24}){0,6}"
    r"[ \t]*:[ \t]*", re.I)
# "Section 3.5." headings end with a period instead of a colon.
_LOCATOR_SECTION_DOT = re.compile(
    r"(^|[\n.;:!?\u2026])[ \t]*(?i:section|appendix|part|phase)"
    r"(?![A-Za-z0-9_-])(?:[ \t]+[^\s:]{1,24}){0,5}?[ \t]*\.[ \t]+(?=[A-Z(])")


def _fold_locator_labels(s: str) -> str:
    """Drop validator-added locator labels ("Results - Evening administration:").

    The numbered-section pattern runs first: it consumes "Section 3.5. " while a
    following space still separates it from the label body, before the word-label
    pattern removes the body and its trailing whitespace.
    """
    for pat in (_LOCATOR_SECTION_DOT, _LOCATOR_WORD_LABEL, _LOCATOR_NUM_LABEL):
        s = pat.sub(lambda m: m.group(1), s)
    return s


def _fold_markup(s: str) -> str:
    """Fold LaTeX math and inline HTML to plain text (representation only)."""
    s = _TAG_BR.sub(" ", s)                      # <br> is a line/word break
    s = _TAG_INLINE.sub("", s)                   # <sub>4</sub> -> 4 (no break)
    s = _TAG_OTHER.sub(" ", s)                   # remaining tags are markup
    s = s.replace("$", "")                       # math delimiters
    # Commands are mapped before the backslash strip so \pm etc. never become
    # the literal tokens "pm"/"times"; unknown command names are markup.
    s = _LATEX_CMD.sub(lambda m: _LATEX_MAP.get(m.group(1), ""), s)
    s = s.replace("{", "").replace("}", "")      # grouping braces
    s = s.replace("^", "").replace("_", "")      # superscript / subscript markers
    s = _SYMBOL_SPACE.sub(r"\1", s)              # μ g -> μg (first pass; see norm_for_match)
    return s


_QUOTE_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "′": "'", "″": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-",
    "―": "-", "−": "-", " ": " ", " ": " ", " ": " ",
    "·": ".", "•": " ", "×": "x",
    "±": "+-", "∓": "-+", "≤": "<=", "≥": ">=", "≈": "~", "∼": "~",
    "≠": "!=", "Δ": "delta",
    # Validators wrap a quotation in quote marks ("..."), the source does not.
    # They carry no semantic content for a verbatim check, so drop them.
    '"': "",
}
_STRIP_MD = re.compile(r"[*`#>|\\]")
_PUNCT_SPACE = re.compile(r"\s*([,.;:()\[\]{}%/=<>+-])\s*")


def norm_for_match(s: str) -> str:
    """Aggressive normalisation used for verbatim-quote verification.

    It folds unicode compatibility forms, LaTeX math and inline HTML markup,
    typographic quotes and dashes, markdown emphasis and table pipes, letter
    case, and whitespace around punctuation.  Two passages that differ only in
    those respects compare equal.
    """
    s = unicodedata.normalize("NFKC", s or "")
    s = _fold_markup(s)
    s = "".join(_QUOTE_MAP.get(ch, ch) for ch in s)
    # _QUOTE_MAP maps curly quotes to ASCII '"' in the same pass that would have to
    # drop them; the output is not re-examined, so drop quote marks explicitly.
    s = s.replace('"', "")
    s = _STRIP_MD.sub(" ", s)
    # Locator-label folding runs after the markdown strip so a bold label
    # ("**Results:**") is already plain ("Results:").
    s = _fold_locator_labels(s)
    # Markdown emphasis markers become spaces, which can re-split a unit from the
    # number (source "**2.34 ± 1.3** µIU/mL" would otherwise fold to
    # "2.34+-1.3 μiu/ml"), so bind unit symbols again after the strip.
    s = _SYMBOL_SPACE.sub(r"\1", s)
    s = re.sub(r"-{2,}|={2,}|:-+|-+:", "-", s)      # table rules of any length
    s = s.lower()
    s = _PUNCT_SPACE.sub(r"\1", s)
    s = _WS.sub(" ", s).strip()
    return s


_TOKEN = re.compile(r"[a-z0-9]+(?:[.\-'][a-z0-9]+)*")
STOPWORDS = frozenset("""
a about above after again against all also am an and any are as at be because been
before being below between both but by can could did do does doing down during each
few for from further had has have having he her here hers herself him himself his how
i if in into is it its itself just me more most my myself no nor not now of off on once
only or other our ours ourselves out over own same she should so some such than that
the their theirs them themselves then there these they this those through to too under
until up very was we were what when where which while who whom why will with would you
your yours yourself yourselves et al vs via per e.g i.e may might must shall
""".split())


def tokens(s: str, drop_stop: bool = True) -> list[str]:
    toks = _TOKEN.findall(norm_for_match(s))
    if drop_stop:
        toks = [t for t in toks if t not in STOPWORDS and len(t) > 1]
    return toks


def truncate_words(s: str, n: int) -> str:
    w = (s or "").split()
    if len(w) <= n:
        return s or ""
    return " ".join(w[:n]) + " …"


def safe_filename(s: str, maxlen: int = 80) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s[:maxlen] or "item"


def chunked(seq: list, n: int) -> Iterator[list]:
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def first_nonempty(*vals):
    for v in vals:
        if v:
            return v
    return None


_NUM = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)*(?:\s?%)?")


def numerals(s: str) -> set[str]:
    """Numbers appearing in a text, normalised (commas removed, % attached)."""
    out = set()
    for m in _NUM.finditer(unicodedata.normalize("NFKC", s or "")):
        t = m.group(0).replace(" ", "").replace(",", "")
        t = t.lstrip("+")
        if t:
            out.add(t)
    return out


NEGATION_RE = re.compile(
    r"\b(?:not|no|none|never|neither|nor|without|cannot|can't|didn't|doesn't|"
    r"don't|isn't|wasn't|weren't|aren't|failed|fail|fails|absent|absence|lack|lacked|"
    r"unchanged|insignificant|nonsignificant|non-significant)\b", re.I)

MODAL_RE = re.compile(
    r"\b(?:may|might|could|can|possibly|possible|likely|unlikely|suggests?|suggested|"
    r"appears?|appeared|must|should|would|probably|potential(?:ly)?|"
    r"hypothesi[sz]ed?|proposed?)\b", re.I)


def negation_count(s: str) -> int:
    return len(NEGATION_RE.findall(s or ""))


def modal_count(s: str) -> int:
    return len(MODAL_RE.findall(s or ""))
