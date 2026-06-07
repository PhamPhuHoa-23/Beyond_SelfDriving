"""P03-S13 InfraX 4 feature cards."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_GREEN, CYAN_RADAR, GOLD_KEY,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, SIZE_MICRO,
    contribution_badge, vehicle_icon,
)
SCRIPT = """OpenCDA-InfraX: configurable sensors, modalities, weather, and maps."""


def _txt(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    return Text(text, font=FONT_PRIMARY, font_size=size, color=color, weight=weight)


def _sensor_icon(color: str) -> VGroup:
    car = vehicle_icon(color=color, scale=0.34)
    dots = VGroup(*[
        Circle(radius=0.055, fill_color=c, fill_opacity=1, stroke_width=0)
        for c in (ACCENT_BLUE, ACCENT_GREEN, "#D97706")
    ]).arrange(RIGHT, buff=0.08)
    dots.next_to(car, UP, buff=0.15)
    rays = VGroup(*[
        Line(car.get_top(), dot.get_bottom(), stroke_color=CYAN_RADAR, stroke_width=1.0, stroke_opacity=0.55)
        for dot in dots
    ])
    return VGroup(rays, car, dots)


def _modality_icon(color: str) -> VGroup:
    nodes = VGroup()
    for p, label in [
        (LEFT * 0.42 + DOWN * 0.12, "V"),
        (RIGHT * 0.42 + DOWN * 0.12, "I"),
        (UP * 0.42, "X"),
    ]:
        node = Circle(radius=0.18, fill_color=interpolate_color(color, WHITE, 0.62), fill_opacity=1, stroke_color=color, stroke_width=1.4)
        txt = _txt(label, size=SIZE_MICRO + 1, color=color, weight=BOLD).move_to(node)
        nodes.add(VGroup(node, txt).move_to(p))
    links = VGroup(
        Line(nodes[0].get_center(), nodes[1].get_center(), stroke_color=color, stroke_width=1.4),
        Line(nodes[1].get_center(), nodes[2].get_center(), stroke_color=color, stroke_width=1.4),
        Line(nodes[2].get_center(), nodes[0].get_center(), stroke_color=color, stroke_width=1.4),
    )
    return VGroup(links, nodes)


def _weather_icon(color: str) -> VGroup:
    sun = Circle(radius=0.16, fill_color="#F59E0B", fill_opacity=1, stroke_width=0).move_to(LEFT * 0.34 + UP * 0.16)
    cloud = VGroup(
        Circle(radius=0.18, fill_color="#CBD5E1", fill_opacity=1, stroke_width=0).move_to(LEFT * 0.05),
        Circle(radius=0.15, fill_color="#CBD5E1", fill_opacity=1, stroke_width=0).move_to(RIGHT * 0.15 + UP * 0.04),
        RoundedRectangle(width=0.54, height=0.18, corner_radius=0.09, fill_color="#CBD5E1", fill_opacity=1, stroke_width=0).move_to(DOWN * 0.08),
    )
    rain = VGroup(*[
        Line(UP * 0.08, DOWN * 0.08, stroke_color=CYAN_RADAR, stroke_width=1.2).move_to([x, -0.34, 0])
        for x in (-0.18, 0.02, 0.22)
    ])
    rain.rotate(-0.2)
    return VGroup(sun, cloud, rain)


def _map_icon(color: str) -> VGroup:
    grid = VGroup()
    for x in (-0.32, 0.18):
        grid.add(Line(UP * 0.45, DOWN * 0.45, stroke_color=color, stroke_width=1.0, stroke_opacity=0.34).shift(RIGHT * x))
    for y in (-0.2, 0.22):
        grid.add(Line(LEFT * 0.55, RIGHT * 0.55, stroke_color=color, stroke_width=1.0, stroke_opacity=0.34).shift(UP * y))
    route = VMobject()
    route.set_points_as_corners([LEFT * 0.48 + DOWN * 0.28, LEFT * 0.12 + DOWN * 0.05, RIGHT * 0.12 + UP * 0.08, RIGHT * 0.5 + UP * 0.32])
    route.set_stroke(color, width=2.4)
    pin = Circle(radius=0.07, fill_color=color, fill_opacity=1, stroke_width=0).move_to(RIGHT * 0.12 + UP * 0.08)
    return VGroup(grid, route, pin)


def _feature_card(title: str, body: str, color: str, icon: Mobject) -> VGroup:
    rect = RoundedRectangle(
        width=4.5, height=1.55, corner_radius=0.15,
        fill_color=BG_PAPER, fill_opacity=1.0,
        stroke_color=color, stroke_width=2.0,
    )
    icon.scale(0.78)
    icon.move_to(rect.get_left() + RIGHT * 0.88)
    t_mob = _txt(title, size=SIZE_LABEL - 1, color=color, weight=BOLD)
    b_mob = _txt(body, size=SIZE_CAPS - 1, color=INK_MID)
    text = VGroup(t_mob, b_mob).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    text.move_to(rect.get_center() + RIGHT * 0.68)
    return VGroup(rect, icon, text)


class P03S13InfraX(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "OpenCDA-InfraX"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        cards = VGroup(
            _feature_card("Sensor Config", "LiDAR / camera / radar\nswappable per deployment", ACCENT_GREEN, _sensor_icon(ACCENT_GREEN)),
            _feature_card("Multi-Modality", "V2V / V2I / V2X / I2I\ncovered in one platform", "#0891B2", _modality_icon("#0891B2")),
            _feature_card("Weather Variation", "rain / fog / snow / night\ncontrolled conditions", "#D97706", _weather_icon("#D97706")),
            _feature_card("Vector Maps", "HD lanes + semantics\nready for planning", "#7C3AED", _map_icon("#7C3AED")),
        )
        cards.arrange_in_grid(2, 2, buff=0.4)
        cards.move_to(ORIGIN + DOWN * 0.2)
        self.play(LaggedStart(*(FadeIn(c, scale=0.85) for c in cards), lag_ratio=0.2))
        badge = contribution_badge("OpenCDA-InfraX Platform", color=GOLD_KEY)
        badge.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(badge))
        self.wait(2)
        self._close()
