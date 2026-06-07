"""I-03 - Orbital Roadmap: 5-node orbital with lightning trace."""
from manimlib import *
from studio.components import (
    StudioScene,
    ACCENT_AMBER,
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_PINK,
    ACCENT_TEAL,
    BG_PAPER,
    GOLD_RICH,
    INK_DARK,
    INK_MID,
    PASTEL_AMBER,
    PASTEL_BLUE,
    PASTEL_GREEN,
    PASTEL_PINK,
    PASTEL_TEAL,
    FONT_PRIMARY,
    SIZE_BODY,
    SIZE_LABEL,
)

SCRIPT = """
Five parts. One road.
"""


PART_COLORS = [ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PINK]
PART_PASTELS = [PASTEL_BLUE, PASTEL_TEAL, PASTEL_GREEN, PASTEL_AMBER, PASTEL_PINK]
PART_LABELS = [
    "Foundation\nModels",
    "Cooperative\nPerception",
    "Sim-to-Real",
    "Efficiency",
    "Physical AI",
]


class I03Roadmap(StudioScene):
    PART_NUM = 0
    SCENE_TITLE = "Five Parts, One Road"

    def construct(self):
        self.camera.background_color = BG_PAPER

        star = RegularPolygon(n=6, radius=0.32, fill_color=GOLD_RICH,
                              fill_opacity=1.0, stroke_width=0)
        self.play(GrowFromCenter(star, run_time=0.8))
        self.play(
            star.animate.scale(1.3).scale(1 / 1.3),
            Flash(star, color=GOLD_RICH, line_length=0.2, num_lines=10),
            run_time=0.4,
            rate_func=there_and_back,
        )

        orbit_r = 2.8
        nodes = VGroup()
        labels = VGroup()
        angles = [PI / 2 + i * TAU / 5 for i in range(5)]
        start_nodes = []

        for i, (ang, color, pastel, lbl) in enumerate(
            zip(angles, PART_COLORS, PART_PASTELS, PART_LABELS)
        ):
            pos = orbit_r * np.array([np.cos(ang), np.sin(ang), 0])
            dot = Circle(radius=0.28, fill_color=pastel, fill_opacity=1.0,
                         stroke_color=color, stroke_width=2.2)
            num = Text(str(i + 1), font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=color, weight=BOLD)
            dot.move_to(pos)
            num.move_to(pos)
            node = VGroup(dot, num)
            label = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_LABEL - 4,
                         color=INK_MID)
            label.next_to(dot, normalize(pos), buff=0.22)
            nodes.add(node)
            labels.add(label)
            start = node.copy().scale(0.001).move_to(ORIGIN)
            start_nodes.append(start)

        orbit_ring = Circle(radius=orbit_r, stroke_color=INK_MID,
                            stroke_width=0.8, stroke_opacity=0.25)
        self.play(ShowCreation(orbit_ring, run_time=0.8))

        for node in nodes:
            node.save_state()
            node.scale(0.001)
            node.move_to(ORIGIN)
        self.play(LaggedStart(
            *(
                Restore(node, path_arc=PI * 0.6, run_time=0.75)
                for node in nodes
            ),
            lag_ratio=0.18,
        ))
        self.play(LaggedStart(*(FadeIn(lbl) for lbl in labels),
                              lag_ratio=0.15, run_time=1.0))

        afterglow = VGroup()
        trace_anims = []
        for i in range(len(nodes)):
            j = (i + 1) % len(nodes)
            arc = ArcBetweenPoints(
                nodes[i][0].get_center(), nodes[j][0].get_center(),
                angle=-TAU / 12,
            )
            glow = arc.copy().set_stroke("#FEF3C7", width=4.0, opacity=0.3)
            flash = arc.copy().set_stroke(GOLD_RICH, width=5.0, opacity=1.0)
            afterglow.add(glow)
            trace_anims.append(AnimationGroup(
                FadeIn(glow, run_time=0.12),
                ShowPassingFlash(flash, time_width=0.4, run_time=0.4),
            ))
        self.play(LaggedStart(*trace_anims, lag_ratio=0.28))
        self.add(afterglow)

        self.play(
            Flash(nodes[0], color=ACCENT_BLUE, line_length=0.25, num_lines=10),
            nodes[0][0].animate.set_fill(ACCENT_BLUE, opacity=0.45),
            nodes[0][0].animate.set_stroke(ACCENT_BLUE, width=3.5),
            run_time=0.8,
        )

        caption = Text("Five parts. One road.", font=FONT_PRIMARY,
                       font_size=SIZE_BODY, color=INK_DARK)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption))
        self.wait(1.5)
        self._close()
