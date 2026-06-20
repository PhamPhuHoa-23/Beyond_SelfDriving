"""P04-S04 CooPre masked voxel pretraining and data-efficiency result."""
from manimlib import *
import numpy as np

from studio.components import (
    StudioScene, BG_PAPER, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER, PASTEL_AMBER, CYAN_RADAR,
    GOLD_RICH, GOLD_KEY, GREEN_FIX, RED_ERROR, INK_DARK, INK_MID, INK_LIGHT, LINE_SEP,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon, agent_trail, contribution_badge,
)

SCRIPT = (
    "CooPre — Cooperative Pretraining for V2X — is the first self-supervised pretraining method "
    "designed for multi-agent cooperative perception, published at IROS 2025. "
    "CooPre masks forty percent of voxels and reconstructs them from cooperative "
    "context. With half the labels it reaches the full-data baseline, and with "
    "all labels it gains another four and a half AP points."
)


def text_label(text, size=SIZE_LABEL, color=INK_DARK, weight=NORMAL):
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def bev_grid(rows=8, cols=8, cell=0.5, color=ACCENT_BLUE):
    """Build a compact BEV voxel grid."""
    grid = VGroup()
    for r in range(rows):
        for c in range(cols):
            cell_sq = Square(side_length=cell)
            cell_sq.set_fill(color, opacity=0.28)
            cell_sq.set_stroke(color, width=1.2, opacity=0.6)
            cell_sq.move_to(np.array([
                (c - cols / 2 + 0.5) * cell,
                (r - rows / 2 + 0.5) * cell,
                0,
            ]))
            grid.add(cell_sq)
    return grid


def result_chart():
    """CooPre results reproduced from materials/images/part4/p4_s14_slide_023.png."""
    percentages = [20, 50, 80, 100]
    baseline = [0.309, 0.433, 0.478, 0.486]
    coopre = [0.409, 0.501, 0.519, 0.531]

    x_left = -5.9
    x_right = 1.6
    y_bottom = -2.15
    y_top = 1.55
    y_max = 0.60

    def y_pos(value):
        return y_bottom + value / y_max * (y_top - y_bottom)

    chart = VGroup()
    axes = VGroup(
        Line([x_left, y_bottom, 0], [x_right, y_bottom, 0]),
        Line([x_left, y_bottom, 0], [x_left, y_top, 0]),
    )
    axes.set_stroke(INK_DARK, width=2.0, opacity=0.9)
    chart.add(axes)

    for tick in [0.3, 0.4, 0.5, 0.6]:
        y = y_pos(tick)
        guide = Line([x_left, y, 0], [x_right, y, 0])
        guide.set_stroke(INK_MID, width=1.0, opacity=0.22)
        tick_label = text_label(f"{tick:.1f}", SIZE_CAPS - 2, INK_MID)
        tick_label.next_to([x_left, y, 0], LEFT, buff=0.12)
        chart.add(guide, tick_label)

    threshold = DashedLine(
        [x_left, y_pos(0.5), 0],
        [x_right, y_pos(0.5), 0],
        dash_length=0.12,
    )
    threshold.set_stroke(GOLD_RICH, width=2.2, opacity=0.8)
    chart.add(threshold)

    group_x = [-4.75, -2.95, -1.15, 0.65]
    bar_width = 0.48
    bars = VGroup()
    value_labels = VGroup()
    x_labels = VGroup()

    for x, pct, base_value, coopre_value in zip(group_x, percentages, baseline, coopre):
        for dx, value, color in [
            (-bar_width / 2, base_value, INK_MID),
            (bar_width / 2, coopre_value, ACCENT_TEAL),
        ]:
            height = y_pos(value) - y_bottom
            bar = Rectangle(width=bar_width, height=height)
            bar.set_fill(color, opacity=0.92)
            bar.set_stroke(color, width=1.0, opacity=1.0)
            bar.move_to([x + dx, y_bottom + height / 2, 0])
            bars.add(bar)

            value_label = text_label(f"{value:.3f}", SIZE_CAPS - 2, color, BOLD)
            value_label.next_to(bar, UP, buff=0.07)
            value_labels.add(value_label)

        pct_label = text_label(f"{pct}%", SIZE_CAPS, INK_DARK, BOLD)
        pct_label.move_to([x, y_bottom - 0.28, 0])
        x_labels.add(pct_label)

    axis_label = text_label("Labeled training data", SIZE_CAPS, INK_MID)
    axis_label.move_to([(x_left + x_right) / 2, y_bottom - 0.7, 0])

    legend_base = Square(side_length=0.17)
    legend_base.set_fill(INK_MID, opacity=0.92).set_stroke(width=0)
    legend_coopre = Square(side_length=0.17)
    legend_coopre.set_fill(ACCENT_TEAL, opacity=0.92).set_stroke(width=0)
    legend = VGroup(
        legend_base,
        text_label("Scratch", SIZE_CAPS - 1, INK_MID),
        legend_coopre,
        text_label("CooPre", SIZE_CAPS - 1, ACCENT_TEAL, BOLD),
    )
    legend.arrange(RIGHT, buff=0.12)
    legend.move_to([-3.85, 1.9, 0])

    chart_title = text_label("V2X-Real  |  mAP@0.5", SIZE_LABEL, INK_DARK, BOLD)
    chart_title.move_to([-2.15, 2.32, 0])

    chart.add(bars, value_labels, x_labels, axis_label, legend, chart_title)
    return chart, bars, value_labels


