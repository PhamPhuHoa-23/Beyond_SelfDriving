"""
Scene 3-08 — Multi-Rate Kalman Filter
========================================
3 input lanes → Kalman Filter box → 100 Hz output.
Animated flow dots using MoveAlongPath.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P03S08KalmanFilter(Scene):
    """
    A — 3 input lanes with frequency badges + limitations
    B — Kalman Filter central box
    C — 100 Hz output lane + animated flow dots
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("Multi-Rate Kalman Filter Fusion", font_size=24, color=COL_GOLD,
                        weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ Kalman filter center box ══════════════════════════════
        kf_box = RoundedRectangle(width=2.6, height=1.2, corner_radius=0.18,
                                   fill_color=COL_NAVY, fill_opacity=1,
                                   stroke_color=COL_GOLD, stroke_width=2)
        kf_lbl = Text("Kalman\nFilter", font_size=16, color=COL_GOLD, weight=BOLD)
        kf_box.move_to(ORIGIN)
        kf_lbl.move_to(kf_box.get_center())

        self.play(FadeIn(VGroup(kf_box, kf_lbl)), run_time=0.3)

        # ═══ Input lanes ══════════════════════════════════════════
        inputs = [
            ("GNSS",          "5 Hz",   "loses fix indoors /\nbetween buildings",   COL_RED,          UP * 1.8),
            ("IMU / Wheel",   "100 Hz", "drifts over time",                          COL_BLUE,         ORIGIN),
            ("LiDAR map-match","1 Hz",  "heavy compute",                              COL_INFRA_ORANGE, DOWN * 1.8),
        ]

        paths = []
        for name, freq, limit, color, y_pos in inputs:
            src_pos = LEFT * 5.2 + y_pos
            dst_pos = kf_box.get_left() + y_pos * 0.18

            freq_badge = RoundedRectangle(width=1.0, height=0.38, corner_radius=0.1,
                                           fill_color=color, fill_opacity=1, stroke_width=0)
            freq_lbl   = Text(freq, font_size=11, color=COL_WHITE, weight=BOLD)
            freq_badge.move_to(src_pos + RIGHT * 0.1)
            freq_lbl.move_to(freq_badge.get_center())

            name_txt = Text(name, font_size=12, color=color, weight=BOLD)
            name_txt.next_to(freq_badge, UP, buff=0.08)

            limit_txt = Text(limit, font_size=10, color=COL_WHITE, slant=ITALIC)
            limit_txt.next_to(freq_badge, DOWN, buff=0.08)

            path = Line(freq_badge.get_right(), dst_pos, color=color, stroke_width=1.8)
            dot  = Dot(radius=0.08, color=color).move_to(path.get_start())

            self.play(FadeIn(VGroup(freq_badge, freq_lbl, name_txt, limit_txt, path)),
                       run_time=0.25)
            self.play(MoveAlongPath(dot, path), run_time=0.5, rate_func=linear)
            self.play(FadeOut(dot), run_time=0.1)
            paths.append(path)

        # ═══ Output lane ══════════════════════════════════════════
        out_pos = RIGHT * 4.5
        out_arr = Arrow(kf_box.get_right(), out_pos, buff=0.05,
                         color=COL_GREEN, stroke_width=2.5, tip_length=0.18)
        out_lbl = Text("100 Hz\nLane-Level Output", font_size=13, color=COL_GREEN, weight=BOLD)
        out_lbl.next_to(out_arr, UP, buff=0.1)

        self.play(Create(out_arr), FadeIn(out_lbl), run_time=0.4)

        # Animate a dot flowing through the output
        out_dot = Dot(radius=0.1, color=COL_GREEN).move_to(kf_box.get_right())
        self.play(MoveAlongPath(out_dot, out_arr), run_time=0.5, rate_func=linear)
        self.play(FadeOut(out_dot), run_time=0.1)
        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
