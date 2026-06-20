"""P04-S07B: Memory-bound inference, 4x memory savings, and arithmetic transition to addition."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene, BG_PAPER, PASTEL_BLUE, PASTEL_GREEN, PASTEL_AMBER,
    RED_ERROR, GREEN_FIX, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER,
    GOLD_RICH, INK_DARK, INK_MID, LINE_GRID, LINE_SEP,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, SIZE_BODY,
)

SCRIPT = (
    "This means inference on edge hardware is memory-bound, not compute-bound. "
    "The bottleneck is not running the arithmetic but loading the model parameters. "
    "Reducing the bit-width of weights from 32-bit float to 8-bit integer cuts the "
    "memory footprint by 4x, replaces multiplications with cheaper integer additions, "
    "and enables hardware accelerators designed specifically for INT8 operations on modern edge chips."
)


def label(text, size=SIZE_LABEL, color=INK_DARK, weight=NORMAL):
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def bit_strip(count, color, *, width=3.6, cell_height=0.22):
    gap = 0.02
    cell_width = (width - gap * (count - 1)) / count
    cells = VGroup()
    for _ in range(count):
        cell = RoundedRectangle(
            width=cell_width,
            height=cell_height,
            corner_radius=min(0.025, cell_width * 0.2),
        )
        cell.set_fill(color, opacity=0.92)
        cell.set_stroke(color, width=0)
        cells.add(cell)
    cells.arrange(RIGHT, buff=gap)
    return cells


def chip_icon(title, subtitle, color, *, width=1.55):
    body = RoundedRectangle(width=width, height=1.12, corner_radius=0.12)
    body.set_fill(color, opacity=0.1)
    body.set_stroke(color, width=2.0, opacity=0.9)

    pins = VGroup()
    for x in [-0.52, -0.16, 0.16, 0.52]:
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


class P04S07BMemoryBound(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Memory-Bound Inference"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)



        # =========================================================================
        # LEFT COLUMN: Memory Funnel Bottleneck
        # =========================================================================
        left_center_x = -3.2

        # 1. DRAM Storage (at the top)
        dram_box = RoundedRectangle(width=2.0, height=0.6, corner_radius=0.08)
        dram_box.set_fill(PASTEL_AMBER, opacity=0.3)
        dram_box.set_stroke(ACCENT_AMBER, width=1.8, opacity=0.9)
        dram_box.move_to([left_center_x, 2.3, 0])
        dram_lbl = label("DRAM (off-chip)", SIZE_CAPS, ACCENT_AMBER, BOLD)
        dram_lbl.move_to(dram_box)

        # 2. Funnel geometry
        # Neck is extended down to y = -1.5, matching core top edge y = -1.54
        left_wall = VMobject()
        left_wall.set_points_as_corners([
            [left_center_x - 1.2, 1.8, 0],
            [left_center_x - 0.3, 0.4, 0],
            [left_center_x - 0.3, -1.5, 0]
        ])
        right_wall = VMobject()
        right_wall.set_points_as_corners([
            [left_center_x + 1.2, 1.8, 0],
            [left_center_x + 0.3, 0.4, 0],
            [left_center_x + 0.3, -1.5, 0]
        ])
        funnel = VGroup(left_wall, right_wall)
        funnel.set_stroke(INK_MID, width=3.0)

        # Bottleneck Indicator Label (completely out of the flow path)
        funnel_lbl = label("MEMORY BANDWIDTH", SIZE_CAPS - 2, INK_MID)
        funnel_lbl.next_to(dram_box, LEFT, buff=0.18)

        limit_lbl = label("BANDWIDTH LIMIT", SIZE_CAPS - 4, ACCENT_AMBER, BOLD)
        limit_lbl.move_to([left_center_x - 1.48, -0.5, 0])
        limit_arrow = Tex(r"\rightarrow", font_size=SIZE_CAPS)
        limit_arrow.set_color(ACCENT_AMBER)
        limit_arrow.next_to(limit_lbl, RIGHT, buff=0.08)
        bandwidth_indicator = VGroup(limit_lbl, limit_arrow)

        # 3. MAC Compute Core (at the bottom)
        core = chip_icon("MAC", "compute core", ACCENT_BLUE, width=1.4)
        core.move_to([left_center_x, -2.1, 0])
        core_body = core[1]

        core_status = label("IDLE (Starving)", SIZE_CAPS, RED_ERROR, BOLD)
        core_status.move_to([left_center_x, -2.9, 0])

        core_note = label("Compute is ready, but waiting for data", SIZE_CAPS - 4, INK_MID)
        core_note.next_to(core, RIGHT, buff=0.2)
        core_note.shift(DOWN * 0.1)

        self.play(
            FadeIn(dram_box), FadeIn(dram_lbl),
            ShowCreation(funnel), FadeIn(funnel_lbl),
            FadeIn(bandwidth_indicator),
            FadeIn(core), FadeIn(core_status), FadeIn(core_note),
            run_time=0.75
        )

        # =========================================================================
        # BEAT 1: FP32 Mode — High Latency, Bottleneck Flow
        # =========================================================================
        # Spawn blocks at the bottom of the DRAM box to avoid overlapping the text label
        spawn_y = dram_box.get_bottom()[1] - 0.22

        fp32_blocks = VGroup()
        for i in range(3):
            blk = RoundedRectangle(width=0.5, height=0.4, corner_radius=0.06)
            blk.set_fill(RED_ERROR, opacity=0.9)
            blk.set_stroke(RED_ERROR, width=0)
            blk.move_to([left_center_x, spawn_y, 0])
            fp32_blocks.add(blk)

        # Queue them up below the neck entrance (avoiding collision with any labels)
        self.play(
            fp32_blocks[0].animate.move_to([left_center_x, -0.1, 0]),
            fp32_blocks[1].animate.move_to([left_center_x, 0.4, 0]),
            fp32_blocks[2].animate.move_to([left_center_x, 0.9, 0]),
            run_time=0.8
        )
        self.wait(0.1)

        # Block 1 slowly moves through the bottleneck neck to the Core
        self.play(
            fp32_blocks[0].animate.move_to([left_center_x, -2.1, 0]),
            fp32_blocks[1].animate.move_to([left_center_x, -0.1, 0]),
            fp32_blocks[2].animate.move_to([left_center_x, 0.4, 0]),
            run_time=1.0,
            rate_func=linear
        )

        # Core processes Block 1 (concentric rounded ripple, block fades)
        ripple = core_body.copy()
        ripple.set_stroke(RED_ERROR, width=2.0, opacity=0.9)
        ripple.set_fill(opacity=0)
        self.play(
            FadeOut(fp32_blocks[0], scale=0.6),
            ripple.animate(run_time=0.45, rate_func=smooth)
                  .scale(1.35)
                  .set_stroke(opacity=0),
            core_status.animate.set_color(RED_ERROR)
        )

        # Block 2 slowly moves down to the core
        self.play(
            fp32_blocks[1].animate.move_to([left_center_x, -2.1, 0]),
            fp32_blocks[2].animate.move_to([left_center_x, -0.1, 0]),
            run_time=1.0,
            rate_func=linear
        )
        self.play(
            FadeOut(fp32_blocks[1], scale=0.6),
            Flash(core_body, color=RED_ERROR, line_length=0.15, num_lines=8),
            run_time=0.45
        )

        # =========================================================================
        # RIGHT COLUMN: Footprint & Spacing Definition
        # =========================================================================
        right_center_x = 3.5

        # 1. Weight Precision Title
        prec_title = label("WEIGHT PRECISION", SIZE_CAPS, INK_DARK, BOLD)
        prec_title.move_to([right_center_x, 2.1, 0])

        fp32_lbl_r = label("FP32 (32-bit float)", SIZE_CAPS - 1, RED_ERROR, BOLD)
        fp32_lbl_r.next_to(prec_title, DOWN, aligned_edge=LEFT, buff=0.22)
        fp32_lbl_r.shift(LEFT * 1.5)

        fp32_strip = bit_strip(32, RED_ERROR, width=3.2)
        fp32_strip.next_to(fp32_lbl_r, DOWN, aligned_edge=LEFT, buff=0.1)

        self.play(
            FadeIn(prec_title),
            FadeIn(fp32_lbl_r),
            LaggedStart(*(FadeIn(b, scale=0.6) for b in fp32_strip), lag_ratio=0.01, run_time=0.8)
        )

        # =========================================================================
        # BEAT 2: Transition to INT8 (Synchronized Left & Right)
        # =========================================================================
        # Prepare INT8 elements on the Right
        int8_lbl_r = label("INT8 (8-bit integer)", SIZE_CAPS - 1, GREEN_FIX, BOLD)
        int8_lbl_r.next_to(fp32_strip, DOWN, aligned_edge=LEFT, buff=0.3)

        int8_strip = bit_strip(8, GREEN_FIX, width=0.8)
        int8_strip.next_to(int8_lbl_r, DOWN, aligned_edge=LEFT, buff=0.1)

        savings_note = label("4x smaller memory footprint", SIZE_CAPS, GREEN_FIX, BOLD)
        savings_note.next_to(int8_strip, RIGHT, buff=0.3)

        # Prepare INT8 elements on the Left (spawning directly at the neck mouth, not at DRAM center)
        green_blocks = VGroup()
        for i in range(4):
            g_blk = RoundedRectangle(width=0.22, height=0.16, corner_radius=0.03)
            g_blk.set_fill(GREEN_FIX, opacity=0.9)
            g_blk.set_stroke(GREEN_FIX, width=0)
            g_blk.move_to([left_center_x, -0.1, 0])
            green_blocks.add(g_blk)

        # Labels update on the Left
        active_status = label("ACTIVE (INT8 Path)", SIZE_CAPS, GREEN_FIX, BOLD)
        active_status.move_to(core_status)
        active_note = label("Fully utilized compute core", SIZE_CAPS - 4, GREEN_FIX, BOLD)
        active_note.move_to(core_note)

        # Synchronized play call mapping left-side transformation and right-side reveal
        self.play(
            FadeOut(fp32_blocks[2], scale=0.6),  # cleanly retire the last red block
            *(FadeIn(g, scale=0.6) for g in green_blocks),
            FadeIn(int8_lbl_r),
            LaggedStart(*(FadeIn(b, scale=0.6) for b in int8_strip), lag_ratio=0.03, run_time=0.4),
            FadeIn(savings_note, shift=UP * 0.1),
            Transform(core_status, active_status),
            Transform(core_note, active_note),
            run_time=0.85
        )

        # Rapid stream animation: green blocks flow quickly and in parallel
        self.play(
            green_blocks[0].animate.move_to([left_center_x - 0.12, -0.4, 0]),
            green_blocks[1].animate.move_to([left_center_x + 0.12, -0.4, 0]),
            green_blocks[2].animate.move_to([left_center_x - 0.12, -0.1, 0]),
            green_blocks[3].animate.move_to([left_center_x + 0.12, -0.1, 0]),
            run_time=0.4
        )

        # Target ONLY core_body to prevent stroking the core's text labels green
        self.play(
            green_blocks[0].animate.move_to([left_center_x - 0.12, -2.1, 0]),
            green_blocks[1].animate.move_to([left_center_x + 0.12, -2.1, 0]),
            green_blocks[2].animate.move_to([left_center_x - 0.12, -1.5, 0]),
            green_blocks[3].animate.move_to([left_center_x + 0.12, -1.5, 0]),
            core_body.animate.set_stroke(GREEN_FIX, width=2.4),
            run_time=0.45,
            rate_func=linear
        )
        self.play(
            FadeOut(green_blocks[0], scale=0.6),
            FadeOut(green_blocks[1], scale=0.6),
            Flash(core_body, color=GREEN_FIX, line_length=0.18, num_lines=10),
            run_time=0.3
        )
        self.play(
            green_blocks[2].animate.move_to([left_center_x - 0.12, -2.1, 0]),
            green_blocks[3].animate.move_to([left_center_x + 0.12, -2.1, 0]),
            run_time=0.3,
            rate_func=linear
        )
        self.play(
            FadeOut(green_blocks[2], scale=0.6),
            FadeOut(green_blocks[3], scale=0.6),
            Flash(core_body, color=GREEN_FIX, line_length=0.18, num_lines=10),
            run_time=0.3
        )

        # =========================================================================
        # BEAT 3: Arithmetic Shift (Multiplication vs Addition)
        # =========================================================================
        arith_title = label("ARITHMETIC SIMPLIFICATION", SIZE_CAPS, INK_DARK, BOLD)
        arith_title.move_to([right_center_x, -0.6, 0])

        fp32_op = VGroup(
            Circle(radius=0.24, stroke_color=RED_ERROR, stroke_width=2),
            label("\u00d7", SIZE_BODY + 4, RED_ERROR, BOLD)  # Use proper multiplication sign ×
        )
        fp32_op[1].move_to(fp32_op[0])
        fp32_op_lbl = label("FP32: 32-bit float operations (Expensive)", SIZE_CAPS - 1, INK_MID)
        fp32_op_group = VGroup(fp32_op, fp32_op_lbl).arrange(RIGHT, buff=0.2)
        fp32_op_group.next_to(arith_title, DOWN, aligned_edge=LEFT, buff=0.22)
        fp32_op_group.shift(LEFT * 1.3)

        int8_op = VGroup(
            Circle(radius=0.24, stroke_color=GREEN_FIX, stroke_width=2),
            label("+", SIZE_BODY, GREEN_FIX, BOLD)
        )
        int8_op[1].move_to(int8_op[0])
        int8_op_lbl = label("INT8: Cheap 8-bit integer ops (Simple)", SIZE_CAPS - 1, INK_MID)
        int8_op_group = VGroup(int8_op, int8_op_lbl).arrange(RIGHT, buff=0.2)
        int8_op_group.next_to(fp32_op_group, DOWN, aligned_edge=LEFT, buff=0.22)

        # Left column flow is kept alive by animating small green packets drifting down
        left_dots1 = VGroup()
        for _ in range(5):
            d = RoundedRectangle(width=0.16, height=0.11, corner_radius=0.03)
            d.set_fill(GREEN_FIX, opacity=0.95)
            d.set_stroke(GREEN_FIX, width=0)
            left_dots1.add(d)

        left_flow_anims1 = []
        for j, d in enumerate(left_dots1):
            # Spawn dots staggered
            d.move_to([left_center_x, spawn_y - j * 0.45, 0])
            left_flow_anims1.append(d.animate(run_time=1.3, rate_func=linear).shift(DOWN * 4.2))

        self.play(
            FadeIn(arith_title),
            FadeIn(fp32_op_group),
            LaggedStart(*left_flow_anims1, lag_ratio=0.15, run_time=1.3),
            run_time=1.3
        )
        self.remove(*left_dots1)
        self.wait(0.3)

        # Another set of dots to keep the visual flow alive during the INT8 reveal
        left_dots2 = VGroup()
        for _ in range(5):
            d = RoundedRectangle(width=0.16, height=0.11, corner_radius=0.03)
            d.set_fill(GREEN_FIX, opacity=0.95)
            d.set_stroke(GREEN_FIX, width=0)
            left_dots2.add(d)

        left_flow_anims2 = []
        for j, d in enumerate(left_dots2):
            d.move_to([left_center_x, spawn_y - j * 0.45, 0])
            left_flow_anims2.append(d.animate(run_time=1.3, rate_func=linear).shift(DOWN * 4.2))

        self.play(
            FadeIn(int8_op_group),
            Flash(int8_op[0], color=GREEN_FIX, line_length=0.12, num_lines=8),
            LaggedStart(*left_flow_anims2, lag_ratio=0.15, run_time=1.3),
            run_time=1.3
        )
        self.remove(*left_dots2)

        summary_badge = label(
            "Memory-bound bottleneck solved: 4x footprint reduction + cheaper INT8 additions",
            SIZE_CAPS,
            INK_DARK,
            BOLD,
        )
        summary_badge.to_edge(DOWN, buff=0.26)
        self.play(FadeIn(summary_badge, shift=UP * 0.08), run_time=0.75)

        self.wait(2.0)
        self._close()
