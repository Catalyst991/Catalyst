---
status: accepted
---

# Use Microsoft PowerPoint (COM automation) for PowerPoint-to-PDF conversion

Supersedes ADR-0002. ADR-0002 chose LibreOffice because neither Microsoft Office nor LibreOffice was found on the development machine. The user has since clarified that this app is meant to run on PCs that already have Microsoft Office installed — which changes the trade-off entirely. On the actual target machines, Microsoft PowerPoint requires no new install at all, and driving PowerPoint's own COM automation (via the `pywin32` Python library) to open the file and "Save As PDF" gives perfect fidelity, since it's the exact export path a person would trigger manually. LibreOffice is no longer used; requiring it would mean asking users who already own Office to install a second, redundant program just for this app.
