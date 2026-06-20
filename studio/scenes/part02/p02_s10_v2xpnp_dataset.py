"""P02-S10 - V2XPnP-Seq dataset stats."""
from manimlib import *

from studio.components import (
    StudioScene,
    ACCENT_TEAL,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    INK_MID,
    INK_LIGHT,
    ORANGE_INFRA,
    PURPLE_MODEL,
    SIZE_CAPS,
    SIZE_LABEL,
    key_number,
    rsu_icon,
    v2x_link,
    vehicle_icon,
)
from studio.scenes.part02._p02_helpers import road_grid_2d


SCRIPT = "V2XPnP-Seq covers V2V, V2I, V2X, and I2I with sequential real-world frames."


def make_continuous_waves(center_mob, color=CYAN_RADAR, max_radius=0.6, speed=0.8):
    waves = VGroup()
    for i in range(2):
        wave = Circle(radius=0.02, stroke_color=color, stroke_width=1.2)
        wave.set_stroke(opacity=0.0)
        wave.progress = i * 0.5  # Staggered start
        
        def wave_updater(mob, dt, cm=center_mob, mr=max_radius, sp=speed):
            mob.progress = (mob.progress + dt * sp) % 1.0
            r = 0.02 + mob.progress * mr
            mob.set_width(2 * r)
            mob.move_to(cm.get_center())
            op = getattr(cm, "current_opacity", 1.0)
            mob.set_stroke(opacity=0.5 * (1.0 - mob.progress) * op)
            
        wave.add_updater(wave_updater)
        waves.add(wave)
    return waves


def make_continuous_packets(start_mob, end_mob, color=CYAN_RADAR, speed=1.0, stagger=0.0):
    packet = Dot(radius=0.05, color=color)
    packet.progress = stagger
    
    def packet_updater(mob, dt, sm=start_mob, em=end_mob, sp=speed):
        mob.progress = (mob.progress + dt * sp) % 1.0
        p = mob.progress
        start_pt = sm.get_center()
        end_pt = em.get_center()
        mob.move_to(start_pt * (1 - p) + end_pt * p)
        if p < 0.2:
            opacity = p / 0.2
        elif p > 0.8:
            opacity = (1.0 - p) / 0.2
        else:
            opacity = 1.0
        op_s = getattr(sm, "current_opacity", 1.0)
        op_e = getattr(em, "current_opacity", 1.0)
        mob.set_opacity(opacity * op_s * op_e)
            
    packet.add_updater(packet_updater)
    return packet


def make_stat_card(value: str, label: str, color: str) -> VGroup:
    val_mob = Text(value, font=FONT_PRIMARY, font_size=38, color=color, weight=BOLD)
    lbl_mob = Text(label, font=FONT_PRIMARY, font_size=18, color=INK_MID)
    group = VGroup(val_mob, lbl_mob)
    group.arrange(DOWN, buff=0.1)
    return group


