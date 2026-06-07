from functools import partial
import sys
sys.path.append('_2025/backprop_3')
from geometric_dl_utils import *
from plane_folding_utils import *
from geometric_dl_utils_simplified import *
from polytope_intersection_utils import intersect_polytopes
from manimlib import *
graphics_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/ai_book/4_deep_learning/graphics/'
colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]
map_filename = 'baarle_hertog_maps-13.png'
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#6e9671'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'

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
        all_relu_groups.add(neuron_group)
    return all_relu_groups

def order_closed_loops_with_closure(segments, tol=1e-06):
    used = [False] * len(segments)
    loops_pts = []
    for i, seg in enumerate(segments):
        if used[i]:
            continue
        loop_segs = [seg.copy()]
        used[i] = True
        start_pt = seg[0].copy()
        curr_pt = seg[1].copy()
        while True:
            found = False
            for j, seg2 in enumerate(segments):
                if used[j]:
                    continue
                p0, p1 = (seg2[0], seg2[1])
                if np.linalg.norm(p0 - curr_pt) < tol:
                    loop_segs.append(seg2.copy())
                    curr_pt = p1.copy()
                    used[j] = True
                    found = True
                    break
                if np.linalg.norm(p1 - curr_pt) < tol:
                    rev = seg2[::-1].copy()
                    loop_segs.append(rev)
                    curr_pt = rev[1].copy()
                    used[j] = True
                    found = True
                    break
            if not found or np.linalg.norm(curr_pt - start_pt) < tol:
                break
        pts = [loop_segs[0][0]]
        for s in loop_segs:
            pts.append(s[1])
        if np.linalg.norm(pts[-1] - start_pt) > tol:
            pts.append(start_pt)
        loops_pts.append(np.vstack(pts))
    return loops_pts

class p7a(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/8_2.pth'
        model = BaarleNet([8])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.05]
        num_neurons = [8, 8, 2]
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/' + map_filename)
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
        first_layer_groups = create_first_layer_relu_groups(model, surfaces, num_neurons_first_layer=8, extent=1, vertical_spacing=0.0)
        self.frame.reorient(0, 54, 0, (0.0, 0.0, 0.0), 2.72)
        for i in range(8):
            self.add(first_layer_groups[i][0])
            self.wait()
            self.remove(first_layer_groups[i][0])
        self.wait()
        polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2])
        polygons_21_copy = polygons_21.copy()
        polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2])
        polygons_22_copy = polygons_22.copy()
        surfaces_1_copy = surfaces[1].copy()
        surfaces_1_copy_2 = surfaces[1].copy()
        first_layer_groups_flat = create_first_layer_relu_groups(model, surfaces, num_neurons_first_layer=8, extent=1, vertical_spacing=0.0)
        shifted_line_copies = Group()
        for i in range(len(first_layer_groups_flat)):
            if len(first_layer_groups_flat[i]) > 1:
                shifted_line_copies.add(first_layer_groups_flat[i][1].copy())
        shifted_line_copies_2 = shifted_line_copies.copy()
        shifted_line_copies.shift([3, 0, 0.9])
        og_lines = Group()
        for i in range(len(first_layer_groups)):
            if len(first_layer_groups[i]) > 1:
                og_lines.add(first_layer_groups[i][1])
        og_line_copies = og_lines.copy()
        og_line_copies_2 = og_lines.copy()
        self.frame.reorient(0, 54, 0, (0.0, 0.0, 0.0), 2.72)
        self.add(surfaces[2][0])
        self.add(polygons_21)
        self.wait()
        self.remove(surfaces[2][0], polygons_21)
        self.frame.reorient(0, 50, 0, (-0.06, -0.15, -0.2), 2.72)
        self.add(surfaces[2][1])
        self.add(polygons_22)
        self.wait()
        self.remove(surfaces[2][1], polygons_22)
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
            poly_3d.set_opacity(0.3)
            top_polygons_vgroup.add(poly_3d)
        polygons_21.set_color(BLUE)
        polygons_22.set_color(YELLOW)
        surfaces[1].set_opacity(0.1)
        loops = order_closed_loops_with_closure(intersection_lines)
        lines = VGroup()
        for loop in loops:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines.add(line)
        self.frame.reorient(-2, 46, 0, (0.06, -0.02, -0.07), 3.07)
        surfaces[2][0].set_opacity(0.3)
        surfaces[2][1].set_opacity(0.3)
        self.add(surfaces[2][0])
        self.add(surfaces[2][1])
        self.wait()
        self.add(polygons_21)
        self.add(polygons_22)
        self.wait()
        self.add(top_polygons_vgroup)
        self.add(lines)
        self.wait()
        self.remove(surfaces[2][0], surfaces[2][1], polygons_21, polygons_22, top_polygons_vgroup, lines)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        lines_flat = VGroup()
        for loop in loops:
            loop = loop * np.array([1, 1, 0])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines_flat.add(line)
        self.frame.reorient(0, 0, 0, (0.02, 0.0, 0.0), 2.65)
        self.add(flat_map)
        self.add(lines_flat)
        self.wait(20)
        self.embed()

