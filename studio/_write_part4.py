"""Write all Part 4 scene files."""
import os
import numpy as np

BASE = "studio/scenes/part04"
os.makedirs(BASE, exist_ok=True)


def W(name, code):
    path = os.path.join(BASE, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"wrote {name}")


W("p04_s01_title.py", '''"""P04-S01 Part 4 Title Card."""
from manimlib import *
from studio.components import (
    StudioScene, BG_TITLECARD, ACCENT_AMBER, GOLD_RICH, INK_LIGHT,
    FONT_PRIMARY, SIZE_CAPS, SIZE_LABEL, write_chiseled,
)
SCRIPT = """Part 4: From Pre-Training to Post-Training — with Seth Zhao."""


class P04S01Title(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "From Pre-Training to Post-Training"

    def construct(self):
        self.camera.background_color = BG_TITLECARD
        part_tag = Text("Part 04", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=ACCENT_AMBER)
        part_tag.to_corner(UR, buff=0.4)
        self.play(FadeIn(part_tag))
        line1 = Text("From Pre-Training", font=FONT_PRIMARY, font_size=52, color=ACCENT_AMBER, weight=BOLD)
        line2 = Text("to Post-Training", font=FONT_PRIMARY, font_size=44, color=GOLD_RICH)
        title = VGroup(line1, line2).arrange(DOWN, buff=0.2).move_to(UP * 0.5)
        self.play(LaggedStart(write_chiseled(line1, run_time=1.8), write_chiseled(line2, run_time=1.5), lag_ratio=0.5))
        speaker = Text("Seth Z. Zhao  ·  UCLA Mobility Lab", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_LIGHT)
        speaker.next_to(title, DOWN, buff=0.45)
        self.play(FadeIn(speaker))
        quote = Text('"A system that cannot run real-time is a demo."',
                     font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        quote.next_to(speaker, DOWN, buff=0.4)
        self.play(write_chiseled(quote, run_time=2.0))
        roadmap = self._roadmap_strip()
        self.play(FadeIn(roadmap))
        self.wait(2)
        self._close()
''')

W("p04_s02_v2x_overview.py", '''"""P04-S02 V2X Overview + 3 Bottlenecks."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_AMBER, RED_ERROR, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, contribution_badge,
)
SCRIPT = """V2X is no longer just research. But three bottlenecks block real deployment."""


class P04S02V2XOverview(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "V2X Deployment Bottlenecks"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # Quick recap: V2X stack
        recap = Text("V2X Cooperative Perception Stack",
                     font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID)
        recap.move_to(UP * 1.5)
        self.play(FadeIn(recap))
        usdot = contribution_badge("USDOT Smart Intersection Funding", color=ACCENT_AMBER)
        usdot.next_to(recap, DOWN, buff=0.3)
        self.play(FadeIn(usdot))
        # 3 bottleneck tags drop in red
        tags = ["Data", "Training", "Inference"]
        tag_mobs = VGroup()
        for name in tags:
            t = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
            bg = RoundedRectangle(width=t.get_width() + 0.5, height=t.get_height() + 0.25,
                                  corner_radius=0.12, fill_color=BG_PAPER, fill_opacity=1.0,
                                  stroke_color=RED_ERROR, stroke_width=2.0)
            t.move_to(bg)
            tag_mobs.add(VGroup(bg, t))
        tag_mobs.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.5)
        self.play(LaggedStart(*(FadeIn(t, shift=DOWN * 0.4) for t in tag_mobs), lag_ratio=0.2))
        cap = Text("Three bottlenecks block real deployment.",
                   font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
''')

