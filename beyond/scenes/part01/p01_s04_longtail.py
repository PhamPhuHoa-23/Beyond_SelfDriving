# beyond/scenes/part01/p01_s04_longtail.py
# ─────────────────────────────────────────────────────────────────
# P1-04  LONG-TAIL — CẢNH ĐẸP NHẤT PART 1  (~65s)
#
# Không có title slide. Cảnh bắt đầu trực tiếp bằng 3 icon kỳ lạ.
# Power-law curve với glowing head trace.
# 3 edge cases "đậu lên đuôi" như bọ kỳ dị.
# Rack focus vào đuôi. Key insight dim-overlay.
#
# Render:  manim -ql "beyond/scenes/part01/p01_s04_longtail.py" P01S04LongTail
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    axes_deploy, key_insight_reveal,
    glow_pulse,
    BG_SPACE, BG_PANEL,
    GOLD, CYAN_NEON, P1_FOUNDATION,
    RED_ALERT, RED_DIM, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_BODY, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=42)


# ── Edge case icon builders ───────────────────────────────────────

def _icon_person_on_road() -> VGroup:
    """Person standing in lane, holding phone, question mark above."""
    body  = Circle(radius=0.16, fill_color="#E8A838", fill_opacity=1,
                   stroke_color=RED_ALERT, stroke_width=1.5)
    torso = Rectangle(width=0.18, height=0.26, fill_color="#E8A838",
                      fill_opacity=1, stroke_width=0)
    torso.next_to(body, DOWN, buff=0.04)
    # Road stripes
    stripe1 = Rectangle(width=0.65, height=0.06, fill_color=TEXT_GHOST,
                        fill_opacity=1, stroke_width=0).shift(DOWN * 0.48)
    stripe2 = stripe1.copy().shift(RIGHT * 0.3)
    # Phone (small rectangle)
    phone = Rectangle(width=0.08, height=0.13, fill_color=CYAN_NEON,
                      fill_opacity=0.9, stroke_width=0)
    phone.next_to(torso, RIGHT, buff=0.05)
    # Question mark — flashing
    qmark = Text("?", font_size=18, color=RED_ALERT,
                 font=FONT_PRIMARY, weight=BOLD)
    qmark.next_to(body, UP, buff=0.08)

    grp = VGroup(stripe1, stripe2, torso, body, phone, qmark)
    return grp


def _icon_traffic_light_truck() -> VGroup:
    """Truck with 3 upside-down traffic lights on top."""
    # Truck body
    truck = Rectangle(width=0.55, height=0.30,
                      fill_color=TEXT_DIM, fill_opacity=1,
                      stroke_color=TEXT_GHOST, stroke_width=1.2)
    cab = Rectangle(width=0.18, height=0.26,
                    fill_color=TEXT_DIM, fill_opacity=1,
                    stroke_color=TEXT_GHOST, stroke_width=1.2)
    cab.align_to(truck, RIGHT).shift(UP * 0.10)
    # Wheels
    wl = Circle(radius=0.07, fill_color="#1A1A1A", fill_opacity=1,
                stroke_width=0).move_to(truck.get_bottom() + LEFT * 0.15)
    wr = wl.copy().move_to(truck.get_bottom() + RIGHT * 0.15)
    # 3 upside-down traffic light circles ON TOP
    light_colors = ["#FF1744", "#FF6D00", "#00E676"]
    lights = VGroup(*[
        Circle(radius=0.055, fill_color=c, fill_opacity=0.9, stroke_width=0)
        for c in light_colors
    ]).arrange(RIGHT, buff=0.06)
    lights.next_to(truck, UP, buff=0.04)
    # AI scan lines — 3 horizontal lines scanning over truck
    scan_lines = VGroup(*[
        Line(truck.get_left() + LEFT * 0.1,
             truck.get_right() + RIGHT * 0.1,
             stroke_color=CYAN_NEON, stroke_width=0.5,
             stroke_opacity=0.6).shift(UP * (0.08 * i - 0.08))
        for i in range(3)
    ])

    grp = VGroup(truck, cab, wl, wr, lights, scan_lines)
    return grp


def _icon_snow_road() -> VGroup:
    """Snow-covered road. Lane detection going haywire."""
    road = Rectangle(width=0.7, height=0.38,
                     fill_color="#2A3550", fill_opacity=1,
                     stroke_color=TEXT_GHOST, stroke_width=1.0)
    # Snow dots
    snow_dots = VGroup(*[
        Dot(radius=RNG.uniform(0.02, 0.045), color=WHITE, fill_opacity=0.8)
        .move_to(road.get_center()
                 + RIGHT * RNG.uniform(-0.28, 0.28)
                 + UP * RNG.uniform(-0.14, 0.14))
        for _ in range(22)
    ])
    # Crazy lane detection — dashed lines going wrong angles
    bad_lane1 = DashedLine(
        road.get_bottom() + LEFT * 0.12,
        road.get_top() + RIGHT * 0.28,
        color=GOLD, stroke_width=1.0, dash_length=0.06
    )
    bad_lane2 = DashedLine(
        road.get_bottom() + RIGHT * 0.15,
        road.get_top() + LEFT * 0.20,
        color=GOLD, stroke_width=1.0, dash_length=0.06
    )
    grp = VGroup(road, snow_dots, bad_lane1, bad_lane2)
    return grp


