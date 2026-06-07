# Ported from Source_manim_reference/welchlabs_videos/once_useful_constructs/light.py
# Lines 32-78 — inverse_quadratic, AmbientLight
from __future__ import annotations

import numpy as np
from manimlib import *

NUM_LEVELS = 15


def inverse_power_law(maxint, scale, cutoff, exponent):
    return lambda r: maxint * (cutoff / (r / scale + cutoff)) ** exponent


def inverse_quadratic(maxint, scale, cutoff):
    return inverse_power_law(maxint, scale, cutoff, 2)


class AmbientLight(VMobject):
    """Radial falloff rings — use for RSU / radar glow (audit light.py:65)."""

    def __init__(
        self,
        source_point=None,
        opacity_function=None,
        color=YELLOW,
        max_opacity=1.0,
        num_levels=NUM_LEVELS,
        radius=5.0,
        **kwargs,
    ):
        if source_point is None:
            source_point = VectorizedPoint(location=ORIGIN, stroke_width=0, fill_opacity=0)
        if opacity_function is None:
            opacity_function = lambda r: 1.0 / (r + 1.0) ** 2
        self.source_point = source_point
        self.opacity_function = opacity_function
        self.color = color
        self.max_opacity = max_opacity
        self.num_levels = num_levels
        self.radius = float(radius)
        super().__init__(**kwargs)
        self.init_points()

    def init_points(self):
        self.set_submobjects([])
        self.add(self.source_point)
        dr = self.radius / self.num_levels
        for r in np.arange(0, self.radius, dr):
            alpha = self.max_opacity * self.opacity_function(r)
            annulus = Annulus(
                inner_radius=r,
                outer_radius=r + dr,
                color=self.color,
                fill_opacity=alpha,
            )
            annulus.move_to(self.get_source_point())
            self.add(annulus)

    def move_source_to(self, point):
        self.move_to(point)
        return self

    def get_source_point(self):
        return self.source_point.get_location()
