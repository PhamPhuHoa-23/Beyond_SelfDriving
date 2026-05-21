# beyond/scenes/part04/p04_s05_quantv2x.py
# ─────────────────────────────────────────────────────────────────
# P4-05  QUANTV2X — BIT COMPRESSION  (~70s)  [Technical Beauty Part 4]
#
# Phase 1: BEV feature blob lớn, FP32_HEAVY đỏ, channel bị nghẹt.
# Phase 2: 3-stage QuantV2X pipeline (B1 animation).
# Phase 3: COMPRESSION REVEAL — blob squeeze 100MB → 0.33MB,
#           ValueTracker animate số, channel mở rộng xanh lá.
# FP32 dots → INT8 dots (32 dots → 8 dots compression).
#
# Render:  manim -ql "beyond/scenes/part04/p04_s05_quantv2x.py" P04S05QuantV2X
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    pipeline_block, pipeline_block_entrance, pipeline_arrow_entrance,
    glow_pulse,
    BG_PANEL, BG_SPACE,
    GOLD, CYAN_NEON, P4_EFFICIENT,
    FP32_HEAVY, INT8_LIGHT, GREEN_SIGNAL, RED_ALERT,
    BLUE_ELECTRIC,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=42)


def _fp32_dots(n: int = 32) -> VGroup:
    """4×8 grid of FP32 dots."""
    dots = VGroup()
    for i in range(4):
        for j in range(8):
            d = Dot(radius=0.055, color=FP32_HEAVY, fill_opacity=0.88)
            d.move_to([-1.55 + j * 0.20, 0.30 - i * 0.20, 0])
            dots.add(d)
    return dots


def _int8_dots(n: int = 8) -> VGroup:
    """1×8 row of INT8 dots (brighter, bigger)."""
    dots = VGroup()
    for j in range(8):
        d = Dot(radius=0.090, color=INT8_LIGHT, fill_opacity=1.0)
        d.move_to([-0.70 + j * 0.20, 0.0, 0])
        dots.add(d)
    return dots


