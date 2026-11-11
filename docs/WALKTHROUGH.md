# Walkthrough: your first Claim Registry quest with NotebookLM

This guide takes you from a question you care about to a finished report. Do the steps in order. Steps 1–6 happen once per corpus. Step 7 is the quest itself, which takes three hours or less and runs unattended. Steps 8 and 9 build and read the evidence.

If you want to see the harness work before you bring your own material, run `python cr.py demo` first. It runs a small synthetic corpus end to end, offline.

## What Claim Registry is, in one paragraph

You start with a question that has competing answers, the hypotheses. You gather the published sources that bear on it. The harness never lets one model read everything and tell you what it thinks. Instead it splits the work:

- **NotebookLM** holds the sources and answers one narrow, source-cited question at a time. This is the *Archivist*.
- **One agent** writes those questions. This is the *Investigator*.
- **A second agent** scores the answers against the hypotheses and tells the Investigator what to ask next. This is the *Manager*.

The Archivist never sees the hypotheses. The Investigator never sees the scores. Each answer cites (source filename, section heading), so every claim can be traced back to the page it came from.

## What you need

- Python 3.11 or newer, and Google Chrome.
- A Google account for NotebookLM. A separate account for this work is a good idea, because the driver stays signed in.
- At least one model API key, saved as a text file. Two or more from different providers is better: if one provider refuses a step or goes down, the harness moves to the next one and records that it did. DeepSeek, OpenAI, Gemini and Anthropic are recognised by file name.
- Optional: a datalab.to account for converting PDFs.

```
pip install playwright
python cr.py selftest            # about a minute; should end with OK
python cr.py doctor              # checks Python, Playwright and Chrome
```

The whole path is six commands:

```
python cr.py new     projects\MyTopic --corpus "D:\my sources" --keys "D:\my keys" --notebook <link> --notebook <link>
python cr.py frame   projects\MyTopic
python cr.py approve projects\MyTopic --by "Your Name"
python cr.py doctor  projects\MyTopic
python cr.py quest   projects\MyTopic
python cr.py run     projects\MyTopic
```

The steps below say what each one does and what you do in between.

## 1. Frame the question

Write one or two paragraphs covering:

- what you want to decide;
- the plausible answers, including the boring and adverse ones;
- what evidence would tell them apart.

That paragraph is the seed of the header in step 4. Keep the hypotheses as rivals: each should predict something the others do not.

## 2. Find the sources

Aim for the sources that could change your mind, not the most sources. On PTX, 111 sources were enough to run 143 questions.

- **Where to look:**
  - PubMed and Europe PMC, for medicine and biology. Europe PMC often has full text.
  - Google Scholar, for citation chains: who cites the key paper, and what it cites.
  - ClinicalTrials.gov and trial registries, for protocols and unpublished results.
  - Regulatory documents such as FDA labels, EMA assessment reports and court filings, where relevant.
  - Unpaywall or the authors' own pages, for legal free copies.
- **Include the adverse evidence:**
  - null trials;
  - papers that measure the mechanism and fail to find it;
  - competing explanations for the same outcome.

  A corpus that only supports one answer cannot test anything.
- **Prefer full text to abstracts.** If only the abstract is available, keep it but note it, because the answers will be thinner.
- **Name files so you can cite them:** `firstauthorYEAR.md`, for example `shirazi2024.md`. Questions name sources by exact filename, so short, stable names save a lot of trouble.

## 3. Convert to Markdown and start the project

1. Convert each PDF to Markdown with datalab.to or another converter. **Open a few converted files with tables and check that the tables survived.** Broken tables are the most common silent failure.
2. Start the project:

   ```
   python cr.py new projects\MyTopic --name "My topic" --corpus "D:\my sources" --keys "D:\my keys"
   ```

   - It copies your Markdown files into the project and hashes them. It flags likely bad conversions, such as `LOW_WORD_COUNT`, `POSSIBLE_OCR…` and `DUPLICATE`. Fix or drop anything it flags.
   - `--keys` names a folder of key files, one `.txt` per provider, for example `deepseek API key.txt`. The harness records each file's path. It never copies a key, and it never writes one to a log.
   - It writes `01_FRAME\question.md`, a short template.

