# beyond/scenes/part01/p01_s08_autovla.py
# ─────────────────────────────────────────────────────────────────
# P1-08  AUTOVLA (UCLA) — CLIMAX PART 1  (~70s)
#
# Scene Complexity Analyzer → toggle Fast/VLA mode.
# VLA mode: typewriter chain-of-thought, slow và có trọng lượng.
# Badge: [IROS 2025 Best Paper · UCLA Mobility Lab] sáng GOLD.
# Bridge: "AutoVLA xử lý được the long tail.
#          Nhưng nó vẫn chỉ nhìn thấy những gì ở trước mặt. → Part 2"
#
# Render:  manim -ql "beyond/scenes/part01/p01_s08_autovla.py" P01S08AutoVLA
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block, pipeline_arrow,
    pipeline_block_entrance, pipeline_arrow_entrance,
    key_insight_reveal,
    BG_SPACE, BG_PANEL,
    GOLD, GOLD_GLOW, CYAN_NEON, P1_FOUNDATION,
    GREEN_SIGNAL, RED_ALERT,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_BODY, SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=81)

COT_LINES = [
    '"There is a person waving on the road —',
    " they appear to be flagging down the vehicle —",
    " emergency? or just jaywalking? —",
    ' safe action: slow down, assess situation..."',
    "→ Brake.  Yield.  Hazard lights on.",
]


