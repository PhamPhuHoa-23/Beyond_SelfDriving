"""P05-S07 From zombie simulation to a living city."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene,
    BG_PAPER,
    BG_CARD,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_AMBER,
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
    INK_LIGHT,
    LINE_GRID,
    LINE_SEP,
    FONT_PRIMARY,
    SIZE_H1,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    pedestrian_icon,
    vehicle_icon,
    sensor_cone,
    agent_trail,
)

SCRIPT = """Simulation environments without realistic pedestrian models are often described as "zombie cities" — populated with agents that move mechanically, without behavioral intent or social awareness. These agents don't react to robots, don't avoid each other naturally, and don't produce the kind of social dynamics that real urban environments contain.

PedGen begins the transition from zombie city to living city. When pedestrians are generated with scene-aware, goal-conditioned motion, the simulation environment starts to exhibit the emergent social dynamics — crowd dispersion, path negotiation, stopping-and-starting — that any robot deployed in a real city will need to navigate."""


class P05S07ZombieToAlive(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Zombie City -> Human-Centric"

    def stage_point(self, stage, x, y):
        return stage["shell"].get_center() + stage["scale"] * (RIGHT * x + UP * y)

    def city_stage(self, *, center=ORIGIN, scale=1.0):
        shell = RoundedRectangle(
            width=12.2,
            height=4.75,
            corner_radius=0.18,
            fill_color=interpolate_color(BG_PAPER, PASTEL_GREEN, 0.16),
            fill_opacity=1.0,
            stroke_color=LINE_SEP,
            stroke_width=1.5,
        )
        h_road = Rectangle(
            width=11.75,
            height=1.34,
            fill_color=LINE_SEP,
            fill_opacity=1.0,
            stroke_width=0,
        )
        h_road.move_to(DOWN * 0.28)
        v_road = Rectangle(
            width=1.46,
            height=4.35,
            fill_color=LINE_SEP,
            fill_opacity=1.0,
            stroke_width=0,
        )
        v_road.move_to(RIGHT * 0.72)

        lane_marks = VGroup(
            DashedLine(
                LEFT * 5.72 + DOWN * 0.28,
                RIGHT * 5.72 + DOWN * 0.28,
                dash_length=0.2,
                stroke_color=WHITE,
                stroke_width=1.2,
                stroke_opacity=0.8,
            ),
            DashedLine(
                RIGHT * 0.72 + DOWN * 2.08,
                RIGHT * 0.72 + UP * 2.08,
                dash_length=0.2,
                stroke_color=WHITE,
                stroke_width=1.2,
                stroke_opacity=0.8,
            ),
        )

        crosswalks = VGroup()
        for x in np.linspace(0.12, 1.32, 7):
            for y in (-1.05, 0.49):
                stripe = Rectangle(
                    width=0.1,
                    height=0.42,
                    fill_color=WHITE,
                    fill_opacity=0.82,
                    stroke_width=0,
                )
                stripe.move_to(RIGHT * x + UP * y)
                crosswalks.add(stripe)
        for y in np.linspace(-0.88, 0.3, 7):
            for x in (-0.12, 1.56):
                stripe = Rectangle(
                    width=0.42,
                    height=0.1,
                    fill_color=WHITE,
                    fill_opacity=0.82,
                    stroke_width=0,
                )
                stripe.move_to(RIGHT * x + UP * y)
                crosswalks.add(stripe)

        buildings = VGroup()
        specs = [
            (-4.7, 1.45, 1.25, 0.72, PASTEL_BLUE),
            (-2.85, 1.45, 1.05, 0.72, PASTEL_GREEN),
            (2.65, 1.45, 1.1, 0.72, PASTEL_AMBER),
            (4.65, 1.45, 1.35, 0.72, PASTEL_PINK),
            (-4.55, -1.67, 1.45, 0.68, PASTEL_AMBER),
            (-2.65, -1.67, 1.05, 0.68, PASTEL_PINK),
            (2.65, -1.67, 1.05, 0.68, PASTEL_BLUE),
            (4.55, -1.67, 1.35, 0.68, PASTEL_GREEN),
        ]
        for x, y, width, height, color in specs:
            building = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.08,
                fill_color=color,
                fill_opacity=0.56,
                stroke_color=interpolate_color(color, INK_MID, 0.25),
                stroke_width=1.0,
            )
            building.move_to(RIGHT * x + UP * y)
            buildings.add(building)

        plaza = RoundedRectangle(
            width=1.2,
            height=0.56,
            corner_radius=0.08,
            fill_color=PASTEL_AMBER,
            fill_opacity=0.7,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.0,
        )
        plaza.move_to(LEFT * 0.65 + UP * 1.34)

        base = VGroup(
            shell,
            h_road,
            v_road,
            lane_marks,
            crosswalks,
            buildings,
            plaza,
        )
        base.scale(scale)
        base.move_to(center)
        return {
            "base": base,
            "shell": shell,
            "roads": VGroup(h_road, v_road),
            "crosswalks": crosswalks,
            "buildings": buildings,
            "plaza": plaza,
            "scale": scale,
        }

    def zombie_agents(self, stage):
        starts = [
            (-5.1, 1.18),
            (-4.9, -1.22),
            (-5.15, 0.63),
            (4.9, -0.78),
            (-1.35, 1.88),
            (3.25, 1.78),
        ]
        ends = [
            (4.9, -1.22),
            (4.95, 1.22),
            (5.0, 0.63),
            (-4.9, -0.78),
            (2.35, -1.88),
            (-2.8, -1.75),
        ]
        agents = VGroup()
        paths = VGroup()
        for start, end in zip(starts, ends):
            path = Line(
                self.stage_point(stage, *start),
                self.stage_point(stage, *end),
                stroke_color=INK_LIGHT,
                stroke_width=1.7,
                stroke_opacity=0.42,
            )
            agent = Square(
                side_length=0.22,
                fill_color=INK_LIGHT,
                fill_opacity=0.92,
                stroke_width=0,
            )
            agent.move_to(path.get_start())
            paths.add(path)
            agents.add(agent)
        return {"agents": agents, "paths": paths}

    def human_agent(self, position, color, *, scale=0.48, halo_radius=0.34):
        icon = pedestrian_icon(color=color).scale(scale)
        icon.move_to(position)
        halo = Circle(
            radius=halo_radius,
            fill_color=color,
            fill_opacity=0.07,
            stroke_color=color,
            stroke_width=1.15,
            stroke_opacity=0.28,
        )
        halo.move_to(position)
        return {"icon": icon, "halo": halo, "group": VGroup(halo, icon)}

    def diagnostic_chip(self, label):
        shell = RoundedRectangle(
            width=1.75,
            height=0.48,
            corner_radius=0.1,
            fill_color=PASTEL_PINK,
            fill_opacity=0.78,
            stroke_color=RED_ERROR,
            stroke_width=1.35,
        )
        text = Text(
            label,
            font=FONT_PRIMARY,
            font_size=13,
            color=RED_ERROR,
            weight=BOLD,
        )
        text.move_to(shell)
        return VGroup(shell, text)

    def token(self, label, color, *, width=0.95):
        shell = RoundedRectangle(
            width=width,
            height=0.48,
            corner_radius=0.1,
            fill_color=interpolate_color(color, WHITE, 0.84),
            fill_opacity=0.98,
            stroke_color=color,
            stroke_width=1.35,
        )
        text = Text(
            label,
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=color,
            weight=BOLD,
        )
        text.move_to(shell)
        return VGroup(shell, text)

    def behavior_bridge(self):
        scene = self.token("SCENE", ACCENT_BLUE)
        goal = self.token("GOAL", ACCENT_GREEN)
        plus = Text(
            "+",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=INK_MID,
            weight=BOLD,
        )
        model = self.token("BEHAVIOR", GOLD_RICH, width=1.45)
        inputs = VGroup(scene, plus, goal).arrange(RIGHT, buff=0.12)
        arrow = Arrow(
            inputs.get_right() + RIGHT * 0.1,
            inputs.get_right() + RIGHT * 0.85,
            fill_color=GOLD_RICH,
            thickness=1.8,
            buff=0,
        )
        model.next_to(arrow, RIGHT, buff=0.08)
        group = VGroup(inputs, arrow, model)
        group.move_to(RIGHT * 3.25 + UP * 1.6)
        return {
            "group": group,
            "inputs": inputs,
            "arrow": arrow,
            "model": model,
        }

    def interaction_chip(self, label, x):
        chip = self.token(label, GREEN_FIX, width=2.25)
        chip.move_to(RIGHT * x + UP * 2.48)
        return chip

    def partial_path(self, path, start, end):
        part = path.copy()
        part.pointwise_become_partial(path, start, end)
        return part

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # 1.0-4.2: Establish a mechanical zombie city.
        zombie_stage = self.city_stage(center=DOWN * 0.28)
        zombie = self.zombie_agents(zombie_stage)
        zombie_label = Text(
            "ZOMBIE CITY",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_MID,
            weight=BOLD,
        )
        zombie_label.move_to(zombie_stage["shell"].get_top() + DOWN * 0.23)
        self.play(FadeIn(zombie_stage["base"]), run_time=0.7)
        self.play(
            LaggedStart(
                *(FadeIn(agent, scale=0.7) for agent in zombie["agents"]),
                lag_ratio=0.08,
            ),
            FadeIn(zombie_label),
            run_time=0.5,
        )
        zombie_trails = VGroup(
            *(agent_trail(agent, color=INK_LIGHT) for agent in zombie["agents"])
        )
        self.add(zombie_trails)
        self.play(
            *(MoveAlongPath(agent, path) for agent, path in zip(zombie["agents"], zombie["paths"])),
            run_time=1.5,
            rate_func=linear,
        )
        self.play(
            FadeOut(zombie_trails),
            Indicate(zombie_label, color=INK_LIGHT, scale_factor=1.04),
            run_time=0.5,
        )

        # 4.2-8.2: The agents ignore a robot, each other, and the social scene.
        robot = vehicle_icon(color=ACCENT_PINK, scale=0.38).rotate(PI)
        robot_path = Line(
            self.stage_point(zombie_stage, 5.2, -0.28),
            self.stage_point(zombie_stage, 0.72, -0.28),
            stroke_color=ACCENT_PINK,
            stroke_width=2.5,
        )
        robot.move_to(robot_path.get_start())
        crossing = Square(
            side_length=0.24,
            fill_color=INK_LIGHT,
            fill_opacity=0.95,
            stroke_width=0,
        )
        crossing_path = Line(
            self.stage_point(zombie_stage, 0.72, 1.85),
            self.stage_point(zombie_stage, 0.72, -0.28),
            stroke_color=INK_LIGHT,
            stroke_width=1.7,
            stroke_opacity=0.5,
        )
        crossing.move_to(crossing_path.get_start())
        robot_trails = VGroup(
            agent_trail(robot, color=ACCENT_PINK),
            agent_trail(crossing, color=INK_LIGHT),
        )
        self.play(
            FadeIn(robot, shift=LEFT * 0.08),
            FadeIn(crossing),
            zombie["agents"].animate.set_opacity(0.38),
            run_time=0.4,
        )
        self.add(robot_trails)
        self.play(
            MoveAlongPath(robot, robot_path),
            MoveAlongPath(crossing, crossing_path),
            run_time=1.2,
            rate_func=linear,
        )
        crash = VGroup(
            Line(LEFT * 0.18, RIGHT * 0.18, stroke_color=RED_ERROR, stroke_width=4).rotate(PI / 4),
            Line(LEFT * 0.18, RIGHT * 0.18, stroke_color=RED_ERROR, stroke_width=4).rotate(-PI / 4),
        )
        crash.move_to(robot)
        self.play(
            FadeIn(crash, scale=1.35),
            Flash(robot, color=RED_ERROR, line_length=0.16, num_lines=8),
            FadeOut(robot_trails),
            run_time=0.35,
        )

        pass_a = Square(
            side_length=0.24,
            fill_color=INK_LIGHT,
            fill_opacity=0.95,
            stroke_width=0,
        )
        pass_b = pass_a.copy()
        pass_a_path = Line(
            self.stage_point(zombie_stage, -2.0, 1.02),
            self.stage_point(zombie_stage, 2.0, 1.02),
            stroke_color=RED_ERROR,
            stroke_width=1.8,
            stroke_opacity=0.45,
        )
        pass_b_path = Line(
            self.stage_point(zombie_stage, 2.0, 1.02),
            self.stage_point(zombie_stage, -2.0, 1.02),
            stroke_color=RED_ERROR,
            stroke_width=1.8,
            stroke_opacity=0.45,
        )
        pass_a.move_to(pass_a_path.get_start())
        pass_b.move_to(pass_b_path.get_start())
        pass_a_first = self.partial_path(pass_a_path, 0, 0.5)
        pass_a_second = self.partial_path(pass_a_path, 0.5, 1)
        pass_b_first = self.partial_path(pass_b_path, 0, 0.5)
        pass_b_second = self.partial_path(pass_b_path, 0.5, 1)
        pass_trails = VGroup(
            agent_trail(pass_a, color=RED_ERROR),
            agent_trail(pass_b, color=RED_ERROR),
        )
        self.play(
            FadeIn(pass_a),
            FadeIn(pass_b),
            run_time=0.15,
        )
        self.add(pass_trails)
        self.play(
            MoveAlongPath(pass_a, pass_a_first),
            MoveAlongPath(pass_b, pass_b_first),
            run_time=0.4,
            rate_func=linear,
        )
        overlap_marker = Circle(
            radius=0.22,
            stroke_color=RED_ERROR,
            stroke_width=3.0,
            fill_color=RED_ERROR,
            fill_opacity=0.1,
        )
        overlap_marker.move_to(pass_a)
        self.play(
            FadeIn(overlap_marker, scale=1.4),
            Flash(pass_a, color=RED_ERROR, line_length=0.12, num_lines=7),
            run_time=0.15,
        )
        self.play(
            MoveAlongPath(pass_a, pass_a_second),
            MoveAlongPath(pass_b, pass_b_second),
            FadeOut(overlap_marker),
            FadeOut(pass_trails),
            run_time=0.4,
            rate_func=linear,
        )
        self.play(
            LaggedStart(
                *(Indicate(agent, color=RED_ERROR, scale_factor=1.16) for agent in zombie["agents"]),
                lag_ratio=0.06,
            ),
            run_time=0.55,
        )
        mechanical = Text(
            "motion without intent",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=RED_ERROR,
            weight=BOLD,
        )
        mechanical.move_to(DOWN * 2.95)
        self.play(FadeIn(mechanical, shift=UP * 0.06), run_time=0.4)

        # 8.2-10.8: Shrink the failed city into a diagnostic comparison.
        zombie_world = VGroup(
            zombie_stage["base"],
            zombie["agents"],
            zombie_label,
            robot,
            crossing,
            crash,
            pass_a,
            pass_b,
            mechanical,
        )
        self.play(
            zombie_world.animate.scale(0.46).move_to(LEFT * 3.25 + DOWN * 0.35),
            run_time=0.8,
            rate_func=smooth,
        )
        diagnostic_chips = VGroup(
            self.diagnostic_chip("no reaction"),
            self.diagnostic_chip("no avoidance"),
            self.diagnostic_chip("no social dynamics"),
        ).arrange(RIGHT, buff=0.12)
        diagnostic_chips.move_to(LEFT * 3.25 + DOWN * 2.05)
        self.play(
            LaggedStart(
                *(FadeIn(chip, shift=UP * 0.08) for chip in diagnostic_chips),
                lag_ratio=0.18,
            ),
            run_time=1.2,
        )
        mechanical_heading = Text(
            "MECHANICAL AGENTS",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=RED_ERROR,
            weight=BOLD,
        )
        mechanical_heading.move_to(LEFT * 3.25 + UP * 1.35)
        self.play(
            FadeIn(mechanical_heading),
            Indicate(diagnostic_chips, color=RED_ERROR, scale_factor=1.02),
            run_time=0.6,
        )

        # 10.8-14.2: Scene and goal conditioning activate a behavior model.
        right_stage = self.city_stage(center=RIGHT * 3.25 + DOWN * 0.42, scale=0.46)
        self.play(FadeIn(right_stage["base"]), run_time=0.55)

        bridge = self.behavior_bridge()
        self.play(
            FadeIn(bridge["inputs"], shift=RIGHT * 0.08),
            ShowCreation(bridge["arrow"]),
            FadeIn(bridge["model"], scale=0.85),
            run_time=0.7,
        )

        preview_specs = [
            (-2.15, 0.78, ACCENT_GREEN),
            (-0.65, 1.15, ACCENT_AMBER),
            (1.75, 0.75, ACCENT_BLUE),
            (2.2, -1.12, ACCENT_PINK),
        ]
        preview_squares = VGroup()
        preview_people = VGroup()
        preview_halos = VGroup()
        preview_goals = VGroup()
        for x, y, color in preview_specs:
            position = self.stage_point(right_stage, x, y)
            square = Square(
                side_length=0.12,
                fill_color=INK_LIGHT,
                fill_opacity=0.9,
                stroke_width=0,
            )
            square.move_to(position)
            person = self.human_agent(position, color, scale=0.23, halo_radius=0.16)
            goal = Dot(
                radius=0.035,
                color=color,
            )
            goal.move_to(position + RIGHT * 0.42 + DOWN * 0.12)
            preview_squares.add(square)
            preview_people.add(person["icon"])
            preview_halos.add(person["halo"])
            preview_goals.add(goal)
        self.add(preview_squares)
        self.play(
            ReplacementTransform(preview_squares, preview_people),
            Flash(bridge["model"], color=GOLD_RICH, line_length=0.1, num_lines=7),
            run_time=0.75,
        )
        self.play(
            LaggedStart(
                *(FadeIn(halo, scale=0.7) for halo in preview_halos),
                *(FadeIn(goal, scale=0.7) for goal in preview_goals),
                lag_ratio=0.08,
            ),
            run_time=0.4,
        )

        living_stage = self.city_stage(center=DOWN * 0.28)
        ambient_people = VGroup()
        ambient_halos = VGroup()
        for x, y, color in preview_specs:
            person = self.human_agent(
                self.stage_point(living_stage, x, y),
                color,
                scale=0.48,
                halo_radius=0.34,
            )
            person["icon"].set_opacity(0.32)
            person["halo"].set_opacity(0.12)
            ambient_people.add(person["icon"])
            ambient_halos.add(person["halo"])
        self.play(
            FadeOut(zombie_world, shift=LEFT * 0.2),
            FadeOut(diagnostic_chips),
            FadeOut(mechanical_heading),
            FadeOut(bridge["group"]),
            FadeOut(preview_goals),
            ReplacementTransform(right_stage["base"], living_stage["base"]),
            ReplacementTransform(preview_people, ambient_people),
            ReplacementTransform(preview_halos, ambient_halos),
            run_time=1.0,
            rate_func=smooth,
        )

        # 14.2-17.7: Crowd dispersion around a robot.
        dispersion_label = self.interaction_chip("crowd dispersion", -4.0)
        blocker = vehicle_icon(color=ACCENT_PINK, scale=0.34)
        blocker.move_to(self.stage_point(living_stage, -0.35, 0.38))
        dispersion_colors = [
            ACCENT_GREEN,
            ACCENT_AMBER,
            ACCENT_BLUE,
            ACCENT_GREEN,
            ACCENT_AMBER,
        ]
        starts = [
            (-4.55, 0.72),
            (-4.48, 0.54),
            (-4.38, 0.35),
            (-4.52, 0.16),
            (-4.36, -0.02),
        ]
        ends = [
            (2.4, 1.82),
            (3.2, 1.1),
            (3.75, 0.36),
            (3.05, -1.02),
            (1.95, -1.72),
        ]
        dispersion_agents = VGroup()
        dispersion_paths = VGroup()
        dispersion_trails = VGroup()
        for index, (start, end, color) in enumerate(zip(starts, ends, dispersion_colors)):
            start_point = self.stage_point(living_stage, *start)
            end_point = self.stage_point(living_stage, *end)
            bend = 0.85 - index * 0.42
            path = CubicBezier(
                start_point,
                self.stage_point(living_stage, -2.0, 0.55 + bend),
                self.stage_point(living_stage, 0.8, 0.4 + bend),
                end_point,
                stroke_color=color,
                stroke_width=2.2,
                stroke_opacity=0.42,
            )
            person = self.human_agent(start_point, color)
            dispersion_agents.add(person["group"])
            dispersion_paths.add(path)
            dispersion_trails.add(agent_trail(person["group"], color=color))
        self.play(
            FadeIn(dispersion_label, shift=DOWN * 0.06),
            FadeIn(blocker, scale=0.8),
            LaggedStart(
                *(FadeIn(agent, scale=0.75) for agent in dispersion_agents),
                lag_ratio=0.06,
            ),
            run_time=0.4,
        )
        self.add(dispersion_trails)
        self.play(
            LaggedStart(
                *(ShowCreation(path) for path in dispersion_paths),
                lag_ratio=0.04,
            ),
            *(
                MoveAlongPath(agent, path)
                for agent, path in zip(dispersion_agents, dispersion_paths)
            ),
            run_time=2.4,
            rate_func=smooth,
        )
        self.play(
            FadeOut(dispersion_agents),
            FadeOut(dispersion_paths),
            FadeOut(dispersion_trails),
            FadeOut(blocker),
            run_time=0.7,
        )

        # 17.7-21.2: Two people negotiate a narrow path instead of overlapping.
        negotiation_label = self.interaction_chip("path negotiation", 0.0)
        person_a = self.human_agent(
            self.stage_point(living_stage, -3.4, 1.03),
            ACCENT_BLUE,
        )
        person_b = self.human_agent(
            self.stage_point(living_stage, 3.45, 1.03),
            ACCENT_AMBER,
        )
        path_a = CubicBezier(
            person_a["group"].get_center(),
            self.stage_point(living_stage, -1.4, 1.02),
            self.stage_point(living_stage, 0.35, 0.68),
            self.stage_point(living_stage, 3.4, 0.92),
            stroke_color=ACCENT_BLUE,
            stroke_width=2.2,
            stroke_opacity=0.48,
        )
        path_b_approach = CubicBezier(
            person_b["group"].get_center(),
            self.stage_point(living_stage, 2.2, 1.02),
            self.stage_point(living_stage, 1.35, 1.03),
            self.stage_point(living_stage, 0.98, 1.05),
            stroke_color=ACCENT_AMBER,
            stroke_width=2.2,
            stroke_opacity=0.48,
        )
        side_step = Line(
            path_b_approach.get_end(),
            path_b_approach.get_end() + UP * 0.48,
            stroke_color=ACCENT_AMBER,
            stroke_width=2.2,
            stroke_opacity=0.48,
        )
        path_b_resume = CubicBezier(
            side_step.get_end(),
            self.stage_point(living_stage, 0.1, 1.58),
            self.stage_point(living_stage, -1.75, 1.35),
            self.stage_point(living_stage, -3.4, 1.1),
            stroke_color=ACCENT_AMBER,
            stroke_width=2.2,
            stroke_opacity=0.48,
        )
        a_approach = self.partial_path(path_a, 0, 0.44)
        a_pass = self.partial_path(path_a, 0.44, 1)
        negotiation_trails = VGroup(
            agent_trail(person_a["group"], color=ACCENT_BLUE),
            agent_trail(person_b["group"], color=ACCENT_AMBER),
        )
        self.play(
            FadeIn(negotiation_label, shift=DOWN * 0.06),
            FadeIn(person_a["group"]),
            FadeIn(person_b["group"]),
            run_time=0.4,
        )
        self.add(negotiation_trails)
        self.play(
            MoveAlongPath(person_a["group"], a_approach),
            MoveAlongPath(person_b["group"], path_b_approach),
            ShowCreation(a_approach),
            ShowCreation(path_b_approach),
            run_time=0.8,
            rate_func=smooth,
        )
        self.play(
            MoveAlongPath(person_b["group"], side_step),
            Indicate(person_a["halo"], color=ACCENT_BLUE, scale_factor=1.18),
            Indicate(person_b["halo"], color=ACCENT_AMBER, scale_factor=1.18),
            run_time=0.5,
            rate_func=smooth,
        )
        self.play(
            MoveAlongPath(person_a["group"], a_pass),
            ShowCreation(a_pass),
            run_time=0.9,
            rate_func=smooth,
        )
        self.play(
            MoveAlongPath(person_b["group"], path_b_resume),
            ShowCreation(path_b_resume),
            run_time=0.9,
            rate_func=smooth,
        )

        # 21.2-24.7: Pedestrians stop, the robot yields, and traffic starts again.
        stop_label = self.interaction_chip("stop / go", 4.0)
        stop_robot = vehicle_icon(color=ACCENT_PINK, scale=0.36)
        stop_robot.move_to(self.stage_point(living_stage, -4.8, -0.62))
        robot_approach = Line(
            stop_robot.get_center(),
            self.stage_point(living_stage, -1.15, -0.62),
            stroke_color=ACCENT_PINK,
            stroke_width=2.5,
            stroke_opacity=0.65,
        )
        robot_resume = Line(
            robot_approach.get_end(),
            self.stage_point(living_stage, 0.62, -0.62),
            stroke_color=ACCENT_PINK,
            stroke_width=2.5,
            stroke_opacity=0.65,
        )
        stop_peds = VGroup()
        ped_approaches = VGroup()
        ped_crossings = VGroup()
        for index, color in enumerate((ACCENT_GREEN, ACCENT_AMBER, ACCENT_BLUE)):
            start = self.stage_point(living_stage, 0.25 + index * 0.43, 1.85)
            curb = self.stage_point(living_stage, 0.25 + index * 0.43, 0.72)
            end = self.stage_point(living_stage, 0.25 + index * 0.43, -1.45)
            person = self.human_agent(start, color, scale=0.44, halo_radius=0.3)
            stop_peds.add(person["group"])
            ped_approaches.add(Line(start, curb))
            ped_crossings.add(Line(curb, end))
        self.play(
            FadeIn(stop_label, shift=DOWN * 0.06),
            FadeOut(VGroup(
                person_a["group"],
                person_b["group"],
                a_approach,
                a_pass,
                path_b_approach,
                side_step,
                path_b_resume,
                negotiation_trails,
            )),
            FadeIn(stop_robot),
            FadeIn(stop_peds),
            run_time=0.4,
        )
        self.play(
            MoveAlongPath(stop_robot, robot_approach),
            LaggedStart(
                *(
                    MoveAlongPath(person, path)
                    for person, path in zip(stop_peds, ped_approaches)
                ),
                lag_ratio=0.08,
            ),
            ShowCreation(robot_approach),
            run_time=0.9,
            rate_func=smooth,
        )
        stop_bars = VGroup()
        for person in stop_peds:
            bar = Line(
                LEFT * 0.15,
                RIGHT * 0.15,
                stroke_color=RED_ERROR,
                stroke_width=3.2,
            )
            bar.next_to(person, DOWN, buff=0.06)
            stop_bars.add(bar)
        yield_arc = Arc(
            radius=0.52,
            start_angle=0.1 * PI,
            angle=0.8 * PI,
            stroke_color=ACCENT_PINK,
            stroke_width=3.0,
        )
        yield_arc.next_to(stop_robot, RIGHT, buff=0.08)
        yield_text = Text(
            "yield",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=ACCENT_PINK,
            weight=BOLD,
        )
        yield_text.next_to(yield_arc, UP, buff=0.02)
        self.play(
            LaggedStart(
                *(FadeIn(bar, scale=0.7) for bar in stop_bars),
                lag_ratio=0.1,
            ),
            ShowCreation(yield_arc),
            FadeIn(yield_text),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *(
                    MoveAlongPath(person, path)
                    for person, path in zip(stop_peds, ped_crossings)
                ),
                lag_ratio=0.18,
            ),
            FadeOut(stop_bars),
            run_time=0.8,
            rate_func=smooth,
        )
        self.play(
            MoveAlongPath(stop_robot, robot_resume),
            ShowCreation(robot_resume),
            FadeOut(yield_arc),
            FadeOut(yield_text),
            run_time=0.9,
            rate_func=smooth,
        )

        # 24.7-28.0: The robot observes people and replans before it moves.
        late_peds = VGroup()
        for x, y, color in [
            (2.15, -0.42, ACCENT_GREEN),
            (2.8, 0.06, ACCENT_AMBER),
            (3.35, -0.82, ACCENT_BLUE),
        ]:
            late_peds.add(
                self.human_agent(
                    self.stage_point(living_stage, x, y),
                    color,
                    scale=0.43,
                    halo_radius=0.3,
                )["group"]
            )
        sensing = sensor_cone(
            stop_robot.get_center(),
            color=ACCENT_AMBER,
            spread=PI / 3.4,
            length=3.25,
            n_levels=7,
        )
        straight_path = Line(
            stop_robot.get_center(),
            self.stage_point(living_stage, 5.0, -0.62),
            stroke_color=RED_ERROR,
            stroke_width=3.0,
            stroke_opacity=0.72,
        )
        self.play(
            FadeOut(stop_peds),
            FadeOut(ambient_people),
            FadeOut(ambient_halos),
            FadeIn(late_peds),
            FadeIn(sensing),
            ShowCreation(straight_path),
            run_time=0.4,
        )
        self.play(
            LaggedStart(
                *(Indicate(person, color=ACCENT_AMBER, scale_factor=1.08) for person in late_peds),
                lag_ratio=0.12,
            ),
            ShowPassingFlash(
                straight_path.copy().set_stroke(RED_ERROR, width=6.0, opacity=0.8),
                time_width=0.35,
            ),
            run_time=0.7,
        )
        stop_point = self.stage_point(living_stage, 1.35, -0.62)
        safe_approach = Line(
            stop_robot.get_center(),
            stop_point,
            stroke_color=GREEN_FIX,
            stroke_width=3.0,
            stroke_opacity=0.82,
        )
        safe_resume = Line(
            stop_point,
            self.stage_point(living_stage, 5.0, -0.62),
            stroke_color=GREEN_FIX,
            stroke_width=3.0,
            stroke_opacity=0.82,
        )
        wait_bar = Line(
            UP * 0.34,
            DOWN * 0.34,
            stroke_color=GREEN_FIX,
            stroke_width=4.0,
        )
        wait_bar.move_to(stop_point + RIGHT * 0.18)
        replan = self.token("REPLAN", GREEN_FIX, width=1.2)
        replan.move_to(self.stage_point(living_stage, 1.35, -1.35))
        self.play(
            FadeOut(straight_path),
            ShowCreation(safe_approach),
            FadeIn(wait_bar, scale=0.8),
            FadeIn(replan, scale=0.8),
            Flash(stop_robot, color=GREEN_FIX, line_length=0.12, num_lines=7),
            run_time=0.5,
        )
        self.play(
            MoveAlongPath(stop_robot, safe_approach),
            run_time=0.5,
            rate_func=smooth,
        )
        clearance_paths = VGroup(
            Line(
                late_peds[0].get_center(),
                self.stage_point(living_stage, 2.15, 1.22),
            ),
            Line(
                late_peds[1].get_center(),
                self.stage_point(living_stage, 2.8, 1.45),
            ),
            Line(
                late_peds[2].get_center(),
                self.stage_point(living_stage, 3.35, -1.55),
            ),
        )
        self.play(
            LaggedStart(
                *(
                    MoveAlongPath(person, path)
                    for person, path in zip(late_peds, clearance_paths)
                ),
                lag_ratio=0.12,
            ),
            run_time=0.6,
            rate_func=smooth,
        )
        self.play(
            ShowCreation(safe_resume),
            MoveAlongPath(stop_robot, safe_resume),
            ShowPassingFlash(
                safe_resume.copy().set_stroke(GREEN_FIX, width=6.5, opacity=0.65),
                time_width=0.35,
            ),
            FadeOut(sensing),
            FadeOut(wait_bar),
            FadeOut(replan),
            run_time=0.9,
            rate_func=smooth,
        )

        # 28.0-29.2: The three behaviors resolve into a living city.
        payoff = Text(
            "LIVING CITY",
            font=FONT_PRIMARY,
            font_size=SIZE_H1,
            color=GREEN_FIX,
            weight=BOLD,
        )
        payoff.move_to(UP * 0.25)
        caption = Text(
            "social dynamics a robot must navigate",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=INK_DARK,
        )
        caption.next_to(payoff, DOWN, buff=0.22)
        behavior_labels = VGroup(
            dispersion_label,
            negotiation_label,
            stop_label,
        )
        self.play(
            behavior_labels.animate.scale(0.22).move_to(payoff).set_opacity(0),
            living_stage["base"].animate.set_opacity(0.18),
            FadeOut(late_peds),
            FadeOut(stop_robot),
            FadeOut(robot_approach),
            FadeOut(robot_resume),
            FadeOut(safe_approach),
            FadeOut(safe_resume),
            FadeIn(payoff, scale=0.82),
            FadeIn(caption, shift=UP * 0.06),
            run_time=0.7,
            rate_func=smooth,
        )
        self.play(
            Indicate(payoff, color=GREEN_FIX, scale_factor=1.04),
            run_time=0.5,
        )

        self._close()
