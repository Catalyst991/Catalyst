import re
import shutil
import tempfile
from datetime import date
from pathlib import Path

from catalyst.tools.daily_report.excel_reader import read_comments
from catalyst.tools.daily_report.pdf_exporter import export_to_pdf
from catalyst.tools.daily_report.report_builder import build_report

INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]')

OUTPUT_FORMAT_PPTX = "pptx"
OUTPUT_FORMAT_PDF = "pdf"
OUTPUT_FORMAT_BOTH = "both"


def _derive_filename(prs) -> str:
    for shape in prs.slides[0].shapes:
        if shape.has_text_frame and shape.name == "عنوان 1":
            return INVALID_FILENAME_CHARS.sub("", shape.text_frame.text)
    raise ValueError("no title shape found")


def generate_report(
    excel_path,
    template_path,
    save_directory,
    output_format: str = OUTPUT_FORMAT_PPTX,
    generation_date: date | None = None,
) -> list[Path]:
    generation_date = generation_date or date.today()
    comments = read_comments(excel_path)
    prs = build_report(template_path, comments, generation_date)
    filename = _derive_filename(prs)
    save_directory = Path(save_directory)

    if output_format == OUTPUT_FORMAT_PDF:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_pptx_path = Path(temp_dir) / f"{filename}.pptx"
            prs.save(temp_pptx_path)
            temp_pdf_path = export_to_pdf(temp_pptx_path)
            pdf_path = save_directory / f"{filename}.pdf"
            shutil.move(temp_pdf_path, pdf_path)
        return [pdf_path]

    pptx_path = save_directory / f"{filename}.pptx"
    prs.save(pptx_path)

    if output_format == OUTPUT_FORMAT_PPTX:
        return [pptx_path]

    pdf_path = export_to_pdf(pptx_path)
    return [pptx_path, pdf_path]
