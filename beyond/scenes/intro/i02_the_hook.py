# beyond/scenes/intro/i02_the_hook.py
# ─────────────────────────────────────────────────────────────────
# I-02  THE HOOK  (~75s)
#
# ACT A — Chiếc Xe Thông Minh: xe lái vào, FM hexagon icons lơ lửng,
#          radar gravitational waves tỏa ra (non-uniform spacing).
# ACT B — Bức Tường: building rơi từ trên, waves bị bóp méo,
#          blind zone đỏ, text "Even the smartest single agent…"
# ACT C — Hợp Tác: 2 xe thêm, 3 hệ sóng, interference, pedestrian,
#          "So we taught them to cooperate." Write chậm, hold 3s.
#
# Kỹ thuật:
#   - BEV top-down view, simulated depth bằng squash vertical
#   - Radar rings: ValueTracker-driven updater → smooth continuous waves
#   - Building squish + dust cloud
#   - Blind zone polygon → ReplacementTransform to green
#   - Pedestrian materializes from inside blind zone
#
# Render:  manim -ql "beyond/scenes/intro/i02_the_hook.py" I02Hook
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import numpy as np
from manim import *
from beyond.components.colors import (
    BG_VOID, BG_SPACE, GRID_LINE, BG_PANEL,
    GOLD, GOLD_GLOW, CYAN_NEON, BLUE_ELECTRIC,
    P1_FOUNDATION, P5_PHYSICAL,
    RED_ALERT, RED_DIM, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_BODY, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=23)

# ── Layout constants (compact, well-centred composition) ───────────
# Canvas: 14.22u wide × 8.0u tall. Keep cars inside ±5.5u × ±3.2u.
CAR_A = np.array([-3.2, -0.6, 0.0])   # hero car — center-left
CAR_B = np.array([ 2.2,  2.0, 0.0])   # second car — top-right
CAR_C = np.array([-0.6, -2.4, 0.0])   # third car — bottom-center
BLDG  = np.array([ 0.6,  0.5, 0.0])   # building — slightly right of center
PED   = np.array([ 1.5,  1.2, 0.0])   # pedestrian — behind building right side


# ── Helpers ───────────────────────────────────────────────────────

def _bev_grid(rows: int = 14, cols: int = 20, cell: float = 0.68) -> VGroup:
    g = VGroup()
    hw = cols * cell / 2;  hh = rows * cell / 2
    for i in range(cols + 1):
        x = -hw + i * cell
        g.add(Line([x, -hh, 0], [x, hh, 0],
                   stroke_color=GRID_LINE, stroke_width=0.55,
                   stroke_opacity=0.55))
    for j in range(rows + 1):
        y = -hh + j * cell
        g.add(Line([-hw, y, 0], [hw, y, 0],
                   stroke_color=GRID_LINE, stroke_width=0.55,
                   stroke_opacity=0.55))
    return g


def _car(color: str, w: float = 0.75, h: float = 0.38) -> VGroup:
    body = RoundedRectangle(corner_radius=0.07, width=w, height=h,
                            fill_color=color, fill_opacity=0.95,
                            stroke_color=WHITE, stroke_width=1.5)
    roof = RoundedRectangle(corner_radius=0.05, width=w * 0.50, height=h * 0.54,
                            fill_color=color, fill_opacity=1,
                            stroke_color=WHITE, stroke_width=1.0)
    roof.align_to(body, UP).shift(DOWN * 0.04)
    wr = h * 0.34
    wl_c = Circle(radius=wr, fill_color="#080808", fill_opacity=1,
                  stroke_color=WHITE, stroke_width=0.8)
    wr_c = wl_c.copy()
    wl_c.move_to(body.get_bottom() + LEFT * w * 0.30 + UP * wr * 0.22)
    wr_c.move_to(body.get_bottom() + RIGHT * w * 0.30 + UP * wr * 0.22)
    hl  = Circle(radius=wr * 0.35, fill_color=GOLD,
                 fill_opacity=0.9, stroke_width=0)
    hl.move_to(body.get_right() + LEFT * wr * 0.3 + UP * h * 0.18)
    return VGroup(body, roof, wl_c, wr_c, hl)


def _radar_ring(center: np.ndarray, r: float, color: str,
                opacity: float) -> Ellipse:
    """Single radar ring — ellipse (squash y for BEV depth)."""
    e = Ellipse(width=r * 2.0, height=r * 1.50,
                stroke_color=color,
                stroke_width=max(0.35, 2.0 * opacity),
                stroke_opacity=opacity, fill_opacity=0)
    e.move_to(center)
    return e


