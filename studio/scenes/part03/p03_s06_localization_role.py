"""P03-S06 Localization Role."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, ACCENT_BLUE, ACCENT_GREEN,
    GOLD_RICH, INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
)

SCRIPT = """With cooperative perception, localization matters. Wrong position = duplicated objects."""


def _label(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    return Text(text, font=FONT_PRIMARY, font_size=size, color=color, weight=weight)


def _panel(title: str, subtitle: str, x: float, color: str) -> VGroup:
    title_mob = _label(title, size=SIZE_LABEL, color=color, weight=BOLD)
    title_mob.move_to([x, 1.62, 0])
    subtitle_mob = _label(subtitle, size=SIZE_CAPS - 1, color=INK_MID)
    subtitle_mob.next_to(title_mob, DOWN, buff=0.08)
    return VGroup(title_mob, subtitle_mob)


def _arrow_tip(point: np.ndarray, direction: np.ndarray, *, color: str, size: float = 0.12, opacity: float = 1.0) -> Polygon:
    unit = direction / max(np.linalg.norm(direction), 1e-6)
    perp = np.array([-unit[1], unit[0], 0])
    base = point - unit * size
    return Polygon(
        point,
        base + perp * size * 0.42,
        base - perp * size * 0.42,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=color,
        stroke_width=0,
    )


def _thin_arrow(start: np.ndarray, end: np.ndarray, *, color: str, width: float = 2.2, tip_size: float = 0.12, opacity: float = 1.0) -> VGroup:
    direction = end - start
    unit = direction / max(np.linalg.norm(direction), 1e-6)
    shaft = Line(
        start,
        end - unit * tip_size * 0.82,
        stroke_color=color,
        stroke_width=width,
        stroke_opacity=opacity,
    )
    return VGroup(shaft, _arrow_tip(end, direction, color=color, size=tip_size, opacity=opacity))


def _thin_curve_arrow(start: np.ndarray, end: np.ndarray, control: np.ndarray, *, color: str, width: float = 2.4, tip_size: float = 0.16) -> VGroup:
    direction = end - control
    unit = direction / max(np.linalg.norm(direction), 1e-6)
    curve = VMobject()
    curve.set_points_smoothly([start, control, end - unit * tip_size * 0.75])
    curve.set_stroke(color, width=width, opacity=0.95)
    return VGroup(curve, _arrow_tip(end, direction, color=color, size=tip_size, opacity=0.95))


def _axis_frame(origin: np.ndarray, *, color: str, label: str, angle: float = 0.0, scale: float = 1.0) -> VGroup:
    x_end = RIGHT * 0.82 * scale
    y_end = UP * 0.62 * scale
    x_axis = _thin_arrow(ORIGIN, x_end, color=color, width=2.2, tip_size=0.12 * scale)
    y_axis = _thin_arrow(ORIGIN, y_end, color=color, width=2.2, tip_size=0.12 * scale)
    x_tip = _label("x", size=SIZE_CAPS - 4, color=color, weight=BOLD)
    y_tip = _label("y", size=SIZE_CAPS - 4, color=color, weight=BOLD)
    x_tip.move_to(x_end + RIGHT * 0.12)
    y_tip.move_to(y_end + UP * 0.1)
    tag = _label(label, size=SIZE_CAPS - 2, color=color, weight=BOLD)
    tag.next_to(VGroup(x_axis, y_axis), DOWN + LEFT, buff=0.03)
    axes = VGroup(x_axis, y_axis, x_tip, y_tip, tag)
    axes.rotate(angle, about_point=ORIGIN)
    axes.move_to(origin)
    return axes


def _object(center: np.ndarray, *, color: str, opacity: float = 0.75, angle: float = 0.0) -> VGroup:
    body = RoundedRectangle(
        width=0.62, height=0.34, corner_radius=0.06,
        fill_color=color, fill_opacity=opacity,
        stroke_color=color, stroke_width=2.0, stroke_opacity=0.95,
    )
    nose = Polygon(
        RIGHT * 0.31,
        RIGHT * 0.17 + UP * 0.11,
        RIGHT * 0.17 + DOWN * 0.11,
        fill_color=color, fill_opacity=opacity,
        stroke_color=color, stroke_width=1.1,
    )
    mark = Line(LEFT * 0.08, RIGHT * 0.15, stroke_color=WHITE, stroke_width=2.0, stroke_opacity=0.65)
    obj = VGroup(body, nose, mark)
    obj.rotate(angle)
    obj.move_to(center)
    return obj


def _grid(center: np.ndarray, *, width: float = 2.25, height: float = 1.55) -> VGroup:
    lines = VGroup()
    for x in np.linspace(-width / 2, width / 2, 5):
        lines.add(Line([x, -height / 2, 0], [x, height / 2, 0], stroke_color=INK_MID, stroke_width=0.8, stroke_opacity=0.18))
    for y in np.linspace(-height / 2, height / 2, 4):
        lines.add(Line([-width / 2, y, 0], [width / 2, y, 0], stroke_color=INK_MID, stroke_width=0.8, stroke_opacity=0.18))
    lines.move_to(center)
    return lines


def _sensor_view(center: np.ndarray, *, label: str, color: str, angle: float, obj_shift: np.ndarray, scale: float = 1.0) -> VGroup:
    grid = _grid(center)
    axes = _axis_frame(center + LEFT * 0.72 + DOWN * 0.48, color=color, label=label, angle=angle, scale=0.72)
    obj = _object(center + obj_shift, color=color, opacity=0.72, angle=angle * 0.55)
    sight = DashedLine(axes.get_center(), obj.get_center(), stroke_color=color, stroke_width=1.4, dash_length=0.08, stroke_opacity=0.62)
    view = VGroup(grid, sight, obj, axes)
    view.scale(scale, about_point=center)
    return view


class P03S06LocalizationRole(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Why Localization Matters"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        left_head = _panel("Two local views", "same object, different frames", -4.2, INK_DARK)
        mid_head = _panel("No calibration", "merge raw coordinates", 0.0, RED_ERROR)
        right_head = _panel("Calibrated", "transform into common frame", 4.2, GREEN_FIX)

        view_1 = _sensor_view(LEFT * 4.48 + UP * 0.34, label="view 1", color=ACCENT_BLUE, angle=0.0, obj_shift=RIGHT * 0.42 + UP * 0.14, scale=0.74)
        view_2 = _sensor_view(LEFT * 4.48 + DOWN * 0.78, label="view 2", color=GOLD_RICH, angle=-0.55, obj_shift=RIGHT * 0.32 + UP * 0.1, scale=0.74)
        view_brace = Brace(VGroup(view_1, view_2), RIGHT, buff=0.12)
        view_brace.set_color(INK_MID)
        view_brace.set_stroke(INK_MID, width=1.4, opacity=0.85)

        raw_arrow = _thin_arrow(
            view_brace.get_right() + RIGHT * 0.18,
            LEFT * 0.95 + DOWN * 0.05,
            color=INK_MID,
            width=2.6,
            tip_size=0.14,
            opacity=0.95,
        )
        raw_txt = _label("raw merge", size=SIZE_CAPS - 2, color=INK_MID, weight=BOLD)
        raw_txt.next_to(raw_arrow, UP, buff=0.06)

        common_bad = _axis_frame(RIGHT * 0.0 + DOWN * 0.82, color=INK_MID, label="common", scale=0.82)
        bad_obj_1 = _object(LEFT * 0.34 + DOWN * 0.16, color=ACCENT_BLUE, opacity=0.78, angle=0.0)
        bad_obj_2 = _object(RIGHT * 0.42 + UP * 0.2, color=GOLD_RICH, opacity=0.66, angle=-0.35)
        offset_a = bad_obj_1.get_center() + UP * 0.32 + RIGHT * 0.08
        offset_b = bad_obj_2.get_center() + UP * 0.32 + LEFT * 0.08
        bad_offset = VGroup(
            _thin_arrow(offset_a, offset_b, color=RED_ERROR, width=1.6, tip_size=0.105, opacity=0.95),
            _thin_arrow(offset_b, offset_a, color=RED_ERROR, width=1.6, tip_size=0.105, opacity=0.95),
        )
        bad_offset_lbl = _label("double object", size=SIZE_CAPS - 2, color=RED_ERROR, weight=BOLD)
        bad_offset_lbl.next_to(bad_offset, UP, buff=0.05)
        bad_group = VGroup(_grid(DOWN * 0.05, width=2.35, height=1.72), common_bad, bad_obj_1, bad_obj_2, bad_offset, bad_offset_lbl)

        transform_arrow = _thin_curve_arrow(
            RIGHT * 1.35 + DOWN * 0.15,
            RIGHT * 2.45 + DOWN * 0.15,
            RIGHT * 1.9 + UP * 0.12,
            color=GREEN_FIX,
            width=2.5,
            tip_size=0.17,
        )
        transform_txt = _label("apply T", size=SIZE_CAPS - 1, color=GREEN_FIX, weight=BOLD)
        transform_txt.next_to(transform_arrow, UP, buff=0.04)

        common_good = _axis_frame(RIGHT * 4.2 + DOWN * 0.82, color=INK_MID, label="common", scale=0.82)
        good_grid = _grid(RIGHT * 4.2 + DOWN * 0.05, width=2.35, height=1.72)
        good_obj_1 = _object(RIGHT * 4.15 + DOWN * 0.04, color=ACCENT_BLUE, opacity=0.78, angle=0.0)
        good_obj_2 = _object(RIGHT * 4.17 + DOWN * 0.03, color=ACCENT_GREEN, opacity=0.55, angle=0.0)
        check = Text("OK", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD)
        check.next_to(VGroup(good_obj_1, good_obj_2), UP, buff=0.22)
        good_group = VGroup(good_grid, common_good, good_obj_1, good_obj_2, check)

        foot = _label("Localization tells each sensor where its coordinate frame sits.", size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        foot.to_edge(DOWN, buff=0.62)

        self.play(FadeIn(left_head), run_time=0.25)
        self.play(FadeIn(view_1), FadeIn(view_2), FadeIn(view_brace), run_time=0.8)
        self.play(FadeIn(raw_arrow), FadeIn(raw_txt), FadeIn(mid_head), run_time=0.45)
        self.play(FadeIn(bad_group), run_time=0.75)
        self.play(Flash(bad_offset_lbl, color=RED_ERROR, line_length=0.16, num_lines=8), run_time=0.5)
        self.play(FadeIn(transform_arrow), FadeIn(transform_txt), FadeIn(right_head), run_time=0.45)
        self.play(FadeIn(good_group), run_time=0.75)
        self.play(Flash(check, color=GREEN_FIX, line_length=0.18, num_lines=8), FadeIn(foot), run_time=0.6)
        self.wait(1.7)
        self._close()
