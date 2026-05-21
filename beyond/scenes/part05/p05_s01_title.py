# beyond/scenes/part05/p05_s01_title.py
# ─────────────────────────────────────────────────────────────────
# P5-01  TITLE CARD — PHYSICAL AI  (~30s)  [ĐẶC BIỆT]
#
# Khoảnh khắc cảm xúc: lần đầu tiên cả 5 nút sáng lên.
# Mỗi nút bùng theo màu của part mình → tất cả đổi GOLD cùng lúc.
# Đường kết nối GOLD chạy nối tất cả 5 nút.
# Quote: "Beyond cars — to any agent, any space."
#
# Render:  manim -ql "beyond/scenes/part05/p05_s01_title.py" P05S01Title
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components.colors import (
    BG_VOID, P5_PHYSICAL, GOLD, GOLD_GLOW,
    P1_FOUNDATION, P2_COOP, P3_SIM, P4_EFFICIENT,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_HERO, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

PART_COLORS = [P1_FOUNDATION, P2_COOP, P3_SIM, P4_EFFICIENT, P5_PHYSICAL]


def _make_roadmap_animated() -> tuple:
    """Returns (line, dots, strip_group) — dots are individual for per-dot animation."""
    spacing = 1.1
    line = Line(LEFT * spacing * 2, RIGHT * spacing * 2,
                stroke_color=TEXT_GHOST, stroke_width=1.3)
    dots = VGroup()
    for i in range(5):
        x = (i - 2) * spacing
        d = Circle(
            radius=0.13,
            fill_color=TEXT_GHOST, fill_opacity=0.35,
            stroke_color=TEXT_DIM, stroke_width=1.4,
        ).move_to([x, 0, 0])
        dots.add(d)
    strip = VGroup(line, dots)
    strip.move_to(DOWN * 3.0)
    return line, dots, strip


class P05S01Title(Scene):
    def setup(self):
        self.camera.background_color = BG_VOID

    def construct(self):
        # ── Pink light radiates from center ───────────────────
        for i in range(5):
            r = Circle(radius=0.1 * (i + 1),
                       stroke_color=P5_PHYSICAL,
                       stroke_width=max(0.4, 2.5 - i * 0.45),
                       stroke_opacity=max(0, 0.85 - i * 0.14),
                       fill_opacity=0)
            self.add(r)
        self.play(
            LaggedStart(*[
                self.mobjects[-(i+1)].animate(run_time=0.80, rate_func=rush_from)
                .scale(28 + i * 5).set_stroke(opacity=0)
                for i in range(5)
            ], lag_ratio=0.08),
            run_time=0.85,
        )

        # ── Supertitle ────────────────────────────────────────
        super_t = Text("Part  05", font_size=SIZE_MICRO + 2,
                       color=TEXT_DIM, font=FONT_PRIMARY)
        super_t.to_corner(UR, buff=0.55)
        self.play(FadeIn(super_t, shift=DOWN * 0.08, run_time=0.28))

        # ── Forge title ───────────────────────────────────────
        line1 = Text("Scalable, Human-Centric",
                     font_size=SIZE_HERO, color="#FFFDE7",
                     font=FONT_PRIMARY, weight=BOLD)
        line2 = Text("Physical AI",
                     font_size=SIZE_HERO, color="#FFFDE7",
                     font=FONT_PRIMARY, weight=BOLD)
        title_grp = VGroup(line1, line2).arrange(DOWN, buff=0.15)
        for ln in (line1, line2):
            if ln.width > 12.5:
                ln.scale(12.5 / ln.width)
        title_grp.arrange(DOWN, buff=0.15).move_to(UP * 1.35)

        self.play(AddTextLetterByLetter(line1, run_time=1.1, rate_func=linear))
        self.play(AddTextLetterByLetter(line2, run_time=0.8, rate_func=linear))
        self.play(
            line1.animate(run_time=0.40).set_color(P5_PHYSICAL),
            line2.animate(run_time=0.40).set_color(P5_PHYSICAL),
            LaggedStart(*[
                Flash(ch.get_center(), color=P5_PHYSICAL,
                      flash_radius=0.12, num_lines=4, run_time=0.14)
                for ch in list(line1) + list(line2)
            ], lag_ratio=0.02),
            run_time=0.55,
        )
        self.wait(0.2)

        # Presenter + sep + quote
        presenter = Text("Wayne Wu  ·  UCLA Mobility Lab",
                         font_size=SIZE_LABEL, color=TEXT_DIM, font=FONT_PRIMARY)
        presenter.next_to(title_grp, DOWN, buff=0.45)
        self.play(FadeIn(presenter, shift=UP * 0.10, run_time=0.38))

        sep = Line(LEFT * 4.0, RIGHT * 4.0, stroke_color=P5_PHYSICAL,
                   stroke_width=0.8, stroke_opacity=0.40)
        sep.next_to(presenter, DOWN, buff=0.25)
        self.play(Create(sep, run_time=0.35))

        quote = Text('"Beyond cars —\n to any agent, any space."',
                     font_size=SIZE_MICRO + 4, color=TEXT_WHITE,
                     font=FONT_PRIMARY, slant=ITALIC, line_spacing=0.45)
        quote.next_to(sep, DOWN, buff=0.28)
        self.play(Write(quote, run_time=1.0))
        self.wait(0.30)

        # ── ROADMAP — all 5 light up ───────────────────────────
        r_line, r_dots, roadmap = _make_roadmap_animated()
        self.play(FadeIn(r_line, run_time=0.25))
        self.add(r_dots)

        # Light each dot with its part color
        for i, (dot, color) in enumerate(zip(r_dots, PART_COLORS)):
            self.play(
                dot.animate(run_time=0.22)
                   .set_fill(color, 1.0)
                   .set_stroke(color, width=1.8),
                Flash(dot.get_center(), color=color,
                      flash_radius=0.25, num_lines=7, run_time=0.25),
            )

        # ALL → GOLD simultaneously
        self.play(
            AnimationGroup(*[
                dot.animate(run_time=0.40).set_fill(GOLD, 1.0).set_stroke(GOLD, 2.0)
                for dot in r_dots
            ]),
            Flash(roadmap.get_center(), color=GOLD,
                  flash_radius=1.5, num_lines=14, run_time=0.50),
        )

        # Gold connection line through all dots
        connect = Line(
            r_dots[0].get_center(), r_dots[-1].get_center(),
            stroke_color=GOLD_GLOW, stroke_width=1.8, stroke_opacity=0.70,
        )
        self.play(Create(connect, run_time=0.65, rate_func=smooth))
        self.wait(2.0)

        # ── Fade out ──────────────────────────────────────────
        all_m = [super_t, title_grp, presenter, sep, quote,
                 r_line, r_dots, connect]
        self.play(
            LaggedStart(*[FadeOut(m, run_time=0.40) for m in all_m],
                        lag_ratio=0.06),
        )
        self.wait(0.2)
