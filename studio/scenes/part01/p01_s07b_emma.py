"""P01-S07b — EMMA: thinking VLM, gradual CoT, single-border panel."""
from manimlib import *
from studio.components import (
    StudioScene, ACCENT_BLUE, PURPLE_MODEL, GOLD_RICH, CYAN_RADAR,
    INK_DARK, INK_MID, PASTEL_AMBER, PASTEL_BLUE,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    h_arrow, CONTENT_TOP,
)

THOUGHTS = [
    "There is a pedestrian crossing...",
    "Light is red — must not proceed.",
    "Brake. Yield.",
]


def _camera_icon() -> VGroup:
    frame = RoundedRectangle(
        width=1.15, height=0.82, corner_radius=0.08,
        fill_color=PASTEL_BLUE, fill_opacity=1.0,
        stroke_color=ACCENT_BLUE, stroke_width=2.5,
    )
    stripes = VGroup(*[
        Line(
            frame.get_left() + 0.14 * RIGHT + (i - 1) * 0.2 * UP,
            frame.get_right() + 0.14 * LEFT + (i - 1) * 0.2 * UP,
            stroke_color=ACCENT_BLUE, stroke_width=2.2,
        )
        for i in range(3)
    ])
    return VGroup(frame, stripes)


def _vlm_with_thinking() -> VGroup:
    layers = VGroup()
    for x in (-0.22, 0.0, 0.22):
        col = VGroup(*[
            Dot(radius=0.05, color=PURPLE_MODEL).set_stroke(INK_DARK, width=1.2)
            for _ in range(3)
        ])
        col.arrange(DOWN, buff=0.12)
        col.move_to(x * RIGHT)
        layers.add(col)
    lines = VGroup()
    for c1, c2 in zip(layers[:-1], layers[1:]):
        for d1 in c1:
            for d2 in c2:
                lines.add(Line(
                    d1.get_center(), d2.get_center(),
                    stroke_color=INK_MID, stroke_width=1.4, stroke_opacity=0.55,
                ))
    w = layers.get_width() + 0.32
    h = layers.get_height() + 0.32
    box = RoundedRectangle(
        width=w, height=h, corner_radius=0.1,
        fill_color="#EDE9FE", fill_opacity=1.0,
        stroke_color=PURPLE_MODEL, stroke_width=2.5,
    )
    box.move_to(layers.get_center())
    spinner = Arc(
        radius=0.28, start_angle=0, angle=TAU * 0.7,
        stroke_color=GOLD_RICH, stroke_width=2.8,
    )
    spinner.move_to(box.get_center())
    return VGroup(box, lines, layers, spinner)


def _output_chip(label: str, *, fill: str, stroke: str) -> VGroup:
    rect = RoundedRectangle(
        width=1.48, height=0.44, corner_radius=0.13,
        fill_color=fill, fill_opacity=1.0,
        stroke_color=stroke, stroke_width=2.2,
    )
    text = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS - 1, color=INK_DARK, weight=BOLD)
    text.set_max_width(rect.get_width() - 0.18)
    text.move_to(rect.get_center())
    return VGroup(rect, text)


