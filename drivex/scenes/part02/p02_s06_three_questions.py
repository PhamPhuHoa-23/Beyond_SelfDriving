"""
Scene 2-06 — The Three Core Questions
======================================
Multi-Agent + Multi-Frame + Multi-Task → What / When / How to fuse?
→ V2XPnP answers.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P02S06ThreeQuestions(Scene):
    """
    Three compound labels converge to an arrow pointing at three
    GOLD question boxes, with the V2XPnP answer at the bottom.
    """

    def construct(self):
        self.camera.background_color = COL_NAVY

        # ── compound label: Multi-Agent + Multi-Frame + Multi-Task ─
        labels = VGroup(
            Text("Multi-Agent",  font_size=22, color=COL_WHITE),
            Text("+",            font_size=22, color=COL_WHITE),
            Text("Multi-Frame",  font_size=22, color=COL_WHITE),
            Text("+",            font_size=22, color=COL_WHITE),
            Text("Multi-Task",   font_size=22, color=COL_WHITE),
        ).arrange(RIGHT, buff=0.25)
        labels.move_to(UP * 2.5)

        self.play(
            AnimationGroup(*[Write(t) for t in labels], lag_ratio=0.2),
            run_time=0.8
        )

        # ── arrow ──────────────────────────────────────────────────
        arrow = Arrow(labels.get_bottom(), labels.get_bottom() + DOWN * 1.0,
                      color=COL_BLUE, stroke_width=4)
        self.play(GrowArrow(arrow), run_time=0.3)

        # ── three question boxes ───────────────────────────────────
        questions = [
            "What to transmit?",
            "When to transmit?",
            "How to fuse?",
        ]
        q_boxes = VGroup()
        q_labels = VGroup()
        for q in questions:
            box = RoundedRectangle(
                width=3.8, height=1.2, corner_radius=0.15,
                fill_color="#1E3A5F", fill_opacity=1,
                stroke_color=COL_BLUE, stroke_width=2
            )
            txt = Text(q, font_size=20, color=COL_GOLD, weight=BOLD)
            txt.move_to(box.get_center())
            q_boxes.add(box)
            q_labels.add(txt)

        q_boxes.arrange(RIGHT, buff=0.4)
        q_boxes.move_to(DOWN * 0.6)
        for i, lbl in enumerate(q_labels):
            lbl.move_to(q_boxes[i].get_center())

        for i in range(len(questions)):
            self.play(FadeIn(q_boxes[i]), FadeIn(q_labels[i]), run_time=0.35)

        # ── V2XPnP answer ──────────────────────────────────────────
        answer_txt = Text("→  V2XPnP", font_size=20, color=COL_WHITE)
        answer_txt.move_to(DOWN * 2.4)
        self.play(Write(answer_txt), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(VGroup(labels, arrow, q_boxes, q_labels, answer_txt)),
                  run_time=0.4)
