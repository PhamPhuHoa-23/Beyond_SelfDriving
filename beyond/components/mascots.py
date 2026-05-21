# beyond/components/mascots.py
# ─────────────────────────────────────────────────────────────────
# PI (curious questioner) and CAR (narrator/guide) mascots.
# Fully geometric — no SVG dependency.
# Designed from scratch for the BEYOND_SELFDRIVING animation guide.
# ─────────────────────────────────────────────────────────────────

from manim import *
from .colors import (
    BG_SPACE, TEXT_WHITE, GOLD, CYAN_NEON,
    BLUE_ELECTRIC, BG_PANEL, TEXT_DIM,
)


# ── PI mascot ────────────────────────────────────────────────────

class PiMascot(VGroup):
    """
    Circular 'Pi' mascot — the curious questioner.

    Parameters
    ----------
    height      : diameter in Manim units (default 1.0)
    body_color  : fill color of the head circle
    stroke_color: outline color
    """

    def __init__(
        self,
        height: float = 1.0,
        body_color: str = "#1E3A5F",    # deep blue body
        stroke_color: str = CYAN_NEON,
        **kwargs,
    ):
        super().__init__(**kwargs)
        r = height / 2

        # Head circle
        head = Circle(
            radius=r,
            fill_color=body_color, fill_opacity=1.0,
            stroke_color=stroke_color, stroke_width=2.0,
        )

        # Eyes — two small bright dots
        ey = r * 0.28
        ex = r * 0.30
        er = r * 0.09
        eye_l = Dot(radius=er, color=TEXT_WHITE).move_to(
            head.get_center() + np.array([-ex, ey, 0])
        )
        eye_r = Dot(radius=er, color=TEXT_WHITE).move_to(
            head.get_center() + np.array([ex, ey, 0])
        )

        # Pupils
        pu_r = er * 0.45
        pupil_l = Dot(radius=pu_r, color="#0A0A0A").move_to(eye_l.get_center())
        pupil_r = Dot(radius=pu_r, color="#0A0A0A").move_to(eye_r.get_center())

        # Slight smile arc
        smile = Arc(
            radius=r * 0.30,
            start_angle=-PI * 0.85,
            angle=PI * 0.70,
            stroke_color=TEXT_WHITE,
            stroke_width=1.8,
        ).move_to(head.get_center() + DOWN * r * 0.20)

        # π symbol on forehead area
        pi_sym = MathTex(r"\pi", color=CYAN_NEON, font_size=int(r * 48))
        pi_sym.move_to(head.get_center() + DOWN * r * 0.15)

        self.body = head
        self.face_group = VGroup(eye_l, eye_r, pupil_l, pupil_r, smile)
        self.add(head, eye_l, eye_r, pupil_l, pupil_r, smile, pi_sym)
        self.scale(height / (r * 2))  # ensure final height matches param

    def idle_bounce(self, amplitude: float = 0.07, run_time: float = 0.7) -> Animation:
        return self.animate(rate_func=there_and_back, run_time=run_time).shift(UP * amplitude)


def create_pi_mascot(height: float = 1.0, **kw) -> PiMascot:
    return PiMascot(height=height, **kw)


# ── CAR mascot ────────────────────────────────────────────────────

class CarMascot(VGroup):
    """
    Side-view car silhouette — the narrator/guide.

    Parameters
    ----------
    height      : overall height in Manim units (default 1.2)
    body_color  : car body fill
    accent_color: headlight / wheel accent
    stroke_color: outline
    """

    def __init__(
        self,
        height: float = 1.2,
        body_color: str = "#1A3A6B",      # UCLA-ish navy
        accent_color: str = GOLD,
        stroke_color: str = CYAN_NEON,
        **kwargs,
    ):
        super().__init__(**kwargs)

        w = height * 2.4
        h = height * 0.75

        # Main body chassis
        body = RoundedRectangle(
            corner_radius=0.12,
            width=w, height=h,
            fill_color=body_color, fill_opacity=1.0,
            stroke_color=stroke_color, stroke_width=2.0,
        )

        # Cabin roof (raised section)
        roof_w = w * 0.52
        roof_h = h * 0.58
        roof = RoundedRectangle(
            corner_radius=0.09,
            width=roof_w, height=roof_h,
            fill_color=body_color, fill_opacity=1.0,
            stroke_color=stroke_color, stroke_width=1.8,
        ).align_to(body, UP).shift(DOWN * 0.05).shift(LEFT * w * 0.05)

        # Windshield window
        win_w = roof_w * 0.78
        win_h = roof_h * 0.62
        window = RoundedRectangle(
            corner_radius=0.06,
            width=win_w, height=win_h,
            fill_color="#4A90C4", fill_opacity=0.7,
            stroke_color=stroke_color, stroke_width=1.2,
        ).move_to(roof.get_center())

        # Wheels
        wr = h * 0.38
        wl = Circle(
            radius=wr,
            fill_color="#0D0D0D", fill_opacity=1.0,
            stroke_color=stroke_color, stroke_width=1.5,
        )
        wr_obj = wl.copy()
        wl.move_to(body.get_bottom() + LEFT * w * 0.27 + UP * wr * 0.25)
        wr_obj.move_to(body.get_bottom() + RIGHT * w * 0.27 + UP * wr * 0.25)

        # Hubcaps
        hub_r = wr * 0.38
        hub_l = Circle(radius=hub_r, fill_color=stroke_color, fill_opacity=0.9,
                       stroke_width=0).move_to(wl.get_center())
        hub_r_obj = hub_l.copy().move_to(wr_obj.get_center())

        # Headlight
        headlight = Ellipse(
            width=h * 0.22, height=h * 0.14,
            fill_color=accent_color, fill_opacity=0.95,
            stroke_width=0,
        ).move_to(body.get_right() + LEFT * h * 0.18 + UP * h * 0.18)

        # Taillight
        taillight = Rectangle(
            width=h * 0.08, height=h * 0.14,
            fill_color="#CC2200", fill_opacity=0.9,
            stroke_width=0,
        ).move_to(body.get_left() + RIGHT * h * 0.15 + UP * h * 0.18)

        self.body = body
        self.face_group = VGroup(window, headlight)
        self.add(
            body, roof, window,
            wl, wr_obj, hub_l, hub_r_obj,
            headlight, taillight,
        )
        self.set_height(height)

    def idle_bounce(self, amplitude: float = 0.05, run_time: float = 0.6) -> Animation:
        return self.animate(rate_func=there_and_back, run_time=run_time).shift(UP * amplitude)


def create_car_mascot(height: float = 1.2, **kw) -> CarMascot:
    return CarMascot(height=height, **kw)
