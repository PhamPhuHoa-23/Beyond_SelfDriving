# beyond/scenes/part01/p01_s02_genai_boom.py
# ─────────────────────────────────────────────────────────────────
# P1-02  GENERATIVE AI BỐC CHÁY  (~45s)
#
# Không phải slide thống kê nhàm. Đây là bảng thời gian sống.
# Curve bắt đầu flat, rồi 2023 bẻ gãy thành đường thẳng đứng.
# Milestones nổi bật như bong bóng: GPT-3, CLIP, ChatGPT, GPT-4...
# Panel definition FM xuất hiện bên phải (không overlap chart).
# Câu hỏi vàng kết thúc — mời sang cảnh tiếp.
#
# Render:  manim -ql "beyond/scenes/part01/p01_s02_genai_boom.py" P01S02GenAiBoom
# ─────────────────────────────────────────────────────────────────

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, scene_open, scene_close, key_insight_reveal,
    axes_deploy, curve_trace,
    pipeline_block, pipeline_block_entrance,
    bullet_reveal, key_term_reveal,
    glow_pulse,
    BG_SPACE, BG_PANEL, GOLD, GOLD_GLOW, CYAN_NEON,
    P1_FOUNDATION, TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    RED_ALERT, GREEN_SIGNAL, BLUE_ELECTRIC,
    SIZE_BODY, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=13)

# Milestones: (year_x_on_axes, label, size_mult, color, annotation)
MILESTONES = [
    (2020.3, "GPT-3",    1.0, P1_FOUNDATION,  "Language as a foundation"),
    (2021.1, "CLIP",     1.1, CYAN_NEON,       "Vision + language aligned"),
    (2022.8, "ChatGPT",  1.5, GOLD_GLOW,       "AI enters everyday life"),
    (2023.3, "GPT-4",    2.0, GOLD,            "Turning point of history"),
    (2024.2, "Gemma /\nQwen",  1.2, GREEN_SIGNAL, "Open-source boom"),
    (2025.0, "???",      1.3, RED_ALERT,       ""),
]


