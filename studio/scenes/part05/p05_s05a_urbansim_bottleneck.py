"""P05-S05a UrbanSim CPU-GPU Bottleneck."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, ACCENT_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_H1,
    pipeline_block, pipeline_arrow, key_number,
)
SCRIPT = """Training a simple RL agent used to take 180 GPU-days — CPU-GPU bottleneck at every step."""


class P05S05AUrbanSimBottleneck(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "UrbanSim: The Bottleneck"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        cpu = pipeline_block("CPU", fill="#FEE2E2", stroke=RED_ERROR, width=1.8)
        gpu = pipeline_block("GPU", fill="#C8DCFA", stroke=ACCENT_BLUE, width=1.8)
        cpu.move_to(LEFT * 1.7 + UP * 0.25)
        gpu.move_to(RIGHT * 1.7 + UP * 0.25)
        transfer = Arrow(cpu.get_right(), gpu.get_left(), fill_color=RED_ERROR, thickness=3.0, buff=0.06)
        transfer_lbl = Text("Transfer\nbottleneck", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2, color=RED_ERROR)
        transfer_lbl.next_to(transfer, UP, buff=0.1)
        self.play(FadeIn(cpu), FadeIn(gpu))
        self.play(ShowCreation(transfer), FadeIn(transfer_lbl))
        self.play(Flash(transfer, color=RED_ERROR, line_length=0.25, num_lines=8))
        cost = key_number("180", "GPU-days to train", color=RED_ERROR)
        cost.to_corner(DR, buff=0.5)
        self.play(FadeIn(cost))
        self.wait(2)
        self._close()
