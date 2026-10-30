# What I decided, and why

*Claude (Opus 5.5), 2026-10-29. Written for Josh.*

You gave me authority to change the specification wherever that was needed to get a working harness,
and to use my own judgment instead of asking. These are the choices I made with that authority. Each
one is either a **configuration value**, so you can change it in a fork and measure the difference, or
a **stated definition** in a module docstring, so it can be argued with. None of them is hidden in the
code.

The earlier attempts stopped at decisions that needed an owner. The rule I worked by: when the
specification leaves something open, pick the cheapest rule I can defend, record it here, report its
effects in the run, and keep going.

---

## 1. The five questions ChatGPT left open (`BLOCKERS - what needs you.md`)

### Q1. The 60-word witness ceiling

**Decision:** I kept 60 words as the reference ceiling. When the witness constructor reports
`ABSTAIN` at 60 words (the mandatory content does not fit), the harness retries that witness once at
80 words. The retry is recorded on the witness as `ceiling_exception: true`. This is the blocker's
third option ("per-pair exception"), with the cap set at 80.

**Why:** ABSTAIN at 60 is caused by the design, not by the evidence. Throwing away a witness because
its qualifications don't fit in 60 words removes exactly the material the protocol most wants to
keep. A recorded exception keeps the 60-word discipline for every witness that can meet it, and the
report counts how many could not.

**To measure the alternative:** `cr fork <project> --from <run> --name W80 --set witness.raw_ceiling=80 --set witness.exception_ceiling=100`
reruns only the witness stage and the stages after it. `cr diff` then compares the two runs.

Settings: `witness.raw_ceiling` (60), `witness.exception_ceiling` (80), `witness.allow_ceiling_exception` (true).

### Q2. The matching layer (lexical pre-filter at 37.5% precision)

**Decision:** Matching is model-judged.

- Two structurally different passes judge every shortlisted witness–unit pair, each in its own
  context:
  - **pass A** is unit-centric: one unit, a list of witnesses;
  - **pass B** goes element by element, with the witness order reversed.
- When both passes agree, the relation is approved (basis `AGREED`).
- When they disagree, a third, separate context decides or abstains (basis `MODEL_ADJUDICATED`). The
  report never presents an adjudicated relation as an agreement. With `matching.dispute_policy = "abstain"`,
  disagreements become `ABSTAIN` instead.
- Before matching, the matcher answers 22 adversarial fixtures (negation, actor reversal,
  possibility vs necessity, quantity conflicts and so on) with the production prompts, in both
  passes. Results are reported pattern by pattern as **qualification**: passing a pattern qualifies
  the matcher for that pattern only.
- A lexical shortlist chooses which pairs get judged:
  - 30 witnesses per required-support or constraint unit;
  - 15 witnesses for the other unit types;
  - every pair when there are 45 witnesses or fewer.

  The shortlist is only a cost control. Every witness the crux stage relies on is later judged
  against **every** rival unit, with no shortlist ("completion matching").
- **When one pass's batch is never answered** (in the PTX run, five pass-A batches and one pass-B batch were
  stopped by a safety classifier in the operator's context and were not re-attempted):
  - the default `matching.one_pass_policy = "abstain"` treats the affected pairs as ABSTAIN;
  - `"accept"` uses the single judgment and labels it `ONE_PASS_ONLY` everywhere it appears.

  The PTX run uses `"accept"`, recorded as an amendment in its RUN-CONFIG.json. Otherwise about half of the
  judged pairs would have been discarded for an operator-side reason that says nothing about the evidence.
  One-pass relations are listed in the review packet for confirmation.
- **You can overrule any relation.** Put entries in
  `07_MATCHING/04_disagreements-and-review/human-decisions.json` and run `cr run <project> --from coverage`.
  A human decision is used everywhere after that (basis `HUMAN`), and the model's relation is kept
  next to it.
- The harness writes `review-packet.md` in the same folder. It lists every complete relation, every
  contradiction and every disagreement, with the unit, the witness, both passes' traces and the
  source file.

