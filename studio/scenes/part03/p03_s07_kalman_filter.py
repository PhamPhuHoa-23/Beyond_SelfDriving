"""P03-S07 Kalman Three Rivers — animated flowing lanes with updater-based motion."""
from manimlib import *
import numpy as np
from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_AMBER, GREEN_FIX, GOLD_KEY,
    INK_MID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    pipeline_block, ambient_glow,
)
SCRIPT = """Three sources, three weaknesses. Kalman fuses all into 100 Hz lane-level stream."""

# ── Layout ──────────────────────────────────────────────────────────────────
LABEL_X   = -5.5   # sensor name labels (center x)
LANE_X0   = -4.3   # dot stream starts (right of labels)
LANE_X1   =  0.6   # dot stream ends (just before Kalman box)
KALMAN_CX =  1.8   # Kalman box center
KALMAN_W  =  2.0
KALMAN_H  =  3.6   # tall enough to span all three lanes
OUT_X0    =  2.9   # output stream starts (right of box)
OUT_X1    =  5.8   # output stream ends

LANE_CFG = [
    # (y,    color,        name,    rate,     speed, spacing, radius)
    ( 1.4,  ACCENT_BLUE,  "GNSS",  "5 Hz",   0.9,   1.55,   0.11),
    ( 0.0,  ACCENT_AMBER, "IMU",   "100 Hz",  5.5,   0.27,   0.07),
    (-1.4,  GREEN_FIX,    "LiDAR", "1 Hz",   0.18,   3.0,    0.14),
]
FADE_ZONE = 0.55


def _make_flow_updater(color, speed, y, x0, x1, spacing):
    """Return an updater that moves dots rightward and wraps them at x0."""
    w = x1 - x0

    def updater(grp, dt):
        for d in grp:
            cx = d.get_center()[0] + speed * dt
            if cx > x1 + 0.15:          # past right edge → teleport left
                cx -= w + spacing
            d.move_to([cx, y, 0])
            # fade-in from left, fade-out into Kalman box
            if cx < x0:
                op = 0.0
            elif cx < x0 + FADE_ZONE:
                op = (cx - x0) / FADE_ZONE * 0.9
            elif cx > x1 - FADE_ZONE:
                op = max(0.0, (x1 - cx) / FADE_ZONE * 0.9)
            else:
                op = 0.9
            d.set_fill(color, opacity=op)

    return updater


def _make_dot_stream(y, color, speed, spacing, radius):
    """Create VGroup of dots pre-distributed along the lane + attach updater."""
    lane_w = LANE_X1 - LANE_X0
    n = max(int(lane_w / spacing) + 3, 3)
    dots = VGroup()
    for i in range(n):
        x = LANE_X0 + (i * spacing) % (lane_w + spacing)
        d = Dot(radius=radius)
        d.set_fill(color, opacity=0.0)
        d.set_stroke(width=0)
        d.move_to([x, y, 0])
        dots.add(d)
    dots.add_updater(_make_flow_updater(color, speed, y, LANE_X0, LANE_X1, spacing))
    return dots


def _make_output_stream():
    """Dense gold output stream from Kalman box to right edge."""
    spacing = 0.27
    out_w = OUT_X1 - OUT_X0
    n = max(int(out_w / spacing) + 3, 3)
    dots = VGroup()
    for i in range(n):
        x = OUT_X0 + (i * spacing) % (out_w + spacing)
        d = Dot(radius=0.08)
        d.set_fill(GOLD_KEY, opacity=0.0)
        d.set_stroke(width=0)
        d.move_to([x, 0, 0])
        dots.add(d)

    def updater(grp, dt):
        for d in grp:
            cx = d.get_center()[0] + 5.5 * dt
            if cx > OUT_X1 + 0.15:
                cx -= out_w + spacing
            d.move_to([cx, 0, 0])
            if cx < OUT_X0:
                op = 0.0
            elif cx < OUT_X0 + FADE_ZONE:
                op = (cx - OUT_X0) / FADE_ZONE * 0.9
            elif cx > OUT_X1 - FADE_ZONE:
                op = max(0.0, (OUT_X1 - cx) / FADE_ZONE * 0.9)
            else:
                op = 0.9
            d.set_fill(GOLD_KEY, opacity=op)

    dots.add_updater(updater)
    return dots


