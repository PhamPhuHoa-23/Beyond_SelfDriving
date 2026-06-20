"""P05-S02a: web-scale language data versus physical robot experience."""
from manimlib import *

from studio.components import (
    StudioScene,
    BG_PAPER,
    BG_CARD,
    PASTEL_BLUE,
    PASTEL_TEAL,
    PASTEL_AMBER,
    ACCENT_BLUE,
    ACCENT_TEAL,
    ACCENT_AMBER,
    ACCENT_PINK,
    RED_ERROR,
    GREEN_FIX,
    GOLD_RICH,
    CYAN_RADAR,
    INK_DARK,
    INK_MID,
    INK_LIGHT,
    LINE_GRID,
    LINE_SEP,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    radar_shells_2d,
    sensor_cone,
    vehicle_icon,
)

SCRIPT = (
    "Large language models succeeded because of one thing: the internet. "
    "Trillions of tokens of human-generated text, freely available, covering "
    "virtually every domain of human knowledge and behavior. Training on that "
    "corpus gave LLMs world knowledge, common sense, and generalizable reasoning - "
    "capabilities that emerged from scale, not from hand-engineered rules. "
    "Robots do not have an internet. Robotic behavior data must be collected "
    "physically - each robot, in each environment, performing each task, observed "
    "by sensors and annotated either by humans or by auxiliary systems. You cannot "
    "crawl the web for robot navigation trajectories. There is no existing corpus "
    "of how a delivery robot should navigate a crowded university campus. The data "
    "problem for physical AI is categorically different from the data problem for "
    "language AI."
)


