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
        title = Text("SENSOR CALIBRATION", font_size=32, weight=BOLD, color=UCLA_GOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Slide 17 Image
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_17.png"))).set_width(12)
        slide_img.next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(slide_img, scale=0.9))
        self.wait(1.5)

        # 3. Time & Space Concept
        box_time = VGroup(
            Text("TIME SYNC", font_size=24, color=BLUE_A, weight=BOLD),
            Text("GPS as Time Reference\nHardware Triggers (No Jitter)", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT)

        box_space = VGroup(
            Text("SPACE SYNC", font_size=24, color=BLUE_A, weight=BOLD),
            Text("Intrinsic & Extrinsic Calibration\nPrevents 'Ghost Objects'", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT)

        concepts = VGroup(box_time, box_space).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.5)
        bg_concepts = BackgroundRectangle(concepts, color=BLACK, fill_opacity=0.8, buff=0.2)
        
        self.play(FadeIn(bg_concepts), FadeIn(concepts, shift=UP*0.3))
        self.wait(2)

        # 4. Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.8).to_corner(DR, buff=0.5)
        self.play(FadeIn(mascot, shift=UP*0.3))

        thought = ThoughtBubble(mascot, "Data from different sensors\nmust align perfectly in time and space.", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3)

        self.play(FadeOut(Group(title, slide_img, bg_concepts, concepts, mascot, thought)))

