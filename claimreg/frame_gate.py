"""The frame gate: a person signs the header before anything is run on it.

The header is the frame, and the frame decides what a run can find.  A researcher is allowed to
shape the frame toward the hypothesis they prefer; this module makes that happen in one place, in
the open, and on the record.  Before a quest or a model-backed run may start, a person at a keyboard

1. types what they want to be able to say and what they would concede;
2. sees a forecast for the draft frame and for alternative frames, and which is best for the
   hypothesis they prefer;
3. types the question and every hypothesis by hand, in their own words (paste is rejected);
4. reads the model's restatement of each hypothesis (a reading check, not a checkbox);
5. accepts each spelled-out consequence by typing it, including the forecast number and the worst
   likely result;
6. signs with a passphrase.  Each axis is signed when it is finished, so the work can be spread
   over several sittings.

The result is a signed frame certificate (``01_FRAME/frame-certificate.json`` and
``FRAME-CERTIFICATE.md``).  The signature is Ed25519 with a key derived from the passphrase, so the
certificate can be checked at launch without the passphrase and cannot be produced without it.
Nothing here judges whether a frame is self-serving.  It refuses only a frame nobody has typed,
read and signed.
"""

from __future__ import annotations

import difflib
import hashlib
import math
import os
import re
import sys
import textwrap
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .util import atomic_write_text, canonical_json, read_json, read_text, sha256_text, utcnow, write_json

CERT_JSON = "frame-certificate.json"
CERT_MD = "FRAME-CERTIFICATE.md"
SIGNER_FILE = Path.home() / ".claimreg" / "signer.json"
# The block on unsigned frames switches itself on the first time a frame is fully signed on this
# computer (that is the proof that signing works here).  There is no command that switches it off.
LOCK_FILE = Path.home() / ".claimreg" / "FRAME-GATE-LOCKED"
TARGET_SHARE = 2 / 3            # the preferred hypothesis should be forecast at two thirds of the gauge
FORECAST_CALLS = 3
PBKDF2_ROUNDS = 200_000
ROLE = "frame_gate"


class NotAPerson(Exception):
    """The frame can only be signed by a person at a keyboard."""


class Changed(Exception):
    """The person chose to stop and change the frame; nothing is signed."""


# --------------------------------------------------------------------------- #
# Ed25519 (RFC 8032), pure Python.  One signature per signing; speed does not matter.

_P = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_D = -121665 * pow(121666, _P - 2, _P) % _P
_I = pow(2, (_P - 1) // 4, _P)


def _add(p, q):
    a = (p[1] - p[0]) * (q[1] - q[0]) % _P
    b = (p[1] + p[0]) * (q[1] + q[0]) % _P
    c = 2 * p[3] * q[3] * _D % _P
    d = 2 * p[2] * q[2] % _P
    e, f, g, h = b - a, d - c, d + c, b + a
    return (e * f % _P, g * h % _P, f * g % _P, e * h % _P)


def _mul(s, p):
    q = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            q = _add(q, p)
        p = _add(p, p)
        s >>= 1
    return q


def _recover_x(y, sign):
    if y >= _P:
        return None
    x2 = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P != 0:
        x = x * _I % _P
    if (x * x - x2) % _P != 0:
        return None
    return _P - x if (x & 1) != sign else x


_GY = 4 * pow(5, _P - 2, _P) % _P
_GX = _recover_x(_GY, 0)
_G = (_GX, _GY, 1, _GX * _GY % _P)


def _compress(p):
    zinv = pow(p[2], _P - 2, _P)
    x, y = p[0] * zinv % _P, p[1] * zinv % _P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _decompress(s):
    if len(s) != 32:
        return None
    y = int.from_bytes(s, "little")
    sign, y = y >> 255, y & ((1 << 255) - 1)
    x = _recover_x(y, sign)
    return None if x is None else (x, y, 1, x * y % _P)


def _expand(seed):
    h = hashlib.sha512(seed).digest()
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a, h[32:]


def ed_public(seed: bytes) -> bytes:
    return _compress(_mul(_expand(seed)[0], _G))


def ed_sign(seed: bytes, msg: bytes) -> bytes:
    a, prefix = _expand(seed)
    pub = _compress(_mul(a, _G))
    r = int.from_bytes(hashlib.sha512(prefix + msg).digest(), "little") % _L
    rs = _compress(_mul(r, _G))
    h = int.from_bytes(hashlib.sha512(rs + pub + msg).digest(), "little") % _L
    return rs + int.to_bytes((r + h * a) % _L, 32, "little")


def ed_verify(public: bytes, msg: bytes, sig: bytes) -> bool:
    if len(public) != 32 or len(sig) != 64:
        return False
    a, r = _decompress(public), _decompress(sig[:32])
    s = int.from_bytes(sig[32:], "little")
    if a is None or r is None or s >= _L:
        return False
    h = int.from_bytes(hashlib.sha512(sig[:32] + public + msg).digest(), "little") % _L
    left, right = _mul(s, _G), _add(r, _mul(h, a))
    return ((left[0] * right[2] - right[0] * left[2]) % _P == 0
            and (left[1] * right[2] - right[1] * left[2]) % _P == 0)


# --------------------------------------------------------------------------- #
# The signer: one person's key, derived from a passphrase that is stored nowhere.

def _seed(passphrase: str, salt_hex: str) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), bytes.fromhex(salt_hex), PBKDF2_ROUNDS, 32)


def fingerprint(public_hex: str) -> str:
    h = hashlib.sha256(bytes.fromhex(public_hex)).hexdigest()[:16].upper()
    return "-".join(h[i:i + 4] for i in range(0, 16, 4))


def load_signer(path: Path | None = None) -> dict | None:
    s = read_json(path or SIGNER_FILE, default=None)
    return s if isinstance(s, dict) and s.get("public_key") and s.get("salt") else None


def create_signer(name: str, passphrase: str, path: Path | None = None) -> dict:
    path = Path(path or SIGNER_FILE)
    salt = os.urandom(16).hex()
    signer = {"name": name, "salt": salt, "public_key": ed_public(_seed(passphrase, salt)).hex(), "created": utcnow()}
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, signer)
    return signer


# --------------------------------------------------------------------------- #
# The console: typed by hand, at a keyboard.

def looks_pasted(stamps: list[float]) -> bool:
    """Keystrokes that arrive under 10 ms apart, for most of the text, were not typed."""
    if len(stamps) < 12:
        return False
    gaps = [b - a for a, b in zip(stamps, stamps[1:])]
    return sum(g < 0.010 for g in gaps) / len(gaps) > 0.5


