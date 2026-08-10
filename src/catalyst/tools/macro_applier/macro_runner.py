import faulthandler
from pathlib import Path

import win32com.client


class MacroSession:
    """A target workbook open in a visible Excel instance.

    Stays open across however many macros get applied to it, so the file
    the user is working on doesn't disappear from under them after a save.
    Only closes automatically if a macro run fails.
    """

    def __init__(self, target_path):
        self.target_path = Path(target_path).resolve()
        # DispatchEx (not Dispatch) forces a brand-new Excel process. Plain
        # Dispatch attaches to whatever Excel.Application is already running
        # via the ROT, so a second session's close()/Quit() would take down
        # the first session's still-open file too.
        self.excel = win32com.client.DispatchEx("Excel.Application")
        self.excel.Visible = True
        # Without this, Excel may quit itself once the last COM reference to
        # it is released, even though it's visible with a workbook open.
        self.excel.UserControl = True
        self.target_workbook = self.excel.Workbooks.Open(str(self.target_path))

    def apply(self, macro_path, macro_name: str, *args):
        macro_path = Path(macro_path).resolve()
        macro_workbook = self.excel.Workbooks.Open(str(macro_path))
        try:
            self.target_workbook.Activate()
            result = self.excel.Application.Run(f"'{macro_path.name}'!{macro_name}", *args)
            self.target_workbook.Save()
        except Exception:
            macro_workbook.Close(False)
            self.close()
            raise
        macro_workbook.Close(False)
        self.target_workbook.Activate()
        return result

    def close(self) -> None:
        if self.excel is None:
            return
        target_workbook = self.target_workbook
        excel = self.excel
        target_workbook.Close(False)
        # See pdf_exporter.export_to_pdf for why faulthandler must be
        # suppressed around Quit() and the local COM references dropped
        # explicitly inside that window.
        was_enabled = faulthandler.is_enabled()
        faulthandler.disable()
        try:
            excel.Quit()
        finally:
            del target_workbook
            del excel
            self.target_workbook = None
            self.excel = None
            if was_enabled:
                faulthandler.enable()
