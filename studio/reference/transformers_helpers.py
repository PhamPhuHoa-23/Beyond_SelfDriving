# Ported from Source_manim_reference/3b1b_videos/_2024/transformers/helpers.py
# Lines 251-339 — WeightMatrix, NumericEmbedding, EmbeddingArray, RandomizeMatrixEntries
from __future__ import annotations

from typing import Optional

import numpy as np
from manimlib import *
from manimlib.utils.color import interpolate_color


def value_to_color(
    value: float,
    low_positive_color,
    high_positive_color,
    low_negative_color,
    high_negative_color,
    vmin: float,
    vmax: float,
):
    """Same role as manim_imports_ext.value_to_color (not in manimlib)."""
    span = max(vmax - vmin, 1e-6)
    alpha = np.clip(abs(value) / span, 0, 1)
    if value >= 0:
        return interpolate_color(low_positive_color, high_positive_color, alpha)
    return interpolate_color(low_negative_color, high_negative_color, alpha)


class WeightMatrix(DecimalMatrix):
    def __init__(
        self,
        values: Optional[np.ndarray] = None,
        shape: tuple[int, int] = (6, 8),
        value_range: tuple[float, float] = (-9.9, 9.9),
        ellipses_row: Optional[int] = -2,
        ellipses_col: Optional[int] = -2,
        num_decimal_places: int = 1,
        bracket_h_buff: float = 0.1,
        decimal_config: dict | None = None,
        low_positive_color=BLUE_E,
        high_positive_color=BLUE_B,
        low_negative_color=RED_E,
        high_negative_color=RED_B,
    ):
        if values is not None:
            shape = values.shape
        self.shape = shape
        self.value_range = value_range
        self.low_positive_color = low_positive_color
        self.high_positive_color = high_positive_color
        self.low_negative_color = low_negative_color
        self.high_negative_color = high_negative_color
        self.ellipses_row = ellipses_row
        self.ellipses_col = ellipses_col
        if values is None:
            values = np.random.uniform(*self.value_range, size=shape)
        if decimal_config is None:
            decimal_config = dict(include_sign=True)
        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
        )
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_color(
                value_to_color(
                    entry.get_value(),
                    self.low_positive_color,
                    self.high_positive_color,
                    self.low_negative_color,
                    self.high_negative_color,
                    0,
                    max(self.value_range),
                )
            )
        return self


class NumericEmbedding(WeightMatrix):
    def __init__(
        self,
        values: Optional[np.ndarray] = None,
        shape: Optional[tuple[int, int]] = None,
        length: int = 7,
        num_decimal_places: int = 1,
        ellipses_row: int = -2,
        ellipses_col: int = -2,
        value_range: tuple[float, float] = (-9.9, 9.9),
        bracket_h_buff: float = 0.1,
        decimal_config: dict | None = None,
        dark_color=GREY_C,
        light_color=WHITE,
        **kwargs,
    ):
        if values is not None:
            if len(values.shape) == 1:
                values = values.reshape((values.shape[0], 1))
            shape = values.shape
        if shape is None:
            shape = (length, 1)
        if decimal_config is None:
            decimal_config = dict(include_sign=True)
        super().__init__(
            values,
            shape=shape,
            value_range=value_range,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            low_positive_color=dark_color,
            high_positive_color=light_color,
            low_negative_color=dark_color,
            high_negative_color=light_color,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
            **kwargs,
        )
        for entry in self.get_entries():
            if entry.get_value() == 0:
                entry.set_opacity(0)


class EmbeddingArray(VGroup):
    def __init__(
        self,
        shape=(10, 9),
        height=4,
        dots_index=-4,
        buff_ratio=0.4,
        bracket_color=GREY_B,
        backstroke_width=3,
        add_background_rectangle=False,
        dark_color=GREY_C,
        light_color=WHITE,
    ):
        super().__init__()
        embeddings = VGroup(
            *(NumericEmbedding(length=shape[0], dark_color=dark_color, light_color=light_color)
              for _ in range(shape[1]))
        )
        embeddings.set_height(height)
        buff = buff_ratio * embeddings[0].get_width()
        embeddings.arrange(RIGHT, buff=buff)
        if add_background_rectangle:
            for embedding in embeddings:
                embedding.add_background_rectangle()
        brackets = Tex(
            "".join((
                r"\left[\begin{array}{c}",
                *(shape[1] // 3) * [r"\quad \\"],
                r"\end{array}\right]",
            ))
        )
        brackets.set_height(1.1 * embeddings.get_height())
        lb = brackets[: len(brackets) // 2]
        rb = brackets[len(brackets) // 2 :]
        lb.next_to(embeddings, LEFT, buff=0)
        rb.next_to(embeddings, RIGHT, buff=0)
        brackets.set_fill(bracket_color)
        dots = VGroup()
        self.add(embeddings, dots, brackets)
        self.embeddings = embeddings
        self.dots = dots
        self.brackets = brackets
        self.set_backstroke(BLACK, backstroke_width)
        if dots_index is not None:
            self.swap_embedding_for_dots(dots_index)

    def swap_embedding_for_dots(self, dots_index=-4):
        to_replace = self.embeddings[dots_index]
        dots = Tex(R"\dots", font_size=60)
        dots.set_width(0.75 * to_replace.get_width())
        dots.move_to(to_replace)
        self.embeddings.remove(to_replace)
        self.dots.add(dots)
        return self


class RandomizeMatrixEntries(Animation):
    def __init__(self, matrix, **kwargs):
        self.matrix = matrix
        self.entries = matrix.get_entries()
        self.start_values = [entry.get_value() for entry in self.entries]
        self.target_values = np.random.uniform(
            matrix.value_range[0], matrix.value_range[1], len(self.entries),
        )
        super().__init__(matrix, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for index, entry in enumerate(self.entries):
            start = self.start_values[index]
            target = self.target_values[index]
            sub_alpha = self.get_sub_alpha(alpha, index, len(self.entries))
            entry.set_value(interpolate(start, target, sub_alpha))
        self.matrix.reset_entry_colors()
