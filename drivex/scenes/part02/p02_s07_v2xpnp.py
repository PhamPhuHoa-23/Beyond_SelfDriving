"""
Scene 2-07 — V2XPnP: Research Problem 1
========================================
Three sub-scenes:
  A — What to Transmit (Early / Intermediate / Late fusion + N-frame badge)
  B — When to Transmit (cars meet, communication window, one-step strategy)
  C — How to Fuse      (Temporal Attention → Spatial Attention → outputs)
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


def _sep_flash(scene):
    """0.2s dark flash between sub-scenes."""
    overlay = Rectangle(width=16, height=9,
                        fill_color=BLACK, fill_opacity=1, stroke_width=0)
    overlay.move_to(ORIGIN)
    scene.play(FadeIn(overlay), run_time=0.1)
    scene.play(FadeOut(overlay), run_time=0.1)


class P02S07V2XPnP(Scene):
    """
    Sub-scene A: What to Transmit
    Sub-scene B: When to Transmit
    Sub-scene C: How to Fuse
    """

    # ─────────────────────── sub-scene A ───────────────────────────
    def _sub_a(self):
        header = Text("Q1: What to Transmit?", font_size=24, color=COL_GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header), run_time=0.4)

        def make_agent_box(label_txt, x):
            box = RoundedRectangle(width=2.8, height=1.5, corner_radius=0.15,
                                   fill_color="#1E3A5F", fill_opacity=1,
                                   stroke_color=COL_BLUE, stroke_width=2)
            lbl = Text(label_txt, font_size=18, color=COL_WHITE, weight=BOLD)
            box.move_to([x, 0, 0])
            lbl.move_to(box.get_center())
            return VGroup(box, lbl)

        a1 = make_agent_box("Agent 1", -4.5)
        a2 = make_agent_box("Agent 2",  4.5)
        self.play(FadeIn(a1), FadeIn(a2), run_time=0.5)

        rows = [
            ("Early Fusion:  Raw LiDAR",           COL_RED,     UP * 1.0),
            ("Intermediate:  BEV Features",          COL_BLUE,    ORIGIN),
            ("Late Fusion:   Bounding Boxes",        COL_GREEN,   DOWN * 1.0),
        ]
        for label_str, color, offset in rows:
            start = a1.get_right() + offset
            end   = a2.get_left()  + offset
            arrow = Arrow(start, end, color=color, buff=0.1, stroke_width=3)
            lbl   = Text(label_str, font_size=14, color=color)
            lbl.next_to(arrow, UP, buff=0.08)
            badge_box = RoundedRectangle(width=1.0, height=0.28, corner_radius=0.08,
                                         fill_color=COL_GOLD, fill_opacity=0.9, stroke_width=0)
            badge_txt = Text("+ N frames", font_size=10, color=BG_DARK)
            badge_box.next_to(arrow, DOWN, buff=0.05)
            badge_txt.move_to(badge_box.get_center())
            self.play(GrowArrow(arrow), FadeIn(lbl), run_time=0.4)
            self.play(FadeIn(VGroup(badge_box, badge_txt)), run_time=0.25)

        note = Text("Key: all three strategies include temporal dimension.",
                    font_size=15, color=COL_GOLD, slant=ITALIC)
        note.to_edge(DOWN, buff=0.6)
        self.play(Write(note), run_time=0.45)
        self.wait(1.2)
        self.play(FadeOut(VGroup(header, a1, a2, note)), run_time=0.3)
        self.clear()

    # ─────────────────────── sub-scene B ───────────────────────────
    def _sub_b(self):
        header = Text("Q2: When to Transmit?", font_size=24, color=COL_GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header), run_time=0.4)

        road = Line(LEFT * 7, RIGHT * 7, color=COL_WHITE, stroke_width=2)
        road.move_to(DOWN * 0.2)
        self.play(Create(road), run_time=0.4)

        def mini_car(color, pos):
            body   = RoundedRectangle(width=0.7, height=0.4, corner_radius=0.08,
                                      fill_color=color, fill_opacity=1, stroke_width=0)
            body.move_to(pos)
            return body

        car_a = mini_car(COL_BLUE,   LEFT * 5 + UP * 0.05)
        car_b = mini_car(COL_PURPLE, RIGHT * 5 + UP * 0.05)
        self.play(FadeIn(car_a), FadeIn(car_b), run_time=0.3)

        # cars converge toward centre
        self.play(
            car_a.animate.move_to(LEFT * 1.5 + UP * 0.05),
            car_b.animate.move_to(RIGHT * 1.5 + UP * 0.05),
            run_time=1.5
        )

        # communication window
        window = Rectangle(width=2.6, height=2.5,
                            fill_color=COL_GREEN, fill_opacity=0.18, stroke_width=0)
        window.move_to(ORIGIN + DOWN * 0.2 + UP * 0.5)
        win_lbl = Text("Only chance to communicate", font_size=14, color=COL_GREEN)
        win_lbl.next_to(window, UP, buff=0.15)
        self.play(FadeIn(window), FadeIn(win_lbl), run_time=0.4)

        # multi-step ✗ vs one-step ✓
        bad_box  = RoundedRectangle(width=4.0, height=1.2, corner_radius=0.12,
                                    fill_color="#2A1A1A", fill_opacity=1,
                                    stroke_color=COL_RED, stroke_width=2)
        bad_box.move_to(LEFT * 4 + DOWN * 2.0)
        bad_lbl  = Text("✗  Multi-step — agents may drive apart", font_size=14, color=COL_RED,
                        t2c={"✗": COL_RED})
        bad_lbl.move_to(bad_box.get_center())

        good_box = RoundedRectangle(width=4.0, height=1.2, corner_radius=0.12,
                                    fill_color="#1B4332", fill_opacity=1,
                                    stroke_color=COL_GREEN, stroke_width=2)
        good_box.move_to(RIGHT * 4 + DOWN * 2.0)
        good_lbl = Text("✓  One-step — transmit entire history at once",
                        font_size=13, color=COL_GREEN, t2c={"✓": COL_GREEN})
        good_lbl.move_to(good_box.get_center())

        comp_note = Text("Temporal attention compresses N frames → 1",
                         font_size=13, color=COL_LIGHT_BLUE, slant=ITALIC)
        comp_note.next_to(good_box, DOWN, buff=0.2)

        self.play(FadeIn(VGroup(bad_box, bad_lbl)), run_time=0.4)
        self.play(FadeIn(VGroup(good_box, good_lbl)), run_time=0.4)
        self.play(Write(comp_note), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.3)

    # ─────────────────────── sub-scene C ───────────────────────────
    def _sub_c(self):
        header = Text("Q3: How to Fuse?", font_size=24, color=COL_GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.4)
        self.play(FadeIn(header), run_time=0.4)

        y_center = DOWN * 0.3

        # N-frame stack (depth effect)
        frame_stack = VGroup(*[
            Rectangle(width=1.8, height=1.2,
                      fill_color=COL_NAVY, fill_opacity=0.9,
                      stroke_color=COL_BLUE, stroke_width=1.5)
            .shift(i * UR * 0.1)
            for i in range(4)
        ])
        frame_stack.move_to(LEFT * 5.5 + y_center)
        stack_lbl = Text("Agent history\n(N frames)", font_size=13, color=COL_LIGHT_BLUE)
        stack_lbl.next_to(frame_stack, DOWN, buff=0.2)
        self.play(FadeIn(VGroup(frame_stack, stack_lbl)), run_time=0.5)

        # Temporal Attention
        ta_box = RoundedRectangle(width=2.8, height=1.5, corner_radius=0.15,
                                   fill_color="#2D1B69", fill_opacity=1,
                                   stroke_color=COL_PURPLE, stroke_width=2)
        ta_lbl = Text("Temporal\nAttention", font_size=16, color=COL_WHITE)
        ta_box.move_to(LEFT * 2.0 + y_center)
        ta_lbl.move_to(ta_box.get_center())
        arr_to_ta = Arrow(frame_stack.get_right(), ta_box.get_left(),
                          color=COL_BLUE, buff=0.1)
        self.play(GrowArrow(arr_to_ta), FadeIn(VGroup(ta_box, ta_lbl)), run_time=0.5)

        # Per-agent temporal feature
        feat_box = Rectangle(width=1.8, height=1.0,
                              fill_color="#1E3A5F", fill_opacity=1,
                              stroke_color=COL_BLUE, stroke_width=1.5)
        feat_lbl = Text("Temporal\nfeature", font_size=13, color=COL_LIGHT_BLUE)
        feat_box.move_to(RIGHT * 1.0 + y_center)
        feat_lbl.move_to(feat_box.get_center())
        arr_ta_feat = Arrow(ta_box.get_right(), feat_box.get_left(),
                            color=COL_BLUE, buff=0.1)
        self.play(GrowArrow(arr_ta_feat), FadeIn(VGroup(feat_box, feat_lbl)), run_time=0.5)

        # Second agent converging
        feat_box2 = feat_box.copy().shift(DOWN * 1.5)
        lbl2      = Text("Agent 2\nfeature", font_size=13, color=COL_LIGHT_BLUE)
        lbl2.move_to(feat_box2.get_center())
        arr2 = Arrow(feat_box2.get_right(), feat_box2.get_right() + RIGHT * 1.2,
                     color=COL_GREEN, buff=0.05)
        self.play(FadeIn(VGroup(feat_box2, lbl2)), GrowArrow(arr2), run_time=0.5)

        # Spatial Attention
        sa_box = RoundedRectangle(width=2.8, height=1.5, corner_radius=0.15,
                                   fill_color="#1B4332", fill_opacity=1,
                                   stroke_color=COL_GREEN, stroke_width=2)
        sa_lbl = Text("Spatial\nAttention", font_size=16, color=COL_WHITE)
        sa_box.move_to(RIGHT * 3.5 + y_center + DOWN * 0.75)
        sa_lbl.move_to(sa_box.get_center())
        arr_feat_sa = Arrow(feat_box.get_right(), sa_box.get_left() + UP * 0.5,
                            color=COL_GREEN, buff=0.05)
        self.play(GrowArrow(arr_feat_sa), FadeIn(VGroup(sa_box, sa_lbl)), run_time=0.5)

        # Output representation
        out_box = RoundedRectangle(width=3.2, height=1.2, corner_radius=0.15,
                                    fill_color=COL_GOLD, fill_opacity=0.95, stroke_width=0)
        out_lbl = Text("Multi-Agent Spatio-\nTemporal Representation",
                       font_size=13, color=BG_DARK, weight=BOLD)
        out_box.move_to(RIGHT * 3.5 + UP * 2.0)
        out_lbl.move_to(out_box.get_center())
        arr_sa_out = Arrow(sa_box.get_top(), out_box.get_bottom(), color=COL_GOLD, buff=0.1)
        self.play(GrowArrow(arr_sa_out), FadeIn(VGroup(out_box, out_lbl)), run_time=0.5)

        # Fork to detection + prediction
        det_box = RoundedRectangle(width=2.0, height=0.8, corner_radius=0.1,
                                    fill_color="#1E3A5F", fill_opacity=1,
                                    stroke_color=COL_BLUE, stroke_width=1.5)
        pred_box = det_box.copy()
        det_lbl  = Text("Detection",  font_size=14, color=COL_WHITE)
        pred_lbl = Text("Prediction", font_size=14, color=COL_WHITE)
        det_box.move_to(RIGHT * 1.5 + UP * 2.5)
        pred_box.move_to(RIGHT * 5.5 + UP * 2.5)
        det_lbl.move_to(det_box.get_center())
        pred_lbl.move_to(pred_box.get_center())

        arr_det  = Arrow(out_box.get_left(),  det_box.get_right(),  color=COL_WHITE, buff=0.1)
        arr_pred = Arrow(out_box.get_right(), pred_box.get_left(),  color=COL_WHITE, buff=0.1)
        self.play(GrowArrow(arr_det),  FadeIn(VGroup(det_box, det_lbl)),  run_time=0.4)
        self.play(GrowArrow(arr_pred), FadeIn(VGroup(pred_box, pred_lbl)), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)

    # ─────────────────────── main construct ────────────────────────
    def construct(self):
        self.camera.background_color = BG_DARK
        self._sub_a()
        _sep_flash(self)
        self._sub_b()
        _sep_flash(self)
        self._sub_c()