W("p04_s03_annotation_cost.py", '''"""P04-S03 Annotation Cost Explosion."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_AMBER, ACCENT_GREEN,
    GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    axes_deploy, bar_reveal, key_number,
)
SCRIPT = """Datasets have grown 5x in two years — but annotation cost grew with them."""


class P04S03AnnotationCost(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Annotation Cost Explosion"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # 3 bars: V2V4Real 240K, DAIR-V2X 460K, V2X-Real 1.2M
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2020/covid.py:770 ShowLogisticCurve
        axes, axes_anim = axes_deploy(
            (0, 4, 1), (0, 1.3, 0.25), x_label="Dataset", y_label="Annotations (M)"
        )
        axes.scale(0.7).move_to(LEFT * 2.0 + DOWN * 0.3)
        self.play(axes_anim)
        # Normalized values: 0.24, 0.46, 1.2
        values = [0.24, 0.46, 1.2]
        colors = [ACCENT_BLUE, ACCENT_AMBER, ACCENT_GREEN]
        bar_anim = bar_reveal(axes, values, colors=colors)
        self.play(bar_anim)
        for i, (lbl, val) in enumerate(zip(["V2V4Real\\n240K", "DAIR-V2X\\n460K", "V2X-Real\\n1.2M"], values)):
            x_pt = axes.c2p(0.5 + i, 0)
            t = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_CAPS - 1, color=INK_MID)
            t.next_to(x_pt, DOWN, buff=0.1)
            self.add(t)
        brace_lbl = Text("5x in 2 years", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                         color=GOLD_RICH, weight=BOLD)
        brace_lbl.move_to(RIGHT * 3.5 + UP * 0.5)
        self.play(FadeIn(brace_lbl, scale=1.2))
        kn = key_number("5x", "annotation growth in 2 years", color=GOLD_RICH)
        kn.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(kn))
        self.wait(2)
        self._close()
''')