class P04S05QuantV2X(BeyondScene):
    PART_COLOR = P4_EFFICIENT

    def construct(self):
        title_mob, sep = self.open("QuantV2X — 300× Communication Compression")
        self.wait(0.2)

        # ── Phase 1: Problem — BEV too heavy ─────────────────
        bev_blob = RoundedRectangle(
            corner_radius=0.18, width=3.5, height=1.8,
            fill_color=FP32_HEAVY, fill_opacity=0.30,
            stroke_color=FP32_HEAVY, stroke_width=2.5,
        ).move_to(LEFT * 3.5 + UP * 0.8)

        bev_lbl1 = Text("BEV Feature Map", font_size=SIZE_MICRO + 2,
                        color=FP32_HEAVY, font=FONT_PRIMARY, weight=BOLD)
        bev_lbl2 = Text("FP32  ·  32 bits/value  ·  ~100 MB/frame",
                        font_size=SIZE_MICRO, color=FP32_HEAVY, font=FONT_PRIMARY)
        bev_lbl1.next_to(bev_blob, UP, buff=0.12)
        bev_lbl2.next_to(bev_blob, DOWN, buff=0.10)

        self.play(
            GrowFromCenter(bev_blob, run_time=0.50),
            FadeIn(bev_lbl1, shift=DOWN * 0.06, run_time=0.30),
            FadeIn(bev_lbl2, shift=UP * 0.06, run_time=0.30),
        )

        # FP32 dots inside blob
        fp32_dots = _fp32_dots()
        fp32_dots.move_to(bev_blob.get_center())
        self.play(
            LaggedStart(*[GrowFromCenter(d, run_time=0.05) for d in fp32_dots],
                        lag_ratio=0.03),
        )
        self.wait(0.2)

        # V2X channel — bottleneck visualization
        channel = Rectangle(width=0.25, height=1.2,
                            fill_color=RED_ALERT, fill_opacity=0.40,
                            stroke_color=RED_ALERT, stroke_width=1.8)
        channel.move_to(LEFT * 0.8 + UP * 0.8)
        channel_lbl = Text("V2X\nChannel", font_size=SIZE_MICRO - 1,
                           color=RED_ALERT, font=FONT_PRIMARY, line_spacing=0.38)
        channel_lbl.next_to(channel, UP, buff=0.10)
        channel_heavy = Text("TOO HEAVY", font_size=SIZE_MICRO,
                             color=RED_ALERT, font=FONT_PRIMARY, weight=BOLD)
        channel_heavy.next_to(channel, DOWN, buff=0.10)

        arr_to_ch = Arrow(bev_blob.get_right(), channel.get_left(),
                          buff=0.08, color=RED_ALERT,
                          stroke_width=2.0, tip_length=0.16)
        self.play(
            Create(arr_to_ch, run_time=0.30),
            GrowFromCenter(channel, run_time=0.40),
            FadeIn(channel_lbl, run_time=0.25),
            FadeIn(channel_heavy, run_time=0.25),
        )
        # Shake channel (bottleneck)
        for _ in range(2):
            self.play(channel.animate(run_time=0.07).shift(RIGHT * 0.07))
            self.play(channel.animate(run_time=0.07).shift(LEFT * 0.14))
            self.play(channel.animate(run_time=0.07).shift(RIGHT * 0.07))
        self.wait(0.3)

        # ── Phase 2: 3-stage QuantV2X pipeline ───────────────
        # Slide everything left to make room
        phase1 = VGroup(bev_blob, bev_lbl1, bev_lbl2, fp32_dots,
                        arr_to_ch, channel, channel_lbl, channel_heavy)
        self.play(phase1.animate(run_time=0.55, rate_func=smooth).shift(LEFT * 1.5))

        # 3 stage boxes (right side)
        stages = [
            ("Full-Precision\nPretraining",   BLUE_ELECTRIC, "FP32 weights\nAll layers"),
            ("Codebook\nLearning",             GOLD,          "Discrete token\nvocabulary"),
            ("Post-Training\nQuantization",    GREEN_SIGNAL,  "FP32 → INT8\nSmart calib."),
        ]
        stage_mobs = []
        prev_box = None
        stage_y = 1.5
        for i, (name, col, sub) in enumerate(stages):
            blk = pipeline_block(name, width=2.4, height=0.80,
                                 border_color=col, fill_color=BG_PANEL,
                                 font_size=SIZE_MICRO + 1)
            blk.move_to(RIGHT * (1.8 + i * 3.0) + UP * stage_y)
            sub_lbl = Text(sub, font_size=SIZE_MICRO - 1, color=TEXT_DIM,
                           font=FONT_PRIMARY, line_spacing=0.35)
            sub_lbl.next_to(blk, DOWN, buff=0.10)
            stage_mobs.append(VGroup(blk, sub_lbl))

        for i, sg in enumerate(stage_mobs):
            self.play(pipeline_block_entrance(sg[0], stages[i][1]))
            self.play(FadeIn(sg[1], shift=UP * 0.06, run_time=0.25))
            if i < len(stage_mobs) - 1:
                arr = Arrow(sg[0].get_right(), stage_mobs[i+1][0].get_left(),
                            buff=0.08, color=stages[i][1],
                            stroke_width=1.6, tip_length=0.15)
                self.play(pipeline_arrow_entrance(arr, style="electric"))

        self.wait(0.3)

        # ── Phase 3: COMPRESSION REVEAL ───────────────────────
        # Fade pipeline stages, show compression animation center-stage
        self.play(
            *[FadeOut(sg, run_time=0.40) for sg in stage_mobs],
            phase1.animate(run_time=0.40).set_opacity(0.25),
        )

        # Large blob → squeeze → tiny bright dot
        big_blob = Ellipse(width=3.0, height=1.5,
                           fill_color=FP32_HEAVY, fill_opacity=0.40,
                           stroke_color=FP32_HEAVY, stroke_width=2.2)
        big_blob.move_to(LEFT * 2.0 + DOWN * 0.5)
        big_size_lbl = Text("100 MB  ·  FP32",
                            font_size=SIZE_LABEL - 1, color=FP32_HEAVY,
                            font=FONT_PRIMARY)
        big_size_lbl.next_to(big_blob, UP, buff=0.12)

        small_dot = Dot(radius=0.22, color=INT8_LIGHT, fill_opacity=1.0)
        small_dot.move_to(RIGHT * 2.5 + DOWN * 0.5)
        small_size_lbl = Text("0.33 MB  ·  INT8",
                              font_size=SIZE_LABEL - 1, color=INT8_LIGHT,
                              font=FONT_PRIMARY)
        small_size_lbl.next_to(small_dot, UP, buff=0.12)

        ratio_lbl = Text("300×\nsmaller", font_size=SIZE_LABEL + 4,
                         color=GOLD, font=FONT_PRIMARY, weight=BOLD,
                         line_spacing=0.40)
        ratio_lbl.move_to(UP * 0.5)

        self.play(
            GrowFromCenter(big_blob, run_time=0.40),
            FadeIn(big_size_lbl, run_time=0.30),
        )
        self.wait(0.2)

        # Squeeze animation
        self.play(
            big_blob.animate(run_time=1.2, rate_func=smooth)
                    .scale(0.12).set_fill(INT8_LIGHT, opacity=0.9)
                    .set_stroke(INT8_LIGHT, width=1.5)
                    .move_to(small_dot.get_center()),
            FadeOut(big_size_lbl, run_time=0.40),
        )
        self.play(
            Flash(small_dot.get_center(), color=INT8_LIGHT,
                  flash_radius=0.60, num_lines=10, run_time=0.45),
            FadeIn(small_size_lbl, shift=UP * 0.08, run_time=0.30),
        )
        self.play(
            Write(ratio_lbl, run_time=0.60),
        )
        self.play(glow_pulse(ratio_lbl, GOLD, n_pulses=2, run_time=0.40))

        # Channel transforms green (feasible now)
        new_channel = Rectangle(width=1.80, height=1.2,
                                fill_color=GREEN_SIGNAL, fill_opacity=0.35,
                                stroke_color=GREEN_SIGNAL, stroke_width=1.8)
        new_channel.move_to(channel.copy().shift(LEFT * 1.5).get_center())
        new_ch_lbl = Text("V2X Channel\nReal-time ✓",
                          font_size=SIZE_MICRO, color=GREEN_SIGNAL,
                          font=FONT_PRIMARY, line_spacing=0.38)
        new_ch_lbl.move_to(new_channel)

        self.play(
            phase1.animate(run_time=0.30).set_opacity(1.0),
            ReplacementTransform(channel.copy().shift(LEFT * 1.5), new_channel,
                                 run_time=0.55),
            FadeOut(channel_heavy, run_time=0.30),
        )
        self.play(FadeIn(new_ch_lbl, run_time=0.25))
        self.wait(1.5)

        self.close()
