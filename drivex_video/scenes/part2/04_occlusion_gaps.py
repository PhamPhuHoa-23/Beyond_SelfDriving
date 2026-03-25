from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class OcclusionProblem(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title Section
        title = Text("PHYSICAL LIMITS: THE OCCLUSION WALL", font="Latin Modern Roman", font_size=32, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP, buff=0.8)
        self.play(Write(title))

        # 2. LiDAR Matrix (p2_s05_gii_hn_ca_single_agent_occlusion_011.png)
        asset_dir = "../../../materials/images/part2/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s05_gii_hn_ca_single_agent_occlusion_011.png"))
        lidar_img = ImageMobject(img_path).set_width(11)
        lidar_img.shift(DOWN*0.3)
        
        # Labels for the matrix
        single_agent_label = Text("SINGLE-AGENT (BLIND SCARS)", font="Latin Modern Roman", font_size=22, color=RED).to_edge(UP, buff=1.8).align_to(lidar_img, LEFT).shift(RIGHT*1.0)
        multi_agent_label = Text("MULTI-AGENT (CLEAR VISION)", font="Latin Modern Roman", font_size=22, color=GREEN).to_edge(DOWN, buff=1.5).align_to(lidar_img, LEFT).shift(RIGHT*1.0)
        
        self.play(FadeIn(lidar_img, scale=0.9))
        self.play(Write(single_agent_label), Write(multi_agent_label))
        self.wait(2)

        # Mascot interjection from bottom corner
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.5).to_corner(DR, buff=0.3)
        self.play(FadeIn(mascot, shift=UP*0.3))
        
        thought = ThoughtBubble(mascot, "Physics limits perception.\nSharing limits physics.", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)
        
        self.play(FadeOut(Group(title, lidar_img, single_agent_label, multi_agent_label, mascot, thought)))
        self.wait(0.5)

class ResearchGaps(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title Section
        title = Text("CRITICAL RESEARCH GAPS", font="Latin Modern Roman", font_size=32, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP, buff=0.8)
        self.play(Write(title))

        # 2. Gap Diagram (p2_s09_research_gap_single_frame_multi_frame_multi_task_027.png)
        asset_dir = "../../../materials/images/part2/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s09_research_gap_single_frame_multi_frame_multi_task_027.png"))
        gap_img = ImageMobject(img_path).set_height(5.5)
        gap_img.shift(DOWN*0.5)
        
        self.play(FadeIn(gap_img, scale=0.9))
        self.wait(1.5)

        # 3. Callout Boxes
        gap1 = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.0, 
                                fill_color=WHITE, fill_opacity=0.1, stroke_width=1, stroke_color=UCLA_GOLD)
        gap1.to_edge(LEFT, buff=0.5).shift(UP*1.0)
        g1_text = VGroup(Text("GAP 1", font="Latin Modern Roman", font_size=22, weight=BOLD), Text("Single-Frame vs Temporal", font="Latin Modern Roman", font_size=22)).arrange(DOWN, aligned_edge=LEFT).move_to(gap1.get_center())
        
        gap2 = gap1.copy().shift(DOWN*2.5)
        g2_text = VGroup(Text("GAP 2", font="Latin Modern Roman", font_size=22, weight=BOLD), Text("Decoupled vs End-to-End", font="Latin Modern Roman", font_size=22)).arrange(DOWN, aligned_edge=LEFT).move_to(gap2.get_center())

        self.play(Create(gap1), Write(g1_text))
        self.wait(1)
        self.play(Create(gap2), Write(g2_text))
        self.wait(3.5)

        self.play(FadeOut(Group(title, gap_img, gap1, gap2, g1_text, g2_text)))
        self.wait(0.5)
