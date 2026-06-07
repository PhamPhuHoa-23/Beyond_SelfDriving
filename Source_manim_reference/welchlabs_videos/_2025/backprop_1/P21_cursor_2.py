from manimlib import *
sys.path.append('/Users/stephen/manim/videos/_2025/backprop_1')
from backprop_data import xs1, losses1, all_probs_1
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'

def get_prob_graph(axes):
    curve = VMobject()
    curve.set_points_smoothly(axes.c2p(xs1, all_probs_1))
    return curve

def get_loss_graph(axes):
    curve = VMobject()
    curve.set_points_smoothly(axes.c2p(xs1, losses1))
    return curve

def create_axes_with_ranges(x_range, y_range):
    return Axes(x_range=x_range, y_range=y_range, axis_config={'include_ticks': True, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'tip_config': {'fill_opacity': 1, 'width': 0.1, 'length': 0.1}})

class P21(InteractiveScene):

    def construct(self):
        initial_x_range = [-1, 4, 1.0]
        initial_y_range = [0, 1.6, 0.2]
        target_x_range = [1, 2, 0.1]
        target_y_range = [0.5, 1.0, 0.1]
        zoom_tracker = ValueTracker(0)
        axes = always_redraw(lambda: create_axes_with_ranges([interpolate(initial_x_range[0], target_x_range[0], zoom_tracker.get_value()), interpolate(initial_x_range[1], target_x_range[1], zoom_tracker.get_value()), interpolate(initial_x_range[2], target_x_range[2], zoom_tracker.get_value())], [interpolate(initial_y_range[0], target_y_range[0], zoom_tracker.get_value()), interpolate(initial_y_range[1], target_y_range[1], zoom_tracker.get_value()), interpolate(initial_y_range[2], target_y_range[2], zoom_tracker.get_value())]))
        graph = always_redraw(lambda: get_prob_graph(axes))
        self.add(axes, graph)
        self.wait()
        self.play(zoom_tracker.animate.set_value(1), run_time=2, rate_func=smooth)
        self.wait()