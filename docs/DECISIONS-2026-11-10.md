# Decisions made on 2026-11-10 (Claude Fable 5.2)

Josh asked for the harness to be finished without being consulted at each fork. This file records each fork, what was chosen and why, so any of it can be challenged or undone. `DECISIONS.md` and `DECISIONS-ADDENDUM.md` cover the earlier builds.

## 1. Why real runs ended with no coverage

The 2026-11-09 PTX run on GPT-5.2 produced 655 validated FRDs and then no complete relation, no coverage set and no crux candidate. `cr funnel` now shows this for any run. Three causes were found in the run's own records.

| Stage | What the records showed | Cause |
|---|---|---|
| Units | 16 of 27 required units described the evidence base ("the available evidence supports a coherent explanation", "affirmative evidence demonstrates a mismatch") | A required unit is covered by one witness, and no single finding can establish a verdict about all the evidence. Zero coverage was the logically correct answer to those units |
| Witnesses | 527 retained FRDs became 114 witnesses. 146 constructor abstentions, 212 failed audits | Witnesses were written and audited as answers to the whole producing question. Quest questions are deliberately broad (several sources, 900 words or more), so one FRD could never answer one, and the auditor counted every unanswered part as a material omission |
| Matching | 4,560 of 5,940 witness-unit pairs were never judged | The shortlist chose pairs by shared vocabulary, and hypothesis wording shares little vocabulary with findings |

## 2. Required units are finding-sized (`prompts/units_derive.md`, `units.py`)

**Chosen:** the unit deriver now breaks each hypothesis sentence into the empirical facts it rests on, using the header's own assumptions and decisive tests. Alternatives the hypothesis offers ("a mismatch in exposure, tissue or timing") become one unit naming the alternatives, because every required unit must be covered. Whatever stays a verdict is typed `EVALUATIVE_JUDGMENT`: visible, reported, never a coverage requirement.

**Guard:** a mechanical check flags verdict-sized required units written by a model. The model gets one revision. A unit still verdict-sized after that is demoted to an evaluative judgment (`derived_type` records what it was). The check applies only to model APIs: the local engine's clause units and file-queue answers are untouched, so the offline regressions are unchanged.

**Consequence:** a hypothesis that only says "the evidence is unresolved" may have no required unit. It is reported as *residual*: it stands to the extent its rivals' parts stay open.

**Risk:** the premises are a model's decomposition of the human text, anchored by verbatim quotation but not individually approved. They are listed in `08_COVERAGE/PREMISE-LEDGER.md`. A stricter rule (a person approves the unit list before matching) would be easy to add and was not, to keep the run unattended.

**Undo:** `"units": {"finding_sized": false}` in `project.json`, or put the old prompt in `90_METHOD/prompts/units_derive.md`.

## 3. A witness states the FRD's finding, not an answer to the whole question (`prompts/witness_construct.md`, `witness_audit.md`)

**Chosen:** the producing question is context. The witness states the one finding the FRD's claim makes. The auditor checks only the assertions the witness makes: an unsupported assertion, or a missing qualification that changes the meaning of something it does assert. A witness that says less than the FRD, and nothing the FRD does not support, passes.

**Unchanged:** the 60-word ceiling, the 80-word recorded exception, the mechanical number check, one repair round, and the rule that a witness never adds anything.

**Why this is safe for coverage:** a witness that asserts less can only cover less. The unsafe direction, asserting more than the source, is still a failed audit.

## 4. A model routes witnesses to units before matching (`prompts/match_route.md`, `matching.route_pairs`)

**Chosen:** with a model matcher, one cheap call per 12 witnesses lists which units each witness could bear on. Those pairs, plus a halved lexical shortlist, go to the two matching passes. Routing never decides a relation.

**Undo:** `"matching": {"route": "off"}`.

## 5. Partial matches say what is missing, and scope gaps can cover conditionally (`coverage.py`, `ledger.py`)

