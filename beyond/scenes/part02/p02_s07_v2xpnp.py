# beyond/scenes/part02/p02_s07_v2xpnp.py
# ─────────────────────────────────────────────────────────────────
# P2-07  V2XPNP FRAMEWORK  (~75s)
#
# 3-tầng architecture xuất hiện từng tầng:
#   Tầng 1 (top):    4 agents (Car A, Car B, Infra 1, Infra 2)
#   Tầng 2 (middle): One-step comm → Temporal Attn ↔ Spatial Attn
#                    → Spatio-temporal BEV
#   Tầng 3 (bottom): Detection | Prediction | Planning
#
# Data burst khi "One-step" xuất hiện: packets từ tất cả agents.
# Kết quả benchmark stamps in: 3 checkmarks.
#
# Render:  manim -ql "beyond/scenes/part02/p02_s07_v2xpnp.py" P02S07V2XPnP
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene,
    pipeline_block, pipeline_arrow,
    pipeline_block_entrance, pipeline_arrow_entrance,
    v2x_link_pulse, signal_ping, glow_pulse,
    BG_PANEL, BG_SPACE,
    P2_COOP, GOLD, CYAN_NEON, BLUE_ELECTRIC, P1_FOUNDATION,
    GREEN_SIGNAL, ORANGE_INFRA, TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

# ── Y-levels ──────────────────────────────────────────────────────
Y_TOP    =  2.6   # agent layer
Y_MID    =  0.5   # fusion layer
Y_BOT    = -1.8   # task output layer

def _agent_node(label: str, color: str) -> VGroup:
    c = Circle(radius=0.28, fill_color=color, fill_opacity=0.9,
               stroke_color=WHITE, stroke_width=1.4)
    t = Text(label, font_size=SIZE_MICRO - 1, color=WHITE,
             font=FONT_PRIMARY, weight=BOLD, line_spacing=0.38)
    t.move_to(c)
    return VGroup(c, t)