class P01S08AutoVLA(BeyondScene):
    PART_COLOR = P1_FOUNDATION

    def construct(self):
        title_mob, sep = self.open("AutoVLA — Dynamic Mode Switching")
        self.wait(0.2)

        # ── Input label ───────────────────────────────────────
        input_lbl = Text("Input: image + sensor data",
                         font_size=SIZE_MICRO + 2, color=TEXT_DIM,
                         font=FONT_PRIMARY)
        input_lbl.move_to(UP * 2.55 + LEFT * 3.5)

        input_arr = Arrow(
            input_lbl.get_right() + RIGHT * 0.1,
            input_lbl.get_right() + RIGHT * 0.9,
            buff=0.0, color=TEXT_DIM, stroke_width=1.5, tip_length=0.14,
        )
        self.play(FadeIn(input_lbl, run_time=0.30),
                  Create(input_arr, run_time=0.25))

        # ── Scene Complexity Analyzer ─────────────────────────
        analyzer = pipeline_block(
            "Scene Complexity\nAnalyzer",
            width=3.0, height=1.0,
            border_color=CYAN_NEON, fill_color=BG_PANEL,
            font_size=SIZE_MICRO + 2,
        )
        analyzer.move_to(UP * 2.55)
        self.play(pipeline_block_entrance(analyzer, accent_color=CYAN_NEON))

        # Pulsing neon on analyzer
        t_ref = [0.0]
        def pulse_border(mob, dt):
            t_ref[0] += dt
            op = 0.6 + 0.4 * abs(np.sin(t_ref[0] * 3.0))
            mob[0].set_stroke(opacity=op)
        analyzer.add_updater(pulse_border)
        self.wait(0.5)

        # ── TWO BRANCHES ─────────────────────────────────────
        # Left: Simple scene → Fast mode (green)
        # Right: Complex scene → VLA mode (gold)

        # Decision arrow going DOWN from analyzer
        decision_arrow = Arrow(
            analyzer.get_bottom(),
            analyzer.get_bottom() + DOWN * 0.7,
            buff=0.0, color=TEXT_DIM, stroke_width=1.5, tip_length=0.15,
        )
        self.play(pipeline_arrow_entrance(decision_arrow, style="electric"))

        # Branch fork node
        fork = Dot(radius=0.08, color=TEXT_DIM,
                   fill_opacity=1.0)
        fork.move_to(analyzer.get_bottom() + DOWN * 0.72)
        self.play(GrowFromCenter(fork, run_time=0.18))

        # LEFT branch — Fast mode
        fast_branch = VGroup(
            Arrow(fork.get_center(), fork.get_center() + LEFT * 2.8,
                  buff=0.0, color=GREEN_SIGNAL, stroke_width=1.8,
                  tip_length=0.16),
        )
        fast_box = pipeline_block(
            "Fast Mode\n(Traditional)",
            width=2.5, height=0.90,
            border_color=GREEN_SIGNAL, fill_color=BG_PANEL,
            font_size=SIZE_MICRO + 1,
        )
        fast_box.move_to(fork.get_center() + LEFT * 3.6 + DOWN * 0.0)

        # Context label above fast branch
        simple_lbl = Text("Simple scene", font_size=SIZE_MICRO,
                          color=GREEN_SIGNAL, font=FONT_PRIMARY)
        simple_lbl.next_to(fast_branch[0], UP, buff=0.08)

        # RIGHT branch — VLA mode
        vla_branch = Arrow(
            fork.get_center(), fork.get_center() + RIGHT * 2.8,
            buff=0.0, color=GOLD, stroke_width=2.0, tip_length=0.16,
        )
        vla_box = pipeline_block(
            "VLA Reasoning\nMode",
            width=2.5, height=0.90,
            border_color=GOLD, fill_color="#1A1200",
            font_size=SIZE_MICRO + 2,
        )
        vla_box.move_to(fork.get_center() + RIGHT * 3.6)

        complex_lbl = Text("Complex / ambiguous scene",
                           font_size=SIZE_MICRO, color=GOLD,
                           font=FONT_PRIMARY)
        complex_lbl.next_to(vla_branch, UP, buff=0.08)

        # Show branches
        self.play(
            AnimationGroup(
                Create(fast_branch[0], run_time=0.35),
                Create(vla_branch, run_time=0.35),
            )
        )
        self.play(
            FadeIn(simple_lbl, shift=UP * 0.06, run_time=0.25),
            FadeIn(complex_lbl, shift=UP * 0.06, run_time=0.25),
        )
        self.play(
            pipeline_block_entrance(fast_box, accent_color=GREEN_SIGNAL),
            run_time=0.55,
        )
        self.play(
            pipeline_block_entrance(vla_box, accent_color=GOLD),
            run_time=0.55,
        )

        # Fast mode output
        fast_out_arr = Arrow(
            fast_box.get_bottom(),
            fast_box.get_bottom() + DOWN * 0.6,
            buff=0.0, color=GREEN_SIGNAL, stroke_width=1.5, tip_length=0.13,
        )
        fast_out = Text("✓ Fast decision", font_size=SIZE_MICRO,
                        color=GREEN_SIGNAL, font=FONT_PRIMARY)
        fast_out.next_to(fast_out_arr, DOWN, buff=0.08)
        self.play(
            Create(fast_out_arr, run_time=0.20),
            FadeIn(fast_out, run_time=0.22),
        )
        self.wait(0.4)

        # ── VLA Chain-of-Thought TYPEWRITER ────────────────────
        # Stop pulsing before cot appears
        analyzer.remove_updater(pulse_border)

        cot_title = Text("Chain-of-Thought Reasoning:",
                         font_size=SIZE_MICRO + 1, color=GOLD,
                         font=FONT_PRIMARY, weight=BOLD)
        cot_title.next_to(vla_box, DOWN, buff=0.28)
        self.play(FadeIn(cot_title, run_time=0.25))

        cot_mobs = VGroup()
        prev = cot_title
        for i, line in enumerate(COT_LINES):
            col = GOLD if i == len(COT_LINES) - 1 else TEXT_WHITE
            style = ITALIC if '"' in line else NORMAL
            cot_line = Text(line, font_size=SIZE_MICRO,
                            color=col, font=FONT_PRIMARY, slant=style)
            cot_line.next_to(prev, DOWN, buff=0.08)
            cot_line.align_to(cot_title, LEFT)
            # Clamp width
            if cot_line.width > 4.5:
                cot_line.scale(4.5 / cot_line.width)
                cot_line.next_to(prev, DOWN, buff=0.08).align_to(cot_title, LEFT)

            # Typewriter speed: thoughtful pacing — capped 0.4s–1.6s per line
            cot_rt = max(0.40, min(1.60, 0.052 * len(line)))
            self.play(
                AddTextLetterByLetter(cot_line, run_time=cot_rt, rate_func=linear),
            )
            # Pause after each line — let viewer read
            pause = 0.50 if i < len(COT_LINES) - 1 else 0.80
            self.wait(pause)
            cot_mobs.add(cot_line)
            prev = cot_line

        self.wait(0.4)

        # ── Badge GOLD — IROS 2025 Best Paper ─────────────────
        badge_bg = RoundedRectangle(
            corner_radius=0.10, width=4.8, height=0.55,
            fill_color="#1A1200", fill_opacity=1.0,
            stroke_color=GOLD, stroke_width=1.8,
        )
        badge_txt = Text(
            "★  IROS 2025 Best Paper  ·  UCLA Mobility Lab",
            font_size=SIZE_MICRO + 2, color=GOLD,
            font=FONT_PRIMARY, weight=BOLD,
        )
        badge_txt.move_to(badge_bg)
        badge = VGroup(badge_bg, badge_txt)
        badge.next_to(cot_mobs, DOWN, buff=0.30)
        if badge.get_bottom()[1] < -3.3:
            badge.shift(UP * abs(badge.get_bottom()[1] + 3.3))

        self.play(
            GrowFromCenter(badge_bg, run_time=0.35),
            FadeIn(badge_txt, run_time=0.25),
            Flash(badge_bg.get_center(), color=GOLD,
                  flash_radius=1.2, num_lines=10, run_time=0.45),
        )
        self.wait(1.5)

        # ── Bridge to Part 2 ──────────────────────────────────
        bridge = VGroup(
            Text("AutoVLA handles the long tail.",
                 font_size=SIZE_LABEL - 1, color=TEXT_WHITE,
                 font=FONT_PRIMARY),
            Text("But it only sees what's directly in front.",
                 font_size=SIZE_LABEL - 1, color=TEXT_DIM,
                 font=FONT_PRIMARY),
            Text("→ Part 2", font_size=SIZE_LABEL,
                 color=P1_FOUNDATION, font=FONT_PRIMARY),
        ).arrange(DOWN, buff=0.20)
        bridge.to_edge(DOWN, buff=0.42)

        self.play(
            LaggedStart(*[FadeIn(ln, shift=UP*0.08, run_time=0.35)
                          for ln in bridge], lag_ratio=0.25),
        )
        self.wait(1.5)

        self.close()