W("p04_s04_coopre_masked.py", '''"""P04-S04 CooPre Masked Voxel Puzzle Hero — 75s."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, CYAN_RADAR,
    GOLD_RICH, GOLD_KEY, GREEN_FIX, RED_ERROR, INK_DARK, INK_MID, PASTEL_BLUE,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon, key_number, contribution_badge, axes_deploy, bar_reveal,
)
SCRIPT = """CooPre masks 40 percent of voxels and asks the model to fill them in. Half the labels, same performance."""


def bev_grid(rows=8, cols=8, cell=0.5, color=ACCENT_BLUE):
    """8x8 BEV voxel grid.
    Pattern adapted from: Source_manim_reference/3b1b_videos/_2026/spheres_talk/volumes.py:53 VolumeGrid
    """
    grid = VGroup()
    for r in range(rows):
        for c in range(cols):
            cell_sq = Square(side_length=cell, fill_color=color, fill_opacity=0.28,
                             stroke_color=color, stroke_width=1.2, stroke_opacity=0.6)
            cell_sq.move_to(np.array([(c - cols / 2 + 0.5) * cell,
                                      (r - rows / 2 + 0.5) * cell, 0]))
            grid.add(cell_sq)
    return grid


class P04S04CooPReMasked(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "CooPre: Masked Voxel Puzzle"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # Beat 1 — BEV grid + 2 agents
        grid = bev_grid(rows=8, cols=8, cell=0.52, color=ACCENT_BLUE)
        grid.move_to(ORIGIN + DOWN * 0.2)
        self.play(LaggedStart(*(FadeIn(v, scale=0.6) for v in grid), lag_ratio=0.01, run_time=1.2))

        agent_a = vehicle_icon(color=ACCENT_BLUE, scale=0.8)
        agent_b = vehicle_icon(color=ACCENT_TEAL, scale=0.8)
        agent_a.move_to(grid.get_corner(UL) + np.array([-0.3, 0.3, 0]))
        agent_b.move_to(grid.get_corner(DR) + np.array([0.3, -0.3, 0]))
        self.play(GrowFromCenter(agent_a), GrowFromCenter(agent_b))

        # LiDAR beams (Lines)
        beam_a = Line(agent_a.get_center(), grid.get_center(), stroke_color=CYAN_RADAR,
                      stroke_width=1.5, stroke_opacity=0.55)
        beam_b = Line(agent_b.get_center(), grid.get_center(), stroke_color=ACCENT_TEAL,
                      stroke_width=1.5, stroke_opacity=0.55)
        self.play(ShowCreation(beam_a), ShowCreation(beam_b))
        self.wait(0.5)

        # Beat 2 — mask 40% of voxels (about 26)
        rng = np.random.RandomState(17)
        n_cells = len(grid)
        mask_indices = sorted(rng.choice(n_cells, int(n_cells * 0.4), replace=False).tolist())
        mask_caption = Text("Can you fill in what you cannot see?",
                            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        mask_caption.to_edge(DOWN, buff=0.45)
        self.play(
            LaggedStart(*(grid[i].animate.set_fill(opacity=0.08).set_stroke(opacity=0.25)
                          for i in mask_indices), lag_ratio=0.05, run_time=2.0),
            FadeIn(mask_caption),
        )
        self.wait(0.8)

        # Beat 3 — particles from Agent B fly along curves to masked voxels
        reconstruct_anims = []
        for idx in mask_indices[:18]:  # animate first 18 for timing
            voxel = grid[idx]
            start = agent_b.get_center()
            mid = (start + voxel.get_center()) / 2 + np.array([rng.uniform(-0.3, 0.3),
                                                                rng.uniform(0.2, 0.5), 0])
            pkt = Dot(radius=0.065, color=ACCENT_TEAL)
            pkt.move_to(start)
            path = CubicBezier(start, mid, mid, voxel.get_center())
            reconstruct_anims.append(
                MoveAlongPath(pkt, path, run_time=0.8, rate_func=smooth)
            )
        self.play(LaggedStart(*reconstruct_anims, lag_ratio=0.07, run_time=3.5))

        # Restore masked voxels with bloom
        restore_anims = []
        for i in mask_indices:
            restore_anims.append(
                grid[i].animate(run_time=0.25, rate_func=there_and_back_with_pause)
                       .set_fill(opacity=1.0).set_stroke(opacity=1.0)
            )
        self.play(LaggedStart(*restore_anims, lag_ratio=0.04, run_time=2.5))
        self.wait(0.5)

        # Beat 4 — bars: 50% data -> same perf / 100% data -> +4% AP
        self.play(FadeOut(grid), FadeOut(agent_a), FadeOut(agent_b),
                  FadeOut(beam_a), FadeOut(beam_b), FadeOut(mask_caption))
        axes, axes_anim = axes_deploy(
            (0, 3, 1), (0, 1.0, 0.25), x_label="Data", y_label="AP"
        )
        axes.scale(0.65).move_to(LEFT * 2.0 + DOWN * 0.2)
        self.play(axes_anim)
        bar_anim = bar_reveal(axes, [0.78, 0.78, 0.82], colors=[INK_MID, GREEN_FIX, GOLD_RICH])
        self.play(bar_anim)
        for i, lbl in enumerate(["Baseline\\n100%", "CooPre\\n50%", "CooPre\\n100%"]):
            t = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_CAPS - 1, color=INK_MID)
            t.next_to(axes.c2p(0.5 + i, 0), DOWN, buff=0.1)
            self.add(t)
        kn = key_number("+4% AP", "100% data, double the labels -> same model", color=GOLD_RICH)
        kn.move_to(RIGHT * 3.5 + UP * 0.3)
        self.play(FadeIn(kn, scale=1.2))
        self.play(Flash(kn[0], color=GOLD_RICH, line_length=0.3, num_lines=10))

        # Badges
        badges = VGroup(
            contribution_badge("IROS 2025  ·  UCLA DriveX", color=GOLD_KEY),
            contribution_badge("CVPR 2025 Workshop", color=ACCENT_BLUE),
        )
        badges.arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.35)
        self.play(LaggedStart(*(FadeIn(b) for b in badges), lag_ratio=0.2))
        self.wait(2)
        # Pad to 75s
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header[0]], run_time=0.5)
        self.wait(62)
        self._close()
''')

