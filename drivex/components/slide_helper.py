# drivex/components/slide_helper.py
# ─────────────────────────────────────────────────────────────────
# SlideImage: loads a PNG/JPG from the assets directory.
# If the file is missing, renders a labeled placeholder rectangle.
#
# Convention for asset filenames:
#   assets/partXX/slide_NN_description.png
#   assets/intro/slide_NN_description.png
#
# Usage:
#   img = SlideImage("part01/slide_05_fm_diagram.png",
#                    width=5, height=3)
#   self.add(img)
# ─────────────────────────────────────────────────────────────────

from manim import *
import os

_ASSETS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets")
)


class SlideImage(VGroup):
    """
    Loads an image from assets/. Falls back to a labeled
    placeholder rectangle if the file does not exist.

    Parameters
    ----------
    relative_path : path relative to assets/ dir
    width, height : target size in Manim units
    label         : override fallback label text (default = filename)
    """

    def __init__(
        self,
        relative_path: str,
        width: float = 4.0,
        height: float = 2.5,
        label: str = "",
        **kwargs,
    ):
        super().__init__(**kwargs)
        full_path = os.path.join(_ASSETS_DIR, relative_path)

        if os.path.isfile(full_path):
            img = ImageMobject(full_path)
            img.set_width(width)
            if img.height > height:
                img.set_height(height)
            self.add(img)
        else:
            # ── Labeled placeholder ──────────────────────────────
            rect = Rectangle(
                width=width, height=height,
                fill_color="#2A2A2A", fill_opacity=1,
                stroke_color="#888888", stroke_width=1.5,
            )
            display_label = label or os.path.basename(relative_path)
            lbl = Text(
                display_label, font_size=14, color="#AAAAAA"
            ).move_to(rect.get_center())
            # Small camera icon indicator
            cam = Text("📷", font_size=22).move_to(
                rect.get_top() + DOWN * 0.35
            )
            self.add(rect, cam, lbl)

        self._width_target = width
        self._height_target = height
