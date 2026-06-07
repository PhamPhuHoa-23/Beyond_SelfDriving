"""P05-S07 Zombie City -> Human-Centric Physical AI."""
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
