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

def create_noisy_arrow_animation(self, start_point, end_point, target_point, num_steps=100, noise_level=0.1, overshoot_factor=0.3):
    initial_direction = np.array(end_point) - np.array(start_point)
    target_direction = np.array(target_point) - np.array(start_point)
    arrow_length = np.linalg.norm(initial_direction)
    initial_angle = np.arctan2(initial_direction[1], initial_direction[0])
    target_angle = np.arctan2(target_direction[1], target_direction[0])
    angle_diff = target_angle - initial_angle
    if angle_diff > np.pi:
        angle_diff -= 2 * np.pi
    elif angle_diff < -np.pi:
        angle_diff += 2 * np.pi
    t_values = np.linspace(0, 1, num_steps)
    np.random.seed(42)
    noise_decay = np.exp(-3 * t_values)
    angle_noise = noise_level * noise_decay * np.random.randn(num_steps)
    overshoot_frequency = 3.0
    overshoot_decay = np.exp(-2 * t_values)
    overshoot_oscillation = overshoot_factor * overshoot_decay * np.sin(overshoot_frequency * np.pi * t_values)
    t_effective = t_values + overshoot_oscillation
    t_effective[-1] = 1.0
    arrow_positions = []
    for i, t_eff in enumerate(t_effective):
        current_angle = initial_angle + t_eff * angle_diff
        if i < len(t_effective) - 1:
            current_angle += angle_noise[i]
        end_x = np.array(start_point)[0] + arrow_length * np.cos(current_angle)
        end_y = np.array(start_point)[1] + arrow_length * np.sin(current_angle)
        arrow_positions.append([end_x, end_y, 0])
    return arrow_positions

