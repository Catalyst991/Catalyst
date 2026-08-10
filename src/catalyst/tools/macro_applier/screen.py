from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from catalyst.tools.macro_applier.macro_runner import MacroSession
from catalyst.tools.macro_applier.tasks import TASKS
from catalyst.ui import theme
from catalyst.ui.widgets import Card, Dropdown, Panel, PrimaryButton, SecondaryButton


def _step_label(master, text: str) -> ctk.CTkLabel:
    return ctk.CTkLabel(
        master,
        text=text.upper(),
        font=theme.font(11, "bold"),
        text_color=theme.TEXT_SECONDARY,
    )


class MacroApplierScreen(Panel):
    def __init__(self, master, on_back):
        super().__init__(master, bg=theme.BG_APP)
        self.on_back = on_back
        self.target_path: Path | None = None
        self.tasks_by_name = {task.name: task for task in TASKS}
        self.macro_buttons: list[ctk.CTkButton] = []
        self.session: MacroSession | None = None

        self._build_header()
        self._build_file_card()
        self._build_task_card()
        self._on_task_selected(TASKS[0].name)

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
            text="Macro Applier",
            font=theme.font_title(),
            text_color=theme.TEXT_PRIMARY,
        ).pack(anchor="w", padx=theme.PAD_XL, pady=(theme.PAD_SM, 2))
        ctk.CTkLabel(
            self,
            text="Pick a file and a task, then apply each macro with one click.",
            font=theme.font_body(),
            text_color=theme.TEXT_SECONDARY,
        ).pack(anchor="w", padx=theme.PAD_XL, pady=(0, theme.PAD_LG))

    def _build_file_card(self):
        card = Card(self)
        card.pack(fill="x", padx=theme.PAD_XL, pady=(0, theme.PAD_MD))

        inner = Panel(card, bg=theme.BG_SURFACE)
        inner.pack(fill="x", padx=theme.PAD_LG, pady=theme.PAD_LG)
        _step_label(inner, "Step 1 — Target file").pack(anchor="w", pady=(0, theme.PAD_SM))

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

        SecondaryButton(row, text="Browse files", command=self.select_target_file, width=130).pack(
            side="right"
        )

    def _build_task_card(self):
        card = Card(self)
        card.pack(fill="x", padx=theme.PAD_XL, pady=(0, theme.PAD_MD))

        inner = Panel(card, bg=theme.BG_SURFACE)
        inner.pack(fill="x", padx=theme.PAD_LG, pady=theme.PAD_LG)
        _step_label(inner, "Step 2 — Task").pack(anchor="w", pady=(0, theme.PAD_SM))

        self.task_dropdown = Dropdown(
            inner,
            values=[task.name for task in TASKS],
            default=TASKS[0].name,
            command=self._on_task_selected,
        )
        self.task_dropdown.pack(fill="x")

        self.macro_button_row = Panel(inner, bg=theme.BG_SURFACE)
        self.macro_button_row.pack(fill="x", pady=(theme.PAD_SM, 0))

    def _on_task_selected(self, task_name: str):
        for widget in self.macro_button_row.winfo_children():
            widget.destroy()
        self.macro_buttons = []

        task = self.tasks_by_name[task_name]
        for index, macro in enumerate(task.macros, start=1):
            button = PrimaryButton(
                self.macro_button_row,
                text=f"{index}. {macro.name}",
                command=lambda m=macro: self._apply_macro(m),
            )
            button.pack(fill="x", pady=(0 if index == 1 else theme.PAD_SM, 0))
            self.macro_buttons.append(button)

    def _apply_macro(self, macro):
        if self.target_path is None:
            messagebox.showerror("Catalyst", "Please select an Excel file first.")
            return

        target_path = self.target_path.resolve()
        if self.session is None or self.session.target_path != target_path:
            self.session = MacroSession(target_path)
        try:
            if macro.needs_confirmation:
                status, message = self.session.apply(macro.path, macro.macro_name, False)
                if status == "CONFIRM":
                    if not messagebox.askyesno("Catalyst", message):
                        return
                    status, message = self.session.apply(macro.path, macro.macro_name, True)
            else:
                result = self.session.apply(macro.path, macro.macro_name)
                status, message = result if result else ("DONE", None)
        except Exception as exc:
            self.session = None
            messagebox.showerror("Catalyst", f"Couldn't apply {macro.name}:\n{exc}")
            return

        if status == "ERROR":
            messagebox.showerror("Catalyst", f"Couldn't apply {macro.name}:\n{message}")
        elif message:
            messagebox.showinfo("Catalyst", f"{macro.name}\n\n{message}")
        else:
            messagebox.showinfo("Catalyst", f"{macro.name} applied and saved.")

    def select_target_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.target_path = Path(path)
            self.file_label.configure(text=self.target_path.name, text_color=theme.TEXT_PRIMARY)
