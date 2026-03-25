from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class Part2Intro(Scene):
    def construct(self):
        # 1. Standard Black Background (Part 1 consistency)
        self.camera.background_color = BLACK
        
        # 2. Title Section
        title = Text("PART 2: TOWARDS E2E COOPERATIVE AUTOMATION", font="Latin Modern Roman", font_size=32, weight=BOLD)
        title.set_color_by_gradient(UCLA_GOLD, WHITE).to_edge(UP, buff=0.8)
        
        self.play(Write(title))
        self.wait(0.5)

        # 3. Mascot Entry
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(2.0)
        mascot.to_corner(DR, buff=0.5)
        
        self.play(FadeIn(mascot, shift=UP*0.3))
        
        # 4. Narrative Transition (Mascot Thinking)
        thought = ThoughtBubble(mascot, "Single-agent perception\nhas hit a physical wall.", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(2)
        
        # 5. Core Message
        message = Text("From Individual Reasoning\nto Collective Intelligence", font="Latin Modern Roman", font_size=32)
        message.set_color(BLUE_A).shift(UP*0.5)
        
        self.play(FadeOut(thought), Write(message))
        self.wait(2)
        
        self.play(FadeOut(Group(title, message, mascot)))
        self.wait(0.5)
