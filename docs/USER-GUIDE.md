# Claim Registry harness — user guide

This harness runs the ACH 2.0 chain end to end.

| Phase | What happens |
|---|---|
| Start | A corpus and an approved quest header |
| Discovery | A firewalled Coordinator / Investigator / Archivist quest |
| FRDs | Candidates (at most 4 per response), blind validation with a mechanical quotation check, retention |
| Witnesses | Question-guided witnesses (60 words) with an independent fidelity audit |
| Language | Optional language tools |
| Matching | Two-pass matching with adjudication |
| Coverage | Deletion-minimal coverage sets |
| Crux | Frozen rival theories with T1/T2 certificates |
| Results | A final ACH_Eval assessment, a crux report under 4,000 words, evidence packets, an HTML audit browser, and hashed releases and forks |

It is plain Python 3.11 or newer with **no third-party packages**. On Windows, use `cr.cmd` in place of
`python cr.py`.

```
python cr.py --help
python cr.py selftest            # 31 tests, about half a minute, no network and no model calls
python cr.py demo                # a complete run of a bundled synthetic corpus, offline
```

---

## 1. Start a new investigation

```
python cr.py init  projects\MyTopic --name "My topic" --corpus "D:\my sources" --copy-corpus ^
                   --header my-header.md --index my-index.md --archivist my-archivist-prompt.txt
python cr.py corpus projects\MyTopic        # hashes every source, writes a manifest, flags odd files
python cr.py run    projects\MyTopic        # runs every stage; resumable; safe to re-run
```

- **The header is required.** It must be the human-approved quest header, built from the Quest Header
  Generator v2 template: axes, hypotheses with their four sections, cohort, gauge and decisive tests.
  `cr header-draft` can draft one from a short frame file, but a draft stays a draft until you
  approve it.
- **The index and the Archivist prompt are optional.** When they are missing, the harness drafts
  them with your generator prompts.
- **Sources are Markdown or text files.** Convert PDFs first. The corpus stage flags files that look
  like failed conversions (`LOW_WORD_COUNT`, `POSSIBLE_OCR…`, `DUPLICATE`).

`cr run` stops cleanly when it needs something:

- queued model answers (status `waiting`);
- budget (status `budget`);
- a fix (status `error`, with the traceback in `00_RUN-CONTROL/stage-state.json`).

Fix the cause and run the same command again. Finished stages are skipped, and every model answer is
cached by the exact prompt, so nothing is asked twice.

Useful flags:

| Flag | Effect |
|---|---|
| `--to frd_validate` | Stop after a stage |
| `--from coverage` | Redo that stage and every later one (imported stages are left as they are) |
| `--only report` | Run only the listed stages |
| `--force report` | Rerun a finished stage |
| `--run RUN-…` | Choose a run (the default is the current one) |

Stages, in order: `corpus, index, archivist_prompt, frame, units, quest, frd_generate, frd_validate,
frd_retain, language, witnesses, transcode, qualify, match, joint, coverage, crux, assess, report`.

## 2. Choose who answers the model calls

Every model-facing role can go to its own provider. There are 19 roles, listed in
`claimreg/config.py`. Set the routing in `project.json`:

```json
{
  "default_provider": "openai",
  "roles": { "archivist": "queue" },
  "providers": {
    "openai": { "model": "gpt-5.5", "api_key_env": "OPENAI_API_KEY" },
    "anthropic": { "model": "claude-opus-5-5", "api_key_file": "C:\\keys\\anthropic.txt" }
  },
  "budget": { "max_calls": 3000, "max_usd": 100, "concurrency": 4 }
}
```

### Provider types

- `openai`: any OpenAI-compatible API. DeepSeek works with `base_url` `https://api.deepseek.com/v1`,
  and local servers work too.
- `anthropic`: the Messages API.
- `local`: **the default**. A deterministic, offline, rules-based analyst that answers every role
  from the supplied text. It needs no key, network or queue, so `cr run` always reaches a report.
  It is a lexical engine, not a language model; see `docs/LOCAL-ENGINE.md` for exactly what it does
  and does not do, and route a real model to any role when you want model judgment.
