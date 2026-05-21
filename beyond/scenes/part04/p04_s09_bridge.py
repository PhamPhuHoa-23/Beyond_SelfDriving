# beyond/scenes/part04/p04_s09_bridge.py — Part 4 → Part 5 bridge
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components import (
    BeyondScene, bullet_reveal, key_insight_reveal,
    P4_EFFICIENT, P5_PHYSICAL, GOLD, TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P04S09Bridge(BeyondScene):
    PART_COLOR = P4_EFFICIENT

    def construct(self):
        title_mob, sep = self.open("Part 4 — Efficiency Achieved")
        self.wait(0.2)

        items = [
            "CooPre: 50% labels → same or better performance",
            "TurboTrain: automated multi-task training pipeline",
            "QuantV2X: 300× bandwidth reduction, real-time V2X",
            "End-to-end latency < 100ms on edge hardware",
        ]
        bullets_grp, bullets_anim = bullet_reveal(
            items, accent_color=P4_EFFICIENT, font_size=SIZE_LABEL - 3
        )
        bullets_grp.move_to(UP * 0.6)
        self.play(bullets_anim)
        self.wait(0.5)

        key_insight_reveal(
            self,
            "Efficient V2X is ready for cars.\nBut what about everything else?",
            hold=2.0,
        )

        bridge = VGroup(
            Text("Delivery robots. Wheelchairs. Pedestrians.",
                 font_size=SIZE_LABEL - 1, color=TEXT_DIM, font=FONT_PRIMARY),
            Text("Who models the humans in the loop?",
                 font_size=SIZE_LABEL - 1, color=TEXT_WHITE, font=FONT_PRIMARY),
            Text("→ Part 5: Scalable Physical AI",
                 font_size=SIZE_LABEL, color=P5_PHYSICAL,
                 font=FONT_PRIMARY, weight=BOLD),
        ).arrange(DOWN, buff=0.22)
        bridge.to_edge(DOWN, buff=0.45)
        self.play(
            LaggedStart(*[FadeIn(ln, shift=UP * 0.08, run_time=0.35)
                          for ln in bridge], lag_ratio=0.28),
        )
        self.wait(1.5)
        self.close()
