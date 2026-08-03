import faulthandler
from pathlib import Path

import win32com.client

PP_SAVE_AS_PDF = 32


def export_to_pdf(pptx_path) -> Path:
    pptx_path = Path(pptx_path).resolve()
    pdf_path = pptx_path.with_suffix(".pdf")

    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    presentation = powerpoint.Presentations.Open(str(pptx_path), True, False, False)
    try:
        presentation.SaveAs(str(pdf_path), PP_SAVE_AS_PDF)
        presentation.Close()
    finally:
        # PowerPoint's process can exit mid-RPC-teardown while releasing these
        # COM proxies, which COM handles internally via its own SEH-based
        # control flow (not a real crash) but which Python's faulthandler
        # still logs as a "fatal exception". The actual Release() happens
        # when the last Python reference is dropped, so the local names must
        # be explicitly deleted inside this suppressed window — letting them
        # go out of scope naturally at function exit releases them too late,
        # after faulthandler is back on.
        was_enabled = faulthandler.is_enabled()
        faulthandler.disable()
        try:
            powerpoint.Quit()
        finally:
            del presentation
            del powerpoint
            if was_enabled:
                faulthandler.enable()

    return pdf_path
