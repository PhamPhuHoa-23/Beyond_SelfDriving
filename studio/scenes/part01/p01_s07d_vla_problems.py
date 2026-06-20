"""P01-S07d — VLA Systematic Problems: Infeasible Actions and Constant Latency."""
from manimlib import *
from studio.components import (
    StudioScene, GOLD_KEY, GOLD_RICH, ACCENT_BLUE, GREEN_FIX, RED_ERROR, INK_DARK, INK_MID,
    PASTEL_AMBER, PASTEL_BLUE, PASTEL_GREEN,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, h_arrow, contribution_badge, error_propagation_marker, place_footer,
)
from studio.reference.bev_grid import waypoint_polyline


def _card_container(title: str, content: Mobject, *, width: float, height: float, fill: str, stroke: str) -> VGroup:
    panel = RoundedRectangle(
        width=width, height=height, corner_radius=0.16,
        fill_color=fill, fill_opacity=1.0,
        stroke_color=stroke, stroke_width=2.5,
    )
    panel.set_z_index(0)
    content.move_to(panel.get_center() + DOWN * 0.18)
    content.set_z_index(1)
    
    title_mob = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL + 1, color=stroke, weight=BOLD)
    title_mob.move_to(panel.get_center() + UP * (height / 2 - 0.4))
    title_mob.set_z_index(2)
    
    return VGroup(panel, content, title_mob)


class P01S07DVLAProblems(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "VLA Systematic Limitations"

    def construct(self):
        self._open(self.SCENE_TITLE)

        # ── Left content: Feasibility Glitch ──────────────────────────────────
        left_content = VGroup()
        road = Rectangle(
            width=2.8, height=1.3, fill_color=GREY_D, fill_opacity=0.35,
            stroke_color=INK_DARK, stroke_width=1.5,
        )
        obstacle = Rectangle(
            width=0.48, height=0.48, fill_color=RED_ERROR, fill_opacity=0.9,
            stroke_color=INK_DARK, stroke_width=1.5,
        )
        obstacle.move_to(road.get_center() + RIGHT * 0.4 + UP * 0.15)
        
        points = [
            road.get_center() + LEFT * 1.1 + DOWN * 0.4,
            road.get_center() + LEFT * 0.4 + DOWN * 0.1,
            road.get_center() + RIGHT * 0.4 + UP * 0.15,
            road.get_center() + RIGHT * 1.1 + UP * 0.4,
        ]
        traj = waypoint_polyline(points=points, color=RED_ERROR, stroke_width=3.5)
        
        marker = error_propagation_marker(radius=0.14, label="Collision", label_side=DOWN)
        marker[0].move_to(obstacle.get_center())
        marker[1].next_to(obstacle, DOWN, buff=0.18)
        
        left_content.add(road, obstacle, traj, marker)

        # ── Right content: Latency Bottleneck ─────────────────────────────────
        right_content = VGroup()
        simple_scene = pipeline_block("Simple\nscene", width=1.3, height=0.6, fill=PASTEL_BLUE, stroke=ACCENT_BLUE)
        slow_cot = pipeline_block("Slow CoT\n(2 Hz)", width=1.3, height=0.6, fill=PASTEL_AMBER, stroke=GOLD_RICH)
        action_block = pipeline_block("Action", width=1.3, height=0.6, fill=PASTEL_GREEN, stroke=GREEN_FIX)
        
        flow = VGroup(simple_scene, slow_cot, action_block).arrange(RIGHT, buff=0.3)
        
        arrow1 = h_arrow(simple_scene, slow_cot, color=INK_MID)
        arrow2 = h_arrow(slow_cot, action_block, color=INK_MID)
        
        latency_badge = VGroup(
            RoundedRectangle(width=1.7, height=0.42, corner_radius=0.08, fill_color=RED_ERROR, fill_opacity=0.15, stroke_color=RED_ERROR, stroke_width=1.5),
            Text("Latency: ~500ms", font=FONT_PRIMARY, font_size=SIZE_CAPS - 2, color=RED_ERROR, weight=BOLD)
        )
        latency_badge[1].move_to(latency_badge[0].get_center())
        latency_badge.next_to(slow_cot, UP, buff=0.25)
        
        right_content.add(simple_scene, slow_cot, action_block, arrow1, arrow2, latency_badge)

        # ── Create the two Cards ──────────────────────────────────────────────
        left_card = _card_container(
            "1. Infeasible Actions", left_content,
            width=5.8, height=3.3, fill="#FDFEFE", stroke=RED_ERROR
        )
        right_card = _card_container(
            "2. Constant Latency", right_content,
            width=5.8, height=3.3, fill="#FDFEFE", stroke=GOLD_RICH
        )
        
        cards = VGroup(left_card, right_card).arrange(RIGHT, buff=0.6)
        cards.move_to(UP * 0.1)

        # ── Animation sequence ────────────────────────────────────────────────
        # Beat 1: Fade in Left Card (Feasibility Issue)
        self.play(FadeIn(left_card[0]), FadeIn(left_card[2])) # Panel and Title
        self.play(FadeIn(road), FadeIn(obstacle))
        self.play(
            ShowCreation(traj[0]),
            LaggedStart(*(FadeIn(d) for d in traj[1]), lag_ratio=0.12),
            run_time=0.9
        )
        self.play(GrowFromCenter(marker))
        self.wait(0.5)

        # Beat 2: Fade in Right Card (Latency Issue)
        self.play(FadeIn(right_card[0]), FadeIn(right_card[2])) # Panel and Title
        self.play(
            LaggedStart(
                FadeIn(simple_scene),
                ShowCreation(arrow1),
                FadeIn(slow_cot),
                ShowCreation(arrow2),
                FadeIn(action_block),
                lag_ratio=0.18
            ),
            run_time=1.2
        )
        self.play(GrowFromCenter(latency_badge))
        self.wait(0.8)

        # Beat 3: Bottom Solution Callout (AutoVLA UCLA)
        badge = contribution_badge("AutoVLA (UCLA) — Specifically designed to address both", color=GOLD_KEY)
        place_footer(badge)
        badge.shift(UP * 1.0)
        self.play(FadeIn(badge))
        self.wait(2.5)

        self._close()
