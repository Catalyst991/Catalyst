import datetime

import openpyxl
import pytest
from pptx import Presentation

from catalyst.tools.daily_report.excel_reader import MissingSheetError
from catalyst.tools.daily_report.pipeline import generate_report

TABLE_HEADERS = ["Date", "User name", "Comment", "Link", "Country", "No. of Followers", "النبرة"]


def make_excel(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Users"
    ws.append(TABLE_HEADERS)
    for row in rows:
        ws.append(row)
    wb.save(path)
    return path


def test_generates_a_pptx_file_readable_back_with_correct_contents(tmp_path, template_path):
    excel_path = make_excel(
        tmp_path / "export.xlsx",
        rows=[
            [datetime.date(2026, 7, 27), "Design Studio", "hello world", "https://x.com/1", "KSA", 1296, "محايد"],
        ],
    )
    save_directory = tmp_path / "reports"
    save_directory.mkdir()

    save_path = generate_report(
        excel_path=excel_path,
        template_path=template_path,
        save_directory=save_directory,
        generation_date=datetime.date(2026, 7, 28),
    )

    assert save_path.exists()
    prs = Presentation(save_path)
    assert len(prs.slides) == 3
    table = next(shape.table for shape in prs.slides[1].shapes if shape.has_table)
    assert table.rows[1].cells[1].text == "Design Studio"


def test_writes_no_file_when_the_excel_file_fails_validation(tmp_path, template_path):
    wb = openpyxl.Workbook()
    wb.active.title = "Official"
    excel_path = tmp_path / "export.xlsx"
    wb.save(excel_path)
    save_directory = tmp_path / "reports"
    save_directory.mkdir()

    with pytest.raises(MissingSheetError):
        generate_report(
            excel_path=excel_path,
            template_path=template_path,
            save_directory=save_directory,
            generation_date=datetime.date(2026, 7, 28),
        )

    assert list(save_directory.iterdir()) == []


def test_saved_filename_matches_the_title_slide_text(tmp_path, template_path):
    excel_path = make_excel(
        tmp_path / "export.xlsx",
        rows=[
            [datetime.date(2026, 7, 27), "Design Studio", "hello world", "https://x.com/1", "KSA", 1296, "محايد"],
        ],
    )
    save_directory = tmp_path / "reports"
    save_directory.mkdir()

    save_path = generate_report(
        excel_path=excel_path,
        template_path=template_path,
        save_directory=save_directory,
        generation_date=datetime.date(2026, 7, 28),
    )

    assert save_path.parent == save_directory
    assert save_path.suffix == ".pptx"
    assert save_path.stem == "تقرير الرصد اليومي – 28 يوليو"