class p48_51v4(InteractiveScene):

    def construct(self):
        batch_size = 2130
        dataset = Swissroll(np.pi / 2, 5 * np.pi, 100)
        loader = DataLoader(dataset, batch_size=batch_size)
        batch = next(iter(loader)).numpy()
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': False, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
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
        traced_path = CustomTracedPath(dot_to_move.get_center, stroke_color=YELLOW, stroke_width=3.5, opacity_range=(0.25, 0.9), fade_length=15)
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
        for j in range(100):
            dot_history.add(dot_to_move.copy().scale(0.4).set_color(YELLOW))
            dot_to_move.move_to(axes.c2p(*random_walk_shifted[j]))
            traced_path.update_path(0.1)
        traced_path.stop_tracing()
        dot_to_move.set_opacity(1.0)
        x100 = Tex('x_{100}', font_size=24).set_color(YELLOW)
        x100.next_to(dot_to_move, 0.07 * UP + 0.001 * RIGHT)
        x0 = Tex('x_{0}', font_size=24).set_color('#00FFFF')
        x0.next_to(dots[i], 0.2 * UP)
        dots[i].set_color('#00FFFF').set_opacity(1.0)
        arrow_x100_to_x0 = Arrow(start=dot_to_move.get_center(), end=dots[i].get_center(), thickness=1, tip_width_ratio=5, buff=0.025)
        arrow_x100_to_x0.set_color('#00FFFF')
        arrow_x100_to_x0.set_opacity(0.6)
        arrow_x100_to_x99 = Arrow(start=dot_to_move.get_center(), end=[4.739921625933185, 2.8708813273028455, 0], thickness=1.5, tip_width_ratio=5, buff=0.04)
        arrow_x100_to_x99.put_start_and_end_on(dot_to_move.get_center(), [4.739921625933185, 2.8708813273028455, 0])
        arrow_x100_to_x99.set_color(CHILL_BROWN)
        self.frame.reorient(0, 0, 0, (3.58, 2.57, 0.0), 2.69)
        self.add(axes, dots, dot_to_move)
        self.add(x100, x0, arrow_x100_to_x0, arrow_x100_to_x99)
        self.wait()
        self.play(FadeOut(dot_to_move), FadeOut(x100), FadeOut(x0), FadeOut(arrow_x100_to_x0), dots.animate.set_opacity(1.0).set_color(YELLOW), run_time=1.5)
        model = torch.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/sora/hackin/jun_20_1.pt')
        schedule = ScheduleLogLinear(N=256, sigma_min=0.01, sigma_max=10)
        bound = 2.0
        num_heatmap_steps = 30
        grid = []
        for i, x in enumerate(np.linspace(-bound, bound, num_heatmap_steps)):
            for j, y in enumerate(np.linspace(-bound, bound, num_heatmap_steps)):
                grid.append([x, y])
        grid = torch.tensor(grid).float()
        gam = 1
        mu = 0.01
        cfg_scale = 0.0
        cond = None
        sigmas = schedule.sample_sigmas(256)
        xt_history = []
        heatmaps = []
        eps = None
        with torch.no_grad():
            model.eval()
            xt = torch.randn((batch_size,) + model.input_dims) * sigmas[0]
            for i, (sig, sig_prev) in enumerate(pairwise(sigmas)):
                eps_prev, eps = (eps, model.predict_eps_cfg(xt, sig.to(xt), cond, cfg_scale))
                sig_p = (sig_prev / sig ** mu) ** (1 / (1 - mu))
                eta = (sig_prev ** 2 - sig_p ** 2).sqrt()
                xt = xt - (sig - sig_p) * eps + eta * model.rand_input(xt.shape[0]).to(xt)
                xt_history.append(xt.numpy())
                heatmaps.append(model.forward(grid, sig, cond=None))
        xt_history = np.array(xt_history)
        self.wait()
        final_vectors = heatmaps[-1].detach().numpy()
        sigma_index = -1

        def vector_function_direct(coords_array):
            res = model.forward(torch.tensor(coords_array).float(), sigmas[sigma_index], cond=None)
            return -res.detach().numpy()
        time_tracker = ValueTracker(0.0)

        def vector_function_with_tracker(coords_array):
            current_time = time_tracker.get_value()
            max_time = 8.0
            sigma_idx = int(np.clip(current_time * 255 / max_time, 0, 255))
            try:
                res = model.forward(torch.tensor(coords_array).float(), sigmas[sigma_idx], cond=None)
                return -res.detach().numpy()
            except:
                return np.zeros((len(coords_array), 2))

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
        vector_field = TrackerControlledVectorField(time_tracker=time_tracker, func=vector_function_with_tracker, coordinate_system=extended_axes, density=3.0, stroke_width=2, max_radius=6.0, min_opacity=0.2, max_opacity=1.0, tip_width_ratio=4, tip_len_to_width=0.01, max_vect_len_to_step_size=0.7, color=CHILL_BROWN)
        self.wait()
        self.play(FadeIn(vector_field), dots.animate.set_opacity(0.75), arrow_x100_to_x99.animate.rotate(-14 * DEGREES).shift([0.17, -0.07, 0]).scale([0.6, 1.2, 1]).set_opacity(0.5), self.frame.animate.reorient(0, 0, 0, (-0.21, 0.02, 0.0), 8.08), run_time=16.0)
        self.remove(arrow_x100_to_x99)
        self.wait()
        dots_to_move = VGroup()
        for point in batch:
            screen_point = axes.c2p(point[0], point[1])
            dot = Dot(screen_point, radius=0.04)
            dots_to_move.add(dot)
        dots_to_move.set_color(YELLOW)
        dots_to_move.set_opacity(1.0)
        random_walks = []
        np.random.seed(2)
        schedule2 = ScheduleLogLinear(N=100, sigma_min=0.02, sigma_max=0.09)
        sigmas100 = schedule2.sample_sigmas(99)
        sigmas100 = sigmas100.numpy()[::-1].reshape(-1, 1)
        for i in range(100):
            rw = sigmas100 * np.random.randn(100, 2)
            rw[0] = np.array([0, 0])
            rw = np.cumsum(rw, axis=0)
            rw = np.hstack((rw, np.zeros((len(rw), 1))))
            rw_shifted = rw + np.array([batch[i][0], batch[i][1], 0])
            random_walks.append(rw_shifted)
        traced_paths = VGroup()
        for idx, d in enumerate(dots_to_move):
            tp = CustomTracedPath(d.get_center, stroke_color=YELLOW, stroke_width=2, opacity_range=(0.1, 0.5), fade_length=10)
            traced_path.set_fill(opacity=0)
            traced_paths.add(tp)
        self.add(traced_paths)
        step_count = MarkupText(str(1), font_size=35)
        step_count.set_color(CHILL_BROWN)
        step_count.move_to([-6.8, -3.3, 0])
        step_label = MarkupText('STEP', font_size=18, font='myriad-pro')
        step_label.set_color(CHILL_BROWN).set_opacity(0.7)
        step_label.next_to(step_count, DOWN, buff=0.1)
        self.wait()
        self.play(FadeOut(vector_field), FadeIn(step_label), FadeIn(step_count))
        self.wait()
        self.add(dots_to_move)
        dots.set_opacity(0.3)
        for step in range(100):
            self.play(*[dots_to_move[i].animate.move_to(axes.c2p(*random_walks[i][step])) for i in range(len(dots_to_move))], run_time=0.1, rate_func=linear)
            self.remove(step_count)
            step_count = MarkupText(str(step + 1), font_size=35)
            step_count.set_color(CHILL_BROWN)
            step_count.move_to([-6.8, -3.3, 0])
            self.add(step_count)
        self.wait()
        for tp in traced_paths:
            tp.stop_tracing()
        vector_field.set_color('#FFFFFF')
        self.play(FadeIn(vector_field), dots_to_move.animate.set_opacity(0.3))
        self.wait()
        self.play(FadeOut(vector_field))
        self.wait()
        editor_warning = MarkupText('Reverse in Post!')
        self.add(editor_warning)
        self.wait()
        self.remove(editor_warning)
        self.wait()
        self.remove(dots_to_move, traced_paths)
        dots_to_move_2 = VGroup()
        for point in batch:
            screen_point = axes.c2p(point[0], point[1])
            dot = Dot(screen_point, radius=0.04)
            dots_to_move_2.add(dot)
        dots_to_move_2.set_color(YELLOW)
        dots_to_move_2.set_opacity(1.0)
        traced_paths_2 = VGroup()
        for idx, d in enumerate(dots_to_move_2):
            tp = CustomTracedPath(d.get_center, stroke_color=YELLOW, stroke_width=2, opacity_range=(0.1, 0.5), fade_length=10)
            traced_path.set_fill(opacity=0)
            traced_paths_2.add(tp)
        self.add(traced_paths_2)
        self.remove(step_count)
        step_count = MarkupText(str(1), font_size=35)
        step_count.set_color(CHILL_BROWN)
        step_count.move_to([-6.8, -3.3, 0])
        self.add(step_count)
        self.add(dots_to_move_2)
        dots.set_opacity(0.3)
        for step in range(2):
            self.play(*[dots_to_move_2[i].animate.move_to(axes.c2p(*random_walks[i][step])) for i in range(len(dots_to_move_2))], run_time=0.1, rate_func=linear)
        self.wait()
        self.add(vector_field)
        time_tracker.set_value(8 * (99 / 100))
        self.wait()
        self.remove(vector_field)
        self.play(FadeIn(vector_field), dots_to_move_2.animate.set_opacity(0.3))
        self.wait()
        self.play(FadeOut(vector_field), FadeOut(dots_to_move_2), FadeOut(traced_paths_2), FadeOut(step_count), FadeOut(step_label), FadeIn(traced_path), FadeIn(dot_to_move), self.frame.animate.reorient(0, 0, 0, (3.58, 2.57, 0.0), 2.69), run_time=5.0)
        self.wait()
        x100 = Tex('x_{100}', font_size=24).set_color(YELLOW)
        x100.next_to(dot_to_move, 0.07 * UP + 0.001 * RIGHT)
        x0 = Tex('x_{0}', font_size=24).set_color('#00FFFF')
        x0.next_to(dots[75], 0.2 * UP)
        arrow_x100_to_x0.set_opacity(1.0)
        self.add(arrow_x100_to_x0)
        dots[75].set_color('#00FFFF').set_opacity(1.0)
        self.add(x100, x0)
        self.wait()
        eq_1 = Tex('f(x_{100})', font_size=24)
        eq_1.set_color('#00FFFF')
        eq_1.move_to([3.5, 2.2, 0])
        self.add(eq_1)
        eq_2 = Tex('f(x_{100}, t)', font_size=24)
        eq_2.set_color('#00FFFF')
        eq_2.move_to(eq_1, aligned_edge=LEFT)
        self.wait()
        self.play(eq_1[-1].animate.move_to([4.03, 2.2, 0]), run_time=1.4)
        self.add(eq_2)
        self.remove(eq_1)
        self.wait()
        eq_3 = Tex('f(x_{100}, t=1.0)', font_size=24)
        eq_3.set_color('#00FFFF')
        eq_3.move_to(eq_1, aligned_edge=LEFT)
        self.wait()
        self.play(eq_2[-1].animate.move_to([4.65, 2.2, 0]), run_time=1.4)
        self.add(eq_3)
        self.remove(eq_2)
        self.wait()
        arrow_x99_to_x0 = Arrow(start=traced_path.traced_points[-2], end=dots[75].get_center(), thickness=1, tip_width_ratio=5, buff=0.025)
        arrow_x99_to_x0.set_color('#FF00FF')
        arrow_x99_to_x0.set_opacity(1.0)
        dot99 = Dot(traced_path.traced_points[-2], radius=0.04)
        dot99.set_color('#FF00FF')
        eq_4 = Tex('f(x_{99}, t=0.99)', font_size=20)
        eq_4.set_color('#FF00FF')
        eq_4.move_to([3.1, 2.9, 0])
        self.wait()
        self.play(FadeIn(arrow_x99_to_x0), FadeIn(dot99), FadeIn(eq_4))
        self.wait()
        arrow_x3_to_x0 = Arrow(start=traced_path.traced_points[2], end=dots[75].get_center(), thickness=1, tip_width_ratio=5, buff=0.025)
        arrow_x3_to_x0.set_color(GREEN)
        arrow_x3_to_x0.set_opacity(1.0)
        dot3 = Dot(traced_path.traced_points[2], radius=0.04)
        dot3.set_color(GREEN)
        eq_5 = Tex('f(x_{2}, t=0.02)', font_size=20)
        eq_5.set_color(GREEN)
        eq_5.move_to([1.93, 2.45, 0])
        self.wait()
        self.play(FadeIn(arrow_x3_to_x0), FadeIn(dot3), FadeIn(eq_5))
        self.wait()
        self.play(FadeOut(arrow_x3_to_x0), FadeOut(eq_5), FadeOut(eq_4), FadeOut(eq_3), FadeOut(arrow_x99_to_x0), FadeOut(arrow_x100_to_x0), FadeOut(traced_path), FadeOut(dot_to_move), FadeOut(x100), FadeOut(dot3), FadeOut(dot99), FadeOut(dot_to_move), dots[75].animate.set_color(YELLOW).set_opacity(0.3), FadeOut(x0), self.frame.animate.reorient(0, 0, 0, (-0.21, 0.02, 0.0), 8.08), run_time=4.0)
        self.wait()
        time_tracker.set_value(0)
        vector_field.set_color('#FFFFFF')
        self.wait()
        time_value = ValueTracker(1.0)
        time_display = DecimalNumber(1.0, num_decimal_places=2, font_size=35, color=CHILL_BROWN)
        time_display.move_to([-6.3, -3.3, 0])
        time_label = MarkupText('t =', font_size=35)
        time_label.set_color(CHILL_BROWN)
        time_label.next_to(time_display, LEFT, buff=0.15)
        time_display.add_updater(lambda m: m.set_value(time_value.get_value()))
        time_tracker.set_value(0)
        self.play(FadeIn(vector_field), FadeIn(time_label), FadeIn(time_display))
        self.wait()
        self.play(time_tracker.animate.set_value(8.0), time_value.animate.set_value(0.0), run_time=10.0, rate_func=linear)
        self.wait()
        self.wait(20)
        self.embed()

