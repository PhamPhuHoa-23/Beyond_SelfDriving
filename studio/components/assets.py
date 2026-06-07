"""Asset helpers that fail soft when optional images are missing."""
from __future__ import annotations

from pathlib import Path

from manimlib import *

from studio.components.colors import BG_PAPER, INK_DARK, INK_MID, LINE_SEP
from studio.components.typography import FONT_PRIMARY, SIZE_CAPS


def img_or_placeholder(
    path: str | Path,
    label: str | None = None,
    *,
    width: float = 3.2,
    height: float = 2.0,
) -> Mobject:
    """Return an ImageMobject if present, otherwise a labelled placeholder."""
    image_path = Path(path)
    if image_path.exists():
        image = ImageMobject(str(image_path))
        image.set_width(width)
        if image.get_height() > height:
            image.set_height(height)
        return image

    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        fill_color=BG_PAPER,
        fill_opacity=0.92,
        stroke_color=LINE_SEP,
        stroke_width=1.8,
    )
    inset = 0.18
    cross = VGroup(
        Line(
            frame.get_corner(UL) + inset * DR,
            frame.get_corner(DR) + inset * UL,
            stroke_color=LINE_SEP,
            stroke_width=1.2,
        ),
        Line(
            frame.get_corner(DL) + inset * UR,
            frame.get_corner(UR) + inset * DL,
            stroke_color=LINE_SEP,
            stroke_width=1.2,
        ),
    )
    text = Text(label or image_path.stem or "image", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
    text.set_max_width(width - 0.35)
    text.move_to(frame.get_center())
    return VGroup(frame, cross, text).set_color(INK_DARK)
