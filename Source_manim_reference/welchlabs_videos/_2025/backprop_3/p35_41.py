from functools import partial
import sys
sys.path.append('_2025/backprop_3')
from geometric_dl_utils import *
from plane_folding_utils import *
from geometric_dl_utils_simplified import *
from polytope_intersection_utils import intersect_polytopes
from manimlib import *
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#6e9671'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
CYAN = '#00FFFF'
graphics_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/graphics/'
colors = [GREY, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]

class LinearPlane(Surface):

    def __init__(self, axes, m1=0.5, m2=0.3, b=1.0, vertical_viz_scale=0.5, **kwargs):
        self.axes = axes
        self.m1 = m1
        self.m2 = m2
        self.b = b
        self.vertical_viz_scale = vertical_viz_scale
        super().__init__(u_range=(-1.0, 1.0), v_range=(-1.0, 1.0), resolution=(64, 64), color='#00FFFF', **kwargs)

    def uv_func(self, u, v):
        x1 = u
        x2 = v
        z = self.vertical_viz_scale * (self.m1 * x1 + self.m2 * x2 + self.b)
        return self.axes.c2p(x1, x2, z)

class LinearPlaneWithGrid(Group):

    def __init__(self, axes, m1=0.5, m2=0.3, b=1.0, vertical_viz_scale=0.5, grid_lines=20, **kwargs):
        super().__init__()
        plane = LinearPlane(axes, m1, m2, b, vertical_viz_scale, **kwargs)
        self.add(plane)
        u_range = (-1.0, 1.0)
        v_range = (-1.0, 1.0)
        for i in range(grid_lines + 1):
            u = u_range[0] + i * (u_range[1] - u_range[0]) / grid_lines
            line_points = []
            for j in range(21):
                v = v_range[0] + j * (v_range[1] - v_range[0]) / 20
                x1, x2 = (u, v)
                z = vertical_viz_scale * (m1 * x1 + m2 * x2 + b)
                line_points.append(axes.c2p(x1, x2, z))
            grid_line = VMobject()
            grid_line.set_points_as_corners(line_points)
            grid_line.set_stroke(WHITE, width=0.5, opacity=0.3)
            self.add(grid_line)
        for i in range(grid_lines + 1):
            v = v_range[0] + i * (v_range[1] - v_range[0]) / grid_lines
            line_points = []
            for j in range(21):
                u = u_range[0] + j * (u_range[1] - u_range[0]) / 20
                x1, x2 = (u, v)
                z = vertical_viz_scale * (m1 * x1 + m2 * x2 + b)
                line_points.append(axes.c2p(x1, x2, z))
            grid_line = VMobject()
            grid_line.set_points_as_corners(line_points)
            grid_line.set_stroke(WHITE, width=0.5, opacity=0.3)
            self.add(grid_line)

