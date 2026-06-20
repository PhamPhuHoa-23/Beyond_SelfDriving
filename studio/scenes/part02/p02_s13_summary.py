"""P02-S13 - Part 2 summary."""
from manimlib import *

from studio.components import StudioScene, GOLD_RICH
from studio.scenes.part02._p02_helpers import p2_card


SCRIPT = "Three contributions, one stack: V2XPnP, TurboTrain, and RiskMap."


class P02S13Summary(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Part 2 Summary"

    def construct(self):
        self._open(self.SCENE_TITLE)
        cards = VGroup(
            p2_card("V2XPnP", "what / when / how for spatio-temporal fusion", width=5.6, stroke=GOLD_RICH),
            p2_card("TurboTrain", "make the framework trainable and efficient", width=5.6, stroke=GOLD_RICH),
            p2_card("RiskMap", "extend fusion toward interpretable planning", width=5.6, stroke=GOLD_RICH),
        ).arrange(DOWN, buff=0.35)
        cards.move_to(DOWN * 0.1)
        for card in cards:
            self.play(FadeIn(card, shift=DOWN * 0.18), run_time=0.55)
            self.wait(0.55)
        self.wait(1.2)
        self._close()
