"""P02-S12 - RiskMap heatmap."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    ORANGE_INFRA,
    RED_ERROR,
    SIZE_CAPS,
    SIZE_LABEL,
    vehicle_icon,
)
from studio.scenes.part02._p02_helpers import mini_heatmap_grid, road_grid_2d


SCRIPT = "Risk is a field, continuous and predictive."


def _risk_rings(center: np.ndarray, *, color: str, radii: list[float], opacity: float) -> VGroup:
    rings = VGroup()
    for i, r in enumerate(reversed(radii)):
        rings.add(Circle(
            radius=r,
            fill_color=color,
            fill_opacity=opacity * (0.42 + 0.12 * i),
            stroke_width=0,
        ).move_to(center))
    return rings


def _corridor(points: list[np.ndarray], *, width: float = 0.54) -> VGroup:
    band = VMobject(stroke_color=GREEN_FIX, stroke_width=width * 56, stroke_opacity=0.18)
    band.set_points_smoothly(points)
    center = VMobject(stroke_color=GREEN_FIX, stroke_width=4.2, stroke_opacity=0.95)
    center.set_points_smoothly(points)
    return VGroup(band, center)


class P02S12RiskMap(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "RiskMap"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Audit reference: region/risk-field partitioning; centers stay anchored
        # to semantic objects and the MPC path stays inside the green corridor.
        road = road_grid_2d(width=12.2, height=5.3).move_to(DOWN * 0.15)

        start = LEFT * 4.65 + DOWN * 0.95
        end = RIGHT * 4.35 + DOWN * 0.62
        ego = vehicle_icon(color=ACCENT_BLUE, scale=0.62).move_to(start)

        other_center = RIGHT * 0.35 + UP * 0.48
        other = vehicle_icon(color=ORANGE_INFRA, scale=0.58).move_to(other_center).rotate(-PI / 7)
        hot = _risk_rings(other.get_center(), color=RED_ERROR, radii=[0.55, 0.88, 1.22, 1.56], opacity=0.32)

        blocked_center = LEFT * 0.85 + UP * 1.18
        unknown = _risk_rings(blocked_center, color=ORANGE_INFRA, radii=[0.55, 0.9, 1.2], opacity=0.18)
        safe_center = LEFT * 1.7 + DOWN * 1.22
        safe = _risk_rings(safe_center, color=GREEN_FIX, radii=[0.48, 0.78, 1.05], opacity=0.18)

        pts = [
            start,
            LEFT * 3.35 + DOWN * 1.22,
            LEFT * 1.95 + DOWN * 1.26,
            LEFT * 0.55 + DOWN * 1.05,
            RIGHT * 0.75 + DOWN * 1.22,
            RIGHT * 2.55 + DOWN * 1.1,
            end,
        ]
        corridor = _corridor(pts)

        inset = mini_heatmap_grid(rows=5, cols=7, cell=0.2).move_to(RIGHT * 4.35 + UP * 1.65)
        inset_label = Text("future risk field", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID, weight=BOLD)
        inset_label.next_to(inset, DOWN, buff=0.12)

        self.play(FadeIn(road), FadeIn(unknown), FadeIn(hot), FadeIn(safe), FadeIn(other), FadeIn(ego))
        self.play(FadeIn(inset), FadeIn(inset_label))
        self.play(ShowCreation(corridor[0]), ShowCreation(corridor[1]), ego.animate.move_to(end), run_time=1.45)

        mpc = Text("MPC follows the low-risk corridor", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        mpc["low-risk"].set_color(GREEN_FIX)
        mpc.move_to(LEFT * 2.85 + UP * 0.05)
        self.play(FadeIn(mpc))

        quote = Text("\"Risk is a language, not a bounding box.\"", font_size=SIZE_LABEL + 6, color=INK_DARK, slant=ITALIC)
        quote["language"].set_color(GOLD_RICH)
        quote.to_edge(DOWN, buff=0.72)
        self.play(FadeIn(quote))
        self.wait(0.9)
        self._close()
