"""
Scene 3-14 — Bridge to Part 04
================================
"Infrastructure layer: complete ✓" → PI 3-bubble → CAR response → 3 red bottlenecks.
"""
from drivex.components.thought_bubble import PIBubble, SpeechBubble
from drivex.components.mascots import CarMascot, PiMascot
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P03S14Bridge(Scene):
    """
    A — "Infrastructure layer: complete ✓" banner
    B — PiMascot: 3 problem bubbles
    C — CarMascot: "Part 04: Efficiency"
    D — 3 red bottleneck cards
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        # ═══ Banner ════════════════════════════════════════════════
        banner_box = RoundedRectangle(width=7.0, height=0.85, corner_radius=0.2,
                                      fill_color=COL_GREEN, fill_opacity=1, stroke_width=0)
        banner_txt = Text("Infrastructure Layer: Complete  ✓", font_size=22,
                          color=BG_BLACK, weight=BOLD)
        banner_box.to_edge(UP, buff=0.4)
        banner_txt.move_to(banner_box.get_center())
        self.play(FadeIn(VGroup(banner_box, banner_txt)), run_time=0.4)

        # ═══ Mascots ══════════════════════════════════════════════
        pi = PiMascot(height=1.0).to_corner(DL, buff=0.5)
        car = CarMascot(height=1.1).to_corner(DR, buff=0.5)
        self.play(FadeIn(pi), FadeIn(car), run_time=0.3)

        # PI: 3 problem bubbles (sequential)
        problems = [
            "Annotation cost?",
            "Training convergence?",
            "Edge compute budget?",
        ]
        for prob in problems:
            bbl = PIBubble(pi, prob, position=UR)
            self.play(FadeIn(bbl), run_time=0.25)
            self.wait(0.4)
            self.play(FadeOut(bbl), run_time=0.2)

        # CAR response
        car_bbl = SpeechBubble(car,
                               "Data efficiency.\nTraining efficiency.\nInference efficiency.\n— Part 04",
                               position=UL)
        self.play(FadeIn(car_bbl), run_time=0.3)
        self.wait(0.5)
        self.play(FadeOut(car_bbl), run_time=0.2)

        # ═══ 3 Red Bottleneck Cards ═══════════════════════════════
        bottlenecks = [
            "Annotation\nCost",
            "Training\nConvergence",
            "Edge Compute\nBudget",
        ]
        cards = []
        for txt in bottlenecks:
            card_bg = RoundedRectangle(width=2.4, height=1.1, corner_radius=0.18,
                                       fill_color=COL_RED, fill_opacity=1, stroke_width=0)
            card_txt = Text(txt, font_size=13, color=COL_WHITE, weight=BOLD)
            card_txt.move_to(card_bg.get_center())
            cards.append(VGroup(card_bg, card_txt))

        card_row = VGroup(*cards).arrange(RIGHT, buff=0.45).move_to(UP * 0.6)
        self.play(*[FadeIn(c) for c in cards], run_time=0.4)

        # "Part 04" pointer arrow
        part4_lbl = Text("→  Part 04: Efficiency",
                         font_size=18, color=COL_GOLD, weight=BOLD)
        part4_lbl.next_to(card_row, DOWN, buff=0.5)
        self.play(Write(part4_lbl), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