class P01S07BEMMA(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "EMMA (Waymo)"

    def construct(self):
        header = self._open(self.SCENE_TITLE)

        cam_icon = _camera_icon()
        cam_lbl = Text("Camera", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_BLUE, weight=BOLD)
        cam_lane = VGroup(cam_lbl, cam_icon).arrange(DOWN, buff=0.12)
        cam_lbl.set_x(cam_icon.get_center()[0])

        vlm_body = _vlm_with_thinking()
        spinner = vlm_body[3]
        vlm_icon = VGroup(vlm_body[0], vlm_body[1], vlm_body[2])
        vlm_lbl = Text("Gemini VLM", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=PURPLE_MODEL, weight=BOLD)
        vlm_lane = VGroup(vlm_lbl, vlm_body).arrange(DOWN, buff=0.12)
        vlm_lbl.set_x(vlm_icon.get_center()[0])

        cot_lines = VGroup(*[
            Text(
                t, font=FONT_PRIMARY, font_size=SIZE_CAPS - 1,
                color=GOLD_RICH if i == 2 else INK_DARK,
                **({"weight": BOLD} if i == 2 else {}),
            )
            for i, t in enumerate(THOUGHTS)
        ])
        cot_lines.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        cot_box = RoundedRectangle(
            width=max(cot_lines.get_width() + 0.45, 4.25),
            height=cot_lines.get_height() + 0.35,
            corner_radius=0.14,
            fill_color=PASTEL_AMBER, fill_opacity=1.0,
            stroke_color=GOLD_RICH, stroke_width=2.2,
        )
        cot_lines.move_to(cot_box.get_center())
        cot_title = Text(
            "Chain-of-thought", font=FONT_PRIMARY, font_size=SIZE_LABEL,
            color=GOLD_RICH, weight=BOLD,
        )
        cot_title.next_to(cot_box, UP, buff=0.12)
        cot_panel = VGroup(cot_box, cot_lines, cot_title)
        for line in cot_lines:
            line.set_opacity(0)
            line.set_color(GOLD_RICH if line is cot_lines[2] else INK_DARK)

        out_blocks = VGroup(
            _output_chip("Trajectory", fill=PASTEL_BLUE, stroke=ACCENT_BLUE),
            _output_chip("BBox", fill=PASTEL_BLUE, stroke=CYAN_RADAR),
            _output_chip("Road graph", fill=PASTEL_AMBER, stroke=PURPLE_MODEL),
        ).arrange(RIGHT, buff=0.22)
        out_lbl = Text(
            "Structured predictions", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2,
            color=INK_MID, weight=BOLD,
        )
        structured_group = VGroup(out_lbl, out_blocks).arrange(DOWN, buff=0.12)

        input_group = VGroup(cam_lane, vlm_lane).arrange(RIGHT, buff=0.78, aligned_edge=DOWN)
        output_group = VGroup(cot_panel, structured_group).arrange(DOWN, buff=0.28)
        output_brace = Brace(output_group, LEFT, buff=0.08)
        output_brace.set_color(GOLD_RICH)
        output_bundle = VGroup(output_brace, output_group)

        layout = VGroup(input_group, output_bundle).arrange(RIGHT, buff=0.74)
        layout.move_to(UP * 0.12 + LEFT * 0.08)
        if layout.get_top()[1] > CONTENT_TOP - 0.1:
            layout.shift(DOWN * (layout.get_top()[1] - (CONTENT_TOP - 0.1)))

        flow_y = output_brace.get_center()[1]
        cam_lane.shift(UP * (flow_y - cam_icon.get_center()[1]))
        vlm_lane.shift(UP * (flow_y - vlm_icon.get_center()[1]))
        a_cam_vlm = h_arrow(cam_icon, vlm_icon, y=flow_y, color=CYAN_RADAR, buff=0.12)
        a_vlm_outputs = h_arrow(vlm_icon, output_brace, y=flow_y, color=GOLD_RICH, buff=0.12)

        self.play(FadeIn(cam_lane))
        self.play(ShowCreation(a_cam_vlm), FadeIn(vlm_lane))
        self.play(
            Rotate(spinner, angle=-TAU, about_point=spinner.get_center(), rate_func=linear),
            run_time=1.2,
        )
        self.play(FadeOut(spinner))
        self.play(ShowCreation(a_vlm_outputs), ShowCreation(output_brace), FadeIn(cot_box), FadeIn(cot_title))
        for line in cot_lines:
            self.play(line.animate.set_opacity(1), run_time=0.42)
            line.set_color(GOLD_RICH if line is cot_lines[2] else INK_DARK)

        self.play(
            FadeIn(structured_group),
        )
        self.wait(1.5)
        self._close()
