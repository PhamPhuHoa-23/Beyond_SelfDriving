"""P02-S02b - 94 percent human error and 80 percent injury reduction."""
from manimlib import *

from studio.components import (
    StudioScene,
    FONT_PRIMARY,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    ACCENT_TEAL,
    RED_ERROR,
    SIZE_BODY,
    SIZE_H1,
    SIZE_LABEL,
    axes_deploy,
    chart_mount,
    bar_reveal,
)
from studio.scenes.part02._p02_helpers import person_grid


SCRIPT = "94 percent are human error; Waymo reports 80 percent fewer injury crashes."


class P02S02BWaymoReduce(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Human Error, Machine Gains"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2020/covid.py:723
        grid = person_grid(rows=8, cols=12)
        grid.scale(0.98)
        grid.move_to(LEFT * 3.45 + DOWN * 0.25)
        self.play(LaggedStart(*(FadeIn(i) for i in grid), lag_ratio=0.01, run_time=1.2))

        red_icons = grid[:90]
        green_icons = grid[90:]
        self.play(LaggedStart(*(i.animate.set_color(RED_ERROR) for i in red_icons), lag_ratio=0.01, run_time=1.0))
        label_94 = Text("94%\nhuman error", font=FONT_PRIMARY, font_size=SIZE_H1, color=RED_ERROR, weight=BOLD)
        label_94.move_to(LEFT * 0.8 + UP * 1.25)
        self.play(FadeIn(label_94, shift=LEFT * 0.1))

        axes, axes_anim = axes_deploy((0, 2, 1), (0, 100, 25), width=4.7, height=3.2, with_tick_labels=False)
        tick_labels = chart_mount(axes, position=RIGHT * 3.25 + DOWN * 0.25, scale=0.9)
        bars = VGroup()
        bar_labels = VGroup()
        for x, value, color, name in [(0.55, 100, RED_ERROR, "Human"), (1.45, 20, GREEN_FIX, "Waymo AV")]:
            bottom = axes.c2p(x, 0)
            top = axes.c2p(x, value)
            bar = Rectangle(
                width=0.46,
                height=abs(top[1] - bottom[1]),
                fill_color=color,
                fill_opacity=0.88,
                stroke_color=INK_DARK,
                stroke_width=1.2,
            )
            bar.move_to((bottom + top) / 2)
            lbl = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID, weight=BOLD)
            lbl.next_to(axes.c2p(x, 0), DOWN, buff=0.18)
            bars.add(bar)
            bar_labels.add(lbl)
        chart_data = VGroup(bars, bar_labels)
        reduction = Text("-80%\ninjury crashes", font=FONT_PRIMARY, font_size=SIZE_H1, color=GREEN_FIX, weight=BOLD)
        reduction.next_to(axes, UP, buff=0.12)
        self.play(
            red_icons.animate.set_color(RED_ERROR).set_opacity(0.82),
            green_icons.animate.set_color(GREEN_FIX).scale(1.15),
            axes_anim,
            FadeIn(tick_labels),
            LaggedStart(*(GrowFromEdge(b, DOWN) for b in bars), lag_ratio=0.16),
            FadeIn(bar_labels),
            FadeIn(reduction),
            run_time=1.4,
        )

        footer = Text("Autonomy helps, but line of sight still limits any single car.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        footer.to_edge(DOWN, buff=0.72)
        self.play(FadeIn(footer))
        self.wait(0.8)
        self._close()
