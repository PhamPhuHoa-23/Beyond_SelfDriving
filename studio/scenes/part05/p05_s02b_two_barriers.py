"""P05-S02b Two Barriers."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, ACCENT_PINK, GOLD_RICH, INK_DARK, INK_MID, INK_LIGHT,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL,
)
SCRIPT = """Two barriers. No data at internet scale. No model of human behavior."""


class P05S02BTwoBarriers(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Two Barriers"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        b1_title = Text("Barrier 1", font=FONT_PRIMARY, font_size=SIZE_H1, color=RED_ERROR, weight=BOLD)
        b1_body = Text("No web-scale robot data", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        b1 = VGroup(b1_title, b1_body).arrange(DOWN, buff=0.15).move_to(LEFT * 2.5 + UP * 0.5)
        b2_title = Text("Barrier 2", font=FONT_PRIMARY, font_size=SIZE_H1, color=RED_ERROR, weight=BOLD)
        b2_body = Text("No human behavior model — no alive simulations.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        b2 = VGroup(b2_title, b2_body).arrange(DOWN, buff=0.15).move_to(RIGHT * 2.5 + UP * 0.3)
        self.play(FadeIn(b1[0]), FadeIn(b1[1]))
        # Mini zombie-city preview: grid agents all moving in straight lines.
        zombies = VGroup()
        for r in range(4):
            for c in range(6):
                z = Square(side_length=0.25, fill_color=INK_MID, fill_opacity=0.9, stroke_width=0)
                z.move_to(LEFT * 2.2 + RIGHT * c * 0.42 + DOWN * (1.15 + r * 0.38))
                zombies.add(z)
        self.play(FadeIn(zombies))
        self.play(*(z.animate(run_time=0.8, rate_func=linear).shift(RIGHT * 0.45) for z in zombies))
        dead_lbl = Text("No personality. No interaction. No life.",
                        font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_LIGHT)
        dead_lbl.next_to(zombies, DOWN, buff=0.28)
        self.play(FadeIn(dead_lbl))
        self.play(FadeIn(b2[0]), FadeIn(b2[1]))
        self.wait(2)
        self._close()
