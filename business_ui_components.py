from __future__ import annotations

import ctypes
import tkinter as tk
import tkinter.font as tkfont
from typing import Callable


def enable_dpi_awareness() -> None:
    """Make Tk text as crisp as the business hub on Windows."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def _rounded_polygon(canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, radius: int, **kwargs) -> int:
    radius = max(1, min(radius, (x2 - x1) // 2, (y2 - y1) // 2))
    points = (
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1,
    )
    return canvas.create_polygon(points, smooth=True, splinesteps=24, **kwargs)


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent: tk.Misc,
        text: str,
        command: Callable[[], None],
        *,
        width: int = 150,
        height: int = 44,
        radius: int = 9,
        bg: str = "#3598F5",
        hover_bg: str = "#2389EB",
        fg: str = "#FFFFFF",
        border: str | None = None,
        parent_bg: str | None = None,
        font: tuple[str, int, str] = ("Segoe UI", 10, "bold"),
        anchor: str = "center",
    ) -> None:
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent_bg or str(parent.cget("bg")),
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self._text = text
        self._command = command
        self._normal_bg = bg
        self._hover_bg = hover_bg
        self._fg = fg
        self._border = border or bg
        self._font = font
        self._radius = radius
        self._anchor = anchor
        self._enabled = True
        self.bind("<Configure>", lambda _event: self._draw())
        self.bind("<Enter>", lambda _event: self._draw(self._hover_bg) if self._enabled else None)
        self.bind("<Leave>", lambda _event: self._draw())
        self.bind("<Button-1>", self._clicked)
        self._draw()

    def _draw(self, fill: str | None = None) -> None:
        self.delete("all")
        width = max(2, self.winfo_width() or int(self.cget("width")))
        height = max(2, self.winfo_height() or int(self.cget("height")))
        color = fill or self._normal_bg
        if not self._enabled:
            color = "#D9DCE1"
        _rounded_polygon(self, 1, 1, width - 1, height - 1, self._radius, fill=color, outline=self._border, width=1)
        x = 16 if self._anchor == "w" else width // 2
        font = self._fitted_font(max(width - 24, 20))
        self.create_text(
            x,
            height // 2,
            text=self._text,
            fill=self._fg if self._enabled else "#8A8D91",
            font=font,
            anchor="w" if self._anchor == "w" else "center",
        )

    def _fitted_font(self, available_width: int):
        try:
            family, size, weight = self._font
            candidate = tkfont.Font(root=self, family=family, size=size, weight=weight)
            while size > 7 and candidate.measure(self._text) > available_width:
                size -= 1
                candidate.configure(size=size)
            return (family, size, weight)
        except (tk.TclError, TypeError, ValueError):
            return self._font

    def _clicked(self, _event) -> None:
        if self._enabled:
            self._command()

    def configure(self, cnf=None, **kwargs):  # type: ignore[override]
        if cnf:
            kwargs.update(cnf)
        if "text" in kwargs:
            self._text = str(kwargs.pop("text"))
        if "state" in kwargs:
            self._enabled = kwargs.pop("state") != "disabled"
        if "bg" in kwargs:
            self._normal_bg = str(kwargs.pop("bg"))
        if "fg" in kwargs:
            self._fg = str(kwargs.pop("fg"))
        if "font" in kwargs:
            self._font = kwargs.pop("font")
        result = super().configure(**kwargs) if kwargs else None
        self._draw()
        return result

    config = configure


class BlueCheckbutton(tk.Frame):
    """Theme-independent checkbox with a blue checked state."""

    def __init__(
        self,
        parent: tk.Misc,
        text: str,
        variable: tk.BooleanVar,
        command: Callable[[], None] | None = None,
        *,
        bg: str | None = None,
        fg: str = "#222326",
        active: str = "#3598F5",
        font: tuple[str, int, str] = ("Segoe UI", 10, "normal"),
    ) -> None:
        background = bg or str(parent.cget("bg"))
        super().__init__(parent, bg=background, cursor="hand2")
        self.variable = variable
        self.command = command
        self.active = active
        self.box = tk.Canvas(self, width=20, height=20, bg=background, highlightthickness=0, bd=0, cursor="hand2")
        self.box.pack(side="left")
        self.label = tk.Label(self, text=text, bg=background, fg=fg, font=font, cursor="hand2")
        self.label.pack(side="left", padx=(5, 0))
        for widget in (self, self.box, self.label):
            widget.bind("<Button-1>", self._toggle)
        self._trace = self.variable.trace_add("write", lambda *_args: self._draw())
        self.bind("<Destroy>", self._destroyed)
        self._draw()

    def _toggle(self, _event=None) -> None:
        self.variable.set(not self.variable.get())
        if self.command is not None:
            self.command()

    def _draw(self) -> None:
        try:
            if not self.box.winfo_exists():
                return
            self.box.delete("all")
        except tk.TclError:
            return
        checked = bool(self.variable.get())
        fill = self.active if checked else "#FFFFFF"
        outline = self.active if checked else "#AEB2B8"
        self.box.create_rectangle(2, 2, 18, 18, fill=fill, outline=outline, width=1)
        if checked:
            self.box.create_line(5, 10, 9, 14, 16, 6, fill="#FFFFFF", width=2.2, capstyle="round", joinstyle="round")

    def _destroyed(self, event) -> None:
        if event.widget is self:
            try:
                self.variable.trace_remove("write", self._trace)
            except (tk.TclError, ValueError):
                pass


class RoundedPanel(tk.Canvas):
    """A rounded visual shell with a regular Frame for child widgets."""

    def __init__(
        self,
        parent: tk.Misc,
        *,
        fill: str = "#F5F5F6",
        border: str = "#E3E4E7",
        radius: int = 12,
        padding: int = 10,
        parent_bg: str | None = None,
        width: int = 100,
        height: int = 80,
    ) -> None:
        super().__init__(parent, width=width, height=height, bg=parent_bg or str(parent.cget("bg")), highlightthickness=0, bd=0)
        self.fill = fill
        self.border = border
        self.radius = radius
        self.padding = padding
        self.body = tk.Frame(self, bg=fill)
        self._window = self.create_window(padding, padding, anchor="nw", window=self.body)
        self.bind("<Configure>", self._resize)

    def _resize(self, _event=None) -> None:
        self.delete("panel")
        width = max(2, self.winfo_width())
        height = max(2, self.winfo_height())
        shape = _rounded_polygon(
            self, 1, 1, width - 1, height - 1, self.radius,
            fill=self.fill, outline=self.border, width=1,
        )
        self.addtag_withtag("panel", shape)
        self.tag_lower(shape)
        inset = self.padding
        self.coords(self._window, inset, inset)
        self.itemconfigure(self._window, width=max(1, width - inset * 2), height=max(1, height - inset * 2))
