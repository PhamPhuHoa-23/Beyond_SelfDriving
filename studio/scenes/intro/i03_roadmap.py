"""I-03 - Orbital Roadmap: 5-node orbital roadmap."""
from manimlib import *
from studio.components import (
    StudioScene,
    ACCENT_AMBER,
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_PINK,
    ACCENT_TEAL,
    BG_PAPER,
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

        orbit_r = 2.8
        nodes = VGroup()
        labels = VGroup()
        angles = [PI / 2 + i * TAU / 5 for i in range(5)]

        for i, (ang, color, pastel, lbl) in enumerate(
            zip(angles, PART_COLORS, PART_PASTELS, PART_LABELS)
        ):
            pos = orbit_r * np.array([np.cos(ang), np.sin(ang), 0])
            dot = Circle(radius=0.28, fill_color=pastel, fill_opacity=1.0,
                         stroke_color=color, stroke_width=2.2)
            num = Text(str(i + 1), font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=INK_DARK, weight=BOLD)
            num.set_color(INK_DARK)
            dot.move_to(pos)
            num.move_to(pos)
            node = VGroup(dot, num)
            label = Text(lbl, font=FONT_PRIMARY, font_size=SIZE_LABEL - 4,
                         color=INK_MID)
            label.next_to(dot, normalize(pos), buff=0.22)
            nodes.add(node)
            labels.add(label)

        orbit_ring = Circle(radius=orbit_r, stroke_color=INK_MID,
                            stroke_width=0.8, stroke_opacity=0.25)
        self.play(ShowCreation(orbit_ring, run_time=0.8))

        def node_reveal(node, label, color):
            reveal_dir = normalize(node.get_center())
            halo = Circle(radius=0.36, stroke_color=color,
                          stroke_width=3.0, stroke_opacity=0.55)
            halo.move_to(node)
            self.play(
                GrowFromCenter(node, run_time=0.45),
                FadeIn(label, shift=0.12 * reveal_dir, run_time=0.45),
                halo.animate.scale(1.45).set_stroke(opacity=0),
            )
            self.wait(0.06)

        def travel_arc(start_angle, color):
            arc = Arc(radius=orbit_r, start_angle=start_angle,
                      angle=TAU / 5)
            arc.set_stroke(color, width=5.0, opacity=1.0)
            glow = Arc(radius=orbit_r, start_angle=start_angle,
                       angle=TAU / 5)
            glow.set_stroke(color, width=9.0, opacity=0.18)
            self.play(
                ShowPassingFlash(glow, time_width=0.35, run_time=0.55),
                ShowPassingFlash(arc, time_width=0.25, run_time=0.55),
            )

        node_reveal(nodes[0], labels[0], PART_COLORS[0])
        for i in range(1, len(nodes)):
            travel_arc(angles[i - 1], PART_COLORS[i])
            node_reveal(nodes[i], labels[i], PART_COLORS[i])

        caption = Text("Five parts. One road.", font=FONT_PRIMARY,
                       font_size=SIZE_BODY, color=INK_DARK)
        caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(caption))
        self.wait(1.5)
        self._close()
