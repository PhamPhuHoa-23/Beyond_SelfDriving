# drivex/scenes/part01/p01_s03_av_arch.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-03: AV Industry — Three Architectures  (~90s)
#
# Spec: spec_intro_part01.md → SCENE 1-03
# Three-column layout: Modular | End-to-End | Hybrid
# Each column builds sequentially with pipeline boxes + arrows.
# Weakness labels (✗/✓) appear after each column.
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    COL_BLUE, COL_WHITE, COL_LIGHT_BLUE, COL_RED, COL_GREEN,
    COL_GOLD, COL_DEEP_BLUE, COL_DEEP_GREEN, COL_DEEP_PURPLE,
    COL_NAVY, BG_DARK,
)

_BG = "#0F172A"
_PIPE_W = 2.2   # column width
_BOX_W  = 1.9   # pipeline box width
_BOX_H  = 0.38
_COL_X  = [-4.2, 0.0, 4.2]   # column centers


def _pipeline_box(label, color=COL_DEEP_BLUE, stroke=COL_BLUE):
    rect = RoundedRectangle(
        corner_radius=0.1, width=_BOX_W, height=_BOX_H,
        fill_color=color, fill_opacity=1,
        stroke_color=stroke, stroke_width=1.5,
    )
    txt = Text(label, font_size=15, color=COL_WHITE).move_to(rect)
    return VGroup(rect, txt)


def _down_arrow():
    return Arrow(
        UP * 0.05, DOWN * 0.05,
        stroke_color=COL_BLUE, stroke_width=1.8,
        buff=0.0, max_tip_length_to_length_ratio=0.4,
    )


def _weakness(text, icon="✗", color=COL_RED):
    sym = Text(icon, font_size=16, color=color)
    lbl = Text(text, font_size=13, color=color)
    grp = VGroup(sym, lbl).arrange(RIGHT, buff=0.1)
    return grp


def _build_modular_column(cx):
    """Build Modular pipeline as a VGroup, placed at x = cx."""
    boxes = [
        _pipeline_box("Sensor"),
        _pipeline_box("Perception"),
        _pipeline_box("Localization"),
        _pipeline_box("Prediction"),
        _pipeline_box("Planning"),
        _pipeline_box("Control"),
        _pipeline_box("Action", color=COL_DEEP_GREEN, stroke=COL_GREEN),
    ]
    col = VGroup()
    for i, box in enumerate(boxes):
        col.add(box)
        if i < len(boxes) - 1:
            col.add(_down_arrow())
    col.arrange(DOWN, buff=0.06).move_to([cx, 0.5, 0])

    weaknesses = VGroup(
        _weakness("Error Accumulation"),
        _weakness("No Joint Optimization"),
        _weakness("No Continual Learning"),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    weaknesses.next_to(col, DOWN, buff=0.25)

    return col, weaknesses


def _build_e2e_column(cx):
    """Build End-to-End pipeline."""
    sensor = _pipeline_box("Sensor")
    nn     = _pipeline_box("Neural Network\n(E2E)",
                           color=COL_DEEP_PURPLE, stroke="#7C3AED")
    nn[0].set_height(0.8)   # make NN box taller
    nn[1].move_to(nn[0])
    action = _pipeline_box("Action", color=COL_DEEP_GREEN, stroke=COL_GREEN)

    col = VGroup(sensor, _down_arrow(), nn, _down_arrow(), action)
    col.arrange(DOWN, buff=0.06).move_to([cx, 0.5, 0])

    weaknesses = VGroup(
        _weakness("Safety Verification\nImpossible"),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    weaknesses.next_to(col, DOWN, buff=0.25)

    return col, weaknesses


def _build_hybrid_column(cx):
    """Build Hybrid pipeline."""
    sensor = _pipeline_box("Sensor")
    ml     = _pipeline_box("ML (Perception\n+ Planning)",
                           color=COL_DEEP_GREEN, stroke=COL_GREEN)
    ml[0].set_height(0.7); ml[1].move_to(ml[0])
    ctrl   = _pipeline_box("Control Module")
    action = _pipeline_box("Action", color=COL_DEEP_GREEN, stroke=COL_GREEN)

    col = VGroup(sensor, _down_arrow(), ml, _down_arrow(), ctrl,
                 _down_arrow(), action)
    col.arrange(DOWN, buff=0.06).move_to([cx, 0.5, 0])

    strengths = VGroup(
        _weakness("Balanced", icon="✓", color=COL_GREEN),
    )
    strengths.next_to(col, DOWN, buff=0.25)

    return col, strengths


class P01S03AVArch(Scene):
    """SCENE 1-03 — AV Industry: Three Architectures"""

    def construct(self):
        self.camera.background_color = _BG

        # Column headers
        headers = VGroup(
            Text("Modular",    font_size=22, color=COL_WHITE, weight=BOLD).move_to([_COL_X[0], 3.2, 0]),
            Text("End-to-End", font_size=22, color=COL_WHITE, weight=BOLD).move_to([_COL_X[1], 3.2, 0]),
            Text("Hybrid",     font_size=22, color=COL_WHITE, weight=BOLD).move_to([_COL_X[2], 3.2, 0]),
        )
        # Separator lines under headers
        seps = VGroup(*[
            Line(LEFT * 1.0 + [cx, 0, 0], RIGHT * 1.0 + [cx, 0, 0],
                 stroke_color=COL_BLUE, stroke_width=1)
                 .next_to(headers[i], DOWN, buff=0.1)
            for i, cx in enumerate(_COL_X)
        ])

        # Build columns
        mod_col,  mod_weak  = _build_modular_column(_COL_X[0])
        e2e_col,  e2e_weak  = _build_e2e_column(_COL_X[1])
        hyb_col,  hyb_str   = _build_hybrid_column(_COL_X[2])

        # ── Column 1: Modular ─────────────────────────────────────
        self.play(Write(headers[0]), Create(seps[0]), run_time=0.4)
        pipe_boxes = [c for c in mod_col if isinstance(c, VGroup)]
        arrows     = [c for c in mod_col if isinstance(c, Arrow)]
        for box in pipe_boxes:
            self.play(FadeIn(box, shift=DOWN * 0.05), run_time=0.22)
        self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.05) for w in mod_weak],
                               lag_ratio=0.15), run_time=0.5)

        # ── Column 2: E2E ─────────────────────────────────────────
        self.play(Write(headers[1]), Create(seps[1]), run_time=0.4)
        self.play(
            *[FadeIn(item) for item in e2e_col],
            run_time=0.8,
        )
        self.play(FadeIn(e2e_weak), run_time=0.3)

        # ── Column 3: Hybrid ──────────────────────────────────────
        self.play(Write(headers[2]), Create(seps[2]), run_time=0.4)
        self.play(
            *[FadeIn(item) for item in hyb_col],
            run_time=0.8,
        )
        self.play(FadeIn(hyb_str), run_time=0.3)

        # Shared limitation note
        note = Text(
            "All three share one fundamental weakness →",
            font_size=18, color=COL_GOLD,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(note), run_time=0.6)
        self.wait(1.0)

        # Outro
        all_objs = VGroup(
            headers, seps,
            mod_col, mod_weak,
            e2e_col, e2e_weak,
            hyb_col, hyb_str,
            note,
        )
        self.play(FadeOut(all_objs), run_time=0.5)
        self.wait(0.2)
