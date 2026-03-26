"""
Scene 3-07 — Mapping & Localization: Why It Matters
======================================================
HD Map center node with 3 role arms + fusion failure illustration.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P03S07LocalizationWhy(Scene):
    """
    A — HD Map role diagram (3 arms: Data Acquisition / Localization / Digital Twin)
    B — Fusion failure: same pedestrian → 2 ghost objects + warning
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("Mapping & Localization", font_size=26, color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.5)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ SECTION A: HD Map Role Diagram ═══════════════════════
        center_box = RoundedRectangle(width=2.4, height=0.65, corner_radius=0.15,
                                       fill_color=COL_NAVY, fill_opacity=1,
                                       stroke_color=COL_GOLD, stroke_width=1.5)
        center_txt = Text("HD Map", font_size=15, color=COL_GOLD, weight=BOLD)
        center_box.move_to(UP * 0.9)
        center_txt.move_to(center_box.get_center())

        roles = [
            ("Data Acquisition",    COL_BLUE,        LEFT * 3.6 + UP * 0.9),
            ("Localization",        COL_GREEN,       UP * 0.9 + DOWN * 1.6),
            ("Digital Twin",        COL_INFRA_ORANGE, RIGHT * 3.6 + UP * 0.9),
        ]
        role_items = []
        for name, color, pos in roles:
            r_box = RoundedRectangle(width=2.5, height=0.55, corner_radius=0.12,
                                      fill_color=color, fill_opacity=0.85, stroke_width=0)
            r_lbl = Text(name, font_size=13, color=COL_WHITE, weight=BOLD)
            r_lbl.move_to(r_box.get_center())
            grp   = VGroup(r_box, r_lbl).move_to(pos)
            arr   = Arrow(center_box.get_center(), grp.get_center(),
                           buff=0.3, color=color, stroke_width=1.8, tip_length=0.14)
            role_items.append((grp, arr))

        self.play(FadeIn(VGroup(center_box, center_txt)), run_time=0.3)
        for grp, arr in role_items:
            self.play(Create(arr), FadeIn(grp), run_time=0.3)
        self.wait(0.5)

        # ═══ SECTION B: Fusion Failure ════════════════════════════
        self.play(
            *[FadeOut(grp) for grp, _ in role_items],
            *[FadeOut(arr) for _, arr in role_items],
            FadeOut(VGroup(center_box, center_txt)),
            run_time=0.3
        )

        fail_title = Text("Without accurate localization:", font_size=16, color=COL_RED)
        fail_title.next_to(heading, DOWN, buff=0.5)
        self.play(FadeIn(fail_title), run_time=0.2)

        # Pedestrian appears in two positions
        ped_real  = Circle(radius=0.22, fill_color=COL_WHITE,  fill_opacity=1, stroke_width=0)
        ped_real.move_to(LEFT * 1.5 + DOWN * 0.2)
        ped_ghost = Circle(radius=0.22, fill_color=COL_WHITE,  fill_opacity=0.5, stroke_width=0)
        ped_ghost.move_to(RIGHT * 1.5 + DOWN * 0.2)

        lbl_r = Text("Agent A sees pedestrian here", font_size=11, color=COL_BLUE)
        lbl_g = Text("Agent B sees same pedestrian\n(different localization frame)",
                      font_size=11, color=COL_RED)
        lbl_r.next_to(ped_real,  DOWN, buff=0.15)
        lbl_g.next_to(ped_ghost, DOWN, buff=0.15)

        self.play(FadeIn(ped_real),  FadeIn(lbl_r), run_time=0.3)
        self.play(FadeIn(ped_ghost), FadeIn(lbl_g), run_time=0.3)

        warn_box = RoundedRectangle(width=5.5, height=0.65, corner_radius=0.15,
                                     fill_color=COL_RED, fill_opacity=1, stroke_width=0)
        warn_txt = Text("Worse than single-agent perception!", font_size=14,
                         color=COL_WHITE, weight=BOLD)
        warn_box.move_to(DOWN * 2.4)
        warn_txt.move_to(warn_box.get_center())

        self.play(FadeIn(VGroup(warn_box, warn_txt)), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
