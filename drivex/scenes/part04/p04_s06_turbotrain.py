"""
Scene 4-06 — TurboTrain: 2-Stage Solution
==========================================
Section A — Stage 1 (Pretrain) + Stage 2 (Balance) pipeline diagram.
Section B — Scatter plot: baseline orange + manual blue + TurboTrain gold star.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P04S06TurboTrain(Scene):
    """
    A — 2-stage pipeline (Pretrain → Balance) with "Solves" badges
    B — Scatter result showing TurboTrain gold star outperforms all
    """

    def construct(self):
        self.camera.background_color = "#0F172A"

        title = Text("TurboTrain — 2-Stage Pipeline", font_size=22, color=COL_GOLD,
                     weight=BOLD)
        title.to_edge(UP, buff=0.4)
        sub = Text("2 stages vs 4 manual stages", font_size=14, color=COL_WHITE,
                   slant=ITALIC)
        sub.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(sub), run_time=0.4)

        # ═══ SECTION A — Pipeline ══════════════════════════════════
        def stage_box(header, sub_lbl, mech_lbl, bg_col, stroke_col, pos):
            box = RoundedRectangle(width=4.5, height=2.2, corner_radius=0.2,
                                   fill_color=bg_col, fill_opacity=1,
                                   stroke_color=stroke_col, stroke_width=2)
            h = Text(header, font_size=16, color=stroke_col, weight=BOLD)
            s = Text(sub_lbl, font_size=13, color=COL_LIGHT_BLUE)
            m = Text(mech_lbl, font_size=11, color=COL_WHITE, slant=ITALIC)
            box.move_to(pos)
            h.move_to(box.get_center() + UP * 0.65)
            s.move_to(box.get_center() + UP * 0.18)
            m.move_to(box.get_center() + DOWN * 0.25)
            m.width = 4.0
            return VGroup(box, h, s, m)

        stage1 = stage_box(
            "Stage 1 — Pretrain",
            "Task-agnostic 4D representation",
            "Masked LiDAR reconstruction\nmulti-agent, multi-frame",
            "#1E3A5F", COL_BLUE, LEFT * 2.8 + DOWN * 0.5
        )
        stage2 = stage_box(
            "Stage 2 — Balance",
            "Hybrid gradient strategy",
            "Free steps  ↔  Conflict-suppressing steps",
            "#1B4332", COL_GREEN, RIGHT * 2.8 + DOWN * 0.5
        )
        mid_arr = Arrow(stage1.get_right(), stage2.get_left(), buff=0.1,
                        color=COL_WHITE, stroke_width=2.5, tip_length=0.16)

        def solves_badge(text, color, parent, direction):
            bg = RoundedRectangle(width=3.0, height=0.45, corner_radius=0.1,
                                  fill_color=COL_NAVY, fill_opacity=1,
                                  stroke_color=color, stroke_width=1.5)
            txt = Text(f"Solves: {text}", font_size=11, color=color)
            bg.next_to(parent, direction, buff=0.12)
            txt.move_to(bg.get_center())
            return VGroup(bg, txt)

        badge1 = solves_badge("initialization sensitivity",
                              COL_GREEN, stage1, DOWN)
        badge2 = solves_badge("gradient conflict",
                              COL_GREEN, stage2, DOWN)

        self.play(FadeIn(stage1), run_time=0.5)
        self.play(FadeIn(badge1), run_time=0.2)
        self.play(GrowArrow(mid_arr), run_time=0.3)
        self.play(FadeIn(stage2), run_time=0.5)
        self.play(FadeIn(badge2), run_time=0.2)

        # Alternating flash on free/conflict arrows (visual for alternating strategy)
        free_arr = Arrow(stage2[0].get_center() + LEFT * 1.0 + DOWN * 0.1,
                         stage2[0].get_center() + RIGHT * 0.8 + DOWN * 0.1,
                         buff=0, color=COL_BLUE, stroke_width=2, tip_length=0.12)
        conf_arr = free_arr.copy().set_color(COL_GREEN).shift(DOWN * 0.35)
        # Already represented in the stage box text; skip extra arrows to keep it clean
        self.wait(0.5)

        # ═══ SECTION B — Result scatter ═══════════════════════════
        self.play(FadeOut(Group(stage1, stage2, mid_arr, badge1, badge2, sub)),
                  run_time=0.3)

        axes = Axes(
            x_range=[0, 1, 0.25], y_range=[0, 1, 0.25],
            x_length=5.5, y_length=3.8,
            axis_config={"color": COL_WHITE,
                         "stroke_width": 1.5, "include_numbers": False},
            tips=False,
        ).shift(DOWN * 0.5)
        ax_xlbl = Text("AP@0.5", font_size=11, color=COL_WHITE)
        ax_xlbl.next_to(axes.x_axis, DOWN, buff=0.15)
        ax_ylbl = Text("EPA", font_size=11, color=COL_WHITE).rotate(PI / 2)
        ax_ylbl.next_to(axes.y_axis, LEFT, buff=0.18)
        self.play(Create(axes), FadeIn(ax_xlbl), FadeIn(ax_ylbl), run_time=0.4)

        # Orange failure dots (reuse from S05)
        fail_pts = [[0.12, 0.10], [0.18, 0.08], [0.08, 0.14], [0.22, 0.12],
                    [0.14, 0.07], [0.10, 0.18], [0.20, 0.16], [0.16, 0.09]]
        for px, py in fail_pts:
            self.play(FadeIn(Dot(axes.c2p(px, py), radius=0.09, color="#E67E22")),
                      run_time=0.04)

        # Blue dots (manual 4-stage, 120 epochs)
        manual_pts = [[0.52, 0.50], [0.55, 0.48], [
            0.48, 0.54], [0.58, 0.46], [0.50, 0.52]]
        for px, py in manual_pts:
            self.play(FadeIn(Dot(axes.c2p(px, py), radius=0.09, color=COL_BLUE)),
                      run_time=0.05)
        manual_lbl = Text("120 epochs\n(manual 4-stage)",
                          font_size=11, color=COL_BLUE)
        manual_lbl.move_to(axes.c2p(0.56, 0.58))
        self.play(FadeIn(manual_lbl), run_time=0.2)

        # Gold star — TurboTrain (45 epochs, best position)
        star_pos = axes.c2p(0.82, 0.85)
        star = Star(n=5, outer_radius=0.18, inner_radius=0.08,
                    fill_color=COL_GOLD, fill_opacity=1, stroke_width=0).move_to(star_pos)
        self.play(FadeIn(star, scale=1.5), run_time=0.4)
        self.play(star.animate.scale(1.0), run_time=0.2)

        star_lbl = Text("TurboTrain\n~45 epochs", font_size=12,
                        color=COL_GOLD, weight=BOLD)
        star_lbl.next_to(star, UR, buff=0.1)
        star_arr = Arrow(star_lbl.get_left(), star.get_right(),
                         buff=0.05, color=COL_GOLD, stroke_width=1.5, tip_length=0.12)
        self.play(FadeIn(star_lbl), Create(star_arr), run_time=0.3)

        callout = RoundedRectangle(width=4.0, height=0.65, corner_radius=0.12,
                                   fill_color="#1B4332", fill_opacity=1,
                                   stroke_color=COL_GREEN, stroke_width=1.5)
        callout_txt = Text("45 vs 120 epochs — less than half the compute",
                           font_size=12, color=COL_INT8_GREEN, weight=BOLD)
        callout.to_edge(DOWN, buff=0.4)
        callout_txt.move_to(callout.get_center())
        self.play(FadeIn(VGroup(callout, callout_txt)), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
