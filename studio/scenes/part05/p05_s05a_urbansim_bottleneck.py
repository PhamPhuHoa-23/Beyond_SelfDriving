"""P05-S05a UrbanSim CPU-GPU bottleneck."""
from manimlib import *

from studio.components import (
    StudioScene,
    BG_PAPER,
    BG_CARD,
    PASTEL_BLUE,
    PASTEL_PINK,
    PASTEL_AMBER,
    ACCENT_BLUE,
    ACCENT_AMBER,
    ACCENT_PINK,
    RED_ERROR,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_H1,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    key_number,
)

SCRIPT = """Traditional robot learning burns time in the CPU-GPU hot loop: observations and actions cross the bus every step."""


class P05S05AUrbanSimBottleneck(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "UrbanSim: The Bottleneck"

    def step_cell(self, label, *, width, height, fill, stroke, font_size=SIZE_MICRO, weight=BOLD):
        rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.06,
            fill_color=fill,
            fill_opacity=0.96,
            stroke_color=stroke,
            stroke_width=1.4,
        )
        text = Text(label, font=FONT_PRIMARY, font_size=font_size, color=INK_DARK, weight=weight)
        text.move_to(rect)
        return VGroup(rect, text)

    def cpu_core_row(self, y_shift):
        sim = self.step_cell("CPU core", width=1.45, height=0.42, fill="#FAD7C6", stroke=ACCENT_AMBER)
        obs = self.step_cell("CPU core", width=1.45, height=0.42, fill="#FAD7C6", stroke=ACCENT_AMBER)
        sim.move_to(LEFT * 4.55 + y_shift)
        obs.move_to(LEFT * 2.8 + y_shift)
        return VGroup(sim, obs)

    def transfer_band(self, label, x, *, height=1.68):
        band = RoundedRectangle(
            width=0.82,
            height=height,
            corner_radius=0.04,
            fill_color=PASTEL_PINK,
            fill_opacity=0.95,
            stroke_color=RED_ERROR,
            stroke_width=1.5,
        )
        band.move_to(RIGHT * x)
        text = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=RED_ERROR, weight=BOLD)
        text.move_to(band)
        return VGroup(band, text)

    def gpu_block(self, x, label="GPU"):
        block = RoundedRectangle(
            width=0.86,
            height=1.68,
            corner_radius=0.04,
            fill_color=PASTEL_BLUE,
            fill_opacity=0.96,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.6,
        )
        block.move_to(RIGHT * x)
        text = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        text.move_to(block)
        return VGroup(block, text)

    def stage_label(self, text, mob):
        label = Text(text, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK, weight=BOLD)
        label.next_to(mob, UP, buff=0.16)
        return label

    def build_traditional_loop(self):
        rows = VGroup(
            self.cpu_core_row(UP * 0.48),
            self.cpu_core_row(ORIGIN),
            self.cpu_core_row(DOWN * 0.48),
        )
        obs_transfer = self.transfer_band("data\ntransfer\n(obs)", -1.48)
        gpu = self.gpu_block(-0.48)
        act_transfer = self.transfer_band("data\ntransfer\n(actions)", 0.58)
        stages = VGroup(rows, obs_transfer, gpu, act_transfer)
        stages.shift(DOWN * 0.14)

        box = RoundedRectangle(
            width=6.45,
            height=2.55,
            corner_radius=0.08,
            fill_color=WHITE,
            fill_opacity=0.28,
            stroke_color=INK_MID,
            stroke_width=1.4,
        )
        box.move_to(LEFT * 2.1 + DOWN * 0.06)

        labels = VGroup(
            self.stage_label("Apply actions\n+ sim step", rows[0][0]),
            self.stage_label("Obs. + reward", rows[0][1]),
            self.stage_label("DNN forward", gpu),
        )
        transfer_tag = Text(
            "CPU \u2194 GPU copy every step",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=RED_ERROR,
            weight=BOLD,
        )
        transfer_tag.next_to(box, DOWN, buff=0.12)

        time_arrow = Arrow(
            box.get_corner(DL) + RIGHT * 0.22 + DOWN * 0.44,
            box.get_corner(DR) + LEFT * 0.22 + DOWN * 0.44,
            fill_color=ACCENT_BLUE,
            thickness=2.6,
            max_tip_length_to_length_ratio=0.08,
            buff=0,
        )
        time_label = VGroup()

        return VGroup(box, rows, obs_transfer, gpu, act_transfer, labels, transfer_tag, time_arrow, time_label)

    def build_gpu_preview(self):
        box = RoundedRectangle(
            width=3.55,
            height=2.18,
            corner_radius=0.08,
            fill_color=PASTEL_BLUE,
            fill_opacity=0.28,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.2,
            stroke_opacity=0.65,
        )
        box.move_to(RIGHT * 4.05 + DOWN * 0.05)
        blocks = VGroup()
        for i, label in enumerate(["sim", "obs", "DNN"]):
            cell = self.step_cell(label, width=0.86, height=1.25, fill=PASTEL_BLUE, stroke=ACCENT_BLUE, font_size=SIZE_MICRO)
            cell.move_to(box.get_left() + RIGHT * (0.67 + i * 0.98) + DOWN * 0.07)
            blocks.add(cell)
        title = Text("UrbanSim fix", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_BLUE, weight=BOLD)
        title.next_to(box, UP, buff=0.25)
        note = Text("GPU end-to-end", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        note.next_to(box, DOWN, buff=0.18)
        return VGroup(box, blocks, title, note).set_opacity(0.45)

    def build_progress(self):
        group = VGroup()
        title = Text("training time to high success", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        title.move_to(LEFT * 1.52 + DOWN * 1.78)
        group.add(title)

        specs = [
            ("5 GPU days", "79%", 0.72, ACCENT_AMBER),
            ("180 GPU-days", "95%", 3.55, RED_ERROR),
        ]
        for i, (label, pct, width, color) in enumerate(specs):
            y = -2.08 - i * 0.34
            track = RoundedRectangle(
                width=3.75,
                height=0.16,
                corner_radius=0.04,
                fill_color=LINE_GRID,
                fill_opacity=0.72,
                stroke_width=0,
            )
            track.move_to(LEFT * 1.42 + UP * y)
            fill = RoundedRectangle(
                width=width,
                height=0.16,
                corner_radius=0.04,
                fill_color=color,
                fill_opacity=0.86,
                stroke_color=color,
                stroke_width=0.8,
            )
            fill.move_to(track.get_left() + RIGHT * (width / 2))
            left_label = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
            left_label.next_to(track, LEFT, buff=0.18)
            value = Text(pct, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=color, weight=BOLD)
            value.next_to(track, RIGHT, buff=0.15)
            group.add(track, fill, left_label, value)

        return group

    def packet(self, color, start):
        pkt = RoundedRectangle(
            width=0.12,
            height=0.12,
            corner_radius=0.02,
            fill_color=color,
            fill_opacity=1.0,
            stroke_color=INK_DARK,
            stroke_width=0.6,
        )
        pkt.move_to(start)
        return pkt

    def build_cost_summary(self):
        card = RoundedRectangle(
            width=3.55,
            height=0.86,
            corner_radius=0.08,
            fill_color=PASTEL_PINK,
            fill_opacity=0.38,
            stroke_color=RED_ERROR,
            stroke_width=1.25,
            stroke_opacity=0.72,
        )
        number = Text("180", font=FONT_PRIMARY, font_size=46, color=RED_ERROR)
        label = Text(
            "GPU-days\nfor 95% success",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=INK_DARK,
        )
        content = VGroup(number, label).arrange(RIGHT, buff=0.24)
        content.move_to(card)
        return VGroup(card, content)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        subtitle = Text(
            "the algorithm is not the wall; the CPU-GPU hot loop is",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=RED_ERROR,
            slant=ITALIC,
        )
        subtitle.move_to(UP * 2.15)

        traditional = self.build_traditional_loop()
        traditional.shift(UP * 0.22)
        gpu_preview = self.build_gpu_preview()
        gpu_preview.shift(UP * 0.18)
        progress = self.build_progress()
        cost = self.build_cost_summary()
        cost.move_to(RIGHT * 4.05 + DOWN * 2.2)

        self.play(FadeIn(subtitle, shift=DOWN * 0.08), run_time=0.45)
        self.play(FadeIn(traditional[0]), FadeIn(traditional[5]), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(row, shift=RIGHT * 0.08) for row in traditional[1]), lag_ratio=0.09), run_time=0.65)
        self.play(FadeIn(traditional[2]), FadeIn(traditional[3]), FadeIn(traditional[4]), run_time=0.55)

        obs_start = traditional[1][1][1][0].get_right() + RIGHT * 0.04
        obs_end = traditional[3][0].get_left() + LEFT * 0.04
        act_start = traditional[3][0].get_right() + RIGHT * 0.04
        act_end = traditional[4][0].get_right() + LEFT * 0.08
        obs_pkt = self.packet(RED_ERROR, obs_start)
        act_pkt = self.packet(RED_ERROR, act_start)
        self.add(obs_pkt, act_pkt)
        self.play(
            obs_pkt.animate.move_to(obs_end),
            act_pkt.animate.move_to(act_end),
            run_time=0.75,
            rate_func=there_and_back,
        )
        self.play(
            Flash(traditional[2][0], color=RED_ERROR, line_length=0.18, num_lines=8),
            Flash(traditional[4][0], color=RED_ERROR, line_length=0.18, num_lines=8),
            FadeIn(traditional[6]),
            ShowCreation(traditional[7]),
            FadeIn(traditional[8]),
            run_time=0.8,
        )
        self.play(FadeOut(obs_pkt), FadeOut(act_pkt), FadeIn(progress), FadeIn(cost), run_time=0.75)
        self.play(FadeIn(gpu_preview, shift=LEFT * 0.08), run_time=0.55)
        self.wait(2.0)
        self._close()
