"""P03-S04a Time Calibration: 50ms -> 83cm error."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, ACCENT_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon, key_number,
)
SCRIPT = """A 50-millisecond delay at 60 km/h is 83 centimeters of position error."""


class P03S04ATimeCalibration(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Time Calibration"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        road = Line(LEFT * 5.4 + UP * 0.48, RIGHT * 4.8 + UP * 0.48,
                    stroke_color=INK_MID, stroke_width=2.2, stroke_opacity=0.35)
        self.play(ShowCreation(road))

        car = vehicle_icon(color=ACCENT_BLUE, scale=1.1).move_to(LEFT * 4.5 + UP * 0.8)
        speed_lbl = Text("60 km/h", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_BLUE)
        speed_lbl.next_to(car, UP, buff=0.12)
        self.play(GrowFromCenter(car), FadeIn(speed_lbl))
        self.play(car.animate.move_to(LEFT * 1.5 + UP * 0.8), run_time=1.0, rate_func=linear)
        # Observed position 83cm behind
        obs_car = car.copy().set_color(RED_ERROR).set_opacity(0.55)
        obs_car.move_to(LEFT * 4.5 + UP * 0.8)
        self.play(FadeIn(obs_car))
        gap_fwd = Arrow(obs_car.get_right() + UP * 0.04, car.get_left() + UP * 0.04,
                        fill_color=RED_ERROR, thickness=1.8, buff=0.06)
        gap_back = Arrow(car.get_left() + DOWN * 0.04, obs_car.get_right() + DOWN * 0.04,
                         fill_color=RED_ERROR, thickness=1.8, buff=0.06)
        gap = VGroup(gap_fwd, gap_back)
        gap_lbl = Text("83 cm offset", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        gap_lbl.next_to(gap, UP, buff=0.28)
        delay_tag = Text("Infrastructure sees 50ms behind", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID)

        timeline = Line(LEFT * 4.5 + DOWN * 0.65, LEFT * 1.5 + DOWN * 0.65,
                        stroke_color=INK_MID, stroke_width=2.0)
        ticks = VGroup()
        for i in range(7):
            x = interpolate(-4.5, -1.5, i / 6)
            tick = Line([x, -0.78, 0], [x, -0.52, 0], stroke_color=INK_MID, stroke_width=1.4)
            ticks.add(tick)
        t0 = Text("0ms", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
        t50 = Text("50ms", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
        t0.next_to(ticks[0], DOWN, buff=0.08)
        t50.next_to(ticks[-1], DOWN, buff=0.08)
        delay_tag.next_to(timeline, UP, buff=0.2)
        self.play(ShowCreation(gap), FadeIn(gap_lbl), FadeIn(delay_tag))
        self.play(ShowCreation(timeline), ShowCreation(ticks), FadeIn(t0), FadeIn(t50))
        kn = key_number("83 cm", "position error at 60 km/h", color=RED_ERROR)
        kn.set_color(RED_ERROR)
        for sub in kn.family_members_with_points():
            sub.set_color(RED_ERROR)
        kn.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(kn))
        self.wait(2)
        self._close()
