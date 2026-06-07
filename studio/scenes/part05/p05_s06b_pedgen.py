"""P05-S06b PedGen diffusion model."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, PURPLE_MODEL, ACCENT_GREEN,
    CYAN_RADAR, INK_DARK, FONT_PRIMARY, SIZE_LABEL,
    pipeline_block, pipeline_arrow, pedestrian_icon,
)
SCRIPT = """PedGen is a diffusion model conditioned on scene, body, and goal. Three inputs, one walker."""


class P05S06BPedGen(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "PedGen: Diffusion Model"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # 3 inputs
        inputs = [
            pipeline_block("Scene Voxel", fill="#C8DCFA", stroke="#2563EB"),
            pipeline_block("SMPL Body", fill="#E0D7FF", stroke=PURPLE_MODEL),
            pipeline_block("Goal", fill="#C8EDD0", stroke=ACCENT_GREEN),
        ]
        inp_grp = VGroup(*inputs).arrange(DOWN, buff=0.3).move_to(LEFT * 3.8)
        diffusion = pipeline_block("Diffusion\nModel", fill="#F9C8D8", stroke=ACCENT_PINK, width=2.5, height=1.5)
        diffusion.move_to(ORIGIN)
        self.play(LaggedStart(*(FadeIn(b) for b in inputs), lag_ratio=0.15))
        self.play(FadeIn(diffusion))
        for b in inputs:
            arr = pipeline_arrow(b, diffusion)
            self.add(arr)
        # Noise particles -> clean walker
        noise_dots = VGroup()
        rng = __import__("numpy").random.RandomState(7)
        for _ in range(20):
            d = Dot(radius=0.06, color=CYAN_RADAR)
            d.move_to(diffusion.get_right() + __import__("numpy").array([rng.uniform(0.2, 0.8), rng.uniform(-0.5, 0.5), 0]))
            noise_dots.add(d)
        self.play(LaggedStart(*(FadeIn(d, scale=0.3) for d in noise_dots), lag_ratio=0.04, run_time=0.8))
        ped = pedestrian_icon(color=ACCENT_PINK).scale(1.2)
        ped.move_to(RIGHT * 3.5)
        arr_out = pipeline_arrow(diffusion, ped, color=ACCENT_PINK)
        self.play(LaggedStart(*(FadeOut(d) for d in noise_dots), lag_ratio=0.03, run_time=0.6))
        self.play(ShowCreation(arr_out), GrowFromCenter(ped))
        cap = Text("noise  ->  anatomically realistic human walker",
                   font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
