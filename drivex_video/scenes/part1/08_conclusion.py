from manim import *
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from drivex_video.styles.theme import UCLA_GOLD, DRIVEX_ACCENT

class KeyTakeaways(Scene):
    def construct(self):
        title = Text("Part 1: Key Takeaways", font="Latin Modern Roman", font_size=42, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP)
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.0)
        mascot.to_corner(DR, buff=0.3)

        points = VGroup(
            Text("1. FMs unlock Long-tail Generalization", font="Latin Modern Roman", font_size=24),
            Text("2. MLLMs bring World Knowledge to AV", font="Latin Modern Roman", font_size=24),
            Text("3. Paradigm shift from Rules to Reasoning", font="Latin Modern Roman", font_size=24),
            Text("4. Safety & Latency remain major hurdles", font="Latin Modern Roman", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).center()

        self.play(Write(title))
        self.play(FadeIn(mascot, shift=UP*0.3))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT*0.3) for p in points], lag_ratio=0.5))
        self.wait(4)
        self.play(FadeOut(Group(title, points, mascot)))
        self.wait(0.5)

class FutureDirections(Scene):
    def construct(self):
        title = Text("Future Directions", font="Latin Modern Roman", font_size=42, weight=BOLD).set_color(DRIVEX_ACCENT).to_edge(UP)
        directions = VGroup(
            Text("• Post-training for VLA Alignment", font="Latin Modern Roman", font_size=24),
            Text("• Unified Multimodal Backbones", font="Latin Modern Roman", font_size=24),
            Text("• Efficient Low-latency VLA", font="Latin Modern Roman", font_size=24),
            Text("• Continual Learning from Feedback", font="Latin Modern Roman", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).center()

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(d, shift=UP*0.3) for d in directions], lag_ratio=0.5))
        self.wait(4)
        self.play(FadeOut(Group(title, directions)))
        self.wait(0.5)

class BridgeToPart2(Scene):
    def construct(self):
        mascot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../materials/images/mascot_drivex.png"))
        mascot = ImageMobject(mascot_path).set_height(1.5)
        mascot.center().shift(UP*0.5)
        
        caption = Text("Single agents have a limited view...", font="Latin Modern Roman", font_size=28).next_to(mascot, DOWN)
        
        self.play(FadeIn(mascot, shift=UP*0.3))
        self.play(Write(caption))
        self.wait(2)
        
        next_part = Text("Coming up in PART 2:\nCooperative Perception & Multi-Agent Intelligence", font="Latin Modern Roman", font_size=32, weight=BOLD)
        next_part.set_color(UCLA_GOLD).center()
        
        # Fixed: Changed ReplacementTransform to FadeOut/FadeIn
        self.play(FadeOut(mascot), FadeOut(caption))
        self.play(FadeIn(next_part, shift=UP*0.2))
        self.wait(3)
        self.play(FadeOut(next_part))
        self.wait(1)
