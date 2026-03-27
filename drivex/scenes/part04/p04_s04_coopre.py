"""
Scene 4-04 — CooPre: Cooperative Pretraining
==============================================
Section A — Masked BEV reconstruction mechanism diagram.
Section B — Results bar chart (50% labeled data = 100% baseline performance).
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P04S04CooPre(Scene):
    """
    A — Multi-agent masked BEV reconstruction + inductive bias callout
    B — Result bars: 50% CooPre = 100% baseline; 100% CooPre = +4% AP
    """

    def construct(self):
        self.camera.background_color = "#0F172A"

        # ═══════════════════════════════════════════════════════════
        # SECTION A — Mechanism
        # ═══════════════════════════════════════════════════════════
        title = Text("CooPre — Cooperative Pretraining", font_size=22, color=COL_GOLD,
                     weight=BOLD)
        title.to_edge(UP, buff=0.4)
        badge = RoundedRectangle(width=2.6, height=0.42, corner_radius=0.1,
                                 fill_color="#1B4332", fill_opacity=1,
                                 stroke_color=COL_GREEN, stroke_width=1.5)
        badge_txt = Text("Zero annotations", font_size=12,
                         color=COL_GREEN, weight=BOLD)
        badge.next_to(title, RIGHT, buff=0.4)
        badge_txt.move_to(badge.get_center())

        self.play(Write(title), FadeIn(VGroup(badge, badge_txt)), run_time=0.5)

        # Agent blocks
        ag1 = Rectangle(width=1.0, height=0.7, fill_color="#1E3A5F", fill_opacity=1,
                        stroke_width=0).move_to(LEFT * 4.5 + UP * 0.8)
        ag2 = Rectangle(width=1.0, height=0.7, fill_color="#1E3A5F", fill_opacity=1,
                        stroke_width=0).move_to(LEFT * 4.5 + DOWN * 0.5)
        ag1_lbl = Text("Agent 1\n(LiDAR)", font_size=10, color=COL_LIGHT_BLUE)
        ag2_lbl = Text("Agent 2\n(LiDAR)", font_size=10, color=COL_LIGHT_BLUE)
        ag1_lbl.move_to(ag1.get_center())
        ag2_lbl.move_to(ag2.get_center())

        self.play(FadeIn(ag1), FadeIn(ag2), FadeIn(
            ag1_lbl), FadeIn(ag2_lbl), run_time=0.4)

        # Arrows to BEV
        bev_center = ORIGIN + DOWN * 0.2
        arr1 = Arrow(ag1.get_right(), bev_center + LEFT * 1.8, buff=0.08,
                     color=COL_BLUE, stroke_width=2, tip_length=0.14)
        arr2 = Arrow(ag2.get_right(), bev_center + LEFT * 1.8, buff=0.08,
                     color=COL_BLUE, stroke_width=2, tip_length=0.14)
        self.play(Create(arr1), Create(arr2), run_time=0.3)

        # BEV 8×8 grid
        grid_n, cell = 8, 0.26
        bev_cells = VGroup()
        for r in range(grid_n):
            for c in range(grid_n):
                cell_sq = Square(side_length=cell)
                cell_sq.set_stroke(color=COL_BLUE, width=0.6, opacity=0.5)
                cell_sq.set_fill(color=COL_NAVY, opacity=0.8)
                cell_sq.move_to(bev_center +
                                LEFT * (grid_n / 2 - c - 0.5) * cell +
                                DOWN * (grid_n / 2 - r - 0.5) * cell)
                bev_cells.add(cell_sq)
        self.play(Create(bev_cells), run_time=0.5)

        # Masked voxels (red, scattered non-uniformly)
        mask_indices = [3, 12, 19, 28, 37, 52, 44, 61]
        masked_cells = VGroup()
        for idx in mask_indices:
            m = bev_cells[idx].copy()
            m.set_fill(color=COL_RED, opacity=0.85)
            m.set_stroke(color=COL_RED, width=0.5)
            masked_cells.add(m)
        self.play(*[FadeIn(mc, scale=1.3) for mc in masked_cells],
                  lag_ratio=0.1, run_time=0.6)

        bev_lbl = Text("Reconstructing masked regions", font_size=12,
                       color=COL_WHITE, slant=ITALIC)
        bev_lbl.next_to(bev_cells, DOWN, buff=0.15)
        self.play(Write(bev_lbl), run_time=0.3)

        # Agent 2 helping arrow (dashed curve toward masked voxels)
        help_arr = CurvedArrow(ag2.get_right() + RIGHT * 0.1,
                               bev_cells[28].get_center(),
                               angle=-PI / 5, color=COL_GREEN,
                               stroke_width=2, tip_length=0.14)
        self.play(Create(help_arr), run_time=0.5)

        # Masked voxels fill green (reconstruction success)
        filled_cells = VGroup()
        for idx in mask_indices:
            f = bev_cells[idx].copy()
            f.set_fill(color=COL_INT8_GREEN, opacity=0.9)
            f.set_stroke(color=COL_GREEN, width=0.5)
            filled_cells.add(f)
        self.play(Transform(masked_cells, filled_cells),
                  run_time=0.6, rate_func=smooth)

        # Inductive bias callout
        bias_bg = RoundedRectangle(width=4.2, height=0.7, corner_radius=0.15,
                                   fill_color=COL_NAVY, fill_opacity=1,
                                   stroke_color=COL_GOLD, stroke_width=1.8)
        bias_txt = Text('"Can\'t see → ask another agent."', font_size=13,
                        color=COL_GOLD, slant=ITALIC, weight=BOLD)
        bias_bg.move_to(RIGHT * 3.5 + DOWN * 0.2)
        bias_txt.move_to(bias_bg.get_center())
        self.play(FadeIn(VGroup(bias_bg, bias_txt)), run_time=0.4)
        self.wait(0.8)

        # ═══════════════════════════════════════════════════════════
        # SECTION B — Results
        # ═══════════════════════════════════════════════════════════
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

        res_title = Text("CooPre Results", font_size=20,
                         color=COL_GOLD, weight=BOLD)
        res_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(res_title), run_time=0.2)

        # Bars:  Baseline 100% | CooPre 50% | CooPre 100%
        base_h = 3.5
        bar_data = [
            ("Baseline\n100% data", base_h,      COL_BLUE),
            ("CooPre\n50% data",    base_h,      COL_INT8_GREEN),
            ("CooPre\n100% data",   base_h * 1.05, COL_INT8_GREEN),
        ]
        bar_w = 0.8
        bar_gap = 1.8
        baseline_y = DOWN * 1.8

        ax_line = Line(LEFT * 2.5 + baseline_y, RIGHT * 3.0 + baseline_y,
                       color=COL_WHITE, stroke_width=1.5)
        self.play(Create(ax_line), run_time=0.2)

        bar_objs = []
        for i, (lbl, h, col) in enumerate(bar_data):
            x = -1.8 + i * bar_gap
            bar = Rectangle(width=bar_w, height=h,
                            fill_color=col, fill_opacity=1, stroke_width=0)
            bar.align_to(ax_line, DOWN).shift(RIGHT * x)
            b_lbl = Text(lbl, font_size=11, color=col)
            b_lbl.next_to(bar, DOWN, buff=0.1)
            bar_objs.append(VGroup(bar, b_lbl))
            start = bar.copy().scale([1, 0.01, 1]).align_to(ax_line, DOWN)
            self.play(Transform(start, bar), FadeIn(
                b_lbl), run_time=0.45, rate_func=smooth)
            bar_objs[-1] = VGroup(start, b_lbl)

        # "Same height" annotation (baseline vs CooPre 50%)
        b_top = bar_objs[0][0].get_top()
        c_top = bar_objs[1][0].get_top()
        horiz = DoubleArrow(b_top + LEFT * 0.2, c_top + RIGHT * 0.2,
                            buff=0.05, color=COL_GOLD, stroke_width=1.5, tip_length=0.12)
        horiz.shift(UP * 0.18)
        h_lbl = Text("50% data = same performance",
                     font_size=11, color=COL_GOLD)
        h_lbl.next_to(horiz, UP, buff=0.08)
        self.play(FadeIn(horiz), FadeIn(h_lbl), run_time=0.4)

        # "+4% AP" annotation (CooPre 100% vs baseline)
        diff_arr = DoubleArrow(bar_objs[0][0].get_top() + RIGHT * 4.1,
                               bar_objs[2][0].get_top() + RIGHT * 0.5,
                               buff=0.05, color=COL_GREEN, stroke_width=1.5, tip_length=0.12)
        diff_lbl = Text("+4% AP", font_size=12, color=COL_GREEN, weight=BOLD)
        diff_lbl.next_to(diff_arr, RIGHT, buff=0.1)
        self.play(FadeIn(diff_arr), FadeIn(diff_lbl), run_time=0.3)

        # Cross-domain badge
        xd_bg = RoundedRectangle(width=4.2, height=0.55, corner_radius=0.12,
                                 fill_color="#1E3A5F", fill_opacity=1,
                                 stroke_color=COL_BLUE, stroke_width=1.5)
        xd_txt = Text("Cross-domain pretraining > single-domain", font_size=12,
                      color=COL_LIGHT_BLUE)
        xd_bg.to_edge(DOWN, buff=0.6)
        xd_txt.move_to(xd_bg.get_center())
        self.play(FadeIn(VGroup(xd_bg, xd_txt)), run_time=0.3)

        paper = Text("CooPre  ·  IROS 2025", font_size=11,
                     color=COL_WHITE, slant=ITALIC)
        paper.to_corner(DR, buff=0.4)
        self.play(FadeIn(paper), run_time=0.2)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
