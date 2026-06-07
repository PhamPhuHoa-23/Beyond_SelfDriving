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
from torch.utils.data import Dataset
from functools import partial

def get_color_wheel_colors(n_colors, saturation=1.0, value=1.0, start_hue=0.0):
    import colorsys
    colors = []
    for i in range(n_colors):
        hue = (start_hue + i / n_colors) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        colors.append(hex_color)
    return colors

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

    def set_opacity_range(self, min_opacity, max_opacity):
        self.min_opacity = min_opacity
        self.max_opacity = max_opacity
        self.apply_radial_opacity()
        return self

    def set_max_radius(self, max_radius):
        self.max_radius = max_radius
        self.apply_radial_opacity()
        return self

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

class MultiClassSwissroll(Dataset):

    def __init__(self, tmin, tmax, N, num_classes=10, center=(0, 0), scale=1.0):
        self.num_classes = num_classes
        t = tmin + torch.linspace(0, 1, N) * tmax
        center = torch.tensor(center).unsqueeze(0)
        spiral_points = center + scale * torch.stack([t * torch.cos(t) / tmax, t * torch.sin(t) / tmax]).T
        class_boundaries = torch.linspace(tmin, tmax, num_classes + 1)
        classes = torch.zeros(N, dtype=torch.long)
        for i in range(N):
            t_val = t[i]
            class_idx = min(int((t_val - tmin) / (tmax - tmin) * num_classes), num_classes - 1)
            classes[i] = class_idx
        self.data = [(spiral_points[i], classes[i].item()) for i in range(N)]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def get_class_colors(self):
        import matplotlib.colors as mcolors
        hues = np.linspace(0, 1, self.num_classes, endpoint=False)
        colors = []
        for hue in hues:
            rgb = mcolors.hsv_to_rgb([hue, 1.0, 1.0])
            colors.append(rgb)
        return colors

class p78_slower_fade_in(InteractiveScene):

    def construct(self):
        batch_size = 2130
        dataset = Swissroll(np.pi / 2, 5 * np.pi, 100)
        loader = DataLoader(dataset, batch_size=batch_size)
        batch = next(iter(loader)).numpy()
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': False, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
        self.add(axes)
        dots = VGroup()
        for point in batch:
            screen_point = axes.c2p(point[0], point[1])
            dot = Dot(screen_point, radius=0.04)
            dots.add(dot)
        dots.set_color(YELLOW)
        self.wait()
        self.play(FadeIn(dots, lag_ratio=0.1), run_time=20)
        self.wait(20)
        self.embed()

