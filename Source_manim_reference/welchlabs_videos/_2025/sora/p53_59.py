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

class p57_58v4(InteractiveScene):

    def construct(self):
        batch_size = 2130
        dataset = Swissroll(np.pi / 2, 5 * np.pi, 100)
        loader = DataLoader(dataset, batch_size=batch_size)
        batch = next(iter(loader)).numpy()
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': False, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
        axes.set_opacity(0.8)
        extended_axes = Axes(x_range=[-2.0, 2.0, 0.5], y_range=[-2.0, 2.0, 0.5], height=7 * (4.0 / 2.4), width=7 * (4.0 / 2.4), axis_config={'stroke_width': 0})
        extended_axes.move_to(axes.get_center())
        dots = VGroup()
        for point in batch:
            screen_point = axes.c2p(point[0], point[1])
            dot = Dot(screen_point, radius=0.04)
            dots.add(dot)
        dots.set_color(YELLOW)
        dots.set_opacity(0.3)
        i = 75
        dot_to_move = dots[i].copy()
        traced_path = CustomTracedPath(dot_to_move.get_center, stroke_color=YELLOW, stroke_width=2.0, opacity_range=(0.25, 0.9), fade_length=15)
        traced_path.set_fill(opacity=0)
        np.random.seed(485)
        random_walk = 0.07 * np.random.randn(100, 2)
        random_walk[0] = np.array([0.2, 0.12])
        random_walk[-1] = np.array([0.19, -0.05])
        random_walk = np.cumsum(random_walk, axis=0)
        random_walk = np.hstack((random_walk, np.zeros((len(random_walk), 1))))
        random_walk_shifted = random_walk + np.array([batch[i][0], batch[i][1], 0])
        dot_history = VGroup()
        dot_history.add(dot_to_move.copy().scale(0.4).set_color(YELLOW))
        traced_path.update_path(0.1)
        model = torch.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/jun_24_1.pt')
        schedule = ScheduleLogLinear(N=64, sigma_min=0.01, sigma_max=1)
        bound = 2.0
        num_heatmap_steps = 30
        grid = []
        for i, x in enumerate(np.linspace(-bound, bound, num_heatmap_steps)):
            for j, y in enumerate(np.linspace(-bound, bound, num_heatmap_steps)):
                grid.append([x, y])
        grid = torch.tensor(grid).float()
        gam = 1
        mu = 0.5
        cfg_scale = 0.0
        cond = None
        sigmas = schedule.sample_sigmas(64)
        xt_history = []
        history_pre_noise = []
        heatmaps = []
        eps = None
        torch.manual_seed(2)
        with torch.no_grad():
            model.eval()
            xt = torch.randn((batch_size,) + model.input_dims) * sigmas[0]
            xt[0, 0] = random_walk_shifted[-1][0]
            xt[0, 1] = random_walk_shifted[-1][1]
            xt_history.append(xt.numpy())
            for i, (sig, sig_prev) in enumerate(pairwise(sigmas)):
                eps_prev, eps = (eps, model.predict_eps_cfg(xt, sig.to(xt), cond, cfg_scale))
                sig_p = (sig_prev / sig ** mu) ** (1 / (1 - mu))
                eta = (sig_prev ** 2 - sig_p ** 2).sqrt()
                history_pre_noise.append(xt - (sig - sig_p) * eps)
                xt = xt - (sig - sig_p) * eps + eta * model.rand_input(xt.shape[0]).to(xt)
                xt_history.append(xt.numpy())
                heatmaps.append(model.forward(grid, sig, cond=None))
        xt_history = np.array(xt_history)
        history_pre_noise = np.array(history_pre_noise)
        time_tracker = ValueTracker(0.0)

        def vector_function_with_tracker(coords_array):
            current_time = time_tracker.get_value()
            max_time = 8.0
            sigma_idx = int(np.clip(current_time * 63 / max_time, 0, 63))
            try:
                res = model.forward(torch.tensor(coords_array).float(), sigmas[sigma_idx], cond=None)
                return -res.detach().numpy()
            except:
                return np.zeros((len(coords_array), 2))
        vector_field = TrackerControlledVectorField(time_tracker=time_tracker, func=vector_function_with_tracker, coordinate_system=extended_axes, density=3.0, stroke_width=2, max_radius=6.0, min_opacity=0.15, max_opacity=1.0, tip_width_ratio=4, tip_len_to_width=0.01, max_vect_len_to_step_size=0.7, color=WHITE)
        self.wait()
        self.frame.reorient(0, 0, 0, (0.0, 0.0, 0.0), 8.25)
        self.add(axes, dots)
        self.wait()
        self.play(FadeIn(vector_field))
        self.wait()
        path_index = 0
        dot_to_move_2 = Dot(axes.c2p(*np.concatenate((xt_history[0, path_index, :], [0]))), radius=0.06)
        dot_to_move_2.set_color(WHITE)
        path_segments = VGroup()
        for k in range(64):
            segment1 = Line(axes.c2p(*[xt_history[k, path_index, 0], xt_history[k, path_index, 1]]), axes.c2p(*[history_pre_noise[k, path_index, 0], history_pre_noise[k, path_index, 1]]), stroke_width=4.0, stroke_color=YELLOW)
            segment2 = Line(axes.c2p(*[history_pre_noise[k, path_index, 0], history_pre_noise[k, path_index, 1]]), axes.c2p(*[xt_history[k + 1, path_index, 0], xt_history[k + 1, path_index, 1]]), stroke_width=4.0, stroke_color=WHITE)
            segment2.set_opacity(0.4)
            segment1.set_opacity(0.9)
            path_segments.add(segment1)
            path_segments.add(segment2)
        self.add(path_segments)
        path_segments.set_opacity(0.0)
        self.wait()
        self.play(FadeOut(vector_field))
        dot_to_move.set_opacity(1.0)
        self.add(dot_to_move, traced_path)
        start_orientation = [0, 0, 0, (0.0, 0.0, 0.0), 8.25]
        end_orientation = [0, 0, 0, (3.48, 1.88, 0.0), 4.26]
        interp_orientations = manual_camera_interpolation(start_orientation, end_orientation, 100)
        self.wait()
        for j in range(100):
            dot_history.add(dot_to_move.copy().scale(0.4).set_color(YELLOW))
            dot_to_move.move_to(axes.c2p(*random_walk_shifted[j]))
            traced_path.update_path(0.1)
            self.frame.reorient(*interp_orientations[j])
            self.wait(0.1)
        traced_path.stop_tracing()
        x100 = Tex('x_{100}', font_size=24).set_color(YELLOW)
        x100.next_to(dot_to_move, 0.07 * UP + 0.001 * RIGHT)
        x99 = Tex('x_{99}', font_size=24).set_color(CHILL_BROWN)
        x99.next_to(dot_history[-1], 0.1 * UP + 0.01 * RIGHT)
        dot99 = Dot(dot_history[-1].get_center(), radius=0.04)
        dot99.set_color(CHILL_BROWN)
        self.play(FadeIn(x100), FadeIn(x99), FadeIn(dot99))
        self.wait()
        a1 = Arrow(dot_history[-1].get_center(), dot_to_move.get_center(), thickness=2.0, tip_width_ratio=5, buff=0.03)
        a1.set_color(YELLOW)
        eq_1 = Tex('p(x_{100} | x_{99}) = \\mathcal{N} (0, \\sigma^2)', font_size=22)
        eq_1.set_color('#FFFFFF')
        eq_1[2:6].set_color(YELLOW)
        eq_1[7:10].set_color(CHILL_BROWN)
        eq_1.move_to([5.2, 3.65, 0])
        self.add(eq_1, a1)
        eq_2 = Tex('p(x_{99} | x_{100}) = \\mathcal{N} (\\mu, \\sigma^2)', font_size=22)
        eq_2.set_color('#FFFFFF')
        eq_2[2:5].set_color(CHILL_BROWN)
        eq_2[6:10].set_color(YELLOW)
        eq_2[14].set_color('#00FFFF')
        eq_2.move_to([5.2, 2.3, 0])
        pre_point_coords = dot_to_move.get_center() - np.array([0.6, 0.18, 0])
        a2 = Arrow(dot_to_move.get_center(), pre_point_coords, thickness=2.0, tip_width_ratio=5, buff=0.035)
        a2.set_color('#00FFFF')
        self.wait()
        self.play(ReplacementTransform(a1, a2), traced_path.animate.set_color(CHILL_BROWN).set_opacity(0.2), x99.animate.set_opacity(0.5), dot99.animate.set_opacity(0.25))
        self.wait()
        self.play(ReplacementTransform(eq_1[:2].copy(), eq_2[:2]), ReplacementTransform(eq_1[2:6].copy(), eq_2[6:10]), ReplacementTransform(eq_1[7:10].copy(), eq_2[2:5]), ReplacementTransform(eq_1[6].copy(), eq_2[5]), ReplacementTransform(eq_1[10:].copy(), eq_2[10:]), run_time=4)
        dot2 = Dot(pre_point_coords, radius=0.04)
        dot2.set_color('#00FFFF')
        a3 = Arrow(pre_point_coords, pre_point_coords + np.array([-0.7, 0.24, 0]), thickness=2.0, tip_width_ratio=5, buff=0.035)
        a3.set_color('#777777')
        self.wait()
        self.play(FadeOut(traced_path), FadeOut(x99), FadeOut(dot99))
        self.add(a3, dot2)
        self.wait()
        mu_label = eq_2[14].copy()
        self.play(mu_label.animate.move_to(a2.get_center() + 0.16 * DOWN + 0.05 * RIGHT), run_time=2.0)
        self.wait()
        eq_3 = Tex('\\mathcal{N} (0, \\sigma^2)', font_size=18)
        eq_3.set_color('#777777')
        eq_3.move_to(a3.get_center() + 0.22 * DOWN + 0.2 * LEFT)
        self.play(ReplacementTransform(eq_2[12:].copy(), eq_3), run_time=2.0)
        self.wait()
        self.play(FadeOut(eq_1), FadeOut(eq_1), FadeOut(eq_2), FadeOut(eq_3), FadeOut(a2), FadeOut(a3), FadeOut(dot2), FadeOut(dot_to_move), FadeOut(mu_label), FadeOut(x100))
        self.add(vector_field)
        self.play(time_tracker.animate.set_value(8.0), run_time=2.0)
        self.remove(vector_field)
        self.play(FadeIn(vector_field), self.frame.animate.reorient(0, 0, 0, (0.0, 0.0, 0.0), 8.0), run_time=4.0)
        self.wait()
        self.play(time_tracker.animate.set_value(0.0), run_time=8.0)
        self.wait()
        self.wait(20)
        self.embed()

