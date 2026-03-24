from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class ShiftToE2E(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title Section
        title = Text("PARADIGM SHIFT: SINGLE-AGENT STACK", font_size=32, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP, buff=0.8)
        self.play(Write(title))

        # 2. UniAD Diagram (Smaller to avoid mascot overlap)
        asset_dir = "../../../materials/images/part2/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s04_single_agent_t_modular_n_end_to_end_006.png"))
        diagram = ImageMobject(img_path).set_width(10)
        diagram.shift(UP*0.3)
        
        # Rounded frame for the diagram
        frame = RoundedRectangle(corner_radius=0.1, width=10.2, height=diagram.height + 0.3, 
                                 stroke_color=WHITE, stroke_width=1, fill_opacity=0.03).move_to(diagram.get_center())
        
        self.play(FadeIn(frame, scale=0.9), FadeIn(diagram, scale=0.9))
        self.wait(1.5)

        # 3. Evolution Callouts (No overlapping text)
        evolution = VGroup(
            Text("From Modular", font_size=20, color=RED),
            Arrow(UP, DOWN, color=GRAY),
            Text("To End-to-End (UniAD)", font_size=24, color=GREEN)
        ).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.8).shift(UP*0.5)

        self.play(Write(evolution))
        self.wait(1)

        # 4. Mascot Interjection
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.6).to_corner(DR, buff=0.3)
        self.play(FadeIn(mascot, shift=UP*0.3))
        
        thought = ThoughtBubble(mascot, "Has End-to-End solved\neverything yet?", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)

        self.play(FadeOut(Group(title, diagram, frame, evolution, mascot, thought)))
        self.wait(0.5)
