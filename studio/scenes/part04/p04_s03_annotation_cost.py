"""P04-S03 Annotation Cost Explosion."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_AMBER, ACCENT_GREEN,
    GOLD_RICH, INK_MID,
    FONT_PRIMARY, SIZE_CAPS,
    axes_deploy, bar_reveal, key_number, chart_mount,
)
SCRIPT = """Datasets have grown 5x in two years — but annotation cost grew with them."""


class P04S03AnnotationCost(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Annotation Cost Explosion"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # Shift chart slightly right so Y-axis label + tick numbers both fit on the left
        axes, axes_anim = axes_deploy((0, 4, 1), (0, 1.3, 0.25))
        tick_labels = chart_mount(axes, position=RIGHT * 0.4 + UP * 0.1, scale=0.85)
        y_lbl = Text("Annotations (M)", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID, weight=BOLD)
        y_lbl.rotate(90 * DEGREES)
        # next_to tick_labels group (not Y-axis) — guarantees no overlap with numbers
        y_lbl.next_to(tick_labels, LEFT, buff=0.35)
        self.play(axes_anim)
        self.play(FadeIn(tick_labels), FadeIn(y_lbl))

        values = [0.24, 0.46, 1.2]
        colors = [ACCENT_BLUE, ACCENT_AMBER, ACCENT_GREEN]
        bars_group, _ = bar_reveal(axes, values, colors=colors)

        # X labels centered under each bar — formula matches bar_reveal's x_step
        x_step = (axes.x_range[1] - axes.x_range[0]) / len(values)
        x_labels = VGroup()
        for i, lbl in enumerate(["V2V4Real\n240K", "DAIR-V2X\n460K", "V2X-Real\n1.2M"]):
            x_pos = axes.x_range[0] + (i + 0.5) * x_step
            t = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_CAPS - 1, color=INK_MID)
            t.next_to(axes.c2p(x_pos, 0), DOWN, buff=0.15)
            x_labels.add(t)

        # Animate each bar, value, and bottom label sequentially from left to right
        for i in range(3):
            self.play(
                GrowFromEdge(bars_group[0][i], DOWN),
                FadeIn(bars_group[1][i]),
                FadeIn(x_labels[i]),
                run_time=0.8
            )
            if i < 2:
                self.wait(1.0)

        # key_number in bottom-right — clear of bar labels at bottom-center
        kn = key_number("5x", "annotation growth in 2 years", color=GOLD_RICH)
        kn.to_corner(DR, buff=0.5)
        self.play(FadeIn(kn))
        self.wait(2)
        self._close()