class p53_56v4(InteractiveScene):

    def construct(self):
        batch_size = 2130
        dataset = Swissroll(np.pi / 2, 5 * np.pi, 100)
        loader = DataLoader(dataset, batch_size=batch_size)
        batch = next(iter(loader)).numpy()
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': False, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
        axes.set_opacity(0.8)
        extended_axes = Axes(x_range=[-2.0, 2.0, 0.5], y_range=[-2.0, 2.0, 0.5], height=7 * (4.0 / 2.4), width=7 * (4.0 / 2.4), axis_config={'stroke_width': 0})
        extended_axes.move_to(axes.get_center())
        dots = VGroup()
        for point in batch:
            screen_point = axes.c2p(point[0], point[1])
            dot = Dot(screen_point, radius=0.04)
            dots.add(dot)
        dots.set_color(YELLOW)
        dots.set_opacity(0.3)
        model = torch.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/jun_24_1.pt')
        schedule = ScheduleLogLinear(N=64, sigma_min=0.01, sigma_max=1)
        bound = 2.0
        num_heatmap_steps = 30
        grid = []
        for i, x in enumerate(np.linspace(-bound, bound, num_heatmap_steps)):
            for j, y in enumerate(np.linspace(-bound, bound, num_heatmap_steps)):
                grid.append([x, y])
        grid = torch.tensor(grid).float()
        gam = 1
        mu = 0.5
        cfg_scale = 0.0
        cond = None
        sigmas = schedule.sample_sigmas(64)
        xt_history = []
        history_pre_noise = []
        heatmaps = []
        eps = None
        torch.manual_seed(2)
        with torch.no_grad():
            model.eval()
            xt = torch.randn((batch_size,) + model.input_dims) * sigmas[0]
            xt_history.append(xt.numpy())
            for i, (sig, sig_prev) in enumerate(pairwise(sigmas)):
                eps_prev, eps = (eps, model.predict_eps_cfg(xt, sig.to(xt), cond, cfg_scale))
                sig_p = (sig_prev / sig ** mu) ** (1 / (1 - mu))
                eta = (sig_prev ** 2 - sig_p ** 2).sqrt()
                history_pre_noise.append(xt - (sig - sig_p) * eps)
                xt = xt - (sig - sig_p) * eps + eta * model.rand_input(xt.shape[0]).to(xt)
                xt_history.append(xt.numpy())
                heatmaps.append(model.forward(grid, sig, cond=None))
        xt_history = np.array(xt_history)
        history_pre_noise = np.array(history_pre_noise)
        time_tracker = ValueTracker(0.0)

        def vector_function_with_tracker(coords_array):
            current_time = time_tracker.get_value()
            max_time = 8.0
            sigma_idx = int(np.clip(current_time * 63 / max_time, 0, 63))
            try:
                res = model.forward(torch.tensor(coords_array).float(), sigmas[sigma_idx], cond=None)
                return -res.detach().numpy()
            except:
                return np.zeros((len(coords_array), 2))
        vector_field = TrackerControlledVectorField(time_tracker=time_tracker, func=vector_function_with_tracker, coordinate_system=extended_axes, density=3.0, stroke_width=2, max_radius=6.0, min_opacity=0.15, max_opacity=0.8, tip_width_ratio=4, tip_len_to_width=0.01, max_vect_len_to_step_size=0.7, color=CHILL_BROWN)
        path_index = 25
        dot_to_move = Dot(axes.c2p(*np.concatenate((xt_history[0, path_index, :], [0]))), radius=0.06)
        dot_to_move.set_color(WHITE)
        path_segments = VGroup()
        for k in range(64):
            segment1 = Line(axes.c2p(*[xt_history[k, path_index, 0], xt_history[k, path_index, 1]]), axes.c2p(*[history_pre_noise[k, path_index, 0], history_pre_noise[k, path_index, 1]]), stroke_width=4.0, stroke_color='#00FFFF')
            segment2 = Line(axes.c2p(*[history_pre_noise[k, path_index, 0], history_pre_noise[k, path_index, 1]]), axes.c2p(*[xt_history[k + 1, path_index, 0], xt_history[k + 1, path_index, 1]]), stroke_width=4.0, stroke_color=WHITE)
            segment2.set_opacity(0.4)
            segment1.set_opacity(0.9)
            path_segments.add(segment1)
            path_segments.add(segment2)
        self.add(path_segments)
        path_segments.set_opacity(0.0)
        self.frame.reorient(0, 0, 0, (0.0, 0.0, 0.0), 8.25)
        self.add(axes)
        self.wait()
        self.play(ShowCreation(dots), self.frame.animate.reorient(0, 0, 0, (0.0, 0.0, 0.0), 8.0), run_time=3.0)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-1.54, 2.65, 0.0), 6.16), run_time=3.0)
        self.add(dot_to_move)
        self.wait()
        a0 = Arrow(dot_to_move.get_center(), dot_to_move.get_center() + np.array([2.5, -3.2, 0]), thickness=3.5, tip_width_ratio=5)
        a0.set_color(YELLOW)
        self.play(FadeIn(a0))
        self.wait()
        self.play(FadeOut(a0))
        self.wait()
        dot_coords = Tex('(' + str(round(xt_history[0, path_index, 0], 1)) + ', ' + str(round(xt_history[0, path_index, 1], 1)) + ')', font_size=32)
        dot_coords.next_to(dot_to_move, DOWN, buff=0.15)
        self.play(Write(dot_coords))
        self.wait()
        self.play(FadeIn(vector_field))
        self.wait()
        self.remove(dot_coords)
        self.play(dot_to_move.animate.move_to(axes.c2p(*[history_pre_noise[0, path_index, 0], history_pre_noise[0, path_index, 1]])), ShowCreation(path_segments[0]), path_segments[0].animate.set_opacity(0.8), run_time=2.0)
        self.wait()
        self.play(dot_to_move.animate.move_to(axes.c2p(*[xt_history[1, path_index, 0], xt_history[1, path_index, 1]])), ShowCreation(path_segments[1]), path_segments[1].animate.set_opacity(0.5), run_time=2.0)
        self.wait()
        for k in range(1, 64):
            self.play(dot_to_move.animate.move_to(axes.c2p(*[history_pre_noise[k, path_index, 0], history_pre_noise[k, path_index, 1]])), ShowCreation(path_segments[2 * k]), path_segments[2 * k].animate.set_opacity(0.8), run_time=0.4)
            self.wait(0.1)
            self.play(dot_to_move.animate.move_to(axes.c2p(*[xt_history[k + 1, path_index, 0], xt_history[k + 1, path_index, 1]])), ShowCreation(path_segments[2 * k + 1]), path_segments[2 * k + 1].animate.set_opacity(0.5), run_time=0.4)
            self.play(time_tracker.animate.set_value(8.0 * (k / 64.0)), run_time=0.1)
        self.wait()
        self.play(FadeOut(path_segments), FadeOut(dot_to_move), FadeOut(vector_field), self.frame.animate.reorient(0, 0, 0, (0.0, 0.0, 0.0), 10), run_time=4.0)
        self.wait()
        num_dots = 256
        colors = get_color_wheel_colors(num_dots)
        all_path_segments = VGroup()
        all_dots_to_move = VGroup()
        for path_index in range(num_dots):
            dot_to_move = Dot(axes.c2p(*np.concatenate((xt_history[0, path_index, :], [0]))), radius=0.06)
            dot_to_move.set_color(colors[path_index])
            all_dots_to_move.add(dot_to_move)
            path_segments = VGroup()
            for k in range(64):
                segment1 = Line(axes.c2p(*[xt_history[k, path_index, 0], xt_history[k, path_index, 1]]), axes.c2p(*[history_pre_noise[k, path_index, 0], history_pre_noise[k, path_index, 1]]), stroke_width=3.0, stroke_color=colors[path_index])
                segment2 = Line(axes.c2p(*[history_pre_noise[k, path_index, 0], history_pre_noise[k, path_index, 1]]), axes.c2p(*[xt_history[k + 1, path_index, 0], xt_history[k + 1, path_index, 1]]), stroke_width=3.0, stroke_color=WHITE)
                segment2.set_opacity(0.4)
                segment1.set_opacity(0.9)
                path_segments.add(segment1)
                path_segments.add(segment2)
            self.add(path_segments)
            path_segments.set_opacity(0.0)
            all_path_segments.add(path_segments)
        self.wait()
        self.play(FadeIn(all_dots_to_move))
        self.wait()
        time_tracker.set_value(0.0)
        self.play(FadeIn(vector_field))
        self.wait()
        history_length = 20
        for k in range(0, 64):
            self.play(*[all_dots_to_move[path_index].animate.move_to(axes.c2p(*[history_pre_noise[k, path_index, 0], history_pre_noise[k, path_index, 1]])) for path_index in range(len(all_dots_to_move))], *[ShowCreation(all_path_segments[path_index][2 * k]) for path_index in range(len(all_dots_to_move))], *[all_path_segments[path_index][2 * k].animate.set_opacity(0.7) for path_index in range(len(all_dots_to_move))], *[all_path_segments[path_index][2 * k - history_length].animate.set_opacity(0.0) for path_index in range(len(all_dots_to_move))], run_time=0.4)
            self.play(*[all_dots_to_move[path_index].animate.move_to(axes.c2p(*[xt_history[k + 1, path_index, 0], xt_history[k + 1, path_index, 1]])) for path_index in range(len(all_dots_to_move))], *[ShowCreation(all_path_segments[path_index][2 * k + 1]) for path_index in range(len(all_dots_to_move))], *[all_path_segments[path_index][2 * k + 1].animate.set_opacity(0.4) for path_index in range(len(all_dots_to_move))], *[all_path_segments[path_index][2 * k + 1 - history_length].animate.set_opacity(0.0) for path_index in range(len(all_dots_to_move))], run_time=0.4)
            self.play(time_tracker.animate.set_value(8.0 * (k / 64.0)), run_time=0.2)
        self.wait()
        self.play(FadeOut(all_path_segments))
        self.wait()
        self.play(FadeOut(all_dots_to_move))
        self.wait()
        self.play(time_tracker.animate.set_value(0.0), run_time=1.0)
        xt_history = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/ddpm_no_noise_1.npy')
        colors = get_color_wheel_colors(num_dots)
        all_traced_paths = VGroup()
        all_dots_to_move = VGroup()
        for path_index in range(num_dots):
            dot_to_move = Dot(axes.c2p(*np.concatenate((xt_history[0, path_index, :], [0]))), radius=0.06)
            dot_to_move.set_color(colors[path_index])
            all_dots_to_move.add(dot_to_move)
            traced_path = CustomTracedPath(dot_to_move.get_center, stroke_color=colors[path_index], stroke_width=2.0, opacity_range=(0.0, 1.0), fade_length=24)
            all_traced_paths.add(traced_path)
        self.add(all_traced_paths)
        self.wait()
        self.play(FadeIn(all_dots_to_move), self.frame.animate.reorient(0, 0, 0, (-0.06, 0.01, 0.0), 7.1), run_time=3.0)
        self.wait()
        for k in range(64):
            self.play(time_tracker.animate.set_value(8.0 * (k / 64.0)), *[all_dots_to_move[path_index].animate.move_to(axes.c2p(*[xt_history[k, path_index, 0], xt_history[k, path_index, 1]])) for path_index in range(len(all_dots_to_move))], rate_func=linear, run_time=0.2)
        self.wait()
        self.play(FadeOut(all_traced_paths), FadeOut(vector_field), FadeOut(axes), self.frame.animate.reorient(0, 0, 0, (-0.11, -0.32, 0.0), 6.34), run_time=2.5)
        self.wait()
        time_tracker.set_value(8.0)
        time_tracker.set_value(0.0)
        self.play(FadeIn(axes), FadeOut(all_dots_to_move), self.frame.animate.reorient(0, 0, 0, (0.0, 0.0, 0.0), 8.25), run_time=3.0)
        self.wait()
        self.wait(20)
        self.embed()