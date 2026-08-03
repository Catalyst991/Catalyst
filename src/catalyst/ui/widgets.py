import customtkinter as ctk

from catalyst.ui import theme


class PrimaryButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        defaults = dict(
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color="#1A1206",
            font=theme.font_subheading(),
            corner_radius=theme.RADIUS_MD,
            height=42,
        )
        defaults.update(kwargs)
        super().__init__(master, **defaults)


class SecondaryButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        defaults = dict(
            fg_color="transparent",
            hover_color=theme.BG_SURFACE_HOVER,
            border_width=1,
            border_color=theme.BORDER,
            text_color=theme.TEXT_PRIMARY,
            font=theme.font_body(),
            corner_radius=theme.RADIUS_MD,
            height=36,
        )
        defaults.update(kwargs)
        super().__init__(master, **defaults)


class Card(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        defaults = dict(
            fg_color=theme.BG_SURFACE,
            border_width=1,
            border_color=theme.BORDER,
            corner_radius=theme.RADIUS_LG,
        )
        defaults.update(kwargs)
        super().__init__(master, **defaults)
