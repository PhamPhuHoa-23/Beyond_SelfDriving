# Ported from Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py:631
from __future__ import annotations

from manimlib import *


def attn_head_lines(
    n_rows: int = 6,
    *,
    color=GREY_B,
    width: float = 0.9,
    row_buff: float = 0.1,
) -> VGroup:
    """Stacked thin lines for attention-head rows (action-expert idiom)."""
    lines = VGroup()
    for i in range(n_rows):
        ln = Line(LEFT * width / 2, RIGHT * width / 2, stroke_color=color, stroke_width=2.2)
        ln.set_opacity(0.35 + 0.1 * (i % 3))
        lines.add(ln)
    lines.arrange(DOWN, buff=row_buff, aligned_edge=LEFT)
    return lines