W("p04_s05_turbotrain_landscape.py", '''"""P04-S05 TurboTrain Loss Landscape."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, GOLD_RICH, ACCENT_AMBER,
    INK_DARK, INK_MID, PURPLE_MODEL, ACCENT_TEAL, ACCENT_BLUE,
    FONT_PRIMARY, SIZE_LABEL, SIZE_H1,
    axes_deploy,
)
SCRIPT = """Three task gradients pull three directions. With pretraining plus gradient balancing, smooth spiral to optimum."""


class P04S05TurboTrainLandscape(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "TurboTrain: Loss Landscape"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # 2D loss-landscape via ParametricFunction contours (max 5)
        # Pattern adapted from: Source_manim_reference/welchlabs_videos/_2025/backprop_3/geometry_while_learning_2.py
        center = np.array([1.2, 0.8, 0])
        contours = VGroup()
        for i in range(1, 6):
            scale = 0.55 + i * 0.28
            ring = Ellipse(width=scale * 2.8, height=scale * 1.6,
                           stroke_color=INK_MID, stroke_width=1.2, stroke_opacity=0.35)
            ring.move_to(center)
            contours.add(ring)
        contours.move_to(ORIGIN + UP * 0.2)
        center_mob = Dot(radius=0.12, color=GOLD_RICH)
        center_mob.move_to(center)
        self.play(LaggedStart(*(ShowCreation(c) for c in contours), lag_ratio=0.1))
        self.play(GrowFromCenter(center_mob))
        gold_star = Text("*", font=FONT_PRIMARY, font_size=36, color=GOLD_RICH, weight=BOLD)
        gold_star.move_to(center)
        self.add(gold_star)

        # 3 gradient arrows tugging from different directions
        conflict_pt = center + np.array([-1.8, -0.8, 0])
        arrow_colors = [ACCENT_TEAL, GOLD_RICH, PURPLE_MODEL]
        arrow_dirs = [UP + RIGHT * 0.6, DOWN + RIGHT * 0.75, LEFT]
        grad_arrows = VGroup()
        for d, color in zip(arrow_dirs, arrow_colors):
            arr = Arrow(conflict_pt, conflict_pt + normalize(d) * 0.95,
                        fill_color=color, thickness=3, buff=0)
            grad_arrows.add(arr)
        conflict_dot = Dot(radius=0.1, color=RED_ERROR).move_to(conflict_pt)
        conflict_lbl = Text("conflict", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR)
        conflict_lbl.next_to(conflict_dot, DOWN, buff=0.1)
        self.play(GrowFromCenter(conflict_dot), FadeIn(conflict_lbl))
        self.play(LaggedStart(*(GrowArrow(a) for a in grad_arrows), lag_ratio=0.15))

        # Without TurboTrain: chaotic zigzag
        zigzag_pts = [conflict_pt + np.array([i * 0.22 + 0.08 * (-1 ** i), (i % 3 - 1) * 0.28, 0]) for i in range(8)]
        zigzag = VGroup(*(Line(zigzag_pts[i], zigzag_pts[i + 1], stroke_color=RED_ERROR, stroke_width=2, stroke_opacity=0.65) for i in range(7)))
        self.play(LaggedStart(*(ShowCreation(z) for z in zigzag), lag_ratio=0.08))
        self.wait(0.4)
        self.play(FadeOut(zigzag))

        # With TurboTrain: smooth spiral to optimum
        t_vals = np.linspace(0, 1, 80)
        spiral_pts = []
        for t in t_vals:
            angle = t * TAU * 2
            r = (1 - t) * 1.4
            spiral_pts.append(center + np.array([r * np.cos(angle) * 0.7, r * np.sin(angle) * 0.5, 0]))
        spiral = VMobject(stroke_color=GREEN_FIX, stroke_width=2.5)
        spiral.set_points_smoothly(spiral_pts)
        spiral.move_to(center)
        self.play(ShowCreation(spiral, run_time=2.5))

        cap = Text("120 epochs  ->  45 epochs  ·  no manual staging",
                   font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
''')

