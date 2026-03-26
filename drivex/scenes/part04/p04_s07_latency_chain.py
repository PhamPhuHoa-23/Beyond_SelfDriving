"""
Scene 4-07 — Inference Bottleneck: Latency Chain
==================================================
Section A — 3-block pipeline (Local → Comm → Fusion) with time budget bar.
Section B — Arithmetic cost: FP32 multiply vs add, memory DRAM vs SRAM.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P04S07LatencyChain(Scene):
    """
    A — V2X inference latency chain (3 stages)
    B — FP32 arithmetic cost + DRAM vs SRAM memory cost comparison
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("Inference Bottleneck: Latency Chain", font_size=20,
                        color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ SECTION A — Latency chain ════════════════════════════
        blocks = [
            ("Local\nInference", COL_BLUE,          "#1E3A5F"),
            ("V2X\nComm",        COL_INFRA_ORANGE,  "#3D1A00"),
            ("Fusion\nInference", COL_GREEN,         "#1B4332"),
        ]
        pipe_blocks = []
        for label, stroke, fill in blocks:
            b = RoundedRectangle(width=2.4, height=1.0, corner_radius=0.15,
                                  fill_color=fill, fill_opacity=1,
                                  stroke_color=stroke, stroke_width=2)
            t = Text(label, font_size=14, color=stroke, weight=BOLD)
            t.move_to(b.get_center())
            pipe_blocks.append(VGroup(b, t))

        pipeline = VGroup(*pipe_blocks).arrange(RIGHT, buff=0.1)
        pipeline.move_to(UP * 0.9)

        arrows = []
        for i in range(len(pipe_blocks) - 1):
            arr = Arrow(pipe_blocks[i].get_right(), pipe_blocks[i + 1].get_left(),
                         buff=0.0, color=COL_WHITE, stroke_width=2, tip_length=0.14)
            arrows.append(arr)

        self.play(*[FadeIn(b) for b in pipe_blocks], run_time=0.4)
        for arr in arrows:
            self.play(GrowArrow(arr), run_time=0.2)

        # Time budget bar (tight, red)
        budget_bar = Rectangle(width=6.5, height=0.28,
                                fill_color=COL_RED, fill_opacity=0.85, stroke_width=0)
        budget_bar.next_to(pipeline, DOWN, buff=0.25)
        budget_lbl = Text("Total time budget: FIXED (real-time constraint)",
                           font_size=12, color=COL_RED)
        budget_lbl.next_to(budget_bar, RIGHT, buff=0.2)

        self.play(Create(budget_bar), FadeIn(budget_lbl), run_time=0.4)
        self.wait(0.4)

        # ═══ SECTION B — Arithmetic + Memory cost ═════════════════
        self.play(FadeOut(VGroup(pipeline[0], pipeline[1], pipeline[2],
                                  *arrows, budget_bar, budget_lbl)),
                  run_time=0.3)

        # FP32 multiply vs add bars
        bar_baseline = DOWN * 0.5
        fp32_mul = Rectangle(width=0.5, height=3.2, fill_color=COL_RED,
                               fill_opacity=1, stroke_width=0)
        fp32_mul.align_to(bar_baseline, DOWN).shift(LEFT * 3.5)
        fp32_add = Rectangle(width=0.5, height=1.2, fill_color=COL_BLUE,
                               fill_opacity=1, stroke_width=0)
        fp32_add.align_to(bar_baseline, DOWN).shift(LEFT * 2.5)

        ax_line2 = Line(LEFT * 4.0 + bar_baseline, LEFT * 1.8 + bar_baseline,
                         color=COL_WHITE, stroke_width=1.5)
        self.play(Create(ax_line2), run_time=0.2)

        ml_t = Text("FP32\nMultiply", font_size=11, color=COL_RED)
        ml_t.next_to(fp32_mul, DOWN, buff=0.08)
        al_t = Text("FP32\nAdd", font_size=11, color=COL_BLUE)
        al_t.next_to(fp32_add, DOWN, buff=0.08)

        self.play(
            Transform(fp32_mul.copy().scale([1, 0.01, 1]).align_to(ax_line2, DOWN), fp32_mul),
            run_time=0.4, rate_func=smooth
        )
        self.play(FadeIn(fp32_mul), FadeIn(ml_t), run_time=0.1)
        self.play(
            Transform(fp32_add.copy().scale([1, 0.01, 1]).align_to(ax_line2, DOWN), fp32_add),
            run_time=0.3, rate_func=smooth
        )
        self.play(FadeIn(fp32_add), FadeIn(al_t), run_time=0.1)

        quad_txt = Text("Double precision → ~4× cost", font_size=12, color=COL_RED,
                         slant=ITALIC)
        quad_txt.move_to(LEFT * 3.0 + UP * 2.2)
        self.play(Write(quad_txt), run_time=0.3)
        self.wait(0.3)

        # Memory access bars (DRAM vs SRAM)
        dram_bar = Rectangle(width=4.2, height=0.38, fill_color=COL_RED,
                               fill_opacity=0.9, stroke_width=0)
        sram_bar = Rectangle(width=0.15, height=0.38, fill_color=COL_INT8_GREEN,
                               fill_opacity=0.9, stroke_width=0)
        dram_bar.move_to(RIGHT * 1.8 + bar_baseline + UP * 0.9)
        sram_bar.align_to(dram_bar, LEFT).move_to(dram_bar.get_center() + DOWN * 0.6)

        # Align left
        dram_bar.align_to(RIGHT * (-0.3), LEFT)
        sram_bar.align_to(RIGHT * (-0.3), LEFT)
        dram_bar.move_to(np.array([-0.3 + dram_bar.width / 2, bar_baseline[1] + 0.9, 0]))
        sram_bar.move_to(np.array([-0.3 + sram_bar.width / 2, bar_baseline[1] + 0.3, 0]))

        dram_lbl = Text("DRAM: 640 pJ / access", font_size=12, color=COL_RED)
        sram_lbl = Text("SRAM: 5 pJ / access", font_size=12, color=COL_INT8_GREEN)
        diff_lbl = Text("128× more expensive", font_size=13, color=COL_RED, weight=BOLD)
        dram_lbl.next_to(dram_bar, RIGHT, buff=0.12)
        sram_lbl.next_to(sram_bar, RIGHT, buff=0.12)
        diff_lbl.move_to(RIGHT * 2.0 + bar_baseline + DOWN * 0.4)

        self.play(FadeIn(dram_bar), FadeIn(dram_lbl), run_time=0.4)
        self.play(FadeIn(sram_bar), FadeIn(sram_lbl), run_time=0.3)
        self.play(Write(diff_lbl), run_time=0.3)

        note = Text("Millions of params × DRAM cost = edge hardware problem",
                     font_size=13, color=COL_WHITE, slant=ITALIC)
        note.to_edge(DOWN, buff=0.6)
        self.play(Write(note), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
