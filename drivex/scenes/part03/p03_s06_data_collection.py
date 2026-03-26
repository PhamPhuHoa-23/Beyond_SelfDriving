"""
Scene 3-06 — Data Collection Strategy
========================================
Intersection + 3 route arcs (right/left/straight) + combined overlay.
Time-of-day strip + dataset badges.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P03S06DataCollection(Scene):
    """
    A — Schematic intersection + route arcs    \
    B — Time-of-day strip                       |- all in one frame
    C — Dataset badges (V2X-Real, V2XPnP-Seq)  /
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("Data Collection Strategy", font_size=26, color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ SECTION A: Intersection + Routes ═══════════════════════
        road_h = Rectangle(width=7, height=1.0, fill_color="#3A3A3A",
                            fill_opacity=1, stroke_width=0)
        road_v = Rectangle(width=1.0, height=5, fill_color="#3A3A3A",
                            fill_opacity=1, stroke_width=0)
        roads = VGroup(road_h, road_v).shift(LEFT * 1.5 + UP * 0.2)

        # ArcBetweenPoints routes
        right_turn = ArcBetweenPoints(
            roads.get_center() + LEFT * 2.0 + DOWN * 0.1,
            roads.get_center() + DOWN * 1.5,
            angle=-PI / 2.5, color=COL_GREEN, stroke_width=2.5
        )
        left_turn  = ArcBetweenPoints(
            roads.get_center() + LEFT * 2.0 + UP * 0.1,
            roads.get_center() + UP * 1.5,
            angle=PI / 2.5, color=COL_BLUE, stroke_width=2.5
        )
        straight   = Arrow(
            roads.get_center() + LEFT * 2.5,
            roads.get_center() + RIGHT * 2.0,
            buff=0, color=COL_GOLD, stroke_width=2.5, tip_length=0.16
        )

        route_legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=COL_GREEN, stroke_width=2.5),
                   Text("Right turn", font_size=11, color=COL_GREEN))
            .arrange(RIGHT, buff=0.1),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=COL_BLUE, stroke_width=2.5),
                   Text("Left turn",  font_size=11, color=COL_BLUE))
            .arrange(RIGHT, buff=0.1),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=COL_GOLD, stroke_width=2.5),
                   Text("Straight",   font_size=11, color=COL_GOLD))
            .arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_corner(UR, buff=0.3)

        self.play(FadeIn(roads), run_time=0.3)
        self.play(Create(right_turn), Create(left_turn), Create(straight), run_time=0.7)
        self.play(FadeIn(route_legend), run_time=0.3)
        self.wait(0.4)

        # ═══ SECTION B: Time-of-day strip ════════════════════════════
        day_bands = [
            ("Morning",   "#F4A261"),
            ("Afternoon", "#2196F3"),
            ("Night",     "#1A1A2E"),
        ]
        band_grps = []
        for i, (label, colour) in enumerate(day_bands):
            band = Rectangle(width=2.2, height=0.55, fill_color=colour,
                              fill_opacity=1, stroke_width=0)
            blbl = Text(label, font_size=12, color=COL_WHITE, weight=BOLD)
            grp  = VGroup(band, blbl)
            blbl.move_to(band.get_center())
            band_grps.append(grp)
        time_strip = VGroup(*band_grps).arrange(RIGHT, buff=0).move_to(DOWN * 2.4)

        self.play(*[FadeIn(g) for g in band_grps], run_time=0.4)
        self.wait(0.3)

        # ═══ SECTION C: Dataset Badges ═══════════════════════════════
        def badge(text, sub, color):
            bg   = RoundedRectangle(width=3.2, height=0.75, corner_radius=0.12,
                                     fill_color=color, fill_opacity=1, stroke_width=0)
            t1   = Text(text, font_size=13, color=COL_WHITE, weight=BOLD)
            t2   = Text(sub,  font_size=10, color=COL_WHITE, slant=ITALIC)
            t1.move_to(bg.get_center() + UP * 0.15)
            t2.move_to(bg.get_center() + DOWN * 0.18)
            return VGroup(bg, t1, t2)

        b1 = badge("V2X-Real", "ECCV 2024",   COL_PURPLE)
        b2 = badge("V2XPnP-Seq", "V2XPnP-Seq", COL_NAVY)
        badges = VGroup(b1, b2).arrange(RIGHT, buff=0.6).move_to(DOWN * 3.4)
        self.play(FadeIn(badges), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
