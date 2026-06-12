"""P04-S06: a V2X frame races against its real-time latency deadline."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, PASTEL_BLUE, PASTEL_AMBER, PASTEL_TEAL,
    RED_ERROR, ACCENT_AMBER, ACCENT_BLUE, ACCENT_TEAL, CYAN_RADAR,
    INK_DARK, INK_MID, LINE_GRID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon, rsu_icon,
)

SCRIPT = (
    "A V2X frame is a chain: local perception, communication, and fusion. "
    "An illustrative edge pipeline can take 170 milliseconds, missing a "
    "100 millisecond real-time budget by 70 milliseconds."
)


def label(text, size=SIZE_LABEL, color=INK_DARK, weight=NORMAL):
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def local_perception_visual():
    road = RoundedRectangle(width=2.45, height=0.82, corner_radius=0.08)
    road.set_fill("#E8EDF2", opacity=0.92)
    road.set_stroke(LINE_GRID, width=1.2, opacity=1.0)
    road.move_to(ORIGIN)

    lane = DashedLine(LEFT * 1.05, RIGHT * 1.05, dash_length=0.14)
    lane.set_stroke(WHITE, width=2.0, opacity=0.95)
    lane.move_to(road)

    car = vehicle_icon(color=ACCENT_BLUE, scale=0.56)
    car.move_to(road.get_center() + LEFT * 0.35)

    targets = VGroup()
    rays = VGroup()
    for offset in [UP * 0.3 + RIGHT * 0.8, RIGHT * 0.95, DOWN * 0.3 + RIGHT * 0.8]:
        target = Dot(radius=0.055)
        target.set_fill(ACCENT_AMBER, opacity=1.0)
        target.set_stroke(ACCENT_AMBER, width=0)
        target.move_to(road.get_center() + offset)
        ray = Line(car.get_right(), target.get_center())
        ray.set_stroke(CYAN_RADAR, width=1.3, opacity=0.65)
        targets.add(target)
        rays.add(ray)

    return VGroup(road, lane, rays, targets, car)


def communication_visual():
    car = vehicle_icon(color=ACCENT_BLUE, scale=0.48)
    car.move_to(LEFT * 0.82 + DOWN * 0.18)
    rsu = rsu_icon(color=ACCENT_AMBER)
    rsu.scale(1.35)
    rsu.move_to(RIGHT * 0.82 + UP * 0.08)

    link = DashedLine(car.get_right(), rsu.get_left(), dash_length=0.1)
    link.set_stroke(ACCENT_TEAL, width=2.0, opacity=0.55)

    packets = VGroup()
    for alpha, color in zip([0.28, 0.5, 0.72], [ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER]):
        packet = Square(side_length=0.14)
        packet.set_fill(color, opacity=1.0)
        packet.set_stroke(color, width=0)
        packet.move_to(link.point_from_proportion(alpha))
        packets.add(packet)

    return VGroup(car, link, packets, rsu), packets, link


def fusion_visual():
    grid = VGroup()
    cell = 0.31
    rows, cols = 4, 6
    for row in range(rows):
        for col in range(cols):
            square = Square(side_length=cell)
            square.set_fill(PASTEL_TEAL, opacity=0.2)
            square.set_stroke(ACCENT_TEAL, width=0.8, opacity=0.38)
            square.move_to([
                (col - (cols - 1) / 2) * cell,
                (row - (rows - 1) / 2) * cell,
                0,
            ])
            grid.add(square)

    car_a = vehicle_icon(color=ACCENT_BLUE, scale=0.3)
    car_b = vehicle_icon(color=ACCENT_AMBER, scale=0.3)
    car_a.move_to(grid.get_center() + LEFT * 0.43 + DOWN * 0.18)
    car_b.rotate(PI / 2)
    car_b.move_to(grid.get_center() + RIGHT * 0.46 + UP * 0.16)

    fused = RoundedRectangle(width=1.3, height=0.72, corner_radius=0.12)
    fused.set_fill(ACCENT_TEAL, opacity=0.08)
    fused.set_stroke(ACCENT_TEAL, width=2.0, opacity=0.85)
    fused.move_to(grid)

    return VGroup(grid, fused, car_a, car_b)


def stage_heading(number, title, subtitle, color):
    number_dot = Circle(radius=0.16)
    number_dot.set_fill(color, opacity=1.0)
    number_dot.set_stroke(color, width=0)
    number_text = label(str(number), SIZE_CAPS - 1, WHITE, BOLD)
    number_text.move_to(number_dot)

    title_text = label(title, SIZE_LABEL, INK_DARK, BOLD)
    subtitle_text = label(subtitle, SIZE_CAPS - 1, INK_MID)
    copy = VGroup(title_text, subtitle_text)
    copy.arrange(DOWN, aligned_edge=LEFT, buff=0.04)

    heading = VGroup(VGroup(number_dot, number_text), copy)
    heading.arrange(RIGHT, buff=0.12)
    return heading


class P04S06LatencyChain(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "V2X Latency Budget"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # Fixed real-time deadline, visible before any work starts.
        timeline_left = -5.75
        timeline_right = 5.75
        timeline_y = -1.55
        total_ms = 170
        deadline_ms = 100

        def time_x(milliseconds):
            return timeline_left + milliseconds / total_ms * (timeline_right - timeline_left)

        baseline = Line(
            [timeline_left, timeline_y, 0],
            [timeline_right, timeline_y, 0],
        )
        baseline.set_stroke(INK_MID, width=2.0, opacity=0.6)

        deadline_x = time_x(deadline_ms)
        deadline = DashedLine(
            [deadline_x, timeline_y - 0.72, 0],
            [deadline_x, timeline_y + 0.72, 0],
            dash_length=0.12,
        )
        deadline.set_stroke(RED_ERROR, width=2.2, opacity=0.75)
        deadline_pill = RoundedRectangle(width=1.78, height=0.44, corner_radius=0.12)
        deadline_pill.set_fill("#FEE2E2", opacity=1.0)
        deadline_pill.set_stroke(RED_ERROR, width=1.4, opacity=0.9)
        deadline_text = label("100 ms deadline", SIZE_CAPS, RED_ERROR, BOLD)
        deadline_text.move_to(deadline_pill)
        deadline_group = VGroup(deadline_pill, deadline_text)
        deadline_group.move_to([deadline_x, timeline_y + 0.9, 0])

        self.play(
            ShowCreation(baseline),
            ShowCreation(deadline),
            FadeIn(deadline_group, shift=0.08 * DOWN),
            run_time=0.65,
        )

        # Three concrete processing views.
        local = local_perception_visual()
        comm, packets, link = communication_visual()
        fusion = fusion_visual()
        local.move_to(LEFT * 4.15 + UP * 0.65)
        comm.move_to(ORIGIN + UP * 0.65)
        fusion.move_to(RIGHT * 4.15 + UP * 0.65)

        headings = VGroup(
            stage_heading(1, "LOCAL PERCEPTION", "sensor  \u2192  BEV", ACCENT_BLUE),
            stage_heading(2, "V2X UPLINK", "share features", ACCENT_TEAL),
            stage_heading(3, "FUSION", "multi-agent BEV", ACCENT_AMBER),
        )
        for heading, center_x in zip(headings, [-4.15, 0.0, 4.15]):
            heading.move_to([center_x, 1.8, 0])

        flow_arrows = VGroup(
            Arrow(
                [-2.72, 0.66, 0],
                [-1.48, 0.66, 0],
                buff=0,
                max_tip_length_to_length_ratio=0.12,
            ),
            Arrow(
                [1.48, 0.66, 0],
                [2.72, 0.66, 0],
                buff=0,
                max_tip_length_to_length_ratio=0.12,
            ),
        )
        flow_arrows.set_stroke(INK_MID, width=2.0, opacity=0.72)
        flow_arrows.set_fill(INK_MID, opacity=0.72)

        # Timeline segments use the reviewed illustrative budget: 80 + 50 + 40 ms.
        stage_data = [
            (0, 80, ACCENT_BLUE, PASTEL_BLUE, "80 ms"),
            (80, 130, ACCENT_TEAL, PASTEL_TEAL, "50 ms"),
            (130, 170, ACCENT_AMBER, PASTEL_AMBER, "40 ms"),
        ]
        segments = VGroup()
        duration_labels = VGroup()
        for start_ms, end_ms, color, fill, duration in stage_data:
            width = time_x(end_ms) - time_x(start_ms)
            segment = Rectangle(width=width, height=0.48)
            segment.set_fill(fill, opacity=0.9)
            segment.set_stroke(color, width=2.0, opacity=0.95)
            segment.move_to([
                (time_x(start_ms) + time_x(end_ms)) / 2,
                timeline_y,
                0,
            ])
            segments.add(segment)

            duration_text = label(duration, SIZE_CAPS, color, BOLD)
            duration_text.next_to(segment, DOWN, buff=0.14)
            duration_labels.add(duration_text)

        cursor = Triangle()
        cursor.set_fill(INK_DARK, opacity=1.0)
        cursor.set_stroke(INK_DARK, width=0)
        cursor.scale(0.1)
        cursor.rotate(-PI / 2)
        cursor.move_to([timeline_left, timeline_y + 0.48, 0])

        # Stage 1.
        self.play(
            FadeIn(headings[0], shift=0.12 * DOWN),
            FadeIn(local),
            FadeIn(cursor),
            run_time=0.55,
        )
        self.play(
            GrowFromEdge(segments[0], LEFT),
            cursor.animate.move_to([time_x(80), timeline_y + 0.48, 0]),
            run_time=1.15,
            rate_func=linear,
        )
        self.play(FadeIn(duration_labels[0]), ShowCreation(flow_arrows[0]), run_time=0.35)

        # Stage 2, including visible feature packets.
        self.play(
            FadeIn(headings[1], shift=0.12 * DOWN),
            FadeIn(comm[0]),
            ShowCreation(link),
            FadeIn(comm[3]),
            run_time=0.55,
        )
        packet_targets = [
            link.point_from_proportion(0.54),
            link.point_from_proportion(0.72),
            link.point_from_proportion(0.9),
        ]
        self.play(
            GrowFromEdge(segments[1], LEFT),
            cursor.animate.move_to([time_x(130), timeline_y + 0.48, 0]),
            *(
                packet.animate.move_to(target)
                for packet, target in zip(packets, packet_targets)
            ),
            run_time=1.0,
            rate_func=linear,
        )
        self.play(
            FadeIn(duration_labels[1]),
            Flash(deadline_group, color=RED_ERROR, line_length=0.18, num_lines=8),
            run_time=0.45,
        )
        self.play(ShowCreation(flow_arrows[1]), run_time=0.3)

        # Stage 3 starts only after the deadline has already passed.
        self.play(
            FadeIn(headings[2], shift=0.12 * DOWN),
            LaggedStart(
                *(FadeIn(cell, scale=0.75) for cell in fusion[0]),
                lag_ratio=0.025,
                run_time=0.7,
            ),
            FadeIn(VGroup(*fusion[1:])),
        )
        self.play(
            GrowFromEdge(segments[2], LEFT),
            cursor.animate.move_to([time_x(170), timeline_y + 0.48, 0]),
            run_time=0.8,
            rate_func=linear,
        )
        self.play(FadeIn(duration_labels[2]), run_time=0.25)

        # Make the missed deadline visceral without another decorative card.
        overflow = Rectangle(
            width=timeline_right - deadline_x,
            height=0.48,
        )
        overflow.set_fill(RED_ERROR, opacity=0.22)
        overflow.set_stroke(RED_ERROR, width=0)
        overflow.move_to([
            (deadline_x + timeline_right) / 2,
            timeline_y,
            0,
        ])

        bracket_y = timeline_y - 0.9
        bracket = VGroup(
            Line([deadline_x, bracket_y, 0], [timeline_right, bracket_y, 0]),
            Line([deadline_x, bracket_y - 0.12, 0], [deadline_x, bracket_y + 0.12, 0]),
            Line([timeline_right, bracket_y - 0.12, 0], [timeline_right, bracket_y + 0.12, 0]),
        )
        bracket.set_stroke(RED_ERROR, width=2.2, opacity=0.9)
        late_text = label("+70 ms late", SIZE_LABEL, RED_ERROR, BOLD)
        late_text.next_to(bracket, DOWN, buff=0.08)

        total_text = VGroup(
            label("Pipeline", SIZE_CAPS, INK_MID),
            label("170 ms", SIZE_LABEL + 5, RED_ERROR, BOLD),
            label(">", SIZE_LABEL, INK_MID, BOLD),
            label("100 ms budget", SIZE_LABEL, INK_DARK, BOLD),
        )
        total_text.arrange(RIGHT, buff=0.13)
        total_text.move_to([0, -3.15, 0])

        self.play(
            FadeIn(overflow),
            ShowCreation(bracket),
            FadeIn(late_text, shift=0.08 * UP),
            run_time=0.55,
        )
        self.play(FadeIn(total_text, shift=0.1 * UP), run_time=0.45)
        self.wait(1.5)
        self._close()
