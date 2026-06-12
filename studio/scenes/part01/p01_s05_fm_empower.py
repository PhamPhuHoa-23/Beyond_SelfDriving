"""P01-S05 - Foundation models empower autonomous driving."""
from manimlib import *
from studio.components import (
    StudioScene, PURPLE_MODEL, GOLD_RICH, CYAN_RADAR, GREEN_FIX, INK_MID,
    INK_DARK, BG_CARD, ACCENT_BLUE, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
)

SOURCES = [
    ("VISION FM", "SAM · DINO · CLIP", ACCENT_BLUE),
    ("VIDEO GM", "Cosmos · Wan", CYAN_RADAR),
    ("LLM", "world knowledge", PURPLE_MODEL),
    ("MLLM", "Gemma · Qwen-VL", "#7C3AED"),
]
TASKS = [
    ("Auto-labeling", GREEN_FIX),
    ("Scenario generation", ORANGE),
    ("Sensor simulation", CYAN_RADAR),
    ("Vehicle interface", ACCENT_BLUE),
    ("Language reasoning", PURPLE_MODEL),
    ("End-to-end driving", GOLD_RICH),
]


def family_card(title, examples, color):
    box = RoundedRectangle(
        width=1.85, height=1.02, corner_radius=0.16,
        fill_color=color, fill_opacity=0.11,
        stroke_color=color, stroke_width=1.8,
    )
    heading = Text(
        title, font=FONT_PRIMARY, font_size=SIZE_CAPS - 1,
        color=color,
    )
    detail = Text(
        examples, font=FONT_PRIMARY, font_size=SIZE_CAPS - 5,
        color=INK_MID,
    )
    content = VGroup(heading, detail).arrange(DOWN, buff=0.11)
    content.move_to(box)
    return VGroup(box, content)


def capability_card(label, color):
    box = RoundedRectangle(
        width=2.05, height=0.7, corner_radius=0.14,
        fill_color=color, fill_opacity=0.11,
        stroke_color=color, stroke_width=1.7,
    )
    text = Text(
        label, font=FONT_PRIMARY, font_size=SIZE_CAPS - 4,
        color=INK_DARK,
    )
    text.set_max_width(1.75)
    text.move_to(box)
    return VGroup(box, text)


def knowledge_core():
    panel = RoundedRectangle(
        width=2.25, height=2.75, corner_radius=0.3,
        fill_color=PURPLE_MODEL, fill_opacity=0.12,
        stroke_color=PURPLE_MODEL, stroke_width=2.8,
    )
    top = Text(
        "WORLD", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2,
        color=PURPLE_MODEL,
    )
    bottom = Text(
        "KNOWLEDGE", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2,
        color=PURPLE_MODEL,
    )
    core_title = VGroup(top, bottom).arrange(DOWN, buff=0.08)
    core_title.next_to(panel.get_top(), DOWN, buff=0.18)

    nodes = VGroup(*[
        Circle(radius=0.09, fill_color=PURPLE_MODEL, fill_opacity=1, stroke_width=0)
        for _ in range(5)
    ])
    node_pos = [
        LEFT * 0.55 + UP * 0.15,
        UP * 0.42,
        RIGHT * 0.55 + UP * 0.1,
        LEFT * 0.25 + DOWN * 0.42,
        RIGHT * 0.42 + DOWN * 0.45,
    ]
    for node, pos in zip(nodes, node_pos):
        node.move_to(pos)
    edges = VGroup(*[
        Line(nodes[a], nodes[b], stroke_color=PURPLE_MODEL, stroke_width=1.5, stroke_opacity=0.55)
        for a, b in [(0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4), (3, 4)]
    ])
    network = VGroup(edges, nodes).move_to(panel.get_center() + DOWN * 0.08)

    empower = Text(
        "EMPOWER", font=FONT_PRIMARY, font_size=SIZE_LABEL - 1,
        color=GOLD_RICH,
    )
    empower.next_to(panel.get_bottom(), UP, buff=0.2)
    return VGroup(panel, top, bottom, network, empower)


