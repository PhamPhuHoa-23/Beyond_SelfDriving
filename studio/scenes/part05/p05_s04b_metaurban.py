"""P05-S04b MetaUrban procedural generator."""
from manimlib import *

from studio.components import (
    StudioScene,
    BG_PAPER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_PINK,
    ACCENT_BLUE,
    ACCENT_TEAL,
    ACCENT_GREEN,
    ACCENT_AMBER,
    ACCENT_PINK,
    GOLD_RICH,
    CYAN_RADAR,
    INK_DARK,
    INK_MID,
    INK_LIGHT,
    LINE_GRID,
    FONT_PRIMARY,
    FONT_MONO,
    SIZE_H1,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    vehicle_icon,
    pedestrian_icon,
)

SCRIPT = (
    "MetaUrban generates urban scenes from a description script: block layout, "
    "intersections, sidewalks, and objects. No two scenes are alike."
)


class P05S04BMetaUrban(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "MetaUrban Generator"

    def terminal(self):
        panel = RoundedRectangle(
            width=3.65,
            height=2.45,
            corner_radius=0.12,
            fill_color="#122033",
            fill_opacity=0.96,
            stroke_color=ACCENT_TEAL,
            stroke_width=1.6,
        )
        dots = VGroup()
        for i, color in enumerate([ACCENT_PINK, ACCENT_AMBER, ACCENT_GREEN]):
            dot = Circle(
                radius=0.045,
                fill_color=color,
                fill_opacity=1,
                stroke_color=color,
                stroke_width=0,
            )
            dot.move_to(panel.get_corner(UL) + RIGHT * (0.22 + i * 0.18) + DOWN * 0.2)
            dots.add(dot)

        lines = [
            "$ generate_scene(",
            "  blocks = 4",
            "  intersection = 'T'",
            "  lane_width = 3.2",
            "  objects = trees + benches",
            "  density = medium",
            ")",
        ]
        text_lines = VGroup()
        for i, line in enumerate(lines):
            color = ACCENT_GREEN if i == 0 else interpolate_color(WHITE, ACCENT_TEAL, 0.15)
            t = Text(line, font=FONT_MONO, font_size=15, color=color)
            t.set_color(color)
            t.move_to(panel.get_left() + RIGHT * 0.28 + UP * (0.74 - i * 0.28), aligned_edge=LEFT)
            text_lines.add(t)

        caption = Text(
            "description script",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=ACCENT_TEAL,
        )
        caption.next_to(panel, DOWN, buff=0.12)
        return VGroup(panel, dots, text_lines, caption)

    def gear(self):
        core = Circle(
            radius=0.46,
            fill_color=CYAN_RADAR,
            fill_opacity=0.18,
            stroke_color=CYAN_RADAR,
            stroke_width=2.2,
        )
        ring = Circle(
            radius=0.67,
            stroke_color=CYAN_RADAR,
            stroke_width=1.2,
            stroke_opacity=0.55,
        )
        teeth = VGroup()
        for i in range(10):
            tooth = RoundedRectangle(
                width=0.12,
                height=0.24,
                corner_radius=0.025,
                fill_color=CYAN_RADAR,
                fill_opacity=0.7,
                stroke_width=0,
            )
            tooth.move_to(UP * 0.66)
            tooth.rotate(i * TAU / 10, about_point=ORIGIN)
            teeth.add(tooth)
        spark = VGroup()
        for angle in np.linspace(0, TAU, 6, endpoint=False):
            dot = Circle(
                radius=0.04,
                fill_color=ACCENT_AMBER,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=0.8,
            )
            dot.move_to(np.array([np.cos(angle), np.sin(angle), 0]) * 0.27)
            spark.add(dot)
        label = Text("procedural\nengine", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        label.next_to(core, DOWN, buff=0.34)
        gear = VGroup(ring, teeth, core, spark)
        return VGroup(gear, label)

    def scene_tile(self, variant, label):
        frame = RoundedRectangle(
            width=3.0,
            height=1.9,
            corner_radius=0.1,
            fill_color=interpolate_color(PASTEL_GREEN, WHITE, 0.22),
            fill_opacity=0.96,
            stroke_color=[ACCENT_TEAL, ACCENT_AMBER, ACCENT_PINK][variant % 3],
            stroke_width=1.8,
        )
        center = frame.get_center()

        roads = VGroup()
        if variant == 0:
            roads.add(Rectangle(width=2.75, height=0.38, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0))
            roads.add(Rectangle(width=0.42, height=1.62, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0))
            roads.move_to(center)
        elif variant == 1:
            road1 = Rectangle(width=2.65, height=0.34, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0)
            road1.rotate(12 * DEGREES)
            road2 = Rectangle(width=0.38, height=1.55, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0)
            road2.move_to(center + RIGHT * 0.55)
            roads.add(road1, road2)
        else:
            roads.add(Rectangle(width=2.7, height=0.34, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0))
            branch = Rectangle(width=1.35, height=0.32, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0)
            branch.rotate(-42 * DEGREES)
            branch.move_to(center + LEFT * 0.45 + UP * 0.32)
            roads.add(branch)
            roads.move_to(center)

        lanes = VGroup()
        for dx in [-0.65, 0.0, 0.65]:
            line = Line(LEFT * 0.16, RIGHT * 0.16, stroke_color=WHITE, stroke_width=1.2, stroke_opacity=0.9)
            line.move_to(center + RIGHT * dx)
            lanes.add(line)

        buildings = VGroup()
        building_specs = [
            (-1.02, 0.58, ACCENT_BLUE), (1.08, 0.56, ACCENT_AMBER),
            (-1.08, -0.58, ACCENT_PINK), (1.02, -0.58, ACCENT_TEAL),
        ]
        if variant == 1:
            building_specs = [(-1.15, 0.48, ACCENT_AMBER), (0.15, 0.62, ACCENT_PINK), (-0.95, -0.58, ACCENT_TEAL), (1.13, -0.42, ACCENT_BLUE)]
        elif variant == 2:
            building_specs = [(-1.18, 0.62, ACCENT_TEAL), (0.95, 0.6, ACCENT_BLUE), (-0.2, -0.62, ACCENT_AMBER), (1.16, -0.58, ACCENT_PINK)]
        for x, y, color in building_specs:
            b = RoundedRectangle(
                width=0.58,
                height=0.32,
                corner_radius=0.04,
                fill_color=interpolate_color(color, WHITE, 0.82),
                fill_opacity=0.92,
                stroke_color=color,
                stroke_width=1.2,
                stroke_opacity=0.82,
            )
            b.move_to(center + RIGHT * x + UP * y)
            buildings.add(b)

        objects = VGroup()
        object_points = [
            (-0.92, 0.05, ACCENT_GREEN),
            (-0.38, -0.42, ACCENT_AMBER),
            (0.72, 0.18, ACCENT_PINK),
            (1.16, -0.04, ACCENT_GREEN),
        ]
        for x, y, color in object_points[: 2 + variant]:
            obj = Dot(radius=0.05, color=color)
            obj.move_to(center + RIGHT * x + UP * y)
            objects.add(obj)

        car = vehicle_icon(color=ACCENT_PINK, scale=0.22)
        car.move_to(center + RIGHT * (0.5 - variant * 0.28) + DOWN * 0.02)
        walker = pedestrian_icon(color=ACCENT_AMBER).scale(0.18)
        walker.move_to(center + LEFT * 0.68 + UP * (0.22 - variant * 0.08))

        title = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        title.next_to(frame, UP, buff=0.16)
        scene = VGroup(frame, roads, lanes, buildings, objects, car, walker)
        return VGroup(title, scene)

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        terminal = self.terminal()
        terminal.move_to(LEFT * 4.35 + UP * 0.32)

        engine = self.gear()
        engine.move_to(LEFT * 0.8 + UP * 0.18)

        scene1 = self.scene_tile(0, "scene 1")
        scene2 = self.scene_tile(1, "scene 2")
        scene3 = self.scene_tile(2, "scene 3")
        scenes = [scene1, scene2, scene3]
        for scene in scenes:
            scene.move_to(RIGHT * 3.65 + UP * 0.34)

        flow_y = engine[0].get_center()[1]
        input_arrow = Arrow(
            np.array([terminal.get_right()[0] + 0.12, flow_y, 0]),
            np.array([engine[0].get_left()[0] - 0.08, flow_y, 0]),
            fill_color=ACCENT_TEAL,
            thickness=2.2,
            buff=0,
        )
        output_arrow = Arrow(
            np.array([engine[0].get_right()[0] + 0.1, flow_y, 0]),
            np.array([scene1[1].get_left()[0] - 0.1, flow_y, 0]),
            fill_color=ACCENT_PINK,
            thickness=2.2,
            buff=0,
        )

        chips = VGroup()
        for label, color in [
            ("layout", ACCENT_TEAL),
            ("lanes", ACCENT_BLUE),
            ("sidewalks", ACCENT_AMBER),
            ("objects", ACCENT_PINK),
        ]:
            chip = RoundedRectangle(
                width=0.86,
                height=0.33,
                corner_radius=0.08,
                fill_color=interpolate_color(color, WHITE, 0.82),
                fill_opacity=0.92,
                stroke_color=color,
                stroke_width=1.1,
            )
            txt = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
            txt.move_to(chip)
            chips.add(VGroup(chip, txt))
        chips.arrange(RIGHT, buff=0.14)
        chips.move_to(LEFT * 4.35 + DOWN * 1.28)

        counter = Text("scene 1  \u2192  2  \u2192  3  \u2192  ...  \u2192  infinite", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        counter.move_to(RIGHT * 3.65 + DOWN * 1.52)
        punch_left = Text("Diversity", font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH)
        punch_left.set_color(GOLD_RICH)
        punch_mid = Text(">", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_DARK)
        punch_right = Text("Quantity", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_LIGHT)
        punch = VGroup(punch_left, punch_mid, punch_right).arrange(RIGHT, buff=0.18)
        punch.move_to(DOWN * 2.05)

        self.play(FadeIn(terminal, shift=RIGHT * 0.08), run_time=0.35)
        self.play(LaggedStart(*(FadeIn(chip, shift=UP * 0.05) for chip in chips), lag_ratio=0.06), run_time=0.35)
        self.play(FadeIn(engine), ShowCreation(input_arrow), run_time=0.55)

        packets = VGroup()
        packet_anims = []
        for i, chip in enumerate(chips):
            color = [ACCENT_TEAL, ACCENT_BLUE, ACCENT_AMBER, ACCENT_PINK][i]
            packet = RoundedRectangle(
                width=0.13,
                height=0.13,
                corner_radius=0.025,
                fill_color=color,
                fill_opacity=1,
                stroke_color=INK_DARK,
                stroke_width=0.8,
            )
            offset = (i - 1.5) * 0.12
            packet.move_to(np.array([terminal.get_right()[0] + 0.18, flow_y + offset, 0]))
            path = Line(
                np.array([terminal.get_right()[0] + 0.18, flow_y + offset, 0]),
                np.array([engine[0].get_left()[0] - 0.1, flow_y + offset, 0]),
            )
            packets.add(packet)
            packet_anims.append(MoveAlongPath(packet, path, rate_func=smooth))
        self.add(packets)
        self.play(
            Rotate(engine[0], angle=TAU, run_time=1.2, rate_func=linear),
            LaggedStart(*packet_anims, lag_ratio=0.08),
            run_time=1.2,
        )
        self.play(FadeOut(packets, scale=0.5), ShowCreation(output_arrow), run_time=0.3)

        current = scene1
        self.play(FadeIn(current, scale=1.04), FadeIn(counter), run_time=0.65)
        for next_scene in [scene2, scene3]:
            self.play(
                Rotate(engine[0], angle=PI, run_time=0.45, rate_func=linear),
                ReplacementTransform(current, next_scene),
                run_time=0.55,
            )
            current = next_scene

        thumbnails = VGroup(
            self.scene_tile(0, "A").scale(0.52),
            self.scene_tile(1, "B").scale(0.52),
            self.scene_tile(2, "C").scale(0.52),
        )
        for thumb in thumbnails:
            thumb[0].set_opacity(0)
        thumbnails.arrange(RIGHT, buff=0.16)
        thumbnails.move_to(RIGHT * 3.65 + DOWN * 0.64)
        self.play(
            current.animate.scale(0.78).move_to(RIGHT * 3.65 + UP * 0.78),
            FadeIn(thumbnails, shift=UP * 0.08),
            FadeIn(punch, shift=UP * 0.1),
            run_time=0.75,
        )
        self.wait(2.0)
        self._close()
