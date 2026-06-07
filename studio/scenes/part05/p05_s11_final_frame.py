"""P05-S11 Final Frame — "Beyond Self-Driving. Not just smarter cars. A safer world." """
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_TITLECARD, GOLD_RICH, GOLD_KEY, INK_LIGHT, CYAN_RADAR,
    ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK,
    FONT_PRIMARY, SIZE_TITLE, SIZE_LABEL, SIZE_CAPS,
    write_chiseled, dust_dissolve,
)
SCRIPT = """Beyond Self-Driving. Not just smarter cars. A safer world."""


class P05S11FinalFrame(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Final Frame"

    def construct(self):
        self.camera.background_color = BG_TITLECARD

        # Subtle background grid (city echo)
        rng = np.random.RandomState(99)
        bg_dots = VGroup()
        for _ in range(40):
            d = Dot(radius=0.04, color=CYAN_RADAR)
            d.move_to(np.array([rng.uniform(-7, 7), rng.uniform(-4, 4), 0]))
            d.set_opacity(rng.uniform(0.08, 0.22))
            bg_dots.add(d)
        self.add(bg_dots)

        # Line 1 — hold 1s after write
        line1 = Text("Beyond Self-Driving.", font=FONT_PRIMARY, font_size=SIZE_TITLE,
                     color=GOLD_RICH, weight=BOLD)
        line1.move_to(UP * 1.2)
        self.play(write_chiseled(line1, run_time=2.5))
        self.wait(1)

        # Line 2 — hold 1s
        line2 = Text("Not just smarter cars.", font=FONT_PRIMARY, font_size=SIZE_TITLE,
                     color=GOLD_RICH)
        line2.move_to(ORIGIN)
        self.play(write_chiseled(line2, run_time=2.0))
        self.wait(1)

        # Line 3 — hold 2s
        line3 = Text("A safer world.", font=FONT_PRIMARY, font_size=SIZE_TITLE,
                     color=GOLD_RICH)
        line3.move_to(DOWN * 1.2)
        self.play(write_chiseled(line3, run_time=1.8))
        self.wait(2)

        # Roadmap strip: all 5 nodes GOLD
        part_colors = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK]
        dots = VGroup()
        for i in range(5):
            d = Dot(radius=0.12, color=GOLD_RICH)
            d.move_to(DOWN * 2.8 + RIGHT * (i - 2) * 1.2)
            dots.add(d)
        connector = Line(dots[0].get_center(), dots[-1].get_center(),
                         stroke_color=GOLD_RICH, stroke_width=1.5, stroke_opacity=0.6)
        self.play(ShowCreation(connector, run_time=0.8),
                  LaggedStart(*(FadeIn(d) for d in dots), lag_ratio=0.1, run_time=0.8))
        self.play(LaggedStart(*(Flash(d, color=GOLD_RICH, line_length=0.18, num_lines=6) for d in dots), lag_ratio=0.08))

        # UCLA text badge
        ucla = Text("UCLA Mobility Lab  ·  ICCV 2025", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        ucla.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(ucla))
        self.wait(1.5)

        # Dust converge to center — inverse of particle_assemble
        # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/logo.py:192 LogoGenerationFlurry inverse
        converge_pts = VGroup()
        for _ in range(80):
            angle = rng.uniform(0, TAU)
            dist = rng.uniform(1.5, 5.5)
            pt = Dot(radius=0.05, color=GOLD_RICH)
            pt.move_to(np.array([dist * np.cos(angle), dist * np.sin(angle), 0]))
            pt.set_opacity(rng.uniform(0.5, 0.9))
            converge_pts.add(pt)
        self.play(LaggedStart(*(FadeIn(p, scale=0.5) for p in converge_pts), lag_ratio=0.01, run_time=0.8))
        # Converge to center dot
        center_dot = Dot(radius=0.18, color=GOLD_RICH)
        self.play(*(p.animate(run_time=2.0, rate_func=smooth, path_arc=rng.uniform(-PI/3, PI/3))
                    .move_to(ORIGIN)
                    for p in converge_pts),
                  FadeOut(VGroup(line1, line2, line3, connector, dots, ucla, bg_dots), run_time=1.5),
                  run_time=2.0)
        self.play(GrowFromCenter(center_dot, run_time=0.3))
        self.play(Flash(center_dot, color=GOLD_RICH, line_length=0.4, num_lines=14, run_time=0.6))
        self.play(FadeOut(converge_pts), FadeOut(center_dot), run_time=1.0)
        self.wait(0.5)
        self._close()
