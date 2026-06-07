"""P05-S06a CityWalker Dataset."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, BG_CARD, ACCENT_PINK, ACCENT_AMBER, ACCENT_BLUE, ACCENT_GREEN,
    GOLD_RICH, GOLD_KEY, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    key_number, pedestrian_icon,
)
SCRIPT = """CityWalker captures pedestrian behavior in context — 30 hours, 120K pedestrians, 227 cities."""


class P05S06ACityWalker(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "CityWalker Dataset"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # World map dots — simplified as ellipse + scattered dots
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/spheres_talk/random_puzzles.py:18 DotHistory
        map_bg = Ellipse(width=9.5, height=4.5, fill_color=BG_CARD, fill_opacity=0.6, stroke_color="#CBD5E1", stroke_width=1.5)
        map_bg.move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(map_bg))
        rng = np.random.RandomState(42)
        dot_colors = [ACCENT_PINK, ACCENT_AMBER, ACCENT_BLUE, ACCENT_GREEN]
        city_dots = VGroup()
        dot_idx = 0
        for _ in range(60):
            x = rng.uniform(-4.5, 4.5)
            y = rng.uniform(-1.8, 1.8)
            if x**2 / 20.25 + y**2 / 5.0625 < 1:
                d = Dot(radius=0.08)
                d.set_fill(dot_colors[dot_idx % len(dot_colors)], opacity=0.9)
                d.set_stroke(width=0)
                d.move_to(np.array([x, y + 0.3, 0]))
                city_dots.add(d)
                dot_idx += 1
        self.play(LaggedStart(*(FadeIn(d, scale=0.3) for d in city_dots), lag_ratio=0.03, run_time=1.5))
        kns = VGroup(
            key_number("30h", "video captured", color=GOLD_RICH),
            key_number("120K", "pedestrians", color=GOLD_RICH),
            key_number("227", "cities worldwide", color=GOLD_RICH),
        )
        kns.arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.4)
        self.play(LaggedStart(*(FadeIn(k, scale=1.1) for k in kns), lag_ratio=0.2))
        self.wait(2)
        self._close()
