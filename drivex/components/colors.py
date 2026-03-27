# drivex/components/colors.py
# ─────────────────────────────────────────────────────────────────
# Canonical color palette for the Beyond Self-Driving video.
# All names prefixed to avoid shadowing Manim built-ins.
# ─────────────────────────────────────────────────────────────────

# ── Background shades ───────────────────────────────────────────
BG_DARK = "#0F172A"   # default scene background (dark blue-slate)
BG_BLACK = "#0D0D0D"   # near-black, used for hook/emotional scenes
BG_NIGHT = "#0A0A0A"   # near-black for gravity scenes (Part 02-02)

# ── Primary palette (from spec doc) ─────────────────────────────
COL_NAVY = "#1F3864"   # backgrounds, headers
COL_BLUE = "#2E75B6"   # accent, arrows, highlights
COL_GOLD = "#E8A838"   # quote text, emphasis
COL_LIGHT_BLUE = "#EAF4FB"   # info boxes, sub-labels
COL_WHITE = "#FFFFFF"   # text on dark backgrounds
COL_RED = "#C0392B"   # warnings, ✗ marks
COL_GREEN = "#27AE60"   # checkmarks, positive outcomes
COL_PURPLE = "#7C3AED"   # neural network components

# ── Part 03 specific ────────────────────────────────────────────
COL_INFRA_ORANGE = "#E67E22"  # infrastructure nodes on maps
COL_ROAD_GRAY = "#4A4A4A"  # road/map elements
COL_SENSOR_CYAN = "#00BCD4"  # sensor beams, calibration lines

# ── Part 04 specific ────────────────────────────────────────────
COL_INT8_GREEN = "#2ECC71"  # quantized / efficient representations
COL_FP32_RED = "#E74C3C"  # heavy FP32 cost indicators
COL_ENERGY_YELLOW = "#F1C40F"  # energy / power cost annotations

# ── Secondary accents ───────────────────────────────────────────
COL_DEEP_PURPLE = "#2D1B69"  # neural net box fill
COL_DEEP_GREEN = "#1B4332"  # positive outcome box fill
COL_DEEP_BLUE = "#1E3A5F"  # info box fill (darker than navy)
COL_GRAY_FILL = "#2A2A2A"  # placeholder image background
COL_DANGER_FILL = "#2A1A1A"  # negative/warning box fill
COL_SOFT_PURPLE = "#A78BFA"  # secondary purple text

# ── UCLA brand ──────────────────────────────────────────────────
UCLA_BLUE = "#2774AE"
UCLA_GOLD = "#FFD100"

# ── Helper: quick opacity variant ───────────────────────────────


def with_opacity(hex_color: str, opacity: float) -> tuple:
    """Return (hex_color, opacity) pair for use with set_fill/stroke."""
    return hex_color, opacity
