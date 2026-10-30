# Claim Registry (ACH 2.0) harness

A working implementation of Josh Davis's Claim Registry specification: a custom agent harness that
distills a document corpus into source-anchored evidence and tests competing hypotheses against it.

```
corpus + approved quest header
  -> firewalled discovery quest (Coordinator / Investigator / Archivist, ACH_Eval, gauge-keyed stop rule)
  -> FRDs (<= 4 per answer) -> blind single-source validation with a mechanical verbatim-quote check
  -> retention -> question-guided 60-word witnesses + independent fidelity audit
  -> optional language tools (Mr. Dictionary, Mr. Canonicalizer, Mr. Transcoder)
  -> two-pass semantic matching + adjudication -> deletion-minimal coverage sets
  -> frozen rival theories, T1/T2 portability tests, crux candidates
  -> ACH_Eval assessment, crux report (< 4,000 words), evidence packets, HTML audit browser
  -> hashed releases and declared forks
```

**It runs with no key, no network and no operator.** The default provider is a deterministic local
engine (`local-rules-v1.8`) that answers every role from the supplied text; a real model can be routed
to any role at any time. See `docs/LOCAL-ENGINE.md` for exactly what the local engine does and does
not do.

* **Start here:** `START HERE.md`
* **How to use it:** `docs/USER-GUIDE.md`
* **What the local engine is:** `docs/LOCAL-ENGINE.md`
* **Decisions where the specification was open:** `docs/DECISIONS.md` (first build) and
  `docs/DECISIONS-ADDENDUM.md` (this build)
* **Answering model calls by hand, in NotebookLM, or with an agent:** `docs/AGENT-OPERATOR.md`
* **The offline PTX demonstration:** `projects/PTX-LOCAL/02_RUNS/RUN-PTX-LOCAL-OFFLINE/`
* **The worked coverage/crux example:** `projects/WORKED/`

Python 3.11 or newer, standard library only.

```
python cr.py selftest     # 31 tests, about half a minute, no network
python cr.py demo         # a complete run of a bundled synthetic corpus, from an empty folder
```

## What is in this repository

- the harness, its prompt library, 31 tests, and the documentation;
- two synthetic example corpora (`examples/demo`, `examples/worked`);
- four completed runs with their reports and machine records:
  `projects/DEMO`, `projects/WORKED`, `projects/PTX` (the earlier queue-based run) and
  `projects/PTX-LOCAL` (the fully offline run on the 111-source PTX corpus).

**Not committed, by design:**

- `projects/*/01_CORPUS/source-files/` — the third-party published papers the PTX corpus was built
  from. Their manifests, hashes and provenance records are committed; the papers are not, because
  redistributing them is not mine to do. Without them, `cr verify` on a PTX run checks everything
  except the quotations, and says so in a `warnings` entry instead of failing.
- `projects/*/cache/` and `projects/*/04_RELEASES/` — model-answer caches (exact prompts and answers,
  including source excerpts) and duplicate hashed releases.
- the previous build's 9 MB model-call archive and its session transcript.

## License

No license has been granted. The harness, the specification documents and the PTX research header are
Josh Davis's work. The third-party papers referenced by the committed manifests are not included and
remain under their own licenses.
