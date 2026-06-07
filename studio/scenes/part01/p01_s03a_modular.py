"""P01-S03a — Modular stack: error cascade -> ego vehicle (clear layout)."""
from manimlib import *
from studio.components import (
    StudioScene, ACCENT_BLUE, RED_ERROR, PASTEL_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, LEFT_X, RIGHT_X,
    pipeline_block, vehicle_icon, content_column,
    error_propagation_marker, h_arrow, v_arrow,
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
        content_column(*blocks, buff=0.28, x=LEFT_X + 0.5, y=0.15)
        col_x = blocks[0][0].get_center()[0]
        arrows = VGroup(*(v_arrow(a, b, x=col_x) for a, b in zip(blocks[:-1], blocks[1:])))

        self.play(LaggedStart(*(FadeIn(b) for b in blocks), lag_ratio=0.1))
        self.play(ShowCreation(arrows))

        err = error_propagation_marker(radius=0.11, label="Sensor noise")
        err.next_to(blocks[0], LEFT, buff=0.22)
        self.play(FadeIn(err, scale=1.35), Flash(err[0], color=RED_ERROR, num_lines=12))

        prev = err
        for i, (block, arr) in enumerate(zip(blocks[1:], arrows)):
            radius = 0.11 + (i + 1) * 0.034
            label = "Amplified error" if block is blocks[-1] else None
            nxt = error_propagation_marker(radius=radius, label=label)
            nxt.next_to(block, LEFT, buff=0.22)
            prev_ring = prev[0] if isinstance(prev[0], Circle) else prev[0][0]
            nxt_ring = nxt[0] if isinstance(nxt[0], Circle) else nxt[0][0]
            anims = [
                arr.animate.set_color(RED_ERROR),
                ShowPassingFlash(arr.copy(), time_width=0.35, run_time=0.42),
                TransformFromCopy(prev_ring, nxt_ring, run_time=0.38),
            ]
            if len(nxt) == 2 and isinstance(nxt[1], Text):
                anims.append(FadeIn(nxt[1], run_time=0.25))
            self.play(*anims)
            prev = nxt

        car = vehicle_icon(color=ACCENT_BLUE, scale=0.72)
        car[0].set_stroke(INK_DARK, width=2.2)
        car_lbl = Text("Ego vehicle", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        cmd_lbl = Text(
            "Actuator command", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID, weight=BOLD,
        )
        compound_lbl = Text(
            "Errors compound", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=RED_ERROR, weight=BOLD,
        )
        ego_col = VGroup(cmd_lbl, car_lbl, car).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        ego_col.next_to(blocks[-1], RIGHT, buff=1.35)
        ego_col.align_to(blocks[-1], UP)
        compound_lbl.next_to(car, DOWN, buff=0.38, aligned_edge=LEFT)
        compound_lbl.align_to(car, LEFT)

        cmd = h_arrow(blocks[-1], ego_col, color=INK_MID, buff=0.14, y=blocks[-1][0].get_center()[1])

        self.play(FadeIn(ego_col), ShowCreation(cmd))
        self.play(
            cmd.animate.set_color(RED_ERROR),
            cmd_lbl.animate.set_color(RED_ERROR),
            FadeIn(compound_lbl),
        )
        fail_lbl = Text(
            "Unsafe maneuver", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD,
        )
        fail_lbl.next_to(compound_lbl, DOWN, buff=0.22, aligned_edge=LEFT)
        self.play(
            car.animate.shift(RIGHT * 0.32),
            FadeIn(fail_lbl),
            run_time=0.85,
            rate_func=linear,
        )

        issues = content_column(
            *[
                Text(t, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
                for t in (
                    "X  Error accumulation",
                    "X  No joint optimization",
                    "X  Cannot learn continuously",
                )
            ],
            buff=0.16, x=RIGHT_X + 0.15, y=0.35, aligned_edge=LEFT,
        )
        self.play(LaggedStart(*(FadeIn(c, shift=LEFT * 0.15) for c in issues), lag_ratio=0.15))
        self.wait(1.5)
        self._close()
