# beyond/components/colors.py
# ─────────────────────────────────────────────────────────────────
# Theme switcher — reads THEME from beyond/config.py and re-exports
# the right palette. Import everything from here, never from
# colors_dark / colors_white directly.
#
# Usage:
#   from beyond.components.colors import *
#   # or
#   from beyond.components.colors import GOLD, BG_SPACE, CYAN_NEON
# ─────────────────────────────────────────────────────────────────

import os as _os
import sys as _sys

# Resolve the `beyond/` package root so config is importable regardless
# of where manim is invoked from.
_here = _os.path.dirname(_os.path.abspath(__file__))
_pkg_root = _os.path.dirname(_here)
if _pkg_root not in _sys.path:
    _sys.path.insert(0, _pkg_root)

try:
    from config import THEME as _THEME, FONT_PRIMARY, FONT_MONO, FONT_LABEL
except ImportError:
    _THEME = "dark"
    FONT_PRIMARY = "Latin Modern Roman"
    FONT_MONO    = "Courier New"
    FONT_LABEL   = "Latin Modern Roman"

if _THEME == "light":
    from .colors_white import *
else:
    from .colors_dark import *
