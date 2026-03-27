"""
Scene 3-03 — UCLA Smart Intersection
======================================
Top-down UCLA intersection map → sensor table →
sensor failure illustration + PI/CAR mascot dialogue.
"""
from drivex.components.thought_bubble import PIBubble, SpeechBubble
from drivex.components.mascots import CarMascot, PiMascot, idle_bounce
from drivex.components.colors import *
from manim import *
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))


class P03S03SmartIntersection(Scene):
    """
    A: Intersection map with NW/SE infrastructure nodes and two CAVs.
    B: Sensor breakdown table.
    C: Sensor failure illustration + mascot dialogue.
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        # ═══ SECTION A: Intersection Map ══════════════════════════
        # Roads (two perpendicular rectangles)
        road_h = Rectangle(width=11, height=1.6,
                           fill_color="#3A3A3A", fill_opacity=1, stroke_width=0)
        road_v = Rectangle(width=1.6, height=8,
                           fill_color="#3A3A3A", fill_opacity=1, stroke_width=0)
        road_h.move_to(ORIGIN)
        road_v.move_to(ORIGIN)
        roads = VGroup(road_h, road_v)

        # lane markings
        lane_marks = VGroup(*[
            DashedLine(LEFT * 4.5 + direction, RIGHT * 4.5 + direction,
                       color=COL_WHITE, stroke_opacity=0.4,
                       dash_length=0.3, dashed_ratio=0.5)
            for direction in [UP * 0.0]
        ] + [
            DashedLine(LEFT * 0.0 + UP * 3 + h_off,
                       LEFT * 0.0 + DOWN * 3 + h_off,
                       color=COL_WHITE, stroke_opacity=0.4,
                       dash_length=0.3, dashed_ratio=0.5)
            for h_off in [ORIGIN]
        ])

        # Infrastructure nodes (diamond shapes)
        nw_node = Square(side_length=0.35, fill_color=COL_INFRA_ORANGE, fill_opacity=1,
                         stroke_width=0).rotate(PI / 4).move_to(LEFT * 2.8 + UP * 1.8)
        se_node = Square(side_length=0.35, fill_color=COL_INFRA_ORANGE, fill_opacity=1,
                         stroke_width=0).rotate(PI / 4).move_to(RIGHT * 2.8 + DOWN * 1.8)
        lbl_nw = Text("NW Node", font_size=12, color=COL_INFRA_ORANGE)
        lbl_nw.next_to(nw_node, UL, buff=0.12)
        lbl_se = Text("SE Node", font_size=12, color=COL_INFRA_ORANGE)
        lbl_se.next_to(se_node, DR, buff=0.12)

        # CAVs
        cav1 = Dot(radius=0.18, color=COL_BLUE).move_to(
            LEFT * 1.5 + DOWN * 0.2)
        cav2 = Dot(radius=0.18, color=COL_BLUE).move_to(RIGHT * 0.6 + UP * 0.3)

        loc_lbl = Text("Charles E. Young Dr & Westwood Plaza — UCLA Campus",
                       font_size=11, color=COL_WHITE, slant=ITALIC)
        loc_lbl.to_edge(DOWN, buff=0.6)

        live_badge = RoundedRectangle(width=3.5, height=0.5, corner_radius=0.1,
                                      fill_color=COL_RED,  fill_opacity=1, stroke_width=0)
        live_lbl = Text("LIVE INTERSECTION", font_size=12,
                        color=COL_WHITE, weight=BOLD)
        live_badge.to_corner(UR, buff=0.3)
        live_lbl.move_to(live_badge.get_center())

        map_group = VGroup(roads, lane_marks, nw_node,
                           se_node, lbl_nw, lbl_se, cav1, cav2)

        self.play(FadeIn(map_group), run_time=0.6)
        self.play(FadeIn(VGroup(live_badge, live_lbl)),
                  FadeIn(loc_lbl), run_time=0.3)
        self.wait(0.8)

        # ═══ SECTION B: Sensor Table ══════════════════════════════
        self.play(map_group.animate.scale(
            0.65).to_edge(LEFT, buff=0.4), run_time=0.4)

        inf_data = [
            "NW: 128-line LiDAR + 2 Cameras + Radar",
            "SE: 64-line LiDAR + 2 Cameras + C-V2X",
        ]
        cav_data = [
            "4× Stereo Cameras",
            "LiDAR RoboSense Ruby+ (128-line)",
            "GNSS + IMU",
        ]

        def make_col(header_txt, color, items):
            hdr = Text(header_txt, font_size=15, color=color, weight=BOLD)
            rows = VGroup(*[Text(item, font_size=13, color=COL_WHITE)
                          for item in items])
            rows.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            return VGroup(hdr, rows).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        col_inf = make_col("Infrastructure Nodes", COL_INFRA_ORANGE, inf_data)
        col_cav = make_col("Connected Vehicles",   COL_BLUE,          cav_data)
        table = VGroup(col_inf, col_cav).arrange(
            RIGHT, buff=1.0, aligned_edge=UP)
        table.move_to(RIGHT * 2.5)

        self.play(FadeIn(table), run_time=0.6)
        self.wait(0.8)

        # ═══ SECTION C: Sensor Failures ════════════════════════════
        self.play(FadeOut(VGroup(table, map_group, live_badge, live_lbl, loc_lbl)),
                  run_time=0.4)

        def sensor_block(icon_txt, fail_label, fail_color, x):
            s_icon = Text(icon_txt, font_size=36)
            s_name = Text(fail_label, font_size=13,
                          color=fail_color, slant=ITALIC)
            grp = VGroup(s_icon, s_name).arrange(DOWN, buff=0.15)
            grp.move_to([x, 0.5, 0])
            return grp

        cam = sensor_block(
            "📷", "Fails in backlight / darkness", COL_RED,  -4.0)
        lid = sensor_block("🔊", "Degrades in heavy rain",
                           COL_RED,  0.0)
        gps = sensor_block(
            "📡", "Lost accuracy between buildings", COL_RED,  4.0)

        self.play(FadeIn(cam), FadeIn(lid), FadeIn(gps), run_time=0.5)

        # PI mascot question
        pi = PiMascot(height=0.9).to_corner(DL, buff=0.5)
        car = CarMascot(height=1.0).to_corner(DR, buff=0.4)
        pi_bubble = PIBubble(
            pi,  "Why so many sensors?\nIsn't that overkill?", position=UR)
        car_bubble = SpeechBubble(car,
                                  "Redundancy = minimum\ncondition for reliability.", position=UL)

        self.play(FadeIn(pi), run_time=0.3)
        self.play(FadeIn(pi_bubble), run_time=0.3)
        self.wait(0.5)
        self.play(FadeOut(pi_bubble), run_time=0.2)
        self.play(FadeIn(car), run_time=0.3)
        self.play(FadeIn(car_bubble), run_time=0.3)

        tagline = Text("Redundancy = Reliability", font_size=22,
                       color=COL_GOLD, weight=BOLD)
        tagline.to_edge(UP, buff=0.8)
        self.play(Write(tagline), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
