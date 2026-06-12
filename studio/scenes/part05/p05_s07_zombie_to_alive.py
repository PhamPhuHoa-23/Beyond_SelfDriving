"""P05-S07 From zombie simulation to human-centric behavior."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene,
    BG_PAPER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_PINK,
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_AMBER,
    ACCENT_PINK,
    RED_ERROR,
    GREEN_FIX,
    GOLD_RICH,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_H1,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    pedestrian_icon,
    vehicle_icon,
)

SCRIPT = """Human-centric physical AI is not just replacing dots with people: it models goals, personal space, and robot yielding around real human behavior."""


class P05S07ZombieToAlive(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Zombie City -> Human-Centric"

    def street_panel(self, title, color):
        panel = RoundedRectangle(
            width=5.5,
            height=3.75,
            corner_radius=0.14,
            fill_color="#F5F2E7",
            fill_opacity=1,
            stroke_color=color,
            stroke_width=1.6,
        )
        road = Rectangle(width=5.08, height=1.12, fill_color="#D9E2E7", fill_opacity=1, stroke_width=0)
        road.move_to(panel.get_center() + DOWN * 0.42)
        sidewalk = Rectangle(width=5.08, height=1.18, fill_color=PASTEL_GREEN, fill_opacity=0.22, stroke_width=0)
        sidewalk.next_to(road, UP, buff=0)
        crosswalk = VGroup()
        for i in range(6):
            stripe = Rectangle(width=0.1, height=1.08, fill_color=WHITE, fill_opacity=0.65, stroke_width=0)
            stripe.move_to(road.get_center() + RIGHT * (i - 2.5) * 0.18)
            crosswalk.add(stripe)
        buildings = VGroup()
        for x, y, w, h, fill in [
            (-1.9, 1.18, 0.85, 0.38, PASTEL_BLUE),
            (1.75, 1.18, 0.95, 0.38, PASTEL_PINK),
            (-2.0, -1.58, 0.9, 0.32, PASTEL_BLUE),
            (1.95, -1.58, 0.78, 0.32, PASTEL_PINK),
        ]:
            b = RoundedRectangle(width=w, height=h, corner_radius=0.05, fill_color=fill, fill_opacity=0.48, stroke_color=LINE_GRID, stroke_width=1.0)
            b.move_to(panel.get_center() + RIGHT * x + UP * y)
            buildings.add(b)
        label = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
        label.next_to(panel, UP, buff=0.14)
        return VGroup(panel, road, sidewalk, crosswalk, buildings, label)

    def zombie_side(self):
        panel = self.street_panel("no behavior model", RED_ERROR)
        origin = panel[0].get_center()
        peds = VGroup()
        paths = VGroup()
        starts = [LEFT * 2.1 + UP * 1.12, LEFT * 1.25 + UP * 1.12, RIGHT * 1.25 + UP * 1.1]
        ends = [RIGHT * 1.8 + DOWN * 1.15, RIGHT * 0.2 + DOWN * 1.2, LEFT * 1.65 + DOWN * 1.12]
        for i, (s, e) in enumerate(zip(starts, ends)):
            path = DashedLine(origin + s, origin + e, dash_length=0.11, stroke_color=RED_ERROR, stroke_width=2.0, stroke_opacity=0.75)
            ped = Square(side_length=0.22, fill_color="#6B7280", fill_opacity=0.9, stroke_width=0)
            ped.move_to(origin + s)
            paths.add(path)
            peds.add(ped)
        robot = vehicle_icon(color=ACCENT_PINK, scale=0.38).rotate(PI)
        robot.move_to(origin + RIGHT * 1.65 + DOWN * 0.42)
        robot_path = Line(origin + RIGHT * 2.25 + DOWN * 0.42, origin + LEFT * 1.35 + DOWN * 0.42, stroke_color=ACCENT_PINK, stroke_width=2.5)
        crash = VGroup(
            Line(LEFT * 0.18 + DOWN * 0.18, RIGHT * 0.18 + UP * 0.18, stroke_color=RED_ERROR, stroke_width=4),
            Line(LEFT * 0.18 + UP * 0.18, RIGHT * 0.18 + DOWN * 0.18, stroke_color=RED_ERROR, stroke_width=4),
        )
        crash.move_to(origin + RIGHT * 0.35 + DOWN * 0.42)
        caption = Text("straight paths ignore people", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
        caption.next_to(panel[0], DOWN, buff=0.14)
        return VGroup(panel, paths, peds, robot_path, robot, crash, caption)

    def human_side(self):
        panel = self.street_panel("human-centric model", GREEN_FIX)
        origin = panel[0].get_center()
        agents = VGroup()
        paths = VGroup()
        data = [
            (LEFT * 2.12 + UP * 1.08, LEFT * 1.05 + UP * 0.62, RIGHT * 0.12 + UP * 0.82, RIGHT * 1.72 + DOWN * 1.1, ACCENT_GREEN),
            (LEFT * 0.4 + UP * 1.18, LEFT * 0.08 + UP * 0.7, RIGHT * 0.62 + UP * 0.02, RIGHT * 0.28 + DOWN * 1.22, ACCENT_AMBER),
            (RIGHT * 2.05 + UP * 1.04, RIGHT * 1.12 + UP * 0.78, LEFT * 0.65 + UP * 0.42, LEFT * 1.8 + DOWN * 1.08, ACCENT_BLUE),
        ]
        for s, c1, c2, e, color in data:
            path = CubicBezier(origin + s, origin + c1, origin + c2, origin + e, stroke_color=color, stroke_width=2.8, stroke_opacity=0.85)
            ped = pedestrian_icon(color=color).scale(0.47)
            halo = Circle(radius=0.34, stroke_color=color, stroke_width=1.2, stroke_opacity=0.28, fill_color=color, fill_opacity=0.08)
            agent = VGroup(halo, ped)
            agent.move_to(path.get_start())
            paths.add(path)
            agents.add(agent)
        robot = vehicle_icon(color=ACCENT_PINK, scale=0.38).rotate(PI)
        robot.move_to(origin + RIGHT * 1.65 + DOWN * 0.42)
        yield_zone = Arc(radius=0.55, start_angle=PI * 0.15, angle=PI * 0.75, stroke_color=ACCENT_PINK, stroke_width=3.0)
        yield_zone.move_to(origin + RIGHT * 0.35 + DOWN * 0.35)
        yield_label = Text("yield", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_PINK, weight=BOLD)
        yield_label.next_to(yield_zone, UP, buff=0.02)
        robot_in = Line(
            origin + RIGHT * 2.3 + DOWN * 0.42,
            origin + RIGHT * 0.75 + DOWN * 0.42,
            stroke_color=ACCENT_PINK,
            stroke_width=2.7,
        )
        robot_detour = CubicBezier(
            origin + RIGHT * 0.75 + DOWN * 0.42,
            origin + RIGHT * 1.4 + DOWN * 0.75,
            origin + LEFT * 0.45 + DOWN * 0.75,
            origin + LEFT * 1.45 + DOWN * 0.42,
            stroke_color=ACCENT_PINK,
            stroke_width=2.7,
        )
        caption = Text("goals + personal space + yielding", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GREEN_FIX, weight=BOLD)
        caption.next_to(panel[0], DOWN, buff=0.14)
        return VGroup(panel, agents, robot, paths, robot_in, robot_detour, VGroup(yield_zone, yield_label), caption)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        left = self.zombie_side()
        left.move_to(LEFT * 3.25 + DOWN * 0.25)
        right = self.human_side()
        right.move_to(RIGHT * 3.25 + DOWN * 0.25)

        arrow = Arrow(
            left[0][0].get_right() + RIGHT * 0.18,
            right[0][0].get_left() + LEFT * 0.18,
            fill_color=GOLD_RICH,
            thickness=2.5,
            max_tip_length_to_length_ratio=0.18,
            buff=0,
        )
        bridge = Text("behavior\nmodel", font=FONT_PRIMARY, font_size=15, color=GOLD_RICH, weight=BOLD)
        bridge.move_to(arrow.get_center() + UP * 0.32)

        footer = Text("human-centric means the robot reasons about people before it moves", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        footer.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(left[0]), FadeIn(left[1]), FadeIn(left[2]), FadeIn(left[3]), FadeIn(left[4]), run_time=0.8)
        self.play(MoveAlongPath(left[4], left[3]), FadeIn(left[5]), FadeIn(left[6]), run_time=1.2, rate_func=smooth)
        self.play(ShowCreation(arrow), FadeIn(bridge), run_time=0.5)
        self.play(FadeIn(right[0]), FadeIn(right[1]), FadeIn(right[2]), run_time=0.7)
        ped_traces = VGroup()
        for agent, path in zip(right[1], right[3]):
            ped_traces.add(TracedPath(agent.get_center, stroke_color=path.get_color(), stroke_width=2.8, stroke_opacity=0.85, time_traced=10))
        robot_trace = TracedPath(right[2].get_center, stroke_color=ACCENT_PINK, stroke_width=2.7, stroke_opacity=0.9, time_traced=10)
        self.add(ped_traces, robot_trace)
        first_cuts = [0.48, 0.34, 0.58]
        first_paths = VGroup()
        second_paths = VGroup()
        for path, cut in zip(right[3], first_cuts):
            first = path.copy()
            first.pointwise_become_partial(path, 0, cut)
            second = path.copy()
            second.pointwise_become_partial(path, cut, 1)
            first_paths.add(first)
            second_paths.add(second)
        self.play(
            LaggedStart(*(MoveAlongPath(agent, path) for agent, path in zip(right[1], first_paths)), lag_ratio=0.04),
            MoveAlongPath(right[2], right[4]),
            run_time=1.15,
            rate_func=smooth,
        )
        self.play(FadeIn(right[6], scale=0.9), run_time=0.35)
        self.play(
            LaggedStart(*(MoveAlongPath(agent, path) for agent, path in zip(right[1], second_paths)), lag_ratio=0.04),
            MoveAlongPath(right[2], right[5]),
            run_time=1.15,
            rate_func=smooth,
        )
        self.play(FadeIn(right[7]), run_time=0.25)
        self.play(FadeIn(footer, shift=UP * 0.08), run_time=0.45)
        self.wait(2.0)
        self._close()
