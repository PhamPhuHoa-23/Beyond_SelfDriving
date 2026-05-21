# beyond/scenes/part05/p05_s05_citywalker_pedgen.py
# ─────────────────────────────────────────────────────────────────
# P5-05  CITYWALKER + PEDGEN — ZOMBIE THÀNH NGƯỜI THẬT  (~70s)
#
# Left side: CityWalker dataset stats + world map dots.
# Right side: PedGen diffusion architecture.
#
# THE BIG TRANSFORM:
#   Zombie city (hình vuông xám, đi thẳng, xuyên nhau)
#   → Alive city (stick figure, màu pink, đường cong, né nhau).
#
# Render:  manim -ql "beyond/scenes/part05/p05_s05_citywalker_pedgen.py" P05S05CityWalker
# ─────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
import numpy as np
from manim import *
from beyond.components import (
    BeyondScene, pipeline_block, pipeline_block_entrance,
    glow_pulse,
    BG_SPACE, BG_PANEL,
    P5_PHYSICAL, GOLD, CYAN_NEON,
    GREEN_SIGNAL, RED_ALERT,
    TEXT_WHITE, TEXT_DIM, TEXT_GHOST,
    SIZE_LABEL, SIZE_MICRO, FONT_PRIMARY,
)

RNG = np.random.default_rng(seed=55)

N_PEDESTRIANS = 8
CITY_CENTER = np.array([-2.8, -0.5, 0.0])


def _zombie(pos: np.ndarray) -> VGroup:
    """Zombie pedestrian: gray square."""
    sq = Square(side_length=0.28, fill_color=TEXT_DIM, fill_opacity=0.85,
                stroke_width=0)
    sq.move_to(pos)
    return sq


def _human(pos: np.ndarray) -> VGroup:
    """Human pedestrian: simple stick figure, pink."""
    head = Circle(radius=0.10, fill_color=P5_PHYSICAL, fill_opacity=1,
                  stroke_color=WHITE, stroke_width=0.8).move_to(pos + UP * 0.24)
    body = Line(pos + UP * 0.14, pos + DOWN * 0.10,
                stroke_color=P5_PHYSICAL, stroke_width=1.4)
    la   = Line(pos + UP * 0.04, pos + LEFT * 0.14 + DOWN * 0.04,
                stroke_color=P5_PHYSICAL, stroke_width=1.0)
    ra   = Line(pos + UP * 0.04, pos + RIGHT * 0.14 + DOWN * 0.04,
                stroke_color=P5_PHYSICAL, stroke_width=1.0)
    ll   = Line(pos + DOWN * 0.10, pos + LEFT * 0.10 + DOWN * 0.28,
                stroke_color=P5_PHYSICAL, stroke_width=1.0)
    rl   = Line(pos + DOWN * 0.10, pos + RIGHT * 0.10 + DOWN * 0.28,
                stroke_color=P5_PHYSICAL, stroke_width=1.0)
    return VGroup(head, body, la, ra, ll, rl)


