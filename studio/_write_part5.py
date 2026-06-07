"""Write all Part 5 + Finale scene files."""
import os, numpy as np

BASE = "studio/scenes/part05"
os.makedirs(BASE, exist_ok=True)


def W(name, code):
    path = os.path.join(BASE, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"wrote {name}")


W("p05_s01_title.py", '''"""P05-S01 Part 5 Title — all 5 roadmap nodes light up simultaneously."""
from manimlib import *
from studio.components import (
    StudioScene, BG_TITLECARD, ACCENT_PINK, GOLD_RICH, INK_LIGHT,
    ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER,
    FONT_PRIMARY, SIZE_CAPS, SIZE_LABEL, write_chiseled,
)
SCRIPT = """Part 5: Scalable, Human-Centric Physical AI — with Wayne Wu. Beyond cars — to any agent, any space."""


class P05S01Title(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Scalable Human-Centric Physical AI"

    def construct(self):
        self.camera.background_color = BG_TITLECARD
        part_tag = Text("Part 05", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_PINK)
        part_tag.to_corner(UR, buff=0.4)
        self.play(FadeIn(part_tag))
        line1 = Text("Scalable,", font=FONT_PRIMARY, font_size=48, color=ACCENT_PINK, weight=BOLD)
        line2 = Text("Human-Centric Physical AI", font=FONT_PRIMARY, font_size=44, color=GOLD_RICH)
        title = VGroup(line1, line2).arrange(DOWN, buff=0.15).move_to(UP * 0.5)
        self.play(LaggedStart(write_chiseled(line1, run_time=1.6), write_chiseled(line2, run_time=2.0), lag_ratio=0.5))
        speaker = Text("Wayne Wu  ·  UCLA Mobility Lab", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        speaker.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(speaker))
        quote = Text('"Beyond cars — to any agent, any space."', font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        quote.next_to(speaker, DOWN, buff=0.35)
        self.play(write_chiseled(quote, run_time=2.0))
        # All 5 roadmap nodes light up simultaneously — first time in the video
        # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/logo.py:216 LogoGenerationFivefold
        part_colors = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK]
        roadmap = self._roadmap_strip()
        self.play(FadeIn(roadmap))
        # Override all dots to GOLD simultaneously
        dots = roadmap[0]
        self.play(AnimationGroup(*(d.animate.set_fill(GOLD_RICH) for d in dots), lag_ratio=0.0, run_time=0.8))
        self.play(LaggedStart(*(Flash(d, color=GOLD_RICH, line_length=0.18, num_lines=6) for d in dots), lag_ratio=0.1))
        self.wait(2)
        self._close()
''')

W("p05_s02a_llm_vs_robot.py", '''"""P05-S02a LLM vs Robot data disparity."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, GOLD_RICH, RED_ERROR, ACCENT_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, pipeline_arrow,
)
SCRIPT = """LLMs work because of web-scale data. Physical AI does not have that."""


class P05S02ALLMVsRobot(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "LLM vs Robot Data Gap"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # Left: internet flood -> LLM
        sources = VGroup(*(
            Text(src, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
            for src in ["Wikipedia", "GitHub", "Reddit", "Books", "News"]
        ))
        sources.arrange(DOWN, buff=0.18).move_to(LEFT * 4.5)
        llm = pipeline_block("LLM", fill="#E0D7FF", stroke=ACCENT_BLUE, width=2.0, height=1.2)
        llm.move_to(LEFT * 1.5)
        tokens = Text("Trillions of tokens", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        tokens.next_to(llm, RIGHT, buff=0.4)
        self.play(LaggedStart(*(FadeIn(s, shift=RIGHT * 0.3) for s in sources), lag_ratio=0.1))
        self.play(FadeIn(llm), FadeIn(tokens))
        for s in sources:
            arr = Arrow(s.get_right() + RIGHT * 0.05, llm.get_left() + LEFT * 0.05, fill_color=ACCENT_BLUE, thickness=1.5, buff=0.06)
            self.add(arr)
        # Right: robots collecting tiny
        robot_lbl = Text("3 robots collecting data", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID)
        robot_lbl.move_to(RIGHT * 3.0 + UP * 0.5)
        trickle = Text("~10 hours / robot", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        trickle.next_to(robot_lbl, DOWN, buff=0.2)
        self.play(FadeIn(robot_lbl), FadeIn(trickle))
        cap = Text("Trillions of tokens  vs  10 hours per robot", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
''')

