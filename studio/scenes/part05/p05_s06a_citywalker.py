"""P05-S06a CityWalker: pedestrian behavior in urban context."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene,
    BG_PAPER,
    BG_CARD,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_AMBER,
    PASTEL_PINK,
    ACCENT_BLUE,
    ACCENT_TEAL,
    ACCENT_GREEN,
    ACCENT_AMBER,
    ACCENT_PINK,
    GOLD_RICH,
    RED_ERROR,
    PURPLE_MODEL,
    CYAN_RADAR,
    GOLD_KEY,
    INK_DARK,
    INK_MID,
    INK_LIGHT,
    LINE_GRID,
    FONT_PRIMARY,
    SIZE_LABEL,
    SIZE_CAPS,
    SIZE_MICRO,
    pedestrian_icon,
    vehicle_icon,
)

SCRIPT = """CityWalker captures real pedestrian behavior in context: 30.8 hours, 120,914 pedestrians, 16,215 scenes, and 227 cities."""


def stroller_prop(color):
    w1 = Circle(radius=0.06, fill_color=color, stroke_color=INK_DARK, stroke_width=0.8, fill_opacity=1.0)
    w2 = Circle(radius=0.06, fill_color=color, stroke_color=INK_DARK, stroke_width=0.8, fill_opacity=1.0)
    w1.shift(LEFT * 0.12)
    w2.shift(RIGHT * 0.12)
    frame = Line(LEFT * 0.12, RIGHT * 0.12, stroke_color=INK_DARK, stroke_width=1.5)
    frame.shift(UP * 0.06)
    handle = Line(RIGHT * 0.08, UP * 0.32 + LEFT * 0.12, stroke_color=INK_DARK, stroke_width=1.5)
    basket = RoundedRectangle(width=0.25, height=0.15, corner_radius=0.03, fill_color=color, fill_opacity=0.75, stroke_color=INK_DARK, stroke_width=1.0)
    basket.shift(UP * 0.14)
    stroller = VGroup(w1, w2, frame, handle, basket)
    return stroller


def phone_prop():
    phone = Rectangle(width=0.04, height=0.08, fill_color=CYAN_RADAR, stroke_color=INK_DARK, stroke_width=0.6, fill_opacity=1.0)
    phone.rotate(15 * DEGREES)
    return phone


def camera_prop(color):
    body = RoundedRectangle(width=0.2, height=0.12, corner_radius=0.02, fill_color=color, fill_opacity=1.0, stroke_color=INK_DARK, stroke_width=0.8)
    lens = Circle(radius=0.045, fill_color=WHITE, stroke_color=INK_DARK, stroke_width=0.8, fill_opacity=1.0)
    lens.move_to(body)
    flash = Rectangle(width=0.04, height=0.03, fill_color=GOLD_KEY, stroke_width=0, fill_opacity=1.0)
    flash.next_to(body, UR, buff=-0.03)
    camera = VGroup(body, lens, flash)
    return camera


def speech_prop():
    bubble = RoundedRectangle(width=0.28, height=0.18, corner_radius=0.05, fill_color=WHITE, fill_opacity=0.95, stroke_color=INK_MID, stroke_width=0.8)
    tail = Polygon([0, 0, 0], [-0.06, -0.06, 0], [0.06, 0, 0], fill_color=WHITE, stroke_color=INK_MID, stroke_width=0.8, fill_opacity=1.0)
    tail.next_to(bubble, DOWN, buff=-0.02).shift(LEFT * 0.05)
    dots = VGroup(*(Dot(radius=0.02, color=INK_MID) for _ in range(3))).arrange(RIGHT, buff=0.03)
    dots.move_to(bubble)
    speech = VGroup(bubble, tail, dots)
    return speech


def warning_triangle_prop():
    triangle = Polygon(
        [-0.18, -0.13, 0], [0.18, -0.13, 0], [0, 0.18, 0],
        fill_color=RED_ERROR, fill_opacity=0.95,
        stroke_color=INK_DARK, stroke_width=1.0
    )
    excl = Text("!", font=FONT_PRIMARY, font_size=12, color=WHITE, weight=BOLD)
    excl.move_to(triangle.get_center() + DOWN * 0.02)
    return VGroup(triangle, excl)


def photo_stop_rate(x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    if x <= 0.375:
        return 0.5 * smooth(x / 0.375)
    elif x <= 0.625:
        return 0.5
    else:
        return 0.5 + 0.5 * smooth((x - 0.625) / 0.375)


class P05S06ACityWalker(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "CityWalker Dataset"

    def city_view(self):
        panel = RoundedRectangle(
            width=7.2,
            height=4.15,
            corner_radius=0.14,
            fill_color="#F4F7EF",
            fill_opacity=1,
            stroke_color=ACCENT_TEAL,
            stroke_width=1.6,
        )
        road = Rectangle(width=6.75, height=1.18, fill_color="#D9E2E7", fill_opacity=1, stroke_width=0)
        road.move_to(panel.get_center() + DOWN * 0.55)
        sidewalk_top = Rectangle(width=6.75, height=0.92, fill_color="#EAF4DF", fill_opacity=1, stroke_width=0)
        sidewalk_top.next_to(road, UP, buff=0)
        sidewalk_bot = Rectangle(width=6.75, height=0.88, fill_color="#F8EBC8", fill_opacity=1, stroke_width=0)
        sidewalk_bot.next_to(road, DOWN, buff=0)

        crosswalk = VGroup()
        for i in range(6):
            stripe = Rectangle(width=0.08, height=1.1, fill_color=WHITE, fill_opacity=0.7, stroke_width=0)
            stripe.move_to(road.get_center() + LEFT * 0.35 + RIGHT * i * 0.16)
            crosswalk.add(stripe)

        blocks = VGroup()
        for x, y, w, h, color in [
            (-2.65, 1.13, 1.0, 0.38, PASTEL_BLUE),
            (-1.25, 1.16, 0.78, 0.35, PASTEL_AMBER),
            (1.85, 1.14, 1.05, 0.38, PASTEL_GREEN),
            (2.95, -1.73, 0.82, 0.36, PASTEL_BLUE),
            (-2.85, -1.78, 1.15, 0.32, PASTEL_GREEN),
        ]:
            b = RoundedRectangle(
                width=w,
                height=h,
                corner_radius=0.06,
                fill_color=color,
                fill_opacity=0.55,
                stroke_color=interpolate_color(color, INK_MID, 0.2),
                stroke_width=1.0,
            )
            b.move_to(panel.get_center() + RIGHT * x + UP * y)
            blocks.add(b)

        car = vehicle_icon(color=ACCENT_BLUE, scale=0.26)
        car.move_to(road.get_center() + LEFT * 2.25 + DOWN * 0.18)

        env = VGroup(road, sidewalk_top, sidewalk_bot, crosswalk, blocks, car)
        return panel, env, car

    def metric_card(self, label, color, motif, suffix="", is_integer=False):
        card = RoundedRectangle(
            width=1.85,
            height=0.86,
            corner_radius=0.09,
            fill_color=interpolate_color(color, WHITE, 0.83),
            fill_opacity=0.95,
            stroke_color=color,
            stroke_width=1.4,
        )
        
        motif.move_to(card.get_corner(UR) + DOWN * 0.18 + LEFT * 0.18)
        
        lbl = Text(label, font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_DARK)
        lbl.move_to(card.get_center() + DOWN * 0.22)
        
        tracker = ValueTracker(0)
        val_mob = Text("0" + suffix, font=FONT_PRIMARY, font_size=28, color=color)
        val_mob.move_to(card.get_center() + UP * 0.1)
        
        def update_val(m):
            val = tracker.get_value()
            if is_integer:
                txt = f"{int(val):,}"
            else:
                txt = f"{val:.1f}"
            new_m = Text(txt + suffix, font=FONT_PRIMARY, font_size=28, color=color)
            new_m.set_color(color)
            new_m.set_fill(color, opacity=1.0)
            new_m.set_stroke(color, width=0)
            new_m.move_to(card.get_center() + UP * 0.1)
            if hasattr(self, "_force_text_contrast"):
                self._force_text_contrast(new_m)
            m.become(new_m)
            
        val_mob.add_updater(update_val)
        
        card_group = VGroup(card, val_mob, lbl, motif)
        return card_group, tracker

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # Initially centered panel coordinate
        panel_center = DOWN * 0.05

        # ----------------------------------------------------
        # Beat 0: Pivot from Sim to Human (0.0s - 1.5s)
        # ----------------------------------------------------
        sim_token = RoundedRectangle(
            width=2.8, height=1.0, corner_radius=0.1,
            fill_color=PASTEL_GREEN, fill_opacity=0.9,
            stroke_color=ACCENT_GREEN, stroke_width=1.5
        )
        sim_label = Text("simulation solved", font=FONT_PRIMARY, font_size=18, color=INK_DARK)
        check_mark = Text("✓", font=FONT_PRIMARY, font_size=20, color=ACCENT_GREEN, weight=BOLD)
        VGroup(sim_label, check_mark).arrange(RIGHT, buff=0.15).move_to(sim_token.get_center())
        sim_group = VGroup(sim_token, sim_label, check_mark)
        sim_group.move_to(ORIGIN + DOWN * 0.3)

        self.add(sim_group)
        self.wait(0.5)

        human_icon = pedestrian_icon(color=ACCENT_PINK).scale(0.8)
        question_mark = Text("?", font=FONT_PRIMARY, font_size=42, color=ACCENT_PINK, weight=BOLD)
        question_mark.next_to(human_icon, UP, buff=0.2)
        human_problem = VGroup(human_icon, question_mark)
        human_problem.move_to(RIGHT * 8 + DOWN * 0.3)

        self.play(
            FadeOut(sim_group, shift=LEFT * 1.5),
            human_problem.animate.move_to(ORIGIN + DOWN * 0.3),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(0.2)

        # ----------------------------------------------------
        # Beat 1: The problem: isolated mocap (1.5s - 7.1s)
        # ----------------------------------------------------
        panel = RoundedRectangle(
            width=7.2,
            height=4.15,
            corner_radius=0.14,
            fill_color="#1E293B",
            fill_opacity=1,
            stroke_color=INK_LIGHT,
            stroke_width=1.6
        )
        panel.move_to(panel_center)

        grid = VGroup()
        for x in np.linspace(-3.3, 3.3, 9):
            grid.add(Line(panel_center + np.array([x, -1.9, 0]), panel_center + np.array([x, 1.9, 0]), stroke_color=INK_LIGHT, stroke_opacity=0.15, stroke_width=0.8))
        for y in np.linspace(-1.8, 1.8, 7):
            grid.add(Line(panel_center + np.array([-3.3, y, 0]), panel_center + np.array([3.3, y, 0]), stroke_color=INK_LIGHT, stroke_opacity=0.15, stroke_width=0.8))

        # P4: Mocap Studio Cues
        rec_text = Text("REC", font=FONT_PRIMARY, font_size=14, weight=BOLD)
        rec_text.set_color(RED_ERROR)
        mocap_rec = VGroup(
            Circle(radius=0.08, fill_color=RED_ERROR, fill_opacity=1.0, stroke_width=0),
            rec_text
        ).arrange(RIGHT, buff=0.1)
        mocap_rec.move_to(panel.get_corner(UL) + RIGHT * 0.6 + DOWN * 0.3)

        mocap_cams = VGroup()
        for corner in [UL, UR, DL, DR]:
            cam = Circle(radius=0.06, fill_color=INK_LIGHT, fill_opacity=0.8, stroke_color=INK_DARK, stroke_width=0.8)
            offset = (DR if np.array_equal(corner, UL) else DL if np.array_equal(corner, UR) else UR if np.array_equal(corner, DL) else UL) * 0.25
            cam.move_to(panel.get_corner(corner) + offset)
            mocap_cams.add(cam)

        mocap_ped = pedestrian_icon(color=WHITE).scale(0.46)
        markers = VGroup()
        for offset in [UP*0.35, UP*0.12 + LEFT*0.13, UP*0.12 + RIGHT*0.13, DOWN*0.18 + LEFT*0.1, DOWN*0.18 + RIGHT*0.1]:
            markers.add(Dot(radius=0.032, color=GOLD_KEY).move_to(mocap_ped.get_center() + offset))
        mocap_character = VGroup(mocap_ped, markers)

        # M2: Path update for parked car collision
        mocap_start = panel_center + LEFT * 2.8 + DOWN * 1.0
        mocap_end = panel_center + RIGHT * 2.6 + UP * 1.4
        mocap_character.move_to(mocap_start)

        blind_trace = TracedPath(
            mocap_character.get_center,
            stroke_color=RED_ERROR,
            stroke_width=2.5,
            stroke_opacity=0.8,
            time_traced=10
        )

        self.play(
            FadeOut(human_problem, shift=UP*0.2),
            FadeIn(panel),
            FadeIn(grid),
            FadeIn(mocap_rec),
            FadeIn(mocap_cams),
            FadeIn(mocap_character),
            run_time=0.6
        )
        self.add(blind_trace)

        u_vals = [0, 0.10, 0.30, 0.35, 0.50, 0.86, 1.0]
        path_pts = [mocap_start + u * (mocap_end - mocap_start) for u in u_vals]

        # Walk to parked car collision
        self.play(
            MoveAlongPath(mocap_character, Line(path_pts[0], path_pts[1])),
            run_time=0.4,
            rate_func=linear
        )

        # M2: Parked car collision warning (Warning 1)
        warn1 = warning_triangle_prop().move_to(path_pts[1] + UP * 0.4 + LEFT * 0.2)
        flash1 = Circle(radius=0.05, color=RED_ERROR, stroke_width=2.0).move_to(path_pts[1])
        self.add(warn1, flash1)
        self.play(flash1.animate.scale(4.0).set_stroke(opacity=0), run_time=0.3)
        self.remove(flash1)

        # Walk on empty stage
        self.play(
            MoveAlongPath(mocap_character, Line(path_pts[1], path_pts[2])),
            run_time=0.8,
            rate_func=linear
        )

        # Environment fades in
        _, env_group, car = self.city_view()
        env_group.move_to(panel_center)

        self.play(
            MoveAlongPath(mocap_character, Line(path_pts[2], path_pts[3])),
            panel.animate.set_fill(color="#F4F7EF", opacity=1.0).set_stroke(color=ACCENT_TEAL),
            FadeIn(env_group),
            FadeOut(grid),
            FadeOut(mocap_rec),
            FadeOut(mocap_cams),
            run_time=0.6,
            rate_func=linear
        )

        # Walk into road (jaywalk violation)
        self.play(
            MoveAlongPath(mocap_character, Line(path_pts[3], path_pts[4])),
            run_time=0.6,
            rate_func=linear
        )
        # Warning 2: jaywalk
        warn2 = warning_triangle_prop().move_to(path_pts[4] + DOWN * 0.5)
        flash2 = Circle(radius=0.05, color=RED_ERROR, stroke_width=2.0).move_to(path_pts[4])
        self.add(warn2, flash2)
        self.play(flash2.animate.scale(4.0).set_stroke(opacity=0), run_time=0.3)
        self.remove(flash2)

        # Walk to Block 3 collision
        self.play(
            MoveAlongPath(mocap_character, Line(path_pts[4], path_pts[5])),
            run_time=1.44,
            rate_func=linear
        )
        # Warning 3: block collision
        warn3 = warning_triangle_prop().move_to(path_pts[5] + UP * 0.4 + RIGHT * 0.2)
        flash3 = Circle(radius=0.05, color=RED_ERROR, stroke_width=2.0).move_to(path_pts[5])
        self.add(warn3, flash3)
        self.play(flash3.animate.scale(4.0).set_stroke(opacity=0), run_time=0.3)
        self.remove(flash3)

        # Walk to end of panel
        self.play(
            MoveAlongPath(mocap_character, Line(path_pts[5], path_pts[6])),
            run_time=0.56,
            rate_func=linear
        )

        # ----------------------------------------------------
        # Beat 2: CityWalker Reveal (7.1s - 8.6s)
        # ----------------------------------------------------
        self.play(
            FadeOut(mocap_character),
            FadeOut(blind_trace),
            FadeOut(warn1),
            FadeOut(warn2),
            FadeOut(warn3),
            run_time=0.5
        )

        paths = VGroup()
        data = [
            ([-2.7, -1.7, 0], [-1.55, -0.6, 0], [-0.25, 0.38, 0], [0.55, 1.18, 0], ACCENT_PINK),
            ([2.8, 1.28, 0], [1.42, 0.62, 0], [0.65, -0.45, 0], [-0.7, -1.38, 0], ACCENT_GREEN),
            ([-0.1, 1.38, 0], [0.38, 0.86, 0], [0.18, 0.08, 0], [1.55, -1.55, 0], ACCENT_AMBER),
            ([-3.0, 0.9, 0], [-1.9, 0.78, 0], [-0.9, 0.64, 0], [0.05, 0.44, 0], ACCENT_TEAL),
        ]
        for start, c1, c2, end, color in data:
            curve = CubicBezier(
                panel_center + np.array(start),
                panel_center + np.array(c1),
                panel_center + np.array(c2),
                panel_center + np.array(end),
                stroke_color=color,
                stroke_width=3.0,
                stroke_opacity=0.85,
            )
            paths.add(curve)

        ped1_base = pedestrian_icon(color=ACCENT_PINK).scale(0.46)
        stroller = stroller_prop(ACCENT_PINK)
        stroller.next_to(ped1_base, RIGHT * 0.4 + UP * 0.15, buff=0)
        ped1 = VGroup(ped1_base, stroller)

        ped2_base = pedestrian_icon(color=ACCENT_GREEN).scale(0.46)
        ped2_base.rotate(-15 * DEGREES)
        phone = phone_prop()
        phone.next_to(ped2_base, LEFT * 0.15 + DOWN * 0.08, buff=0)
        ped2 = VGroup(ped2_base, phone)

        ped3 = pedestrian_icon(color=ACCENT_AMBER).scale(0.46)

        ped4_base = pedestrian_icon(color=ACCENT_TEAL).scale(0.46)
        ped4_comp = pedestrian_icon(color=ACCENT_TEAL).scale(0.46)
        ped4_comp.shift(DOWN * 0.25 + RIGHT * 0.1)
        ped4 = VGroup(ped4_base, ped4_comp)

        ped1.move_to(paths[0].get_start())
        ped2.move_to(paths[1].get_start())
        ped3.move_to(paths[2].get_start())
        ped4.move_to(paths[3].get_start())

        trails = VGroup()
        for ped, color in zip([ped1, ped2, ped3, ped4], [ACCENT_PINK, ACCENT_GREEN, ACCENT_AMBER, ACCENT_TEAL]):
            def get_ped_center(p=ped):
                if isinstance(p, VGroup):
                    return p[0].get_center()
                return p.get_center()
            trail = TracedPath(
                get_ped_center,
                stroke_color=color,
                stroke_width=3.0,
                stroke_opacity=0.82,
                time_traced=10,
            )
            trails.add(trail)

        caption = Text("real pedestrian trajectories in context", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        caption.next_to(panel, UP, buff=0.14)

        # M1: Sync context peds reveal with context caption write-in
        self.play(
            Write(caption),
            FadeIn(ped1), FadeIn(ped2), FadeIn(ped3), FadeIn(ped4),
            run_time=0.8
        )
        self.add(trails)
        self.wait(0.2)

        # ----------------------------------------------------
        # Beat 3: Diversity of Behaviors (8.6s - 13.0s)
        # ----------------------------------------------------
        time_tracker = ValueTracker(0)
        ped1.add_updater(lambda m: m.move_to(paths[0].point_from_proportion(smooth(time_tracker.get_value() / 4.0))))
        ped2.add_updater(lambda m: m.move_to(paths[1].point_from_proportion(smooth(time_tracker.get_value() / 4.0))))
        ped3.add_updater(lambda m: m.move_to(paths[2].point_from_proportion(photo_stop_rate(time_tracker.get_value() / 4.0))))
        ped4.add_updater(lambda m: m.move_to(paths[3].point_from_proportion(smooth(time_tracker.get_value() / 4.0))))

        tag1 = Text("stroller", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_PINK, weight=BOLD)
        tag2 = Text("phone", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_GREEN, weight=BOLD)
        tag3 = Text("photo stop", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_AMBER, weight=BOLD)
        tag4 = Text("gesture", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=ACCENT_TEAL, weight=BOLD)

        tag1.move_to(panel_center + LEFT * 2.05 + DOWN * 1.83)
        tag2.move_to(panel_center + RIGHT * 1.85 + DOWN * 0.85)
        tag3.move_to(panel_center + LEFT * 0.28 + UP * 1.38)
        tag4.move_to(panel_center + LEFT * 2.3 + UP * 0.45)

        camera = camera_prop(ACCENT_AMBER)
        camera.add_updater(lambda m: m.next_to(ped3, UP * 0.15 + RIGHT * 0.1))

        flash_circle = Circle(radius=0.05, color=GOLD_KEY, fill_color=GOLD_KEY, fill_opacity=0.8, stroke_width=0)
        flash_circle.add_updater(lambda m: m.move_to(camera[2].get_center()))

        speech = speech_prop()
        speech.add_updater(lambda m: m.next_to(ped4[0], UP * 0.15))

        self.play(time_tracker.animate.set_value(0.5), run_time=0.5, rate_func=linear)
        self.play(time_tracker.animate.set_value(1.1), FadeIn(tag1, shift=UP*0.1), run_time=0.6, rate_func=linear)
        self.play(time_tracker.animate.set_value(1.6), FadeIn(tag2, shift=UP*0.1), run_time=0.5, rate_func=linear)
        
        self.add(camera, flash_circle)
        self.play(
            time_tracker.animate.set_value(2.0),
            FadeIn(tag3, shift=UP*0.1),
            flash_circle.animate.scale(5.0).set_opacity(0),
            run_time=0.4,
            rate_func=linear
        )
        self.remove(flash_circle)
        
        self.play(time_tracker.animate.set_value(2.2), run_time=0.2, rate_func=linear)
        
        self.play(
            time_tracker.animate.set_value(2.6),
            FadeIn(tag4, shift=UP*0.1),
            FadeIn(speech),
            run_time=0.4,
            rate_func=linear
        )
        self.play(time_tracker.animate.set_value(3.2), FadeOut(camera), run_time=0.6, rate_func=linear)
        self.play(time_tracker.animate.set_value(4.0), FadeOut(speech), run_time=0.8, rate_func=linear)

        ped1.clear_updaters()
        ped2.clear_updaters()
        ped3.clear_updaters()
        ped4.clear_updaters()
        for trail in trails:
            trail.clear_updaters()

        # ----------------------------------------------------
        # Beat 4: Metrics slide-in & count up (13.0s - 16.5s)
        # ----------------------------------------------------
        play_circle = Circle(radius=0.1, fill_color=GOLD_RICH, fill_opacity=0.2, stroke_color=GOLD_RICH, stroke_width=0.8)
        play_tri = Polygon([0.04, 0, 0], [-0.02, 0.04, 0], [-0.02, -0.04, 0], fill_color=GOLD_RICH, stroke_width=0, fill_opacity=1.0)
        play_tri.move_to(play_circle)
        play_motif = VGroup(play_circle, play_tri)

        dots_motif = VGroup(*(Circle(radius=0.018, fill_color=ACCENT_PINK, stroke_width=0) for _ in range(5)))
        dots_motif.arrange_in_grid(2, 3, buff=0.04)

        scenes_motif = RoundedRectangle(width=0.2, height=0.14, corner_radius=0.02, fill_color=ACCENT_GREEN, fill_opacity=0.2, stroke_color=ACCENT_GREEN, stroke_width=0.8)

        globe_circle = Circle(radius=0.11, fill_color=ACCENT_TEAL, fill_opacity=0.2, stroke_color=ACCENT_TEAL, stroke_width=0.8)
        globe_grid = VGroup(
            Line([-0.11, 0, 0], [0.11, 0, 0], stroke_color=ACCENT_TEAL, stroke_opacity=0.3, stroke_width=0.6),
            Line([0, -0.11, 0], [0, 0.11, 0], stroke_color=ACCENT_TEAL, stroke_opacity=0.3, stroke_width=0.6),
        )
        globe_grid.move_to(globe_circle)
        globe_dots = VGroup(*(Dot(radius=0.014, color=GOLD_KEY) for _ in range(4)))
        for dot, pos in zip(globe_dots, [[-0.04, 0.03, 0], [0.05, 0.04, 0], [-0.02, -0.04, 0], [0.03, -0.05, 0]]):
            dot.move_to(globe_circle.get_center() + np.array(pos))
        globe_motif = VGroup(globe_circle, globe_grid, globe_dots)

        card1, t1 = self.metric_card("video", GOLD_RICH, play_motif, suffix="h", is_integer=False)
        card2, t2 = self.metric_card("pedestrians", ACCENT_PINK, dots_motif, is_integer=True)
        card3, t3 = self.metric_card("scenes", ACCENT_GREEN, scenes_motif, is_integer=True)
        card4, t4 = self.metric_card("cities", ACCENT_TEAL, globe_motif, is_integer=True)

        metrics = VGroup(card1, card2, card3, card4).arrange(DOWN, buff=0.18)
        metrics.move_to(RIGHT * 4.3 + DOWN * 0.05)

        # P2: Smooth shift of the panel/pedestrians/trails to the left
        all_left_elements = VGroup(panel, env_group, caption, tag1, tag2, tag3, tag4, ped1, ped2, ped3, ped4, trails)

        self.play(
            all_left_elements.animate.shift(LEFT * 2.25),
            LaggedStart(*(
                FadeIn(card_group, shift=LEFT * 0.5)
                for card_group in [card1, card2, card3, card4]
            ), lag_ratio=0.15),
            run_time=1.0,
            rate_func=smooth
        )

        self.play(
            t1.animate.set_value(30.8),
            t2.animate.set_value(120914),
            t3.animate.set_value(16215),
            t4.animate.set_value(227),
            run_time=2.2,
            rate_func=smooth
        )
        self.wait(0.5)

        for card_group in [card1, card2, card3, card4]:
            card_group[1].clear_updaters()

        # ----------------------------------------------------
        # Beat 5: Bridge to PedGen (16.5s - 20.0s)
        # ----------------------------------------------------
        all_right_elements = VGroup(card1, card2, card3, card4)
        
        # P1: Center target slightly above y = 0
        collapse_target = LEFT * 1.8 + UP * 0.2

        self.play(
            all_left_elements.animate.scale(0.01).move_to(collapse_target).set_opacity(0),
            all_right_elements.animate.scale(0.01).move_to(collapse_target).set_opacity(0),
            run_time=0.8,
            rate_func=smooth
        )

        training_token = RoundedRectangle(
            width=2.2, height=0.6, corner_radius=0.1,
            fill_color=PASTEL_PINK, fill_opacity=0.9,
            stroke_color=ACCENT_PINK, stroke_width=1.5
        )
        training_label = Text("training signal", font=FONT_PRIMARY, font_size=15, color=INK_DARK, weight=BOLD)
        training_label.move_to(training_token.get_center())
        training_group = VGroup(training_token, training_label)
        training_group.move_to(collapse_target)

        model_box = RoundedRectangle(
            width=2.2, height=1.0, corner_radius=0.12,
            fill_color=interpolate_color(PURPLE_MODEL, WHITE, 0.8), fill_opacity=0.9,
            stroke_color=PURPLE_MODEL, stroke_width=2.0
        )
        model_label = Text("PedGen", font=FONT_PRIMARY, font_size=20, color=INK_DARK, weight=BOLD)
        model_sub = Text("Behavior Model", font=FONT_PRIMARY, font_size=SIZE_MICRO, color=INK_LIGHT)
        VGroup(model_label, model_sub).arrange(DOWN, buff=0.05).move_to(model_box)
        model_group = VGroup(model_box, model_label, model_sub)
        model_group.move_to(RIGHT * 1.8 + UP * 0.2)

        arrow = Arrow(
            training_group.get_right() + RIGHT * 0.1,
            model_group.get_left() + LEFT * 0.1,
            fill_color=ACCENT_PINK,
            thickness=2.5,
            buff=0
        )

        self.play(
            FadeIn(training_group, scale=0.5),
            run_time=0.4
        )
        self.play(
            ShowCreation(arrow),
            FadeIn(model_group, shift=LEFT * 0.3),
            run_time=0.6
        )
        self.wait(2.0)

        self._close()