- `queue`: writes requests to files and waits for answers (see §3).
- `mock`: deterministic, for tests (answers are meaningless by design).
- `replay`: answers only from the cache. Use it to re-run a finished run without spending anything.

A new project with no `project.json` routing runs on `local`. To use a model instead:

```json
{"default_provider": "openai"}
```

### Switching provider partway through a run

Every cached answer is keyed by the exact prompt and by the provider and model that gave it. Suppose
you move a role to another provider, for example from the queue to OpenAI. To keep the answers you
already have, add this to `project.json`:

```json
"cache_fallback_providers": ["queue"]
```

Only requests with no stored answer go to the new provider. Each reused answer keeps its original
provider and model in the records.

### API keys

API keys are read at call time from the named environment variable or key file. They are never
written to any project file, log or release. Prices in the provider block are used only for the
budget estimate.

## 3. Answering model calls through the file queue (NotebookLM, a chat window, or an agent)

Use `"default_provider": "queue"`, or route single roles to it. A common choice is to route the
`archivist` role to the queue so your NotebookLM notebook answers the Archivist questions.

1. `cr run` stops with status `waiting` and writes batch files to `queue\batches\`. Each batch has a
   `.json` and a `.md`, grouped by role. One batch holds one kind of task.
2. Answer every request in a batch. Each request has a SYSTEM part and a USER part. Answer it exactly
   as a model given only that text would.
3. Save the answers next to the batch, in either form:
   - as `BATCH-0007-matcher_a.response.json`: `{"<key>": "<answer>", …}`. An answer may be a JSON
     object.
   - as `BATCH-0007-matcher_a.response.md`, with blocks headed `=== RESPONSE <key> ===`.
4. Run `cr queue import <project> --operator-model "<who answered>"`, then `cr run <project>` again.

If a request cannot be answered, mark it with
`cr queue skip <project> --key <key> --reason "…"`. The harness records the call as failed and does
not invent an answer.

`cr queue status` shows what is waiting. `cr queue export --size 12 --role matcher_a` re-packs pending
requests. To set batch sizes per role:

```json
"queue_batch_size": {"default": 10, "matcher_a": 12}
```

Rules for whoever answers are in `docs/AGENT-OPERATOR.md`. The most important rule: the witness
constructor and the witness auditor, and matching pass A and pass B, must be answered in **different**
contexts.

## 4. Reading the results

Everything is inside `02_RUNS\<run>\`. Each stage folder has a README.md that explains:

- what the stage takes and what it produces;
- how to check it;
- what it does **not** establish.

| Open first | What it is |
|---|---|
| `RUN-STATUS.md` | Every stage, its status and its headline numbers |
| `10_REPORTS\CRUX-REPORT.md` | The analyst report: crux candidates with certificates, coverage per hypothesis, diagnostic witnesses, the final assessment, compression metrics and limitations |
| `10_REPORTS\EVIDENCE-PACKETS.md` | Per hypothesis: controlling claims, strongest objections, material qualifications and gaps, each tied to a witness and its source file |
| `10_REPORTS\report.html` | The audit browser. Click a witness to see its FRD, the verbatim source quotation, the question that produced it and the Archivist's answer |
| `RUN-MAP.md` | Where every artifact lives |

## 5. Reviewing and overruling

| To change | Edit | Then |
|---|---|---|
| A witness–unit relation | `07_MATCHING\04_disagreements-and-review\human-decisions.json` (template next to it; read `review-packet.md` first) | `cr run <project> --from coverage` |
| A witness–witness incompatibility | `07_MATCHING\04_disagreements-and-review\human-incompatibilities.json` | `cr run <project> --from coverage` |
| A coverage unit | Edit `07_MATCHING\01_hypothesis-units\units.json`, or fork with a changed `units.` setting | `cr run <project> --from match` |

Human decisions are labelled `HUMAN` everywhere, and the model's judgment is kept beside them.

## 6. Variants and forks

```
python cr.py fork projects\PTX --from RUN-PTX-2026-10-29 --name W80 ^
       --set witness.raw_ceiling=80 --set witness.exception_ceiling=100 --set witness.transcoded_ceiling=100 ^
       --note "measure the 60-word ceiling against 80/100"
