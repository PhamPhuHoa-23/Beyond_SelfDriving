"""P01-S02b — Foundation Model Definition.

Audit: helpers EmbeddingArray; network_flow attention; vla patch rows.
"""
from manimlib import *
from studio.components import (
    StudioScene, INK_DARK, INK_MID, PURPLE_MODEL, GREEN_FIX, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    place_footer, fm_three_lane,
)
from studio.reference.transformers_helpers import EmbeddingArray
from studio.reference.network_attention import play_simple_attention_animation
from studio.reference.vla_patches import make_embedding_row_stack

SOURCES = ["Text", "Images", "Speech", "3D"]
TASKS = ["Auto-Label", "Detect", "Scene QA", "E2E"]


class P01S02BFMDefinition(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "What Is a Foundation Model?"

    def construct(self):
        self._open(self.SCENE_TITLE)

        hub = EmbeddingArray(
            shape=(6, 5), height=2.3, dots_index=-2, buff_ratio=0.6,
            bracket_color=INK_MID, dark_color=GREY_D, light_color=PURPLE_MODEL,
        )
        hub_label = Text(
            "Shared representation", font=FONT_PRIMARY, font_size=SIZE_LABEL,
            color=PURPLE_MODEL, weight=BOLD,
        )
        hub_group = VGroup(hub_label, hub)
        hub_group.arrange(DOWN, buff=0.2)
        hub_label.set_x(hub.get_center()[0])

        source_cols = VGroup()
        for name in SOURCES:
            rows = make_embedding_row_stack(5, BLUE_C, vertical_spacing=0.09, width=0.8)
            lbl = Text(name, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=BLUE_C, weight=BOLD)
            lbl.next_to(rows, LEFT, buff=0.2)
            source_cols.add(VGroup(lbl, rows))

        task_cols = VGroup()
        for name, col in zip(TASKS, [GREEN_FIX, ORANGE, BLUE_B, GOLD]):
            rows = make_embedding_row_stack(5, col, vertical_spacing=0.09, width=0.8)
            lbl = Text(name, font=FONT_PRIMARY, font_size=SIZE_CAPS - 2, color=col, weight=BOLD)
            lbl.next_to(rows, RIGHT, buff=0.2)
            task_cols.add(VGroup(rows, lbl))

        diagram = fm_three_lane(source_cols, hub_group, task_cols, y=0.1, gap=1.0)

        self.play(FadeIn(diagram[1]), run_time=0.8)
        self.play(LaggedStart(*(FadeIn(s) for s in diagram[0]), lag_ratio=0.1))
        play_simple_attention_animation(self, hub, run_time=2.8)
        self.play(LaggedStart(*(FadeIn(t) for t in diagram[2]), lag_ratio=0.1))
        play_simple_attention_animation(self, hub, run_time=1.5)

        caption = Text(
            "Diverse data in -> one representation -> many downstream tasks.",
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK,
        )
        place_footer(caption)
        self.play(FadeIn(caption))
        self.wait(1.5)
        self._close()
