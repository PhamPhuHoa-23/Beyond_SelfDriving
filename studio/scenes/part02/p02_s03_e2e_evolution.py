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
            label = VGroup(title, subtitle).arrange(DOWN, buff=0.1)
            label.next_to(dot, UP, buff=0.22)
            note_mob = Text(note, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
            note_mob.next_to(dot, DOWN, buff=0.34)
            nodes.add(dot)
            labels.add(label)
            notes.add(note_mob)

        # Animate each milestone group (dot + label + note) sequentially from left to right
        animations = []
        for i in range(len(data)):
            anim = AnimationGroup(
                FadeIn(nodes[i], shift=DOWN * 0.12),
                FadeIn(labels[i]),
                FadeIn(notes[i]),
                lag_ratio=0.15
            )
            animations.append(anim)
        self.play(LaggedStart(*animations, lag_ratio=0.8, run_time=3.5))

        modular = Text("modular", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        modular.next_to(nodes[0], DOWN, buff=0.85)
        e2e = Text("end-to-end", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD)
        e2e.next_to(nodes[2], UP, buff=0.9)
        # Brainstormed E2E Advantages Card design
        def get_checkmark(color=GREEN_FIX, scale=0.12):
            chk = VMobject()
            chk.set_points_as_corners([
                LEFT * 0.35 + DOWN * 0.08,
                LEFT * 0.08 + DOWN * 0.35,
                RIGHT * 0.35 + UP * 0.35
            ])
            chk.set_stroke(color, width=2.8)
            chk.scale(scale)
            return chk

        title = Text("E2E ADVANTAGES", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GREEN_FIX, weight=BOLD)
        
        bullets_data = [
            "less error accumulation",
            "less information loss",
            "joint optimization"
        ]
        
        bullets = VGroup()
        for text_str in bullets_data:
            chk = get_checkmark()
            lbl = Text(text_str, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
            bullet = VGroup(chk, lbl).arrange(RIGHT, buff=0.16)
            bullets.add(bullet)
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        
        content_no_sep = VGroup(title, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        sep = Line(LEFT * 0.5, RIGHT * 0.5, stroke_color=GREEN_FIX, stroke_width=1.0, stroke_opacity=0.3)
        sep.match_width(content_no_sep)
        
        content = VGroup(title, sep, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        
        card_box = RoundedRectangle(
            width=content.get_width() + 0.5,
            height=content.get_height() + 0.4,
            corner_radius=0.12,
            fill_color=BG_CARD,
            fill_opacity=1.0,
            stroke_color=GREEN_FIX,
            stroke_width=2.0,
        )
        glow_box = RoundedRectangle(
            width=card_box.get_width() + 0.12,
            height=card_box.get_height() + 0.12,
            corner_radius=0.14,
            fill_color=GREEN_FIX,
            fill_opacity=0.06,
            stroke_color=GREEN_FIX,
            stroke_width=4.0,
            stroke_opacity=0.15,
        )
        
        adv_group = VGroup(glow_box, card_box, content).move_to(RIGHT * 3.4 + DOWN * 1.85)
        content.move_to(card_box)
        glow_box.move_to(card_box)
        
        self.play(FadeIn(modular), FadeIn(e2e), FadeIn(adv_group, shift=LEFT * 0.15))

        q = small_caption("Has end-to-end solved everything?", color=INK_DARK)
        q.to_edge(DOWN, buff=0.74)
        self.play(FadeIn(q))
        self.wait(0.8)
        self._close()
