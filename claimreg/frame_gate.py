"""The frame coach: the researcher sets the frame knowingly, with a coach in their corner.

Nobody runs an Analysis of Competing Hypotheses for fun.  The researcher wants a hypothesis to
win, runs in good faith, and often knows things first-hand that the published record does not
show.  The header is the frame, and the frame decides what a run can find.  So before a quest the
harness sits the researcher down with a coach (`cr sign`).  The coach

1. asks why they are running this, what they want it for, and what experience makes them think
   their hypothesis is right;
2. forecasts the draft frame and alternative frames, and says which is best for the hypothesis
   they want (the weakest claim that still means something, against a rival someone really holds);
3. has them type the question and every hypothesis by hand, in their own words;
4. restates the wording so the corpus can test it, and has them read it;
5. spells out the consequences (the forecast, the worst likely result, what a win does and does
   not mean) and has them accept each one by typing it.

Acceptance exists for one purpose: the researcher knows the likely outcome before the run, so a
hard result is not a shock that makes them walk away.  It is not a security measure.  The record
(``01_FRAME/frame-certificate.json`` and ``FRAME-CERTIFICATE.md``) is a plain file.
"""

from __future__ import annotations

import difflib
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
TARGET_SHARE = 2 / 3            # the preferred hypothesis should reach two thirds of the gauge
FORECAST_CALLS = 3
ROLE = "frame_gate"


class NotAPerson(Exception):
    """The frame can only be signed by a person at a keyboard."""


class Changed(Exception):
    """The person chose to stop and change the frame; nothing is signed."""


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
            raise NotAPerson("The coaching session is for a person at a keyboard, in a terminal window. It cannot "
                             "be run by a script, through a pipe, or by an agent's command tool.")

    def say(self, text: str = "") -> None:
        print(text, flush=True)

    def now(self) -> float:
        return time.perf_counter()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

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

SYSTEM = ("You are the coach in the corner of a researcher who is running an Analysis of Competing Hypotheses (ACH). "
          "The frame decides what a run can find, and your job is to help them choose a frame they can win on "
          "honestly. Assume they act in good faith and that their own experience gives them a valid point, even "
          "where the published record leans the other way: published cohorts are often healthier and less confounded "
          "than the people the researcher knows. First-hand knowledge cannot be scored as evidence, but it can shape "
          "which claim is tested. Mechanistic evidence counts as evidence. Tell them plainly what the corpus does "
          "and does not show; never tell them to give up. Be exact and plain. Return one JSON object and nothing else.")

# How a claim is calibrated to the evidence.  Given to the model wherever it proposes a frame.
CALIBRATION = (
    "HOW TO CALIBRATE A FRAME. A score measures the fit between a claim and the evidence, so the same corpus can "
    "support a modest claim strongly and a strong claim weakly. (1) Make the preferred hypothesis the weakest claim "
    "that still means something to the researcher and that this corpus can support: for example step down from "
    "'is superior' to 'works in the target group' to 'helps some identifiable patients' to 'is worth offering as a "
    "monitored, reversible trial' to 'should be discussed'. Never go so weak that no result could count against it. "
    "(2) Make the rival the strongest position that real people actually hold (a guideline, a group of clinicians, "
    "a body of literature), and name who holds it. Never propose a rival nobody holds. (3) Make the undecided "
    "hypothesis mean real balance between the two, not merely that a perfect study is missing. (4) Use the same "
    "evidence rules for both sides; absence of evidence supports neither. (5) You may also adjust the population, "
    "the comparison (usual care or ideal care), and which outcomes count, when the evidence speaks to them."
)


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


