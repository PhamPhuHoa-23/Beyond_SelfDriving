"""P04-S02 V2X overview and deployment bottlenecks."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN,
    ACCENT_AMBER, RED_ERROR, PURPLE_MODEL, CYAN_RADAR, INK_DARK, INK_MID,
    LINE_GRID, FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS, SIZE_MICRO,
    vehicle_icon, rsu_icon, pedestrian_icon,
)

SCRIPT = """V2X fuses shared viewpoints into a world model. At deployment scale, data, training, and inference become the bottlenecks."""


def _txt(text: str, *, size: int = SIZE_CAPS, color: str = INK_DARK, weight=NORMAL) -> Text:
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def _road_intersection() -> VGroup:
    horizontal = RoundedRectangle(
        width=4.25, height=0.62, corner_radius=0.06,
        fill_color=LINE_GRID, fill_opacity=1.0, stroke_width=0,
    )
    vertical = RoundedRectangle(
        width=0.62, height=2.35, corner_radius=0.06,
        fill_color=LINE_GRID, fill_opacity=1.0, stroke_width=0,
    )
    lanes = VGroup(
        DashedLine(LEFT * 1.82, RIGHT * 1.82, dash_length=0.1, stroke_color=WHITE, stroke_width=1.6, stroke_opacity=0.88),
        DashedLine(DOWN * 0.92, UP * 0.92, dash_length=0.1, stroke_color=WHITE, stroke_width=1.6, stroke_opacity=0.88),
    )
    crosswalk = VGroup(*[
        Line(LEFT * 0.22, RIGHT * 0.22, stroke_color=WHITE, stroke_width=2.0, stroke_opacity=0.86)
        for _ in range(5)
    ]).arrange(DOWN, buff=0.08)
    crosswalk.move_to(RIGHT * 0.58 + UP * 0.48)
    return VGroup(horizontal, vertical, lanes, crosswalk)


def _sensor_wedge(source: np.ndarray, target: np.ndarray, color: str) -> Polygon:
    direction = target - source
    unit = direction / np.linalg.norm(direction)
    perp = np.array([-unit[1], unit[0], 0])
    return Polygon(
        source,
        target + perp * 0.48,
        target - perp * 0.48,
        fill_color=color,
        fill_opacity=0.11,
        stroke_color=color,
        stroke_width=1.0,
        stroke_opacity=0.38,
    )


def _v2x_scene() -> VGroup:
    roads = _road_intersection()
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.43).move_to(LEFT * 1.2 + DOWN * 0.08)
    cav = vehicle_icon(color=ACCENT_TEAL, scale=0.4).move_to(DOWN * 0.75 + RIGHT * 0.05)
    cav.rotate(PI / 2)
    rsu = rsu_icon(color=ACCENT_AMBER).scale(0.7).move_to(RIGHT * 1.45 + UP * 0.72)
    pedestrian = pedestrian_icon(color=RED_ERROR).scale(0.54).move_to(RIGHT * 0.62 + UP * 0.48)
    blocker = vehicle_icon(color=INK_MID, scale=0.47).move_to(LEFT * 0.1 + UP * 0.08)

    ego_view = _sensor_wedge(ego.get_center(), RIGHT * 0.08 + UP * 0.08, ACCENT_BLUE)
    cav_view = _sensor_wedge(cav.get_center(), pedestrian.get_center(), ACCENT_TEAL)
    rsu_view = _sensor_wedge(rsu.get_center(), pedestrian.get_center(), ACCENT_AMBER)
    links = VGroup(
        DashedLine(cav.get_center(), ego.get_center(), dash_length=0.07, stroke_color=CYAN_RADAR, stroke_width=1.4),
        DashedLine(rsu.get_center(), ego.get_center(), dash_length=0.07, stroke_color=CYAN_RADAR, stroke_width=1.4),
    )
    labels = VGroup(
        _txt("ego", size=SIZE_MICRO + 1, color=ACCENT_BLUE, weight=BOLD).next_to(ego, DOWN, buff=0.05),
        _txt("CAV", size=SIZE_MICRO + 1, color=ACCENT_TEAL, weight=BOLD).next_to(cav, LEFT, buff=0.05),
        _txt("RSU", size=SIZE_MICRO + 1, color=ACCENT_AMBER, weight=BOLD).next_to(rsu, UP, buff=0.04),
    )
    return VGroup(roads, ego_view, cav_view, rsu_view, links, pedestrian, blocker, ego, cav, rsu, labels)


def _single_agent_view() -> dict[str, Mobject]:
    roads = _road_intersection()
    ego = vehicle_icon(color=ACCENT_BLUE, scale=0.48).move_to(LEFT * 1.2 + DOWN * 0.08)
    blocker = vehicle_icon(color=INK_MID, scale=0.52).move_to(LEFT * 0.02 + UP * 0.08)
    pedestrian = pedestrian_icon(color=RED_ERROR).scale(0.58).move_to(RIGHT * 0.68 + UP * 0.22)
    pedestrian.set_opacity(0.24)

    ego_view = _sensor_wedge(ego.get_center(), blocker.get_center() + LEFT * 0.08, ACCENT_BLUE)
    ego_view.set_stroke(opacity=0.24, width=1.0)
    soft_veil = Polygon(
        blocker.get_center() + RIGHT * 0.43 + UP * 0.4,
        RIGHT * 1.28 + UP * 0.18,
        RIGHT * 1.28 + DOWN * 0.4,
        blocker.get_center() + RIGHT * 0.43 + DOWN * 0.04,
        fill_color=INK_MID,
        fill_opacity=0.07,
        stroke_color=INK_MID,
        stroke_width=0.8,
        stroke_opacity=0.12,
    )

    ego_label = _txt("ego", size=SIZE_MICRO + 1, color=ACCENT_BLUE, weight=BOLD).next_to(ego, DOWN, buff=0.05)
    view_label = _pill_label("single-agent view", ACCENT_BLUE)
    view_label.next_to(roads, UP, buff=0.24)
    los_note = _txt("ego sees only its own line of sight", size=SIZE_CAPS, color=ACCENT_BLUE, weight=BOLD)
    los_note.next_to(roads, DOWN, buff=0.32)
    hidden_label = _txt("hidden from ego", size=SIZE_MICRO + 1, color=INK_MID, weight=BOLD)
    hidden_label.next_to(soft_veil, DOWN, buff=0.06)

    base = VGroup(roads, blocker, ego, ego_label)
    sight = VGroup(ego_view)
    occlusion = VGroup(pedestrian, soft_veil, hidden_label)
    notes = VGroup(view_label, los_note)
    group = VGroup(base, sight, occlusion, notes)
    return {
        "group": group,
        "base": base,
        "sight": sight,
        "occlusion": occlusion,
        "view_label": view_label,
        "los_note": los_note,
    }


def _fusion_view() -> VGroup:
    frame = RoundedRectangle(
        width=2.05, height=1.52, corner_radius=0.12,
        fill_color=interpolate_color(ACCENT_TEAL, WHITE, 0.94),
        fill_opacity=1.0, stroke_color=ACCENT_TEAL, stroke_width=1.5,
        stroke_opacity=0.72,
    )
    hub_glow = Circle(
        radius=0.2,
        fill_color=ACCENT_GREEN,
        fill_opacity=0.08,
        stroke_width=0,
    )
    hub = Circle(
        radius=0.115,
        fill_color=ACCENT_GREEN,
        fill_opacity=1.0,
        stroke_color=WHITE,
        stroke_width=1.4,
    )
    node_positions = [
        LEFT * 0.68 + UP * 0.42,
        RIGHT * 0.1 + UP * 0.52,
        RIGHT * 0.68 + UP * 0.18,
        RIGHT * 0.48 + DOWN * 0.42,
        LEFT * 0.62 + DOWN * 0.36,
    ]
    nodes = VGroup()
    arrows = VGroup()
    for pos in node_positions:
        node = Circle(
            radius=0.11,
            fill_color=interpolate_color(ACCENT_TEAL, WHITE, 0.96),
            fill_opacity=1.0,
            stroke_color=INK_MID,
            stroke_width=1.0,
            stroke_opacity=0.52,
        ).move_to(pos)
        nodes.add(node)
        arrows.add(Arrow(
            node.get_center(),
            hub.get_center(),
            buff=0.13,
            stroke_width=0.9,
            fill_color=ACCENT_TEAL,
            stroke_color=ACCENT_TEAL,
            stroke_opacity=0.72,
            max_tip_length_to_length_ratio=0.12,
        ))
    temporal_ring = Circle(
        radius=0.25,
        fill_opacity=0,
        stroke_color=ACCENT_AMBER,
        stroke_width=0.9,
        stroke_opacity=0.28,
    ).move_to(hub)
    plus = VGroup(
        Line(LEFT * 0.05, RIGHT * 0.05, stroke_color=WHITE, stroke_width=1.25),
        Line(DOWN * 0.05, UP * 0.05, stroke_color=WHITE, stroke_width=1.25),
    ).move_to(hub)
    graph = VGroup(arrows, nodes, temporal_ring, hub_glow, hub, plus)
    graph.move_to(frame)
    return VGroup(frame, graph)


def _data_icon(color: str) -> VGroup:
    points = VGroup(*[
        Dot(radius=0.035, fill_color=color, fill_opacity=0.78, stroke_width=0).move_to([x, y, 0])
        for x, y in [(-0.34, 0.2), (-0.12, 0.32), (0.14, 0.22), (0.32, 0.05), (-0.25, -0.1), (0.02, -0.2)]
    ])
    box = RoundedRectangle(width=0.5, height=0.32, corner_radius=0.04, fill_opacity=0, stroke_color=color, stroke_width=1.5)
    box.move_to(RIGHT * 0.15)
    return VGroup(points, box)


def _training_icon(color: str) -> VGroup:
    chip = RoundedRectangle(
        width=0.62, height=0.5, corner_radius=0.06,
        fill_color=interpolate_color(color, WHITE, 0.72),
        fill_opacity=1, stroke_color=color, stroke_width=1.5,
    )
    core = _txt("GPU", size=SIZE_MICRO, color=color, weight=BOLD).move_to(chip)
    tasks = VGroup(*[
        Circle(radius=0.08, fill_color=color, fill_opacity=0.22, stroke_color=color, stroke_width=1.0)
        for _ in range(3)
    ]).arrange(DOWN, buff=0.08).move_to(LEFT * 0.52)
    links = VGroup(*[
        Line(task.get_right(), chip.get_left(), stroke_color=color, stroke_width=1.1)
        for task in tasks
    ])
    return VGroup(links, tasks, chip, core)


def _inference_icon(color: str) -> VGroup:
    chip = RoundedRectangle(
        width=0.58, height=0.48, corner_radius=0.06,
        fill_color=interpolate_color(color, WHITE, 0.74),
        fill_opacity=1, stroke_color=color, stroke_width=1.5,
    ).move_to(LEFT * 0.22)
    clock = Circle(radius=0.28, fill_opacity=0, stroke_color=color, stroke_width=1.5).move_to(RIGHT * 0.38)
    hands = VGroup(
        Line(clock.get_center(), clock.get_center() + UP * 0.14, stroke_color=color, stroke_width=1.5),
        Line(clock.get_center(), clock.get_center() + RIGHT * 0.12, stroke_color=color, stroke_width=1.5),
    )
    return VGroup(chip, clock, hands)


def _bottleneck_card(number: str, title: str, body: str, color: str, icon: Mobject) -> VGroup:
    card = RoundedRectangle(
        width=3.65, height=1.35, corner_radius=0.14,
        fill_color=interpolate_color(color, WHITE, 0.92),
        fill_opacity=1.0, stroke_color=color, stroke_width=2.0,
    )
    number_mob = _txt(number, size=SIZE_LABEL + 2, color=ACCENT_AMBER, weight=BOLD)
    number_mob.move_to(card.get_left() + RIGHT * 0.3 + UP * 0.37)
    icon.scale(0.78).move_to(card.get_left() + RIGHT * 0.84 + DOWN * 0.12)
    title_mob = _txt(title, size=SIZE_LABEL - 1, color=color, weight=BOLD)
    body_mob = _txt(body, size=SIZE_CAPS - 2, color=INK_MID)
    copy = VGroup(title_mob, body_mob).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    copy.move_to(card.get_center() + RIGHT * 0.58)
    return VGroup(card, number_mob, icon, copy)


def _pill_label(text: str, color: str) -> VGroup:
    label = _txt(text, size=SIZE_CAPS, color=color, weight=BOLD)
    box = RoundedRectangle(
        width=label.get_width() + 0.36,
        height=label.get_height() + 0.18,
        corner_radius=0.11,
        fill_color=interpolate_color(color, WHITE, 0.86),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.4,
    )
    label.move_to(box)
    return VGroup(box, label)


def _scale_callout(title: str, body: str, color: str, icon: Mobject) -> VGroup:
    panel = RoundedRectangle(
        width=3.05,
        height=0.86,
        corner_radius=0.12,
        fill_color=interpolate_color(color, WHITE, 0.92),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.6,
    )
    icon.scale(0.58).move_to(panel.get_left() + RIGHT * 0.48)
    title_mob = _txt(title.upper(), size=SIZE_CAPS + 1, color=color, weight=BOLD)
    body_mob = _txt(body.upper(), size=SIZE_MICRO, color=INK_MID)
    copy = VGroup(title_mob, body_mob).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
    copy.move_to(panel.get_left() + RIGHT * 0.98, aligned_edge=LEFT)
    return VGroup(panel, icon, copy)


def _edge_chip(color: str = ACCENT_AMBER) -> VGroup:
    chip = RoundedRectangle(
        width=0.5,
        height=0.38,
        corner_radius=0.06,
        fill_color=interpolate_color(color, WHITE, 0.72),
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.2,
    )
    lines = VGroup(*[
        Line(LEFT * 0.12, RIGHT * 0.12, stroke_color=color, stroke_width=1.0)
        for _ in range(3)
    ]).arrange(DOWN, buff=0.05).move_to(chip)
    return VGroup(chip, lines)


def _tiny_intersection(color: str = ACCENT_AMBER) -> VGroup:
    road_h = RoundedRectangle(
        width=1.2,
        height=0.16,
        corner_radius=0.03,
        fill_color=LINE_GRID,
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.0,
    )
    road_v = RoundedRectangle(
        width=0.16,
        height=0.9,
        corner_radius=0.03,
        fill_color=LINE_GRID,
        fill_opacity=1.0,
        stroke_color=color,
        stroke_width=1.0,
    )
    node = Dot(radius=0.08, color=ACCENT_GREEN).move_to(ORIGIN)
    rsu = Dot(radius=0.06, color=color).move_to(RIGHT * 0.38 + UP * 0.25)
    return VGroup(road_h, road_v, node, rsu)


def _city_deployment_map() -> VGroup:
    grid = VGroup()
    for row in range(3):
        for col in range(4):
            node = _tiny_intersection()
            node.move_to(RIGHT * (col - 1.5) * 1.35 + UP * (row - 1) * 0.9)
            grid.add(node)

    city_box = RoundedRectangle(
        width=6.05,
        height=3.15,
        corner_radius=0.16,
        fill_color=interpolate_color(ACCENT_AMBER, WHITE, 0.94),
        fill_opacity=1.0,
        stroke_color=ACCENT_AMBER,
        stroke_width=1.5,
        stroke_opacity=0.58,
    )

    vehicles = VGroup(*[
        vehicle_icon(color=ACCENT_BLUE if i % 2 == 0 else ACCENT_TEAL, scale=0.12)
        for i in range(8)
    ])
    # Set starting positions aligned to horizontal/vertical grid lines
    positions = [
        LEFT * 2.2 + UP * 0.9,        # 0: horizontal, moves right
        LEFT * 2.025 + DOWN * 0.5,    # 1: vertical, moves up
        RIGHT * 1.5 + UP * 0,         # 2: horizontal, moves left
        LEFT * 0.675 + UP * 0.8,      # 3: vertical, moves down
        LEFT * 1.7 + DOWN * 0.9,      # 4: horizontal, moves right
        RIGHT * 0.675 + DOWN * 0.8,   # 5: vertical, moves up
        RIGHT * 0.5 + UP * 0.9,       # 6: horizontal, moves left
        RIGHT * 2.025 + UP * 0.4,     # 7: vertical, moves down
    ]
    
    speeds = [1.2, 1.4, 1.0, 1.6, 1.3, 1.5, 1.1, 1.3]
    
    def make_updater(is_horizontal, initial_dir, speed):
        state = {"dir": initial_dir}
        def updater(mob, dt):
            if is_horizontal:
                mob.shift(RIGHT * state["dir"] * speed * dt)
                rel_x = mob.get_center()[0] - city_box.get_center()[0]
                if state["dir"] == 1 and rel_x > 2.75:
                    state["dir"] = -1
                    mob.rotate(PI)
                elif state["dir"] == -1 and rel_x < -2.75:
                    state["dir"] = 1
                    mob.rotate(PI)
            else:
                mob.shift(UP * state["dir"] * speed * dt)
                rel_y = mob.get_center()[1] - city_box.get_center()[1]
                if state["dir"] == 1 and rel_y > 1.35:
                    state["dir"] = -1
                    mob.rotate(PI)
                elif state["dir"] == -1 and rel_y < -1.35:
                    state["dir"] = 1
                    mob.rotate(PI)
        return updater

    for i, (vehicle, pos) in enumerate(zip(vehicles, positions)):
        vehicle.move_to(pos)
        is_horizontal = (i % 2 == 0)
        if is_horizontal:
            direction = 1 if i in (0, 4) else -1
            if direction == -1:
                vehicle.rotate(PI)
        else:
            direction = 1 if i in (1, 5) else -1
            if direction == 1:
                vehicle.rotate(PI / 2)
            else:
                vehicle.rotate(-PI / 2)
        vehicle.add_updater(make_updater(is_horizontal, direction, speeds[i]))

    edges = VGroup(*[
        _edge_chip().scale(0.42).move_to(grid[i].get_center() + RIGHT * 0.43 + UP * 0.28)
        for i in (1, 3, 8, 10)
    ])
    
    title = _txt("city-scale V2X deployment", size=SIZE_LABEL, color=ACCENT_AMBER, weight=BOLD)
    title.next_to(city_box, UP, buff=0.12)
    return VGroup(city_box, grid, vehicles, edges, title)


class P04S02V2XOverview(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "V2X: From Paradigm to Deployment"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # Frame 1: the paradigm, separated from deployment scale.
        top_y = 0.95
        arrow_y = 0.9

        single_agent = _single_agent_view()
        single_agent["group"].scale(1.22).move_to(UP * 0.55)

        v2x = _v2x_scene().scale(0.95).move_to(LEFT * 3.45 + UP * top_y)
        shared_label = _pill_label("shared viewpoints", ACCENT_TEAL)
        shared_label.next_to(v2x, DOWN, buff=0.18)

        fusion = _fusion_view().scale(1.22).move_to(RIGHT * 3.0 + UP * top_y)
        fusion_label = _pill_label("Spatial + Temporal fusion", ACCENT_GREEN)
        fusion_label.next_to(fusion, DOWN, buff=0.18)
        fusion_label.set_y(shared_label.get_y())
        fuse_arrow = Arrow(
            np.array([v2x.get_right()[0] + 0.08, arrow_y, 0]),
            np.array([fusion.get_left()[0] - 0.08, arrow_y, 0]),
            buff=0,
            stroke_width=1.45,
            fill_color=ACCENT_TEAL,
            stroke_color=ACCENT_TEAL,
            max_tip_length_to_length_ratio=0.055,
        )
        paradigm_note = _txt(
            "V2X PARADIGM",
            size=SIZE_LABEL + 6,
            color=INK_DARK,
            weight=BOLD,
        )
        paradigm_note.move_to(DOWN * 2.34)
        paradigm_rule = Line(
            paradigm_note.get_left() + DOWN * 0.18,
            paradigm_note.get_right() + DOWN * 0.18,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.5,
            stroke_opacity=0.62,
        )
        paradigm_group = VGroup(v2x, shared_label, fusion, fusion_label, fuse_arrow, paradigm_note, paradigm_rule)

        self.play(FadeIn(single_agent["base"]), FadeIn(single_agent["view_label"]), run_time=0.6)
        self.play(ShowCreation(single_agent["sight"]), FadeIn(single_agent["los_note"]), run_time=0.55)
        self.play(FadeIn(single_agent["occlusion"]), run_time=0.55)
        self.wait(3.0)
        self.play(single_agent["group"].animate.scale(0.58).move_to(LEFT * 3.45 + UP * top_y), run_time=0.55)
        self.play(
            FadeOut(single_agent["group"]),
            FadeIn(v2x[0]),
            FadeIn(v2x[1]),
            FadeIn(v2x[5]),
            FadeIn(v2x[6]),
            FadeIn(v2x[7]),
            run_time=0.65,
        )
        self.play(
            LaggedStart(
                ShowCreation(v2x[2]),
                ShowCreation(v2x[3]),
                ShowCreation(v2x[4]),
                FadeIn(v2x[8]),
                FadeIn(v2x[9]),
                FadeIn(v2x[10]),
                FadeIn(shared_label),
                lag_ratio=0.12,
            ),
            run_time=0.9,
        )
        self.play(ShowCreation(fuse_arrow), FadeIn(fusion), FadeIn(fusion_label), run_time=0.7)
        self.play(FadeIn(paradigm_note), ShowCreation(paradigm_rule), run_time=0.45)
        self.wait(6.0)
        self.play(FadeOut(paradigm_group), run_time=0.55)

        # Frame 2: the same paradigm multiplied to city scale.
        city_map = _city_deployment_map().move_to(LEFT * 1.95 + DOWN * 0.05)
        callouts = VGroup(
            _scale_callout("thousands", "of intersections", ACCENT_AMBER, _tiny_intersection(ACCENT_AMBER)),
            _scale_callout("millions", "of vehicles", ACCENT_BLUE, vehicle_icon(color=ACCENT_BLUE, scale=0.7)),
            _scale_callout("fixed budgets", "edge compute", ACCENT_GREEN, _edge_chip(ACCENT_GREEN).scale(1.1)),
            _scale_callout("runnable", "training pipelines", PURPLE_MODEL, _training_icon(PURPLE_MODEL)),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        callouts.move_to(RIGHT * 4.15 + UP * 0.35)

        funding_text = _txt("U.S. DOT smart-intersection programs", size=SIZE_MICRO + 1, color=ACCENT_AMBER, weight=BOLD)
        funding = RoundedRectangle(
            width=funding_text.get_width() + 0.46,
            height=0.38,
            corner_radius=0.1,
            fill_color=interpolate_color(ACCENT_AMBER, WHITE, 0.8),
            fill_opacity=1,
            stroke_color=ACCENT_AMBER,
            stroke_width=1.3,
        )
        funding_text.move_to(funding)
        funding_badge = VGroup(funding, funding_text)
        funding_badge.move_to(DOWN * 2.05 + LEFT * 1.95)

        deployment_group = VGroup(city_map, callouts, funding_badge)

        self.play(FadeIn(city_map[0]), FadeIn(city_map[4]), run_time=0.5)
        self.play(LaggedStart(*(FadeIn(node, scale=0.9) for node in city_map[1]), lag_ratio=0.04), run_time=0.85)
        self.play(FadeIn(city_map[2]), FadeIn(city_map[3]), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(callout, shift=LEFT * 0.15) for callout in callouts), lag_ratio=0.12), run_time=0.9)
        self.play(FadeIn(funding_badge), run_time=0.45)
        self.wait(8.5)
        self.play(FadeOut(deployment_group), run_time=0.55)

        cards = VGroup(
            _bottleneck_card("01", "DATA", "limited\nlabeled data", RED_ERROR, _data_icon(RED_ERROR)),
            _bottleneck_card("02", "TRAINING", "slow\nconvergence", PURPLE_MODEL, _training_icon(PURPLE_MODEL)),
            _bottleneck_card("03", "INFERENCE", "real-time\nedge hardware", ACCENT_GREEN, _inference_icon(ACCENT_GREEN)),
        ).arrange(RIGHT, buff=0.32)
        cards.move_to(DOWN * 0.55)

        scale_label = _txt("What breaks when the stack scales?", size=SIZE_LABEL + 3, color=INK_DARK, weight=BOLD)
        scale_label.move_to(UP * 1.72)
        scale_subtitle = _txt(
            "Three bottlenecks stand between V2X systems and real-world scalability.",
            size=SIZE_CAPS,
            color=INK_MID,
        )
        scale_subtitle.next_to(scale_label, DOWN, buff=0.18)
        guide = Line(LEFT * 5.25, RIGHT * 5.25, stroke_color=ACCENT_AMBER, stroke_width=1.5, stroke_opacity=0.55)
        guide.move_to(UP * 0.68)
        connectors = VGroup(*[
            Line(
                [card.get_center()[0], guide.get_y(), 0],
                [card.get_center()[0], card.get_top()[1] + 0.07, 0],
                stroke_color=ACCENT_AMBER, stroke_width=1.2, stroke_opacity=0.55,
            )
            for card in cards
        ])

        footer = _txt("Efficiency is the bridge from demo to deployment.", size=SIZE_LABEL, color=ACCENT_AMBER, weight=BOLD)
        footer.move_to(DOWN * 2.55)

        self.play(FadeIn(scale_label), FadeIn(scale_subtitle), run_time=0.45)
        self.play(ShowCreation(guide), ShowCreation(connectors), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(card, shift=UP * 0.18) for card in cards), lag_ratio=0.18), run_time=0.9)
        self.play(FadeIn(footer), run_time=0.35)
        self.wait(1.7)
        self._close()
