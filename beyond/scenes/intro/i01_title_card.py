# beyond/scenes/intro/i01_title_card.py
# ─────────────────────────────────────────────────────────────────
# I-01  KHAI MÀN  (~22s)
#
# Layout (y-axis, per 5_PART_GUIDE §I-01):
#   y=+2.4  "BEYOND SELF-DRIVING"   GOLD 52  forge effect
#   y=+1.4  "ICCV 2025 Tutorial · UCLA Mobility Lab"  WHITE 24
#   y=+0.7  divider line  GOLD
#   y=+0.2  "UCLA Mobility Lab"  (implicit in subtitle)
#   y=-0.4  5 presenter names
#   y=-3.0  roadmap strip (all 5 dots dim)
#
# Timeline:
#   0-2.0s   silence / black
#   2-3.0s   seed particle pulse → BURST 200 hạt
#   3-5.5s   title forges letter by letter (WriteLetterByLetter + cool to gold)
#   5.5-6.2s subtitle fades in
#   6.2-6.8s gold divider draws left→right
#   6.8-8.0s 5 names appear staggered
#   8.0-12s  hold 4s — khán giả đọc tên, ngắm tiêu đề
#   12-14s   dissolve: tan thành tàn lửa bay lên
#
# Render:  manim -ql "beyond/scenes/intro/i01_title_card.py" I01TitleCard
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import numpy as np
from manim import *
from beyond.components.colors import (
    BG_VOID, GOLD, GOLD_GLOW, CYAN_NEON, BLUE_ELECTRIC,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_HERO, SIZE_BODY, SIZE_LABEL, SIZE_MICRO,
    FONT_PRIMARY, UCLA_GOLD,
)

RNG = np.random.default_rng(seed=7)

# ── 5-dot roadmap strip ─────────────────────────────────────────

def _roadmap_strip_dim() -> VGroup:
    """All 5 dots dim — will light up in I-03."""
    spacing = 1.1
    line = Line(
        LEFT * spacing * 2, RIGHT * spacing * 2,
        stroke_color=TEXT_GHOST, stroke_width=1.2,
    ).move_to(DOWN * 3.0)
    dots = VGroup(*[
        Circle(radius=0.10,
               fill_color=TEXT_GHOST, fill_opacity=0.5,
               stroke_color=TEXT_GHOST, stroke_width=1.0)
        .move_to(DOWN * 3.0 + RIGHT * (i - 2) * spacing)
        for i in range(5)
    ])
    return VGroup(line, dots)


# ── particle helpers ────────────────────────────────────────────

def _burst_particles(n: int = 200) -> tuple[VGroup, list]:
    angles  = RNG.uniform(0, TAU, n)
    dists   = RNG.uniform(5.5, 10.5, n)
    radii   = RNG.uniform(0.012, 0.055, n)
    colors  = RNG.choice([CYAN_NEON, GOLD, GOLD_GLOW, BLUE_ELECTRIC, WHITE], n)

    pts = VGroup(*[
        Dot(radius=float(radii[i]),
            color=str(colors[i]),
            fill_opacity=float(RNG.uniform(0.55, 1.0)))
        .move_to(ORIGIN)
        for i in range(n)
    ])
    targets = [
        np.array([float(dists[i]) * np.cos(float(angles[i])),
                  float(dists[i]) * np.sin(float(angles[i])), 0.0])
        for i in range(n)
    ]
    return pts, targets


def _dissolve_up(mobs: list, run_time: float = 1.8) -> LaggedStart:
    """Tan ra như tàn lửa: each element drifts up/sideways and fades."""
    anims = []
    for mob in mobs:
        dy = float(RNG.uniform(0.5, 1.8))
        dx = float(RNG.uniform(-0.8, 0.8))
        rt = float(RNG.uniform(0.6, run_time))
        anims.append(
            mob.animate(run_time=rt, rate_func=smooth)
               .shift(np.array([dx, dy, 0.0]))
               .set_opacity(0)
        )
    return LaggedStart(*anims, lag_ratio=0.06)


# ── Scene ─────────────────────────────────────────────────────────

