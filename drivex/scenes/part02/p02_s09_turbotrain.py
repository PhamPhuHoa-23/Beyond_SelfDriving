"""
Scene 2-09 — TurboTrain: Research Problem 2
============================================
Scatter plot of training runs → TurboTrain pipeline (Pretrain + Balance).
Result: ~45 epochs vs 120 (manual 4-stage).
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P02S09TurboTrain(Scene):
    """
    Part A: Scatter plot (orange failed runs, blue manual 4-stage, gold TurboTrain star).
    Part B: 2-stage pipeline with alternating gradient arrows + result box.
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        # ═══ PART A: Scatter Plot ══════════════════════════════════
        axes = Axes(
            x_range=[0, 1.1, 0.25],
            y_range=[0, 1.1, 0.25],
            x_length=6,
            y_length=4.5,
            axis_config={"color": COL_WHITE, "stroke_width": 1.5,
                         "include_tip": True, "include_numbers": False},
        )
        axes.move_to(LEFT * 2.5 + DOWN * 0.3)
        x_lbl = Text("AP @ 0.5  (Detection)", font_size=13, color=COL_WHITE)
        y_lbl = Text("EPA  (Prediction)", font_size=13, color=COL_WHITE).rotate(PI / 2)
        x_lbl.next_to(axes.x_axis, DOWN, buff=0.25)
        y_lbl.next_to(axes.y_axis, LEFT, buff=0.25)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.6)

        # orange dots — failed one-time runs (low, scattered)
        import random
        random.seed(42)
        orange_pts = [(random.uniform(0.05, 0.35), random.uniform(0.05, 0.35)) for _ in range(8)]
        orange_dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.08, color=COL_GOLD, fill_opacity=0.85)
            for x, y in orange_pts
        ])
        orange_dots.set_color(COL_GOLD).set_color_by_gradient(COL_GOLD, COL_RED)
        # override to orange
        for d in orange_dots:
            d.set_color("#E88C28")

        # blue dots — manual 4-stage (mid-range)
        blue_pts = [(0.45, 0.42), (0.50, 0.47), (0.55, 0.52), (0.58, 0.50), (0.52, 0.55)]
        blue_dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.08, color=COL_BLUE)
            for x, y in blue_pts
        ])

        self.play(AnimationGroup(*[FadeIn(d, scale=0.5) for d in orange_dots], lag_ratio=0.1),
                  run_time=0.8)
        self.play(AnimationGroup(*[FadeIn(d, scale=0.5) for d in blue_dots], lag_ratio=0.15),
                  run_time=0.6)

        # legend
        leg_orange = VGroup(
            Dot(radius=0.08, color="#E88C28"),
            Text("One-time (failed)", font_size=13, color=COL_WHITE)
        ).arrange(RIGHT, buff=0.12)
        leg_blue = VGroup(
            Dot(radius=0.08, color=COL_BLUE),
            Text("Manual 4-stage (~120 ep)", font_size=13, color=COL_WHITE)
        ).arrange(RIGHT, buff=0.12)
        leg_gold = VGroup(
            Star(n=5, outer_radius=0.12, inner_radius=0.05, color=COL_GOLD, fill_opacity=1),
            Text("TurboTrain (~45 ep)", font_size=13, color=COL_GOLD, weight=BOLD)
        ).arrange(RIGHT, buff=0.12)
        legend = VGroup(leg_orange, leg_blue, leg_gold).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        legend.to_corner(UR, buff=0.4)
        self.play(FadeIn(legend), run_time=0.3)
        self.wait(0.5)

        # ═══ PART B: TurboTrain Pipeline ══════════════════════════
        # Shift scatter to left, show pipeline on right
        pipeline_x = RIGHT * 3.8

        pt_header = Text("TurboTrain", font_size=26, color=COL_GOLD, weight=BOLD)
        pt_header.move_to(pipeline_x + UP * 3.0)
        self.play(FadeIn(pt_header), run_time=0.4)

        # Stage 1
        s1_box = RoundedRectangle(width=4.0, height=1.6, corner_radius=0.15,
                                   fill_color="#1E3A5F", fill_opacity=1,
                                   stroke_color=COL_BLUE, stroke_width=2)
        s1_box.move_to(pipeline_x + UP * 1.5)
        s1_lbl = Text("Stage 1: Pretrain", font_size=16, color=COL_BLUE, weight=BOLD)
        s1_sub = Text("Masked LiDAR reconstruction\n(task-agnostic 4D repr.)", font_size=13, color=COL_WHITE)
        VGroup(s1_lbl, s1_sub).arrange(DOWN, buff=0.1).move_to(s1_box.get_center())
        self.play(FadeIn(s1_box), FadeIn(s1_lbl), FadeIn(s1_sub), run_time=0.5)

        arr12 = Arrow(s1_box.get_bottom(), s1_box.get_bottom() + DOWN * 0.7,
                      color=COL_WHITE, buff=0.05)
        self.play(GrowArrow(arr12), run_time=0.3)

        # Stage 2
        s2_box = RoundedRectangle(width=4.0, height=1.6, corner_radius=0.15,
                                   fill_color="#1B4332", fill_opacity=1,
                                   stroke_color=COL_GREEN, stroke_width=2)
        s2_box.move_to(pipeline_x + DOWN * 0.3)
        s2_lbl = Text("Stage 2: Balance", font_size=16, color=COL_GREEN, weight=BOLD)
        s2_sub = Text("Hybrid gradient strategy", font_size=13, color=COL_WHITE)
        VGroup(s2_lbl, s2_sub).arrange(DOWN, buff=0.1).move_to(s2_box.get_center())
        self.play(FadeIn(s2_box), FadeIn(s2_lbl), FadeIn(s2_sub), run_time=0.5)

        # Alternating gradient arrows
        sub_a = Text("Free gradient steps", font_size=12, color=COL_LIGHT_BLUE)
        sub_b = Text("Conflict-suppressing steps", font_size=12, color=COL_GREEN)
        VGroup(sub_a, sub_b).arrange(DOWN, buff=0.12).next_to(s2_box, DOWN, buff=0.2)

        for _ in range(2):
            arr_free     = Arrow(s2_box.get_right(), s2_box.get_right() + RIGHT * 0.7,
                                 color=COL_BLUE, buff=0)
            arr_conflict = Arrow(s2_box.get_right(), s2_box.get_right() + RIGHT * 0.7,
                                 color=COL_GREEN, buff=0)
            self.play(GrowArrow(arr_free),   run_time=0.2)
            self.play(FadeOut(arr_free),     run_time=0.1)
            self.play(GrowArrow(arr_conflict), run_time=0.2)
            self.play(FadeOut(arr_conflict), run_time=0.1)

        self.play(FadeIn(sub_a), FadeIn(sub_b), run_time=0.3)

        # TurboTrain star on scatter plot
        star = Star(n=5, outer_radius=0.15, inner_radius=0.06,
                    fill_color=COL_GOLD, fill_opacity=1, stroke_width=0)
        star.move_to(axes.c2p(0.82, 0.88))
        ep_lbl = Text("~45 ep", font_size=12, color=COL_GOLD)
        ep_lbl.next_to(star, UR, buff=0.1)
        self.play(FadeIn(star, scale=2.0), FadeIn(ep_lbl), run_time=0.5)

        # Result box
        result_box = RoundedRectangle(width=4.0, height=1.2, corner_radius=0.12,
                                       fill_color="#1B4332", fill_opacity=1,
                                       stroke_color=COL_GREEN, stroke_width=2)
        result_box.next_to(sub_b, DOWN, buff=0.25)
        r1 = Text("45 ep  vs.  120 ep  (manual)", font_size=16, color=COL_GREEN, weight=BOLD)
        r2 = Text("No human expertise needed",   font_size=13, color=COL_WHITE)
        VGroup(r1, r2).arrange(DOWN, buff=0.1).move_to(result_box.get_center())
        self.play(FadeIn(result_box), FadeIn(r1), FadeIn(r2), run_time=0.5)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
