# beyond/scenes/part02/p02_s08_dataset.py — V2X-Real dataset overview
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, axes_deploy,
    P2_COOP, BLUE_ELECTRIC, GREEN_SIGNAL, GOLD,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=77)

class P02S08Dataset(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("V2X-Real — UCLA's Real-World V2X Dataset")
        self.wait(0.2)

        # Stats cards (top row)
        stats = [
            ("V2X-Real", "1.2M", "annotations", GREEN_SIGNAL),
            ("V2V4Real",  "240K", "annotations", BLUE_ELECTRIC),
            ("DAIR-V2X",  "460K", "annotations", P2_COOP),
        ]
        cards = VGroup()
        for name, val, lbl, col in stats:
            bg = RoundedRectangle(corner_radius=0.12, width=2.8, height=1.5,
                                  fill_color=BG_PANEL, fill_opacity=1.0,
                                  stroke_color=col, stroke_width=1.6)
            nt = Text(name, font_size=SIZE_MICRO + 2, color=col,
                      font=FONT_PRIMARY, weight=BOLD)
            vt = Text(val, font_size=SIZE_LABEL + 4, color=col,
                      font=FONT_PRIMARY, weight=BOLD)
            lt = Text(lbl, font_size=SIZE_MICRO, color=TEXT_DIM, font=FONT_PRIMARY)
            VGroup(nt, vt, lt).arrange(DOWN, buff=0.06).move_to(bg)
            cards.add(VGroup(bg, nt, vt, lt))
        cards.arrange(RIGHT, buff=0.45).move_to(UP * 1.8)

        self.play(
            LaggedStart(*[GrowFromCenter(c[0], run_time=0.30) for c in cards],
                        lag_ratio=0.15),
        )
        self.play(
            LaggedStart(*[FadeIn(VGroup(*c[1:]), shift=DOWN * 0.06, run_time=0.25)
                          for c in cards], lag_ratio=0.15),
        )
        self.wait(0.3)

        # Feature highlights (left)
        feat_lbl = Text("V2X-Real Features:", font_size=SIZE_LABEL - 1,
                        color=GREEN_SIGNAL, font=FONT_PRIMARY, weight=BOLD)
        feat_lbl.move_to(LEFT * 4.0 + UP * 0.6)
        features = [
            "• Infrastructure + Vehicle sensors",
            "• Multi-modal: LiDAR + Camera + Radar",
            "• 5 intersections, real traffic",
            "• Annotated with 3D bounding boxes",
        ]
        feat_mobs = VGroup(*[
            Text(f, font_size=SIZE_MICRO + 1, color=TEXT_DIM, font=FONT_PRIMARY)
            for f in features
        ]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        feat_mobs.next_to(feat_lbl, DOWN, buff=0.18)

        self.play(FadeIn(feat_lbl, shift=DOWN * 0.06, run_time=0.25))
        self.play(
            LaggedStart(*[FadeIn(m, shift=RIGHT * 0.08, run_time=0.22)
                          for m in feat_mobs], lag_ratio=0.14),
        )

        # Simple bar chart (right) — growth over time
        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 1_400_000, 400_000],
            x_length=4.0, y_length=3.2,
            axis_config={"color": TEXT_DIM, "stroke_width": 1.2,
                         "include_tip": False},
        ).move_to(RIGHT * 3.5 + DOWN * 0.4)

        self.play(Create(axes.y_axis, run_time=0.28),
                  Create(axes.x_axis, run_time=0.28))

        bar_info = [(1.0, 240_000, BLUE_ELECTRIC, "V2V4Real\n'22"),
                    (2.0, 460_000, P2_COOP,       "DAIR\n'23"),
                    (3.0, 1_200_000, GREEN_SIGNAL, "V2X-Real\n'24")]

        for bx, val, col, name in bar_info:
            bar = Rectangle(width=0.7, height=0.01,
                            fill_color=col, fill_opacity=0.85, stroke_width=0)
            bar.align_to(axes.get_origin(), DOWN).set_x(axes.c2p(bx, 0)[0])
            target_h = axes.c2p(0, val)[1] - axes.get_origin()[1]
            xl = Text(name, font_size=SIZE_MICRO - 1, color=col, font=FONT_PRIMARY,
                      line_spacing=0.35)
            xl.next_to(axes.c2p(bx, 0), DOWN, buff=0.10)
            self.play(
                bar.animate(run_time=0.8, rate_func=smooth)
                   .stretch_to_fit_height(target_h)
                   .align_to(axes.get_origin(), DOWN)
                   .set_x(axes.c2p(bx, 0)[0]),
                FadeIn(xl, run_time=0.28),
            )

        self.wait(1.2)
        self.close()