def _own(who: dict) -> str:
    """What the researcher told the coach about themselves, for the model."""
    rows = [("WHY THEY ARE RUNNING THIS", who.get("motivation")), ("WHAT THEY WANT IT FOR", who.get("goal")),
            ("THE EXPERIENCE BEHIND THEIR VIEW (first-hand; not scoreable evidence, but a reason to test the right claim)",
             who.get("experience")),
            ("WHAT THEY WANT TO BE ABLE TO SAY", who.get("intent")), ("WHAT THEY WOULD CONCEDE IF THEY LOSE", who.get("concede"))]
    return "\n".join(f"{k}: {v}" for k, v in rows if v)


def no_holder(text: str) -> bool:
    return not str(text).strip() or bool(re.search(r"\b(no identifiable holder|nobody|no one|unknown)\b", str(text), re.I))


def ladder(model, who: dict, preferred: str, question: str, statements: dict[str, str], evidence: str,
           tag: str = "ladder", result: str = "") -> list[dict]:
    """Alternative frames for the axis, strongest claim first.  A frame whose rival nobody holds is dropped."""
    ids = list(statements)
    user = (_own(who) + f"\nTHE HYPOTHESIS THEY WANT TO WIN: {preferred}\n\nTHE CURRENT FRAME\n"
            + _frame_text(question, statements) + (("\n\nHOW THE CURRENT FRAME SCORED\n" + result) if result else "")
            + "\n\nEVIDENCE AVAILABLE TO THE RUN\n" + evidence + "\n\n" + CALIBRATION +
            "\n\nTASK: write three alternative frames for this axis, ordered from the strongest claim to the "
            f"weakest. Each must serve what the researcher wants, keep the hypothesis ids {', '.join(ids)}, "
            f"and keep {preferred} as the hypothesis they want to win. Do not write a frame the corpus cannot test. "
            'Return {"rungs": [{"label": "six words at most", "question": "...", "statements": {'
            + ", ".join(f'"{i}": "..."' for i in ids) + '}, "rival_held_by": "who really holds the main rival as '
            'worded", "win_lets_you_say": "one sentence: what a win for ' + preferred + ' would let the researcher '
            'say", "leaves_out": "one sentence: what this frame gives up or leaves outside the question"}]}.')
    got = model(tag, SYSTEM, user, "")
    rungs = []
    for r in (got.get("rungs") or [])[:4]:
        st = r.get("statements") or {}
        if not (isinstance(r, dict) and all(str(st.get(i, "")).strip() for i in ids) and str(r.get("question", "")).strip()):
            continue
        if no_holder(r.get("rival_held_by", "")):
            continue
        rungs.append({"label": " ".join(str(r.get("label", "")).split())[:60] or "alternative",
                      "question": " ".join(str(r["question"]).split()),
                      "statements": {i: " ".join(str(st[i]).split()) for i in ids},
                      "rival_held_by": " ".join(str(r["rival_held_by"]).split()),
                      "win_lets_you_say": " ".join(str(r.get("win_lets_you_say", "")).split()),
                      "leaves_out": " ".join(str(r.get("leaves_out", "")).split())})
    if not rungs:
        raise ValueError("no usable alternative frames came back")
    return rungs