class P01S02GenAiBoom(BeyondScene):
    PART_COLOR = P1_FOUNDATION

    def construct(self):
        title_mob, sep = self.open("Generative AI Boom")
        self.wait(0.2)

        # ── Axes (LEFT 55% of canvas) ─────────────────────────
        axes = Axes(
            x_range=[2019.5, 2025.5, 1],
            y_range=[0, 1.05, 0.25],
            x_length=7.0,
            y_length=4.2,
            axis_config={
                "color": TEXT_DIM,
                "stroke_width": 1.5,
                "include_tip": True,
                "tip_length": 0.18,
            },
            x_axis_config={
                "numbers_to_include": [2020, 2021, 2022, 2023, 2024, 2025],
                "label_direction": DOWN,
                "font_size": SIZE_MICRO,
                "decimal_number_config": {"num_decimal_places": 0},
            },
            y_axis_config={"include_numbers": False},
        ).shift(LEFT * 2.5 + DOWN * 0.4)

        x_label = Text("Year", font_size=SIZE_MICRO + 1, color=TEXT_DIM, font=FONT_PRIMARY)
        x_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.12)
        y_label = Text("AI Capability", font_size=SIZE_MICRO + 1,
                       color=TEXT_DIM, font=FONT_PRIMARY)
        y_label.next_to(axes.y_axis.get_end(), UP, buff=0.10)

        self.play(axes_deploy(axes, "", ""))
        self.play(
            FadeIn(x_label, shift=RIGHT * 0.08, run_time=0.25),
            FadeIn(y_label, shift=UP * 0.08, run_time=0.25),
        )

        # ── AI capability curve ────────────────────────────────
        # Flat then exponential — 2023 is the "knee"
        def ai_curve(x):
            if x < 2022.5:
                return 0.04 + (x - 2019.5) * 0.055
            else:
                v = (x - 2022.5) ** 2.2 * 0.38
                return min(0.04 + (2022.5 - 2019.5) * 0.055 + v, 1.0)

        # Gradient fill under curve (approximated with area)
        main_curve = axes.plot(ai_curve, x_range=[2019.6, 2025.2],
                               color=P1_FOUNDATION, stroke_width=3.0)
        fill_area = axes.get_area(
            main_curve, x_range=[2019.6, 2025.2],
            color=P1_FOUNDATION, opacity=0.10,
        )

        # Trace curve with glowing head (curve_trace recipe)
        head = Dot(radius=0.08, color=WHITE)
        head_trail = TracedPath(head.get_center, stroke_color=P1_FOUNDATION,
                                stroke_width=3.5, dissipating_time=0.35)
        x_tracker = ValueTracker(2019.6)
        head.add_updater(lambda m: m.move_to(
            axes.input_to_graph_point(x_tracker.get_value(), main_curve)
        ))
        head.move_to(axes.input_to_graph_point(2019.6, main_curve))

        self.add(head, head_trail)
        self.play(
            AnimationGroup(
                x_tracker.animate(run_time=2.0, rate_func=smooth).set_value(2025.2),
                Create(main_curve, run_time=2.0, rate_func=smooth),
            )
        )
        head.remove_updater(head.get_updaters()[-1])
        self.play(
            FadeOut(head, run_time=0.18),
            FadeOut(head_trail, run_time=0.18),
            FadeIn(fill_area, run_time=0.3),
        )

        # ── Milestones bubble up along curve ──────────────────
        milestone_mobs = []
        for year, name, size, color, note in MILESTONES:
            try:
                pt = axes.input_to_graph_point(year, main_curve)
            except Exception:
                pt = axes.c2p(year, ai_curve(year))

            dot = Dot(radius=0.07 * size, color=color, fill_opacity=1.0).move_to(pt)

            # Label above the dot
            lbl = Text(name, font_size=SIZE_MICRO + (1 if size > 1.2 else 0),
                       color=color, font=FONT_PRIMARY, line_spacing=0.35)
            lbl.next_to(dot, UP + LEFT * 0.3, buff=0.10)
            # Keep inside canvas
            if lbl.get_left()[0] < -6.4:
                lbl.next_to(dot, RIGHT, buff=0.10)

            milestone_mobs.append((dot, lbl, color, size))

        for dot, lbl, color, size in milestone_mobs:
            n_lines = 5 if size < 1.5 else 8
            self.play(
                GrowFromCenter(dot, run_time=0.18),
                Flash(dot.get_center(), color=color,
                      flash_radius=0.12 * size, num_lines=n_lines, run_time=0.2),
                FadeIn(lbl, shift=UP * 0.06, run_time=0.22),
                run_time=0.3,
            )
            if size >= 1.5:  # big moments get an extra beat
                self.wait(0.25)

        self.wait(0.3)

        # ── RIGHT side: Foundation Model definition panel ──────
        # Strictly in RIGHT 38% of canvas (x > 1.5)
        panel_x = RIGHT * 4.4

        fm_title = Text("Foundation Model", font_size=SIZE_LABEL,
                        color=P1_FOUNDATION, font=FONT_PRIMARY, weight=BOLD)
        fm_title.move_to(panel_x + UP * 1.4)

        panel_bg = RoundedRectangle(
            corner_radius=0.14, width=3.6, height=3.0,
            fill_color=BG_PANEL, fill_opacity=1.0,
            stroke_color=P1_FOUNDATION, stroke_width=1.4,
        ).move_to(panel_x + DOWN * 0.1)

        bullet_items = [
            "Train on massive,\ndiverse data",
            "Self-supervised\nlearning",
            "Fine-tune to any\ndownstream task",
        ]
        bullets = VGroup(*[
            VGroup(
                Dot(radius=0.05, color=P1_FOUNDATION),
                Text(txt, font_size=SIZE_MICRO + 1,
                     color=TEXT_WHITE, font=FONT_PRIMARY, line_spacing=0.35),
            ).arrange(RIGHT, buff=0.20)
            for txt in bullet_items
        ]).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        bullets.move_to(panel_bg).shift(LEFT * 0.2 + UP * 0.15)

        citation = Text("[Stanford CRFM, 2021]", font_size=SIZE_MICRO - 1,
                        color=TEXT_GHOST, font=FONT_PRIMARY)
        citation.next_to(panel_bg, DOWN, buff=0.10)

        # Hologram scan reveal
        scan_line = Line(
            panel_bg.get_left() + UP * panel_bg.height / 2,
            panel_bg.get_right() + UP * panel_bg.height / 2,
            stroke_color=CYAN_NEON, stroke_width=1.8, stroke_opacity=0.75,
        )
        self.play(FadeIn(fm_title, shift=DOWN * 0.08, run_time=0.35))
        self.play(Create(panel_bg, run_time=0.4))
        self.play(
            AnimationGroup(
                scan_line.animate(run_time=0.65, rate_func=linear)
                         .shift(DOWN * panel_bg.height),
                LaggedStart(*[
                    FadeIn(row, shift=DOWN * 0.04, run_time=0.22)
                    for row in bullets
                ], lag_ratio=0.15),
            ),
        )
        self.play(
            scan_line.animate(run_time=0.2, rate_func=rush_into)
                     .shift(DOWN * 0.5).set_stroke(opacity=0),
            FadeIn(citation, run_time=0.25),
        )
        self.wait(0.5)

        # ── Closing question ──────────────────────────────────
        question = Text(
            "If AI can write, draw, reason —\nwhy can't self-driving go everywhere?",
            font_size=SIZE_LABEL + 1,
            color=GOLD,
            font=FONT_PRIMARY,
            slant=ITALIC,
            line_spacing=0.5,
        )
        # Place below content, safe zone
        question.to_edge(DOWN, buff=0.55)

        self.play(Write(question, run_time=1.4))
        self.wait(0.2)
        self.play(glow_pulse(question, color=GOLD, n_pulses=2, run_time=0.40))
        self.wait(1.8)   # let the question breathe — it's inviting Part 1

        # ── Clean close ───────────────────────────────────────
        self.close()
