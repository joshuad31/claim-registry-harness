# Proposal: a model-agnostic quest relay with provider failover (revision 2)

**Status:** revised proposal, ready to build in phases (§8).
**History:**

- Revision 1 was written 2026-11-09 by Claude (Opus 5.5) at Josh Davis's request.
- DeepSeek reviewed it the same day: verdict "build it, with changes".
- This revision folds that review in. §10 lists what changed and why.

**Read first:** `HANDOFF.md`, `docs/NOTEBOOKLM-QUEST.md`, `claimreg/notebooklm/MANAGER.md`.

## 1. Why

A discovery quest has a fixed shape. NotebookLM is the Archivist. There are exactly two research agents:

- an **Investigator**, which asks the questions;
- a **Manager**, which runs ACH_Eval and steers the Investigator with feedback packets and ready-to-send questions.

The NotebookLM side works with any model. Claude and DeepSeek have both driven the local driver successfully. On 11-09 it sent its first question 1.6 minutes after the go-ahead, and six lanes returned 12 usable answers in about four minutes.

The remaining weak points are in the reasoning roles and their plumbing. All three were seen on 11-09:

- **One provider's safety classifier halted a quest.** Two separate Claude Manager contexts were each stopped partway through grading round R001, on published pentoxifylline pharmacology for a patient-advocacy project. Nothing was saved.
- **A network outage stopped a pipeline role.** A VPN/DNS window interrupted `frd_validator` during DeepSeek's model run. One alternative provider would have made it a non-event.
- **A long-lived Manager context ran out.** In DeepSeek's run it died after 27 rounds. A fresh context picked up from a compact `state.md` and finished R028–R029 cleanly, which proves the stateless-handover design below.

The purpose of this harness is to let patients and clinicians work through the medical literature themselves. It cannot stop dead whenever one provider declines one step, or one connection or context fails. So:

1. **Any role can run on any provider:** DeepSeek, OpenAI-compatible endpoints, Anthropic, local servers, or the file queue answered by an agent.
2. **Failover belongs in the router, not in an agent.** When a provider refuses, filters, errors or times out, the role moves to the next provider in its list. The switch is recorded and never silent.
3. **The relay is plain Python and runs unattended.** An LLM overseer is optional operations tooling (§5), outside the research path.

## 2. Architecture

```
  Investigator model (API) ◄──┐            ┌──────────────┐            ┌──► Manager model (API), 2 calls/round
  header-public + index +     ├── relay.py ┤ firewall,    ├────────────┤    (a) assess → JSON {ledger_entry, new_state,
  latest packet + asked list  │  (Python)  │ pacing,      │            │        repair_requests}
                              └────────────┤ state, status├────────────┘    (b) packet → Markdown (## Ready questions)
                                           └──────┬───────┘
                                                  │ queue/Qnnnn.json  ▲ Qnnnn-A01.json
                                                  ▼                   │
                                    NotebookLM driver (unchanged) — 1 to 6 notebook lanes

  Optional overseer (any agentic LLM): reads relay-status.json / relay.log; restarts; edits relay.json;
  READ-ONLY on ledger, state and packets. Not a research agent.
```

| Part | What it is | What it never does |
|---|---|---|
| **Archivist** | NotebookLM through the existing driver (unchanged) | Sees the header, hypotheses or scores |
| **Relay** (`claimreg/notebooklm/relay.py`, new) | Python. Moves files, calls the two research roles through the router, applies the existing firewall, keeps versioned Manager state, paces to the Manager, writes status. Runs unattended | Makes research judgments |
| **Investigator** | A model role through the API (stateless calls) | Sees the Manager's scores or state: the relay never sends them |
| **Manager** | A model role through the API (two stateless calls per round; state passed in and out) | Touches NotebookLM |
| **Overseer** (optional) | Any agentic LLM session, for operations | Writes the ledger, state or packets, or grades or asks research questions |

**The quest still has exactly two research agents.** The overseer is optional operations staff, which Josh wants available to troubleshoot the relay. It is not a third research agent.

## 3. Reuse what exists. Step 0: merge DeepSeek's working copy

