# beyond/scenes/part02/p02_s04_occlusion.py
# ─────────────────────────────────────────────────────────────────
# P2-04  OCCLUSION — RADAR GRAVITATIONAL WAVES  (~75s)
#
# Cảnh đặc trưng nhất của cả video. Full cinematic treatment.
# 2D BEV view với camera tilt effect (simulated bằng scaling).
# Sóng radar tỏa ra như gravitational waves — ellipsoid shells,
# khoảng cách không đều, afterglow.
# Tòa nhà rơi, sóng bị bóp méo, blind zone đỏ.
# 2 xe thêm → 3 hệ sóng → interference → xanh lá.
# Người đi bộ xuất hiện sau tòa nhà.
# Quote: "Cooperation is a physics solution, not an algorithm one."
#
# Render:  manim -ql "beyond/scenes/part02/p02_s04_occlusion.py" P02S04Occlusion
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    signal_ping, glow_pulse,
    BG_SPACE, BG_PANEL, BG_GRID_LINE, GRID_LINE,
    GOLD, CYAN_NEON, BLUE_ELECTRIC,
    P1_FOUNDATION, P2_COOP,
    RED_ALERT, RED_DIM, GREEN_SIGNAL, GREEN_DIM,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_BODY, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=99)

# ── BEV layout constants (all in Manim units) ─────────────────────
CAR_A_POS   = np.array([-3.8, -1.2, 0])   # hero car
CAR_B_POS   = np.array([ 2.5,  2.2, 0])   # second car
CAR_C_POS   = np.array([-1.5, -3.1, 0])   # third car
BUILDING_POS = np.array([ 0.3,  0.1, 0])  # obstacle center
PEDESTRIAN_POS = np.array([ 1.0, 1.2, 0]) # hidden behind building


# ── Helper: car icon ──────────────────────────────────────────────

def _car_icon(color: str, size: float = 0.38) -> VGroup:
    body = RoundedRectangle(corner_radius=0.06,
                            width=size * 2.2, height=size * 0.9,
                            fill_color=color, fill_opacity=0.95,
                            stroke_color=WHITE, stroke_width=1.4)
    roof = RoundedRectangle(corner_radius=0.04,
                            width=size * 1.1, height=size * 0.55,
                            fill_color=color, fill_opacity=1.0,
                            stroke_color=WHITE, stroke_width=1.0)
    roof.align_to(body, UP).shift(DOWN * 0.04)
    wl = Circle(radius=size * 0.22, fill_color="#0A0A0A",
                fill_opacity=1, stroke_color=WHITE, stroke_width=0.8)
    wr = wl.copy()
    wl.move_to(body.get_bottom() + LEFT * size * 0.55 + UP * size * 0.12)
    wr.move_to(body.get_bottom() + RIGHT * size * 0.55 + UP * size * 0.12)
    return VGroup(body, roof, wl, wr)


# ── Helper: radar ring ────────────────────────────────────────────

def _radar_ring(center: np.ndarray, radius: float,
                color: str, opacity: float) -> Ellipse:
    """Single radar ring — ellipsoid (slightly squashed for BEV feel)."""
    ring = Ellipse(
        width=radius * 2.0,
        height=radius * 1.55,      # squash vertically for depth illusion
        stroke_color=color,
        stroke_width=max(0.4, 2.2 * opacity),
        stroke_opacity=opacity,
        fill_opacity=0,
    )
    ring.move_to(center)
    return ring


def _radar_burst(scene: Scene, center: np.ndarray, color: str,
                 n_rings: int = 5, max_r: float = 3.2,
                 run_time: float = 1.5, phase_offset: float = 0.0):
    """
    Animates n_rings expanding radar rings from center.
    Rings are unevenly spaced (gravitational wave style: close at center,
    sparse at edge). Each ring fades as it expands.
    """
    rings = []
    for i in range(n_rings):
        # Non-uniform spacing: inner rings close together
        frac = ((i + 1) / n_rings) ** 1.6
        target_r = frac * max_r
        start_r = 0.05

        r_mob = _radar_ring(center, start_r, color, opacity=0.85)
        scene.add(r_mob)
        rings.append((r_mob, target_r))

    scene.play(
        LaggedStart(*[
            AnimationGroup(
                r.animate(run_time=run_time, rate_func=linear)
                 .become(_radar_ring(center, tr, color,
                                     opacity=max(0, 0.9 - tr / max_r * 0.95))),
            )
            for r, tr in rings
        ], lag_ratio=phase_offset / n_rings),
        run_time=run_time,
    )
    # Remove rings after they finish
    for r, _ in rings:
        scene.remove(r)


