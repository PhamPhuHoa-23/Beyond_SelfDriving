"""Studio layout zone helpers — position helpers and multi-column arrangers."""
from __future__ import annotations
from manimlib import *

# Zone boundaries (Manim canvas = 14.22u × 8.00u)
TITLE_Y: float = 3.2
SEP_Y: float = 2.85
CONTENT_TOP: float = 2.7
CONTENT_BOTTOM: float = -3.2
FOOTER_Y: float = -3.5
LEFT_X: float = -4.0
RIGHT_X: float = 4.0
CENTER_X: float = 0.0
MAX_TEXT_X: float = 6.5


def place_title(mob: Mobject) -> Mobject:
    """Move mob to title zone (y = TITLE_Y), centered x."""
    mob.move_to([CENTER_X, TITLE_Y, 0])
    return mob


def place_left(mob: Mobject, *, y: float = 0.0) -> Mobject:
    """Move mob to left column (x = LEFT_X)."""
    mob.move_to([LEFT_X, y, 0])
    return mob


def place_right(mob: Mobject, *, y: float = 0.0) -> Mobject:
    """Move mob to right column (x = RIGHT_X)."""
    mob.move_to([RIGHT_X, y, 0])
    return mob


def place_footer(mob: Mobject) -> Mobject:
    """Move mob to footer zone (y = FOOTER_Y), centered x."""
    mob.move_to([CENTER_X, FOOTER_Y, 0])
    return mob


def two_column(left: VGroup, right: VGroup, *, gap: float = 1.0) -> VGroup:
    """Arrange two groups side-by-side with gap at center."""
    group = VGroup(left, right)
    group.arrange(RIGHT, buff=gap)
    return group


def three_column(left: VGroup, mid: VGroup, right: VGroup) -> VGroup:
    """Arrange three groups evenly spaced horizontally."""
    group = VGroup(left, mid, right)
    group.arrange(RIGHT, buff=0.8)
    return group


def content_row(*items: Mobject, buff: float = 0.75, y: float = 0.1) -> VGroup:
    """Horizontally arrange items centered in the content band."""
    row = VGroup(*items)
    row.arrange(RIGHT, buff=buff, aligned_edge=DOWN)
    row.move_to([CENTER_X, y, 0])
    return row


def content_column(
    *items: Mobject,
    buff: float = 0.32,
    x: float = LEFT_X,
    y: float = 0.1,
    aligned_edge=LEFT,
) -> VGroup:
    """Vertically stack items in the left/mid content column."""
    col = VGroup(*items)
    col.arrange(DOWN, buff=buff, aligned_edge=aligned_edge)
    col.move_to([x, y, 0])
    return col


def match_left_edges(*groups: Mobject) -> VGroup:
    """Align all groups to share the same left x (for dual-rail layouts)."""
    for g in groups[1:]:
        g.align_to(groups[0], LEFT)
    return VGroup(*groups)


def fm_three_lane(
    sources: VGroup,
    hub: VGroup,
    tasks: VGroup,
    *,
    y: float = 0.15,
    gap: float = 0.85,
) -> VGroup:
    """Sources | hub | tasks — audit network_flow staging."""
    sources.arrange(DOWN, buff=0.85, aligned_edge=RIGHT)
    tasks.arrange(DOWN, buff=0.85, aligned_edge=LEFT)
    row = VGroup(sources, hub, tasks)
    row.arrange(RIGHT, buff=gap, aligned_edge=UP)
    row.move_to([CENTER_X, y, 0])
    return row


def grid_4(items: list[VGroup]) -> VGroup:
    """Arrange up to 4 items in a 2x2 grid."""
    assert len(items) <= 4
    if len(items) <= 2:
        g = VGroup(*items)
        g.arrange(RIGHT, buff=0.8)
        return g
    top = VGroup(*items[:2]).arrange(RIGHT, buff=0.8)
    bot = VGroup(*items[2:]).arrange(RIGHT, buff=0.8)
    g = VGroup(top, bot)
    g.arrange(DOWN, buff=0.6)
    return g
