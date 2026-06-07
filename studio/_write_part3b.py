"""Write Part 3 scenes batch 2 — math-heavy + remaining."""
import os
BASE = "studio/scenes/part03"


def W(name, code):
    path = os.path.join(BASE, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"wrote {name}")


W("p03_s07_kalman_filter.py", '''"""P03-S07 Kalman Three Rivers — UNCERTAINTY_CLOUD."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_AMBER, GREEN_FIX, GOLD_KEY,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, SIZE_H1,
    pipeline_block, ambient_glow, markup,
)
SCRIPT = """Three sources, three weaknesses. Kalman fuses all into 100 Hz lane-level stream."""


class P03S07KalmanFilter(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Kalman Filter: Three Rivers"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # Three input streams from left
        # Pattern adapted from: Source_manim_reference/3b1b_videos/_2018/uncertainty.py
        node = RIGHT * 0.5

        def make_stream(start, end, color, width=3.0, n_dots=8, pulsed=False):
            pts = VGroup()
            for i in range(n_dots):
                t = i / (n_dots - 1)
                pos = start + t * (end - start)
                if pulsed:
                    d = Dot(radius=0.08, color=color)
                    d.set_opacity(0.9 if i % 2 == 0 else 0.3)
                else:
                    d = Dot(radius=0.06 + 0.04 * (1 - t), color=color)
                    d.set_opacity(0.7 + 0.3 * t)
                d.move_to(pos)
                pts.add(d)
            return pts

        gnss_start = LEFT * 5.5 + UP * 1.8
        imu_start = LEFT * 5.5 + ORIGIN
        lidar_start = LEFT * 5.5 + DOWN * 1.8
        confluence = LEFT * 0.2

        gnss_stream = make_stream(gnss_start, confluence, ACCENT_BLUE, width=4.0)
        imu_stream = make_stream(imu_start, confluence, ACCENT_AMBER, width=2.5)
        lidar_stream = make_stream(lidar_start, confluence, GREEN_FIX, pulsed=True)

        gnss_lbl = Text("GNSS  5 Hz", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_BLUE, weight=BOLD)
        gnss_lbl.next_to(gnss_start, LEFT, buff=0.15)
        imu_lbl = Text("IMU  100 Hz", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_AMBER, weight=BOLD)
        imu_lbl.next_to(imu_start, LEFT, buff=0.15)
        lidar_lbl = Text("LiDAR  1 Hz", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GREEN_FIX, weight=BOLD)
        lidar_lbl.next_to(lidar_start, LEFT, buff=0.15)

        self.play(
            LaggedStart(*(FadeIn(d, scale=0.4) for d in gnss_stream), lag_ratio=0.06, run_time=0.8),
            FadeIn(gnss_lbl),
        )
        self.play(
            LaggedStart(*(FadeIn(d, scale=0.4) for d in imu_stream), lag_ratio=0.06, run_time=0.8),
            FadeIn(imu_lbl),
        )
        self.play(
            LaggedStart(*(FadeIn(d, scale=0.4) for d in lidar_stream), lag_ratio=0.06, run_time=0.8),
            FadeIn(lidar_lbl),
        )

        # Kalman node
        kalman_box = pipeline_block("Kalman\nFilter", width=1.8, height=1.1,
                                    fill="#C8EDD0", stroke=GREEN_FIX)
        kalman_box.move_to(RIGHT * 1.2)
        glow = ambient_glow(kalman_box, color=GREEN_FIX, radius=0.9)
        self.play(FadeIn(kalman_box), FadeIn(glow))

        # Output stream: single smooth 100Hz
        out_stream = make_stream(RIGHT * 2.5, RIGHT * 5.0, GREEN_FIX, n_dots=10)
        out_lbl = Text("100 Hz  lane-level", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=GOLD_KEY, weight=BOLD)
        out_lbl.next_to(RIGHT * 5.0, RIGHT, buff=0.12)
        self.play(
            LaggedStart(*(FadeIn(d, scale=0.4) for d in out_stream), lag_ratio=0.05, run_time=0.8),
            FadeIn(out_lbl),
        )

        caption = Text(
            "5 Hz + 100 Hz + 1 Hz  ->  100 Hz lane-level",
            font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK,
        )
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption))
        self.wait(2)
        self._close()
''')

