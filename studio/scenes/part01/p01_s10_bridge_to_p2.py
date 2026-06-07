"""P01-S10 — Bridge to Part 2: recap chip + forward gold question."""
from manimlib import *
from studio.components import (
    StudioScene,
    BG_PAPER, GOLD_RICH, ACCENT_TEAL, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL,
    contribution_badge, write_chiseled, place_footer,
)

SCRIPT = """
AutoVLA handles the long tail.
But even the smartest agent only sees what's in front of it.
"""


class P01S10BridgeToP2(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Bridge to Part 2"

    def construct(self):
        header = self._open(self.SCENE_TITLE)

        # Recap chip
        recap = Text("AutoVLA handles the long tail.", font=FONT_PRIMARY,
                     font_size=SIZE_LABEL, color=INK_MID)
        bg = RoundedRectangle(
            width=recap.get_width() + 0.5, height=recap.get_height() + 0.2,
            corner_radius=0.1, fill_color=BG_PAPER, fill_opacity=1.0,
            stroke_color=INK_MID, stroke_width=1.2,
        )
        recap.move_to(bg)
        recap_card = VGroup(bg, recap)
        recap_card.move_to(UP * 0.8)
        self.play(FadeIn(recap_card))

        # Forward question gold
        forward = Text(
            "But even the smartest agent\nonly sees what's in front of it.",
            font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH,
        )
        place_footer(forward)
        self.play(write_chiseled(forward, run_time=2.5))

        dot_p2 = Circle(radius=0.18, fill_color=ACCENT_TEAL, fill_opacity=1.0, stroke_width=0)
        dot_p2.next_to(forward, DOWN, buff=0.45)
        self.play(FadeIn(dot_p2))
        self.play(Flash(dot_p2, color=ACCENT_TEAL, line_length=0.25, num_lines=8))

        self.wait(1.5)
        self._close()


from studio.components.colors import BG_PAPER  # noqa: E402
