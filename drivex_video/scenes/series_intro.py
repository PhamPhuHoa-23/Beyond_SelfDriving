from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT, BLUE_A

class SeriesStoryIntro(Scene):
    def construct(self):
        self.camera.background_color = "#1C1C1C"
        
        # Mascot Setup
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(2.0)
        mascot.to_corner(DR, buff=0.5)

        # 1. The Question
        story_1 = Text("We gave cars eyes to see...", font_size=36, slant=ITALIC).center()
        story_2 = Text("...and Foundation Models to reason.", font_size=36, slant=ITALIC).center()
        
        self.play(Write(story_1))
        self.wait(1)
        self.play(ReplacementTransform(story_1, story_2))
        self.wait(1)
        
        # 2. The Conflict (Single Agent limits)
        story_3 = Text("But even the smartest agent\ncannot see through walls.", font_size=32, weight=BOLD)
        story_3.set_color(RED_A).center()
        
        self.play(FadeOut(story_2), FadeIn(story_3, shift=UP*0.3))
        self.wait(1.5)
        
        # 3. The Resolution (Cooperation)
        story_4 = Text("So we taught them to cooperate.", font_size=36, weight=BOLD)
        story_4.set_color(DRIVEX_ACCENT).center()
        
        self.play(ReplacementTransform(story_3, story_4))
        self.play(FadeIn(mascot, shift=LEFT))
        self.wait(1)

        # 4. The 5-Part Journey Intro
        title = Text("DriveX: The 5-Part Journey", font_size=42, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP, buff=0.5)
        self.play(ReplacementTransform(story_4, title))
        
        parts = VGroup(
            Text("1. Individual Reasoning (Foundation Models)", font_size=22),
            Text("2. Collective Intelligence (Cooperative V2X)", font_size=22),
            Text("3. The Sim-to-Real Bridge", font_size=22),
            Text("4. Efficiency & Online Adaptation", font_size=22),
            Text("5. Scalable Human-Centric Physical AI", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).center().shift(RIGHT*0.5)

        for i, part in enumerate(parts):
            bullet = Dot(color=UCLA_GOLD).next_to(part, LEFT, buff=0.3)
            self.play(Create(bullet), FadeIn(part, shift=RIGHT*0.2))
            self.wait(0.5)

        final_lead = Text("ICCV 2025 Tutorial", font_size=20, color=GRAY_B).next_to(parts, DOWN, buff=0.8)
        self.play(FadeIn(final_lead, shift=UP*0.2))
        self.play(Indicate(mascot))
        self.wait(3)
        
        self.play(FadeOut(Group(title, parts, final_lead, mascot)))
        self.wait(1)
