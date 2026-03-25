from manim import *

class ThoughtBubble(VGroup):
    def __init__(self, target, text, position=UP+LEFT, **kwargs):
        super().__init__(**kwargs)
        
        # Premium Styling: Rounded corners
        self.text = Text(text, font="Georgia", font_size=24, color="#1C1C1C")
        
        # Calculate padding based on text
        padding = 0.6
        w = max(self.text.width + padding, 3.0)
        h = max(self.text.height + padding, 1.6)
        
        # Premium Bubble
        self.bubble = RoundedRectangle(
            corner_radius=0.4, 
            width=w, 
            height=h, 
            fill_color=WHITE, 
            fill_opacity=1.0, # solid white is cleaner
            stroke_color="#CCCCCC", 
            stroke_width=2
        )
        
        # Tail: Three circles with decreasing size
        c1 = Circle(radius=0.12, fill_color=WHITE, fill_opacity=1.0, stroke_width=0.5).set_color(GRAY_B)
        c2 = Circle(radius=0.08, fill_color=WHITE, fill_opacity=1.0, stroke_width=0.5).set_color(GRAY_C)
        c3 = Circle(radius=0.05, fill_color=WHITE, fill_opacity=1.0, stroke_width=0.5).set_color(GRAY_C)
        
        # ASSEMBLE the bubble and text first to move them together
        bubble_with_text = VGroup(self.bubble, self.text)
        self.text.move_to(self.bubble.get_center())
        
        # Positioning relative to target (usually mascot)
        offset = 0.8
        bubble_with_text.next_to(target, position, buff=offset)
        
        # Circles lead from target corner to bubble
        start_point = target.get_corner(position)
        end_point = self.bubble.get_corner(-position)
        
        c1.move_to(start_point + position * 0.15)
        c3.move_to(end_point - position * 0.15)
        c2.move_to(interpolate(c1.get_center(), c3.get_center(), 0.5))
        
        self.add(c1, c2, c3, bubble_with_text)
        # Store references for animations
        self.tail = VGroup(c1, c2, c3)
        self.main_bubble = self.bubble
        self.main_text = self.text

    def get_pop_animation(self):
        """Returns a stable entry animation where text follows bubble."""
        return LaggedStart(
            FadeIn(self.tail[0], scale=0.5),
            FadeIn(self.tail[1], scale=0.5),
            FadeIn(self.tail[2], scale=0.5),
            GrowFromCenter(self[3][0]), # Grow bubble
            Write(self[3][1]),          # Write text
            lag_ratio=0.1
        )
