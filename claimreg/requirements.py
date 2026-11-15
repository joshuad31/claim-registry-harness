"""Hypothesis-to-requirements view: how each hypothesis was compiled into units, in words.

Coverage and the crux tests are run against the units a hypothesis was compiled into, not against
its sentences.  A missed or over-strict required unit decides a result, and nobody can see that
without opening JSON.  This view puts the compilation in front of the reader before coverage:

* the hypothesis as written, sentence by sentence;
* which units each sentence produced, and which sentences produced none
  ("written by you, checked by nothing");
* each unit's role, anchor, state and coverage options;
* how conjunctions and alternatives were read;
* what is not a requirement at all;
* what complete coverage would, and would not, let a reader conclude.

It is computed from saved records only (the frozen frame, the units, the coverage record and the
premise ledger).  It makes no model call, it is not an approval gate, and it changes no result.
Where the record does not hold something (for example why a sentence was divided as it was), the
view says NOT RECORDED; it never reconstructs a reason and presents it as history.
"""

from __future__ import annotations

import re

from .corpus import find_quote
from .units import constraint_kind
from .util import atomic_write_text, norm_for_match, tokens, truncate_words, utcnow

PARTS = (("statement", "Statement"), ("assumptions", "Assumptions and antecedents"),
         ("falsification", "Potential falsification"), ("corroboration", "Potential corroboration"))

ROLE = {"REQUIRED_SUPPORT": "must be supported", "PREMISE": "must not be contradicted",
        "BOUNDARY": "the hypothesis is about", "ADVERSE_TEST": "visible, not required (would count against)",
        "CORROBORATING_EXPECTATION": "visible, not required (expected)",
        "EVALUATIVE_JUDGMENT": "not a requirement (judged in the final assessment)"}

NOT_RECORDED = "NOT RECORDED"

# words after which a full stop does not end a sentence
_ABBREV = r"(?:e\.g|i\.e|vs|cf|et al|approx|Fig|No|Dr|St|resp|incl|ca)\."
_SENT_END = re.compile(r"(?<=[.!?])[\"')\]]?\s+(?=[\"'(\[]?[A-Z0-9])")


def split_sentences(text: str) -> list[str]:
    """Sentences of a short human-written passage.  Mechanical: a full stop, question mark or
    exclamation mark followed by a space and a capital or digit, except after a common abbreviation."""
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return []
    out, start = [], 0
    for m in _SENT_END.finditer(text):
        head = text[start:m.start()]
        if re.search(_ABBREV + r"$", head) or re.search(r"\(\w{1,3}\)$|\b[ivx]{1,4}\)$", head):
            continue
        out.append(head.strip())
        start = m.end()
    out.append(text[start:].strip())
    return [s for s in out if s]


def _occurrences(hay: str, needle: str) -> list[int]:
    out, i = [], hay.find(needle)
    while i != -1:
        out.append(i)
        i = hay.find(needle, i + 1)
    return out


def locate(quote: str, sentences: list[dict], other_text: str) -> dict:
    """Where a unit's anchoring quotation sits.

    {"where": "hypothesis", "sentences": [n, ...], "occurrences": k, "method": ...}  in this hypothesis
    {"where": "header"}        in the header passages or another hypothesis's text
    {"where": "unanchored"}    nowhere: the unit is inactive
    A quotation found more than once is reported with every place it occurs, never only the first."""
    nq = norm_for_match(quote or "")
    if not nq:
        return {"where": "unanchored", "sentences": [], "occurrences": 0, "method": "none"}
    # the whole text normalised at once (normalisation closes up spaces around punctuation, so
    # sentences cannot be normalised one by one and joined); each sentence's span is read off the
    # normalised length of the text up to and including it
    spans, start = [], 0
    for i, s in enumerate(sentences):
        end = len(norm_for_match(" ".join(x["text"] for x in sentences[:i + 1])))
        spans.append((start, end, s["n"]))
        start = end
    hay = norm_for_match(" ".join(x["text"] for x in sentences))
    hits = _occurrences(hay, nq)
    if hits:
        ns_ = sorted({n for i in hits for a, b, n in spans if i < b and i + len(nq) > a})
        return {"where": "hypothesis", "sentences": ns_, "occurrences": len(hits), "method": "exact"}
    # not word for word in one place: the same check the compiler used, sentence by sentence
    found = [s["n"] for s in sentences if find_quote(s["text"], quote, 0.9).get("found")]
    if found:
        return {"where": "hypothesis", "sentences": found, "occurrences": len(found), "method": "checked"}
    whole = find_quote(" ".join(s["text"] for s in sentences), quote, 0.9)
    if whole.get("found"):
        return {"where": "hypothesis", "sentences": [], "occurrences": 1, "method": whole.get("method", "checked"),
                "note": "the quotation joins passages of this hypothesis; it is not inside one sentence"}
    if other_text and find_quote(other_text, quote, 0.9).get("found"):
        return {"where": "header", "sentences": [], "occurrences": 1, "method": "checked"}
    return {"where": "unanchored", "sentences": [], "occurrences": 0, "method": "none"}


