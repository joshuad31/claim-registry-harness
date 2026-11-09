# Walkthrough: your first Claim Registry quest with NotebookLM

This guide takes you from a question you care about to a finished discovery quest. Do the steps in order. Steps 1–6 happen once per corpus. Steps 7–10 are the quest itself, which takes three hours or less.

If you want to see the harness work before you bring your own material, run `python cr.py demo` first. It runs a small synthetic corpus end to end, offline.

## What Claim Registry is, in one paragraph

You start with a question that has competing answers, the hypotheses. You gather the published sources that bear on it. The harness never lets one model read everything and tell you what it thinks. Instead it splits the work:

- **NotebookLM** holds the sources and answers one narrow, source-cited question at a time. This is the *Archivist*.
- **One agent** writes those questions. This is the *Investigator*.
- **A second agent** scores the answers against the hypotheses and tells the Investigator what to ask next. This is the *Manager*.

The Archivist never sees the hypotheses. The Investigator never sees the scores. Each answer cites (source filename, section heading), so every claim can be traced back to the page it came from.

## What you need

- A Google account for NotebookLM. A separate account for this work is a good idea, because the driver stays signed in.
- Python 3.11 or newer.
- Google Chrome.
- Two agent sessions, for example two Claude chats, or Claude plus Codex, Cursor or Grok. They only read and write files. No API key is needed.
- Optional: a datalab.to account for converting PDFs.

```
pip install playwright
python cr.py selftest            # about 30 seconds; should end with OK
```

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

## 3. Convert to Markdown and build the index

1. Convert each PDF to Markdown with datalab.to or another converter. **Open a few converted files with tables and check that the tables survived.** Broken tables are the most common silent failure.
2. Create a project and check the corpus:

   ```
   python cr.py init   projects\MyTopic --name "My topic" --corpus "D:\my sources" --copy-corpus
   python cr.py corpus projects\MyTopic
   ```

   `cr corpus` hashes every file and flags likely bad conversions, such as `LOW_WORD_COUNT`, `POSSIBLE_OCR…` and `DUPLICATE`. Fix or drop anything it flags.
3. **Write the index.** The index is a ranked list of the sources: one line per file saying what it is and what it is good for. The Investigator uses it to pick sources to name in questions. It is routing metadata only, never evidence. You can draft it in a chat with any capable model: give it the file list and the first page of each source. Or let the harness draft it with `python cr.py run projects\MyTopic --to index`. Save the result as `projects\MyTopic\01_FRAME\index.md`.

> **Who drafts.** `cr` commands that draft things (`--to index`, `--to archivist_prompt` and `header-draft`) use whatever provider those roles are routed to. Out of the box that is the offline local engine, which produces a usable skeleton, not model judgment. For a real draft, either route the `indexer`, `archivist_writer` and `investigator` roles to a model or to the file queue (`docs/USER-GUIDE.md` §2–3), or draft in a chat using the spec files named below.

## 4. Write and approve the quest header

The header is the contract for the whole quest. It sets out:

- the axes, the hypotheses and what each predicts;
- the cohort;
- the gauge;
- the decisive tests;
- the **query firewall**: the rules every question must follow.

It follows `claimreg/prompts/spec/Quest_Header_Generator_v2.md`.

```
python cr.py header-draft projects\MyTopic my-frame.md
```

(`my-frame.md` is your paragraph from step 1 plus the hypotheses you want tested.)

This writes `01_FRAME\header-DRAFT.md`. Read it as the person responsible for the result:

- Are the hypotheses real rivals?
- Is anything you care about missing?
- Would the decisive tests actually decide anything?

Edit the draft, then save it as `01_FRAME\header.md`. **No discovery starts until a human has approved the header.**

## 5. Generate the Archivist custom prompt

The Archivist prompt tells NotebookLM how to answer:

- only from the sources;
- with (filename, section heading) beside each number;
- with a synthesis and limitations at the end.

It follows `claimreg/prompts/spec/Archivist_Prompt_Generator_v4.md`. Draft it in a chat with that spec plus your index, or run `python cr.py run projects\MyTopic --to archivist_prompt`. It lands in `01_FRAME\archivist-custom-prompt.txt`.

The prompt must never ask for fewer than 900 words.

## 6. Set up NotebookLM: one notebook, then copies

1. Create a notebook and upload every Markdown source.
2. Open **⋮ → Configure Chat**:
   - choose **Custom** and paste the Archivist prompt;
   - choose **Longer**;
   - Save.

   Longer lets your prompt alone control the length. Default or Shorter cut answers below what the prompt asks for.
3. Make copies of the notebook. Each copy is one *lane*, and lanes answer in parallel. Six is the tested maximum. Copies add speed, not independent evidence.
4. **Open every copy and check Configure Chat again.** On PTX, three copies had quietly kept Default or Shorter.
5. Keep the notebooks clean:
   - never use the "Discover sources" / Fast Research box;
   - never Import its results;
   - never save answers to notes.

   These change what the Archivist "knows" in ways nobody can audit.

## 7. Configure and start the driver

Copy `examples\quest-driver.PTX.json` to `examples\quest-driver.MyTopic.json` and edit it:

