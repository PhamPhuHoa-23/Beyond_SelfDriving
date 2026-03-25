from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class BackgroundStats(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title
        title = Text("PART 2: TOWARDS COOPERATIVE AUTOMATION", font="Latin Modern Roman", font_size=32, color=DRIVEX_ACCENT).to_edge(UP, buff=0.8)
        
        # 2. Stats vs Image Layout
        # Left side: Stats
        stats = VGroup(
            VGroup(Text("1.19M", font="Latin Modern Roman", color=RED, weight=BOLD), Text("Traffic deaths/year", font="Latin Modern Roman", font_size=22)).arrange(DOWN, aligned_edge=LEFT),
            VGroup(Text("94%", font="Latin Modern Roman", color=RED, weight=BOLD), Text("Human error", font="Latin Modern Roman", font_size=22)).arrange(DOWN, aligned_edge=LEFT),
            VGroup(Text("80%", font="Latin Modern Roman", color=GREEN, weight=BOLD), Text("Safety gain (AI)", font="Latin Modern Roman", font_size=22)).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).to_edge(LEFT, buff=1.0)

        # Right side: Image (Delivery Robots - p2_s03_slide_003.png)
        asset_dir = "../../../materials/images/part2/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s03_slide_003.png"))
        img = ImageMobject(img_path).set_height(4.0).to_edge(RIGHT, buff=0.8)
        
        caption = Text("Logistics Robots (Future of Delivery)", font="Latin Modern Roman", font_size=22, color=UCLA_GOLD).next_to(img, DOWN)

        self.play(Write(title))
        self.play(FadeIn(stats, shift=RIGHT*0.3), FadeIn(img, shift=LEFT*0.3), Write(caption))
        self.wait(2)

        # Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.6).to_corner(DR, buff=0.3)
        self.play(FadeIn(mascot, shift=UP*0.2))
        
        thought = ThoughtBubble(mascot, "Can individual robots\nsolve complex traffic?", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3)
        
        self.play(FadeOut(Group(title, stats, img, caption, mascot, thought)))
