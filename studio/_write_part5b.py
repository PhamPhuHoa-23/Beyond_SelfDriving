"""Write Part 5 hero scenes: S09 Living City, S10 Montage, S11 Final Frame."""
import os, numpy as np

BASE = "studio/scenes/part05"
os.makedirs(BASE, exist_ok=True)


def W(name, code):
    path = os.path.join(BASE, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"wrote {name}")


W("p05_s09_living_city.py", '''"""P05-S09 The Living City — 3D hero finale, 50s."""
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
        for x in np.linspace(-5.5, 5.5, 12):
            grid.add(Line([x, -4, 0], [x, 4, 0], stroke_color=CYAN_RADAR, stroke_width=0.5, stroke_opacity=0.18))
        for y in np.linspace(-4, 4, 9):
            grid.add(Line([-5.5, y, 0], [5.5, y, 0], stroke_color=CYAN_RADAR, stroke_width=0.5, stroke_opacity=0.18))
        roads_h = Rectangle(width=11, height=0.9, fill_color="#0F172A", fill_opacity=0.5, stroke_width=0)
        roads_v = Rectangle(width=0.9, height=8, fill_color="#0F172A", fill_opacity=0.5, stroke_width=0)
        self.play(FadeIn(grid), FadeIn(roads_h), FadeIn(roads_v), run_time=0.8)

        rng = np.random.RandomState(7)
        all_agents = []

        # Phase 1 — 6 agent types fade in at t=1,3,5,7,9,11s
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/hairy_ball/model3d.py:68

        # t=1s: cars (blue)
        cars = VGroup()
        car_positions = [[-3.5, -0.4, 0.05], [-1.2, 1.2, 0.05], [2.8, -0.4, 0.05], [0.8, -1.8, 0.05]]
        for pos in car_positions:
            c = vehicle_icon(color=ACCENT_BLUE, scale=0.75)
            c.move_to(pos)
            cars.add(c)
        self.play(LaggedStart(*(FadeIn(c) for c in cars), lag_ratio=0.15, run_time=0.8))
        all_agents.extend(list(cars))
        self.wait(1.2)

        # t=3s: robots (green)
        robots = VGroup()
        for pos in [[-2.2, 1.8, 0.05], [3.5, 1.2, 0.05], [-0.5, -2.5, 0.05]]:
            r = vehicle_icon(color=ACCENT_GREEN, scale=0.6)
            r.move_to(pos)
            robots.add(r)
        self.play(LaggedStart(*(FadeIn(r) for r in robots), lag_ratio=0.15, run_time=0.6))
        all_agents.extend(list(robots))
        self.wait(1.4)

        # t=5s: wheelchairs (pink)
        chairs = VGroup()
        for pos in [[1.5, 2.2, 0.05], [-3.8, 1.0, 0.05]]:
            ch = pedestrian_icon(color=ACCENT_PINK).scale(0.8)
            ch.move_to(pos)
            chairs.add(ch)
        self.play(LaggedStart(*(FadeIn(ch) for ch in chairs), lag_ratio=0.2, run_time=0.5))
        all_agents.extend(list(chairs))
        self.wait(1.5)

        # t=7s: pedestrians (gold)
        peds = VGroup()
        for pos in [[-1.8, -1.5, 0.05], [0.3, 2.8, 0.05], [4.0, -1.5, 0.05], [-4.2, -1.8, 0.05]]:
            p = pedestrian_icon(color=GOLD_KEY).scale(0.75)
            p.move_to(pos)
            peds.add(p)
        self.play(LaggedStart(*(FadeIn(p) for p in peds), lag_ratio=0.12, run_time=0.6))
        all_agents.extend(list(peds))
        self.wait(1.4)

        # t=9s: RSUs (orange) at intersection corners
        rsus = VGroup()
        for pos in [[-4.5, 3.5, 0.05], [4.5, 3.5, 0.05], [-4.5, -3.5, 0.05]]:
            r = rsu_icon(color=ORANGE_INFRA).scale(1.1)
            r.move_to(pos)
            rsus.add(r)
        self.play(LaggedStart(*(GrowFromCenter(r) for r in rsus), lag_ratio=0.2))
        all_agents.extend(list(rsus))
        self.wait(1.5)

        # t=11s: drones (white/light)
        drones = VGroup()
        for pos in [[2.0, 0.5, 0.5], [-2.5, 3.0, 0.5], [0.0, -3.2, 0.5]]:
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
        all_shells = VGroup()
        for rsu in rsu_list:
            shells, anim = radar_shells_2d(rsu.get_center(), color=CYAN_RADAR, n_shells=3, max_radius=2.5)
            all_shells.add(shells)
        for ag in list(cars)[:2]:
            shells, anim = radar_shells_2d(ag.get_center(), color=ACCENT_BLUE, n_shells=2, max_radius=1.8)
            all_shells.add(shells)
        self.play(LaggedStart(*(FadeIn(s) for s in all_shells), lag_ratio=0.05, run_time=2.0))

        # Camera rotate +30deg over 15s
        self.play(self.frame.animate.reorient(5, 60, 0), run_time=15, rate_func=smooth)

        # Phase 3 (30-50s): camera pullback, city becomes background
        self.play(self.frame.animate.set_height(16), run_time=8, rate_func=smooth)
        self.wait(10)
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=1.5)
        self.wait(0.5)
''')