3. **Write your question in `01_FRAME\question.md`:** what you want to decide, who or what it is about, the rival answers, and the evidence that would tell them apart. This is your paragraph from step 1.

## 4. Draft the index, the Archivist prompt and the header

```
python cr.py frame projects\MyTopic
```

It reads every source once and writes three things into `01_FRAME\`:

- **`index.md`**: a ranked list of the sources, one entry per file, saying what each is and what it is good for. The Investigator uses it to pick sources to name in questions. It is routing only, never evidence.
- **`archivist-custom-prompt.txt`**: the instructions NotebookLM will follow. It follows `claimreg/prompts/spec/Archivist_Prompt_Generator_v4.md`: answer only from the sources, put (filename, section heading) beside each number, and end with a synthesis and limitations.
- **`header-DRAFT.md`**: the draft quest header. It follows `claimreg/prompts/spec/Quest_Header_Generator_v2.md`.

The header is the contract for the whole quest. It sets out the axes, the hypotheses and what each predicts, the cohort, the gauge, the decisive tests, and the **query firewall**: the rules every question must follow.

Read the draft as the person responsible for the result:

- Are the hypotheses real rivals?
- Is anything you care about missing?
- Would the decisive tests actually decide anything?

Edit it until it says what you mean. Then approve it:

```
python cr.py approve projects\MyTopic --by "Your Name"
```

**No discovery starts until a person has approved the header.** `cr quest` refuses to run without it.

## 5. Set up NotebookLM: one notebook, then copies

1. Create a notebook and upload every Markdown source.
2. Open **⋮ → Configure Chat**:
   - choose **Custom** and paste the contents of `archivist-custom-prompt.txt`;
   - choose **Longer**;
   - Save.

   Longer lets your prompt alone control the length. Default or Shorter cut answers below what the prompt asks for.
3. Make copies of the notebook. Each copy is one *lane*, and lanes answer in parallel. Three to six copies give the 45 or more graded answers an hour that the method assumes. Six is the tested maximum. Copies add speed, not independent evidence.
4. **Open every copy and check Configure Chat again.** On PTX, three copies had quietly kept Default or Shorter.
5. Keep the notebooks clean:
   - never use the "Discover sources" / Fast Research box;
   - never Import its results;
   - never save answers to notes.

   These change what the Archivist "knows" in ways nobody can audit.
6. Give the harness the links (once), by adding them to `cr new` or to the first `cr quest`:

   ```
   python cr.py quest projects\MyTopic --notebook <link 1> --notebook <link 2> --notebook <link 3>
   ```

## 6. Check everything

```
python cr.py doctor projects\MyTopic
```

It checks the corpus, the header, the index, the notebook links and each model key, and it sends each model a one-word test. If a model name is no longer offered, `cr doctor --fix` picks one that is. Add `--notebooks` to resolve every notebook link with the driver's browser profile — a one-character typo in a link otherwise silently costs you a lane for the whole quest. Fix anything marked FAIL before the quest.

## 7. Run the quest

```
python cr.py quest projects\MyTopic
```

The first time, a Chrome window opens: sign in to the Google account that owns the notebooks, check that a notebook opens, and close the window. After that the quest runs by itself for up to three hours. `cr quest` first checks that every lane comes up (it refuses to start if a notebook link does not resolve) and starts the driver with a live log:

- A Chrome window opens with one tab per notebook copy. Leave it open and **unminimized** — a minimized window throttles the tabs, and the driver now launches maximized and restores a minimized window automatically. Never use a headless driver.
- The **Investigator** (a model) writes questions. Each one must pass the firewall: it names one to three exact source filenames, asks for (filename, section heading) beside each number, uses no project vocabulary, and never asks for fewer than 900 words.
- **NotebookLM** answers. Every answer is saved exactly as shown, with its query, its lane and its times.
- The **Manager** (a second model call, which the Investigator never sees) runs ACH_Eval on every six answers, commits the round, and writes a feedback packet with ready-to-send questions for the next batch.
- The harness never lets more than 12 answers wait for grading, so the Manager's feedback keeps steering the questions.

Watch `quest\<quest id>\relay-status.json` for progress. To stop early, create an empty file named `STOP` in the quest folder: the lanes finish their current answers, the Manager grades what is left, and the quest closes. Running `cr quest` again resumes an unfinished quest; committed rounds are never graded twice.

If a lane stalls, do not restart the relay: unminimize the window first, and if the tab is genuinely wedged, restart only the driver (`python -m claimreg.notebooklm.driver run "<quest>\quest.json"`) — in-flight answers are re-read from the chat. `docs\NOTEBOOKLM-QUEST.md` §5 lists every failure mode and what the harness now does about it.

When it ends, the harness writes `CLOSEOUT.md` and `SCORECARD.txt` (PASS or FAIL against the throughput standard) and imports the quest into a new run. No FRDs are made during the quest.

**What the import does:**

- **It picks one answer per question.** When a question was re-asked (A01, A02), the newest usable answer without notebook tool output is taken.
- **It keeps answers flagged for NotebookLM tool output, labelled candidates.** FRD validation then checks each quotation against the real source file, which clears or rejects it.
- **It labels the stop honestly:** operational unless the Manager directed STOP.
- **It leaves the Manager's private files out.** The run's own `assess` stage makes the final assessment.

## 8. Build the evidence and the report

```
python cr.py run projects\MyTopic
```

This runs the rest of the chain. Finished stages are skipped if you run it again, and every model answer is cached, so nothing is asked twice.

| Stage | What it does |
|---|---|
| FRDs | Splits each answer into at most four source-attributed claims |
| Validation | Checks each claim against its named source only. The quotation must be found word for word in the source file, or the claim does not go forward |
| Witnesses | States each validated finding in 60 words or fewer; a separate auditor checks it against the claim |
| Units | Breaks each hypothesis into finding-sized parts: facts that one published finding could establish |
| Matching | Two separate passes judge each witness against each part; disagreements are adjudicated and labelled |
| Coverage | Finds the smallest sets of witnesses that cover every required part of a hypothesis |
| Crux | Finds the witnesses that one hypothesis needs and a rival cannot accommodate |
| Report | Writes the report, the premise ledger and the audit browser |

## 9. Read the result

Open these, in this order, in `02_RUNS\<run>\`:

1. **`08_COVERAGE\PREMISE-LEDGER.md`**: what each hypothesis rests on, and where each part stands:
   - *established*: a finding states it;
   - *contested*: one finding establishes it and another contradicts it. This is where the sources disagree;
   - *supported if a transfer is granted*: the effect is shown, but in another species, model, tissue or dose. The ledger says exactly what you would have to grant;
   - *not addressed*: no source in the corpus speaks to it.
2. **`10_REPORTS\CRUX-REPORT.md`**: the run at a glance, the crux candidates and the coverage of each hypothesis.
3. **`10_REPORTS\report.html`**: click any witness to reach its claim, the word-for-word source quotation and the question that found it.

If a result surprises you, `python cr.py funnel projects\MyTopic` shows where the run lost material, stage by stage, and what limited it. To overrule a matching judgment, add it to `07_MATCHING\04_disagreements-and-review\human-decisions.json` and run `python cr.py run projects\MyTopic --from coverage`.

**What the result is, and is not.** It is the best reading of *this corpus* in *this run*. A covered hypothesis is one whose required parts each have a source-anchored finding behind them; it is not thereby true. An uncovered part tells you what to go and find.

## Where to read more

| Topic | File |
|---|---|
| The quest, in reference form, and the throughput scorecard | `docs/NOTEBOOKLM-QUEST.md` |
| Every `cr` command, providers and failover, the file queue, forks, publishing | `docs/USER-GUIDE.md` |
| What the offline local engine does and does not do | `docs/LOCAL-ENGINE.md` |
| Why the specification was completed the way it was | `docs/DECISIONS.md`, `docs/DECISIONS-ADDENDUM.md`, `docs/DECISIONS-2026-11-10.md` |
