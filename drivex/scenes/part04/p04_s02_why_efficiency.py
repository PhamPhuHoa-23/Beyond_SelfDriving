"""
Scene 4-02 — Why Efficiency Matters in V2X
============================================
V2X "borrowing eyes" diagram → US DoT badge →
3 question cards (Data / Training / Inference).
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P04S02WhyEfficiency(Scene):
    """
    A — V2X concept diagram (two agents + infra node)
    B — US DoT badge
    C — Three question cards (01 Data / 02 Training / 03 Inference)
    """

    def construct(self):
        self.camera.background_color = "#0F172A"

        heading = Text("Why Efficiency Matters in V2X", font_size=22, color=COL_GOLD,
                       weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ SECTION A: V2X diagram ════════════════════════════════
        car1 = RoundedRectangle(width=0.9, height=0.5, corner_radius=0.1,
                                fill_color=COL_BLUE, fill_opacity=1, stroke_width=0)
        car2 = RoundedRectangle(width=0.9, height=0.5, corner_radius=0.1,
                                fill_color=COL_BLUE, fill_opacity=1, stroke_width=0)
        inf = Square(side_length=0.4, fill_color=COL_INFRA_ORANGE, fill_opacity=1,
                     stroke_width=0).rotate(PI / 4)

        car1.move_to(LEFT * 3.2 + UP * 1.2)
        car2.move_to(RIGHT * 2.8 + UP * 1.2)
        inf.move_to(ORIGIN + UP * 1.2)

        lbl1 = Text("CAV 1", font_size=10, color=COL_BLUE)
        lbl2 = Text("CAV 2", font_size=10, color=COL_BLUE)
        lbli = Text("INF",   font_size=10, color=COL_INFRA_ORANGE)
        lbl1.next_to(car1, DOWN, buff=0.06)
        lbl2.next_to(car2, DOWN, buff=0.06)
        lbli.next_to(inf,  DOWN, buff=0.06)

        comm1 = DashedLine(car1.get_right(), inf.get_left(),
                           color=COL_LIGHT_BLUE, dash_length=0.15, stroke_width=1.2)
        comm2 = DashedLine(car2.get_left(),  inf.get_right(),
                           color=COL_LIGHT_BLUE, dash_length=0.15, stroke_width=1.2)

        v2x_grp = VGroup(car1, car2, inf, lbl1, lbl2, lbli, comm1, comm2)
        self.play(FadeIn(v2x_grp), run_time=0.5)

        # DoT badge
        dot_box = RoundedRectangle(width=3.8, height=0.55, corner_radius=0.12,
                                   fill_color="#1E3A5F", fill_opacity=1,
                                   stroke_color=COL_BLUE, stroke_width=1.5)
        dot_txt = Text("US DoT — Smart Intersection Program",
                       font_size=11, color=COL_WHITE)
        dot_box.next_to(v2x_grp, DOWN, buff=0.2)
        dot_txt.move_to(dot_box.get_center())
        self.play(FadeIn(VGroup(dot_box, dot_txt)), run_time=0.3)
        self.wait(0.3)

        # ═══ SECTION B: Scale down top, reveal 3 questions ═════════
        self.play(VGroup(v2x_grp, dot_box, dot_txt).animate.scale(0.7).to_edge(UP, buff=1.2),
                  run_time=0.4)

        questions = [
            ("01", "Data:  annotation doesn't scale"),
            ("02", "Training:  months of compute"),
            ("03", "Inference:  edge hardware limits"),
        ]
        q_items = []
        for num, text in questions:
            card = RoundedRectangle(width=7.5, height=0.65, corner_radius=0.12,
                                    fill_color="#1E3A5F", fill_opacity=1,
                                    stroke_color=COL_BLUE, stroke_width=1.2)
            num_txt = Text(num, font_size=22, color=COL_GOLD, weight=BOLD)
            q_txt = Text(text, font_size=16, color=COL_WHITE)
            num_txt.move_to(card.get_left() + RIGHT * 0.5)
            q_txt.move_to(card.get_center() + RIGHT * 0.3)
            q_items.append(VGroup(card, num_txt, q_txt))

        q_col = VGroup(*q_items).arrange(DOWN, buff=0.25).move_to(DOWN * 0.9)
        for q in q_items:
            self.play(FadeIn(q), run_time=0.3)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
