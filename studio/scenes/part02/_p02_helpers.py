"""Local helpers for Part 2 scenes."""
from __future__ import annotations

from manimlib import *

from studio.components import (
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_CARD,
    BG_PAPER,
    BG_SECTION,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_KEY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_LIGHT,
    INK_MID,
    LINE_ARROW,
    LINE_GRID,
    ORANGE_INFRA,
    PASTEL_AMBER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_TEAL,
    PURPLE_MODEL,
    RED_ERROR,
    SIZE_BODY,
    SIZE_CAPS,
    SIZE_H1,
    SIZE_LABEL,
    SIZE_MICRO,
    vehicle_icon,
)


def p2_card(
    title: str,
    body: str = "",
    *,
    width: float = 3.3,
    height: float = 1.35,
    stroke: str = ACCENT_TEAL,
    fill: str = BG_CARD,
    title_color: str = INK_DARK,
    body_size: int = SIZE_CAPS,
) -> VGroup:
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=2.0,
    )
    title_mob = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=title_color, weight=BOLD)
    if body:
        body_mob = Text(body, font=FONT_PRIMARY, font_size=body_size, color=INK_MID)
        body_mob.set_max_width(width - 0.35)
        group = VGroup(title_mob, body_mob).arrange(DOWN, buff=0.1)
    else:
        group = VGroup(title_mob)
    group.move_to(rect)
    return VGroup(rect, group)


def mechanism_block(
    title: str,
    visual: Mobject,
    *,
    width: float = 2.6,
    height: float = 1.05,
    fill: str = BG_CARD,
    stroke: str = ACCENT_TEAL,
) -> VGroup:
    """Block with separate title and visual slots; avoids visual-on-label overlap."""
    rect = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.14,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=2.4,
    )
    title_mob = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
    title_mob.set_max_width(width - 0.3)
    title_mob.move_to(rect.get_top() + DOWN * 0.26)
    visual.set_max_width(width - 0.45)
    visual.set_max_height(height * 0.42)
    visual.move_to(rect.get_center() + DOWN * 0.22)
    return VGroup(rect, title_mob, visual)


def small_caption(text: str, *, color: str = INK_MID) -> Text:
    return Text(text, font=FONT_PRIMARY, font_size=SIZE_BODY, color=color)


def road_grid_2d(width: float = 12.0, height: float = 5.2) -> VGroup:
    road_h = height / 2
    horiz = VGroup(
        Rectangle(width=width, height=road_h, fill_color=BG_SECTION, fill_opacity=1.0, stroke_width=0),
        Rectangle(width=road_h, height=height, fill_color=BG_SECTION, fill_opacity=1.0, stroke_width=0),
    )
    lane_lines = VGroup()
    for y in [-0.5, 0.5]:
        lane_lines.add(Line(LEFT * width / 2 + UP * y, RIGHT * width / 2 + UP * y, stroke_color=LINE_GRID, stroke_width=2))
    for x in [-0.5, 0.5]:
        lane_lines.add(Line(DOWN * height / 2 + RIGHT * x, UP * height / 2 + RIGHT * x, stroke_color=LINE_GRID, stroke_width=2))
    return VGroup(horiz, lane_lines)


def road_grid_3d(width: float = 9.0, height: float = 6.0) -> VGroup:
    grid = VGroup()
    for x in np.linspace(-width / 2, width / 2, 10):
        grid.add(Line([x, -height / 2, 0], [x, height / 2, 0], stroke_color=LINE_GRID, stroke_width=1, stroke_opacity=0.25))
    for y in np.linspace(-height / 2, height / 2, 8):
        grid.add(Line([-width / 2, y, 0], [width / 2, y, 0], stroke_color=LINE_GRID, stroke_width=1, stroke_opacity=0.25))
    roads = VGroup(
        Rectangle(width=width, height=1.3, fill_color=BG_SECTION, fill_opacity=0.35, stroke_color=LINE_GRID, stroke_width=1),
        Rectangle(width=1.3, height=height, fill_color=BG_SECTION, fill_opacity=0.35, stroke_color=LINE_GRID, stroke_width=1),
    )
    return VGroup(grid, roads)