```json
{
  "run_id": "MYTOPIC-NLM-2026-11-15",
  "notebooks": {
    "primary": "https://notebooklm.google.com/notebook/<id of the first notebook>",
    "clone-1": "https://notebooklm.google.com/notebook/<id of the first copy>"
  },
  "answers_dir": "../nlm-answers-mytopic",
  "profile_dir": "../.notebooklm-profile",
  "channel": "chrome",
  "max_backlog": 12,
  "assessed_file": "../nlm-answers-mytopic/assessed-qids.json",
  "poll_seconds": 3
}
```

Paste each notebook's address from Chrome's address bar. Paths are relative to the config file. Then:

```
nlm login examples\quest-driver.MyTopic.json   # once: sign in yourself, open a notebook, close the window
nlm run   examples\quest-driver.MyTopic.json   # leave this window open for the whole quest
```

(`nlm` is `nlm.cmd` on Windows. Elsewhere use `python -m claimreg.notebooklm.driver`.)

The driver opens its own Chrome window with one tab per notebook copy and prints `lane … ready` for each. It writes each answer straight to `answers_dir`, so there are no permission prompts and no tabs to babysit.

**Never commit `.notebooklm-profile`.** It holds your signed-in Google session. The repository's `.gitignore` already excludes it.

## 8. Start the two agents

Open two separate agent sessions. They must not share a context.

**Investigator.** Give it:

- `claimreg/notebooklm/INVESTIGATOR.md`;
- the approved header;
- the index;
- the Archivist prompt;
- `docs/NOTEBOOKLM-QUEST.md`;
- the answers folder path.

It writes questions as `Qnnnn.json` files (`{"qid", "attempt", "text"}`) into `<answers_dir>/queue/`. You can also have it write batch files and run `quest_tool.py enqueue`, as the brief describes. Every question must pass the firewall:

- it names one to three exact source filenames;
- it asks for (exact source filename, actual section heading) beside each number;
- it uses no hypothesis labels or project jargon;
- it never asks for fewer than 900 words.

**Manager.** Give it:

- `claimreg/notebooklm/MANAGER.md`, with the paths changed to your project as its template note says;
- the approved header;
- `claimreg/prompts/spec/ACH_Eval_NLM_Super.md`;
- the index, as routing metadata only.

It never touches NotebookLM or a browser. Every 5–6 new answers, it:

- runs ACH_Eval on the cumulative record, scoring each axis separately;
- writes a public feedback packet with 8–10 ready-to-send questions;
- keeps its scores private.

## 9. Run the loop

```
Investigator: write 6-12 questions   ->  queue/        ->  lanes answer (45-110 s each)
Investigator: collect answers        ->  hand 5-6 at a time to the Manager
Manager:      ACH_Eval + packet      ->  feedback-packets/Rnnn.md
Investigator: send the packet's ready questions, write the rest, repeat
```

After each packet, mark the assessed answers so the driver keeps pacing:

```
python claimreg\notebooklm\quest_tool.py assessed <assessed_file> Q0001 Q0002 …
```

The lanes produce about 250 answers an hour, but one Manager assesses about 70. The driver holds new questions while more than `max_backlog` answers are waiting, so the Manager's packets still steer the questions. Pace the quest to the Manager, not to NotebookLM.

**When answers go wrong**, check the flags in each answer file:

| Flag in the answer file | Meaning | Do this |
|---|---|---|
| `contains_tool_output: true` | NotebookLM showed its own "Tool response" blocks as if they were file text | Treat its quotes as unverified, and re-ask once as attempt A02 |
| `outcome: FAILED` | Nothing but unexecuted tool calls | Re-ask, ideally in another lane |
| `answer_names_requested_source: false` | The answer is about something else, often an earlier question | Not usable. If one lane keeps doing it, open that copy, use **⋮ → Delete chat history**, and restart the driver |

Clear chat history only when answers degrade, not after every answer.

`driver-status.json` in the answers folder shows what every lane is doing.

## 10. Stop and close out

- **Operational stop.** You decide when time is up: write a file named `STOP` into `queue/`. Each lane finishes its current answer and the driver exits.
- **Scientific stop.** Only the Manager can direct STOP, and only when the header's numerical rule and every substantive requirement hold. Never stop for time or count reasons, and never call an operational stop a scientific one.

Have the Manager write a closeout covering:

- what was assessed;
- the final position on each axis, in words;
- the open obligations;
- the strongest affirmative and adverse cases;
- what source-only validation must check first.

`projects/PTX` and the PTX closeout are the worked example.

## After the quest

FRDs are built after the quest, never during it. FRD construction and blind source-only validation (`frd_generate`, `frd_validate` and the stages after them in `cr run`) are separate downstream stages. Nothing in a quest certifies source fidelity. Answers flagged for tool output stay *candidate* until their quotations are checked against the source files.

> **Current gap.** The only importer from a recorded quest into `cr run` is still the PTX-specific `cr import-chatgpt`. A general importer for NotebookLM quest records is an open item. Until it exists, the quest's answer files and closeout are the deliverable of this stage.

## Where to read more

| Topic | File |
|---|---|
| The quest, in reference form | `docs/NOTEBOOKLM-QUEST.md` |
| Every `cr` command, providers, the file queue, forks, publishing | `docs/USER-GUIDE.md` |
| What the offline local engine does and does not do | `docs/LOCAL-ENGINE.md` |
| Why the specification was completed the way it was | `docs/DECISIONS.md`, `docs/DECISIONS-ADDENDUM.md` |
