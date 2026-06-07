"""P05-S09 The Living City — 3D hero finale, 50s."""
from manimlib import *
import numpy as np
from studio.components import (
    Studio3DScene, BG_TITLECARD,
    ACCENT_BLUE, ACCENT_PINK, ACCENT_GREEN, GOLD_KEY, ORANGE_INFRA, INK_LIGHT, CYAN_RADAR,
    FONT_PRIMARY, SIZE_LABEL,
    vehicle_icon, pedestrian_icon, rsu_icon, drone_icon,
    radar_shells_2d, v2x_link, ambient_glow,
)
SCRIPT = """Every agent. Every signal. A city that breathes by electromagnetic radiation."""


class P05S09LivingCity(Studio3DScene):
    PART_NUM = 5
    SCENE_TITLE = "The Living City"
    default_frame_orientation = (-25, 60)

    def construct(self):
        self.camera.background_color = BG_TITLECARD

        # City grid
        grid = VGroup()
        for x in np.linspace(-4.7, 4.7, 11):
            grid.add(Line([x, -3.1, 0], [x, 3.1, 0], stroke_color=CYAN_RADAR, stroke_width=0.5, stroke_opacity=0.18))
        for y in np.linspace(-3.1, 3.1, 9):
            grid.add(Line([-5.0, y, 0], [5.0, y, 0], stroke_color=CYAN_RADAR, stroke_width=0.5, stroke_opacity=0.18))
        roads_h = Rectangle(width=9.3, height=0.78, fill_color="#0F172A", fill_opacity=0.5, stroke_width=0)
        roads_v = Rectangle(width=0.78, height=6.2, fill_color="#0F172A", fill_opacity=0.5, stroke_width=0)
        self.play(FadeIn(grid), FadeIn(roads_h), FadeIn(roads_v), run_time=0.8)

        rng = np.random.RandomState(7)
        all_agents = []

        # Phase 1 — 6 agent types fade in at t=1,3,5,7,9,11s
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py:68

        # t=1s: cars (blue)
        cars = VGroup()
        car_positions = [[-3.1, -0.35, 0.05], [-1.1, 1.05, 0.05], [2.5, -0.35, 0.05], [0.75, -1.25, 0.05]]
        for pos in car_positions:
            c = vehicle_icon(color=ACCENT_BLUE, scale=0.75)
            c.move_to(pos)
            cars.add(c)
        self.play(LaggedStart(*(FadeIn(c) for c in cars), lag_ratio=0.15, run_time=0.8))
        all_agents.extend(list(cars))
        self.wait(1.2)

        # t=3s: robots (green)
        robots = VGroup()
        for pos in [[-2.0, 1.55, 0.05], [3.1, 1.05, 0.05], [-0.45, -1.75, 0.05]]:
            r = vehicle_icon(color=ACCENT_GREEN, scale=0.6)
            r.move_to(pos)
            robots.add(r)
        self.play(LaggedStart(*(FadeIn(r) for r in robots), lag_ratio=0.15, run_time=0.6))
        all_agents.extend(list(robots))
        self.wait(1.4)

        # t=5s: wheelchairs (pink)
        chairs = VGroup()
        for pos in [[1.35, 1.9, 0.05], [-3.35, 0.9, 0.05]]:
            ch = pedestrian_icon(color=ACCENT_PINK).scale(0.8)
            ch.move_to(pos)
            chairs.add(ch)
        self.play(LaggedStart(*(FadeIn(ch) for ch in chairs), lag_ratio=0.2, run_time=0.5))
        all_agents.extend(list(chairs))
        self.wait(1.5)

        # t=7s: pedestrians (gold)
        peds = VGroup()
        for pos in [[-1.6, -1.05, 0.05], [0.25, 2.4, 0.05], [3.55, -1.05, 0.05], [-3.7, -1.2, 0.05]]:
            p = pedestrian_icon(color=GOLD_KEY).scale(0.75)
            p.move_to(pos)
            peds.add(p)
        self.play(LaggedStart(*(FadeIn(p) for p in peds), lag_ratio=0.12, run_time=0.6))
        all_agents.extend(list(peds))
        self.wait(1.4)

        # t=9s: RSUs (orange) at intersection corners
        rsus = VGroup()
        for pos in [[-3.65, 2.65, 0.05], [3.65, 2.65, 0.05], [-2.85, -1.45, 0.05]]:
            r = rsu_icon(color=ORANGE_INFRA).scale(1.1)
            r.move_to(pos)
            rsus.add(r)
        self.play(LaggedStart(*(GrowFromCenter(r) for r in rsus), lag_ratio=0.2))
        all_agents.extend(list(rsus))
        self.wait(1.5)

        # t=11s: drones (white/light)
        drones = VGroup()
        for pos in [[1.8, 0.45, 0.5], [-2.2, 2.35, 0.5], [0.0, -1.9, 0.5]]:
            d = drone_icon(color=INK_LIGHT).scale(0.9)
            d.move_to(pos)
            drones.add(d)
        self.play(LaggedStart(*(FadeIn(d, shift=DOWN * 0.3) for d in drones), lag_ratio=0.2))
        all_agents.extend(list(drones))
        self.wait(2)

        # Phase 2 (15-30s): V2X web links + radar interference
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py:260
        links = VGroup()
        rsu_list = list(rsus)
        for rsu in rsu_list:
            for ag in all_agents[:12]:  # connect RSUs to nearby agents
                lnk = Line(rsu.get_center(), ag.get_center(),
                           stroke_color=CYAN_RADAR, stroke_width=0.8, stroke_opacity=0.35)
                links.add(lnk)
        self.play(LaggedStart(*(ShowCreation(l) for l in links), lag_ratio=0.01, run_time=3.0))

        # Radar shells from RSUs + interference
        all_shells = Group()
        for i, rsu in enumerate(rsu_list):
            radius = 1.2 if i == 2 else 1.65
            shells, anim = radar_shells_2d(rsu.get_center(), color=CYAN_RADAR, n_shells=3, max_radius=radius)
            all_shells.add(shells)
        for ag in list(cars)[:2]:
            shells, anim = radar_shells_2d(ag.get_center(), color=ACCENT_BLUE, n_shells=2, max_radius=1.45)
            all_shells.add(shells)
        self.play(LaggedStart(*(FadeIn(s) for s in all_shells), lag_ratio=0.05, run_time=2.0))

        # Camera rotate +30deg over 15s
        self.play(self.frame.animate.reorient(5, 60, 0), run_time=15, rate_func=smooth)

        # Phase 3 (30-50s): camera pullback, city becomes background
        self.play(self.frame.animate.set_height(14), run_time=8, rate_func=smooth)
        self.wait(10)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.5)
