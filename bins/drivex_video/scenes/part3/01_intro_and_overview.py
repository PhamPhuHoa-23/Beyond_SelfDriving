from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class Part3Intro(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title Transition from Part 2
        p2_recap = Text("Part 2 Built the Models", font_size=24, color=GRAY).to_edge(UP, buff=0.8)
        p3_title = Text("PART 3: BRIDGING SIMULATION & REALITY", font_size=36, weight=BOLD, color=UCLA_GOLD).next_to(p2_recap, DOWN, buff=0.5)
        
        self.play(FadeIn(p2_recap, shift=DOWN*0.3))
        self.play(Write(p3_title))
        self.wait(1)
        
        # 2. Add slide image (slide 1)
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_01.png"))).set_width(8)
        slide_img.move_to(DOWN*0.8 + LEFT*2)
        
        self.play(FadeIn(slide_img, scale=0.95))
        self.wait(1.5)
        
        # 3. Mascot Question (Split screen on the right)
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.8).to_corner(DR, buff=0.5)
        self.play(FadeIn(mascot, shift=UP*0.3))
        
        thought = ThoughtBubble(mascot, "Theory is solid.\nBut how do we\ndeploy this on\nactual roads?", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)
        
        self.play(FadeOut(Group(p2_recap, p3_title, slide_img, mascot, thought)))

class FourPillars(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Main Title
        title = Text("4 PILLARS OF REAL-WORLD DEPLOYMENT", font_size=32, weight=BOLD, color=BLUE_A).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Slide 3 (The 4 domains)
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_03.png"))).set_width(7.5)
        slide_img.to_edge(LEFT, buff=0.5)
        
        self.play(FadeIn(slide_img, shift=RIGHT*0.3))
        self.wait(2)

        # 3. Text on the Right
        pillars = VGroup(
            Text("1. Hardware & Setup", font_size=22, color=WHITE),
            Text("2. Map & Localization", font_size=22, color=WHITE),
            Text("3. Late/Intermediate Fusion", font_size=22, color=WHITE),
            Text("4. Digital Twins", font_size=22, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(slide_img, RIGHT, buff=1.0)

        for i, p in enumerate(pillars):
            self.play(FadeIn(p, shift=LEFT*0.3))
            self.wait(0.5)
            
        self.wait(2)
        self.play(FadeOut(Group(title, slide_img, pillars)))
