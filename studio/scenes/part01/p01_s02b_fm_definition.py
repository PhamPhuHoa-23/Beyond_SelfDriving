"""P01-S02b - Foundation Model Definition."""
from manimlib import *
from studio.components import (
    StudioScene, INK_DARK, INK_MID, PURPLE_MODEL, GREEN_FIX, BG_CARD,
    ACCENT_BLUE, CYAN_RADAR, GOLD_RICH, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    place_footer,
)

SOURCES = [
    ("Text", "Aa", ACCENT_BLUE),
    ("Images", "IMG", CYAN_RADAR),
    ("Speech", ")))", PURPLE_MODEL),
    ("3D signals", "XYZ", GOLD_RICH),
]
TASKS = [
    ("Information extraction", GREEN_FIX),
    ("Object recognition", ORANGE),
    ("Instruction following", ACCENT_BLUE),
    ("Question answering", PURPLE_MODEL),
]


def labeled_chip(label, glyph, color, width=2.45):
    box = RoundedRectangle(
        width=width, height=0.56, corner_radius=0.14,
        fill_color=color, fill_opacity=0.13,
        stroke_color=color, stroke_width=1.7,
    )
    icon = Text(glyph, font=FONT_PRIMARY, font_size=SIZE_CAPS - 3, color=color)
    icon.move_to(box.get_left() + RIGHT * 0.4)
    text = Text(
        label, font=FONT_PRIMARY, font_size=SIZE_CAPS - 1,
        color=INK_DARK,
    )
    text.next_to(icon, RIGHT, buff=0.2)
    return VGroup(box, icon, text)


def task_chip(label, color, width=2.7):
    box = RoundedRectangle(
        width=width, height=0.56, corner_radius=0.14,
        fill_color=color, fill_opacity=0.12,
        stroke_color=color, stroke_width=1.7,
    )
    dot = Circle(radius=0.075, fill_color=color, fill_opacity=1, stroke_width=0)
    dot.move_to(box.get_left() + RIGHT * 0.27)
    text = Text(
        label, font=FONT_PRIMARY, font_size=SIZE_CAPS - 3,
        color=INK_DARK,
    )
    text.next_to(dot, RIGHT, buff=0.16)
    return VGroup(box, dot, text)


def representation_network():
    positions = [
        LEFT * 0.75 + UP * 0.5,
        LEFT * 0.15 + UP * 0.82,
        RIGHT * 0.58 + UP * 0.48,
        LEFT * 0.62 + DOWN * 0.25,
        RIGHT * 0.1 + DOWN * 0.05,
        RIGHT * 0.7 + DOWN * 0.42,
        LEFT * 0.05 + DOWN * 0.72,
    ]
    links = [(0, 1), (0, 3), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5),
             (3, 4), (3, 6), (4, 5), (4, 6), (5, 6)]
    edges = VGroup(*[
        Line(positions[a], positions[b], stroke_color=PURPLE_MODEL,
             stroke_width=1.7, stroke_opacity=0.6)
        for a, b in links
    ])
    nodes = VGroup(*[
        Circle(
            radius=0.105, fill_color=PURPLE_MODEL, fill_opacity=1,
            stroke_color=INK_DARK, stroke_width=1.1,
        ).move_to(pos)
        for pos in positions
    ])
    return VGroup(edges, nodes)


