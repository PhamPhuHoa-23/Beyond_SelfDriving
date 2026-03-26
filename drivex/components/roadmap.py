# drivex/components/roadmap.py
# ─────────────────────────────────────────────────────────────────
# Reusable 5-part roadmap strip used:
#   1. Full-size as SCENE I-03
#   2. Mini-strip at the bottom of every Part title scene
#
# Usage:
#   roadmap = RoadmapStrip(current_part=1)
#   self.play(roadmap.build_animation())
# ─────────────────────────────────────────────────────────────────

from manim import *
from .colors import COL_NAVY, COL_BLUE, COL_GOLD, COL_WHITE, COL_LIGHT_BLUE

PART_TITLES_SHORT = [
    "Individual\nReasoning",
    "Collective\nIntelligence",
    "Sim-to-Real\nBridge",
    "Efficiency &\nAdaptation",
    "Scalable\nPhysical AI",
]


class RoadmapStrip(VGroup):
    """
    5-node journey roadmap.

    Parameters
    ----------
    current_part   : int 1–5, which node to highlight (0 = none)
    mini           : if True, renders a compact bottom-strip version
    spine_width    : total horizontal span (Manim units)
    """

    def __init__(
        self,
        current_part: int = 0,
        mini: bool = False,
        spine_width: float = 11.0,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.current_part = current_part
        self.mini = mini

        node_r = 0.18 if mini else 0.38
        label_fs = 11 if mini else 16
        title_fs = 10 if mini else 14
        spine_h = 0.025

        # ── Spine ────────────────────────────────────────────────
        spine = Line(
            LEFT * spine_width / 2,
            RIGHT * spine_width / 2,
            stroke_color=COL_WHITE,
            stroke_width=2,
        )

        # ── Nodes ────────────────────────────────────────────────
        # Odd parts (1,3,5) arc above, even (2,4) arc below
        node_positions = [
            LEFT * spine_width / 2 + RIGHT * spine_width * i / 4
            for i in range(5)
        ]

        nodes = VGroup()
        node_labels = VGroup()
        part_titles = VGroup()

        for i, (pos, title) in enumerate(zip(node_positions, PART_TITLES_SHORT)):
            part_num = i + 1
            above = (part_num % 2 == 1)  # odd above spine
            y_offset = node_r * 1.0 if above else -node_r * 1.0

            is_current = (part_num == current_part)
            fill_col = COL_GOLD if is_current else COL_BLUE
            stroke_col = COL_GOLD if is_current else COL_WHITE

            node = Circle(
                radius=node_r,
                fill_color=fill_col,
                fill_opacity=1,
                stroke_color=stroke_col,
                stroke_width=2,
            ).move_to(pos + UP * y_offset)

            num_label = Text(
                str(part_num),
                font_size=label_fs,
                color=COL_WHITE,
                weight=BOLD,
            ).move_to(node.get_center())

            title_y = node_r * 1.8 if above else -node_r * 1.8
            title_label = Text(
                title, font_size=title_fs, color=COL_LIGHT_BLUE
            ).move_to(pos + UP * (y_offset + title_y))

            nodes.add(VGroup(node, num_label))
            part_titles.add(title_label)

        # Tick marks between nodes
        ticks = VGroup()
        for i in range(4):
            mid = (node_positions[i] + node_positions[i + 1]) / 2
            tick = Line(mid + UP * 0.08, mid + DOWN * 0.08,
                        stroke_color=COL_WHITE, stroke_width=1.5)
            ticks.add(tick)

        self.spine = spine
        self.nodes = nodes
        self.part_titles = part_titles
        self.ticks = ticks

        self.add(spine, ticks, nodes, part_titles)

        if mini:
            self.scale(0.52)

    # ── Animation builders ────────────────────────────────────────

    def build_animation(self, lag: float = 0.12) -> AnimationGroup:
        """Full draw-in animation for SCENE I-03."""
        anims = [Create(self.spine)]
        for node_grp, title in zip(self.nodes, self.part_titles):
            anims.append(LaggedStart(
                Create(node_grp[0]),
                FadeIn(node_grp[1]),
                FadeIn(title),
                lag_ratio=0.2,
            ))
        anims.append(FadeIn(self.ticks))
        return LaggedStart(*anims, lag_ratio=lag)

    def highlight_node(self, part_num: int) -> AnimationGroup:
        """Highlight a specific node (pulse gold)."""
        idx = part_num - 1
        node_circle = self.nodes[idx][0]
        return Succession(
            node_circle.animate(rate_func=there_and_back, run_time=0.5)
                       .scale(1.25),
            node_circle.animate(run_time=0.2).set_fill(COL_GOLD),
        )
