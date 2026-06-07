"""P05-S01 Part 5 Title — all 5 roadmap nodes light up simultaneously."""
from manimlib import *
from studio.components import (
    StudioScene, BG_TITLECARD, ACCENT_PINK, GOLD_RICH, INK_LIGHT,
    ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER,
    FONT_PRIMARY, SIZE_CAPS, SIZE_LABEL, write_chiseled,
)
SCRIPT = """Part 5: Scalable, Human-Centric Physical AI — with Wayne Wu. Beyond cars — to any agent, any space."""


class P05S01Title(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Scalable Human-Centric Physical AI"

    def construct(self):
        self.camera.background_color = BG_TITLECARD
        part_tag = Text("Part 05", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_PINK)
        part_tag.set_color(ACCENT_PINK)
        part_tag.to_corner(UR, buff=0.4)
        self.play(FadeIn(part_tag))
        line1 = Text("Scalable,", font=FONT_PRIMARY, font_size=48, color=ACCENT_PINK, weight=BOLD)
        line2 = Text("Human-Centric Physical AI", font=FONT_PRIMARY, font_size=44, color=GOLD_RICH)
        line1.set_color(ACCENT_PINK)
        line2.set_color(GOLD_RICH)
        title = VGroup(line1, line2).arrange(DOWN, buff=0.15).move_to(UP * 0.5)
        self.play(LaggedStart(write_chiseled(line1, run_time=1.6), write_chiseled(line2, run_time=2.0), lag_ratio=0.5))
        speaker = Text("Wayne Wu  ·  UCLA Mobility Lab", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        speaker.set_color(INK_LIGHT)
        speaker.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(speaker))
        quote = Text('"Beyond cars — to any agent, any space."', font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        quote.set_color(GOLD_RICH)
        quote.next_to(speaker, DOWN, buff=0.35)
        self.play(write_chiseled(quote, run_time=2.0))
        # All 5 roadmap nodes light up simultaneously — first time in the video
        # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/logo.py:216 LogoGenerationFivefold
        part_colors = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK]
        roadmap = self._roadmap_strip()
        self.play(FadeIn(roadmap))
        # Override all dots to GOLD simultaneously
        dots = roadmap[0]
        self.play(AnimationGroup(*(d.animate.set_fill(GOLD_RICH) for d in dots), lag_ratio=0.0, run_time=0.8))
        self.play(LaggedStart(*(Flash(d, color=GOLD_RICH, line_length=0.18, num_lines=6) for d in dots), lag_ratio=0.1))
        self.wait(2)
        self._close()
