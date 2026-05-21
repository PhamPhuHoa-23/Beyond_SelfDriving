# beyond/scenes/part03/p03_s08_localization.py
# ─────────────────────────────────────────────────────────────────
# P3-08  WHY LOCALIZATION MATTERS  (~40s)
#
# Demo: 1m của localization error → object association failure.
# Infrastructure sees pedestrian at (x, y).
# Vehicle localizes itself wrong → thinks pedestrian is at wrong spot.
# Result: wrong avoidance → near-miss.
# Fix: CooperFuse + precise localization → correct association.
#
# Render:  manim -ql "beyond/scenes/part03/p03_s08_localization.py" P03S08Localization
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    P3_SIM, CYAN_NEON, ORANGE_INFRA, P5_PHYSICAL,
    RED_ALERT, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)


class P03S08Localization(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("Localization Error — Why 1 Meter Matters")
        self.wait(0.2)

        # Road
        road = Rectangle(width=13.0, height=1.2,
                         fill_color="#050D18", fill_opacity=1.0,
                         stroke_color="#0D1829", stroke_width=1.0)
        road.move_to(DOWN * 0.5)
        dash = DashedLine(LEFT * 6, RIGHT * 6, dash_length=0.25,
                          stroke_color=TEXT_DIM, stroke_width=0.5,
                          stroke_opacity=0.35)
        dash.move_to(DOWN * 0.5)
        self.play(FadeIn(road, run_time=0.35), Create(dash, run_time=0.28))

        # Vehicle
        veh_true = Rectangle(width=0.85, height=0.45,
                              fill_color=CYAN_NEON, fill_opacity=0.85,
                              stroke_color=WHITE, stroke_width=1.2)
        veh_true.move_to(LEFT * 3.5 + DOWN * 0.5)
        self.play(GrowFromCenter(veh_true, run_time=0.30))

        # Pedestrian (infrastructure sees correctly)
        ped = Circle(radius=0.15, fill_color=P5_PHYSICAL, fill_opacity=1.0,
                     stroke_color=WHITE, stroke_width=0.8)
        ped.move_to(RIGHT * 1.2 + DOWN * 0.5)
        infra_label = Text("Infra sees pedestrian at X=1.2m",
                           font_size=SIZE_MICRO + 1, color=ORANGE_INFRA,
                           font=FONT_PRIMARY)
        infra_label.move_to(RIGHT * 1.2 + UP * 1.0)
        self.play(GrowFromCenter(ped, run_time=0.28),
                  FadeIn(infra_label, run_time=0.22))

        # Vehicle localization error: vehicle thinks it's 1m further right
        veh_believed = veh_true.copy().set_fill(CYAN_NEON, opacity=0.25).set_stroke(RED_ALERT, width=1.0)
        veh_believed.shift(RIGHT * 1.0)
        err_label = Text("Vehicle believes it's HERE\n(1m localization error)",
                         font_size=SIZE_MICRO, color=RED_ALERT,
                         font=FONT_PRIMARY, line_spacing=0.38)
        err_label.next_to(veh_believed, DOWN, buff=0.10)
        self.play(GrowFromCenter(veh_believed, run_time=0.28),
                  FadeIn(err_label, run_time=0.22))

        # Result: vehicle plans path wrongly (too close to pedestrian)
        bad_path = DashedLine(veh_true.get_right(),
                              ped.get_center() + RIGHT * 0.8,
                              stroke_color=RED_ALERT, stroke_width=1.4,
                              stroke_opacity=0.70, dash_length=0.12)
        bad_result = Text("Near-miss risk!", font_size=SIZE_LABEL - 2,
                          color=RED_ALERT, font=FONT_PRIMARY, weight=BOLD)
        bad_result.move_to(UP * 2.3)
        self.play(Create(bad_path, run_time=0.40),
                  FadeIn(bad_result, scale=1.2, run_time=0.25))
        self.wait(0.5)

        # FIX: correct localization
        self.play(
            FadeOut(VGroup(veh_believed, err_label, bad_path, bad_result),
                    run_time=0.40),
        )
        safe_path = DashedLine(veh_true.get_right(),
                               ped.get_center() + RIGHT * 0.9 + DOWN * 0.5,
                               stroke_color=GREEN_SIGNAL, stroke_width=1.4,
                               stroke_opacity=0.80, dash_length=0.12)
        fix_label = Text("Precise localization → correct avoidance",
                         font_size=SIZE_LABEL - 2, color=GREEN_SIGNAL,
                         font=FONT_PRIMARY)
        fix_label.move_to(UP * 2.3)
        self.play(Create(safe_path, run_time=0.40),
                  FadeIn(fix_label, shift=DOWN * 0.06, run_time=0.25))
        self.wait(1.2)
        self.close()
