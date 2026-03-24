from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class SensorCalibration(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Main Title
        title = Text("CALIBRATION: TIME & SPACE", font_size=32, weight=BOLD, color=UCLA_GOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Add slide 12 (Time Sync)
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_12.png"))).set_width(7.5)
        slide_img.to_edge(LEFT, buff=0.5)
        
        self.play(FadeIn(slide_img, shift=RIGHT*0.3))
        self.wait(2)

        # 3. Text on the right
        bullets = VGroup(
            Text("TIME SYNCHRONIZATION", font_size=20, weight=BOLD, color=BLUE_A),
            Text("• Global GPS Time Reference", font_size=16),
            Text("• Hardware triggers (no jitter)", font_size=16),
            Text(" ", font_size=10),
            Text("SPACE SYNCHRONIZATION", font_size=20, weight=BOLD, color=BLUE_A),
            Text("• Intrinsic & Extrinsic matrix", font_size=16),
            Text("• Prevents \"Ghost Objects\"", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(slide_img, RIGHT, buff=0.8)

        bg_box = BackgroundRectangle(bullets, color=BLACK, fill_opacity=0.8, buff=0.2)
        bullets_group = VGroup(bg_box, bullets)

        self.play(FadeIn(bullets_group, shift=LEFT*0.3))
        self.wait(2)

        # Transition to Space Sync Slide (17)
        slide_17 = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_17.png"))).set_width(7.5)
        slide_17.to_edge(LEFT, buff=0.5)
        self.play(FadeOut(slide_img), FadeIn(slide_17, shift=UP*0.3))
        self.wait(2.5)

        self.play(FadeOut(Group(title, slide_17, bullets_group)))

class MapLocalization(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Main Title
        title = Text("HD MAP & LOCALIZATION", font_size=32, weight=BOLD, color=BLUE_A).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Slide 28 Image (Localization ghost effect)
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_28.png"))).set_width(8.0)
        slide_img.move_to(DOWN*0.8 + LEFT*1.5)
        
        self.play(FadeIn(slide_img, scale=0.9))
        self.wait(1.5)

        # 3. Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.8).to_corner(DR, buff=0.5)
        self.play(FadeIn(mascot, shift=UP*0.3))

        thought = ThoughtBubble(mascot, "Bad localization makes\ncooperation worse than\nsingle-agent driving!", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)

        # Transition to Kalman Filter Solution Text
        problem_text = Text("SOLUTION: MULTI-RATE EKF", font_size=18, color=GREEN).next_to(mascot, DOWN, buff=1.0)
        self.play(Write(problem_text))
        self.wait(2)

        self.play(FadeOut(Group(title, slide_img, mascot, thought, problem_text)))