_ALT_HEAD = re.compile(r"^\s*at least one of the following\b", re.I)
_ALT_ITEM = re.compile(r"\(([a-z])\)\s*")
_ALT_OTHER = re.compile(r"\b(?:either|any one of|any of the following|one or more of|at least one of)\b", re.I)


def reading_of(text: str) -> dict:
    """How one unit's text reads: SINGLE, ANY_OF with its alternatives (the form the unit prompt
    prescribes: "At least one of the following ...: (a) ...; (b) ..."), or UNCLEAR when it seems to
    list alternatives in another form and a person should look."""
    marks = list(_ALT_ITEM.finditer(text or ""))
    if _ALT_HEAD.search(text or "") and len(marks) >= 2:
        items = []
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            items.append({"label": m.group(1), "text": text[m.end():end].strip(" ;.")})
        return {"reading": "ANY_OF", "alternatives": items}
    if len(marks) >= 2 or _ALT_OTHER.search(text or ""):
        return {"reading": "UNCLEAR", "alternatives": [],
                "note": "may list alternatives in a form other than the prescribed one; for a person to check"}
    return {"reading": "SINGLE", "alternatives": []}


def _role(u: dict, kinds: dict) -> str:
    if u["type"] == "CONTEXTUAL_CONSTRAINT":
        return ROLE[constraint_kind(u, kinds)]
    return ROLE.get(u["type"], u["type"])


