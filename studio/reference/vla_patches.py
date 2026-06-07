# Ported from Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py
# Lines 214-219 — make_embedding_row
from __future__ import annotations

from manimlib import *
from manimlib.utils.color import interpolate_color

from studio.components.colors import INK_MID


def make_embedding_row(
    color,
    *,
    width: float = 1.1,
    height: float = 0.03,
    y_pos: float = 0.0,
    x_pos: float = -1.5,
) -> Rectangle:
    """Single VLA latent feature bar (not a hand-drawn Dot)."""
    r = Rectangle(width=width, height=height)
    r.set_fill(color, opacity=1).set_stroke(INK_MID, width=0.9, opacity=0.85)
    r.move_to([x_pos, y_pos, 0])
    return r


def make_embedding_row_stack(
    n_rows: int,
    base_color,
    *,
    vertical_spacing: float = 0.12,
    width: float = 1.1,
) -> VGroup:
    """Stack of VLA embedding rows with slight color variation."""
    rows = VGroup()
    for i in range(n_rows):
        c = interpolate_color(base_color, WHITE, 0.08 * (i % 4))
        rows.add(
            make_embedding_row(
                c,
                width=width,
                y_pos=3.15 - i * vertical_spacing,
            )
        )
    return rows
