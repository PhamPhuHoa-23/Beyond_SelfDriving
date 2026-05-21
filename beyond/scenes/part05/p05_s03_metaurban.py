# beyond/scenes/part05/p05_s03_metaurban.py
# ─────────────────────────────────────────────────────────────────
# P5-03  METAURBAN — "THE WORLD IS COMPOSITIONAL"  (~70s)
#
# Quote card: từng chữ bay vào từ random positions → hợp thành quote.
# Stuart Geman attribution.
# Procedural Generation: terminal script → generator engine → ∞ scenes.
# Power-law scaling chart: diversity > quantity.
#
# Render:  manim -ql "beyond/scenes/part05/p05_s03_metaurban.py" P05S03MetaUrban
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, axes_deploy, curve_trace, glow_pulse,
    BG_SPACE, BG_PANEL,
    P5_PHYSICAL, GOLD, GOLD_GLOW, CYAN_NEON, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_BODY, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=88)

QUOTE_TEXT = '"The world is compositional,'
QUOTE_TEXT2 = '  or there is a god."'
ATTR_TEXT  = "— Stuart Geman"


class P05S03MetaUrban(BeyondScene):
    PART_COLOR = P5_PHYSICAL

    def construct(self):
        title_mob, sep = self.open("MetaUrban — Infinite Compositional Environments")
        self.wait(0.15)

        # ── QUOTE — words fly in from random positions ─────────
        # Build target text first (invisible), then animate each word
        q1 = Text(QUOTE_TEXT,  font_size=SIZE_BODY + 4, color=GOLD,
                  font=FONT_PRIMARY, slant=ITALIC)
        q2 = Text(QUOTE_TEXT2, font_size=SIZE_BODY + 4, color=GOLD,
                  font=FONT_PRIMARY, slant=ITALIC)
        q_grp = VGroup(q1, q2).arrange(DOWN, buff=0.12).move_to(UP * 0.5)

        attr = Text(ATTR_TEXT, font_size=SIZE_LABEL - 2, color=TEXT_DIM,
                    font=FONT_PRIMARY, slant=ITALIC)
        attr.next_to(q_grp, DOWN, buff=0.30).to_edge(RIGHT, buff=1.5)

        # Each word of q1 + q2 starts at random off-screen position
        all_words = list(q1) + list(q2)
        for w in all_words:
            w.save_state()
            w.move_to(np.array([float(RNG.uniform(-6, 6)),
                                 float(RNG.uniform(-4, 4)), 0]))
            w.set_opacity(0)

        self.add(q_grp)
        self.play(
            LaggedStart(*[
                w.animate(run_time=0.55, rate_func=smooth).restore()
                for w in all_words
            ], lag_ratio=0.06),
            run_time=2.0,
        )
        self.play(FadeIn(attr, shift=LEFT * 0.10, run_time=0.40))
        self.wait(3.0)   # mandatory hold per guide

        self.play(FadeOut(q_grp, run_time=0.35), FadeOut(attr, run_time=0.35))
        self.wait(0.2)

        # ── Procedural Generation Demo ─────────────────────────
        # Terminal-style code block
        terminal_bg = RoundedRectangle(
            corner_radius=0.10, width=6.5, height=2.4,
            fill_color="#050D0F", fill_opacity=1.0,
            stroke_color=CYAN_NEON, stroke_width=1.4,
        ).move_to(LEFT * 2.5 + UP * 0.8)

        code_lines = [
            "$ generate_scene(",
            "    blocks=4,  intersections='T-shaped',",
            "    lane_width=3.2,",
            "    objects=['bench','tree','lamp'],",
            "    density='medium'  )",
        ]
        code_mobs = VGroup(*[
            Text(ln, font_size=SIZE_MICRO, color=GREEN_SIGNAL,
                 font="Courier New")
            for ln in code_lines
        ]).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        code_mobs.move_to(terminal_bg.get_center()).shift(LEFT * 0.2)

        self.play(FadeIn(terminal_bg, run_time=0.35))
        self.play(
            LaggedStart(*[
                AddTextLetterByLetter(ln, run_time=0.25, rate_func=linear)
                for ln in code_mobs
            ], lag_ratio=0.4),
        )
        self.wait(0.3)

        # Generator gear icon (spinning cog)
        gear = Circle(radius=0.45, fill_color="#0A1A28", fill_opacity=1.0,
                      stroke_color=P5_PHYSICAL, stroke_width=2.2)
        gear.move_to(ORIGIN + DOWN * 0.0)
        # Gear teeth
        teeth = VGroup(*[
            Rectangle(width=0.12, height=0.22,
                      fill_color=P5_PHYSICAL, fill_opacity=1.0, stroke_width=0)
            .move_to(gear.get_center() + np.array([
                np.cos(i * TAU/8) * 0.52,
                np.sin(i * TAU/8) * 0.52, 0
            ]))
            .rotate(i * TAU/8)
            for i in range(8)
        ])
        gear_grp = VGroup(gear, teeth)
        gear_lbl = Text("GENERATOR", font_size=SIZE_MICRO + 1,
                        color=P5_PHYSICAL, font=FONT_PRIMARY, weight=BOLD)
        gear_lbl.move_to(gear)

        arr_to_gear = Arrow(terminal_bg.get_right(),
                            gear.get_left() + LEFT * 0.08,
                            buff=0.05, color=CYAN_NEON,
                            stroke_width=1.8, tip_length=0.16)
        self.play(
            Create(arr_to_gear, run_time=0.28),
            GrowFromCenter(gear_grp, run_time=0.40),
            FadeIn(gear_lbl, run_time=0.25),
        )

        # Spinning gear
        self.play(
            Rotate(gear_grp, angle=TAU, run_time=1.2, rate_func=smooth),
        )
        self.play(glow_pulse(gear, P5_PHYSICAL, n_pulses=1, run_time=0.35))

        # Output: scene 1 → 2 → 3 → ∞
        out_labels = ["Scene 1", "Scene 2", "Scene 3", "∞ scenes"]
        out_mobs = VGroup(*[
            Text(lbl, font_size=SIZE_MICRO + 2,
                 color=P5_PHYSICAL if "∞" not in lbl else GOLD,
                 font=FONT_PRIMARY, weight=BOLD if "∞" in lbl else NORMAL)
            for lbl in out_labels
        ]).arrange(RIGHT, buff=0.45)
        out_mobs.move_to(RIGHT * 3.8 + UP * 0.0)

        arr_from_gear = Arrow(gear.get_right() + RIGHT * 0.08,
                              out_mobs.get_left() + LEFT * 0.08,
                              buff=0.05, color=P5_PHYSICAL,
                              stroke_width=1.8, tip_length=0.16)
        self.play(
            Create(arr_from_gear, run_time=0.25),
            LaggedStart(*[FadeIn(m, shift=LEFT * 0.08, run_time=0.22)
                          for m in out_mobs], lag_ratio=0.15),
        )
        self.wait(0.4)

        # ── Power-law scaling chart ────────────────────────────
        # Fade gear section
        self.play(
            VGroup(terminal_bg, code_mobs, arr_to_gear, gear_grp,
                   gear_lbl, arr_from_gear, out_mobs)
            .animate(run_time=0.50).set_opacity(0.15),
        )

        axes = Axes(
            x_range=[0, 100, 20], y_range=[0, 1.1, 0.25],
            x_length=6.5, y_length=3.5,
            axis_config={"color": TEXT_DIM, "stroke_width": 1.3,
                         "include_tip": True, "tip_length": 0.15},
        ).move_to(DOWN * 0.5)

        self.play(axes_deploy(axes, "Unique training layouts", "Performance"))

        power_law  = axes.plot(lambda x: 0.92 * x**0.40 / 100 if x > 0 else 0,
                               x_range=[1, 100], color=P5_PHYSICAL,
                               stroke_width=3.0)
        linear_ref = axes.plot(lambda x: 0.50 * x / 100,
                               x_range=[1, 100], color=TEXT_GHOST,
                               stroke_width=1.5, stroke_opacity=0.50)

        self.play(
            Create(linear_ref, run_time=0.80, rate_func=smooth),
        )
        self.play(
            Create(power_law, run_time=1.20, rate_func=smooth),
        )

        # Annotation
        ann = Text('"Diversity > Quantity"', font_size=SIZE_LABEL - 1,
                   color=GOLD, font=FONT_PRIMARY, slant=ITALIC)
        ann.next_to(axes, RIGHT, buff=0.3)
        self.play(FadeIn(ann, shift=LEFT * 0.08, run_time=0.35))
        self.wait(1.2)

        self.close()
