"""
Scene 2-04 — The Physics Limit: Occlusion
==========================================
Top-down LiDAR visualisation (single-agent vs multi-agent).
Blind zones shrink when a second agent shares its view.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P02S04Occlusion(Scene):
    """
    Two-panel layout (top: single-agent scan, bottom: multi-agent scan).
    Blind zones filled red → green gain zone when second agent added.
    """

    def _make_agent(self, pos, color=COL_BLUE):
        body = Circle(radius=0.18, fill_color=color, fill_opacity=1, stroke_width=0)
        body.move_to(pos)
        return body

    def _make_lidar_sweep(self, center, radius=2.0, color=COL_BLUE):
        """Stylised LiDAR arc sweep (three arcs to suggest rotating scan)."""
        arcs = VGroup()
        for angle in [0, PI / 6, PI / 3]:
            arc = Arc(radius=radius, start_angle=angle, angle=PI,
                      color=color, stroke_opacity=0.35, stroke_width=1.5)
            arc.move_arc_center_to(center)
            arcs.add(arc)
        return arcs

    def _make_blind_zone(self, points, color=COL_RED, opacity=0.40):
        poly = Polygon(*points,
                       fill_color=color, fill_opacity=opacity, stroke_width=0)
        return poly

    def construct(self):
        self.camera.background_color = BG_DARK

        # ── dividing line at y=0 ───────────────────────────────────
        divider = Line(LEFT * 7, RIGHT * 7, color=COL_WHITE,
                       stroke_opacity=0.3, stroke_width=1)
        divider.move_to(ORIGIN)

        lbl_single = Text("Single Agent", font_size=20, color=COL_WHITE, weight=BOLD)
        lbl_multi  = Text("Multi Agent",  font_size=20, color=COL_WHITE, weight=BOLD)
        lbl_single.move_to(LEFT * 5.5 + UP * 1.6)
        lbl_multi.move_to(LEFT * 5.5 + DOWN * 1.6)

        self.play(Create(divider), FadeIn(lbl_single), FadeIn(lbl_multi), run_time=0.5)

        # ── TOP: single-agent panel ────────────────────────────────
        center_s = UP * 1.5
        agent_s  = self._make_agent(center_s, COL_BLUE)
        sweep_s  = self._make_lidar_sweep(center_s, radius=2.3)

        # four blind zones (simulated buildings / trucks)
        blind_zones_s = VGroup(
            self._make_blind_zone([
                center_s + UP * 0.8 + LEFT * 1.5,
                center_s + UP * 2.2 + LEFT * 2.8,
                center_s + UP * 2.2 + LEFT * 1.2,
            ]),
            self._make_blind_zone([
                center_s + RIGHT * 1.2 + UP * 0.5,
                center_s + RIGHT * 2.8 + UP * 1.0,
                center_s + RIGHT * 2.9 + DOWN * 0.3,
            ]),
            self._make_blind_zone([
                center_s + DOWN * 0.5 + RIGHT * 0.8,
                center_s + DOWN * 1.8 + RIGHT * 1.8,
                center_s + DOWN * 1.8 + LEFT * 0.5,
            ]),
            self._make_blind_zone([
                center_s + LEFT * 1.0 + DOWN * 0.5,
                center_s + LEFT * 2.5 + DOWN * 1.4,
                center_s + LEFT * 2.4 + UP * 0.5,
            ]),
        )
        single_panel = VGroup(agent_s, sweep_s, blind_zones_s)
        single_panel.shift(RIGHT * 1.5)     # centre in right-half of screen

        self.play(Create(sweep_s), run_time=0.8)
        self.play(FadeIn(agent_s), FadeIn(blind_zones_s), run_time=0.5)

        lbl_dark = Text("Dark regions = blind spots", font_size=15, color=COL_RED)
        lbl_dark.next_to(blind_zones_s, RIGHT, buff=0.3)
        arr_dark = Arrow(lbl_dark.get_left(), lbl_dark.get_left() + LEFT * 0.8,
                         color=COL_RED, buff=0, max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(lbl_dark), GrowArrow(arr_dark), run_time=0.4)
        self.wait(0.5)

        # ── BOTTOM: multi-agent panel ──────────────────────────────
        center_m1 = DOWN * 1.5 + RIGHT * 0.2
        center_m2 = DOWN * 1.5 + RIGHT * 2.8
        agent_m1  = self._make_agent(center_m1, COL_BLUE)
        agent_m2  = self._make_agent(center_m2, COL_PURPLE)
        sweep_m1  = self._make_lidar_sweep(center_m1, radius=2.3)
        sweep_m2  = self._make_lidar_sweep(center_m2, radius=2.0, color=COL_PURPLE)

        # smaller remaining blind zones
        blind_zones_m = VGroup(
            self._make_blind_zone([
                center_m1 + UP * 0.5 + LEFT * 1.2,
                center_m1 + UP * 1.4 + LEFT * 2.0,
                center_m1 + UP * 1.4 + LEFT * 0.8,
            ], COL_RED, 0.3),
        )

        # green gain zone
        gain_zone = self._make_blind_zone([
            center_m1 + UP * 0.8 + RIGHT * 1.0,
            center_m1 + UP * 2.2 + RIGHT * 2.2,
            center_m2 + UP * 2.0 + LEFT * 0.5,
        ], COL_GREEN, 0.25)

        comm_link = DashedLine(center_m1, center_m2, color=COL_BLUE,
                               dash_length=0.15, dashed_ratio=0.5)

        self.play(Create(sweep_m1), Create(sweep_m2), run_time=0.7)
        self.play(FadeIn(agent_m1), FadeIn(agent_m2), FadeIn(blind_zones_m), run_time=0.4)
        self.play(FadeIn(gain_zone, rate_func=smooth), run_time=0.6)
        self.play(Create(comm_link), run_time=0.4)

        lbl_gain = Text("Coverage gain ↑", font_size=15, color=COL_GREEN)
        lbl_gain.next_to(gain_zone, RIGHT, buff=0.25)
        self.play(FadeIn(lbl_gain), run_time=0.3)

        # ── physics statement ──────────────────────────────────────
        physics = Text(
            "Physics problem — not algorithm.",
            font_size=22, color=COL_GOLD, weight=BOLD
        )
        physics.to_edge(DOWN, buff=1.0)
        self.play(Write(physics), run_time=0.5)
        self.wait(0.6)

        conclusion_box = RoundedRectangle(
            width=7.5, height=0.9, corner_radius=0.15,
            fill_color="#1E3A5F", fill_opacity=1,
            stroke_color=COL_BLUE, stroke_width=2
        )
        conclusion_txt = Text(
            "Complementary Information Sharing",
            font_size=20, color=COL_WHITE
        )
        conclusion_box.to_edge(DOWN, buff=0.25)
        conclusion_txt.move_to(conclusion_box.get_center())
        self.play(FadeIn(VGroup(conclusion_box, conclusion_txt)), run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            divider, lbl_single, lbl_multi,
            single_panel, lbl_dark, arr_dark,
            sweep_m1, sweep_m2, agent_m1, agent_m2,
            blind_zones_m, gain_zone, comm_link, lbl_gain,
            physics, conclusion_box, conclusion_txt
        )), run_time=0.4)
