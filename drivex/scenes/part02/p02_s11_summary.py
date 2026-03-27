"""
Scene 2-11 — Summary: Three Problems, Three Solutions
======================================================
V2XPnP → TurboTrain → RiskMap as a coherent cooperative E2E stack.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P02S11Summary(Scene):
    """
    Three horizontally-arranged cards, connected by arrows.
    Bottom label: "Cooperative E2E AD Stack".
    """

    CARDS = [
        ("V2XPnP",     "Dataset + What/When/How\nspatio-temporal fusion framework",
         [LEFT * 0.3 + DOWN * 0.3, RIGHT * 0.3 + DOWN * 0.3,   # two agent dots
          UP * 0.3]),                                             # arc above
        ("TurboTrain", "2-stage: Pretrain + Balance\nReplaces manual 4-stage pipeline"),
        ("RiskMap",    "Interpretable planning\nvia Risk Map middleware"),
    ]

    def _agent_icon(self):
        """Two dots connected by a short arc — V2XPnP icon."""
        d1 = Dot(radius=0.1, color=COL_BLUE)
        d2 = Dot(radius=0.1, color=COL_PURPLE)
        VGroup(d1, d2).arrange(RIGHT, buff=0.5)
        arc = ArcBetweenPoints(d1.get_center(), d2.get_center(),
                               angle=PI / 2, color=COL_BLUE, stroke_width=2)
        return VGroup(d1, d2, arc)

    def _pipeline_icon(self):
        """Two-step pipeline arrow — TurboTrain icon."""
        b1 = Rectangle(width=0.5, height=0.35,
                       fill_color="#1E3A5F", fill_opacity=1, stroke_width=0)
        b2 = Rectangle(width=0.5, height=0.35,
                       fill_color="#1B4332", fill_opacity=1, stroke_width=0)
        arr = Arrow(b1.get_right(), b2.get_left(), buff=0.05, stroke_width=2, color=COL_WHITE,
                    max_tip_length_to_length_ratio=0.3)
        VGroup(b1, arr, b2).arrange(RIGHT, buff=0.1)
        return VGroup(b1, arr, b2)

    def _riskmap_icon(self):
        """Small heatmap grid — RiskMap icon."""
        grid = VGroup()
        colors = [COL_GREEN, COL_GOLD, COL_RED, COL_GREEN, COL_GOLD, COL_RED,
                  COL_GREEN, COL_GREEN, COL_GOLD]
        for i in range(9):
            cell = Rectangle(width=0.25, height=0.25,
                             fill_color=colors[i], fill_opacity=0.8, stroke_width=0)
            grid.add(cell)
        grid.arrange_in_grid(rows=3, cols=3, buff=0.02)
        return grid

    def construct(self):
        self.camera.background_color = COL_NAVY

        header = Text("Three Problems — Three Solutions",
                      font_size=26, color=COL_GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header), run_time=0.4)

        icons = [self._agent_icon(), self._pipeline_icon(),
                 self._riskmap_icon()]
        card_titles = ["V2XPnP",    "TurboTrain",
                       "RiskMap"]
        card_bodies = [
            "Dataset + What/When/How\nspatio-temporal fusion",
            "2-stage: Pretrain + Balance\n( <½ compute of manual 4-stage )",
            "Interpretable planning\nvia Risk Map middleware",
        ]

        cards = VGroup()
        for i, (title, body) in enumerate(zip(card_titles, card_bodies)):
            card_box = RoundedRectangle(
                width=3.8, height=4.0, corner_radius=0.2,
                fill_color="#182030", fill_opacity=1,
                stroke_color=COL_BLUE, stroke_width=2
            )
            t_title = Text(title, font_size=20, color=COL_GOLD, weight=BOLD)
            t_body = Text(body,  font_size=13, color=COL_WHITE)
            icon = icons[i].scale_to_fit_width(1.2)
            content = VGroup(icon, t_title, t_body).arrange(DOWN, buff=0.22)
            content.move_to(card_box.get_center())
            cards.add(VGroup(card_box, content))

        cards.arrange(RIGHT, buff=0.5)
        cards.move_to(DOWN * 0.3)

        connecting_arrows = VGroup(
            Arrow(cards[0].get_right(), cards[1].get_left(),
                  color=COL_BLUE, buff=0.05),
            Arrow(cards[1].get_right(), cards[2].get_left(),
                  color=COL_BLUE, buff=0.05),
        )

        self.play(FadeIn(cards[0]), run_time=0.5)
        self.play(GrowArrow(connecting_arrows[0]), run_time=0.3)
        self.play(FadeIn(cards[1]), run_time=0.5)
        self.play(GrowArrow(connecting_arrows[1]), run_time=0.3)
        self.play(FadeIn(cards[2]), run_time=0.5)

        bottom_lbl = Text("Cooperative End-to-End Autonomous Driving Stack",
                          font_size=18, color=COL_GOLD, slant=ITALIC)
        bottom_lbl.to_edge(DOWN, buff=0.45)
        self.play(Write(bottom_lbl), run_time=0.5)

        # all three cards pulse
        self.play(
            cards.animate.scale(1.03),
            rate_func=there_and_back, run_time=0.4
        )
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
