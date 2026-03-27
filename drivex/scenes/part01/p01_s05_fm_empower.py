# drivex/scenes/part01/p01_s05_fm_empower.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-05: Foundation Models Empower AV  (~60s)
#
# Spec: spec_intro_part01.md → SCENE 1-05
# Left column: FM categories (Vision/Video/Vector/LLM/Multimodal)
# Right column: AV requirements rows
# Center "Empower" arrow
# Bottom goal text: "Long-tail Generalization and Generalist Experience"
# ─────────────────────────────────────────────────────────────────

from drivex.components.colors import (
    COL_NAVY, COL_BLUE, COL_GOLD, COL_WHITE, COL_LIGHT_BLUE,
    COL_GREEN, COL_DEEP_BLUE, COL_DEEP_GREEN, BG_DARK,
)
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")))


_BG = BG_DARK


def _fm_row(label, sub, color):
    rect = RoundedRectangle(
        corner_radius=0.1, width=2.8, height=0.52,
        fill_color=COL_DEEP_BLUE, fill_opacity=1,
        stroke_color=color, stroke_width=2,
    )
    main = Text(label, font_size=15, color=COL_WHITE, weight=BOLD).move_to(
        rect.get_center() + LEFT * 0.6)
    sub_lbl = Text(sub, font_size=11, color=COL_LIGHT_BLUE).move_to(
        rect.get_center() + RIGHT * 0.6)
    return VGroup(rect, main, sub_lbl)


def _ad_row(label):
    rect = RoundedRectangle(
        corner_radius=0.1, width=2.8, height=0.52,
        fill_color=COL_DEEP_GREEN, fill_opacity=1,
        stroke_color=COL_GREEN, stroke_width=2,
    )
    lbl = Text(label, font_size=14, color=COL_WHITE).move_to(rect)
    return VGroup(rect, lbl)


class P01S05FMEmpower(Scene):
    """SCENE 1-05 — Foundation Models Empower Autonomous Driving"""

    def construct(self):
        self.camera.background_color = _BG

        # ── Left column: Foundation Models ────────────────────────
        fm_header = Text("Foundation Models",
                         font_size=20, color=COL_WHITE, weight=BOLD)
        fm_rows = VGroup(
            _fm_row("Vision",     "SAM / DINO",          COL_BLUE),
            _fm_row("Video",      "Wan / Cosmos",        "#8A55E0"),
            _fm_row("Vector",     "HD Map Encoders",     "#2A9E9E"),
            _fm_row("LLM",        "GPT-4 / LLaMA",      COL_GOLD),
            _fm_row("Multimodal", "CLIP / LLaVA / BLIP", "#D4812A"),
        ).arrange(DOWN, buff=0.1)

        fm_col = VGroup(fm_header, fm_rows).arrange(DOWN, buff=0.18)
        fm_col.shift(LEFT * 4.0)

        # ── Right column: AV Requirements ─────────────────────────
        ad_header = Text("Autonomous Driving",
                         font_size=20, color=COL_WHITE, weight=BOLD)
        ad_rows = VGroup(
            _ad_row("Auto Data Labeling"),
            _ad_row("Scenario Generation"),
            _ad_row("Sensor Simulation"),
            _ad_row("Traffic Simulation"),
            _ad_row("Language Reasoning"),
            _ad_row("Edge-Case Coverage"),
        ).arrange(DOWN, buff=0.1)

        ad_col = VGroup(ad_header, ad_rows).arrange(DOWN, buff=0.18)
        ad_col.shift(RIGHT * 4.0)

        # ── Center "Empower" Arrow ────────────────────────────────
        empower_arrow = Arrow(
            LEFT * 1.2, RIGHT * 1.2,
            stroke_color=COL_GOLD, stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.25,
        )
        empower_lbl = Text("Empower", font_size=18,
                           color=COL_GOLD, weight=BOLD)
        empower_lbl.next_to(empower_arrow, UP, buff=0.12)

        # ── Bottom goal text ──────────────────────────────────────
        goal = Text(
            "Long-tail Generalization and Generalist Experience",
            font_size=20, color=COL_GOLD, weight=BOLD,
        ).to_edge(DOWN, buff=0.6)
        goal_box = SurroundingRectangle(
            goal, color=COL_GOLD, stroke_width=1.5, buff=0.2,
        )

        # ── Animations ────────────────────────────────────────────
        self.play(Write(fm_header), run_time=0.4)
        self.play(LaggedStart(
            *[FadeIn(row, shift=RIGHT * 0.1) for row in fm_rows],
            lag_ratio=0.15,
        ), run_time=0.75)

        self.play(Write(ad_header), run_time=0.4)
        self.play(LaggedStart(
            *[FadeIn(row, shift=LEFT * 0.1) for row in ad_rows],
            lag_ratio=0.12,
        ), run_time=0.8)

        self.play(GrowArrow(empower_arrow), run_time=0.8)
        self.play(FadeIn(empower_lbl), run_time=0.3)
        # Pulse the arrow
        self.play(
            empower_arrow.animate(rate_func=there_and_back, run_time=0.3)
            .scale(1.1),
        )

        self.play(Write(goal), run_time=0.8)
        self.play(Create(goal_box), run_time=0.4)
        self.wait(1.5)

        # Outro
        self.play(FadeOut(VGroup(
            fm_col, ad_col, empower_arrow, empower_lbl, goal, goal_box,
        )), run_time=0.5)
        self.wait(0.2)
