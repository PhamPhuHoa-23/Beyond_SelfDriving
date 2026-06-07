from manimlib import *
import glob
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
GREEN = '#00a14b'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
from torch.utils.data import DataLoader
from smalldiffusion import ScheduleLogLinear, samples, Swissroll, ModelMixin

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

class p40_51_sketch(InteractiveScene):

    def construct(self):
        batch_size = 2130
        dataset = Swissroll(np.pi / 2, 5 * np.pi, 100)
        loader = DataLoader(dataset, batch_size=batch_size)
        batch = next(iter(loader)).numpy()
        axes = Axes(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5], height=7, width=7, axis_config={'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'include_ticks': True, 'tick_size': 0.06, 'tip_config': {'color': CHILL_BROWN, 'length': 0.15, 'width': 0.15}})
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
        traced_path = TracedPath(dot_to_move.get_center, stroke_color=YELLOW, stroke_width=2)
        traced_path.set_opacity(0.5)
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
        dot_history.add(dot_to_move.copy().scale(0.25))
        self.add(dot_history[-1])
        self.play(dot_to_move.animate.move_to(axes.c2p(*random_walk_shifted[0])), run_time=1.0)
        self.wait()
        for i in range(100):
            dot_history.add(dot_to_move.copy().scale(0.25))
            self.add(dot_history[-1])
            self.play(dot_to_move.animate.move_to(axes.c2p(*random_walk_shifted[i])), run_time=0.2, rate_func=linear)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-0.07, 0.01, 0.0), 7.59), dots.animate.set_opacity(1.0), run_time=3.0)
        self.wait()
        random_walks = []
        np.random.seed(2)
        for i in range(100):
            rw = 0.07 * np.random.randn(100, 2)
            rw = np.cumsum(rw, axis=0)
            rw = np.hstack((rw, np.zeros((len(rw), 1))))
            rw_shifted = rw + np.array([batch[i][0], batch[i][1], 0])
            random_walks.append(rw_shifted)
        traced_paths = VGroup()
        for d in dots:
            tp = TracedPath(d.get_center, stroke_color=YELLOW, stroke_width=2)
            tp.set_opacity(0.2)
            tp.set_fill(opacity=0)
            traced_path.add(tp)
        remaining_indices = np.concatenate((np.arange(75), np.arange(76, len(batch))))
        start_orientation = [0, 0, 0, (-0.07, 0.01, 0.0), 7.59]
        end_orientation = [0, 0, 0, (0.23, -0.24, 0.0), 14.98]
        interp_orientations = manual_camera_interpolation(start_orientation, end_orientation, num_steps=100)
        self.wait()
        remaining_indices = np.concatenate((np.arange(75), np.arange(76, len(batch))))
        for step in range(100):
            self.play(*[dots[i].animate.move_to(axes.c2p(*random_walks[i][step])) for i in remaining_indices], self.frame.animate.reorient(*interp_orientations[step]), run_time=0.1, rate_func=linear)
        self.wait()
        self.wait(20)
        self.embed()