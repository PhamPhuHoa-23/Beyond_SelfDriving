"""P05-S08 Vid2Sim: video to interactive simulator."""
from manimlib import *
import numpy as np
from pathlib import Path

from studio.components import (
    StudioScene,
    BG_PAPER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_AMBER,
    PASTEL_PINK,
    ACCENT_BLUE,
    ACCENT_TEAL,
    ACCENT_GREEN,
    ACCENT_AMBER,
    ACCENT_PINK,
    PURPLE_MODEL,
    GOLD_RICH,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    img_or_placeholder,
)

SCRIPT = """Vid2Sim converts a real city-tour video into a simulator by combining 3D Gaussian splatting for photorealistic observations with a mesh layer for physical interaction."""


class P05S08Vid2Sim(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Vid2Sim: Video -> Simulator"
    ASSET_DIR = Path("materials/images/part5/vid2sim")

    def framed_image(self, path, label, color, width, height, image_width=None, image_height=None):
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.14,
            fill_color=interpolate_color(color, WHITE, 0.9),
            fill_opacity=1,
            stroke_color=color,
            stroke_width=1.6,
        )
        image = img_or_placeholder(path, label, width=image_width or width - 0.25, height=image_height or height - 0.55)
        image.move_to(panel.get_center() + DOWN * 0.12)
        text = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=color, weight=BOLD)
        text.move_to(panel.get_top() + DOWN * 0.19)
        return Group(panel, image, text)

    def video_panel(self):
        title = Text("1. city-tour videos", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_BLUE, weight=BOLD)
        card = self.framed_image(self.ASSET_DIR / "city_tours.jpg", "many real street videos", ACCENT_BLUE, 3.35, 3.0, 3.05, 2.25)
        title.next_to(card[0], UP, buff=0.14)
        tags = VGroup(
            Text("viewpoints", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_BLUE),
            Text("traffic", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_PINK),
            Text("city scale", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_GREEN),
        ).arrange(RIGHT, buff=0.16)
        tags.next_to(card[0], DOWN, buff=0.1)
        return Group(card[0], card[1], card[2], title, tags)

    def reconstruction_panel(self):
        shell = RoundedRectangle(
            width=3.75,
            height=3.0,
            corner_radius=0.14,
            fill_color="#F8F2FF",
            fill_opacity=1,
            stroke_color=PURPLE_MODEL,
            stroke_width=1.6,
        )
        title = Text("2. reconstruct layers", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=PURPLE_MODEL, weight=BOLD)
        title.next_to(shell, UP, buff=0.14)
        gaussian = img_or_placeholder(self.ASSET_DIR / "gaussian_scene.jpg", "3DGS", width=1.65, height=1.45)
        mesh = img_or_placeholder(self.ASSET_DIR / "mesh_scene.jpg", "mesh", width=1.38, height=1.45)
        row = Group(gaussian, mesh).arrange(RIGHT, buff=0.22)
        row.move_to(shell.get_center() + UP * 0.02)
        g_label = Text("3DGS\nappearance", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=PURPLE_MODEL, weight=BOLD)
        m_label = Text("mesh\nphysics", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_GREEN, weight=BOLD)
        labels = VGroup(g_label, m_label).arrange(RIGHT, buff=0.72)
        labels.move_to(shell.get_bottom() + UP * 0.33)
        return Group(shell, row, labels, title)

    def simulator_panel(self):
        title = Text("3. train in simulator", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_GREEN, weight=BOLD)
        card = self.framed_image(self.ASSET_DIR / "robot_training.jpg", "robot observations + actions", ACCENT_GREEN, 3.35, 3.0, 3.05, 2.25)
        title.next_to(card[0], UP, buff=0.14)
        tag = Text("interactive rollout", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        tag.next_to(card[0], DOWN, buff=0.1)
        return Group(card[0], card[1], card[2], title, tag)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        video = self.video_panel()
        recon = self.reconstruction_panel()
        sim = self.simulator_panel()
        video.move_to(LEFT * 4.35 + DOWN * 0.25)
        recon.move_to(DOWN * 0.25)
        sim.move_to(RIGHT * 4.35 + DOWN * 0.25)
        y = video[0].get_center()[1]

        arrow1 = Arrow([video[0].get_right()[0] + 0.12, y, 0], [recon[0].get_left()[0] - 0.12, y, 0], fill_color=ACCENT_BLUE, thickness=2.1, max_tip_length_to_length_ratio=0.18, buff=0)
        arrow2 = Arrow([recon[0].get_right()[0] + 0.12, y, 0], [sim[0].get_left()[0] - 0.12, y, 0], fill_color=ACCENT_GREEN, thickness=2.1, max_tip_length_to_length_ratio=0.18, buff=0)

        bottom = Text(
            "photorealistic observations + physical mesh = a simulator robots can act in",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=INK_DARK,
        )
        bottom.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(video[0]), FadeIn(video[1]), FadeIn(video[2:]), run_time=0.75)
        self.play(ShowCreation(arrow1), FadeIn(recon[0]), FadeIn(recon[3]), run_time=0.45)
        self.play(FadeIn(recon[1]), FadeIn(recon[2]), run_time=0.8)
        self.play(ShowCreation(arrow2), FadeIn(sim[0]), FadeIn(sim[1]), FadeIn(sim[2:]), run_time=0.75)
        self.play(FadeIn(bottom, shift=UP * 0.08), run_time=0.45)
        self.wait(2.0)
        self._close()