class P05S05CityWalker(BeyondScene):
    PART_COLOR = P5_PHYSICAL

    def construct(self):
        title_mob, sep = self.open("CityWalker + PedGen — Human-Centric AI")
        self.wait(0.2)

        # ── LEFT: CityWalker dataset stats ────────────────────
        stats = [
            ("227", "cities"),
            ("30.8h", "video data"),
            ("120,914", "pedestrians"),
            ("16,215", "scenes"),
        ]
        stat_mobs = VGroup()
        for i, (val, lbl) in enumerate(stats):
            val_t = Text(val, font_size=SIZE_LABEL + 4,
                         color=P5_PHYSICAL, font=FONT_PRIMARY, weight=BOLD)
            lbl_t = Text(lbl, font_size=SIZE_MICRO + 1,
                         color=TEXT_DIM, font=FONT_PRIMARY)
            grp = VGroup(val_t, lbl_t).arrange(DOWN, buff=0.06)
            stat_mobs.add(grp)

        stat_mobs.arrange_in_grid(rows=2, cols=2, buff=0.55)
        stat_mobs.move_to(LEFT * 3.8 + UP * 0.6)

        self.play(
            LaggedStart(*[
                Succession(
                    FadeIn(grp[0], scale=0.85, run_time=0.28),
                    FadeIn(grp[1], shift=UP * 0.06, run_time=0.22),
                )
                for grp in stat_mobs
            ], lag_ratio=0.20),
        )
        self.wait(0.3)

        # "More diversity than any prior dataset" label
        div_lbl = Text('"More diversity than any prior dataset."',
                       font_size=SIZE_MICRO + 2, color=TEXT_DIM,
                       font=FONT_PRIMARY, slant=ITALIC)
        div_lbl.next_to(stat_mobs, DOWN, buff=0.28)
        self.play(FadeIn(div_lbl, shift=UP * 0.06, run_time=0.35))
        self.wait(0.3)

        # ── RIGHT: PedGen architecture ────────────────────────
        input_labels = ["Scene Context\n(Voxel 3D)", "Body Context\n(SMPL skeleton)", "Goal\n(waypoint)"]
        input_blocks = VGroup(*[
            pipeline_block(lbl, width=2.0, height=0.72,
                           border_color=P5_PHYSICAL, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO)
            for lbl in input_labels
        ]).arrange(RIGHT, buff=0.25)
        input_blocks.move_to(RIGHT * 3.5 + UP * 2.2)

        self.play(
            LaggedStart(*[pipeline_block_entrance(b, P5_PHYSICAL)
                          for b in input_blocks], lag_ratio=0.20),
        )

        # Arrow down to diffusion model
        arr_down = Arrow(input_blocks.get_bottom(), input_blocks.get_bottom() + DOWN * 0.6,
                         buff=0.0, color=P5_PHYSICAL, stroke_width=1.5, tip_length=0.14)
        diff_box = pipeline_block("DIFFUSION MODEL\n(noise → structure)",
                                  width=3.2, height=0.78,
                                  border_color=GOLD, fill_color=BG_PANEL,
                                  font_size=SIZE_MICRO + 1)
        diff_box.move_to(RIGHT * 3.5 + UP * 1.0)
        self.play(Create(arr_down, run_time=0.25),
                  pipeline_block_entrance(diff_box, GOLD))
        self.play(glow_pulse(diff_box, GOLD, n_pulses=1, run_time=0.38))

        # Output: trajectory + pose
        arr_out = Arrow(diff_box.get_bottom(), diff_box.get_bottom() + DOWN * 0.5,
                        buff=0.0, color=GOLD, stroke_width=1.5, tip_length=0.14)
        out_labels = ["Generated\nTrajectory", "Generated\nPose"]
        out_blocks = VGroup(*[
            pipeline_block(lbl, width=1.8, height=0.65,
                           border_color=GREEN_SIGNAL, fill_color=BG_PANEL,
                           font_size=SIZE_MICRO)
            for lbl in out_labels
        ]).arrange(RIGHT, buff=0.3).move_to(RIGHT * 3.5 + DOWN * 0.1)
        self.play(Create(arr_out, run_time=0.20),
                  LaggedStart(*[FadeIn(b, shift=DOWN * 0.06, run_time=0.28)
                                for b in out_blocks], lag_ratio=0.20))
        self.wait(0.5)

        # ── FADE everything → THE BIG TRANSFORM ──────────────
        self.play(
            VGroup(stat_mobs, div_lbl, input_blocks, arr_down,
                   diff_box, arr_out, out_blocks)
            .animate(run_time=0.50).set_opacity(0.15),
        )

        # ── ZOMBIE CITY ───────────────────────────────────────
        zombie_pos = [
            CITY_CENTER + np.array([float(RNG.uniform(-2.2, 2.2)),
                                     float(RNG.uniform(-1.5, 1.5)), 0])
            for _ in range(N_PEDESTRIANS)
        ]
        zombies = VGroup(*[_zombie(p) for p in zombie_pos])

        self.play(
            LaggedStart(*[GrowFromCenter(z, run_time=0.18) for z in zombies],
                        lag_ratio=0.08),
        )

        zombie_label = Text("Zombie City", font_size=SIZE_LABEL,
                            color=RED_ALERT, font=FONT_PRIMARY, weight=BOLD)
        zombie_label.move_to(CITY_CENTER + UP * 2.3)
        self.play(FadeIn(zombie_label, run_time=0.28))

        # Zombies walk in straight lines (intersect each other — no avoidance)
        straight_dirs = [
            np.array([float(RNG.uniform(-0.6, 0.6)), float(RNG.uniform(-0.3, 0.3)), 0])
            for _ in range(N_PEDESTRIANS)
        ]
        self.play(
            LaggedStart(*[
                z.animate(run_time=0.60, rate_func=linear).shift(d)
                for z, d in zip(zombies, straight_dirs)
            ], lag_ratio=0.04),
        )
        self.wait(0.4)

        # ── FREEZE + TRANSFORM ────────────────────────────────
        # Dim overlay
        dim = FullScreenRectangle(fill_color="#010308", fill_opacity=0.45,
                                  stroke_width=0)
        self.play(FadeIn(dim, run_time=0.40))

        # Transform each zombie → human, curved path, pink
        humans = VGroup(*[_human(z.get_center()) for z in zombies])
        self.play(
            LaggedStart(*[
                ReplacementTransform(z, h, run_time=0.45)
                for z, h in zip(zombies, humans)
            ], lag_ratio=0.10),
            FadeOut(dim, run_time=0.55),
        )
        self.wait(0.2)

        # Humans walk in organic curves (dodge each other)
        organic_dirs = [
            np.array([float(RNG.uniform(-0.4, 0.4)),
                      float(RNG.uniform(-0.5, 0.5)), 0])
            for _ in range(N_PEDESTRIANS)
        ]
        self.play(
            LaggedStart(*[
                h.animate(run_time=0.70, rate_func=smooth)
                 .shift(d + np.array([0.0, float(RNG.uniform(-0.2, 0.2)), 0]))
                for h, d in zip(humans, organic_dirs)
            ], lag_ratio=0.06),
        )

        self.wait(0.4)  # let humans settle after organic walk

        # Label transform — slow and confident
        alive_label = Text("Human-Centric Physical AI",
                           font_size=SIZE_LABEL - 1, color=GREEN_SIGNAL,
                           font=FONT_PRIMARY, weight=BOLD)
        alive_label.move_to(zombie_label.get_center())
        self.play(ReplacementTransform(zombie_label, alive_label, run_time=0.65))
        # Brief glow pulse to emphasize the transformation
        self.play(
            Flash(alive_label.get_center(), color=GREEN_SIGNAL,
                  flash_radius=1.5, num_lines=10, run_time=0.40),
        )
        self.wait(2.0)   # mandatory 2.0s hold per 5_PART_GUIDE

        self.close()
