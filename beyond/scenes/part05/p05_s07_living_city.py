# beyond/scenes/part05/p05_s07_living_city.py
# ─────────────────────────────────────────────────────────────────
# P5-07  THE LIVING CITY — GRAND FINALE  (~50s)
# Cảnh WOW nhất của toàn bộ video. Không giới hạn render time.
#
# PHASE 1 (0-15s): Thành phố đêm — từng loại agent fade in:
#   cars (BLUE_ELECTRIC), robots (GREEN_SIGNAL),
#   wheelchairs (P5_PHYSICAL), pedestrians (GOLD),
#   RSU towers (ORANGE_INFRA), drones (WHITE nhạt).
#
# PHASE 2 (15-30s): Communication web sáng lên — thin lines LaggedStart.
#   Radar waves từ tất cả agents. "Thành phố thở".
#
# PHASE 3 (30-50s): 5 vignette panels drop in (P1→P5 recap).
#   Fade out → city trở lại full screen.
#
# FINAL: "Beyond Self-Driving. / Not just smarter cars. / A safer world."
#   Write từng dòng, GOLD. Roadmap 5 nút gold pulsing. FIN.
#
# Render:  manim -ql "beyond/scenes/part05/p05_s07_living_city.py" P05S07LivingCity
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components.colors import (
    BG_VOID, BG_SPACE, GRID_LINE,
    GOLD, GOLD_GLOW, CYAN_NEON, BLUE_ELECTRIC,
    GREEN_SIGNAL, P5_PHYSICAL, ORANGE_INFRA,
    P1_FOUNDATION, P2_COOP, P3_SIM, P4_EFFICIENT,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST, COMM_LINK,
    SIZE_BODY, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=2025)

# ── City layout ────────────────────────────────────────────────────
CITY_BLOCKS = [
    # (center_x, center_y, w, h) — dark rectangles
    (-4.5,  2.0, 1.8, 1.5),
    (-1.8,  2.2, 2.0, 1.2),
    ( 1.5,  2.4, 1.5, 1.0),
    ( 4.2,  2.1, 1.6, 1.4),
    (-4.8, -0.8, 1.4, 2.0),
    ( 4.6, -0.5, 1.5, 1.8),
    (-3.0, -2.5, 2.2, 1.3),
    ( 2.8, -2.3, 2.0, 1.5),
]

AGENT_DEFS = [
    # (color, n_agents, role, size, path_style)
    (BLUE_ELECTRIC, 4, "car",        0.35, "bezier"),
    (GREEN_SIGNAL,  3, "robot",      0.22, "grid"),
    (P5_PHYSICAL,   3, "wheelchair", 0.25, "slow"),
    (GOLD,          5, "pedestrian", 0.18, "organic"),
    (ORANGE_INFRA,  3, "rsu",        0.28, "static"),
]


def _city_grid() -> VGroup:
    g = VGroup()
    for i in range(-8, 9):
        x = i * 0.85
        g.add(Line([x, -4, 0], [x, 4, 0],
                   stroke_color=GRID_LINE, stroke_width=0.45,
                   stroke_opacity=0.40))
    for j in range(-5, 6):
        y = j * 0.85
        g.add(Line([-7, y, 0], [7, y, 0],
                   stroke_color=GRID_LINE, stroke_width=0.45,
                   stroke_opacity=0.40))
    return g


def _building(cx, cy, w, h) -> VGroup:
    rect = Rectangle(width=w, height=h,
                     fill_color="#0A1628", fill_opacity=1.0,
                     stroke_color="#1E3A5F", stroke_width=1.2)
    rect.move_to([cx, cy, 0])
    # Window lights
    wins = VGroup()
    cols_n = max(1, int(w / 0.45))
    rows_n = max(1, int(h / 0.45))
    for r in range(rows_n):
        for c in range(cols_n):
            if RNG.random() > 0.45:
                wx = cx - w/2 + (c + 0.5) * w/cols_n
                wy = cy - h/2 + (r + 0.5) * h/rows_n
                win = Rectangle(width=0.12, height=0.10,
                                fill_color="#FFD060", fill_opacity=0.65,
                                stroke_width=0)
                win.move_to([wx, wy, 0])
                wins.add(win)
    return VGroup(rect, wins)


def _agent(color: str, size: float) -> VGroup:
    body = Circle(radius=size, fill_color=color, fill_opacity=0.90,
                  stroke_color=WHITE, stroke_width=0.8)
    return body