W("p05_s02b_two_barriers.py", '''"""P05-S02b Two Barriers."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, ACCENT_PINK, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL,
)
SCRIPT = """Two barriers. No data at internet scale. No model of human behavior."""


class P05S02BTwoBarriers(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Two Barriers"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        b1_title = Text("Barrier 1", font=FONT_PRIMARY, font_size=SIZE_H1, color=RED_ERROR, weight=BOLD)
        b1_body = Text("No web-scale robot data", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        b1 = VGroup(b1_title, b1_body).arrange(DOWN, buff=0.15).move_to(LEFT * 2.5 + UP * 0.5)
        b2_title = Text("Barrier 2", font=FONT_PRIMARY, font_size=SIZE_H1, color=RED_ERROR, weight=BOLD)
        b2_body = Text("No human behavior model —\nso simulations look like zombie cities.", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        b2 = VGroup(b2_title, b2_body).arrange(DOWN, buff=0.15).move_to(RIGHT * 2.5 + UP * 0.3)
        self.play(FadeIn(b1[0]), FadeIn(b1[1]))
        # Mini zombie-city preview: grey squares moving straight
        zombies = VGroup(*(Square(side_length=0.12, fill_color="#6B7280", fill_opacity=0.8, stroke_width=0).move_to(np.array([x, y, 0])) for x, y in zip(np.linspace(-1.5, 1.5, 5), [-1.8] * 5)))
        self.play(FadeIn(zombies))
        self.play(*(z.animate(run_time=0.8, rate_func=linear).shift(RIGHT * 0.5) for z in zombies))
        self.play(FadeIn(b2[0]), FadeIn(b2[1]))
        self.wait(2)
        self._close()
''')

W("p05_s03_micromobility.py", '''"""P05-S03 Micro-Mobility Testbed."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, GOLD_KEY, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon, pedestrian_icon, drone_icon, contribution_badge,
)
SCRIPT = """Sixty percent of US trips are under five miles. Micro-mobility: robots, wheelchairs, scooters, humanoids."""


class P05S03Micromobility(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Micro-Mobility Testbed"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        stat = Text("60% of US trips  <  5 miles", font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH, weight=BOLD)
        stat.move_to(UP * 1.6)
        self.play(FadeIn(stat, scale=1.1))
        agents = [
            ("Delivery Robot", vehicle_icon(color="#10B981")),
            ("e-Wheelchair", pedestrian_icon(color="#8B5CF6")),
            ("Scooter", vehicle_icon(color=ACCENT_PINK)),
            ("Humanoid", pedestrian_icon(color=GOLD_KEY)),
        ]
        cards = VGroup()
        for name, icon in agents:
            icon.scale(1.2)
            lbl = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
            bg = RoundedRectangle(width=2.2, height=1.8, corner_radius=0.15, fill_color=BG_PAPER, fill_opacity=1.0, stroke_color=ACCENT_PINK, stroke_width=1.8)
            grp = VGroup(icon, lbl).arrange(DOWN, buff=0.12)
            grp.move_to(bg)
            cards.add(VGroup(bg, grp))
        cards.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.3)
        self.play(LaggedStart(*(FadeIn(c, scale=0.85) for c in cards), lag_ratio=0.2))
        badge = contribution_badge("COCO Robotics Partnership", color=GOLD_KEY)
        badge.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(badge))
        self.wait(2)
        self._close()
''')

W("p05_s04a_compositional_quote.py", '''"""P05-S04a Stuart Geman quote — letters fly from random positions."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_TITLECARD, GOLD_RICH, INK_LIGHT,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL, SIZE_CAPS,
    write_chiseled,
)
SCRIPT = """The world is compositional, or there is a god — Stuart Geman."""


class P05S04ACompositionalQuote(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "A Fundamental Insight"

    def construct(self):
        self.camera.background_color = BG_TITLECARD
        # Pattern adapted from: Source_manim_reference/3b1b_videos/custom/opening_quote.py:8
        quote1 = Text('"The world is compositional,', font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH)
        quote2 = Text('or there is a god."', font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH)
        attribution = Text("— Stuart Geman", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_LIGHT)
        q_group = VGroup(quote1, quote2).arrange(DOWN, buff=0.22)
        q_group.move_to(ORIGIN + UP * 0.3)
        attribution.next_to(q_group, DOWN, buff=0.35)
        # Letters scatter from random then fly to position
        rng = np.random.RandomState(42)
        char_mobs = VGroup(*quote1, *quote2)
        for m in char_mobs:
            m.save_state()
            m.move_to(np.array([rng.uniform(-6, 6), rng.uniform(-3.5, 3.5), 0]))
            m.set_opacity(0)
        self.play(LaggedStart(*(Restore(m, run_time=1.2) for m in char_mobs), lag_ratio=0.02, run_time=2.5))
        self.play(FadeIn(attribution))
        self.wait(3)
        self._close()
''')

