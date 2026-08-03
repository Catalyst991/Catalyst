from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from catalyst.tools.daily_report.excel_reader import ExcelValidationError
from catalyst.tools.daily_report.pipeline import (
    OUTPUT_FORMAT_BOTH,
    OUTPUT_FORMAT_PDF,
    OUTPUT_FORMAT_PPTX,
    generate_report,
)
from catalyst.ui import theme
from catalyst.ui.widgets import Card, OptionGroup, Panel, PrimaryButton, SecondaryButton

TEMPLATE_PATH = Path(__file__).parent / "assets" / "template.pptx"

OUTPUT_FORMAT_LABELS = {
    "PowerPoint only": OUTPUT_FORMAT_PPTX,
    "PDF only": OUTPUT_FORMAT_PDF,
    "Both": OUTPUT_FORMAT_BOTH,
}


def _step_label(master, text: str) -> ctk.CTkLabel:
    return ctk.CTkLabel(
        master,
        text=text.upper(),
        font=theme.font(11, "bold"),
        text_color=theme.TEXT_SECONDARY,
    )


class DailyReportScreen(Panel):
    def __init__(self, master, on_back):
        super().__init__(master, bg=theme.BG_APP)
        self.on_back = on_back
        self.excel_path: Path | None = None

        self._build_header()
        self._build_file_card()
        self._build_format_card()
        self._build_generate_button()

    def _build_header(self):
        back_link = ctk.CTkLabel(
            self,
            text="←  Catalyst",
            font=theme.font_small(),
            text_color=theme.TEXT_SECONDARY,
            cursor="hand2",
        )
        back_link.pack(anchor="w", padx=theme.PAD_XL, pady=(theme.PAD_LG, 0))
        back_link.bind("<Button-1>", lambda _event: self.on_back())

        ctk.CTkLabel(
            self,
            text="Daily Report Generator",
            font=theme.font_title(),
            text_color=theme.TEXT_PRIMARY,
        ).pack(anchor="w", padx=theme.PAD_XL, pady=(theme.PAD_SM, 2))
        ctk.CTkLabel(
            self,
            text="Turn a daily Excel export into a formatted PowerPoint or PDF report.",
            font=theme.font_body(),
            text_color=theme.TEXT_SECONDARY,
        ).pack(anchor="w", padx=theme.PAD_XL, pady=(0, theme.PAD_LG))

    def _build_file_card(self):
        card = Card(self)
        card.pack(fill="x", padx=theme.PAD_XL, pady=(0, theme.PAD_MD))

        inner = Panel(card, bg=theme.BG_SURFACE)
        inner.pack(fill="x", padx=theme.PAD_LG, pady=theme.PAD_LG)
        _step_label(inner, "Step 1 — Excel file").pack(anchor="w", pady=(0, theme.PAD_SM))

        row = Panel(inner, bg=theme.BG_SURFACE)
        row.pack(fill="x")

        info = Panel(row, bg=theme.BG_SURFACE)
        info.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(info, text="📄", font=theme.font(22), text_color=theme.TEXT_SECONDARY).pack(
            side="left", padx=(0, theme.PAD_SM)
        )
        self.file_label = ctk.CTkLabel(
            info,
            text="No Excel file selected",
            font=theme.font_body(),
            text_color=theme.TEXT_SECONDARY,
            anchor="w",
        )
        self.file_label.pack(side="left", fill="x", expand=True)

        SecondaryButton(row, text="Browse files", command=self.select_excel_file, width=130).pack(
            side="right"
        )

    def _build_format_card(self):
        card = Card(self)
        card.pack(fill="x", padx=theme.PAD_XL, pady=(0, theme.PAD_MD))

        inner = Panel(card, bg=theme.BG_SURFACE)
        inner.pack(fill="x", padx=theme.PAD_LG, pady=theme.PAD_LG)
        _step_label(inner, "Step 2 — Output format").pack(anchor="w", pady=(0, theme.PAD_SM))

        self.format_selector = OptionGroup(
            inner,
            bg=theme.BG_SURFACE,
            values=list(OUTPUT_FORMAT_LABELS),
            default="PowerPoint only",
        )
        self.format_selector.pack(fill="x")

    def _build_generate_button(self):
        footer = Panel(self, bg=theme.BG_APP)
        footer.pack(fill="x", padx=theme.PAD_XL, pady=(theme.PAD_SM, theme.PAD_XL))
        PrimaryButton(footer, text="Generate Report", command=self.generate).pack(fill="x")

    def select_excel_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.excel_path = Path(path)
            self.file_label.configure(text=self.excel_path.name, text_color=theme.TEXT_PRIMARY)

    def generate(self):
        if self.excel_path is None:
            messagebox.showerror("Catalyst", "Please select an Excel file first.")
            return

        save_directory = filedialog.askdirectory(title="Choose where to save the report")
        if not save_directory:
            return

        output_format = OUTPUT_FORMAT_LABELS[self.format_selector.get()]

        try:
            save_paths = generate_report(
                excel_path=self.excel_path,
                template_path=TEMPLATE_PATH,
                save_directory=save_directory,
                output_format=output_format,
            )
        except ExcelValidationError as exc:
            messagebox.showerror("Catalyst", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("Catalyst", f"Couldn't generate the report:\n{exc}")
            return

        saved_list = "\n".join(str(path) for path in save_paths)
        messagebox.showinfo("Catalyst", f"Report saved:\n{saved_list}")
