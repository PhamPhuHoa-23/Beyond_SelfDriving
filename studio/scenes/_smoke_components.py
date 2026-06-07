"""Phase 1 smoke test — one scene exercising every component module."""
from manimlib import *
from studio.components import (
    # colors
    BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK,
    PASTEL_BLUE, CYAN_RADAR, GOLD_KEY, ORANGE_INFRA, GOLD_RICH, INK_DARK,
    # typography
    text, markup, math,
    # base
    StudioScene,
    # pipeline
    pipeline_block, pipeline_arrow, pipeline_row,
    # charts
    axes_deploy, curve_trace,
    # agents
    vehicle_icon, pedestrian_icon, rsu_icon,
    # signals
    radar_shells_2d, ambient_glow,
    # annotations
    callout, contribution_badge,
    # animations
    forge_text, write_chiseled,
)


class SmokeComponents(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "Component Smoke Test"

    def construct(self):
        self.camera.background_color = BG_PAPER

        # --- Row 1: typography ---
        t1 = text("Foundation Models", size=28, color=INK_DARK)
        t2 = markup(
            'Markup: <span foreground="#DC2626">1%</span> '
            'scenarios - <span foreground="#D97706">100%</span> fatal',
            size=20,
        )
        t3 = math(r"\hat{y} = \sigma(Wx + b)", size=24)
        row1 = VGroup(t1, t2, t3).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        row1.to_corner(UL, buff=0.4)
        self.play(FadeIn(row1, lag_ratio=0.2))

        # --- Row 2: pipeline ---
        b1 = pipeline_block("Cameras", fill=PASTEL_BLUE, stroke=ACCENT_BLUE)
        b2 = pipeline_block("LLM", fill="#C8EDD0", stroke=ACCENT_GREEN)
        b3 = pipeline_block("Action", fill="#FAE3B0", stroke=ACCENT_AMBER)
        row2 = VGroup(b1, b2, b3)
        row2.arrange(RIGHT, buff=0.6)
        row2.move_to([0, 1.2, 0])
        arrows = VGroup(pipeline_arrow(b1, b2), pipeline_arrow(b2, b3))
        self.play(FadeIn(row2, lag_ratio=0.15))
        self.play(ShowCreation(arrows))

        # --- Row 3: charts ---
        axes, axes_anim = axes_deploy(
            (0, 5), (0, 1),
            x_label="Time", y_label="AP",
        )
        axes.scale(0.55).move_to([-3.5, -0.5, 0])
        self.play(axes_anim)
        self.play(curve_trace(axes, lambda x: 1 - np.exp(-x), color=ACCENT_TEAL))

        # --- Row 4: agents ---
        car = vehicle_icon(color=ACCENT_BLUE).scale(0.8)
        ped = pedestrian_icon(color=GOLD_KEY).scale(0.8)
        rsu = rsu_icon(color=ORANGE_INFRA).scale(0.8)
        agents = VGroup(car, ped, rsu).arrange(RIGHT, buff=0.5)
        agents.move_to([3.0, -0.3, 0])
        self.play(FadeIn(agents, lag_ratio=0.2))

        # --- Radar shells ---
        shells, shell_anim = radar_shells_2d(
            ORIGIN + np.array([2.5, -1.8, 0]),
            color=CYAN_RADAR, n_shells=3, max_radius=1.2,
        )
        self.play(shell_anim)

        # --- Ambient glow ---
        glow = ambient_glow(car, color=ACCENT_BLUE, radius=0.6)
        self.play(FadeIn(glow))

        # --- Callout ---
        ct = callout("Cooperative!", car, side="right")
        self.play(FadeIn(ct))

        # --- Contribution badge ---
        badge = contribution_badge("IROS 2025 Best Paper - UCLA", color=GOLD_KEY)
        badge.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(badge))

        # --- Forge text ---
        forge_anim = forge_text("BEYOND", size=48, color=GOLD_RICH)
        forge_target = Text("BEYOND", font="CMU Serif", font_size=48, color=GOLD_RICH)
        forge_target.to_corner(DR, buff=0.6)
        forge_target.set_opacity(0)
        self.add(forge_target)
        self.play(forge_anim)

        self.wait(1.5)
        self._close()