class Terminal:
    """A real console.  Refuses pipes, scripts and command tools: there must be a keyboard."""

    def __init__(self):
        if not (sys.stdin.isatty() and sys.stdout.isatty()):
            raise NotAPerson("The frame is signed by a person at a keyboard, in a terminal window. It cannot be "
                             "run by a script, through a pipe, or by an agent's command tool.")

    def say(self, text: str = "") -> None:
        print(text, flush=True)

    def now(self) -> float:
        return time.perf_counter()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def secret(self, prompt: str) -> str:
        import getpass
        return getpass.getpass(prompt)

    def line(self, prompt: str) -> tuple[str, list[float], bool]:
        """(text, time of each keystroke, whether the keystrokes could be timed)."""
        try:
            return (*self._timed(prompt), True)
        except (KeyboardInterrupt, EOFError):
            raise
        except Exception:               # an unusual console: take the line untimed and say so on the certificate
            return input(prompt), [], False

    def _timed(self, prompt: str) -> tuple[str, list[float]]:
        buf, stamps = [], []
        sys.stdout.write(prompt)
        sys.stdout.flush()
        if os.name == "nt":
            import msvcrt
            while True:
                ch = msvcrt.getwch()
                if ch in ("\r", "\n"):
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break
                if ch == "\x03":
                    raise KeyboardInterrupt
                if ch in ("\x00", "\xe0"):          # arrow and function keys arrive as two codes
                    msvcrt.getwch()
                    continue
                if ch == "\b":
                    if buf:
                        buf.pop()
                        stamps.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue
                if ch < " ":
                    continue
                buf.append(ch)
                stamps.append(time.perf_counter())
                sys.stdout.write(ch)
                sys.stdout.flush()
            return "".join(buf), stamps
        import codecs
        import termios
        import tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        dec = codecs.getincrementaldecoder("utf-8")("replace")
        escape = False
        try:
            tty.setcbreak(fd)
            while True:
                b = os.read(fd, 1)
                if not b:
                    raise EOFError
                ch = dec.decode(b)
                if not ch:
                    continue
                if escape:                          # swallow an escape sequence (arrow keys and the like)
                    escape = not (ch.isalpha() or ch == "~")
                    continue
                if ch in "\r\n":
                    sys.stdout.write("\n")
                    sys.stdout.flush()
                    break
                if ch == "\x03":
                    raise KeyboardInterrupt
                if ch == "\x04":
                    raise EOFError
                if ch == "\x1b":
                    escape = True
                    continue
                if ch in ("\x7f", "\b"):
                    if buf:
                        buf.pop()
                        stamps.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue
                if ch < " ":
                    continue
                buf.append(ch)
                stamps.append(time.perf_counter())
                sys.stdout.write(ch)
                sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return "".join(buf), stamps


def _same(a: str, b: str) -> bool:
    """The same wording, or the same with a word or two changed."""
    n = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    return bool(n(a)) and bool(n(b)) and difflib.SequenceMatcher(None, n(a), n(b)).ratio() >= 0.9


def hand_typed(con, prompt: str, min_words: int = 0, forbid: tuple = ()) -> dict:
    """One answer typed by hand.  Paste, too few words and the draft's own wording are refused."""
    while True:
        con.say(prompt)
        text, stamps, timed = con.line("> ")
        text = " ".join(text.split())
        if timed and looks_pasted(stamps):
            con.say("That arrived faster than anyone types. Paste is not accepted here; type it by hand.")
            continue
        if len(text.split()) < min_words:
            con.say(f"At least {min_words} words, please.")
            continue
        if any(_same(text, f) for f in forbid):
            con.say("That is the draft's wording. Type it in your own words.")
            continue
        return {"text": text, "keystrokes": len(stamps),
                "seconds": round(stamps[-1] - stamps[0], 1) if len(stamps) > 1 else 0, "timed": timed, "at": utcnow()}


def accept(con, phrase: str, also: tuple = ()) -> str:
    """The person types `phrase` exactly (or one of `also`).  Typing CHANGE stops without signing."""
    while True:
        text, stamps, timed = con.line("> ")
        text = " ".join(text.split())
        if text.upper() == "CHANGE":
            raise Changed()
        if timed and looks_pasted(stamps):
            con.say("Type it by hand.")
            continue
        for p in (phrase, *also):
            if text.lower() == p.lower():
                return p
        con.say(f"Type exactly: {phrase}" + (f"   (or: {', '.join(also)})" if also else "") + "   (or CHANGE to stop)")


def _show(con, text: str, indent: str = "    ") -> None:
    for para in str(text).split("\n"):
        con.say(textwrap.fill(para, width=96, initial_indent=indent, subsequent_indent=indent) if para.strip() else "")


def read_check(con, label: str, text: str) -> dict:
    """The person reads `text`: a minimum time on screen, two missing-word questions, and a typed
    statement that they read it."""
    words = text.split()
    need = max(5.0, len(words) / 5.0)                      # 300 words a minute is fast reading
    con.say("")
    con.say(f"--- {label}, as it will stand in the header. Read it. ---")
    _show(con, text)
    start = con.now()
    con.line("Press Enter when you have read it. ")
    waited = con.now() - start
    if waited < need:
        con.say(f"That was {waited:.0f} seconds for {len(words)} words. Read it; the next question opens in "
                f"{need - waited:.0f} seconds.")
        con.sleep(need - waited)
    candidates = [i for i, w in enumerate(words) if i >= 1 and len(re.sub(r"\W", "", w)) >= 5
                  and re.sub(r"\W", "", w).isalpha()]
    picks, blanks = [], []
    seed = int(sha256_text(text)[:8], 16)
    while candidates and len(picks) < 2:
        i = candidates.pop(seed % len(candidates))
        seed = seed * 31 + 7
        if all(abs(i - j) > 4 for j in picks):
            picks.append(i)
    for i in sorted(picks):
        answer = re.sub(r"\W", "", words[i])
        around = " ".join(words[max(0, i - 5):i] + ["_____"] + words[i + 1:i + 5])
        while True:
            con.say(f"Which word is missing?   ... {around} ...")
            got, _, _ = con.line("> ")
            if re.sub(r"\W", "", got).lower() == answer.lower():
                break
            con.say("That is not the word. It is in the text above.")
        blanks.append(answer)
    phrase = f"I have read {label}"
    con.say(f"Type: {phrase}")
    accept(con, phrase)
    return {"label": label, "words": len(words), "seconds_on_screen": round(max(waited, need), 1), "blanks": blanks}


# --------------------------------------------------------------------------- #
# The header: axis blocks and their hypothesis statements.

