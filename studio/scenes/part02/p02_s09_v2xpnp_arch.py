"""P02-S09 - V2XPnP architecture."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_SECTION,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    ORANGE_INFRA,
    PASTEL_AMBER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_TEAL,
    PURPLE_MODEL,
    RED_ERROR,
    SIZE_CAPS,
    SIZE_LABEL,
    SIZE_MICRO,
    rsu_icon,
    vehicle_icon,
)
from studio.scenes.part02._p02_helpers import attention_arcs, feature_row, mini_heatmap_grid


SCRIPT = "V2XPnP transmits everything in one shot and fuses across time and space."


def _txt(label: str, *, size: int = SIZE_LABEL, color: str = INK_DARK, weight=None) -> Text:
    kwargs = {"font": FONT_PRIMARY, "font_size": size, "color": color}
    if weight is not None:
        kwargs["weight"] = weight
    return Text(label, **kwargs)


def _h_arrow(start: np.ndarray, end: np.ndarray, *, color: str, thickness: float = 3.0) -> Arrow:
    return Arrow(
        start,
        end,
        thickness=thickness,
        fill_color=color,
        buff=0,
        max_tip_length_to_length_ratio=0.14,
    )


def _tiny_road() -> VGroup:
    road = RoundedRectangle(
        width=3.45,
        height=1.72,
        corner_radius=0.12,
        fill_color=BG_SECTION,
        fill_opacity=1.0,
        stroke_color=ACCENT_TEAL,
        stroke_width=2.0,
    )
    lane_h = Rectangle(width=3.08, height=0.46, fill_color="#CBD5E1", fill_opacity=1.0, stroke_width=0)
    lane_v = Rectangle(width=0.5, height=1.35, fill_color="#CBD5E1", fill_opacity=1.0, stroke_width=0)
    dash = VGroup()
    for x in [-1.12, -0.58, 0.58, 1.12]:
        dash.add(Line(RIGHT * (x - 0.11), RIGHT * (x + 0.11), stroke_color=WHITE, stroke_width=1.6))
    return VGroup(road, lane_h, lane_v, dash)


def _input_panel() -> VGroup:
    shell = RoundedRectangle(
        width=3.9,
        height=3.15,
        corner_radius=0.16,
        fill_color=PASTEL_TEAL,
        fill_opacity=0.75,
        stroke_color=ACCENT_TEAL,
        stroke_width=2.4,
    )
    title = _txt("V2X agents", size=SIZE_LABEL, color=ACCENT_TEAL, weight=BOLD)
    title.move_to(shell.get_top() + DOWN * 0.3)
    subtitle = _txt("agent graph + history", size=SIZE_CAPS, color=INK_MID)
    subtitle.move_to(shell.get_top() + DOWN * 0.6)

    road = _tiny_road().move_to(shell.get_center() + UP * 0.05)
    car_a = vehicle_icon(color=ACCENT_BLUE, scale=0.34).move_to(road.get_center() + LEFT * 0.9 + DOWN * 0.16)
    car_b = vehicle_icon(color=GREEN_FIX, scale=0.34).move_to(road.get_center() + RIGHT * 0.78 + UP * 0.2)
    rsu = rsu_icon(color=ORANGE_INFRA).scale(0.78).move_to(road.get_center() + RIGHT * 0.08 + UP * 0.55)
    links = VGroup(
        Line(car_a.get_center(), rsu.get_center(), stroke_color=CYAN_RADAR, stroke_width=2.4, stroke_opacity=0.62),
        Line(car_b.get_center(), rsu.get_center(), stroke_color=CYAN_RADAR, stroke_width=2.4, stroke_opacity=0.62),
    )

    history = VGroup()
    for i, color in enumerate([ACCENT_BLUE, GREEN_FIX]):
        rows = VGroup(*(feature_row(n=5, color=color, width=1.06, height=0.13).shift(DOWN * j * 0.12) for j in range(3)))
        rows.move_to(shell.get_bottom() + UP * 0.35 + RIGHT * (-0.75 + 1.5 * i))
        history.add(rows)
    return VGroup(shell, title, subtitle, road, links, car_a, car_b, rsu, history)


def _fusion_core() -> VGroup:
    shell = RoundedRectangle(
        width=3.9,
        height=3.25,
        corner_radius=0.16,
        fill_color="#FFF4CC",
        fill_opacity=1.0,
        stroke_color=GOLD_RICH,
        stroke_width=2.4,
    )
    title = _txt("Spatio-temporal fusion", size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
    title.move_to(shell.get_top() + DOWN * 0.3)
    subtitle = _txt("memory rows + attention graph", size=SIZE_CAPS, color=INK_MID)
    subtitle.move_to(shell.get_top() + DOWN * 0.6)

    memory = VGroup(*(feature_row(n=9, color=GOLD_RICH, width=2.35, height=0.15).shift(DOWN * i * 0.14) for i in range(4)))
    memory.move_to(shell.get_center() + UP * 0.42)

    nodes = VGroup(
        Dot(LEFT * 0.85 + DOWN * 0.42, radius=0.075, color=ACCENT_BLUE),
        Dot(LEFT * 0.18 + DOWN * 0.18, radius=0.075, color=GREEN_FIX),
        Dot(RIGHT * 0.5 + DOWN * 0.48, radius=0.075, color=ORANGE_INFRA),
        Dot(RIGHT * 0.95 + DOWN * 0.1, radius=0.075, color=PURPLE_MODEL),
    )
    arcs = attention_arcs(nodes, color=PURPLE_MODEL)
    arcs.set_stroke(width=2.0, opacity=0.72)
    graph = VGroup(arcs, nodes).move_to(shell.get_center() + DOWN * 0.42)

    return VGroup(shell, title, subtitle, memory, graph)


def _bev_panel() -> VGroup:
    shell = RoundedRectangle(
        width=3.35,
        height=3.15,
        corner_radius=0.16,
        fill_color=PASTEL_BLUE,
        fill_opacity=0.72,
        stroke_color=ACCENT_BLUE,
        stroke_width=2.4,
    )
    title = _txt("Shared BEV state", size=SIZE_LABEL, color=ACCENT_BLUE, weight=BOLD)
    title.move_to(shell.get_top() + DOWN * 0.3)
    subtitle = _txt("task-ready map", size=SIZE_CAPS, color=INK_MID)
    subtitle.move_to(shell.get_top() + DOWN * 0.6)

    grid = mini_heatmap_grid(rows=5, cols=7, cell=0.22, hot_color=RED_ERROR, safe_color=GREEN_FIX)
    grid.scale(1.18)
    grid.move_to(shell.get_center() + UP * 0.08)
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.25).move_to(grid.get_center() + LEFT * 0.42 + DOWN * 0.05)
    path = VMobject(stroke_color=GREEN_FIX, stroke_width=3.0)
    path.set_points_smoothly([
        grid.get_center() + LEFT * 0.55 + DOWN * 0.42,
        grid.get_center() + RIGHT * 0.1 + DOWN * 0.08,
        grid.get_center() + RIGHT * 0.75 + UP * 0.42,
    ])

    heads = VGroup(
        _task_chip("Detect", ACCENT_TEAL),
        _task_chip("Predict", GOLD_RICH),
        _task_chip("Plan", PURPLE_MODEL),
    ).arrange(RIGHT, buff=0.12)
    heads.move_to(shell.get_bottom() + UP * 0.42)
    return VGroup(shell, title, subtitle, grid, path, ego, heads)


def _task_chip(label: str, color: str) -> VGroup:
    rect = RoundedRectangle(
        width=0.92,
        height=0.36,
        corner_radius=0.08,
        fill_color=interpolate_color(color, WHITE, 0.72),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.5,
    )
    text = _txt(label, size=SIZE_MICRO, color=INK_DARK, weight=BOLD).move_to(rect)
    return VGroup(rect, text)


class P02S09V2XPnPArch(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "V2XPnP Architecture"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Audit references: network_flow attention arcs + graph_theory topology.
        # Adapted into a left-to-right architecture canvas, not a vertical box stack.
        inputs = _input_panel().move_to(LEFT * 4.55 + DOWN * 0.1)
        fusion = _fusion_core().move_to(DOWN * 0.1)
        bev = _bev_panel().move_to(RIGHT * 4.55 + DOWN * 0.1)

        arrow_in = _h_arrow(
            inputs[0].get_right() + RIGHT * 0.06,
            fusion[0].get_left() + LEFT * 0.06,
            color=CYAN_RADAR,
        )
        arrow_out = _h_arrow(
            fusion[0].get_right() + RIGHT * 0.06,
            bev[0].get_left() + LEFT * 0.06,
            color=GOLD_RICH,
        )
        self.play(FadeIn(inputs, shift=UP * 0.12), run_time=0.3)
        self.wait(0.6)
        self.play(FadeIn(fusion, shift=UP * 0.12), ShowCreation(arrow_in), run_time=0.3)
        self.wait(0.6)
        self.play(FadeIn(bev, shift=UP * 0.12), ShowCreation(arrow_out), run_time=0.3)
        self.wait(1.4)
        self._close()