class I01TitleCard(Scene):
    def setup(self):
        self.camera.background_color = BG_VOID

    def construct(self):

        # ── [0-2s] Silence ────────────────────────────────────
        self.wait(2.0)

        # ── [2s] Seed → pulse → BURST ─────────────────────────
        seed = Dot(radius=0.035, color=CYAN_NEON, fill_opacity=1.0).move_to(ORIGIN)
        self.play(GrowFromCenter(seed, run_time=0.2))
        # Pulse twice: build tension
        self.play(seed.animate(run_time=0.15, rate_func=there_and_back).scale(3.0))
        self.play(seed.animate(run_time=0.10, rate_func=there_and_back).scale(4.5))

        # BURST
        particles, targets = _burst_particles(200)
        rt_each = RNG.uniform(0.45, 1.05, 200)
        self.add(particles)
        self.remove(seed)

        self.play(
            LaggedStart(*[
                particles[i].animate(
                    run_time=float(rt_each[i]), rate_func=rush_from
                ).move_to(targets[i]).set_fill(opacity=0.0)
                for i in range(200)
            ], lag_ratio=0.005),
            run_time=1.2,
        )

        # ── [~3.2s] TITLE — forge letter by letter ─────────────
        # Use AddTextLetterByLetter (proven reliable) starting white-hot,
        # then cool the entire title to GOLD with flash burst.
        title = Text(
            "BEYOND SELF-DRIVING",
            font_size=SIZE_HERO,
            color="#FFFDE7",          # white-hot initial color
            font=FONT_PRIMARY,
            weight=BOLD,
        )
        title.move_to(UP * 2.4)      # y=+2.4 per guide layout

        # Clamp width to safe zone
        if title.width > 12.0:
            title.scale(12.0 / title.width)

        self.play(
            AddTextLetterByLetter(title, run_time=2.0, rate_func=linear),
        )

        # Cool: white → GOLD  +  flash per character (staggered)
        self.play(
            title.animate(run_time=0.45, rate_func=smooth).set_color(GOLD),
            LaggedStart(*[
                Flash(ch.get_center(), color=GOLD_GLOW,
                      flash_radius=0.16, num_lines=4, run_time=0.18)
                for ch in title
            ], lag_ratio=0.04),
            run_time=0.55,
        )
        self.wait(0.2)

        # ── [~5.7s] Subtitle ──────────────────────────────────
        subtitle = Text(
            "ICCV 2025 Tutorial  ·  UCLA Mobility Lab",
            font_size=SIZE_LABEL + 2,
            color=TEXT_WHITE,
            font=FONT_PRIMARY,
        )
        subtitle.move_to(UP * 1.45)   # y=+1.45 per guide

        self.play(FadeIn(subtitle, shift=UP * 0.12, run_time=0.55))
        self.wait(0.15)

        # ── [~6.4s] Gold divider ──────────────────────────────
        divider = Line(
            LEFT * 5.5, LEFT * 5.5,   # starts as a point
            stroke_color=GOLD, stroke_width=1.0, stroke_opacity=0.65,
        )
        divider.move_to(UP * 0.80)    # y=+0.8 per layout

        self.play(
            divider.animate(run_time=0.55, rate_func=smooth)
                   .put_start_and_end_on(
                       LEFT * 5.5 + UP * 0.80,
                       RIGHT * 5.5 + UP * 0.80,
                   ),
        )

        # ── [~7.0s] 5 Presenter names ─────────────────────────
        names = [
            "Dr. Zhiyu Huang",
            "Zewei Zhou",
            "Zhaoliang Zheng",
            "Seth Z. Zhao",
            "Wayne Wu",
        ]
        name_mobs = VGroup(*[
            Text(n, font_size=SIZE_MICRO + 2,
                 color=TEXT_DIM, font=FONT_PRIMARY)
            for n in names
        ])
        name_mobs.arrange(RIGHT, buff=0.65)
        name_mobs.move_to(DOWN * 0.35)   # y=-0.35

        self.play(
            LaggedStart(*[
                FadeIn(nm, shift=UP * 0.09, run_time=0.32)
                for nm in name_mobs
            ], lag_ratio=0.14),
        )

        # ── UCLA placeholder logo (top-left) ──────────────────
        ucla_box = RoundedRectangle(
            corner_radius=0.05, width=0.72, height=0.50,
            fill_color=UCLA_GOLD, fill_opacity=1.0, stroke_width=0,
        ).to_corner(UL, buff=0.40)
        ucla_txt = Text("UCLA", font_size=14, color="#0A0A16",
                        font=FONT_PRIMARY, weight=BOLD).move_to(ucla_box)

        self.play(GrowFromCenter(ucla_box, run_time=0.35),
                  FadeIn(ucla_txt, run_time=0.25))

        # ── Roadmap strip (all 5 dim) ──────────────────────────
        roadmap = _roadmap_strip_dim()
        self.play(FadeIn(roadmap, run_time=0.40))

        # ── [~8.2s] HOLD — 4 seconds ──────────────────────────
        # Audience reads the title, names, absorbs the visual
        self.wait(4.0)

        # ── [~12.2s] DISSOLVE — tan thành tàn lửa ─────────────
        # Mỗi element drift UP với random offset và fade ra
        all_elems = [title, subtitle, divider, name_mobs,
                     ucla_box, ucla_txt, roadmap]
        self.play(_dissolve_up(all_elems, run_time=1.6))
        self.wait(0.4)
