from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class IntersectionSetup(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Title
        title = Text("UCLA SMART INTERSECTION", font_size=32, weight=BOLD, color=UCLA_GOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Add slide 6 and 11
        asset_dir = "../../../materials/images/part3_slides/"
        slide_06 = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_06.png"))).set_width(7.5)
        slide_11 = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_11.png"))).set_width(7.5)
        
        # Position them Left
        slide_06.to_edge(LEFT, buff=0.5)
        slide_11.to_edge(LEFT, buff=0.5)

        self.play(FadeIn(slide_06, shift=RIGHT*0.3))
        self.wait(1.5)

        # 3. Text on the right
        hardware = VGroup(
            Text("NOT A SIMULATION!", font_size=20, weight=BOLD, color=RED),
            Text("2 Infrastructure Nodes:", font_size=18, color=UCLA_GOLD),
            Text(" • LiDAR 128/64 + C-V2X", font_size=16),
            Text("2 CAV Vehicles:", font_size=18, color=UCLA_GOLD),
            Text(" • Stereo cameras + LiDAR 128", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(slide_06, RIGHT, buff=0.6)

        bg_box = BackgroundRectangle(hardware, color=BLACK, fill_opacity=0.8, buff=0.2)
        hardware_group = VGroup(bg_box, hardware)

        self.play(FadeIn(hardware_group, shift=LEFT*0.3))
        self.wait(2.5)

        # Switch to Slide 11 (Hardware closer look)
        self.play(FadeOut(slide_06), FadeIn(slide_11, shift=UP*0.3))
        self.wait(2.5)

        self.play(FadeOut(Group(title, slide_11, hardware_group)))

class DataCollection(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Main Title
        title = Text("SYSTEMATIC DATA COLLECTION", font_size=32, weight=BOLD, color=BLUE_A).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Add slide 18
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_18.png"))).set_width(8.0)
        slide_img.move_to(DOWN*0.8 + LEFT*1.5)
        
        self.play(FadeIn(slide_img, scale=0.9))
        self.wait(1.5)

        # 3. Mascot on right
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(2.0).next_to(slide_img, RIGHT, buff=1.0)
        self.play(FadeIn(mascot, shift=UP*0.3))

        thought = ThoughtBubble(mascot, "We don't just drive\nrandomly. We design\nspecific routes and\ntime combos.", position=UP+RIGHT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)

        self.play(FadeOut(Group(title, slide_img, mascot, thought)))