class p7b_16(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/16_1.pth'
        model = BaarleNet([16])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.04]
        num_neurons = [16, 16, 2]
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/' + map_filename)
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
        loops = order_closed_loops_with_closure(intersection_lines)
        lines = VGroup()
        for loop in loops:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#FF00FF', width=5)
            lines.add(line)
        lines.shift([3, 0, 0])
        polygon_max_height = 0.8
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        surfaces[2][0].shift([3, 0, 0])
        polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_21_copy = polygons_21.copy()
        polygons_21.shift([3, 0, 0.001])
        surfaces[2][1].shift([3, 0, 0])
        polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_22_copy = polygons_22.copy()
        polygons_22.shift([3, 0, 0.002])
        polygons_22.set_color(YELLOW)
        polygons_21.set_color(BLUE)
        polygons_21.set_opacity(0.3)
        polygons_22.set_opacity(0.3)
        surfaces[2][0].set_opacity(0.4)
        surfaces[2][1].set_opacity(0.4)
        top_polygons_vgroup.set_opacity(0.5)
        self.frame.reorient(0, 40, 0, (3.1, -0.16, -0.18), 4.12)
        self.add(polygons_21, polygons_22)
        self.add(top_polygons_vgroup)
        self.add(lines)
        self.wait()
        self.remove(polygons_21, polygons_22, top_polygons_vgroup, lines)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat = VGroup()
        for loop in loops:
            loop = loop * np.array([1, 1, 0])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=6)
            lines_flat.add(line)
        lines_flat.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (5.73, 0.0, 0.0), 2.51)
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([5.7, 0, 0])
            top_polygons_vgroup_flat.add(poly_3d)
        self.wait()
        self.add(flat_map)
        self.add(top_polygons_vgroup_flat)
        self.add(lines_flat)
        self.wait()
        self.wait()
        self.wait(20)
        self.embed()

class p7c_32(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/32_1.pth'
        model = BaarleNet([32])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.04]
        num_neurons = [32, 32, 2]
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/' + map_filename)
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
        loops = order_closed_loops_with_closure(intersection_lines)
        lines = VGroup()
        for loop in loops:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines.add(line)
        lines.shift([3, 0, 0])
        polygon_max_height = 0.8
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        surfaces[2][0].shift([3, 0, 0])
        polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_21_copy = polygons_21.copy()
        polygons_21.shift([3, 0, 0.001])
        surfaces[2][1].shift([3, 0, 0])
        polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_22_copy = polygons_22.copy()
        polygons_22.shift([3, 0, 0.002])
        polygons_22.set_color(YELLOW)
        polygons_21.set_color(BLUE)
        polygons_21.set_opacity(0.3)
        polygons_22.set_opacity(0.3)
        surfaces[2][0].set_opacity(0.4)
        surfaces[2][1].set_opacity(0.4)
        top_polygons_vgroup.set_opacity(0.5)
        self.frame.reorient(0, 40, 0, (3.1, -0.16, -0.18), 4.12)
        self.add(polygons_21, polygons_22)
        self.add(top_polygons_vgroup)
        self.add(lines)
        self.wait()
        self.remove(polygons_21, polygons_22, top_polygons_vgroup, lines)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat = VGroup()
        for loop in loops:
            loop = loop * np.array([1, 1, 0])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=6)
            lines_flat.add(line)
        lines_flat.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (5.73, 0.0, 0.0), 2.51)
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([5.7, 0, 0])
            top_polygons_vgroup_flat.add(poly_3d)
        self.wait()
        self.add(flat_map)
        self.add(top_polygons_vgroup_flat)
        self.add(lines_flat)
        self.wait()
        self.wait(20)
        self.embed()

