"""P05-S04c MetaUrban Scaling Curve."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL,
    axes_deploy, curve_trace,
)
SCRIPT = """The scaling is power-law. A hundred diverse scenes beat a thousand near-duplicates."""


class P05S04CMetaUrbanScaling(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Diversity Scaling"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        axes, axes_anim = axes_deploy(
            (0, 5, 1), (0, 1.0, 0.25), x_label="Unique layouts", y_label="Unseen env. perf."
        )
        axes.scale(0.75).move_to(LEFT * 1.5 + DOWN * 0.2)
        self.play(axes_anim)
        # Power-law curve: diverse
        diverse_anim = curve_trace(axes, lambda x: 1 - np.exp(-x * 0.9), color=GOLD_RICH, run_time=2.0)
        self.play(diverse_anim)
        # Linear baseline: repeated
        repeat_anim = curve_trace(axes, lambda x: x * 0.12, color=INK_MID, run_time=1.5)
        self.play(repeat_anim)
        callout = Text("100 diverse > 1000 repeated", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        callout.move_to(RIGHT * 3.5 + UP * 0.8)
        self.play(FadeIn(callout, scale=1.05))
        self.wait(2)
        self._close()
