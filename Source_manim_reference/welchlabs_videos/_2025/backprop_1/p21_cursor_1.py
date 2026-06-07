from manimlib import *
from functools import partial
sys.path.append('/Users/stephen/manim_videos/_2025/backprop_1')
from backprop_data import all_probs_1, losses1, xs1
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'

class P21(InteractiveScene):

    def construct(self):
        y_axis = Line(start=(-1, -1.2), end=(-1, 1.1), color=CHILL_BROWN, stroke_width=2)
        y_arrow_tip = Triangle(fill_opacity=1, stroke_width=0, color=CHILL_BROWN)
        y_arrow_tip.scale(0.1)
        y_arrow_tip.rotate(PI / 2)
        y_arrow_tip.shift([-1, 1.2, 0])
        x_axis = Line(start=(-1.2, 0.15), end=(1.1, 0.15), color=CHILL_BROWN, stroke_width=2)
        x_arrow_tip = Triangle(fill_opacity=1, stroke_width=0, color=CHILL_BROWN)
        x_arrow_tip.scale(0.1)
        x_arrow_tip.shift([1.2, 0.15, 0])
        axes = Axes(x_range=[-1.2, 1.2, 1.0], y_range=[-1.2, 1.2, 1.0], axis_config={'include_ticks': False, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': False})
        axes.x_axis.set_opacity(0)
        axes.y_axis.set_opacity(0)
        prob_graph = axes.get_graph(lambda x: all_probs_1[int((x + 1.2) * len(all_probs_1) / 2.4)], x_range=[-1.2, 1.2], color=YELLOW)
        loss_graph = axes.get_graph(lambda x: losses1[int((x + 1.2) * len(losses1) / 2.4)], x_range=[-1.2, 1.2], color=BLUE)
        self.add(axes, y_axis, y_arrow_tip, x_axis, x_arrow_tip, prob_graph, loss_graph)