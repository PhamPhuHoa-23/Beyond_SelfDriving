"""P01-S05 — FM Empowers AV. Audit: network_flow + vla patch rows."""
from manimlib import *
from studio.components import (
    StudioScene, PURPLE_MODEL, GOLD_RICH, CYAN_RADAR, GREEN_FIX, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, place_footer, fm_three_lane,
    EmbeddingArray, make_embedding_row_stack, play_simple_attention_animation,
)

SOURCES = [("VFM", BLUE_C), ("LLM", PURPLE_MODEL), ("MLLM", "#7C3AED"), ("VGM", TEAL)]
TASKS = [("Auto-Label", GREEN_FIX), ("Scenario Gen", ORANGE), ("Sensor Sim", TEAL), ("E2E", GOLD_RICH)]


class P01S05FMEmpower(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Foundation Models Empower AV"

    def construct(self):
        self._open(self.SCENE_TITLE)

        hub = EmbeddingArray(shape=(6, 5), height=2.3, dots_index=-2, buff_ratio=0.6,
                             bracket_color=INK_MID, dark_color=GREY_D, light_color=PURPLE_MODEL)
        hub_lbl = Text("Foundation Models", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=PURPLE_MODEL, weight=BOLD)
        hub_group = VGroup(hub_lbl, hub).arrange(DOWN, buff=0.18)
        hub_lbl.set_x(hub.get_center()[0])

        src_cols = VGroup()
        for name, col in SOURCES:
            rows = make_embedding_row_stack(5, col, vertical_spacing=0.08, width=0.75)
            lbl = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=col, weight=BOLD)
            lbl.next_to(rows, LEFT, buff=0.18)
            src_cols.add(VGroup(lbl, rows))

        task_cols = VGroup()
        for name, col in TASKS:
            rows = make_embedding_row_stack(5, col, vertical_spacing=0.08, width=0.75)
            lbl = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=col, weight=BOLD)
            lbl.next_to(rows, RIGHT, buff=0.18)
            task_cols.add(VGroup(rows, lbl))

        diagram = fm_three_lane(src_cols, hub_group, task_cols, y=0.12, gap=1.0)
        self.play(FadeIn(diagram[1]))
        self.play(LaggedStart(*(FadeIn(s) for s in diagram[0]), lag_ratio=0.1))
        play_simple_attention_animation(self, hub, run_time=2.0)
        self.play(LaggedStart(*(FadeIn(t) for t in diagram[2]), lag_ratio=0.1))

        flashes = []
        for s in diagram[0]:
            flashes.append(ShowPassingFlash(
                Line(s[1].get_right(), hub.get_left(), color=CYAN_RADAR, stroke_width=2),
                time_width=0.4,
            ))
        for t in diagram[2]:
            flashes.append(ShowPassingFlash(
                Line(hub.get_right(), t[0].get_left(), color=GOLD_RICH, stroke_width=2),
                time_width=0.4,
            ))
        self.play(LaggedStart(*flashes, lag_ratio=0.06, run_time=1.6))

        caption = Text(
            "Long-tail Generalization & Generalist Experience",
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD,
        )
        place_footer(caption)
        self.play(FadeIn(caption))
        self.wait(1.8)
        self._close()
