# Claim Registry UI implementation plan

Date: 2026-11-15  
Status: Proposed design and implementation sequence; no application code changed.  
Repository reviewed: `125b0b5` (`Expose hypothesis compilation and add conditional-scope handling`).

## 1. Product decision

Build a local research workbench around the existing harness. Its central job is to help a person understand the claim they are testing, assemble the relevant source material, inspect how the harness interpreted that claim, and follow the evidence through the run.

The primary journey is:

```text
Research brief + provisional hypotheses
                  ↕
Evidence plan → acquire/import → convert/check → corpus/index
                  ↕
Coach: compare frames → choose wording → inspect requirements → accept
                  ↓
Notebook and provider setup → readiness → launch
                  ↓
Monitor → human checkpoints → inspect findings and limitations
```

These are revisitable workspace sections, not a sequence of forms that loses progress when the user goes backward. A user with an existing project lands on its current state; a new user receives guidance in the same interface.

ACH_Eval, its 64-unit gauge, and the evidence pipeline's scientific behavior remain unchanged by this UI project. Language processing remains off by default. A UI feature is not an opportunity to introduce a new downstream scoring or steering method.

## 2. What to keep and change from the supplied design

The original notes and DeepSeek's design are inputs to this proposal, not instructions to execute automatically.

| Keep | Refine before implementation |
|---|---|
| Clear problem, desired outcome, and explanation of the tool | Distinguish what the user hopes to establish from what the evidence establishes; permit exploratory questions as well as immediate decisions. |
| Claim ladder and serious rival | Make assistance concrete, but do not require an arbitrary 30-character minimum or a named organization for every rival. An identifiable, defensible rival position is the point. |
| Evidence plan and source ledger | Use source targets as planning aids. Source counts, a token contrary paper, and green badges do not establish sufficiency. |
| Corpus conversion and index review | Show what was inspected and what remains uninspected. File size and successful conversion are not fidelity checks. |
| Human coach acceptance | Use review-and-accept language. Preserve the existing substantive session; do not add signatures, hash-copying, or simulated keyboard acceptance. |
| Artifact-backed readiness | Separate execution blockers from research limitations. Do not add universal rights or primary-study quotas as launch gates. |
| Domain-specific source gathering | Support any number of topic collections, with separate search histories where useful. Admit their selected sources into the one logical corpus used by the quest. |
| Role separation | Include the Manager as well as Investigator and Archivist. The Investigator sees the frame; the Archivist does not. |
| Local project storage | Explain that selected content is sent to NotebookLM, model providers, or an external converter when those features are used. Local storage does not imply local processing. |
| Five starting modes | Replace them with Create project / Open project, followed by suggestions based on existing artifacts. Advanced controls are a disclosure, not another workflow. |
| Requirements view | Move it into the first release. Show the actual compiled reading, not just an assistant's prediction of what the compiler might do. |

Final coach acceptance should normally follow corpus/index preparation so forecasts have a stated basis. Draft hypotheses and preliminary coaching can happen earlier. If an existing project has already accepted a frame, show its actual status and evidence basis; do not invalidate it merely because this preferred order differs.

## 3. Workspace and interaction design

Persistent navigation: **Overview · Question & frame · Evidence plan · Sources · Prepare & launch · Runs**.

The center contains the current task. A right-hand panel shows either context-sensitive help, implications of an edit, or a selected artifact. The header always identifies project, run if applicable, saved/draft state, and current background work. There is one suggested next action, with the other sections still accessible.

Use plain text alongside status colors. Keep jargon in expandable explanations. Provide keyboard navigation, readable tables, visible save/error states, and layouts that work without relying on color or a large display. Expose file paths and equivalent CLI actions in an optional details panel.

### Overview

Show the question, selected frame, admitted source count, research gaps, active run, and next useful action. Explain the tool with a small example: a corpus becomes source-grounded findings, findings bear on competing statements, and a reader can trace the result back to passages.