W("p05_s04b_metaurban.py", '''"""P05-S04b MetaUrban Generator."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, CYAN_RADAR, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, contribution_badge,
)
SCRIPT = """MetaUrban generates urban scenes from a script: layout, intersections, objects. No two scenes alike."""


class P05S04BMetaUrban(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "MetaUrban Generator"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        input_block = pipeline_block("generate_scene(\\nparams...)", fill="#F0FDF4", stroke="#10B981", width=3.0, height=1.2)
        input_block.move_to(LEFT * 3.5 + UP * 0.3)
        gear = Circle(radius=0.5, fill_color=CYAN_RADAR, fill_opacity=0.2, stroke_color=CYAN_RADAR, stroke_width=2.5)
        gear_lbl = Text("Generator", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=CYAN_RADAR)
        gear_grp = VGroup(gear, gear_lbl).arrange(DOWN, buff=0.08)
        gear_grp.move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(input_block), GrowFromCenter(gear_grp))
        # Output scenes cycling
        scene_labels = ["Urban Scene 1", "Urban Scene 2", "Urban Scene 3", "...  infinity"]
        colors = [ACCENT_PINK, GOLD_RICH, CYAN_RADAR, INK_MID]
        for lbl, col in zip(scene_labels, colors):
            s = pipeline_block(lbl, fill=BG_PAPER, stroke=col, width=2.4, height=0.7)
            s.move_to(RIGHT * 3.5 + UP * 0.3)
            self.play(FadeIn(s, run_time=0.3))
            self.wait(0.2)
            self.play(FadeOut(s, run_time=0.25))
        key_lbl = Text("Diversity > Quantity", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        key_lbl.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(key_lbl))
        self.wait(2)
        self._close()
''')

W("p05_s04c_metaurban_scaling.py", '''"""P05-S04c MetaUrban Scaling Curve."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL,
    axes_deploy, curve_trace,
)
SCRIPT = """The scaling is power-law. A hundred diverse scenes beat a thousand near-duplicates."""


class P05S04CMetaUrbanScaling(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Diversity Scaling"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        axes, axes_anim = axes_deploy(
            (0, 5, 1), (0, 1.0, 0.25), x_label="Unique layouts", y_label="Unseen env. perf."
        )
        axes.scale(0.75).move_to(LEFT * 1.5 + DOWN * 0.2)
        self.play(axes_anim)
        # Power-law curve: diverse
        diverse_anim = curve_trace(axes, lambda x: 1 - np.exp(-x * 0.9), color=GOLD_RICH, run_time=2.0)
        self.play(diverse_anim)
        # Linear baseline: repeated
        repeat_anim = curve_trace(axes, lambda x: x * 0.12, color=INK_MID, run_time=1.5)
        self.play(repeat_anim)
        callout = Text("100 diverse > 1000 repeated", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        callout.move_to(RIGHT * 3.5 + UP * 0.8)
        self.play(FadeIn(callout, scale=1.05))
        self.wait(2)
        self._close()
''')

