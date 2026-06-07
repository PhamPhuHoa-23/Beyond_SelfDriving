# BEV feature tiles — audit: network_flow token grids + vla patch rows
from __future__ import annotations

import numpy as np
from manimlib import *
from manimlib.utils.color import interpolate_color

from studio.components.colors import INK_DARK, INK_MID


def lidar_point_cloud_side(
    n: int = 48,
    *,
    color=TEAL,
    width: float = 2.2,
    height: float = 1.6,
    seed: int = 7,
) -> VGroup:
    """Side-view LiDAR scatter (3D points projected to 2D)."""
    rng = np.random.RandomState(seed)
    pts = VGroup()
    for _ in range(n):
        x = rng.uniform(-width / 2, width / 2)
        y = rng.uniform(0.1, height)
        z = rng.uniform(0, 1)
        d = Dot(radius=0.06 + 0.025 * z, color=color)
        d.set_fill(color, opacity=1.0)
        d.set_stroke(INK_DARK, width=1.1, opacity=1.0)
        d.move_to([x, y - height / 2, 0])
        pts.add(d)
    return pts


def bev_token_grid(
    n_rows: int = 8,
    n_cols: int = 8,
    *,
    cell_size: float = 0.24,
    base_color=TEAL,
    seed: int = 11,
) -> VGroup:
    """Top-down BEV cells — colored feature map (not hand-drawn boxes)."""
    rng = np.random.RandomState(seed)
    cells = VGroup()
    for i in range(n_rows):
        for j in range(n_cols):
            t = rng.uniform(0, 1)
            c = interpolate_color(base_color, BLUE_C, 0.15 + 0.55 * t)
            cell = Square(
                side_length=cell_size,
                fill_color=c,
                fill_opacity=1.0,
                stroke_color=INK_MID,
                stroke_width=1.0,
            )
            cell.move_to(np.array([
                (j - (n_cols - 1) / 2) * cell_size,
                ((n_rows - 1) / 2 - i) * cell_size,
                0,
            ]))
            cells.add(cell)
    frame = SurroundingRectangle(cells, buff=0.06, color=base_color, stroke_width=2.5)
    return VGroup(frame, cells)


def qformer_stack(n: int = 4, *, color=BLUE_C, width: float = 1.4, depth: float = 0.12) -> VGroup:
    """Stacked blocks suggesting Q-Former / projection (audit: network_flow get_block)."""
    blocks = VGroup()
    for i in range(n):
        face = Rectangle(
            width=width,
            height=0.28,
            fill_color=interpolate_color(color, WHITE, 0.08 * i),
            fill_opacity=1.0,
            stroke_color=INK_MID,
            stroke_width=1.2,
        )
        lip = Rectangle(
            width=width + depth,
            height=0.08,
            fill_color=interpolate_color(color, BLACK, 0.25),
            fill_opacity=0.9,
            stroke_width=0,
        )
        lip.next_to(face, DOWN, buff=0)
        lip.shift(RIGHT * depth * 0.5)
        blocks.add(VGroup(face, lip))
    blocks.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    return blocks


def waypoint_polyline(
    points: list[np.ndarray] | None = None,
    *,
    color=GREEN,
    stroke_width: float = 3.0,
) -> VMobject:
    """Predicted trajectory on BEV plane."""
    if points is None:
        points = [
            np.array([-1.4, -0.9, 0]),
            np.array([-0.5, -0.5, 0]),
            np.array([0.2, -0.15, 0]),
            np.array([0.9, 0.35, 0]),
            np.array([1.5, 0.75, 0]),
        ]
    path = VMobject()
    path.set_points_as_corners([*points])
    path.set_stroke(color, stroke_width)
    tips = VGroup(*[Dot(p, radius=0.07, color=color) for p in points])
    return VGroup(path, tips)
