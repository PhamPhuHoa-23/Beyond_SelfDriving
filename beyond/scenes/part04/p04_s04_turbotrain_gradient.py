# beyond/scenes/part04/p04_s04_turbotrain_gradient.py
# ─────────────────────────────────────────────────────────────────
# P4-04  TURBOTRAIN — GRADIENT CONFLICT  (~60s)
#
# Weight space visualization:
#   3 gradient arrows (Detection NE, Prediction SE, Planning W) conflict.
#   WITHOUT TurboTrain: chaotic zigzag path (red).
#   WITH TurboTrain: smooth spiral to optimum (green).
#   Counter: 120 epochs → 45 epochs.
#
# Render:  manim -ql "beyond/scenes/part04/p04_s04_turbotrain_gradient.py" P04S04TurboTrainGrad
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    P4_EFFICIENT, CYAN_NEON, BLUE_ELECTRIC, ORANGE_INFRA, P1_FOUNDATION,
    RED_ALERT, GREEN_SIGNAL, GOLD, GOLD_GLOW,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)


class P04S04TurboTrainGrad(BeyondScene):
    PART_COLOR = P4_EFFICIENT

    def construct(self):
        title_mob, sep = self.open("TurboTrain — Resolving Gradient Conflict")
        self.wait(0.2)

        # ── Weight space canvas ───────────────────────────────
        ws_title = Text("Weight Space", font_size=SIZE_MICRO + 2,
                        color=TEXT_DIM, font=FONT_PRIMARY)
        ws_title.move_to(UP * 2.4 + LEFT * 3.5)
        ws_bg = RoundedRectangle(corner_radius=0.12, width=7.0, height=5.5,
                                  fill_color="#040B14", fill_opacity=0.85,
                                  stroke_color=TEXT_GHOST, stroke_width=0.8)
        ws_bg.move_to(LEFT * 3.2 + DOWN * 0.2)
        self.play(FadeIn(ws_bg, run_time=0.35), FadeIn(ws_title, run_time=0.22))

        # Start point
        start = np.array([-5.5, 1.0, 0])
        optimum_pos = np.array([-1.5, -1.2, 0])

        # ★ optimum
        star = Text("★", font_size=SIZE_LABEL + 4, color=GOLD, font=FONT_PRIMARY)
        star.move_to(optimum_pos)
        opt_lbl = Text("Global Optimum", font_size=SIZE_MICRO,
                       color=GOLD, font=FONT_PRIMARY)
        opt_lbl.next_to(star, RIGHT, buff=0.12)
        self.play(FadeIn(star, scale=0.8, run_time=0.28),
                  FadeIn(opt_lbl, run_time=0.22))

        # Start dot
        start_dot = Dot(radius=0.10, color=TEXT_WHITE).move_to(start)
        self.play(GrowFromCenter(start_dot, run_time=0.20))

        # 3 gradient arrows from start
        grad_data = [
            (np.array([1.0, 0.8, 0]),  CYAN_NEON,    "Detection ↗"),
            (np.array([0.8, -0.9, 0]), ORANGE_INFRA,  "Prediction ↘"),
            (np.array([-1.0, 0.1, 0]), P1_FOUNDATION, "Planning ←"),
        ]
        grad_arrows = VGroup()
        for direction, color, label in grad_data:
            arr = Arrow(start, start + direction * 1.2,
                        buff=0.0, color=color, stroke_width=2.0, tip_length=0.16)
            lbl = Text(label, font_size=SIZE_MICRO - 1, color=color, font=FONT_PRIMARY)
            lbl.next_to(arr.get_end(), direction[:2].tolist(), buff=0.08)
            grad_arrows.add(VGroup(arr, lbl))

        self.play(
            LaggedStart(*[
                AnimationGroup(
                    Create(g[0], run_time=0.28),
                    FadeIn(g[1], run_time=0.22),
                )
                for g in grad_arrows
            ], lag_ratio=0.2),
        )

        # Conflict zone
        conflict_zone = Circle(radius=0.45, fill_color=RED_ALERT,
                               fill_opacity=0.18, stroke_color=RED_ALERT,
                               stroke_width=0.8, stroke_opacity=0.5)
        conflict_zone.move_to(start)
        conflict_lbl = Text("Conflict", font_size=SIZE_MICRO - 1,
                            color=RED_ALERT, font=FONT_PRIMARY)
        conflict_lbl.next_to(conflict_zone, DOWN, buff=0.06)
        self.play(FadeIn(conflict_zone, run_time=0.25),
                  FadeIn(conflict_lbl, run_time=0.20))
        self.wait(0.4)

        # ── WITHOUT TurboTrain: chaotic path ──────────────────
        # Zigzag path never converging
        bad_pts = [start]
        p = start.copy()
        rng_local = np.random.default_rng(42)
        for _ in range(8):
            # Random direction influenced by conflicting gradients
            angle = float(rng_local.uniform(0, TAU))
            step = 0.6
            p = p + step * np.array([np.cos(angle), np.sin(angle), 0])
            # Keep inside ws_bg area
            p = np.clip(p, [-6.5, -2.5, 0], [-0.5, 2.2, 0])
            bad_pts.append(p.copy())

        bad_path = VMobject(stroke_color=RED_ALERT, stroke_width=1.8,
                            stroke_opacity=0.70, fill_opacity=0)
        bad_path.set_points_as_corners([p for p in bad_pts])

        bad_lbl = Text("Without TurboTrain: zigzag, no convergence",
                       font_size=SIZE_MICRO, color=RED_ALERT, font=FONT_PRIMARY)
        bad_lbl.to_edge(DOWN, buff=0.80)
        self.play(FadeIn(bad_lbl, shift=UP * 0.06, run_time=0.22))
        self.play(Create(bad_path, run_time=1.5, rate_func=smooth))
        self.wait(0.4)
        self.play(FadeOut(bad_path, run_time=0.30),
                  FadeOut(bad_lbl, run_time=0.25))

        # ── WITH TurboTrain: smooth convergence ───────────────
        good_pts = [start]
        p = start.copy()
        for i in range(10):
            t = (i + 1) / 10
            p = p + (optimum_pos - p) * 0.35 + np.array([
                float(rng_local.uniform(-0.08, 0.08)), 0, 0
            ])
            good_pts.append(p.copy())
        good_pts.append(optimum_pos)

        good_path = VMobject(stroke_color=GREEN_SIGNAL, stroke_width=2.2,
                             stroke_opacity=0.90, fill_opacity=0)
        good_path.set_points_smoothly([p for p in good_pts])

        good_lbl = Text("With TurboTrain: smooth convergence to optimum",
                        font_size=SIZE_MICRO, color=GREEN_SIGNAL, font=FONT_PRIMARY)
        good_lbl.to_edge(DOWN, buff=0.80)
        self.play(FadeIn(good_lbl, shift=UP * 0.06, run_time=0.22))
        self.play(Create(good_path, run_time=1.5, rate_func=smooth))
        self.play(
            Flash(optimum_pos, color=GOLD,
                  flash_radius=0.50, num_lines=10, run_time=0.40),
        )
        self.wait(0.4)

        # ── RIGHT side: counter ───────────────────────────────
        before_txt = Text("Before: 120 epochs", font_size=SIZE_LABEL - 2,
                          color=RED_ALERT, font=FONT_PRIMARY)
        after_txt  = Text("After:   45 epochs",  font_size=SIZE_LABEL - 2,
                          color=GREEN_SIGNAL, font=FONT_PRIMARY)
        VGroup(before_txt, after_txt).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.5)
        self.play(FadeIn(before_txt, shift=LEFT * 0.08, run_time=0.28))
        self.play(FadeIn(after_txt,  shift=LEFT * 0.08, run_time=0.28))
        self.play(
            Flash(after_txt.get_center(), color=GREEN_SIGNAL,
                  flash_radius=0.70, num_lines=8, run_time=0.35),
        )
        self.wait(1.5)

        self.close()
