# beyond/scenes/part03/p03_s02_sim_gap.py
# ─────────────────────────────────────────────────────────────────
# P3-02  SIM-TO-REAL GAP  (~45s)
#
# Màn hình chia đôi bởi đường nứt sét đánh (lightning crack).
# Trái: Simulation world — clean geometry, teal.
# Phải: Real world — messy, amber.
# Mũi tên cố đi từ sim→real nhưng bị chặn.
# Đường nứt từ từ "hàn lại" ở cuối — hành trình Part 3.
#
# Render:  manim -ql "beyond/scenes/part03/p03_s02_sim_gap.py" P03S02SimGap
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    BG_SPACE, BG_PANEL,
    P3_SIM, P4_EFFICIENT, RED_ALERT, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=31)


def _lightning_crack() -> VMobject:
    """Zigzag vertical crack from top to bottom."""
    pts = [UP * 4.0]
    y = 4.0
    while y > -4.0:
        y -= float(RNG.uniform(0.5, 1.2))
        x = float(RNG.uniform(-0.35, 0.35))
        pts.append(np.array([x, y, 0]))
    pts.append(DOWN * 4.0)
    crack = VMobject(stroke_color="#00BFFF", stroke_width=2.5,
                     stroke_opacity=0.85)
    crack.set_points_as_corners(pts)
    return crack


def _sim_element(pos: np.ndarray) -> VGroup:
    """Clean geometric element for SIM world."""
    s = RNG.uniform(0.15, 0.40)
    shape_type = int(RNG.integers(0, 3))
    if shape_type == 0:
        m = Square(side_length=float(s), fill_color=P3_SIM, fill_opacity=0.35,
                   stroke_color=P3_SIM, stroke_width=1.0)
    elif shape_type == 1:
        m = Rectangle(width=float(s)*1.8, height=float(s)*0.8,
                      fill_color=P3_SIM, fill_opacity=0.30,
                      stroke_color=P3_SIM, stroke_width=1.0)
    else:
        m = Circle(radius=float(s)*0.5, fill_color=P3_SIM, fill_opacity=0.25,
                   stroke_color=P3_SIM, stroke_width=1.0)
    m.move_to(pos)
    return m


def _real_element(pos: np.ndarray) -> VGroup:
    """Irregular, noisy element for REAL world."""
    # Slightly tilted, irregular rectangle
    s = float(RNG.uniform(0.18, 0.45))
    angle = float(RNG.uniform(-0.3, 0.3))
    m = Rectangle(width=s*float(RNG.uniform(1.0, 2.2)),
                  height=s*float(RNG.uniform(0.5, 1.0)),
                  fill_color=P4_EFFICIENT, fill_opacity=0.28,
                  stroke_color=P4_EFFICIENT, stroke_width=0.9)
    m.rotate(angle)
    m.move_to(pos)
    # Add noise dots
    noise = VGroup(*[
        Dot(radius=float(RNG.uniform(0.02, 0.05)),
            color=P4_EFFICIENT, fill_opacity=float(RNG.uniform(0.2, 0.6)))
        .move_to(pos + np.array([float(RNG.uniform(-0.5, 0.5)),
                                  float(RNG.uniform(-0.3, 0.3)), 0]))
        for _ in range(int(RNG.integers(2, 5)))
    ])
    return VGroup(m, noise)


