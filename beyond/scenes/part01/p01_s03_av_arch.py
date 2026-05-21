# beyond/scenes/part01/p01_s03_av_arch.py
# ─────────────────────────────────────────────────────────────────
# P1-03  BA KIẾN TRÚC AV  (~55s)
#
# 3 cột pipeline: MODULAR (trái), HYBRID (giữa), E2E (phải).
# Xuất hiện lần lượt, không cùng lúc.
#
# MODULAR: pipeline build từng block B1, mũi tên electric.
#   → Error cascade animation: nhiễu khuếch đại, mũi tên flash đỏ,
#   → xe đi sai hướng, 3 badge ✗.
#
# E2E: 1 block lớn với neural net pulsing bên trong.
#   → 1 badge ✓ (joint opt) + 1 ⚠ (black box).
#
# HYBRID: kết hợp, badges.
#
# Kết: tất cả dim → dòng "Cả ba đều có chung một điểm yếu." sáng.
#
# Render:  manim -ql "beyond/scenes/part01/p01_s03_av_arch.py" P01S03AvArch
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    pipeline_block, pipeline_arrow, pipeline_block_entrance, pipeline_arrow_entrance,
    BG_SPACE, BG_PANEL,
    GOLD, CYAN_NEON, P1_FOUNDATION,
    RED_ALERT, GREEN_SIGNAL, TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=55)

# ── Column x-positions ─────────────────────────────────────────────
COL_L = -4.6    # MODULAR
COL_M =  0.0    # HYBRID
COL_R = +4.6    # E2E

BLOCK_W = 2.05
BLOCK_H = 0.62
ARROW_COLOR = CYAN_NEON


def _col_title(text: str, color: str, x: float) -> Text:
    t = Text(text, font_size=SIZE_LABEL, color=color,
             font=FONT_PRIMARY, weight=BOLD)
    t.move_to([x, 3.0, 0])
    return t


def _badge(symbol: str, text: str, color: str) -> VGroup:
    sym = Text(symbol, font_size=SIZE_MICRO + 2, color=color, font=FONT_PRIMARY)
    lbl = Text(text,   font_size=SIZE_MICRO,     color=color, font=FONT_PRIMARY)
    row = VGroup(sym, lbl).arrange(RIGHT, buff=0.14)
    return row


def _vertical_pipeline(labels: list, x: float, top_y: float,
                        border: str, gap: float = 0.18) -> tuple:
    """Build vertical stack of pipeline blocks + downward arrows."""
    blocks = []
    arrows = []
    y = top_y
    for i, lbl in enumerate(labels):
        blk = pipeline_block(lbl, width=BLOCK_W, height=BLOCK_H,
                             border_color=border, fill_color=BG_PANEL,
                             font_size=SIZE_MICRO + 1)
        blk.move_to([x, y, 0])
        blocks.append(blk)
        if i < len(labels) - 1:
            arr = Arrow(
                blk.get_bottom(), blk.get_bottom() + DOWN * gap,
                buff=0.05, color=ARROW_COLOR,
                stroke_width=1.8, tip_length=0.14,
                max_tip_length_to_length_ratio=0.6,
            )
            # arrow will be repositioned after next block placed
            arrows.append(arr)
        y -= BLOCK_H + gap
    # Fix arrow positions now that blocks are placed
    for i, arr in enumerate(arrows):
        arr.put_start_and_end_on(
            blocks[i].get_bottom() + DOWN * 0.02,
            blocks[i + 1].get_top() + UP * 0.02,
        )
    return blocks, arrows


