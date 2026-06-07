"""P02-S14 - Bridge to Part 3."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_GREEN,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    BG_CARD,
    BG_PAPER,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    ORANGE_INFRA,
    SIZE_H1,
    SIZE_LABEL,
    h_arrow,
    vehicle_icon,
    write_chiseled,
)
from studio.scenes.part02._p02_helpers import road_grid_2d


SCRIPT = "All of this needs real data from real sensors on real roads."


class P02S14BridgeToP3(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Bridge to Part 3"

    def construct(self):
        self._open(self.SCENE_TITLE)
        setup = Text("Fusion. Training. Planning.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID)
        setup.move_to(UP * 1.92)
        self.play(FadeIn(setup))

        def bridge_panel(label, stroke):
            rect = RoundedRectangle(
                width=3.55,
                height=1.65,
                corner_radius=0.12,
                fill_color=BG_CARD,
                fill_opacity=1.0,
                stroke_color=stroke,
                stroke_width=2.4,
            )
            title = Text(label, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
            title.move_to(rect.get_top() + DOWN * 0.34)
            return VGroup(rect, title)

        sim = bridge_panel("Simulation", ACCENT_BLUE)
        real = bridge_panel("Reality", GREEN_FIX)
        panels = VGroup(sim, real).arrange(RIGHT, buff=1.55).move_to(UP * 0.36)
        bridge = h_arrow(sim, real, y=panels.get_center()[1], color=GOLD_RICH, thickness=3.2)
        gap = Text("sim-to-real gap", font=FONT_PRIMARY, font_size=18, color=ORANGE_INFRA, weight=BOLD)
        gap_bg = RoundedRectangle(
            width=gap.get_width() + 0.32,
            height=gap.get_height() + 0.16,
            corner_radius=0.1,
            fill_color=BG_PAPER,
            fill_opacity=1.0,
            stroke_color=ORANGE_INFRA,
            stroke_width=1.4,
        )
        gap_group = VGroup(gap_bg, gap)
        gap_group.move_to(panels.get_bottom() + DOWN * 0.36)

        sim_grid = road_grid_2d(width=2.65, height=1.7).scale(0.28).move_to(sim[0].get_center() + DOWN * 0.26)
        sim_note = Text("many scenarios", font=FONT_PRIMARY, font_size=18, color=INK_MID)
        sim_note.move_to(sim[0].get_bottom() + UP * 0.22)
        real_car = vehicle_icon(color=GREEN_FIX, scale=0.36).move_to(real[0].get_center() + DOWN * 0.26)
        sensor = VGroup(*(
            Line(real_car.get_center(), real_car.get_center() + RIGHT * (0.35 + i * 0.25) + UP * (i - 1) * 0.16, stroke_color=LINE_GRID, stroke_width=2)
            for i in range(3)
        ))
        real_note = Text("real sensor data", font=FONT_PRIMARY, font_size=18, color=INK_MID)
        real_note.move_to(real[0].get_bottom() + UP * 0.22)

        self.play(FadeIn(panels[0]), FadeIn(sim_grid))
        self.play(
            ShowCreation(bridge),
            FadeIn(gap_group),
            FadeIn(panels[1]),
            FadeIn(real_car),
            ShowCreation(sensor),
            FadeIn(sim_note),
            FadeIn(real_note),
        )

        forward = Text(
            "Part 3 needs real data\nfrom real sensors on real roads.",
            font=FONT_PRIMARY,
            font_size=SIZE_H1,
            color=GOLD_RICH,
            slant=ITALIC,
        )
        forward.move_to(DOWN * 1.8)
        self.play(write_chiseled(forward, run_time=2.2))
        dot = Circle(radius=0.16, fill_color=ACCENT_GREEN, fill_opacity=1.0, stroke_width=0)
        dot.next_to(forward, DOWN, buff=0.22)
        self.play(FadeIn(dot), Flash(dot, color=ACCENT_GREEN, line_length=0.25, num_lines=8))
        self.wait(0.8)
        self._close()
