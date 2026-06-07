"""Chart building blocks — axes, bar reveals, curve traces, scatter rain."""
from __future__ import annotations

from typing import Callable

import numpy as np
from manimlib import *

from studio.components.colors import ACCENT_BLUE, INK_DARK, INK_MID
from studio.components.typography import FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS

# Default chart footprint — fills studio content band (fixes tiny charts / Y labels)
CHART_WIDTH: float = 9.0
CHART_HEIGHT: float = 5.2
CHART_TICK_SIZE: int = SIZE_LABEL
CHART_AXIS_LABEL_SIZE: int = SIZE_LABEL


def _y_tick_labels(axes: Axes, *, font_size: int = CHART_TICK_SIZE) -> VGroup:
    y0, y1, step = axes.y_range[0], axes.y_range[1], axes.y_range[2]
    labels = VGroup()
    y = y0
    while y <= y1 + step * 0.01:
        if abs(y - round(y)) < 0.01:
            txt = f"{int(round(y))}"
        else:
            txt = f"{y:.2f}".rstrip("0").rstrip(".")
        t = Text(txt, font=FONT_PRIMARY, font_size=font_size, color=INK_MID, weight=BOLD)
        tick_pt = axes.c2p(axes.x_range[0], y)
        t.move_to(tick_pt)
        t.align_to(tick_pt, RIGHT)
        t.shift(LEFT * 0.48)
        labels.add(t)
        y += step
    return labels


def _x_tick_labels(
    axes: Axes,
    labels: list[str],
    *,
    font_size: int = CHART_TICK_SIZE,
) -> VGroup:
    group = VGroup()
    n = len(labels)
    x0, x1 = axes.x_range[0], axes.x_range[1]
    for i, lbl in enumerate(labels):
        x = x0 + (i + 0.5) * (x1 - x0) / max(n, 1)
        t = Text(lbl, font=FONT_PRIMARY, font_size=font_size, color=INK_MID, weight=BOLD)
        t.next_to(axes.c2p(x, 0), DOWN, buff=0.24)
        group.add(t)
    return group


def bar_group_labels(
    axes: Axes,
    groups: list[tuple[str, int, int]],
    *,
    n_bars: int = 4,
    font_size: int = CHART_AXIS_LABEL_SIZE,
) -> VGroup:
    """Category names under bar ranges — i_end is exclusive, e.g. ('nuPlan', 0, 2)."""
    out = VGroup()
    x0, x1 = axes.x_range[0], axes.x_range[1]
    step = (x1 - x0) / max(n_bars, 1)
    for name, i_start, i_end in groups:
        # Center of bar indices [i_start, i_end) — e.g. bars 2–3 → index 2.5
        mid_idx = (i_start + i_end - 1) / 2.0
        x_mid = x0 + (mid_idx + 0.5) * step
        t = Text(name, font=FONT_PRIMARY, font_size=font_size, color=INK_DARK, weight=BOLD)
        t.next_to(axes.c2p(x_mid, 0), DOWN, buff=0.58)
        out.add(t)
    return out


def axes_deploy(
    x_range: tuple,
    y_range: tuple,
    *,
    x_label: str = "",
    y_label: str = "",
    width: float = CHART_WIDTH,
    height: float = CHART_HEIGHT,
    axis_config: dict | None = None,
    with_tick_labels: bool = True,
) -> tuple[Axes, AnimationGroup]:
    """Returns (axes, animation). Axes first, then data.
    # Pattern adapted from: Source_manim_reference/welchlabs_videos/_2025/generalization/p8_15.py
    """
    cfg = axis_config or {
        "include_tip": True,
        "stroke_color": INK_MID,
        "stroke_width": 2.5,
    }
    xr = list(x_range) + [1] if len(x_range) == 2 else list(x_range)
    yr = list(y_range) + [1] if len(y_range) == 2 else list(y_range)
    axes = Axes(
        x_range=xr,
        y_range=yr,
        width=width,
        height=height,
        axis_config=cfg,
    )
    anims: list[Animation] = [
        ShowCreation(axes.x_axis),
        ShowCreation(axes.y_axis),
    ]
    return axes, AnimationGroup(*anims, lag_ratio=0.25)


def place_chart(axes: Axes, position: np.ndarray = ORIGIN, scale: float = 1.0) -> Axes:
    """Position chart in content area — do NOT scale below 0.85."""
    axes.scale(max(scale, 0.85))
    axes.move_to(position)
    return axes