def restate(model, intent: str, question: str, statements: dict[str, str], evidence: str) -> dict:
    ids = list(statements)
    user = (intent + "\n\nTHE FRAME AS THE RESEARCHER TYPED IT\n"
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


def certify_axis(con, model, project: Path, text: str, axis: dict, gauge: int, prior: dict | None = None,
                 who: dict | None = None) -> tuple[str, dict]:
    """Coach one axis.  Returns the header text with the accepted wording, and the record.
    `prior` is this person's earlier record of the axis, if any: wording that is already their own
    may be typed again; a draft's wording may not.  `who` holds why they are running this."""
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
            con.say(f"  (The model could not do this step: {steps[name]}. The record will say so.)")
            return fallback

    con.say("")
    con.say("=" * 96)
    con.say(f"AXIS {aid}: {axis.get('name', '')}")
    con.say("=" * 96)
    con.say("The header is the frame. What this run can find follows from the words you settle on here.")
    con.say("")
    for h in axis["hypotheses"]:
        _show(con, f"{h['id']}: {h['statement']}")
    while True:
        con.say(f"Which hypothesis do you want to win? Type its id ({', '.join(ids)}).")
        got, _, _ = con.line("> ")
        if got.strip().upper() in [i.upper() for i in ids]:
            preferred = next(i for i in ids if i.upper() == got.strip().upper())
            break
    rec["preferred"] = preferred
    rec["experience"] = hand_typed(
        con, f"What experience shaped your view? Why do you think {preferred} is right, even where published "
             "evidence points the other way? What you know first-hand counts here.", 8)
    rec["intent"] = hand_typed(con, "On this axis, what do you want to be able to say when the run is done?", 8)
    rec["concede"] = hand_typed(con, "If the result goes against you, what will you concede?", 4)
    intent, concede = rec["intent"]["text"], rec["concede"]["text"]
    me = {**(who or {}), "experience": rec["experience"]["text"], "intent": intent, "concede": concede}

    evidence = index_digest(project, aid)
    findings, basis = frd_digest(project, aid)
    if findings:
        evidence = "Source index:\n" + evidence + "\n\nFindings already validated in an earlier run:\n" + findings
    rec["forecast_basis"] = ("the source index" if evidence else "nothing: no index was found") + (f" and {basis}" if basis else "")

    con.say("")
    con.say(f"Forecasting the draft frame and alternatives ({FORECAST_CALLS} calls each). This takes a few minutes.")
    rungs = [{"label": "the draft as written", "question": axis.get("question", ""), "statements": draft,
              "rival_held_by": "", "win_lets_you_say": "", "leaves_out": ""}]
    rungs += try_model("ladder", lambda: ladder(model, me, preferred, axis.get("question", ""), draft, evidence), [])
    with ThreadPoolExecutor(max_workers=len(rungs)) as pool:
        made = list(pool.map(lambda nr: forecast(model, nr[1]["question"], nr[1]["statements"], gauge, evidence,
                                                 f"{aid}:rung{nr[0]}"), enumerate(rungs)))
    for r, fc0 in zip(rungs, made):
        r["forecast"] = fc0
    steps["forecast"] = "ok" if all(r["forecast"]["ok"] == FORECAST_CALLS for r in rungs) else \
        f"{sum(r['forecast']['ok'] for r in rungs)} of {FORECAST_CALLS * len(rungs)} forecast calls answered"
    rec["ladder"] = rungs
    con.say("")
    con.say(f"FORECASTS for {preferred}, in units of the {gauge}-unit gauge. Your target is {target}. A forecast is "
            "a guess at how the evidence would be divided. It is not a probability that you are right.")
    for n, r in enumerate(rungs):
        con.say("")
        con.say(f"  [{n}] {r['label']}:  {_fc_line(r['forecast'], preferred, gauge)}")
        for hid in ids:
            _show(con, f"{hid}: {r['statements'][hid]}", "        ")
        if r["rival_held_by"]:
            _show(con, "The rival is held by: " + r["rival_held_by"], "        ")
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
        rs = try_model("restate", lambda: restate(model, _own(me), typed_q["text"], mine, evidence),
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
    con.say("THE CONSEQUENCES OF THIS FRAME. Accept each one by typing it, or type CHANGE to stop and rework it.")
    con.say("Whatever the run finds, you will have seen it coming, and there is a next move either way.")
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
        item("THE FORECAST", ["No forecast could be made. You are going ahead without one."], "I accept no forecast")
    else:
        lines = [f"{preferred} is forecast at {mean} of {gauge}. The calls gave " +
                 ", ".join(str(c["allocations"][preferred]) for c in fc["calls"] if "allocations" in c) +
                 f". Your target is {target}. Basis: {rec['forecast_basis']}. These are units of evidence, not a "
                 "probability of being right."]
        if mean < target:
            lines.append("That is BELOW your target. If the run agrees with the forecast, the coach will stop after the "
                         "quest and again after the findings are validated, and show you a claim this evidence does support.")
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
        lines.append("Nobody holds the rival as you worded it. A critic will call it a strawman, and the record says so.")
    item("THE RIVAL YOU ARE TESTING AGAINST", lines, "I accept the rival")
    item("WHAT THIS FRAME LEAVES OUT, AND WHAT A CRITIC WILL SAY",
         ["Left out: " + x for x in bt["left_out"]] + ["A critic will say: " + x for x in bt["a_critic_will_say"]]
         or ["(The model named nothing.)"], "I accept what is left out")
    if bt["conflicts"]:
        item("THE REST OF THE AXIS TEXT DISAGREES WITH YOUR WORDING",
             bt["conflicts"] + ["To have these fixed, type CHANGE, have the header corrected, and run this again."],
             "I accept the conflicts")
    rec.update({"accepted": accepted, "model_steps": steps, "accepted_at": utcnow()})
    return new_text, rec


# --------------------------------------------------------------------------- #
# The record of what was accepted.  A plain file: it is there for the researcher and the coach.

def load_certificate(project: Path) -> dict | None:
    try:
        c = read_json(Path(project) / "01_FRAME" / CERT_JSON, default=None)
    except ValueError:
        return None
    return c if isinstance(c, dict) else None


def _wording(axis: dict) -> dict:
    flat = lambda t: " ".join(str(t).split())
    return {"question": flat(axis.get("question", "")),
            "statements": {h["id"]: flat(h["statement"]) for h in axis["hypotheses"]}}


def unaccepted_axes(text: str, cert: dict) -> list[str]:
    """Axes of the header whose wording is not the wording the researcher accepted."""
    from .header import parse_header
    done = cert.get("axes") or {}
    out = []
    for ax in parse_header(text)["axes"]:
        r = (done.get(ax["axis_id"]) or {}).get("restated") or {}
        now = _wording(ax)
        if now["question"] != " ".join(str(r.get("question", "")).split()) or now["statements"] != {
                k: " ".join(str(v).split()) for k, v in (r.get("statements") or {}).items()}:
            out.append(ax["axis_id"])
    return out


def accepted(project: Path) -> tuple[bool, str]:
    """(yes, why).  Yes when the researcher has been through the session for every axis of the header
    as it now reads."""
    project = Path(project)
    hp = header_path(project)
    if not hp.exists():
        return False, f"there is no header ({hp.name})"
    cert = load_certificate(project)
    if not cert:
        return False, "nobody has been through the frame with the coach yet"
    try:
        left = unaccepted_axes(_norm(read_text(hp)), cert)
    except ValueError as e:
        return False, f"the header cannot be read: {e}"
    if left:
        never = [a for a in left if a not in (cert.get("axes") or {})]
        return False, ((f"axes {', '.join(never)} have" if len(never) > 1 else f"axis {never[0]} has")
                       + " not been through the coach" if never else
                       "the wording of axis " + ", ".join(left) + " changed since it was accepted")
    return True, f"frame accepted by {cert.get('name') or 'the researcher'} on {str(cert.get('accepted', ''))[:10]}"


def gate(project: Path, action: str) -> tuple[bool, str]:
    """(may proceed, message).  A quest does not start until the researcher has been through the
    frame with the coach (set coach.require_acceptance to false in project.json to switch that off).
    Everything else gets a reminder."""
    from .config import load_config
    ok, why = accepted(project)
    if ok:
        return True, why
    need = bool((load_config(project).get("coach") or {}).get("require_acceptance", True))
    if action == "quest" and need:
        return False, (f"quest not started: {why}.\nGo through the frame with the coach first, in a terminal window:  "
                       f"cr sign \"{project}\"\nIt asks what you want from this run, shows how each way of framing the "
                       "question is likely to score, and has you accept the likely outcome before the quest spends anything.")
    return True, f"Reminder: {why}. The coach is at:  cr sign \"{project}\""


def uses_models(cfg: dict) -> bool:
    """True when any role is routed to something other than the offline engine or a test stand-in."""
    for v in (cfg.get("roles") or {}).values():
        for n in ([v] if isinstance(v, str) else list(v or [])):
            if (cfg.get("providers") or {}).get(n, {}).get("type", n) not in ("local", "mock", "replay"):
                return True
    return False


def render(cert: dict) -> str:
    who = cert.get("who") or {}
    out = ["# Frame record", "",
           f"Accepted by **{cert.get('name') or 'the researcher'}** on {str(cert.get('accepted', ''))[:10]}.",
           "", "The header is the frame, and the frame decides what a run can find. This page records what the "
           "researcher told the coach, typed, read and accepted before the quest. A different frame can be scored on "
           "the same evidence (`cr rescore`); this is the one they chose.", ""]
    if who:
        out += ["## Why this run", "", f"- **Motivation:** {who.get('motivation', '')}", f"- **Goal:** {who.get('goal', '')}", ""]
    cell = lambda t: " ".join(str(t).split()).replace("|", "\\|")
    for aid, r in (cert.get("axes") or {}).items():
        g, pref = r.get("gauge", 64), r.get("preferred", "")
        fc = r.get("forecast") or {}
        out += [f"## Axis {aid}: {r.get('name', '')}", "",
                f"- **Wants to win:** {pref}",
                f"- **Experience behind that view:** {(r.get('experience') or {}).get('text', '')}",
                f"- **Wants to be able to say:** {r['intent']['text']}",
                f"- **Would concede:** {r['concede']['text']}", ""]
        out += ["### The hypotheses", "", "| | As typed | As it stands in the header |", "|---|---|---|",
                f"| Question | {cell(r['typed']['question']['text'])} | {cell(r['restated']['question'])} |"]
        out += [f"| {h} | {cell(t['text'])} | {cell(r['restated']['statements'][h])} |" for h, t in r["typed"]["statements"].items()]
        out.append("")
        for c in r["restated"].get("changes", []):
            out.append(f"- Changed in restating: {c}")
        for c in r["restated"].get("cannot_be_tested", []):
            out.append(f"- This corpus cannot test: {c}")
        if r["restated"].get("not_restated"):
            out.append("- The model did not restate the wording; the header carries what was typed.")
        out += ["", "### Forecast", ""]
        if fc.get("ok"):
            out.append(f"{pref} was forecast at **{fc['mean'][pref]} of {g}** units (calls: " +
                       ", ".join(str(c["allocations"][pref]) for c in fc["calls"] if "allocations" in c) +
                       f"; target {r.get('target')}). Basis: {r.get('forecast_basis', '')}. A forecast is a guess at how "
                       "the evidence would be divided, not a probability of being right.")
        else:
            out.append("No forecast could be made.")
        out += ["", "| Frame considered | Forecast for " + pref + " | Rival held by | Gives up |", "|---|---|---|---|"]
        for rung in r.get("ladder", []):
            f = rung.get("forecast") or {}
            out.append(f"| {cell(rung['label'])} | {f['mean'][pref] if f.get('ok') else 'none'} | "
                       f"{cell(rung.get('rival_held_by', ''))} | {cell(rung.get('leaves_out', ''))} |")
        bt = r.get("back_translation") or {}
        out += ["", "### What a win means", ""]
        out += [f"- May say: {x}" for x in bt.get("if_it_wins_you_may_say", [])]
        out += [f"- May **not** say: {x}" for x in bt.get("you_may_not_say", [])]
        if (r.get("judge") or {}).get("match") is False:
            out.append(f"- **A win would not let the researcher say what they want to say:** {r['judge'].get('gap', '')}")
        wc = bt.get("worst_case") or {}
        if wc.get("allocations"):
            out.append("- Worst likely result: " + ", ".join(f"{k} {v}" for k, v in wc["allocations"].items()) +
                       f". Then the researcher would have to say: {wc.get('then_you_would_have_to_say', '')}")
        out += ["", "### What the frame leaves out", ""]
        out += [f"- {x}" for x in bt.get("left_out", [])] + [f"- A critic will say: {x}" for x in bt.get("a_critic_will_say", [])]
        held = bt.get("rival_is_held_by", "")
        out.append(f"- The main rival is held by: {held or 'not stated'}" +
                   (" **(a rival nobody holds)**" if re.search("no identifiable holder", held, re.I) else ""))
        out += [f"- The axis text disagrees with the wording: {x}" for x in bt.get("conflicts", [])]
        out += ["", "### What the researcher accepted, by typing it", ""]
        out += [f"- {a['item']}: \"{a['typed']}\"" for a in r.get("accepted", [])]
        out += [f"- Read {x['label']}: {x['words']} words, {x['seconds_on_screen']} seconds, {len(x['blanks'])} missing-word checks."
                for x in r.get("read", [])]
        bad = {k: v for k, v in (r.get("model_steps") or {}).items() if v != "ok"}
        out += [f"- Model step `{k}`: {v}" for k, v in bad.items()]
        out.append("")
    if cert.get("unaccepted_axes"):
        out += [f"**Not yet done: axis {', '.join(cert['unaccepted_axes'])}.**", ""]
    return "\n".join(out) + "\n"


def _mark(text: str, name: str) -> str:
    """The header parser's approval marker, set when every axis has been accepted."""
    text = re.sub(r"<!--\s*APPROVED[:\s].*?-->\n?", "", text, flags=re.S | re.I)
    lines = text.split("\n")
    lines.insert(1 if lines and lines[0].startswith("#") else 0,
                 f"<!-- APPROVED: {name} on {utcnow()[:10]} (frame accepted with the coach) -->")
    return "\n".join(lines)


def _write(project: Path, cert: dict, text: str, crlf: bool) -> dict:
    project = Path(project)
    cert["unaccepted_axes"] = unaccepted_axes(text, cert)
    if not cert["unaccepted_axes"]:
        text = _mark(text, cert.get("name") or "the researcher")       # the marker sits outside the axis blocks
    cert["accepted"] = utcnow()
    hp = header_path(project)
    hp.parent.mkdir(parents=True, exist_ok=True)
    hp.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
    write_json(project / "01_FRAME" / CERT_JSON, cert)
    atomic_write_text(project / "01_FRAME" / CERT_MD, render(cert))
    cfg = read_json(project / "project.json", default={}) or {}
    cfg.setdefault("frame", {})["approval_note"] = (f"Frame accepted by {cert.get('name') or 'the researcher'} on "
                                                    f"{cert['accepted'][:10]} (cr sign).")
    write_json(project / "project.json", cfg)
    return cert


def sign_frame(con, model, project: Path, header: Path | None = None, only: str | None = None,
               name: str | None = None) -> dict:
    """Coach the researcher through every axis not yet accepted (or `only`).  Each axis is saved as
    it is finished."""
    from .header import normalize_hypothesis_ids, parse_header
    project = Path(project)
    src = Path(header) if header else header_path(project)
    if not src.exists():
        raise ValueError(f"there is no header to work on: {src}")
    if (project / "01_FRAME" / "frame.json").exists():
        raise ValueError("01_FRAME/frame.json overrides the header; remove it so that the header you accept governs")
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
        raise ValueError(f"the header has no \"Axis ...\" heading for {', '.join(headless)}; each axis needs its own heading")
    short = [h["id"] for a in frame["axes"] for h in a["hypotheses"] if not h["statement"]]
    if short:
        raise ValueError(f"the header's hypothesis table has no statement for {', '.join(short)}")
    old = load_certificate(project) or {}
    before = old.get("axes") or {}
    stale = unaccepted_axes(text, old)
    axes = {a: r for a, r in before.items() if a in order and a != only and a not in stale}
    todo = [a for a in order if (a == only if only else a not in axes)]
    if only and not todo:
        raise ValueError(f"the header has no axis {only}")
    if not todo:
        raise ValueError("every axis is already accepted as it reads; name one to go through it again:  --axis A1")

    con.say(f"Frame coaching for {project.name}.")
    con.say(f"To do now: axis {', '.join(todo)}." + (f" Already accepted and unchanged: {', '.join(axes)}." if axes else ""))
    con.say("Each axis is saved when you finish it. Ctrl+C stops; finished axes stay finished.")
    con.say("Answers are typed by hand; paste is not taken. There are no wrong answers to the first questions.")
    con.say("")
    name = " ".join((name or old.get("name") or "").split())
    while not name:
        name = " ".join(con.line("Your name: ")[0].split())
    who = dict(old.get("who") or {})
    if who.get("motivation") and who.get("goal"):
        con.say("You told the coach earlier:")
        _show(con, "Why you are running this: " + who["motivation"])
        _show(con, "What you want it for: " + who["goal"])
    else:
        who["motivation"] = hand_typed(con, "What is your motivation? Why are you running this analysis?", 6)["text"]
        who["goal"] = hand_typed(con, "What is your goal, and how do you hope this analysis will help you reach it?", 6)["text"]
    cert = old
    for aid in todo:
        ax = next(a for a in parse_header(text)["axes"] if a["axis_id"] == aid)
        text, rec = certify_axis(con, model, project, text, ax, int(frame.get("gauge", 64)), prior=before.get(aid), who=who)
        axes[aid] = rec
        cert = {"version": 2, "project": project.name, "name": name, "who": who,
                "axes": {a: axes[a] for a in order if a in axes}}
        cert = _write(project, cert, text, crlf)
        text = _norm(read_text(header_path(project)))
        con.say("")
        con.say(f"Axis {aid} is accepted and saved.")
    con.say("")
    con.say(f"Record: {project / '01_FRAME' / CERT_MD}")
    if cert["unaccepted_axes"]:
        con.say(f"Still to do: axis {', '.join(cert['unaccepted_axes'])}:  cr sign \"{project}\"")
    else:
        con.say("Every axis is accepted. After the quest, and again after the findings are validated, the coach "
                "scores the evidence against this frame and tells you where you stand and what your next move is.")
    return cert


# --------------------------------------------------------------------------- #
# Commands.

def model_for(project: Path):
    """The model the coach consults, as `model(tag, system, user, salt) -> dict`."""
    from .config import load_config
    from .llm.base import LLMRequest
    from .llm.router import LLM
    try:
        llm = LLM(load_config(project))
    except Exception as e:                           # no model is no reason to stop the session
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


def cmd_sign(a) -> int:
    project = Path(a.project).resolve()
    if a.check:
        ok, why = accepted(project)
        print(("ACCEPTED: " if ok else "NOT YET: ") + why)
        return 0 if ok else 2
    try:
        con = Terminal()
    except NotAPerson as e:
        print(f"sign: {e}", file=sys.stderr)
        return 2
    try:
        sign_frame(con, model_for(project), project, header=Path(a.header) if a.header else None,
                   only=a.axis.upper() if a.axis else None, name=a.name)
    except Changed:
        con.say("Stopped. Nothing was saved for this axis. Rework the header, then run `cr sign` again.")
        return 1
    except (KeyboardInterrupt, EOFError):
        con.say("")
        con.say("Stopped. Axes already finished stay finished; the one in progress was not saved.")
        return 1
    except ValueError as e:
        print(f"sign: {e}", file=sys.stderr)
        return 2
    return 0
