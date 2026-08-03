# Handoff: Catalyst — planning complete, nothing built yet

**Date:** 2026-08-03
**Repo:** `Catalyst991/Catalyst` on GitHub (recently renamed from `Catalyst991/daily-report-generator`)

## Who this user is

Complete beginner in software development — no assumed knowledge of git, repositories, issue trackers, frameworks, package managers, or terminals. **Explain every decision and action in plain language.** This preference has held across the whole session and should carry forward.

## What Catalyst is

A Windows desktop toolbox app. It opens to a home screen listing available **Tools** (see `CONTEXT.md`). The first Tool is the **Daily Report Generator**: takes a user-selected Excel workbook (fixed structure, "Users" sheet only — see `CONTEXT.md`'s **Comment** term) and fills a fixed PowerPoint template with the data, producing a `.pptx` and/or `.pdf`. The user explicitly wants more Tools added to Catalyst over time — this is why the app has a home-screen shell rather than being single-purpose (ADR-0004).

## Current state — planning is done, nothing is built

- Repo-skills setup complete: `CLAUDE.md`, `docs/agents/{issue-tracker,triage-labels,domain,agent-brief}.md`, `docs/agents/handoffs/`
- `CONTEXT.md` has 3 resolved terms: **Catalyst**, **Tool**, **Comment**
- 4 ADRs in `docs/adr/`: 0001 (manual trigger, not scheduled), 0002 (LibreOffice for PDF — **superseded**), 0003 (Microsoft PowerPoint COM automation for PDF export — supersedes 0002, since target PCs already have Office installed), 0004 (Catalyst toolbox shell)
- PRD published: [#1](https://github.com/Catalyst991/Catalyst/issues/1) (`epic` label)
- 4 slices published, all `ready-for-agent`:
  - [#2 — Slice 1: Catalyst home screen + core pipeline](https://github.com/Catalyst991/Catalyst/issues/2) — **no dependencies, start here.** Covers: home screen with tool list, Excel reading/validation happy path, filling Start+1 Content+End slides for ≤7 Comments, saving `.pptx`.
  - [#3 — Slice 3: Reject a mismatched Excel file](https://github.com/Catalyst991/Catalyst/issues/3) — no dependencies, can run in parallel with Slice 1
  - [#5 — Slice 2: Multiple content slides for larger files](https://github.com/Catalyst991/Catalyst/issues/5) — blocked by #2
  - [#4 — Slice 4: PDF export and format choice](https://github.com/Catalyst991/Catalyst/issues/4) — blocked by #2
- **No code exists yet.** Next real step is building Slice 1 (#2) test-first via `/tdd`, per that issue's "Inherited context" section.

## Local machine notes (not in the repo, but relevant)

- Python 3.12 + `openpyxl` + `python-pptx` were installed on this PC (via winget/pip) to inspect the user's sample files during planning. They remain installed.
- The user's real sample files (Excel export and PowerPoint template) are **not in the repo** — held locally by the user in their Downloads folder. Whoever builds Slice 1 will need to ask the user for a fresh copy of the template.
- The local project folder is still named `D:\AI\daily-report-generator` even though the GitHub repo is now `Catalyst`. The user is renaming it manually (outside any active session, since Windows locks a directory that's a running process's cwd) and will launch the next session from the renamed folder.

## Open questions (non-blocking)

- PRD §12: should generating a report with zero Comments produce Start+End slides only, or refuse entirely? Flagged P1, not decided, doesn't block starting Slice 1.

## Suggested next steps / skills

1. Confirm the new session's working directory is the renamed local folder and that `git remote -v` still points at `Catalyst991/Catalyst` (it was already updated, but re-verify given the folder rename happened outside any session).
2. Start building **Slice 1** ([#2](https://github.com/Catalyst991/Catalyst/issues/2)) via `/tdd` — the issue's own "Inherited context" section says to build test-first and inherit the acceptance criteria + PRD §8 seams as the test plan.
3. Slice 3 ([#3](https://github.com/Catalyst991/Catalyst/issues/3)) can be picked up independently/in parallel.

## Suggested Skills

- `/tdd` — to build Slice 1 (and later slices) test-first, red-green-refactor
- `/session-report` — running automatically right after this handoff
