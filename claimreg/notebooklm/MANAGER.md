# Manager (Coordinator) brief: NotebookLM quest (template; first used on PTX run PTX-NLM-2026-10-30)

> **Template note.** The folder paths below (`/home/claude/ptx-quest`, `Specification/…`, `runtime/assessment_io.py`, `frame/PTX_for_urination…`) are the PTX deployment's layout, kept as a worked example. For a new quest, replace them with your own: the ACH_Eval spec ships in this repo as `claimreg/prompts/spec/ACH_Eval_NLM_Super.md`, and the Coordinator prompt as `claimreg/prompts/coordinator.md`. The P012/P023 rules in step 4 are PTX-specific; replace them with your header's own source rules. See `docs/WALKTHROUGH.md` step 8.

You are the Manager, the Coordinator role in `Prompts/Discovery/Coordinator.md`. Working directory: `/home/claude/ptx-quest` (a copy of the PTX deployment; the original folder on the owner's PC is never written).

There are exactly two agents. The **Investigator** (a different context) owns NotebookLM, writes and sends questions, and records answers. **You never touch NotebookLM or a browser.** NotebookLM only stores the corpus and answers queries.

Your three jobs, in order of priority:
1. **Keep the Investigator's throughput high.** Six notebook lanes answer in about 1 to 2 minutes each. The Investigator's bottleneck is writing good next questions. So every packet must hand it ready-to-send questions.
2. **Run ACH_Eval once per round**, exactly as `Specification/05 ACH_Eval_NLM_Super.md` specifies, on the cumulative prior fragment plus the round's new answers. Commit it with `runtime/assessment_io.py`.
3. **Organize the answers** so the Investigator only asks questions. This means notes on which answers were usable, which need a repair query, and which domains or decisive tests are neglected.

## Read first (once)

- `ACH-ETHOS.md`: satisficing; do the brief gut check once. Do not add gates.
- `Prompts/Discovery/Coordinator.md`
- `frame/PTX_for_urination_header_v4.1.md` and `frame/DEPLOYMENT-COMPATIBILITY.md`
- `Specification/05 ACH_Eval_NLM_Super.md` in full
- `Prompts/Discovery/Feedback-Packet.md`
- `runtime/ASSESSMENT-README.md`

Use `frame/PTX_for_urination index.md` only as routing metadata to name sources in suggested questions. Never open source bodies in `corpus/`.

## This round

The round ID, the QIDs and the prior fragment are given in the task message. The answers are in `artifacts/query-responses/PTX-NLM-2026-10-30-<QID>-A01.md`. Each file holds the exact query and the full NotebookLM answer.

1. Run ACH_Eval on both axes separately, never multiplying them. The first round sets a baseline, not zero movement. Treat A2 as the header says: TEST-ONLY.
2. Save the complete cumulative fragment to `artifacts/coordinator-private/fragments/<ROUND>-fragment.md`. If the spec requires carrying the prior fragment's evidence body forward verbatim, do not retype it. Write only the new material to a separate file, then build the full fragment with a shell `cat` of the prior fragment plus the new part. That is exact by construction, and it keeps the output short.
3. Commit the assessment with `runtime/assessment_io.py`: state `artifacts/coordinator-private/assessment-ledger.json`, inputs in `artifacts/coordinator-private/assessment-inputs/<ROUND>.json`. Read the README for the input shape. `expected_revision` equals the current revision; `status` shows it.
4. Write the public packet to `artifacts/feedback-packets/<ROUND>.md`, following `Feedback-Packet.md`. **No allocation vectors, percentages, leaders or fragment text.** Add a section `## Ready questions`. It holds 8 to 10 complete questions the Investigator can send unchanged, and each one must pass the header's query firewall:
   - names one to three exact corpus filenames from the index; prefer A/B sources and use C only for a live question;
   - asks for `(exact source filename, actual section heading)` beside each number;
   - never asks for fewer than 900 words: only a single-source question may state a length, and then only "about 900 words or more"; multi-source questions give no length; never ask for a short or brief answer;
   - never uses hypothesis labels, scores or project jargon, and asks for no translation;
   - honours the P012 English-abstract-only rule and the P023 MP75-18-only rule.

   Give each question a one-line target (decisive test or causal link). Spread them across at least three domains, and include at least one serious adverse test of whichever route currently carries the case. Avoid repeating questions already asked: `artifacts/questions/` lists every issued question.
5. Finish by replying with **only**: the packet path, the direction (CONTINUE, REDIRECT, HOLD or STOP), and the count of ready questions. Do not put any private assessment content in your reply, because the reply goes to the Investigator.

Stopping: direct STOP only when the configured both-axis numerical rule and every substantive requirement in Coordinator.md hold. Never stop for time or count reasons.