W("p05_s05a_urbansim_bottleneck.py", '''"""P05-S05a UrbanSim CPU-GPU Bottleneck."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, ACCENT_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_H1,
    pipeline_block, pipeline_arrow,
)
SCRIPT = """Training a simple RL agent used to take 180 GPU-days — CPU-GPU bottleneck at every step."""


class P05S05AUrbanSimBottleneck(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "UrbanSim: The Bottleneck"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        cpu = pipeline_block("CPU", fill="#FEE2E2", stroke=RED_ERROR, width=1.8)
        gpu = pipeline_block("GPU", fill="#C8DCFA", stroke=ACCENT_BLUE, width=1.8)
        cpu.move_to(LEFT * 3.0)
        gpu.move_to(RIGHT * 0.5)
        transfer = DoubleArrow(cpu.get_right() + RIGHT * 0.05, gpu.get_left() + LEFT * 0.05, fill_color=RED_ERROR, thickness=3.0, buff=0.06) if False else Arrow(cpu.get_right(), gpu.get_left(), fill_color=RED_ERROR, thickness=3.0, buff=0.06)
        transfer_lbl = Text("Transfer\\nbottleneck", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2, color=RED_ERROR)
        transfer_lbl.next_to(transfer, UP, buff=0.1)
        self.play(FadeIn(cpu), FadeIn(gpu))
        self.play(ShowCreation(transfer), FadeIn(transfer_lbl))
        self.play(Flash(transfer, color=RED_ERROR, line_length=0.25, num_lines=8))
        bar = Rectangle(width=5.5, height=0.8, fill_color=RED_ERROR, fill_opacity=0.25, stroke_color=RED_ERROR, stroke_width=2.0)
        bar.next_to(gpu, RIGHT, buff=0.3)
        bar_lbl = Text("180 GPU-days", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        bar_lbl.move_to(bar)
        self.play(FadeIn(bar), FadeIn(bar_lbl))
        self.wait(2)
        self._close()
''')

W("p05_s05b_urbansim_results.py", '''"""P05-S05b UrbanSim All-GPU Results."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, GREEN_FIX, GOLD_RICH, GOLD_KEY, ACCENT_BLUE, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    key_number, contribution_badge,
)
SCRIPT = """UrbanSim: 256 parallel environments, three hours instead of 180 days."""


class P05S05BUrbanSimResults(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "UrbanSim: 180 Days -> 3 Hours"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # 256 parallel env grid (16x16 tiles)
        grid = VGroup()
        for r in range(8):
            for c in range(16):
                sq = Square(side_length=0.28, fill_color=GREEN_FIX, fill_opacity=0.35, stroke_color=GREEN_FIX, stroke_width=0.8)
                sq.move_to(np.array([(c - 7.5) * 0.32, (r - 3.5) * 0.32 + 0.5, 0]))
                grid.add(sq)
        self.play(LaggedStart(*(FadeIn(s, scale=0.4) for s in grid), lag_ratio=0.005, run_time=1.5))
        env_lbl = Text("128 parallel environments (subset shown)", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=GREEN_FIX)
        env_lbl.next_to(grid, DOWN, buff=0.15)
        self.play(FadeIn(env_lbl))
        kns = VGroup(
            key_number("3h", "vs 180 GPU-days", color=GOLD_RICH),
            key_number("2620 FPS", "simulation throughput", color=GOLD_RICH),
        )
        kns.arrange(RIGHT, buff=1.5).to_edge(DOWN, buff=0.4)
        self.play(LaggedStart(*(FadeIn(k, scale=1.2) for k in kns), lag_ratio=0.3))
        self.play(*(Flash(k[0], color=GOLD_RICH, line_length=0.2, num_lines=8) for k in kns))
        self.wait(2)
        self._close()
''')

W("p05_s06a_citywalker.py", '''"""P05-S06a CityWalker Dataset."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, GOLD_KEY, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    key_number, pedestrian_icon,
)
SCRIPT = """CityWalker captures pedestrian behavior in context — 30 hours, 120K pedestrians, 227 cities."""


class P05S06ACityWalker(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "CityWalker Dataset"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # World map dots — simplified as ellipse + scattered dots
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/spheres_talk/random_puzzles.py:18 DotHistory
        map_bg = Ellipse(width=9.5, height=4.5, fill_color="#F1F5F9", fill_opacity=0.4, stroke_color="#CBD5E1", stroke_width=1.5)
        map_bg.move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(map_bg))
        rng = np.random.RandomState(42)
        city_dots = VGroup()
        for _ in range(60):
            x = rng.uniform(-4.5, 4.5)
            y = rng.uniform(-1.8, 1.8)
            if x**2 / 20.25 + y**2 / 5.0625 < 1:
                d = Dot(radius=0.07, color=ACCENT_PINK)
                d.move_to(np.array([x, y + 0.3, 0]))
                city_dots.add(d)
        self.play(LaggedStart(*(FadeIn(d, scale=0.3) for d in city_dots), lag_ratio=0.03, run_time=1.5))
        kns = VGroup(
            key_number("30h", "video captured", color=GOLD_RICH),
            key_number("120K", "pedestrians", color=GOLD_RICH),
            key_number("227", "cities worldwide", color=GOLD_RICH),
        )
        kns.arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.4)
        self.play(LaggedStart(*(FadeIn(k, scale=1.1) for k in kns), lag_ratio=0.2))
        self.wait(2)
        self._close()
''')

