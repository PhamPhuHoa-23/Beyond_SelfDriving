"""P02-S08 - Three questions."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_CARD,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    PASTEL_AMBER,
    PASTEL_BLUE,
    PASTEL_TEAL,
    PURPLE_MODEL,
    SIZE_CAPS,
    SIZE_LABEL,
    SIZE_MICRO,
    v2x_link,
    vehicle_icon,
)
from studio.scenes.part02._p02_helpers import attention_arcs, feature_row


SCRIPT = "Three questions: what to transmit, when to transmit, how to fuse."


def _label(text: str, *, size: int = SIZE_LABEL, color: str = INK_DARK, weight=None) -> Text:
    kwargs = {"font": FONT_PRIMARY, "font_size": size, "color": color}
    if weight is not None:
        kwargs["weight"] = weight
    return Text(text, **kwargs)


def _payload_visual() -> VGroup:
    lidar = VGroup(
        Dot(LEFT * 0.38, radius=0.065, color=ACCENT_TEAL),
        Dot(LEFT * 0.13 + UP * 0.1, radius=0.065, color=ACCENT_TEAL),
        Dot(RIGHT * 0.13 + DOWN * 0.08, radius=0.065, color=ACCENT_TEAL),
        Dot(RIGHT * 0.38 + UP * 0.03, radius=0.065, color=ACCENT_TEAL),
    )
    box = Rectangle(width=0.78, height=0.36, stroke_color=GOLD_RICH, stroke_width=2.3)
    box.move_to(RIGHT * 1.05)
    bev = feature_row(n=6, color=ACCENT_BLUE, width=1.08, height=0.26).move_to(RIGHT * 2.18)
    captions = VGroup(
        _label("LiDAR", size=SIZE_MICRO, color=INK_MID),
        _label("boxes", size=SIZE_MICRO, color=INK_MID),
        _label("BEV", size=SIZE_MICRO, color=INK_MID),
    )
    for cap, mob in zip(captions, [lidar, box, bev]):
        cap.next_to(mob, DOWN, buff=0.08)
    group = VGroup(lidar, box, bev, captions)
    group.move_to(ORIGIN)
    return group


def _window_visual() -> VGroup:
    car_a = vehicle_icon(color=ACCENT_BLUE, scale=0.52).move_to(LEFT * 0.86)
    car_b = vehicle_icon(color=GREEN_FIX, scale=0.52).move_to(RIGHT * 0.86)
    link, _ = v2x_link(car_a, car_b, color=GREEN_FIX)
    link.set_stroke(width=3.0, opacity=0.88)
    window = Line(LEFT * 1.34 + DOWN * 0.5, RIGHT * 1.34 + DOWN * 0.5, stroke_color=GOLD_RICH, stroke_width=3.2)
    ticks = VGroup(
        Line(UP * 0.09, DOWN * 0.09, stroke_color=GOLD_RICH, stroke_width=2.0).move_to(window.get_start()),
        Line(UP * 0.09, DOWN * 0.09, stroke_color=GOLD_RICH, stroke_width=2.0).move_to(window.get_end()),
    )
    caption = _label("contact window", size=SIZE_MICRO, color=INK_MID).next_to(window, DOWN, buff=0.08)
    return VGroup(link, car_a, car_b, window, ticks, caption)


def _attention_visual() -> VGroup:
    nodes = VGroup(
        Dot(LEFT * 0.84 + DOWN * 0.06, radius=0.105, color=PURPLE_MODEL),
        Dot(LEFT * 0.28 + UP * 0.19, radius=0.105, color=GOLD_RICH),
        Dot(RIGHT * 0.28 + DOWN * 0.19, radius=0.105, color=ACCENT_TEAL),
        Dot(RIGHT * 0.84 + UP * 0.06, radius=0.105, color=GREEN_FIX),
    )
    arcs = attention_arcs(nodes, color=PURPLE_MODEL)
    arcs.set_stroke(width=2.2, opacity=0.78)
    caption = _label("temporal + spatial", size=SIZE_MICRO, color=INK_MID).next_to(nodes, DOWN, buff=0.28)
    return VGroup(arcs, nodes, caption)


def _question_card(title: str, body: str, visual: Mobject, *, stroke: str, fill: str) -> VGroup:
    rect = RoundedRectangle(
        width=3.55,
        height=2.08,
        corner_radius=0.14,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_color=stroke,
        stroke_width=2.4,
    )
    title_mob = _label(title, size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
    body_mob = _label(body, size=SIZE_CAPS, color=INK_MID)
    title_mob.move_to(rect.get_top() + DOWN * 0.35)
    body_mob.move_to(rect.get_top() + DOWN * 0.7)
    visual.set_max_width(2.9)
    visual.set_max_height(0.94)
    visual.move_to(rect.get_center() + DOWN * 0.46)
    return VGroup(rect, title_mob, body_mob, visual)


class P02S08ThreeQuestions(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Three Questions"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Audit references: network_flow attention arcs + V2X graph links, kept as
        # persistent visual slots inside each card so the icons cannot be covered.
        what = _question_card("What?", "payload representation", _payload_visual(), stroke=ACCENT_TEAL, fill=PASTEL_TEAL)
        when = _question_card("When?", "communication timing", _window_visual(), stroke=GOLD_RICH, fill=PASTEL_AMBER)
        how = _question_card("How?", "fusion mechanism", _attention_visual(), stroke=PURPLE_MODEL, fill=PASTEL_BLUE)
        cards = VGroup(what, when, how).arrange(RIGHT, buff=0.5).move_to(UP * 0.38)

        self.play(LaggedStart(*(FadeIn(card, shift=UP * 0.12) for card in cards), lag_ratio=0.16))

        highlights = VGroup(
            SurroundingRectangle(what[3], buff=0.12, color=ACCENT_TEAL, stroke_width=2.0),
            SurroundingRectangle(when[3], buff=0.12, color=GOLD_RICH, stroke_width=2.0),
            SurroundingRectangle(how[3], buff=0.12, color=PURPLE_MODEL, stroke_width=2.0),
        )
        self.play(LaggedStart(*(ShowCreation(h) for h in highlights), lag_ratio=0.16), run_time=0.9)
        self.play(FadeOut(highlights), run_time=0.35)

        answer = _label("V2XPnP answers all three.", size=34, color=INK_DARK, weight=BOLD)
        answer["V2XPnP"].set_color(GOLD_RICH)
        answer.to_edge(DOWN, buff=0.65)
        self.play(FadeIn(answer, shift=UP * 0.2))
        self.wait(0.8)
        self._close()
