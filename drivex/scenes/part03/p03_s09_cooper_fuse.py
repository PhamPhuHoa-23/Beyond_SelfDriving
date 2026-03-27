"""
Scene 3-09 — CooperFuse: Late Fusion
=======================================
NMS (confidence-only) vs CooperFuse (temporal bbox features).
Rotated bounding box visualization showing orientation quality difference.
Paper: IV 2024.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P03S09CooperFuse(Scene):
    """
    Left panel  — NMS: picks highest confidence, ignores orientation
    Right panel — CooperFuse: temporal bbox features → better orientation
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("CooperFuse — Late Fusion", font_size=26,
                       color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        divider = Line(UP * 2.5, DOWN * 2.5,
                       color=COL_WHITE, stroke_opacity=0.3)
        self.play(Create(divider), run_time=0.2)

        # ═══════ LEFT: NMS ══════════════════════════════════════════
        nms_title = Text("NMS (baseline)", font_size=15,
                         color=COL_RED, weight=BOLD)
        nms_title.move_to(LEFT * 3.3 + UP * 2.0)

        # Two overlapping detections (different orientations)
        nms_bbox1 = Rectangle(width=1.4, height=0.55, stroke_color=COL_RED, stroke_width=2,
                              fill_opacity=0).rotate(PI / 8).move_to(LEFT * 3.5 + UP * 0.6)
        nms_bbox2 = Rectangle(width=1.4, height=0.55, stroke_color=COL_BLUE, stroke_width=2,
                              fill_opacity=0).rotate(-PI / 5).move_to(LEFT * 3.2 + UP * 0.3)

        conf1 = Text("conf=0.92", font_size=10, color=COL_RED)
        conf2 = Text("conf=0.78", font_size=10, color=COL_BLUE)
        conf1.next_to(nms_bbox1, UR, buff=0.08)
        conf2.next_to(nms_bbox2, DR, buff=0.08)

        # NMS keeps highest confidence — but orientation is bad
        cross_note = Text("Keeps CONF, ignores\norientation quality ✗", font_size=11,
                          color=COL_RED)
        cross_note.move_to(LEFT * 3.3 + DOWN * 1.4)

        self.play(FadeIn(nms_title), run_time=0.2)
        self.play(Create(nms_bbox1), FadeIn(conf1), run_time=0.25)
        self.play(Create(nms_bbox2), FadeIn(conf2), run_time=0.25)
        # Add rotation to show NMS picks wrong orientation
        self.play(Rotate(nms_bbox1, angle=PI / 6, about_point=nms_bbox1.get_center()),
                  run_time=0.5)
        self.play(nms_bbox2.animate.set_stroke(opacity=0.25),
                  # NMS suppresses it
                  conf2.animate.set_opacity(0.25), run_time=0.3)
        self.play(FadeIn(cross_note), run_time=0.3)

        # ═══════ RIGHT: CooperFuse ════════════════════════════════
        cf_title = Text("CooperFuse", font_size=15,
                        color=COL_GREEN, weight=BOLD)
        cf_title.move_to(RIGHT * 3.3 + UP * 2.0)

        # Well-aligned fused detection
        cf_bbox = Rectangle(width=1.4, height=0.55, stroke_color=COL_GREEN, stroke_width=2,
                            fill_opacity=0).rotate(PI / 10).move_to(RIGHT * 3.2 + UP * 0.5)

        feat_list = VGroup(
            Text("• Position history", font_size=11, color=COL_WHITE),
            Text("• Heading history", font_size=11, color=COL_WHITE),
            Text("• Size consistency", font_size=11, color=COL_WHITE),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        feat_list.move_to(RIGHT * 3.3 + DOWN * 0.6)

        check_note = Text("Temporal BBox features → better heading ✓", font_size=11,
                          color=COL_GREEN)
        check_note.move_to(RIGHT * 3.3 + DOWN * 1.9)

        self.play(FadeIn(cf_title), run_time=0.2)
        self.play(Create(cf_bbox), run_time=0.3)
        self.play(FadeIn(feat_list), run_time=0.3)
        self.play(FadeIn(check_note), run_time=0.3)

        # Paper badge
        paper_badge = RoundedRectangle(width=3.5, height=0.5, corner_radius=0.1,
                                       fill_color=COL_NAVY, fill_opacity=1, stroke_width=0)
        paper_txt = Text("CooperFuse  ·  IV 2024",
                         font_size=12, color=COL_WHITE)
        paper_badge.to_edge(DOWN, buff=0.4)
        paper_txt.move_to(paper_badge.get_center())
        self.play(FadeIn(VGroup(paper_badge, paper_txt)), run_time=0.3)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
