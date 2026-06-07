"""P03-S02 Sim-to-Real Gap."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene, BG_PAPER, ACCENT_TEAL, ACCENT_AMBER, ACCENT_BLUE, RED_ERROR,
    INK_LIGHT, LINE_GRID,
    FONT_PRIMARY, SIZE_H1, SIZE_CAPS,
    vehicle_icon,
)

SCRIPT = "Two worlds. Clean simulation on the left, messy reality on the right."


class P03S02SimRealGap(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Sim-to-Real Gap"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        divider = Line(UP * 2.65, DOWN * 1.45, stroke_color=RED_ERROR, stroke_width=3)
        self.play(ShowCreation(divider, run_time=0.8))

        sim_lbl = Text("Simulation", font=FONT_PRIMARY, font_size=SIZE_H1 + 2, color=ACCENT_TEAL)
        real_lbl = Text("Reality", font=FONT_PRIMARY, font_size=SIZE_H1 + 2, color=ACCENT_AMBER)
        sim_lbl.move_to(LEFT * 3.4 + UP * 1.85)
        real_lbl.move_to(RIGHT * 3.4 + UP * 1.85)
        self.play(FadeIn(sim_lbl), FadeIn(real_lbl))

        sim_lane_top = Line(LEFT * 5.75 + UP * 0.25, LEFT * 1.05 + UP * 0.25,
                            stroke_color=ACCENT_TEAL, stroke_width=4)
        sim_lane_bot = Line(LEFT * 5.75 + DOWN * 0.35, LEFT * 1.05 + DOWN * 0.35,
                            stroke_color=ACCENT_TEAL, stroke_width=4)
        sim_center = DashedLine(LEFT * 5.75 + DOWN * 0.05, LEFT * 1.05 + DOWN * 0.05,
                                stroke_color=LINE_GRID, stroke_width=2)
        sim_road = VGroup(sim_lane_top, sim_lane_bot, sim_center)

        real_top = VMobject(stroke_color=INK_LIGHT, stroke_width=4, stroke_opacity=0.75)
        real_bot = VMobject(stroke_color=INK_LIGHT, stroke_width=4, stroke_opacity=0.75)
        xs = np.linspace(1.05, 5.75, 18)
        top_pts = [np.array([x, 0.22 + 0.08 * np.sin(2.2 * x), 0]) for x in xs]
        bot_pts = [np.array([x, -0.43 + 0.10 * np.sin(2.5 * x + 0.8), 0]) for x in xs]
        real_top.set_points_smoothly(top_pts)
        real_bot.set_points_smoothly(bot_pts)
        noise_pts = [
            (1.35, 0.72), (1.75, -0.85), (2.15, 0.55), (2.65, -0.72),
            (3.1, 0.86), (3.65, -0.92), (4.05, 0.62), (4.55, -0.66),
            (5.05, 0.78), (5.45, -0.78), (3.35, 0.12), (4.85, -0.1),
        ]
        noise = VGroup(*(
            Dot(radius=0.04, color=ACCENT_AMBER).set_opacity(0.45).move_to([x, y, 0])
            for x, y in noise_pts
        ))
        real_road = VGroup(real_top, real_bot, noise)

        sim_car = vehicle_icon(color=ACCENT_BLUE, scale=0.72)
        sim_car.move_to(LEFT * 3.35 + DOWN * 0.05)
        real_car = vehicle_icon(color=ACCENT_AMBER, scale=0.72)
        real_car.rotate(8 * DEGREES)
        real_car.move_to(RIGHT * 3.35 + DOWN * 0.12)

        self.play(ShowCreation(sim_road), ShowCreation(real_road))
        self.play(GrowFromCenter(sim_car), GrowFromCenter(real_car))

        sim_caption = Text("Clean  -  Predictable  -  Unlimited",
                           font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_TEAL, weight=BOLD)
        real_caption = Text("Noisy  -  Unpredictable  -  Expensive",
                            font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_AMBER, weight=BOLD)
        sim_caption.move_to(LEFT * 3.35 + DOWN * 1.15)
        real_caption.move_to(RIGHT * 3.35 + DOWN * 1.15)
        self.play(FadeIn(sim_caption), FadeIn(real_caption))

        gap_lbl = Text("Sim-to-Real Gap", font=FONT_PRIMARY, font_size=SIZE_H1 + 2, color=RED_ERROR)
        gap_lbl.move_to(DOWN * 2.35)
        self.play(FadeIn(gap_lbl, scale=1.1))
        self.wait(2)
        self._close()
