# beyond/scenes/part03/p03_s14_bridge.py — Part 3 → Part 4 bridge
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components import (
    BeyondScene, bullet_reveal, key_insight_reveal,
    P3_SIM, P4_EFFICIENT, GOLD, TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P03S14Bridge(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("Part 3 — Sim to Reality: What We Built")
        self.wait(0.2)

        items = [
            "UCLA Smart Intersection: real V2X testbed",
            "Temporal + spatial calibration solved",
            "Kalman filter fusion: 100Hz lane-level accuracy",
            "CooperFuse: uncertainty-aware bbox fusion",
            "Digital Twin: real-time synchronized environment",
        ]
        bullets_grp, bullets_anim = bullet_reveal(
            items, accent_color=P3_SIM, font_size=SIZE_LABEL - 3
        )
        bullets_grp.move_to(UP * 0.6)
        self.play(bullets_anim)
        self.wait(0.5)

        key_insight_reveal(
            self,
            "The gap between sim and real has been bridged.\nBut can we deploy it at scale?",
            hold=2.0,
        )

        bridge = VGroup(
            Text("Communication is too heavy. Training is too slow.",
                 font_size=SIZE_LABEL - 1, color=TEXT_DIM, font=FONT_PRIMARY),
            Text("→ Part 4: Building Efficient V2X",
                 font_size=SIZE_LABEL, color=P4_EFFICIENT,
                 font=FONT_PRIMARY, weight=BOLD),
        ).arrange(DOWN, buff=0.22)
        bridge.to_edge(DOWN, buff=0.48)
        self.play(
            LaggedStart(*[FadeIn(ln, shift=UP * 0.08, run_time=0.35)
                          for ln in bridge], lag_ratio=0.30),
        )
        self.wait(1.5)
        self.close()
