import customtkinter as ctk
import pytest

from catalyst.app import CatalystApp


@pytest.fixture(scope="module")
def app():
    instance = CatalystApp()
    yield instance
    instance.destroy()


@pytest.fixture(autouse=True)
def reset_app(app, monkeypatch, tmp_path):
    from catalyst.ui import theme

    monkeypatch.setattr(theme, "_SETTINGS_PATH", tmp_path / "settings.json")
    app.show_home()


def _buttons(widget):
    found = []
    for child in widget.winfo_children():
        if isinstance(child, ctk.CTkButton):
            found.append(child)
        found.extend(_buttons(child))
    return found


def test_home_screen_lists_daily_report_generator(app):
    button_texts = [b.cget("text") for b in _buttons(app)]
    assert any("Daily Report Generator" in text for text in button_texts)


def test_selecting_daily_report_generator_opens_its_screen(app):
    button = next(b for b in _buttons(app) if "Daily Report Generator" in b.cget("text"))

    button.cget("command")()

    from catalyst.tools.daily_report.screen import DailyReportScreen

    assert any(isinstance(child, DailyReportScreen) for child in app.container.winfo_children())


def test_toggling_theme_switches_mode_and_rebuilds_sidebar(app):
    from catalyst.ui import theme

    original_mode = theme.get_mode()
    try:
        old_sidebar = app.sidebar

        app.set_theme_mode("light" if original_mode == "dark" else "dark")

        assert theme.get_mode() != original_mode
        assert app.sidebar is not old_sidebar
        assert not old_sidebar.winfo_exists()
    finally:
        app.set_theme_mode(original_mode)


def test_toggling_theme_preserves_the_active_view(app):
    from catalyst.tools.daily_report.screen import DailyReportScreen
    from catalyst.ui import theme

    original_mode = theme.get_mode()
    button = next(b for b in _buttons(app) if "Daily Report Generator" in b.cget("text"))
    button.cget("command")()

    try:
        app.set_theme_mode("light" if original_mode == "dark" else "dark")

        assert any(
            isinstance(child, DailyReportScreen) for child in app.container.winfo_children()
        )
    finally:
        app.set_theme_mode(original_mode)
