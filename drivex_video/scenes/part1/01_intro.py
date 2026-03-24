from manim import *
import sys
import os

# Add the root directory to sys.path to import styles
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT

class IntroQuestion(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        
        # Mascot Setup
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.5)
        mascot.to_corner(DR, buff=0.5)

        question = Text(
            "Why is it that in 2025, with all that AI has achieved\n"
            "— coding, art, answering every question —\n"
            "self-driving cars still aren't everywhere?",
            font_size=32, line_spacing=1.5,
            t2c={"Why is it that in 2025": UCLA_GOLD}
        )
        
        answer_lead = Text(
            "To answer that, we need to understand where AI stands\nand where autonomous driving stands.",
            font_size=24, color=GRAY_B
        ).next_to(question, DOWN, buff=1.0)

        # Mascot animation: Slide in and "wave" (subtle shift)
        self.play(Write(question), run_time=4)
        self.play(FadeIn(mascot, shift=LEFT), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(answer_lead, shift=UP*0.3))
        self.wait(2)
        
        self.play(FadeOut(question), FadeOut(answer_lead), FadeOut(mascot))
        self.wait(0.5)

class IntroOutline(Scene):
    def construct(self):
        title = Text("The Three-Step Journey", font_size=42, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP)
        
        # Mascot
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.5)
        mascot.to_corner(UL, buff=0.5)

        steps = VGroup(
            Text("1. Overview (AI & AV Today)", font_size=32),
            Text("2. The Bridge (Current Research)", font_size=32),
            Text("3. The Future (Challenges & Roadmap)", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).center().shift(RIGHT*0.5)

        self.play(Write(title))
        self.play(FadeIn(mascot, shift=RIGHT))
        self.wait(0.5)
        
        for step in steps:
            self.play(FadeIn(step, shift=UP*0.2))
            self.wait(1)
            
        self.wait(2)
        self.play(FadeOut(Group(title, mascot, steps)))
        self.wait(1)

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