Explain the limits without a wall of disclaimers: retrieval may miss material, a quote can be genuine but misinterpreted, the corpus can omit relevant studies, and a stronger claim can score differently from a narrower one. Do not describe validation of model answers as trivial or guaranteed.

### Question & frame

The brief asks: What is the problem? What do you want to learn or decide? What result do you hope for? Who or what is in scope? What outcomes, comparator, harms, and time period matter? Which of these are still unknown?

Offer decision-first, hope-and-objection, and bridge-between-topics prompts as optional starting aids within the same editor. An assistant may propose alternatives, always displayed as proposals. Saving a draft does not accept it.

Display H1/H2/H3 together, including assumptions, falsification, corroboration, and governing boundary. Help the user identify a substantive rival and explain the axis's actual H3 wording. Do not silently turn a different substantive third hypothesis into equipoise.

The claim ladder compares stronger, intermediate, and weakest meaningful versions with their scope, evidential demands, and what a favorable result would permit the user to say. Preserve the user's original wording alongside proposed changes.

The requirements inspector has two distinct states:

1. **Draft evidence needs:** planning suggestions, explicitly uncompiled.
2. **Compiled reading:** the real unit compiler's saved output, showing required support, premises, boundaries, adverse tests, alternatives/conjunctions, and sentences without a recorded anchor.

Reuse `requirements.py` for the second state. Its missing-anchor warnings identify things to inspect; they are not proof that a concept disappeared. A preview for an unaccepted draft needs an isolated preparation context using the same compiler, without overwriting an accepted frame or fabricating an acceptance record. Show when it requires a model call. Invalidate a preview when its inputs change.

The coach presents forecasts with their basis (for example index-based or validated-FRD-based), alternative frames, restatement differences, consequences, and the user's responses. Forecasts are advisory predictions, never results. After coach edits, refresh the compiled reading or clearly mark it stale. Final acceptance applies to the exact selected wording through the existing acceptance mechanism.

### Evidence plan

Use editable rows: question/claim component, evidence needed, suitable source types, relevant topic collections, search terms, exclusions, and known gaps. Mark whether a row is a user planning priority or an actual compiled requirement.

Include adverse tests and rival-supporting searches. Prefer documenting the searches attempted and the evidence found to imposing a fixed contrary-evidence quota. Support search stopping criteria such as a time limit, a bounded reference expansion, or no additional eligible sources found by specified searches. Label these acquisition limits; they do not prove exhaustive search or compel an H3 result.

For a bridge between literatures, maintain separate search briefs and logs for each domain and a third, optional bridge search. Offer the user's two-context strategy as a way to reduce leading searches. Do not enforce an untested claim that every single-context search is biased. Keep a portable research brief with the exported search prompt so later relevance review does not depend on recovering a particular chat window.

### Sources

Use one table with filters for collection, candidate/admitted status, acquisition, conversion, review, and gaps. A source can belong to several collections. Do not duplicate its evidence because it has several tags.

Minimum entry: title or identifier, collection, provenance/import method, and candidate status. Enrich metadata progressively. First-release intake supports local Markdown/text, PDFs awaiting conversion, manual citations, and parsed BibTeX/RIS imports. Renaming `.bib` to `.md` is not conversion: retain the original bibliography and parse its records into candidates.

Each source drawer contains citation and identifiers; how it was found; original and converted files; access/license information if known; conversion method/settings; review flags; inclusion/exclusion reason; and links to study mappings and index entries. Show title-match duplicates as candidates for review. Byte-identical files, two reports of one trial, and independent studies are different relationships. Never merge witnesses or declare independent corroboration merely from bibliographic deduplication.

Separate states:

```text
Candidate → located/acquired → converted → checked → admitted
                    ↘ unavailable / excluded / needs review
```

Metadata-only candidates remain visible as research gaps and cannot enter the quoted evidence corpus. Reviews and guidelines can be useful sources; source-type eligibility depends on the claim and its use, not a universal ban.

Conversion is a resumable queue. Preserve originals; record converter/version/options and the resulting Markdown revision. Show original and extracted text together, emphasizing tables, numerals, negations, captions, and complex layouts. Automated warnings help prioritize review; they do not certify faithful extraction. A chart image being extracted does not mean its information is represented in the text-only pipeline.