def chart_labels(
    axes: Axes,
    *,
    x_label: str = "",
    y_label: str = "",
) -> VGroup:
    """Build tick + axis labels AFTER place_chart (correct c2p coords)."""
    tick_mobs = VGroup(_y_tick_labels(axes))
    if x_label:
        xl = Text(x_label, font=FONT_PRIMARY, font_size=CHART_AXIS_LABEL_SIZE, color=INK_DARK, weight=BOLD)
        xl.next_to(axes.x_axis, DOWN, buff=0.85)
        tick_mobs.add(xl)
    if y_label:
        yl = Text(y_label, font=FONT_PRIMARY, font_size=CHART_AXIS_LABEL_SIZE, color=INK_DARK, weight=BOLD)
        yl.rotate(90 * DEGREES)
        yl.next_to(axes.c2p(axes.x_range[0], axes.y_range[1]), LEFT, buff=1.05)
        tick_mobs.add(yl)
    axes.tick_labels = tick_mobs  # type: ignore[attr-defined]
    return tick_mobs


def chart_mount(
    axes: Axes,
    position: np.ndarray = ORIGIN,
    scale: float = 1.0,
    *,
    x_label: str = "",
    y_label: str = "",
) -> VGroup:
    """place_chart + chart_labels — call before FadeIn labels."""
    place_chart(axes, position, scale)
    return chart_labels(axes, x_label=x_label, y_label=y_label)


def bar_reveal(
    axes: Axes,
    values: list[float],
    *,
    colors: list[str],
    bar_width: float = 0.62,
    show_values: bool = True,
    x_labels: list[str] | None = None,
) -> tuple[VGroup, LaggedStart]:
    """Bars grow from y=0; optional value labels on top."""
    bars = VGroup()
    value_labels = VGroup()
    x_step = (axes.x_range[1] - axes.x_range[0]) / max(len(values), 1)
    for i, (val, col) in enumerate(zip(values, colors)):
        x = axes.x_range[0] + (i + 0.5) * x_step
        bottom = axes.c2p(x, 0)
        top = axes.c2p(x, val)
        bar = Rectangle(
            width=bar_width * x_step,
            height=abs(top[1] - bottom[1]),
            fill_color=col,
            fill_opacity=0.88,
            stroke_color=interpolate_color(col, INK_DARK, 0.25),
            stroke_width=1.2,
        )
        bar.move_to((bottom + top) / 2)
        bars.add(bar)
        if show_values:
            vl = Text(
                f"{val:.2f}".rstrip("0").rstrip("."),
                font=FONT_PRIMARY,
                font_size=SIZE_CAPS,
                color=INK_DARK,
                weight=BOLD,
            )
            vl.next_to(bar, UP, buff=0.12)
            value_labels.add(vl)
    group = VGroup(bars, value_labels)
    anim = LaggedStart(
        *(GrowFromEdge(b, DOWN) for b in bars),
        lag_ratio=0.18,
        run_time=1.2,
    )
    if x_labels:
        xl = _x_tick_labels(axes, x_labels)
        group.add(xl)
    return group, anim


def curve_trace(
    axes: Axes,
    fn: Callable[[float], float],
    *,
    color: str = ACCENT_BLUE,
    x_range: tuple | None = None,
    run_time: float = 2.0,
    stroke_width: float = 3.5,
) -> ShowCreation:
    """Trace a function curve left-to-right with ShowCreation."""
    xr = x_range or (axes.x_range[0], axes.x_range[1])
    curve = axes.get_graph(fn, x_range=list(xr), color=color, stroke_width=stroke_width)
    return ShowCreation(curve, run_time=run_time)


def scatter_rain(
    axes: Axes,
    points: list[tuple[float, float]],
    *,
    color: str,
    radius: float = 0.06,
) -> LaggedStart:
    """Points fall in from y_max to their final coord."""
    y_max = axes.y_range[1]
    dots = VGroup()
    anims = []
    for px, py in points:
        d = Dot(radius=radius, color=color)
        final = axes.c2p(px, py)
        start = axes.c2p(px, y_max)
        d.move_to(start)
        dots.add(d)
        anims.append(d.animate(run_time=0.5, rate_func=rush_into).move_to(final))
    return LaggedStart(*anims, lag_ratio=0.05)
