import shutil
from pathlib import Path

import openpyxl

from catalyst.tools.macro_applier.macro_runner import MacroSession
from catalyst.tools.macro_applier.tasks import (
    DAILY_REPORT_FORMATTING,
    MAIN_TWITTER,
    TALKWALKER_TRADITIONAL,
)

RAW_EXPORT_SAMPLE = Path(__file__).parent / "fixtures" / "raw_export_sample.xlsx"


def test_applies_the_real_macro_and_saves_the_target_file_in_place(tmp_path):
    target_path = tmp_path / "target.xlsx"
    shutil.copy(RAW_EXPORT_SAMPLE, target_path)

    session = MacroSession(target_path)
    try:
        session.apply(MAIN_TWITTER.path, MAIN_TWITTER.macro_name)
        assert session.target_workbook.Saved
    finally:
        session.close()

    wb = openpyxl.load_workbook(target_path)
    assert "Users" in wb.sheetnames


def test_close_is_safe_to_call_twice(tmp_path):
    target_path = tmp_path / "target.xlsx"
    shutil.copy(RAW_EXPORT_SAMPLE, target_path)

    session = MacroSession(target_path)
    session.apply(MAIN_TWITTER.path, MAIN_TWITTER.macro_name)
    session.close()
    session.close()


def test_a_macro_with_no_dialogs_returns_its_status_and_message_instead_of_popping_a_box(
    tmp_path,
):
    target_path = tmp_path / "target.xlsx"
    shutil.copy(RAW_EXPORT_SAMPLE, target_path)

    session = MacroSession(target_path)
    try:
        result = session.apply(DAILY_REPORT_FORMATTING.path, DAILY_REPORT_FORMATTING.macro_name)
    finally:
        session.close()

    assert result == ("DONE", "Done.")


def test_a_confirmation_macro_previews_without_changing_anything_then_applies_on_confirm(
    tmp_path,
):
    target_path = tmp_path / "target.xlsx"
    shutil.copy(RAW_EXPORT_SAMPLE, target_path)

    session = MacroSession(target_path)
    try:
        status, message = session.apply(
            TALKWALKER_TRADITIONAL.path, TALKWALKER_TRADITIONAL.macro_name, False
        )
        assert status == "CONFIRM"
        assert "Continue?" in message
        session.target_workbook.Save()

        wb = openpyxl.load_workbook(target_path, read_only=True)
        assert "Budget" not in wb.sheetnames
        assert wb.active["A1"].value == "url"
        wb.close()

        status, message = session.apply(
            TALKWALKER_TRADITIONAL.path, TALKWALKER_TRADITIONAL.macro_name, True
        )
        assert status == "DONE"
        assert "converted successfully" in message
    finally:
        session.close()

    wb = openpyxl.load_workbook(target_path)
    assert "Budget" in wb.sheetnames
