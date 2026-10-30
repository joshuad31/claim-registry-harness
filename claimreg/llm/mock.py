"""Deterministic offline provider used by the test suite and `cr selftest`.

It answers every role with structurally valid output derived from the
request's ``meta`` (never from model knowledge).  Its scientific content is
meaningless by design: it exists to exercise the pipeline end to end.
"""

from __future__ import annotations

import json
import re

from ..util import digest, tokens, utcnow
from .base import LLMRequest, LLMResponse
from .providers import BaseProvider


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if len(s.split()) >= 6]


def _overlap(a: str, b: str) -> float:
    ta, tb = set(tokens(a)), set(tokens(b))
    return len(ta & tb) / max(1, min(len(ta), len(tb)))


class MockProvider(BaseProvider):
    kind = "mock"

    def complete(self, req: LLMRequest, key: str) -> LLMResponse:
        fn = getattr(self, "_" + req.role, None)
        text = fn(req) if fn else json.dumps({"note": f"mock has no handler for {req.role}"})
        if not isinstance(text, str):
            text = json.dumps(text, ensure_ascii=False)
        return LLMResponse(text=text, provider=self.name, model="mock-deterministic",
                           usage={"input_tokens": len(req.user) // 4, "output_tokens": len(text) // 4},
                           cost_usd=0.0, started=utcnow(), finished=utcnow(), key=key)

    # ---------------------------------------------------------------- roles
    def _indexer(self, req):
        fn = req.meta.get("filename", "x")
        return {"filename": fn, "rank": "A" if int(digest(fn, 2), 16) % 2 else "B",
                "author_year_title": fn, "relevance": "mock relevance", "summary": "mock summary",
                "contradictions_and_gaps": "none noted"}

    def _archivist_writer(self, req):
        return ("You are a precision researcher working from a fixed notebook.\n\nWORKFLOW:\n1. Outline.\n2. Cover.\n"
                "3. Draft.\n4. Check.\n5. Cut.\n\nEVIDENCE DISCIPLINE:\n* [SOURCE] = source-reported finding\n"
                "* [INFERRED] = extrapolation\n* [NO SOURCE] = not located\n\nCORPUS-SPECIFIC GUARDRAILS:\n* Verify.\n\n"
                "CITATION RULES:\n* Cite (exact source filename, section heading).\n\nLANGUAGE CALIBRATION:\n* Match strength.\n\n"
                "OUTPUT:\n* Limit responses to 1,400 words.")

    def _investigator(self, req):
        rnd = int(req.meta.get("round", 1))
        n = int(req.meta.get("n", 5))
        srcs = list(req.meta.get("sources") or [])
        qs = []
        for i in range(n):
            if not srcs:
                break
            a = srcs[(rnd * n + i) % len(srcs)]
            b = srcs[(rnd * n + i + 1) % len(srcs)]
            names = [a] if i % 2 else [a, b]
            qs.append({"text": f"Using {' and '.join(names)}, what findings, designs, denominators and "
                               f"limitations do the authors report (question {rnd}.{i + 1})?",
                       "sources": names, "target": "mock target", "packet_priority_id": None,
                       "rationale": "mock"})
        return {"round_record": {"packet_read": rnd > 1, "priorities_taken": [], "priorities_set_aside": [],
                                 "disagreement_with_packet": ""},
                "ledger": f"Mock ledger after round {rnd}.", "questions": qs}

    def _archivist(self, req):
        blocks = re.findall(r"=== SOURCE: (\S+) [^\n]*===\n(?:Headings:[^\n]*\n\n)?(.*?)(?=\n=== SOURCE: |\Z)",
                            req.user, re.S)
        lines = []
        for fn, body in blocks[:3]:
            for s in _sentences(body)[:2]:
                lines.append(f"[SOURCE] {s} ({fn}, Results)")
        if not lines:
            return "[NO SOURCE] The supplied passages do not address this question."
        return "\n".join(lines) + "\n\nSynthesis: the cited passages report the findings above."

    def _coordinator(self, req):
        frame = req.meta.get("frame") or {"axes": []}
        g = int(req.meta.get("gauge", 64))
        rnd = int(req.meta.get("round", 1))
        alloc = {}
        for ax in frame.get("axes", []):
            ids = [h["id"] for h in ax["hypotheses"]]
            base = [g // 2, g // 4, g - g // 2 - g // 4][:len(ids)]
            if rnd == 2 and len(base) >= 2:
                base[0] += 2
                base[-1] -= 2
            if rnd >= 3 and len(base) >= 2:
                base[0] += 2
                base[-1] -= 2
            if len(ids) > len(base):
                base += [0] * (len(ids) - len(base))
            base[-1] = g - sum(base[:-1])
            alloc[ax["axis_id"]] = dict(zip(ids, base))
        data = {"allocations": alloc, "basis_confidence": {},
                "substantive_conditions": {k: rnd >= 3 for k in (
                    "decisive_tests_oriented", "every_live_hypothesis_adversely_tested",
                    "weakest_and_shared_links_tested", "project_success_conditions_addressed")},
                "direction": "CONTINUE",
                "feedback_packet": {"expected_return": "stable", "posture": "target named gaps",
                                    "priorities": [{"id": f"P-{rnd}", "finding_or_gap": "G-1",
                                                    "missing_material": "dose", "question": "mock",
                                                    "sources": [], "success_criterion": "x", "affects": "y"}],
                                    "substantial_novelty": "mock", "trivial_novelty": "mock",
                                    "open_gaps_and_corrections": [], "answers_needing_repair": [], "holds": "none"}}
        return (f"---\nartifact_type: CUMULATIVE-ACH-FUSION-FRAGMENT\nrevision: {rnd}\n---\n"
                f"Part A mock evidence through round {rnd}.\n\n```json\n{json.dumps(data)}\n```\n")

    def _frd_generator(self, req):
        resp = req.meta.get("response", "")
        out = []
        for line in resp.splitlines():
            m = re.match(r"\[SOURCE\]\s+(.*)\((\S+), Results\)", line)
            if m and len(out) < 3:
                out.append({"cluster": "mock", "label": "mock", "source_files": [m.group(2)],
                            "locator": "Results", "claim": m.group(1).strip(),
                            "verification_instruction": "check the sentence", "evidence_label": "[SOURCE]",
                            "provenance": "OWN_RESULT", "status": "ordinary", "speaker": "authors"})
        return {"qid": req.meta.get("qid"), "frds": out, "harvest_review": {}}

    def _frd_validator(self, req):
        frd = req.meta.get("frd", {})
        src = req.meta.get("source_text", "")
        sents = _sentences(src)
        best = max(sents, key=lambda s: _overlap(s, frd.get("claim", "")), default="")
        return {"frd_id": frd.get("frd_id"), "citation": {"filename": req.meta.get("source"), "locator": "Results"},
                "claim": best, "source_text": best, "verdict": "MOSTLY RIGHT",
                "verdict_explanation": "mock", "evidence_label": "[SOURCE]", "provenance": "OWN_RESULT",
                "readiness": "READY FOR WITNESS CONSTRUCTION" if best else "NOT READY FOR WITNESS CONSTRUCTION",
                "readiness_reason": "", "children": []}

    def _unit_deriver(self, req):
        h = req.meta.get("hypothesis", {})

        def q(t):
            w = (t or "").split()
            return " ".join(w[:9]) if len(w) >= 9 else (t or "")
        units = []
        if h.get("statement"):
            units.append({"code": "R1", "type": "REQUIRED_SUPPORT", "text": h["statement"],
                          "source_quote": q(h["statement"]), "evidence_terms": tokens(h["statement"])[:8],
                          "satisfied_by": "a finding stating it"})
        if h.get("assumptions"):
            units.append({"code": "R2", "type": "REQUIRED_SUPPORT", "text": h["assumptions"],
                          "source_quote": q(h["assumptions"]), "evidence_terms": tokens(h["assumptions"])[:8],
                          "satisfied_by": "a finding stating it"})
            units.append({"code": "C1", "type": "CONTEXTUAL_CONSTRAINT", "text": h["assumptions"],
                          "source_quote": q(h["assumptions"]), "evidence_terms": [], "satisfied_by": ""})
        if h.get("falsification"):
            units.append({"code": "A1", "type": "ADVERSE_TEST", "text": h["falsification"],
                          "source_quote": q(h["falsification"]), "evidence_terms": [], "satisfied_by": ""})
        if h.get("corroboration"):
            units.append({"code": "E1", "type": "CORROBORATING_EXPECTATION", "text": h["corroboration"],
                          "source_quote": q(h["corroboration"]), "evidence_terms": [], "satisfied_by": ""})
        return {"hypothesis_id": h.get("id"), "units": units, "notes": "mock"}

    def _witness_constructor(self, req):
        v = req.meta.get("vfrd", {})
        c = int(req.meta.get("ceiling", 60))
        words = v.get("claim", "").split()[: max(5, c - 5)]
        return {"status": "WITNESS", "witness": " ".join(words), "preserved": [], "omitted": [],
                "would_be_lost": "", "repair_needed": ""}

    def _witness_auditor(self, req):
        return {"unsupported_assertions": [], "material_omissions": [], "strongest_forbidden_reading": "",
                "reader_recovers": "same", "verdict": "PASS", "reason": "mock", "fix": ""}

    def _match(self, req, thr_full, thr_part):
        u = req.meta.get("unit_text", "")
        js = []
        for wid, wt in (req.meta.get("witnesses") or {}).items():
            o = _overlap(u, wt)
            rel = ("WITNESS_ENTAILS_UNIT" if o >= thr_full else
                   "PARTIALLY_COVERS" if o >= thr_part else "NO_SEMANTIC_RELATION")
            if re.search(r"\bnot\b|\bno\b", wt) and o >= thr_part and "CONTRADICT" in u.upper():
                rel = "CONTRADICTS"
            js.append({"witness_id": wid, "relation": rel, "trace": f"mock overlap {o:.2f}"})
        return {"unit_id": (req.meta.get("unit") or {}).get("unit_id"), "judgments": js}

    def _matcher_a(self, req):
        return self._match(req, 0.30, 0.12)

    def _matcher_b(self, req):
        return self._match(req, 0.28, 0.12)

    def _match_adjudicator(self, req):
        ds = []
        for wid, rec in (req.meta.get("disputes") or {}).items():
            ds.append({"witness_id": wid, "relation": rec.get("a", "ABSTAIN"), "trace": "mock: pass A",
                       "agrees_with": "A"})
        return {"decisions": ds}

    def _joint_checker(self, req):
        if "group" in req.meta:
            return {"approve": True, "member_contributions": {}, "reason": "mock"}
        p = req.meta.get("partials") or []
        return {"groups": [{"witness_ids": p[:2], "contributions": {}, "trace": "mock"}] if len(p) >= 2 else []}

    def _incompat_checker(self, req):
        return {"pairs": [{"a": a, "b": b, "incompatible": False, "basis": "NONE", "trace": "mock"}
                          for a, b in req.meta.get("pairs", [])]}

    def _transcoder(self, req):
        out = []
        for it in req.meta.get("items", []):
            out.append(f"### {it['item_id']} · {it['type']} · PASS\nOriginal: {it['raw']}\nTranscoded: {it['raw']}\n"
                       f"Bindings: none\nRules: none\nCheck: PASS")
        return "\n\n".join(out)

    def _dictionary_reviewer(self, req):
        return ("---\nartifact_type: ACH-CUSTOM-DICTIONARY\n---\n\nD-001 — trial (experimental comparison)\n"
                "Base form: trial\nDefinition: a mock entry\nScope: mock\nStatus: ACTIVE\nAliases: none\n")

    def _assessor(self, req):
        frame = req.meta.get("frame") or {"axes": []}
        g = int(req.meta.get("gauge", 64))
        alloc = {}
        for ax in frame.get("axes", []):
            ids = [h["id"] for h in ax["hypotheses"]]
            vec = [g // len(ids)] * len(ids)
            vec[-1] = g - sum(vec[:-1])
            alloc[ax["axis_id"]] = dict(zip(ids, vec))
        return "Mock assessment.\n\n```json\n" + json.dumps({"allocations": alloc, "drivers": {}}) + "\n```\n"

    def _reporter(self, req):
        return {"summary": "Mock summary of the run record."}
