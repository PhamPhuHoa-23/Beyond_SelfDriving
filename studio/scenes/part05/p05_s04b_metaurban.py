"""P05-S04b MetaUrban procedural generator."""
from manimlib import *

from studio.components import (
    StudioScene,
    BG_PAPER,
    PASTEL_BLUE,
    PASTEL_TEAL,
    PASTEL_GREEN,
    PASTEL_AMBER,
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
    contribution_badge,
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
            t = Text(line, font=FONT_MONO, font_size=14, color=color)
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
        
        # Gold Spotlight Badge
        spotlight = contribution_badge("ICLR 2025 Spotlight", color=GOLD_RICH)
        spotlight.scale(0.85)
        spotlight.move_to(panel.get_top() + UP * 0.18)
        
        return VGroup(panel, dots, text_lines, caption, spotlight)

    def engine(self):
        housing = RoundedRectangle(
            width=1.4,
            height=1.4,
            corner_radius=0.25,
            fill_color=PASTEL_PINK,
            fill_opacity=0.18,
            stroke_color=ACCENT_PINK,
            stroke_width=2.5,
        )
        
        # Central gear
        core = Circle(
            radius=0.18,
            fill_color=ACCENT_PINK,
            fill_opacity=0.9,
            stroke_color=INK_DARK,
            stroke_width=1.5,
        )
        ring = Circle(
            radius=0.36,
            stroke_color=INK_DARK,
            stroke_width=2.0,
        )
        teeth = VGroup()
        for i in range(8):
            tooth = Polygon(
                np.array([-0.09, 0, 0]),
                np.array([0.09, 0, 0]),
                np.array([0.06, 0.18, 0]),
                np.array([-0.06, 0.18, 0]),
                stroke_color=INK_DARK,
                stroke_width=1.8,
                fill_color=ACCENT_PINK,
                fill_opacity=1.0,
            )
            tooth.move_to(UP * 0.36)
            tooth.rotate(i * TAU / 8, about_point=ORIGIN)
            teeth.add(tooth)
            
        gear = VGroup(ring, teeth, core)
        
        # Input funnel (left)
        funnel = Polygon(
            np.array([-0.25, 0.22, 0]),
            np.array([0.0, 0.1, 0]),
            np.array([0.0, -0.1, 0]),
            np.array([-0.25, -0.22, 0]),
            stroke_color=INK_DARK,
            stroke_width=2.0,
            fill_color=PASTEL_PINK,
            fill_opacity=0.6,
        )
        funnel.next_to(housing, LEFT, buff=-0.08)
        
        # Emitter slot (right)
        emitter = Rectangle(
            width=0.2,
            height=0.3,
            stroke_color=INK_DARK,
            stroke_width=2.0,
            fill_color=PASTEL_PINK,
            fill_opacity=0.6,
        )
        emitter.next_to(housing, RIGHT, buff=-0.08)
        
        # Seed die
        die_box = RoundedRectangle(
            width=0.28,
            height=0.28,
            corner_radius=0.06,
            fill_color=WHITE,
            fill_opacity=0.95,
            stroke_color=INK_DARK,
            stroke_width=1.5,
        )
        die_box.move_to(housing.get_top() + UP * 0.12)
        
        dots = VGroup()
        for x, y in [(-0.06, 0.06), (0.06, 0.06), (-0.06, -0.06), (0.06, -0.06), (0, 0)]:
            dots.add(Circle(radius=0.02, fill_color=ACCENT_PINK, stroke_width=0).move_to(die_box.get_center() + RIGHT * x + UP * y))
            
        die = VGroup(die_box, dots)
        
        label = Text("procedural engine", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK)
        label.next_to(housing, DOWN, buff=0.3)
        
        engine_group = VGroup(housing, funnel, emitter, gear, die, label)
        return engine_group

    def scene_tile(self, variant, label):
        frame = RoundedRectangle(
            width=3.0,
            height=1.9,
            corner_radius=0.1,
            fill_color=PASTEL_GREEN,
            fill_opacity=0.96,
            stroke_color=[ACCENT_TEAL, ACCENT_AMBER, ACCENT_PINK][variant % 3],
            stroke_width=1.8,
        )
        center = frame.get_center()

        # Helper to make vector trees and benches
        def make_tree(pt):
            trunk = Rectangle(width=0.03, height=0.06, fill_color="#8B5A2B", fill_opacity=1.0, stroke_width=0)
            trunk.move_to(pt + DOWN * 0.04)
            canopy = Circle(radius=0.08, fill_color=ACCENT_GREEN, fill_opacity=0.9, stroke_color=INK_DARK, stroke_width=0.6)
            canopy.move_to(pt)
            return VGroup(trunk, canopy)

        def make_bench(pt, rot=0):
            b = Rectangle(width=0.14, height=0.06, fill_color=ACCENT_AMBER, fill_opacity=0.9, stroke_color=INK_DARK, stroke_width=0.6)
            b.rotate(rot)
            b.move_to(pt)
            return b

        # 1. Plots (city blocks)
        plots = VGroup()
        if variant == 0:
            for x, y in [(-0.85, 0.52), (0.85, 0.52), (-0.85, -0.52), (0.85, -0.52)]:
                plots.add(RoundedRectangle(
                    width=0.85, height=0.46, corner_radius=0.04,
                    fill_color=interpolate_color(PASTEL_BLUE, WHITE, 0.4), fill_opacity=0.9,
                    stroke_color=ACCENT_BLUE, stroke_width=1.0
                ).move_to(center + RIGHT * x + UP * y))
        elif variant == 1:
            for x, y in [(-0.82, 0.52), (0.82, 0.52), (-0.82, -0.52), (0.82, -0.52)]:
                plots.add(RoundedRectangle(
                    width=0.75, height=0.42, corner_radius=0.04,
                    fill_color=interpolate_color(PASTEL_PINK, WHITE, 0.4), fill_opacity=0.9,
                    stroke_color=ACCENT_PINK, stroke_width=1.0
                ).move_to(center + RIGHT * x + UP * y))
        else:
            for x, y in [(-0.85, 0.54), (0.85, 0.54), (-0.85, -0.54), (0.85, -0.54)]:
                plots.add(RoundedRectangle(
                    width=0.8, height=0.44, corner_radius=0.04,
                    fill_color=interpolate_color(PASTEL_AMBER, WHITE, 0.4), fill_opacity=0.9,
                    stroke_color=ACCENT_AMBER, stroke_width=1.0
                ).move_to(center + RIGHT * x + UP * y))

        # 2. Sidewalks (margins around roads)
        sidewalks = VGroup()
        if variant == 0:
            sidewalks.add(Rectangle(width=2.85, height=0.48, fill_color="#B8C4CC", fill_opacity=1, stroke_width=0).move_to(center))
            sidewalks.add(Rectangle(width=0.48, height=1.0, fill_color="#B8C4CC", fill_opacity=1, stroke_width=0).move_to(center + DOWN * 0.45))
        elif variant == 1:
            sidewalks.add(Rectangle(width=2.75, height=0.44, fill_color="#B8C4CC", fill_opacity=1, stroke_width=0).move_to(center))
            sidewalks.add(Rectangle(width=0.44, height=1.7, fill_color="#B8C4CC", fill_opacity=1, stroke_width=0).move_to(center))
        else:
            sidewalks.add(Rectangle(width=2.8, height=0.44, fill_color="#B8C4CC", fill_opacity=1, stroke_width=0).move_to(center))
            sidewalks.add(Rectangle(width=0.44, height=1.7, fill_color="#B8C4CC", fill_opacity=1, stroke_width=0).move_to(center))
            sidewalks.add(Circle(radius=0.62, fill_color="#B8C4CC", fill_opacity=1, stroke_width=0).move_to(center))

        # 3. Roads
        roads = VGroup()
        if variant == 0:
            roads.add(Rectangle(width=2.85, height=0.38, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0).move_to(center))
            roads.add(Rectangle(width=0.38, height=0.95, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0).move_to(center + DOWN * 0.475))
        elif variant == 1:
            roads.add(Rectangle(width=2.75, height=0.34, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0).move_to(center))
            roads.add(Rectangle(width=0.34, height=1.7, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0).move_to(center))
        else:
            roads.add(Rectangle(width=2.8, height=0.34, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0).move_to(center))
            roads.add(Rectangle(width=0.34, height=1.7, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0).move_to(center))
            roads.add(Circle(radius=0.54, fill_color="#C9D8DF", fill_opacity=1, stroke_width=0).move_to(center))
            roads.add(Circle(radius=0.32, fill_color=interpolate_color(PASTEL_GREEN, WHITE, 0.22), stroke_color=INK_DARK, stroke_width=1.0, fill_opacity=1.0).move_to(center))

        # 4. Lanes
        lanes = VGroup()
        if variant == 0:
            lanes.add(DashedLine(center + LEFT * 1.35, center + RIGHT * 1.35, stroke_color=WHITE, stroke_width=1.2, dash_length=0.1, buff=0))
            lanes.add(DashedLine(center, center + DOWN * 0.85, stroke_color=WHITE, stroke_width=1.2, dash_length=0.1, buff=0))
        elif variant == 1:
            lanes.add(DashedLine(center + LEFT * 1.35, center + RIGHT * 1.35, stroke_color=WHITE, stroke_width=1.2, dash_length=0.1, buff=0))
            lanes.add(DashedLine(center + UP * 0.85, center + DOWN * 0.85, stroke_color=WHITE, stroke_width=1.2, dash_length=0.1, buff=0))
        else:
            circle_path = Circle(radius=0.43).move_to(center)
            lanes.add(DashedVMobject(circle_path, num_dashes=16, stroke_color=WHITE, stroke_width=1.2))

        # 5. Vegetation (trees)
        vegetation = VGroup()
        if variant == 0:
            for pt in [center + LEFT * 1.1 + UP * 0.6, center + RIGHT * 1.1 + UP * 0.6, center + RIGHT * 1.1 + DOWN * 0.6]:
                vegetation.add(make_tree(pt))
        elif variant == 1:
            for pt in [center + LEFT * 1.1 + UP * 0.68, center + LEFT * 0.6 + UP * 0.68, center + RIGHT * 1.1 + UP * 0.68,
                       center + RIGHT * 0.6 + DOWN * 0.68, center + LEFT * 1.1 + DOWN * 0.68, center + RIGHT * 1.1 + DOWN * 0.68]:
                vegetation.add(make_tree(pt))
        else:
            for pt in [center + LEFT * 1.2 + UP * 0.68, center + RIGHT * 1.2 + DOWN * 0.68]:
                vegetation.add(make_tree(pt))

        # 6. Objects (benches)
        objects = VGroup()
        if variant == 0:
            objects.add(make_bench(center + LEFT * 0.5 + DOWN * 0.32))
            objects.add(make_bench(center + RIGHT * 0.5 + UP * 0.28))
        elif variant == 1:
            objects.add(make_bench(center + LEFT * 0.4 + UP * 0.28))
            objects.add(make_bench(center + RIGHT * 0.4 + DOWN * 0.28))
            objects.add(make_bench(center + LEFT * 0.4 + DOWN * 0.28))
            objects.add(make_bench(center + RIGHT * 0.4 + UP * 0.28))
        else:
            objects.add(make_bench(center + LEFT * 0.3 + DOWN * 0.3))

        # 7. Cars
        if variant == 0:
            car = vehicle_icon(color=ACCENT_PINK, scale=0.22).move_to(center + RIGHT * 0.6 + DOWN * 0.02)
        elif variant == 1:
            car1 = vehicle_icon(color=ACCENT_PINK, scale=0.22).move_to(center + RIGHT * 0.5 + DOWN * 0.08)
            car2 = vehicle_icon(color=ACCENT_BLUE, scale=0.22).rotate(PI).move_to(center + LEFT * 0.5 + UP * 0.08)
            car = VGroup(car1, car2)
        else:
            car = vehicle_icon(color=ACCENT_PINK, scale=0.22).move_to(center + RIGHT * 0.6 + UP * 0.1)

        # 8. Walkers
        if variant == 0:
            walker = pedestrian_icon(color=ACCENT_AMBER).scale(0.18).move_to(center + LEFT * 0.6 + UP * 0.2)
        elif variant == 1:
            walker1 = pedestrian_icon(color=ACCENT_AMBER).scale(0.18).move_to(center + LEFT * 0.7 + UP * 0.3)
            walker2 = pedestrian_icon(color=ACCENT_AMBER).scale(0.18).move_to(center + RIGHT * 0.7 + DOWN * 0.3)
            walker = VGroup(walker1, walker2)
        else:
            walker = pedestrian_icon(color=ACCENT_AMBER).scale(0.18).move_to(center + LEFT * 0.6 + DOWN * 0.2)

        title = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_MID)
        title.next_to(frame, UP, buff=0.16)
        scene = VGroup(frame, plots, sidewalks, roads, lanes, vegetation, objects, car, walker)
        return VGroup(title, scene)


    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # 1. Create components
        terminal = self.terminal()
        terminal.move_to(LEFT * 4.35 + UP * 0.52)

        engine = self.engine()
        engine.move_to(LEFT * 0.7 + UP * 0.18)

        scene1 = self.scene_tile(0, "")
        scene2 = self.scene_tile(1, "")
        scene3 = self.scene_tile(2, "")
        
        # Position them at the right column zone
        for scene in [scene1, scene2, scene3]:
            scene.move_to(RIGHT * 3.7 + UP * 0.34)

        flow_y = engine[0].get_center()[1]
        
        input_arrow = Arrow(
            np.array([terminal[0].get_right()[0] + 0.12, flow_y, 0]),
            np.array([engine[1].get_left()[0] - 0.08, flow_y, 0]),
            fill_color=ACCENT_TEAL,
            thickness=2.2,
            buff=0,
        )
        output_arrow = Arrow(
            np.array([engine[2].get_right()[0] + 0.1, flow_y, 0]),
            np.array([scene1[1].get_left()[0] - 0.1, flow_y, 0]),
            fill_color=ACCENT_PINK,
            thickness=2.2,
            buff=0,
        )

        # 5 chips
        chips = VGroup()
        for label, color in [
            ("layout", ACCENT_TEAL),
            ("lanes", ACCENT_BLUE),
            ("sidewalks", ACCENT_AMBER),
            ("vegetation", ACCENT_GREEN),
            ("objects", ACCENT_PINK),
        ]:
            chip = RoundedRectangle(
                width=0.75,
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
        chips.arrange(RIGHT, buff=0.1)
        chips.move_to(LEFT * 4.35 + DOWN * 1.65)

        counter = Text("scene 1", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID)
        counter.move_to(RIGHT * 3.7 + DOWN * 1.65)

        punch_left = Text("Diversity", font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH)
        punch_left.set_color(GOLD_RICH)
        punch_mid = Text(">", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_DARK)
        punch_right = Text("Quantity", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_LIGHT)
        punch = VGroup(punch_left, punch_mid, punch_right).arrange(RIGHT, buff=0.18)
        punch.move_to(DOWN * 2.15)

        # --- BEAT 1: Establish Title & Terminal typing (0 to 3.0s) ---
        self.play(
            FadeIn(terminal[0]),
            FadeIn(terminal[1]),
            FadeIn(terminal[3], shift=UP * 0.05),
            FadeIn(terminal[4], shift=DOWN * 0.05),
            run_time=0.45
        )

        cursor = Rectangle(width=0.06, height=0.18, fill_color=ACCENT_GREEN, fill_opacity=0.9, stroke_width=0)
        cursor.move_to(terminal[2][0].get_left(), aligned_edge=LEFT)
        self.add(cursor)

        for i, line in enumerate(terminal[2]):
            self.play(
                Write(line),
                cursor.animate.next_to(line, RIGHT, buff=0.05),
                run_time=min(0.35, len(line.text) * 0.02)
            )
            if i < len(terminal[2]) - 1:
                next_line = terminal[2][i+1]
                self.play(
                    cursor.animate.move_to(next_line.get_left(), aligned_edge=LEFT),
                    run_time=0.08
                )
        self.play(FadeOut(cursor), run_time=0.15)

        # --- BEAT 2: Engine powers on & ingests script (3.0s to 5.0s) ---
        self.play(
            FadeIn(engine),
            ShowCreation(input_arrow),
            LaggedStart(*(FadeIn(chip, shift=UP * 0.05) for chip in chips), lag_ratio=0.06),
            run_time=0.65
        )

        packets = VGroup()
        packet_anims = []
        for i, chip in enumerate(chips):
            color = chip[0].get_stroke_color()
            packet = RoundedRectangle(
                width=0.1,
                height=0.1,
                corner_radius=0.02,
                fill_color=color,
                fill_opacity=1.0,
                stroke_color=INK_DARK,
                stroke_width=0.6,
            )
            offset = (i - 2.0) * 0.1
            start_pt = np.array([terminal[0].get_right()[0] + 0.15, flow_y + offset, 0])
            packet.move_to(start_pt)
            dest_pt = np.array([engine[1].get_left()[0] - 0.05, flow_y + offset, 0])
            path = Line(start_pt, dest_pt)
            packets.add(packet)
            packet_anims.append(MoveAlongPath(packet, path, rate_func=smooth))
        
        self.add(packets)
        self.play(
            Rotate(engine[3], angle=TAU, run_time=1.2, rate_func=linear),
            LaggedStart(*packet_anims, lag_ratio=0.08),
            run_time=1.2
        )
        self.play(
            FadeOut(packets, scale=0.3),
            ShowCreation(output_arrow),
            Rotate(engine[3], angle=PI/2, run_time=0.3, rate_func=linear),
            run_time=0.3
        )

        # --- BEAT 3: Compositional assembly (5.0s to 9.5s) ---
        self.play(
            FadeIn(scene1[0], shift=DOWN * 0.05),
            FadeIn(scene1[1][0]), # frame card
            FadeIn(counter),
            Rotate(engine[3], angle=PI, run_time=0.5, rate_func=linear),
            run_time=0.5
        )

        # 1. Plots and Roads (layout chip)
        self.play(
            Indicate(chips[0], scale_factor=1.1, color=ACCENT_TEAL),
            FadeIn(scene1[1][1], shift=UP * 0.1), # plots
            FadeIn(scene1[1][3]), # roads
            Rotate(engine[3], angle=PI, run_time=0.6, rate_func=linear),
            run_time=0.6
        )

        # 2. Sidewalks (sidewalks chip)
        self.play(
            Indicate(chips[2], scale_factor=1.1, color=ACCENT_AMBER),
            FadeIn(scene1[1][2]), # sidewalks
            Rotate(engine[3], angle=PI, run_time=0.6, rate_func=linear),
            run_time=0.6
        )

        # 3. Lanes (lanes chip)
        self.play(
            Indicate(chips[1], scale_factor=1.1, color=ACCENT_BLUE),
            ShowCreation(scene1[1][4]), # lanes
            Rotate(engine[3], angle=PI, run_time=0.6, rate_func=linear),
            run_time=0.6
        )

        # 4. Vegetation (vegetation chip)
        self.play(
            Indicate(chips[3], scale_factor=1.1, color=ACCENT_GREEN),
            LaggedStart(*(FadeIn(tree, scale=0.5) for tree in scene1[1][5]), lag_ratio=0.15),
            Rotate(engine[3], angle=PI, run_time=0.7, rate_func=linear),
            run_time=0.7
        )

        # 5. Objects & Agents (objects chip)
        self.play(
            Indicate(chips[4], scale_factor=1.1, color=ACCENT_PINK),
            LaggedStart(*(FadeIn(bench, scale=0.5) for bench in scene1[1][6]), lag_ratio=0.15),
            FadeIn(scene1[1][7], shift=RIGHT * 0.1), # car
            FadeIn(scene1[1][8], shift=UP * 0.1), # walker
            Rotate(engine[3], angle=PI, run_time=0.8, rate_func=linear),
            run_time=0.8
        )

        # --- BEAT 4: Vary the distributions (9.5s to 14.5s) ---
        dist_groups = VGroup()
        for i, chip in enumerate(chips):
            center_chip = chip[0].get_center()
            if i % 3 == 0:
                vis = VGroup()
                for h in [0.06, 0.15, 0.22, 0.12, 0.05]:
                    vis.add(Rectangle(width=0.03, height=h, fill_color=INK_DARK, fill_opacity=0.8, stroke_width=0))
                vis.arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
            elif i % 3 == 1:
                line = Line(LEFT * 0.22, RIGHT * 0.22, stroke_color=INK_DARK, stroke_width=1.0)
                dot = Dot(radius=0.035, color=chip[0].get_stroke_color())
                dot.move_to(line.get_center() + RIGHT * 0.08)
                vis = VGroup(line, dot)
            else:
                vis = VMobject(stroke_color=INK_DARK, stroke_width=1.2)
                vis.set_points_smoothly([center_chip + LEFT * 0.25, center_chip + UP * 0.18, center_chip + RIGHT * 0.25])
            
            vis.move_to(center_chip)
            dist_groups.add(vis)

        self.play(
            *(ReplacementTransform(chip[1], dist_groups[i]) for i, chip in enumerate(chips)),
            run_time=0.45
        )

        # Reroll 1
        counter2 = Text("scene 2", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID).move_to(counter)
        self.play(
            Rotate(engine[4], angle=TAU, run_time=0.6),
            dist_groups[1][1].animate.shift(LEFT * 0.16),
            dist_groups[4][1].animate.shift(RIGHT * 0.12),
            Rotate(engine[3], angle=1.5*TAU, run_time=0.6, rate_func=smooth),
            Indicate(engine[0], scale_factor=1.06, color=ACCENT_PINK),
            run_time=0.6
        )
        self.play(
            ReplacementTransform(scene1, scene2),
            ReplacementTransform(counter, counter2),
            run_time=0.65
        )
        counter = counter2

        # Reroll 2
        counter3 = Text("scene 3", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID).move_to(counter)
        self.play(
            Rotate(engine[4], angle=-TAU, run_time=0.5),
            dist_groups[1][1].animate.shift(RIGHT * 0.2),
            dist_groups[4][1].animate.shift(LEFT * 0.22),
            Rotate(engine[3], angle=1.5*TAU, run_time=0.5, rate_func=smooth),
            Indicate(engine[0], scale_factor=1.06, color=ACCENT_PINK),
            run_time=0.5
        )
        self.play(
            ReplacementTransform(scene2, scene3),
            ReplacementTransform(counter, counter3),
            run_time=0.65
        )
        counter = counter3

        # --- BEAT 5: Effectively infinite variety (14.5s to 18.0s) ---
        counter_cascade = Text("scene 4  \u2192  5  \u2192  6  \u2192  ...", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID).move_to(counter)
        self.play(
            ReplacementTransform(counter, counter_cascade),
            run_time=0.4
        )
        counter = counter_cascade

        # Shrink scene3 to top-left position of grid (r=0, c=0)
        g_pos_00 = RIGHT * 3.7 + UP * 0.3 + RIGHT * (-1) * 0.95 + UP * (1) * 0.62
        self.play(
            scene3.animate.scale(0.3).move_to(g_pos_00),
            Rotate(engine[3], angle=PI, run_time=0.5),
            run_time=0.5
        )

        grid_tiles = VGroup()
        grid_anims = []
        for r in range(3):
            for c in range(3):
                if r == 0 and c == 0:
                    continue
                tile = self.scene_tile((r * 3 + c) % 3, "").scale(0.3)
                tile.move_to(engine[2].get_center())
                target_pos = RIGHT * 3.7 + UP * 0.3 + RIGHT * (c - 1) * 0.95 + UP * (1 - r) * 0.62
                grid_tiles.add(tile)
                grid_anims.append((tile, target_pos))

        self.add(grid_tiles)
        
        fly_anims = []
        for idx, (tile, target_pos) in enumerate(grid_anims):
            rt = max(0.18, 0.45 - idx * 0.03)
            fly = tile.animate(run_time=rt, rate_func=smooth).move_to(target_pos)
            fly_anims.append(fly)
            
        self.play(
            LaggedStart(*fly_anims, lag_ratio=0.12),
            Rotate(engine[3], angle=4*TAU, run_time=2.2, rate_func=linear),
            run_time=2.2
        )

        counter_inf = Text("infinite environments  \u221e", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH).move_to(counter)
        self.play(
            ReplacementTransform(counter, counter_inf),
            run_time=0.5
        )
        counter = counter_inf

        # --- BEAT 6: Payoff & Settle (18.0s to 20.0s) ---
        self.play(
            FadeIn(punch, shift=UP * 0.1),
            run_time=0.6
        )
        self.wait(2.2)
        self._close()
