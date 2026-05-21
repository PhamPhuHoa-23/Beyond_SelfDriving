# beyond/scenes/part03/p03_s10_v2x_realo.py
# ─────────────────────────────────────────────────────────────────
# P3-10  V2X-REALO — REAL-WORLD ONLINE CALIBRATION  (~40s)
#
# Problem: calibration parameters drift over time / temperature.
# V2X-ReaLO: online re-calibration during operation.
# Visual: curve trôi dạt → V2X-ReaLO locks it back.
#
# Render:  manim -ql "beyond/scenes/part03/p03_s10_v2x_realo.py" P03S10V2XReaLO
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, axes_deploy, glow_pulse,
    P3_SIM, RED_ALERT, GREEN_SIGNAL, GOLD,
    TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)


class P03S10V2XReaLO(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("V2X-ReaLO — Online Recalibration")
        self.wait(0.2)

        axes = Axes(
            x_range=[0, 10, 2], y_range=[-0.6, 0.6, 0.2],
            x_length=9.0, y_length=4.5,
            axis_config={"color": TEXT_DIM, "stroke_width": 1.3,
                         "include_tip": True, "tip_length": 0.15},
        ).move_to(DOWN * 0.2)

        x_lbl = Text("Time →", font_size=SIZE_MICRO, color=TEXT_DIM, font=FONT_PRIMARY)
        x_lbl.next_to(axes.x_axis.get_end(), RIGHT, buff=0.08)
        y_lbl = Text("Calibration Error", font_size=SIZE_MICRO,
                     color=TEXT_DIM, font=FONT_PRIMARY).rotate(PI/2)
        y_lbl.next_to(axes.y_axis.get_end(), LEFT, buff=0.18)
        self.play(axes_deploy(axes, "", ""), FadeIn(x_lbl), FadeIn(y_lbl))

        # Zero reference line
        zero = DashedLine(axes.c2p(0, 0), axes.c2p(10, 0),
                          stroke_color=GREEN_SIGNAL, stroke_width=0.8,
                          stroke_opacity=0.5, dash_length=0.2)
        self.play(Create(zero, run_time=0.28))

        # Drifting calibration (without correction) - red curve that grows
        def drift_func(x):
            return 0.04 * x + 0.02 * np.sin(x * 0.8)

        drift_curve = axes.plot(drift_func, x_range=[0, 10],
                                color=RED_ALERT, stroke_width=2.2)
        drift_lbl = Text("Without correction: drift grows",
                         font_size=SIZE_MICRO + 1, color=RED_ALERT, font=FONT_PRIMARY)
        drift_lbl.to_corner(UR, buff=0.5)

        self.play(Create(drift_curve, run_time=1.5, rate_func=smooth))
        self.play(FadeIn(drift_lbl, shift=DOWN * 0.06, run_time=0.25))
        self.wait(0.4)
        self.play(FadeOut(drift_curve, run_time=0.35), FadeOut(drift_lbl, run_time=0.25))

        # V2X-ReaLO: corrections at keyframes → stays near zero
        def realo_func(x):
            # Small drift between corrections, snapped back
            phase = x % 2.5
            return 0.06 * phase * (1 - phase/2.5) * np.sin(x * 0.5)

        realo_curve = axes.plot(realo_func, x_range=[0, 10],
                                color=P3_SIM, stroke_width=2.5)

        # Snap points
        snap_xs = [2.5, 5.0, 7.5]
        snap_pts = [Dot(radius=0.08, color=GOLD, fill_opacity=1.0)
                    .move_to(axes.c2p(x, realo_func(x)))
                    for x in snap_xs]

        realo_lbl = Text("V2X-ReaLO: online corrections keep error bounded",
                         font_size=SIZE_MICRO + 1, color=P3_SIM, font=FONT_PRIMARY)
        realo_lbl.to_corner(UR, buff=0.5)

        self.play(Create(realo_curve, run_time=1.5, rate_func=smooth))
        self.play(
            LaggedStart(*[GrowFromCenter(p, run_time=0.18) for p in snap_pts],
                        lag_ratio=0.25),
        )
        self.play(
            LaggedStart(*[
                Flash(p.get_center(), color=GOLD, flash_radius=0.25,
                      num_lines=6, run_time=0.22)
                for p in snap_pts
            ], lag_ratio=0.20),
        )
        self.play(FadeIn(realo_lbl, shift=DOWN * 0.06, run_time=0.25))
        self.wait(1.2)
        self.close()
