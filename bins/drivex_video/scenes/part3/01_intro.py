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
        p2_recap = Text("Part 2 Built the Models", font_size=24, color=GRAY).to_edge(UP, buff=1.0)
        p3_title = Text("PART 3: BRIDGING SIMULATION AND REALITY", font_size=36, weight=BOLD, color=UCLA_GOLD).next_to(p2_recap, DOWN, buff=0.5)
        
        self.play(FadeIn(p2_recap, shift=DOWN*0.3))
        self.play(Write(p3_title))
        self.wait(1)
        
        # 2. Add slide image (slide 1)
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_01.png"))).set_width(10)
        slide_img.move_to(DOWN*0.5)
        
        self.play(FadeIn(slide_img, scale=0.95))
        self.wait(2)
        
        # 3. Mascot Question
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.8).to_corner(DR, buff=0.5)
        self.play(FadeIn(mascot, shift=UP*0.3))
        
        thought = ThoughtBubble(mascot, "Theory is solid. But where does\nthe data come from?", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)
        
        self.play(FadeOut(Group(p2_recap, p3_title, slide_img, mascot, thought)))

class UCLAIntersection(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title
        title = Text("UCLA SMART INTERSECTION", font_size=32, weight=BOLD, color=BLUE_A).to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # 2. Slide 6 Image
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_06.png"))).set_width(12)
        slide_img.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(slide_img, shift=UP*0.3))
        self.wait(2)

        # 3. Key Concepts Box
        hardware_list = VGroup(
            Text("• 2 Infrastructure Nodes (LiDAR, Cameras)", font_size=16, color=WHITE),
            Text("• 2 Connected Automated Vehicles (GNSS/IMU)", font_size=16, color=WHITE),
            Text("• Redundancy is key for reliability", font_size=16, color=UCLA_GOLD)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)

        bg_box = BackgroundRectangle(hardware_list, color=BLACK, fill_opacity=0.8, buff=0.2)
        hardware_group = VGroup(bg_box, hardware_list)

        self.play(FadeIn(hardware_group, shift=UP*0.3))
        self.wait(3)

        self.play(FadeOut(Group(title, slide_img, hardware_group)))
