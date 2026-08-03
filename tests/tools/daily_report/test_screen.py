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


def test_generate_uses_powerpoint_only_by_default(root, tmp_path, monkeypatch):
    excel_path = tmp_path / "export.xlsx"
    excel_path.touch()
    save_directory = tmp_path / "reports"
    save_directory.mkdir()

    screen = DailyReportScreen(root, on_back=lambda: None)
    screen.excel_path = excel_path
    monkeypatch.setattr(
        "catalyst.tools.daily_report.screen.filedialog.askdirectory",
        lambda **kwargs: str(save_directory),
    )
    generate = MagicMock(return_value=[save_directory / "report.pptx"])
    monkeypatch.setattr("catalyst.tools.daily_report.screen.generate_report", generate)
    monkeypatch.setattr("catalyst.tools.daily_report.screen.messagebox.showinfo", MagicMock())

    screen.generate()

    assert generate.call_args.kwargs["output_format"] == "pptx"


def test_generate_passes_the_selected_output_format(root, tmp_path, monkeypatch):
    excel_path = tmp_path / "export.xlsx"
    excel_path.touch()
    save_directory = tmp_path / "reports"
    save_directory.mkdir()

    screen = DailyReportScreen(root, on_back=lambda: None)
    screen.excel_path = excel_path
    screen.format_selector.set("PDF only")
    monkeypatch.setattr(
        "catalyst.tools.daily_report.screen.filedialog.askdirectory",
        lambda **kwargs: str(save_directory),
    )
    generate = MagicMock(return_value=[save_directory / "report.pdf"])
    monkeypatch.setattr("catalyst.tools.daily_report.screen.generate_report", generate)
    monkeypatch.setattr("catalyst.tools.daily_report.screen.messagebox.showinfo", MagicMock())

    screen.generate()

    assert generate.call_args.kwargs["output_format"] == "pdf"


def test_shows_all_saved_paths_in_the_success_message(root, tmp_path, monkeypatch):
    excel_path = tmp_path / "export.xlsx"
    excel_path.touch()
    save_directory = tmp_path / "reports"
    save_directory.mkdir()
    pptx_path = save_directory / "report.pptx"
    pdf_path = save_directory / "report.pdf"

    screen = DailyReportScreen(root, on_back=lambda: None)
    screen.excel_path = excel_path
    screen.format_selector.set("Both")
    monkeypatch.setattr(
        "catalyst.tools.daily_report.screen.filedialog.askdirectory",
        lambda **kwargs: str(save_directory),
    )
    monkeypatch.setattr(
        "catalyst.tools.daily_report.screen.generate_report",
        MagicMock(return_value=[pptx_path, pdf_path]),
    )
    shown = MagicMock()
    monkeypatch.setattr("catalyst.tools.daily_report.screen.messagebox.showinfo", shown)

    screen.generate()

    message = shown.call_args.args[1]
    assert str(pptx_path) in message
    assert str(pdf_path) in message
