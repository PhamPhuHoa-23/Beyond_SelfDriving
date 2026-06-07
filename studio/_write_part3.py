"""Script to write all Part 3 scene files."""
import os

BASE = "studio/scenes/part03"
os.makedirs(BASE, exist_ok=True)


def W(name, code):
    path = os.path.join(BASE, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"wrote {name}")


W("p03_s02_sim_real_gap.py", '''"""P03-S02 Sim-to-Real Gap."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_TEAL, ACCENT_AMBER, RED_ERROR, INK_DARK,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL, SIZE_BODY,
)
SCRIPT = """Two worlds. Clean simulation on the left, messy reality on the right."""


class P03S02SimRealGap(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Sim-to-Real Gap"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        divider = Line(UP * 3.2, DOWN * 3.2, stroke_color=RED_ERROR, stroke_width=3)
        self.play(ShowCreation(divider, run_time=0.8))
        sim_lbl = Text("Simulation", font=FONT_PRIMARY, font_size=SIZE_H1, color=ACCENT_TEAL, weight=BOLD)
        real_lbl = Text("Reality", font=FONT_PRIMARY, font_size=SIZE_H1, color=ACCENT_AMBER, weight=BOLD)
        sim_lbl.move_to(LEFT * 3.0 + UP * 1.5)
        real_lbl.move_to(RIGHT * 3.0 + UP * 1.5)
        self.play(FadeIn(sim_lbl, shift=RIGHT * 0.3), FadeIn(real_lbl, shift=LEFT * 0.3))
        sim_road = Rectangle(width=5.5, height=0.6, fill_color="#E2E8F0", fill_opacity=0.5, stroke_width=0)
        sim_road.move_to(LEFT * 3.3 + DOWN * 0.5)
        real_road = Rectangle(width=5.5, height=0.6, fill_color="#374151", fill_opacity=0.25, stroke_width=0)
        real_road.move_to(RIGHT * 3.3 + DOWN * 0.5)
        sim_car = Rectangle(width=0.7, height=0.35, fill_color=ACCENT_TEAL, fill_opacity=0.9, stroke_width=0)
        sim_car.move_to(LEFT * 3 + DOWN * 0.5)
        real_car = Rectangle(width=0.7, height=0.35, fill_color=ACCENT_AMBER, fill_opacity=0.8,
                              stroke_color=RED_ERROR, stroke_width=1.5)
        real_car.move_to(RIGHT * 3 + DOWN * 0.5)
        self.play(FadeIn(sim_road), FadeIn(real_road))
        self.play(GrowFromCenter(sim_car), GrowFromCenter(real_car))
        gap_lbl = Text("Sim-to-Real Gap", font=FONT_PRIMARY, font_size=SIZE_H1, color=RED_ERROR, weight=BOLD)
        gap_lbl.move_to(DOWN * 2.2)
        self.play(FadeIn(gap_lbl, scale=1.1))
        self.wait(2)
        self._close()
''')