**Before building anything,** merge into this repo the `quest_tool.py` subcommands DeepSeek added and used on 11-09. The repo's `quest_tool.py` (as of commit "Handoff…") has only `enqueue`, `ingest`, `status` and `assessed`. DeepSeek's working copy also has:

- **`stage`:** driver answers → Manager workspace Markdown;
- **`packet`:** the mechanical firewall over a packet's ready questions (index filenames, the 900-word rule, the multi-source length rule, jargon, duplicates) → queue files;
- **`sync`:** ledger rounds → `assessed-qids.json`, with per-round `committed_at`.

Merge these, plus any other changes from DeepSeek's 11-09 model-quality run, with their tests. **The relay calls these functions. It does not reimplement them.** A second implementation would drift.

Also reused unchanged:

- **The provider layer** (`claimreg/llm/providers.py`, `router.py`). The `openai` type already reaches DeepSeek through `base_url: https://api.deepseek.com/v1` and an `api_key_file`. Keys are read at call time and never logged. Calls are cached by prompt, provider and model.
- **The driver:** queue in, answers out, `max_backlog`, `assessed_file`, `quest-clock.json` and `STOP` all work as they are.
- **The prompts:** `ACH_Eval_NLM_Super.md`, `coordinator.md`, `MANAGER.md`, `INVESTIGATOR.md`.
- **`cr quest-score` and `cr import-quest`.**

## 4. New pieces

### 4.1 Per-role failover in the router (benefits the whole pipeline)

Allow an ordered list wherever a role is routed today. **The single-string form keeps working.**

```json
"roles": {
  "quest_manager":      ["deepseek_reasoner", "deepseek_chat", "openai_alt", "queue"],
  "quest_investigator": ["deepseek_chat", "anthropic"],
  "frd_validator":      ["deepseek_chat", "openai_alt", "local"]
},
"providers": {
  "deepseek_reasoner": {"type": "openai", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-reasoner",
                        "api_key_file": "C:\\Users\\joshu\\Desktop\\FINAL SPECIFICATION DOCUMENTS\\ChatGPT output\\API key"},
  "deepseek_chat":     {"type": "openai", "base_url": "https://api.deepseek.com/v1", "model": "deepseek-chat",
                        "api_key_file": "C:\\Users\\joshu\\Desktop\\FINAL SPECIFICATION DOCUMENTS\\ChatGPT output\\API key"},
  "openai_alt":        {"type": "openai", "base_url": "<any OpenAI-compatible endpoint>", "model": "...", "api_key_env": "..."},
  "anthropic":         {"type": "anthropic", "model": "...", "api_key_env": "ANTHROPIC_API_KEY"}
},
"failover": {"max_passes_per_request": 1, "max_usd_per_round": 0.50}
```

**When to move to the next provider.** The checks are mechanical and per provider. Never match refusal phrases in prose, because legitimate hedging would cause false failovers.

