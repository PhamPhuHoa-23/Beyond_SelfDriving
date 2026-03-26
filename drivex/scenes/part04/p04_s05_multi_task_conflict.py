"""
Scene 4-05 — Training Bottleneck: Multi-Task Conflict
=======================================================
Section A — Architecture complexity (single-frame → multi-frame/task).
Section B — Orange dot scatter (one-time training failures).
Section C — Gradient conflict 3-direction diagram.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P04S05MultiTaskConflict(Scene):
    """
    A — Simple → complex architecture arrow
    B — Scatter plot: orange failure dots (one-time training)
    C — 3 gradient arrows pulling model node in different directions
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("Training Bottleneck: Multi-Task Conflict", font_size=20,
                        color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ SECTION A — Architecture ══════════════════════════════
        def simple_box(label, color, pos):
            b = RoundedRectangle(width=1.8, height=0.55, corner_radius=0.12,
                                  fill_color=color, fill_opacity=0.25,
                                  stroke_color=color, stroke_width=1.5)
            t = Text(label, font_size=11, color=color)
            b.move_to(pos); t.move_to(b)
            return VGroup(b, t)

        s_frame = simple_box("Single-frame\n1 agent · 1 task", COL_BLUE, LEFT * 3.5 + UP * 0.8)
        m_frame = simple_box("Multi-frame + Multi-agent\n+ Multi-task", COL_RED,  RIGHT * 2.0 + UP * 0.8)
        ext_arr = Arrow(s_frame.get_right(), m_frame.get_left(), buff=0.1,
                         color=COL_WHITE, stroke_width=2, tip_length=0.14)
        ext_lbl = Text("extend →", font_size=11, color=COL_WHITE)
        ext_lbl.next_to(ext_arr, UP, buff=0.06)
        complex_lbl = Text("Many dimensions at once", font_size=14, color=COL_RED, slant=ITALIC)
        complex_lbl.next_to(m_frame, DOWN, buff=0.18)

        self.play(FadeIn(s_frame), run_time=0.3)
        self.play(Create(ext_arr), FadeIn(ext_lbl), run_time=0.3)
        self.play(FadeIn(m_frame), Write(complex_lbl), run_time=0.4)
        self.wait(0.4)

        # ═══ SECTION B — Scatter plot ═════════════════════════════
        self.play(FadeOut(VGroup(s_frame, m_frame, ext_arr, ext_lbl, complex_lbl)),
                  run_time=0.3)

        axes = Axes(
            x_range=[0, 1, 0.25], y_range=[0, 1, 0.25],
            x_length=4.5, y_length=3.5,
            axis_config={"color": COL_WHITE, "stroke_width": 1.5,
                          "include_numbers": False, "numbers_to_exclude": []},
            tips=False,
        ).shift(LEFT * 0.5 + DOWN * 0.4)
        ax_xlbl = Text("AP@0.5", font_size=11, color=COL_WHITE)
        ax_xlbl.next_to(axes.x_axis, DOWN, buff=0.15)
        ax_ylbl = Text("EPA", font_size=11, color=COL_WHITE).rotate(PI / 2)
        ax_ylbl.next_to(axes.y_axis, LEFT, buff=0.2)

        self.play(Create(axes), FadeIn(ax_xlbl), FadeIn(ax_ylbl), run_time=0.4)

        # Orange failure dots (low-left cluster)
        fail_positions = [
            [0.12, 0.10], [0.18, 0.08], [0.08, 0.14], [0.22, 0.12],
            [0.14, 0.07], [0.10, 0.18], [0.20, 0.16], [0.16, 0.09],
        ]
        fail_zone = Polygon(
            axes.c2p(0.05, 0.04), axes.c2p(0.28, 0.04),
            axes.c2p(0.28, 0.22), axes.c2p(0.05, 0.22),
            fill_color="#E67E22", fill_opacity=0.08, stroke_width=0
        )
        self.play(FadeIn(fail_zone), run_time=0.3)

        for px, py in fail_positions:
            d = Dot(axes.c2p(px, py), radius=0.09, color="#E67E22")
            self.play(FadeIn(d), run_time=0.08)

        fail_lbl = Text("One-time training: strong models fail", font_size=12,
                         color="#E67E22", slant=ITALIC)
        fail_lbl.move_to(RIGHT * 3.2 + UP * 0.2)
        self.play(Write(fail_lbl), run_time=0.3)
        self.wait(0.5)

        # ═══ SECTION C — Gradient conflict ════════════════════════
        self.play(FadeOut(Group(axes, ax_xlbl, ax_ylbl, fail_zone, fail_lbl,
                                *self.mobjects)), run_time=0.3)

        model_circ = Circle(radius=0.45, fill_color="#1E3A5F", fill_opacity=1,
                              stroke_color=COL_BLUE, stroke_width=2)
        model_lbl  = Text("Model", font_size=14, color=COL_WHITE, weight=BOLD)
        model_circ.move_to(ORIGIN + DOWN * 0.3)
        model_lbl.move_to(model_circ.get_center())

        # 3 gradient arrows ~120° apart
        angles  = [PI / 2, PI / 2 + 2 * PI / 3, PI / 2 + 4 * PI / 3]
        g_colors = [COL_BLUE, COL_GREEN, COL_PURPLE]
        g_labels = ["Detect", "Predict", "Plan"]
        grad_arrows = []
        grad_labels = []
        for ang, col, lbl in zip(angles, g_colors, g_labels):
            tip = model_circ.get_center() + 1.6 * np.array([np.cos(ang), np.sin(ang), 0])
            arr = Arrow(model_circ.get_center(), tip, buff=0.45,
                         color=col, stroke_width=2.5, tip_length=0.16)
            t = Text(lbl, font_size=12, color=col, weight=BOLD)
            t.move_to(tip + 0.35 * np.array([np.cos(ang), np.sin(ang), 0]))
            grad_arrows.append(arr)
            grad_labels.append(t)

        self.play(FadeIn(model_circ), FadeIn(model_lbl), run_time=0.3)
        for arr, lbl in zip(grad_arrows, grad_labels):
            self.play(GrowArrow(arr), FadeIn(lbl), run_time=0.35)

        # Conflict pulse
        self.play(model_circ.animate.set_stroke(color=COL_RED, width=5), run_time=0.25)
        self.play(model_circ.animate.set_stroke(color=COL_BLUE, width=2), run_time=0.25)

        conflict_lbl = Text("Gradients pull model in different directions",
                             font_size=13, color=COL_WHITE)
        conflict_note = Text("Improve Detection → Prediction may degrade  ✗",
                              font_size=12, color=COL_RED, slant=ITALIC)
        conflict_lbl.to_edge(DOWN, buff=1.0)
        conflict_note.next_to(conflict_lbl, DOWN, buff=0.12)
        self.play(Write(conflict_lbl), Write(conflict_note), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
