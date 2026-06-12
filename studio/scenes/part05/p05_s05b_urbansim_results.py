"""P05-S05b UrbanSim all-GPU training results."""
from manimlib import *

from studio.components import (
    StudioScene,
    BG_PAPER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_TEAL,
    ACCENT_BLUE,
    ACCENT_TEAL,
    ACCENT_GREEN,
    ACCENT_AMBER,
    GOLD_RICH,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
)

SCRIPT = """UrbanSim keeps simulation, observations, and inference on the GPU: 256 envs, 2,620 FPS, 11.2GB memory, and useful learning in three hours."""


class P05S05BUrbanSimResults(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "UrbanSim: 180 Days -> 3 Hours"

    def mini_env(self, idx, size=0.34):
        frame = RoundedRectangle(
            width=size,
            height=size,
            corner_radius=0.035,
            fill_color=PASTEL_GREEN if idx % 3 else PASTEL_TEAL,
            fill_opacity=0.72,
            stroke_color=ACCENT_GREEN,
            stroke_width=0.7,
            stroke_opacity=0.75,
        )
        road = Rectangle(
            width=size * 0.84,
            height=size * 0.16,
            fill_color="#D8E4E8",
            fill_opacity=0.9,
            stroke_width=0,
        )
        road.move_to(frame)
        if idx % 4 == 0:
            branch = Rectangle(width=size * 0.16, height=size * 0.75, fill_color="#D8E4E8", fill_opacity=0.9, stroke_width=0)
            branch.move_to(frame)
            road = VGroup(road, branch)
        car_color = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER][idx % 3]
        car = RoundedRectangle(
            width=size * 0.18,
            height=size * 0.09,
            corner_radius=0.015,
            fill_color=car_color,
            fill_opacity=0.78,
            stroke_width=0,
        )
        car.move_to(frame.get_center() + RIGHT * ((idx % 3) - 1) * size * 0.17)
        return VGroup(frame, road, car)

    def env_grid(self):
        tiles = VGroup()
        for r in range(8):
            for c in range(12):
                tile = self.mini_env(r * 12 + c)
                tile.move_to(RIGHT * (c - 5.5) * 0.39 + DOWN * (r - 3.5) * 0.39)
                tiles.add(tile)
        panel = RoundedRectangle(
            width=5.35,
            height=3.72,
            corner_radius=0.14,
            fill_color=PASTEL_GREEN,
            fill_opacity=0.18,
            stroke_color=ACCENT_GREEN,
            stroke_width=1.6,
        )
        tiles.shift(DOWN * 0.12)
        panel.move_to(tiles.get_center() + UP * 0.02)
        label = Text("256 parallel environments", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_GREEN, weight=BOLD)
        label.move_to(panel.get_top() + DOWN * 0.22)
        sub = Text("subset shown: heterogeneous scenes", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        sub.move_to(panel.get_bottom() + UP * 0.16)
        return VGroup(panel, tiles, label, sub)

    def gpu_engine(self):
        chip = RoundedRectangle(
            width=5.15,
            height=0.92,
            corner_radius=0.12,
            fill_color=interpolate_color(PASTEL_BLUE, WHITE, 0.25),
            fill_opacity=0.92,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.8,
        )
        cells = VGroup()
        for i, (name, color) in enumerate([("sim", ACCENT_GREEN), ("obs", ACCENT_TEAL), ("DNN", ACCENT_BLUE)]):
            cell = RoundedRectangle(
                width=1.35,
                height=0.48,
                corner_radius=0.08,
                fill_color=interpolate_color(color, WHITE, 0.78),
                fill_opacity=1,
                stroke_color=color,
                stroke_width=1.2,
            )
            txt = Text(name, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK, weight=BOLD)
            txt.move_to(cell)
            cells.add(VGroup(cell, txt))
        cells.arrange(RIGHT, buff=0.22)
        cells.move_to(chip)
        title = Text("GPU end-to-end hot loop", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_BLUE, weight=BOLD)
        title.next_to(chip, UP, buff=0.1)
        arrows = VGroup()
        for a, b in zip(cells[:-1], cells[1:]):
            arrows.add(Arrow(
                a.get_right() + RIGHT * 0.03,
                b.get_left() + LEFT * 0.03,
                fill_color=INK_MID,
                thickness=1.5,
                max_tip_length_to_length_ratio=0.22,
                buff=0,
            ))
        return VGroup(chip, cells, arrows, title)

    def metric_card(self, number, label, color, *, width=1.78):
        card = RoundedRectangle(
            width=width,
            height=0.82,
            corner_radius=0.09,
            fill_color=interpolate_color(color, WHITE, 0.83),
            fill_opacity=0.95,
            stroke_color=color,
            stroke_width=1.4,
        )
        n = Text(number, font=FONT_PRIMARY, font_size=25, color=color)
        l = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO - 1, color=INK_DARK)
        content = VGroup(n, l).arrange(DOWN, buff=0.05)
        content.move_to(card)
        return VGroup(card, content)

    def meters(self):
        fps = self.metric_card("2,620 FPS", "simulation throughput", GOLD_RICH)
        mem = self.metric_card("11.2 GB", "of 46 GB GPU memory", ACCENT_TEAL)
        hours = self.metric_card("3h", "wall-clock training", ACCENT_GREEN)
        cards = VGroup(fps, mem, hours).arrange(RIGHT, buff=0.12)

        mem_bar_bg = RoundedRectangle(width=1.42, height=0.1, corner_radius=0.03, fill_color=LINE_GRID, fill_opacity=0.85, stroke_width=0)
        mem_bar_fill = RoundedRectangle(width=1.42 * 0.243, height=0.1, corner_radius=0.03, fill_color=ACCENT_TEAL, fill_opacity=0.95, stroke_width=0)
        mem_bar_fill.move_to(mem_bar_bg.get_left() + RIGHT * (mem_bar_fill.get_width() / 2))
        mem_bar = VGroup(mem_bar_bg, mem_bar_fill)
        mem_bar.next_to(cards, DOWN, buff=0.14)
        mem_bar.align_to(mem, LEFT)
        pct = Text("24.3% used", font=FONT_PRIMARY, font_size=SIZE_MICRO - 1, color=INK_MID)
        pct.next_to(mem_bar, DOWN, buff=0.03)
        return VGroup(cards, mem_bar, pct)

    def performance_chart(self):
        values = [6, 18, 27, 41]
        labels = ["1", "64", "128", "256"]
        colors = [interpolate_color(ACCENT_BLUE, WHITE, 0.65), interpolate_color(ACCENT_BLUE, WHITE, 0.45), interpolate_color(ACCENT_BLUE, WHITE, 0.25), ACCENT_BLUE]
        width, height = 4.6, 1.55
        baseline = Line(LEFT * width / 2, RIGHT * width / 2, stroke_color=INK_MID, stroke_width=1.4)
        bars = VGroup()
        texts = VGroup()
        for i, (v, lbl, color) in enumerate(zip(values, labels, colors)):
            x = -width / 2 + (i + 0.5) * width / 4
            h = height * v / 45
            bar = Rectangle(
                width=0.58,
                height=h,
                fill_color=color,
                fill_opacity=0.9,
                stroke_color=color,
                stroke_width=1.0,
            )
            bar.move_to(np.array([x, h / 2, 0]))
            pct = Text(f"{v}%", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK, weight=BOLD)
            pct.next_to(bar, UP, buff=0.06)
            lab = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
            lab.next_to(np.array([x, 0, 0]), DOWN, buff=0.1)
            bars.add(bar)
            texts.add(pct, lab)
        title = Text("success rate after 3 hours", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        title.next_to(VGroup(baseline, bars), UP, buff=0.18)
        xlabel = Text("parallel environments", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        xlabel.next_to(baseline, DOWN, buff=0.36)
        chart = VGroup(baseline, bars, texts, title, xlabel)
        return chart

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        subtitle = Text(
            "keep the whole training loop on one GPU, then multiply environments",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=ACCENT_GREEN,
            slant=ITALIC,
        )
        subtitle.move_to(UP * 2.15)

        engine = self.gpu_engine()
        engine.scale(0.88)
        engine.move_to(LEFT * 3.25 + UP * 1.18)
        grid = self.env_grid()
        grid.scale(0.72)
        grid.move_to(LEFT * 3.25 + DOWN * 1.05)
        metrics = self.meters()
        metrics.move_to(RIGHT * 3.35 + UP * 1.08)
        chart = self.performance_chart()
        chart.scale(0.95)
        chart.move_to(RIGHT * 3.35 + DOWN * 1.45)
        engine_to_grid = Arrow(
            engine[0].get_bottom() + DOWN * 0.02,
            grid[0].get_top() + UP * 0.02,
            fill_color=ACCENT_GREEN,
            thickness=1.6,
            max_tip_length_to_length_ratio=0.18,
            buff=0.03,
        )

        self.play(FadeIn(subtitle, shift=DOWN * 0.08), run_time=0.45)
        self.play(FadeIn(engine[0]), FadeIn(engine[1]), FadeIn(engine[3]), ShowCreation(engine[2]), run_time=0.75)

        packet = Dot(radius=0.055, color=ACCENT_GREEN)
        packet.move_to(engine[1][0].get_center())
        self.add(packet)
        loop_path = VMobject()
        loop_path.set_points_smoothly([
            engine[1][0].get_center(),
            engine[1][1].get_center(),
            engine[1][2].get_center(),
            engine[1][0].get_center() + DOWN * 0.38,
            engine[1][0].get_center(),
        ])
        self.play(MoveAlongPath(packet, loop_path), run_time=1.0, rate_func=linear)
        self.play(FadeOut(packet), run_time=0.15)

        self.play(ShowCreation(engine_to_grid), FadeIn(grid[0]), run_time=0.35)
        self.play(LaggedStart(*(FadeIn(t, scale=0.55) for t in grid[1]), lag_ratio=0.006), run_time=1.0)
        self.play(FadeIn(grid[2]), FadeIn(grid[3]), run_time=0.35)
        self.play(LaggedStart(*(FadeIn(m, shift=LEFT * 0.06) for m in metrics[0]), lag_ratio=0.12), run_time=0.8)
        self.play(FadeIn(metrics[1]), FadeIn(metrics[2]), run_time=0.35)
        self.play(FadeIn(chart[0]), LaggedStart(*(GrowFromEdge(b, DOWN) for b in chart[1]), lag_ratio=0.08), run_time=0.85)
        self.play(FadeIn(VGroup(chart[2], chart[3], chart[4])), run_time=0.45)
        self.wait(2.0)
        self._close()
