# Claim Registry (ACH 2.0) harness

Claim Registry is a method for testing competing answers to a question against a body of published sources, in a way that anyone can audit. This harness runs it. You bring the sources; it produces a report in which every claim traces back to a word-for-word quotation from a named source.

It is for people who can download peer-reviewed research, convert it to Markdown and upload it to NotebookLM. It implements Josh Davis's Claim Registry (ACH 2.0) specification.

## What it does

1. **NotebookLM holds your sources** and answers one narrow, source-cited question at a time. It never sees your hypotheses.
2. **An Investigator model writes the questions.** A separate **Manager model** grades the answers against your hypotheses and steers the next questions. The Investigator never sees the grades.
3. **Every answer is broken into claims, and every claim is checked against its source file.** A claim goes forward only if its quotation is found word for word in the source.
4. **Each hypothesis is broken into parts that a single published finding could establish.** The harness finds the smallest sets of findings that cover each hypothesis, the parts no source addresses, and the findings on which the sources disagree.

You get a **premise ledger** (what each hypothesis rests on and where each part stands), a **crux report**, and an **audit browser** where any finding can be followed back to its source sentence.

## Quick start

You need Python 3.11 or newer, Google Chrome, a Google account for NotebookLM, and at least one model API key saved as a text file (two from different providers is better).

```
pip install playwright
python cr.py selftest                 # about a minute, no network
python cr.py demo                     # a complete offline run of a small synthetic corpus
```

Then, for your own question:

```
python cr.py new     projects\MyTopic --corpus "D:\my sources" --keys "D:\my keys" --notebook <NotebookLM link>
   (write your question in projects\MyTopic\01_FRAME\question.md)
python cr.py frame   projects\MyTopic     # drafts the source index, the NotebookLM prompt and the quest header
   (read and edit 01_FRAME\header-DRAFT.md; paste archivist-custom-prompt.txt into NotebookLM: Configure Chat -> Custom + Longer)
python cr.py sign    projects\MyTopic     # go through the frame with the coach (docs/FRAME-GATE.md)
python cr.py doctor  projects\MyTopic     # checks everything, including each model key
python cr.py quest   projects\MyTopic     # the discovery quest: up to 3 hours, unattended
python cr.py run     projects\MyTopic     # claims, validation, matching, coverage, report
```

**`docs/WALKTHROUGH.md` explains every step**, including where to find sources and how to set up the notebook. On Windows you can type `cr` in place of `python cr.py`.

## What is in a result

In `projects\MyTopic\02_RUNS\<run>\`:

Each axis of your header gets its **own database**: a folder `AXIS-A1__<name>` inside the run that holds only that axis's questions, answers, FRDs, witnesses and reports. Open `RUN-MAP.md` in the run folder first. The files below are inside each axis folder. See `docs/AXIS-DATABASES.md`.

| File | What it tells you |
|---|---|
| `08_COVERAGE\PREMISE-LEDGER.md` | Each hypothesis, part by part: established, contested, supported only if a named transfer is granted, or not addressed by any source |
| `10_REPORTS\CRUX-REPORT.md` | The run at a glance, the crux candidates, coverage of each hypothesis, limits |
| `10_REPORTS\report.html` | Click any finding to see its claim, its word-for-word source quotation and the question that found it |
| `10_REPORTS\EVIDENCE-PACKETS.md` | Per hypothesis: the controlling findings, the strongest objections and the gaps |

`python cr.py funnel projects\MyTopic` shows where a run lost material and what limited it.

## Things worth knowing

- **Models are interchangeable, and a refusal cannot stop a run.** Each role has an ordered list of providers. If one refuses, filters, errors or times out, the next is asked, and the switch is recorded with its reason. DeepSeek, OpenAI, Gemini, Anthropic and any OpenAI-compatible endpoint work.
- **A coach in your corner.** Nobody runs this for fun: you want a hypothesis to win. `cr sign` asks why you are running this and what experience is behind your view, forecasts how each way of framing the question is likely to score, has you type the hypotheses yourself and accept the likely outcome. After the quest, and again after the findings are validated, the run scores the evidence against your hypothesis. If it is short of target the run stops and the coach tells you why, what the evidence does support, and your next move. `cr rescore` scores the same findings under a different frame for a dollar or two. See `docs/FRAME-GATE.md`.
- **Nothing is accepted on a model's word.** Quotations are checked mechanically against the source files. Matching is done twice, independently, and disagreements are labelled.
- **Mechanistic and animal evidence counts, with its assumptions shown.** When a finding shows the right effect in another species, model, tissue or dose, it can cover a part of a hypothesis only with the transfer it relies on written beside it. Such coverage is reported as `COMPLETE_WITH_ASSUMPTIONS`, never as `COMPLETE`.
- **It also runs with no key and no network.** The default offline engine (`docs/LOCAL-ENGINE.md`) finishes every stage by fixed rules. It is a floor for testing the machinery, not a substitute for a model.
- **A result is the best reading of this corpus in this run.** It does not establish that a covered hypothesis is true.

## Commands

| Command | What it does |
|---|---|
| `cr new`, `cr frame` | Start a project, draft its frame |
| `cr sign` (or `cr coach`) | Go through the frame with the coach before a quest (`--axis A2` for one axis, `--check` to see whether it is done) |
| `cr rescore` | Score a run's validated findings under the header as it reads now, or under another header; every frame tried is kept in `01_FRAME/FRAME-LADDER.md` |
| `cr doctor` | Check Python, Chrome, the corpus, the header, the notebooks and each model key (`--fix` repairs model names) |
| `cr quest` | Run the NotebookLM quest unattended, score it, and import it (`--then-run` continues into the report) |
| `cr run` | Run or resume the evidence pipeline (`--from <stage>` redoes a stage and everything after it) |
| `cr funnel`, `cr status`, `cr verify` | Diagnose a run, show stage status, re-check a run's records |
| `cr quest-score`, `cr import-quest` | Score or import a quest recorded another way |
| `cr fork`, `cr diff`, `cr publish` | Fork a run with declared changes, compare runs, write a hashed release |
| `cr demo`, `cr selftest` | The offline demonstration and the test suite |

## Where things are

| Path | What it is |
|---|---|
| `docs/WALKTHROUGH.md` | Your first investigation, step by step |
| `docs/NOTEBOOKLM-QUEST.md` | The quest in reference form: driver, relay, scorecard, failure modes |
| `docs/USER-GUIDE.md` | Every command, providers and failover, the file queue, forks, publishing |
| `docs/DECISIONS*.md` | Every place the specification was open, and what was chosen |
| `claimreg/` | The harness (standard library only; the NotebookLM driver also needs Playwright) |
| `claimreg/prompts/` | The prompt library. The specification prompts in `prompts/spec/` are used unchanged |
| `projects/` | Example runs: `DEMO` (offline), `WORKED` (coverage and crux), and the PTX runs |
| `HANDOFF.md` | For whoever maintains this code next |

The third-party source papers, the model-answer caches and browser profiles are not in this repository.
