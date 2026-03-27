"""
Scene 2-10 — RiskMap: Research Problem 3
==========================================
Three-row diagram: (a) Modular, (b) Conventional E2E, (c) RiskMap.
RiskMap splits prediction ("Where dangerous?") from planning ("What path?").
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P02S10RiskMap(Scene):
    """
    Three-row paradigm comparison centred on RiskMap as interpretable middleware.
    """

    def _make_row(self, boxes_data, y):
        """
        boxes_data: list of (label, fill_color, stroke_color)
        Returns VGroup of boxes + arrows + all labels, anchored at y.
        """
        items = VGroup()
        arrows = VGroup()
        box_objs = []
        for label, fill, stroke in boxes_data:
            box = RoundedRectangle(width=2.2, height=0.85, corner_radius=0.1,
                                   fill_color=fill, fill_opacity=1,
                                   stroke_color=stroke, stroke_width=1.8)
            txt = Text(label, font_size=12, color=COL_WHITE)
            txt.move_to(box.get_center())
            items.add(VGroup(box, txt))
            box_objs.append(box)

        items.arrange(RIGHT, buff=0.6)
        items.move_to([0, y, 0])

        for i in range(len(box_objs) - 1):
            a = Arrow(items[i].get_right(), items[i + 1].get_left(),
                      color=COL_BLUE, buff=0.05, max_tip_length_to_length_ratio=0.25,
                      stroke_width=2)
            arrows.add(a)

        return VGroup(items, arrows)

    def construct(self):
        self.camera.background_color = BG_BLACK

        header = Text("Three Planning Paradigms", font_size=24,
                      color=COL_GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header), run_time=0.3)

        # ── Row (a) Modular ────────────────────────────────────────
        lbl_a = Text("(a) Modular", font_size=16, color=COL_WHITE)
        lbl_a.move_to(LEFT * 6.0 + UP * 2.2)
        row_a = self._make_row([
            ("Detect",   "#1E3A5F", COL_BLUE),
            ("Predict",  "#1E3A5F", COL_BLUE),
            ("Plan",     "#1E3A5F", COL_BLUE),
            ("Control",  "#1E3A5F", COL_BLUE),
        ], y=2.2)
        badge_a = Text("✗  Error accumulation", font_size=13, color=COL_RED,
                       t2c={"✗": COL_RED})
        badge_a.next_to(row_a, RIGHT, buff=0.25)
        self.play(FadeIn(lbl_a), FadeIn(row_a), FadeIn(badge_a), run_time=0.6)

        # ── Row (b) Conventional E2E ───────────────────────────────
        lbl_b = Text("(b) Conv. E2E", font_size=16, color=COL_WHITE)
        lbl_b.move_to(LEFT * 6.0 + UP * 0.4)
        row_b = self._make_row([
            ("Sensors",   "#1E3A5F", COL_BLUE),
            ("Black Box", "#111111", COL_RED),
            ("Action",    "#1B4332", COL_GREEN),
        ], y=0.4)
        badge_b = Text("✗  Safety verification impossible", font_size=13, color=COL_RED,
                       t2c={"✗": COL_RED})
        badge_b.next_to(row_b, RIGHT, buff=0.2)
        self.play(FadeIn(lbl_b), FadeIn(row_b), FadeIn(badge_b), run_time=0.6)

        self.wait(0.8)

        # ── Row (c) RiskMap ────────────────────────────────────────
        lbl_c = Text("(c) RiskMap", font_size=18, color=COL_GOLD, weight=BOLD)
        lbl_c.move_to(LEFT * 6.0 + DOWN * 1.6)

        # Build the RiskMap row manually for the special GOLD box
        sx_start = -4.5

        def _box(label, fill, stroke, x, y):
            box = RoundedRectangle(width=2.4, height=0.95, corner_radius=0.12,
                                   fill_color=fill, fill_opacity=1,
                                   stroke_color=stroke, stroke_width=2)
            txt = Text(label, font_size=13, color=COL_WHITE if fill != COL_GOLD else BG_DARK,
                       weight=BOLD if fill == COL_GOLD else NORMAL)
            box.move_to([x, y, 0])
            txt.move_to(box.get_center())
            return VGroup(box, txt)

        rm_y = -1.6
        b_sensors = _box("Multi-Agent\nSensors",
                         "#1E3A5F", COL_BLUE,   -4.8, rm_y)
        b_riskmap = _box("Risk Map\n(spatiotemporal)",
                         "#3D1A00", COL_GOLD, -1.8, rm_y)
        b_mpc = _box("Learning-based\nMPC", "#1B4332", COL_GREEN,    1.0, rm_y)
        b_traj = _box("Safe Trajectory", COL_GREEN,
                      COL_GREEN,         3.7, rm_y)

        arr_sr = Arrow(b_sensors.get_right(),
                       b_riskmap.get_left(), color=COL_BLUE,  buff=0.05)
        arr_rm = Arrow(b_riskmap.get_right(), b_mpc.get_left(),
                       color=COL_GOLD,  buff=0.05)
        arr_mt = Arrow(b_mpc.get_right(),     b_traj.get_left(),
                       color=COL_GREEN, buff=0.05)

        badge_c = Text("✓  Interpretable + Safe", font_size=13, color=COL_GREEN,
                       t2c={"✓": COL_GREEN})
        badge_c.next_to(b_traj, RIGHT, buff=0.2)

        # Annotations
        ann1 = Text("\"Where dangerous?\"", font_size=12,
                    color=COL_LIGHT_BLUE, slant=ITALIC)
        ann2 = Text("\"What path?\"",        font_size=12,
                    color=COL_GREEN,      slant=ITALIC)
        ann1.next_to(b_riskmap, DOWN, buff=0.2)
        ann2.next_to(b_mpc,     DOWN, buff=0.2)

        self.play(Write(lbl_c), run_time=0.4)
        self.play(FadeIn(b_sensors), GrowArrow(arr_sr), run_time=0.4)
        self.play(FadeIn(b_riskmap), run_time=0.5)
        self.play(GrowArrow(arr_rm), FadeIn(b_mpc), run_time=0.4)
        self.play(GrowArrow(arr_mt), FadeIn(b_traj),
                  FadeIn(badge_c), run_time=0.4)
        self.play(FadeIn(ann1), FadeIn(ann2), run_time=0.4)

        # ── result bar ─────────────────────────────────────────────
        result_box = RoundedRectangle(width=9.0, height=0.75, corner_radius=0.12,
                                      fill_color="#1B4332", fill_opacity=1,
                                      stroke_color=COL_GREEN, stroke_width=2)
        result_lbl = Text(
            "Best on Detection + Prediction + Planning simultaneously",
            font_size=15, color=COL_GREEN
        )
        result_box.to_edge(DOWN, buff=0.25)
        result_lbl.move_to(result_box.get_center())
        self.play(FadeIn(result_box), Write(result_lbl), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
