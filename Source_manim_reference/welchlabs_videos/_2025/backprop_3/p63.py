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

def create_first_layer_relu_groups(model, surfaces, num_neurons_first_layer=8, extent=1, vertical_spacing=0.9):
    with torch.no_grad():
        w1 = model.model[0].weight.cpu().numpy()
        b1 = model.model[0].bias.cpu().numpy()
    all_relu_groups = Group()
    total_height = (num_neurons_first_layer - 1) * vertical_spacing
    start_z = total_height / 2
    for neuron_idx in range(num_neurons_first_layer):
        joint_points = get_relu_joint(w1[neuron_idx, 0], w1[neuron_idx, 1], b1[neuron_idx], extent=extent)
        joint_line = line_from_joint_points_1(joint_points)
        if joint_line is not None:
            joint_line.set_opacity(0.9)
            neuron_group = Group(surfaces[1][neuron_idx], joint_line)
        else:
            neuron_group = Group(surfaces[1][neuron_idx])
        z_position = start_z - neuron_idx * vertical_spacing
        neuron_group.shift([0, 0, z_position])
        all_relu_groups.add(neuron_group)
    return all_relu_groups

class p63(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/16_16_16_1.pth'
        model = BaarleNet([16, 16, 16])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.15]
        num_neurons = [16, 16, 16, 16, 16, 16, 2]
        vertical_spacing = 1.0
        w1 = model.model[0].weight.detach().numpy()
        b1 = model.model[0].bias.detach().numpy()
        w2 = model.model[2].weight.detach().numpy()
        b2 = model.model[2].bias.detach().numpy()
        w3 = model.model[4].weight.detach().numpy()
        b3 = model.model[4].bias.detach().numpy()
        w4 = model.model[6].weight.detach().numpy()
        b4 = model.model[6].bias.detach().numpy()
        adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
        final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
        adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
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
        if prev_layer_1_polygons is not None:
            prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
        else:
            prev_layer_1_polygons = polygons['0.new_tiling']
        layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        if prev_layer_2_polygons is not None:
            prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
        else:
            prev_layer_2_polygons = polygons['1.new_tiling']
        layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        if prev_layer_3_polygons is not None:
            prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
        else:
            prev_layer_3_polygons = polygons['2.new_tiling']
        layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6)
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
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
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
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
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
            line.set_stroke(color='#FF00FF', width=10)
            lines_flat.add(line)
        group_combined_output.set_opacity(0.3)
        final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
        layer_1_polygons_flat.shift([0.0, 2.0, -5.0])
        layer_2_polygons_flat.shift([2.35, 2.0, -5.0])
        layer_3_polygons_flat.shift([0.0, -0.35, -5.0])
        final_map_group.shift([2.35, -0.35, -5.0])
        self.wait()
        self.frame.reorient(0, 0, 0, (3.07, 0.82, 0.0), 0.77)
        self.add(layer_1_polygons_flat)
        self.add(layer_2_polygons_flat)
        self.add(layer_3_polygons_flat)
        self.add(final_map_group)
        self.wait()
        self.wait(20)
        self.embed()

class p63b(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/16_16_16_1.pth'
        model = BaarleNet([16, 16, 16])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.15]
        num_neurons = [16, 16, 16, 16, 16, 16, 2]
        vertical_spacing = 1.0
        w1 = model.model[0].weight.detach().numpy()
        b1 = model.model[0].bias.detach().numpy()
        w2 = model.model[2].weight.detach().numpy()
        b2 = model.model[2].bias.detach().numpy()
        w3 = model.model[4].weight.detach().numpy()
        b3 = model.model[4].bias.detach().numpy()
        w4 = model.model[6].weight.detach().numpy()
        b4 = model.model[6].bias.detach().numpy()
        adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
        final_layer_viz = scale = 1.8 * min(adaptive_viz_scales[-1])
        adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[-1][0])
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
        if prev_layer_1_polygons is not None:
            prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
        else:
            prev_layer_1_polygons = polygons['0.new_tiling']
        layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=adaptive_viz_scales[-1][0], opacity=0.6)
        if prev_layer_2_polygons is not None:
            prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
        else:
            prev_layer_2_polygons = polygons['1.new_tiling']
        layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=adaptive_viz_scales[-1][0], opacity=0.6)
        if prev_layer_3_polygons is not None:
            prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
        else:
            prev_layer_3_polygons = polygons['2.new_tiling']
        layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=adaptive_viz_scales[-1][0], opacity=0.6)
        groups_output = Group()
        layer_idx = len(model.model) - 1
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[-1][0], opacity=0.6)
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
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.5)
            top_polygons_vgroup.add(poly_3d)
        lines = VGroup()
        for loop in intersection_lines:
            loop = loop * np.array([1, 1, adaptive_viz_scales[-1][0]])
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
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
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
            line.set_stroke(color='#FF00FF', width=8)
            lines_flat.add(line)
        group_combined_output.set_opacity(0.3)
        final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
        combined_3d_group = Group(group_combined_output, top_polygons_vgroup, lines)
        self.wait()
        self.add(combined_3d_group)
        self.frame.reorient(-46, 60, 0, (-0.05, -0.03, -0.3), 3.23)
        self.wait()
        self.play(self.frame.animate.reorient(20, 44, 0, (-0.01, -0.1, -0.38), 3.23), run_time=10)
        self.wait()
        self.wait(20)
        self.embed()