class p47bv2(InteractiveScene):

    def construct(self):
        batch_size = 2130
        dataset = Swissroll(np.pi / 2, 5 * np.pi, 100)
        loader = DataLoader(dataset, batch_size=batch_size)
        batch = next(iter(loader)).numpy()
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': False, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
        dots = VGroup()
        for point in batch:
            screen_point = axes.c2p(point[0], point[1])
            dot = Dot(screen_point, radius=0.04)
            dots.add(dot)
        dots.set_color(YELLOW)
        dots.set_opacity(0.3)
        i = 75
        dot_to_move = dots[i].copy()
        traced_path = CustomTracedPath(dot_to_move.get_center, stroke_color=YELLOW, stroke_width=3.5, opacity_range=(0.25, 0.9), fade_length=15)
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
        for j in range(100):
            dot_history.add(dot_to_move.copy().scale(0.4).set_color(YELLOW))
            dot_to_move.move_to(axes.c2p(*random_walk_shifted[j]))
            traced_path.update_path(0.1)
        traced_path.stop_tracing()
        dot_to_move.set_opacity(1.0)
        self.frame.reorient(0, 0, 0, (3.58, 2.57, 0.0), 2.69)
        self.add(axes, dots, traced_path, dot_to_move)
        self.wait()
        x100 = Tex('x_{100}', font_size=24).set_color(YELLOW)
        x100.next_to(dot_to_move, 0.07 * UP + 0.001 * RIGHT)
        x99 = Tex('x_{99}', font_size=24).set_color(CHILL_BROWN)
        x99.next_to(dot_history[-1], 0.1 * UP + 0.01 * RIGHT)
        dot99 = Dot(dot_history[-1].get_center(), radius=0.04)
        dot99.set_color(CHILL_BROWN)
        x0 = Tex('x_{0}', font_size=24).set_color('#00FFFF')
        x0.next_to(dots[i], 0.2 * UP)
        dots[i].set_color('#00FFFF').set_opacity(1.0)
        arrow_x100_to_x0 = Arrow(start=dot_to_move.get_center(), end=dots[i].get_center(), thickness=1, tip_width_ratio=5, buff=0.025)
        arrow_x100_to_x0.set_color('#00FFFF')
        arrow_x100_to_x0.set_opacity(0.6)
        arrow_x100_to_x99 = Arrow(start=dot_to_move.get_center(), end=dot_history[-1].get_center(), thickness=1.5, tip_width_ratio=5, buff=0.04)
        arrow_x100_to_x99.set_color(CHILL_BROWN)
        self.add(x100, x99, dot99, x0, arrow_x100_to_x0, arrow_x100_to_x99)
        self.wait()
        self.remove(x99, traced_path)
        self.wait()
        noise_level = 0.06
        overshoot_factor = 2.0
        start_delay = 20
        early_end = 10
        arrow_end_positions = create_noisy_arrow_animation(self, start_point=dot_to_move.get_center()[:2], end_point=dot_history[-1].get_center()[:2], target_point=dots[i].get_center()[:2], num_steps=100 - start_delay - early_end, noise_level=noise_level, overshoot_factor=overshoot_factor)
        random_walks = []
        np.random.seed(2)
        for j in tqdm(range(int(2000000.0))):
            rw = 0.07 * np.random.randn(100, 2)
            rw[0] = np.array([0, 0])
            rw = np.cumsum(rw, axis=0)
            rw = np.hstack((rw, np.zeros((len(rw), 1))))
            rw_shifted = rw + np.array([batch[j % len(batch)][0], batch[j % len(batch)][1], 0])
            if rw_shifted[-1][0] > 2.1 and rw_shifted[-1][1] > 1.4:
                random_walks.append(rw_shifted)
        print(len(random_walks))
        print(len(random_walks))
        dots_to_move = VGroup()
        for j in range(len(random_walks)):
            screen_point = axes.c2p(batch[j % len(batch)][0], batch[j % len(batch)][1])
            dot = Dot(screen_point, radius=0.04)
            dots_to_move.add(dot)
        dots_to_move.set_color(FRESH_TAN)
        dots_to_move.set_opacity(0.2)
        traced_paths = VGroup()
        for idx, d in enumerate(dots_to_move):
            if idx != 75:
                tp = CustomTracedPath(d.get_center, stroke_color=FRESH_TAN, stroke_width=2, opacity_range=(0.01, 0.35), fade_length=10)
                traced_path.set_fill(opacity=0)
                traced_paths.add(tp)
        self.add(traced_paths)
        self.wait()
        for step in range(100):
            self.play(*[dots_to_move[i].animate.move_to(axes.c2p(*random_walks[i][step])) for i in range(len(random_walks))], run_time=0.1, rate_func=linear)
            if step > start_delay:
                arrow_index = np.clip(step - start_delay, 0, len(arrow_end_positions) - 1)
                arrow_x100_to_x99.put_start_and_end_on(dot_to_move.get_center(), arrow_end_positions[arrow_index])
        self.wait()
        self.remove(dots_to_move, traced_paths, dot99)
        self.wait(20)
        self.embed()