class P01S02BFMDefinition(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "What Is a Foundation Model?"

    def construct(self):
        self._open(self.SCENE_TITLE)

        left_panel = RoundedRectangle(
            width=3.05, height=3.75, corner_radius=0.2,
            fill_color=BG_CARD, fill_opacity=0.62,
            stroke_color=ACCENT_BLUE, stroke_width=2,
        )
        left_panel.move_to(LEFT * 4.65 + DOWN * 0.08)
        left_title = Text(
            "BROAD DATA", font=FONT_PRIMARY, font_size=SIZE_LABEL - 1,
            color=ACCENT_BLUE,
        )
        left_title.next_to(left_panel.get_top(), DOWN, buff=0.18)
        sources = VGroup(*[labeled_chip(*spec) for spec in SOURCES])
        sources.arrange(DOWN, buff=0.22).move_to(left_panel.get_center() + DOWN * 0.16)

        model_panel = RoundedRectangle(
            width=3.15, height=3.25, corner_radius=0.28,
            fill_color=PURPLE_MODEL, fill_opacity=0.1,
            stroke_color=PURPLE_MODEL, stroke_width=2.6,
        )
        model_panel.move_to(DOWN * 0.08)
        model_title = Text(
            "FOUNDATION MODEL", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2,
            color=PURPLE_MODEL,
        )
        model_title.set_max_width(model_panel.get_width() - 0.42)
        model_title.next_to(model_panel.get_top(), DOWN, buff=0.22)
        network = representation_network()
        network.move_to(model_panel.get_center() + DOWN * 0.12)
        model_note = Text(
            "shared representation", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2,
            color=INK_MID,
        )
        model_note.next_to(model_panel.get_bottom(), UP, buff=0.2)

        right_panel = RoundedRectangle(
            width=3.3, height=3.75, corner_radius=0.2,
            fill_color=BG_CARD, fill_opacity=0.62,
            stroke_color=GREEN_FIX, stroke_width=2,
        )
        right_panel.move_to(RIGHT * 4.65 + DOWN * 0.08)
        right_title = Text(
            "MANY TASKS", font=FONT_PRIMARY, font_size=SIZE_LABEL - 1,
            color=GREEN_FIX,
        )
        right_title.next_to(right_panel.get_top(), DOWN, buff=0.18)
        tasks = VGroup(*[task_chip(*spec) for spec in TASKS])
        tasks.arrange(DOWN, buff=0.22).move_to(right_panel.get_center() + DOWN * 0.16)

        flow_y = model_panel.get_center()[1]
        train_arrow = Arrow(
            [left_panel.get_right()[0] + 0.08, flow_y, 0],
            [model_panel.get_left()[0] - 0.08, flow_y, 0],
            thickness=3, fill_color=ACCENT_BLUE, buff=0,
        )
        adapt_arrow = Arrow(
            [model_panel.get_right()[0] + 0.08, flow_y, 0],
            [right_panel.get_left()[0] - 0.08, flow_y, 0],
            thickness=3, fill_color=GREEN_FIX, buff=0,
        )
        train_label = Text(
            "PRE-TRAIN", font=FONT_PRIMARY, font_size=SIZE_CAPS - 3,
            color=ACCENT_BLUE,
        )
        train_label.next_to(train_arrow, UP, buff=0.12)
        adapt_label = Text(
            "ADAPT", font=FONT_PRIMARY, font_size=SIZE_CAPS - 3,
            color=GREEN_FIX,
        )
        adapt_label.next_to(adapt_arrow, UP, buff=0.12)

        self.play(FadeIn(left_panel), FadeIn(left_title))
        self.play(LaggedStart(*(FadeIn(s, shift=RIGHT * 0.12) for s in sources), lag_ratio=0.12))
        self.play(ShowCreation(train_arrow), FadeIn(train_label))
        self.play(FadeIn(model_panel), FadeIn(model_title))
        self.play(
            ShowCreation(network[0]),
            LaggedStart(*(GrowFromCenter(n) for n in network[1]), lag_ratio=0.08),
        )
        self.play(FadeIn(model_note))
        self.play(ShowCreation(adapt_arrow), FadeIn(adapt_label))
        self.play(FadeIn(right_panel), FadeIn(right_title))
        self.play(LaggedStart(*(FadeIn(t, shift=LEFT * 0.12) for t in tasks), lag_ratio=0.12))

        caption = Text(
            "Pre-train once on broad data. Adapt the same model to many tasks.",
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK,
        )
        place_footer(caption)
        caption.set_y(-3.05)
        self.play(FadeIn(caption))
        self.wait(1.5)
        self._close()
