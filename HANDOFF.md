# Handoff: Claim Registry harness (for the next model)

> **Asked to "launch", "start" or "use" Claim Registry?** Run `python cr.py start` and follow it. There is no program to launch. This file is for *changing* the harness: read it only if someone wants its code, tests, prompts or documents changed.

Written 2026-11-09 by Claude (Opus 5.5) for Josh Davis, who is handing this project to another model. If you are changing the harness, read this file first, then `START HERE.md`, `docs/WALKTHROUGH.md` and `docs/NOTEBOOKLM-QUEST.md`.

## 1. What this is and what Josh wants

This repository implements Josh's **Claim Registry (ACH 2.0)** specification. It is a harness that:

- distils a document corpus into source-anchored evidence;
- tests competing hypotheses against that evidence, through discovery quest → FRDs → witnesses → matching → coverage sets → crux → report.

**Josh's goal:** a harness people can download and use immediately. It should teach the method, including where to acquire sources, and automate every step up to minimal coverage groups. Coverage-group formation, crux identification and FRD condensation are still experimental.

**His fixed design for discovery (do not change it):**

- **NotebookLM is the Archivist.** It holds the corpus and answers one question at a time. It is used because it is auditable, and because notebooks can be shared and copied with their sources intact.
- **A quest takes ≤ 3 hours.** No FRDs are made during it.
- **There are exactly two agents and no third.**
  - The **Investigator** is the only role that touches NotebookLM. It writes questions and collects answers.
  - The **Manager** runs ACH_Eval, organizes the answers, writes feedback packets with ready-to-send questions, and steers throughput. It never touches NotebookLM.
- **No API keys are needed.** datalab.to (PDF to Markdown) is optional.
- **Throughput is essential:** at least 45 usable, *graded* questions an hour, with 60 as the aspiration (§5).

## 2. Josh's standing rules

**NotebookLM:**

- Configure Chat must be **Custom + Longer** on every notebook copy.
- Never use the "Discover sources" / Fast Research box or Import its results.
- Never save answers to notes.
- Delete a copy's chat history only when its answers degrade (your judgment).
- **Questions never ask for fewer than 900 words.** Only a single-source question may state a length, and then only "about 900 words or more". This overrides header v4.1, which allows "900 words or less".
- Josh signs in to Google himself. Never enter credentials.

**Working with Josh:**

- Share a plan of steps before any substantial piece of work.
- Recognize "good enough": don't keep optimizing once he says the work is done.
- He wants adversarial rigor on the *evidence*, never attacks on the legitimacy of patient-led "citizen meta-analysis".
- Treat mechanistic evidence as a legitimate basis for telling hypotheses apart, not merely as context.
- Don't ask him where to save outputs; choose sensibly.
- Minimize his manual steps, such as repeated permission clicks.
- **GitHub:** he uses **GitHub Desktop**, not the git command line. To publish, write the changed files into his local clone. He then enters a Summary, clicks **Commit to main**, then **Push origin**. Push only with his OK.

## 3. Where things are

| Thing | Location |
|---|---|
| This repo (canonical) | https://github.com/joshuad31/claim-registry-harness; Josh's local clone: `C:\Users\joshu\Desktop\FINAL SPECIFICATION DOCUMENTS\claim-registry-harness` |
| Driver working folder (where `nlm run` was used) | `C:\Users\joshu\Desktop\FINAL SPECIFICATION DOCUMENTS\Claude output\`. Its `claimreg\` core is an **older 10-29 build**: never copy it over the repo. Its NotebookLM files match the repo except the 11-09 bug fixes. |
| PTX corpus (111 Markdown sources) | `Claude output\projects\PTX\01_CORPUS\source-files\` (not in git: third-party papers) |
| PTX header v4.1, ranked index, Archivist prompt | `Claude output\projects\PTX\01_FRAME\` (also committed under `projects/PTX/01_FRAME/`) |
| 10-30 NotebookLM quest record | `Claude output\PTX-QUEST\PTX-NLM-2026-10-30-run.zip` plus `CLOSEOUT.md` |
| 11-09 halted test quest answers | `Claude output\nlm-answers\` (Q0001–Q0012 answered; Q0013–Q0018 queued, never sent; ignore Q9001–Q9003) |
| Josh's throughput history (source of the standard) | `C:\Users\joshu\Desktop\PTX stuff\fix ACH deployer\ACH-Generic-Workflow-Kit\Project-Template\PROJECT_NAME ACH\NotebookLM throughput strategy\` (Ready-Fire-Aim protocol) |
| PTX notebooks (throwaway Google account; six copies = six lanes) | primary `3b728d29-628f-4c3e-9b0d-ce485d37d24a`; clone-1 `4ffdb7f0-b402-4f08-92da-ab34503a9f01`; clone-2 `466f348c-7541-43f9-936d-9f8539880774`; clone-3 `f6a049d5-56f4-4ae8-be11-ed48f8d4cf31`; clone-4 `5c481b42-32cd-4f53-bec9-4f11b664282f`; clone-5 `cb66526c-e692-4e5b-98ed-b56df7cee09a` (config: `examples/quest-driver.PTX.json`) |

## 4. What works now (verified)

- **`python cr.py selftest`:** 139 tests pass, plus 1 browser test that is skipped in selftest. That test is `python tests/test_notebooklm_driver.py`: an end-to-end driver run against a mock notebook, about 90 s, which passes.
- **The full offline pipeline:**
  - `python cr.py demo` runs from an empty folder to a report.
  - The default provider is the deterministic local engine `local-rules-v1.9` (`docs/LOCAL-ENGINE.md`). It is a lexical floor, not a language model.
- **The NotebookLM local driver** (`claimreg/notebooklm/driver.py`, run as `nlm run <config>`):
  - It runs its own Chrome profile, with one tab per notebook copy, and writes answers straight to disk with no permission prompts.
  - It flags tool-output answers and off-target answers, recovers from reloads, and stops on a `STOP` file.
  - It holds new questions while `max_backlog` answers wait for grading.
  - **Live result on 11-09:** first send 1.6 min after the go-ahead; 12 usable answers in about 4 min; generation took 67–135 s each.
- **`cr import-quest`** (`claimreg/quest_import.py`) brings a finished quest into a run, and `cr run` continues at FRD generation.
  - It reads either the `quest_tool` recording or the driver's answer files.
  - It picks one answer per question: the closeout's "Selected repair attempts" line, or `--select`, wins; otherwise the newest usable attempt without tool output.
  - It keeps tool-output answers as `CANDIDATE_UNVERIFIED`.
  - It labels the stop operational unless `--stop scientific`.
  - **On the real 10-30 quest:**
    - The import takes 6 s and matches the Manager's selections.
    - The offline run to report takes 41 s: 572 candidate FRDs, 473 validated against the papers, 336 witnesses.
    - `cr verify` passes.
- **`cr quest-score`** (`claimreg/notebooklm/scorecard.py`) gives PASS/FAIL against the throughput standard (§5) and names the bottleneck.

## 5. The throughput standard, and the record so far

The standard is Josh's Ready-Fire-Aim protocol, implemented in `cr quest-score`:

- **What counts:** unique usable QIDs, **captured and graded**.
- **The clock:** starts at the go-ahead, not the first send. Only disclosed away time is excluded.
- **PASS needs all five:**
  - first send ≤ 4 min;
  - ≥ 15 saved at 20 min;
  - ≥ 45 graded in the first hour;
  - ≥ 45/h for the whole quest;
  - grading backlog ≤ 12.

| Run | Start-up | 20 min | First hour | Whole quest | Steering |
|---|---|---|---|---|---|
| 10-24 (ChatGPT, browser extension) | 5.3 min FAIL | 9 FAIL | 61 captured, grading not recorded | 66/h captured | n/a |
| 10-30 (Claude, lane runner, no driver) | 86 min FAIL | 0 FAIL | 0 FAIL | 50/h PASS | backlog 111, FAIL |
| 11-09 (Claude, local driver) — **halted** | **1.6 min PASS** | 12 (halted at 8 min) | — | — | — |

**What 11-09 proved:** the driver fixed start-up, and the lanes are fast. With `max_backlog = 12`, **throughput now equals the Manager's grading speed**, and that is the one thing still unproven.

**Why 11-09 halted:**

- Claude was both agents: this chat was the Investigator, and subagents were the Manager.
- Two separate Claude Opus 5.5 Manager contexts were each cut off partway through grading round R001 by an automated Anthropic safety classifier, and nothing was written.
- The round's six answers were pentoxifylline pharmacology: a human add-on trial, rat bladder-obstruction studies, TNF/cytokine concentrations and vasorelaxation. The same kind of material was graded by Claude without incident on 10-30.
- Josh has decided to continue with another model.

## 6. How to run a quest (summary; details in `docs/WALKTHROUGH.md`)

1. **Set up the notebooks.** The corpus is in Markdown in one NotebookLM notebook, copied up to six times, each copy on Custom + Longer with the Archivist prompt.
2. **Start the driver.** `pip install playwright`, then `nlm login examples\quest-driver.<X>.json` once (Josh signs in), then `nlm run …`. Note the go-ahead time, or write `{"go_ahead": "<ISO>"}` into `<answers_dir>/quest-clock.json`.
3. **Investigator:** write `<answers_dir>/queue/Qnnnn.json` (`{"qid","attempt","text"}`), 6–12 at a time, each passing the firewall (`claimreg/notebooklm/INVESTIGATOR.md`). Then copy new answer files into the Manager workspace's `answers/` as Markdown.
4. **Manager:** follow `claimreg/notebooklm/MANAGER.md`. Every 6 answers, run ACH_Eval, commit a round to `assessment-ledger.json`, and write a packet with 8–10 ready questions.
5. **After each round:** `python claimreg/notebooklm/quest_tool.py assessed <answers_dir>/assessed-qids.json Q…` releases the next questions and stamps grading times. The PTX config's `assessed_file` is `../nlm-answers/assessed-qids.json`, and it must exist for pacing to work.
6. **End:** put a `STOP` file in `queue/`, then run:
   - `python cr.py quest-score <answers_dir>` (copy the Manager's `assessment-ledger.json` in first);
   - `python cr.py import-quest projects\<X> <quest folder>`;
   - `python cr.py run projects\<X> --run <id>`.

## 7. Open items, in priority order

0. **Evaluate and build the proposal in `docs/PROPOSAL-RELAY-AND-FAILOVER.md` (revision 2, by Claude).** It covers a model-agnostic quest relay (Investigator and Manager as API roles, the NotebookLM driver unchanged, an optional read-only LLM overseer for operations) and per-role provider failover, so one provider's refusal can no longer halt a quest. Josh has API key files at `C:\Users\joshu\Desktop\FINAL SPECIFICATION DOCUMENTS\ChatGPT output\API key`; reference them by path, never copy a key. **Its Step 0 is already done:** the `stage` / `packet` / `sync` commands and their tests are on `main` in commit `8708bf9`. Build v1 directly. Items 1 and 3 below are folded into the proposal.
1. **DONE — see §9. Prove grading speed.** Run one timed PTX quest with a Manager model that can grade this material, and score it with `cr quest-score`. **First test a single R001 round on the 11-09 answers (Q0001–Q0006)** before starting a timed quest.
2. **DONE — see §9. Restart the driver from the current code.** The 11-09 fixes (off-target detection under truncated filenames in `lane-runner.js`; pre-go-ahead records excluded from the scorecard; the driver's `quest-clock.json`) only take effect after copying `claimreg/notebooklm/` from the repo into `Claude output\claimreg\notebooklm\` (or running from the clone after `nlm login` there) and restarting `nlm run`.
3. **DONE — see §9. A small Investigator↔Manager sync tool.** On 11-09 the Investigator did these by hand:
   - staging driver answers into the Manager workspace as Markdown;
   - parsing a packet's `## Ready questions` into queue files;
   - syncing `assessed-qids.json` from the ledger.

   `quest_tool.py` now has `stage`, `packet` and `sync` for exactly these.