class thumbnail_hackin_1(InteractiveScene):

    def construct(self):
        dataset = MultiClassSwissroll(np.pi / 2, 5 * np.pi, 100, num_classes=3)
        colors = dataset.get_class_colors()
        loader = DataLoader(dataset, batch_size=len(dataset) * 2, shuffle=True)
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': False, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
        axes.set_opacity(0.8)
        extended_axes = Axes(x_range=[-2.0, 2.0, 0.5], y_range=[-2.0, 2.0, 0.5], height=7 * (4.0 / 2.4), width=7 * (4.0 / 2.4), axis_config={'stroke_width': 0})
        extended_axes.move_to(axes.get_center())
        dots = VGroup()
        labels_array = []
        for point in dataset.data:
            screen_point = axes.c2p(point[0][0], point[0][1])
            dot = Dot(screen_point, radius=0.04)
            dots.add(dot)
            labels_array.append(point[1])
        labels_array = np.array(labels_array)
        dots.set_color(YELLOW)
        dots.set_opacity(0.5)
        i = 75
        dot_to_move = dots[i].copy()
        dot_to_move.set_opacity(1.0)
        traced_path = CustomTracedPath(dot_to_move.get_center, stroke_color=YELLOW, stroke_width=2.0, opacity_range=(0.25, 0.9), fade_length=15)
        traced_path.set_fill(opacity=0)
        np.random.seed(485)
        random_walk = 0.07 * np.random.randn(100, 2)
        random_walk[0] = np.array([0.2, 0.12])
        random_walk[-1] = np.array([0.19, -0.05])
        random_walk = np.cumsum(random_walk, axis=0)
        random_walk = np.hstack((random_walk, np.zeros((len(random_walk), 1))))
        random_walk_shifted = random_walk + np.array([dataset.data[i][0][0], dataset.data[i][0][1], 0])
        dot_history = VGroup()
        dot_history.add(dot_to_move.copy().scale(0.4).set_color(YELLOW))
        traced_path.update_path(0.1)
        dots[i].set_opacity(0.0)
        start_orientation = [0, 0, 0, (0.0, 0.0, 0.0), 8.0]
        end_orientation = [0, 0, 0, (3.48, 1.88, 0.0), 4.26]
        interp_orientations = manual_camera_interpolation(start_orientation, end_orientation, 100)
        x100 = Tex('x_{100}', font_size=24).set_color(WHITE)
        x100.next_to(dot_to_move, 0.07 * UP + 0.001 * RIGHT)
        pre_point_coords = dot_to_move.get_center() - np.array([0.76, 0.25, 0])
        a2 = Arrow(dot_to_move.get_center(), pre_point_coords, thickness=2.0, tip_width_ratio=5, buff=0.035)
        a2.set_color(WHITE)
        eq_2 = Tex('f(x_{100}, t)', font_size=24)
        eq_2.set_color(WHITE)
        eq_2.move_to([5.3, 2.7, 0])
        eq_3 = Tex('f(x_{100}, t, cat)', font_size=24)
        eq_3.set_color(WHITE)
        eq_3[-4:-1].set_color(YELLOW)
        eq_3.move_to(eq_2, aligned_edge=LEFT)
        xt_history = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/conditioned_history_3.npy')
        heatmaps = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/conditioned_heatmaps_3.npy')
        num_dots_per_class = 96
        colors_by_class = {2: YELLOW, 0: '#00FFFF', 1: '#FF00FF'}
        all_traced_paths = VGroup()
        all_dots_to_move = VGroup()
        for class_index in range(xt_history.shape[0]):
            for path_index in range(num_dots_per_class):
                dot_to_move_2 = Dot(axes.c2p(*np.concatenate((xt_history[class_index, 0, path_index, :], [0]))), radius=0.06)
                dot_to_move_2.set_color(colors_by_class[class_index])
                all_dots_to_move.add(dot_to_move_2)
                traced_path_2 = CustomTracedPath(dot_to_move_2.get_center, stroke_color=colors_by_class[class_index], stroke_width=2.0, opacity_range=(0.0, 1.0), fade_length=12)
                all_traced_paths.add(traced_path_2)
        cat_dots = VGroup()
        for i, d in enumerate(dots):
            if labels_array[i] == 2:
                cat_dots.add(d)
        xt_history = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/conditioned_history_5.npy')
        heatmaps = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/conditioned_heatmaps_5.npy')
        heatmaps_u = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/conditioned_heatmaps_5u.npy')
        heatmaps_c = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/conditioned_heatmaps_5c.npy')
        model = torch.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/jun_27_1.pt', map_location=torch.device('cpu'))
        bound = 2.0
        num_heatmap_steps = 64
        grid = []
        for i, x in enumerate(np.linspace(-bound, bound, num_heatmap_steps)):
            for j, y in enumerate(np.linspace(-bound, bound, num_heatmap_steps)):
                grid.append([x, y])
        grid = torch.tensor(grid).float()
        time_tracker = ValueTracker(0.0)
        schedule = ScheduleLogLinear(N=256, sigma_min=0.01, sigma_max=10)
        sigmas = schedule.sample_sigmas(256)

        def vector_function_heatmap(coords_array):
            result = np.zeros((len(coords_array), 2))
            for i, coord in enumerate(coords_array):
                x, y = (coord[0], coord[1])
                current_time = time_tracker.get_value()
                max_time = 8.0
                sigma_idx = int(np.clip(current_time * 255 / max_time, 0, 255))
                distances = np.linalg.norm(grid.numpy() - np.array([x, y]), axis=1)
                closest_idx = np.argmin(distances)
                vector = heatmaps_c[0, sigma_idx, closest_idx, :]
                result[i] = vector
            return -result

        def vector_function_heatmap_u(coords_array):
            result = np.zeros((len(coords_array), 2))
            for i, coord in enumerate(coords_array):
                x, y = (coord[0], coord[1])
                current_time = time_tracker.get_value()
                max_time = 8.0
                sigma_idx = int(np.clip(current_time * 255 / max_time, 0, 255))
                distances = np.linalg.norm(grid.numpy() - np.array([x, y]), axis=1)
                closest_idx = np.argmin(distances)
                vector = heatmaps_u[0, sigma_idx, closest_idx, :]
                result[i] = vector
            return -result
        vector_field = TrackerControlledVectorField(time_tracker=time_tracker, func=vector_function_heatmap, coordinate_system=extended_axes, density=3.0, stroke_width=3.5, max_radius=4.5, min_opacity=0.1, max_opacity=1.0, tip_width_ratio=4, tip_len_to_width=0.01, max_vect_len_to_step_size=0.7, color=YELLOW)
        vector_field_u = TrackerControlledVectorField(time_tracker=time_tracker, func=vector_function_heatmap_u, coordinate_system=extended_axes, density=3.0, stroke_width=3.5, max_radius=4.5, min_opacity=0.1, max_opacity=0.7, tip_width_ratio=4, tip_len_to_width=0.01, max_vect_len_to_step_size=0.7, color='#AAAAAA')
        self.frame.reorient(0, 0, 0, (0, 0, 0), 8)
        self.add(vector_field_u)
        self.add(vector_field)
        dots.set_color(CHILL_BROWN)
        dots.set_opacity(0.5)
        self.remove(dots)
        self.add(cat_dots)
        cat_dots.set_color(WHITE)
        cat_dots.set_opacity(1.0)
        time_tracker.set_value(4.08)
        self.wait()
        self.wait()