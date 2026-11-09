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

- **`python cr.py selftest`:** 56 tests pass, plus 1 browser test that is skipped in selftest. That test is `python tests/test_notebooklm_driver.py`: an end-to-end driver run against a mock notebook, about 60 s, which passes.
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

1. **Prove grading speed.** Run one timed PTX quest with a Manager model that can grade this material, and score it with `cr quest-score`. **First test a single R001 round on the 11-09 answers (Q0001–Q0006)** before starting a timed quest.
2. **Restart the driver from the current code.** The 11-09 fixes (off-target detection under truncated filenames in `lane-runner.js`; pre-go-ahead records excluded from the scorecard; the driver's `quest-clock.json`) only take effect after copying `claimreg/notebooklm/` from the repo into `Claude output\claimreg\notebooklm\` (or running from the clone after `nlm login` there) and restarting `nlm run`.
3. **A small Investigator↔Manager sync tool.** On 11-09 the Investigator did these by hand:
   - staging driver answers into the Manager workspace as Markdown;
   - parsing a packet's `## Ready questions` into queue files;
   - syncing `assessed-qids.json` from the ledger.

   A `quest_tool.py` subcommand for each would remove the remaining manual glue.
4. **FRD and matching quality.** The local engine is a lexical floor. Its validator accepts ≥ 25% content overlap (349 of 473 validations on 10-30 were PARTLY RIGHT), and it never reaches complete coverage. For a result anyone relies on, route `frd_generator`, `frd_validator` and the matching roles to a model or to the file queue (`docs/USER-GUIDE.md` §2–3).
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
- **Open item 3 is done.** `quest_tool.py` now has `stage` (driver answer JSON → Manager Markdown answers), `packet` (a packet's `## Ready questions` → queue files, with mechanical firewall warnings) and `sync` (assessment ledger → `assessed-qids.json`, stamping each round's `committed_at`). 13 new tests in `tests/test_quest_tool.py`; `cr selftest` is 56 tests (57 with the browser test), all passing. `docs/NOTEBOOKLM-QUEST.md` §4 and `docs/WALKTHROUGH.md` §9 document the commands.
- **New learning — Manager context lifetime.** One Manager context degraded after about 27 rounds (it completed R027, then failed before replying). A fresh Manager context was spawned; it read `private/state.md` and graded R028–R029 and wrote the closeout. Plan on recycling the Manager context every ~20 rounds for long quests; the compact state file is what makes the handover safe.
- **Evidence run.** `cr import-quest` imported 156 questions (154 usable; closeout's repair Q0033-A02 selected; stop labelled OPERATIONAL) and `cr run` completed: 605 candidate FRDs, 424 validated/retained, 327 witnesses, crux report and HTML audit browser written; `cr verify` ok. The local engine still reaches **no complete coverage and no crux candidates** — the quality limit is unchanged and is now the top open item.
- **What is left, in priority order:**
  1. Route `frd_generator`, `frd_validator` and the matching roles to a real model (file queue or API) on this 156-answer quest; the local-engine floor is now the only thing between the harness and a result someone can rely on.
  2. Repo metadata: the GitHub description still says 31 tests / 19 stages; update it (56 tests) on the repo page.
  3. The six NotebookLM notebook IDs are public in `examples/quest-driver.PTX.json` and the older committed run records — IDs, not credentials, but decide whether to scrub them before promoting the repo.
  4. Optional: promote the Lead's ad-hoc `round.py` loop into a `nlm cycle` command and add a Manager checkpoint/restart helper.
  5. Teaching: unchanged.
