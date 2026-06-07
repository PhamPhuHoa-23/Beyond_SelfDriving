"""P03-S03 UCLA Smart Intersection."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ORANGE_INFRA, CYAN_RADAR, ACCENT_AMBER, ACCENT_BLUE,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    rsu_icon, vehicle_icon,
)

SCRIPT = """This is a working intersection at UCLA - sensors lit up at once."""


def _road_surface(width: float, height: float, *, horizontal: bool = True) -> VGroup:
    road = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.03,
        fill_color="#E8EEF3",
        fill_opacity=0.72,
        stroke_color="#CBD5E1",
        stroke_width=1.0,
        stroke_opacity=0.35,
    )
    lane_marks = VGroup()
    if horizontal:
        for x in np.linspace(-width / 2 + 0.65, width / 2 - 0.65, 12):
            lane_marks.add(Line(
                [x - 0.16, 0, 0], [x + 0.16, 0, 0],
                stroke_color=WHITE, stroke_width=2.0, stroke_opacity=0.55,
            ))
    else:
        for y in np.linspace(-height / 2 + 0.65, height / 2 - 0.65, 8):
            lane_marks.add(Line(
                [0, y - 0.16, 0], [0, y + 0.16, 0],
                stroke_color=WHITE, stroke_width=2.0, stroke_opacity=0.55,
            ))
    lane_marks.move_to(road)
    return VGroup(road, lane_marks)


def _coverage(center: np.ndarray, *, color: str = CYAN_RADAR) -> VGroup:
    rings = VGroup()
    for radius, opacity, width in [(0.42, 0.65, 2.3), (0.82, 0.38, 1.8), (1.22, 0.20, 1.4)]:
        ring = Circle(
            radius=radius,
            stroke_color=color,
            stroke_width=width,
            stroke_opacity=opacity,
            fill_opacity=0,
        )
        ring.move_to(center)
        rings.add(ring)
    return rings


def _sensor_wedge(source: np.ndarray, target: np.ndarray, *, color: str = ACCENT_AMBER) -> Polygon:
    direction = target - source
    theta = np.arctan2(direction[1], direction[0])
    spread = 34 * DEGREES
    length = min(2.35, np.linalg.norm(direction) * 0.92)
    p1 = source + length * np.array([np.cos(theta - spread), np.sin(theta - spread), 0])
    p2 = source + length * np.array([np.cos(theta + spread), np.sin(theta + spread), 0])
    return Polygon(source, p1, p2, fill_color=color, fill_opacity=0.13, stroke_width=0)


def _label(text: str, mob: Mobject, *, color: str = INK_MID, side=DOWN) -> Text:
    label = Text(text, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=color, weight=BOLD)
    label.next_to(mob, side, buff=0.12)
    return label


class P03S03SmartIntersection(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "UCLA Smart Intersection"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        road_h = _road_surface(11.9, 1.1, horizontal=True).move_to(DOWN * 0.08)
        road_v = _road_surface(1.18, 5.35, horizontal=False).move_to(DOWN * 0.08)
        hub = Circle(
            radius=0.46,
            fill_color=WHITE,
            fill_opacity=0.35,
            stroke_color="#CBD5E1",
            stroke_width=1.2,
        )
        hub.move_to(road_h.get_center())
        self.play(FadeIn(road_h), FadeIn(road_v), FadeIn(hub), run_time=0.8)

        rsu_nw = rsu_icon(color=ORANGE_INFRA).scale(1.0).move_to(LEFT * 3.15 + UP * 1.35)
        rsu_se = rsu_icon(color=ORANGE_INFRA).scale(1.0).move_to(RIGHT * 3.15 + DOWN * 1.5)
        rsu_lbls = VGroup(
            _label("RSU north-west", rsu_nw, color=ORANGE_INFRA, side=UP),
            _label("RSU south-east", rsu_se, color=ORANGE_INFRA, side=DOWN),
        )
        self.play(
            LaggedStart(GrowFromCenter(rsu_nw), GrowFromCenter(rsu_se), lag_ratio=0.2),
            FadeIn(rsu_lbls),
            run_time=0.9,
        )

        car1 = vehicle_icon(color=ACCENT_BLUE, scale=0.74).move_to(LEFT * 1.65 + DOWN * 0.28)
        car2 = vehicle_icon(color=ACCENT_BLUE, scale=0.74).move_to(RIGHT * 2.05 + UP * 0.32)
        car2.rotate(PI)
        car_lbls = VGroup(
            _label("CAV", car1, color=ACCENT_BLUE, side=DOWN),
            _label("CAV", car2, color=ACCENT_BLUE, side=UP),
        )
        self.play(FadeIn(car1), FadeIn(car2), FadeIn(car_lbls), run_time=0.7)

        center = hub.get_center()
        cone_nw = _sensor_wedge(rsu_nw.get_center(), center)
        cone_se = _sensor_wedge(rsu_se.get_center(), center)
        cov_nw = _coverage(rsu_nw.get_center())
        cov_se = _coverage(rsu_se.get_center())
        link = Line(
            rsu_nw.get_center(), rsu_se.get_center(),
            stroke_color=CYAN_RADAR,
            stroke_width=2.0,
            stroke_opacity=0.45,
        )
        link_flash = ShowPassingFlash(
            link.copy().set_stroke(CYAN_RADAR, width=4.0, opacity=0.95),
            time_width=0.35,
            run_time=1.1,
        )
        self.play(
            FadeIn(cone_nw),
            FadeIn(cone_se),
            LaggedStart(*(ShowCreation(r) for r in cov_nw), lag_ratio=0.12),
            LaggedStart(*(ShowCreation(r) for r in cov_se), lag_ratio=0.12),
            ShowCreation(link),
            run_time=1.2,
        )
        self.play(link_flash, Flash(hub, color=CYAN_RADAR, line_length=0.18, num_lines=10), run_time=1.1)

        caption = Text(
            "2 RSU  ·  2 CAV  ·  LiDAR  ·  Camera  ·  Radar  ·  C-V2X",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=INK_DARK,
        )
        caption.to_edge(DOWN, buff=0.66)
        self.play(FadeIn(caption))
        self.wait(2)
        self._close()
