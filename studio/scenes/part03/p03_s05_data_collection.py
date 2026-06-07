"""P03-S05 Data Collection Routes."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_GREEN, ACCENT_BLUE, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    contribution_badge, vehicle_icon,
)

SCRIPT = """V2X-Real and V2XPnP-Seq: routes, every time of day."""


def _sky_band(label: str, color: str, x: float, *, icon: str) -> VGroup:
    band = Rectangle(width=3.15, height=4.9, fill_color=color, fill_opacity=0.22, stroke_width=0)
    band.move_to([x, -0.15, 0])
    title = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
    title.move_to([x, 2.12, 0])

    if icon == "moon":
        moon = Circle(radius=0.16, fill_color="#E2E8F0", fill_opacity=1.0, stroke_width=0)
        cut = Circle(radius=0.16, fill_color=color, fill_opacity=1.0, stroke_width=0)
        cut.shift(RIGHT * 0.08 + UP * 0.02)
        symbol = VGroup(moon, cut)
    else:
        symbol = VGroup(Circle(radius=0.14, fill_color=GOLD_RICH, fill_opacity=1.0, stroke_width=0))
        for a in np.linspace(0, TAU, 8, endpoint=False):
            symbol.add(Line(
                np.array([np.cos(a), np.sin(a), 0]) * 0.2,
                np.array([np.cos(a), np.sin(a), 0]) * 0.3,
                stroke_color=GOLD_RICH,
                stroke_width=1.4,
                stroke_opacity=0.72,
            ))
    symbol.move_to([x, 1.64, 0])
    return VGroup(band, symbol, title)


def _route(points: list[np.ndarray], *, color: str) -> VMobject:
    path = VMobject()
    path.set_points_smoothly(points)
    path.set_stroke(color, width=4.0, opacity=0.95)
    return path


def _drive_along(car: Mobject, path: VMobject) -> UpdateFromAlphaFunc:
    template = car.copy()

    def update(mob: Mobject, alpha: float) -> None:
        p = path.point_from_proportion(alpha)
        q = path.point_from_proportion(min(alpha + 0.01, 1.0))
        if alpha > 0.99:
            q = p
            p = path.point_from_proportion(0.99)
        angle = angle_of_vector(q - p)
        mob.become(template.copy())
        mob.rotate(angle)
        mob.move_to(path.point_from_proportion(alpha))

    return UpdateFromAlphaFunc(car, update, run_time=1.0, rate_func=smooth)


def _road_scene() -> VGroup:
    road_fill = "#E2E8F0"
    road_h = RoundedRectangle(width=10.6, height=0.95, corner_radius=0.05, fill_color=road_fill, fill_opacity=0.82, stroke_width=0)
    road_v = RoundedRectangle(width=1.0, height=4.65, corner_radius=0.05, fill_color=road_fill, fill_opacity=0.82, stroke_width=0)
    road_h.move_to(DOWN * 0.15)
    road_v.move_to(DOWN * 0.15)
    marks = VGroup()
    for x in np.linspace(-4.7, 4.7, 11):
        marks.add(Line([x - 0.12, -0.15, 0], [x + 0.12, -0.15, 0], stroke_color=WHITE, stroke_width=2.0, stroke_opacity=0.55))
    for y in np.linspace(-2.0, 1.7, 7):
        marks.add(Line([0, y - 0.1, 0], [0, y + 0.1, 0], stroke_color=WHITE, stroke_width=2.0, stroke_opacity=0.55))
    hub = Circle(radius=0.42, fill_color=BG_PAPER, fill_opacity=0.25, stroke_color=WHITE, stroke_width=1.2, stroke_opacity=0.75)
    hub.move_to(road_h)
    return VGroup(road_h, road_v, marks, hub)


class P03S05DataCollection(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Data Collection"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        bands = VGroup(
            _sky_band("Morning", "#FDE68A", -4.7, icon="sun"),
            _sky_band("Noon", "#BAE6FD", -1.57, icon="sun"),
            _sky_band("Evening", "#FDBA74", 1.57, icon="sun"),
            _sky_band("Night", "#334155", 4.7, icon="moon"),
        )
        self.play(LaggedStart(*(FadeIn(b) for b in bands), lag_ratio=0.08), run_time=0.8)

        roads = _road_scene()
        self.play(FadeIn(roads), run_time=0.7)

        routes = [
            ("Straight", _route([LEFT * 4.7 + DOWN * 0.28, LEFT * 0.75 + DOWN * 0.28, RIGHT * 4.35 + DOWN * 0.28], color=ACCENT_GREEN), ACCENT_GREEN),
            ("L-Turn", _route([
                LEFT * 4.7 + DOWN * 0.02,
                LEFT * 1.12 + DOWN * 0.02,
                LEFT * 0.32 + UP * 0.12,
                RIGHT * 0.12 + UP * 0.72,
                RIGHT * 0.16 + UP * 1.62,
            ], color=ACCENT_BLUE), ACCENT_BLUE),
            ("R-Turn", _route([
                LEFT * 4.7 + UP * 0.23,
                LEFT * 1.1 + UP * 0.23,
                LEFT * 0.26 + UP * 0.05,
                RIGHT * 0.14 + DOWN * 0.62,
                RIGHT * 0.18 + DOWN * 1.82,
            ], color=GOLD_RICH), GOLD_RICH),
        ]

        for i, (label, path, color) in enumerate(routes):
            car = vehicle_icon(color=color, scale=0.48)
            car.move_to(path.get_start())
            route_label = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=color, weight=BOLD)
            route_label.move_to(LEFT * 5.05 + UP * (1.18 - i * 0.28))
            swatch = Line(LEFT * 5.85, LEFT * 5.5, stroke_color=color, stroke_width=4.0)
            swatch.set_y(route_label.get_center()[1])
            route_key = VGroup(swatch, route_label)
            self.play(ShowCreation(path), FadeIn(route_key), FadeIn(car), run_time=0.45)
            self.play(_drive_along(car, path))

        badges = VGroup(
            contribution_badge("V2X-Real  ·  ECCV 2024", color=GOLD_RICH),
            contribution_badge("V2XPnP-Seq Dataset", color=ACCENT_GREEN),
        )
        badges.arrange(RIGHT, buff=0.5)
        badges.to_edge(DOWN, buff=0.58)
        self.play(LaggedStart(*(FadeIn(b) for b in badges), lag_ratio=0.2))
        self.wait(1.5)
        self._close()
