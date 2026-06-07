"""P05-S02a: web-scale language data versus physical robot experience."""
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
    SIZE_BODY,
    SIZE_LABEL,
    SIZE_CAPS,
    vehicle_icon,
)

SCRIPT = (
    "LLMs work because web-scale data already exists. Robot behavior does not. "
    "Every experience must be collected by a robot, in the real world, "
    "one environment and one task at a time."
)


class P05S02ALLMVsRobot(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Web Data vs. Robot Experience"

    def source_chip(self, label, color):
        icon = Circle(
            radius=0.11,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        )
        text = Text(
            label,
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_DARK,
            weight=BOLD,
        )
        content = VGroup(icon, text).arrange(RIGHT, buff=0.14)
        box = RoundedRectangle(
            width=1.62,
            height=0.48,
            corner_radius=0.08,
            fill_color=interpolate_color(color, WHITE, 0.82),
            fill_opacity=0.88,
            stroke_color=color,
            stroke_width=1.4,
        )
        content.move_to(box)
        return VGroup(box, content)

    def llm_core(self):
        shell = RoundedRectangle(
            width=1.72,
            height=1.62,
            corner_radius=0.16,
            fill_color=PASTEL_BLUE,
            fill_opacity=0.72,
            stroke_color=ACCENT_BLUE,
            stroke_width=2.2,
        )
        nodes = VGroup()
        positions = [
            LEFT * 0.42 + UP * 0.34,
            UP * 0.42,
            RIGHT * 0.42 + UP * 0.3,
            LEFT * 0.42 + DOWN * 0.2,
            DOWN * 0.26,
            RIGHT * 0.42 + DOWN * 0.18,
        ]
        for point in positions:
            nodes.add(
                Dot(
                    shell.get_center() + point,
                    radius=0.055,
                    color=ACCENT_BLUE,
                )
            )
        links = VGroup()
        for a, b in [(0, 1), (1, 2), (0, 4), (1, 3), (1, 5), (2, 4), (3, 4), (4, 5)]:
            links.add(
                Line(
                    nodes[a].get_center(),
                    nodes[b].get_center(),
                    stroke_color=ACCENT_TEAL,
                    stroke_width=1.25,
                    stroke_opacity=0.7,
                )
            )
        label = Text(
            "LLM",
            font=FONT_PRIMARY,
            font_size=SIZE_BODY,
            color=INK_DARK,
            weight=BOLD,
        )
        label.next_to(shell, DOWN, buff=0.14)
        return VGroup(shell, links, nodes, label)

    def delivery_robot(self):
        robot = vehicle_icon(color=ACCENT_PINK, scale=0.68)
        sensor = Circle(
            radius=0.08,
            fill_color=INK_DARK,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1,
        )
        sensor.move_to(robot.get_center() + RIGHT * 0.18)
        return VGroup(robot, sensor)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        divider = Line(
            UP * 2.28,
            DOWN * 2.45,
            stroke_color=LINE_SEP,
            stroke_width=1.5,
            stroke_opacity=0.9,
        )

        web_kicker = Text(
            "LANGUAGE AI",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=ACCENT_BLUE,
            weight=BOLD,
        )
        web_kicker.set_color(ACCENT_BLUE)
        web_title = Text(
            "Data already exists",
            font=FONT_PRIMARY,
            font_size=SIZE_H1,
            color=INK_DARK,
            weight=BOLD,
        )
        web_heading = VGroup(web_kicker, web_title).arrange(DOWN, buff=0.06)
        web_heading.move_to(LEFT * 3.48 + UP * 2.02)

        robot_kicker = Text(
            "PHYSICAL AI",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=ACCENT_PINK,
            weight=BOLD,
        )
        robot_kicker.set_color(ACCENT_PINK)
        robot_title = Text(
            "Experience must be created",
            font=FONT_PRIMARY,
            font_size=SIZE_H1,
            color=INK_DARK,
            weight=BOLD,
        )
        robot_heading = VGroup(robot_kicker, robot_title).arrange(DOWN, buff=0.06)
        robot_heading.move_to(RIGHT * 3.5 + UP * 2.02)

        source_specs = [
            ("Books", ACCENT_AMBER),
            ("Wikipedia", ACCENT_BLUE),
            ("GitHub", ACCENT_TEAL),
            ("Forums", ACCENT_PINK),
            ("Video", ACCENT_AMBER),
        ]
        sources = VGroup(*(self.source_chip(*spec) for spec in source_specs))
        sources.arrange(DOWN, buff=0.13)
        sources.move_to(LEFT * 5.35 + UP * 0.25)

        llm = self.llm_core()
        llm.move_to(LEFT * 1.55 + UP * 0.2)

        streams = VGroup()
        for i, source in enumerate(sources):
            stream = Line(
                source.get_right() + RIGHT * 0.06,
                llm[0].get_left() + LEFT * 0.08 + UP * (0.48 - i * 0.24),
                stroke_color=source_specs[i][1],
                stroke_width=3.0,
                stroke_opacity=0.55,
            )
            streams.add(stream)

        web_stat = Text(
            "TRILLIONS OF TOKENS",
            font=FONT_PRIMARY,
            font_size=SIZE_BODY,
            color=ACCENT_BLUE,
            weight=BOLD,
        )
        web_stat.set_color(ACCENT_BLUE)
        web_note = Text(
            "already online  |  continuously harvested",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_MID,
        )
        web_caption = VGroup(web_stat, web_note).arrange(DOWN, buff=0.08)
        web_caption.move_to(LEFT * 3.45 + DOWN * 1.62)

        road = RoundedRectangle(
            width=4.85,
            height=1.32,
            corner_radius=0.12,
            fill_color="#E7ECF2",
            fill_opacity=0.92,
            stroke_color=LINE_GRID,
            stroke_width=1.4,
        )
        road.move_to(RIGHT * 3.48 + UP * 0.38)
        lane_marks = VGroup()
        for x in np.linspace(1.45, 5.55, 7):
            mark = Line(
                LEFT * 0.18,
                RIGHT * 0.18,
                stroke_color=WHITE,
                stroke_width=2.2,
                stroke_opacity=0.95,
            )
            mark.move_to(np.array([x, 0.38, 0]))
            lane_marks.add(mark)

        start_label = Text(
            "real world",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_LIGHT,
        )
        start_label.next_to(road, UP, buff=0.12).align_to(road, LEFT).shift(RIGHT * 0.15)

        robot = self.delivery_robot()
        robot.move_to(RIGHT * 1.45 + UP * 0.38)

        log_stack = VGroup()
        for i, opacity in enumerate([0.45, 0.68, 0.95]):
            tile_box = RoundedRectangle(
                width=0.32,
                height=0.42,
                corner_radius=0.04,
                fill_color=ACCENT_PINK,
                fill_opacity=opacity,
                stroke_color=ACCENT_PINK,
                stroke_width=1,
            )
            tile_lines = VGroup(
                Line(LEFT * 0.08, RIGHT * 0.08, stroke_color=WHITE, stroke_width=1.1),
                Line(LEFT * 0.08, RIGHT * 0.04, stroke_color=WHITE, stroke_width=1.1),
            ).arrange(DOWN, buff=0.08)
            tile_lines.move_to(tile_box)
            tile = VGroup(tile_box, tile_lines)
            tile.move_to(RIGHT * (5.28 + i * 0.18) + UP * (0.3 + i * 0.08))
            log_stack.add(tile)
        log_label = Text(
            "3 experience logs",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_MID,
        )
        log_label.next_to(log_stack, DOWN, buff=0.14)

        factor_labels = VGroup()
        for label, color in [
            ("1 ROBOT", ACCENT_PINK),
            ("1 WORLD", ACCENT_TEAL),
            ("1 TASK", ACCENT_AMBER),
        ]:
            text = Text(
                label,
                font=FONT_PRIMARY,
                font_size=SIZE_CAPS,
                color=color,
                weight=BOLD,
            )
            text.set_color(color)
            factor_labels.add(text)
        times = VGroup(*(
            Text(
                "x",
                font=FONT_PRIMARY,
                font_size=SIZE_LABEL,
                color=INK_LIGHT,
                weight=BOLD,
            )
            for _ in range(2)
        ))
        factors = VGroup(
            factor_labels[0],
            times[0],
            factor_labels[1],
            times[1],
            factor_labels[2],
        ).arrange(RIGHT, buff=0.2)
        factors.move_to(RIGHT * 3.48 + DOWN * 0.77)

        robot_stat = Text(
            "~10 HOURS / ROBOT",
            font=FONT_PRIMARY,
            font_size=SIZE_BODY,
            color=RED_ERROR,
            weight=BOLD,
        )
        robot_stat.set_color(RED_ERROR)
        robot_note = Text(
            "collected physically, one run at a time",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_MID,
        )
        robot_caption = VGroup(robot_stat, robot_note).arrange(DOWN, buff=0.08)
        robot_caption.move_to(RIGHT * 3.48 + DOWN * 1.62)

        insight_rule = Line(
            LEFT * 5.7,
            RIGHT * 5.7,
            stroke_color=LINE_SEP,
            stroke_width=1.2,
        )
        insight_rule.move_to(DOWN * 2.25)
        insight_left = Text(
            "The web stores text.",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=INK_DARK,
            weight=BOLD,
        )
        insight_right = Text(
            "Robot behavior must be made.",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=ACCENT_PINK,
            weight=BOLD,
        )
        insight_right.set_color(ACCENT_PINK)
        insight = VGroup(insight_left, insight_right).arrange(RIGHT, buff=0.22)
        insight.next_to(insight_rule, DOWN, buff=0.2)

        self.play(
            FadeIn(divider),
            FadeIn(web_heading, shift=DOWN * 0.12),
            FadeIn(robot_heading, shift=DOWN * 0.12),
        )

        self.play(
            LaggedStart(
                *(FadeIn(source, shift=RIGHT * 0.18) for source in sources),
                lag_ratio=0.1,
            ),
            FadeIn(llm),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*(ShowCreation(stream) for stream in streams), lag_ratio=0.08),
            run_time=0.7,
        )

        token_packets = VGroup()
        token_anims = []
        for i in range(15):
            source_index = i % len(sources)
            packet = RoundedRectangle(
                width=0.13,
                height=0.09,
                corner_radius=0.02,
                fill_color=source_specs[source_index][1],
                fill_opacity=1,
                stroke_width=0,
            )
            packet.move_to(streams[source_index].get_start())
            token_packets.add(packet)
            token_anims.append(
                MoveAlongPath(packet, streams[source_index].copy(), rate_func=linear)
            )
        self.add(token_packets)
        self.play(
            LaggedStart(*token_anims, lag_ratio=0.055),
            run_time=1.65,
        )
        self.play(
            FadeOut(token_packets, scale=0.5),
            FadeIn(web_caption, shift=UP * 0.12),
            run_time=0.5,
        )

        self.play(
            FadeIn(road),
            FadeIn(lane_marks),
            FadeIn(start_label),
            FadeIn(robot),
            FadeIn(factors, shift=UP * 0.1),
            run_time=0.8,
        )

        checkpoints = [2.45, 3.35, 4.15]
        for x, tile in zip(checkpoints, log_stack):
            self.play(
                robot.animate.move_to(np.array([x, 0.38, 0])),
                run_time=0.55,
                rate_func=smooth,
            )
            self.play(FadeIn(tile, shift=UP * 0.08), run_time=0.18)

        self.play(
            robot.animate.move_to(RIGHT * 4.7 + UP * 0.38),
            FadeIn(log_label),
            FadeIn(robot_caption, shift=UP * 0.12),
            run_time=0.55,
            rate_func=smooth,
        )
        self.play(
            ShowCreation(insight_rule),
            FadeIn(insight, shift=UP * 0.1),
            run_time=0.7,
        )
        self.wait(1.5)
        self._close()
