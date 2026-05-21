# beyond/scenes/part03/p03_s05_kalman.py
# ─────────────────────────────────────────────────────────────────
# P3-05  BA DÒNG SÔNG — KALMAN FILTER  (~60s)
#
# 3 sensor streams như 3 dòng sông chảy về KALMAN FILTER node:
#   Stream 1 — GNSS: rộng, chậm, bị block khi có building
#   Stream 2 — IMU+Wheel: medium, nhanh, drift theo thời gian
#   Stream 3 — LiDAR map-matching: hẹp, chậm, chính xác
#
# Họ hội tụ về node → Output: clean 100Hz green stream.
#
# Render:  manim -ql "beyond/scenes/part03/p03_s05_kalman.py" P03S05Kalman
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, glow_pulse,
    BG_SPACE, BG_PANEL,
    P3_SIM, P4_EFFICIENT, CYAN_NEON, BLUE_ELECTRIC,
    GREEN_SIGNAL, ORANGE_INFRA, RED_ALERT,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=44)

# Colors for each stream
C_GNSS  = BLUE_ELECTRIC
C_IMU   = ORANGE_INFRA
C_LIDAR = CYAN_NEON

STREAM_DATA = [
    {
        "name": "GNSS",     "rate": "5 Hz",   "color": C_GNSS,
        "pro":  "Absolute position",
        "con":  "Blocked by buildings",
        "width": 0.55, "start_x": -5.5, "y": 1.5,
    },
    {
        "name": "IMU + Wheel", "rate": "100 Hz", "color": C_IMU,
        "pro":  "Fast & continuous",
        "con":  "Drifts over time",
        "width": 0.38, "start_x": -5.5, "y": 0.0,
    },
    {
        "name": "LiDAR Map", "rate": "1 Hz",  "color": C_LIDAR,
        "pro":  "Lane-level precise",
        "con":  "Compute heavy",
        "width": 0.22, "start_x": -5.5, "y": -1.5,
    },
]

FUSION_POS = np.array([1.2, 0.0, 0.0])
OUTPUT_END = np.array([5.5, 0.0, 0.0])


def _stream_ribbon(y: float, color: str, width: float,
                   x0: float, x1: float, opacity: float = 0.45) -> Rectangle:
    rx = (x1 - x0) / 2
    r = Rectangle(width=x1 - x0, height=width,
                  fill_color=color, fill_opacity=opacity, stroke_width=0)
    r.move_to([(x0 + x1) / 2, y, 0])
    return r


def _stream_label(sd: dict, x: float) -> VGroup:
    name_t = Text(sd["name"], font_size=SIZE_MICRO + 2,
                  color=sd["color"], font=FONT_PRIMARY, weight=BOLD)
    rate_t = Text(sd["rate"], font_size=SIZE_MICRO,
                  color=TEXT_DIM, font=FONT_PRIMARY)
    pro_t  = Text(f"✓ {sd['pro']}", font_size=SIZE_MICRO - 1,
                  color=GREEN_SIGNAL, font=FONT_PRIMARY)
    con_t  = Text(f"⚠ {sd['con']}", font_size=SIZE_MICRO - 1,
                  color=RED_ALERT, font=FONT_PRIMARY)
    grp = VGroup(name_t, rate_t, pro_t, con_t).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    grp.move_to([x, sd["y"], 0])
    return grp


class P03S05Kalman(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("Sensor Fusion — Three Rivers Metaphor")
        self.wait(0.2)

        # ── Labels on the left ────────────────────────────────
        labels = VGroup(*[_stream_label(sd, -4.2) for sd in STREAM_DATA])
        self.play(
            LaggedStart(*[FadeIn(lbl, shift=RIGHT * 0.10, run_time=0.35)
                          for lbl in labels], lag_ratio=0.20),
        )
        self.wait(0.3)

        # ── Streams flow toward fusion node ───────────────────
        x0 = -2.6
        x1 = FUSION_POS[0] - 0.1
        ribbons = VGroup()
        for sd in STREAM_DATA:
            r = _stream_ribbon(sd["y"], sd["color"], sd["width"], x0, x1,
                               opacity=0.40)
            ribbons.add(r)

        self.play(
            LaggedStart(*[
                Create(r, run_time=0.70, rate_func=smooth)
                for r in ribbons
            ], lag_ratio=0.15),
        )

        # ── Stream anomalies (visualize pros/cons) ─────────────

        # GNSS: blocked momentarily (flash red, gap)
        gnss_block = Rectangle(width=0.30, height=0.55 + 0.2,
                               fill_color=RED_ALERT, fill_opacity=0.55,
                               stroke_width=0)
        gnss_block.move_to([-1.2, STREAM_DATA[0]["y"], 0])
        self.play(FadeIn(gnss_block, run_time=0.20))
        self.play(FadeOut(gnss_block, run_time=0.40))

        # IMU: drift — ribbon tilts slightly
        self.play(
            ribbons[1].animate(run_time=0.55, rate_func=smooth)
                      .shift(UP * 0.18),
        )
        self.play(
            ribbons[1].animate(run_time=0.30, rate_func=smooth)
                      .shift(DOWN * 0.18),
        )

        self.wait(0.2)

        # ── KALMAN FILTER node ─────────────────────────────────
        fusion_circle = Circle(
            radius=0.55,
            fill_color="#0A1828", fill_opacity=1.0,
            stroke_color=GREEN_SIGNAL, stroke_width=2.5,
        ).move_to(FUSION_POS)
        fusion_lbl = Text("KALMAN\nFILTER", font_size=SIZE_MICRO + 1,
                          color=GREEN_SIGNAL, font=FONT_PRIMARY, weight=BOLD,
                          line_spacing=0.38)
        fusion_lbl.move_to(FUSION_POS)

        self.play(
            GrowFromCenter(fusion_circle, run_time=0.50),
            FadeIn(fusion_lbl, run_time=0.30),
        )
        self.play(glow_pulse(fusion_circle, GREEN_SIGNAL, n_pulses=2, run_time=0.40))

        # Convergence arrows (streams taper to fusion)
        for sd in STREAM_DATA:
            arr = Arrow(
                np.array([x1, sd["y"], 0]),
                FUSION_POS + np.array([-0.56, 0, 0]),
                buff=0.05, color=sd["color"],
                stroke_width=max(1.0, sd["width"] * 4.0),
                tip_length=0.14,
            )
            self.play(Create(arr, run_time=0.28, rate_func=rush_into))

        self.wait(0.3)

        # ── OUTPUT: single clean green stream ─────────────────
        output_ribbon = _stream_ribbon(0.0, GREEN_SIGNAL, 0.45,
                                       FUSION_POS[0] + 0.56,
                                       OUTPUT_END[0],
                                       opacity=0.60)
        output_arr = Arrow(
            FUSION_POS + RIGHT * 0.56,
            OUTPUT_END,
            buff=0.0, color=GREEN_SIGNAL,
            stroke_width=2.5, tip_length=0.18,
        )

        self.play(
            Create(output_ribbon, run_time=0.65, rate_func=smooth),
            Create(output_arr, run_time=0.50),
        )

        # Output label
        out_lbl = Text("100 Hz  ·  Lane-level accuracy  ·  Real-time",
                       font_size=SIZE_MICRO + 2, color=GREEN_SIGNAL,
                       font=FONT_PRIMARY, weight=BOLD)
        out_lbl.next_to(output_arr, UP, buff=0.15)
        self.play(Write(out_lbl, run_time=0.70))
        self.play(glow_pulse(output_ribbon, GREEN_SIGNAL, n_pulses=2, run_time=0.40))
        self.wait(1.8)

        self.close()
