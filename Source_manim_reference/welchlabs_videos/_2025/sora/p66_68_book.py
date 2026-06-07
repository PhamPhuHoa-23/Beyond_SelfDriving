from manimlib import *
import glob
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#00a14b'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
from torch.utils.data import DataLoader
from smalldiffusion import ScheduleLogLinear, samples, Swissroll, ModelMixin, ScheduleDDPM
from typing import Callable
from tqdm import tqdm
import torch
from itertools import pairwise

def get_color_wheel_colors(n_colors, saturation=1.0, value=1.0, start_hue=0.0):
    import colorsys
    colors = []
    for i in range(n_colors):
        hue = (start_hue + i / n_colors) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        colors.append(hex_color)
    return colors

class CustomTracedPath(VMobject):

    def __init__(self, traced_point_func, stroke_width=2.0, stroke_color=YELLOW, opacity_range=(0.1, 0.8), fade_length=20, **kwargs):
        super().__init__(**kwargs)
        self.traced_point_func = traced_point_func
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.opacity_range = opacity_range
        self.fade_length = fade_length
        self.segments = VGroup()
        self.traced_points = []
        self.is_tracing = True
        self.add_updater(lambda m, dt: m.update_path(dt))

    def update_path(self, dt=0):
        if not self.is_tracing or dt == 0:
            return
        point = self.traced_point_func()
        self.traced_points.append(point.copy())
        if len(self.traced_points) >= 2:
            segment = Line(self.traced_points[-2], self.traced_points[-1], stroke_width=self.stroke_width, stroke_color=self.stroke_color)
            self.segments.add(segment)
            self.update_segment_opacities()
            self.add(segment)

    def update_segment_opacities(self):
        n_segments = len(self.segments)
        if n_segments == 0:
            return
        min_op, max_op = self.opacity_range
        for i, segment in enumerate(self.segments):
            if i >= n_segments - self.fade_length:
                fade_progress = (i - (n_segments - self.fade_length)) / self.fade_length
                opacity = min_op + (max_op - min_op) * fade_progress
            else:
                opacity = min_op
            segment.set_opacity(opacity)

    def remove_last_segment(self):
        if len(self.segments) > 0:
            last_segment = self.segments[-1]
            self.segments.remove(last_segment)
            self.remove(last_segment)
            if len(self.traced_points) > 0:
                self.traced_points.pop()
        if len(self.segments) > 0:
            last_segment = self.segments[-1]
            self.segments.remove(last_segment)
            self.remove(last_segment)
            if len(self.traced_points) > 0:
                self.traced_points.pop()
        self.update_segment_opacities()

    def stop_tracing(self):
        self.is_tracing = False

    def start_tracing(self):
        self.is_tracing = True

    def get_num_segments(self):
        return len(self.segments)

class TrackerControlledVectorField(VectorField):

    def __init__(self, time_tracker, max_radius=2.0, min_opacity=0.1, max_opacity=0.7, **kwargs):
        self.time_tracker = time_tracker
        self.max_radius = max_radius
        self.min_opacity = min_opacity
        self.max_opacity = max_opacity
        super().__init__(**kwargs)
        self.add_updater(self.update_from_tracker)

    def update_from_tracker(self, mob, dt):
        current_time = self.time_tracker.get_value()
        if not hasattr(self, '_last_time') or abs(current_time - self._last_time) > 0.01:
            self._last_time = current_time
            self.update_vectors()
            self.apply_radial_opacity()

    def apply_radial_opacity(self):
        opacities = self.get_stroke_opacities()
        n_vectors = len(self.sample_points)
        for i in range(n_vectors):
            base_point = self.sample_points[i]
            distance = np.linalg.norm(base_point[:2])
            opacity_factor = max(0, 1 - distance / self.max_radius)
            final_opacity = self.min_opacity + (self.max_opacity - self.min_opacity) * opacity_factor
            start_idx = i * 8
            end_idx = min(start_idx + 8, len(opacities))
            opacities[start_idx:end_idx] = final_opacity
        self.note_changed_data()

