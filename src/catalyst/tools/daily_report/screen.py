from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from catalyst.tools.daily_report.pipeline import generate_report

TEMPLATE_PATH = Path(__file__).parent / "assets" / "template.pptx"


class DailyReportScreen(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.on_back = on_back
        self.excel_path: Path | None = None

        ctk.CTkButton(self, text="< Back", command=self.on_back).pack(anchor="w", padx=10, pady=10)
        ctk.CTkLabel(self, text="Daily Report Generator", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        self.file_label = ctk.CTkLabel(self, text="No Excel file selected")
        self.file_label.pack(pady=5)
        ctk.CTkButton(self, text="Select Excel File", command=self.select_excel_file).pack(pady=5)
        ctk.CTkButton(self, text="Generate", command=self.generate).pack(pady=15)

    def select_excel_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.excel_path = Path(path)
            self.file_label.configure(text=self.excel_path.name)

    def generate(self):
        if self.excel_path is None:
            messagebox.showerror("Catalyst", "Please select an Excel file first.")
            return

        save_directory = filedialog.askdirectory(title="Choose where to save the report")
        if not save_directory:
            return

        try:
            save_path = generate_report(
                excel_path=self.excel_path,
                template_path=TEMPLATE_PATH,
                save_directory=save_directory,
            )
        except Exception as exc:
            messagebox.showerror("Catalyst", f"Couldn't generate the report:\n{exc}")
            return

        messagebox.showinfo("Catalyst", f"Report saved:\n{save_path}")
