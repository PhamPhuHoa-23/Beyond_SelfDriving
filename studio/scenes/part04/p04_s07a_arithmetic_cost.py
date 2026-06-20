"""P04-S07: arithmetic and memory energy costs behind quantized inference."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, PASTEL_BLUE, PASTEL_GREEN,
    RED_ERROR, GREEN_FIX, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER,
    GOLD_RICH, INK_DARK, INK_MID, LINE_GRID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
)

SCRIPT = (
    "Why is neural network inference expensive on edge hardware? "
    "Neural networks are dominated by two operations: multiply-accumulate in "
    "fully connected and convolutional layers, and memory reads to load weights "
    "from off-chip memory. The energy costs are revealing. A 32-bit floating-point "
    "multiplication costs roughly 3.7 picojoules. A 32-bit memory access from DRAM "
    "costs approximately 640 picojoules — more than 170 times more expensive than "
    "the computation itself."
)


def label(text, size=SIZE_LABEL, color=INK_DARK, weight=NORMAL):
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def bit_strip(count, color, *, width=4.35, cell_height=0.27):
    gap = 0.025
    cell_width = (width - gap * (count - 1)) / count
    cells = VGroup()
    for _ in range(count):
        cell = RoundedRectangle(
            width=cell_width,
            height=cell_height,
            corner_radius=min(0.035, cell_width * 0.2),
        )
        cell.set_fill(color, opacity=0.92)
        cell.set_stroke(color, width=0)
        cells.add(cell)
    cells.arrange(RIGHT, buff=gap)
    return cells


def energy_bar(value, max_value, color, *, width=2.8):
    track = RoundedRectangle(width=width, height=0.26, corner_radius=0.08)
    track.set_fill(LINE_GRID, opacity=0.58)
    track.set_stroke(LINE_GRID, width=0)

    fill_width = max(0.07, width * value / max_value)
    fill = RoundedRectangle(width=fill_width, height=0.26, corner_radius=0.08)
    fill.set_fill(color, opacity=0.95)
    fill.set_stroke(color, width=0)
    fill.align_to(track, LEFT)
    return VGroup(track, fill)


def chip_icon(title, subtitle, color, *, width=1.72):
    body = RoundedRectangle(width=width, height=1.12, corner_radius=0.12)
    body.set_fill(color, opacity=0.1)
    body.set_stroke(color, width=2.0, opacity=0.9)

    pins = VGroup()
    for x in [-0.62, -0.2, 0.2, 0.62]:
        for y in [-0.65, 0.65]:
            pin = Line([x, y - 0.09, 0], [x, y + 0.09, 0])
            pin.set_stroke(color, width=2.0, opacity=0.75)
            pins.add(pin)
    for y in [-0.34, 0, 0.34]:
        for x in [-width / 2 - 0.1, width / 2 + 0.1]:
            pin = Line([x - 0.09, y, 0], [x + 0.09, y, 0])
            pin.set_stroke(color, width=2.0, opacity=0.75)
            pins.add(pin)

    title_mob = label(title, SIZE_LABEL, color, BOLD)
    subtitle_mob = label(subtitle, SIZE_CAPS - 1, INK_MID)
    copy = VGroup(title_mob, subtitle_mob)
    copy.arrange(DOWN, buff=0.05)
    copy.move_to(body)
    return VGroup(pins, body, copy)


class P04S07AArithmeticCost(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Arithmetic Energy Cost"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        divider = Line(UP * 2.3, DOWN * 2.8)
        divider.set_stroke(LINE_GRID, width=1.4, opacity=0.9)
        self.play(ShowCreation(divider), run_time=0.35)

        # Left: arithmetic cost from the original energy table.
        compute_title = label("COMPUTE  |  one multiply", SIZE_LABEL, INK_DARK, BOLD)
        compute_title.move_to(LEFT * 3.45 + UP * 2.12)
        compute_note = label("narrower operands switch less circuitry", SIZE_CAPS, INK_MID)
        compute_note.next_to(compute_title, DOWN, buff=0.07)
        self.play(FadeIn(compute_title), FadeIn(compute_note), run_time=0.45)

        fp32_name = label("FP32", SIZE_LABEL, RED_ERROR, BOLD)
        fp32_bits = bit_strip(32, RED_ERROR, width=4.35)
        fp32_bits.move_to(LEFT * 3.25 + UP * 0.88)
        fp32_name.next_to(fp32_bits, UP, aligned_edge=LEFT, buff=0.1)
        fp32_caption = label("32 bits", SIZE_CAPS, INK_MID)
        fp32_caption.next_to(fp32_bits, DOWN, buff=0.08)

        int8_name = label("INT8", SIZE_LABEL, GREEN_FIX, BOLD)
        int8_bits = bit_strip(8, GREEN_FIX, width=1.35)
        int8_bits.align_to(fp32_bits, LEFT)
        int8_bits.move_to([
            fp32_bits.get_left()[0] + int8_bits.get_width() / 2,
            -0.15,
            0,
        ])
        int8_name.next_to(int8_bits, UP, aligned_edge=LEFT, buff=0.1)
        int8_caption = label("8 bits", SIZE_CAPS, INK_MID)
        int8_caption.next_to(int8_bits, DOWN, buff=0.08)

        self.play(
            FadeIn(fp32_name),
            LaggedStart(*(FadeIn(bit, scale=0.6) for bit in fp32_bits),
                        lag_ratio=0.012, run_time=0.8),
            FadeIn(fp32_caption),
        )
        self.play(
            TransformFromCopy(fp32_name, int8_name),
            LaggedStart(*(FadeIn(bit, scale=0.6) for bit in int8_bits),
                        lag_ratio=0.04, run_time=0.55),
            FadeIn(int8_caption),
        )

        fp32_bar = energy_bar(3.7, 3.7, RED_ERROR)
        fp32_bar.move_to(LEFT * 3.25 + DOWN * 1.05)
        fp32_value = label("3.7 pJ", SIZE_LABEL, RED_ERROR, BOLD)
        fp32_value.next_to(fp32_bar, RIGHT, buff=0.15)
        fp32_op = label("FP32 MUL", SIZE_CAPS, INK_MID)
        fp32_op.next_to(fp32_bar, LEFT, buff=0.14)

        int8_bar = energy_bar(0.2, 3.7, GREEN_FIX)
        int8_bar.move_to(LEFT * 3.25 + DOWN * 1.68)
        int8_value = label("0.2 pJ", SIZE_LABEL, GREEN_FIX, BOLD)
        int8_value.next_to(int8_bar, RIGHT, buff=0.15)
        int8_op = label("INT8 MUL", SIZE_CAPS, INK_MID)
        int8_op.next_to(int8_bar, LEFT, buff=0.14)

        self.play(
            GrowFromEdge(fp32_bar[1], LEFT),
            FadeIn(fp32_bar[0]),
            FadeIn(fp32_op),
            FadeIn(fp32_value),
            run_time=0.65,
        )
        self.play(
            GrowFromEdge(int8_bar[1], LEFT),
            FadeIn(int8_bar[0]),
            FadeIn(int8_op),
            FadeIn(int8_value),
            run_time=0.45,
        )

        compute_ratio = VGroup(
            label("18.5x", SIZE_LABEL + 5, GREEN_FIX, BOLD),
            label("less arithmetic energy", SIZE_CAPS, INK_MID),
        )
        compute_ratio.arrange(DOWN, buff=0.02)
        compute_ratio.move_to(LEFT * 3.45 + DOWN * 2.48)
        self.play(FadeIn(compute_ratio, shift=0.08 * UP), run_time=0.45)

        # Right: memory hierarchy. This is a separate, much larger bottleneck.
        memory_title = label("MEMORY  |  move one 32-bit value", SIZE_LABEL, INK_DARK, BOLD)
        memory_title.move_to(RIGHT * 3.45 + UP * 2.12)
        memory_note = label("distance dominates energy", SIZE_CAPS, INK_MID)
        memory_note.next_to(memory_title, DOWN, buff=0.07)
        self.play(FadeIn(memory_title), FadeIn(memory_note), run_time=0.45)

        core = chip_icon("MAC", "compute core", ACCENT_BLUE, width=1.55)
        core.move_to(RIGHT * 3.55 + DOWN * 0.05)
        dram = chip_icon("DRAM", "off-chip", RED_ERROR)
        dram.move_to(RIGHT * 1.2 + UP * 0.95)
        sram = chip_icon("SRAM", "on-chip", GREEN_FIX)
        sram.move_to(RIGHT * 5.55 + UP * 0.95)

        dram_path = Arrow(
            dram.get_bottom(),
            core.get_left() + UP * 0.1,
            path_arc=0.35,
            buff=0.08,
            max_tip_length_to_length_ratio=0.1,
        )
        dram_path.set_stroke(RED_ERROR, width=3.0, opacity=0.82)
        dram_path.set_fill(RED_ERROR, opacity=0.82)

        sram_path = Arrow(
            sram.get_bottom(),
            core.get_right() + UP * 0.1,
            path_arc=-0.35,
            buff=0.08,
            max_tip_length_to_length_ratio=0.12,
        )
        sram_path.set_stroke(GREEN_FIX, width=3.0, opacity=0.82)
        sram_path.set_fill(GREEN_FIX, opacity=0.82)

        self.play(FadeIn(core), FadeIn(dram), FadeIn(sram), run_time=0.6)
        self.play(ShowCreation(dram_path), run_time=0.65)

        dram_packet = Square(side_length=0.18)
        dram_packet.set_fill(RED_ERROR, opacity=1.0)
        dram_packet.set_stroke(RED_ERROR, width=0)
        dram_packet.move_to(dram_path.get_start())
        self.add(dram_packet)
        self.play(MoveAlongPath(dram_packet, dram_path), run_time=0.8, rate_func=linear)

        dram_value = label("640 pJ", SIZE_LABEL + 3, RED_ERROR, BOLD)
        dram_value.move_to(RIGHT * 1.28 + DOWN * 1.35)
        dram_sub = label("DRAM access", SIZE_CAPS, INK_MID)
        dram_sub.next_to(dram_value, DOWN, buff=0.05)
        self.play(FadeIn(dram_value), FadeIn(dram_sub), run_time=0.35)

        self.play(ShowCreation(sram_path), run_time=0.45)
        sram_packet = Square(side_length=0.18)
        sram_packet.set_fill(GREEN_FIX, opacity=1.0)
        sram_packet.set_stroke(GREEN_FIX, width=0)
        sram_packet.move_to(sram_path.get_start())
        self.add(sram_packet)
        self.play(MoveAlongPath(sram_packet, sram_path), run_time=0.38, rate_func=linear)

        sram_value = label("5 pJ", SIZE_LABEL + 3, GREEN_FIX, BOLD)
        sram_value.move_to(RIGHT * 5.55 + DOWN * 1.35)
        sram_sub = label("SRAM access", SIZE_CAPS, INK_MID)
        sram_sub.next_to(sram_value, DOWN, buff=0.05)
        self.play(FadeIn(sram_value), FadeIn(sram_sub), run_time=0.35)

        memory_ratio = VGroup(
            label("128x", SIZE_LABEL + 5, GOLD_RICH, BOLD),
            label("more energy to fetch from DRAM", SIZE_CAPS, INK_MID),
        )
        memory_ratio.arrange(DOWN, buff=0.02)
        memory_ratio.move_to(RIGHT * 3.45 + DOWN * 2.48)
        self.play(
            FadeIn(memory_ratio, shift=0.08 * UP),
            Flash(dram_value, color=RED_ERROR, line_length=0.16, num_lines=8),
            run_time=0.55,
        )

        self.wait(1.5)
        self._close()
