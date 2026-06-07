from manimlib import *
from functools import partial
import numpy as np
import torch
import sys
sys.path.append('_2025/backprop_2')
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
GREEN = '#00a14b'

def get_edge_points(circle1, circle2, neuron_radius):
    direction = circle2.get_center() - circle1.get_center()
    unit_vector = direction / np.linalg.norm(direction)
    start_point = circle1.get_center() + unit_vector * neuron_radius
    end_point = circle2.get_center() - unit_vector * neuron_radius
    return (start_point, end_point)
viridis_colormap = plt.get_cmap('viridis')
blues_colormap = plt.get_cmap('Blues')
custom_cmap_tans = mcolors.LinearSegmentedColormap.from_list('custom', ['#000000', '#dfd0b9'], N=256)
custom_cmap_cyan = mcolors.LinearSegmentedColormap.from_list('custom', ['#000000', '#00FFFF'], N=256)

def get_nueron_color(value, vmax=0.95):
    value_clipped = np.clip(np.abs(value) / vmax, 0, 1)
    rgba = custom_cmap_tans(value_clipped)
    return Color(rgb=rgba[:3])

def get_grad_color(value, vmin=-2, vmax=2):
    value_clipped = np.clip((value - vmin) / (vmax - vmin), 0, 1)
    rgba = custom_cmap_cyan(value_clipped)
    return Color(rgb=rgba[:3])

class AttentionPattern(VMobject):

    def __init__(self, matrix, square_size=0.3, min_opacity=0.0, max_opacity=1.0, stroke_width=1.0, viz_scaling_factor=2.5, stroke_color=CHILL_BROWN, colormap=custom_cmap_tans, **kwargs):
        super().__init__(**kwargs)
        self.matrix = np.array(matrix)
        self.n_rows, self.n_cols = self.matrix.shape
        self.square_size = square_size
        self.min_opacity = min_opacity
        self.max_opacity = np.max(self.matrix)
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self._colormap = colormap
        self.viz_scaling_factor = viz_scaling_factor
        self.build()

    def map_value_to_style(self, val):
        val_scaled = np.clip(self.viz_scaling_factor * val / self.max_opacity, 0, 1)
        rgba = self._colormap(val_scaled)
        color = Color(rgb=rgba[:3])
        opacity = 1.0
        return {'color': color, 'opacity': opacity}

    def build(self):
        self.clear()
        squares = VGroup()
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                val = self.matrix[i, j]
                style = self.map_value_to_style(val)
                square = Square(side_length=self.square_size)
                square.set_fill(style['color'], opacity=style['opacity'])
                square.set_stroke(self.stroke_color, width=self.stroke_width)
                pos = RIGHT * j * self.square_size + DOWN * i * self.square_size
                square.move_to(pos)
                squares.add(square)
        squares.move_to(ORIGIN)
        self.add(squares)