class p66v4(InteractiveScene):

    def construct(self):
        batch_size = 2130
        dataset = Swissroll(np.pi / 2, 5 * np.pi, 100)
        loader = DataLoader(dataset, batch_size=batch_size)
        batch = next(iter(loader)).numpy()
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': False, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
        axes.set_opacity(0.5)
        extended_axes = Axes(x_range=[-2.0, 2.0, 0.5], y_range=[-2.0, 2.0, 0.5], height=7 * (4.0 / 2.4), width=7 * (4.0 / 2.4), axis_config={'stroke_width': 0})
        extended_axes.move_to(axes.get_center())
        dots = VGroup()
        for point in batch:
            screen_point = axes.c2p(point[0], point[1])
            dot = Dot(screen_point, radius=0.05)
            dots.add(dot)
        dots.set_color(CHILL_BROWN)
        dots.set_opacity(0.5)
        xt_history = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/ddim_history_2.npy')
        heatmaps = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/ddim_heatmaps_2.npy')
        model = torch.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/jun_26_2.pt')
        time_tracker = ValueTracker(0.0)
        schedule = ScheduleLogLinear(N=256, sigma_min=0.01, sigma_max=1)
        sigmas = schedule.sample_sigmas(256)

        def vector_function_with_tracker(coords_array):
            current_time = time_tracker.get_value()
            max_time = 8.0
            sigma_idx = int(np.clip(current_time * 255 / max_time, 0, 255))
            try:
                res = model.forward(torch.tensor(coords_array).float(), sigmas[sigma_idx], cond=None)
                return -res.detach().numpy()
            except:
                return np.zeros((len(coords_array), 2))
        vector_field = TrackerControlledVectorField(time_tracker=time_tracker, func=vector_function_with_tracker, coordinate_system=extended_axes, density=5.0, stroke_width=2.0, max_radius=6.0, min_opacity=0.5, max_opacity=0.5, tip_width_ratio=4, tip_len_to_width=0.01, max_vect_len_to_step_size=0.7, color=CHILL_BROWN)
        self.frame.reorient(0, 0, 0, (0.0, 0.0, 0.0), 10)
        self.add(axes, dots)
        num_dots = 256
        colors = get_color_wheel_colors(num_dots)
        all_traced_paths = VGroup()
        all_dots_to_move = VGroup()
        for path_index in range(num_dots):
            dot_to_move = Dot(axes.c2p(*np.concatenate((xt_history[0, path_index, :], [0]))), radius=0.06)
            dot_to_move.set_color(colors[path_index])
            all_dots_to_move.add(dot_to_move)
            traced_path = CustomTracedPath(dot_to_move.get_center, stroke_color=colors[path_index], stroke_width=2.0, opacity_range=(0.4, 0.4), fade_length=64)
            all_traced_paths.add(traced_path)
        self.add(all_traced_paths)
        self.add(all_dots_to_move)
        self.wait()
        for k in range(xt_history.shape[0]):
            self.play(time_tracker.animate.set_value(8.0 * (k / 256.0)), *[all_dots_to_move[path_index].animate.move_to(axes.c2p(*[xt_history[k, path_index, 0], xt_history[k, path_index, 1]])) for path_index in range(len(all_dots_to_move))], rate_func=linear, run_time=0.1)
        self.wait()
        self.wait()
        self.remove(all_traced_paths)
        self.wait()
        self.add(all_traced_paths)
        self.frame.reorient(0, 0, 0, (-0.23, 0.03, 0.0), 7.34)
        self.wait()
        self.remove(axes)
        self.frame.reorient(0, 0, 0, (-0.39, -0.12, 0.0), 7.81)
        self.wait()
        self.frame.reorient(0, 0, 0, (-0.26, -0.33, 0.0), 6.4)
        self.wait()
        self.remove(all_traced_paths)
        self.wait()
        self.wait(20)
        self.embed()