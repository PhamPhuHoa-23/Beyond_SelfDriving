# beyond/scenes/part01/p01_s05_fm_empower.py
# ─────────────────────────────────────────────────────────────────
# P1-05  FM EMPOWER AV  (~50s)
#
# Hub-and-spoke diagram. Trung tâm: hexagon "Foundation Models".
# Trái: 4 nguồn FM (VFM, VGM, LLM, MLLM).
# Phải: 5 nhu cầu AV — E2E Driving Stack nổi bật GOLD nhất.
# Data packets (hexagon nhỏ) chạy liên tục left→hub→right.
# Kết: subtitle + bridge question.
#
# Render:  manim -ql "beyond/scenes/part01/p01_s05_fm_empower.py" P01S05FmEmpower
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, glow_pulse, node_block,
    BG_SPACE, BG_PANEL,
    GOLD, GOLD_GLOW, CYAN_NEON, P1_FOUNDATION,
    GREEN_SIGNAL, BLUE_ELECTRIC,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=17)

# ── Layout ─────────────────────────────────────────────────────────
HUB_POS   = ORIGIN
LEFT_X    = -5.0
RIGHT_X   =  5.0

SOURCES = [
    ("VFM",  "SAM · DINO · CLIP",   P1_FOUNDATION),
    ("VGM",  "Wan · Cosmos",         "#9B59B6"),
    ("LLM",  "GPT · Llama",          BLUE_ELECTRIC),
    ("MLLM", "Gemma3 · Qwen3-VL",    CYAN_NEON),
]
TARGETS = [
    ("Auto-labeling",     TEXT_DIM,       False),
    ("Scenario Gen",      TEXT_DIM,       False),
    ("Sensor Simulation", TEXT_DIM,       False),
    ("Vehicle Interface", TEXT_DIM,       False),
    ("E2E Driving Stack", GOLD,           True),   # highlighted
]

def _source_node(label: str, sub: str, color: str, pos) -> VGroup:
    bg = RoundedRectangle(corner_radius=0.12, width=2.0, height=0.65,
                          fill_color=BG_PANEL, fill_opacity=1.0,
                          stroke_color=color, stroke_width=1.4)
    bg.move_to(pos)
    t1 = Text(label, font_size=SIZE_MICRO + 2, color=color,
              font=FONT_PRIMARY, weight=BOLD).move_to(pos + UP * 0.10)
    t2 = Text(sub,   font_size=SIZE_MICRO - 1, color=TEXT_GHOST,
              font=FONT_PRIMARY).move_to(pos + DOWN * 0.14)
    return VGroup(bg, t1, t2)

def _target_node(label: str, color: str, highlight: bool, pos) -> VGroup:
    bw = 2.2 if highlight else 2.0
    bh = 0.68 if highlight else 0.60
    sw = 2.0 if highlight else 1.3
    bg = RoundedRectangle(corner_radius=0.12, width=bw, height=bh,
                          fill_color=BG_PANEL, fill_opacity=1.0,
                          stroke_color=color, stroke_width=sw)
    bg.move_to(pos)
    t = Text(label, font_size=SIZE_MICRO + (2 if highlight else 1),
             color=color, font=FONT_PRIMARY,
             weight=BOLD if highlight else NORMAL)
    t.move_to(pos)
    return VGroup(bg, t)

def _hex_packet(color: str) -> RegularPolygon:
    return RegularPolygon(n=6, radius=0.055, color=color,
                          fill_opacity=0.90, stroke_width=0)