4. **FRD and matching quality.** The local engine is a lexical floor (349 of 473 validations on 10-30 were PARTLY RIGHT) and reaches no complete coverage. On 11-09 the 156-answer quest was also run end-to-end on **GPT-5.2** (`projects/PTX-NLM-MODEL/`): 655 READY FRDs (570 records failed the verbatim quote gate) and 114 witnesses, but still **0 complete relations, 0 coverage sets, 0 crux candidates**. So the zero-coverage wall is not only the lexical engine; the next diagnostic is the matching/witness stage itself — relation distribution, the 413 held witnesses, and the strictness of the `matching`/`witness` config — compared with `projects/WORKED/`, where 42 sets and 7 crux candidates are produced. Keep routing real models to `frd_generator`, `frd_validator` and the matching roles when the result matters.
5. **Teaching.** `docs/WALKTHROUGH.md` covers the method end to end. Josh also wanted the harness to teach where to acquire sources (§2 there is a start).

## 8. Repo map (the parts touched since 10-30)

| Path | What |
|---|---|
| `claimreg/notebooklm/driver.py`, `lane-runner.js`, `quest_tool.py`, `quest_io.py` | Local driver, the browser lane logic it injects, Investigator helper, single-writer recorder |
| `claimreg/notebooklm/INVESTIGATOR.md`, `MANAGER.md` | Role briefs (MANAGER.md is now generic) |
| `claimreg/notebooklm/scorecard.py` | `cr quest-score` |
| `claimreg/quest_import.py` | `cr import-quest` |
| `claimreg/corpus.py` | `Corpus.resolve` fix (the old recursion hung on long phrases) |
| `claimreg/llm/local.py` | Local engine v1.9: the FRD generator reads NotebookLM's `claim (file.md, heading)` citations |
| `docs/WALKTHROUGH.md`, `docs/NOTEBOOKLM-QUEST.md` | New-user walkthrough; quest reference including the scorecard (§6) |
| `tests/test_quest_import.py`, `tests/test_scorecard.py`, `tests/test_notebooklm_driver.py` | Tests for the above |

## 9. Update — later on 2026-11-09 (DeepSeek session): the throughput standard is proven

