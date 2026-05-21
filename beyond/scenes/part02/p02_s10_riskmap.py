# beyond/scenes/part02/p02_s10_riskmap.py
# ─────────────────────────────────────────────────────────────────
# P2-10  RISKMAP  (~45s)
#
# Top-down road view. Risk field = heatmap overlay:
#   đỏ nóng quanh xe khác, cam giao lộ, xanh làn trống.
# Khi xe di chuyển: heatmap update real-time.
# Xe bẻ lái đột ngột → vùng nguy hiểm bùng to.
# Trajectory planning: đường path tự né vùng đỏ như sông tránh đá.
#
# Render:  manim -ql "beyond/scenes/part02/p02_s10_riskmap.py" P02S10RiskMap
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    BG_SPACE, GRID_LINE,
    P2_COOP, RED_ALERT, RED_DIM, GREEN_SIGNAL,
    GOLD, CYAN_NEON, TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=66)

# ── Scene geometry ─────────────────────────────────────────────────
ROAD_W = 9.5
ROAD_H = 5.5
LANE_W = 2.0

# Obstacle vehicle positions
OBSTACLES = [
    np.array([ 1.5,  0.8, 0.0]),
    np.array([-2.0, -0.5, 0.0]),
    np.array([ 3.5, -1.0, 0.0]),
]

def _road() -> VGroup:
    """Simple road with lane markings."""
    road = Rectangle(width=ROAD_W, height=ROAD_H,
                     fill_color="#050F18", fill_opacity=1.0,
                     stroke_color="#0D1829", stroke_width=1.5)
    # Lane lines
    lanes = VGroup()
    for x in [-LANE_W, 0, LANE_W]:
        l = DashedLine(
            [x, -ROAD_H/2 + 0.3, 0], [x, ROAD_H/2 - 0.3, 0],
            stroke_color=TEXT_DIM, stroke_width=0.6,
            stroke_opacity=0.40, dash_length=0.25,
        )
        lanes.add(l)
    # Road edges
    edge_l = Line([-ROAD_W/2, -ROAD_H/2, 0], [-ROAD_W/2, ROAD_H/2, 0],
                  stroke_color=TEXT_DIM, stroke_width=1.2, stroke_opacity=0.6)
    edge_r = Line([ ROAD_W/2, -ROAD_H/2, 0], [ ROAD_W/2, ROAD_H/2, 0],
                  stroke_color=TEXT_DIM, stroke_width=1.2, stroke_opacity=0.6)
    return VGroup(road, lanes, edge_l, edge_r)


def _risk_ellipse(center: np.ndarray, rx: float, ry: float,
                  color: str, opacity: float) -> Ellipse:
    e = Ellipse(width=rx*2, height=ry*2,
                fill_color=color, fill_opacity=opacity, stroke_width=0)
    e.move_to(center)
    return e


def _vehicle(color: str, size: float = 0.45) -> VGroup:
    body = RoundedRectangle(corner_radius=0.06, width=size, height=size*0.60,
                            fill_color=color, fill_opacity=0.90,
                            stroke_color=WHITE, stroke_width=1.2)
    roof = Rectangle(width=size*0.50, height=size*0.32,
                     fill_color=color, fill_opacity=1.0, stroke_width=0)
    roof.align_to(body, UP).shift(DOWN*0.04)
    return VGroup(body, roof)


