"""P02-S02a - 1.19 million traffic deaths counter."""
from manimlib import *

from studio.components import (
    StudioScene,
    BG_CARD,
    FONT_PRIMARY,
    GOLD_RICH,
    INK_DARK,
    INK_MID,
    RED_ERROR,
    SIZE_BODY,
    SIZE_HERO,
    SIZE_LABEL,
)
from studio.scenes.part02._p02_helpers import person_grid


SCRIPT = "Every year, 1.19 million people die in traffic."


class P02S02A119M(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Why This Matters"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2020/covid.py:205
        grid = person_grid(rows=8, cols=14)
        grid.scale(0.98)
        grid.set_opacity(0.42)

        grid_panel = RoundedRectangle(
            width=grid.get_width() + 0.55,
            height=grid.get_height() + 0.55,
            corner_radius=0.14,
            fill_color=BG_CARD,
            fill_opacity=1.0,
            stroke_color=RED_ERROR,
            stroke_width=2.0,
            stroke_opacity=0.8,
        )
        grid_group = VGroup(grid_panel, grid).move_to(LEFT * 3.15 + DOWN * 0.05)
        grid.move_to(grid_panel)

        number = Text("1,190,000", font=FONT_PRIMARY, font_size=SIZE_HERO, color=RED_ERROR, weight=BOLD)
        number.set_color(RED_ERROR)
        label = Text("people die in traffic\neach year", font=FONT_PRIMARY, font_size=SIZE_BODY, color=INK_DARK, weight=BOLD)
        label.next_to(number, DOWN, buff=0.28)
        stat = VGroup(number, label).move_to(RIGHT * 2.55 + UP * 0.05)

        y = grid_panel.get_center()[1]
        connector = Line(
            [grid_panel.get_right()[0] + 0.2, y, 0],
            [number.get_left()[0] - 0.2, y, 0],
            stroke_color=RED_ERROR,
            stroke_width=2.0,
            stroke_opacity=0.55,
        )
        connector.set_z_index(-1)

        self.play(FadeIn(grid_panel), LaggedStart(*(FadeIn(i) for i in grid), lag_ratio=0.008), run_time=0.9)
        self.play(ShowCreation(connector), FadeIn(number, shift=UP * 0.12), run_time=0.7)
        self.play(Flash(number, color=RED_ERROR, line_length=0.22, num_lines=12, flash_radius=0.9), run_time=0.45)
        self.play(FadeIn(label), run_time=0.45)

        sub = Text("Safety at scale needs systems, not isolated agents.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        sub.to_edge(DOWN, buff=0.74)
        self.play(FadeIn(sub))
        self.wait(0.8)
        self._close()
