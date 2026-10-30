# WORKED EXAMPLE — engineered so coverage and crux identification actually run

This is a synthetic, deliberately worded case. Unlike the demo corpus, the source
sentences restate the hypothesis clauses almost verbatim, so the local lexical
matcher can reach complete relations. That makes the last three modules — coverage
sets, incompatibility, and crux identification with T1/T2 certificates — produce
real artifacts you can inspect.

It is a **test fixture, not research**. Every study, number and quotation is
invented. The point is to show what a finished coverage set and a crux candidate
look like, and to fail loudly if those modules ever stop working.

Expected result (asserted by `tests/test_worked_example.py`):

- H1 and H2 each get at least one deletion-minimal coverage set.
- At least one crux candidate is identified, with a T1 and a T2 certificate.
- At least one witness pair is approved as incompatible (opposite polarity).
- H3 gets no complete coverage, so it appears in the report as unresolved.