def milestone_bead(label: str, subtitle: str, color: str) -> VGroup:
    bead = Circle(radius=0.18, fill_color=color, fill_opacity=1.0, stroke_color=color, stroke_width=2)
    title = Text(label, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
    sub = Text(subtitle, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
    texts = VGroup(title, sub).arrange(DOWN, buff=0.04)
    texts.next_to(bead, UP, buff=0.16)
    return VGroup(bead, texts)


def feature_row(
    *,
    n: int = 10,
    color: str = ACCENT_TEAL,
    width: float = 1.75,
    height: float = 0.28,
) -> VGroup:
    """Compact feature-token row inspired by transformer embedding rows."""
    cells = VGroup()
    cell_w = width / n
    for i in range(n):
        alpha = 0.35 + 0.55 * ((i * 5) % 11) / 10
        cell = Rectangle(
            width=cell_w * 0.88,
            height=height,
            fill_color=interpolate_color(color, WHITE, 1 - alpha),
            fill_opacity=1.0,
            stroke_color=INK_DARK,
            stroke_width=0.45,
            stroke_opacity=0.25,
        )
        cells.add(cell)
    cells.arrange(RIGHT, buff=0.02)
    return cells


def mini_heatmap_grid(
    *,
    rows: int = 5,
    cols: int = 7,
    cell: float = 0.22,
    hot_color: str = RED_ERROR,
    safe_color: str = GREEN_FIX,
) -> VGroup:
    """Risk-map cells with a visible hot spot and safe corridor."""
    grid = VGroup()
    hot = np.array([cols * 0.62, rows * 0.68])
    safe = np.array([cols * 0.28, rows * 0.22])
    for r in range(rows):
        for c in range(cols):
            p = np.array([c, r])
            hotness = np.exp(-np.linalg.norm(p - hot) ** 2 / 4.0)
            safeness = np.exp(-np.linalg.norm(p - safe) ** 2 / 3.0)
            color = interpolate_color(safe_color, hot_color, hotness / (hotness + safeness + 0.25))
            sq = Square(
                side_length=cell,
                fill_color=color,
                fill_opacity=0.42 + 0.35 * max(hotness, safeness),
                stroke_color=INK_DARK,
                stroke_width=0.45,
                stroke_opacity=0.18,
            )
            grid.add(sq)
    grid.arrange_in_grid(rows, cols, buff=0.015)
    return grid


def person_grid(rows: int = 10, cols: int = 10) -> VGroup:
    icons = VGroup()
    for _ in range(rows * cols):
        head = Circle(radius=0.035, fill_color=INK_LIGHT, fill_opacity=1.0, stroke_width=0)
        body = Line(ORIGIN, DOWN * 0.12, stroke_color=INK_LIGHT, stroke_width=1.6)
        head.next_to(body, UP, buff=0.01)
        icons.add(VGroup(head, body))
    icons.arrange_in_grid(rows, cols, buff=0.1)
    return icons


def packet_cloud(center: np.ndarray, *, n: int = 20, color: str = CYAN_RADAR) -> VGroup:
    cloud = VGroup()
    for i in range(n):
        dot = Dot(radius=0.035, color=color)
        angle = TAU * i / n
        rad = 0.25 + 0.45 * ((i * 7) % 13) / 13
        dot.move_to(center + rad * np.array([np.cos(angle), np.sin(angle), 0]))
        cloud.add(dot)
    return cloud


def attention_arcs(nodes: VGroup, *, color: str = GOLD_RICH) -> VGroup:
    # Pattern adapted from: Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py:161
    arcs = VGroup()
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            sign = 1 if b.get_x() > a.get_x() else -1
            arcs.add(Line(a.get_top(), b.get_top(), path_arc=sign * PI / 3, stroke_color=color, stroke_width=2.5, stroke_opacity=0.65))
    return arcs


def gradient_arrows(center: np.ndarray) -> VGroup:
    specs = [
        ("Detect", ACCENT_TEAL, UP + LEFT * 0.6),
        ("Predict", GOLD_RICH, DOWN + RIGHT * 0.75),
        ("Plan", PURPLE_MODEL, LEFT),
    ]
    group = VGroup()
    for label, color, vec in specs:
        arrow = Arrow(center, center + normalize(vec) * 1.05, fill_color=color, thickness=3, buff=0.0)
        text = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=color, weight=BOLD)
        text.next_to(arrow.get_end(), normalize(vec), buff=0.08)
        group.add(VGroup(arrow, text))
    return group


def topdown_car(color: str = ACCENT_BLUE, scale: float = 0.7) -> VGroup:
    car = vehicle_icon(color=color, scale=scale)
    return car


def heat_blob(center: np.ndarray, *, color: str, radius: float, opacity: float) -> VGroup:
    # Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/region.py:50
    blobs = VGroup()
    for i in range(4):
        c = Circle(
            radius=radius * (1 + i * 0.34),
            fill_color=color,
            fill_opacity=opacity * (1 - i * 0.22),
            stroke_width=0,
        )
        c.move_to(center)
        blobs.add(c)
    return blobs


def scene_end_pause(scene: Scene, seconds: float = 0.5) -> None:
    scene.wait(seconds)
