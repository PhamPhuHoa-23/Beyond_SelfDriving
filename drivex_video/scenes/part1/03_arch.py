from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A

class AVArchitectures(Scene):
    def construct(self):
        title = Text("Three Pillars of AV Architecture", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.0)
        mascot.to_corner(DR, buff=0.3)

        asset_dir = "../../../materials/images/part1/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_s05_arch.png"))
        diagram = ImageMobject(img_path)
        diagram.height = 4.2
        diagram.next_to(title, DOWN, buff=0.8)

        labels = Group(
            Text("Modular", font_size=22, color=UCLA_GOLD, weight=BOLD),
            Text("End-to-End", font_size=22, color=UCLA_GOLD, weight=BOLD),
            Text("Hybrid", font_size=22, color=UCLA_GOLD, weight=BOLD)
        )
        labels.arrange(RIGHT, buff=2.3).next_to(diagram, UP, buff=0.1)

        self.play(Write(title))
        self.play(FadeIn(diagram, shift=UP*0.2))
        self.play(FadeIn(labels, shift=DOWN*0.1))
        self.play(FadeIn(mascot, shift=LEFT))
        self.wait(1.5)

        box_mod = Rectangle(width=2.5, height=3.5, color=BLUE_A).shift(LEFT*3.5 + DOWN*0.5)
        box_e2e = Rectangle(width=2.5, height=3.5, color=DRIVEX_ACCENT).shift(ORIGIN + DOWN*0.5)
        
        lab_mod = Text("Current Standard", font_size=16, color=BLUE_A).next_to(box_mod, UP)
        self.play(Create(box_mod), FadeIn(lab_mod))
        self.play(Indicate(box_mod, color=BLUE_A))
        self.wait(1.5)
        
        lab_e2e = Text("Future Generalization", font_size=16, color=DRIVEX_ACCENT).next_to(box_e2e, UP)
        self.play(ReplacementTransform(box_mod, box_e2e), ReplacementTransform(lab_mod, lab_e2e))
        self.play(Indicate(box_e2e, color=DRIVEX_ACCENT))
        self.play(Indicate(mascot))
        self.wait(2)
        
        self.play(FadeOut(Group(title, diagram, labels, box_e2e, lab_e2e, mascot)))
        self.wait(0.5)