Manual conversion/import is a complete first-release path. Add Datalab through an optional provider adapter later. Datalab documents Markdown output and parse-quality information, which can be recorded as vendor diagnostics, not a fidelity verdict ([official conversion description](https://www.datalab.to/platform/processors/convert)). The user's size-based batching preferences can be saved presets; do not hard-code them as quality rules.

The collection summary reports coverage of the user's search plan, source types, search attempts, gaps, duplicates, and conversion flags. Use **Prepared to run / Prepared with gaps / Needs preparation**, not a numerical corpus truth or sufficiency score. Distinguish relevance rank from methodological quality and certainty.

### Prepare & launch

Show corpus admission, ranked index, Archivist prompt, final frame/coach state, provider routes, notebook configuration, and execution limits in one checklist. A generated index and prompt must be inspectable and repairable. Index ranks use the harness's existing A/B/C/F scheme; they are not evidence weights.

Notebook setup begins with manual creation/upload and the existing Chrome/Playwright driver. The user signs in to Google directly. Record the mapping between admitted local sources and notebook sources, including whether the uploaded representation was PDF or Markdown. A file-count match or a successful test question cannot establish that every source was correctly uploaded.

Every additional notebook lane must serve the same logical corpus. Do not automatically split the corpus into disjoint notebooks when a capacity limit is encountered. Surface that limitation and let the user deliberately revise scope or change archive strategy; a different retrieval topology needs its own design.

Keep the frame, hypotheses, ranked index, private allocations, and expected answer out of NotebookLM. Inspect the actual Archivist prompt and questions; a forbidden-word check alone cannot prove absence of semantic leakage. Use the harness's existing firewall and distinguish manual review from automated checks.

A launch summary states the frame version, included sources, notebooks, execution mode, role/provider routes, time/question/call limits, estimated spending limit, and human checkpoints. Selected content transfers are explained at the action where they happen. Use ordinary review-and-launch, not repeated security or approval rituals.

Keep the gauge at 64 in this release. Do not offer optimization experiments. Keep experimental language controls out of the ordinary setup path. Expose existing advanced settings without inventing unsupported capabilities.

### Runs

Show a stage timeline, questions asked/captured/graded, backlog, lane health, source usage, elapsed time, estimated spend, provider failures, stop reason, and human decisions due. Keep post-quest and post-validation coach checkpoints distinct from the pipeline's explicit release gate.

A question drawer follows: question → captured response → validation/FRD → witness → matching/coverage role → assessment. Reuse the saved artifacts and existing audit report. Include both supporting and opposing material and study identity warnings.

Allocation plots show H1/H2/H3 across rounds with their actual denominators and axis. Label provisional question-response, validated-FRD, and final-witness assessments separately. Explain that allocations are model judgments under the prompt and frame, not a demonstrated calibration to real-world probabilities. An unchanged allocation can still accompany useful confirmation, a null finding, a correction, or unsuccessful retrieval; do not rank question value solely by score movement.

Offer **Stop after current work** and **Resume** only with the actual supported semantics. The existing relay drains active work and records operational closeout; expose that behavior first. A true pause without closeout is additional engine work, not merely a renamed STOP button. Distinguish operational termination, scientific stop, blocked work, and awaiting a human decision. Closing a browser tab does not cancel a job.

Results lead with the assessed frame, findings, requirements coverage, counterevidence, missing evidence, stop reason, and links back to sources. Do not make the winning allocation the only conclusion.

## 4. Readiness rules

Readiness is computed per action. Opening a project, drafting a frame, offline inspection, preparing a corpus, launching a live quest, and continuing a pipeline do not share one universal gate.

| Class | Examples | UI behavior |
|---|---|---|
| Execution blocker | Invalid required configuration; no readable admitted corpus; invalid required frame; required coach acceptance absent; missing required index/prompt; invalid notebook route for a NotebookLM quest; no usable live model route in live mode; another writer holds the project | Explain and link to repair. Re-check in the backend at execution. A typed reason does not make missing inputs executable. |
| Research limitation | Unavailable paper; unknown license metadata; thin topic collection; no adverse evidence found; unreviewed conversion flags; uncertain study identity; uncompiled or changed interpretation preview | State the limitation and permit the relevant action when the engine supports it. Offer repair, scope revision, or proceeding with the limitation recorded. |
| External-action constraint | A source is explicitly marked local-only; proposed upload or public export exceeds its recorded handling choice | Apply to that transfer/export. Do not mislabel the whole local research project as scientifically invalid. |
| Informational | Source count, search history, estimated throughput, last check time | Show the observation and its basis, without implying complete evidence. |

Each check returns `id`, action, status, severity, observed inputs/version, checked time, explanation, verification method, and repair action. Use `unknown` or `not checked` when appropriate. Distinguish **user confirmed**, **locally checked**, and **online checked**.

Reuse doctor checks, but extract structured results instead of parsing printed PASS/WARN rows. The current doctor does not prove notebook-source parity, rights clearance, exhaustive search, or semantic isolation. Live checks must be explicit because they can contact providers or make a small paid request. A stored green badge is not authority to launch against changed inputs.

Do not create a new mandatory evidence-plan acceptance gate or automatic H3 risk forecast. Preserve existing configurable coach requirements and show deviations from the default visibly.

## 5. Application architecture

Recommended implementation: a React/TypeScript client served by a local Python FastAPI/Uvicorn application, with supervised worker processes calling shared harness services. This is a proposed dependency choice, not an existing repository capability. Install UI dependencies separately so CLI-only use remains available.

FastAPI supports streaming responses and file responses; these fit event delivery and artifact inspection ([official response documentation](https://fastapi.tiangolo.com/advanced/custom-response/)). Use server-sent events for progress with cursor-based reconnection and a polling fallback. Do not run a multi-hour quest inside an HTTP request or a disposable request-background task.

```text
Browser UI ── typed local API ── Application services ── Harness modules
                                    │                       │
                                    ├── job supervisor      └── existing artifacts
                                    ├── readiness projection
                                    └── workspace metadata

CLI ─────────────────────────── same application services
Worker processes ────────────── same harness + durable job records
```

Refactor orchestration out of `cmd_*` functions incrementally; do not duplicate the pipeline in JavaScript. CLI printing/argument parsing, web requests, and coaching presentation are adapters around shared operations.

Proposed modules: `claimreg/app/` for services and records, `claimreg/ui/` for the local API/launcher, and `ui/` for client source. These names are proposed and do not exist yet. A new `cr ui` launcher starts the local application and opens its URL; desktop packaging can follow after the workflow works.

| Capability | Existing foundation | New work |
|---|---|---|
| Project/configuration | `config.py`, `onramp.py` | Shared create/open/update operations; version-aware saves; workspace summary |
| Corpus | `corpus.py` ingest, manifests, quality/duplicate flags | Candidate ledger, topic collections, bibliography parsing, conversion queue, admission and revision mapping |
| Frame/index/prompt | `header.py`, `index.py`, setup stages | Draft editing, proposal comparison, incremental preparation, source-backed previews |
| Coaching | `frame_gate.py`, `coach.py` | Resumable native session interface and transport-neutral input events |
| Requirements | `units.py`, `requirements.py` | Draft preparation context and typed inspector projection; no alternate compiler |
| Preflight | `onramp.py` doctor/notebook checks | Structured checks, per-action policy, freshness and repair links |
| Quest | `notebooklm/relay.py`, driver, `quest_import.py` | Job lifecycle adapter, unified events/status, documented stop/reconcile behavior |
| Pipeline/results | `pipeline.py`, `runctx.py`, reports, study mapping | Web projections, checkpoint decisions, artifact navigation; reuse existing calculations |

### Durable records and component contracts

Existing project files, manifests, run configurations, stage state, question records, and evidence artifacts remain authoritative for the engine. Additional UI metadata must not become a competing scientific database.

Proposed storage additions:

```text
00_WORKSPACE/
  workspace.json           # schema version, collection definitions, preferences
  brief.json               # structured draft; exports to existing question.md
  evidence-plan.json       # planning rows and search limits, not evidence
  search-log.jsonl         # queries, imported results, relevance decisions
  jobs/<job_id>/            # status, input versions, events, worker/recovery data
01_CORPUS/
  source-ledger.json       # candidates, provenance, file revisions and mappings
  source-originals/        # optional managed copies; preserve external originals
  source-files/           # admitted canonical text for new managed projects
  manifests/              # existing engine manifests
01_FRAME/                 # existing frame/index/prompt/coach records
02_RUNS/                  # existing engine runs and outputs
```

Respect configured paths in existing projects; do not relocate their corpus into this example layout automatically. Keep search logs, planning notes, bibliographies, and UI metadata outside the admitted source directory. They must not accidentally become primary evidence when ingestion recursively scans text files.

| Component | Input and result | Required invariant |
|---|---|---|
| Project service | Open/create a project; return workspace and engine summaries | Opening/importing is read-only until a deliberate save/action. Preserve unknown configuration fields. |
| Draft service | Save edits with expected revision; return new revision and affected previews | Atomic writes; detect external edits; no silent overwrite; no model call merely from typing. |
| Source service | Candidate/collection/file operations; return ledger records and admission preview | Stable ledger identity independent of content-derived manifest IDs. Keep PDF, conversion revisions, study identity, and current admitted source IDs distinct. |
| Preparation service | Explicit index, prompt, or compilation operation; return a job and derived artifacts | Record exact frame, manifest, prompt and model inputs; reuse only valid cached work; never mark generated suggestions accepted. |
| Coach service | Begin/resume, obtain next prompt, submit human response, review proposed edits, finalize | Same substantive coach behavior for CLI and UI; acceptance applies only to reviewed wording; stale sessions cannot overwrite newer edits. |
| Readiness service | Project plus intended action; return structured checks and input versions | No cached UI badge substitutes for backend validation; checking does not silently fix models or change settings. |
| Job service | Start an allowed operation; return durable job ID; stream events; request stop/resume | One mutating engine job per project; idempotent launch; state survives client disconnect. |
| Inspection service | Artifact/run/axis IDs; return saved findings and links | No model-generated explanations presented as recorded history; keep unknowns explicit. |

Use typed commands, not an API that accepts arbitrary shell strings. Mutation requests carry an expected revision; start requests also carry an idempotency key. Artifact access uses project-scoped IDs rather than arbitrary filesystem paths supplied by the browser.

An event contains a sequence number, job ID, time, stage, optional axis/question ID, event kind, concise message, and references to existing artifacts. Keep engine status records authoritative; events provide notification and history rather than independently recomputing scores or counts.

The native coach is a real refactoring task. The current implementation couples dialogue and acceptance to terminal input. Extract its transitions and presentation while preserving the meaning of its questions, consequences, and human choices. Retain the existing acceptance-record format and terminology internally for compatibility. Do not manufacture terminal timing, pipe scripted answers into `cr sign`, or write a certificate from a generic Next button. Until the native adapter passes equivalence checks, hand off to the actual terminal coach and refresh state afterward. Any future change to typing/paste or accessibility policy is a separate explicit product decision, not an incidental UI bypass.

### Job lifecycle, freshness, and recovery

Job states: `queued`, `running`, `awaiting_human`, `stopping`, `stopped`, `completed`, `failed`, and `interrupted`. Pipeline stages and quest closeout reasons remain separate fields. A completed worker process does not necessarily mean a scientifically completed quest or a completed pipeline.

The supervisor persists worker identity and heartbeats, enforces a project-wide writer lock shared with the CLI, and reconciles jobs after restart. Closing the browser leaves a running worker alone. If the supervisor exits or the computer restarts, show interrupted work and recover from committed records; do not automatically launch new paid requests. In-flight remote calls can have uncertain outcomes after interruption, so do not promise exactly-once billing or free retries.

Map Stop after current work to the relay's existing STOP/drain behavior and show what can still be captured or graded. Preserve failed/import-pending state if quest capture succeeds but import fails. Retry import without launching the quest again. Checkpoint release calls the existing decision/continue operations, not a direct edit of stage status.

Show estimated spend, calls, and outstanding work. The current router checks recorded spending against limits before calls; do not present that as a guaranteed maximum provider charge, especially with concurrent requests. A strict reservation-based spending ceiling would be separate backend work if required.

Use a dependency map for freshness:

- Source admission or converted text changes affect the manifest and dependent index/preparation artifacts; an existing frozen run retains its pinned inputs.
- Frame wording changes affect acceptance and derived requirements according to existing engine rules.
- Changes to index/evidence basis flag forecasts and previews for review without inventing a new automatic acceptance rule.
- Display preferences and citation metadata corrections do not automatically redo scientific stages.
- Provider/model or scientific configuration changes use the harness's existing invalidation logic; surface what would rerun before starting it.

Detect external edits on refresh/focus and before mutations. Preserve prior outputs and show superseded work rather than deleting it. Editing an active run's scientific inputs is blocked by its writer lock; make a draft/fork instead.

### Local application and content handling

Bind to loopback, validate host/origin, use a per-launch session secret, and authorize access to the opened project roots. Resolve paths, including Windows junctions, before reads/writes. Keep credentials in backend-managed local references; do not return secrets in frontend configuration, URLs, or logs. Sanitize Markdown/HTML from sources and models and avoid running embedded content. These are implementation requirements, not user-facing approval ceremonies.

Show a compact data-flow explanation:

| Action | Data leaving the machine |
|---|---|
| Local inspection/editing | None from that action |
| DOI/metadata lookup | Search identifiers or query text |
| External conversion | Selected original document(s) and conversion options |
| Notebook setup/query | Uploaded corpus representation, questions, and service interaction |
| Model-assisted preparation or run | Role-specific prompts and selected source/evidence passages |
| Export | The selected files; destination is the user's chosen route |

Respect per-source local-only handling choices by disabling incompatible external actions for those sources, rather than promising a local-only live NotebookLM workflow. Track access route, stated license, redistribution choice, and unknowns as metadata. Do not infer permission from possession of a PDF or from an open-access link. Export previews list included original files, converted text, and derivative artifacts so the user can control what is shared.

## 6. Implementation sequence and release boundaries

The first useful increment should open the existing LEVO project and show real state. Do not start by building all of the onboarding forms against mocked readiness.

| Milestone | Deliverable | Exit criterion |
|---|---|---|
| 0. Contracts and shared operations | Define workspace/check/job schemas; extract project summary, doctor results, and orchestration entry points; agree on low-fidelity screen layouts | The CLI still works; an existing project can be read without mutation; structured checks agree with the checks they replace. |
| 1. Existing-project workbench | Local launcher, navigation, overview, source/frame/requirements inspection, run timeline, report links | Open a completed LEVO run without paid calls; trace a displayed finding through its recorded question and source; missing records show as unknown. |
| 2. One controlled execution path | Durable worker, locking, progress/events, readiness, existing-project quest/pipeline actions, terminal coach handoff, stop/recovery, checkpoint UI | A fixture run survives browser disconnect and can stop/resume; duplicate launch is prevented; import-only retry works; real engine release gates are respected. |
| 3. Guided project construction | Brief/frame drafts, evidence plan, topic collections, candidate ledger, Markdown/PDF/bibliography import, conversion handoff/QC, index/prompt preparation, manual notebook setup | A new user can prepare a new project from supplied local material without undocumented file editing; acquisition notes never enter the evidence corpus. |
| 4. Native coaching and complete first release | Shared coach session adapter, frame comparisons, actual requirements preview, acceptance, launch summary, help/accessibility/error recovery | A new user can go from a blank project with supplied sources to a run, checkpoints, and inspectable results; existing projects retain CLI compatibility. |
| 5. Optional acquisition automation | Metadata/OA lookup, bounded related-paper expansion, Datalab adapter, richer upload verification, packaging | Each adapter has explicit data transfer, cache/retry behavior, provenance, and a usable manual fallback. No adapter is required to open or inspect a project. |

Milestones 0–2 produce a useful workbench for the existing harness. Milestones 3–4 complete the guided first release. Milestone 5 improves convenience and should follow the end-to-end path, not delay it.

The first two implementation tickets should be:

1. **Read-only project projection:** open a selected project and expose its configured corpus, frame, coach status, notebooks, runs, pipeline state, requirements, and saved reports. Add accurate missing/stale states. No live requests on open.
2. **Supervised action path:** run one existing operation through a durable worker with structured progress, shared locking, idempotent start, reconnect, and recovery. Prove the interface controls the real harness before expanding the wizard.

Defer a desktop wrapper/installer, collaboration/accounts, automatic publisher downloads, automatic notebook creation/upload, autonomous source expansion, corpus sufficiency scoring, and language experimentation. Retain hooks for them without exposing placeholder controls as working features.

## 7. Verification and acceptance

Use small saved-project fixtures and the existing local/demo machinery for development. Inspect the LEVO project read-only as a realistic compatibility example. No ACH_Eval tuning or source-versus-FRD scoring experiment is part of this work. A live paid end-to-end smoke run belongs to implementation validation when authorized, not to writing this plan.

Required checks are behavioral:

1. **Compatibility:** opening a legacy project changes no files; saved edits preserve unrelated config; CLI and UI see the same accepted frame and stage state.
2. **Interpretation:** the requirements panel agrees with saved compiler artifacts, labels previews separately, and never presents an absent explanation as historical fact.
3. **Isolation:** inspect outgoing payload fixtures by role. Archivist receives no frame/index/private allocations; Investigator does not receive allocations or primary bodies during discovery; Manager does not receive primary bodies during discovery. Source-only validation uses its existing separate access rules.
4. **Admission:** search logs and metadata-only records cannot become evidence; conversion revisions remain linked to originals; topic tagging does not multiply evidence; duplicate reports are not silently counted as independent studies.
5. **Freshness:** edit a header, converted source, or configuration externally; the UI reports the affected stale state, preserves prior outputs, and re-checks at execution.
6. **Human choices:** declining or interrupting coaching creates no false acceptance; refreshing a session preserves completed work; an acceptance against an old revision cannot overwrite a newer frame; checkpoint release follows the real gate.
7. **Recovery:** double-click launch, browser disconnect, worker failure, driver timeout, paid-provider failure, operational stop, successful capture with failed import, and reboot reconciliation each produce an intelligible recoverable state.
8. **Content and local API:** source Markdown cannot execute scripts; untrusted page requests cannot start jobs; artifact IDs cannot escape project roots; logs and API responses contain no keys.
9. **Usability:** a novice can state a question, compare frame options, import a supplied corpus, see gaps, complete coaching, configure an existing notebook, launch, and locate the evidence behind a conclusion without a developer editing files. Record points of confusion rather than declaring the design successful from screenshots.

Track UI outcomes separately from scientific outcomes: completion of setup tasks, mistaken state interpretations, failed recovery, unnecessary repeated work, and the user's ability to explain what a favorable result would actually mean. Do not optimize onboarding for speed at the expense of understanding the frame.

## 8. Recommendation

Proceed with this UI. The strongest improvement to the supplied proposal is to make the user's understanding visible at each transition: their question into hypotheses, hypotheses into actual requirements, source candidates into admitted evidence, and provisional allocations into traceable findings. Build that continuous path before automating the surrounding research services.

Reference inputs:

- `C:/Users/joshu/Desktop/Notes on Claim Registry UI.md`
- `C:/Users/joshu/Desktop/FINAL SPECIFICATION DOCUMENTS/Claude output/LEVO/QUEST-INITIALIZATION-UI-DESIGN-2026-11-15.md`
- `C:/Users/joshu/.codex/attachments/9b267514-9402-494a-b07a-5ad3573173de/Pasted text.txt`

