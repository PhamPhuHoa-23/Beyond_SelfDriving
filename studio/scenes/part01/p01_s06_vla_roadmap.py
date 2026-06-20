"""P01-S06 — VLA Roadmap: 2023-2025 timeline beads + dataset chips."""
from manimlib import *
from studio.components import (
    StudioScene,
    BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER, ACCENT_PINK,
    GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    contribution_badge, write_chiseled,
)

SCRIPT = """
Since 2023, four directions: language as output, motion, guidance, and transfer.
Each forces the model to explain — and explanation is generalization.
"""

BEADS = [
    (2023.0, "Text actions", ACCENT_BLUE),
    (2023.5, "Numerical actions", ACCENT_TEAL),
    (2024.0, "Explicit guidance", ACCENT_AMBER),
    (2024.8, "Implicit transfer", ACCENT_PINK),
]

DATASETS = ["DriveLM", "CoVLA", "Impromptu VLA"]


class P01S06VLARoadmap(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "VLA Research Directions 2023-2025"

    def construct(self):
        header = self._open(self.SCENE_TITLE)

        # Timeline spine
        spine = Line(LEFT * 5.5, RIGHT * 5.5,
                     stroke_color=INK_MID, stroke_width=2)
        spine.move_to(UP * 0.2)
        self.play(ShowCreation(spine))

        # Year labels
        for yr in [2023, 2024, 2025]:
            x = (yr - 2023) / 2 * 11 - 5.5
            tick = Line(UP * 0.15, DOWN * 0.15, stroke_color=INK_MID, stroke_width=1.5)
            tick.move_to(spine.get_center() + RIGHT * x)
            lbl = Text(str(yr), font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID, weight=BOLD)
            lbl.next_to(tick, DOWN, buff=0.12)
            self.add(tick, lbl)

        # Beads drop in
        bead_y = spine.get_y() + 0.3
        for i, (yr, label, color) in enumerate(BEADS):
            x = (yr - 2023) / 2 * 11 - 5.5
            bead = Circle(radius=0.18, fill_color=color, fill_opacity=0.9, stroke_width=0)
            bead.move_to(np.array([x, bead_y, 0]))
            lbl = Text(label, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
            lbl.next_to(bead, UP, buff=0.12)
            self.play(
                GrowFromCenter(bead, run_time=0.6),
                FadeIn(lbl, shift=DOWN * 0.2, run_time=0.55),
            )
            if i < len(BEADS) - 1:
                self.wait(0.7)

        # Dataset chips drop below
        chip_group = VGroup(*(
            contribution_badge(d, color=GOLD_RICH) for d in DATASETS
        ))
        chip_group.arrange(RIGHT, buff=1.35)
        chip_group.next_to(spine, DOWN, buff=1.35)
        self.play(
            LaggedStart(
                *(FadeIn(c, shift=0.3 * UP, scale=0.96) for c in chip_group),
                lag_ratio=0.90,
                run_time=2.2
            )
        )

        # Quote
        quote = Text(
            '"Language is not only input — it\'s an interface for reasoning."',
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK,
        )
        from studio.components import place_footer
        place_footer(quote)
        self.play(write_chiseled(quote, run_time=2.0))
        self.wait(2)
        self._close()
