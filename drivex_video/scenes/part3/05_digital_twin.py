from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class DigitalTwin(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Main Title
        title = Text("CLOSING THE LOOP: DIGITAL TWIN", font_size=32, weight=BOLD, color=BLUE_A).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Add slide 50 
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_50.png"))).set_width(7.5)
        slide_img.to_edge(LEFT, buff=0.5)

        self.play(FadeIn(slide_img, shift=RIGHT*0.3))
        self.wait(1.5)

        # 3. Text on the right
        features = VGroup(
            Text("OpenCDA-ROS", font_size=20, weight=BOLD, color=UCLA_GOLD),
            Text("• Connects Simulation with Real", font_size=16),
            Text("• ROS Middleware streaming", font_size=16),
            Text(" ", font_size=10),
            Text("CDA-SimBoost", font_size=20, weight=BOLD, color=UCLA_GOLD),
            Text("• Generates edge cases (rain, fail)", font_size=16),
            Text("• Exposes models to challenges", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(slide_img, RIGHT, buff=0.5)

        bg_box = BackgroundRectangle(features, color=BLACK, fill_opacity=0.8, buff=0.2)
        features_group = VGroup(bg_box, features)

        self.play(FadeIn(features_group, shift=LEFT*0.3))
        self.wait(3.5)

        self.play(FadeOut(Group(title, slide_img, features_group)))


class Part3Conclusion(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Summary Title
        title = Text("PART 3 SUMMARY: ENGINEERING THE PIPELINE", font_size=32, weight=BOLD, color=UCLA_GOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Pillars
        pillars = VGroup(
            Text("1. Hardware Node & V2X Data Collection", font_size=20),
            Text("2. Time/Space Calibration & EKF Localization", font_size=20),
            Text("3. CooperFuse & V2X-ReaLO Fusions", font_size=20),
            Text("4. OpenCDA-ROS Digital Twin Simulation", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP*0.5)

        for pillar in pillars:
            self.play(FadeIn(pillar, shift=RIGHT*0.3))
            self.wait(0.5)

        self.wait(1)

        # 3. Transition to Part 4
        bridge = VGroup(
            Text("But annotation is costly and edge computation is limited.", font_size=16, color=GRAY),
            Text("NEXT: TACKLING DATA AND EFFICIENCY BOTTLENECKS...", font_size=20, slant=ITALIC, color=BLUE_A)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.8)

        self.play(Write(bridge))
        self.play(Indicate(bridge[1]))
        self.wait(3.5)

        self.play(FadeOut(Group(title, pillars, bridge)))
