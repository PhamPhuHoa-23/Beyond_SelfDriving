"""P05-S06b PedGen: scene-aware pedestrian diffusion."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene,
    BG_PAPER,
    BG_CARD,
    BG_SECTION,
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
    PURPLE_MODEL,
    RED_ERROR,
    GREEN_FIX,
    CYAN_RADAR,
    GOLD_KEY,
    INK_DARK,
    INK_MID,
    INK_LIGHT,
    LINE_GRID,
    LINE_ARROW,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    pedestrian_icon,
    vehicle_icon,
)

SCRIPT = """PedGen conditions diffusion on scene geometry, body shape, and destination so generated pedestrians move around obstacles instead of through them."""


class P05S06BPedGen(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "PedGen: Scene-Aware Motion"
    RNG_SEED = 17

    def rounded_token(
        self,
        label,
        *,
        width,
        height,
        fill,
        stroke,
        font_size=SIZE_CAPS,
    ):
        shell = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            fill_color=fill,
            fill_opacity=0.96,
            stroke_color=stroke,
            stroke_width=1.7,
        )
        text = Text(
            label,
            font=FONT_PRIMARY,
            font_size=font_size,
            color=INK_DARK,
            weight=BOLD,
        )
        text.move_to(shell)
        return VGroup(shell, text)

    def noise_dots(self, center, *, count=28, radius=0.04, spread_x=0.82, spread_y=0.32):
        rng = np.random.RandomState(self.RNG_SEED)
        dots = VGroup()
        colors = [ACCENT_PINK, PURPLE_MODEL, ACCENT_BLUE, ACCENT_GREEN]
        for i in range(count):
            dot = Dot(
                radius=radius * rng.uniform(0.65, 1.2),
                color=colors[i % len(colors)],
            )
            dot.set_opacity(rng.uniform(0.35, 0.92))
            dot.move_to(
                center
                + RIGHT * rng.uniform(-spread_x, spread_x)
                + UP * rng.uniform(-spread_y, spread_y)
            )
            dots.add(dot)
        return dots

    def small_model(self):
        shell = RoundedRectangle(
            width=3.55,
            height=1.5,
            corner_radius=0.16,
            fill_color=PASTEL_PINK,
            fill_opacity=0.72,
            stroke_color=ACCENT_PINK,
            stroke_width=2.2,
        )
        title = Text(
            "PedGen",
            font=FONT_PRIMARY,
            font_size=24,
            color=ACCENT_PINK,
            weight=BOLD,
        )
        subtitle = Text(
            "conditioned diffusion",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=INK_LIGHT,
            weight=BOLD,
        )
        labels = VGroup(title, subtitle).arrange(DOWN, buff=0.01)
        labels.move_to(shell.get_top() + DOWN * 0.32)
        return VGroup(shell, labels)

    def condition_shell(self, title, color):
        shell = RoundedRectangle(
            width=2.82,
            height=1.32,
            corner_radius=0.13,
            fill_color=interpolate_color(color, WHITE, 0.86),
            fill_opacity=0.98,
            stroke_color=color,
            stroke_width=1.8,
        )
        label = Text(
            title,
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=color,
            weight=BOLD,
        )
        label.move_to(shell.get_top() + DOWN * 0.2)
        return shell, label

    def scene_condition(self):
        shell, label = self.condition_shell("SCENE CONTEXT", ACCENT_BLUE)
        cells = VGroup()
        active = VGroup()
        occupied = {(0, 1), (0, 4), (1, 3), (2, 0), (2, 3)}
        for row in range(3):
            for col in range(6):
                cell = Square(
                    side_length=0.18,
                    fill_color=PASTEL_BLUE,
                    fill_opacity=0.34,
                    stroke_color=ACCENT_BLUE,
                    stroke_width=0.65,
                )
                cell.move_to(
                    shell.get_center()
                    + RIGHT * (col - 2.5) * 0.21
                    + DOWN * (row - 1) * 0.21
                    + DOWN * 0.09
                )
                cells.add(cell)
                if (row, col) in occupied:
                    hot = cell.copy()
                    hot.set_fill(ACCENT_BLUE, opacity=0.94)
                    active.add(hot)
        scan = Line(
            shell.get_left() + RIGHT * 0.54 + UP * 0.25,
            shell.get_left() + RIGHT * 0.54 + DOWN * 0.45,
            stroke_color=CYAN_RADAR,
            stroke_width=3.0,
            stroke_opacity=0.9,
        )
        return {
            "base": VGroup(shell, label, cells),
            "active": active,
            "scan": scan,
            "full": VGroup(shell, label, cells, active),
            "shell": shell,
        }

    def body_condition(self):
        shell, label = self.condition_shell("BODY CONTEXT", PURPLE_MODEL)
        child = pedestrian_icon(color=PURPLE_MODEL).scale(0.38)
        adult = pedestrian_icon(color=ACCENT_PINK).scale(0.57)
        silhouettes = VGroup(child, adult).arrange(RIGHT, buff=0.42, aligned_edge=DOWN)
        silhouettes.move_to(shell.get_center() + DOWN * 0.12)

        selected = pedestrian_icon(color=PURPLE_MODEL).scale(0.52)
        selected.move_to(shell.get_center() + DOWN * 0.1)
        stride = VGroup(
            Line(LEFT * 0.42, RIGHT * 0.42, stroke_color=PURPLE_MODEL, stroke_width=1.0),
            *(
                Line(
                    ORIGIN + UP * 0.05,
                    ORIGIN + DOWN * 0.05,
                    stroke_color=PURPLE_MODEL,
                    stroke_width=1.0,
                ).shift(RIGHT * x)
                for x in np.linspace(-0.38, 0.38, 5)
            ),
        )
        stride.move_to(shell.get_center() + DOWN * 0.43)
        return {
            "base": VGroup(shell, label, silhouettes),
            "silhouettes": silhouettes,
            "selected": selected,
            "stride": stride,
            "full": VGroup(shell, label, selected, stride),
            "shell": shell,
        }

    def goal_condition(self):
        shell, label = self.condition_shell("GOAL", ACCENT_GREEN)
        start = shell.get_center() + LEFT * 0.72 + DOWN * 0.1
        final = shell.get_center() + RIGHT * 0.7 + UP * 0.02
        pin = VGroup(
            Circle(
                radius=0.16,
                fill_color=PASTEL_GREEN,
                fill_opacity=0.65,
                stroke_color=ACCENT_GREEN,
                stroke_width=1.6,
            ),
            Dot(radius=0.055, color=ACCENT_GREEN),
        )
        pin.move_to(start)
        vector = Arrow(
            start + LEFT * 0.1,
            final + LEFT * 0.18,
            fill_color=ACCENT_GREEN,
            thickness=1.8,
            buff=0,
        )
        return {
            "base": VGroup(shell, label, pin),
            "pin": pin,
            "pin_final": final,
            "vector": vector,
            "full": VGroup(shell, label, pin, vector),
            "shell": shell,
        }

    def condition_packet(self, card_shell, model_shell, color, *, port_x):
        start = card_shell.get_bottom() + DOWN * 0.03
        end = model_shell.get_top() + RIGHT * port_x + UP * 0.03
        path = Arrow(
            start,
            end,
            fill_color=color,
            thickness=2.1,
            max_tip_length_to_length_ratio=0.13,
            buff=0,
        )
        path.set_stroke(color, width=2.1, opacity=0.72)
        path.set_fill(color, opacity=0.72)
        packet = Dot(radius=0.075, color=color)
        packet.move_to(start)
        return path, packet

    def hero_environment(self):
        shell = RoundedRectangle(
            width=8.25,
            height=4.0,
            corner_radius=0.17,
            fill_color=interpolate_color(PASTEL_PINK, WHITE, 0.72),
            fill_opacity=0.98,
            stroke_color=ACCENT_PINK,
            stroke_width=2.0,
        )
        shell.move_to(DOWN * 0.42)
        grid = VGroup()
        for x in np.linspace(-3.6, 3.6, 13):
            grid.add(
                Line(
                    shell.get_center() + RIGHT * x + DOWN * 1.6,
                    shell.get_center() + RIGHT * x + UP * 1.35,
                    stroke_color=LINE_GRID,
                    stroke_width=0.65,
                    stroke_opacity=0.75,
                )
            )
        for y in np.linspace(-1.6, 1.35, 7):
            grid.add(
                Line(
                    shell.get_center() + LEFT * 3.65 + UP * y,
                    shell.get_center() + RIGHT * 3.65 + UP * y,
                    stroke_color=LINE_GRID,
                    stroke_width=0.65,
                    stroke_opacity=0.75,
                )
            )
        obstacle = RoundedRectangle(
            width=1.0,
            height=0.82,
            corner_radius=0.1,
            fill_color=PASTEL_AMBER,
            fill_opacity=0.95,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.7,
        )
        obstacle.move_to(shell.get_center() + DOWN * 0.02)
        occupied = Text(
            "occupied",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=ACCENT_AMBER,
            weight=BOLD,
        )
        occupied.move_to(obstacle)
        start = shell.get_center() + LEFT * 3.45 + DOWN * 1.2
        start_dot = Dot(radius=0.07, color=INK_MID)
        start_dot.move_to(start)
        goal = shell.get_center() + RIGHT * 3.38 + UP * 1.05
        goal_pin = VGroup(
            Circle(radius=0.16, stroke_color=ACCENT_GREEN, stroke_width=2.0),
            Dot(radius=0.055, color=ACCENT_GREEN),
        )
        goal_pin.move_to(goal)
        title = Text(
            "denoise a distribution of possible motion",
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=INK_DARK,
            weight=BOLD,
        )
        title.move_to(shell.get_top() + DOWN * 0.24)
        return {
            "shell": shell,
            "grid": grid,
            "obstacle": obstacle,
            "occupied": occupied,
            "start": start,
            "start_dot": start_dot,
            "goal": goal,
            "goal_pin": goal_pin,
            "title": title,
            "base": VGroup(shell, grid, obstacle, occupied, start_dot, goal_pin, title),
        }

    def target_modes(self, start, goal):
        xs = np.linspace(start[0], goal[0], 9)
        u = np.linspace(0, 1, 9)
        linear_y = start[1] + (goal[1] - start[1]) * u
        upper = linear_y + 1.05 * np.sin(PI * u)
        lower = linear_y - 0.62 * np.sin(PI * u)
        wide_upper = linear_y + 1.42 * np.sin(PI * u)
        return [
            np.column_stack([xs, upper, np.zeros_like(xs)]),
            np.column_stack([xs, lower, np.zeros_like(xs)]),
            np.column_stack([xs, wide_upper, np.zeros_like(xs)]),
        ]

    def trajectory_state(self, step, start, goal):
        blend = {4: 0.0, 3: 0.3, 2: 0.58, 1: 0.84, 0: 1.0}[step]
        modes = self.target_modes(start, goal)
        paths = VGroup()
        endpoints = VGroup()
        poses = VGroup()
        for index in range(7):
            rng = np.random.RandomState(self.RNG_SEED + index * 31)
            target = modes[index % len(modes)].copy()
            noisy = target.copy()
            noisy[:, 0] += rng.normal(0, 0.26, len(noisy))
            noisy[:, 1] = (
                start[1]
                + rng.normal(0, 1.0, len(noisy))
                + np.linspace(-0.2, 0.35, len(noisy))
            )
            noisy[0] = start
            noisy[-1] = goal + np.array(
                [rng.uniform(-0.2, 0.2), rng.uniform(-1.0, 1.0), 0]
            )
            points = (1 - blend) * noisy + blend * target
            points[0] = start
            if step == 0:
                points[-1] = goal

            path = VMobject()
            path.set_points_smoothly(points)
            if step == 0 and index == 0:
                path.set_stroke(ACCENT_PINK, width=4.2, opacity=1.0)
            else:
                opacity = 0.68 - 0.08 * index
                if step == 0:
                    opacity = 0.2 if index < 3 else 0.09
                path.set_stroke(
                    PURPLE_MODEL,
                    width=2.4 if step > 1 else 2.0,
                    opacity=max(opacity, 0.08),
                )
            paths.add(path)

            end_dot = Dot(
                radius=0.045 if step > 0 else 0.035,
                color=PURPLE_MODEL if index else ACCENT_PINK,
            )
            end_dot.set_opacity(0.62 if step > 0 else (1.0 if index == 0 else 0.18))
            end_dot.move_to(points[-1])
            endpoints.add(end_dot)

        selected = paths[0]
        for index, alpha in enumerate(np.linspace(0.12, 0.88, 5)):
            rng = np.random.RandomState(self.RNG_SEED + 300 + index)
            pose = pedestrian_icon(color=PURPLE_MODEL).scale(0.34)
            if step >= 3:
                pose.rotate(rng.uniform(-0.7, 0.7))
                pose.stretch(rng.uniform(0.65, 1.35), 0)
                pose.move_to(
                    selected.point_from_proportion(alpha)
                    + RIGHT * rng.uniform(-0.55, 0.55)
                    + UP * rng.uniform(-0.48, 0.48)
                )
                pose.set_opacity(0.2)
            else:
                pose.move_to(selected.point_from_proportion(alpha))
                pose.set_opacity(0.28 if step else 0.18 + 0.1 * index)
            poses.add(pose)
        return VGroup(paths, endpoints, poses)

    def timestep_label(self, step, panel):
        suffix = {
            4: "noise",
            3: "scene constraints",
            2: "body-consistent",
            1: "goal-directed",
            0: "trajectory",
        }[step]
        label = self.rounded_token(
            f"t = {step}  {suffix}",
            width=1.75,
            height=0.42,
            fill=BG_CARD,
            stroke=ACCENT_PINK,
            font_size=SIZE_MICRO,
        )
        label.move_to(panel.get_corner(UR) + LEFT * 1.15 + DOWN * 0.55)
        return label

    def loss_rail(self):
        label = Text(
            "training constraints",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=INK_LIGHT,
            weight=BOLD,
        )
        chips = VGroup()
        specs = [
            (r"L_{\mathrm{rec}}", "pose", PURPLE_MODEL),
            (r"L_{\mathrm{traj}}", "goal", ACCENT_GREEN),
            (r"L_{\mathrm{geo}}", "joints", ACCENT_BLUE),
        ]
        for formula, note, color in specs:
            shell = RoundedRectangle(
                width=1.28,
                height=0.48,
                corner_radius=0.09,
                fill_color=interpolate_color(color, WHITE, 0.87),
                fill_opacity=0.98,
                stroke_color=color,
                stroke_width=1.3,
            )
            tex = Tex(formula, font_size=22)
            tex.set_color(color)
            note_mob = Text(
                note,
                font=FONT_PRIMARY,
                font_size=11,
                color=INK_LIGHT,
            )
            VGroup(tex, note_mob).arrange(RIGHT, buff=0.1).move_to(shell)
            chips.add(VGroup(shell, tex, note_mob))
        chips.arrange(RIGHT, buff=0.13)
        row = VGroup(label, chips).arrange(RIGHT, buff=0.25)
        row.move_to(DOWN * 2.83)
        return VGroup(label, chips)

    def comparison_panel(self, *, context_on):
        color = GREEN_FIX if context_on else RED_ERROR
        fill = PASTEL_GREEN if context_on else PASTEL_PINK
        title = "SCENE CONTEXT ON" if context_on else "SCENE CONTEXT OFF"
        shell = RoundedRectangle(
            width=5.65,
            height=3.55,
            corner_radius=0.15,
            fill_color=interpolate_color(fill, WHITE, 0.78),
            fill_opacity=0.98,
            stroke_color=color,
            stroke_width=1.8,
        )
        heading = Text(
            title,
            font=FONT_PRIMARY,
            font_size=SIZE_CAPS,
            color=color,
            weight=BOLD,
        )
        heading.move_to(shell.get_top() + DOWN * 0.24)
        grid = VGroup()
        for x in np.linspace(-2.35, 2.35, 10):
            grid.add(
                Line(
                    shell.get_center() + RIGHT * x + DOWN * 1.35,
                    shell.get_center() + RIGHT * x + UP * 1.02,
                    stroke_color=LINE_GRID,
                    stroke_width=0.55,
                )
            )
        for y in np.linspace(-1.35, 1.02, 6):
            grid.add(
                Line(
                    shell.get_center() + LEFT * 2.35 + UP * y,
                    shell.get_center() + RIGHT * 2.35 + UP * y,
                    stroke_color=LINE_GRID,
                    stroke_width=0.55,
                )
            )
        obstacle = RoundedRectangle(
            width=0.92,
            height=0.86,
            corner_radius=0.09,
            fill_color=PASTEL_AMBER,
            fill_opacity=0.96,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.5,
        )
        obstacle.move_to(shell.get_center() + DOWN * 0.05)
        start = shell.get_center() + LEFT * 2.35 + DOWN * 1.08
        goal = shell.get_center() + RIGHT * 2.28 + UP * 0.83
        start_dot = Dot(radius=0.06, color=INK_MID).move_to(start)
        goal_pin = VGroup(
            Circle(radius=0.14, stroke_color=ACCENT_GREEN, stroke_width=1.8),
            Dot(radius=0.05, color=ACCENT_GREEN),
        ).move_to(goal)

        candidates = VGroup()
        modes = self.target_modes(start, goal)
        for index, points in enumerate(modes):
            path = VMobject()
            path.set_points_smoothly(points)
            path.set_stroke(
                PURPLE_MODEL if context_on else RED_ERROR,
                width=1.8,
                opacity=0.18 if context_on else 0.13,
            )
            candidates.add(path)

        if context_on:
            selected = VMobject()
            selected.set_points_smoothly(modes[0])
            selected.set_stroke(GREEN_FIX, width=3.8, opacity=1.0)
        else:
            missed_goal = goal + DOWN * 0.42
            selected = Line(
                start,
                missed_goal,
                stroke_color=RED_ERROR,
                stroke_width=3.2,
                stroke_opacity=0.9,
            )

        ped = pedestrian_icon(color=ACCENT_PINK).scale(0.48)
        ped.move_to(start)
        status = Text(
            "coherent" if context_on else "collision",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=color,
            weight=BOLD,
        )
        status.move_to(shell.get_bottom() + UP * 0.2 + RIGHT * 1.8)
        return {
            "shell": shell,
            "heading": heading,
            "grid": grid,
            "obstacle": obstacle,
            "start": start,
            "goal": goal,
            "start_dot": start_dot,
            "goal_pin": goal_pin,
            "candidates": candidates,
            "selected": selected,
            "ped": ped,
            "status": status,
            "base": VGroup(shell, grid, obstacle, start_dot, goal_pin, heading),
        }

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # Beat 1 (1.0-2.4): CityWalker becomes the noisy training signal.
        citywalker = self.rounded_token(
            "CityWalker data",
            width=2.45,
            height=0.72,
            fill=PASTEL_TEAL,
            stroke=ACCENT_TEAL,
            font_size=SIZE_LABEL,
        )
        citywalker.move_to(LEFT * 3.55 + DOWN * 0.45)
        model = self.small_model()
        model.move_to(DOWN * 1.12)
        seed = self.noise_dots(
            model[0].get_center() + DOWN * 0.18,
            count=32,
            spread_x=1.1,
            spread_y=0.28,
        )
        self.play(FadeIn(citywalker, shift=RIGHT * 0.12), FadeIn(model), run_time=0.4)
        self.play(
            citywalker.animate.scale(0.45).move_to(
                model[0].get_center() + DOWN * 0.12
            ),
            Indicate(model[0], color=ACCENT_PINK, scale_factor=1.05),
            run_time=0.5,
            rate_func=smooth,
        )
        self.play(ReplacementTransform(citywalker, seed), run_time=0.5)

        # Beat 2 (2.4-6.6): Three conditions enter the same diffusion model.
        scene_card = self.scene_condition()
        body_card = self.body_condition()
        goal_card = self.goal_condition()
        for card, x in zip(
            [scene_card, body_card, goal_card],
            [-3.65, 0.0, 3.65],
        ):
            card["base"].move_to(RIGHT * x + UP * 1.25)
            if "active" in card:
                card["active"].move_to(card["base"][2])
                card["scan"].move_to(
                    card["shell"].get_left() + RIGHT * 0.54 + DOWN * 0.1
                )
            if "selected" in card:
                card["selected"].move_to(card["shell"].get_center() + DOWN * 0.1)
                card["stride"].move_to(card["shell"].get_center() + DOWN * 0.43)
            if "vector" in card:
                delta = card["shell"].get_center() - ORIGIN
                card["vector"].shift(delta)
                card["pin_final"] = card["pin_final"] + delta

        scene_link, scene_packet = self.condition_packet(
            scene_card["shell"], model[0], ACCENT_BLUE, port_x=-0.9
        )
        body_link, body_packet = self.condition_packet(
            body_card["shell"], model[0], PURPLE_MODEL, port_x=0.0
        )
        goal_link, goal_packet = self.condition_packet(
            goal_card["shell"], model[0], ACCENT_GREEN, port_x=0.9
        )

        self.play(FadeIn(scene_card["base"], shift=DOWN * 0.08), run_time=0.35)
        scan_target = scene_card["scan"].copy().shift(RIGHT * 2.05)
        self.add(scene_card["scan"])
        self.play(
            Transform(scene_card["scan"], scan_target),
            LaggedStart(
                *(FadeIn(cell, scale=0.7) for cell in scene_card["active"]),
                lag_ratio=0.08,
            ),
            run_time=0.45,
            rate_func=linear,
        )
        self.remove(scene_card["scan"])
        self.play(
            ShowCreation(scene_link),
            MoveAlongPath(scene_packet, scene_link),
            Flash(model[0], color=ACCENT_BLUE, line_length=0.1, num_lines=6),
            run_time=0.4,
        )
        self.remove(scene_packet)

        self.play(FadeIn(body_card["base"], shift=DOWN * 0.08), run_time=0.35)
        self.play(
            ReplacementTransform(body_card["silhouettes"], body_card["selected"]),
            FadeIn(body_card["stride"]),
            run_time=0.45,
        )
        self.play(
            ShowCreation(body_link),
            MoveAlongPath(body_packet, body_link),
            Flash(model[0], color=PURPLE_MODEL, line_length=0.1, num_lines=6),
            run_time=0.4,
        )
        self.remove(body_packet)

        self.play(FadeIn(goal_card["base"], shift=DOWN * 0.08), run_time=0.3)
        self.play(
            goal_card["pin"].animate.move_to(goal_card["pin_final"]),
            run_time=0.4,
            rate_func=smooth,
        )
        self.play(ShowCreation(goal_card["vector"]), run_time=0.2)
        self.play(
            ShowCreation(goal_link),
            MoveAlongPath(goal_packet, goal_link),
            Flash(model[0], color=ACCENT_GREEN, line_length=0.1, num_lines=6),
            run_time=0.3,
        )
        self.remove(goal_packet)
        self.play(
            Flash(scene_card["shell"], color=ACCENT_BLUE, line_length=0.09, num_lines=6),
            Flash(body_card["shell"], color=PURPLE_MODEL, line_length=0.09, num_lines=6),
            Flash(goal_card["shell"], color=ACCENT_GREEN, line_length=0.09, num_lines=6),
            Flash(model[0], color=ACCENT_PINK, line_length=0.12, num_lines=8),
            seed.animate.set_opacity(0.95),
            run_time=0.6,
        )

        # Beat 3 (6.6-14.2): The distribution resolves from noise to motion.
        hero = self.hero_environment()
        self.remove(model)
        self.add(model[0], model[1])
        self.remove(
            scene_card["base"],
            scene_card["active"],
            body_card["base"],
            body_card["selected"],
            body_card["stride"],
            goal_card["base"],
            goal_card["vector"],
        )
        hero_cards = VGroup(
            scene_card["full"],
            body_card["full"],
            goal_card["full"],
        )
        self.add(hero_cards)
        hero_cards_target = hero_cards.copy()
        hero_cards_target.arrange(RIGHT, buff=0.68)
        hero_cards_target.scale(0.7)
        hero_cards_target.move_to(UP * 2.22)
        model_target = hero["shell"].copy()
        hero_contents = VGroup(
            hero["grid"],
            hero["obstacle"],
            hero["occupied"],
            hero["start_dot"],
            hero["goal_pin"],
            hero["title"],
        )
        self.play(
            ReplacementTransform(model[0], model_target),
            FadeOut(model[1]),
            FadeOut(seed),
            FadeOut(VGroup(scene_link, body_link, goal_link)),
            Transform(hero_cards, hero_cards_target),
            FadeIn(hero_contents),
            run_time=0.8,
            rate_func=smooth,
        )
        self.remove(model_target, hero_contents, hero_cards)
        self.add(
            model_target,
            hero["grid"],
            hero["obstacle"],
            hero["occupied"],
            hero["start_dot"],
            hero["goal_pin"],
            hero["title"],
            hero_cards,
        )
        hero["shell"] = model_target

        loss_rail = self.loss_rail()
        state = self.trajectory_state(4, hero["start"], hero["goal"])
        step_label = self.timestep_label(4, hero["shell"])
        self.play(
            FadeIn(state),
            FadeIn(step_label, shift=LEFT * 0.08),
            FadeIn(loss_rail, shift=UP * 0.06),
            run_time=0.6,
        )

        next_state = self.trajectory_state(3, hero["start"], hero["goal"])
        next_label = self.timestep_label(3, hero["shell"])
        collision_flash = Line(
            hero["obstacle"].get_left() + LEFT * 0.45 + DOWN * 0.2,
            hero["obstacle"].get_right() + RIGHT * 0.45 + UP * 0.25,
            stroke_color=RED_ERROR,
            stroke_width=5.0,
        )
        self.play(
            ReplacementTransform(state, next_state),
            ReplacementTransform(step_label, next_label),
            Indicate(hero_cards[0][0], color=ACCENT_BLUE, scale_factor=1.06),
            Indicate(loss_rail[1][2], color=ACCENT_BLUE, scale_factor=1.08),
            ShowPassingFlash(collision_flash, time_width=0.35),
            Flash(hero["obstacle"], color=RED_ERROR, line_length=0.1, num_lines=7),
            run_time=1.0,
        )
        state, step_label = next_state, next_label

        next_state = self.trajectory_state(2, hero["start"], hero["goal"])
        next_label = self.timestep_label(2, hero["shell"])
        self.play(
            ReplacementTransform(state, next_state),
            ReplacementTransform(step_label, next_label),
            Indicate(hero_cards[1][0], color=PURPLE_MODEL, scale_factor=1.06),
            Indicate(loss_rail[1][0], color=PURPLE_MODEL, scale_factor=1.08),
            run_time=1.0,
        )
        state, step_label = next_state, next_label

        next_state = self.trajectory_state(1, hero["start"], hero["goal"])
        next_label = self.timestep_label(1, hero["shell"])
        self.play(
            ReplacementTransform(state, next_state),
            ReplacementTransform(step_label, next_label),
            Indicate(hero_cards[2][0], color=ACCENT_GREEN, scale_factor=1.06),
            Indicate(loss_rail[1][1], color=ACCENT_GREEN, scale_factor=1.08),
            Flash(hero["goal_pin"], color=ACCENT_GREEN, line_length=0.1, num_lines=7),
            run_time=1.0,
        )
        state, step_label = next_state, next_label

        next_state = self.trajectory_state(0, hero["start"], hero["goal"])
        next_label = self.timestep_label(0, hero["shell"])
        self.play(
            ReplacementTransform(state, next_state),
            ReplacementTransform(step_label, next_label),
            Indicate(hero_cards[0][0], color=ACCENT_BLUE, scale_factor=1.04),
            Indicate(hero_cards[1][0], color=PURPLE_MODEL, scale_factor=1.04),
            Indicate(hero_cards[2][0], color=ACCENT_GREEN, scale_factor=1.04),
            run_time=1.0,
        )
        state, step_label = next_state, next_label

        selected_path = state[0][0]
        generated_ped = pedestrian_icon(color=ACCENT_PINK).scale(0.5)
        generated_ped.move_to(selected_path.get_start())
        self.play(
            ShowPassingFlash(
                selected_path.copy().set_stroke(
                    ACCENT_PINK, width=7.0, opacity=0.65
                ),
                time_width=0.35,
            ),
            FadeIn(generated_ped, scale=0.85),
            FadeOut(loss_rail),
            run_time=0.6,
        )
        self.play(
            MoveAlongPath(generated_ped, selected_path),
            run_time=1.6,
            rate_func=smooth,
        )

        # Beat 4 (14.2-21.4): Same seed, context off versus context on.
        shared_seed = self.rounded_token(
            "same seed  |  same body  |  same goal",
            width=4.1,
            height=0.58,
            fill=BG_CARD,
            stroke=PURPLE_MODEL,
            font_size=15,
        )
        shared_seed.move_to(UP * 2.25)
        hero_group = VGroup(
            hero["shell"],
            hero["grid"],
            hero["obstacle"],
            hero["occupied"],
            hero["start_dot"],
            hero["goal_pin"],
            hero["title"],
            state,
            step_label,
            generated_ped,
            hero_cards,
        )
        self.play(
            hero_group.animate.scale(0.04).move_to(shared_seed).set_opacity(0),
            FadeIn(shared_seed, scale=0.75),
            run_time=0.8,
            rate_func=smooth,
        )

        left = self.comparison_panel(context_on=False)
        right = self.comparison_panel(context_on=True)
        left["base"].move_to(LEFT * 3.18 + DOWN * 0.42)
        right["base"].move_to(RIGHT * 3.18 + DOWN * 0.42)
        for panel in [left, right]:
            delta = panel["shell"].get_center() - ORIGIN
            panel["candidates"].shift(delta)
            panel["selected"].shift(delta)
            panel["ped"].shift(delta)
            panel["status"].shift(delta)
            panel["start"] = panel["start"] + delta
            panel["goal"] = panel["goal"] + delta
        self.play(FadeIn(left["base"]), FadeIn(right["base"]), run_time=0.8)

        split_left = Arrow(
            shared_seed.get_bottom() + LEFT * 0.65,
            left["shell"].get_top() + UP * 0.05,
            fill_color=RED_ERROR,
            thickness=1.5,
            buff=0,
        )
        split_right = Arrow(
            shared_seed.get_bottom() + RIGHT * 0.65,
            right["shell"].get_top() + UP * 0.05,
            fill_color=GREEN_FIX,
            thickness=1.5,
            buff=0,
        )
        self.play(
            ShowCreation(split_left),
            ShowCreation(split_right),
            Flash(shared_seed, color=PURPLE_MODEL, line_length=0.09, num_lines=6),
            run_time=0.6,
        )

        self.play(
            FadeIn(left["candidates"]),
            FadeIn(right["candidates"]),
            ShowCreation(left["selected"]),
            FadeIn(left["ped"]),
            run_time=0.4,
        )
        left_first = left["selected"].copy()
        left_second = left["selected"].copy()
        left_first.pointwise_become_partial(left["selected"], 0, 0.52)
        left_second.pointwise_become_partial(left["selected"], 0.52, 1)
        self.play(
            MoveAlongPath(left["ped"], left_first),
            run_time=0.6,
            rate_func=linear,
        )
        crash = VGroup(
            Line(LEFT * 0.15, RIGHT * 0.15, stroke_color=RED_ERROR, stroke_width=4.0).rotate(PI / 4),
            Line(LEFT * 0.15, RIGHT * 0.15, stroke_color=RED_ERROR, stroke_width=4.0).rotate(-PI / 4),
        )
        crash.move_to(left["ped"])
        self.play(
            FadeIn(crash, scale=1.3),
            FadeIn(left["status"]),
            Flash(left["ped"], color=RED_ERROR, line_length=0.14, num_lines=8),
            run_time=0.3,
        )
        self.play(
            MoveAlongPath(left["ped"], left_second),
            crash.animate.set_opacity(0.35),
            run_time=0.5,
            rate_func=linear,
        )

        self.play(
            ShowCreation(right["selected"]),
            FadeIn(right["ped"]),
            ShowPassingFlash(
                right["selected"].copy().set_stroke(
                    GREEN_FIX, width=6.0, opacity=0.55
                ),
                time_width=0.35,
            ),
            run_time=0.4,
        )
        right_first = right["selected"].copy()
        right_second = right["selected"].copy()
        right_first.pointwise_become_partial(right["selected"], 0, 0.48)
        right_second.pointwise_become_partial(right["selected"], 0.48, 1)
        self.play(
            MoveAlongPath(right["ped"], right_first),
            run_time=0.8,
            rate_func=smooth,
        )
        self.play(
            Indicate(right["ped"], color=ACCENT_PINK, scale_factor=1.08),
            Indicate(right["obstacle"], color=ACCENT_AMBER, scale_factor=1.05),
            run_time=0.3,
        )
        self.play(
            MoveAlongPath(right["ped"], right_second),
            FadeIn(right["status"]),
            run_time=1.1,
            rate_func=smooth,
        )
        self.wait(0.2)

        # Beat 5 (21.4-24.2): The generated human motion becomes predictable.
        left_all = VGroup(
            left["base"],
            left["candidates"],
            left["selected"],
            left["ped"],
            left["status"],
            crash,
        )
        right_all = VGroup(
            right["base"],
            right["candidates"],
            right["selected"],
            right["ped"],
            right["status"],
        )
        right_target = right_all.copy()
        right_target.scale(1.32)
        right_target.move_to(DOWN * 0.18)
        self.play(
            FadeOut(left_all, shift=LEFT * 0.3),
            FadeOut(VGroup(shared_seed, split_left, split_right)),
            Transform(right_all, right_target),
            run_time=0.5,
            rate_func=smooth,
        )

        predicted = DashedVMobject(
            right["selected"].copy(),
            num_dashes=24,
        )
        predicted.set_stroke(ACCENT_BLUE, width=4.5, opacity=0.95)
        predicted.shift(DOWN * 0.055)
        robot = vehicle_icon(color=ACCENT_BLUE, scale=0.34)
        robot.move_to(right["shell"].get_corner(DL) + RIGHT * 0.72 + UP * 0.58)
        prediction_label = Text(
            "robot prediction",
            font=FONT_PRIMARY,
            font_size=SIZE_MICRO,
            color=ACCENT_BLUE,
            weight=BOLD,
        )
        prediction_label.set_color(ACCENT_BLUE)
        prediction_label.set_fill(ACCENT_BLUE, opacity=1.0)
        prediction_label.set_stroke(width=0)
        prediction_label.next_to(robot, RIGHT, buff=0.1)
        self.play(
            FadeIn(robot, scale=0.85),
            FadeIn(prediction_label, shift=UP * 0.05),
            run_time=0.4,
        )
        self.play(
            ShowCreation(predicted),
            right["selected"].animate.set_stroke(opacity=0.48),
            Flash(right["goal_pin"], color=CYAN_RADAR, line_length=0.12, num_lines=7),
            run_time=0.6,
        )
        check = Text(
            "✓",
            font=FONT_PRIMARY,
            font_size=32,
            color=GREEN_FIX,
            weight=BOLD,
        )
        check.set_color(GREEN_FIX)
        check.set_fill(GREEN_FIX, opacity=1.0)
        check.set_stroke(width=0)
        payoff = Text(
            "predictable motion",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=GREEN_FIX,
            weight=BOLD,
        )
        payoff.set_color(GREEN_FIX)
        payoff.set_fill(GREEN_FIX, opacity=1.0)
        payoff.set_stroke(width=0)
        VGroup(check, payoff).arrange(RIGHT, buff=0.12)
        VGroup(check, payoff).move_to(DOWN * 2.75)
        self.play(
            FadeIn(check, scale=0.7),
            FadeIn(payoff, shift=RIGHT * 0.08),
            Flash(check, color=GREEN_FIX, line_length=0.12, num_lines=7),
            run_time=0.4,
        )
        self.wait(1.0)
        self._close()
