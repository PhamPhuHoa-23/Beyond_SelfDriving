"""Studio color palette — all hex literals live here, nowhere else."""
from typing import Final

# Backgrounds — warm cream/beige palette
BG_PAPER: Final[str] = "#FFF9E6"     # warm cream (main scene background)
BG_CARD: Final[str] = "#FFF4CC"      # light amber for card/chip fills
BG_SECTION: Final[str] = "#FDEDB0"   # section/panel fills
BG_TITLECARD: Final[str] = "#FFF9E6" # title card scenes (same warm cream)

# Pastel fills
PASTEL_BLUE: Final[str] = "#BFDBFE"
PASTEL_TEAL: Final[str] = "#99F6E4"
PASTEL_GREEN: Final[str] = "#BBF7D0"
PASTEL_AMBER: Final[str] = "#FDE68A"
PASTEL_PINK: Final[str] = "#FBCFE8"

# Vivid accents
ACCENT_BLUE: Final[str] = "#2563EB"
ACCENT_TEAL: Final[str] = "#0891B2"
ACCENT_GREEN: Final[str] = "#16A34A"
ACCENT_AMBER: Final[str] = "#D97706"
ACCENT_PINK: Final[str] = "#DB2777"

# Ink (text)
INK_DARK: Final[str] = "#0F172A"
INK_MID: Final[str] = "#1E293B"
INK_LIGHT: Final[str] = "#334155"

# Functional semantic
GOLD_RICH: Final[str] = "#D97706"
RED_ERROR: Final[str] = "#DC2626"
GREEN_FIX: Final[str] = "#16A34A"
PURPLE_MODEL: Final[str] = "#7C3AED"
ORANGE_INFRA: Final[str] = "#EA580C"
CYAN_RADAR: Final[str] = "#06B6D4"
GOLD_KEY: Final[str] = "#F59E0B"

# Lines / structure
LINE_GRID: Final[str] = "#E2E8F0"
LINE_SEP: Final[str] = "#CBD5E1"
LINE_ARROW: Final[str] = "#475569"

# Per-part palette lookup
PART_PALETTES: dict[int, dict] = {
    0: {"pastel": PASTEL_BLUE, "accent": ACCENT_BLUE, "ink": INK_DARK},
    1: {"pastel": PASTEL_BLUE, "accent": ACCENT_BLUE, "ink": INK_DARK},
    2: {"pastel": PASTEL_TEAL, "accent": ACCENT_TEAL, "ink": INK_DARK},
    3: {"pastel": PASTEL_GREEN, "accent": ACCENT_GREEN, "ink": INK_DARK},
    4: {"pastel": PASTEL_AMBER, "accent": ACCENT_AMBER, "ink": INK_DARK},
    5: {"pastel": PASTEL_PINK, "accent": ACCENT_PINK, "ink": INK_DARK},
}
