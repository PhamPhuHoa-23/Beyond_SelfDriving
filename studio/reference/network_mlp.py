# Ported from Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py
# Lines 173-206 (MLP synapses), 232-248 (mention_repetitions)
from __future__ import annotations

import itertools as it
import random

import numpy as np
from manimlib import *

from studio.reference.transformers_helpers import NumericEmbedding, value_to_color


def mlp_synapse_block(
    embedding: NumericEmbedding,
    *,
    n_neurons: int = 14,
    depth: float = 1.2,
    neuron_color="#7C3AED",
    sample_fraction: float = 0.18,
    line_color="#0F172A",
    flat_lines: bool = True,
) -> VGroup:
    """2D slice of progress_through_mlp_block — dots + sparse synapses."""
    col = embedding.get_columns()[0]
    l1 = np.array([e.get_center() for e in col])
    x0 = embedding.get_center()[0]
    y_min = embedding.get_bottom()[1] + 0.08
    y_max = embedding.get_top()[1] - 0.08
    z_mid = 0.0
    l1[:, 2] = z_mid
    l3 = l1.copy()
    l3[:, 0] = x0 + depth
    l2 = np.array([[x0 + depth * 0.5, y, z_mid] for y in np.linspace(y_min, y_max, n_neurons)])

    neurons = VGroup()
    for p in np.vstack([l1, l2, l3]):
        d = Dot(p, radius=0.075, color=neuron_color)
        d.set_stroke("#0F172A", width=1.4, opacity=1.0)
        neurons.add(d)

    lines = VGroup()
    for pts1, pts2 in [(l1, l2), (l2, l3)]:
        for p1, p2 in it.product(pts1, pts2):
            if random.random() < sample_fraction:
                if flat_lines:
                    stroke = line_color
                else:
                    val = random.uniform(-10, 10)
                    stroke = value_to_color(
                        val, line_color, "#06B6D4", line_color, "#06B6D4", 0, 10,
                    )
                lines.add(Line(
                    p1, p2, buff=0.03, stroke_width=4.0,
                    stroke_opacity=0.95,
                    stroke_color=stroke,
                ))
    return VGroup(lines, neurons)


def mention_repetitions_brace(
    mob: Mobject,
    *,
    depth: float = 2.4,
    label: str = "Many\nlayers",
) -> VGroup:
    """Side brace for stacked depth (network_flow mention_repetitions, 2D)."""
    dots = Tex(R"\vdots", font_size=48)
    brace = Brace(mob, LEFT, buff=0.15)
    txt = Text(label, font_size=22, color=GREY_B)
    txt.next_to(brace, LEFT, buff=0.1)
    group = VGroup(brace, txt, dots)
    dots.next_to(mob, DOWN, buff=0.12)
    return group
