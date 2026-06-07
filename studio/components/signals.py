"""Radar shells, sensor cones, V2X links, ambient glow, wave interference."""
from __future__ import annotations
from manimlib import *
from studio.components.colors import CYAN_RADAR, ACCENT_TEAL, ACCENT_AMBER


def _spherical_shell(
    radius: float,
    *,
    color: str,
    stroke_width: float,
    opacity: float,
    squash: float = 0.66,
    planes: int = 3,
) -> VGroup:
    """Projected sphere shell: several tilted ellipses plus a soft outer glow."""
    shell = VGroup()
    glow = Circle(
        radius=radius,
        stroke_color=color,
        stroke_width=stroke_width * 3.0,
        stroke_opacity=opacity * 0.1,
    )
    shell.add(glow)
    angles = [0, PI / 2, PI / 4, -PI / 4][:planes]
    opacities = [1.0, 0.68, 0.42, 0.42][:planes]
    for angle, alpha_scale in zip(angles, opacities):
        ring = Ellipse(
            width=radius * 2,
            height=radius * 2 * squash,
            stroke_color=color,
            stroke_width=stroke_width,
            stroke_opacity=opacity * alpha_scale,
            fill_opacity=0,
        )
        ring.rotate(angle)
        shell.add(ring)
    return shell


def _expanding_sphere_shell(
    *,
    color: str,
    opacity: float,
    stroke_width: float,
) -> Group:
    """Unit spherical wavefront: actual transparent sphere, not ring geometry."""
    surface = Sphere(radius=1.0, resolution=(64, 32))
    surface.set_color(color)
    surface.set_opacity(opacity * 0.06)

    glow = Sphere(radius=1.08, resolution=(48, 24))
    glow.set_color(color)
    glow.set_opacity(opacity * 0.035)

    mesh = SurfaceMesh(
        surface,
        resolution=(25, 13),
        stroke_color=color,
        stroke_width=max(0.45, stroke_width * 0.42),
        normal_nudge=0.012,
        depth_test=False,
    )
    mesh.set_stroke(color, width=max(0.45, stroke_width * 0.42), opacity=opacity * 0.7)
    return Group(glow, surface, mesh)


def spherical_coverage_3d(
    center: np.ndarray,
    *,
    color: str = CYAN_RADAR,
    radius: float = 3.0,
    opacity: float = 0.1,
) -> Group:
    """Static transparent spherical coverage volume for 3D overlap moments."""
    outer = Sphere(radius=radius, resolution=(64, 32))
    outer.set_color(color)
    outer.set_opacity(opacity * 0.46)
    inner = Sphere(radius=radius * 0.72, resolution=(48, 24))
    inner.set_color(color)
    inner.set_opacity(opacity * 0.16)
    bubble = Group(outer, inner)
    bubble.move_to(center)
    return bubble


def sort_spherical_waves_to_camera(shells: Mobject, camera) -> Mobject:
    """Use 3b1b's transparent-surface pattern: sort sphere surfaces to camera."""
    for mob in shells.family_members_with_points():
        if isinstance(mob, Surface):
            mob.always_sort_to_camera(camera)
    return shells


def radar_shells_2d(
    center: np.ndarray,
    *,
    color: str = CYAN_RADAR,
    n_shells: int = 5,
    max_radius: float = 3.0,
) -> tuple[VGroup, LaggedStart]:
    """Gravitational-wave shells with projected-sphere glow and uneven spacing."""
    shells = Group()
    radii = [max_radius * ((i + 1) / n_shells) ** 1.6 for i in range(n_shells)]
    for i, r in enumerate(radii):
        opacity = 0.86 * (1 - i / (n_shells + 1)) ** 0.8
        width = max(1.0, 2.8 - i * 0.35)
        shell = _spherical_shell(
            r, color=color, stroke_width=width, opacity=opacity,
            squash=0.72, planes=4,
        )
        shell.move_to(center)
        shells.add(shell)
    anims = [ShowCreation(s, run_time=0.42 + i * 0.06) for i, s in enumerate(shells)]
    return shells, LaggedStart(*anims, lag_ratio=0.16)


