
# beyond/scenes/part04/p04_s01_title.py
# ─────────────────────────────────────────────────────────────────
# P4-01  TITLE CARD — EFFICIENT V2X  (~25s)
# Amber bùng lên như ánh lửa điện. Forge nhanh hơn các part trước.
# Render:  manim -ql "beyond/scenes/part04/p04_s01_title.py" P04S01Title
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components.colors import (
    BG_VOID, P4_EFFICIENT, GOLD, GOLD_GLOW,
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
    return VGroup(line, dots).move_to(DOWN*3.05)


class P04S01Title(Scene):
    def setup(self):
        self.camera.background_color = BG_VOID

    def construct(self):
        # Amber spark burst — faster, electric feel
        sparks = VGroup(*[
            Line(ORIGIN, np.array([np.cos(a)*1.5, np.sin(a)*1.5, 0]),
                 stroke_color=P4_EFFICIENT, stroke_width=1.8,
                 stroke_opacity=0.8)
            for a in np.linspace(0, TAU, 16, endpoint=False)
        ])
        self.add(sparks)
        self.play(
            sparks.animate(run_time=0.40, rate_func=rush_from)
                  .scale(5.0).set_stroke(opacity=0),
        )
        self.remove(sparks)

        super_t = Text("Part  04", font_size=SIZE_MICRO+2, color=TEXT_DIM, font=FONT_PRIMARY)
        super_t.to_corner(UR, buff=0.55)
        self.play(FadeIn(super_t, shift=DOWN*0.08, run_time=0.25))

        lines_txt = [
            "From Pre-Training to Post-Training:",
            "Building an Efficient",
            "V2X Cooperative Perception System",
        ]
        line_mobs = [
            Text(t, font_size=SIZE_HERO - (0 if i==0 else 4),
                 color="#FFFDE7", font=FONT_PRIMARY, weight=BOLD)
            for i, t in enumerate(lines_txt)
        ]
        tg = VGroup(*line_mobs).arrange(DOWN, buff=0.12)
        for ln in line_mobs:
            if ln.width > 12.8: ln.scale(12.8/ln.width)
        tg.arrange(DOWN, buff=0.12).move_to(UP*1.0)

        # Fast forge
        for ln in line_mobs:
            self.play(AddTextLetterByLetter(ln, run_time=0.6, rate_func=linear))
        self.play(
            *[ln.animate(run_time=0.35).set_color(P4_EFFICIENT) for ln in line_mobs],
            LaggedStart(*[Flash(ch.get_center(), color=GOLD_GLOW,
                               flash_radius=0.10, num_lines=3, run_time=0.12)
                         for ch in list(line_mobs[0])], lag_ratio=0.01),
            run_time=0.40,
        )
        self.wait(0.2)

        presenter = Text("Seth Z. Zhao  ·  UCLA Mobility Lab",
                         font_size=SIZE_LABEL, color=TEXT_DIM, font=FONT_PRIMARY)
        presenter.next_to(tg, DOWN, buff=0.40)
        self.play(FadeIn(presenter, shift=UP*0.08, run_time=0.35))

        sep = Line(LEFT*4.5, RIGHT*4.5, stroke_color=P4_EFFICIENT,
                   stroke_width=0.8, stroke_opacity=0.40)
        sep.next_to(presenter, DOWN, buff=0.22)
        self.play(Create(sep, run_time=0.32))

        quote = Text(
            '"A system that cannot run in real-time\n  is not a system — it\'s a demo."',
            font_size=SIZE_MICRO+3, color=TEXT_WHITE,
            font=FONT_PRIMARY, slant=ITALIC, line_spacing=0.42,
        )
        quote.next_to(sep, DOWN, buff=0.25)
        self.play(Write(quote, run_time=1.0))
        self.wait(0.15)

        roadmap = _roadmap(4)
        self.play(FadeIn(roadmap, run_time=0.32))
        self.play(Flash(roadmap[1][3].get_center(), color=P4_EFFICIENT,
                        flash_radius=0.28, num_lines=8, run_time=0.35))

        self.wait(2.2)
        all_m = [super_t, tg, presenter, sep, quote, roadmap]
        self.play(LaggedStart(*[FadeOut(m, run_time=0.35) for m in all_m],
                              lag_ratio=0.06))
        self.wait(0.15)
