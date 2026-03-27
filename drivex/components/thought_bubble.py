# drivex/components/thought_bubble.py
# ─────────────────────────────────────────────────────────────────
# Speech / thought bubble components.
# ThoughtBubble  — rounded speech bubble with pointed tail.
# SpeechBubble   — alias with thicker border (for CAR mascot quotes).
# ─────────────────────────────────────────────────────────────────

from manim import *
import numpy as np

from .colors import COL_NAVY, COL_BLUE, COL_WHITE, COL_GOLD


class ThoughtBubble(VGroup):
    """
    3B1B-style speech bubble.
    - Dark fill with colored border
    - Pointed triangular tail toward target mobject

    Parameters
    ----------
    target      : Mobject the tail points toward
    text        : string inside bubble
    position    : direction to place bubble (e.g. UP+RIGHT)
    font_size   : text size inside bubble
    fill_color  : bubble background color
    border_color: bubble border color
    text_color  : text color
    buff        : gap between target and bubble
    """

    def __init__(
        self,
        target: Mobject,
        text: str,
        position=UP + RIGHT,
        font_size: int = 24,
        fill_color: str = "#111111",
        border_color: str = COL_WHITE,
        text_color: str = COL_WHITE,
        buff: float = 0.65,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.label = Text(text, font_size=font_size, color=text_color)

        pad_x, pad_y = 0.5, 0.35
        bw = max(self.label.width + pad_x * 2.0, 3.2)
        bh = max(self.label.height + pad_y * 2.0, 1.5)

        bubble = RoundedRectangle(
            corner_radius=0.28,
            width=bw, height=bh,
            fill_color=fill_color, fill_opacity=1.0,
            stroke_color=border_color, stroke_width=2.5,
        )
        self.label.move_to(bubble.get_center())
        bubble_grp = VGroup(bubble, self.label)
        bubble_grp.next_to(target, position, buff=buff)

        # Triangular tail
        tip = target.get_critical_point(
            position) * 0.5 + target.get_center() * 0.5
        anchor = bubble.get_corner(-position)
        direction = tip - anchor
        length = np.linalg.norm(direction)
        d_norm = direction / length if length > 0 else np.array([1, 0, 0])
        perp = np.array([-d_norm[1], d_norm[0], 0]) * 0.14

        tail = Polygon(
            anchor + perp,
            anchor - perp,
            tip,
            fill_color=fill_color, fill_opacity=1.0,
            stroke_color=border_color, stroke_width=2.5,
        )

        self.main_bubble = bubble
        self.tail_shape = tail
        self.add(tail, bubble_grp)

    def get_pop_animation(self, lag: float = 0.15):
        """Pop-in animation: tail → bubble → text."""
        return LaggedStart(
            GrowFromCenter(self.tail_shape),
            GrowFromCenter(self.main_bubble),
            Write(self.label),
            lag_ratio=lag,
        )


# Convenience subclass with blue border (for PI mascot)
class PIBubble(ThoughtBubble):
    def __init__(self, target, text, **kw):
        kw.setdefault("border_color", COL_BLUE)
        kw.setdefault("fill_color", "#0D1B2E")
        kw.setdefault("text_color", COL_WHITE)
        super().__init__(target, text, **kw)


# Alias for direct speech (CAR mascot)
class SpeechBubble(ThoughtBubble):
    def __init__(self, target, text, **kw):
        kw.setdefault("border_color", COL_GOLD)
        kw.setdefault("fill_color", "#1A1200")
        kw.setdefault("text_color", COL_GOLD)
        super().__init__(target, text, **kw)
