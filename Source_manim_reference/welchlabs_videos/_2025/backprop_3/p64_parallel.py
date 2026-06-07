from functools import partial
import sys
sys.path.append('_2025/backprop_3')
from geometric_dl_utils import *
from plane_folding_utils import *
from geometric_dl_utils_simplified import *
from polytope_intersection_utils import intersect_polytopes
from manimlib import *
from tqdm import tqdm
from order_matching_tools import reorder_polygons_optimal, reorder_polygons_greedy
from gap_filler import fill_gaps
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
colors = [BLUE, GREY, GREEN, TEAL, PURPLE, PINK, TEAL, YELLOW, FRESH_TAN, CHILL_BLUE, CHILL_GREEN, YELLOW_FADE]

class p64_a_2201_start(InteractiveScene):

    def construct(self):
        model = BaarleNet([32, 32, 32, 32])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [32, 32, 32, 32, 32, 32, 32, 32, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/32_32_32_32_1.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        prev_layer_4_polygons = None
        self.frame.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04)
        for train_step in tqdm(list(range(2201, 2401, 10))):
            try:
                if 'layer_1_polygons_flat' in locals():
                    self.remove(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, layer_4_polygons_flat, final_map_group, border_map_only)
                w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
                b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
                w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
                b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
                w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
                b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
                w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
                b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
                w5 = training_cache['weights_history'][train_step]['model.8.weight'].numpy()
                b5 = training_cache['weights_history'][train_step]['model.8.bias'].numpy()
                with torch.no_grad():
                    model.model[0].weight.copy_(torch.from_numpy(w1))
                    model.model[0].bias.copy_(torch.from_numpy(b1))
                    model.model[2].weight.copy_(torch.from_numpy(w2))
                    model.model[2].bias.copy_(torch.from_numpy(b2))
                    model.model[4].weight.copy_(torch.from_numpy(w3))
                    model.model[4].bias.copy_(torch.from_numpy(b3))
                    model.model[6].weight.copy_(torch.from_numpy(w4))
                    model.model[6].bias.copy_(torch.from_numpy(b4))
                    model.model[8].weight.copy_(torch.from_numpy(w5))
                    model.model[8].bias.copy_(torch.from_numpy(b5))
                adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
                final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
                adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
                surfaces = []
                surface_funcs = []
                for layer_idx in range(len(model.model)):
                    s = Group()
                    surface_funcs.append([])
                    if layer_idx > 7:
                        for neuron_idx in range(num_neurons[layer_idx]):
                            surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx])
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
                    polygons[str(layer_id) + '.new_tiling_nested'] = recompute_tiling_polygonize(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                    polygons[str(layer_id) + '.new_tiling'] = [item for sublist in polygons[str(layer_id) + '.new_tiling_nested'] for item in sublist]
                    print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
                polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
                intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
                my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
                print(len(my_top_polygons), len(my_indicator))
                my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
                print(len(my_top_polygons), len(my_indicator))
                if prev_layer_1_polygons is not None:
                    prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
                else:
                    prev_layer_1_polygons = polygons['0.new_tiling']
                layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_2_polygons is not None:
                    prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
                else:
                    prev_layer_2_polygons = polygons['1.new_tiling']
                layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_3_polygons is not None:
                    prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
                else:
                    prev_layer_3_polygons = polygons['2.new_tiling']
                layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_4_polygons is not None:
                    prev_layer_4_polygons = reorder_polygons_optimal(prev_layer_4_polygons, polygons['3.new_tiling'])
                else:
                    prev_layer_4_polygons = polygons['3.new_tiling']
                layer_4_polygons_flat = manim_polygons_from_np_list(prev_layer_4_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                groups_output = Group()
                layer_idx = len(model.model) - 1
                total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
                start_z = total_height / 2
                for neuron_idx in range(num_neurons[layer_idx]):
                    pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
                    s = surfaces[layer_idx][neuron_idx]
                    g = Group(s, pgs)
                    groups_output.add(g)
                group_combined_output = groups_output.copy()
                group_combined_output[0].set_color(BLUE)
                group_combined_output[1].set_color(YELLOW)
                top_polygons_vgroup = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = p_scaled[:, 2] * adaptive_viz_scales[-1][0]
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup.add(poly_3d)
                lines = VGroup()
                for loop in intersection_lines:
                    loop = loop * np.array([1, 1, viz_scales[2]])
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines.add(line)
                top_polygons_vgroup_flat = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = 0
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup_flat.add(poly_3d)

                def flat_surf_func(u, v):
                    return [u, v, 0]
                flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
                lines_flat = VGroup()
                for loop in intersection_lines:
                    loop[:, 2] = 0
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines_flat.add(line)
                group_combined_output.set_opacity(0.3)
                final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
                border_map_only = Group(flat_map_2.copy(), lines_flat.copy())
                layer_1_polygons_flat.shift([0.0, 2.0, 0.0])
                layer_2_polygons_flat.shift([2.35, 2.0, 0.0])
                layer_3_polygons_flat.shift([0.0, -0.35, 0.0])
                layer_4_polygons_flat.shift([2.35, -0.35, 0.0])
                final_map_group.shift([2 * 2.35, 2, 0.0])
                border_map_only.shift([2 * 2.35, -0.35, 0.0])
                self.frame.reorient(0, 0, 0, (2.97, 0.81, 0.0), 4.8)
                self.add(layer_1_polygons_flat)
                self.add(layer_2_polygons_flat)
                self.add(layer_3_polygons_flat)
                self.add(layer_4_polygons_flat)
                self.add(final_map_group)
                self.add(border_map_only)
                self.wait(0.1)
            except Exception as e:
                print(f'Skipping frame, Error occurred: {e}')
        self.wait(20)
        self.embed()

class p64_b_2401_start(InteractiveScene):

    def construct(self):
        model = BaarleNet([32, 32, 32, 32])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [32, 32, 32, 32, 32, 32, 32, 32, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/32_32_32_32_1.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        prev_layer_4_polygons = None
        self.frame.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04)
        for train_step in tqdm(list(range(2401, 2601, 10))):
            try:
                if 'layer_1_polygons_flat' in locals():
                    self.remove(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, layer_4_polygons_flat, final_map_group, border_map_only)
                w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
                b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
                w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
                b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
                w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
                b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
                w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
                b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
                w5 = training_cache['weights_history'][train_step]['model.8.weight'].numpy()
                b5 = training_cache['weights_history'][train_step]['model.8.bias'].numpy()
                with torch.no_grad():
                    model.model[0].weight.copy_(torch.from_numpy(w1))
                    model.model[0].bias.copy_(torch.from_numpy(b1))
                    model.model[2].weight.copy_(torch.from_numpy(w2))
                    model.model[2].bias.copy_(torch.from_numpy(b2))
                    model.model[4].weight.copy_(torch.from_numpy(w3))
                    model.model[4].bias.copy_(torch.from_numpy(b3))
                    model.model[6].weight.copy_(torch.from_numpy(w4))
                    model.model[6].bias.copy_(torch.from_numpy(b4))
                    model.model[8].weight.copy_(torch.from_numpy(w5))
                    model.model[8].bias.copy_(torch.from_numpy(b5))
                adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
                final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
                adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
                surfaces = []
                surface_funcs = []
                for layer_idx in range(len(model.model)):
                    s = Group()
                    surface_funcs.append([])
                    if layer_idx > 7:
                        for neuron_idx in range(num_neurons[layer_idx]):
                            surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx])
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
                    polygons[str(layer_id) + '.new_tiling_nested'] = recompute_tiling_polygonize(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                    polygons[str(layer_id) + '.new_tiling'] = [item for sublist in polygons[str(layer_id) + '.new_tiling_nested'] for item in sublist]
                    print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
                polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
                intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
                my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
                print(len(my_top_polygons), len(my_indicator))
                my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
                print(len(my_top_polygons), len(my_indicator))
                if prev_layer_1_polygons is not None:
                    prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
                else:
                    prev_layer_1_polygons = polygons['0.new_tiling']
                layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_2_polygons is not None:
                    prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
                else:
                    prev_layer_2_polygons = polygons['1.new_tiling']
                layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_3_polygons is not None:
                    prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
                else:
                    prev_layer_3_polygons = polygons['2.new_tiling']
                layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_4_polygons is not None:
                    prev_layer_4_polygons = reorder_polygons_optimal(prev_layer_4_polygons, polygons['3.new_tiling'])
                else:
                    prev_layer_4_polygons = polygons['3.new_tiling']
                layer_4_polygons_flat = manim_polygons_from_np_list(prev_layer_4_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                groups_output = Group()
                layer_idx = len(model.model) - 1
                total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
                start_z = total_height / 2
                for neuron_idx in range(num_neurons[layer_idx]):
                    pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
                    s = surfaces[layer_idx][neuron_idx]
                    g = Group(s, pgs)
                    groups_output.add(g)
                group_combined_output = groups_output.copy()
                group_combined_output[0].set_color(BLUE)
                group_combined_output[1].set_color(YELLOW)
                top_polygons_vgroup = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = p_scaled[:, 2] * adaptive_viz_scales[-1][0]
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup.add(poly_3d)
                lines = VGroup()
                for loop in intersection_lines:
                    loop = loop * np.array([1, 1, viz_scales[2]])
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines.add(line)
                top_polygons_vgroup_flat = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = 0
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup_flat.add(poly_3d)

                def flat_surf_func(u, v):
                    return [u, v, 0]
                flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
                lines_flat = VGroup()
                for loop in intersection_lines:
                    loop[:, 2] = 0
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines_flat.add(line)
                group_combined_output.set_opacity(0.3)
                final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
                border_map_only = Group(flat_map_2.copy(), lines_flat.copy())
                layer_1_polygons_flat.shift([0.0, 2.0, 0.0])
                layer_2_polygons_flat.shift([2.35, 2.0, 0.0])
                layer_3_polygons_flat.shift([0.0, -0.35, 0.0])
                layer_4_polygons_flat.shift([2.35, -0.35, 0.0])
                final_map_group.shift([2 * 2.35, 2, 0.0])
                border_map_only.shift([2 * 2.35, -0.35, 0.0])
                self.frame.reorient(0, 0, 0, (2.97, 0.81, 0.0), 4.8)
                self.add(layer_1_polygons_flat)
                self.add(layer_2_polygons_flat)
                self.add(layer_3_polygons_flat)
                self.add(layer_4_polygons_flat)
                self.add(final_map_group)
                self.add(border_map_only)
                self.wait(0.1)
            except Exception as e:
                print(f'Skipping frame, Error occurred: {e}')
        self.wait(20)
        self.embed()

class p64_c_600_start(InteractiveScene):

    def construct(self):
        model = BaarleNet([32, 32, 32, 32])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [32, 32, 32, 32, 32, 32, 32, 32, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/32_32_32_32_1.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        prev_layer_4_polygons = None
        self.frame.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04)
        for train_step in tqdm(list(range(600, 1000, 10))):
            try:
                if 'layer_1_polygons_flat' in locals():
                    self.remove(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, layer_4_polygons_flat, final_map_group, border_map_only)
                w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
                b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
                w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
                b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
                w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
                b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
                w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
                b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
                w5 = training_cache['weights_history'][train_step]['model.8.weight'].numpy()
                b5 = training_cache['weights_history'][train_step]['model.8.bias'].numpy()
                with torch.no_grad():
                    model.model[0].weight.copy_(torch.from_numpy(w1))
                    model.model[0].bias.copy_(torch.from_numpy(b1))
                    model.model[2].weight.copy_(torch.from_numpy(w2))
                    model.model[2].bias.copy_(torch.from_numpy(b2))
                    model.model[4].weight.copy_(torch.from_numpy(w3))
                    model.model[4].bias.copy_(torch.from_numpy(b3))
                    model.model[6].weight.copy_(torch.from_numpy(w4))
                    model.model[6].bias.copy_(torch.from_numpy(b4))
                    model.model[8].weight.copy_(torch.from_numpy(w5))
                    model.model[8].bias.copy_(torch.from_numpy(b5))
                adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
                final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
                adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
                surfaces = []
                surface_funcs = []
                for layer_idx in range(len(model.model)):
                    s = Group()
                    surface_funcs.append([])
                    if layer_idx > 7:
                        for neuron_idx in range(num_neurons[layer_idx]):
                            surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx])
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
                    polygons[str(layer_id) + '.new_tiling_nested'] = recompute_tiling_polygonize(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                    polygons[str(layer_id) + '.new_tiling'] = [item for sublist in polygons[str(layer_id) + '.new_tiling_nested'] for item in sublist]
                    print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
                polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
                intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
                my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
                print(len(my_top_polygons), len(my_indicator))
                my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
                print(len(my_top_polygons), len(my_indicator))
                if prev_layer_1_polygons is not None:
                    prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
                else:
                    prev_layer_1_polygons = polygons['0.new_tiling']
                layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_2_polygons is not None:
                    prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
                else:
                    prev_layer_2_polygons = polygons['1.new_tiling']
                layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_3_polygons is not None:
                    prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
                else:
                    prev_layer_3_polygons = polygons['2.new_tiling']
                layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_4_polygons is not None:
                    prev_layer_4_polygons = reorder_polygons_optimal(prev_layer_4_polygons, polygons['3.new_tiling'])
                else:
                    prev_layer_4_polygons = polygons['3.new_tiling']
                layer_4_polygons_flat = manim_polygons_from_np_list(prev_layer_4_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                groups_output = Group()
                layer_idx = len(model.model) - 1
                total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
                start_z = total_height / 2
                for neuron_idx in range(num_neurons[layer_idx]):
                    pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
                    s = surfaces[layer_idx][neuron_idx]
                    g = Group(s, pgs)
                    groups_output.add(g)
                group_combined_output = groups_output.copy()
                group_combined_output[0].set_color(BLUE)
                group_combined_output[1].set_color(YELLOW)
                top_polygons_vgroup = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = p_scaled[:, 2] * adaptive_viz_scales[-1][0]
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup.add(poly_3d)
                lines = VGroup()
                for loop in intersection_lines:
                    loop = loop * np.array([1, 1, viz_scales[2]])
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines.add(line)
                top_polygons_vgroup_flat = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = 0
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup_flat.add(poly_3d)

                def flat_surf_func(u, v):
                    return [u, v, 0]
                flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
                lines_flat = VGroup()
                for loop in intersection_lines:
                    loop[:, 2] = 0
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines_flat.add(line)
                group_combined_output.set_opacity(0.3)
                final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
                border_map_only = Group(flat_map_2.copy(), lines_flat.copy())
                layer_1_polygons_flat.shift([0.0, 2.0, 0.0])
                layer_2_polygons_flat.shift([2.35, 2.0, 0.0])
                layer_3_polygons_flat.shift([0.0, -0.35, 0.0])
                layer_4_polygons_flat.shift([2.35, -0.35, 0.0])
                final_map_group.shift([2 * 2.35, 2, 0.0])
                border_map_only.shift([2 * 2.35, -0.35, 0.0])
                self.frame.reorient(0, 0, 0, (2.97, 0.81, 0.0), 4.8)
                self.add(layer_1_polygons_flat)
                self.add(layer_2_polygons_flat)
                self.add(layer_3_polygons_flat)
                self.add(layer_4_polygons_flat)
                self.add(final_map_group)
                self.add(border_map_only)
                self.wait(0.1)
            except Exception as e:
                print(f'Skipping frame, Error occurred: {e}')
        self.wait(20)
        self.embed()

class p64_d_900_start(InteractiveScene):

    def construct(self):
        model = BaarleNet([32, 32, 32, 32])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [32, 32, 32, 32, 32, 32, 32, 32, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/32_32_32_32_1.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        prev_layer_4_polygons = None
        self.frame.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04)
        for train_step in tqdm(list(range(900, 2100, 10))):
            try:
                if 'layer_1_polygons_flat' in locals():
                    self.remove(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, layer_4_polygons_flat, final_map_group, border_map_only)
                w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
                b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
                w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
                b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
                w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
                b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
                w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
                b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
                w5 = training_cache['weights_history'][train_step]['model.8.weight'].numpy()
                b5 = training_cache['weights_history'][train_step]['model.8.bias'].numpy()
                with torch.no_grad():
                    model.model[0].weight.copy_(torch.from_numpy(w1))
                    model.model[0].bias.copy_(torch.from_numpy(b1))
                    model.model[2].weight.copy_(torch.from_numpy(w2))
                    model.model[2].bias.copy_(torch.from_numpy(b2))
                    model.model[4].weight.copy_(torch.from_numpy(w3))
                    model.model[4].bias.copy_(torch.from_numpy(b3))
                    model.model[6].weight.copy_(torch.from_numpy(w4))
                    model.model[6].bias.copy_(torch.from_numpy(b4))
                    model.model[8].weight.copy_(torch.from_numpy(w5))
                    model.model[8].bias.copy_(torch.from_numpy(b5))
                adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
                final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
                adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
                surfaces = []
                surface_funcs = []
                for layer_idx in range(len(model.model)):
                    s = Group()
                    surface_funcs.append([])
                    if layer_idx > 7:
                        for neuron_idx in range(num_neurons[layer_idx]):
                            surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx])
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
                    polygons[str(layer_id) + '.new_tiling_nested'] = recompute_tiling_polygonize(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                    polygons[str(layer_id) + '.new_tiling'] = [item for sublist in polygons[str(layer_id) + '.new_tiling_nested'] for item in sublist]
                    print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
                polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
                intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
                my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
                print(len(my_top_polygons), len(my_indicator))
                my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
                print(len(my_top_polygons), len(my_indicator))
                if prev_layer_1_polygons is not None:
                    prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
                else:
                    prev_layer_1_polygons = polygons['0.new_tiling']
                layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_2_polygons is not None:
                    prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
                else:
                    prev_layer_2_polygons = polygons['1.new_tiling']
                layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_3_polygons is not None:
                    prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
                else:
                    prev_layer_3_polygons = polygons['2.new_tiling']
                layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_4_polygons is not None:
                    prev_layer_4_polygons = reorder_polygons_optimal(prev_layer_4_polygons, polygons['3.new_tiling'])
                else:
                    prev_layer_4_polygons = polygons['3.new_tiling']
                layer_4_polygons_flat = manim_polygons_from_np_list(prev_layer_4_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                groups_output = Group()
                layer_idx = len(model.model) - 1
                total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
                start_z = total_height / 2
                for neuron_idx in range(num_neurons[layer_idx]):
                    pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
                    s = surfaces[layer_idx][neuron_idx]
                    g = Group(s, pgs)
                    groups_output.add(g)
                group_combined_output = groups_output.copy()
                group_combined_output[0].set_color(BLUE)
                group_combined_output[1].set_color(YELLOW)
                top_polygons_vgroup = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = p_scaled[:, 2] * adaptive_viz_scales[-1][0]
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup.add(poly_3d)
                lines = VGroup()
                for loop in intersection_lines:
                    loop = loop * np.array([1, 1, viz_scales[2]])
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines.add(line)
                top_polygons_vgroup_flat = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = 0
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup_flat.add(poly_3d)

                def flat_surf_func(u, v):
                    return [u, v, 0]
                flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
                lines_flat = VGroup()
                for loop in intersection_lines:
                    loop[:, 2] = 0
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines_flat.add(line)
                group_combined_output.set_opacity(0.3)
                final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
                border_map_only = Group(flat_map_2.copy(), lines_flat.copy())
                layer_1_polygons_flat.shift([0.0, 2.0, 0.0])
                layer_2_polygons_flat.shift([2.35, 2.0, 0.0])
                layer_3_polygons_flat.shift([0.0, -0.35, 0.0])
                layer_4_polygons_flat.shift([2.35, -0.35, 0.0])
                final_map_group.shift([2 * 2.35, 2, 0.0])
                border_map_only.shift([2 * 2.35, -0.35, 0.0])
                self.frame.reorient(0, 0, 0, (2.97, 0.81, 0.0), 4.8)
                self.add(layer_1_polygons_flat)
                self.add(layer_2_polygons_flat)
                self.add(layer_3_polygons_flat)
                self.add(layer_4_polygons_flat)
                self.add(final_map_group)
                self.add(border_map_only)
                self.wait(0.1)
            except Exception as e:
                print(f'Skipping frame, Error occurred: {e}')
        self.wait(20)
        self.embed()

class p64_e(InteractiveScene):

    def construct(self):
        model = BaarleNet([32, 32, 32, 32])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [32, 32, 32, 32, 32, 32, 32, 32, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/32_32_32_32_1.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        prev_layer_4_polygons = None
        self.frame.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04)
        for train_step in tqdm(list(range(1700, 1900, 10))):
            try:
                if 'layer_1_polygons_flat' in locals():
                    self.remove(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, layer_4_polygons_flat, final_map_group, border_map_only)
                w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
                b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
                w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
                b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
                w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
                b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
                w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
                b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
                w5 = training_cache['weights_history'][train_step]['model.8.weight'].numpy()
                b5 = training_cache['weights_history'][train_step]['model.8.bias'].numpy()
                with torch.no_grad():
                    model.model[0].weight.copy_(torch.from_numpy(w1))
                    model.model[0].bias.copy_(torch.from_numpy(b1))
                    model.model[2].weight.copy_(torch.from_numpy(w2))
                    model.model[2].bias.copy_(torch.from_numpy(b2))
                    model.model[4].weight.copy_(torch.from_numpy(w3))
                    model.model[4].bias.copy_(torch.from_numpy(b3))
                    model.model[6].weight.copy_(torch.from_numpy(w4))
                    model.model[6].bias.copy_(torch.from_numpy(b4))
                    model.model[8].weight.copy_(torch.from_numpy(w5))
                    model.model[8].bias.copy_(torch.from_numpy(b5))
                adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
                final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
                adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
                surfaces = []
                surface_funcs = []
                for layer_idx in range(len(model.model)):
                    s = Group()
                    surface_funcs.append([])
                    if layer_idx > 7:
                        for neuron_idx in range(num_neurons[layer_idx]):
                            surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx])
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
                    polygons[str(layer_id) + '.new_tiling_nested'] = recompute_tiling_polygonize(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                    polygons[str(layer_id) + '.new_tiling'] = [item for sublist in polygons[str(layer_id) + '.new_tiling_nested'] for item in sublist]
                    print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
                polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
                intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
                my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
                print(len(my_top_polygons), len(my_indicator))
                my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
                print(len(my_top_polygons), len(my_indicator))
                if prev_layer_1_polygons is not None:
                    prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
                else:
                    prev_layer_1_polygons = polygons['0.new_tiling']
                layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_2_polygons is not None:
                    prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
                else:
                    prev_layer_2_polygons = polygons['1.new_tiling']
                layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_3_polygons is not None:
                    prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
                else:
                    prev_layer_3_polygons = polygons['2.new_tiling']
                layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_4_polygons is not None:
                    prev_layer_4_polygons = reorder_polygons_optimal(prev_layer_4_polygons, polygons['3.new_tiling'])
                else:
                    prev_layer_4_polygons = polygons['3.new_tiling']
                layer_4_polygons_flat = manim_polygons_from_np_list(prev_layer_4_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                groups_output = Group()
                layer_idx = len(model.model) - 1
                total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
                start_z = total_height / 2
                for neuron_idx in range(num_neurons[layer_idx]):
                    pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
                    s = surfaces[layer_idx][neuron_idx]
                    g = Group(s, pgs)
                    groups_output.add(g)
                group_combined_output = groups_output.copy()
                group_combined_output[0].set_color(BLUE)
                group_combined_output[1].set_color(YELLOW)
                top_polygons_vgroup = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = p_scaled[:, 2] * adaptive_viz_scales[-1][0]
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup.add(poly_3d)
                lines = VGroup()
                for loop in intersection_lines:
                    loop = loop * np.array([1, 1, viz_scales[2]])
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines.add(line)
                top_polygons_vgroup_flat = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = 0
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup_flat.add(poly_3d)

                def flat_surf_func(u, v):
                    return [u, v, 0]
                flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
                lines_flat = VGroup()
                for loop in intersection_lines:
                    loop[:, 2] = 0
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines_flat.add(line)
                group_combined_output.set_opacity(0.3)
                final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
                border_map_only = Group(flat_map_2.copy(), lines_flat.copy())
                layer_1_polygons_flat.shift([0.0, 2.0, 0.0])
                layer_2_polygons_flat.shift([2.35, 2.0, 0.0])
                layer_3_polygons_flat.shift([0.0, -0.35, 0.0])
                layer_4_polygons_flat.shift([2.35, -0.35, 0.0])
                final_map_group.shift([2 * 2.35, 2, 0.0])
                border_map_only.shift([2 * 2.35, -0.35, 0.0])
                self.frame.reorient(0, 0, 0, (2.97, 0.81, 0.0), 4.8)
                self.add(layer_1_polygons_flat)
                self.add(layer_2_polygons_flat)
                self.add(layer_3_polygons_flat)
                self.add(layer_4_polygons_flat)
                self.add(final_map_group)
                self.add(border_map_only)
                self.wait(0.1)
            except Exception as e:
                print(f'Skipping frame, Error occurred: {e}')
        self.wait(20)
        self.embed()

class p64_f(InteractiveScene):

    def construct(self):
        model = BaarleNet([32, 32, 32, 32])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [32, 32, 32, 32, 32, 32, 32, 32, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/32_32_32_32_1.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        prev_layer_4_polygons = None
        self.frame.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04)
        for train_step in tqdm(list(range(1500, 1700, 10))):
            try:
                if 'layer_1_polygons_flat' in locals():
                    self.remove(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, layer_4_polygons_flat, final_map_group, border_map_only)
                w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
                b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
                w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
                b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
                w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
                b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
                w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
                b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
                w5 = training_cache['weights_history'][train_step]['model.8.weight'].numpy()
                b5 = training_cache['weights_history'][train_step]['model.8.bias'].numpy()
                with torch.no_grad():
                    model.model[0].weight.copy_(torch.from_numpy(w1))
                    model.model[0].bias.copy_(torch.from_numpy(b1))
                    model.model[2].weight.copy_(torch.from_numpy(w2))
                    model.model[2].bias.copy_(torch.from_numpy(b2))
                    model.model[4].weight.copy_(torch.from_numpy(w3))
                    model.model[4].bias.copy_(torch.from_numpy(b3))
                    model.model[6].weight.copy_(torch.from_numpy(w4))
                    model.model[6].bias.copy_(torch.from_numpy(b4))
                    model.model[8].weight.copy_(torch.from_numpy(w5))
                    model.model[8].bias.copy_(torch.from_numpy(b5))
                adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
                final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
                adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
                surfaces = []
                surface_funcs = []
                for layer_idx in range(len(model.model)):
                    s = Group()
                    surface_funcs.append([])
                    if layer_idx > 7:
                        for neuron_idx in range(num_neurons[layer_idx]):
                            surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx])
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
                    polygons[str(layer_id) + '.new_tiling_nested'] = recompute_tiling_polygonize(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                    polygons[str(layer_id) + '.new_tiling'] = [item for sublist in polygons[str(layer_id) + '.new_tiling_nested'] for item in sublist]
                    print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
                polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
                intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
                my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
                print(len(my_top_polygons), len(my_indicator))
                my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
                print(len(my_top_polygons), len(my_indicator))
                if prev_layer_1_polygons is not None:
                    prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
                else:
                    prev_layer_1_polygons = polygons['0.new_tiling']
                layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_2_polygons is not None:
                    prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
                else:
                    prev_layer_2_polygons = polygons['1.new_tiling']
                layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_3_polygons is not None:
                    prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
                else:
                    prev_layer_3_polygons = polygons['2.new_tiling']
                layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_4_polygons is not None:
                    prev_layer_4_polygons = reorder_polygons_optimal(prev_layer_4_polygons, polygons['3.new_tiling'])
                else:
                    prev_layer_4_polygons = polygons['3.new_tiling']
                layer_4_polygons_flat = manim_polygons_from_np_list(prev_layer_4_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                groups_output = Group()
                layer_idx = len(model.model) - 1
                total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
                start_z = total_height / 2
                for neuron_idx in range(num_neurons[layer_idx]):
                    pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
                    s = surfaces[layer_idx][neuron_idx]
                    g = Group(s, pgs)
                    groups_output.add(g)
                group_combined_output = groups_output.copy()
                group_combined_output[0].set_color(BLUE)
                group_combined_output[1].set_color(YELLOW)
                top_polygons_vgroup = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = p_scaled[:, 2] * adaptive_viz_scales[-1][0]
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup.add(poly_3d)
                lines = VGroup()
                for loop in intersection_lines:
                    loop = loop * np.array([1, 1, viz_scales[2]])
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines.add(line)
                top_polygons_vgroup_flat = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = 0
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup_flat.add(poly_3d)

                def flat_surf_func(u, v):
                    return [u, v, 0]
                flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
                lines_flat = VGroup()
                for loop in intersection_lines:
                    loop[:, 2] = 0
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines_flat.add(line)
                group_combined_output.set_opacity(0.3)
                final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
                border_map_only = Group(flat_map_2.copy(), lines_flat.copy())
                layer_1_polygons_flat.shift([0.0, 2.0, 0.0])
                layer_2_polygons_flat.shift([2.35, 2.0, 0.0])
                layer_3_polygons_flat.shift([0.0, -0.35, 0.0])
                layer_4_polygons_flat.shift([2.35, -0.35, 0.0])
                final_map_group.shift([2 * 2.35, 2, 0.0])
                border_map_only.shift([2 * 2.35, -0.35, 0.0])
                self.frame.reorient(0, 0, 0, (2.97, 0.81, 0.0), 4.8)
                self.add(layer_1_polygons_flat)
                self.add(layer_2_polygons_flat)
                self.add(layer_3_polygons_flat)
                self.add(layer_4_polygons_flat)
                self.add(final_map_group)
                self.add(border_map_only)
                self.wait(0.1)
            except Exception as e:
                print(f'Skipping frame, Error occurred: {e}')
        self.wait(20)
        self.embed()

class p64_g(InteractiveScene):

    def construct(self):
        model = BaarleNet([32, 32, 32, 32])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [32, 32, 32, 32, 32, 32, 32, 32, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/32_32_32_32_1.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        prev_layer_4_polygons = None
        self.frame.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04)
        for train_step in tqdm(list(range(1300, 1500, 10))):
            try:
                if 'layer_1_polygons_flat' in locals():
                    self.remove(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, layer_4_polygons_flat, final_map_group, border_map_only)
                w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
                b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
                w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
                b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
                w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
                b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
                w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
                b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
                w5 = training_cache['weights_history'][train_step]['model.8.weight'].numpy()
                b5 = training_cache['weights_history'][train_step]['model.8.bias'].numpy()
                with torch.no_grad():
                    model.model[0].weight.copy_(torch.from_numpy(w1))
                    model.model[0].bias.copy_(torch.from_numpy(b1))
                    model.model[2].weight.copy_(torch.from_numpy(w2))
                    model.model[2].bias.copy_(torch.from_numpy(b2))
                    model.model[4].weight.copy_(torch.from_numpy(w3))
                    model.model[4].bias.copy_(torch.from_numpy(b3))
                    model.model[6].weight.copy_(torch.from_numpy(w4))
                    model.model[6].bias.copy_(torch.from_numpy(b4))
                    model.model[8].weight.copy_(torch.from_numpy(w5))
                    model.model[8].bias.copy_(torch.from_numpy(b5))
                adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
                final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
                adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
                surfaces = []
                surface_funcs = []
                for layer_idx in range(len(model.model)):
                    s = Group()
                    surface_funcs.append([])
                    if layer_idx > 7:
                        for neuron_idx in range(num_neurons[layer_idx]):
                            surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx])
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
                    polygons[str(layer_id) + '.new_tiling_nested'] = recompute_tiling_polygonize(polygons[str(layer_id) + '.split_polygons_nested_clipped'])
                    polygons[str(layer_id) + '.new_tiling'] = [item for sublist in polygons[str(layer_id) + '.new_tiling_nested'] for item in sublist]
                    print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
                polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
                intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
                my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
                print(len(my_top_polygons), len(my_indicator))
                my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
                print(len(my_top_polygons), len(my_indicator))
                if prev_layer_1_polygons is not None:
                    prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
                else:
                    prev_layer_1_polygons = polygons['0.new_tiling']
                layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_2_polygons is not None:
                    prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
                else:
                    prev_layer_2_polygons = polygons['1.new_tiling']
                layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_3_polygons is not None:
                    prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
                else:
                    prev_layer_3_polygons = polygons['2.new_tiling']
                layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                if prev_layer_4_polygons is not None:
                    prev_layer_4_polygons = reorder_polygons_optimal(prev_layer_4_polygons, polygons['3.new_tiling'])
                else:
                    prev_layer_4_polygons = polygons['3.new_tiling']
                layer_4_polygons_flat = manim_polygons_from_np_list(prev_layer_4_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6, stroke_width=0.6)
                groups_output = Group()
                layer_idx = len(model.model) - 1
                total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
                start_z = total_height / 2
                for neuron_idx in range(num_neurons[layer_idx]):
                    pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
                    s = surfaces[layer_idx][neuron_idx]
                    g = Group(s, pgs)
                    groups_output.add(g)
                group_combined_output = groups_output.copy()
                group_combined_output[0].set_color(BLUE)
                group_combined_output[1].set_color(YELLOW)
                top_polygons_vgroup = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = p_scaled[:, 2] * adaptive_viz_scales[-1][0]
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup.add(poly_3d)
                lines = VGroup()
                for loop in intersection_lines:
                    loop = loop * np.array([1, 1, viz_scales[2]])
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines.add(line)
                top_polygons_vgroup_flat = VGroup()
                for j, p in enumerate(my_top_polygons):
                    if len(p) < 3:
                        continue
                    if my_indicator[j]:
                        color = YELLOW
                    else:
                        color = BLUE
                    p_scaled = copy.deepcopy(p)
                    p_scaled[:, 2] = 0
                    poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0.6)
                    poly_3d.set_opacity(0.5)
                    top_polygons_vgroup_flat.add(poly_3d)

                def flat_surf_func(u, v):
                    return [u, v, 0]
                flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
                flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
                lines_flat = VGroup()
                for loop in intersection_lines:
                    loop[:, 2] = 0
                    line = VMobject()
                    line.set_points_as_corners(loop)
                    line.set_stroke(color='#FF00FF', width=4)
                    lines_flat.add(line)
                group_combined_output.set_opacity(0.3)
                final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
                border_map_only = Group(flat_map_2.copy(), lines_flat.copy())
                layer_1_polygons_flat.shift([0.0, 2.0, 0.0])
                layer_2_polygons_flat.shift([2.35, 2.0, 0.0])
                layer_3_polygons_flat.shift([0.0, -0.35, 0.0])
                layer_4_polygons_flat.shift([2.35, -0.35, 0.0])
                final_map_group.shift([2 * 2.35, 2, 0.0])
                border_map_only.shift([2 * 2.35, -0.35, 0.0])
                self.frame.reorient(0, 0, 0, (2.97, 0.81, 0.0), 4.8)
                self.add(layer_1_polygons_flat)
                self.add(layer_2_polygons_flat)
                self.add(layer_3_polygons_flat)
                self.add(layer_4_polygons_flat)
                self.add(final_map_group)
                self.add(border_map_only)
                self.wait(0.1)
            except Exception as e:
                print(f'Skipping frame, Error occurred: {e}')
        self.wait(20)
        self.embed()