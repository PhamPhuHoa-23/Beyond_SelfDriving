# beyond/scenes/part04/p04_s02_annotation_cost.py
# ─────────────────────────────────────────────────────────────────
# P4-02  ANNOTATION COST EXPLOSION  (~45s)
#
# Bar chart LEFT 60% — 3 bars grow bottom-up với particle trail + counter.
# Annotations RIGHT 35% — không overlap chart.
# "5× in 2 years" gold arrow.
# Câu hỏi cuối: "How can models learn with limited labeled data?"
#
# Render:  manim -ql "beyond/scenes/part04/p04_s02_annotation_cost.py" P04S02AnnotationCost
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, axes_deploy,
    BG_SPACE,
    P4_EFFICIENT, GOLD, GOLD_GLOW, BLUE_ELECTRIC, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=22)

BAR_DATA = [
    ("V2V4Real\n2022",  240_000,  BLUE_ELECTRIC),
    ("DAIR-V2X\n2023",  460_000,  P4_EFFICIENT),
    ("V2X-Real\n2024", 1_200_000, GREEN_SIGNAL),
]

CHART_LEFT  = -5.5
CHART_RIGHT = -0.5
CHART_SHIFT = LEFT * 2.5 + DOWN * 0.2


class P04S02AnnotationCost(BeyondScene):
    PART_COLOR = P4_EFFICIENT

    def construct(self):
        title_mob, sep = self.open("The Annotation Cost Explosion")
        self.wait(0.2)

        # ── Axes (LEFT 60%) ───────────────────────────────────
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1_400_000, 200_000],
            x_length=5.5,
            y_length=4.2,
            axis_config={"color": TEXT_DIM, "stroke_width": 1.4,
                         "include_tip": True, "tip_length": 0.16},
            y_axis_config={
                "numbers_to_include": [200_000, 600_000, 1_000_000],
                "label_direction": LEFT,
                "font_size": SIZE_MICRO,
                "decimal_number_config": {"num_decimal_places": 0},
            },
            x_axis_config={"include_numbers": False},
        ).shift(CHART_SHIFT)

        y_lbl = Text("Annotation count", font_size=SIZE_MICRO, color=TEXT_DIM, font=FONT_PRIMARY)
        y_lbl.rotate(PI/2).next_to(axes.y_axis.get_end(), LEFT, buff=0.35)

        self.play(axes_deploy(axes, "", ""))
        self.play(FadeIn(y_lbl, run_time=0.25))

        # ── 3 bars + counters ─────────────────────────────────
        bar_w     = 0.85
        bar_xs    = [1.0, 2.0, 3.0]
        bar_mobs  = []

        for i, ((name, value, color), bx) in enumerate(zip(BAR_DATA, bar_xs)):
            bar = Rectangle(
                width=bar_w,
                height=0.01,
                fill_color=color, fill_opacity=0.85, stroke_width=0,
            )
            bar.align_to(axes.get_origin(), DOWN)
            bar.set_x(axes.c2p(bx, 0)[0])

            target_h = axes.c2p(0, value)[1] - axes.get_origin()[1]

            # x-label
            x_lbl = Text(name, font_size=SIZE_MICRO - 1, color=color,
                         font=FONT_PRIMARY, line_spacing=0.38)
            x_lbl.next_to(axes.c2p(bx, 0), DOWN, buff=0.12)

            self.add(bar)
            counter_val = ValueTracker(0)
            counter_mob = Integer(0, color=color, font_size=SIZE_MICRO + 2)
            counter_mob.add_updater(lambda m, v=counter_val: m.set_value(int(v.get_value())).next_to(bar, UP, buff=0.08))
            self.add(counter_mob)

            # Particle emitter at top of bar
            particles = VGroup()
            for _ in range(6):
                p = Dot(radius=0.025, color=color, fill_opacity=0.7).move_to(bar.get_top())
                particles.add(p)

            self.play(
                AnimationGroup(
                    bar.animate(run_time=1.1, rate_func=smooth)
                       .stretch_to_fit_height(target_h)
                       .align_to(axes.get_origin(), DOWN)
                       .set_x(axes.c2p(bx, 0)[0]),
                    counter_val.animate(run_time=1.1, rate_func=smooth).set_value(value),
                    LaggedStart(*[
                        p.animate(run_time=0.50, rate_func=rush_from)
                         .shift(UP * float(RNG.uniform(0.25, 0.7)))
                         .set_fill(opacity=0)
                        for p in particles
                    ], lag_ratio=0.10),
                ),
            )
            counter_mob.remove_updater(counter_mob.get_updaters()[-1])
            self.play(Flash(bar.get_top(), color=color,
                            flash_radius=0.30, num_lines=5, run_time=0.22))
            self.play(FadeIn(x_lbl, shift=UP * 0.05, run_time=0.20))
            bar_mobs.append((bar, counter_mob))

        self.wait(0.3)

        # ── RIGHT side annotations ────────────────────────────
        ann_x = RIGHT * 2.8
        ann_y = UP * 1.5

        # "5× in 2 years" arrow
        five_x_lbl = Text("5× in 2 years", font_size=SIZE_LABEL - 1,
                           color=GOLD, font=FONT_PRIMARY, weight=BOLD)
        five_x_lbl.move_to(ann_x + ann_y)
        five_x_arr = Arrow(
            five_x_lbl.get_bottom() + DOWN * 0.1,
            five_x_lbl.get_bottom() + DOWN * 0.9,
            buff=0.0, color=GOLD, stroke_width=2.0, tip_length=0.16,
        )
        self.play(FadeIn(five_x_lbl, shift=DOWN * 0.08, run_time=0.35),
                  Create(five_x_arr, run_time=0.28))

        # Bullet points
        bullets = [
            "• Annotators: specialized + expensive",
            "• Toolkits: complex multi-pass",
            "• QC: 3-layer review required",
        ]
        bullet_mobs = VGroup(*[
            Text(b, font_size=SIZE_MICRO + 1, color=TEXT_DIM, font=FONT_PRIMARY)
            for b in bullets
        ]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        bullet_mobs.next_to(five_x_arr, DOWN, buff=0.22)
        self.play(
            LaggedStart(*[FadeIn(bm, shift=UP * 0.06, run_time=0.25)
                          for bm in bullet_mobs], lag_ratio=0.18),
        )
        self.wait(0.5)

        # ── Closing question ──────────────────────────────────
        q = Text("How can models learn with limited labeled data?",
                 font_size=SIZE_LABEL - 2, color=GOLD,
                 font=FONT_PRIMARY, slant=ITALIC)
        q.to_edge(DOWN, buff=0.50)
        self.play(Write(q, run_time=0.80))
        self.play(glow_pulse(q, GOLD, n_pulses=1, run_time=0.35))
        self.wait(1.5)

        self.close()
