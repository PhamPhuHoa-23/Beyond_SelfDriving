"""P02-S04a - Single-agent occlusion problem."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    BG_CARD,
    FONT_PRIMARY,
    INK_DARK,
    RED_ERROR,
    SIZE_HERO,
    SIZE_LABEL,
    vehicle_icon,
)
from studio.scenes.part02._p02_helpers import road_grid_2d


SCRIPT = "Has end-to-end solved everything? Not yet."


class P02S04AOcclusionProblem(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "The Occlusion Problem"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py:95
        road = road_grid_2d()
        road.move_to(DOWN * 0.15)
        car = vehicle_icon(color=ACCENT_BLUE, scale=0.85)
        car.move_to(LEFT * 3.1 + DOWN * 0.25)
        truck = RoundedRectangle(width=1.5, height=0.85, corner_radius=0.1, fill_color=BG_CARD, fill_opacity=1.0, stroke_color=INK_DARK, stroke_width=2)
        truck.move_to(LEFT * 0.35 + DOWN * 0.25)
        cone = VGroup()
        source = car.get_center() + RIGHT * 0.35
        # Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py:95
        for i in range(5):
            near = source + RIGHT * (0.35 + i * 0.55)
            far = source + RIGHT * (0.9 + i * 0.55)
            spread_near = 0.12 + i * 0.12
            spread_far = 0.24 + i * 0.14
            cone.add(Polygon(
                near + UP * spread_near,
                far + UP * spread_far,
                far + DOWN * spread_far,
                near + DOWN * spread_near,
                fill_color=ACCENT_BLUE,
                fill_opacity=0.22 * (1 - i / 6),
                stroke_width=0,
            ))
        blind = Polygon(
            truck.get_right() + UP * 0.45,
            RIGHT * 4.3 + UP * 1.6,
            RIGHT * 4.3 + DOWN * 1.9,
            truck.get_right() + DOWN * 0.45,
            fill_color=RED_ERROR,
            fill_opacity=0.3,
            stroke_color=RED_ERROR,
            stroke_width=2,
        )
        self.play(FadeIn(road), FadeIn(car, shift=RIGHT * 0.4))
        self.play(FadeIn(cone), FadeIn(truck, shift=DOWN * 0.35))
        self.play(FadeIn(blind))
        label = Text("single agent -> blind to occlusion", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        label.move_to(RIGHT * 3.6 + UP * 2.25)
        label_bg = SurroundingRectangle(label, buff=0.12, fill_color=BG_CARD, fill_opacity=1.0, stroke_color=RED_ERROR, stroke_width=1.8)
        self.play(FadeIn(label_bg), FadeIn(label))
        no = Text("Not yet.", font=FONT_PRIMARY, font_size=SIZE_HERO, color=RED_ERROR, weight=BOLD)
        no.move_to(DOWN * 2.05)
        self.play(Write(no, run_time=0.8))
        self.wait(1.1)
        self._close()
