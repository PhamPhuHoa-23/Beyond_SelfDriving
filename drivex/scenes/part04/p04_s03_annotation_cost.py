"""
Scene 4-03 — Data Bottleneck: Annotation Cost Problem
=======================================================
Bar chart showing dataset growth (V2V4Real / DAIR-V2X / V2X-Real) +
parallel cost bars + annotation complexity bullets + key question box.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P04S03AnnotationCost(Scene):
    """
    A — Grouped bar chart: dataset scale (blue) vs annotation cost (red)
    B — Annotation complexity bullets
    C — Key question box
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("Data Bottleneck: Annotation Cost", font_size=22, color=COL_GOLD,
                        weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ Bar chart ════════════════════════════════════════════
        datasets = [("V2V4Real\n240K", 2.0), ("DAIR-V2X\n460K", 3.84), ("V2X-Real\n1.2M", 10.0)]
        bar_width = 0.55
        spacing   = 2.2
        origin    = LEFT * 3.5 + DOWN * 0.2

        data_bars = []
        cost_bars = []
        for i, (name, height) in enumerate(datasets):
            x = origin[0] + i * spacing

            # Dataset bar (blue, scale)
            db = Rectangle(width=bar_width, height=height * 0.28,
                            fill_color=COL_BLUE, fill_opacity=1, stroke_width=0)
            db.move_to([x, origin[1] + db.height / 2, 0])

            # Cost bar (red, same height — key point)
            cb = Rectangle(width=bar_width, height=height * 0.28,
                            fill_color=COL_RED, fill_opacity=0.85, stroke_width=0)
            cb.move_to([x + bar_width + 0.08, origin[1] + cb.height / 2, 0])

            lbl = Text(name, font_size=10, color=COL_WHITE)
            lbl.next_to(VGroup(db, cb), DOWN, buff=0.1)

            data_bars.append(VGroup(db, lbl))
            cost_bars.append(cb)

        # Legend
        leg_d = VGroup(Square(side_length=0.16, fill_color=COL_BLUE, fill_opacity=1,
                               stroke_width=0),
                        Text("Dataset size", font_size=11, color=COL_BLUE)).arrange(RIGHT, buff=0.1)
        leg_c = VGroup(Square(side_length=0.16, fill_color=COL_RED, fill_opacity=1,
                               stroke_width=0),
                        Text("Annotation cost", font_size=11, color=COL_RED)).arrange(RIGHT, buff=0.1)
        legend = VGroup(leg_d, leg_c).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        legend.to_corner(UL, buff=1.5).shift(DOWN * 0.8)

        # Axis baseline
        ax_base = Line(origin + LEFT * 0.3, origin + RIGHT * 6.2,
                        color=COL_WHITE, stroke_width=1.5)

        self.play(FadeIn(ax_base), run_time=0.2)

        # Grow bars staggered
        for i, (dg, cb) in enumerate(zip(data_bars, cost_bars)):
            db = dg[0]
            # Animate from zero height
            db_start = db.copy().stretch_to_fit_height(0.01).align_to(ax_base, DOWN)
            cb_start = cb.copy().stretch_to_fit_height(0.01).align_to(ax_base, DOWN)
            self.play(
                Transform(db_start, db),
                Transform(cb_start, cb),
                FadeIn(dg[1]),
                run_time=0.4, rate_func=smooth
            )
            data_bars[i] = VGroup(db_start, dg[1])
            cost_bars[i] = cb_start

        # 5× label
        five_x = Text("5× in 2 years", font_size=17, color=COL_GOLD, weight=BOLD)
        five_x.move_to(RIGHT * 1.0 + UP * 1.8)
        self.play(Write(five_x), run_time=0.3)

        # "Cost grows same rate" label
        cost_lbl = Text("Annotation cost ↑ same rate", font_size=14, color=COL_RED)
        cost_lbl.next_to(five_x, DOWN, buff=0.2)
        self.play(FadeIn(cost_lbl), run_time=0.3)
        self.play(FadeIn(legend), run_time=0.2)
        self.wait(0.3)

        # ═══ Annotation complexity bullets ════════════════════════
        bullets_info = [
            "Specialized 3D LiDAR toolkit",
            "Trained point-cloud annotators",
            "Multi-layer quality checking",
        ]
        bullets = VGroup(*[
            Text(f"• {b}", font_size=13, color=COL_WHITE) for b in bullets_info
        ]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        bullets.move_to(RIGHT * 3.2 + UP * 0.3)

        self.play(FadeIn(bullets), run_time=0.4)
        self.wait(0.3)

        # ═══ Key question box ══════════════════════════════════════
        q_bg  = RoundedRectangle(width=7.0, height=0.65, corner_radius=0.15,
                                  fill_color="#2A1A1A", fill_opacity=1,
                                  stroke_color=COL_RED, stroke_width=2)
        q_txt = Text("How do you make a model learn well with limited labels?",
                      font_size=14, color=COL_RED, weight=BOLD)
        q_bg.to_edge(DOWN, buff=0.5)
        q_txt.move_to(q_bg.get_center())
        self.play(FadeIn(VGroup(q_bg, q_txt)), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
