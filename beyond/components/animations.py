# beyond/components/animations.py
# ─────────────────────────────────────────────────────────────────
# Micro-animation recipe library.
# Sources:
#   - MICRO_ANIMATION_BIBLE.md (Phần A–K)
#   - BEYOND_SELFDRIVING_ANIMATION_GUIDE.md § 13
#
# Import specific recipes as needed:
#   from beyond.components.animations import scene_open, key_insight_reveal
#
# All recipes return Animation / AnimationGroup / Succession objects
# unless they directly call scene.play() (marked with "→ calls play").
# ─────────────────────────────────────────────────────────────────

from __future__ import annotations
import numpy as np
from manim import *
from .colors import (
    BG_VOID, BG_SPACE, BG_PANEL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    GOLD, CYAN_NEON, GREEN_SIGNAL, RED_ALERT,
    BLUE_ELECTRIC, COMM_LINK, VOXEL_ACTIVE, VOXEL_MASKED,
    P1_FOUNDATION, P5_PHYSICAL,
    SIZE_TITLE, SIZE_BODY, SIZE_LABEL, SIZE_MICRO,
    FONT_PRIMARY,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# A. TEXT ANIMATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def scene_title_entrance(
    title_text: str,
    color: str = TEXT_WHITE,
    accent_color: str = CYAN_NEON,
) -> tuple[Text, Succession]:
    """
    Scene title with scan-line reveal (MICRO_ANIMATION_BIBLE A1).
    Returns (title_mob, animation). Add title_mob to scene first.
    """
    title = Text(title_text, font_size=SIZE_TITLE,
                 color=color, font=FONT_PRIMARY, weight=BOLD)
    title.to_edge(UP, buff=0.28)

    scan = Line(
        title.get_left() + LEFT * 0.1,
        title.get_left() + LEFT * 0.1,
        stroke_color=accent_color, stroke_width=2.5,
    )

    anim = Succession(
        Create(scan, run_time=0.05),
        AnimationGroup(
            scan.animate(run_time=0.6, rate_func=smooth).put_start_and_end_on(
                title.get_left(),
                title.get_right() + RIGHT * 0.15,
            ),
            AddTextLetterByLetter(title, run_time=0.55, rate_func=linear),
        ),
        Flash(title.get_right(), color=accent_color,
              flash_radius=0.18, num_lines=5, run_time=0.18),
        FadeOut(scan, run_time=0.12),
    )
    return title, anim


def separator_line(
    reference_mob: Mobject,
    accent_color: str = CYAN_NEON,
) -> tuple[Line, Create]:
    """Horizontal separator drawn below the title. Returns (line, Create anim)."""
    sep = Line(
        LEFT * 6.5, RIGHT * 6.5,
        stroke_color=accent_color,
        stroke_width=0.8, stroke_opacity=0.35,
    ).next_to(reference_mob, DOWN, buff=0.15)
    return sep, Create(sep, run_time=0.35, rate_func=smooth)


def bullet_reveal(
    items: list[str],
    accent_color: str = CYAN_NEON,
    font_size: int = None,
    stagger: float = 0.18,
) -> tuple[VGroup, LaggedStart]:
    """
    Bullet list reveal (MICRO_ANIMATION_BIBLE A6):
    dot flash → letter-by-letter text per item.
    Returns (mobs_group, animation).
    """
    if font_size is None:
        font_size = SIZE_BODY
    rows = VGroup()
    anims = []

    for text in items:
        dot = Dot(radius=0.07, color=accent_color)
        line = Text(text, font_size=font_size,
                    color=TEXT_WHITE, font=FONT_PRIMARY)
        row = VGroup(dot, line).arrange(RIGHT, buff=0.28)
        rows.add(row)
        anims.append(
            Succession(
                GrowFromCenter(dot, run_time=0.10),
                Flash(dot, color=accent_color, flash_radius=0.12,
                      num_lines=4, run_time=0.10),
                AddTextLetterByLetter(line, run_time=0.28),
            )
        )

    rows.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
    return rows, LaggedStart(*anims, lag_ratio=stagger)