class P03S07KalmanFilter(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "Kalman Filter: Three Rivers"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # ── Phase 1: sensor labels ────────────────────────────────────────────
        lbl_groups = VGroup()
        for y, color, name, rate, *_ in LANE_CFG:
            name_t = Text(name, font=FONT_PRIMARY, font_size=SIZE_LABEL,
                          color=color, weight=BOLD)
            rate_t = Text(rate, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=color)
            name_t.move_to([LABEL_X, y + 0.16, 0])
            rate_t.next_to(name_t, DOWN, buff=0.04)
            lbl_groups.add(VGroup(name_t, rate_t))

        # Horizontal track lines — background tracks for dots to flow along
        track_lines = VGroup()
        for y, color, *_ in LANE_CFG:
            ln = Line(np.array([LANE_X0, y, 0]), np.array([LANE_X1, y, 0]),
                      stroke_color=color, stroke_width=1.8)
            ln.set_stroke(opacity=0.28)
            track_lines.add(ln)

        self.play(
            LaggedStart(*(FadeIn(g, shift=RIGHT * 0.3) for g in lbl_groups),
                        lag_ratio=0.35, run_time=0.9),
            FadeIn(track_lines),
        )

        # ── Phase 2: start flowing dot lanes ──────────────────────────────────
        streams = []
        for y, color, _, _, speed, spacing, radius in LANE_CFG:
            dots = _make_dot_stream(y, color, speed, spacing, radius)
            streams.append(dots)
            self.add(dots)

        self.wait(2.5)   # let the flow establish — updaters run during wait()

        # ── Phase 3: Kalman box + convergence arrows ──────────────────────────
        kalman_box = pipeline_block("Kalman Filter", width=KALMAN_W, height=KALMAN_H,
                                    fill="#C8EDD0", stroke=GREEN_FIX)
        kalman_box.move_to([KALMAN_CX, 0, 0])
        glow = ambient_glow(kalman_box, color=GREEN_FIX, radius=1.1)

        box_left = KALMAN_CX - KALMAN_W / 2   # 0.8

        # Diagonal convergence lines — no arrowhead needed, angle tells direction
        conv_lines = VGroup()
        for y, color, *_ in LANE_CFG:
            ln = Line(
                np.array([LANE_X1, y, 0]),
                np.array([box_left, 0, 0]),     # all converge to box center-left
                stroke_color=color, stroke_width=2.2,
            )
            conv_lines.add(ln)

        self.play(FadeIn(kalman_box), FadeIn(glow))
        self.play(LaggedStart(*(ShowCreation(ln) for ln in conv_lines), lag_ratio=0.2))
        self.wait(1.5)

        # ── Phase 4: output stream ─────────────────────────────────────────────
        box_right = KALMAN_CX + KALMAN_W / 2   # 2.8

        # Output track: connector line + faint background track
        out_connector = Line(
            np.array([box_right, 0, 0]), np.array([OUT_X0, 0, 0]),
            stroke_color=GOLD_KEY, stroke_width=2.5,
        )
        out_track = Line(
            np.array([OUT_X0, 0, 0]), np.array([OUT_X1, 0, 0]),
            stroke_color=GOLD_KEY, stroke_width=1.8,
        )
        out_track.set_stroke(opacity=0.30)
        out_lbl = Text("100 Hz  lane-level", font=FONT_PRIMARY, font_size=SIZE_LABEL,
                       color=GOLD_KEY, weight=BOLD)
        out_lbl.move_to([(OUT_X0 + OUT_X1) / 2, 0.45, 0])

        out_dots = _make_output_stream()
        self.add(out_dots)
        self.play(ShowCreation(out_connector), ShowCreation(out_track), FadeIn(out_lbl))
        self.wait(2.5)

        # ── Phase 5: caption ──────────────────────────────────────────────────
        caption = Text("5 Hz + 100 Hz + 1 Hz  →  100 Hz lane-level",
                       font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_MID)
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption))
        self.wait(3.0)

        # Stop updaters before _close() to prevent ghost motion
        for s in streams:
            s.clear_updaters()
        out_dots.clear_updaters()

        self._close()
