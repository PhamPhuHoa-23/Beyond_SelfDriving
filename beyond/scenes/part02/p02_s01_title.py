# beyond/scenes/part02/p02_s01_title.py
# ─────────────────────────────────────────────────────────────────
# P2-01  TITLE CARD — COOPERATIVE AUTOMATION  (~25s)
#
# Teal bùng lên từ trung tâm như sóng biển lan ra.
# Title forge. Quote. Roadmap nút 2 sáng.
#
# Render:  manim -ql "beyond/scenes/part02/p02_s01_title.py" P02S01Title
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components.colors import (
    BG_VOID, P2_COOP, GOLD, GOLD_GLOW,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_HERO, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)


def _roadmap_strip(current: int) -> VGroup:
    part_colors = ["#7986CB", "#00BCD4", "#4CAF50", "#FFC107", "#F06292"]
    spacing = 1.1
    line = Line(LEFT * spacing * 2, RIGHT * spacing * 2,
                stroke_color=TEXT_GHOST, stroke_width=1.2)
    dots = VGroup()
    for i in range(5):
        x = (i - 2) * spacing
        active = (i + 1 == current)
        d = Circle(
            radius=0.11,
            fill_color=part_colors[i] if active else TEXT_GHOST,
            fill_opacity=1.0 if active else 0.35,
            stroke_color=part_colors[i] if active else TEXT_DIM,
            stroke_width=1.4,
        ).move_to([x, 0, 0])
        dots.add(d)
    return VGroup(line, dots).move_to(DOWN * 3.05)


class P02S01Title(Scene):
    def setup(self):
        self.camera.background_color = BG_VOID

    def construct(self):
        # ── Teal wave burst from center ───────────────────────
        rings = [
            Circle(radius=0.05 * (i + 1),
                   stroke_color=P2_COOP,
                   stroke_width=max(0.5, 3.0 - i * 0.5),
                   stroke_opacity=max(0, 0.9 - i * 0.12),
                   fill_opacity=0)
            for i in range(8)
        ]
        [self.add(r) for r in rings]
        self.play(
            LaggedStart(*[
                r.animate(run_time=0.9, rate_func=rush_from)
                 .scale(22 + i * 6)
                 .set_stroke(opacity=0)
                for i, r in enumerate(rings)
            ], lag_ratio=0.06),
            run_time=1.0,
        )
        [self.remove(r) for r in rings]

        # ── Supertitle ────────────────────────────────────────
        super_t = Text("Part  02", font_size=SIZE_MICRO + 2,
                       color=TEXT_DIM, font=FONT_PRIMARY)
        super_t.to_corner(UR, buff=0.55)
        self.play(FadeIn(super_t, shift=DOWN * 0.08, run_time=0.30))

        # ── Forge title ───────────────────────────────────────
        line1 = Text("Towards End-to-End",
                     font_size=SIZE_HERO,
                     color="#FFFDE7", font=FONT_PRIMARY, weight=BOLD)
        line2 = Text("Cooperative Automation",
                     font_size=SIZE_HERO - 4,
                     color="#FFFDE7", font=FONT_PRIMARY, weight=BOLD)
        title_grp = VGroup(line1, line2).arrange(DOWN, buff=0.15)
        for ln in (line1, line2):
            if ln.width > 12.5:
                ln.scale(12.5 / ln.width)
        title_grp.arrange(DOWN, buff=0.15).move_to(UP * 1.3)

        self.play(AddTextLetterByLetter(line1, run_time=1.3, rate_func=linear))
        self.play(AddTextLetterByLetter(line2, run_time=1.1, rate_func=linear))
        self.play(
            line1.animate(run_time=0.40).set_color(P2_COOP),
            line2.animate(run_time=0.40).set_color(P2_COOP),
            LaggedStart(*[
                Flash(ch.get_center(), color=P2_COOP,
                      flash_radius=0.13, num_lines=4, run_time=0.15)
                for ch in list(line1) + list(line2)
            ], lag_ratio=0.02),
            run_time=0.55,
        )
        self.wait(0.2)

        # ── Presenter ─────────────────────────────────────────
        presenter = Text("Zewei Zhou  ·  UCLA Mobility Lab",
                         font_size=SIZE_LABEL, color=TEXT_DIM,
                         font=FONT_PRIMARY)
        presenter.next_to(title_grp, DOWN, buff=0.50)
        self.play(FadeIn(presenter, shift=UP * 0.10, run_time=0.40))

        sep = Line(LEFT * 4.2, RIGHT * 4.2, stroke_color=P2_COOP,
                   stroke_width=0.8, stroke_opacity=0.40)
        sep.next_to(presenter, DOWN, buff=0.28)
        self.play(Create(sep, run_time=0.38))

        # ── Quote ─────────────────────────────────────────────
        quote = Text(
            '"Single agent, no matter how smart,\n'
            '  is limited by its own line of sight."',
            font_size=SIZE_MICRO + 3, color=TEXT_WHITE,
            font=FONT_PRIMARY, slant=ITALIC, line_spacing=0.45,
        )
        quote.next_to(sep, DOWN, buff=0.30)
        self.play(Write(quote, run_time=1.0))
        self.wait(0.15)

        # ── Roadmap ───────────────────────────────────────────
        roadmap = _roadmap_strip(current=2)
        self.play(FadeIn(roadmap, run_time=0.35))
        p2_dot = roadmap[1][1]
        self.play(Flash(p2_dot.get_center(), color=P2_COOP,
                        flash_radius=0.28, num_lines=8, run_time=0.38))

        self.wait(2.2)

        # ── Fade out ──────────────────────────────────────────
        all_m = [super_t, title_grp, presenter, sep, quote, roadmap]
        self.play(
            LaggedStart(*[FadeOut(m, run_time=0.38) for m in all_m],
                        lag_ratio=0.06),
        )
        self.wait(0.15)
