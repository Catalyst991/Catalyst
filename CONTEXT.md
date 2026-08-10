# Catalyst

Catalyst is a standalone toolbox application. It opens to a home screen listing available Tools; the first Tool is the Daily Report Generator, which turns a daily export of social media monitoring data into a fixed-format PowerPoint presentation and PDF.

## Language

**Catalyst**:
The standalone toolbox application itself — opens to a home screen listing available Tools.
_Avoid_: The app, the program

**Tool**:
A single feature accessible from Catalyst's home screen (e.g. the Daily Report Generator). New capabilities are added as new Tools, not as changes to existing ones.
_Avoid_: Feature, module

### Daily Report Generator

**Comment**:
One row of monitoring data — a public social media post or reply that mentions the monitored account, along with its author, link, country, follower count, and tone. Specific to the Daily Report Generator Tool.
_Avoid_: Mention, post, entry

### Macro Applier

**Task**:
A named unit of work the user picks from Macro Applier's dropdown (e.g. "Standard Workflow," "Just Social"). Each **Task** is an ordered list of one or more **Macros**, shown to the user as numbered, labeled buttons — one per **Macro**, in sequence. Clicking a button applies that one **Macro** to the **Target file**; the user triggers each step themselves, in whatever order they choose (typically the numbered order). Some Tasks are a single **Macro** (one button); others chain several.
_Avoid_: Application (clashes with "Catalyst" itself being an application), Workflow, Job

**Macro**:
A named VBA routine, provided by the user, that transforms whichever Excel file is currently open in the same Excel session. Never selected directly — always run as one step of a **Task**.
_Avoid_: Script, macro file (the macro is the routine; see **Macro file** for where it lives)

**Macro file**:
The `.xlsm` workbook holding one **Macro**'s VBA code. Bundled into Catalyst; identified internally by filename, but not shown to the user directly — the **Task** name is what appears in the dropdown.
_Avoid_: Template, macro

**Target file**:
The Excel file the user uploads to Macro Applier for a chosen **Task** to run against. Each **Macro** in the **Task** modifies it in place, one at a time, in order.
_Avoid_: Uploaded file, input file, data file

## Relationships

- **Catalyst** hosts one or more **Tools**
- The **Daily Report Generator** is a **Tool** that reads **Comments** from an Excel file
- **Macro Applier** is a **Tool** that runs a **Task** against a **Target file**
- A **Task** is an ordered list of one or more **Macros**
- Each **Macro** lives in its own **Macro file**, bundled into Catalyst
- A **Task** modifies its **Target file** one **Macro** at a time, as the user clicks each **Macro**'s button; each click saves the **Target file** in place only if that **Macro** succeeds, leaving it unchanged if it fails — there is no automatic chaining from one **Macro** to the next
