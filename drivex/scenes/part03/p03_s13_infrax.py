"""
Scene 3-13 — OpenCDA-InfraX
==============================
2×2 feature card grid + arrow pointing to "Training Data".
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P03S13InfraX(Scene):
    """
    2×2 feature card grid (Flexible Sensor Config / Multi-Modal /
    Weather Variation / Vector Maps) → arrow → "Training Data"
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("OpenCDA-InfraX", font_size=28, color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.5)
        self.play(FadeIn(heading), run_time=0.3)

        features = [
            ("Flexible\nSensor Config",  COL_SENSOR_CYAN),
            ("Multi-Modal\nFusion",       COL_INFRA_ORANGE),
            ("Weather\nVariation",        COL_BLUE),
            ("Vector\nMaps",              COL_GREEN),
        ]

        cards = []
        for title, color in features:
            card_bg  = RoundedRectangle(width=2.5, height=1.3, corner_radius=0.2,
                                         fill_color=color, fill_opacity=0.25,
                                         stroke_color=color, stroke_width=2)
            card_txt = Text(title, font_size=14, color=color, weight=BOLD)
            card_txt.move_to(card_bg.get_center())
            cards.append(VGroup(card_bg, card_txt))

        grid = VGroup(
            VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.4),
            VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.4).move_to(LEFT * 1.5 + DOWN * 0.2)

        self.play(*[FadeIn(c) for c in cards], run_time=0.5)

        # Arrow → "Training Data"
        arrow = Arrow(grid.get_right(), grid.get_right() + RIGHT * 2.2,
                       buff=0.1, color=COL_GOLD, stroke_width=2.5, tip_length=0.2)
        td_lbl = Text("Training\nData", font_size=16, color=COL_GOLD, weight=BOLD)
        td_lbl.next_to(arrow, RIGHT, buff=0.1)

        self.play(Create(arrow), FadeIn(td_lbl), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