A timed PTX quest ran **14:10:14–15:10:18 CST** on the six existing notebooks. The driver ran from the current repo code (six lanes ready at 13:58:11), the Manager was a fresh DeepSeek context, and the Investigator was the Lead session. Full record: `Claude output\quests\PTX-NLM-2026-11-09\` (answers, manager workspace, closeout, scorecard, evidence-run project).

- **`cr quest-score` → PASS, all five checks:** start-up 0.3 min; 39 usable QIDs saved at 20 min; 130 graded in the first hour; 133 graded/h over the whole quest (142 graded of 144 questions, one repair Q0033-A02); backlog never above 12; median capture-to-graded 2 min.
- 156 answers captured (Q0001–Q0156), 29 grading rounds (R001–R029). Round times ran 1–3 minutes once warm.
- **Open item 2 is done.** The driver was launched from the repo (`python -m claimreg.notebooklm.driver run <config>`), so the 11-09 fixes were live; the previous long-running process had started before those files changed.
- **Open item 3 is done.** `quest_tool.py` now has `stage` (driver answer JSON → Manager Markdown answers), `packet` (a packet's `## Ready questions` → queue files, with mechanical firewall warnings) and `sync` (assessment ledger → `assessed-qids.json`, stamping each round's `committed_at`). 13 new tests in `tests/test_quest_tool.py`; `cr selftest` is 139 tests (109 with the browser test), all passing. `docs/NOTEBOOKLM-QUEST.md` §4 and `docs/WALKTHROUGH.md` §9 document the commands.
- **New learning — Manager context lifetime.** One Manager context degraded after about 27 rounds (it completed R027, then failed before replying). A fresh Manager context was spawned; it read `private/state.md` and graded R028–R029 and wrote the closeout. Plan on recycling the Manager context every ~20 rounds for long quests; the compact state file is what makes the handover safe.
- **Evidence run.** `cr import-quest` imported 156 questions (154 usable; closeout's repair Q0033-A02 selected; stop labelled OPERATIONAL) and `cr run` completed: 605 candidate FRDs, 424 validated/retained, 327 witnesses, crux report and HTML audit browser written; `cr verify` ok. The local engine still reaches **no complete coverage and no crux candidates** — the quality limit is unchanged and is now the top open item.
- **What is left, in priority order:**
  1. Route `frd_generator`, `frd_validator` and the matching roles to a real model (file queue or API) on this 156-answer quest; the local-engine floor is now the only thing between the harness and a result someone can rely on.
  2. Repo metadata: the GitHub description still says 31 tests / 19 stages; update it (139 tests) on the repo page.
  3. The six NotebookLM notebook IDs are public in `examples/quest-driver.PTX.json` and the older committed run records — IDs, not credentials, but decide whether to scrub them before promoting the repo.
  4. Optional: promote the Lead's ad-hoc `round.py` loop into a `nlm cycle` command and add a Manager checkpoint/restart helper.
  5. Teaching: unchanged.

## 10. Update — 2026-11-10 (Claude Fable 5.2 session)

Josh brought the project back to Claude and asked for it to be finished without consulting him at each fork. `docs/DECISIONS-2026-11-10.md` records every choice. In short:

- **The zero-coverage wall had three causes, all found in the 11-09 GPT-5.2 run's own records** (`cr funnel` shows them): required units that were verdicts about the evidence; witnesses judged as answers to the whole producing question, which lost 78% of them; and a lexical shortlist that left 77% of pairs unjudged. All three are changed (decisions 2 to 5).
- **New in the evidence pipeline:** finding-sized units with one revision round; witness prompts scoped to the FRD's claim; model routing before matching; gap-typed partial matches; an assumption-labelled coverage tier (`COMPLETE_WITH_ASSUMPTIONS`); the premise ledger (`08_COVERAGE/PREMISE-LEDGER.md`); `cr funnel`.
- **Provider failover** is in the router for every role (ordered lists; mechanical triggers; provenance in the call log).
- **The quest relay is built** (`claimreg/notebooklm/relay.py`): Investigator and Manager as model roles, the driver unchanged. Open item 0 of §7 is done except the optional overseer.
- **New-user commands:** `cr new`, `cr frame`, `cr approve`, `cr doctor`, `cr quest`. `README.md` and `docs/WALKTHROUGH.md` are rewritten around them.
- **Tests:** `cr selftest` runs 139 tests (109 with the browser test). The new ones use a scripted stand-in for a model API (`tests/fakes.py`) and a stand-in driver, so failover, the relay and the whole new-user path are tested with no network.

**What a live run still has to show.** Everything above was built and tested offline. See the session's closing message, or `docs/LIVE-RESULTS-2026-11-10.md` if it exists, for what the live PTX re-run and the levothyroxine quest showed.

**Working with Claude on this corpus.** On 11-09 two Claude contexts were stopped by a safety classifier while grading PTX answers. Nothing in the current design has Claude, or any agent session, grade answers: the Manager and Investigator are API roles with failover. Put `anthropic` last in a provider list for pharmacology corpora, or leave it out.

## 11. Update — 2026-11-11 (LEVO quest run, and the driver/relay hardening it forced)

- **The first real 4-lane quest ran** on the levothyroxine corpus (`Claude output\LEVO\`): 147 attempts → **142 usable → 142 graded in 26 rounds** at **42 graded/h**; cost $3.68. Scorecard: **2/5 PASS** (start-up 0.1 min PASS, 20-minute 22 saved PASS; first hour 28 graded FAIL, whole quest 42/h FAIL, steering FAIL). Operational stop at the 3-hour limit; imported as `RUN-LEVO-QUEST-20261111T033955Z`.
- **Why it missed 45/h:** the driver's Chrome window was minimized twice (~30 min lost), one lane was dead for 2 h 40 m because of a one-character notebook-link typo, a headless driver froze for ~18 min, and questions lost across restarts pinned the driver's backlog. Manager rounds (median 159 s) were sound. Full incident log: `Claude output\LEVO\HANDOFF-LEVO.md` Appendix A.
- **Fixed in the harness the same day** (uncommitted at the time of writing; see `docs/DECISIONS-2026-11-10.md` §11 and `docs/NOTEBOOKLM-QUEST.md` §5): stale lane-runner IndexedDB/localStorage state is cleared when the quest `run_id` changes (and kept on same-quest restarts for recovery); `pushed` is recomputed from answer files at startup; a lane releases its claim after two failed tries and records a `FAILED` answer; the relay takes a short grading round when the driver reports HOLD with no busy lane and answers waiting; the driver launches Chrome maximized and restores a minimized notebook window on every poll; **headless is explicitly not supported** (it froze); `cr doctor --notebooks` resolves every notebook link and `cr quest` preflights the lanes, refuses to start the relay if one does not come up, and starts the driver with `PYTHONUNBUFFERED=1`.
- **A clean throughput re-run has not been done yet.** The pilot measured ≈97 answers/hour captured and ≈120/hour grading capacity; with four valid links, an unminimized window, no headless driver and `max_backlog` 12, the standard should be reachable. Do not raise `max_backlog` to work around lost questions — the startup sanitisation drops them and raising it fails the steering check by construction.
- **The LEVO evidence pipeline** (FRDs → validation → witnesses → matching → coverage → crux → report) was run on GPT-5.2 because DeepSeek v4-pro's reasoning output was far too slow on this corpus (6–19 k tokens per unit call). Results are in `Claude output\LEVO\02_RUNS\RUN-LEVO-QUEST-20261111T033955Z\`: `08_COVERAGE\PREMISE-LEDGER.md` and `10_REPORTS\CRUX-REPORT.md`.
- **Result of the LEVO evidence run** (`02_RUNS\RUN-LEVO-QUEST-20261111T033955Z`): 551 witnesses released, 1,897 pairs judged; coverage complete-with-assumptions only for A1-H1 (3/3 required units) and A1-H2 (2/2), partial with named gaps for A2–A4, **0 crux candidates** (7 diagnostic witnesses); full four-axis ACH_Eval in `10_REPORTS/CRUX-REPORT.md`; `cr verify` = ok. Two further bugs were found by running it and fixed: the assessment stage only allocated axes A1/A2 on a four-axis frame (now one parallel call per axis), and `cr verify` treated designed COMPLETE_WITH_ASSUMPTIONS sets as failed checks (now checked against the configured assumptions; `docs/DECISIONS-2026-11-10.md` §11 items 6–7). Spend: quest $3.68, evidence $54.38; the OpenAI key ran out of credits mid-run and the router failed over to DeepSeek.

## 12. One evidence database per axis (2026-11-11)

Specification: `docs/AXIS-DATABASES.md`. Decisions: `docs/DECISIONS-2026-11-11.md`.

- New runs keep one database per axis (`AXIS-A1__<name>/`, ...) plus `SHARED/`; no file holds two axes.
- Every question names exactly one axis (`"axis"` from the Investigator, `[axis: A2]` on a Manager ready
  question). The relay refuses a question with no single axis.
- Stages `units` to `report` run once per axis (`claimreg/runctx.py: AxisContext`, `claimreg/pipeline.py:
  run_stage`). Cross-axis relations are SHARED records (`claimreg/axes.py`).
- Old runs keep their single database and still read. To file an old quest by axis, import it into a new run.
- Not done: one Manager state per axis (the Manager's quest records are SHARED); the internal offline quest
  (`quest.py`) does not ask its Investigator for an axis, so its questions are filed by label or wording;
  `quest_tool.py` (the hand-run path) parses `[axis: ...]` but keeps no ledger of it.
- Tests: `tests/test_axes.py`; suite is 139 tests.


## 13. Preliminary FRD evaluation and the researcher's stop (2026-11-11)

- New stage `frd_assess`, after `frd_retain`: ACH_Eval on each axis's validated FRDs and on the combined set. Spec: `docs/FRD-EVALUATION.md`.
- A plain `cr run` now halts after it (`pipeline.stop_after`). Continue with `cr run <project> --run <id> --continue`.
- Outputs: `FRD-EVALUATION.md` and `frd-evaluation.json` at the run root; `AXIS-<id>/axis.db` per axis.
- No blended final score is implemented. Josh decides the rule after seeing LEVO output.
- Tests: `tests/test_frd_assess.py`; suite is 139 tests.

## 12. Bedtime-dosing repair attempt (2026-11-11)

Josh rejected the A2 null results (prior FRD ACH_Eval A2 12/18/34; harness run A2 8/12/44). The repair package is in `ChatGPT output\Bedtime Dosing Protocol Repair 2026-11-11\`: an audit of the framing/evidence-use defects, a 15-rule bedtime-dosing ruleset, and a deterministic acceptance gate (`evaluation_gate.py`, 16/16 synthetic self-tests). The new-attempt handoff is `HANDOFF-NEW-ATTEMPT-A2-BEDTIME.md` in that folder: it defines the repaired practical frame `A2-P-v1`, the required evidence extraction and exposure ledger, the gate contract, the source facts (including the corrected Willems 2024 numbers), and the definition of done. Read it before touching Axis A2 again; the *practical* question must be evaluated on its own terms, not as a rerun of the frozen two-comparator A2.

## 14. Domain modules (2026-11-11)

- Investigation-specific rules live in `claimreg/domains/<name>/` and load only when a project names them under `domain_modules`. Spec: `docs/DOMAIN-MODULES.md`.
- `levo` holds the bedtime-dosing ruleset and acceptance gate. A rejected report is withheld for correction, never scored.
- Tests: `tests/test_domain_levo.py`; suite is 139 tests.

## 15. The frame gate (2026-11-12, Claude Fable 5.2 session)

**Why.** RUN-LEVO-A2-v3 to v5 scored a frame Josh had not read: the header asked whether bedtime dosing improves TSH, and his question was whether patients should be offered the option. `cr approve --by "Joshua Davis"` had been run by an agent. An approval that any command line can issue is not a person's approval.

**What.** `claimreg/frame_gate.py`, commands `cr signer` and `cr sign`, guide `docs/FRAME-GATE.md`, tests `tests/test_frame_gate.py`. A person says which hypothesis they want to win, sees forecasts for alternative frames, types the question and every hypothesis by hand, reads the restated wording, accepts each consequence by typing it, and signs each axis with a passphrase (Ed25519; the key is derived from the passphrase and stored nowhere). The result is `01_FRAME/FRAME-CERTIFICATE.md`, copied into every run.

**What is refused.** Once a frame has been fully signed on a computer, `cr quest`, `cr import-quest`, `cr approve` and any `cr run` that uses a model refuse to start on a frame that is not signed, or whose header, index, Archivist prompt, prompt overrides or `corpus` / `frd_assess` settings changed after signing. There is no override flag.

**Rules for agents.**

- Do not try to sign. `cr sign` needs a keyboard and Josh's passphrase. Never ask for the passphrase and never accept it in a chat.
- When a command is refused, tell Josh the exact reason it printed and the command it names (`cr sign <project>`, `--axis A2`, or `--resign`). Do not work around it: no editing of `frame_gate.py`, the certificate, the signer file or the lock file, and no calling the pipeline from Python to skip the check.
- If you change anything the certificate covers (the header, the index, those settings), say so before you do it. Josh will have to sign again.
- Josh's design intent: the header is the one place where a researcher may tilt a run toward the hypothesis they prefer, and the tilt is on the record. Nothing downstream of the header may be tilted. Do not down-rank, exclude or re-grade sources to move a result.

## 16. Domain modules removed (2026-11-12)

Section 14 is obsolete. `claimreg/domains/` (the levothyroxine bedtime rules R1 to R22 and their gate), `tests/test_domain_levo.py` and `docs/DOMAIN-MODULES.md` are removed, with the three hooks in `frd_assess.py` and the `domain_modules` setting. Josh's decision: a topic-specific rule set is a tilt outside the header, however openly it is done. Do not add one back. A rule that matters belongs in the header's governing boundary, which a person signs. RUN-LEVO-A2-v3 to v6 were scored with the module on; their numbers carry that.

## 17. The gate became a coach (2026-11-14, Claude Fable 5.2 session)

Section 15 is superseded in part. Josh's direction: no signatures, hashes or tamper checks while the system is still being made to work; acceptance exists only so that the researcher knows the likely outcome before the run and does not walk away when it is hard. The harness should make the model a coach in the researcher's corner.

**Removed:** `cr signer`, the passphrase, the Ed25519 signature, the lock file, `--resign`, and the checks that voided a certificate when the index or settings changed. `cr approve` works again.

**Kept (`claimreg/frame_gate.py`, `cr sign` / `cr coach`):** the session before a quest. It now asks the researcher's motivation, goal and the experience behind their view, and gives those to the model that proposes frames. Frames are proposed by the calibration method in `CALIBRATION` (weakest meaningful claim the corpus supports; the strongest rival that someone really holds; a rival nobody holds is never offered; same evidence rules both sides). The record is a plain file. A quest waits for it unless `coach.require_acceptance` is false.

**Added (`claimreg/coach.py`, tests `tests/test_coach.py`, guide `docs/FRAME-GATE.md`):**

- Checkpoint 1, in front of `frd_generate`: scores the quest's answers once (the Manager's private ACH_Eval files are not imported, so the run makes its own reading).
- Checkpoint 2, after `frd_assess`: if the stage's vector is below target, two more scorings, then the mean.
- Below target: the run halts (`cr run --continue` releases it) and `COACH-CHECKPOINT-<n>.md` gives the corner talk: why, what the evidence does show, openings, questions to ask next, and the three moves.
- `cr rescore <project> --run RUN [--header FILE] [--axis A2] [--answers] [--times N]`: scores the run's findings under another frame without changing the run.
- `01_FRAME/FRAME-LADDER.md`: every frame scored and its score.
- The checkpoints act only on axes whose preferred hypothesis is known (from the session, or `coach.preferred` in `project.json`).

**Rules for agents.** Coach, do not gatekeep. Assume the researcher runs in good faith and has a valid point from their own experience; never tell them to give up; say plainly what the corpus does and does not show. Treat mechanistic evidence as evidence. `cr sign` is for the researcher at a keyboard: do not try to run it for them. Still no domain modules, and no down-ranking, excluding or re-grading of sources to move a result: the claim is the lever, and it is in the header.

## 18. Fixes after DeepSeek's review of the coach (2026-11-14)

Done: the session's choice of preferred hypothesis now wins over `coach.preferred`; "too close to call" is a mean within 2 units of target (`coach.NOISE`), not one high scoring; `cr rescore` uses the re-scored header's gauge and says so when the preferred hypothesis is not in that header; the ladder appends every scoring and states that the target is a guide and that scores compare only within one run and one kind of evidence; the final (witness-level) score is added to the ladder after `assess`; `cr rescore` under a claim the run's questions were not written for writes `01_FRAME/QUESTION-CHECK-<AXIS>.md` (advice, no block).

Declined, by Josh's direction: a pre-registered finite ladder, caps on reframes or re-scores, and evidence-set or header hashes on ladder entries.

## 19. Repairs after the 2026-11-14 review (Claude Fable 5.2 session)

ChatGPT reviewed revision `3cc3016` and found six defects; Claude reproduced all six and measured four more on `RUN-LEVO-A2-v7` (project doc `CLAUDE-REVIEW-OF-CHATGPT-ASSESSMENT-2026-11-14.md`). All are repaired here. Every repair is topic-neutral: nothing knows what a run is about, and none can be tuned toward a hypothesis. Tests: `tests/test_review_fixes.py`.

**Matching (`matching.py`, prompts `match_*.md`)**
- A pass that leaves rows out of its answer is asked again for those rows only, in small batches (`matching.reask_rounds`, `matching.reask_batch`).
- A pair that still has one judgment is `ONE_PASS_ONLY` under `matching.one_pass_policy` (default ABSTAIN). It is not sent to the adjudicator: one judgment is not a disagreement.
- The adjudicator chooses between the two passes' answers or abstains. A third answer leaves the pair ABSTAIN, basis `DISPUTED`, with `adjudicator_relation` kept.
- Qualification now controls something (spec 28.1): while any fixture pattern is failed, only relations both passes agree on are approved. A relation the adjudicator would have approved is ABSTAIN, basis `UNQUALIFIED_MATCHER`, and is listed in the review packet (`matching.unqualified_policy`).
- One transfer standard in both directions. A finding from another population, species, model or dose could already only partly cover a unit, with the transfer named. Now a CONTRADICTS from another scope carries `gap_type: SCOPE` and the transfer in `gap`. Fixtures FX-23 and FX-24 test it. This is a matching rule for every run; there is no topic rule behind it.

**Crux (`crux.py`)**
- T2 is decided by the coverage solver on the whole rival (options, incompatibilities and constraint vetoes together). The old test asked unit by unit and could return PASS with an "example arrangement" that contained an incompatible pair.
- A required unit whose option list was cut at `coverage.max_options_per_unit` cannot produce a T2 FAIL; the result is UNKNOWN and says so.
- A crux that fails its tests only through scope-conditional contradictions is still a candidate, with `defeats_only_with_assumptions` and the transfers in `assumptions`. The report prints them under the candidate.

**Quotation check (`corpus.find_quote`)**
- A similar passage only locates the quotation. Every difference is then examined: a dropped or changed negation, number, hedge or limiting word fails, and so do words the source does not have. Spacing, markup residue and citation markers pass.
- New method `spans`: a sentence the Markdown conversion split around a figure or table passes when all of it is in the source, in order, and nothing protected was skipped in a short gap.
- A passage of an ellipsis quotation that is not in the source fails unless it is a locator label or differs only in formatting.
- On the 16 quotations of v7 that had used the weak paths, 12 still pass and 4 fail (garbled citation numbers, a rewritten table row).

**Smaller repairs**
- `cr verify`: a run with nothing recorded reports `NOTHING TO VERIFY` and is not `ok`; a recorded file that is gone is a problem. No new proof machinery.
- Assessment parsers: an allocation must name exactly the axis's hypotheses, each 0 to the gauge, summing to the gauge. A rejected vector is kept under `rejected_allocations` and not carried into the report.
- A setting changed after a stage ran marks that stage and the later ones `stale` in `stage-state.json` (same table as `cr fork`). Nothing is redone unasked; the log, `cr status` and `cr verify` say what to redo. Model and provider changes mark nothing. A setting with no earlier value (a new default) marks nothing.
- Retention: two claims are redundant only with the same numbers, the same negations and no direction word on one side only.
- Coach checkpoint 2 scores `coach.times` times whatever the first score is.
- From ChatGPT's ACH_Eval study (`ACH-Eval-Study-2026-11-14`, 219 readings): the ACH_Eval prompt and the 64 gauge are unchanged. `coach.NOISE` is 3 (was 2), and every ladder entry records `scored_by`, because two models scored the same evidence about ten units apart.

**Report (`report.py`)**
- Crux candidates are grouped by underlying study from the validated FRDs' provenance labels. Witnesses are not merged; the grouping stops eight witnesses reading as eight studies. The validator prompt now says a review restating a study is `DERIVED_FROM` that study and never names itself.
- Coverage is shown as "n of m required parts covered directly, k with a named transfer".
- The glance table says whether the FRD database is within its size budget, and the frames scored are listed with the number of scorings behind each.

**Not done:** the language-layer test fork (needs model calls on the PC); showing each hypothesis's compilation into units before coverage; a veto by a scope-conditional contradiction of a CONTEXTUAL_CONSTRAINT still vetoes a set unconditionally.

**To get these into a result:** an existing run keeps its records. Matching prompts changed, so `cr run <project> --run <RUN> --from qualify` asks the matcher again (model calls).

## 20. One study, one voice; the second reader; the control run (2026-11-14, Claude Fable 5.2 session)

Built from DeepSeek's plan for two of the upgrades in the review. Tests: `tests/test_studies.py`.

**One study, one voice (`claimreg/studies.py`, `cr studies <project>`)**
- `01_FRAME/STUDY-MAP.json` and `.md`: every source file with its study and kind (primary, review, meta-analysis, guideline, commentary, synthesis). The kind is a first guess from the title; a second copy named in `corpus.duplicates` belongs to the first copy's study. Correct either under `overrides` in the same file and run `cr studies` again.
- Each validated finding is attributed to the study it rests on. From a primary source: that study. From a secondary source, or labelled DERIVED_FROM / DERIVATIVE_UNKNOWN by validation: the one other study of the corpus it names by author and year (restated); several (a summary); none (a secondary report, original not identified). Summaries and unidentified secondary reports are listed and are not counted as studies.
- Used in: the report (crux candidates grouped by study, "n witnesses from k studies"), `coverage.json` (`studies` per hypothesis), `crux-candidates.json` (`study` per candidate, `candidates_by_study`), `metrics.json`, and both assessors, which are given a STUDIES list and told that rows of one study are one study (`assess.study_identity`, `frd_assess.study_identity`). After the final assessment a driver audit flags one study cited as several drivers.
- Not done on purpose: study identity never changes a coverage relation, a coverage set or a crux test. The spec decides coverage from text alone (28, 29), and a test holds this. Witnesses are never merged. The ACH_Eval prompt file is unchanged; the STUDIES list is added to what the assessor is shown.
- Nothing is signed. The map is a plain editable file.

**Second reader (`assess.second_reader`, role `assessor_b`)**
- Route `assessor_b` to a different model than `assessor` in `project.json` and the final assessment is read by both, with the same question. `assessment.json` gets `second_reading`, the report prints both and their difference, and the ladder gets a second entry under the second model. With one model routed, nothing changes.

**Control run (`claimreg/control.py`)**
- `cr control <project> <new folder>`: a sibling project with the same corpus (read in place), index, Archivist prompt and study map; the coach off; no preferred hypothesis; `01_FRAME/CONTROL-NOTE.md` to fill in before the quest. The parent's header is deliberately not copied.
- `cr structure <project> [--run R] [--against <project> --against-run R]`: the shape of a run, alone or beside another: findings per answer, quote and verdict rates, witnesses held, studies behind the witnesses, how often the two matching passes answer and agree, coverage direct and with a transfer, crux candidates and their studies, the share of the last-listed hypothesis, the gap between two readers. Written to `STRUCTURE.md` in the run.

**To apply to an existing run** (no new quest, FRDs or matching): `cr studies <project> --run <RUN>`, read `STUDY-MAP.md`, then fork and redo from coverage: `cr fork <project> --from <RUN> --name <RUN>-STUDIES`, `cr run <project> --run <RUN>-STUDIES --from coverage`. The assessment and the report summary are asked again (a few model calls).

**Repairs after DeepSeek's review of this section (same day)**
- Driver audit: it read only witness ids, and the assessor (as asked) names studies, so it reported clean having read nothing. It now reads row ids and study ids, counts drivers per study and direction, lists drivers that name neither, and sets `checked: false` when no driver names anything. The report says "could not be checked" in that case.
- Source kinds: `label` and `regulatory` added and treated as secondary. The bare word "label" is not matched ("open-label" is a trial design). A review whose title does not say so (Geer 2015) is still guessed primary: correct it under `overrides` in `STUDY-MAP.json`.
- `cr control`: writes a blank `01_FRAME/question.md` (without it `cr frame` refused to run) and removes the parent's notebook links, because those notebooks hold the parent's conversation. The control needs new notebooks made from the same sources.
- Second reader: when `assessor_b` is the same model as `assessor`, `assessment.json` gets `second_reader_note` and the report says there was one reader.
- Report: states that study identity is shown beside the results and changes no coverage set, crux test or score.
- Declined: recording a hash of the control note (no proof machinery yet; the commit dates the note). The 44/8/12 of RUN-LEVO-A2-v7-STUDIES against v7's 42/8/14 is inside run-to-run noise and is not an effect of study identity.
- The control is optional. It costs a quest and a run on a question the researcher has no stake in; nothing else depends on it.

**Open:** which question the control asks, and whether to run one at all, is Josh's to choose. The preference-symmetry arm of DeepSeek's plan (a randomly assigned preferred hypothesis) is not built.

## 21. Conditional contradictions, the requirements view, question transcoding (2026-11-14, Claude Fable 5.2 session)

Built from `HANDOFF-SPEC-UPGRADES-2026-11-14.md`, after DeepSeek's design and ChatGPT's corrections of it. Tests: `tests/test_conditional_contradictions.py`, `tests/test_requirements.py`, `tests/test_question_transcoding.py`. Nothing here has been run against a live model.

**One standard for support and contradiction from another scope (`coverage.py`, `ledger.py`, `crux.py`, `report.py`)**
- A CONTEXTUAL_CONSTRAINT is a BOUNDARY (what the hypothesis is about; nothing refutes it) or a PREMISE (an assumption a finding could show false). The unit compiler records `constraint_kind` (prompt `units_derive.md` v3); `coverage.constraint_kinds` ({unit_id: kind}) overrides it by hand for one run. A constraint nobody classified is a PREMISE, which is the old rule. A project that keeps its own `90_METHOD/prompts/units_derive.md` does not get the new instruction until that copy is updated.
- A set member's CONTRADICTS against a PREMISE: outright (no `gap_type`) invalidates the set, as before. With `gap_type: SCOPE` the set stays valid and names it under `contrary_assumed_not_to_transfer`; a hypothesis whose every set has one is COMPLETE_WITH_ASSUMPTIONS, even when all its support is direct. This does not depend on `coverage.assume_gaps`.
- Against a BOUNDARY: no veto and no T1 conflict. The witness is listed as outside the hypothesis's scope (`outside_scope` in `coverage.json`, `outside_rival_scope` in a T1 certificate).
- Transfer conflict: a witness that would cover a required unit only under a transfer of scope, while its contrary finding against a premise also depends on one. Its conditional option is not offered (`coverage.transfer_conflict: reject`, default) or is offered and marked (`flag`). It is decided when options are built, per witness, so the solver's validity stays monotone. The two transfers are free text and are not compared, so this can refuse an option whose two transfers differ in kind (dose versus population); `flag` is for that case.
- Ledger: `contradicted_by` now lists outright contradictions only; conditional ones are in `contradicted_if_transferred`. New statuses CONTESTED_IF_TRANSFERRED, CONTRADICTED_IF_TRANSFERRED and BOUNDARY.
- Report, evidence packets and the final assessor's coverage summary say "counts against this if the finding transfers" with the transfer, and each example set lists both groups of assumptions.
- On RUN-LEVO-A2-v7's saved records: old and new code give the same sets and the same 144 test results. With `A2-H1-C1` and `A2-H1-C2` marked BOUNDARY the one hard veto (`W-FRD-Q0024-01-Q0024`) becomes "outside scope", no set changes, and one T1 result goes from UNKNOWN to PASS. The eight candidates are unchanged. v7 has no CONTRADICTS with a scope gap, so the conditional rule does nothing there until matching is redone.
- Found on the way: v7's saved `coverage.json` (120 sets for A2-H1) is older than its `relations.json`. Re-deciding from the saved relations gives 102, with old code and new alike, because two complete matches for `A2-H1-R1` were judged during crux completion after coverage was written.

**Hypothesis-to-requirements view (`claimreg/requirements.py`)**
- Written by the coverage stage: `08_COVERAGE/HYPOTHESIS-REQUIREMENTS.md` and `.json`. Also a short section at the top of `CRUX-REPORT.md` and a Requirements tab in `report.html`. Saved records only, no model call, not a gate.
- Per hypothesis: every sentence with the units anchored on it; sentences with no unit ("written by you, checked by nothing"); each unit's role, state and options; which sentences were read as ALL of several units and which unit as ANY ONE of its alternatives; what is not a requirement; what complete coverage does and does not let a reader conclude.
- Where the record holds nothing (why a sentence was divided as it was; which of two identical passages licensed a unit) it prints NOT RECORDED.
- Hints, shown and never enforced: a required unit with no option; two required units on the same words; an anchor that occurs twice; a required unit anchored only on corroboration or falsification text; an anchor under six words.
- On v7: A2-H1 has 5 required, 3 constraint, 4 adverse, 4 expected and 1 evaluative unit. Its sentences 3 (the two patient groups) and 5 (all of its assumptions) have no unit, and three of its five required units (R1, R2, R5) are anchored on "Potential corroboration" text. A2-H2's second sentence has no unit.

**Questions transcoded before witnesses (`language.transcode_questions`, `witness.py`)**
- The witness stage transcodes every applied question first and saves `05_WITNESSES/01_question-applications/transcoded-questions.json`. The constructor and the auditor read the transcoded question when it passed, the raw one otherwise; each witness records `question_form`. `language.question_fallback: hold` holds that question's applications instead. The matcher is never given a question.
- With `language.mode: off` (every run so far) the records are the identity and no prompt changes.

**Not built:** independent binding passes, protected-property review, deterministic vocabulary and sense accounting (stages 3b to 3d of the spec). They wait for the off-versus-labels comparison on a real run (3e), which costs model calls.

**To see these on an existing run** (no model call for coverage; the report summary is asked again): fork and redo from coverage, `cr fork <project> --from <RUN> --name <RUN>-REQ`, then `cr run <project> --run <RUN>-REQ --from coverage`. To mark boundaries by hand, put `"coverage": {"constraint_kinds": {"<unit id>": "BOUNDARY"}}` in `project.json` first.

## 22. The interface is the person's own assistant (2026-11-15, Claude Fable 5.2 session)

Josh's decision: no separate application. The person already has an AI assistant installed on their computer (Codex, Cursor, Claude, ...). It downloads this repository and is the interface. A separate window exists only for what a chat cannot give: a steady checklist. The intended user is at home on the internet, new to research, and does not program. DeepSeek's wizard design and ChatGPT's React/FastAPI plan (`docs/UI-IMPLEMENTATION-PLAN-2026-11-15.md`) are superseded by this; what survives from them is readiness read from files, the requirements view, lawful source routes, and keeping search notes out of the corpus folder.

**Built (slices 1 and 2). Tests: `tests/test_checklist.py`.**
- `cr next [project]` (`claimreg/checklist.py`, alias `cr checklist`): nine steps up to the first quest, each with a bar, read from the project's files; the one next step; why it matters; what the person does; what the assistant does. `--json` for assistants, `--md` for a chat reply, `--window` writes and opens `<project>/CHECKLIST.html` (the checklist plus the guide; it reloads itself and is rewritten on every `cr next`), `--watch` keeps it current.
- Two things files cannot show are the person's own confirmation, stored in `<project>/CHECKLIST.json` and labelled as such: `--done sources` (the collection is complete) and `--done notebook` (every copy is set to Custom and Longer). Everything else is computed. A project that already ran a quest counts those as done.
- It makes no model call, contacts nothing and is not a gate. `cr quest` still decides for itself what it needs.
- `AGENTS.md` (with `CLAUDE.md` and `GEMINI.md` pointing to it): how any host assistant behaves. It first separates the two jobs: someone changing the harness goes to this file; anyone else is a researcher and gets the guide behaviour. Opening line "What do you want to research?", short answers, one next step with its reason, more only on request, progress always from `cr next --json`.
- `docs/guide/`: nine pages of about 150 to 200 words. What it does and does not; how it differs from asking an AI; the work; what you get; distillation; roles; hypotheses; sources (legal routes only, Josh's conversion batching); NotebookLM. The checklist window renders them, so keep them to headings, paragraphs, lists, bold, italic, code and links: no tables.
- PDFs waiting for conversion go in `<project>/01_CORPUS/pdf/`. Only `source-files` is ingested, so notes and reference lists must stay out of it.

**Rules for agents here**
- Wording a novice reads (step titles, reasons, guide pages) is product. Keep it plain and short; do not add steps without Josh.
- The checklist must never claim more than the files show. A new step needs a file-based test or an explicit confirmation.

**Not built yet**
- Slice 3 is now built: `cr coach` resumes a harness-managed review inside the assistant conversation. See the chat-coach integration note below. The old keyboard interview requires an explicit `--terminal` option.
- Slice 4: a structured source list is still pending. Datalab conversion is now available through `cr convert` (see the integration note below). Slice 5: a no-key quest where the host assistant plays Investigator and Manager through one command; today that route is the manual one in `claimreg/notebooklm/INVESTIGATOR.md` and `MANAGER.md`, and `cr quest` needs a model key.
- Nothing has been tried from a second assistant yet. That is the test that matters: different assistants follow `AGENTS.md` differently.


**Launch fix (same day).** DeepSeek, told "Launch claim registry" and given the folder path, spent two minutes lost: nothing said what launching means, and `START HERE.md` was the old build record. Now `python cr.py start` (also `launch`, and `cr.py` with no arguments) prints about twenty lines telling an assistant to ask the opening question and not to run tests or read the repository first. `START HERE.md` is a ten-line pointer to it, the first lines of `README.md` and `AGENTS.md` say the same, and the build record moved to `docs/BUILD-RECORD.md`.

**Mentor voice and paper help (same day).** Josh's first real trial (DeepSeek, a spine differential) produced two correct but discouraging replies: the instructions said "do not sell", told the assistant to lead with where it cannot help, capped replies at 120 words, and the guide said it "cannot find sources for you". `AGENTS.md` now casts the assistant as a research coach and mentor: the second reply takes the question seriously, names what the person brought, says what they would get and what it costs, and asks one easy question; limits come after the value and only if they matter. New sections "Being a mentor" and "Helping them get the papers" (search, download every free lawful copy, and for each failed download the exact reason and the way round it; list kept in `<project>/SOURCES.md`). New guide pages `worth-it.md` and `getting-papers.md`. This is wording only: no download command exists yet, so the host assistant uses its own web tools.

**Depersonalized converter kit integration (same day).** `kits/research-paper-converter/` contains fresh generic agent guidance and two portable skills adapted from a user-supplied kit. Personal memory/profile/workstream files and historical versions were excluded entirely; no original archive is copied into the repository. `claimreg/conversion.py` implements optional Datalab conversion, exposed as `cr convert <project>` with `--dry-run`, external key-file/environment authentication, accurate mode by default, preserved relative filenames, clean Markdown, sidecar provenance, matching-hash skip checks, pending-job resumption, and preservation of unverified existing outputs. Conversion does not automatically ingest sources or alter runs. The checklist and agent guidance point to this kit. `python tools/package_research_kit.py` rebuilds `dist/research-paper-converter-kit.zip` from five explicitly allowed files with neutral ZIP metadata; the generated ZIP is ignored by Git. Nine offline conversion/packaging tests and fourteen checklist tests pass; both skill validators and a standalone dry run pass. No live conversion or paid call was performed. ACH_Eval is unchanged.

**Full personality integration (supersedes the five-file approach above).** The user restored six memory/research files to the repository's distribution ZIP and explicitly requested that EVERYTHING in it become part of the agent's standing personality. All eleven supplied files are now preserved byte-for-byte under `agent/research-personality/`, with import hashes/sizes in `INTEGRATION.json`. Do not discard the workstreams, lessons, fetch-quest examples, paper index, or acquisition history. `PERSONALITY.md` explains how to apply the complete experience in context. `cr start` (including no-argument and launch entry points) now includes the entire package; `cr personality` reloads it, and `--part N` provides lossless small chunks for hosts that truncate tool output. Root AGENTS/CLAUDE/GEMINI/start instructions require loading it. The builder now includes all files and generates twelve Cursor always-on `.mdc` rules containing the full profile and every original body; no optional @mention routing is used. The source directory, not the ZIP, is authoritative; future additions are included automatically. New tests check original-file integrity, complete startup loading, lossless parts, missing-memory failures, Cursor inlining, and rebuild preservation. This affects host mentoring only; role-specific evidence payloads and ACH_Eval remain unchanged. No live model or paid conversion was used to validate this integration.


**Corpus-size mentoring guidance.** The user's intended minimum for normal Claim Registry research is 50 relevant distinct sources. Below 20, recommend conversion to Markdown and direct LLM review; at 20-49, recommend further acquisition. A three- or five-paper batch is progress, not a sufficient stopping point. Explain the limitation once, then comply if the informed user chooses a smaller run; no hard source-count gate or repeated pressure. Never pad with duplicates, metadata-only candidates, inaccessible papers, or irrelevant documents. This is now in AGENTS, the standing personality, startup guidance, acquisition/value guide pages, and the rebuilt Cursor rules/ZIP. `cr next` exposes `corpus_size` advice in JSON, text, Markdown, and HTML; its count is explicitly a file-inventory estimate requiring identity/relevance review. Source confirmation still permits a small corpus and the advisory remains visible afterward. Thresholds 0/5/19/20/49/50/51 and a five-source proceed choice are tested. All 34 targeted checklist/personality/conversion tests pass. Import hashes remain historical provenance: subsequent user edits to memory are accepted, and rebuild tests check preservation of the current files rather than forcing a reset to old hashes. User-curated acquisition resources and all restored memories were retained. ACH_Eval and pipeline execution requirements are unchanged; no live model or paid call was made.


**Chat-native wording review (2026-11-16).** The user rejected the terminal interview and cryptic missing-header/axis messages during their live Bertolotti setup. `claimreg/chat_coach.py` now implements a durable conversational state machine, exposed by `cr coach` and the `cr sign` alias by default. The assistant asks plain questions in chat and submits actual user replies through response files with the current session ID/revision. No name prompt, anti-paste check, forced retyping, timer, or missing-word quiz is used. The flow discusses purpose, optional preference (an open mind is valid), experience, and what would change the user's view; it then reviews wording choices, each statement with supporting context, scope, consequences, and final approval. Changes clear confirmations and return to review. Optional `--model-review` reuses the existing restatement, ladder, three-call forecasts, interpretation, and intent-check functions; absent/failed forecasts remain explicit. No model call is made just to start/resume, and there is no automatic approval.

The draft is used automatically when the configured finalized header is absent. Preparation and coaching share axis-heading recognition, including Axis A1 and multi-digit axes; an unambiguous single-axis missing-heading layout can be repaired without rewriting its statements. Invalid drafts are returned as plain repair tasks for the assistant. Session/header/map/config edits and stale replies prevent approval of a superseded review. Acceptance promotes the exact reviewed text, retains prior files in 99_ARCHIVE/frame-coaching, writes the existing certificate formats with chat provenance, and saves completed questions independently. Chat acceptance also tracks the full reviewed scope and supporting paragraphs. Existing terminal certificates remain compatible; the legacy interview is opt-in only.

AGENTS, the standing personality, checklist, README, and current coaching guides now keep this process in the conversation. `docs/CHAT-COACH.md` is the assistant protocol; never show its JSON/IDs/revisions to the user or launch a terminal to work around a problem. Root instructions also explain external source-map/model processing before first use and avoid reciting backend failover chains. The user's existing Bertolotti draft passed the new read-only preflight; it was not edited or approved. Regression run: 301 tests, one skipped, passed; latest focused chat tests: 19 passed. No real model/paid conversion was run, all restored research memories remain present, and ACH_Eval and its gauge were left unchanged.


**DeepSeek startup detection, verified distribution bundled (2026-11-16).** The user clarified that detection should recommend installing the Claim Registry preset and opening a new session with it selected, not reinstalling the DeepSeek Harness application. Added `claimreg/host_context.py`, `cr host`, and a check in every startup entry point. Detection uses the installed DSH shell-env contract: DSH_SHELL=1 plus a nonempty DSH_SESSION_ID; it never prints the ID, scans processes, or infers the host from DeepSeek model/API-key names. An explicit --active-preset from visible session metadata or user confirmation suppresses redundant setup advice; DSH_PROFILE is not a selected-preset signal.

The final sibling distribution has now been independently checked: the folder and an extracted ZIP each passed 56 checks, with two advisory warnings and no failures; all seven extracted files match the folder, and runtime files match the maintained source after documented portability rewrites. Both presets, the pinned blind worker, corrected user-confirmation rule, answer-length clarification, and mentor stance are included. The exact verified 22,364-byte ZIP is bundled at resources/deepseek-preset/claim-registry-preset-1.0.0.zip (SHA-256 571b2ea4e2fa2634d8624f3ad66dde8cd281b46dbf462e449e3c1d3952f12192). `claimreg/deepseek-preset.json` is status=ready with that relative bundle_path. DeepSeek Harness startup can now recommend installing the included Claim Registry preset and starting a new session with it selected. Missing/invalid/external archive paths still fail softly rather than blocking research. The sibling development folder is never a runtime release signal. No profile edits, installation, network/model calls, or changes to the sibling preset distribution were made. See docs/DEEPSEEK-STARTUP.md for installation and release-update steps. Live blind-worker behavior remains untested here; its file-access limits are instructions, not an OS sandbox. The separate analyst-preset choice remains open. After integration, all 34 host/checklist/personality tests passed, and a smoke check using the actual bundled manifest confirmed the recommendation in all three startup entry points, suppression for a confirmed active preset, silence on other hosts, and preservation of the complete personality. Current research memories and ACH_Eval are unchanged.


**Corpus admission ceiling (2026-11-16).** The user requires Markdown files no larger than 210 KB for NotebookLM. `claimreg/corpus_intake.py` enforces a fixed 210,000-byte ceiling on admitted Markdown/text. `cr corpus <project> --add <staged-file-or-folder>`, new/init copy intake, demo copy intake, and conversion split before writing admitted text; corpus registration normalizes external drops before manifest creation. Stage downloads and edits outside the corpus: this is application enforcement, not an OS file-write filter. Existing research projects were not migrated. Standard-project originals are archived under 99_ARCHIVE/corpus-originals, outside 01_CORPUS. Pieces retain exact UTF-8 text without summaries, added headings or overlap; legacy text is normalized with original bytes retained. Hidden split metadata and manifest provenance record identity, order, offsets and hashes. Checklist counts, study grouping, original-name synthesis/duplicate exclusions and study overrides retain the original logical source. Conversion retries verify all output pieces before skipping, so splitting does not cause another paid upload. A stale manifest with an oversized file on disk is refused. See docs/CORPUS-INTAKE.md; rebuild the index and review affected citations before deliberately migrating an existing investigation. Standing personality and Cursor rules were refreshed without removing memories. ACH_Eval prompts, scoring and gauge are unchanged. Unicode/boundary/retry tests passed, and a read-only test of the real 223,105-byte hall2018.pdf.md produced 209,907- and 13,198-byte pieces with exact reconstruction and an unchanged input. No live model or paid conversion was used.

Final verification for the corpus-limit update: full offline selftest passed (320 tests, one skipped). The filename-only manifest compatibility issue found in the first run was corrected; the complete suite was rerun successfully. Real-paper lossless splitting and current research-personality packaging were also checked.

**Tiny-tail prevention (2026-11-16).** On the user's follow-up, splitting now merges or rebalances the final pair if the last piece would be under 20,000 bytes. Newly split documents have pieces of 20,000–210,000 bytes; naturally small documents stay intact. Paragraph/line/word boundary preferences, UTF-8 integrity and exact reconstruction are preserved. Forty focused intake, conversion, checklist and filename-resolution tests passed. The previously tested real paper was checked again with the new splitter; no research files were changed. Existing split corpora are not silently renamed or repartitioned.


**JSON housekeeping (2026-11-17).** User requires a json subfolder for JSON collections, with at most two JSON files left directly in a folder. Added json_files helpers for collision-checked organization, dry-run plans, existing JSON-folder reuse and prevention of json/json. Fixed-path backend files must be explicitly retained or their readers reconciled before moving; this is not a global rewrite of engine storage paths. Chat-coach packets now return next_request.response_file under 01_FRAME/json (or existing JSON), using session ID and revision; the adapter and standing personality require that path for replies. Source artifacts and state formats are unchanged. The user's external Ezekiel4617/01_FRAME folder was cleaned with authorization: all 24 loose p*/q* payload JSON files moved into its existing JSON folder; byte hashes verified. Only coaching-session.json and frame-certificate.json remain at root. Headers, documents, saved session and certificate bytes were verified unchanged. No approval was created or coaching state advanced.
