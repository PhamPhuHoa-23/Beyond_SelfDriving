# beyond/scenes/part01/p01_s01_title.py
# ─────────────────────────────────────────────────────────────────
# P1-01  TITLE CARD — FOUNDATION MODELS  (~28s)
#
# Opening: subtle P1_FOUNDATION neural net pulses in background.
# Supertitle → forge title (white-hot → GOLD) → presenter →
# separator → quote (word-by-word, không phải drift) →
# roadmap strip nút 1 sáng GOLD + flash → hold 2.5s → fade.
#
# Render:  manim -ql "beyond/scenes/part01/p01_s01_title.py" P01S01Title
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import numpy as np
from manim import *
from beyond.components.colors import (
    BG_VOID,
    GOLD, GOLD_GLOW, P1_FOUNDATION,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_HERO, SIZE_LABEL, SIZE_MICRO,
    FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=11)


# ── Ambient background: faint neural net for P1 ───────────────────

def _p1_ambient_bg(n_nodes: int = 16) -> VGroup:
    """Faint indigo neural net drifting — P1 Foundation Models theme."""
    positions = [
        np.array([float(RNG.uniform(-6.5, 6.5)),
                  float(RNG.uniform(-3.8, 3.8)), 0])
        for _ in range(n_nodes)
    ]
    nodes = VGroup(*[
        Dot(radius=float(RNG.uniform(0.030, 0.055)),
            color=P1_FOUNDATION,
            fill_opacity=float(RNG.uniform(0.06, 0.14)))
        .move_to(positions[i])
        for i in range(n_nodes)
    ])
    edges = VGroup()
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            d = np.linalg.norm(positions[i] - positions[j])
            if d < 3.5 and RNG.random() < 0.28:
                edges.add(Line(
                    positions[i], positions[j],
                    stroke_color=P1_FOUNDATION,
                    stroke_width=0.35, stroke_opacity=0.05,
                ))
    return VGroup(edges, nodes)


# ── Roadmap strip ─────────────────────────────────────────────────

def _roadmap_strip(current: int = 1) -> tuple:
    """Returns (strip_group, active_dot)."""
    PART_COLORS = ["#7986CB", "#00BCD4", "#4CAF50", "#FFC107", "#F06292"]
    sp = 1.1
    line = Line(
        LEFT * sp * 2, RIGHT * sp * 2,
        stroke_color=TEXT_GHOST, stroke_width=1.2,
    )
    dots = VGroup()
    active_dot = None
    for i in range(5):
        x = (i - 2) * sp
        is_active = (i + 1 == current)
        d = Circle(
            radius=0.12,
            fill_color=PART_COLORS[i] if is_active else TEXT_GHOST,
            fill_opacity=1.0 if is_active else 0.35,
            stroke_color=PART_COLORS[i] if is_active else TEXT_DIM,
            stroke_width=1.4,
        ).move_to([x, 0, 0])
        dots.add(d)
        if is_active:
            active_dot = d
    strip = VGroup(line, dots)
    strip.move_to(DOWN * 3.05)
    return strip, active_dot


# ── Scene ─────────────────────────────────────────────────────────

