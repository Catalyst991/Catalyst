# Catalyst

Catalyst is a Windows toolbox app for the report-generation tasks a team does by hand today. It opens to a home screen listing available **Tools**:

- **Daily Report Generator** — turns a daily social-media-monitoring Excel export into a formatted PowerPoint and/or PDF report.
- **Macro Applier** — pick an Excel file and a Task, then apply that Task's bundled macros to it with one click each, via real Excel automation.

## For end users

If you just want to run Catalyst, you don't need this source code — grab `CatalystSetup.exe` from the [latest release](https://github.com/Catalyst991/Catalyst/releases/latest), run it, and follow the installer. It installs with no admin rights required, adds a Start Menu entry and optional Desktop shortcut, and can be removed later from **Start Menu → Catalyst → Uninstall Catalyst** or **Settings → Apps**.

The installer isn't code-signed, so Windows will likely show a "Windows protected your PC" SmartScreen warning the first time you run it. Click **More info**, then **Run anyway** to continue — this is expected.

**Requirements:**
- Macro Applier needs **Microsoft Excel** installed — it applies macros via Excel automation.
- Daily Report Generator's PDF export option needs **Microsoft PowerPoint** installed — it drives PowerPoint's own "Save As PDF" rather than bundling a separate PDF engine. Generating a PowerPoint-only report doesn't need PowerPoint.

## For developers

```bash
pip install -r requirements-dev.txt
python run.py
```

Run the tests:

```bash
python -m pytest
```

### Building a standalone .exe

```bash
pyinstaller --noconfirm --clean Catalyst.spec
```

### Building the installer

Requires [Inno Setup](https://jrsoftware.org/isinfo.php). Build the app first (above), then:

```bash
cd installer
ISCC Catalyst.iss
```

The finished installer lands in `installer/output/CatalystSetup.exe`.

## Project layout

- `src/catalyst/` — application source (`app.py` is the home-screen shell; each Tool lives under `src/catalyst/tools/`)
- `tests/` — mirrors `src/`
- `docs/` — domain glossary (`CONTEXT.md`), architecture decisions (`docs/adr/`), and the agent-driven development workflow this project uses (`docs/agents/`)
- `installer/` — the Inno Setup installer script
