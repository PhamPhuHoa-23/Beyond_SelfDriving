# beyond/scenes/part02/p02_s02_background.py
# ─────────────────────────────────────────────────────────────────
# P2-02  1.19 TRIỆU NGƯỜI  (~40s)
#
# Counter đếm lên 0→1,190,000 màu đổi trắng→đỏ.
# Grid 10×10 icon xe — 94 flash đỏ (94% human error).
# Waymo -80%: bar chart nhỏ + brace label.
#
# Render:  manim -ql "beyond/scenes/part02/p02_s02_background.py" P02S02Background
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    BG_SPACE, BG_PANEL,
    P2_COOP, RED_ALERT, RED_DIM, GREEN_SIGNAL,
    GOLD, CYAN_NEON,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_BODY, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=33)
TARGET = 1_190_000


def _car_icon_small(color: str, size: float = 0.30) -> VGroup:
    body = RoundedRectangle(corner_radius=0.04, width=size, height=size * 0.55,
                            fill_color=color, fill_opacity=1.0, stroke_width=0)
    roof = Rectangle(width=size * 0.50, height=size * 0.30,
                     fill_color=color, fill_opacity=1.0, stroke_width=0)
    roof.align_to(body, UP).shift(DOWN * 0.04).shift(LEFT * size * 0.05)
    return VGroup(body, roof)


class P02S02Background(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("Why Cooperative Perception?")
        self.wait(0.2)

        # ── DEATH COUNTER ─────────────────────────────────────
        counter_val = ValueTracker(0)

        counter_mob = Integer(0, color=TEXT_WHITE,
                              font_size=72)
        counter_mob.move_to(UP * 1.6 + LEFT * 2.5)

        def counter_updater(mob):
            v = int(counter_val.get_value())
            mob.set_value(v)
            # Color: white → red as counter rises
            alpha = min(1.0, v / TARGET)
            mob.set_color(interpolate_color(TEXT_WHITE, RED_ALERT, alpha ** 0.5))

        counter_mob.add_updater(counter_updater)
        self.add(counter_mob)

        label = Text("traffic deaths per year worldwide",
                     font_size=SIZE_MICRO + 2, color=TEXT_DIM,
                     font=FONT_PRIMARY)
        label.next_to(counter_mob, DOWN, buff=0.18)
        self.play(FadeIn(label, run_time=0.30))

        self.play(
            counter_val.animate(run_time=2.5, rate_func=smooth)
                       .set_value(TARGET),
        )
        counter_mob.remove_updater(counter_updater)

        # Lock-in flash
        self.play(
            Flash(counter_mob.get_center(), color=RED_ALERT,
                  flash_radius=1.0, num_lines=10, run_time=0.40),
            counter_mob.animate(run_time=0.15).scale(1.12),
            counter_mob.animate(run_time=0.15).scale(1/1.12),
        )
        self.wait(0.4)

        # ── 10×10 ICON GRID — 94% human error ────────────────
        GRID_N = 10
        CELL   = 0.44
        HUMAN_ERROR = 94    # out of 100

        icons = VGroup()
        positions = []
        for r in range(GRID_N):
            for c in range(GRID_N):
                x = (c - GRID_N / 2 + 0.5) * CELL + 2.8
                y = (r - GRID_N / 2 + 0.5) * CELL * 0.80 + 0.3
                positions.append(np.array([x, y, 0]))
                icons.add(_car_icon_small(TEXT_GHOST).move_to([x, y, 0]))

        # Shuffle to pick 94 "human error" icons
        indices = list(range(100))
        RNG.shuffle(indices)
        error_idx = set(indices[:HUMAN_ERROR])

        self.play(
            LaggedStart(*[GrowFromCenter(ic, run_time=0.04)
                          for ic in icons], lag_ratio=0.015),
        )
        self.wait(0.3)

        # Flash 94 icons red
        self.play(
            LaggedStart(*[
                icons[i].animate(run_time=0.12).set_fill(RED_ALERT, 1.0)
                for i in indices[:HUMAN_ERROR]
            ], lag_ratio=0.012),
        )

        pct_lbl = Text("94% — human error", font_size=SIZE_LABEL - 1,
                       color=RED_ALERT, font=FONT_PRIMARY, weight=BOLD)
        pct_lbl.move_to(RIGHT * 2.8 + UP * 1.85)
        self.play(FadeIn(pct_lbl, shift=DOWN * 0.08, run_time=0.35))
        self.wait(0.5)

        # Waymo reduction: 6 green icons grow
        self.play(
            LaggedStart(*[
                icons[i].animate(run_time=0.20)
                        .set_fill(GREEN_SIGNAL, 1.0)
                        .scale(1.3)
                for i in indices[HUMAN_ERROR:]  # last 6
            ], lag_ratio=0.12),
        )

        waymo_txt = Text("Waymo AV:  −80% injury crashes",
                         font_size=SIZE_MICRO + 3, color=GREEN_SIGNAL,
                         font=FONT_PRIMARY, weight=BOLD)
        waymo_txt.move_to(RIGHT * 2.8 + UP * 1.35)
        self.play(FadeIn(waymo_txt, shift=DOWN * 0.08, run_time=0.35))
        self.wait(0.3)

        # Shrink error icons to 20% (visual of 80% reduction)
        self.play(
            LaggedStart(*[
                icons[i].animate(run_time=0.20).scale(0.50)
                for i in indices[:HUMAN_ERROR]
            ], lag_ratio=0.008),
        )
        self.wait(0.5)

        # ── Bridge question ───────────────────────────────────
        bridge = Text("Can AV technology close the gap further?",
                      font_size=SIZE_LABEL - 1, color=GOLD,
                      font=FONT_PRIMARY, slant=ITALIC)
        bridge.to_edge(DOWN, buff=0.50)
        self.play(Write(bridge, run_time=0.80))
        self.wait(1.5)

        self.close()
