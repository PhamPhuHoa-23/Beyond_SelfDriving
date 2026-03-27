# drivex/scenes/part01/p01_s07_vla_arch.py
# ─────────────────────────────────────────────────────────────────
# SCENE 1-07: Four VLA Architectures  (~120s)
#
# Spec: spec_intro_part01.md → SCENE 1-07
# 4 sequential sub-scenes, each on full screen:
#   A: GPT-Driver (zero-shot, text in → action out)
#   B: BEVDriver  (LiDAR/cam → BEV → LLM → waypoints)
#   C: EMMA/Waymo (camera → Gemini → multi-output)
#   D: DriveVLM   (dual-system: VLM slow + 3D fast)
# ─────────────────────────────────────────────────────────────────

from drivex.components.colors import (
    COL_BLUE, COL_GOLD, COL_WHITE, COL_LIGHT_BLUE,
    COL_GREEN, COL_PURPLE, COL_DEEP_BLUE, COL_DEEP_GREEN,
    COL_DEEP_PURPLE, COL_NAVY, BG_DARK,
)
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../..")))


_BG = "#0F172A"


def _io_box(label, color_fill=COL_DEEP_BLUE, color_stroke=COL_BLUE,
            width=2.8, height=0.75):
    rect = RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        fill_color=color_fill, fill_opacity=1,
        stroke_color=color_stroke, stroke_width=2,
    )
    lbl = Text(label, font_size=14, color=COL_WHITE).move_to(rect)
    return VGroup(rect, lbl)


def _arrow_right():
    return Arrow(LEFT * 0.1, RIGHT * 0.1, stroke_color=COL_BLUE,
                 stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.4)


def _badge(text, fill=COL_GOLD, text_color="#1A1A00"):
    b = RoundedRectangle(corner_radius=0.1, width=1.8, height=0.4,
                         fill_color=fill, fill_opacity=1, stroke_width=0)
    t = Text(text, font_size=13, color=text_color, weight=BOLD).move_to(b)
    return VGroup(b, t)


def _sub_intro(scene_obj, label):
    """Brief dark flash transition with architecture name."""
    flash_lbl = Text(label, font_size=28, color=COL_GOLD, weight=BOLD).center()
    scene_obj.play(FadeIn(flash_lbl), run_time=0.3)
    scene_obj.play(FadeOut(flash_lbl), run_time=0.3)


