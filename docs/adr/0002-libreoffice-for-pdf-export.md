---
status: superseded by ADR-0003
---

# Use LibreOffice (headless) for PowerPoint-to-PDF conversion

**Superseded by ADR-0003** — this assumed the app might run on a PC without Microsoft Office. The user clarified the app is meant to run on PCs that already have Microsoft Office installed, which removes the rationale for a separate free tool and makes native PowerPoint automation strictly better (no new install, better fidelity). Kept here for the record of why LibreOffice was considered.

Converting the finished PowerPoint into a PDF needs a real rendering engine — there's no reliable way to do this from pure Python alone. Neither Microsoft PowerPoint nor LibreOffice was found installed on the target PC, so either option requires a new install. We chose **LibreOffice**, run headlessly (`soffice --headless --convert-to pdf`), over Microsoft PowerPoint automation, because it's free and open-source with no subscription or licensing cost, keeps conversion entirely local (nothing leaves the PC), and gives fidelity close enough to PowerPoint's own export for this use case. The trade-off is a large one-time install and occasional minor rendering differences (fonts/spacing) versus what PowerPoint itself would produce.