- empty output;
- `finish_reason` in `{content_filter, refusal}` (or the provider's own equivalent);
- an HTTP 400 whose body matches `/content[_ ]?filter|safety|policy|blocked/i`, after one retry;
- schema validation failing twice (validate, repair once, then fail over);
- a transport error or timeout after the existing retry and backoff.

**Loop guard.** At most one pass through a role's provider list per request, plus a per-round budget ceiling. A prompt that fails everywhere then stops the round with a clear status, instead of multiplying spend.

**Provenance.** Every call record and the run log name the provider and model that produced the output, and why earlier providers were skipped.

**Caching intent.** Each call declares its stable prefix (spec, header, index), so providers can cache it:

- DeepSeek and OpenAI cache automatically;
- Anthropic needs `cache_control` markers.

**The quote gate stays provider-independent.** FRD quotations are checked mechanically against the source files, so a failover can never fake evidence. That makes the post-quest roles the highest-value use of failover (§8, v3).

### 4.2 The relay loop (`python -m claimreg.notebooklm.relay run <relay.json>`)

```
start: read config; write quest-clock go_ahead ONLY if absent (never reset on restart)
       Manager warm-up → private/state/R000.md
loop until STOP, the 3-hour limit, or the Manager directs STOP:
  quest_tool.stage → new driver answers into manager-workspace/answers/*.md
  if ≥ 6 new usable answers are unassessed and no round is in flight:
      round = next id; skip if a ledger entry for this id is already committed (idempotent restart)
      call A (assess): header + spec + state/<prev>.md + these answers + asked list
           → JSON {ledger_entry, new_state, repair_requests}; validate, repair once, else fail over
      append ledger_entry (committed_at = relay clock); write private/state/<round>.md; advance the state pointer
      quest_tool.sync → assessed-qids.json (releases the driver's pacing hold)
      call B (packet): header + new state + index + asked list → Markdown with "## Ready questions"
           (if call B fails everywhere, the round stays committed; the Investigator fills the gap)
  keep the queue topped up to the backlog limit, at most one packet's flight ahead:
      quest_tool.packet → firewall-clean ready questions → queue/Qnnnn.json
      if the queue would run dry: call Investigator (header-public + index + latest packet + asked list
           + per-source question counts) → questions → quest_tool.packet firewall → queue
  re-ask once (A02, another lane) for FAILED, off-target, or Manager-requested repairs
  write relay-status.json every few seconds (round, backlog, provider used per role, last error, spend)
end: closeout stub; cr quest-score; print the import command
```

**Firewall** (in `quest_tool.packet`, kept narrow):

- names one to three filenames that exist exactly in the corpus manifest or index;
- asks for "(exact source filename, actual section heading)";
- **deny-list:** hypothesis labels, `A1`/`H1`-style codes and allocation vocabulary, taken from the header. Numbers and percentages in a question are fine: "report the percentage change in IPSS" is a legitimate question;
- **length rule:** reject length requests below the 900-word answer floor ("900 words or less", "brief", "short answer" and similar). Only a single-source question may say "about 900 words or more"; multi-source questions state no length;
- not a duplicate of an asked query (normalized text).

Rejected questions are logged and sent back to the Investigator once.

**Information barrier.** The Investigator prompt is built from an allow-list of files and never includes the ledger, vectors or state. A test asserts this.

**Versioned state with rollback.** The Manager state lives at `private/state/R001.md`, `R002.md` and so on, each under about 10 KB. The pointer advances only after a round's ledger entry commits. A malformed state from a failover model can be rolled back; it is not fatal.

**Idempotent restart.** The round ID plus a committed ledger entry is the deduplication key. Suppose the relay crashes between appending the ledger and syncing `assessed-qids.json`. On restart it re-runs `sync`, not the round, so no round is graded twice.

**Source throttling.** The relay tracks questions per source from the index and passes the counts to the Investigator, so one paper can't be exhausted while C-rank sources wait.

## 5. The optional overseer (`docs/RELAY-OVERSEER.md`, v2)

The relay runs without it. Josh wants an LLM available to supervise and troubleshoot, so the playbook covers:

- **Watch** `relay-status.json`, `driver-status.json` and `relay.log`: is the round advancing, is the backlog ≤ 12, are lanes idle with an empty queue, is spend under its cap?
- **Do:**
  - restart the relay or driver (both resume from files);
  - move a role to its next provider by editing `relay.json`;
  - fix bugs and run the tests before restarting;
  - clear a degraded notebook copy's chat history only with Josh's OK. He signs in himself.
- **Never:**
  - write the ledger, state or packets;
  - grade answers or write research questions;
  - read answer content, except to diagnose a specific malformed round.

## 6. Acceptance tests

1. **Mock tests** (`tests/test_relay.py`; no network; mock providers; temporary driver folder):
   - the round loop with two Manager calls;
   - failover on an injected `content_filter` stop, an HTTP 400 "policy" body and a timeout;
   - the loop guard and budget stop;
   - firewall rejections, including "900 words or less", while accepting a question that asks for a percentage;
   - the information barrier;
   - state rollback after a malformed state;
   - an idempotent restart between ledger append and sync;
   - `go_ahead` not reset on restart.
2. **A one-round live test.** Using the 11-09 answers Q0001–Q0006 (in `Claude output\nlm-answers\`; DeepSeek has a known-good R001 packet for them), run R001 on `deepseek-reasoner`. Pass: a valid ledger entry, a packet with 8–10 firewall-clean ready questions, and nothing private in the packet. Measure the time per round. If it exceeds about 2 minutes, retest on `deepseek-chat`. The hard ceiling is 6 minutes for 45/h.
3. **A live timed quest** on the PTX notebooks with the driver plus relay, judged by `cr quest-score`. Pass all five:
   - first send ≤ 4 min after the go-ahead;
   - ≥ 15 saved by 20 min;
   - ≥ 45 graded in the first hour;
   - ≥ 45/h for the whole quest;
   - backlog ≤ 12.

## 7. Models and cost (DeepSeek's estimates, 11-09; verify against current prices)

- **Investigator:** `deepseek-chat`.
- **Manager:** try `deepseek-reasoner` first, and fall back to `deepseek-chat` if it's slower than about 2 minutes per round.
- **Context per Manager round:** about 40–50K input tokens (spec ~12K, header ~9K, state ~3K, six answers ~25K) and 3–8K output.
- **Cost:** at the prices DeepSeek quoted, a round costs about 2–3 cents. Automatic context caching cuts the fixed prefix substantially.
- **For comparison:** DeepSeek's 11-09 GPT-5.2 pipeline run cost $11.45 for 351 calls, about $0.036 per call.
- **Cost is not the constraint. Reliability and round time are.**

## 8. Phasing

**First, ship DeepSeek's current model-quality run.** That puts a real-model demonstration in the repo before the relay changes the plumbing.

- **v1:**
  - Step 0: merge DeepSeek's `quest_tool` commands (§3);
  - router list-form failover with mechanical refusal detection, the loop guard and a budget cap;
  - the relay loop for the Manager (two calls) and the Investigator, using the `quest_tool` functions;
  - versioned state, idempotent restart, `relay-status.json`;
  - mock tests and the one-round live test.
- **v2:** the overseer playbook, then the live timed quest.
- **v3:** failover lists for the post-quest roles (FRD generation and validation, matching).

## 9. Notes

- **Privacy:** the corpus is published literature, and sending excerpts to an API provider is acceptable for this project. Never send keys, the Google session or personal files. Keys stay in key files or environment variables, referenced by path. Add `relay.json` to `.gitignore` if it ever holds a key.
- **Josh's NotebookLM rules still apply** (`HANDOFF.md` §2): Custom + Longer, no Fast Research or Import, no saved notes, the 900-word answer floor, and he signs in himself.
- **Working with Josh:** share the build plan before starting; stop when it's good enough; publish through his GitHub Desktop clone.

## 10. What changed from revision 1, and why

| # | Revision 1 | Revision 2 | Why (DeepSeek's review, plus Claude's reconciliation) |
|---|---|---|---|
| 1 | One Manager call returning JSON with the packet inside | Two calls: JSON assessment, then a Markdown packet | Escaping about 10 KB of Markdown in JSON invites truncation, and one bad JSON loses the round. A packet refusal no longer loses the ledger entry |
| 2 | The relay reimplements the firewall, staging and sync | The relay calls `quest_tool stage/packet/sync`; Step 0 merges them first | One implementation, no drift. These commands exist only in DeepSeek's working copy today |
| 3 | The deny-list included percentages and "word counts under 900" | Deny hypothesis labels and allocation vocabulary only; reject length *requests* under 900 | Percentages are legitimate; the 900 rule is about the answer length requested |
| 4 | A single `state.md` | Versioned `state/Rnnn.md`, advanced after commit, with rollback | A malformed state from a failover model must be recoverable |
| 5 | "Resume from files" | Idempotent restart keyed on round ID plus committed ledger; `go_ahead` written once | No double grading after a crash; the clock is never reset |
| 6 | A refusal-pattern list in prose | Mechanical per-provider signals; one pass through the list; a budget cap per round | Avoids false failovers on hedging and runaway spend |
| 7 | The overseer as part of the architecture | The relay runs unattended; the overseer is optional, read-only on scientific files | Keeps "exactly two research agents" true while giving Josh the LLM supervision he asked for |
| 8 | Build everything | v1/v2/v3, after the model-quality run ships | Smaller, testable steps |
| 9 | Open model questions | Answered in §7 from DeepSeek's 11-09 evidence | Same |
