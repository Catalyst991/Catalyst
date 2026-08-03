# Handoff: Slice 1 built and working, nothing committed yet

**Date:** 2026-08-03
**Repo:** `Catalyst991/Catalyst` on GitHub

## Who this user is

Complete beginner in software development — no assumed knowledge of git, repositories, issue trackers, frameworks, package managers, or terminals. Explain every decision and action in plain language. This preference has held across sessions and should carry forward. See the prior handoff (`2026-08-03-catalyst-planning-handoff.md`) for the same note.

## What happened this session

Built Slice 1 ([#2](https://github.com/Catalyst991/Catalyst/issues/2) — Catalyst home screen + core pipeline) test-first via `/tdd`, then spent most of the session chasing down real formatting bugs in the generated PowerPoint output that only showed up when checked against the user's real files. **The user confirmed the final output is correct** ("perfect") at the end of this session.

### Code built (all committed to disk, none committed to git yet)

- `src/catalyst/app.py` — Catalyst's home screen (CustomTkinter), lists Tools, currently just "Daily Report Generator"
- `src/catalyst/tool_registry.py` — testable list-of-Tools data model, decoupled from the actual Tkinter widgets (per ADR-0004)
- `src/catalyst/tools/daily_report/`:
  - `truncate.py` — 90-char + "..." truncation helper
  - `excel_reader.py` — reads/validates the "Users" sheet into `Comment` records, ignores "Official" sheet, skips blank trailing rows
  - `report_builder.py` — fills Start/Content/End slides from the template; this is where nearly all the bug-fixing happened (see below)
  - `pipeline.py` — `generate_report(excel_path, template_path, save_directory, generation_date=None)`, the full seam-to-seam function; derives the output filename from the title slide text (not user-typed)
  - `screen.py` — the Tool's own CustomTkinter screen (file picker → Generate → save-folder picker)
  - `assets/template.pptx` — the **blank template asset**, derived from the user's real filled example (`تقرير الرصد اليومي – 25 مايو.pptx`): extra Content slides removed, data rows cleared, fonts fixed (see below)
- `run.py` — simple launcher (`python run.py`) so the user doesn't need to know about `PYTHONPATH` or packaging
- `tests/` — 23 tests, all passing, mirroring the `src/` structure; `conftest.py` under `tests/tools/daily_report/` builds a synthetic template fixture in-code (not a committed binary) with deliberately realistic quirks (multi-run title text, custom fonts) so regression tests actually exercise real bugs
- `requirements.txt` / `requirements-dev.txt`, `pyproject.toml` (pytest config, `pythonpath = ["src"]`)

### The bug chain (in order found — useful context for why the code looks the way it does)

1. **Formatting wiped on every write.** python-pptx's `cell.text = value` / `text_frame.text = value` replaces the whole paragraph, destroying any existing run-level font/size/color. Fixed by explicitly re-applying captured per-column styles (`COLUMN_STYLES` in `report_builder.py`) after every write, and by mutating existing runs' `.text` (not replacing the paragraph) for the title.
2. **Title text is split across two runs** in the real file (PowerPoint's own bidi handling of the embedded "25" digit inside Arabic text). Fixing #1 for the title required merging into whichever run contains "–" and blanking the rest, not just touching `runs[0]`.
3. **Row height / font size "not fixed."** Initially over-corrected by disabling word-wrap and autofit — this was **wrong**. A full scan of the real file (every cell, all 3 original content slides) showed the source template never disables wrap/autofit; it just makes rows generously tall (~50pt) so wrapped text never needs to grow the row. Reverted to match; this is the current, correct behavior.
4. **Missing hyperlinks.** The real file's Link column cells have live hyperlinks (`run.hyperlink.address`). Initially assumed unsafe to replicate — it isn't; python-pptx manages the relationship correctly. Now added.
5. **Fonts not installed.** The real template's fonts (`Montserrat`, `Montserrat (Body)`, `DIN Next LT Arabic`, `DIN Next LT Arabic Medium`) — including the **theme's own default font** — are not installed on this PC at all (confirmed via `System.Drawing.Text.InstalledFontCollection`, 269 families, zero matches). PowerPoint was silently substituting fallback fonts on every render, which no XML-level fix could address. **User explicitly chose** (via AskUserQuestion) to switch the template to fonts that are actually installed rather than install/source the originals. Replaced with **Segoe UI** (body) / **Segoe UI Semibold** (title), updated both the code (`FONT_NAME` in `report_builder.py`) and the template asset's baked-in title/end-slide runs and theme (`ppt/theme/theme1.xml` inside `assets/template.pptx`).
6. **Embedded newlines in source data.** One row in the user's real Excel export has literal `\n` characters inside "User name" and "Comment" (human-typed multi-line tweet text). python-pptx splits text containing `\n` into separate paragraphs on `cell.text = value`, and only `paragraphs[0]` was getting styled — the rest inherited default (wrong) formatting and broke that row's height. Fixed with a `_normalize_whitespace()` helper (collapses all whitespace, including newlines, to single spaces) applied before truncation/insertion for every text field.

**Lesson for future work on this Tool:** don't trust "looks correct" from the synthetic test fixtures alone — the real bugs only appeared with the user's actual data and only became visible by exhaustively scanning the real file's XML (every cell, all slides) and cross-checking installed fonts, not by spot-checking one cell.

## Current state

- All 23 tests pass (`python -m pytest` from repo root).
- The user confirmed the final generated file (from their real Excel export) looks correct.
- **Nothing has been committed to git yet** — `git status` shows everything from this session as untracked/modified.
- Issue [#2](https://github.com/Catalyst991/Catalyst/issues/2) has NOT been marked done/closed yet.

## Immediate next steps

1. **Commit this work.** Nothing has been committed — the user should confirm they want a commit (they were asked and picked "run handoff" instead, so this is still open). Consider whether `assets/template.pptx` (binary) should be committed — it contains no personal data (cleared), only the user's real template's structure/branding, so it should be fine to commit, unlike the raw sample Excel/pptx files which stay local per the PRD's own notes.
2. Decide whether to mark issue #2 as done, given the user said "perfect" but the completion wasn't formally confirmed against every acceptance criterion line-by-line since the font/formatting detour absorbed most of the session.
3. Next slice to pick up: [#3 — Reject a mismatched Excel file](https://github.com/Catalyst991/Catalyst/issues/3) (no dependencies) or [#5 — Slice 2: multiple content slides](https://github.com/Catalyst991/Catalyst/issues/5) (blocked by #2, now unblocked).

## Open questions (non-blocking, carried over)

- PRD-001 §12: zero-Comment edge case (Start+End only, or refuse?) — still unanswered, still P1/non-blocking.

## Suggested Skills

- `/session-report` — running automatically right after this handoff
- `/tdd` — for Slice 2 or Slice 3 next
- If committing: plain `git add` / `git commit` (user will need this explained step-by-step, per their beginner status)
