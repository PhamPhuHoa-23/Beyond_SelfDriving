"""P03-S10 OpenCDA-ROS bridge."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER,
    CYAN_RADAR, GOLD_RICH, INK_DARK, INK_MID, FONT_PRIMARY, SIZE_LABEL,
    SIZE_CAPS, vehicle_icon, rsu_icon,
)

SCRIPT = """OpenCDA-ROS bridges robotics middleware to simulation. Same stack, no rewrite."""


def _txt(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    return Text(text, font=FONT_PRIMARY, font_size=size, color=color, weight=weight)


def _packet(label: str, color: str) -> VGroup:
    chip = RoundedRectangle(
        width=1.15, height=0.28, corner_radius=0.08,
        fill_color=interpolate_color(color, WHITE, 0.72),
        fill_opacity=1.0,
        stroke_color=color, stroke_width=1.2,
    )
    text = _txt(label, size=SIZE_CAPS - 5, color=color, weight=BOLD)
    text.move_to(chip)
    return VGroup(chip, text)


def _world_panel(title: str, color: str, x: float, content: Mobject) -> VGroup:
    panel = RoundedRectangle(
        width=3.55, height=2.78, corner_radius=0.16,
        fill_color=interpolate_color(color, WHITE, 0.9),
        fill_opacity=0.94,
        stroke_color=color, stroke_width=2.4,
    )
    panel.move_to([x, 0.13, 0])
    title_mob = _txt(title, size=SIZE_LABEL, color=color, weight=BOLD)
    title_mob.next_to(panel, UP, buff=0.16)
    content.move_to(panel.get_center() + DOWN * 0.03)
    return VGroup(panel, content, title_mob)


def _real_world() -> VGroup:
    road = RoundedRectangle(width=2.8, height=0.78, corner_radius=0.08, fill_color="#DDE7F1", fill_opacity=1.0, stroke_width=0)
    road.shift(DOWN * 0.22)
    lanes = VGroup()
    for x in (-0.75, 0.0, 0.75):
        lanes.add(Line([x - 0.22, -0.22, 0], [x + 0.22, -0.22, 0], stroke_color=WHITE, stroke_width=2.0, stroke_opacity=0.75))
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.34).move_to(LEFT * 0.42 + DOWN * 0.22)
    cav = vehicle_icon(color=ACCENT_GREEN, scale=0.3).move_to(RIGHT * 0.72 + DOWN * 0.22)
    tower = rsu_icon(color=ACCENT_AMBER).scale(0.9).move_to(LEFT * 1.05 + UP * 0.6)
    rays = VGroup(
        DashedLine(tower.get_center(), ego.get_center(), stroke_color=CYAN_RADAR, stroke_width=1.2, dash_length=0.06, stroke_opacity=0.75),
        DashedLine(tower.get_center(), cav.get_center(), stroke_color=CYAN_RADAR, stroke_width=1.2, dash_length=0.06, stroke_opacity=0.75),
    )
    packets = VGroup(
        _packet("/lidar", ACCENT_BLUE),
        _packet("/v2x", ACCENT_AMBER),
        _packet("/tf", ACCENT_GREEN),
    ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    packets.scale(0.9)
    packets.move_to(RIGHT * 0.88 + UP * 0.62)
    label = _txt("ROS bag + live topics", size=SIZE_CAPS - 2, color=INK_MID, weight=BOLD)
    label.move_to(DOWN * 0.98)
    return VGroup(road, lanes, rays, ego, cav, tower, packets, label)


def _carla_world() -> VGroup:
    grid = VGroup()
    for x in (-0.78, 0.0, 0.78):
        grid.add(RoundedRectangle(width=0.34, height=2.0, corner_radius=0.04, fill_color="#DDE7F1", fill_opacity=1.0, stroke_width=0).move_to(RIGHT * x))
    for y in (-0.46, 0.28):
        grid.add(RoundedRectangle(width=2.65, height=0.3, corner_radius=0.04, fill_color="#DDE7F1", fill_opacity=1.0, stroke_width=0).move_to(UP * y))
    blocks = VGroup()
    for x, y, c in [(-1.0, 0.78, "#FDE68A"), (-0.32, 0.75, "#BAE6FD"), (0.58, 0.82, "#BBF7D0"), (1.05, -0.72, "#FDBA74"), (-0.92, -0.78, "#DDD6FE")]:
        block = Rectangle(width=0.42, height=0.36, fill_color=c, fill_opacity=1.0, stroke_color=INK_MID, stroke_width=0.8, stroke_opacity=0.28)
        block.move_to([x, y, 0])
        blocks.add(block)
    ego = vehicle_icon(color=ACCENT_GREEN, scale=0.26).move_to(RIGHT * 0.78 + UP * 0.28)
    ego.rotate(PI / 2)
    ghost = vehicle_icon(color=ACCENT_BLUE, scale=0.25).move_to(LEFT * 0.78 + DOWN * 0.46)
    label = _txt("CARLA digital scene", size=SIZE_CAPS - 2, color=INK_MID, weight=BOLD)
    label.move_to(DOWN * 1.04)
    return VGroup(grid, blocks, ego, ghost, label)


def _bridge_box() -> VGroup:
    body = RoundedRectangle(
        width=2.18, height=3.05, corner_radius=0.16,
        fill_color="#DCFCE7", fill_opacity=1.0,
        stroke_color=ACCENT_GREEN, stroke_width=2.7,
    )
    title = _txt("OpenCDA-ROS", size=SIZE_CAPS + 1, color=ACCENT_GREEN, weight=BOLD)
    title.set_width(1.82)
    title.move_to(body.get_top() + DOWN * 0.48)
    modules = VGroup()
    for label, color in [
        ("V2X comm", ACCENT_AMBER),
        ("time sync", CYAN_RADAR),
        ("data stream", ACCENT_BLUE),
    ]:
        chip = RoundedRectangle(width=1.48, height=0.34, corner_radius=0.08, fill_color=WHITE, fill_opacity=0.82, stroke_color=color, stroke_width=1.4)
        txt = _txt(label, size=SIZE_CAPS - 3, color=color, weight=BOLD)
        txt.move_to(chip)
        modules.add(VGroup(chip, txt))
    modules.arrange(DOWN, buff=0.15)
    modules.move_to(body.get_center() + DOWN * 0.18)
    port_l = Circle(radius=0.07, fill_color=ACCENT_GREEN, fill_opacity=1.0, stroke_width=0).move_to(body.get_left() + RIGHT * 0.08 + UP * 0.62)
    port_r = Circle(radius=0.07, fill_color=ACCENT_GREEN, fill_opacity=1.0, stroke_width=0).move_to(body.get_right() + LEFT * 0.08 + UP * 0.62)
    return VGroup(body, title, modules, port_l, port_r)


def _h_arrow(start: np.ndarray, end: np.ndarray, color: str) -> Arrow:
    return Arrow(start, end, buff=0, stroke_width=2.6, fill_color=color, max_tip_length_to_length_ratio=0.14)


class P03S10OpenCDAROS(StudioScene):
    PART_NUM = 3
    SCENE_TITLE = "OpenCDA-ROS Bridge"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        real = _world_panel("Real Vehicle", ACCENT_BLUE, -4.25, _real_world())
        sim = _world_panel("Simulation (CARLA)", ACCENT_AMBER, 4.25, _carla_world())
        bridge = _bridge_box().move_to(UP * 0.05)

        data_y = 0.82
        ctrl_y = -0.48
        real_r = real[0].get_right()[0] + 0.1
        sim_l = sim[0].get_left()[0] - 0.1
        bridge_l = bridge[0].get_left()[0] - 0.08
        bridge_r = bridge[0].get_right()[0] + 0.08
        arrows = VGroup(
            _h_arrow(np.array([real_r, data_y, 0]), np.array([bridge_l, data_y, 0]), ACCENT_GREEN),
            _h_arrow(np.array([bridge_r, data_y, 0]), np.array([sim_l, data_y, 0]), ACCENT_GREEN),
            _h_arrow(np.array([sim_l, ctrl_y, 0]), np.array([bridge_r, ctrl_y, 0]), CYAN_RADAR),
            _h_arrow(np.array([bridge_l, ctrl_y, 0]), np.array([real_r, ctrl_y, 0]), CYAN_RADAR),
        )
        data_lbl = _txt("data", size=SIZE_CAPS - 5, color=ACCENT_GREEN, weight=BOLD)
        data_lbl.move_to(LEFT * 1.78 + UP * (data_y + 0.24))
        ctrl_lbl = _txt("control", size=SIZE_CAPS - 5, color=CYAN_RADAR, weight=BOLD)
        ctrl_lbl.move_to(RIGHT * 1.78 + UP * (ctrl_y - 0.24))

        same_code = VGroup(
            _packet("perception", ACCENT_BLUE),
            _packet("planning", ACCENT_GREEN),
            _packet("control", GOLD_RICH),
        ).arrange(RIGHT, buff=0.18)
        same_code.move_to(DOWN * 2.05)
        brace = Brace(same_code, DOWN, buff=0.07)
        brace.set_color(GOLD_RICH)
        tagline = _txt("write once, run in real car or CARLA", size=SIZE_LABEL, color=GOLD_RICH, weight=BOLD)
        tagline.next_to(brace, DOWN, buff=0.1)

        self.play(FadeIn(real), FadeIn(sim), run_time=0.75)
        self.play(FadeIn(bridge, shift=UP * 0.15), run_time=0.55)
        self.play(LaggedStart(*(FadeIn(m) for m in bridge[2]), lag_ratio=0.15), run_time=0.45)
        self.play(ShowCreation(arrows[0]), ShowCreation(arrows[1]), FadeIn(data_lbl), run_time=0.55)
        self.play(ShowCreation(arrows[2]), ShowCreation(arrows[3]), FadeIn(ctrl_lbl), run_time=0.55)
        self.play(FadeIn(same_code), GrowFromCenter(brace), FadeIn(tagline), run_time=0.7)
        self.wait(1.8)
        self._close()
