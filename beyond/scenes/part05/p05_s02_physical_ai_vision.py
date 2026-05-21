# beyond/scenes/part05/p05_s02_physical_ai_vision.py
# ─────────────────────────────────────────────────────────────────
# P5-02  PHYSICAL AI VISION — 2 RÀO CẢN  (~60s)
#
# LLMs: internet data river → 1 trillion tokens → knows everything.
# Physical AI: robot data trickle → millions → cannot scale.
# Barrier 1: No web-scale robot data.
# Barrier 2: No human behavior model → Zombie City.
#
# Render:  manim -ql "beyond/scenes/part05/p05_s02_physical_ai_vision.py" P05S02PhysicalAI
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, bullet_reveal,
    P5_PHYSICAL, GOLD, CYAN_NEON, BLUE_ELECTRIC,
    RED_ALERT, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=44)


class P05S02PhysicalAI(BeyondScene):
    PART_COLOR = P5_PHYSICAL

    def construct(self):
        title_mob, sep = self.open("Why Physical AI Is Hard")
        self.wait(0.2)

        # ── LLMs: river of internet data ──────────────────────
        llm_title = Text("Why LLMs Succeeded:", font_size=SIZE_LABEL - 1,
                         color=BLUE_ELECTRIC, font=FONT_PRIMARY, weight=BOLD)
        llm_title.move_to(LEFT * 3.5 + UP * 2.0)
        self.play(FadeIn(llm_title, shift=DOWN * 0.06, run_time=0.28))

        data_sources = ["Books", "Wikipedia", "GitHub", "Reddit", "..."]
        src_mobs = VGroup(*[
            Text(s, font_size=SIZE_MICRO + 1, color=BLUE_ELECTRIC, font=FONT_PRIMARY)
            for s in data_sources
        ]).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        src_mobs.next_to(llm_title, DOWN, buff=0.18)

        self.play(
            LaggedStart(*[FadeIn(m, shift=RIGHT * 0.08, run_time=0.18)
                          for m in src_mobs], lag_ratio=0.12),
        )

        # Flow arrow → LLM box
        llm_box = RoundedRectangle(corner_radius=0.10, width=1.6, height=0.70,
                                   fill_color="#0D1829", fill_opacity=1.0,
                                   stroke_color=BLUE_ELECTRIC, stroke_width=1.8)
        llm_box.move_to(LEFT * 0.8 + UP * 0.8)
        llm_lbl = Text("LLM", font_size=SIZE_MICRO + 4, color=BLUE_ELECTRIC,
                       font=FONT_PRIMARY, weight=BOLD)
        llm_lbl.move_to(llm_box)

        arr_llm = Arrow(src_mobs.get_right() + RIGHT * 0.1,
                        llm_box.get_left(),
                        buff=0.05, color=BLUE_ELECTRIC,
                        stroke_width=2.5, tip_length=0.18)

        result_lbl = Text("Trillion tokens  →  Knows everything",
                          font_size=SIZE_MICRO + 1, color=GREEN_SIGNAL,
                          font=FONT_PRIMARY)
        result_lbl.next_to(llm_box, DOWN, buff=0.15)

        self.play(Create(arr_llm, run_time=0.35),
                  GrowFromCenter(llm_box, run_time=0.35),
                  FadeIn(llm_lbl, run_time=0.22))
        self.play(FadeIn(result_lbl, shift=UP * 0.06, run_time=0.28))
        self.wait(0.4)

        # ── Physical AI: trickle ──────────────────────────────
        phys_title = Text("Physical AI Data:", font_size=SIZE_LABEL - 1,
                          color=P5_PHYSICAL, font=FONT_PRIMARY, weight=BOLD)
        phys_title.move_to(RIGHT * 3.2 + UP * 2.0)
        self.play(FadeIn(phys_title, shift=DOWN * 0.06, run_time=0.28))

        robot_sources = ["Robot 1  →  10 hours", "Robot 2  →  10 hours",
                         "Robot 3  →  10 hours"]
        rob_mobs = VGroup(*[
            Text(s, font_size=SIZE_MICRO + 1, color=TEXT_DIM, font=FONT_PRIMARY)
            for s in robot_sources
        ]).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        rob_mobs.next_to(phys_title, DOWN, buff=0.18)

        self.play(
            LaggedStart(*[FadeIn(m, shift=RIGHT * 0.08, run_time=0.18)
                          for m in rob_mobs], lag_ratio=0.14),
        )

        trickle = Text("Trickle. Slow. Expensive.",
                       font_size=SIZE_MICRO + 2, color=RED_ALERT,
                       font=FONT_PRIMARY, slant=ITALIC)
        trickle.next_to(rob_mobs, DOWN, buff=0.18)
        self.play(FadeIn(trickle, shift=UP * 0.06, run_time=0.28))
        self.wait(0.5)

        # ── BARRIER 1 ─────────────────────────────────────────
        b1_bg = RoundedRectangle(corner_radius=0.10, width=8.5, height=0.75,
                                 fill_color="#1A050A", fill_opacity=1.0,
                                 stroke_color=RED_ALERT, stroke_width=1.8)
        b1_bg.move_to(DOWN * 0.5)
        b1_txt = Text("BARRIER 1:  No web-scale robot behavior data.",
                      font_size=SIZE_LABEL - 2, color=RED_ALERT,
                      font=FONT_PRIMARY, weight=BOLD)
        b1_txt.move_to(b1_bg)
        self.play(GrowFromCenter(b1_bg, run_time=0.35),
                  FadeIn(b1_txt, run_time=0.25))
        self.wait(0.5)

        # ── BARRIER 2: Zombie city visual ─────────────────────
        b2_bg = b1_bg.copy().set_color(RED_ALERT).set_y(DOWN * 1.5 + DOWN * 0.0)
        b2_bg.shift(DOWN * 0.82)
        b2_txt = Text("BARRIER 2:  Robots with no model of human behavior.",
                      font_size=SIZE_LABEL - 2, color=RED_ALERT,
                      font=FONT_PRIMARY, weight=BOLD)
        b2_txt.move_to(b2_bg)
        self.play(GrowFromCenter(b2_bg, run_time=0.30),
                  FadeIn(b2_txt, run_time=0.22))
        self.wait(0.3)

        # Quick zombie pedestrian demo (3 gray squares, straight lines, intersect)
        zombie_area = Rectangle(width=4.0, height=1.2,
                                fill_color="#060D15", fill_opacity=0.80,
                                stroke_color=TEXT_GHOST, stroke_width=0.8)
        zombie_area.to_edge(DOWN, buff=0.38)
        z_label = Text('"Zombie City"', font_size=SIZE_MICRO + 2,
                       color=RED_ALERT, font=FONT_PRIMARY, weight=BOLD)
        z_label.next_to(zombie_area, UP, buff=0.08)

        zombies = VGroup(*[
            Square(side_length=0.20, fill_color=TEXT_GHOST, fill_opacity=0.75,
                   stroke_width=0)
            .move_to(zombie_area.get_center()
                     + np.array([float(RNG.uniform(-1.7, 1.7)), 0, 0]))
            for _ in range(5)
        ])

        self.play(FadeIn(zombie_area, run_time=0.25),
                  FadeIn(z_label, run_time=0.20))
        self.play(LaggedStart(*[GrowFromCenter(z, run_time=0.14) for z in zombies],
                              lag_ratio=0.10))
        # Walk straight through each other
        dirs = [np.array([float(RNG.uniform(-0.6, 0.6)), 0, 0]) for _ in range(5)]
        self.play(LaggedStart(*[
            z.animate(run_time=0.60, rate_func=linear).shift(d)
            for z, d in zip(zombies, dirs)
        ], lag_ratio=0.04))
        self.wait(0.8)

        self.close()