def _mini_encoder(color=ACCENT_AMBER):
    encoder = VGroup()
    heights = [0.8, 0.6, 0.4]
    widths = [0.15, 0.15, 0.15]
    for w, h in zip(widths, heights):
        rect = RoundedRectangle(width=w, height=h, corner_radius=0.03)
        rect.set_fill(color, opacity=0.85)
        rect.set_stroke(color, width=1.0, opacity=1.0)
        encoder.add(rect)
    encoder.arrange(RIGHT, buff=0.08)
    return encoder


def _mini_masked_grid(color=ACCENT_BLUE):
    grid = VGroup()
    rows, cols = 4, 4
    cell = 0.28
    rng = np.random.RandomState(42)
    mask_indices = rng.choice(16, 6, replace=False)
    for r in range(rows):
        for c in range(cols):
            cell_sq = Square(side_length=cell)
            idx = r * cols + c
            if idx in mask_indices:
                cell_sq.set_fill(INK_MID, opacity=0.05)
                cell_sq.set_stroke(INK_MID, width=0.8, opacity=0.15)
            else:
                cell_sq.set_fill(color, opacity=0.45)
                cell_sq.set_stroke(color, width=1.0, opacity=0.8)
            cell_sq.move_to(np.array([
                (c - cols / 2 + 0.5) * cell,
                (r - rows / 2 + 0.5) * cell,
                0,
            ]))
            grid.add(cell_sq)
    return grid


def _mini_reconstructed_grid(color=ACCENT_TEAL):
    grid = VGroup()
    rows, cols = 4, 4
    cell = 0.28
    for r in range(rows):
        for c in range(cols):
            cell_sq = Square(side_length=cell)
            cell_sq.set_fill(color, opacity=0.75)
            cell_sq.set_stroke(color, width=1.0, opacity=0.9)
            cell_sq.move_to(np.array([
                (c - cols / 2 + 0.5) * cell,
                (r - rows / 2 + 0.5) * cell,
                0,
            ]))
            grid.add(cell_sq)
    return grid


def _mini_bev_grid(rows=4, cols=4, cell=0.36, color=ACCENT_BLUE):
    grid = VGroup()
    for r in range(rows):
        for c in range(cols):
            cell_sq = Square(side_length=cell)
            cell_sq.set_fill(color, opacity=0.15)
            cell_sq.set_stroke(color, width=1.0, opacity=0.4)
            cell_sq.move_to(np.array([
                (c - cols / 2 + 0.5) * cell,
                (r - rows / 2 + 0.5) * cell,
                0,
            ]))
            grid.add(cell_sq)
    return grid


