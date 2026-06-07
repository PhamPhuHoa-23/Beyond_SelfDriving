"""P02-S05 - Radar gravitational waves hero."""
import random

from manimlib import *

from studio.components import (
    ACCENT_BLUE,
    BG_PAPER,
    CYAN_RADAR,
    FONT_PRIMARY,
    GOLD_RICH,
    GREEN_FIX,
    INK_LIGHT,
    PURPLE_MODEL,
    RED_ERROR,
    SIZE_TITLE,
    Studio3DScene,
    ambient_glow,
    pedestrian_icon,
    radar_shells_3d,
    spherical_coverage_3d,
    sort_spherical_waves_to_camera,
    vehicle_icon_3d,
    write_chiseled,
)


SCRIPT = "Three cars. Three radar systems. Cooperation is a physics solution."


def dark_road_grid(width: float = 10.5, height: float = 6.8) -> VGroup:
    grid = NumberPlane(
        x_range=(-6, 6),
        y_range=(-4, 4),
        background_line_style={
            "stroke_color": CYAN_RADAR,
            "stroke_width": 0.5,
            "stroke_opacity": 0.15,
        },
    )
    roads = VGroup(
        Rectangle(width=width, height=1.25, fill_color="#0D1B2A",
                  fill_opacity=1.0, stroke_width=0),
        Rectangle(width=1.25, height=height, fill_color="#0D1B2A",
                  fill_opacity=1.0, stroke_width=0),
    )
    lanes = VGroup(
        DashedLine(LEFT * width / 2, RIGHT * width / 2,
                   stroke_color=WHITE, stroke_width=1.0, stroke_opacity=0.22),
        DashedLine(DOWN * height / 2, UP * height / 2,
                   stroke_color=WHITE, stroke_width=1.0, stroke_opacity=0.22),
    )
    road = VGroup(grid, roads, lanes)
    road.shift(0.035 * IN)
    road.apply_depth_test()
    return road


