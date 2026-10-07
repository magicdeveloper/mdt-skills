---
name: document-fact-extractor
description: Use when extracting every useful fact from any document.
version: 0.1.0
author: Mohamed Elghannam
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [document-processing, fact-extraction, information-mining, pdf, docx]
    related_skills: [pdf, docx, obsidian-markdown]
---

# Document Fact Extractor

Extract every useful fact from any text-bearing file (PDF, Word, Excel, PowerPoint, OpenDocument, RTF, EPUB, HTML, Markdown, plain text, CSV, Jupyter notebooks — including its images, tables, and diagrams) into a compact Obsidian-Markdown facts file: one short fact per line, in the source language, grouped thematically, deduplicated, opening with the file name, the business document type, and a ≤500-char summary. Zero invented content.

## When to Use

- User points to a document and asks to extract, mine, or digest its facts, values, and key information into a file.
- Building a compact knowledge-base entry from a document.

Don't use for: prose translation, narrative summaries, or preserving the original structure.

## Prerequisites

- `read_file` — the primary extractor; it auto-extracts PDF, Word, Excel, PowerPoint, OpenDocument, RTF, EPUB, notebooks, and plain text to readable text (tables included).
- The `pdf` skill and the `docx` skill — used only when `read_file` is not enough (per-page structure, embedded tables/images, heading outline, OCR).
- Scanned PDFs: OCR via the `pdf` skill's OCR extraction reference.

## Procedure

1. **Gather.** Ask the user for the source file path and confirm the output location (propose `<stem>-facts.md` next to the source).
2. **Extract with built-in tools — write no extraction code:**
   - Default for every text-bearing format: `read_file` (auto-extracts PDF, Word, Excel, PowerPoint, OpenDocument, RTF, EPUB, notebooks, plain text; markdown tables read as-is).
   - Escalate to the `pdf` skill only when `read_file` is not enough: `pdf_read.py <f> --meta` (page count, `encrypted`, `likely_scanned_pages`), `pdf_read.py <f> --text` (per-page JSON), `pdf_read.py <f> --tables` (scrambled tables). Scanned/image-only pages → `pdf` skill OCR extraction reference; if OCR is unavailable, warn the user and stop.
   - Escalate to the `docx` skill only when `read_file` is not enough: `docx_read.py <f> --text`, `--structure` (heading outline), `--images <dir>` (embedded images).
   - Pages for non-PDF formats: estimate as `round(words / 500)`.
3. **Vision.** For every extracted image (and any PDF page whose text is nearly empty — likely a figure), run `vision_analyze` in parallel batches (`region` zoom for small text). Report only what is visibly stated — labels, values, relationships shown — source language, one fact per line, never infer missing parts.
4. **Size.** `pages ≤ 20` → skip to step 6. Larger → step 5.
5. **Split.** The split script only consumes what the built-in tools produced — it never reads the document itself:
   - PDF: save `pdf_read.py <f> --text` output as `pages.json` (its raw object with a `pages` array is accepted as-is).
   - Any other format: run with the extracted text directly — `python3 <skill_dir>/scripts/split_document.py --text <extracted.txt> <headings.json> <outdir>` (chunked internally into 250-line pseudo-pages).
   - `headings.json` (`[{level, title, page}]`, optional): docx → `docx_read.py --structure` with estimated pages; markdown → the `#` heading lines from `read_file`; PDF bookmarks → only if the `pdf` skill exposes them; otherwise omit it.
   - Splits by headings recursively, falls back to ~10-page chunks with exactly 1 page of overlap; every unit ≤ 20 pages.

6. **Extract per unit.** For ≤ 20-page documents extract the full text yourself. For larger ones, dispatch one `delegate_task` subagent per unit, all in parallel, passing the unit path, the source language, its facts-file path, and the prompt from `templates/subagent-prompt.md`. Contract: one fact per line, as short as possible, exact values, source language, stated facts only, no repeated facts (shortest wording wins), no headings/bullets, NO_FACTS line if empty, self-check completeness and no-duplicates before writing.

