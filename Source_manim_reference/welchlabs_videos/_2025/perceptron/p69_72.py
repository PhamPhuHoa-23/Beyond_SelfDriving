from manimlib import *
from functools import partial
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys
sys.path.append('/Users/stephen/Dropbox/welch_labs/perceptron/animations/videos')
from helpers import *
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'

def get_edge_points(circle1, circle2, neuron_radius):
    direction = circle2.get_center() - circle1.get_center()
    unit_vector = direction / np.linalg.norm(direction)
    start_point = circle1.get_center() + unit_vector * neuron_radius
    end_point = circle2.get_center() - unit_vector * neuron_radius
    return (start_point, end_point)

def get_mlp(line_weight=2.0, line_opacity=0.3):
    INPUT_NEURONS = 5
    HIDDEN_NEURONS = 7
    OUTPUT_NEURONS = 5
    NEURON_RADIUS = 0.2
    LAYER_SPACING = 1.5
    VERTICAL_SPACING = 0.5
    input_layer = VGroup()
    hidden_layer = VGroup()
    output_layer = VGroup()
    dots = VGroup()
    for i in range(INPUT_NEURONS):
        if i == 2:
            dot = Tex('...').rotate(PI / 2, OUT).move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
            neuron.move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            input_layer.add(neuron)
    for i in range(HIDDEN_NEURONS):
        if i == 4:
            dot = Tex('...').rotate(PI / 2, OUT).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
            neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            hidden_layer.add(neuron)
    for i in range(OUTPUT_NEURONS):
        if i == 2:
            dot = Tex('...').rotate(PI / 2, OUT).move_to(RIGHT * LAYER_SPACING + UP * ((OUTPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
            neuron.move_to(RIGHT * LAYER_SPACING + UP * ((OUTPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            output_layer.add(neuron)
    connections = VGroup()
    for in_neuron in input_layer:
        for hidden_neuron in hidden_layer:
            start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
            line = Line(start_point, end_point, stroke_opacity=line_opacity, stroke_width=line_weight)
            connections.add(line)
    for hidden_neuron in hidden_layer:
        for out_neuron in output_layer:
            start_point, end_point = get_edge_points(hidden_neuron, out_neuron, NEURON_RADIUS)
            line = Line(start_point, end_point, stroke_opacity=line_opacity, stroke_width=line_weight)
            connections.add(line)
    return VGroup(connections, input_layer, hidden_layer, output_layer, dots)

def get_transformer_block_gpt(attention_block_width=8, attention_block_height=5, attention_block_depth=1, mlp_block_width=8, mlp_block_height=5, mlp_block_depth=1, block_orig=np.array([0, 0, 0]), line_padding=0.3, residual_compute_block_spacing=11, line_thickness=6, circle_stroke_width=3, plus_stroke_width=3, residual_to_attention_line_spacing=5.0):
    attention_block_1 = create_prism(center=block_orig + np.array([11, -3 - attention_block_depth / 2, 0]), height=attention_block_depth, width=attention_block_width, depth=attention_block_height, face_colors=BLUE, opacity=0.2, label_text='Attention', label_size=80, label_opacity=1.0, label_face='back')
    mlp_block_1 = create_prism(center=block_orig + np.array([11, -12 - mlp_block_depth, 0]), height=mlp_block_depth, width=mlp_block_width, depth=mlp_block_height, face_colors=GREEN, opacity=0.2, label_text='Multilayer Perceptron', label_size=80, label_opacity=1.0, label_face='back')
    a0 = Arrow(start=block_orig + np.array([residual_compute_block_spacing + line_padding, 0, 0]), end=block_orig + np.array([0, 0, 0]), fill_color=WHITE, thickness=line_thickness, tip_width_ratio=0)
    a1 = Arrow(start=block_orig + np.array([residual_compute_block_spacing, 0.3, 0]), end=block_orig + np.array([residual_compute_block_spacing, -3.0, 0]), fill_color=WHITE, thickness=line_thickness)
    a2 = Arrow(start=block_orig + np.array([residual_compute_block_spacing, -3.0 - attention_block_depth, 0]), end=block_orig + np.array([residual_compute_block_spacing, -4.3 - attention_block_depth, 0]), fill_color=WHITE, thickness=line_thickness, tip_width_ratio=0)
    a3 = Arrow(start=block_orig + np.array([residual_compute_block_spacing + line_padding, -4 - attention_block_depth, 0]), end=block_orig + np.array([0.5, -4 - attention_block_depth, 0]), fill_color=WHITE, thickness=line_thickness)
    c = circle_plus(circle_stroke_width=circle_stroke_width, plus_stroke_width=plus_stroke_width, overall_scale=0.6, position=block_orig + np.array([0, -4 - attention_block_depth, 0]))
    a4 = Arrow(start=block_orig + np.array([0, 0, 0]), end=block_orig + np.array([0, -3.5 - attention_block_depth, 0]), fill_color=WHITE, thickness=line_thickness)
    a5 = Arrow(start=block_orig + np.array([0, -4.5 - attention_block_depth, 0]), end=block_orig + np.array([0, -8.5 - attention_block_depth - mlp_block_depth, 0]), fill_color=WHITE, thickness=line_thickness)
    a6 = Arrow(start=block_orig + np.array([residual_compute_block_spacing + line_padding, -6.5 - attention_block_depth, 0]), end=block_orig + np.array([-0.3, -6.5 - attention_block_depth, 0]), fill_color=WHITE, thickness=line_thickness, tip_width_ratio=0)
    a7 = Arrow(start=block_orig + np.array([residual_compute_block_spacing, -6.2 - attention_block_depth, 0]), end=block_orig + np.array([residual_compute_block_spacing, -8 - attention_block_depth, 0]), fill_color=WHITE, thickness=line_thickness)
    a8 = Arrow(start=block_orig + np.array([residual_compute_block_spacing, -8.0 - attention_block_depth - mlp_block_depth, 0]), end=block_orig + np.array([residual_compute_block_spacing, -9.3 - attention_block_depth - mlp_block_depth, 0]), fill_color=WHITE, thickness=line_thickness, tip_width_ratio=0)
    a9 = Arrow(start=block_orig + np.array([residual_compute_block_spacing + line_padding, -9.0 - attention_block_depth - mlp_block_depth, 0]), end=block_orig + np.array([0.5, -9.0 - attention_block_depth - mlp_block_depth, 0]), fill_color=WHITE, thickness=line_thickness)
    c2 = circle_plus(circle_stroke_width=circle_stroke_width, plus_stroke_width=plus_stroke_width, overall_scale=0.6, position=block_orig + np.array([0, -9 - attention_block_depth - mlp_block_depth, 0]))
    a10 = Arrow(start=block_orig + np.array([0, -9.5 - attention_block_depth - mlp_block_depth, 0]), end=block_orig + np.array([0, -11.5 - attention_block_depth - mlp_block_depth, 0]), fill_color=WHITE, thickness=line_thickness)
    return (VGroup(attention_block_1, mlp_block_1, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, c, c2), VGroup(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, c, c2))

def get_attention_first_layer():
    INPUT_NEURONS = 5
    HIDDEN_NEURONS = 5
    OUTPUT_NEURONS = 5
    NEURON_RADIUS = 0.2
    LAYER_SPACING = 1.5
    VERTICAL_SPACING = 0.5
    input_layer = VGroup()
    hidden_layer = VGroup()
    query_layer = VGroup()
    key_layer = VGroup()
    output_layer = VGroup()
    dots = VGroup()
    hidden_dots = VGroup()
    query_dots = VGroup()
    key_dots = VGroup()
    for i in range(INPUT_NEURONS):
        if i == 2:
            dot = Tex('...').rotate(PI / 2, OUT).move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
            neuron.move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
            input_layer.add(neuron)
    for i in range(HIDDEN_NEURONS):
        if i == 2:
            dot = Tex('...').rotate(PI / 2, OUT).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            hidden_dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
            neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            hidden_layer.add(neuron)
    query_shift = 3
    for i in range(HIDDEN_NEURONS):
        if i == 2:
            dot = Tex('...').rotate(PI / 2, OUT).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            dot.shift(query_shift * UP)
            dot.set_color(YELLOW)
            query_dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=YELLOW)
            neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            neuron.shift(query_shift * UP)
            query_layer.add(neuron)
    key_shift = -3
    for i in range(HIDDEN_NEURONS):
        if i == 2:
            dot = Tex('...').rotate(PI / 2, OUT).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            dot.set_color(BLUE)
            dot.shift(key_shift * UP)
            key_dots.add(dot)
        else:
            neuron = Circle(radius=NEURON_RADIUS, stroke_color=BLUE)
            neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
            neuron.shift(key_shift * UP)
            key_layer.add(neuron)
    connections = VGroup()
    for in_neuron in input_layer:
        for hidden_neuron in hidden_layer:
            start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
            line = Line(start_point, end_point, stroke_opacity=0.3, stroke_width=2.0)
            connections.add(line)
        for hidden_neuron in query_layer:
            start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
            line = Line(start_point, end_point, stroke_opacity=0.3, stroke_width=2.0)
            line.set_color(YELLOW)
            connections.add(line)
        for hidden_neuron in key_layer:
            start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
            line = Line(start_point, end_point, stroke_opacity=0.3, stroke_width=2.0)
            line.set_color(BLUE)
            connections.add(line)
    return VGroup(input_layer, hidden_layer, hidden_dots, key_layer, query_layer, dots, key_dots, query_dots, connections)

def random_color_between():
    start = tuple((int(x, 16) for x in ('65', 'c8', 'd0')))
    end = tuple((int(x, 16) for x in ('ff', 'd3', '5a')))
    random_color = tuple((int(start[i] + (end[i] - start[i]) * random.random()) for i in range(3)))
    return '#{:02x}{:02x}{:02x}'.format(*random_color)

def get_attention():
    NEURON_RADIUS = 0.2
    first_layers = []
    hidden_layers = []
    hidden_layers_dots = []
    for i in range(7):
        a = get_attention_first_layer()
        a.shift([0, 0, 5 * i / 11 - 5 / 2])
        first_layers.append(a)
        hidden_layers.append(a[1])
        hidden_layers_dots.append(a[2])
    output_layers = [o.copy() for o in hidden_layers]
    output_dots = [o.copy() for o in hidden_layers_dots]
    for o in output_layers:
        o.shift([3, 0, 0])
    for o in output_dots:
        o.shift([3, 0, 0])
    output_connections = VGroup()
    for i, h in enumerate(hidden_layers):
        for j, o in enumerate(output_layers):
            if i >= j:
                for in_neuron in h:
                    for hidden_neuron in o:
                        start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
                        line = Line(start_point, end_point, stroke_opacity=0.3, stroke_width=2.0)
                        line.set_color(random_color_between())
                        output_connections.add(line)
    return VGroup(VGroup(first_layers), VGroup(output_layers), VGroup(output_dots), output_connections)

class P69_72v3(InteractiveScene):

    def construct(self):
        attention_block_width = 12
        attention_block_height = 5
        attention_block_depth = 8
        mlp_block_width = 8
        mlp_block_height = 5
        mlp_block_depth = 8
        block_orig = np.array([0, 0, 0])
        line_padding = 0.3
        residual_compute_block_spacing = 11
        line_thickness = 6
        circle_stroke_width = 3
        plus_stroke_width = 3
        main_tb, main_tb_lines = get_transformer_block_gpt(block_orig=np.array([0, 0, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
        non_main_tbs = VGroup()
        non_main_tb_lines = VGroup()
        for i in range(-7, 0):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            non_main_tbs.add(tb)
            non_main_tb_lines.add(tb_lines)
        for i in range(1, 8):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            non_main_tbs.add(tb)
            non_main_tb_lines.add(tb_lines)
        for o in [-2, -7, -12]:
            d = Dot([6, -27.5 * 8 + o, 0], radius=1)
            d.set_color(CHILL_BROWN)
            self.add(d)
        for i in range(9, 17):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i + 12, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            non_main_tbs.add(tb)
            non_main_tb_lines.add(tb_lines)
        self.add(main_tb)
        self.add(main_tb_lines)
        self.add(non_main_tbs)
        self.add(non_main_tb_lines)
        self.frame.reorient(-144, 68, 0, (3.42, 6.35, 4.32), 37.33)
        self.wait()
        self.play(self.frame.animate.reorient(-90.18440887882343, 58.711012775757, 0.0, (83.48, -134.0099, -39.85), 457.04), run_time=6.0)
        self.wait()
        self.play(self.frame.animate.reorient(-90, 27, 0, (9.09, -14.74, 0.81), 28.92), run_time=6)
        self.wait()
        self.play(FadeOut(non_main_tbs), FadeOut(non_main_tb_lines), run_time=3)
        self.wait()
        n_stacked_mlps = 7
        mlps = VGroup()
        for i in range(n_stacked_mlps):
            if i < 6:
                mlp = get_mlp(line_weight=2.0, line_opacity=0.3)
                mlp.set_opacity(0.3)
            else:
                mlp = get_mlp(line_weight=3.0, line_opacity=1.0)
            mlp.rotate(PI / 2, IN).scale(2.0)
            mlp.move_to(main_tb[1])
            mlp.shift([0, 0, mlp_block_height * i / float(n_stacked_mlps) - mlp_block_height / 2])
            mlps.add(mlp)
        self.wait()
        self.play(main_tb.animate.set_opacity(0.1), FadeIn(mlps), self.frame.animate.reorient(-90, 19, 0, (10.67, -20.4, 1.78), 15.11), run_time=3)
        self.wait()
        self.play(main_tb.animate.set_opacity(1.0), mlps.animate.set_opacity(0.3), self.frame.animate.reorient(-90, 25, 0, (10.58, -7.19, 0.46), 20.73), run_time=3)
        self.wait()
        att = get_attention()
        att.rotate(PI / 2, IN).scale(1.5)
        att.move_to(main_tb[0])
        self.wait()
        self.play(main_tb.animate.set_opacity(0.1), FadeIn(att), self.frame.animate.reorient(-90, 32, 0, (10.52, -6.99, 0.45), 14.98), run_time=3)
        self.wait()
        self.play(self.frame.animate.reorient(-90, 87, 0, (10.51, -6.99, 0.09), 14.98), run_time=3)
        self.wait()
        self.play(FadeIn(non_main_tbs), FadeIn(non_main_tb_lines), main_tb.animate.set_opacity(0.6), run_time=1)
        self.play(self.frame.animate.reorient(-90.18440887882343, 58.711012775757, 0.0, (83.48, -134.0099, -39.85), 457.04), run_time=6)
        self.wait()
        self.wait(20)

class OpeningHacking(InteractiveScene):

    def construct(self):
        attention_block_width = 12
        attention_block_height = 5
        attention_block_depth = 8
        mlp_block_width = 8
        mlp_block_height = 5
        mlp_block_depth = 8
        block_orig = np.array([0, 0, 0])
        line_padding = 0.3
        residual_compute_block_spacing = 11
        line_thickness = 6
        circle_stroke_width = 3
        plus_stroke_width = 3
        main_tb, main_tb_lines = get_transformer_block_gpt(block_orig=np.array([0, 0, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
        non_main_tbs = VGroup()
        non_main_tb_lines = VGroup()
        for i in range(-7, 0):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            non_main_tbs.add(tb)
            non_main_tb_lines.add(tb_lines)
        for i in range(1, 8):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            non_main_tbs.add(tb)
            non_main_tb_lines.add(tb_lines)
        for o in [-2, -7, -12]:
            d = Dot([6, -27.5 * 8 + o, 0], radius=1)
            d.set_color(CHILL_BROWN)
            self.add(d)
        for i in range(9, 17):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i + 12, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            non_main_tbs.add(tb)
            non_main_tb_lines.add(tb_lines)
        self.add(main_tb)
        self.add(main_tb_lines)
        self.add(non_main_tbs)
        self.add(non_main_tb_lines)
        self.frame.reorient(-144, 68, 0, (3.42, 6.35, 4.32), 37.33)
        self.wait()
        self.play(self.frame.animate.reorient(-90.18440887882343, 58.711012775757, 0.0, (83.48, -134.0099, -39.85), 457.04), run_time=6.0)
        self.wait()
        self.play(self.frame.animate.reorient(-90, 27, 0, (9.09, -14.74, 0.81), 28.92), run_time=6)
        self.wait()
        self.play(FadeOut(non_main_tbs), FadeOut(non_main_tb_lines), run_time=3)
        self.wait()
        n_stacked_mlps = 7
        mlps = VGroup()
        for i in range(n_stacked_mlps):
            if i < 6:
                mlp = get_mlp(line_weight=2.0, line_opacity=0.3)
                mlp.set_opacity(0.3)
            else:
                mlp = get_mlp(line_weight=3.0, line_opacity=1.0)
            mlp.rotate(PI / 2, IN).scale(2.0)
            mlp.move_to(main_tb[1])
            mlp.shift([0, 0, mlp_block_height * i / float(n_stacked_mlps) - mlp_block_height / 2])
            mlps.add(mlp)
        self.wait()
        self.play(main_tb.animate.set_opacity(0.1), FadeIn(mlps), self.frame.animate.reorient(-90, 19, 0, (10.67, -20.4, 1.78), 15.11), run_time=3)
        self.wait()
        self.play(main_tb.animate.set_opacity(1.0), self.frame.animate.reorient(-90, 25, 0, (10.58, -7.19, 0.46), 20.73), run_time=3)
        self.wait()
        att = get_attention()
        att.rotate(PI / 2, IN).scale(1.5)
        att.move_to(main_tb[0])
        self.wait()
        self.play(main_tb.animate.set_opacity(0.1), FadeIn(att), self.frame.animate.reorient(-90, 32, 0, (10.52, -6.99, 0.45), 14.98), run_time=3)
        self.wait()
        self.frame.reorient(-55, 62, 0, (10.11, -12.14, -1.59), 22.56)
        self.wait()
        self.play(self.frame.animate.reorient(-137, 46, 0, (10.11, -12.14, -1.59), 22.56), run_time=5)
        self.wait(20)

class P70Hackin(InteractiveScene):

    def construct(self):
        attention_block_width = 12
        attention_block_height = 5
        attention_block_depth = 8
        mlp_block_width = 8
        mlp_block_height = 5
        mlp_block_depth = 8
        block_orig = np.array([0, 0, 0])
        line_padding = 0.3
        residual_compute_block_spacing = 11
        line_thickness = 6
        circle_stroke_width = 3
        plus_stroke_width = 3
        tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, 0, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
        self.add(tb)
        self.add(tb_lines)
        self.frame.reorient(-90, 1, 0, (7.32, -12.4, -0.31), 23.42)
        self.wait()
        self.frame.reorient(-60, 56, 0, (8.33, -12.23, 0.91), 23.42)
        n_stacked_mlps = 7
        mlps = VGroup()
        for i in range(n_stacked_mlps):
            mlp = get_mlp()
            mlp.rotate(PI / 2, IN).scale(2.0)
            mlp.move_to(tb[1])
            mlp.shift([0, 0, mlp_block_height * i / float(n_stacked_mlps) - mlp_block_height / 2])
            mlps.add(mlp)
        self.add(mlps)
        self.wait()
        att = get_attention()
        self.wait()
        att.rotate(PI / 2, IN).scale(1.5)
        att.move_to(tb[0])
        self.add(att)
        for i in range(-7, 0):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            self.add(tb, tb_lines)
        for i in range(8):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            self.add(tb, tb_lines)
        for o in [-2, -7, -12]:
            d = Dot([6, -27.5 * 8 + o, 0], radius=1)
            d.set_color(CHILL_BROWN)
            self.add(d)
        for i in range(9, 17):
            tb, tb_lines = get_transformer_block_gpt(block_orig=np.array([0, -27.5 * i + 12, 0]), attention_block_depth=attention_block_depth, mlp_block_depth=mlp_block_depth, attention_block_width=attention_block_width)
            self.add(tb, tb_lines)
        self.frame.reorient(-54, 61, 0, (85.42, -259.86, -42.71), 312.62)
        self.wait()

class AttentionHackin2(InteractiveScene):

    def construct(self):
        NEURON_RADIUS = 0.2
        first_layers = []
        hidden_layers = []
        hidden_layers_dots = []
        for i in range(7):
            a = get_attention_first_layer()
            a.shift([0, 0, 5 * i / 7 - 5 / 2])
            first_layers.append(a)
            hidden_layers.append(a[1])
            hidden_layers_dots.append(a[2])
        for a in first_layers:
            self.add(a)
        self.wait()
        output_layers = [o.copy() for o in hidden_layers]
        output_dots = [o.copy() for o in hidden_layers_dots]
        for o in output_layers:
            o.shift([3, 0, 0])
        for o in output_dots:
            o.shift([3, 0, 0])
        for o in output_layers + output_dots:
            self.add(o)
        output_connections = VGroup()
        for i, h in enumerate(hidden_layers):
            for j, o in enumerate(output_layers):
                if i >= j:
                    for in_neuron in h:
                        for hidden_neuron in o:
                            start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
                            line = Line(start_point, end_point, stroke_opacity=0.3, stroke_width=2.0)
                            line.set_color(random_color_between())
                            output_connections.add(line)
        self.add(output_connections)
        self.frame.reorient(0, 0, 0, (2.31, -0.03, 0.0), 9.07)
        self.wait()

class AttentionHacking(InteractiveScene):

    def construct(self):
        INPUT_NEURONS = 5
        HIDDEN_NEURONS = 5
        OUTPUT_NEURONS = 5
        NEURON_RADIUS = 0.2
        LAYER_SPACING = 1.5
        VERTICAL_SPACING = 0.5
        input_layer = VGroup()
        hidden_layer = VGroup()
        output_layer = VGroup()
        dots = VGroup()
        for i in range(INPUT_NEURONS):
            if i == 2:
                dot = Tex('...').rotate(PI / 2, OUT).move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
                dots.add(dot)
            else:
                neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
                neuron.move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
                input_layer.add(neuron)
        for i in range(HIDDEN_NEURONS):
            if i == 2:
                dot = Tex('...').rotate(PI / 2, OUT).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
                dots.add(dot)
            else:
                neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
                neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
                hidden_layer.add(neuron)
        query_shift = 3
        for i in range(HIDDEN_NEURONS):
            if i == 2:
                dot = Tex('...').rotate(PI / 2, OUT).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
                dot.shift(query_shift * UP)
                dots.add(dot)
            else:
                neuron = Circle(radius=NEURON_RADIUS, stroke_color=YELLOW)
                neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
                neuron.shift(query_shift * UP)
                hidden_layer.add(neuron)
        query_shift = -3
        for i in range(HIDDEN_NEURONS):
            if i == 2:
                dot = Tex('...').rotate(PI / 2, OUT).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
                dot.shift(query_shift * UP)
                dots.add(dot)
            else:
                neuron = Circle(radius=NEURON_RADIUS, stroke_color=BLUE)
                neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
                neuron.shift(query_shift * UP)
                hidden_layer.add(neuron)
        connections = VGroup()
        for in_neuron in input_layer:
            for hidden_neuron in hidden_layer:
                start_point, end_point = get_edge_points(in_neuron, hidden_neuron, NEURON_RADIUS)
                line = Line(start_point, end_point, stroke_opacity=0.3, stroke_width=1.5)
                connections.add(line)
        self.add(input_layer, hidden_layer, dots, connections)
        self.frame.reorient(0, 0, 0, (2.31, -0.03, 0.0), 9.07)
        self.wait()

class MLPAloneHacking(InteractiveScene):

    def construct(self):
        INPUT_NEURONS = 5
        HIDDEN_NEURONS = 8
        OUTPUT_NEURONS = 5
        NEURON_RADIUS = 0.2
        LAYER_SPACING = 1.5
        VERTICAL_SPACING = 0.5
        input_layer = VGroup()
        hidden_layer = VGroup()
        output_layer = VGroup()
        dots = VGroup()
        for i in range(INPUT_NEURONS):
            if i == 2:
                dot = Tex('...').rotate(PI / 2, OUT).move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
                dots.add(dot)
            else:
                neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
                neuron.move_to(LEFT * LAYER_SPACING + UP * ((INPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
                input_layer.add(neuron)
        for i in range(HIDDEN_NEURONS):
            if i == 4:
                dot = Tex('...').rotate(PI / 2, OUT).move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
                dots.add(dot)
            else:
                neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
                neuron.move_to(UP * ((HIDDEN_NEURONS // 2 - i) * VERTICAL_SPACING))
                hidden_layer.add(neuron)
        for i in range(OUTPUT_NEURONS):
            if i == 2:
                dot = Tex('...').rotate(PI / 2, OUT).move_to(RIGHT * LAYER_SPACING + UP * ((OUTPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
                dots.add(dot)
            else:
                neuron = Circle(radius=NEURON_RADIUS, stroke_color=WHITE)
                neuron.move_to(RIGHT * LAYER_SPACING + UP * ((OUTPUT_NEURONS // 2 - i) * VERTICAL_SPACING))
                output_layer.add(neuron)
        connections = VGroup()

        def get_edge_points(circle1, circle2):
            direction = circle2.get_center() - circle1.get_center()
            unit_vector = direction / np.linalg.norm(direction)
            start_point = circle1.get_center() + unit_vector * NEURON_RADIUS
            end_point = circle2.get_center() - unit_vector * NEURON_RADIUS
            return (start_point, end_point)
        for in_neuron in input_layer:
            for hidden_neuron in hidden_layer:
                start_point, end_point = get_edge_points(in_neuron, hidden_neuron)
                line = Line(start_point, end_point, stroke_opacity=0.7)
                connections.add(line)
        for hidden_neuron in hidden_layer:
            for out_neuron in output_layer:
                start_point, end_point = get_edge_points(hidden_neuron, out_neuron)
                line = Line(start_point, end_point, stroke_opacity=0.7)
                connections.add(line)
        self.add(connections, input_layer, hidden_layer, output_layer, dots)
        self.wait()