# Lessons learned while doing the work

## Datalab
- Endpoint POST https://www.datalab.to/api/v1/convert, header X-API-Key, form fields mode=accurate, output_format=markdown; poll request_check_url every ~5s until status=complete; markdown is in the "markdown" field, page count in "page_count". Results expire after about an hour, so save immediately.
- Accurate is about a few cents per page; drug labels and low-value docs can go balanced to save money. Roughly $11 for ~1,470 pages accurate in one big batch.
- 3 concurrent requests with 3 retries each is reliable. Back off on 429.
- No translation option exists; additional_config only supports keep_pageheader_in_output, keep_pagefooter_in_output, keep_spreadsheet_formatting. Foreign papers convert in the original language; NotebookLM can translate.
- Never prepend provenance comments; NotebookLM rejects them.

## Moving files between the bot's computer and the user's PC
- Stage unconverted files in AgentScratch\temp\<job>\ as F1.pdf, F2.pdf... with map.txt (tab-separated short name -> original filename) so odd characters in filenames never break transfers; zip, copy to the box, convert, zip results, copy back, unzip, rename via map.txt into Markdowns, delete the temp folder.
- Copy-back can occasionally land the zip at %USERPROFILE%\out.zip instead of the target path; check for it, move it, and make sure no stray zip is left. Never delete map.txt before the rename finishes.
- Use PowerShell -LiteralPath everywhere (brackets and % in paper filenames).
- After each batch verify PDF count == markdown count, no missing, no empty files.
- The user's PC can go offline mid-job; keep the converted output on the bot's computer and copy it in when the PC is back.
- Chat attachments arrive with hash names; recover the real paper (title/authors in the converted text) and name it authorYear.pdf(.md), and copy the PDF into the folder too.

## Papers and DOIs
- LLM-supplied (Perplexity, NotebookLM, Gemini) DOIs and PMIDs are wrong surprisingly often (off-by-one suffixes, other papers entirely, invented .pubN versions). Always check https://api.crossref.org/works/{doi} and compare title/first author/year; find the right one with Crossref query.bibliographic. PubMed eutils needs a browser User-Agent.
- Old JBJS/Spine/LWW papers often do have DOIs (10.2106/..., 10.1097/...) even when lists say PMID only.
- Some journals (e.g. J Nucl Med 2003) have no DOI; give the free journal page instead.
- Check for duplicates: the same paper often arrives under a DOI-style name and an authorYear name.
- When a "missing paper" list arrives, compare it against the folder first and report which are already present.