def _radar_waves(car, color=CYAN_RADAR):
    waves = VGroup()
    for i in range(2):
        wave = Circle(radius=0.1, stroke_color=color, stroke_width=1.0)
        wave.set_stroke(opacity=0.0)
        wave.progress = i * 0.5 # staggered start
        
        def wave_updater(mob, dt):
            mob.progress = (mob.progress + dt * 0.6) % 1.0
            mob.set_width(0.1 + mob.progress * 0.8)
            mob.move_to(car.get_center())
            car_fade = getattr(car, "fade_factor", 1.0)
            mob.set_stroke(opacity=0.45 * (1.0 - mob.progress) * car_fade)
            
        wave.add_updater(wave_updater)
        waves.add(wave)
    return waves


def _mini_detection_scene(with_boxes=False):
    road_fill = "#E2E8F0"
    road_h = RoundedRectangle(width=2.2, height=0.45, corner_radius=0.03, fill_color=road_fill, fill_opacity=0.82, stroke_width=0)
    road_v = RoundedRectangle(width=0.45, height=2.2, corner_radius=0.03, fill_color=road_fill, fill_opacity=0.82, stroke_width=0)
    
    car_ego = vehicle_icon(color=ACCENT_BLUE, scale=0.32)
    car_ego.move_to(LEFT * 0.45 + DOWN * 0.1)
    car_ego.fade_factor = 1.0
    
    car_cav = vehicle_icon(color=ACCENT_TEAL, scale=0.32)
    car_cav.move_to(RIGHT * 0.35 + UP * 0.35)
    car_cav.rotate(PI / 2)
    car_cav.fade_factor = 1.0
    
    # Ego car updater (moves right continuously relative to road_h, fades near boundaries)
    def ego_updater(mob, dt):
        mob.shift(RIGHT * 0.35 * dt)
        rel_x = mob.get_center()[0] - road_h.get_center()[0]
        half_w = road_h.get_width() / 2
        if rel_x > half_w + 0.1:
            mob.set_x(road_h.get_center()[0] - half_w - 0.1)
            rel_x = -half_w - 0.1
        fade_dist = 0.3
        right_dist = (half_w + 0.1) - rel_x
        left_dist = rel_x - (-half_w - 0.1)
        factor = min(right_dist / fade_dist, left_dist / fade_dist)
        factor = max(0.0, min(1.0, factor))
        mob.fade_factor = factor
        mob.set_opacity(factor)
            
    # CAV car updater (moves down continuously relative to road_v, fades near boundaries)
    def cav_updater(mob, dt):
        mob.shift(DOWN * 0.35 * dt)
        rel_y = mob.get_center()[1] - road_v.get_center()[1]
        half_h = road_v.get_height() / 2
        if rel_y < -half_h - 0.1:
            mob.set_y(road_v.get_center()[1] + half_h + 0.1)
            rel_y = half_h + 0.1
        fade_dist = 0.3
        bottom_dist = rel_y - (-half_h - 0.1)
        top_dist = (half_h + 0.1) - rel_y
        factor = min(bottom_dist / fade_dist, top_dist / fade_dist)
        factor = max(0.0, min(1.0, factor))
        mob.fade_factor = factor
        mob.set_opacity(factor)
            
    car_ego.add_updater(ego_updater)
    car_cav.add_updater(cav_updater)
    
    # V2X Radar communication waves
    waves_ego = _radar_waves(car_ego, CYAN_RADAR)
    waves_cav = _radar_waves(car_cav, ACCENT_TEAL)
    
    scene = VGroup(road_h, road_v, waves_ego, waves_cav, car_ego, car_cav)
    
    if with_boxes:
        box_ego = Rectangle(width=0.42, height=0.24, stroke_color=RED_ERROR, stroke_width=1.5)
        box_ego.add_updater(lambda mob: mob.move_to(car_ego.get_center()).set_stroke(opacity=getattr(car_ego, "fade_factor", 1.0)))
        
        box_cav = Rectangle(width=0.24, height=0.42, stroke_color=RED_ERROR, stroke_width=1.5)
        box_cav.add_updater(lambda mob: mob.move_to(car_cav.get_center()).set_stroke(opacity=getattr(car_cav, "fade_factor", 1.0)))
        
        scene.add(box_ego, box_cav)
        
    return scene