def key_term_reveal(
    term: str,
    color: str = GOLD,
    font_size: int = None,
) -> tuple[VGroup, Succession]:
    """
    First-mention reveal for technical terms (MICRO_ANIMATION_BIBLE A4).
    Returns (group, animation). Position the group before playing.
    """
    if font_size is None:
        font_size = SIZE_BODY + 2

    term_mob = Text(term, font_size=font_size,
                    color=color, weight=BOLD, font=FONT_PRIMARY)

    underline = Line(
        term_mob.get_left() + DOWN * 0.18,
        term_mob.get_left() + DOWN * 0.18,
        stroke_color=color, stroke_width=1.5,
    )

    glow_ring = Circle(
        radius=max(term_mob.width, term_mob.height) * 0.55,
        stroke_color=color, stroke_opacity=0.25, stroke_width=8,
        fill_opacity=0,
    ).move_to(term_mob)

    grp = VGroup(term_mob, underline, glow_ring)

    anim = Succession(
        FadeIn(term_mob, scale=0.9, run_time=0.20),
        AnimationGroup(
            underline.animate(run_time=0.30).put_start_and_end_on(
                term_mob.get_left() + DOWN * 0.18,
                term_mob.get_right() + DOWN * 0.18,
            ),
            FadeIn(glow_ring, run_time=0.10),
            glow_ring.animate(run_time=0.40).scale(1.5).set_stroke(opacity=0),
        ),
    )
    return grp, anim


def quote_reveal(
    quote_text: str,
    author: str = "",
    color: str = GOLD,
) -> tuple[VGroup, Succession]:
    """
    Framed quote (MICRO_ANIMATION_BIBLE A7).
    Returns (group, animation). Place group before playing.
    """
    quote = Text(
        f'"{quote_text}"',
        font_size=SIZE_BODY + 4, slant=ITALIC,
        color=color, font=FONT_PRIMARY, line_spacing=1.45,
    ).move_to(ORIGIN)

    half_h = quote.height / 2 + 0.22
    top_line = Line(quote.get_left() + UP * half_h,
                    quote.get_left() + UP * half_h,
                    stroke_color=color, stroke_width=1.2, stroke_opacity=0.5)
    bot_line = top_line.copy().shift(DOWN * half_h * 2)

    grp = VGroup(quote, top_line, bot_line)

    author_mob = ORIGIN  # placeholder
    extra_anim = Wait(0)
    if author:
        author_mob = Text(f"— {author}", font_size=SIZE_LABEL,
                          color=TEXT_DIM, slant=ITALIC, font=FONT_PRIMARY)
        author_mob.next_to(quote, DOWN, buff=0.3).to_edge(RIGHT, buff=1.2)
        grp.add(author_mob)
        extra_anim = FadeIn(author_mob, shift=LEFT * 0.1, run_time=0.35)

    anim = Succession(
        AnimationGroup(
            top_line.animate(run_time=0.45).put_start_and_end_on(
                quote.get_left() + UP * half_h,
                quote.get_right() + UP * half_h,
            ),
            bot_line.animate(run_time=0.45).put_start_and_end_on(
                quote.get_left() + DOWN * half_h,
                quote.get_right() + DOWN * half_h,
            ),
        ),
        AddTextLetterByLetter(quote, run_time=max(0.8, len(quote_text) * 0.045)),
        extra_anim,
        AnimationGroup(
            top_line.animate(run_time=0.28).set_stroke(opacity=1.0),
            bot_line.animate(run_time=0.28).set_stroke(opacity=1.0),
        ),
        AnimationGroup(
            top_line.animate(run_time=0.28).set_stroke(opacity=0.4),
            bot_line.animate(run_time=0.28).set_stroke(opacity=0.4),
        ),
    )
    return grp, anim


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# B. BLOCK ANIMATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def pipeline_block_entrance(
    block: VGroup,
    accent_color: str = CYAN_NEON,
) -> Succession:
    """
    Corner-flash → border → fill → label (MICRO_ANIMATION_BIBLE B1).
    block must be VGroup([rect, label]).
    """
    rect, label = block[0], block[1]

    corners = [rect.get_corner(d) for d in [UL, UR, DR, DL]]
    corner_dots = VGroup(*[
        Dot(radius=0.05, color=accent_color).move_to(c)
        for c in corners
    ])

    return Succession(
        LaggedStart(*[GrowFromCenter(d, run_time=0.07) for d in corner_dots],
                    lag_ratio=0.08),
        AnimationGroup(
            Create(rect, run_time=0.35, rate_func=smooth),
            FadeOut(corner_dots, run_time=0.18),
        ),
        rect.animate(run_time=0.20).set_fill(rect.fill_color, opacity=1.0),
        AddTextLetterByLetter(label, run_time=0.25),
    )


