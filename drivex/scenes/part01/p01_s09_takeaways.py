# drivex/scenes/part01/p01_s09_takeaways.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-09: Key Takeaways from Part 01  (~60s)
#
# Spec: spec_intro_part01.md → SCENE 1-09
# 4 numbered takeaway cards appear sequentially
# CAR mascot waves at the end
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    COL_NAVY, COL_BLUE, COL_GOLD, COL_WHITE, COL_LIGHT_BLUE,
    COL_GREEN, COL_DEEP_BLUE, COL_DEEP_GREEN,
)
from drivex.components.mascots import create_car_mascot, idle_bounce

_BG = COL_NAVY

_TAKEAWAYS = [
    (
        "1",
        "Long-tail Generalization",
        "Foundation models unlock the edge cases\nthat rule-based systems simply cannot handle.",
        COL_BLUE,
    ),
    (
        "2",
        "Multimodal LLMs (MLLMs)",
        "The most promising path toward scalable AV —\nbrings internet-scale world knowledge.",
        COL_GREEN,
    ),
    (
        "3",
        "Language as Inductive Bias",
        "Requiring the model to explain its reasoning\nforces better generalization, not just prediction.",
        COL_GOLD,
    ),
    (
        "4",
        "AutoVLA: Think When Needed",
        "Dual-mode reasoning cuts runtime by 66.8%\nwhile improving planning score by 10.6%.",
        "#E67E22",
    ),
]


def _takeaway_card(num, title, body, color, width=4.8, height=1.5):
    bg = RoundedRectangle(
        corner_radius=0.2, width=width, height=height,
        fill_color=COL_DEEP_BLUE, fill_opacity=1,
        stroke_color=color, stroke_width=2.5,
    )
    num_mob = Text(num, font_size=36, color=color, weight=BOLD)
    num_mob.move_to(bg.get_left() + RIGHT * 0.55)

    title_mob = Text(title, font_size=16, color=COL_WHITE, weight=BOLD)
    body_mob  = Text(body,  font_size=13, color=COL_LIGHT_BLUE)
    text_grp  = VGroup(title_mob, body_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    text_grp.move_to(bg.get_center() + RIGHT * 0.45)

    return VGroup(bg, num_mob, text_grp)


class P01S09Takeaways(Scene):
    """SCENE 1-09 — Part 01 Key Takeaways"""

    def construct(self):
        self.camera.background_color = _BG

        header = Text(
            "Part 01 — Key Takeaways",
            font_size=28, color=COL_GOLD, weight=BOLD,
        ).to_edge(UP, buff=0.45)
        self.play(Write(header), run_time=0.5)

        # Build 2×2 card grid
        cards = [_takeaway_card(*t) for t in _TAKEAWAYS]
        grid  = VGroup(
            VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.4),
            VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.35).center().shift(DOWN * 0.2)

        for i, card in enumerate(cards):
            self.play(FadeIn(card, shift=UP * 0.08), run_time=0.4)
            self.wait(0.3)

        self.wait(0.5)

        # CAR mascot wave
        car = create_car_mascot(height=1.4)
        car.to_corner(DR, buff=0.4)
        self.play(FadeIn(car, shift=LEFT * 0.2), run_time=0.4)
        self.play(idle_bounce(car, amplitude=0.1, run_time=0.9))

        # "See you in Part 02" note
        see_you = Text(
            "Next: Part 02 — Collective Intelligence (V2X)",
            font_size=18, color=COL_LIGHT_BLUE,
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(see_you), run_time=0.4)
        self.wait(2.0)

        self.play(FadeOut(VGroup(header, grid, car, see_you)), run_time=0.6)
        self.wait(0.2)
