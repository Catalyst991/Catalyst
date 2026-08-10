# Handoff — Macro Applier: PRD approved, 3 slices published, nothing committed yet

## Metadata
- Date: 2026-08-10
- Branch: `macro-applier` (created off `master`, at commit `db098d7` — nothing new committed on this branch yet)
- Task reference: [PRD-002: Macro Applier (#6)](https://github.com/Catalyst991/Catalyst/issues/6)

## Current state

### Completed this session
1. **Window-centering task — abandoned, rolled back.** Tried twice to center the main window on launch (first using primary-monitor `GetSystemMetrics`, then fixing a `customtkinter` DPI-scaling interaction). User reported it still didn't work; rather than debug further, rolled `master` back to `db098d7` via `git reset --hard` (safe — commits were local/unpushed). **No trace of this remains in the code.** If resumed later, start fresh — don't reuse the abandoned approach without re-verifying against the user's actual multi-monitor/DPI setup, which was never directly observed.
2. **Handoff cleanup.** Per user request, scrubbed the parked "social media extractor" and "logo redesign" topics out of the previous handoff doc (`docs/agents/handoffs/2026-08-09-theme-toggle-handoff.md`, renamed from a longer filename) — both topics are now fully gone from the repo (never existed in `CONTEXT.md`/ADRs anyway). That file is **still untracked/uncommitted** — see Next actions.
3. **New Tool scoped end-to-end: Macro Applier.** Ran the full `/grill-with-docs` → `/to-prd` → `/to-issues` pipeline. The tool's shape changed twice mid-conversation as the user refined the idea — both pivots are already folded into the final PRD, not left as stale history to reconcile:
   - v1: pick one macro from a dropdown, apply it, overwrite the target file in place.
   - v2: pick a **Task** (a named, ordered list of macros) from the dropdown; Catalyst *automatically* chains and saves each step.
   - v3 (final, what got built): Catalyst does **not** auto-chain. Selecting a Task renders one numbered, labeled button per macro; each button is independently clickable and runs that one macro (via the same COM-automation mechanism throughout: open macro file + target file, run, save in place, close) whenever the user clicks it, in whatever order they choose.
4. **`CONTEXT.md` updated** with the `### Macro Applier` subheading (terms: **Task**, **Macro**, **Macro file**, **Target file**) — reflects the final (v3) design. **Uncommitted.**
5. **4 real macro files bundled** at `src/catalyst/tools/macro_applier/assets/`: `Main Twitter.xlsm`, `Talkwalker Traditional.xlsm`, `Social File Arrangement.xlsm`, `Daily Report Formatting.xlsm` (renamed from the user's originals — `Daily Report Formatting` was deliberately renamed from "Daily report" to avoid colliding with the existing "Daily Report Generator" Tool name). **Uncommitted.**
6. **PRD-002 published and iterated 3 times** as the design changed — final version is the single source of truth, includes the confirmed Task→macro registry table (§7):

   | Task | Macros, in order |
   |------|-------------------|
   | Standard Workflow | 1. Main Twitter · 2. Social File Arrangement |
   | Daily Report Excel File | 1. Main Twitter · 2. Daily Report Formatting |
   | Traditional Talkwalker | 1. Talkwalker Traditional |
   | Just Social | 1. Main Twitter |

7. **3 build-ready slices published**, all `ready-for-agent`, each with a full agent brief:
   - [#7 — Slice 1: Home screen entry + single-macro Task, end to end](https://github.com/Catalyst991/Catalyst/issues/7) — no dependencies, can start immediately.
   - [#8 — Slice 2: Multi-macro Tasks — numbered, independently-clickable buttons](https://github.com/Catalyst991/Catalyst/issues/8) — blocked by #7.
   - [#9 — Slice 3: Failure isolation and guard rails](https://github.com/Catalyst991/Catalyst/issues/9) — blocked by #7.

## Next actions

1. **Nothing is committed yet.** `git status` on `macro-applier` currently shows: `CONTEXT.md` modified, `src/catalyst/tools/macro_applier/` untracked (the 4 macro assets), and `docs/agents/handoffs/2026-08-09-theme-toggle-handoff.md` untracked (unrelated leftover from the prior session — never got committed then either). Before starting Slice 1, either commit `CONTEXT.md` + the macro assets to `macro-applier` (recommended — they're real inputs Slice 1 depends on), or at minimum confirm they're still present before building against them.
2. **Start Slice 1** (#7) via `/tdd` — it's explicitly written to be picked up standalone; it references the parent PRD for shared context rather than needing this conversation's history.
3. Slices 2 and 3 follow once #7 merges — both only depend on #7, not each other.

## Open questions

Three non-blocking P1 items logged in PRD-002 §12, worth resolving whenever convenient (none block Slice 1–3 work):
- Should **"Daily Report Excel File"** be renamed? It reads close to both "Daily Report Generator" (existing Tool) and "Daily Report Formatting" (its own macro).
- Should the Target file be restricted to `.xlsx`, or should `.xlsm` targets (files that already have their own macros) also be accepted?
- Exact user-facing wording for the "file locked" and "macro file missing" edge cases (placeholder wording exists; not yet confirmed with the user).

## Suggested Skills
- `/tdd` — to build Slice 1 (#7) test-first, per its brief.
- `/to-issues` context is already fully consumed — no need to re-run grilling or PRD work for Macro Applier unless the scope changes again.

## Context dump
- **Branching convention** (established this session, applies going forward): every Tool/feature gets a short-lived branch off `master`, implemented + tested there, merged back via `--no-ff`, branch deleted. Empty branches (no commits) get deleted without merging. `macro-applier` is the active branch for this work.
- **Testing philosophy for this repo**: COM automation (Excel/PowerPoint) is tested against the *real* application in tests, never mocked — see `tests/tools/daily_report/test_pdf_exporter.py` for the existing precedent. Slice 1–3's agent briefs all point back to this.
- The Daily Report Generator's `screen.py` / `pipeline.py` / `pdf_exporter.py` are the direct structural reference for how Macro Applier's screen and COM lifecycle should look — cited explicitly in the PRD and all 3 slice briefs.
