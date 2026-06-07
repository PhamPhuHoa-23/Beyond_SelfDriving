"""Agent icons — vehicles, pedestrians, RSUs, drones, trails."""
from __future__ import annotations
from manimlib import *
from studio.components.colors import (
    ACCENT_BLUE, GOLD_KEY, ORANGE_INFRA, INK_LIGHT, INK_DARK, CYAN_RADAR,
)


def vehicle_icon(*, color: str = ACCENT_BLUE, scale: float = 1.0) -> VGroup:
    """Proper top-down car: body, roof, wheels, and windshield line."""
    body = RoundedRectangle(
        width=1.1, height=0.55, corner_radius=0.1,
        fill_color=color, fill_opacity=1.0,
        stroke_color=color, stroke_width=1.0,
    )
    roof = RoundedRectangle(
        width=0.58, height=0.36, corner_radius=0.08,
        fill_color=interpolate_color(color, WHITE, 0.25), fill_opacity=0.9,
        stroke_width=0,
    )
    roof.move_to(body.get_center() + LEFT * 0.05)
    windshield = Line(
        roof.get_corner(UR) + LEFT * 0.04,
        roof.get_corner(DR) + LEFT * 0.04,
        stroke_color=interpolate_color(color, WHITE, 0.6),
        stroke_width=1.5,
    )
    wheel_color = interpolate_color(color, BLACK, 0.55)
    wheels = VGroup()
    for dx, dy in [(0.42, 0.22), (0.42, -0.22), (-0.42, 0.22), (-0.42, -0.22)]:
        wheel = RoundedRectangle(
            width=0.2, height=0.12, corner_radius=0.04,
            fill_color=wheel_color, fill_opacity=1.0, stroke_width=0,
        )
        wheel.move_to(body.get_center() + RIGHT * dx + UP * dy)
        wheels.add(wheel)
    icon = VGroup(body, wheels, roof, windshield)
    icon.scale(scale)
    return icon


def vehicle_icon_3d(*, color: str = ACCENT_BLUE, scale: float = 1.0) -> VGroup:
    """Small extruded car for 3D scenes: body, raised cabin, wheels, headlights."""
    body = Prism(width=1.18, height=0.56, depth=0.22, color=color, opacity=1.0)
    body.set_color(color)
    body.move_to(OUT * 0.12)

    cabin_color = interpolate_color(color, WHITE, 0.28)
    cabin = Prism(width=0.56, height=0.38, depth=0.2, color=cabin_color, opacity=0.95)
    cabin.set_color(cabin_color)
    cabin.move_to(LEFT * 0.08 + OUT * 0.34)

    wheel_color = interpolate_color(color, BLACK, 0.62)
    wheels = Group()
    for dx, dy in [(0.43, 0.3), (0.43, -0.3), (-0.43, 0.3), (-0.43, -0.3)]:
        wheel = Prism(width=0.22, height=0.08, depth=0.16, color=wheel_color, opacity=1.0)
        wheel.set_color(wheel_color)
        wheel.move_to(RIGHT * dx + UP * dy + OUT * 0.09)
        wheels.add(wheel)

    headlights = VGroup()
    for dy in [-0.14, 0.14]:
        lamp = Dot(radius=0.04, color="#FEF08A")
        lamp.move_to(RIGHT * 0.6 + UP * dy + OUT * 0.22)
        headlights.add(lamp)

    windshield = Rectangle(
        width=0.06, height=0.3,
        fill_color=interpolate_color(color, WHITE, 0.68),
        fill_opacity=0.82,
        stroke_width=0,
    )
    windshield.move_to(cabin.get_center() + RIGHT * 0.2 + OUT * 0.12)

    car = Group(body, wheels, cabin, windshield, headlights)
    car.scale(scale)
    return car