class p44_47(InteractiveScene):

    def construct(self):
        batch_size = 2130
        dataset = Swissroll(np.pi / 2, 5 * np.pi, 100)
        loader = DataLoader(dataset, batch_size=batch_size)
        batch = next(iter(loader)).numpy()
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': False, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
        dots = VGroup()
        for point in batch:
            screen_point = axes.c2p(point[0], point[1])
            dot = Dot(screen_point, radius=0.04)
            dots.add(dot)
        dots.set_color(YELLOW)
        i = 75
        dot_to_move = dots[i].copy()
        traced_path = CustomTracedPath(dot_to_move.get_center, stroke_color=YELLOW, stroke_width=3.5, opacity_range=(0.25, 0.9), fade_length=15)
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
        for i in range(100):
            dot_history.add(dot_to_move.copy().scale(0.4).set_color(YELLOW))
            dot_to_move.move_to(axes.c2p(*random_walk_shifted[i]))
            traced_path.update_path(0.1)
        self.frame.reorient(0, 0, 0, (-0.07, 0.01, 0.0), 7.59)
        self.add(axes, dots)
        self.wait()
        traced_path.stop_tracing()
        self.play(FadeIn(traced_path), FadeIn(dot_to_move))
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (3.58, 2.57, 0.0), 2.69), dots.animate.set_opacity(0.3), run_time=3.0)
        self.wait()
        random_walks = []
        np.random.seed(2)
        for j in tqdm(range(int(2000000.0))):
            rw = 0.07 * np.random.randn(100, 2)
            rw[0] = np.array([0, 0])
            rw = np.cumsum(rw, axis=0)
            rw = np.hstack((rw, np.zeros((len(rw), 1))))
            rw_shifted = rw + np.array([batch[j % len(batch)][0], batch[j % len(batch)][1], 0])
            if rw_shifted[-1][0] > 2.1 and rw_shifted[-1][1] > 1.4:
                random_walks.append(rw_shifted)
        print(len(random_walks))
        print(len(random_walks))
        dots_to_move = VGroup()
        for j in range(len(random_walks)):
            screen_point = axes.c2p(batch[j % len(batch)][0], batch[j % len(batch)][1])
            dot = Dot(screen_point, radius=0.04)
            dots_to_move.add(dot)
        dots_to_move.set_color(FRESH_TAN)
        dots_to_move.set_opacity(0.3)
        traced_paths = VGroup()
        for idx, d in enumerate(dots_to_move):
            if idx != 75:
                tp = CustomTracedPath(d.get_center, stroke_color=FRESH_TAN, stroke_width=2, opacity_range=(0.02, 0.5), fade_length=10)
                traced_path.set_fill(opacity=0)
                traced_paths.add(tp)
        self.add(traced_paths)
        remaining_indices = np.concatenate((np.arange(75), np.arange(76, len(batch))))
        start_orientation = [0, 0, 0, (3.58, 2.57, 0.0), 2.69]
        end_orientation = [0, 0, 0, (4.86, 2.65, 0.0), 3.06]
        interp_orientations = manual_camera_interpolation(start_orientation, end_orientation, num_steps=100)
        remaining_indices = np.concatenate((np.arange(75), np.arange(76, len(batch))))
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (2.74, 1.72, 0.0), 3.99))
        r = RoundedRectangle(1.5, 1.0, 0.05)
        r.set_stroke(color='#00FFFF', width=2)
        r.move_to(dot_to_move)
        self.add(r)
        self.wait()
        for step in range(100):
            self.play(*[dots_to_move[i].animate.move_to(axes.c2p(*random_walks[i][step])) for i in range(len(random_walks))], run_time=0.1, rate_func=linear)
        self.wait()
        for tp in traced_paths:
            tp.stop_tracing()
        self.remove(dots_to_move, traced_paths)
        self.play(FadeOut(r))
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (3.58, 2.57, 0.0), 2.69), run_time=3)
        self.wait()
        self.wait(20)
        self.embed()

