"""
Scene 2-05 — Related Works & Research Gaps
===========================================
Timeline: V2VNet → V2X-ViT → Where2comm → CodeFilling.
Datasets: OPV2V (sim) → V2X-Real (real).
Two gap cards: Model Gap + Data Gap.
"""
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P02S05RelatedWorks(Scene):
    """
    Part A: method timeline with category colour tags.
    Part B: two gap cards (slide in from sides).
    """

    METHODS = [
        ("V2VNet",     "CoRL'20",  "GNN",       COL_BLUE),
        ("V2X-ViT",   "ECCV'22",  "Attention",  COL_PURPLE),
        ("Where2comm", "NeurIPS'22", "Sparse",     COL_GREEN),
        ("CoBEVT",    "CoRL'22",  "Swin Xfmr",  COL_PURPLE),
        ("Where2comm", "NeurIPS'22", "Sparse",     COL_GREEN),
        ("CodeFilling", "CVPR'24", "Codebook",    COL_GOLD),
    ]

    # Deduplicate for display
    METHODS = [
        ("V2VNet",      "CoRL'20",  "GNN",       COL_BLUE),
        ("V2X-ViT",    "ECCV'22",  "Transformer", COL_PURPLE),
        ("Where2comm", "NeurIPS'22", "Sparse",     COL_GREEN),
        ("CodeFilling", "CVPR'24", "Codebook",    COL_GOLD),
        ("OPV2V",       "CVPR'22", "Sim data",    "#888888"),
        ("V2X-Real",    "CVPR'24", "Real data",   COL_GREEN),
    ]

    def construct(self):
        self.camera.background_color = BG_DARK

        # ═══════════════ PART A — Timeline ══════════════════════
        header = Text("Related Works", font_size=28,
                      color=COL_GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.35)
        self.play(FadeIn(header), run_time=0.3)

        spine = Line(LEFT * 6.0, RIGHT * 6.0, color=COL_WHITE, stroke_width=2)
        spine.move_to(ORIGIN + DOWN * 0.1)
        self.play(Create(spine), run_time=0.5)

        n = len(self.METHODS)
        xs = [spine.get_left()[0] + i * spine.get_width() / (n - 1)
              for i in range(n)]
        y0 = spine.get_y()

        node_grp = VGroup()
        for i, (name, venue, cat, color) in enumerate(self.METHODS):
            side = 1 if i % 2 == 0 else -1
            dot = Dot(point=[xs[i], y0, 0], radius=0.11, color=color)
            lbl = VGroup(
                Text(name,  font_size=14, color=COL_WHITE, weight=BOLD),
                Text(venue, font_size=12, color=COL_LIGHT_BLUE),
            ).arrange(DOWN, buff=0.05)
            lbl.next_to(dot, UP * side * 1.2, buff=0.22)
            tag_box = RoundedRectangle(
                width=lbl.get_width() * 0.9, height=0.28, corner_radius=0.08,
                fill_color=color, fill_opacity=0.85, stroke_width=0
            )
            tag_txt = Text(cat, font_size=10, color=BG_DARK)
            tag_box.next_to(lbl, DOWN * side, buff=0.08)
            tag_txt.move_to(tag_box.get_center())
            node_elem = VGroup(dot, lbl, tag_box, tag_txt)
            self.play(FadeIn(node_elem), run_time=0.2)
            node_grp.add(node_elem)

        # dataset brackets
        sim_line = Line([xs[4], y0 - 0.9, 0], [xs[4], y0 -
                        0.9, 0], color=COL_RED)  # placeholder
        # Sim bracket: methods 0-3, Real bracket: method 4+
        sim_brace_x = (xs[0] + xs[3]) / 2
        real_brace_x = (xs[4] + xs[5]) / 2

        sim_bracket = Line([xs[0], y0 - 0.85, 0], [xs[3], y0 - 0.85, 0],
                           color=COL_RED, stroke_width=2)
        sim_lbl = Text("Simulation Era", font_size=13, color=COL_RED)
        sim_lbl.move_to([sim_brace_x, y0 - 1.1, 0])

        real_bracket = Line([xs[4], y0 - 0.85, 0], [xs[5], y0 - 0.85, 0],
                            color=COL_GREEN, stroke_width=2)
        real_lbl = Text("Real-World", font_size=13, color=COL_GREEN)
        real_lbl.move_to([real_brace_x, y0 - 1.1, 0])

        self.play(Create(sim_bracket), FadeIn(sim_lbl), run_time=0.4)
        self.play(Create(real_bracket), FadeIn(real_lbl), run_time=0.4)
        self.wait(0.8)

        # ═══════════════ PART B — Gap Cards ══════════════════════
        self.play(FadeOut(VGroup(header, spine, sim_bracket, sim_lbl,
                                 real_bracket, real_lbl, node_grp)),
                  run_time=0.4)

        gap_header = Text("Critical Research Gaps",
                          font_size=26, color=COL_RED, weight=BOLD)
        gap_header.to_edge(UP, buff=0.4)
        self.play(FadeIn(gap_header), run_time=0.3)

        def make_gap_card(title, bullets, x):
            card = RoundedRectangle(
                width=5.5, height=3.5, corner_radius=0.2,
                fill_color="#2A1A1A", fill_opacity=1,
                stroke_color=COL_RED, stroke_width=2
            )
            card.move_to([x, -0.2, 0])
            t_title = Text(title, font_size=20, color=COL_RED, weight=BOLD)
            t_title.move_to(card.get_top() + DOWN * 0.45)
            sep = Line(card.get_left() + RIGHT * 0.2, card.get_right() + LEFT * 0.2,
                       color=COL_RED, stroke_opacity=0.5, stroke_width=1)
            sep.move_to([x, card.get_top()[1] - 0.8, 0])
            b_group = VGroup(*[
                Text(f"• {b}", font_size=14,
                     color=COL_WHITE, t2c={"•": COL_RED})
                for b in bullets
            ]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            b_group.next_to(sep, DOWN, buff=0.25)
            b_group.set_x(x)
            return VGroup(card, t_title, sep, b_group)

        card1 = make_gap_card(
            "Model Gap", [
                "Only cooperative perception —",
                "no prediction / planning",
                "Single-frame only —",
                "no temporal context",
            ], x=-3.2
        )
        card1.shift(LEFT * 4)  # start off-screen left

        card2 = make_gap_card(
            "Data Gap", [
                "No sequential data / HD maps",
                "Only V2V or V2I separately —",
                "never all V2X modes together",
            ], x=3.2
        )
        card2.shift(RIGHT * 4)  # start off-screen right

        self.play(card1.animate.shift(RIGHT * 4), run_time=0.5)
        self.play(card2.animate.shift(LEFT * 4), run_time=0.5)

        # both cards pulse
        self.play(
            card1.animate.scale(1.04),
            card2.animate.scale(1.04),
            rate_func=there_and_back, run_time=0.4
        )
        self.wait(1.5)

        closing = Text(
            "These gaps are exactly what Part 2 addresses.",
            font_size=18, color=COL_GOLD
        )
        closing.to_edge(DOWN, buff=0.5)
        self.play(Write(closing), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(VGroup(gap_header, card1, card2, closing)), run_time=0.4)
