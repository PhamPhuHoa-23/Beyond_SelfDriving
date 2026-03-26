# drivex/scenes/part01/p01_s06_vla_roadmap.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-06: VLA Roadmap & DriveLM Dataset  (~60s)
#
# Spec: spec_intro_part01.md → SCENE 1-06
# Timeline of VLA approaches (2023-2025) with 4 approach categories
# Language emphasis box → DriveLM QA chain diagram
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    COL_BLUE, COL_GOLD, COL_WHITE, COL_LIGHT_BLUE,
    COL_GREEN, COL_PURPLE, COL_DEEP_BLUE, BG_DARK,
)

_BG = "#0F172A"

# Timeline model data: (name, year_offset, above_or_below, category)
# year_offset: 0.0 to 1.0 (left to right on spine)
_MODELS = [
    ("GPT-Driver",    0.05, True,  COL_BLUE,   "Text Action"),
    ("BEVDriver",     0.2,  False, COL_GREEN,  "Numerical"),
    ("DriveLM",       0.38, True,  COL_GOLD,   "Explicit"),
    ("DriveVLM",      0.52, False, COL_PURPLE, "Implicit"),
    ("EMMA",          0.65, True,  COL_BLUE,   "Text Action"),
    ("UniAD-e2e",     0.78, False, COL_GREEN,  "Numerical"),
    ("DiffusionDrv",  0.90, True,  "#E67E22",  "Numerical"),
]

_CATEGORIES = [
    ("Textual Action",       COL_BLUE),
    ("Numerical Action",     COL_GREEN),
    ("Explicit Guidance",    "#E67E22"),
    ("Implicit Transfer",    COL_PURPLE),
]


def _model_node(label, year_str, above, color):
    """A timeline node: dot + label + year."""
    dot = Dot(radius=0.1, color=color)
    n_lbl = Text(label, font_size=12, color=COL_WHITE)
    y_lbl = Text(year_str, font_size=10, color=COL_LIGHT_BLUE)
    y_off = 0.7 if above else -0.7
    n_lbl.next_to(dot, UP * y_off, buff=0.1) if above else n_lbl.next_to(dot, DOWN * abs(y_off), buff=0.1)
    y_lbl.next_to(n_lbl, DOWN if above else UP, buff=0.05)
    return VGroup(dot, n_lbl, y_lbl)


def _drivelm_step(text, color):
    box = RoundedRectangle(
        corner_radius=0.12, width=2.2, height=0.75,
        fill_color=COL_DEEP_BLUE, fill_opacity=1,
        stroke_color=color, stroke_width=2,
    )
    lbl = Text(text, font_size=13, color=COL_WHITE).move_to(box)
    return VGroup(box, lbl)


class P01S06VLARoadmap(Scene):
    """SCENE 1-06 — VLA Roadmap & DriveLM"""

    def construct(self):
        self.camera.background_color = _BG

        # ── Timeline ──────────────────────────────────────────────
        spine_w = 10.5
        spine = Line(LEFT * spine_w / 2, RIGHT * spine_w / 2,
                     stroke_color=COL_WHITE, stroke_width=2)
        spine.shift(UP * 0.4)

        self.play(Create(spine), run_time=0.6)

        # Place model nodes
        nodes = VGroup()
        for name, t, above, color, _ in _MODELS:
            pos = spine.get_left() + RIGHT * spine_w * t
            node = _model_node(name, "2023-25", above, color)
            node.move_to(pos + UP * (0.1 if above else -0.1))
            nodes.add(node)

        self.play(LaggedStart(
            *[FadeIn(n, shift=UP * 0.05) for n in nodes],
            lag_ratio=0.1,
        ), run_time=2.0)

        # ── Category legend (right side) ─────────────────────────
        legend = VGroup()
        for cat, color in _CATEGORIES:
            bar  = Rectangle(width=0.25, height=0.25,
                             fill_color=color, fill_opacity=0.85,
                             stroke_width=0)
            cat_lbl = Text(cat, font_size=12, color=COL_WHITE)
            row = VGroup(bar, cat_lbl).arrange(RIGHT, buff=0.12)
            legend.add(row)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR, buff=0.5)

        self.play(FadeIn(legend), run_time=0.4)

        # ── "Language" emphasis box ───────────────────────────────
        lang_box = RoundedRectangle(
            corner_radius=0.2, width=3.2, height=0.8,
            fill_color="#1A1200", fill_opacity=1,
            stroke_color=COL_GOLD, stroke_width=2.5,
        ).to_edge(DOWN, buff=1.4)
        lang_lbl = Text("Language is at the core.",
                        font_size=20, color=COL_GOLD, weight=BOLD)
        lang_lbl.move_to(lang_box)
        self.play(FadeIn(lang_box), Write(lang_lbl), run_time=0.6)
        self.wait(0.5)

        # Dim timeline, bring up DriveLM chain
        self.play(
            spine.animate.set_opacity(0.3),
            nodes.animate.set_opacity(0.3),
            legend.animate.set_opacity(0.3),
            lang_box.animate.shift(UP * 2.5),
            lang_lbl.animate.shift(UP * 2.5),
            run_time=0.5,
        )

        # ── DriveLM chain diagram ─────────────────────────────────
        step_data = [
            ("Perceive:\nWhat do I see?",   COL_BLUE),
            ("Predict:\nWhat will happen?", COL_PURPLE),
            ("Plan:\nWhat should I do?",    COL_GOLD),
            ("Act:\nExact trajectory",      COL_GREEN),
        ]
        steps = [_drivelm_step(t, c) for t, c in step_data]
        steps_grp = VGroup(*steps).arrange(RIGHT, buff=0.3).center().shift(DOWN * 0.4)

        chain_arrows = VGroup(*[
            Arrow(
                steps[i].get_right(), steps[i + 1].get_left(),
                stroke_color=COL_WHITE, stroke_width=1.5,
                max_tip_length_to_length_ratio=0.35, buff=0.05,
            )
            for i in range(len(steps) - 1)
        ])

        dl_header = Text("DriveLM — Grounded Language QA Chain",
                         font_size=18, color=COL_LIGHT_BLUE)
        dl_header.next_to(steps_grp, UP, buff=0.4)

        self.play(FadeIn(dl_header), run_time=0.3)
        for step, arrow in zip(steps, list(chain_arrows) + [None]):
            self.play(FadeIn(step, shift=RIGHT * 0.1), run_time=0.3)
            if arrow:
                self.play(GrowArrow(arrow), run_time=0.2)
        self.wait(1.2)

        # Outro
        self.play(FadeOut(VGroup(
            spine, nodes, legend, lang_box, lang_lbl,
            steps_grp, chain_arrows, dl_header,
        )), run_time=0.5)
        self.wait(0.2)
