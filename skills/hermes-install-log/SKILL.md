---
name: hermes-install-log
description: "Log Hermes and pip installs to hermes_install.md."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, install, runbook, logging]
    related_skills: []
---

# Hermes Install Log Skill

After installing any Hermes plugin or skill, or any Python library (`pip install`) — append its
commands to `hermes_install.md` in the active workspace (currently
`/workspace/hermes_install.md`). Do this automatically, never wait to be asked.

## When to Use

- Installing any Hermes plugin (`hermes plugins install`) or skill.
- Any `hermes ... install` step.
- Installing Python libraries (`pip install`).

## Rules
- Verify successful installation.
- Append every install command in the order run, one command per line.
- Then append exactly one verification command for that install.
- English only, no comments, no blank separator lines between entries.
- Keep all prior commands intact; add new commands at the end.
- after appending Start a new session.

## Procedure

1. `read_file` `hermes_install.md`. If it does not exist, create it with the same name
   (`write_file` to `hermes_install.md`) before appending.
2. Append the new install command(s), one per line.
3. Append a verification command (`hermes plugins list`, `hermes skills list`,
   or `pip show <package>` for pip installs).
4. Write the full updated content back with `write_file`, or use `patch` to append.

## Verification

- The new commands are the final lines of the file, one command per line, with the
  verification command last.



