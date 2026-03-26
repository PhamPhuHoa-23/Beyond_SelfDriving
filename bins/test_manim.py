from manim import *

class HelloWorld(Scene):
    def construct(self):
        # Create text
        text = Text("Hello, Manim!", font_size=72)
        # Create math formula to test LaTeX
        math = MathTex(r"e^{i\pi} + 1 = 0")
        math.next_to(text, DOWN)

        # Animations
        self.play(Write(text))
        self.wait(1)
        self.play(Write(math))
        self.wait(2)
        self.play(FadeOut(text), FadeOut(math))