def build_view(frame: dict, units: list[dict], coverage: dict, ledger: dict,
               header_text: str = "", constraint_kinds: dict | None = None) -> dict:
    kinds = constraint_kinds or {}
    led = (ledger or {}).get("hypotheses", {})
    all_hyp_text = {h["id"]: " ".join(str(h.get(k) or "") for k, _ in PARTS)
                    for ax in frame.get("axes", []) for h in ax.get("hypotheses", [])}
    extra = "\n".join([header_text or "", str(frame.get("mission") or ""),
                       "\n".join(f"{t.get('test', '')}: {t.get('question', '')}"
                                 for t in frame.get("decisive_tests") or [])])
    out = {}
    for ax in frame.get("axes", []):
        ids = [h["id"] for h in ax.get("hypotheses", [])]
        for h in ax.get("hypotheses", []):
            hid = h["id"]
            sentences, n = [], 0
            for key, label in PARTS:
                for s in split_sentences(str(h.get(key) or "")):
                    n += 1
                    sentences.append({"n": n, "part": key, "part_label": label, "text": s, "units": []})
            mine = [u for u in units if u.get("hypothesis_id") == hid]
            cov = coverage.get(hid, {}) or {}
            status_of = {r["unit_id"]: r for r in led.get(hid, [])}
            other = extra + "\n" + "\n".join(t for k, t in all_hyp_text.items() if k != hid)
            uviews, header_anchors, unanchored, ambiguous = [], [], [], []
            for u in mine:
                loc = locate(u.get("source_quote", ""), sentences, other)
                for sn in loc["sentences"]:
                    sentences[sn - 1]["units"].append(u["unit_id"])
                if loc["where"] == "header":
                    header_anchors.append(u["unit_id"])
                elif loc["where"] == "unanchored":
                    unanchored.append(u["unit_id"])
                if loc["occurrences"] > 1:
                    ambiguous.append({"unit_id": u["unit_id"], "occurrences": loc["occurrences"],
                                      "sentences": loc["sentences"]})
                opts = (cov.get("options") or {}).get(u["unit_id"], [])
                row = status_of.get(u["unit_id"], {})
                kind = constraint_kind(u, kinds)
                uviews.append({
                    "unit_id": u["unit_id"], "type": u["type"], "role": _role(u, kinds),
                    **({"constraint_kind": kind} if kind else {}),
                    "text": u.get("text", ""), "anchor_quote": u.get("source_quote", ""), "anchor": loc,
                    "quote_check_method": (u.get("quote_check") or {}).get("method", ""),
                    "serves": u.get("serves", ""), "satisfied_by": u.get("satisfied_by", ""),
                    "status": row.get("status", "" if u.get("active") else "NOT_MATCHED"),
                    "active": bool(u.get("active")), "inactive_reason": u.get("inactive_reason", ""),
                    "derived_type": u.get("derived_type", ""),
                    "reading": reading_of(u.get("text", "")) if u["type"] == "REQUIRED_SUPPORT" else None,
                    "coverage": ({"strict_options": sum(1 for o in opts if not o.get("assumption")),
                                  "conditional_options": sum(1 for o in opts if o.get("assumption")),
                                  "witnesses": sorted({w for o in opts for w in o["witnesses"]})}
                                 if u["type"] == "REQUIRED_SUPPORT" and u.get("active") else None),
                    # the compiler returns no reason for dividing a sentence as it did
                    "derivation_rationale": NOT_RECORDED})
            by_id = {u["unit_id"]: u for u in uviews}
            req = [u for u in uviews if u["type"] == "REQUIRED_SUPPORT" and u["active"]]
            # how the text was read
            conj = [{"sentence": s["n"], "units": [x for x in s["units"] if x in {u["unit_id"] for u in req}]}
                    for s in sentences]
            conj = [c for c in conj if len(c["units"]) >= 2]
            alts = [{"unit_id": u["unit_id"], "alternatives": u["reading"]["alternatives"]}
                    for u in req if u["reading"]["reading"] == "ANY_OF"]
            unclear = [u["unit_id"] for u in req if u["reading"]["reading"] == "UNCLEAR"]
            # diagnostics: shown, never enforced
            same, seen = [], {}
            for u in req:
                k = norm_for_match(u["anchor_quote"])
                if k:
                    seen.setdefault(k, []).append(u["unit_id"])
            same = [v for v in seen.values() if len(v) > 1]
            # words each required unit uses that its anchor sentence does not: one comparable number per
            # unit, so a reader sees which unit was elaborated most.  A rough count, not a judgment.
            added_words = []
            for u in req:
                anchor_s = " ".join(sentences[i - 1]["text"] for i in u["anchor"]["sentences"])
                if anchor_s:
                    added = sorted(set(tokens(u["text"])) - set(tokens(anchor_s)))
                    added_words.append({"unit_id": u["unit_id"], "count": len(added), "words": added[:12]})
            added_words.sort(key=lambda a: (-a["count"], a["unit_id"]))
            part_of = {s["n"]: s for s in sentences}
            # a required unit licensed by text that only says what would corroborate or falsify
            off_statement = [{"unit_id": u["unit_id"],
                              "part": part_of[u["anchor"]["sentences"][0]]["part_label"]}
                             for u in req if u["anchor"]["sentences"]
                             and all(part_of[n]["part"] in ("corroboration", "falsification")
                                     for n in u["anchor"]["sentences"])]
            short = [{"unit_id": u["unit_id"], "words": len(u["anchor_quote"].split())}
                     for u in req if 0 < len(u["anchor_quote"].split()) < 6]
            sets = cov.get("sets") or []
            first = sets[0] if sets else {}
            evaluative = [u for u in uviews if u["type"] == "EVALUATIVE_JUDGMENT"]
            out[hid] = {
                "axis_id": ax.get("axis_id"), "hypothesis_id": hid, "title": h.get("title", ""),
                "rivals": [i for i in ids if i != hid],
                "as_written": {k: str(h.get(k) or "") for k, _ in PARTS},
                "sentences": sentences,
                # a bare "Yes." or "No." asserts nothing a unit could represent
                "unmapped_sentences": [s["n"] for s in sentences if not s["units"] and len(s["text"].split()) >= 3],
                "header_anchored_units": header_anchors, "unanchored_units": unanchored,
                "units": uviews,
                "how_read": {
                    "solver_rule": "The solver requires every \"must be supported\" unit together (a conjunction); "
                                   "alternatives inside one unit count as one requirement.",
                    "this_is": "how the text was compiled for the solver, not a finding that the text means it",
                    "conjunctions": conj, "alternatives": alts, "alternatives_unclear": unclear,
                    "why_divided_this_way": NOT_RECORDED},
                "not_requirements": {
                    "evaluative": [{"unit_id": u["unit_id"], "text": u["text"], "derived_type": u["derived_type"],
                                    "reason": u["inactive_reason"]} for u in evaluative],
                    "inactive": [{"unit_id": u["unit_id"], "type": u["type"], "text": u["text"],
                                  "reason": u["inactive_reason"]} for u in uviews
                                 if not u["active"] and u["type"] != "EVALUATIVE_JUDGMENT"]},
                "coverage": {
                    "status": cov.get("status", ""), "sets": len(sets),
                    "required": len(req),
                    "covered_directly": sum(1 for u in req if u["coverage"]["strict_options"]),
                    "covered_only_with_a_transfer": sum(1 for u in req if not u["coverage"]["strict_options"]
                                                        and u["coverage"]["conditional_options"]),
                    "example_set": {"set_id": first.get("set_id", ""),
                                    "transfers_granted_for_support": first.get("assumptions", []),
                                    "contrary_findings_assumed_not_to_transfer":
                                        first.get("contrary_assumed_not_to_transfer", [])}},
                "diagnostics": {
                    "note": "mechanical hints for a reader; none of them changes a result",
                    "required_units_without_an_option": [u["unit_id"] for u in req
                                                         if not (u["coverage"]["strict_options"]
                                                                 or u["coverage"]["conditional_options"])],
                    "required_units_anchored_on_the_same_words": same,
                    "anchor_occurs_more_than_once": ambiguous,
                    "required_units_anchored_only_on_corroboration_or_falsification_text": off_statement,
                    "required_units_with_an_anchor_under_six_words": short,
                    "words_added_beyond_the_anchor_sentence": added_words},
                "counts": {t: sum(1 for u in uviews if u["type"] == t)
                           for t in ("REQUIRED_SUPPORT", "CONTEXTUAL_CONSTRAINT", "ADVERSE_TEST",
                                     "CORROBORATING_EXPECTATION", "EVALUATIVE_JUDGMENT")}}
            del by_id
            means, not_ = permits(out[hid])
            out[hid]["complete_coverage"] = {"means": means, "does_not_mean": not_}
    return {"hypotheses": out, "time": utcnow(),
            "note": "computed from saved records; no model call; not an approval gate; changes no result"}