class p40_44v2(InteractiveScene):

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
        self.play(FadeIn(dots, lag_ratio=0.1), run_time=2)
        self.wait()
        i = 75
        dot_to_move = dots[i].copy()
        self.wait()
        self.play(dots.animate.set_opacity(0.1), dot_to_move.animate.scale(1.25), self.frame.animate.reorient(0, 0, 0, (2.92, 1.65, 0.0), 4.19), run_time=2.0)
        self.wait()
        traced_path = CustomTracedPath(dot_to_move.get_center, stroke_color=YELLOW, stroke_width=2, opacity_range=(0.1, 0.8), fade_length=15)
        traced_path.set_fill(opacity=0)
        self.add(traced_path)
        self.add(dot_to_move)
        np.random.seed(485)
        random_walk = 0.07 * np.random.randn(100, 2)
        random_walk[0] = np.array([0.2, 0.12])
        random_walk[-1] = np.array([0.08, -0.02])
        random_walk = np.cumsum(random_walk, axis=0)
        print(random_walk[0])
        random_walk = np.hstack((random_walk, np.zeros((len(random_walk), 1))))
        random_walk_shifted = random_walk + np.array([batch[i][0], batch[i][1], 0])
        print(random_walk_shifted[-1])
        self.wait()
        dot_history = VGroup()
        dot_history.add(dot_to_move.copy().scale(0.22).set_color(YELLOW_FADE))
        self.add(dot_history[-1])
        self.play(dot_to_move.animate.move_to(axes.c2p(*random_walk_shifted[0])), run_time=1.0)
        self.wait()
        for i in range(100):
            dot_history.add(dot_to_move.copy().scale(0.22).set_color(YELLOW_FADE))
            self.add(dot_history[-1])
            self.play(dot_to_move.animate.move_to(axes.c2p(*random_walk_shifted[i])), run_time=0.1, rate_func=linear)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-0.07, 0.01, 0.0), 7.59), dots.animate.set_opacity(1.0), run_time=3.0)
        self.wait()
        random_walks = []
        np.random.seed(2)
        schedule2 = ScheduleLogLinear(N=100, sigma_min=0.02, sigma_max=0.09)
        sigmas100 = schedule2.sample_sigmas(99)
        sigmas100 = sigmas100.numpy()[::-1].reshape(-1, 1)
        for i in range(100):
            rw = sigmas100 * np.random.randn(100, 2)
            rw[0] = np.array([0, 0])
            rw = np.cumsum(rw, axis=0)
            rw = np.hstack((rw, np.zeros((len(rw), 1))))
            rw_shifted = rw + np.array([batch[i][0], batch[i][1], 0])
            random_walks.append(rw_shifted)
        traced_paths = VGroup()
        for idx, d in enumerate(dots):
            if idx != 75:
                tp = CustomTracedPath(d.get_center, stroke_color=YELLOW, stroke_width=2, opacity_range=(0.1, 0.5), fade_length=10)
                traced_path.set_fill(opacity=0)
                traced_paths.add(tp)
        self.add(traced_paths)
        remaining_indices = np.concatenate((np.arange(75), np.arange(76, len(batch))))
        start_orientation = [0, 0, 0, (-0.07, 0.01, 0.0), 7.59]
        end_orientation = [0, 0, 0, (0.29, -0.21, 0.0), 12.94]
        interp_orientations = manual_camera_interpolation(start_orientation, end_orientation, num_steps=100)
        self.wait()
        remaining_indices = np.concatenate((np.arange(75), np.arange(76, len(batch))))
        for step in range(100):
            self.play(*[dots[i].animate.move_to(axes.c2p(*random_walks[i][step])) for i in remaining_indices], self.frame.animate.reorient(*interp_orientations[step]), run_time=0.1, rate_func=linear)
            self.remove(dot_history)
            self.remove(dot_to_move)
            self.remove(traced_path)
            self.remove(dots[75])
        self.wait()
        for tp in traced_paths:
            tp.stop_tracing()
        self.wait()
        for j, step in enumerate(range(99, -1, -1)):
            self.play(*[dots[i].animate.move_to(axes.c2p(*random_walks[i][step])) for i in remaining_indices], self.frame.animate.reorient(*interp_orientations[step]), run_time=0.1, rate_func=linear)
            for tp in traced_paths:
                tp.remove_last_segment()
                if j == 0:
                    tp.remove_last_segment()
        self.add(dots[75])
        self.wait()
        self.wait(20)
        self.embed()