class P02S07V2XPnP(BeyondScene):
    PART_COLOR = P2_COOP

    def construct(self):
        title_mob, sep = self.open("V2XPnP — Plug-and-Play V2X Framework")
        self.wait(0.2)

        # ════════════════════════════════════════════════════════
        # TẦNG 1 — Agents
        # ════════════════════════════════════════════════════════
        layer1_label = Text("Multi-Agent Inputs",
                            font_size=SIZE_MICRO + 2, color=TEXT_DIM,
                            font=FONT_PRIMARY)
        layer1_label.move_to(LEFT * 5.8 + UP * Y_TOP)

        agents_data = [
            ("Car A",    CYAN_NEON),
            ("Car B",    BLUE_ELECTRIC),
            ("Infra 1",  ORANGE_INFRA),
            ("Infra 2",  ORANGE_INFRA),
        ]
        agent_xs = np.linspace(-4.5, 4.5, len(agents_data))
        agents = VGroup(*[
            _agent_node(lbl, col).move_to([x, Y_TOP, 0])
            for (lbl, col), x in zip(agents_data, agent_xs)
        ])

        self.play(FadeIn(layer1_label, shift=RIGHT * 0.08, run_time=0.25))
        self.play(
            LaggedStart(*[GrowFromCenter(a, run_time=0.25) for a in agents],
                        lag_ratio=0.15),
        )

        # V2X links between agents (dashed lines)
        links = VGroup(*[
            DashedLine(agents[i].get_center(), agents[j].get_center(),
                       stroke_color=P2_COOP, stroke_width=0.7,
                       stroke_opacity=0.35, dash_length=0.10)
            for i in range(len(agents)) for j in range(i+1, len(agents))
        ])
        self.play(
            LaggedStart(*[Create(l, run_time=0.25) for l in links],
                        lag_ratio=0.06),
        )
        self.wait(0.2)

        # ════════════════════════════════════════════════════════
        # TẦNG 2 — Fusion
        # ════════════════════════════════════════════════════════
        layer2_label = Text("Communication & Fusion",
                            font_size=SIZE_MICRO + 2, color=TEXT_DIM,
                            font=FONT_PRIMARY)
        layer2_label.move_to(LEFT * 5.8 + UP * Y_MID)
        self.play(FadeIn(layer2_label, shift=RIGHT * 0.08, run_time=0.25))

        # One-step block
        one_step = pipeline_block(
            "One-Step\nCommunication",
            width=2.4, height=0.85,
            border_color=P2_COOP, fill_color=BG_PANEL,
            font_size=SIZE_MICRO + 1,
        )
        one_step.move_to([0, Y_MID + 0.9, 0])
        self.play(pipeline_block_entrance(one_step, P2_COOP))

        # DATA BURST from all agents to one_step
        for a in agents:
            pkt_path = Line(a.get_center(), one_step.get_center())
            pkt = RegularPolygon(n=6, radius=0.055, color=P2_COOP,
                                 fill_opacity=0.9, stroke_width=0)
            pkt.move_to(a.get_center())
            self.play(
                MoveAlongPath(pkt, pkt_path, run_time=0.28, rate_func=smooth),
                FadeOut(pkt, run_time=0.08),
                run_time=0.35,
            )
        self.play(
            Flash(one_step.get_center(), color=P2_COOP,
                  flash_radius=0.55, num_lines=8, run_time=0.35),
        )

        # Temporal + Spatial attention
        arr_down = Arrow(one_step.get_bottom(), one_step.get_bottom() + DOWN * 0.5,
                         buff=0.0, color=P2_COOP, stroke_width=1.5,
                         tip_length=0.13)
        self.play(pipeline_arrow_entrance(arr_down, style="electric"))

        temporal = pipeline_block("Temporal\nAttention", width=2.2, height=0.80,
                                  border_color=BLUE_ELECTRIC,
                                  fill_color=BG_PANEL, font_size=SIZE_MICRO + 1)
        spatial  = pipeline_block("Spatial\nAttention",  width=2.2, height=0.80,
                                  border_color=CYAN_NEON,
                                  fill_color=BG_PANEL, font_size=SIZE_MICRO + 1)
        temporal.move_to([-2.0, Y_MID - 0.35, 0])
        spatial.move_to([ 2.0, Y_MID - 0.35, 0])

        self.play(
            pipeline_block_entrance(temporal, BLUE_ELECTRIC),
            pipeline_block_entrance(spatial,  CYAN_NEON),
        )

        # Double-headed arrow between temporal ↔ spatial
        ts_arrow = DoubleArrow(temporal.get_right(), spatial.get_left(),
                               buff=0.08, color=TEXT_DIM,
                               stroke_width=1.4, tip_length=0.14)
        self.play(Create(ts_arrow, run_time=0.30))

        # BEV output block
        arr_t_bev = Arrow(temporal.get_bottom(),
                          temporal.get_bottom() + DOWN * 0.6,
                          buff=0.0, color=BLUE_ELECTRIC,
                          stroke_width=1.5, tip_length=0.13)
        arr_s_bev = Arrow(spatial.get_bottom(),
                          spatial.get_bottom() + DOWN * 0.6,
                          buff=0.0, color=CYAN_NEON,
                          stroke_width=1.5, tip_length=0.13)
        self.play(
            pipeline_arrow_entrance(arr_t_bev, style="electric"),
            pipeline_arrow_entrance(arr_s_bev, style="electric"),
        )

        bev = pipeline_block("Spatio-Temporal\nBEV Representation",
                             width=3.8, height=0.80,
                             border_color=P2_COOP,
                             fill_color=BG_PANEL, font_size=SIZE_MICRO + 1)
        bev.move_to([0, Y_MID - 1.25, 0])
        self.play(pipeline_block_entrance(bev, P2_COOP))
        self.wait(0.2)

        # ════════════════════════════════════════════════════════
        # TẦNG 3 — Task outputs
        # ════════════════════════════════════════════════════════
        layer3_label = Text("Multi-Task Outputs",
                            font_size=SIZE_MICRO + 2, color=TEXT_DIM,
                            font=FONT_PRIMARY)
        layer3_label.move_to(LEFT * 5.8 + UP * Y_BOT)
        self.play(FadeIn(layer3_label, shift=RIGHT * 0.08, run_time=0.25))

        task_data = [
            ("3D Detection", CYAN_NEON),
            ("Motion Prediction", GOLD),
            ("Motion Planning", P1_FOUNDATION),
        ]
        task_xs = [-3.2, 0.0, 3.2]
        tasks = [
            pipeline_block(lbl, width=2.3, height=0.72,
                           border_color=col, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO + 1)
            .move_to([x, Y_BOT, 0])
            for (lbl, col), x in zip(task_data, task_xs)
        ]

        arr_bev_to_tasks = [
            Arrow(bev.get_bottom(),
                  np.array([x, Y_BOT + 0.38, 0]),
                  buff=0.05, color=task_data[i][1],
                  stroke_width=1.6, tip_length=0.14)
            for i, x in enumerate(task_xs)
        ]
        self.play(
            LaggedStart(*[
                Succession(
                    pipeline_arrow_entrance(arr, style="beam"),
                    pipeline_block_entrance(blk, task_data[i][1]),
                )
                for i, (blk, arr) in enumerate(zip(tasks, arr_bev_to_tasks))
            ], lag_ratio=0.20),
        )
        self.wait(0.4)

        # ── Benchmark stamps ──────────────────────────────────
        stamps = [
            ("✓  SOTA Detection",    CYAN_NEON,    tasks[0]),
            ("✓  SOTA Prediction",   GOLD,          tasks[1]),
            ("✓  Outperforms All",   GREEN_SIGNAL,  tasks[2]),
        ]
        for txt, col, blk in stamps:
            stamp_mob = Text(txt, font_size=SIZE_MICRO + 1,
                             color=col, font=FONT_PRIMARY, weight=BOLD)
            stamp_mob.next_to(blk, DOWN, buff=0.15)
            self.play(
                FadeIn(stamp_mob, scale=1.3, run_time=0.22),
                Flash(blk.get_center(), color=col,
                      flash_radius=0.45, num_lines=6, run_time=0.25),
            )
        self.wait(1.5)

        self.close()
