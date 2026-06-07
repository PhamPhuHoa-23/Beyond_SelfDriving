"""P05-S10 Chain of Solutions Montage — 5 vignettes."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK,
    GOLD_RICH, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_MICRO,
)
SCRIPT = """Five parts. Five solutions. One story."""


PART_SUMMARIES = [
    ("Part 1", "Foundation Models\nAutoVLA", ACCENT_BLUE),
    ("Part 2", "Cooperative\nV2XPnP", ACCENT_TEAL),
    ("Part 3", "Sim-to-Real\nCooperFuse", ACCENT_GREEN),
    ("Part 4", "Efficiency\nQuantV2X 300x", ACCENT_AMBER),
    ("Part 5", "Physical AI\nPedGen alive", ACCENT_PINK),
]


class P05S10ChainOfSolutions(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Five Parts, One Story"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        panels = VGroup()
        for part, summary, color in PART_SUMMARIES:
            bg = RoundedRectangle(width=2.0, height=3.2, corner_radius=0.15,
                                  fill_color=BG_PAPER, fill_opacity=1.0,
            stroke_color=color, stroke_width=2.5)
            title = Text(part, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
            body = Text(summary, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
            max_body_width = bg.get_width() - 0.3
            if body.get_width() > max_body_width:
                body.set_width(max_body_width)
            inner = VGroup(title, body).arrange(DOWN, buff=0.15)
            inner.move_to(bg)
            panels.add(VGroup(bg, inner))
        panels.arrange(RIGHT, buff=0.26).move_to(ORIGIN + DOWN * 0.2)
        self.play(LaggedStart(*(FadeIn(p, shift=DOWN * 0.5) for p in panels), lag_ratio=0.2, run_time=1.5))
        finale = Text("Five parts. Five solutions. One story.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        finale.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(finale, scale=1.05))
        self.wait(2)
        self._close()
