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
    LINE_ARROW,
    LINE_GRID,
    LINE_SEP,
    ORANGE_INFRA,
    PASTEL_AMBER,
    PASTEL_TEAL,
    RED_ERROR,
    SIZE_CAPS,
    SIZE_LABEL,
    SIZE_MICRO,
    vehicle_icon,
)


SCRIPT = "Two gaps remain: task scope and data coverage."


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
        fill_color=LINE_SEP,
        fill_opacity=1.0,
        stroke_width=0,
    )
    cross = RoundedRectangle(
        width=0.7,
        height=height - 0.18,
        corner_radius=0.04,
        fill_color=LINE_SEP,
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


def _stage_block(label: str, *, color: str, width: float = 1.55) -> VGroup:
    rect = RoundedRectangle(
        width=width,
        height=0.5,
        corner_radius=0.08,
        fill_color=interpolate_color(color, WHITE, 0.72),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.8,
    )
    txt = _text(label, size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
    txt.set_max_width(width - 0.22)
    txt.move_to(rect)
    return VGroup(rect, txt)


def _blocked_stage(label: str) -> VGroup:
    rect = RoundedRectangle(
        width=1.34,
        height=0.46,
        corner_radius=0.08,
        fill_color=LINE_SEP,
        fill_opacity=0.66,
        stroke_color=LINE_ARROW,
        stroke_width=1.35,
    )
    txt = _text(f"{label} ?", size=SIZE_CAPS, color=INK_MID, weight=BOLD)
    txt.set_max_width(1.1)
    txt.move_to(rect)
    return VGroup(rect, txt)


def _flow_arrow(left: Mobject, right: Mobject, *, color: str = LINE_ARROW) -> Arrow:
    return Arrow(
        left.get_right() + RIGHT * 0.05,
        right.get_left() + LEFT * 0.05,
        buff=0,
        thickness=1.8,
        fill_color=color,
        stroke_color=color,
        max_tip_length_to_length_ratio=0.16,
    )


def _missing_mark(scale: float = 1.0) -> VGroup:
    mark = VGroup(
        Line(LEFT * 0.11 + DOWN * 0.11, RIGHT * 0.11 + UP * 0.11, stroke_color=RED_ERROR, stroke_width=2.6),
        Line(LEFT * 0.11 + UP * 0.11, RIGHT * 0.11 + DOWN * 0.11, stroke_color=RED_ERROR, stroke_width=2.6),
    )
    mark.scale(scale)
    return mark


def _stop_badge() -> VGroup:
    rect = RoundedRectangle(
        width=0.82,
        height=0.4,
        corner_radius=0.08,
        fill_color=RED_ERROR,
        fill_opacity=0.14,
        stroke_color=RED_ERROR,
        stroke_width=1.8,
    )
    txt = _text("STOP", size=SIZE_MICRO, color=RED_ERROR, weight=BOLD)
    txt.move_to(rect)
    return VGroup(rect, txt)


def _mode_chip(label: str, color: str, *, active: bool = True) -> VGroup:
    chip = _chip(label, color)
    if not active:
        chip[0].set_fill(LINE_SEP, opacity=0.5)
        chip[0].set_stroke(LINE_GRID, width=1.4)
        chip[1].set_color(INK_MID)
        chip.set_opacity(0.58)
    return chip


def _requirement_row(label: str, status_visual: Mobject) -> VGroup:
    row_bg = RoundedRectangle(
        width=3.55,
        height=0.56,
        corner_radius=0.08,
        fill_color=interpolate_color(LINE_SEP, WHITE, 0.55),
        fill_opacity=0.92,
        stroke_color=LINE_GRID,
        stroke_width=1.1,
    )
    label_mob = _text(label, size=SIZE_CAPS, color=INK_MID, weight=BOLD)
    label_mob.set_max_width(2.65)
    label_mob.move_to(row_bg.get_left() + RIGHT * (0.28 + label_mob.get_width() / 2))
    status_visual.move_to(row_bg.get_right() + LEFT * (0.22 + status_visual.get_width() / 2))
    return VGroup(row_bg, label_mob, status_visual)


def _gap_panel(title: str, subtitle: str, color: str, fill: str, visual: Mobject) -> VGroup:
    shell = RoundedRectangle(
        width=11.55,
        height=2.08,
        corner_radius=0.16,
        fill_color=fill,
        fill_opacity=0.62,
        stroke_color=color,
        stroke_width=2.2,
    )
    title_mob = _text(title, size=SIZE_LABEL, color=color, weight=BOLD)
    subtitle_mob = _text(subtitle, size=SIZE_CAPS, color=INK_MID)
    title_mob.set_max_width(2.95)
    subtitle_mob.set_max_width(3.1)
    copy = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    left_anchor = shell.get_left() + RIGHT * 0.42 + UP * 0.28
    copy.move_to(left_anchor + RIGHT * copy.get_width() / 2)
    visual.set_max_width(7.75)
    visual.set_max_height(1.78)
    visual.move_to(shell.get_center() + RIGHT * 1.82)
    return VGroup(shell, copy, visual)


def _cooperative_detection_scene() -> VGroup:
    road = _mini_road(width=2.35, height=0.86)
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.23).move_to(LEFT * 0.66)
    peer = vehicle_icon(color=ACCENT_TEAL, scale=0.21).move_to(RIGHT * 0.02)
    target = vehicle_icon(color=ORANGE_INFRA, scale=0.2).move_to(RIGHT * 0.68)
    link = Line(
        ego.get_right() + RIGHT * 0.05,
        peer.get_left() + LEFT * 0.05,
        stroke_color=ACCENT_TEAL,
        stroke_width=2.2,
        stroke_opacity=0.72,
    )
    box = SurroundingRectangle(target, buff=0.05, color=ACCENT_TEAL, stroke_width=2.0)
    caption = _text("cooperative sensing", size=SIZE_MICRO, color=INK_MID)
    caption.next_to(road, DOWN, buff=0.06)
    return VGroup(road, link, ego, peer, target, box, caption)


def _trajectory_options() -> VGroup:
    straight = Arrow(
        LEFT * 0.28,
        RIGHT * 0.28,
        buff=0,
        thickness=1.25,
        fill_color=INK_MID,
        stroke_color=INK_MID,
        max_tip_length_to_length_ratio=0.22,
    )
    turn = VGroup(
        Line(LEFT * 0.2 + DOWN * 0.08, RIGHT * 0.16 + DOWN * 0.08, stroke_color=GOLD_RICH, stroke_width=1.55),
        Line(RIGHT * 0.16 + DOWN * 0.08, RIGHT * 0.16 + UP * 0.22, stroke_color=GOLD_RICH, stroke_width=1.55),
    )
    stop = VGroup(
        Circle(radius=0.08, stroke_color=RED_ERROR, stroke_width=1.8),
        Line(LEFT * 0.07, RIGHT * 0.07, stroke_color=RED_ERROR, stroke_width=1.5),
    )
    option_specs = [
        (turn, "turn?", GOLD_RICH),
        (straight, "straight?", INK_MID),
        (stop, "stop?", RED_ERROR),
    ]
    options = VGroup()
    for icon, label, color in option_specs:
        text = _text(label, size=SIZE_MICRO, color=color)
        item = VGroup(icon, text).arrange(DOWN, buff=0.04)
        options.add(item)
    options.arrange(RIGHT, buff=0.38)
    options.set_opacity(0.68)
    return options


def _temporal_cue() -> VGroup:
    chip = _chip("single frame", RED_ERROR).scale(0.78)
    note = _text("no motion history", size=SIZE_MICRO, color=RED_ERROR, weight=BOLD)
    header = VGroup(chip, note).arrange(RIGHT, buff=0.13)
    options = _trajectory_options()
    cue = VGroup(header, options).arrange(DOWN, buff=0.14)
    return cue


def _vehicle_sequence() -> VGroup:
    cars = VGroup()
    labels = ["t-3", "t-2", "t-1", "t"]
    opacities = [0.36, 0.52, 0.68, 0.84]
    for label, opacity in zip(labels, opacities):
        car = vehicle_icon(color=ORANGE_INFRA, scale=0.15)
        car.set_opacity(opacity)
        time = _text(label, size=SIZE_MICRO, color=INK_MID)
        time.next_to(car, DOWN, buff=0.03)
        cars.add(VGroup(car, time))
    cars.arrange(RIGHT, buff=0.34)
    connectors = VGroup(
        Line(cars[0][0].get_right() + RIGHT * 0.05, cars[1][0].get_left() + LEFT * 0.05, stroke_color=GOLD_RICH, stroke_width=1.8, stroke_opacity=0.55),
        Line(cars[2][0].get_right() + RIGHT * 0.05, cars[3][0].get_left() + LEFT * 0.05, stroke_color=GOLD_RICH, stroke_width=1.8, stroke_opacity=0.55),
    )
    missing = _missing_mark(scale=0.7)
    missing.move_to((cars[1][0].get_right() + cars[2][0].get_left()) / 2)
    return VGroup(connectors, cars, missing)


def _task_scope_visual() -> VGroup:
    scene = _cooperative_detection_scene()
    detect = _stage_block("detection\nboxes", color=ACCENT_TEAL, width=1.42)
    stop = _stop_badge()
    predict = _blocked_stage("prediction")
    planning = _blocked_stage("planning")
    flow = VGroup(detect, stop, predict, planning).arrange(RIGHT, buff=0.2)
    flow.next_to(scene, RIGHT, buff=0.42)
    flow.shift(UP * 0.08)
    arrows = VGroup(
        _flow_arrow(detect, stop, color=RED_ERROR),
        _flow_arrow(stop, predict),
        _flow_arrow(predict, planning),
    )
    arrows[1:].set_opacity(0.42)
    top = VGroup(scene, flow, arrows)
    temporal = _temporal_cue()
    temporal.next_to(flow, DOWN, buff=0.18)
    temporal.shift(LEFT * 0.12)
    visual = VGroup(top, temporal)
    visual.move_to(ORIGIN)
    return VGroup(scene, flow, arrows, temporal)


def _data_coverage_visual() -> VGroup:
    seq_status = VGroup(_missing_mark(scale=0.9))
    together_status = VGroup(_missing_mark(scale=0.9))
    rows = VGroup(
        _requirement_row("sequential time-series", seq_status),
        _requirement_row("all modes together", together_status),
    ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    rows.move_to(LEFT * 2.05 + UP * 0.12)

    seq_visual = _vehicle_sequence()
    seq_visual.move_to(RIGHT * 2.05 + UP * 0.5)

    modes = VGroup(
        _mode_chip("V2V", ACCENT_TEAL),
        _mode_chip("V2I", GOLD_RICH),
        _mode_chip("I2I", ORANGE_INFRA, active=False),
    ).arrange(RIGHT, buff=0.1)
    modes.scale(0.82)
    modes_title = _text("partial modes", size=SIZE_MICRO, color=INK_MID, weight=BOLD)
    mode_visual = VGroup(modes_title, VGroup(modes, _missing_mark(scale=0.75)).arrange(RIGHT, buff=0.14))
    mode_visual.arrange(DOWN, buff=0.06)
    mode_visual.move_to(RIGHT * 2.05 + DOWN * 0.2)

    caption = _text("No single dataset covers all modes over time", size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
    caption.move_to(RIGHT * 2.05 + DOWN * 0.72)
    return VGroup(rows, seq_visual, mode_visual, caption)


class P02S07ResearchGaps(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Research Gaps"

    def construct(self):
        self._open(self.SCENE_TITLE)
        task = _gap_panel(
            "Gap 1 - Task Scope",
            "Prior work detects boxes,\nthen stops.",
            ACCENT_TEAL,
            PASTEL_TEAL,
            _task_scope_visual(),
        ).move_to(UP * 1.03)
        data = _gap_panel(
            "Gap 2 - Data Coverage",
            "Temporal fusion needs\nsequence + all modes.",
            GOLD_RICH,
            PASTEL_AMBER,
            _data_coverage_visual(),
        ).move_to(DOWN * 1.18)

        gap = VGroup(
            _text("Missing: downstream tasks, sequence, all V2X modes", size=SIZE_LABEL, color=INK_DARK, weight=BOLD),
            Line(LEFT * 3.55, RIGHT * 3.55, stroke_color=GOLD_RICH, stroke_width=3.0),
        ).arrange(DOWN, buff=0.08)
        gap.move_to(DOWN * 2.82)

        task_visual = task[2]
        self.play(FadeIn(task[0]), FadeIn(task[1]))
        self.play(FadeIn(task_visual[0], shift=UP * 0.08))
        self.play(FadeIn(task_visual[1][0]), ShowCreation(task_visual[2][0]), FadeIn(task_visual[1][1]))
        self.play(FadeIn(task_visual[1][2]), FadeIn(task_visual[1][3]), ShowCreation(task_visual[2][1]), ShowCreation(task_visual[2][2]))
        self.play(FadeIn(task_visual[3][0], shift=UP * 0.05), FadeIn(task_visual[3][1], shift=UP * 0.04))

        data_visual = data[2]
        self.play(FadeIn(data[0]), FadeIn(data[1]))
        self.play(FadeIn(data_visual[0][0], shift=RIGHT * 0.08), FadeIn(data_visual[1], shift=UP * 0.05))
        self.play(FadeIn(data_visual[0][1], shift=RIGHT * 0.08), FadeIn(data_visual[2], shift=UP * 0.05))
        self.play(FadeIn(data_visual[3], shift=UP * 0.08), FadeIn(gap, shift=UP * 0.08))
        self.wait(0.7)
        self._close()
