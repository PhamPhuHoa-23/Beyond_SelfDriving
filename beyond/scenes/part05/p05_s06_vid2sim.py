# beyond/scenes/part05/p05_s06_vid2sim.py
# ─────────────────────────────────────────────────────────────────
# P5-06  VID2SIM — REALITY BECOMES PLAYGROUND  (~45s)
#
# Input: city tour video → 3D Gaussian Splatting → photorealistic sim.
# Visual: scene "dissolves" thành hàng nghìn colored gaussians (galaxy).
# Mesh reconstruction: wireframe phủ lên geometry.
# Robot walks in the sim → transfer to real.
#
# Render:  manim -ql "beyond/scenes/part05/p05_s06_vid2sim.py" P05S06Vid2Sim
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block, pipeline_block_entrance,
    pipeline_arrow_entrance, glow_pulse,
    P5_PHYSICAL, CYAN_NEON, GREEN_SIGNAL, GOLD, P3_SIM,
    TEXT_WHITE, TEXT_DIM, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=88)


class P05S06Vid2Sim(BeyondScene):
    PART_COLOR = P5_PHYSICAL

    def construct(self):
        title_mob, sep = self.open("Vid2Sim — Real Video → Trainable Simulator")
        self.wait(0.2)

        # ── Pipeline overview (top) ───────────────────────────
        stages = [
            ("City Tour\nVideo",        TEXT_DIM),
            ("3D Gaussian\nSplatting",   P5_PHYSICAL),
            ("Mesh\nReconstruction",     CYAN_NEON),
            ("Vid2Sim\nEnvironment",     GREEN_SIGNAL),
        ]
        blocks = VGroup(*[
            pipeline_block(lbl, width=2.0, height=0.80,
                           border_color=col, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO + 1)
            for lbl, col in stages
        ]).arrange(RIGHT, buff=0.35).move_to(UP * 2.3)

        self.play(
            LaggedStart(*[pipeline_block_entrance(b, stages[i][1])
                          for i, b in enumerate(blocks)], lag_ratio=0.15),
        )
        arrows = [
            Arrow(blocks[i].get_right(), blocks[i+1].get_left(),
                  buff=0.05, color=stages[i+1][1],
                  stroke_width=1.8, tip_length=0.15)
            for i in range(len(blocks) - 1)
        ]
        self.play(
            LaggedStart(*[pipeline_arrow_entrance(a, style="electric")
                          for a in arrows], lag_ratio=0.12),
        )
        self.wait(0.3)

        # ── Real scene → Gaussian Splatting dissolution ───────
        # "Real" scene: rough rectangles
        real_scene = VGroup(*[
            Rectangle(
                width=float(RNG.uniform(0.4, 1.2)),
                height=float(RNG.uniform(0.3, 0.9)),
                fill_color=TEXT_DIM, fill_opacity=float(RNG.uniform(0.4, 0.7)),
                stroke_color=TEXT_DIM, stroke_width=0.7,
            ).move_to([
                float(RNG.uniform(-5.5, -2.5)),
                float(RNG.uniform(-1.5, 1.0)),
                0,
            ])
            for _ in range(8)
        ])
        real_lbl = Text("Real scene", font_size=SIZE_MICRO + 1,
                        color=TEXT_DIM, font=FONT_PRIMARY)
        real_lbl.move_to(LEFT * 4.0 + UP * 1.6)
        self.play(
            LaggedStart(*[GrowFromCenter(e, run_time=0.18) for e in real_scene],
                        lag_ratio=0.08),
            FadeIn(real_lbl, run_time=0.22),
        )
        self.wait(0.2)

        # Dissolve into colored gaussian splats (dots)
        n_splats = 50
        splats = VGroup(*[
            Dot(
                radius=float(RNG.uniform(0.025, 0.08)),
                color=RNG.choice([P5_PHYSICAL, CYAN_NEON, GREEN_SIGNAL, GOLD, "#FF9999"]),
                fill_opacity=float(RNG.uniform(0.5, 0.95)),
            ).move_to([
                float(RNG.uniform(-5.5, -2.2)),
                float(RNG.uniform(-1.5, 1.2)),
                0,
            ])
            for _ in range(n_splats)
        ])
        self.play(
            *[FadeOut(e, run_time=0.45, rate_func=rush_from) for e in real_scene],
            LaggedStart(*[GrowFromCenter(s, run_time=0.06) for s in splats],
                        lag_ratio=0.02),
        )
        splats_lbl = Text("3D Gaussians\n(photorealistic)", font_size=SIZE_MICRO,
                          color=P5_PHYSICAL, font=FONT_PRIMARY, line_spacing=0.38)
        splats_lbl.next_to(splats, DOWN, buff=0.12)
        self.play(FadeIn(splats_lbl, run_time=0.22))
        self.wait(0.3)

        # Wireframe mesh overlay
        mesh_lines = VGroup()
        for _ in range(12):
            p1 = np.array([float(RNG.uniform(-5.5, -2.2)),
                           float(RNG.uniform(-1.5, 1.2)), 0])
            p2 = np.array([float(RNG.uniform(-5.5, -2.2)),
                           float(RNG.uniform(-1.5, 1.2)), 0])
            mesh_lines.add(
                Line(p1, p2, stroke_color=CYAN_NEON,
                     stroke_width=0.5, stroke_opacity=0.50)
            )
        self.play(
            LaggedStart(*[Create(l, run_time=0.12) for l in mesh_lines],
                        lag_ratio=0.04),
        )
        self.wait(0.3)

        # ── Vid2Sim environment (right) ───────────────────────
        sim_bg = RoundedRectangle(corner_radius=0.12, width=4.2, height=3.5,
                                  fill_color="#050E1A", fill_opacity=1.0,
                                  stroke_color=GREEN_SIGNAL, stroke_width=1.8)
        sim_bg.move_to(RIGHT * 3.5 + DOWN * 0.0)

        sim_road = Rectangle(width=3.8, height=0.55,
                             fill_color="#061018", fill_opacity=1.0,
                             stroke_width=0)
        sim_road.move_to(RIGHT * 3.5 + DOWN * 0.5)

        sim_robot = Circle(radius=0.18, fill_color=GREEN_SIGNAL, fill_opacity=0.9,
                           stroke_color=WHITE, stroke_width=1.0)
        sim_robot.move_to(RIGHT * 1.8 + DOWN * 0.5)
        sim_robot_lbl = Text("Robot agent", font_size=SIZE_MICRO - 1,
                             color=GREEN_SIGNAL, font=FONT_PRIMARY)
        sim_robot_lbl.next_to(sim_robot, DOWN, buff=0.08)

        sim_title = Text("Vid2Sim", font_size=SIZE_LABEL - 1,
                         color=GREEN_SIGNAL, font=FONT_PRIMARY, weight=BOLD)
        sim_title.move_to(RIGHT * 3.5 + UP * 1.5)

        self.play(
            FadeIn(sim_bg, run_time=0.40),
            FadeIn(sim_road, run_time=0.28),
            FadeIn(sim_title, shift=DOWN * 0.06, run_time=0.25),
        )
        self.play(GrowFromCenter(sim_robot, run_time=0.30),
                  FadeIn(sim_robot_lbl, run_time=0.22))

        # Robot walks in sim
        self.play(
            sim_robot.animate(run_time=1.0, rate_func=smooth).shift(RIGHT * 2.5),
        )

        # Sim-to-real transfer arrow
        transfer_arr = Arrow(RIGHT * 5.2, RIGHT * 6.2,
                             buff=0.0, color=GOLD,
                             stroke_width=2.2, tip_length=0.18)
        transfer_lbl = Text("→ Real world\ntransfer", font_size=SIZE_MICRO,
                            color=GOLD, font=FONT_PRIMARY, line_spacing=0.38)
        # Position it inside safe zone
        transfer_lbl.to_edge(RIGHT, buff=0.35).set_y(sim_robot.get_center()[1])

        self.play(glow_pulse(sim_bg, GREEN_SIGNAL, n_pulses=1, run_time=0.38))
        self.wait(0.3)

        bottom_insight = Text(
            "Train in Vid2Sim → High visual fidelity → Small sim-to-real gap",
            font_size=SIZE_MICRO + 1, color=TEXT_DIM,
            font=FONT_PRIMARY, slant=ITALIC,
        )
        bottom_insight.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(bottom_insight, shift=UP * 0.08, run_time=0.35))
        self.wait(1.5)

        self.close()
