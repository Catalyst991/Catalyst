import customtkinter as ctk
import pytest

from catalyst.app import CatalystApp


@pytest.fixture(scope="module")
def app():
    instance = CatalystApp()
    yield instance
    instance.destroy()


@pytest.fixture(autouse=True)
def reset_app(app):
    app.show_home()


def _buttons(widget):
    found = []
    for child in widget.winfo_children():
        if isinstance(child, ctk.CTkButton):
            found.append(child)
        found.extend(_buttons(child))
    return found


def test_home_screen_lists_daily_report_generator(app):
    button_texts = [b.cget("text") for b in _buttons(app.container)]
    assert "Daily Report Generator" in button_texts


def test_selecting_daily_report_generator_opens_its_screen(app):
    button = next(b for b in _buttons(app.container) if b.cget("text") == "Daily Report Generator")

    button.cget("command")()

    from catalyst.tools.daily_report.screen import DailyReportScreen

    assert any(isinstance(child, DailyReportScreen) for child in app.container.winfo_children())
