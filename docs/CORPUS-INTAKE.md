# Corpus file limit

Every admitted Markdown or text file must be at most **210,000 bytes** (decimal 210 KB). This is the user's operational NotebookLM limit, not a claim about the service's published maximum. Bytes are measured on disk, including multibyte Hebrew and other Unicode text.

The assistant stages downloads and edits outside the configured source folder, then runs:

```
python cr.py corpus <project> --add <file-or-folder>
```

`cr new --corpus`, `cr init --copy-corpus`, and `cr convert` use the same admission layer. Oversized text is split before any admitted Markdown file is written. `cr corpus` also repairs oversized files already placed in the folder by an external tool, before writing a manifest. This is application enforcement; it does not block Explorer or unrelated programs from writing files. After such a write, run `cr corpus` before uploading or using the corpus. A stale manifest pointing at an oversized file is refused when loaded.

Pieces use stable names such as `paper--<content-hash>.part-0001.md`. Splitting prefers paragraph, line, then space boundaries; an unusually long paragraph, table, or unbroken string may need a byte-boundary split. If the last piece would be under **20,000 bytes**, the final two pieces are merged when they fit, or rebalanced around their midpoint. Every piece of a split document stays between 20,000 and 210,000 bytes. Naturally small documents remain intact without padding. UTF-8 characters are never cut. No summaries, overlapping passages, or invented headings are added. Review tables and cross-part context when preparing NotebookLM uploads. Cite the actual piece filename and its heading; the original unsplit filename is not an alias for an arbitrarily chosen piece.

The exact original is retained outside the corpus: under `99_ARCHIVE/corpus-originals` for a standard project, or in a sibling `<source-folder>-originals` directory for standalone/custom output. Legacy Windows-1252 text is normalized to UTF-8 for the pieces; the original bytes remain in that archive. The hidden `.corpus-parts.json` sidecar records original identity and hash, part order, hashes, and byte offsets in the UTF-8 reconstruction. Concatenating pieces in order recovers the normalized document. The corpus manifest carries that provenance.

The checklist counts the pieces as one logical source, and the study map groups them under the original document. Original-filename synthesis exclusions, duplicate-copy exclusions, and study overrides continue to apply. Conversion retries verify every recorded piece and do not upload again when the completed output matches. Edited or conflicting pieces are preserved and require reconciliation before replacement.

Existing research projects are not automatically migrated by installing this update. Run corpus registration deliberately before framing a new investigation. Splitting an existing corpus changes filenames and its manifest; rebuild its index and review affected citations/frame wording before continuing an existing investigation. Never rewrite an old run's recorded manifest or approvals to hide those changes.
