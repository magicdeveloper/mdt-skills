# mdt-skills

A small collection of [Hermes Agent](https://hermes-agent.nousresearch.com) skills, installed under the **`mdt`** category.

## Installation

```bash
hermes skills install magicdeveloper/mdt-skills/skills/document-fact-extractor --category mdt
hermes skills install magicdeveloper/mdt-skills/skills/hermes-install-log --category mdt
```

Verify: `hermes skills list` — both skills must appear under `mdt`, enabled.

> **Note:** `hermes skills install` copies the skill files only — it does **not** install dependencies. See [Prerequisites](#prerequisites) below.

---

## Prerequisites

Run these **before** installing the skills. Each check is silent: present → skip, missing → install.

### Python libraries (document-fact-extractor)

```bash
# Check (import name → pip package):
python3 -c "import fitz"          # pymupdf
python3 -c "import pypdf"         # pypdf
python3 -c "import pypdfium2"     # pypdfium2
python3 -c "import pdfplumber"    # pdfplumber
python3 -c "import docx"          # python-docx

# Install whatever is missing:
pip install pymupdf pypdf pypdfium2 pdfplumber python-docx
```

### Hermes skills (document-fact-extractor escalation helpers)

`pdf` and `docx` are bundled Hermes skills. Check with `hermes skills list`; if missing, restore them:

```bash
hermes skills opt-in
```

---

## Skills

### document-fact-extractor

Extracts every useful fact from any text-bearing document (PDF, Word, Excel, PowerPoint, OpenDocument, RTF, EPUB, HTML, Markdown, plain text, CSV, Jupyter notebooks — including images, tables, and diagrams) into a compact Obsidian-Markdown facts file: one short fact per line, in the source language, grouped thematically, deduplicated, opening with the file name, the business document type, and a summary. Zero invented content.

**When to use:** when a document needs to be mined into a compact knowledge-base entry — the user asks to extract, digest, or fact-mine a file.

**Dependencies:**
- Hermes skills: `pdf` (`pdf_read.py`), `docx` (`docx_read.py`) — escalation helpers only
- Python libraries: `pymupdf`, `pypdf`, `pypdfium2`, `pdfplumber`, `python-docx`

### hermes-install-log

Automatically logs every Hermes plugin/skill install and every `pip install` to `hermes_install.md` in the active workspace — one command per line plus a verification command, in order, English only.

**When to use:** after any Hermes install operation (plugins, skills, other `hermes ... install` steps) or any Python library install — run automatically, never wait to be asked.

**Dependencies:** none (only the `hermes` CLI itself for verification).

---

Each skill folder also ships an `install.md` with a dependency-checking, idempotent local-install procedure for cases where the GitHub route is not available.
