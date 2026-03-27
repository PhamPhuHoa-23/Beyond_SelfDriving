"""
Scene 4-08 — QuantV2X: Full-Pipeline Quantization
===================================================
Section A — FP32 → INT8 concept (32 vs 8 squares).
Section B — V2X-specific challenge (different activation distributions).
Section C — Two-layer diagram: model quantization + communication codebook (300×).
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


FP32_RED = "#E74C3C"
INT8_GREEN = "#2ECC71"


class P04S08QuantV2X(Scene):
    """
    A — 32 red squares → 8 green squares (FP32 to INT8) + impact list
    B — Two agent distributions (different shapes) + naive clip zone
    C — Agent block → Layer 1 (FP32→INT8) → Layer 2 codebook (300× shrink)
    """

    def construct(self):
        self.camera.background_color = "#0F172A"

        title = Text("QuantV2X — Full-Pipeline Quantization", font_size=20,
                     color=COL_GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.3)

        # ═══ SECTION A — FP32 → INT8 ═══════════════════════════════
        def bit_squares(n, color, start_x, y):
            grp = VGroup()
            for i in range(n):
                sq = Square(side_length=0.18,
                            fill_color=color, fill_opacity=1, stroke_width=0)
                sq.move_to([start_x + i * 0.22, y, 0])
                grp.add(sq)
            return grp

        fp32_row = bit_squares(32, FP32_RED,   -3.9, 1.5)
        int8_row = bit_squares(8,  INT8_GREEN, -1.0, 1.5)

        fp32_lbl = Text("FP32", font_size=16, color=FP32_RED, weight=BOLD)
        int8_lbl = Text("INT8", font_size=16, color=INT8_GREEN, weight=BOLD)
        fp32_lbl.next_to(fp32_row, LEFT, buff=0.2)
        int8_lbl.next_to(int8_row, LEFT, buff=0.2)

        quant_arr = Arrow(fp32_row.get_right(), int8_row.get_left(),
                          buff=0.12, color=COL_WHITE, stroke_width=2, tip_length=0.14)
        quant_lbl = Text("quantize", font_size=11, color=COL_WHITE)
        quant_lbl.next_to(quant_arr, UP, buff=0.06)

        self.play(FadeIn(fp32_lbl), FadeIn(fp32_row), run_time=0.4)
        self.play(GrowArrow(quant_arr), FadeIn(quant_lbl), run_time=0.3)
        self.play(FadeIn(int8_lbl), FadeIn(int8_row), run_time=0.3)

        # Impact list
        impacts = [
            "FP multiply → INT add  (much cheaper)",
            "Memory: 4× smaller",
            "Edge chips: INT8 hardware throughput ↑",
        ]
        imp_grp = VGroup(*[
            Text(f"✓  {t}", font_size=12, color=COL_WHITE) for t in impacts
        ]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        imp_grp.move_to(RIGHT * 2.5 + UP * 1.5)
        self.play(FadeIn(imp_grp), run_time=0.4)
        self.wait(0.4)

        # ═══ SECTION B — V2X distribution challenge ════════════════
        self.play(FadeOut(VGroup(fp32_row, fp32_lbl, int8_row, int8_lbl,
                                 quant_arr, quant_lbl, imp_grp)),
                  run_time=0.3)

        axes = Axes(
            x_range=[-3, 3.5, 1], y_range=[0, 1.2, 0.5],
            x_length=5.5, y_length=2.2,
            axis_config={"color": COL_WHITE, "stroke_width": 1.5,
                         "include_numbers": False},
            tips=False,
        ).move_to(DOWN * 0.2)

        dist1 = axes.plot(lambda x: np.exp(-0.7 * x**2),            x_range=[-3, 3],
                          color=COL_BLUE, stroke_width=2)
        dist2 = axes.plot(lambda x: 0.7 * np.exp(-0.4 * (x - 0.8)**2), x_range=[-3, 3.5],
                          color=COL_INFRA_ORANGE, stroke_width=2)

        clip_zone = axes.get_area(
            dist2, x_range=[2.2, 3.5], color=FP32_RED, opacity=0.35)

        d1_lbl = Text("Agent 1 activations", font_size=11, color=COL_BLUE)
        d2_lbl = Text("Agent 2 activations\n(different dist.)",
                      font_size=11, color=COL_INFRA_ORANGE)
        d1_lbl.next_to(axes, UR, buff=0.1).shift(LEFT * 2.5 + DOWN * 0.3)
        d2_lbl.next_to(axes, UR, buff=0.1).shift(LEFT * 0.5 + DOWN * 0.6)
        clip_lbl = Text("Naive clip → loses\ncomplementary info  ✗",
                        font_size=11, color=FP32_RED)
        clip_lbl.move_to(axes.c2p(2.8, 0.9))

        self.play(Create(axes), run_time=0.3)
        self.play(Create(dist1), FadeIn(d1_lbl), run_time=0.3)
        self.play(Create(dist2), FadeIn(d2_lbl), run_time=0.3)
        self.play(FadeIn(clip_zone), Write(clip_lbl), run_time=0.3)
        self.wait(0.5)

        # ═══ SECTION C — Two-layer diagram ═════════════════════════
        self.play(FadeOut(Group(axes, dist1, dist2, d1_lbl, d2_lbl, clip_zone, clip_lbl)),
                  run_time=0.3)

        # Agent block
        agent_box = RoundedRectangle(width=1.8, height=1.0, corner_radius=0.15,
                                     fill_color="#1E3A5F", fill_opacity=1,
                                     stroke_color=COL_BLUE, stroke_width=2)
        agent_lbl = Text("Agent\n(NN)", font_size=13,
                         color=COL_BLUE, weight=BOLD)
        agent_box.move_to(LEFT * 4.5 + DOWN * 0.4)
        agent_lbl.move_to(agent_box.get_center())

        # Layer 1 box
        l1_box = RoundedRectangle(width=2.4, height=0.7, corner_radius=0.12,
                                  fill_color="#1E3A5F", fill_opacity=1,
                                  stroke_color=INT8_GREEN, stroke_width=1.8)
        l1_txt = Text("Layer 1: FP32 → INT8", font_size=12,
                      color=INT8_GREEN, weight=BOLD)
        l1_box.move_to(LEFT * 1.5 + DOWN * 0.4)
        l1_txt.move_to(l1_box.get_center())

        # BEV feature (uncompressed, wide = FP32_RED)
        bev_big = Rectangle(width=2.5, height=0.45, fill_color=FP32_RED,
                            fill_opacity=0.9, stroke_width=0)
        bev_big.move_to(RIGHT * 1.2 + DOWN * 0.4)
        bev_lbl1 = Text("BEV features (FP32)", font_size=10, color=FP32_RED)
        bev_lbl1.next_to(bev_big, UP, buff=0.08)

        # Layer 2 box
        l2_box = RoundedRectangle(width=2.4, height=0.7, corner_radius=0.12,
                                  fill_color="#1B4332", fill_opacity=1,
                                  stroke_color=INT8_GREEN, stroke_width=1.8)
        l2_txt = Text("Layer 2: Codebook (300×)", font_size=12,
                      color=INT8_GREEN, weight=BOLD)
        l2_box.move_to(RIGHT * 1.2 + UP * 0.9)
        l2_txt.move_to(l2_box.get_center())

        # Compressed sliver (INT8_GREEN, tiny)
        bev_small = Rectangle(width=0.04, height=0.45, fill_color=INT8_GREEN,
                              fill_opacity=0.9, stroke_width=0)
        bev_small.move_to(bev_big.get_left() + RIGHT * 0.02)

        # 300× annotation
        brace_bg = RoundedRectangle(width=2.0, height=0.45, corner_radius=0.1,
                                    fill_color=COL_NAVY, fill_opacity=1,
                                    stroke_color=COL_GOLD, stroke_width=1.5)
        brace_txt = Text("300× smaller", font_size=13,
                         color=COL_GOLD, weight=BOLD)
        brace_bg.next_to(bev_big, DOWN, buff=0.3)
        brace_txt.move_to(brace_bg.get_center())

        bw_badge = RoundedRectangle(width=2.6, height=0.42, corner_radius=0.1,
                                    fill_color="#1B4332", fill_opacity=1,
                                    stroke_color=COL_GREEN, stroke_width=1.5)
        bw_txt = Text("Fits V2X bandwidth", font_size=12, color=COL_GREEN)
        bw_badge.next_to(brace_bg, RIGHT, buff=0.4)
        bw_txt.move_to(bw_badge.get_center())

        self.play(FadeIn(VGroup(agent_box, agent_lbl)), run_time=0.3)
        a_to_l1 = Arrow(agent_box.get_right(), l1_box.get_left(),
                        buff=0.05, color=COL_BLUE, stroke_width=2, tip_length=0.12)
        self.play(GrowArrow(a_to_l1), FadeIn(
            VGroup(l1_box, l1_txt)), run_time=0.4)
        self.play(FadeIn(bev_big), FadeIn(bev_lbl1), run_time=0.3)
        self.play(FadeIn(VGroup(l2_box, l2_txt)), run_time=0.3)

        # 300× compression transform
        self.play(Transform(bev_big, bev_small.copy().set_fill(
            INT8_GREEN)), run_time=0.8)
        self.play(FadeIn(VGroup(brace_bg, brace_txt)),
                  FadeIn(VGroup(bw_badge, bw_txt)), run_time=0.4)

        # Final note
        note = Text("Acceptable performance drop — edge-deployable V2X",
                    font_size=13, color=COL_WHITE, slant=ITALIC)
        note.to_edge(DOWN, buff=0.5)
        self.play(Write(note), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
