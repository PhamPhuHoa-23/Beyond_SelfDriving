from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
surf = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/animation/p_24_28_losses_4.npy')
xy = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/animation/p_24_28_losses_4xy.npy')
grads_1 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/animation/p_33_35_grads_1_2.npy')
grads_2 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/animation/p_33_35_grads_2_2.npy')
xy_grads = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/animation/p_33_35_xy_2.npy')

def param_surface(u, v):
    u_idx = np.abs(xy[0] - u).argmin()
    v_idx = np.abs(xy[1] - v).argmin()
    try:
        z = surf[u_idx, v_idx]
    except IndexError:
        z = 0
    return np.array([u, v, z])

def param_surface_scaled(u, v):
    u_idx = np.abs(xy[0] - u).argmin()
    v_idx = np.abs(xy[1] - v).argmin()
    try:
        z = 1.5 * surf[u_idx, v_idx]
    except IndexError:
        z = 0
    return np.array([u, v, z])

def get_grads(u, v):
    u_idx = np.abs(xy_grads[0] - u).argmin()
    v_idx = np.abs(xy_grads[1] - v).argmin()
    try:
        z1 = grads_1[u_idx, v_idx]
    except IndexError:
        z1 = 0
    try:
        z2 = grads_2[u_idx, v_idx]
    except IndexError:
        z2 = 0
    return np.array([u, v, z1, z2])

def map_to_canvas(value, axis_min, axis_max, axis_end, axis_start=0):
    value_scaled = (value - axis_min) / (axis_max - axis_min)
    return (value_scaled + axis_start) * axis_end

def get_pivot_and_scale(axis_min, axis_max, axis_end):
    scale = axis_end / (axis_max - axis_min)
    return (axis_min, scale)

