# Running a discovery quest with NotebookLM

A quest has exactly three parts. New to this? Start with `docs/WALKTHROUGH.md`, which walks through every step below in order.

| Part | Who | Does | Never does |
|---|---|---|---|
| Archivist | NotebookLM, in 1 to 6 copies of the same notebook | Holds the corpus and answers one query at a time | Sees the header, the hypotheses or any score |
| Investigator | An agent: Claude, Codex, Cursor, Grok and so on | Writes questions and files answers | Scores hypotheses or sees the Manager's numbers |
| Manager | A second agent context | Runs ACH_Eval every 5–6 answers, writes the feedback packet and ready-to-send questions | Touches NotebookLM |

No API key is needed. NotebookLM is the only model the harness talks to during the quest. The two agents only read and write files. FRDs are made after the quest, not during it: `cr import-quest` brings the finished quest into a run, and `cr run` builds the evidence from it.

## 1. Before the quest (once per corpus)

1. **Convert sources to Markdown.** Run PDFs through datalab.to or another converter, and check that the tables survived.
2. **Upload the corpus to one notebook, then make copies.** Each copy is a lane. Six copies is the tested maximum. Copies add speed, not independent evidence.
3. **Set the custom prompt.** In Notebook configuration (⋮) → Configure Chat, choose **Custom**, paste the Archivist prompt from the Archivist Custom Prompt Generator, choose **Longer**, and Save. Longer lets the custom prompt alone control length; Shorter or Default cut answers below what the prompt asks for. Check every copy: in the PTX notebooks, three copies had kept Default or Shorter.
4. **Keep the chats clean.** Don't save answers to notes, and never use the "Discover sources" / Fast Research box or Import its results. When answers start going wrong (an answer about an earlier question, repeated wrong descriptions), use ⋮ → Delete chat history on that copy, then restart the driver so its pages reload.
5. **Write the index and the quest header.** The header must be human-approved before discovery starts. See `USER-GUIDE.md` §1.

## 2. Quick start: the local driver (recommended)

The driver opens its own Chrome window on its own profile. It runs every notebook copy as a lane and writes each answer straight to disk, so there are no permission prompts and no tabs to babysit.

```
pip install playwright
python -m claimreg.notebooklm.driver login examples\quest-driver.PTX.json   # once: sign in, open a notebook, close the window
python -m claimreg.notebooklm.driver run   examples\quest-driver.PTX.json   # leave running during the quest
```

On Windows, `nlm.cmd login …` and `nlm.cmd run …` do the same.

- **Config:** `examples/quest-driver.PTX.json` is a ready config for the six PTX notebooks. For a new corpus, copy it and change `run_id` and `notebooks`.
- **Questions in:** the Investigator writes `Qnnnn.json` files (`{"qid","attempt","text"}`) into `<answers_dir>/queue/`. The driver feeds them to free lanes.
- **Answers out:** `<answers_dir>/Qnnnn-A01.json` holds the exact query, the answer as rendered, the lane, the notebook URL, the submit and capture times, and two flags: `contains_tool_output` and `outcome`.
- **Status:** `<answers_dir>/driver-status.json` shows what every lane is doing.
- **Pacing:** the driver holds new questions while more than `max_backlog` answers (default 12) are waiting for the Manager. Mark answers assessed with `quest_tool.py assessed <assessed_file> Q0001 …`. Without an `assessed_file`, the driver runs at full speed.
- **Stop:** put a file named `STOP` in `queue/`. Lanes finish their current answer, and the driver exits.
- **Restarts:** if a tab reloads or crashes, the driver reopens it and re-reads any answer that was already generated, instead of sending the question again.

A mock-notebook test checks all of this end to end: `python tests/test_notebooklm_driver.py`.

## 3. Without the driver: the lane runner in an ordinary browser

`claimreg/notebooklm/lane-runner.js` is the same lane logic the driver injects. It can run in any signed-in Chrome where a person or a browser-extension agent opens the notebook tabs:

- A person can paste it into each tab's DevTools console.
- An agent can upload the file into a hidden file input, keep the text in the page's localStorage, and evaluate it in each tab.

Set `localStorage.crl_lanes` (notebook id → lane name) first. In this mode, saving files needs a one-time folder permission, which Chrome forgets when it restarts. That is why the driver is recommended.

## 4. The loop

```
Investigator: write 6-12 questions   ->  queue/Qnnnn.json   ->  lanes answer
Investigator: collect answers        ->  quest_tool ingest  ->  query-responses/
Manager:      every 5-6 new answers  ->  ACH_Eval, ledger   ->  feedback-packets/Rnnn.md
Investigator: read the packet's priorities and ready questions, write the next batch
```

Every question must pass the header's query firewall:

- it names one to three exact source filenames;
- it asks for (exact source filename, actual section heading) beside each number;
- it uses no hypothesis labels or project jargon;
- it never asks for fewer than 900 words. Only a single-source question may state a length, and then only "about 900 words or more". Never ask for a short or brief answer.

**Pace to the Manager, not to NotebookLM.** In the PTX test (111 sources, six copies, 2026-10-30), the lanes saved 112 answers in 27 minutes, about 250 an hour, with each answer taking 45–110 seconds. One Manager assessed about 70 an hour in 6-answer rounds. Measured from the first send, the quest finished in 1 h 28 min: 143 questions, all assessed, closed as an operational stop. Size `max_backlog` so the Manager's packets still steer the questions.

## 5. NotebookLM failure modes, and what the harness does about them

| Seen in the PTX test | What happens now |
|---|---|
| The first textarea on the page is the "Discover sources" web-search box | Only `textarea[aria-label="Query box"]` is ever typed into |
| Two tabs claimed the same question (localStorage is not consistent across tabs) | Claims go through IndexedDB transactions |
| Answers began with the collapsible "Thoughts" list | Stripped as page chrome |
| A PC restart closed the tabs | Lanes are reopened and in-flight answers re-read (`CRL_recover`) |
| Background tabs were slowed to one check a minute | The driver disables throttling; the browser runner broadcasts a tick from the visible tab |
| 10 of 115 answers contained NotebookLM's own "Tool response" blocks shown as file text. In some, the claimed title, species or length does not match the real file | Flagged `contains_tool_output`. Quotes from those blocks stay unverified until source-only validation; re-ask once as A02 |
| Two answers were nothing but unexecuted tool calls | Recorded `FAILED`, not usable; re-ask in another lane |
| One long chat kept repeating a wrong description of a source | Re-ask in a different notebook copy; the answer from the other chat was consistent with the rest |
| One Manager could not keep up with six lanes | Backlog pacing (`max_backlog`) |
