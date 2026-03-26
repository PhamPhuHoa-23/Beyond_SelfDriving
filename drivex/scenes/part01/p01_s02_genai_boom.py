# drivex/scenes/part01/p01_s02_genai_boom.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-02: Generative AI Boom  (~60s)
#
# Spec: spec_intro_part01.md → SCENE 1-02
# Grid of 4 capability icons → converge to "Foundation Models" box
# PI question → Foundation Model pipeline diagram
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    COL_BLUE, COL_GOLD, COL_WHITE, COL_LIGHT_BLUE,
    COL_GREEN, COL_PURPLE, COL_NAVY,
    COL_DEEP_BLUE, COL_DEEP_GREEN, COL_DEEP_PURPLE,
    BG_DARK,
)
from drivex.components.mascots import create_pi_mascot
from drivex.components.thought_bubble import PIBubble

_BG = "#111827"


def _cap_icon(symbol, label, color):
    """Small capability icon: symbol text + label."""
    box = RoundedRectangle(
        corner_radius=0.15, width=1.6, height=1.6,
        fill_color=color, fill_opacity=0.2,
        stroke_color=color, stroke_width=2,
    )
    sym = Text(symbol, font_size=32, color=color).move_to(box.get_center() + UP * 0.2)
    lbl = Text(label, font_size=14, color=COL_WHITE).move_to(box.get_center() + DOWN * 0.38)
    return VGroup(box, sym, lbl)


def _data_row(label, sub, color):
    """A colored row in the pipeline data column."""
    rect = Rectangle(width=1.8, height=0.38,
                     fill_color=color, fill_opacity=0.7,
                     stroke_width=0)
    txt = Text(f"{label} — {sub}", font_size=11, color=COL_WHITE).move_to(rect)
    return VGroup(rect, txt)


def _task_row(label, color="#2A2A3A"):
    """A task row on the right side of the pipeline."""
    rect = Rectangle(width=2.0, height=0.38,
                     fill_color=color, fill_opacity=0.8,
                     stroke_color=COL_BLUE, stroke_width=0.8)
    txt = Text(label, font_size=11, color=COL_WHITE).move_to(rect)
    return VGroup(rect, txt)


