from manimlib import *
from functools import partial
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
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