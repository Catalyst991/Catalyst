from unittest.mock import MagicMock

import customtkinter as ctk
import openpyxl
import pytest

from catalyst.tools.daily_report.screen import DailyReportScreen


@pytest.fixture(scope="module")
def root():
    instance = ctk.CTk()
    yield instance
    instance.destroy()


def test_shows_the_exact_validation_message_without_wrapping_it(root, tmp_path, monkeypatch):
    wb = openpyxl.Workbook()
    wb.active.title = "Official"
    excel_path = tmp_path / "export.xlsx"
    wb.save(excel_path)
    save_directory = tmp_path / "reports"
    save_directory.mkdir()

    screen = DailyReportScreen(root, on_back=lambda: None)
    screen.excel_path = excel_path
    monkeypatch.setattr(
        "catalyst.tools.daily_report.screen.filedialog.askdirectory",
        lambda **kwargs: str(save_directory),
    )
    shown = MagicMock()
    monkeypatch.setattr("catalyst.tools.daily_report.screen.messagebox.showerror", shown)

    screen.generate()

    shown.assert_called_once_with(
        "Catalyst",
        "This file doesn't have a 'Users' sheet with the expected data — please check the file and try again.",
    )
    assert list(save_directory.iterdir()) == []
