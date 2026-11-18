"""Tests for the depth-first arrangement search in crux and the crash-proof run logger.

The search replaces an exhaustive transversal enumeration (every arrangement built before the first
was returned), which took about 88 seconds on a six-unit theory.  These tests pin the three answers
T2 depends on: an arrangement is found, none exists (a definite FAIL), or the node budget ran out
(UNKNOWN).  The logger test pins that a closed console cannot kill a stage.
"""
from __future__ import annotations

import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from claimreg.crux import _arrangement  # noqa: E402
from claimreg.runctx import RunContext  # noqa: E402


def theory(units: int, options_per_unit: int, *, violator: str = "", incompat=()) -> tuple[dict, dict]:
    th = {"hypothesis_id": "A1-H1", "constraint_violators": {}, "incompatibilities": list(incompat)}
    if violator:
        th["constraint_violators"] = {violator: ["C1"]}
    opts = {}
    for i in range(units):
        opts[f"U{i}"] = [
            {"option_id": f"O{i}-{j}", "witnesses": [f"w{i}-{j}"], "relation": "EQUIVALENT", "joint": False}
            for j in range(options_per_unit)
        ]
    return th, opts


class ArrangementSearchTests(unittest.TestCase):
    def test_finds_an_arrangement_quickly(self):
        th, opts = theory(6, 12)
        start = time.perf_counter()
        res = _arrangement(th, list(opts), opts, set(), {"max_states": 3000})
        elapsed = time.perf_counter() - start
        self.assertTrue(res["found"])
        self.assertEqual(set(res["example"]), set(opts))
        self.assertLess(elapsed, 1.0, f"search took {elapsed:.3f}s")

    def test_constraint_violator_is_a_definite_no(self):
        th, opts = theory(2, 1, violator="w0-0")
        res = _arrangement(th, list(opts), opts, set(), {"max_states": 3000})
        self.assertFalse(res["found"])
        self.assertFalse(res["bounded"])

    def test_incompatible_pair_is_a_definite_no(self):
        th, opts = theory(2, 1, incompat=[["w0-0", "w1-0"]])
        res = _arrangement(th, list(opts), opts, set(), {"max_states": 3000})
        self.assertFalse(res["found"])
        self.assertFalse(res["bounded"])

    def test_node_budget_returns_bounded_not_fail(self):
        th, opts = theory(2, 2)
        res = _arrangement(th, list(opts), opts, set(), {"max_states": 1})
        self.assertFalse(res["found"])
        self.assertTrue(res["bounded"])

    def test_no_units_is_not_an_arrangement(self):
        res = _arrangement({"hypothesis_id": "H"}, [], {}, set(), {"max_states": 3000})
        self.assertFalse(res["found"])
        self.assertFalse(res["bounded"])


class LoggerTests(unittest.TestCase):
    def test_closed_console_does_not_raise_and_the_file_keeps_the_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx = object.__new__(RunContext)
            ctx.run_dir = Path(tmp)
            ctx.quiet = False
            (Path(tmp) / "00_RUN-CONTROL").mkdir(parents=True, exist_ok=True)
            with mock.patch("builtins.print", side_effect=OSError("console gone")):
                ctx.log("progress line")          # must not raise
            log = (Path(tmp) / "00_RUN-CONTROL" / "run-log.txt").read_text(encoding="utf-8")
            self.assertIn("progress line", log)


if __name__ == "__main__":
    unittest.main()
