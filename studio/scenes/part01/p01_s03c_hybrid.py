"""P01-S03c — Hybrid: ML vs classical modules (color-coded + legend)."""
from manimlib import *
from studio.components import (
    StudioScene, PURPLE_MODEL, INK_DARK, INK_MID,
    RED_ERROR, PASTEL_BLUE, PASTEL_AMBER,
    FONT_PRIMARY, SIZE_LABEL, SIZE_BODY, SIZE_CAPS,
    pipeline_block, place_footer, CONTENT_TOP, v_arrow,
)

# name, kind, stroke, fill
MODULES = [
    ("Perception", "ml", PURPLE_MODEL, "#EDE9FE"),
    ("Localization", "classical", INK_MID, PASTEL_BLUE),
    ("Prediction", "classical", INK_MID, PASTEL_BLUE),
    ("Planning", "ml", PURPLE_MODEL, "#EDE9FE"),
    ("Control", "classical", INK_DARK, PASTEL_AMBER),
]


def _kind_tag(kind: str, stroke: str) -> VGroup:
    short = "ML" if kind == "ml" else "Cls"
    lbl = Text(short, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=stroke, weight=BOLD)
    band = Rectangle(
        width=0.16, height=0.52, fill_color=stroke, fill_opacity=1.0, stroke_width=0,
    )
    return VGroup(band, lbl).arrange(RIGHT, buff=0.1)


def _legend_row(stroke: str, fill: str, title: str, modules: str) -> VGroup:
    swatch = RoundedRectangle(
        width=0.38, height=0.38, corner_radius=0.06,
        fill_color=fill, fill_opacity=1.0,
        stroke_color=stroke, stroke_width=2.8,
    )
    title_mob = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
    sub = Text(modules, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
    text = VGroup(title_mob, sub).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
    return VGroup(swatch, text).arrange(RIGHT, buff=0.16, aligned_edge=UP)


class P01S03CHybrid(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Hybrid Systems"

    def construct(self):
        header = self._open(self.SCENE_TITLE)

        rows = VGroup()
        blocks = []
        tags = VGroup()
        for name, kind, stroke, fill in MODULES:
            block = pipeline_block(name, width=2.55, height=0.62, fill=fill, stroke=stroke)
            tag = _kind_tag(kind, stroke)
            tag.next_to(block, LEFT, buff=0.14)
            row = VGroup(tag, block)
            rows.add(row)
            blocks.append(block)
            tags.add(tag)

        stack = rows
        stack.arrange(DOWN, buff=0.24, aligned_edge=RIGHT)
        stack.next_to(header, DOWN, buff=0.55)
        if stack.get_top()[1] > CONTENT_TOP - 0.15:
            stack.shift(DOWN * (stack.get_top()[1] - (CONTENT_TOP - 0.15)))

        col_x = blocks[0][0].get_center()[0]
        stack_arrows = VGroup(*(v_arrow(a, b, x=col_x) for a, b in zip(blocks[:-1], blocks[1:])))

        legend = VGroup(
            _legend_row(PURPLE_MODEL, "#EDE9FE", "Machine learning", "Perception · Planning"),
            _legend_row(INK_MID, PASTEL_BLUE, "Classical", "Localization · Prediction"),
            _legend_row(INK_DARK, PASTEL_AMBER, "Classical", "Control (rules / MPC)"),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        legend.next_to(stack, RIGHT, buff=0.55)
        legend.align_to(stack, UP)

        self.play(LaggedStart(*(FadeIn(r) for r in rows), lag_ratio=0.1))
        self.play(ShowCreation(stack_arrows))
        self.play(FadeIn(legend))

        dim = VGroup(*[b[0] for b in blocks], stack_arrows)
        self.play(dim.animate.set_opacity(0.42))

        weakness = Text(
            "All three architectures share one weakness:\nthe long tail.",
            font=FONT_PRIMARY, font_size=SIZE_BODY, color=RED_ERROR, weight=BOLD,
        )
        place_footer(weakness)
        self.play(FadeIn(weakness))
        self.wait(2)
        self._close()