**Why:** A pre-filter cannot judge meaning, so the third option ("ship the pre-filter and stop calling
coverage a finding") would have given you a harness that never produces coverage. The second option
was the cost: about a day of work and API keys. I built that, made the model calls answerable
through a file queue (see the user guide) so no key is required, and added the human override path,
so the first option (you adjudicate) still works.

### Q3. The missing dictionary release

**Decision:** The language layer is **off** by default (`language.mode = "off"`). The transcoder is
the identity: matching uses the raw witness and unit text, and every item is recorded with status
`IDENTITY`. With `language.mode = "labels"`, your own tools run unattended:

- Superior Mr. Dictionary v5.1;
- Mr. Canonicalizer v1.1;
- Mr. Transcoder v1.0.

An existing dictionary can be imported instead, from a flat JSON file or Mr. Dictionary Markdown
(`language.dictionary_file`). A mechanical check compares each transcoded text with its raw text
(numbers, negation, modality, length). Anything that fails is held back from matching as `REVIEW`.

**Why:** The dictionary's job is to make matching consistent across wording. A model matcher already
reads synonyms. Requiring dictionary "closure" before any downstream stage could run is what stalled
the ChatGPT harness. Making the layer optional, declared and measurable keeps it in the design
without letting it block the run. I did not reconstruct the missing release. (The later hardening
report says the dictionary was in the run's SQLite store all along. The PTX demonstration does not
depend on it.)

### Q4. Incompatibility approval is undefined in the specification

**Decision:** I adopted the rule ChatGPT proposed. Two witnesses are incompatible when they report
the same quantity with conflicting values (`SAME_QUANTITY_CONFLICT`), or opposite polarity on the
same predicate at the same scope (`OPPOSITE_POLARITY`).

In place of human confirmation, approval requires **two independent model passes that both find
it**. You can approve or reject any pair in
`07_MATCHING/04_disagreements-and-review/human-incompatibilities.json`. Only pairs that could change
a result are checked: witnesses that appear in coverage options and that share vocabulary or a
source. The check is capped at `coverage.max_incompat_pairs` (200).

**Why:** Leaving the rule undefined makes the incompatibility path untestable forever. Requiring two
passes to agree keeps false approvals rare, and the human file keeps you in charge.

### Q5. Two Rank A sources were never queried

**Decision:** The PTX demonstration imports the ChatGPT/NotebookLM discovery record as it stands (see
§3), so it inherits whatever that record contains. In runs the harness carries out itself, the quest
keeps a source-coverage ledger. A source named twice and never cited is flagged
`SOURCE_UNRESPONSIVE`. Branch 2 of the stop rule cannot fire until every Rank A and Rank B source
has been queried. (The later hardening report says both sources were in fact queried, cited and
held for internal table inconsistencies. I have not re-checked that claim.)

---

## 2. Other places where the specification was open, and what the harness does

### Coverage units (the matching representation of each hypothesis)

One model call per hypothesis turns the human-written hypothesis into typed units:

| Type | What it is |
|---|---|
| `REQUIRED_SUPPORT` | Must be established for complete coverage. |
| `CONTEXTUAL_CONSTRAINT` | A condition the hypothesis depends on. A contradicting witness vetoes a set. |
| `ADVERSE_TEST` | From the falsification section. Evidence meeting it counts against the hypothesis. |
| `CORROBORATING_EXPECTATION` | From the corroboration section. |
| `EVALUATIVE_JUDGMENT` | **Added by me.** Claims like "meaningfully improve" or "consequential" that no single source passage can establish. They are reported to you and never matched, because demanding a witness for a value judgment guarantees an uncovered unit. |

Every unit must carry a verbatim quotation of at least six words from the hypothesis, its header
section, or a header definition. The quotation is checked mechanically. A unit that cannot be
anchored is kept for audit but set inactive, because it may introduce a commitment you never
approved.

### Crux definitions (spec 29.1–30)

The full statement is in the docstring at the top of `claimreg/crux.py`.

- **Rivals** are the other hypotheses on the same axis.
- **Frozen rival theory.** Each rival's theory is compiled once and hashed before any test runs. It
  holds the rival's units, its approved options, its approved incompatibilities and its joint
  groups.
- **T1 (consistency) fails** when the witness contradicts any unit the rival asserts (required,
  constraint or corroborating), or when it meets one of the rival's adverse tests.
- **T2 (coverage) fails** when, once the witness is established, the rival loses coverage it needs.
  That happens in either of two ways:
  - the witness contradicts one of the rival's required units;
  - every option for one of the rival's required units contains a witness that is
    approved-incompatible with this one.

  T2 is counterfactual. If the rival was already incomplete regardless of the witness, the
  certificate says so and the incompleteness is not blamed on the witness.
- **`UNKNOWN`** means a needed relation was never judged. It is never converted into PASS or FAIL.
- **A crux candidate** must meet all three conditions:
  - it is in a deletion-minimal set of its home hypothesis;
  - it is in none of the rival's sets (the membership screen);
  - it fails both T1 and T2 against that rival.
- **Diagnostic witnesses** (spec Optional Route B, reported separately). When the home hypothesis has
  no complete coverage, witnesses that fully establish at least one of its required parts get the
  same tests. Those that fail both are listed as diagnostic witnesses, never as crux candidates.
  This is the harness's answer to "no hypothesis reaches complete coverage, so there is nothing to
  report".

### Coverage solver (spec 29, technical specification 4)

The solver enumerates the minimal transversals of the option hypergraph, then runs the literal
deletion pass on every candidate, with a removal certificate for each witness. It is checked against
brute force on 150 random problems (`tests/test_core.py`). Search bounds are reported as
`RESOURCE_BOUNDED`, never presented as exhaustive.

### Stop rule (header template v2)

- The thresholds come from the gauge-keyed table. At G = 64:
  - branch 1: the mean change over the last 3 rounds is ≤ 0.334 units;
  - branch 2: every A and B source has been queried and the mean over 4 rounds is ≤ 0.75.
- The change between two rounds is x = half the sum of absolute per-hypothesis unit changes.
- Round 1 has no prior round, so its change is undefined, not zero.
- The rule fires only when the Coordinator's four substantive conditions are also true.
- `quest.max_rounds` is an operational ceiling. Hitting it is recorded as `OPERATIONAL_LIMIT`, never
  as a scientific stop.

### Discovery firewall

The firewall is deterministic. It strips hypothesis labels and protocol jargon from questions,
enforces one to three named sources, rejects questions that name no source, and records every
repair. The Archivist never sees the header, and feedback packets never carry allocations.

### FRDs and the quote gate

- At most four FRDs per response (the Problems note).
- The blind validator sees one FRD and its named source only. It must copy its supporting text
  verbatim, and the harness then looks that text up in the source file: exact match first, then
  segments split at ellipses, then a fuzzy match at ≥ 0.92.
- An FRD whose quotation cannot be found does not become READY (`frd.quote_gate = "block"`). This is
  what makes every downstream witness traceable to a real passage.

### Retention (the Problems note)

READY FRDs are ranked. The lowest-ranked are archived, never deleted, but only when the validated
database exceeds its corpus-size budget. The budget is 25% of the corpus at ≤ 1 MB, falling linearly
to 8% at ≥ 12 MB. At most 20% are archived (`retention.keep_fraction = 0.8`). Near-duplicates
(token Jaccard ≥ 0.72) are archived first.

### Witnesses

- Each witness reuses its FRD's origin question (required origin reuse).
- The constructor and the auditor always run in different contexts.
- Mechanical checks run on every witness:
  - word count;
  - numerals that are not in the parent FRD or the source heading. Signs and ranges are ignored, so
    "12-16" is not read as "-16". Digit runs inside file names (author-year citations) and number words
    ("nine") count as present;
  - negation dropped from a negative FRD.
- One revision round is allowed.
- A witness is released only when its final audit is PASS **and** its mechanical checks pass.
  Everything else is held with its reason, and nothing is deleted.

### Independence between roles

Every role is a separate model call with its own prompt. When the model is answered through the file
queue, batches are grouped by role. In the PTX demonstration, each batch was answered by a fresh
agent context that saw only that batch file. So the constructor never saw the audit, and pass A
never saw pass B.

### Reports

- `CRUX-REPORT.md` stays under 4,000 words.
- `EVIDENCE-PACKETS.md` is new. It is the compact packet the October 22 handoff proposed. For each
  hypothesis it lists:
  - the controlling claims;
  - the strongest objections;
  - the material qualifications;
  - the gaps.

  Each entry is tied to witnesses and source files. It is useful even when no hypothesis reaches
  complete coverage.
- `report.html` is the audit browser. It follows a witness to its FRD, the verbatim source quote,
  the producing question and the Archivist's answer.

### Publication and forks (spec 34)

- `cr publish` writes a release with a hash for every artifact and every model answer used.
- `cr fork` copies a run with declared configuration changes. It resets only the stages those
  changes affect, and records the fork in `FORK-RECORD.json`.

---

## 3. How the PTX demonstration run was produced

- **Upstream.** Corpus, header v4.1, ranked index, Archivist prompt, the 62 questions with their
  NotebookLM answers, the 77 candidate FRDs and the 73 retained READY validations are imported from
  `ChatGPT output\PTX-Full-Run-2026-10-24`. They are labelled `imported` in the run state, with the
  source file's hash. Re-running discovery would have meant re-asking NotebookLM. Every imported
  validation still went through this harness's own quotation check: all 77 verified (75 exact,
  2 by segments), including the 73 retained ones.
