"""Unit tests for deterministic components: coverage solver, stop rule, firewall,
quote verification, JSON extraction, header parsing, crux tests."""

import itertools
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.corpus import find_quote  # noqa: E402
from claimreg.coverage import Option, Problem, complete, solve  # noqa: E402
from claimreg.crux import test_t1, test_t2  # noqa: E402
from claimreg.header import parse_header  # noqa: E402
from claimreg.llm.jsonparse import extract_json  # noqa: E402
from claimreg.quest import delta_units, evaluate_stop, firewall, render_packet, stop_thresholds  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "mini"


def brute_force_sets(pb: Problem) -> set:
    """Every deletion-minimal complete witness set, by exhaustive search over subsets."""
    ws = sorted({w for opts in pb.options.values() for o in opts for w in o.witnesses})
    found = set()
    for r in range(1, len(ws) + 1):
        for comb in itertools.combinations(ws, r):
            s = set(comb)
            if complete(pb, s) and all(not complete(pb, s - {w}) for w in s):
                found.add(frozenset(s))
    return found


class CoverageTest(unittest.TestCase):
    def test_spec_worked_example(self):
        # Technical specification 4: W1 covers A, W2 covers B, W3 covers both.
        pb = Problem("H", ["A", "B"], {
            "A": [Option("o1", "A", ("W1",), "EQUIVALENT"), Option("o3a", "A", ("W3",), "EQUIVALENT")],
            "B": [Option("o2", "B", ("W2",), "EQUIVALENT"), Option("o3b", "B", ("W3",), "EQUIVALENT")]})
        res = solve(pb)
        got = {frozenset(s["witnesses"]) for s in res["sets"]}
        self.assertEqual(got, {frozenset({"W1", "W2"}), frozenset({"W3"})})
        self.assertEqual(res["search_status"], "EXHAUSTIVE")
        for s in res["sets"]:
            for c in s["certificates"]:
                self.assertTrue(c["uncovered_units"])

    def test_uncovered_unit(self):
        pb = Problem("H", ["A", "B"], {"A": [Option("o1", "A", ("W1",), "EQUIVALENT")], "B": []})
        res = solve(pb)
        self.assertEqual(res["status"], "NO_COMPLETE_COVERAGE")
        self.assertEqual(res["uncovered_units"], ["B"])

    def test_random_against_brute_force(self):
        rng = random.Random(7)
        for trial in range(150):
            n_units = rng.randint(1, 4)
            n_w = rng.randint(1, 6)
            ws = [f"W{i}" for i in range(n_w)]
            units = [f"U{j}" for j in range(n_units)]
            opts = {}
            for u in units:
                lst = []
                for k in range(rng.randint(0, 3)):
                    size = 1 if rng.random() < 0.7 else 2
                    mem = tuple(sorted(rng.sample(ws, min(size, len(ws)))))
                    lst.append(Option(f"{u}-{k}", u, mem, "EQUIVALENT" if size == 1 else "JOINTLY_SUFFICIENT",
                                      size > 1))
                opts[u] = lst
            viol = {}
            if rng.random() < 0.3:
                viol[rng.choice(ws)] = ["C1"]
            inc = set()
            if rng.random() < 0.3 and len(ws) >= 2:
                a, b = rng.sample(ws, 2)
                inc.add(frozenset((a, b)))
            pb = Problem("H", units, opts, viol, inc)
            res = solve(pb, max_states=10000, max_sets=10000)
            got = {frozenset(s["witnesses"]) for s in res["sets"]}
            self.assertEqual(got, brute_force_sets(pb), f"trial {trial}")


class StopRuleTest(unittest.TestCase):
    def test_thresholds(self):
        self.assertEqual(stop_thresholds(64), (0.334, 0.75))
        self.assertEqual(stop_thresholds(100), (1.0, 1.2))
        self.assertEqual(stop_thresholds(50), (0.0, 0.5))

    def test_delta(self):
        self.assertEqual(delta_units({"a": 30, "b": 20, "c": 14}, {"a": 31, "b": 20, "c": 13}), 1.0)

    def test_round_one_undefined_and_earliest_stop(self):
        mk = lambda vecs: [{"round": i + 1, "allocations": {"A1": v}} for i, v in enumerate(vecs)]
        v = {"H1": 30, "H2": 20, "H3": 14}
        self.assertFalse(evaluate_stop(mk([v, v, v]), 64, ["A1"], True, True)["stop"])   # 2 deltas only
        self.assertTrue(evaluate_stop(mk([v, v, v, v]), 64, ["A1"], False, True)["stop"])  # end of round 4
        w = {"H1": 31, "H2": 20, "H3": 13}
        # deltas 0,0,1 -> mean 0.333 <= 0.334 at G=64 (the spec's worked example)
        self.assertTrue(evaluate_stop(mk([v, v, v, w]), 64, ["A1"], False, True)["stop"])
        self.assertFalse(evaluate_stop(mk([v, v, v, v]), 64, ["A1"], True, False)["stop"])  # substantive gate