def _fm_hexagon_cluster(center: np.ndarray,
                         color: str = P1_FOUNDATION) -> VGroup:
    """3 floating hexagons + connecting wires for FM icons."""
    offsets = [np.array([-0.55, 0.55, 0]),
               np.array([ 0.00, 0.72, 0]),
               np.array([ 0.55, 0.55, 0])]
    labels  = ["GPT-4", "CLIP", "DINO"]
    grp = VGroup()
    hex_mobs = []
    for off, lbl in zip(offsets, labels):
        pos = center + off
        hx = RegularPolygon(n=6, radius=0.22,
                            fill_color=color, fill_opacity=0.30,
                            stroke_color=color, stroke_width=1.4)
        hx.move_to(pos)
        lt = Text(lbl, font_size=SIZE_MICRO - 2, color=color,
                  font=FONT_PRIMARY).move_to(pos)
        grp.add(VGroup(hx, lt))
        hex_mobs.append(hx)
    # Connecting wires
    for i in range(len(hex_mobs)):
        for j in range(i + 1, len(hex_mobs)):
            wire = DashedLine(
                hex_mobs[i].get_center(),
                hex_mobs[j].get_center(),
                stroke_color=color, stroke_width=0.6,
                stroke_opacity=0.40, dash_length=0.07,
            )
            grp.add(wire)
    return grp


def _blind_zone_poly(fill: str, opacity: float) -> Polygon:
    """Shadow behind building — proportional to building size."""
    return Polygon(
        BLDG + RIGHT * 0.53 + UP * 0.60,
        BLDG + RIGHT * 0.53 + DOWN * 0.60,
        BLDG + RIGHT * 2.80 + DOWN * 0.95,
        BLDG + RIGHT * 2.80 + UP * 0.95,
        fill_color=fill, fill_opacity=opacity, stroke_width=0,
    )


def _stick_person(pos: np.ndarray, color: str = P5_PHYSICAL) -> VGroup:
    head = Circle(radius=0.13, fill_color=color, fill_opacity=1,
                  stroke_color=WHITE, stroke_width=0.8)
    head.move_to(pos + UP * 0.32)
    body = Line(pos + UP * 0.19, pos + DOWN * 0.12,
                stroke_color=color, stroke_width=1.5)
    l_arm = Line(pos + UP * 0.08, pos + LEFT * 0.20 + DOWN * 0.05,
                 stroke_color=color, stroke_width=1.2)
    r_arm = Line(pos + UP * 0.08, pos + RIGHT * 0.20 + DOWN * 0.05,
                 stroke_color=color, stroke_width=1.2)
    l_leg = Line(pos + DOWN * 0.12, pos + LEFT * 0.15 + DOWN * 0.35,
                 stroke_color=color, stroke_width=1.2)
    r_leg = Line(pos + DOWN * 0.12, pos + RIGHT * 0.15 + DOWN * 0.35,
                 stroke_color=color, stroke_width=1.2)
    return VGroup(head, body, l_arm, r_arm, l_leg, r_leg)


# ── Continuous radar wave (updater pattern) ───────────────────────

class _RadarSystem:
    """
    Manages a continuous stream of expanding radar rings from `center`.
    Call .add_to(scene) to register, .remove_from(scene) to clean up.
    """
    def __init__(self, center: np.ndarray, color: str,
                 max_r: float = 3.6, speed: float = 1.8,
                 n_rings: int = 5):
        self.center = center
        self.color  = color
        self.max_r  = max_r
        self.speed  = speed
        self.n_rings = n_rings
        self.t = 0.0
        # Each ring has a phase offset so they're spaced non-uniformly
        self.phases = [i / n_rings for i in range(n_rings)]
        self.rings  = VGroup(*[
            _radar_ring(center, 0.05, color, opacity=0.0)
            for _ in range(n_rings)
        ])

    def _updater(self, mob, dt):
        self.t += dt
        for i, ring in enumerate(mob):
            # Non-uniform spacing: inner rings close, outer sparse
            phase = (self.t * self.speed / self.max_r + self.phases[i]) % 1.0
            r = (phase ** 1.4) * self.max_r  # power curve: sparse at edge
            op = max(0.0, 0.88 * (1.0 - phase ** 0.7))
            ring.become(_radar_ring(self.center, max(r, 0.05),
                                    self.color, opacity=op))

    def add_to(self, scene: Scene):
        self.rings.add_updater(self._updater)
        scene.add(self.rings)

    def remove_from(self, scene: Scene):
        self.rings.remove_updater(self._updater)
        scene.remove(self.rings)


