from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class MapLocalization(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Main Title
        title = Text("WHY LOCALIZATION?", font_size=32, weight=BOLD, color=UCLA_GOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Slide 28 Image (Localization ghost effect)
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_28.png"))).set_width(12)
        slide_img.next_to(title, DOWN, buff=0.2)
        
        self.play(FadeIn(slide_img, scale=0.9))
        self.wait(1.5)

        # 3. Problem & Solution
        problem_text = Text("❌ Bad Pose = Fusion Ghost Effect", font_size=16, color=RED)
        solution_text = Text("✔ Multi-rate EKF: GNSS (5Hz) + IMU/Wheel (100Hz) + LiDAR (1Hz)", font_size=16, color=GREEN)
        
        box = VGroup(problem_text, solution_text).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
        bg_box = BackgroundRectangle(box, color=BLACK, fill_opacity=0.8, buff=0.2)
        
        self.play(FadeIn(bg_box), FadeIn(box, shift=UP*0.3))
        self.wait(2)

        # 4. Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.8).to_corner(DL, buff=0.5)
        self.play(FadeIn(mascot, shift=UP*0.3))

        thought = ThoughtBubble(mascot, "Bad localization makes cooperation\nworse than single-agent driving!", position=UP+RIGHT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)

        self.play(FadeOut(Group(title, slide_img, bg_box, box, mascot, thought)))

class LateVsIntermediate(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Title
        title = Text("LATE VS INTERMEDIATE FUSION", font_size=32, weight=BOLD, color=BLUE_A).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Add slide 33
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_33.png"))).set_width(12)
        slide_img.next_to(title, DOWN, buff=0.2)
        
        self.play(FadeIn(slide_img, scale=0.9))
        self.wait(2)
        self.play(FadeOut(slide_img))

        # 3. Add slide 44
        slide_44 = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_44.png"))).set_width(12)
        slide_44.next_to(title, DOWN, buff=0.2)
        
        self.play(FadeIn(slide_44, scale=0.9))
        self.wait(2)

        # 4. Keys
        key_list = VGroup(
            Text("CooperFuse: Late Fusion, Temporal Features instead of NMS", font_size=16, color=UCLA_GOLD),
            Text("V2X-ReaLO: Intermediate, 0.5MB limit for Real-World V2X", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)

        bg_box = BackgroundRectangle(key_list, color=BLACK, fill_opacity=0.8, buff=0.2)
        
        self.play(FadeIn(bg_box), FadeIn(key_list, shift=UP*0.3))
        self.wait(3)

        self.play(FadeOut(Group(title, slide_44, bg_box, key_list)))