class p7d_64(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/64_1.pth'
        model = BaarleNet([64])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.04]
        num_neurons = [64, 64, 2]
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/' + map_filename)
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
        loops = order_closed_loops_with_closure(intersection_lines)
        lines = VGroup()
        for loop in loops:
            loop = loop * np.array([1, 1, viz_scales[2]])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines.add(line)
        lines.shift([3, 0, 0])
        polygon_max_height = 0.8
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        surfaces[2][0].shift([3, 0, 0])
        polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_21_copy = polygons_21.copy()
        polygons_21.shift([3, 0, 0.001])
        surfaces[2][1].shift([3, 0, 0])
        polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_22_copy = polygons_22.copy()
        polygons_22.shift([3, 0, 0.002])
        polygons_22.set_color(YELLOW)
        polygons_21.set_color(BLUE)
        polygons_21.set_opacity(0.3)
        polygons_22.set_opacity(0.3)
        surfaces[2][0].set_opacity(0.4)
        surfaces[2][1].set_opacity(0.4)
        top_polygons_vgroup.set_opacity(0.5)
        self.frame.reorient(0, 40, 0, (3.1, -0.16, -0.18), 4.12)
        self.add(polygons_21, polygons_22)
        self.add(top_polygons_vgroup)
        self.add(lines)
        self.wait()
        self.remove(polygons_21, polygons_22, top_polygons_vgroup, lines)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat = VGroup()
        for loop in loops:
            loop = loop * np.array([1, 1, 0])
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=6)
            lines_flat.add(line)
        lines_flat.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (5.73, 0.0, 0.0), 2.51)
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([5.7, 0, 0])
            top_polygons_vgroup_flat.add(poly_3d)
        self.wait()
        self.add(flat_map)
        self.add(top_polygons_vgroup_flat)
        self.add(lines_flat)
        self.wait()
        self.wait()
        self.wait(20)
        self.embed()

class p7e_128(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/128_1.pth'
        model = BaarleNet([128])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.04]
        num_neurons = [128, 128, 2]
        surfaces = []
        surface_funcs = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=viz_scales[layer_idx])
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/' + map_filename)
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
        with open('_2025/backprop_3/models/128_1_borders.p', 'rb') as file:
            borders_interp = pickle.load(file)
        lines = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines.add(line)
        lines.shift([3, 0, 0])
        polygon_max_height = 0.8
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3, 0, 0])
            top_polygons_vgroup.add(poly_3d)
        surfaces[2][0].shift([3, 0, 0])
        polygons_21 = manim_polygons_from_np_list(polygons['1.linear_out'][0], colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_21_copy = polygons_21.copy()
        polygons_21.shift([3, 0, 0.001])
        surfaces[2][1].shift([3, 0, 0])
        polygons_22 = manim_polygons_from_np_list(polygons['1.linear_out'][1], colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_22_copy = polygons_22.copy()
        polygons_22.shift([3, 0, 0.002])
        polygons_22.set_color(YELLOW)
        polygons_21.set_color(BLUE)
        polygons_21.set_opacity(0.3)
        polygons_22.set_opacity(0.3)
        surfaces[2][0].set_opacity(0.4)
        surfaces[2][1].set_opacity(0.4)
        top_polygons_vgroup.set_opacity(0.5)
        self.frame.reorient(0, 31, 0, (3.13, -0.06, -0.12), 4.12)
        self.add(polygons_21, polygons_22)
        self.add(top_polygons_vgroup)
        self.add(lines)
        self.wait()
        self.remove(polygons_21, polygons_22, top_polygons_vgroup, lines)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat_cleaner = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines_flat_cleaner.add(line)
        lines_flat_cleaner.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (5.73, 0.0, 0.0), 2.51)
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=0)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([5.7, 0, 0])
            top_polygons_vgroup_flat.add(poly_3d)
        self.wait()
        self.add(flat_map)
        self.add(top_polygons_vgroup_flat)
        self.add(lines_flat_cleaner)
        self.wait()
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
            p_scaled[:, -1] = np.clip(p_scaled[:, -1], -polygon_max_height, polygon_max_height)
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3, 0, 0])
            top_polygons_vgroup_flat.add(poly_3d)
        polygon_arrays_1_flat = copy.deepcopy(polygons['1.linear_out'][0])
        for p in polygon_arrays_1_flat:
            p[:, 2] = 0
        polygon_arrays_2_flat = copy.deepcopy(polygons['1.linear_out'][1])
        for p in polygon_arrays_2_flat:
            p[:, 2] = 0
        polygons_21_flat = manim_polygons_from_np_list(polygon_arrays_1_flat, colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_21_flat.shift([3, 0, 0.001])
        polygons_22_flat = manim_polygons_from_np_list(polygon_arrays_2_flat, colors=colors, viz_scale=viz_scales[2], polygon_max_height=polygon_max_height)
        polygons_22_flat.shift([3, 0, 0.002])
        polygons_22_flat.set_color(YELLOW)
        polygons_21_flat.set_color(BLUE)
        polygons_21_flat.set_opacity(0.1)
        polygons_22_flat.set_opacity(0.1)
        top_polygons_vgroup_flat.set_opacity(0.5)
        self.wait()
        self.remove(polygons_21, polygons_22)
        self.play(ReplacementTransform(top_polygons_vgroup, top_polygons_vgroup_flat), self.frame.animate.reorient(0, 0, 0, (4.34, 0.02, -0.19), 3.47), run_time=6)
        self.remove(lines)
        self.add(lines)
        self.wait()
        self.wait(20)
        self.embed()

class p7f_256(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/256_1.pth'
        model = BaarleNet([256])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.04]
        num_neurons = [256, 256, 2]
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
        with open('_2025/backprop_3/models/256_1_borders.p', 'rb') as file:
            borders_interp = pickle.load(file)
        lines = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines.add(line)
        lines.shift([3, 0, 0])
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
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3, 0, 0])
            top_polygons_vgroup_flat.add(poly_3d)
        top_polygons_vgroup_flat.set_opacity(0.5)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat_cleaner = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines_flat_cleaner.add(line)
        lines_flat_cleaner.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (4.34, 0.02, -0.19), 3.47)
        self.add(top_polygons_vgroup_flat)
        self.add(lines)
        polygons_copy = top_polygons_vgroup_flat.copy()
        polygons_copy.set_stroke(width=0)
        polygons_copy.shift([2.7, 0, 0])
        self.add(flat_map, lines_flat_cleaner)
        self.add(polygons_copy)
        self.wait()
        self.wait(20)
        self.embed()

