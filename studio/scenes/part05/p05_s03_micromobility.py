"""P05-S03 Micro-Mobility Testbed."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, GOLD_KEY, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon, pedestrian_icon, drone_icon, contribution_badge,
)
SCRIPT = """Sixty percent of US trips are under five miles. Micro-mobility: robots, wheelchairs, scooters, humanoids."""


class P05S03Micromobility(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Micro-Mobility Testbed"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        stat = Text("60% of US trips  <  5 miles", font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH, weight=BOLD)
        stat.move_to(UP * 1.6)
        self.play(FadeIn(stat, scale=1.1))
        agents = [
            ("Delivery Robot", vehicle_icon(color="#10B981")),
            ("e-Wheelchair", pedestrian_icon(color="#8B5CF6")),
            ("Scooter", vehicle_icon(color=ACCENT_PINK)),
            ("Humanoid", pedestrian_icon(color=GOLD_KEY)),
        ]
        cards = VGroup()
        for name, icon in agents:
            icon.scale(1.2)
            lbl = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
            bg = RoundedRectangle(width=2.2, height=1.8, corner_radius=0.15, fill_color=BG_PAPER, fill_opacity=1.0, stroke_color=ACCENT_PINK, stroke_width=1.8)
            grp = VGroup(icon, lbl).arrange(DOWN, buff=0.12)
            grp.move_to(bg)
            cards.add(VGroup(bg, grp))
        cards.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.3)
        self.play(LaggedStart(*(FadeIn(c, scale=0.85) for c in cards), lag_ratio=0.2))
        badge = contribution_badge("COCO Robotics Partnership", color=GOLD_KEY)
        badge.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(badge))
        self.wait(2)
        self._close()
