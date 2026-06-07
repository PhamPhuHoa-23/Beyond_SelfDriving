"""P01-S02a — GenAI Boom Timeline: 2020-2025 beads, non-overlapping labels."""
from manimlib import *
from studio.components import (
    StudioScene,
    ACCENT_BLUE, GOLD_RICH, INK_DARK, INK_MID,
    PURPLE_MODEL,
    FONT_PRIMARY, SIZE_CAPS,
    place_footer,
)

SCRIPT = """
Since 2023, generative AI has done what felt impossible.
So a natural question: why not driving?
"""

# (year, label, bead_size, color)
EVENTS = [
    (2020.5, "GPT-3", 0.18, INK_MID),
    (2021.5, "CLIP", 0.22, ACCENT_BLUE),
    (2022.9, "ChatGPT", 0.38, GOLD_RICH),
    (2023.5, "GPT-4", 0.48, GOLD_RICH),
    (2024.0, "Gemini", 0.35, ACCENT_BLUE),
    (2024.6, "LLaMA 3", 0.30, PURPLE_MODEL),
    (2025.0, "GPT-4o+", 0.28, ACCENT_BLUE),
]

AXIS_LEFT = -6.3
AXIS_RIGHT = 6.3


def timeline_x(year: float) -> float:
    return AXIS_LEFT + (year - 2020) / 5 * (AXIS_RIGHT - AXIS_LEFT)


class P01S02AGenAITimeline(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "The GenAI Boom"

    def construct(self):
        header = self._open(self.SCENE_TITLE)

        axis_y = -1.15
        axis = Line([AXIS_LEFT, 0, 0], [AXIS_RIGHT, 0, 0], stroke_color=INK_MID, stroke_width=2)
        axis.move_to([0, axis_y, 0])
        self.play(ShowCreation(axis, run_time=1.0))

        years = VGroup()
        for yr in range(2020, 2026):
            x = timeline_x(yr)
            tick = Line(UP * 0.12, DOWN * 0.12, stroke_color=INK_MID, stroke_width=1.5)
            tick.move_to([x, axis_y, 0])
            lbl = Text(str(yr), font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID, weight=BOLD)
            lbl.next_to(tick, DOWN, buff=0.12)
            years.add(VGroup(tick, lbl))
        self.play(LaggedStart(*(FadeIn(y) for y in years), lag_ratio=0.1))

        bead_mobs = []
        label_y = axis_y + 0.95
        for yr, label, size, color in EVENTS:
            x = timeline_x(yr)
            r = 0.1 + size * 0.5
            bead = Circle(radius=r, fill_color=color, fill_opacity=0.92, stroke_width=0)
            bead_y = axis_y + r + 0.06
            bead.move_to([x, bead_y + 2.5, 0])

            fs = SIZE_CAPS if yr < 2024.0 else SIZE_CAPS - 4
            lbl = Text(label, font=FONT_PRIMARY, font_size=fs, color=color, weight=BOLD)
            lbl.move_to([x, label_y, 0])
            bead_mobs.append((bead, lbl, np.array([x, bead_y, 0])))

        for bead, lbl, final_pos in bead_mobs:
            self.play(
                bead.animate(run_time=0.45, rate_func=rush_into).move_to(final_pos),
                FadeIn(lbl, shift=DOWN * 0.2, run_time=0.35),
            )

        question = Text(
            '"Why, in 2025, can AI write code, draw art, answer anything\n'
            '— yet self-driving cars still struggle?"',
            font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD,
        )
        place_footer(question)
        question.shift(UP * 0.18)
        self.play(FadeIn(question, shift=UP * 0.2, run_time=0.8))
        self.wait(2)
        self._close()