class p35_41b(InteractiveScene):

    def construct(self):
        model = BaarleNet([3])
        pickle_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/3_starting_configs_4/training_data_seed_01_acc_0.8561.pkl'
        with open(pickle_path, 'rb') as f:
            p = pickle.load(f)
        print(len(p['weights_history']), ' training steps loaded.')
        viz_scales = [0.2, 0.2, 0.1]
        num_neurons = [3, 3, 2]
        train_step = 7
        w1 = p['weights_history'][train_step]['model.0.weight'].numpy()
        b1 = p['weights_history'][train_step]['model.0.bias'].numpy()
        w2 = p['weights_history'][train_step]['model.2.weight'].numpy()
        b2 = p['weights_history'][train_step]['model.2.bias'].numpy()
        with torch.no_grad():
            model.model[0].weight.copy_(torch.from_numpy(w1))
            model.model[0].bias.copy_(torch.from_numpy(b1))
            model.model[2].weight.copy_(torch.from_numpy(w2))
            model.model[2].bias.copy_(torch.from_numpy(b2))
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                ts.set_shading(0, 0, 0).set_opacity(0.8)
                s.add(ts)
                surface_funcs[-1].append(surface_func)
            surfaces.append(s)
        polygons = {}
        polygons['-1.new_tiling'] = [np.array([[-1.0, -1, 0], [-1, 1, 0], [1, 1, 0], [1, -1, 0]])]
        for layer_id in range(len(model.model) // 2):
            polygons[str(layer_id) + '.linear_out'] = process_with_layers(model.model[:2 * layer_id + 1], polygons[str(layer_id - 1) + '.new_tiling'])
            polygons[str(layer_id) + '.split_polygons_nested'] = split_polygons_with_relu_simple(polygons[str(layer_id) + '.linear_out'])
            polygons[str(layer_id) + '.split_polygons_nested_clipped'] = clip_polygons(polygons[str(layer_id) + '.split_polygons_nested'])
            polygons[str(layer_id) + '.split_polygons_merged'] = merge_zero_regions(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
            polygons[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons[str(layer_id) + '.split_polygons_merged'])
            print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
        polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
        intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
        my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
        joint_points_11 = get_relu_joint(w1[0, 0], w1[0, 1], b1[0], extent=1)
        group_11 = Group(surfaces[1][0])
        if len(joint_points_11) > 0:
            joint_line_11 = line_from_joint_points_1(joint_points_11).set_opacity(0.9)
            group_11.add(joint_line_11)
        group_12 = Group(surfaces[1][1])
        joint_points_12 = get_relu_joint(w1[1, 0], w1[1, 1], b1[1], extent=1)
        if len(joint_points_12) > 0:
            joint_line_12 = line_from_joint_points_1(joint_points_12).set_opacity(0.9)
            group_12.add(joint_line_12)
        group_13 = Group(surfaces[1][2])
        joint_points_13 = get_relu_joint(w1[2, 0], w1[2, 1], b1[2], extent=1)
        if len(joint_points_13) > 0:
            joint_line_13 = line_from_joint_points_1(joint_points_13).set_opacity(0.9)
            group_13.add(joint_line_13)
        group_11.shift([0, 0, 1.5])
        group_13.shift([0, 0, -1.5])
        polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        polygons_21.shift([0, 0, 0.001])
        polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        polygons_22.shift([0, 0, 0.001])
        group_21 = Group(surfaces[2][0], polygons_21)
        group_22 = Group(surfaces[2][1], polygons_22)
        group_21.shift([3.0, 0, 0.6])
        group_22.shift([3.0, 0, -0.6])
        group_21.set_opacity(0.5)
        group_22.set_opacity(0.5)
        group_31 = group_21.copy()
        group_31[1].set_color(BLUE)
        group_31.shift([3, 0, -0.6])
        group_32 = group_22.copy()
        group_32[1].set_color(YELLOW)
        group_32.shift([3, 0, 0.6])
        lines = VGroup()
        for loop in intersection_lines:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines.add(line)
        lines.shift([6, 0, 0])
        group_31[0].set_opacity(0.9)
        group_32[0].set_opacity(0.9)
        self.frame.reorient(-1, 46, 0, (3.09, 0.56, -0.42), 7.25)
        self.add(group_12, group_13)
        self.add(group_21, group_22)
        self.add(group_31, group_32, lines)
        self.add(group_11)
        map_coords_1 = Tex('(0.6, 0.4)', font_size=11).set_color('#FF00FF')
        map_pt_1 = Dot(ORIGIN, radius=0.015).set_color('#FF00FF')
        map_pt_1.move_to([-0.39, 0.12, 0])
        map_coords_1.move_to([-0.4, 0.04, 0])
        coords_group_1 = VGroup(map_pt_1, map_coords_1)
        coords_group_1.scale(2.0)
        coords_group_1.move_to([0.56, 0.22, 1.5])
        coords_group_2 = coords_group_1.copy()
        coords_group_3 = coords_group_1.copy()
        coords_group_2.move_to([0.56, 0.22, 0.0])
        coords_group_3.move_to([0.56, 0.22, -1.5])
        coords_group_4 = coords_group_2.copy()
        coords_group_5 = coords_group_2.copy()
        coords_group_4.shift([3, 0.0, 0.77])
        coords_group_5.shift([3, 0.0, -0.83])
        self.wait()
        self.play(self.frame.animate.reorient(0, 3, 0, (-0.01, 0.19, -0.42), 4.81), group_11.animate.set_opacity(1.0), run_time=4)
        self.wait()
        self.play(Write(coords_group_1[1]), FadeIn(coords_group_1[0]), run_time=2)
        self.wait()
        self.play(self.frame.animate.reorient(-1, 47, 0, (3.25, 0.26, -0.22), 4.15), FadeIn(coords_group_2[0]), FadeIn(coords_group_3[0]), FadeIn(coords_group_5[0]), FadeIn(coords_group_4[0]), Write(coords_group_4[1]), run_time=5.0)
        self.wait()
        outline = polygons_21[0].copy()
        outline.set_fill(opacity=0)
        outline.set_stroke('#FF00FF', width=4, opacity=0.9)
        self.play(ShowCreation(outline, run_time=2))
        self.wait()
        top_polygons_vgroup = VGroup()
        for j, p in enumerate(my_top_polygons):
            if len(p) < 3:
                continue
            if my_indicator[j]:
                color = YELLOW
            else:
                color = BLUE
            p_scaled = copy.deepcopy(p)
            p_scaled[:, 2] = p_scaled[:, 2] * viz_scales[2]
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.5)
            poly_3d.shift([6, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        self.wait()
        outline_2 = top_polygons_vgroup[0].copy()
        outline_2.set_fill(opacity=0)
        outline_2.set_stroke(BLUE, width=2)
        coords_group_6 = coords_group_4.copy()
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (6.15, 0.01, -0.17), 3.55), FadeIn(top_polygons_vgroup), group_31[1].animate.set_opacity(0), group_32[1].animate.set_opacity(0), ReplacementTransform(outline.copy(), outline_2), coords_group_6.animate.shift([3, 0, -0.6]), run_time=3)
        self.remove(lines)
        self.add(lines)
        self.remove(coords_group_6)
        self.add(coords_group_6)
        self.wait()
        self.play(self.frame.animate.reorient(0, 42, 0, (2.99, -0.49, -0.81), 7.09), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(-1, 44, 0, (0.02, -0.84, -1.64), 2.68), run_time=4)
        self.wait()
        axes_1 = ThreeDAxes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], z_range=[-1, 1, 1], width=2, height=2.05, depth=2, axis_config={'color': FRESH_TAN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 4, 'tip_config': {'width': 0.08, 'length': 0.08}})
        w = model.model[0].weight.detach().numpy()
        b = model.model[0].bias.detach().numpy()
        plane_1 = LinearPlane(axes_1, w1[2, 0], w[2, 1], b1[2], vertical_viz_scale=viz_scales[0])
        plane_1.set_opacity(0.5)
        plane_1.set_color('#FF00FF')
        axis_and_plane_31 = Group(axes_1, plane_1)
        axis_and_plane_31.shift([0, 0.02, -1.475 - 0.007])
        self.wait()
        self.play(ShowCreation(plane_1))
        self.wait()
        with open(pickle_path, 'rb') as f:
            p = pickle.load(f)
        train_step = 7 + 10
        w1 = p['weights_history'][train_step]['model.0.weight'].numpy()
        b1 = p['weights_history'][train_step]['model.0.bias'].numpy()
        w2 = p['weights_history'][train_step]['model.2.weight'].numpy()
        b2 = p['weights_history'][train_step]['model.2.bias'].numpy()
        with torch.no_grad():
            model.model[0].weight.copy_(torch.from_numpy(w1))
            model.model[0].bias.copy_(torch.from_numpy(b1))
            model.model[2].weight.copy_(torch.from_numpy(w2))
            model.model[2].bias.copy_(torch.from_numpy(b2))
        surfaces_2 = []
        surface_funcs_2 = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs_2.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                ts.set_shading(0, 0, 0).set_opacity(0.8)
                s.add(ts)
                surface_funcs_2[-1].append(surface_func)
            surfaces_2.append(s)
        polygons_2 = {}
        polygons_2['-1.new_tiling'] = [np.array([[-1.0, -1, 0], [-1, 1, 0], [1, 1, 0], [1, -1, 0]])]
        for layer_id in range(len(model.model) // 2):
            polygons_2[str(layer_id) + '.linear_out'] = process_with_layers(model.model[:2 * layer_id + 1], polygons_2[str(layer_id - 1) + '.new_tiling'])
            polygons_2[str(layer_id) + '.split_polygons_nested'] = split_polygons_with_relu_simple(polygons_2[str(layer_id) + '.linear_out'])
            polygons_2[str(layer_id) + '.split_polygons_nested_clipped'] = clip_polygons(polygons_2[str(layer_id) + '.split_polygons_nested'])
            polygons_2[str(layer_id) + '.split_polygons_merged'] = merge_zero_regions(polygons_2[str(layer_id) + '.split_polygons_nested_clipped'])
            polygons_2[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons_2[str(layer_id) + '.split_polygons_merged'])
            print('Retiled plane into ', str(len(polygons_2[str(layer_id) + '.new_tiling'])), ' polygons_2.')
        polygons_2[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons_2[str(layer_id) + '.new_tiling'])
        intersection_lines_2, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons_2[str(layer_id + 1) + '.linear_out'])
        my_indicator, my_top_polygons_2 = compute_top_polytope(model, new_2d_tiling)
        joint_points_11_2 = get_relu_joint(w1[0, 0], w1[0, 1], b1[0], extent=1)
        group_11_2 = Group(surfaces_2[1][0])
        if len(joint_points_11_2) > 0:
            joint_line_11 = line_from_joint_points_1(joint_points_11_2).set_opacity(0.9)
            group_11_2.add(joint_line_11)
        group_12_2 = Group(surfaces_2[1][1])
        joint_points_12_2 = get_relu_joint(w1[1, 0], w1[1, 1], b1[1], extent=1)
        if len(joint_points_12_2) > 0:
            joint_line_12 = line_from_joint_points_1(joint_points_12_2).set_opacity(0.9)
            group_12_2.add(joint_line_12)
        group_13_2 = Group(surfaces_2[1][2])
        joint_points_13_2 = get_relu_joint(w1[2, 0], w1[2, 1], b1[2], extent=1)
        if len(joint_points_13_2) > 0:
            joint_line_13 = line_from_joint_points_1(joint_points_13_2).set_opacity(0.9)
            group_13_2.add(joint_line_13)
        group_11_2.shift([0, 0, 1.5])
        group_13_2.shift([0, 0, -1.5])
        polygons_21_2 = manim_polygons_from_np_list(polygons_2['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        polygons_21_2.shift([0, 0, 0.001])
        polygons_22_2 = manim_polygons_from_np_list(polygons_2['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        polygons_22_2.shift([0, 0, 0.001])
        group_21_2 = Group(surfaces_2[2][0], polygons_21_2)
        group_22_2 = Group(surfaces_2[2][1], polygons_22_2)
        group_21_2.shift([3.0, 0, 0.6])
        group_22_2.shift([3.0, 0, -0.6])
        group_21_2.set_opacity(0.5)
        group_22_2.set_opacity(0.5)
        group_31_2 = group_21_2.copy()
        group_31_2[1].set_color(BLUE)
        group_31_2.shift([3, 0, -0.6])
        group_32_2 = group_22_2.copy()
        group_32_2[1].set_color(YELLOW)
        group_32_2.shift([3, 0, 0.6])
        lines_2 = VGroup()
        for loop in intersection_lines_2:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines_2.add(line)
        lines_2.shift([6, 0, 0])
        group_31_2[0].set_opacity(0.9)
        group_32_2[0].set_opacity(0.9)
        plane_2 = LinearPlane(axes_1, w1[2, 0], w[2, 1], b1[2], vertical_viz_scale=viz_scales[0])
        plane_2.set_opacity(0.5)
        plane_2.set_color('#FF00FF')
        axis_and_plane_31_2 = Group(axes_1, plane_2)
        plane_2.scale([1, 1.01, 1])
        plane_2.shift([0, 0, 0.002])
        self.wait()
        self.play(ReplacementTransform(plane_1, plane_2), ReplacementTransform(group_13, group_13_2), run_time=1)
        self.remove(plane_2)
        self.add(plane_2)
        self.remove(coords_group_3[0])
        self.add(coords_group_3[0])
        self.wait()
        self.remove(coords_group_1, coords_group_2, coords_group_4, coords_group_5, outline, outline_2)
        self.remove(top_polygons_vgroup)
        group_31[0].set_opacity(0.9)
        group_31[1].set_opacity(0.6)
        group_32[0].set_opacity(0.9)
        group_32[1].set_opacity(0.6)
        self.wait()
        self.play(self.frame.animate.reorient(-1, 55, 0, (2.78, 0.37, -0.29), 6.21), run_time=4)
        self.wait()
        self.remove(group_11, group_12, group_21, group_22)
        self.add(group_11_2, group_12_2, group_21_2, group_22_2)
        self.wait()
        coords_group_7 = coords_group_6.copy()
        coords_group_7.shift([0, 0, -0.03])
        self.remove(group_31, group_32, lines)
        self.add(group_31_2, group_32_2, lines_2)
        self.remove(coords_group_6)
        self.add(coords_group_7)
        self.wait()
        self.wait()

class p36_loop(InteractiveScene):

    def construct(self):
        model = BaarleNet([3])
        pickle_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/3_starting_configs_4/training_data_seed_01_acc_0.8561.pkl'
        with open(pickle_path, 'rb') as f:
            p = pickle.load(f)
        print(len(p['weights_history']), ' training steps loaded.')
        viz_scales = [0.2, 0.2, 0.1]
        num_neurons = [3, 3, 2]
        self.frame.reorient(-1, 55, 0, (2.78, 0.37, -0.29), 6.21)
        start_step = 17
        step_size = 3
        for train_step in np.arange(start_step, len(p['weights_history']), step_size):
            if 'group_12' in locals():
                self.remove(group_12, group_13)
                self.remove(group_21, group_22)
                self.remove(group_31, group_32, lines)
                self.remove(group_11)
            w1 = p['weights_history'][train_step]['model.0.weight'].numpy()
            b1 = p['weights_history'][train_step]['model.0.bias'].numpy()
            w2 = p['weights_history'][train_step]['model.2.weight'].numpy()
            b2 = p['weights_history'][train_step]['model.2.bias'].numpy()
            with torch.no_grad():
                model.model[0].weight.copy_(torch.from_numpy(w1))
                model.model[0].bias.copy_(torch.from_numpy(b1))
                model.model[2].weight.copy_(torch.from_numpy(w2))
                model.model[2].bias.copy_(torch.from_numpy(b2))
            surfaces = []
            surface_funcs = []
            for layer_idx in range(len(model.model)):
                s = Group()
                surface_funcs.append([])
                for neuron_idx in range(num_neurons[layer_idx]):
                    surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                    bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                    ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                    ts.set_shading(0, 0, 0).set_opacity(0.8)
                    s.add(ts)
                    surface_funcs[-1].append(surface_func)
                surfaces.append(s)
            polygons = {}
            polygons['-1.new_tiling'] = [np.array([[-1.0, -1, 0], [-1, 1, 0], [1, 1, 0], [1, -1, 0]])]
            for layer_id in range(len(model.model) // 2):
                polygons[str(layer_id) + '.linear_out'] = process_with_layers(model.model[:2 * layer_id + 1], polygons[str(layer_id - 1) + '.new_tiling'])
                polygons[str(layer_id) + '.split_polygons_nested'] = split_polygons_with_relu_simple(polygons[str(layer_id) + '.linear_out'])
                polygons[str(layer_id) + '.split_polygons_nested_clipped'] = clip_polygons(polygons[str(layer_id) + '.split_polygons_nested'])
                polygons[str(layer_id) + '.split_polygons_merged'] = merge_zero_regions(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                polygons[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons[str(layer_id) + '.split_polygons_merged'])
                print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
            polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
            intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
            my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
            joint_points_11 = get_relu_joint(w1[0, 0], w1[0, 1], b1[0], extent=1)
            group_11 = Group(surfaces[1][0])
            if len(joint_points_11) > 0:
                joint_line_11 = line_from_joint_points_1(joint_points_11).set_opacity(0.9)
                group_11.add(joint_line_11)
            group_12 = Group(surfaces[1][1])
            joint_points_12 = get_relu_joint(w1[1, 0], w1[1, 1], b1[1], extent=1)
            if len(joint_points_12) > 0:
                joint_line_12 = line_from_joint_points_1(joint_points_12).set_opacity(0.9)
                group_12.add(joint_line_12)
            group_13 = Group(surfaces[1][2])
            joint_points_13 = get_relu_joint(w1[2, 0], w1[2, 1], b1[2], extent=1)
            if len(joint_points_13) > 0:
                joint_line_13 = line_from_joint_points_1(joint_points_13).set_opacity(0.9)
                group_13.add(joint_line_13)
            group_11.shift([0, 0, 1.5])
            group_13.shift([0, 0, -1.5])
            polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
            polygons_21.shift([0, 0, 0.001])
            polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
            polygons_22.shift([0, 0, 0.001])
            group_21 = Group(surfaces[2][0], polygons_21)
            group_22 = Group(surfaces[2][1], polygons_22)
            group_21.shift([3.0, 0, 0.6])
            group_22.shift([3.0, 0, -0.6])
            group_21.set_opacity(0.5)
            group_22.set_opacity(0.5)
            group_31 = group_21.copy()
            group_31[1].set_color(BLUE)
            group_31.shift([3, 0, -0.6])
            group_32 = group_22.copy()
            group_32[1].set_color(YELLOW)
            group_32.shift([3, 0, 0.6])
            lines = VGroup()
            for loop in intersection_lines:
                loop = loop * np.array([1, 1, viz_scales[2]])
                line = VMobject()
                line.set_points_as_corners(loop)
                line.set_stroke(color='#FF00FF', width=5)
                lines.add(line)
            lines.shift([6, 0, 0])
            group_31[0].set_opacity(0.9)
            group_32[0].set_opacity(0.9)
            self.add(group_12, group_13)
            self.add(group_21, group_22)
            self.add(group_31, group_32, lines)
            self.add(group_11)
            self.wait(0.1)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (6.12, 0.0, -0.3), 3.43))
        self.wait(20)
        self.embed()

class p36_train_end_zoom_border_and_back(InteractiveScene):

    def construct(self):
        model = BaarleNet([3])
        pickle_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/3_starting_configs_4/training_data_seed_01_acc_0.8561.pkl'
        with open(pickle_path, 'rb') as f:
            p = pickle.load(f)
        print(len(p['weights_history']), ' training steps loaded.')
        viz_scales = [0.2, 0.2, 0.1]
        num_neurons = [3, 3, 2]
        self.frame.reorient(-1, 55, 0, (2.78, 0.37, -0.29), 6.21)
        start_step = 17
        step_size = 3
        train_step = len(p['weights_history']) - 1
        if 'group_12' in locals():
            self.remove(group_12, group_13)
            self.remove(group_21, group_22)
            self.remove(group_31, group_32, lines)
            self.remove(group_11)
        w1 = p['weights_history'][train_step]['model.0.weight'].numpy()
        b1 = p['weights_history'][train_step]['model.0.bias'].numpy()
        w2 = p['weights_history'][train_step]['model.2.weight'].numpy()
        b2 = p['weights_history'][train_step]['model.2.bias'].numpy()
        with torch.no_grad():
            model.model[0].weight.copy_(torch.from_numpy(w1))
            model.model[0].bias.copy_(torch.from_numpy(b1))
            model.model[2].weight.copy_(torch.from_numpy(w2))
            model.model[2].bias.copy_(torch.from_numpy(b2))
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                ts.set_shading(0, 0, 0).set_opacity(0.8)
                s.add(ts)
                surface_funcs[-1].append(surface_func)
            surfaces.append(s)
        polygons = {}
        polygons['-1.new_tiling'] = [np.array([[-1.0, -1, 0], [-1, 1, 0], [1, 1, 0], [1, -1, 0]])]
        for layer_id in range(len(model.model) // 2):
            polygons[str(layer_id) + '.linear_out'] = process_with_layers(model.model[:2 * layer_id + 1], polygons[str(layer_id - 1) + '.new_tiling'])
            polygons[str(layer_id) + '.split_polygons_nested'] = split_polygons_with_relu_simple(polygons[str(layer_id) + '.linear_out'])
            polygons[str(layer_id) + '.split_polygons_nested_clipped'] = clip_polygons(polygons[str(layer_id) + '.split_polygons_nested'])
            polygons[str(layer_id) + '.split_polygons_merged'] = merge_zero_regions(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
            polygons[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons[str(layer_id) + '.split_polygons_merged'])
            print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
        polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
        intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
        my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
        joint_points_11 = get_relu_joint(w1[0, 0], w1[0, 1], b1[0], extent=1)
        group_11 = Group(surfaces[1][0])
        if len(joint_points_11) > 0:
            joint_line_11 = line_from_joint_points_1(joint_points_11).set_opacity(0.9)
            group_11.add(joint_line_11)
        group_12 = Group(surfaces[1][1])
        joint_points_12 = get_relu_joint(w1[1, 0], w1[1, 1], b1[1], extent=1)
        if len(joint_points_12) > 0:
            joint_line_12 = line_from_joint_points_1(joint_points_12).set_opacity(0.9)
            group_12.add(joint_line_12)
        group_13 = Group(surfaces[1][2])
        joint_points_13 = get_relu_joint(w1[2, 0], w1[2, 1], b1[2], extent=1)
        if len(joint_points_13) > 0:
            joint_line_13 = line_from_joint_points_1(joint_points_13).set_opacity(0.9)
            group_13.add(joint_line_13)
        group_11.shift([0, 0, 1.5])
        group_13.shift([0, 0, -1.5])
        polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        polygons_21.shift([0, 0, 0.001])
        polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        polygons_22.shift([0, 0, 0.001])
        group_21 = Group(surfaces[2][0], polygons_21)
        group_22 = Group(surfaces[2][1], polygons_22)
        group_21.shift([3.0, 0, 0.6])
        group_22.shift([3.0, 0, -0.6])
        group_21.set_opacity(0.5)
        group_22.set_opacity(0.5)
        group_31 = group_21.copy()
        group_31[1].set_color(BLUE)
        group_31.shift([3, 0, -0.6])
        group_32 = group_22.copy()
        group_32[1].set_color(YELLOW)
        group_32.shift([3, 0, 0.6])
        lines = VGroup()
        for loop in intersection_lines:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines.add(line)
        lines.shift([6, 0, 0])
        group_31[0].set_opacity(0.9)
        group_32[0].set_opacity(0.9)
        self.add(group_12, group_13)
        self.add(group_21, group_22)
        self.add(group_31, group_32, lines)
        self.add(group_11)
        self.wait(0.1)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (6.12, 0.0, -0.3), 3.43), run_time=5)
        self.wait()
        self.play(self.frame.animate.reorient(-1, 55, 0, (2.78, 0.37, -0.29), 6.21), run_time=5)
        self.wait(20)
        self.embed()

class p36_loop_2(InteractiveScene):

    def construct(self):
        model = BaarleNet([3])
        pickle_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/3_starting_configs_4/training_data_seed_32_acc_0.6159.pkl'
        with open(pickle_path, 'rb') as f:
            p = pickle.load(f)
        print(len(p['weights_history']), ' training steps loaded.')
        viz_scales = [0.2, 0.2, 0.1]
        num_neurons = [3, 3, 2]
        self.frame.reorient(-1, 55, 0, (2.78, 0.37, -0.29), 6.21)
        start_step = 0
        step_size = 3
        for train_step in np.arange(start_step, len(p['weights_history']), step_size):
            if 'group_12' in locals():
                self.remove(group_12, group_13)
                self.remove(group_21, group_22)
                self.remove(group_31, group_32, lines)
                self.remove(group_11)
            w1 = p['weights_history'][train_step]['model.0.weight'].numpy()
            b1 = p['weights_history'][train_step]['model.0.bias'].numpy()
            w2 = p['weights_history'][train_step]['model.2.weight'].numpy()
            b2 = p['weights_history'][train_step]['model.2.bias'].numpy()
            with torch.no_grad():
                model.model[0].weight.copy_(torch.from_numpy(w1))
                model.model[0].bias.copy_(torch.from_numpy(b1))
                model.model[2].weight.copy_(torch.from_numpy(w2))
                model.model[2].bias.copy_(torch.from_numpy(b2))
            surfaces = []
            surface_funcs = []
            for layer_idx in range(len(model.model)):
                s = Group()
                surface_funcs.append([])
                for neuron_idx in range(num_neurons[layer_idx]):
                    surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                    bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                    ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                    ts.set_shading(0, 0, 0).set_opacity(0.8)
                    s.add(ts)
                    surface_funcs[-1].append(surface_func)
                surfaces.append(s)
            polygons = {}
            polygons['-1.new_tiling'] = [np.array([[-1.0, -1, 0], [-1, 1, 0], [1, 1, 0], [1, -1, 0]])]
            for layer_id in range(len(model.model) // 2):
                polygons[str(layer_id) + '.linear_out'] = process_with_layers(model.model[:2 * layer_id + 1], polygons[str(layer_id - 1) + '.new_tiling'])
                polygons[str(layer_id) + '.split_polygons_nested'] = split_polygons_with_relu_simple(polygons[str(layer_id) + '.linear_out'])
                polygons[str(layer_id) + '.split_polygons_nested_clipped'] = clip_polygons(polygons[str(layer_id) + '.split_polygons_nested'])
                polygons[str(layer_id) + '.split_polygons_merged'] = merge_zero_regions(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                polygons[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons[str(layer_id) + '.split_polygons_merged'])
                print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
            polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
            intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
            my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
            joint_points_11 = get_relu_joint(w1[0, 0], w1[0, 1], b1[0], extent=1)
            group_11 = Group(surfaces[1][0])
            if len(joint_points_11) > 0:
                joint_line_11 = line_from_joint_points_1(joint_points_11).set_opacity(0.9)
                group_11.add(joint_line_11)
            group_12 = Group(surfaces[1][1])
            joint_points_12 = get_relu_joint(w1[1, 0], w1[1, 1], b1[1], extent=1)
            if len(joint_points_12) > 0:
                joint_line_12 = line_from_joint_points_1(joint_points_12).set_opacity(0.9)
                group_12.add(joint_line_12)
            group_13 = Group(surfaces[1][2])
            joint_points_13 = get_relu_joint(w1[2, 0], w1[2, 1], b1[2], extent=1)
            if len(joint_points_13) > 0:
                joint_line_13 = line_from_joint_points_1(joint_points_13).set_opacity(0.9)
                group_13.add(joint_line_13)
            group_11.shift([0, 0, 1.5])
            group_13.shift([0, 0, -1.5])
            polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
            polygons_21.shift([0, 0, 0.001])
            polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
            polygons_22.shift([0, 0, 0.001])
            group_21 = Group(surfaces[2][0], polygons_21)
            group_22 = Group(surfaces[2][1], polygons_22)
            group_21.shift([3.0, 0, 0.6])
            group_22.shift([3.0, 0, -0.6])
            group_21.set_opacity(0.5)
            group_22.set_opacity(0.5)
            group_31 = group_21.copy()
            group_31[1].set_color(BLUE)
            group_31.shift([3, 0, -0.6])
            group_32 = group_22.copy()
            group_32[1].set_color(YELLOW)
            group_32.shift([3, 0, 0.6])
            lines = VGroup()
            for loop in intersection_lines:
                loop = loop * np.array([1, 1, viz_scales[2]])
                line = VMobject()
                line.set_points_as_corners(loop)
                line.set_stroke(color='#FF00FF', width=5)
                lines.add(line)
            lines.shift([6, 0, 0])
            group_31[0].set_opacity(0.9)
            group_32[0].set_opacity(0.9)
            self.add(group_12, group_13)
            self.add(group_21, group_22)
            self.add(group_31, group_32, lines)
            self.add(group_11)
            self.wait(0.1)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (6.12, 0.0, -0.3), 3.43))
        self.wait(20)
        self.embed()