class P04S04CooPReMasked(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "CooPre: Masked Voxel Pretraining"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # ==========================================
        # FRAME 1: CooPre Framework Concept
        # ==========================================
        # Left side: Input
        input_title = text_label("MULTI-AGENT INPUT", SIZE_CAPS, INK_MID, BOLD).move_to(LEFT * 4.5 + UP * 1.4)
        input_scene = _mini_detection_scene(with_boxes=False) # Road + Cars (no bounding boxes yet)
        input_scene.scale(0.85).move_to(LEFT * 4.5 + UP * 0.0)
        input_group = VGroup(input_title, input_scene)

        # Middle: Stacked 3D Encoders
        encoder_top = _mini_encoder(ACCENT_AMBER).move_to(LEFT * 1.2 + UP * 1.2)
        lbl_encoder_top = text_label("3D ENCODER", size=9, color=ACCENT_AMBER, weight=BOLD).next_to(encoder_top, UP, buff=0.08)
        
        encoder_bot = _mini_encoder(ACCENT_AMBER).move_to(LEFT * 1.2 + DOWN * 1.4)
        lbl_encoder_bot = text_label("3D ENCODER", size=9, color=ACCENT_AMBER, weight=BOLD).next_to(encoder_bot, DOWN, buff=0.08)
        
        init_arrow = Arrow(encoder_top.get_bottom(), encoder_bot.get_top(), buff=0.1, stroke_width=1.8, stroke_color=GREEN_FIX, fill_color=GREEN_FIX)
        lbl_init = text_label("INITIALIZATION", size=8, color=GREEN_FIX, weight=BOLD).next_to(init_arrow, LEFT, buff=0.08)
        init_group = VGroup(encoder_top, lbl_encoder_top, encoder_bot, lbl_encoder_bot, init_arrow, lbl_init)

        # Stage Panels (Phase 1 & 2 Cards)
        panel_pretrain = RoundedRectangle(width=7.4, height=2.2, corner_radius=0.12,
                                          fill_color=ACCENT_TEAL, fill_opacity=0.02,
                                          stroke_color=ACCENT_TEAL, stroke_width=1.0, stroke_opacity=0.25)
        panel_pretrain.move_to(RIGHT * 1.6 + UP * 1.4)

        panel_finetune = RoundedRectangle(width=7.4, height=2.5, corner_radius=0.12,
                                          fill_color=GOLD_RICH, fill_opacity=0.02,
                                          stroke_color=GOLD_RICH, stroke_width=1.0, stroke_opacity=0.25)
        panel_finetune.move_to(RIGHT * 1.6 + DOWN * 1.15)

        # Top-Right: Pretraining
        pretrain_title = text_label("1. COOPERATIVE PRETRAINING (SELF-SUPERVISED)", SIZE_CAPS, ACCENT_TEAL, BOLD).move_to(RIGHT * 1.6 + UP * 2.2)
        grid_masked = _mini_masked_grid(ACCENT_BLUE).move_to(RIGHT * 1.5 + UP * 1.2)
        grid_recon = _mini_reconstructed_grid(ACCENT_TEAL).move_to(RIGHT * 4.2 + UP * 1.2)
        recon_arrow = Arrow(grid_masked.get_right(), grid_recon.get_left(), buff=0.12, stroke_width=1.5, stroke_color=ACCENT_TEAL, fill_color=ACCENT_TEAL)
        lbl_recon = text_label("RECONSTRUCT", size=8, color=ACCENT_TEAL, weight=BOLD).next_to(recon_arrow, UP, buff=0.06)
        pretrain_group = VGroup(panel_pretrain, pretrain_title, grid_masked, grid_recon, recon_arrow, lbl_recon)

        # Bottom-Right: Finetuning
        finetune_title = text_label("2. COOPERATIVE 3D DETECTION (SUPERVISED)", SIZE_CAPS, GOLD_RICH, BOLD).move_to(RIGHT * 1.6 + DOWN * 0.25)
        det_scene = _mini_detection_scene(with_boxes=True) # Road + Cars + Red bounding boxes
        det_scene.scale(0.85).move_to(RIGHT * 2.8 + DOWN * 1.4)
        finetune_group = VGroup(panel_finetune, finetune_title, det_scene)

        # Connecting arrows from Left Input to Middle Encoders
        arrow_to_top = Arrow(input_scene.get_right(), encoder_top.get_left(), buff=0.15, stroke_width=1.5, stroke_color=INK_MID, fill_color=INK_MID)
        arrow_to_bot = Arrow(input_scene.get_right(), encoder_bot.get_left(), buff=0.15, stroke_width=1.5, stroke_color=INK_MID, fill_color=INK_MID)
        
        # Connecting arrows from Middle Encoders to Right Tasks
        arrow_to_task_top = Arrow(encoder_top.get_right(), grid_masked.get_left(), buff=0.15, stroke_width=1.5, stroke_color=ACCENT_TEAL, fill_color=ACCENT_TEAL)
        arrow_to_task_bot = Arrow(encoder_bot.get_right(), det_scene.get_left(), buff=0.15, stroke_width=1.5, stroke_color=GOLD_RICH, fill_color=GOLD_RICH)
        
        connections = VGroup(arrow_to_top, arrow_to_bot, arrow_to_task_top, arrow_to_task_bot)

        # Play animations for Frame 1
        self.play(FadeIn(input_group), run_time=0.6)
        self.play(
            FadeIn(panel_pretrain),
            ShowCreation(arrow_to_top),
            FadeIn(encoder_top),
            FadeIn(lbl_encoder_top),
            run_time=0.6
        )
        self.play(
            ShowCreation(arrow_to_task_top),
            FadeIn(pretrain_title),
            FadeIn(grid_masked),
            run_time=0.6
        )
        self.play(ShowCreation(recon_arrow), FadeIn(lbl_recon), FadeIn(grid_recon), run_time=0.6)
        self.wait(0.5)
        
        self.play(
            ShowCreation(init_arrow),
            FadeIn(lbl_init),
            FadeIn(encoder_bot),
            FadeIn(lbl_encoder_bot),
            run_time=0.6
        )
        self.play(
            FadeIn(panel_finetune),
            FadeIn(finetune_title),
            FadeIn(det_scene),
            ShowCreation(arrow_to_bot),
            ShowCreation(arrow_to_task_bot),
            run_time=0.6
        )
        self.wait(11.8)

        # Transition out Frame 1
        frame1_all = VGroup(input_group, init_group, pretrain_group, finetune_group, connections)
        self.play(FadeOut(frame1_all), run_time=0.6)

        # Beat 2: mask BEV voxels and reconstruct them from another agent.
        grid = bev_grid(rows=8, cols=8, cell=0.48, color=ACCENT_BLUE)
        grid.move_to(DOWN * 0.25)
        self.play(LaggedStart(
            *(FadeIn(voxel, scale=0.6) for voxel in grid),
            lag_ratio=0.008,
            run_time=1.0,
        ))

        agent_a = vehicle_icon(color=ACCENT_BLUE, scale=0.74)
        agent_b = vehicle_icon(color=ACCENT_TEAL, scale=0.74)
        agent_a.move_to(grid.get_corner(UL) + np.array([-0.32, 0.32, 0]))
        agent_b.move_to(grid.get_corner(DR) + np.array([0.32, -0.32, 0]))
        self.play(GrowFromCenter(agent_a), GrowFromCenter(agent_b), run_time=0.5)

        beam_a = Line(agent_a.get_center(), grid.get_center())
        beam_a.set_stroke(CYAN_RADAR, width=1.5, opacity=0.55)
        beam_b = Line(agent_b.get_center(), grid.get_center())
        beam_b.set_stroke(ACCENT_TEAL, width=1.5, opacity=0.55)
        self.play(ShowCreation(beam_a), ShowCreation(beam_b), run_time=0.5)

        rng = np.random.RandomState(17)
        mask_indices = sorted(
            rng.choice(len(grid), int(len(grid) * 0.4), replace=False).tolist()
        )
        mask_caption = text_label(
            "40% hidden  \u2192  reconstruct from cooperative context",
            SIZE_LABEL,
            INK_DARK,
            BOLD,
        )
        mask_caption.to_edge(DOWN, buff=0.38)
        self.play(
            LaggedStart(
                *(
                    grid[i].animate
                    .set_fill(opacity=0.05)
                    .set_stroke(opacity=0.18)
                    for i in mask_indices
                ),
                lag_ratio=0.025,
                run_time=1.1,
            ),
            FadeIn(mask_caption),
        )

        packets = VGroup()
        packet_anims = []
        for idx in mask_indices[:18]:
            voxel = grid[idx]
            start = agent_b.get_center()
            midpoint = (start + voxel.get_center()) / 2 + np.array([
                rng.uniform(-0.25, 0.25),
                rng.uniform(0.15, 0.4),
                0,
            ])
            packet = Dot(radius=0.055)
            packet.set_fill(ACCENT_TEAL, opacity=1.0)
            packet.set_stroke(ACCENT_TEAL, width=0.8, opacity=1.0)
            packet.move_to(start)
            packets.add(packet)
            path = CubicBezier(start, midpoint, midpoint, voxel.get_center())
            packet_anims.append(MoveAlongPath(packet, path, rate_func=smooth))

        self.play(LaggedStart(*packet_anims, lag_ratio=0.045, run_time=2.0))
        self.play(
            LaggedStart(
                *(
                    grid[i].animate.set_fill(opacity=0.75).set_stroke(opacity=0.9)
                    for i in mask_indices
                ),
                lag_ratio=0.018,
                run_time=1.0,
            ),
            FadeOut(packets),
        )
        self.wait(0.35)

        # Transition out Frame 2
        self.play(
            FadeOut(grid),
            FadeOut(agent_a),
            FadeOut(agent_b),
            FadeOut(beam_a),
            FadeOut(beam_b),
            FadeOut(mask_caption),
            run_time=0.6,
        )

        # ==========================================
        # FRAME 1.5: Inductive Bias & Downstream Cooperation (Redesign)
        # ==========================================
        bias_title = text_label("INDUCTIVE BIAS FOR COOPERATIVE PERCEPTION", SIZE_CAPS, INK_DARK, BOLD).move_to(UP * 2.4)
        
        # Cards
        card_ego = RoundedRectangle(width=5.2, height=3.6, corner_radius=0.12,
                                    fill_color=ACCENT_BLUE, fill_opacity=0.02,
                                    stroke_color=INK_MID, stroke_width=1.0, stroke_opacity=0.25)
        card_ego.move_to(LEFT * 3.4 + DOWN * 0.4)
        lbl_card_ego = text_label("EGO — OCCLUDED VIEW", size=SIZE_CAPS, color=INK_DARK, weight=BOLD).move_to(LEFT * 3.4 + UP * 1.1)
        
        card_cav = RoundedRectangle(width=5.2, height=3.6, corner_radius=0.12,
                                    fill_color=ACCENT_TEAL, fill_opacity=0.02,
                                    stroke_color=ACCENT_TEAL, stroke_width=1.0, stroke_opacity=0.25)
        card_cav.move_to(RIGHT * 3.4 + DOWN * 0.4)
        lbl_card_cav = text_label("CAV — COMPLEMENTARY VIEW", size=SIZE_CAPS, color=ACCENT_TEAL, weight=BOLD).move_to(RIGHT * 3.4 + UP * 1.1)
        
        # Transmission Lane Label in the gap (centered at y = -0.4 mid-line)
        lbl_lane = text_label("COOPERATIVE SHARING", size=SIZE_CAPS - 4, color=ACCENT_AMBER, weight=BOLD)
        lbl_lane.move_to(DOWN * 0.4)
            
        # Grids (cell size scaled to 0.48)
        grid_ego = _mini_bev_grid(rows=4, cols=4, cell=0.48, color=ACCENT_BLUE)
        grid_ego.move_to(LEFT * 3.4 + DOWN * 0.4)
        
        # Set distinct present/obstacle/masked grid contrasts for EGO
        for idx in range(16):
            c = idx % 4
            if c in [0, 1]:  # Columns 0 and 1: sensed cells
                grid_ego[idx].set_fill(ACCENT_BLUE, opacity=0.30).set_stroke(ACCENT_BLUE, width=1.0, opacity=0.7)
            elif c == 2:  # Column 2: Obstacle footprint cells
                grid_ego[idx].set_fill(INK_DARK, opacity=0.80).set_stroke(INK_DARK, width=1.5, opacity=0.9)
            elif c == 3:  # Column 3: Masked cells
                grid_ego[idx].set_fill(INK_MID, opacity=0.05).set_stroke(INK_MID, width=0.8, opacity=0.15)
                
        # Masked cells "?" symbols (only in empty cells 3 and 15, to avoid target car silhouette overlap in 7 and 11)
        question_marks = VGroup()
        for idx in [3, 15]:
            q_mark = text_label("?", size=12, color=INK_MID, weight=BOLD)
            q_mark.move_to(grid_ego[idx].get_center())
            question_marks.add(q_mark)
            
        grid_cav = _mini_bev_grid(rows=4, cols=4, cell=0.48, color=ACCENT_TEAL)
        grid_cav.move_to(RIGHT * 3.4 + DOWN * 0.4)
        
        # Highlight CAV's complementary left column (indices [0, 4, 8, 12] nearest to the gap)
        for idx in range(16):
            c = idx % 4
            if c == 0:
                grid_cav[idx].set_fill(ACCENT_TEAL, opacity=0.70).set_stroke(ACCENT_TEAL, width=1.2, opacity=0.9)
            else:
                grid_cav[idx].set_fill(ACCENT_TEAL, opacity=0.30).set_stroke(ACCENT_TEAL, width=1.0, opacity=0.7)
                
        # Vehicles (Symmetric layout)
        ego_car = vehicle_icon(color=ACCENT_BLUE, scale=0.48)
        ego_car.move_to(LEFT * 5.0 + DOWN * 0.4)
        
        cav_car = vehicle_icon(color=ACCENT_TEAL, scale=0.48)
        cav_car.move_to(RIGHT * 5.0 + DOWN * 0.4)
        cav_car.rotate(PI) # Face left, towards the grid
        
        # Soft shadow-wedge over EGO's occluded column c=3 (x = -2.68)
        shadow_ego = Rectangle(width=0.48, height=1.92, fill_color=INK_DARK, fill_opacity=0.22, stroke_width=0)
        shadow_ego.move_to(LEFT * 2.68 + DOWN * 0.4)
        
        # Target Vehicles: consistent grey target car (INK_MID) across EGO and CAV
        # EGO Target: faint grey silhouette during setup
        ego_target_silhouette = vehicle_icon(color=INK_MID, scale=0.42)
        ego_target_silhouette.move_to(LEFT * 2.68 + DOWN * 0.4)
        ego_target_silhouette.set_opacity(0.25)
        
        # CAV Target: solid grey car (fully visible to CAV)
        target_cav = vehicle_icon(color=INK_MID, scale=0.42)
        target_cav.move_to(RIGHT * 2.68 + DOWN * 0.4)
        
        # Groupings (setup has no building_cav, building_ego, target_ghost, lane_bg, or lane_arrows)
        frame_bias_base = VGroup(
            bias_title, card_ego, lbl_card_ego, card_cav, lbl_card_cav, lbl_lane,
            grid_ego, grid_cav, ego_car, cav_car, shadow_ego, ego_target_silhouette, target_cav, question_marks
        )
        
        self.play(FadeIn(frame_bias_base), run_time=0.8)
        self.wait(2.2)
        
        # Step 2: Bold Amber Transmission Packets with trails & higher arc
        packets = VGroup()
        packet_anims = []
        for r in range(4):
            start = grid_cav[r * 4].get_center() # column c=0
            end = grid_ego[r * 4 + 3].get_center() # column c=3
            packet = Dot(radius=0.09)
            packet.set_fill(ACCENT_AMBER, opacity=1.0)
            packet.set_stroke(GOLD_RICH, width=1.6, opacity=1.0)
            packets.add(packet)
            mid = (start + end) / 2 + UP * 0.75
            path = CubicBezier(start, mid, mid, end)
            packet_anims.append(MoveAlongPath(packet, path, rate_func=smooth))
            
        trails = VGroup()
        for packet in packets:
            trail = agent_trail(packet, color=ACCENT_AMBER)
            trails.add(trail)
        self.add(trails)
        
        self.play(
            LaggedStart(*packet_anims, lag_ratio=0.15, run_time=1.5)
        )
        self.wait(0.4)
        
        # Step 3: Amber Reconstruction Payoff & Downstream Detection Box
        recon_anims = [
            grid_ego[idx].animate.set_fill(PASTEL_AMBER, opacity=0.55).set_stroke(ACCENT_AMBER, width=1.5, opacity=0.85)
            for idx in [3, 7, 11, 15]
        ]
        
        # Detected car appears at EGO's target location c=3 (resolves to solid grey car)
        detected_car = vehicle_icon(color=INK_MID, scale=0.42)
        detected_car.move_to(LEFT * 2.68 + DOWN * 0.4)
        
        # Red bounding box around the detected car
        bbox = Rectangle(width=0.56, height=0.32, stroke_color=RED_ERROR, stroke_width=2.0)
        bbox.move_to(detected_car.get_center())
        
        tag_detect = text_label("= COOPERATIVE DETECTION", size=SIZE_CAPS - 2, color=RED_ERROR, weight=BOLD)
        tag_detect.move_to(LEFT * 3.4 + DOWN * 2.6)
        
        connector = DashedLine(
            bbox.get_bottom() + DOWN * 0.05,
            [bbox.get_x(), tag_detect.get_top()[1] + 0.05, 0],
            dash_length=0.06,
        )
        connector.set_stroke(RED_ERROR, width=1.2, opacity=0.7)
        
        self.play(
            LaggedStart(*recon_anims, lag_ratio=0.15, run_time=1.0),
            FadeOut(question_marks),
            FadeOut(packets),
            FadeOut(trails),
            run_time=1.0
        )
        self.play(
            FadeOut(ego_target_silhouette),
            FadeIn(detected_car),
            FadeIn(bbox),
            FadeIn(tag_detect),
            ShowCreation(connector),
            run_time=0.6
        )
        self.play(
            Flash(detected_car, color=RED_ERROR, line_length=0.18, num_lines=8),
            run_time=0.6
        )
        self.wait(2.6)
        
        # Clean up and Fade out Frame 1.5 elements
        frame_bias_all = VGroup(frame_bias_base, bbox, tag_detect, connector, detected_car)
        
        self.play(
            FadeOut(frame_bias_all),
            run_time=0.6,
        )

        # Beat 2: show the exact data-efficiency results from the source slide.

        chart, bars, value_labels = result_chart()
        static_chart = VGroup(*[
            mob for mob in chart.submobjects
            if mob is not bars and mob is not value_labels
        ])
        self.play(FadeIn(static_chart), run_time=0.65)
        self.play(
            LaggedStart(
                *(GrowFromEdge(bar, DOWN) for bar in bars),
                lag_ratio=0.08,
                run_time=1.5,
            )
        )
        self.play(
            LaggedStart(
                *(FadeIn(label, shift=0.08 * UP) for label in value_labels),
                lag_ratio=0.05,
                run_time=0.7,
            )
        )

        result_50 = VGroup(
            text_label("50% labels", SIZE_LABEL, ACCENT_TEAL, BOLD),
            text_label("0.501 mAP", SIZE_LABEL + 4, INK_DARK, BOLD),
            text_label("> scratch at 100%: 0.486", SIZE_CAPS, INK_MID),
        )
        result_50.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        result_100 = VGroup(
            text_label("100% labels", SIZE_LABEL, GOLD_RICH, BOLD),
            text_label("0.531 mAP", SIZE_LABEL + 4, INK_DARK, BOLD),
            text_label("+0.045 mAP over scratch", SIZE_CAPS, INK_MID),
        )
        result_100.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        insights = VGroup(result_50, result_100)
        insights.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        insights.move_to(RIGHT * 4.35 + DOWN * 0.05)
        self.play(
            LaggedStart(
                FadeIn(result_50, shift=0.18 * LEFT),
                FadeIn(result_100, shift=0.18 * LEFT),
                lag_ratio=0.35,
                run_time=1.0,
            )
        )
        self.play(
            Flash(result_100[1], color=GOLD_RICH, line_length=0.22, num_lines=8),
            run_time=0.7,
        )

        badges = VGroup(
            contribution_badge("IROS 2025  |  UCLA DriveX", color=GOLD_KEY),
            contribution_badge("CVPR 2025 Workshop", color=ACCENT_BLUE),
        )
        badges.arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.25)
        self.play(LaggedStart(*(FadeIn(b) for b in badges), lag_ratio=0.15), run_time=0.6)
        self.wait(1.5)
        self._close()