def pipeline_arrow_entrance(
    arrow: Arrow,
    style: str = "electric",
) -> Succession:
    """
    Animated arrow entrance (MICRO_ANIMATION_BIBLE C1).
    style: "electric" | "data" | "beam"
    """
    if style == "electric":
        return Succession(
            Create(arrow, run_time=0.16, rate_func=rush_into),
            Flash(arrow.get_end(), color=arrow.get_color(),
                  flash_radius=0.14, num_lines=5, run_time=0.12),
        )

    elif style == "data":
        path_ghost = arrow.copy().set_stroke(
            arrow.get_color(), width=0.8, opacity=0.25
        )
        dots = VGroup(*[
            Dot(radius=0.04, color=arrow.get_color(), fill_opacity=0.9)
            .move_to(arrow.get_start())
            for _ in range(5)
        ])
        path = Line(arrow.get_start(), arrow.get_end())
        return Succession(
            Create(path_ghost, run_time=0.12),
            LaggedStart(*[
                MoveAlongPath(d, path, run_time=0.38)
                for d in dots
            ], lag_ratio=0.14),
            AnimationGroup(
                Create(arrow, run_time=0.18),
                FadeOut(path_ghost, run_time=0.12),
                FadeOut(dots, run_time=0.08),
            ),
        )

    else:  # "beam"
        glow = arrow.copy().set_stroke(
            width=arrow.get_stroke_width() * 3.5, opacity=0.15
        )
        return Succession(
            Create(arrow, run_time=0.10, rate_func=linear),
            AnimationGroup(
                FadeIn(glow, run_time=0.05),
                glow.animate(run_time=0.22).set_stroke(opacity=0),
            ),
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# C. CHART ANIMATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def axes_deploy(
    axes: Axes,
    label_x: str = "",
    label_y: str = "",
    color: str = CYAN_NEON,
) -> Succession:
    """
    Axes deploy like radar startup (MICRO_ANIMATION_BIBLE D1).
    Origin flash → X shoots right → Y shoots up → labels appear.
    """
    parts = []
    if label_x:
        xl = Text(label_x, font_size=SIZE_LABEL, color=TEXT_DIM, font=FONT_PRIMARY)
        xl.next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
        parts.append(xl)
    if label_y:
        yl = Text(label_y, font_size=SIZE_LABEL, color=TEXT_DIM, font=FONT_PRIMARY)
        yl.next_to(axes.y_axis.get_end(), UP, buff=0.15)
        parts.append(yl)

    label_anim = (
        AnimationGroup(*[FadeIn(p, shift=UP * 0.08, run_time=0.22) for p in parts])
        if parts else Wait(0)
    )

    return Succession(
        Flash(axes.get_origin(), color=color,
              flash_radius=0.20, num_lines=8, run_time=0.20),
        AnimationGroup(
            Create(axes.x_axis, run_time=0.32, rate_func=rush_into),
            Succession(
                Wait(0.10),
                Create(axes.y_axis, run_time=0.32, rate_func=rush_into),
            ),
        ),
        label_anim,
    )


