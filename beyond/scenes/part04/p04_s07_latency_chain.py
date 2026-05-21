# beyond/scenes/part04/p04_s07_latency_chain.py
# ─────────────────────────────────────────────────────────────────
# P4-07  LATENCY CHAIN  (~45s)
#
# End-to-end latency breakdown: 5 stages trong pipeline.
# Mỗi stage có bar riêng grow up, counter.
# Total time = sum visible.
# QuantV2X cuts communication latency dramatically.
#
# Render:  manim -ql "beyond/scenes/part04/p04_s07_latency_chain.py" P04S07LatencyChain
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    P4_EFFICIENT, RED_ALERT, GREEN_SIGNAL, GOLD, CYAN_NEON,
    TEXT_WHITE, TEXT_DIM, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

STAGES = [
    ("Sensing\n& capture",  18,  CYAN_NEON),
    ("Encoding\n(FP32)",    45,  RED_ALERT),
    ("Transmission\n(V2X)", 60,  RED_ALERT),     # biggest bottleneck
    ("Decoding\n& fuse",    30,  P4_EFFICIENT),
    ("Inference\n& output", 22,  GREEN_SIGNAL),
]

AFTER_QUANT = [18, 12, 5, 30, 22]    # QuantV2X cuts encoding+transmission


class P04S07LatencyChain(BeyondScene):
    PART_COLOR = P4_EFFICIENT

    def construct(self):
        title_mob, sep = self.open("V2X Latency Chain — Where Time Goes")
        self.wait(0.2)

        # ── Bar chart (vertical) ──────────────────────────────
        n = len(STAGES)
        bar_w = 1.0
        bar_spacing = 2.0
        max_val = max(v for _, v, _ in STAGES)
        max_h = 3.2
        bottom_y = -2.2

        # Y axis
        y_ax = Line([-5.5, bottom_y, 0], [-5.5, bottom_y + max_h + 0.3, 0],
                    stroke_color=TEXT_DIM, stroke_width=1.2)
        x_ax = Line([-5.5, bottom_y, 0], [4.5, bottom_y, 0],
                    stroke_color=TEXT_DIM, stroke_width=1.2)
        self.play(Create(y_ax, run_time=0.25), Create(x_ax, run_time=0.30))

        y_lbl = Text("Latency (ms)", font_size=SIZE_MICRO, color=TEXT_DIM,
                     font=FONT_PRIMARY).rotate(PI/2)
        y_lbl.next_to(y_ax, LEFT, buff=0.12)
        self.play(FadeIn(y_lbl, run_time=0.22))

        bars = []
        bar_xs = np.linspace(-4.0, 3.5, n)

        for i, ((name, val, col), bx) in enumerate(zip(STAGES, bar_xs)):
            target_h = (val / max_val) * max_h
            bar = Rectangle(width=bar_w, height=0.01,
                            fill_color=col, fill_opacity=0.82, stroke_width=0)
            bar.align_to(x_ax, DOWN).shift(UP * 0.01).set_x(bx)
            x_lbl = Text(name, font_size=SIZE_MICRO - 1, color=col,
                         font=FONT_PRIMARY, line_spacing=0.35)
            x_lbl.next_to([bx, bottom_y, 0], DOWN, buff=0.12)
            val_lbl = Text(f"{val}ms", font_size=SIZE_MICRO + 1,
                           color=col, font=FONT_PRIMARY, weight=BOLD)

            self.add(bar)
            self.play(
                bar.animate(run_time=0.7, rate_func=smooth)
                   .stretch_to_fit_height(target_h)
                   .align_to(x_ax, DOWN).shift(UP * 0.01).set_x(bx),
                FadeIn(x_lbl, run_time=0.25),
            )
            val_lbl.next_to(bar, UP, buff=0.08)
            self.play(FadeIn(val_lbl, scale=1.1, run_time=0.18))
            bars.append((bar, val_lbl, target_h, bx, col))

        # Total time
        total = sum(v for _, v, _ in STAGES)
        total_lbl = Text(f"Total: {total} ms", font_size=SIZE_LABEL - 1,
                         color=TEXT_WHITE, font=FONT_PRIMARY, weight=BOLD)
        total_lbl.move_to(RIGHT * 3.5 + UP * 2.2)
        self.play(FadeIn(total_lbl, shift=DOWN * 0.08, run_time=0.30))
        self.wait(0.5)

        # ── QuantV2X cuts encoding + transmission ─────────────
        bottleneck_lbl = Text("QuantV2X: encode+transmit shrink 10×",
                              font_size=SIZE_MICRO + 2, color=GREEN_SIGNAL,
                              font=FONT_PRIMARY, weight=BOLD)
        bottleneck_lbl.move_to(RIGHT * 3.5 + UP * 1.5)
        self.play(FadeIn(bottleneck_lbl, shift=DOWN * 0.06, run_time=0.28))

        # Shrink bars 1 and 2 (Encoding and Transmission)
        for idx in [1, 2]:
            bar, val_lbl, _, bx, col = bars[idx]
            new_val = AFTER_QUANT[idx]
            new_h = (new_val / max_val) * max_h
            new_val_lbl = Text(f"{new_val}ms", font_size=SIZE_MICRO + 1,
                               color=GREEN_SIGNAL, font=FONT_PRIMARY, weight=BOLD)
            new_val_lbl.next_to([bx, bottom_y + new_h, 0], UP, buff=0.08)
            self.play(
                bar.animate(run_time=0.80, rate_func=smooth)
                   .stretch_to_fit_height(new_h)
                   .align_to(x_ax, DOWN).shift(UP * 0.01).set_x(bx),
                ReplacementTransform(val_lbl, new_val_lbl, run_time=0.55),
            )

        new_total = sum(AFTER_QUANT)
        new_total_lbl = Text(f"Total: {new_total} ms  ✓ Real-time",
                             font_size=SIZE_LABEL - 1, color=GREEN_SIGNAL,
                             font=FONT_PRIMARY, weight=BOLD)
        new_total_lbl.next_to(total_lbl, DOWN, buff=0.18)
        self.play(
            FadeOut(total_lbl, run_time=0.30),
            FadeIn(new_total_lbl, shift=DOWN * 0.06, run_time=0.30),
        )
        self.wait(1.5)
        self.close()
