"""I-04 - Bridge to Part 1: recap chips + forward question."""
from manimlib import *
from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    BG_PAPER,
    GOLD_RICH,
    INK_MID,
    FONT_PRIMARY,
    SIZE_H1,
    SIZE_LABEL,
    write_chiseled,
)

SCRIPT = """
Before we make many agents cooperate - what's actually inside one agent's mind?
"""


class I04BridgeToP1(StudioScene):
    PART_NUM = 0
    SCENE_TITLE = "Before Part 1"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        chips_data = [
            ("→", "Smart agent", "blind to occlusion"),
            ("→", "Cooperation", "physics, not just algorithm"),
            ("→", "5 parts", "one story"),
        ]
        chips = VGroup()
        for icon, bold_part, rest in chips_data:
            t = Text(
                f"{icon}  {bold_part} - {rest}",
                font=FONT_PRIMARY,
                font_size=SIZE_LABEL,
                color=INK_MID,
            )
            bg = RoundedRectangle(
                width=t.get_width() + 0.5,
                height=t.get_height() + 0.24,
                corner_radius=0.14,
                fill_color=BG_PAPER,
                fill_opacity=1.0,
                stroke_color="#CBD5E1",
                stroke_width=1.4,
            )
            t.move_to(bg)
            chips.add(VGroup(bg, t))
        chips.arrange(DOWN, buff=0.25)
        chips.move_to(UP * 0.55)
        self.play(LaggedStart(*(FadeIn(c, shift=UP * 0.1) for c in chips),
                              lag_ratio=0.24))

        forward_q = Text(
            "What is inside one agent's mind?",
            font=FONT_PRIMARY,
            font_size=SIZE_H1 + 4,
            color=GOLD_RICH,
            weight=BOLD,
        )
        glow = Rectangle(
            width=forward_q.get_width() + 0.35,
            height=0.18,
            fill_color="#FEF3C7",
            fill_opacity=0.15,
            stroke_width=0,
        )
        forward_q.next_to(chips, DOWN, buff=0.62)
        glow.move_to(forward_q.get_bottom() + UP * 0.08)
        self.play(FadeIn(glow), write_chiseled(forward_q, run_time=2.0))

        p1_dot = Circle(radius=0.2, fill_color=ACCENT_BLUE, fill_opacity=0.22,
                        stroke_color=ACCENT_BLUE, stroke_width=2.0)
        p1_dot.to_edge(DOWN, buff=0.42)
        self.add(p1_dot)
        for _ in range(3):
            self.play(p1_dot.animate.set_fill(ACCENT_BLUE, opacity=0.55),
                      run_time=0.15)
            self.play(p1_dot.animate.set_fill(ACCENT_BLUE, opacity=0.22),
                      run_time=0.15)
        self.wait(1.2)
        self._close()
