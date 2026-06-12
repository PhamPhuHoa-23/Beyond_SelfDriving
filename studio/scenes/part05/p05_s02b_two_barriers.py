"""P05-S02b: two blockers for scalable physical AI."""
from manimlib import *

from studio.components import (
    StudioScene,
    BG_PAPER,
    PASTEL_BLUE,
    PASTEL_PINK,
    ACCENT_BLUE,
    ACCENT_TEAL,
    ACCENT_AMBER,
    ACCENT_PINK,
    RED_ERROR,
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
    vehicle_icon,
)

SCRIPT = (
    "Two barriers remain. First, robot behavior data cannot be scraped from the web. "
    "Second, robots operate around people, but simulation often lacks human behavior."
)


class P05S02BTwoBarriers(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Two Barriers"

    def barrier_heading(self, number, title, subtitle, color, x):
        badge = Circle(
            radius=0.17,
            fill_color=color,
            fill_opacity=1,
            stroke_color=color,
            stroke_width=1,
        )
        badge_num = Text(
            str(number),
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=WHITE,
            weight=BOLD,
        )
        badge_num.move_to(badge)
        headline = Text(
            title,
            font=FONT_PRIMARY,
            font_size=28,
            color=INK_DARK,
        )
        sub = Text(
            subtitle,
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_LIGHT,
        )
        copy = VGroup(headline, sub).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        group = VGroup(VGroup(badge, badge_num), copy).arrange(RIGHT, buff=0.16)
        group.move_to(np.array([x, 1.82, 0]))
        return group

    def data_card(self, label, color):
        box = RoundedRectangle(
            width=0.74,
            height=0.46,
            corner_radius=0.05,
            fill_color=interpolate_color(color, WHITE, 0.76),
            fill_opacity=0.94,
            stroke_color=color,
            stroke_width=1.2,
        )
        line1 = Line(LEFT * 0.22, RIGHT * 0.22, stroke_color=color, stroke_width=1.5)
        line2 = Line(LEFT * 0.22, RIGHT * 0.12, stroke_color=color, stroke_width=1.5)
        marks = VGroup(line1, line2).arrange(DOWN, buff=0.07)
        marks.move_to(box)
        tag = Text(label, font=FONT_PRIMARY, font_size=15, color=INK_MID)
        tag.next_to(box, DOWN, buff=0.07)
        return VGroup(box, marks, tag)

    def mini_world(self, label, color):
        tile = RoundedRectangle(
            width=1.2,
            height=0.68,
            corner_radius=0.08,
            fill_color=interpolate_color(color, WHITE, 0.84),
            fill_opacity=0.9,
            stroke_color=color,
            stroke_width=1.1,
        )
        road = Line(
            tile.get_left() + RIGHT * 0.18 + DOWN * 0.12,
            tile.get_right() + LEFT * 0.18 + DOWN * 0.12,
            stroke_color=LINE_GRID,
            stroke_width=5.2,
            stroke_opacity=0.9,
        )
        text = Text(label, font=FONT_PRIMARY, font_size=19, color=INK_MID)
        text.next_to(tile, UP, buff=0.08)
        return VGroup(tile, road, text)

    def robot_marker(self, color=ACCENT_PINK, scale=0.45):
        robot = vehicle_icon(color=color, scale=scale)
        sensor = Dot(robot.get_center() + RIGHT * 0.13, radius=0.035, color=INK_DARK)
        return VGroup(robot, sensor)

    def person_dot(self, color=INK_MID):
        body = Dot(radius=0.07, color=color)
        intent = Triangle(
            fill_color=color,
            fill_opacity=0.9,
            stroke_width=0,
        )
        intent.scale(0.08)
        intent.next_to(body, RIGHT, buff=0.03)
        return VGroup(body, intent)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        divider = Line(
            UP * 2.18,
            DOWN * 2.36,
            stroke_color=LINE_SEP,
            stroke_width=1.4,
            stroke_opacity=0.85,
        )

        left_heading = self.barrier_heading(
            1,
            "Data bottleneck",
            "No web-scale robot behavior data",
            ACCENT_PINK,
            -3.5,
        )
        right_heading = self.barrier_heading(
            2,
            "Human modeling gap",
            "Simulation has people, but not behavior",
            RED_ERROR,
            3.55,
        )

        # Barrier 1: active collection is a trickle, not a web crawl.
        world_labels = [
            ("campus", ACCENT_TEAL),
            ("curb", ACCENT_AMBER),
            ("crosswalk", ACCENT_PINK),
        ]
        worlds = VGroup(*(self.mini_world(label, color) for label, color in world_labels))
        worlds.arrange(RIGHT, buff=0.24)
        worlds.move_to(LEFT * 3.55 + UP * 0.62)

        robot = self.robot_marker(ACCENT_PINK, 0.4)
        robot.move_to(worlds[0][1].get_center())

        slow_label = Text(
            "one robot  x  one environment  x  one task",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_MID,
        )
        slow_label.move_to(LEFT * 3.55 + DOWN * 0.04)

        cards = VGroup()
        for i, color in enumerate([ACCENT_TEAL, ACCENT_AMBER, ACCENT_PINK]):
            card = self.data_card(f"log {i + 1}", color)
            card.move_to(LEFT * (4.9 - i * 0.78) + DOWN * 0.72)
            cards.add(card)

        archive_box = RoundedRectangle(
            width=2.05,
            height=0.94,
            corner_radius=0.08,
            fill_color=PASTEL_BLUE,
            fill_opacity=0.42,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.4,
            stroke_opacity=0.7,
        )
        archive_box.move_to(LEFT * 1.82 + DOWN * 0.72)
        archive_slots = VGroup()
        for r in range(2):
            for c in range(6):
                slot = Square(
                    side_length=0.14,
                    fill_color=WHITE,
                    fill_opacity=0.2,
                    stroke_color=ACCENT_BLUE,
                    stroke_width=0.8,
                    stroke_opacity=0.35,
                )
                slot.move_to(archive_box.get_center() + LEFT * 0.74 + RIGHT * c * 0.28 + UP * (0.2 - r * 0.34))
                archive_slots.add(slot)
        archive_label = Text(
            "needs web-scale\ncoverage",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=ACCENT_BLUE,
        )
        archive_label.next_to(archive_box, DOWN, buff=0.08)
        archive = VGroup(archive_box, archive_slots, archive_label)

        b1_conclusion = Text(
            "Data arrives as a trickle.",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=ACCENT_PINK,
        )
        b1_conclusion.move_to(LEFT * 3.55 + DOWN * 1.88)

        # Barrier 2: a city without behavior produces collisions, not realism.
        city_bg = RoundedRectangle(
            width=4.55,
            height=2.3,
            corner_radius=0.12,
            fill_color="#EEF3F2",
            fill_opacity=0.9,
            stroke_color=LINE_GRID,
            stroke_width=1.2,
        )
        city_bg.move_to(RIGHT * 3.55 + UP * 0.2)

        road_h = Rectangle(
            width=4.3,
            height=0.58,
            fill_color="#DCE5E8",
            fill_opacity=0.95,
            stroke_width=0,
        )
        road_v = Rectangle(
            width=0.62,
            height=2.05,
            fill_color="#DCE5E8",
            fill_opacity=0.95,
            stroke_width=0,
        )
        roads = VGroup(road_h, road_v).move_to(city_bg)

        crosswalk = VGroup()
        for i in range(5):
            stripe = Rectangle(
                width=0.05,
                height=0.52,
                fill_color=WHITE,
                fill_opacity=0.85,
                stroke_width=0,
            )
            stripe.move_to(city_bg.get_center() + LEFT * 0.18 + RIGHT * i * 0.09)
            crosswalk.add(stripe)

        blocks = VGroup()
        for dx, dy, color in [
            (-1.35, 0.72, ACCENT_TEAL),
            (1.4, 0.72, ACCENT_AMBER),
            (-1.35, -0.72, ACCENT_BLUE),
            (1.4, -0.72, ACCENT_PINK),
        ]:
            block = RoundedRectangle(
                width=0.86,
                height=0.46,
                corner_radius=0.06,
                fill_color=interpolate_color(color, WHITE, 0.82),
                fill_opacity=0.9,
                stroke_color=color,
                stroke_width=1,
                stroke_opacity=0.55,
            )
            block.move_to(city_bg.get_center() + RIGHT * dx + UP * dy)
            blocks.add(block)

        city = VGroup(city_bg, roads, crosswalk, blocks)

        people = VGroup()
        p1 = self.person_dot(INK_MID).move_to(city_bg.get_center() + LEFT * 0.08 + UP * 0.92)
        p2 = self.person_dot(INK_LIGHT).move_to(city_bg.get_center() + RIGHT * 1.62 + DOWN * 0.05)
        p3 = self.person_dot(INK_MID).move_to(city_bg.get_center() + LEFT * 1.7 + DOWN * 0.05)
        p2.rotate(PI)
        p3.rotate(0)
        people.add(p1, p2, p3)

        sim_robot = self.robot_marker(ACCENT_PINK, 0.36)
        sim_robot.move_to(city_bg.get_center() + LEFT * 1.72 + DOWN * 0.19)

        straight_paths = VGroup(
            Line(p1.get_center(), city_bg.get_center() + LEFT * 0.08 + DOWN * 0.92, stroke_color=INK_MID, stroke_width=1.5, stroke_opacity=0.45),
            Line(p2.get_center(), city_bg.get_center() + LEFT * 1.62 + DOWN * 0.05, stroke_color=INK_LIGHT, stroke_width=1.5, stroke_opacity=0.45),
            Line(sim_robot.get_center(), city_bg.get_center() + RIGHT * 1.65 + DOWN * 0.19, stroke_color=ACCENT_PINK, stroke_width=1.8, stroke_opacity=0.55),
        )

        warning = VGroup(
            Circle(radius=0.22, stroke_color=RED_ERROR, stroke_width=2.0, stroke_opacity=0.9),
            Text("no yielding", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=RED_ERROR),
        )
        warning[0].move_to(city_bg.get_center() + LEFT * 0.06 + DOWN * 0.07)
        warning[1].next_to(warning[0], DOWN, buff=0.07)

        zombie_label = Text(
            "Zombie-city motion: straight lines, no interaction.",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=RED_ERROR,
        )
        zombie_label.move_to(RIGHT * 3.55 + DOWN * 1.42)

        b2_conclusion = Text(
            "Safety needs human behavior.",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=RED_ERROR,
        )
        b2_conclusion.move_to(RIGHT * 3.55 + DOWN * 1.88)

        bottom_rule = Line(
            LEFT * 5.7,
            RIGHT * 5.7,
            stroke_color=LINE_SEP,
            stroke_width=1.1,
        )
        bottom_rule.move_to(DOWN * 2.28)
        bottom_text = Text(
            "Physical AI needs scalable simulation and human-centric modeling.",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_DARK,
        )
        bottom_text.next_to(bottom_rule, DOWN, buff=0.18)
        bottom_text.set_color_by_text("scalable simulation", ACCENT_PINK)
        bottom_text.set_color_by_text("human-centric modeling", RED_ERROR)

        self.play(
            FadeIn(divider),
            FadeIn(left_heading, shift=DOWN * 0.1),
            FadeIn(right_heading, shift=DOWN * 0.1),
            run_time=0.8,
        )

        self.play(
            LaggedStart(*(FadeIn(w, shift=UP * 0.08) for w in worlds), lag_ratio=0.12),
            FadeIn(robot),
            FadeIn(slow_label),
            run_time=0.9,
        )
        for world, card in zip(worlds, cards):
            self.play(
                robot.animate.move_to(world[1].get_center()),
                run_time=0.45,
                rate_func=smooth,
            )
            self.play(FadeIn(card, shift=UP * 0.08), run_time=0.2)
        self.play(FadeIn(archive, shift=UP * 0.08), run_time=0.5)
        self.play(FadeIn(b1_conclusion, shift=UP * 0.08), run_time=0.45)

        self.play(FadeIn(city), run_time=0.7)
        self.play(
            LaggedStart(*(FadeIn(p) for p in people), lag_ratio=0.08),
            FadeIn(sim_robot),
            ShowCreation(straight_paths),
            run_time=0.8,
        )
        self.play(
            p1.animate.move_to(city_bg.get_center() + LEFT * 0.08 + DOWN * 0.92),
            p2.animate.move_to(city_bg.get_center() + LEFT * 1.62 + DOWN * 0.05),
            p3.animate.move_to(city_bg.get_center() + RIGHT * 1.7 + DOWN * 0.05),
            sim_robot.animate.move_to(city_bg.get_center() + RIGHT * 1.65 + DOWN * 0.19),
            run_time=1.25,
            rate_func=linear,
        )
        self.play(FadeIn(warning, scale=1.08), FadeIn(zombie_label, shift=UP * 0.08), run_time=0.55)
        self.play(FadeIn(b2_conclusion, shift=UP * 0.08), run_time=0.45)
        self.play(ShowCreation(bottom_rule), FadeIn(bottom_text, shift=UP * 0.08), run_time=0.65)
        self.wait(1.5)
        self._close()
