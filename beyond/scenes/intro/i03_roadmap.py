# beyond/scenes/intro/i03_roadmap.py
# ─────────────────────────────────────────────────────────────────
# I-03  BẢN ĐỒ HÀNH TRÌNH  (~30s)
#
# Orbital diagram: 5 hành tinh (P1-P5) quanh "Beyond Self-Driving"
# core ở trung tâm. Mỗi hành tinh có quỹ đạo ellipse riêng, màu riêng.
# Sau khi cả 5 nút sáng lên: lightning chain P1→P2→P3→P4→P5.
# P1 bùng sáng GOLD, camera zoom vào P1 → transition Part 1.
#
# Fix: dùng MovingCameraScene để camera.frame hoạt động đúng.
#
# Render:  manim -ql "beyond/scenes/intro/i03_roadmap.py" I03Roadmap
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import numpy as np
from manim import *
from beyond.components.colors import (
    BG_SPACE,
    GOLD, GOLD_GLOW, CYAN_NEON,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    P1_FOUNDATION, P2_COOP, P3_SIM, P4_EFFICIENT, P5_PHYSICAL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

# ── Part definitions ──────────────────────────────────────────────
PARTS = [
    {"label": "Foundation\nModels",      "color": P1_FOUNDATION,
     "pos": np.array([-3.2,  1.9, 0.0]),  "orbit": (3.9, 2.3)},
    {"label": "Cooperative\nPerception", "color": P2_COOP,
     "pos": np.array([-2.9, -1.7, 0.0]),  "orbit": (3.5, 2.1)},
    {"label": "Sim to\nReality",         "color": P3_SIM,
     "pos": np.array([ 0.0, -3.0, 0.0]),  "orbit": (3.0, 2.5)},
    {"label": "Efficiency",              "color": P4_EFFICIENT,
     "pos": np.array([ 2.9, -1.7, 0.0]),  "orbit": (3.5, 2.1)},
    {"label": "Physical AI",             "color": P5_PHYSICAL,
     "pos": np.array([ 3.2,  1.9, 0.0]),  "orbit": (3.9, 2.3)},
]


def _orbit(rx: float, ry: float, color: str) -> Ellipse:
    return Ellipse(
        width=rx * 2, height=ry * 2,
        stroke_color=color, stroke_width=0.8, stroke_opacity=0.18,
        fill_opacity=0,
    )


def _part_node(color: str, radius: float = 0.24) -> Circle:
    return Circle(
        radius=radius,
        fill_color=color, fill_opacity=1.0,
        stroke_color=WHITE, stroke_width=1.5,
    )


class I03Roadmap(MovingCameraScene):
    def setup(self):
        self.camera.background_color = BG_SPACE

    def construct(self):
        # ── Core "Beyond Self-Driving" ─────────────────────────
        core_ring  = Circle(radius=0.68,
                            fill_color="#0F1A2E", fill_opacity=1.0,
                            stroke_color=GOLD, stroke_width=2.2)
        core_glow  = Circle(radius=0.80,
                            stroke_color=GOLD, stroke_opacity=0.20,
                            stroke_width=6, fill_opacity=0)
        core_label = Text("Beyond\nSelf-Driving",
                          font_size=SIZE_MICRO + 3, color=GOLD,
                          font=FONT_PRIMARY, weight=BOLD, line_spacing=0.42)
        core_label.move_to(ORIGIN)
        core = VGroup(core_ring, core_label)

        # Pulsing core — updater that oscillates outer glow
        t_val = [0.0]
        def pulse_glow(mob, dt):
            t_val[0] += dt
            mob.set_stroke(opacity=0.12 + 0.12 * np.sin(t_val[0] * 2.5))
        core_glow.add_updater(pulse_glow)

        # ── Orbit ellipses ─────────────────────────────────────
        orbits = VGroup(*[
            _orbit(p["orbit"][0], p["orbit"][1], p["color"])
            for p in PARTS
        ])

        # ── Nodes, numbers, labels ─────────────────────────────
        nodes      = VGroup()
        num_labels = VGroup()
        txt_labels = VGroup()

        for i, p in enumerate(PARTS):
            node = _part_node(p["color"]).move_to(p["pos"])
            num  = Text(f"P{i+1}", font_size=SIZE_MICRO - 1,
                        color=WHITE, font=FONT_PRIMARY, weight=BOLD)
            num.move_to(node)

            # Label direction: push away from center
            away = p["pos"] / (np.linalg.norm(p["pos"]) + 1e-8)
            lbl  = Text(p["label"], font_size=SIZE_MICRO + 2,
                        color=p["color"], font=FONT_PRIMARY, line_spacing=0.38)
            lbl.next_to(node, direction=away, buff=0.24)

            nodes.add(node)
            num_labels.add(num)
            txt_labels.add(lbl)

        # ── ANIMATE ────────────────────────────────────────────

        # 1. Core grows
        self.play(GrowFromCenter(core_ring, run_time=0.55))
        self.play(FadeIn(core_label, run_time=0.35),
                  FadeIn(core_glow,  run_time=0.30))
        self.wait(0.25)

        # 2. Orbits draw — staggered, give depth
        self.play(
            LaggedStart(*[
                Create(o, run_time=0.75, rate_func=smooth)
                for o in orbits
            ], lag_ratio=0.10),
        )
        self.wait(0.15)

        # 3. Nodes appear with flash + label
        for i in range(len(PARTS)):
            self.play(
                Succession(
                    GrowFromCenter(nodes[i], run_time=0.22),
                    AnimationGroup(
                        Flash(nodes[i].get_center(),
                              color=PARTS[i]["color"],
                              flash_radius=0.38, num_lines=8,
                              run_time=0.28),
                        FadeIn(num_labels[i], run_time=0.15),
                        FadeIn(txt_labels[i],
                               shift=np.sign(PARTS[i]["pos"]) * 0.07,
                               run_time=0.28),
                    ),
                ),
                run_time=0.5,
            )
        self.wait(0.35)

        # 4. Lightning chain P1 → P2 → P3 → P4 → P5
        #    Each segment: glowing CubicBezier arc, then fades
        for i in range(len(PARTS) - 1):
            a = PARTS[i]["pos"]
            b = PARTS[i + 1]["pos"]
            # Slightly arced through center region
            mid_ctl = (a + b) * 0.5 + np.array([0.0, 0.4, 0.0])
            arc = CubicBezier(
                a, a + (mid_ctl - a) * 0.6,
                b + (mid_ctl - b) * 0.6, b,
                stroke_color=GOLD_GLOW, stroke_width=2.5,
                stroke_opacity=0.9,
            )
            self.play(
                Succession(
                    Create(arc, run_time=0.14, rate_func=rush_into),
                    Flash(b, color=PARTS[i+1]["color"],
                          flash_radius=0.30, num_lines=6, run_time=0.12),
                    arc.animate(run_time=0.45).set_stroke(opacity=0),
                ),
                run_time=0.72,
            )

        self.wait(0.3)

        # 5. P1 HIGHLIGHT — bùng sáng gold
        gold_ring = Circle(radius=0.24, stroke_color=GOLD,
                           stroke_width=2.8, fill_opacity=0)
        gold_ring.move_to(nodes[0])

        self.play(
            nodes[0].animate(run_time=0.40)
                    .set_fill(GOLD, 1.0).set_stroke(GOLD, width=2.5),
            num_labels[0].animate(run_time=0.40).set_color("#0A0A16"),
            txt_labels[0].animate(run_time=0.40).set_color(GOLD),
            gold_ring.animate(run_time=0.65).scale(3.0).set_stroke(opacity=0),
            Flash(nodes[0].get_center(), color=GOLD,
                  flash_radius=0.62, num_lines=12, run_time=0.45),
        )
        self.wait(0.5)

        # 6. Camera zoom toward P1 node
        core_glow.remove_updater(pulse_glow)
        p1_center = nodes[0].get_center()

        self.play(
            self.camera.frame.animate(run_time=2.0, rate_func=smooth)
                .set(width=5.8)
                .move_to(p1_center + RIGHT * 0.15 + UP * 0.08),
        )
        self.wait(0.5)

        # Fade all → transition to Part 1
        all_mobs = [core_ring, core_label, core_glow, orbits,
                    nodes, num_labels, txt_labels, gold_ring]
        self.play(
            LaggedStart(*[FadeOut(m, run_time=0.45) for m in all_mobs],
                        lag_ratio=0.05),
        )
        self.wait(0.15)
