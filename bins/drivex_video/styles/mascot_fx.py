from manim import *
import numpy as np

class ThoughtBubble(VGroup):
    """
    3Blue1Brown-style speech bubble:
    - Dark fill (#111111) with white border
    - White text, pointed triangular tail toward mascot
    """
    def __init__(self, target, text, position=UP+RIGHT, **kwargs):
        super().__init__(**kwargs)

        # White text on dark background
        self.text = Text(text, font="Latin Modern Roman", font_size=28, color=WHITE)

        # Bubble sizing
        px, py = 0.6, 0.45
        w = max(self.text.width + px * 2, 3.5)
        h = max(self.text.height + py * 2, 1.8)

        # Dark rounded rectangle with white border
        self.bubble = RoundedRectangle(
            corner_radius=0.3,
            width=w,
            height=h,
            fill_color="#111111",
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=2.5,
        )

        # Place text inside bubble
        bubble_group = VGroup(self.bubble, self.text)
        self.text.move_to(self.bubble.get_center())

        # Position bubble next to mascot
        offset = 0.7
        bubble_group.next_to(target, position, buff=offset)

        # Triangular pointed tail from bubble edge toward mascot
        tip = target.get_top() + position * 0.2   # near mascot mouth area
        anchor = self.bubble.get_corner(-position) # bubble corner facing mascot

        # Perpendicular vector for tail width
        direction = tip - anchor
        length = np.linalg.norm(direction)
        if length > 0:
            d_norm = direction / length
        else:
            d_norm = np.array([1, 0, 0])
        perp = np.array([-d_norm[1], d_norm[0], 0]) * 0.18

        tail = Polygon(
            anchor + perp,
            anchor - perp,
            tip,
            fill_color="#111111",
            fill_opacity=1.0,
            stroke_color=WHITE,
            stroke_width=2.5,
        )

        # Draw: tail first (behind bubble), then bubble + text on top
        self.add(tail, bubble_group)
        self.tail_shape = tail
        self.main_bubble = self.bubble
        self.main_text = self.text

    def get_pop_animation(self):
        """Clean pop-in animation."""
        return LaggedStart(
            GrowFromCenter(self[0]),    # tail
            GrowFromCenter(self[1][0]), # bubble
            Write(self[1][1]),          # text
            lag_ratio=0.2,
        )
