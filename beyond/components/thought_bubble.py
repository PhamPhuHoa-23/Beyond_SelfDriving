# beyond/components/thought_bubble.py
# ─────────────────────────────────────────────────────────────────
# Speech / thought bubble components — v2 rewrite.
#
# Two main classes:
#   CalloutBubble  — rounded rect + smooth bezier tail (no seam)
#   ThoughtBubble  — classic cloud: chain of circles → main ellipse
#
# Key technique for seamless tail (learned from Manim VMobject API):
#   Build tail as an OPEN VMobject path (no close_path call).
#   SVG fill closes the area implicitly — no stroke on the seam edge.
#   Rect body sits on top, covering any artifacts.
# ─────────────────────────────────────────────────────────────────

from __future__ import annotations
import numpy as np
from manim import *
from .colors import (
    TEXT_WHITE, TEXT_DIM, CYAN_NEON, GOLD,
    BG_PANEL, BLUE_ELECTRIC,
    SIZE_LABEL, FONT_PRIMARY,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Geometry helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _norm(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    return v / n if n > 1e-8 else np.array([1.0, 0.0, 0.0])


def _perp2d(v: np.ndarray) -> np.ndarray:
    """2-D perpendicular (CCW rotation 90°), z=0."""
    return np.array([-v[1], v[0], 0.0])


def _attachment_info(body: RoundedRectangle, position) -> tuple:
    """
    Returns (p1, p2, edge_dir) where p1/p2 are the two attachment
    points of the tail on the bubble edge, edge_dir is the tangent
    direction along that edge (RIGHT or UP).

    The edge chosen is the one facing *toward* the target
    (i.e. opposite to the `position` direction).
    """
    pos = np.array(position, dtype=float)
    px, py = pos[0], pos[1]
    cx, cy = body.get_center()[0], body.get_center()[1]
    hw = body.width / 2
    hh = body.height / 2
    tail_hw = 0.13   # half-width of tail base (in Manim units)

    if abs(py) >= abs(px):
        # Vertical dominant → use horizontal edge
        ey = cy - np.sign(py) * hh        # bottom edge if bubble above
        # Shift attachment point horizontally toward the mascot
        shift_x = np.clip(-px * hw * 0.35, -hw + 0.28, hw - 0.28)
        ac = cx + shift_x
        p1 = np.array([ac - tail_hw, ey, 0.0])
        p2 = np.array([ac + tail_hw, ey, 0.0])
        edge_dir = np.array([1.0, 0.0, 0.0])   # RIGHT
    else:
        # Horizontal dominant → use vertical edge
        ex = cx - np.sign(px) * hw        # left edge if bubble to the right
        shift_y = np.clip(-py * hh * 0.35, -hh + 0.25, hh - 0.25)
        ac = cy + shift_y
        p1 = np.array([ex, ac - tail_hw, 0.0])
        p2 = np.array([ex, ac + tail_hw, 0.0])
        edge_dir = np.array([0.0, 1.0, 0.0])   # UP

    return p1, p2, edge_dir


def _bezier_tail(
    p1: np.ndarray,
    p2: np.ndarray,
    tip: np.ndarray,
    fill_color: str,
    border_color: str,
    border_width: float,
) -> VMobject:
    """
    Build an OPEN VMobject path:  p1 →(bezier)→ tip →(bezier)→ p2
    No close_path() call → no stroke on the seam edge.
    The fill still covers the enclosed area (SVG implicit closure).

    Both bezier sides use tangent-continuous control points that give
    a gentle inward curve (slightly concave sides — comic/speech look).
    """
    mid = (p1 + p2) * 0.5
    d = tip - mid
    d_len = np.linalg.norm(d)
    if d_len < 1e-6:
        d_len = 0.5
    dn = d / d_len                  # unit direction to tip
    pull = 0.18                     # inward pull factor (makes sides concave)

    # "Inward" vectors: for each attachment, direction toward the midpoint
    inward_1 = _norm(mid - p1)
    inward_2 = _norm(mid - p2)

    strength = max(d_len * 0.52, 0.20)

    # Control points
    ctrl1 = p1 + dn * strength + inward_1 * pull
    ctrl2 = tip + (mid - tip) * 0.12    # arrive near tip, slight pull to mid
    ctrl3 = tip + (mid - tip) * 0.12    # symmetric departure from tip
    ctrl4 = p2 + dn * strength + inward_2 * pull

    tail = VMobject(
        fill_color=fill_color, fill_opacity=1.0,
        stroke_color=border_color, stroke_width=border_width,
    )
    tail.start_new_path(p1)
    tail.add_cubic_bezier_curve_to(ctrl1, ctrl2, tip)
    tail.add_cubic_bezier_curve_to(ctrl3, ctrl4, p2)
    # Intentionally NOT calling close_path() — seam gets no stroke

    return tail


def _shadow(body: RoundedRectangle, offset: float = 0.055, opacity: float = 0.18) -> VMobject:
    """Subtle drop shadow — a darker copy offset down-right."""
    s = body.copy()
    s.set_fill("#000000", opacity).set_stroke(width=0)
    s.shift(np.array([offset, -offset, 0]))
    return s


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CalloutBubble — the main class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CalloutBubble(VGroup):
    """
    Speech bubble with a smooth bezier tail — no visible seam.

    Parameters
    ----------
    target       : Mobject the tail points toward
    text         : displayed string (multi-line supported with \\n)
    position     : direction from target to place the bubble (default UP+RIGHT)
    font_size    : text size
    fill_color   : bubble background
    border_color : stroke color
    text_color   : label color
    pad_x, pad_y : horizontal / vertical padding around text
    buff         : gap between target edge and bubble
    corner_radius: roundness of bubble corners
    drop_shadow  : add a subtle drop shadow
    border_width : stroke weight
    """

    def __init__(
        self,
        target: Mobject,
        text: str,
        position=UP + RIGHT,
        font_size: int = None,
        fill_color: str = BG_PANEL,
        border_color: str = CYAN_NEON,
        text_color: str = TEXT_WHITE,
        pad_x: float = 0.35,
        pad_y: float = 0.22,
        buff: float = 0.50,
        corner_radius: float = 0.22,
        drop_shadow: bool = True,
        border_width: float = 1.5,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if font_size is None:
            font_size = SIZE_LABEL

        # ── Label ─────────────────────────────────────────────────
        self.label = Text(
            text, font_size=font_size, color=text_color,
            font=FONT_PRIMARY, line_spacing=0.42,
        )

        # ── Body ──────────────────────────────────────────────────
        bw = max(self.label.width + pad_x * 2, 0.6)
        bh = max(self.label.height + pad_y * 2, 0.45)

        self.main_body = RoundedRectangle(
            corner_radius=corner_radius,
            width=bw, height=bh,
            fill_color=fill_color, fill_opacity=1.0,
            stroke_color=border_color, stroke_width=border_width,
        )
        self.label.move_to(self.main_body)
        bubble_grp = VGroup(self.main_body, self.label)
        bubble_grp.next_to(target, position, buff=buff)

        # ── Tail ──────────────────────────────────────────────────
        # Tip: a point on the target, slightly inside (not the very edge)
        tip = (
            target.get_critical_point(position) * 0.55
            + target.get_center() * 0.45
        )
        p1, p2, _ = _attachment_info(self.main_body, position)

        self.tail_shape = _bezier_tail(p1, p2, tip,
                                       fill_color, border_color, border_width)

        # ── Seam cap ──────────────────────────────────────────────
        # A thick stroke at the attachment line, colored like fill.
        # This covers any partial rendering artifacts at the edge seam.
        seam = Line(
            p1, p2,
            stroke_color=fill_color,
            stroke_width=border_width * 3.5,
        )

        # ── Inner highlight (top edge arc) ────────────────────────
        # Very subtle white arc at the top — suggests 3-D roundness.
        hl_w = min(bw * 0.55, bw - corner_radius * 2)
        hl_center = self.main_body.get_center() + UP * (bh * 0.28)
        highlight = Line(
            hl_center + LEFT * hl_w * 0.5,
            hl_center + RIGHT * hl_w * 0.5,
            stroke_color=WHITE, stroke_width=0.8, stroke_opacity=0.15,
        )

        # ── Layer order ───────────────────────────────────────────
        # shadow → tail → seam cap → body → label → highlight
        if drop_shadow:
            self.add(_shadow(self.main_body))
        self.add(self.tail_shape, seam, self.main_body, self.label, highlight)

    # ── Animations ────────────────────────────────────────────────

    def pop_in(self) -> Succession:
        """Bubble materializes from the tail tip outward."""
        return Succession(
            FadeIn(self.tail_shape, scale=0.85, run_time=0.18),
            GrowFromCenter(self.main_body, run_time=0.24),
            FadeIn(self.label, run_time=0.18),
        )

    def pop_out(self, run_time: float = 0.22) -> FadeOut:
        return FadeOut(self, run_time=run_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ThoughtBubble — cloud style (thinking, not speaking)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ThoughtBubble(VGroup):
    """
    Classic thought bubble: a chain of 3 circles → main ellipse body.

    Use this when PI is *thinking* (uncertain, hypothetical).
    Use CalloutBubble when PI is *speaking* (asserting a question).
    """

    def __init__(
        self,
        target: Mobject,
        text: str,
        position=UP + RIGHT,
        font_size: int = None,
        fill_color: str = BG_PANEL,
        border_color: str = CYAN_NEON,
        text_color: str = TEXT_WHITE,
        pad_x: float = 0.35,
        pad_y: float = 0.22,
        buff: float = 0.55,
        border_width: float = 1.3,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if font_size is None:
            font_size = SIZE_LABEL

        self.label = Text(
            text, font_size=font_size, color=text_color,
            font=FONT_PRIMARY, line_spacing=0.42,
        )
        bw = max(self.label.width + pad_x * 2, 0.6)
        bh = max(self.label.height + pad_y * 2, 0.45)

        # Main ellipse body (slightly wider than tall for softer look)
        self.main_body = RoundedRectangle(
            corner_radius=min(bh * 0.48, 0.38),
            width=bw, height=bh,
            fill_color=fill_color, fill_opacity=1.0,
            stroke_color=border_color, stroke_width=border_width,
        )
        self.label.move_to(self.main_body)
        bubble_grp = VGroup(self.main_body, self.label)
        bubble_grp.next_to(target, position, buff=buff)

        # Chain of 3 circles from target → bubble
        target_pt = (
            target.get_critical_point(position) * 0.6
            + target.get_center() * 0.4
        )
        bubble_pt = self.main_body.get_critical_point(-position)
        chain_dir = _norm(bubble_pt - target_pt)

        chain_sizes = [0.06, 0.09, 0.13]  # radii, increasing toward bubble
        chain_circles = VGroup()
        for i, r in enumerate(chain_sizes):
            t = (i + 1) / (len(chain_sizes) + 1)
            center = target_pt + chain_dir * np.linalg.norm(bubble_pt - target_pt) * t
            c = Circle(
                radius=r,
                fill_color=fill_color, fill_opacity=1.0,
                stroke_color=border_color, stroke_width=border_width,
            ).move_to(center)
            chain_circles.add(c)

        self.chain = chain_circles
        self.add(_shadow(self.main_body), chain_circles, bubble_grp)

    def pop_in(self) -> LaggedStart:
        return LaggedStart(
            *[GrowFromCenter(c, run_time=0.12) for c in self.chain],
            GrowFromCenter(self.main_body, run_time=0.22),
            FadeIn(self.label, run_time=0.18),
            lag_ratio=0.25,
        )

    def pop_out(self, run_time: float = 0.22) -> FadeOut:
        return FadeOut(self, run_time=run_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Backward-compat alias + typed wrappers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TightBubble = CalloutBubble   # alias for import compatibility


class PIBubble(CalloutBubble):
    """Callout bubble styled for PI mascot (curious questioner)."""
    _DARK_FILL  = "#071222"
    _LIGHT_FILL = "#DBEAFE"

    def __init__(self, target, text, dark_theme: bool = True, **kw):
        kw.setdefault("fill_color",   self._DARK_FILL if dark_theme else self._LIGHT_FILL)
        kw.setdefault("border_color", BLUE_ELECTRIC)
        kw.setdefault("text_color",   TEXT_WHITE)
        super().__init__(target, text, **kw)


class SpeechBubble(CalloutBubble):
    """Callout bubble styled for CAR mascot (narrator)."""
    _DARK_FILL  = "#12100A"
    _LIGHT_FILL = "#FEF3C7"

    def __init__(self, target, text, dark_theme: bool = True, **kw):
        kw.setdefault("fill_color",   self._DARK_FILL if dark_theme else self._LIGHT_FILL)
        kw.setdefault("border_color", GOLD)
        kw.setdefault("text_color",   TEXT_WHITE)
        super().__init__(target, text, **kw)
