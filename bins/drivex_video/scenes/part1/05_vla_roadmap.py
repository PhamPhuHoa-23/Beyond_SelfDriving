from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT

class FoundationEmpowerment(Scene):
    def construct(self):
        title = Text("Foundation Models empower AV", font="Latin Modern Roman", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.0)
        mascot.to_corner(DR, buff=0.3)

        asset_dir = "../../../materials/images/part1/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_s07_why_fm.png"))
        diagram = ImageMobject(img_path)
        diagram.height = 4.5
        diagram.next_to(title, DOWN, buff=0.4)

        text_bubble = Text("Not replacing,\nbut empowering!", font="Latin Modern Roman", font_size=22, color=UCLA_GOLD).next_to(mascot, UP)

        self.play(Write(title))
        self.play(FadeIn(diagram, shift=UP*0.2))
        self.play(FadeIn(mascot, shift=LEFT))
        self.play(Write(text_bubble))
        self.wait(2)
        
        self.play(FadeOut(Group(title, diagram, mascot, text_bubble)))
        self.wait(0.5)

class VLARoadmap(Scene):
    def construct(self):
        title = Text("The VLA Roadmap for AV", font="Latin Modern Roman", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        asset_dir = "../../../materials/images/part1_new/"
        # New roadmap image: p1_new-049.jpg
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_new-049.jpg"))
        diagram = ImageMobject(img_path)
        diagram.set_height(4.0)
        diagram.next_to(title, DOWN, buff=0.5)

        categories = VGroup(
            Text("1. Text Actions", font="Latin Modern Roman", font_size=22),
            Text("2. Numerical Actions", font="Latin Modern Roman", font_size=22),
            Text("3. Explicit Guidance", font="Latin Modern Roman", font_size=22),
            Text("4. Implicit Transfer", font="Latin Modern Roman", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=1.0)

        self.play(Write(title))
        self.play(FadeIn(diagram))
        self.wait(1)
        
        for cat in categories:
            self.play(FadeIn(cat, shift=RIGHT*0.2))
            self.wait(0.5)
            
        self.wait(2)
        self.play(FadeOut(Group(title, diagram, categories)))
        self.wait(0.5)

class VLADatasets(Scene):
    def construct(self):
        title = Text("New Generation of AV Datasets", font="Latin Modern Roman", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        asset_dir = "../../../materials/images/part1_new/"
        # Dataset visual: p1_new-073.jpg
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_new-073.jpg"))
        visual = ImageMobject(img_path)
        visual.set_height(4.0)
        visual.center().shift(RIGHT*2)

        datasets = VGroup(
            Text("• DriveLM (Graph Reasoning)", font="Latin Modern Roman", font_size=24),
            Text("• CoVLA (Video-Language)", font="Latin Modern Roman", font_size=24),
            Text("• Impromptu VLA (Real Scenarios)", font="Latin Modern Roman", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).to_edge(LEFT, buff=1.5)

        self.play(Write(title))
        self.play(FadeIn(visual, shift=LEFT*0.3))
        self.play(LaggedStart(*[FadeIn(d, shift=UP*0.3) for d in datasets], lag_ratio=0.5))
        self.wait(3)
        self.play(FadeOut(Group(title, datasets, visual)))
        self.wait(0.5)
