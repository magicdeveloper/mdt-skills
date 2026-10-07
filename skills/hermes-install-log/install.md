# hermes-install-log — Installation Task

You must install the `hermes-install-log` Hermes skill from the **current directory** into the `mdt` category. install it into current active Hermes profile

## Dependencies

| Type | Items |
|---|---|
| Skills (escalation helpers) | none |
| Python libraries | none |

Check all dependencies first: anything already present is skipped; anything missing you must install it silently — no questions, no confirmation.

```bash
# Paths
SKILLS_ROOT="${HERMES_HOME:-$HOME/.hermes}"
[ "${HERMES_PROFILE:-default}" != "default" ] && SKILLS_ROOT="$SKILLS_ROOT/profiles/$HERMES_PROFILE"
HERMES_BIN="${HERMES_BIN:-$(command -v hermes || echo /app/venv/bin/hermes)}"
```

## Step 1 — Check dependencies (before any install)

```bash
# The only runtime dependency is the hermes CLI itself (used for the final verification)
[ -x "$HERMES_BIN" ] && echo "OK: hermes CLI ($HERMES_BIN)" || echo "MISSING: hermes CLI (verification falls back to on-disk checks)"
```

## Step 2 — Install missing dependencies if not exist

```bash
# No Python libraries or helper skills are required by hermes-install-log — nothing to install.
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
cp -r "$(pwd)" "$SKILLS_ROOT/skills/mdt/hermes-install-log"
```

## Step 5 — Verify

```bash
"$HERMES_BIN" skills list
ls "$SKILLS_ROOT/skills/mdt/hermes-install-log"
```

`skills list` must show `hermes-install-log` under `mdt`, enabled; the folder must contain `SKILL.md`, `install.md`.
