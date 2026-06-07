"""P04-S10 Bridge to Part 5."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL,
    write_chiseled,
)
SCRIPT = """Everything so far has been about cars. The world has robots, wheelchairs, scooters, and humans."""


class P04S10BridgeToP5(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Bridge to Part 5"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        recap = Text("Parts 2-4: all about cars.", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_MID)
        recap.move_to(UP * 0.8)
        self.play(FadeIn(recap))
        forward = Text(
            "But the world has delivery robots,\nwheelchairs, scooters —\nand the most unpredictable agent: humans.",
            font=FONT_PRIMARY, font_size=SIZE_H1, color=ACCENT_PINK,
        )
        forward.move_to(DOWN * 0.5)
        self.play(write_chiseled(forward, run_time=3.0))
        self.wait(1.5)
        self._close()
