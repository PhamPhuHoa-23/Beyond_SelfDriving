"""
Scene 2-02 — Background: Why This Problem Matters
==================================================
Crowd death statistics → Waymo 80% reduction → delivery robots.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P02S02Background(Scene):
    """
    Crowd death grid (10×5 dots) → 94% human error overlay →
    Waymo stat box → delivery robot section.
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        # ── crowd grid 10×5 ───────────────────────────────────────
        cols, rows = 10, 5
        dot_gap = 0.6
        crowd = VGroup(*[
            Dot(radius=0.12, color=COL_WHITE, fill_opacity=0.9)
            for _ in range(cols * rows)
        ])
        crowd.arrange_in_grid(rows=rows, cols=cols, buff=dot_gap - 0.24)
        crowd.move_to(ORIGIN + UP * 0.8)

        stat_num = Text("1,190,000", font_size=48, color=COL_RED, weight=BOLD)
        stat_lbl = Text("deaths per year (road accidents)", font_size=20, color=COL_WHITE)
        VGroup(stat_num, stat_lbl).arrange(DOWN, buff=0.2).next_to(crowd, DOWN, buff=0.5)

        self.play(FadeIn(crowd), run_time=0.6)
        self.play(Write(stat_num), run_time=0.8)
        self.play(FadeIn(stat_lbl), run_time=0.4)

        # ── 94% red overlay ────────────────────────────────────────
        crowd_w  = crowd.get_width()
        crowd_h  = crowd.get_height()

        overlay = Rectangle(
            width=crowd_w * 0.94, height=crowd_h,
            fill_color=COL_RED, fill_opacity=0.55, stroke_width=0
        )
        overlay.align_to(crowd, LEFT).align_to(crowd, UP)

        lbl_94 = Text("94% — Human Error", font_size=22, color=COL_RED, weight=BOLD)
        lbl_94.next_to(crowd, RIGHT, buff=0.3)

        self.play(FadeIn(overlay, rate_func=linear), run_time=0.9)
        self.play(Write(lbl_94), run_time=0.5)
        self.wait(0.5)

        # ── Waymo stat box ─────────────────────────────────────────
        waymo_box = RoundedRectangle(
            width=4.5, height=2.2, corner_radius=0.2,
            fill_color="#1B4332", fill_opacity=1,
            stroke_color=COL_GREEN, stroke_width=3
        )
        waymo_big  = Text("80% reduction", font_size=32, color=COL_GREEN, weight=BOLD)
        waymo_sub  = Text("injury accidents vs. human drivers\n(Waymo, 2024)", font_size=14, color=COL_WHITE)
        waymo_grp  = VGroup(waymo_big, waymo_sub).arrange(DOWN, buff=0.2)
        waymo_box.move_to(RIGHT * 4.5 + DOWN * 0.5)
        waymo_grp.move_to(waymo_box.get_center())
        waymo_full = VGroup(waymo_box, waymo_grp)
        waymo_full.shift(RIGHT * 3)          # off-screen start

        self.play(waymo_full.animate.shift(LEFT * 3), run_time=0.6)
        self.wait(1.0)

        # ── transition: fade crowd section ─────────────────────────
        self.play(FadeOut(VGroup(crowd, overlay, stat_num, stat_lbl, lbl_94, waymo_full)),
                  run_time=0.4)

        # ── delivery robots section ─────────────────────────────────
        # Left robot (Amazon style) — simple square car + wheel dots
        def make_robot(color):
            body   = RoundedRectangle(width=0.9, height=0.7, corner_radius=0.12,
                                      fill_color=color, fill_opacity=1, stroke_width=0)
            wheel1 = Dot(radius=0.12, color=GREY_D)
            wheel2 = Dot(radius=0.12, color=GREY_D)
            VGroup(wheel1, wheel2).arrange(RIGHT, buff=0.45)
            wheels = VGroup(wheel1, wheel2)
            wheels.next_to(body, DOWN, buff=0.05)
            eye    = Rectangle(width=0.3, height=0.15,
                                fill_color=COL_LIGHT_BLUE, fill_opacity=0.9, stroke_width=0)
            eye.move_to(body.get_center() + UP * 0.08)
            return VGroup(body, wheels, eye)

        robot_a = make_robot(COL_BLUE).move_to(LEFT * 3 + DOWN * 0.5)
        robot_b = make_robot(COL_GOLD).move_to(ORIGIN + DOWN * 0.5)
        robot_c = make_robot(COL_GREEN).move_to(RIGHT * 3 + DOWN * 0.5)

        lbl_a = Text("Amazon Sidewalk Robot", font_size=14, color=COL_LIGHT_BLUE)
        lbl_b = Text("COCO Campus Delivery",  font_size=14, color=COL_GOLD)
        lbl_c = Text("Starship / Scout",       font_size=14, color=COL_GREEN)
        lbl_a.next_to(robot_a, DOWN, buff=0.2)
        lbl_b.next_to(robot_b, DOWN, buff=0.2)
        lbl_c.next_to(robot_c, DOWN, buff=0.2)

        arrow_ab = Arrow(robot_a.get_right(), robot_b.get_left(), color=COL_BLUE, buff=0.1)
        arrow_bc = Arrow(robot_b.get_right(), robot_c.get_left(), color=COL_BLUE, buff=0.1)

        caption = Text("AI is reshaping logistics — last-mile delivery",
                       font_size=18, color=COL_WHITE, slant=ITALIC)
        caption.to_edge(UP, buff=0.4)

        self.play(FadeIn(VGroup(robot_a, lbl_a, robot_b, lbl_b, robot_c, lbl_c)), run_time=0.6)
        self.play(GrowArrow(arrow_ab), GrowArrow(arrow_bc), run_time=0.4)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(1.2)

        safety_quote = Text(
            "Getting multi-agent systems right\nis a safety problem at scale.",
            font_size=22, color=COL_GOLD
        )
        safety_quote.to_edge(DOWN, buff=0.6)
        self.play(Write(safety_quote), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(VGroup(
            robot_a, lbl_a, robot_b, lbl_b, robot_c, lbl_c,
            arrow_ab, arrow_bc, caption, safety_quote
        )), run_time=0.4)
