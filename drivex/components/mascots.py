# drivex/components/mascots.py
# ─────────────────────────────────────────────────────────────────
# Mascot builders for CAR (guide) and PI (curious questioner).
#
# Both return VGroup objects with:
#   .body          — main shape
#   .face_group    — eyes/mouth
#
# Priority: load SVG from assets/ if present, otherwise use
# fully geometric fallback so scenes always render.
# ─────────────────────────────────────────────────────────────────

from manim import *
import os

# Asset search path (relative to this file → project root → assets/)
_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")


def _try_svg(name: str):
    """Return SVGMobject if file exists, else None."""
    path = os.path.abspath(os.path.join(_ASSETS_DIR, name))
    if os.path.isfile(path):
        return SVGMobject(path)
    return None


# ── CAR mascot ──────────────────────────────────────────────────

class CarMascot(VGroup):
    """
    A simple side-view car character.
    Geometric fallback — replace assets/car_mascot.svg to upgrade.

    Params
    ------
    height      : overall height in Manim units (default 1.5)
    body_color  : car body fill
    window_color: window fill
    """

    def __init__(self, height: float = 1.5,
                 body_color: str = "#2E75B6",
                 window_color: str = "#AED6F1",
                 **kwargs):
        super().__init__(**kwargs)

        svg = _try_svg("car_mascot.svg")
        if svg is not None:
            svg.set_height(height)
            self.add(svg)
            self.body = svg
            self.face_group = VGroup()
            return

        # ── Geometric fallback ───────────────────────────────────
        w, h = height * 2.2, height * 0.9

        # Body
        body = RoundedRectangle(
            corner_radius=0.15, width=w, height=h,
            fill_color=body_color, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2,
        )

        # Cabin roof
        roof_w, roof_h = w * 0.55, h * 0.55
        roof = RoundedRectangle(
            corner_radius=0.1, width=roof_w, height=roof_h,
            fill_color=body_color, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2,
        ).move_to(body.get_top() + DOWN * roof_h * 0.4)

        # Window
        win_w, win_h = roof_w * 0.75, roof_h * 0.6
        window = RoundedRectangle(
            corner_radius=0.05, width=win_w, height=win_h,
            fill_color=window_color, fill_opacity=0.85,
            stroke_color=WHITE, stroke_width=1,
        ).move_to(roof.get_center())

        # Wheels
        wheel_r = h * 0.32
        wheel_l = Circle(radius=wheel_r,
                         fill_color="#222222", fill_opacity=1,
                         stroke_color=WHITE, stroke_width=1.5)
        wheel_r_obj = wheel_l.copy()
        wheel_l.move_to(body.get_bottom() + LEFT * w * 0.28 + UP * wheel_r * 0.3)
        wheel_r_obj.move_to(body.get_bottom() + RIGHT * w * 0.28 + UP * wheel_r * 0.3)

        # Hubcap dots
        hub_l = Dot(radius=wheel_r * 0.3, color=WHITE).move_to(wheel_l.get_center())
        hub_r = Dot(radius=wheel_r * 0.3, color=WHITE).move_to(wheel_r_obj.get_center())

        # Headlight
        headlight = Dot(radius=h * 0.08, color="#FFD700").move_to(
            body.get_right() + LEFT * 0.15 + UP * h * 0.2
        )

        self.body = body
        self.face_group = VGroup(window)
        self.add(body, roof, window,
                 wheel_l, wheel_r_obj, hub_l, hub_r,
                 headlight)
        self.set_height(height)


def create_car_mascot(height: float = 1.5, **kw) -> CarMascot:
    """Convenience factory function."""
    return CarMascot(height=height, **kw)


# ── PI mascot ────────────────────────────────────────────────────

class PiMascot(VGroup):
    """
    Small circular 'Pi' curious mascot.
    Geometric fallback — replace assets/pi_mascot.svg to upgrade.

    Params
    ------
    height  : diameter in Manim units (default 1.0)
    color   : body fill color
    """

    def __init__(self, height: float = 1.0,
                 color: str = "#E8A838",
                 **kwargs):
        super().__init__(**kwargs)

        svg = _try_svg("pi_mascot.svg")
        if svg is not None:
            svg.set_height(height)
            self.add(svg)
            self.body = svg
            self.face_group = VGroup()
            return

        r = height / 2
        # Head
        head = Circle(radius=r,
                      fill_color=color, fill_opacity=1,
                      stroke_color=WHITE, stroke_width=2)

        # Eyes
        eye_offset = r * 0.3
        eye_r = r * 0.1
        eye_l = Dot(radius=eye_r, color="#1A1A1A").move_to(
            head.get_center() + LEFT * eye_offset + UP * eye_offset * 0.4)
        eye_r_obj = Dot(radius=eye_r, color="#1A1A1A").move_to(
            head.get_center() + RIGHT * eye_offset + UP * eye_offset * 0.4)

        # Smile
        smile = Arc(radius=r * 0.35, angle=-PI * 0.55,
                    stroke_color="#1A1A1A", stroke_width=2)
        smile.move_to(head.get_center() + DOWN * r * 0.15)

        # π symbol on chest area
        pi_text = Text("π", font_size=int(r * 55), color="#1A1A1A", weight=BOLD)
        pi_text.move_to(head.get_center() + DOWN * r * 0.25)

        self.body = head
        self.face_group = VGroup(eye_l, eye_r_obj, smile)
        self.add(head, eye_l, eye_r_obj, smile, pi_text)
        self.set_height(height)


def create_pi_mascot(height: float = 1.0, **kw) -> PiMascot:
    """Convenience factory function."""
    return PiMascot(height=height, **kw)


# ── Idle bounce animation ────────────────────────────────────────

def idle_bounce(mobject, amplitude: float = 0.08, run_time: float = 0.8):
    """Returns a subtle up-down bounce animation (plays once)."""
    return Succession(
        mobject.animate(rate_func=there_and_back, run_time=run_time)
               .shift(UP * amplitude),
    )
