"""P03-S15 Bridge to Part 4."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_AMBER, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL,
    write_chiseled,
)
SCRIPT = """Now it works. But efficient enough to deploy? Three bottlenecks are next."""


class P03S15BridgeToP4(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Bridge to Part 4"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        recap = Text("Now it works.", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_MID)
        recap.move_to(UP * 0.8)
        self.play(FadeIn(recap))
        forward = Text(
            "But is it efficient enough to deploy?",
            font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH,
        )
        forward.move_to(DOWN * 0.2)
        self.play(write_chiseled(forward, run_time=2.0))
        bottlenecks = ["Data", "Training", "Inference"]
        tags = VGroup()
        for name in bottlenecks:
            t = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_AMBER, weight=BOLD)
            bg = RoundedRectangle(width=t.get_width() + 0.4, height=t.get_height() + 0.2,
                                  corner_radius=0.1, fill_color=BG_PAPER, fill_opacity=1.0,
                                  stroke_color=ACCENT_AMBER, stroke_width=2.0)
            t.move_to(bg)
            tags.add(VGroup(bg, t))
        tags.arrange(RIGHT, buff=0.5)
        tags.move_to(DOWN * 1.5)
        self.play(LaggedStart(*(FadeIn(t, shift=UP * 0.2) for t in tags), lag_ratio=0.2))
        self.wait(1.5)
        self._close()