W("p03_s03_smart_intersection.py", '''"""P03-S03 UCLA Smart Intersection."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ORANGE_INFRA, CYAN_RADAR, ACCENT_AMBER, ACCENT_BLUE,
    INK_DARK, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    rsu_icon, vehicle_icon, sensor_cone, radar_shells_2d, v2x_link,
)
SCRIPT = """This is a working intersection at UCLA — sensors lit up at once."""


class P03S03SmartIntersection(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "UCLA Smart Intersection"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        road_h = Rectangle(width=12, height=1.0, fill_color="#E2E8F0", fill_opacity=0.5, stroke_width=0)
        road_v = Rectangle(width=1.0, height=7, fill_color="#E2E8F0", fill_opacity=0.5, stroke_width=0)
        self.play(FadeIn(road_h), FadeIn(road_v))
        rsu_nw = rsu_icon(color=ORANGE_INFRA).scale(1.3).move_to(LEFT * 3 + UP * 1.8)
        rsu_se = rsu_icon(color=ORANGE_INFRA).scale(1.3).move_to(RIGHT * 3 + DOWN * 1.8)
        self.play(LaggedStart(GrowFromCenter(rsu_nw), GrowFromCenter(rsu_se), lag_ratio=0.2))
        self.play(
            Flash(rsu_nw, color=ORANGE_INFRA, line_length=0.25, num_lines=8),
            Flash(rsu_se, color=ORANGE_INFRA, line_length=0.25, num_lines=8),
        )
        car1 = vehicle_icon(color=ACCENT_BLUE, scale=0.9).move_to(LEFT * 1.5 + DOWN * 0.2)
        car2 = vehicle_icon(color=ACCENT_BLUE, scale=0.9).move_to(RIGHT * 2.0 + UP * 0.2)
        self.play(FadeIn(car1), FadeIn(car2))
        cone_nw = sensor_cone(rsu_nw.get_center(), color=ACCENT_AMBER, spread=PI / 3, length=2.5)
        cone_se = sensor_cone(rsu_se.get_center(), color=ACCENT_AMBER, spread=PI / 3, length=2.5)
        shells_nw, anim_nw = radar_shells_2d(rsu_nw.get_center(), color=CYAN_RADAR, n_shells=3, max_radius=2.0)
        shells_se, anim_se = radar_shells_2d(rsu_se.get_center(), color=CYAN_RADAR, n_shells=3, max_radius=2.0)
        lnk, lnk_flash = v2x_link(rsu_nw, rsu_se, color=CYAN_RADAR)
        self.play(FadeIn(cone_nw), FadeIn(cone_se), anim_nw, anim_se, ShowCreation(lnk))
        caption = Text(
            "2 RSU  ·  2 CAV  ·  LiDAR  ·  Camera  ·  Radar  ·  C-V2X",
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK,
        )
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption))
        self.wait(2)
        self._close()
''')

W("p03_s04a_time_calibration.py", '''"""P03-S04a Time Calibration: 50ms -> 83cm error."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, ACCENT_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL,
    vehicle_icon, key_number,
)
SCRIPT = """A 50-millisecond delay at 60 km/h is 83 centimeters of position error."""


class P03S04ATimeCalibration(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Time Calibration"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        car = vehicle_icon(color=ACCENT_BLUE, scale=1.1).move_to(LEFT * 3 + UP * 0.8)
        speed_lbl = Text("60 km/h", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_BLUE)
        speed_lbl.next_to(car, UP, buff=0.12)
        self.play(GrowFromCenter(car), FadeIn(speed_lbl))
        self.play(car.animate.move_to(LEFT * 1.2 + UP * 0.8), run_time=1.0, rate_func=linear)
        # Observed position 83cm behind
        obs_car = car.copy().set_color(RED_ERROR).set_opacity(0.55)
        obs_car.move_to(car.get_center() + LEFT * 0.83)
        self.play(FadeIn(obs_car))
        gap = DoubleArrow(obs_car.get_right(), car.get_left(), buff=0.05,
                          fill_color=RED_ERROR, thickness=2.5)
        gap_lbl = Text("83 cm error", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        gap_lbl.next_to(gap, DOWN, buff=0.1)
        delay_tag = Text("Infra sees -50ms ago", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR)
        delay_tag.next_to(obs_car, UP, buff=0.12)
        self.play(ShowCreation(gap), FadeIn(gap_lbl), FadeIn(delay_tag))
        kn = key_number("83 cm", "position error at 60 km/h", color=RED_ERROR)
        kn.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(kn))
        self.wait(2)
        self._close()
''')

