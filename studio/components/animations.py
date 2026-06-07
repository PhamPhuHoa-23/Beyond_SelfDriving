"""Custom animations — forge text, particle assemble, fivefold, scan reveal, dust, write chiseled."""
from __future__ import annotations
from manimlib import *
from studio.components.colors import GOLD_RICH, INK_DARK
from studio.components.typography import FONT_PRIMARY, SIZE_HERO


def forge_text(s: str, *, size: int = SIZE_HERO, color: str = GOLD_RICH) -> Succession:
    """Ink-first Write that warms into the target color on a white canvas."""
    mob = Text(s, font=FONT_PRIMARY, font_size=size, color=color)
    white_version = mob.copy().set_color(INK_DARK)
    return Succession(
        Write(white_version, run_time=1.8, lag_ratio=0.025),
        white_version.animate(run_time=0.8).set_color(color),
    )


def particle_assemble(target: VMobject, *, n_particles: int = 200) -> LaggedStart:
    """Particles burst from origin then converge into target shape.
    # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/logo.py:192 LogoGenerationFlurry
    """
    particles = VGroup()
    center = target.get_center()
    for _ in range(n_particles):
        p = Dot(radius=0.04, color=random_bright_color())
        p.move_to(center)
        particles.add(p)
    # scatter phase
    scatter_anims = []
    for p in particles:
        angle = random.uniform(0, TAU)
        dist = random.uniform(0.5, 3.5)
        dest = center + dist * np.array([np.cos(angle), np.sin(angle), 0])
        scatter_anims.append(p.animate(run_time=0.6, rate_func=rush_from).move_to(dest))
    # converge phase — use bounding box to generate target positions
    bb = target.get_bounding_box()
    w, h = bb[2][0] - bb[0][0], bb[2][1] - bb[0][1]
    converge_anims = []
    for p in particles:
        tx = bb[0][0] + random.uniform(0, max(w, 0.1))
        ty = bb[0][1] + random.uniform(0, max(h, 0.1))
        converge_anims.append(
            p.animate(run_time=1.2, rate_func=smooth, path_arc=random.uniform(-PI / 2, PI / 2))
            .move_to(np.array([tx, ty, 0]))
        )
    return Succession(
        AnimationGroup(*scatter_anims),
        AnimationGroup(*converge_anims),
    )


def fivefold_assemble(target: VGroup) -> AnimationGroup:
    """Radial 5-fold spin-in assembly for 5-part roadmap.
    # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/logo.py:216 LogoGenerationFivefold
    """
    anims = []
    for i, item in enumerate(target):
        angle = i * TAU / 5
        item_copy = item.copy()
        item_copy.rotate(angle, about_point=ORIGIN)
        anims.append(Rotate(item_copy, -angle, about_point=ORIGIN, run_time=2.0))
    return AnimationGroup(*anims, lag_ratio=0.1)


def scan_reveal(target: VMobject, *, direction: str = "down") -> ShowCreation:
    """Holographic scan-line sweep revealing target."""
    return ShowCreation(target, run_time=1.5, rate_func=linear)


def dust_dissolve(*targets: Mobject) -> LaggedStart:
    """Particles drift up as objects fade — inverse of particle_assemble."""
    anims = []
    for mob in targets:
        fade = FadeOut(mob, shift=0.5 * UP, run_time=0.8)
        anims.append(fade)
    return LaggedStart(*anims, lag_ratio=0.1)


def write_chiseled(t: VMobject, *, run_time: float = 3.0) -> Write:
    """Slow Write — for the project's quote moments (I-02, P02-S05, finale)."""
    return Write(t, run_time=run_time, lag_ratio=0.01)


import random  # noqa: E402
