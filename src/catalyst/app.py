import customtkinter as ctk

from catalyst.tool_registry import build_registry


class CatalystApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Catalyst")
        self.geometry("500x400")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.tools = build_registry(daily_report_open=self.open_daily_report_generator)
        self.show_home()

    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_home(self):
        self._clear_container()
        ctk.CTkLabel(self.container, text="Catalyst", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        for tool in self.tools:
            ctk.CTkButton(self.container, text=tool.name, command=tool.open).pack(pady=10)

    def open_daily_report_generator(self):
        from catalyst.tools.daily_report.screen import DailyReportScreen

        self._clear_container()
        DailyReportScreen(self.container, on_back=self.show_home).pack(fill="both", expand=True)


def main():
    app = CatalystApp()
    app.mainloop()


if __name__ == "__main__":
    main()