class P01S05FMEmpower(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Foundation Models Empower AV"

    def construct(self):
        self._open(self.SCENE_TITLE)

        left_panel = RoundedRectangle(
            width=4.35, height=3.55, corner_radius=0.22,
            fill_color=BG_CARD, fill_opacity=0.62,
            stroke_color=ACCENT_BLUE, stroke_width=2,
        ).move_to(LEFT * 4.15 + UP * 0.02)
        left_title = Text(
            "FOUNDATION MODEL ECOSYSTEM", font=FONT_PRIMARY, font_size=SIZE_CAPS - 4,
            color=ACCENT_BLUE,
        )
        left_title.next_to(left_panel.get_top(), DOWN, buff=0.22)
        families = VGroup(*[family_card(*spec) for spec in SOURCES])
        families.arrange_in_grid(n_rows=2, n_cols=2, buff=0.23)
        families.move_to(left_panel.get_center() + DOWN * 0.18)

        core = knowledge_core().move_to(DOWN * 0.02)

        right_panel = RoundedRectangle(
            width=4.55, height=3.55, corner_radius=0.22,
            fill_color=BG_CARD, fill_opacity=0.62,
            stroke_color=GREEN_FIX, stroke_width=2,
        ).move_to(RIGHT * 4.15 + UP * 0.02)
        right_title = Text(
            "AUTONOMOUS-DRIVING CAPABILITIES", font=FONT_PRIMARY, font_size=SIZE_CAPS - 5,
            color=GREEN_FIX,
        )
        right_title.next_to(right_panel.get_top(), DOWN, buff=0.22)
        capabilities = VGroup(*[capability_card(*spec) for spec in TASKS])
        capabilities.arrange_in_grid(n_rows=3, n_cols=2, buff=0.21)
        capabilities.move_to(right_panel.get_center() + DOWN * 0.18)

        flow_y = core[0].get_center()[1]
        into_core = Arrow(
            [left_panel.get_right()[0] + 0.06, flow_y, 0],
            [core[0].get_left()[0] - 0.06, flow_y, 0],
            thickness=3, fill_color=PURPLE_MODEL, buff=0,
        )
        into_av = Arrow(
            [core[0].get_right()[0] + 0.06, flow_y, 0],
            [right_panel.get_left()[0] - 0.06, flow_y, 0],
            thickness=3, fill_color=GOLD_RICH, buff=0,
        )

        goal_band = RoundedRectangle(
            width=9.4, height=0.62, corner_radius=0.16,
            fill_color=GOLD_RICH, fill_opacity=0.13,
            stroke_color=GOLD_RICH, stroke_width=1.8,
        )
        goal_band.move_to(DOWN * 2.63)
        goal = Text(
            "Long-tail Generalization & Generalist Experience",
            font=FONT_PRIMARY, font_size=SIZE_LABEL - 1, color=GOLD_RICH,
        )
        goal.move_to(goal_band)

        self.play(FadeIn(left_panel), FadeIn(left_title))
        self.play(LaggedStart(*(FadeIn(card, shift=RIGHT * 0.1) for card in families), lag_ratio=0.12))
        self.play(ShowCreation(into_core))
        self.play(FadeIn(core[0]), FadeIn(VGroup(core[1], core[2])))
        self.play(
            ShowCreation(core[3][0]),
            LaggedStart(*(GrowFromCenter(n) for n in core[3][1]), lag_ratio=0.1),
        )
        self.play(FadeIn(core[4]))
        self.play(ShowCreation(into_av))
        self.play(FadeIn(right_panel), FadeIn(right_title))
        self.play(LaggedStart(*(FadeIn(card, shift=LEFT * 0.1) for card in capabilities), lag_ratio=0.1))
        self.play(FadeIn(goal_band), FadeIn(goal))
        self.wait(1.8)
        self._close()