def pedestrian_icon(*, color: str = GOLD_KEY) -> VGroup:
    """Detailed stick figure: larger head, angled arms, walking legs."""
    head = Circle(radius=0.12, fill_color=color, fill_opacity=1.0,
                  stroke_color=interpolate_color(color, WHITE, 0.35), stroke_width=1.0)
    body = Line(ORIGIN, DOWN * 0.38, stroke_color=color, stroke_width=3.0)
    shoulder = body.point_from_proportion(0.35)
    hip = body.get_end()
    arm_l = Line(shoulder, shoulder + LEFT * 0.2 + DOWN * 0.12,
                 stroke_color=color, stroke_width=2.5)
    arm_r = Line(shoulder, shoulder + RIGHT * 0.22 + UP * 0.08,
                 stroke_color=color, stroke_width=2.5)
    leg_l = Line(hip, hip + LEFT * 0.2 + DOWN * 0.22,
                 stroke_color=color, stroke_width=2.5)
    leg_r = Line(hip, hip + RIGHT * 0.18 + DOWN * 0.18,
                 stroke_color=color, stroke_width=2.5)
    head.next_to(body, UP, buff=0.04)
    return VGroup(head, body, leg_l, leg_r, arm_l, arm_r)


def rsu_icon(*, color: str = ORANGE_INFRA) -> VGroup:
    """2D RSU: base, antenna, beacon, and subtle signal glow."""
    base = Square(side_length=0.28, fill_color=color, fill_opacity=0.9,
                  stroke_color=color, stroke_width=1.5)
    antenna = Triangle(fill_color=color, fill_opacity=0.9, stroke_width=0)
    antenna.scale(0.18)
    antenna.next_to(base, UP, buff=0.0)
    dot = Dot(radius=0.05, color=color)
    dot.next_to(antenna, UP, buff=0.04)
    glow = VGroup()
    for r, alpha in [(0.18, 0.28), (0.3, 0.16)]:
        ring = Circle(radius=r, stroke_color=CYAN_RADAR, stroke_width=1.2,
                      stroke_opacity=alpha)
        ring.move_to(dot)
        glow.add(ring)
    return VGroup(base, antenna, dot, glow)


def rsu_tower_3d(*, color: str = ORANGE_INFRA, height: float = 2.0) -> VGroup:
    """3D lattice tower: 4 legs + cross struts.
    # Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py:68
    """
    corners = [UP * 0 + d for d in compass_directions(4)]
    legs = VGroup(*(Line(c, c * 0.3 + height * OUT, stroke_color=color,
                         stroke_width=2) for c in corners))
    n_cross = 4
    struts = VGroup()
    for leg_a, leg_b in zip(legs, [*legs[1:], legs[0]]):
        pts_a = [leg_a.pfp(t) for t in np.linspace(0, 1, n_cross + 1)]
        pts_b = [leg_b.pfp(t) for t in np.linspace(0, 1, n_cross + 1)]
        for pa, pb in zip(pts_a[:-1], pts_b[1:]):
            struts.add(Line(pa, pb, stroke_color=color, stroke_width=1.2))
        for pa, pb in zip(pts_a[1:], pts_b[:-1]):
            struts.add(Line(pa, pb, stroke_color=color, stroke_width=1.2))
    tower = VGroup(legs, struts)
    tower.set_depth(height, stretch=True)
    return tower


def drone_icon(*, color: str = INK_LIGHT) -> VGroup:
    """Top-down drone: center circle + 4 rotor circles."""
    center = Circle(radius=0.1, fill_color=color, fill_opacity=0.8, stroke_width=0)
    rotors = VGroup(*(
        Circle(radius=0.12, fill_color=color, fill_opacity=0.5,
               stroke_color=color, stroke_width=1.5)
        for _ in range(4)
    ))
    for r, d in zip(rotors, compass_directions(4)):
        r.move_to(center.get_center() + 0.28 * d)
    return VGroup(center, rotors)


def agent_trail(mob: Mobject, *, color: str, max_length: float = 2.0) -> TracedPath:
    """Fading trail behind a moving agent.
    # Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py
    """
    return TracedPath(
        mob.get_center,
        stroke_color=color,
        stroke_width=2.5,
        stroke_opacity=[0, 1],
        time_traced=0.4,
    )
