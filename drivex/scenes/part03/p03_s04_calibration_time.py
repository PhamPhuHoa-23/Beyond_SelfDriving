"""
Scene 3-04 — Time Calibration
==============================
Moving car at 60 km/h → 50 ms delay → ghost car ~1 m behind.
Solution: GPS shared time reference + hardware triggers.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P03S04CalibrationTime(Scene):
    """
    A — Ghost car animation (50 ms lag at 60 km/h → ~0.83 m gap)
    B — Solution: GPS time source + hardware trigger diagram
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        # ═══ SECTION A: The Problem ════════════════════════════════
        heading = Text("Time Calibration", font_size=28,
                       color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.5)
        self.play(FadeIn(heading), run_time=0.3)

        # Road surface
        road = Rectangle(width=11, height=0.8, fill_color="#3A3A3A", fill_opacity=1,
                         stroke_width=0)
        road.move_to(DOWN * 0.8)
        road_line = DashedLine(LEFT * 5 + DOWN * 0.8, RIGHT * 5 + DOWN * 0.8,
                               color=COL_WHITE, stroke_opacity=0.3, dash_length=0.4)
        self.play(FadeIn(road), run_time=0.3)

        # True car (blue)
        car_true = RoundedRectangle(width=0.9, height=0.45, corner_radius=0.1,
                                    fill_color=COL_BLUE, fill_opacity=1, stroke_width=0)
        car_true.move_to(LEFT * 3.5 + DOWN * 0.8)
        true_lbl = Text("True position", font_size=11, color=COL_BLUE)
        true_lbl.next_to(car_true, UP, buff=0.1)

        # Ghost car (red, ~0.9 units behind — represents ~1 m at scale)
        car_ghost = RoundedRectangle(width=0.9, height=0.45, corner_radius=0.1,
                                     fill_color=COL_RED, fill_opacity=0.6, stroke_width=0)
        car_ghost.move_to(car_true.get_center() + LEFT * 0.9)
        ghost_lbl = Text("50 ms delayed", font_size=11, color=COL_RED)
        ghost_lbl.next_to(car_ghost, UP, buff=0.1)

        # Gap annotation
        gap_arr = DoubleArrow(car_ghost.get_right(), car_true.get_left(),
                              buff=0.05, color=COL_GOLD, tip_length=0.15, stroke_width=1.8)
        gap_txt = Text("~1 m gap", font_size=12, color=COL_GOLD)
        gap_txt.next_to(gap_arr, DOWN, buff=0.1)

        self.play(FadeIn(car_true), FadeIn(true_lbl), run_time=0.3)
        self.play(FadeIn(car_ghost), FadeIn(ghost_lbl), run_time=0.3)
        self.play(Create(gap_arr), FadeIn(gap_txt), run_time=0.4)

        # Animate both cars moving right together (but ghost lags)
        self.play(
            car_true.animate.shift(RIGHT * 4),
            true_lbl.animate.shift(RIGHT * 4),
            car_ghost.animate.shift(RIGHT * 4),
            ghost_lbl.animate.shift(RIGHT * 4),
            gap_arr.animate.shift(RIGHT * 4),
            gap_txt.animate.shift(RIGHT * 4),
            run_time=1.2, rate_func=linear
        )
        self.wait(0.4)

        speed_note = Text("60 km/h  →  16.7 m/s  →  50 ms delay  ≈  0.83 m",
                          font_size=14, color=COL_WHITE)
        speed_note.move_to(DOWN * 2.3)
        self.play(FadeIn(speed_note), run_time=0.3)
        self.wait(0.5)

        # ═══ SECTION B: Solution ═══════════════════════════════════
        self.play(FadeOut(Group(road, road_line, car_true, true_lbl,
                                car_ghost, ghost_lbl, gap_arr, gap_txt,
                                speed_note)),
                  run_time=0.3)

        sol_title = Text("Solution", font_size=18,
                         color=COL_GREEN, weight=BOLD)
        sol_title.next_to(heading, DOWN, buff=0.4)
        self.play(FadeIn(sol_title), run_time=0.2)

        # Source node
        gps_box = RoundedRectangle(width=2.8, height=0.7, corner_radius=0.15,
                                   fill_color=COL_PURPLE, fill_opacity=1, stroke_width=0)
        gps_lbl = Text("GPS Shared Time Source", font_size=13,
                       color=COL_WHITE, weight=BOLD)
        gps_box.move_to(UP * 0.5)
        gps_lbl.move_to(gps_box.get_center())

        hw_box = RoundedRectangle(width=2.6, height=0.6, corner_radius=0.15,
                                  fill_color=COL_GREEN, fill_opacity=1, stroke_width=0)
        hw_lbl = Text("Hardware Trigger", font_size=13,
                      color=BG_BLACK, weight=BOLD)
        hw_box.move_to(LEFT * 2.8 + DOWN * 0.9)
        hw_lbl.move_to(hw_box.get_center())

        sw_box = RoundedRectangle(width=2.6, height=0.6, corner_radius=0.15,
                                  fill_color=COL_RED, fill_opacity=1, stroke_width=0)
        sw_lbl = Text("Software Trigger", font_size=13,
                      color=COL_WHITE, weight=BOLD)
        sw_box.move_to(RIGHT * 2.8 + DOWN * 0.9)
        sw_lbl.move_to(sw_box.get_center())

        cross = Cross(sw_box, color=COL_RED, stroke_width=3).scale(1.1)

        latency_sw = Text("OS jitter: ±100 ms", font_size=11,
                          color=COL_RED, slant=ITALIC)
        latency_sw.next_to(sw_box, DOWN, buff=0.15)
        latency_hw = Text("Precision: < 1 µs", font_size=11,
                          color=COL_GREEN, slant=ITALIC)
        latency_hw.next_to(hw_box, DOWN, buff=0.15)

        arr_hw = Arrow(gps_box.get_bottom(), hw_box.get_top(), buff=0.05,
                       color=COL_GREEN, stroke_width=2)
        arr_sw = Arrow(gps_box.get_bottom(), sw_box.get_top(), buff=0.05,
                       color=COL_GREEN, stroke_width=2)

        self.play(FadeIn(VGroup(gps_box, gps_lbl)), run_time=0.3)
        self.play(Create(arr_hw), Create(arr_sw), run_time=0.3)
        self.play(FadeIn(VGroup(hw_box, hw_lbl)), FadeIn(
            VGroup(sw_box, sw_lbl)), run_time=0.3)
        self.play(FadeIn(latency_hw), FadeIn(latency_sw), run_time=0.3)
        self.play(Create(cross), run_time=0.3)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
