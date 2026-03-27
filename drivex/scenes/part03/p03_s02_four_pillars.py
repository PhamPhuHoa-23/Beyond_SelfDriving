"""
Scene 3-02 — Four Pillars Overview
===================================
Vertical timeline: Hardware → Mapping → Fusion → Digital Twin.
Challenge badges on the right.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P03S02FourPillars(Scene):
    """
    4-station vertical pipeline (dependency order) with three challenge badges.
    """

    PILLARS = [
        ("Hardware + Data Collection",   "⚙", COL_BLUE),
        ("Mapping + Localization",        "📍", COL_GREEN),
        ("Late + Intermediate Fusion",    "🔗", COL_PURPLE),
        ("Digital Twin",                  "🌐", COL_GOLD),
    ]

    CHALLENGES = [
        "Solve blind-spot problem via cooperation",
        "Make data trustworthy enough to learn from",
        "Ensure safety at urban intersections",
    ]

    def construct(self):
        self.camera.background_color = BG_DARK

        header = Text("Part 03 — Four Pillars", font_size=26,
                      color=COL_GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header), run_time=0.3)

        # vertical spine (left-center)
        spine_top = UP * 2.5 + LEFT * 3.0
        spine_bot = DOWN * 2.5 + LEFT * 3.0
        spine = Line(spine_top, spine_bot, color=COL_WHITE, stroke_width=2)
        self.play(Create(spine), run_time=0.6)

        n = len(self.PILLARS)
        ys = [spine_top[1] - i *
              (spine_top[1] - spine_bot[1]) / (n - 1) for i in range(n)]

        for i, (title, icon, color) in enumerate(self.PILLARS):
            spine_x = spine_top[0]
            dot = Dot(point=[spine_x, ys[i], 0], radius=0.13, color=color)
            box = RoundedRectangle(
                width=4.2, height=0.85, corner_radius=0.12,
                fill_color="#1E3A5F", fill_opacity=1,
                stroke_color=COL_GOLD if i == 0 else color,
                stroke_width=2 if i == 0 else 1.5
            )
            box.move_to([spine_x + 2.8, ys[i], 0])
            lbl = Text(title, font_size=14, color=COL_WHITE,
                       weight=BOLD if i == 0 else NORMAL)
            lbl.move_to(box.get_center())
            icon_txt = Text(icon, font_size=18)
            icon_txt.next_to(box, LEFT, buff=0.2)
            self.play(FadeIn(dot), FadeIn(box), FadeIn(
                lbl), FadeIn(icon_txt), run_time=0.3)

        # dependency arrows between pillar stations
        for i in range(n - 1):
            arr = Arrow(
                [spine_top[0], ys[i] - 0.15, 0],
                [spine_top[0], ys[i + 1] + 0.15, 0],
                color=COL_BLUE, buff=0, stroke_width=2,
                max_tip_length_to_length_ratio=0.25
            )
            self.play(GrowArrow(arr), run_time=0.25)

        # challenge badges (right side)
        badge_x = 4.2
        badge_ys = [1.2, 0.0, -1.2]
        for j, ch in enumerate(self.CHALLENGES):
            bage_box = RoundedRectangle(
                width=4.5, height=0.75, corner_radius=0.12,
                fill_color="#2A1A1A", fill_opacity=1,
                stroke_color=COL_RED, stroke_width=1.5
            )
            bage_box.move_to([badge_x, badge_ys[j], 0])
            bage_txt = Text(ch, font_size=12, color=COL_WHITE)
            bage_txt.move_to(bage_box.get_center())
            self.play(FadeIn(VGroup(bage_box, bage_txt)), run_time=0.25)

        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
