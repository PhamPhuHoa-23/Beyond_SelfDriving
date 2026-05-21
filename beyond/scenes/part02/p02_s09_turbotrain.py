# beyond/scenes/part02/p02_s09_turbotrain.py
# ─────────────────────────────────────────────────────────────────
# P2-09  TURBOTRAIN (ICCV 2025)  (~60s)
#
# Chart: scatter "one-time training" vs 4-stage manual (higher).
# Gap performance clear.
# TurboTrain: 2 stages — pretraining masked + balancing.
# Counter: 120 epochs → 45 epochs.
#
# Render:  manim -ql "beyond/scenes/part02/p02_s09_turbotrain.py" P02S09TurboTrain
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, axes_deploy, pipeline_block, pipeline_block_entrance,
    pipeline_arrow_entrance,
    P2_COOP, ORANGE_INFRA, GOLD, GREEN_SIGNAL,
    BLUE_ELECTRIC, RED_ALERT,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=19)


class P02S09TurboTrain(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("TurboTrain — Automated Multi-Task Training")
        self.wait(0.2)

        # ── LEFT: Performance scatter chart ───────────────────
        axes = Axes(
            x_range=[0, 1.0, 0.25], y_range=[0, 1.0, 0.25],
            x_length=4.8, y_length=3.8,
            axis_config={"color": TEXT_DIM, "stroke_width": 1.3,
                         "include_tip": True, "tip_length": 0.15},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
        ).shift(LEFT * 2.8 + DOWN * 0.2)

        x_lbl = Text("Detection AP →", font_size=SIZE_MICRO, color=TEXT_DIM, font=FONT_PRIMARY)
        x_lbl.next_to(axes.x_axis.get_end(), RIGHT, buff=0.08)
        y_lbl = Text("Prediction EPA ↑", font_size=SIZE_MICRO, color=TEXT_DIM, font=FONT_PRIMARY)
        y_lbl.rotate(PI/2).next_to(axes.y_axis.get_end(), LEFT, buff=0.20)

        self.play(axes_deploy(axes, "", ""), FadeIn(x_lbl), FadeIn(y_lbl))

        # Orange dots: "one-time training" — clustered LOW
        orange_pts = VGroup(*[
            Dot(radius=0.065, color=ORANGE_INFRA, fill_opacity=0.85)
            .move_to(axes.c2p(
                float(RNG.uniform(0.10, 0.45)),
                float(RNG.uniform(0.08, 0.42))
            ))
            for _ in range(12)
        ])
        orange_lbl = Text("One-time training", font_size=SIZE_MICRO,
                          color=ORANGE_INFRA, font=FONT_PRIMARY)
        orange_lbl.move_to(axes.c2p(0.28, 0.55))

        self.play(
            LaggedStart(*[
                Dot(radius=0.0, color=ORANGE_INFRA).animate(run_time=0.0)
                for _ in range(1)
            ], lag_ratio=0),
        )
        self.play(
            LaggedStart(*[
                GrowFromCenter(d, run_time=0.12) for d in orange_pts
            ], lag_ratio=0.05),
        )
        self.play(FadeIn(orange_lbl, shift=DOWN * 0.06, run_time=0.28))

        # Blue dots: "4-stage manual" — HIGH
        blue_pts = VGroup(*[
            Dot(radius=0.075, color=BLUE_ELECTRIC, fill_opacity=0.90)
            .move_to(axes.c2p(
                float(RNG.uniform(0.60, 0.90)),
                float(RNG.uniform(0.62, 0.90))
            ))
            for _ in range(6)
        ])
        blue_lbl = Text("4-stage manual", font_size=SIZE_MICRO,
                        color=BLUE_ELECTRIC, font=FONT_PRIMARY)
        blue_lbl.move_to(axes.c2p(0.75, 0.48))

        self.play(
            LaggedStart(*[
                GrowFromCenter(d, run_time=0.15) for d in blue_pts
            ], lag_ratio=0.08),
        )
        self.play(FadeIn(blue_lbl, shift=DOWN * 0.06, run_time=0.28))

        # Gap arrow
        gap = DoubleArrow(axes.c2p(0.28, 0.28), axes.c2p(0.72, 0.72),
                          buff=0.08, color=RED_ALERT, stroke_width=1.4,
                          tip_length=0.14)
        gap_lbl = Text("Performance\ngap", font_size=SIZE_MICRO,
                       color=RED_ALERT, font=FONT_PRIMARY, line_spacing=0.38)
        gap_lbl.next_to(gap, RIGHT, buff=0.10)
        self.play(Create(gap, run_time=0.30), FadeIn(gap_lbl, run_time=0.22))
        self.wait(0.4)

        # ── RIGHT: TurboTrain 2 stages ────────────────────────
        stage1 = pipeline_block(
            "Stage 1\nPretraining\n(Masked Reconstruction)",
            width=3.0, height=1.10,
            border_color=P2_COOP, fill_color=BG_PANEL, font_size=SIZE_MICRO,
        ).move_to(RIGHT * 3.2 + UP * 1.5)

        stage2 = pipeline_block(
            "Stage 2\nBalancing\n(Free ↔ Conflict-suppressing)",
            width=3.0, height=1.10,
            border_color=GOLD, fill_color=BG_PANEL, font_size=SIZE_MICRO,
        ).move_to(RIGHT * 3.2 + DOWN * 0.1)

        st1_sub = Text('"Learn structure — no labels needed"',
                       font_size=SIZE_MICRO - 1, color=P2_COOP,
                       font=FONT_PRIMARY, slant=ITALIC)
        st1_sub.next_to(stage1, DOWN, buff=0.08)

        st2_sub = Text('"Auto-balance gradients across tasks"',
                       font_size=SIZE_MICRO - 1, color=GOLD,
                       font=FONT_PRIMARY, slant=ITALIC)
        st2_sub.next_to(stage2, DOWN, buff=0.08)

        self.play(pipeline_block_entrance(stage1, P2_COOP))
        self.play(FadeIn(st1_sub, shift=UP * 0.06, run_time=0.22))

        arr12 = Arrow(stage1.get_bottom(), stage2.get_top(),
                      buff=0.05, color=TEXT_DIM, stroke_width=1.5, tip_length=0.14)
        self.play(pipeline_arrow_entrance(arr12, style="electric"))
        self.play(pipeline_block_entrance(stage2, GOLD))
        self.play(FadeIn(st2_sub, shift=UP * 0.06, run_time=0.22))
        self.wait(0.4)

        # ── Counter: 120 epochs → 45 epochs ──────────────────
        epoch_val = ValueTracker(120)
        epoch_mob = Integer(120, color=RED_ALERT, font_size=SIZE_LABEL + 4)
        epoch_mob.add_updater(lambda m: m.set_value(int(epoch_val.get_value()))
                              .set_color(interpolate_color(RED_ALERT, GREEN_SIGNAL,
                                         max(0, (120 - epoch_val.get_value()) / 75))))
        epoch_mob.move_to(RIGHT * 3.2 + DOWN * 1.6)
        epoch_lbl = Text("training epochs", font_size=SIZE_MICRO + 1,
                         color=TEXT_DIM, font=FONT_PRIMARY)
        epoch_lbl.next_to(epoch_mob, DOWN, buff=0.12)

        self.add(epoch_mob)
        self.play(FadeIn(epoch_lbl, run_time=0.25))
        self.play(
            epoch_val.animate(run_time=1.5, rate_func=smooth).set_value(45),
        )
        epoch_mob.remove_updater(epoch_mob.get_updaters()[-1])
        self.play(
            Flash(epoch_mob.get_center(), color=GREEN_SIGNAL,
                  flash_radius=0.55, num_lines=8, run_time=0.35),
        )
        self.wait(1.5)

        self.close()
