import re
from datetime import date
from pathlib import Path

from catalyst.tools.daily_report.excel_reader import read_comments
from catalyst.tools.daily_report.report_builder import build_report

INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]')


def _derive_filename(prs) -> str:
    for shape in prs.slides[0].shapes:
        if shape.has_text_frame and shape.name == "عنوان 1":
            return INVALID_FILENAME_CHARS.sub("", shape.text_frame.text)
    raise ValueError("no title shape found")


def generate_report(excel_path, template_path, save_directory, generation_date: date | None = None) -> Path:
    generation_date = generation_date or date.today()
    comments = read_comments(excel_path)
    prs = build_report(template_path, comments, generation_date)
    save_path = Path(save_directory) / f"{_derive_filename(prs)}.pptx"
    prs.save(save_path)
    return save_path
