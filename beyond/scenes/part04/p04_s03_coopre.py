# beyond/scenes/part04/p04_s03_coopre.py
# ─────────────────────────────────────────────────────────────────
# P4-03  COOPRE — MASKED VOXEL PUZZLE  (~80s)  [WOW scene Part 4]
#
# BEV grid holographic. Agent A và B ở hai góc.
# 40% voxels bị tắt (pixel-dropout, LaggedStart).
# Question "Can you fill in what you can't see?" trôi lên.
# Agent B gửi particles → masked voxels bùng sáng lại từng cái.
# Results: 2 bars counter animate, IROS badge stamp in.
#
# Render:  manim -ql "beyond/scenes/part04/p04_s03_coopre.py" P04S03CooPre
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, glow_pulse,
    BG_SPACE, BG_PANEL, GRID_LINE,
    GOLD, GOLD_GLOW, CYAN_NEON, BLUE_ELECTRIC,
    P4_EFFICIENT, GREEN_SIGNAL, VOXEL_ACTIVE, VOXEL_MASKED,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=77)

ROWS, COLS = 8, 10
CELL = 0.52
MASK_RATIO = 0.40

# Grid center
GX, GY = -0.5, 0.2


class P04S03CooPre(BeyondScene):
    PART_COLOR = P4_EFFICIENT

    def construct(self):
        title_mob, sep = self.open("CooPre — Cooperative Pre-Training")
        self.wait(0.2)

        # ── BEV grid ──────────────────────────────────────────
        hw = COLS * CELL / 2
        hh = ROWS * CELL / 2
        grid_lines = VGroup()
        for i in range(COLS + 1):
            x = GX - hw + i * CELL
            grid_lines.add(Line([x, GY - hh, 0], [x, GY + hh, 0],
                                stroke_color=GRID_LINE, stroke_width=0.5,
                                stroke_opacity=0.5))
        for j in range(ROWS + 1):
            y = GY - hh + j * CELL
            grid_lines.add(Line([GX - hw, y, 0], [GX + hw, y, 0],
                                stroke_color=GRID_LINE, stroke_width=0.5,
                                stroke_opacity=0.5))
        self.play(FadeIn(grid_lines, run_time=0.5))

        # ── Voxels ────────────────────────────────────────────
        voxels = VGroup()
        voxel_positions = []
        for r in range(ROWS):
            for c in range(COLS):
                x = GX - hw + (c + 0.5) * CELL
                y = GY - hh + (r + 0.5) * CELL
                pos = np.array([x, y, 0])
                voxel_positions.append(pos)
                sq = Square(
                    side_length=CELL * 0.82,
                    fill_color=VOXEL_ACTIVE,
                    fill_opacity=0.60,
                    stroke_color=GRID_LINE, stroke_width=0.4,
                ).move_to(pos)
                voxels.add(sq)

        self.play(
            LaggedStart(*[GrowFromCenter(v, run_time=0.04) for v in voxels],
                        lag_ratio=0.015),
        )
        self.wait(0.2)

        # ── Agent labels ──────────────────────────────────────
        agent_a = Circle(radius=0.22, fill_color=CYAN_NEON, fill_opacity=1,
                         stroke_color=WHITE, stroke_width=1.3)
        agent_a.move_to([GX - hw - 0.9, GY, 0])
        lbl_a = Text("A", font_size=SIZE_MICRO + 2, color=WHITE,
                     font=FONT_PRIMARY, weight=BOLD).move_to(agent_a)

        agent_b = Circle(radius=0.22, fill_color=BLUE_ELECTRIC, fill_opacity=1,
                         stroke_color=WHITE, stroke_width=1.3)
        agent_b.move_to([GX + hw + 0.9, GY + hh * 0.5, 0])
        lbl_b = Text("B", font_size=SIZE_MICRO + 2, color=WHITE,
                     font=FONT_PRIMARY, weight=BOLD).move_to(agent_b)

        self.play(
            GrowFromCenter(agent_a), FadeIn(lbl_a),
            GrowFromCenter(agent_b), FadeIn(lbl_b),
        )
        self.wait(0.2)

        # ── MASKING — pixel dropout ────────────────────────────
        n_total = ROWS * COLS
        mask_idx = RNG.choice(n_total, int(n_total * MASK_RATIO), replace=False)
        mask_idx_set = set(mask_idx.tolist())

        self.play(
            LaggedStart(*[
                voxels[i].animate(run_time=0.12)
                         .set_fill(VOXEL_MASKED, opacity=0.18)
                for i in mask_idx
            ], lag_ratio=0.04),
        )

        # Question
        q = Text('"Can you fill in what you cannot see?"',
                 font_size=SIZE_LABEL - 2, color=GOLD,
                 font=FONT_PRIMARY, slant=ITALIC)
        q.to_edge(DOWN, buff=0.55)
        # Fix: use single animate chain for opacity + position
        q.set_opacity(0).shift(DOWN * 0.4)
        self.add(q)
        self.play(
            q.animate(run_time=0.70, rate_func=smooth)
             .shift(UP * 0.4).set_opacity(1.0),
        )
        self.wait(0.8)
        self.play(FadeOut(q, run_time=0.30))

        # ── RECONSTRUCTION — Agent B sends particles ───────────
        masked_voxels = [voxels[i] for i in mask_idx]
        # Sort by distance from B for natural flow
        masked_sorted = sorted(masked_voxels,
                               key=lambda v: np.linalg.norm(
                                   v.get_center() - agent_b.get_center()))

        reconstruct_anims = []
        for vox in masked_sorted:
            particle = Dot(radius=0.04, color=BLUE_ELECTRIC, fill_opacity=0.9)
            particle.move_to(agent_b.get_center())
            path = Line(agent_b.get_center(), vox.get_center())
            reconstruct_anims.append(
                Succession(
                    MoveAlongPath(particle, path,
                                  run_time=0.28, rate_func=smooth),
                    AnimationGroup(
                        vox.animate(run_time=0.15)
                           .set_fill(VOXEL_ACTIVE, opacity=0.65),
                        FadeOut(particle, run_time=0.10),
                    ),
                )
            )

        self.play(
            LaggedStart(*reconstruct_anims, lag_ratio=0.06),
        )

        # Full grid flash
        self.play(
            LaggedStart(*[
                voxels[i].animate(run_time=0.08).set_fill(GREEN_SIGNAL, opacity=0.7)
                for i in mask_idx
            ], lag_ratio=0.01),
        )
        self.play(
            LaggedStart(*[
                voxels[i].animate(run_time=0.12).set_fill(VOXEL_ACTIVE, opacity=0.60)
                for i in mask_idx
            ], lag_ratio=0.01),
        )
        self.wait(0.3)

        # ── Caption ───────────────────────────────────────────
        caption = Text(
            "Model learns: when I cannot see it, I ask another agent.",
            font_size=SIZE_MICRO + 2, color=TEXT_WHITE,
            font=FONT_PRIMARY, slant=ITALIC,
        )
        caption.to_edge(DOWN, buff=0.52)
        self.play(FadeIn(caption, shift=UP * 0.08, run_time=0.40))
        self.wait(0.5)
        self.play(FadeOut(caption, run_time=0.25))

        # ── Results bars ──────────────────────────────────────
        results_area = VGroup(grid_lines, voxels, agent_a, lbl_a, agent_b, lbl_b)
        self.play(
            results_area.animate(run_time=0.55).shift(LEFT * 2.5).scale(0.65),
        )

        # Simple bar chart (right side)
        bar_data = [
            ("Baseline\n(100% labels)",   1.00, TEXT_DIM,    "100%"),
            ("CooPre\n(50% labels)",      0.98, GREEN_SIGNAL, "≈100%  ✓"),
            ("CooPre\n(100% labels)",     1.04, GOLD,         "+4% AP ↑"),
        ]
        bar_w, bar_max_h = 0.55, 2.6
        bar_x_start = 1.8
        bar_spacing = 1.35
        bar_bottom_y = -1.2
        axes_obj = Axes(
            x_range=[0, 4, 1], y_range=[0, 1.1, 0.25],
            x_length=4.5, y_length=bar_max_h,
            axis_config={"color": TEXT_DIM, "stroke_width": 1.2,
                         "include_tip": False},
        ).shift(RIGHT * 3.0 + DOWN * 0.2)

        self.play(Create(axes_obj.y_axis, run_time=0.35),
                  Create(axes_obj.x_axis, run_time=0.35))

        for i, (lbl, frac, col, val_txt) in enumerate(bar_data):
            bh = bar_max_h * frac * 0.9
            bar = Rectangle(
                width=bar_w, height=0.01,
                fill_color=col, fill_opacity=0.88, stroke_width=0,
            )
            bar.align_to(axes_obj.get_bottom(), DOWN)
            bar.shift(RIGHT * (bar_x_start + i * bar_spacing - 0.5))

            bar_lbl = Text(lbl, font_size=SIZE_MICRO - 1,
                           color=col, font=FONT_PRIMARY, line_spacing=0.35)
            bar_lbl.next_to(bar, DOWN, buff=0.08)

            val_m = Text(val_txt, font_size=SIZE_MICRO + 1,
                         color=col, font=FONT_PRIMARY, weight=BOLD)

            self.play(
                bar.animate(run_time=0.9, rate_func=smooth)
                   .stretch_to_fit_height(bh)
                   .align_to(axes_obj.get_bottom(), DOWN)
                   .shift(RIGHT * (bar_x_start + i * bar_spacing - 0.5)),
                FadeIn(bar_lbl, run_time=0.35),
            )
            val_m.next_to(bar, UP, buff=0.08)
            self.play(
                FadeIn(val_m, scale=1.2, run_time=0.22),
                Flash(bar.get_top(), color=col,
                      flash_radius=0.25, num_lines=5, run_time=0.22),
            )

        # Badge
        badge_txt = Text(
            "★  IROS 2025 & CVPR 2025 DriveX Best Paper",
            font_size=SIZE_MICRO + 1, color=GOLD,
            font=FONT_PRIMARY, weight=BOLD,
        )
        badge_bg = RoundedRectangle(corner_radius=0.08,
                                    width=badge_txt.width + 0.5, height=0.48,
                                    fill_color="#1A1200", fill_opacity=1.0,
                                    stroke_color=GOLD, stroke_width=1.6)
        badge_txt.move_to(badge_bg)
        badge = VGroup(badge_bg, badge_txt)
        badge.to_edge(DOWN, buff=0.42)
        self.play(
            GrowFromCenter(badge_bg, run_time=0.30),
            FadeIn(badge_txt, run_time=0.22),
            Flash(badge_bg.get_center(), color=GOLD,
                  flash_radius=1.0, num_lines=10, run_time=0.40),
        )
        self.wait(1.5)

        self.close()
