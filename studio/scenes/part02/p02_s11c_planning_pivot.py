"""P02-S11c - Planning Pivot."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_PAPER,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    ORANGE_INFRA,
    RED_ERROR,
    SIZE_CAPS,
    SIZE_H1,
    SIZE_LABEL,
    ambient_glow,
    sensor_cone,
    vehicle_icon,
    write_chiseled,
)
from studio.scenes.part02._p02_helpers import road_grid_2d


SCRIPT = "Perception and prediction are inputs to planning; planning must be safe enough to stake a life on."


def set_layer(mob: Mobject, z: int) -> Mobject:
    if hasattr(mob, "set_z_index"):
        mob.set_z_index(z)
    return mob


def _check_mark(color=BG_PAPER, scale: float = 1.0) -> VGroup:
    p0 = LEFT * 0.08 + DOWN * 0.01
    p1 = LEFT * 0.02 + DOWN * 0.08
    p2 = RIGHT * 0.12 + UP * 0.10
    return VGroup(
        Line(p0, p1, stroke_color=color, stroke_width=2.3 * scale),
        Line(p1, p2, stroke_color=color, stroke_width=2.3 * scale),
    )


def label_chip(label: str, color: str, *, checked: bool = False, question: bool = False) -> VGroup:
    text = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
    width = max(1.20, text.get_width() + 0.64)
    rect = RoundedRectangle(
        width=width,
        height=0.34,
        corner_radius=0.12,
        fill_color=BG_PAPER,
        fill_opacity=0.90,
        stroke_color=color,
        stroke_width=1.8,
        stroke_opacity=0.92,
    )
    text.move_to(rect.get_center() + RIGHT * 0.10)

    marker = VGroup()
    if checked:
        disc = Circle(radius=0.115, fill_color=GREEN_FIX, fill_opacity=1.0, stroke_width=0)
        chk = _check_mark(scale=0.82).move_to(disc.get_center())
        marker = VGroup(disc, chk)
    elif question:
        disc = Circle(radius=0.115, fill_color=BG_PAPER, fill_opacity=1.0, stroke_color=color, stroke_width=1.7)
        q = Text("?", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=color, weight=BOLD)
        q.move_to(disc.get_center() + DOWN * 0.005)
        marker = VGroup(disc, q)
    else:
        marker = Dot(radius=0.055, color=color)

    marker.move_to(rect.get_left() + RIGHT * 0.22)
    return VGroup(rect, marker, text)


def human_silhouette(color=ORANGE_INFRA, h: float = 0.95) -> VGroup:
    head = Circle(radius=0.12 * h).set_fill(color, 1.0).set_stroke(width=0)
    body = Polygon(
        LEFT * 0.16 * h + DOWN * 0.55 * h,
        RIGHT * 0.16 * h + DOWN * 0.55 * h,
        RIGHT * 0.10 * h + UP * 0.18 * h,
        LEFT * 0.10 * h + UP * 0.18 * h,
    )
    body.round_corners(0.06)
    body.set_fill(color, 1.0).set_stroke(width=0)
    head.next_to(body, UP, buff=0.02)
    return VGroup(body, head)


def planning_lens(center: np.ndarray, radius: float = 0.78) -> VGroup:
    core = Circle(
        radius=radius,
        fill_color=ACCENT_BLUE,
        fill_opacity=0.035,
        stroke_color=ACCENT_BLUE,
        stroke_width=3.2,
        stroke_opacity=0.95,
    )
    inner = Circle(
        radius=radius * 0.55,
        fill_opacity=0,
        stroke_color=ACCENT_BLUE,
        stroke_width=1.8,
        stroke_opacity=0.45,
    )
    arcs = VGroup(
        Arc(radius=radius * 1.12, start_angle=0.10 * PI, angle=0.48 * PI),
        Arc(radius=radius * 1.12, start_angle=0.76 * PI, angle=0.36 * PI),
        Arc(radius=radius * 1.12, start_angle=1.46 * PI, angle=0.42 * PI),
    )
    arcs.set_stroke(ACCENT_BLUE, width=5.0, opacity=0.82)
    cross = VGroup(
        Line(LEFT * radius * 0.32, RIGHT * radius * 0.32, stroke_color=ACCENT_BLUE, stroke_width=1.4, stroke_opacity=0.42),
        Line(DOWN * radius * 0.32, UP * radius * 0.32, stroke_color=ACCENT_BLUE, stroke_width=1.4, stroke_opacity=0.42),
        Dot(radius=0.055, color=ACCENT_BLUE),
    )
    lens = VGroup(core, inner, arcs, cross)
    lens.move_to(center)
    return lens


def risk_ring(center: np.ndarray) -> VGroup:
    rings = VGroup()
    for radius, fill_opacity, stroke_opacity in [(0.78, 0.04, 0.22), (0.58, 0.06, 0.36), (0.40, 0.08, 0.62)]:
        rings.add(Circle(
            radius=radius,
            fill_color=RED_ERROR,
            fill_opacity=fill_opacity,
            stroke_color=RED_ERROR,
            stroke_width=1.7,
            stroke_opacity=stroke_opacity,
        ).move_to(center))
    return rings


def candidate_path(
    points: list[np.ndarray],
    color: str,
    *,
    dashed: bool = False,
    width: float = 4.0,
    opacity: float = 0.90,
) -> VMobject:
    path = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    path.set_points_smoothly(points)
    if dashed:
        path = DashedVMobject(path, num_dashes=22)
        path.set_stroke(color, width=width, opacity=opacity)
    return path


def safe_corridor(points: list[np.ndarray]) -> VGroup:
    band = VMobject(stroke_color=GREEN_FIX, stroke_width=34, stroke_opacity=0.16)
    band.set_points_smoothly(points)
    center = VMobject(stroke_color=GREEN_FIX, stroke_width=4.4, stroke_opacity=0.96)
    center.set_points_smoothly(points)
    return VGroup(band, center)


def detection_brackets(center: np.ndarray, *, width: float = 0.86, height: float = 1.12) -> VGroup:
    corners = [
        center + LEFT * width / 2 + UP * height / 2,
        center + RIGHT * width / 2 + UP * height / 2,
        center + LEFT * width / 2 + DOWN * height / 2,
        center + RIGHT * width / 2 + DOWN * height / 2,
    ]
    dirs = [(RIGHT, DOWN), (LEFT, DOWN), (RIGHT, UP), (LEFT, UP)]
    marks = VGroup()
    for corner, (x_dir, y_dir) in zip(corners, dirs):
        marks.add(Line(corner, corner + x_dir * 0.20, stroke_color=ACCENT_TEAL, stroke_width=2.6))
        marks.add(Line(corner, corner + y_dir * 0.20, stroke_color=ACCENT_TEAL, stroke_width=2.6))
    return marks


class P02S11CPlanningPivot(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "From Understanding to Planning"

    def construct(self):
        self._open(self.SCENE_TITLE)

        road = road_grid_2d(width=12.2, height=4.8).move_to(DOWN * 0.25)
        road.set_opacity(0.34)
        set_layer(road, -5)

        ego = vehicle_icon(color=ACCENT_BLUE, scale=0.64)
        ego.move_to(LEFT * 4.35 + DOWN * 0.95)
        set_layer(ego, 4)
        human = human_silhouette().move_to(RIGHT * 1.45 + DOWN * 0.20)
        set_layer(human, 7)
        human_shadow = Circle(
            radius=0.33,
            fill_color=INK_MID,
            fill_opacity=0.08,
            stroke_width=0,
        ).move_to(human.get_center() + DOWN * 0.36)
        set_layer(human_shadow, 1)

        self.play(FadeIn(road), FadeIn(ego), FadeIn(human_shadow), FadeIn(human), run_time=0.9)

        ego_front = ego.get_right() + RIGHT * 0.08
        lens_center = LEFT * 2.45 + DOWN * 0.55
        human_center = human.get_center()

        # Perception: the scene is seen, not merely named.
        cone = sensor_cone(ego_front, color=ACCENT_TEAL, spread=PI / 5.2, length=4.9, n_levels=10)
        cone.set_opacity(0.50)
        set_layer(cone, -1)
        brackets = detection_brackets(human_center)
        set_layer(brackets, 8)
        blips = VGroup(
            Dot(human_center + LEFT * 0.34 + UP * 0.36, radius=0.055, color=ACCENT_TEAL),
            Dot(human_center + RIGHT * 0.30 + DOWN * 0.28, radius=0.050, color=ACCENT_TEAL),
            Dot(human_center + LEFT * 0.28 + DOWN * 0.16, radius=0.042, color=ACCENT_TEAL),
        )
        set_layer(blips, 8)
        perception_chip = label_chip("Perception", ACCENT_TEAL, checked=True).scale(0.90)
        prediction_chip = label_chip("Prediction", ACCENT_TEAL, checked=True).scale(0.90)
        VGroup(perception_chip, prediction_chip).arrange(RIGHT, buff=0.14).move_to(lens_center + UP * 1.42 + RIGHT * 0.06)
        set_layer(perception_chip, 9)
        set_layer(prediction_chip, 9)

        self.play(FadeIn(cone), ShowCreation(brackets), FadeIn(blips), FadeIn(perception_chip), run_time=1.15)
        self.wait(0.25)

        # Prediction is carried by the verified chip; avoid extra marks near the human.
        self.play(FadeIn(prediction_chip), run_time=0.8)
        self.wait(0.45)

        # Planning: understanding gets gathered into a decision lens.
        lens = planning_lens(lens_center)
        lens_glow = ambient_glow(lens[0], color=ACCENT_BLUE, radius=1.15).set_opacity(0.24)
        set_layer(lens_glow, 0)
        set_layer(lens, 5)
        planning_chip = label_chip("Planning", ACCENT_BLUE, question=True).scale(0.90).move_to(lens_center + UP * 1.02)
        set_layer(planning_chip, 9)
        flow_perception = candidate_path(
            [human_center + LEFT * 0.40 + UP * 0.40, LEFT * 0.15 + UP * 0.95, lens_center + RIGHT * 0.36 + UP * 0.18],
            ACCENT_TEAL,
            width=2.2,
            opacity=0.26,
        )
        set_layer(flow_perception, 3)
        evidence_dot_a = Dot(radius=0.060, color=ACCENT_TEAL).move_to(flow_perception.get_start())
        set_layer(evidence_dot_a, 6)

        self.add(lens_glow)
        self.play(FadeIn(lens_glow), ShowCreation(lens), FadeIn(planning_chip), run_time=0.85)
        self.play(
            ShowCreation(flow_perception),
            MoveAlongPath(evidence_dot_a, flow_perception),
            ShowPassingFlash(flow_perception.copy().set_stroke(ACCENT_BLUE, width=5.0, opacity=0.82), time_width=0.45),
            run_time=1.15,
        )

        # Decision: the unsafe candidate is visible, then planning rejects it.
        danger = risk_ring(human_center)
        set_layer(danger, 4)
        red_path = candidate_path(
            [
                ego_front,
                LEFT * 2.30 + DOWN * 0.78,
                LEFT * 0.45 + DOWN * 0.50,
                human_center,
                RIGHT * 3.80 + DOWN * 0.10,
            ],
            RED_ERROR,
            dashed=True,
            width=4.2,
            opacity=0.72,
        )
        set_layer(red_path, 2)
        safe_points = [
            ego_front,
            LEFT * 2.85 + DOWN * 1.04,
            LEFT * 1.10 + DOWN * 1.42,
            RIGHT * 1.45 + DOWN * 1.54,
            RIGHT * 3.40 + DOWN * 1.22,
            RIGHT * 4.90 + DOWN * 0.82,
        ]
        corridor = safe_corridor(safe_points)
        set_layer(corridor, 3)

        self.play(
            cone.animate.set_opacity(0.12),
            VGroup(brackets, blips, flow_perception).animate.set_opacity(0.22),
            ShowCreation(danger),
            ShowCreation(red_path),
            run_time=1.0,
        )
        self.add(human_shadow, human)
        self.play(red_path.animate.set_opacity(0.16), danger.animate.set_opacity(0.78), run_time=0.55)
        self.play(ShowCreation(corridor[0]), ShowCreation(corridor[1]), run_time=1.15)

        hook_text = Text(
            "safe enough to stake a life on.",
            font=FONT_PRIMARY,
            font_size=SIZE_H1,
            color=GOLD_RICH,
            slant=ITALIC,
        )
        hook_text.move_to(DOWN * 3.05)
        self.play(write_chiseled(hook_text, run_time=2.2))
        self.play(
            ShowPassingFlash(
                danger.copy().set_stroke(ORANGE_INFRA, width=5.5, opacity=0.65),
                time_width=0.70,
                run_time=0.95,
            )
        )
        self.wait(1.1)
        self._close()
