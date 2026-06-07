from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
from functools import partial
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
loss_curve_1 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_24_5/all_execpt_embedding_random_64.npy')
loss_curve_2 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_24_5/all_execpt_embedding_random_51.npy')
loss_curve_3 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_24_7/all_execpt_embedding_pretrained_19.npy')
loss_curve_4 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_24_7/all_execpt_embedding_pretrained_27.npy')
alphas_1 = np.linspace(-2.5, 2.5, 512)
loss_2d_1 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_25_1/000.npy')

class Dot3D(Sphere):

    def __init__(self, center=ORIGIN, radius=0.05, **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.move_to(center)

def param_surface_1(u, v):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = 0.07 * loss_2d_1[v_idx, u_idx]
    except IndexError:
        z = 0
    return np.array([u, v, z])

def param_surface_2(u, v, surf_array):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = 0.07 * surf_array[v_idx, u_idx]
    except IndexError:
        z = 0
    return np.array([u, v, z])

def get_pivot_and_scale(axis_min, axis_max, axis_end):
    scale = axis_end / (axis_max - axis_min)
    return (axis_min, scale)

def get_numerical_gradient(surface_fn, u, v, epsilon=0.01):
    height = surface_fn(u, v)[2]
    height_du = surface_fn(u + epsilon, v)[2]
    du = (height_du - height) / epsilon
    height_dv = surface_fn(u, v + epsilon)[2]
    dv = (height_dv - height) / epsilon
    return (du, dv)
import numpy as np

def find_local_minima(surface):
    rows, cols = surface.shape
    minima = []
    for i in range(rows):
        for j in range(cols):
            current_val = surface[i, j]
            neighbors = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = (i + di, j + dj)
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbors.append((ni, nj))
            is_minimum = True
            for ni, nj in neighbors:
                if surface[ni, nj] < current_val:
                    is_minimum = False
                    break
            if is_minimum:
                minima.append((i, j))
    return minima

def manual_camera_interpolation(start_orientation, end_orientation, num_steps):
    result = []
    for step in range(num_steps):
        t = step / (num_steps - 1) if num_steps > 1 else 0
        interpolated = []
        for i in range(len(start_orientation)):
            if i == 3:
                start_tuple = start_orientation[i]
                end_tuple = end_orientation[i]
                interpolated_tuple = tuple((start_tuple[j] + t * (end_tuple[j] - start_tuple[j]) for j in range(len(start_tuple))))
                interpolated.append(interpolated_tuple)
            else:
                start_val = start_orientation[i]
                end_val = end_orientation[i]
                interpolated_val = start_val + t * (end_val - start_val)
                interpolated.append(interpolated_val)
        result.append(interpolated)
    return result

class P39_48(InteractiveScene):

    def construct(self):
        x_axis_1 = WelchXAxis(x_min=-2.5, x_max=2.5, x_ticks=[-2.0, -1.0, 0, 1.0, 2.0], x_tick_height=0.15, x_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=8)
        y_axis_1 = WelchYAxis(y_min=8, y_max=16, y_ticks=[8, 9, 10, 11, 12, 13, 14, 15], y_tick_width=0.15, y_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=6)
        x_label_1 = Tex('\\alpha', font_size=36).set_color(CHILL_BROWN)
        y_label_1 = Tex('Loss', font_size=30).set_color(CHILL_BROWN)
        x_label_1.next_to(x_axis_1, RIGHT, buff=0.05)
        y_label_1.next_to(y_axis_1, UP, buff=0.08)
        mapped_x_1 = x_axis_1.map_to_canvas(loss_curve_1[0, :])
        mapped_y_1 = y_axis_1.map_to_canvas(loss_curve_1[1, :])
        curve_1 = VMobject()
        curve_1.set_points_smoothly(np.vstack((mapped_x_1, mapped_y_1, np.zeros_like(mapped_x_1))).T)
        curve_1.set_stroke(width=4, color=YELLOW, opacity=1.0)
        axes_1 = VGroup(x_axis_1, y_axis_1, x_label_1, y_label_1, curve_1)
        axes_1.move_to([0, 0, 0])
        axes_1.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        self.frame.reorient(0, 90, 0, (-0.21, -0.01, -0.02), 8.0)
        self.add(x_axis_1, y_axis_1, x_label_1, y_label_1)
        self.wait(0)
        self.play(ShowCreation(curve_1), run_time=5)
        self.wait()
        x_axis_2 = WelchXAxis(x_min=-2.5, x_max=2.5, x_ticks=[-2.0, -1.0, 0, 1.0, 2.0], x_tick_height=0.15, x_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=8)
        y_axis_2 = WelchYAxis(y_min=8, y_max=16, y_ticks=[8, 9, 10, 11, 12, 13, 14, 15], y_tick_width=0.15, y_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=6)
        x_label_2 = Tex('\\alpha', font_size=36).set_color(CHILL_BROWN)
        y_label_2 = Tex('Loss', font_size=30).set_color(CHILL_BROWN)
        x_label_2.next_to(x_axis_2, RIGHT, buff=0.05)
        y_label_2.next_to(y_axis_2, UP, buff=0.08)
        mapped_x_2 = x_axis_2.map_to_canvas(loss_curve_2[0, :])
        mapped_y_2 = y_axis_2.map_to_canvas(loss_curve_2[1, :])
        curve_2 = VMobject()
        curve_2.set_points_smoothly(np.vstack((mapped_x_2, mapped_y_2, np.zeros_like(mapped_x_2))).T)
        curve_2.set_stroke(width=4, color=YELLOW, opacity=1.0)
        axes_2 = VGroup(x_axis_2, y_axis_2, x_label_2, y_label_2, curve_2)
        axes_2.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        axes_2.move_to([10, 0, 0])
        self.play(self.frame.animate.reorient(0, 90, 0, (5.03, 0.05, 0.0), 12.15), FadeIn(VGroup(x_axis_2, y_axis_2, x_label_2, y_label_2)), ShowCreation(curve_2), run_time=3.0)
        self.wait()
        x_axis_3 = WelchXAxis(x_min=-2.5, x_max=2.5, x_ticks=[-2.0, -1.0, 0, 1.0, 2.0], x_tick_height=0.15, x_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=8)
        y_axis_3 = WelchYAxis(y_min=0, y_max=40, y_ticks=[0, 5, 10, 15, 20, 25, 30, 35], y_tick_width=0.15, y_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=6)
        x_label_3 = Tex('\\alpha', font_size=36).set_color(CHILL_BROWN)
        y_label_3 = Tex('Loss', font_size=30).set_color(CHILL_BROWN)
        x_label_3.next_to(x_axis_3, RIGHT, buff=0.05)
        y_label_3.next_to(y_axis_3, UP, buff=0.08)
        mapped_x_3 = x_axis_3.map_to_canvas(loss_curve_3[0, :])
        mapped_y_3 = y_axis_3.map_to_canvas(loss_curve_3[1, :])
        curve_3 = VMobject()
        curve_3.set_points_smoothly(np.vstack((mapped_x_3, mapped_y_3, np.zeros_like(mapped_x_3))).T)
        curve_3.set_stroke(width=4, color=BLUE, opacity=1.0)
        axes_3 = VGroup(x_axis_3, y_axis_3, x_label_3, y_label_3, curve_3)
        axes_3.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        axes_3.move_to([10, 0, 0])
        x_axis_4 = WelchXAxis(x_min=-2.5, x_max=2.5, x_ticks=[-2.0, -1.0, 0, 1.0, 2.0], x_tick_height=0.15, x_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=8)
        y_axis_4 = WelchYAxis(y_min=0, y_max=40, y_ticks=[0, 5, 10, 15, 20, 25, 30, 35], y_tick_width=0.15, y_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=6)
        x_label_4 = Tex('\\alpha', font_size=36).set_color(CHILL_BROWN)
        y_label_4 = Tex('Loss', font_size=30).set_color(CHILL_BROWN)
        x_label_4.next_to(x_axis_4, RIGHT, buff=0.05)
        y_label_4.next_to(y_axis_4, UP, buff=0.08)
        mapped_x_4 = x_axis_4.map_to_canvas(loss_curve_4[0, :])
        mapped_y_4 = y_axis_4.map_to_canvas(loss_curve_4[1, :])
        curve_4 = VMobject()
        curve_4.set_points_smoothly(np.vstack((mapped_x_4, mapped_y_4, np.zeros_like(mapped_x_3))).T)
        curve_4.set_stroke(width=4, color=BLUE, opacity=1.0)
        axes_4 = VGroup(x_axis_4, y_axis_4, x_label_4, y_label_4, curve_4)
        axes_4.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        axes_4.move_to([10, 0, -7])
        self.wait()
        self.play(axes_2.animate.move_to([0, 0, -7]), self.frame.animate.reorient(0, 90, 0, (4.6, -3.5, -3.6), 12.54), run_time=2.0)
        self.play(FadeIn(VGroup(x_axis_3, y_axis_3, x_label_3, y_label_3)), FadeIn(VGroup(x_axis_4, y_axis_4, x_label_4, y_label_4)), ShowCreation(curve_3), ShowCreation(curve_4), run_time=4)
        self.wait()
        slice_1 = loss_2d_1[255, :]
        slice_2 = loss_2d_1[:, 255]
        x_axis_5 = WelchXAxis(x_min=-2.5, x_max=2.5, x_ticks=[-2.0, -1.0, 0, 1.0, 2.0], x_tick_height=0.15, x_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=8)
        y_axis_5 = WelchYAxis(y_min=0, y_max=25, y_ticks=[0, 5, 10, 15, 20], y_tick_width=0.15, y_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=6)
        x_label_5 = Tex('\\alpha', font_size=36).set_color(CHILL_BROWN)
        y_label_5 = Tex('Loss', font_size=30).set_color(CHILL_BROWN)
        x_label_5.next_to(x_axis_5, RIGHT, buff=0.05)
        y_label_5.next_to(y_axis_5, UP, buff=0.08)
        mapped_x_5 = x_axis_5.map_to_canvas(alphas_1)
        mapped_y_5 = y_axis_5.map_to_canvas(slice_1)
        curve_5 = VMobject()
        curve_5.set_points_smoothly(np.vstack((mapped_x_5, mapped_y_5, np.zeros_like(mapped_x_5))).T)
        curve_5.set_stroke(width=4, color='#FF00FF', opacity=1.0)
        axes_5 = VGroup(x_axis_5, y_axis_5, x_label_5, y_label_5, curve_5)
        axes_5.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        axes_5.move_to([20, 0, 0])
        x_axis_6 = WelchXAxis(x_min=-2.5, x_max=2.5, x_ticks=[-2.0, -1.0, 0, 1.0, 2.0], x_tick_height=0.15, x_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=8)
        y_axis_6 = WelchYAxis(y_min=0, y_max=25, y_ticks=[0, 5, 10, 15, 20], y_tick_width=0.15, y_label_font_size=32, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=6)
        x_label_6 = Tex('\\alpha', font_size=36).set_color(CHILL_BROWN)
        y_label_6 = Tex('Loss', font_size=30).set_color(CHILL_BROWN)
        x_label_6.next_to(x_axis_6, RIGHT, buff=0.05)
        y_label_6.next_to(y_axis_6, UP, buff=0.08)
        mapped_x_6 = x_axis_6.map_to_canvas(alphas_1)
        mapped_y_6 = y_axis_6.map_to_canvas(slice_2)
        curve_6 = VMobject()
        curve_6.set_points_smoothly(np.vstack((mapped_x_6, mapped_y_6, np.zeros_like(mapped_x_6))).T)
        curve_6.set_stroke(width=4, color='#FF00FF', opacity=1.0)
        axes_6 = VGroup(x_axis_6, y_axis_6, x_label_6, y_label_6, curve_6)
        axes_6.rotate(90 * DEGREES, [1, 0, 0], about_point=ORIGIN)
        axes_6.move_to([20, 0, -7])
        self.wait()
        self.play(FadeIn(VGroup(x_axis_5, y_axis_5, x_label_5, y_label_5)), FadeIn(VGroup(x_axis_6, y_axis_6, x_label_6, y_label_6)), ShowCreation(curve_5), ShowCreation(curve_6), self.frame.animate.reorient(0, 89, 0, (9.97, -3.5, -3.39), 14.41), run_time=6)
        self.wait()
        surface = ParametricSurface(param_surface_1, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(128, 128))
        ts = TexturedSurface(surface, '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/loss_2d_1.png')
        ts.set_shading(0.0, 0.1, 0)
        pivot_x, scale_x = get_pivot_and_scale(axis_min=x_axis_5.x_min, axis_max=x_axis_5.x_max, axis_end=x_axis_5.axis_length_on_canvas)
        pivot_y, scale_y = get_pivot_and_scale(axis_min=y_axis_5.y_min, axis_max=y_axis_5.y_max, axis_end=y_axis_5.axis_length_on_canvas)
        num_lines = 32
        num_points = 512
        u_gridlines = VGroup()
        v_gridlines = VGroup()
        u_values = np.linspace(-2.5, 2.5, num_lines)
        v_points = np.linspace(-2.5, 2.5, num_points)
        for u in u_values:
            points = [param_surface_1(u, v) for v in v_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            u_gridlines.add(line)
        u_points = np.linspace(-2.5, 2.5, num_points)
        for v in u_values:
            points = [param_surface_1(u, v) for u in u_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            v_gridlines.add(line)
        surf_and_mesh = Group(ts, u_gridlines, v_gridlines)
        surf_and_mesh.scale([scale_x, scale_x, scale_y * 0.6], about_point=[pivot_x, pivot_x, pivot_y])
        surf_and_mesh.move_to([20, 0, 0])
        surf_and_mesh.shift([0.1, 0.075, -0.45])
        self.wait()
        axes_1.set_opacity(0)
        axes_2.set_opacity(0)
        axes_3.set_opacity(0)
        axes_4.set_opacity(0)
        y_axis_6.set_opacity(0)
        y_label_6.set_opacity(0)
        y_axis_5.set_opacity(0)
        y_label_5.set_opacity(0)
        axes_6[0][-1][2].set_opacity(0)
        curve_5.scale([1, 1, 0.6])
        curve_6.scale([1, 1, 0.6])
        axes_6.move_to([0, 0, 0])
        axes_6.rotate(90 * DEGREES, axis=[0, 0, 1])
        self.wait(0)
        self.frame.reorient(27, 37, 0, (18.74, 3.76, -6.28), 17.77)
        self.add(surf_and_mesh)
        self.wait()
        self.frame.reorient(27, 37, 0, (18.74, 3.76, -6.28), 17.77)
        self.embed()
        self.wait(20)

class sketch_3d(InteractiveScene):

    def construct(self):
        surface = ParametricSurface(param_surface_1, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
        ts = TexturedSurface(surface, '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/loss_2d_1.png')
        ts.set_shading(0.0, 0.1, 0)
        ts.scale([1, 1, 0.1])
        ts.move_to([0, 0, 0])
        self.add(ts)
        num_lines = 64
        num_points = 512
        u_gridlines = VGroup()
        v_gridlines = VGroup()
        u_values = np.linspace(-2.5, 2.5, num_lines)
        v_points = np.linspace(-2.5, 2.5, num_points)
        for u in u_values:
            points = [param_surface_1(u, v) for v in v_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            u_gridlines.add(line)
        u_points = np.linspace(-2.5, 2.5, num_points)
        for v in u_values:
            points = [param_surface_1(u, v) for u in u_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            v_gridlines.add(line)
        u_gridlines.scale([1, 1, 0.1])
        u_gridlines.move_to([0, 0, 0])
        v_gridlines.scale([1, 1, 0.1])
        v_gridlines.move_to([0, 0, 0])
        self.wait()
        self.frame.reorient(32, 38, 0, (0.12, -0.18, -0.23), 7.45)
        self.play(ShowCreation(u_gridlines), ShowCreation(v_gridlines), self.frame.animate.reorient(161, 33, 0, (0.11, -0.12, -0.23), 4.84), run_time=10)
        self.wait()
        self.add(ts)
        self.embed()
        self.wait(20)

class sketch_getting_stuck(InteractiveScene):

    def construct(self):
        surface = ParametricSurface(param_surface_1, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
        surface_inner = ParametricSurface(param_surface_1, u_range=[-1.25, 1.25], v_range=[-1.25, 1.25], resolution=(128, 128))
        ts = TexturedSurface(surface, '/Users/stephen/manim/videos/loss_2d_1.png')
        ts.set_shading(0.0, 0.1, 0)
        tsi = TexturedSurface(surface_inner, '/Users/stephen/manim/videos/loss_2d_1_inner.png')
        tsi.set_shading(0.0, 0.1, 0)
        num_lines = 64
        num_points = 512
        u_gridlines = VGroup()
        v_gridlines = VGroup()
        u_values = np.linspace(-2.5, 2.5, num_lines)
        v_points = np.linspace(-2.5, 2.5, num_points)
        for u in u_values:
            points = [param_surface_1(u, v) for v in v_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.15)
            u_gridlines.add(line)
        u_points = np.linspace(-2.5, 2.5, num_points)
        for v in u_values:
            points = [param_surface_1(u, v) for u in u_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.15)
            v_gridlines.add(line)
        self.wait()
        self.frame.reorient(32, 38, 0, (0.12, -0.18, -0.23), 7.45)
        self.play(ShowCreation(u_gridlines), ShowCreation(v_gridlines), self.frame.animate.reorient(161, 33, 0, (0.11, -0.12, -0.23), 4.84), run_time=10)
        self.wait()
        self.add(ts)
        starting_coords = [0.05, -0.9]
        starting_point = param_surface_1(*starting_coords)
        s1 = Dot3D(center=starting_point, radius=0.06, color='$FF00FF')
        self.add(s1)
        num_steps = 200
        learning_rate = 0.002
        trajectory = [[starting_point[0], starting_point[1], param_surface_1(starting_point[0], starting_point[1])[2]]]
        for i in range(num_steps):
            g = get_numerical_gradient(param_surface_1, trajectory[-1][0], trajectory[-1][1], epsilon=0.01)
            delta = learning_rate * np.array(g)
            new_x = trajectory[-1][0] - delta[0]
            new_y = trajectory[-1][1] - delta[1]
            trajectory.append([new_x, new_y, param_surface_1(new_x, new_y)[2]])
        ending_coords = [0, 0]
        ending_point = param_surface_1(*ending_coords)
        s2 = Dot3D(center=ending_point, radius=0.06, color='$FF00FF')
        self.add(s2)
        num_steps2 = 90
        learning_rate_2 = 0.005
        for i in range(num_steps2):
            g = -np.array([ending_coords[0] - trajectory[-1][0], ending_coords[1] - trajectory[-1][1]])
            delta = learning_rate_2 * np.array(g)
            new_x = trajectory[-1][0] - delta[0]
            new_y = trajectory[-1][1] - delta[1]
            trajectory.append([new_x, new_y, param_surface_1(new_x, new_y)[2]])
        num_steps3 = 512
        trajectory_waypoint = trajectory[-1]
        g = np.array([ending_coords[0] - trajectory[-1][0], ending_coords[1] - trajectory[-1][1]])
        for i in range(num_steps3):
            new_x = trajectory_waypoint[0] + i / num_steps3 * g[0]
            new_y = trajectory_waypoint[1] + i / num_steps3 * g[1]
            trajectory.append([new_x, new_y, param_surface_1(new_x, new_y)[2]])
        trajectory = np.array(trajectory)
        dot_path = Group()
        for t in trajectory:
            dot_path.add(Dot3D(center=t, radius=0.017, color='$FF00FF'))
        self.add(dot_path)
        self.add(u_gridlines, v_gridlines)
        self.embed()
        self.wait(20)

class sketch_local_minima(InteractiveScene):

    def construct(self):
        surface = ParametricSurface(param_surface_1, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
        ts = TexturedSurface(surface, '/Users/stephen/manim/videos/loss_2d_1.png')
        ts.set_shading(0.0, 0.1, 0)
        self.add(ts)
        minima = find_local_minima(loss_2d_1)
        minima = np.array(minima)
        minima = minima / 512.0 * 5.0 - 2.5
        minima_dots = Group()
        minima_to_show = 8
        for i in np.random.choice(range(len(minima)), minima_to_show):
            minima_dots.add(Dot3D(center=[minima[i][1], minima[i][0], param_surface_1(minima[i][1], minima[i][0])[2]], radius=0.04, color='$FF00FF'))
        self.add(minima_dots)

class sketch_wormole(InteractiveScene):

    def construct(self):
        loss_arrays = []
        num_time_steps = 3
        for i in range(num_time_steps):
            loss_arrays.append(np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_25_1/' + str(i).zfill(3) + '.npy'))
        surfaces = Group()
        for i in range(num_time_steps):
            surf_func = partial(param_surface_2, surf_array=loss_arrays[i])
            surface = ParametricSurface(surf_func, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
            ts = TexturedSurface(surface, '/Users/stephen/manim/videos/' + 'loss_2d_1_' + str(i).zfill(3) + '.png')
            ts.set_shading(0.0, 0.1, 0)
            surfaces.add(ts)
        self.add(surfaces[0])
        self.frame.reorient(155, 35, 0, (-0.06, -0.74, 0.16), 2.66)
        num_total_steps = 16
        start_orientation = [142, 34, 0, (-0.09, -0.77, 0.15), 3.55]
        end_orientation = [131, 31, 0, (-0.12, -0.88, 0.22), 2.9]
        interp_orientations = manual_camera_interpolation(start_orientation, end_orientation, num_steps=num_total_steps)
        self.frame.reorient(*start_orientation)
        surface_update_counter = 1
        frames_per_surface_upddate = np.floor(num_total_steps / num_time_steps)
        for i in range(1, num_total_steps):
            if i % frames_per_surface_upddate == 0 and surface_update_counter < len(surfaces):
                self.remove(surfaces[surface_update_counter - 1])
                self.add(surfaces[surface_update_counter])
                surface_update_counter += 1
            self.frame.reorient(*interp_orientations[i])
            self.wait(0.1)
        self.wait()
        self.embed()