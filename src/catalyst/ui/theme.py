import json
from pathlib import Path

import customtkinter as ctk

FONT_FAMILY = "Segoe UI"

# Brand colors sourced from the Rawnaa logo: a deep teal wordmark/mark with a
# small warm orange accent dot. Teal is the primary interactive color; orange
# is reserved as a small "spark" highlight (mirroring how little of it the
# logo itself uses). Both are mode-independent — only neutrals swap between
# the light and dark palettes below.
ACCENT = "#12726B"
ACCENT_HOVER = "#0E5B56"
ACCENT_SPARK = "#E8592E"
ON_ACCENT = "#FFFFFF"

# Every screen should pull colors from here rather than hardcoding hex
# values, so future Tools stay visually consistent (ADR-0004).
_DARK = dict(
    BG_APP="#12191A",
    BG_SIDEBAR="#0D1315",
    BG_SURFACE="#1B2426",
    BG_SURFACE_HOVER="#232E30",
    BORDER="#2A3436",
    ACCENT_MUTED="#17302E",
    TEXT_PRIMARY="#F2F4F4",
    TEXT_SECONDARY="#8B979A",
    TEXT_MUTED="#5B6668",
    SUCCESS="#4CAF7D",
    ERROR="#E5626B",
)

_LIGHT = dict(
    BG_APP="#F6F8F8",
    BG_SIDEBAR="#EEF3F2",
    BG_SURFACE="#FFFFFF",
    BG_SURFACE_HOVER="#EAF0EF",
    BORDER="#DCE3E2",
    ACCENT_MUTED="#DCEEEC",
    TEXT_PRIMARY="#15211F",
    TEXT_SECONDARY="#54615F",
    TEXT_MUTED="#8B9997",
    SUCCESS="#2F9163",
    ERROR="#C7414B",
)

_PALETTES = {"dark": _DARK, "light": _LIGHT}
_SETTINGS_PATH = Path.home() / ".catalyst" / "settings.json"

RADIUS_SM = 6
RADIUS_MD = 10
RADIUS_LG = 14

PAD_SM = 8
PAD_MD = 16
PAD_LG = 24
PAD_XL = 32


def _load_saved_mode() -> str:
    try:
        saved = json.loads(_SETTINGS_PATH.read_text())["theme_mode"]
    except (OSError, ValueError, KeyError):
        return "dark"
    return saved if saved in _PALETTES else "dark"


def _save_mode(mode: str) -> None:
    try:
        _SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        _SETTINGS_PATH.write_text(json.dumps({"theme_mode": mode}))
    except OSError:
        pass


_mode = _load_saved_mode()
globals().update(_PALETTES[_mode])


def apply() -> None:
    ctk.set_appearance_mode(_mode)
    ctk.set_default_color_theme("dark-blue")


def get_mode() -> str:
    return _mode


def set_mode(mode: str) -> None:
    global _mode
    if mode not in _PALETTES:
        raise ValueError(f"Unknown theme mode: {mode!r}")
    _mode = mode
    globals().update(_PALETTES[mode])
    ctk.set_appearance_mode(mode)
    _save_mode(mode)


def toggle_mode() -> str:
    set_mode("light" if _mode == "dark" else "dark")
    return _mode


def font(size: int, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight=weight)


def font_title() -> ctk.CTkFont:
    return font(26, "bold")


def font_heading() -> ctk.CTkFont:
    return font(18, "bold")


def font_subheading() -> ctk.CTkFont:
    return font(14, "bold")


def font_body() -> ctk.CTkFont:
    return font(13)


def font_small() -> ctk.CTkFont:
    return font(11)
