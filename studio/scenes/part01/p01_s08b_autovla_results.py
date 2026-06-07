"""P01-S08b — AutoVLA Results: bar chart + key numbers (clean axis layout)."""
from manimlib import *
from studio.components import (
    StudioScene,
    GOLD_RICH, GOLD_KEY, GREEN_FIX, INK_MID, INK_DARK,
    axes_deploy, bar_reveal, bar_group_labels, chart_mount, key_number, contribution_badge,
    place_footer,
)

SCRIPT = """
Reasoning beats action-only training on every metric.
Plus RFT cuts runtime by two-thirds.
"""


class P01S08BAutoVLAResults(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "AutoVLA Results"

    def construct(self):
        self._open(self.SCENE_TITLE)

        axes, axes_anim = axes_deploy(
            (0, 4, 1), (0, 1.0, 0.2),
            width=6.0, height=4.2, with_tick_labels=False,
        )
        tick_labels = chart_mount(
            axes, LEFT * 1.8 + DOWN * 0.2, scale=0.88, y_label="Score",
        )
        self.play(axes_anim, FadeIn(tick_labels))

        values = [0.72, 0.79, 0.68, 0.82]
        colors = [INK_MID, GOLD_RICH, INK_MID, GOLD_RICH]
        bar_lbls = ["base", "AutoVLA", "base", "AutoVLA"]
        bars, bar_anim = bar_reveal(
            axes, values, colors=colors, show_values=True, x_labels=bar_lbls,
        )
        groups = bar_group_labels(axes, [("nuPlan", 0, 2), ("nuScenes", 2, 4)])
        self.play(bar_anim)
        self.add(bars, groups)

        kn_plan = key_number("+10.6%", "planning score", color=GREEN_FIX)
        kn_rt = key_number("3×", "faster  (−66.8% runtime)", color=GREEN_FIX)
        kn_group = VGroup(kn_plan, kn_rt).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        kn_group.scale(0.80)
        kn_group.move_to(RIGHT * 3.6 + UP * 0.3)

        self.play(
            LaggedStart(FadeIn(kn_plan, scale=1.08), FadeIn(kn_rt, scale=1.08), lag_ratio=0.35),
            Flash(bars[0][1], color=GOLD_RICH, num_lines=12, line_length=0.2),
        )

        badge = contribution_badge("IROS 2025 Best Paper  ·  UCLA DriveX", color=GOLD_KEY)
        place_footer(badge)
        self.play(FadeIn(badge))
        self.wait(2)
        self._close()