W("p03_s04b_space_calibration.py", '''"""P03-S04b Space Calibration: matrix fly-in + point cloud merge."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_GREEN, RED_ERROR, PURPLE_MODEL, GOLD_RICH,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
)
SCRIPT = """Space calibration is the transform from one sensor frame into a common one."""


def point_cloud_mob(center, n=16, color=ACCENT_BLUE, spread=0.55, seed=42):
    """Local helper — Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/vector_space_scene.py:204"""
    rng = np.random.RandomState(seed)
    pts = VGroup()
    for _ in range(n):
        dx, dy = rng.uniform(-spread, spread, 2)
        d = Dot(radius=0.055, color=color)
        d.move_to(center + np.array([dx, dy, 0]))
        pts.add(d)
    return pts


class P03S04BSpaceCalibration(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Space Calibration"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        cloud_v = point_cloud_mob(LEFT * 3.5 + UP * 0.2, color=ACCENT_BLUE, seed=1)
        cloud_i = point_cloud_mob(RIGHT * 0.2 + UP * 0.8, color=ACCENT_GREEN, seed=5)
        lbl_v = Text("Vehicle frame", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_BLUE)
        lbl_v.next_to(cloud_v, DOWN, buff=0.15)
        lbl_i = Text("Infra frame", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_GREEN)
        lbl_i.next_to(cloud_i, DOWN, buff=0.15)

        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in cloud_v), lag_ratio=0.04, run_time=1.0))
        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in cloud_i), lag_ratio=0.04, run_time=1.0))
        self.play(FadeIn(lbl_v), FadeIn(lbl_i))

        # Transform matrix flies in from top
        # Pattern adapted from: Source_manim_reference/welchlabs_videos/once_useful_constructs/vector_space_scene.py:204
        mat_entries = [["R", "t"], ["0", "1"]]
        mat = Matrix(mat_entries, h_buff=1.2, v_buff=0.8)
        mat.set_column_colors(PURPLE_MODEL, GOLD_RICH)
        mat_lbl = Text("Spatial Transform T", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=PURPLE_MODEL, weight=BOLD)
        mat.move_to(ORIGIN + UP * 0.2)
        mat_lbl.next_to(mat, UP, buff=0.12)
        self.play(FadeIn(mat, shift=DOWN * 1.5, run_time=0.8), FadeIn(mat_lbl))

        # Merged cloud appears right
        merged = point_cloud_mob(RIGHT * 4.0 + UP * 0.2, n=24, color=ACCENT_GREEN, seed=99)
        lbl_merged = Text("Common frame", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_GREEN)
        lbl_merged.next_to(merged, DOWN, buff=0.15)
        arr_v = Arrow(cloud_v.get_right() + RIGHT * 0.05, merged.get_left() + LEFT * 0.05,
                      fill_color=PURPLE_MODEL, thickness=2.0, buff=0.06)
        arr_i = Arrow(cloud_i.get_right() + RIGHT * 0.05, merged.get_left() + LEFT * 0.05,
                      fill_color=PURPLE_MODEL, thickness=2.0, buff=0.06)
        self.play(ShowCreation(arr_v), ShowCreation(arr_i))
        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in merged), lag_ratio=0.02, run_time=0.8))
        self.play(FadeIn(lbl_merged))

        # Ghost object bad calibration demo
        ghost = point_cloud_mob(RIGHT * 4.0 + UP * 1.2, n=10, color=RED_ERROR, spread=0.65, seed=13)
        ghost_lbl = Text("[WARN] Bad calib -> ghost object", font=FONT_PRIMARY,
                         font_size=SIZE_LABEL, color=RED_ERROR)
        ghost_lbl.next_to(ghost, UP, buff=0.1)
        self.play(FadeIn(ghost, scale=0.5), FadeIn(ghost_lbl))
        self.play(Flash(VGroup(ghost, ghost_lbl), color=RED_ERROR, num_lines=8, line_length=0.3, run_time=0.5))
        self.play(FadeOut(ghost), FadeOut(ghost_lbl))

        self.wait(2)
        self._close()
''')

