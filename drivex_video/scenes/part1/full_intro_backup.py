from manim import *
import sys
import os

# Add the root directory to sys.path to import styles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from drivex_video.styles.theme import UCLA_BLUE, UCLA_GOLD, DRIVEX_ACCENT, DriveXStyle

class IntroQuestion(Scene):
    def construct(self):
        # 1. Background
        self.camera.background_color = "#1C1C1C"
        
        # 2. Narration Text (English)
        question = Text(
            "Why is it that in 2025, with all that AI has achieved\n"
            "— coding, art, answering every question —\n"
            "self-driving cars still aren't everywhere?",
            font_size=32,
            line_spacing=1.5,
            t2c={"Why is it that in 2025": UCLA_GOLD}
        )
        
        answer_lead = Text(
            "To answer that, we need to understand where AI stands\nand where autonomous driving stands.",
            font_size=24,
            color=GRAY_B
        ).next_to(question, DOWN, buff=1.0)

        # 3. Animation
        self.play(Write(question), run_time=4)
        self.wait(1)
        self.play(FadeIn(answer_lead, shift=UP*0.3))
        self.wait(2)
        
        self.play(FadeOut(question), FadeOut(answer_lead))
        self.wait(0.5)

class TitleScene(Scene):
    def construct(self):
        # 1. Background and Initial Setup
        self.camera.background_color = "#1C1C1C"
        
        # 2. Creating Text Elements
        title = Text("Beyond Self-Driving", font_size=72, weight=BOLD)
        title.set_color(DRIVEX_ACCENT)
        
        subtitle = Text("Exploring Three Levels of Driving Automation", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.5)
        subtitle.set_color(UCLA_GOLD)
        
        venue = Text("ICCV 2025 Tutorial", font_size=24, slant=ITALIC)
        venue.to_edge(DOWN, buff=1.0)
        venue.set_color(GRAY_B)

        # 3. Animation Sequence
        self.play(Write(title))
        self.wait(0.5)
        
        underline = Underline(title, color=UCLA_GOLD, buff=0.1)
        self.play(
            FadeIn(subtitle, shift=UP*0.3),
            Create(underline),
            run_time=1.5
        )
        self.wait(0.5)
        
        self.play(FadeIn(venue, shift=UP*0.5))
        self.wait(2)
        
        self.play(FadeOut(Group(title, subtitle, underline, venue)), run_time=1)
        self.wait(0.5)

class TransitionToPart1(Scene):
    def construct(self):
        part_num = Text("PART 1", font_size=36, weight=BOLD).set_color(DRIVEX_ACCENT)
        part_title = Text("Foundation Models for Autonomous Driving", font_size=48)
        part_title.next_to(part_num, DOWN, buff=0.3)
        
        group = VGroup(part_num, part_title).center()
        
        self.play(FadeIn(group, shift=RIGHT*0.5))
        self.wait(2)
        self.play(FadeOut(group, shift=LEFT*0.5))
        self.wait(1)

class GenerativeAIBoom(Scene):
    def construct(self):
        # 1. Title
        title = Text("The Generative AI Boom (2023+)", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.5).set_color(DRIVEX_ACCENT)
        
        # 2. Asset Grid Setup (4 Pillars)
        asset_dir = "../../materials/images/part1_new/"
        
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
            
            label = Text(label_text, font_size=16).next_to(img, DOWN, buff=0.15)
            item = Group(img, label)
            items.append(item)
            
        # 2x2 Grid - Tighter buff
        grid = Group(*items).arrange_in_grid(rows=2, buff=0.5)
        grid.next_to(title, DOWN, buff=0.6).shift(DOWN*0.1)

        # 4. Animation Sequence
        self.play(FadeIn(title, shift=DOWN*0.2))
        self.wait(0.5)
        
        # Animate items
        self.play(
            LaggedStart(
                *[FadeIn(item, shift=UP*0.2) for item in items],
                lag_ratio=0.3,
                run_time=2.5
            )
        )
        self.wait(3)

        # Highlight point: "Foundation Models"
        highlight_box = SurroundingRectangle(grid, color=UCLA_GOLD, buff=0.2)
        fm_label = Text("FOUNDATION MODELS", font_size=32, weight=BOLD)
        fm_label.set_color(UCLA_GOLD).next_to(highlight_box, UP, buff=0.2)
        
        self.play(Create(highlight_box), FadeIn(fm_label, shift=DOWN*0.2))
        self.wait(2)
        
        self.play(FadeOut(Group(title, grid, highlight_box, fm_label)))
        self.wait(0.5)

