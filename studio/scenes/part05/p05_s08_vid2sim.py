"""P05-S08 Vid2Sim pipeline."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, GOLD_RICH, CYAN_RADAR, ACCENT_GREEN, PURPLE_MODEL,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL,
    pipeline_block, pipeline_arrow, vehicle_icon,
)
SCRIPT = """Vid2Sim turns a city-tour video into a simulator: gaussians for visuals, mesh for physics."""


class P05S08Vid2Sim(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Vid2Sim"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # Pipeline: Video -> Gaussian Splats -> Mesh -> Sim
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/spheres_talk/volumes.py:365
        video_block = pipeline_block("City-tour\nVideo", fill="#C8DCFA", stroke="#2563EB")
        splat_block = pipeline_block("3D Gaussian\nSplats", fill="#E0D7FF", stroke=PURPLE_MODEL)
        mesh_block = pipeline_block("Mesh\nWireframe", fill="#D1FAE5", stroke=ACCENT_GREEN)
        sim_block = pipeline_block("Interactive\nSimulator", fill="#FAE3B0", stroke="#D97706")
        pipeline = VGroup(video_block, splat_block, mesh_block, sim_block)
        pipeline.arrange(RIGHT, buff=0.7).move_to(UP * 0.5)
        self.play(LaggedStart(*(FadeIn(b) for b in pipeline), lag_ratio=0.2))
        arrows = VGroup(*(pipeline_arrow(pipeline[i], pipeline[i + 1]) for i in range(3)))
        self.play(LaggedStart(*(ShowCreation(a) for a in arrows), lag_ratio=0.15))
        # Gaussian splat visualization: colored dots cluster
        rng = __import__("numpy").random.RandomState(3)
        splats = VGroup()
        colors = [CYAN_RADAR, GOLD_RICH, ACCENT_GREEN, PURPLE_MODEL]
        for i in range(30):
            d = Dot(radius=0.08, color=colors[i % 4])
            d.move_to(__import__("numpy").array([rng.uniform(-1.5, 1.5), rng.uniform(-0.4, 0.2) - 0.8, 0]))
            d.set_opacity(rng.uniform(0.5, 0.9))
            splats.add(d)
        self.play(LaggedStart(*(FadeIn(d, scale=0.3) for d in splats), lag_ratio=0.03, run_time=0.8))
        robot = vehicle_icon(color=ACCENT_GREEN, scale=0.8).move_to(__import__("numpy").array([1.5, -0.8, 0]))
        robot_path = Line(__import__("numpy").array([0.0, -0.8, 0]), __import__("numpy").array([2.5, -0.8, 0]))
        self.play(GrowFromCenter(robot))
        self.play(robot.animate(run_time=1.0, rate_func=smooth).move_to(__import__("numpy").array([2.5, -0.8, 0])))
        cap = Text("video  ->  playground", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
