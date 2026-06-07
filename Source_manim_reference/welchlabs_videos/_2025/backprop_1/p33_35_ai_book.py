from manimlib import *
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
RED = '#EC2027'
BLUE = '#65c8d0'
surf = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/p_24_28_losses_4.npy')
xy = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/p_24_28_losses_4xy.npy')
grads_1 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/p_33_35_grads_1_2.npy')
grads_2 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/p_33_35_grads_2_2.npy')
xy_grads = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/p_33_35_xy_2.npy')

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
num_steps = 10
learning_rate = 1.05
grad_adjustment_factors_1 = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
grad_adjustment_factors_2 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
descent_points = []
arrow_end_points_1 = []
arrow_end_points_2 = []
starting_values = param_surface(0, 0)
descent_points.append(list(starting_values))
for i in range(1, num_steps):
    g = get_grads(descent_points[i - 1][0], descent_points[i - 1][1])
    step_x_1 = learning_rate * abs(g[2])
    step_x_2 = learning_rate * abs(g[3])
    new_x_1 = descent_points[i - 1][0] + step_x_1
    new_x_2 = descent_points[i - 1][1] + step_x_2
    arrow_end_points_1.append([new_x_1, descent_points[i - 1][2] + step_x_1 * g[2] * grad_adjustment_factors_1[i], 0])
    arrow_end_points_2.append([new_x_2, descent_points[i - 1][2] + step_x_2 * g[3] * grad_adjustment_factors_2[i], 0])
    descent_points.append([new_x_1, new_x_2, param_surface(new_x_1, new_x_2)[2]])
arrow_end_points_1 = np.array(arrow_end_points_1)
arrow_end_points_2 = np.array(arrow_end_points_2)
descent_points = np.array(descent_points)

