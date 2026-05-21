# beyond/scenes/part05/p05_s08_final_summary.py — Part 5 summary + credits
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components import (
    BeyondScene, bullet_reveal,
    P5_PHYSICAL, GOLD, GOLD_GLOW, TEXT_WHITE, TEXT_DIM, UCLA_GOLD,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P05S08FinalSummary(BeyondScene):
    PART_COLOR = P5_PHYSICAL

    def construct(self):
        title_mob, sep = self.open("Part 5 — Physical AI for Everyone")
        self.wait(0.2)

        items = [
            "MetaUrban: procedural generation → infinite environments",
            "UrbanSim: GPU-native sim, 180 days → 3 hours",
            "CityWalker: 227 cities, 120K+ diverse pedestrians",
            "PedGen: diffusion model for realistic human behavior",
            "Vid2Sim: any city video → trainable simulator",
        ]
        bullets_grp, bullets_anim = bullet_reveal(
            items, accent_color=P5_PHYSICAL, font_size=SIZE_LABEL - 3
        )
        bullets_grp.move_to(UP * 0.6)
        self.play(bullets_anim)
        self.wait(0.6)

        # Final message
        final_msg = VGroup(
            Text("From one smart car", font_size=SIZE_LABEL - 1,
                 color=TEXT_DIM, font=FONT_PRIMARY),
            Text("to a city full of cooperating agents —", font_size=SIZE_LABEL - 1,
                 color=TEXT_WHITE, font=FONT_PRIMARY),
            Text("human, robot, and everything in between.", font_size=SIZE_LABEL - 1,
                 color=P5_PHYSICAL, font=FONT_PRIMARY),
            Text('"Beyond Self-Driving."', font_size=SIZE_LABEL + 4,
                 color=GOLD, font=FONT_PRIMARY, weight=BOLD, slant=ITALIC),
        ).arrange(DOWN, buff=0.22)
        final_msg.to_edge(DOWN, buff=0.42)
        self.play(
            LaggedStart(*[FadeIn(ln, shift=UP * 0.08, run_time=0.35)
                          for ln in final_msg], lag_ratio=0.25),
        )

        # UCLA credit
        ucla_txt = Text("UCLA Mobility Lab  ·  ICCV 2025",
                        font_size=SIZE_MICRO + 1, color=UCLA_GOLD,
                        font=FONT_PRIMARY)
        ucla_txt.to_corner(DR, buff=0.40)
        self.play(FadeIn(ucla_txt, run_time=0.28))
        self.wait(2.0)
        self.close()
