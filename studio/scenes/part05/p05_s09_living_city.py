"""P05-S09 Living City: a 32-second top-down physical-AI hero scene."""
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
    ACCENT_TEAL,
    ACCENT_GREEN,
    ACCENT_AMBER,
    ACCENT_PINK,
    ORANGE_INFRA,
    CYAN_RADAR,
    GOLD_KEY,
    RED_ERROR,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    INK_LIGHT,
    LINE_GRID,
    LINE_SEP,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    vehicle_icon,
    pedestrian_icon,
    rsu_icon,
    agent_trail,
    sensor_cone,
)

SCRIPT = """This is what the full stack produces: a simulated city with realistic geometry, photorealistic rendering, physically correct surfaces, and populated by pedestrians that navigate, react, and move in ways that reflect real human behavior.

A robot trained in this environment inherits all of that: spatial awareness, reactive navigation, and the ability to anticipate the kind of behavior it will encounter when deployed in the real world."""


class P05S09LivingCity(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "The Living City"
    CITY_CENTER = DOWN * 0.12

    def point(self, x, y):
        return self.CITY_CENTER + RIGHT * x + UP * y

    def badge(self, label, color, *, width=2.45):
        shell = RoundedRectangle(
            width=width,
            height=0.46,
            corner_radius=0.1,
            fill_color=interpolate_color(color, WHITE, 0.86),
            fill_opacity=0.98,
            stroke_color=color,
            stroke_width=1.45,
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

    def building(self, x, y, width, height, color):
        center = self.point(x, y)
        shadow = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            fill_color=INK_MID,
            fill_opacity=0.12,
            stroke_width=0,
        )
        shadow.move_to(center + RIGHT * 0.08 + DOWN * 0.08)

        body = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            fill_color=color,
            fill_opacity=0.9,
            stroke_color=interpolate_color(color, INK_MID, 0.3),
            stroke_width=1.1,
        )
        body.move_to(center)

        roof = RoundedRectangle(
            width=width * 0.74,
            height=height * 0.54,
            corner_radius=0.05,
            fill_color=interpolate_color(color, WHITE, 0.42),
            fill_opacity=0.76,
            stroke_color=interpolate_color(color, WHITE, 0.15),
            stroke_width=0.8,
        )
        roof.move_to(center + LEFT * 0.05 + UP * 0.03)

        windows = VGroup()
        n_windows = max(2, int(width / 0.38))
        for wx in np.linspace(-width * 0.3, width * 0.3, n_windows):
            window = RoundedRectangle(
                width=0.13,
                height=0.1,
                corner_radius=0.02,
                fill_color=ACCENT_BLUE,
                fill_opacity=0.36,
                stroke_width=0,
            )
            window.move_to(center + RIGHT * wx + DOWN * height * 0.29)
            windows.add(window)

        footprint = RoundedRectangle(
            width=width + 0.12,
            height=height + 0.12,
            corner_radius=0.09,
            fill_opacity=0,
            stroke_color=INK_LIGHT,
            stroke_width=1.1,
            stroke_opacity=0.52,
        )
        footprint.move_to(center)
        return {
            "footprint": footprint,
            "fill": VGroup(shadow, body, roof),
            "details": windows,
            "body": body,
        }

    def tree(self, x, y, scale=1.0):
        shadow = Circle(
            radius=0.16 * scale,
            fill_color=INK_MID,
            fill_opacity=0.12,
            stroke_width=0,
        )
        shadow.move_to(self.point(x, y) + RIGHT * 0.06 + DOWN * 0.06)
        crown = Circle(
            radius=0.16 * scale,
            fill_color=ACCENT_GREEN,
            fill_opacity=0.82,
            stroke_color=interpolate_color(ACCENT_GREEN, INK_MID, 0.22),
            stroke_width=0.9,
        )
        crown.move_to(self.point(x, y))
        highlight = Dot(
            self.point(x, y) + LEFT * 0.04 + UP * 0.04,
            radius=0.045 * scale,
            color=PASTEL_GREEN,
        )
        return VGroup(shadow, crown, highlight)

    def city_map(self):
        shell = RoundedRectangle(
            width=12.2,
            height=4.82,
            corner_radius=0.18,
            fill_color=interpolate_color(BG_PAPER, PASTEL_GREEN, 0.12),
            fill_opacity=1.0,
            stroke_color=ACCENT_TEAL,
            stroke_width=1.5,
        )
        shell.move_to(self.CITY_CENTER)

        h_sidewalk = Rectangle(
            width=11.72,
            height=1.82,
            fill_color=interpolate_color(BG_PAPER, LINE_GRID, 0.36),
            fill_opacity=1.0,
            stroke_color=LINE_SEP,
            stroke_width=1.0,
        )
        v_sidewalk = Rectangle(
            width=1.86,
            height=4.42,
            fill_color=interpolate_color(BG_PAPER, LINE_GRID, 0.36),
            fill_opacity=1.0,
            stroke_color=LINE_SEP,
            stroke_width=1.0,
        )
        h_road = Rectangle(
            width=11.72,
            height=1.28,
            fill_color=interpolate_color(LINE_SEP, INK_LIGHT, 0.12),
            fill_opacity=1.0,
            stroke_width=0,
        )
        v_road = Rectangle(
            width=1.3,
            height=4.42,
            fill_color=interpolate_color(LINE_SEP, INK_LIGHT, 0.12),
            fill_opacity=1.0,
            stroke_width=0,
        )
        for road in (h_sidewalk, v_sidewalk, h_road, v_road):
            road.move_to(self.CITY_CENTER)

        road_outlines = VGroup(
            Rectangle(
                width=11.72,
                height=1.82,
                fill_opacity=0,
                stroke_color=INK_LIGHT,
                stroke_width=1.1,
                stroke_opacity=0.52,
            ).move_to(self.CITY_CENTER),
            Rectangle(
                width=1.86,
                height=4.42,
                fill_opacity=0,
                stroke_color=INK_LIGHT,
                stroke_width=1.1,
                stroke_opacity=0.52,
            ).move_to(self.CITY_CENTER),
        )

        specs = [
            (-4.72, 1.56, 1.35, 0.78, PASTEL_BLUE),
            (-2.75, 1.56, 1.18, 0.78, PASTEL_GREEN),
            (2.65, 1.56, 1.18, 0.78, PASTEL_AMBER),
            (4.62, 1.56, 1.4, 0.78, PASTEL_PINK),
            (-4.55, -1.58, 1.48, 0.74, PASTEL_AMBER),
            (-2.55, -1.58, 1.1, 0.74, PASTEL_PINK),
            (2.55, -1.58, 1.14, 0.74, PASTEL_BLUE),
            (4.52, -1.58, 1.42, 0.74, PASTEL_GREEN),
        ]
        footprints = VGroup()
        building_fills = VGroup()
        building_details = VGroup()
        building_bodies = VGroup()
        for spec in specs:
            parts = self.building(*spec)
            footprints.add(parts["footprint"])
            building_fills.add(parts["fill"])
            building_details.add(parts["details"])
            building_bodies.add(parts["body"])

        plaza = RoundedRectangle(
            width=1.15,
            height=0.5,
            corner_radius=0.08,
            fill_color=PASTEL_AMBER,
            fill_opacity=0.78,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.0,
        )
        plaza.move_to(self.point(-1.48, 1.56))

        trees = VGroup(
            self.tree(-5.55, 1.55, 0.95),
            self.tree(-3.65, 1.55, 0.82),
            self.tree(1.55, 1.57, 0.9),
            self.tree(3.55, 1.55, 0.78),
            self.tree(-5.45, -1.57, 0.82),
            self.tree(-3.52, -1.57, 0.95),
            self.tree(1.45, -1.58, 0.82),
            self.tree(3.5, -1.57, 0.9),
        )

        lane_marks = VGroup(
            DashedLine(
                self.point(-5.68, 0),
                self.point(5.68, 0),
                dash_length=0.18,
                stroke_color=WHITE,
                stroke_width=1.2,
                stroke_opacity=0.82,
            ),
            DashedLine(
                self.point(0, -2.12),
                self.point(0, 2.12),
                dash_length=0.18,
                stroke_color=WHITE,
                stroke_width=1.2,
                stroke_opacity=0.82,
            ),
        )

        direction_marks = VGroup()
        for x in (-4.25, -2.75, 2.75, 4.25):
            direction_marks.add(
                Arrow(
                    self.point(x - 0.22, -0.34),
                    self.point(x + 0.22, -0.34),
                    fill_color=INK_MID,
                    thickness=1.0,
                    max_tip_length_to_length_ratio=0.4,
                    buff=0,
                )
            )
            direction_marks.add(
                Arrow(
                    self.point(x + 0.22, 0.34),
                    self.point(x - 0.22, 0.34),
                    fill_color=INK_MID,
                    thickness=1.0,
                    max_tip_length_to_length_ratio=0.4,
                    buff=0,
                )
            )
        for y in (-1.55, 1.55):
            direction_marks.add(
                Arrow(
                    self.point(0.34, y - 0.2),
                    self.point(0.34, y + 0.2),
                    fill_color=INK_MID,
                    thickness=1.0,
                    max_tip_length_to_length_ratio=0.4,
                    buff=0,
                )
            )
            direction_marks.add(
                Arrow(
                    self.point(-0.34, y + 0.2),
                    self.point(-0.34, y - 0.2),
                    fill_color=INK_MID,
                    thickness=1.0,
                    max_tip_length_to_length_ratio=0.4,
                    buff=0,
                )
            )

        crosswalks = VGroup()
        for y in np.linspace(-0.48, 0.48, 7):
            crosswalks.add(
                Rectangle(
                    width=0.48,
                    height=0.07,
                    fill_color=WHITE,
                    fill_opacity=0.88,
                    stroke_width=0,
                ).move_to(self.point(-0.92, y))
            )
        for y in np.linspace(-0.48, 0.48, 7):
            crosswalks.add(
                Rectangle(
                    width=0.48,
                    height=0.07,
                    fill_color=WHITE,
                    fill_opacity=0.88,
                    stroke_width=0,
                ).move_to(self.point(0.92, y))
            )
        for x in np.linspace(-0.48, 0.48, 7):
            crosswalks.add(
                Rectangle(
                    width=0.07,
                    height=0.46,
                    fill_color=WHITE,
                    fill_opacity=0.88,
                    stroke_width=0,
                ).move_to(self.point(x, 0.94))
            )
        for x in np.linspace(-0.48, 0.48, 7):
            crosswalks.add(
                Rectangle(
                    width=0.07,
                    height=0.46,
                    fill_color=WHITE,
                    fill_opacity=0.88,
                    stroke_width=0,
                ).move_to(self.point(x, -0.94))
            )

        road_overlay = VGroup(
            Rectangle(
                width=11.72,
                height=1.28,
                fill_color=ACCENT_BLUE,
                fill_opacity=0.08,
                stroke_width=0,
            ).move_to(self.CITY_CENTER),
            Rectangle(
                width=1.3,
                height=4.42,
                fill_color=ACCENT_BLUE,
                fill_opacity=0.08,
                stroke_width=0,
            ).move_to(self.CITY_CENTER),
        )
        walk_overlay = VGroup(
            Rectangle(
                width=11.72,
                height=1.82,
                fill_color=ACCENT_GREEN,
                fill_opacity=0.06,
                stroke_color=ACCENT_GREEN,
                stroke_width=1.0,
                stroke_opacity=0.35,
            ).move_to(self.CITY_CENTER),
            Rectangle(
                width=1.86,
                height=4.42,
                fill_color=ACCENT_GREEN,
                fill_opacity=0.06,
                stroke_color=ACCENT_GREEN,
                stroke_width=1.0,
                stroke_opacity=0.35,
            ).move_to(self.CITY_CENTER),
        )
        collision_overlay = VGroup(
            *(
                footprint.copy().set_stroke(ACCENT_AMBER, width=2.0, opacity=0.72)
                for footprint in footprints
            )
        )

        geometry = VGroup(road_outlines, footprints)
        rendering = VGroup(
            h_sidewalk,
            v_sidewalk,
            h_road,
            v_road,
            building_fills,
            plaza,
        )
        details = VGroup(building_details, trees)
        physics = VGroup(lane_marks, crosswalks, direction_marks)
        overlays = VGroup(road_overlay, walk_overlay, collision_overlay)
        return {
            "shell": shell,
            "geometry": geometry,
            "rendering": rendering,
            "details": details,
            "physics": physics,
            "overlays": overlays,
            "buildings": building_bodies,
        }

    def car(self, position, color, angle=0, scale=0.29):
        car = vehicle_icon(color=color, scale=scale)
        car.rotate(angle)
        car.move_to(position)
        return car

    def pedestrian(self, position, color, scale=0.42):
        person = pedestrian_icon(color=color).scale(scale)
        person.move_to(position)
        return person

    def dynamic_link(self, source, target):
        link = DashedLine(
            source.get_center(),
            target.get_center(),
            dash_length=0.09,
            stroke_color=CYAN_RADAR,
            stroke_width=1.25,
            stroke_opacity=0.5,
        )

        def update_link(mob):
            mob.become(
                DashedLine(
                    source.get_center(),
                    target.get_center(),
                    dash_length=0.09,
                    stroke_color=CYAN_RADAR,
                    stroke_width=1.25,
                    stroke_opacity=0.5,
                )
            )

        link.add_updater(update_link)
        return link

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)  # 0.0-1.0

        city = self.city_map()
        layer_badges = VGroup(
            self.badge("GEOMETRY", ACCENT_BLUE, width=2.15),
            self.badge("RENDERING", ACCENT_PINK, width=2.15),
            self.badge("PHYSICS", ACCENT_AMBER, width=2.15),
            self.badge("HUMAN BEHAVIOR", ACCENT_GREEN, width=2.65),
        ).arrange(RIGHT, buff=0.22)
        layer_badges.move_to(DOWN * 3.36)

        # 1.0-3.8: Assemble the urban world from geometry.
        self.play(FadeIn(city["shell"], scale=0.985), run_time=0.9)
        self.play(
            LaggedStart(
                *(ShowCreation(outline) for outline in city["geometry"][0]),
                lag_ratio=0.18,
            ),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *(ShowCreation(footprint) for footprint in city["geometry"][1]),
                lag_ratio=0.08,
            ),
            run_time=1.1,
        )

        # 3.8-5.0: Emphasize realistic geometry.
        self.play(
            FadeIn(layer_badges[0], shift=UP * 0.08),
            LaggedStart(
                *(Indicate(item, color=ACCENT_BLUE, scale_factor=1.02)
                  for item in city["geometry"]),
                lag_ratio=0.12,
            ),
            run_time=1.2,
        )

        # 5.0-6.2: A render sweep fills the wireframe with a vibrant city.
        render_sweep = Rectangle(
            width=0.26,
            height=4.55,
            fill_color=ACCENT_PINK,
            fill_opacity=0.18,
            stroke_color=ACCENT_PINK,
            stroke_width=2.0,
            stroke_opacity=0.7,
        )
        render_sweep.move_to(self.point(-5.72, 0))
        self.add(render_sweep)
        self.play(
            FadeIn(city["rendering"]),
            FadeIn(city["details"]),
            FadeIn(layer_badges[1], shift=UP * 0.08),
            render_sweep.animate.shift(RIGHT * 11.44),
            run_time=1.2,
            rate_func=smooth,
        )
        self.remove(render_sweep)

        # 6.2-8.6: Mark drivable, walkable, and collidable surfaces.
        self.play(
            FadeIn(city["physics"]),
            FadeIn(city["overlays"]),
            FadeIn(layer_badges[2], shift=UP * 0.08),
            run_time=1.2,
        )
        self.play(
            Succession(
                LaggedStart(
                    Indicate(
                        city["overlays"][0],
                        color=ACCENT_BLUE,
                        scale_factor=1.01,
                    ),
                    Indicate(
                        city["overlays"][1],
                        color=ACCENT_GREEN,
                        scale_factor=1.01,
                    ),
                    Indicate(
                        city["overlays"][2],
                        color=ACCENT_AMBER,
                        scale_factor=1.01,
                    ),
                    lag_ratio=0.18,
                    run_time=0.8,
                ),
                FadeOut(city["overlays"], run_time=0.4),
            ),
            run_time=1.2,
        )

        # Agent layout and route definitions.
        robot = self.car(self.point(-4.92, -0.34), ACCENT_PINK, scale=0.32)
        car_top = self.car(self.point(4.95, 0.34), ACCENT_TEAL, PI)
        car_bottom = self.car(self.point(-4.55, -0.34), ACCENT_BLUE)
        car_vertical = self.car(self.point(0.34, -2.02), ACCENT_AMBER, PI / 2)
        cars = VGroup(car_top, car_bottom, car_vertical)

        ped_a = self.pedestrian(self.point(-1.08, 1.5), GOLD_KEY)
        ped_b = self.pedestrian(self.point(-0.76, -1.48), ACCENT_GREEN)
        ambient_ped = self.pedestrian(self.point(3.45, 1.0), ACCENT_BLUE, scale=0.37)
        pedestrians = VGroup(ped_a, ped_b, ambient_ped)

        rsus = VGroup()
        for position in (self.point(-1.65, 1.45), self.point(1.65, -1.45)):
            rsu = rsu_icon(color=ORANGE_INFRA).scale(0.68)
            rsu.move_to(position)
            rsus.add(rsu)

        robot_intro = Line(robot.get_center(), self.point(-2.15, -0.34))
        top_route = Line(car_top.get_center(), self.point(-4.85, 0.34))
        bottom_route = Line(car_bottom.get_center(), self.point(5.15, -0.34))
        vertical_route = Line(car_vertical.get_center(), self.point(0.34, 1.98))
        ped_a_approach = Line(ped_a.get_center(), self.point(-1.08, 0.73))
        ped_b_approach = Line(ped_b.get_center(), self.point(-0.76, -0.73))
        ambient_route = Line(ambient_ped.get_center(), self.point(4.5, 1.0))

        moving_agents = VGroup(robot, cars, pedestrians)
        trails = VGroup(
            agent_trail(robot, color=ACCENT_PINK),
            agent_trail(car_top, color=ACCENT_TEAL),
            agent_trail(car_bottom, color=ACCENT_BLUE),
            agent_trail(car_vertical, color=ACCENT_AMBER),
            agent_trail(ped_a, color=GOLD_KEY),
            agent_trail(ped_b, color=ACCENT_GREEN),
        )

        # 8.6-11.5: Populate the city and establish lawful navigation.
        self.play(
            LaggedStart(
                *(FadeIn(agent, scale=0.72) for agent in moving_agents),
                lag_ratio=0.07,
            ),
            LaggedStart(*(GrowFromCenter(rsu) for rsu in rsus), lag_ratio=0.18),
            FadeIn(layer_badges[3], shift=UP * 0.08),
            run_time=0.8,
        )
        self.add(trails)
        self.play(
            MoveAlongPath(robot, robot_intro),
            MoveAlongPath(car_top, top_route),
            MoveAlongPath(car_bottom, bottom_route),
            MoveAlongPath(car_vertical, vertical_route),
            MoveAlongPath(ped_a, ped_a_approach),
            MoveAlongPath(ped_b, ped_b_approach),
            MoveAlongPath(ambient_ped, ambient_route),
            run_time=2.1,
            rate_func=smooth,
        )

        # 11.5-14.0: The robot detects a crossing interaction and yields.
        sensing = sensor_cone(
            robot.get_center(),
            color=ACCENT_AMBER,
            spread=PI / 3.6,
            length=2.25,
            n_levels=7,
        )
        sensing.set_opacity(0.55)
        reaction_halo = Circle(
            radius=0.72,
            fill_color=ACCENT_PINK,
            fill_opacity=0.04,
            stroke_color=ACCENT_PINK,
            stroke_width=1.8,
            stroke_opacity=0.55,
        )
        reaction_halo.move_to(robot)
        self.play(
            FadeIn(sensing),
            FadeIn(reaction_halo, scale=0.65),
            Flash(robot, color=ACCENT_PINK, line_length=0.13, num_lines=8),
            run_time=0.5,
        )

        robot_stop = Line(robot.get_center(), self.point(-1.72, -0.34))
        ped_a_enter = CubicBezier(
            ped_a.get_center(),
            self.point(-1.08, 0.5),
            self.point(-1.04, 0.3),
            self.point(-1.02, 0.12),
        )
        ped_b_enter = CubicBezier(
            ped_b.get_center(),
            self.point(-0.76, -0.5),
            self.point(-0.78, -0.3),
            self.point(-0.8, -0.12),
        )
        self.play(
            MoveAlongPath(robot, robot_stop),
            MoveAlongPath(ped_a, ped_a_enter),
            MoveAlongPath(ped_b, ped_b_enter),
            reaction_halo.animate.move_to(robot_stop.get_end()),
            sensing.animate.shift(robot_stop.get_end() - robot_stop.get_start()),
            run_time=1.2,
            rate_func=smooth,
        )

        yield_bar = Line(
            UP * 0.42,
            DOWN * 0.42,
            stroke_color=ACCENT_PINK,
            stroke_width=4.0,
        )
        yield_bar.move_to(self.point(-1.32, -0.34))
        yield_text = Text(
            "YIELD",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=ACCENT_PINK,
            weight=BOLD,
        )
        yield_text.next_to(robot, DOWN, buff=0.14)
        yield_text.shift(LEFT * 0.08)
        self.play(
            FadeIn(yield_bar, scale=0.75),
            FadeIn(yield_text, shift=UP * 0.05),
            Indicate(ped_a, color=GOLD_KEY, scale_factor=1.12),
            Indicate(ped_b, color=ACCENT_GREEN, scale_factor=1.12),
            run_time=0.8,
        )

        # 14.0-16.0: People negotiate the crossing; the robot waits, then resumes.
        ped_a_cross = CubicBezier(
            ped_a.get_center(),
            self.point(-1.18, -0.08),
            self.point(-1.2, -0.58),
            self.point(-1.18, -1.12),
        )
        ped_b_cross = CubicBezier(
            ped_b.get_center(),
            self.point(-0.6, 0.02),
            self.point(-0.57, 0.56),
            self.point(-0.62, 1.12),
        )
        self.play(
            MoveAlongPath(ped_a, ped_a_cross),
            MoveAlongPath(ped_b, ped_b_cross),
            FadeOut(yield_text),
            run_time=1.4,
            rate_func=smooth,
        )
        robot_resume = Line(robot.get_center(), self.point(0.45, -0.34))
        self.play(
            MoveAlongPath(robot, robot_resume),
            FadeOut(yield_bar),
            FadeOut(sensing),
            FadeOut(reaction_halo),
            run_time=0.6,
            rate_func=smooth,
        )

        # 16.0-18.2: Compress the four environment layers into the robot.
        for trail in trails:
            trail.clear_updaters()
        self.play(
            LaggedStart(
                *(
                    badge.animate.scale(0.18).move_to(robot).set_opacity(0)
                    for badge in layer_badges
                ),
                lag_ratio=0.08,
            ),
            FadeOut(trails),
            run_time=1.2,
            rate_func=smooth,
        )
        full_stack = self.badge("FULL STACK", ACCENT_PINK, width=1.75)
        full_stack.next_to(robot, UP, buff=0.12)
        self.play(
            FadeIn(full_stack, scale=0.72),
            Flash(robot, color=ACCENT_PINK, line_length=0.22, num_lines=12),
            Indicate(city["rendering"], color=ACCENT_PINK, scale_factor=1.005),
            run_time=1.0,
        )

        capability_badges = VGroup(
            self.badge("SPATIAL AWARENESS", ACCENT_TEAL, width=3.25),
            self.badge("REACTIVE NAVIGATION", ACCENT_GREEN, width=3.35),
            self.badge("ANTICIPATION", ACCENT_AMBER, width=2.75),
        ).arrange(RIGHT, buff=0.28)
        capability_badges.move_to(DOWN * 3.36)

        coverage = VGroup()
        for center in (rsus[0], rsus[1], robot):
            disc = Circle(
                radius=1.14 if center is not robot else 0.82,
                fill_color=CYAN_RADAR,
                fill_opacity=0.025,
                stroke_color=CYAN_RADAR,
                stroke_width=1.15,
                stroke_opacity=0.34,
            )
            disc.move_to(center)
            coverage.add(disc)
        coverage[2].add_updater(lambda mob: mob.move_to(robot))

        links = VGroup(
            self.dynamic_link(rsus[0], robot),
            self.dynamic_link(rsus[0], ped_a),
            self.dynamic_link(rsus[1], robot),
            self.dynamic_link(rsus[1], car_top),
            self.dynamic_link(robot, ped_b),
        )

        # 18.2-22.0: Spatial awareness emerges from local sensing and V2X.
        self.play(
            FadeIn(capability_badges[0], shift=UP * 0.08),
            FadeIn(coverage),
            LaggedStart(*(ShowCreation(link) for link in links), lag_ratio=0.1),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *(
                    ShowPassingFlash(
                        link.copy().clear_updaters().set_stroke(
                            CYAN_RADAR, width=4.2, opacity=0.9
                        ),
                        time_width=0.35,
                    )
                    for link in links
                ),
                lag_ratio=0.12,
            ),
            coverage.animate.set_stroke(opacity=0.58),
            run_time=1.6,
        )
        awareness_packet = Dot(radius=0.08, color=ACCENT_TEAL)
        awareness_path = CubicBezier(
            capability_badges[0].get_top(),
            self.point(-3.6, -2.55),
            self.point(-0.4, -1.2),
            robot.get_center(),
        )
        awareness_packet.move_to(awareness_path.get_start())
        self.add(awareness_packet)
        self.play(
            MoveAlongPath(awareness_packet, awareness_path),
            Flash(
                capability_badges[0],
                color=ACCENT_TEAL,
                line_length=0.13,
                num_lines=9,
            ),
            run_time=1.4,
            rate_func=smooth,
        )
        self.remove(awareness_packet)

        # 22.0-25.8: Detect an unsafe route, replan, and navigate around people.
        blocker_a = self.pedestrian(self.point(2.55, -0.18), GOLD_KEY, scale=0.4)
        blocker_b = self.pedestrian(self.point(2.82, -0.48), ACCENT_GREEN, scale=0.4)
        blockers = VGroup(blocker_a, blocker_b)
        bad_route = Line(
            robot.get_center(),
            self.point(3.45, -0.34),
            stroke_color=RED_ERROR,
            stroke_width=3.0,
            stroke_opacity=0.78,
        )
        self.play(
            FadeIn(capability_badges[1], shift=UP * 0.08),
            FadeIn(blockers, scale=0.76),
            ShowCreation(bad_route),
            FadeOut(full_stack),
            run_time=0.8,
        )
        safe_route = CubicBezier(
            robot.get_center(),
            self.point(1.2, -0.52),
            self.point(1.65, 0.42),
            self.point(2.22, 0.32),
            stroke_color=GREEN_FIX,
            stroke_width=3.1,
            stroke_opacity=0.86,
        )
        self.play(
            ShowPassingFlash(
                bad_route.copy().set_stroke(RED_ERROR, width=6.0, opacity=0.75),
                time_width=0.35,
            ),
            LaggedStart(
                Indicate(blocker_a, color=RED_ERROR, scale_factor=1.12),
                Indicate(blocker_b, color=RED_ERROR, scale_factor=1.12),
                lag_ratio=0.18,
            ),
            run_time=0.8,
        )
        self.play(
            FadeOut(bad_route),
            ShowCreation(safe_route),
            MoveAlongPath(robot, safe_route),
            run_time=1.6,
            rate_func=smooth,
        )
        self.play(
            Flash(
                capability_badges[1],
                color=ACCENT_GREEN,
                line_length=0.13,
                num_lines=9,
            ),
            ShowPassingFlash(
                safe_route.copy().set_stroke(GREEN_FIX, width=6.0, opacity=0.68),
                time_width=0.35,
            ),
            run_time=0.6,
        )

        # 25.8-29.2: Forecast a pedestrian trajectory before it becomes occupied.
        future_ped = self.pedestrian(self.point(3.42, 1.28), ACCENT_AMBER, scale=0.4)
        actual_ped = future_ped.copy()
        actual_ped.set_opacity(0.18)
        ghost_path = CubicBezier(
            future_ped.get_center(),
            self.point(3.38, 0.72),
            self.point(3.32, 0.02),
            self.point(3.28, -1.04),
            stroke_color=ACCENT_AMBER,
            stroke_width=2.2,
            stroke_opacity=0.62,
        )
        ghost_path.set_stroke(opacity=0.62)
        self.play(
            FadeIn(capability_badges[2], shift=UP * 0.08),
            FadeIn(actual_ped),
            ShowCreation(ghost_path),
            run_time=0.8,
        )
        early_stop = Line(robot.get_center(), self.point(2.72, 0.18))
        self.play(
            MoveAlongPath(robot, early_stop),
            ShowPassingFlash(
                ghost_path.copy().set_stroke(ACCENT_AMBER, width=5.0, opacity=0.76),
                time_width=0.4,
            ),
            run_time=0.8,
            rate_func=smooth,
        )
        self.play(
            actual_ped.animate.set_opacity(1.0),
            MoveAlongPath(actual_ped, ghost_path),
            Flash(
                capability_badges[2],
                color=ACCENT_AMBER,
                line_length=0.13,
                num_lines=9,
            ),
            run_time=1.0,
            rate_func=smooth,
        )
        final_route = CubicBezier(
            robot.get_center(),
            self.point(3.1, 0.08),
            self.point(3.58, -0.2),
            self.point(4.12, -0.34),
        )
        self.play(
            MoveAlongPath(robot, final_route),
            FadeOut(ghost_path),
            run_time=0.8,
            rate_func=smooth,
        )

        # 29.2-31.2: The learned capabilities converge into real-world readiness.
        capability_destinations = (
            robot.get_center() + LEFT * 0.45 + UP * 0.48,
            robot.get_center() + UP * 0.66,
            robot.get_center() + RIGHT * 0.45 + UP * 0.48,
        )
        capability_nodes = VGroup(
            Dot(radius=0.09, color=ACCENT_TEAL),
            Dot(radius=0.09, color=ACCENT_GREEN),
            Dot(radius=0.09, color=ACCENT_AMBER),
        )
        for node, destination in zip(capability_nodes, capability_destinations):
            node.move_to(destination)
        self.play(
            *(
                badge.animate.scale(0.16).move_to(destination).set_opacity(0)
                for badge, destination in zip(
                    capability_badges, capability_destinations
                )
            ),
            FadeIn(capability_nodes, scale=0.45),
            coverage.animate.set_stroke(opacity=0.72),
            Flash(robot, color=ACCENT_PINK, line_length=0.28, num_lines=14),
            run_time=1.0,
            rate_func=smooth,
        )
        payoff = Text(
            "TRAIN IN THE CITY. READY FOR THE WORLD.",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=ACCENT_PINK,
            weight=BOLD,
        )
        payoff.move_to(DOWN * 3.36)
        self.play(
            FadeIn(payoff, shift=UP * 0.08),
            LaggedStart(
                *(
                    ShowPassingFlash(
                        link.copy().clear_updaters().set_stroke(
                            CYAN_RADAR, width=4.0, opacity=0.86
                        ),
                        time_width=0.35,
                    )
                    for link in links
                ),
                lag_ratio=0.08,
            ),
            LaggedStart(
                *(
                    Flash(
                        node,
                        color=color,
                        line_length=0.11,
                        num_lines=7,
                    )
                    for node, color in zip(
                        capability_nodes,
                        (ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER),
                    )
                ),
                lag_ratio=0.14,
            ),
            run_time=1.0,
        )

        for link in links:
            link.clear_updaters()
        coverage[2].clear_updaters()
        self._close()  # 31.2-32.0