W("p05_s06b_pedgen.py", '''"""P05-S06b PedGen diffusion model."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, PURPLE_MODEL, ACCENT_GREEN,
    CYAN_RADAR, INK_DARK, FONT_PRIMARY, SIZE_LABEL,
    pipeline_block, pipeline_arrow, pedestrian_icon,
)
SCRIPT = """PedGen is a diffusion model conditioned on scene, body, and goal. Three inputs, one walker."""


class P05S06BPedGen(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "PedGen: Diffusion Model"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # 3 inputs
        inputs = [
            pipeline_block("Scene Voxel", fill="#C8DCFA", stroke="#2563EB"),
            pipeline_block("SMPL Body", fill="#E0D7FF", stroke=PURPLE_MODEL),
            pipeline_block("Goal", fill="#C8EDD0", stroke=ACCENT_GREEN),
        ]
        inp_grp = VGroup(*inputs).arrange(DOWN, buff=0.3).move_to(LEFT * 3.8)
        diffusion = pipeline_block("Diffusion\\nModel", fill="#F9C8D8", stroke=ACCENT_PINK, width=2.5, height=1.5)
        diffusion.move_to(ORIGIN)
        self.play(LaggedStart(*(FadeIn(b) for b in inputs), lag_ratio=0.15))
        self.play(FadeIn(diffusion))
        for b in inputs:
            arr = pipeline_arrow(b, diffusion)
            self.add(arr)
        # Noise particles -> clean walker
        noise_dots = VGroup()
        rng = __import__("numpy").random.RandomState(7)
        for _ in range(20):
            d = Dot(radius=0.06, color=CYAN_RADAR)
            d.move_to(diffusion.get_right() + __import__("numpy").array([rng.uniform(0.2, 0.8), rng.uniform(-0.5, 0.5), 0]))
            noise_dots.add(d)
        self.play(LaggedStart(*(FadeIn(d, scale=0.3) for d in noise_dots), lag_ratio=0.04, run_time=0.8))
        ped = pedestrian_icon(color=ACCENT_PINK).scale(1.2)
        ped.move_to(RIGHT * 3.5)
        arr_out = pipeline_arrow(diffusion, ped, color=ACCENT_PINK)
        self.play(LaggedStart(*(FadeOut(d) for d in noise_dots), lag_ratio=0.03, run_time=0.6))
        self.play(ShowCreation(arr_out), GrowFromCenter(ped))
        cap = Text("noise  ->  anatomically realistic human walker",
                   font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
''')

W("p05_s07_zombie_to_alive.py", '''"""P05-S07 Zombie City -> Human-Centric Physical AI."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GREEN_FIX, INK_MID, INK_LIGHT, GOLD_RICH,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL,
    pedestrian_icon, write_chiseled,
)
SCRIPT = """Without human modeling, bodies walk through each other. PedGen and CityWalker make it alive."""


class P05S07ZombieToAlive(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Zombie City -> Human-Centric"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # Beat 1 — zombie city: grey squares, straight lines, pass-through
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2020/covid.py:723 ViralSpreadModelWithClusters
        rng = np.random.RandomState(11)
        n_zombies = 16
        zombies = VGroup()
        zombie_dirs = []
        for i in range(n_zombies):
            x = rng.uniform(-5.0, 5.0)
            y = rng.uniform(-2.2, 2.2)
            sq = Square(side_length=0.22, fill_color="#6B7280", fill_opacity=0.85, stroke_width=0)
            sq.move_to(np.array([x, y, 0]))
            zombies.add(sq)
            angle = rng.uniform(0, TAU)
            zombie_dirs.append(np.array([np.cos(angle), np.sin(angle), 0]) * 1.2)
        zombie_lbl = Text("Zombie City", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_MID)
        zombie_lbl.move_to(DOWN * 2.8)
        self.play(LaggedStart(*(FadeIn(z, scale=0.5) for z in zombies), lag_ratio=0.05, run_time=0.8))
        self.play(FadeIn(zombie_lbl))
        # Straight-line movement (zombie = no collision avoidance)
        self.play(*(z.animate(run_time=1.5, rate_func=linear).shift(d) for z, d in zip(zombies, zombie_dirs)))

        # Beat 2 — all freeze
        self.play(FadeOut(zombie_lbl))
        dim = Rectangle(width=16, height=9, fill_color="#000000", fill_opacity=0.45, stroke_width=0)
        self.play(FadeIn(dim, run_time=0.5))
        self.wait(0.5)

        # Beat 3 — each square transforms: square -> stick figure, gray -> PINK, organic path
        alive_peds = VGroup()
        transform_anims = []
        for z in zombies:
            ped = pedestrian_icon(color=ACCENT_PINK).scale(0.9)
            ped.move_to(z.get_center())
            alive_peds.add(ped)
            transform_anims.append(ReplacementTransform(z, ped, run_time=0.6))
        self.play(FadeOut(dim, run_time=0.4))
        self.play(LaggedStart(*transform_anims, lag_ratio=0.05, run_time=2.0))

        # Organic movement with avoidance
        self.play(*(
            p.animate(run_time=1.8, rate_func=smooth)
            .shift(np.array([np.cos(i * TAU / n_zombies + 0.3) * 0.8,
                             np.sin(i * TAU / n_zombies + 0.3) * 0.6, 0]))
            for i, p in enumerate(alive_peds)
        ))

        # Beat 4 — label transform
        alive_lbl = Text("Human-Centric Physical AI", font=FONT_PRIMARY, font_size=SIZE_H1, color=GREEN_FIX, weight=BOLD)
        alive_lbl.move_to(DOWN * 2.8)
        self.play(FadeIn(alive_lbl))
        self.wait(2)
        self._close()
''')

