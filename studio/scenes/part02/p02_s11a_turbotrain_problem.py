"""P02-S11a - TurboTrain problem chart."""
from manimlib import *

from studio.components import StudioScene, ACCENT_BLUE, ORANGE_INFRA, RED_ERROR, INK_DARK, INK_MID, FONT_PRIMARY, SIZE_CAPS, SIZE_LABEL, axes_deploy


SCRIPT = "Training a multi-agent, multi-frame, multi-task model is unstable."


class P02S11ATurboTrainProblem(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "TurboTrain Problem"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Pattern adapted from: Source_manim_reference/welchlabs_videos/_2025/backprop_3/geometry_while_learning_2.py
        axes, anim = axes_deploy((0, 10), (0, 10), x_label="", y_label="", width=6.8, height=4.15, with_tick_labels=False)
        axes.move_to(RIGHT * 0.25 + UP * 0.35)
        y_ticks = VGroup()
        for y in range(0, 11, 2):
            tick = Text(str(y), font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID, weight=BOLD)
            tick.next_to(axes.c2p(0, y), LEFT, buff=0.2)
            y_ticks.add(tick)
        y_label = Text("EPA", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        y_label.rotate(90 * DEGREES)
        y_label.next_to(y_ticks, LEFT, buff=0.38)
        self.play(anim, FadeIn(y_ticks), FadeIn(y_label))
        x_label = Text("AP@0.5", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        x_label.next_to(axes.x_axis, DOWN, buff=0.24)
        self.play(FadeIn(x_label), run_time=0.25)
        orange_pts = [(1.5, 1.8), (2.2, 1.5), (3.0, 2.3), (2.7, 1.1), (3.4, 2.0), (1.8, 2.7), (2.9, 2.8)]
        orange_dots = VGroup(*(
            Circle(
                radius=0.1,
                fill_color=ORANGE_INFRA,
                fill_opacity=1.0,
                stroke_color=INK_DARK,
                stroke_width=0.8,
            ).move_to(axes.c2p(*p))
            for p in orange_pts
        ))
        self.play(LaggedStart(*(FadeIn(d, shift=DOWN * 0.15) for d in orange_dots), lag_ratio=0.06))
        fail_label = Text("one-shot runs\ncollapse", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ORANGE_INFRA, weight=BOLD)
        fail_label.move_to(axes.c2p(2.3, 3.65))
        self.play(FadeIn(fail_label))
        blue_pts = [(4.0, 3.0), (5.2, 4.4), (6.5, 5.9), (7.8, 7.2)]
        dots = VGroup()
        for i, p in enumerate(blue_pts):
            d = Dot(radius=0.12)
            d.set_fill(ACCENT_BLUE, opacity=1.0)
            d.set_stroke(width=0)
            d.move_to(axes.c2p(*p))
            dots.add(d)
            self.play(FadeIn(d, shift=DOWN * 0.1), run_time=0.25)
        path = VMobject(stroke_color=ACCENT_BLUE, stroke_width=3).set_points_smoothly([axes.c2p(*p) for p in blue_pts])
        self.play(ShowCreation(path))
        divide = DashedLine(axes.c2p(3.7, 0.8), axes.c2p(7.2, 8.2), stroke_color=RED_ERROR, stroke_width=2)
        manual = Text("manual 4-stage\n120 epochs", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_BLUE, weight=BOLD)
        manual.move_to(RIGHT * 3.85 + UP * 1.15)
        label = Text("Unstable initialization + task conflict", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        label.to_edge(DOWN, buff=0.78)
        self.play(ShowCreation(divide), FadeIn(manual), FadeIn(label))
        self.wait(0.8)
        self._close()
