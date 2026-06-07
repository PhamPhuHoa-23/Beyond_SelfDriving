"""Pipeline diagram building blocks — blocks, rows, arrows, flowing packets."""
from __future__ import annotations

import numpy as np
from manimlib import *
from studio.components.colors import (
    PASTEL_BLUE, ACCENT_BLUE, LINE_ARROW, CYAN_RADAR, INK_DARK, INK_MID,
    BG_CARD, BG_SECTION,
)
from studio.components.typography import FONT_PRIMARY, SIZE_LABEL


def stage_panel(
    title: str,
    content: Mobject,
    *,
    width: float = 2.55,
    height: float = 2.05,
    fill: str = PASTEL_BLUE,
    stroke: str = ACCENT_BLUE,
    inner_fill: str | None = None,
    tight: bool = False,
    pad: float = 0.26,
    show_inner_bg: bool = True,
) -> VGroup:
    """Labeled stage box — high-contrast panel on cream BG (audit: network_flow blocks)."""
    if tight:
        width = max(width, content.get_width() + 2 * pad)
        height = max(height, content.get_height() + 2 * pad)
    panel = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=3.0,
    )
    if not tight:
        content.set_max_width(width - 0.45)
        content.set_max_height(height - 0.45)
    content.move_to(panel.get_center())
    title_mob = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=stroke, weight=BOLD)
    title_mob.next_to(panel, UP, buff=0.14)
    if not show_inner_bg:
        return VGroup(panel, content, title_mob)
    inner_pad = 0.14 if tight else 0.28
    inner_bg = RoundedRectangle(
        width=width - 2 * inner_pad,
        height=height - 2 * inner_pad,
        corner_radius=0.12,
        fill_color=inner_fill or BG_SECTION,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=2.0,
        stroke_opacity=0.85,
    )
    inner_bg.move_to(panel.get_center())
    if hasattr(content, "set_z_index"):
        content.set_z_index(2)
        inner_bg.set_z_index(1)
        panel.set_z_index(0)
        title_mob.set_z_index(3)
    return VGroup(panel, inner_bg, content, title_mob)


def pipeline_block(
    label: str,
    *,
    width: float = 2.4,
    height: float = 1.0,
    fill: str = PASTEL_BLUE,
    stroke: str = ACCENT_BLUE,
) -> VGroup:
    """Rounded rect + centered label. Returns VGroup(rect, label)."""
    shadow = RoundedRectangle(
        width=width, height=height,
        corner_radius=0.18,
        fill_color=BLACK, fill_opacity=0.06,
        stroke_width=0,
    )
    shadow.shift(0.04 * DOWN + 0.04 * RIGHT)
    rect = RoundedRectangle(
        width=width, height=height,
        corner_radius=0.18,
        fill_color=fill, fill_opacity=1.0,
        stroke_color=stroke, stroke_width=2.5,
    )
    lbl = Text(label, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
    lbl.move_to(rect.get_center())
    if hasattr(shadow, "set_z_index"):
        shadow.set_z_index(-1)
        rect.set_z_index(0)
        lbl.set_z_index(1)
    return VGroup(rect, lbl, shadow)


def link_rect(mob: Mobject) -> Mobject:
    """Primary box for connectors (pipeline_block rect, stage_panel shell, etc.)."""
    if isinstance(mob, VGroup) and len(mob) > 0:
        return mob[0]
    return mob


def h_arrow(
    left: Mobject,
    right: Mobject,
    *,
    y: float | None = None,
    color: str = LINE_ARROW,
    buff: float = 0.08,
    thickness: float = 2.8,
) -> Arrow:
    """Horizontal arrow: shared y, rect edge to rect edge (no diagonal overlap)."""
    L = link_rect(left)
    R = link_rect(right)
    if y is None:
        y = (L.get_center()[1] + R.get_center()[1]) / 2
    start = np.array([L.get_right()[0] + buff, y, 0.0])
    end = np.array([R.get_left()[0] - buff, y, 0.0])
    return Arrow(
        start, end,
        thickness=thickness,
        max_tip_length_to_length_ratio=0.35,
        fill_color=color,
        buff=0,
    )


def v_arrow(
    upper: Mobject,
    lower: Mobject,
    *,
    x: float | None = None,
    color: str = LINE_ARROW,
    buff: float = 0.08,
    thickness: float = 2.5,
) -> Arrow:
    """Vertical arrow: shared x, top rect bottom to lower rect top."""
    T = link_rect(upper)
    B = link_rect(lower)
    if x is None:
        x = (T.get_center()[0] + B.get_center()[0]) / 2
    start = np.array([x, T.get_bottom()[1] - buff, 0.0])
    end = np.array([x, B.get_top()[1] + buff, 0.0])
    return Arrow(
        start, end,
        thickness=thickness,
        max_tip_length_to_length_ratio=0.35,
        fill_color=color,
        buff=0,
    )


def pipeline_arrow(start: Mobject, end: Mobject, *, color: str = LINE_ARROW) -> Arrow:
    """Horizontal link between pipeline blocks (aligned centers)."""
    return h_arrow(start, end, color=color, buff=0.06, thickness=3.0)


def pipeline_row(blocks: list[VGroup], *, gap: float = 0.6) -> VGroup:
    """Arrange blocks horizontally with aligned horizontal arrows."""
    arranged = VGroup(*blocks)
    arranged.arrange(RIGHT, buff=gap, aligned_edge=DOWN)
    arrows = VGroup(*(pipeline_arrow(a, b) for a, b in zip(blocks[:-1], blocks[1:])))
    return VGroup(arranged, arrows)


def pipeline_column(blocks: list[VGroup], *, buff: float = 0.28) -> VGroup:
    """Vertical stack with centered vertical arrows (one x column)."""
    arranged = VGroup(*blocks)
    arranged.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    x = link_rect(blocks[0]).get_center()[0]
    arrows = VGroup(*(v_arrow(a, b, x=x, buff=0.08) for a, b in zip(blocks[:-1], blocks[1:])))
    return VGroup(arranged, arrows)


def pipeline_flow(
    blocks: list[VGroup],
    *,
    packet_color: str = CYAN_RADAR,
    n_packets: int = 4,
) -> LaggedStart:
    """Packets traveling left-to-right through block sequence.
    # Pattern adapted from: Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py:55
    """
    anims = []
    for a, b in zip(blocks[:-1], blocks[1:]):
        start_pt = a.get_right() + RIGHT * 0.1
        end_pt = b.get_left() + LEFT * 0.1
        for _ in range(n_packets):
            pkt = Dot(radius=0.07, color=packet_color)
            pkt.move_to(start_pt)
            anims.append(
                pkt.animate(run_time=0.6, rate_func=linear).move_to(end_pt)
            )
    return LaggedStart(*anims, lag_ratio=0.15)
