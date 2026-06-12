"""P01-S07a — BEVDriver: reveal shell then content (no full-then-replay)."""
from manimlib import *
from studio.components import (
    StudioScene,
    PASTEL_TEAL, PASTEL_BLUE, PASTEL_GREEN,
    ACCENT_TEAL, ACCENT_BLUE, GREEN_FIX, INK_DARK, CYAN_RADAR,
    FONT_PRIMARY, SIZE_LABEL, place_footer, pipeline_arrow,
)
from studio.reference.bev_grid import (
    lidar_point_cloud_side, bev_token_grid, waypoint_polyline, qformer_stack,
)


def _stage_shell(title: str, content: Mobject, *, fill, stroke, pad=0.22):
    content.set_z_index(1)
    w = content.get_width() + 2 * pad
    h = content.get_height() + 2 * pad
    panel = RoundedRectangle(
        width=w, height=h, corner_radius=0.16,
        fill_color=fill, fill_opacity=1.0,
        stroke_color=stroke, stroke_width=3.0,
    )
    panel.set_z_index(0)
    content.move_to(panel.get_center())
    title_mob = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=stroke, weight=BOLD)
    title_mob.next_to(panel, UP, buff=0.14)
    title_mob.set_z_index(2)
    return VGroup(panel, content, title_mob)


class P01S07ABEVDriver(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "BEVDriver"

    def construct(self):
        self._open(self.SCENE_TITLE)

        lidar = lidar_point_cloud_side(44, color="#0F766E", width=1.7, height=1.2)
        cam_strip = VGroup(*[
            Rectangle(width=1.1, height=0.06, fill_color=ACCENT_BLUE, fill_opacity=1, stroke_width=0)
            for _ in range(5)
        ])
        cam_strip.arrange(DOWN, buff=0.05)
        sensors = VGroup(lidar, cam_strip).arrange(DOWN, buff=0.18)

        bev = bev_token_grid(7, 7, cell_size=0.2, base_color=ACCENT_TEAL)
        llm_stack = qformer_stack(4, color=ACCENT_BLUE, width=1.35)
        llm_lbl = Text("LLM", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_BLUE, weight=BOLD)
        llm_inner = VGroup(llm_lbl, llm_stack).arrange(DOWN, buff=0.12)
        llm_lbl.set_x(llm_stack.get_center()[0])

        road = Rectangle(
            width=1.5, height=0.55, fill_color=GREY_D, fill_opacity=0.35,
            stroke_color=INK_DARK, stroke_width=1.5,
        )
        traj = waypoint_polyline(color=GREEN_FIX)
        traj.scale(0.7)
        traj.move_to(road.get_center() + UP * 0.05)
        wp_inner = VGroup(road, traj)

        # Hide all inner content until its beat
        sensors.set_opacity(0)
        bev[1].set_opacity(0)
        llm_inner.set_opacity(0)
        wp_inner.set_opacity(0)

        stages = [
            _stage_shell("Sensors", sensors, fill=PASTEL_TEAL, stroke=ACCENT_TEAL),
            _stage_shell("BEV map", bev, fill=PASTEL_TEAL, stroke=ACCENT_TEAL),
            _stage_shell("Q-Former + LLM", llm_inner, fill=PASTEL_BLUE, stroke=ACCENT_BLUE),
            _stage_shell("Waypoints", wp_inner, fill=PASTEL_GREEN, stroke=GREEN_FIX),
        ]
        strip = VGroup(*stages)
        strip.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        strip.move_to(ORIGIN + UP * 0.05)

        def _show_shell(idx):
            return FadeIn(stages[idx][0]), FadeIn(stages[idx][2])

        self.play(*_show_shell(0))
        self.play(sensors.animate.set_opacity(1), run_time=0.9)

        self.play(ShowCreation(pipeline_arrow(stages[0][0], stages[1][0])), *_show_shell(1))
        self.play(bev[1].animate.set_opacity(1), run_time=0.15)
        self.play(LaggedStart(*(GrowFromCenter(c) for c in bev[1]), lag_ratio=0.03, run_time=0.95))

        self.play(ShowCreation(pipeline_arrow(stages[1][0], stages[2][0])), *_show_shell(2))
        self.play(llm_inner.animate.set_opacity(1), run_time=0.15)
        self.play(LaggedStart(*(FadeIn(b) for b in llm_stack), lag_ratio=0.1), FadeIn(llm_lbl))

        self.play(ShowCreation(pipeline_arrow(stages[2][0], stages[3][0])), *_show_shell(3))
        self.play(wp_inner.animate.set_opacity(1), run_time=0.15)
        self.play(FadeIn(road), ShowCreation(traj[0]),
                  LaggedStart(*(FadeIn(d) for d in traj[1]), lag_ratio=0.12))

        key = Text(
            "3D sensors  \u2192  BEV  \u2192  language model  \u2192  trajectory",
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD,
        )
        place_footer(key)
        self.play(FadeIn(key))
        self.wait(2)
        self._close()
