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


class Dropdown(ctk.CTkFrame):
    """A CTkOptionMenu-alike whose popup is a themed, rounded CTkFrame in a
    borderless Toplevel, rather than CTkOptionMenu's own dropdown — which is
    a subclass of the OS-native tkinter.Menu (see customtkinter's
    DropdownMenu) and so ignores corner_radius entirely on Windows. Mirrors
    CTkOptionMenu's .get()/.set()/cget("values") interface so it's a drop-in
    replacement.
    """

    def __init__(self, master, values: list, default: str | None = None, command=None, **kwargs):
        defaults = dict(fg_color=theme.BG_SURFACE_HOVER, corner_radius=theme.RADIUS_MD, height=36)
        defaults.update(kwargs)
        super().__init__(master, **defaults)
        self.pack_propagate(False)

        self._values = list(values)
        self._selected = default or self._values[0]
        self._command = command
        self._popup: tk.Toplevel | None = None
        self._unmap_binding: str | None = None

        self._label = ctk.CTkLabel(
            self,
            text=self._selected,
            font=theme.font_body(),
            text_color=theme.TEXT_PRIMARY,
            anchor="w",
        )
        self._label.pack(side="left", fill="both", expand=True, padx=(theme.PAD_MD, 0))

        self._chevron = ctk.CTkLabel(
            self, text="▾", font=theme.font_body(), text_color=theme.TEXT_SECONDARY, width=20
        )
        self._chevron.pack(side="right", padx=(0, theme.PAD_MD))

        for widget in (self, self._label, self._chevron):
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

        # The root's <Unmap> binding (see _open_popup) targets a window that
        # can outlive this widget (tool screens get destroyed and rebuilt on
        # the same long-lived root). Without this, a Dropdown destroyed
        # while its popup binding is still registered leaves a stale
        # binding on the root pointing at a dead widget.
        self.bind("<Destroy>", self._on_destroy, add="+")

    def get(self) -> str:
        return self._selected

    def set(self, value: str) -> None:
        self._selected = value
        self._label.configure(text=value)

    def cget(self, key):
        if key == "values":
            return self._values
        return super().cget(key)

    def _on_enter(self, _event=None):
        self.configure(fg_color=theme.ACCENT_MUTED)

    def _on_leave(self, _event=None):
        self.configure(fg_color=theme.BG_SURFACE_HOVER)

    def _on_click(self, _event=None):
        if self._popup is not None:
            self._close_popup()
        else:
            self._open_popup()

    def _open_popup(self):
        popup = tk.Toplevel(self)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        # No true per-pixel window transparency without Win32 region masking,
        # so this background shows as small squared-off corners just outside
        # the rounded frame below. BG_APP keeps that seam close to invisible
        # against the screen background the popup normally opens over.
        popup.configure(bg=theme.BG_APP)

        frame = ctk.CTkFrame(popup, fg_color=theme.BG_SURFACE, corner_radius=theme.RADIUS_MD)
        frame.pack(fill="both", expand=True)

        for value in self._values:
            item = ctk.CTkButton(
                frame,
                text=value,
                anchor="w",
                fg_color="transparent",
                hover_color=theme.ACCENT_MUTED,
                text_color=theme.TEXT_PRIMARY,
                font=theme.font_body(),
                corner_radius=theme.RADIUS_SM,
                height=32,
                command=lambda v=value: self._select(v),
            )
            item.pack(fill="x", padx=4, pady=2)

        # Size off the frame's actual rendered height rather than a guessed
        # px-per-item constant: CTk scales widget heights by the display's
        # DPI/scaling factor, so a fixed formula sized correctly at 100%
        # scaling clips items on a monitor with a different scaling setting.
        popup.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 4
        popup.geometry(f"{self.winfo_width()}x{frame.winfo_reqheight()}+{x}+{y}")

        self._popup = popup
        # Click-outside-to-close, implemented via a global ButtonRelease-1
        # rather than <FocusOut> on the popup: FocusOut fires the instant a
        # child widget (like one of the item buttons above) takes focus on
        # press, which is *before* that button's own click fires its
        # command — so a FocusOut-driven close would destroy the popup out
        # from under the very click that was selecting an item. Listening
        # app-wide on release instead lets the clicked widget's own binding
        # run first (Tk dispatches the widget-specific binding before the
        # "all" bindtag for the same event), so a real item selection has
        # already happened by the time this fires and finds self._popup is
        # already None.
        # bind_all/unbind_all must go through `popup` (a plain tk.Toplevel),
        # not `self` — customtkinter's CTkBaseClass overrides both to raise,
        # since it relies on the "all" bindtag for its own internals. The
        # binding itself is still process-global either way; only the
        # widget used to install/remove it matters.
        popup.bind_all("<ButtonRelease-1>", self._on_global_click, add="+")

        # overrideredirect + topmost means Windows won't hide this popup
        # when the main window is minimized — it would otherwise keep
        # floating on top of every other app. Close it explicitly instead.
        self._unmap_binding = self.winfo_toplevel().bind(
            "<Unmap>", self._on_root_unmap, add="+"
        )

    def _on_root_unmap(self, _event=None):
        self._close_popup()

    def _on_global_click(self, event):
        if self._popup is None:
            return
        widget = event.widget
        if self._is_descendant(widget, self) or self._is_descendant(widget, self._popup):
            return
        self._close_popup()

    @staticmethod
    def _is_descendant(widget, ancestor) -> bool:
        while widget is not None:
            if widget == ancestor:
                return True
            widget = getattr(widget, "master", None)
        return False

    def _select(self, value: str) -> None:
        self.set(value)
        self._close_popup()
        if self._command is not None:
            self._command(value)

    def _close_popup(self) -> None:
        if self._popup is not None:
            self._popup.unbind_all("<ButtonRelease-1>")
            self._remove_unmap_binding()
            self._popup.destroy()
            self._popup = None

    def _remove_unmap_binding(self) -> None:
        if self._unmap_binding is not None:
            self.winfo_toplevel().unbind("<Unmap>", self._unmap_binding)
            self._unmap_binding = None

    def _on_destroy(self, _event=None) -> None:
        self._remove_unmap_binding()
        if self._popup is not None:
            self._popup.unbind_all("<ButtonRelease-1>")
            self._popup.destroy()
            self._popup = None
