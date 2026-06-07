"""P03-S14 Part 3 Summary: 4 contribution badges."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_GREEN, GOLD_KEY, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL,
    contribution_badge,
)
SCRIPT = """Four contributions: real smart intersection, calibration, real-time fusion, digital twin."""


class P03S14Summary(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Part 3 Contributions"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        contribs = [
            ("UCLA Smart Intersection  ·  Real deployment", ACCENT_GREEN),
            ("Time + Space Calibration  ·  83cm -> cm", "#0891B2"),
            ("CooperFuse  ·  Gaussian fusion beats NMS", ACCENT_GREEN),
            ("OpenCDA Digital Twin  ·  100ms real-time", GOLD_KEY),
        ]
        badges = VGroup()
        for txt, color in contribs:
            badges.add(contribution_badge(txt, color=color))
        badges.arrange(DOWN, buff=0.35)
        badges.move_to(ORIGIN + UP * 0.2)
        self.play(LaggedStart(*(FadeIn(b, shift=RIGHT * 0.2) for b in badges), lag_ratio=0.25))
        self.wait(2)
        self._close()
