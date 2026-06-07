"""P01-S07c — DriveVLM: input, Hz-labelled rails, merge to action (no packet dots)."""
from manimlib import *
from studio.components import (
    StudioScene, ACCENT_BLUE, GOLD_RICH, INK_MID, INK_DARK, GREEN_FIX,
    PASTEL_BLUE, PASTEL_AMBER, PASTEL_GREEN,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    place_footer, pipeline_block, pipeline_row,
)

FAST_HZ = 10
SLOW_HZ = 2


def _rail_container(blocks: list[VGroup]) -> RoundedRectangle:
    rail = VGroup(*blocks)
    box = RoundedRectangle(
        width=rail.get_width() + 0.42,
        height=rail.get_height() + 0.34,
        corner_radius=0.18,
        fill_opacity=0.0,
        stroke_color=INK_DARK,
        stroke_width=1.8,
        stroke_opacity=0.85,
    )
    box.move_to(rail.get_center())
    box.set_stroke(INK_DARK, width=1.8, opacity=0.85)
    return box


def _loader_segments(container: Mobject, *, color: str, width: float = 5.0) -> VGroup:
    segments = VGroup(container.copy(), container.copy())
    for seg in segments:
        seg.set_fill(opacity=0)
        seg.set_stroke(color, width=width, opacity=0)
    return segments


def _update_loader(
    segments: VGroup,
    container: Mobject,
    alpha: float,
    *,
    loops: float,
    span: float = 0.18,
    color: str,
) -> VGroup:
    start = (alpha * loops) % 1.0
    end = start + span
    template = container.copy()

    segments[0].pointwise_become_partial(template, start, min(end, 1.0))
    segments[0].set_fill(opacity=0)
    segments[0].set_stroke(color, width=5.0, opacity=1.0)

    if end > 1.0:
        segments[1].pointwise_become_partial(template, 0.0, end - 1.0)
        segments[1].set_fill(opacity=0)
        segments[1].set_stroke(color, width=5.0, opacity=1.0)
    else:
        segments[1].set_stroke(opacity=0)
    return segments