class P02S10RiskMap(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("RiskMap — Cooperative Risk Field Estimation")
        self.wait(0.2)

        # ── Road setup ────────────────────────────────────────
        road = _road()
        self.play(FadeIn(road, run_time=0.50))

        # Obstacle vehicles
        obs_vehicles = VGroup()
        for pos in OBSTACLES:
            v = _vehicle(TEXT_DIM, size=0.48).move_to(pos)
            obs_vehicles.add(v)
        self.play(
            LaggedStart(*[GrowFromCenter(v, run_time=0.28) for v in obs_vehicles],
                        lag_ratio=0.15),
        )

        # ── Initial risk map (static) ─────────────────────────
        risk_zones = VGroup()
        for pos in OBSTACLES:
            # Danger zone (red, tight)
            r1 = _risk_ellipse(pos, 1.1, 0.75, RED_ALERT, 0.32)
            # Transition zone (orange)
            r2 = _risk_ellipse(pos, 1.8, 1.25, "#FF6D00", 0.16)
            # Warning zone (amber, wide)
            r3 = _risk_ellipse(pos, 2.6, 1.80, GOLD, 0.08)
            risk_zones.add(VGroup(r3, r2, r1))

        # Intersection risk
        inter_risk = _risk_ellipse(np.array([0, 0, 0]), 2.2, 1.6, "#FF6D00", 0.12)

        self.play(
            LaggedStart(*[FadeIn(z, run_time=0.35) for z in risk_zones],
                        lag_ratio=0.12),
            FadeIn(inter_risk, run_time=0.35),
        )
        self.wait(0.4)

        # ── Hero vehicle approaches ────────────────────────────
        hero = _vehicle(CYAN_NEON, size=0.52).move_to([-4.2, -0.3, 0])
        self.play(GrowFromCenter(hero, run_time=0.35))
        self.play(
            hero.animate(run_time=1.2, rate_func=smooth).shift(RIGHT * 2.5),
        )

        # Update risk: zones shift slightly as hero moves
        self.play(
            LaggedStart(*[
                z.animate(run_time=0.40, rate_func=smooth).scale(0.95)
                for z in risk_zones
            ], lag_ratio=0.08),
        )
        self.wait(0.3)

        # ── Sudden swerve from obstacle #2 ─────────────────────
        self.play(
            obs_vehicles[1].animate(run_time=0.25, rate_func=rush_into)
                           .shift(RIGHT * 0.9 + UP * 0.3),
        )
        # Risk EXPLODES
        danger_burst = _risk_ellipse(
            OBSTACLES[1] + RIGHT * 0.9 + UP * 0.3, 3.0, 2.0,
            RED_ALERT, 0.45
        )
        self.play(
            FadeIn(danger_burst, scale=0.3, run_time=0.25),
            Flash(obs_vehicles[1].get_center(), color=RED_ALERT,
                  flash_radius=0.80, num_lines=8, run_time=0.30),
        )
        self.wait(0.3)
        self.play(
            danger_burst.animate(run_time=0.55, rate_func=smooth)
                        .set_fill(opacity=0.20).scale(0.75),
        )

        # ── Label ─────────────────────────────────────────────
        lbl = Text('"Risk is a language — not a bounding box."',
                   font_size=SIZE_LABEL - 1, color=GOLD,
                   font=FONT_PRIMARY, slant=ITALIC)
        lbl.to_edge(DOWN, buff=0.52)
        self.play(FadeIn(lbl, shift=UP * 0.08, run_time=0.40))
        self.wait(0.4)

        # ── Trajectory planning: path avoids red zones ─────────
        # Bezier path curving around obstacles
        waypoints = [
            np.array([-1.6, -0.3, 0]),
            np.array([-0.5, -1.4, 0]),    # dip below obstacle 2
            np.array([ 0.8, -1.6, 0]),
            np.array([ 2.5, -0.9, 0]),
            np.array([ 4.0, -0.5, 0]),
        ]
        safe_path = VMobject(stroke_color=GREEN_SIGNAL,
                             stroke_width=2.5, stroke_opacity=0.90,
                             fill_opacity=0)
        safe_path.set_points_smoothly([wp for wp in waypoints])

        path_arrow = CurvedArrow(
            waypoints[0], waypoints[-1],
            angle=-0.4, color=GREEN_SIGNAL,
            stroke_width=2.5, tip_length=0.18,
        )

        self.play(Create(safe_path, run_time=1.2, rate_func=smooth))

        # Label: risk as a language
        insight_lbl = Text('"Risk is a shared language across all agents."',
                           font_size=SIZE_MICRO + 2, color=GOLD,
                           font=FONT_PRIMARY, slant=ITALIC)
        insight_lbl.to_edge(DOWN, buff=0.48)
        self.play(Write(insight_lbl, run_time=0.80))
        self.wait(1.5)

        self.close()
