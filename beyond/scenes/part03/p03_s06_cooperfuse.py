# beyond/scenes/part03/p03_s06_cooperfuse.py — CooperFuse late fusion
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, glow_pulse,
    P3_SIM, CYAN_NEON, ORANGE_INFRA, GREEN_SIGNAL, RED_ALERT,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P03S06CooperFuse(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("CooperFuse — Uncertainty-Aware Late Fusion")
        self.wait(0.2)

        # Two bounding boxes from different sensors
        box_v = Rectangle(width=1.2, height=0.7, fill_color=CYAN_NEON,
                          fill_opacity=0.20, stroke_color=CYAN_NEON, stroke_width=1.8)
        box_v.move_to(LEFT * 1.8 + UP * 0.5)
        lbl_v = Text("Vehicle box", font_size=SIZE_MICRO + 1,
                     color=CYAN_NEON, font=FONT_PRIMARY)
        lbl_v.next_to(box_v, UP, buff=0.10)

        box_i = Rectangle(width=1.2, height=0.7, fill_color=ORANGE_INFRA,
                          fill_opacity=0.20, stroke_color=ORANGE_INFRA, stroke_width=1.8)
        box_i.move_to(RIGHT * 0.4 + UP * 0.5)
        lbl_i = Text("Infrastructure box", font_size=SIZE_MICRO + 1,
                     color=ORANGE_INFRA, font=FONT_PRIMARY)
        lbl_i.next_to(box_i, DOWN, buff=0.10)

        self.play(GrowFromCenter(box_v), GrowFromCenter(box_i),
                  FadeIn(lbl_v), FadeIn(lbl_i), run_time=0.40)
        self.wait(0.3)

        # NMS approach (old): pick one, discard other
        old_lbl = Text("Old: NMS — pick higher confidence, discard other",
                       font_size=SIZE_MICRO + 1, color=RED_ALERT, font=FONT_PRIMARY)
        old_lbl.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(old_lbl, shift=UP * 0.06, run_time=0.25))
        # X over discarded box
        x_mark = Text("✗", font_size=48, color=RED_ALERT, font=FONT_PRIMARY)
        x_mark.move_to(box_i.get_center())
        self.play(FadeIn(x_mark, scale=1.5, run_time=0.18),
                  box_i.animate(run_time=0.20).set_fill(opacity=0.05)
                       .set_stroke(opacity=0.25))
        self.wait(0.5)
        self.play(FadeOut(x_mark, run_time=0.20),
                  box_i.animate(run_time=0.20).set_fill(opacity=0.20)
                       .set_stroke(opacity=1.0),
                  FadeOut(old_lbl, run_time=0.20))

        # CooperFuse: uncertainty ellipses
        unc_v = Ellipse(width=1.8, height=1.1, fill_color=CYAN_NEON,
                        fill_opacity=0.08, stroke_color=CYAN_NEON,
                        stroke_width=0.8, stroke_opacity=0.5)
        unc_v.move_to(box_v.get_center())
        unc_i = Ellipse(width=1.2, height=0.75, fill_color=ORANGE_INFRA,
                        fill_opacity=0.10, stroke_color=ORANGE_INFRA,
                        stroke_width=0.8, stroke_opacity=0.5)
        unc_i.move_to(box_i.get_center())

        unc_lbl_v = Text("large uncertainty\n(vehicle moving)", font_size=SIZE_MICRO - 1,
                         color=CYAN_NEON, font=FONT_PRIMARY, line_spacing=0.38)
        unc_lbl_v.next_to(unc_v, DOWN, buff=0.10)
        unc_lbl_i = Text("small uncertainty\n(infra fixed)", font_size=SIZE_MICRO - 1,
                         color=ORANGE_INFRA, font=FONT_PRIMARY, line_spacing=0.38)
        unc_lbl_i.next_to(unc_i, UP, buff=0.10)

        new_lbl = Text("CooperFuse: uncertainty-weighted fusion",
                       font_size=SIZE_MICRO + 2, color=P3_SIM,
                       font=FONT_PRIMARY, weight=BOLD)
        new_lbl.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(new_lbl, shift=UP * 0.06, run_time=0.25))
        self.play(
            FadeIn(unc_v, run_time=0.35), FadeIn(unc_i, run_time=0.30),
            FadeIn(unc_lbl_v, run_time=0.22), FadeIn(unc_lbl_i, run_time=0.22),
        )
        self.wait(0.4)

        # Fused result crystallizes between the two boxes
        fused_box = Rectangle(width=1.0, height=0.60,
                              fill_color=GREEN_SIGNAL, fill_opacity=0.35,
                              stroke_color=GREEN_SIGNAL, stroke_width=2.2)
        fused_box.move_to(LEFT * 0.7 + UP * 0.5)
        fused_lbl = Text("Fused — smaller,\nmore accurate", font_size=SIZE_MICRO,
                         color=GREEN_SIGNAL, font=FONT_PRIMARY, line_spacing=0.38)
        fused_lbl.next_to(fused_box, UP, buff=0.10)

        self.play(GrowFromCenter(fused_box, run_time=0.40),
                  FadeIn(fused_lbl, run_time=0.25))
        self.play(glow_pulse(fused_box, GREEN_SIGNAL, n_pulses=1, run_time=0.40))
        self.wait(1.2)

        self.close()
