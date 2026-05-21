# beyond/scenes/part01/p01_s09_takeaways.py — Part 1 summary + bridge
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components import (
    BeyondScene, bullet_reveal, key_insight_reveal,
    P1_FOUNDATION, P2_COOP, GOLD, TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P01S09Takeaways(BeyondScene):
    PART_COLOR = P1_FOUNDATION

    def construct(self):
        title_mob, sep = self.open("Part 1 — What We Learned")
        self.wait(0.2)

        items = [
            "Foundation Models generalize to autonomous driving",
            "Long-tail edge cases require contextual reasoning",
            "E2E > Modular: joint optimization, no error cascade",
            "VLA: Vision-Language-Action unifies perception + planning",
            "AutoVLA: dynamic mode switching handles complexity",
        ]
        bullets_grp, bullets_anim = bullet_reveal(
            items, accent_color=P1_FOUNDATION, font_size=SIZE_LABEL - 3
        )
        bullets_grp.move_to(UP * 0.6)
        self.play(bullets_anim)
        self.wait(0.6)

        key_insight_reveal(
            self,
            "One smart car sees far.\nBut it still can't see around corners.",
            hold=2.2,
        )

        bridge = VGroup(
            Text("Collaboration is the missing piece.", font_size=SIZE_LABEL - 1,
                 color=TEXT_WHITE, font=FONT_PRIMARY),
            Text("→ Part 2: Cooperative Perception",
                 font_size=SIZE_LABEL, color=P2_COOP,
                 font=FONT_PRIMARY, weight=BOLD),
        ).arrange(DOWN, buff=0.22)
        bridge.to_edge(DOWN, buff=0.48)
        self.play(
            LaggedStart(*[FadeIn(ln, shift=UP * 0.08, run_time=0.35)
                          for ln in bridge], lag_ratio=0.3),
        )
        self.wait(1.5)
        self.close()
