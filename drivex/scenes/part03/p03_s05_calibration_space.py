"""
Scene 3-05 — Space Calibration
================================
4 coordinate frames → misaligned point cloud → ghost object →
Transform animation (snap to correct) + PJLab badge.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P03S05CalibrationSpace(Scene):
    """
    A — 4 coordinate frames (Camera / LiDAR / Vehicle / World)
    B — Misaligned point cloud → ghost object
    C — Transform to aligned + PJLab SensorsCalibration badge
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("Space Calibration", font_size=28, color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.5)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ SECTION A: 4 Coordinate Frames ════════════════════════
        frames_info = [
            ("Camera",  COL_SENSOR_CYAN, LEFT * 4.5 + UP * 1.0),
            ("LiDAR",   COL_INFRA_ORANGE, LEFT * 1.5 + UP * 1.0),
            ("Vehicle", COL_BLUE,        RIGHT * 1.5 + UP * 1.0),
            ("World",   COL_GREEN,       RIGHT * 4.5 + UP * 1.0),
        ]

        frame_groups = []
        for name, color, pos in frames_info:
            ax_x = Arrow(ORIGIN, RIGHT * 0.5, buff=0, color=color, stroke_width=2, tip_length=0.12)
            ax_y = Arrow(ORIGIN, UP    * 0.5, buff=0, color=color, stroke_width=2, tip_length=0.12)
            lbl  = Text(name, font_size=12, color=color)
            lbl.next_to(VGroup(ax_x, ax_y), DOWN, buff=0.12)
            grp  = VGroup(ax_x, ax_y, lbl).move_to(pos)
            frame_groups.append(grp)

        arrows_tf = []
        for i in range(len(frame_groups) - 1):
            src = frame_groups[i].get_right()
            dst = frame_groups[i+1].get_left()
            mid_src = np.array([src[0], frames_info[i][2][1], 0])
            mid_dst = np.array([dst[0], frames_info[i+1][2][1], 0])
            arr = Arrow(mid_src, mid_dst, buff=0.08, color=COL_WHITE,
                         stroke_width=1.5, tip_length=0.12)
            arrows_tf.append(arr)

        self.play(*[FadeIn(g) for g in frame_groups], run_time=0.5)
        self.play(*[Create(a) for a in arrows_tf], run_time=0.4)
        self.wait(0.5)

        # ═══ SECTION B: Misaligned point cloud ══════════════════════
        misalign_title = Text("Without calibration", font_size=16, color=COL_RED)
        misalign_title.move_to(DOWN * 0.1)
        self.play(FadeIn(misalign_title), run_time=0.3)

        # True object (green)
        obj_true = Circle(radius=0.25, fill_color=COL_GREEN, fill_opacity=0.9, stroke_width=0)
        obj_true.move_to(LEFT * 1.0 + DOWN * 1.2)
        lbl_true = Text("True", font_size=11, color=COL_GREEN)
        lbl_true.next_to(obj_true, DOWN, buff=0.08)

        # Ghost object (red, offset due to miscalibration)
        obj_ghost = Circle(radius=0.25, fill_color=COL_RED, fill_opacity=0.6, stroke_width=0)
        obj_ghost.move_to(LEFT * 1.0 + DOWN * 1.2 + RIGHT * 0.9 + UP * 0.4)
        lbl_ghost = Text("Ghost (LiDAR offset)", font_size=11, color=COL_RED)
        lbl_ghost.next_to(obj_ghost, UR, buff=0.08)

        self.play(FadeIn(obj_true), FadeIn(lbl_true),
                  FadeIn(obj_ghost), FadeIn(lbl_ghost), run_time=0.4)
        self.wait(0.5)

        # ═══ SECTION C: Calibration → Aligned ═══════════════════════
        self.play(
            Transform(obj_ghost, obj_true.copy()),
            lbl_ghost.animate.become(
                Text("Aligned  ✓", font_size=11, color=COL_GREEN)
                .next_to(obj_true.copy(), DOWN, buff=0.08)
            ),
            run_time=0.8
        )
        self.wait(0.3)

        badge = RoundedRectangle(width=3.8, height=0.55, corner_radius=0.12,
                                  fill_color=COL_NAVY, fill_opacity=1, stroke_color=COL_INFRA_ORANGE,
                                  stroke_width=1.5)
        badge_txt = Text("PJLab SensorsCalibration  (open-source)", font_size=12, color=COL_WHITE)
        badge.to_corner(DR, buff=0.4)
        badge_txt.move_to(badge.get_center())

        self.play(FadeIn(VGroup(badge, badge_txt)), run_time=0.4)
        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
