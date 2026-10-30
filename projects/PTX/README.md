# PTX for urination — Claim Registry project

The PTX investigation (header v4.1, two axes, six hypotheses), run through this harness on 2026-10-29.

| Folder | What it holds |
|---|---|
| `01_CORPUS\source-files\` | The 111 Markdown sources (4.9 MB), copied from the October 24 run |
| `01_CORPUS\manifests\` | Hash manifest of the corpus |
| `01_FRAME\` | The approved header, ranked index and Archivist prompt |
| `02_RUNS\RUN-PTX-2026-10-29\` | The run. Start with `RUN-STATUS.md`, then `10_REPORTS\` |
| `project.json` | Configuration (all roles routed to the file queue; `matching` settings declared for this run) |
| `PTX-model-calls-queue-and-release.zip` | Machine folders, packed to keep the folder light. Unzip here to restore them. |

The zip holds three folders:

- `cache\llm\`: the exact prompt and answer of every model call;
- `queue\`: every queued request, the batch files the operator answered, and the skip records;
- `04_RELEASES\`: the hashed release written by `cr publish`.

`queue\OPERATOR-NOTES.md` is kept outside the zip. It explains every incident in the run.

**What came from where.** Discovery (62 questions and their NotebookLM answers), the 77 candidate FRDs
and the 73 retained validations were imported from
`ChatGPT output\PTX-Full-Run-2026-10-24` (marked `imported` in the run). Paths in the run records that
start with `/mnt/user-data/uploads/FINAL SPECIFICATION DOCUMENTS/` refer to that folder on your Desktop.
Everything from coverage units onward was produced in this harness, by Claude answering the file queue.

**To check the run:** `python cr.py verify projects\PTX`. This makes no model calls. It re-checks:

- hashes;
- that every FRD quotation is in its source file;
- witness ceilings and audit status;
- coverage-set minimality;
- crux consistency.

**To continue it:**

1. Unzip the zip into this folder.
2. Route the roles to a provider in `project.json`.
3. Optionally delete `queue\done\*.skip.json` to have the skipped requests asked again.
4. Run `python cr.py run projects\PTX --from witnesses`.

Every answer already given is reused from the cache. `project.json` sets
`"cache_fallback_providers": ["queue"]`, so the answers given through the queue are reused even after
the roles are routed to another provider. Only the missing requests are asked.
