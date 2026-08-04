import tkinter as tk

import customtkinter as ctk

from catalyst.ui import theme


class Panel(tk.Frame):
    """A plain, unstyled container for pure layout grouping (padding, alignment).

    Unlike CTkFrame — which always allocates its own Canvas and redraws on every
    resize event, even when fg_color="transparent" — this is a lightweight native
    Frame. Using it for structural-only wrappers instead of CTkFrame noticeably
    reduces the number of widgets redrawn on every resize tick.
    """

    def __init__(self, master, bg: str, **kwargs):
        super().__init__(master, bg=bg, highlightthickness=0, bd=0, **kwargs)


class PrimaryButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        defaults = dict(
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color=theme.ON_ACCENT,
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


class OptionGroup(Panel):
    """A row of mutually-exclusive option buttons with real visible gaps between
    them (unlike CTkSegmentedButton, which renders as one continuous bar with no
    way to space out its segments). Mirrors CTkSegmentedButton's .get()/.set()
    interface so it's a drop-in replacement.
    """

    def __init__(self, master, bg: str, values: list, default: str | None = None, **kwargs):
        super().__init__(master, bg=bg, **kwargs)
        self._selected = default or values[0]
        self._buttons: dict[str, ctk.CTkButton] = {}

        for index, value in enumerate(values):
            button = ctk.CTkButton(
                self,
                text=value,
                font=theme.font_body(),
                text_color=theme.TEXT_PRIMARY,
                corner_radius=theme.RADIUS_MD,
                height=36,
                command=lambda v=value: self.set(v),
            )
            button.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(0, theme.PAD_SM) if index < len(values) - 1 else 0,
            )
            self._buttons[value] = button

        self._refresh_colors()

    def _refresh_colors(self) -> None:
        for value, button in self._buttons.items():
            is_selected = value == self._selected
            button.configure(
                fg_color=theme.ACCENT if is_selected else theme.BG_SURFACE_HOVER,
                hover_color=theme.ACCENT_HOVER if is_selected else theme.BG_SURFACE_HOVER,
            )

    def get(self) -> str:
        return self._selected

    def set(self, value: str) -> None:
        self._selected = value
        self._refresh_colors()
