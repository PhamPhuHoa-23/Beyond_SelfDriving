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

W("p04_s07a_arithmetic_cost.py", '''"""P04-S07A: arithmetic and memory energy costs behind quantized inference."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, PASTEL_BLUE, PASTEL_GREEN,
    RED_ERROR, GREEN_FIX, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER,
    GOLD_RICH, INK_DARK, INK_MID, LINE_GRID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
)

SCRIPT = (
    "Why is neural network inference expensive on edge hardware? "
    "Neural networks are dominated by two operations: multiply-accumulate in "
    "fully connected and convolutional layers, and memory reads to load weights "
    "from off-chip memory. The energy costs are revealing. A 32-bit floating-point "
    "multiplication costs roughly 3.7 picojoules. A 32-bit memory access from DRAM "
    "costs approximately 640 picojoules — more than 170 times more expensive than "
    "the computation itself."
)


def label(text, size=SIZE_LABEL, color=INK_DARK, weight=NORMAL):
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def bit_strip(count, color, *, width=4.35, cell_height=0.27):
    gap = 0.025
    cell_width = (width - gap * (count - 1)) / count
    cells = VGroup()
    for _ in range(count):
        cell = RoundedRectangle(
            width=cell_width,
            height=cell_height,
            corner_radius=min(0.035, cell_width * 0.2),
        )
        cell.set_fill(color, opacity=0.92)
        cell.set_stroke(color, width=0)
        cells.add(cell)
    cells.arrange(RIGHT, buff=gap)
    return cells


def energy_bar(value, max_value, color, *, width=2.8):
    track = RoundedRectangle(width=width, height=0.26, corner_radius=0.08)
    track.set_fill(LINE_GRID, opacity=0.58)
    track.set_stroke(LINE_GRID, width=0)

    fill_width = max(0.07, width * value / max_value)
    fill = RoundedRectangle(width=fill_width, height=0.26, corner_radius=0.08)
    fill.set_fill(color, opacity=0.95)
    fill.set_stroke(color, width=0)
    fill.align_to(track, LEFT)
    return VGroup(track, fill)


def chip_icon(title, subtitle, color, *, width=1.72):
    body = RoundedRectangle(width=width, height=1.12, corner_radius=0.12)
    body.set_fill(color, opacity=0.1)
    body.set_stroke(color, width=2.0, opacity=0.9)

    pins = VGroup()
    for x in [-0.62, -0.2, 0.2, 0.62]:
        for y in [-0.65, 0.65]:
            pin = Line([x, y - 0.09, 0], [x, y + 0.09, 0])
            pin.set_stroke(color, width=2.0, opacity=0.75)
            pins.add(pin)
    for y in [-0.34, 0, 0.34]:
        for x in [-width / 2 - 0.1, width / 2 + 0.1]:
            pin = Line([x - 0.09, y, 0], [x + 0.09, y, 0])
            pin.set_stroke(color, width=2.0, opacity=0.75)
            pins.add(pin)

    title_mob = label(title, SIZE_LABEL, color, BOLD)
    subtitle_mob = label(subtitle, SIZE_CAPS - 1, INK_MID)
    copy = VGroup(title_mob, subtitle_mob)
    copy.arrange(DOWN, buff=0.05)
    copy.move_to(body)
    return VGroup(pins, body, copy)


class P04S07AArithmeticCost(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Arithmetic Energy Cost"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        divider = Line(UP * 2.3, DOWN * 2.8)
        divider.set_stroke(LINE_GRID, width=1.4, opacity=0.9)
        self.play(ShowCreation(divider), run_time=0.35)

        # Left: arithmetic cost from the original energy table.
        compute_title = label("COMPUTE  |  one multiply", SIZE_LABEL, INK_DARK, BOLD)
        compute_title.move_to(LEFT * 3.45 + UP * 2.12)
        compute_note = label("narrower operands switch less circuitry", SIZE_CAPS, INK_MID)
        compute_note.next_to(compute_title, DOWN, buff=0.07)
        self.play(FadeIn(compute_title), FadeIn(compute_note), run_time=0.45)

        fp32_name = label("FP32", SIZE_LABEL, RED_ERROR, BOLD)
        fp32_bits = bit_strip(32, RED_ERROR, width=4.35)
        fp32_bits.move_to(LEFT * 3.25 + UP * 0.88)
        fp32_name.next_to(fp32_bits, UP, aligned_edge=LEFT, buff=0.1)
        fp32_caption = label("32 bits", SIZE_CAPS, INK_MID)
        fp32_caption.next_to(fp32_bits, DOWN, buff=0.08)

        int8_name = label("INT8", SIZE_LABEL, GREEN_FIX, BOLD)
        int8_bits = bit_strip(8, GREEN_FIX, width=1.35)
        int8_bits.align_to(fp32_bits, LEFT)
        int8_bits.move_to([
            fp32_bits.get_left()[0] + int8_bits.get_width() / 2,
            -0.15,
            0,
        ])
        int8_name.next_to(int8_bits, UP, aligned_edge=LEFT, buff=0.1)
        int8_caption = label("8 bits", SIZE_CAPS, INK_MID)
        int8_caption.next_to(int8_bits, DOWN, buff=0.08)

        self.play(
            FadeIn(fp32_name),
            LaggedStart(*(FadeIn(bit, scale=0.6) for bit in fp32_bits),
                        lag_ratio=0.012, run_time=0.8),
            FadeIn(fp32_caption),
        )
        self.play(
            TransformFromCopy(fp32_name, int8_name),
            LaggedStart(*(FadeIn(bit, scale=0.6) for bit in int8_bits),
                        lag_ratio=0.04, run_time=0.55),
            FadeIn(int8_caption),
        )

        fp32_bar = energy_bar(3.7, 3.7, RED_ERROR)
        fp32_bar.move_to(LEFT * 3.25 + DOWN * 1.05)
        fp32_value = label("3.7 pJ", SIZE_LABEL, RED_ERROR, BOLD)
        fp32_value.next_to(fp32_bar, RIGHT, buff=0.15)
        fp32_op = label("FP32 MUL", SIZE_CAPS, INK_MID)
        fp32_op.next_to(fp32_bar, LEFT, buff=0.14)

        int8_bar = energy_bar(0.2, 3.7, GREEN_FIX)
        int8_bar.move_to(LEFT * 3.25 + DOWN * 1.68)
        int8_value = label("0.2 pJ", SIZE_LABEL, GREEN_FIX, BOLD)
        int8_value.next_to(int8_bar, RIGHT, buff=0.15)
        int8_op = label("INT8 MUL", SIZE_CAPS, INK_MID)
        int8_op.next_to(int8_bar, LEFT, buff=0.14)

        self.play(
            GrowFromEdge(fp32_bar[1], LEFT),
            FadeIn(fp32_bar[0]),
            FadeIn(fp32_op),
            FadeIn(fp32_value),
            run_time=0.65,
        )
        self.play(
            GrowFromEdge(int8_bar[1], LEFT),
            FadeIn(int8_bar[0]),
            FadeIn(int8_op),
            FadeIn(int8_value),
            run_time=0.45,
        )

        compute_ratio = VGroup(
            label("18.5x", SIZE_LABEL + 5, GREEN_FIX, BOLD),
            label("less arithmetic energy", SIZE_CAPS, INK_MID),
        )
        compute_ratio.arrange(DOWN, buff=0.02)
        compute_ratio.move_to(LEFT * 3.45 + DOWN * 2.48)
        self.play(FadeIn(compute_ratio, shift=0.08 * UP), run_time=0.45)

        # Right: memory hierarchy. This is a separate, much larger bottleneck.
        memory_title = label("MEMORY  |  move one 32-bit value", SIZE_LABEL, INK_DARK, BOLD)
        memory_title.move_to(RIGHT * 3.45 + UP * 2.12)
        memory_note = label("distance dominates energy", SIZE_CAPS, INK_MID)
        memory_note.next_to(memory_title, DOWN, buff=0.07)
        self.play(FadeIn(memory_title), FadeIn(memory_note), run_time=0.45)

        core = chip_icon("MAC", "compute core", ACCENT_BLUE, width=1.55)
        core.move_to(RIGHT * 3.55 + DOWN * 0.05)
        dram = chip_icon("DRAM", "off-chip", RED_ERROR)
        dram.move_to(RIGHT * 1.2 + UP * 0.95)
        sram = chip_icon("SRAM", "on-chip", GREEN_FIX)
        sram.move_to(RIGHT * 5.55 + UP * 0.95)

        dram_path = Arrow(
            dram.get_bottom(),
            core.get_left() + UP * 0.1,
            path_arc=0.35,
            buff=0.08,
            max_tip_length_to_length_ratio=0.1,
        )
        dram_path.set_stroke(RED_ERROR, width=3.0, opacity=0.82)
        dram_path.set_fill(RED_ERROR, opacity=0.82)

        sram_path = Arrow(
            sram.get_bottom(),
            core.get_right() + UP * 0.1,
            path_arc=-0.35,
            buff=0.08,
            max_tip_length_to_length_ratio=0.12,
        )
        sram_path.set_stroke(GREEN_FIX, width=3.0, opacity=0.82)
        sram_path.set_fill(GREEN_FIX, opacity=0.82)

        self.play(FadeIn(core), FadeIn(dram), FadeIn(sram), run_time=0.6)
        self.play(ShowCreation(dram_path), run_time=0.65)

        dram_packet = Square(side_length=0.18)
        dram_packet.set_fill(RED_ERROR, opacity=1.0)
        dram_packet.set_stroke(RED_ERROR, width=0)
        dram_packet.move_to(dram_path.get_start())
        self.add(dram_packet)
        self.play(MoveAlongPath(dram_packet, dram_path), run_time=0.8, rate_func=linear)

        dram_value = label("640 pJ", SIZE_LABEL + 3, RED_ERROR, BOLD)
        dram_value.move_to(RIGHT * 1.28 + DOWN * 1.35)
        dram_sub = label("DRAM access", SIZE_CAPS, INK_MID)
        dram_sub.next_to(dram_value, DOWN, buff=0.05)
        self.play(FadeIn(dram_value), FadeIn(dram_sub), run_time=0.35)

        self.play(ShowCreation(sram_path), run_time=0.45)
        sram_packet = Square(side_length=0.18)
        sram_packet.set_fill(GREEN_FIX, opacity=1.0)
        sram_packet.set_stroke(GREEN_FIX, width=0)
        sram_packet.move_to(sram_path.get_start())
        self.add(sram_packet)
        self.play(MoveAlongPath(sram_packet, sram_path), run_time=0.38, rate_func=linear)

        sram_value = label("5 pJ", SIZE_LABEL + 3, GREEN_FIX, BOLD)
        sram_value.move_to(RIGHT * 5.55 + DOWN * 1.35)
        sram_sub = label("SRAM access", SIZE_CAPS, INK_MID)
        sram_sub.next_to(sram_value, DOWN, buff=0.05)
        self.play(FadeIn(sram_value), FadeIn(sram_sub), run_time=0.35)

        memory_ratio = VGroup(
            label("128x", SIZE_LABEL + 5, GOLD_RICH, BOLD),
            label("more energy to fetch from DRAM", SIZE_CAPS, INK_MID),
        )
        memory_ratio.arrange(DOWN, buff=0.02)
        memory_ratio.move_to(RIGHT * 3.45 + DOWN * 2.48)
        self.play(
            FadeIn(memory_ratio, shift=0.08 * UP),
            Flash(dram_value, color=RED_ERROR, line_length=0.16, num_lines=8),
            run_time=0.55,
        )

        self.wait(1.5)
        self._close()
''')

