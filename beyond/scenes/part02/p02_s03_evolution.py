# beyond/scenes/part02/p02_s03_evolution.py
# ─────────────────────────────────────────────────────────────────
# P2-03  SINGLE-AGENT E2E JOURNEY  (~50s)
#
# J1 evolution timeline: PnPNet → GameFormer → UniAD → DiffusionDrive.
# Mỗi milestone: bead + label TRÊN spine + "why next exists" text dưới.
# Kết: xe đơn độc nhìn thẳng, blindspot, "Chưa." lớn đỏ, hold 2s.
#
# Render:  manim -ql "beyond/scenes/part02/p02_s03_evolution.py" P02S03Evolution
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, evolution_timeline,
    P2_COOP, GOLD, CYAN_NEON, BLUE_ELECTRIC, P1_FOUNDATION,
    RED_ALERT,
    TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

MILESTONES = [
    {
        "year": 2021, "name": "PnPNet",
        "contribution": "CNN + LSTM\njoint perc+pred",
        "bottleneck": "interaction quality",
        "color": P2_COOP,
    },
    {
        "year": 2022, "name": "GameFormer",
        "contribution": "Interactive\nprediction",
        "bottleneck": "end-to-end joint",
        "color": BLUE_ELECTRIC,
    },
    {
        "year": 2023, "name": "UniAD",
        "contribution": "Query-based\nend-to-end",
        "bottleneck": "trajectory quality",
        "color": P1_FOUNDATION,
    },
    {
        "year": 2024, "name": "DiffusionDrive",
        "contribution": "Diffusion-based\ntrajectory",
        "bottleneck": "occlusion still unsolved",
        "color": GOLD,
    },
]


class P02S03Evolution(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("Single-Agent AV: How Far Have We Come?")
        self.wait(0.2)

        # Timeline (shifted up to leave room below)
        full_grp, timeline_anim = evolution_timeline(MILESTONES, spine_y=0.4)
        full_grp.shift(UP * 0.3)

        self.play(timeline_anim, run_time=5.5)
        self.wait(0.5)

        # Bridge question
        q = Text("Has end-to-end solved everything?",
                 font_size=SIZE_LABEL - 1, color=TEXT_WHITE,
                 font=FONT_PRIMARY)
        q.to_edge(DOWN, buff=1.0)
        self.play(Write(q, run_time=0.70))
        self.wait(1.2)
        self.play(FadeOut(q, run_time=0.30))

        # ── Solo car facing forward — blindspot ───────────────
        # Fade timeline to 25%
        self.play(full_grp.animate(run_time=0.50).set_opacity(0.20))

        # Car (simple top-down view)
        car_body = RoundedRectangle(corner_radius=0.08, width=1.0, height=0.55,
                                    fill_color=CYAN_NEON, fill_opacity=0.85,
                                    stroke_color=WHITE, stroke_width=1.5)
        car_roof = RoundedRectangle(corner_radius=0.05, width=0.50, height=0.32,
                                    fill_color=CYAN_NEON, fill_opacity=1.0,
                                    stroke_color=WHITE, stroke_width=1.0)
        car_roof.align_to(car_body, LEFT).shift(RIGHT * 0.12).align_to(car_body, UP).shift(DOWN * 0.04)
        car = VGroup(car_body, car_roof).move_to(LEFT * 2.5 + DOWN * 0.2)

        # Truck behind (blocking view)
        truck = Rectangle(width=1.4, height=0.90,
                          fill_color="#1C2E50", fill_opacity=0.95,
                          stroke_color="#5B8DC8", stroke_width=1.8)
        truck.move_to(LEFT * 0.2 + DOWN * 0.2)

        # LiDAR scan (blocked)
        lidar_rays = VGroup(*[
            Line(car.get_right(), car.get_right() + RIGHT * 1.1 + UP * np.sin(a) * 0.5,
                 stroke_color=CYAN_NEON, stroke_width=0.7, stroke_opacity=0.6)
            for a in np.linspace(-0.5, 0.5, 8)
        ])

        self.play(
            GrowFromCenter(car, run_time=0.40),
            GrowFromCenter(truck, run_time=0.40),
        )
        self.play(
            LaggedStart(*[Create(r, run_time=0.12) for r in lidar_rays],
                        lag_ratio=0.04),
        )

        # Rays hit truck — change to red (blocked)
        self.play(
            lidar_rays.animate(run_time=0.35).set_stroke(RED_ALERT, opacity=0.55),
        )

        # Blind zone behind truck
        blind = Polygon(
            truck.get_right() + UP * 0.46,
            truck.get_right() + DOWN * 0.46,
            truck.get_right() + RIGHT * 2.5 + DOWN * 0.85,
            truck.get_right() + RIGHT * 2.5 + UP * 0.85,
            fill_color=RED_ALERT, fill_opacity=0.28, stroke_width=0,
        )
        self.play(FadeIn(blind, run_time=0.55))
        self.wait(0.4)

        # BIG "Not yet." text
        not_yet = Text("Not yet.", font_size=72,
                       color=RED_ALERT, font=FONT_PRIMARY, weight=BOLD)
        not_yet.move_to(RIGHT * 3.0 + DOWN * 0.2)

        # Stamp in — big, single hit
        not_yet.scale(1.4).set_opacity(0)
        self.add(not_yet)
        self.play(
            not_yet.animate(run_time=0.28, rate_func=rush_into)
                   .scale(1 / 1.4).set_opacity(1.0),
        )
        # Brief rebound
        self.play(
            not_yet.animate(run_time=0.08).scale(1.06),
            not_yet.animate(run_time=0.08).scale(1 / 1.06),
        )
        self.play(
            Flash(not_yet.get_center(), color=RED_ALERT,
                  flash_radius=1.2, num_lines=10, run_time=0.35),
        )
        self.wait(2.0)   # mandatory hold per guide

        self.close()