W("p03_s08_cooperfuse.py", '''"""P03-S08 CooperFuse Gaussian beauty."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, ACCENT_BLUE, ACCENT_GREEN,
    INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_H1,
)
SCRIPT = """NMS throws information away. CooperFuse fuses — and the result is more precise."""


def gaussian_ellipse(center, rx, ry, color, opacity=0.18, n_rings=4):
    """Concentric ellipse rings simulating Gaussian uncertainty.
    Pattern adapted from: Source_manim_reference/3b1b_videos/_2018/uncertainty.py
    """
    grp = VGroup()
    for i in range(n_rings):
        scale = (n_rings - i) / n_rings
        e = Ellipse(width=2 * rx * scale, height=2 * ry * scale,
                    fill_color=color, fill_opacity=opacity * (1 - scale * 0.6),
                    stroke_color=color, stroke_width=1.5 * (1 - i * 0.15),
                    stroke_opacity=0.7 * (1 - i * 0.2))
        e.move_to(center)
        grp.add(e)
    return grp


class P03S08CooperFuse(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "CooperFuse: Gaussian Fusion"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)

        # Two bounding boxes (offset)
        bb_v = RoundedRectangle(width=1.2, height=0.65, corner_radius=0.1,
                                fill_color=ACCENT_BLUE, fill_opacity=0.12,
                                stroke_color=ACCENT_BLUE, stroke_width=2.0)
        bb_i = RoundedRectangle(width=1.2, height=0.65, corner_radius=0.1,
                                fill_color=ACCENT_GREEN, fill_opacity=0.12,
                                stroke_color=ACCENT_GREEN, stroke_width=2.0)
        bb_v.move_to(LEFT * 2.5 + UP * 0.5)
        bb_i.move_to(LEFT * 2.5 + UP * 0.5 + np.array([0.35, 0.25, 0]))
        lbl_v = Text("Vehicle det.", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2, color=ACCENT_BLUE)
        lbl_i = Text("Infra det.", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2, color=ACCENT_GREEN)
        lbl_v.next_to(bb_v, DOWN, buff=0.08)
        lbl_i.next_to(bb_i, UP, buff=0.08)

        gauss_v = gaussian_ellipse(bb_v.get_center(), 0.75, 0.45, ACCENT_BLUE)
        gauss_i = gaussian_ellipse(bb_i.get_center(), 0.65, 0.4, ACCENT_GREEN)

        self.play(FadeIn(bb_v), FadeIn(bb_i), FadeIn(lbl_v), FadeIn(lbl_i))
        self.play(FadeIn(gauss_v), FadeIn(gauss_i))

        # Left side: NMS discards one with red X
        nms_lbl = Text("NMS", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=RED_ERROR, weight=BOLD)
        nms_lbl.move_to(LEFT * 2.5 + DOWN * 1.5)
        nms_sub = Text("Discards weaker detection", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2,
                       color=RED_ERROR)
        nms_sub.next_to(nms_lbl, DOWN, buff=0.06)
        self.play(FadeIn(nms_lbl), FadeIn(nms_sub))
        x1 = Line(bb_i.get_corner(UL), bb_i.get_corner(DR), stroke_color=RED_ERROR, stroke_width=3)
        x2 = Line(bb_i.get_corner(UR), bb_i.get_corner(DL), stroke_color=RED_ERROR, stroke_width=3)
        self.play(ShowCreation(x1), ShowCreation(x2))
        self.play(FadeOut(bb_i), FadeOut(gauss_i), FadeOut(lbl_i))
        self.wait(0.5)
        self.play(FadeOut(x1), FadeOut(x2), FadeOut(nms_lbl), FadeOut(nms_sub))
        self.play(FadeIn(bb_i), FadeIn(gauss_i), FadeIn(lbl_i))

        # Right side: CooperFuse multiplies Gaussians -> tighter result
        cf_lbl = Text("CooperFuse", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                      color=GREEN_FIX, weight=BOLD)
        cf_lbl.move_to(RIGHT * 2.5 + UP * 0.5)
        self.play(FadeIn(cf_lbl))

        # Show both Gaussians on right side
        gauss_v2 = gaussian_ellipse(RIGHT * 2.0 + UP * 0.6, 0.75, 0.45, ACCENT_BLUE)
        gauss_i2 = gaussian_ellipse(RIGHT * 2.85 + UP * 0.75, 0.65, 0.4, ACCENT_GREEN)
        self.play(FadeIn(gauss_v2), FadeIn(gauss_i2))

        # Tighter result crystallizes
        result = gaussian_ellipse(RIGHT * 2.4 + UP * 0.65, 0.35, 0.22, GREEN_FIX, opacity=0.35)
        result_bb = RoundedRectangle(width=0.75, height=0.42, corner_radius=0.08,
                                     fill_color=GREEN_FIX, fill_opacity=0.15,
                                     stroke_color=GREEN_FIX, stroke_width=2.5)
        result_bb.move_to(RIGHT * 2.4 + UP * 0.65)
        ok_lbl = Text("[OK] Tighter, more precise", font=FONT_PRIMARY, font_size=SIZE_LABEL - 2,
                      color=GREEN_FIX)
        ok_lbl.next_to(result_bb, DOWN, buff=0.1)
        self.play(FadeIn(result), GrowFromCenter(result_bb, run_time=0.8))
        self.play(FadeIn(ok_lbl))
        self.play(Flash(result_bb, color=GREEN_FIX, line_length=0.2, num_lines=8))

        self.wait(2)
        self._close()
''')

