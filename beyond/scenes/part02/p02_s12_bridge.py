# beyond/scenes/part02/p02_s12_bridge.py — Part 2 → Part 3 bridge
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components import (
    BeyondScene, key_insight_reveal,
    P2_COOP, P3_SIM, GOLD, TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P02S12Bridge(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("Part 2 — What Comes Next?")
        self.wait(0.2)

        # Summary of what Part 2 achieved
        achieved = VGroup(
            Text("✓  V2X cooperation solves occlusion", font_size=SIZE_LABEL - 2,
                 color=TEXT_WHITE, font=FONT_PRIMARY),
            Text("✓  V2XPnP: unified multi-task framework", font_size=SIZE_LABEL - 2,
                 color=TEXT_WHITE, font=FONT_PRIMARY),
            Text("✓  TurboTrain: automated training pipeline", font_size=SIZE_LABEL - 2,
                 color=TEXT_WHITE, font=FONT_PRIMARY),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(UP * 0.8)

        self.play(
            LaggedStart(*[FadeIn(ln, shift=RIGHT * 0.10, run_time=0.32)
                          for ln in achieved], lag_ratio=0.20),
        )
        self.wait(0.5)

        key_insight_reveal(
            self,
            "We can cooperate in simulation.\nBut does it hold in the real world?",
            hold=2.0,
        )

        bridge = VGroup(
            Text("Real data. Real sensors. Real gaps.",
                 font_size=SIZE_LABEL - 1, color=TEXT_DIM, font=FONT_PRIMARY),
            Text("→ Part 3: Bridging Sim and Reality",
                 font_size=SIZE_LABEL, color=P3_SIM,
                 font=FONT_PRIMARY, weight=BOLD),
        ).arrange(DOWN, buff=0.22)
        bridge.to_edge(DOWN, buff=0.48)
        self.play(
            LaggedStart(*[FadeIn(ln, shift=UP * 0.08, run_time=0.35)
                          for ln in bridge], lag_ratio=0.30),
        )
        self.wait(1.5)
        self.close()
