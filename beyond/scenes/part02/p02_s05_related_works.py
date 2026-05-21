# beyond/scenes/part02/p02_s05_related_works.py
# ─────────────────────────────────────────────────────────────────
# P2-05  RELATED WORKS CHAIN  (~55s)
#
# Dùng evolution_timeline recipe (J1 từ MICRO_ANIMATION_BIBLE).
# 4 methods: V2VNet → V2X-ViT → Where2comm → CodeFilling.
# Dấu ??? blink. Khoảng trống. V2XPnP bay vào fill the gap.
# PI bubble: "But all 4 miss multi-frame multi-task fusion..."
#
# Render:  manim -ql "beyond/scenes/part02/p02_s05_related_works.py" P02S05RelatedWorks
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, evolution_timeline,
    PIBubble, PiMascot,
    GOLD, GOLD_GLOW, CYAN_NEON, P2_COOP,
    BLUE_ELECTRIC, P1_FOUNDATION, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

MILESTONES = [
    {
        "year": 2020, "name": "V2VNet",
        "contribution": "GNN Fusion",
        "bottleneck": "fusion quality",
        "color": P2_COOP,
    },
    {
        "year": 2022, "name": "V2X-ViT",
        "contribution": "Transformer Attention",
        "bottleneck": "comm. volume",
        "color": BLUE_ELECTRIC,
    },
    {
        "year": 2022, "name": "Where2comm",
        "contribution": "Sparse Communication",
        "bottleneck": "feature size",
        "color": P1_FOUNDATION,
    },
    {
        "year": 2024, "name": "CodeFilling",
        "contribution": "Codebook Compression",
        "bottleneck": "???",
        "color": GOLD,
    },
]


class P02S05RelatedWorks(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("The Evolution of Cooperative Perception")
        self.wait(0.2)

        # ── Timeline (shift up to leave room below) ────────────
        full_grp, timeline_anim = evolution_timeline(MILESTONES, spine_y=0.3)
        full_grp.shift(UP * 0.5)

        self.play(timeline_anim, run_time=5.0)
        self.wait(0.4)

        # ── ??? on CodeFilling bottleneck — blink ─────────────
        # Find the bottleneck text for CodeFilling (last milestone)
        # It's inside full_grp — just create a new blink dot
        q_marks = Text("??? ", font_size=SIZE_LABEL,
                       color=RED_ALERT if False else GOLD,
                       font=FONT_PRIMARY, weight=BOLD)
        # Position near CodeFilling node (rightmost)
        # Spine starts at x = -spine_w/2, spacing = spine_w/(n-1)
        n = len(MILESTONES)
        spine_w = min(12.0, (n - 1) * 3.0)
        cf_x = spine_w / 2  # rightmost node
        q_marks.move_to(np.array([cf_x, 0.3 - 0.88, 0]) + UP * 0.5)
        self.add(q_marks)

        # Blink 3 times
        for _ in range(3):
            self.play(q_marks.animate(run_time=0.25).set_opacity(0))
            self.play(q_marks.animate(run_time=0.25).set_opacity(1.0))
        self.wait(0.2)

        # ── Timeline extension line (khoảng trống sau CodeFilling) ──
        gap_line = DashedLine(
            full_grp.get_right() + RIGHT * 0.1,
            full_grp.get_right() + RIGHT * 2.0,
            stroke_color=TEXT_GHOST, stroke_width=1.0,
            dash_length=0.12,
        )
        gap_line.set_y(0.3 + 0.5)   # align with spine y
        self.play(Create(gap_line, run_time=0.45, rate_func=smooth))
        self.wait(0.2)

        # ── PI mascot + bubble ─────────────────────────────────
        pi = PiMascot(height=0.85).to_corner(UR, buff=0.55)
        self.play(GrowFromCenter(pi, run_time=0.40))

        pi_bubble = PIBubble(
            pi,
            "All 4 miss\nmulti-frame,\nmulti-task fusion.",
            position=DOWN + LEFT,
            font_size=SIZE_MICRO + 1,
        )
        self.play(FadeIn(pi_bubble, shift=DOWN * 0.06, run_time=0.35))
        self.wait(1.2)
        self.play(FadeOut(pi_bubble, run_time=0.22))
        self.wait(0.15)

        # ── V2XPnP flies in from right edge ───────────────────
        v2xpnp_pos = full_grp.get_right() + RIGHT * 2.5 + UP * 0.5
        v2xpnp_node = Circle(
            radius=0.26,
            fill_color=GOLD, fill_opacity=1.0,
            stroke_color=WHITE, stroke_width=2.0,
        ).move_to(v2xpnp_pos + RIGHT * 5)  # start off-screen right

        v2xpnp_num = Text("?", font_size=SIZE_MICRO,
                          color="#0A0A16", font=FONT_PRIMARY, weight=BOLD)
        v2xpnp_num.move_to(v2xpnp_node)

        v2xpnp_lbl = Text("V2XPnP", font_size=SIZE_LABEL - 2,
                           color=GOLD, font=FONT_PRIMARY, weight=BOLD)
        v2xpnp_sub = Text("Multi-agent × Multi-frame\n× Multi-task",
                          font_size=SIZE_MICRO, color=GOLD_GLOW,
                          font=FONT_PRIMARY, line_spacing=0.38)
        v2xpnp_lbl.next_to(v2xpnp_node.copy().move_to(v2xpnp_pos), UP, buff=0.22)
        v2xpnp_sub.next_to(v2xpnp_lbl, DOWN, buff=0.10)

        self.add(v2xpnp_node, v2xpnp_num)
        self.play(
            v2xpnp_node.animate(run_time=0.65, rate_func=rush_into)
                       .move_to(v2xpnp_pos),
            v2xpnp_num.animate(run_time=0.65, rate_func=rush_into)
                      .move_to(v2xpnp_pos),
        )
        self.play(
            Flash(v2xpnp_pos, color=GOLD,
                  flash_radius=0.70, num_lines=12, run_time=0.50),
            v2xpnp_num.animate(run_time=0.20).become(
                Text("★", font_size=SIZE_MICRO + 2,
                     color="#0A0A16", font=FONT_PRIMARY)
                .move_to(v2xpnp_pos)
            ),
        )
        self.play(
            LaggedStart(
                FadeIn(v2xpnp_lbl, shift=UP * 0.08, run_time=0.30),
                FadeIn(v2xpnp_sub, shift=UP * 0.06, run_time=0.30),
                lag_ratio=0.25,
            )
        )
        self.wait(1.5)

        self.close()
