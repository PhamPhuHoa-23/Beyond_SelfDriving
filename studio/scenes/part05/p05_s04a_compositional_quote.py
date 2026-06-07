"""P05-S04a Stuart Geman quote — letters fly from random positions."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_TITLECARD, GOLD_RICH, INK_LIGHT,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL, SIZE_CAPS,
    write_chiseled,
)
SCRIPT = """The world is compositional, or there is a god — Stuart Geman."""


class P05S04ACompositionalQuote(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "A Fundamental Insight"

    def construct(self):
        self.camera.background_color = BG_TITLECARD
        # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/opening_quote.py:8
        quote1 = Text('"The world is compositional,', font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH)
        quote2 = Text('or there is a god."', font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH)
        attribution = Text("— Stuart Geman", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_LIGHT)
        q_group = VGroup(quote1, quote2).arrange(DOWN, buff=0.22)
        q_group.move_to(ORIGIN + UP * 0.3)
        attribution.next_to(q_group, DOWN, buff=0.35)
        # Force color on submobjects before save_state so Restore() keeps the correct color
        for mob in [quote1, quote2]:
            mob.set_color(GOLD_RICH)
            for sub in mob.family_members_with_points():
                sub.set_color(GOLD_RICH)
        # Letters scatter from random then fly to position
        rng = np.random.RandomState(42)
        char_mobs = VGroup(*quote1, *quote2)
        for m in char_mobs:
            m.save_state()
            m.move_to(np.array([rng.uniform(-6, 6), rng.uniform(-3.5, 3.5), 0]))
            m.set_opacity(0)
        self.play(LaggedStart(*(Restore(m, run_time=1.2) for m in char_mobs), lag_ratio=0.02, run_time=2.5))
        self.play(FadeIn(attribution))
        self.wait(3)
        self._close()