def curve_trace(
    axes: Axes,
    func,
    color: str = CYAN_NEON,
    x_range: list = None,
    glow: bool = True,
    run_time: float = 1.5,
) -> Succession:
    """
    Curve with glowing head tracing along path (MICRO_ANIMATION_BIBLE D3).
    Returns animation. The main curve mob is drawn into the scene automatically.
    """
    if x_range is None:
        x_range = [axes.x_range[0], axes.x_range[1]]

    main_curve = axes.plot(func, x_range=x_range,
                           color=color, stroke_width=2.5)

    glow_curve = None
    if glow:
        glow_curve = axes.plot(func, x_range=x_range,
                               color=color, stroke_width=8, stroke_opacity=0.18)

    x_tracker = ValueTracker(x_range[0])
    head = Dot(radius=0.07, color=WHITE, fill_opacity=1.0)
    head_trail = TracedPath(head.get_center,
                            stroke_color=color, stroke_width=2.8,
                            dissipating_time=0.28)

    try:
        head.move_to(axes.input_to_graph_point(x_range[0], main_curve))
    except Exception:
        head.move_to(axes.get_origin())

    def head_updater(h):
        try:
            h.move_to(axes.input_to_graph_point(x_tracker.get_value(), main_curve))
        except Exception:
            pass

    head.add_updater(head_updater)

    post = []
    if glow and glow_curve is not None:
        post.append(FadeIn(glow_curve, run_time=0.18))

    return Succession(
        AnimationGroup(FadeIn(head, run_time=0.08), FadeIn(head_trail, run_time=0.08)),
        AnimationGroup(
            x_tracker.animate(run_time=run_time, rate_func=smooth).set_value(x_range[1]),
            Create(main_curve, run_time=run_time, rate_func=smooth),
        ),
        AnimationGroup(
            FadeOut(head, run_time=0.18),
            FadeOut(head_trail, run_time=0.18),
            *(post),
        ),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# D. SPECIAL EFFECTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def glow_pulse(
    mob: Mobject,
    color: str = CYAN_NEON,
    n_pulses: int = 2,
    scale: float = 1.35,
    run_time: float = 0.38,
) -> LaggedStart:
    """Expanding glow rings from a node (BEYOND_SELFDRIVING guide § 13)."""
    anims = []
    for _ in range(n_pulses):
        ring = mob.copy().set_fill(opacity=0).set_stroke(color, width=2.8)
        anims.append(
            Succession(
                GrowFromCenter(ring, run_time=run_time),
                ring.animate(run_time=run_time * 0.5).set_stroke(opacity=0),
            )
        )
    return LaggedStart(*anims, lag_ratio=0.5)


def signal_ping(
    position: np.ndarray,
    color: str = CYAN_NEON,
) -> LaggedStart:
    """3-ring signal ping (MICRO_ANIMATION_BIBLE H2)."""
    rings = [
        Circle(radius=0.01,
               stroke_color=color,
               stroke_width=max(0.5, 2.2 - i * 0.6),
               stroke_opacity=0.85 - i * 0.2,
               fill_opacity=0).move_to(position)
        for i in range(3)
    ]
    return LaggedStart(*[
        rings[i].animate(run_time=0.52, rate_func=rush_from)
                .scale(180 + i * 60).set_stroke(opacity=0)
        for i in range(3)
    ], lag_ratio=0.15)


