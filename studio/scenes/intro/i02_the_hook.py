"""I-02 - The Hook: occlusion, spherical radar waves, cooperation, quote."""
import random

from manimlib import *
from studio.components import (
    Studio3DScene,
    ACCENT_BLUE,
    BG_PAPER,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_DARK,
    RED_ERROR,
    PURPLE_MODEL,
    SIZE_LABEL,
    SIZE_TITLE,
    ambient_glow,
    pedestrian_icon,
    radar_shells_3d,
    spherical_coverage_3d,
    sort_spherical_waves_to_camera,
    vehicle_icon_3d,
    write_chiseled,
)

SCRIPT = """
Even the smartest single agent cannot see around corners.
So we taught them to cooperate.
Cooperation, it turns out, is a physics solution - not an algorithm one.
"""


def occluder_column(
    base_center: np.ndarray,
    *,
    radius: float = 0.56,
    height: float = 1.6,
    color: str = "#D1D5DB",
) -> Group:
    """Vertical 3D column obstacle that anchors the blind-zone wedge."""
    side = Cylinder(
        radius=radius,
        height=height,
        axis=OUT,
        resolution=(64, 10),
        color=color,
        opacity=1.0,
    )
    side.set_color(color)
    side.move_to(base_center + OUT * (height / 2))
    side.deactivate_depth_test()

    top = Circle(
        radius=radius,
        fill_color="#F8FAFC",
        fill_opacity=1.0,
        stroke_color="#9CA3AF",
        stroke_width=2.4,
    )
    top.move_to(base_center + OUT * (height + 0.01))
    ribs = VGroup()
    for angle in np.linspace(0, TAU, 8, endpoint=False):
        xy = radius * np.array([np.cos(angle), np.sin(angle), 0])
        rib = Line(
            base_center + xy + OUT * 0.03,
            base_center + xy + OUT * height,
            stroke_color="#94A3B8",
            stroke_width=1.1,
            stroke_opacity=0.55,
        )
        ribs.add(rib)
    rim = top.copy().set_fill(opacity=0).set_stroke("#64748B", 2.2, opacity=0.95)
    column = Group(side, ribs, top, rim)
    column.deactivate_depth_test()
    return column