class P01S01Title(Scene):
    def setup(self):
        self.camera.background_color = BG_VOID

    def construct(self):

        # ── Ambient background ─────────────────────────────────
        ambient = _p1_ambient_bg()
        self.add_to_back(ambient)

        # Slow gentle pulse on ambient nodes
        t_ref = [0.0]
        def pulse_ambient(mob, dt):
            t_ref[0] += dt
            for node in mob[1]:  # nodes are mob[1]
                node.set_fill(opacity=0.06 + 0.08 * abs(np.sin(t_ref[0] * 0.8 + float(RNG.random()) * 6)))
        ambient.add_updater(pulse_ambient)

        # ── Supertitle ────────────────────────────────────────
        super_title = Text(
            "Part  01",
            font_size=SIZE_MICRO + 2,
            color=TEXT_DIM,
            font=FONT_PRIMARY,
        )
        super_title.to_corner(UR, buff=0.55)
        self.play(FadeIn(super_title, shift=DOWN * 0.08, run_time=0.38))
        self.wait(0.15)

        # ── Forge title (white-hot → P1 GOLD) ────────────────
        line1 = Text(
            "Foundation Models",
            font_size=SIZE_HERO,
            color="#FFFDE7",
            font=FONT_PRIMARY,
            weight=BOLD,
        )
        line2 = Text(
            "for Autonomous Driving",
            font_size=SIZE_HERO - 4,
            color="#FFFDE7",
            font=FONT_PRIMARY,
            weight=BOLD,
        )
        title_grp = VGroup(line1, line2).arrange(DOWN, buff=0.20)
        for ln in (line1, line2):
            if ln.width > 12.2:
                ln.scale(12.2 / ln.width)
        title_grp.arrange(DOWN, buff=0.20).move_to(UP * 1.25)

        self.play(AddTextLetterByLetter(line1, run_time=1.3, rate_func=linear))
        self.play(AddTextLetterByLetter(line2, run_time=1.1, rate_func=linear))
        self.wait(0.05)

        # Cool: white-hot → GOLD + staggered character flashes
        self.play(
            AnimationGroup(
                line1.animate(run_time=0.40).set_color(GOLD),
                line2.animate(run_time=0.40).set_color(GOLD),
                LaggedStart(*[
                    Flash(
                        ch.get_center(),
                        color=GOLD_GLOW,
                        flash_radius=0.13,
                        num_lines=4,
                        run_time=0.15,
                    )
                    for ch in list(line1) + list(line2)
                ], lag_ratio=0.022),
            ),
            run_time=0.55,
        )
        # Brief accent glow on the entire title
        title_glow = SurroundingRectangle(
            title_grp,
            color=P1_FOUNDATION,
            stroke_width=0,
            fill_color=P1_FOUNDATION,
            fill_opacity=0.04,
            corner_radius=0.18,
            buff=0.15,
        )
        self.play(FadeIn(title_glow, run_time=0.20),
                  title_glow.animate(run_time=0.40).set_fill(opacity=0))
        self.remove(title_glow)
        self.wait(0.20)

        # ── Presenter ─────────────────────────────────────────
        presenter = Text(
            "Dr. Zhiyu Huang  ·  UCLA Mobility Lab",
            font_size=SIZE_LABEL,
            color=P1_FOUNDATION,
            font=FONT_PRIMARY,
        )
        presenter.next_to(title_grp, DOWN, buff=0.55)
        self.play(FadeIn(presenter, shift=UP * 0.12, run_time=0.40))
        self.wait(0.15)

        # ── Separator line ────────────────────────────────────
        sep = Line(
            presenter.get_left() + LEFT * 0.5,
            presenter.get_left() + LEFT * 0.5,  # starts zero-length
            stroke_color=P1_FOUNDATION,
            stroke_width=0.9, stroke_opacity=0.50,
        )
        self.play(
            sep.animate(run_time=0.45, rate_func=smooth)
               .put_start_and_end_on(
                   presenter.get_left() + LEFT * 0.4 + DOWN * 0.25,
                   presenter.get_right() + RIGHT * 0.4 + DOWN * 0.25,
               ),
        )
        self.wait(0.10)

        # ── Quote — word by word, let each phrase breathe ─────
        quote_txt = (
            '"Why, in 2025, can AI write code, draw art, answer anything —\n'
            '  yet self-driving cars still can\'t go everywhere?"'
        )
        quote = Text(
            quote_txt,
            font_size=SIZE_MICRO + 4,
            color=TEXT_WHITE,
            font=FONT_PRIMARY,
            slant=ITALIC,
            line_spacing=0.50,
        )
        quote.next_to(sep, DOWN, buff=0.30)

        # Reveal: set opacity 0 first, then AddTextLetterByLetter
        quote.set_opacity(0)
        self.add(quote)
        self.play(
            quote.animate(run_time=0.40, rate_func=smooth).set_opacity(1.0),
        )
        # Word-by-word reflow is tricky with multi-line; use FadeIn with subtle shift
        # The quote is already placed correctly — just a clean reveal
        self.wait(0.30)

        # ── Roadmap strip ─────────────────────────────────────
        roadmap, active_dot = _roadmap_strip(current=1)
        self.play(FadeIn(roadmap, run_time=0.45))
        self.wait(0.10)

        # Active dot flash + expanding ring
        glow_ring = Circle(
            radius=0.12,
            stroke_color=GOLD, stroke_opacity=0,
            fill_opacity=0,
        ).move_to(active_dot.get_center())

        self.play(
            AnimationGroup(
                Flash(
                    active_dot.get_center(),
                    color=GOLD, flash_radius=0.35,
                    num_lines=10, run_time=0.40,
                ),
                glow_ring.animate(run_time=0.55)
                         .scale(3.5)
                         .set_stroke(opacity=0),
            )
        )
        self.remove(glow_ring)

        # ── HOLD ──────────────────────────────────────────────
        self.wait(2.5)

        # ── Clean fade out ────────────────────────────────────
        ambient.remove_updater(pulse_ambient)
        all_mobs = VGroup(
            super_title, title_grp, presenter, sep, quote, roadmap, ambient
        )
        self.play(FadeOut(all_mobs, run_time=0.65))
        self.wait(0.20)
