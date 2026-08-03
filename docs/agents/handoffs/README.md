# Handoffs

This folder is the designated output location for the `/handoff-conversation` skill.

## Purpose

When an agent session ends mid-task, `/handoff-conversation` writes a structured snapshot
of the in-flight context here so the next session can resume without losing state.

## Naming convention

Files are named using the pattern:

  YYYY-MM-DD_<slug>.md

where `<slug>` is a short kebab-case description of the feature or task in progress
(e.g. `2025-06-07_auth-refactor.md`). If multiple handoffs happen on the same day for
the same task, append a counter: `2025-06-07_auth-refactor-2.md`.

## Resuming a session

When starting a new session in a repo that has handoff files, read the **most recent file**
in this folder before doing anything else. The handoff file is the source of truth for
where work left off; do not rely on git history or issue comments alone.

## File format

Each handoff file is produced by `/handoff-conversation` and follows this structure:

- **Metadata block** — date, author agent, task reference (issue number or PRD slug)
- **Current state** — what was completed, what is in progress, what is blocked
- **Next actions** — the exact next steps the resuming agent should take, in order
- **Open questions** — anything that needs human input before proceeding
- **Context dump** — relevant snippets, decisions made, and reasoning that won't be
  obvious from the code or issue tracker alone

Do not hand-edit handoff files after they are written; create a new one via
`/handoff-conversation` if the state has changed.