def permits(v: dict) -> tuple[list[str], list[str]]:
    """What complete coverage of this hypothesis means and does not mean: a fixed template filled
    from the record, in the solver's own terms."""
    c = v["coverage"]
    ex = c["example_set"]
    n = c["required"]
    if not n:
        return (["This hypothesis has no finding-sized requirement of its own, so there is nothing for "
                 "witnesses to cover. It holds to the extent its rivals' required parts stay uncovered or "
                 "contested."], _DOES_NOT_MEAN)
    means = [f"Each of the {n} parts listed as \"must be supported\" is made true by at least one released "
             "witness, accepted as written" + (", or under a transfer the set names" if
                                               c["covered_only_with_a_transfer"] or ex[
                                                   "transfers_granted_for_support"] else "") + ".",
             "No witness in the set is known to contradict a listed premise outright. \"No known "
             "contradiction\" is not \"shown to hold\": a premise nobody tested is not thereby satisfied.",
             "The set contains no pair of witnesses approved as incompatible."]
    if ex["transfers_granted_for_support"] or ex["contrary_findings_assumed_not_to_transfer"]:
        means.append(f"As it stands, the example set grants {len(ex['transfers_granted_for_support'])} transfer(s) "
                     f"for support and assumes {len(ex['contrary_findings_assumed_not_to_transfer'])} contrary "
                     "finding(s) from another scope do not transfer. Coverage holds only if those are accepted.")
    return means, _DOES_NOT_MEAN


_DOES_NOT_MEAN = [
    "that the hypothesis is true, or that its rivals are false;",
    "that the judgments listed under \"Not requirements\" are right: those are made in the final assessment;",
    "that the adverse tests came out negative: they are shown, not required;",
    "that the witnesses are independent studies (see the study map), or that the studies are sound;",
    "that the units are a faithful reading of the hypothesis: check that against the sentences above."]


