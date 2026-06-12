"""P05-S04c MetaUrban scaling charts from the source slide."""
from manimlib import *

from studio.components import (
    StudioScene,
    BG_PAPER,
    ACCENT_BLUE,
    ACCENT_AMBER,
    GOLD_RICH,
    PASTEL_AMBER,
    INK_DARK,
    INK_MID,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
)

SCRIPT = """Adding more training environments improves unseen performance as a power law."""


class P05S04CMetaUrbanScaling(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Diversity Scaling"

    def chart_axes(self, width=4.4, height=2.55):
        origin = LEFT * width / 2 + DOWN * height / 2
        x_axis = Line(origin, origin + RIGHT * width, stroke_color=INK_MID, stroke_width=2.1)
        y_axis = Line(origin, origin + UP * height, stroke_color=INK_MID, stroke_width=2.1)
        grid = VGroup()
        for i in range(1, 5):
            x = origin[0] + width * i / 5
            grid.add(Line(
                np.array([x, origin[1], 0]),
                np.array([x, origin[1] + height, 0]),
                stroke_color=LINE_GRID,
                stroke_width=0.8,
                stroke_opacity=0.6,
            ))
        for i in range(1, 5):
            y = origin[1] + height * i / 5
            grid.add(Line(
                np.array([origin[0], y, 0]),
                np.array([origin[0] + width, y, 0]),
                stroke_color=LINE_GRID,
                stroke_width=0.8,
                stroke_opacity=0.6,
            ))
        return VGroup(grid, x_axis, y_axis)

    def left_chart(self):
        width, height = 4.55, 2.65
        axes = self.chart_axes(width, height)
        origin = axes[1].get_start()

        xs = [1, 4, 8, 16, 32]
        x_pos = {x: origin[0] + width * i / (len(xs) - 1) for i, x in enumerate(xs)}

        def p(x, y):
            return np.array([x_pos[x], origin[1] + height * y / 0.5, 0])

        blue = [(1, 0.0), (4, 0.025), (8, 0.14), (16, 0.245), (32, 0.42)]
        red = [(1, 0.0), (4, 0.01), (8, 0.03), (16, 0.04), (32, 0.048)]

        blue_line = VMobject(stroke_color=ACCENT_BLUE, stroke_width=3.0)
        blue_line.set_points_smoothly([p(x, y) for x, y in blue])
        red_line = VMobject(stroke_color="#9B1C12", stroke_width=2.5)
        red_line.set_points_smoothly([p(x, y) for x, y in red])

        dots = VGroup()
        for x, y in blue:
            d = Circle(radius=0.06, fill_color=ACCENT_BLUE, fill_opacity=1, stroke_color=WHITE, stroke_width=0.7)
            d.move_to(p(x, y))
            dots.add(d)
        for x, y in red:
            d = Circle(radius=0.055, fill_color="#9B1C12", fill_opacity=1, stroke_color=WHITE, stroke_width=0.65)
            d.move_to(p(x, y))
            dots.add(d)

        labels = VGroup()
        for x in xs:
            t = Text(str(x), font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
            t.next_to(np.array([x_pos[x], origin[1], 0]), DOWN, buff=0.13)
            labels.add(t)
        for y in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
            t = Text(f"{y:.1f}", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
            t.move_to(np.array([origin[0], origin[1] + height * y / 0.5, 0]))
            t.align_to(np.array([origin[0], 0, 0]), RIGHT)
            t.shift(LEFT * 0.18)
            labels.add(t)

        title = Text(
            "Performance with more unique layouts",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_DARK,
            weight=BOLD,
        )
        title.next_to(axes, UP, buff=0.2)

        xlabel = Text("Number of Training Layouts", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
        xlabel.next_to(axes[1], DOWN, buff=0.46)
        ylabel = Text("Success Rate", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
        ylabel.rotate(90 * DEGREES)
        ylabel.next_to(axes[2], LEFT, buff=0.45)

        legend_box = RoundedRectangle(
            width=2.0,
            height=0.55,
            corner_radius=0.04,
            fill_color=WHITE,
            fill_opacity=0.82,
            stroke_color=INK_MID,
            stroke_width=0.8,
        )
        legend_box.move_to(axes.get_corner(UL) + RIGHT * 1.08 + DOWN * 0.28)
        legend_items = VGroup()
        for i, (name, color) in enumerate([("UrbanVerse", ACCENT_BLUE), ("MetaUrban (PG)", "#9B1C12")]):
            sample = Line(LEFT * 0.13, RIGHT * 0.13, stroke_color=color, stroke_width=2.4)
            sample.add(Dot(sample.get_center(), radius=0.035, color=color))
            text = Text(name, font=FONT_PRIMARY, font_size=SIZE_MICRO - 2, color=INK_DARK)
            item = VGroup(sample, text).arrange(RIGHT, buff=0.08)
            item.move_to(legend_box.get_left() + RIGHT * 0.75 + UP * (0.12 - i * 0.22), aligned_edge=LEFT)
            legend_items.add(item)

        return VGroup(axes, labels, title, xlabel, ylabel, legend_box, legend_items, blue_line, red_line, dots)

    def right_chart(self):
        width, height = 4.35, 2.65
        axes = self.chart_axes(width, height)
        origin = axes[1].get_start()

        def xmap(x):
            return origin[0] + width * (x - 1) / 4

        def ymap(error):
            # log10 axis from 10^-1 to 10^0, mapped to 0..1.
            return origin[1] + height * (np.log10(error) + 1.0)

        def p(x, error):
            return np.array([xmap(x), ymap(error), 0])

        points = [(1, 0.72), (2, 0.58), (3, 0.38), (4, 0.17), (5, 0.10)]
        fit_points = [p(x, e) for x, e in [(1, 0.82), (2, 0.52), (3, 0.30), (4, 0.17), (5, 0.11)]]
        fit = VGroup()
        for a, b in zip(fit_points, fit_points[1:]):
            fit.add(DashedLine(
                a,
                b,
                dash_length=0.12,
                stroke_color=ACCENT_AMBER,
                stroke_width=2.6,
                stroke_opacity=0.9,
            ))

        dots = VGroup()
        for x, e in points:
            d = Circle(radius=0.08, fill_color=ACCENT_AMBER, fill_opacity=1, stroke_color=WHITE, stroke_width=0.8)
            d.move_to(p(x, e))
            dots.add(d)

        labels = VGroup()
        for x in range(1, 6):
            t = Text(str(x), font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
            t.next_to(np.array([xmap(x), origin[1], 0]), DOWN, buff=0.13)
            labels.add(t)
        for val, lbl in [(1.0, "10^0"), (0.1, "10^-1")]:
            t = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
            t.move_to(np.array([origin[0], ymap(val), 0]))
            t.align_to(np.array([origin[0], 0, 0]), RIGHT)
            t.shift(LEFT * 0.24)
            labels.add(t)

        title = Text(
            "Power-law scaling between data size and error",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_DARK,
            weight=BOLD,
        )
        title.next_to(axes, UP, buff=0.2)
        xlabel = Text("Training layouts + cousins", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
        xlabel.next_to(axes[1], DOWN, buff=0.46)
        ylabel = Text("Error (1 - SR)", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
        ylabel.rotate(90 * DEGREES)
        ylabel.next_to(axes[2], LEFT, buff=0.45)

        fit_box = RoundedRectangle(
            width=2.25,
            height=0.55,
            corner_radius=0.04,
            fill_color=WHITE,
            fill_opacity=0.85,
            stroke_color=INK_MID,
            stroke_width=0.8,
        )
        fit_box.move_to(axes.get_corner(UR) + LEFT * 1.16 + DOWN * 0.28)
        fit_text = Text("E = 1.001 · N^-0.003\nPearson r = -0.903", font=FONT_PRIMARY, font_size=SIZE_MICRO - 2, color=INK_DARK)
        fit_text.move_to(fit_box)

        legend = Text("PPO-UrbanVerse on CraftBench", font=FONT_PRIMARY, font_size=SIZE_MICRO - 1, color=INK_DARK)
        legend_box = RoundedRectangle(
            width=2.55,
            height=0.32,
            corner_radius=0.04,
            fill_color=WHITE,
            fill_opacity=0.78,
            stroke_color=INK_MID,
            stroke_width=0.7,
        )
        legend_box.move_to(axes.get_corner(DL) + RIGHT * 1.42 + UP * 0.18)
        dot = Dot(radius=0.045, color=ACCENT_AMBER)
        legend_group = VGroup(dot, legend).arrange(RIGHT, buff=0.08)
        legend_group.move_to(legend_box)

        return VGroup(axes, labels, title, xlabel, ylabel, fit_box, fit_text, legend_box, legend_group, fit, dots)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        subtitle = Text(
            "Adding more training environments improves performance as a power law",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color="#B01818",
            slant=ITALIC,
        )
        subtitle.move_to(UP * 2.22)

        left = self.left_chart()
        right = self.right_chart()
        left.scale(0.86).move_to(LEFT * 3.0 + DOWN * 0.1)
        right.scale(0.86).move_to(RIGHT * 3.05 + DOWN * 0.1)

        settings = Text(
            "Urban micromobility · UrbanVerse-Unseen · RL (PPO) · Success Rate",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=INK_MID,
        )
        settings.move_to(DOWN * 2.55)

        conclusion = Text(
            "layout/content diversity matters more than repeated scenes",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=GOLD_RICH,
            weight=BOLD,
        )
        conclusion.next_to(settings, UP, buff=0.24)

        self.play(FadeIn(subtitle, shift=DOWN * 0.08), run_time=0.45)
        self.play(
            ShowCreation(left[0][1]),
            ShowCreation(left[0][2]),
            ShowCreation(right[0][1]),
            ShowCreation(right[0][2]),
            FadeIn(VGroup(left[1], right[1], left[2], right[2], left[3], right[3], left[4], right[4])),
            run_time=0.8,
        )
        self.play(
            FadeIn(VGroup(left[5], left[6], right[5], right[6], right[7], right[8])),
            ShowCreation(left[7]),
            ShowCreation(left[8]),
            ShowCreation(right[9]),
            run_time=1.1,
        )
        self.play(FadeIn(left[9]), FadeIn(right[10]), run_time=0.55)
        self.play(FadeIn(conclusion, shift=UP * 0.08), FadeIn(settings), run_time=0.55)
        self.wait(2.0)
        self._close()
