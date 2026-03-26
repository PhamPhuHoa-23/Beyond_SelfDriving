# drivex/scenes/part01/p01_s08_autovla.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-08: AutoVLA  (~75s)
#
# Spec: spec_intro_part01.md → SCENE 1-08
# Dual thinking mode diagram: simple → Fast / complex → Slow
# Training: SFT → RFT (GRPO) pipeline
# Results: 10.6% ↑ Planning, 66.8% ↓ Runtime
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    COL_BLUE, COL_GOLD, COL_WHITE, COL_LIGHT_BLUE,
    COL_GREEN, COL_RED, COL_DEEP_BLUE, COL_DEEP_GREEN,
    COL_DEEP_PURPLE, COL_PURPLE, BG_DARK,
)

_BG = "#0F172A"
_DEEP_RED = "#3D1A1A"


class P01S08AutoVLA(Scene):
    """SCENE 1-08 — AutoVLA: Dual Thinking Modes + Training"""

    def construct(self):
        self.camera.background_color = _BG

        # ── Header ────────────────────────────────────────────────
        title = Text("AutoVLA", font_size=28, color=COL_GOLD, weight=BOLD)
        title.to_corner(UL, buff=0.5)
        subtitle = Text("Dual Thinking Modes",
                        font_size=22, color=COL_WHITE)
        subtitle.next_to(title, RIGHT, buff=0.5)
        self.play(FadeIn(title), Write(subtitle), run_time=0.6)

        # ── Decision diamond ──────────────────────────────────────
        diamond = Square(side_length=1.1, fill_color=COL_DEEP_BLUE,
                         fill_opacity=1, stroke_color=COL_BLUE,
                         stroke_width=2).rotate(PI / 4).center().shift(UP * 0.5)
        sit_lbl = Text("Situation?", font_size=14, color=COL_WHITE)
        sit_lbl.move_to(diamond.get_center())
        self.play(FadeIn(diamond), FadeIn(sit_lbl), run_time=0.5)

        # ── Fast mode (left) ──────────────────────────────────────
        fast_box = RoundedRectangle(
            corner_radius=0.15, width=3.0, height=1.0,
            fill_color=COL_DEEP_GREEN, fill_opacity=1,
            stroke_color=COL_GREEN, stroke_width=2,
        ).shift(LEFT * 3.5 + UP * 0.5)
        fast_lbl = Text("Fast Mode\nDirect Action Output",
                        font_size=15, color=COL_GREEN).move_to(fast_box)

        arrow_simple = Arrow(
            diamond.get_left(), fast_box.get_right(),
            stroke_color=COL_GREEN, stroke_width=2, buff=0.1,
            max_tip_length_to_length_ratio=0.35,
        )
        simple_tag = Text("Simple", font_size=13, color=COL_GREEN)
        simple_tag.next_to(arrow_simple, UP, buff=0.08)

        self.play(GrowArrow(arrow_simple), FadeIn(simple_tag), run_time=0.4)
        self.play(FadeIn(fast_box), Write(fast_lbl), run_time=0.4)

        # ── Slow mode (right) ─────────────────────────────────────
        slow_box = RoundedRectangle(
            corner_radius=0.15, width=3.0, height=1.0,
            fill_color=_DEEP_RED, fill_opacity=1,
            stroke_color=COL_RED, stroke_width=2,
        ).shift(RIGHT * 3.5 + UP * 0.5)
        slow_lbl = Text("Slow Mode\nChain-of-Thought → Action",
                        font_size=14, color=COL_RED).move_to(slow_box)

        arrow_complex = Arrow(
            diamond.get_right(), slow_box.get_left(),
            stroke_color=COL_RED, stroke_width=2, buff=0.1,
            max_tip_length_to_length_ratio=0.35,
        )
        complex_tag = Text("Complex", font_size=13, color=COL_RED)
        complex_tag.next_to(arrow_complex, UP, buff=0.08)

        self.play(GrowArrow(arrow_complex), FadeIn(complex_tag), run_time=0.4)
        self.play(FadeIn(slow_box), Write(slow_lbl), run_time=0.4)
        self.wait(0.8)

        # ── Training pipeline (below) ─────────────────────────────
        divider = Line(LEFT * 5.5, RIGHT * 5.5,
                       stroke_color=COL_WHITE, stroke_width=1,
                       stroke_opacity=0.3).shift(DOWN * 0.8)
        self.play(Create(divider), run_time=0.3)

        sft_box = RoundedRectangle(
            corner_radius=0.15, width=2.8, height=0.85,
            fill_color=COL_DEEP_BLUE, fill_opacity=1,
            stroke_color=COL_BLUE, stroke_width=2,
        ).shift(LEFT * 3.0 + DOWN * 1.7)
        sft_lbl  = Text("Stage 1: SFT", font_size=16, color=COL_WHITE, weight=BOLD)
        sft_sub  = Text("Teaches both fast & slow modes", font_size=12, color=COL_LIGHT_BLUE)
        VGroup(sft_lbl, sft_sub).arrange(DOWN, buff=0.08).move_to(sft_box)

        arr_train = Arrow(
            sft_box.get_right(), sft_box.get_right() + RIGHT * 1.8,
            stroke_color=COL_WHITE, stroke_width=2, buff=0,
            max_tip_length_to_length_ratio=0.35,
        )

        rft_box = RoundedRectangle(
            corner_radius=0.15, width=2.8, height=0.85,
            fill_color=COL_DEEP_PURPLE, fill_opacity=1,
            stroke_color=COL_PURPLE, stroke_width=2,
        ).shift(RIGHT * 2.0 + DOWN * 1.7)
        rft_lbl  = Text("Stage 2: RFT (GRPO)", font_size=16, color=COL_WHITE, weight=BOLD)
        rft_sub  = Text("Align with verified rewards", font_size=12, color="#A78BFA")
        VGroup(rft_lbl, rft_sub).arrange(DOWN, buff=0.08).move_to(rft_box)

        self.play(FadeIn(sft_box), Write(sft_lbl), FadeIn(sft_sub), run_time=0.4)
        self.play(GrowArrow(arr_train), run_time=0.3)
        self.play(FadeIn(rft_box), Write(rft_lbl), FadeIn(rft_sub), run_time=0.4)

        # ── Results ───────────────────────────────────────────────
        res_quote = Text(
            "Reasoning training > Action-only training",
            font_size=18, color=COL_GOLD, weight=BOLD,
        ).shift(DOWN * 1.7 + RIGHT * 1.2)

        res_box1 = RoundedRectangle(
            corner_radius=0.12, width=2.2, height=0.75,
            fill_color=COL_DEEP_GREEN, fill_opacity=1, stroke_color=COL_GREEN, stroke_width=2,
        ).shift(DOWN * 2.8 + LEFT * 1.8)
        res_lbl1 = Text("10.6% ↑ Planning", font_size=16, color=COL_GREEN, weight=BOLD)
        res_lbl1.move_to(res_box1)

        res_box2 = RoundedRectangle(
            corner_radius=0.12, width=2.2, height=0.75,
            fill_color=COL_DEEP_GREEN, fill_opacity=1, stroke_color=COL_GREEN, stroke_width=2,
        ).shift(DOWN * 2.8 + RIGHT * 1.2)
        res_lbl2 = Text("66.8% ↓ Runtime", font_size=16, color=COL_GREEN, weight=BOLD)
        res_lbl2.move_to(res_box2)

        self.play(Write(res_quote), run_time=0.5)
        self.play(
            FadeIn(res_box1), Write(res_lbl1),
            FadeIn(res_box2), Write(res_lbl2),
            run_time=0.5,
        )
        self.wait(1.5)

        # Outro
        self.play(FadeOut(VGroup(
            title, subtitle, diamond, sit_lbl,
            fast_box, fast_lbl, arrow_simple, simple_tag,
            slow_box, slow_lbl, arrow_complex, complex_tag,
            divider, sft_box, arr_train, rft_box,
            res_quote, res_box1, res_lbl1, res_box2, res_lbl2,
        )), run_time=0.5)
        self.wait(0.2)