W("p03_s09_v2x_realo.py", '''"""P03-S09 V2X-ReaLO 32x compression."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, RED_ERROR, GREEN_FIX, GOLD_KEY, CYAN_RADAR, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL,
    pipeline_block, pipeline_arrow, pipeline_flow, v2x_link, key_number,
)
SCRIPT = """V2X-ReaLO hits the sweet spot at 0.5 MB per message — 32x compression."""


class P03S09V2XReaLO(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "V2X-ReaLO: BEV Compression"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        big_blob = Ellipse(width=3.5, height=2.2, fill_color=RED_ERROR, fill_opacity=0.18,
                           stroke_color=RED_ERROR, stroke_width=2.0)
        big_blob.move_to(LEFT * 4.0)
        big_lbl = Text("BEV Features\\n16 MB  FP32", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=RED_ERROR, weight=BOLD)
        big_lbl.move_to(big_blob)
        compress_block = pipeline_block("32x\\nCompression", width=1.8, height=1.0,
                                       fill="#FAE3B0", stroke=GOLD_KEY)
        compress_block.move_to(ORIGIN)
        small_blob = Ellipse(width=1.2, height=0.8, fill_color=GREEN_FIX, fill_opacity=0.25,
                             stroke_color=GREEN_FIX, stroke_width=2.0)
        small_blob.move_to(RIGHT * 3.5)
        small_lbl = Text("0.5 MB\\nV2X Ready", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                         color=GREEN_FIX, weight=BOLD)
        small_lbl.move_to(small_blob)
        self.play(FadeIn(big_blob), FadeIn(big_lbl))
        self.play(FadeIn(compress_block))
        arr1 = pipeline_arrow(big_blob, compress_block, color=RED_ERROR)
        arr2 = pipeline_arrow(compress_block, small_blob, color=GREEN_FIX)
        self.play(ShowCreation(arr1))
        self.play(GrowFromCenter(small_blob, run_time=0.8), FadeIn(small_lbl))
        self.play(ShowCreation(arr2))
        kn = key_number("32x", "compression  16 MB -> 0.5 MB", color=GOLD_KEY)
        kn.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(kn))
        self.wait(2)
        self._close()
''')