class I02TheHook(Studio3DScene):
    PART_NUM = 0
    SCENE_TITLE = "The Hook"
    default_frame_orientation = (-25, 65)

    def pulse_waves(self, center, *, color, n_shells=5, max_radius=3.0, run_time=1.2):
        shells, anim = radar_shells_3d(
            np.array(center), color=color, n_shells=n_shells, max_radius=max_radius,
        )
        sort_spherical_waves_to_camera(shells, self.camera)
        self.play(anim, run_time=run_time)
        self.play(FadeOut(shells, run_time=0.35))
        return shells

    def construct(self):
        self.camera.background_color = BG_PAPER
        self.frame.reorient(-25, 65, 0)
        world = Group()

        def keep_foreground(*mobs: Mobject) -> None:
            for mob in mobs:
                mob.deactivate_depth_test()
            self.remove(*mobs)
            self.add(*mobs)

        grid = NumberPlane(
            x_range=(-7, 7),
            y_range=(-5, 5),
            background_line_style={
                "stroke_color": CYAN_RADAR,
                "stroke_width": 0.5,
                "stroke_opacity": 0.12,
            },
        )
        road_h = Rectangle(width=13.5, height=1.1, fill_color="#0F1A2E",
                           fill_opacity=1.0, stroke_width=0)
        road_v = Rectangle(width=1.1, height=9.0, fill_color="#0F1A2E",
                           fill_opacity=1.0, stroke_width=0)
        roads = VGroup(road_h, road_v)
        roads.shift(0.035 * IN)
        grid.shift(0.04 * IN)
        roads.apply_depth_test()
        grid.apply_depth_test()
        world.add(grid, roads)
        self.play(FadeIn(grid, run_time=0.8), FadeIn(roads, run_time=0.8))

        hero_car = vehicle_icon_3d(color=CYAN_RADAR, scale=0.9)
        hero_car.deactivate_depth_test()
        hero_car.move_to(np.array([-7, 0, 0.42]))
        trail = TracedPath(
            hero_car.get_center,
            stroke_color=CYAN_RADAR,
            stroke_width=2.5,
            stroke_opacity=[0, 0.85],
            time_traced=0.4,
        )
        self.add(trail, hero_car)
        self.play(
            hero_car.animate.move_to(np.array([-1.75, -0.45, 0.42])),
            run_time=0.5,
            rate_func=smooth,
        )
        world.add(hero_car)

        shells1 = self.pulse_waves(hero_car.get_center(), color=CYAN_RADAR,
                                   n_shells=6, max_radius=3.5, run_time=1.2)
        keep_foreground(hero_car)
        shells2 = self.pulse_waves(hero_car.get_center(), color=CYAN_RADAR,
                                   n_shells=6, max_radius=3.5, run_time=1.1)
        keep_foreground(hero_car)
        world.add(shells1, shells2)

        building_center = np.array([0.35, 0.65, 0.08])
        shadow = Ellipse(width=1.8, height=0.45, fill_color=BLACK,
                         fill_opacity=0.16, stroke_width=0)
        shadow.move_to(building_center + DOWN * 0.72)
        building = occluder_column(building_center, radius=0.58, height=1.65)
        building.move_to(building_center + UP * 8 + OUT * 0.82)
        dust = VGroup()
        for a in np.linspace(0, TAU, 16, endpoint=False):
            d = Dot(radius=0.035, color="#CBD5E1")
            d.move_to(building_center + 0.35 * np.array([np.cos(a), np.sin(a), 0]))
            dust.add(d)
        self.add(dust)
        self.play(FadeIn(shadow), building.animate.move_to(building_center + OUT * 0.82),
                  run_time=0.8, rate_func=rush_into)
        self.play(
            building.animate.stretch(1.12, 2).stretch(1 / 1.12, 2),
            LaggedStart(*(
                FadeOut(d, shift=0.55 * normalize(d.get_center() - building_center))
                for d in dust
            ), lag_ratio=0.02),
            run_time=0.28,
        )
        world.add(shadow, building)

        blind_zone = AnnularSector(
            inner_radius=0.25,
            outer_radius=3.1,
            start_angle=-0.48,
            angle=1.05,
            arc_center=building_center + RIGHT * 0.35 + OUT * 0.12,
            fill_color=RED_ERROR,
            fill_opacity=0.22,
            stroke_color=RED_ERROR,
            stroke_width=1.5,
            stroke_opacity=0.5,
        )
        distortion = VGroup()
        for r in [0.8, 1.15, 1.55, 1.95]:
            arc = Arc(
                start_angle=-0.75,
                angle=1.5,
                radius=r,
                stroke_color=CYAN_RADAR,
                stroke_width=2.0,
                stroke_opacity=0.4,
            )
            arc.stretch(0.55 + 0.08 * r, 1)
            arc.move_to(building_center + RIGHT * 0.8 + DOWN * 0.1 + OUT * 0.24)
            distortion.add(arc)
        self.play(FadeIn(blind_zone), ShowCreation(distortion), run_time=0.8)
        self.remove(building)
        self.add(building)
        keep_foreground(hero_car)
        world.add(blind_zone, distortion)

        overlay = Text(
            "Blind zone",
            font=FONT_PRIMARY,
            font_size=SIZE_LABEL,
            color=RED_ERROR,
            weight=BOLD,
        )
        overlay.fix_in_frame()
        overlay.to_corner(UR, buff=0.45)
        overlay_bg = SurroundingRectangle(
            overlay,
            buff=0.12,
            fill_color=BG_PAPER,
            fill_opacity=0.82,
            stroke_color=RED_ERROR,
            stroke_width=1.2,
        )
        overlay_bg.fix_in_frame()
        self.play(FadeIn(overlay_bg), FadeIn(overlay), run_time=0.45)

        car2 = vehicle_icon_3d(color=ACCENT_BLUE, scale=0.78)
        car2.deactivate_depth_test()
        car2.move_to(np.array([3.0, 1.75, 0.42]))
        car2.rotate(PI)
        car3 = vehicle_icon_3d(color=PURPLE_MODEL, scale=0.78)
        car3.deactivate_depth_test()
        car3.move_to(np.array([0.8, -2.75, 0.42]))
        car3.rotate(PI / 2)
        self.add(car2, car3)
        self.play(FadeIn(car2, shift=LEFT * 0.7), FadeIn(car3, shift=UP * 0.7),
                  run_time=0.9)
        world.add(car2, car3)

        # All 3 cars pulse simultaneously for cooperation moment
        shells_h, anim_h = radar_shells_3d(hero_car.get_center(), color=CYAN_RADAR,
                                           n_shells=5, max_radius=3.0)
        shells_a, anim_a = radar_shells_3d(car2.get_center(), color=ACCENT_BLUE,
                                           n_shells=5, max_radius=3.0)
        shells_b, anim_b = radar_shells_3d(car3.get_center(), color=PURPLE_MODEL,
                                           n_shells=5, max_radius=3.0)
        sort_spherical_waves_to_camera(shells_h, self.camera)
        sort_spherical_waves_to_camera(shells_a, self.camera)
        sort_spherical_waves_to_camera(shells_b, self.camera)
        self.add(shells_h, shells_a, shells_b)
        keep_foreground(hero_car, car2, car3)
        
        # Reduced opacity for subtler coverage spheres
        interference = Group(
            spherical_coverage_3d(hero_car.get_center(), color=CYAN_RADAR, radius=2.9, opacity=0.035),
            spherical_coverage_3d(car2.get_center(), color=ACCENT_BLUE, radius=2.5, opacity=0.028),
            spherical_coverage_3d(car3.get_center(), color=PURPLE_MODEL, radius=2.5, opacity=0.028),
        )
        sort_spherical_waves_to_camera(interference, self.camera)
        
        # Interference pattern bright nodes
        bright_nodes = VGroup()
        for _ in range(22):
            node = Dot(radius=random.uniform(0.025, 0.055), color=WHITE)
            node.set_opacity(0.18)
            node.move_to(np.array([random.uniform(-0.2, 1.5), random.uniform(-0.7, 0.9), 0]))
            bright_nodes.add(node)
        
        # All 3 pulses play simultaneously
        self.play(anim_h, anim_a, anim_b, FadeIn(interference), FadeIn(bright_nodes),
                  run_time=1.4)
        self.remove(building)
        self.add(building)
        keep_foreground(hero_car, car2, car3)
        world.add(shells_h, shells_a, shells_b, interference, bright_nodes)

        # Fade out shells BEFORE revealing pedestrian
        self.play(
            FadeOut(shells_h),
            FadeOut(shells_a),
            FadeOut(shells_b),
            FadeOut(interference),
            FadeOut(bright_nodes),
            run_time=0.5,
        )
        
        # Now reveal pedestrian with transformed blind zone
        ped = pedestrian_icon(color=GREEN_FIX)
        ped.scale(0.9)
        ped.move_to(building_center + RIGHT * 1.45 + UP * 0.28)
        glow = ambient_glow(ped, color=GREEN_FIX, radius=0.5)
        ped.set_opacity(0)
        glow.set_opacity(0)
        self.add(glow, ped)
        self.play(
            blind_zone.animate.set_fill(GREEN_FIX, opacity=0.13).set_stroke(GREEN_FIX, 1.8),
            overlay.animate.set_color(GREEN_FIX),
            overlay_bg.animate.set_stroke(GREEN_FIX),
            ped.animate.set_opacity(1),
            glow.animate.set_opacity(1),
            run_time=1.2,
        )
        self.play(Flash(ped, color=GREEN_FIX, line_length=0.25, num_lines=8), run_time=0.5)
        world.add(ped, glow)

        # Updated quote about single agent limitation
        quote = Text(
            "No single agent can see through walls.\nCooperation is a physics solution,\nnot an algorithm one.",
            font=FONT_PRIMARY,
            font_size=SIZE_TITLE - 4,
            color=GOLD_RICH,
            weight=BOLD,
        )
        quote.fix_in_frame()
        quote.move_to(DOWN * 2.35)
        quote.set_color(GOLD_RICH)
        quote.deactivate_depth_test()
        self.play(FadeOut(overlay), FadeOut(overlay_bg), run_time=0.35)
        keep_foreground(hero_car, car2, car3)
        self.add(quote)
        self.play(write_chiseled(quote, run_time=3.0))
        self.wait(2.5)

        curtain = Rectangle(width=20, height=12, fill_color=BG_PAPER,
                            fill_opacity=0, stroke_width=0)
        curtain.fix_in_frame()
        self.add(curtain)
        self.play(curtain.animate.set_fill(BG_PAPER, opacity=1.0), run_time=1.0)
        self.clear()
        self.wait(0.5)
