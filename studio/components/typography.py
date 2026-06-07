"""Studio typography — font detection, size constants, Text/Tex builder helpers."""
from __future__ import annotations
from manimlib import *
from studio.components.colors import INK_DARK, GOLD_RICH


def detect_primary_font() -> str:
    """Return CMU Serif if available in Pango, else Latin Modern Roman, else raise."""
    import manimpango
    fonts = manimpango.list_fonts()
    if "CMU Serif" in fonts:
        return "CMU Serif"
    if "Latin Modern Roman" in fonts:
        return "Latin Modern Roman"
    raise RuntimeError(
        "Neither CMU Serif nor Latin Modern Roman found. "
        "Install cm-unicode from CTAN: https://ctan.org/pkg/cm-unicode"
    )


FONT_PRIMARY: str = detect_primary_font()
FONT_MONO: str = "CMU Typewriter Text"

SIZE_HERO: int = 96
SIZE_TITLE: int = 56
SIZE_H1: int = 40
SIZE_BODY: int = 28
SIZE_LABEL: int = 22
SIZE_CAPS: int = 18
SIZE_MICRO: int = 14


def text(s: str, size: int = SIZE_BODY, color: str = INK_DARK, **kw) -> Text:
    """Studio Text — CMU Serif, INK_DARK default."""
    return Text(s, font=FONT_PRIMARY, font_size=size, color=color, **kw)


def markup(s: str, size: int = SIZE_BODY, color: str = INK_DARK, **kw) -> Text:
    """Studio markup Text — same font, accepts <span foreground='#hex'> Pango tags."""
    return Text(s, font=FONT_PRIMARY, font_size=size, color=color, **kw)


def math(s: str, size: int = SIZE_BODY, color: str = INK_DARK) -> Tex:
    """Studio math — LaTeX Tex object, INK_DARK stroke."""
    t = Tex(s, font_size=size)
    t.set_color(color)
    return t


def gold_key_number(s: str, size: int = SIZE_HERO) -> Text:
    """Big GOLD_RICH key number for footer-zone callouts."""
    return Text(s, font=FONT_PRIMARY, font_size=size, color=GOLD_RICH, weight=BOLD)


def bold_text(s: str, size: int = SIZE_BODY, color: str = INK_DARK, **kw) -> Text:
    """Bold Studio Text helper."""
    return Text(s, font=FONT_PRIMARY, font_size=size, color=color, weight=BOLD, **kw)


def italic_text(s: str, size: int = SIZE_BODY, color: str = INK_DARK, **kw) -> Text:
    """Italic Studio Text helper."""
    return Text(s, font=FONT_PRIMARY, font_size=size, color=color, slant=ITALIC, **kw)