def v2x_link_pulse(
    node_a: Mobject,
    node_b: Mobject,
    link_color: str = COMM_LINK,
    bidirectional: bool = True,
) -> Succession:
    """Dashed V2X communication link with packet flow (MICRO_ANIMATION_BIBLE C2)."""
    link = DashedLine(
        node_a.get_center(), node_b.get_center(),
        color=link_color, stroke_width=1.2, stroke_opacity=0.40,
        dash_length=0.14,
    )

    def _packet():
        return RegularPolygon(n=6, radius=0.06,
                              color=link_color, fill_opacity=0.9,
                              stroke_width=0)

    pkt_ab = _packet().move_to(node_a.get_center())
    pkt_ba = _packet().move_to(node_b.get_center())
    path_ab = Line(node_a.get_center(), node_b.get_center())
    path_ba = Line(node_b.get_center(), node_a.get_center())

    flow = AnimationGroup(
        Succession(
            MoveAlongPath(pkt_ab, path_ab, run_time=0.55, rate_func=linear),
            Flash(node_b.get_center(), color=link_color, flash_radius=0.14, run_time=0.08),
            FadeOut(pkt_ab, run_time=0.04),
        ),
        Succession(
            Wait(0.28),
            MoveAlongPath(pkt_ba, path_ba, run_time=0.55, rate_func=linear),
            Flash(node_a.get_center(), color=link_color, flash_radius=0.14, run_time=0.08),
            FadeOut(pkt_ba, run_time=0.04),
        ) if bidirectional else Wait(0),
    )
    return Succession(Create(link, run_time=0.30), flow)


def neural_spark(
    source: Mobject,
    target: Mobject,
    color: str = P1_FOUNDATION,
) -> Succession:
    """Tiny arc spark between two model nodes (MICRO_ANIMATION_BIBLE H1)."""
    spark = Dot(radius=0.03, color=WHITE)
    spark.move_to(source.get_center())
    path = ArcBetweenPoints(
        source.get_center(), target.get_center(),
        angle=np.random.choice([-0.5, 0.5]) * np.random.uniform(0.3, 0.6),
    )
    return Succession(
        MoveAlongPath(spark, path, run_time=0.28, rate_func=smooth),
        Flash(target.get_center(), color=color,
              flash_radius=0.12, num_lines=4, run_time=0.14),
        FadeOut(spark, run_time=0.04),
    )


def compression_squeeze(
    mob: Mobject,
    target_scale: float = 0.30,
    target_color: str = None,
) -> Succession:
    """Data compression visual (MICRO_ANIMATION_BIBLE H4)."""
    from .colors import INT8_LIGHT
    if target_color is None:
        target_color = INT8_LIGHT
    return Succession(
        mob.animate(run_time=0.28, rate_func=smooth)
           .scale(target_scale).set_color(target_color),
        Flash(mob.get_center(), color=target_color,
              flash_radius=0.18, num_lines=6, run_time=0.18),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# E. SCENE CHOREOGRAPHY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def scene_open(
    scene: Scene,
    title: str,
    part_color: str = CYAN_NEON,
) -> tuple[Text, Line]:
    """
    Standard 3-beat scene opening → calls scene.play() (MICRO_ANIMATION_BIBLE G1).
    Beat 1: faint BG flash  Beat 2: title scan  Beat 3: separator line
    Returns (title_mob, sep_mob) — keep references for FadeOut at end.
    """
    bg_flash = FullScreenRectangle(fill_color=part_color,
                                   fill_opacity=0.04, stroke_width=0)
    scene.play(FadeIn(bg_flash, run_time=0.14),
               FadeOut(bg_flash, run_time=0.24))

    title_mob, title_anim = scene_title_entrance(title, accent_color=part_color)
    scene.add(title_mob)
    scene.play(title_anim)

    sep, sep_anim = separator_line(title_mob, part_color)
    scene.play(sep_anim)

    return title_mob, sep


def scene_close(
    scene: Scene,
    part_color: str = CYAN_NEON,
    keep: list = None,
) -> None:
    """
    Standard scene close → calls scene.play() (MICRO_ANIMATION_BIBLE G2).
    Fades out all mobjects except those in `keep` list.
    """
    keep_set = set(keep or [])
    targets = [
        m for m in scene.mobjects
        if m not in keep_set
        and not isinstance(m, (BackgroundRectangle, FullScreenRectangle))
    ]
    if targets:
        scene.play(
            LaggedStart(*[FadeOut(m, shift=UP * 0.04) for m in targets],
                        lag_ratio=0.04, run_time=0.5)
        )
    flash = FullScreenRectangle(fill_color=part_color,
                                fill_opacity=0.05, stroke_width=0)
    scene.play(FadeIn(flash, run_time=0.08), FadeOut(flash, run_time=0.18))
    scene.wait(0.10)