# ── Scene ─────────────────────────────────────────────────────────

class P01S04LongTail(BeyondScene):
    PART_COLOR = P1_FOUNDATION

    def construct(self):
        # ── [0s] THREE EDGE CASE ICONS appear first — no title ──
        icon1 = _icon_person_on_road().scale(0.9).move_to(LEFT * 5.0 + UP * 1.8)
        icon2 = _icon_traffic_light_truck().scale(0.9).move_to(RIGHT * 5.0 + UP * 1.8)
        icon3 = _icon_snow_road().scale(0.9).move_to(UP * 0.0 + DOWN * 2.2)

        # Labels appear AFTER icons settle
        lbl1 = Text("Person in lane?", font_size=SIZE_MICRO,
                    color=RED_ALERT, font=FONT_PRIMARY)
        lbl1.next_to(icon1, DOWN, buff=0.12)
        lbl2 = Text("AI doesn't recognize\nthis as traffic light",
                    font_size=SIZE_MICRO, color=RED_ALERT,
                    font=FONT_PRIMARY, line_spacing=0.35)
        lbl2.next_to(icon2, DOWN, buff=0.12)
        lbl3 = Text("Lane detection\nfailure in snow",
                    font_size=SIZE_MICRO, color=RED_ALERT,
                    font=FONT_PRIMARY, line_spacing=0.35)
        lbl3.next_to(icon3, DOWN, buff=0.12)

        self.play(
            LaggedStart(
                GrowFromCenter(icon1, run_time=0.45),
                GrowFromCenter(icon2, run_time=0.45),
                GrowFromCenter(icon3, run_time=0.45),
                lag_ratio=0.25,
            )
        )
        self.play(
            LaggedStart(
                FadeIn(lbl1, shift=UP * 0.06, run_time=0.28),
                FadeIn(lbl2, shift=UP * 0.06, run_time=0.28),
                FadeIn(lbl3, shift=UP * 0.06, run_time=0.28),
                lag_ratio=0.2,
            )
        )
        self.wait(0.8)

        # ── Slide icons to corners — pre-compute target positions ─
        # Compute where each icon+label will land BEFORE animating
        def _corner_targets(icon, lbl, corner, lbl_direction, scale=0.65, lbl_scale=0.75):
            ghost_icon = icon.copy().scale(scale)
            ghost_icon.to_corner(corner, buff=0.5)
            ghost_lbl  = lbl.copy().scale(lbl_scale)
            ghost_lbl.next_to(ghost_icon, lbl_direction, buff=0.07)
            return ghost_icon.get_center(), ghost_lbl.get_center()

        i1c, l1c = _corner_targets(icon1, lbl1, UL, DOWN)
        i2c, l2c = _corner_targets(icon2, lbl2, UR, DOWN)
        i3c, l3c = _corner_targets(icon3, lbl3, DR, UP)

        self.play(
            icon1.animate(run_time=0.6, rate_func=smooth).scale(0.65).move_to(i1c),
            lbl1.animate(run_time=0.6, rate_func=smooth).scale(0.75).move_to(l1c),
            icon2.animate(run_time=0.6, rate_func=smooth).scale(0.65).move_to(i2c),
            lbl2.animate(run_time=0.6, rate_func=smooth).scale(0.75).move_to(l2c),
            icon3.animate(run_time=0.6, rate_func=smooth).scale(0.65).move_to(i3c),
            lbl3.animate(run_time=0.6, rate_func=smooth).scale(0.75).move_to(l3c),
        )
        self.wait(0.2)

        # ── POWER-LAW AXES (deployed first — RULE U7) ─────────
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 1.1, 0.25],
            x_length=7.2,
            y_length=4.0,
            axis_config={
                "color": TEXT_DIM, "stroke_width": 1.5,
                "include_tip": True, "tip_length": 0.18,
            },
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).shift(LEFT * 1.8 + DOWN * 0.3)

        x_lbl = Text("Scenario frequency rank →", font_size=SIZE_MICRO,
                     color=TEXT_DIM, font=FONT_PRIMARY)
        x_lbl.next_to(axes.x_axis.get_end(), RIGHT, buff=0.08)
        y_lbl = Text("Frequency", font_size=SIZE_MICRO,
                     color=TEXT_DIM, font=FONT_PRIMARY).rotate(PI / 2)
        y_lbl.next_to(axes.y_axis.get_end(), LEFT, buff=0.10)

        self.play(axes_deploy(axes, "", ""))
        self.play(
            FadeIn(x_lbl, shift=RIGHT * 0.06, run_time=0.22),
            FadeIn(y_lbl, shift=UP * 0.06, run_time=0.22),
        )

        # ── Power-law curve ────────────────────────────────────
        def power_law(x):
            return min(1.0, 1.8 * max(x + 0.5, 0.1) ** (-1.15))

        main_curve = axes.plot(
            power_law, x_range=[0.2, 98],
            color=P1_FOUNDATION, stroke_width=3.0,
        )

        # Glowing head trace
        x_track = ValueTracker(0.2)
        head = Dot(radius=0.08, color=WHITE, fill_opacity=1.0)
        head_trail = TracedPath(head.get_center,
                                stroke_color=P1_FOUNDATION,
                                stroke_width=4.0, dissipating_time=0.3)
        head.move_to(axes.input_to_graph_point(0.2, main_curve))
        head.add_updater(lambda m: m.move_to(
            axes.input_to_graph_point(x_track.get_value(), main_curve)
        ))

        self.add(head, head_trail)
        self.play(
            AnimationGroup(
                x_track.animate(run_time=2.0, rate_func=smooth).set_value(98),
                Create(main_curve, run_time=2.0, rate_func=smooth),
            )
        )
        head.remove_updater(head.get_updaters()[-1])
        self.play(FadeOut(head, run_time=0.18), FadeOut(head_trail, run_time=0.18))

        # ── Fill areas ────────────────────────────────────────
        # Left: common scenarios (tall, blue)
        common_area = axes.get_area(
            main_curve, x_range=[0.2, 15],
            color=P1_FOUNDATION, opacity=0.20,
        )
        # Right: edge cases (long tail, red)
        tail_area = axes.get_area(
            main_curve, x_range=[30, 98],
            color=RED_ALERT, opacity=0.22,
        )
        self.play(
            FadeIn(common_area, run_time=0.4),
            FadeIn(tail_area, run_time=0.5),
        )

        # Area labels
        common_lbl = Text("99% of driving", font_size=SIZE_MICRO + 1,
                          color=P1_FOUNDATION, font=FONT_PRIMARY)
        common_lbl.move_to(axes.c2p(6, 0.55))
        tail_lbl_main = Text("1% of scenarios",
                             font_size=SIZE_MICRO + 1,
                             color=RED_ALERT, font=FONT_PRIMARY)
        tail_lbl_sub = Text("← 100% of accidents",
                            font_size=SIZE_MICRO,
                            color=RED_ALERT, font=FONT_PRIMARY)
        tail_group = VGroup(tail_lbl_main, tail_lbl_sub).arrange(DOWN, buff=0.08)
        tail_group.move_to(axes.c2p(65, 0.40))

        self.play(
            FadeIn(common_lbl, shift=UP * 0.06, run_time=0.3),
            FadeIn(tail_group, shift=UP * 0.06, run_time=0.35),
        )
        self.wait(0.4)

        # ── Tail pulses (danger!) ──────────────────────────────
        self.play(
            tail_area.animate(run_time=0.38).set_fill(opacity=0.48),
            tail_lbl_main.animate(run_time=0.38).scale(1.08),
        )
        self.play(
            tail_area.animate(run_time=0.38).set_fill(opacity=0.22),
            tail_lbl_main.animate(run_time=0.38).scale(1 / 1.08),
        )

        # ── Edge case icons FLY onto the tail area ─────────────
        # Their final positions are over the tail distribution
        tail_pts = [
            axes.c2p(35, power_law(35) + 0.12),
            axes.c2p(58, power_law(58) + 0.12),
            axes.c2p(80, power_law(80) + 0.12),
        ]
        icon_targets = [icon1, icon2, icon3]
        for icon, target_pt in zip(icon_targets, tail_pts):
            self.play(
                icon.animate(run_time=0.45, rate_func=rush_into)
                    .scale(0.5).move_to(target_pt),
                run_time=0.45,
            )

        self.wait(0.5)

        # ── Contextual reasoning text ─────────────────────────
        context_items = [
            "Contextual reasoning.",
            "Common sense.",
            "A lifetime of experience\n with the physical world.",
        ]
        ctx_group = VGroup(*[
            Text(t, font_size=SIZE_LABEL - 1 if i < 2 else SIZE_LABEL - 2,
                 color=TEXT_WHITE if i < 2 else GOLD,
                 font=FONT_PRIMARY,
                 slant=NORMAL if i < 2 else ITALIC,
                 line_spacing=0.4)
            for i, t in enumerate(context_items)
        ]).arrange(DOWN, buff=0.30, aligned_edge=LEFT)
        ctx_group.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)

        self.play(
            LaggedStart(*[
                FadeIn(line, shift=LEFT * 0.08, run_time=0.35)
                for line in ctx_group
            ], lag_ratio=0.28),
        )
        self.wait(0.8)

        # ── KEY INSIGHT ────────────────────────────────────────
        key_insight_reveal(
            self,
            "We need generalist experience\nto handle the long tail.",
            color=GOLD,
            hold=2.5,
        )

        # ── Clean close ───────────────────────────────────────
        self.close()