W("p03_s10_opencda_ros.py", '''"""P03-S10 OpenCDA-ROS bridge."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_GREEN, GOLD_RICH, CYAN_RADAR, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL,
    pipeline_block, pipeline_arrow,
)
SCRIPT = """OpenCDA-ROS bridges robotics middleware to simulation. No rewrite."""


class P03S10OpenCDAROS(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "OpenCDA-ROS Bridge"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        real = pipeline_block("Real-World\\nROS Bag", width=2.4, fill="#C8DCFA", stroke="#2563EB")
        bridge = pipeline_block("OpenCDA-ROS\\nBridge", width=2.4, fill="#C8EDD0", stroke=ACCENT_GREEN)
        sim = pipeline_block("CARLA\\nSimulation", width=2.4, fill="#FAE3B0", stroke="#D97706")
        row = VGroup(real, bridge, sim).arrange(RIGHT, buff=1.0).move_to(ORIGIN + UP * 0.5)
        self.play(LaggedStart(*(FadeIn(b) for b in row), lag_ratio=0.2))
        arr1 = pipeline_arrow(real, bridge, color=ACCENT_GREEN)
        arr2 = pipeline_arrow(bridge, sim, color=ACCENT_GREEN)
        arr_back1 = pipeline_arrow(sim, bridge, color=CYAN_RADAR)
        arr_back1.put_start_and_end_on(sim.get_left() + LEFT * 0.05, bridge.get_right() + RIGHT * 0.05)
        arr_back1.shift(DOWN * 0.3)
        arr_back2 = pipeline_arrow(bridge, real, color=CYAN_RADAR)
        arr_back2.put_start_and_end_on(bridge.get_left() + LEFT * 0.05, real.get_right() + RIGHT * 0.05)
        arr_back2.shift(DOWN * 0.3)
        self.play(ShowCreation(arr1), ShowCreation(arr2))
        self.play(ShowCreation(arr_back1), ShowCreation(arr_back2))
        cap = Text("Code runs on real car  =  code runs in CARLA — no rewrite",
                   font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
''')

W("p03_s11_simboost.py", '''"""P03-S11 CDA-SimBoost closed loop."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_GREEN, ACCENT_AMBER, CYAN_RADAR, GOLD_RICH, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL,
    pipeline_block, pipeline_arrow, pipeline_flow,
)
SCRIPT = """Real data builds a digital twin. The twin generates challenging scenarios."""


class P03S11SimBoost(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "CDA-SimBoost Loop"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        cards = [
            pipeline_block("Real Data", fill="#C8DCFA", stroke="#2563EB"),
            pipeline_block("Digital Twin", fill="#C8EDD0", stroke=ACCENT_GREEN),
            pipeline_block("Challenging\\nScenarios", fill="#FAE3B0", stroke=ACCENT_AMBER),
            pipeline_block("Train + Deploy", fill="#F9C8D8", stroke="#DB2777"),
        ]
        positions = [LEFT * 4 + UP * 1, LEFT * 1 + UP * 1, RIGHT * 2 + UP * 1, RIGHT * 4.5 + UP * 1]
        for c, p in zip(cards, positions):
            c.move_to(p)
        self.play(LaggedStart(*(FadeIn(c) for c in cards), lag_ratio=0.15))
        for i in range(len(cards) - 1):
            arr = pipeline_arrow(cards[i], cards[i + 1])
            self.play(ShowCreation(arr, run_time=0.3))
        # Loop back arrow
        loop = CurvedArrow(cards[-1].get_bottom(), cards[0].get_bottom(), angle=-TAU / 6,
                           fill_color=CYAN_RADAR, thickness=2.0)
        self.play(ShowCreation(loop))
        cap = Text("Closed loop: real  ->  twin  ->  scenarios  ->  deploy",
                   font=FONT_PRIMARY, font_size=SIZE_LABEL, color=GOLD_RICH)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
''')

