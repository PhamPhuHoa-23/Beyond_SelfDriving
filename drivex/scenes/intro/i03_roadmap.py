# drivex/scenes/intro/i03_roadmap.py
# ─────────────────────────────────────────────────────────────────
# SCENE I-03: The 5-Part Journey (Roadmap)  (~30s)
#
# Spec: spec_intro_part01.md → SCENE I-03
#   - NAVY background
#   - Horizontal spine
#   - 5 arc nodes alternating above/below spine
#   - Node labels + short part titles
#   - Nodes pulse, then Part 1 highlights gold
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    COL_NAVY, COL_BLUE, COL_GOLD, COL_WHITE, COL_LIGHT_BLUE,
)
from drivex.components.roadmap import RoadmapStrip

PART_TITLES_LONG = [
    "Individual Reasoning\n(Foundation Models)",
    "Collective Intelligence\n(Cooperative V2X)",
    "Sim-to-Real Bridge",
    "Efficiency &\nOnline Adaptation",
    "Scalable\nPhysical AI",
]


class I03Roadmap(Scene):
    """SCENE I-03 — The 5-Part Journey Roadmap"""

    def construct(self):
        self.camera.background_color = COL_NAVY

        # Header
        header = Text(
            "The 5-Part Journey",
            font_size=30, color=COL_WHITE, weight=BOLD,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(header), run_time=0.4)

        # Build the roadmap using the shared component
        roadmap = RoadmapStrip(current_part=0, mini=False, spine_width=10.5)
        roadmap.shift(DOWN * 0.3)

        # Animate the roadmap drawing in
        self.play(roadmap.build_animation())
        self.wait(0.4)

        # All nodes pulse
        pulse_anims = [
            Succession(
                roadmap.nodes[i][0].animate(
                    rate_func=there_and_back, run_time=0.3
                ).scale(1.2),
            )
            for i in range(5)
        ]
        self.play(LaggedStart(*pulse_anims, lag_ratio=0.12))
        self.wait(0.3)

        # Part 1 highlights gold — signals we start here
        p1_circle = roadmap.nodes[0][0]
        self.play(
            p1_circle.animate(run_time=0.4)
                     .set_fill(COL_GOLD)
                     .set_stroke(COL_GOLD),
        )
        self.wait(1.2)

        self.play(FadeOut(VGroup(header, roadmap)), run_time=0.5)
        self.wait(0.2)
