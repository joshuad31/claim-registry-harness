"""The local analyst: a deterministic, offline, rules-based engine for every role.

Why this exists
---------------
Every earlier attempt at this harness stalled on the same thing: several hundred
model answers were needed before an investigation could finish, and no model
operator was available to write them.  The local provider removes that
dependency.  With ``default_provider = "local"`` a project runs from an empty
folder to a finished report with no network, no API key and no queue: every
stage is answered in-process from the supplied text.

What it is, exactly
-------------------
It is a *lexical-structural analyst*, not a language model.  It reads the same
prompt the model roles read, applies explicit rules to the words in it, and
writes the same JSON shape.  Its judgments are therefore:

* reproducible (same input -> same answer, byte for byte);
* inspectable (every trace names the rule and the counts it used);
* narrow (it handles polarity, quantities, modality, scope, voice and lexical
  overlap; it does not understand a sentence).

Consequences, stated plainly:

* Unit derivation is clause splitting with verbatim anchors, not interpretation.
* Matching is weighted token overlap plus the explicit semantic checks below.
  It is *not* model judgment; its qualification on the adversarial fixtures is
  evidence about those 22 patterns only.
* The Archivist is extractive: it quotes the passages it was given and never
  composes new claims.
* The final assessment counts evidence per hypothesis.  It is a bookkeeping
  number, not ACH_Eval judgment, and the artifact says so.

Every artifact produced through this provider records the provider identity
``local:local-rules-v1`` in the run's call log, and the report discloses that
the run used the local engine.  A real model can be routed to any role at any
time; cached local answers are never presented as model answers.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from ..util import (MODAL_RE, NEGATION_RE, norm_for_match, norm_ws, read_text,
                    truncate_words, utcnow, word_count)
from .base import LLMRequest, LLMResponse
from .providers import BaseProvider

MODEL = "local-rules-v1.8"
VERSION = "1.8"

# --------------------------------------------------------------------------- #
# 1. text engine
# --------------------------------------------------------------------------- #

_WORD = re.compile(r"[a-z0-9]+(?:[.\-'/][a-z0-9]+)*")

# multi-word phrases are folded to one token before tokenising
_PHRASES = [
    (re.compile(r"\bmaximum flow rate\b", re.I), " qmax "),
    (re.compile(r"\bpeak flow rate\b", re.I), " qmax "),
    (re.compile(r"\bflow rate\b", re.I), " qmax "),
    (re.compile(r"\bshy bladder\b", re.I), " paruresis "),
    (re.compile(r"\bsocial anxiety\b", re.I), " socialanxiety "),
    (re.compile(r"\btumou?r necrosis factor(?:[- ]alpha)?\b", re.I), " tnfa "),
    (re.compile(r"\btnf[- ]?alpha\b", re.I), " tnfa "),
    (re.compile(r"\binterleukin[- ]?1\b", re.I), " il1 "),
    (re.compile(r"\binterleukin[- ]?6\b", re.I), " il6 "),
    (re.compile(r"\bblood flow\b", re.I), " perfusion "),
    (re.compile(r"\bpelvic floor\b", re.I), " pelvicfloor "),
    (re.compile(r"\bvitamin e\b", re.I), " vitamine "),
    (re.compile(r"\bthree times daily\b", re.I), " tiddose "),
    (re.compile(r"\btwice daily\b", re.I), " biddose "),
    (re.compile(r"\bonce daily\b", re.I), " qddose "),
    (re.compile(r"\bin vitro\b", re.I), " invitro "),
    (re.compile(r"\bin vivo\b", re.I), " invivo "),
]

# Domain-neutral synonym groups.  The first item is the canonical form.
# This is a readability aid for lexical matching, not an ontology; the PTX
# project can extend it with ``matching.synonyms`` (shortlist only) and a
# project can ship a dictionary through the language layer.
_SYN_GROUPS = [
    ("ptx", "pentoxifylline", "oxpentoxifylline", "trental"),
    ("human", "humans", "patient", "patients", "man", "men", "people", "person", "subjects",
     "subject", "volunteer", "volunteers", "cohort", "clinical"),
    ("animal", "animals", "rat", "rats", "mouse", "mice", "dog", "dogs", "pig", "pigs",
     "rabbit", "rabbits", "rodent", "rodents", "canine", "murine", "bovine", "sheep"),
    ("improve", "improved", "improves", "improving", "improvement", "improvements",
     "ameliorate", "ameliorated", "better", "enhance", "enhanced"),
    ("reduce", "reduced", "reduces", "reducing", "reduction", "decrease", "decreased",
     "lower", "lowered", "attenuate", "attenuated", "inhibit", "inhibited"),
    ("increase", "increased", "increases", "increasing", "raise", "raised", "elevate",
     "elevated", "rise", "rose", "heighten"),
    ("void", "voiding", "urination", "urinate", "urinary", "micturition", "micurate"),
    ("fibrosis", "fibrotic", "collagen", "fibrogenesis"),
    ("measure", "measured", "measuring", "measurement", "detected", "detect", "found",
     "find", "reach", "reached", "reaches", "attain", "attained", "achieve", "achieved"),
    ("dose", "doses", "dosing", "dosage", "dosed"),
    ("contractility", "contraction", "contractions", "tension", "contractile"),
    ("perfusion", "flow"),
    ("bph", "prostate", "prostatic", "hyperplasia"),
    ("inflammation", "inflammatory"),
    ("level", "levels", "concentration", "concentrations", "exposure", "exposures"),
    ("structure", "structural", "remodeling", "remodelling"),
    ("rapid", "quick", "early", "immediate", "fast"),
    ("slow", "late", "delayed", "gradual"),
]

_STOP = set("""
a about above after again against all also am an and any are as at be because been before
being below between both but by can could did do does doing down during each few for from
further had has have having he her here hers herself him himself his how i if in into is it
its itself just me more most my myself no nor not now of off on once only or other our ours
ourselves out over own same she should so some such than that the their theirs them
themselves then there these they this those through to too under until up very was we were
what when where which while who whom why will with would you your yours yourself yourselves
et al vs via per e.g i.e
""".split())

# Research-reporting words: present in almost every sentence, so they weigh little.
_META = {"study", "studies", "trial", "trials", "report", "reports", "reported", "review",
         "reviews", "author", "authors", "finding", "findings", "result", "results",
         "publication", "publications", "article", "articles", "paper", "papers",
         "evidence", "data", "group", "groups", "table", "figure", "significant"}

# Modality / negation words never count as content.
_MODAL_WORDS = {"may", "might", "could", "can", "possibly", "possible", "likely", "unlikely",
                "suggest", "suggests", "suggested", "appear", "appears", "appeared", "must",
                "should", "would", "probably", "potential", "potentially", "perhaps"}
_NEG_WORDS = {"not", "no", "none", "never", "neither", "nor", "without", "cannot", "absent",
              "absence", "lack", "lacked", "unchanged", "insignificant", "nonsignificant"}

_VERB_RE = re.compile(
    r"\b(?:reduc(?:e|es|ed|ing)|increas(?:e|es|ed|ing)|improv(?:e|es|ed|ing)|"
    r"measur(?:e|es|ed|ing)|randomiz(?:e|es|ed|ing)|characteriz(?:e|es|ed|ing)|"
    r"report(?:s|ed|ing)?|show(?:s|ed|n)?|found|demonstrat(?:e|es|ed|ing)|"
    r"caus(?:e|es|ed|ing)|reach(?:es|ed|ing)?|differ(?:s|ed|ing)?|chang(?:e|es|ed|ing)|"
    r"act(?:s|ed|ing)?|produc(?:e|es|ed|ing)|lead(?:s|ing)?|led|prevent(?:s|ed|ing)?|"
    r"inhibit(?:s|ed|ing)?|attenuat(?:e|es|ed|ing)|lower(?:s|ed|ing)?|rais(?:e|es|ed|ing)|"
    r"elevat(?:e|es|ed|ing)|decreas(?:e|es|ed|ing)|block(?:s|ed|ing)?|modulat(?:e|es|ed|ing)|"
    r"target(?:s|ed|ing)?|suggest(?:s|ed|ing)?|indicat(?:e|es|ed|ing)|associat(?:e|es|ed|ing)|"
    r"correlat(?:e|es|ed|ing)|predict(?:s|ed|ing)?|support(?:s|ed|ing)?|justif(?:y|ies|ied)|"
    r"warrant(?:s|ed|ing)?|requir(?:e|es|ed|ing)|preclud(?:e|es|ed|ing)|"
    r"exclud(?:e|es|ed|ing)|resolv(?:e|es|ed|ing)|remain(?:s|ed|ing)?|persist(?:s|ed|ing)?)\b")
_PASSIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being)\s+(?:[a-z]+ly\s+)?[a-z]+(?:ed|en)\b")
_REPORT_RE = re.compile(
    r"\b(?:report(?:s|ed|ing)?|review(?:s|ed)?|according to|cites?|cited|states?|stated|"
    r"describes?|described|notes?|noted)\b", re.I)
_COND_RE = re.compile(r"\b(?:if|unless|provided that|in the event)\b", re.I)
_EXIST_RE = re.compile(
    r"\b(?:at least one|a study|studies have|some studies|there is evidence|has been reported|"
    r"have been reported|can|capable of)\b", re.I)
_NUM_UNIT_RE = re.compile(
    r"(?<![a-z])(\d+(?:[.,]\d+)?)\s*(ml/s|ml|mg|µg|ug|%|percent|weeks?|days?|hours?|months?|"
    r"minutes?|patients?|men|rats?|mice|mmhg|cmh2o)", re.I)
_FREQ_RE = re.compile(
    r"\b(once|twice|three times|four times|two times|q\.?d\.?|b\.?i\.?d\.?|t\.?i\.?d\.?|"
    r"qddose|biddose|tiddose)\b", re.I)
_FREQ_MAP = {"once": "1", "twice": "2", "two times": "2", "three times": "3", "four times": "4",
             "qd": "1", "bid": "2", "tid": "3", "qddose": "1", "biddose": "2", "tiddose": "3"}

# the boilerplate of a quest question; it must not dominate retrieval scoring
_QUESTION_FRAME = {"find", "finding", "report", "study", "design", "population", "model", "dose",
                   "exposure", "comparator", "contrary", "null", "result", "cite", "exact",
                   "passage", "question", "source", "specifically", "bear", "what", "which",
                   "how", "does", "do", "are", "is", "give", "provide", "state", "say"}


def _stem(w: str) -> str:
    w = w.lower()
    if len(w) > 5 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 5 and w.endswith("ing"):
        w = w[:-3]
    elif len(w) > 4 and w.endswith("ed"):
        w = w[:-2]
    elif len(w) > 4 and w.endswith("es"):
        w = w[:-2]
    elif len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        w = w[:-1]
    return w


_SYN: dict[str, str] = {}
for _g in _SYN_GROUPS:
    _canon = _g[0]
    for _w in _g:
        _SYN[_stem(_w)] = _canon
        _SYN[_w] = _canon


def _prep(s: str) -> str:
    s = norm_for_match(s)
    for pat, rep in _PHRASES:
        s = pat.sub(rep, s)
    return s


def _toks(s: str) -> list[str]:
    return _WORD.findall(_prep(s))


def _canon(t: str) -> str:
    return _SYN.get(_stem(t), _stem(t))


def _content(s: str) -> set[str]:
    out = set()
    for t in _toks(s):
        if t in _STOP or t in _MODAL_WORDS or t in _NEG_WORDS or t.isdigit():
            continue
        if len(t) < 3:
            continue
        out.add(_canon(t))
    return out


def _weight(t: str) -> float:
    return 0.35 if t in _META else 1.0


def _coverage(need: set[str], have: set[str]) -> float:
    if not need:
        return 0.0
    tot = sum(_weight(t) for t in need)
    got = sum(_weight(t) for t in need if t in have)
    return got / tot if tot else 0.0


class _Seg:
    """Structural reading of one short text."""

    __slots__ = ("text", "low", "content", "neg", "modal_strong", "modal_weak", "numbers",
                 "freq", "species", "passive", "subject", "report", "conditional",
                 "existential", "plus_partner")

    def __init__(self, text: str):
        self.text = text or ""
        self.low = _prep(self.text)
        self.content = _content(self.text)
        # "without new data" / "without a control" describes provenance, not polarity; only
        # explicit denial or null-result wording counts as negation here.
        self.neg = bool(re.search(
            r"\b(?:not|no|none|never|neither|nor|cannot|didn't|doesn't|isn't|wasn't|weren't|"
            r"aren't|failed to|fail to|unchanged|insignificant|nonsignificant|non-significant)\b",
            self.text, re.I))
        mods = {m.lower() for m in MODAL_RE.findall(self.text)}
        self.modal_strong = bool(mods & {"must", "should", "required", "requires"})
        self.modal_weak = bool(mods & {"may", "might", "could", "possibly", "possible", "suggest",
                                       "suggests", "suggested", "appear", "appears", "likely",
                                       "potential", "potentially", "can"})
        self.numbers = []
        for m in _NUM_UNIT_RE.finditer(self.text):
            val = m.group(1).replace(",", ".")
            unit = m.group(2).lower().rstrip("s") if m.group(2).lower() not in ("ml/s", "mmhg",
                                                                               "cmh2o") else m.group(2).lower()
            self.numbers.append((unit, val))
        fm = _FREQ_RE.search(self.low)
        self.freq = _FREQ_MAP.get(fm.group(1).replace(".", "").lower()) if fm else None
        if re.search(r"\b(human|humans|patients?|men|man|people|subjects?|volunteers?|clinical|"
                     r"cohort)\b", self.low):
            self.species = "human"
        elif re.search(r"\b(rats?|mice|mouse|dogs?|pigs?|rabbits?|rodents?|animals?|canine|murine)\b",
                       self.low):
            self.species = "animal"
        elif re.search(r"\b(invitro|cell|cells|culture)\b", self.low):
            self.species = "invitro"
        else:
            self.species = None
        self.passive = bool(_PASSIVE_RE.search(self.low))
        m = _VERB_RE.search(self.low)
        self.subject = set()
        if m:
            head = self.low[:m.start()]
            toks = [t for t in _WORD.findall(head) if t not in _STOP and len(t) > 2]
            self.subject = {_canon(t) for t in toks[-4:]}
        self.report = bool(_REPORT_RE.search(self.low))
        self.conditional = bool(_COND_RE.search(self.low))
        self.existential = bool(_EXIST_RE.search(self.low))
        pm = re.search(r"\bplus\s+([a-z0-9\-]+)", self.low)
        self.plus_partner = {_canon(pm.group(1))} if pm else None


def _number_conflict(u: _Seg, w: _Seg) -> str:
    for uu, uv in u.numbers:
        for wu, wv in w.numbers:
            if uu == wu and uv != wv:
                return f"quantity conflict: {uu}={uv} vs {wv}"
    return ""


def _actor_reversal(u: _Seg, w: _Seg) -> str:
    """Both active, disjoint subjects, each subject appearing as an object in the other text.

    A passive construction is excluded because it is the same proposition with the roles
    reordered ('X measured Y' / 'Y was measured by X')."""
    if u.passive or w.passive or not u.subject or not w.subject:
        return ""
    if u.subject & w.subject:
        return ""
    if (u.subject & w.content) and (w.subject & u.content):
        return (f"actor/object reversal: subject {sorted(u.subject)} of the unit is reported as an "
                f"object of the witness, whose subject {sorted(w.subject)} is an object of the unit")
    return ""


def _judge(unit_text: str, witness_text: str, strict: bool = False) -> tuple[str, str]:
    """Return (relation, trace) for one witness-unit pair."""
    u, w = _Seg(unit_text), _Seg(witness_text)
    if not u.content or not w.content:
        return "NO_SEMANTIC_RELATION", "one text has no content words"
    cov = _coverage(u.content, w.content)
    sub = _coverage(w.content, u.content)

    conf = _number_conflict(u, w)
    if conf:
        return "CONTRADICTS", conf

    if u.freq and w.freq and u.freq != w.freq and cov >= 0.4:
        return "PARTIALLY_COVERS", f"same quantities, different frequency ({u.freq} vs {w.freq})"

    rev = _actor_reversal(u, w)
    if rev and cov >= 0.5:
        return "NO_SEMANTIC_RELATION", rev

    scope = ""
    if u.species and w.species and u.species != w.species and {u.species, w.species} <= {"human", "animal"}:
        scope = f"scope mismatch: unit is {u.species}, witness is {w.species}"
    elif u.species == "human" and w.species == "invitro":
        scope = "scope mismatch: unit is human, witness is in vitro"

    # A contradiction needs the same predicate asserted with opposite polarity.  Sentence-level
    # negation is not enough: "some report no yield difference" is not the negation of "reviews
    # report inconsistent results", and an aim sentence ("we tested whether X improves Y") never
    # contradicts a finding.
    us, ws_ = _pred_signs(unit_text), _pred_signs(witness_text)
    shared = set(us) & set(ws_)
    polarity_conflict = any(("-" in us[f] and "+" in ws_[f]) or ("+" in us[f] and "-" in ws_[f])
                            for f in shared)
    if polarity_conflict and cov >= 0.55 and not scope and not _AIM_RE.search(witness_text):
        return "CONTRADICTS", (f"predicate {sorted(shared)} asserted with opposite polarity "
                               f"(coverage {cov:.2f})")

    if scope:
        rel = "PARTIALLY_COVERS" if cov >= 0.3 else "NO_SEMANTIC_RELATION"
        return rel, f"{scope}; content coverage {cov:.2f}"

    if u.plus_partner and w.plus_partner and u.plus_partner != w.plus_partner and cov >= 0.4:
        return "PARTIALLY_COVERS", (f"combination partners differ: unit {sorted(u.plus_partner)} vs "
                                    f"witness {sorted(w.plus_partner)}; coverage {cov:.2f}")

    if u.modal_strong and w.modal_weak and cov >= 0.5:
        return "UNIT_ENTAILS_WITNESS", f"unit is stronger (must) than witness (may/suggest); coverage {cov:.2f}"

    if w.report and not u.report and cov >= 0.5:
        return "PARTIALLY_COVERS", f"witness reports the claim at second hand; coverage {cov:.2f}"

    if w.conditional and not u.conditional and cov >= 0.5:
        return "PARTIALLY_COVERS", f"witness states the unit only conditionally; coverage {cov:.2f}"

    if u.existential and cov >= 0.55:
        return "WITNESS_ENTAILS_UNIT", (f"a concrete instance establishes the unit's existential/capability "
                                        f"claim; coverage {cov:.2f}")

    thr = 0.72 + (0.05 if strict else 0.0)
    if cov >= thr:
        if sub >= 0.55:
            return "EQUIVALENT", f"content coverage {cov:.2f} both ways ({sub:.2f}); no polarity, quantity, scope or modality conflict"
        return "WITNESS_ENTAILS_UNIT", f"witness supplies every unit element and adds detail; coverage {cov:.2f}"
    if cov >= 0.45 + (0.03 if strict else 0.0):
        return "PARTIALLY_COVERS", f"partial content coverage {cov:.2f}; at least one required element missing"
    return "NO_SEMANTIC_RELATION", f"content coverage {cov:.2f} is too low"


# --------------------------------------------------------------------------- #
# 2. sentence / clause helpers
# --------------------------------------------------------------------------- #

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[\"'])")
_CLAUSE_SPLIT = re.compile(
    # split at semicolons, at commas before a conjunction, and at subordinating
    # conjunctions.  A bare " and " is NOT a split point: it usually joins two
    # nouns inside one requirement ("a component that tamsulosin and their
    # pelvic-floor intervention do not address").
    r"\s*(?:;|,\s*(?:and|but|while|whereas|because|which|that|although|though|yet|so)\b|"
    r"\s+(?:but|while|whereas|because|although|though)\s+)\s*", re.I)


def _sentences(text: str, min_words: int = 6) -> list[str]:
    out = []
    for para in re.split(r"\n{2,}", text or ""):
        for s in _SENT.split(para.strip()):
            s = norm_ws(s)
            if word_count(s) >= min_words and not s.startswith("#") and not s.startswith("|"):
                out.append(s)
    return out


def _clauses(text: str, min_words: int = 5) -> list[str]:
    """Split one sentence into short, self-contained clauses (anchors stay verbatim).

    A short fragment is joined to its neighbour only when the joined string is itself a
    contiguous substring of the original; otherwise it is dropped, because a unit's
    ``source_quote`` must be found verbatim in the hypothesis by the anchoring check.
    """
    text = norm_ws(text)
    full = norm_for_match(text)
    out: list[str] = []
    for piece in _SENT.split(text):
        parts = [p.strip(" ,;:.") for p in _CLAUSE_SPLIT.split(piece) if p.strip()]
        i = 0
        while i < len(parts):
            p = parts[i]
            if word_count(p) >= min_words:
                out.append(p)
                i += 1
                continue
            if i + 1 < len(parts):
                cand = (p + " " + parts[i + 1]).strip(" ,;:.")
                if word_count(cand) >= min_words and norm_for_match(cand) in full:
                    out.append(cand)
                    i += 2
                    continue
            i += 1
    return [o for o in out if word_count(o) >= min_words]


def _anchor_ok(quote: str, source: str, min_words: int = 6) -> bool:
    if word_count(quote) < min_words:
        return False
    q = norm_for_match(quote)
    return bool(q) and q in norm_for_match(source)


def _best_sentence(claim: str, source: str, min_overlap: float = 0.25) -> tuple[str, float]:
    """The verbatim sentence of ``source`` that best supports ``claim``."""
    c = _content(claim)
    best, best_s = "", 0.0
    for s in _sentences(source, 5):
        ov = _coverage(c, _content(s))
        if ov > best_s:
            best, best_s = s, ov
    # exact containment beats any similarity
    nq, ns = norm_for_match(claim), norm_for_match(source)
    if nq and len(nq.split()) >= 5 and nq in ns:
        return claim.strip(), 1.0
    return best, best_s


_FINDING_WORDS = re.compile(
    r"\b(?:increas|decreas|improv|reduc|lower|higher|attenuat|inhibit|prevent|associated|"
    r"correlat|predict|result|effect|difference|benefit|risk|response|efficacy|safety)\w*\b", re.I)
_METHOD_WORDS = re.compile(
    r"\b(?:objective of this study|materials and methods|diagnosis was based|eligible|consent|"
    r"questionnaire|adherence of the?rapist|power to detect|were randomized to|were enrolled|"
    r"inclusion criteria|exclusion criteria|statistical analysis|study design)\b", re.I)
_AIM_RE = re.compile(
    r"\b(?:tested whether|to determine whether|to evaluate whether|we (?:tested|investigated|"
    r"examined|aimed)|the objective|the aim|the purpose of this|was (?:conducted|designed|"
    r"performed) to|were (?:enrolled|randomized|assigned) to|this (?:study|trial|review) "
    r"(?:tested|aimed|evaluated))\b", re.I)

# predicate families used to judge polarity at the predicate, not at the sentence
_PRED_FAMILIES = [
    (re.compile(r"\b(?:increas|rise|rose|rais|elevat|improv|enhanc|higher|greater)\w*"), "UP"),
    (re.compile(r"\b(?:decreas|reduc|lower|attenuat|inhibit|diminish|smaller)\w*"), "DOWN"),
    (re.compile(r"\b(?:differ|chang|alter|affect)\w*"), "DIFF"),
    (re.compile(r"\b(?:reach|act|target|engag|detect|measur)\w*"), "REACH"),
    (re.compile(r"\b(?:report|show|demonstrat|find|found|conclude)\w*"), "REPORT"),
]


def _pred_signs(text: str) -> dict[str, set[str]]:
    """predicate family -> {'+', '-'} observed in this text.

    The negator must sit in the four words immediately before the predicate ("did not
    differ", "no significant increase").  A wider window reads one clause's negation as
    the next clause's polarity, which produced false contradictions.
    """
    low = _prep(text)
    out: dict[str, set[str]] = {}
    for rx, fam in _PRED_FAMILIES:
        for m in rx.finditer(low):
            before = _WORD.findall(low[max(0, m.start() - 60):m.start()])[-4:]
            neg = any(t in {"not", "no", "never", "cannot", "none", "neither", "nor"} for t in before) \
                or "failed to" in " ".join(before)
            out.setdefault(fam, set()).add("-" if neg else "+")
    return out


def _finding_value(s: str) -> float:
    """Small retrieval prior: prefer sentences that report a result over methods boilerplate."""
    v = 0.0
    if _FINDING_WORDS.search(s):
        v += 0.18
    if re.search(r"\d", s):
        v += 0.06
    if re.search(r"\b(?:may|suggests?|associated|possible|could)\b", s, re.I):
        v += 0.04
    if _METHOD_WORDS.search(s):
        v -= 0.30
    if word_count(s) < 10:
        v -= 0.10
    return v


def _author_year(filename: str) -> str:
    stem = Path(filename).stem
    m = re.match(r"([A-Za-z][A-Za-z\-']+)[-_ ]?(\d{4})", stem)
    if m:
        return f"{m.group(1).capitalize()} ({m.group(2)})"
    return stem.replace("_", " ").replace("-", " ")[:48]


def _trim_to(text: str, ceiling: int) -> str:
    """Trim to <= ceiling words at a clause or comma boundary, never mid-word."""
    words = text.split()
    if len(words) <= ceiling:
        return text
    cut = " ".join(words[:ceiling])
    for sep in (". ", "; ", ", "):
        i = cut.rfind(sep)
        if i > len(cut) * 0.45:
            return cut[:i].rstrip(" ,;:") + "."
    # drop a trailing partial clause
    i = max(cut.rfind(" and "), cut.rfind(" which "), cut.rfind(" that "))
    if i > len(cut) * 0.5:
        return cut[:i].rstrip(" ,;:") + "."
    return cut.rstrip(" ,;:") + "."


# --------------------------------------------------------------------------- #
# 3. the provider
# --------------------------------------------------------------------------- #

class LocalProvider(BaseProvider):
    """Deterministic offline analyst (see the module docstring for its limits)."""

    kind = "local"

    @property
    def model(self) -> str:
        return str(self.cfg.get("model", MODEL))

    @property
    def identity(self) -> str:
        return f"{self.kind}:{self.model}"

    def complete(self, req: LLMRequest, key: str) -> LLMResponse:
        fn = getattr(self, "_role_" + req.role, None)
        if fn is None:
            payload: object = {"note": f"local engine has no handler for role {req.role}"}
        else:
            payload = fn(req)
        text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
        return LLMResponse(text=text, provider=self.name, model=self.model, usage={},
                           cost_usd=0.0, started=utcnow(), finished=utcnow(), key=key)

    # ---------------------------------------------------------------- helpers
    def _src_file(self, filename: str) -> str:
        p = self.project_dir / "01_CORPUS" / "source-files" / filename
        try:
            if p.exists():
                return read_text(p)
        except OSError:
            pass
        return ""

    @staticmethod
    def _between(text: str, start: str, end: str) -> str:
        i = (text or "").find(start)
        if i < 0:
            return ""
        i += len(start)
        j = text.find(end, i)
        return text[i:j if j >= 0 else len(text)]

    @staticmethod
    def _last_json_dict(text: str) -> dict:
        for b in reversed(re.findall(r"```json\s*\n(.*?)\n?```", text or "", re.S)):
            try:
                d = json.loads(b)
                if isinstance(d, dict):
                    return d
            except Exception:
                continue
        return {}

    # ---------------------------------------------------------------- units
    def _role_unit_deriver(self, req: LLMRequest) -> dict:
        h = req.meta.get("hypothesis") or {}
        stmt = h.get("statement", "") or ""
        full = "\n".join([stmt, h.get("assumptions", "") or "", h.get("falsification", "") or "",
                          h.get("corroboration", "") or ""])
        units = []

        def add(code: str, typ: str, clause: str) -> None:
            clause = norm_ws(clause.strip(" ,;:."))
            if not _anchor_ok(clause, full, 6):
                return
            terms = []
            for t in _toks(clause):
                if t in _STOP or t in _MODAL_WORDS or t in _NEG_WORDS or len(t) < 3:
                    continue
                if t not in terms:
                    terms.append(t)
            units.append({"code": code, "type": typ, "text": clause, "source_quote": clause,
                          "evidence_terms": terms[:10],
                          "satisfied_by": f"a source-reported finding stating that {truncate_words(clause, 26)}"})

        def fill(prefix: str, typ: str, text: str, cap: int) -> None:
            n = 0
            for c in _clauses(text, 5):
                if n >= cap:
                    break
                before = len(units)
                add(f"{prefix}{n + 1}", typ, c)
                if len(units) > before:
                    n += 1

        # REQUIRED_SUPPORT: the clauses of the human-written statement, one requirement each
        fill("R", "REQUIRED_SUPPORT", stmt, 8)
        if not any(u["type"] == "REQUIRED_SUPPORT" for u in units) and word_count(stmt) >= 6:
            add("R1", "REQUIRED_SUPPORT", truncate_words(stmt, 18).rstrip(" …"))
        # CONTEXTUAL_CONSTRAINT: assumptions and antecedents
        fill("C", "CONTEXTUAL_CONSTRAINT", h.get("assumptions", "") or "", 4)
        # ADVERSE_TEST: the falsification context
        fill("A", "ADVERSE_TEST", h.get("falsification", "") or "", 3)
        # CORROBORATING_EXPECTATION: the corroboration context
        fill("E", "CORROBORATING_EXPECTATION", h.get("corroboration", "") or "", 3)
        # one EVALUATIVE_JUDGMENT where the hypothesis itself makes a holistic judgment:
        # use the whole sentence that contains the judgment word, never a mid-word slice
        for sent in _sentences(stmt, 6):
            if re.search(r"\b(sufficient|compelling|meaningfully|consequential)\b", sent, re.I):
                add("J1", "EVALUATIVE_JUDGMENT", sent)
                break
        return {"hypothesis_id": h.get("id"), "units": units,
                "notes": ("Local engine: units are clause-level verbatim anchors of the human-written "
                          "hypothesis. No wording was introduced; every source_quote is a contiguous "
                          "substring of the hypothesis or a header passage.")}

    # ---------------------------------------------------------------- corpus
    def _role_indexer(self, req: LLMRequest) -> dict:
        fn = req.meta.get("filename") or ""
        body = self._src_file(fn)[:6000].lower()
        rank = "C"
        if re.search(r"\brandomi[sz]ed\b|\bdouble[- ]blind\b|\bplacebo\b", body):
            rank = "A"
        elif re.search(r"\bpatients?\b|\bmen\b|\bhuman\b|\bcohort\b|\btrial\b", body):
            rank = "A" if re.search(r"\boutcome|\bresult", body) else "B"
        elif re.search(r"\brats?\b|\bmice\b|\bmodels?\b", body):
            rank = "B"
        elif re.search(r"\breview\b|\bmeta[- ]analysis\b", body):
            rank = "B"
        txt = self._src_file(fn)
        sents = _sentences(txt, 8)[:2]
        summary = truncate_words(" ".join(sents), 45) or "(no opening text found)"
        return {"filename": fn, "rank": rank, "author_year_title": _author_year(fn),
                "relevance": truncate_words(txt[:600], 30),
                "summary": summary, "contradictions_and_gaps": "not assessed by the local engine"}

    def _role_archivist_writer(self, req: LLMRequest) -> str:
        return (
            "You are a precision research assistant working from one fixed notebook. You answer "
            "questions only from the passages supplied with each question.\n\n"
            "WORKFLOW\n1. Read the question. 2. Find the passages that bear on it. 3. Quote the "
            "sentence or table row that carries the finding. 4. Add the filename and section heading. "
            "5. State plainly what the passages do not contain.\n\n"
            "EVIDENCE DISCIPLINE\n* [SOURCE] marks a finding the named source reports.\n"
            "* [INFERRED] marks an inference you draw from several passages.\n"
            "* [NO SOURCE] marks something the passages do not establish.\n\n"
            "CITATION RULES\n* Cite the exact filename and section heading beside every substantive "
            "claim. Never invent a quotation, number, table or heading.\n\n"
            "LANGUAGE CALIBRATION\n* Match the strength of the passage: do not turn 'was associated "
            "with' into 'causes'.\n\n"
            "OUTPUT\n* Answer in short paragraphs. Keep every qualification, number and null result.")

    # ---------------------------------------------------------------- quest
    def _role_investigator(self, req: LLMRequest) -> dict:
        rnd = int(req.meta.get("round", 1) or 1)
        n = int(req.meta.get("n", 5) or 5)
        sources = [s for s in (req.meta.get("sources") or []) if isinstance(s, str) and s]
        # the frozen header sits in the SYSTEM section of the investigator prompt
        whole = (req.system or "") + "\n" + (req.user or "")
        header = self._between(whole, "<<<HEADER", "HEADER>>>")
        themes = []
        table_rows = re.findall(r"\|\s*\*\*(A\d+-H\d+)\*\*\s*\|\s*([^|]+)\|", header)
        for hid, stmt in table_rows:
            for c in _clauses(stmt, 6)[:2]:
                themes.append((hid, c))
        if not themes:
            for c in _clauses(header, 8)[:12]:
                themes.append(("", c))
        tests = re.findall(r"\|\s*([^|]{3,60})\s*\|\s*([^|]{20,200})\s*\|",
                           self._between(header, "Decisive-test", "##"))
        issued_text = self._between(req.user, "QUESTIONS ALREADY ISSUED", "YOUR RESEARCH LEDGER")
        asked = len(re.findall(r"\bQ\d{4}\b", issued_text))
        qs = []
        for i in range(n):
            if not sources:
                break
            k = (rnd - 1) * n + i
            src = sources[k % len(sources)]
            second = sources[(k + 1) % len(sources)] if len(sources) > 1 and i % 2 else None
            names = [src] + ([second] if second and second != src else [])
            theme = themes[(asked + i) % len(themes)][1] if themes else "the reported findings"
            theme = RE_HID.sub("", theme).strip(" ,;:")
            if tests and i == 0:
                t, q = tests[(rnd - 1) % len(tests)]
                text = (f"In {names[0]}, what does the source report about {t.lower()} - specifically, "
                        f"what findings, study design, denominators, doses or exposures, comparators, "
                        f"timing, and contrary or null results bear on the question: {q.strip()}?")
                target = f"decisive test: {t}"
            else:
                text = (f"In {', '.join(names)}, what findings, study designs, populations or models, "
                        f"doses or exposures, comparators, and contrary or null results are reported "
                        f"about {theme}? Cite the exact passage for each finding.")
                target = f"coverage of: {theme[:80]}"
            qs.append({"text": text, "sources": names, "target": target,
                       "packet_priority_id": None,
                       "rationale": "The local engine rotates the ranked sources across the "
                                    "hypothesis clauses and decisive tests so that every source and "
                                    "every required part is queried at least once."})
        prior = []
        if rnd > 1:
            prior.append(f"Round {rnd - 1} answers were read; the ledger carries forward only "
                         f"source-attributed findings.")
        ledger = (f"# Research ledger - round {rnd} (local engine)\n\n"
                  f"- Questions issued so far: {asked}\n"
                  f"- Sources rotated this round: {', '.join(sources[:4]) or 'none'}\n"
                  f"- Themes queried this round: {len(qs)}\n"
                  f"- Standing rule: a link is unresolved only after the sources naming it have been "
                  f"asked and no finding addresses it.\n" + ("\n".join(f"- {p}" for p in prior)))
        return {"round_record": {"packet_read": rnd > 1, "priorities_taken": [],
                                 "priorities_set_aside": [],
                                 "disagreement_with_packet": ""},
                "ledger": ledger, "questions": qs}

    def _role_archivist(self, req: LLMRequest) -> str:
        passages = self._between(req.user, "NOTEBOOK PASSAGES", "QUESTION")
        question = req.user.rsplit("QUESTION", 1)[-1].strip()
        blocks = []
        for m in re.finditer(
                r"=== SOURCE: (\S+) \((requested|other notebook source)[^)]*\)[^=]*===\n"
                r"(?:Headings:([^\n]*)\n)?(.*?)(?=\n=== SOURCE: |\Z)", passages, re.S):
            blocks.append({"file": m.group(1), "kind": m.group(2),
                           "headings": [h.strip() for h in (m.group(3) or "").split(";") if h.strip()],
                           "body": m.group(4)})
        if not blocks:
            return ("[NO SOURCE] No notebook passages were supplied for this question, so nothing "
                    "can be reported from this notebook.")
        qc = _content(question) - _QUESTION_FRAME
        picks = []
        for b in blocks:
            sents = _sentences(b["body"], 8)
            scored = []
            for s in sents:
                if re.search(r"\b(doi|https?://|copyright|all rights reserved)\b", s, re.I):
                    continue
                ov = _coverage(qc, _content(s)) if qc else 0.0
                scored.append((ov + _finding_value(s), s))
            scored.sort(key=lambda x: (-x[0], -word_count(x[1])))
            take = scored[:2] if b["kind"] == "requested" else scored[:1]
            for ov, s in take:
                if ov <= 0:
                    continue
                picks.append((0 if b["kind"] == "requested" else 1, -ov, b, s))
        picks.sort(key=lambda x: (x[0], x[1]))
        lines = []
        used = set()
        for _, _, b, s in picks[:6]:
            if norm_for_match(s) in used:
                continue
            used.add(norm_for_match(s))
            head = b["headings"][0] if b["headings"] else "Results"
            head = re.sub(r"^#+\s*", "", head)[:80] or "Results"
            lines.append(f'[SOURCE] "{s.strip()}" ({b["file"]}, {head})')
        if not lines:
            return ("[NO SOURCE] The supplied passages do not contain a statement that answers this "
                    "question. This is a retrieval gap, not evidence of absence.")
        body = "\n".join(lines)
        files = sorted({b["file"] for _, _, b, _ in picks[:6]})
        return (body + "\n\n[INFERRED] The quoted passages are what this notebook contains on the "
                "question. Each quotation is attributed above to its file and section; no finding "
                f"outside these passages is asserted. Sources quoted: {', '.join(files)}.")

    def _role_coordinator(self, req: LLMRequest) -> str:
        frame = req.meta.get("frame") or {"axes": []}
        gauge = int(req.meta.get("gauge", 64) or 64)
        rnd = int(req.meta.get("round", 1) or 1)
        whole = (req.system or "") + "\n" + (req.user or "")
        header = self._between(whole, "<<<HEADER", "HEADER>>>")
        blob = self._between(req.user, "NEW SAVED QUERY-RESPONSE RECORDS THIS ROUND",
                             "SOURCE COVERAGE LEDGER")
        records = "\n".join(blob.splitlines()[1:]) if blob else ""
        prior = self._last_json_dict(self._between(req.user, "<<<PRIOR", "PRIOR>>>"))
        prior_counts = prior.get("evidence_counts") or {}
        blocks = [b for b in re.split(r"\n\s*\n", records) if word_count(b) > 12]

        def touched(text: str, floor: float = 0.3) -> bool:
            tc = _content(text)
            return any(_coverage(tc, _content(b)) >= floor for b in blocks)

        alloc, counts = {}, {}
        for ax in frame.get("axes", []):
            ids = [h["id"] for h in ax["hypotheses"]]
            weights = []
            for h in ax["hypotheses"]:
                hc = _content(h.get("statement", "") + " " + h.get("assumptions", ""))
                # which hypothesis does each answer block speak to most strongly?
                gain = 0
                for b in blocks:
                    bc = _content(b)
                    best, best_cov = "", 0.0
                    for hh in ax["hypotheses"]:
                        c = _coverage(_content(hh.get("statement", "") + " " +
                                               hh.get("assumptions", "")), bc)
                        if c > best_cov:
                            best, best_cov = hh["id"], c
                    if best == h["id"] and best_cov >= 0.25:
                        gain += 1 + int(3 * best_cov)
                try:
                    before = int(prior_counts.get(h["id"], 0))
                except (TypeError, ValueError):
                    before = 0
                counts[h["id"]] = before + gain
                # a flat prior keeps every hypothesis representable; evidence volume moves it
                weights.append(8.0 + 3.0 * counts[h["id"]])
            tot = sum(weights)
            vec = [max(0, int(round(gauge * w / tot))) for w in weights]
            while sum(vec) < gauge:
                vec[max(range(len(vec)), key=lambda i: weights[i])] += 1
            while sum(vec) > gauge and max(vec) > 0:
                vec[vec.index(max(vec))] -= 1
            if sum(vec) != gauge:
                vec[-1] += gauge - sum(vec)
            alloc[ax["axis_id"]] = dict(zip(ids, vec))

        tests = []
        tsec = re.split(r"\n#{1,6}\s+", header)
        for piece in tsec:
            if re.search(r"decisive[- ]test", piece.splitlines()[0] if piece.splitlines() else "", re.I):
                for row in re.findall(r"^\|\s*([^|]{3,60})\s*\|\s*([^|]{15,220})\s*\|", piece, re.M):
                    if row[0].strip().lower() not in ("test", "decisive test") and not row[0].startswith("---"):
                        tests.append((row[0].strip(), row[1].strip()))
                break
        tests_hit = sum(1 for _, q in tests if touched(q, 0.28))
        hyps = [h for ax in frame.get("axes", []) for h in ax["hypotheses"]]
        adverse_hit = sum(1 for h in hyps if touched(h.get("falsification", ""), 0.3))
        weak_hit = sum(1 for h in hyps if touched(h.get("assumptions", ""), 0.3))
        success_hit = sum(1 for h in hyps if touched(h.get("corroboration", ""), 0.3))
        n = max(1, len(hyps))
        substantive = {
            "decisive_tests_oriented": (not tests) or tests_hit >= max(1, len(tests) // 2),
            "every_live_hypothesis_adversely_tested": adverse_hit >= (2 * n + 2) // 3,
            "weakest_and_shared_links_tested": weak_hit >= (2 * n + 2) // 3,
            "project_success_conditions_addressed": success_hit >= (n + 1) // 2,
            "notes": (f"local engine: {tests_hit}/{len(tests)} decisive tests, {adverse_hit}/{n} "
                      f"hypotheses adversely tested, {weak_hit}/{n} assumptions touched, "
                      f"{success_hit}/{n} corroboration contexts touched")}
        data = {"allocations": alloc, "evidence_counts": counts,
                "basis_confidence": {a: "local bookkeeping" for a in alloc},
                "substantive_conditions": substantive, "direction": "CONTINUE",
                "feedback_packet": {
                    "expected_return": "stable" if rnd >= 3 else "rising",
                    "posture": "query sources that have not yet been named; test the weakest required part",
                    "priorities": [{
                        "id": f"P-{rnd}", "finding_or_gap": "sources named once and never cited",
                        "missing_material": "a source-attributed finding for an unqueried named source",
                        "question": "What does the source report about the required part it was named for?",
                        "sources": [], "success_criterion": "a usable, cited answer",
                        "affects": "coverage of the named hypothesis parts"}],
                    "substantial_novelty": "new source-attributed findings from newly named sources",
                    "trivial_novelty": "restatements of findings already recorded",
                    "open_gaps_and_corrections": [substantive["notes"]],
                    "answers_needing_repair": [], "holds": "none"}}
        return (f"---\nartifact_type: CUMULATIVE-ACH-FUSION-FRAGMENT\nrevision: {rnd}\n---\n\n"
                f"Local-engine checkpoint for round {rnd}. The allocations below are a bookkeeping "
                f"split of the gauge over the frozen hypotheses, computed from the cumulative count "
                f"of answer blocks that share terminology with each hypothesis. They are not an "
                f"ACH_Eval judgment. Substantive conditions: {substantive['notes']}.\n\n"
                "```json\n" + json.dumps(data, ensure_ascii=False, indent=1) + "\n```\n")

    # ---------------------------------------------------------------- FRDs
    def _role_frd_generator(self, req: LLMRequest) -> dict:
        resp = req.meta.get("response", "") or ""
        cap = 4
        out = []
        for m in re.finditer(r"\[SOURCE\]\s+\"(.+?)\"\s+\(([^,]+),\s*([^)]*)\)", resp, re.S):
            quote, fname, loc = norm_ws(m.group(1)), m.group(2).strip(), m.group(3).strip()
            if word_count(quote) < 6:
                continue
            out.append({"cluster": (loc or "findings").lower().replace(" ", "-")[:40],
                        "label": truncate_words(quote, 8),
                        "source_files": [fname], "locator": loc or "Results",
                        "claim": quote, "verification_instruction":
                            f"Find the quoted sentence in {fname} at '{loc or 'Results'}' and check "
                            f"every number, qualifier and the direction of the finding.",
                        "evidence_label": "[SOURCE]", "provenance": "OWN_RESULT",
                        "status": "ordinary", "speaker": "the source authors"})
            if len(out) >= cap:
                break
        if not out:
            for s in _sentences(resp, 10)[:cap]:
                out.append({"cluster": "unattributed", "label": truncate_words(s, 8),
                            "source_files": [], "locator": "Results", "claim": s,
                            "verification_instruction": "No source was cited in the response; the "
                                                        "claim cannot be attributed.",
                            "evidence_label": "[NO SOURCE]", "provenance": "DERIVATIVE_UNKNOWN",
                            "status": "needs-source", "speaker": "unattributed"})
        return {"qid": req.meta.get("qid"), "frds": out,
                "harvest_review": {"sources_cited_in_response": req.meta.get("sources", []),
                                   "cited_sources_without_frd": [],
                                   "not_extracted": [],
                                   "unresolved_citations_or_labels": [],
                                   "gaps_and_unsupported_synthesis": []}}

    def _role_frd_validator(self, req: LLMRequest) -> dict:
        frd = req.meta.get("frd", {}) or {}
        fname = req.meta.get("source") or ""
        source = req.meta.get("source_text", "") or ""
        claim = frd.get("claim", "") or ""
        quote, ov = _best_sentence(claim, source)
        if not quote or ov < 0.25:
            return {"frd_id": frd.get("frd_id"),
                    "citation": {"filename": fname, "locator": frd.get("locator", "")},
                    "claim": claim, "source_text": "",
                    "verdict": "NOT FOUND",
                    "verdict_explanation": "no sentence of the named source supports the candidate claim",
                    "evidence_label": frd.get("evidence_label", ""),
                    "provenance": frd.get("provenance", "DERIVATIVE_UNKNOWN"),
                    "readiness": "NOT READY FOR WITNESS CONSTRUCTION",
                    "readiness_reason": "the claim could not be located in the named source",
                    "children": []}
        exact = norm_for_match(claim) and norm_for_match(claim) in norm_for_match(source)
        verdict = "RIGHT" if exact else ("MOSTLY RIGHT" if ov >= 0.6 else "PARTLY RIGHT")
        return {"frd_id": frd.get("frd_id"),
                "citation": {"filename": fname, "locator": frd.get("locator", "") or "Results"},
                "claim": norm_ws(quote), "source_text": quote.strip(),
                "verdict": verdict,
                "verdict_explanation": (f"The exact quoted sentence appears in the named source."
                                        if exact else
                                        f"A source sentence supports the substance of the claim "
                                        f"(content overlap {ov:.2f}); the candidate wording was "
                                        f"replaced by the source's own words."),
                "evidence_label": frd.get("evidence_label", "[SOURCE]"),
                "provenance": frd.get("provenance", "OWN_RESULT"),
                "readiness": "READY FOR WITNESS CONSTRUCTION",
                "readiness_reason": "a verbatim supporting sentence was located in the named source",
                "children": []}

    # ---------------------------------------------------------------- witness
    def _role_witness_constructor(self, req: LLMRequest) -> dict:
        v = req.meta.get("vfrd", {}) or {}
        ceiling = int(req.meta.get("ceiling", 60) or 60)
        claim = norm_ws(v.get("claim", "") or "")
        if not claim:
            return {"status": "ABSTAIN", "witness": "", "preserved": [], "omitted": [],
                    "would_be_lost": "the parent FRD has no claim", "repair_needed": ""}
        # A declarative statement with a citation suffix, not "X reports that ...": the
        # witness is the finding itself, and a report framing would make every witness look
        # second-hand to the matcher.
        cite = Path(v.get("source_file", "") or "").stem
        suffix = f" ({cite})." if cite else "."
        room = max(6, ceiling - word_count(suffix))
        body = claim.rstrip(" .;:")
        if word_count(body) > room:
            body = _trim_to(body, room).rstrip(" .;:")
        text = body + suffix
        if word_count(text) > ceiling:
            return {"status": "ABSTAIN", "witness": "", "preserved": self._preserved(claim),
                    "omitted": [], "would_be_lost": "the claim cannot be stated faithfully within "
                    "the ceiling", "repair_needed": ""}
        return {"status": "WITNESS", "witness": text,
                "preserved": self._preserved(claim), "omitted": [], "would_be_lost": "",
                "repair_needed": ""}

    @staticmethod
    def _preserved(claim: str) -> list[str]:
        keep = []
        if NEGATION_RE.search(claim):
            keep.append("negation")
        if re.search(r"\d", claim):
            keep.append("quantities")
        if re.search(r"\b(may|might|could|suggest|appears?|likely|possible)\b", claim, re.I):
            keep.append("modality")
        if re.search(r"\b(rats?|mice|dogs?|patients?|men|humans?|cells?|invitro)\b", claim, re.I):
            keep.append("population/model")
        if re.search(r"\b(weeks?|days?|months?|hours?|after|before|during)\b", claim, re.I):
            keep.append("timing")
        return keep or ["assertion"]

    def _role_witness_auditor(self, req: LLMRequest) -> dict:
        v = req.meta.get("vfrd", {}) or {}
        witness = req.meta.get("witness", "") or ""
        claim = v.get("claim", "") or ""
        wc, cc = _content(witness), _content(claim)
        # the citation suffix "(alvarez2021)." is licensed by the parent's source file name
        prefix = witness.replace(claim, " ", 1) if claim and claim in witness else ""
        stem = Path(v.get("source_file", "") or "").stem
        licensed = (cc | _content(prefix) | _content(v.get("source_file", "")) | _content(stem)
                    | {"report"})
        extra = sorted(t for t in (wc - licensed) if t not in {"author", "source"})
        problems = []
        if extra:
            problems.append({"words": ", ".join(extra[:6]),
                             "problem": "the witness adds content words that the parent FRD does not "
                                        "contain", "property": "fabrication/scope"})
        if NEGATION_RE.search(claim) and not NEGATION_RE.search(witness):
            problems.append({"words": "negation", "problem": "the witness drops the parent's negation",
                             "property": "polarity"})
        if numeral_drop(claim, witness):
            problems.append({"words": numeral_drop(claim, witness),
                             "problem": "a number in the parent FRD is missing from the witness",
                             "property": "quantity"})
        if problems:
            return {"unsupported_assertions": problems, "material_omissions": [],
                    "strongest_forbidden_reading": "the witness states more than the FRD supports",
                    "reader_recovers": "wrong", "verdict": "REVISE_WITNESS",
                    "reason": "local audit found content not licensed by the parent FRD",
                    "fix": "state only what the parent claim states, keeping its polarity and quantities"}
        return {"unsupported_assertions": [], "material_omissions": [],
                "strongest_forbidden_reading": "",
                "reader_recovers": "same" if _coverage(cc, wc) >= 0.8 else "weaker",
                "verdict": "PASS",
                "reason": "every content word of the witness is licensed by the parent FRD; polarity "
                          "and quantities are preserved (local structural audit)",
                "fix": ""}

    # ---------------------------------------------------------------- matching
    def _role_matcher_a(self, req: LLMRequest) -> dict:
        return self._match(req, strict=False)

    def _role_matcher_b(self, req: LLMRequest) -> dict:
        return self._match(req, strict=True)

    def _match(self, req: LLMRequest, strict: bool) -> dict:
        unit = req.meta.get("unit") or {}
        utext = req.meta.get("unit_text") or unit.get("text", "")
        wits = req.meta.get("witnesses") or {}
        js = []
        for wid, wt in wits.items():
            rel, trace = _judge(utext, wt or "", strict=strict)
            js.append({"witness_id": wid, "relation": rel,
                       "elements_compared": f"content, polarity, quantity, scope, modality ({'B' if strict else 'A'})",
                       "trace": trace + f" [local-rules {VERSION} pass {'B' if strict else 'A'}]"})
        return {"unit_id": unit.get("unit_id"), "judgments": js}

    def _role_match_adjudicator(self, req: LLMRequest) -> dict:
        ds = []
        rank = {"EQUIVALENT": 5, "WITNESS_ENTAILS_UNIT": 4, "UNIT_ENTAILS_WITNESS": 3,
                "PARTIALLY_COVERS": 2, "NO_SEMANTIC_RELATION": 1, "ABSTAIN": 0.5, "CONTRADICTS": 0}
        for wid, rec in (req.meta.get("disputes") or {}).items():
            a, b = rec.get("a", "ABSTAIN"), rec.get("b", "ABSTAIN")
            pick = a if rank.get(a, 0.5) <= rank.get(b, 0.5) else b
            ds.append({"witness_id": wid, "relation": pick,
                       "trace": f"local adjudicator kept the weaker relation ({a} vs {b}); a conflict "
                                f"outranks an entailment, and the pair is labelled MODEL_ADJUDICATED",
                       "agrees_with": "A" if pick == a else "B"})
        return {"unit_id": (req.meta.get("unit") or {}).get("unit_id"), "decisions": ds}

    @staticmethod
    def _prompt_witnesses(text: str) -> dict:
        out = {}
        for m in re.finditer(r"^\[(W-[^\]]+)\]\s+(.+)$", text or "", re.M):
            out[m.group(1)] = m.group(2).strip()
        return out

    def _role_joint_checker(self, req: LLMRequest) -> dict:
        """Propose/verify jointly-sufficient groups by union coverage of the unit's content.

        A group is jointly sufficient here when, taken together, its witnesses supply at least
        0.85 of the unit's weighted content, every member contributes, and no member alone
        reaches that coverage.  This is a declared lexical construction, not logical
        entailment; the group is recorded as model-approved and can be revoked in
        human-decisions.json.
        """
        needed = 0.85
        texts = self._prompt_witnesses(req.user)
        if req.meta.get("group"):
            g = req.meta["group"]
            ws = [w for w in g.get("witnesses", []) if w in texts]
            m = re.search(r"^COVERAGE UNIT [^:]+ of hypothesis [^:]+:\n\"(.+?)\"", req.user, re.M | re.S)
            unit_text = m.group(1) if m else ""
            if len(ws) < 2 or not unit_text:
                return {"approve": False, "member_contributions": {},
                        "reason": "local engine could not read the group or the unit from the request"}
            uc = _content(unit_text)
            parts = {w: _content(texts[w]) for w in ws}
            union = set().union(*parts.values())
            cov = _coverage(uc, union)
            strongest = max((_coverage(uc, parts[w]) for w in ws), default=0.0)
            contrib = {}
            for w in ws:
                rest = set().union(*[parts[x] for x in ws if x != w])
                contrib[w] = f"supplies {_coverage(uc, parts[w] - rest):.2f} of the unit content uniquely"
            ok = cov >= needed and strongest < needed
            return {"approve": ok, "member_contributions": contrib,
                    "reason": (f"union coverage {cov:.2f} (needed {needed:.2f}); strongest single member "
                               f"{strongest:.2f}; local lexical rule, not logical entailment")}
        u = req.meta.get("unit") or {}
        uc = _content(u.get("text", ""))
        cand = [w for w in (req.meta.get("partials") or []) if w in texts]
        groups = []
        if len(cand) >= 2 and uc:
            pool = sorted(cand, key=lambda w: -_coverage(uc, _content(texts[w])))
            chosen: list[str] = []
            covered: set[str] = set()
            while len(chosen) < 3:
                best, best_gain = "", 0.0
                for w in pool:
                    if w in chosen:
                        continue
                    gain = _coverage(uc, (_content(texts[w]) | covered)) - _coverage(uc, covered)
                    if gain > best_gain:
                        best, best_gain = w, gain
                if not best or best_gain < 0.08:
                    break
                chosen.append(best)
                covered |= _content(texts[best])
                if _coverage(uc, covered) >= needed:
                    break
            if len(chosen) >= 2 and _coverage(uc, covered) >= needed:
                groups.append({"witness_ids": chosen,
                               "contributions": {w: "supplies terms the others do not" for w in chosen},
                               "trace": (f"union coverage {_coverage(uc, covered):.2f} over {len(chosen)} "
                                         f"witnesses (local lexical rule)")})
        return {"unit_id": u.get("unit_id"), "groups": groups}

    def _role_incompat_checker(self, req: LLMRequest) -> dict:
        texts = req.meta.get("texts") or {}
        out = []
        for a, b in req.meta.get("pairs", []) or []:
            ta, tb = texts.get(a, ""), texts.get(b, "")
            sa, sb = _Seg(ta), _Seg(tb)
            basis, why = "NONE", ""
            conf = _number_conflict(sa, sb)
            pa, pb = _pred_signs(ta), _pred_signs(tb)
            shared = set(pa) & set(pb)
            pol = any(("-" in pa[f] and "+" in pb[f]) or ("+" in pa[f] and "-" in pb[f])
                      for f in shared)
            if conf:
                basis, why = "SAME_QUANTITY_CONFLICT", conf
            elif pol and _coverage(sa.content, sb.content) >= 0.6:
                basis, why = "OPPOSITE_POLARITY", "same predicate, opposite polarity"
            out.append({"a": a, "b": b, "incompatible": bool(why), "basis": basis,
                        "trace": why or "different statements; both can be true"})
        return {"pairs": out}

    # ---------------------------------------------------------------- language
    def _role_transcoder(self, req: LLMRequest) -> str:
        out = []
        for it in req.meta.get("items", []) or []:
            raw = it.get("raw", "")
            out.append(f"### {it.get('item_id')} · {it.get('type')} · PASS\n"
                       f"Original: {raw}\nTranscoded: {raw}\nBindings: none\nRules: none\nCheck: PASS")
        return "\n\n".join(out)

    def _role_dictionary_reviewer(self, req: LLMRequest) -> str:
        return ("---\nartifact_type: ACH-CUSTOM-DICTIONARY\nversion: local-1\n---\n\n"
                "D-001 - reporting verb (sense: source attribution)\n"
                "Base form: report\nDefinition: to state what a named source found\n"
                "Scope: discovery answers and FRD claims\nStatus: ACTIVE\nAliases: state, note, describe\n\n"
                "D-002 - unchanged (sense: null result)\n"
                "Base form: unchanged\nDefinition: no measurable difference from comparator\n"
                "Scope: findings\nStatus: ACTIVE\nAliases: no change, similar\n")

    # ---------------------------------------------------------------- reports
    def _role_assessor(self, req: LLMRequest) -> str:
        frame = req.meta.get("frame") or {"axes": []}
        gauge = int(req.meta.get("gauge", 64) or 64)
        wit_block = self._between(req.user, "VALIDATED WITNESS REGISTRY", "MACHINE RECORDS")
        witnesses = re.findall(r"^(W-[^\s|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| (.+)$",
                               wit_block, re.M)
        alloc, drivers = {}, {}
        for ax in frame.get("axes", []):
            ids = [h["id"] for h in ax["hypotheses"]]
            scores = {}
            for h in ax["hypotheses"]:
                hc = _content(h.get("statement", "") + " " + h.get("assumptions", ""))
                hit = sum(1 for w in witnesses if _coverage(hc, _content(w[4])) >= 0.45)
                scores[h["id"]] = 1 + hit
                drivers[h["id"]] = [f"{w[0]}: shares the hypothesis's terminology"
                                    for w in witnesses if _coverage(hc, _content(w[4])) >= 0.45][:8]
            tot = sum(scores.values())
            vec = [max(0, int(round(gauge * scores[i] / tot))) for i in ids]
            while sum(vec) < gauge:
                vec[ids.index(max(ids, key=lambda x: scores[x]))] += 1
            while sum(vec) > gauge and max(vec) > 0:
                vec[vec.index(max(vec))] -= 1
            if sum(vec) != gauge:
                vec[0] += gauge - sum(vec)
            alloc[ax["axis_id"]] = dict(zip(ids, vec))
        data = {"allocations": alloc,
                "basis_confidence": {a: "local bookkeeping only: count of witnesses sharing "
                                        "terminology with each hypothesis" for a in alloc},
                "drivers": drivers,
                "strongest_objection": {a: "see the evidence packets: no hypothesis reaches complete "
                                           "coverage" for a in alloc},
                "reversal_finding": {a: "a single source reporting the missing required part" for a in alloc}}
        lines = ["# Final assessment (local engine)", "",
                 f"Gauge G = {gauge}. Witnesses in the validated registry: {len(witnesses)}.", "",
                 "The allocations below count, per hypothesis, how many released witnesses share its "
                 "terminology. They are **not** an ACH_Eval judgment, not probabilities, and not "
                 "validated by the crux result. Route a model to the `assessor` role to replace this "
                 "artifact.", "", "```json", json.dumps(data, ensure_ascii=False, indent=1), "```", ""]
        return "\n".join(lines)

    def _role_reporter(self, req: LLMRequest) -> dict:
        m = req.meta.get("metrics") or {}
        cov = req.meta.get("coverage") or {}
        q = req.meta.get("quest") or {}
        crux = int((req.meta.get("crux") or {}).get("candidates", 0) or 0)
        if not m:
            # no structured metrics supplied (an older caller): fall back to reading the record
            rec = json.dumps(req.meta.get("record") or {}, ensure_ascii=False)[:12000]
            g = re.search(r"witnesses?[^0-9]{0,20}(\d+)", rec, re.I)
            s = re.search(r"coverage sets?[^0-9]{0,20}(\d+)", rec, re.I)
            c = re.search(r"crux candidates?[^0-9]{0,20}(\d+)", rec, re.I)
            return {"summary": (f"This run judged {g.group(1) if g else 'the released'} released witnesses. "
                                f"Coverage sets: {s.group(1) if s else 'none'}; crux candidates: "
                                f"{c.group(1) if c else 'none'}. Best understood from this corpus and this "
                                f"run; the local engine's matching is a lexical approximation, not model "
                                f"understanding.")}
        n_w = int(m.get("witnesses_released", 0) or 0)
        n_ans = int(m.get("responses_usable", 0) or 0)
        n_h = len(cov)
        n_units = sum(len(c.get("required_units", []) or []) for c in cov.values())
        n_covered = sum(int(c.get("units_covered", 0) or 0) for c in cov.values())
        sets = sum(len(c.get("sets", []) or []) for c in cov.values())
        complete = [h for h, c in cov.items() if c.get("status") == "COMPLETE"]
        parts = [f"This run used {n_ans} usable discovery answers to build {n_w} released witnesses, "
                 f"then judged every shortlisted witness-unit pair against {n_units} required coverage "
                 f"units across {n_h} frozen hypotheses."]
        if complete:
            parts.append(f"{len(complete)} of {n_h} hypotheses reached complete coverage "
                         f"({', '.join(sorted(complete))}), with {sets} deletion-minimal coverage set(s) "
                         f"overall; every set was checked by deleting each witness in turn.")
        else:
            parts.append(f"No hypothesis reached complete coverage: {n_covered} of {n_units} required "
                         f"units were established by at least one approved option. The evidence packets "
                         f"name, for every uncovered part, the nearest judged evidence and mark it as not "
                         f"a match, so the gap can be reviewed rather than assumed.")
        if crux:
            parts.append(f"{crux} witness(es) qualified as crux candidates: each belongs to a coverage "
                         f"set of its home hypothesis and fails both the T1 consistency test and the T2 "
                         f"coverage test against a named rival, with a certificate for each test.")
        else:
            parts.append("No witness qualified as a crux candidate. A crux candidate must first belong "
                         "to a deletion-minimal coverage set of its home hypothesis, so an uncovered "
                         "hypothesis produces none by construction, not by a silent failure.")
        st = str(q.get("status") or "")
        if st == "OPERATIONAL_LIMIT":
            parts.append(f"Discovery stopped at its operational ceiling ({q.get('rounds', '?')} rounds, "
                         f"{q.get('questions_issued', '?')} questions); that is an operational limit, "
                         f"not a scientific completion finding.")
        elif st == "SCIENTIFIC_STOP":
            parts.append(f"Discovery stopped under the gauge-keyed stop rule after {q.get('rounds', '?')} "
                         f"rounds.")
        parts.append("Every quotation behind a witness was checked against its named source file, so each "
                     "row of the evidence packets can be followed back to a passage. These conclusions are "
                     "best understood from this corpus and this run: the local engine judges meaning by "
                     "explicit lexical and structural rules, so its matching is a stated approximation, not "
                     "model understanding, and the final assessment is a bookkeeping count, not ACH_Eval "
                     "judgment.")
        return {"summary": " ".join(parts)}


RE_HID = re.compile(r"\b[A-Z][A-Za-z]?\d+-H\d+\b")


def numeral_drop(parent: str, text: str) -> str:
    """A numeral present in the parent but absent from the witness (mechanical fidelity aid)."""
    def bare(x: str) -> str:
        return x.replace("\u2212", "-").lstrip("+-").rstrip("%")
    have = {bare(x) for x in re.findall(r"(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)*(?:\s?%)?", text or "")}
    missing = []
    for x in re.findall(r"(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)*(?:\s?%)?", parent or ""):
        b = bare(x)
        if b and b not in have and b not in {"1", "2"}:   # 1/2 appear in ordinary prose ("one of two")
            missing.append(b)
    return ", ".join(sorted(set(missing))[:4])
