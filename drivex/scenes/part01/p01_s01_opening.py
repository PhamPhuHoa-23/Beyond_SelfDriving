# drivex/scenes/part01/p01_s01_opening.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-01: Opening Question  (~30s)
#
# Spec: spec_intro_part01.md → SCENE 1-01
# Large question text + PI mascot with two speech bubbles:
#   "AI đang ở đâu?"  and  "AV đang ở đâu?"
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    COL_NAVY, COL_BLUE, COL_WHITE, COL_LIGHT_BLUE,
    COL_GOLD, BG_DARK,
)
from drivex.components.mascots import create_pi_mascot, idle_bounce
from drivex.components.thought_bubble import PIBubble


class P01S01Opening(Scene):
    """SCENE 1-01 — Opening Question"""

    def construct(self):
        self.camera.background_color = BG_DARK

        # Large question text
        question = Text(
            "Why, in 2025 — with everything AI can do —\n"
            "write code, generate videos, answer any question —\n"
            "why can't self-driving cars just... work everywhere?",
            font_size=30,
            color=COL_WHITE,
            line_spacing=1.4,
        ).center().shift(UP * 0.6)

        # PI mascot on left
        pi = create_pi_mascot(height=1.0)
        pi.to_edge(LEFT, buff=0.8).shift(DOWN * 0.8)

        # Speech bubbles
        bubble1 = PIBubble(pi, "AI đang ở đâu?",
                           position=UP + RIGHT, font_size=20)
        bubble2 = PIBubble(pi, "AV đang ở đâu?",
                           position=RIGHT, font_size=20)

        # Animations
        self.play(Write(question), run_time=1.5)
        self.play(FadeIn(pi, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(bubble1), run_time=0.4)
        self.wait(0.8)
        self.play(
            FadeOut(bubble1),
            FadeIn(bubble2),
            run_time=0.4,
        )
        self.wait(1.0)
        self.play(FadeOut(VGroup(question, pi, bubble2)), run_time=0.5)
        self.wait(0.3)
