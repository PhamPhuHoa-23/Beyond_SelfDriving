"""
Scene 3-10 — V2X-ReaLO: Intermediate Fusion
=============================================
BEV 8×8 grid → compress 32× → 0.5 MB.
Balance scale tipping animation (accuracy ↔ latency).
Paper: T-PAMI.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P03S10V2XReaLO(Scene):
    """
    A — BEV feature grid + compression pipeline
    B — Balance scale (accuracy vs latency) finding working point
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("V2X-ReaLO — Intermediate Fusion", font_size=24, color=COL_GOLD,
                        weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ SECTION A: BEV Grid ══════════════════════════════════
        grid_size = 8
        cell_w, cell_h = 0.28, 0.28
        bev_cells = VGroup()
        for r in range(grid_size):
            for c in range(grid_size):
                cell = Square(side_length=cell_w)
                cell.set_stroke(color=COL_SENSOR_CYAN, width=0.5, opacity=0.6)
                cell.set_fill(color=COL_NAVY, opacity=0.7)
                cell.move_to(LEFT * 4.0 + LEFT * (grid_size / 2 - c) * cell_w
                              + UP * (grid_size / 2 - r) * cell_h)
                bev_cells.add(cell)
        bev_lbl = Text("BEV Feature\n8×8 grid", font_size=12, color=COL_SENSOR_CYAN)
        bev_lbl.next_to(bev_cells, DOWN, buff=0.15)

        self.play(Create(bev_cells), run_time=0.6)
        self.play(FadeIn(bev_lbl), run_time=0.2)

        # Compression arrow
        comp_arr = Arrow(bev_cells.get_right(), RIGHT * 0.8,
                          buff=0.08, color=COL_GREEN, stroke_width=2, tip_length=0.15)
        comp_txt = Text("Compress 32×", font_size=12, color=COL_GREEN)
        comp_txt.next_to(comp_arr, UP, buff=0.08)
        size_txt = Text("→ 0.5 MB", font_size=12, color=COL_GREEN)
        size_txt.next_to(comp_arr, DOWN, buff=0.08)

        self.play(Create(comp_arr), FadeIn(comp_txt), FadeIn(size_txt), run_time=0.4)
        self.wait(0.4)

        # ═══ SECTION B: Balance Scale ════════════════════════════
        pivot = Dot(radius=0.07, color=COL_WHITE).move_to(RIGHT * 3.5 + DOWN * 0.3)
        beam  = Line(LEFT * 0.9, RIGHT * 0.9, color=COL_WHITE, stroke_width=2)
        beam.move_to(pivot.get_center())

        pan_l = Square(side_length=0.6, fill_color=COL_BLUE, fill_opacity=0.9,
                        stroke_width=0).move_to(pivot.get_center() + LEFT * 0.9 + DOWN * 0.5)
        pan_r = Square(side_length=0.6, fill_color=COL_RED,  fill_opacity=0.9,
                        stroke_width=0).move_to(pivot.get_center() + RIGHT * 0.9 + DOWN * 0.5)

        lbl_acc = Text("Accuracy", font_size=11, color=COL_BLUE)
        lbl_lat = Text("Latency",  font_size=11, color=COL_RED)
        lbl_acc.next_to(pan_l, DOWN, buff=0.1)
        lbl_lat.next_to(pan_r, DOWN, buff=0.1)

        self.play(FadeIn(VGroup(pivot, beam, pan_l, pan_r, lbl_acc, lbl_lat)), run_time=0.4)

        # Tip left (accuracy wins)→ then balance → mark working point
        self.play(
            beam.animate.rotate(PI / 10, about_point=pivot.get_center()),
            pan_l.animate.shift(DOWN * 0.25),
            pan_r.animate.shift(UP * 0.25),
            run_time=0.5
        )
        self.play(
            beam.animate.rotate(-PI / 10, about_point=pivot.get_center()),
            pan_l.animate.shift(UP * 0.25),
            pan_r.animate.shift(DOWN * 0.25),
            run_time=0.5
        )

        wp = Dot(radius=0.09, color=COL_GOLD).move_to(pivot.get_center() + RIGHT * 0.1)
        wp_lbl = Text("Working\npoint", font_size=10, color=COL_GOLD)
        wp_lbl.next_to(wp, UR, buff=0.08)
        self.play(FadeIn(wp), FadeIn(wp_lbl), run_time=0.3)

        # Paper badge
        paper_badge = RoundedRectangle(width=3.5, height=0.5, corner_radius=0.1,
                                        fill_color=COL_NAVY, fill_opacity=1, stroke_width=0)
        paper_txt   = Text("V2X-ReaLO  ·  T-PAMI", font_size=12, color=COL_WHITE)
        paper_badge.to_edge(DOWN, buff=0.4)
        paper_txt.move_to(paper_badge.get_center())
        self.play(FadeIn(VGroup(paper_badge, paper_txt)), run_time=0.3)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
