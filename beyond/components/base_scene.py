# beyond/components/base_scene.py
# ─────────────────────────────────────────────────────────────────
# BeyondScene — base class for all "Beyond Self-Driving" scenes.
# Handles: theme BG, ambient setup, scene_open / scene_close wrappers.
#
# Usage:
#   class MyScene(BeyondScene):
#       PART_COLOR = P2_COOP
#       def construct(self):
#           title, sep = self.open("Scene Title")
#           # ... animation ...
#           self.close()
# ─────────────────────────────────────────────────────────────────

from manim import *
from .colors import (
    BG_SPACE, BG_VOID, BG_PANEL,
    TEXT_WHITE, GOLD, CYAN_NEON,
    P1_FOUNDATION, P2_COOP, P3_SIM, P4_EFFICIENT, P5_PHYSICAL,
    SIZE_TITLE, SIZE_BODY, SIZE_LABEL, SIZE_HERO, SIZE_MICRO,
    FONT_PRIMARY,
    UCLA_BLUE, UCLA_GOLD,
    TEXT_DIM, TEXT_GHOST,
)
from .animations import (
    scene_open, scene_close, key_insight_reveal,
    setup_ambient_particles,
)


class BeyondScene(Scene):
    """
    Base for all body scenes. White or dark BG comes from colors.BG_SPACE.
    Subclass and set PART_COLOR to the part's accent color.
    """
    PART_COLOR: str = CYAN_NEON
    SHOW_AMBIENT: bool = True   # particle drift background

    def setup(self):
        self.camera.background_color = BG_SPACE
        self._ambient_particles = None

    def construct(self):
        raise NotImplementedError("Subclass must implement construct()")

    # ── convenience wrappers ─────────────────────────────────────

    def open(self, title: str) -> tuple:
        """3-beat scene open. Returns (title_mob, separator_mob)."""
        if self.SHOW_AMBIENT:
            self._ambient_particles = setup_ambient_particles(
                self, color=self.PART_COLOR
            )
        return scene_open(self, title, part_color=self.PART_COLOR)

    def close(self, keep: list = None) -> None:
        """Fade out everything, brief part-color flash."""
        if self._ambient_particles is not None:
            self._ambient_particles.clear_updaters()
        scene_close(self, part_color=self.PART_COLOR, keep=keep)

    def insight(self, text: str, hold: float = 2.0) -> None:
        """Key insight moment — dims scene, gold text, hold, restore."""
        key_insight_reveal(self, text, hold=hold)

    def wait_beat(self, short: bool = False) -> None:
        """Standard pause after a key moment."""
        self.wait(0.5 if short else 1.2)

    def fade_all(self, run_time: float = 0.5) -> None:
        """FadeOut every non-Background mobject."""
        targets = [m for m in self.mobjects
                   if not isinstance(m, BackgroundRectangle)]
        if targets:
            self.play(FadeOut(VGroup(*targets), run_time=run_time))


# ── Part title card ───────────────────────────────────────────────

class PartTitleCard(Scene):
    """
    Navy-background part transition card.
    Subclass and set:  PART_NUM, PART_TITLE, SPEAKER, TEASER, PART_COLOR.

    The 5-dot roadmap strip at bottom highlights the current part.
    """
    PART_NUM:   int = 1
    PART_TITLE: str = "Foundation Models"
    PART_SUBTITLE: str = "for Autonomous Driving"
    SPEAKER:    str = "Dr. Zhiyu Huang · UCLA"
    TEASER:     str = ""
    PART_COLOR: str = P1_FOUNDATION

    def setup(self):
        self.camera.background_color = BG_VOID

    def construct(self):
        # Super-title "Part 0X"
        super_title = Text(
            f"Part {self.PART_NUM:02d}",
            font_size=SIZE_LABEL, color=TEXT_DIM, font=FONT_PRIMARY,
        ).to_edge(UP, buff=0.9)

        # Main title
        main = Text(
            self.PART_TITLE,
            font_size=SIZE_HERO, color=GOLD,
            font=FONT_PRIMARY, weight=BOLD,
        )

        # Sub-title (optional)
        sub_mobs = []
        if self.PART_SUBTITLE:
            sub = Text(
                self.PART_SUBTITLE,
                font_size=SIZE_HERO, color=GOLD,
                font=FONT_PRIMARY, weight=BOLD,
            )
            grp = VGroup(main, sub).arrange(DOWN, buff=0.12)
            grp.move_to(ORIGIN + UP * 0.3)
            sub_mobs.append(sub)
        else:
            main.move_to(ORIGIN + UP * 0.3)

        # Speaker label
        speaker_mob = Text(
            self.SPEAKER,
            font_size=SIZE_LABEL, color=self.PART_COLOR, font=FONT_PRIMARY,
        ).next_to(main if not sub_mobs else sub_mobs[0], DOWN, buff=0.55)

        # Teaser line
        teaser_mob = None
        if self.TEASER:
            teaser_mob = Text(
                self.TEASER,
                font_size=SIZE_BODY - 2, color=TEXT_WHITE,
                font=FONT_PRIMARY, slant=ITALIC,
            ).next_to(speaker_mob, DOWN, buff=0.35)

        # 5-dot roadmap strip at bottom (dots only — no labels)
        strip = self._roadmap_strip()

        # Animate
        self.play(FadeIn(super_title, shift=DOWN * 0.1, run_time=0.35))
        self.play(Write(main, run_time=0.90))
        if sub_mobs:
            self.play(Write(sub_mobs[0], run_time=0.75))
        self.wait(0.2)
        self.play(FadeIn(speaker_mob, shift=UP * 0.08, run_time=0.40))
        if teaser_mob:
            self.play(FadeIn(teaser_mob, shift=UP * 0.05, run_time=0.40))
        self.play(FadeIn(strip, run_time=0.50))
        self.wait(1.8)

        all_mobs = [m for m in self.mobjects
                    if not isinstance(m, BackgroundRectangle)]
        self.play(FadeOut(VGroup(*all_mobs), run_time=0.55))
        self.wait(0.1)

    def _roadmap_strip(self) -> VGroup:
        total = 5
        spacing = 1.0
        total_w = spacing * (total - 1)
        line = Line(
            LEFT * total_w / 2, RIGHT * total_w / 2,
            stroke_color=TEXT_GHOST, stroke_width=1.4,
        )
        dots = VGroup()
        for i in range(total):
            x = -total_w / 2 + i * spacing
            is_current = (i + 1 == self.PART_NUM)
            d = Circle(
                radius=0.11,
                fill_color=GOLD if is_current else TEXT_GHOST,
                fill_opacity=1.0,
                stroke_color=GOLD if is_current else TEXT_DIM,
                stroke_width=1.4,
            ).move_to([x, 0, 0])
            dots.add(d)
        strip = VGroup(line, dots)
        strip.move_to([0, -3.0, 0])
        return strip