class FirewallTest(unittest.TestCase):
    class C:
        def resolve(self, n):
            return {"smith2020.md": "smith2020.md", "jones2021.md": "jones2021.md"}.get(n)

    def test_strips_labels_and_trims(self):
        fw = firewall({"text": "Does smith2020.md support A1-H1?", "sources": ["smith2020.md"]}, self.C())
        self.assertNotIn("A1-H1", fw["text"])
        self.assertEqual(fw["status"], "REPAIRED")
        fw = firewall({"text": "Compare a, b, c, d", "sources": ["a.md", "b.md", "c.md", "d.md"]}, self.C())
        self.assertEqual(len(fw["sources_as_sent"]), 3)
        self.assertEqual(fw["sources_resolved"]["a.md"], "UNRESOLVED_NAME")

    def test_rejects_source_agnostic(self):
        fw = firewall({"text": "What does the literature say?", "sources": []}, self.C())
        self.assertEqual(fw["status"], "REJECTED")

    def test_packet_never_carries_allocations(self):
        txt = render_packet(3, ["Q1"], "CONTINUE", {"expected_return": "stable",
                                                     "substantial_novelty": "H1 leads with 40 units allocation"})
        self.assertNotIn("40 units", txt)


class QuoteTest(unittest.TestCase):
    SRC = ("## Results\n\nMaximum urinary flow rate increased by 3.1 mL/s in the compound Z group and by "
           "0.4 mL/s in the placebo group, a significant difference.\n\n| Group | n | Qmax |\n|---|---|---|\n"
           "| Z | 30 | 3.1 |\n| Placebo | 30 | 0.4 |\n")

    def test_exact_and_typography(self):
        self.assertTrue(find_quote(self.SRC, "Maximum urinary flow rate increased by 3.1 mL/s in the compound Z "
                                             "group")["found"])
        self.assertTrue(find_quote(self.SRC, "maximum   urinary flow rate increased by 3.1 ml/s in the "
                                             "compound z group")["found"])

    def test_segments_and_tables(self):
        q = "Maximum urinary flow rate increased by 3.1 mL/s ... a significant difference"
        self.assertTrue(find_quote(self.SRC, q)["found"])
        self.assertTrue(find_quote(self.SRC, "| Group | n | Qmax |\n|------|----|-----|\n| Z | 30 | 3.1 |")["found"])

    def test_fabrication_rejected(self):
        self.assertFalse(find_quote(self.SRC, "Maximum urinary flow rate increased by 5.9 mL/s in all men "
                                              "receiving compound Z for a year")["found"])


class WitnessMechanicalTest(unittest.TestCase):
    def test_numbers(self):
        from claimreg.witness import mechanical
        v = {"claim": "Twelve to 16 weeks; nine of ten men; 2004-2009 cohort", "source_text": "",
             "source_file": "raison2013.pdf.md"}
        m = mechanical("Raison 2013: 12-16 weeks, 9 of 10 men, 2004-2009, 11 extra", v, 60)
        self.assertEqual(m["numerals_not_in_parent"], ["11"])   # only the invented number
        self.assertFalse(m["ok"])
        self.assertTrue(mechanical("Raison 2013 reported 12-16 weeks.", v, 60)["ok"])
        self.assertFalse(mechanical("one two three four five", v, 4)["within_ceiling"])