def get_mlp(w1, w2, neuron_fills=None, grads_1=None, grads_2=None, line_weight=1.0, line_opacity=0.5, neuron_stroke_width=1.0, neuron_stroke_color='#dfd0b9', line_stroke_color='#948979', connection_display_thresh=0.4, grad_display_thresh=0.5):
    INPUT_NEURONS = w1.shape[0]
    HIDDEN_NEURONS = w1.shape[1]
    OUTPUT_NEURONS = w1.shape[0]
    NEURON_RADIUS = 0.06
    LAYER_SPACING = 0.23
    VERTICAL_SPACING = 0.18
    DOTS_SCALE = 0.5
    input_layer = VGroup()
    hidden_layer = VGroup()
    output_layer = VGroup()
    dots = VGroup()
    for i in range(INPUT_NEURONS):
        if i == w1.shape[0] // 2:
            dot = Tex('...').rotate(PI / 2, OUT).scale(DOTS_SCALE).move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            dot.set_color(neuron_stroke_color)
            dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=neuron_stroke_color)
            neuron.set_stroke(width=neuron_stroke_width)
            if neuron_fills is None:
                neuron.set_fill(color='#000000', opacity=1.0)
            else:
                neuron.set_fill(color=get_nueron_color(neuron_fills[0][i]), opacity=1.0)
            neuron.move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            input_layer.add(neuron)
    for i in range(HIDDEN_NEURONS):
        if i == w1.shape[1] // 2:
            dot = Tex('...').rotate(PI / 2, OUT).scale(DOTS_SCALE).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            dot.set_color(neuron_stroke_color)
            dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=neuron_stroke_color)
            neuron.set_stroke(width=neuron_stroke_width)
            if neuron_fills is None:
                neuron.set_fill(color='#000000', opacity=1.0)
            else:
                neuron.set_fill(color=get_nueron_color(neuron_fills[1][i]), opacity=1.0)
            neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            hidden_layer.add(neuron)
    for i in range(OUTPUT_NEURONS):
        if i == w1.shape[0] // 2:
            dot = Tex('...').rotate(PI / 2, OUT).scale(DOTS_SCALE).move_to(RIGHT * LAYER_SPACING + UP * ((OUTPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            dot.set_color(neuron_stroke_color)
            dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=neuron_stroke_color)
            neuron.set_stroke(width=neuron_stroke_width)
            if neuron_fills is None:
                neuron.set_fill(color='#000000', opacity=1.0)
            else:
                neuron.set_fill(color=get_nueron_color(neuron_fills[2][i]), opacity=1.0)
            neuron.move_to(RIGHT * LAYER_SPACING + UP * ((OUTPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            output_layer.add(neuron)
    connections = VGroup()
    w1_abs = np.abs(w1)
    w1_scaled = w1_abs / np.percentile(w1_abs, 99)
    for i, in_neuron in enumerate(input_layer):
        for j, hidden_neuron in enumerate(hidden_layer):
            if np.abs(w1_scaled[i, j]) < 0.75:
                continue
            if abs(i - j) > 6:
                continue
            start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
            line = Line(start_point, end_point)
            line.set_stroke(opacity=np.clip(w1_scaled[i, j], 0, 1), width=1.0 * w1_scaled[i, j])
            line.set_color(line_stroke_color)
            connections.add(line)
    w2_abs = np.abs(w2)
    w2_scaled = w2_abs / np.percentile(w2_abs, 99)
    for i, hidden_neuron in enumerate(hidden_layer):
        for j, out_neuron in enumerate(output_layer):
            if np.abs(w2_scaled[i, j]) < 0.45:
                continue
            if abs(i - j) > 6:
                continue
            start_point, end_point = get_edge_points(hidden_neuron, out_neuron, NEURON_RADIUS)
            line = Line(start_point, end_point)
            line.set_stroke(opacity=np.clip(w2_scaled[i, j], 0, 1), width=1.0 * w2_scaled[i, j])
            line.set_color(line_stroke_color)
            connections.add(line)
    grad_conections = VGroup()
    if grads_1 is not None:
        for i, in_neuron in enumerate(input_layer):
            for j, hidden_neuron in enumerate(hidden_layer):
                if np.abs(grads_1[i, j]) < grad_display_thresh:
                    continue
                if abs(i - j) > 6:
                    continue
                start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
                line_grad = Line(start_point, end_point)
                line_grad.set_stroke(opacity=np.clip(0.8 * (np.abs(grads_1[i, j]) - grad_display_thresh), 0, 1), width=np.abs(grads_1[i, j]))
                line_grad.set_color(get_grad_color(grads_1[i, j]))
                grad_conections.add(line_grad)
    if grads_2 is not None:
        for i, hidden_neuron in enumerate(hidden_layer):
            for j, out_neuron in enumerate(output_layer):
                if np.abs(grads_2[i, j]) < grad_display_thresh:
                    continue
                if abs(i - j) > 6:
                    continue
                start_point, end_point = get_edge_points(hidden_neuron, out_neuron, NEURON_RADIUS)
                line_grad = Line(start_point, end_point)
                line_grad.set_stroke(opacity=np.clip(0.8 * (np.abs(grads_2[i, j]) - grad_display_thresh), 0, 1), width=np.abs(grads_2[i, j]))
                line_grad.set_color(get_grad_color(grads_2[i, j]))
                grad_conections.add(line_grad)
    return VGroup(connections, grad_conections, input_layer, hidden_layer, output_layer, dots)

class LlamaLearningSketchOne(InteractiveScene):

    def construct(self):
        grads_1 = np.random.randn(32, 34)
        grads_2 = np.random.randn(34, 32)
        data_dir = '/Users/stephen/welch_labs/backprop2/hackin/may_31_1'
        layer_num = 8
        neuron_fills = [np.load(data_dir + '/blocks.' + str(layer_num) + '.hook_resid_mid.npy'), np.load(data_dir + '/blocks.' + str(layer_num) + '.mlp.hook_post.npy'), np.load(data_dir + '/blocks.' + str(layer_num) + '.hook_mlp_out.npy')]
        w1 = np.load(data_dir + '/blocks.' + str(layer_num) + '.mlp.W_in' + '.npy')
        w2 = np.load(data_dir + '/blocks.' + str(layer_num) + '.mlp.W_out' + '.npy')
        mlp = get_mlp(w1, w2, neuron_fills)
        mlp.move_to([-4, 0, 0])
        neuron_fills = [np.load(data_dir + '/blocks.' + str(layer_num + 1) + '.hook_resid_mid.npy'), np.load(data_dir + '/blocks.' + str(layer_num + 1) + '.mlp.hook_post.npy'), np.load(data_dir + '/blocks.' + str(layer_num + 1) + '.hook_mlp_out.npy')]
        w1 = np.load(data_dir + '/blocks.' + str(layer_num + 1) + '.mlp.W_in' + '.npy')
        w2 = np.load(data_dir + '/blocks.' + str(layer_num + 1) + '.mlp.W_out' + '.npy')
        mlp2 = get_mlp(w1, w2, neuron_fills)
        mlp2.move_to([-2.4, 0, 0])
        attention_connection_display_thresh = 0.5
        all_attn_patterns = np.load(data_dir + '/blocks.' + str(layer_num) + '.attn.hook_pattern.npy')
        wO_full = np.load(data_dir + '/blocks.' + str(layer_num) + '.attn.W_O.npy')
        wq_full = np.load(data_dir + '/blocks.' + str(layer_num) + '.attn.W_Q.npy')
        attn_patterns = []
        wos = []
        wqs = []
        for i in range(0, 30, 3):
            attn_patterns.append(all_attn_patterns[0][i][1:, 1:])
            wos.append(wO_full[i, 0])
            wqs.append(wq_full[i, :, 0])
        wos = np.array(wos)
        wqs = np.array(wqs)
        attention_connections_left = wqs.T
        attention_connections_right = wos
        num_attention_pattern_slots = len(attn_patterns) + 1
        attention_pattern_spacing = 0.51
        attention_border = RoundedRectangle(width=0.59, height=5.4, corner_radius=0.1)
        attention_border.set_stroke(width=1.0, color=CHILL_BROWN)
        attention_patterns = VGroup()
        connection_points_left = VGroup()
        connection_points_right = VGroup()
        attn_pattern_count = 0
        for i in range(num_attention_pattern_slots):
            if i == num_attention_pattern_slots // 2:
                dot = Tex('...').rotate(PI / 2, OUT).scale(0.5).move_to([0, num_attention_pattern_slots * attention_pattern_spacing / 2 - attention_pattern_spacing * (i + 0.5), 0])
                dot.set_color(CHILL_BROWN)
                attention_patterns.add(dot)
            else:
                if i > num_attention_pattern_slots // 2:
                    offset = 0.15
                else:
                    offset = -0.15
                attn_pattern = AttentionPattern(matrix=attn_patterns[attn_pattern_count], square_size=0.07, stroke_width=0.5)
                attn_pattern.move_to([0, num_attention_pattern_slots * attention_pattern_spacing / 2 + offset - attention_pattern_spacing * (i + 0.5), 0])
                attention_patterns.add(attn_pattern)
                connection_point_left = Circle(radius=0)
                connection_point_left.move_to([-0.59 / 2.0, num_attention_pattern_slots * attention_pattern_spacing / 2 + offset - attention_pattern_spacing * (i + 0.5), 0])
                connection_points_left.add(connection_point_left)
                connection_point_right = Circle(radius=0)
                connection_point_right.move_to([0.59 / 2.0, num_attention_pattern_slots * attention_pattern_spacing / 2 + offset - attention_pattern_spacing * (i + 0.5), 0])
                connection_points_right.add(connection_point_right)
                attn_pattern_count += 1
        attention_layer = VGroup(attention_patterns, attention_border, connection_points_left, connection_points_right)
        attention_layer.move_to([-3.2, 0, 0])
        connections_left = VGroup()
        attention_connections_left_abs = np.abs(attention_connections_left)
        attention_connections_left_scaled = attention_connections_left_abs / np.max(attention_connections_left_abs)
        for i, mlp_out_neuron in enumerate(mlp[4]):
            for j, attention_neuron in enumerate(connection_points_left):
                if np.abs(attention_connections_left_scaled[i, j]) < 0.5:
                    continue
                if abs(i / 4 - j) > 3:
                    continue
                start_point, end_point = get_edge_points(mlp_out_neuron, attention_neuron, 0.06)
                line = Line(start_point, attention_neuron.get_center())
                line.set_stroke(opacity=np.clip(attention_connections_left_scaled[i, j], 0, 1), width=1.0 * attention_connections_left_scaled[i, j])
                line.set_color(CHILL_BROWN)
                connections_left.add(line)
        connections_right = VGroup()
        attention_connections_right_abs = np.abs(attention_connections_right)
        attention_connections_right_scaled = attention_connections_right_abs / np.percentile(attention_connections_left_abs, 99)
        for i, attention_neuron in enumerate(connection_points_right):
            for j, mlp_in_neuron in enumerate(mlp2[2]):
                if np.abs(attention_connections_right_scaled[i, j]) < 0.6:
                    continue
                if abs(j / 4 - i) > 3:
                    continue
                start_point, end_point = get_edge_points(mlp_in_neuron, attention_neuron, 0.06)
                line = Line(start_point, attention_neuron.get_center())
                line.set_stroke(opacity=np.clip(attention_connections_right_scaled[i, j], 0, 1), width=1.0 * attention_connections_right_scaled[i, j])
                line.set_color(CHILL_BROWN)
                connections_right.add(line)
        self.add(connections_left)
        self.add(connections_right)
        self.add(mlp)
        self.add(attention_layer)
        self.add(mlp2)
        self.remove(mlp[3][1])
        self.add(mlp[3][1])
        self.remove(mlp[2][1])
        self.add(mlp[2][1])
        self.remove(mlp[4][1])
        self.add(mlp[4][1])
        self.remove(mlp2[3][1])
        self.add(mlp2[3][1])
        self.remove(mlp2[2][1])
        self.add(mlp2[2][1])
        self.remove(mlp2[4][1])
        self.add(mlp2[4][1])
        self.wait()
        self.wait()
        self.wait()
        self.embed()