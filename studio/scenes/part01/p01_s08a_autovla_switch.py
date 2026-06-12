"""P01-S08a — AutoVLA: semicircle gauge (FAST/SLOW needle), centered phases."""
from manimlib import *
from studio.components import (
    StudioScene, GOLD_KEY, GOLD_RICH, ACCENT_BLUE, GREEN_FIX, INK_DARK,
    PASTEL_AMBER, PASTEL_BLUE,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, h_arrow, contribution_badge, place_footer,
)

# ── Slow-phase layout (4 elements centered in canvas) ──────────────────────
#   complex(-4.4) → gauge(-1.5) → slow(1.4) → CoT(4.1)   all at same y
CLF_X_SLOW = -1.55
CMP_X = -4.85
SLW_X = 1.55
COT_X = 4.55


def _reasoning_gauge(*, on_fast: bool = True) -> VGroup:
    """Semi-circle gauge — needle + FAST/SLOW labels inside arc."""
    box = RoundedRectangle(
        width=3.05, height=2.2, corner_radius=0.16,
        fill_color=PASTEL_AMBER, fill_opacity=1.0,
        stroke_color=GOLD_KEY, stroke_width=2.8,
    )
    title = Text("Scene classifier", font=FONT_PRIMARY, font_size=SIZE_LABEL - 1,
                 color=INK_DARK, weight=BOLD)
    title.move_to(box.get_center() + UP * 0.72)
    center = box.get_center() + DOWN * 0.04
    arc_bg   = Arc(radius=0.52, start_angle=5*PI/6, angle=-4*PI/6, stroke_color=INK_DARK,   stroke_width=5)
    arc_fast = Arc(radius=0.52, start_angle=5*PI/6, angle=-2*PI/6, stroke_color=GREEN_FIX,  stroke_width=5)
    arc_slow = Arc(radius=0.52, start_angle=PI/2,   angle=-2*PI/6, stroke_color=GOLD_RICH,  stroke_width=5)
    for arc in (arc_bg, arc_fast, arc_slow):
        arc.move_arc_center_to(center)
    fast_lbl = Text("FAST", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GREEN_FIX,  weight=BOLD)
    slow_lbl = Text("SLOW", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GOLD_RICH, weight=BOLD)
    fast_lbl.move_to(center + LEFT * 0.46 + DOWN * 0.43)
    slow_lbl.move_to(center + RIGHT * 0.46 + DOWN * 0.43)
    # PI/6 → needle upper-LEFT = FAST;  -PI/6 → upper-RIGHT = SLOW
    needle_angle = PI / 6 if on_fast else -PI / 6
    tip = center + rotate_vector(UP * 0.43, needle_angle)
    needle = Line(center, tip, stroke_color=INK_DARK, stroke_width=3.5)
    needle.add_tip()
    gauge = VGroup(arc_bg, arc_fast, arc_slow, fast_lbl, slow_lbl, needle)
    return VGroup(box, title, gauge)