class RobustnessTest(unittest.TestCase):
    def test_relation_labels_strict(self):
        from claimreg.matching import norm_rel
        self.assertEqual(norm_rel("not equivalent"), "ABSTAIN")
        self.assertEqual(norm_rel("does not contradict"), "ABSTAIN")
        self.assertEqual(norm_rel("Witness entails unit"), "WITNESS_ENTAILS_UNIT")
        self.assertEqual(norm_rel("EQUIVALENT (strong)"), "EQUIVALENT")

    def test_bom_and_legacy_encoding(self):
        from claimreg.util import read_json, read_text
        from scratch import cleanup, scratch_dir
        d = scratch_dir("bom")
        self.addCleanup(cleanup, d)
        (d / "a.json").write_bytes(b"\xef\xbb\xbf" + b'{"x": 1}')
        self.assertEqual(read_json(d / "a.json"), {"x": 1})
        (d / "b.md").write_bytes("µ ± “q”".encode("cp1252"))
        self.assertEqual(read_text(d / "b.md"), "µ ± “q”")

    def test_unknown_relations_are_unknown(self):
        th = {"required": ["R1"], "constraints": [], "corroborating": [], "adverse": [], "options": {}}
        rel = {("w", "R1"): {"final": "ABSTAIN", "basis": "MISSING", "trace": ""}}
        self.assertEqual(test_t1("w", th, rel)[0], "UNKNOWN")
        self.assertEqual(test_t2("w", th, rel, set())[0], "UNKNOWN")


class JsonTest(unittest.TestCase):
    def test_extract(self):
        self.assertEqual(extract_json('{"a": 1}'), {"a": 1})
        self.assertEqual(extract_json('Here:\n```json\n{"a": [1, 2,]}\n```\nthanks'), {"a": [1, 2]})
        self.assertEqual(extract_json('prose {"x": {"y": 2}} more'), {"x": {"y": 2}})


class HeaderTest(unittest.TestCase):
    def test_mini_header(self):
        f = parse_header((FIX / "header.md").read_text(encoding="utf-8"))
        self.assertEqual(f["gauge"], 64)
        self.assertEqual([h["id"] for h in f["axes"][0]["hypotheses"]], ["A1-H1", "A1-H2", "A1-H3"])
        h1 = f["axes"][0]["hypotheses"][0]
        self.assertIn("standard oral doses", h1["statement"])
        self.assertIn("reach the bladder", h1["assumptions"])
        self.assertTrue(h1["falsification"] and h1["corroboration"])
        self.assertEqual(f["axes"][0]["approval"], "APPROVED")
        self.assertEqual(len(f["decisive_tests"]), 2)


class CruxTest(unittest.TestCase):
    def rel(self, d):
        return {(w, u): {"final": r, "basis": "AGREED", "trace": "t"} for (w, u), r in d.items()}

    def test_t1_t2(self):
        th = {"required": ["R1", "R2"], "constraints": ["C1"], "corroborating": ["E1"], "adverse": ["A1"],
              "options": {"R1": [{"option_id": "o1", "witnesses": ["X"]}], "R2": [{"option_id": "o2", "witnesses": ["Y"]}]}}
        # contradicts a required unit -> both fail
        rel = self.rel({("w", "R1"): "CONTRADICTS", ("w", "R2"): "NO_SEMANTIC_RELATION", ("w", "C1"): "NO_SEMANTIC_RELATION",
                        ("w", "E1"): "NO_SEMANTIC_RELATION", ("w", "A1"): "NO_SEMANTIC_RELATION"})
        self.assertEqual(test_t1("w", th, rel)[0], "FAIL")
        self.assertEqual(test_t2("w", th, rel, set())[0], "FAIL")
        # contradicts only a corroborating expectation -> T1 fail, T2 pass
        rel = self.rel({("w", "R1"): "NO_SEMANTIC_RELATION", ("w", "R2"): "NO_SEMANTIC_RELATION",
                        ("w", "C1"): "NO_SEMANTIC_RELATION", ("w", "E1"): "CONTRADICTS", ("w", "A1"): "NO_SEMANTIC_RELATION"})
        self.assertEqual(test_t1("w", th, rel)[0], "FAIL")
        self.assertEqual(test_t2("w", th, rel, set())[0], "PASS")
        # incompatible with the only option of R2 -> T1 pass, T2 fail
        rel = self.rel({("w", u): "NO_SEMANTIC_RELATION" for u in ("R1", "R2", "C1", "E1", "A1")})
        self.assertEqual(test_t1("w", th, rel)[0], "PASS")
        self.assertEqual(test_t2("w", th, rel, {frozenset(("w", "Y"))})[0], "FAIL")
        # an unjudged relation is UNKNOWN, never PASS
        rel = self.rel({("w", "R1"): "NO_SEMANTIC_RELATION"})
        self.assertEqual(test_t1("w", th, rel)[0], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