class FoundationModelDiagram(Scene):
    def construct(self):
        # 1. Title
        title = Text("The Foundation Model Paradigm", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # 2. Main Diagram Asset
        asset_dir = "../../materials/images/part1_new/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_new-022.jpg"))
        diagram = ImageMobject(img_path)
        diagram.height = 5.0
        diagram.next_to(title, DOWN, buff=0.5)

        # 3. Transparent Highlight Boxes
        box_data = Rectangle(width=2.8, height=4.5, color=BLUE_A).shift(LEFT*3.8 + DOWN*0.2)
        box_model = Rectangle(width=3.2, height=3.2, color=UCLA_GOLD).shift(ORIGIN + DOWN*0.2)
        box_tasks = Rectangle(width=2.8, height=4.5, color=DRIVEX_ACCENT).shift(RIGHT*3.8 + DOWN*0.2)
        
        # 4. Animation Sequence
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(diagram))
        self.wait(1)

        # Stage 1: Data
        label_data = Text("Stage 1: Massive Multimodal Data", font_size=24, color=BLUE_A).to_edge(BOTTOM, buff=0.8)
        self.play(Create(box_data), FadeIn(label_data, shift=UP*0.2))
        self.play(Indicate(box_data, color=BLUE_A, scale_factor=1.1))
        self.wait(1.5)

        # Stage 2: Model
        label_fm = Text("Stage 2: Foundation Model Training", font_size=24, color=UCLA_GOLD).to_edge(BOTTOM, buff=0.8)
        self.play(
            ReplacementTransform(box_data, box_model),
            ReplacementTransform(label_data, label_fm)
        )
        self.play(Indicate(box_model, color=UCLA_GOLD, scale_factor=1.1))
        self.wait(1.5)

        # Stage 3: Tasks
        label_tasks = Text("Stage 3: Task-Specific Adaptation", font_size=24, color=DRIVEX_ACCENT).to_edge(BOTTOM, buff=0.8)
        self.play(
            ReplacementTransform(box_model, box_tasks),
            ReplacementTransform(label_fm, label_tasks)
        )
        self.play(Indicate(box_tasks, color=DRIVEX_ACCENT, scale_factor=1.1))
        self.wait(1.5)

        self.play(FadeOut(Group(title, diagram, box_tasks, label_tasks)))
        self.wait(0.5)

class AVArchitectures(Scene):
    def construct(self):
        # 1. Title
        title = Text("Three Pillars of AV Architecture", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # 2. Main Diagram Asset
        asset_dir = "../../materials/images/part1/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_s05_arch.png"))
        diagram = ImageMobject(img_path)
        diagram.height = 4.2
        diagram.next_to(title, DOWN, buff=0.8)

        # 3. Pedagogy: English Labels
        labels = Group(
            Text("Modular", font_size=22, color=UCLA_GOLD, weight=BOLD),
            Text("End-to-End", font_size=22, color=UCLA_GOLD, weight=BOLD),
            Text("Hybrid", font_size=22, color=UCLA_GOLD, weight=BOLD)
        )
        labels.arrange(RIGHT, buff=2.3).next_to(diagram, UP, buff=0.1)

        # 4. Animation Sequence
        self.play(Write(title))
        self.play(FadeIn(diagram, shift=UP*0.2))
        self.play(FadeIn(labels, shift=DOWN*0.1))
        self.wait(1.5)

        # Highlight boxes for the diagram columns
        box_mod = Rectangle(width=2.5, height=3.5, color=BLUE_A).shift(LEFT*3.5 + DOWN*0.5)
        box_e2e = Rectangle(width=2.5, height=3.5, color=DRIVEX_ACCENT).shift(ORIGIN + DOWN*0.5)
        
        # Highlight Modular
        lab_mod = Text("Current Standard", font_size=16, color=BLUE_A).next_to(box_mod, UP)
        self.play(Create(box_mod), FadeIn(lab_mod))
        self.play(Indicate(box_mod, color=BLUE_A))
        self.wait(1.5)
        
        # Highlight E2E
        lab_e2e = Text("Future Generalization", font_size=16, color=DRIVEX_ACCENT).next_to(box_e2e, UP)
        self.play(
            ReplacementTransform(box_mod, box_e2e),
            ReplacementTransform(lab_mod, lab_e2e)
        )
        self.play(Indicate(box_e2e, color=DRIVEX_ACCENT))
        self.wait(2)

        self.play(FadeOut(Group(title, diagram, labels, box_e2e, lab_e2e)))
        self.wait(0.5)

