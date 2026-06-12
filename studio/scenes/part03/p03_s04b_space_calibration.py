"""P03-S04b Space Calibration: matrix fly-in + point cloud merge."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER, RED_ERROR, PURPLE_MODEL, GOLD_RICH,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, h_arrow,
)
SCRIPT = """Space calibration is the transform from one sensor frame into a common one."""


def point_cloud_mob(center, n=16, color=ACCENT_BLUE, spread=0.55, seed=42):
    """Local helper — Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/vector_space_scene.py:204"""
    rng = np.random.RandomState(seed)
    pts = VGroup()
    for _ in range(n):
        dx, dy = rng.uniform(-spread, spread, 2)
        d = Dot(radius=0.055)
        d.set_fill(color, opacity=1.0)
        d.set_stroke(width=0)
        d.move_to(center + np.array([dx, dy, 0]))
        pts.add(d)
    return pts


class P03S04BSpaceCalibration(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Space Calibration"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # Two-row funnel: [Vehicle / Infra] → [Transform T] → [Common frame]
        cloud_v = point_cloud_mob(LEFT * 4.5 + UP * 1.0, color=ACCENT_BLUE, seed=1)
        cloud_i = point_cloud_mob(LEFT * 4.5 + DOWN * 1.0, color=ACCENT_GREEN, seed=5)
        lbl_v = Text("Vehicle frame", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_BLUE)
        lbl_v.next_to(cloud_v, DOWN, buff=0.12)
        lbl_i = Text("Infra frame", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_GREEN)
        lbl_i.next_to(cloud_i, DOWN, buff=0.12)

        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in cloud_v), lag_ratio=0.04, run_time=1.0))
        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in cloud_i), lag_ratio=0.04, run_time=1.0))
        self.play(FadeIn(lbl_v), FadeIn(lbl_i))

        # Transform matrix flies in from top
        # Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/vector_space_scene.py:204
        mat_entries = [["R", "t"], ["0", "1"]]
        mat = Matrix(mat_entries, h_buff=1.2, v_buff=0.8)
        mat.set_column_colors(PURPLE_MODEL, GOLD_RICH)
        mat.get_brackets().set_color(PURPLE_MODEL)
        mat.get_brackets().set_stroke(PURPLE_MODEL, width=2.4, opacity=0.95)
        mat_lbl = Text("Spatial Transform T", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=PURPLE_MODEL, weight=BOLD)
        mat.move_to(ORIGIN)
        mat_lbl.next_to(mat, UP, buff=0.26)
        mat_panel = RoundedRectangle(
            width=mat.get_width() + 0.42,
            height=mat.get_height() + 0.36,
            corner_radius=0.12,
            fill_color=BG_PAPER,
            fill_opacity=0.96,
            stroke_color=PURPLE_MODEL,
            stroke_width=1.4,
            stroke_opacity=0.28,
        )
        mat_panel.move_to(mat)
        mat_panel.set_z_index(-1)
        self.play(FadeIn(mat_panel, shift=DOWN * 1.5, run_time=0.8), FadeIn(mat, shift=DOWN * 1.5, run_time=0.8), FadeIn(mat_lbl))

        # Diagonal arrows from each cloud into matrix left edge
        arr_v = Arrow(
            cloud_v.get_right() + RIGHT * 0.05,
            mat.get_left() + UP * 0.25,
            color=PURPLE_MODEL, stroke_width=2.5, buff=0.0,
        )
        arr_i = Arrow(
            cloud_i.get_right() + RIGHT * 0.05,
            mat.get_left() + DOWN * 0.25,
            color=PURPLE_MODEL, stroke_width=2.5, buff=0.0,
        )
        self.play(ShowCreation(arr_v), ShowCreation(arr_i))

        # Merged cloud appears right, arrow from matrix
        merged = point_cloud_mob(RIGHT * 4.5, n=24, color=ACCENT_AMBER, seed=99)
        lbl_merged = Text("Common frame", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_AMBER)
        lbl_merged.next_to(merged, DOWN, buff=0.15)
        arr_out = Arrow(
            mat.get_right() + RIGHT * 0.05,
            merged.get_left() + LEFT * 0.05,
            color=PURPLE_MODEL, stroke_width=2.5, buff=0.0,
        )
        self.play(ShowCreation(arr_out))
        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in merged), lag_ratio=0.02, run_time=0.8))
        self.play(FadeIn(lbl_merged))

        # Ghost object bad calibration demo
        ghost = point_cloud_mob(RIGHT * 4.5 + UP * 1.2, n=10, color=RED_ERROR, spread=0.65, seed=13)
        ghost_lbl = Text("[WARN] Bad calib \u2192 ghost object", font=FONT_PRIMARY,
                         font_size=SIZE_LABEL, color=RED_ERROR)
        ghost_lbl.next_to(ghost, UP, buff=0.1)
        self.play(FadeIn(ghost, scale=0.5), FadeIn(ghost_lbl))
        self.play(Flash(VGroup(ghost, ghost_lbl), color=RED_ERROR, num_lines=8, line_length=0.3, run_time=0.5))
        self.play(FadeOut(ghost), FadeOut(ghost_lbl))

        self.wait(2)
        self._close()