def occluder_column(
    base_center: np.ndarray,
    *,
    radius: float = 0.55,
    height: float = 1.55,
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


class P02S05RadarWaves(Studio3DScene):
    PART_NUM = 2
    SCENE_TITLE = "Radar Gravitational Waves"

    def pulse_waves(
        self,
        center: np.ndarray,
        *,
        color: str,
        n_cycles: int = 2,
        n_shells: int = 5,
        max_radius: float = 3.4,
    ) -> VGroup:
        all_shells = VGroup()
        for _ in range(n_cycles):
            shells, anim = radar_shells_3d(
                center, color=color, n_shells=n_shells, max_radius=max_radius,
            )
            sort_spherical_waves_to_camera(shells, self.camera)
            self.play(anim, run_time=1.15)
            self.play(FadeOut(shells, run_time=0.55))
            all_shells.add(shells)
        return all_shells

    def construct(self):
        self.camera.background_color = BG_PAPER
        self.frame.reorient(-30, 70, 0)
        world = Group()

        def keep_foreground(*mobs: Mobject) -> None:
            for mob in mobs:
                mob.deactivate_depth_test()
            self.remove(*mobs)
            self.add(*mobs)

        road = dark_road_grid()
        world.add(road)
        self.play(FadeIn(road, run_time=0.8))

        car1 = vehicle_icon_3d(color=CYAN_RADAR, scale=0.78)
        car1.deactivate_depth_test()
        car1.move_to([-4.2, -0.45, 0.42])
        trail = TracedPath(
            car1.get_center,
            stroke_color=CYAN_RADAR,
            stroke_width=2.5,
            stroke_opacity=[0, 0.8],
            time_traced=0.45,
        )
        self.add(trail, car1)
        self.play(car1.animate.move_to([-1.75, -0.45, 0.42]), run_time=0.5)
        world.add(car1)

        for cycle in range(2):
            shells1, anim1 = radar_shells_3d(
                car1.get_center(), color=CYAN_RADAR, n_shells=7, max_radius=3.5,
            )
            sort_spherical_waves_to_camera(shells1, self.camera)
            self.add(shells1)
            keep_foreground(car1)
            self.play(anim1, run_time=1.15)
            keep_foreground(car1)
            self.play(FadeOut(shells1, run_time=0.25 if cycle == 0 else 0.45))

        building_center = np.array([0.25, 0.1, 0.08])
        shadow = Ellipse(width=1.8, height=0.45, fill_color=BLACK,
                         fill_opacity=0.1, stroke_width=0)
        shadow.move_to(building_center + DOWN * 0.75)
        building = occluder_column(building_center, radius=0.56, height=1.6)
        building.move_to(building_center + UP * 5.5 + OUT * 0.8)
        dust = VGroup()
        for a in np.linspace(0, TAU, 12, endpoint=False):
            d = Dot(radius=0.035, color=INK_LIGHT)
            d.move_to(building_center + 0.35 * np.array([np.cos(a), np.sin(a), 0]))
            dust.add(d)
        self.add(dust)
        self.play(
            FadeIn(shadow),
            building.animate.move_to(building_center + OUT * 0.8),
                  run_time=0.65, rate_func=rush_into)
        self.play(
            building.animate.stretch(1.08, 2).stretch(1 / 1.08, 2),
            LaggedStart(*(
                FadeOut(d, shift=0.5 * normalize(d.get_center() - building_center))
                for d in dust
            ), lag_ratio=0.02),
            run_time=0.22,
        )
        world.add(shadow, building)

        blind = Polygon(
            building_center + RIGHT * 0.45 + DOWN * 0.45 + OUT * 0.12,
            building_center + RIGHT * 3.0 + DOWN * 1.35 + OUT * 0.12,
            building_center + RIGHT * 3.35 + DOWN * 0.1 + OUT * 0.12,
            building_center + RIGHT * 2.9 + UP * 1.1 + OUT * 0.12,
            building_center + RIGHT * 0.45 + UP * 0.45 + OUT * 0.12,
            fill_color=RED_ERROR,
            fill_opacity=0.18,
            stroke_color=RED_ERROR,
            stroke_width=1.8,
            stroke_opacity=0.0,
        )
        border = blind.copy().set_fill(opacity=0).set_stroke(RED_ERROR, 2.5, opacity=0.65)
        distortion = VGroup()
        for r in [0.8, 1.2, 1.6, 2.05]:
            arc = Arc(start_angle=-0.75, angle=1.45, radius=r,
                      stroke_color=CYAN_RADAR, stroke_width=2,
                      stroke_opacity=0.38)
            arc.stretch(0.55, 1)
            arc.move_to(building_center + RIGHT * 0.75 + DOWN * 0.1 + OUT * 0.22)
            distortion.add(arc)
        self.play(
            FadeIn(blind),
            ShowPassingFlash(border, time_width=0.5, run_time=1.1),
            ShowCreation(distortion),
            self.frame.animate.reorient(-15, 65, 0),
            run_time=1.1,
        )
        self.remove(building)
        self.add(building)
        keep_foreground(car1)
        world.add(blind, distortion)

        label = Text("Single agent: blind to occlusions.",
                     font=FONT_PRIMARY, font_size=24,
                     color=RED_ERROR, weight=BOLD)
        label.fix_in_frame()
        label.to_corner(UR, buff=0.45)
        label_bg = SurroundingRectangle(label, buff=0.12, fill_color=BG_PAPER,
                                        fill_opacity=0.82, stroke_color=RED_ERROR,
                                        stroke_width=1.2)
        label_bg.fix_in_frame()
        self.play(FadeIn(label_bg), FadeIn(label), run_time=0.35)

        car2 = vehicle_icon_3d(color=ACCENT_BLUE, scale=0.7)
        car2.deactivate_depth_test()
        car2.move_to([4.2, 1.9, 0.42])
        car2.rotate(PI)
        car3 = vehicle_icon_3d(color=PURPLE_MODEL, scale=0.7)
        car3.deactivate_depth_test()
        car3.move_to([0.9, -3.5, 0.42])
        car3.rotate(PI / 2)
        self.add(car2, car3)
        self.play(
            car2.animate.move_to([2.8, 1.9, 0.42]),
            car3.animate.move_to([0.9, -2.55, 0.42]),
            run_time=0.8,
        )
        world.add(car2, car3)

        interference = Group(
            spherical_coverage_3d(car1.get_center(), color=CYAN_RADAR, radius=2.9, opacity=0.11),
            spherical_coverage_3d(car2.get_center(), color=ACCENT_BLUE, radius=2.55, opacity=0.09),
            spherical_coverage_3d(car3.get_center(), color=PURPLE_MODEL, radius=2.55, opacity=0.09),
        )
        sort_spherical_waves_to_camera(interference, self.camera)
        overlap_sparks = VGroup()
        for _ in range(38):
            spark = Dot(radius=random.uniform(0.018, 0.05), color=WHITE)
            spark.set_opacity(0.15)
            spark.move_to([random.uniform(-0.25, 1.65),
                           random.uniform(-0.85, 0.95), 0.12])
            overlap_sparks.add(spark)
        for cycle in range(2):
            shells2, anim2 = radar_shells_3d(
                car2.get_center(), color=ACCENT_BLUE, n_shells=5, max_radius=3.0,
            )
            shells3, anim3 = radar_shells_3d(
                car3.get_center(), color=PURPLE_MODEL, n_shells=5, max_radius=3.1,
            )
            sort_spherical_waves_to_camera(shells2, self.camera)
            sort_spherical_waves_to_camera(shells3, self.camera)
            self.add(shells2, shells3)
            keep_foreground(car1, car2, car3)
            plays = [anim2, anim3]
            if cycle == 0:
                plays.extend([
                    FadeIn(interference),
                    LaggedStart(*(FadeIn(s) for s in overlap_sparks), lag_ratio=0.015),
                ])
            self.play(*plays, run_time=1.25)
            keep_foreground(car1, car2, car3)
            self.play(FadeOut(shells2), FadeOut(shells3), run_time=0.25)
        self.remove(building)
        self.add(building)
        keep_foreground(car1, car2, car3)
        self.play(
            AnimationGroup(*(
                Flash(s, color=WHITE, line_length=0.08, num_lines=4)
                for s in overlap_sparks[::5]
            )),
            run_time=0.6,
        )
        world.add(shells2, shells3, interference, overlap_sparks)

        self.play(self.frame.animate.reorient(0, 65, 0), run_time=0.65)
        self.play(
            blind.animate.set_fill(GREEN_FIX, opacity=0.24).set_stroke(GREEN_FIX, 2),
            label.animate.set_color(GREEN_FIX),
            label_bg.animate.set_stroke(GREEN_FIX),
            run_time=0.6,
        )
        keep_foreground(car1, car2, car3)

        ped = pedestrian_icon(color=GREEN_FIX)
        ped.scale(0.82)
        ped.move_to([1.55, 0.75, 0.18])
        glow = ambient_glow(ped, color=GREEN_FIX, radius=0.6)
        ped.set_opacity(0)
        glow.set_opacity(0)
        self.add(glow, ped)
        self.play(glow.animate.set_opacity(1), ped.animate.set_opacity(1), run_time=2.0)
        self.play(Flash(ped, color=GREEN_FIX, num_lines=8, line_length=0.2),
                  run_time=0.5)
        world.add(ped, glow)

        quote = Text(
            "\"Cooperation is a physics solution,\nnot an algorithm one.\"",
            font=FONT_PRIMARY,
            font_size=SIZE_TITLE,
            color=GOLD_RICH,
            weight=BOLD,
        )
        quote.fix_in_frame()
        quote.move_to(DOWN * 2.15)
        quote.set_color(GOLD_RICH)
        quote.deactivate_depth_test()

        self.play(
            FadeOut(interference),
            FadeOut(overlap_sparks),
            run_time=0.45,
        )
        keep_foreground(car1, car2, car3)
        self.add(quote)

        ping1, ping_anim1 = radar_shells_3d(car1.get_center(), color=CYAN_RADAR,
                                            n_shells=3, max_radius=1.8)
        ping2, ping_anim2 = radar_shells_3d(car2.get_center(), color=ACCENT_BLUE,
                                            n_shells=3, max_radius=1.7)
        ping3, ping_anim3 = radar_shells_3d(car3.get_center(), color=PURPLE_MODEL,
                                            n_shells=3, max_radius=1.7)
        sort_spherical_waves_to_camera(ping1, self.camera)
        sort_spherical_waves_to_camera(ping2, self.camera)
        sort_spherical_waves_to_camera(ping3, self.camera)
        self.add(ping1, ping2, ping3)
        keep_foreground(car1, car2, car3)
        self.play(
            ping_anim1,
            ping_anim2,
            ping_anim3,
            write_chiseled(quote, run_time=3.5),
            run_time=3.5,
        )
        keep_foreground(car1, car2, car3)
        world.add(ping1, ping2, ping3)
        self.play(FadeOut(ping1), FadeOut(ping2), FadeOut(ping3), run_time=0.45)
        keep_foreground(car1, car2, car3)
        self.wait(2.5)

        curtain = Rectangle(width=20, height=12, fill_color=BG_PAPER,
                            fill_opacity=0, stroke_width=0)
        curtain.fix_in_frame()
        self.add(curtain)
        self.play(curtain.animate.set_fill(BG_PAPER, opacity=1.0), run_time=1.0)
        self.clear()
        self.wait(0.5)
