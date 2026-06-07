"""P02-S01 — Part 2 Title Card: teal wave forge."""
from manimlib import *
from studio.components import (
    StudioScene, BG_TITLECARD, ACCENT_TEAL, GOLD_RICH, INK_LIGHT, INK_MID,
    CYAN_RADAR, FONT_PRIMARY, SIZE_CAPS, SIZE_LABEL, write_chiseled,
    vehicle_icon,
)
SCRIPT = """Part 2: Towards End-to-End Cooperative Automation — with Zewei Zhou."""

class P02S01Title(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Towards Cooperative Automation"
    def construct(self):
        self.camera.background_color = BG_TITLECARD
        part_tag = Text("Part 02", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_TEAL)
        part_tag.set_color(ACCENT_TEAL)
        part_tag.to_corner(UR, buff=0.4)
        self.play(FadeIn(part_tag))
        left_center = LEFT * 2.05 + UP * 1.84
        right_center = RIGHT * 2.05 + UP * 1.84
        link = Line(left_center, right_center, stroke_color=CYAN_RADAR, stroke_width=2.4, stroke_opacity=0.45)
        car_a = vehicle_icon(color=ACCENT_TEAL, scale=0.42).move_to(left_center)
        car_b = vehicle_icon(color=GOLD_RICH, scale=0.42).move_to(right_center)

        def signal_rings(center, color):
            rings = VGroup()
            for i, r in enumerate([0.46, 0.72, 0.98, 1.24]):
                rings.add(Circle(
                    radius=r,
                    stroke_color=color,
                    stroke_width=2.1 - 0.22 * i,
                    stroke_opacity=0.58 - 0.08 * i,
                    fill_opacity=0,
                ).move_to(center))
            return rings

        shells_a = signal_rings(left_center, CYAN_RADAR)
        shells_b = signal_rings(right_center, GOLD_RICH)
        network = VGroup(link, shells_a, shells_b, car_a, car_b)
        self.play(
            ShowCreation(link),
            LaggedStart(*(ShowCreation(r) for r in shells_a), lag_ratio=0.08),
            LaggedStart(*(ShowCreation(r) for r in shells_b), lag_ratio=0.08),
            FadeIn(car_a),
            FadeIn(car_b),
            run_time=1.2,
        )
        line1 = Text("Towards End-to-End", font=FONT_PRIMARY, font_size=52, color=ACCENT_TEAL, weight=BOLD)
        line2 = Text("Cooperative Automation", font=FONT_PRIMARY, font_size=44, color=GOLD_RICH)
        line1.set_color(ACCENT_TEAL)
        line2.set_color(GOLD_RICH)
        title = VGroup(line1, line2).arrange(DOWN, buff=0.2).move_to(UP * 0.5)
        self.play(LaggedStart(write_chiseled(line1, run_time=1.8), write_chiseled(line2, run_time=1.5), lag_ratio=0.5))
        speaker = Text("Zewei Zhou  ·  UCLA Mobility Lab", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        speaker.set_color(INK_LIGHT)
        speaker.next_to(title, DOWN, buff=0.45)
        self.play(FadeIn(speaker))
        quote = Text('"A single agent, no matter how smart, is limited by its own line of sight."',
                     font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        quote.set_color(GOLD_RICH)
        quote.next_to(speaker, DOWN, buff=0.4)
        self.play(write_chiseled(quote, run_time=2.0))
        dots = VGroup()
        labels = VGroup()
        names = ["FM", "Coop", "Sim", "Eff", "PhysAI"]
        for i, name in enumerate(names):
            active = i == 1
            color = ACCENT_TEAL if active else INK_MID
            dot = Circle(
                radius=0.085,
                fill_color=color,
                fill_opacity=1.0,
                stroke_color=INK_LIGHT,
                stroke_width=1.2,
            )
            label = Text(name, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=color, weight=BOLD if active else NORMAL)
            label.set_color(color)
            dots.add(dot)
            labels.add(label)
        dots.arrange(RIGHT, buff=0.9).move_to(DOWN * 2.45)
        for dot, label in zip(dots, labels):
            label.next_to(dot, DOWN, buff=0.12)
        roadmap = VGroup(dots, labels)
        self.play(FadeIn(roadmap))
        self.wait(2)
        self.play(FadeOut(network), run_time=0.4)
        self._close()