W("p05_s10_chain_of_solutions.py", '''"""P05-S10 Chain of Solutions Montage — 5 vignettes."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK,
    GOLD_RICH, INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    contribution_badge,
)
SCRIPT = """Five parts. Five solutions. One story."""


PART_SUMMARIES = [
    ("Part 1", "Foundation Models\nAutoVLA: long-tail reasoning", ACCENT_BLUE),
    ("Part 2", "Cooperative Perception\nV2XPnP: blind zone vanishes", ACCENT_TEAL),
    ("Part 3", "Sim-to-Real\nCooperFuse + Digital Twin", ACCENT_GREEN),
    ("Part 4", "Efficiency\nQuantV2X: 300x smaller", ACCENT_AMBER),
    ("Part 5", "Physical AI\nCityWalker + PedGen: alive", ACCENT_PINK),
]


class P05S10ChainOfSolutions(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Five Parts, One Story"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        panels = VGroup()
        for part, summary, color in PART_SUMMARIES:
            bg = RoundedRectangle(width=2.0, height=3.2, corner_radius=0.15,
                                  fill_color=BG_PAPER, fill_opacity=1.0,
                                  stroke_color=color, stroke_width=2.5)
            title = Text(part, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
            body = Text(summary, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
            inner = VGroup(title, body).arrange(DOWN, buff=0.15)
            inner.move_to(bg)
            panels.add(VGroup(bg, inner))
        panels.arrange(RIGHT, buff=0.35).move_to(ORIGIN + DOWN * 0.2)
        self.play(LaggedStart(*(FadeIn(p, shift=DOWN * 0.5) for p in panels), lag_ratio=0.2, run_time=1.5))
        finale = Text("Five parts. Five solutions. One story.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        finale.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(finale, scale=1.05))
        self.wait(2)
        self._close()
''')