- **Downstream.** Everything downstream ran in this harness:
  - units;
  - witnesses and audits;
  - matching qualification;
  - two-pass matching and adjudication;
  - joint groups and incompatibilities;
  - coverage;
  - crux;
  - the final ACH_Eval assessment;
  - the reports.

  Every model request went through the file queue and was answered by Claude Opus 5.5 working in
  fresh agent contexts, one context per batch. The batch prompt is quoted in
  `docs/AGENT-OPERATOR.md`. No API key was used. Each answer is stored with that operator identity,
  and the call log records it.
- **Requests that could not be answered.** Some operator contexts were stopped by a safety classifier
  before they wrote any answer:
  - 1 of 4 witness-audit batches;
  - 6 of 16 matching batches;
  - 1 of 2 adjudication batches;
  - the joint-group verification;
  - the single Investigator request of an attempted live quest round (a separate smoke-test project,
    later removed).

  I did not re-attempt any of them. The harness gained `cr queue skip` for this case: a skipped request
  is recorded as a failed call, and each stage handles it explicitly:
  - an unaudited witness is held;
  - a pair with one pass is `ONE_PASS_ONLY`;
  - a pair with no pass is `MISSING`;
  - an unadjudicated dispute stays `DISPUTED`;
  - an unverified joint group is not approved.

  Of the 511 requests queued in the PTX run, 115 were skipped. They are listed in
  `projects/PTX/queue/OPERATOR-NOTES.md`.