class P03S02SimGap(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("The Simulation-to-Reality Gap")
        self.wait(0.2)

        # ── LEFT half: Simulation ─────────────────────────────
        sim_bg = Rectangle(width=7.0, height=6.5,
                           fill_color="#051510", fill_opacity=0.6,
                           stroke_width=0)
        sim_bg.align_to(LEFT * 7.0, LEFT).align_to(DOWN * 3.5, DOWN)

        sim_title = Text("Simulation", font_size=SIZE_LABEL,
                         color=P3_SIM, font=FONT_PRIMARY, weight=BOLD)
        sim_title.move_to(LEFT * 3.5 + UP * 2.2)

        sim_sub = Text("Clean  ·  Perfect  ·  Digital",
                       font_size=SIZE_MICRO, color=P3_SIM,
                       font=FONT_PRIMARY)
        sim_sub.next_to(sim_title, DOWN, buff=0.10)

        # Geometric elements on left side
        sim_positions = [LEFT*2.8+UP*0.8, LEFT*4.2+UP*0.4, LEFT*1.8+DOWN*0.5,
                         LEFT*3.5+DOWN*1.2, LEFT*2.2+DOWN*1.8]
        sim_elements = VGroup(*[_sim_element(p) for p in sim_positions])

        # Road lines (perfect, straight)
        road_l = Line(LEFT*6.5+DOWN*2.5, LEFT*0.2+DOWN*2.5,
                      stroke_color=P3_SIM, stroke_width=1.0, stroke_opacity=0.5)
        road_center = DashedLine(LEFT*6.5+DOWN*2.0, LEFT*0.2+DOWN*2.0,
                                 stroke_color=P3_SIM, stroke_width=0.6,
                                 stroke_opacity=0.35, dash_length=0.15)

        # ── RIGHT half: Reality ───────────────────────────────
        real_bg = Rectangle(width=7.0, height=6.5,
                            fill_color="#160C05", fill_opacity=0.6,
                            stroke_width=0)
        real_bg.align_to(RIGHT * 7.0, RIGHT).align_to(DOWN * 3.5, DOWN)

        real_title = Text("Reality", font_size=SIZE_LABEL,
                          color=P4_EFFICIENT, font=FONT_PRIMARY, weight=BOLD)
        real_title.move_to(RIGHT * 3.5 + UP * 2.2)

        real_sub = Text("Noisy  ·  Messy  ·  Unpredictable",
                        font_size=SIZE_MICRO, color=P4_EFFICIENT,
                        font=FONT_PRIMARY)
        real_sub.next_to(real_title, DOWN, buff=0.10)

        real_positions = [RIGHT*2.5+UP*0.9, RIGHT*4.0+UP*0.3, RIGHT*1.8+DOWN*0.6,
                          RIGHT*3.2+DOWN*1.1, RIGHT*2.0+DOWN*1.9]
        real_elements = VGroup(*[_real_element(p) for p in real_positions])

        # Cracked road (imperfect)
        road_r = Line(RIGHT*0.2+DOWN*2.5, RIGHT*6.5+DOWN*2.5,
                      stroke_color=P4_EFFICIENT, stroke_width=0.9,
                      stroke_opacity=0.45)
        crack_line = DashedLine(RIGHT*0.2+DOWN*2.1, RIGHT*6.5+DOWN*2.3,
                                stroke_color=P4_EFFICIENT, stroke_width=0.5,
                                stroke_opacity=0.25, dash_length=0.20)

        # ── Reveal left then right ─────────────────────────────
        self.play(
            FadeIn(sim_bg, run_time=0.40),
            FadeIn(sim_title, shift=RIGHT*0.08, run_time=0.35),
            FadeIn(sim_sub, run_time=0.25),
        )
        self.play(
            LaggedStart(*[GrowFromCenter(e, run_time=0.22) for e in sim_elements],
                        lag_ratio=0.10),
            Create(road_l, run_time=0.35),
            Create(road_center, run_time=0.35),
        )
        self.wait(0.2)

        # ── Lightning CRACK draws from top to bottom ──────────
        crack = _lightning_crack()
        self.play(
            Create(crack, run_time=0.50, rate_func=rush_into),
            Flash(ORIGIN, color="#00BFFF", flash_radius=0.5,
                  num_lines=8, run_time=0.35),
        )

        # Right side reveals
        self.play(
            FadeIn(real_bg, run_time=0.35),
            FadeIn(real_title, shift=LEFT*0.08, run_time=0.35),
            FadeIn(real_sub, run_time=0.25),
        )
        self.play(
            LaggedStart(*[GrowFromCenter(e, run_time=0.22) for e in real_elements],
                        lag_ratio=0.10),
            Create(road_r, run_time=0.30),
            Create(crack_line, run_time=0.30),
        )
        self.wait(0.3)

        # ── Gap arrow (blocked) ───────────────────────────────
        gap_arrow = Arrow(
            LEFT * 0.5 + DOWN * 0.8, RIGHT * 0.5 + DOWN * 0.8,
            buff=0.0, color=RED_ALERT, stroke_width=2.2, tip_length=0.18,
        )
        gap_lbl = Text("Sim-to-Real Gap", font_size=SIZE_MICRO + 2,
                       color=RED_ALERT, font=FONT_PRIMARY, weight=BOLD)
        gap_lbl.next_to(gap_arrow, DOWN, buff=0.12)

        self.play(
            Create(gap_arrow, run_time=0.40),
            FadeIn(gap_lbl, run_time=0.30),
        )
        # Arrow blocked: shake
        for _ in range(2):
            self.play(gap_arrow.animate(run_time=0.08).shift(RIGHT*0.10))
            self.play(gap_arrow.animate(run_time=0.08).shift(LEFT*0.10))
        self.wait(0.5)

        # ── Crack heals: "Part 3 bridges this gap" ─────────────
        bridge_txt = Text("Part 3 bridges this gap.",
                          font_size=SIZE_LABEL - 1, color=GREEN_SIGNAL,
                          font=FONT_PRIMARY, slant=ITALIC)
        bridge_txt.to_edge(DOWN, buff=0.52)

        self.play(
            crack.animate(run_time=1.2, rate_func=smooth)
                 .set_stroke(GREEN_SIGNAL, opacity=0.75)
                 .set_stroke(width=3.5),
        )
        self.play(
            Write(bridge_txt, run_time=0.80),
            Flash(ORIGIN, color=GREEN_SIGNAL,
                  flash_radius=0.35, num_lines=6, run_time=0.40),
        )
        self.wait(1.8)

        self.close()
