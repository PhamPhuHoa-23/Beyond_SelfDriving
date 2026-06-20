"""P01-S04a — Long-Tail Problem: axes first, footer without hero overlap."""
from pathlib import Path

from manimlib import *
from studio.components import (
    StudioScene, RED_ERROR, GOLD_RICH, ACCENT_BLUE, BG_CARD, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL,
    axes_deploy, chart_mount, curve_trace, img_or_placeholder, place_footer,
)

SCRIPT = """
Self-driving fails most where it's seen least.
Just one percent of scenarios cause virtually all fatal accidents.
"""

ASSET_DIR = Path(__file__).resolve().parents[3] / "materials" / "images" / "part1"


def _photo_card(filename: str, label: str) -> VGroup:
    frame = RoundedRectangle(
        width=3.05, height=2.18, corner_radius=0.12,
        fill_color=BG_CARD, fill_opacity=0.75,
        stroke_color=ACCENT_BLUE, stroke_width=2.0,
    )
    image = img_or_placeholder(
        ASSET_DIR / filename,
        label,
        width=2.72,
        height=1.55,
    )
    image.move_to(frame.get_center() + UP * 0.18)
    caption = Text(
        label, font=FONT_PRIMARY, font_size=SIZE_LABEL,
        color=INK_DARK, weight=BOLD,
    )
    caption.next_to(frame.get_bottom(), UP, buff=0.18)
    return Group(frame, image, caption)


def ease_out_back(t: float) -> float:
    s = 1.70158
    t = t - 1
    return t * t * ((s + 1) * t + s) + 1


class P01S04ALongtailProblem(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "The Long-Tail Problem"

    def construct(self):
        self._open(self.SCENE_TITLE)

        photo_row = Group(
            _photo_card("p1_s06_corner_cases.png", "Person in active lane"),
            _photo_card("p1_s06_long_tail_problem_010.jpg", "Traffic lights on truck"),
            _photo_card("p1_s06_long_tail_problem_011.png", "Snow-covered road"),
        ).arrange(RIGHT, buff=0.38)
        photo_row.move_to(UP * 0.85)
        # Slower entry cascade with ease_out_back overshoot/bounce settle (more spaced out)
        self.play(
            LaggedStart(
                *(FadeIn(card, shift=0.35 * UP, scale=0.92, rate_func=ease_out_back) for card in photo_row),
                lag_ratio=0.95,
                run_time=4.5
            )
        )
        self.wait(1.5)

        axes, axes_anim = axes_deploy(
            (0, 5, 1), (0, 1.0, 0.2),
            width=7.2, height=3.8, with_tick_labels=False,
        )
        tick_labels = chart_mount(
            axes, UP * 0.1 + LEFT * 0.35, scale=0.86,
            x_label="Rarity", y_label="Accident rate",
        )
        self.play(axes_anim, FadeOut(photo_row), FadeIn(tick_labels))

        self.play(curve_trace(axes, lambda x: 0.9 * np.exp(-x), color=ACCENT_BLUE, run_time=1.5))

        head_pt0, head_pt1 = axes.c2p(0, 0), axes.c2p(2.5, 0.75)
        tail_pt0, tail_pt1 = axes.c2p(2.5, 0), axes.c2p(5, 0.25)
        head_fill = Rectangle(
            width=abs(head_pt1[0] - head_pt0[0]),
            height=abs(head_pt1[1] - head_pt0[1]),
            fill_color=ACCENT_BLUE, fill_opacity=0.12, stroke_width=0,
        ).move_to((head_pt0 + head_pt1) / 2)
        tail_fill = Rectangle(
            width=abs(tail_pt1[0] - tail_pt0[0]),
            height=abs(tail_pt1[1] - tail_pt0[1]),
            fill_color=RED_ERROR, fill_opacity=0.22, stroke_width=0,
        ).move_to((tail_pt0 + tail_pt1) / 2)
        head_lbl = Text("99% driving", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_BLUE)
        head_lbl.move_to(axes.c2p(1.2, 0.62))
        tail_lbl = Text("1% scenarios", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR)
        tail_lbl.move_to(axes.c2p(3.8, 0.28))
        self.play(FadeIn(head_fill), FadeIn(tail_fill), FadeIn(head_lbl), FadeIn(tail_lbl))

        footer = Text(
            "1% of scenarios account for 100% of fatal accidents",
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD,
        )
        place_footer(footer)
        self.play(FadeIn(footer))
        self.wait(2.5)
        self._close()
