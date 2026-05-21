# beyond/scenes/_bubble_test.py
# Render:  manim -ql "beyond/scenes/_bubble_test.py" BubbleTest

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from manim import *
from beyond.components import (
    BeyondScene,
    PiMascot, CarMascot,
    CalloutBubble, ThoughtBubble,
    PIBubble, SpeechBubble,
    CYAN_NEON, GOLD, P2_COOP, P1_FOUNDATION,
    BG_SPACE, TEXT_WHITE, TEXT_DIM,
    SIZE_LABEL, SIZE_BODY, FONT_PRIMARY,
)


class BubbleTest(BeyondScene):
    """
    Side-by-side visual test of all bubble variants.
    PI on the left, CAR on the right.
    Shows: CalloutBubble in all 4 directions + ThoughtBubble.
    """
    PART_COLOR = P2_COOP
    SHOW_AMBIENT = False  # keep frame clean for inspection

    def construct(self):
        title, sep = self.open("Bubble Style Test")
        self.wait(0.3)

        # ── Mascots ─────────────────────────────────────────────
        pi  = PiMascot(height=1.1).move_to(LEFT * 4.5 + DOWN * 0.5)
        car = CarMascot(height=1.0).move_to(RIGHT * 3.5 + DOWN * 0.5)
        self.play(GrowFromCenter(pi), GrowFromCenter(car), run_time=0.5)
        self.wait(0.3)

        # ── 1. PIBubble  UP+RIGHT ─────────────────────────────
        b1 = PIBubble(pi, "Why cooperate?", position=UP + RIGHT)
        self.play(FadeIn(b1, shift=DOWN * 0.06, run_time=0.35))
        self.wait(1.2)
        self.play(FadeOut(b1, run_time=0.22))
        self.wait(0.12)

        # ── 2. PIBubble  UP (straight above) ─────────────────
        b2 = PIBubble(pi, "Blind zone\nahead?", position=UP)
        self.play(FadeIn(b2, shift=DOWN * 0.06, run_time=0.35))
        self.wait(1.2)
        self.play(FadeOut(b2, run_time=0.22))
        self.wait(0.12)

        # ── 3. PIBubble  RIGHT ──────────────────────────────
        b3 = PIBubble(pi, "What about\nlong-tail?", position=RIGHT)
        self.play(FadeIn(b3, shift=LEFT * 0.06, run_time=0.35))
        self.wait(1.2)
        self.play(FadeOut(b3, run_time=0.22))
        self.wait(0.12)

        # ── 4. ThoughtBubble (PI thinking) ───────────────────
        b4 = ThoughtBubble(pi, "Hmm...\nmaybe V2X?",
                           position=UP + RIGHT, border_color=P1_FOUNDATION)
        self.play(b4.pop_in())
        self.wait(1.4)
        self.play(b4.pop_out())
        self.wait(0.15)

        # ── 5. SpeechBubble CAR  UP+LEFT ────────────────────
        b5 = SpeechBubble(car, "Cooperation\nfills the gap!",
                          position=UP + LEFT)
        self.play(FadeIn(b5, shift=DOWN * 0.06, run_time=0.35))
        self.wait(1.2)
        self.play(FadeOut(b5, run_time=0.22))
        self.wait(0.12)

        # ── 6. SpeechBubble CAR  RIGHT (short text) ─────────
        b6 = SpeechBubble(car, "300× faster!", position=RIGHT)
        self.play(FadeIn(b6, shift=LEFT * 0.06, run_time=0.35))
        self.wait(1.0)
        self.play(FadeOut(b6, run_time=0.22))
        self.wait(0.12)

        # ── 7. Custom CalloutBubble with GOLD border ──────────
        b7 = CalloutBubble(car, "QuantV2X\n300× smaller",
                           position=UP,
                           border_color=GOLD,
                           fill_color="#1A1200",
                           font_size=SIZE_LABEL + 2)
        self.play(b7.pop_in())
        self.wait(1.4)
        self.play(b7.pop_out())
        self.wait(0.2)

        # ── 8. Both bubbles simultaneously (show single-at-a-time rule) ─
        note = Text("One bubble per mascot at a time →",
                    font_size=SIZE_LABEL - 2, color=TEXT_DIM,
                    font=FONT_PRIMARY).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(note, shift=UP * 0.08, run_time=0.35))

        b8a = PIBubble(pi, "This is PI's bubble", position=UP + RIGHT)
        b8b = SpeechBubble(car, "CAR bubble here", position=UP + LEFT)
        self.play(FadeIn(b8a, run_time=0.3), FadeIn(b8b, run_time=0.3))
        self.wait(1.5)

        self.close()
