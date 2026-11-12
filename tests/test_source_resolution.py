"""Source-name resolution, including NotebookLM's truncation of long filenames in citations."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claimreg.corpus import Corpus  # noqa: E402

LONG = "TCRM-414460-medications-and-food-interfering-with-the-bioavailability-of.pdf.md"
OTHER = "bolk2010.pdf.md"
MANIFEST = {
    "source_dir": str(Path(__file__).resolve().parent),
    "sources": [{"filename": LONG}, {"filename": OTHER}],
}


class SourceResolutionTest(unittest.TestCase):
    def setUp(self):
        self.corpus = Corpus(MANIFEST)

    def test_exact_and_case_folded_still_work(self):
        self.assertEqual(self.corpus.resolve(LONG), LONG)
        self.assertEqual(self.corpus.resolve(LONG.upper()), LONG)
        self.assertEqual(self.corpus.resolve("BOlk2010.pdf.md"), OTHER)

    def test_notebooklm_truncated_citation_resolves_to_the_unique_source(self):
        truncated = "TCRM-414460-medications-and-food-interfering-with-the-bioava.md"
        self.assertEqual(self.corpus.resolve(truncated), LONG)

    def test_truncated_citation_with_markdown_backticks_resolves(self):
        self.assertEqual(self.corpus.resolve("`TCRM-414460-medications-and-food-interfering-with-the-bioava.md`"), LONG)

    def test_short_or_ambiguous_prefixes_are_never_guessed(self):
        self.assertIsNone(self.corpus.resolve("TCRM-414460.md"))
        self.assertIsNone(self.corpus.resolve("unknown-source-file-name.pdf.md"))


if __name__ == "__main__":
    unittest.main()
