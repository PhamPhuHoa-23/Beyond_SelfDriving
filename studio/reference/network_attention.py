# Ported from Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py
# Lines 159-171 — play_simple_attention_animation
from __future__ import annotations

import random

from manimlib import *

from studio.reference.transformers_helpers import RandomizeMatrixEntries


def random_bright_color(hue_range=(0.1, 0.3)):
    palette = [BLUE_B, TEAL, GREEN_B, YELLOW, MAROON_B]
    return random.choice(palette)


def play_simple_attention_animation(scene, layer, run_time=5, added_anims=None):
    """Exact structure from 3b1b network_flow — scene.play wrapper."""
    if added_anims is None:
        added_anims = []
    arc_groups = VGroup()
    for _ in range(3):
        for n, e1 in enumerate(layer.embeddings):
            arc_group = VGroup()
            for e2 in layer.embeddings[n + 1 :]:
                sign = (-1) ** int(e2.get_x() > e1.get_x())
                arc_group.add(
                    Line(
                        e1.get_top(),
                        e2.get_top(),
                        path_arc=sign * PI / 3,
                        stroke_color=random_bright_color(hue_range=(0.1, 0.3)),
                        stroke_width=5 * random.random() ** 5,
                    )
                )
            arc_group.shuffle()
            if len(arc_group) > 0:
                arc_groups.add(arc_group)
    scene.play(
        LaggedStart(
            *(
                AnimationGroup(
                    LaggedStartMap(
                        VShowPassingFlash,
                        arc_group.copy(),
                        time_width=2,
                        lag_ratio=0.15,
                    ),
                    LaggedStartMap(
                        ShowCreationThenFadeOut,
                        arc_group,
                        lag_ratio=0.15,
                    ),
                )
                for arc_group in arc_groups
            ),
            lag_ratio=0.0,
        ),
        LaggedStartMap(RandomizeMatrixEntries, layer.embeddings, lag_ratio=0.0),
        *added_anims,
        run_time=run_time,
    )
    scene.add(layer)
