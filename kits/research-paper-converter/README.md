# Research Paper Converter kit

**Integration update:** the complete supplied kit, including the six restored memory/research files, is now the standing [research personality](../../agent/research-personality/PERSONALITY.md). `cr start` and `cr personality` emit every file; Cursor rules inline them all. The source package on disk is authoritative and the rebuilt ZIP retains every supplied file. The earlier five-file description below records the initial implementation and is superseded where it says memories are absent.

A portable, depersonalized paper-preparation kit for a local AI assistant, including Cursor, Codex, Claude, or a compatible bot with filesystem and web tools. It contains no owner profile, personal memories, research history, credentials, or machine-specific paths. It does not configure a particular hosted bot service automatically.

In Claim Registry, the assistant reads `AGENT-GUIDE.md` when preparing papers. The two `skills/` folders provide task-specific instructions. Existing Claim Registry role isolation and human acceptance rules still apply.

## Convert in Claim Registry

Put originals in `<project>/01_CORPUS/pdf/`. Preview without uploading:

```text
python cr.py convert "projects/MyResearch" --dry-run
```

When conversion is requested, use `DATALAB_API_KEY` from the environment or an external key file. Install the optional dependency with `python -m pip install requests`. Never put a key in chat, a command-line value, project documents, or this kit.

```text
python cr.py convert "projects/MyResearch" --key-file "<external-key-file>"
```

Accurate mode and three workers are the defaults. `--mode balanced` or `--mode fast` changes the mode; `--folder` selects a different input folder. Subfolders are preserved: a small `article.pdf` becomes `article.pdf.md`. Output exceeding 210,000 bytes is split into named pieces before admission; the unsplit original is retained outside the corpus. Retries verify every piece before skipping the conversion. See [corpus intake](../../docs/CORPUS-INTAKE.md). Conversion does not register the corpus or alter existing runs. Review the text and then use `cr corpus` to register it.

This uploads documents to Datalab and can incur charges. A dry run does neither. Converted Markdown contains the conversion text only; provenance and pending job records are JSON sidecars under `.conversion-state`. Nonempty, unchanged outputs with matching records are skipped. Unverified existing outputs are preserved and reported; `--force` explicitly permits replacement and can incur another charge. A timeout after submission can have an unknown billing outcome: inspect provider jobs before forcing another submission.

## Standalone distribution

The distributable ZIP includes the same converter as `datalab_convert.py`:

```text
python datalab_convert.py "<papers-folder>" --dry-run
python datalab_convert.py "<papers-folder>" --key-file "<external-key-file>"
```

Standalone output defaults to a `Markdowns` subfolder. It requires Python 3.11+ and, for actual uploads, `requests`. No bot-specific secret UI is assumed.

## Scope and checks

Bibliographies and source shortlists are planning artifacts, not primary evidence. The bibliography skill is an assistant workflow, not a new automatic bibliography command. Source lookup depends on the host assistant's available web tools. Verify a downloaded file rather than trusting HTTP success or a `.pdf` suffix.

Review tables, units, numerals, negations, and complex layouts against originals. File counts and a successful conversion do not certify fidelity. Preserve foreign-language originals; conversion is not a translation workflow. Keep figures or extraction limitations visible rather than assuming images are represented by their captions.

To rebuild the distribution from this repository, run `python tools/package_research_kit.py`. The builder uses an explicit allowlist; it does not copy user projects, runtime records, hidden files, or the original archive.

API reference checked during integration: [Datalab conversion request and polling](https://www.datalab.to/blog/faster-api-responses).
