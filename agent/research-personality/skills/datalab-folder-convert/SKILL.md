---
name: datalab-folder-convert
description: Convert selected local research documents into Markdown through Datalab, preserving filenames and tracking per-file completion. Use for conversion requests, not for source discovery or evidence assessment.
---

# Datalab folder conversion

Use the converter documented in [the kit README](../../README.md). In Claim Registry run `python cr.py convert <project> --dry-run` first to inspect the file set; when conversion is requested run without `--dry-run`. The standalone distribution provides `datalab_convert.py` with a folder argument instead.

Default to accurate mode, three workers, exact original filename plus `.md`, and preserved subfolders. In a project use its configured source directory; standalone uses `Markdowns`. Use balanced or fast when the user requests it. Do not infer conversion quality solely from file size.

Use `DATALAB_API_KEY` or `--key-file` with an external file. Never put secret values in instructions, chat, logs, archives, or examples. Conversion sends documents to Datalab and may cost money; explain this before first use. Do not run a paid live conversion just to test the kit.

Use direct local uploads; do not copy documents to another bot's machine or create ZIP staging batches unnecessarily. Keep originals. Do not insert provenance headers or comments into the resulting Markdown; maintain JSON sidecars instead. Poll pending jobs after interruption. Unverified or changed existing outputs need review before `--force`; do not blindly skip by filename or resubmit an uncertain job.

Report per-file outcomes. Compare tables, quantities, units, symbols, and negations with the original, prioritizing complex pages. Count reconciliation detects missing files, not missing evidence. No implicit translation or automatic corpus registration.
