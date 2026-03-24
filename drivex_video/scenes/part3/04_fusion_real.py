from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class LateFusion(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Main Title
        title = Text("COOPERFUSE: LATE FUSION", font_size=32, weight=BOLD, color=BLUE_A).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Add slide 33
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_33.png"))).set_width(7.5)
        slide_img.to_edge(LEFT, buff=0.5)

        self.play(FadeIn(slide_img, shift=RIGHT*0.3))
        self.wait(1.5)

        # 3. Text on the right
        bullets = VGroup(
            Text("PROBLEM WITH NMS:", font_size=20, weight=BOLD, color=RED),
            Text("Confidence scores ignore\nphysical properties.", font_size=16),
            Text(" ", font_size=10),
            Text("COOPERFUSE INSIGHT:", font_size=20, weight=BOLD, color=UCLA_GOLD),
            Text("Fuse using temporal\nfeatures (XYZ, orientation)", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(slide_img, RIGHT, buff=0.8)

        bg_box = BackgroundRectangle(bullets, color=BLACK, fill_opacity=0.8, buff=0.2)
        bullets_group = VGroup(bg_box, bullets)

        self.play(FadeIn(bullets_group, shift=LEFT*0.3))
        self.wait(2.5)

        self.play(FadeOut(Group(title, slide_img, bullets_group)))


class IntermediateFusion(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        # 1. Main Title
        title = Text("V2X-ReaLO: INTERMEDIATE FUSION", font_size=32, weight=BOLD, color=UCLA_GOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 2. Slide 44 Image
        asset_dir = "../../../materials/images/part3_slides/"
        slide_img = ImageMobject(os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p3_slide_44.png"))).set_width(8.0)
        slide_img.move_to(DOWN*0.5 + LEFT*1.5)

        self.play(FadeIn(slide_img, scale=0.9))
        self.wait(1.5)

        # 3. Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(2.0).next_to(slide_img, RIGHT, buff=1.0)
        self.play(FadeIn(mascot, shift=UP*0.3))

        thought = ThoughtBubble(mascot, "0.5MB per message working\npoint. 32x BEV compression\nfor real-time V2X!", position=UP+RIGHT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)

        self.play(FadeOut(Group(title, slide_img, mascot, thought)))