W("p04_s06_latency_chain.py", '''"""P04-S06 V2X Latency Chain."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, ACCENT_AMBER, CYAN_RADAR, GOLD_RICH, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, pipeline_arrow, pipeline_flow,
)
SCRIPT = """Every V2X frame has a latency budget. Each stage eats into it. FP32 inference does not fit."""


class P04S06LatencyChain(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "V2X Latency Budget"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # Chain of blocks with time budgets
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2023/optics_puzzles/wave_machine.py
        stages = [
            ("Local\\nInference", "30ms", ACCENT_AMBER),
            ("Communication", "20ms", CYAN_RADAR),
            ("Fusion\\nInference", "20ms", ACCENT_AMBER),
        ]
        blocks = []
        for name, budget, color in stages:
            b = pipeline_block(name, fill="#FAE3B0", stroke=color, width=2.5, height=1.0)
            blocks.append(b)
        row = VGroup(*blocks).arrange(RIGHT, buff=0.8).move_to(UP * 0.5)
        self.play(LaggedStart(*(FadeIn(b) for b in blocks), lag_ratio=0.2))
        arrows = VGroup(*(pipeline_arrow(blocks[i], blocks[i + 1]) for i in range(2)))
        self.play(ShowCreation(arrows))
        # Time budget labels
        for b, (_, budget, color) in zip(blocks, stages):
            t = Text(budget, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
            t.next_to(b, DOWN, buff=0.12)
            self.play(FadeIn(t, run_time=0.3))
        # FP32 bottleneck glow red
        bottleneck_lbl = Text("FP32: too slow", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                              color=RED_ERROR, weight=BOLD)
        bottleneck_lbl.move_to(blocks[2].get_center() + DOWN * 0.85)
        self.play(blocks[2].animate.set_stroke(RED_ERROR, width=3.5),
                  FadeIn(bottleneck_lbl))
        self.play(Flash(blocks[2], color=RED_ERROR, line_length=0.25, num_lines=8))
        total = Text("Total budget: <100ms  |  FP32 alone: 150ms+",
                     font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
        total.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(total))
        self.wait(2)
        self._close()
''')