W("p03_s05_data_collection.py", '''"""P03-S05 Data Collection Routes."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_GREEN, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    contribution_badge,
)
SCRIPT = """V2X-Real and V2XPnP-Seq: routes, every time of day."""


class P03S05DataCollection(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Data Collection"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        routes_data = [("R-Turn", UP), ("L-Turn", LEFT), ("Straight", RIGHT * 2)]
        y_starts = [1.0, 0.0, -1.0]
        for (name, direction), y in zip(routes_data, y_starts):
            start = LEFT * 4.5 + UP * y
            end = LEFT * 2.0 + UP * y + direction * 0.5
            line = Line(start, end, stroke_color=ACCENT_GREEN, stroke_width=2.5)
            lbl = Text(name, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
            lbl.next_to(start, LEFT, buff=0.1)
            self.play(ShowCreation(line, run_time=0.4), FadeIn(lbl, run_time=0.3))
        times = ["Morning", "Noon", "Evening", "Night"]
        colors = ["#FCD34D", "#FDE68A", "#F97316", "#1E293B"]
        time_group = VGroup()
        for t, c in zip(times, colors):
            box = RoundedRectangle(width=1.8, height=0.6, corner_radius=0.1,
                                   fill_color=c, fill_opacity=0.7, stroke_width=0)
            lbl = Text(t, font=FONT_PRIMARY, font_size=SIZE_CAPS,
                       color=INK_DARK if c != "#1E293B" else "#94A3B8")
            lbl.move_to(box)
            time_group.add(VGroup(box, lbl))
        time_group.arrange(RIGHT, buff=0.2).move_to(DOWN * 1.2)
        self.play(LaggedStart(*(FadeIn(g) for g in time_group), lag_ratio=0.15))
        badges = VGroup(
            contribution_badge("V2X-Real  ·  ECCV 2024", color=GOLD_RICH),
            contribution_badge("V2XPnP-Seq Dataset", color=ACCENT_GREEN),
        )
        badges.arrange(RIGHT, buff=0.5)
        badges.to_edge(DOWN, buff=0.4)
        self.play(LaggedStart(*(FadeIn(b) for b in badges), lag_ratio=0.2))
        self.wait(2)
        self._close()
''')

W("p03_s06_localization_role.py", '''"""P03-S06 Localization Role."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, ACCENT_BLUE, ACCENT_GREEN, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL,
)
SCRIPT = """With cooperative perception, localization matters. Wrong position = worse than single."""


def cloud(center, n, color, spread=0.4, seed=42):
    rng = np.random.RandomState(seed)
    grp = VGroup()
    for _ in range(n):
        dx, dy = rng.uniform(-spread, spread, 2)
        d = Dot(radius=0.055, color=color)
        d.move_to(center + np.array([dx, dy, 0]))
        grp.add(d)
    return grp


class P03S06LocalizationRole(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Why Localization Matters"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # Left: bad localization
        bad_v = cloud(LEFT * 3.5 + UP * 0.3, 12, ACCENT_BLUE, seed=1)
        bad_i = cloud(LEFT * 3.5 + UP * 0.3 + np.array([0.5, 0.35, 0]), 10, RED_ERROR, seed=2)
        bad_lbl = Text("[NO] No localization", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR)
        bad_lbl.next_to(bad_v, DOWN, buff=0.12)
        bad_sub = Text("Worse than single", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2, color=RED_ERROR)
        bad_sub.next_to(bad_lbl, DOWN, buff=0.05)
        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in bad_v), lag_ratio=0.03))
        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in bad_i), lag_ratio=0.03))
        self.play(FadeIn(bad_lbl), FadeIn(bad_sub))
        # Right: good localization
        good_v = cloud(RIGHT * 2.5 + UP * 0.3, 12, ACCENT_BLUE, seed=3)
        good_i = cloud(RIGHT * 2.5 + UP * 0.3, 10, ACCENT_GREEN, seed=4, spread=0.35)
        good_lbl = Text("[OK] Precise localization", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GREEN_FIX)
        good_lbl.next_to(good_v, DOWN, buff=0.12)
        good_sub = Text("Clean fused output", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2, color=GREEN_FIX)
        good_sub.next_to(good_lbl, DOWN, buff=0.05)
        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in good_v), lag_ratio=0.03))
        self.play(LaggedStart(*(FadeIn(d, scale=0.4) for d in good_i), lag_ratio=0.03))
        self.play(FadeIn(good_lbl), FadeIn(good_sub))
        self.wait(2)
        self._close()
''')

print("Batch 1 done (S02-S06)")
