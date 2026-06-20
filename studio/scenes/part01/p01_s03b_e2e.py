"""P01-S03b - E2E: sensor stack -> neural policy -> action."""
from manimlib import *
from studio.components import (
    StudioScene,
    BG_CARD, BG_PAPER, BG_SECTION,
    PASTEL_BLUE, PASTEL_PINK, ACCENT_BLUE, PURPLE_MODEL,
    INK_DARK, INK_MID, LINE_ARROW,
    GREEN_FIX, RED_ERROR, CYAN_RADAR,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    h_arrow, vehicle_icon,
)


def _symbolic_mlp(*, n_cols: int = 3, n_rows: int = 3) -> VGroup:
    """Readable MLP icon: white nodes, purple glow, sparse synapses."""
    cols = VGroup()
    glows = VGroup()
    x_step = 0.7
    for xi in range(n_cols):
        col = VGroup()
        for _ in range(n_rows):
            glow = Circle(
                radius=0.13,
                fill_color=PURPLE_MODEL,
                fill_opacity=0.08,
                stroke_color=PURPLE_MODEL,
                stroke_width=1.1,
                stroke_opacity=0.2,
            )
            node = Circle(
                radius=0.078,
                fill_color=BG_PAPER,
                fill_opacity=1.0,
                stroke_color=PURPLE_MODEL,
                stroke_width=2.0,
            )
            glows.add(glow)
            col.add(node)
        col.arrange(DOWN, buff=0.22)
        col.move_to(xi * x_step * RIGHT)
        for glow, node in zip(glows[-n_rows:], col):
            glow.move_to(node)
        cols.add(col)
    lines = VGroup()
    for c1, c2 in zip(cols[:-1], cols[1:]):
        for d1 in c1:
            for d2 in c2:
                lines.add(Line(
                    d1.get_center(), d2.get_center(),
                    stroke_color=PURPLE_MODEL, stroke_width=1.45, stroke_opacity=0.5,
                ))
    return VGroup(glows, lines, cols)


def _sensor_symbol(kind: str) -> VGroup:
    if kind == "camera":
        body = RoundedRectangle(
            width=0.28, height=0.18, corner_radius=0.04,
            fill_color=ACCENT_BLUE, fill_opacity=0.14,
            stroke_color=ACCENT_BLUE, stroke_width=1.6,
        )
        lens = Circle(
            radius=0.052,
            fill_color=ACCENT_BLUE,
            fill_opacity=0.22,
            stroke_color=ACCENT_BLUE,
            stroke_width=1.4,
        )
        lens.move_to(body)
        bump = Rectangle(
            width=0.1, height=0.045,
            fill_color=ACCENT_BLUE, fill_opacity=0.18,
            stroke_width=0,
        )
        bump.next_to(body, UP, buff=0)
        return VGroup(body, lens, bump)
    if kind == "lidar":
        base = Dot(radius=0.035, color=ACCENT_BLUE)
        rays = VGroup(*[
            Line(ORIGIN, 0.2 * d, stroke_color=ACCENT_BLUE, stroke_width=1.5)
            for d in (UP, UR, RIGHT, DR, DOWN)
        ])
        rays.move_to(base)
        return VGroup(rays, base)
    core = Dot(radius=0.04, color=CYAN_RADAR)
    rings = VGroup(*[
        Circle(
            radius=r,
            stroke_color=CYAN_RADAR,
            stroke_width=1.2,
            stroke_opacity=0.55,
        )
        for r in (0.1, 0.17)
    ])
    rings.move_to(core)
    return VGroup(rings, core)


