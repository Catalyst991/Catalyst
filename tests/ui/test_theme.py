import json

import pytest

from catalyst.ui import theme


@pytest.fixture(autouse=True)
def restore_mode(monkeypatch, tmp_path):
    monkeypatch.setattr(theme, "_SETTINGS_PATH", tmp_path / "settings.json")
    original_mode = theme.get_mode()
    yield
    theme.set_mode(original_mode)


def test_toggle_mode_flips_between_light_and_dark():
    theme.set_mode("dark")

    assert theme.toggle_mode() == "light"
    assert theme.toggle_mode() == "dark"


def test_set_mode_swaps_palette_values():
    theme.set_mode("dark")
    dark_bg = theme.BG_APP

    theme.set_mode("light")

    assert theme.BG_APP != dark_bg
    assert theme.get_mode() == "light"


def test_set_mode_rejects_unknown_mode():
    with pytest.raises(ValueError):
        theme.set_mode("purple")


def test_set_mode_persists_choice_to_disk():
    theme.set_mode("light")

    saved = json.loads(theme._SETTINGS_PATH.read_text())
    assert saved["theme_mode"] == "light"


def test_accent_colors_are_mode_independent():
    theme.set_mode("dark")
    dark_accent = theme.ACCENT

    theme.set_mode("light")

    assert theme.ACCENT == dark_accent
