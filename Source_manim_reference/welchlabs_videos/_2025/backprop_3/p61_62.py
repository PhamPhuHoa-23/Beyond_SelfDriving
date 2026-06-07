from functools import partial
import sys
sys.path.append('_2025/backprop_3')
from geometric_dl_utils import *
from plane_folding_utils import *
from geometric_dl_utils_simplified import *
from polytope_intersection_utils import intersect_polytopes
from manimlib import *
from gap_filler import fill_gaps
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
colors_old = [GREY, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]

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

class p61b(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/8_8_1.pth'
        model = BaarleNet([8, 8])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.15]
        num_neurons = [8, 8, 8, 8, 2]
        vertical_spacing = 1.0
        w1 = model.model[0].weight.detach().numpy()
        b1 = model.model[0].bias.detach().numpy()
        w2 = model.model[2].weight.detach().numpy()
        b2 = model.model[2].bias.detach().numpy()
        adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=1.0, extent=1)
        final_layer_viz = scale = 2 * min(adaptive_viz_scales[-1])
        adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
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
            polygons[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons[str(layer_id) + '.split_polygons_merged'])
            print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
        polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
        intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
        my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
        groups_1 = create_first_layer_relu_groups(model, surfaces, num_neurons_first_layer=8, extent=1, vertical_spacing=vertical_spacing)
        layer_1_polygons_flat = manim_polygons_from_np_list(polygons['0.new_tiling'], colors=colors_old, viz_scale=viz_scales[2], opacity=0.6)
        layer_1_polygons_flat.shift([0, 0, -5.0])
        groups_2 = Group()
        layer_idx = 3
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['1.split_polygons_merged'][neuron_idx], colors=colors_old, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs[1:])
            g.shift([3 * (layer_idx - 1) / 2, 0, start_z - neuron_idx * vertical_spacing])
            groups_2.add(g)
        layer_2_polygons_flat = manim_polygons_from_np_list(polygons['1.new_tiling'], colors=colors_old, viz_scale=viz_scales[2], opacity=0.6)
        layer_2_polygons_flat.shift([3, 0, -5.0])
        groups_output = Group()
        layer_idx = len(model.model) - 1
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['2.linear_out'][neuron_idx], colors=colors_old, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs)
            g.shift([6, 0, start_z - neuron_idx * vertical_spacing])
            groups_output.add(g)
        group_combined_output = groups_output.copy()
        group_combined_output[0].set_color(BLUE)
        group_combined_output[1].set_color(YELLOW)
        group_combined_output[0].shift([3, 0, -vertical_spacing / 2])
        group_combined_output[1].shift([3, 0, vertical_spacing / 2])
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
            poly_3d.shift([9, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        lines = VGroup()
        for loop in intersection_lines:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=4)
            lines.add(line)
        lines.shift([9, 0, 0.0])
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
            poly_3d.shift([9, 0, -2])
            top_polygons_vgroup_flat.add(poly_3d)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
        flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map_2.shift([9, 0, -2])
        lines_flat = VGroup()
        for loop in intersection_lines:
            loop[:, 2] = 0
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines_flat.add(line)
        lines_flat.shift([9, 0, -2])
        group_combined_output.set_opacity(0.3)
        self.wait()
        self.frame.reorient(0, 64, 0, (4.62, 2.85, -1.51), 12.99)
        self.add(groups_1)
        self.add(layer_1_polygons_flat)
        self.add(groups_2)
        self.add(layer_2_polygons_flat)
        self.add(groups_output)
        self.add(group_combined_output)
        self.add(top_polygons_vgroup)
        self.add(lines)
        self.add(flat_map_2)
        self.add(top_polygons_vgroup_flat)
        self.add(lines_flat)
        self.wait()
        self.play(self.frame.animate.reorient(0, 58, 0, (1.45, 1.08, -5.07), 5.78), run_time=6)
        self.wait()
        self.play(self.frame.animate.reorient(18, 58, 0, (2.47, 1.79, 0.9), 5.81), groups_1.animate.set_opacity(0.1), groups_2[0].animate.set_opacity(0.1), groups_2[2:].animate.set_opacity(0.1), groups_output.animate.set_opacity(0.1), run_time=6)
        self.wait()
        self.play(self.frame.animate.reorient(-4, 58, 0, (7.86, 1.54, -1.02), 6.99), groups_1.animate.set_opacity(0.6), groups_2[0].animate.set_opacity(0.6), groups_2[2:].animate.set_opacity(0.6), groups_output.animate.set_opacity(0.6), run_time=6)
        self.wait()
        self.play(self.frame.animate.reorient(0, 38, 0, (9.09, 0.29, -2.69), 3.98), group_combined_output.animate.set_opacity(0.05), top_polygons_vgroup.animate.set_opacity(0.05), lines.animate.set_opacity(0.05), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(0, 74, 0, (5.17, 1.54, -0.87), 11.81), group_combined_output.animate.set_opacity(0.2), top_polygons_vgroup.animate.set_opacity(0.5), lines.animate.set_opacity(0.8), run_time=6)
        self.wait()
        self.play(self.frame.animate.reorient(-36, 72, 0, (3.44, 1.56, 0.35), 6.39), run_time=6)
        self.wait()
        self.play(self.frame.animate.reorient(36, 70, 0, (3.21, 1.43, 0.42), 6.39), run_time=12, rate_func=linear)
        self.wait()
        self.play(self.frame.animate.reorient(0, 74, 0, (5.17, 1.54, -0.87), 11.81), run_time=6)
        self.wait(20)
        self.embed()

class p62(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/8_8_8_1.pth'
        model = BaarleNet([8, 8, 8])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [8, 8, 8, 8, 8, 8, 2]
        vertical_spacing = 1.0
        w1 = model.model[0].weight.detach().numpy()
        b1 = model.model[0].bias.detach().numpy()
        w2 = model.model[2].weight.detach().numpy()
        b2 = model.model[2].bias.detach().numpy()
        adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
        final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
        adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
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
            polygons[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons[str(layer_id) + '.split_polygons_merged'])
            print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
        polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
        intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
        my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
        groups_1 = create_first_layer_relu_groups(model, surfaces, num_neurons_first_layer=8, extent=1, vertical_spacing=vertical_spacing)
        layer_1_polygons_flat = manim_polygons_from_np_list(polygons['0.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_1_polygons_flat.shift([0, 0, -5.0])
        groups_2 = Group()
        layer_idx = 3
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['1.split_polygons_merged'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs[1:])
            g.shift([3 * (layer_idx - 1) / 2, 0, start_z - neuron_idx * vertical_spacing])
            groups_2.add(g)
        layer_2_polygons_flat = manim_polygons_from_np_list(polygons['1.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_2_polygons_flat.shift([3, 0, -5.0])
        groups_3 = Group()
        layer_idx = 5
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['2.split_polygons_merged'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs[1:])
            g.shift([3 * (layer_idx - 1) / 2, 0, start_z - neuron_idx * vertical_spacing])
            groups_3.add(g)
        layer_3_polygons_flat = manim_polygons_from_np_list(polygons['2.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_3_polygons_flat.shift([6, 0, -5.0])
        output_horizontal_offset = 9
        groups_output = Group()
        layer_idx = len(model.model) - 1
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs)
            g.shift([output_horizontal_offset, 0, start_z - neuron_idx * vertical_spacing])
            groups_output.add(g)
        group_combined_output = groups_output.copy()
        group_combined_output[0].set_color(BLUE)
        group_combined_output[1].set_color(YELLOW)
        group_combined_output[0].shift([3, 0, -vertical_spacing / 2])
        group_combined_output[1].shift([3, 0, vertical_spacing / 2])
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
            poly_3d.shift([output_horizontal_offset + 3, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        lines = VGroup()
        for loop in intersection_lines:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=4)
            lines.add(line)
        lines.shift([output_horizontal_offset + 3, 0, 0.0])
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
            poly_3d.shift([output_horizontal_offset + 3, 0, -2])
            top_polygons_vgroup_flat.add(poly_3d)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
        flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map_2.shift([output_horizontal_offset + 3, 0, -2])
        lines_flat = VGroup()
        for loop in intersection_lines:
            loop[:, 2] = 0
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines_flat.add(line)
        lines_flat.shift([output_horizontal_offset + 3, 0, -2])
        group_combined_output.set_opacity(0.3)
        self.wait()
        self.frame.reorient(0, 65, 0, (5.72, 2.88, -1.46), 12.99)
        self.add(groups_1)
        self.add(layer_1_polygons_flat)
        self.add(groups_2)
        self.add(layer_2_polygons_flat)
        self.add(groups_3)
        self.add(layer_3_polygons_flat)
        self.add(groups_output)
        self.add(group_combined_output)
        self.add(top_polygons_vgroup)
        self.add(lines)
        self.add(flat_map_2)
        self.add(top_polygons_vgroup_flat)
        self.add(lines_flat)
        self.wait()
        self.play(self.frame.animate.reorient(-42, 56, 0, (6.58, 0.65, 0.58), 3.23), groups_3[:2].animate.set_opacity(0.05), groups_3[3:].animate.set_opacity(0.05), groups_2.animate.set_opacity(0.05), groups_output.animate.set_opacity(0.05), group_combined_output.animate.set_opacity(0.05), top_polygons_vgroup.animate.set_opacity(0.05), lines.animate.set_opacity(0.05), flat_map_2.animate.set_opacity(0.05), top_polygons_vgroup_flat.animate.set_opacity(0.05), lines_flat.animate.set_opacity(0.05), run_time=6)
        self.wait()
        self.play(self.frame.animate.reorient(-69, 56, 0, (6.83, 0.24, 0.61), 3.23), run_time=5)
        self.wait()
        self.play(self.frame.animate.reorient(0, 65, 0, (5.72, 2.88, -1.46), 12.99), groups_3[:2].animate.set_opacity(0.6), groups_3[3:].animate.set_opacity(0.6), groups_2.animate.set_opacity(0.6), groups_output.animate.set_opacity(0.6), group_combined_output.animate.set_opacity(0.2), top_polygons_vgroup.animate.set_opacity(0.6), lines.animate.set_opacity(0.8), flat_map_2.animate.set_opacity(0.5), top_polygons_vgroup_flat.animate.set_opacity(0.5), lines_flat.animate.set_opacity(0.8), run_time=6)
        self.wait()
        self.play(groups_1.animate.set_opacity(0), groups_2.animate.set_opacity(0), groups_3.animate.set_opacity(0), groups_output.animate.set_opacity(0), run_time=3)
        self.wait()
        self.play(group_combined_output.animate.set_opacity(0), top_polygons_vgroup.animate.set_opacity(0), lines.animate.set_opacity(0), run_time=3)
        self.wait()
        final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
        self.wait()
        self.play(layer_1_polygons_flat.animate.shift([0, 2, 0]).set_opacity(0.65), layer_2_polygons_flat.animate.shift([-0.65, 2, 0]).set_opacity(0.65), layer_3_polygons_flat.animate.shift([-6, 0.5 - 0.85, 0]).set_opacity(0.65), final_map_group.animate.shift([-12 + 2.5 - 0.15, -0.35, -3]).set_opacity(0.6), self.frame.animate.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04), run_time=6)
        self.wait()
        self.wait(20)
        self.embed()

class p62b(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/8_8_8_1.pth'
        model = BaarleNet([8, 8, 8])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [8, 8, 8, 8, 8, 8, 2]
        vertical_spacing = 1.0
        w1 = model.model[0].weight.detach().numpy()
        b1 = model.model[0].bias.detach().numpy()
        w2 = model.model[2].weight.detach().numpy()
        b2 = model.model[2].bias.detach().numpy()
        adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
        final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
        adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
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
            polygons[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons[str(layer_id) + '.split_polygons_merged'])
            print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
        polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
        intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
        my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
        groups_1 = create_first_layer_relu_groups(model, surfaces, num_neurons_first_layer=8, extent=1, vertical_spacing=vertical_spacing)
        layer_1_polygons_flat = manim_polygons_from_np_list(polygons['0.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_1_polygons_flat.shift([0, 0, -5.0])
        groups_2 = Group()
        layer_idx = 3
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['1.split_polygons_merged'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs[1:])
            g.shift([3 * (layer_idx - 1) / 2, 0, start_z - neuron_idx * vertical_spacing])
            groups_2.add(g)
        layer_2_polygons_flat = manim_polygons_from_np_list(polygons['1.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_2_polygons_flat.shift([3, 0, -5.0])
        groups_3 = Group()
        layer_idx = 5
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['2.split_polygons_merged'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs[1:])
            g.shift([3 * (layer_idx - 1) / 2, 0, start_z - neuron_idx * vertical_spacing])
            groups_3.add(g)
        layer_3_polygons_flat = manim_polygons_from_np_list(polygons['2.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_3_polygons_flat.shift([6, 0, -5.0])
        output_horizontal_offset = 9
        groups_output = Group()
        layer_idx = len(model.model) - 1
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs)
            g.shift([output_horizontal_offset, 0, start_z - neuron_idx * vertical_spacing])
            groups_output.add(g)
        group_combined_output = groups_output.copy()
        group_combined_output[0].set_color(BLUE)
        group_combined_output[1].set_color(YELLOW)
        group_combined_output[0].shift([3, 0, -vertical_spacing / 2])
        group_combined_output[1].shift([3, 0, vertical_spacing / 2])
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
            poly_3d.shift([output_horizontal_offset + 3, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        lines = VGroup()
        for loop in intersection_lines:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=4)
            lines.add(line)
        lines.shift([output_horizontal_offset + 3, 0, 0.0])
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
            poly_3d.shift([output_horizontal_offset + 3, 0, -2])
            top_polygons_vgroup_flat.add(poly_3d)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
        flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map_2.shift([output_horizontal_offset + 3, 0, -2])
        lines_flat = VGroup()
        for loop in intersection_lines:
            loop[:, 2] = 0
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines_flat.add(line)
        lines_flat.shift([output_horizontal_offset + 3, 0, -2])
        group_combined_output.set_opacity(0.3)
        self.wait()
        self.frame.reorient(0, 65, 0, (5.72, 2.88, -1.46), 12.99)
        self.add(groups_1)
        self.add(layer_1_polygons_flat)
        self.add(groups_2)
        self.add(layer_2_polygons_flat)
        self.add(groups_3)
        self.add(layer_3_polygons_flat)
        self.add(groups_output)
        self.add(group_combined_output)
        self.add(top_polygons_vgroup)
        self.add(lines)
        self.add(flat_map_2)
        self.add(top_polygons_vgroup_flat)
        self.add(lines_flat)
        self.wait()
        self.play(groups_1.animate.set_opacity(0), groups_2.animate.set_opacity(0), groups_3.animate.set_opacity(0), groups_output.animate.set_opacity(0), run_time=3)
        self.wait()
        self.play(group_combined_output.animate.set_opacity(0), top_polygons_vgroup.animate.set_opacity(0), lines.animate.set_opacity(0), run_time=3)
        self.wait()
        final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
        self.remove(groups_1, groups_2, groups_3, groups_output)
        flat_map_2.set_opacity(1.0)
        top_polygons_vgroup_flat.set_opacity(0.45)
        self.wait()
        self.play(layer_1_polygons_flat.animate.shift([0, 2, 0]), layer_2_polygons_flat.animate.shift([-0.65, 2, 0]), layer_3_polygons_flat.animate.shift([-6, 0.5 - 0.85, 0]), final_map_group.animate.shift([-12 + 2.5 - 0.15, -0.35, -3]), self.frame.animate.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04), run_time=6)
        self.wait()
        self.wait(20)
        self.embed()

class p62c2(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/8_8_8_1.pth'
        model = BaarleNet([8, 8, 8])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [8, 8, 8, 8, 8, 8, 2]
        vertical_spacing = 1.0
        w1 = model.model[0].weight.detach().numpy()
        b1 = model.model[0].bias.detach().numpy()
        w2 = model.model[2].weight.detach().numpy()
        b2 = model.model[2].bias.detach().numpy()
        adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
        final_layer_viz = scale = 1.4 * min(adaptive_viz_scales[-1])
        adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
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
            polygons[str(layer_id) + '.new_tiling'] = recompute_tiling_general(polygons[str(layer_id) + '.split_polygons_merged'])
            print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling'])), ' polygons.')
        polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling'])
        intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
        my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
        groups_1 = create_first_layer_relu_groups(model, surfaces, num_neurons_first_layer=8, extent=1, vertical_spacing=vertical_spacing)
        layer_1_polygons_flat = manim_polygons_from_np_list(polygons['0.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_1_polygons_flat.shift([0, 0, -5.0])
        groups_2 = Group()
        layer_idx = 3
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['1.split_polygons_merged'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs[1:])
            g.shift([3 * (layer_idx - 1) / 2, 0, start_z - neuron_idx * vertical_spacing])
            groups_2.add(g)
        layer_2_polygons_flat = manim_polygons_from_np_list(polygons['1.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_2_polygons_flat.shift([3, 0, -5.0])
        groups_3 = Group()
        layer_idx = 5
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['2.split_polygons_merged'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs[1:])
            g.shift([3 * (layer_idx - 1) / 2, 0, start_z - neuron_idx * vertical_spacing])
            groups_3.add(g)
        layer_3_polygons_flat = manim_polygons_from_np_list(polygons['2.new_tiling'], colors=colors, viz_scale=viz_scales[2], opacity=0.6)
        layer_3_polygons_flat.shift([6, 0, -5.0])
        output_horizontal_offset = 9
        groups_output = Group()
        layer_idx = len(model.model) - 1
        total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
        start_z = total_height / 2
        for neuron_idx in range(num_neurons[layer_idx]):
            pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
            s = surfaces[layer_idx][neuron_idx]
            g = Group(s, pgs)
            g.shift([output_horizontal_offset, 0, start_z - neuron_idx * vertical_spacing])
            groups_output.add(g)
        group_combined_output = groups_output.copy()
        group_combined_output[0].set_color(BLUE)
        group_combined_output[1].set_color(YELLOW)
        group_combined_output[0].shift([3, 0, -vertical_spacing / 2])
        group_combined_output[1].shift([3, 0, vertical_spacing / 2])
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
            poly_3d.shift([output_horizontal_offset + 3, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        lines = VGroup()
        for loop in intersection_lines:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=4)
            lines.add(line)
        lines.shift([output_horizontal_offset + 3, 0, 0.0])
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
            poly_3d.shift([output_horizontal_offset + 3, 0, -2])
            top_polygons_vgroup_flat.add(poly_3d)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
        flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map_2.shift([output_horizontal_offset + 3, 0, -2])
        lines_flat = VGroup()
        for loop in intersection_lines:
            loop[:, 2] = 0
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines_flat.add(line)
        lines_flat.shift([output_horizontal_offset + 3, 0, -2])
        group_combined_output.set_opacity(0.3)
        self.wait()
        self.frame.reorient(0, 65, 0, (5.72, 2.88, -1.46), 12.99)
        combined_3d_group = Group(group_combined_output, top_polygons_vgroup, lines)
        self.add(combined_3d_group)
        self.wait()
        self.play(self.frame.animate.reorient(48, 50, 0, (-0.04, 0.13, -0.47), 3.99), combined_3d_group.animate.move_to(ORIGIN), run_time=6, rate_func=linear)
        self.wait()
        self.wait(20)
        self.embed()

class p62d(InteractiveScene):

    def construct(self):
        model = BaarleNet([8, 8, 8])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [8, 8, 8, 8, 8, 8, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/8_8_8_2.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        self.frame.reorient(27, 54, 0, (-0.02, 0.05, -0.55), 3.99)
        for train_step in tqdm(np.arange(0, 1000, 1)):
            if 'combined_3d_group' in locals():
                self.remove(combined_3d_group)
            w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
            b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
            w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
            b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
            w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
            b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
            w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
            b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
            with torch.no_grad():
                model.model[0].weight.copy_(torch.from_numpy(w1))
                model.model[0].bias.copy_(torch.from_numpy(b1))
                model.model[2].weight.copy_(torch.from_numpy(w2))
                model.model[2].bias.copy_(torch.from_numpy(b2))
                model.model[4].weight.copy_(torch.from_numpy(w3))
                model.model[4].bias.copy_(torch.from_numpy(b3))
                model.model[6].weight.copy_(torch.from_numpy(w4))
                model.model[6].bias.copy_(torch.from_numpy(b4))
            adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
            adaptive_viz_scales[-1] = [0.014, 0.014]
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
            print(len(my_top_polygons), len(my_indicator))
            my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
            print(len(my_top_polygons), len(my_indicator))
            output_horizontal_offset = 9
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
            group_combined_output.set_opacity(0.3)
            top_polygons_vgroup.set_opacity(0.6)
            combined_3d_group = Group(group_combined_output, top_polygons_vgroup, lines)
            self.add(combined_3d_group)
            self.wait(0.1)
        self.wait(20)
        self.embed()

class p62e(InteractiveScene):

    def construct(self):
        model = BaarleNet([8, 8, 8])
        viz_scales = [0.06, 0.06, 0.042, 0.042, 0.042, 0.042, 0.15]
        num_neurons = [8, 8, 8, 8, 8, 8, 2]
        vertical_spacing = 1.0
        data_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/training_caches/8_8_8_2.pkl'
        with open(data_path, 'rb') as file:
            training_cache = pickle.load(file)
        prev_layer_1_polygons = None
        prev_layer_2_polygons = None
        prev_layer_3_polygons = None
        self.frame.reorient(0, 0, 0, (3.94, 0.38, 0.0), 2.04)
        for train_step in tqdm(np.arange(0, 1000, 1)):
            if 'layer_1_polygons_flat' in locals():
                self.remove(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, final_map_group)
            w1 = training_cache['weights_history'][train_step]['model.0.weight'].numpy()
            b1 = training_cache['weights_history'][train_step]['model.0.bias'].numpy()
            w2 = training_cache['weights_history'][train_step]['model.2.weight'].numpy()
            b2 = training_cache['weights_history'][train_step]['model.2.bias'].numpy()
            w3 = training_cache['weights_history'][train_step]['model.4.weight'].numpy()
            b3 = training_cache['weights_history'][train_step]['model.4.bias'].numpy()
            w4 = training_cache['weights_history'][train_step]['model.6.weight'].numpy()
            b4 = training_cache['weights_history'][train_step]['model.6.bias'].numpy()
            with torch.no_grad():
                model.model[0].weight.copy_(torch.from_numpy(w1))
                model.model[0].bias.copy_(torch.from_numpy(b1))
                model.model[2].weight.copy_(torch.from_numpy(w2))
                model.model[2].bias.copy_(torch.from_numpy(b2))
                model.model[4].weight.copy_(torch.from_numpy(w3))
                model.model[4].bias.copy_(torch.from_numpy(b3))
                model.model[6].weight.copy_(torch.from_numpy(w4))
                model.model[6].bias.copy_(torch.from_numpy(b4))
            adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=0.6, extent=1)
            adaptive_viz_scales[-1] = [0.014, 0.014]
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
            print(len(my_top_polygons), len(my_indicator))
            my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
            print(len(my_top_polygons), len(my_indicator))
            if prev_layer_1_polygons is not None:
                prev_layer_1_polygons = reorder_polygons_optimal(prev_layer_1_polygons, polygons['0.new_tiling'])
            else:
                prev_layer_1_polygons = polygons['0.new_tiling']
            layer_1_polygons_flat = manim_polygons_from_np_list(prev_layer_1_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6)
            layer_1_polygons_flat.shift([0, 0, -5.0])
            if prev_layer_2_polygons is not None:
                prev_layer_2_polygons = reorder_polygons_optimal(prev_layer_2_polygons, polygons['1.new_tiling'])
            else:
                prev_layer_2_polygons = polygons['1.new_tiling']
            layer_2_polygons_flat = manim_polygons_from_np_list(prev_layer_2_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6)
            layer_2_polygons_flat.shift([3, 0, -5.0])
            if prev_layer_3_polygons is not None:
                prev_layer_3_polygons = reorder_polygons_optimal(prev_layer_3_polygons, polygons['2.new_tiling'])
            else:
                prev_layer_3_polygons = polygons['2.new_tiling']
            layer_3_polygons_flat = manim_polygons_from_np_list(prev_layer_3_polygons, colors=colors, viz_scale=viz_scales[2], opacity=0.6)
            layer_3_polygons_flat.shift([6, 0, -5.0])
            output_horizontal_offset = 9
            groups_output = Group()
            layer_idx = len(model.model) - 1
            total_height = (num_neurons[layer_idx] - 1) * vertical_spacing
            start_z = total_height / 2
            for neuron_idx in range(num_neurons[layer_idx]):
                pgs = manim_polygons_from_np_list(polygons['3.linear_out'][neuron_idx], colors=colors, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx], opacity=0.6)
                s = surfaces[layer_idx][neuron_idx]
                g = Group(s, pgs)
                g.shift([output_horizontal_offset, 0, start_z - neuron_idx * vertical_spacing])
                groups_output.add(g)
            group_combined_output = groups_output.copy()
            group_combined_output[0].set_color(BLUE)
            group_combined_output[1].set_color(YELLOW)
            group_combined_output[0].shift([3, 0, -vertical_spacing / 2])
            group_combined_output[1].shift([3, 0, vertical_spacing / 2])
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
                poly_3d.shift([output_horizontal_offset + 3, 0, 0])
                top_polygons_vgroup.add(poly_3d)
            lines = VGroup()
            for loop in intersection_lines:
                loop = loop * np.array([1, 1, viz_scales[2]])
                line = VMobject()
                line.set_points_as_corners(loop)
                line.set_stroke(color='#FF00FF', width=4)
                lines.add(line)
            lines.shift([output_horizontal_offset + 3, 0, 0.0])
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
                poly_3d.shift([output_horizontal_offset + 3, 0, -2])
                top_polygons_vgroup_flat.add(poly_3d)

            def flat_surf_func(u, v):
                return [u, v, 0]
            flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
            flat_map_2 = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-17.png')
            flat_map_2.set_shading(0, 0, 0).set_opacity(0.8)
            flat_map_2.shift([output_horizontal_offset + 3, 0, -2])
            lines_flat = VGroup()
            for loop in intersection_lines:
                loop[:, 2] = 0
                line = VMobject()
                line.set_points_as_corners(loop)
                line.set_stroke(color='#FF00FF', width=5)
                lines_flat.add(line)
            lines_flat.shift([output_horizontal_offset + 3, 0, -2])
            group_combined_output.set_opacity(0.3)
            final_map_group = Group(flat_map_2, top_polygons_vgroup_flat, lines_flat)
            layer_1_polygons_flat.shift([0, 2, 0])
            layer_2_polygons_flat.shift([-0.65, 2, 0])
            layer_3_polygons_flat.shift([-6, 0.5 - 0.85, 0])
            final_map_group.shift([-12 + 2.5 - 0.15, -0.35, -3])
            self.add(layer_1_polygons_flat, layer_2_polygons_flat, layer_3_polygons_flat, final_map_group)
            self.wait(0.1)
        self.wait(20)
        self.embed()