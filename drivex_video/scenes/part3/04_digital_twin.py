from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class DigitalTwin(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Title
        title = Text("CLOSING THE LOOP: DIGITAL TWIN", font_size=32, weight=BOLD, color=UCLA_GOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Slide 50 Image (OpenCDA-ROS & CDA-SimBoost)
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_50.png"))).set_width(12)
        slide_img.next_to(title, DOWN, buff=0.2)
        
        self.play(FadeIn(slide_img, scale=0.9))
        self.wait(2)

        # 3. Features
        features = VGroup(
            Text("✔ OpenCDA-ROS (Middleware)", font_size=18, color=WHITE),
            Text("✔ CDA-SimBoost (Simulation)", font_size=18, color=WHITE),
            Text("Generate edge-cases from real data", font_size=16, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)

        bg_box = BackgroundRectangle(features, color=BLACK, fill_opacity=0.8, buff=0.2)
        bg_features = VGroup(bg_box, features)

        self.play(FadeIn(bg_features, shift=UP*0.3))
        self.wait(2)

        self.play(FadeOut(Group(title, slide_img, bg_features)))

class Part3Conclusion(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Summary Title
        title = Text("PART 3 SUMMARY: ENGINEERING THE PIPELINE", font_size=32, weight=BOLD, color=BLUE_A).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Pillars
        pillars = VGroup(
            Text("1. Hardware Node & V2X Sync", font_size=20),
            Text("2. Calibration & EKF Localization", font_size=20),
            Text("3. CooperFuse & V2X-ReaLO Data Fusions", font_size=20),
            Text("4. Digital Twins & CARLA Simulation", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP*0.5)

        for pillar in pillars:
            self.play(FadeIn(pillar, shift=RIGHT*0.3))
            self.wait(0.5)

        self.wait(1)

        # 3. Transition to Part 4
        bridge = Text("NEXT: TACKLING DATA AND EFFICIENCY BOTTLENECKS...", font_size=18, slant=ITALIC, color=UCLA_GOLD).to_edge(DOWN, buff=0.8)
        self.play(Write(bridge))
        self.play(Indicate(bridge))
        self.wait(3.5)

        self.play(FadeOut(Group(title, pillars, bridge)))