6b. **Wait gate — never end the task while subagents are running.** `delegate_task` returns immediately and subagents keep running in the background. Run `terminal(command="python3 <skill_dir>/scripts/wait_for_units.py <facts_dir> <N>")` (polls every 30 s, ~5 min per cycle; N = unit count in `units/index.json`). Exit 0 = all N files present and stable (size unchanged across two checks). Exit 1 = cycle timeout: report progress to the user in one short line (X of N done, missing: …), then run the next cycle — up to 10 cycles (~50 min). If units are still missing: read the failed units' live transcripts (`~/.hermes/profiles/<profile>/cache/delegation/live/<deleg-id>/task-*.log`), diagnose the cause (read error, tool failure, truncation, session interruption), fix it, re-dispatch ONLY the failed units (each writes a distinct file, so re-dispatch is safe), and keep waiting until the gate exits 0.
7. **Merge.** Refuse to run while any unit file is missing — go back to the wait gate and re-dispatch. Collect all unit outputs + vision facts. Group thematically (`## <Group>` by subject). Remove verbatim and paraphrase duplicates (keep the shorter wording).
8. **Deep review — hard gate. Never save before every check passes:**
   - Completeness: ≤ 20 pages → re-scan the extracted text against the file; nothing useful missing. Larger → compare per-unit fact counts before/after merge; a unit shrank > 20% → re-extract that unit, never patch.
   - Dedup: no two lines carry the same fact; overlap-page duplicates gone.
   - Structure: one fact per line; source language; frontmatter complete (`name`, English `description` ≤ 60 chars, `source`, ≥ 8 `tags`, `language`, `extracted`, `pages`, `facts`); summary ≤ 500 chars and matches content.
   - Anti-hallucination: every line traceable to the source; drop the rest.
9. Write a one-line English description of the document (≤ 60 chars) and at least 3 lowercase English topic tags.
10. Strictly predict up to 8 relevant `tags` based on file content, intended use, and business domain; strictly NO spaces (use hyphens), max 8 tags, use standard uppercase acronyms (e.g., `RFP`, `SRS`, `BRD`, `PRD`, `CDM`, `LDM`, `ERD`, `SOP`, `API-spec`, `HLD`, `audit-report`).
11. **Write.** Save with `write_file` to the confirmed location:
```markdown
---
name: <Business name>
description: <English, ≤ 60 chars>
source: <original file name>
tags: [<tag1>, <tag2>, <tag3>]
language: <source language>
extracted: <YYYY-MM-DD>
pages: <page count>
facts: <fact count after dedup>
---

# <original file name>

Type: <business document type>

Summary: <≤ 500 chars, source language>

## <Thematic group>

<fact line>
```

## Hard Rules

- Only what the file states — never invent, assume, derive, translate, or round values.
- One fact per line, very short, plain lines (no bullets).
- Facts and summary in the source language.

## Pitfalls

- Multi-column PDFs: sanity-check read order in the per-page text; if garbled, use the `pdf` skill's other extractors.
- OOXML variant namespace (purl.oclc.org officeDocument rels) makes both `read_file` and the `docx` skill fail — the file is a valid docx. Fall back to a minimal stdlib read (zipfile + regex over `word/document.xml`: `<w:t>` per paragraph, `<w:pStyle>` for heading levels, `<w:tbl>` rows; unzip `word/media` for images). One-off runtime fallback, not shipped code.
- Scrambled tables: re-extract with the `pdf` skill's table tools.
- Subagents run in the background after dispatch — the wait gate (step 6b) is mandatory; the facts files are the source of truth, never the delivery messages (they can be lost or delayed).
- Session interruption kills running subagents — the wait gate times out, so re-dispatch the missing units (idempotent).
- Image facts often duplicate text facts — removed at merge.
- Many images = many vision calls — run parallel batches.
- docx page counts are estimates — the 20-page threshold is approximate.
- Overlap duplicates boundary facts — expected; merge removes them.
- "Almost done" is not done — the deep-review gate (step 8) must pass before saving.

## Verification

- Facts file exists at the confirmed path with frontmatter keys `name, description, source, tags, language, extracted, pages, facts`.
- The wait gate exited 0 (all N unit files present and stable) before the merge ran.
- Step 8 checklist passed; `facts` equals the count of non-empty lines under the groups.
