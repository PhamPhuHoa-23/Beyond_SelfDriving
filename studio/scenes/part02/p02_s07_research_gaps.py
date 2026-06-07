"""P02-S07 - Research gaps."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_SECTION,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    ORANGE_INFRA,
    PASTEL_AMBER,
    PASTEL_TEAL,
    RED_ERROR,
    SIZE_CAPS,
    SIZE_LABEL,
    SIZE_MICRO,
    vehicle_icon,
)


SCRIPT = "Temporal is not optional."


def _text(label: str, *, size: int = SIZE_LABEL, color: str = INK_DARK, weight=None) -> Text:
    kwargs = {"font": FONT_PRIMARY, "font_size": size, "color": color}
    if weight is not None:
        kwargs["weight"] = weight
    return Text(label, **kwargs)


def _chip(label: str, color: str) -> VGroup:
    txt = _text(label, size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
    pad = RoundedRectangle(
        width=max(1.25, txt.get_width() + 0.34),
        height=0.34,
        corner_radius=0.08,
        fill_color=interpolate_color(color, WHITE, 0.72),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.5,
    )
    txt.move_to(pad)
    return VGroup(pad, txt)


def _lane_marks(width: float) -> VGroup:
    marks = VGroup()
    for x in np.linspace(-width / 2 + 0.38, width / 2 - 0.38, 10):
        marks.add(Line(
            RIGHT * (x - 0.11),
            RIGHT * (x + 0.11),
            stroke_color=WHITE,
            stroke_width=2.0,
            stroke_opacity=0.85,
        ))
    return marks


def _mini_road(width: float = 4.95, height: float = 1.32) -> VGroup:
    base = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.1,
        fill_color=BG_SECTION,
        fill_opacity=1.0,
        stroke_color=LINE_GRID,
        stroke_width=1.4,
    )
    road = RoundedRectangle(
        width=width - 0.46,
        height=0.58,
        corner_radius=0.04,
        fill_color="#CBD5E1",
        fill_opacity=1.0,
        stroke_width=0,
    )
    cross = RoundedRectangle(
        width=0.7,
        height=height - 0.18,
        corner_radius=0.04,
        fill_color="#CBD5E1",
        fill_opacity=1.0,
        stroke_width=0,
    )
    lane_h = _lane_marks(width - 0.7)
    lane_v = _lane_marks(height - 0.28).rotate(PI / 2)
    center_line = Line(
        LEFT * (width / 2 - 0.45),
        RIGHT * (width / 2 - 0.45),
        stroke_color=INK_MID,
        stroke_width=1.2,
        stroke_opacity=0.22,
    )
    return VGroup(base, road, cross, lane_h, lane_v, center_line)


def _snapshot_visual() -> VGroup:
    road = _mini_road()
    y = 0.0
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.34).move_to(LEFT * 1.55 + UP * y)
    target = vehicle_icon(color=ORANGE_INFRA, scale=0.3).move_to(RIGHT * 1.25 + UP * y)
    box = SurroundingRectangle(target, buff=0.07, color=ACCENT_TEAL, stroke_width=2.4)
    connector = Line(
        ego.get_right() + RIGHT * 0.08,
        target.get_left() + LEFT * 0.08,
        stroke_color=ACCENT_TEAL,
        stroke_width=3.0,
        stroke_opacity=0.78,
    )
    tick = Line(UP * 0.23, DOWN * 0.23, stroke_color=ACCENT_TEAL, stroke_width=2.0).move_to(target)
    now = Dot(radius=0.07, color=ACCENT_TEAL).move_to(target)
    label = _chip("detect now", ACCENT_TEAL).scale(0.86)
    label.next_to(road, RIGHT, buff=0.25)
    return VGroup(road, connector, ego, target, box, tick, now, label)


def _temporal_visual() -> VGroup:
    road = _mini_road()
    y = 0.0
    history_points = [
        LEFT * 1.75 + UP * y,
        LEFT * 1.12 + UP * y,
        LEFT * 0.49 + UP * y,
        RIGHT * 0.14 + UP * y,
    ]
    past = VGroup()
    for i, point in enumerate(history_points[:-1]):
        ghost = vehicle_icon(color=GOLD_RICH, scale=0.22 + 0.025 * i)
        ghost.move_to(point)
        ghost.set_opacity(0.32 + 0.18 * i)
        past.add(ghost)
    current = vehicle_icon(color=ORANGE_INFRA, scale=0.31).move_to(history_points[-1])

    trail = VGroup()
    for a, b in zip(history_points[:-1], history_points[1:]):
        trail.add(Line(a + RIGHT * 0.14, b + LEFT * 0.14, stroke_color=GOLD_RICH, stroke_width=3.0, stroke_opacity=0.82))
    future = Arrow(
        history_points[-1] + RIGHT * 0.28,
        RIGHT * 1.62 + UP * y,
        thickness=3.6,
        fill_color=GREEN_FIX,
        buff=0,
        max_tip_length_to_length_ratio=0.18,
    )

    conflict = Circle(
        radius=0.22,
        fill_color=RED_ERROR,
        fill_opacity=0.16,
        stroke_color=RED_ERROR,
        stroke_width=1.6,
    ).move_to(RIGHT * 1.72 + UP * y)
    time_labels = VGroup()
    for label, point in zip(["t-3", "t-2", "t-1", "t"], history_points):
        t = _text(label, size=SIZE_MICRO, color=INK_MID)
        t.move_to(point + DOWN * 0.36)
        time_labels.add(t)
    out = VGroup(_chip("detect", ACCENT_TEAL), _chip("predict", GREEN_FIX)).arrange(DOWN, buff=0.08)
    out.scale(0.78)
    out.next_to(road, RIGHT, buff=0.25)
    return VGroup(road, trail, past, current, future, conflict, time_labels, out)


def _row(title: str, subtitle: str, color: str, fill: str, visual: Mobject) -> VGroup:
    shell = RoundedRectangle(
        width=11.4,
        height=1.92,
        corner_radius=0.16,
        fill_color=fill,
        fill_opacity=0.62,
        stroke_color=color,
        stroke_width=2.2,
    )
    title_mob = _text(title, size=SIZE_LABEL, color=color, weight=BOLD)
    subtitle_mob = _text(subtitle, size=SIZE_CAPS, color=INK_MID)
    title_mob.set_max_width(2.75)
    subtitle_mob.set_max_width(3.15)
    copy = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    left_anchor = shell.get_left() + RIGHT * 0.42 + UP * 0.25
    copy.move_to(left_anchor + RIGHT * copy.get_width() / 2)
    visual.move_to(shell.get_center() + RIGHT * 1.72)
    return VGroup(shell, copy, visual)


class P02S07ResearchGaps(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Research Gap"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Audit references: network_flow temporal feature flow + VLA trajectory/action rows,
        # adapted here as road-state history rather than box-pipeline decoration.
        single = _row(
            "Single frame",
            "One frozen state can only answer\nwhat is here now.",
            ACCENT_TEAL,
            PASTEL_TEAL,
            _snapshot_visual(),
        ).move_to(UP * 1.05)
        temporal = _row(
            "Multi-frame + multi-task",
            "History exposes motion;\nprediction becomes an output.",
            GOLD_RICH,
            PASTEL_AMBER,
            _temporal_visual(),
        ).move_to(DOWN * 1.05)

        gap = VGroup(
            _text("the missing ingredient is time", size=SIZE_LABEL, color=INK_DARK, weight=BOLD),
            Line(LEFT * 2.55, RIGHT * 2.55, stroke_color=GOLD_RICH, stroke_width=3.0),
        ).arrange(DOWN, buff=0.08)
        gap.move_to(DOWN * 2.55)

        self.play(FadeIn(single[0]), FadeIn(single[1]))
        self.play(FadeIn(single[2][0]), ShowCreation(single[2][1]), FadeIn(single[2][2]), FadeIn(single[2][3]))
        self.play(ShowCreation(single[2][4]), ShowCreation(single[2][5]), FadeIn(single[2][6]), FadeIn(single[2][7]))
        self.play(FadeIn(temporal[0]), FadeIn(temporal[1]), FadeIn(temporal[2][0]))
        self.play(ShowCreation(temporal[2][1]), LaggedStart(*(FadeIn(car) for car in temporal[2][2]), lag_ratio=0.18))
        self.play(FadeIn(temporal[2][3]), ShowCreation(temporal[2][4]), FadeIn(temporal[2][5]))
        self.play(FadeIn(temporal[2][6]), FadeIn(temporal[2][7]), FadeIn(gap))
        self.wait(0.7)
        self._close()
