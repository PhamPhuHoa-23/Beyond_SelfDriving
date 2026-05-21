# beyond/scenes/part03/p03_s12_simboost.py — SimBoost: sim data augments real
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components import (
    BeyondScene, axes_deploy,
    P3_SIM, GREEN_SIGNAL, GOLD, TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P03S12SimBoost(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("SimBoost — Simulation Augments Real Data")
        self.wait(0.2)

        # Concept: real data (small) + sim data (large) → better model
        real_box_lbl = Text("Real data\n(limited, expensive)", font_size=SIZE_MICRO + 1,
                            color=TEXT_DIM, font=FONT_PRIMARY, line_spacing=0.38)
        sim_box_lbl  = Text("Sim data\n(unlimited, cheap)", font_size=SIZE_MICRO + 1,
                            color=P3_SIM, font=FONT_PRIMARY, line_spacing=0.38)
        plus = Text("+", font_size=SIZE_LABEL + 8, color=GOLD, font=FONT_PRIMARY)
        eq   = Text("=", font_size=SIZE_LABEL + 8, color=GOLD, font=FONT_PRIMARY)
        result_lbl = Text("Strong\nV2X Model", font_size=SIZE_LABEL - 1,
                          color=GREEN_SIGNAL, font=FONT_PRIMARY, weight=BOLD,
                          line_spacing=0.38)

        row = VGroup(real_box_lbl, plus, sim_box_lbl, eq, result_lbl)
        row.arrange(RIGHT, buff=0.50).move_to(UP * 1.0)

        self.play(
            LaggedStart(*[FadeIn(m, shift=DOWN * 0.06, run_time=0.28)
                          for m in row], lag_ratio=0.20),
        )
        self.wait(0.4)

        # Chart: performance vs data
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.1, 0.25],
            x_length=7.5, y_length=3.5,
            axis_config={"color": TEXT_DIM, "stroke_width": 1.3,
                         "include_tip": True, "tip_length": 0.15},
        ).move_to(DOWN * 0.8)
        self.play(axes_deploy(axes, "Amount of real training data", "Model performance"))

        real_only = axes.plot(lambda x: 0.85 * (1 - np.exp(-x * 0.5)),
                              x_range=[0, 10], color=TEXT_DIM, stroke_width=2.0)
        simboost  = axes.plot(lambda x: 0.95 * (1 - np.exp(-x * 0.8)),
                              x_range=[0, 10], color=P3_SIM, stroke_width=2.5)

        self.play(Create(real_only, run_time=0.90), Create(simboost, run_time=0.90))

        # Labels on curves
        lbl_r = Text("Real data only", font_size=SIZE_MICRO, color=TEXT_DIM, font=FONT_PRIMARY)
        lbl_r.next_to(axes.c2p(8, 0.73), UR, buff=0.06)
        lbl_s = Text("SimBoost (real + sim)", font_size=SIZE_MICRO, color=P3_SIM, font=FONT_PRIMARY)
        lbl_s.next_to(axes.c2p(7, 0.92), UL, buff=0.06)
        self.play(FadeIn(lbl_r, shift=UP*0.06), FadeIn(lbl_s, shift=UP*0.06))
        self.wait(1.2)
        self.close()