W("p05_s11_final_frame.py", '''"""P05-S11 Final Frame — "Beyond Self-Driving. Not just smarter cars. A safer world." """
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_TITLECARD, GOLD_RICH, GOLD_KEY, INK_LIGHT, CYAN_RADAR,
    ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK,
    FONT_PRIMARY, SIZE_TITLE, SIZE_LABEL, SIZE_CAPS,
    write_chiseled, dust_dissolve,
)
SCRIPT = """Beyond Self-Driving. Not just smarter cars. A safer world."""


class P05S11FinalFrame(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Final Frame"

    def construct(self):
        self.camera.background_color = BG_TITLECARD

        # Subtle background grid (city echo)
        rng = np.random.RandomState(99)
        bg_dots = VGroup()
        for _ in range(40):
            d = Dot(radius=0.04, color=CYAN_RADAR)
            d.move_to(np.array([rng.uniform(-7, 7), rng.uniform(-4, 4), 0]))
            d.set_opacity(rng.uniform(0.08, 0.22))
            bg_dots.add(d)
        self.add(bg_dots)

        # Line 1 — hold 1s after write
        line1 = Text("Beyond Self-Driving.", font=FONT_PRIMARY, font_size=SIZE_TITLE,
                     color=GOLD_RICH, weight=BOLD)
        line1.move_to(UP * 1.2)
        self.play(write_chiseled(line1, run_time=2.5))
        self.wait(1)

        # Line 2 — hold 1s
        line2 = Text("Not just smarter cars.", font=FONT_PRIMARY, font_size=SIZE_TITLE,
                     color=GOLD_RICH)
        line2.move_to(ORIGIN)
        self.play(write_chiseled(line2, run_time=2.0))
        self.wait(1)

        # Line 3 — hold 2s
        line3 = Text("A safer world.", font=FONT_PRIMARY, font_size=SIZE_TITLE,
                     color=GOLD_RICH)
        line3.move_to(DOWN * 1.2)
        self.play(write_chiseled(line3, run_time=1.8))
        self.wait(2)

        # Roadmap strip: all 5 nodes GOLD
        part_colors = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK]
        dots = VGroup()
        for i in range(5):
            d = Dot(radius=0.12, color=GOLD_RICH)
            d.move_to(DOWN * 2.8 + RIGHT * (i - 2) * 1.2)
            dots.add(d)
        connector = Line(dots[0].get_center(), dots[-1].get_center(),
                         stroke_color=GOLD_RICH, stroke_width=1.5, stroke_opacity=0.6)
        self.play(ShowCreation(connector, run_time=0.8),
                  LaggedStart(*(FadeIn(d) for d in dots), lag_ratio=0.1, run_time=0.8))
        self.play(LaggedStart(*(Flash(d, color=GOLD_RICH, line_length=0.18, num_lines=6) for d in dots), lag_ratio=0.08))

        # UCLA text badge
        ucla = Text("UCLA Mobility Lab  ·  ICCV 2025", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        ucla.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(ucla))
        self.wait(1.5)

        # Dust converge to center — inverse of particle_assemble
        # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/logo.py:192 LogoGenerationFlurry inverse
        converge_pts = VGroup()
        for _ in range(80):
            angle = rng.uniform(0, TAU)
            dist = rng.uniform(1.5, 5.5)
            pt = Dot(radius=0.05, color=GOLD_RICH)
            pt.move_to(np.array([dist * np.cos(angle), dist * np.sin(angle), 0]))
            pt.set_opacity(rng.uniform(0.5, 0.9))
            converge_pts.add(pt)
        self.play(LaggedStart(*(FadeIn(p, scale=0.5) for p in converge_pts), lag_ratio=0.01, run_time=0.8))
        # Converge to center dot
        center_dot = Dot(radius=0.18, color=GOLD_RICH)
        self.play(*(p.animate(run_time=2.0, rate_func=smooth, path_arc=rng.uniform(-PI/3, PI/3))
                    .move_to(ORIGIN)
                    for p in converge_pts),
                  FadeOut(VGroup(line1, line2, line3, connector, dots, ucla, bg_dots), run_time=1.5),
                  run_time=2.0)
        self.play(GrowFromCenter(center_dot, run_time=0.3))
        self.play(Flash(center_dot, color=GOLD_RICH, line_length=0.4, num_lines=14, run_time=0.6))
        self.play(FadeOut(converge_pts), FadeOut(center_dot), run_time=1.0)
        self.wait(0.5)
''')

print("Batch 2 done (S09-S11 heroes + finale)")
