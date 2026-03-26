"""
Scene 4-10 — Bridge to Part 05: Humans Enter the Equation
==========================================================
Checkmarks for data/training/inference efficiency, then expanding agent types,
human figure icons, and a tease toward Part 05.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *

INT8_GREEN = "#2ECC71"


def _small_human(color=WHITE):
    """Stick figure: circle head + body + legs."""
    head  = Circle(radius=0.12, fill_color=color, fill_opacity=1, stroke_width=0)
    body  = Line(ORIGIN, DOWN * 0.35, stroke_color=color, stroke_width=2)
    leg_l = Line(ORIGIN, DL * 0.22, stroke_color=color, stroke_width=2)
    leg_r = Line(ORIGIN, DR * 0.22, stroke_color=color, stroke_width=2)
    body.move_to(head.get_bottom() + DOWN * 0.175)
    leg_l.move_to(body.get_bottom())
    leg_r.move_to(body.get_bottom())
    return VGroup(head, body, leg_l, leg_r)


class P04S10Bridge(Scene):

    def construct(self):
        self.camera.background_color = COL_NAVY

        # ── Section A: efficiency checkmarks ──────────────────────
        checks = [
            Text("✓  Data Efficiency",       font_size=22, color=INT8_GREEN, weight=BOLD),
            Text("✓  Training Efficiency",   font_size=22, color=INT8_GREEN, weight=BOLD),
            Text("✓  Inference Efficiency",  font_size=22, color=INT8_GREEN, weight=BOLD),
        ]
        for i, ck in enumerate(checks):
            ck.move_to(LEFT * 3.5 + UP * (1 - i * 0.8))

        for ck in checks:
            self.play(Write(ck), run_time=0.35)

        infra_lbl = Text("Cars + Infrastructure", font_size=20, color=COL_LIGHT_BLUE)
        infra_lbl.next_to(checks[-1], DOWN, buff=0.5).align_to(checks[0], LEFT)
        self.play(Write(infra_lbl), run_time=0.3)
        self.wait(0.5)

        # ── Section B: expanding agent types ──────────────────────
        sec_title = Text("But who else is on the road?", font_size=22, color=COL_WHITE)
        sec_title.to_edge(UP, buff=0.5)
        self.play(Write(sec_title), run_time=0.3)

        # Simple agent shapes centred on right side
        # Car (rectangle)
        car_rect = Rectangle(width=0.8, height=0.4, fill_color=COL_BLUE,
                              fill_opacity=1, stroke_color=COL_WHITE, stroke_width=1.5)
        car_lbl  = Text("Car", font_size=12, color=COL_WHITE)
        car_lbl.next_to(car_rect, DOWN, buff=0.06)
        car_group = VGroup(car_rect, car_lbl).move_to(RIGHT * 2.5)

        # Robot (taller rect)
        rob_rect = Rectangle(width=0.5, height=0.7, fill_color="#5D6D7E",
                              fill_opacity=1, stroke_color=COL_WHITE, stroke_width=1.5)
        rob_lbl  = Text("Robot", font_size=12, color=COL_WHITE)
        rob_lbl.next_to(rob_rect, DOWN, buff=0.06)
        rob_group = VGroup(rob_rect, rob_lbl).move_to(RIGHT * 4.0 + UP * 0.3)

        # Wheelchair (circle + small rect)
        wc_circ = Circle(radius=0.22, fill_color="#7F8C8D", fill_opacity=1,
                          stroke_color=COL_WHITE, stroke_width=1.5)
        wc_seat = Rectangle(width=0.28, height=0.18, fill_color="#7F8C8D",
                             fill_opacity=1, stroke_color=COL_WHITE, stroke_width=1)
        wc_seat.next_to(wc_circ, UP, buff=0.0)
        wc_lbl  = Text("Wheelchair", font_size=12, color=COL_WHITE)
        wc_lbl.next_to(wc_circ, DOWN, buff=0.06)
        wc_group = VGroup(wc_circ, wc_seat, wc_lbl).move_to(RIGHT * 1.5 + DOWN * 1.0)

        # Scooter (small rect + circles)
        sc_body = Rectangle(width=0.6, height=0.25, fill_color=COL_GREEN,
                             fill_opacity=1, stroke_color=COL_WHITE, stroke_width=1.5)
        sc_w1 = Circle(radius=0.1, fill_color=COL_GRAY_FILL, fill_opacity=1,
                        stroke_color=COL_WHITE, stroke_width=1)
        sc_w2 = Circle(radius=0.1, fill_color=COL_GRAY_FILL, fill_opacity=1,
                        stroke_color=COL_WHITE, stroke_width=1)
        sc_w1.next_to(sc_body, DOWN, buff=0.0).align_to(sc_body, LEFT).shift(RIGHT * 0.05)
        sc_w2.next_to(sc_body, DOWN, buff=0.0).align_to(sc_body, RIGHT).shift(LEFT * 0.05)
        sc_lbl = Text("Scooter", font_size=12, color=COL_WHITE)
        sc_lbl.next_to(sc_body, DOWN, buff=0.18)
        sc_group = VGroup(sc_body, sc_w1, sc_w2, sc_lbl).move_to(RIGHT * 3.2 + DOWN * 1.4)

        self.play(FadeIn(car_group), run_time=0.3)
        self.play(FadeIn(rob_group), run_time=0.3)
        self.play(FadeIn(wc_group),  run_time=0.3)
        self.play(FadeIn(sc_group),  run_time=0.3)

        # ── Section C: human figures ───────────────────────────────
        positions = [UL * 0.8, UR * 0.8, DL * 0.5, DR * 0.5, UP * 1.5, DOWN * 1.8 + LEFT * 0.5]
        humans = VGroup(*[_small_human(COL_WHITE).scale(0.65).move_to(p)
                          for p in positions])
        self.play(LaggedStart(*[FadeIn(h) for h in humans], lag_ratio=0.1), run_time=0.7)

        hardest = Text("The hardest variable: the human",
                        font_size=22, color=COL_GOLD, weight=BOLD, slant=ITALIC)
        hardest.to_edge(DOWN, buff=0.8)
        self.play(Write(hardest), run_time=0.4)
        self.wait(0.6)

        # ── Section D: Part 05 reveal ──────────────────────────────
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)

        next_lbl = Text("Part 05", font_size=40, color=COL_GOLD, weight=BOLD)
        sub_lbl  = Text("MetaUrban · UrbanSim · CityWalker",
                         font_size=20, color=COL_LIGHT_BLUE)
        sub_lbl.next_to(next_lbl, DOWN, buff=0.3)
        teaser   = Text("Human-centric mobile intelligence",
                         font_size=18, color=COL_WHITE, slant=ITALIC)
        teaser.next_to(sub_lbl, DOWN, buff=0.2)

        self.play(Write(next_lbl), run_time=0.5)
        self.play(FadeIn(VGroup(sub_lbl, teaser), shift=UP * 0.2), run_time=0.4)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
