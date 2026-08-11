import faulthandler
from pathlib import Path

import pywintypes
import win32com.client


def _clean_message(exc: Exception) -> str:
    """Excel's own COM errors bury a human-readable message inside an
    otherwise unreadable exception repr; surface just that part."""
    if isinstance(exc, pywintypes.com_error) and exc.excepinfo and exc.excepinfo[2]:
        return exc.excepinfo[2].strip()
    return str(exc)


class MacroSession:
    """A target workbook open in a visible Excel instance.

    Stays open across however many macros get applied to it, so the file
    the user is working on doesn't disappear from under them after a save.
    A macro that raises tears the whole session down (closes everything,
    quits Excel). A macro that reports its own failure via
    Array("ERROR", ...) instead reloads the target workbook from its last
    saved state and keeps the session open - the file is never left
    reflecting a partial run either way.
    """

    def __init__(self, target_path):
        self.target_path = Path(target_path).resolve()
        self.excel = None
        self.target_workbook = None
        self._check_not_locked(self.target_path)

        # DispatchEx (not Dispatch) forces a brand-new Excel process. Plain
        # Dispatch attaches to whatever Excel.Application is already running
        # via the ROT, so a second session's close()/Quit() would take down
        # the first session's still-open file too.
        self.excel = win32com.client.DispatchEx("Excel.Application")
        self.excel.Visible = True
        # Without this, Excel may quit itself once the last COM reference to
        # it is released, even though it's visible with a workbook open.
        self.excel.UserControl = True
        try:
            self.target_workbook = self.excel.Workbooks.Open(str(self.target_path))
        except Exception as exc:
            self._quit_excel()
            raise RuntimeError(_clean_message(exc)) from exc

    @staticmethod
    def _check_not_locked(path: Path) -> None:
        # Excel's own COM automation doesn't reliably fail up front when a
        # target file is already open elsewhere - a second Excel process can
        # silently open it too, risking a clobbered save later. A plain OS
        # file handle catches the lock immediately and cleanly instead.
        try:
            with open(path, "r+b"):
                pass
        except OSError as exc:
            raise RuntimeError(
                f"{path.name} is currently open in another program. Close it and try again."
            ) from exc

    def apply(self, macro_path, macro_name: str, *args):
        macro_path = Path(macro_path).resolve()
        # Suppresses Excel's own confirmation popups (format-mismatch
        # warnings, "keep macros?" prompts, etc.) for exactly this
        # automated run - anything not already handled by the
        # Array(status, message) protocol would otherwise block forever
        # under unattended automation. Scoped to just this call and always
        # restored below: left False for the whole visible session, it also
        # suppresses Excel's native "save changes?" prompt, silently
        # discarding any edits the user makes by hand afterward whenever
        # they close the workbook without an explicit save.
        self.excel.DisplayAlerts = False
        try:
            try:
                macro_workbook = self.excel.Workbooks.Open(str(macro_path))
            except Exception as exc:
                self.close()
                raise RuntimeError(_clean_message(exc)) from exc

            try:
                self.target_workbook.Activate()
                result = self.excel.Application.Run(f"'{macro_path.name}'!{macro_name}", *args)
            except Exception as exc:
                macro_workbook.Close(False)
                self.close()
                raise RuntimeError(_clean_message(exc)) from exc

            status = result[0] if isinstance(result, tuple) else None
            if status == "ERROR":
                # The macro reported its own failure without raising. Discard
                # whatever it mutated in memory and reload from the last saved
                # state, so neither the file on disk nor the open window shows
                # a partial run.
                self.target_workbook.Close(False)
                self.target_workbook = self.excel.Workbooks.Open(str(self.target_path))
            elif status != "CONFIRM":
                self.target_workbook.Save()

            macro_workbook.Close(False)
            self.target_workbook.Activate()
            return result
        finally:
            if self.excel is not None:
                self.excel.DisplayAlerts = True

    def close(self) -> None:
        if self.excel is None:
            return
        target_workbook = self.target_workbook
        self.target_workbook = None
        if target_workbook is not None:
            target_workbook.Close(False)
            del target_workbook
        self._quit_excel()

    def _quit_excel(self) -> None:
        excel = self.excel
        self.excel = None
        # See pdf_exporter.export_to_pdf for why faulthandler must be
        # suppressed around Quit() and the local COM references dropped
        # explicitly inside that window.
        was_enabled = faulthandler.is_enabled()
        faulthandler.disable()
        try:
            excel.Quit()
        finally:
            del excel
            if was_enabled:
                faulthandler.enable()
