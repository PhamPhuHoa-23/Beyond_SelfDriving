"""P01-S03b — E2E: compact symbolic network (visible, linked, one border)."""
from manimlib import *
from studio.components import (
    StudioScene,
    PASTEL_BLUE, ACCENT_BLUE, PURPLE_MODEL, INK_DARK, INK_MID, GREEN_FIX, RED_ERROR,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    stage_panel, h_arrow,
)


def _symbolic_mlp(*, n_cols: int = 3, n_rows: int = 3) -> VGroup:
    """Small MLP icon: dots + sparse synapses (all nodes connected across layers)."""
    cols = VGroup()
    x_step = 0.62
    for xi in range(n_cols):
        col = VGroup(*[
            Dot(radius=0.09, color=PURPLE_MODEL).set_stroke(INK_DARK, width=1.6)
            for _ in range(n_rows)
        ])
        col.arrange(DOWN, buff=0.2)
        col.move_to(xi * x_step * RIGHT)
        cols.add(col)
    lines = VGroup()
    for c1, c2 in zip(cols[:-1], cols[1:]):
        for d1 in c1:
            for d2 in c2:
                lines.add(Line(
                    d1.get_center(), d2.get_center(),
                    stroke_color=INK_DARK, stroke_width=2.2, stroke_opacity=0.75,
                ))
    return VGroup(lines, cols)


class P01S03BE2E(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "End-to-End Systems"

    def construct(self):
        self._open(self.SCENE_TITLE)

        net = _symbolic_mlp(n_cols=3, n_rows=3)
        net.set_height(2.55)

        panel = stage_panel(
            "Neural network (black box)",
            net,
            fill=PASTEL_BLUE,
            stroke=PURPLE_MODEL,
            show_inner_bg=False,
            tight=True,
            pad=0.36,
        )
        panel.scale(1.28)
        panel.move_to(ORIGIN + UP * 0.35)

        sensors = Text("Sensors", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        action = Text("Action", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        sensors.next_to(panel[0], LEFT, buff=0.65)
        action.next_to(panel[0], RIGHT, buff=0.65)

        self.play(FadeIn(panel))
        self.play(ShowCreation(net[0]), lag_ratio=0.02, run_time=1.2)
        self.play(LaggedStart(*(FadeIn(d) for d in net[1]), lag_ratio=0.08, run_time=0.7))
        self.play(
            FadeIn(sensors), FadeIn(action),
            ShowCreation(h_arrow(sensors, panel[0], color=INK_DARK)),
            ShowCreation(h_arrow(panel[0], action, color=INK_DARK)),
        )

        badges = VGroup(*[
            Text(line, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
            for line, color in [
                ("[OK] No error accumulation", GREEN_FIX),
                ("[OK] Joint optimization", GREEN_FIX),
                ("[WARN] Black box — hard to debug", RED_ERROR),
            ]
        ])
        badges.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        badges.to_edge(DOWN, buff=0.3)
        self.play(LaggedStart(*(FadeIn(b) for b in badges), lag_ratio=0.15))
        self.wait(1.5)
        self._close()
