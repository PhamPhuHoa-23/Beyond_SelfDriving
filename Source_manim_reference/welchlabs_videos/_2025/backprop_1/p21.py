from manimlib import *
from functools import partial
import sys
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
sys.path.append('/Users/stephen/manim/videos/_2025/backprop_1')
from backprop_data import xs1, losses1, all_probs_1
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'

def get_x_axis(t, intial_bounds, final_bounds, position=None):
    lower_bound, upper_bound = time_to_bounds(t, intial_bounds, final_bounds)
    x_ticks, x_axis_min, x_axis_max = generate_nice_ticks(lower_bound, 0.95 * upper_bound, min_ticks=3, max_ticks=16, ignore=[])
    x_axis = WelchXAxis(x_min=lower_bound, x_max=upper_bound, x_ticks=x_ticks, x_tick_height=0.15, x_label_font_size=24, stroke_width=3, arrow_tip_scale=0.1, axis_length_on_canvas=7)
    if position is not None:
        x_axis.move_to(position)
    return x_axis

def get_y_axis(t, intial_bounds, final_bounds, position=None):
    lower_bound_x, upper_bound_x = time_to_bounds(t, intial_bounds, final_bounds)
    indices_in_range = np.logical_and(xs1 > lower_bound_x, xs1 < upper_bound_x)
    y_to_viz = all_probs_1[indices_in_range]
    upper_bound = 1.01 * np.max(y_to_viz)
    lower_bound = 0.99 * np.min(y_to_viz)
    y_ticks, x_axis_min, x_axis_max = generate_nice_ticks(lower_bound, upper_bound, min_ticks=3, max_ticks=16, ignore=[])
    y_axis = WelchYAxis(y_min=lower_bound, y_max=upper_bound, y_ticks=y_ticks, y_tick_width=0.15, y_label_font_size=24, stroke_width=3, arrow_tip_scale=0.1, axis_length_on_canvas=5)
    if position is not None:
        y_axis.move_to(position)
    return y_axis

def get_fixed_y_axis(t, intial_bounds, final_bounds, position=None, y_zoom_t=0.0):
    lower_bound_x, upper_bound_x = time_to_bounds(t, intial_bounds, final_bounds)
    indices_in_range = np.logical_and(xs1 > lower_bound_x, xs1 < upper_bound_x)
    y_to_viz = all_probs_1[indices_in_range]
    current_upper_bound = 1.01 * np.max(y_to_viz)
    current_lower_bound = 0.99 * np.min(y_to_viz)
    fixed_lower_bound = 0.15
    fixed_upper_bound = 1.6
    lower_bound = y_zoom_t * fixed_lower_bound + (1 - y_zoom_t) * current_lower_bound
    upper_bound = y_zoom_t * fixed_upper_bound + (1 - y_zoom_t) * current_upper_bound
    y_ticks, x_axis_min, x_axis_max = generate_nice_ticks(lower_bound, upper_bound, min_ticks=3, max_ticks=16, ignore=[])
    y_axis = WelchYAxis(y_min=lower_bound, y_max=upper_bound, y_ticks=y_ticks, y_tick_width=0.15, y_label_font_size=24, stroke_width=3, arrow_tip_scale=0.1, axis_length_on_canvas=5)
    if position is not None:
        y_axis.move_to(position)
    return y_axis

def get_scatter_points(t, initial_bounds, final_bounds, x_axis_position, y_axis_position):
    lower_bound_x, upper_bound_x = time_to_bounds(t, initial_bounds, final_bounds)
    indices_in_range = np.logical_and(xs1 > lower_bound_x, xs1 < upper_bound_x)
    x_values = xs1[indices_in_range]
    y_values = all_probs_1[indices_in_range]
    if len(y_values) > 0:
        y_min = 0.99 * np.min(y_values)
        y_max = 1.01 * np.max(y_values)
    else:
        y_min = 0
        y_max = 1
    x_axis_length = 7
    y_axis_length = 5
    x_scale = (upper_bound_x - lower_bound_x) / x_axis_length
    y_scale = (y_max - y_min) / y_axis_length
    origin_x = x_axis_position[0] - x_axis_length / 2
    origin_y = y_axis_position[1] - y_axis_length / 2
    dots = VGroup()
    for x_val, y_val in zip(x_values, y_values):
        x_norm = (x_val - lower_bound_x) / (upper_bound_x - lower_bound_x)
        y_norm = (y_val - y_min) / (y_max - y_min)
        x_pos = origin_x + x_norm * x_axis_length
        y_pos = origin_y + y_norm * y_axis_length
        dot = Dot(point=[x_pos, y_pos, 0], radius=0.05, stroke_width=0, fill_opacity=0.8)
        dot.set_color(YELLOW)
        dots.add(dot)
    return dots

