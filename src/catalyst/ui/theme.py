import customtkinter as ctk

FONT_FAMILY = "Segoe UI"

# Dark palette. Warm amber accent ("catalyst" spark) against cool neutral
# surfaces, so the app reads as its own thing rather than a default-blue
# CTk app. Every screen should pull colors from here rather than hardcoding
# hex values, so future Tools stay visually consistent (ADR-0004).
BG_APP = "#15171C"
BG_SIDEBAR = "#101216"
BG_SURFACE = "#20232B"
BG_SURFACE_HOVER = "#272A33"
BORDER = "#2C2F38"

ACCENT = "#E8974E"
ACCENT_HOVER = "#D6853D"
ACCENT_MUTED = "#3A2E20"

TEXT_PRIMARY = "#F2F3F5"
TEXT_SECONDARY = "#8B909C"
TEXT_MUTED = "#5C616D"

SUCCESS = "#4CAF7D"
ERROR = "#E5626B"

RADIUS_SM = 6
RADIUS_MD = 10
RADIUS_LG = 14

PAD_SM = 8
PAD_MD = 16
PAD_LG = 24
PAD_XL = 32


def apply() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


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
