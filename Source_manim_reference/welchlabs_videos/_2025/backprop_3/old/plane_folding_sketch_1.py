from manimlib import *
from functools import partial
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#6e9671'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
graphics_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/backprop_3/graphics/'

def get_relu_joint(weight_1, weight_2, bias, extent=1):
    if np.abs(weight_2) < 1e-08:
        x_intercept = -bias / weight_1
        return [[x_intercept, -extent], [x_intercept, extent]] if -extent <= x_intercept <= extent else []
    elif np.abs(weight_1) < 1e-08:
        y_intercept = -bias / weight_2
        return [[-extent, y_intercept], [extent, y_intercept]] if -extent <= y_intercept <= extent else []
    else:
        points = []
        for x in [-extent, extent]:
            y = (-x * weight_1 - bias) / weight_2
            if -extent <= y <= extent:
                points.append([x, y])
        for y in [-extent, extent]:
            x = (-y * weight_2 - bias) / weight_1
            if -extent <= x <= extent:
                points.append([x, y])
        unique_points = []
        for p in points:
            is_duplicate = False
            for existing in unique_points:
                if abs(p[0] - existing[0]) < 1e-08 and abs(p[1] - existing[1]) < 1e-08:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_points.append(p)
        return unique_points

def line_from_joint_points_1(joint_points, stroke_width=3):
    if joint_points:
        joint_3d_points = []
        for point in joint_points:
            x, y = point
            z = 0
            joint_3d_points.append([x, y, z])
        if len(joint_3d_points) >= 2:
            joint_line = DashedLine(start=[joint_points[0][0], joint_points[0][1], 0], end=[joint_points[1][0], joint_points[1][1], 0], color=WHITE, stroke_width=stroke_width, dash_length=0.05)
            return joint_line

def surface_func_general(u, v, w1, w2, b, viz_scale=0.5):
    linear_output = w1 * u + w2 * v + b
    relu_output = max(0, linear_output)
    z = relu_output * viz_scale
    return np.array([u, v, z])

def surface_func_second_layer(u, v, w1, b1, w2, b2, neuron_idx=0, viz_scale=0.5):
    linear_output_1 = w1[0, 0] * u + w1[0, 1] * v + b1[0]
    relu_output_1 = max(0, linear_output_1)
    linear_output_2 = w1[1, 0] * u + w1[1, 1] * v + b1[1]
    relu_output_2 = max(0, linear_output_2)
    second_layer_input = w2[neuron_idx, 0] * relu_output_1 + w2[neuron_idx, 1] * relu_output_2 + b2[neuron_idx]
    second_layer_output = max(0, second_layer_input)
    z = second_layer_output * viz_scale
    return np.array([u, v, z])

def get_second_layer_joints(w1, b1, w2, b2, neuron_idx=0, extent=1):
    joint_lines = []
    joint_points_1 = get_relu_joint(w1[0, 0], w1[0, 1], b1[0], extent)
    joint_points_2 = get_relu_joint(w1[1, 0], w1[1, 1], b1[1], extent)
    if joint_points_1:
        joint_lines.append(joint_points_1)
    if joint_points_2:
        joint_lines.append(joint_points_2)
    regions = [(False, False), (True, False), (False, True), (True, True)]
    for relu1_active, relu2_active in regions:
        w2_eff = w2[neuron_idx, :]
        b2_eff = b2[neuron_idx]
        if relu1_active and relu2_active:
            eff_w1 = w2_eff[0] * w1[0, 0] + w2_eff[1] * w1[1, 0]
            eff_w2 = w2_eff[0] * w1[0, 1] + w2_eff[1] * w1[1, 1]
            eff_b = w2_eff[0] * b1[0] + w2_eff[1] * b1[1] + b2_eff
        elif relu1_active and (not relu2_active):
            eff_w1 = w2_eff[0] * w1[0, 0]
            eff_w2 = w2_eff[0] * w1[0, 1]
            eff_b = w2_eff[0] * b1[0] + b2_eff
        elif not relu1_active and relu2_active:
            eff_w1 = w2_eff[1] * w1[1, 0]
            eff_w2 = w2_eff[1] * w1[1, 1]
            eff_b = w2_eff[1] * b1[1] + b2_eff
        elif abs(b2_eff) < 1e-08:
            continue
        else:
            continue
        region_joints = get_relu_joint(eff_w1, eff_w2, eff_b, extent)
        if region_joints:
            clipped_joints = clip_joint_to_region(region_joints, relu1_active, relu2_active, w1, b1, extent)
            if clipped_joints:
                joint_lines.append(clipped_joints)
    return joint_lines

