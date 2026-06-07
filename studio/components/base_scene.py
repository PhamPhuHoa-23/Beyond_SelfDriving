"""StudioScene and Studio3DScene base classes with _open/_close/_roadmap_strip."""
from __future__ import annotations
from manimlib import *
from studio.components.colors import (
    ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK,
    PASTEL_BLUE, INK_DARK, INK_MID, PART_PALETTES, BG_PAPER,
)
from studio.components.typography import FONT_PRIMARY, SIZE_TITLE, SIZE_LABEL


class StudioScene(Scene):
    PART_NUM: int = 0
    PART_COLOR: str = ACCENT_BLUE
    PART_PASTEL: str = PASTEL_BLUE
    SCENE_TITLE: str = ""

    def setup(self) -> None:
        super().setup()
        palette = PART_PALETTES.get(self.PART_NUM, PART_PALETTES[0])
        self.PART_COLOR = palette["accent"]
        self.PART_PASTEL = palette["pastel"]
        self.camera.background_color = BG_PAPER
        self.camera.background_rgba = color_to_rgba(BG_PAPER)

    def _force_text_contrast(self, *items) -> None:
        """ManimGL Text ignores color= in this setup; prevent white-on-white text."""
        def visit(item) -> None:
            if isinstance(item, Animation):
                visit(item.mobject)
            elif isinstance(item, Mobject):
                if isinstance(item, Text) and str(item.get_color()).upper() == "#FFFFFF":
                    item.set_color(INK_DARK)
                for sm in item.submobjects:
                    visit(sm)

        for item in items:
            visit(item)

    def add(self, *new_mobjects: Mobject):
        self._force_text_contrast(*new_mobjects)
        return super().add(*new_mobjects)

    def play(self, *animations, **kwargs):
        self._force_text_contrast(*animations)
        return super().play(*animations, **kwargs)

    def _open(self, title: str | None = None) -> VGroup:
        """Create title bar + separator line; returns VGroup to FadeOut later."""
        t = title or self.SCENE_TITLE
        title_mob = Text(t, font=FONT_PRIMARY, font_size=SIZE_TITLE, color=INK_DARK)
        title_mob.to_edge(UP, buff=0.35)
        sep_glow = Line(
            LEFT * 6.5, RIGHT * 6.5,
            stroke_color=self.PART_COLOR, stroke_width=6,
            stroke_opacity=0.15,
        )
        sep_glow.next_to(title_mob, DOWN, buff=0.12)
        sep = Line(
            LEFT * 6.5, RIGHT * 6.5,
            stroke_color=self.PART_COLOR, stroke_width=2.0,
            stroke_opacity=0.85,
        )
        sep.move_to(sep_glow)
        header = VGroup(title_mob, sep_glow, sep)
        self.play(FadeIn(title_mob, shift=0.15 * DOWN, run_time=0.5))
        self.play(
            ShowCreation(sep, run_time=0.5),
            ShowCreation(sep_glow, run_time=0.5),
        )
        return header

    def _close(self, *extra: Mobject, fade_lag: float = 0.04) -> None:
        """FadeOut everything on screen plus extra. Always last call in construct."""
        targets = [m for m in self.mobjects] + list(extra)
        if targets:
            self.play(LaggedStart(
                *(FadeOut(m) for m in targets),
                lag_ratio=fade_lag,
                run_time=0.8,
            ))

    def _roadmap_strip(self) -> VGroup:
        """5-dot roadmap strip for part title cards; active dot = PART_COLOR."""
        dots = VGroup()
        labels = ["FM", "Coop", "Sim", "Eff", "PhysAI"]
        part_colors = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK]
        for i in range(5):
            active = i + 1 == self.PART_NUM
            color = part_colors[i] if active else INK_MID
            d = Circle(radius=0.1)
            d.set_fill(color, opacity=1.0)
            d.set_stroke(color, width=1.4, opacity=1.0)
            dots.add(d)
        dots.arrange(RIGHT, buff=1.0)
        dots.to_edge(DOWN, buff=0.35)
        lbl_group = VGroup()
        for i, (d, lbl) in enumerate(zip(dots, labels)):
            active = i + 1 == self.PART_NUM
            color = part_colors[i] if active else INK_MID
            t = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_LABEL, weight=BOLD if active else NORMAL)
            t.set_color(color)
            t.next_to(d, DOWN if i % 2 == 0 else UP, buff=0.12)
            lbl_group.add(t)
        return VGroup(dots, lbl_group)


class Studio3DScene(Scene):
    """3D variant — uses frame.reorient() for camera, phi=70 theta=-30 default."""
    PART_NUM: int = 0
    PART_COLOR: str = ACCENT_BLUE
    SCENE_TITLE: str = ""
    default_frame_orientation = (-30, 70)  # (theta_deg, phi_deg)

    def setup(self) -> None:
        super().setup()
        palette = PART_PALETTES.get(self.PART_NUM, PART_PALETTES[0])
        self.PART_COLOR = palette["accent"]
        self.camera.background_color = BG_PAPER
        self.camera.background_rgba = color_to_rgba(BG_PAPER)

    def _force_text_contrast(self, *items) -> None:
        """ManimGL Text ignores color= in this setup; prevent white-on-white text."""
        def visit(item) -> None:
            if isinstance(item, Animation):
                visit(item.mobject)
            elif isinstance(item, Mobject):
                if isinstance(item, Text) and str(item.get_color()).upper() == "#FFFFFF":
                    item.set_color(INK_DARK)
                for sm in item.submobjects:
                    visit(sm)

        for item in items:
            visit(item)

    def add(self, *new_mobjects: Mobject):
        self._force_text_contrast(*new_mobjects)
        return super().add(*new_mobjects)

    def play(self, *animations, **kwargs):
        self._force_text_contrast(*animations)
        return super().play(*animations, **kwargs)