class P01S07VLAArch(Scene):
    """SCENE 1-07 — Four VLA Architectures"""

    def construct(self):
        self.camera.background_color = _BG

        # ══════════════════════════════════════════════════════
        # Sub-scene A: GPT-Driver
        # ══════════════════════════════════════════════════════
        _sub_intro(self, "GPT-Driver")
        sec_lbl = Text("GPT-Driver", font_size=24, color=COL_GOLD, weight=BOLD)
        sec_lbl.to_corner(UL, buff=0.5)
        self.play(FadeIn(sec_lbl), run_time=0.3)

        inp_a = _io_box("Language\nDescription of Scene",
                        COL_DEEP_BLUE, COL_BLUE, width=2.8, height=0.9)
        gpt_a = _io_box("GPT-3.5\n(Zero-shot)",
                        "#1A1A3A", "#7C3AED", width=2.4, height=0.9)
        out_a = _io_box("Motion\nPlanning Result",
                        COL_DEEP_GREEN, COL_GREEN, width=2.8, height=0.9)
        zero_badge = _badge("Zero-shot")

        row_a = VGroup(inp_a, _arrow_right(), gpt_a, _arrow_right(), out_a)
        row_a.arrange(RIGHT, buff=0.5).center()
        zero_badge.next_to(gpt_a, UP, buff=0.2)

        self.play(FadeIn(inp_a), run_time=0.3)
        self.play(GrowArrow(row_a[1]), FadeIn(gpt_a), run_time=0.4)
        self.play(FadeIn(zero_badge), run_time=0.2)
        self.play(GrowArrow(row_a[3]), FadeIn(out_a), run_time=0.4)

        note_a = Text(
            "GPT-3.5 absorbs traffic common sense from the internet.\nNo fine-tuning needed.",
            font_size=16, color=COL_LIGHT_BLUE,
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note_a), run_time=0.4)
        self.wait(1.5)
        self.play(FadeOut(VGroup(sec_lbl, row_a, zero_badge, note_a)), run_time=0.3)

        # ══════════════════════════════════════════════════════
        # Sub-scene B: BEVDriver
        # ══════════════════════════════════════════════════════
        _sub_intro(self, "BEVDriver")
        sec_lbl_b = Text("BEVDriver", font_size=24,
                         color=COL_GOLD, weight=BOLD)
        sec_lbl_b.to_corner(UL, buff=0.5)
        self.play(FadeIn(sec_lbl_b), run_time=0.3)

        sensors_b = VGroup(
            _io_box("LiDAR", COL_DEEP_BLUE, COL_BLUE, width=1.4, height=0.55),
            _io_box("Camera", COL_DEEP_BLUE, COL_BLUE, width=1.4, height=0.55),
        ).arrange(DOWN, buff=0.1)

        bev_b = _io_box("BEV Map\n(Bird's Eye View)",
                        "#1E293B", COL_BLUE, width=2.4, height=1.0)
        # grid lines on BEV box
        for i in range(3):
            bev_b.add(Line(bev_b[0].get_left() + RIGHT * (0.6 * (i + 1)) * (2.4 / 4),
                           bev_b[0].get_left() + RIGHT * (0.6 * (i + 1)
                                                          ) * (2.4 / 4) + UP * 0.9,
                           stroke_color=COL_BLUE, stroke_width=0.5, stroke_opacity=0.4))

        llm_b = _io_box("LLM\n(Reasoning)",
                        COL_DEEP_PURPLE, COL_PURPLE, width=2.2, height=1.0)
        out_b = VGroup(*[
            Dot(radius=0.08, color=COL_GREEN).move_to(
                np.array([0.3 * (j - 2), 0.2 * j, 0])
            )
            for j in range(5)
        ])
        out_b_box = _io_box("Waypoints", COL_DEEP_GREEN,
                            COL_GREEN, width=2.0, height=0.9)

        row_b = VGroup(sensors_b, _arrow_right(), bev_b, _arrow_right(), llm_b,
                       _arrow_right(), out_b_box)
        row_b.arrange(RIGHT, buff=0.45)
        # Force all major blocks to same vertical center for clean alignment
        for elem in [sensors_b, bev_b, llm_b, out_b_box]:
            elem.set_y(0)
        row_b.center()

        tag_b = Text("3D Spatial + Language Reasoning",
                     font_size=15, color=COL_LIGHT_BLUE)
        tag_b.next_to(row_b, DOWN, buff=0.4)

        self.play(FadeIn(sensors_b), run_time=0.3)
        self.play(GrowArrow(row_b[1]), FadeIn(bev_b), run_time=0.4)
        self.play(GrowArrow(row_b[3]), FadeIn(llm_b), run_time=0.4)
        self.play(GrowArrow(row_b[5]), FadeIn(out_b_box), run_time=0.4)
        self.play(FadeIn(tag_b), run_time=0.3)
        self.wait(1.5)
        self.play(FadeOut(VGroup(sec_lbl_b, row_b, tag_b)), run_time=0.3)

        # ══════════════════════════════════════════════════════
        # Sub-scene C: EMMA (Waymo)
        # ══════════════════════════════════════════════════════
        _sub_intro(self, "EMMA (Waymo)")
        sec_lbl_c = Text("EMMA (Waymo)", font_size=24,
                         color=COL_GOLD, weight=BOLD)
        sec_lbl_c.to_corner(UL, buff=0.5)
        self.play(FadeIn(sec_lbl_c), run_time=0.3)

        inp_c = VGroup(
            _io_box("Camera Frames", COL_DEEP_BLUE,
                    COL_BLUE, width=2.4, height=0.6),
            _io_box("Text Instruction", COL_DEEP_BLUE,
                    COL_BLUE, width=2.4, height=0.6),
        ).arrange(DOWN, buff=0.15).shift(LEFT * 3.8)

        emma_c = _io_box("EMMA\n(Gemini)\nThinking…",
                         "#1A1A2E", COL_GOLD, width=2.6, height=1.4)

        # Thinking animation: "Thinking…" updates 2×
        think_lbl = emma_c[1]

        outputs_c = VGroup(
            _io_box("Chain-of-Thought",   COL_DEEP_BLUE,
                    COL_BLUE,   width=2.2, height=0.6),
            _io_box("Trajectory",         COL_DEEP_GREEN,
                    COL_GREEN,  width=2.2, height=0.6),
            _io_box("Perception BBoxes",  "#2A1A00",
                    COL_GOLD,   width=2.2, height=0.6),
            _io_box("Road Graph",         "#2A0A3A",
                    COL_PURPLE, width=2.2, height=0.6),
        ).arrange(DOWN, buff=0.12).shift(RIGHT * 4.0)

        arrow_in_c = Arrow(inp_c.get_right(), emma_c.get_left(),
                           stroke_color=COL_BLUE, stroke_width=2, buff=0.15)

        self.play(FadeIn(inp_c), run_time=0.3)
        self.play(GrowArrow(arrow_in_c), FadeIn(emma_c), run_time=0.5)

        # "Thinking…" animation
        for _ in range(2):
            self.play(think_lbl.animate.set_opacity(0.3), run_time=0.25)
            self.play(think_lbl.animate.set_opacity(1.0), run_time=0.25)

        out_arrows_c = VGroup(*[
            Arrow(emma_c.get_right(), outputs_c[i].get_left(),
                  stroke_color=COL_WHITE, stroke_width=1.5, buff=0.12,
                  max_tip_length_to_length_ratio=0.35)
            for i in range(4)
        ])
        self.play(
            LaggedStart(
                *[Succession(GrowArrow(out_arrows_c[i]), FadeIn(outputs_c[i]))
                  for i in range(4)],
                lag_ratio=0.2,
            ),
            run_time=1.5,
        )

        quote_c = Text("THINK FIRST, THEN ACT",
                       font_size=20, color=COL_GOLD, weight=BOLD)
        quote_c.to_edge(DOWN, buff=0.5)
        self.play(Write(quote_c), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(VGroup(
            sec_lbl_c, inp_c, emma_c, outputs_c, arrow_in_c, out_arrows_c, quote_c,
        )), run_time=0.3)

        # ══════════════════════════════════════════════════════
        # Sub-scene D: DriveVLM
        # ══════════════════════════════════════════════════════
        _sub_intro(self, "DriveVLM")
        sec_lbl_d = Text("DriveVLM", font_size=24, color=COL_GOLD, weight=BOLD)
        sec_lbl_d.to_corner(UL, buff=0.5)
        self.play(FadeIn(sec_lbl_d), run_time=0.3)

        sensor_d = _io_box("Sensor Input\n(Camera / LiDAR)",
                           COL_DEEP_BLUE, COL_BLUE, width=2.6, height=1.0)
        sensor_d.shift(LEFT * 4.2)

        vlm_d = _io_box("VLM\nScene Understanding\n& Planning",
                        COL_DEEP_PURPLE, COL_PURPLE, width=3.0, height=1.4)
        vlm_d.shift(RIGHT * 0.8 + UP * 1.5)
        hz_vlm = Text("~1 Hz", font_size=13, color=COL_LIGHT_BLUE)
        hz_vlm.next_to(vlm_d, RIGHT, buff=0.12)

        pipe_d = _io_box("3D Perception\n& Trajectory",
                         COL_DEEP_GREEN, COL_GREEN, width=3.0, height=1.4)
        pipe_d.shift(RIGHT * 0.8 + DOWN * 1.5)
        hz_pipe = Text("~10 Hz", font_size=13, color=COL_GREEN)
        hz_pipe.next_to(pipe_d, RIGHT, buff=0.12)

        arr_d1 = Arrow(sensor_d.get_right(), vlm_d.get_left(),
                       stroke_color=COL_PURPLE, stroke_width=2, buff=0.15)
        arr_d2 = Arrow(sensor_d.get_right(), pipe_d.get_left(),
                       stroke_color=COL_GREEN, stroke_width=2, buff=0.15)

        self.play(FadeIn(sensor_d), run_time=0.3)
        self.play(GrowArrow(arr_d1), FadeIn(vlm_d),
                  FadeIn(hz_vlm), run_time=0.5)
        self.play(GrowArrow(arr_d2), FadeIn(pipe_d),
                  FadeIn(hz_pipe), run_time=0.5)

        # Frequency flash: 3D flashes 2× while VLM flashes 1×
        self.play(
            Succession(
                pipe_d.animate(rate_func=there_and_back,
                               run_time=0.3).scale(1.08),
                pipe_d.animate(rate_func=there_and_back,
                               run_time=0.3).scale(1.08),
            ),
            vlm_d.animate(rate_func=there_and_back, run_time=0.6).scale(1.04),
            run_time=0.6,
        )

        summary_d = Text(
            "Language = Core Architecture",
            font_size=22, color=COL_GOLD, weight=BOLD,
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(summary_d), run_time=0.5)
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            sec_lbl_d, sensor_d, vlm_d, hz_vlm,
            pipe_d, hz_pipe, arr_d1, arr_d2, summary_d,
        )), run_time=0.4)
        self.wait(0.2)