class P05S02ALLMVsRobot(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Web Data vs. Robot Experience"

    def claim_card(self, kicker, title, color):
        kicker_mob = Text(
            kicker,
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=color,
            weight=BOLD,
        )
        kicker_mob.set_color(color)
        title_mob = Text(
            title,
            font=FONT_PRIMARY,
            font_size=30,
            color=INK_DARK,
        )
        copy = VGroup(kicker_mob, title_mob).arrange(DOWN, buff=0.08)
        bg = RoundedRectangle(
            width=copy.get_width() + 0.45,
            height=copy.get_height() + 0.26,
            corner_radius=0.12,
            fill_color=interpolate_color(color, WHITE, 0.92),
            fill_opacity=0.72,
            stroke_color=color,
            stroke_width=1.2,
        )
        copy.move_to(bg)
        underline = Line(
            bg.get_left() + RIGHT * 0.18 + DOWN * 0.02,
            bg.get_right() + LEFT * 0.18 + DOWN * 0.02,
            stroke_color=color,
            stroke_width=3.0,
            stroke_opacity=0.75,
        )
        underline.next_to(bg, DOWN, buff=0.05)
        return VGroup(bg, copy, underline)

    def web_source_card(self, label, color, kind):
        box = RoundedRectangle(
            width=1.78,
            height=0.56,
            corner_radius=0.09,
            fill_color=interpolate_color(color, WHITE, 0.86),
            fill_opacity=0.92,
            stroke_color=color,
            stroke_width=1.45,
        )

        if kind == "books":
            icon = VGroup(
                Rectangle(width=0.18, height=0.26, fill_color=color, fill_opacity=0.95, stroke_width=0),
                Rectangle(width=0.18, height=0.26, fill_color=interpolate_color(color, WHITE, 0.28), fill_opacity=0.95, stroke_width=0),
            ).arrange(RIGHT, buff=0.02)
            icon[0].rotate(-4 * DEGREES)
            icon[1].rotate(4 * DEGREES)
        elif kind == "wiki":
            icon = VGroup()
            for i in range(3):
                page = RoundedRectangle(
                    width=0.24,
                    height=0.28,
                    corner_radius=0.025,
                    fill_color=WHITE,
                    fill_opacity=0.94,
                    stroke_color=color,
                    stroke_width=1.0,
                )
                page.shift(RIGHT * i * 0.035 + UP * i * 0.02)
                icon.add(page)
        elif kind == "code":
            icon = Text(
                "{}",
                font=FONT_PRIMARY,
                font_size=18,
                color=color,
                weight=BOLD,
            )
            icon.set_color(color)
        elif kind == "forums":
            bubble_a = RoundedRectangle(
                width=0.27,
                height=0.18,
                corner_radius=0.04,
                fill_color=color,
                fill_opacity=0.88,
                stroke_width=0,
            )
            bubble_b = bubble_a.copy().scale(0.82)
            bubble_b.set_fill(interpolate_color(color, WHITE, 0.3), opacity=0.92)
            bubble_b.next_to(bubble_a, DR, buff=-0.02)
            icon = VGroup(bubble_a, bubble_b)
        else:
            reel = RoundedRectangle(
                width=0.34,
                height=0.22,
                corner_radius=0.035,
                fill_color=color,
                fill_opacity=0.9,
                stroke_width=0,
            )
            holes = VGroup()
            for dx in [-0.11, 0.0, 0.11]:
                holes.add(Square(side_length=0.04, fill_color=WHITE, fill_opacity=0.9, stroke_width=0).shift(RIGHT * dx))
            holes.move_to(reel)
            icon = VGroup(reel, holes)

        icon.move_to(box.get_left() + RIGHT * 0.34)
        text = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK)
        text.next_to(icon, RIGHT, buff=0.15)
        text.align_to(box, UP).shift(DOWN * 0.16)

        data_tabs = VGroup()
        for i in range(3):
            tab = RoundedRectangle(
                width=0.16,
                height=0.035,
                corner_radius=0.012,
                fill_color=color,
                fill_opacity=0.42 + i * 0.14,
                stroke_width=0,
            )
            tab.move_to(box.get_right() + LEFT * 0.22 + DOWN * (0.11 - i * 0.08))
            data_tabs.add(tab)

        return VGroup(box, icon, text, data_tabs)

    def llm_engine(self):
        glow = RoundedRectangle(
            width=2.14,
            height=1.88,
            corner_radius=0.22,
            fill_color=PASTEL_BLUE,
            fill_opacity=0.18,
            stroke_color=ACCENT_BLUE,
            stroke_width=6.5,
        )
        glow.set_stroke(ACCENT_BLUE, width=6.5, opacity=0.14)

        body = RoundedRectangle(
            width=1.9,
            height=1.66,
            corner_radius=0.18,
            fill_color=interpolate_color(PASTEL_BLUE, WHITE, 0.3),
            fill_opacity=0.9,
            stroke_color=ACCENT_BLUE,
            stroke_width=2.4,
        )

        layers = VGroup()
        for i in range(5):
            layer = RoundedRectangle(
                width=0.16,
                height=1.02 - abs(2 - i) * 0.08,
                corner_radius=0.04,
                fill_color=interpolate_color(ACCENT_BLUE, WHITE, 0.62),
                fill_opacity=0.55,
                stroke_color=ACCENT_BLUE,
                stroke_width=1.0,
            )
            layers.add(layer)
        layers.arrange(RIGHT, buff=0.14)
        layers.move_to(body.get_center() + DOWN * 0.02)

        left_ports = VGroup()
        right_ports = VGroup()
        for y in np.linspace(-0.47, 0.47, 5):
            left_ports.add(
                RoundedRectangle(
                    width=0.12,
                    height=0.055,
                    corner_radius=0.015,
                    fill_color=ACCENT_TEAL,
                    fill_opacity=0.78,
                    stroke_width=0,
                ).move_to(body.get_left() + RIGHT * 0.08 + UP * y)
            )
            right_ports.add(
                RoundedRectangle(
                    width=0.12,
                    height=0.055,
                    corner_radius=0.015,
                    fill_color=ACCENT_AMBER,
                    fill_opacity=0.72,
                    stroke_width=0,
                ).move_to(body.get_right() + LEFT * 0.08 + UP * y)
            )
        ports = VGroup(left_ports, right_ports)

        arcs = VGroup()

        label = Text("LLM", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        label.move_to(body.get_center() + DOWN * 0.68)
        subtitle = VGroup()

        return VGroup(glow, body, ports, layers, arcs, subtitle, label)

    def token_packet(self, color):
        return RoundedRectangle(
            width=0.13,
            height=0.085,
            corner_radius=0.02,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        )

    def delivery_robot_rig(self):
        return vehicle_icon(color=ACCENT_PINK, scale=0.42)

    def route_angle(self, route, t):
        delta = 0.012
        t0 = float(np.clip(t - delta, 0.0, 1.0))
        t1 = float(np.clip(t + delta, 0.0, 1.0))
        tangent = route.pfp(t1) - route.pfp(t0)
        if np.linalg.norm(tangent) < 1e-6:
            return 0.0
        return np.arctan2(tangent[1], tangent[0])

    def route_front_point(self, route, t, distance=0.25):
        angle = self.route_angle(route, t)
        return route.pfp(float(np.clip(t, 0.0, 1.0))) + rotate_vector(RIGHT * distance, angle)

    def place_vehicle_on_route(self, vehicle, base_vehicle, route, t):
        t = float(np.clip(t, 0.0, 1.0))
        angle = self.route_angle(route, t)
        vehicle.become(base_vehicle.copy().rotate(angle).move_to(route.pfp(t)))
        return vehicle

    def drive_vehicle(self, vehicle, base_vehicle, route, start_t, end_t, run_time):
        def update_vehicle(mob, alpha):
            t = interpolate(start_t, end_t, alpha)
            self.place_vehicle_on_route(mob, base_vehicle, route, t)

        return UpdateFromAlphaFunc(vehicle, update_vehicle, run_time=run_time, rate_func=smooth)

    def physical_world_panel(self):
        panel = RoundedRectangle(
            width=4.84,
            height=1.7,
            corner_radius=0.14,
            fill_color=interpolate_color(PASTEL_TEAL, WHITE, 0.72),
            fill_opacity=0.94,
            stroke_color=LINE_GRID,
            stroke_width=1.4,
        )
        road = RoundedRectangle(
            width=4.42,
            height=0.98,
            corner_radius=0.11,
            fill_color=interpolate_color(LINE_GRID, WHITE, 0.34),
            fill_opacity=0.9,
            stroke_color=LINE_GRID,
            stroke_width=1.0,
        )
        road.move_to(panel.get_center() + DOWN * 0.04)

        lane_marks = VGroup()
        for x in np.linspace(-1.75, 1.75, 6):
            mark = Line(
                LEFT * 0.16,
                RIGHT * 0.16,
                stroke_color=WHITE,
                stroke_width=2.1,
                stroke_opacity=0.92,
            )
            mark.move_to(road.get_center() + RIGHT * x + DOWN * 0.01)
            lane_marks.add(mark)

        route = CubicBezier(
            road.get_left() + RIGHT * 0.35 + DOWN * 0.22,
            road.get_left() + RIGHT * 1.35 + UP * 0.48,
            road.get_right() + LEFT * 1.32 + DOWN * 0.48,
            road.get_right() + LEFT * 0.32 + UP * 0.2,
        )
        route.set_stroke(ACCENT_PINK, width=2.3, opacity=0.42)

        checkpoints = VGroup()
        for t, color in [(0.28, ACCENT_PINK), (0.57, ACCENT_TEAL), (0.83, ACCENT_AMBER)]:
            checkpoints.add(
                Circle(
                    radius=0.085,
                    fill_color=WHITE,
                    fill_opacity=1.0,
                    stroke_color=color,
                    stroke_width=2.0,
                ).move_to(route.pfp(t))
            )

        obstacle = VGroup(
            Circle(radius=0.08, fill_color=ACCENT_AMBER, fill_opacity=1.0, stroke_width=0),
            Line(UP * 0.01, DOWN * 0.23, stroke_color=ACCENT_AMBER, stroke_width=2.0),
            Line(DOWN * 0.09, DOWN * 0.22 + LEFT * 0.11, stroke_color=ACCENT_AMBER, stroke_width=1.8),
            Line(DOWN * 0.09, DOWN * 0.22 + RIGHT * 0.1, stroke_color=ACCENT_AMBER, stroke_width=1.8),
        )
        obstacle.move_to(road.get_center() + RIGHT * 0.48 + UP * 0.22)

        flag_pole = Line(ORIGIN, UP * 0.42, stroke_color=GOLD_RICH, stroke_width=2.0)
        flag = Triangle(fill_color=GOLD_RICH, fill_opacity=0.95, stroke_width=0)
        flag.scale(0.12)
        flag.rotate(-90 * DEGREES)
        flag.next_to(flag_pole.get_top(), RIGHT, buff=0.0)
        target = VGroup(flag_pole, flag)
        target.move_to(route.get_end() + UP * 0.25)

        label = Text("real world", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        label.next_to(panel, UP, buff=0.14).align_to(panel, LEFT).shift(RIGHT * 0.12)

        return VGroup(panel, road, lane_marks, route, checkpoints, obstacle, target, label)

    def experience_log_card(self, label, color):
        box = RoundedRectangle(
            width=0.92,
            height=0.62,
            corner_radius=0.065,
            fill_color=interpolate_color(color, WHITE, 0.82),
            fill_opacity=0.98,
            stroke_color=color,
            stroke_width=1.35,
        )
        title = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=color, weight=BOLD)
        title.set_color(color)
        title.move_to(box.get_top() + DOWN * 0.13)
        rows = VGroup()
        row_specs = [("obs", ACCENT_TEAL), ("act", ACCENT_PINK), ("label", ACCENT_AMBER)]
        for i, (row_label, row_color) in enumerate(row_specs):
            dot = Dot(radius=0.022, color=row_color)
            line = Line(LEFT * 0.11, RIGHT * 0.22, stroke_color=INK_LIGHT, stroke_width=1.0, stroke_opacity=0.58)
            row = VGroup(dot, line).arrange(RIGHT, buff=0.045)
            row.move_to(box.get_center() + LEFT * 0.05 + DOWN * (0.01 + i * 0.12))
            rows.add(row)
        stamp = VGroup(
            Line(LEFT * 0.055, ORIGIN, stroke_color=GREEN_FIX, stroke_width=1.5),
            Line(ORIGIN, RIGHT * 0.11 + UP * 0.1, stroke_color=GREEN_FIX, stroke_width=1.5),
        )
        stamp.move_to(box.get_bottom() + UP * 0.1 + RIGHT * 0.23)
        return VGroup(box, title, rows, stamp)

    def factor_chip(self, label, color):
        text = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=color, weight=BOLD)
        text.set_color(color)
        box = RoundedRectangle(
            width=text.get_width() + 0.3,
            height=0.38,
            corner_radius=0.1,
            fill_color=interpolate_color(color, WHITE, 0.88),
            fill_opacity=0.95,
            stroke_color=color,
            stroke_width=1.45,
        )
        text.move_to(box)
        return VGroup(box, text)

    def make_search_panel(self):
        panel = RoundedRectangle(
            width=4.45,
            height=0.94,
            corner_radius=0.12,
            fill_color=BG_CARD,
            fill_opacity=0.95,
            stroke_color=LINE_SEP,
            stroke_width=1.4,
        )
        query = Text(
            "crawl robot trajectories",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_DARK,
        )
        query.move_to(panel.get_center() + LEFT * 0.18 + UP * 0.17)
        lens = Circle(radius=0.08, stroke_color=INK_LIGHT, stroke_width=1.5)
        handle = Line(ORIGIN, RIGHT * 0.1 + DOWN * 0.1, stroke_color=INK_LIGHT, stroke_width=1.5)
        handle.next_to(lens, DR, buff=-0.02)
        search_icon = VGroup(lens, handle)
        search_icon.move_to(panel.get_left() + RIGHT * 0.32 + UP * 0.16)
        query.next_to(search_icon, RIGHT, buff=0.12)

        spinner = VGroup()
        for i in range(8):
            dot = Dot(radius=0.023, color=ACCENT_PINK)
            dot.set_opacity(0.18 + 0.08 * i)
            dot.move_to(panel.get_center() + RIGHT * 1.73 + DOWN * 0.21 + rotate_vector(RIGHT * 0.16, i * TAU / 8))
            spinner.add(dot)

        result = Text("no web corpus", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
        result.set_color(RED_ERROR)
        result.move_to(panel.get_center() + DOWN * 0.24)
        strike = Line(
            query.get_left() + LEFT * 0.02,
            query.get_right() + RIGHT * 0.02,
            stroke_color=RED_ERROR,
            stroke_width=2.2,
        )
        return VGroup(panel, search_icon, query, spinner, result, strike)

    def corpus_tile(self, kind, color):
        box = RoundedRectangle(
            width=0.44,
            height=0.3,
            corner_radius=0.04,
            fill_color=interpolate_color(color, WHITE, 0.84),
            fill_opacity=0.88,
            stroke_color=color,
            stroke_width=0.8,
            stroke_opacity=0.7,
        )
        if kind == "text":
            glyph = VGroup(
                Line(LEFT * 0.1, RIGHT * 0.12, stroke_color=color, stroke_width=1.0),
                Line(LEFT * 0.1, RIGHT * 0.06, stroke_color=color, stroke_width=1.0),
                Line(LEFT * 0.1, RIGHT * 0.1, stroke_color=color, stroke_width=1.0),
            ).arrange(DOWN, buff=0.035)
        elif kind == "code":
            glyph = Text("</>", font=FONT_PRIMARY, font_size=8, color=color, weight=BOLD)
            glyph.set_color(color)
        elif kind == "chat":
            glyph = VGroup(
                RoundedRectangle(width=0.19, height=0.09, corner_radius=0.025, fill_color=color, fill_opacity=0.8, stroke_width=0),
                RoundedRectangle(width=0.14, height=0.08, corner_radius=0.025, fill_color=interpolate_color(color, WHITE, 0.28), fill_opacity=0.9, stroke_width=0),
            ).arrange(DOWN, buff=0.025)
        else:
            glyph = VGroup()
            for dx in [-0.1, 0.0, 0.1]:
                glyph.add(Square(side_length=0.045, fill_color=color, fill_opacity=0.85, stroke_width=0).shift(RIGHT * dx))
        glyph.move_to(box)
        return VGroup(box, glyph)

    def capability_badge(self, label, color):
        box = RoundedRectangle(
            width=0.58,
            height=0.34,
            corner_radius=0.09,
            fill_color=interpolate_color(color, WHITE, 0.86),
            fill_opacity=0.95,
            stroke_color=color,
            stroke_width=1.4,
        )
        glyph = VGroup(
            Dot(radius=0.03, color=color),
            Line(LEFT * 0.08, RIGHT * 0.08, stroke_color=color, stroke_width=1.2),
            Line(LEFT * 0.08, RIGHT * 0.05, stroke_color=color, stroke_width=1.2),
        ).arrange(DOWN, buff=0.035)
        glyph.move_to(box)
        return VGroup(box, glyph)

    def annotation_pipeline(self):
        colors = [ACCENT_TEAL, ACCENT_AMBER, GREEN_FIX]
        cards = VGroup()
        arrows = VGroup()
        for index, color in enumerate(colors):
            box = RoundedRectangle(
                width=0.66,
                height=0.48,
                corner_radius=0.08,
                fill_color=interpolate_color(color, WHITE, 0.86),
                fill_opacity=0.96,
                stroke_color=color,
                stroke_width=1.2,
            )
            if index == 0:
                glyph = VGroup(
                    Arc(radius=0.13, start_angle=-35 * DEGREES, angle=70 * DEGREES, stroke_color=color, stroke_width=1.5),
                    Dot(radius=0.024, color=color),
                )
            elif index == 1:
                glyph = VGroup(
                    Line(LEFT * 0.09 + DOWN * 0.06, RIGHT * 0.08 + UP * 0.08, stroke_color=color, stroke_width=1.5),
                    Circle(radius=0.055, stroke_color=color, stroke_width=1.3, fill_opacity=0),
                )
            else:
                glyph = VGroup(
                    Line(LEFT * 0.09, LEFT * 0.015 + DOWN * 0.07, stroke_color=color, stroke_width=1.7),
                    Line(LEFT * 0.015 + DOWN * 0.07, RIGHT * 0.11 + UP * 0.09, stroke_color=color, stroke_width=1.7),
                )
            glyph.move_to(box)
            cards.add(VGroup(box, glyph))
        cards.arrange(RIGHT, buff=0.28)
        for left, right in zip(cards[:-1], cards[1:]):
            arrows.add(
                Arrow(
                    left.get_right() + RIGHT * 0.03,
                    right.get_left() + LEFT * 0.03,
                    buff=0,
                    stroke_color=INK_LIGHT,
                    stroke_width=1.5,
                )
            )
        panel = RoundedRectangle(
            width=cards.get_width() + 0.38,
            height=cards.get_height() + 0.3,
            corner_radius=0.12,
            fill_color=BG_CARD,
            fill_opacity=0.72,
            stroke_color=LINE_SEP,
            stroke_width=1.0,
        )
        VGroup(cards, arrows).move_to(panel)
        return VGroup(panel, cards, arrows)

    def campus_absence_card(self):
        card = RoundedRectangle(
            width=3.15,
            height=0.9,
            corner_radius=0.13,
            fill_color=BG_CARD,
            fill_opacity=0.96,
            stroke_color=RED_ERROR,
            stroke_width=1.6,
        )
        title = Text("no campus corpus", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
        title.set_color(RED_ERROR)
        result = Text("0 matches", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_LIGHT)
        stack = VGroup(title, result).arrange(DOWN, buff=0.08)
        stack.move_to(card)
        cross = VGroup(
            Line(card.get_left() + RIGHT * 0.2, card.get_right() + LEFT * 0.2, stroke_color=RED_ERROR, stroke_width=1.7, stroke_opacity=0.32),
            Line(card.get_left() + RIGHT * 0.2 + DOWN * 0.18, card.get_right() + LEFT * 0.2 + DOWN * 0.18, stroke_color=RED_ERROR, stroke_width=1.7, stroke_opacity=0.32),
        )
        return VGroup(card, stack, cross)

    def data_gap_meter(self):
        left_bar = RoundedRectangle(
            width=2.1,
            height=0.16,
            corner_radius=0.04,
            fill_color=ACCENT_BLUE,
            fill_opacity=0.9,
            stroke_width=0,
        )
        right_bar = RoundedRectangle(
            width=0.42,
            height=0.16,
            corner_radius=0.04,
            fill_color=ACCENT_PINK,
            fill_opacity=0.9,
            stroke_width=0,
        )
        left_ticks = VGroup(*(Dot(radius=0.018, color=ACCENT_BLUE) for _ in range(12))).arrange(RIGHT, buff=0.055)
        right_ticks = VGroup(*(Dot(radius=0.018, color=ACCENT_PINK) for _ in range(3))).arrange(RIGHT, buff=0.055)
        left = VGroup(left_bar, left_ticks).arrange(DOWN, buff=0.08)
        right = VGroup(right_bar, right_ticks).arrange(DOWN, buff=0.08)
        left_ticks.align_to(left_bar, LEFT)
        right_ticks.align_to(right_bar, LEFT)
        bracket = VGroup(
            Line(UP * 0.24, DOWN * 0.24, stroke_color=LINE_SEP, stroke_width=1.2),
            Line(UP * 0.24, UP * 0.24 + RIGHT * 0.14, stroke_color=LINE_SEP, stroke_width=1.2),
            Line(DOWN * 0.24, DOWN * 0.24 + RIGHT * 0.14, stroke_color=LINE_SEP, stroke_width=1.2),
        )
        group = VGroup(left, bracket, right).arrange(RIGHT, buff=0.38)
        return group

    def clean_radar_ping_2d(self, center, color=CYAN_RADAR, radius=0.48):
        waves = VGroup()
        anims = []
        for i in range(3):
            circle = Circle(
                radius=radius,
                stroke_color=color,
                stroke_width=2.2 - i * 0.6,
                stroke_opacity=0.85 - i * 0.25,
            )
            circle.move_to(center)
            circle.scale(0.05)
            waves.add(circle)
            anims.append(
                circle.animate(run_time=0.98, rate_func=linear)
                .scale(20.0 + i * 8.0)
                .set_stroke(opacity=0)
            )
        return waves, LaggedStart(*anims, lag_ratio=0.25)

    def server_rack_icon(self, color=INK_LIGHT, scale=0.45):
        rack = VGroup()
        
        # Outer frame
        frame = RoundedRectangle(
            width=0.72,
            height=0.96,
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=1.5,
            fill_color=BG_PAPER,
            fill_opacity=1.0,
        )
        rack.add(frame)
        
        leds = VGroup()
        # 3 server slots inside
        for i in range(3):
            slot = RoundedRectangle(
                width=0.56,
                height=0.18,
                corner_radius=0.04,
                stroke_color=interpolate_color(color, WHITE, 0.4),
                stroke_width=1.0,
                fill_color=BG_CARD,
                fill_opacity=0.6,
            )
            slot.move_to(frame.get_center() + UP * (0.26 - i * 0.26))
            rack.add(slot)
            
            # Detail line (tray pull handle)
            detail = Line(
                slot.get_left() + RIGHT * 0.08,
                slot.get_left() + RIGHT * 0.22,
                stroke_color=color,
                stroke_width=1.2,
            )
            detail.move_to(slot.get_center() + LEFT * 0.1)
            rack.add(detail)
            
            # Inactive LED status dot (gray / line_sep color)
            led = Dot(
                radius=0.024,
                color=interpolate_color(color, WHITE, 0.3),
            )
            led.move_to(slot.get_center() + RIGHT * 0.16)
            rack.add(led)
            leds.add(led)
            
        rack.leds = leds  # Attach leds group for direct animation access
        rack.scale(scale)
        return rack

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        divider = Line(
            UP * 2.35,
            DOWN * 2.38,
            stroke_color=LINE_SEP,
            stroke_width=1.5,
            stroke_opacity=0.9,
        )

        web_heading = self.claim_card("LANGUAGE AI", "Data already exists", ACCENT_BLUE)
        web_heading.move_to(LEFT * 3.45 + UP * 2.05)
        robot_heading = self.claim_card("PHYSICAL AI", "Experience must be created", ACCENT_PINK)
        robot_heading.move_to(RIGHT * 3.45 + UP * 2.05)

        shimmer = VGroup()
        shimmer_colors = [ACCENT_AMBER, ACCENT_BLUE, ACCENT_TEAL, ACCENT_PINK]
        for i in range(16):
            packet = self.token_packet(shimmer_colors[i % len(shimmer_colors)])
            packet.scale(0.72 + 0.08 * (i % 3))
            packet.move_to(np.array([-5.92 + (i % 4) * 0.72, 1.0 - (i // 4) * 0.36, 0]))
            shimmer.add(packet)

        corpus_kinds = ["text", "code", "chat", "video"]
        corpus_colors = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER, ACCENT_PINK]
        corpus_tiles = VGroup()
        for i in range(36):
            tile = self.corpus_tile(corpus_kinds[i % len(corpus_kinds)], corpus_colors[i % len(corpus_colors)])
            tile.scale(0.78 + 0.04 * (i % 4))
            x = -6.05 + (i % 6) * 0.58
            y = 1.25 - (i // 6) * 0.34
            tile.move_to(np.array([x, y, 0]))
            corpus_tiles.add(tile)
        corpus_label = VGroup(*(Dot(radius=0.018, color=INK_LIGHT) for _ in range(8))).arrange(RIGHT, buff=0.08)
        corpus_label.next_to(corpus_tiles, UP, buff=0.12).align_to(corpus_tiles, LEFT)

        source_specs = [
            ("Books", ACCENT_AMBER, "books"),
            ("Wikipedia", ACCENT_BLUE, "wiki"),
            ("GitHub", ACCENT_TEAL, "code"),
            ("Forums", ACCENT_PINK, "forums"),
            ("Video", ACCENT_AMBER, "video"),
        ]
        sources = VGroup(*(self.web_source_card(*spec) for spec in source_specs))
        sources.arrange(DOWN, buff=0.16)
        sources.move_to(LEFT * 5.32 + DOWN * 0.32)

        llm = self.llm_engine()
        llm.move_to(LEFT * 1.48 + DOWN * 0.28)

        streams = VGroup()
        for i, source in enumerate(sources):
            start = source[0].get_right() + RIGHT * 0.05
            end = llm[1].get_left() + LEFT * 0.08 + UP * (0.5 - i * 0.25)
            stream = CubicBezier(
                start,
                start + RIGHT * 0.85 + UP * (0.2 - i * 0.07),
                end + LEFT * 0.68,
                end,
            )
            stream.set_stroke(source_specs[i][1], width=2.8, opacity=0.54)
            streams.add(stream)

        web_stat = Text("Trillions of tokens", font=FONT_PRIMARY, font_size=25, color=ACCENT_BLUE, weight=BOLD)
        web_stat.set_color(ACCENT_BLUE)
        web_caption = VGroup(web_stat)
        web_caption.move_to(LEFT * 3.45 + DOWN * 2.43)

        search_panel = self.make_search_panel()
        search_panel.move_to(RIGHT * 3.5 + UP * 0.18)

        world = self.physical_world_panel()
        world.move_to(RIGHT * 3.48 + UP * 0.32)
        route = world[3]
        checkpoints = world[4]

        robot_template = self.delivery_robot_rig()
        robot = robot_template.copy()
        self.place_vehicle_on_route(robot, robot_template, route, 0.0)
        trace = TracedPath(
            robot.get_center,
            stroke_color=ACCENT_PINK,
            stroke_width=2.8,
            stroke_opacity=0.75,
            time_traced=10,
        )

        factor_chips = VGroup(
            self.factor_chip("1 ROBOT", ACCENT_PINK),
            Text("×", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_LIGHT),
            self.factor_chip("1 WORLD", ACCENT_TEAL),
            Text("×", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_LIGHT),
            self.factor_chip("1 TASK", ACCENT_AMBER),
        ).arrange(RIGHT, buff=0.14)
        factor_chips.move_to(RIGHT * 2.9 + DOWN * 1.15)

        db_icon = self.server_rack_icon(color=INK_LIGHT, scale=0.45)
        db_icon.move_to(RIGHT * 5.15 + DOWN * 1.15)

        robot_stat = Text("one run at a time", font=FONT_PRIMARY, font_size=25, color=ACCENT_PINK, weight=BOLD)
        robot_stat.set_color(ACCENT_PINK)
        robot_caption = VGroup(robot_stat)
        robot_caption.move_to(RIGHT * 3.45 + DOWN * 2.43)

        insight_rule = Line(LEFT * 5.55, RIGHT * 5.55, stroke_color=LINE_SEP, stroke_width=1.15)
        insight_rule.move_to(DOWN * 2.78)
        insight_left = Text("The web stores text.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        insight_right = Text("Robot behavior must be made.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_PINK, weight=BOLD)
        insight_right.set_color(ACCENT_PINK)
        insight = VGroup(insight_left, insight_right).arrange(RIGHT, buff=0.3)
        insight.next_to(insight_rule, DOWN, buff=0.18)

        abundance = Text("ABUNDANT", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GREEN_FIX, weight=BOLD)
        abundance.set_color(GREEN_FIX)
        expensive = Text("EXPENSIVE", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
        expensive.set_color(RED_ERROR)
        abundance.move_to(LEFT * 3.45 + DOWN * 2.08)
        expensive.move_to(RIGHT * 3.45 + DOWN * 2.08)

        self.play(
            ShowCreation(divider),
            FadeIn(web_heading, shift=DOWN * 0.12),
            FadeIn(robot_heading, shift=DOWN * 0.12),
            run_time=0.7,
        )
        self.play(
            LaggedStart(*(FadeIn(packet, shift=RIGHT * 0.08) for packet in shimmer), lag_ratio=0.035),
            run_time=0.45,
        )
        self.play(
            LaggedStart(*(packet.animate.shift(RIGHT * 0.2 + UP * (0.04 * ((i % 3) - 1))) for i, packet in enumerate(shimmer)), lag_ratio=0.02),
            run_time=0.45,
            rate_func=there_and_back,
        )
        self.play(
            FadeOut(shimmer, scale=0.7),
            FadeIn(corpus_label, shift=DOWN * 0.08),
            LaggedStart(*(FadeIn(tile, scale=0.85) for tile in corpus_tiles), lag_ratio=0.018),
            run_time=1.0,
        )
        self.play(
            LaggedStart(
                *(
                    tile.animate.shift(UP * (0.06 * ((i % 3) - 1)) + RIGHT * (0.04 * ((i % 4) - 1.5)))
                    for i, tile in enumerate(corpus_tiles)
                ),
                lag_ratio=0.01,
            ),
            run_time=0.85,
            rate_func=there_and_back,
        )

        self.play(
            FadeOut(corpus_label, shift=UP * 0.06),
            FadeOut(corpus_tiles, scale=0.55),
            run_time=0.25,
        )
        self.play(
            LaggedStart(*(FadeIn(source, shift=RIGHT * 0.22) for source in sources), lag_ratio=0.08),
            FadeIn(llm[0], scale=1.12),
            FadeIn(llm[1]),
            LaggedStart(*(FadeIn(mob, scale=0.8) for mob in [llm[2], llm[3], llm[4], llm[5], llm[6]]), lag_ratio=0.08),
            run_time=0.45,
        )
        self.play(
            LaggedStart(*(ShowCreation(stream) for stream in streams), lag_ratio=0.08),
            run_time=0.52,
        )

        token_packets = VGroup()
        token_anims = []
        for i in range(54):
            source_index = i % len(streams)
            packet = self.token_packet(source_specs[source_index][1])
            packet.move_to(streams[source_index].get_start())
            token_packets.add(packet)
            token_anims.append(MoveAlongPath(packet, streams[source_index].copy(), rate_func=linear))
        self.add(token_packets)
        self.play(
            LaggedStart(*token_anims, lag_ratio=0.024),
            run_time=3.15,
        )
        self.play(
            FadeOut(token_packets, scale=0.55),
            run_time=0.55,
        )
        self.play(
            FadeIn(web_caption, shift=UP * 0.14),
            FadeIn(abundance, shift=UP * 0.08),
            run_time=0.55,
        )

        for i in range(3):
            capability_packets = VGroup()
            capability_anims = []
            for j in range(10):
                source_index = (i + j) % len(streams)
                packet = self.token_packet(source_specs[source_index][1]).scale(0.82)
                packet.move_to(streams[source_index].get_start())
                capability_packets.add(packet)
                capability_anims.append(MoveAlongPath(packet, streams[source_index].copy(), rate_func=linear))
            self.add(capability_packets)
            self.play(
                LaggedStart(*capability_anims, lag_ratio=0.055),
                run_time=0.82,
            )
            self.play(FadeOut(capability_packets, scale=0.6), run_time=0.22)
            self.wait(0.1)
        for wave_index in range(8):
            extended_packets = VGroup()
            extended_anims = []
            for j in range(22):
                source_index = (wave_index + j) % len(streams)
                packet = self.token_packet(source_specs[source_index][1]).scale(0.86)
                packet.move_to(streams[source_index].get_start())
                extended_packets.add(packet)
                extended_anims.append(MoveAlongPath(packet, streams[source_index].copy(), rate_func=linear))
            self.add(extended_packets)
            self.play(
                LaggedStart(*extended_anims, lag_ratio=0.035),
                run_time=1.405,
            )
            self.remove(extended_packets)

        self.play(FadeIn(search_panel[0]), FadeIn(search_panel[1]), FadeIn(search_panel[2]), run_time=0.65)
        self.play(FadeIn(search_panel[3]), Rotate(search_panel[3], TAU), run_time=0.9, rate_func=smooth)
        self.play(
            FadeIn(search_panel[4], shift=UP * 0.08),
            ShowCreation(search_panel[5]),
            Flash(search_panel[4], color=RED_ERROR, line_length=0.13, num_lines=8),
            run_time=0.75,
        )
        self.wait(0.2)
        self.play(FadeOut(search_panel, shift=DOWN * 0.14), run_time=0.45)

        self.play(
            FadeIn(world[0]),
            FadeIn(world[1]),
            FadeIn(world[7], shift=DOWN * 0.08),
            run_time=0.75,
        )
        self.play(
            LaggedStart(*(FadeIn(mark) for mark in world[2]), lag_ratio=0.06),
            ShowCreation(world[3]),
            FadeIn(world[5], scale=0.9),
            FadeIn(world[6], shift=UP * 0.08),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*(GrowFromCenter(check) for check in checkpoints), lag_ratio=0.14),
            FadeIn(db_icon, scale=0.8),
            run_time=0.75,
        )

        self.add(trace)
        self.play(FadeIn(robot, scale=0.92), Flash(robot, color=ACCENT_PINK, line_length=0.11, num_lines=7), run_time=0.6)

        move_segments = [
            (0.0, 0.28, checkpoints[0], ACCENT_PINK),
            (0.28, 0.57, checkpoints[1], ACCENT_TEAL),
            (0.57, 0.83, checkpoints[2], ACCENT_AMBER),
        ]
        for idx, (start_t, end_t, checkpoint, color) in enumerate(move_segments):
            self.play(
                self.drive_vehicle(robot, robot_template, route, start_t, end_t, run_time=2.2),
            )
            sensor_origin = self.route_front_point(route, end_t, distance=0.26)
            rings, ring_anim = self.clean_radar_ping_2d(sensor_origin, color=CYAN_RADAR, radius=0.48)
            ray = Line(
                self.route_front_point(route, end_t, distance=0.34),
                checkpoint.get_center(),
                stroke_color=color,
                stroke_width=2.0,
                stroke_opacity=0.7,
            )
            self.play(
                ring_anim,
                ShowPassingFlash(ray.copy().set_stroke(color, width=4.2, opacity=0.95), time_width=0.35),
                run_time=0.98,
            )
            self.remove(rings)

            packet = self.token_packet(color).scale(0.8)
            packet.move_to(checkpoint.get_center())
            
            path = CubicBezier(
                checkpoint.get_center(),
                checkpoint.get_center() + DOWN * 0.4 + RIGHT * 0.2,
                db_icon.get_center() + UP * 0.5 + LEFT * 0.2,
                db_icon.get_center(),
            )
            
            self.play(
                checkpoint.animate(run_time=0.5)
                .set_fill(GREEN_FIX, opacity=1.0)
                .set_stroke(GREEN_FIX, width=2.0),
                
                MoveAlongPath(packet, path, rate_func=smooth),
                run_time=1.5,
            )
            db_icon.leds[idx].set_color(color)
            self.play(
                Flash(db_icon, color=color, line_length=0.1, num_lines=6),
                db_icon.animate.scale(1.15),
                FadeOut(packet, scale=0.4),
                run_time=0.36,
                rate_func=there_and_back,
            )

        self.play(
            self.drive_vehicle(robot, robot_template, route, 0.83, 0.94, run_time=1.8),
        )
        self.play(
            FadeIn(factor_chips, shift=UP * 0.1),
            run_time=0.9,
        )
        self.play(
            Flash(factor_chips[0], color=ACCENT_PINK, line_length=0.11, num_lines=7),
            Flash(factor_chips[2], color=ACCENT_TEAL, line_length=0.11, num_lines=7),
            Flash(factor_chips[4], color=ACCENT_AMBER, line_length=0.11, num_lines=7),
            run_time=0.9,
        )
        self.play(
            FadeIn(robot_caption, shift=UP * 0.1),
            FadeIn(expensive, shift=UP * 0.08),
            run_time=1.1,
        )
        self.wait(1.0)

        self.play(
            ShowCreation(insight_rule),
            FadeIn(insight, shift=UP * 0.1),
            run_time=1.75,
        )
        self.wait(2.2)
        self._close(trace)
