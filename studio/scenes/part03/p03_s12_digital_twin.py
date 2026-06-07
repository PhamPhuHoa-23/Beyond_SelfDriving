"""P03-S12 Digital Twin scan reveal."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_GREEN, GOLD_RICH, CYAN_RADAR,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon, rsu_icon,
)

SCRIPT = """Scan a real intersection, build its digital twin. The twin keeps the same geometry and moves with reality."""


def _txt(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    return Text(text, font=FONT_PRIMARY, font_size=size, color=color, weight=weight)


def _road_map(*, color: str, twin: bool = False) -> VGroup:
    fill = "#DDE7F1" if not twin else "#CCFBF1"
    opacity = 0.92 if not twin else 0.42
    h_road = RoundedRectangle(
        width=2.7, height=0.44, corner_radius=0.06,
        fill_color=fill, fill_opacity=opacity,
        stroke_color=color, stroke_width=1.2 if twin else 0,
        stroke_opacity=0.5 if twin else 0,
    )
    v_road = RoundedRectangle(
        width=0.44, height=2.05, corner_radius=0.06,
        fill_color=fill, fill_opacity=opacity,
        stroke_color=color, stroke_width=1.2 if twin else 0,
        stroke_opacity=0.5 if twin else 0,
    )
    lanes = VGroup(
        DashedLine(LEFT * 1.15, RIGHT * 1.15, stroke_color=WHITE, stroke_width=1.4, dash_length=0.08, stroke_opacity=0.72),
        DashedLine(DOWN * 0.82, UP * 0.82, stroke_color=WHITE, stroke_width=1.4, dash_length=0.08, stroke_opacity=0.72),
    )
    if twin:
        lanes.set_stroke(CYAN_RADAR, opacity=0.42)
    return VGroup(h_road, v_road, lanes)


def _world(center: np.ndarray, *, twin: bool = False) -> VGroup:
    color = CYAN_RADAR if twin else INK_MID
    accent = CYAN_RADAR if twin else ACCENT_BLUE
    world = _road_map(color=color, twin=twin)

    # Shared local coordinates: real and twin must be congruent.
    rsu_pos = LEFT * 0.78 + UP * 0.74
    car_pos = RIGHT * 0.58 + DOWN * 0.42

    car = vehicle_icon(color=accent, scale=0.52).move_to(car_pos)
    car.rotate(0)
    tower = rsu_icon(color=color).scale(0.74).move_to(rsu_pos)
    link = DashedLine(
        tower.get_center(), car.get_center(),
        stroke_color=CYAN_RADAR, stroke_width=1.2,
        dash_length=0.06, stroke_opacity=0.72,
    )
    rings = VGroup(
        Circle(radius=0.25, stroke_color=CYAN_RADAR, stroke_width=1.0, stroke_opacity=0.36),
        Circle(radius=0.42, stroke_color=CYAN_RADAR, stroke_width=1.0, stroke_opacity=0.25),
    ).move_to(tower)

    if twin:
        car.set_fill(opacity=0.28)
        tower.set_fill(opacity=0.22)
        link.set_stroke(opacity=0.38)
        rings.set_stroke(opacity=0.26)

    group = VGroup(world, link, rings, tower, car)
    group.move_to(center)
    return group


class P03S12DigitalTwin(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Digital Twin"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        div = Line(UP * 2.75, DOWN * 2.55, stroke_color=INK_MID, stroke_width=1.4, stroke_opacity=0.32)
        real_lbl = _txt("Real", size=SIZE_LABEL, color=INK_DARK, weight=BOLD).move_to(LEFT * 3.45 + UP * 2.18)
        twin_lbl = _txt("Digital Twin", size=SIZE_LABEL, color=CYAN_RADAR, weight=BOLD).move_to(RIGHT * 3.45 + UP * 2.18)

        real_center = LEFT * 3.45 + DOWN * 0.05
        twin_center = RIGHT * 3.45 + DOWN * 0.05
        real = _world(real_center, twin=False)
        twin = _world(twin_center, twin=True)

        clone_lines = VGroup(
            DashedLine(real[3].get_center(), twin[3].get_center(), stroke_color=CYAN_RADAR, stroke_width=1.2, dash_length=0.08, stroke_opacity=0.38),
            DashedLine(real[4].get_center(), twin[4].get_center(), stroke_color=CYAN_RADAR, stroke_width=1.2, dash_length=0.08, stroke_opacity=0.38),
        )
        clone_lbl = _txt("same coordinates", size=SIZE_CAPS, color=CYAN_RADAR, weight=BOLD)
        clone_lbl.move_to(UP * 0.28)

        scan_line = Line(UP * 2.6, DOWN * 2.45, stroke_color=CYAN_RADAR, stroke_width=2.4)
        scan_line.move_to(LEFT * 6)

        cap = _txt("OpenCDA -> synchronized digital twin", size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        cap.move_to(DOWN * 2.62)

        self.play(ShowCreation(div), FadeIn(real_lbl), FadeIn(twin_lbl), run_time=0.55)
        self.play(FadeIn(real), run_time=0.65)
        self.play(scan_line.animate.move_to(RIGHT * 6), run_time=1.1, rate_func=linear)
        self.remove(scan_line)
        self.play(FadeIn(twin), ShowCreation(clone_lines), FadeIn(clone_lbl), run_time=0.75)
        self.play(
            real[4].animate.shift(RIGHT * 0.35),
            twin[4].animate.shift(RIGHT * 0.35),
            clone_lines[1].animate.shift(RIGHT * 0.35),
            run_time=0.9,
        )
        self.play(FadeIn(cap), run_time=0.35)
        self.wait(1.7)
        self._close()
