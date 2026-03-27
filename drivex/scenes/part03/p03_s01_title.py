# drivex/scenes/part03/p03_s01_title.py
# ─────────────────────────────────────────────────────────────────
# SCENE 3-01: Title & Context Handoff  (~25s)
# Speaker: Zhaoliang Zheng, UCLA Mobility Lab
#
# Spec: spec_part03.md → SCENE 3-01
# ─────────────────────────────────────────────────────────────────

from drivex.components.title_card import make_part_title_card
from drivex.components.colors import (
    COL_NAVY, COL_BLUE, COL_GOLD, COL_WHITE, COL_PURPLE,
    COL_GREEN, BG_DARK,
)
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")))


class P03S01Title(Scene):
    """SCENE 3-01 — Part 03 Title Card"""

    def construct(self):
        self.camera.background_color = COL_NAVY

        card = make_part_title_card(
            part_num=3,
            title="Bridging Simulation and Reality\nin Cooperative V2X Systems",
            speaker="Zhaoliang Zheng · UCLA Mobility Lab",
            callback_quote="Theory doesn't drive.",
        )
        self.play(card.build_animation())

        # Brief "Theory → Engineering" bridge visual
        self.wait(0.5)
        bridge = VGroup(
            Text("Theory", font_size=22, color=COL_PURPLE),
            Arrow(LEFT * 0.1, RIGHT * 0.1, stroke_color=COL_GOLD,
                  stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.4),
            Text("Engineering", font_size=22, color=COL_GREEN),
        ).arrange(RIGHT, buff=0.4).shift(DOWN * 0.5)
        self.play(FadeIn(bridge), run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(card, bridge)), run_time=0.5)
        self.wait(0.2)


# ─────────────────────────────────────────────────────────────────
# SCENE 3-02: Four Pillars Overview
# TODO: Implement from spec_part03.md → SCENE 3-02
# ─────────────────────────────────────────────────────────────────

class P03S02FourPillars(Scene):
    """SCENE 3-02 — [STUB] Four Pillars Overview"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 3-02\nFour Pillars Overview\n\n"
                   "Hardware → Localization → Fusion → Simulation",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


# ─────────────────────────────────────────────────────────────────
# SCENE 3-03 … 3-0N: Subsequent Part 03 scenes
# TODO: Map from spec_part03.md
# ─────────────────────────────────────────────────────────────────

class P03S03HardwareData(Scene):
    """SCENE 3-03 — [STUB] Hardware and Data Collection"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 3-03\nHardware & Data Collection\n\n"
                   "UCLA CARLA intersection setup, sensor placement",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


class P03S04Calibration(Scene):
    """SCENE 3-04 — [STUB] Sensor Calibration"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 3-04\nSensor Calibration\n\n"
                   "Extrinsic/intrinsic calibration, target board",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


class P03S05Localization(Scene):
    """SCENE 3-05 — [STUB] Map-Based Localization"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 3-05\nMap-Based Localization & Fusion\n\n"
                   "Late vs Intermediate fusion comparison",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


class P03S06DigitalTwin(Scene):
    """SCENE 3-06 — [STUB] Digital Twin"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 3-06\nDigital Twin Construction\n\n"
                   "Sim-to-real gap, CARLA environment generation",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)
