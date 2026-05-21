# beyond/scenes/part03/p03_s11_opencda.py — OpenCDA + ROS integration
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block, pipeline_block_entrance,
    pipeline_arrow_entrance,
    P3_SIM, CYAN_NEON, ORANGE_INFRA, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

class P03S11OpenCDA(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("OpenCDA — Open-Source V2X Development Platform")
        self.wait(0.2)

        # 3-layer stack: Simulation → ROS → Hardware
        layers = [
            ("CARLA / MetaDrive\n(Simulation Engine)", P3_SIM,    UP * 1.5),
            ("ROS2 Middleware\n(Communication Hub)",   CYAN_NEON,  ORIGIN),
            ("Real Sensor Hardware\n(LiDAR, Camera, V2X)", ORANGE_INFRA, DOWN * 1.5),
        ]

        blocks = []
        for lbl, col, pos in layers:
            blk = pipeline_block(lbl, width=4.5, height=0.90,
                                 border_color=col, fill_color=BG_PANEL,
                                 font_size=SIZE_MICRO + 1)
            blk.move_to(pos)
            blocks.append(blk)

        self.play(
            LaggedStart(*[pipeline_block_entrance(b, layers[i][1])
                          for i, b in enumerate(blocks)], lag_ratio=0.20),
        )

        # Bidirectional arrows between layers
        for i in range(len(blocks) - 1):
            arr = DoubleArrow(blocks[i].get_bottom(), blocks[i+1].get_top(),
                              buff=0.05, color=TEXT_DIM,
                              stroke_width=1.5, tip_length=0.14)
            self.play(Create(arr, run_time=0.25))

        # Feature labels (right side)
        features = [
            ("✓ Plug-and-play co-simulation",     P3_SIM),
            ("✓ Real-time data bridge",            CYAN_NEON),
            ("✓ V2X protocol support",             ORANGE_INFRA),
            ("✓ Open-source + extensible",         GREEN_SIGNAL),
        ]
        feat_grp = VGroup(*[
            Text(f"{txt}", font_size=SIZE_MICRO + 1, color=col, font=FONT_PRIMARY)
            for txt, col in features
        ]).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to(RIGHT * 4.0)

        self.play(
            LaggedStart(*[FadeIn(m, shift=LEFT * 0.08, run_time=0.22)
                          for m in feat_grp], lag_ratio=0.15),
        )
        self.wait(1.2)
        self.close()
