# beyond/scenes/part05/p05_s04_urbansim.py
# ─────────────────────────────────────────────────────────────────
# P5-04  URBANSIM — 180 NGÀY VÀ 3 GIỜ  (~55s)
#
# Bar "Traditional: 180 GPU-days" quá dài, chạy ra ngoài màn hình.
# Bottleneck: CPU→GPU ping-pong.
# UrbanSim: everything on GPU, no transfer.
# Counter: 180 days → 3 hours.
# 2620 FPS badge.
#
# Render:  manim -ql "beyond/scenes/part05/p05_s04_urbansim.py" P05S04UrbanSim
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block, pipeline_block_entrance,
    pipeline_arrow_entrance, glow_pulse,
    BG_PANEL, P5_PHYSICAL, GOLD, GOLD_GLOW,
    FP32_HEAVY, INT8_LIGHT, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST, RED_ALERT,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=77)


class P05S04UrbanSim(BeyondScene):
    PART_COLOR = P5_PHYSICAL

    def construct(self):
        title_mob, sep = self.open("UrbanSim — 180 GPU-Days vs 3 Hours")
        self.wait(0.2)

        # ── Traditional pipeline bottleneck ───────────────────
        boxes_old = ["CPU\n(physics)", "TRANSFER\n⚠ bottleneck", "GPU\n(neural net)", "TRANSFER\n⚠ back"]
        colors_old = [TEXT_DIM, RED_ALERT, TEXT_DIM, RED_ALERT]
        blocks_old = VGroup(*[
            pipeline_block(lbl, width=1.9, height=0.80,
                           border_color=col, fill_color=BG_PANEL, font_size=SIZE_MICRO)
            for lbl, col in zip(boxes_old, colors_old)
        ]).arrange(RIGHT, buff=0.30).move_to(UP * 1.8)

        old_lbl = Text("Traditional Pipeline", font_size=SIZE_MICRO + 2,
                       color=TEXT_DIM, font=FONT_PRIMARY, weight=BOLD)
        old_lbl.next_to(blocks_old, UP, buff=0.15)

        self.play(FadeIn(old_lbl, shift=DOWN * 0.06, run_time=0.28))
        self.play(
            LaggedStart(*[pipeline_block_entrance(b, colors_old[i])
                          for i, b in enumerate(blocks_old)], lag_ratio=0.15),
        )

        # Bottleneck arrows shake
        for i in [1, 3]:
            blk = blocks_old[i]
            self.play(
                blk.animate(run_time=0.07).shift(UP * 0.07),
                blk.animate(run_time=0.07).shift(DOWN * 0.14),
                blk.animate(run_time=0.07).shift(UP * 0.07),
            )
        self.wait(0.3)

        # ── UrbanSim pipeline ─────────────────────────────────
        boxes_new = ["GPU\n(physics)", "GPU\n(render)", "GPU\n(neural net)", "GPU\n(output)"]
        blocks_new = VGroup(*[
            pipeline_block(lbl, width=1.9, height=0.80,
                           border_color=GREEN_SIGNAL, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO)
            for lbl in boxes_new
        ]).arrange(RIGHT, buff=0.30).move_to(UP * 0.3)

        new_lbl = Text("UrbanSim — Everything on GPU", font_size=SIZE_MICRO + 2,
                       color=GREEN_SIGNAL, font=FONT_PRIMARY, weight=BOLD)
        new_lbl.next_to(blocks_new, UP, buff=0.15)

        # Arrows between GPU blocks (smooth, electric)
        new_arrs = [
            Arrow(blocks_new[i].get_right(), blocks_new[i+1].get_left(),
                  buff=0.05, color=GREEN_SIGNAL, stroke_width=1.8, tip_length=0.15)
            for i in range(len(blocks_new) - 1)
        ]

        self.play(FadeIn(new_lbl, shift=DOWN * 0.06, run_time=0.28))
        self.play(
            LaggedStart(*[pipeline_block_entrance(b, GREEN_SIGNAL)
                          for b in blocks_new], lag_ratio=0.12),
        )
        self.play(
            LaggedStart(*[pipeline_arrow_entrance(a, style="electric")
                          for a in new_arrs], lag_ratio=0.10),
        )
        self.wait(0.3)

        # ── Comparison bars ───────────────────────────────────
        BAR_Y = -1.4
        bar_old = Rectangle(width=7.5, height=0.58,
                            fill_color=FP32_HEAVY, fill_opacity=0.80,
                            stroke_width=0)
        bar_old.align_to(LEFT * 6.5, LEFT).set_y(BAR_Y)

        bar_new = Rectangle(width=0.0, height=0.58,
                            fill_color=GREEN_SIGNAL, fill_opacity=0.90,
                            stroke_width=0)
        bar_new.align_to(LEFT * 6.5, LEFT).set_y(BAR_Y - 0.75)

        lbl_old = Text("Traditional: 180 GPU-days", font_size=SIZE_MICRO + 1,
                       color=FP32_HEAVY, font=FONT_PRIMARY)
        lbl_new = Text("UrbanSim:   3 hours", font_size=SIZE_MICRO + 1,
                       color=GREEN_SIGNAL, font=FONT_PRIMARY)
        lbl_old.next_to(bar_old, RIGHT, buff=0.15)
        lbl_new.set_y(bar_new.get_center()[1])
        lbl_new.to_edge(LEFT, buff=0.8)

        self.play(FadeIn(bar_old, run_time=0.50), FadeIn(lbl_old, run_time=0.30))
        self.play(
            bar_new.animate(run_time=0.80, rate_func=smooth)
                   .stretch_to_fit_width(0.18)
                   .align_to(LEFT * 6.5, LEFT)
                   .set_y(BAR_Y - 0.75),
            FadeIn(lbl_new, run_time=0.30),
        )
        self.play(
            Flash(bar_new.get_right(), color=GREEN_SIGNAL,
                  flash_radius=0.35, num_lines=6, run_time=0.28),
        )
        self.wait(0.3)

        # ── FPS badge ─────────────────────────────────────────
        fps_txt = Text("2,620 FPS  ·  256 environments  ·  11.2 GB VRAM",
                       font_size=SIZE_MICRO + 2, color=GOLD,
                       font=FONT_PRIMARY, weight=BOLD)
        fps_bg = RoundedRectangle(corner_radius=0.08,
                                  width=fps_txt.width + 0.5, height=0.48,
                                  fill_color="#1A1200", fill_opacity=1.0,
                                  stroke_color=GOLD, stroke_width=1.5)
        fps_txt.move_to(fps_bg)
        fps_badge = VGroup(fps_bg, fps_txt).to_edge(DOWN, buff=0.42)

        self.play(
            GrowFromCenter(fps_bg, run_time=0.28),
            FadeIn(fps_txt, run_time=0.22),
            Flash(fps_bg.get_center(), color=GOLD,
                  flash_radius=1.0, num_lines=10, run_time=0.40),
        )
        self.wait(1.5)

        self.close()
