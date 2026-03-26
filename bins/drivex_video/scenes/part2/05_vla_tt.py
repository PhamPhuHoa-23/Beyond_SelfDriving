from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class V2XPnP_Framework(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title
        title = Text("V2XPnP: SPATIO-TEMPORAL FUSION", font="Latin Modern Roman", font_size=32, weight=BOLD, color=DRIVEX_ACCENT).to_edge(UP, buff=0.8)
        self.play(Write(title))

        # 2. Main Architecture Diagram (p2_s06_related_works_v_research_gaps_019.png)
        # This is the correct cooperation paradigm diagram
        asset_dir = "../../../materials/images/part2/"
        arch_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s06_related_works_v_research_gaps_019.png"))
        arch_img = ImageMobject(arch_path).set_width(12)
        arch_img.shift(UP*0.5)
        
        frame = RoundedRectangle(corner_radius=0.1, width=12.2, height=arch_img.height + 0.3, 
                                 stroke_color=UCLA_GOLD, stroke_width=1, fill_opacity=0.03).move_to(arch_img.get_center())
        
        self.play(FadeIn(frame, scale=0.9), FadeIn(arch_img, scale=0.9))
        self.wait(1.5)

        # 3. Key Concepts (Positioned to NOT overlap the center diagram)
        concepts = VGroup(
            Text("WHAT: 3 Fusion Schemes", font="Latin Modern Roman", font_size=22, color=BLUE_A),
            Text("WHEN: One-Step Flow", font="Latin Modern Roman", font_size=22, color=BLUE_A),
            Text("HOW: Spatial-Temporal Fusion", font="Latin Modern Roman", font_size=22, color=BLUE_A)
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=1.2)

        self.play(FadeIn(concepts, shift=UP*0.3))
        self.wait(1)

        # 4. Mascot Interjection (Bottom corner, no overlap)
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.4).to_corner(DR, buff=0.2)
        self.play(FadeIn(mascot, shift=UP*0.2))
        
        thought = ThoughtBubble(mascot, "Fusing history in one shot\nbeats frame-by-frame lag.", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)

        self.play(FadeOut(Group(title, arch_img, frame, concepts, mascot, thought)))

class TurboTrain(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title
        title = Text("TURBOTRAIN: SOLVING GRADIENT CONFLICTS", font="Latin Modern Roman", font_size=32, weight=BOLD, color=DRIVEX_ACCENT).to_edge(UP, buff=0.8)
        self.play(Write(title))

        # 2. Results Chart (p2_s16_turbotrain_iccv_2025_037.png)
        asset_dir = "../../../materials/images/part2/"
        chart_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s16_turbotrain_iccv_2025_037.png"))
        chart = ImageMobject(chart_path).set_height(4.0)
        chart.to_edge(RIGHT, buff=0.8).shift(UP*0.3)
        
        self.play(FadeIn(chart, shift=LEFT*0.3))
        self.wait(1)

        # 3. Training Paradigm (p2_s17_slide_041.png - Pretraining)
        pretrain_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s17_slide_041.png"))
        pretrain_img = ImageMobject(pretrain_path).set_width(5.0)
        pretrain_img.to_edge(LEFT, buff=0.8).shift(UP*0.3)
        
        p_label = Text("Stage 1: Pretrain-then-Balance", font="Latin Modern Roman", font_size=22, color=UCLA_GOLD).next_to(pretrain_img, UP)

        self.play(FadeIn(pretrain_img, shift=RIGHT*0.3), Write(p_label))
        self.wait(2)

        # 4. Efficiency Stats (Bottom, center)
        efficiency = VGroup(
            Text("• 45 Epochs vs 120 Epochs", font="Latin Modern Roman", font_size=22, color=GREEN),
            Text("• No Human Tuning Needed", font="Latin Modern Roman", font_size=22, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=1.0)

        self.play(FadeIn(efficiency, shift=UP*0.3))
        self.wait(3)

        self.play(FadeOut(Group(title, chart, pretrain_img, p_label, efficiency)))