W("p03_s12_digital_twin.py", '''"""P03-S12 Digital Twin scan reveal."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_TEAL, GOLD_RICH, CYAN_RADAR, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL,
    vehicle_icon, rsu_icon, scan_reveal, write_chiseled,
)
SCRIPT = """Scan a real intersection, build its digital twin. The twin moves when reality moves."""


class P03S12DigitalTwin(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Digital Twin"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        # Divider
        div = Line(UP * 3, DOWN * 3, stroke_color=INK_MID, stroke_width=1.5, stroke_opacity=0.4)
        self.play(ShowCreation(div))
        real_lbl = Text("Real", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        twin_lbl = Text("Digital Twin", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=CYAN_RADAR, weight=BOLD)
        real_lbl.move_to(LEFT * 3.5 + UP * 2.4)
        twin_lbl.move_to(RIGHT * 3.5 + UP * 2.4)
        self.play(FadeIn(real_lbl), FadeIn(twin_lbl))
        # Real side: plain icons
        rcar = vehicle_icon(color=INK_MID, scale=0.9).move_to(LEFT * 3 + DOWN * 0.5)
        rrsu = rsu_icon(color=INK_MID).scale(1.1).move_to(LEFT * 4 + UP * 0.8)
        self.play(FadeIn(rcar), FadeIn(rrsu))
        # Scan reveal: scan line sweeps L->R
        scan_line = Line(UP * 3.2, DOWN * 3.2, stroke_color=CYAN_RADAR, stroke_width=2.5)
        scan_line.move_to(LEFT * 6)
        self.play(scan_line.animate.move_to(RIGHT * 6), run_time=1.5, rate_func=linear)
        self.remove(scan_line)
        # Twin side: wireframe cyan icons
        tcar = vehicle_icon(color=CYAN_RADAR, scale=0.9).move_to(RIGHT * 3 + DOWN * 0.5)
        tcar.set_fill(opacity=0.25)
        trsu = rsu_icon(color=CYAN_RADAR).scale(1.1).move_to(RIGHT * 4 + UP * 0.8)
        trsu.set_fill(opacity=0.25)
        self.play(FadeIn(tcar), FadeIn(trsu))
        # Sync movement
        self.play(
            rcar.animate.shift(RIGHT * 0.5),
            tcar.animate.shift(RIGHT * 0.5),
            run_time=1.0,
        )
        cap = Text("OpenCDA -> real-time digital twin  (100ms lag)", font=FONT_PRIMARY,
                   font_size=SIZE_LABEL, color=GOLD_RICH)
        cap.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(cap))
        self.wait(2)
        self._close()
''')

W("p03_s13_infrax.py", '''"""P03-S13 InfraX 4 feature cards."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_GREEN, GOLD_KEY, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    grid_4, contribution_badge,
)
SCRIPT = """OpenCDA-InfraX: configurable sensors, modalities, weather, and maps."""


class P03S13InfraX(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "OpenCDA-InfraX"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        features = [
            ("Sensor Config", "LiDAR / Camera / Radar\\nadjustable per deployment", ACCENT_GREEN),
            ("Multi-Modality", "V2V / V2I / V2X / I2I\\nall modes covered", "#0891B2"),
            ("Weather Variation", "Rain / Fog / Snow\\nrealistic conditions", "#D97706"),
            ("Vector Maps", "HD maps with lane info\\nfull semantic detail", "#7C3AED"),
        ]
        cards = VGroup()
        for title, body, color in features:
            rect = RoundedRectangle(width=4.5, height=1.6, corner_radius=0.15,
                                    fill_color=BG_PAPER, fill_opacity=1.0,
                                    stroke_color=color, stroke_width=2.0)
            t_mob = Text(title, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=color, weight=BOLD)
            b_mob = Text(body, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_MID)
            grp = VGroup(t_mob, b_mob).arrange(DOWN, buff=0.08)
            grp.move_to(rect)
            cards.add(VGroup(rect, grp))
        cards.arrange_in_grid(2, 2, buff=0.4)
        cards.move_to(ORIGIN + DOWN * 0.2)
        self.play(LaggedStart(*(FadeIn(c, scale=0.85) for c in cards), lag_ratio=0.2))
        badge = contribution_badge("OpenCDA-InfraX Platform", color=GOLD_KEY)
        badge.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(badge))
        self.wait(2)
        self._close()
''')

