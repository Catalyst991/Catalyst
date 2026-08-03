from pathlib import Path

import customtkinter as ctk

from catalyst.tool_registry import build_registry
from catalyst.ui import theme

SIDEBAR_WIDTH = 230
TOOL_ICON = "▤"
ICON_PATH = Path(__file__).parent / "ui" / "icon.ico"


class CatalystApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        theme.apply()

        self.title("Catalyst")
        self.geometry("980x640")
        self.minsize(760, 520)
        self.configure(fg_color=theme.BG_APP)
        if ICON_PATH.exists():
            self.iconbitmap(ICON_PATH)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tools = build_registry(daily_report_open=self.open_daily_report_generator)
        self._nav_buttons: dict[str, ctk.CTkButton] = {}

        self._build_sidebar()

        self.container = ctk.CTkFrame(self, fg_color=theme.BG_APP, corner_radius=0)
        self.container.grid(row=0, column=1, sticky="nsew")

        self.show_home()

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=theme.BG_SIDEBAR, corner_radius=0, width=SIDEBAR_WIDTH)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        brand = ctk.CTkFrame(sidebar, fg_color="transparent", cursor="hand2")
        brand.pack(fill="x", padx=theme.PAD_LG, pady=(theme.PAD_XL, theme.PAD_LG))
        brand_row = ctk.CTkFrame(brand, fg_color="transparent")
        brand_row.pack(anchor="w")
        brand_mark = ctk.CTkLabel(
            brand_row, text="◆", font=theme.font_title(), text_color=theme.ACCENT
        )
        brand_mark.pack(side="left", padx=(0, 6))
        brand_title = ctk.CTkLabel(
            brand_row, text="Catalyst", font=theme.font_title(), text_color=theme.TEXT_PRIMARY
        )
        brand_title.pack(side="left")
        brand_subtitle = ctk.CTkLabel(
            brand, text="Toolbox", font=theme.font_small(), text_color=theme.TEXT_SECONDARY
        )
        brand_subtitle.pack(anchor="w")
        for widget in (brand, brand_row, brand_mark, brand_title, brand_subtitle):
            widget.bind("<Button-1>", lambda _event: self.show_home())

        divider = ctk.CTkFrame(sidebar, fg_color=theme.BORDER, height=1)
        divider.pack(fill="x", padx=theme.PAD_LG, pady=(0, theme.PAD_MD))

        nav = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav.pack(fill="x", padx=theme.PAD_MD)
        for tool in self.tools:
            button = ctk.CTkButton(
                nav,
                text=f"  {TOOL_ICON}   {tool.name}",
                anchor="w",
                command=tool.open,
                fg_color="transparent",
                hover_color=theme.BG_SURFACE_HOVER,
                text_color=theme.TEXT_PRIMARY,
                font=theme.font_body(),
                corner_radius=theme.RADIUS_MD,
                height=40,
            )
            button.pack(fill="x", pady=2)
            self._nav_buttons[tool.name] = button

    def _set_active_nav(self, active_name: str | None) -> None:
        for name, button in self._nav_buttons.items():
            is_active = name == active_name
            button.configure(
                fg_color=theme.ACCENT_MUTED if is_active else "transparent",
                text_color=theme.ACCENT if is_active else theme.TEXT_PRIMARY,
            )

    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_home(self):
        self._clear_container()
        self._set_active_nav(None)

        empty_state = ctk.CTkFrame(self.container, fg_color="transparent")
        empty_state.place(relx=0.5, rely=0.45, anchor="center")
        ctk.CTkLabel(
            empty_state, text="◇", font=theme.font(48), text_color=theme.TEXT_MUTED
        ).pack(pady=(0, theme.PAD_SM))
        ctk.CTkLabel(
            empty_state,
            text="Select a Tool to get started",
            font=theme.font_heading(),
            text_color=theme.TEXT_PRIMARY,
        ).pack()
        ctk.CTkLabel(
            empty_state,
            text="Choose one from the sidebar on the left.",
            font=theme.font_body(),
            text_color=theme.TEXT_SECONDARY,
        ).pack(pady=(4, 0))

    def open_daily_report_generator(self):
        from catalyst.tools.daily_report.screen import DailyReportScreen

        self._clear_container()
        self._set_active_nav("Daily Report Generator")
        DailyReportScreen(self.container, on_back=self.show_home).pack(fill="both", expand=True)


def main():
    app = CatalystApp()
    app.mainloop()


if __name__ == "__main__":
    main()
