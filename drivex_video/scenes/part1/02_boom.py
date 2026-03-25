from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A

class GenerativeAIBoom(Scene):
    def construct(self):
        title = Text("The Generative AI Boom (2023+)", font="Latin Modern Roman", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.5).set_color(DRIVEX_ACCENT)
        
        # Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.2)
        mascot.to_corner(DR, buff=0.3)

        asset_dir = "../../../materials/images/part1_new/"
        assets_data = [
            ("p1_new-013.jpg", "Coding & Chat"),
            ("p1_new-014.jpg", "Reasoning"),
            ("p1_new-015.jpg", "Image / Video"),
            ("p1_new-016.jpg", "3D World Models")
        ]
        items = []
        for img_name, label_text in assets_data:
            img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + img_name))
            img = ImageMobject(img_path)
            img.height = 2.0
            label = Text(label_text, font="Latin Modern Roman", font_size=22).next_to(img, DOWN, buff=0.15)
            item = Group(img, label)
            items.append(item)
            
        grid = Group(*items).arrange_in_grid(rows=2, buff=0.5)
        grid.next_to(title, DOWN, buff=0.6).shift(DOWN*0.1)

        self.play(FadeIn(title, shift=DOWN*0.2))
        self.play(FadeIn(mascot, shift=UP*0.3))
        self.wait(0.5)
        
        self.play(LaggedStart(*[FadeIn(item, shift=UP*0.2) for item in items], lag_ratio=0.3, run_time=2.5))
        self.wait(2)
        
        highlight_box = SurroundingRectangle(grid, color=UCLA_GOLD, buff=0.2)
        fm_label = Text("FOUNDATION MODELS", font="Latin Modern Roman", font_size=32, weight=BOLD).set_color(UCLA_GOLD).next_to(highlight_box, UP, buff=0.2)
        
        self.play(Create(highlight_box), FadeIn(fm_label, shift=DOWN*0.2))
        self.play(Indicate(mascot)) # Mascot react
        self.wait(2)
        
        self.play(FadeOut(Group(title, grid, highlight_box, fm_label, mascot)))
        self.wait(0.5)

class FoundationModelParadigm(Scene):
    def construct(self):
        title = Text("The Foundation Model Paradigm", font="Latin Modern Roman", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        asset_dir = "../../../materials/images/part1_new/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_new-022.jpg"))
        diagram = ImageMobject(img_path)
        diagram.height = 5.0
        diagram.next_to(title, DOWN, buff=0.5)

        box_data = Rectangle(width=2.8, height=4.5, color=BLUE_A).shift(LEFT*3.8 + DOWN*0.2)
        box_model = Rectangle(width=3.2, height=3.2, color=UCLA_GOLD).shift(ORIGIN + DOWN*0.2)
        box_tasks = Rectangle(width=2.8, height=4.5, color=DRIVEX_ACCENT).shift(RIGHT*3.8 + DOWN*0.2)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(diagram))
        self.wait(1)
        
        label_data = Text("Stage 1: Massive Multimodal Data", font="Latin Modern Roman", font_size=24, color=BLUE_A).to_edge(DOWN, buff=0.8)
        self.play(Create(box_data), FadeIn(label_data, shift=UP*0.2))
        self.play(Indicate(box_data, color=BLUE_A))
        self.wait(1)
        
        label_fm = Text("Stage 2: Foundation Model Training", font="Latin Modern Roman", font_size=24, color=UCLA_GOLD).to_edge(DOWN, buff=0.8)
        self.play(ReplacementTransform(box_data, box_model), ReplacementTransform(label_data, label_fm))
        self.play(Indicate(box_model, color=UCLA_GOLD))
        self.wait(1.5)
        
        label_tasks = Text("Stage 3: Task-Specific Adaptation", font="Latin Modern Roman", font_size=24, color=DRIVEX_ACCENT).to_edge(DOWN, buff=0.8)
        self.play(ReplacementTransform(box_model, box_tasks), ReplacementTransform(label_fm, label_tasks))
        self.play(Indicate(box_tasks, color=DRIVEX_ACCENT))
        self.wait(2)
        
        self.play(FadeOut(Group(title, diagram, box_tasks, label_tasks)))
        self.wait(0.5)
