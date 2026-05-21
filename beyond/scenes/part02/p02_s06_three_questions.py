# beyond/scenes/part02/p02_s06_three_questions.py
# ─────────────────────────────────────────────────────────────────
# P2-06  BA CÂU HỎI CỐT LÕI  (~35s)
#
# 3 câu hỏi xuất hiện ở 3 góc với animation minh họa nhỏ:
#   "What?" — 3 options: raw LiDAR / bbox / BEV features
#   "When?" — cửa sổ cơ hội khi 2 xe đủ gần
#   "How?"  — 2 luồng temporal + spatial merge
# → converge về center: "What? When? How?"
# → "V2XPnP answers all three."
#
# Render:  manim -ql "beyond/scenes/part02/p02_s06_three_questions.py" P02S06ThreeQuestions
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block,
    P2_COOP, GOLD, CYAN_NEON, BLUE_ELECTRIC, GREEN_SIGNAL,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)


class P02S06ThreeQuestions(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("Three Core Questions of V2X Cooperation")
        self.wait(0.2)

        questions = [
            {
                "q": "What?", "color": CYAN_NEON,
                "pos": LEFT * 3.8 + UP * 1.0,
                "sub": "What to transmit?",
                "options": ["Raw LiDAR", "Bounding boxes", "BEV features ✓"],
            },
            {
                "q": "When?", "color": GOLD,
                "pos": RIGHT * 3.8 + UP * 1.0,
                "sub": "When to communicate?",
                "options": ["When close enough", "Opportunity window", "Adaptive timing"],
            },
            {
                "q": "How?", "color": BLUE_ELECTRIC,
                "pos": DOWN * 1.5,
                "sub": "How to fuse?",
                "options": ["Temporal attention", "Spatial attention", "Joint spatio-temporal"],
            },
        ]

        q_mobs = []
        for qd in questions:
            # Question label (large)
            ql = Text(qd["q"], font_size=SIZE_LABEL + 10,
                      color=qd["color"], font=FONT_PRIMARY, weight=BOLD)
            ql.move_to(qd["pos"])
            # Sub-label
            sl = Text(qd["sub"], font_size=SIZE_MICRO + 1,
                      color=TEXT_DIM, font=FONT_PRIMARY)
            sl.next_to(ql, DOWN, buff=0.12)
            # Options
            opts = VGroup(*[
                Text(f"• {o}", font_size=SIZE_MICRO,
                     color=GREEN_SIGNAL if "✓" in o else TEXT_DIM,
                     font=FONT_PRIMARY)
                for o in qd["options"]
            ]).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            opts.next_to(sl, DOWN, buff=0.12)

            grp = VGroup(ql, sl, opts)
            q_mobs.append(grp)

            self.play(
                FadeIn(ql, scale=0.85, run_time=0.28),
                Flash(qd["pos"], color=qd["color"],
                      flash_radius=0.45, num_lines=6, run_time=0.28),
            )
            self.play(
                FadeIn(sl, shift=UP * 0.06, run_time=0.22),
                LaggedStart(*[FadeIn(o, shift=LEFT * 0.06, run_time=0.18)
                              for o in opts], lag_ratio=0.12),
            )
            self.wait(0.2)

        self.wait(0.4)

        # ── Converge to center ─────────────────────────────────
        center_labels = VGroup(
            Text("What?", font_size=SIZE_LABEL + 4, color=CYAN_NEON,
                 font=FONT_PRIMARY, weight=BOLD),
            Text("When?", font_size=SIZE_LABEL + 4, color=GOLD,
                 font=FONT_PRIMARY, weight=BOLD),
            Text("How?",  font_size=SIZE_LABEL + 4, color=BLUE_ELECTRIC,
                 font=FONT_PRIMARY, weight=BOLD),
        ).arrange(RIGHT, buff=0.55).move_to(UP * 0.4)

        self.play(
            *[FadeOut(q, run_time=0.40) for q in q_mobs],
        )
        self.play(
            LaggedStart(*[
                FadeIn(cl, scale=1.2, run_time=0.28)
                for cl in center_labels
            ], lag_ratio=0.15),
        )
        self.play(
            LaggedStart(*[
                Flash(cl.get_center(), color=cl.get_color(),
                      flash_radius=0.40, num_lines=6, run_time=0.25)
                for cl in center_labels
            ], lag_ratio=0.10),
        )
        self.wait(0.5)

        # Answer
        answer = Text("V2XPnP answers all three.",
                      font_size=SIZE_LABEL + 2, color=TEXT_WHITE,
                      font=FONT_PRIMARY, weight=BOLD)
        answer.next_to(center_labels, DOWN, buff=0.45)
        self.play(Write(answer, run_time=0.80))
        self.wait(1.5)

        self.close()
