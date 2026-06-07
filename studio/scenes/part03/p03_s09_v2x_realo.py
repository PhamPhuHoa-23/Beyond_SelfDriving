"""P03-S09 V2X-ReaLO 32x compression."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, GOLD_KEY, ACCENT_TEAL,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, key_number,
)
from studio.reference.bev_grid import bev_token_grid

SCRIPT = """V2X-ReaLO compresses BEV features by keeping useful cells and packing them for V2X."""


def _label(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    return Text(text, font=FONT_PRIMARY, font_size=size, color=color, weight=weight)


def _packed_grid(source_cells: VGroup, active_idx: list[int], *, cell_size: float = 0.22) -> VGroup:
    cells = VGroup()
    for k, idx in enumerate(active_idx):
        src = source_cells[idx]
        cell = Square(
            side_length=cell_size,
            fill_color=src.get_fill_color(),
            fill_opacity=1.0,
            stroke_color=INK_MID,
            stroke_width=0.9,
        )
        row, col = divmod(k, 4)
        cell.move_to([
            (col - 1.5) * cell_size,
            (1.5 - row) * cell_size,
            0,
        ])
        cells.add(cell)
    frame = SurroundingRectangle(cells, buff=0.06, color=GREEN_FIX, stroke_width=2.4)
    return VGroup(frame, cells)


def _encoder() -> VGroup:
    body = Polygon(
        LEFT * 0.95 + UP * 0.72,
        LEFT * 0.95 + DOWN * 0.72,
        RIGHT * 0.95 + DOWN * 0.36,
        RIGHT * 0.95 + UP * 0.36,
        fill_color="#FAE3B0",
        fill_opacity=1.0,
        stroke_color=GOLD_KEY,
        stroke_width=2.6,
    )
    title = _label("32x", size=SIZE_LABEL, color=GOLD_KEY, weight=BOLD)
    sub = _label("encoder", size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
    text = VGroup(title, sub).arrange(DOWN, buff=0.02)
    text.move_to(body)
    ribs = VGroup()
    for y in (-0.3, 0, 0.3):
        ribs.add(Line(LEFT * 0.55 + UP * y, RIGHT * 0.45 + UP * (y * 0.5), stroke_color=GOLD_KEY, stroke_width=1.2, stroke_opacity=0.55))
    return VGroup(body, ribs, text)


class P03S09V2XReaLO(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "V2X-ReaLO: BEV Compression"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        bev = bev_token_grid(8, 8, cell_size=0.21, base_color=ACCENT_TEAL)
        bev.scale(1.35)
        bev.move_to(LEFT * 4.25 + UP * 0.12)
        bev_title = _label("BEV feature map", size=SIZE_LABEL, color=ACCENT_TEAL, weight=BOLD)
        bev_title.next_to(bev, UP, buff=0.18)
        bev_sub = _label("16 MB  FP32", size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
        bev_sub.next_to(bev, DOWN, buff=0.16)

        active_idx = [1, 3, 6, 10, 13, 18, 21, 26, 29, 33, 36, 42, 45, 50, 54, 61]
        source_cells = bev[1]
        inactive = VGroup(*(cell for i, cell in enumerate(source_cells) if i not in active_idx))
        active = VGroup(*(source_cells[i] for i in active_idx))

        encoder = _encoder()
        encoder.move_to(ORIGIN + UP * 0.1)
        enc_note = _label("drop blank cells\npack useful tokens", size=SIZE_CAPS - 1, color=INK_MID, weight=BOLD)
        enc_note.next_to(encoder, DOWN, buff=0.18)

        packed = _packed_grid(source_cells, active_idx, cell_size=0.2)
        packed.scale(1.28)
        packed.move_to(RIGHT * 3.65 + UP * 0.18)
        packed_title = _label("compressed BEV", size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD)
        packed_title.next_to(packed, UP, buff=0.18)
        packed_sub = _label("0.5 MB\nV2X ready", size=SIZE_CAPS, color=GREEN_FIX, weight=BOLD)
        packed_sub.next_to(packed, RIGHT, buff=0.22)

        arr1 = Arrow(bev.get_right() + RIGHT * 0.18, encoder.get_left() + LEFT * 0.18, buff=0, stroke_width=3.0, fill_color=GOLD_KEY)
        arr2 = Arrow(encoder.get_right() + RIGHT * 0.18, packed.get_left() + LEFT * 0.18, buff=0, stroke_width=3.0, fill_color=GREEN_FIX)

        self.play(FadeIn(bev_title), FadeIn(bev_sub), FadeIn(bev[0]), run_time=0.35)
        self.play(LaggedStart(*(GrowFromCenter(c) for c in source_cells), lag_ratio=0.012), run_time=1.0)
        self.play(inactive.animate.set_opacity(0.16), active.animate.set_stroke(GOLD_KEY, width=1.7), run_time=0.65)
        self.play(ShowCreation(arr1), FadeIn(encoder), FadeIn(enc_note), run_time=0.65)

        self.play(
            LaggedStart(
                *(TransformFromCopy(source_cells[idx], packed[1][k]) for k, idx in enumerate(active_idx)),
                lag_ratio=0.035,
            ),
            ShowCreation(arr2),
            run_time=1.25,
        )
        self.play(FadeIn(packed), FadeIn(packed_title), FadeIn(packed_sub), run_time=0.45)

        kn = key_number("32x", "compression  16 MB -> 0.5 MB", color=GOLD_KEY)
        kn.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(kn))
        self.wait(1.7)
        self._close()