class Dot3D(Sphere):

    def __init__(self, center=ORIGIN, radius=0.05, **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.move_to(center)

class P33v1(InteractiveScene):

    def construct(self):
        x_axis_1 = WelchXAxis(x_min=-1.2, x_max=4.5, x_ticks=[-1, 0, 1, 2, 3, 4], x_tick_height=0.15, x_label_font_size=24, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_1 = WelchYAxis(y_min=0.3, y_max=2.2, y_ticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0], y_tick_width=0.15, y_label_font_size=20, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=3)
        axes_1 = VGroup(x_axis_1, y_axis_1)
        points_1 = [param_surface(u, 0) for u in np.linspace(-1, 4, 128)]
        points_mapped = np.array(points_1)[:, (0, 2, 1)]
        points_mapped[:, 0] = map_to_canvas(points_mapped[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        points_mapped[:, 1] = map_to_canvas(points_mapped[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        curve_1 = VMobject()
        curve_1.set_points_smoothly(points_mapped)
        curve_1.set_stroke(width=4, color=YELLOW, opacity=0.8)
        x_label_1 = Tex('\\theta_{1}', font_size=30).set_color(CHILL_BROWN)
        y_label_1 = Tex('Loss', font_size=25).set_color(CHILL_BROWN)
        x_label_1.next_to(x_axis_1, RIGHT, buff=0.05)
        y_label_1.next_to(y_axis_1, UP, buff=0.05)
        p1_values = param_surface(0, 0)
        p1_values[0] = map_to_canvas(p1_values[0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        p1_values[1] = map_to_canvas(p1_values[2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        p1_values[2] = 0
        p1 = Dot(p1_values, radius=0.06, fill_color=YELLOW)
        g = get_grads(0, 0)
        grad_viz_scale = 1.25 * abs(g[2])
        p1_values_2 = param_surface(0, 0)
        g_values = np.array([[p1_values_2[0], p1_values_2[2], 0], [p1_values_2[0] + grad_viz_scale, p1_values_2[2] + grad_viz_scale * g[2] * 0.6, 0]])
        g_values[:, 0] = map_to_canvas(g_values[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        g_values[:, 1] = map_to_canvas(g_values[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        a1 = Arrow(start=g_values[0], end=g_values[1], fill_color=YELLOW, thickness=3.0, tip_width_ratio=5, buff=0)
        panel_1 = VGroup(axes_1, curve_1, x_label_1, y_label_1, p1, a1)
        x_axis_2 = WelchXAxis(x_min=-1.2, x_max=4.5, x_ticks=[-1, 0, 1, 2, 3, 4], x_tick_height=0.15, x_label_font_size=24, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_2 = WelchYAxis(y_min=0.3, y_max=2.2, y_ticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0], y_tick_width=0.15, y_label_font_size=20, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=3)
        axes_2 = VGroup(x_axis_2, y_axis_2)
        points_2 = [param_surface(0, v) for v in np.linspace(-1, 4, 128)]
        points_mapped_2 = np.array(points_2)[:, (1, 2, 0)]
        points_mapped_2[:, 0] = map_to_canvas(points_mapped_2[:, 0], axis_min=x_axis_2.x_min, axis_max=x_axis_2.x_max, axis_end=x_axis_2.axis_length_on_canvas)
        points_mapped_2[:, 1] = map_to_canvas(points_mapped_2[:, 1], axis_min=y_axis_2.y_min, axis_max=y_axis_2.y_max, axis_end=y_axis_2.axis_length_on_canvas)
        curve_2 = VMobject()
        curve_2.set_points_smoothly(points_mapped_2)
        curve_2.set_stroke(width=4, color=BLUE, opacity=0.8)
        x_label_2 = Tex('\\theta_{2}', font_size=30).set_color(CHILL_BROWN)
        y_label_2 = Tex('Loss', font_size=25).set_color(CHILL_BROWN)
        x_label_2.next_to(x_axis_2, RIGHT, buff=0.05)
        y_label_2.next_to(y_axis_2, UP, buff=0.05)
        p2_values = param_surface(0, 0)
        p2_values[0] = map_to_canvas(p2_values[0], axis_min=x_axis_2.x_min, axis_max=x_axis_2.x_max, axis_end=x_axis_2.axis_length_on_canvas)
        p2_values[1] = map_to_canvas(p2_values[2], axis_min=y_axis_2.y_min, axis_max=y_axis_2.y_max, axis_end=y_axis_2.axis_length_on_canvas)
        p2_values[2] = 0
        p2 = Dot(p2_values, radius=0.06, fill_color=BLUE)
        g = get_grads(0, 0)
        grad_viz_scale = 1.25 * abs(g[3])
        p2_values_2 = param_surface(0, 0)
        g_values_2 = np.array([[p2_values_2[0], p2_values_2[2], 0], [p2_values_2[0] + grad_viz_scale, p2_values_2[2] + grad_viz_scale * g[3] * 1.0, 0]])
        g_values_2[:, 0] = map_to_canvas(g_values_2[:, 0], axis_min=x_axis_2.x_min, axis_max=x_axis_2.x_max, axis_end=x_axis_2.axis_length_on_canvas)
        g_values_2[:, 1] = map_to_canvas(g_values_2[:, 1], axis_min=y_axis_2.y_min, axis_max=y_axis_2.y_max, axis_end=y_axis_2.axis_length_on_canvas)
        a2 = Arrow(start=g_values_2[0], end=g_values_2[1], fill_color=BLUE, thickness=3.0, tip_width_ratio=5, buff=0)
        panel_2 = VGroup(axes_2, curve_2, x_label_2, p2, a2)
        curve_1.set_stroke(opacity=0.5)
        curve_2.set_stroke(opacity=0.5)
        panel_2.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        panel_1.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        self.add(panel_1, panel_2)
        self.frame.reorient(0, 89, 0, (-0.46, 0.0, 1.36), 8.97)
        panel_1_shift = [-5, 0, 2.0]
        panel_2_shift = [-5, 0, -2.0]
        panel_1.shift(panel_1_shift)
        panel_2.shift(panel_2_shift)
        self.wait()
        r = panel_2.get_corner(LEFT + BOTTOM)
        r[0] = -4.15
        self.wait()
        self.play(y_axis_2.animate.set_opacity(0.0), x_axis_1[-1].animate.set_opacity(0.0), x_axis_2[-1].animate.set_opacity(0.0), y_axis_1[-1].animate.set_opacity(0.0), x_axis_1[-2].animate.set_opacity(0.0), x_axis_2[-2].animate.set_opacity(0.0), y_axis_1[-2].animate.set_opacity(0.0), run_time=1.0)
        self.play(panel_1.animate.shift([0, 0, -2.0]), panel_2.animate.rotate(90 * DEGREES, [0, 0, 1], about_point=r).shift([0, 0, 2.0]), self.frame.animate.reorient(13, 85, 0, (-1.88, -0.77, 1.56), 5.01), run_time=4)
        self.wait()
        surface = ParametricSurface(param_surface, u_range=[-1, 4], v_range=[-1, 4], resolution=(256, 256))
        ts = TexturedSurface(surface, '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/animation/p_24_28_losses_4.png')
        ts.set_shading(0.0, 0.1, 0)
        pivot_x, scale_x = get_pivot_and_scale(axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        pivot_y, scale_y = get_pivot_and_scale(axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        ts.scale([scale_x, scale_x, scale_y], about_point=[pivot_x, pivot_x, pivot_y])
        surf_shift = [-3.8, 0.34, -0.3]
        ts.shift(surf_shift)
        num_lines = 21
        num_points = 256
        u_gridlines = VGroup()
        v_gridlines = VGroup()
        u_values = np.linspace(-1, 4, num_lines)
        v_points = np.linspace(-1, 4, num_points)
        for u in u_values:
            points = [param_surface(u, v) for v in v_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.0)
            u_gridlines.add(line)
        u_points = np.linspace(-1, 4, num_points)
        for v in u_values:
            points = [param_surface(u, v) for u in u_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.0)
            v_gridlines.add(line)
        u_gridlines.scale([scale_x, scale_x, scale_y], about_point=[pivot_x, pivot_x, pivot_y])
        u_gridlines.shift(surf_shift)
        v_gridlines.scale([scale_x, scale_x, scale_y], about_point=[pivot_x, pivot_x, pivot_y])
        v_gridlines.shift(surf_shift)
        ts.set_opacity(0.0)
        self.add(ts, u_gridlines, v_gridlines)
        self.remove(a1)
        self.add(a1)
        self.remove(a2)
        self.add(a2)
        self.remove(p1)
        self.add(p1)
        self.remove(p2)
        self.add(p2)
        self.play(ts.animate.set_opacity(0.5), p1.animate.set_opacity(0.0), p2.animate.set_opacity(0.0), a1.animate.rotate(-DEGREES * 135, axis=a1.get_end() - a1.get_start()), a2.animate.rotate(-DEGREES * 80, axis=a2.get_end() - a2.get_start()), u_gridlines.animate.set_stroke(opacity=0.14), v_gridlines.animate.set_stroke(opacity=0.14), self.frame.animate.reorient(124, 40, 0, (-2.57, 0.86, 2.7), 1.81), run_time=4.0)
        self.wait()
        a3 = Arrow(start=[a1.get_corner(LEFT)[0] + 0.03, a1.get_corner(LEFT)[1] + 0.01, a1.get_corner(OUT)[2]], end=[a1.get_corner(RIGHT)[0], a2.get_corner(UP)[1], a2.get_corner(IN)[2]], fill_color='#FF00FF', thickness=3.0, tip_width_ratio=5, buff=0)
        self.wait()
        self.play(TransformFromCopy(a1, a3), TransformFromCopy(a2, a3), run_time=3.0)
        self.wait()
        s1 = Dot3D(center=a3.get_start(), radius=0.06, color='$FF00FF')
        s2 = Dot3D(center=a3.get_end(), radius=0.06, color='$FF00FF')
        self.wait()
        self.play(a1.animate.set_opacity(0.0), a2.animate.set_opacity(0.0), curve_1.animate.set_opacity(0.0), curve_2.animate.set_opacity(0.0), FadeIn(s1), FadeIn(s2), self.frame.animate.reorient(175, 47, 0, (-3.89, 1.49, 1.6), 3.75), run_time=2.0)
        self.wait()
        self.embed()
        self.wait(20)

class P34_2d_deprecated(InteractiveScene):

    def construct(self):
        x_axis_1 = WelchXAxis(x_min=-1.2, x_max=4.5, x_ticks=[-1, 0, 1, 2, 3, 4], x_tick_height=0.15, x_label_font_size=24, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_1 = WelchYAxis(y_min=0.3, y_max=2.2, y_ticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0], y_tick_width=0.15, y_label_font_size=20, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=3)
        axes_1 = VGroup(x_axis_1, y_axis_1)
        points_1 = [param_surface(u, 0) for u in np.linspace(-1, 4, 128)]
        points_mapped = np.array(points_1)[:, (0, 2, 1)]
        points_mapped[:, 0] = map_to_canvas(points_mapped[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        points_mapped[:, 1] = map_to_canvas(points_mapped[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        curve_1 = VMobject()
        curve_1.set_points_smoothly(points_mapped)
        curve_1.set_stroke(width=4, color=YELLOW, opacity=0.8)
        x_label_1 = Tex('\\theta_{1}', font_size=30).set_color(CHILL_BROWN)
        y_label_1 = Tex('Loss', font_size=25).set_color(CHILL_BROWN)
        x_label_1.next_to(x_axis_1, RIGHT, buff=0.05)
        y_label_1.next_to(y_axis_1, UP, buff=0.05)
        p1_values = param_surface(0, 0)
        p1_values[0] = map_to_canvas(p1_values[0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        p1_values[1] = map_to_canvas(p1_values[2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        p1_values[2] = 0
        p1 = Dot(p1_values, radius=0.06, fill_color=YELLOW)
        g = get_grads(0, 0)
        grad_viz_scale = 1.25 * abs(g[2])
        p1_values_2 = param_surface(0, 0)
        g_values = np.array([[p1_values_2[0], p1_values_2[2], 0], [p1_values_2[0] + grad_viz_scale, p1_values_2[2] + grad_viz_scale * g[2] * 0.6, 0]])
        g_values[:, 0] = map_to_canvas(g_values[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        g_values[:, 1] = map_to_canvas(g_values[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        a1 = Arrow(start=g_values[0], end=g_values[1], fill_color=YELLOW, thickness=3.0, tip_width_ratio=5, buff=0)
        panel_1 = VGroup(axes_1, curve_1, x_label_1, y_label_1, p1, a1)
        x_axis_2 = WelchXAxis(x_min=-1.2, x_max=4.5, x_ticks=[-1, 0, 1, 2, 3, 4], x_tick_height=0.15, x_label_font_size=24, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_2 = WelchYAxis(y_min=0.3, y_max=2.2, y_ticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0], y_tick_width=0.15, y_label_font_size=20, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=3)
        axes_2 = VGroup(x_axis_2, y_axis_2)
        points_2 = [param_surface(0, v) for v in np.linspace(-1, 4, 128)]
        points_mapped_2 = np.array(points_2)[:, (1, 2, 0)]
        points_mapped_2[:, 0] = map_to_canvas(points_mapped_2[:, 0], axis_min=x_axis_2.x_min, axis_max=x_axis_2.x_max, axis_end=x_axis_2.axis_length_on_canvas)
        points_mapped_2[:, 1] = map_to_canvas(points_mapped_2[:, 1], axis_min=y_axis_2.y_min, axis_max=y_axis_2.y_max, axis_end=y_axis_2.axis_length_on_canvas)
        curve_2 = VMobject()
        curve_2.set_points_smoothly(points_mapped_2)
        curve_2.set_stroke(width=4, color=BLUE, opacity=0.8)
        x_label_2 = Tex('\\theta_{2}', font_size=30).set_color(CHILL_BROWN)
        y_label_2 = Tex('Loss', font_size=25).set_color(CHILL_BROWN)
        x_label_2.next_to(x_axis_2, RIGHT, buff=0.05)
        y_label_2.next_to(y_axis_2, UP, buff=0.05)
        p2_values = param_surface(0, 0)
        p2_values[0] = map_to_canvas(p2_values[0], axis_min=x_axis_2.x_min, axis_max=x_axis_2.x_max, axis_end=x_axis_2.axis_length_on_canvas)
        p2_values[1] = map_to_canvas(p2_values[2], axis_min=y_axis_2.y_min, axis_max=y_axis_2.y_max, axis_end=y_axis_2.axis_length_on_canvas)
        p2_values[2] = 0
        p2 = Dot(p2_values, radius=0.06, fill_color=BLUE)
        g = get_grads(0, 0)
        grad_viz_scale = 1.25 * abs(g[3])
        p2_values_2 = param_surface(0, 0)
        g_values_2 = np.array([[p2_values_2[0], p2_values_2[2], 0], [p2_values_2[0] + grad_viz_scale, p2_values_2[2] + grad_viz_scale * g[3] * 1.0, 0]])
        g_values_2[:, 0] = map_to_canvas(g_values_2[:, 0], axis_min=x_axis_2.x_min, axis_max=x_axis_2.x_max, axis_end=x_axis_2.axis_length_on_canvas)
        g_values_2[:, 1] = map_to_canvas(g_values_2[:, 1], axis_min=y_axis_2.y_min, axis_max=y_axis_2.y_max, axis_end=y_axis_2.axis_length_on_canvas)
        a2 = Arrow(start=g_values_2[0], end=g_values_2[1], fill_color=BLUE, thickness=3.0, tip_width_ratio=5, buff=0)
        panel_2 = VGroup(axes_2, curve_2, x_label_2, p2, a2)
        curve_1.set_stroke(opacity=0.5)
        curve_2.set_stroke(opacity=0.5)
        panel_2.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        panel_1.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        self.add(panel_1, panel_2)
        self.frame.reorient(0, 89, 0, (-0.46, 0.0, 1.36), 8.97)
        panel_1_shift = [-5, 0, 2.0]
        panel_2_shift = [-5, 0, -2.0]
        panel_1.shift(panel_1_shift)
        panel_2.shift(panel_2_shift)
        self.wait()
        num_steps = 7
        grad_adjustment_factors = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
        descent_points_1 = []
        arrow_end_points_1 = []
        p1_values_3 = param_surface(0, 0)
        g = get_grads(0, 0)
        grad_viz_scale = 1.25 * abs(g[2])
        descent_points_1.append([p1_values_3[0], p1_values_3[2], 0])
        for i in range(1, num_steps):
            g = get_grads(descent_points_1[i - 1][0], 0)
            grad_viz_scale = 1.25 * abs(g[2])
            new_x = descent_points_1[i - 1][0] + grad_viz_scale
            arrow_end_points_1.append([new_x, descent_points_1[i - 1][1] + grad_viz_scale * g[2] * grad_adjustment_factors[i], 0])
            descent_points_1.append([new_x, param_surface(new_x, 0)[2], 0])
        descent_points_1 = np.array(descent_points_1)
        arrow_end_points_1 = np.array(arrow_end_points_1)
        descent_points_1_mapped = np.zeros_like(descent_points_1)
        descent_points_1_mapped[:, 0] = map_to_canvas(descent_points_1[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        descent_points_1_mapped[:, 1] = map_to_canvas(descent_points_1[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        arrow_end_points_1_mapped = np.zeros_like(arrow_end_points_1)
        arrow_end_points_1_mapped[:, 0] = map_to_canvas(arrow_end_points_1[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        arrow_end_points_1_mapped[:, 1] = map_to_canvas(arrow_end_points_1[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        arrows_1 = VGroup()
        points_1 = VGroup()
        for i in range(num_steps - 1):
            arrows_1.add(Arrow(start=descent_points_1_mapped[i], end=arrow_end_points_1_mapped[i], fill_color=YELLOW, thickness=3.0, tip_width_ratio=5, buff=0))
            points_1.add(Dot(descent_points_1_mapped[i], radius=0.06, fill_color=YELLOW))
        arrows_1.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        arrows_1.shift(panel_1_shift)
        points_1.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        points_1.shift(panel_1_shift)
        grad_adjustment_factors = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        descent_points_2 = []
        arrow_end_points_2 = []
        p1_values_3 = param_surface(0, 0)
        g = get_grads(0, 0)
        grad_viz_scale = 1.25 * abs(g[3])
        descent_points_2.append([p1_values_3[1], p1_values_3[2], 0])
        for i in range(1, num_steps):
            g = get_grads(0, descent_points_2[i - 1][0])
            grad_viz_scale = 1.25 * abs(g[3])
            new_x = descent_points_2[i - 1][0] + grad_viz_scale
            arrow_end_points_2.append([new_x, descent_points_2[i - 1][1] + grad_viz_scale * g[3] * grad_adjustment_factors[i], 0])
            descent_points_2.append([new_x, param_surface(0, new_x)[2], 0])
        descent_points_2 = np.array(descent_points_2)
        arrow_end_points_2 = np.array(arrow_end_points_2)
        descent_points_2_mapped = np.zeros_like(descent_points_2)
        descent_points_2_mapped[:, 0] = map_to_canvas(descent_points_2[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        descent_points_2_mapped[:, 1] = map_to_canvas(descent_points_2[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        arrow_end_points_2_mapped = np.zeros_like(arrow_end_points_2)
        arrow_end_points_2_mapped[:, 0] = map_to_canvas(arrow_end_points_2[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        arrow_end_points_2_mapped[:, 1] = map_to_canvas(arrow_end_points_2[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        arrows_2 = VGroup()
        points_2 = VGroup()
        for i in range(num_steps - 1):
            arrows_2.add(Arrow(start=descent_points_2_mapped[i], end=arrow_end_points_2_mapped[i], fill_color=BLUE, thickness=3.0, tip_width_ratio=5, buff=0))
            points_2.add(Dot(descent_points_2_mapped[i], radius=0.06, fill_color=BLUE))
        arrows_2.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        arrows_2.shift(panel_2_shift)
        points_2.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        points_2.shift(panel_2_shift)
        self.add(arrows_2, points_2)
        self.wait()
        self.embed()