"""Focused tests for markup normalisation in the mechanical verbatim-quote check.

The corpus markdown keeps PDF-conversion markup (LaTeX math, inline HTML), while
validators quote the rendered text.  These tests pin the representation-only folds
in ``claimreg.util.norm_for_match`` and prove that they make the mechanical
``find_quote`` check succeed on real markup cases *without* weakening the match
threshold or the fabrication rejection.

Order: `python -m unittest tests.test_quote_normalisation`
"""

import inspect
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from claimreg.config import DEFAULT_CONFIG  # noqa: E402
from claimreg.corpus import find_quote  # noqa: E402
from claimreg.util import norm_for_match, tokens  # noqa: E402


class MathMarkupTest(unittest.TestCase):
    def test_latex_pm_matches_unicode_pm(self):
        # "$5.4\pm4.3$" in the source is quoted as "5.4 ± 4.3".
        self.assertEqual(norm_for_match(r"$5.4\pm4.3$"), norm_for_match("5.4 ± 4.3"))
        self.assertTrue(find_quote(r"TSH was $5.4\pm4.3$ mIU/L.", "TSH was 5.4 ± 4.3 mIU/L.")["found"])

    def test_latex_p_value_matches_spaced_text(self):
        # "$P=.026$" in the source is quoted as "P = .026".
        self.assertEqual(norm_for_match(r"$P=.026$"), norm_for_match("P = .026"))
        self.assertTrue(find_quote(r"( $P=.026$ )", "( P = .026 )")["found"])

    def test_other_latex_operators_fold(self):
        cases = [
            (r"$3 \times 4$", "3 x 4"),
            (r"$a \le b \ge c$", "a <= b >= c"),
            (r"$p \approx .05$", "p ~ .05"),
            (r"$\mu$ g", "μg"),
            (r"$37^{\circ}$C", "37°C"),
            (r"10.0 $\mu\text{g/dL}$", "10.0 μg/dL"),
        ]
        for src, quote in cases:
            with self.subTest(src=src, quote=quote):
                self.assertEqual(norm_for_match(src), norm_for_match(quote))

    def test_math_markup_never_becomes_literal_tokens(self):
        # \pm must not index as the token "pm" (it is markup, not content).
        self.assertNotIn("pm", tokens(r"$5.4\pm4.3$"))
        self.assertIn("5.4", norm_for_match(r"$5.4\pm4.3$"))


class HtmlMarkupTest(unittest.TestCase):
    def test_subscript_matches_plain(self):
        # "T<sub>4</sub>" in the source is quoted as "T4".
        self.assertEqual(norm_for_match("T<sub>4</sub>"), norm_for_match("T4"))
        self.assertEqual(norm_for_match("LT<sub>4</sub> dose"), norm_for_match("LT4 dose"))
        self.assertTrue(find_quote("Serum T<sub>4</sub> rose.", "Serum T4 rose.")["found"])

    def test_superscript_and_emphasis_tags(self):
        self.assertEqual(norm_for_match("I<sup>2</sup> = 66%"), norm_for_match("I2 = 66%"))
        self.assertEqual(norm_for_match("the <i>p</i> value"), norm_for_match("the p value"))
        self.assertEqual(norm_for_match("line one<br>line two"), norm_for_match("line one line two"))

    def test_autolink_url_is_not_eaten_as_a_tag(self):
        # The precise tag pattern must not treat <https://...> as an HTML tag.
        self.assertIn("doi.org", norm_for_match("<https://doi.org/10.1000/test>"))


class TableAndLocatorTest(unittest.TestCase):
    SRC = (
        "## Results\n\n"
        "TSH was $1.06 \\pm 1.23$ mIU/liter with fasting and $2.93 \\pm 1.20$ with breakfast.\n\n"
        "**TABLE 4.** Least squares means\n\n"
        "| Analyte | BB | WB | HS |\n"
        "|---|---|---|---|\n"
        "| TSH, mIU/liter | 1.06 | 2.93 | 2.19 |\n"
    )

    def test_markdown_table_quote_matches_respaced_source_table(self):
        q = ("| Analyte | BB | WB | HS |\n|---|---|---|---|\n"
             "| TSH, mIU/liter | 1.06 | 2.93 | 2.19 |")
        self.assertTrue(find_quote(self.SRC, q)["found"])

    def test_quote_wrapping_and_locator_label_are_folded(self):
        # Validators wrap quotations in quote marks and prefix the section label.
        q = '**Results:** "TSH was 1.06 ± 1.23 mIU/liter with fasting and 2.93 ± 1.20 with breakfast."'
        self.assertTrue(find_quote(self.SRC, q)["found"])
        self.assertEqual(norm_for_match('Results – Evening administration: "Eight RCTs"'),
                         norm_for_match("Eight RCTs"))

    def test_bold_markers_do_not_split_unit_from_number(self):
        # Source bolds the numbers; the bold markers must not re-split "µIU/mL".
        src = "The baseline mean TSH value was **2.34 ± 1.3** µIU/mL, and after treatment it was 3.0 ± 2.2 µIU/mL."
        q = "The baseline mean TSH value was 2.34 ± 1.3 μIU/mL, and after treatment it was 3.0 ± 2.2 μIU/mL."
        self.assertTrue(find_quote(src, q)["found"])

    def test_section_numbered_heading_label_is_folded(self):
        src = ("The result of NMA was described as a League table to rank regimens according to "
               "SUCRA (left to right), with MD and 95% Crl (Table 2).")
        q = ('**Section 3.5. Results of syntheses:** "The result of NMA was described as a League '
             'table to rank regimens according to SUCRA (left to right), with MD and 95% Crl (Table 2)."')
        self.assertTrue(find_quote(src, q)["found"])


class EndToEndTest(unittest.TestCase):
    def test_ordinary_prose_still_matches(self):
        src = "Patients were asked to take their levothyroxine at bedtime, at least two hours after the last meal."
        q = "patients were asked to take their levothyroxine at bedtime, at least two hours after the last meal"
        self.assertTrue(find_quote(src, q)["found"])

    def test_genuinely_different_numbers_still_fail(self):
        src = "TSH was $1.06 \\pm 1.23$ mIU/liter with fasting and $2.93 \\pm 1.20$ with breakfast."
        # Two different result values: the character-level fuzzy fallback (0.92) rejects it.
        self.assertFalse(find_quote(src, "TSH was 1.06 ± 1.23 mIU/liter with fasting and 7.41 ± 8.88 with breakfast")["found"])
        # A short quote with a different number is not found verbatim either.
        self.assertFalse(find_quote(src, "TSH was 9.99 mIU/liter with fasting")["found"])

    def test_fabricated_sentence_still_fails(self):
        src = ("TSH was $1.06 \\pm 1.23$ mIU/liter with fasting and $2.93 \\pm 1.20$ with breakfast; "
               "bedtime dosing was superior to both.")
        self.assertFalse(find_quote(src, "TSH was 1.06 mIU/liter with fasting and bedtime dosing "
                                         "reduced cardiovascular events by half in all patients")["found"])


class ThresholdUnchangedTest(unittest.TestCase):
    def test_configured_threshold_is_still_092(self):
        self.assertEqual(float(DEFAULT_CONFIG["frd"]["quote_min_ratio"]), 0.92)

    def test_find_quote_default_threshold_is_still_092(self):
        default = inspect.signature(find_quote).parameters["min_ratio"].default
        self.assertEqual(float(default), 0.92)


if __name__ == "__main__":
    unittest.main()
