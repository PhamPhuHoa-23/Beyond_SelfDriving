"""
Scene 2-12 — Bridge to Part 03
================================
Simulation panel vs Reality panel, with a GOLD bridge arc.
CAR mascot: "Sim-to-Real. Let's go."
"""
from drivex.components.thought_bubble import SpeechBubble
from drivex.components.mascots import CarMascot, idle_bounce
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P02S12Bridge(Scene):
    """
    Left panel: Simulation world (grid roads, coloured boxes).
    Right panel: Reality (placeholder image-style rectangle).
    Bridge arc in GOLD + GAP label → "Part 03: Bridging Sim and Reality".
    """

    def construct(self):
        self.camera.background_color = COL_NAVY

        # ── sim panel ──────────────────────────────────────────────
        sim_box = RoundedRectangle(
            width=4.5, height=3.2, corner_radius=0.18,
            fill_color="#1A2A3A", fill_opacity=1,
            stroke_color=COL_BLUE, stroke_width=2
        )
        sim_box.move_to(LEFT * 3.5 + UP * 0.3)
        sim_lbl = Text("Simulation", font_size=18, color=COL_BLUE, weight=BOLD)
        sim_lbl.next_to(sim_box, UP, buff=0.15)

        # road grid inside sim box
        road_h = Line(sim_box.get_left() + RIGHT * 0.3, sim_box.get_right() + LEFT * 0.3,
                      color=COL_WHITE, stroke_opacity=0.4)
        road_v = Line(sim_box.get_top() + DOWN * 0.3, sim_box.get_bottom() + UP * 0.3,
                      color=COL_WHITE, stroke_opacity=0.4)
        road_h.move_to(sim_box.get_center())
        road_v.move_to(sim_box.get_center())

        building1 = Rectangle(width=0.7, height=0.6,
                              fill_color="#2A3A4A", fill_opacity=1, stroke_width=0)
        building2 = Rectangle(width=0.5, height=0.8,
                              fill_color="#2A3A4A", fill_opacity=1, stroke_width=0)
        building1.move_to(sim_box.get_center() + UL * 0.6)
        building2.move_to(sim_box.get_center() + DR * 0.5)

        sim_car = Dot(radius=0.12, color=COL_BLUE).move_to(
            sim_box.get_center() + UR * 0.3)
        sim_full = VGroup(sim_box, sim_lbl, road_h, road_v,
                          building1, building2, sim_car)

        # ── real panel ─────────────────────────────────────────────
        real_box = RoundedRectangle(
            width=4.5, height=3.2, corner_radius=0.18,
            fill_color="#1A1A1A", fill_opacity=1,
            stroke_color=COL_GREEN, stroke_width=2
        )
        real_box.move_to(RIGHT * 3.5 + UP * 0.3)
        real_lbl = Text("Reality", font_size=18, color=COL_GREEN, weight=BOLD)
        real_lbl.next_to(real_box, UP, buff=0.15)

        real_placeholder = Rectangle(
            width=3.8, height=2.2,
            fill_color="#2A2A2A", fill_opacity=1, stroke_width=0
        )
        real_placeholder.move_to(real_box.get_center())
        real_ph_lbl = Text("[real road photo]", font_size=14,
                           color=GREY_B, slant=ITALIC)
        real_ph_lbl.move_to(real_placeholder.get_center())
        real_full = VGroup(real_box, real_lbl, real_placeholder, real_ph_lbl)

        self.play(FadeIn(sim_full), run_time=0.5)
        self.play(FadeIn(real_full), run_time=0.5)

        # ── bridge arc + GAP label ────────────────────────────────
        bridge = ArcBetweenPoints(
            sim_box.get_right() + UP * 0.5,
            real_box.get_left() + UP * 0.5,
            angle=-PI / 3,
            color=COL_GOLD, stroke_width=4
        )
        gap_lbl = Text("GAP  ⟺", font_size=18, color=COL_RED, weight=BOLD)
        gap_lbl.move_to(ORIGIN + UP * 1.8)

        self.play(Create(bridge), FadeIn(gap_lbl), run_time=0.6)

        # ── Part 03 label ──────────────────────────────────────────
        p03_lbl = Text("Part 03: Bridging Sim and Reality",
                       font_size=24, color=COL_GOLD, weight=BOLD)
        p03_lbl.to_edge(DOWN, buff=1.2)
        self.play(Write(p03_lbl), run_time=0.6)

        # ── CAR mascot ─────────────────────────────────────────────
        car = CarMascot(height=1.0)
        car.to_corner(DR, buff=0.5)
        bubble = SpeechBubble(car, "Sim-to-Real.\nLet's go.", position=UP)
        self.play(FadeIn(car), run_time=0.4)
        self.play(FadeIn(bubble), run_time=0.3)
        self.play(idle_bounce(car, 0.07, 1.0), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
