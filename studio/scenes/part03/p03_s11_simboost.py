"""P03-S11 CDA-SimBoost closed loop."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER,
    ACCENT_PINK, CYAN_RADAR, GOLD_RICH, INK_DARK, INK_MID, FONT_PRIMARY,
    SIZE_LABEL, SIZE_CAPS, SIZE_MICRO, vehicle_icon,
)

SCRIPT = """CDA-SimBoost closes the loop: real data becomes a digital twin, then edge cases, training, and real validation."""


def _txt(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    return Text(text, font=FONT_PRIMARY, font_size=size, color=color, weight=weight)


def _card(title: str, color: str, icon: Mobject, subtitle: str = "") -> VGroup:
    body = RoundedRectangle(
        width=2.06, height=1.14, corner_radius=0.14,
        fill_color=interpolate_color(color, WHITE, 0.86),
        fill_opacity=0.96,
        stroke_color=color, stroke_width=2.2,
    )
    title_mob = _txt(title, size=SIZE_CAPS + 1, color=color, weight=BOLD)
    title_mob.move_to(body.get_top() + DOWN * 0.23)
    icon.scale(0.76)
    icon.move_to(body.get_center() + DOWN * 0.05)
    parts = VGroup(body, icon, title_mob)
    if subtitle:
        sub = _txt(subtitle, size=SIZE_MICRO + 1, color=INK_MID, weight=BOLD)
        sub.move_to(body.get_bottom() + UP * 0.13)
        parts.add(sub)
    return parts


def _real_icon() -> VGroup:
    car = vehicle_icon(color=ACCENT_BLUE, scale=0.3).move_to(LEFT * 0.32)
    logs = VGroup(*[
        RoundedRectangle(width=0.18, height=0.18, corner_radius=0.03, fill_color=c, fill_opacity=1, stroke_width=0)
        for c in (ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER)
    ]).arrange(RIGHT, buff=0.07)
    logs.move_to(RIGHT * 0.36)
    arrow = Arrow(car.get_right() + RIGHT * 0.03, logs.get_left() + LEFT * 0.03, buff=0, stroke_width=1.8, fill_color=CYAN_RADAR, max_tip_length_to_length_ratio=0.16)
    return VGroup(car, arrow, logs)


def _twin_icon() -> VGroup:
    grid = VGroup()
    grid.add(RoundedRectangle(width=0.18, height=0.9, corner_radius=0.03, fill_color="#DDE7F1", fill_opacity=1, stroke_width=0))
    grid.add(RoundedRectangle(width=1.25, height=0.18, corner_radius=0.03, fill_color="#DDE7F1", fill_opacity=1, stroke_width=0))
    car = vehicle_icon(color=ACCENT_GREEN, scale=0.25).move_to(RIGHT * 0.28 + UP * 0.08)
    car.rotate(PI / 2)
    return VGroup(grid, car)


def _scenario_icon() -> VGroup:
    triangle = Triangle(fill_color=ACCENT_AMBER, fill_opacity=0.22, stroke_color=ACCENT_AMBER, stroke_width=1.8)
    triangle.set_width(0.58)
    bang = _txt("!", size=SIZE_CAPS + 8, color=ACCENT_AMBER, weight=BOLD).move_to(triangle.get_center() + DOWN * 0.01)
    rays = VGroup(
        Line(LEFT * 0.34 + UP * 0.18, LEFT * 0.52 + UP * 0.28, stroke_color=ACCENT_AMBER, stroke_width=1.4),
        Line(RIGHT * 0.34 + UP * 0.18, RIGHT * 0.52 + UP * 0.28, stroke_color=ACCENT_AMBER, stroke_width=1.4),
    )
    return VGroup(triangle, bang, rays)


def _train_icon() -> VGroup:
    chart = VGroup()
    base = Line(LEFT * 0.44 + DOWN * 0.18, RIGHT * 0.44 + DOWN * 0.18, stroke_color=INK_MID, stroke_width=1.2, stroke_opacity=0.35)
    chart.add(base)
    for i, h in enumerate([0.26, 0.5]):
        bar = Rectangle(width=0.16, height=h, fill_color=[ACCENT_BLUE, ACCENT_GREEN][i], fill_opacity=0.78, stroke_width=0)
        bar.move_to(LEFT * 0.18 + RIGHT * i * 0.32 + DOWN * 0.18 + UP * h / 2)
        chart.add(bar)
    return chart


def _validate_icon() -> VGroup:
    car = vehicle_icon(color=ACCENT_GREEN, scale=0.3).move_to(LEFT * 0.24)
    check = _txt("OK", size=SIZE_CAPS + 5, color=ACCENT_GREEN, weight=BOLD).move_to(RIGHT * 0.4 + UP * 0.02)
    return VGroup(car, check)


def _arrow(start: Mobject, end: Mobject, *, color: str = ACCENT_GREEN) -> Arrow:
    return Arrow(
        start.get_center(), end.get_center(),
        buff=1.03, stroke_width=2.3, fill_color=color,
        max_tip_length_to_length_ratio=0.11,
    )


class P03S11SimBoost(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "CDA-SimBoost Loop"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        real = _card("1 Real", ACCENT_BLUE, _real_icon(), "ROS logs").move_to(LEFT * 3.75 + UP * 0.68)
        twin = _card("2 Twin", ACCENT_GREEN, _twin_icon(), "CARLA").move_to(UP * 1.68)
        scenarios = _card("3 Cases", ACCENT_AMBER, _scenario_icon(), "rare events").move_to(RIGHT * 3.75 + UP * 0.68)
        train = _card("4 Train", ACCENT_PINK, _train_icon(), "models").move_to(RIGHT * 2.25 + DOWN * 1.55)
        validate = _card("5 Validate", ACCENT_GREEN, _validate_icon(), "hardware").move_to(LEFT * 2.25 + DOWN * 1.55)
        nodes = VGroup(real, twin, scenarios, train, validate)

        arrows = VGroup(
            _arrow(real, twin, color=ACCENT_GREEN),
            _arrow(twin, scenarios, color=ACCENT_GREEN),
            _arrow(scenarios, train, color=ACCENT_GREEN),
            _arrow(train, validate, color=CYAN_RADAR),
            _arrow(validate, real, color=CYAN_RADAR),
        )

        twin_note = _txt("simulation fills the rare tail", size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        twin_note.move_to(DOWN * 2.72)

        self.play(FadeIn(real), run_time=0.35)
        self.play(FadeIn(twin), run_time=0.25)
        self.play(ShowCreation(arrows[0]), run_time=0.32)
        self.play(FadeIn(scenarios), run_time=0.25)
        self.play(ShowCreation(arrows[1]), run_time=0.32)
        self.play(FadeIn(train), run_time=0.25)
        self.play(ShowCreation(arrows[2]), run_time=0.32)
        self.play(FadeIn(validate), run_time=0.25)
        self.play(ShowCreation(arrows[3]), run_time=0.32)
        self.play(ShowCreation(arrows[4]), FadeIn(twin_note), run_time=0.55)
        self.wait(2.2)
        self._close()