class p7g_512(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/512_1_longer.pth'
        model = BaarleNet([512])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.04]
        num_neurons = [512, 512, 2]
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
        with open('_2025/backprop_3/models/512_1_borders.p', 'rb') as file:
            borders_interp = pickle.load(file)
        lines = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines.add(line)
        lines.shift([3, 0, 0])
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
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3, 0, 0])
            top_polygons_vgroup_flat.add(poly_3d)
        top_polygons_vgroup_flat.set_opacity(0.5)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat_cleaner = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines_flat_cleaner.add(line)
        lines_flat_cleaner.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (4.34, 0.02, -0.19), 3.47)
        self.add(top_polygons_vgroup_flat)
        self.add(lines)
        polygons_copy = top_polygons_vgroup_flat.copy()
        polygons_copy.set_stroke(width=0)
        polygons_copy.shift([2.7, 0, 0])
        self.add(flat_map, lines_flat_cleaner)
        self.add(polygons_copy)
        self.wait()
        self.wait(20)
        self.embed()

class p7h_1024(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/one_layer_1024_nuerons_long.pth'
        model = BaarleNet([1024])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.04]
        num_neurons = [1024, 1024, 2]
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
        with open('_2025/backprop_3/models/1024_borders.p', 'rb') as file:
            borders_interp = pickle.load(file)
        lines = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines.add(line)
        lines.shift([3, 0, 0])
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
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3, 0, 0])
            top_polygons_vgroup_flat.add(poly_3d)
        top_polygons_vgroup_flat.set_opacity(0.5)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat_cleaner = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=4)
            lines_flat_cleaner.add(line)
        lines_flat_cleaner.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (4.34, 0.02, -0.19), 3.47)
        self.add(top_polygons_vgroup_flat)
        self.add(lines)
        polygons_copy = top_polygons_vgroup_flat.copy()
        polygons_copy.set_stroke(width=0)
        polygons_copy.shift([2.7, 0, 0])
        self.add(flat_map, lines_flat_cleaner)
        self.add(polygons_copy)
        self.wait()
        self.play(top_polygons_vgroup_flat.animate.set_opacity(0.0), lines.animate.set_opacity(0.0), self.frame.animate.reorient(0, 0, 0, (5.67, -0.01, -0.19), 3.47), run_time=5.0)
        self.wait(20)
        self.embed()

class p7i_10k(InteractiveScene):

    def construct(self):
        with open('_2025/backprop_3/models/10k_borders.p', 'rb') as file:
            borders_interp = pickle.load(file)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat_cleaner = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=6)
            lines_flat_cleaner.add(line)
        lines_flat_cleaner.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (5.67, -0.01, -0.19), 3.47)
        self.add(flat_map, lines_flat_cleaner)
        self.wait(20)
        self.embed()

class p7j_100k(InteractiveScene):

    def construct(self):
        with open('_2025/backprop_3/models/100k_borders.p', 'rb') as file:
            borders_interp = pickle.load(file)

        def flat_surf_func(u, v):
            return [u, v, 0]
        flat_map_surf = ParametricSurface(flat_surf_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
        flat_map = TexturedSurface(flat_map_surf, graphics_dir + '/baarle_hertog_maps/' + map_filename)
        flat_map.set_shading(0, 0, 0).set_opacity(0.8)
        flat_map.shift([5.7, 0, 0])
        lines_flat_cleaner = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=6)
            lines_flat_cleaner.add(line)
        lines_flat_cleaner.shift([5.7, 0, 0])
        self.frame.reorient(0, 0, 0, (5.67, -0.01, -0.19), 3.47)
        self.add(flat_map, lines_flat_cleaner)
        self.wait(20)
        self.embed()