class P02S10V2XPnPDataset(StudioScene):
    PART_NUM = 2
    SCENE_TITLE = "V2XPnP-Seq Dataset"

    def construct(self):
        self._open(self.SCENE_TITLE)
        # Pattern adapted from: Source_manim_reference/welchlabs_videos/_2026/vla/p31_61_1.py:43
        map_panel = RoundedRectangle(
            width=5.15,
            height=3.45,
            corner_radius=0.14,
            fill_color="#E0F2FE",
            fill_opacity=1.0,
            stroke_color=ACCENT_TEAL,
            stroke_width=2.5,
        ).move_to(LEFT * 3.05 + DOWN * 0.05)
        roads = road_grid_2d(width=4.7, height=3.05).scale(0.88).move_to(map_panel)
        car1 = vehicle_icon(color=ACCENT_TEAL, scale=0.42).move_to(map_panel.get_center() + LEFT * 1.35 + DOWN * 0.45)
        car2 = vehicle_icon(color=GREEN_FIX, scale=0.42).move_to(map_panel.get_center() + RIGHT * 1.0 + UP * 0.55)
        car2.rotate(PI)
        rsu1 = rsu_icon(color=ORANGE_INFRA).scale(0.75).move_to(map_panel.get_center() + LEFT * 1.6 + UP * 1.25)
        rsu2 = rsu_icon(color=ORANGE_INFRA).scale(0.75).move_to(map_panel.get_center() + RIGHT * 1.55 + DOWN * 1.25)
        agents = VGroup(car1, car2, rsu1, rsu2)

        # Initialize dynamic opacity attribute for all agents
        for agent in agents:
            agent.current_opacity = 1.0

        # Define vehicle wrap-around motion updaters
        def car1_updater(mob, dt):
            mob.shift(RIGHT * 0.35 * dt)
            rel_x = mob.get_center()[0] - map_panel.get_center()[0]
            half_w = 4.7 * 0.88 / 2
            margin = 0.35
            if rel_x > half_w + margin:
                mob.set_x(map_panel.get_center()[0] - half_w - margin)
                rel_x = -half_w - margin
            
            # Fade near boundaries
            dist_to_right = (half_w + margin) - rel_x
            dist_to_left = rel_x - (-half_w - margin)
            fade_factor = min(dist_to_right / 0.4, dist_to_left / 0.4)
            fade_factor = max(0.0, min(1.0, fade_factor))
            mob.current_opacity = fade_factor
            mob.set_opacity(fade_factor)

        def car2_updater(mob, dt):
            mob.shift(LEFT * 0.35 * dt)
            rel_x = mob.get_center()[0] - map_panel.get_center()[0]
            half_w = 4.7 * 0.88 / 2
            margin = 0.35
            if rel_x < -half_w - margin:
                mob.set_x(map_panel.get_center()[0] + half_w + margin)
                rel_x = half_w + margin
            
            # Fade near boundaries
            dist_to_right = (half_w + margin) - rel_x
            dist_to_left = rel_x - (-half_w - margin)
            fade_factor = min(dist_to_right / 0.4, dist_to_left / 0.4)
            fade_factor = max(0.0, min(1.0, fade_factor))
            mob.current_opacity = fade_factor
            mob.set_opacity(fade_factor)


        links = VGroup()
        flashes = []
        for a, b in [(car1, car2), (car1, rsu1), (car2, rsu2), (rsu1, rsu2)]:
            line, flash = v2x_link(a, b, color=CYAN_RADAR)
            def line_updater(mob, start_mob=a, end_mob=b):
                mob.set_points_by_ends(start_mob.get_center(), end_mob.get_center())
                op_s = getattr(start_mob, "current_opacity", 1.0)
                op_e = getattr(end_mob, "current_opacity", 1.0)
                mob.set_stroke(opacity=0.5 * op_s * op_e)
            line.add_updater(line_updater)
            links.add(line)
            flashes.append(flash)
        map_label = Text("all collaboration modes", font=FONT_PRIMARY, font_size=SIZE_LABEL, color=INK_DARK, weight=BOLD)
        map_label.next_to(map_panel, DOWN, buff=0.16)

        stats = [
            ("2", "vehicles", ACCENT_TEAL),
            ("2", "infra nodes", ORANGE_INFRA),
            ("40K", "LiDAR frames", GOLD_RICH),
            ("208K", "camera frames", GREEN_FIX),
            ("HD", "maps + trajectories", PURPLE_MODEL),
            ("V2V / V2I / I2I", "same sequence", ACCENT_TEAL),
        ]
        cards = VGroup(*(make_stat_card(v, label, color=c) for v, label, c in stats))
        cards.arrange_in_grid(3, 2, h_buff=0.9, v_buff=0.35)
        cards.move_to(RIGHT * 3.2 + DOWN * 0.05)

        foot = Text("Real-world, sequential, multi-agent data.", font=FONT_PRIMARY, font_size=SIZE_CAPS, color=INK_DARK, weight=BOLD)
        foot.to_edge(DOWN, buff=0.72)

        # Create continuous packets and waves
        packets = VGroup(
            make_continuous_packets(car1, car2, CYAN_RADAR, speed=0.7, stagger=0.0),
            make_continuous_packets(rsu1, car1, CYAN_RADAR, speed=0.7, stagger=0.25),
            make_continuous_packets(car2, rsu2, CYAN_RADAR, speed=0.7, stagger=0.5),
            make_continuous_packets(rsu1, rsu2, CYAN_RADAR, speed=0.7, stagger=0.75),
        )
        waves = VGroup(
            make_continuous_waves(car1, CYAN_RADAR, max_radius=0.5, speed=0.6),
            make_continuous_waves(car2, CYAN_RADAR, max_radius=0.5, speed=0.6),
            make_continuous_waves(rsu1, CYAN_RADAR, max_radius=0.5, speed=0.6),
            make_continuous_waves(rsu2, CYAN_RADAR, max_radius=0.5, speed=0.6),
        )

        self.play(FadeIn(map_panel), FadeIn(roads))
        self.play(LaggedStart(*(FadeIn(a) for a in agents), lag_ratio=0.1))
        
        # Draw links statically first
        self.play(ShowCreation(links))
        
        # Start continuous vehicle motion updaters after entry animations complete
        car1.add_updater(car1_updater)
        car2.add_updater(car2_updater)
        self.add(packets, waves)
        
        self.play(FadeIn(map_label), LaggedStart(*(FadeIn(card, shift=UP * 0.14) for card in cards), lag_ratio=0.1))
        self.play(FadeIn(foot))
        self.wait(19.0)
        
        # Remove updaters so FadeOut can fade them out cleanly
        for mob in [car1, car2, *links, *packets, *waves]:
            mob.clear_updaters()
            
        self._close()
