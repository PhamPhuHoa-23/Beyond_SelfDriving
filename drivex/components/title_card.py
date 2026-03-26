# drivex/components/title_card.py
# ─────────────────────────────────────────────────────────────────
# Reusable part-title card template.
# Returns a VGroup containing all elements for a part title scene.
#
# Usage (in a Scene):
#   card = make_part_title_card(
#       part_num=2,
#       title="Towards End-to-End\nCooperative Automation",
#       speaker="Zewei Zhou, UCLA Mobility Lab",
#   )
#   self.play(card.build_animation())
# ─────────────────────────────────────────────────────────────────

from manim import *
from .colors import (COL_NAVY, COL_BLUE, COL_GOLD,
                     COL_WHITE, COL_LIGHT_BLUE, BG_DARK)
from .roadmap import RoadmapStrip


class PartTitleCard(VGroup):
    """
    Full-screen part title card.

    Parameters
    ----------
    part_num : int 1–5
    title    : part title string (newlines allowed)
    speaker  : speaker credit line
    callback_quote : optional one-liner quote from previous part
    """

    def __init__(
        self,
        part_num: int,
        title: str,
        speaker: str,
        callback_quote: str = "",
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Watermark part number
        watermark = Text(
            f"0{part_num}",
            font_size=160,
            color=COL_GOLD,
            weight=BOLD,
        ).set_opacity(0.08).move_to(ORIGIN)

        # Title
        title_mob = Text(
            title, font_size=38, color=COL_WHITE, weight=BOLD
        ).center().shift(UP * 0.8)

        # Speaker
        speaker_mob = Text(
            speaker, font_size=20, color=COL_LIGHT_BLUE
        ).next_to(title_mob, DOWN, buff=0.4)

        # Divider
        divider = Line(LEFT * 4.5, RIGHT * 4.5,
                       stroke_color=COL_BLUE, stroke_width=2)
        divider.next_to(speaker_mob, DOWN, buff=0.35)

        # Callback quote (optional)
        self.quote_mob = None
        if callback_quote:
            self.quote_mob = Text(
                f'"{callback_quote}"',
                font_size=20, color=COL_WHITE, slant=ITALIC
            ).set_opacity(0.8).next_to(divider, DOWN, buff=0.35)

        # Roadmap mini-strip at bottom
        roadmap = RoadmapStrip(current_part=part_num, mini=True)
        roadmap.to_edge(DOWN, buff=0.35)

        self.watermark = watermark
        self.title_mob = title_mob
        self.speaker_mob = speaker_mob
        self.divider = divider
        self.roadmap = roadmap

        elements = [watermark, title_mob, speaker_mob, divider]
        if self.quote_mob:
            elements.append(self.quote_mob)
        elements.append(roadmap)
        self.add(*elements)

    def build_animation(self) -> AnimationGroup:
        """Sequenced entrance animation for all card elements."""
        anims = [
            FadeIn(self.watermark, run_time=0.4),
            Write(self.title_mob, run_time=1.0),
            FadeIn(self.speaker_mob, shift=UP * 0.1, run_time=0.4),
            Create(self.divider, run_time=0.4),
        ]
        if self.quote_mob:
            anims.append(FadeIn(self.quote_mob, run_time=0.5))
        anims.append(FadeIn(self.roadmap, run_time=0.5))
        return Succession(*anims, lag_ratio=0.5)


def make_part_title_card(part_num: int, title: str,
                         speaker: str, callback_quote: str = "") -> PartTitleCard:
    """Factory shortcut."""
    return PartTitleCard(part_num, title, speaker, callback_quote)
