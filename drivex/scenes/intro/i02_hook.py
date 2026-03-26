# drivex/scenes/intro/i02_hook.py
# ─────────────────────────────────────────────────────────────────
# SCENE I-02: The Hook  (~40s)
#
# Spec: spec_intro_part01.md → SCENE I-02
# Three sub-scenes:
#   A: Single car with radar + FM icons → thought bubble
#   B: Wall appears, radar blocked, blind zone visible
#   C: 2 more cars, communication arcs, wall disappears,
#      hidden object now visible
# Bookended by the core quote lines.
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import (
    BG_BLACK, COL_BLUE, COL_GOLD, COL_WHITE,
    COL_RED, COL_GREEN,
)


class I02Hook(Scene):
    """SCENE I-02 — The Hook (visual essay on cooperation)"""

    def construct(self):
        self.camera.background_color = BG_BLACK

        # ═══════════════════════════════════════════════════════
        # Part 1: Quote delivery
        # ═══════════════════════════════════════════════════════
        q1 = Text("We gave cars eyes to see,",
                  font_size=32, color=COL_WHITE).shift(UP * 1.4)
        q2 = Text("and Foundation Models to reason —",
                  font_size=32, color=COL_WHITE).next_to(q1, DOWN, buff=0.25)
        q3 = Text("but even the smartest agent",
                  font_size=28, color=COL_WHITE).next_to(q2, DOWN, buff=0.2)
        q4 = Text("cannot see through walls.",
                  font_size=28, color=COL_WHITE, weight=BOLD).next_to(q3, DOWN, buff=0.15)

        self.play(Write(q1), run_time=1.0)
        self.play(Write(q2), run_time=1.0)
        self.play(Write(q3), Write(q4), run_time=1.2)
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════
        # Transition: quotes fade, sub-scene A begins
        # ═══════════════════════════════════════════════════════
        self.play(FadeOut(VGroup(q1, q2, q3, q4)), run_time=0.6)

        # ═══════════════════════════════════════════════════════
        # Sub-scene A: Single car, radar, FM, thought bubble
        # ═══════════════════════════════════════════════════════
        car_a = self._make_car(color=COL_BLUE).shift(LEFT * 2.5)

        self.play(FadeIn(car_a), run_time=0.5)

        # Radar sweep arcs
        radar_arcs = self._make_radar(car_a.get_right(), color=COL_BLUE)
        self.play(Create(radar_arcs), run_time=1.5)

        # Detection dots appear as sweep passes
        det_dots = VGroup(*[
            Dot(radius=0.1, color=COL_GREEN).move_to(
                car_a.get_right() + RIGHT * (1.2 + i * 0.5) + UP * ((i - 2) * 0.3)
            )
            for i in range(5)
        ])
        self.play(LaggedStart(
            *[FadeIn(d) for d in det_dots], lag_ratio=0.15
        ), run_time=0.8)

        # FM icons (small labeled boxes near car)
        fm1 = self._fm_icon("GPT").next_to(car_a, UP + LEFT, buff=0.15).scale(0.6)
        fm2 = self._fm_icon("VLM").next_to(fm1, RIGHT, buff=0.15).scale(0.6)
        self.play(FadeIn(fm1), FadeIn(fm2), run_time=0.4)

        # Thought bubble
        think_box = self._thought_box(
            car_a, "There is a human\nover there.\n→ Turn left."
        )
        self.play(FadeIn(think_box, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════
        # Sub-scene B: Wall appears, radar blocked, blind zone
        # ═══════════════════════════════════════════════════════
        wall = Rectangle(
            width=0.5, height=2.2,
            fill_color="#555555", fill_opacity=1,
            stroke_color=COL_WHITE, stroke_width=2,
        ).move_to(RIGHT * 0.8)

        self.play(FadeOut(think_box),
                  FadeOut(radar_arcs),
                  FadeOut(det_dots), run_time=0.3)
        self.play(FadeIn(wall, shift=LEFT * 0.2), run_time=0.5)

        # Blocked radar arcs (truncated at wall)
        blocked = self._make_radar_blocked(car_a.get_right(), wall_x=0.55)
        self.play(Create(blocked), run_time=1.2)

        # Blind zone polygon
        blind_zone = Polygon(
            car_a.get_right() + RIGHT * 0.1,
            wall.get_top() + RIGHT * 0.25,
            wall.get_top() + RIGHT * 3.5,
            wall.get_bottom() + RIGHT * 3.5,
            wall.get_bottom() + RIGHT * 0.25,
            fill_color=COL_RED, fill_opacity=0.18,
            stroke_width=0,
        )
        self.play(FadeIn(blind_zone), run_time=0.5)
        self.wait(0.6)

        # ═══════════════════════════════════════════════════════
        # Sub-scene C: Multi-agent cooperation
        # ═══════════════════════════════════════════════════════
        car_b = self._make_car(color=COL_GREEN).scale(0.7).move_to(RIGHT * 3.0 + UP * 1.8)
        car_c = self._make_car(color=COL_GREEN).scale(0.7).move_to(RIGHT * 3.0 + DOWN * 1.8)

        self.play(FadeOut(blind_zone), FadeOut(blocked), run_time=0.3)
        self.play(FadeIn(car_b), FadeIn(car_c), run_time=0.6)

        # Communication arcs between cars (curved dashed lines)
        comm_ab = ArcBetweenPoints(
            car_a.get_right(), car_b.get_left(),
            angle=-TAU / 6,
            stroke_color=COL_BLUE, stroke_width=2,
        )
        comm_ac = ArcBetweenPoints(
            car_a.get_right(), car_c.get_left(),
            angle=TAU / 6,
            stroke_color=COL_BLUE, stroke_width=2,
        )
        self.play(Create(comm_ab), Create(comm_ac), run_time=1.0)

        # Wall becomes transparent
        self.play(wall.animate.set_opacity(0.2), run_time=0.8)

        # Hidden human now visible
        hidden_human = Dot(radius=0.18, color=COL_GREEN).move_to(
            RIGHT * 2.0 + UP * 0.0
        )
        self.play(FadeIn(hidden_human), run_time=0.4)

        i_see = Text("I see.", font_size=18, color=COL_GREEN, weight=BOLD)
        i_see.next_to(car_a, UP, buff=0.15)
        self.play(Write(i_see), run_time=0.5)
        self.wait(0.5)

        # Fade all scene objects
        self.play(FadeOut(VGroup(
            car_a, car_b, car_c, wall, fm1, fm2,
            comm_ab, comm_ac, hidden_human, i_see,
        )), run_time=0.8)

        # ═══════════════════════════════════════════════════════
        # Payoff quote
        # ═══════════════════════════════════════════════════════
        divider = Line(LEFT * 1.0, RIGHT * 1.0,
                       stroke_color=COL_GOLD, stroke_width=2)
        payoff = Text(
            "So we taught them to cooperate.",
            font_size=36, color=COL_GOLD, weight=BOLD,
        ).center()
        divider.next_to(payoff, UP, buff=0.3)

        self.play(FadeIn(divider), run_time=0.4)
        self.play(Write(payoff), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(VGroup(divider, payoff)), run_time=0.5)

    # ── Helpers ──────────────────────────────────────────────────

    def _make_car(self, color=COL_BLUE):
        """Simple side-view car VGroup."""
        body = RoundedRectangle(
            corner_radius=0.12, width=1.6, height=0.65,
            fill_color=color, fill_opacity=1,
            stroke_color=COL_WHITE, stroke_width=1.5,
        )
        roof = RoundedRectangle(
            corner_radius=0.08, width=0.8, height=0.35,
            fill_color=color, fill_opacity=1,
            stroke_color=COL_WHITE, stroke_width=1.5,
        ).move_to(body.get_top() + DOWN * 0.2)
        wheel_l = Circle(radius=0.19, fill_color="#222", fill_opacity=1,
                         stroke_color=COL_WHITE, stroke_width=1.2
                         ).move_to(body.get_bottom() + LEFT * 0.45 + UP * 0.1)
        wheel_r = wheel_l.copy().move_to(body.get_bottom() + RIGHT * 0.45 + UP * 0.1)
        return VGroup(body, roof, wheel_l, wheel_r)

    def _make_radar(self, origin, color=COL_BLUE, n=3):
        """Fan of outward arcs simulating radar sweep."""
        arcs = VGroup()
        for i in range(n):
            r = 0.8 + i * 0.6
            arc = Arc(
                radius=r, angle=TAU / 4, start_angle=-TAU / 8,
                stroke_color=color,
                stroke_width=max(1, 3 - i),
                stroke_opacity=1.0 - i * 0.25,
            ).move_arc_center_to(origin)
            arcs.add(arc)
        return arcs

    def _make_radar_blocked(self, origin, wall_x):
        """Radar arcs but truncated near wall x-position."""
        arcs = VGroup()
        for i in range(3):
            r = 0.8 + i * 0.6
            # Only show upper-half arc (blocked below by wall line)
            arc = Arc(
                radius=r, angle=TAU / 8, start_angle=-TAU / 16,
                stroke_color=COL_BLUE,
                stroke_width=max(1, 3 - i),
                stroke_opacity=0.6 - i * 0.15,
            ).move_arc_center_to(origin)
            arcs.add(arc)
        return arcs

    def _fm_icon(self, name):
        """Small labeled rounded-rect representing a Foundation Model."""
        box = RoundedRectangle(
            corner_radius=0.08, width=0.9, height=0.45,
            fill_color="#1E3A5F", fill_opacity=1,
            stroke_color=COL_BLUE, stroke_width=1.2,
        )
        label = Text(name, font_size=14, color=COL_WHITE).move_to(box)
        return VGroup(box, label)

    def _thought_box(self, anchor, text):
        """Simple thought bubble above/right of anchor."""
        box = RoundedRectangle(
            corner_radius=0.2, width=2.8, height=1.2,
            fill_color="#111111", fill_opacity=1,
            stroke_color=COL_WHITE, stroke_width=2,
        ).next_to(anchor, UP + RIGHT, buff=0.5)
        label = Text(text, font_size=14, color=COL_WHITE).move_to(box)
        return VGroup(box, label)