W("p04_s07_arithmetic_cost.py", '''"""P04-S07 Arithmetic Cost — 640 pJ DRAM vs 5 pJ SRAM."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, GOLD_RICH, INK_DARK, INK_MID,
    ACCENT_AMBER,
    FONT_PRIMARY, SIZE_H1, SIZE_BODY, SIZE_LABEL, SIZE_CAPS,
    key_number,
)
SCRIPT = """FP32 multiplication is expensive. INT8 turns multiplies into adds — and shrinks the memory footprint."""


def energy_droplets(center, n, color, upward=True):
    drops = VGroup()
    rng = __import__("numpy").random.RandomState(99)
    for i in range(n):
        d = Dot(radius=0.055, color=color)
        angle = rng.uniform(0, 3.14) * (1 if upward else -1)
        d.move_to(center + 0.2 * numpy.array([numpy.cos(angle), numpy.sin(angle), 0]))
        drops.add(d)
    return drops

import numpy


class P04S07ArithmeticCost(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Arithmetic Energy Cost"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # Left: FP32 multiply — big, expensive
        fp32_box = RoundedRectangle(width=3.5, height=1.2, corner_radius=0.15,
                                    fill_color="#FEE2E2", fill_opacity=0.9,
                                    stroke_color=RED_ERROR, stroke_width=2.5)
        fp32_box.move_to(LEFT * 3.0 + UP * 0.8)
        fp32_lbl = Text("FP32  x  Multiply", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                        color=RED_ERROR, weight=BOLD)
        fp32_lbl.move_to(fp32_box)
        dram_lbl = Text("640 pJ  DRAM access", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                        color=RED_ERROR)
        dram_lbl.next_to(fp32_box, DOWN, buff=0.12)
        self.play(FadeIn(fp32_box), FadeIn(fp32_lbl))
        self.play(FadeIn(dram_lbl))
        # Energy droplets flying out
        drops_bad = energy_droplets(fp32_box.get_center(), 12, RED_ERROR)
        self.play(LaggedStart(*(d.animate(run_time=0.4, rate_func=rush_from)
                                 .shift(numpy.array([0, 0.8, 0]))
                                 .set_opacity(0)
                                for d in drops_bad), lag_ratio=0.05))

        # Right: INT8 add — small, cheap
        int8_box = RoundedRectangle(width=3.5, height=1.2, corner_radius=0.15,
                                    fill_color="#D1FAE5", fill_opacity=0.9,
                                    stroke_color=GREEN_FIX, stroke_width=2.5)
        int8_box.move_to(RIGHT * 3.0 + UP * 0.8)
        int8_lbl = Text("INT8  +  Add", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                        color=GREEN_FIX, weight=BOLD)
        int8_lbl.move_to(int8_box)
        sram_lbl = Text("5 pJ  SRAM access", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                        color=GREEN_FIX)
        sram_lbl.next_to(int8_box, DOWN, buff=0.12)
        self.play(FadeIn(int8_box), FadeIn(int8_lbl))
        self.play(FadeIn(sram_lbl))
        # Small efficient dots
        drops_good = energy_droplets(int8_box.get_center(), 3, GREEN_FIX)
        self.play(LaggedStart(*(d.animate(run_time=0.25, rate_func=rush_from)
                                 .shift(numpy.array([0, 0.5, 0]))
                                 .set_opacity(0)
                                for d in drops_good), lag_ratio=0.08))

        # Key comparison
        comp = Text("640 pJ DRAM  vs  5 pJ SRAM  =  128x energy savings",
                    font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        comp.move_to(DOWN * 1.8)
        self.play(FadeIn(comp, scale=1.05))
        kn = key_number("128x", "energy saved: DRAM -> SRAM + FP32 -> INT8", color=GOLD_RICH)
        kn.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(kn))
        self.wait(2)
        self._close()
''')

