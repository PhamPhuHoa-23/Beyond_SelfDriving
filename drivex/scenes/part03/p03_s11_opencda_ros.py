"""
Scene 3-11 — OpenCDA-ROS Digital Twin
=======================================
Real World ↔ OpenCDA-ROS bridge ↔ CARLA Simulation.
Bidirectional arrows + "Write once, run anywhere" tagline.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from manim import *
from drivex.components.colors import *


class P03S11OpenCDAROS(Scene):
    """
    3-panel layout: Real World | OpenCDA-ROS | CARLA
    Bidirectional flow arrows + module labels + tagline
    """

    def construct(self):
        self.camera.background_color = BG_BLACK

        heading = Text("OpenCDA-ROS Digital Twin", font_size=26, color=COL_GOLD, weight=BOLD)
        heading.to_edge(UP, buff=0.4)
        self.play(FadeIn(heading), run_time=0.3)

        # ═══ 3 panels ═════════════════════════════════════════════
        panels = [
            ("Real\nWorld",     COL_BLUE,        LEFT * 4.0),
            ("OpenCDA-ROS\nBridge", COL_PURPLE,  ORIGIN),
            ("CARLA\nSimulation", COL_GREEN,     RIGHT * 4.0),
        ]

        panel_objs = []
        for title, color, pos in panels:
            box = RoundedRectangle(width=2.6, height=2.0, corner_radius=0.2,
                                    fill_color=color, fill_opacity=0.25,
                                    stroke_color=color, stroke_width=2)
            box.move_to(pos + DOWN * 0.3)
            lbl = Text(title, font_size=15, color=color, weight=BOLD)
            lbl.move_to(box.get_center())
            panel_objs.append(VGroup(box, lbl))

        self.play(*[FadeIn(p) for p in panel_objs], run_time=0.4)

        # ═══ Bidirectional arrows ══════════════════════════════════
        modules = ["V2X Comm", "Time Sync", "Data Streaming"]

        arrows   = []
        mod_lbls = []
        for i, (mod, y_off) in enumerate(zip(modules, [0.5, -0.2, -0.9])):
            # Real World → Bridge
            a1 = DoubleArrow(panel_objs[0].get_right(), panel_objs[1].get_left(),
                              buff=0.1, color=COL_WHITE, stroke_width=1.5, tip_length=0.12)
            # Bridge → CARLA
            a2 = DoubleArrow(panel_objs[1].get_right(), panel_objs[2].get_left(),
                              buff=0.1, color=COL_WHITE, stroke_width=1.5, tip_length=0.12)
            # Position at different y heights
            a1.shift(UP * y_off * 0.05)
            a2.shift(UP * y_off * 0.05)

            mod_lbl = Text(mod, font_size=10, color=COL_WHITE, slant=ITALIC)
            mod_lbl.move_to(a1.get_center() + UP * 0.15 + UP * y_off * 0.05)

            arrows.extend([a1, a2])
            mod_lbls.append(mod_lbl)

        self.play(*[Create(a) for a in arrows], run_time=0.4)
        self.play(*[FadeIn(l) for l in mod_lbls], run_time=0.3)

        # ═══ Tagline ═══════════════════════════════════════════════
        tagline = Text('"Write once, run anywhere"', font_size=18,
                        color=COL_GOLD, slant=ITALIC, weight=BOLD)
        tagline.to_edge(DOWN, buff=0.8)
        self.play(Write(tagline), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.4)
