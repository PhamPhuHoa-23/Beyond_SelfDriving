"""P04-S04 CooPre masked voxel pretraining and data-efficiency result."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, CYAN_RADAR,
    GOLD_RICH, GOLD_KEY, GREEN_FIX, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon, contribution_badge,
)

SCRIPT = (
    "CooPre masks forty percent of voxels and reconstructs them from cooperative "
    "context. With half the labels it reaches the full-data baseline, and with "
    "all labels it gains another four and a half AP points."
)


def text_label(text, size=SIZE_LABEL, color=INK_DARK, weight=NORMAL):
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def bev_grid(rows=8, cols=8, cell=0.5, color=ACCENT_BLUE):
    """Build a compact BEV voxel grid."""
    grid = VGroup()
    for r in range(rows):
        for c in range(cols):
            cell_sq = Square(side_length=cell)
            cell_sq.set_fill(color, opacity=0.28)
            cell_sq.set_stroke(color, width=1.2, opacity=0.6)
            cell_sq.move_to(np.array([
                (c - cols / 2 + 0.5) * cell,
                (r - rows / 2 + 0.5) * cell,
                0,
            ]))
            grid.add(cell_sq)
    return grid


def result_chart():
    """CooPre results reproduced from materials/images/part4/p4_s14_slide_023.png."""
    percentages = [20, 50, 80, 100]
    baseline = [0.309, 0.433, 0.478, 0.486]
    coopre = [0.409, 0.501, 0.519, 0.531]

    x_left = -5.9
    x_right = 1.6
    y_bottom = -2.15
    y_top = 1.55
    y_max = 0.60

    def y_pos(value):
        return y_bottom + value / y_max * (y_top - y_bottom)

    chart = VGroup()
    axes = VGroup(
        Line([x_left, y_bottom, 0], [x_right, y_bottom, 0]),
        Line([x_left, y_bottom, 0], [x_left, y_top, 0]),
    )
    axes.set_stroke(INK_DARK, width=2.0, opacity=0.9)
    chart.add(axes)

    for tick in [0.3, 0.4, 0.5, 0.6]:
        y = y_pos(tick)
        guide = Line([x_left, y, 0], [x_right, y, 0])
        guide.set_stroke(INK_MID, width=1.0, opacity=0.22)
        tick_label = text_label(f"{tick:.1f}", SIZE_CAPS - 2, INK_MID)
        tick_label.next_to([x_left, y, 0], LEFT, buff=0.12)
        chart.add(guide, tick_label)

    threshold = DashedLine(
        [x_left, y_pos(0.5), 0],
        [x_right, y_pos(0.5), 0],
        dash_length=0.12,
    )
    threshold.set_stroke(GOLD_RICH, width=2.2, opacity=0.8)
    chart.add(threshold)

    group_x = [-4.75, -2.95, -1.15, 0.65]
    bar_width = 0.48
    bars = VGroup()
    value_labels = VGroup()
    x_labels = VGroup()

    for x, pct, base_value, coopre_value in zip(group_x, percentages, baseline, coopre):
        for dx, value, color in [
            (-bar_width / 2, base_value, INK_MID),
            (bar_width / 2, coopre_value, ACCENT_TEAL),
        ]:
            height = y_pos(value) - y_bottom
            bar = Rectangle(width=bar_width, height=height)
            bar.set_fill(color, opacity=0.92)
            bar.set_stroke(color, width=1.0, opacity=1.0)
            bar.move_to([x + dx, y_bottom + height / 2, 0])
            bars.add(bar)

            value_label = text_label(f"{value:.3f}", SIZE_CAPS - 2, color, BOLD)
            value_label.next_to(bar, UP, buff=0.07)
            value_labels.add(value_label)

        pct_label = text_label(f"{pct}%", SIZE_CAPS, INK_DARK, BOLD)
        pct_label.move_to([x, y_bottom - 0.28, 0])
        x_labels.add(pct_label)

    axis_label = text_label("Labeled training data", SIZE_CAPS, INK_MID)
    axis_label.move_to([(x_left + x_right) / 2, y_bottom - 0.7, 0])

    legend_base = Square(side_length=0.17)
    legend_base.set_fill(INK_MID, opacity=0.92).set_stroke(width=0)
    legend_coopre = Square(side_length=0.17)
    legend_coopre.set_fill(ACCENT_TEAL, opacity=0.92).set_stroke(width=0)
    legend = VGroup(
        legend_base,
        text_label("Scratch", SIZE_CAPS - 1, INK_MID),
        legend_coopre,
        text_label("CooPre", SIZE_CAPS - 1, ACCENT_TEAL, BOLD),
    )
    legend.arrange(RIGHT, buff=0.12)
    legend.move_to([-3.85, 1.9, 0])

    chart_title = text_label("V2X-Real  |  mAP@0.5", SIZE_LABEL, INK_DARK, BOLD)
    chart_title.move_to([-2.15, 2.32, 0])

    chart.add(bars, value_labels, x_labels, axis_label, legend, chart_title)
    return chart, bars, value_labels


class P04S04CooPReMasked(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "CooPre: Masked Voxel Puzzle"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # Beat 1: mask BEV voxels and reconstruct them from another agent.
        grid = bev_grid(rows=8, cols=8, cell=0.48, color=ACCENT_BLUE)
        grid.move_to(DOWN * 0.25)
        self.play(LaggedStart(
            *(FadeIn(voxel, scale=0.6) for voxel in grid),
            lag_ratio=0.008,
            run_time=1.0,
        ))

        agent_a = vehicle_icon(color=ACCENT_BLUE, scale=0.74)
        agent_b = vehicle_icon(color=ACCENT_TEAL, scale=0.74)
        agent_a.move_to(grid.get_corner(UL) + np.array([-0.32, 0.32, 0]))
        agent_b.move_to(grid.get_corner(DR) + np.array([0.32, -0.32, 0]))
        self.play(GrowFromCenter(agent_a), GrowFromCenter(agent_b), run_time=0.5)

        beam_a = Line(agent_a.get_center(), grid.get_center())
        beam_a.set_stroke(CYAN_RADAR, width=1.5, opacity=0.55)
        beam_b = Line(agent_b.get_center(), grid.get_center())
        beam_b.set_stroke(ACCENT_TEAL, width=1.5, opacity=0.55)
        self.play(ShowCreation(beam_a), ShowCreation(beam_b), run_time=0.5)

        rng = np.random.RandomState(17)
        mask_indices = sorted(
            rng.choice(len(grid), int(len(grid) * 0.4), replace=False).tolist()
        )
        mask_caption = text_label(
            "40% hidden  ->  reconstruct from cooperative context",
            SIZE_LABEL,
            INK_DARK,
            BOLD,
        )
        mask_caption.to_edge(DOWN, buff=0.38)
        self.play(
            LaggedStart(
                *(
                    grid[i].animate
                    .set_fill(opacity=0.05)
                    .set_stroke(opacity=0.18)
                    for i in mask_indices
                ),
                lag_ratio=0.025,
                run_time=1.1,
            ),
            FadeIn(mask_caption),
        )

        packets = VGroup()
        packet_anims = []
        for idx in mask_indices[:18]:
            voxel = grid[idx]
            start = agent_b.get_center()
            midpoint = (start + voxel.get_center()) / 2 + np.array([
                rng.uniform(-0.25, 0.25),
                rng.uniform(0.15, 0.4),
                0,
            ])
            packet = Dot(radius=0.055)
            packet.set_fill(ACCENT_TEAL, opacity=1.0)
            packet.set_stroke(ACCENT_TEAL, width=0.8, opacity=1.0)
            packet.move_to(start)
            packets.add(packet)
            path = CubicBezier(start, midpoint, midpoint, voxel.get_center())
            packet_anims.append(MoveAlongPath(packet, path, rate_func=smooth))

        self.play(LaggedStart(*packet_anims, lag_ratio=0.045, run_time=2.0))
        self.play(
            LaggedStart(
                *(
                    grid[i].animate.set_fill(opacity=0.75).set_stroke(opacity=0.9)
                    for i in mask_indices
                ),
                lag_ratio=0.018,
                run_time=1.0,
            ),
            FadeOut(packets),
        )
        self.wait(0.35)

        # Beat 2: show the exact data-efficiency results from the source slide.
        self.play(
            FadeOut(grid),
            FadeOut(agent_a),
            FadeOut(agent_b),
            FadeOut(beam_a),
            FadeOut(beam_b),
            FadeOut(mask_caption),
            run_time=0.55,
        )

        chart, bars, value_labels = result_chart()
        static_chart = VGroup(*[
            mob for mob in chart.submobjects
            if mob is not bars and mob is not value_labels
        ])
        self.play(FadeIn(static_chart), run_time=0.65)
        self.play(
            LaggedStart(
                *(GrowFromEdge(bar, DOWN) for bar in bars),
                lag_ratio=0.08,
                run_time=1.5,
            )
        )
        self.play(
            LaggedStart(
                *(FadeIn(label, shift=0.08 * UP) for label in value_labels),
                lag_ratio=0.05,
                run_time=0.7,
            )
        )

        result_50 = VGroup(
            text_label("50% labels", SIZE_LABEL, ACCENT_TEAL, BOLD),
            text_label("0.501 mAP", SIZE_LABEL + 4, INK_DARK, BOLD),
            text_label("> scratch at 100%: 0.486", SIZE_CAPS, INK_MID),
        )
        result_50.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        result_100 = VGroup(
            text_label("100% labels", SIZE_LABEL, GOLD_RICH, BOLD),
            text_label("0.531 mAP", SIZE_LABEL + 4, INK_DARK, BOLD),
            text_label("+0.045 mAP over scratch", SIZE_CAPS, INK_MID),
        )
        result_100.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        insights = VGroup(result_50, result_100)
        insights.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        insights.move_to(RIGHT * 4.35 + DOWN * 0.05)
        self.play(
            LaggedStart(
                FadeIn(result_50, shift=0.18 * LEFT),
                FadeIn(result_100, shift=0.18 * LEFT),
                lag_ratio=0.35,
                run_time=1.0,
            )
        )
        self.play(
            Flash(result_100[1], color=GOLD_RICH, line_length=0.22, num_lines=8),
            run_time=0.7,
        )

        badges = VGroup(
            contribution_badge("IROS 2025  |  UCLA DriveX", color=GOLD_KEY),
            contribution_badge("CVPR 2025 Workshop", color=ACCENT_BLUE),
        )
        badges.arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.25)
        self.play(LaggedStart(*(FadeIn(b) for b in badges), lag_ratio=0.15), run_time=0.6)
        self.wait(1.5)
        self._close()