def _random_road_pos() -> np.ndarray:
    """Random position NOT inside a building."""
    for _ in range(50):
        x = float(RNG.uniform(-5.5, 5.5))
        y = float(RNG.uniform(-3.2, 3.2))
        # Check not inside any building
        ok = True
        for cx, cy, w, h in CITY_BLOCKS:
            if abs(x - cx) < w/2 + 0.3 and abs(y - cy) < h/2 + 0.3:
                ok = False
                break
        if ok:
            return np.array([x, y, 0.0])
    return np.array([float(RNG.uniform(-3, 3)), float(RNG.uniform(-2, 2)), 0.0])


def _vignette_panel(title: str, color: str, desc: str,
                    pos: np.ndarray) -> VGroup:
    bg = RoundedRectangle(corner_radius=0.10, width=3.0, height=1.6,
                          fill_color="#0A1020", fill_opacity=0.95,
                          stroke_color=color, stroke_width=1.5)
    bg.move_to(pos)
    t = Text(title, font_size=SIZE_MICRO + 2, color=color,
             font=FONT_PRIMARY, weight=BOLD)
    d = Text(desc, font_size=SIZE_MICRO - 1, color=TEXT_DIM,
             font=FONT_PRIMARY, line_spacing=0.38)
    VGroup(t, d).arrange(DOWN, buff=0.10).move_to(pos)
    return VGroup(bg, t, d)