class P33_35(InteractiveScene):

    def construct(self):
        x_axis_1 = WelchXAxis(x_min=-1.2, x_max=4.5, x_ticks=[-1, 0, 1, 2, 3, 4], x_tick_height=0.15, x_label_font_size=24, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_1 = WelchYAxis(y_min=0.3, y_max=2.2, y_ticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0], y_tick_width=0.15, y_label_font_size=20, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=3)
        axes_1 = VGroup(x_axis_1, y_axis_1)
        x_label_1 = Tex('\\theta_{1}', font_size=30).set_color(CHILL_BROWN)
        y_label_1 = Tex('Loss', font_size=25).set_color(CHILL_BROWN)
        x_label_1.next_to(x_axis_1, RIGHT, buff=0.05)
        y_label_1.next_to(y_axis_1, UP, buff=0.05)
        x_axis_2 = WelchXAxis(x_min=-1.2, x_max=4.5, x_ticks=[-1, 0, 1, 2, 3, 4], x_tick_height=0.15, x_label_font_size=24, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_2 = WelchYAxis(y_min=0.3, y_max=2.2, y_ticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0], y_tick_width=0.15, y_label_font_size=20, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=3)
        axes_2 = VGroup(x_axis_2, y_axis_2)
        x_label_2 = Tex('\\theta_{2}', font_size=30).set_color(CHILL_BROWN)
        y_label_2 = Tex('Loss', font_size=25).set_color(CHILL_BROWN)
        x_label_2.next_to(x_axis_2, RIGHT, buff=0.05)
        y_label_2.next_to(y_axis_2, UP, buff=0.05)
        curves_1 = VGroup()
        curves_2 = VGroup()
        points_1 = VGroup()
        points_2 = VGroup()
        arrows_1 = VGroup()
        arrows_2 = VGroup()
        lines_1 = VGroup()
        lines_2 = VGroup()
        descent_points_mapped_1 = np.zeros_like(descent_points)
        descent_points_mapped_1[:, 0] = map_to_canvas(descent_points[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        descent_points_mapped_1[:, 1] = map_to_canvas(descent_points[:, 2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        descent_points_mapped_2 = np.zeros_like(descent_points)
        descent_points_mapped_2[:, 0] = map_to_canvas(descent_points[:, 1], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        descent_points_mapped_2[:, 1] = map_to_canvas(descent_points[:, 2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        arrow_end_points_1_mapped = np.zeros_like(arrow_end_points_1)
        arrow_end_points_1_mapped[:, 0] = map_to_canvas(arrow_end_points_1[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        arrow_end_points_1_mapped[:, 1] = map_to_canvas(arrow_end_points_1[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        arrow_end_points_2_mapped = np.zeros_like(arrow_end_points_2)
        arrow_end_points_2_mapped[:, 0] = map_to_canvas(arrow_end_points_2[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        arrow_end_points_2_mapped[:, 1] = map_to_canvas(arrow_end_points_2[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        for i in range(len(descent_points)):
            p1 = np.array([param_surface(u, descent_points[i][1]) for u in np.linspace(-1, 4, 128)])
            points_mapped = np.zeros_like(p1)
            points_mapped[:, 0] = map_to_canvas(p1[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
            points_mapped[:, 1] = map_to_canvas(p1[:, 2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
            c = VMobject()
            c.set_points_smoothly(points_mapped)
            c.set_stroke(width=4, color=RED, opacity=0.8)
            curves_1.add(c)
            p = Dot(descent_points_mapped_1[i], radius=0.06, fill_color=RED)
            points_1.add(p)
            p1 = np.array([param_surface(descent_points[i][0], v) for v in np.linspace(-1, 4, 128)])
            points_mapped = np.zeros_like(p1)
            points_mapped[:, 0] = map_to_canvas(p1[:, 1], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
            points_mapped[:, 1] = map_to_canvas(p1[:, 2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
            c = VMobject()
            c.set_points_smoothly(points_mapped)
            c.set_stroke(width=4, color=BLUE, opacity=0.8)
            curves_2.add(c)
            p = Dot(descent_points_mapped_2[i], radius=0.06, fill_color=BLUE)
            points_2.add(p)
            if i > 0:
                lines_1.add(Line(start=[descent_points_mapped_1[i - 1][0], descent_points_mapped_1[i - 1][1], 0], end=[descent_points_mapped_1[i][0], descent_points_mapped_1[i][1], 0], color=RED, buff=0, stroke_width=1.5))
                arrows_1.add(Arrow(start=[descent_points_mapped_1[i - 1][0], descent_points_mapped_1[i - 1][1], 0], end=arrow_end_points_1_mapped[i - 1], fill_color=RED, thickness=3.0, tip_width_ratio=5, buff=0, max_width_to_length_ratio=0.2))
                lines_2.add(Line(start=[descent_points_mapped_2[i - 1][0], descent_points_mapped_2[i - 1][1], 0], end=[descent_points_mapped_2[i][0], descent_points_mapped_2[i][1], 0], color=BLUE, buff=0, stroke_width=1.5))
                arrows_2.add(Arrow(start=[descent_points_mapped_2[i - 1][0], descent_points_mapped_2[i - 1][1], 0], end=arrow_end_points_2_mapped[i - 1], fill_color=BLUE, thickness=3.0, tip_width_ratio=5, buff=0, max_width_to_length_ratio=0.2))
        panel_1 = VGroup(axes_1, x_label_1, y_label_1, curves_1, points_1, arrows_1, lines_1)
        panel_1.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        panel_2 = VGroup(axes_2, x_label_2, y_label_2, curves_2, points_2, arrows_2, lines_2)
        panel_2.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        panel_1_shift = [-5, 0, 2.0]
        panel_2_shift = [-5, 0, -2.0]
        panel_1.shift(panel_1_shift)
        panel_2.shift(panel_2_shift)
        self.frame.reorient(0, 89, 0, (-0.46, 0.0, 1.36), 8.97)
        curves_1[0].set_stroke(opacity=0.5)
        curves_2[0].set_stroke(opacity=0.5)
        panel_1_start = VGroup(axes_1, x_label_1, y_label_1, curves_1[0], points_1[0], arrows_1[0])
        panel_2_start = VGroup(axes_2, x_label_2, y_label_2, curves_2[0], points_2[0], arrows_2[0])
        self.add(panel_1_start)
        self.add(panel_2_start)
        self.wait()

        def get_arrow_1(u):
            start = param_surface(u, 0)
            g = get_grads(u + 0.2, 0)
            step_x_1 = 0.6
            new_x = start[0] + step_x_1
            new_y = start[2] + step_x_1 * g[2] * 0.7
            mapped_values = np.zeros((2, 2))
            mapped_values[:, 0] = map_to_canvas(np.array([start[0], new_x]), axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
            mapped_values[:, 1] = map_to_canvas(np.array([start[2], new_y]), axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
            a = Arrow(start=[mapped_values[0, 0], mapped_values[0, 1], 0], end=[mapped_values[1, 0], mapped_values[1, 1], 0], fill_color=RED, thickness=3.0, tip_width_ratio=5, buff=0, max_width_to_length_ratio=0.2)
            a.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
            a.shift(panel_1_shift)
            return a

        def get_arrow_2(v):
            start = param_surface(0, v)
            g = get_grads(0, v * 0.75)
            step_x_1 = 0.6
            new_x = start[1] + step_x_1
            if v > 0:
                new_y = start[2] + step_x_1 * g[3]
            else:
                new_y = start[2] + step_x_1 * g[3] - 0.2 * abs(v)
            mapped_values = np.zeros((2, 2))
            mapped_values[:, 0] = map_to_canvas(np.array([start[1], new_x]), axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
            mapped_values[:, 1] = map_to_canvas(np.array([start[2], new_y]), axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
            a = Arrow(start=[mapped_values[0, 0], mapped_values[0, 1], 0], end=[mapped_values[1, 0], mapped_values[1, 1], 0], fill_color=BLUE, thickness=3.0, tip_width_ratio=5, buff=0, max_width_to_length_ratio=0.2)
            a.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
            a.shift(panel_2_shift)
            return a
        initial_time = 0
        t_tracker = ValueTracker(initial_time)
        moving_arrow_1 = always_redraw(lambda: get_arrow_1(t_tracker.get_value()))
        moving_arrow_2 = always_redraw(lambda: get_arrow_2(t_tracker.get_value()))
        self.remove(arrows_1[0], arrows_2[0])
        self.add(moving_arrow_1, moving_arrow_2)
        self.play(t_tracker.animate.set_value(1.6), run_time=3)
        self.play(t_tracker.animate.set_value(-0.5), run_time=3)
        self.play(t_tracker.animate.set_value(0), run_time=3)
        self.remove(moving_arrow_1, moving_arrow_2)
        self.add(arrows_1[0], arrows_2[0])
        self.wait()
        r = panel_2.get_corner(LEFT + BOTTOM)
        r[0] = -4.15
        self.wait()
        self.play(y_axis_2.animate.set_opacity(0.0), x_axis_1[-1].animate.set_opacity(0.0), x_axis_2[-1].animate.set_opacity(0.0), y_axis_1[-1].animate.set_opacity(0.0), x_axis_1[-2].animate.set_opacity(0.0), x_axis_2[-2].animate.set_opacity(0.0), y_axis_1[-2].animate.set_opacity(0.0), y_label_2.animate.set_opacity(0.0), run_time=1.0)
        self.play(panel_1_start.animate.shift([0, 0, -2.0]), panel_2_start.animate.rotate(90 * DEGREES, [0, 0, 1], about_point=r).shift([0, 0, 2.0]), self.frame.animate.reorient(13, 85, 0, (-1.88, -0.77, 1.56), 5.01), run_time=4)
        self.wait()
        surface = ParametricSurface(param_surface, u_range=[-1, 4], v_range=[-1, 4], resolution=(256, 256))
        ts = TexturedSurface(surface, '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/p_24_28_losses_4.png')
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
        self.remove(arrows_1[0])
        self.add(arrows_1[0])
        self.remove(arrows_2[0])
        self.add(arrows_2[0])
        self.remove(points_1[0])
        self.add(points_1[0])
        self.remove(points_2[0])
        self.add(points_2[0])
        self.play(ts.animate.set_opacity(0.5), points_1[0].animate.set_opacity(0.0), points_2[0].animate.set_opacity(0.0), arrows_1[0].animate.rotate(-DEGREES * 135, axis=arrows_1[0].get_end() - arrows_1[0].get_start()), arrows_2[0].animate.rotate(-DEGREES * 80, axis=arrows_2[0].get_end() - arrows_2[0].get_start()), u_gridlines.animate.set_stroke(opacity=0.5), v_gridlines.animate.set_stroke(opacity=0.5), self.frame.animate.reorient(124, 40, 0, (-2.57, 0.86, 2.7), 1.81), run_time=4.0)
        self.wait()
        self.remove(x_label_1)
        self.remove(x_label_2)
        self.remove(y_label_1)
        self.remove(arrows_1)
        self.remove(arrows_2)
        self.wait()
        self.frame.reorient(-150, 60, 0, (-3.52, 1.99, 1.55), 5.15)
        self.wait(5)
        self.embed()

class P33_35_2D(InteractiveScene):

    def construct(self):
        x_axis_1 = WelchXAxis(x_min=-1.2, x_max=4.5, x_ticks=[-1, 0, 1, 2, 3, 4], x_tick_height=0.15, x_label_font_size=24, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_1 = WelchYAxis(y_min=0.3, y_max=2.2, y_ticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0], y_tick_width=0.15, y_label_font_size=20, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=3)
        axes_1 = VGroup(x_axis_1, y_axis_1)
        x_label_1 = Tex('\\theta_{1}', font_size=30).set_color(CHILL_BROWN)
        y_label_1 = Tex('Loss', font_size=25).set_color(CHILL_BROWN)
        x_label_1.next_to(x_axis_1, RIGHT, buff=0.05)
        y_label_1.next_to(y_axis_1, UP, buff=0.05)
        x_axis_2 = WelchXAxis(x_min=-1.2, x_max=4.5, x_ticks=[-1, 0, 1, 2, 3, 4], x_tick_height=0.15, x_label_font_size=24, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_2 = WelchYAxis(y_min=0.3, y_max=2.2, y_ticks=[0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0], y_tick_width=0.15, y_label_font_size=20, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=3)
        axes_2 = VGroup(x_axis_2, y_axis_2)
        x_label_2 = Tex('\\theta_{2}', font_size=30).set_color(CHILL_BROWN)
        y_label_2 = Tex('Loss', font_size=25).set_color(CHILL_BROWN)
        x_label_2.next_to(x_axis_2, RIGHT, buff=0.05)
        y_label_2.next_to(y_axis_2, UP, buff=0.05)
        curves_1 = VGroup()
        curves_2 = VGroup()
        points_1 = VGroup()
        points_2 = VGroup()
        arrows_1 = VGroup()
        arrows_2 = VGroup()
        lines_1 = VGroup()
        lines_2 = VGroup()
        descent_points_mapped_1 = np.zeros_like(descent_points)
        descent_points_mapped_1[:, 0] = map_to_canvas(descent_points[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        descent_points_mapped_1[:, 1] = map_to_canvas(descent_points[:, 2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        descent_points_mapped_2 = np.zeros_like(descent_points)
        descent_points_mapped_2[:, 0] = map_to_canvas(descent_points[:, 1], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        descent_points_mapped_2[:, 1] = map_to_canvas(descent_points[:, 2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        arrow_end_points_1_mapped = np.zeros_like(arrow_end_points_1)
        arrow_end_points_1_mapped[:, 0] = map_to_canvas(arrow_end_points_1[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        arrow_end_points_1_mapped[:, 1] = map_to_canvas(arrow_end_points_1[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        arrow_end_points_2_mapped = np.zeros_like(arrow_end_points_2)
        arrow_end_points_2_mapped[:, 0] = map_to_canvas(arrow_end_points_2[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
        arrow_end_points_2_mapped[:, 1] = map_to_canvas(arrow_end_points_2[:, 1], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
        for i in range(len(descent_points)):
            p1 = np.array([param_surface(u, descent_points[i][1]) for u in np.linspace(-1, 4, 128)])
            points_mapped = np.zeros_like(p1)
            points_mapped[:, 0] = map_to_canvas(p1[:, 0], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
            points_mapped[:, 1] = map_to_canvas(p1[:, 2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
            c = VMobject()
            c.set_points_smoothly(points_mapped)
            c.set_stroke(width=4, color=RED, opacity=0.8)
            curves_1.add(c)
            p = Dot(descent_points_mapped_1[i], radius=0.06, fill_color=RED)
            points_1.add(p)
            p1 = np.array([param_surface(descent_points[i][0], v) for v in np.linspace(-1, 4, 128)])
            points_mapped = np.zeros_like(p1)
            points_mapped[:, 0] = map_to_canvas(p1[:, 1], axis_min=x_axis_1.x_min, axis_max=x_axis_1.x_max, axis_end=x_axis_1.axis_length_on_canvas)
            points_mapped[:, 1] = map_to_canvas(p1[:, 2], axis_min=y_axis_1.y_min, axis_max=y_axis_1.y_max, axis_end=y_axis_1.axis_length_on_canvas)
            c = VMobject()
            c.set_points_smoothly(points_mapped)
            c.set_stroke(width=4, color=BLUE, opacity=0.8)
            curves_2.add(c)
            p = Dot(descent_points_mapped_2[i], radius=0.06, fill_color=BLUE)
            points_2.add(p)
            if i > 0:
                lines_1.add(Line(start=[descent_points_mapped_1[i - 1][0], descent_points_mapped_1[i - 1][1], 0], end=[descent_points_mapped_1[i][0], descent_points_mapped_1[i][1], 0], color=RED, buff=0, stroke_width=1.5))
                arrows_1.add(Arrow(start=[descent_points_mapped_1[i - 1][0], descent_points_mapped_1[i - 1][1], 0], end=arrow_end_points_1_mapped[i - 1], fill_color=RED, thickness=3.0, tip_width_ratio=5, buff=0))
                lines_2.add(Line(start=[descent_points_mapped_2[i - 1][0], descent_points_mapped_2[i - 1][1], 0], end=[descent_points_mapped_2[i][0], descent_points_mapped_2[i][1], 0], color=BLUE, buff=0, stroke_width=1.5))
                arrows_2.add(Arrow(start=[descent_points_mapped_2[i - 1][0], descent_points_mapped_2[i - 1][1], 0], end=arrow_end_points_2_mapped[i - 1], fill_color=BLUE, thickness=3.0, tip_width_ratio=5, buff=0))
        panel_1 = VGroup(axes_1, x_label_1, y_label_2, curves_1, points_1, arrows_1, lines_1)
        panel_1.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        panel_2 = VGroup(axes_2, x_label_2, y_label_2, curves_2, points_2, arrows_2, lines_2)
        panel_2.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        panel_1_shift = [-5, 0, 2.0]
        panel_2_shift = [-5, 0, -2.0]
        panel_1.shift(panel_1_shift)
        panel_2.shift(panel_2_shift)
        self.add(panel_1, panel_2)
        self.frame.reorient(0, 89, 0, (-0.46, 0.0, 1.36), 8.97)
        self.wait()
        self.embed()
        self.wait(20)
from manimlib import *
from functools import partial
CHILL_BROWN = '#948979'
BLUE = '#65c8d0'
WELCH_ASSET_PATH = '/Users/stephen/manim/videos/welch_assets'

def generate_nice_ticks(min_val, max_val, min_ticks=3, max_ticks=16, ignore=[0]):
    if min_val > max_val:
        min_val, max_val = (max_val, min_val)
    if abs(max_val - min_val) < 1e-10:
        min_val = min_val - 1
        max_val = max_val + 1
    range_val = max_val - min_val
    power = np.floor(np.log10(range_val))
    possible_step_sizes = [10 ** power, 5 * 10 ** (power - 1), 2 * 10 ** (power - 1), 10 ** (power - 1)]
    chosen_step = possible_step_sizes[0]
    for step in possible_step_sizes:
        first_tick = np.ceil(min_val / step) * step
        last_tick = np.floor(max_val / step) * step
        num_ticks = 0
        current = first_tick
        while current <= last_tick * (1 + 1e-10):
            if not any((abs(current - ignored_val) < 1e-10 for ignored_val in ignore)):
                num_ticks += 1
            current += step
        if min_ticks <= num_ticks <= max_ticks:
            chosen_step = step
            break
        elif num_ticks > max_ticks:
            break
    first_tick = np.floor(min_val / chosen_step) * chosen_step
    last_tick = np.ceil(max_val / chosen_step) * chosen_step
    axis_min = first_tick - chosen_step
    axis_max = last_tick + chosen_step
    ticks = []
    current = np.ceil(min_val / chosen_step) * chosen_step
    while current <= max_val * (1 + 1e-10):
        if not any((abs(current - ignored_val) < 1e-10 for ignored_val in ignore)):
            ticks.append(float(current))
        current += chosen_step
    if len(ticks) < min_ticks and possible_step_sizes.index(chosen_step) < len(possible_step_sizes) - 1:
        return generate_nice_ticks(min_val, max_val, min_ticks, max_ticks, ignore)
    return (ticks, float(axis_min), float(axis_max))

class WelchXAxis(VGroup):

    def __init__(self, x_min=0, x_max=6, x_ticks=[1, 2, 3, 4, 5], x_tick_height=0.15, x_label_font_size=24, stroke_width=3, color=CHILL_BROWN, arrow_tip_scale=0.1, axis_length_on_canvas=5, include_tip=True, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.x_ticks = x_ticks
        self.x_tick_height = x_tick_height
        self.x_label_font_size = x_label_font_size
        self.stroke_width = stroke_width
        self.axis_color = color
        self.arrow_tip_scale = arrow_tip_scale
        self.x_min = x_min
        self.x_max = x_max
        self.axis_length_on_canvas = axis_length_on_canvas
        self.include_tip = include_tip
        self.axis_to_canvas_scale = (self.x_max - self.x_min) / axis_length_on_canvas
        self.x_ticks_scaled = (np.array(x_ticks) - self.x_min) / self.axis_to_canvas_scale
        self._create_axis_line()
        self._create_ticks()
        self._create_labels()

    def _create_axis_line(self):
        axis_line = Line(start=np.array([0, 0, 0]), end=np.array([self.axis_length_on_canvas, 0, 0]), color=self.axis_color, stroke_width=self.stroke_width)
        if self.include_tip:
            arrow_tip = SVGMobject(WELCH_ASSET_PATH + '/welch_arrow_tip_1.svg')
            arrow_tip.scale(self.arrow_tip_scale)
            arrow_tip.move_to([self.axis_length_on_canvas, 0, 0])
            axis_line = VGroup(axis_line, arrow_tip)
        self.add(axis_line)

    def _create_ticks(self):
        self.ticks = VGroup()
        for x_val in self.x_ticks_scaled:
            tick = Line(start=np.array([x_val, 0, 0]), end=np.array([x_val, -self.x_tick_height, 0]), color=self.axis_color, stroke_width=self.stroke_width)
            self.ticks.add(tick)
        self.add(self.ticks)

    def _create_labels(self):
        self.labels = VGroup()
        for x_val, x_val_label in zip(self.x_ticks_scaled, self.x_ticks):
            label = Tex(str(round(x_val_label, 4)))
            label.scale(self.x_label_font_size / 48)
            label.set_color(self.axis_color)
            label.next_to(np.array([x_val, -self.x_tick_height, 0]), DOWN, buff=0.1)
            self.labels.add(label)
        self.add(self.labels)

    def get_axis_line(self):
        return self.axis_line

    def get_ticks(self):
        return self.ticks

    def get_labels(self):
        return self.labels

    def map_to_canvas(self, value, axis_start=0):
        value_scaled = (value - self.x_min) / (self.x_max - self.x_min)
        return (value_scaled + axis_start) * self.axis_length_on_canvas

class WelchYAxis(VGroup):

    def __init__(self, y_min=0, y_max=6, y_ticks=[1, 2, 3, 4, 5], y_tick_width=0.15, y_label_font_size=24, stroke_width=3, color=CHILL_BROWN, arrow_tip_scale=0.1, axis_length_on_canvas=5, include_tip=True, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.y_ticks = y_ticks
        self.y_tick_width = y_tick_width
        self.y_label_font_size = y_label_font_size
        self.stroke_width = stroke_width
        self.axis_color = color
        self.arrow_tip_scale = arrow_tip_scale
        self.y_min = y_min
        self.y_max = y_max
        self.axis_length_on_canvas = axis_length_on_canvas
        self.include_tip = include_tip
        self.axis_to_canvas_scale = (self.y_max - self.y_min) / axis_length_on_canvas
        self.y_ticks_scaled = (np.array(y_ticks) - self.y_min) / self.axis_to_canvas_scale
        self._create_axis_line()
        self._create_ticks()
        self._create_labels()

    def _create_axis_line(self):
        axis_line = Line(start=np.array([0, 0, 0]), end=np.array([0, self.axis_length_on_canvas, 0]), color=self.axis_color, stroke_width=self.stroke_width)
        if self.include_tip:
            arrow_tip = SVGMobject(WELCH_ASSET_PATH + '/welch_arrow_tip_1.svg')
            arrow_tip.scale(self.arrow_tip_scale)
            arrow_tip.move_to([0, self.axis_length_on_canvas, 0])
            arrow_tip.rotate(PI / 2)
            axis_line = VGroup(axis_line, arrow_tip)
        self.add(axis_line)

    def _create_ticks(self):
        self.ticks = VGroup()
        for y_val in self.y_ticks_scaled:
            tick = Line(start=np.array([0, y_val, 0]), end=np.array([-self.y_tick_width, y_val, 0]), color=self.axis_color, stroke_width=self.stroke_width)
            self.ticks.add(tick)
        self.add(self.ticks)

    def _create_labels(self):
        self.labels = VGroup()
        for y_val, y_val_label in zip(self.y_ticks_scaled, self.y_ticks):
            label = Tex(str(round(y_val_label, 5)))
            label.scale(self.y_label_font_size / 48)
            label.set_color(self.axis_color)
            label.next_to(np.array([-self.y_tick_width, y_val, 0]), LEFT, buff=0.1)
            self.labels.add(label)
        self.add(self.labels)

    def get_axis_line(self):
        return self.axis_line

    def get_ticks(self):
        return self.ticks

    def get_labels(self):
        return self.labels

    def map_to_canvas(self, value, axis_start=0):
        value_scaled = (value - self.y_min) / (self.y_max - self.y_min)
        return (value_scaled + axis_start) * self.axis_length_on_canvas