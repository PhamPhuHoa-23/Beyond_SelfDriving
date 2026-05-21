# beyond/scenes/part03/p03_s04_calibration.py
# ─────────────────────────────────────────────────────────────────
# P3-04  CALIBRATION — TIME AND SPACE  (~55s)
#
# TIME: xe chạy 60km/h, delay 50ms → lệch 83cm.
#   Animation: 2 chấm cách nhau (vị trí "seen" vs thực tế).
#   Fix: GPS time sync → kim đồng hồ khớp.
#
# SPACE: 2 point clouds cùng người, 2 hệ tọa độ.
#   Transform matrix bay vào → clouds hợp thành 1.
#   Ngược lại: calibration sai → ghost object.
#
# Render:  manim -ql "beyond/scenes/part03/p03_s04_calibration.py" P03S04Calibration
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    P3_SIM, CYAN_NEON, ORANGE_INFRA, RED_ALERT, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=55)


class P03S04Calibration(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("Calibration — Time and Space Alignment")
        self.wait(0.2)

        # ════════════════════════════════════════════════════════
        # PART 1: TIME CALIBRATION
        # ════════════════════════════════════════════════════════
        time_lbl = Text("1. Temporal Calibration", font_size=SIZE_LABEL - 1,
                        color=P3_SIM, font=FONT_PRIMARY, weight=BOLD)
        time_lbl.move_to(UP * 2.3 + LEFT * 2.5)
        self.play(FadeIn(time_lbl, shift=DOWN * 0.06, run_time=0.28))

        # Timeline
        timeline = Line(LEFT * 5.5 + UP * 1.5, RIGHT * 1.5 + UP * 1.5,
                        stroke_color=TEXT_DIM, stroke_width=1.2)
        self.play(Create(timeline, run_time=0.35))

        # Car moves right at 60km/h
        car_body = RoundedRectangle(corner_radius=0.05, width=0.70, height=0.38,
                                    fill_color=CYAN_NEON, fill_opacity=0.85,
                                    stroke_color=WHITE, stroke_width=1.2)
        car_body.move_to(LEFT * 4.8 + UP * 1.5)
        car_trail = TracedPath(car_body.get_center, stroke_color=CYAN_NEON,
                               stroke_width=0.8, stroke_opacity=0.3,
                               dissipating_time=1.0)
        self.add(car_body, car_trail)
        self.play(
            car_body.animate(run_time=1.2, rate_func=smooth).shift(RIGHT * 4.2),
        )
        car_real_pos = car_body.get_center().copy()

        # Infra "sees" car at 50ms-old position
        infra_seen = Dot(radius=0.12, color=ORANGE_INFRA, fill_opacity=0.90)
        infra_seen.move_to(car_real_pos + LEFT * 0.83)  # 83cm behind

        self.play(GrowFromCenter(infra_seen, run_time=0.28))

        # Labels for the gap
        gap_arr = DoubleArrow(infra_seen.get_right(), car_body.get_left(),
                              buff=0.05, color=RED_ALERT, stroke_width=1.4,
                              tip_length=0.13)
        gap_txt = Text("83 cm offset\n(50ms delay)", font_size=SIZE_MICRO,
                       color=RED_ALERT, font=FONT_PRIMARY, line_spacing=0.38)
        gap_txt.next_to(gap_arr, DOWN, buff=0.10)

        self.play(Create(gap_arr, run_time=0.28), FadeIn(gap_txt, run_time=0.22))
        self.wait(0.4)

        # FIX: clocks sync → gap closes
        sync_txt = Text("GPS time sync + hardware trigger",
                        font_size=SIZE_MICRO + 1, color=GREEN_SIGNAL,
                        font=FONT_PRIMARY)
        sync_txt.next_to(timeline, DOWN, buff=0.22)
        self.play(FadeIn(sync_txt, shift=UP * 0.06, run_time=0.28))
        self.play(
            infra_seen.animate(run_time=0.55, rate_func=smooth)
                      .move_to(car_real_pos),
            FadeOut(VGroup(gap_arr, gap_txt), run_time=0.35),
        )
        self.play(
            Flash(car_real_pos, color=GREEN_SIGNAL,
                  flash_radius=0.35, num_lines=6, run_time=0.28),
        )
        self.wait(0.3)

        # Fade time section
        self.play(
            VGroup(time_lbl, timeline, car_body, car_trail, infra_seen, sync_txt)
            .animate(run_time=0.45).set_opacity(0.15),
        )

        # ════════════════════════════════════════════════════════
        # PART 2: SPACE CALIBRATION
        # ════════════════════════════════════════════════════════
        space_lbl = Text("2. Spatial Calibration", font_size=SIZE_LABEL - 1,
                         color=P3_SIM, font=FONT_PRIMARY, weight=BOLD)
        space_lbl.move_to(DOWN * 0.5 + LEFT * 2.5)
        self.play(FadeIn(space_lbl, shift=DOWN * 0.06, run_time=0.28))

        # Two point clouds of "same person" in different coord systems
        person_pos_A = LEFT * 3.5 + DOWN * 1.8
        person_pos_B = RIGHT * 0.5 + DOWN * 1.4  # offset = misaligned

        cloud_A = VGroup(*[
            Dot(radius=float(RNG.uniform(0.03, 0.06)), color=CYAN_NEON,
                fill_opacity=float(RNG.uniform(0.5, 0.9)))
            .move_to(person_pos_A + np.array([
                float(RNG.uniform(-0.3, 0.3)),
                float(RNG.uniform(-0.4, 0.4)), 0
            ]))
            for _ in range(14)
        ])
        cloud_B = VGroup(*[
            Dot(radius=float(RNG.uniform(0.03, 0.06)), color=ORANGE_INFRA,
                fill_opacity=float(RNG.uniform(0.5, 0.9)))
            .move_to(person_pos_B + np.array([
                float(RNG.uniform(-0.3, 0.3)),
                float(RNG.uniform(-0.4, 0.4)), 0
            ]))
            for _ in range(14)
        ])

        lbl_A = Text("Vehicle\nLiDAR", font_size=SIZE_MICRO - 1,
                     color=CYAN_NEON, font=FONT_PRIMARY, line_spacing=0.35)
        lbl_A.next_to(cloud_A, UP, buff=0.10)
        lbl_B = Text("Infra\nLiDAR", font_size=SIZE_MICRO - 1,
                     color=ORANGE_INFRA, font=FONT_PRIMARY, line_spacing=0.35)
        lbl_B.next_to(cloud_B, UP, buff=0.10)

        self.play(
            LaggedStart(*[GrowFromCenter(d, run_time=0.04) for d in cloud_A],
                        lag_ratio=0.03),
            LaggedStart(*[GrowFromCenter(d, run_time=0.04) for d in cloud_B],
                        lag_ratio=0.03),
            FadeIn(lbl_A, run_time=0.22),
            FadeIn(lbl_B, run_time=0.22),
        )
        self.wait(0.3)

        # Transform matrix appears
        mat = Text("T = [R | t]", font_size=SIZE_LABEL,
                   color=P3_SIM, font=FONT_PRIMARY)
        mat.move_to(RIGHT * 3.5 + DOWN * 1.8)
        self.play(FadeIn(mat, scale=0.85, run_time=0.30))

        # Apply transform: cloud_B shifts to merge with cloud_A
        target_pos = person_pos_A
        self.play(
            cloud_B.animate(run_time=0.80, rate_func=smooth)
                   .shift(target_pos - person_pos_B),
            lbl_B.animate(run_time=0.80).shift(target_pos - person_pos_B),
            Flash(target_pos, color=GREEN_SIGNAL,
                  flash_radius=0.50, num_lines=8, run_time=0.35),
        )
        merged_lbl = Text("✓ Fused — same object", font_size=SIZE_MICRO + 1,
                          color=GREEN_SIGNAL, font=FONT_PRIMARY)
        merged_lbl.next_to(cloud_A, DOWN, buff=0.15)
        self.play(FadeIn(merged_lbl, shift=UP * 0.06, run_time=0.25))
        self.wait(1.2)

        self.close()
