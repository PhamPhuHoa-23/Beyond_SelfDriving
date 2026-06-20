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
    pedestrian_icon,
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
        return pedestrian_icon(color=color).scale(0.42)

    def mini_corpus_tile(self, label, color):
        box = RoundedRectangle(
            width=0.86,
            height=0.42,
            corner_radius=0.06,
            fill_color=interpolate_color(color, WHITE, 0.88),
            fill_opacity=0.9,
            stroke_color=color,
            stroke_width=1.0,
        )
        txt = Text(label, font=FONT_PRIMARY, font_size=11, color=INK_DARK)
        txt.move_to(box)
        return VGroup(box, txt)

    def make_crawler(self):
        circle = Circle(radius=0.18, stroke_color=INK_LIGHT, stroke_width=1.5, fill_color=BG_PAPER, fill_opacity=0.8)
        handle = Line(ORIGIN, RIGHT * 0.14 + DOWN * 0.14, stroke_color=INK_LIGHT, stroke_width=1.5)
        handle.next_to(circle, DR, buff=-0.02)
        label = Text("robot behavior?", font=FONT_PRIMARY, font_size=10, color=RED_ERROR, weight=BOLD)
        label.next_to(circle, UP, buff=0.04)
        return VGroup(circle, handle, label)

    def make_cross(self, center, color=RED_ERROR):
        circle = Circle(radius=0.12, stroke_color=color, stroke_width=1.5)
        line = Line(LEFT * 0.08 + UP * 0.08, RIGHT * 0.08 + DOWN * 0.08, stroke_color=color, stroke_width=1.5)
        cross = VGroup(circle, line)
        cross.move_to(center)
        return cross

    def make_clock_counter(self):
        clock_circle = Circle(radius=0.12, stroke_color=INK_LIGHT, stroke_width=1.2)
        hand_h = Line(ORIGIN, UP * 0.07, stroke_color=INK_LIGHT, stroke_width=1.2)
        hand_m = Line(ORIGIN, RIGHT * 0.05, stroke_color=INK_LIGHT, stroke_width=1.2)
        clock = VGroup(clock_circle, hand_h, hand_m)
        text = Text("0 runs", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        text.next_to(clock, RIGHT, buff=0.08)
        return VGroup(clock, text)

    def make_drop(self, color=ACCENT_PINK, scale=0.18):
        drop = VMobject(fill_color=color, fill_opacity=0.9, stroke_width=0)
        drop.set_points_as_corners([
            UP * 0.5,
            RIGHT * 0.3 + DOWN * 0.2,
            DOWN * 0.5,
            LEFT * 0.3 + DOWN * 0.2,
            UP * 0.5,
        ])
        drop.make_smooth()
        drop.scale(scale)
        return drop

    def make_fleet_option(self):
        fleet = VGroup()
        for r in range(2):
            for c in range(3):
                bot = self.robot_marker(INK_LIGHT, 0.22)[0]
                bot.move_to(np.array([c * 0.28, -r * 0.22, 0]))
                fleet.add(bot)
        label = Text("$$$", font=FONT_PRIMARY, font_size=12, color=RED_ERROR, weight=BOLD)
        label.move_to(fleet)
        return VGroup(fleet, label)

    def make_sim_option(self):
        monitor = Rectangle(width=0.78, height=0.52, stroke_color=INK_LIGHT, stroke_width=1.2)
        stand = Line(monitor.get_bottom() + DOWN * 0.02, monitor.get_bottom() + DOWN * 0.12, stroke_color=INK_LIGHT, stroke_width=1.2)
        base = Line(monitor.get_bottom() + DOWN * 0.12 + LEFT * 0.15, monitor.get_bottom() + DOWN * 0.12 + RIGHT * 0.15, stroke_color=INK_LIGHT, stroke_width=1.2)
        crack = VMobject(stroke_color=RED_ERROR, stroke_width=1.5)
        crack.set_points_as_corners([
            monitor.get_top() + LEFT * 0.02,
            monitor.get_center() + RIGHT * 0.04 + UP * 0.08,
            monitor.get_center() + LEFT * 0.06 + DOWN * 0.08,
            monitor.get_bottom() + RIGHT * 0.02,
        ])
        return VGroup(monitor, stand, base, crack)

    def make_warn_stamp(self, center, color=RED_ERROR):
        circle = Circle(radius=0.12, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=1.0)
        excl = Text("!", font=FONT_PRIMARY, font_size=12, color=WHITE, weight=BOLD)
        excl.move_to(circle)
        stamp = VGroup(circle, excl)
        stamp.move_to(center)
        return stamp

    def make_gaze_arc(self, ped, robot, color=ACCENT_TEAL):
        line = DashedLine(
            ped.get_center(),
            robot.get_center(),
            stroke_color=color,
            stroke_width=1.0,
            dash_length=0.06,
        )
        return line

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

        # Right heading starts dimmed
        right_heading.set_opacity(0.25)

        # ----------------------------------------------------
        # INTRO SEQUENCE (0-2s)
        # ----------------------------------------------------
        self.play(
            FadeIn(divider),
            FadeIn(left_heading, shift=DOWN * 0.1),
            FadeIn(right_heading, shift=DOWN * 0.1),
            run_time=0.8,
        )
        self.wait(1.2)

        # ----------------------------------------------------
        # BARRIER 1: DATA BOTTLENECK (2-17s)
        # ----------------------------------------------------
        # B1.1: Web Crawl (2.0 to 5.5s)
        corpus_labels = [("Books", ACCENT_TEAL), ("Wiki", ACCENT_AMBER), ("GitHub", ACCENT_BLUE), ("Video", ACCENT_PINK)]
        corpus_tiles = VGroup(*(self.mini_corpus_tile(lbl, col) for lbl, col in corpus_labels))
        corpus_tiles.arrange(RIGHT, buff=0.18)
        corpus_tiles.move_to(LEFT * 3.55 + UP * 0.9)

        crawler = self.make_crawler()
        crawler.move_to(corpus_tiles[0].get_center() + UP * 0.4 + LEFT * 0.4)

        self.play(
            FadeIn(corpus_tiles),
            FadeIn(crawler),
            run_time=0.5
        )

        crosses = VGroup()
        for idx, tile in enumerate(corpus_tiles):
            self.play(crawler.animate.move_to(tile.get_center()), run_time=0.4, rate_func=smooth)
            cross = self.make_cross(tile.get_center(), RED_ERROR)
            self.play(
                FadeIn(cross, scale=1.2),
                tile.animate.set_opacity(0.35),
                run_time=0.2
            )
            crosses.add(cross)

        zero_count = Text("0 matches", font=FONT_PRIMARY, font_size=15, color=RED_ERROR, weight=BOLD)
        zero_count.next_to(crawler[0], DOWN, buff=0.08)
        self.play(FadeIn(zero_count, scale=1.1), run_time=0.3)
        self.wait(0.3)

        # Fade out web crawl
        self.play(
            FadeOut(corpus_tiles),
            FadeOut(crawler),
            FadeOut(crosses),
            FadeOut(zero_count),
            run_time=0.4
        )

        # B1.2: Mini-Worlds & Clock (5.5 to 9.5s)
        world_labels = [
            ("campus", ACCENT_TEAL),
            ("curb", ACCENT_AMBER),
            ("crosswalk", ACCENT_PINK),
        ]
        worlds = VGroup(*(self.mini_world(label, color) for label, color in world_labels))
        worlds.arrange(RIGHT, buff=0.24)
        worlds.move_to(LEFT * 3.55 + UP * 0.85)

        robot = self.robot_marker(ACCENT_PINK, 0.4)
        robot.move_to(worlds[0][1].get_center())

        clock_counter = self.make_clock_counter()
        clock_counter.move_to(LEFT * 1.8 + UP * 1.4)

        slow_label = Text(
            "one robot  ×  one environment  ×  one task",
            font=FONT_PRIMARY,
            font_size=18,
            color=INK_MID,
        )
        slow_label.move_to(LEFT * 3.55 + UP * 0.32)

        self.play(
            LaggedStart(*(FadeIn(w, shift=UP * 0.08) for w in worlds), lag_ratio=0.1),
            FadeIn(robot),
            FadeIn(clock_counter),
            FadeIn(slow_label),
            run_time=0.6
        )

        run_texts = ["1 run", "2 runs", "3 runs"]
        emitted_cards = VGroup()
        for idx in range(3):
            start_pt = worlds[idx][1].get_start()
            end_pt = worlds[idx][1].get_end()
            robot.move_to(start_pt)
            
            path = TracedPath(
                robot.get_center,
                stroke_color=ACCENT_PINK,
                stroke_width=3,
                stroke_opacity=0.9
            )
            self.add(path)
            
            self.play(
                robot.animate.move_to(end_pt),
                clock_counter[0][1].animate.rotate(-PI, about_point=clock_counter[0][1].get_start()),
                clock_counter[0][2].animate.rotate(-2*PI, about_point=clock_counter[0][2].get_start()),
                run_time=0.7,
                rate_func=smooth
            )
            
            new_text = Text(run_texts[idx], font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
            new_text.move_to(clock_counter[1])
            self.play(
                Transform(clock_counter[1], new_text),
                run_time=0.15
            )
            
            card = self.data_card(f"log {idx + 1}", world_labels[idx][1])
            card.scale(0.85)
            card.move_to(np.array([worlds[idx].get_x(), -0.25, 0]))
            self.play(FadeIn(card, shift=DOWN * 0.1), run_time=0.2)
            emitted_cards.add(card)
            
            self.remove(path)
            self.wait(0.1)

        # B1.3: Archive Grid (9.5 to 13.0s)
        archive_box = RoundedRectangle(
            width=2.5,
            height=1.2,
            corner_radius=0.08,
            fill_color=PASTEL_BLUE,
            fill_opacity=0.3,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.2,
            stroke_opacity=0.6,
        )
        archive_box.move_to(LEFT * 3.55 + DOWN * 1.25)
        
        archive_slots = VGroup()
        for r in range(6):
            for c in range(8):
                slot = Square(
                    side_length=0.08,
                    fill_color=WHITE,
                    fill_opacity=0.15,
                    stroke_color=ACCENT_BLUE,
                    stroke_width=0.6,
                    stroke_opacity=0.3,
                )
                slot.move_to(
                    archive_box.get_center()
                    + LEFT * 0.45
                    + RIGHT * c * 0.13
                    + UP * 0.35
                    + DOWN * r * 0.14
                )
                archive_slots.add(slot)

        gauge_bg = RoundedRectangle(
            width=1.2,
            height=0.12,
            corner_radius=0.03,
            stroke_color=INK_LIGHT,
            stroke_width=1.0,
            fill_color=BG_PAPER,
            fill_opacity=1
        )
        gauge_fill = RoundedRectangle(
            width=0.02,
            height=0.08,
            corner_radius=0.01,
            stroke_width=0,
            fill_color=ACCENT_PINK,
            fill_opacity=0.9
        )
        gauge_fill.align_to(gauge_bg, LEFT).shift(RIGHT * 0.02)
        gauge_text = Text("0.02% filled", font=FONT_PRIMARY, font_size=13, color=INK_MID)
        gauge_group = VGroup(gauge_bg, gauge_fill, gauge_text).arrange(RIGHT, buff=0.1)
        gauge_group.next_to(archive_box, RIGHT, buff=0.2)

        archive_label = Text(
            "needed: web-scale dataset",
            font=FONT_PRIMARY,
            font_size=16,
            color=ACCENT_BLUE,
        )
        archive_label.next_to(archive_box, DOWN, buff=0.08)
        archive = VGroup(archive_box, archive_slots, archive_label, gauge_group)

        self.play(FadeIn(archive, shift=UP * 0.08), run_time=0.6)

        target_slots = [archive_slots[12], archive_slots[27], archive_slots[39]]
        fly_animations = []
        slot_fills = VGroup()
        for card, slot, col in zip(emitted_cards, target_slots, [ACCENT_TEAL, ACCENT_AMBER, ACCENT_PINK]):
            slot_fill = Square(
                side_length=0.07,
                fill_color=col,
                fill_opacity=0.9,
                stroke_width=0
            )
            slot_fill.move_to(slot)
            slot_fills.add(slot_fill)
            fly_animations.append(
                ReplacementTransform(card, slot_fill)
            )
        self.play(
            *fly_animations,
            run_time=0.9,
            rate_func=smooth
        )
        self.wait(0.9)

        # Fade out archive, slot fills, and dim the rest before sprouting options (0.6s)
        self.play(
            FadeOut(archive),
            FadeOut(slot_fills),
            worlds.animate.set_opacity(0.18),
            robot.animate.set_opacity(0.18),
            clock_counter.animate.set_opacity(0.18),
            slow_label.animate.set_opacity(0.18),
            run_time=0.6
        )

        # B1.4: Scaling Options (13.0 to 15.0s)
        branch_start = LEFT * 3.55 + DOWN * 0.4
        left_branch = Line(branch_start, LEFT * 4.6 + DOWN * 1.1, stroke_color=INK_LIGHT, stroke_width=1.0)
        right_branch = Line(branch_start, LEFT * 2.5 + DOWN * 1.1, stroke_color=INK_LIGHT, stroke_width=1.0)
        
        fleet_opt = self.make_fleet_option()
        fleet_opt.move_to(LEFT * 4.6 + DOWN * 1.45)
        fleet_label = Text("physical fleet\n(high cost)", font=FONT_PRIMARY, font_size=14, color=INK_MID)
        fleet_label.next_to(fleet_opt, DOWN, buff=0.1)
        fleet_group = VGroup(fleet_opt, fleet_label)
        
        sim_opt = self.make_sim_option()
        sim_opt.move_to(LEFT * 2.5 + DOWN * 1.45)
        sim_label = Text("simulation\n(sim-to-real gap)", font=FONT_PRIMARY, font_size=14, color=INK_MID)
        sim_label.next_to(sim_opt, DOWN, buff=0.1)
        sim_group = VGroup(sim_opt, sim_label)

        self.play(
            ShowCreation(left_branch),
            ShowCreation(right_branch),
            FadeIn(fleet_group),
            FadeIn(sim_group),
            run_time=0.7
        )

        warn_fleet = self.make_warn_stamp(fleet_opt.get_center(), RED_ERROR)
        warn_sim = self.make_warn_stamp(sim_opt.get_center(), RED_ERROR)
        self.play(
            FadeIn(warn_fleet, scale=1.3),
            FadeIn(warn_sim, scale=1.3),
            fleet_group.animate.set_opacity(0.4),
            sim_group.animate.set_opacity(0.4),
            left_branch.animate.set_opacity(0.4),
            right_branch.animate.set_opacity(0.4),
            run_time=0.8
        )
        self.wait(0.5)

        # B1.5: Trickle Coalesce (15.0 to 17.0s)
        drop = self.make_drop(ACCENT_PINK, scale=0.3)
        drop.move_to(LEFT * 3.55 + DOWN * 1.2)

        b1_conclusion = Text(
            "Data arrives as a trickle.",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=ACCENT_PINK,
        )
        b1_conclusion.move_to(LEFT * 3.55 + DOWN * 2.05)
        
        self.play(
            FadeOut(fleet_group),
            FadeOut(sim_group),
            FadeOut(warn_fleet),
            FadeOut(warn_sim),
            FadeOut(left_branch),
            FadeOut(right_branch),
            FadeIn(drop, shift=DOWN * 0.1),
            FadeIn(b1_conclusion, shift=UP * 0.1),
            run_time=0.8
        )
        self.wait(1.2)

        # ----------------------------------------------------
        # BARRIER 2: HUMAN MODELING GAP (17-32s)
        # ----------------------------------------------------
        # Brighten Right Column Heading
        self.play(
            right_heading.animate.set_opacity(1.0),
            run_time=0.5
        )

        # B2.1: Intersection Panel Build (17.0 to 19.0s)
        city_bg = RoundedRectangle(
            width=4.55,
            height=2.3,
            corner_radius=0.12,
            fill_color="#E2E7EC",
            fill_opacity=0.95,
            stroke_color=LINE_GRID,
            stroke_width=1.2,
        )
        city_bg.move_to(RIGHT * 3.55 + UP * 0.2)
        C = city_bg.get_center()

        road_h = Rectangle(
            width=4.3,
            height=0.6,
            fill_color="#23272A",
            fill_opacity=1,
            stroke_width=0,
        )
        road_v = Rectangle(
            width=0.6,
            height=2.05,
            fill_color="#23272A",
            fill_opacity=1,
            stroke_width=0,
        )
        roads = VGroup(road_h, road_v).move_to(city_bg)

        # White dashed centerlines down the lanes
        centerline_h1 = DashedLine(C + LEFT * 2.15, C + LEFT * 0.35, stroke_color=WHITE, stroke_width=1.0, stroke_opacity=0.4, dash_length=0.08)
        centerline_h2 = DashedLine(C + RIGHT * 0.35, C + RIGHT * 2.15, stroke_color=WHITE, stroke_width=1.0, stroke_opacity=0.4, dash_length=0.08)
        centerline_v1 = DashedLine(C + UP * 1.025, C + UP * 0.3, stroke_color=WHITE, stroke_width=1.0, stroke_opacity=0.4, dash_length=0.08)
        centerline_v2 = DashedLine(C + DOWN * 0.3, C + DOWN * 1.025, stroke_color=WHITE, stroke_width=1.0, stroke_opacity=0.4, dash_length=0.08)
        centerlines = VGroup(centerline_h1, centerline_h2, centerline_v1, centerline_v2)

        # Solid white stop lines at the intersection entrances
        stop_line_left = Line(C + LEFT * 0.35 + UP * 0.3, C + LEFT * 0.35 + DOWN * 0.3, stroke_color=WHITE, stroke_width=1.5, stroke_opacity=0.6)
        stop_line_right = Line(C + RIGHT * 0.35 + UP * 0.3, C + RIGHT * 0.35 + DOWN * 0.3, stroke_color=WHITE, stroke_width=1.5, stroke_opacity=0.6)
        stop_lines = VGroup(stop_line_left, stop_line_right)

        crosswalk = VGroup()
        for i in range(5):
            stripe = Rectangle(
                width=0.05,
                height=0.52,
                fill_color=WHITE,
                fill_opacity=0.85,
                stroke_width=0,
            )
            stripe.move_to(C + LEFT * 0.18 + RIGHT * i * 0.09)
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
            block.move_to(C + RIGHT * dx + UP * dy)
            blocks.add(block)

        city = VGroup(city_bg, roads, centerlines, stop_lines, crosswalk, blocks)

        sim_robot = self.robot_marker(ACCENT_PINK, 0.36)
        sim_robot.move_to(city_bg.get_center() + LEFT * 1.72 + DOWN * 0.19)
        
        p1 = self.person_dot(ACCENT_TEAL)
        p1.move_to(city_bg.get_center() + LEFT * 0.08 + UP * 0.92)

        self.play(
            FadeIn(city),
            run_time=0.8
        )
        self.play(
            FadeIn(sim_robot),
            FadeIn(p1),
            run_time=0.7
        )

        # B2.2: Zombie Sim (19.0 to 23.5s)
        rail_robot = Line(sim_robot.get_center(), city_bg.get_center() + RIGHT * 1.65 + DOWN * 0.19, stroke_color=INK_LIGHT, stroke_width=1.5, stroke_opacity=0.6)
        rail_p1 = Line(p1.get_center(), city_bg.get_center() + LEFT * 0.08 + DOWN * 0.92, stroke_color=INK_LIGHT, stroke_width=1.5, stroke_opacity=0.6)
        
        self.play(
            ShowCreation(rail_robot),
            ShowCreation(rail_p1),
            run_time=0.6
        )

        zombie_label = Text(
            "straight lines · no interaction",
            font=FONT_PRIMARY,
            font_size=18,
            color=RED_ERROR,
        )
        zombie_label.move_to(RIGHT * 3.55 + DOWN * 1.42)

        self.play(
            sim_robot.animate.move_to(city_bg.get_center() + RIGHT * 1.65 + DOWN * 0.19),
            p1.animate.move_to(city_bg.get_center() + LEFT * 0.08 + DOWN * 0.92),
            FadeIn(zombie_label, shift=UP * 0.1),
            run_time=1.8,
            rate_func=linear
        )

        conflict_point = city_bg.get_center() + LEFT * 0.08 + DOWN * 0.19
        sign_box = RoundedRectangle(
            width=1.3,
            height=0.45,
            corner_radius=0.05,
            fill_color=RED_ERROR,
            fill_opacity=1.0,
            stroke_color=RED_ERROR,
            stroke_width=1.0
        )
        sign_text = Text("NO YIELDING", font=FONT_PRIMARY, font_size=13, color=WHITE, weight=BOLD)
        sign_text.move_to(sign_box)
        warning = VGroup(sign_box, sign_text)
        warning.move_to(conflict_point)

        self.play(
            FadeIn(warning, scale=1.2),
            run_time=0.6
        )
        self.wait(1.5)

        # B2.3: Reactive Real Behavior (23.5 to 27.5s)
        self.play(
            FadeOut(warning),
            FadeOut(zombie_label),
            sim_robot.animate.move_to(city_bg.get_center() + LEFT * 1.72 + DOWN * 0.19),
            p1.animate.move_to(city_bg.get_center() + LEFT * 0.08 + UP * 0.92),
            rail_robot.animate.set_opacity(0.15),
            rail_p1.animate.set_opacity(0.15),
            run_time=0.8
        )

        gaze_arc = always_redraw(lambda: self.make_gaze_arc(p1, sim_robot, ACCENT_TEAL))
        
        path_curve = VMobject()
        p_start = city_bg.get_center() + LEFT * 1.72 + DOWN * 0.19
        p_end = city_bg.get_center() + RIGHT * 1.65 + DOWN * 0.19
        path_curve.set_points_as_corners([
            p_start,
            p_start + RIGHT * 0.8,
            p_start + RIGHT * 1.3 + DOWN * 0.12,
            p_end + LEFT * 0.8 + DOWN * 0.12,
            p_end
        ])
        path_curve.make_smooth()
        path_curve.set_stroke(ACCENT_TEAL, width=2, opacity=0.7)

        self.add(gaze_arc)
        self.play(FadeIn(path_curve), run_time=0.4)

        self.play(
            MoveAlongPath(sim_robot, path_curve),
            p1.animate.move_to(city_bg.get_center() + LEFT * 0.08 + UP * 0.35),
            run_time=1.8,
            rate_func=smooth
        )

        badge = Circle(
            radius=0.18,
            fill_color="#2ECC71",
            fill_opacity=1.0,
            stroke_color="#2ECC71",
            stroke_width=1.0
        )
        check = Text("✓", font=FONT_PRIMARY, font_size=16, color=WHITE, weight=BOLD)
        check.move_to(badge)
        check_mark = VGroup(badge, check)
        check_mark.move_to(city_bg.get_center() + LEFT * 0.08 + DOWN * 0.19)
        self.play(FadeIn(check_mark, scale=1.3), run_time=0.4)
        self.wait(0.6)

        self.play(
            FadeOut(check_mark),
            FadeOut(path_curve),
            FadeOut(gaze_arc),
            run_time=0.4
        )
        self.remove(gaze_arc)

        # B2.4: Intent Prediction Failure (27.5 to 30.5s)
        self.play(
            sim_robot.animate.move_to(city_bg.get_center() + LEFT * 0.6 + DOWN * 0.19),
            p1.animate.move_to(city_bg.get_center() + LEFT * 0.08 + UP * 0.5),
            run_time=0.5
        )

        cone = Polygon(
            sim_robot.get_center(),
            sim_robot.get_center() + RIGHT * 1.2 + UP * 0.6,
            sim_robot.get_center() + RIGHT * 1.2 + DOWN * 0.6,
            fill_color=ACCENT_AMBER,
            fill_opacity=0.15,
            stroke_width=0
        )
        
        pred_arrow = DashedLine(
            p1.get_center(),
            p1.get_center() + DOWN * 0.6,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.5
        )
        pred_label = Text("predicts straight line", font=FONT_PRIMARY, font_size=14, color=ACCENT_AMBER, weight=BOLD)
        pred_label.next_to(pred_arrow, RIGHT, buff=0.08)

        self.play(
            FadeIn(cone),
            ShowCreation(pred_arrow),
            FadeIn(pred_label),
            run_time=0.5
        )

        divergent_path = Line(p1.get_center(), city_bg.get_center() + RIGHT * 0.35 + DOWN * 0.19, stroke_color=ACCENT_PINK, stroke_width=2.0)
        self.play(
            ShowCreation(divergent_path),
            p1.animate.move_to(city_bg.get_center() + RIGHT * 0.35 + DOWN * 0.19),
            sim_robot.animate.move_to(city_bg.get_center() + RIGHT * 0.1 + DOWN * 0.19),
            run_time=1.0,
            rate_func=smooth
        )

        near_miss_flash = self.make_warn_stamp(city_bg.get_center() + RIGHT * 0.25 + DOWN * 0.19, RED_ERROR)
        self.play(
            FadeIn(near_miss_flash, scale=1.3),
            run_time=0.4
        )
        self.wait(0.6)

        # B2.5: Pedestrian Splay (30.5 to 32.0s)
        self.play(
            FadeOut(cone),
            FadeOut(pred_arrow),
            FadeOut(pred_label),
            FadeOut(divergent_path),
            FadeOut(near_miss_flash),
            run_time=0.4
        )

        splay_lines = VGroup(
            DashedLine(p1.get_center(), p1.get_center() + RIGHT * 0.6 + UP * 0.4, stroke_color=ACCENT_TEAL, stroke_width=1.2),
            DashedLine(p1.get_center(), p1.get_center() + RIGHT * 0.8 + DOWN * 0.1, stroke_color=ACCENT_AMBER, stroke_width=1.2),
            DashedLine(p1.get_center(), p1.get_center() + RIGHT * 0.5 + DOWN * 0.5, stroke_color=ACCENT_PINK, stroke_width=1.2),
            DashedLine(p1.get_center(), p1.get_center() + UP * 0.5 + LEFT * 0.2, stroke_color=ACCENT_BLUE, stroke_width=1.2)
        )
        b2_conclusion = Text(
            "Safety needs human behavior.",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=RED_ERROR,
        )
        b2_conclusion.move_to(RIGHT * 3.55 + DOWN * 1.88)

        self.play(
            ShowCreation(splay_lines),
            FadeIn(b2_conclusion, shift=UP * 0.1),
            run_time=0.8
        )
        self.wait(0.3)

        # ----------------------------------------------------
        # OUTRO SEQUENCE (32-35s)
        # ----------------------------------------------------
        b2_group = VGroup(city, sim_robot, p1, splay_lines, rail_robot, rail_p1)
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
            b2_group.animate.set_opacity(0.18),
            ShowCreation(bottom_rule),
            FadeIn(bottom_text, shift=UP * 0.1),
            run_time=0.8
        )
        self.wait(2.2)
        self._close()