**Chosen:** for a partial match, both passes now name the gap: `SCOPE` (the unit's own effect, shown in another population, species, model, tissue or dose), `ELEMENT`, `STRENGTH` or `OTHER`, with one sentence saying what would have to be true for the unit to follow.

When a required unit has no complete match, a `SCOPE` partial may cover it *conditionally*. The transfer it relies on is written into the coverage set as a named assumption, and the hypothesis is reported as `COMPLETE_WITH_ASSUMPTIONS`, never `COMPLETE`. Strict coverage is computed first and is unchanged.

**Why:** the literature almost never studies the exact cohort a hypothesis is about. Under strict entailment alone, animal and mechanistic findings could never cover anything, which builds a bias against mechanistic evidence into the arithmetic. This tier lets that evidence carry a hypothesis while showing exactly what must be granted. The list of assumptions is also the list of things an "unresolved" rival rests on.

**Undo:** `"coverage": {"assume_gaps": []}`.

## 6. The premise ledger (`08_COVERAGE/PREMISE-LEDGER.md`)

**Chosen:** a mechanical table, per hypothesis and per part: established, contested (a finding for and a finding against), supported with an assumption, partly supported, contradicted, or not addressed. It is the first thing a reader should open. No model writes it.

## 7. Provider failover (`llm/router.py`)

**Chosen:** a role may be routed to an ordered list of providers. The next provider is asked when the current one errors or times out after retries, returns an empty answer, stops with a content-filter or refusal signal, is rejected with a content-policy HTTP error, or returns output that fails JSON parsing or validation after one repair attempt. The triggers are mechanical; the prose of an answer is never searched for refusal phrases. One pass through the list per request. Every skip is logged with its reason, and the answer records which provider gave it.

## 8. The quest relay (`notebooklm/relay.py`, `cr quest`)

Built from `PROPOSAL-RELAY-AND-FAILOVER.md` revision 2, with these choices:

- **Exactly two research roles.** `quest_investigator` and `quest_manager` are model calls. The relay is plain Python and makes no research judgment. There is no third agent.
- **Manager output is three delimited blocks** (fragment, state, a small JSON), not one large JSON, so a long Markdown state cannot break the parse.
- **The record is grow-only on disk** (`private/fragments/`, `private/record.md`), as ACH_Eval_NLM_Super requires. The Manager is given its compact state plus the new answers each round, which is what made 133 graded answers an hour possible on 11-09.
- **Questions are queued just in time**, newest packet first, so questions do not run far ahead of the Manager's feedback. The Investigator writes the opening batch and fills in whenever no packet question is ready.
- **Rounds are committed by the ledger entry.** A restart skips committed rounds, re-syncs the pacing file and never resets the go-ahead time.
- **Not built:** the optional LLM overseer. `relay-status.json` and `relay.log` are the interface an overseer would read.

## 9. The new-user commands (`onramp.py`)

`cr new`, `cr frame`, `cr approve`, `cr doctor`, `cr quest`. Choices:

- **A person must approve the header.** `cr frame` writes `header-DRAFT.md`; `cr quest` refuses to run without `cr approve --by NAME`.
- **Keys are found by file name and referenced by path.** A key is read only at call time.
- **Model names are checked, not assumed.** `cr doctor` compares the configured model with the provider's own list and `--fix` picks from that list.

## 10. What was not attempted

- Changing the fixed quest design: NotebookLM as Archivist, two agents, no FRDs during the quest, three hours.
- Changing the specification prompts in `prompts/spec/`.
- FRD condensation by QID, which stays experimental.

## 11. Fixes forced by the 2026-11-10 LEVO quest (2026-11-11)

The first real 4-lane quest captured 142 sourced, graded answers but scored 42 graded/h against the 45/h
standard (2/5 scorecard checks). The shortfall was operational, and the five causes each got a small,
testable fix. Full incident log: `Claude output\LEVO\HANDOFF-LEVO.md` Appendix A.

1. **Stale lane-runner state on a reused profile** (`driver.py`, `lane-runner.js`). The lane runner keeps
   its jobs and claims in IndexedDB `crl` + `crl_*` localStorage keyed only by qid, and a new quest restarts
   numbering at Q0001, so the previous quest's claims idled every lane of the new quest. **Chosen:** the
   driver clears that state when the quest `run_id` differs; on a restart of the same quest the state is kept
   so `CRL_recover()` can re-read in-flight answers from the chat. Alternative rejected: wiping the profile
   between quests, which would force a Google sign-in every time.
2. **Lost questions pinned the backlog** (`driver.py: sanitise_pushed`). `pushed - saved` counted a question
   lost to a page wedge or a restart as outstanding forever, holding the feed at its limit. **Chosen:** at
   startup, keep only `pushed` entries whose question has an answer file; unanswered in-flight questions
   live in the lane runner's IndexedDB and are recovered, so nothing is lost. Raising `max_backlog` is
   explicitly not the fix (it fails the steering check by construction).
3. **A wedged lane held its claim forever** (`lane-runner.js`, v7). When the chat pair could not be found
   the old code returned before its `MAX_GEN_MS` timeout could fire. **Chosen:** a lane that cannot submit or
   find its answer card releases the claim after two tries and records a `FAILED` answer; the backlog is
   released and the relay re-asks it as A02 elsewhere.
4. **Driver HOLD deadlock** (`relay.py`). With the driver reporting HOLD, no lane busy and answers waiting,
   the relay waited for `max_wait_seconds` before taking a short round. **Chosen:** that state triggers a
   short grading round immediately.
5. **Minimized browser window and link typos** (`driver.py`, `cr doctor`, `cr quest`). Chrome throttles
   hidden tabs; a minimized window stalls the lanes, and the persistent context re-opens minimized. A
   one-character notebook-link typo silently killed one lane for a whole quest. **Chosen:** launch Chrome
   maximized and restore a minimized notebook window on each driver poll; **headless is explicitly not
   supported** (a headless renderer froze after ~20 minutes). `cr doctor --notebooks` resolves every link
   with the driver profile, and `cr quest` preflights the lanes and refuses to start the relay if they do
   not all come up. `cr quest` also starts the driver with `PYTHONUNBUFFERED=1` so `driver.log` is live.

Tests: `tests/test_driver_state.py` (backlog sanitising), `tests/test_relay.py`
(`test_short_round_breaks_a_driver_hold`), and the browser mock test now runs a second quest on the same
profile to prove stale claims are cleared and listens for the lane-level failure behaviour.

6. **Assessment on frames with more than two axes** (2026-11-11, found by the LEVO evidence run). The
   assessment prompt is written for one enabled axis per pass ("use one axis unless a second distinct
   question warrants another"), but v2-generated headers can carry four axes; a single combined call
   wrote allocations only for A1 and A2, leaving A3 and A4 at 0. **Chosen:** one assessment call per axis
   (its own question, hypotheses and coverage summary), issued in parallel with `call_many` and merged.
   A single call cannot be trusted to cover an arbitrary number of axes.
7. **`cr verify` and COMPLETE_WITH_ASSUMPTIONS sets** (2026-11-11). Verify recomputed each coverage set
   with strict relations only, so every designed assumption-bearing set was reported as "not complete"
   and the run failed verification. **Chosen:** when the recorded status is COMPLETE_WITH_ASSUMPTIONS,
   re-check the set against the configured `coverage.assume_gaps`; list such sets under
   `coverage_sets.assumption_sets` rather than as problems. Strict sets are still checked strictly.
