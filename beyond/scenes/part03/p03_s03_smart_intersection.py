# beyond/scenes/part03/p03_s03_smart_intersection.py
# ─────────────────────────────────────────────────────────────────
# P3-03  UCLA SMART INTERSECTION  (~50s)
#
# Map campus UCLA, 2 nodes highlight.
# Hardware specs deploy như blueprints (B1 animation).
# Sensors bật đồng loạt: LiDAR fan, Camera triangle, Radar wave, C-V2X hex.
# Giao lộ "sống dậy" — mạng nhện điện tử.
#
# Render:  manim -ql "beyond/scenes/part03/p03_s03_smart_intersection.py" P03S03SmartIntersection
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block, pipeline_block_entrance,
    signal_ping, glow_pulse,
    P3_SIM, CYAN_NEON, ORANGE_INFRA, BLUE_ELECTRIC, GOLD,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=23)

# ── Sensor builders ────────────────────────────────────────────────

def _sensor_fan(pos, color, angle_span=PI/3, n_lines=5):
    """Camera / LiDAR fan."""
    lines = VGroup(*[
        Line(pos, pos + 1.5 * np.array([
            np.cos(-angle_span/2 + i * angle_span / (n_lines-1)),
            np.sin(-angle_span/2 + i * angle_span / (n_lines-1)),
            0
        ]), stroke_color=color, stroke_width=0.7, stroke_opacity=0.55)
        for i in range(n_lines)
    ])
    return lines

def _infra_tower(pos) -> VGroup:
    pole = Line(pos + DOWN * 0.5, pos + UP * 0.5,
                stroke_color=ORANGE_INFRA, stroke_width=2.0)
    head = RegularPolygon(n=3, radius=0.20, fill_color=ORANGE_INFRA,
                          fill_opacity=0.85, stroke_width=0)
    head.move_to(pos + UP * 0.55)
    return VGroup(pole, head)


class P03S03SmartIntersection(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("UCLA Smart Intersection — Real V2X Testbed")
        self.wait(0.2)

        # ── Simple road map ───────────────────────────────────
        # Horizontal road
        h_road = Rectangle(width=13.0, height=0.8,
                           fill_color="#060E18", fill_opacity=1.0,
                           stroke_color="#0D1829", stroke_width=1.0)
        h_road.move_to(DOWN * 0.2)
        # Vertical road
        v_road = Rectangle(width=0.8, height=7.0,
                           fill_color="#060E18", fill_opacity=1.0,
                           stroke_color="#0D1829", stroke_width=1.0)
        v_road.move_to(LEFT * 0.5 + DOWN * 0.2)

        # Road markings
        for x in np.linspace(-6, 5, 12):
            if abs(x - (-0.5)) > 0.6:
                dash = Rectangle(width=0.45, height=0.08,
                                 fill_color=TEXT_GHOST, fill_opacity=0.4, stroke_width=0)
                dash.move_to([x, -0.2, 0])
                h_road.add(dash)

        self.play(FadeIn(h_road, run_time=0.40), FadeIn(v_road, run_time=0.35))

        # ── 2 Infrastructure nodes ────────────────────────────
        nw_pos = np.array([-3.8, 1.8, 0])
        se_pos = np.array([ 3.0, -1.8, 0])

        nw_tower = _infra_tower(nw_pos)
        se_tower = _infra_tower(se_pos)
        nw_lbl = Text("NW Node", font_size=SIZE_MICRO, color=ORANGE_INFRA,
                      font=FONT_PRIMARY)
        nw_lbl.next_to(nw_tower, UP, buff=0.12)
        se_lbl = Text("SE Node", font_size=SIZE_MICRO, color=ORANGE_INFRA,
                      font=FONT_PRIMARY)
        se_lbl.next_to(se_tower, DOWN, buff=0.12)

        self.play(
            GrowFromCenter(nw_tower, run_time=0.35),
            GrowFromCenter(se_tower, run_time=0.35),
            FadeIn(nw_lbl, run_time=0.22),
            FadeIn(se_lbl, run_time=0.22),
        )

        # Intersection label
        intersection_lbl = Text("UCLA Campus — 2 Smart Intersections",
                                font_size=SIZE_MICRO + 2, color=P3_SIM,
                                font=FONT_PRIMARY)
        intersection_lbl.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(intersection_lbl, shift=UP * 0.06, run_time=0.28))
        self.wait(0.3)

        # ── Hardware specs deploy ─────────────────────────────
        hw_data = [
            ("LiDAR 128L", CYAN_NEON,    nw_pos + LEFT * 1.5 + UP * 0.5),
            ("Camera ×2",  P3_SIM,       nw_pos + RIGHT * 1.5 + UP * 0.5),
            ("Radar",      BLUE_ELECTRIC, nw_pos + LEFT * 1.5 + DOWN * 0.5),
            ("C-V2X Unit", ORANGE_INFRA,  se_pos + RIGHT * 1.5 + UP * 0.5),
        ]

        hw_blocks = VGroup()
        conn_lines = VGroup()
        for name, color, pos in hw_data:
            blk = pipeline_block(name, width=1.6, height=0.52,
                                 border_color=color, fill_color=BG_PANEL,
                                 font_size=SIZE_MICRO)
            blk.move_to(pos)
            hw_blocks.add(blk)

        self.play(
            LaggedStart(*[pipeline_block_entrance(b, hw_data[i][1])
                          for i, b in enumerate(hw_blocks)], lag_ratio=0.18),
        )
        self.wait(0.4)

        # ── ALL SENSORS ACTIVATE ──────────────────────────────
        # LiDAR scan fan from NW
        lidar_fan = _sensor_fan(nw_pos, CYAN_NEON, angle_span=PI*0.7, n_lines=7)
        # Camera cone from SE
        cam_fan = _sensor_fan(se_pos, P3_SIM, angle_span=PI*0.4, n_lines=5)
        # Radar waves
        self.play(
            LaggedStart(*[Create(l, run_time=0.12) for l in lidar_fan],
                        lag_ratio=0.04),
            LaggedStart(*[Create(l, run_time=0.10) for l in cam_fan],
                        lag_ratio=0.03),
        )

        # V2X packet from NW to SE
        v2x_path = Line(nw_pos, se_pos)
        v2x_pkt = RegularPolygon(n=6, radius=0.07, color=ORANGE_INFRA,
                                  fill_opacity=0.9, stroke_width=0)
        v2x_pkt.move_to(nw_pos)
        self.play(
            MoveAlongPath(v2x_pkt, v2x_path, run_time=0.55, rate_func=smooth),
        )
        self.play(
            Flash(se_pos, color=ORANGE_INFRA, flash_radius=0.40,
                  num_lines=6, run_time=0.25),
            FadeOut(v2x_pkt, run_time=0.08),
        )

        # Signal pings from both nodes
        self.play(
            AnimationGroup(
                signal_ping(nw_pos, CYAN_NEON),
                signal_ping(se_pos, ORANGE_INFRA),
            ),
        )
        self.wait(1.0)

        self.close()
