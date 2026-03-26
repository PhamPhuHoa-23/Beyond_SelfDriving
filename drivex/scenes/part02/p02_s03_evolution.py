"""
Scene 2-03 — Single-Agent Evolution: Modular → End-to-End
==========================================================
Timeline: PnPNet → GameFormer → UniAD → VAD → DiffusionDrive.
Modular vs E2E era brackets. Advantage box. PI question.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *
from drivex.components.mascots import PiMascot, idle_bounce
from drivex.components.thought_bubble import PIBubble


class P02S03Evolution(Scene):
    """
    5-milestone timeline (PnPNet→DiffusionDrive) with era brackets
    and E2E advantages box. PI mascot pops up with question at the end.
    """

    MILESTONES = [
        ("PnPNet",        "CVPR'20", "CNN+LSTM\nPerception+Pred."),
        ("GameFormer",    "ICCV'23", "Interactive\nPrediction"),
        ("UniAD",         "CVPR'23", "Full E2E\nQuery-based"),
        ("VAD",           "ICCV'23", "Vectorized\nAD"),
        ("DiffusionDrive","CVPR'25", "Diffusion-based\nTrajectory"),
    ]

    def construct(self):
        self.camera.background_color = BG_DARK

        # ── header ────────────────────────────────────────────────
        header = Text("Single-Agent Evolution", font_size=28, color=COL_GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header), run_time=0.4)

        # ── timeline spine ─────────────────────────────────────────
        spine = Line(LEFT * 6, RIGHT * 6, color=COL_WHITE, stroke_width=2)
        spine.move_to(ORIGIN + DOWN * 0.3)
        self.play(Create(spine), run_time=0.6)

        # ── milestones ─────────────────────────────────────────────
        n = len(self.MILESTONES)
        xs = [spine.get_left()[0] + i * spine.get_width() / (n - 1) for i in range(n)]
        y0 = spine.get_y()

        nodes = VGroup()
        for i, (name, venue, desc) in enumerate(self.MILESTONES):
            x = xs[i]
            dot = Dot(point=[x, y0, 0], radius=0.12, color=COL_BLUE)
            # alternate labels above/below spine
            side = 1 if i % 2 == 0 else -1
            label_name  = Text(name,  font_size=14, color=COL_WHITE,      weight=BOLD)
            label_venue = Text(venue, font_size=12, color=COL_LIGHT_BLUE)
            label_desc  = Text(desc,  font_size=11, color=COL_LIGHT_BLUE)
            lbl_grp = VGroup(label_name, label_venue, label_desc).arrange(DOWN, buff=0.07)
            lbl_grp.next_to(dot, UP * side * 1.2, buff=0.25)

            # small placeholder for slide image
            placeholder = RoundedRectangle(
                width=1.4, height=0.9, corner_radius=0.08,
                fill_color="#2A2A2A", fill_opacity=1,
                stroke_color=COL_BLUE, stroke_width=1
            )
            placeholder.next_to(lbl_grp, UP * side, buff=0.1)

            nodes.add(VGroup(dot, lbl_grp, placeholder))

        self.play(AnimationGroup(*[FadeIn(n) for n in nodes], lag_ratio=0.2), run_time=1.4)

        # ── era brackets ──────────────────────────────────────────
        # "Modular" bracket — first two milestones
        brace_modular_x_left  = xs[0]
        brace_modular_x_right = xs[1]
        modular_line = Line(
            [brace_modular_x_left, y0 - 1.0, 0],
            [brace_modular_x_right, y0 - 1.0, 0],
            color=COL_RED, stroke_width=3
        )
        tick_l = Line([brace_modular_x_left,  y0 - 0.85, 0], [brace_modular_x_left,  y0 - 1.0, 0], color=COL_RED, stroke_width=3)
        tick_r = Line([brace_modular_x_right, y0 - 0.85, 0], [brace_modular_x_right, y0 - 1.0, 0], color=COL_RED, stroke_width=3)
        brace_mod_lbl = Text("Modular Era", font_size=14, color=COL_RED)
        brace_mod_lbl.move_to([(brace_modular_x_left + brace_modular_x_right) / 2, y0 - 1.3, 0])
        modular_group = VGroup(modular_line, tick_l, tick_r, brace_mod_lbl)

        # "End-to-End" bracket — milestones 3→5
        brace_e2e_x_left  = xs[2]
        brace_e2e_x_right = xs[4]
        e2e_line = Line(
            [brace_e2e_x_left, y0 - 1.0, 0],
            [brace_e2e_x_right, y0 - 1.0, 0],
            color=COL_GREEN, stroke_width=3
        )
        tick_el = Line([brace_e2e_x_left,  y0 - 0.85, 0], [brace_e2e_x_left,  y0 - 1.0, 0], color=COL_GREEN, stroke_width=3)
        tick_er = Line([brace_e2e_x_right, y0 - 0.85, 0], [brace_e2e_x_right, y0 - 1.0, 0], color=COL_GREEN, stroke_width=3)
        brace_e2e_lbl = Text("End-to-End Era", font_size=14, color=COL_GREEN)
        brace_e2e_lbl.move_to([(brace_e2e_x_left + brace_e2e_x_right) / 2, y0 - 1.3, 0])
        e2e_group = VGroup(e2e_line, tick_el, tick_er, brace_e2e_lbl)

        self.play(Create(modular_group), run_time=0.4)
        self.play(Create(e2e_group),    run_time=0.4)

        # ── advantages box ─────────────────────────────────────────
        adv_box = RoundedRectangle(
            width=4.5, height=2.2, corner_radius=0.18,
            fill_color="#1B4332", fill_opacity=1,
            stroke_color=COL_GREEN, stroke_width=2
        )
        adv_title = Text("E2E Advantages", font_size=16, color=COL_GREEN, weight=BOLD)
        bullets = [
            "No error accumulation",
            "No information loss",
            "Joint optimization",
        ]
        bullet_texts = VGroup(*[
            Text(f"✓  {b}", font_size=14, color=COL_WHITE)
            for b in bullets
        ]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        adv_content = VGroup(adv_title, bullet_texts).arrange(DOWN, buff=0.18)
        adv_box.move_to(RIGHT * 4.6 + DOWN * 0.3)
        adv_content.move_to(adv_box.get_center())
        adv_full = VGroup(adv_box, adv_content)

        self.play(FadeIn(adv_full), run_time=0.5)
        self.wait(0.5)

        # ── PI mascot & question ───────────────────────────────────
        pi = PiMascot(height=0.9)
        pi.to_corner(DL, buff=0.4)
        bubble = PIBubble(pi, "E2E đã giải quyết\nmọi thứ chưa?", position=UR)
        self.play(FadeIn(pi), run_time=0.4)
        self.play(FadeIn(bubble), run_time=0.4)
        self.play(idle_bounce(pi, 0.08, 1.2), run_time=1.2)

        answer = Text("Not yet — a physics limit remains.", font_size=20, color=COL_GOLD)
        answer.to_edge(DOWN, buff=0.5)
        self.play(Write(answer), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(VGroup(pi, bubble, answer, nodes, spine,
                                  modular_group, e2e_group, adv_full, header)),
                  run_time=0.5)
