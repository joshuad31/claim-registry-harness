# Operating the file queue with an AI agent (or by hand)

When a role is routed to the `queue` provider, the harness writes each model request to
`<project>/queue/pending/` and packs them into batch files in `<project>/queue/batches/`:

* `BATCH-0007-matcher_a.json` — machine-readable: `{"requests": [{"key", "role", "expect_json", "system", "user"}, ...]}`
* `BATCH-0007-matcher_a.md` — the same requests laid out for a person to copy into a chat window

Answer every request in a batch and save the answers next to it as
`BATCH-0007-matcher_a.response.json`:

```json
{ "<key of request 1>": "<the complete answer text>", "<key of request 2>": {"a": "JSON answers may be objects"} }
```

or as `BATCH-0007-matcher_a.response.md` with one block per request:

```
=== RESPONSE <key> ===
<the complete answer>
```

Then run `cr queue import <project>` (answers that should be JSON but do not parse are rejected and stay
pending) and `cr run <project>` to continue. Every answer is cached; nothing is asked twice.

If a request cannot be answered at all, do not invent an answer. Mark it skipped:

```
cr queue skip <project> --key <key> --reason "why it was not answered"
cr queue skip <project> --batch BATCH-0007-matcher_a --reason "..."    # every unanswered request in a batch
```

The harness then treats that call as failed and says so: the witness is held, the relation is recorded
as missing, and so on. Nothing downstream pretends the answer exists. To ask again later, delete
`queue/done/<key>.skip.json`.

## Rules for whoever answers

1. **One request at a time, independently.** Answer each request exactly as a model that received only that
   request's system prompt and user prompt would. Do not carry information between requests.
2. **No outside material.** Use nothing except the text of the request. Do not open other files.
3. **Separate contexts for separate roles.** The witness constructor and the witness auditor, matching pass A
   and pass B, and the blind FRD validator must be answered by different people / fresh agent contexts. Batches
   are grouped by role so this is easy.
4. **JSON when asked.** When `expect_json` is true, the answer is one valid JSON value and nothing else.
5. **Record who answered.** `cr queue import <project> --operator-model "<model or person>"` stores the identity
   with each answer; it appears in the call log and the release.

## Prompt given to each agent context in the PTX demonstration run

(Final wording. The first batches used an earlier version that saved helper scripts in a shared scratch
folder; two parallel contexts once collided on a file name. See `projects/PTX/queue/OPERATOR-NOTES.md`.)

> You are acting as the language model backend for a research harness. Work only with the batch file named
> below: open it with the Read tool (if the Read tool says the file is too large, call it again with
> allow_large set to true); do not open, list or search any other file, and do not use web search.
>
> Batch file: `<batch>.json`
>
> The file is JSON whose "requests" list holds objects with "key", "role", "expect_json", "system" and "user".
> For each request independently, follow its "system" prompt as your instructions and treat its "user" prompt
> as the input, exactly as a model receiving only that request would. Do not let one request's content
> influence another's answer. Do the task genuinely and carefully: these answers are the real model outputs of
> the run and will be audited against primary sources. When expect_json is true the answer must be a single
> valid JSON value of the requested shape and nothing else.
>
> Write every answer into `<batch>.response.json` as one JSON object mapping each request's "key" to its
> answer (a JSON object for JSON answers, a string otherwise). Run Python inline with a heredoc that builds
> the dict, writes the file with json.dump(ensure_ascii=False), re-opens it and checks one entry per key. Do
> not save script files anywhere (other agents share the scratch folders). Keep your replies short and do not
> reproduce source passages in prose. If you cannot answer a particular request, leave its key out and name
> it in your reply. Reply with the count of answers written (and any keys left out) and nothing else.

Role-specific additions: auditors were told "You are the independent auditor; be exacting rather than
generous"; constructors were told "Count words carefully against any word ceiling the request states".