class P01S08AAutoVLASwitch(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "AutoVLA — Adaptive Reasoning"

    def construct(self):
        self._open(self.SCENE_TITLE)

        # ── Phase 1: FAST path ────────────────────────────────────────────────
        clf = _reasoning_gauge(on_fast=True)
        box, needle = clf[0], clf[2][-1]

        simple    = pipeline_block("Simple scene",  width=2.25, height=0.58, fill=PASTEL_BLUE,   stroke=ACCENT_BLUE)
        fast      = pipeline_block("Fast action",   width=2.25, height=0.58, fill="#C8EDD0",     stroke=GREEN_FIX)
        simple[1].scale(0.9)
        fast[1].scale(0.9)
        fast_note = Text("Skip reasoning", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GREEN_FIX, weight=BOLD)
        fast_grp  = VGroup(fast, fast_note).arrange(DOWN, buff=0.18)

        row_a = VGroup(simple, clf, fast_grp)
        row_a.arrange(RIGHT, buff=0.85, aligned_edge=ORIGIN)
        row_a.move_to(UP * 0.12)
        fast_grp.shift(UP * (box.get_center()[1] - fast[0].get_center()[1]))

        ROW_Y = box.get_center()[1]   # save y — all slow elements share this y

        arr_sf = h_arrow(simple, box,  y=ROW_Y, color=INK_DARK)
        arr_ff = h_arrow(box,  fast,   y=ROW_Y, color=GREEN_FIX)

        self.play(FadeIn(row_a), ShowCreation(arr_sf), ShowCreation(arr_ff))
        self.wait(0.6)

        # ── Phase 2: SLOW path ────────────────────────────────────────────────
        complex_blk = pipeline_block("Complex scene\n(night / rain)", width=2.45, height=0.72,
                                     fill=PASTEL_BLUE, stroke=ACCENT_BLUE)
        slow_blk    = pipeline_block("Slow reasoning", width=2.25, height=0.58,
                                     fill=PASTEL_AMBER, stroke=GOLD_RICH)
        complex_blk[1].scale(0.84)
        slow_blk[1].scale(0.86)

        # CoT panel — plain RoundedRectangle, no stage_panel hidden bounding-box
        cot_lines = VGroup(
            Text("Person waving:", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2, color=INK_DARK, weight=BOLD),
            Text("slow down and assess", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2, color=INK_DARK, weight=BOLD),
        ).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        if cot_lines.get_width() > 2.3:
            cot_lines.scale(2.3 / cot_lines.get_width())
        cot_bg = RoundedRectangle(
            width=max(cot_lines.get_width() + 0.38, 2.65),
            height=max(cot_lines.get_height() + 0.34, 0.92),
            corner_radius=0.12,
            fill_color=PASTEL_AMBER, fill_opacity=1.0,
            stroke_color=GOLD_RICH, stroke_width=2.5,
        )
        cot_title = Text("Chain-of-thought", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                         color=GOLD_RICH, weight=BOLD)

        # Position all slow elements at ROW_Y — gauge MOVES to CLF_X_SLOW
        complex_blk.move_to([CMP_X, ROW_Y, 0])
        slow_blk.move_to([SLW_X, ROW_Y, 0])
        cot_bg.move_to([COT_X, ROW_Y, 0])
        cot_lines.move_to(cot_bg.get_center())
        cot_title.next_to(cot_bg, UP, buff=0.18)

        # Transition: fade old, slide gauge left, fade in new
        self.play(
            FadeOut(simple), FadeOut(fast_grp),
            FadeOut(arr_sf), FadeOut(arr_ff),
            clf.animate.move_to([CLF_X_SLOW, ROW_Y, 0]),
            FadeIn(complex_blk), FadeIn(slow_blk),
            FadeIn(cot_bg), FadeIn(cot_title),
            run_time=0.9,
        )
        # Rotate needle FAST → SLOW (upper-left → upper-right = -PI/3 CW)
        self.play(
            needle.animate.rotate(-PI / 3, about_point=needle.get_start()),
            run_time=0.7,
        )

        # Horizontal arrows — all same y, perfectly straight
        arr_cs = Arrow(complex_blk.get_right(), box.get_left(),
                       color=ACCENT_BLUE, stroke_width=2.5, buff=0.05)
        arr_gs = Arrow(box.get_right(), slow_blk.get_left(),
                       color=GOLD_RICH, stroke_width=2.5, buff=0.05)
        arr_sc = Arrow(slow_blk.get_right(), cot_bg.get_left(),
                       color=GOLD_RICH, stroke_width=2.5, buff=0.05)
        self.play(ShowCreation(arr_cs), ShowCreation(arr_gs), ShowCreation(arr_sc), run_time=0.6)
        self.play(LaggedStart(*(Write(ln) for ln in cot_lines), lag_ratio=0.35, run_time=1.0))

        badge = contribution_badge("IROS 2025 Best Paper  ·  UCLA", color=GOLD_KEY)
        place_footer(badge)
        self.play(FadeIn(badge))
        self.wait(2.5)
        self._close()
