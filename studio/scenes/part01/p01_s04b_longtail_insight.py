"""P01-S04b — Long-Tail Insight: dim overlay + chiseled quote."""
from manimlib import *
from studio.components import (
    StudioScene,
    BG_PAPER, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_BODY, SIZE_LABEL,
    write_chiseled, text,
)

SCRIPT = """
Why do humans handle these?
Contextual reasoning, common sense, a lifetime of experience.
That's what we need to teach the long tail.
"""


class P01S04BLongtailInsight(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Why Humans Handle It"

    def construct(self):
        header = self._open(self.SCENE_TITLE)

        # Dim overlay
        overlay = Rectangle(
            width=15, height=9,
            fill_color=BG_PAPER, fill_opacity=0.0, stroke_width=0,
        )
        self.add(overlay)

        # Three lines write-chiseled one by one
        # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/logo.py:211 WrittenLogo
        lines = [
            "Contextual reasoning.",
            "Common sense.",
            "A lifetime of experience.",
        ]
        line_mobs = VGroup()
        for line in lines:
            mob = Text(line, font=FONT_PRIMARY, font_size=SIZE_BODY, color=INK_MID)
            line_mobs.add(mob)
        line_mobs.arrange(DOWN, buff=0.35)
        line_mobs.move_to(UP * 0.5)

        for mob in line_mobs:
            self.play(write_chiseled(mob, run_time=1.0))
        self.wait(0.5)

        # Key insight gold large
        insight = Text(
            "We need generalist experience\nto handle the long tail.",
            font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH,
        )
        insight.next_to(line_mobs, DOWN, buff=0.55)
        self.play(write_chiseled(insight, run_time=2.5))
        self.wait(2.5)
        self._close()
