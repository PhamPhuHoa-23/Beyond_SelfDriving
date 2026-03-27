"""
Scene 4-09 — Efficiency Summary: Three Solutions
=================================================
3 summary cards: CooPre / TurboTrain / QuantV2X with key results.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P04S09EfficiencySummary(Scene):
    """
    Three horizontal cards: CooPre | TurboTrain | QuantV2X
    Each with mini icon + key result metric.
    """

    def construct(self):
        self.camera.background_color = COL_NAVY

        heading = Text("Three Bottlenecks. Three Solutions.", font_size=24,
                       color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.5)
        self.play(Write(heading), run_time=0.4)

        cards_data = [
            (
                "CooPre",
                "Data Efficiency",
                "50% data = 100% performance",
                COL_BLUE,
                "Multi-agent masked BEV\nreconstruction",
            ),
            (
                "TurboTrain",
                "Training Efficiency",
                "45 vs 120 epochs",
                COL_GREEN,
                "Pretrain + conflict-\nsuppressing fine-tune",
            ),
            (
                "QuantV2X",
                "Inference Efficiency",
                "300× comm compression",
                COL_INT8_GREEN,
                "FP32→INT8 model +\ncodebook communication",
            ),
        ]

        card_objs = []
        for name, subtitle, result, color, desc in cards_data:
            bg = RoundedRectangle(width=3.8, height=3.8, corner_radius=0.22,
                                  fill_color="#1E3A5F", fill_opacity=1,
                                  stroke_color=color, stroke_width=2)
            nm = Text(name, font_size=20, color=COL_GOLD, weight=BOLD)
            st = Text(subtitle, font_size=13, color=color)
            res = Text(result, font_size=14, color=COL_INT8_GREEN, weight=BOLD)
            ds = Text(desc, font_size=11, color=COL_WHITE, slant=ITALIC)

            nm.move_to(bg.get_center() + UP * 1.4)
            st.next_to(nm, DOWN, buff=0.12)
            res.next_to(st, DOWN, buff=0.28)
            ds.next_to(res, DOWN, buff=0.22)

            card_objs.append(VGroup(bg, nm, st, res, ds))

        card_row = VGroup(*card_objs).arrange(RIGHT,
                                              buff=0.45).move_to(DOWN * 0.3)
        con_arrows = []
        for i in range(len(card_objs) - 1):
            arr = Arrow(card_objs[i].get_right(), card_objs[i + 1].get_left(),
                        buff=0.05, color=COL_BLUE, stroke_width=2, tip_length=0.14)
            con_arrows.append(arr)

        for i, card in enumerate(card_objs):
            self.play(FadeIn(card), run_time=0.4)
            if i < len(con_arrows):
                self.play(GrowArrow(con_arrows[i]), run_time=0.2)

        # Bottom tagline
        tagline = Text("Edge-deployable V2X cooperative perception stack",
                       font_size=17, color=COL_GOLD, slant=ITALIC, weight=BOLD)
        tagline.to_edge(DOWN, buff=0.5)
        self.play(Write(tagline), run_time=0.4)

        # Pulse all cards
        self.play(*[card[0].animate.set_stroke(width=4)
                  for card in card_objs], run_time=0.3)
        self.play(*[card[0].animate.set_stroke(width=2)
                  for card in card_objs], run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
