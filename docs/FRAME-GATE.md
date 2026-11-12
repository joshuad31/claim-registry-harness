# The frame gate

The header is the frame of a run: the question, the rival hypotheses, and the limits on each axis. The frame decides what a run can find, in the way a formal statement decides what a proof can prove. A run scored on a frame nobody read answers a question nobody asked.

Nobody runs this method for fun. Everyone who runs it wants one hypothesis to win. The gate does not forbid that. It gives the wish one place to act, the header, and puts on record what was done there. Everything after the header (questions, quotation checks, matching, scoring) stays out of reach. Anyone who dislikes the frame can score the same evidence on a different one.

## What you do

Once per computer:

```
python cr.py signer --name "Your Name"
```

You choose a passphrase. It is stored nowhere. Keep it in your head or on paper: not in a file, and never in a chat with a model. A frame cannot be signed as you without it.

For each project:

```
python cr.py sign "path\to\project"
```

Run it yourself, in a terminal window. It refuses to run from a script, a pipe or an agent's command tool. For each axis of the header:

1. **You say what you want.** In your own words: what you want to be able to say when the run is done, what you will concede if it goes against you, and which hypothesis you want to win.
2. **You see forecasts.** A model writes alternative ways of framing the axis, from the strongest claim to the weakest. Each one, and the current draft, is forecast three times against the source index (and the validated findings of an earlier run, if there is one): how many of the 64 units your hypothesis would get. You are told which frame is best for the hypothesis you want. The target is two thirds: 43 of 64.
3. **You type the frame by hand.** The question and every hypothesis, in your own words. Paste is refused (keystrokes are timed), and so is typing back the draft's wording.
4. **The model restates it.** Correct grammar, and wording this corpus can test, with every change listed and every term the corpus cannot test named. The restated wording is forecast. If another frame is forecast higher for your hypothesis, or yours is below target, you are asked whether you are sure. You keep it or type again.
5. **You read it.** Each hypothesis as it will stand in the header, with its assumptions, what would count against it and what would count for it, then the boundary and cohort of the axis. Each has a minimum time on screen and two missing-word questions, and you type "I have read A2-H1".
6. **You accept the consequences, one at a time, by typing them.** A second model call, which has not been told what you want, reads the finished axis and says what a win would and would not let you say, the worst result you could plausibly get, who really holds the rival hypothesis (or that nobody does), what a critic will say, what the frame leaves out, and where the rest of the axis text contradicts your wording. You type "I accept 46 of 64", "I accept the worst case" and so on. Typing CHANGE stops with nothing signed.
7. **You sign the axis with your passphrase.**

Each axis is signed when you finish it, so a header with several axes can be done over several sittings. Allow 15 to 25 minutes an axis. The model calls cost roughly a dollar or two an axis at current prices.

## What you get

`01_FRAME/FRAME-CERTIFICATE.md` (and `frame-certificate.json`): what you wanted, what you typed, what it was restated to, every frame that was considered and its forecast, what a win means, the worst case, what is left out, and each acceptance you typed. The certificate is copied into every run and linked from `RUN-MAP.md`. A reader of a result can see the frame was chosen, by whom, and with what expectations.

## What is refused

`cr quest`, `cr import-quest`, and any `cr run` that uses a model check the certificate first. They refuse when

- there is no certificate, or an axis of the header is not signed;
- the header changed after signing;
- a file that shapes the result changed after signing: the source index, the Archivist prompt, `01_FRAME/match-fixtures.json`, any prompt override in `90_METHOD/prompts`, the `corpus`, `frd_assess` and `domain_modules` settings in `project.json`, or the rule files of a domain module the project uses;
- the certificate was edited, or was signed by a different signer;
- `01_FRAME/frame.json` exists (it would override the header).

There is no flag that overrides this. `cr approve` is refused as well.

If the wording of an axis changed, sign that axis again: `cr sign <project> --axis A2`. If something else changed (the index gained a source, a rule file was fixed), `cr sign <project> --resign` shows you what changed; you accept it by typing and sign again.

`cr sign <project> --check` says whether a frame is signed. `cr doctor` reports it too.

The block switches itself on the first time a frame is fully signed on a computer, because that is the proof that signing works there. Until then the same commands print a warning and go on. Runs that use no model (the offline engine, the demo, the test suite) are not gated: they spend nothing.

## What it cannot do

- It does not judge whether a frame is fair. It makes sure a person chose it knowingly, and it publishes the choice.
- A forecast is a guess from the index and earlier findings. Three calls are made and all three are shown.
- If no model is reachable, signing still works, and the certificate says which steps the model did not do.
- The gate stops shortcuts, not fraud. Someone with full control of the computer can replace the signing key or edit this program. That leaves traces (a different signer fingerprint on the certificate, a changed file in version control), and it is a deliberate act, which is the point: the easy path and the honest path are now the same path.
- The paragraphs under each hypothesis (assumptions, falsification, corroboration) and the boundary are not rewritten by the gate. You read them, and the second model call reports where they contradict your wording. If they do, type CHANGE, have them corrected, and sign again.
