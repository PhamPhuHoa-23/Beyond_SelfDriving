# beyond/scenes/part01/p01_s06_vla_gallery.py
# ─────────────────────────────────────────────────────────────────
# P1-06/07  VLA ARCHITECTURE GALLERY  (~70s)
#
# 4 cards lần lượt lật lên theo timeline 2021→2024:
#   BEVDriver (2021) — 3D→BEV compression (teal)
#   EMMA (2022)      — chain-of-thought all outputs (blue electric)
#   DriveVLM (2023)  — fast/slow dual tracks (indigo)
#   AutoVLA (2024)   — scene complexity switch → p01_s08
#
# Mỗi card: border trace B1, nội dung scan in.
# Timeline spine với year labels dưới.
#
# Render:  manim -ql "beyond/scenes/part01/p01_s06_vla_gallery.py" P01S06VlaGallery
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block, pipeline_block_entrance,
    pipeline_arrow_entrance,
    BG_PANEL, BG_SPACE,
    GOLD, GOLD_GLOW, CYAN_NEON, P1_FOUNDATION, P2_COOP,
    BLUE_ELECTRIC, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

CARD_W = 2.8
CARD_H = 3.6
CARD_XS = [-4.8, -1.6, 1.6, 4.8]

CARDS = [
    {
        "year": "2021", "name": "BEVDriver",
        "color": P2_COOP,
        "tag": "3D → BEV",
        "body": [
            "3D LiDAR scan",
            "↓  compress to 2D",
            "Bird's Eye View grid",
            "→ LLM reasoning",
        ],
        "insight": "First to use LLM\non BEV features",
    },
    {
        "year": "2022", "name": "EMMA",
        "color": BLUE_ELECTRIC,
        "tag": "Language = universal output",
        "body": [
            "Camera images",
            "↓",
            "Chain-of-Thought",
            "→ Detection",
            "→ Prediction",
            "→ Planning",
        ],
        "insight": "All tasks through\none language model",
    },
    {
        "year": "2023", "name": "DriveVLM",
        "color": P1_FOUNDATION,
        "tag": "Fast + Slow thinking",
        "body": [
            "FAST track (trad.)",
            "→ routine scenes",
            "",
            "SLOW track (VLM)",
            "→ complex scenes",
            "→ merged decision",
        ],
        "insight": "Dual-speed architecture",
    },
    {
        "year": "2024", "name": "AutoVLA",
        "color": GOLD,
        "tag": "UCLA · IROS 2025 Best Paper",
        "body": [
            "Scene Complexity",
            "Analyzer",
            "↓",
            "Simple → Fast",
            "Complex → VLA",
            "★ Best of both",
        ],
        "insight": "See p01_s08 for\nfull breakdown",
    },
]


