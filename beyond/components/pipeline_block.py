# beyond/components/pipeline_block.py
# ─────────────────────────────────────────────────────────────────
# Standardized pipeline block and arrow helpers.
# Source: BEYOND_SELFDRIVING_ANIMATION_GUIDE.md § 4.3
#
# All pipeline boxes use the same helper function — never eyeball
# widths. Use .arrange(RIGHT, buff=0.55) on VGroup of blocks.
# ─────────────────────────────────────────────────────────────────

from manim import *
from .colors import (
    CYAN_NEON, BG_PANEL, TEXT_WHITE, BLUE_ELECTRIC,
    SIZE_LABEL, FONT_PRIMARY,
)


def pipeline_block(
    text: str,
    width: float = 2.4,
    height: float = 0.85,
    border_color: str = CYAN_NEON,
    fill_color: str = BG_PANEL,
    font_size: int = None,
    text_color: str = TEXT_WHITE,
    corner_radius: float = 0.12,
    min_font: int = 12,
) -> VGroup:
    """
    Standard pipeline block (rounded rect + centered label).

    If the label overflows the width, font_size is reduced automatically
    down to min_font before giving up.

    Returns VGroup([rect, label]) — index 0 is rect, index 1 is label.
    """
    if font_size is None:
        font_size = SIZE_LABEL

    rect = RoundedRectangle(
        corner_radius=corner_radius,
        width=width, height=height,
        fill_color=fill_color, fill_opacity=1.0,
        stroke_color=border_color, stroke_width=1.8,
    )

    label = Text(text, font_size=font_size,
                 color=text_color, font=FONT_PRIMARY)
    # Auto-shrink if too wide
    while label.width > width - 0.25 and font_size > min_font:
        font_size -= 2
        label = Text(text, font_size=font_size,
                     color=text_color, font=FONT_PRIMARY)
    label.move_to(rect.get_center())

    return VGroup(rect, label)


def pipeline_arrow(
    from_mob: Mobject,
    to_mob: Mobject,
    color: str = BLUE_ELECTRIC,
    buff: float = 0.08,
    tip_length: float = 0.18,
    stroke_width: float = 2.0,
) -> Arrow:
    """Standard arrow from one pipeline block to the next."""
    return Arrow(
        from_mob.get_right(), to_mob.get_left(),
        buff=buff,
        color=color,
        stroke_width=stroke_width,
        tip_length=tip_length,
        max_tip_length_to_length_ratio=0.5,
    )


def pipeline_row(
    texts: list[str],
    buff: float = 0.55,
    block_width: float = 2.4,
    block_height: float = 0.85,
    border_color: str = CYAN_NEON,
    fill_color: str = BG_PANEL,
    font_size: int = None,
    text_color: str = TEXT_WHITE,
    with_arrows: bool = True,
    arrow_color: str = BLUE_ELECTRIC,
) -> tuple[VGroup, VGroup]:
    """
    Build a horizontal row of pipeline blocks with arrows between them.

    Returns (blocks_group, arrows_group).
    blocks_group: VGroup of individual pipeline_block VGroups.
    arrows_group: VGroup of Arrow objects (empty if with_arrows=False).
    """
    blocks = VGroup(*[
        pipeline_block(t, width=block_width, height=block_height,
                       border_color=border_color, fill_color=fill_color,
                       font_size=font_size, text_color=text_color)
        for t in texts
    ])
    blocks.arrange(RIGHT, buff=buff)

    arrows = VGroup()
    if with_arrows:
        for i in range(len(blocks) - 1):
            arrows.add(pipeline_arrow(blocks[i], blocks[i + 1],
                                      color=arrow_color))

    return blocks, arrows


def node_block(
    text: str,
    radius: float = 0.45,
    border_color: str = CYAN_NEON,
    fill_color: str = BG_PANEL,
    font_size: int = None,
    text_color: str = TEXT_WHITE,
) -> VGroup:
    """Circular node variant — useful for hub-and-spoke diagrams."""
    if font_size is None:
        font_size = SIZE_LABEL - 2

    circle = Circle(
        radius=radius,
        fill_color=fill_color, fill_opacity=1.0,
        stroke_color=border_color, stroke_width=1.8,
    )
    label = Text(text, font_size=font_size,
                 color=text_color, font=FONT_PRIMARY)
    if label.width > radius * 1.6:
        label.scale(radius * 1.6 / label.width)
    label.move_to(circle.get_center())

    return VGroup(circle, label)
