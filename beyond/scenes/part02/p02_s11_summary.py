# beyond/scenes/part02/p02_s11_summary.py — P2 summary + bridge to Part 3
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components import (
    BeyondScene, bullet_reveal,
    P2_COOP, P3_SIM, GOLD, TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P02S11Summary(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("Part 2 — Key Takeaways")
        self.wait(0.2)

        items = [
            "Single-agent E2E AI is limited by line-of-sight",
            "V2X cooperation = physics solution to occlusion",
            "V2XPnP: multi-agent × multi-frame × multi-task",
            "TurboTrain: 120 epochs → 45 epochs automated",
            "RiskMap: risk fields as a shared language",
        ]
        bullets_grp, bullets_anim = bullet_reveal(
            items, accent_color=P2_COOP, font_size=SIZE_LABEL - 3,
        )
        bullets_grp.move_to(UP * 0.5)
        self.play(bullets_anim)
        self.wait(0.5)

        bridge = VGroup(
            Text("But all this still needs real-world data...",
                 font_size=SIZE_LABEL - 1, color=TEXT_DIM, font=FONT_PRIMARY),
            Text("How do we bridge simulation and reality?",
                 font_size=SIZE_LABEL - 1, color=P3_SIM, font=FONT_PRIMARY),
            Text("→ Part 3", font_size=SIZE_LABEL,
                 color=P3_SIM, font=FONT_PRIMARY, weight=BOLD),
        ).arrange(DOWN, buff=0.20)
        bridge.to_edge(DOWN, buff=0.50)
        self.play(
            LaggedStart(*[FadeIn(ln, shift=UP * 0.08, run_time=0.35)
                          for ln in bridge], lag_ratio=0.25),
        )
        self.wait(1.5)
        self.close()