python cr.py run  projects\PTX                      # runs the fork (forks become the current run)
python cr.py diff projects\PTX RUN-PTX-2026-10-29 <fork id>
```

A fork copies the parent run and records the declared changes in `FORK-RECORD.json`. It reruns only
the stages those changes affect. Some useful variants:

| Variant | Settings |
|---|---|
| Witness ceilings | `witness.raw_ceiling`, `witness.exception_ceiling` |
| Your language tools | `language.mode=labels` (with `language.dictionary_file` to reuse a dictionary) |
| No adjudication: disagreements become ABSTAIN | `matching.dispute_policy=abstain` |
| Wider matching | `matching.shortlist_k=45` |
| Witnesses from the best question in their cluster | `witness.cluster_best=true` |
| When one matching pass was never answered: use the other pass's judgment, labelled | `matching.one_pass_policy=accept` (the default is `abstain`) |
| Synonyms for the matching shortlist only | `matching.synonyms` in project.json, e.g. `[["PTX", "pentoxifylline"]]` |

## 7. Publishing and checking

```
python cr.py verify  projects\PTX       # re-checks quotations, ceilings, set minimality, crux consistency, hashes
python cr.py publish projects\PTX       # 04_RELEASES\RELEASE-…: the run, every model answer used, a hash manifest
```

`verify` makes no model calls. It recomputes completeness and deletion-minimality for every set from
the saved relations. If a run's source corpus is not present (a published clone, for example), its
quotations are reported as unverifiable with a warning instead of being called mismatches.

## 8. What a run costs

For the PTX corpus (111 sources, 4.9 MB, 73 retained FRDs, 6 hypotheses), the stages from witnesses
onward make roughly:

- 150–200 witness calls;
- 44 qualification calls;
- 150–250 matching calls;
- a few dozen adjudication, joint, incompatibility and completion calls;
- one assessment call and one summary call.

A discovery quest adds:

- one Investigator call per round;
- one Archivist call per question;
- one Coordinator call per round;
- one FRD generation call per answer;
- about one validation call per FRD.

The budget block stops the run before it exceeds `max_calls` or `max_usd`.

The **local engine costs nothing** and makes no network calls, so the default configuration has no
budget exposure at all. The counts above matter only when you route roles to a paid model.

## 9. Troubleshooting

| Symptom | What to do |
|---|---|
| A stage says `error` | `cr status <project>` shows the message. The full traceback is in `00_RUN-CONTROL\stage-state.json`. Fix the cause and run again. |
| A queued answer was rejected | `queue\import-log.json` says why. Usually it is invalid JSON. Fix the response file and import again. |
| You want a fresh answer to one request | Delete its cache file: `cache\llm\<first two characters>\<key>.json` (the key is in `00_RUN-CONTROL\model-and-human-decisions\llm-calls.jsonl`). For a queue answer, also delete `queue\done\<key>.txt`. Then redo the stage with `--from <stage>`. |
| A stage says `partial` | Some model calls failed (network, rate limit). They were not cached, so `cr run` asks them again. |
| A stage says `error` and mentions a skipped request | That stage cannot go on without that answer. Delete the request's `queue\done\<key>.skip.json` to have it asked again. |
| Windows shows strange characters | The harness writes UTF-8. JSON files saved by Notepad or PowerShell with a byte-order mark are read correctly. A source file that is not UTF-8 is read as Windows-1252 and flagged `NOT_UTF8_DECODED_AS_CP1252` by `cr corpus`. |
| You changed a prompt | Prompts in `90_METHOD\prompts\` of the project override the built-in ones. Changing a prompt changes its cache key, so the affected calls are asked again. |
