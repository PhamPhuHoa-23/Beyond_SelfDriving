from manim import *
import os

# Ensure LaTeX (MacTeX) is in PATH for Tex/MathTex rendering
os.environ["PATH"] = "/Library/TeX/texbin:" + os.environ.get("PATH", "")

# --- 3Blue1Brown-inspired Color Palette ---
UCLA_BLUE = "#2774AE"
UCLA_GOLD = "#FFD100"
UCLA_DARK = "#003B5C"

DRIVEX_ACCENT = "#58C4DD"  # Sky Blue
DRIVEX_GOLD = "#F9D71C"    # Warm Yellow
DRIVEX_GREEN = "#83C167"   # Soft Green
DRIVEX_RED = "#E07A5F"     # Muted Red

BG_COLOR = "#1C1C1C"       # Deep Dark Gray (Almost Black)
TEXT_COLOR = WHITE

# --- Typography ---
# Use LaTeX rendering (Computer Modern font, same as 3Blue1Brown)
# Text() still uses Pango; use Tex() for LaTeX font in scenes
config.font = "Latin Modern Roman"
config.background_color = BG_COLOR

class DriveXStyle:
    """Class to manage styling across all tutorial parts."""
    
    PRIMARY = DRIVEX_ACCENT
    SECONDARY = DRIVEX_GOLD
    SUCCESS = DRIVEX_GREEN
    ERROR = DRIVEX_RED
    
    @staticmethod
    def get_title_header(text):
        return Title(text, color=WHITE, match_underline_width_to_text=True)

    @staticmethod
    def get_footer_logo():
        # placeholder for adding a small logo at corner
        pass