def _card_group(card: dict, x: float) -> VGroup:
    """Full card VGroup: border + header + body lines."""
    bg = RoundedRectangle(
        corner_radius=0.14, width=CARD_W, height=CARD_H,
        fill_color=BG_PANEL, fill_opacity=1.0,
        stroke_color=card["color"], stroke_width=1.8,
    ).move_to([x, 0.3, 0])

    # Header strip
    header_bg = Rectangle(
        width=CARD_W, height=0.68,
        fill_color=card["color"], fill_opacity=0.22, stroke_width=0,
    )
    header_bg.align_to(bg, UP).shift(DOWN * 0.01)

    name_t = Text(card["name"], font_size=SIZE_MICRO + 4,
                  color=card["color"], font=FONT_PRIMARY, weight=BOLD)
    year_t = Text(card["year"], font_size=SIZE_MICRO,
                  color=TEXT_DIM, font=FONT_PRIMARY)
    VGroup(name_t, year_t).arrange(RIGHT, buff=0.2)
    VGroup(name_t, year_t).move_to(header_bg)

    tag_t = Text(card["tag"], font_size=SIZE_MICRO - 1,
                 color=card["color"], font=FONT_PRIMARY, slant=ITALIC)
    tag_t.next_to(header_bg, DOWN, buff=0.12)

    # Body text
    body_lines = VGroup(*[
        Text(line if line else " ", font_size=SIZE_MICRO,
             color=TEXT_WHITE if not line.startswith("→") else card["color"],
             font=FONT_PRIMARY)
        for line in card["body"]
    ]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    body_lines.next_to(tag_t, DOWN, buff=0.14)
    body_lines.align_to(bg, LEFT).shift(RIGHT * 0.20)

    # Insight footer
    insight_t = Text(card["insight"], font_size=SIZE_MICRO - 1,
                     color=TEXT_DIM, font=FONT_PRIMARY,
                     slant=ITALIC, line_spacing=0.38)
    insight_t.align_to(bg, DOWN).shift(UP * 0.22 + RIGHT * (x - bg.get_left()[0]))
    insight_t.move_to([x, bg.get_bottom()[1] + 0.22, 0])

    return VGroup(bg, header_bg, name_t, year_t, tag_t, body_lines, insight_t)


class P01S06VlaGallery(BeyondScene):
    PART_COLOR = P1_FOUNDATION

    def construct(self):
        title_mob, sep = self.open("Vision-Language-Action Architecture Gallery")
        self.wait(0.2)

        # ── Timeline spine ────────────────────────────────────
        spine_y = -2.55
        spine = Line(LEFT * 5.5, RIGHT * 5.5,
                     stroke_color=TEXT_GHOST, stroke_width=1.2)
        spine.set_y(spine_y)
        self.play(Create(spine, run_time=0.55, rate_func=smooth))

        # Year markers on spine
        year_mobs = VGroup()
        for card, x in zip(CARDS, CARD_XS):
            ym = Text(card["year"], font_size=SIZE_MICRO,
                      color=TEXT_DIM, font=FONT_PRIMARY)
            ym.move_to([x, spine_y - 0.28, 0])
            year_mobs.add(ym)
            tick = Line([x, spine_y - 0.08, 0], [x, spine_y + 0.08, 0],
                        stroke_color=TEXT_DIM, stroke_width=1.0)
            year_mobs.add(tick)
        self.play(LaggedStart(*[FadeIn(m, run_time=0.18) for m in year_mobs],
                              lag_ratio=0.12))
        self.wait(0.2)

        # ── Cards appear one by one ────────────────────────────
        card_groups = []
        for i, (card, x) in enumerate(zip(CARDS, CARD_XS)):
            cg = _card_group(card, x)
            card_groups.append(cg)

            bg = cg[0]
            rest = VGroup(*cg[1:])

            # B1-style: border trace → content scan in
            self.play(Create(bg, run_time=0.40, rate_func=smooth))

            # Scan line sweeps down through card
            scan = Line(
                bg.get_left() + UP * (CARD_H / 2 - 0.05),
                bg.get_right() + UP * (CARD_H / 2 - 0.05),
                stroke_color=card["color"], stroke_width=1.5,
                stroke_opacity=0.70,
            )
            self.play(
                AnimationGroup(
                    scan.animate(run_time=0.55, rate_func=linear)
                        .shift(DOWN * CARD_H),
                    LaggedStart(*[FadeIn(m, shift=DOWN * 0.04, run_time=0.18)
                                  for m in rest], lag_ratio=0.08),
                ),
            )
            self.play(scan.animate(run_time=0.15, rate_func=rush_into)
                         .shift(DOWN * 0.4).set_stroke(opacity=0))
            self.remove(scan)

            # Connector from spine to card
            conn = Line([x, spine_y, 0], [x, bg.get_bottom()[1] + 0.05, 0],
                        stroke_color=card["color"], stroke_width=0.8,
                        stroke_opacity=0.45)
            self.add_to_back(conn)

            if i < len(CARDS) - 1:
                self.wait(0.40)   # breathing room between cards

        self.wait(0.6)

        # ── Bridge: AutoVLA is the CLIMAX ─────────────────────
        # Highlight AutoVLA card (last)
        last_card_bg = card_groups[-1][0]
        self.play(
            last_card_bg.animate(run_time=0.40)
                        .set_stroke(GOLD_GLOW, width=2.8),
            Flash(CARD_XS[-1], color=GOLD,
                  flash_radius=0.80, num_lines=10, run_time=0.45),
        )
        self.wait(0.5)

        bridge = Text("Next: AutoVLA in depth  →",
                      font_size=SIZE_LABEL - 1, color=P1_FOUNDATION,
                      font=FONT_PRIMARY, slant=ITALIC)
        bridge.to_edge(DOWN, buff=0.45)
        self.play(Write(bridge, run_time=0.70))
        self.wait(1.5)

        self.close()