W("p05_s08_vid2sim.py", '''"""P05-S08 Vid2Sim pipeline."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, GOLD_RICH, CYAN_RADAR, ACCENT_GREEN, PURPLE_MODEL,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL,
    pipeline_block, pipeline_arrow, vehicle_icon,
)
SCRIPT = """Vid2Sim turns a city-tour video into a simulator: gaussians for visuals, mesh for physics."""


class P05S08Vid2Sim(StudioScene):
    PART_NUM = 5
    SCENE_TITLE = "Vid2Sim"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # Pipeline: Video -> Gaussian Splats -> Mesh -> Sim
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/spheres_talk/volumes.py:365
        video_block = pipeline_block("City-tour\\nVideo", fill="#C8DCFA", stroke="#2563EB")
        splat_block = pipeline_block("3D Gaussian\\nSplats", fill="#E0D7FF", stroke=PURPLE_MODEL)
        mesh_block = pipeline_block("Mesh\\nWireframe", fill="#D1FAE5", stroke=ACCENT_GREEN)
        sim_block = pipeline_block("Interactive\\nSimulator", fill="#FAE3B0", stroke="#D97706")
        pipeline = VGroup(video_block, splat_block, mesh_block, sim_block)
        pipeline.arrange(RIGHT, buff=0.7).move_to(UP * 0.5)
        self.play(LaggedStart(*(FadeIn(b) for b in pipeline), lag_ratio=0.2))
        arrows = VGroup(*(pipeline_arrow(pipeline[i], pipeline[i + 1]) for i in range(3)))
        self.play(LaggedStart(*(ShowCreation(a) for a in arrows), lag_ratio=0.15))
        # Gaussian splat visualization: colored dots cluster
        rng = __import__("numpy").random.RandomState(3)
        splats = VGroup()
        colors = [CYAN_RADAR, GOLD_RICH, ACCENT_GREEN, PURPLE_MODEL]
        for i in range(30):
            d = Dot(radius=0.08, color=colors[i % 4])
            d.move_to(__import__("numpy").array([rng.uniform(-1.5, 1.5), rng.uniform(-0.4, 0.2) - 0.8, 0]))
            d.set_opacity(rng.uniform(0.5, 0.9))
            splats.add(d)
        self.play(LaggedStart(*(FadeIn(d, scale=0.3) for d in splats), lag_ratio=0.03, run_time=0.8))
        robot = vehicle_icon(color=ACCENT_GREEN, scale=0.8).move_to(__import__("numpy").array([1.5, -0.8, 0]))
        robot_path = Line(__import__("numpy").array([0.0, -0.8, 0]), __import__("numpy").array([2.5, -0.8, 0]))
        self.play(GrowFromCenter(robot))
        self.play(robot.animate(run_time=1.0, rate_func=smooth).move_to(__import__("numpy").array([2.5, -0.8, 0])))
        cap = Text("video  ->  playground", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
''')

print("Batch 1 done (S01-S08)")
