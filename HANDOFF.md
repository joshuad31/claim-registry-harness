# Handoff: Claim Registry harness (for the next model)

Written 2026-11-09 by Claude (Opus 5.5) for Josh Davis, who is handing this project to another model. Read this file first, then `START HERE.md`, `docs/WALKTHROUGH.md` and `docs/NOTEBOOKLM-QUEST.md`.

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