# ── Scene ──────────────────────────────────────────────────────────

class I02Hook(Scene):
    def setup(self):
        self.camera.background_color = BG_VOID   # dark during act A/B
        self._radar_systems: list[_RadarSystem] = []

    def construct(self):

        # ────────────────────────────────────────────────────────
        # ACT A — ONE SMART CAR
        # ────────────────────────────────────────────────────────

        # BEV grid
        grid = _bev_grid()
        self.play(FadeIn(grid, run_time=0.7))

        # Car A drives in from LEFT, wheels rolling
        car_a = _car(CYAN_NEON).move_to(CAR_A + LEFT * 9)
        self.add(car_a)
        self.play(car_a.animate(run_time=1.0, rate_func=smooth)
                         .move_to(CAR_A))
        # Brake squish
        self.play(
            car_a.animate(run_time=0.07).stretch(1.10, 0).stretch(0.92, 1),
            car_a.animate(run_time=0.07).stretch(1/1.10, 0).stretch(1/0.92, 1),
        )

        # FM icons float above car A
        fm_icons = _fm_hexagon_cluster(CAR_A + UP * 1.0)
        self.play(
            LaggedStart(*[
                GrowFromCenter(elem, run_time=0.22)
                for elem in fm_icons
            ], lag_ratio=0.15),
        )
        # Gentle float oscillation
        float_t = [0.0]
        def float_update(mob, dt):
            float_t[0] += dt
            mob.set_y(CAR_A[1] + 1.0 + 0.05 * np.sin(float_t[0] * 2.0))
        fm_icons.add_updater(float_update)

        # Radar gravitational waves START — max_r tuned to canvas
        radar_a = _RadarSystem(CAR_A, CYAN_NEON, max_r=2.5, speed=2.0)
        radar_a.add_to(self)
        self._radar_systems.append(radar_a)
        self.wait(2.0)   # watch the beautiful waves

        # ────────────────────────────────────────────────────────
        # ACT B — THE WALL
        # ────────────────────────────────────────────────────────

        # Building drops from above — clearly visible against dark BG
        building = Rectangle(
            width=1.05, height=1.30,
            fill_color="#1C2E50", fill_opacity=1.0,   # brighter navy
            stroke_color="#5B8DC8", stroke_width=2.2, # cyan-blue border
        ).move_to(BLDG)
        # Window details (yellow-warm for realism)
        def _win(offset):
            return Rectangle(width=0.20, height=0.16,
                             fill_color="#FFD060", fill_opacity=0.75,
                             stroke_width=0).move_to(BLDG + offset)
        win1 = _win(UP * 0.30 + LEFT * 0.24)
        win2 = _win(UP * 0.30 + RIGHT * 0.24)
        win3 = _win(DOWN * 0.10 + LEFT * 0.24)
        win4 = _win(DOWN * 0.10 + RIGHT * 0.24)
        bldg_grp = VGroup(building, win1, win2, win3, win4)
        bldg_grp.shift(UP * 8)
        self.add(bldg_grp)

        self.play(
            bldg_grp.animate(run_time=0.50, rate_func=rush_into)
                    .shift(DOWN * 8),
        )
        # Squish on impact
        self.play(
            bldg_grp.animate(run_time=0.06).stretch(1.14, 0).stretch(0.89, 1),
            bldg_grp.animate(run_time=0.07).stretch(1/1.14, 0).stretch(1/0.89, 1),
        )
        # Dust cloud
        dust = VGroup(*[
            Dot(radius=float(RNG.uniform(0.025, 0.065)),
                color=TEXT_GHOST, fill_opacity=0.65)
            .move_to(BLDG + np.array([
                float(RNG.uniform(-0.6, 0.6)), -0.68, 0
            ]))
            for _ in range(14)
        ])
        self.add(dust)
        self.play(
            LaggedStart(*[
                d.animate(run_time=0.45, rate_func=rush_from)
                 .shift(np.array([float(RNG.uniform(-0.7, 0.7)),
                                  float(RNG.uniform(0.15, 0.65)), 0]))
                 .set_fill(opacity=0)
                for d in dust
            ], lag_ratio=0.04),
        )
        self.remove(dust)

        # Blind zone forms
        blind_zone = _blind_zone_poly(RED_ALERT, opacity=0.28)
        self.play(FadeIn(blind_zone, run_time=0.65))

        # FM icons fade (xe thông minh cũng vô dụng)
        fm_icons.remove_updater(float_update)
        self.play(FadeOut(fm_icons, run_time=0.50))
        self.wait(0.25)

        # Text overlay: two lines, heavy and slow
        txt1 = Text("Even the smartest single agent…",
                    font_size=SIZE_LABEL, color=TEXT_WHITE,
                    font=FONT_PRIMARY)
        txt2 = Text("…cannot see around corners.",
                    font_size=SIZE_LABEL, color=RED_ALERT,
                    font=FONT_PRIMARY)
        txt1.to_corner(UR, buff=0.5)
        txt2.next_to(txt1, DOWN, buff=0.22).align_to(txt1, RIGHT)

        self.play(AddTextLetterByLetter(txt1, run_time=1.0))
        self.wait(1.0)
        self.play(AddTextLetterByLetter(txt2, run_time=0.9))
        self.wait(1.2)
        self.play(FadeOut(VGroup(txt1, txt2), run_time=0.35))

        # ────────────────────────────────────────────────────────
        # ACT C — COOPERATION REVEALS
        # ────────────────────────────────────────────────────────

        # Stop car A radar briefly, then restart with 3 cars
        radar_a.remove_from(self)

        # Cars B and C drive in
        car_b = _car(BLUE_ELECTRIC).move_to(CAR_B + UP * 5)
        car_c = _car(P1_FOUNDATION).move_to(CAR_C + DOWN * 5)
        self.add(car_b, car_c)
        self.play(
            car_b.animate(run_time=0.75, rate_func=smooth).move_to(CAR_B),
            car_c.animate(run_time=0.75, rate_func=smooth).move_to(CAR_C),
        )
        self.wait(0.2)

        # 3 radar systems simultaneously — smaller rings, tighter composition
        radar_a2 = _RadarSystem(CAR_A, CYAN_NEON,    max_r=2.4, speed=1.9)
        radar_b  = _RadarSystem(CAR_B, BLUE_ELECTRIC, max_r=2.2, speed=2.1)
        radar_c  = _RadarSystem(CAR_C, P1_FOUNDATION, max_r=2.0, speed=1.8)
        for r in (radar_a2, radar_b, radar_c):
            r.add_to(self)
        self.wait(2.5)   # interference pattern builds up visually

        # Blind zone: red → green (cooperation fills the gap)
        green_zone = _blind_zone_poly(GREEN_SIGNAL, opacity=0.25)
        self.play(ReplacementTransform(blind_zone, green_zone, run_time=1.2))

        # Pedestrian materializes from behind building
        person = _stick_person(PED)
        self.play(FadeIn(person, scale=0.4, run_time=1.0, rate_func=smooth))
        # Gentle glow pulse
        glow = Circle(radius=0.35, stroke_color=P5_PHYSICAL,
                      stroke_opacity=0, fill_opacity=0)
        glow.move_to(PED)
        self.play(
            glow.animate(run_time=0.6).scale(2.8).set_stroke(opacity=0.35),
            glow.copy().animate(run_time=0.8).scale(4.0).set_stroke(opacity=0),
        )
        self.wait(0.3)

        # Stop all radar before quote
        for r in (radar_a2, radar_b, radar_c):
            r.remove_from(self)

        # ── THE QUOTE — khắc vào đá ────────────────────────────
        # Dim overlay
        dim = FullScreenRectangle(fill_color="#020408",
                                  fill_opacity=0.50, stroke_width=0)
        self.play(FadeIn(dim, run_time=0.55))

        q1 = Text('"So we taught them to cooperate."',
                  font_size=SIZE_BODY + 6,
                  color=GOLD, font=FONT_PRIMARY, slant=ITALIC)
        q1.move_to(ORIGIN + DOWN * 0.1)
        if q1.width > 11.5:
            q1.scale(11.5 / q1.width)

        self.play(Write(q1, run_time=2.5))
        self.wait(3.0)   # mandatory hold per guide

        # Fade everything
        all_main = [grid, car_a, car_b, car_c, bldg_grp,
                    green_zone, person, glow, q1, dim]
        self.play(
            LaggedStart(*[FadeOut(m, run_time=0.50) for m in all_main],
                        lag_ratio=0.06),
        )
        self.wait(0.3)
