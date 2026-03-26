# drivex/scenes/part02/p02_s01_title.py
# ─────────────────────────────────────────────────────────────────
# SCENE 2-01: Title & Handoff from Part 01  (~25s)
# Speaker: Zewei Zhou, UCLA Mobility Lab
#
# Spec: spec_part02.md → SCENE 2-01
# ─────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from manim import *
from drivex.components.colors import COL_NAVY, BG_DARK
from drivex.components.title_card import make_part_title_card


class P02S01Title(Scene):
    """SCENE 2-01 — Part 02 Title Card"""

    def construct(self):
        self.camera.background_color = COL_NAVY

        card = make_part_title_card(
            part_num=2,
            title="Towards End-to-End\nCooperative Automation",
            speaker="Zewei Zhou · UCLA Mobility Lab",
            callback_quote="A single agent is still limited by its own field of view.",
        )

        self.play(card.build_animation())
        self.wait(2.0)
        self.play(FadeOut(card), run_time=0.5)
        self.wait(0.2)


# ─────────────────────────────────────────────────────────────────
# SCENE 2-02: Background — Why This Problem Matters
# TODO: Implement from spec_part02.md → SCENE 2-02
# ─────────────────────────────────────────────────────────────────

class P02S02Background(Scene):
    """SCENE 2-02 — [STUB] Background: Why This Problem Matters"""

    def construct(self):
        self.camera.background_color = "#0A0A0A"
        lbl = Text("STUB: Scene 2-02\nBackground — Why This Problem Matters\n\n"
                   "Implement from spec_part02.md → SCENE 2-02",
                   font_size=22, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


# ─────────────────────────────────────────────────────────────────
# SCENE 2-03: Single-Agent Evolution: Modular → End-to-End
# TODO: Implement from spec_part02.md → SCENE 2-03
# ─────────────────────────────────────────────────────────────────

class P02S03Evolution(Scene):
    """SCENE 2-03 — [STUB] Single-Agent Evolution"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 2-03\nSingle-Agent Evolution: Modular → End-to-End\n\n"
                   "Timeline: PnPNet → GameFormer → UniAD → DiffusionDrive",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


# ─────────────────────────────────────────────────────────────────
# SCENE 2-04: The Physics Limit — Occlusion
# TODO: Implement from spec_part02.md → SCENE 2-04
# ─────────────────────────────────────────────────────────────────

class P02S04Occlusion(Scene):
    """SCENE 2-04 — [STUB] Physics Limit: Occlusion"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 2-04\nThe Physics Limit: Occlusion\n\n"
                   "Single-agent blind zones vs multi-agent coverage",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)


# ─────────────────────────────────────────────────────────────────
# SCENE 2-05: Related Works & Research Gaps
# TODO: Implement from spec_part02.md → SCENE 2-05
# ─────────────────────────────────────────────────────────────────

class P02S05RelatedWorks(Scene):
    """SCENE 2-05 — [STUB] Related Works & Research Gaps"""

    def construct(self):
        self.camera.background_color = "#0F172A"
        lbl = Text("STUB: Scene 2-05\nRelated Works & Research Gaps\n\n"
                   "V2VNet, V2X-ViT, Where2comm, CodeFilling timeline",
                   font_size=20, color=WHITE).center()
        self.add(lbl)
        self.wait(2)
