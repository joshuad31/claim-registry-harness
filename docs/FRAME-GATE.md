# The coach: framing, checkpoints and re-scoring

Nobody runs this method for fun. You want a hypothesis to win, you are running in good faith, and you may know things first-hand that the published record does not show. The harness is built to keep you in the fight: it tells you what the evidence does and does not say, and when your hypothesis comes in low it shows you the next move.

A score measures the fit between a claim and the evidence. The same corpus can support a modest claim strongly and a strong claim weakly. So the first lever is the claim itself, and the claim lives in the header.

There are three points where the coach works with you.

## 1. Before the quest: review the wording in chat

Your assistant runs `cr coach <project>` behind the scenes and continues the conversation with you. `cr sign` uses the same chat flow by default. You do not need a terminal, a name prompt, or any file editing. For each research question:

1. **Discuss the purpose.** What you want the research to help you understand or do, the experience behind your interest, and what you would reconsider. You may favor an explanation or keep an open mind. The assistant uses relevant answers you already gave.
2. **Consider wording choices.** Keep your current wording or discuss a change. Optional model-assisted preparation can propose clearer wording, stronger/weaker alternatives, and three independent forecasts per candidate. This can incur model usage. A forecast is advisory, never a research result or a probability of being right; unavailable forecasts are labeled as such.
3. **Review each explanation.** See the exact statement, assumptions, and what evidence would count for and against it. You can keep the wording or request changes. There is no forced retyping, paste restriction, timed reading, or missing-word quiz.
4. **Review the scope and consequences.** Who and what the research covers, what a favorable result would support, what it would not, and the possibility of an inconclusive or unfavorable result.
5. **Choose whether to proceed.** A normal reply in the conversation can approve the exact wording you reviewed. A request merely to open the coach does not approve the wording. Changes return to review.

The point of accepting is that you understand what the comparison means and its limitations before the run. It is not a security measure. The harness saves your actual replies in its coaching session and writes the existing frame record (`01_FRAME/FRAME-CERTIFICATE.md`) when you approve.

Missing drafts and formatting problems are handled by the assistant. A saved draft is used automatically when no finalized header exists. If the question or source map changes during review, the assistant refreshes the review rather than approving an old version. The previous keyboard interview is retained only as an explicit `--terminal` compatibility option.

A quest does not start until every research question has been reviewed. Progress is saved between replies, so you can stop and return. The assistant adapter and response-file contract are documented in [CHAT-COACH.md](CHAT-COACH.md). The existing configurable acceptance requirement is unchanged.

## 2. After the quest: checkpoint 1

Before any money is spent on extracting and validating findings, the run scores the notebook's answers against your hypothesis, once. This reading is early and provisional.

If your hypothesis is below target, the run stops and writes `COACH-CHECKPOINT-1.md` in the run folder.

## 3. After the findings are validated: checkpoint 2

The run scores the validated findings three times, whatever the first score is, and takes the mean, because one scoring moves by several units on its own (measured: 3 to 5 units of a 64-unit gauge for one scoring, 2 to 3 for a mean of three). If the mean is within 3 units of target, the coach says it is too close to call and does not stop you. Every ladder entry names the model that scored it; scores from different models are not comparable.

This is the findings-level score. The final score is made later, from the witnesses, and can differ by several units: on the first run where both exist, the findings-level scorings were 36 and 40 and the final score 42. The ladder shows both once a run is finished.

If the mean is below target, the run stops and writes `COACH-CHECKPOINT-2.md`.

## What a checkpoint tells you

- **Where you stand:** the score, each scoring, and your target.
- **Why it came in low:** which part of your claim the evidence did not cover.
- **What the evidence does show for you.**
- **How your own experience fits,** for example why people like you may differ from the people studied.
- **Openings:** weaker claims this evidence is more likely to support, each against a rival someone really holds, with what a win would let you say and what the claim gives up.
- **Questions to put to the corpus next** that nobody has asked yet.

And your three moves:

- **Take an opening.** `cr coach <project> --axis A2 --action restart`, review the new wording in chat, then `cr rescore <project> --run <RUN>` (add `--answers` at checkpoint 1).
- **Ask more.** Put the suggested questions to the corpus and run again.
- **Go on as you are.** `cr run <project> --run <RUN> --continue`. A result below target is still a result.

## Re-scoring and the ladder

```
python cr.py rescore "path\to\project" --run RUN-ID [--header other-header.md] [--axis A2]
```

The corpus, the index, the questions, the answers and the validated findings are the expensive part, and they are built once. `cr rescore` scores those same findings under the header as it reads now, or under another header file, three times. Nothing in the run changes. It costs roughly a dollar or two. It uses the gauge of the header it scores.

When the claim is not the one the run's questions were written for, `cr rescore` also writes `01_FRAME/QUESTION-CHECK-<AXIS>.md`: what the new claim needs from the corpus, whether anyone asked, and the questions still to ask. It is advice; nothing waits on it.

Every scoring, by a checkpoint, by `cr rescore` or by the final assessment, is added to `01_FRAME/FRAME-LADDER.md`; nothing is replaced. Scores can be compared only within one run and one kind of evidence. The ladder is the result of an investigation: the strongest claim this evidence supports, shown beside the stronger claims it does not. For example: "lowers TSH in refractory patients: 34. Patients should be offered the option: 42."

A re-score is an evidence-level score on the validated findings. To carry a new frame through witnesses and the final report, fork the run (`cr fork`) and run it.

## Settings (`project.json`)

```
"coach": {
  "enabled": true,              // the two checkpoints
  "target_share": 0.6667,       // where your hypothesis should stand
  "times": 3,                   // scorings averaged at checkpoint 2 and by cr rescore
  "require_acceptance": true,   // a quest waits for cr sign
  "preferred": {"A2": "A2-H1"}  // the hypothesis you want, if there has been no cr sign session
}
```

The checkpoints only work on an axis when the coach knows which hypothesis you want: from the `cr sign` session, or from `preferred`.

## What is not in the harness

- **No topic-specific rules.** A rule set for one topic shapes the score from outside the header. A rule you believe in goes in the axis's governing boundary, where everyone can read it.
- **No signatures, passphrases or tamper checks.** The earlier version had them. They were removed on 2026-11-14: the system has to work before anyone knows what securing it should mean, and anyone who wanted a biased result would get it more easily upstream, in the source conversions, than in the frame.