def _norm(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _configured(project: Path) -> dict[str, Path]:
    """Where the project keeps its header, index and Archivist prompt."""
    from .config import load_config, resolve_path
    cfg = load_config(project)
    return {k: resolve_path(cfg, cfg["frame"].get(f"{k}_file") or d)
            for k, d in (("header", "01_FRAME/header.md"), ("index", "01_FRAME/index.md"),
                         ("archivist_prompt", "01_FRAME/archivist-custom-prompt.txt"))}


def header_path(project: Path) -> Path:
    return _configured(Path(project))["header"]


def axis_spans(text: str) -> dict[str, tuple[int, int]]:
    """{axis id: (start, end)} of each axis block, found the way the header parser finds them."""
    from .header import _sections
    word_num = {"one": 1, "two": 2, "three": 3, "four": 4, "1": 1, "2": 2, "3": 3, "4": 4}
    heads = [(s, e, h) for lvl, h, s, e in _sections(text) if re.search(r"\baxis\b", h, re.I)]
    out = {}
    for s, e, h in heads:
        m = re.search(r"axis\s*(one|two|three|four|\d)", h, re.I)
        if m:
            nxt = [s2 for s2, _, _ in heads if s2 > s]
            out[f"A{word_num[m.group(1).lower()]}"] = (s, min(nxt) if nxt else e)
    return out


def block_sha(text: str, axis_id: str) -> str:
    spans = axis_spans(text)
    if axis_id not in spans:
        return ""
    s, e = spans[axis_id]
    return sha256_text(text[s:e].strip())


def replace_axis(text: str, axis_id: str, question: str, statements: dict[str, str]) -> str:
    """The header with this axis's question and hypothesis statements replaced.  Nothing else moves."""
    text = _norm(text)
    spans = axis_spans(text)
    if axis_id not in spans:
        raise ValueError(f"the header has no block for axis {axis_id}")
    s, e = spans[axis_id]
    lines = text[s:e].split("\n")
    cell = lambda t: " ".join(str(t).split()).replace("|", "\\|")
    i = 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    j = i
    while j < len(lines) and lines[j].strip():
        j += 1
    if i >= len(lines):
        raise ValueError(f"axis {axis_id} has no question paragraph")
    lines[i:j] = [" ".join(question.split())]
    for hid, st in statements.items():
        pat = re.compile(r"^\s*\|\s*\**\s*" + re.escape(hid) + r"\s*\**\s*\|")
        rows = [k for k, ln in enumerate(lines) if pat.match(ln)]
        if not rows:
            raise ValueError(f"the header has no table row for {hid}")
        lines[rows[0]] = f"| **{hid}** | {cell(st)} |"
    return text[:s] + "\n".join(lines) + text[e:]


# --------------------------------------------------------------------------- #
# What the forecasts read: the index, and findings from an earlier run when there is one.

def index_digest(project: Path, axis_id: str, cap: int = 60_000) -> str:
    path = Path(project) / "01_FRAME" / "index.md"
    if not path.exists():
        return ""
    try:
        from .index import parse_index
        parsed = parse_index(read_text(path))
    except Exception:
        return read_text(path)[:cap]
    entries = parsed.get("entries", {})
    if not entries:
        return read_text(path)[:cap]
    mine = {f: b for f, b in entries.items() if re.search(r"\b" + re.escape(axis_id) + r"\b", b)}
    use = mine or entries
    per = max(120, min(600, cap // max(1, len(use))))
    out = [f"- ({parsed.get('ranks', {}).get(f, '?')}) {f}: " + " ".join(b.split())[:per] for f, b in use.items()]
    return "\n".join(out)[:cap]


def frd_digest(project: Path, axis_id: str, cap: int = 70_000) -> tuple[str, str]:
    """(findings text, where it came from) from the newest run that holds validated FRDs for the axis."""
    runs = Path(project) / "02_RUNS"
    found = []
    if runs.is_dir():
        for p in list(runs.glob(f"*/AXIS-{axis_id}__*/03_FRDS/05_validated/retained-frds.json")) + \
                list(runs.glob("*/03_FRDS/05_validated/retained-frds.json")):
            if p.stat().st_size > 10:
                found.append(p)
    if not found:
        return "", ""
    best = max(found, key=lambda p: p.stat().st_mtime)
    rows = [r for r in (read_json(best, default=[]) or []) if isinstance(r, dict) and r.get("claim")]
    if not rows:
        return "", ""
    per = max(120, min(320, cap // len(rows)))
    text = "\n".join(f"- [{r.get('source_file', '?')}] " + " ".join(str(r["claim"]).split())[:per] for r in rows)
    return text[:cap], f"{len(rows)} validated findings from {best.relative_to(runs).parts[0]}"


# --------------------------------------------------------------------------- #
# The model's part.  `model(tag, system, user, salt)` returns a parsed JSON object or raises.

SYSTEM = ("You help a researcher fix the frame of an Analysis of Competing Hypotheses (ACH) run before any evidence "
          "is scored. The frame decides what the run can find. Be exact and plain. Return one JSON object and "
          "nothing else.")


def _frame_text(question: str, statements: dict[str, str]) -> str:
    return "QUESTION: " + question + "\n" + "\n".join(f"{h}: {s}" for h, s in statements.items())


def forecast(model, question: str, statements: dict[str, str], gauge: int, evidence: str, tag: str) -> dict:
    """Three independent forecasts of how the gauge would be divided among these hypotheses as worded."""
    ids = list(statements)
    user = (_frame_text(question, statements) + f"\n\nGAUGE: {gauge} units, divided among the hypotheses.\n\n"
            "EVIDENCE AVAILABLE TO THE RUN\n" + (evidence or "(no index or findings were supplied)") +
            "\n\nTASK: forecast how an evidence-level ACH assessment of this corpus would divide the gauge among "
            "these hypotheses exactly as they are worded. A weaker claim is easier to support; a claim the corpus "
            "cannot test belongs to the undecided hypothesis. Return "
            '{"allocations": {' + ", ".join(f'"{i}": 0' for i in ids) + '}, "why": "one or two sentences"} '
            f"with non-negative integers that sum to {gauge}.")

    def one(n):
        try:
            got = model(f"forecast:{tag}:{n}", SYSTEM, user, f"forecast-{n}")
            alloc = {i: int(got["allocations"][i]) for i in ids}
            if sum(alloc.values()) != gauge or min(alloc.values()) < 0:
                raise ValueError(f"allocations do not sum to {gauge}")
            return {"allocations": alloc, "why": " ".join(str(got.get("why", "")).split())[:400]}
        except Exception as e:
            return {"error": f"{type(e).__name__}: {e}"[:200]}

    with ThreadPoolExecutor(max_workers=FORECAST_CALLS) as pool:
        calls = list(pool.map(one, range(1, FORECAST_CALLS + 1)))
    good = [c["allocations"] for c in calls if "allocations" in c]
    out = {"calls": calls, "ok": len(good)}
    if good:
        out["mean"] = {i: round(sum(g[i] for g in good) / len(good)) for i in ids}
        out["low"] = {i: min(g[i] for g in good) for i in ids}
        out["high"] = {i: max(g[i] for g in good) for i in ids}
    return out


def ladder(model, intent: str, concede: str, preferred: str, question: str, statements: dict[str, str],
           evidence: str) -> list[dict]:
    ids = list(statements)
    user = ("WHAT THE RESEARCHER WANTS TO BE ABLE TO SAY: " + intent + "\nWHAT THEY WOULD CONCEDE IF THEY LOSE: "
            + concede + f"\nTHE HYPOTHESIS THEY WANT TO WIN: {preferred}\n\nTHE DRAFT FRAME\n"
            + _frame_text(question, statements) + "\n\nEVIDENCE AVAILABLE TO THE RUN\n" + evidence +
            "\n\nTASK: write three alternative frames for this axis, ordered from the strongest claim to the "
            f"weakest. Each must serve what the researcher wants to say, keep the hypothesis ids {', '.join(ids)}, "
            f"and keep {preferred} as the hypothesis they want to win. Do not write a frame the corpus cannot test. "
            'Return {"rungs": [{"label": "six words at most", "question": "...", "statements": {'
            + ", ".join(f'"{i}": "..."' for i in ids) + '}, "win_lets_you_say": "one sentence: what a win for '
            + preferred + ' would let the researcher say", "leaves_out": "one sentence: what this frame leaves '
            'outside the question"}]}.')
    got = model("ladder", SYSTEM, user, "")
    rungs = []
    for r in (got.get("rungs") or [])[:4]:
        st = r.get("statements") or {}
        if isinstance(r, dict) and all(str(st.get(i, "")).strip() for i in ids) and str(r.get("question", "")).strip():
            rungs.append({"label": " ".join(str(r.get("label", "")).split())[:60] or "alternative",
                          "question": " ".join(str(r["question"]).split()),
                          "statements": {i: " ".join(str(st[i]).split()) for i in ids},
                          "win_lets_you_say": " ".join(str(r.get("win_lets_you_say", "")).split()),
                          "leaves_out": " ".join(str(r.get("leaves_out", "")).split())})
    if not rungs:
        raise ValueError("no alternative frames came back")
    return rungs


def restate(model, intent: str, question: str, statements: dict[str, str], evidence: str) -> dict:
    ids = list(statements)
    user = ("WHAT THE RESEARCHER WANTS TO BE ABLE TO SAY: " + intent + "\n\nTHE FRAME AS THE RESEARCHER TYPED IT\n"
            + _frame_text(question, statements) + "\n\nEVIDENCE AVAILABLE TO THE RUN\n" + evidence +
            "\n\nTASK: restate the question and each hypothesis so that the grammar is correct and each statement "
            "can be tested against this corpus: name the population, the intervention, the comparison and the "
            "outcome wherever the researcher implied them. Keep the researcher's meaning. Do not make any claim "
            "stronger or weaker. Do not add a condition the researcher did not state unless the statement cannot "
            "be tested without it, and list every such addition. Each statement must be longer than 30 characters. "
            'Return {"question": "...", "statements": {' + ", ".join(f'"{i}": "..."' for i in ids) +
            '}, "changes": ["each thing you changed or added, and why"], "cannot_be_tested": ["any term or claim '
            'in the researcher\'s wording that this corpus cannot test"]}.')
    got = model("restate", SYSTEM, user, "")
    st = got.get("statements") or {}
    if not all(len(" ".join(str(st.get(i, "")).split())) > 30 for i in ids) or not str(got.get("question", "")).strip():
        raise ValueError("the restatement did not return every hypothesis")
    strs = lambda v: [" ".join(str(x).split()) for x in (v or []) if str(x).strip()][:12]
    return {"question": " ".join(str(got["question"]).split()),
            "statements": {i: " ".join(str(st[i]).split()) for i in ids},
            "changes": strs(got.get("changes")), "cannot_be_tested": strs(got.get("cannot_be_tested"))}


def back_translate(model, block: str, preferred: str, fc: dict, gauge: int) -> dict:
    """A reading of the finished axis text by a model that has not seen what the researcher wants."""
    user = ("THE AXIS AS IT WILL STAND IN THE HEADER\n" + block + "\n\nFORECASTS OF THE RESULT (units of "
            f"{gauge}): " + canonical_json([c.get("allocations", c) for c in fc.get("calls", [])]) +
            f"\n\nThe researcher wants {preferred} to win. You have not been told why. TASK: say what this frame "
            "does. Guess the worst result the researcher could plausibly get from this corpus, not the average. "
            'Return {"if_it_wins_you_may_say": ["plain claims a win for ' + preferred + ' would support"], '
            '"you_may_not_say": ["claims a reader might expect that a win would NOT support"], '
            '"worst_case": {"allocations": {"<id>": 0}, "then_you_would_have_to_say": "one sentence"}, '
            '"rival_is_held_by": "who really holds the main rival hypothesis as worded, or the words: no '
            'identifiable holder", "a_critic_will_say": ["the strongest objections to this frame"], '
            '"left_out": ["relevant matters this frame puts outside the question"], '
            '"conflicts": ["places where the boundary, cohort or supporting text of the axis contradicts the '
            'hypothesis statements; empty if none"]}.')
    got = model("back-translate", SYSTEM, user, "")
    strs = lambda v: [" ".join(str(x).split()) for x in (v or []) if str(x).strip()][:8]
    wc = got.get("worst_case") or {}
    if not strs(got.get("if_it_wins_you_may_say")):
        raise ValueError("no reading of the frame came back")
    alloc = {}
    try:
        alloc = {str(k): int(v) for k, v in (wc.get("allocations") or {}).items()}
    except Exception:
        alloc = {}
    return {"if_it_wins_you_may_say": strs(got.get("if_it_wins_you_may_say")),
            "you_may_not_say": strs(got.get("you_may_not_say")),
            "worst_case": {"allocations": alloc,
                           "then_you_would_have_to_say": " ".join(str(wc.get("then_you_would_have_to_say", "")).split())},
            "rival_is_held_by": " ".join(str(got.get("rival_is_held_by", "")).split()),
            "a_critic_will_say": strs(got.get("a_critic_will_say")), "left_out": strs(got.get("left_out")),
            "conflicts": strs(got.get("conflicts"))}


def judge(model, intent: str, may_say: list[str]) -> dict:
    user = ("WHAT THE RESEARCHER WANTS TO BE ABLE TO SAY: " + intent + "\n\nWHAT A WIN UNDER THE FRAME WOULD LET "
            "THEM SAY:\n" + "\n".join(f"- {s}" for s in may_say) + "\n\nTASK: would a win let the researcher say "
            'what they want to say? Return {"match": true or false, "gap": "one sentence naming the difference, '
            'or an empty string"}.')
    got = model("judge", SYSTEM, user, "")
    return {"match": bool(got.get("match")), "gap": " ".join(str(got.get("gap", "")).split())}


# --------------------------------------------------------------------------- #
# One axis, start to finish.

def _fc_line(fc: dict, hid: str, gauge: int) -> str:
    if not fc.get("ok"):
        return "no forecast (the model did not answer)"
    spread = sorted(c["allocations"][hid] for c in fc["calls"] if "allocations" in c)
    return f"{fc['mean'][hid]} of {gauge}   (calls: {', '.join(str(x) for x in spread)})"


def certify_axis(con, model, project: Path, text: str, axis: dict, gauge: int, prior: dict | None = None) -> tuple[str, dict]:
    """Take one axis through the gate.  Returns the header text with the signed wording, and the record.
    `prior` is this person's earlier signed record of the axis, if any: wording that is already their
    own may be typed again; a draft's wording may not."""
    aid = axis["axis_id"]
    ids = [h["id"] for h in axis["hypotheses"]]
    draft = {h["id"]: h["statement"] for h in axis["hypotheses"]}
    was = (prior or {}).get("restated") or {}
    not_mine = lambda now, before: () if before and _same(now, before) else (now,)
    target = math.ceil(TARGET_SHARE * gauge)
    steps: dict[str, str] = {}
    rec: dict = {"axis_id": aid, "name": axis.get("name", ""), "gauge": gauge, "target": target}

    def try_model(name, fn, fallback):
        try:
            out = fn()
            steps[name] = "ok"
            return out
        except Exception as e:
            steps[name] = f"failed: {type(e).__name__}: {e}"[:300]
            con.say(f"  (The model could not do this step: {steps[name]}. The certificate will say so.)")
            return fallback

    con.say("")
    con.say("=" * 96)
    con.say(f"AXIS {aid}: {axis.get('name', '')}")
    con.say("=" * 96)
    con.say("The header is the frame. What this run can find follows from the words you sign here.")
    con.say("")
    rec["intent"] = hand_typed(con, "In your own words: what do you want to be able to say when this run is done?", 8)
    rec["concede"] = hand_typed(con, "If the result goes against you, what will you concede?", 4)
    while True:
        con.say(f"Which hypothesis do you want to win? Type its id ({', '.join(ids)}).")
        got, _, _ = con.line("> ")
        if got.strip().upper() in [i.upper() for i in ids]:
            preferred = next(i for i in ids if i.upper() == got.strip().upper())
            break
    rec["preferred"] = preferred
    intent, concede = rec["intent"]["text"], rec["concede"]["text"]

    evidence = index_digest(project, aid)
    findings, basis = frd_digest(project, aid)
    if findings:
        evidence = "Source index:\n" + evidence + "\n\nFindings already validated in an earlier run:\n" + findings
    rec["forecast_basis"] = ("the source index" if evidence else "nothing: no index was found") + (f" and {basis}" if basis else "")

    con.say("")
    con.say(f"Forecasting the draft frame and alternatives ({FORECAST_CALLS} calls each). This takes a few minutes.")
    rungs = [{"label": "the draft as written", "question": axis.get("question", ""), "statements": draft,
              "win_lets_you_say": "", "leaves_out": ""}]
    rungs += try_model("ladder", lambda: ladder(model, intent, concede, preferred, axis.get("question", ""), draft, evidence), [])
    with ThreadPoolExecutor(max_workers=len(rungs)) as pool:
        made = list(pool.map(lambda nr: forecast(model, nr[1]["question"], nr[1]["statements"], gauge, evidence,
                                                 f"{aid}:rung{nr[0]}"), enumerate(rungs)))
    for r, fc0 in zip(rungs, made):
        r["forecast"] = fc0
    steps["forecast"] = "ok" if all(r["forecast"]["ok"] == FORECAST_CALLS for r in rungs) else \
        f"{sum(r['forecast']['ok'] for r in rungs)} of {FORECAST_CALLS * len(rungs)} forecast calls answered"
    rec["ladder"] = rungs
    con.say("")
    con.say(f"FORECASTS for {preferred}. Your target is {target} of {gauge}. A forecast is a guess, not a result.")
    for n, r in enumerate(rungs):
        con.say("")
        con.say(f"  [{n}] {r['label']}:  {_fc_line(r['forecast'], preferred, gauge)}")
        for hid in ids:
            _show(con, f"{hid}: {r['statements'][hid]}", "        ")
        if r["win_lets_you_say"]:
            _show(con, "A win lets you say: " + r["win_lets_you_say"], "        ")
        if r["leaves_out"]:
            _show(con, "It leaves out: " + r["leaves_out"], "        ")
    scored = [r for r in rungs if r["forecast"].get("ok")]
    best = max(scored, key=lambda r: r["forecast"]["mean"][preferred]) if scored else None
    if best:
        con.say("")
        con.say(f"If you want {preferred} to be preferred, the best of these is \"{best['label']}\" "
                f"({best['forecast']['mean'][preferred]} of {gauge}).")

    while True:
        con.say("")
        con.say("Now type the question and each hypothesis in your own words. Paste is refused, and so is the "
                "draft's own wording. You may follow any of the frames above.")
        typed_q = hand_typed(con, f"The question for axis {aid}:", 6,
                             forbid=not_mine(axis.get("question", ""), was.get("question", "")))
        typed = {hid: hand_typed(con, f"{hid}" + (" (the one you want to win)" if hid == preferred else "") + ":", 6,
                                 forbid=not_mine(draft[hid], (was.get("statements") or {}).get(hid, ""))) for hid in ids}
        mine = {h: t["text"] for h, t in typed.items()}
        con.say("")
        con.say("Restating your wording against the source index, then forecasting it. This takes a few minutes.")
        rs = try_model("restate", lambda: restate(model, intent, typed_q["text"], mine, evidence),
                       {"question": typed_q["text"], "statements": mine, "changes": [], "cannot_be_tested": [],
                        "not_restated": True})
        try:
            new_text = replace_axis(text, aid, rs["question"], rs["statements"])
            from .header import parse_header
            got_ids = [h["id"] for a in parse_header(new_text)["axes"] if a["axis_id"] == aid for h in a["hypotheses"]
                       if h["statement"]]
            if got_ids != ids:
                raise ValueError("a statement is too short for the header (30 characters at least)")
        except ValueError as e:
            con.say(f"That wording cannot go into the header: {e}. Type it again.")
            continue
        fc = forecast(model, rs["question"], rs["statements"], gauge, evidence, f"{aid}:final")
        con.say("")
        con.say("YOUR FRAME, RESTATED so that this corpus can test it:")
        _show(con, "Question: " + rs["question"])
        for hid in ids:
            _show(con, f"{hid}: {rs['statements'][hid]}")
        for c in rs["changes"]:
            _show(con, "Changed: " + c, "      ")
        for c in rs["cannot_be_tested"]:
            _show(con, "This corpus cannot test: " + c, "      ")
        con.say("")
        con.say(f"FORECAST for {preferred} under your wording: {_fc_line(fc, preferred, gauge)}. Target: {target}.")
        mean = fc["mean"][preferred] if fc.get("ok") else None
        if best and mean is not None and best["forecast"]["mean"][preferred] > mean:
            con.say(f"Are you sure you are OK with this wording? If you want {preferred} to be preferred, "
                    f"\"{best['label']}\" is the better choice: {best['forecast']['mean'][preferred]} of {gauge} "
                    f"against {mean} for yours." + (f" It leaves out: {best['leaves_out']}" if best["leaves_out"] else ""))
        elif mean is not None and mean < target:
            con.say(f"Are you sure you are OK with this wording? It is forecast below your target of {target}.")
        con.say("Type KEEP to go on with your wording, or RETYPE to type it again.")
        if accept(con, "KEEP", also=("RETYPE",)) == "KEEP":
            break
    rec.update({"typed": {"question": typed_q, "statements": typed}, "restated": rs, "forecast": fc})

    # While the person reads, a model that has not been told what they want reads the finished axis.
    s, e = axis_spans(new_text)[aid]
    block = new_text[s:e]
    reader = ThreadPoolExecutor(max_workers=1)
    reading = reader.submit(back_translate, model, block, preferred, fc, gauge)
    reader.shutdown(wait=False)

    # what the assessor is given for each hypothesis: the statement and the three paragraphs under it
    under = {h["id"]: "\n".join(f"{label}: {h[k]}" for k, label in (("assumptions", "Assumptions and antecedents"),
                                                                    ("falsification", "Potential falsification"),
                                                                    ("corroboration", "Potential corroboration")) if h.get(k))
             for h in axis["hypotheses"]}
    rec["read"] = [read_check(con, hid, rs["statements"][hid] + ("\n" + under[hid] if under[hid] else "")) for hid in ids]
    limits = "\n".join(x for x in (("Governing boundary. " + axis["boundary"]) if axis.get("boundary") else "",
                                   ("Cohort: " + axis["scope"]) if axis.get("scope") else "") if x)
    if limits:
        con.say("")
        con.say("The header also limits this axis. These limits are part of what you sign.")
        rec["read"].append(read_check(con, f"the limits of {aid}", limits))

    empty = {"if_it_wins_you_may_say": [], "you_may_not_say": [], "worst_case": {"allocations": {}, "then_you_would_have_to_say": ""},
             "rival_is_held_by": "", "a_critic_will_say": [], "left_out": [], "conflicts": []}
    if not reading.done():
        con.say("")
        con.say("A model that has not been told what you want is reading the finished axis, to say what this frame "
                "does and to guess the worst result. One moment.")
    bt = try_model("back_translate", reading.result, empty)
    jd = try_model("judge", lambda: judge(model, intent, bt["if_it_wins_you_may_say"]), {"match": None, "gap": ""}) \
        if bt["if_it_wins_you_may_say"] else {"match": None, "gap": ""}
    rec.update({"back_translation": bt, "judge": jd})

    con.say("")
    con.say("=" * 96)
    con.say("THE CONSEQUENCES OF THIS FRAME. Accept each one by typing it, or type CHANGE to stop without signing.")
    con.say("=" * 96)
    accepted = []

    def item(title, lines, phrase):
        con.say("")
        con.say(f"{len(accepted) + 1}. {title}")
        for ln in lines:
            _show(con, ln)
        con.say(f"Type: {phrase}")
        accept(con, phrase)
        accepted.append({"item": title, "shown": lines, "typed": phrase, "at": utcnow()})

    if mean is None:
        item("THE FORECAST", ["No forecast could be made. You are signing without one."], "I accept no forecast")
    else:
        lines = [f"{preferred} is forecast at {mean} of {gauge}. The calls gave " +
                 ", ".join(str(c["allocations"][preferred]) for c in fc["calls"] if "allocations" in c) +
                 f". Your target is {target}. Basis: {rec['forecast_basis']}."]
        if mean < target:
            lines.append("That is BELOW your target. If the run agrees with the forecast, you will not get the result you want.")
        item("THE FORECAST", lines, f"I accept {mean} of {gauge}")
    wc = bt["worst_case"]
    item("THE WORST LIKELY RESULT",
         [("The worst likely result is " + ", ".join(f"{k} {v}" for k, v in wc["allocations"].items()) + ".")
          if wc["allocations"] else "The model gave no worst case. The run can still go against you.",
          "Then you would have to say: " + (wc["then_you_would_have_to_say"] or concede),
          "You said you would concede: " + concede], "I accept the worst case")
    lines = ["You want to be able to say: " + intent]
    lines += ["A win lets you say: " + x for x in bt["if_it_wins_you_may_say"]] or ["(The model did not say what a win would mean.)"]
    lines += ["A win does NOT let you say: " + x for x in bt["you_may_not_say"]]
    if jd["match"] is False:
        lines.append("WARNING. A win would not let you say what you want to say: " + jd["gap"])
    item("WHAT A WIN MEANS", lines, "I accept what a win means")
    held = bt["rival_is_held_by"]
    lines = ["The main rival is held by: " + (held or "(the model did not say)")]
    if re.search(r"no identifiable holder", held, re.I):
        lines.append("Nobody holds the rival as you worded it. A critic will call it a strawman, and the certificate says so.")
    item("THE RIVAL YOU ARE TESTING AGAINST", lines, "I accept the rival")
    item("WHAT THIS FRAME LEAVES OUT, AND WHAT A CRITIC WILL SAY",
         ["Left out: " + x for x in bt["left_out"]] + ["A critic will say: " + x for x in bt["a_critic_will_say"]]
         or ["(The model named nothing.)"], "I accept what is left out")
    if bt["conflicts"]:
        item("THE REST OF THE AXIS TEXT DISAGREES WITH YOUR WORDING",
             bt["conflicts"] + ["To have these fixed, type CHANGE, have the header corrected, and run this again."],
             "I accept the conflicts")
    rec.update({"accepted": accepted, "model_steps": steps, "certified": utcnow(), "block_sha256": block_sha(new_text, aid)})
    return new_text, rec


# --------------------------------------------------------------------------- #
# The certificate.

def _frame_files(project: Path) -> dict[str, str]:
    """Every file besides the header that shapes the result: the source index, the Archivist prompt,
    the matcher's fixtures, any prompt the project overrides, the settings that exclude sources or
    set gates, and the rule files of any domain module the project turns on."""
    project = Path(project)
    where = _configured(project)
    files = [where["index"], where["archivist_prompt"], project / "01_FRAME" / "match-fixtures.json"]
    over = project / "90_METHOD" / "prompts"
    if over.is_dir():
        files += sorted(p for p in over.rglob("*") if p.is_file())
    digest = lambda p: hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    out = {}
    for p in files:
        if p and p.exists():
            try:
                key = p.resolve().relative_to(project.resolve()).as_posix()
            except ValueError:
                key = str(p)
            out[key] = digest(p)
    cfg = read_json(project / "project.json", default={}) or {}
    for key in ("domain_modules", "frd_assess", "corpus"):
        if key in cfg:
            out[f"project.json#{key}"] = sha256_text(canonical_json(cfg[key]))
    for name in sorted(cfg.get("domain_modules") or {}):
        d = Path(__file__).resolve().parent / "domains" / str(name)
        if d.is_dir():
            for p in sorted(d.iterdir()):
                if p.is_file() and p.suffix in (".md", ".py", ".json"):
                    out[f"claimreg/domains/{name}/{p.name}"] = digest(p)
    return out


def _body(cert: dict) -> bytes:
    return canonical_json({k: v for k, v in cert.items() if k != "signature"}).encode("utf-8")


def load_certificate(project: Path) -> dict | None:
    try:
        c = read_json(Path(project) / "01_FRAME" / CERT_JSON, default=None)
    except ValueError:
        return None
    return c if isinstance(c, dict) else None


def _unsigned_axes(text: str, cert: dict) -> list[str]:
    """Axes of the header that the certificate does not cover as they now stand."""
    from .header import parse_header
    try:
        ids = [a["axis_id"] for a in parse_header(text)["axes"]]
    except ValueError:
        ids = list(axis_spans(text))
    axes = cert.get("axes") or {}
    return [a for a in ids if not axes.get(a, {}).get("block_sha256") or axes[a]["block_sha256"] != block_sha(text, a)]


def verify(project: Path, signer_file: Path | None = None) -> tuple[bool, str]:
    """(valid, reason).  Valid means: a certificate signed by this computer's signer covers the header
    exactly as it stands, every axis in it, and every other file that shapes the result."""
    project = Path(project)
    hp = header_path(project)
    if not hp.exists():
        return False, f"there is no header ({hp.name})"
    if (project / "01_FRAME" / "frame.json").exists():
        return False, "01_FRAME/frame.json overrides the header; remove it so that the signed header governs"
    cert = load_certificate(project)
    if not cert:
        return False, "nobody has signed the frame (there is no frame certificate)"
    signer = load_signer(signer_file)
    if not signer:
        return False, "this computer has no signer; run `cr signer`"
    pub = str((cert.get("signer") or {}).get("public_key", ""))
    if pub != signer["public_key"]:
        return False, "the frame certificate was not signed by this computer's signer"
    try:
        good = ed_verify(bytes.fromhex(pub), _body(cert), bytes.fromhex(str(cert.get("signature", ""))))
    except ValueError:
        good = False
    if not good:
        return False, "the frame certificate's signature is not valid (the certificate was edited after signing)"
    text = _norm(read_text(hp))
    unsigned = _unsigned_axes(text, cert)
    never = [a for a in unsigned if a not in (cert.get("axes") or {})]
    if never:
        return False, "nobody has signed axis " + ", ".join(never)
    if unsigned:
        return False, "the wording of axis " + ", ".join(unsigned) + " changed after it was signed"
    if sha256_text(text) != cert.get("header_sha256"):
        return False, "the header changed after it was signed (outside the axes)"
    now, then = _frame_files(project), cert.get("frame_files") or {}
    drift = sorted(k for k in set(now) | set(then) if now.get(k) != then.get(k))
    if drift:
        return False, "changed since signing: " + ", ".join(drift[:6]) + (" ..." if len(drift) > 6 else "")
    return True, (f"frame signed by {cert['signer'].get('name', '?')} on {str(cert.get('signed', ''))[:10]} "
                  f"(signer {cert['signer'].get('fingerprint', '?')})")


def locked() -> bool:
    return LOCK_FILE.exists()


def lock(signer: dict) -> None:
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(LOCK_FILE, f"The frame gate was locked on {utcnow()} after the first complete signing by "
                                 f"{signer.get('name', '?')} (signer {fingerprint(signer['public_key'])}).\n")


def gate(project: Path, action: str) -> tuple[bool, str]:
    """(may proceed, message).  Once the gate is locked, nothing runs on a frame that is not signed."""
    ok, why = verify(project)
    if ok:
        return True, why
    if not locked():
        return True, ("=" * 96 + f"\nFRAME GATE NOT YET LOCKED. Nobody has completed a signing on this computer.\n"
                      f"Once someone has, this {action} would be refused: {why}.\n"
                      f"Sign the frame:  cr sign \"{project}\"\n" + "=" * 96)
    return False, (f"{action} refused: {why}.\nA person must sign the frame first:  cr sign \"{project}\"\n"
                   "There is no override.")


def uses_models(cfg: dict) -> bool:
    """True when any role is routed to something other than the offline engine or a test stand-in."""
    for v in (cfg.get("roles") or {}).values():
        for n in ([v] if isinstance(v, str) else list(v or [])):
            if (cfg.get("providers") or {}).get(n, {}).get("type", n) not in ("local", "mock", "replay"):
                return True
    return False


def render(cert: dict) -> str:
    s = cert.get("signer") or {}
    out = ["# Frame certificate", "",
           f"Signed by **{s.get('name', '?')}** on {str(cert.get('signed', ''))[:10]} (signer {s.get('fingerprint', '?')}).",
           "", "The header is the frame, and the frame decides what a run can find. This page records what the "
           "signer typed, read and accepted before any evidence was scored. A different frame can be scored on "
           "the same evidence; this is the one the signer chose.", ""]
    cell = lambda t: " ".join(str(t).split()).replace("|", "\\|")
    for aid, r in (cert.get("axes") or {}).items():
        g, pref = r.get("gauge", 64), r.get("preferred", "")
        fc = r.get("forecast") or {}
        out += [f"## Axis {aid}: {r.get('name', '')}", "",
                f"- **Wants to be able to say:** {r['intent']['text']}",
                f"- **Would concede:** {r['concede']['text']}",
                f"- **Wants to win:** {pref}", ""]
        out += ["### The hypotheses", "", "| | As the signer typed it | As it stands in the header |", "|---|---|---|",
                f"| Question | {cell(r['typed']['question']['text'])} | {cell(r['restated']['question'])} |"]
        out += [f"| {h} | {cell(t['text'])} | {cell(r['restated']['statements'][h])} |" for h, t in r["typed"]["statements"].items()]
        out.append("")
        for c in r["restated"].get("changes", []):
            out.append(f"- Changed in restating: {c}")
        for c in r["restated"].get("cannot_be_tested", []):
            out.append(f"- This corpus cannot test: {c}")
        if r["restated"].get("not_restated"):
            out.append("- The model did not restate the wording; the header carries what the signer typed.")
        out += ["", "### Forecast", ""]
        if fc.get("ok"):
            out.append(f"{pref} was forecast at **{fc['mean'][pref]} of {g}** (calls: " +
                       ", ".join(str(c["allocations"][pref]) for c in fc["calls"] if "allocations" in c) +
                       f"; target {r.get('target')}). Basis: {r.get('forecast_basis', '')}. A forecast is a guess, not a result.")
        else:
            out.append("No forecast could be made.")
        out += ["", "| Frame considered | Forecast for " + pref + " | Leaves out |", "|---|---|---|"]
        for rung in r.get("ladder", []):
            f = rung.get("forecast") or {}
            out.append(f"| {cell(rung['label'])} | {f['mean'][pref] if f.get('ok') else 'none'} | {cell(rung.get('leaves_out', ''))} |")
        bt = r.get("back_translation") or {}
        out += ["", "### What a win means", ""]
        out += [f"- May say: {x}" for x in bt.get("if_it_wins_you_may_say", [])]
        out += [f"- May **not** say: {x}" for x in bt.get("you_may_not_say", [])]
        if (r.get("judge") or {}).get("match") is False:
            out.append(f"- **A win would not let the signer say what they want to say:** {r['judge'].get('gap', '')}")
        wc = bt.get("worst_case") or {}
        if wc.get("allocations"):
            out.append("- Worst likely result: " + ", ".join(f"{k} {v}" for k, v in wc["allocations"].items()) +
                       f". Then the signer would have to say: {wc.get('then_you_would_have_to_say', '')}")
        out += ["", "### What the frame leaves out", ""]
        out += [f"- {x}" for x in bt.get("left_out", [])] + [f"- A critic will say: {x}" for x in bt.get("a_critic_will_say", [])]
        held = bt.get("rival_is_held_by", "")
        out.append(f"- The main rival is held by: {held or 'not stated'}" +
                   (" **(a rival nobody holds)**" if re.search("no identifiable holder", held, re.I) else ""))
        out += [f"- The axis text disagrees with the wording: {x}" for x in bt.get("conflicts", [])]
        out += ["", "### What the signer accepted, by typing it", ""]
        out += [f"- {a['item']}: \"{a['typed']}\"" for a in r.get("accepted", [])]
        out += [f"- Read {x['label']}: {x['words']} words, {x['seconds_on_screen']} seconds, {len(x['blanks'])} missing-word checks."
                for x in r.get("read", [])]
        untimed = [k for k, t in {"question": r["typed"]["question"], **r["typed"]["statements"]}.items() if not t.get("timed")]
        if untimed:
            out.append(f"- Typing could not be timed on this console for: {', '.join(untimed)}.")
        bad = {k: v for k, v in (r.get("model_steps") or {}).items() if v != "ok"}
        out += [f"- Model step `{k}`: {v}" for k, v in bad.items()]
        out.append("")
    if cert.get("unsigned_axes"):
        out += [f"**Not yet signed: axis {', '.join(cert['unsigned_axes'])}.** Nothing runs on this header until they are.", ""]
    out += ["## Locked at signature", "", f"- Header: `{cert.get('header_sha256', '')[:16]}`"]
    out += [f"- {k}: `{v[:16]}`" for k, v in (cert.get("frame_files") or {}).items()]
    for n in cert.get("resigned", []):
        out.append(f"- Signed again on {n['at'][:10]} after changes to: {', '.join(n['changed'])}")
    return "\n".join(out) + "\n"


def _unlock(con, signer: dict) -> bytes:
    """Ask for the passphrase until it matches the signer's key."""
    while True:
        seed = _seed(con.secret(f"Passphrase for {signer['name']}: "), signer["salt"])
        if ed_public(seed).hex() == signer["public_key"]:
            return seed
        con.say("That is not the passphrase.")


def _mark(text: str, name: str) -> str:
    """The parser's approval marker, set by a complete signature."""
    text = re.sub(r"<!--\s*APPROVED[:\s].*?-->\n?", "", text, flags=re.S | re.I)
    lines = text.split("\n")
    lines.insert(1 if lines and lines[0].startswith("#") else 0,
                 f"<!-- APPROVED: {name} on {utcnow()[:10]} (signed frame certificate) -->")
    return "\n".join(lines)


def _sign_and_write(project: Path, cert: dict, text: str, seed: bytes, signer: dict, crlf: bool) -> dict:
    project = Path(project)
    cert["unsigned_axes"] = [a for a in _unsigned_axes(text, cert) if a not in cert["axes"]]
    if not cert["unsigned_axes"]:
        text = _mark(text, signer["name"])          # the marker sits outside the axis blocks
    cert["header_sha256"] = sha256_text(text)
    cert["header_text"] = text
    cert["frame_files"] = _frame_files(project)
    cert["signer"] = {"name": signer["name"], "public_key": signer["public_key"], "fingerprint": fingerprint(signer["public_key"])}
    cert["signed"] = utcnow()
    cert.pop("signature", None)
    cert["signature"] = ed_sign(seed, _body(cert)).hex()
    hp = header_path(project)
    hp.parent.mkdir(parents=True, exist_ok=True)
    hp.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
    write_json(project / "01_FRAME" / CERT_JSON, cert)
    atomic_write_text(project / "01_FRAME" / CERT_MD, render(cert))
    cfg = read_json(project / "project.json", default={}) or {}
    cfg.setdefault("frame", {})["approval_note"] = (f"Frame signed by {signer['name']} on {cert['signed'][:10]} "
                                                    f"(signer {fingerprint(signer['public_key'])}).")
    write_json(project / "project.json", cfg)
    return cert


def sign_frame(con, model, project: Path, header: Path | None = None, only: str | None = None,
               signer_file: Path | None = None) -> dict:
    """Take every unsigned axis (or `only`) through the gate.  Each axis is signed as it is finished."""
    from .header import normalize_hypothesis_ids, parse_header
    project = Path(project)
    signer = load_signer(signer_file)
    if not signer:
        raise ValueError("this computer has no signer yet; run `cr signer --name \"Your Name\"` first")
    src = Path(header) if header else header_path(project)
    if not src.exists():
        raise ValueError(f"there is no header to sign: {src}")
    if (project / "01_FRAME" / "frame.json").exists():
        raise ValueError("01_FRAME/frame.json overrides the header; remove it so that the signed header governs")
    where = _configured(project)
    if not where["index"].exists():
        raise ValueError(f"there is no source index ({where['index'].name}); the forecasts and the restatement are made "
                         "against it. Run `cr frame` first")
    raw = read_text(src)
    crlf = "\r\n" in raw
    text, _ = normalize_hypothesis_ids(_norm(raw))
    frame = parse_header(text)
    order = [a["axis_id"] for a in frame["axes"]]
    headless = [a for a in order if a not in axis_spans(text)]
    if headless:
        raise ValueError(f"the header has no \"Axis ...\" heading for {', '.join(headless)}; each axis needs its own "
                         "heading so that it can be signed")
    short = [h["id"] for a in frame["axes"] for h in a["hypotheses"] if not h["statement"]]
    if short:
        raise ValueError(f"the header's hypothesis table has no statement for {', '.join(short)}")
    old = load_certificate(project) or {}
    if old and (old.get("signer") or {}).get("public_key") != signer["public_key"]:
        old = {}                                     # another signer's certificate carries nothing over
    before = old.get("axes") or {}
    axes = {a: r for a, r in before.items() if a in order and a != only and r.get("block_sha256") == block_sha(text, a)}
    todo = [a for a in order if (a == only if only else a not in axes)]
    if only and not todo:
        raise ValueError(f"the header has no axis {only}")
    if not todo:
        raise ValueError("every axis is already signed and unchanged; use `cr sign --resign` if other files changed")
    con.say(f"Signing the frame of {project.name} as {signer['name']} (signer {fingerprint(signer['public_key'])}).")
    con.say(f"To sign now: axis {', '.join(todo)}." + (f" Already signed and unchanged: {', '.join(axes)}." if axes else ""))
    con.say("Each axis is signed when you finish it. Ctrl+C stops; finished axes stay signed.")
    if not where["archivist_prompt"].exists():
        con.say("Note: there is no Archivist prompt file yet. When one is written it becomes part of the frame, and "
                "you will be asked to sign again (cr sign --resign).")
    cert = old
    for aid in todo:
        ax = next(a for a in parse_header(text)["axes"] if a["axis_id"] == aid)
        text, rec = certify_axis(con, model, project, text, ax, int(frame.get("gauge", 64)), prior=before.get(aid))
        axes[aid] = rec
        con.say("")
        con.say(f"Sign axis {aid} with your passphrase. Nothing is written until you do.")
        seed = _unlock(con, signer)
        cert = {"version": 1, "project": project.name, "axes": {a: axes[a] for a in order if a in axes},
                "resigned": old.get("resigned", [])}
        cert = _sign_and_write(project, cert, text, seed, signer, crlf)
        text = cert["header_text"]
        con.say(f"Axis {aid} is signed.")
    con.say("")
    con.say(f"Certificate: {project / '01_FRAME' / CERT_MD}")
    if cert["unsigned_axes"]:
        con.say(f"Still unsigned: axis {', '.join(cert['unsigned_axes'])}. Nothing runs on this header until they "
                f"are signed too:  cr sign \"{project}\"")
    return cert


def resign(con, project: Path, signer_file: Path | None = None) -> dict:
    """Sign again after something other than the axis wording changed.  The person sees what changed
    and accepts it by typing."""
    project = Path(project)
    signer = load_signer(signer_file)
    cert = load_certificate(project)
    if not signer or not cert:
        raise ValueError(f"there is nothing to sign again; run `cr sign \"{project}\"` first")
    raw = read_text(header_path(project))
    text = _norm(raw)
    moved = _unsigned_axes(text, cert)
    if moved:
        raise ValueError(f"axis {', '.join(moved)} changed or was never signed; that takes a full signing:  "
                         f"cr sign \"{project}\" --axis {moved[0]}")
    now, then = _frame_files(project), cert.get("frame_files") or {}
    changed = sorted(k for k in set(now) | set(then) if now.get(k) != then.get(k))
    if (cert.get("signer") or {}).get("public_key") != signer["public_key"]:
        changed.insert(0, f"the signer (was {(cert.get('signer') or {}).get('fingerprint', '?')}, "
                          f"now {fingerprint(signer['public_key'])})")
    if sha256_text(text) != cert.get("header_sha256"):
        changed.insert(0, "the header, outside the axes")
        diff = [ln for ln in difflib.unified_diff(str(cert.get("header_text", "")).split("\n"), text.split("\n"), lineterm="", n=0)
                if ln[:1] in "+-" and ln[:3] not in ("+++", "---")]
        con.say("The header changed outside the axes:")
        for ln in diff[:60]:
            con.say("  " + ln[:200])
    if not changed:
        raise ValueError("nothing changed since the frame was signed")
    con.say("Changed since signing:")
    for c in changed:
        con.say(f"  - {c}")
    con.say("These shape the result. To accept them as part of your frame:")
    con.say("Type: I accept the changed files")
    accept(con, "I accept the changed files")
    seed = _unlock(con, signer)
    cert.setdefault("resigned", []).append({"at": utcnow(), "changed": changed})
    cert = _sign_and_write(project, cert, text, seed, signer, "\r\n" in raw)
    con.say(f"Signed again. Certificate: {project / '01_FRAME' / CERT_MD}")
    return cert


# --------------------------------------------------------------------------- #
# Commands.

def model_for(project: Path):
    """The model the gate consults, as `model(tag, system, user, salt) -> dict`."""
    from .config import load_config
    from .llm.base import LLMRequest
    from .llm.router import LLM
    try:
        llm = LLM(load_config(project))
    except Exception as e:                           # no model is no reason to stop a person signing
        problem = f"{type(e).__name__}: {e}"

        def none(tag: str, system: str, user: str, salt: str = "") -> dict:
            raise RuntimeError(f"no model could be set up ({problem})")
        return none

    def ask(tag: str, system: str, user: str, salt: str = "") -> dict:
        resp = llm.call(LLMRequest(role=ROLE, system=system, user=user, expect_json=True, tag=f"frame_gate:{tag}", salt=salt))
        if not isinstance(resp.parsed, dict):
            raise ValueError(resp.parse_error or "the answer was not a JSON object")
        return resp.parsed
    return ask


def cmd_signer(a) -> int:
    signer = load_signer()
    if signer and not a.new:
        print(f"Signer on this computer: {signer['name']} (signer {fingerprint(signer['public_key'])}), "
              f"created {str(signer.get('created', ''))[:10]}.")
        print("The frame gate is locked: nothing runs on a frame that is not signed." if locked() else
              "The frame gate locks itself the first time a frame is fully signed on this computer.")
        return 0
    try:
        con = Terminal()
    except NotAPerson as e:
        print(f"signer: {e}", file=sys.stderr)
        return 2
    try:
        if signer:
            con.say(f"This replaces the signer {signer['name']} ({fingerprint(signer['public_key'])}). Every frame "
                    "signed with it must then be signed again (`cr sign <project> --resign`).")
            con.say("Replacing a signer takes its present passphrase. If you have forgotten it, delete this file "
                    f"yourself and run `cr signer` again: {SIGNER_FILE}")
            _unlock(con, signer)
            con.say("Type: REPLACE MY SIGNER")
            accept(con, "REPLACE MY SIGNER")
        name = " ".join((a.name or con.line("Your name, as it will stand on certificates: ")[0]).split())
        if not name:
            print("signer: a name is needed", file=sys.stderr)
            return 2
        con.say("Choose a passphrase of 8 characters or more. It is stored nowhere, and a frame cannot be signed as "
                "you without it. Keep it in your head or on paper: not in a file, and never in a chat with a model.")
        while True:
            first = con.secret("Passphrase: ")
            if len(first) < 8:
                con.say("8 characters or more.")
            elif con.secret("Again: ") != first:
                con.say("Those did not match.")
            else:
                break
    except (Changed, KeyboardInterrupt, EOFError):
        print("Stopped. No signer was created.")
        return 1
    signer = create_signer(name, first)
    con.say(f"Signer created: {name} (signer {fingerprint(signer['public_key'])}). Next:  cr sign <project>")
    return 0


def cmd_sign(a) -> int:
    project = Path(a.project).resolve()
    if a.check:
        ok, why = verify(project)
        print(("SIGNED: " if ok else "NOT SIGNED: ") + why)
        if not ok:
            print("The frame gate is locked: no quest or model-backed run will start on this project." if locked() else
                  "The frame gate is not yet locked on this computer; it locks at the first complete signing.")
        return 0 if ok else 2
    try:
        con = Terminal()
    except NotAPerson as e:
        print(f"sign: {e}", file=sys.stderr)
        return 2
    try:
        if a.resign:
            resign(con, project)
        else:
            sign_frame(con, model_for(project), project, header=Path(a.header) if a.header else None,
                       only=a.axis.upper() if a.axis else None)
    except Changed:
        con.say("Stopped. Nothing was signed. Have the header changed, then run `cr sign` again.")
        return 1
    except (KeyboardInterrupt, EOFError):
        con.say("")
        con.say("Stopped. Axes already signed stay signed; the one in progress was not.")
        return 1
    except ValueError as e:
        print(f"sign: {e}", file=sys.stderr)
        return 2
    ok, why = verify(project)
    if ok and not locked():
        lock(load_signer())
        con.say("")
        con.say("THE FRAME GATE IS NOW LOCKED ON THIS COMPUTER. From now on no quest and no model-backed run starts "
                "on a frame that is not signed, in any project. There is no override.")
    return 0
