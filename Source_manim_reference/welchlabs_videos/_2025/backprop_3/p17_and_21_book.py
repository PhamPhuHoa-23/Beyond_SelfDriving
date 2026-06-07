from manimlib import *
import numpy as np
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#6e9671'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
graphics_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/ai_book/4_deep_learning/graphics/'
map_filename = 'baarle_hertog_maps-13.png'

class LinearPlane(Surface):

    def __init__(self, axes, m1=0.5, m2=0.3, b=1.0, vertical_viz_scale=0.5, **kwargs):
        self.axes = axes
        self.m1 = m1
        self.m2 = m2
        self.b = b
        self.vertical_viz_scale = vertical_viz_scale
        super().__init__(u_range=(-5, 5), v_range=(-5, 5), resolution=(64, 64), color='#00FFFF', **kwargs)

    def uv_func(self, u, v):
        x1 = u
        x2 = v
        z = self.vertical_viz_scale * (self.m1 * x1 + self.m2 * x2 + self.b)
        return self.axes.c2p(x1, x2, z)

def find_plane_intersection(plane1, plane2):
    a = plane1.m1 - plane2.m1
    b = plane1.m2 - plane2.m2
    c = plane2.b - plane1.b
    if abs(a) > abs(b):

        def get_point(t):
            x2 = t
            x1 = (c - b * x2) / a if abs(a) > 1e-10 else 0
            z = plane1.vertical_viz_scale * (plane1.m1 * x1 + plane1.m2 * x2 + plane1.b)
            return np.array([x1, x2, z])
    else:

        def get_point(t):
            x1 = t
            x2 = (c - a * x1) / b if abs(b) > 1e-10 else 0
            z = plane1.vertical_viz_scale * (plane1.m1 * x1 + plane1.m2 * x2 + plane1.b)
            return np.array([x1, x2, z])
    return get_point

class IntersectionLine(ParametricCurve):

    def __init__(self, axes, plane1, plane2, t_range=(-5, 5, 0.1), **kwargs):
        self.axes = axes
        self.plane1 = plane1
        self.plane2 = plane2
        self.intersection_func = find_plane_intersection(plane1, plane2)
        super().__init__(lambda t: self.axes.c2p(*self.intersection_func(t)), t_range=t_range, **kwargs)

class HalfPlane(Surface):

    def __init__(self, axes, base_plane, other_plane, above=True, **kwargs):
        self.axes = axes
        self.base_plane = base_plane
        self.other_plane = other_plane
        self.above = above
        super().__init__(u_range=(-5, 5), v_range=(-5, 5), resolution=(32, 32), **kwargs)

    def uv_func(self, u, v):
        x1, x2 = (u, v)
        z1 = self.base_plane.vertical_viz_scale * (self.base_plane.m1 * x1 + self.base_plane.m2 * x2 + self.base_plane.b)
        z2 = self.other_plane.vertical_viz_scale * (self.other_plane.m1 * x1 + self.other_plane.m2 * x2 + self.other_plane.b)
        if self.above and z1 <= z2:
            return self.axes.c2p(x1, x2, -10)
        elif not self.above and z1 >= z2:
            return self.axes.c2p(x1, x2, -10)
        else:
            return self.axes.c2p(x1, x2, z1)

class FlatHalfPlane(Surface):

    def __init__(self, axes, base_plane, other_plane, above=True, **kwargs):
        self.axes = axes
        self.base_plane = base_plane
        self.other_plane = other_plane
        self.above = above
        super().__init__(u_range=(-5, 5), v_range=(-5, 5), resolution=(32, 32), **kwargs)

    def uv_func(self, u, v):
        x1, x2 = (u, v)
        z1 = self.base_plane.vertical_viz_scale * (self.base_plane.m1 * x1 + self.base_plane.m2 * x2 + self.base_plane.b)
        z2 = self.other_plane.vertical_viz_scale * (self.other_plane.m1 * x1 + self.other_plane.m2 * x2 + self.other_plane.b)
        if self.above and z1 <= z2:
            return self.axes.c2p(x1, x2, -10)
        elif not self.above and z1 >= z2:
            return self.axes.c2p(x1, x2, -10)
        else:
            return self.axes.c2p(x1, x2, 0)

