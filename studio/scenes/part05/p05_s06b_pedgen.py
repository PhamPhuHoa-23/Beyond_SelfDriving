"""P05-S06b PedGen: scene-aware pedestrian diffusion."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene,
    BG_PAPER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_AMBER,
    PASTEL_PINK,
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_AMBER,
    ACCENT_PINK,
    PURPLE_MODEL,
    RED_ERROR,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    pedestrian_icon,
)

SCRIPT = """PedGen conditions diffusion on scene geometry, body shape, and destination so generated pedestrians move around obstacles instead of through them."""


class P05S06BPedGen(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "PedGen: Scene-Aware Motion"

    def condition_card(self, title, visual, color):
        card = RoundedRectangle(
            width=2.25,
            height=1.22,
            corner_radius=0.12,
            fill_color=interpolate_color(color, WHITE, 0.84),
            fill_opacity=0.95,
            stroke_color=color,
            stroke_width=1.5,
        )
        visual.set_max_width(1.58)
        visual.set_max_height(0.58)
        visual.move_to(card.get_center() + DOWN * 0.08)
        label = Text(title, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=color, weight=BOLD)
        label.move_to(card.get_top() + DOWN * 0.18)
        return VGroup(card, visual, label)

    def voxel_visual(self):
        cells = VGroup()
        for r in range(3):
            for c in range(5):
                active = (r, c) in {(0, 1), (0, 2), (1, 2), (2, 4)}
                sq = Square(
                    side_length=0.18,
                    fill_color=ACCENT_BLUE if active else PASTEL_BLUE,
                    fill_opacity=0.9 if active else 0.32,
                    stroke_color=ACCENT_BLUE,
                    stroke_width=0.7,
                )
                sq.move_to(RIGHT * (c - 2) * 0.2 + DOWN * (r - 1) * 0.2)
                cells.add(sq)
        return cells

    def body_visual(self):
        small = pedestrian_icon(color=PURPLE_MODEL).scale(0.48)
        tall = pedestrian_icon(color=ACCENT_PINK).scale(0.65)
        return VGroup(small, tall).arrange(RIGHT, buff=0.28, aligned_edge=DOWN)

    def goal_visual(self):
        pin = VGroup(
            Circle(radius=0.15, fill_color=ACCENT_GREEN, fill_opacity=0.22, stroke_color=ACCENT_GREEN, stroke_width=1.5),
            Dot(radius=0.055, color=ACCENT_GREEN),
        )
        arrow = Arrow(LEFT * 0.72, RIGHT * 0.48, fill_color=ACCENT_GREEN, thickness=1.7, buff=0)
        return VGroup(arrow, pin).arrange(RIGHT, buff=0.05)

    def diffusion_model(self):
        shell = RoundedRectangle(
            width=2.45,
            height=3.45,
            corner_radius=0.16,
            fill_color=PASTEL_PINK,
            fill_opacity=0.48,
            stroke_color=ACCENT_PINK,
            stroke_width=2.0,
        )
        title = Text("diffusion", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_PINK, weight=BOLD)
        title.move_to(shell.get_top() + DOWN * 0.3)
        steps = VGroup()
        for i, alpha in enumerate([0.22, 0.4, 0.62, 0.9]):
            path = VMobject()
            y = 0.48 - i * 0.48
            points = [
                LEFT * 0.72 + UP * y,
                LEFT * 0.25 + UP * (y + (0.2 if i < 2 else 0.08)),
                RIGHT * 0.25 + UP * (y - (0.14 if i < 2 else 0.02)),
                RIGHT * 0.72 + UP * y,
            ]
            path.set_points_smoothly(points)
            path.set_stroke(PURPLE_MODEL, width=2.0, opacity=alpha)
            steps.add(path)
        steps.move_to(shell.get_center() + DOWN * 0.12)
        denoise = Text("noise \u2192 trajectory", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        denoise.move_to(shell.get_bottom() + UP * 0.25)
        return VGroup(shell, steps, title, denoise)

    def comparison_scene(self):
        panel = RoundedRectangle(
            width=4.7,
            height=3.45,
            corner_radius=0.14,
            fill_color="#F4F7EF",
            fill_opacity=1,
            stroke_color=ACCENT_GREEN,
            stroke_width=1.6,
        )
        grid = VGroup()
        for x in np.linspace(-2.0, 2.0, 9):
            grid.add(Line([x, -1.25, 0], [x, 1.25, 0], stroke_color=LINE_GRID, stroke_width=0.7))
        for y in np.linspace(-1.25, 1.25, 6):
            grid.add(Line([-2.0, y, 0], [2.0, y, 0], stroke_color=LINE_GRID, stroke_width=0.7))
        grid.move_to(panel)

        obstacle = Circle(
            radius=0.38,
            fill_color=PASTEL_AMBER,
            fill_opacity=0.92,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.5,
        )
        obstacle.move_to(panel.get_center())
        obstacle_label = Text("obstacle", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_AMBER)
        obstacle_label.move_to(obstacle)

        start = panel.get_left() + RIGHT * 0.45 + DOWN * 0.75
        goal = panel.get_right() + LEFT * 0.4 + UP * 0.72
        raw = DashedLine(start, goal, dash_length=0.12, stroke_color=RED_ERROR, stroke_width=2.2)
        legend_green = Line(LEFT * 0.3, RIGHT * 0.3, stroke_color=GREEN_FIX, stroke_width=3.0)
        legend_green_text = Text("with context", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=GREEN_FIX, weight=BOLD)
        legend_red = DashedLine(LEFT * 0.3, RIGHT * 0.3, dash_length=0.08, stroke_color=RED_ERROR, stroke_width=2.2)
        legend_red_text = Text("without context", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=RED_ERROR, weight=BOLD)
        legend = VGroup(
            VGroup(legend_green, legend_green_text).arrange(RIGHT, buff=0.1),
            VGroup(legend_red, legend_red_text).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.32)
        legend.move_to(panel.get_bottom() + UP * 0.22)

        aware = CubicBezier(
            start,
            panel.get_center() + LEFT * 1.15 + UP * 0.45,
            panel.get_center() + RIGHT * 0.95 + UP * 1.18,
            goal,
            stroke_color=GREEN_FIX,
            stroke_width=3.4,
        )
        aware_label = Text("generated trajectory", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GREEN_FIX, weight=BOLD)
        aware_label.move_to(panel.get_top() + DOWN * 0.25)

        ped = pedestrian_icon(color=ACCENT_PINK).scale(0.58)
        ped.move_to(start)
        goal_pin = VGroup(
            Circle(radius=0.16, stroke_color=ACCENT_GREEN, stroke_width=2.0),
            Dot(radius=0.055, color=ACCENT_GREEN),
        )
        goal_pin.move_to(goal)
        return VGroup(panel, grid, obstacle, obstacle_label, raw, legend, aware, aware_label, ped, goal_pin)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        inputs = VGroup(
            self.condition_card("SCENE VOXEL", self.voxel_visual(), ACCENT_BLUE),
            self.condition_card("BODY SHAPE", self.body_visual(), PURPLE_MODEL),
            self.condition_card("GOAL", self.goal_visual(), ACCENT_GREEN),
        ).arrange(DOWN, buff=0.22)
        inputs.move_to(LEFT * 5.0 + DOWN * 0.25)

        model = self.diffusion_model()
        model.move_to(LEFT * 1.9 + DOWN * 0.23)

        result = self.comparison_scene()
        result.move_to(RIGHT * 3.45 + DOWN * 0.18)

        arrows = VGroup()
        for card in inputs:
            y = card[0].get_center()[1]
            arrows.add(Arrow(
                [card[0].get_right()[0] + 0.08, y, 0],
                [model[0].get_left()[0] - 0.08, y, 0],
                fill_color=INK_MID,
                thickness=1.5,
                max_tip_length_to_length_ratio=0.18,
                buff=0,
            ))
        out = Arrow(
            model[0].get_right() + RIGHT * 0.08,
            result[0].get_left() + LEFT * 0.08,
            fill_color=ACCENT_PINK,
            thickness=2.2,
            max_tip_length_to_length_ratio=0.2,
            buff=0,
        )

        footer = Text(
            "context turns plausible body motion into safe urban behavior",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=INK_DARK,
        )
        footer.to_edge(DOWN, buff=0.42)

        self.play(LaggedStart(*(FadeIn(c, shift=RIGHT * 0.08) for c in inputs), lag_ratio=0.14), run_time=0.9)
        self.play(LaggedStart(*(ShowCreation(a) for a in arrows), lag_ratio=0.12), FadeIn(model[0]), FadeIn(model[2:]), run_time=0.8)
        self.play(LaggedStart(*(ShowCreation(p) for p in model[1]), lag_ratio=0.12), run_time=0.8)
        self.play(ShowCreation(out), FadeIn(result[:6]), run_time=0.75)
        self.play(ShowCreation(result[6]), FadeIn(result[7]), FadeIn(result[9]), run_time=0.65)
        self.play(FadeIn(result[8]), MoveAlongPath(result[8], result[6]), run_time=1.35, rate_func=smooth)
        self.play(FadeIn(footer, shift=UP * 0.08), run_time=0.45)
        self.wait(2.0)
        self._close()