def clip_joint_to_region(joint_points, relu1_active, relu2_active, w1, b1, extent):
    if not joint_points or len(joint_points) < 2:
        return []
    start, end = (joint_points[0], joint_points[1])
    clipped_points = []
    for t in np.linspace(0, 1, 100):
        x = start[0] + t * (end[0] - start[0])
        y = start[1] + t * (end[1] - start[1])
        linear1 = w1[0, 0] * x + w1[0, 1] * y + b1[0]
        linear2 = w1[1, 0] * x + w1[1, 1] * y + b1[1]
        relu1_here = linear1 > 0
        relu2_here = linear2 > 0
        if relu1_here == relu1_active and relu2_here == relu2_active:
            clipped_points.append([x, y])
    if len(clipped_points) >= 2:
        return [clipped_points[0], clipped_points[-1]]
    else:
        return []

def create_second_layer_joint_lines(w1, b1, w2, b2, neuron_idx=0, extent=1):
    joint_lines = get_second_layer_joints(w1, b1, w2, b2, neuron_idx, extent)
    manim_lines = []
    colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
    for i, joint_points in enumerate(joint_lines):
        if len(joint_points) >= 2:
            color = colors[i % len(colors)]
            joint_line = DashedLine(start=[joint_points[0][0], joint_points[0][1], 0], end=[joint_points[1][0], joint_points[1][1], 0], color=color, stroke_width=3, dash_length=0.05)
            manim_lines.append(joint_line)
    return manim_lines

class plane_folding_sketch_1(InteractiveScene):

    def construct(self):
        w1 = np.array([[-0.02866297, 1.6250265], [-1.3056537, 0.46831134]], dtype=np.float32)
        b1 = np.array([-0.4677289, 1.0067637], dtype=np.float32)
        w2 = np.array([[1.3398709, 0.68694556], [-0.29886743, -1.8411286]], dtype=np.float32)
        b2 = np.array([-0.7817721, 0.90856946], dtype=np.float32)
        w3 = np.array([[1.8897862, 3.0432484], [-1.7220999, -2.2057745]], dtype=np.float32)
        b3 = np.array([-1.0249746, 0.61326534], dtype=np.float32)
        map_img = ImageMobject(graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
        map_img.set_height(2)
        map_img.set_width(2)
        map_img.move_to(ORIGIN)
        self.frame.reorient(0, 0, 0, (0.03, -0.02, 0.0), 3.27)
        surface_func_11 = partial(surface_func_general, w1=w1[0, 0], w2=w1[0, 1], b=b1[0], viz_scale=0.3)
        bent_surface_11 = ParametricSurface(surface_func_11, u_range=[-1, 1], v_range=[-1, 1], resolution=(50, 50))
        ts11 = TexturedSurface(bent_surface_11, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
        ts11.set_shading(0, 0, 0)
        ts11.set_opacity(0.75)
        joint_points_11 = get_relu_joint(w1[0, 0], w1[0, 1], b1[0], extent=1)
        joint_line_11 = line_from_joint_points_1(joint_points_11).set_opacity(0.8)
        group_11 = Group(ts11, joint_line_11)
        surface_func_12 = partial(surface_func_general, w1=w1[1, 0], w2=w1[1, 1], b=b1[1], viz_scale=0.3)
        bent_surface_12 = ParametricSurface(surface_func_12, u_range=[-1, 1], v_range=[-1, 1], resolution=(50, 50))
        ts12 = TexturedSurface(bent_surface_12, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
        ts12.set_shading(0, 0, 0)
        ts12.set_opacity(0.75)
        joint_points_12 = get_relu_joint(w1[1, 0], w1[1, 1], b1[1], extent=1)
        joint_line_12 = line_from_joint_points_1(joint_points_12).set_opacity(0.8)
        group_12 = Group(ts12, joint_line_12)
        self.add(group_11)
        self.add(group_12)
        group_12.move_to([0, 0, 1.2])
        self.wait()
        surface_func_21 = partial(surface_func_second_layer, w1=w1, b1=b1, w2=w2, b2=b2, neuron_idx=1, viz_scale=0.3)
        self.wait()
        bent_surface_21 = ParametricSurface(surface_func_21, u_range=[-1, 1], v_range=[-1, 1], resolution=(50, 50))
        ts21 = TexturedSurface(bent_surface_21, graphics_dir + '/baarle_hertog_maps/baarle_hertog_maps-11.png')
        ts21.set_shading(0, 0, 0)
        ts21.set_opacity(0.75)
        joint_lines_21 = create_second_layer_joint_lines(w1, b1, w2, b2, neuron_idx=1, extent=1)
        group_21_lines = Group(*joint_lines_21)
        group_21 = Group(ts21, group_21_lines)
        group_21.move_to([0, 0, 2.4])
        self.add(group_21)
        self.wait(20)
        self.embed()