class CornerCases(Scene):
    def construct(self):
        # 1. Title
        title = Text("The 'Long Tail' Challenge", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # 2. Main Diagram Asset
        asset_dir = "../../materials/images/part1/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_s06_corner_cases.png"))
        diagram = ImageMobject(img_path)
        diagram.height = 4.5
        diagram.next_to(title, DOWN, buff=0.5)

        # 3. Transparent Highlighting
        tail_box = Rectangle(width=3.5, height=2.0, color=ORANGE).shift(RIGHT*2.5 + DOWN*0.5)
        label = Text("Infinite Corner Cases", font_size=20, color=ORANGE).next_to(tail_box, UP)

        # 4. Animation Sequence
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(diagram))
        self.wait(1)

        self.play(Create(tail_box), Write(label))
        self.play(Indicate(tail_box, color=ORANGE))
        self.wait(2)
        
        self.play(FadeOut(Group(title, diagram, tail_box, label)))
        self.wait(0.5)

class WhyFoundationModels(Scene):
    def construct(self):
        # 1. Title
        title = Text("Why Foundation Models for AV?", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # 2. Main Diagram Asset
        asset_dir = "../../materials/images/part1/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_s07_why_fm.png"))
        diagram = ImageMobject(img_path)
        diagram.height = 4.5
        diagram.next_to(title, DOWN, buff=0.5)

        # 3. Three Pillars
        pillars = VGroup(
            Text("Generalization", font_size=22, color=UCLA_GOLD, weight=BOLD),
            Text("Reasoning", font_size=22, color=UCLA_GOLD, weight=BOLD),
            Text("World Modeling", font_size=22, color=UCLA_GOLD, weight=BOLD)
        )
        pillars.arrange(RIGHT, buff=1.2).next_to(diagram, UP, buff=0.2)

        # 4. Animation Sequence
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(diagram, shift=UP*0.3))
        self.play(Write(pillars))
        self.wait(2)
        
        # Highlight Reasoning
        reason_box = SurroundingRectangle(pillars[1], color=UCLA_GOLD)
        self.play(Create(reason_box))
        self.play(Indicate(pillars[1]))
        self.wait(1.5)

        self.play(FadeOut(Group(title, diagram, pillars, reason_box)))
        self.wait(0.5)

class ScalingLaws(Scene):
    def construct(self):
        # 1. Title
        title = Text("The Power of Scaling", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4).set_color(DRIVEX_ACCENT)
        
        # 2. Scaling Laws Diagram (Slide 9)
        asset_dir = "../../materials/images/part1/"
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), asset_dir + "p1_s09_scaling.png"))
        diagram = ImageMobject(img_path)
        diagram.height = 4.5
        diagram.next_to(title, DOWN, buff=0.5)

        # 3. Annotation
        trend_line = Line(start=LEFT*2 + DOWN*1, end=RIGHT*2 + UP*1, color=UCLA_GOLD).set_stroke(width=6)
        trend_label = Text("Predictable Performance Gain", font_size=20, color=UCLA_GOLD).next_to(trend_line, UP)

        # 4. Animation Sequence
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(diagram))
        self.wait(1)
        
        self.play(Create(trend_line), Write(trend_label))
        self.play(Indicate(trend_line))
        self.wait(2)
        
        self.play(FadeOut(Group(title, diagram, trend_line, trend_label)))
        self.wait(0.5)

class Part1Summary(Scene):
    def construct(self):
        title = Text("Part 1 Summary", font_size=48, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP)
        
        points = VGroup(
            Text("• FM is the 'Base Model' for downstream tasks", font_size=28),
            Text("• Scaling predictable performance gains", font_size=28),
            Text("• Transition from Modular to E2E Foundation systems", font_size=28),
            Text("• Solving 'Long Tail' corner cases with reasoning", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).center()
        
        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT*0.3) for p in points], lag_ratio=0.5))
        self.wait(4)
        self.play(FadeOut(Group(title, points)))
        self.wait(1)
