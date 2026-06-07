from manimlib import *
from functools import partial
import sys
import pickle
sys.path.append('_2025/backprop_3')
from plane_folding_utils import *
from decision_boundary_utils import *
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#6e9671'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
graphics_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/graphics/'

class goemetry_while_learning_1b(InteractiveScene):

    def construct(self):
        map_img = ImageMobject(graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
        map_img.set_height(2)
        map_img.set_width(2)
        map_img.move_to(ORIGIN)
        viz_scale_1 = 0.25
        viz_scale_2 = 0.1
        pickle_path = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/hackin/3_training_weights_1/training_data_seed_13_acc_0.6098.pkl'
        with open(pickle_path, 'rb') as f:
            p = pickle.load(f)
        self.frame.reorient(1, 58, 0, (-0.17, 2.27, -0.1), 8.46)
        step_size = 10
        for i in range(250):
            train_step = step_size * i
            w1 = p['weights_history'][train_step]['model.0.weight'].numpy()
            b1 = p['weights_history'][train_step]['model.0.bias'].numpy()
            w2 = p['weights_history'][train_step]['model.2.weight'].numpy()
            b2 = p['weights_history'][train_step]['model.2.bias'].numpy()
            surface_func_11 = partial(surface_func_general, w1=w1[0, 0], w2=w1[0, 1], b=b1[0], viz_scale=viz_scale_1)
            bent_surface_11 = ParametricSurface(surface_func_11, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
            ts11 = TexturedSurface(bent_surface_11, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
            ts11.set_shading(0, 0, 0)
            ts11.set_opacity(0.75)
            joint_points_11 = get_relu_joint(w1[0, 0], w1[0, 1], b1[0], extent=1)
            joint_line_11 = line_from_joint_points_1(joint_points_11).set_opacity(0.5)
            group_11 = Group(ts11, joint_line_11)
            surface_func_12 = partial(surface_func_general, w1=w1[1, 0], w2=w1[1, 1], b=b1[1], viz_scale=viz_scale_1)
            bent_surface_12 = ParametricSurface(surface_func_12, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
            ts12 = TexturedSurface(bent_surface_12, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
            ts12.set_shading(0, 0, 0)
            ts12.set_opacity(0.75)
            joint_points_12 = get_relu_joint(w1[1, 0], w1[1, 1], b1[1], extent=1)
            joint_line_12 = line_from_joint_points_1(joint_points_12).set_opacity(0.5)
            group_12 = Group(ts12, joint_line_12)
            surface_func_13 = partial(surface_func_general, w1=w1[2, 0], w2=w1[2, 1], b=b1[2], viz_scale=viz_scale_1)
            bent_surface_13 = ParametricSurface(surface_func_13, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
            ts13 = TexturedSurface(bent_surface_13, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
            ts13.set_shading(0, 0, 0)
            ts13.set_opacity(0.75)
            joint_points_13 = get_relu_joint(w1[2, 0], w1[2, 1], b1[2], extent=1)
            joint_line_13 = line_from_joint_points_1(joint_points_13).set_opacity(0.5)
            group_13 = Group(ts13, joint_line_13)
            group_13.shift([-3, 0, 3])
            group_12.shift([-3, 0, 1.5])
            group_11.shift([-3, 0, 0])
            neuron_idx = 0
            surface_func_21 = partial(surface_func_second_layer_no_relu_multi, w1=w1, b1=b1, w2=w2, b2=b2, neuron_idx=neuron_idx, viz_scale=viz_scale_2)
            bent_surface_21 = ParametricSurface(surface_func_21, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
            ts21 = TexturedSurface(bent_surface_21, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
            ts21.set_shading(0, 0, 0)
            ts21.set_opacity(0.75)
            bs21_copy = bent_surface_21.copy()
            ts21_copy = ts21.copy()
            joint_points_list = [joint_points_11, joint_points_12, joint_points_13]
            polygons = get_polygon_corners_multi(joint_points_list, extent=1)
            ts21.shift([0, 0, 1.5])
            polygon_3d_objects = create_3d_polygon_regions_multi(polygons, w1, b1, w2, b2, neuron_idx=neuron_idx, viz_scale=viz_scale_2)
            polygon_3d_objects_copy = create_3d_polygon_regions_multi(polygons, w1, b1, w2, b2, neuron_idx=neuron_idx, viz_scale=viz_scale_2)
            neuron_idx = 1
            surface_func_22 = partial(surface_func_second_layer_no_relu_multi, w1=w1, b1=b1, w2=w2, b2=b2, neuron_idx=neuron_idx, viz_scale=viz_scale_2)
            bent_surface_22 = ParametricSurface(surface_func_22, u_range=[-1, 1], v_range=[-1, 1], resolution=(64, 64))
            ts22 = TexturedSurface(bent_surface_22, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
            ts22.set_shading(0, 0, 0)
            ts22.set_opacity(0.75)
            bs22_copy = bent_surface_22.copy()
            ts22_copy = ts22.copy()
            polygon_3d_objects_2 = create_3d_polygon_regions_multi(polygons, w1, b1, w2, b2, neuron_idx=neuron_idx, viz_scale=viz_scale_2)
            polygon_3d_objects_2_copy = create_3d_polygon_regions_multi(polygons, w1, b1, w2, b2, neuron_idx=neuron_idx, viz_scale=viz_scale_2)
            bs21_copy.move_to([3, 0, 0.75])
            ts21_copy.move_to([3, 0, 0.75])
            bs22_copy.move_to([3, 0, 0.75])
            ts22_copy.move_to([3, 0, 0.75])
            map_img.move_to([3, 0, 0.5])
            decision_boundaries = create_decision_boundary_lines(w1, b1, w2, b2, polygons, extent=1, z_offset=0, color=WHITE, stroke_width=4)
            self.add(group_11, group_12, group_13)
            self.add(ts21)
            for poly in polygon_3d_objects:
                poly.set_opacity(0.3)
                poly.shift([0, 0, 1.5])
                self.add(poly)
            self.add(ts22)
            for poly in polygon_3d_objects_2:
                poly.set_opacity(0.3)
                self.add(poly)
            self.add(map_img)
            for poly in polygon_3d_objects_copy:
                poly.set_opacity(0.3).set_color(BLUE)
                poly.shift([3, 0, 0.75])
                self.add(poly)
            for poly in polygon_3d_objects_2_copy:
                poly.set_opacity(0.3).set_color(YELLOW)
                poly.shift([3, 0, 0.75])
                self.add(poly)
            if len(decision_boundaries) > 0:
                decision_boundaries[0].shift([3, 0, 0.75])
                self.add(decision_boundaries[0])
            self.wait(0.1)
            self.remove(group_11, group_12, group_13, ts21, ts22, map_img)
            if len(decision_boundaries) > 0:
                self.remove(decision_boundaries[0])
            for poly in polygon_3d_objects + polygon_3d_objects_2 + polygon_3d_objects_copy + polygon_3d_objects_2_copy:
                self.remove(poly)
        self.embed()