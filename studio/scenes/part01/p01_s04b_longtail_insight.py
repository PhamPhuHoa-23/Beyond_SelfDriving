"""P01-S04b — Long-Tail Insight: dim overlay + chiseled quote."""
from pathlib import Path

from manimlib import *
from studio.components import (
    StudioScene,
    ACCENT_BLUE, BG_CARD, GOLD_RICH, INK_DARK, INK_MID, PASTEL_AMBER,
    FONT_PRIMARY, SIZE_BODY, SIZE_LABEL, SIZE_CAPS,
    img_or_placeholder, place_footer, write_chiseled,
)

SCRIPT = """
Why do humans handle these?
Contextual reasoning, common sense, a lifetime of experience.
That's what we need to teach the long tail.
"""

ASSET_DIR = Path(__file__).resolve().parents[3] / "materials" / "images" / "part1"


def _thumbnail(filename: str) -> VGroup:
    frame = RoundedRectangle(
        width=1.75, height=0.9, corner_radius=0.08,
        fill_color=BG_CARD, fill_opacity=1.0,
        stroke_color=ACCENT_BLUE, stroke_width=1.5,
    )
    image = img_or_placeholder(ASSET_DIR / filename, width=1.55, height=0.72)
    image.move_to(frame.get_center())
    return Group(frame, image)


def _capability(label: str) -> VGroup:
    box = RoundedRectangle(
        width=3.25, height=0.62, corner_radius=0.14,
        fill_color=PASTEL_AMBER, fill_opacity=1.0,
        stroke_color=GOLD_RICH, stroke_width=2.0,
    )
    label_mob = Text(
        label, font=FONT_PRIMARY, font_size=SIZE_CAPS,
        color=INK_DARK, weight=BOLD,
    )
    label_mob.move_to(box.get_center())
    return VGroup(box, label_mob)


class P01S04BLongtailInsight(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "The Common-Sense Gap"

    def construct(self):
        self._open(self.SCENE_TITLE)

        scene_title = Text(
            "Unseen situations", font=FONT_PRIMARY, font_size=SIZE_LABEL,
            color=ACCENT_BLUE, weight=BOLD,
        )
        scenes = Group(
            _thumbnail("p1_s06_corner_cases.png"),
            _thumbnail("p1_s06_long_tail_problem_010.jpg"),
            _thumbnail("p1_s06_long_tail_problem_011.png"),
        ).arrange(DOWN, buff=0.16)
        scene_stack = Group(scene_title, scenes).arrange(DOWN, buff=0.16)
        scene_stack.move_to(LEFT * 4.75 + UP * 0.15)

        driver_frame = RoundedRectangle(
            width=3.0, height=2.25, corner_radius=0.14,
            fill_color=BG_CARD, fill_opacity=1.0,
            stroke_color=GOLD_RICH, stroke_width=2.2,
        )
        driver = img_or_placeholder(
            ASSET_DIR / "p1_s06_long_tail_problem_012.jpg",
            "Human driver",
            width=2.7,
            height=1.55,
        )
        driver.move_to(driver_frame.get_center() + UP * 0.18)
        driver_label = Text(
            "Human driver", font=FONT_PRIMARY, font_size=SIZE_LABEL,
            color=GOLD_RICH, weight=BOLD,
        )
        driver_label.next_to(driver_frame.get_bottom(), UP, buff=0.18)
        driver_card = Group(driver_frame, driver, driver_label)
        driver_card.move_to(LEFT * 1.35 + UP * 0.15)

        capability_title = Text(
            "Transferable judgment", font=FONT_PRIMARY, font_size=SIZE_LABEL,
            color=GOLD_RICH, weight=BOLD,
        )
        capabilities = VGroup(
            _capability("Contextual understanding"),
            _capability("Common-sense reasoning"),
            _capability("A lifetime of experience"),
        ).arrange(DOWN, buff=0.22)
        capability_stack = VGroup(capability_title, capabilities).arrange(DOWN, buff=0.2)
        capability_stack.move_to(RIGHT * 3.55 + UP * 0.15)

        flow_y = driver_frame.get_center()[1]
        to_driver = Arrow(
            [scenes.get_right()[0] + 0.12, flow_y, 0],
            [driver_frame.get_left()[0] - 0.12, flow_y, 0],
            thickness=3.0, fill_color=INK_MID, buff=0,
        )
        to_judgment = Arrow(
            [driver_frame.get_right()[0] + 0.12, flow_y, 0],
            [capabilities.get_left()[0] - 0.12, flow_y, 0],
            thickness=3.0, fill_color=GOLD_RICH, buff=0,
        )

        self.play(LaggedStart(*(FadeIn(item) for item in scenes), lag_ratio=0.18), FadeIn(scene_title))
        self.play(ShowCreation(to_driver), FadeIn(driver_card))
        self.play(
            ShowCreation(to_judgment),
            FadeIn(capability_title),
            LaggedStart(*(FadeIn(item, shift=LEFT * 0.12) for item in capabilities), lag_ratio=0.18),
        )

        insight = Text(
            "AVs need broad world experience, not memorized edge cases.",
            font=FONT_PRIMARY, font_size=SIZE_BODY, color=GOLD_RICH, weight=BOLD,
        )
        place_footer(insight)
        self.play(write_chiseled(insight, run_time=1.8))
        self.wait(2.0)
        self._close()
