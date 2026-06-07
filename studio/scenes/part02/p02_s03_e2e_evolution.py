"""P02-S03 - Single-agent end-to-end evolution."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_CARD,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    PURPLE_MODEL,
    RED_ERROR,
    SIZE_CAPS,
    SIZE_LABEL,
    FONT_PRIMARY,
)
from studio.scenes.part02._p02_helpers import small_caption


SCRIPT = "From PnPNet to DiffusionDrive, the single-agent stack has come a long way."


class P02S03E2EEvolution(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Single-Agent Evolution"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py:227
        start = LEFT * 5.25 + DOWN * 0.22
        end = RIGHT * 5.25 + DOWN * 0.22
        spine = Line(start, end, stroke_color=ACCENT_TEAL, stroke_width=3.0)
        self.play(ShowCreation(spine, run_time=0.8))

        data = [
            ("PnPNet", "2021 · CNN+LSTM", ACCENT_TEAL, "joint perception + prediction"),
            ("GameFormer", "2022 · interaction", ACCENT_BLUE, "prediction becomes game-like"),
            ("UniAD", "2023 · query E2E", PURPLE_MODEL, "optimize the whole stack"),
            ("DiffusionDrive", "2024 · diffusion", GOLD_RICH, "trajectory as generation"),
        ]
        nodes = VGroup()
        notes = VGroup()
        labels = VGroup()
        for i, (name, sub, color, note) in enumerate(data):
            t = i / (len(data) - 1)
            point = interpolate(start, end, t)
            dot = Circle(
                radius=0.18,
                fill_color=color,
                fill_opacity=1.0,
                stroke_color=INK_DARK,
                stroke_width=1.2,
            ).move_to(point)
            title = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
            subtitle = Text(sub, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID, weight=BOLD)
            label = VGroup(title, subtitle).arrange(DOWN, buff=0.02)
            label.next_to(dot, UP, buff=0.22)
            note_mob = Text(note, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
            note_mob.next_to(dot, DOWN, buff=0.34)
            nodes.add(dot)
            labels.add(label)
            notes.add(note_mob)

        self.play(LaggedStart(*(FadeIn(n, shift=DOWN * 0.12) for n in nodes), lag_ratio=0.16))
        self.play(LaggedStart(*(FadeIn(l) for l in labels), lag_ratio=0.12))
        self.play(LaggedStart(*(FadeIn(n) for n in notes), lag_ratio=0.12))

        modular = Text("modular", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        modular.next_to(nodes[0], DOWN, buff=0.85)
        e2e = Text("end-to-end", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD)
        e2e.next_to(nodes[2], UP, buff=0.9)
        adv = VGroup(
            Text("less error accumulation", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK),
            Text("less information loss", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK),
            Text("joint optimization", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        adv_box = RoundedRectangle(
            width=adv.get_width() + 0.45,
            height=adv.get_height() + 0.35,
            corner_radius=0.12,
            fill_color=BG_CARD,
            fill_opacity=1.0,
            stroke_color=GREEN_FIX,
            stroke_width=2,
        )
        adv_group = VGroup(adv_box, adv).move_to(RIGHT * 3.25 + DOWN * 1.55)
        adv.move_to(adv_box)
        self.play(FadeIn(modular), FadeIn(e2e), FadeIn(adv_group, shift=LEFT * 0.15))

        q = small_caption("Has end-to-end solved everything?", color=INK_DARK)
        q.to_edge(DOWN, buff=0.74)
        self.play(FadeIn(q))
        self.wait(0.8)
        self._close()
