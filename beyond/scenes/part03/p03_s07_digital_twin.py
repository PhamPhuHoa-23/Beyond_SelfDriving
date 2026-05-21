# beyond/scenes/part03/p03_s07_digital_twin.py
# ─────────────────────────────────────────────────────────────────
# P3-07  DIGITAL TWIN  (~55s)
#
# Scan line quét qua cảnh thực → chuyển hóa thành digital twin.
# Twin live: khi xe real di chuyển, twin đồng bộ.
#
# Render:  manim -ql "beyond/scenes/part03/p03_s07_digital_twin.py" P03S07DigitalTwin
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, glow_pulse,
    P3_SIM, CYAN_NEON, GOLD, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, BG_PANEL,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=11)

# ── Element helpers ────────────────────────────────────────────────

def _real_element(pos, color="#6B7A99", size=0.5):
    """Rough/noisy element for real world."""
    angle = float(RNG.uniform(-0.2, 0.2))
    rect = Rectangle(width=size*float(RNG.uniform(0.8, 1.4)),
                     height=size*float(RNG.uniform(0.5, 1.0)),
                     fill_color=color, fill_opacity=0.65,
                     stroke_color=TEXT_DIM, stroke_width=0.8)
    rect.rotate(angle).move_to(pos)
    return rect

def _digital_element(pos, size=0.5):
    """Clean teal grid element for digital world."""
    rect = Rectangle(width=size*0.9, height=size*0.65,
                     fill_color="#071828", fill_opacity=0.9,
                     stroke_color=P3_SIM, stroke_width=1.5)
    rect.move_to(pos)
    return rect


class P03S07DigitalTwin(BeyondScene):
    PART_COLOR = P3_SIM

    def construct(self):
        title_mob, sep = self.open("Digital Twin — Reality Cloned in Real-Time")
        self.wait(0.2)

        # ── Left: REAL world ──────────────────────────────────
        real_label = Text("Real World", font_size=SIZE_LABEL - 1,
                          color=TEXT_DIM, font=FONT_PRIMARY, weight=BOLD)
        real_label.move_to(LEFT * 3.5 + UP * 2.5)
        self.play(FadeIn(real_label, shift=DOWN * 0.06, run_time=0.28))

        real_positions = [
            LEFT * 4.0 + UP * 1.2,
            LEFT * 2.5 + UP * 0.5,
            LEFT * 4.2 + DOWN * 0.8,
            LEFT * 2.8 + DOWN * 1.5,
        ]
        real_elements = VGroup(*[_real_element(p) for p in real_positions])
        self.play(
            LaggedStart(*[GrowFromCenter(e, run_time=0.28) for e in real_elements],
                        lag_ratio=0.12),
        )

        # Real car
        real_car = Rectangle(width=0.75, height=0.40,
                             fill_color="#6B7A99", fill_opacity=0.85,
                             stroke_color=TEXT_DIM, stroke_width=1.0)
        real_car.move_to(LEFT * 3.2 + DOWN * 0.0)
        self.play(GrowFromCenter(real_car, run_time=0.28))
        self.wait(0.3)

        # ── SCAN LINE sweeps left→right ───────────────────────
        scan = Line(
            LEFT * 5.5 + UP * 2.8,
            LEFT * 5.5 + UP * 2.8,
            stroke_color=CYAN_NEON, stroke_width=2.8, stroke_opacity=0.90,
        )
        scan.put_start_and_end_on(
            LEFT * 5.5 + UP * 2.8, LEFT * 5.5 + DOWN * 2.8
        )

        # Right side: digital elements appear BEHIND scan
        digital_label = Text("Digital Twin", font_size=SIZE_LABEL - 1,
                             color=P3_SIM, font=FONT_PRIMARY, weight=BOLD)
        digital_label.move_to(RIGHT * 3.5 + UP * 2.5)

        digital_elements = VGroup(*[
            _digital_element(p + RIGHT * 7.0)
            for p in real_positions
        ])
        twin_car = Rectangle(width=0.75, height=0.40,
                             fill_color="#071828", fill_opacity=1.0,
                             stroke_color=P3_SIM, stroke_width=1.8)
        twin_car.move_to(RIGHT * 4.2 + DOWN * 0.0)

        # Hide digital elements initially
        for e in digital_elements:
            e.set_opacity(0)
        twin_car.set_opacity(0)
        digital_label.set_opacity(0)

        self.add(scan, digital_elements, twin_car, digital_label)

        # Sweep scan from left to right, revealing digital elements
        self.play(
            scan.animate(run_time=1.8, rate_func=smooth)
                .shift(RIGHT * 12.0),
            LaggedStart(*[
                e.animate(run_time=0.5).set_opacity(1.0)
                for e in list(digital_elements) + [twin_car, digital_label]
            ], lag_ratio=0.20),
        )
        self.remove(scan)
        self.wait(0.3)

        # ── LIVE SYNC: real car moves, twin follows ────────────
        sync_lbl = Text("Live sync  ·  0.1s lag",
                        font_size=SIZE_MICRO + 2, color=GREEN_SIGNAL,
                        font=FONT_PRIMARY)
        sync_lbl.to_edge(DOWN, buff=0.52)
        self.play(FadeIn(sync_lbl, shift=UP * 0.06, run_time=0.30))

        # Real car moves, twin follows with slight delay
        self.play(
            real_car.animate(run_time=0.8, rate_func=smooth).shift(RIGHT * 0.9),
        )
        self.play(
            twin_car.animate(run_time=0.55, rate_func=smooth).shift(RIGHT * 0.9),
        )
        self.play(glow_pulse(twin_car, P3_SIM, n_pulses=1, run_time=0.35))
        self.wait(0.4)

        # OpenCDA label
        cda_lbl = Text("OpenCDA → Real-time Digital Twin", font_size=SIZE_LABEL - 2,
                       color=GOLD, font=FONT_PRIMARY, weight=BOLD)
        cda_lbl.move_to(DOWN * 0.2)
        self.play(FadeIn(cda_lbl, shift=UP * 0.08, run_time=0.35))
        self.wait(1.5)

        self.close()
