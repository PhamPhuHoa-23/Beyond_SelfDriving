from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT

class VLAArchitectures(Scene):
    def construct(self):
        title = Text("State-of-the-Art VLA Architectures", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.0)
        mascot.to_corner(DR, buff=0.3)

        asset_dir = "../../../materials/images/part1_new/"
        # VLA detailed diagram (e.g. EMMA logic): p1_new-143.jpg
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_new-143.jpg"))
        diagram = ImageMobject(img_path)
        diagram.set_height(4.0)
        diagram.next_to(title, DOWN, buff=0.5)

        arch_list = VGroup(
            Text("GPT-Driver: Zero-shot Planning", font_size=20),
            Text("BEVDriver: 3D Aware Reasoning", font_size=20),
            Text("EMMA: Multimodal End-to-End", font_size=20),
            Text("DriveVLM: Hybrid Dual-System", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(diagram))
        self.play(FadeIn(mascot, shift=LEFT))
        self.wait(1)
        
        for arch in arch_list:
            self.play(FadeIn(arch, shift=RIGHT*0.2))
            self.play(Indicate(mascot))
            self.wait(1)
            
        self.wait(3)
        self.play(FadeOut(Group(title, diagram, arch_list, mascot)))
        self.wait(0.5)

class ArchitectureComparison(Scene):
    def construct(self):
        title = Text("Which Paradigm Wins?", font_size=42, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP)
        asset_dir = "../../../materials/images/part1_new/"
        # Comparison grid: p1_new-080.jpg
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_new-080.jpg"))
        diagram = ImageMobject(img_path)
        diagram.set_height(4.5)
        diagram.center().shift(DOWN*0.5)
        
        self.play(Write(title))
        self.play(FadeIn(diagram, shift=UP*0.3))
        self.wait(4)
        self.play(FadeOut(Group(title, diagram)))
        self.wait(0.5)
