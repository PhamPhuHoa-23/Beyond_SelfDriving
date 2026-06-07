from manimlib import *
from functools import partial
import sys
sys.path.append('_2025/backprop_3')
from geometric_dl_utils import *
from polytope_intersection_utils import intersect_polytopes
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#6e9671'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
graphics_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/graphics/'
heatmaps_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/heatmaps'

class refactor_sketch_1(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/3_3_1.pth'
        model = BaarleNet([3, 3])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.1, 0.1, 0.05, 0.05, 0.15]
        num_neurons = [3, 3, 3, 3, 2]
        vertical_spacing = 1.5
        horizontal_spacing = 3
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]
        adaptive_viz_scales = compute_adaptive_viz_scales(model, max_surface_height=1.0, extent=1)
        final_layer_viz = scale = 2 * min(adaptive_viz_scales[-1])
        adaptive_viz_scales[-1] = [final_layer_viz, final_layer_viz]
        surfaces = []
        surface_funcs = []
        surface_funcs_no_viz_scale = []
        for layer_idx in range(len(model.model)):
            s = Group()
            surface_funcs.append([])
            surface_funcs_no_viz_scale.append([])
            for neuron_idx in range(num_neurons[layer_idx]):
                surface_func = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=adaptive_viz_scales[layer_idx][neuron_idx])
                surface_func_no_scaling = partial(surface_func_from_model, model=model, layer_idx=layer_idx, neuron_idx=neuron_idx, viz_scale=1.0)
                bent_surface = ParametricSurface(surface_func, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
                ts = TexturedSurface(bent_surface, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
                ts.set_shading(0, 0, 0).set_opacity(0.75)
                s.add(ts)
                surface_funcs[-1].append(surface_func)
                surface_funcs_no_viz_scale[-1].append(surface_func_no_scaling)
            surfaces.append(s)
        for layer_idx, sl in enumerate(surfaces):
            for neuron_idx, s in enumerate(sl):
                s.shift([horizontal_spacing * layer_idx - 6, 0, vertical_spacing * neuron_idx])
                self.add(s)
        self.frame.reorient(0, 54, 0, (1.41, 1.82, 4.15), 15.71)
        layer_idx = 0
        relu_intersections_planes_1 = get_relu_intersection_planes(num_neurons[layer_idx], layer_idx, neuron_idx, horizontal_spacing, vertical_spacing)
        self.add(relu_intersections_planes_1)
        layer_idx = 1
        layer_1_polygons = get_polygon_corners_layer_1(model)
        layer_1_polygons_3d = get_3d_polygons_layer_1(layer_1_polygons, surface_funcs_no_viz_scale, num_neurons=num_neurons[layer_idx], layer_idx=1)
        scaled_layer_1_polygons_3d = apply_viz_scale_to_3d_polygons(layer_1_polygons_3d, adaptive_viz_scales[layer_idx])
        polygons_vgroup = viz_3d_polygons(scaled_layer_1_polygons_3d, layer_idx, colors=None, color_gray_index=1)
        self.add(polygons_vgroup)
        self.wait()
        layer_2_polygons = carve_plane_with_relu_joints([o['relu_line'] for o in layer_1_polygons])
        output_poygons_2d = viz_carved_regions_flat(layer_2_polygons, horizontal_spacing, layer_idx, colors=None)
        self.add(output_poygons_2d)
        layer_idx = 2
        layer_2_polygons_3d = get_3d_polygons(layer_2_polygons, num_neurons[layer_idx], surface_funcs_no_viz_scale, layer_idx)
        scaled_layer_2_polygons_3d = apply_viz_scale_to_3d_polygons(layer_2_polygons_3d, adaptive_viz_scales[layer_idx])
        polygons_vgroup_2 = viz_3d_polygons(scaled_layer_2_polygons_3d, layer_idx, colors=None, color_gray_index=None)
        self.add(polygons_vgroup_2)
        relu_intersections_planes_2 = get_relu_intersection_planes(num_neurons[layer_idx], layer_idx, neuron_idx, horizontal_spacing, vertical_spacing)
        self.add(relu_intersections_planes_2)
        layer_idx = 3
        all_polygons, merged_zero_polygons, unmerged_polygons = split_polygons_with_relu(layer_2_polygons_3d)
        all_polygons_after_merging = copy.deepcopy(merged_zero_polygons)
        for i, o in enumerate(unmerged_polygons):
            all_polygons_after_merging[i].extend(o)
        all_polygons_after_merging_scaled = apply_viz_scale_to_3d_polygons(all_polygons_after_merging, adaptive_viz_scales[layer_idx])
        layer_2_polygons_split_vgroup = viz_3d_polygons(all_polygons_after_merging_scaled, layer_idx, colors=None)
        self.add(layer_2_polygons_split_vgroup)
        all_polygons_after_merging_2d = []
        for p in all_polygons_after_merging:
            pd2 = [o[:, :2] for o in p]
            all_polygons_after_merging_2d.append(pd2)
        layer3_regions_2d = find_polygon_intersections(all_polygons_after_merging_2d)
        output_poygons_2d_2 = viz_carved_regions_flat(layer3_regions_2d, horizontal_spacing, layer_idx, colors=None)
        self.add(output_poygons_2d_2)
        layer_idx = 4
        layer_3_polygons_3d = get_3d_polygons(layer3_regions_2d, num_neurons[layer_idx], surface_funcs_no_viz_scale, layer_idx)
        scaled_layer_3_polygons_3d = apply_viz_scale_to_3d_polygons(layer_3_polygons_3d, adaptive_viz_scales[layer_idx])
        polygons_vgroup_3 = viz_3d_polygons(scaled_layer_3_polygons_3d, layer_idx, colors=None)
        self.add(polygons_vgroup_3)
        map_img = ImageMobject(graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png').set_width(2).set_height(2)
        map_img.shift([horizontal_spacing * (layer_idx + 1) - 6, 0, -1.5])
        self.add(map_img)
        map_region_1 = ImageMobject(heatmaps_dir + '/8_8_0.png').set_width(2).set_height(2).set_opacity(0.3)
        map_region_1.shift([horizontal_spacing * (layer_idx + 1) - 6, 0, -1.5])
        self.add(map_region_1)
        map_region_2 = ImageMobject(heatmaps_dir + '/8_8_1.png').set_width(2).set_height(2).set_opacity(0.5)
        map_region_2.shift([horizontal_spacing * (layer_idx + 1) - 6, 0, -1.5])
        self.add(map_region_2)
        scaled_final_polygons = copy.deepcopy(scaled_layer_3_polygons_3d)
        polygons_vgroup_4a = viz_3d_polygons([scaled_final_polygons[0]], layer_idx=5, colors=[BLUE])
        polygons_vgroup_4b = viz_3d_polygons([scaled_final_polygons[1]], layer_idx=5, colors=[YELLOW])
        self.add(polygons_vgroup_4a, polygons_vgroup_4b)
        final_polygons = copy.deepcopy(layer_3_polygons_3d)
        intersection_line_coords, new_tiling, top_polygons, indicator = intersect_polytopes(final_polygons[0], final_polygons[1])
        intersection_line_coords_scaled = copy.deepcopy(intersection_line_coords)
        for line in intersection_line_coords_scaled:
            for l in line:
                l[2] = l[2] * adaptive_viz_scales[layer_idx][0]
        decision_boundary_lines = Group()
        for line_segment in intersection_line_coords_scaled:
            if len(line_segment) == 2:
                start_point, end_point = line_segment
                line = Line3D(start=start_point, end=end_point, color='#FF00FF', width=0.02)
                line.shift([horizontal_spacing * (layer_idx + 1) - 6, 0, 0])
                decision_boundary_lines.add(line)
        self.add(decision_boundary_lines)
        decision_boundary_lines_flat = Group()
        for line_segment in intersection_line_coords_scaled:
            if len(line_segment) == 2:
                start_point, end_point = line_segment
                start_point[2] = -1.5
                end_point[2] = -1.5
                line = Line3D(start=start_point, end=end_point, color='#FF00FF', width=0.02)
                line.shift([horizontal_spacing * (layer_idx + 1) - 6, 0, 0])
                decision_boundary_lines_flat.add(line)
        self.add(decision_boundary_lines_flat)
        output_poygons_2d_final = viz_carved_regions_flat(new_tiling, horizontal_spacing, layer_idx + 2, colors=None)
        self.add(output_poygons_2d_final)
        decision_boundary_lines_flat = Group()
        for line_segment in intersection_line_coords_scaled:
            if len(line_segment) == 2:
                start_point, end_point = line_segment
                start_point[2] = -1.5
                end_point[2] = -1.5
                line = Line3D(start=start_point, end=end_point, color='#FF00FF', width=0.02)
                line.shift([horizontal_spacing * (layer_idx + 2) - 6, 0, 0])
                decision_boundary_lines_flat.add(line)
        self.add(decision_boundary_lines_flat)
        decision_boundary_lines_flat.set_opacity(0.3)
        hyperspace_polygons = []
        for poly_2d in new_tiling:
            hyperspace_polygon = []
            for pt in poly_2d:
                pt_copy = copy.deepcopy(list(pt))
                for j, surf_func in enumerate(surface_funcs_no_viz_scale[4]):
                    pt_copy.append(surf_func(*pt)[-1])
                hyperspace_polygon.append(pt_copy)
            hyperspace_polygons.append(np.array(hyperspace_polygon))
        my_top_polygons = []
        my_indicator = []
        for p in hyperspace_polygons:
            if np.all(p[:, 2] > p[:, 3]):
                my_top_polygons.append(p[:, (0, 1, 2)])
                my_indicator.append(0)
            elif np.all(p[:, 3] > p[:, 2]):
                my_top_polygons.append(p[:, (0, 1, 3)])
                my_indicator.append(1)
            elif np.max(p[:, 2]) > np.max(p[:, 3]):
                my_top_polygons.append(p[:, (0, 1, 2)])
                my_indicator.append(0)
            elif np.max(p[:, 3]) > np.max(p[:, 2]):
                my_top_polygons.append(p[:, (0, 1, 3)])
                my_indicator.append(1)
        polygons_vgroup = VGroup()
        for j, p in enumerate(my_top_polygons):
            if len(p) < 3:
                continue
            if my_indicator[j]:
                color = YELLOW
            else:
                color = BLUE
            p_scaled = copy.deepcopy(p)
            p_scaled[:, 2] = p_scaled[:, 2] * adaptive_viz_scales[layer_idx][0]
            poly_3d = Polygon(*p_scaled, fill_color=color, fill_opacity=0.4, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([horizontal_spacing * (layer_idx + 1) - 6, 0, 2])
            polygons_vgroup.add(poly_3d)
        self.add(polygons_vgroup)
        self.wait()
        self.embed()