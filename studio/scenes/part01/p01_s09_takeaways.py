"""P01-S09 — Part 1 Takeaways: 4 bullet cards."""
from manimlib import *
from studio.components import (
    StudioScene,
    BG_PAPER, ACCENT_BLUE, GOLD_RICH, GREEN_FIX, RED_ERROR, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_BODY, SIZE_LABEL,
    contribution_badge, text,
)

SCRIPT = """
Four takeaways: foundation models open the long tail;
multi-modal LLMs are the leading architecture;
there's no dominant paradigm yet;
and safety, latency, data — still hard.
"""

TAKEAWAYS = [
    ("Foundation models open the long tail", ACCENT_BLUE),
    ("MLLMs: scalable, reasoning-first architectures", GOLD_RICH),
    ("No dominant paradigm — active research", GREEN_FIX),
    ("Safety / latency / data: still hard", RED_ERROR),
]


class P01S09Takeaways(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Part 1 Takeaways"

    def construct(self):
        header = self._open(self.SCENE_TITLE)

        cards = VGroup()
        for i, (msg, color) in enumerate(TAKEAWAYS):
            t = Text(msg, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
            num = Text(str(i + 1), font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=color, weight=BOLD)
            bg = RoundedRectangle(
                width=t.get_width() + 0.9, height=t.get_height() + 0.25,
                corner_radius=0.12,
                fill_color=BG_PAPER, fill_opacity=1.0,
                stroke_color=color, stroke_width=1.8,
            )
            t.move_to(bg)
            num.next_to(bg, LEFT, buff=0.12)
            cards.add(VGroup(num, bg, t))

        cards.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        cards.move_to(ORIGIN + UP * 0.2)

        self.play(LaggedStart(*(FadeIn(c, shift=RIGHT * 0.2) for c in cards), lag_ratio=0.25))
        self.wait(2)
        self._close()


from studio.components.colors import BG_PAPER  # noqa: E402 (already in __init__ but for clarity)
