# drivex/scenes/part01/p01_s04_longtail.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-04: The Long-Tail Problem  (~75s)
#
# Spec: spec_intro_part01.md → SCENE 1-04
# "Long-Tail Problem" title → 3 photo placeholders → shrink →
# Distribution curve (99% blue / 1% red tail) →
# PI + CAR mascots dialogue → "Common Sense" conclusion
# ─────────────────────────────────────────────────────────────────

from drivex.components.slide_helper import SlideImage
from drivex.components.thought_bubble import PIBubble, SpeechBubble
from drivex.components.mascots import create_pi_mascot, create_car_mascot
from drivex.components.colors import (
    COL_BLUE, COL_GOLD, COL_WHITE, COL_RED, COL_GREEN,
    COL_LIGHT_BLUE, COL_DEEP_BLUE, BG_DARK,
)
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")))


_BG = "#0F172A"


def _photo_placeholder(label, width=3.2, height=2.0):
    """Image placeholder with an 'IMAGE' label."""
    rect = Rectangle(
        width=width, height=height,
        fill_color="#2A2A2A", fill_opacity=1,
        stroke_color="#888", stroke_width=1.5,
    )
    lbl = Text(label, font_size=12, color="#AAAAAA").move_to(rect)
    cam = Text("[img]", font_size=14, color="#666").next_to(lbl, UP, buff=0.1)
    return VGroup(rect, cam, lbl)


class P01S04LongTail(Scene):
    """SCENE 1-04 — The Long-Tail Problem"""

    def construct(self):
        self.camera.background_color = _BG

        # ── "Long-Tail Problem" title ─────────────────────────────
        title = Text(
            "The Long-Tail Problem",
            font_size=36, color=COL_RED, weight=BOLD,
        ).center()
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)
        self.play(title.animate.to_edge(UP, buff=0.4), run_time=0.4)

        # ── 3 photo placeholders ──────────────────────────────────
        photos = VGroup(
            _photo_placeholder("Person in road\n(person_road.png)"),
            _photo_placeholder(
                "Traffic lights\non truck\n(traffic_truck.png)"),
            _photo_placeholder("Snowy road\n(snowy_road.png)"),
        ).arrange(RIGHT, buff=0.4).center()

        self.play(LaggedStart(
            *[FadeIn(p, shift=UP * 0.08) for p in photos],
            lag_ratio=0.2,
        ), run_time=0.8)
        self.wait(1.0)

        # Shrink photos upward
        self.play(
            photos.animate.scale(0.52).to_edge(UP, buff=1.0),
            run_time=0.6,
        )

        # ── Long-tail distribution curve ──────────────────────────
        axes = Axes(
            x_range=[-0.1, 5.0, 1],
            y_range=[0, 1.2, 0.5],
            x_length=8,
            y_length=3.5,
            axis_config={"color": COL_WHITE, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.4)

        # Right-skewed distribution (log-normal shape)
        def dist_func(x):
            import math
            if x <= 0:
                return 0
            mu, sigma = 0.6, 0.65
            exponent = -((math.log(x + 0.01) - mu) ** 2) / (2 * sigma ** 2)
            return 0.95 * math.exp(exponent) / ((x + 0.01) * sigma * math.sqrt(2 * math.pi))

        curve = axes.plot(dist_func, x_range=[
                          0.01, 5.0], color=COL_BLUE, stroke_width=2.5)

        # 99% fill area (left of threshold)
        thresh_x = 3.8
        fill_99 = axes.get_area(
            axes.plot(dist_func, x_range=[0.01, thresh_x]),
            x_range=[0.01, thresh_x],
            color=COL_BLUE, opacity=0.3,
        )
        # 1% tail (right of threshold)
        fill_1 = axes.get_area(
            axes.plot(dist_func, x_range=[thresh_x, 4.99]),
            x_range=[thresh_x, 4.99],
            color=COL_RED, opacity=0.45,
        )

        lbl_99 = Text("99%", font_size=22, color=COL_WHITE)
        lbl_99.next_to(axes.c2p(1.8, 0.55), UP, buff=0.05)
        lbl_1 = Text("1%", font_size=20, color=COL_RED, weight=BOLD)
        lbl_1.next_to(axes.c2p(4.3, 0.1), UP + RIGHT, buff=0.05)

        arrow_1 = Arrow(lbl_1.get_left(), axes.c2p(4.15, 0.08),
                        stroke_color=COL_RED, stroke_width=1.5,
                        max_tip_length_to_length_ratio=0.4)

        x_label_common = Text("Common situations",
                              font_size=13, color=COL_LIGHT_BLUE)
        x_label_common.next_to(axes.c2p(1.5, -0.05), DOWN, buff=0.1)
        x_label_edge = Text("Edge cases", font_size=13, color=COL_RED)
        x_label_edge.next_to(axes.c2p(4.3, -0.05), DOWN, buff=0.1)

        self.play(Create(curve), run_time=1.0)
        self.play(FadeIn(fill_99), run_time=0.5)
        self.play(FadeIn(fill_1),  run_time=0.5)
        self.play(FadeIn(lbl_99), FadeIn(lbl_1),
                  GrowArrow(arrow_1), run_time=0.4)
        self.play(FadeIn(x_label_common), FadeIn(x_label_edge), run_time=0.3)

        # Dots traveling from photo positions to tail
        for i, photo in enumerate(photos):
            dot = Dot(radius=0.08, color=COL_RED).move_to(photo.get_center())
            target = axes.c2p(4.0 + i * 0.15, 0.06)
            self.play(dot.animate.move_to(target), run_time=0.5)
            self.play(FadeOut(dot), run_time=0.15)

        self.wait(0.8)

        # ── Mascot dialogue ───────────────────────────────────────
        pi = create_pi_mascot(height=0.85).to_corner(DL, buff=0.4)
        car = create_car_mascot(height=1.2).to_corner(DR, buff=0.4)

        self.play(FadeIn(pi), FadeIn(car), run_time=0.5)

        bubble_pi = PIBubble(pi, "Tại sao con người\nxử lý được?",
                             position=UP + RIGHT, font_size=17)
        self.play(FadeIn(bubble_pi), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(bubble_pi), run_time=0.3)

        bubble_car = SpeechBubble(
            car,
            "Common sense.\nContext. Experience.\nThat's what's missing.",
            position=UP + LEFT, font_size=15,
        )
        self.play(FadeIn(bubble_car), run_time=0.4)

        # "Common Sense" flash
        cs_text = Text("→ Common Sense", font_size=28,
                       color=COL_GOLD, weight=BOLD)
        cs_text.to_edge(DOWN, buff=0.7)
        self.play(Write(cs_text, run_time=0.5))
        self.wait(1.0)

        # Outro
        self.play(FadeOut(VGroup(
            title, photos, axes, curve, fill_99, fill_1,
            lbl_99, lbl_1, arrow_1, x_label_common, x_label_edge,
            pi, car, bubble_car, cs_text,
        )), run_time=0.5)
        self.wait(0.2)
