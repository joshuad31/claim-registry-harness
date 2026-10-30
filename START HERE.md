# START HERE — Claim Registry harness (final build, 2026-10-30)

This folder holds a **finished Claim Registry harness**: it takes a corpus and an approved quest header
and runs every stage of the ACH 2.0 specification through to a report, an audit browser and a hashed
release. It does that **with no API key, no network and no operator** — the default provider is a
deterministic local engine — and it also runs on a real model whenever you route one to a role.

Four runs ship with it, because they prove different things:

| Run | What it proves | Result in one line |
|---|---|---|
| `projects\PTX-LOCAL\02_RUNS\RUN-PTX-LOCAL-OFFLINE\` | the whole chain runs from scratch, offline, on the real 111-source PTX corpus | 40 questions, 160 quote-verified FRDs, 115 witnesses, 1,530 judged pairs; **no hypothesis reaches complete coverage** |
| `projects\WORKED\` | coverage sets, incompatibility approval and crux identification actually produce artifacts | 73 complete relations → 42 deletion-minimal coverage sets for A1-H2, 49 approved incompatibilities, **7 crux candidates** with T1/T2 certificates |
| `projects\DEMO\` | a new user can go from an empty folder to a report in one command | 24 questions, 96 FRDs, 77 witnesses, 4 complete relations, report written |
| `projects\PTX\02_RUNS\RUN-PTX-2026-10-29\` | the earlier queue-based PTX run is preserved, with its answer cache restored | 56 released witnesses, 1,680 judged pairs, no complete coverage |

The first three were produced entirely by this build's local engine. The fourth is the previous build's
run, kept untouched for comparison.

## Prove it in two commands

```
cd "C:\Users\joshu\Desktop\FINAL SPECIFICATION DOCUMENTS\DeepSeek_2 output"
python cr.py selftest      # 31 tests, about 30 seconds, no network
python cr.py demo          # builds a fresh project (projects\DEMO-2 if DEMO exists) and runs every stage
```

`cr selftest` includes an end-to-end offline pipeline test and a worked-example regression that fails
if coverage sets or crux candidates stop being produced. `cr demo` prints the report and browser paths
when it finishes.

## Read these, in this order

1. **`docs\LOCAL-ENGINE.md`** — what answers the calls, role by role, and exactly where its judgment
   stops. Read this before trusting or dismissing any result.
2. **The PTX offline result** — in `projects\PTX-LOCAL\02_RUNS\RUN-PTX-LOCAL-OFFLINE\10_REPORTS\`:
   - `CRUX-REPORT.md` — the run at a glance, coverage per hypothesis, assessment, limits;
   - `EVIDENCE-PACKETS.md` — per hypothesis: controlling claims, strongest objections, qualifications,
     and for every uncovered part the *nearest judged evidence, explicitly marked "not a match"*;
   - `report.html` — click any witness to reach its FRD, its verbatim source quotation and its question.
3. **The worked example** — `projects\WORKED\02_RUNS\RUN-WORKED-20261030T033909Z\08_COVERAGE\coverage.json`
   and `09_CRUX\05_candidates\crux-candidates.json`. This is what the last three modules look like when
   there *is* coverage.
4. **`docs\DECISIONS.md` and `docs\DECISIONS-ADDENDUM.md`** — every place the specification was open
   and what was chosen, including the local engine's rules and their failure modes.
5. **`docs\USER-GUIDE.md`** — how to start your own investigation, connect a model, use NotebookLM or
   an agent through the file queue, overrule a judgment, fork a variant, and publish.

## What is different from the ChatGPT, DeepSeek and Claude attempts

- **It cannot stop for lack of model answers.** The local engine answers every role in-process, so the
  requests that went unanswered in the previous build are no longer needed: the run answers its own
  and reaches a report. A model can still be routed to any role, and cached local answers are never
  presented as model answers.
- **The whole chain now runs live, not just the second half.** Discovery (Investigator → firewall →
  Archivist → Coordinator), FRD generation and blind validation ran for real in the PTX offline run:
  40 questions, 160 candidate FRDs, all 160 quote-verified against their named source files.
- **The last three modules are exercised end to end.** The previous build never produced a coverage
  set or a crux candidate in any real run. The worked example now produces 42 deletion-minimal coverage
  sets, 49 approved incompatibilities and 7 crux candidates with T1/T2 certificates — and a regression
  test fails if that stops happening.
- **The report shows the nearest evidence when nothing matches.** An uncovered required part no longer
  says "nothing in the registry addresses it"; it lists the closest judged witnesses, their word
  overlap and their relation, marked *not a match*, so you can see what the matcher declined to infer
  and overrule it in `human-decisions.json`.
- **The defaults are safe.** Local provider by default, language layer off, no API key required, no
  network calls anywhere in the default path.

## How to run your own investigation

```
python cr.py init projects\MyTopic --name "My topic" --corpus "D:\my sources" --copy-corpus
# put the human-approved header at projects\MyTopic\01_FRAME\header.md
python cr.py run projects\MyTopic
```

With no routing in `project.json` it uses the local engine and always finishes. To use a model for
some roles, add to `project.json`:

```json
{
  "roles": {"matcher_a": "anthropic", "matcher_b": "anthropic"},
  "providers": {"anthropic": {"model": "claude-opus-5-5", "api_key_env": "ANTHROPIC_API_KEY"}},
  "cache_fallback_providers": ["local"]
}
```

Then run the same command. Only the roles you moved are asked again.

## Honest limits

- **The PTX offline run reaches no complete coverage, and that is a real result, not a bug being
  hidden.** The matcher is lexical. Hypothesis clauses ("the materially supported rationale") and
  source findings ("flow rose by 1.2 mL/s") share too little wording, and the engine declines to
  infer what it cannot match. The report says so, and lists the nearest evidence for every uncovered
  part. A model matcher, or your own overrides, can do better.
- **The quest stopped at its operational ceiling** in the PTX offline run (8 rounds, 40 questions,
  `OPERATIONAL_LIMIT`). That is not a scientific completion finding, and the run record says so.
  `quest.max_rounds` and `quest.round_size` are configuration.
- **The final assessment is bookkeeping.** The local assessor counts witnesses that share terminology
  with each hypothesis. The artifact says it is not ACH_Eval judgment.
- **Coverage sets in the worked example are inflated by duplicate witnesses.** The same source
  sentence can arrive through several questions; retention only archives duplicates when the FRD
  database exceeds its budget. The sets are deletion-minimal, but there are many equivalent ones.
- **The local engine is not a claim about what a model would conclude.** It is a floor that guarantees
  a finished run, with every judgment labelled, traceable and overrulable.
- **The demo and worked corpora are synthetic.** Every file says so at the top. They must never be
  cited as evidence.

## Folder map

| Path | What it is |
|---|---|
| `claimreg\` | The harness (Python 3.11+, standard library only) |
| `claimreg\llm\local.py` | The local engine: one handler per role, with its rules and traces |
| `claimreg\prompts\` | The prompt library; your specification prompts are used verbatim from `prompts\spec\` |
| `cr.py`, `cr.cmd` | The command line (`selftest`, `demo`, `run`, `verify`, `fork`, `publish`, `queue`) |
| `docs\` | User guide, local-engine guide, decisions (both builds), queue operator instructions |
| `tests\` | 31 tests: solver vs brute force, header parsing, mechanical gates, mock pipeline, offline pipeline, worked example |
| `examples\demo\` | The synthetic realistic corpus `cr demo` copies |
| `examples\worked\` | The engineered corpus behind the coverage/crux regression |
| `projects\PTX-LOCAL\` | The offline demonstration on the real PTX corpus (run records; the papers themselves are not committed) |
| `projects\WORKED\` | The worked coverage/crux example |
| `projects\DEMO\` | The one-command demo |
| `projects\PTX\` | The previous build's queue-based run |

Not committed, by design: the third-party source corpus under `01_CORPUS\source-files\`, the
model-answer caches, the hashed releases, and the previous build's archive and session transcript. See
`README.md` for what that means for `cr verify`.

The ChatGPT, DeepSeek and Claude attempt folders from the original working directory are not part of
this repository; this repository is the harness and its runs only.