def key_insight_reveal(
    scene: Scene,
    text: str,
    color: str = GOLD,
    hold: float = 2.0,
) -> None:
    """
    Full-screen key insight moment → calls scene.play() (MICRO_ANIMATION_BIBLE G3).
    Dims scene, shows gold text center-stage, holds, then restores.
    """
    dim = FullScreenRectangle(fill_color=BG_VOID,
                              fill_opacity=0.55, stroke_width=0)
    insight = Text(text, font_size=SIZE_BODY + 6,
                   color=color, font=FONT_PRIMARY,
                   line_spacing=1.4).move_to(ORIGIN)
    glow = Circle(
        radius=max(insight.width, insight.height) * 0.65,
        stroke_color=color, stroke_opacity=0, fill_opacity=0,
    ).move_to(ORIGIN)

    scene.play(FadeIn(dim, run_time=0.28), Write(insight, run_time=0.80))
    scene.play(
        glow.animate(run_time=0.55).scale(2.5).set_stroke(opacity=0.30),
        glow.copy().animate(run_time=0.75).scale(3.5).set_stroke(opacity=0),
    )
    scene.wait(hold)
    scene.play(
        FadeOut(dim, run_time=0.38),
        FadeOut(insight, run_time=0.38),
        FadeOut(glow, run_time=0.18),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# F. AMBIENT BACKGROUNDS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def setup_ambient_particles(
    scene: Scene,
    color: str = CYAN_NEON,
    n: int = 22,
    opacity_range: tuple = (0.04, 0.10),
) -> VGroup:
    """
    Subtle drifting particle background (MICRO_ANIMATION_BIBLE F1).
    Returns the VGroup so you can FadeOut it at scene end.
    """
    particles = VGroup(*[
        Dot(
            radius=np.random.uniform(0.015, 0.038),
            color=color,
            fill_opacity=np.random.uniform(*opacity_range),
        ).move_to([
            np.random.uniform(-7, 7),
            np.random.uniform(-4, 4),
            0,
        ])
        for _ in range(n)
    ])

    speeds = [
        np.array([np.random.uniform(-0.007, 0.007),
                  np.random.uniform(-0.003, 0.003), 0])
        for _ in range(n)
    ]

    def drift(group, dt):
        for i, p in enumerate(group):
            p.shift(speeds[i])
            c = p.get_center()
            if c[0] > 7.5:
                p.shift(LEFT * 15)
            elif c[0] < -7.5:
                p.shift(RIGHT * 15)
            if c[1] > 4.5:
                p.shift(DOWN * 9)
            elif c[1] < -4.5:
                p.shift(UP * 9)

    particles.add_updater(drift)
    scene.add(particles)
    return particles


def setup_p1_ambient(scene: Scene) -> None:
    """Faint neural-net graph in background for Part 1 scenes."""
    nodes = VGroup(*[
        Dot(radius=0.04, color=P1_FOUNDATION, fill_opacity=0.06)
        .move_to([np.random.uniform(-6, 6), np.random.uniform(-3, 3), 0])
        for _ in range(14)
    ])
    edges = VGroup()
    pos = [n.get_center() for n in nodes]
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            if np.random.random() < 0.28:
                edges.add(Line(pos[i], pos[j],
                               stroke_color=P1_FOUNDATION,
                               stroke_width=0.4, stroke_opacity=0.04))
    scene.add_to_back(VGroup(edges, nodes))


