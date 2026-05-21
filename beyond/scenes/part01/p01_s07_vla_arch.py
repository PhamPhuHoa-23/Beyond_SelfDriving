# beyond/scenes/part01/p01_s07_vla_arch.py
# ─────────────────────────────────────────────────────────────────
# P1-07  VLA ARCHITECTURE DETAILS  (~65s)
#
# 3 kiến trúc hiện ra lần lượt với animation đặc trưng:
#
# BEVDriver (2021): 3D point cloud → BEV compression → LLM
#   Point cloud rối loạn → "ép phẳng" xuống 2D → grid teal phát sáng
#
# EMMA (2022): Chain-of-thought typewriter — ALL outputs through language
#   Input image → language token flow → concurrent outputs
#
# DriveVLM (2023): Fast track (gray) || Slow track (colored) parallel
#   Two tracks race → merge at output
#
# Render:  manim -ql "beyond/scenes/part01/p01_s07_vla_arch.py" P01S07VlaArch
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block, pipeline_block_entrance,
    pipeline_arrow_entrance,
    BG_PANEL,
    P2_COOP, BLUE_ELECTRIC, P1_FOUNDATION,
    GREEN_SIGNAL, TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=31)


class P01S07VlaArch(BeyondScene):
    PART_COLOR = P1_FOUNDATION

    def construct(self):
        title_mob, sep = self.open("VLA Deep Dive — Three Architectures")
        self.wait(0.2)

        # ══════════════════════════════════════════════════════
        # BEVDRIVER (2021) — 3D → BEV
        # ══════════════════════════════════════════════════════
        arch_title1 = Text("BEVDriver (2021)", font_size=SIZE_LABEL,
                           color=P2_COOP, font=FONT_PRIMARY, weight=BOLD)
        arch_title1.to_edge(UP, buff=0.90)
        self.play(FadeIn(arch_title1, shift=DOWN * 0.08, run_time=0.30))

        # 3D Point cloud (scattered dots)
        n_pts = 30
        cloud = VGroup(*[
            Dot(radius=float(RNG.uniform(0.025, 0.055)),
                color=P2_COOP,
                fill_opacity=float(RNG.uniform(0.4, 0.9)))
            .move_to([
                float(RNG.uniform(-5.5, -2.5)),
                float(RNG.uniform(-1.2, 1.2)),
                0,
            ])
            for _ in range(n_pts)
        ])
        cloud_lbl = Text("3D LiDAR Point Cloud",
                         font_size=SIZE_MICRO + 1, color=P2_COOP, font=FONT_PRIMARY)
        cloud_lbl.move_to(LEFT * 4.0 + DOWN * 1.6)

        self.play(
            LaggedStart(*[GrowFromCenter(d, run_time=0.06) for d in cloud],
                        lag_ratio=0.03),
        )
        self.play(FadeIn(cloud_lbl, run_time=0.22))
        self.wait(0.2)

        # COMPRESS arrow → BEV grid
        compress_arr = Arrow(
            np.array([-2.0, 0.0, 0]), np.array([-0.5, 0.0, 0]),
            buff=0.05, color=P2_COOP, stroke_width=2.0, tip_length=0.18,
        )
        compress_lbl = Text("compress\nto 2D", font_size=SIZE_MICRO - 1,
                            color=TEXT_DIM, font=FONT_PRIMARY, line_spacing=0.38)
        compress_lbl.next_to(compress_arr, UP, buff=0.08)

        # BEV grid (bird's eye view)
        bev = VGroup()
        for r in range(6):
            for c in range(6):
                sq = Square(side_length=0.30,
                            fill_color=P2_COOP,
                            fill_opacity=float(RNG.uniform(0.15, 0.55)),
                            stroke_color=P2_COOP, stroke_width=0.5,
                            stroke_opacity=0.6)
                sq.move_to(np.array([0.3 + c * 0.32, 0.9 - r * 0.32, 0]))
                bev.add(sq)
        bev_lbl = Text("BEV Grid", font_size=SIZE_MICRO + 1,
                       color=P2_COOP, font=FONT_PRIMARY)
        bev_lbl.next_to(bev, DOWN, buff=0.10)

        self.play(
            Create(compress_arr, run_time=0.30),
            FadeIn(compress_lbl, run_time=0.22),
        )
        self.play(
            cloud.animate(run_time=0.70, rate_func=smooth)
                 .set_fill(opacity=0.0).shift(RIGHT * 0.6),
            LaggedStart(*[GrowFromCenter(sq, run_time=0.05) for sq in bev],
                        lag_ratio=0.015),
        )
        self.play(FadeIn(bev_lbl, run_time=0.20))

        # Arrow to LLM
        llm_arrow = Arrow(bev.get_right() + RIGHT * 0.05,
                          np.array([2.8, 0.3, 0]),
                          buff=0.05, color=P2_COOP, stroke_width=1.8, tip_length=0.16)
        llm_box = pipeline_block("LLM\nReasoning", width=2.0, height=0.80,
                                 border_color=P2_COOP, fill_color=BG_PANEL,
                                 font_size=SIZE_MICRO + 2)
        llm_box.move_to(np.array([3.5, 0.3, 0]))
        self.play(Create(llm_arrow, run_time=0.25),
                  pipeline_block_entrance(llm_box, P2_COOP))

        insight1 = Text("First to use LLM on Bird's Eye View features",
                        font_size=SIZE_MICRO + 1, color=TEXT_DIM,
                        font=FONT_PRIMARY, slant=ITALIC)
        insight1.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(insight1, shift=UP * 0.06, run_time=0.28))
        self.wait(1.0)

        # Clear
        self.play(
            FadeOut(VGroup(arch_title1, cloud, cloud_lbl, compress_arr,
                           compress_lbl, bev, bev_lbl, llm_arrow, llm_box,
                           insight1), run_time=0.45),
        )

        # ══════════════════════════════════════════════════════
        # EMMA (2022) — Language as universal output
        # ══════════════════════════════════════════════════════
        arch_title2 = Text("EMMA (2022)", font_size=SIZE_LABEL,
                           color=BLUE_ELECTRIC, font=FONT_PRIMARY, weight=BOLD)
        arch_title2.to_edge(UP, buff=0.90)
        self.play(FadeIn(arch_title2, shift=DOWN * 0.08, run_time=0.28))

        # Input
        input_box = pipeline_block("Camera Images", width=2.2, height=0.72,
                                   border_color=BLUE_ELECTRIC, fill_color=BG_PANEL,
                                   font_size=SIZE_MICRO + 1)
        input_box.move_to(LEFT * 4.5 + UP * 0.3)
        self.play(pipeline_block_entrance(input_box, BLUE_ELECTRIC))

        # Language model center
        lang_box = pipeline_block("One\nLanguage Model", width=2.4, height=1.0,
                                  border_color=BLUE_ELECTRIC, fill_color=BG_PANEL,
                                  font_size=SIZE_MICRO + 2)
        lang_box.move_to(ORIGIN + UP * 0.3)
        arr_in = Arrow(input_box.get_right(), lang_box.get_left(),
                       buff=0.05, color=BLUE_ELECTRIC, stroke_width=1.8, tip_length=0.15)
        self.play(Create(arr_in, run_time=0.25),
                  pipeline_block_entrance(lang_box, BLUE_ELECTRIC))

        # Chain-of-thought typewriter (small, right side)
        cot_lines = [
            "There is a pedestrian crossing...",
            "Traffic light is red...",
            "→ Brake. Yield.",
            "→ Detect bounding boxes.",
            "→ Update road graph.",
        ]
        cot_mobs = VGroup()
        prev = lang_box
        for i, line in enumerate(cot_lines):
            col = BLUE_ELECTRIC if i < 2 else GREEN_SIGNAL
            m = Text(line, font_size=SIZE_MICRO - 1, color=col,
                     font=FONT_PRIMARY, slant=ITALIC if i < 2 else NORMAL)
            m.next_to(prev, DOWN, buff=0.06)
            m.to_edge(RIGHT, buff=0.5)
            cot_mobs.add(m)
            self.play(AddTextLetterByLetter(m, run_time=0.07 * len(line),
                                            rate_func=linear))
            prev = m

        insight2 = Text("Every task output passes through language tokens",
                        font_size=SIZE_MICRO + 1, color=TEXT_DIM,
                        font=FONT_PRIMARY, slant=ITALIC)
        insight2.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(insight2, shift=UP * 0.06, run_time=0.28))
        self.wait(0.8)

        self.play(FadeOut(VGroup(arch_title2, input_box, arr_in, lang_box,
                                 cot_mobs, insight2), run_time=0.40))

        # ══════════════════════════════════════════════════════
        # DRIVEVLM (2023) — Fast / Slow dual track
        # ══════════════════════════════════════════════════════
        arch_title3 = Text("DriveVLM (2023)", font_size=SIZE_LABEL,
                           color=P1_FOUNDATION, font=FONT_PRIMARY, weight=BOLD)
        arch_title3.to_edge(UP, buff=0.90)
        self.play(FadeIn(arch_title3, shift=DOWN * 0.08, run_time=0.28))

        # Fast track (top, gray/green)
        fast_track = VGroup(
            pipeline_block("Sensor Input", width=1.8, height=0.65,
                           border_color=TEXT_DIM, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO).move_to(LEFT * 4.0 + UP * 1.0),
            pipeline_block("Traditional\nPipeline", width=1.8, height=0.65,
                           border_color=TEXT_DIM, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO).move_to(LEFT * 1.8 + UP * 1.0),
            pipeline_block("Fast\nDecision", width=1.8, height=0.65,
                           border_color=GREEN_SIGNAL, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO).move_to(RIGHT * 0.4 + UP * 1.0),
        )
        fast_lbl = Text("FAST track — routine scenes",
                        font_size=SIZE_MICRO + 1, color=TEXT_DIM, font=FONT_PRIMARY)
        fast_lbl.move_to(LEFT * 2.0 + UP * 1.8)

        # Slow track (bottom, colored)
        slow_track = VGroup(
            pipeline_block("Sensor Input", width=1.8, height=0.65,
                           border_color=P1_FOUNDATION, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO).move_to(LEFT * 4.0 + DOWN * 0.5),
            pipeline_block("VLM\nReasoning", width=1.8, height=0.65,
                           border_color=P1_FOUNDATION, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO).move_to(LEFT * 1.8 + DOWN * 0.5),
            pipeline_block("Slow\nDecision", width=1.8, height=0.65,
                           border_color=P1_FOUNDATION, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO).move_to(RIGHT * 0.4 + DOWN * 0.5),
        )
        slow_lbl = Text("SLOW track — complex/ambiguous scenes",
                        font_size=SIZE_MICRO + 1, color=P1_FOUNDATION, font=FONT_PRIMARY)
        slow_lbl.move_to(LEFT * 2.0 + DOWN * 1.3)

        # Merge at output
        merge_box = pipeline_block("Merged\nOutput", width=1.8, height=0.80,
                                   border_color=GREEN_SIGNAL, fill_color=BG_PANEL,
                                   font_size=SIZE_MICRO + 1)
        merge_box.move_to(RIGHT * 3.2 + UP * 0.25)

        self.play(
            FadeIn(fast_lbl, shift=DOWN * 0.06, run_time=0.22),
            FadeIn(slow_lbl, shift=DOWN * 0.06, run_time=0.22),
        )
        self.play(
            LaggedStart(*[pipeline_block_entrance(b, TEXT_DIM) for b in fast_track],
                        lag_ratio=0.15),
        )
        self.play(
            LaggedStart(*[pipeline_block_entrance(b, P1_FOUNDATION) for b in slow_track],
                        lag_ratio=0.15),
        )

        # Fast → merge, Slow → merge arrows
        arr_f = Arrow(fast_track[-1].get_right(), merge_box.get_top() + LEFT * 0.2,
                      buff=0.05, color=TEXT_DIM, stroke_width=1.5, tip_length=0.13)
        arr_s = Arrow(slow_track[-1].get_right(), merge_box.get_bottom() + LEFT * 0.2,
                      buff=0.05, color=P1_FOUNDATION, stroke_width=1.5, tip_length=0.13)
        self.play(Create(arr_f, run_time=0.25), Create(arr_s, run_time=0.25))
        self.play(pipeline_block_entrance(merge_box, GREEN_SIGNAL))

        insight3 = Text("Best of both worlds — speed + intelligence",
                        font_size=SIZE_MICRO + 1, color=TEXT_DIM,
                        font=FONT_PRIMARY, slant=ITALIC)
        insight3.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(insight3, shift=UP * 0.06, run_time=0.28))
        self.wait(1.5)

        self.close()
