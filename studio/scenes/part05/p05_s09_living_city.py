"""P05-S09 Living City: a coherent 2D multi-agent urban system."""
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
    ACCENT_TEAL,
    ACCENT_GREEN,
    ACCENT_AMBER,
    ACCENT_PINK,
    ORANGE_INFRA,
    CYAN_RADAR,
    GOLD_KEY,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    vehicle_icon,
    pedestrian_icon,
    rsu_icon,
)

SCRIPT = """The living city is a coordinated urban system: vehicles follow lane direction, pedestrians occupy crosswalks, robots share space, and infrastructure connects nearby agents."""


class P05S09LivingCity(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "The Living City"

    def city_map(self):
        base = RoundedRectangle(
            width=11.7,
            height=5.25,
            corner_radius=0.16,
            fill_color="#F3F5EB",
            fill_opacity=1,
            stroke_color=ACCENT_TEAL,
            stroke_width=1.4,
        )
        hroad = Rectangle(width=11.1, height=1.3, fill_color="#CBD5DB", fill_opacity=1, stroke_width=0)
        vroad = Rectangle(width=1.3, height=4.75, fill_color="#CBD5DB", fill_opacity=1, stroke_width=0)
        hroad.move_to(base)
        vroad.move_to(base)

        lanes = VGroup(
            DashedLine(hroad.get_left() + UP * 0.02, hroad.get_right() + UP * 0.02, dash_length=0.18, stroke_color=WHITE, stroke_width=1.1, stroke_opacity=0.75),
            DashedLine(vroad.get_bottom() + RIGHT * 0.02, vroad.get_top() + RIGHT * 0.02, dash_length=0.18, stroke_color=WHITE, stroke_width=1.1, stroke_opacity=0.75),
        )

        direction_marks = VGroup()
        for x in [-4.15, -2.65, 2.65, 4.15]:
            direction_marks.add(Arrow([x - 0.22, -0.32, 0], [x + 0.22, -0.32, 0], fill_color=INK_MID, thickness=1.1, max_tip_length_to_length_ratio=0.4, buff=0))
            direction_marks.add(Arrow([x + 0.22, 0.32, 0], [x - 0.22, 0.32, 0], fill_color=INK_MID, thickness=1.1, max_tip_length_to_length_ratio=0.4, buff=0))
        for y in [-1.65, 1.65]:
            direction_marks.add(Arrow([0.32, y - 0.22, 0], [0.32, y + 0.22, 0], fill_color=INK_MID, thickness=1.1, max_tip_length_to_length_ratio=0.4, buff=0))
            direction_marks.add(Arrow([-0.32, y + 0.22, 0], [-0.32, y - 0.22, 0], fill_color=INK_MID, thickness=1.1, max_tip_length_to_length_ratio=0.4, buff=0))

        crosswalks = VGroup()
        for x in np.linspace(-0.48, 0.48, 6):
            crosswalks.add(Rectangle(width=0.08, height=0.42, fill_color=WHITE, fill_opacity=0.75, stroke_width=0).move_to([x, 0.94, 0]))
            crosswalks.add(Rectangle(width=0.08, height=0.42, fill_color=WHITE, fill_opacity=0.75, stroke_width=0).move_to([x, -0.94, 0]))
        for y in np.linspace(-0.48, 0.48, 6):
            crosswalks.add(Rectangle(width=0.42, height=0.08, fill_color=WHITE, fill_opacity=0.75, stroke_width=0).move_to([0.94, y, 0]))
            crosswalks.add(Rectangle(width=0.42, height=0.08, fill_color=WHITE, fill_opacity=0.75, stroke_width=0).move_to([-0.94, y, 0]))

        buildings = VGroup()
        building_specs = [
            (-4.4, 1.75, 1.35, 0.8, PASTEL_BLUE),
            (-2.45, 1.75, 1.15, 0.8, PASTEL_GREEN),
            (2.45, 1.75, 1.1, 0.8, PASTEL_AMBER),
            (4.35, 1.75, 1.3, 0.8, PASTEL_PINK),
            (-4.25, -1.78, 1.45, 0.76, PASTEL_AMBER),
            (-2.3, -1.78, 1.0, 0.76, PASTEL_PINK),
            (2.3, -1.78, 1.1, 0.76, PASTEL_BLUE),
            (4.25, -1.78, 1.35, 0.76, PASTEL_GREEN),
        ]
        for x, y, w, h, color in building_specs:
            b = RoundedRectangle(
                width=w,
                height=h,
                corner_radius=0.07,
                fill_color=color,
                fill_opacity=0.62,
                stroke_color=interpolate_color(color, INK_MID, 0.25),
                stroke_width=1.0,
            )
            b.move_to([x, y, 0])
            buildings.add(b)
        return VGroup(base, hroad, vroad, lanes, direction_marks, crosswalks, buildings)

    def car_with_path(self, start, end, color, angle=0):
        car = vehicle_icon(color=color, scale=0.32).rotate(angle)
        car.move_to(start)
        path = Line(start, end, stroke_color=color, stroke_width=1.4, stroke_opacity=0.32)
        return VGroup(path, car)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        city = self.city_map()
        city.move_to(DOWN * 0.25)

        cars = VGroup(
            self.car_with_path([-4.7, -0.57, 0], [4.7, -0.57, 0], ACCENT_BLUE, 0),
            self.car_with_path([4.7, 0.08, 0], [-4.7, 0.08, 0], ACCENT_TEAL, PI),
            self.car_with_path([0.57, -2.25, 0], [0.57, 2.05, 0], ACCENT_GREEN, PI / 2),
            self.car_with_path([-0.08, 2.05, 0], [-0.08, -2.25, 0], ACCENT_AMBER, -PI / 2),
        )
        cars.shift(DOWN * 0.25)

        robots = VGroup(
            vehicle_icon(color=ACCENT_PINK, scale=0.24).move_to([-3.1, 1.0, 0]),
            vehicle_icon(color=ACCENT_GREEN, scale=0.24).rotate(PI).move_to([3.2, -1.05, 0]),
        )
        robots.shift(DOWN * 0.25)

        peds = VGroup()
        for pos, color in [
            ([-0.32, 0.88, 0], GOLD_KEY),
            ([0.3, -0.95, 0], ACCENT_PINK),
            ([1.0, 0.28, 0], ACCENT_GREEN),
            ([-1.0, -0.26, 0], ACCENT_BLUE),
        ]:
            p = pedestrian_icon(color=color).scale(0.42)
            p.move_to(np.array(pos) + DOWN * 0.25)
            peds.add(p)

        rsus = VGroup()
        coverage = VGroup()
        for pos in [[-1.45, 1.28, 0], [1.45, -1.3, 0]]:
            rsu = rsu_icon(color=ORANGE_INFRA).scale(0.78)
            rsu.move_to(np.array(pos) + DOWN * 0.25)
            rsus.add(rsu)
            disc = Circle(radius=1.3, fill_color=CYAN_RADAR, fill_opacity=0.035, stroke_color=CYAN_RADAR, stroke_width=1.0, stroke_opacity=0.3)
            disc.move_to(rsu)
            coverage.add(disc)

        links = VGroup()
        for rsu, targets in [(rsus[0], [cars[0][1], cars[2][1], peds[0]]), (rsus[1], [cars[1][1], cars[3][1], robots[1]])]:
            for target in targets:
                links.add(DashedLine(rsu.get_center(), target.get_center(), dash_length=0.09, stroke_color=CYAN_RADAR, stroke_width=1.2, stroke_opacity=0.45))

        labels = VGroup(
            Text("lane-aware mobility", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_BLUE, weight=BOLD),
            Text("people + robots share space", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_PINK, weight=BOLD),
            Text("infrastructure coordinates locally", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_TEAL, weight=BOLD),
        ).arrange(RIGHT, buff=0.85)
        labels.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(city), run_time=0.8)
        self.play(LaggedStart(*(FadeIn(c) for c in cars), lag_ratio=0.12), FadeIn(robots), FadeIn(peds), run_time=0.9)
        self.play(FadeIn(coverage), FadeIn(rsus), LaggedStart(*(ShowCreation(l) for l in links), lag_ratio=0.05), run_time=0.9)
        self.play(
            *(MoveAlongPath(c[1], c[0]) for c in cars),
            run_time=2.4,
            rate_func=linear,
        )
        self.play(LaggedStart(*(FadeIn(label, shift=UP * 0.06) for label in labels), lag_ratio=0.12), run_time=0.7)
        self.wait(2.0)
        self._close()
