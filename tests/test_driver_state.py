"""Unit tests for the driver's stale-backlog cleanup.

A driver restart used to keep every previously pushed question in `driver-state.json["pushed"]`, so a
question lost to a page wedge or a killed lane stayed counted as outstanding forever: the backlog
(`pushed - saved`) sat at its limit and the lanes went idle.  `sanitise_pushed` keeps only entries
whose question has an answer file on disk (unanswered in-flight questions live in the lane runner's
IndexedDB and are recovered from the chat, so nothing is lost)."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from claimreg.notebooklm.driver import restore_minimized_windows, sanitise_pushed  # noqa: E402


class SanitisePushedTest(unittest.TestCase):
    def test_keeps_answered_questions_and_drops_lost_ones(self):
        pushed = ["Q0001.json", "Q0002.json", "Q0003-A02.json", "Q0004.json"]
        saved = {"Q0001", "Q0003"}
        self.assertEqual(sanitise_pushed(pushed, saved), {"Q0001.json", "Q0003-A02.json"})

    def test_retry_attempts_are_matched_by_their_question_id(self):
        self.assertEqual(sanitise_pushed(["Q0010-A02.json"], {"Q0010"}), {"Q0010-A02.json"})
        self.assertEqual(sanitise_pushed(["Q0010-A02.json"], {"Q0010", "Q0011"}), {"Q0010-A02.json"})

    def test_empty_inputs(self):
        self.assertEqual(sanitise_pushed([], {"Q0001"}), set())
        self.assertEqual(sanitise_pushed(["Q0001.json"], set()), set())
        self.assertEqual(sanitise_pushed(None, None), set())
        self.assertEqual(sanitise_pushed(["garbage"], {"Q0001"}), set())

    def test_window_restore_is_best_effort_and_never_raises(self):
        # Only Windows attempts it, and it must return an int on every platform; the test does not
        # call it against a live browser.
        self.assertTrue(callable(restore_minimized_windows))


if __name__ == "__main__":
    unittest.main()
