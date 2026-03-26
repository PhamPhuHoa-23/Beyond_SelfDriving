"""
Scene 3-12 — CDA-SimBoost
============================
5-step circular pipeline + edge cases + long-tail distribution.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P03S12SimBoost(Scene):
    """
    A — 5-step circular loop (Import → Twin → Scenarios → Train → Validate)
    B — Edge case scenario labels (rain, pedestrian, sensor failure)
    C — Long-tail distribution: simulation fills green tail
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("CDA-SimBoost", font_size=28, color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ SECTION A: Circular Loop ═════════════════════════════
        steps = [
            ("Import\nReal Data",    COL_BLUE),
            ("Digital\nTwin",        COL_PURPLE),
            ("Generate\nScenarios",  COL_INFRA_ORANGE),
            ("Train",                COL_GREEN),
            ("Validate",             COL_SENSOR_CYAN),
        ]
        n     = len(steps)
        R     = 1.7   # circle radius
        angs  = [PI / 2 + 2 * PI * i / n for i in range(n)]   # spread around circle
        nodes = []

        for (label, color), ang in zip(steps, angs):
            pos  = R * np.array([np.cos(ang), np.sin(ang), 0]) + LEFT * 2.0
            box  = RoundedRectangle(width=1.5, height=0.6, corner_radius=0.15,
                                     fill_color=color, fill_opacity=0.9, stroke_width=0)
            box.move_to(pos)
            txt  = Text(label, font_size=11, color=COL_WHITE, weight=BOLD)
            txt.move_to(box.get_center())
            nodes.append(VGroup(box, txt))

        self.play(*[FadeIn(n_) for n_ in nodes], run_time=0.5)

        # Curved arrows between consecutive nodes
        for i in range(n):
            src = nodes[i].get_center()
            dst = nodes[(i + 1) % n].get_center()
            arc = CurvedArrow(src, dst, angle=-PI / 4, color=COL_WHITE,
                               stroke_width=1.5, tip_length=0.12)
            self.play(Create(arc), run_time=0.18)

        self.wait(0.4)

        # ═══ SECTION B: Edge cases ════════════════════════════════
        edge_cases = ["Heavy rain", "Sudden pedestrian", "Sensor failure"]
        edge_grp = VGroup(*[
            Text(f"• {e}", font_size=12, color=COL_RED)
            for e in edge_cases
        ]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        edge_grp.move_to(RIGHT * 3.5 + UP * 0.6)
        edge_hdr = Text("Edge cases simulated:", font_size=13, color=COL_WHITE)
        edge_hdr.next_to(edge_grp, UP, buff=0.15)

        self.play(FadeIn(edge_hdr), FadeIn(edge_grp), run_time=0.4)
        self.wait(0.3)

        # ═══ SECTION C: Long-tail distribution ════════════════════
        ax = Axes(
            x_range=[0, 6, 1], y_range=[0, 1.2, 0.5],
            x_length=3.5, y_length=1.8,
            axis_config={"color": COL_WHITE, "stroke_width": 1.5},
            tips=False,
        ).move_to(RIGHT * 3.5 + DOWN * 1.8)

        # Main distribution (blue)
        main_curve = ax.plot(lambda x: np.exp(-0.8 * x) * 1.0, x_range=[0, 5.5],
                              color=COL_BLUE, stroke_width=2)
        # Simulation fills the tail (green fill)
        tail_fill = ax.get_area(main_curve, x_range=[3, 5.5], color=COL_GREEN, opacity=0.5)

        dist_lbl  = Text("Simulation fills\nlong tail", font_size=10, color=COL_GREEN)
        dist_lbl.next_to(ax, DOWN, buff=0.1)

        self.play(Create(main_curve), run_time=0.4)
        self.play(FadeIn(tail_fill), FadeIn(dist_lbl), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
