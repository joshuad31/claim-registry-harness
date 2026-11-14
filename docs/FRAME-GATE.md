# The coach: framing, checkpoints and re-scoring

Nobody runs this method for fun. You want a hypothesis to win, you are running in good faith, and you may know things first-hand that the published record does not show. The harness is built to keep you in the fight: it tells you what the evidence does and does not say, and when your hypothesis comes in low it shows you the next move.

A score measures the fit between a claim and the evidence. The same corpus can support a modest claim strongly and a strong claim weakly. So the first lever is the claim itself, and the claim lives in the header.

There are three points where the coach works with you.

## 1. Before the quest: `cr sign`

```
python cr.py sign "path\to\project"
```

Run it yourself, in a terminal window (`cr coach` is the same command). For each axis of the header:

1. **The coach asks about you.** Why you are running this. What your goal is and how the analysis can help. Which hypothesis you want to win, what experience shaped that view, what you want to be able to say, and what you would concede.
2. **You see forecasts.** The coach writes alternative ways of framing the axis, from the strongest claim to the weakest, each against a rival that someone really holds. Each one, and the current draft, is forecast three times: how many of the 64 units your hypothesis would get. The target is two thirds, 43 of 64. These are units of evidence, not a probability that you are right.
3. **You type the frame by hand.** The question and every hypothesis, in your own words. Paste is not taken.
4. **The coach restates it** so that this corpus can test it, lists every change, and forecasts it. If another frame is forecast higher for your hypothesis, it asks whether you are sure.
5. **You read it.** Each hypothesis as it will stand, with what would count for and against it.
6. **You accept the consequences by typing them:** the forecast, the worst likely result, what a win does and does not let you say, who holds the rival, and what the frame leaves out.

The point of accepting is that you know the likely outcome before the run. A hard result is then not a shock. It is not a security measure, and the record (`01_FRAME/FRAME-CERTIFICATE.md`) is a plain file.

A quest does not start until every axis of the header has been through this. Each axis is saved when you finish it, so you can do them in separate sittings. Allow 15 to 25 minutes an axis. To switch the requirement off, set `"coach": {"require_acceptance": false}` in `project.json`.

## 2. After the quest: checkpoint 1

Before any money is spent on extracting and validating findings, the run scores the notebook's answers against your hypothesis, once. This reading is early and provisional.

If your hypothesis is below target, the run stops and writes `COACH-CHECKPOINT-1.md` in the run folder.

## 3. After the findings are validated: checkpoint 2

The run scores the validated findings. If the first scoring is below target it scores twice more and takes the mean, because one scoring moves by several units on its own. If the mean is below target but one scoring reached it, the coach says it is too close to call and does not stop you.

If the mean is below target, the run stops and writes `COACH-CHECKPOINT-2.md`.

## What a checkpoint tells you

- **Where you stand:** the score, each scoring, and your target.
- **Why it came in low:** which part of your claim the evidence did not cover.
- **What the evidence does show for you.**
- **How your own experience fits,** for example why people like you may differ from the people studied.
- **Openings:** weaker claims this evidence is more likely to support, each against a rival someone really holds, with what a win would let you say and what the claim gives up.
- **Questions to put to the corpus next** that nobody has asked yet.

And your three moves:

- **Take an opening.** `cr sign <project> --axis A2`, type the new claim, then `cr rescore <project> --run <RUN>` (add `--answers` at checkpoint 1).
- **Ask more.** Put the suggested questions to the corpus and run again.
- **Go on as you are.** `cr run <project> --run <RUN> --continue`. A result below target is still a result.

## Re-scoring and the ladder

```
python cr.py rescore "path\to\project" --run RUN-ID [--header other-header.md] [--axis A2]
```

The corpus, the index, the questions, the answers and the validated findings are the expensive part, and they are built once. `cr rescore` scores those same findings under the header as it reads now, or under another header file, three times. Nothing in the run changes. It costs roughly a dollar or two.

Every frame scored, by a checkpoint or by `cr rescore`, is kept in `01_FRAME/FRAME-LADDER.md`. The ladder is the result of an investigation: the strongest claim this evidence supports, shown beside the stronger claims it does not. For example: "lowers TSH in refractory patients: 34. Patients should be offered the option: 42."

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
