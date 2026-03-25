from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A
from drivex_video.styles.mascot_fx import ThoughtBubble

class RiskMap_Planning(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Title
        title = Text("RISKMAP: INTERPRETABLE PLANNING", font="Latin Modern Roman", font_size=32, weight=BOLD, color=DRIVEX_ACCENT).to_edge(UP, buff=0.8)
        self.play(Write(title))

        # 2. RiskMap Diagram (p2_s23_riskmap_054.png)
        asset_dir = "../../../materials/images/part2/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s23_riskmap_054.png"))
        risk_img = ImageMobject(img_path).set_width(12)
        risk_img.shift(DOWN*0.5)
        
        frame = RoundedRectangle(corner_radius=0.1, width=12.2, height=risk_img.height + 0.3, 
                                 stroke_color=BLUE_A, stroke_width=1, fill_opacity=0.03).move_to(risk_img.get_center())
        
        self.play(FadeIn(frame, scale=0.9), FadeIn(risk_img, scale=0.9))
        self.wait(1.5)

        # 3. Features Sidebar (Positioned to NOT overlap the center diagram)
        features = VGroup(
            Text("THE MIDDLEWARE", font="Latin Modern Roman", font_size=22, weight=BOLD, color=UCLA_GOLD),
            Text("✔ Explicit Risk Map", font="Latin Modern Roman", font_size=22),
            Text("✔ Safe Trajectories", font="Latin Modern Roman", font_size=22),
            Text("✔ Traceable Logic", font="Latin Modern Roman", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=0.8).shift(UP*0.5)

        self.play(FadeIn(features, shift=RIGHT*0.3))
        self.wait(1.5)

        # 4. Mascot Interjection
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.6).to_corner(DR, buff=0.3)
        self.play(FadeIn(mascot, shift=UP*0.3))
        
        thought = ThoughtBubble(mascot, "AI perceives, the RiskMap\nvalidates the path.", position=UP+LEFT)
        self.play(thought.get_pop_animation())
        self.wait(3.5)
        
        self.play(FadeOut(Group(title, risk_img, frame, features, mascot, thought)))

class Part2Conclusion(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # 1. Summary Image (p2_s26_summary_060.png)
        asset_dir = "../../../materials/images/part2/"
        summary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p2_s26_summary_060.png"))
        summary_img = ImageMobject(summary_path).set_height(4.0).shift(UP*0.3)
        
        title = Text("PART 2 SUMMARY: COOPERATIVE AUTOMATION", font="Latin Modern Roman", font_size=32, weight=BOLD, color=DRIVEX_ACCENT).next_to(summary_img, UP, buff=0.5)
        
        self.play(FadeIn(summary_img, scale=0.9), Write(title))
        self.wait(1.5)

        # 2. Pillars
        pillars = VGroup(
            Text("• Foundations: V2XPnP (AISTATS 2024)", font="Latin Modern Roman", font_size=22),
            Text("• Performance: TurboTrain (ICCV 2025)", font="Latin Modern Roman", font_size=22),
            Text("• Logic: RiskMap (Proposed Middleware)", font="Latin Modern Roman", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=1.0).shift(DOWN*1.0)
        
        self.play(LaggedStart(*[FadeIn(p, shift=UP*0.2) for p in pillars], lag_ratio=0.5))
        self.wait(2.5)
        
        # 3. Final Bridge
        bridge = Text("NEXT: BRIDGING SENSORS TO REAL WORLD ROADS...", font="Latin Modern Roman", font_size=22, color=UCLA_GOLD).to_edge(DOWN, buff=0.8)
        self.play(Write(bridge))
        self.play(Indicate(bridge))
        self.wait(4)

        self.play(FadeOut(Group(title, summary_img, pillars, bridge)))
