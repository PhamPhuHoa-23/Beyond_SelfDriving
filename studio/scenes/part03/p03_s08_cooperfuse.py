"""P03-S08 CooperFuse: Gaussian late fusion."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, GOLD_RICH, ACCENT_BLUE,
    ACCENT_GREEN, ACCENT_TEAL, INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL,
    SIZE_CAPS, vehicle_icon,
)

SCRIPT = "CooperFuse keeps multiple detections, scores consistency, and fuses them into one tight box."


def _txt(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    return Text(text, font=FONT_PRIMARY, font_size=size, color=color, weight=weight)


def _gaussian(center, rx, ry, color, *, opacity=0.18, rings=4, angle=0.0) -> VGroup:
    group = VGroup()
    for i in range(rings):
        scale = 1.0 - i * 0.18
        e = Ellipse(
            width=2 * rx * scale,
            height=2 * ry * scale,
            fill_color=color,
            fill_opacity=opacity * (0.35 + i * 0.18),
            stroke_color=color,
            stroke_width=1.4,
            stroke_opacity=0.55 - i * 0.08,
        )
        e.rotate(angle)
        e.move_to(center)
        group.add(e)
    return group


def _det_box(center, color, *, angle=0.0, opacity=0.18) -> VGroup:
    box = RoundedRectangle(
        width=0.88,
        height=0.45,
        corner_radius=0.06,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=color,
        stroke_width=2.2,
    )
    tick = Line(LEFT * 0.17, RIGHT * 0.18, stroke_color=WHITE, stroke_width=1.8, stroke_opacity=0.65)
    obj = VGroup(box, tick)
    obj.rotate(angle)
    obj.move_to(center)
    return obj


def _agent_detection(
    label: str,
    color: str,
    base: np.ndarray,
    shift: np.ndarray,
    *,
    angle=0.0,
    agent_offset: np.ndarray = DOWN * 0.72,
    tag_dir: np.ndarray = DOWN,
) -> VGroup:
    agent = vehicle_icon(color=color, scale=0.36)
    agent.move_to(base + agent_offset)
    tag = _txt(label, size=SIZE_CAPS - 2, color=color, weight=BOLD)
    tag.next_to(agent, tag_dir, buff=0.05)
    det_center = base + shift
    cloud = _gaussian(det_center, 0.56, 0.34, color, opacity=0.18, rings=3, angle=angle)
    box = _det_box(det_center, color, angle=angle, opacity=0.12)
    ray = DashedLine(agent.get_center() + UP * 0.18, det_center, stroke_color=color, stroke_width=1.2, dash_length=0.06, stroke_opacity=0.56)
    return VGroup(cloud, box, ray, agent, tag)


def _score_chip(title: str, value: str, color: str, y: float) -> VGroup:
    left = Dot(radius=0.055, color=color)
    name = _txt(title, size=SIZE_CAPS - 3, color=INK_DARK, weight=BOLD)
    bar_bg = RoundedRectangle(width=1.32, height=0.1, corner_radius=0.05, fill_color="#D7DEE8", fill_opacity=0.9, stroke_width=0)
    bar_fg = RoundedRectangle(width=0.96 if value == "high" else 0.72, height=0.1, corner_radius=0.05, fill_color=color, fill_opacity=0.92, stroke_width=0)
    bar_fg.align_to(bar_bg, LEFT)
    group = VGroup(left, name, bar_bg, bar_fg)
    group.arrange(RIGHT, buff=0.1)
    group.move_to([0.0, y, 0])
    return group


class P03S08CooperFuse(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "CooperFuse: Gaussian Fusion"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        stage_titles = VGroup(
            _txt("1. multi-agent boxes", size=SIZE_LABEL, color=ACCENT_BLUE, weight=BOLD).move_to(LEFT * 4.2 + UP * 1.58),
            _txt("2. consistency scores", size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD).move_to(UP * 1.58),
            _txt("3. fused estimate", size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD).move_to(RIGHT * 4.05 + UP * 1.58),
        )

        target_shadow = _gaussian(LEFT * 4.25 + DOWN * 0.1, 0.72, 0.42, INK_MID, opacity=0.08, rings=2)
        target = _det_box(LEFT * 4.25 + DOWN * 0.1, INK_MID, opacity=0.05)
        det_ego = _agent_detection("ego", ACCENT_BLUE, LEFT * 5.25 + DOWN * 0.15, RIGHT * 1.02 + UP * 0.1, angle=0.0)
        det_cav = _agent_detection(
            "cav",
            ACCENT_GREEN,
            LEFT * 4.95 + UP * 0.18,
            RIGHT * 0.85 + DOWN * 0.18,
            angle=0.08,
            agent_offset=UP * 0.78,
            tag_dir=LEFT,
        )
        det_rsu = _agent_detection("rsu", GOLD_RICH, LEFT * 3.25 + DOWN * 0.15, LEFT * 0.64 + UP * 0.28, angle=-0.12)
        detections = VGroup(det_ego, det_cav, det_rsu)
        left_note = _txt("keep weak evidence", size=SIZE_CAPS - 1, color=INK_MID, weight=BOLD)
        left_note.move_to(LEFT * 4.2 + DOWN * 1.7)

        link_1 = Arrow(LEFT * 2.05 + DOWN * 0.62, LEFT * 0.52 + DOWN * 0.62, buff=0, stroke_width=2.6, fill_color=INK_MID)

        score_panel = VGroup(
            _score_chip("confidence", "high", ACCENT_BLUE, 0.78),
            _score_chip("motion match", "high", ACCENT_GREEN, 0.44),
            _score_chip("scale match", "mid", GOLD_RICH, 0.1),
        )
        mixer = Circle(radius=0.36, stroke_color=GOLD_RICH, stroke_width=2.2, fill_color=GOLD_RICH, fill_opacity=0.08)
        mixer.move_to(DOWN * 0.62)
        sigma = Text("Σ", font=FONT_PRIMARY, font_size=34, color=GOLD_RICH, weight=BOLD)
        sigma.move_to(mixer)
        mid_note = _txt("weighted Gaussian fusion", size=SIZE_CAPS - 1, color=INK_MID, weight=BOLD)
        mid_note.move_to(DOWN * 1.7)
        mid_group = VGroup(score_panel, mixer, sigma, mid_note)

        link_2 = Arrow(RIGHT * 0.52 + DOWN * 0.62, RIGHT * 2.6 + DOWN * 0.62, buff=0, stroke_width=2.6, fill_color=INK_MID)

        raw_faint = VGroup(
            _gaussian(RIGHT * 4.0 + DOWN * 0.02 + LEFT * 0.22, 0.54, 0.34, ACCENT_BLUE, opacity=0.1, rings=2),
            _gaussian(RIGHT * 4.0 + DOWN * 0.02 + RIGHT * 0.22, 0.52, 0.32, ACCENT_GREEN, opacity=0.1, rings=2),
            _gaussian(RIGHT * 4.0 + DOWN * 0.02 + UP * 0.18, 0.48, 0.28, GOLD_RICH, opacity=0.1, rings=2),
        )
        fused_cloud = _gaussian(RIGHT * 4.0 + DOWN * 0.02, 0.34, 0.2, GREEN_FIX, opacity=0.32, rings=4)
        fused_box = _det_box(RIGHT * 4.0 + DOWN * 0.02, GREEN_FIX, opacity=0.16)
        ok = _txt("one stable box", size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD)
        ok.move_to(RIGHT * 4.0 + DOWN * 1.05)
        no_drop = _txt("no hard NMS drop", size=SIZE_CAPS - 1, color=RED_ERROR, weight=BOLD)
        no_drop.move_to(RIGHT * 4.0 + DOWN * 1.55)
        right_group = VGroup(raw_faint, fused_cloud, fused_box, ok, no_drop)

        self.play(FadeIn(stage_titles), run_time=0.35)
        self.play(FadeIn(target_shadow), FadeIn(target), FadeIn(left_note), run_time=0.45)
        for det in (det_ego, det_cav, det_rsu):
            cloud, box, ray, agent, tag = det
            self.play(FadeIn(agent), FadeIn(tag), ShowCreation(ray), run_time=0.32)
            self.play(FadeIn(cloud), GrowFromCenter(box), run_time=0.38)
            self.play(Flash(box, color=box[0].get_stroke_color(), line_length=0.12, num_lines=6), run_time=0.22)
        self.play(ShowCreation(link_1), run_time=0.35)
        self.play(LaggedStart(*(FadeIn(c) for c in score_panel), lag_ratio=0.18), FadeIn(mixer), FadeIn(sigma), FadeIn(mid_note), run_time=0.9)
        self.play(Flash(mixer, color=GOLD_RICH, line_length=0.2, num_lines=10), run_time=0.5)
        self.play(ShowCreation(link_2), run_time=0.35)
        self.play(FadeIn(raw_faint), run_time=0.35)
        self.play(FadeIn(fused_cloud), GrowFromCenter(fused_box), FadeIn(ok), FadeIn(no_drop), run_time=0.75)
        self.play(Flash(fused_box, color=GREEN_FIX, line_length=0.22, num_lines=8), run_time=0.5)
        self.wait(1.5)
        self._close()