class p17(InteractiveScene):

    def construct(self):
        map_img = ImageMobject(graphics_dir + '/baarle_hertog_maps/' + map_filename)
        map_img.move_to(ORIGIN)
        map_img.scale(0.25)
        axes_1 = ThreeDAxes(x_range=[-5, 5, 1], y_range=[-5, 5, 1], z_range=[-3.5, 3.5, 1], width=1, height=1, depth=1, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.015, 'length': 0.015}})
        plane_1 = LinearPlane(axes_1, 0.5, 1.2, 4, vertical_viz_scale=0.2)
        plane_1.set_opacity(0.3)
        plane_1.set_color('#00FFFF')
        plane_2 = LinearPlane(axes_1, -1, 0.2, 4, vertical_viz_scale=0.2)
        plane_2.set_opacity(0.3)
        plane_2.set_color(YELLOW)
        intersection_line = IntersectionLine(axes_1, plane_1, plane_2, t_range=(-5, 5, 0.1), color='#FF00FF', stroke_width=4)
        self.frame.reorient(0, 0, 0, (0.01, -0.01, 0.0), 1.29)
        self.add(map_img)
        self.wait()
        self.play(ShowCreation(plane_1), ShowCreation(plane_2), self.frame.animate.reorient(0, 46, 0, (-0.03, 0.02, 0.01), 1.62), run_time=5)
        self.wait()
        self.play(self.frame.animate.reorient(-16, 47, 0, (-0.04, 0.02, 0.0), 1.62))
        self.play(ShowCreation(intersection_line))
        self.wait()

        class FlatIntersectionLine(ParametricCurve):

            def __init__(self, axes, plane1, plane2, t_range=(-5, 5, 0.1), **kwargs):
                self.axes = axes
                self.plane1 = plane1
                self.plane2 = plane2
                self.intersection_func = find_plane_intersection(plane1, plane2)
                super().__init__(lambda t: self.axes.c2p(*self.intersection_func(t)[:2], 0), t_range=t_range, **kwargs)
        flat_intersection_line = FlatIntersectionLine(axes_1, plane_1, plane_2, t_range=(-5, 5, 0.1), color='#FF00FF', stroke_width=4)
        self.wait()
        self.frame.reorient(0, 45, 0, (-0.04, 0.01, -0.01), 1.62)
        plane_1.set_opacity(0.3)
        plane_2.set_opacity(0.45)
        self.wait()
        self.play(ReplacementTransform(intersection_line, flat_intersection_line), plane_1.animate.set_opacity(0.0), plane_2.animate.set_opacity(0.0), self.frame.animate.reorient(0, 2, 0, (-0.04, 0.02, 0.0), 1.62), run_time=4)
        self.wait()
        self.wait(20)
        self.embed()

class p21_final_planes(InteractiveScene):

    def construct(self):
        map_img = ImageMobject('/Users/stephen/Stephencwelch\\ Dropbox/welch_labs/ai_book/3_backprop_2/graphics/barrle_hertog_map_32.png')
        map_img.move_to(ORIGIN)
        map_img.scale(0.25)
        axes_1 = ThreeDAxes(x_range=[-5, 5, 1], y_range=[-5, 5, 1], z_range=[-3.5, 3.5, 1], width=1, height=1, depth=1, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.015, 'length': 0.015}})
        plane_1 = LinearPlane(axes_1, 0.5, 1.2, 4, vertical_viz_scale=0.2)
        plane_1.set_opacity(0.2)
        plane_1.set_color('#FF00FF')
        plane_2 = LinearPlane(axes_1, -1, 0.2, 4, vertical_viz_scale=0.2)
        plane_2.set_opacity(0.5)
        plane_2.set_color(CHILL_GREEN)
        intersection_line = IntersectionLine(axes_1, plane_1, plane_2, t_range=(-5, 5, 0.1), color=WHITE, stroke_width=4)
        self.frame.reorient(0, 0, 0, (0.01, -0.01, 0.0), 1.29)
        self.add(map_img)
        self.wait()
        self.play(ShowCreation(plane_1), ShowCreation(plane_2), self.frame.animate.reorient(0, 46, 0, (-0.03, 0.02, 0.01), 1.62), run_time=5)
        self.wait()
        self.play(self.frame.animate.reorient(-16, 47, 0, (-0.04, 0.02, 0.0), 1.62))
        self.play(ShowCreation(intersection_line))
        self.wait()

        class FlatIntersectionLine(ParametricCurve):

            def __init__(self, axes, plane1, plane2, t_range=(-5, 5, 0.1), **kwargs):
                self.axes = axes
                self.plane1 = plane1
                self.plane2 = plane2
                self.intersection_func = find_plane_intersection(plane1, plane2)
                super().__init__(lambda t: self.axes.c2p(*self.intersection_func(t)[:2], 0), t_range=t_range, **kwargs)
        flat_intersection_line = FlatIntersectionLine(axes_1, plane_1, plane_2, t_range=(-5, 5, 0.1), color=WHITE, stroke_width=4)
        self.wait()
        self.wait()
        self.wait(20)
        self.embed()