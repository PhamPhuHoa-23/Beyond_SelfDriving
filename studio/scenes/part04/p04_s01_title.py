"""P04-S01 Part 4 Title Card."""
from manimlib import *
from studio.components import (
    StudioScene, BG_TITLECARD, ACCENT_AMBER, GOLD_RICH, INK_LIGHT,
    FONT_PRIMARY, SIZE_CAPS, SIZE_LABEL, write_chiseled,
)
SCRIPT = """Part 4: From Pre-Training to Post-Training — with Seth Zhao."""


class P04S01Title(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "From Pre-Training to Post-Training"

    def construct(self):
        self.camera.background_color = BG_TITLECARD
        part_tag = Text("Part 04", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_AMBER)
        part_tag.set_color(ACCENT_AMBER)
        part_tag.to_corner(UR, buff=0.4)
        self.play(FadeIn(part_tag))
        line1 = Text("From Pre-Training", font=FONT_PRIMARY, font_size=52, color=ACCENT_AMBER, weight=BOLD)
        line2 = Text("to Post-Training", font=FONT_PRIMARY, font_size=44, color=GOLD_RICH)
        line1.set_color(ACCENT_AMBER)
        line2.set_color(GOLD_RICH)
        title = VGroup(line1, line2).arrange(DOWN, buff=0.2).move_to(UP * 0.5)
        self.play(LaggedStart(write_chiseled(line1, run_time=1.8), write_chiseled(line2, run_time=1.5), lag_ratio=0.5))
        speaker = Text("Seth Z. Zhao  ·  UCLA Mobility Lab", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        speaker.set_color(INK_LIGHT)
        speaker.next_to(title, DOWN, buff=0.45)
        self.play(FadeIn(speaker))
        quote = Text('"A system that cannot run real-time is a demo."',
                     font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        quote.set_color(GOLD_RICH)
        quote.next_to(speaker, DOWN, buff=0.4)
        self.play(write_chiseled(quote, run_time=2.0))
        roadmap = self._roadmap_strip()
        self.play(FadeIn(roadmap))
        self.wait(2)
        self._close()
