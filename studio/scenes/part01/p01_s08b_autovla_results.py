"""P01-S08b — AutoVLA Results: bar chart + key numbers (clean axis layout)."""
from manimlib import *
from studio.components import (
    StudioScene,
    GOLD_RICH, GOLD_KEY, GREEN_FIX, INK_MID, INK_DARK, BG_CARD, LINE_SEP,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    axes_deploy, chart_mount, key_number, contribution_badge,
    place_footer,
)

SCRIPT = """
Reasoning beats action-only training on every metric.
Plus RFT cuts runtime by two-thirds.
"""


class P01S08BAutoVLAResults(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "AutoVLA Results"

    def construct(self):
        self._open(self.SCENE_TITLE)

        axes, axes_anim = axes_deploy(
            (0, 4, 1), (0, 1.0, 0.2),
            width=6.0, height=4.2, with_tick_labels=False,
        )
        tick_labels = chart_mount(
            axes, LEFT * 1.8 + DOWN * 0.2, scale=0.88, y_label="Score",
        )

        # ── Background card panels for nuPlan and nuScenes ────────────────────
        panels = VGroup()
        headers = VGroup()
        
        p1_bottom_left = axes.c2p(0.20, 0.0)
        p1_top_right = axes.c2p(1.80, 1.05)
        p2_bottom_left = axes.c2p(2.20, 0.0)
        p2_top_right = axes.c2p(3.80, 1.05)
        
        for bl, tr, name in [
            (p1_bottom_left, p1_top_right, "nuPlan"),
            (p2_bottom_left, p2_top_right, "nuScenes")
        ]:
            w = tr[0] - bl[0]
            h = tr[1] - bl[1]
            center = (bl + tr) / 2
            
            panel = RoundedRectangle(
                width=w,
                height=h,
                corner_radius=0.12,
                fill_color=BG_CARD,
                fill_opacity=0.35,
                stroke_color=LINE_SEP,
                stroke_width=1.5,
            )
            panel.move_to(center)
            panel.set_z_index(-1)
            panels.add(panel)
            
            header = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
            header.move_to(np.array([center[0], tr[1] - 0.32, 0]))
            header.set_z_index(1)
            headers.add(header)

        self.play(
            axes_anim,
            FadeIn(tick_labels),
            FadeIn(panels),
            Write(headers),
        )

        # ── Custom bars and labels ────────────────────────────────────────────
        x_coords = [0.6, 1.4, 2.6, 3.4]
        values = [0.72, 0.79, 0.68, 0.82]
        colors = [INK_MID, GOLD_RICH, INK_MID, GOLD_RICH]
        bar_lbls = ["base", "AutoVLA", "base", "AutoVLA"]
        
        bars = VGroup()
        value_labels = VGroup()
        x_labels = VGroup()
        
        bar_width_axes = 0.62
        
        for x, val, col, lbl in zip(x_coords, values, colors, bar_lbls):
            bottom = axes.c2p(x, 0)
            top = axes.c2p(x, val)
            
            w = axes.c2p(bar_width_axes, 0)[0] - axes.c2p(0, 0)[0]
            h = abs(top[1] - bottom[1])
            
            bar = Rectangle(
                width=w,
                height=h,
                fill_color=col,
                fill_opacity=0.88,
                stroke_color=interpolate_color(col, INK_DARK, 0.25),
                stroke_width=1.2,
            )
            bar.move_to((bottom + top) / 2)
            bars.add(bar)
            
            vl = Text(
                f"{val:.2f}".rstrip("0").rstrip("."),
                font=FONT_PRIMARY,
                font_size=SIZE_CAPS,
                color=INK_DARK,
                weight=BOLD,
            )
            vl.next_to(bar, UP, buff=0.12)
            value_labels.add(vl)
            
            xl = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID, weight=BOLD)
            xl.next_to(axes.c2p(x, 0), DOWN, buff=0.24)
            x_labels.add(xl)

        bars_group = VGroup(bars, value_labels, x_labels)
        bar_anim = LaggedStart(
            *(GrowFromEdge(b, DOWN) for b in bars),
            lag_ratio=0.18,
            run_time=1.2,
        )

        self.play(
            bar_anim,
            FadeIn(x_labels),
            FadeIn(value_labels),
        )

        kn_plan = key_number("+10.6%", "planning score", color=GREEN_FIX)
        kn_rt = key_number("3×", "faster  (−66.8% runtime)", color=GREEN_FIX)
        kn_group = VGroup(kn_plan, kn_rt).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        kn_group.scale(0.80)
        kn_group.move_to(RIGHT * 3.6 + UP * 0.3)

        self.play(
            # bars_group[0][1] corresponds to the second bar (AutoVLA on nuPlan)
            LaggedStart(FadeIn(kn_plan, scale=1.08), FadeIn(kn_rt, scale=1.08), lag_ratio=0.35),
            Flash(bars_group[0][1], color=GOLD_RICH, num_lines=12, line_length=0.2),
        )

        badge = contribution_badge("IROS 2025 Best Paper  ·  UCLA DriveX", color=GOLD_KEY)
        place_footer(badge)
        badge.shift(UP * 0.45)
        self.play(FadeIn(badge))
        self.wait(2)
        self._close()

