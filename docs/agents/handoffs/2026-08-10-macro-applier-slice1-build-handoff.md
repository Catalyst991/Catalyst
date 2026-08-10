# Handoff — Macro Applier Slice 1: built, live-tested, one real bug found & fixed; still uncommitted

## Metadata
- Date: 2026-08-10
- Branch: `macro-applier` (off `master`)
- Task reference: [PRD-002: Macro Applier (#6)](https://github.com/Catalyst991/Catalyst/issues/6), [Slice 1 (#7)](https://github.com/Catalyst991/Catalyst/issues/7)
- Argument for next session: **"the next session will be used to follow up on this one and all the remaining tasks/requests from me"** — i.e. no new topic, just continue exactly where this one stopped. The user's last message before this handoff was asking whether to commit now or hold off — that question is still open.

## Current state

### Committed on `macro-applier` (2 commits, both landed this session)
1. `22f0445` — `CONTEXT.md` Macro Applier vocabulary (Task/Macro/Macro file/Target file) + fixed a stale naming-convention line in `docs/agents/handoffs/README.md` (it documented `YYYY-MM-DD_<slug>.md`, but every real handoff file — including this one — uses `YYYY-MM-DD-<slug>-handoff.md`).
2. `5c8f604` — the 4 real bundled macro `.xlsm` files under `src/catalyst/tools/macro_applier/assets/`.

### Uncommitted (this session's main work — Slice 1 build, TDD)
- `src/catalyst/tools/macro_applier/tasks.py` (new) — the real Task registry (`TASKS` = all 4 confirmed Tasks from PRD-002 §7), each `Macro` carrying `name`, `macro_name` (the actual VBA Sub to call — **not in the PRD**, discovered this session via `oletools.olevba` since `Application.Run` needs the real Sub name, not the display name), and `path`.
- `src/catalyst/tools/macro_applier/macro_runner.py` (new) — `apply_macro(macro_path, macro_name, target_path)`: real COM automation (open macro + target, activate target, `Application.Run`, save, close), modeled on `pdf_exporter.py`'s `faulthandler`-suppressed `Quit()` pattern. Runs Excel with **`Visible=True`** (a deliberate deviation from the headless PDF-export precedent) because `Talkwalker Traditional`'s macro (`TransformRawToFinal`) pops native `MsgBox` dialogs the user must click through — headless would hang forever.
- `src/catalyst/tools/macro_applier/screen.py` (new) — `MacroApplierScreen`: file picker, Task dropdown, dynamic numbered macro buttons, click-to-apply wiring. Mirrors `DailyReportScreen`'s structure.
- `src/catalyst/tool_registry.py`, `src/catalyst/app.py` — wired in the second Tool (`macro_applier_open`).
- `src/catalyst/ui/widgets.py` — new `Dropdown` widget (see "The dropdown rebuild" below).
- Tests: `tests/tools/macro_applier/test_tasks.py`, `test_macro_runner.py` (real-Excel integration test, no mocking), `test_macro_applier_screen.py` (named to avoid a module-basename collision with `daily_report`'s `test_screen.py` — this repo has no `__init__.py` under `tests/`, so pytest needs unique basenames tree-wide), plus additions to `tests/test_tool_registry.py` and `tests/test_app.py`.
- `tests/tools/macro_applier/fixtures/raw_export_sample.xlsx` — a **sanitized** copy of a real raw-export sample the user provided from `Downloads\Test.xlsx`. Real schema (101 columns) and real values for mechanically-important columns (sentiment, source_type, tags_customer, category codes) preserved; third-party-identifying columns (URLs, post content, author name/handle/bio) replaced with obvious placeholders. Used by the real-COM integration test.
- All 58 tests pass (`python -m pytest -q`).

### The dropdown rebuild (mid-session detour, now resolved)
User asked to clean up the Task dropdown's styling, then asked for a full rounded-corner rebuild (native `CTkOptionMenu`'s popup is backed by `tkinter.Menu` and ignores `corner_radius` entirely — confirmed by reading customtkinter's source). Built a replacement `Dropdown` widget in `ui/widgets.py`: a `CTkFrame` pill that opens a borderless `tk.Toplevel` containing a real rounded `CTkFrame` popup. Mirrors `CTkOptionMenu`'s `.get()`/`.set()`/`cget("values")` interface (same pattern `OptionGroup` already uses), so `screen.py` and all tests needed almost no changes.

**Two real bugs were found and fixed during this rebuild, both only surfaced by live-testing through the actual UI — not by the unit tests**, which don't exercise popup click mechanics:
1. Clicking a popup item raced against a `<FocusOut>`-triggered close (the popup was destroyed mid-click, before the item's own command fired). Fixed by switching to a global `<ButtonRelease-1>` listener with widget-ancestry filtering, dropping the now-unnecessary hover-flag workaround.
2. That fix's first version called `self.bind_all(...)` — but `customtkinter`'s `CTkBaseClass` **raises `AttributeError` on `bind_all`/`unbind_all`** (it reserves the "all" bindtag for its own internals). This silently broke every dropdown selection except the default (the exception was swallowed as a background Tkinter callback error — no crash, just a dropdown that visually looked fine but never actually changed selection). Fixed by routing the global bind through the popup itself, a plain `tk.Toplevel` (not a CTk widget, so unaffected by that guard) — `popup.bind_all(...)` / `popup.unbind_all(...)`.

This second bug was **only found because the user asked me to test with a live file** — the automated tests never drive a real popup click, so this would have shipped broken (Task selection permanently stuck on the default) had testing stopped at "looks right in a screenshot."

### Live-file test (final activity before this handoff)
Copied the user's real sample (`Downloads\Test.xlsx`, never modified — only its `LastAccessTime` moved from an earlier picker interaction, `LastWriteTime`/size untouched) to a scratch location, drove the real app UI end-to-end: browsed to the copy, selected "Just Social," clicked "1. Main Twitter." Confirmed via file diff (15041→15709 bytes) and by re-opening the result with `openpyxl` that the real ~1900-line `Twitter_Macro_Hesham` macro executed its actual transformation correctly (`Users` + `Official` sheets present, column A renamed to "Date" — matching the macro's real column-shuffle logic, not just "no crash"). No orphaned Excel processes.

## Next actions

1. **Answer the open question from the end of the last session**: commit everything now, or hold off? Nothing has been committed since `5c8f604`; all of Slice 1's implementation (tasks.py, macro_runner.py, screen.py, tool_registry/app wiring, the Dropdown widget + both bugfixes, all tests, the fixture) is sitting uncommitted in the working tree.
2. If committing: consider whether to split into logical commits (e.g. Slice 1 implementation as one, the Dropdown rebuild + bugfixes as another) or one commit — no decision was made on this either way.
3. Once committed, Slice 1 (#7) is functionally complete and live-verified — consider whether to open/merge a PR, close #7, or move straight to Slice 2 (#8, multi-macro Tasks — blocked by #7, not by anything else) and Slice 3 (#9, failure isolation).
4. **Known, deliberately out-of-scope gaps** (per Slice 1's brief, owned by Slice 3, not bugs): no guard against clicking a macro button with no Target file selected (will raise uncaught); no "leave file untouched on failure" safety net; no friendly error messages on macro failure. Don't be surprised by these — they're Slice 3's job.
5. Non-blocking PRD §12 open questions (unchanged from prior handoff): "Daily Report Excel File" naming collision, `.xlsm` target-file support, exact edge-case wording.

## Open questions
- Commit now vs. hold — see Next actions #1, this is the literal last thing pending.
- Whether the Dropdown widget's popup-background color choice (`BG_APP`, chosen to minimize the unavoidable-without-Win32-region-masking square-corner seam) needs revisiting if it's ever opened over a lighter card background rather than the screen's own background — untested edge case, low risk given the app is single-theme-per-screen.

## Suggested Skills
- No `/tdd` needed for anything currently in flight — Slice 1's TDD cycle is complete and green. `/tdd` again only once Slice 2 or 3 work starts.
- Plain git commit workflow for Next action #1 — no skill needed, just needs the user's go-ahead on scope/split.

## Context dump
- **Real VBA Sub names** (not in the PRD, had to reverse-engineer via `oletools.olevba` since `Application.Run` needs the exact Sub, not the display name): `Main Twitter.xlsm` → `Twitter_Macro_Hesham` (dialog-free, fully automatable); `Talkwalker Traditional.xlsm` → `TransformRawToFinal` (has blocking `MsgBox` confirmations, needs a human present, cannot be headlessly automated); `Social File Arrangement.xlsm` → `Run_Tags_MoveDelete_ThenConsolidate`; `Daily Report Formatting.xlsm` → `KeepColumns_ACEFSW_SetWidth_AndHyperlinks`. All 4 are wired into `tasks.py`; only the first two were exercised this session (Slice 1 only needed the two single-macro Tasks).
- **Testing philosophy reaffirmed**: real COM, no mocking, per existing repo convention (`test_pdf_exporter.py` precedent) — but scoped `apply_macro`'s real-Excel test to `Twitter_Macro_Hesham` only, since `TransformRawToFinal`'s interactive dialogs make it untestable unattended.
- **A process note for whoever automates UI testing again**: simulated native-dialog interaction (file pickers, `SendKeys`) is fragile — window position isn't stable across relaunches (varies with DPI/monitor state), so pixel coordinates must be recomputed from a fresh `GetWindowRect` each time, not reused. Also: `customtkinter` blocks `bind_all`/`unbind_all` on its own widget classes — route any app-wide event listening through a plain `tk.Toplevel`/`tk.Frame` instead.
- Branching/workflow conventions from the prior handoff still apply unchanged (short-lived branch per Tool, `--no-ff` merge, delete if empty).
