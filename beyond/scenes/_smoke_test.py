# beyond/scenes/_smoke_test.py
# ─────────────────────────────────────────────────────────────────
# Smoke test: renders every component on one background.
# Pass = no overlap, readable text, clean end frame.
#
# Render:
#   manim -ql beyond\scenes\_smoke_test.py SmokeTest
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from manim import *
from beyond.components import (
    # Colors
    BG_SPACE, GOLD, CYAN_NEON, GREEN_SIGNAL, RED_ALERT,
    P1_FOUNDATION, P2_COOP, P4_EFFICIENT,
    TEXT_WHITE, TEXT_DIM,
    SIZE_TITLE, SIZE_BODY, SIZE_LABEL,
    FONT_PRIMARY,
    # Components
    BeyondScene,
    PiMascot, CarMascot,
    TightBubble, PIBubble, SpeechBubble,
    pipeline_block, pipeline_arrow, pipeline_row,
    node_block,
    # Animations
    scene_title_entrance, separator_line,
    bullet_reveal, key_term_reveal,
    pipeline_block_entrance, pipeline_arrow_entrance,
    glow_pulse, signal_ping,
)


class SmokeTest(BeyondScene):
    """
    Verifies all components render cleanly on dark background.
    Timeline:
      [0s]  Scene open (scan title)
      [2s]  PI + CAR mascots appear bottom corners
      [4s]  PIBubble / SpeechBubble
      [7s]  3-block pipeline with arrows
      [10s] Bullet list
      [13s] Key term reveal
      [15s] signal_ping micro effect
      [16s] glow_pulse on a node
      [17s] Scene close (fade all)
    """

    PART_COLOR = CYAN_NEON

    def construct(self):
        # ── 1. Scene open ────────────────────────────────────────
        title, sep = self.open("Component Smoke Test")
        self.wait(0.5)

        # ── 2. Mascots ───────────────────────────────────────────
        pi = PiMascot(height=1.0).to_corner(DL, buff=0.5)
        car = CarMascot(height=1.0).to_corner(DR, buff=0.5)
        self.play(
            GrowFromCenter(pi, run_time=0.5),
            GrowFromCenter(car, run_time=0.5),
        )
        self.wait(0.4)

        # ── 3. PI bubble → hold → fade, then CAR bubble ──────────
        pi_bubble = PIBubble(pi, "Why cooperate?", position=UP + RIGHT)
        self.play(FadeIn(pi_bubble, shift=DOWN * 0.08, run_time=0.4))
        self.wait(1.0)
        self.play(FadeOut(pi_bubble, run_time=0.25))
        self.wait(0.15)

        car_bubble = SpeechBubble(car, "Cooperation fills the gap!", position=UP + LEFT)
        self.play(FadeIn(car_bubble, shift=DOWN * 0.08, run_time=0.4))
        self.wait(1.0)
        self.play(FadeOut(car_bubble, run_time=0.25))
        self.wait(0.3)

        # ── 4. Pipeline row ──────────────────────────────────────
        blocks, arrows = pipeline_row(
            ["Sensor\nFusion", "BEV\nEncoder", "V2X\nAttention", "Detection"],
            buff=0.50,
            block_width=2.2,
            block_height=0.80,
            border_color=P2_COOP,
        )
        pipeline = VGroup(blocks, arrows).move_to(ORIGIN + UP * 0.8)

        self.play(
            LaggedStart(*[
                pipeline_block_entrance(b, accent_color=P2_COOP)
                for b in blocks
            ], lag_ratio=0.25),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[
                pipeline_arrow_entrance(a, style="electric")
                for a in arrows
            ], lag_ratio=0.15),
        )
        self.wait(0.6)

        # ── 5. Bullet list ───────────────────────────────────────
        items = [
            "Shared BEV representation across agents",
            "4D temporal attention for motion",
            "Multi-task: detect + predict + plan",
        ]
        bullet_grp, bullet_anim = bullet_reveal(
            items, accent_color=P1_FOUNDATION, font_size=SIZE_LABEL,
        )
        bullet_grp.to_edge(LEFT, buff=1.0).shift(DOWN * 0.6)
        self.play(bullet_anim)
        self.wait(0.8)

        # ── 6. Key term ──────────────────────────────────────────
        grp, kt_anim = key_term_reveal("V2XPnP", color=GOLD)
        grp.move_to(RIGHT * 3.2 + DOWN * 0.6)
        self.play(kt_anim)
        self.wait(0.5)

        # ── 7. Signal ping ───────────────────────────────────────
        ping_pos = car.get_center() + UP * 0.8
        self.play(signal_ping(ping_pos, color=CYAN_NEON))

        # ── 8. Glow pulse on a pipeline node ─────────────────────
        center_node = node_block("Core", radius=0.35,
                                 border_color=GOLD, fill_color="#12100A")
        center_node.move_to(RIGHT * 3.5 + UP * 1.5)
        self.play(GrowFromCenter(center_node, run_time=0.4))
        self.play(glow_pulse(center_node, color=GOLD, n_pulses=2))
        self.wait(0.5)

        # ── 9. Scene close ───────────────────────────────────────
        self.close()
