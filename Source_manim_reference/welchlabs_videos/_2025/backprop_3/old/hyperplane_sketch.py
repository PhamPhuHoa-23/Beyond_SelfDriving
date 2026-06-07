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
        self.frame.reorient(0, 56, 0, (-0.06, -0.01, 1.23), 9.57)
        layer_idx = 0
        relu_intersections_planes_1 = get_relu_intersection_planes(num_neurons[layer_idx], layer_idx, neuron_idx, horizontal_spacing, vertical_spacing)
        self.add(relu_intersections_planes_1)
        layer_idx = 1
        layer_1_polygons = get_polygon_corners_layer_1(model)
        layer_1_polygons_3d = get_3d_polygons_layer_1(layer_1_polygons, surface_funcs_no_viz_scale, num_neurons=num_neurons[layer_idx], layer_idx=1)
        scaled_layer_1_polygons_3d = apply_viz_scale_to_3d_polygons(layer_1_polygons_3d, adaptive_viz_scales[layer_idx])
        polygons_vgroup = viz_3d_polygons(scaled_layer_1_polygons_3d, layer_idx, colors=None, color_gray_index=1)
        self.add(polygons_vgroup)
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
        hyperspace_polygons = []
        for poly_2d in layer_2_polygons:
            hyperspace_polygon = []
            for pt in poly_2d:
                pt_copy = copy.deepcopy(list(pt))
                for j, surf_func in enumerate(surface_funcs_no_viz_scale[2]):
                    pt_copy.append(surf_func(*pt)[-1])
                hyperspace_polygon.append(pt_copy)
            hyperspace_polygons.append(np.array(hyperspace_polygon))
        axes_1 = ThreeDAxes(x_range=[-8, 8, 1], y_range=[-8, 8, 1], z_range=[-8, 8, 1], height=3, width=3, depth=3, axis_config={'include_ticks': True, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'tip_config': {'fill_opacity': 1, 'width': 0.1, 'length': 0.1}})
        axes_1.move_to([0 * horizontal_spacing, 0, 6])
        self.add(axes_1)
        polygons_activation_space_1 = VGroup()
        for j, polygon in enumerate(hyperspace_polygons):
            color = colors[j % len(colors)]
            pts = []
            for pt in polygon:
                pts.append(axes_1.c2p(pt[2], pt[3], pt[4]))
            poly_3d = Polygon(*pts, fill_color=color, fill_opacity=0.7, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.3)
            polygons_activation_space_1.add(poly_3d)
        self.add(polygons_activation_space_1)
        hyperspace_polygons = []
        for poly_2d in layer3_regions_2d:
            hyperspace_polygon = []
            for pt in poly_2d:
                pt_copy = copy.deepcopy(list(pt))
                for j, surf_func in enumerate(surface_funcs_no_viz_scale[3]):
                    pt_copy.append(surf_func(*pt)[-1])
                hyperspace_polygon.append(pt_copy)
            hyperspace_polygons.append(np.array(hyperspace_polygon))
        axes_2 = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-4, 4, 1], height=3, width=3, depth=3, axis_config={'include_ticks': True, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'tip_config': {'fill_opacity': 1, 'width': 0.1, 'length': 0.1}})
        axes_2.move_to([horizontal_spacing, 0, 6])
        self.add(axes_2)
        polygons_activation_space_2 = VGroup()
        for j, polygon in enumerate(hyperspace_polygons):
            color = colors[j % len(colors)]
            pts = []
            for pt in polygon:
                pts.append(axes_2.c2p(pt[2], pt[3], pt[4]))
            poly_3d = Polygon(*pts, fill_color=color, fill_opacity=0.7, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.9)
            polygons_activation_space_2.add(poly_3d)
        self.add(polygons_activation_space_2)
        layer_idx = 4
        layer_3_polygons_3d = get_3d_polygons(layer3_regions_2d, num_neurons[layer_idx], surface_funcs_no_viz_scale, layer_idx)
        scaled_layer_3_polygons_3d = apply_viz_scale_to_3d_polygons(layer_3_polygons_3d, adaptive_viz_scales[layer_idx])
        polygons_vgroup_3 = viz_3d_polygons(scaled_layer_3_polygons_3d, layer_idx, colors=None)
        self.add(polygons_vgroup_3)
        hyperspace_polygons = []
        for poly_2d in layer3_regions_2d:
            hyperspace_polygon = []
            for pt in poly_2d:
                pt_copy = copy.deepcopy(list(pt))
                for j, surf_func in enumerate(surface_funcs_no_viz_scale[4]):
                    pt_copy.append(surf_func(*pt)[-1])
                hyperspace_polygon.append(pt_copy)
            hyperspace_polygons.append(np.array(hyperspace_polygon))
        axes_3 = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-4, 4, 1], height=3, width=3, depth=3, axis_config={'include_ticks': True, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'tip_config': {'fill_opacity': 1, 'width': 0.1, 'length': 0.1}})
        axes_3.move_to([2 * horizontal_spacing, 0, 5])
        self.add(axes_3)
        polygons_activation_space_3 = VGroup()
        for j, polygon in enumerate(hyperspace_polygons):
            color = colors[j % len(colors)]
            pts = []
            for pt in polygon:
                pts.append(axes_3.c2p(pt[2], pt[3], 0))
            poly_3d = Polygon(*pts, fill_color=color, fill_opacity=0.7, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.9)
            polygons_activation_space_3.add(poly_3d)
        self.add(polygons_activation_space_3)
        self.wait()
        self.embed()