class P05S07LivingCity(Scene):
    def setup(self):
        self.camera.background_color = BG_VOID

    def construct(self):
        # ────────────────────────────────────────────────────────
        # PHASE 1 — City at Night
        # ────────────────────────────────────────────────────────

        # Road grid
        grid = _city_grid()
        self.play(FadeIn(grid, run_time=0.80))

        # Buildings with window lights
        buildings = VGroup(*[_building(*b) for b in CITY_BLOCKS])
        self.play(
            LaggedStart(*[FadeIn(b, run_time=0.35) for b in buildings],
                        lag_ratio=0.10),
        )
        self.wait(0.4)

        # Agents fade in by type, staggered
        all_agents = []
        agent_positions = []

        for color, n, role, size, _ in AGENT_DEFS:
            group_agents = VGroup()
            group_positions = []
            for _ in range(n):
                pos = _random_road_pos()
                a = _agent(color, size).move_to(pos)
                group_agents.add(a)
                group_positions.append(pos)
            all_agents.append(group_agents)
            agent_positions.append(group_positions)

            self.play(
                LaggedStart(*[GrowFromCenter(a, run_time=0.28)
                              for a in group_agents], lag_ratio=0.15),
            )
            self.wait(0.2)

        self.wait(0.5)

        # ────────────────────────────────────────────────────────
        # PHASE 2 — Communication Web
        # ────────────────────────────────────────────────────────

        # Create comm links between nearby agents
        all_agent_mobs = [a for grp in all_agents for a in grp]
        all_agent_pos  = [pos for grp in agent_positions for pos in grp]

        links = VGroup()
        for i, (pi, ai) in enumerate(zip(all_agent_pos, all_agent_mobs)):
            for j, (pj, aj) in enumerate(zip(all_agent_pos, all_agent_mobs)):
                if j <= i:
                    continue
                dist = np.linalg.norm(np.array(pi) - np.array(pj))
                if dist < 2.8:
                    link = Line(pi, pj, stroke_color=COMM_LINK,
                                stroke_width=0.6, stroke_opacity=0.30)
                    links.add(link)

        self.play(
            LaggedStart(*[Create(l, run_time=0.15) for l in links],
                        lag_ratio=0.02),
        )

        # Signal pings from each agent
        ping_anims = []
        for pos in all_agent_pos[:8]:   # limit for performance
            ping_anims.append(
                AnimationGroup(*[
                    Circle(radius=0.05 * (k+1),
                           stroke_color=COMM_LINK,
                           stroke_width=max(0.3, 1.5 - k*0.4),
                           stroke_opacity=max(0, 0.7 - k*0.2),
                           fill_opacity=0)
                    .move_to(pos)
                    .animate(run_time=0.70, rate_func=rush_from)
                    .scale(8 + k*3).set_stroke(opacity=0)
                    for k in range(3)
                ])
            )
        self.play(LaggedStart(*ping_anims, lag_ratio=0.08))
        self.wait(0.6)

        # ────────────────────────────────────────────────────────
        # PHASE 3 — 5 Vignette Panels
        # ────────────────────────────────────────────────────────

        # Dim city
        dim = FullScreenRectangle(fill_color="#010308",
                                  fill_opacity=0.60, stroke_width=0)
        self.play(FadeIn(dim, run_time=0.55))

        panel_data = [
            ("Part 1", P1_FOUNDATION, "FM → reasoning\nLong tail handled",
             np.array([-4.5, 1.8, 0])),
            ("Part 2", P2_COOP,       "Radar waves\nBlind zone → green",
             np.array([-1.5, 1.8, 0])),
            ("Part 3", P3_SIM,        "Sensor calibration\nSim → Real",
             np.array([ 1.5, 1.8, 0])),
            ("Part 4", P4_EFFICIENT,  "FP32 → INT8\n300× smaller",
             np.array([-3.0, -1.0, 0])),
            ("Part 5", P5_PHYSICAL,   "Zombie → Human\nCity alive",
             np.array([ 0.0, -1.0, 0])),
        ]

        panels = [_vignette_panel(t, c, d, pos) for t, c, d, pos in panel_data]

        self.play(
            LaggedStart(*[
                FadeIn(p, shift=DOWN * 0.3, run_time=0.45)
                for p in panels
            ], lag_ratio=0.18),
        )
        self.wait(2.5)

        # Fade panels out
        self.play(
            LaggedStart(*[FadeOut(p, run_time=0.35) for p in panels],
                        lag_ratio=0.06),
            FadeOut(dim, run_time=0.55),
        )
        self.wait(0.3)

        # ────────────────────────────────────────────────────────
        # FINAL TEXT
        # ────────────────────────────────────────────────────────

        final_lines = [
            "Beyond Self-Driving.",
            "Not just smarter cars.",
            "A safer world.",
        ]
        final_mobs = VGroup()
        for i, txt in enumerate(final_lines):
            fs = SIZE_BODY + 8 if i == 0 else SIZE_BODY + 4 if i == 1 else SIZE_BODY + 8
            col = GOLD if i != 1 else TEXT_WHITE
            m = Text(txt, font_size=fs, color=col,
                     font=FONT_PRIMARY,
                     weight=BOLD if i != 1 else NORMAL,
                     slant=ITALIC if i == 2 else NORMAL)
            final_mobs.add(m)
        final_mobs.arrange(DOWN, buff=0.35).move_to(ORIGIN)

        for i, m in enumerate(final_mobs):
            self.play(Write(m, run_time=0.90))
            wait_t = 1.0 if i < 2 else 3.0   # "A safer world." hold 3s per guide
            self.wait(wait_t)

        # Roadmap strip — all 5 gold, pulsing
        spacing = 1.1
        rm_line = Line(LEFT * spacing * 2, RIGHT * spacing * 2,
                       stroke_color=GOLD, stroke_width=1.3)
        rm_dots = VGroup(*[
            Circle(radius=0.12, fill_color=GOLD, fill_opacity=1.0,
                   stroke_color=GOLD_GLOW, stroke_width=1.6)
            .move_to([(i - 2) * spacing, 0, 0])
            for i in range(5)
        ])
        roadmap = VGroup(rm_line, rm_dots).move_to(DOWN * 3.0)
        self.play(FadeIn(roadmap, run_time=0.55))

        # All 5 dots pulse
        self.play(
            LaggedStart(*[
                Flash(d.get_center(), color=GOLD,
                      flash_radius=0.28, num_lines=6, run_time=0.30)
                for d in rm_dots
            ], lag_ratio=0.12),
        )
        self.wait(1.5)

        # ── DISSOLVE INTO SINGLE POINT ─────────────────────────
        everything = VGroup(grid, buildings,
                            *all_agents, links, roadmap, *final_mobs)
        center_dot = Dot(radius=0.0, color=GOLD, fill_opacity=1.0).move_to(ORIGIN)
        self.add(center_dot)

        self.play(
            *[mob.animate(run_time=1.5, rate_func=smooth)
                .move_to(ORIGIN).scale(0.01).set_opacity(0)
              for mob in [grid, buildings,
                          *all_agents, links, roadmap, final_mobs]],
            center_dot.animate(run_time=0.5).scale(800).set_fill(opacity=0),
        )
        self.wait(0.3)

        # Final single pulse → darkness
        seed = Dot(radius=0.06, color=GOLD, fill_opacity=1.0).move_to(ORIGIN)
        self.play(GrowFromCenter(seed, run_time=0.3))
        self.play(seed.animate(run_time=0.3, rate_func=there_and_back).scale(3.0))
        self.play(FadeOut(seed, run_time=0.4))
        self.wait(0.5)