def setup_p2_ambient(scene: Scene) -> VGroup:
    """Slowly expanding radar rings for Part 2 scenes."""
    rings = VGroup(*[
        Circle(
            radius=np.random.uniform(0.5, 2.2),
            stroke_color=CYAN_NEON,
            stroke_width=0.5,
            stroke_opacity=np.random.uniform(0.02, 0.06),
        ).move_to([np.random.uniform(-5, 5), np.random.uniform(-3, 3), 0])
        for _ in range(6)
    ])

    def expand(group, dt):
        for ring in group:
            ring.scale(1 + dt * 0.04)
            new_r = np.linalg.norm(ring.get_width()) / 2
            if new_r > 5.5:
                ring.scale(0.12)
                ring.set_stroke(opacity=0.06)
            else:
                ring.set_stroke(opacity=max(0, ring.get_stroke_opacity() - dt * 0.004))

    rings.add_updater(expand)
    scene.add_to_back(rings)
    return rings


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# G. TIMELINE / EVOLUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def evolution_timeline(
    milestones: list[dict],
    spine_y: float = -0.5,
) -> tuple[VGroup, Succession]:
    """
    Method evolution timeline (MICRO_ANIMATION_BIBLE J1).

    Each milestone dict:
      {"year": 2020, "name": "V2VNet", "contribution": "GNN fusion",
       "bottleneck": "quality", "color": "#4D9FFF"}

    All labels go ABOVE the spine — no zigzag.
    Returns (full_group, animation).
    """
    n = len(milestones)
    max_w = 12.0
    spacing = min(max_w / max(n - 1, 1), 3.0)
    spine_w = spacing * (n - 1)

    spine = Line(
        LEFT * spine_w / 2 + UP * spine_y,
        RIGHT * spine_w / 2 + UP * spine_y,
        stroke_color=TEXT_GHOST, stroke_width=1.2,
    )

    all_mobs = VGroup(spine)
    anims = [Create(spine, run_time=0.55, rate_func=smooth)]

    for i, ms in enumerate(milestones):
        x = -spine_w / 2 + i * spacing

        node = Circle(
            radius=0.17,
            fill_color=ms["color"], fill_opacity=1.0,
            stroke_color=TEXT_WHITE, stroke_width=1.4,
        ).move_to([x, spine_y, 0])

        name_mob = Text(ms["name"], font_size=SIZE_LABEL,
                        color=ms["color"], weight=BOLD, font=FONT_PRIMARY)
        name_mob.move_to([x, spine_y + 0.55, 0])

        year_mob = Text(str(ms["year"]), font_size=SIZE_MICRO,
                        color=TEXT_DIM, font=FONT_PRIMARY)
        year_mob.move_to([x, spine_y - 0.45, 0])

        contrib_mob = Text(ms.get("contribution", ""), font_size=SIZE_MICRO,
                           color=TEXT_DIM, slant=ITALIC, font=FONT_PRIMARY)
        contrib_mob.move_to([x, spine_y + 0.90, 0])

        all_mobs.add(node, name_mob, year_mob, contrib_mob)

        anims.append(Succession(
            GrowFromCenter(node, run_time=0.20),
            Flash(node.get_center(), color=ms["color"],
                  flash_radius=0.28, num_lines=6, run_time=0.18),
            AnimationGroup(
                FadeIn(name_mob, shift=UP * 0.08, run_time=0.22),
                FadeIn(contrib_mob, shift=UP * 0.05, run_time=0.18),
                FadeIn(year_mob, shift=DOWN * 0.05, run_time=0.18),
            ),
        ))

        # Bottleneck annotation between nodes
        if i < n - 1 and ms.get("bottleneck"):
            mid_x = x + spacing / 2
            bn = Text(
                f"→ fixes:\n'{ms['bottleneck']}'",
                font_size=SIZE_MICRO, color=TEXT_DIM,
                slant=ITALIC, font=FONT_PRIMARY, line_spacing=0.75,
            ).move_to([mid_x, spine_y - 0.88, 0])
            all_mobs.add(bn)
            anims.append(FadeIn(bn, shift=UP * 0.04, run_time=0.25))

    return all_mobs, Succession(*anims)