def render_view(view: dict, frame: dict) -> str:
    L = ["# How each hypothesis was compiled into requirements", "",
         "Coverage sets and crux tests are decided against the *units* below, not against the hypothesis "
         "sentences. Read this before the coverage and crux results: a sentence no unit represents is invisible "
         "to both, and a unit stricter than its sentence makes coverage harder than the author asked for. "
         "This page is computed from saved records. It makes no model call, it is not an approval step and it "
         "changes no result.", ""]
    for ax in frame.get("axes", []):
        L += [f"## Axis {ax.get('axis_id')}: {truncate_words(ax.get('question', ''), 45)}", ""]
        for h in ax.get("hypotheses", []):
            v = view["hypotheses"].get(h["id"])
            if not v:
                continue
            by_id = {u["unit_id"]: u for u in v["units"]}
            c = v["counts"]
            L += [f"### {v['hypothesis_id']} - {v['title']}", "",
                  f"{c['REQUIRED_SUPPORT']} required, {c['CONTEXTUAL_CONSTRAINT']} constraint, {c['ADVERSE_TEST']} "
                  f"adverse-test, {c['CORROBORATING_EXPECTATION']} expected and {c['EVALUATIVE_JUDGMENT']} "
                  "evaluative unit(s).", ""]
            if v["rivals"]:
                L += [f"This is the compiled theory the crux tests are run against when a witness of "
                      f"{', '.join(v['rivals'])} is tested against {v['hypothesis_id']}.", ""]
            # 1-2: the text and what each sentence produced
            L += ["#### The hypothesis as written, and what each sentence produced", ""]
            part = None
            for s in v["sentences"]:
                if s["part"] != part:
                    L += ([""] if part else []) + [f"*{s['part_label']}*", ""]
                    part = s["part"]
                L.append(f"{s['n']}. {s['text']}")
                for uid in s["units"]:
                    u = by_id[uid]
                    L.append(f"   - `{uid}` ({u['role']}), anchored on: \"{truncate_words(u['anchor_quote'], 30)}\"")
                if not s["units"]:
                    L.append("   - *no unit*")
            L.append("")
            if v["unmapped_sentences"]:
                L += ["**Written by you, checked by nothing.** No unit is anchored on these sentences, so "
                      "neither coverage nor the crux tests see them: "
                      + ", ".join(f"sentence {n}" for n in v["unmapped_sentences"]) + ".", ""]
            else:
                L += ["Every sentence has at least one unit anchored on it.", ""]
            if v["header_anchored_units"]:
                L += ["Units anchored on header passages or another hypothesis's text, not on this hypothesis: "
                      + ", ".join(f"`{x}`" for x in v["header_anchored_units"]) + ".", ""]
            # 3: the requirements table
            L += ["#### Requirements", "",
                  "| Unit | Role | Text | Serves | Satisfied by | State | Options | Active |",
                  "|---|---|---|---|---|---|---|---|"]
            for u in v["units"]:
                if u["type"] == "EVALUATIVE_JUDGMENT":
                    continue
                cov = u["coverage"]
                opt = (f"{cov['strict_options']} direct, {cov['conditional_options']} with a transfer"
                       if cov else "-")
                cell = lambda x: str(x or "").replace("|", "/").replace("\n", " ")
                L.append(f"| `{u['unit_id']}` | {u['role']} | {cell(u['text'])} | {cell(u['serves'])} | "
                         f"{cell(u['satisfied_by'])} | {cell(u['status']).replace('_', ' ').lower()} | {opt} | "
                         + ("yes" if u["active"] else "no: " + cell(u["inactive_reason"])) + " |")
            L.append("")
            # 4: how the text was read
            hr = v["how_read"]
            L += ["#### How the text was read", "",
                  f"{hr['solver_rule']} That is {hr['this_is']}.", ""]
            for cj in hr["conjunctions"]:
                L.append(f"- Sentence {cj['sentence']} was read as requiring ALL of: "
                         + ", ".join(f"`{x}`" for x in cj["units"]) + ".")
            for a in hr["alternatives"]:
                L.append(f"- `{a['unit_id']}` was read as requiring ANY ONE of: "
                         + "; ".join(f"({x['label']}) {x['text']}" for x in a["alternatives"])
                         + ". It is one requirement: one witness satisfying any alternative covers it.")
            for x in hr["alternatives_unclear"]:
                L.append(f"- `{x}` may list alternatives in a form other than the prescribed one; for a person "
                         "to check.")
            if c["REQUIRED_SUPPORT"] > 1:
                L.append(f"- All {c['REQUIRED_SUPPORT'] - len(v['not_requirements']['inactive'])} active required "
                         "units must be covered for complete coverage."
                         if not v["not_requirements"]["inactive"] else
                         "- Every active required unit must be covered for complete coverage.")
            L += [f"- Why each sentence was divided as it was: {hr['why_divided_this_way']} (the unit compiler "
                  "returns no rationale).", ""]
            # 5: not requirements
            nr = v["not_requirements"]
            if nr["evaluative"] or nr["inactive"]:
                L += ["#### Not requirements", "",
                      "These are judged in the final assessment, not by witness matching.", ""]
                for e in nr["evaluative"]:
                    L.append(f"- `{e['unit_id']}` {e['text']}"
                             + (f" - recorded as {e['derived_type'].replace('_', ' ').lower()} by the compiler and "
                                f"demoted: {e['reason']}" if e["derived_type"] else ""))
                for e in nr["inactive"]:
                    L.append(f"- `{e['unit_id']}` ({e['type'].replace('_', ' ').lower()}, not used): {e['text']} - "
                             f"{e['reason']}")
                L.append("")
            # 6: what coverage permits
            means, not_ = v["complete_coverage"]["means"], v["complete_coverage"]["does_not_mean"]
            cv = v["coverage"]
            L += ["#### What complete coverage of this hypothesis would let a reader conclude", "",
                  f"State in this run: **{cv['status'] or 'n/a'}**"
                  + (f"; {cv['covered_directly']} of {cv['required']} required parts have a direct match, "
                     f"{cv['covered_only_with_a_transfer']} only with a transfer; {cv['sets']} minimal set(s)."
                     if cv["required"] else "."), "", "It means:", ""]
            L += [f"- {m}" for m in means]
            L += ["", "It does not mean:", ""] + [f"- {m}" for m in not_] + [""]
            # diagnostics
            dg = v["diagnostics"]
            lines = []
            for x in dg["required_units_without_an_option"]:
                lines.append(f"- `{x}` has no coverage option: nothing in the registry covers it, even with a transfer.")
            for grp in dg["required_units_anchored_on_the_same_words"]:
                lines.append("- " + ", ".join(f"`{x}`" for x in grp) + " are anchored on the same words: possibly "
                             "one requirement counted twice.")
            for a in dg["anchor_occurs_more_than_once"]:
                lines.append(f"- The anchor of `{a['unit_id']}` occurs {a['occurrences']} times in this hypothesis "
                             f"(sentences {', '.join(map(str, a['sentences']))}); which one licensed the unit is "
                             f"{NOT_RECORDED}.")
            for a in dg["required_units_anchored_only_on_corroboration_or_falsification_text"]:
                lines.append(f"- `{a['unit_id']}` is a requirement, but its anchor is in the \"{a['part']}\" text, "
                             "which says what would be expected or would count against, not what the hypothesis "
                             "asserts. Check that the hypothesis needs it.")
            for a in dg["required_units_with_an_anchor_under_six_words"]:
                lines.append(f"- `{a['unit_id']}` is anchored on {a['words']} words; the unit compiler is asked for at "
                             "least six, so most of this unit's content is the compiler's elaboration.")
            if dg["words_added_beyond_the_anchor_sentence"]:
                lines.append("- Content words each required unit uses that its anchor sentence does not (a rough "
                             "count of how far the unit was elaborated, not a judgment): "
                             + ", ".join(f"`{a['unit_id']}` {a['count']}"
                                         for a in dg["words_added_beyond_the_anchor_sentence"]) + ".")
            for x in v["unanchored_units"]:
                lines.append(f"- `{x}` has no anchor in the frozen text and is not used.")
            if lines:
                L += ["#### Worth a look", "", "Mechanical hints; none of them changes a result.", ""] + lines + [""]
    return "\n".join(L) + "\n"


def write_view(ctx, coverage: dict, ledger: dict | None = None) -> dict:
    units = ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or []
    if ledger is None:
        ledger = ctx.load("coverage", "premise-ledger.json", default={}) or {}
    hp = ctx.p("frame", "header.md")
    from .util import read_text
    header_text = read_text(hp) if hp.exists() else ""
    view = build_view(ctx.frame, units, coverage, ledger, header_text,
                      dict(ctx.cfg["coverage"].get("constraint_kinds") or {}))
    ctx.save("coverage", "HYPOTHESIS-REQUIREMENTS.json", view, "hypothesis-requirements")
    atomic_write_text(ctx.p("coverage", "HYPOTHESIS-REQUIREMENTS.md"), render_view(view, ctx.frame))
    return {h: {"sentences": len(v["sentences"]), "unmapped": len(v["unmapped_sentences"])}
            for h, v in view["hypotheses"].items()}
