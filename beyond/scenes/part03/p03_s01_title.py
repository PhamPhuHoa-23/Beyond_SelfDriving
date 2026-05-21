# beyond/scenes/part03/p03_s01_title.py
# ─────────────────────────────────────────────────────────────────
# P3-01  TITLE CARD — SIM TO REALITY  (~25s)
# Render:  manim -ql "beyond/scenes/part03/p03_s01_title.py" P03S01Title
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components.colors import (
    BG_VOID, P3_SIM, GOLD, GOLD_GLOW,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_HERO, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)


def _roadmap(current):
    colors = ["#7986CB", "#00BCD4", "#4CAF50", "#FFC107", "#F06292"]
    sp = 1.1
    line = Line(LEFT*sp*2, RIGHT*sp*2, stroke_color=TEXT_GHOST, stroke_width=1.2)
    dots = VGroup(*[
        Circle(radius=0.11,
               fill_color=colors[i] if i+1==current else TEXT_GHOST,
               fill_opacity=1.0 if i+1==current else 0.35,
               stroke_color=colors[i] if i+1==current else TEXT_DIM,
               stroke_width=1.4).move_to([(i-2)*sp, 0, 0])
        for i in range(5)
    ])
    return VGroup(line, dots).move_to(DOWN * 3.05)


class P03S01Title(Scene):
    def setup(self):
        self.camera.background_color = BG_VOID

    def construct(self):
        # Green wave burst
        rings = [Circle(radius=0.08*(i+1), stroke_color=P3_SIM,
                        stroke_width=max(0.4, 2.8-i*0.5),
                        stroke_opacity=max(0, 0.9-i*0.14), fill_opacity=0)
                 for i in range(7)]
        [self.add(r) for r in rings]
        self.play(LaggedStart(*[
            r.animate(run_time=0.8, rate_func=rush_from).scale(20+i*5).set_stroke(opacity=0)
            for i, r in enumerate(rings)
        ], lag_ratio=0.07), run_time=0.85)
        [self.remove(r) for r in rings]

        super_t = Text("Part  03", font_size=SIZE_MICRO+2, color=TEXT_DIM, font=FONT_PRIMARY)
        super_t.to_corner(UR, buff=0.55)
        self.play(FadeIn(super_t, shift=DOWN*0.08, run_time=0.28))

        l1 = Text("Bridging Simulation", font_size=SIZE_HERO, color="#FFFDE7",
                  font=FONT_PRIMARY, weight=BOLD)
        l2 = Text("and Reality in V2X", font_size=SIZE_HERO-4, color="#FFFDE7",
                  font=FONT_PRIMARY, weight=BOLD)
        tg = VGroup(l1, l2).arrange(DOWN, buff=0.14)
        for ln in (l1, l2):
            if ln.width > 12.5: ln.scale(12.5/ln.width)
        tg.arrange(DOWN, buff=0.14).move_to(UP*1.3)

        self.play(AddTextLetterByLetter(l1, run_time=1.2, rate_func=linear))
        self.play(AddTextLetterByLetter(l2, run_time=1.0, rate_func=linear))
        self.play(
            l1.animate(run_time=0.40).set_color(P3_SIM),
            l2.animate(run_time=0.40).set_color(P3_SIM),
            LaggedStart(*[Flash(ch.get_center(), color=P3_SIM,
                               flash_radius=0.12, num_lines=4, run_time=0.14)
                         for ch in list(l1)+list(l2)], lag_ratio=0.02),
            run_time=0.55,
        )
        self.wait(0.2)

        presenter = Text("Zhaoliang Zheng  ·  UCLA Mobility Lab",
                         font_size=SIZE_LABEL, color=TEXT_DIM, font=FONT_PRIMARY)
        presenter.next_to(tg, DOWN, buff=0.45)
        self.play(FadeIn(presenter, shift=UP*0.10, run_time=0.38))

        sep = Line(LEFT*4.2, RIGHT*4.2, stroke_color=P3_SIM,
                   stroke_width=0.8, stroke_opacity=0.40)
        sep.next_to(presenter, DOWN, buff=0.25)
        self.play(Create(sep, run_time=0.35))

        quote = Text('"Theory without deployment\n is just fiction."',
                     font_size=SIZE_MICRO+4, color=TEXT_WHITE,
                     font=FONT_PRIMARY, slant=ITALIC, line_spacing=0.45)
        quote.next_to(sep, DOWN, buff=0.28)
        self.play(Write(quote, run_time=1.0))
        self.wait(0.15)

        roadmap = _roadmap(3)
        self.play(FadeIn(roadmap, run_time=0.35))
        self.play(Flash(roadmap[1][2].get_center(), color=P3_SIM,
                        flash_radius=0.28, num_lines=8, run_time=0.38))

        self.wait(2.2)
        all_m = [super_t, tg, presenter, sep, quote, roadmap]
        self.play(LaggedStart(*[FadeOut(m, run_time=0.38) for m in all_m],
                              lag_ratio=0.06))
        self.wait(0.15)
