# Coaching inside the assistant conversation

The assistant is the user interface. The harness owns the durable coaching state, the reviewed wording, and the acceptance record. Do not open a terminal interview for the user. The user does not have to supply a name, retype hypotheses, disable paste, wait through a reading timer, or answer missing-word questions.

This document is an adapter contract for the assistant, not a set of commands to hand to a novice.

## Start and resume

Run `python cr.py coach "<project>"`. `cr sign` now uses the same chat flow by default. The command reads the configured header when present and otherwise starts from `01_FRAME/header-DRAFT.md`. It checks the source map and question structure before any user-facing interview. It does not contact a model, make a paid call, or approve anything merely by starting.

The response contains `step`, `revision`, `question`, optional material to `show`, and instructions for the assistant. Ask the question in ordinary chat. Show one explanation at a time, with its assumptions and what would count for or against it. Explain technical terms when needed. Do not display the tool's JSON, internal IDs, numeric choices, revision numbers, or filesystem diagnostics to the user.

Use relevant answers the user has already given, copied faithfully. Ask only for missing information or clarification. Never invent a reply or confirmation. The ordinary questions are the person's purpose, whether they favor an explanation (an open mind is allowed), the experience behind their interest, and what they would reconsider if the evidence differs.

## Record a reply

Write a response JSON file in the project's coaching workspace or a permitted scratch directory, then run:

```text
python cr.py coach "<project>" --action reply --response-file "<response.json>"
```

A response includes the returned `session_id`, `revision`, and `text` copied from the actual user reply. For the preference step, include `choice`: the selected saved hypothesis ID or `null` for no preference. Translate a clear natural-language selection into the code; never make the user type a code.

For wording, scope, and consequence review, include `confirmed: true` only when the person's reply actually confirms the displayed material. Pasting is allowed. There are no minimum word counts. A request to open the coach is not acceptance of the research wording.

Read the command's next step after every submission. Files on disk, not the assistant's remembered place in the dialogue, determine progress. `coaching-session.json` stores the session and the user's recorded replies.

## Prepare and choose wording

When `step` is `prepare`, submit a response file containing the current session ID and revision with `--action prepare`. This prepares the existing draft for review without external model calls. The host assistant can explain it using the saved question and source map and can stage requested edits through `revise`.

For model-generated alternative frames, restatements, independent forecasts, and a reading of the limits, add `--model-review` to `prepare` and `select`. This uses the configured coach provider and can incur usage; explain external processing/cost before first use. It reuses the existing coach's model functions. Forecasts are estimates, not findings or probabilities. Failures are disclosed; they do not manufacture a number or force the user back to a terminal.

At `options`, explain the current wording and any alternatives in manageable pieces. To record the user's selection, use `--action select` with current revision, their actual reply in `text`, and the corresponding zero-based `choice`. The selected wording is still a proposal; it is not approved yet.

## Changes

Use `--action revise` with current revision, the user's actual request in `text`, and a `candidate` object containing the question and every existing hypothesis statement. This stages the change, clears old forecasts, and restarts wording/limits review. It does not write an approved header.

If assumptions, scope, or other supporting text need revision, supply `draft_file` instead: a complete proposed header plus an optional `changes` list. The harness requires the same question/hypothesis identities and unchanged other questions. To add or remove questions or hypotheses, restart a full review. Keep the person's meaning; never silently weaken a claim to improve a forecast. Explain changes as proposals before asking for confirmation.

## Approve the exact reviewed version

The flow reviews each explanation, the scope, the consequences, then asks whether the person wants to use this exact wording. Only at `step: approval` may the assistant submit `--action accept` with the current revision, actual user reply, and `confirmed: true`.

The harness saves the reviewed header and the existing frame-record formats, backs up prior files, and records that acceptance happened in chat. Completed questions survive interruption. It adds approval only when all questions have been reviewed. `cr quest` continues to enforce the existing acceptance requirement.

If the user asks for changes or declines, do not accept. Stage the requested change or leave the session pending. Do not use `cr approve`, turn off coach acceptance, synthesize typed responses, or fabricate a keyboard session to get past the review.

## Repair and recovery

If `status` is `needs_preparation`, the plain `message` explains the situation; `for_the_assistant` gives the repair task. Handle it yourself. Common cases include preparing a missing draft/map, repairing unambiguous layout, or reconciling a separate frame definition. Never discard hypotheses or delete a competing definition silently.

The harness detects source-map/header/configuration edits and stale response revisions. After an external change, use `--action restart` and review the current version. Do not replay acceptance from an older review. Reply files and session data are project artifacts; they do not become source evidence.

The old keyboard interview remains available only through an explicit `--terminal` option for existing technical users. It is not the default and must not be offered to novice users as the next step.