def radar_shells_3d(
    center: np.ndarray,
    *,
    color: str = CYAN_RADAR,
    n_shells: int = 4,
    max_radius: float = 3.5,
) -> tuple[Group, LaggedStart]:
    """3D radar pulses that actually expand outward as fading spherical shells."""
    shells = Group()
    radii = [max_radius * ((i + 1) / n_shells) ** 1.5 for i in range(n_shells)]
    anims = []
    seed_scale = 0.045
    for i, r in enumerate(radii):
        opacity = 0.92 * (1 - i / (n_shells + 1)) ** 0.7
        width = max(0.8, 1.7 - i * 0.18)
        shell = _expanding_sphere_shell(color=color, opacity=opacity, stroke_width=width)
        shell.scale(seed_scale)
        shell.move_to(center)
        shells.add(shell)
        anims.append(
            shell.animate(run_time=0.85 + i * 0.08, rate_func=smooth)
            .scale(r / seed_scale)
            .set_opacity(0.06)
        )
    return shells, LaggedStart(*anims, lag_ratio=0.18)


def sensor_cone(
    source: np.ndarray,
    *,
    color: str = ACCENT_AMBER,
    spread: float = PI / 4,
    length: float = 3.5,
    n_levels: int = 8,
) -> VGroup:
    """Sensor FOV frustum as layered AnnularSectors with opacity falloff."""
    sectors = VGroup()
    dr = length / n_levels
    for i in range(n_levels):
        r_inner = i * dr
        r_outer = r_inner + dr
        alpha = (1.0 - i / n_levels) * 0.45
        s = AnnularSector(
            inner_radius=r_inner,
            outer_radius=r_outer,
            start_angle=-spread / 2,
            angle=spread,
            arc_center=source,
            fill_color=color,
            fill_opacity=alpha,
            stroke_width=0,
        )
        sectors.add(s)
    return sectors


def v2x_link(
    a: Mobject,
    b: Mobject,
    *,
    color: str = ACCENT_TEAL,
) -> tuple[Line, ShowPassingFlash]:
    """Thin line between two agents + animated packet pulse."""
    line = Line(a.get_center(), b.get_center(),
                stroke_color=color, stroke_width=1.5, stroke_opacity=0.5)
    flash = ShowPassingFlash(
        line.copy().set_stroke(color, width=4, opacity=1.0),
        time_width=0.4, run_time=1.0,
    )
    return line, flash


def ambient_glow(center: Mobject, *, color: str, radius: float = 0.8) -> VGroup:
    """Concentric annuli with radial opacity falloff."""
    glow = VGroup()
    n = 8
    dr = radius / n
    c = center.get_center()
    for i in range(n):
        r_inner = i * dr
        r_outer = r_inner + dr
        alpha = 0.35 * (1.0 - i / n) ** 2
        annulus = Annulus(inner_radius=r_inner, outer_radius=r_outer,
                          fill_color=color, fill_opacity=alpha, stroke_width=0)
        annulus.move_to(c)
        glow.add(annulus)
    return glow


def interference_pattern(
    sources: list[np.ndarray],
    *,
    color: str,
    n_rings: int = 6,
    max_r: float = 3.0,
) -> VGroup:
    """Multi-source projected-shell overlay plus bright constructive nodes."""
    all_rings = VGroup()
    for src in sources:
        for i in range(n_rings):
            r = max_r * ((i + 1) / n_rings) ** 1.25
            ring = _spherical_shell(
                r, color=color, stroke_width=1.1,
                opacity=0.48 * (1 - i / (n_rings + 1)),
                squash=0.7, planes=3,
            )
            ring.move_to(src)
            all_rings.add(ring)
    if len(sources) >= 2:
        for a, b in zip(sources[:-1], sources[1:]):
            spark = Dot(radius=0.08, color=WHITE)
            spark.set_opacity(0.28)
            spark.move_to((np.array(a) + np.array(b)) / 2)
            all_rings.add(spark)
    return all_rings
