"""
Scene 2-08 — V2XPnP-Seq Dataset
=================================
First real-world multi-modal V2X sequential dataset.
Map visualisation + stat box + comparison strip.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P02S08Dataset(Scene):
    """
    Left: top-down map with V2V / V2I / I2I comm links.
    Right: dataset stats.
    Bottom: comparison strip vs prior datasets.
    """

    def construct(self):
        self.camera.background_color = BG_DARK

        # ── title ──────────────────────────────────────────────────
        title = Text("V2XPnP-Seq", font_size=30, color=COL_GOLD, weight=BOLD)
        sub = Text("First large-scale real-world V2X sequential dataset",
                   font_size=18, color=COL_WHITE)
        VGroup(title, sub).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.3)
        self.play(Write(title), FadeIn(sub), run_time=0.6)

        # ── top-down map (left half) ───────────────────────────────
        map_bg = RoundedRectangle(
            width=5.5, height=4.0, corner_radius=0.2,
            fill_color="#1A2A3A", fill_opacity=1,
            stroke_color=COL_BLUE, stroke_width=2
        )
        map_bg.move_to(LEFT * 3.5 + DOWN * 0.8)

        # road lines
        roads = VGroup(
            Line(LEFT * 2.5 + DOWN * 0.8, RIGHT * 0 + DOWN *
                 0.8,    color=COL_WHITE, stroke_opacity=0.4),
            Line(LEFT * 1.0 + UP * 1.2,   LEFT * 1.0 + DOWN *
                 2.8,   color=COL_WHITE, stroke_opacity=0.4),
        )
        roads.shift(LEFT * 3.5 + DOWN * 0.8 - roads.get_center())

        # vehicle icons
        v1 = Dot(radius=0.18, color=COL_BLUE).move_to(LEFT * 4.8 + DOWN * 0.6)
        v2 = Dot(radius=0.18, color=COL_BLUE).move_to(LEFT * 3.5 + DOWN * 1.2)
        # infrastructure nodes
        i1 = Square(side_length=0.3, fill_color=COL_GOLD, fill_opacity=1,
                    stroke_width=0).move_to(LEFT * 2.8 + UP * 0.1)
        i2 = Square(side_length=0.3, fill_color=COL_GOLD, fill_opacity=1,
                    stroke_width=0).move_to(LEFT * 4.2 + DOWN * 1.8)

        # V2V link
        link_v2v = DashedLine(v1.get_center(), v2.get_center(),
                              color=COL_BLUE, dash_length=0.1)
        lbl_v2v = Text("V2V", font_size=10, color=COL_BLUE)
        lbl_v2v.next_to(link_v2v.get_center(), UP, buff=0.12)
        # V2I links
        link_v2i1 = DashedLine(
            v1.get_center(), i1.get_center(), color=COL_GREEN,  dash_length=0.1)
        link_v2i2 = DashedLine(
            v2.get_center(), i2.get_center(), color=COL_GREEN,  dash_length=0.1)
        # I2I link
        link_i2i = DashedLine(i1.get_center(), i2.get_center(),
                              color=COL_GOLD,   dash_length=0.1)
        lbl_i2i = Text("I2I",  font_size=10, color=COL_GOLD)
        lbl_i2i.next_to(link_i2i.get_center(), RIGHT, buff=0.12)

        self.play(FadeIn(map_bg), Create(roads), run_time=0.5)
        self.play(FadeIn(v1), FadeIn(v2), FadeIn(i1), FadeIn(i2), run_time=0.4)
        self.play(Create(link_v2v), FadeIn(lbl_v2v), run_time=0.3)
        self.play(Create(link_v2i1), Create(link_v2i2), run_time=0.3)
        self.play(Create(link_i2i), FadeIn(lbl_i2i), run_time=0.3)

        # ── stats box (right half) ─────────────────────────────────
        stats_data = [
            ("2 vehicles + 2 infra nodes", COL_WHITE),
            ("40,000 LiDAR frames",        COL_WHITE),
            ("208,000 camera frames",      COL_WHITE),
            ("HD maps + trajectories",     COL_WHITE),
            ("All V2X collaboration modes", COL_GREEN),
        ]
        stats_box = RoundedRectangle(
            width=5.0, height=3.2, corner_radius=0.15,
            fill_color="#1E3A5F", fill_opacity=1,
            stroke_color=COL_BLUE, stroke_width=2
        )
        stats_box.move_to(RIGHT * 3.5 + DOWN * 0.8)
        stats_title = Text("Dataset Stats", font_size=16,
                           color=COL_LIGHT_BLUE, weight=BOLD)
        stats_title.next_to(stats_box, UP, buff=0).align_to(
            stats_box, UP).shift(DOWN * 0.35)

        stat_items = VGroup(*[
            Text(f"• {s}", font_size=14, color=c, t2c={"•": COL_GOLD})
            for s, c in stats_data
        ]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        stat_items.move_to(stats_box.get_center() + DOWN * 0.15)

        self.play(FadeIn(stats_box), FadeIn(stats_title), run_time=0.4)
        self.play(AnimationGroup(
            *[FadeIn(s) for s in stat_items], lag_ratio=0.2), run_time=0.8)

        # ── comparison strip ───────────────────────────────────────
        comp_data = [
            ("OPV2V '22",  "Sim only",    COL_RED),
            ("DAIR-V2X",   "V2I only",    COL_RED),
            ("V2X-Real '24", "V2V+V2I",    COL_BLUE),
            ("V2XPnP-Seq", "All V2X ✓",  COL_GREEN),
        ]
        strip = VGroup()
        for label, tag, color in comp_data:
            item_box = RoundedRectangle(width=2.5, height=0.7, corner_radius=0.1,
                                        fill_color="#1A1A1A", fill_opacity=1,
                                        stroke_color=color, stroke_width=1.5)
            item_lbl = Text(f"{label}\n{tag}", font_size=11, color=color)
            item_lbl.move_to(item_box.get_center())
            strip.add(VGroup(item_box, item_lbl))
        strip.arrange(RIGHT, buff=0.2)
        strip.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(strip), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
