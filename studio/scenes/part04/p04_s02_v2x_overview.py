"""P04-S02 V2X overview and deployment bottlenecks."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN,
    ACCENT_AMBER, RED_ERROR, CYAN_RADAR, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, SIZE_MICRO,
    vehicle_icon, rsu_icon, pedestrian_icon,
)

SCRIPT = """V2X lets agents borrow another viewpoint, but data, training, and inference costs block deployment."""


def _txt(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def _road_intersection() -> VGroup:
    road_color = "#DDE7F1"
    horizontal = RoundedRectangle(
        width=4.25, height=0.62, corner_radius=0.06,
        fill_color=road_color, fill_opacity=1.0, stroke_width=0,
    )
    vertical = RoundedRectangle(
        width=0.62, height=2.35, corner_radius=0.06,
        fill_color=road_color, fill_opacity=1.0, stroke_width=0,
    )
    lanes = VGroup(
        DashedLine(LEFT * 1.82, RIGHT * 1.82, dash_length=0.1, stroke_color=WHITE, stroke_width=1.6, stroke_opacity=0.88),
        DashedLine(DOWN * 0.92, UP * 0.92, dash_length=0.1, stroke_color=WHITE, stroke_width=1.6, stroke_opacity=0.88),
    )
    crosswalk = VGroup(*[
        Line(LEFT * 0.22, RIGHT * 0.22, stroke_color=WHITE, stroke_width=2.0, stroke_opacity=0.86)
        for _ in range(5)
    ]).arrange(DOWN, buff=0.08)
    crosswalk.move_to(RIGHT * 0.58 + UP * 0.48)
    return VGroup(horizontal, vertical, lanes, crosswalk)


def _sensor_wedge(source: np.ndarray, target: np.ndarray, color: str) -> Polygon:
    direction = target - source
    unit = direction / np.linalg.norm(direction)
    perp = np.array([-unit[1], unit[0], 0])
    return Polygon(
        source,
        target + perp * 0.48,
        target - perp * 0.48,
        fill_color=color,
        fill_opacity=0.11,
        stroke_color=color,
        stroke_width=1.0,
        stroke_opacity=0.38,
    )


def _v2x_scene() -> VGroup:
    roads = _road_intersection()
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.43).move_to(LEFT * 1.2 + DOWN * 0.08)
    cav = vehicle_icon(color=ACCENT_TEAL, scale=0.4).move_to(DOWN * 0.75 + RIGHT * 0.05)
    cav.rotate(PI / 2)
    rsu = rsu_icon(color=ACCENT_AMBER).scale(0.7).move_to(RIGHT * 1.45 + UP * 0.72)
    pedestrian = pedestrian_icon(color=RED_ERROR).scale(0.54).move_to(RIGHT * 0.62 + UP * 0.48)
    blocker = vehicle_icon(color=INK_MID, scale=0.47).move_to(LEFT * 0.1 + UP * 0.08)

    ego_view = _sensor_wedge(ego.get_center(), RIGHT * 0.08 + UP * 0.08, ACCENT_BLUE)
    cav_view = _sensor_wedge(cav.get_center(), pedestrian.get_center(), ACCENT_TEAL)
    rsu_view = _sensor_wedge(rsu.get_center(), pedestrian.get_center(), ACCENT_AMBER)
    links = VGroup(
        DashedLine(cav.get_center(), ego.get_center(), dash_length=0.07, stroke_color=CYAN_RADAR, stroke_width=1.4),
        DashedLine(rsu.get_center(), ego.get_center(), dash_length=0.07, stroke_color=CYAN_RADAR, stroke_width=1.4),
    )
    labels = VGroup(
        _txt("ego", size=SIZE_MICRO + 1, color=ACCENT_BLUE, weight=BOLD).next_to(ego, DOWN, buff=0.05),
        _txt("CAV", size=SIZE_MICRO + 1, color=ACCENT_TEAL, weight=BOLD).next_to(cav, LEFT, buff=0.05),
        _txt("RSU", size=SIZE_MICRO + 1, color=ACCENT_AMBER, weight=BOLD).next_to(rsu, UP, buff=0.04),
    )
    return VGroup(roads, ego_view, cav_view, rsu_view, links, pedestrian, blocker, ego, cav, rsu, labels)


def _fusion_view() -> VGroup:
    frame = RoundedRectangle(
        width=2.05, height=1.52, corner_radius=0.12,
        fill_color=interpolate_color(ACCENT_GREEN, WHITE, 0.9),
        fill_opacity=1.0, stroke_color=ACCENT_GREEN, stroke_width=2.0,
    )
    grid = VGroup()
    for x in (-0.55, 0, 0.55):
        grid.add(Line(UP * 0.48, DOWN * 0.48, stroke_color=INK_MID, stroke_width=0.8, stroke_opacity=0.18).shift(RIGHT * x))
    for y in (-0.32, 0, 0.32):
        grid.add(Line(LEFT * 0.78, RIGHT * 0.78, stroke_color=INK_MID, stroke_width=0.8, stroke_opacity=0.18).shift(UP * y))
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.22).move_to(LEFT * 0.42 + DOWN * 0.18)
    ped = pedestrian_icon(color=ACCENT_GREEN).scale(0.31).move_to(RIGHT * 0.34 + UP * 0.18)
    detect = RoundedRectangle(
        width=0.45, height=0.58, corner_radius=0.04,
        fill_opacity=0, stroke_color=ACCENT_GREEN, stroke_width=1.6,
    ).move_to(ped)
    title = _txt("fused scene", size=SIZE_CAPS, color=ACCENT_GREEN, weight=BOLD)
    title.next_to(frame, UP, buff=0.1)
    return VGroup(frame, grid, ego, ped, detect, title)


def _data_icon(color: str) -> VGroup:
    points = VGroup(*[
        Dot(radius=0.035, fill_color=color, fill_opacity=0.78, stroke_width=0).move_to([x, y, 0])
        for x, y in [(-0.34, 0.2), (-0.12, 0.32), (0.14, 0.22), (0.32, 0.05), (-0.25, -0.1), (0.02, -0.2)]
    ])
    box = RoundedRectangle(width=0.5, height=0.32, corner_radius=0.04, fill_opacity=0, stroke_color=color, stroke_width=1.5)
    box.move_to(RIGHT * 0.15)
    return VGroup(points, box)


def _training_icon(color: str) -> VGroup:
    chip = RoundedRectangle(
        width=0.62, height=0.5, corner_radius=0.06,
        fill_color=interpolate_color(color, WHITE, 0.72),
        fill_opacity=1, stroke_color=color, stroke_width=1.5,
    )
    core = _txt("GPU", size=SIZE_MICRO, color=color, weight=BOLD).move_to(chip)
    tasks = VGroup(*[
        Circle(radius=0.08, fill_color=color, fill_opacity=0.22, stroke_color=color, stroke_width=1.0)
        for _ in range(3)
    ]).arrange(DOWN, buff=0.08).move_to(LEFT * 0.52)
    links = VGroup(*[
        Line(task.get_right(), chip.get_left(), stroke_color=color, stroke_width=1.1)
        for task in tasks
    ])
    return VGroup(links, tasks, chip, core)


def _inference_icon(color: str) -> VGroup:
    chip = RoundedRectangle(
        width=0.58, height=0.48, corner_radius=0.06,
        fill_color=interpolate_color(color, WHITE, 0.74),
        fill_opacity=1, stroke_color=color, stroke_width=1.5,
    ).move_to(LEFT * 0.22)
    clock = Circle(radius=0.28, fill_opacity=0, stroke_color=color, stroke_width=1.5).move_to(RIGHT * 0.38)
    hands = VGroup(
        Line(clock.get_center(), clock.get_center() + UP * 0.14, stroke_color=color, stroke_width=1.5),
        Line(clock.get_center(), clock.get_center() + RIGHT * 0.12, stroke_color=color, stroke_width=1.5),
    )
    return VGroup(chip, clock, hands)


def _bottleneck_card(number: str, title: str, body: str, color: str, icon: Mobject) -> VGroup:
    card = RoundedRectangle(
        width=3.65, height=1.35, corner_radius=0.14,
        fill_color=interpolate_color(color, WHITE, 0.92),
        fill_opacity=1.0, stroke_color=color, stroke_width=2.0,
    )
    number_mob = _txt(number, size=SIZE_LABEL + 2, color=ACCENT_AMBER, weight=BOLD)
    number_mob.move_to(card.get_left() + RIGHT * 0.3 + UP * 0.37)
    icon.scale(0.78).move_to(card.get_left() + RIGHT * 0.84 + DOWN * 0.12)
    title_mob = _txt(title, size=SIZE_LABEL - 1, color=color, weight=BOLD)
    body_mob = _txt(body, size=SIZE_CAPS - 2, color=INK_MID)
    copy = VGroup(title_mob, body_mob).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    copy.move_to(card.get_center() + RIGHT * 0.58)
    return VGroup(card, number_mob, icon, copy)


class P04S02V2XOverview(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "V2X Deployment Bottlenecks"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        top_y = 1.18
        arrow_y = 1.08

        v2x = _v2x_scene().scale(0.84).move_to(LEFT * 3.85 + UP * top_y)
        borrowing = _txt("borrow another viewpoint", size=SIZE_LABEL, color=ACCENT_BLUE, weight=BOLD)
        borrowing.next_to(v2x, UP, buff=0.08)

        fusion = _fusion_view().move_to(RIGHT * 0.1 + UP * top_y)
        fuse_arrow = Arrow(
            np.array([v2x.get_right()[0] + 0.08, arrow_y, 0]),
            np.array([fusion.get_left()[0] - 0.08, arrow_y, 0]),
            buff=0, stroke_width=2.2, fill_color=ACCENT_GREEN,
            max_tip_length_to_length_ratio=0.1,
        )

        deployment = VGroup(
            _txt("REAL DEPLOYMENT", size=SIZE_CAPS, color=ACCENT_AMBER, weight=BOLD),
            _txt("millions of intersections", size=SIZE_LABEL - 1, color=INK_DARK, weight=BOLD),
            _txt("pedestrian safety", size=SIZE_CAPS, color=INK_MID),
        ).arrange(DOWN, buff=0.08)
        deployment.move_to(RIGHT * 4.35 + UP * top_y)
        deploy_arrow = Arrow(
            np.array([fusion.get_right()[0] + 0.08, arrow_y, 0]),
            np.array([deployment.get_left()[0] - 0.18, arrow_y, 0]),
            buff=0, stroke_width=2.2, fill_color=ACCENT_AMBER,
            max_tip_length_to_length_ratio=0.1,
        )
        funding_text = _txt("US DoT smart intersections", size=SIZE_MICRO, color=ACCENT_AMBER, weight=BOLD)
        funding = RoundedRectangle(
            width=funding_text.get_width() + 0.42, height=0.36, corner_radius=0.09,
            fill_color=interpolate_color(ACCENT_AMBER, WHITE, 0.78),
            fill_opacity=1, stroke_color=ACCENT_AMBER, stroke_width=1.3,
        )
        funding_text.move_to(funding)
        funding_badge = VGroup(funding, funding_text)
        funding_badge.next_to(deployment, DOWN, buff=0.16)

        cards = VGroup(
            _bottleneck_card("01", "DATA", "3D labels\ndo not scale", RED_ERROR, _data_icon(RED_ERROR)),
            _bottleneck_card("02", "TRAINING", "multi-agent tasks\nconsume months", "#7C3AED", _training_icon("#7C3AED")),
            _bottleneck_card("03", "INFERENCE", "edge hardware\nmust stay real-time", ACCENT_GREEN, _inference_icon(ACCENT_GREEN)),
        ).arrange(RIGHT, buff=0.34)
        cards.move_to(DOWN * 1.48)

        scale_label = _txt("What breaks when the stack scales?", size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        scale_label.move_to(DOWN * 0.34)
        guide = Line(LEFT * 5.2, RIGHT * 5.2, stroke_color=ACCENT_AMBER, stroke_width=1.5, stroke_opacity=0.5)
        guide.next_to(scale_label, DOWN, buff=0.12)
        connectors = VGroup(*[
            Line(
                [card.get_center()[0], guide.get_y(), 0],
                [card.get_center()[0], card.get_top()[1] + 0.07, 0],
                stroke_color=ACCENT_AMBER, stroke_width=1.2, stroke_opacity=0.55,
            )
            for card in cards
        ])

        footer = _txt("A lab demo must survive all three.", size=SIZE_LABEL, color=ACCENT_AMBER, weight=BOLD)
        footer.move_to(DOWN * 2.7)

        self.play(FadeIn(v2x), FadeIn(borrowing), run_time=0.65)
        self.play(
            LaggedStart(
                ShowCreation(v2x[2]),
                ShowCreation(v2x[3]),
                ShowCreation(v2x[4]),
                lag_ratio=0.12,
            ),
            run_time=0.7,
        )
        self.play(ShowCreation(fuse_arrow), FadeIn(fusion), run_time=0.6)
        self.play(ShowCreation(deploy_arrow), FadeIn(deployment), FadeIn(funding_badge), run_time=0.65)
        self.play(FadeIn(scale_label), ShowCreation(guide), ShowCreation(connectors), run_time=0.5)
        self.play(LaggedStart(*(FadeIn(card, shift=UP * 0.18) for card in cards), lag_ratio=0.18), run_time=0.9)
        self.play(FadeIn(footer), run_time=0.35)
        self.wait(1.7)
        self._close()
