# drivex/scenes/part04/p04_s01_title.py
# ─────────────────────────────────────────────────────────────────
# SCENE 4-01: Title & Efficiency Framing  (~30s)
# Speaker: Seth Z. Zhao, UCLA Mobility Lab
#
# Spec: spec_part04.md → SCENE 4-01
# ─────────────────────────────────────────────────────────────────

from drivex.components.title_card import make_part_title_card
from drivex.components.colors import (
    COL_NAVY, COL_BLUE, COL_GOLD, COL_WHITE, COL_RED,
    COL_DEEP_BLUE, BG_DARK,
)
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")))


class P04S01Title(Scene):
    """SCENE 4-01 — Part 04 Title Card + Three Bottlenecks"""

    def construct(self):
        self.camera.background_color = COL_NAVY

        card = make_part_title_card(
            part_num=4,
            title="From Pre-Training to Post-Training:\nBuilding an Efficient V2X System",
            speaker="Seth Z. Zhao · UCLA Mobility Lab",
            callback_quote="'Works' is not enough.",
        )
        self.play(card.build_animation())
        self.wait(0.5)

        # Three bottleneck boxes
        def _bottle_box(label):
            box = RoundedRectangle(
                corner_radius=0.15, width=2.6, height=1.0,
                fill_color="#2A1A1A", fill_opacity=1,
                stroke_color=COL_RED, stroke_width=2,
            )
            lbl = Text(label, font_size=20, color=COL_RED, weight=BOLD)
            lbl.move_to(box)
            return VGroup(box, lbl)

        boxes = VGroup(
            _bottle_box("Data"),
            _bottle_box("Training"),
            _bottle_box("Inference"),
        )
        arrows = VGroup(
            Arrow(boxes[0].get_right(), boxes[1].get_left(),
                  stroke_color=COL_WHITE, stroke_width=1.5, buff=0.05),
            Arrow(boxes[1].get_right(), boxes[2].get_left(),
                  stroke_color=COL_WHITE, stroke_width=1.5, buff=0.05),
        )
        row = VGroup(boxes[0], arrows[0], boxes[1], arrows[1], boxes[2])
        row.arrange(RIGHT, buff=0.1).center().shift(DOWN * 0.8)

        for item in row:
            if isinstance(item, VGroup):
                self.play(FadeIn(item, shift=UP * 0.05), run_time=0.3)
            else:
                self.play(GrowArrow(item), run_time=0.2)

        self.wait(1.5)
        self.play(FadeOut(VGroup(card, row)), run_time=0.5)
        self.wait(0.2)


# ─────────────────────────────────────────────────────────────────
# SCENE 4-02: Why Efficiency Matters
# TODO: Implement from spec_part04.md → SCENE 4-02
# ─────────────────────────────────────────────────────────────────

class P04S02WhyEfficiency(Scene):
    """SCENE 4-02 — [STUB] Why Efficiency Matters in V2X"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 4-02\nWhy Efficiency Matters in V2X\n\n"
                   "Edge hardware constraints, latency, power budget",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


# ─────────────────────────────────────────────────────────────────
# SCENE 4-03 … 4-0N: Subsequent Part 04 scenes
# TODO: Map from spec_part04.md
# ─────────────────────────────────────────────────────────────────

class P04S03DataBottleneck(Scene):
    """SCENE 4-03 — [STUB] Bottleneck 1: Data Scarcity"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 4-03\nBottleneck 1: Data Scarcity\n\n"
                   "Semi-supervised / self-supervised labeling approaches",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


class P04S04TrainingBottleneck(Scene):
    """SCENE 4-04 — [STUB] Bottleneck 2: Training Cost"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 4-04\nBottleneck 2: Training Cost\n\n"
                   "LoRA / adapter fine-tuning, parameter efficiency",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


class P04S05InferenceBottleneck(Scene):
    """SCENE 4-05 — [STUB] Bottleneck 3: Inference on Edge"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 4-05\nBottleneck 3: Inference on Edge\n\n"
                   "INT8 quantization, FP32 vs INT8 cost comparison",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)