W("p03_s14_summary.py", '''"""P03-S14 Part 3 Summary: 4 contribution badges."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_GREEN, GOLD_KEY, INK_DARK,
    FONT_PRIMARY, SIZE_LABEL,
    contribution_badge,
)
SCRIPT = """Four contributions: real smart intersection, calibration, real-time fusion, digital twin."""


class P03S14Summary(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Part 3 Contributions"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        contribs = [
            ("UCLA Smart Intersection  ·  Real deployment", ACCENT_GREEN),
            ("Time + Space Calibration  ·  83cm -> cm", "#0891B2"),
            ("CooperFuse  ·  Gaussian fusion beats NMS", ACCENT_GREEN),
            ("OpenCDA Digital Twin  ·  100ms real-time", GOLD_KEY),
        ]
        badges = VGroup()
        for txt, color in contribs:
            badges.add(contribution_badge(txt, color=color))
        badges.arrange(DOWN, buff=0.35)
        badges.move_to(ORIGIN + UP * 0.2)
        self.play(LaggedStart(*(FadeIn(b, shift=RIGHT * 0.2) for b in badges), lag_ratio=0.25))
        self.wait(2)
        self._close()
''')

W("p03_s15_bridge_to_p4.py", '''"""P03-S15 Bridge to Part 4."""
from manimlib import *
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_AMBER, GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_H1, SIZE_LABEL,
    write_chiseled,
)
SCRIPT = """Now it works. But efficient enough to deploy? Three bottlenecks are next."""


class P03S15BridgeToP4(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Bridge to Part 4"

    def construct(self):
        self.camera.background_color = BG_PAPER
        header = self._open(self.SCENE_TITLE)
        recap = Text("Now it works.", font=FONT_PRIMARY, font_size=SIZE_H1, color=INK_MID)
        recap.move_to(UP * 0.8)
        self.play(FadeIn(recap))
        forward = Text(
            "But is it efficient enough to deploy?",
            font=FONT_PRIMARY, font_size=SIZE_H1, color=GOLD_RICH,
        )
        forward.move_to(DOWN * 0.2)
        self.play(write_chiseled(forward, run_time=2.0))
        bottlenecks = ["Data", "Training", "Inference"]
        tags = VGroup()
        for name in bottlenecks:
            t = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL, color=ACCENT_AMBER, weight=BOLD)
            bg = RoundedRectangle(width=t.get_width() + 0.4, height=t.get_height() + 0.2,
                                  corner_radius=0.1, fill_color=BG_PAPER, fill_opacity=1.0,
                                  stroke_color=ACCENT_AMBER, stroke_width=2.0)
            t.move_to(bg)
            tags.add(VGroup(bg, t))
        tags.arrange(RIGHT, buff=0.5)
        tags.move_to(DOWN * 1.5)
        self.play(LaggedStart(*(FadeIn(t, shift=UP * 0.2) for t in tags), lag_ratio=0.2))
        self.wait(1.5)
        self._close()
''')

print("Batch 2 done (S07-S15)")
