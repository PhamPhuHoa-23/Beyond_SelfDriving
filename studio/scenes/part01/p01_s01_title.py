"""P01-S01 — Part 1 Title Card."""
from manimlib import *
from studio.components import (
    StudioScene,
    BG_TITLECARD, GOLD_RICH, INK_LIGHT, ACCENT_BLUE,
    FONT_PRIMARY, SIZE_HERO, SIZE_LABEL, SIZE_CAPS,
    forge_text, dust_dissolve,
)

SCRIPT = """
Part 1: Foundation Models for Autonomous Driving — with Dr. Zhiyu Huang.
"""


class P01S01Title(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Foundation Models for AV"

    def construct(self):
        self.camera.background_color = BG_TITLECARD

        # Part label top right
        part_tag = Text("Part 01", font=FONT_PRIMARY, font_size=SIZE_CAPS,
                        color=ACCENT_BLUE)
        part_tag.set_color(ACCENT_BLUE)
        part_tag.to_corner(UR, buff=0.4)
        self.play(FadeIn(part_tag))

        # Title forge white-hot -> indigo
        # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/logo.py:211 WrittenLogo
        line1 = Text("Foundation Models", font=FONT_PRIMARY, font_size=56,
                     color=GOLD_RICH, weight=BOLD)
        line2 = Text("for Autonomous Driving", font=FONT_PRIMARY, font_size=44,
                     color=GOLD_RICH)
        line1.set_color(GOLD_RICH)
        line2.set_color(GOLD_RICH)
        title = VGroup(line1, line2).arrange(DOWN, buff=0.2)
        title.move_to(UP * 0.85)

        self.play(
            LaggedStart(
                write_chiseled(line1, run_time=1.8),
                write_chiseled(line2, run_time=1.5),
                lag_ratio=0.6,
            )
        )

        # Speaker + quote
        speaker = Text("Dr. Zhiyu Huang  ·  UCLA Mobility Lab",
                       font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        speaker.set_color(INK_LIGHT)
        speaker.next_to(title, DOWN, buff=0.45)
        self.play(FadeIn(speaker))

        quote = Text(
            '"Why, in 2025, can AI write code, draw art, answer anything\n'
            '— yet self-driving cars still can\'t go everywhere?"',
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH,
        )
        quote.set_color(GOLD_RICH)
        quote.scale(0.92)
        quote.next_to(speaker, DOWN, buff=0.32)
        self.play(write_chiseled(quote, run_time=2.5))

        # Roadmap strip P1 lit
        roadmap = self._roadmap_strip()
        roadmap.move_to(DOWN * 2.25)
        self.play(FadeIn(roadmap))

        self.wait(2)
        self._close()


from studio.components.animations import write_chiseled  # noqa: E402