W("p04_s07b_memory_bound.py", '''"""P04-S07B: Memory-bound inference, 4x memory savings, and arithmetic transition to addition."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene, BG_PAPER, PASTEL_BLUE, PASTEL_GREEN, PASTEL_AMBER,
    RED_ERROR, GREEN_FIX, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER,
    GOLD_RICH, INK_DARK, INK_MID, LINE_GRID, LINE_SEP,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, SIZE_BODY,
)

SCRIPT = (
    "This means inference on edge hardware is memory-bound, not compute-bound. "
    "The bottleneck is not running the arithmetic but loading the model parameters. "
    "Reducing the bit-width of weights from 32-bit float to 8-bit integer cuts the "
    "memory footprint by 4x, replaces multiplications with cheaper integer additions, "
    "and enables hardware accelerators designed specifically for INT8 operations on modern edge chips."
)


def label(text, size=SIZE_LABEL, color=INK_DARK, weight=NORMAL):
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def bit_strip(count, color, *, width=3.6, cell_height=0.22):
    gap = 0.02
    cell_width = (width - gap * (count - 1)) / count
    cells = VGroup()
    for _ in range(count):
        cell = RoundedRectangle(
            width=cell_width,
            height=cell_height,
            corner_radius=min(0.025, cell_width * 0.2),
        )
        cell.set_fill(color, opacity=0.92)
        cell.set_stroke(color, width=0)
        cells.add(cell)
    cells.arrange(RIGHT, buff=gap)
    return cells


def chip_icon(title, subtitle, color, *, width=1.55):
    body = RoundedRectangle(width=width, height=1.12, corner_radius=0.12)
    body.set_fill(color, opacity=0.1)
    body.set_stroke(color, width=2.0, opacity=0.9)

    pins = VGroup()
    for x in [-0.52, -0.16, 0.16, 0.52]:
        for y in [-0.65, 0.65]:
            pin = Line([x, y - 0.09, 0], [x, y + 0.09, 0])
            pin.set_stroke(color, width=2.0, opacity=0.75)
            pins.add(pin)
    for y in [-0.34, 0, 0.34]:
        for x in [-width / 2 - 0.1, width / 2 + 0.1]:
            pin = Line([x - 0.09, y, 0], [x + 0.09, y, 0])
            pin.set_stroke(color, width=2.0, opacity=0.75)
            pins.add(pin)

    title_mob = label(title, SIZE_LABEL, color, BOLD)
    subtitle_mob = label(subtitle, SIZE_CAPS - 1, INK_MID)
    copy = VGroup(title_mob, subtitle_mob)
    copy.arrange(DOWN, buff=0.05)
    copy.move_to(body)
    return VGroup(pins, body, copy)


class P04S07BMemoryBound(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "Memory-Bound Inference"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)



        # =========================================================================
        # LEFT COLUMN: Memory Funnel Bottleneck
        # =========================================================================
        left_center_x = -3.2

        # 1. DRAM Storage (at the top)
        dram_box = RoundedRectangle(width=2.0, height=0.6, corner_radius=0.08)
        dram_box.set_fill(PASTEL_AMBER, opacity=0.3)
        dram_box.set_stroke(ACCENT_AMBER, width=1.8, opacity=0.9)
        dram_box.move_to([left_center_x, 2.3, 0])
        dram_lbl = label("DRAM (off-chip)", SIZE_CAPS, ACCENT_AMBER, BOLD)
        dram_lbl.move_to(dram_box)

        # 2. Funnel geometry
        left_wall = VMobject()
        left_wall.set_points_as_corners([
            [left_center_x - 1.2, 1.8, 0],
            [left_center_x - 0.3, 0.4, 0],
            [left_center_x - 0.3, -1.5, 0]
        ])
        right_wall = VMobject()
        right_wall.set_points_as_corners([
            [left_center_x + 1.2, 1.8, 0],
            [left_center_x + 0.3, 0.4, 0],
            [left_center_x + 0.3, -1.5, 0]
        ])
        funnel = VGroup(left_wall, right_wall)
        funnel.set_stroke(INK_MID, width=3.0)

        # Bottleneck Indicator Label (completely out of the flow path)
        funnel_lbl = label("MEMORY BANDWIDTH", SIZE_CAPS - 2, INK_MID)
        funnel_lbl.next_to(dram_box, LEFT, buff=0.18)

        limit_lbl = label("BANDWIDTH LIMIT", SIZE_CAPS - 4, ACCENT_AMBER, BOLD)
        limit_lbl.move_to([left_center_x - 1.48, -0.5, 0])
        limit_arrow = Tex(r"\rightarrow", font_size=SIZE_CAPS)
        limit_arrow.set_color(ACCENT_AMBER)
        limit_arrow.next_to(limit_lbl, RIGHT, buff=0.08)
        bandwidth_indicator = VGroup(limit_lbl, limit_arrow)

        # 3. MAC Compute Core (at the bottom)
        core = chip_icon("MAC", "compute core", ACCENT_BLUE, width=1.4)
        core.move_to([left_center_x, -2.1, 0])
        core_body = core[1]

        core_status = label("IDLE (Starving)", SIZE_CAPS, RED_ERROR, BOLD)
        core_status.move_to([left_center_x, -2.9, 0])

        core_note = label("Compute is ready, but waiting for data", SIZE_CAPS - 4, INK_MID)
        core_note.next_to(core, RIGHT, buff=0.2)
        core_note.shift(DOWN * 0.1)

        self.play(
            FadeIn(dram_box), FadeIn(dram_lbl),
            ShowCreation(funnel), FadeIn(funnel_lbl),
            FadeIn(bandwidth_indicator),
            FadeIn(core), FadeIn(core_status), FadeIn(core_note),
            run_time=0.75
        )

        # =========================================================================
        # BEAT 1: FP32 Mode — High Latency, Bottleneck Flow
        # =========================================================================
        spawn_y = dram_box.get_bottom()[1] - 0.22

        fp32_blocks = VGroup()
        for i in range(3):
            blk = RoundedRectangle(width=0.5, height=0.4, corner_radius=0.06)
            blk.set_fill(RED_ERROR, opacity=0.9)
            blk.set_stroke(RED_ERROR, width=0)
            blk.move_to([left_center_x, spawn_y, 0])
            fp32_blocks.add(blk)

        self.play(
            fp32_blocks[0].animate.move_to([left_center_x, -0.1, 0]),
            fp32_blocks[1].animate.move_to([left_center_x, 0.4, 0]),
            fp32_blocks[2].animate.move_to([left_center_x, 0.9, 0]),
            run_time=0.8
        )
        self.wait(0.1)

        self.play(
            fp32_blocks[0].animate.move_to([left_center_x, -2.1, 0]),
            fp32_blocks[1].animate.move_to([left_center_x, -0.1, 0]),
            fp32_blocks[2].animate.move_to([left_center_x, 0.4, 0]),
            run_time=1.0,
            rate_func=linear
        )

        ripple = core_body.copy()
        ripple.set_stroke(RED_ERROR, width=2.0, opacity=0.9)
        ripple.set_fill(opacity=0)
        self.play(
            FadeOut(fp32_blocks[0], scale=0.6),
            ripple.animate(run_time=0.45, rate_func=smooth)
                  .scale(1.35)
                  .set_stroke(opacity=0),
            core_status.animate.set_color(RED_ERROR)
        )

        self.play(
            fp32_blocks[1].animate.move_to([left_center_x, -2.1, 0]),
            fp32_blocks[2].animate.move_to([left_center_x, -0.1, 0]),
            run_time=1.0,
            rate_func=linear
        )
        self.play(
            FadeOut(fp32_blocks[1], scale=0.6),
            Flash(core_body, color=RED_ERROR, line_length=0.15, num_lines=8),
            run_time=0.45
        )

        # =========================================================================
        # RIGHT COLUMN: Footprint & Spacing Definition
        # =========================================================================
        right_center_x = 3.5

        prec_title = label("WEIGHT PRECISION", SIZE_CAPS, INK_DARK, BOLD)
        prec_title.move_to([right_center_x, 2.1, 0])

        fp32_lbl_r = label("FP32 (32-bit float)", SIZE_CAPS - 1, RED_ERROR, BOLD)
        fp32_lbl_r.next_to(prec_title, DOWN, aligned_edge=LEFT, buff=0.22)
        fp32_lbl_r.shift(LEFT * 1.5)

        fp32_strip = bit_strip(32, RED_ERROR, width=3.2)
        fp32_strip.next_to(fp32_lbl_r, DOWN, aligned_edge=LEFT, buff=0.1)

        self.play(
            FadeIn(prec_title),
            FadeIn(fp32_lbl_r),
            LaggedStart(*(FadeIn(b, scale=0.6) for b in fp32_strip), lag_ratio=0.01, run_time=0.8)
        )

        # =========================================================================
        # BEAT 2: Transition to INT8 (Synchronized Left & Right)
        # =========================================================================
        int8_lbl_r = label("INT8 (8-bit integer)", SIZE_CAPS - 1, GREEN_FIX, BOLD)
        int8_lbl_r.next_to(fp32_strip, DOWN, aligned_edge=LEFT, buff=0.3)

        int8_strip = bit_strip(8, GREEN_FIX, width=0.8)
        int8_strip.next_to(int8_lbl_r, DOWN, aligned_edge=LEFT, buff=0.1)

        savings_note = label("4x smaller memory footprint", SIZE_CAPS, GREEN_FIX, BOLD)
        savings_note.next_to(int8_strip, RIGHT, buff=0.3)

        green_blocks = VGroup()
        for i in range(4):
            g_blk = RoundedRectangle(width=0.22, height=0.16, corner_radius=0.03)
            g_blk.set_fill(GREEN_FIX, opacity=0.9)
            g_blk.set_stroke(GREEN_FIX, width=0)
            g_blk.move_to([left_center_x, -0.1, 0])
            green_blocks.add(g_blk)

        active_status = label("ACTIVE (INT8 Path)", SIZE_CAPS, GREEN_FIX, BOLD)
        active_status.move_to(core_status)
        active_note = label("Fully utilized compute core", SIZE_CAPS - 4, GREEN_FIX, BOLD)
        active_note.move_to(core_note)

        self.play(
            FadeOut(fp32_blocks[2], scale=0.6),
            *(FadeIn(g, scale=0.6) for g in green_blocks),
            FadeIn(int8_lbl_r),
            LaggedStart(*(FadeIn(b, scale=0.6) for b in int8_strip), lag_ratio=0.03, run_time=0.4),
            FadeIn(savings_note, shift=UP * 0.1),
            Transform(core_status, active_status),
            Transform(core_note, active_note),
            run_time=0.85
        )

        self.play(
            green_blocks[0].animate.move_to([left_center_x - 0.12, -0.4, 0]),
            green_blocks[1].animate.move_to([left_center_x + 0.12, -0.4, 0]),
            green_blocks[2].animate.move_to([left_center_x - 0.12, -0.1, 0]),
            green_blocks[3].animate.move_to([left_center_x + 0.12, -0.1, 0]),
            run_time=0.4
        )

        self.play(
            green_blocks[0].animate.move_to([left_center_x - 0.12, -2.1, 0]),
            green_blocks[1].animate.move_to([left_center_x + 0.12, -2.1, 0]),
            green_blocks[2].animate.move_to([left_center_x - 0.12, -1.5, 0]),
            green_blocks[3].animate.move_to([left_center_x + 0.12, -1.5, 0]),
            core_body.animate.set_stroke(GREEN_FIX, width=2.4),
            run_time=0.45,
            rate_func=linear
        )
        self.play(
            FadeOut(green_blocks[0], scale=0.6),
            FadeOut(green_blocks[1], scale=0.6),
            Flash(core_body, color=GREEN_FIX, line_length=0.18, num_lines=10),
            run_time=0.3
        )
        self.play(
            green_blocks[2].animate.move_to([left_center_x - 0.12, -2.1, 0]),
            green_blocks[3].animate.move_to([left_center_x + 0.12, -2.1, 0]),
            run_time=0.3,
            rate_func=linear
        )
        self.play(
            FadeOut(green_blocks[2], scale=0.6),
            FadeOut(green_blocks[3], scale=0.6),
            Flash(core_body, color=GREEN_FIX, line_length=0.18, num_lines=10),
            run_time=0.3
        )

        # =========================================================================
        # BEAT 3: Arithmetic Shift (Multiplication vs Addition)
        # =========================================================================
        arith_title = label("ARITHMETIC SIMPLIFICATION", SIZE_CAPS, INK_DARK, BOLD)
        arith_title.move_to([right_center_x, -0.6, 0])

        fp32_op = VGroup(
            Circle(radius=0.24, stroke_color=RED_ERROR, stroke_width=2),
            label("\u00d7", SIZE_BODY + 4, RED_ERROR, BOLD)
        )
        fp32_op[1].move_to(fp32_op[0])
        fp32_op_lbl = label("FP32: 32-bit float operations (Expensive)", SIZE_CAPS - 1, INK_MID)
        fp32_op_group = VGroup(fp32_op, fp32_op_lbl).arrange(RIGHT, buff=0.2)
        fp32_op_group.next_to(arith_title, DOWN, aligned_edge=LEFT, buff=0.22)
        fp32_op_group.shift(LEFT * 1.3)

        int8_op = VGroup(
            Circle(radius=0.24, stroke_color=GREEN_FIX, stroke_width=2),
            label("+", SIZE_BODY, GREEN_FIX, BOLD)
        )
        int8_op[1].move_to(int8_op[0])
        int8_op_lbl = label("INT8: Cheap 8-bit integer ops (Simple)", SIZE_CAPS - 1, INK_MID)
        int8_op_group = VGroup(int8_op, int8_op_lbl).arrange(RIGHT, buff=0.2)
        int8_op_group.next_to(fp32_op_group, DOWN, aligned_edge=LEFT, buff=0.22)

        left_dots1 = VGroup()
        for _ in range(5):
            d = RoundedRectangle(width=0.16, height=0.11, corner_radius=0.03)
            d.set_fill(GREEN_FIX, opacity=0.95)
            d.set_stroke(GREEN_FIX, width=0)
            left_dots1.add(d)

        left_flow_anims1 = []
        for j, d in enumerate(left_dots1):
            d.move_to([left_center_x, spawn_y - j * 0.45, 0])
            left_flow_anims1.append(d.animate(run_time=1.3, rate_func=linear).shift(DOWN * 4.2))

        self.play(
            FadeIn(arith_title),
            FadeIn(fp32_op_group),
            LaggedStart(*left_flow_anims1, lag_ratio=0.15, run_time=1.3),
            run_time=1.3
        )
        self.remove(*left_dots1)
        self.wait(0.3)

        left_dots2 = VGroup()
        for _ in range(5):
            d = RoundedRectangle(width=0.16, height=0.11, corner_radius=0.03)
            d.set_fill(GREEN_FIX, opacity=0.95)
            d.set_stroke(GREEN_FIX, width=0)
            left_dots2.add(d)

        left_flow_anims2 = []
        for j, d in enumerate(left_dots2):
            d.move_to([left_center_x, spawn_y - j * 0.45, 0])
            left_flow_anims2.append(d.animate(run_time=1.3, rate_func=linear).shift(DOWN * 4.2))

        self.play(
            FadeIn(int8_op_group),
            Flash(int8_op[0], color=GREEN_FIX, line_length=0.12, num_lines=8),
            LaggedStart(*left_flow_anims2, lag_ratio=0.15, run_time=1.3),
            run_time=1.3
        )
        self.remove(*left_dots2)

        summary_badge = label(
            "Memory-bound bottleneck solved: 4x footprint reduction + cheaper INT8 additions",
            SIZE_CAPS,
            INK_DARK,
            BOLD,
        )
        summary_badge.to_edge(DOWN, buff=0.26)
        self.play(FadeIn(summary_badge, shift=UP * 0.08), run_time=0.75)

        self.wait(2.0)
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
