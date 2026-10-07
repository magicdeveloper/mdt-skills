# document-fact-extractor — Installation Task

You must install the `document-fact-extractor` Hermes skill from the **current directory** into the `mdt` category. install it into current active Hermes profile 

## Dependencies

| Type | Items |
|---|---|
| Skills (escalation helpers) | `pdf` (pdf_read.py), `docx` (docx_read.py) |
| Python libraries | `pymupdf`, `pypdf`, `pypdfium2`, `pdfplumber`, `python-docx` |

Check all dependencies first: anything already present is skipped; anything missing you must install it silently — no questions, no confirmation.

```bash
# Paths
SKILLS_ROOT="${HERMES_HOME:-$HOME/.hermes}"
[ "${HERMES_PROFILE:-default}" != "default" ] && SKILLS_ROOT="$SKILLS_ROOT/profiles/$HERMES_PROFILE"
HERMES_BIN="${HERMES_BIN:-$(command -v hermes || echo /app/venv/bin/hermes)}"
```

## Step 1 — Check dependencies (before any install)

```bash
# Libraries
for pair in "fitz:pymupdf" "pypdf:pypdf" "pypdfium2:pypdfium2" "pdfplumber:pdfplumber" "docx:python-docx"; do
  mod="${pair%%:*}"; pkg="${pair##*:}"
  python3 -c "import $mod" 2>/dev/null && echo "OK: $pkg" || echo "MISSING: $pkg"
done

# Skills
mkdir -p "$SKILLS_ROOT/skills"
for s in pdf docx; do
  find "$SKILLS_ROOT/skills" -name "${s}_read.py" 2>/dev/null | grep -q . && echo "OK: skill $s" || echo "MISSING: skill $s"
done
```

## Step 2 — Install missing dependencies if not exist

```bash
# Libraries
for pair in "fitz:pymupdf" "pypdf:pypdf" "pypdfium2:pypdfium2" "pdfplumber:pdfplumber" "docx:python-docx"; do
  mod="${pair%%:*}"; pkg="${pair##*:}"
  python3 -c "import $mod" 2>/dev/null || pip install -q "$pkg"
done

# Skills — bundled seeding first, then bundled source, else WARN
for s in pdf docx; do
  find "$SKILLS_ROOT/skills" -name "${s}_read.py" 2>/dev/null | grep -q . && continue
  "$HERMES_BIN" skills opt-in >/dev/null 2>&1 || true
  find "$SKILLS_ROOT/skills" -name "${s}_read.py" 2>/dev/null | grep -q . && { echo "Restored: $s"; continue; }
  src="$(find /app/hermes-agent-src/skills /opt/hermes/skills -maxdepth 3 -type d -name "$s" 2>/dev/null | head -1)"
  if [ -n "$src" ]; then cp -r "$src" "$SKILLS_ROOT/skills/$s" && echo "Installed: $s"; else echo "WARN: $s unavailable"; fi
done
```

## Step 3 — Check the mdt category, then create it if missing

The skill must be installed **inside the `mdt` category**. Verify the category first, then create it if it does not exist:

```bash
# Verify the category
[ -d "$SKILLS_ROOT/skills/mdt" ] && echo "OK: category mdt" || echo "MISSING: category mdt"

# Create it if missing (no-op when it exists)
mkdir -p "$SKILLS_ROOT/skills/mdt"
```

## Step 4 — Install the skill into the mdt category from this folder

```bash
cp -r "$(pwd)" "$SKILLS_ROOT/skills/mdt/document-fact-extractor"
```

## Step 5 — Verify

```bash
"$HERMES_BIN" skills list
ls "$SKILLS_ROOT/skills/mdt/document-fact-extractor"
```

`skills list` must show `document-fact-extractor` under `mdt`, enabled; the folder must contain `SKILL.md`, `scripts/`, `templates/`, `install.md`.
