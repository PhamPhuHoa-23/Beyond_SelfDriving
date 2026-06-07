"""P01-S04a — Long-Tail Problem: axes first, footer without hero overlap."""
from manimlib import *
from studio.components import (
    StudioScene, RED_ERROR, GOLD_RICH, ACCENT_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL,
    axes_deploy, chart_mount, curve_trace, failure_icon, place_footer, CONTENT_TOP,
)

SCRIPT = """
Self-driving fails most where it's seen least.
Just one percent of scenarios cause virtually all fatal accidents.
"""


class P01S04ALongtailProblem(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "The Long-Tail Problem"

    def construct(self):
        self._open(self.SCENE_TITLE)

        icons = VGroup(
            failure_icon(kind="phone_pedestrian"),
            failure_icon(kind="inverted_lights"),
            failure_icon(kind="snow_lane"),
        )
        labels = ["Phone in road", "Inverted lights", "Snow-covered lane"]
        icon_group = VGroup()
        for icon, lbl in zip(icons, labels):
            icon.scale(1.15)
            lbl_mob = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
            lbl_mob.next_to(icon, DOWN, buff=0.12)
            icon_group.add(VGroup(icon, lbl_mob))
        icon_group.arrange(RIGHT, buff=1.0)
        icon_group.move_to(UP * 1.85)
        if icon_group.get_top()[1] > CONTENT_TOP - 0.25:
            icon_group.shift(DOWN * (icon_group.get_top()[1] - (CONTENT_TOP - 0.25)))
        self.play(LaggedStart(*(FadeIn(ig, scale=0.8) for ig in icon_group), lag_ratio=0.2))
        self.wait(0.4)

        axes, axes_anim = axes_deploy(
            (0, 5, 1), (0, 1.0, 0.2),
            width=7.2, height=3.8, with_tick_labels=False,
        )
        tick_labels = chart_mount(
            axes, UP * 0.1 + LEFT * 0.35, scale=0.86,
            x_label="Rarity", y_label="Accident rate",
        )
        self.play(axes_anim, FadeOut(icon_group), FadeIn(tick_labels))

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