class P01S05FmEmpower(BeyondScene):
    PART_COLOR = P1_FOUNDATION

    def construct(self):
        title_mob, sep = self.open("Foundation Models Empower AV")
        self.wait(0.2)

        # ── Hub hexagon ───────────────────────────────────────
        hub_hex = RegularPolygon(n=6, radius=0.70,
                                 fill_color="#0D1829", fill_opacity=1.0,
                                 stroke_color=P1_FOUNDATION, stroke_width=2.2)
        hub_hex.move_to(HUB_POS)
        hub_lbl = Text("Foundation\nModels", font_size=SIZE_MICRO + 3,
                       color=P1_FOUNDATION, font=FONT_PRIMARY, weight=BOLD,
                       line_spacing=0.40)
        hub_lbl.move_to(HUB_POS)
        hub = VGroup(hub_hex, hub_lbl)

        self.play(GrowFromCenter(hub_hex, run_time=0.55))
        self.play(FadeIn(hub_lbl, run_time=0.30))
        self.play(glow_pulse(hub_hex, P1_FOUNDATION, n_pulses=2, run_time=0.40))
        self.wait(0.15)

        # ── Source nodes (left) ────────────────────────────────
        n_src = len(SOURCES)
        src_ys = np.linspace(1.8, -1.8, n_src)
        src_nodes = VGroup()
        src_positions = []
        for i, (lbl, sub, col) in enumerate(SOURCES):
            pos = np.array([LEFT_X, src_ys[i], 0])
            nd = _source_node(lbl, sub, col, pos)
            src_nodes.add(nd)
            src_positions.append(pos)

        self.play(
            LaggedStart(*[FadeIn(nd, shift=RIGHT*0.12, run_time=0.35)
                          for nd in src_nodes], lag_ratio=0.18),
        )

        # Lines from source to hub
        src_lines = VGroup(*[
            Line(np.array([LEFT_X + 1.02, src_positions[i][1], 0]),
                 HUB_POS + LEFT * 0.72,
                 stroke_color=SOURCES[i][2], stroke_width=0.8,
                 stroke_opacity=0.40)
            for i in range(n_src)
        ])
        self.play(
            LaggedStart(*[Create(l, run_time=0.30) for l in src_lines],
                        lag_ratio=0.12),
        )

        # ── Target nodes (right) ──────────────────────────────
        n_tgt = len(TARGETS)
        tgt_ys = np.linspace(2.0, -2.0, n_tgt)
        tgt_nodes = VGroup()
        tgt_positions = []
        for i, (lbl, col, hi) in enumerate(TARGETS):
            pos = np.array([RIGHT_X, tgt_ys[i], 0])
            nd = _target_node(lbl, col, hi, pos)
            tgt_nodes.add(nd)
            tgt_positions.append(pos)

        self.play(
            LaggedStart(*[FadeIn(nd, shift=LEFT*0.12, run_time=0.35)
                          for nd in tgt_nodes], lag_ratio=0.15),
        )

        # Lines from hub to targets
        tgt_lines = VGroup(*[
            Line(HUB_POS + RIGHT * 0.72,
                 np.array([RIGHT_X - 1.12, tgt_positions[i][1], 0]),
                 stroke_color=TARGETS[i][1], stroke_width=0.8,
                 stroke_opacity=0.40)
            for i in range(n_tgt)
        ])
        self.play(
            LaggedStart(*[Create(l, run_time=0.28) for l in tgt_lines],
                        lag_ratio=0.10),
        )

        # ── Data packet animation — 3 waves ──────────────────
        # Each packet travels: source → hub → target, with matching colors
        route_pairs = [
            (0, 4, GOLD),           # VFM → E2E Driving Stack
            (1, 2, "#9B59B6"),      # VGM → Sensor Simulation
            (2, 0, BLUE_ELECTRIC),  # LLM → Auto-labeling
            (3, 1, CYAN_NEON),      # MLLM → Scenario Gen
            (0, 3, P1_FOUNDATION),  # VFM → Vehicle Interface
        ]
        for _ in range(3):   # 3 waves for continuous feel
            wave_anims = []
            for s_idx, t_idx, color in route_pairs:
                pkt = _hex_packet(color)
                sp = src_positions[s_idx]
                tp = tgt_positions[t_idx]
                mid_l = np.array([LEFT_X + 1.02, sp[1], 0])
                mid_r = np.array([RIGHT_X - 1.12, tp[1], 0])

                path_l = Line(mid_l, HUB_POS)
                path_r = Line(HUB_POS, mid_r)

                wave_anims.append(
                    Succession(
                        pkt.animate(run_time=0.0).move_to(mid_l),
                        MoveAlongPath(pkt, path_l, run_time=0.38, rate_func=smooth),
                        Flash(HUB_POS, color=color, flash_radius=0.12,
                              num_lines=4, run_time=0.08),
                        MoveAlongPath(pkt, path_r, run_time=0.38, rate_func=smooth),
                        FadeOut(pkt, run_time=0.08),
                    )
                )
            self.play(LaggedStart(*wave_anims, lag_ratio=0.10))

        # Hub pulse after packets
        self.play(glow_pulse(hub_hex, GOLD, n_pulses=1, run_time=0.45))

        # ── E2E label shimmer ─────────────────────────────────
        e2e_node = tgt_nodes[-1]
        self.play(
            e2e_node.animate(run_time=0.30).set_stroke(GOLD_GLOW, width=2.8),
            Flash(tgt_positions[-1], color=GOLD,
                  flash_radius=0.55, num_lines=8, run_time=0.35),
        )
        self.wait(0.3)

        # ── Subtitle ──────────────────────────────────────────
        sub = Text("One large model → fine-tune for any AV task.",
                   font_size=SIZE_MICRO + 3, color=TEXT_DIM,
                   font=FONT_PRIMARY, slant=ITALIC)
        sub.to_edge(DOWN, buff=0.50)
        self.play(FadeIn(sub, shift=UP * 0.08, run_time=0.40))
        self.wait(1.0)

        self.close()
