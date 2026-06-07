"""Studio global config — background default, font, quality presets."""
from studio.components.colors import BG_PAPER
from studio.components.typography import FONT_PRIMARY, FONT_MONO

# Default quality presets (for manimgl CLI)
QUALITY_LOW = "-l"       # 480p15  — for preview
QUALITY_MED = "-m"       # 720p30
QUALITY_HIGH = "--hd"    # 1080p60
QUALITY_4K = "--uhd"     # 4K

# Background used by all body scenes
STUDIO_BG = BG_PAPER

__all__ = [
    "STUDIO_BG",
    "FONT_PRIMARY",
    "FONT_MONO",
    "QUALITY_LOW",
    "QUALITY_MED",
    "QUALITY_HIGH",
    "QUALITY_4K",
]