W("p04_s08_quantv2x.py", '''"""P04-S08 QuantV2X Compression Squeeze Hero — 65s."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, GOLD_RICH, GOLD_KEY,
    ACCENT_AMBER, CYAN_RADAR, INK_DARK, INK_MID, PURPLE_MODEL, PASTEL_AMBER,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, pipeline_arrow, key_number, contribution_badge,
)
SCRIPT = """QuantV2X quantizes both model and communication. 100 MB to 330 KB — three hundred times smaller."""


class P04S08QuantV2X(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "QuantV2X: Quantization Pipeline"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # Stage 1 — FP32 blob clogging channel
        big_blob = RoundedRectangle(width=3.2, height=2.0, corner_radius=0.2,
                                    fill_color=RED_ERROR, fill_opacity=0.18,
                                    stroke_color=RED_ERROR, stroke_width=2.5)
        big_blob.move_to(LEFT * 3.5 + UP * 0.5)
        fp32_lbl = Text("BEV Features\\n100 MB  FP32",
                        font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        fp32_lbl.move_to(big_blob)
        # V2X channel (blocked)
        channel_top = Line(LEFT * 1.0, RIGHT * 4.5, stroke_color=RED_ERROR, stroke_width=1.8)
        channel_bot = Line(LEFT * 1.0, RIGHT * 4.5, stroke_color=RED_ERROR, stroke_width=1.8)
        channel_top.move_to(UP * 0.15)
        channel_bot.move_to(DOWN * 0.15)
        blocked_lbl = Text("V2X channel — blocked", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                           color=RED_ERROR)
        blocked_lbl.move_to(RIGHT * 2.5 + DOWN * 0.5)
        self.play(FadeIn(big_blob), FadeIn(fp32_lbl))
        self.play(ShowCreation(channel_top), ShowCreation(channel_bot))
        self.play(FadeIn(blocked_lbl))
        self.wait(0.5)

        # 3-stage pipeline (top to bottom)
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2024/transformers/network_flow.py:55 get_block
        stage1 = pipeline_block("Full-Precision\\nPretraining", width=2.8, height=0.8,
                                fill=PASTEL_AMBER, stroke=ACCENT_AMBER)
        stage2 = pipeline_block("Codebook\\nLearning", width=2.8, height=0.8,
                                fill="#E0D7FF", stroke=PURPLE_MODEL)
        stage3 = pipeline_block("Post-Training\\nQuantization", width=2.8, height=0.8,
                                fill="#D1FAE5", stroke=GREEN_FIX)
        stages = VGroup(stage1, stage2, stage3).arrange(DOWN, buff=0.3)
        stages.move_to(LEFT * 3.5 + DOWN * 0.5)
        stage_arrows = VGroup(*(pipeline_arrow(stages[i], stages[i + 1]) for i in range(2)))
        for arr in stage_arrows:
            arr.put_start_and_end_on(stages[0 if stages.index(arr) == 0 else 1].get_bottom() if hasattr(stages, "index") else stages[0].get_bottom(), stages[1].get_top())

        self.play(FadeOut(big_blob), FadeOut(fp32_lbl))
        self.play(LaggedStart(*(FadeIn(s) for s in stages), lag_ratio=0.25))
        for i in range(2):
            arr = pipeline_arrow(stages[i], stages[i + 1])
            arr.put_start_and_end_on(stages[i].get_bottom(), stages[i + 1].get_top())
            self.play(ShowCreation(arr, run_time=0.35))

        # Beat: squeeze reveal — blob shrinks and color flips
        self.wait(0.5)
        squeeze_blob_start = RoundedRectangle(width=3.0, height=1.8, corner_radius=0.18,
                                              fill_color=RED_ERROR, fill_opacity=0.22,
                                              stroke_color=RED_ERROR, stroke_width=2.5)
        squeeze_blob_start.move_to(RIGHT * 3.0 + UP * 0.5)
        fp32_tag = Text("100 MB  FP32", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                        color=RED_ERROR, weight=BOLD)
        fp32_tag.move_to(squeeze_blob_start)
        self.play(FadeIn(squeeze_blob_start), FadeIn(fp32_tag))
        self.wait(0.3)
        # Squeeze animation
        int8_blob = RoundedRectangle(width=0.32, height=0.22, corner_radius=0.06,
                                     fill_color=GREEN_FIX, fill_opacity=0.8,
                                     stroke_color=GREEN_FIX, stroke_width=2.0)
        int8_blob.move_to(squeeze_blob_start.get_center())
        int8_tag = Text("0.33 MB  INT8", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                        color=GREEN_FIX, weight=BOLD)
        int8_tag.next_to(int8_blob, RIGHT, buff=0.25)
        self.play(
            Transform(squeeze_blob_start, int8_blob, run_time=2.0),
            FadeOut(fp32_tag, run_time=0.8),
        )
        self.play(FadeIn(int8_tag))

        # Channel opens — green packets flow
        channel_top.set_color(GREEN_FIX)
        channel_bot.set_color(GREEN_FIX)
        blocked_lbl.set_color(GREEN_FIX)
        self.play(
            channel_top.animate.set_stroke(GREEN_FIX, width=1.8),
            channel_bot.animate.set_stroke(GREEN_FIX, width=1.8),
            FadeOut(blocked_lbl),
        )
        free_lbl = Text("V2X channel — open!", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                        color=GREEN_FIX)
        free_lbl.move_to(RIGHT * 2.5 + DOWN * 0.5)
        # Packet pulses
        for _ in range(4):
            pkt = Dot(radius=0.07, color=CYAN_RADAR)
            pkt.move_to(channel_top.get_left() + RIGHT * 0.1)
            self.play(pkt.animate(run_time=0.5, rate_func=linear)
                      .move_to(channel_top.get_right() + LEFT * 0.1), FadeIn(free_lbl))
            self.remove(pkt)

        # Counter: 300x gold burst
        kn = key_number("300x", "smaller  100 MB FP32  ->  0.33 MB INT8", color=GOLD_RICH)
        kn.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(kn, scale=1.2))
        self.play(Flash(kn[0], color=GOLD_RICH, line_length=0.35, num_lines=12))
        self.wait(2)
        # Pad to 65s
        self.play(*[FadeOut(m) for m in self.mobjects if m is not header[0]], run_time=0.5)
        self.wait(51)
        self._close()
''')

