"""Callouts, thought bubbles, badges, key numbers, failure icons."""
from __future__ import annotations
from manimlib import *
from studio.components.colors import (
    INK_DARK, INK_MID, INK_LIGHT, GOLD_KEY, GOLD_RICH, RED_ERROR, BG_PAPER, LINE_SEP,
    PASTEL_PINK,
)
from studio.components.typography import FONT_PRIMARY, SIZE_BODY, SIZE_LABEL, SIZE_CAPS, SIZE_HERO


def callout(text_str: str, target: Mobject, *, side: str = "right") -> VGroup:
    """Tight speech callout (label + slim border + leader line to target).
    # Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py:95
    """
    lbl = Text(text_str, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
    pad_h, pad_v = 0.2, 0.12
    bubble = RoundedRectangle(
        width=lbl.get_width() + 2 * pad_h,
        height=lbl.get_height() + 2 * pad_v,
        corner_radius=0.1,
        fill_color=PASTEL_PINK, fill_opacity=0.98,
        stroke_color=INK_MID, stroke_width=2.2,
    )
    lbl.move_to(bubble.get_center())
    direction = RIGHT if side == "right" else LEFT
    group = VGroup(bubble, lbl)
    group.next_to(target, direction, buff=0.3)
    anchor = bubble.get_left() if side == "right" else bubble.get_right()
    tip = target.get_center()
    leader = Line(anchor, tip, stroke_color=INK_MID, stroke_width=1.8)
    return VGroup(group, leader)


def error_propagation_marker(
    *,
    radius: float = 0.11,
    label: str | None = None,
    label_side=LEFT,
) -> VGroup:
    """Red error badge (visible on cream BG) — sensor noise / uncertainty."""
    ring = Circle(
        radius=radius,
        fill_color=RED_ERROR,
        fill_opacity=1.0,
        stroke_color=INK_DARK,
        stroke_width=2.8,
    )
    s = radius * 0.52
    cross = VGroup(
        Line([-s, 0, 0], [s, 0, 0], color=WHITE, stroke_width=3.2),
        Line([0, -s, 0], [0, s, 0], color=WHITE, stroke_width=3.2),
    )
    cross.move_to(ring.get_center())
    group = VGroup(ring, cross)
    if label:
        lbl = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
        lbl.next_to(ring, label_side, buff=0.14)
        group = VGroup(group, lbl)
    return group


def error_callout(text_str: str, target: Mobject, *, side: str = "right") -> VGroup:
    """Red-tinted callout for failure / compounding errors."""
    lbl = Text(text_str, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
    pad_h, pad_v = 0.22, 0.14
    bubble = RoundedRectangle(
        width=lbl.get_width() + 2 * pad_h,
        height=lbl.get_height() + 2 * pad_v,
        corner_radius=0.1,
        fill_color=PASTEL_PINK,
        fill_opacity=1.0,
        stroke_color=RED_ERROR,
        stroke_width=2.8,
    )
    lbl.move_to(bubble.get_center())
    direction = RIGHT if side == "right" else LEFT
    group = VGroup(bubble, lbl)
    group.next_to(target, direction, buff=0.28)
    anchor = bubble.get_left() if side == "right" else bubble.get_right()
    leader = Line(anchor, target.get_center(), stroke_color=RED_ERROR, stroke_width=2.2)
    return VGroup(group, leader)


def thought_bubble(text_str: str, target: Mobject) -> VGroup:
    """Pi-style thought bubble: three small circles + main oval bubble."""
    small_dots = VGroup(*(
        Dot(radius=0.04 + i * 0.025, color=LINE_SEP) for i in range(3)
    ))
    small_dots.arrange(UR, buff=0.08)
    small_dots.next_to(target, UR, buff=0.1)
    lbl = Text(text_str, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
    pad_h, pad_v = 0.25, 0.18
    bubble = RoundedRectangle(
        width=lbl.get_width() + 2 * pad_h,
        height=lbl.get_height() + 2 * pad_v,
        corner_radius=0.2,
        fill_color="#FFFFFF", fill_opacity=0.95,
        stroke_color=LINE_SEP, stroke_width=1.5,
    )
    lbl.move_to(bubble.get_center())
    bubble.next_to(small_dots[-1], UR, buff=0.05)
    lbl.move_to(bubble.get_center())
    return VGroup(small_dots, bubble, lbl)


def contribution_badge(label: str, *, color: str = GOLD_KEY) -> VGroup:
    """Gold rounded badge for paper credits."""
    lbl = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
    glow = RoundedRectangle(
        width=lbl.get_width() + 0.42,
        height=lbl.get_height() + 0.24,
        corner_radius=0.14,
        fill_color=color, fill_opacity=0.08,
        stroke_color=color, stroke_width=5.0, stroke_opacity=0.12,
    )
    badge = RoundedRectangle(
        width=lbl.get_width() + 0.3,
        height=lbl.get_height() + 0.16,
        corner_radius=0.12,
        fill_color=interpolate_color(color, WHITE, 0.35), fill_opacity=0.95,
        stroke_color=color, stroke_width=2.8,
    )
    lbl.move_to(badge.get_center())
    return VGroup(glow, badge, lbl)


def key_number(value: str, label: str, *, color: str = GOLD_RICH) -> VGroup:
    """SIZE_HERO value + SIZE_LABEL caption below — for footer zone."""
    val_mob = Text(value, font=FONT_PRIMARY, font_size=SIZE_HERO, color=color, weight=BOLD)
    lbl_mob = Text(label, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID)
    group = VGroup(val_mob, lbl_mob)
    group.arrange(DOWN, buff=0.1)
    return group


def failure_icon(*, kind: str = "phone_pedestrian") -> VGroup:
    """Simple line-art failure icon; kind in {'phone_pedestrian', 'inverted_lights', 'snow_lane'}."""
    if kind == "phone_pedestrian":
        ped = pedestrian_stub(RED_ERROR)
        phone = Rectangle(width=0.2, height=0.32, fill_color=RED_ERROR, fill_opacity=0.9,
                          stroke_width=0)
        phone.rotate(-25 * DEGREES)
        phone.next_to(ped, RIGHT, buff=0.05)
        return VGroup(ped, phone)
    if kind == "inverted_lights":
        lights = VGroup(
            Circle(radius=0.12, fill_color=GREEN_FIX, fill_opacity=1.0, stroke_width=0),
            Circle(radius=0.12, fill_color=RED_ERROR, fill_opacity=1.0, stroke_width=0),
        )
        lights.arrange(DOWN, buff=0.06)
        box = SurroundingRectangle(lights, buff=0.1,
                                   stroke_color=INK_MID, stroke_width=1.5,
                                   fill_color=INK_DARK, fill_opacity=0.8)
        cross = VGroup(
            Line(box.get_corner(UL), box.get_corner(DR), stroke_color=RED_ERROR, stroke_width=2),
            Line(box.get_corner(UR), box.get_corner(DL), stroke_color=RED_ERROR, stroke_width=2),
        )
        return VGroup(box, lights, cross)
    # snow_lane
    lane = Rectangle(width=1.2, height=0.4, fill_color=INK_LIGHT, fill_opacity=0.3,
                     stroke_color=INK_MID, stroke_width=1.5)
    snow_dots = VGroup(*(Dot(radius=0.04, color=INK_LIGHT) for _ in range(6)))
    snow_dots.arrange_in_grid(2, 3, buff=0.2)
    snow_dots.move_to(lane)
    return VGroup(lane, snow_dots)


def pedestrian_stub(color: str) -> VGroup:
    """Minimal stick figure for failure_icon internals."""
    head = Circle(radius=0.08, fill_color=color, fill_opacity=1.0, stroke_width=0)
    body = Line(ORIGIN, DOWN * 0.28, stroke_color=color, stroke_width=2)
    legs = Line(DOWN * 0.28, DOWN * 0.5 + LEFT * 0.12, stroke_color=color, stroke_width=2)
    head.next_to(body, UP, buff=0.03)
    return VGroup(head, body, legs)


# avoid circular import — bring in GREEN_FIX here
from studio.components.colors import GREEN_FIX  # noqa: E402