# ── BEV background grid ────────────────────────────────────────────

def _bev_grid(n: int = 12, cell: float = 0.7) -> VGroup:
    grid = VGroup()
    half = n * cell / 2
    for i in range(n + 1):
        x = -half + i * cell
        grid.add(Line([x, -half, 0], [x, half, 0],
                      stroke_color=GRID_LINE, stroke_width=0.6,
                      stroke_opacity=0.55))
        grid.add(Line([-half, x, 0], [half, x, 0],
                      stroke_color=GRID_LINE, stroke_width=0.6,
                      stroke_opacity=0.55))
    return grid


# ── Scene ──────────────────────────────────────────────────────────

class P02S04Occlusion(BeyondScene):
    PART_COLOR = P2_COOP
    SHOW_AMBIENT = False  # keep BEV clean — no floating particles

    def construct(self):
        # ── [0s] BEV grid appears ──────────────────────────────
        grid = _bev_grid()
        self.play(FadeIn(grid, run_time=0.6))

        # ── [0.5s] Hero car A drives in from LEFT ─────────────
        car_a = _car_icon(CYAN_NEON).move_to(CAR_A_POS + LEFT * 6)
        self.add(car_a)
        # Wheels "spin" during drive — simulate with horizontal scaling oscillation
        self.play(
            car_a.animate(run_time=0.9, rate_func=smooth).move_to(CAR_A_POS),
        )
        # Brake squish
        self.play(
            car_a.animate(run_time=0.07).stretch(1.08, 0).stretch(0.94, 1),
            car_a.animate(run_time=0.07).stretch(1/1.08, 0).stretch(1/0.94, 1),
        )
        self.wait(0.15)

        # ── [1.0s] Radar waves START (car A, cyan) ─────────────
        # 3 separate "burst" plays to get continuous wave feel
        for phase in [0.0, 0.35, 0.70]:
            _radar_burst(self, CAR_A_POS, CYAN_NEON, n_rings=4,
                         max_r=3.0, run_time=1.1, phase_offset=phase)

        self.wait(0.1)

        # ── [1.8s] BUILDING DROPS ──────────────────────────────
        building = Rectangle(
            width=1.0, height=1.2,
            fill_color=BG_PANEL, fill_opacity=0.96,
            stroke_color=TEXT_DIM, stroke_width=1.8,
        ).move_to(BUILDING_POS + UP * 7)  # start high above

        self.add(building)

        # Dust cloud dots
        dust = VGroup(*[
            Dot(radius=RNG.uniform(0.03, 0.07), color=TEXT_GHOST, fill_opacity=0.7)
            .move_to(BUILDING_POS + np.array([
                RNG.uniform(-0.55, 0.55), -0.62, 0
            ]))
            for _ in range(12)
        ])

        self.play(
            building.animate(run_time=0.48, rate_func=rush_into)
                    .move_to(BUILDING_POS),
        )
        # Squish on impact
        self.play(
            building.animate(run_time=0.06).stretch(1.12, 0).stretch(0.90, 1),
            building.animate(run_time=0.07).stretch(1/1.12, 0).stretch(1/0.90, 1),
        )
        # Dust burst
        self.add(dust)
        self.play(
            LaggedStart(*[
                d.animate(run_time=0.40, rate_func=rush_from)
                 .shift(np.array([RNG.uniform(-0.6, 0.6),
                                  RNG.uniform(0.1, 0.5), 0]))
                 .set_fill(opacity=0)
                for d in dust
            ], lag_ratio=0.04),
        )
        self.remove(dust)

        # ── [2.2s] BLIND ZONE forms behind building ────────────
        # Building blocks radar → shadow zone (polygon behind building)
        # Approximate blind zone as a stretched triangle behind building
        blind_zone = Polygon(
            BUILDING_POS + RIGHT * 0.5 + UP * 0.6,    # upper-right edge of building
            BUILDING_POS + RIGHT * 0.5 + DOWN * 0.6,  # lower-right edge
            BUILDING_POS + RIGHT * 3.2 + DOWN * 1.0,  # far bottom-right
            BUILDING_POS + RIGHT * 3.2 + UP * 1.0,    # far top-right
            fill_color=RED_ALERT, fill_opacity=0.22,
            stroke_width=0,
        )

        self.play(FadeIn(blind_zone, run_time=0.55))
        self.wait(0.1)

        # ── [3.0s] Text: single agent warning ─────────────────
        warning_txt = Text("Single agent: blind to occlusions.",
                           font_size=SIZE_LABEL - 1,
                           color=RED_ALERT, font=FONT_PRIMARY)
        warning_txt.to_corner(UR, buff=0.45)
        self.play(FadeIn(warning_txt, shift=DOWN * 0.08, run_time=0.4))
        self.wait(0.6)
        self.play(FadeOut(warning_txt, run_time=0.3))

        # ── [3.8s] Car B drives in (upper-right) ──────────────
        car_b = _car_icon(BLUE_ELECTRIC).move_to(CAR_B_POS + UP * 5)
        self.add(car_b)
        self.play(car_b.animate(run_time=0.65, rate_func=smooth).move_to(CAR_B_POS))

        # ── [4.0s] Car C drives in (bottom) ───────────────────
        car_c = _car_icon(P1_FOUNDATION).move_to(CAR_C_POS + DOWN * 5)
        self.add(car_c)
        self.play(car_c.animate(run_time=0.65, rate_func=smooth).move_to(CAR_C_POS))
        self.wait(0.15)

        # ── [4.3s] THREE WAVE SYSTEMS ─────────────────────────
        # Play simultaneous radar bursts from all three cars
        # Achieve by adding rings in parallel using AnimationGroup
        wave_data = [
            (CAR_A_POS, CYAN_NEON),
            (CAR_B_POS, BLUE_ELECTRIC),
            (CAR_C_POS, P1_FOUNDATION),
        ]

        # Two rounds of waves
        for _round in range(2):
            ring_groups = []
            for center, color in wave_data:
                rings_this_car = []
                for i in range(4):
                    frac = ((i + 1) / 4) ** 1.5
                    target_r = frac * 3.0
                    r = _radar_ring(center, 0.05, color, opacity=0.80)
                    self.add(r)
                    rings_this_car.append((r, target_r, color))
                ring_groups.append(rings_this_car)

            self.play(
                *[
                    r.animate(run_time=1.1, rate_func=linear)
                     .become(_radar_ring(center, tr, color,
                                         opacity=max(0, 0.85 - tr / 3.0 * 0.92)))
                    for ring_list, (center, color) in zip(ring_groups, wave_data)
                    for r, tr, _ in ring_list
                ],
                run_time=1.1,
            )
            for ring_list in ring_groups:
                for r, _, _ in ring_list:
                    self.remove(r)

        # ── [5.0s] Camera rotate effect ─────────────────────────
        # Simulate by slightly scaling the whole scene group
        scene_group = VGroup(grid, car_a, car_b, car_c, building, blind_zone)
        self.play(
            scene_group.animate(run_time=1.0, rate_func=smooth)
                       .stretch(0.94, 1)  # slight vertical squash → depth
                       .shift(DOWN * 0.12),
        )

        # ── [5.5s] BLIND ZONE: red → green ────────────────────
        green_zone = Polygon(
            *blind_zone.get_vertices(),
            fill_color=GREEN_SIGNAL, fill_opacity=0.22, stroke_width=0,
        )

        self.play(ReplacementTransform(blind_zone, green_zone, run_time=1.0))

        # ── [6.0s] Pedestrian MATERIALIZES — khoảnh khắc cảm xúc ─
        # Proper stick figure — họ đã ở đó từ đầu, ta mới vừa nhìn thấy
        ped_pos = PEDESTRIAN_POS
        ped_head = Circle(radius=0.13, fill_color="#F06292", fill_opacity=1,
                          stroke_color=WHITE, stroke_width=1.0)
        ped_head.move_to(ped_pos + UP * 0.34)
        ped_body = Line(ped_pos + UP * 0.20, ped_pos + DOWN * 0.10,
                        stroke_color="#F06292", stroke_width=1.8)
        ped_la   = Line(ped_pos + UP * 0.07, ped_pos + LEFT * 0.17 + DOWN * 0.03,
                        stroke_color="#F06292", stroke_width=1.3)
        ped_ra   = Line(ped_pos + UP * 0.07, ped_pos + RIGHT * 0.17 + DOWN * 0.03,
                        stroke_color="#F06292", stroke_width=1.3)
        ped_ll   = Line(ped_pos + DOWN * 0.10, ped_pos + LEFT * 0.12 + DOWN * 0.32,
                        stroke_color="#F06292", stroke_width=1.3)
        ped_rl   = Line(ped_pos + DOWN * 0.10, ped_pos + RIGHT * 0.12 + DOWN * 0.32,
                        stroke_color="#F06292", stroke_width=1.3)
        pedestrian = VGroup(ped_head, ped_body, ped_la, ped_ra, ped_ll, ped_rl)

        # Ghost-like materialization: opacity 0 → 1, slow
        pedestrian.set_opacity(0)
        self.add(pedestrian)
        self.play(
            pedestrian.animate(run_time=1.0, rate_func=smooth).set_opacity(1.0),
        )
        self.play(
            glow_pulse(ped_head, color="#F06292", n_pulses=2, run_time=0.40),
            Flash(ped_pos, color="#F06292",
                  flash_radius=0.50, num_lines=8, run_time=0.45),
        )
        self.wait(0.5)

        # ── [6.5s] Signal ping — all 3 cars acknowledge ────────
        self.play(
            AnimationGroup(*[
                signal_ping(center, color)
                for center, color in wave_data
            ]),
        )
        self.wait(0.5)

        # ── [7.0s] THE QUOTE — khắc vào đá ────────────────────
        # World dims. Quote appears large, gold, center stage.
        fade_overlay = FullScreenRectangle(fill_color="#020408",
                                           fill_opacity=0.60, stroke_width=0)
        self.play(FadeIn(fade_overlay, run_time=0.60))

        quote_line1 = Text(
            '"Cooperation is a physics solution,',
            font_size=SIZE_BODY + 6,
            color=GOLD, font=FONT_PRIMARY, slant=ITALIC,
        )
        quote_line2 = Text(
            '  not an algorithm one."',
            font_size=SIZE_BODY + 6,
            color=GOLD, font=FONT_PRIMARY, slant=ITALIC,
        )
        quote = VGroup(quote_line1, quote_line2).arrange(DOWN, buff=0.18,
                                                          aligned_edge=LEFT)
        quote.move_to(ORIGIN + DOWN * 0.15)
        # Clamp width
        if quote.width > 11.2:
            quote.scale(11.2 / quote.width)

        # Write slowly — each line gets its own beat
        self.play(Write(quote_line1, run_time=1.60))
        self.wait(0.40)
        self.play(Write(quote_line2, run_time=1.20))
        self.wait(2.5)  # mandatory 2.5s hold per 5_PART_GUIDE

        # ── CLOSE ─────────────────────────────────────────────
        all_mobs = [
            grid, car_a, car_b, car_c, building,
            green_zone, pedestrian, quote, fade_overlay,
        ]
        self.play(
            LaggedStart(*[FadeOut(m, run_time=0.4) for m in all_mobs],
                        lag_ratio=0.06),
        )
        self.wait(0.2)