def get_scatter_points_with_interpolated_y(t, initial_bounds, final_bounds, x_axis_position, y_axis_position, y_zoom_t=0.0):
    lower_bound_x, upper_bound_x = time_to_bounds(t, initial_bounds, final_bounds)
    indices_in_range = np.logical_and(xs1 > lower_bound_x, xs1 < upper_bound_x)
    x_values = xs1[indices_in_range]
    y_values = all_probs_1[indices_in_range]
    if len(y_values) > 0:
        current_y_min = 0.99 * np.min(y_values)
        current_y_max = 1.01 * np.max(y_values)
    else:
        current_y_min = 0
        current_y_max = 1
    fixed_y_min = 0.15
    fixed_y_max = 1.6
    y_min = y_zoom_t * fixed_y_min + (1 - y_zoom_t) * current_y_min
    y_max = y_zoom_t * fixed_y_max + (1 - y_zoom_t) * current_y_max
    x_axis_length = 7
    y_axis_length = 5
    x_scale = (upper_bound_x - lower_bound_x) / x_axis_length
    y_scale = (y_max - y_min) / y_axis_length
    origin_x = x_axis_position[0] - x_axis_length / 2
    origin_y = y_axis_position[1] - y_axis_length / 2
    dots = VGroup()
    for x_val, y_val in zip(x_values, y_values):
        x_norm = (x_val - lower_bound_x) / (upper_bound_x - lower_bound_x)
        y_norm = (y_val - y_min) / (y_max - y_min)
        x_pos = origin_x + x_norm * x_axis_length
        y_pos = origin_y + y_norm * y_axis_length
        dot = Dot(point=[x_pos, y_pos, 0], radius=0.05, stroke_width=0, fill_opacity=0.8)
        dot.set_color(YELLOW)
        dots.add(dot)
    return dots

def time_to_bounds(t, intial_bounds, final_bounds):
    lower_bound = t * (final_bounds[0] - intial_bounds[0]) + intial_bounds[0]
    upper_bound = t * (final_bounds[1] - intial_bounds[1]) + intial_bounds[1]
    return (lower_bound, upper_bound)

class P21(InteractiveScene):

    def construct(self):
        initial_x_range = [-0.027, 0.013]
        final_x_range = [-1.1, 4.1]
        initial_y_range = [0.3887, 0.394]
        final_y_range = [0.15, 0.6]
        initial_time = 0.0
        t_tracker = ValueTracker(initial_time)
        y_zoom_tracker = ValueTracker(0.0)
        x_axis_position = [0, -2, 0]
        y_axis_position = [-3.84, 0.73, 0]
        x_axis = always_redraw(lambda: get_x_axis(t_tracker.get_value(), initial_x_range, final_x_range, x_axis_position))
        y_axis = always_redraw(lambda: get_y_axis(t_tracker.get_value(), initial_x_range, final_x_range, y_axis_position))
        fixed_y_axis = always_redraw(lambda: get_fixed_y_axis(t_tracker.get_value(), initial_x_range, final_x_range, y_axis_position, y_zoom_tracker.get_value()))
        scatter = always_redraw(lambda: get_scatter_points(t_tracker.get_value(), initial_x_range, final_x_range, x_axis_position, y_axis_position))
        interpolated_scatter = always_redraw(lambda: get_scatter_points_with_interpolated_y(t_tracker.get_value(), initial_x_range, final_x_range, x_axis_position, y_axis_position, y_zoom_tracker.get_value()))
        self.add(x_axis, y_axis, scatter)
        self.wait()
        self.play(t_tracker.animate.set_value(1.0), run_time=4)
        self.wait()
        self.remove(y_axis, scatter)
        self.add(fixed_y_axis, interpolated_scatter)
        self.play(y_zoom_tracker.animate.set_value(1.0), run_time=3)
        self.wait()

class AxisHacking(InteractiveScene):

    def construct(self):
        x_axis = WelchXAxis(x_ticks=[1, 2, 3, 4, 5], x_tick_height=0.15, x_label_font_size=24, stroke_width=3, arrow_tip_scale=0.1)
        y_axis = WelchYAxis(y_ticks=[1, 2, 3, 4, 5], y_tick_width=0.15, y_label_font_size=24, stroke_width=3, arrow_tip_scale=0.1)
        self.add(x_axis, y_axis)