W("p04_s09_efficiency_summary.py", '''"""P04-S09 Efficiency Summary: 3 gold cards."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_AMBER, GOLD_KEY, GOLD_RICH, GREEN_FIX,
    ACCENT_BLUE, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    contribution_badge, key_number,
)
SCRIPT = """Three efficiency contributions, three key numbers: 50% labels, 45 epochs, 300x."""


class P04S09EfficiencySummary(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Part 4 Efficiency Contributions"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        cards_data = [
            ("Data", "CooPre", "50% labels -> same performance", ACCENT_BLUE, "50%"),
            ("Training", "TurboTrain", "120 epochs -> 45 epochs", ACCENT_AMBER, "45 ep"),
            ("Inference", "QuantV2X", "100 MB -> 0.33 MB -> 300x smaller", GREEN_FIX, "300x"),
        ]
        cards = VGroup()
        for category, method, detail, color, key in cards_data:
            bg = RoundedRectangle(width=3.5, height=2.0, corner_radius=0.2,
                                  fill_color=BG_PAPER, fill_opacity=1.0,
                                  stroke_color=color, stroke_width=2.5)
            cat_lbl = Text(category, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
            meth_lbl = Text(method, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK)
            detail_lbl = Text(detail, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
            key_lbl = Text(key, font=FONT_PRIMARY, font_size=40, color=GOLD_RICH, weight=BOLD)
            inner = VGroup(cat_lbl, meth_lbl, detail_lbl, key_lbl).arrange(DOWN, buff=0.08)
            inner.move_to(bg)
            cards.add(VGroup(bg, inner))
        cards.arrange(RIGHT, buff=0.4).move_to(ORIGIN + DOWN * 0.2)
        self.play(LaggedStart(*(FadeIn(c, scale=0.85) for c in cards), lag_ratio=0.25))
        self.wait(2)
        self._close()
''')

W("p04_s10_bridge_to_p5.py", '''"""P04-S10 Bridge to Part 5."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_PINK, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL,
    write_chiseled,
)
SCRIPT = """Everything so far has been about cars. The world has robots, wheelchairs, scooters, and humans."""


class P04S10BridgeToP5(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Bridge to Part 5"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        recap = Text("Parts 2-4: all about cars.", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_MID)
        recap.move_to(UP * 0.8)
        self.play(FadeIn(recap))
        forward = Text(
            "But the world has delivery robots,\\nwheelchairs, scooters —\\nand the most unpredictable agent: humans.",
            font=FONT_PRIMARY, font_size=SIZE_H1, color=ACCENT_PINK,
        )
        forward.move_to(DOWN * 0.5)
        self.play(write_chiseled(forward, run_time=3.0))
        self.wait(1.5)
        self._close()
''')

print("All 10 Part 4 scenes written.")
