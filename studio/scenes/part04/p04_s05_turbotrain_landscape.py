"""P04-S05 TurboTrain Loss Landscape."""
from manimlib import *

from studio.components import (
    Studio3DScene,
    BG_PAPER,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    RED_ERROR,
    SIZE_H1,
    SIZE_LABEL,
)

SCRIPT = "TurboTrain pretrains and then balances gradients; 120 epochs becomes 45."


def _loss(x: float, y: float) -> float:
    bowl = 0.12 * ((x - 0.25) ** 2 + 0.75 * (y + 0.25) ** 2)
    ridge = 0.8 * np.exp(-((x + 1.35) ** 2 / 0.6 + (y - 0.85) ** 2 / 0.35))
    wall = 0.55 * np.exp(-((x - 1.25) ** 2 / 0.75 + (y + 1.25) ** 2 / 0.55))
    ripple = 0.08 * np.sin(2.4 * x) * np.cos(2.1 * y)
    return bowl + ridge + wall + ripple


def _screen_text(label: str, *, size: int, color: str = INK_DARK, weight=None) -> Text:
    kwargs = {"font": FONT_PRIMARY, "font_size": size, "color": color}
    if weight is not None:
        kwargs["weight"] = weight
    mob = Text(label, **kwargs)
    mob.fix_in_frame()
    return mob


class P04S05TurboTrainLandscape(Studio3DScene):
    PART_NUM = 4
    SCENE_TITLE = "TurboTrain: Loss Landscape"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self.camera.background_rgba = color_to_rgba(BG_PAPER)
        self.frame.reorient(-38, 66, 0)

        title = _screen_text(self.SCENE_TITLE, size=56, color=INK_DARK)
        title.to_edge(UP, buff=0.35)
        sep = Line(LEFT * 6.5, RIGHT * 6.5, stroke_color=CYAN_RADAR, stroke_width=2.0, stroke_opacity=0.85).fix_in_frame()
        sep_glow = Line(LEFT * 6.5, RIGHT * 6.5, stroke_color=CYAN_RADAR, stroke_width=6.0, stroke_opacity=0.13).fix_in_frame()
        sep.next_to(title, DOWN, buff=0.12)
        sep_glow.move_to(sep)
        self.play(FadeIn(title, shift=DOWN * 0.15), ShowCreation(sep), ShowCreation(sep_glow), run_time=0.7)

        axes = ThreeDAxes(
            x_range=[-2.7, 2.7, 1],
            y_range=[-2.2, 2.2, 1],
            z_range=[0, 1.9, 0.5],
            width=6.6,
            height=5.2,
            depth=2.2,
            axis_config={
                "include_ticks": False,
                "include_numbers": False,
                "include_tip": True,
                "stroke_color": INK_MID,
                "stroke_width": 1.6,
            },
        )
        axes.move_to(DOWN * 0.6)

        surface = ParametricSurface(
            lambda u, v: axes.c2p(u, v, _loss(u, v)),
            u_range=[-2.45, 2.45],
            v_range=[-1.9, 1.9],
            resolution=(48, 36),
        )
        surface.set_color_by_gradient(RED_ERROR, GOLD_RICH, GREEN_FIX)
        surface.set_opacity(0.76)
        surface.apply_depth_test()

        basin = Sphere(radius=0.08, color=GOLD_RICH)
        basin.move_to(axes.c2p(0.25, -0.25, _loss(0.25, -0.25) + 0.1))
        basin.apply_depth_test()

        self.play(ShowCreation(axes), FadeIn(surface), run_time=1.0)
        self.play(GrowFromCenter(basin), run_time=0.35)

        bad_xy = [
            (-2.0, 1.25), (-1.42, 0.45), (-1.78, -0.25),
            (-1.05, 0.15), (-0.78, -0.7), (-0.28, -0.18),
        ]
        bad_path = VMobject(stroke_color=RED_ERROR, stroke_width=4.2, stroke_opacity=0.9)
        bad_path.set_points_as_corners([axes.c2p(x, y, _loss(x, y) + 0.08) for x, y in bad_xy])
        bad_dot = Sphere(radius=0.07, color=RED_ERROR)
        bad_dot.move_to(bad_path.get_start())
        stage1 = _screen_text("Stage 1: masked pretrain stabilizes the basin", size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        stage1.to_edge(LEFT, buff=0.72).to_edge(DOWN, buff=1.12)
        self.play(FadeIn(stage1), GrowFromCenter(bad_dot), run_time=0.35)
        self.play(ShowCreation(bad_path), MoveAlongPath(bad_dot, bad_path), run_time=1.5)
        self.play(FadeOut(stage1), FadeOut(bad_dot), run_time=0.3)

        t_vals = np.linspace(0, 1, 96)
        good_points = []
        for t in t_vals:
            angle = 2.2 * TAU * (1 - t)
            radius = 1.7 * (1 - t) ** 1.35
            x = 0.25 + radius * np.cos(angle)
            y = -0.25 + 0.7 * radius * np.sin(angle)
            good_points.append(axes.c2p(x, y, _loss(x, y) + 0.1))
        good_path = VMobject(stroke_color=GREEN_FIX, stroke_width=5.0, stroke_opacity=0.95)
        good_path.set_points_smoothly(good_points)
        good_dot = Sphere(radius=0.085, color=GREEN_FIX)
        good_dot.move_to(good_path.get_start())
        stage2 = _screen_text("Stage 2: gradient balance descends cleanly", size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD)
        stage2.to_edge(LEFT, buff=0.72).to_edge(DOWN, buff=1.12)
        self.play(FadeIn(stage2), GrowFromCenter(good_dot), run_time=0.35)
        self.play(ShowCreation(good_path), MoveAlongPath(good_dot, good_path), run_time=2.0)

        counter = _screen_text("120 epochs  \u2192  45 epochs", size=SIZE_H1, color=INK_DARK, weight=BOLD)
        counter["120 epochs"].set_color(RED_ERROR)
        counter["45 epochs"].set_color(GREEN_FIX)
        counter.to_edge(DOWN, buff=0.92)
        self.play(FadeOut(stage2), FadeIn(counter, shift=UP * 0.15), run_time=0.5)

        self.frame.add_ambient_rotation(0.8 * DEG)
        self.wait(1.1)
        self.frame.clear_updaters()

        self.play(LaggedStart(*(FadeOut(m) for m in self.mobjects), lag_ratio=0.03, run_time=0.8))
