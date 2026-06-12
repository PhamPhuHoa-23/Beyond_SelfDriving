"""P05-S06a CityWalker: pedestrian behavior in urban context."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene,
    BG_PAPER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_AMBER,
    ACCENT_BLUE,
    ACCENT_TEAL,
    ACCENT_GREEN,
    ACCENT_AMBER,
    ACCENT_PINK,
    GOLD_RICH,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    pedestrian_icon,
    vehicle_icon,
)

SCRIPT = """CityWalker captures real pedestrian behavior in context: 30.8 hours, 120,914 pedestrians, 16,215 scenes, and 227 cities."""


class P05S06ACityWalker(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "CityWalker Dataset"

    def city_view(self):
        panel = RoundedRectangle(
            width=7.2,
            height=4.15,
            corner_radius=0.14,
            fill_color="#F4F7EF",
            fill_opacity=1,
            stroke_color=ACCENT_TEAL,
            stroke_width=1.6,
        )
        road = Rectangle(width=6.75, height=1.18, fill_color="#D9E2E7", fill_opacity=1, stroke_width=0)
        road.move_to(panel.get_center() + DOWN * 0.55)
        sidewalk_top = Rectangle(width=6.75, height=0.92, fill_color="#EAF4DF", fill_opacity=1, stroke_width=0)
        sidewalk_top.next_to(road, UP, buff=0)
        sidewalk_bot = Rectangle(width=6.75, height=0.88, fill_color="#F8EBC8", fill_opacity=1, stroke_width=0)
        sidewalk_bot.next_to(road, DOWN, buff=0)

        crosswalk = VGroup()
        for i in range(6):
            stripe = Rectangle(width=0.08, height=1.1, fill_color=WHITE, fill_opacity=0.7, stroke_width=0)
            stripe.move_to(road.get_center() + LEFT * 0.35 + RIGHT * i * 0.16)
            crosswalk.add(stripe)

        blocks = VGroup()
        for x, y, w, h, color in [
            (-2.65, 1.13, 1.0, 0.38, PASTEL_BLUE),
            (-1.25, 1.16, 0.78, 0.35, PASTEL_AMBER),
            (1.85, 1.14, 1.05, 0.38, PASTEL_GREEN),
            (2.95, -1.73, 0.82, 0.36, PASTEL_BLUE),
            (-2.85, -1.78, 1.15, 0.32, PASTEL_GREEN),
        ]:
            b = RoundedRectangle(
                width=w,
                height=h,
                corner_radius=0.06,
                fill_color=color,
                fill_opacity=0.55,
                stroke_color=interpolate_color(color, INK_MID, 0.2),
                stroke_width=1.0,
            )
            b.move_to(panel.get_center() + RIGHT * x + UP * y)
            blocks.add(b)

        car = vehicle_icon(color=ACCENT_BLUE, scale=0.26)
        car.move_to(road.get_center() + LEFT * 2.25 + DOWN * 0.18)

        paths = VGroup()
        peds = VGroup()
        data = [
            ([-2.7, -1.7, 0], [-1.55, -0.6, 0], [-0.25, 0.38, 0], [0.55, 1.18, 0], ACCENT_PINK),
            ([2.8, 1.28, 0], [1.42, 0.62, 0], [0.65, -0.45, 0], [-0.7, -1.38, 0], ACCENT_GREEN),
            ([-0.1, 1.38, 0], [0.38, 0.86, 0], [0.18, 0.08, 0], [1.55, -1.55, 0], ACCENT_AMBER),
            ([-3.0, 0.9, 0], [-1.9, 0.78, 0], [-0.9, 0.64, 0], [0.05, 0.44, 0], ACCENT_TEAL),
        ]
        for start, c1, c2, end, color in data:
            curve = CubicBezier(
                panel.get_center() + np.array(start),
                panel.get_center() + np.array(c1),
                panel.get_center() + np.array(c2),
                panel.get_center() + np.array(end),
                stroke_color=color,
                stroke_width=3.0,
                stroke_opacity=0.85,
            )
            paths.add(curve)
            ped = pedestrian_icon(color=color).scale(0.46)
            ped.move_to(curve.get_start())
            peds.add(ped)

        tags = VGroup()
        for label, pos, color in [
            ("stroller", LEFT * 2.05 + DOWN * 1.83, ACCENT_AMBER),
            ("photo stop", LEFT * 0.28 + UP * 1.38, ACCENT_TEAL),
            ("jaywalk", RIGHT * 1.85 + DOWN * 0.85, ACCENT_PINK),
        ]:
            tag = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=color, weight=BOLD)
            tag.move_to(panel.get_center() + pos)
            tags.add(tag)

        title = Text("real pedestrian trajectories in context", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        title.next_to(panel, UP, buff=0.14)
        return VGroup(panel, road, sidewalk_top, sidewalk_bot, blocks, crosswalk, car, paths, peds, tags, title)

    def metric(self, number, label, color):
        card = RoundedRectangle(
            width=1.75,
            height=0.84,
            corner_radius=0.09,
            fill_color=interpolate_color(color, WHITE, 0.83),
            fill_opacity=0.95,
            stroke_color=color,
            stroke_width=1.4,
        )
        n = Text(number, font=FONT_PRIMARY, font_size=30, color=color)
        l = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
        VGroup(n, l).arrange(DOWN, buff=0.03).move_to(card)
        return VGroup(card, n, l)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        view = self.city_view()
        view.move_to(LEFT * 2.25 + DOWN * 0.05)

        metrics = VGroup(
            self.metric("30.8h", "video", GOLD_RICH),
            self.metric("120,914", "pedestrians", ACCENT_PINK),
            self.metric("16,215", "scenes", ACCENT_GREEN),
            self.metric("227", "cities", ACCENT_TEAL),
        ).arrange(DOWN, buff=0.2)
        metrics.move_to(RIGHT * 4.15 + DOWN * 0.05)

        bottom = Text(
            "not motion-capture in isolation: behavior tied to sidewalks, obstacles, and goals",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=INK_MID,
        )
        bottom.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(view[:7]), FadeIn(view[-1]), run_time=0.75)
        self.play(LaggedStart(*(FadeIn(p, scale=0.75) for p in view[8]), lag_ratio=0.1), run_time=0.5)
        trails = VGroup()
        for ped, path in zip(view[8], view[7]):
            trail = TracedPath(
                ped.get_center,
                stroke_color=path.get_color(),
                stroke_width=3.0,
                stroke_opacity=0.82,
                time_traced=10,
            )
            trails.add(trail)
        self.add(trails)
        self.play(
            LaggedStart(*(MoveAlongPath(ped, path) for ped, path in zip(view[8], view[7])), lag_ratio=0.08),
            FadeIn(view[9]),
            run_time=1.65,
            rate_func=smooth,
        )
        self.play(LaggedStart(*(FadeIn(m, shift=LEFT * 0.08) for m in metrics), lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(bottom, shift=UP * 0.08), run_time=0.45)
        self.wait(2.0)
        self._close()
