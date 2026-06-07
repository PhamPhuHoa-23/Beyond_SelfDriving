"""I-01 - Title Card: particle burst -> wordmark forge."""
import random

from manimlib import *
from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    BG_TITLECARD,
    CYAN_RADAR,
    GOLD_RICH,
    INK_DARK,
    PURPLE_MODEL,
    FONT_PRIMARY,
    SIZE_LABEL,
)

SCRIPT = """
Beyond Self-Driving. An ICCV 2025 tutorial from UCLA Mobility Lab.
"""


class I01TitleCard(StudioScene):
    PART_NUM = 0
    SCENE_TITLE = "Beyond Self-Driving"

    def construct(self):
        self.camera.background_color = BG_TITLECARD

        palette = [CYAN_RADAR, GOLD_RICH, ACCENT_BLUE, PURPLE_MODEL, INK_DARK]
        particles = VGroup()
        trails = VGroup()
        for _ in range(200):
            p_color = random.choice(palette)
            p = Dot(radius=0.055, fill_color=p_color, fill_opacity=1.0, stroke_width=0)
            p.set_color(p_color)
            p.move_to(ORIGIN)
            particles.add(p)
            trails.add(TracedPath(
                p.get_center,
                stroke_color=p.get_color(),
                stroke_width=2.2,
                stroke_opacity=[0, 0.9],
                time_traced=0.42,
            ))
        self.add(trails, particles)

        burst_anims = []
        for p in particles:
            angle = random.uniform(0, TAU)
            radius = random.uniform(1.5, 5.8)
            dest = radius * np.array([np.cos(angle), np.sin(angle), 0])
            burst_anims.append(
                p.animate(run_time=1.5, rate_func=rush_from).move_to(dest)
            )
        self.play(AnimationGroup(*burst_anims))
        self.play(FadeOut(particles, run_time=0.35), FadeOut(trails, run_time=0.35))
        self.remove(trails, particles)

        wordmark = Text(
            "BEYOND SELF-DRIVING",
            font=FONT_PRIMARY,
            font_size=80,
            color=INK_DARK,
            weight=BOLD,
        )
        wordmark.move_to(ORIGIN + UP * 0.35)
        self.play(Write(wordmark, run_time=3.0, lag_ratio=0.025))
        self.play(wordmark.animate.set_color(GOLD_RICH), run_time=0.8)

        subtitle = Text(
            "ICCV 2025 Tutorial  |  UCLA Mobility Lab",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=INK_DARK,
        )
        subtitle.next_to(wordmark, DOWN, buff=0.35)
        rule = Line(LEFT * 4.5, RIGHT * 4.5, stroke_color=GOLD_RICH, stroke_width=0.8)
        rule.next_to(subtitle, DOWN, buff=0.25)
        speakers = Text(
            "Zhiyu Huang  |  Zewei Zhou  |  Zhaoliang Zheng  |  Seth Zhao  |  Wayne Wu",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL + 2,
            color=INK_DARK,
        )
        speakers.next_to(rule, DOWN, buff=0.2)
        title_group = VGroup(wordmark, subtitle, rule, speakers)

        self.play(FadeIn(subtitle, shift=UP * 0.2, run_time=0.8))
        self.play(ShowCreation(rule, run_time=0.6))
        self.play(FadeIn(speakers, run_time=0.8))
        self.wait(1.5)

        self.play(
            title_group.animate.set_opacity(0),
            run_time=1.2,
        )
