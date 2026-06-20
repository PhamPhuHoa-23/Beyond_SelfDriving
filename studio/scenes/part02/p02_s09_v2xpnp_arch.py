"""P02-S09 - V2XPnP architecture."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_CARD,
    BG_PAPER,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    ORANGE_INFRA,
    PASTEL_AMBER,
    PASTEL_BLUE,
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


SCRIPT = (
    "What to transmit? V2XPnP evaluates all three fusion strategies - early, late, "
    "and intermediate - each with a temporal dimension. When to transmit? Using a "
    "one-step communication strategy: when agents are within range, they transmit "
    "their full history in a single exchange. Temporal attention then compresses "
    "this multi-frame history into a single-frame representation before "
    "transmission. How to fuse? Two complementary modules: temporal attention "
    "aggregates the motion history of each individual agent; spatial attention "
    "integrates information across different agents at the same timestep."
)


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


def _stage_shell(*, width: float, height: float, fill: str, stroke: str) -> RoundedRectangle:
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        fill_color=fill,
        fill_opacity=0.68,
        stroke_color=stroke,
        stroke_width=2.35,
    )


def _question_label(label: str, *, color: str, width: float = 1.85) -> VGroup:
    text = _txt(label, size=SIZE_CAPS, color=color, weight=BOLD)
    underline = Line(LEFT * width / 2, RIGHT * width / 2, stroke_color=color, stroke_width=2.1)
    return VGroup(text, underline).arrange(DOWN, buff=0.05)


def _raw_payload_visual(color: str) -> VGroup:
    dots = VGroup()
    points = [
        LEFT * 0.22 + UP * 0.08,
        LEFT * 0.06 + DOWN * 0.08,
        RIGHT * 0.1 + UP * 0.0,
        RIGHT * 0.26 + UP * 0.1,
        RIGHT * 0.28 + DOWN * 0.09,
    ]
    for point in points:
        dots.add(Dot(point, radius=0.035, color=color))
    return dots


def _bev_payload_visual(color: str) -> VGroup:
    rows = VGroup(
        feature_row(n=5, color=color, width=0.74, height=0.1),
        feature_row(n=5, color=color, width=0.74, height=0.1),
    ).arrange(DOWN, buff=0.035)
    return rows


def _box_payload_visual(color: str) -> VGroup:
    boxes = VGroup(
        Rectangle(width=0.38, height=0.19, stroke_color=color, stroke_width=2.0),
        Rectangle(width=0.24, height=0.16, stroke_color=color, stroke_width=1.7),
    )
    boxes[0].shift(LEFT * 0.13 + DOWN * 0.02)
    boxes[1].shift(RIGHT * 0.22 + UP * 0.08)
    return boxes


def _time_card(visual: Mobject, *, color: str, width: float = 0.84, height: float = 0.43) -> VGroup:
    back = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.06,
        fill_color=interpolate_color(color, WHITE, 0.72),
        fill_opacity=0.82,
        stroke_color=color,
        stroke_width=1.1,
        stroke_opacity=0.38,
    ).shift(LEFT * 0.07 + UP * 0.06)
    mid = back.copy().shift(RIGHT * 0.06 + DOWN * 0.04)
    front = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.06,
        fill_color=BG_PAPER,
        fill_opacity=0.92,
        stroke_color=color,
        stroke_width=1.4,
    )
    visual.set_max_width(width - 0.18)
    visual.set_max_height(height - 0.14)
    visual.move_to(front)
    return VGroup(back, mid, front, visual)


def _payload_lane(strategy: str, payload: str, color: str, visual: Mobject) -> VGroup:
    lane = RoundedRectangle(
        width=2.18,
        height=0.80,
        corner_radius=0.1,
        fill_color=BG_PAPER,
        fill_opacity=0.94,
        stroke_color=color,
        stroke_width=1.45,
    )
    tag = _txt(strategy, size=SIZE_MICRO, color=color, weight=BOLD)
    tag.set_max_width(0.82)
    tag.move_to(lane.get_top() + DOWN * 0.17 + LEFT * 0.58)

    label = _txt(payload, size=SIZE_MICRO, color=INK_DARK, weight=BOLD)
    label.set_max_width(0.9)
    label.move_to(lane.get_top() + DOWN * 0.17 + RIGHT * 0.55)

    card = _time_card(visual, color=color, width=0.92, height=0.34)
    card.move_to(lane.get_center() + DOWN * 0.12)
    return VGroup(lane, tag, label, card)


def _payload_stack() -> VGroup:
    shell = _stage_shell(width=2.58, height=3.5, fill=PASTEL_TEAL, stroke=ACCENT_TEAL)
    lanes = VGroup(
        _payload_lane("Early", "Raw", ACCENT_TEAL, _raw_payload_visual(ACCENT_TEAL)),
        _payload_lane("Intermediate", "BEV features", ACCENT_BLUE, _bev_payload_visual(ACCENT_BLUE)),
        _payload_lane("Late", "Boxes", GOLD_RICH, _box_payload_visual(GOLD_RICH)),
    ).arrange(DOWN, buff=0.16)
    lanes.move_to(shell.get_center() + DOWN * 0.05)
    return VGroup(shell, lanes)


def _history_frame(color: str, label: str) -> VGroup:
    frame = RoundedRectangle(
        width=0.32,
        height=0.30,
        corner_radius=0.05,
        fill_color=interpolate_color(color, WHITE, 0.74),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.15,
    )
    bars = feature_row(n=3, color=color, width=0.20, height=0.045)
    bars.move_to(frame.get_center() + UP * 0.03)
    text = _txt(label, size=9, color=INK_MID)
    text.move_to(frame.get_center() + DOWN * 0.08)
    return VGroup(frame, bars, text)


def _agent_history_row(icon: Mobject, color: str) -> VGroup:
    frames = VGroup(
        _history_frame(color, "t-2"),
        _history_frame(color, "t-1"),
        _history_frame(color, "t"),
    ).arrange(RIGHT, buff=0.04)
    icon.set_max_width(0.34)
    icon.set_max_height(0.34)
    return VGroup(icon, frames).arrange(RIGHT, buff=0.08)


def _history_panel() -> VGroup:
    shell = _stage_shell(width=2.55, height=3.5, fill=PASTEL_AMBER, stroke=GOLD_RICH)
    rows = VGroup(
        _agent_history_row(vehicle_icon(color=ACCENT_BLUE, scale=0.28), ACCENT_BLUE),
        _agent_history_row(vehicle_icon(color=GREEN_FIX, scale=0.28), GREEN_FIX),
        _agent_history_row(rsu_icon(color=ORANGE_INFRA).scale(0.55), ORANGE_INFRA),
    ).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
    rows.move_to(shell.get_center() + LEFT * 0.44 + UP * 0.05)

    packet_x = shell.get_center()[0] + 0.85
    packet_y = shell.get_center()[1] - 0.07

    packet = RoundedRectangle(
        width=0.54,
        height=2.25,
        corner_radius=0.1,
        fill_color=BG_CARD,
        fill_opacity=1.0,
        stroke_color=GOLD_RICH,
        stroke_width=2.1,
    )
    packet.move_to([packet_x, packet_y, 0])

    feat_1 = feature_row(n=4, color=ACCENT_BLUE, width=0.38, height=0.07)
    feat_2 = feature_row(n=4, color=GREEN_FIX, width=0.38, height=0.07)
    feat_3 = feature_row(n=4, color=ORANGE_INFRA, width=0.38, height=0.07)

    feat_1.move_to([packet_x, rows[0].get_center()[1], 0])
    feat_2.move_to([packet_x, rows[1].get_center()[1], 0])
    feat_3.move_to([packet_x, rows[2].get_center()[1], 0])

    label = _txt("one-step\nexchange", size=10, color=GOLD_RICH, weight=BOLD)
    label.set_max_width(0.48)
    label.move_to([packet_x, packet_y - 0.90, 0])

    packet_group = VGroup(packet, feat_1, feat_2, feat_3, label)

    arrows = VGroup()
    for row in rows:
        start_pt = row[1].get_right() + RIGHT * 0.05
        end_pt = np.array([packet.get_left()[0] - 0.05, row.get_center()[1], 0])
        arrows.add(_h_arrow(start_pt, end_pt, color=GOLD_RICH, thickness=1.5))

    range_line = DashedLine(
        shell.get_bottom() + LEFT * 0.86 + UP * 0.32,
        shell.get_bottom() + RIGHT * 0.86 + UP * 0.32,
        dash_length=0.08,
        stroke_color=GOLD_RICH,
        stroke_width=1.5,
        stroke_opacity=0.7,
    )
    range_label = _txt("within range", size=SIZE_MICRO, color=INK_MID)
    range_label.next_to(range_line, DOWN, buff=0.04)
    return VGroup(shell, rows, packet_group, arrows, range_line, range_label)


def _attention_module(title: str, color: str) -> VGroup:
    shell = RoundedRectangle(
        width=2.48,
        height=3.5,
        corner_radius=0.16,
        fill_color=BG_CARD,
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=2.35,
    )
    title_mob = _txt(title, size=SIZE_LABEL, color=color, weight=BOLD)
    title_mob.set_max_width(1.9)
    title_mob.move_to(shell.get_top() + DOWN * 0.35)

    memory = VGroup(*(feature_row(n=8, color=color, width=1.42, height=0.12).shift(DOWN * i * 0.12) for i in range(4)))
    memory.move_to(shell.get_center() + UP * 0.77)

    nodes = VGroup(
        Dot(LEFT * 0.48 + DOWN * 0.05, radius=0.065, color=ACCENT_BLUE),
        Dot(LEFT * 0.12 + UP * 0.18, radius=0.065, color=GREEN_FIX),
        Dot(RIGHT * 0.32 + DOWN * 0.15, radius=0.065, color=ORANGE_INFRA),
        Dot(RIGHT * 0.56 + UP * 0.12, radius=0.065, color=PURPLE_MODEL),
    )
    arcs = attention_arcs(nodes, color=PURPLE_MODEL)
    arcs.set_stroke(width=1.8, opacity=0.72)
    graph = VGroup(arcs, nodes).move_to(shell.get_center() + DOWN * 0.09)

    single = RoundedRectangle(
        width=1.18,
        height=0.38,
        corner_radius=0.08,
        fill_color=interpolate_color(color, WHITE, 0.68),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.8,
    )
    single_label = _txt("single frame", size=SIZE_MICRO, color=INK_DARK, weight=BOLD).move_to(single)
    single_group = VGroup(single, single_label)
    single_group.move_to(shell.get_center() + DOWN * 1.17)

    compress = _h_arrow(graph.get_bottom() + DOWN * 0.08, single.get_top() + UP * 0.08, color=color, thickness=1.7)

    return VGroup(shell, title_mob, memory, graph, compress, single_group)


def _bev_panel() -> VGroup:
    shell = RoundedRectangle(
        width=3.18,
        height=3.5,
        corner_radius=0.16,
        fill_color=PASTEL_BLUE,
        fill_opacity=0.68,
        stroke_color=ACCENT_BLUE,
        stroke_width=2.35,
    )
    title = _txt("Spatial attention", size=SIZE_LABEL, color=ACCENT_BLUE, weight=BOLD)
    title.move_to(shell.get_top() + DOWN * 0.35)

    nodes = VGroup(
        Dot(LEFT * 0.38 + DOWN * 0.25, radius=0.07, color=ACCENT_BLUE),
        Dot(LEFT * 0.08 + UP * 0.17, radius=0.07, color=GREEN_FIX),
        Dot(RIGHT * 0.34 + DOWN * 0.02, radius=0.07, color=ORANGE_INFRA),
    )
    arcs = attention_arcs(nodes, color=ACCENT_BLUE)
    arcs.set_stroke(width=1.8, opacity=0.7)
    agent_graph = VGroup(arcs, nodes)
    agent_graph.move_to(shell.get_center() + LEFT * 0.78 + UP * 0.24)

    grid = mini_heatmap_grid(rows=5, cols=6, cell=0.21, hot_color=RED_ERROR, safe_color=GREEN_FIX)
    grid.move_to(shell.get_center() + RIGHT * 0.6 + UP * 0.2)
    bev_label = _txt("Shared BEV", size=SIZE_MICRO, color=INK_DARK, weight=BOLD)
    bev_label.next_to(grid, UP, buff=0.08)
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.25).move_to(grid.get_center() + LEFT * 0.42 + DOWN * 0.05)
    path = VMobject(stroke_color=GREEN_FIX, stroke_width=3.0)
    path.set_points_smoothly([
        grid.get_center() + LEFT * 0.55 + DOWN * 0.42,
        grid.get_center() + RIGHT * 0.1 + DOWN * 0.08,
        grid.get_center() + RIGHT * 0.75 + UP * 0.42,
    ])
    fuse_arrow = _h_arrow(agent_graph.get_right() + RIGHT * 0.08, grid.get_left() + LEFT * 0.08, color=ACCENT_BLUE, thickness=2.1)

    heads = VGroup(
        _task_chip("Detect", ACCENT_TEAL),
        _task_chip("Predict", GOLD_RICH),
    ).arrange(RIGHT, buff=0.18)
    heads.move_to(shell.get_bottom() + UP * 0.5)
    return VGroup(shell, title, agent_graph, fuse_arrow, bev_label, grid, path, ego, heads)


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
        # Concepts are borrowed from the paper diagrams, but compressed into the
        # video's own what/when/how visual grammar.
        payload = _payload_stack().move_to(LEFT * 5.12 + DOWN * 0.28)
        history = _history_panel().move_to(LEFT * 2.05 + DOWN * 0.28)
        temporal = _attention_module("Temporal\nattention", GOLD_RICH).move_to(RIGHT * 1.0 + DOWN * 0.28)
        spatial = _bev_panel().move_to(RIGHT * 4.45 + DOWN * 0.28)

        what_label = _question_label("What to transmit?", color=ACCENT_TEAL, width=2.12)
        what_label.move_to(payload[0].get_top() + UP * 0.34)
        when_label = _question_label("When to transmit?", color=GOLD_RICH, width=2.18)
        when_label.move_to(history[0].get_top() + UP * 0.34)
        how_label = _question_label("How to fuse?", color=PURPLE_MODEL, width=1.72)
        how_label.move_to([
            (temporal[0].get_center()[0] + spatial[0].get_center()[0]) / 2,
            temporal[0].get_top()[1] + 0.34,
            0,
        ])

        arrow_payload_history = _h_arrow(
            payload[0].get_right() + RIGHT * 0.08,
            history[0].get_left() + LEFT * 0.08,
            color=CYAN_RADAR,
            thickness=2.2,
        )
        arrow_history_temporal = _h_arrow(
            history[0].get_right() + RIGHT * 0.08,
            temporal[0].get_left() + LEFT * 0.08,
            color=GOLD_RICH,
            thickness=3.0,
        )
        arrow_temporal_spatial = _h_arrow(
            temporal[0].get_right() + RIGHT * 0.08,
            spatial[0].get_left() + LEFT * 0.08,
            color=PURPLE_MODEL,
            thickness=2.4,
        )

        self.play(FadeIn(what_label), FadeIn(payload, shift=UP * 0.12), run_time=0.75)
        self.wait(0.75)
        self.play(
            ShowCreation(arrow_payload_history),
            FadeIn(when_label),
            FadeIn(history, shift=UP * 0.12),
            run_time=0.75,
        )
        self.wait(0.75)
        self.play(
            ShowCreation(arrow_history_temporal),
            FadeIn(how_label),
            FadeIn(temporal, shift=UP * 0.12),
            run_time=0.75,
        )
        self.wait(0.75)
        self.play(
            ShowCreation(arrow_temporal_spatial),
            FadeIn(spatial, shift=UP * 0.12),
            run_time=0.75,
        )
        self.wait(2.0)
        self._close()