class P01S07CDriveVLM(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "DriveVLM (Dual-System)"

    def construct(self):
        self._open(self.SCENE_TITLE)

        bw, bh, gap = 1.72, 0.48, 0.32

        scene_in = pipeline_block(
            "Driving\nscene", width=1.5, height=0.68, fill=PASTEL_BLUE, stroke=ACCENT_BLUE,
        )

        fast_blocks = [
            pipeline_block(n, width=bw, height=bh, fill=PASTEL_BLUE, stroke=ACCENT_BLUE)
            for n in ("Perception", "Planning", "Control")
        ]
        fast_pipe = pipeline_row(fast_blocks, gap=gap)
        fast_tag = VGroup(
            Text("Fast", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD),
            Text(f"{FAST_HZ} Hz", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        fast_tag.next_to(fast_blocks[0], UP, buff=0.15)
        fast_tag.align_to(fast_blocks[0], LEFT)
        fast_group = VGroup(fast_tag, fast_pipe)

        slow_blocks = [
            pipeline_block("Vision", width=bw, height=bh, fill=PASTEL_BLUE, stroke=ACCENT_BLUE),
            pipeline_block("VLM", width=bw, height=bh, fill=PASTEL_AMBER, stroke=GOLD_RICH),
            pipeline_block("Plan", width=bw, height=bh, fill=PASTEL_BLUE, stroke=ACCENT_BLUE),
        ]
        slow_pipe = pipeline_row(slow_blocks, gap=gap)
        slow_tag = VGroup(
            Text("Slow", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD),
            Text(f"{SLOW_HZ} Hz", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GOLD_RICH),
        ).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        slow_tag.next_to(slow_blocks[0], DOWN, buff=0.15)
        slow_tag.align_to(slow_blocks[0], LEFT)
        slow_group = VGroup(slow_tag, slow_pipe)

        scene_in.move_to(LEFT * 5.45 + UP * 0.35)
        fast_pipe.move_to(LEFT * 0.8 + UP * 1.15)
        slow_pipe.move_to(LEFT * 0.8 + DOWN * 0.15)
        fast_tag.next_to(fast_blocks[0], UP, buff=0.15)
        fast_tag.align_to(fast_blocks[0], LEFT)
        slow_tag.next_to(slow_blocks[0], DOWN, buff=0.15)
        slow_tag.align_to(slow_blocks[0], LEFT)

        fast_container = _rail_container(fast_blocks)
        slow_container = _rail_container(slow_blocks)
        fast_loader = _loader_segments(fast_container, color=ACCENT_BLUE)
        slow_loader = _loader_segments(slow_container, color=GOLD_RICH)

        action = pipeline_block("Action", width=2.35, height=0.5, fill=PASTEL_GREEN, stroke=GREEN_FIX)
        action.move_to(RIGHT * 5.05 + UP * 0.5)

        fork_x = scene_in[0].get_right()[0] + 0.55
        fork_stem = Arrow(
            scene_in[0].get_right() + RIGHT * 0.06,
            np.array([fork_x, scene_in[0].get_center()[1], 0.0]),
            thickness=2.8,
            max_tip_length_to_length_ratio=0.01,
            fill_color=INK_MID,
            buff=0,
        )
        fork_split = Line(
            [fork_x, slow_blocks[0][0].get_center()[1], 0],
            [fork_x, fast_blocks[0][0].get_center()[1], 0],
            stroke_color=INK_MID,
            stroke_width=2.8,
        )
        in_fast = Arrow(
            [fork_x, fast_blocks[0][0].get_center()[1], 0],
            fast_blocks[0][0].get_left() + LEFT * 0.08,
            thickness=2.8,
            max_tip_length_to_length_ratio=0.18,
            fill_color=INK_MID,
            buff=0,
        )
        in_slow = Arrow(
            [fork_x, slow_blocks[0][0].get_center()[1], 0],
            slow_blocks[0][0].get_left() + LEFT * 0.08,
            thickness=2.8,
            max_tip_length_to_length_ratio=0.18,
            fill_color=GOLD_RICH,
            buff=0,
        )
        input_fork = VGroup(fork_stem, fork_split, in_fast, in_slow)
        self.play(FadeIn(scene_in))
        self.play(
            ShowCreation(input_fork),
            FadeIn(fast_group),
            FadeIn(slow_group),
            ShowCreation(fast_container),
            ShowCreation(slow_container),
        )

        self.add(fast_loader, slow_loader)
        self.play(
            UpdateFromAlphaFunc(
                fast_loader,
                lambda m, a: _update_loader(
                    m, fast_container, a, loops=3.0, color=ACCENT_BLUE,
                ),
            ),
            UpdateFromAlphaFunc(
                slow_loader,
                lambda m, a: _update_loader(
                    m, slow_container, a, loops=1.0, color=GOLD_RICH,
                ),
            ),
            run_time=2.4,
            rate_func=linear,
        )

        merge_x = action[0].get_left()[0] - 0.58
        merge_y = action[0].get_center()[1]
        fast_y = fast_blocks[-1][0].get_center()[1]
        slow_y = slow_blocks[-1][0].get_center()[1]
        fast_out = Arrow(
            fast_blocks[-1][0].get_right() + RIGHT * 0.08,
            [merge_x, fast_y, 0],
            thickness=2.8,
            max_tip_length_to_length_ratio=0.12,
            fill_color=INK_MID,
            buff=0,
        )
        slow_out = Arrow(
            slow_blocks[-1][0].get_right() + RIGHT * 0.08,
            [merge_x, slow_y, 0],
            thickness=2.8,
            max_tip_length_to_length_ratio=0.12,
            fill_color=GOLD_RICH,
            buff=0,
        )
        merge_line = Line(
            [merge_x, slow_y, 0],
            [merge_x, fast_y, 0],
            stroke_color=GREEN_FIX,
            stroke_width=2.8,
        )
        merge_arrow = Arrow(
            [merge_x, merge_y, 0],
            action[0].get_left() + LEFT * 0.08,
            thickness=2.8,
            max_tip_length_to_length_ratio=0.18,
            fill_color=GREEN_FIX,
            buff=0,
        )
        output_merge = VGroup(fast_out, slow_out, merge_line, merge_arrow)
        self.play(
            ShowCreation(output_merge),
            FadeIn(action),
        )

        caption = Text(
            "Fast path for routine scenes  ·  Slow VLM when complexity rises",
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD,
        )
        place_footer(caption)
        self.play(FadeIn(caption))
        self.wait(2)
        self._close()
