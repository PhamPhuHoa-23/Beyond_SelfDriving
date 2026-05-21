# beyond/config.py
# ─────────────────────────────────────────────────────────────────
# Single place to toggle theme and global settings.
# Change THEME = "dark" | "light" then re-render.
# ─────────────────────────────────────────────────────────────────

# "dark"  → Space Navy bg (#090E1A), neon accents — cinematic
# "light" → White bg (#FFFFFF), navy text — clean/academic
THEME = "dark"

# Default font — "Latin Modern Roman" is confirmed installed on this system.
# Switch to "CMU Serif" if you have it (closer to Welch Labs / 3B1B style).
FONT_PRIMARY = "Latin Modern Roman"
FONT_MONO    = "Courier New"
FONT_LABEL   = "Latin Modern Roman"

# Global quality preset hint (used by render scripts, not Manim itself)
QUALITY = "ql"   # "ql" = 480p15 preview | "qh" = 1080p60 | "qk" = 4K
