# Catalyst

Catalyst is a Windows toolbox app for the report-generation tasks a team does by hand today. It opens to a home screen listing available **Tools** — the first one is the **Daily Report Generator**, which turns a daily social-media-monitoring Excel export into a formatted PowerPoint and/or PDF report.

## For end users

If you just want to run Catalyst, you don't need this source code — grab `CatalystSetup.exe` from whoever built it, run it, and follow the installer. It installs with no admin rights required, adds a Start Menu entry and optional Desktop shortcut, and can be removed later from **Start Menu → Catalyst → Uninstall Catalyst** or **Settings → Apps**.

Catalyst needs **Microsoft Office (PowerPoint) installed** on the PC for the PDF export feature to work — it drives PowerPoint's own "Save As PDF" rather than bundling a separate PDF engine.

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
pyinstaller --noconfirm --clean --name Catalyst --windowed --onedir ^
  --icon src\catalyst\ui\icon.ico --paths src ^
  --add-data "src\catalyst\tools\daily_report\assets\template.pptx;catalyst\tools\daily_report\assets" ^
  --add-data "src\catalyst\ui\icon.ico;catalyst\ui" ^
  run.py
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
