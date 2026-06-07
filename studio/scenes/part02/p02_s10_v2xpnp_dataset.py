"""P02-S10 - V2XPnP-Seq dataset stats."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_TEAL,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    ORANGE_INFRA,
    PURPLE_MODEL,
    SIZE_CAPS,
    SIZE_LABEL,
    key_number,
    rsu_icon,
    v2x_link,
    vehicle_icon,
)
from studio.scenes.part02._p02_helpers import road_grid_2d


SCRIPT = "V2XPnP-Seq covers V2V, V2I, V2X, and I2I with sequential real-world frames."


class P02S10V2XPnPDataset(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "V2XPnP-Seq Dataset"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Pattern adapted from: Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py:43
        map_panel = RoundedRectangle(
            width=5.15,
            height=3.45,
            corner_radius=0.14,
            fill_color="#E0F2FE",
            fill_opacity=1.0,
            stroke_color=ACCENT_TEAL,
            stroke_width=2.5,
        ).move_to(LEFT * 3.05 + DOWN * 0.05)
        roads = road_grid_2d(width=4.7, height=3.05).scale(0.88).move_to(map_panel)
        car1 = vehicle_icon(color=ACCENT_TEAL, scale=0.42).move_to(map_panel.get_center() + LEFT * 1.35 + DOWN * 0.45)
        car2 = vehicle_icon(color=GREEN_FIX, scale=0.42).move_to(map_panel.get_center() + RIGHT * 1.0 + UP * 0.55)
        rsu1 = rsu_icon(color=ORANGE_INFRA).scale(0.75).move_to(map_panel.get_center() + LEFT * 1.6 + UP * 0.9)
        rsu2 = rsu_icon(color=ORANGE_INFRA).scale(0.75).move_to(map_panel.get_center() + RIGHT * 1.55 + DOWN * 0.85)
        agents = VGroup(car1, car2, rsu1, rsu2)
        links = VGroup()
        flashes = []
        for a, b in [(car1, car2), (car1, rsu1), (car2, rsu2), (rsu1, rsu2)]:
            line, flash = v2x_link(a, b, color=CYAN_RADAR)
            links.add(line)
            flashes.append(flash)
        map_label = Text("all collaboration modes", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        map_label.next_to(map_panel, DOWN, buff=0.16)

        stats = [
            ("2", "vehicles", ACCENT_TEAL),
            ("2", "infra nodes", ORANGE_INFRA),
            ("40K", "LiDAR frames", GOLD_RICH),
            ("208K", "camera frames", GREEN_FIX),
            ("HD", "maps + trajectories", PURPLE_MODEL),
            ("V2V / V2I / I2I", "same sequence", ACCENT_TEAL),
        ]
        cards = VGroup(*(key_number(v, label, color=c).scale(0.38) for v, label, c in stats))
        cards.arrange_in_grid(3, 2, h_buff=0.9, v_buff=0.26)
        cards.move_to(RIGHT * 3.2 + DOWN * 0.05)

        foot = Text("Real-world, sequential, multi-agent data.", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        foot.to_edge(DOWN, buff=0.72)

        self.play(FadeIn(map_panel), FadeIn(roads))
        self.play(LaggedStart(*(FadeIn(a, shift=DOWN * 0.12) for a in agents), lag_ratio=0.1))
        self.play(ShowCreation(links), *flashes)
        self.play(FadeIn(map_label), LaggedStart(*(FadeIn(card, shift=UP * 0.14) for card in cards), lag_ratio=0.1))
        self.play(FadeIn(foot))
        self.wait(1.0)
        self._close()