class P01S03AvArch(BeyondScene):
    PART_COLOR = P1_FOUNDATION

    def construct(self):
        title_mob, sep = self.open("Three Architectures for AV")
        self.wait(0.2)

        # ════════════════════════════════════════════════════════
        # COLUMN 1 — MODULAR
        # ════════════════════════════════════════════════════════
        col1_title = _col_title("MODULAR", CYAN_NEON, COL_L)
        self.play(FadeIn(col1_title, shift=DOWN * 0.08, run_time=0.35))

        mod_labels = ["Perception", "Localization",
                      "Prediction", "Planning", "Control"]
        mod_blocks, mod_arrows = _vertical_pipeline(
            mod_labels, COL_L, top_y=2.0, border=CYAN_NEON
        )

        # Build blocks one by one (B1 animation)
        for blk, arr in zip(mod_blocks, mod_arrows + [None]):
            self.play(pipeline_block_entrance(blk, accent_color=CYAN_NEON),
                      run_time=0.55)
            if arr is not None:
                self.play(pipeline_arrow_entrance(arr, style="electric"),
                          run_time=0.25)
        self.play(pipeline_block_entrance(mod_blocks[-1], CYAN_NEON), run_time=0.55)

        # ── Error cascade animation ──────────────────────────
        # Noise particle appears in Perception, khuếch đại xuống
        noise = Dot(radius=0.06, color=RED_ALERT, fill_opacity=0.9)
        noise.move_to(mod_blocks[0].get_center())
        self.play(GrowFromCenter(noise, run_time=0.20))
        self.wait(0.15)

        for i, arr in enumerate(mod_arrows):
            # Arrow flashes red + shakes
            self.play(
                arr.animate(run_time=0.12).set_color(RED_ALERT).set_stroke(width=3.0),
                arr.animate(run_time=0.05).shift(RIGHT * 0.06),
                arr.animate(run_time=0.05).shift(LEFT * 0.12),
                arr.animate(run_time=0.05).shift(RIGHT * 0.06),
            )
            # Noise grows as it propagates
            scale_f = 1.0 + (i + 1) * 0.45
            new_pos = mod_blocks[i + 1].get_center()
            self.play(
                noise.animate(run_time=0.18, rate_func=rush_into)
                     .move_to(new_pos).scale(scale_f),
            )
        self.play(FadeOut(noise, run_time=0.25))

        # 3 ✗ badges
        bad_labels = ["✗ Error accumulation",
                      "✗ No joint optimization",
                      "✗ Cannot learn continuously"]
        badges1 = VGroup(*[
            _badge("", lbl, RED_ALERT) for lbl in bad_labels
        ]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        badges1.next_to(mod_blocks[-1], DOWN, buff=0.22)
        self.play(
            LaggedStart(*[
                FadeIn(b, shift=UP * 0.07, run_time=0.28)
                for b in badges1
            ], lag_ratio=0.18),
        )
        self.wait(0.4)

        # ════════════════════════════════════════════════════════
        # COLUMN 3 — E2E (appears second per guide)
        # ════════════════════════════════════════════════════════
        col3_title = _col_title("END-TO-END", P1_FOUNDATION, COL_R)
        self.play(FadeIn(col3_title, shift=DOWN * 0.08, run_time=0.35))

        # ONE large block — neural net pulsing inside
        e2e_rect = RoundedRectangle(
            corner_radius=0.16, width=BLOCK_W + 0.2, height=3.4,
            fill_color=BG_PANEL, fill_opacity=1.0,
            stroke_color=P1_FOUNDATION, stroke_width=1.8,
        ).move_to([COL_R, 0.6, 0])

        # Neural dots inside
        n_dots = 18
        inner_dots = VGroup(*[
            Dot(
                radius=float(RNG.uniform(0.028, 0.052)),
                color=P1_FOUNDATION,
                fill_opacity=float(RNG.uniform(0.2, 0.75)),
            ).move_to([
                COL_R + float(RNG.uniform(-0.7, 0.7)),
                float(RNG.uniform(-0.7, 2.0)),
                0,
            ])
            for _ in range(n_dots)
        ])
        e2e_label_top = Text("Sensors", font_size=SIZE_MICRO + 1,
                             color=TEXT_DIM, font=FONT_PRIMARY)
        e2e_label_top.next_to(e2e_rect, UP, buff=0.12)
        e2e_label_bot = Text("Action", font_size=SIZE_MICRO + 1,
                             color=TEXT_DIM, font=FONT_PRIMARY)
        e2e_label_bot.next_to(e2e_rect, DOWN, buff=0.12)

        self.play(Create(e2e_rect, run_time=0.50))

        # Neural shimmer
        def shimmer(mob, alpha):
            for d in mob:
                d.set_fill(opacity=0.15 + 0.60 * abs(np.sin(alpha * np.pi * 3 + float(RNG.random()) * 2)))
        self.play(
            FadeIn(inner_dots, run_time=0.25),
            UpdateFromAlphaFunc(inner_dots, shimmer, run_time=0.90),
        )
        self.play(FadeOut(inner_dots, run_time=0.30))

        e2e_center_label = Text("Neural\nNetwork", font_size=SIZE_MICRO + 2,
                                color=P1_FOUNDATION, font=FONT_PRIMARY,
                                line_spacing=0.4)
        e2e_center_label.move_to(e2e_rect)
        self.play(
            FadeIn(e2e_center_label, run_time=0.25),
            FadeIn(e2e_label_top, run_time=0.25),
            FadeIn(e2e_label_bot, run_time=0.25),
        )

        badges3 = VGroup(
            _badge("✓", "Joint optimization",      GREEN_SIGNAL),
            _badge("✓", "No error accumulation",   GREEN_SIGNAL),
            _badge("⚠", "Black box — hard to debug", GOLD),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        badges3.next_to(e2e_rect, DOWN, buff=0.28)
        self.play(
            LaggedStart(*[
                FadeIn(b, shift=UP * 0.07, run_time=0.28)
                for b in badges3
            ], lag_ratio=0.18),
        )
        self.wait(0.35)

        # ════════════════════════════════════════════════════════
        # COLUMN 2 — HYBRID (appears last)
        # ════════════════════════════════════════════════════════
        col2_title = _col_title("HYBRID", GOLD, COL_M)
        self.play(FadeIn(col2_title, shift=DOWN * 0.08, run_time=0.35))

        hyb_labels = ["ML Perception", "ML Planning", "Trad. Control"]
        hyb_blocks, hyb_arrows = _vertical_pipeline(
            hyb_labels, COL_M, top_y=1.8, border=GOLD
        )
        for blk, arr in zip(hyb_blocks, hyb_arrows + [None]):
            self.play(pipeline_block_entrance(blk, accent_color=GOLD), run_time=0.45)
            if arr is not None:
                self.play(pipeline_arrow_entrance(arr, style="electric"), run_time=0.20)
        self.play(pipeline_block_entrance(hyb_blocks[-1], GOLD), run_time=0.45)

        badges2 = VGroup(
            _badge("✓", "Best of both worlds",    GREEN_SIGNAL),
            _badge("✓", "Industry standard",       GREEN_SIGNAL),
            _badge("→", "Still has a flaw...",     TEXT_DIM),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        badges2.next_to(hyb_blocks[-1], DOWN, buff=0.22)
        self.play(
            LaggedStart(*[
                FadeIn(b, shift=UP * 0.07, run_time=0.28)
                for b in badges2
            ], lag_ratio=0.18),
        )
        self.wait(0.6)

        # ── ALL DIM → single truth ─────────────────────────────
        all_content = VGroup(
            col1_title, VGroup(*mod_blocks), VGroup(*mod_arrows), badges1,
            col2_title, VGroup(*hyb_blocks), VGroup(*hyb_arrows), badges2,
            col3_title, e2e_rect, e2e_center_label, e2e_label_top,
            e2e_label_bot, badges3,
        )
        self.play(all_content.animate(run_time=0.70).set_opacity(0.22))

        # Per guide: "1.5 giây im lặng" — let the dimmed scene breathe
        self.wait(1.5)

        # Final reveal — Write for dramatic weight
        truth = Text("All three share the same fundamental flaw.",
                     font_size=SIZE_LABEL + 1,
                     color=TEXT_WHITE, font=FONT_PRIMARY)
        truth.move_to(DOWN * 0.15)
        self.play(Write(truth, run_time=0.90))
        self.wait(1.8)

        # ── Close ─────────────────────────────────────────────
        self.close()
