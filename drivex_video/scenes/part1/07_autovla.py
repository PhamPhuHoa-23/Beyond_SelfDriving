from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT

class AutoVLA_Concept(Scene):
    def construct(self):
        title = Text("AutoVLA: Dual Thinking Modes", font="Latin Modern Roman", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.0)
        mascot.to_corner(DR, buff=0.3)

        asset_dir = "../../../materials/images/part1/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_s17_autovla_033.png"))
        diagram = ImageMobject(img_path)
        diagram.set_height(4.0)
        diagram.next_to(title, DOWN, buff=0.4)

        modes = VGroup(
            Text("System 1: FAST (Reactive)", font="Latin Modern Roman", font_size=24, color=BLUE_A),
            Text("System 2: SLOW (Reasoning)", font="Latin Modern Roman", font_size=24, color=UCLA_GOLD)
        ).arrange(RIGHT, buff=1.0).next_to(diagram, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(diagram))
        self.play(FadeIn(mascot, shift=LEFT))
        self.wait(1)
        
        self.play(FadeIn(modes[0], shift=UP*0.2))
        self.wait(1)
        self.play(FadeIn(modes[1], shift=UP*0.2))
        self.play(Indicate(mascot))
        self.wait(2.5)
        
        self.play(FadeOut(Group(title, diagram, mascot, modes)))
        self.wait(0.5)

class AutoVLA_Results(Scene):
    def construct(self):
        title = Text("AutoVLA Results (nuPlan)", font="Latin Modern Roman", font_size=42, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP)
        
        stats = VGroup(
            Text("+10.6% Planning Score Improvement", font="Latin Modern Roman", font_size=28),
            Text("-66.8% Runtime Reduction (Fast Mode)", font="Latin Modern Roman", font_size=28),
            Text("Superior OOD Generalization", font="Latin Modern Roman", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).center()

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT*0.3) for s in stats], lag_ratio=0.5))
        self.wait(3.5)
        self.play(FadeOut(Group(title, stats)))
        self.wait(0.5)