def _sensor_chip(label: str, kind: str) -> VGroup:
    shell = RoundedRectangle(
        width=1.55, height=0.42, corner_radius=0.1,
        fill_color=BG_PAPER, fill_opacity=0.92,
        stroke_color=ACCENT_BLUE, stroke_width=1.6,
    )
    icon = _sensor_symbol(kind)
    txt = Text(label, font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
    row = VGroup(icon, txt).arrange(RIGHT, buff=0.16)
    row.move_to(shell)
    return VGroup(shell, row)


def _sensor_card() -> VGroup:
    shell = RoundedRectangle(
        width=2.15, height=2.55, corner_radius=0.16,
        fill_color=BG_CARD, fill_opacity=0.92,
        stroke_color=ACCENT_BLUE, stroke_width=2.4,
    )
    shadow = shell.copy()
    shadow.set_fill(BLACK, opacity=0.06)
    shadow.set_stroke(width=0)
    shadow.shift(0.05 * RIGHT + 0.05 * DOWN)

    title = Text(
        "Sensor stack",
        font=FONT_PRIMARY, font_size=SIZE_LABEL,
        color=ACCENT_BLUE, weight=BOLD,
    )
    chips = VGroup(
        _sensor_chip("Camera", "camera"),
        _sensor_chip("LiDAR", "lidar"),
        _sensor_chip("Radar", "radar"),
    ).arrange(DOWN, buff=0.18)
    content = VGroup(title, chips).arrange(DOWN, buff=0.24)
    content.move_to(shell)

    if hasattr(shadow, "set_z_index"):
        shadow.set_z_index(-1)
    return VGroup(shell, content, shadow)


def _lock_badge() -> VGroup:
    badge = Circle(
        radius=0.31,
        fill_color=PASTEL_PINK,
        fill_opacity=1.0,
        stroke_color=RED_ERROR,
        stroke_width=2.6,
    )
    body = RoundedRectangle(
        width=0.27, height=0.21, corner_radius=0.04,
        fill_color=BG_PAPER,
        fill_opacity=1.0,
        stroke_color=RED_ERROR,
        stroke_width=1.8,
    )
    shackle = Arc(
        radius=0.12,
        start_angle=0,
        angle=PI,
        stroke_color=RED_ERROR,
        stroke_width=2.1,
    )
    shackle.move_to(body.get_top() + UP * 0.03)
    keyhole = Dot(radius=0.023, color=RED_ERROR)
    keyhole.move_to(body.get_center() + DOWN * 0.02)
    lock = VGroup(shackle, body, keyhole).move_to(badge)
    return VGroup(badge, lock)


def _policy_panel(net: Mobject) -> VGroup:
    shell = RoundedRectangle(
        width=4.0, height=3.05, corner_radius=0.18,
        fill_color=PASTEL_BLUE, fill_opacity=1.0,
        stroke_color=PURPLE_MODEL, stroke_width=3.0,
    )
    shadow = shell.copy()
    shadow.set_fill(BLACK, opacity=0.06)
    shadow.set_stroke(width=0)
    shadow.shift(0.06 * RIGHT + 0.06 * DOWN)

    core = RoundedRectangle(
        width=3.38, height=2.22, corner_radius=0.14,
        fill_color=BG_SECTION,
        fill_opacity=0.45,
        stroke_color=PURPLE_MODEL,
        stroke_width=1.6,
        stroke_opacity=0.32,
    )
    core.move_to(shell.get_center() + DOWN * 0.06)
    net.set_height(1.95)
    net.move_to(core)

    title = Text(
        "Single neural policy",
        font=FONT_PRIMARY, font_size=SIZE_LABEL,
        color=PURPLE_MODEL, weight=BOLD,
    )
    title.next_to(shell, UP, buff=0.14)

    lock = _lock_badge()
    lock.move_to(shell.get_corner(UR) + LEFT * 0.08 + DOWN * 0.08)

    if hasattr(shadow, "set_z_index"):
        shadow.set_z_index(-1)
        shell.set_z_index(0)
        core.set_z_index(1)
        net.set_z_index(2)
        title.set_z_index(3)
        lock.set_z_index(4)
    return VGroup(shell, core, net, title, lock, shadow)


def _action_card() -> VGroup:
    shell = RoundedRectangle(
        width=2.15, height=2.55, corner_radius=0.16,
        fill_color=BG_CARD, fill_opacity=0.92,
        stroke_color=GREEN_FIX, stroke_width=2.4,
    )
    shadow = shell.copy()
    shadow.set_fill(BLACK, opacity=0.06)
    shadow.set_stroke(width=0)
    shadow.shift(0.05 * RIGHT + 0.05 * DOWN)

    title = Text(
        "Action",
        font=FONT_PRIMARY, font_size=SIZE_LABEL,
        color=GREEN_FIX, weight=BOLD,
    )
    car = vehicle_icon(color=ACCENT_BLUE, scale=0.78)
    car[0].set_stroke(INK_DARK, width=1.6)
    curve = CurvedArrow(
        LEFT * 0.62 + DOWN * 0.58,
        RIGHT * 0.62 + DOWN * 0.28,
        angle=-TAU / 8,
        color=GREEN_FIX,
        stroke_width=3.0,
    )
    label = Text(
        "steer / brake",
        font=FONT_PRIMARY, font_size=SIZE_CAPS,
        color=INK_MID, weight=BOLD,
    )
    content = VGroup(title, car, curve, label).arrange(DOWN, buff=0.16)
    content.move_to(shell)

    if hasattr(shadow, "set_z_index"):
        shadow.set_z_index(-1)
    return VGroup(shell, content, shadow)


def _flow_dots(start, end, *, color: str) -> VGroup:
    dots = VGroup()
    for alpha in (0.28, 0.5, 0.72):
        dot = Dot(radius=0.055, color=color)
        dot.move_to(start + alpha * (end - start))
        dots.add(dot)
    return dots


def _check_icon(color: str) -> VGroup:
    disc = Circle(
        radius=0.13,
        fill_color=color, fill_opacity=1.0,
        stroke_color=color, stroke_width=1.2,
    )
    mark = VGroup(
        Line(LEFT * 0.055 + DOWN * 0.005, LEFT * 0.005 + DOWN * 0.055, stroke_color=BG_PAPER, stroke_width=2.4),
        Line(LEFT * 0.005 + DOWN * 0.055, RIGHT * 0.075 + UP * 0.065, stroke_color=BG_PAPER, stroke_width=2.4),
    )
    mark.move_to(disc)
    return VGroup(disc, mark)


def _warning_icon(color: str) -> VGroup:
    tri = Triangle(
        fill_color=color,
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.2,
    )
    tri.scale(0.16)
    bang = VGroup(
        Line(UP * 0.055, DOWN * 0.025, stroke_color=BG_PAPER, stroke_width=2.2),
        Dot(radius=0.012, color=BG_PAPER).shift(DOWN * 0.075),
    )
    bang.move_to(tri)
    return VGroup(tri, bang)


def _status_chip(label: str, *, color: str, warning: bool = False) -> VGroup:
    icon = _warning_icon(color) if warning else _check_icon(color)
    txt = Text(
        label,
        font=FONT_PRIMARY, font_size=SIZE_CAPS,
        color=color, weight=BOLD,
    )
    row = VGroup(icon, txt).arrange(RIGHT, buff=0.13)
    shell = RoundedRectangle(
        width=row.get_width() + 0.42,
        height=0.48,
        corner_radius=0.12,
        fill_color=BG_PAPER,
        fill_opacity=0.9,
        stroke_color=color,
        stroke_width=1.9,
    )
    row.move_to(shell)
    return VGroup(shell, row)


class P01S03BE2E(StudioScene):
    PART_NUM = 1
    SCENE_TITLE = "End-to-End Systems"

    def construct(self):
        self._open(self.SCENE_TITLE)

        net = _symbolic_mlp(n_cols=3, n_rows=3)
        sensor_card = _sensor_card()
        policy_panel = _policy_panel(net)
        action_card = _action_card()
        sensor_card.move_to(LEFT * 4.6 + UP * 0.25)
        policy_panel.move_to(UP * 0.25)
        action_card.move_to(RIGHT * 4.6 + UP * 0.25)

        policy_bg = VGroup(policy_panel[5], policy_panel[0], policy_panel[1], policy_panel[3])
        in_arrow = h_arrow(sensor_card, policy_panel, y=0.25, color=LINE_ARROW, thickness=3.0)
        out_arrow = h_arrow(policy_panel, action_card, y=0.25, color=LINE_ARROW, thickness=3.0)
        in_dots = _flow_dots(in_arrow.get_start(), in_arrow.get_end(), color=CYAN_RADAR)
        out_dots = _flow_dots(out_arrow.get_start(), out_arrow.get_end(), color=GREEN_FIX)

        self.play(FadeIn(sensor_card, shift=0.12 * RIGHT))
        self.play(
            ShowCreation(in_arrow),
            LaggedStart(*(FadeIn(dot, scale=1.25) for dot in in_dots), lag_ratio=0.14),
            run_time=0.65,
        )
        self.play(FadeIn(policy_bg, shift=0.12 * RIGHT))
        self.play(FadeIn(net[0], run_time=0.35))
        self.play(ShowCreation(net[1]), run_time=1.0, lag_ratio=0.02)
        self.play(LaggedStart(*(FadeIn(col) for col in net[2]), lag_ratio=0.08, run_time=0.65))
        self.play(FadeIn(policy_panel[4], scale=1.18), run_time=0.35)

        self.play(
            ShowCreation(out_arrow),
            LaggedStart(*(FadeIn(dot, scale=1.25) for dot in out_dots), lag_ratio=0.14),
            run_time=0.65,
        )
        self.play(FadeIn(action_card, shift=0.12 * RIGHT))

        badges = VGroup(*[
            _status_chip(label, color=color, warning=warning)
            for label, color, warning in [
                ("No handoff errors", GREEN_FIX, False),
                ("Joint objective", GREEN_FIX, False),
                ("Opaque diagnosis", RED_ERROR, True),
            ]
        ]).arrange(RIGHT, buff=0.22)
        badges.move_to(DOWN * 2.75)
        for b in badges:
            self.play(FadeIn(b, shift=0.18 * RIGHT), run_time=0.55)
            self.wait(0.25)
        self.wait(1.2)
        self._close()
