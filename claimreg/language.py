"""Phase IV language layer: custom dictionary, canonicalizer, transcoder (spec 21-23, 26).

``language.mode``:

* ``off`` (default) - the identity transcoder: transcoded text = raw text, status
  IDENTITY.  Recorded as a declared variant; nothing is hidden.
* ``labels`` - the user's own language tools, run unattended:
    1. dictionary: imported (``language.dictionary_file``: Mr. Dictionary
       Markdown or a flat JSON dictionary) or built with Superior Mr. Dictionary
       v5.1 for up to ``language.dictionary_passes`` passes;
    2. rulebook: imported (``language.rulebook_file``) or built with
       Mr. Canonicalizer v1.1 (one pass);
    3. Mr. Transcoder v1.0 on every released witness and every active
       coverage unit, in small batches, with only the relevant dictionary
       entries supplied.
  A mechanical check then compares raw and transcoded text (numbers, negation,
  modality, length).  Anything that fails is REVIEW and is withheld from
  matching (the raw witness is kept and reported).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .config import resolve_path
from .header import all_hypotheses, hypothesis_text
from .llm.base import LLMRequest
from .util import (atomic_write_text, chunked, modal_count, negation_count, numerals, read_json,
                   read_text, truncate_words, utcnow, word_count)

_ENTRY_MD = re.compile(r"^(D-\d{3,})\s+[—–-]+\s+(.+?)\s*$", re.M)


# --------------------------------------------------------------------------- #
# dictionary import / compile
# --------------------------------------------------------------------------- #

def compile_flat_json(d: dict) -> list[dict]:
    """ChatGPT-era flat dictionary JSON -> entry records for the transcoder."""
    out = []
    for e in d.get("entries", []):
        exs = []
        for x in (e.get("examples") or [])[:3]:
            if isinstance(x, dict):
                exs.append(x.get("sentence") or x.get("text") or x.get("verbatim") or "")
            elif isinstance(x, str):
                exs.append(x)
        klass = e.get("binding_class", "NO-BIND")
        status = e.get("status", "PROVISIONAL")
        block = "\n".join([
            f"{e['id']} — {e.get('label', e.get('base', ''))} [{klass} · {status}]",
            f"Base form: {e.get('base', '')}",
            f"Definition: {e.get('definition', '')}",
            f"Scope: {e.get('scope', '')}",
            f"Aliases: {'; '.join(e.get('aliases') or []) or 'none'}",
        ] + ([f"Examples: " + " | ".join(f'"{truncate_words(x, 45)}"' for x in exs if x)] if exs else []))
        out.append({"id": e["id"], "base": e.get("base", ""), "label": e.get("label", ""),
                    "aliases": e.get("aliases") or [], "binding_class": klass, "status": status,
                    "block": block})
    return out


def parse_markdown_dictionary(text: str) -> list[dict]:
    """Mr. Dictionary Markdown (fragment or compiled) -> entry records."""
    out = []
    marks = list(_ENTRY_MD.finditer(text))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        block = text[m.start():end].strip()
        label = m.group(2)
        base_m = re.search(r"^Base form:\s*(.+)$", block, re.M)
        al_m = re.search(r"^Aliases:\s*(.+)$", block, re.M)
        st_m = re.search(r"^Status:\s*(\w+)", block, re.M)
        status = st_m.group(1).upper() if st_m else ("ACTIVE" if "ACTIVE" in block[:400] else "PROVISIONAL")
        klass = "BIND" if status == "ACTIVE" else "NO-BIND"
        if re.search(r"\bREFERENCE\b", block[:300]):
            klass = "REFERENCE"
        base = base_m.group(1).strip() if base_m else re.sub(r"\s*\(.*$", "", label).strip()
        aliases = [a.strip() for a in re.split(r"[;,]", al_m.group(1))] if al_m else []
        aliases = [a for a in aliases if a and a.lower() not in ("none", "n/a", "-")]
        out.append({"id": m.group(1), "base": base, "label": label, "aliases": aliases,
                    "binding_class": klass, "status": status, "block": truncate_words(block, 260)})
    return out


def relevant_entries(entries: list[dict], text: str) -> list[dict]:
    low = text.lower()
    hits = []
    for e in entries:
        words = [e["base"]] + list(e.get("aliases", []))
        if any(w and re.search(r"\b" + re.escape(w.lower()) + r"(?:e?s)?\b", low) for w in words):
            hits.append(e)
    return hits


# --------------------------------------------------------------------------- #
# stages
# --------------------------------------------------------------------------- #

def _goal(frame):
    return frame["axes"][0].get("question", frame.get("title", "")) if frame.get("axes") else frame.get("title", "")


def _hyps_verbatim(frame):
    return "\n\n".join(hypothesis_text(h) for h in all_hypotheses(frame))


def language_stage(ctx) -> dict:
    lcfg = ctx.cfg["language"]
    mode = lcfg.get("mode", "off")
    if mode == "off":
        ctx.save("language", "LANGUAGE-STATUS.json",
                 {"mode": "off", "note": "identity transcoder; no dictionary or rulebook in use"}, "language-status")
        return {"mode": "off"}
    out = {"mode": mode}
    # ---- dictionary
    dfile = resolve_path(ctx.cfg, lcfg.get("dictionary_file"))
    if dfile and dfile.exists():
        if dfile.suffix.lower() == ".json":
            entries = compile_flat_json(read_json(dfile))
            dict_id = (read_json(dfile) or {}).get("id", dfile.stem)
        else:
            entries = parse_markdown_dictionary(read_text(dfile))
            dict_id = dfile.stem
        source = f"imported from {dfile}"
    else:
        frds = ctx.load("frds", "05_validated/retained-frds.json", default=None) or \
            ctx.load("frds", "05_validated/validated-frds.json", default=[]) or []
        frd_txt = "\n".join(f"[{v['vfrd_id']} | {v['source_file']}] CLAIM: {v['claim']}\n  SOURCE TEXT: "
                            f"{truncate_words(v.get('source_text', ''), 160)}" for v in frds)
        idx = read_text(ctx.p("frame", "index.md")) if ctx.p("frame", "index.md").exists() else ""
        from .index import parse_index
        ranks = parse_index(idx, ctx.corpus)["ranks"] if idx else {}
        fragments = sorted(ctx.p("discovery", "04_ach-eval-checkpoints").glob("R*-fragment.md"))
        trusted = read_text(fragments[-1]) if fragments else (
            "artifact_type: CUMULATIVE-ACH-FUSION-FRAGMENT\n(no discovery fragment available; frame only)\n"
            + _hyps_verbatim(ctx.frame))
        prior = "none"
        maxp = int(lcfg.get("dictionary_passes", 2))
        text = ""
        for p in range(1, maxp + 1):
            system, user, _ = ctx.prompts.render(
                "dictionary_pass.md", PASS=p, MAX_PASSES=maxp, GOAL=_goal(ctx.frame),
                HYPOTHESES=_hyps_verbatim(ctx.frame), TRUSTED_FRAGMENT=truncate_words(trusted, 9000),
                PRIOR=prior, FRDS=frd_txt, RANKS="\n".join(f"{k}: {v}" for k, v in sorted(ranks.items())) or "none")
            res = ctx.llm.call(LLMRequest(role="dictionary_reviewer", system=system, user=user,
                                          expect_json=False, tag=f"dictionary:pass{p}",
                                          max_output_tokens=32000, meta={"frds": frds}))
            text = res.text
            atomic_write_text(ctx.p("language", f"02_dictionary/mr-dictionary-pass{p}.md"), text)
            prior = text
            if "ACH-CUSTOM-DICTIONARY" in text[:2000]:
                break
        entries = parse_markdown_dictionary(text)
        dict_id = f"DICT-{ctx.run_id}"
        source = "built with Superior Mr. Dictionary v5.1"
    ctx.save("language", "02_dictionary/dictionary-entries.json",
             {"dictionary_id": dict_id, "source": source, "entries": entries}, "dictionary")
    out.update(dictionary_id=dict_id, entries=len(entries),
               active=sum(1 for e in entries if e["binding_class"] == "BIND"))
    # ---- rulebook
    rfile = resolve_path(ctx.cfg, lcfg.get("rulebook_file"))
    if rfile and rfile.exists():
        rule_text = read_text(rfile)
        rule_id = rfile.stem
    else:
        frds = ctx.load("frds", "05_validated/retained-frds.json", default=None) or []
        dict_text = "\n\n".join(e["block"] for e in entries if e["binding_class"] == "BIND")
        system, user, _ = ctx.prompts.render(
            "canonicalizer_pass.md", DICTIONARY=dict_text or "(no active entries)",
            HYPOTHESES=_hyps_verbatim(ctx.frame), PRIOR="none",
            FRDS="\n".join(f"- {truncate_words(v['claim'], 80)}" for v in frds[:60]))
        res = ctx.llm.call(LLMRequest(role="dictionary_reviewer", system=system, user=user, expect_json=False,
                                      tag="canonicalizer:pass1", max_output_tokens=32000))
        rule_text = res.text
        rule_id = f"RULEBOOK-{ctx.run_id}"
    atomic_write_text(ctx.p("language", "03_canonicalizer/rulebook.md"), rule_text)
    ctx.save("language", "LANGUAGE-STATUS.json",
             {"mode": mode, "dictionary_id": dict_id, "dictionary_source": source, "rulebook_id": rule_id,
              "rulebook_chars": len(rule_text), "time": utcnow()}, "language-status")
    out.update(rulebook_id=rule_id)
    return out


_ITEM = re.compile(r"^###\s+(\S+)\s*[·|]\s*([A-Z_]+)\s*[·|]\s*(PASS|REVIEW)\b", re.M)


def parse_transcoder(text: str) -> dict:
    out = {}
    marks = list(_ITEM.finditer(text or ""))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        block = text[m.end():end]

        def field(name):
            mm = re.search(rf"^\s*{name}:\s*(.*?)(?=^\s*(?:Original|Transcoded|Bindings|Rules|Check):|\Z)",
                           block, re.M | re.S)
            return re.sub(r"\s+", " ", mm.group(1)).strip() if mm else ""
        out[m.group(1)] = {"type": m.group(2), "status": m.group(3), "transcoded": field("Transcoded"),
                           "bindings": field("Bindings"), "rules": field("Rules"), "check": field("Check")}
    return out


def mechanical_conformance(raw: str, new: str, ceiling: int | None) -> dict:
    nr, nn = numerals(raw), numerals(new)
    issues = []
    if nr != nn:
        issues.append(f"numbers changed: removed {sorted(nr - nn)}, added {sorted(nn - nr)}")
    if negation_count(new) < negation_count(raw):
        issues.append("negation count dropped")
    if modal_count(new) < modal_count(raw):
        issues.append("modal/hedge count dropped")
    if ceiling and word_count(new) > ceiling:
        issues.append(f"{word_count(new)} words exceeds the transcoded ceiling {ceiling}")
    return {"ok": not issues, "issues": issues}


def transcode_stage(ctx) -> dict:
    lcfg = ctx.cfg["language"]
    mode = lcfg.get("mode", "off")
    witnesses = ctx.load("witnesses", "05_released/witnesses.json", default=[]) or []
    units = [u for u in (ctx.load("matching", "01_hypothesis-units/units.json", default=[]) or []) if u.get("active")]
    items = ([{"item_id": w["witness_id"], "type": "WITNESS", "raw": w["text"]} for w in witnesses]
             + [{"item_id": u["unit_id"], "type": "HYPOTHESIS", "raw": u["text"]} for u in units])
    if mode == "off":
        for it in items:
            it.update(transcoded=it["raw"], status="IDENTITY", bindings="", rules="", check="identity transcoder")
        ctx.save("transcoding", "transcoded.json", {"mode": "off", "items": items, "time": utcnow()}, "transcoded")
        return {"mode": "off", "items": len(items)}
    dic = ctx.load("language", "02_dictionary/dictionary-entries.json", default={}) or {}
    entries = dic.get("entries", [])
    rule_text = read_text(ctx.p("language", "03_canonicalizer/rulebook.md"))
    rule_text_short = truncate_words(rule_text, int(lcfg.get("rulebook_max_words", 7000)))
    status = ctx.load("language", "LANGUAGE-STATUS.json", default={}) or {}
    reqs, idx = [], []
    for bno, batch in enumerate(chunked(items, int(lcfg.get("transcode_batch", 8)))):
        btext = " ".join(i["raw"] for i in batch)
        rel = relevant_entries(entries, btext)
        dtext = "\n\n".join(e["block"] for e in rel) or "(no dictionary headword occurs in these items)"
        itxt = "\n\n".join(f"ITEM {i['item_id']} · {i['type']}\n{i['raw']}" for i in batch)
        system, user, _ = ctx.prompts.render("transcode.md", DICTIONARY_ID=status.get("dictionary_id", ""),
                                             DICTIONARY=dtext, RULEBOOK_ID=status.get("rulebook_id", ""),
                                             RULEBOOK=rule_text_short, ITEMS=itxt)
        reqs.append(LLMRequest(role="transcoder", system=system, user=user, expect_json=False,
                               tag=f"transcode:{bno}", meta={"items": batch}))
        idx.append(batch)
    results = ctx.llm.call_many(reqs)
    wc = int(ctx.cfg["witness"].get("transcoded_ceiling", 80))
    for batch, res in zip(idx, results):
        parsed = parse_transcoder(res.text if res else "")
        for it in batch:
            p = parsed.get(it["item_id"])
            if not p or not p["transcoded"]:
                it.update(transcoded=it["raw"], status="REVIEW", bindings="", rules="",
                          check="transcoder returned no block for this item", call_key=res.key if res else "")
                continue
            mc = mechanical_conformance(it["raw"], p["transcoded"], wc if it["type"] == "WITNESS" else None)
            st = p["status"] if mc["ok"] else "REVIEW"
            it.update(transcoded=p["transcoded"], status=st, bindings=p["bindings"], rules=p["rules"],
                      check=p["check"] + ("" if mc["ok"] else " | mechanical: " + "; ".join(mc["issues"])),
                      mechanical=mc, call_key=res.key if res else "")
    ctx.save("transcoding", "transcoded.json",
             {"mode": mode, "dictionary_id": status.get("dictionary_id"), "rulebook_id": status.get("rulebook_id"),
              "items": items, "time": utcnow()}, "transcoded")
    return {"mode": mode, "items": len(items), "pass": sum(1 for i in items if i["status"] == "PASS"),
            "review": sum(1 for i in items if i["status"] == "REVIEW")}