- **Declared settings added during the run.** Each is recorded as an amendment in the run's
  RUN-CONFIG.json:
  - `matching.synonyms = [["PTX", "pentoxifylline", ...]]`. This affects the shortlist only; the
    matcher never sees it.
  - `matching.one_pass_policy = "accept"`.
- **Harness fixes made during the run.** The numeral check read ranges such as "12-16" as negative
  numbers, and author years as invented numbers. Fixing it reduced 17 revision requests to 3. The report
  summary's input contained a timestamp, so every rerun asked a new question; it no longer does.
- **Not done in this session.** I did not run a live discovery quest (Investigator → Archivist →
  Coordinator rounds). That code path is exercised end to end by the mock-provider test only. With
  an API key, or with the queue, `cr run` on a new project runs it.

## 4. Independent review

A separate agent, with no part in building the harness, tested it. It ran the test suite and the whole
command line (init, corpus, run, status, verify, fork, diff, publish, and the queue path) on the test
fixture, and read the core modules. It reported 24 defects. All were fixed before delivery, and the
PTX run was then redone from the cache, with no new model calls and the same results. The main fixes:

- **Coverage could go stale.** Crux completion matching added relations after coverage had run, which
  could leave a coverage set no longer deletion-minimal. Coverage is now recomputed until it is stable.
- **Relation labels were matched as substrings.** "not equivalent" was read as EQUIVALENT. Only exact
  labels count now.
- **Unknown relations passed the tests.** An unknown or undecided relation now yields `UNKNOWN` in T1
  and T2, never PASS.
- **Human decisions were not checked.** A decision naming a witness or unit that does not exist is now
  ignored and reported.
- **Forks lost settings.** A fork of a fork now keeps its parent's settings. A forked or forced quest
  starts again; its old state is kept under `99_superseded`. `--from` redoes the named stage.
- **Failed model calls looked like success.** A stage with failed calls is now marked `partial`, and
  the next run asks the calls again.
- **Single-call stages could not survive a skip.** A skipped assessment or summary request no longer
  breaks the run.
- **Windows problems.**
  - JSON files saved with a byte-order mark are now read correctly.
  - Non-UTF-8 sources are flagged.
  - The console is forced to UTF-8.
  - Accented file names in citations are recognized.
- **Releases.** Release folders carry a timestamp, so they are never mixed. The rebuild instructions
  are corrected.
- **Smaller fixes.**
  - Dropped network connections are retried.
  - A malformed response file no longer stops an import.
  - Queue batches can be re-packed.
  - Retention archives only when the database is over budget.
  - Report truncation respects the 4,000-word limit.
  - An empty corpus folder is an error.
  - Dead settings were removed.

## 5. What this harness does not establish

- That every relevant item in the corpus was extracted. Discovery is question-guided, not
  exhaustive.
- That model matching is right beyond the tested fixture patterns. Every relation can be read in the
  review packet and overruled.
- That a witness's source is true, independent or authoritative. A crux candidate is a witness the
  rival cannot absorb under these definitions. It is not proof.
- That ACH_Eval allocations are probabilities. They are uncalibrated working judgments.
- That runs are reproducible across different models. Within one model they are reproducible from
  the cache: every answer is stored, keyed by the exact prompt.
