"""P05-S05b UrbanSim All-GPU Results."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, GREEN_FIX, GOLD_RICH, GOLD_KEY, ACCENT_BLUE, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    key_number, contribution_badge,
)
SCRIPT = """UrbanSim: 256 parallel environments, three hours instead of 180 days."""


class P05S05BUrbanSimResults(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "UrbanSim: 180 Days -> 3 Hours"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # 256 parallel env grid (16x16 tiles)
        grid = VGroup()
        for r in range(8):
            for c in range(16):
                sq = Square(side_length=0.28, fill_color=GREEN_FIX, fill_opacity=0.35, stroke_color=GREEN_FIX, stroke_width=0.8)
                sq.move_to(np.array([(c - 7.5) * 0.32, (r - 3.5) * 0.32 + 0.5, 0]))
                grid.add(sq)
        self.play(LaggedStart(*(FadeIn(s, scale=0.4) for s in grid), lag_ratio=0.005, run_time=1.5))
        env_lbl = Text("128 parallel environments (subset shown)", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GREEN_FIX)
        env_lbl.next_to(grid, DOWN, buff=0.15)
        self.play(FadeIn(env_lbl))
        kns = VGroup(
            key_number("3h", "vs 180 GPU-days", color=GOLD_RICH),
            key_number("2620 FPS", "simulation throughput", color=GOLD_RICH),
        )
        kns.arrange(RIGHT, buff=1.5).to_edge(DOWN, buff=0.4)
        self.play(LaggedStart(*(FadeIn(k, scale=1.2) for k in kns), lag_ratio=0.3))
        self.play(*(Flash(k[0], color=GOLD_RICH, line_length=0.2, num_lines=8) for k in kns))
        self.wait(2)
        self._close()