class P01S02GenAIBoom(Scene):
    """SCENE 1-02 — Generative AI Boom & Foundation Models"""

    def construct(self):
        self.camera.background_color = _BG

        # ── Year label ────────────────────────────────────────────
        year_lbl = Text("2023 →", font_size=22, color=COL_GOLD)
        year_lbl.to_corner(UL, buff=0.4)
        self.play(FadeIn(year_lbl), run_time=0.4)

        # ── 4 capability icons in a 2x2 grid ─────────────────────
        icons = VGroup(
            _cap_icon("⚙", "Coding",    COL_BLUE),
            _cap_icon("💡", "Reasoning", COL_GOLD),
            _cap_icon("🖼", "Image Gen", COL_GREEN),
            _cap_icon("▶", "Video Syn", COL_PURPLE),
        ).arrange_in_grid(rows=2, cols=2, buff=0.4).center()

        for i, icon in enumerate(icons):
            self.play(FadeIn(icon, shift=UP * 0.1), run_time=0.3)

        self.wait(0.4)

        # Converge icons to center
        center_pos = ORIGIN
        self.play(
            *[icon.animate.move_to(center_pos).scale(0.4) for icon in icons],
            run_time=0.6,
        )
        self.play(FadeOut(icons), run_time=0.3)

        # ── "Foundation Models" central label box ─────────────────
        fm_box = RoundedRectangle(
            corner_radius=0.25, width=3.8, height=1.0,
            fill_color=COL_BLUE, fill_opacity=1,
            stroke_color=COL_WHITE, stroke_width=2,
        ).center()
        fm_lbl = Text("Foundation Models", font_size=28, color=COL_WHITE, weight=BOLD)
        fm_lbl.move_to(fm_box)
        fm_group = VGroup(fm_box, fm_lbl)
        self.play(FadeIn(fm_group), run_time=0.5)
        self.wait(0.4)

        # ── PI mascot question ────────────────────────────────────
        pi = create_pi_mascot(height=0.9)
        pi.to_corner(DL, buff=0.5)
        bubble = PIBubble(pi, "Foundation Model\nlà gì vậy?",
                          position=UP + RIGHT, font_size=18)
        self.play(FadeIn(pi), FadeIn(bubble), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(pi), FadeOut(bubble), FadeOut(fm_group),
                  FadeOut(year_lbl), run_time=0.4)

        # ═══════════════════════════════════════════════════════
        # Pipeline diagram: Data → FM → Tasks
        # ═══════════════════════════════════════════════════════
        # ── Data column ──────────────────────────────────────────
        data_rows = VGroup(
            _data_row("Text",   "Wiki/Books",  "#4A4A8A"),
            _data_row("Image",  "LAION/CC",    COL_BLUE),
            _data_row("Speech", "Common Voice","#2A7A2A"),
            _data_row("3D",     "ShapeNet",    "#7A2A7A"),
            _data_row("Video",  "YT/Panda",    "#8A4A2A"),
        ).arrange(DOWN, buff=0.06)

        data_header = Text("Diverse Data", font_size=16, color=COL_LIGHT_BLUE)
        data_col = VGroup(data_header, data_rows).arrange(DOWN, buff=0.12)
        data_col.shift(LEFT * 4.8)

        # ── Center model box ──────────────────────────────────────
        model_box = RoundedRectangle(
            corner_radius=0.3, width=2.5, height=2.2,
            fill_color=COL_NAVY, fill_opacity=1,
            stroke_color=COL_GOLD, stroke_width=2.5,
        )
        model_lbl = Text("Foundation\nModel", font_size=20,
                         color=COL_WHITE, weight=BOLD).move_to(model_box)
        ssl_lbl = Text("(self-supervised)", font_size=13,
                       color=COL_LIGHT_BLUE).next_to(model_box, DOWN, buff=0.12)
        model_grp = VGroup(model_box, model_lbl, ssl_lbl)

        # ── Tasks column ──────────────────────────────────────────
        task_rows = VGroup(
            _task_row("Info Extraction"),
            _task_row("Object Recognition"),
            _task_row("Image Captioning"),
            _task_row("Visual QA"),
            _task_row("Text Generation"),
            _task_row("Fine-tuned Tasks"),
        ).arrange(DOWN, buff=0.06)

        task_header = Text("Downstream Tasks", font_size=16, color=COL_LIGHT_BLUE)
        task_col = VGroup(task_header, task_rows).arrange(DOWN, buff=0.12)
        task_col.shift(RIGHT * 4.6)

        # ── Arrows ────────────────────────────────────────────────
        arr_train = Arrow(
            data_col.get_right(), model_grp.get_left(),
            stroke_color=COL_WHITE, stroke_width=2, buff=0.2,
        )
        arr_train_lbl = Text("Train", font_size=13, color=COL_LIGHT_BLUE)
        arr_train_lbl.next_to(arr_train, UP, buff=0.08)

        arr_adapt = Arrow(
            model_grp.get_right(), task_col.get_left(),
            stroke_color=COL_WHITE, stroke_width=2, buff=0.2,
        )
        arr_adapt_lbl = Text("Adapt", font_size=13, color=COL_LIGHT_BLUE)
        arr_adapt_lbl.next_to(arr_adapt, UP, buff=0.08)

        # ── Animate pipeline ─────────────────────────────────────
        self.play(FadeIn(data_col), run_time=0.6)
        self.play(Create(arr_train), FadeIn(arr_train_lbl), run_time=0.4)
        self.play(FadeIn(model_grp), run_time=0.5)
        self.play(Create(arr_adapt), FadeIn(arr_adapt_lbl), run_time=0.4)
        self.play(LaggedStart(
            *[FadeIn(row, shift=LEFT * 0.1) for row in task_rows],
            lag_ratio=0.12,
        ), FadeIn(task_header), run_time=0.8)

        self.wait(1.5)

        # Outro
        self.play(FadeOut(VGroup(
            data_col, model_grp, task_col,
            arr_train, arr_train_lbl, arr_adapt, arr_adapt_lbl,
        )), run_time=0.5)
        self.wait(0.2)
