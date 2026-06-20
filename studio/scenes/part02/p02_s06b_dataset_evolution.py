"""P02-S06B - V2X dataset evolution."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_CARD,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    LINE_ARROW,
    LINE_SEP,
    ORANGE_INFRA,
    RED_ERROR,
    SIZE_CAPS,
    SIZE_LABEL,
    SIZE_MICRO,
    rsu_icon,
    vehicle_icon,
)


SCRIPT = "Datasets matured from simulation to real-world V2X."


def _text(label: str, *, size: int = SIZE_LABEL, color: str = INK_DARK, weight=None) -> Text:
    kwargs = {"font": FONT_PRIMARY, "font_size": size, "color": color}
    if weight is not None:
        kwargs["weight"] = weight
    return Text(label, **kwargs)


def _venue_badge(label: str, color: str) -> VGroup:
    txt = _text(label, size=SIZE_MICRO, color=color, weight=BOLD)
    pad = RoundedRectangle(
        width=txt.get_width() + 0.26,
        height=0.26,
        corner_radius=0.06,
        fill_color=interpolate_color(color, WHITE, 0.82),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.2,
    )
    txt.move_to(pad)
    return VGroup(pad, txt)


def _dataset_card(name: str, venue: str, subtitle: str, visual: Mobject, color: str) -> VGroup:
    shell = RoundedRectangle(
        width=3.45,
        height=2.35,
        corner_radius=0.14,
        fill_color=BG_CARD,
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=2.0,
    )
    title = _text(name, size=SIZE_LABEL, color=color, weight=BOLD)
    badge = _venue_badge(venue, color)
    title_row = VGroup(title, badge).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    title_row.move_to(shell.get_top() + DOWN * 0.34)

    body = _text(subtitle, size=SIZE_CAPS, color=INK_MID)
    body.set_max_width(2.95)
    body.next_to(title_row, DOWN, buff=0.06)
    body.move_to(np.array([shell.get_center()[0], body.get_y(), 0]))

    visual.set_max_width(2.75)
    visual.set_max_height(0.86)
    visual.move_to(shell.get_bottom() + UP * 0.66)
    return VGroup(shell, title_row, body, visual)


def _mini_sim_visual() -> VGroup:
    road = RoundedRectangle(
        width=2.45,
        height=0.58,
        corner_radius=0.05,
        fill_color=LINE_SEP,
        fill_opacity=1.0,
        stroke_width=0,
    )
    lanes = VGroup()
    for x in np.linspace(-0.9, 0.9, 5):
        lanes.add(Line(
            RIGHT * (x - 0.12),
            RIGHT * (x + 0.12),
            stroke_color=BG_CARD,
            stroke_width=2.0,
            stroke_opacity=0.9,
        ))
    car_a = vehicle_icon(color=ACCENT_BLUE, scale=0.25).move_to(LEFT * 0.65)
    car_b = vehicle_icon(color=ACCENT_TEAL, scale=0.22).move_to(RIGHT * 0.72)
    bubble = Circle(
        radius=0.58,
        fill_color=ACCENT_TEAL,
        fill_opacity=0.08,
        stroke_color=ACCENT_TEAL,
        stroke_width=1.6,
        stroke_opacity=0.55,
    ).move_to(RIGHT * 0.05)
    return VGroup(bubble, road, lanes, car_a, car_b)


def _mini_infra_visual() -> VGroup:
    horiz = RoundedRectangle(
        width=2.45,
        height=0.48,
        corner_radius=0.04,
        fill_color=LINE_SEP,
        fill_opacity=1.0,
        stroke_width=0,
    )
    vert = RoundedRectangle(
        width=0.48,
        height=1.25,
        corner_radius=0.04,
        fill_color=LINE_SEP,
        fill_opacity=1.0,
        stroke_width=0,
    )
    car = vehicle_icon(color=ACCENT_BLUE, scale=0.24).move_to(LEFT * 0.72)
    tower = rsu_icon(color=ORANGE_INFRA).scale(0.62).move_to(RIGHT * 0.62 + UP * 0.38)
    link = Line(
        tower.get_center() + DOWN * 0.08,
        car.get_center() + RIGHT * 0.15,
        stroke_color=CYAN_RADAR,
        stroke_width=2.0,
        stroke_opacity=0.75,
    )
    pulse = Circle(
        radius=0.36,
        stroke_color=CYAN_RADAR,
        stroke_width=1.3,
        stroke_opacity=0.32,
    ).move_to(tower.get_center() + UP * 0.04)
    return VGroup(horiz, vert, link, pulse, car, tower)


def _mini_real_visual() -> VGroup:
    road = RoundedRectangle(
        width=2.45,
        height=0.58,
        corner_radius=0.05,
        fill_color=LINE_SEP,
        fill_opacity=1.0,
        stroke_width=0,
    )
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.24).move_to(LEFT * 0.78 + DOWN * 0.02)
    peer = vehicle_icon(color=ACCENT_TEAL, scale=0.22).move_to(RIGHT * 0.08 + DOWN * 0.02)
    tower = rsu_icon(color=ORANGE_INFRA).scale(0.56).move_to(RIGHT * 0.88 + UP * 0.42)
    v2v = Line(
        ego.get_center() + RIGHT * 0.2,
        peer.get_center() + LEFT * 0.18,
        stroke_color=ACCENT_TEAL,
        stroke_width=2.2,
        stroke_opacity=0.8,
    )
    v2i = Line(
        peer.get_center() + RIGHT * 0.12,
        tower.get_center() + DOWN * 0.1,
        stroke_color=ORANGE_INFRA,
        stroke_width=2.2,
        stroke_opacity=0.78,
    )
    return VGroup(road, v2v, v2i, ego, peer, tower)


def _dataset_evolution_frame() -> VGroup:
    subtitle = _text("from simulated cooperation to real-world V2X", size=SIZE_CAPS, color=INK_MID)
    subtitle.move_to(UP * 2.34)

    cards = VGroup(
        _dataset_card("OPV2V", "ICRA '22", "simulated V2V", _mini_sim_visual(), ACCENT_TEAL),
        _dataset_card("DAIR-V2X", "CVPR '22", "real infrastructure data", _mini_infra_visual(), ORANGE_INFRA),
        _dataset_card("V2X-Real", "ECCV '24", "large-scale real-world\nV2V + V2I", _mini_real_visual(), GOLD_RICH),
    )
    cards.arrange(RIGHT, buff=0.52).move_to(UP * 0.45)

    arrows = VGroup()
    for left, right in zip(cards[:-1], cards[1:]):
        arrows.add(Arrow(
            left.get_right() + RIGHT * 0.06,
            right.get_left() + LEFT * 0.06,
            buff=0,
            thickness=2.2,
            fill_color=LINE_ARROW,
            stroke_color=LINE_ARROW,
            max_tip_length_to_length_ratio=0.14,
        ))

    takeaway = VGroup(
        _text("Reality improved.", size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD),
        _text("Temporal + all-mode coverage still missing.", size=SIZE_LABEL, color=RED_ERROR, weight=BOLD),
    ).arrange(RIGHT, buff=0.18)
    takeaway.move_to(DOWN * 2.45)

    return VGroup(subtitle, cards, arrows, takeaway)


class P02S06BDatasetEvolution(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Dataset Evolution"

    def construct(self):
        self._open(self.SCENE_TITLE)
        frame = _dataset_evolution_frame()
        subtitle, cards, arrows, takeaway = frame

        self.play(FadeIn(subtitle, shift=DOWN * 0.1))
        self.play(FadeIn(cards[0], shift=UP * 0.12))
        for i in range(1, len(cards)):
            self.play(
                ShowCreation(arrows[i - 1]),
                FadeIn(cards[i], shift=UP * 0.12),
                run_time=0.55,
            )
        self.play(FadeIn(takeaway, shift=UP * 0.1))
        self.wait(0.8)
        self._close()
