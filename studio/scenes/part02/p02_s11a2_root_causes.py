"""P02-S11A2 - Two Root Causes: Initialization sensitivity and gradient conflict."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene,
    ACCENT_BLUE,
    ACCENT_TEAL,
    BG_CARD,
    BG_PAPER,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    INK_LIGHT,
    PURPLE_MODEL,
    RED_ERROR,
    SIZE_CAPS,
    SIZE_LABEL,
    SIZE_MICRO,
)
from studio.components.charts import axes_deploy

SCRIPT = "Two root causes: rugged landscape from random init, and task gradients that cancel."

# Loss landscape bumps configuration: (amplitude, center, width)
BUMPS_0 = []
BUMPS_1 = [(0.35, -2.5, 0.6)]
BUMPS_2 = BUMPS_1 + [(0.30, -0.5, 0.5), (0.25, 1.5, 0.4)]
BUMPS_3 = BUMPS_2 + [(0.80, 3.0, 1.5)]


def f0(x):
    return 0.08 * ((x - 0.5) ** 2)


def df0(x):
    return 0.16 * (x - 0.5)


def get_bump_val(x, bump):
    a, b, w = bump
    return a * np.exp(-((x - b) ** 2) / w)


def get_bump_deriv(x, bump):
    a, b, w = bump
    return -2.0 * a * (x - b) / w * np.exp(-((x - b) ** 2) / w)


def eval_f(x, bumps, ripple=False):
    val = f0(x)
    for b in bumps:
        val -= get_bump_val(x, b)
    if ripple:
        val -= 0.05 * np.sin(10.0 * x)
    return val


def eval_df(x, bumps, ripple=False):
    val = df0(x)
    for b in bumps:
        val -= get_bump_deriv(x, b)
    if ripple:
        val -= 0.5 * np.cos(10.0 * x)
    return val


def run_gd(x_start, lr, steps, bumps, ripple=False):
    path = [x_start]
    curr = x_start
    for _ in range(steps):
        grad = eval_df(curr, bumps, ripple)
        curr = curr - lr * grad
        curr = np.clip(curr, -4.5, 4.5)
        path.append(curr)
    return path


def _txt(label: str, *, size: int = SIZE_LABEL, color: str = INK_DARK, weight=None) -> Text:
    kwargs = {"font": FONT_PRIMARY, "font_size": size, "color": color}
    if weight is not None:
        kwargs["weight"] = weight
    return Text(label, **kwargs)


def _small_chip(text_val: str) -> VGroup:
    t = _txt(text_val, size=SIZE_MICRO, color=INK_DARK, weight=BOLD)
    r = RoundedRectangle(
        width=t.get_width() + 0.3,
        height=0.36,
        corner_radius=0.06,
        fill_color=BG_CARD,
        fill_opacity=1.0,
        stroke_color=INK_MID,
        stroke_width=1.0,
    )
    t.move_to(r)
    return VGroup(r, t)


def _cause_chip(label: str, color: str) -> VGroup:
    text = _txt(label, size=SIZE_LABEL, color=color, weight=BOLD)
    rect = RoundedRectangle(
        width=text.get_width() + 0.4,
        height=0.48,
        corner_radius=0.08,
        fill_color=BG_CARD,
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.5,
    )
    text.move_to(rect)
    return VGroup(rect, text)


class P02S11A2RootCauses(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "Two Root Causes"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # -------------------------------------------------------------
        # BEAT 1: Initialization Sensitivity
        # -------------------------------------------------------------

        # Deploy abstract axes (no ticks, no labels)
        axes, deploy_anim = axes_deploy(
            x_range=(-4.5, 4.5),
            y_range=(-1.2, 2.2),
            width=9.5,
            height=3.4,
            axis_config={
                "include_tip": True,
                "include_ticks": False,
                "stroke_color": INK_MID,
                "stroke_width": 2.0,
            }
        )
        axes.move_to(UP * 0.4)
        self.play(deploy_anim)

        # Helper to construct curves in axes system
        def get_curve(bumps, ripple=False):
            xs = np.linspace(-4.5, 4.5, 120)
            points = [axes.c2p(x, eval_f(x, bumps, ripple)) for x in xs]
            curve_mob = VMobject()
            curve_mob.set_points_smoothly(points)
            curve_mob.set_stroke(ACCENT_TEAL, width=4)
            curve_mob.set_fill(opacity=0)
            return curve_mob

        # 1. Simple bowl
        curve = get_curve(BUMPS_0)
        self.play(ShowCreation(curve, run_time=1.5))

        # 2. Add complexity chips & morph curve
        chip_temporal = _small_chip("temporal")
        chip_agent = _small_chip("multi-agent")
        chip_task = _small_chip("multi-task")

        chips = VGroup(chip_temporal, chip_agent, chip_task).arrange(RIGHT, buff=0.4)
        chips.move_to(UP * 2.4)

        # Morph 1
        self.play(FadeIn(chip_temporal, shift=UP * 0.1))
        curve_1 = get_curve(BUMPS_1)
        self.play(Transform(curve, curve_1), run_time=0.8)

        # Morph 2
        self.play(FadeIn(chip_agent, shift=UP * 0.1))
        curve_2 = get_curve(BUMPS_2)
        self.play(Transform(curve, curve_2), run_time=0.8)

        # Morph 3
        self.play(FadeIn(chip_task, shift=UP * 0.1))
        curve_3 = get_curve(BUMPS_3, ripple=True)
        self.play(Transform(curve, curve_3), run_time=0.8)
        self.wait(0.3)

        # 3. Drop random starts
        x_starts = [-3.8, -1.2, 1.1, 4.2]
        dots = VGroup()
        for x in x_starts:
            y = eval_f(x, BUMPS_3, ripple=True)
            dot = Dot(axes.c2p(x, y), radius=0.09, fill_color=INK_DARK, fill_opacity=1.0, stroke_width=0)
            dots.add(dot)

        caption_init = _txt("random init", size=SIZE_MICRO, color=INK_MID)
        caption_init.move_to(axes.c2p(-2.0, 1.4))

        self.play(FadeIn(dots), FadeIn(caption_init), run_time=0.8)
        self.wait(0.5)

        # 4. Animate Gradient Descent paths
        lr = 0.12
        steps = 35
        paths = []
        for x_start in x_starts:
            x_path = run_gd(x_start, lr, steps, BUMPS_3, ripple=False)
            pts = [axes.c2p(x, eval_f(x, BUMPS_3, ripple=True)) for x in x_path]
            path_mob = VMobject()
            path_mob.set_points_smoothly(pts)
            paths.append(path_mob)

        gd_anims = []
        for i, dot in enumerate(dots):
            gd_anims.append(MoveAlongPath(dot, paths[i], rate_func=smooth))

        self.play(
            LaggedStart(*gd_anims, lag_ratio=0.15, run_time=2.2),
            FadeOut(caption_init),
        )

        # 5. Minima trapping indicator
        self.play(
            dots[0].animate.set_color(RED_ERROR),
            dots[1].animate.set_color(RED_ERROR),
            dots[2].animate.set_color(RED_ERROR),
            dots[3].animate.set_color(GREEN_FIX),
            run_time=0.2
        )
        self.play(
            Indicate(dots[0], color=RED_ERROR, scale_factor=1.5),
            Indicate(dots[1], color=RED_ERROR, scale_factor=1.5),
            Indicate(dots[2], color=RED_ERROR, scale_factor=1.5),
            dots[3].animate.set_color(INK_DARK),
            run_time=0.6
        )
        self.wait(0.5)

        # 6. Shrink and park to Left Column
        beat1_group = VGroup(axes, curve, dots, chips)
        self.play(
            beat1_group.animate.scale(0.62).move_to(LEFT * 3.2 + UP * 0.4),
            run_time=0.8
        )

        gold_chip = _cause_chip("init sensitivity", GOLD_RICH)
        gold_chip.move_to(LEFT * 3.2 + DOWN * 1.5)
        self.play(FadeIn(gold_chip, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        # -------------------------------------------------------------
        # BEAT 2: Gradient Conflict
        # -------------------------------------------------------------

        # Anchor everything at theta center (no coordinate axes)
        theta_center = RIGHT * 3.2 + UP * 0.6
        theta = Dot(theta_center, radius=0.1, fill_color=INK_DARK, fill_opacity=1.0, stroke_width=0)
        theta_label = Tex(r"\theta", font_size=SIZE_CAPS)
        theta_label.set_color(INK_DARK)
        theta_label.next_to(theta, UP + LEFT, buff=0.08)

        self.play(FadeIn(theta), FadeIn(theta_label), run_time=0.6)

        # Gradient vectors pointing in obtuse angles
        det_vec = np.array([1.0, 1.4, 0])
        pred_vec = np.array([1.1, -1.2, 0])
        plan_vec = np.array([-1.8, -0.1, 0])

        det_arrow = Arrow(
            theta_center,
            theta_center + det_vec,
            stroke_color=ACCENT_BLUE,
            stroke_width=5,
            buff=0,
            max_tip_length_to_length_ratio=0.12,
        )
        det_label = _txt("det", size=SIZE_CAPS, color=ACCENT_BLUE, weight=BOLD)
        det_label.next_to(det_arrow.get_end(), UP + RIGHT, buff=0.12)

        pred_arrow = Arrow(
            theta_center,
            theta_center + pred_vec,
            stroke_color=GOLD_RICH,
            stroke_width=5,
            buff=0,
            max_tip_length_to_length_ratio=0.12,
        )
        pred_label = _txt("pred", size=SIZE_CAPS, color=GOLD_RICH, weight=BOLD)
        pred_label.next_to(pred_arrow.get_end(), DOWN + RIGHT, buff=0.12)

        plan_arrow = Arrow(
            theta_center,
            theta_center + plan_vec,
            stroke_color=PURPLE_MODEL,
            stroke_width=5,
            buff=0,
            max_tip_length_to_length_ratio=0.12,
        )
        plan_label = _txt("plan", size=SIZE_CAPS, color=PURPLE_MODEL, weight=BOLD)
        plan_label.next_to(plan_arrow.get_end(), LEFT, buff=0.12)

        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(det_arrow), FadeIn(det_label)),
                AnimationGroup(GrowArrow(pred_arrow), FadeIn(pred_label)),
                AnimationGroup(GrowArrow(plan_arrow), FadeIn(plan_label)),
                lag_ratio=0.18,
                run_time=1.0
            )
        )
        self.wait(0.3)

        # Staged tip-to-tail ghost chain
        ghost_det = Arrow(
            theta_center,
            theta_center + det_vec,
            stroke_color=ACCENT_BLUE,
            stroke_width=3.5,
            stroke_opacity=0.40,
            fill_opacity=0.40,
            buff=0,
        )
        ghost_pred = Arrow(
            theta_center + det_vec,
            theta_center + det_vec + pred_vec,
            stroke_color=GOLD_RICH,
            stroke_width=3.5,
            stroke_opacity=0.40,
            fill_opacity=0.40,
            buff=0,
        )
        ghost_plan = Arrow(
            theta_center + det_vec + pred_vec,
            theta_center + det_vec + pred_vec + plan_vec,
            stroke_color=PURPLE_MODEL,
            stroke_width=3.5,
            stroke_opacity=0.40,
            fill_opacity=0.40,
            buff=0,
        )

        self.play(GrowArrow(ghost_det), run_time=0.45)
        self.play(GrowArrow(ghost_pred), run_time=0.45)
        self.play(GrowArrow(ghost_plan), run_time=0.45)

        # Net step arrow representing sum ≈ 0
        sum_vec = det_vec + pred_vec + plan_vec
        net_arrow = Arrow(
            theta_center,
            theta_center + sum_vec,
            stroke_color=RED_ERROR,
            stroke_width=5.5,
            buff=0,
            max_tip_length_to_length_ratio=0.25,
        )
        net_label = _txt("net step ≈ 0", size=SIZE_CAPS, color=RED_ERROR, weight=BOLD)
        net_label.next_to(net_arrow, UP + RIGHT, buff=0.08)

        self.play(GrowArrow(net_arrow), FadeIn(net_label), run_time=0.5)
        self.play(Indicate(net_arrow, color=RED_ERROR, scale_factor=1.3), run_time=0.6)
        self.wait(0.5)

        # Transition to short stubs & clear labels
        self.play(
            det_arrow.animate.scale(0.35, about_point=theta_center).set_opacity(0.5),
            pred_arrow.animate.scale(0.35, about_point=theta_center).set_opacity(0.5),
            plan_arrow.animate.scale(0.35, about_point=theta_center).set_opacity(0.5),
            net_arrow.animate.scale(0.35, about_point=theta_center).set_opacity(0.6),
            FadeOut(det_label), FadeOut(pred_label), FadeOut(plan_label), FadeOut(net_label),
            FadeOut(ghost_det), FadeOut(ghost_pred), FadeOut(ghost_plan),
            run_time=0.6
        )

        # "Thrash-in-place" zigzag steps with visible trail
        rng = np.random.default_rng(2)
        trail = VGroup()
        cur = theta_center.copy()
        amp = 0.15  # stays inside the stub cluster (amplitude ≈ stub length * 0.3)
        counter = _txt("steps: 50", size=SIZE_CAPS, color=INK_MID)
        counter.next_to(theta, DOWN, buff=0.5)
        self.add(trail)
        self.play(FadeIn(counter), run_time=0.3)

        for k, n in enumerate([50, 120, 200, 300, 400, 500, 600, 700, 800, 900, 950, 1000]):
            nxt = theta_center + rng.uniform(-amp, amp, size=3) * np.array([1, 1, 0])
            seg = Line(cur, nxt, stroke_color=INK_LIGHT, stroke_width=2.5)
            new_counter = _txt(f"steps: {n}", size=SIZE_CAPS, color=INK_MID).move_to(counter)
            self._force_text_contrast(new_counter)
            self.play(
                theta.animate.move_to(nxt),
                ShowCreation(seg),
                run_time=0.18,
                rate_func=linear
            )
            self.remove(counter)
            self.add(new_counter)
            counter = new_counter
            self.remove(seg)
            trail.add(seg)
            cur = nxt

        self.play(theta.animate.move_to(theta_center), run_time=0.25)
        self.wait(0.4)

        # Park to Right Column (keeping stubs + trail visible, no scaling down)
        beat2_group = VGroup(theta, theta_label, det_arrow, pred_arrow, plan_arrow, net_arrow, trail, counter)
        self.play(
            beat2_group.animate.move_to(RIGHT * 3.2 + UP * 0.4),
            run_time=0.8
        )

        green_chip = _cause_chip("gradient conflict", GREEN_FIX)
        green_chip.move_to(RIGHT * 3.2 + DOWN * 1.5)
        self.play(FadeIn(green_chip, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        # -------------------------------------------------------------
        # CLOSING BEAT
        # -------------------------------------------------------------
        self.play(
            axes.animate.set_opacity(0.45),
            curve.animate.set_stroke(opacity=0.45),
            dots.animate.set_opacity(0.45),
            chips.animate.set_opacity(0.45),
            theta.animate.set_opacity(0.45),
            theta_label.animate.set_opacity(0.45),
            det_arrow.animate.set_opacity(0.25),
            pred_arrow.animate.set_opacity(0.25),
            plan_arrow.animate.set_opacity(0.25),
            net_arrow.animate.set_opacity(0.30),
            trail.animate.set_stroke(opacity=0.45),
            counter.animate.set_opacity(0.45),
            run_time=0.8
        )

        closing_text = _txt("SGD cannot fix either.", size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        closing_text.move_to(DOWN * 2.5)
        self.play(FadeIn(closing_text, shift=UP * 0.12), run_time=0.6)
        self.wait(1.8)

        self._close()
