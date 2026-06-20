"""P01-S03a — Modular stack: error cascade -> ego vehicle (clear layout)."""
from manimlib import *
from studio.components import (
    StudioScene, ACCENT_BLUE, RED_ERROR, PASTEL_BLUE, BG_CARD, BG_PAPER, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, vehicle_icon, content_column,
    error_propagation_marker, v_arrow,
)

MODULES = ["Perception", "Localization", "Prediction", "Planning", "Control"]


class P01S03AModular(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Modular Systems"

    def construct(self):
        self._open(self.SCENE_TITLE)

        blocks = [
            pipeline_block(m, width=2.5, height=0.62, fill=PASTEL_BLUE, stroke=ACCENT_BLUE)
            for m in MODULES
        ]
        content_column(*blocks, buff=0.28, x=-3.45, y=0.15)
        col_x = blocks[0][0].get_center()[0]
        arrows = VGroup(*(v_arrow(a, b, x=col_x) for a, b in zip(blocks[:-1], blocks[1:])))

        def reveal_block(block):
            halo = block[0].copy()
            halo.set_fill(opacity=0)
            halo.set_stroke(ACCENT_BLUE, width=5.0, opacity=0.5)
            self.play(
                FadeIn(block, shift=0.08 * DOWN, run_time=0.42),
                GrowFromCenter(halo, run_time=0.42),
            )
            self.play(halo.animate.scale(1.12).set_stroke(opacity=0), run_time=0.25)
            self.remove(halo)

        reveal_block(blocks[0])
        for arrow, block in zip(arrows, blocks[1:]):
            self.play(ShowCreation(arrow, run_time=0.28))
            reveal_block(block)

        err = error_propagation_marker(radius=0.11, label="Sensor noise", label_side=UP)
        err.next_to(blocks[0], LEFT, buff=0.22)
        self.play(FadeIn(err, scale=1.35), Flash(err[0], color=RED_ERROR, num_lines=12))

        prev = err
        for i, (block, arr) in enumerate(zip(blocks[1:], arrows)):
            radius = 0.11 + (i + 1) * 0.034
            label = "Amplified error" if block is blocks[-1] else None
            nxt = error_propagation_marker(radius=radius, label=label, label_side=UP)
            nxt.next_to(block, LEFT, buff=0.22)
            prev_ring = prev[0] if isinstance(prev[0], Circle) else prev[0][0]
            nxt_ring = nxt[0] if isinstance(nxt[0], Circle) else nxt[0][0]
            error_flash = arr.copy()
            error_flash.set_color(RED_ERROR)
            anims = [
                ShowPassingFlash(error_flash, time_width=0.35, run_time=0.42),
                TransformFromCopy(prev_ring, nxt_ring, run_time=0.38),
            ]
            if len(nxt) == 2 and isinstance(nxt[1], Text):
                anims.append(FadeIn(nxt[1], run_time=0.25))
            self.play(*anims)
            prev = nxt

        panel = RoundedRectangle(
            width=7.05, height=3.95, corner_radius=0.18,
            fill_color=BG_CARD, fill_opacity=0.72,
            stroke_color=ACCENT_BLUE, stroke_width=2.2,
        )
        panel.move_to(RIGHT * 2.05 + UP * 0.05)
        panel_title = Text(
            "Downstream consequences", font=FONT_PRIMARY, font_size=SIZE_LABEL,
            color=INK_DARK, weight=BOLD,
        )
        panel_title.next_to(panel.get_top(), DOWN, buff=0.2)
        divider = Line(
            panel.get_center() + UP * 1.18 + LEFT * 0.25,
            panel.get_center() + DOWN * 1.42 + LEFT * 0.25,
            stroke_color=ACCENT_BLUE, stroke_width=1.5, stroke_opacity=0.45,
        )

        car = vehicle_icon(color=ACCENT_BLUE, scale=0.78)
        car[0].set_stroke(INK_DARK, width=2.2)
        car_lbl = Text("Ego vehicle", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2, color=INK_DARK, weight=BOLD)
        cmd_lbl = Text(
            "Actuator command", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2, color=INK_MID, weight=BOLD,
        )
        compound_lbl = Text(
            "Errors compound", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2, color=RED_ERROR, weight=BOLD,
        )
        fail_lbl = Text(
            "Unsafe maneuver", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD,
        )
        ego_col = VGroup(cmd_lbl, car_lbl, car, compound_lbl, fail_lbl).arrange(
            DOWN, buff=0.21,
        )
        ego_col.move_to(panel.get_center() + LEFT * 2.0 + DOWN * 0.18)

        def issue_row(label):
            badge = Circle(
                radius=0.13,
                fill_color=RED_ERROR,
                fill_opacity=1.0,
                stroke_color=RED_ERROR,
                stroke_width=1.2,
            )
            bang = VGroup(
                Line(
                    UP * 0.065,
                    DOWN * 0.025,
                    stroke_color=BG_PAPER,
                    stroke_width=2.4,
                ),
                Circle(
                    radius=0.013,
                    fill_color=BG_PAPER,
                    fill_opacity=1.0,
                    stroke_width=0,
                ).shift(DOWN * 0.07),
            )
            bang.move_to(badge)
            text = Text(
                label, font=FONT_PRIMARY, font_size=SIZE_CAPS,
                color=RED_ERROR, weight=BOLD,
            )
            text.next_to(badge, RIGHT, buff=0.18)
            return VGroup(badge, bang, text)

        issues = VGroup(*[
            issue_row(t)
            for t in (
                "Error accumulation",
                "No joint optimization",
                "Cannot learn continuously",
            )
        ]).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        issues.move_to(panel.get_center() + RIGHT * 1.55 + DOWN * 0.02)

        control_y = blocks[-1][0].get_center()[1]
        car_y = car[0].get_center()[1]
        elbow_x = panel.get_left()[0] + 0.34
        cmd = VGroup(
            Line(
                blocks[-1][0].get_right() + RIGHT * 0.08,
                [elbow_x, control_y, 0],
                stroke_color=INK_MID, stroke_width=2.8,
            ),
            Line(
                [elbow_x, control_y, 0],
                [elbow_x, car_y, 0],
                stroke_color=INK_MID, stroke_width=2.8,
            ),
            Arrow(
                [elbow_x, car_y, 0],
                car[0].get_left() + LEFT * 0.1,
                thickness=2.8,
                max_tip_length_to_length_ratio=0.18,
                fill_color=INK_MID,
                buff=0,
            ),
        )

        self.play(FadeIn(panel), FadeIn(panel_title), FadeIn(divider))
        self.play(FadeIn(VGroup(cmd_lbl, car_lbl, car)), ShowCreation(cmd))
        self.play(
            cmd.animate.set_color(RED_ERROR),
            cmd_lbl.animate.set_color(RED_ERROR),
            FadeIn(compound_lbl),
        )
        sway_distance = 0.13
        sway_seconds_per_step = 0.36
        sway_state = {"side": 0}

        def sway_run_time(target_side):
            return max(0.18, abs(target_side - sway_state["side"]) * sway_seconds_per_step)

        def sway_car(target_side):
            delta = (target_side - sway_state["side"]) * sway_distance
            sway_state["side"] = target_side
            return car.animate.shift(RIGHT * delta)

        initial_sway_time = sway_run_time(1)
        self.play(FadeIn(fail_lbl), sway_car(1), run_time=initial_sway_time, rate_func=smooth)
        for target_side in (-1, 1, -1):
            sway_time = sway_run_time(target_side)
            self.play(sway_car(target_side), run_time=sway_time, rate_func=smooth)

        def reveal_issue(row):
            halo = row[0].copy()
            halo.set_fill(opacity=0)
            halo.set_stroke(RED_ERROR, width=4.0, opacity=0.45)
            reveal_sway_time = sway_run_time(1)
            self.play(
                FadeIn(row, shift=LEFT * 0.15, run_time=0.35),
                GrowFromCenter(halo, run_time=0.35),
                sway_car(1),
                run_time=reveal_sway_time,
                rate_func=smooth,
            )
            fade_sway_time = sway_run_time(-1)
            self.play(
                halo.animate.scale(1.85).set_stroke(opacity=0),
                sway_car(-1),
                run_time=fade_sway_time,
                rate_func=smooth,
            )
            self.remove(halo)

        for issue in issues:
            reveal_issue(issue)
        settle_sway_time = sway_run_time(0)
        self.play(sway_car(0), run_time=settle_sway_time, rate_func=smooth)
        self.wait(1.5)
        self._close()
