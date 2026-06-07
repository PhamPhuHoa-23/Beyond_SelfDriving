"""P02-S06 - Related works chain."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    GOLD_RICH,
    INK_MID,
    PURPLE_MODEL,
    RED_ERROR,
    FONT_PRIMARY,
    SIZE_CAPS,
    h_arrow,
    thought_bubble,
)
from studio.scenes.part02._p02_helpers import p2_card


SCRIPT = "The field matured through V2VNet, V2X-ViT, Where2comm, and CodeFilling."


class P02S06RelatedWorks(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Related Works Chain"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py:227
        items = [
            ("V2VNet", "GNN fusion", ACCENT_TEAL, "perception only"),
            ("V2X-ViT", "attention", ACCENT_BLUE, "single frame"),
            ("Where2comm", "sparse comms", PURPLE_MODEL, "no planning"),
            ("CodeFilling", "codebook", GOLD_RICH, "no temporal stack"),
        ]
        cards = VGroup(*(
            p2_card(name, sub, width=2.28, height=1.0, stroke=color, body_size=SIZE_CAPS)
            for name, sub, color, _ in items
        ))
        cards.arrange(RIGHT, buff=0.52).move_to(UP * 0.35)
        arrows = VGroup(*(h_arrow(cards[i], cards[i + 1], color=INK_MID, thickness=2.4) for i in range(len(cards) - 1)))

        gaps = VGroup()
        for card, (_, _, _, gap) in zip(cards, items):
            label = Text(gap, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
            label.next_to(card, DOWN, buff=0.26)
            gaps.add(label)

        self.play(FadeIn(cards[0], shift=UP * 0.15))
        for i in range(1, len(cards)):
            self.play(ShowCreation(arrows[i - 1]), FadeIn(cards[i], shift=UP * 0.15), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(g) for g in gaps), lag_ratio=0.12))

        bubble_anchor = Dot().move_to(RIGHT * 4.0 + UP * 1.9).set_opacity(0)
        bubble = thought_bubble("The missing piece:\nsequence + tasks.", bubble_anchor)
        bubble.scale(0.82)
        self.play(FadeIn(bubble))

        v2xpnp = p2_card(
            "V2XPnP",
            "multi-agent x multi-frame x multi-task",
            width=4.0,
            height=1.05,
            stroke=GOLD_RICH,
            body_size=SIZE_CAPS,
        )
        v2xpnp.move_to(DOWN * 2.1)
        self.play(FadeIn(v2xpnp, shift=UP * 0.2), Flash(v2xpnp[0], color=GOLD_RICH))
        self.wait(0.9)
        self._close()
