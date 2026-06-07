from manimlib import *
from functools import partial
from itertools import combinations
import math
import torch.nn as nn
import torch
import copy

class BaarleNet(nn.Module):

    def __init__(self, hidden_layers=[64]):
        super(BaarleNet, self).__init__()
        layers = [nn.Linear(2, hidden_layers[0]), nn.ReLU()]
        for i in range(len(hidden_layers) - 1):
            layers.append(nn.Linear(hidden_layers[i], hidden_layers[i + 1]))
            layers.append(nn.ReLU())
        layers.append(nn.Linear(hidden_layers[-1], 2))
        self.layers = layers
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

def manim_polygons_from_np_list(np_polygon_list, colors=None, viz_scale=1.0, stroke_width=2, polygon_max_height=None, opacity=0.3):
    if colors is None:
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]
    polygons = VGroup()
    list_copy = copy.deepcopy(np_polygon_list)
    for j, p in enumerate(list_copy):
        if len(p) < 3:
            continue
        p[:, 2] = p[:, 2] * viz_scale
        if polygon_max_height is not None:
            p[:, -1] = np.clip(p[:, -1], -polygon_max_height, polygon_max_height)
        poly_3d = Polygon(*p, fill_color=colors[j % len(colors)], fill_opacity=0.7, stroke_color=colors[j % len(colors)], stroke_width=stroke_width)
        poly_3d.set_opacity(opacity)
        polygons.add(poly_3d)
    return polygons

def get_relu_intersection_planes(num_neurons, layer_idx, neuron_idx, horizontal_spacing, vertical_spacing):
    relu_intersections_planes = VGroup()
    for neuron_idx in range(num_neurons):
        plane = Rectangle(width=2, height=2, fill_color=GREY, fill_opacity=0.15, stroke_color=WHITE, stroke_width=0.5)
        plane.shift([horizontal_spacing * layer_idx - 6, 0, vertical_spacing * neuron_idx])
        relu_intersections_planes.add(plane)
    return relu_intersections_planes

def get_3d_polygons_layer_1(layer_1_polygons, surface_funcs, num_neurons, layer_idx=1):
    layer_1_polygons_3d = []
    for neuron_idx in range(num_neurons):
        layer_1_polygons_3d.append([])
        for region in ['positive_region', 'negative_region']:
            a = []
            for pt_idx in range(len(layer_1_polygons[neuron_idx][region])):
                a.append(surface_funcs[layer_idx][neuron_idx](*layer_1_polygons[neuron_idx][region][pt_idx]))
            a = np.array(a)
            layer_1_polygons_3d[-1].append(a)
    return layer_1_polygons_3d

def get_3d_polygons(polygons_2d, num_neurons, surface_funcs, layer_idx):
    polygons_3d = []
    for neuron_idx in range(num_neurons):
        polygons_3d.append([])
        for region in polygons_2d:
            a = []
            for pt_idx in range(len(region)):
                a.append(surface_funcs[layer_idx][neuron_idx](*region[pt_idx]))
            a = np.array(a)
            polygons_3d[-1].append(a)
    return polygons_3d

def viz_3d_polygons(polygons_3d, layer_idx, colors=None, color_gray_index=0):
    if colors == None:
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]
    polygons_vgroup = VGroup()
    for neuron_idx, polygons in enumerate(polygons_3d):
        for j, p in enumerate(polygons):
            if len(p) < 3:
                continue
            color = colors[j % len(colors)]
            if color_gray_index is not None:
                if color_gray_index == j:
                    color = GREY
            else:
                color = colors[j % len(colors)]
            poly_3d = Polygon(*p, fill_color=color, fill_opacity=0.7, stroke_color=color, stroke_width=2)
            poly_3d.set_opacity(0.3)
            poly_3d.shift([3 * layer_idx - 6, 0, 1.5 * neuron_idx])
            polygons_vgroup.add(poly_3d)
    return polygons_vgroup

def viz_carved_regions_flat(layer_2_polygons, horizontal_spacing, layer_idx, colors=None):
    if colors == None:
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE, PINK, TEAL]
    output_poygons_2d = VGroup()
    for j, polygon in enumerate(layer_2_polygons):
        polygon = Polygon(*np.hstack((np.array(polygon), np.zeros((len(polygon), 1)))), fill_color=colors[j % len(colors)], fill_opacity=0.7, stroke_color=colors[j % len(colors)], stroke_width=2)
        polygon.set_opacity(0.3)
        polygon.shift([horizontal_spacing * layer_idx - 6, 0, -1.5])
        output_poygons_2d.add(polygon)
    return output_poygons_2d

def compute_adaptive_viz_scales(model, max_surface_height=0.75, extent=1):
    available_viz_scales = [1.0, 0.5, 0.25, 0.15, 0.125, 0.1, 0.075, 0.05, 0.025, 0.01, 0.0075, 0.005, 0.0025, 0.001]
    test_points = torch.tensor([[-extent, -extent], [-extent, extent], [extent, -extent], [extent, extent]], dtype=torch.float32)
    adaptive_scales = []
    for layer_idx in range(len(model.model)):
        current_layer = model.model[layer_idx]
        if isinstance(current_layer, torch.nn.ReLU):
            if layer_idx > 0 and len(adaptive_scales) > 0:
                previous_scales = adaptive_scales[-1].copy()
                adaptive_scales.append(previous_scales)
            else:
                with torch.no_grad():
                    x = test_points
                    for i in range(layer_idx + 1):
                        x = model.model[i](x)
                num_neurons = x.shape[1]
                layer_scales = []
                for neuron_idx in range(num_neurons):
                    neuron_activations = x[:, neuron_idx].numpy()
                    max_abs_activation = np.max(np.abs(neuron_activations))
                    selected_scale = available_viz_scales[-1]
                    for scale in available_viz_scales:
                        max_viz_height = max_abs_activation * scale
                        if max_viz_height <= max_surface_height:
                            selected_scale = scale
                            break
                    layer_scales.append(selected_scale)
                adaptive_scales.append(layer_scales)
        else:
            with torch.no_grad():
                x = test_points
                for i in range(layer_idx + 1):
                    x = model.model[i](x)
            num_neurons = x.shape[1]
            layer_scales = []
            for neuron_idx in range(num_neurons):
                neuron_activations = x[:, neuron_idx].numpy()
                max_abs_activation = np.max(np.abs(neuron_activations))
                selected_scale = available_viz_scales[-1]
                for scale in available_viz_scales:
                    max_viz_height = max_abs_activation * scale
                    if max_viz_height <= max_surface_height:
                        selected_scale = scale
                        break
                layer_scales.append(selected_scale)
            adaptive_scales.append(layer_scales)
    return adaptive_scales

def surface_func_from_model(u, v, model, layer_idx, neuron_idx, viz_scale=0.5):
    input_tensor = torch.tensor([[u, v]], dtype=torch.float32)
    with torch.no_grad():
        x = input_tensor
        for i in range(layer_idx + 1):
            x = model.model[i](x)
        activation = x[0, neuron_idx].item()
        z = activation * viz_scale
        return np.array([u, v, z])

def get_polygon_corners_layer_1(model):
    first_layer = model.model[0]
    weights = first_layer.weight.detach().numpy()
    biases = first_layer.bias.detach().numpy()
    boundary = [-1, 1, -1, 1]
    x_min, x_max, y_min, y_max = boundary
    square_corners = [[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]
    polygons_per_neuron = []
    for neuron_idx in range(weights.shape[0]):
        w1, w2 = weights[neuron_idx]
        b = biases[neuron_idx]
        intersections = []
        edges = [([x_min, y_min], [x_max, y_min]), ([x_max, y_min], [x_max, y_max]), ([x_max, y_max], [x_min, y_max]), ([x_min, y_max], [x_min, y_min])]
        for edge_start, edge_end in edges:
            if edge_start[0] == edge_end[0]:
                x = edge_start[0]
                if w2 != 0:
                    y = -(w1 * x + b) / w2
                    if y_min <= y <= y_max:
                        intersections.append([x, y])
            else:
                y = edge_start[1]
                if w1 != 0:
                    x = -(w2 * y + b) / w1
                    if x_min <= x <= x_max:
                        intersections.append([x, y])
        unique_intersections = []
        for point in intersections:
            is_duplicate = False
            for existing in unique_intersections:
                if abs(point[0] - existing[0]) < 1e-06 and abs(point[1] - existing[1]) < 1e-06:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_intersections.append(point)
        if len(unique_intersections) >= 2:
            p1, p2 = (unique_intersections[0], unique_intersections[1])

            def side_of_line(point, line_p1, line_p2):
                return (line_p2[0] - line_p1[0]) * (point[1] - line_p1[1]) - (line_p2[1] - line_p1[1]) * (point[0] - line_p1[0])
            positive_corners = []
            negative_corners = []
            for corner in square_corners:
                activation = w1 * corner[0] + w2 * corner[1] + b
                if activation >= 0:
                    positive_corners.append(corner)
                else:
                    negative_corners.append(corner)
            positive_polygon = positive_corners + unique_intersections
            negative_polygon = negative_corners + unique_intersections

            def sort_polygon_points(points):
                if len(points) < 3:
                    return points
                cx = sum((p[0] for p in points)) / len(points)
                cy = sum((p[1] for p in points)) / len(points)

                def angle_from_center(point):
                    return np.arctan2(point[1] - cy, point[0] - cx)
                return sorted(points, key=angle_from_center)
            positive_polygon = sort_polygon_points(positive_polygon)
            negative_polygon = sort_polygon_points(negative_polygon)
            polygons_per_neuron.append({'positive_region': positive_polygon, 'negative_region': negative_polygon, 'relu_line': unique_intersections, 'line_equation': f'{w1:.3f}*x + {w2:.3f}*y + {b:.3f} = 0'})
        elif b >= 0:
            polygons_per_neuron.append({'positive_region': square_corners, 'negative_region': [], 'relu_line': [], 'line_equation': f'{w1:.3f}*x + {w2:.3f}*y + {b:.3f} = 0'})
        else:
            polygons_per_neuron.append({'positive_region': [], 'negative_region': square_corners, 'relu_line': [], 'line_equation': f'{w1:.3f}*x + {w2:.3f}*y + {b:.3f} = 0'})
    return polygons_per_neuron

def carve_plane_with_relu_joints(joint_points_list, extent=1):
    valid_lines = []
    for joint_points in joint_points_list:
        if joint_points and len(joint_points) >= 2:
            valid_lines.append(joint_points[:2])
    if len(valid_lines) == 0:
        return [[[-extent, -extent], [extent, -extent], [extent, extent], [-extent, extent]]]

    def line_equation(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        a = y2 - y1
        b = x1 - x2
        c = x2 * y1 - x1 * y2
        return (a, b, c)

    def evaluate_line(point, a, b, c):
        return a * point[0] + b * point[1] + c

    def line_intersection(p1, p2, p3, p4):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return None
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return [x, y]

    def clip_polygon_by_line(polygon, line_p1, line_p2):
        if not polygon:
            return []
        a, b, c = line_equation(line_p1, line_p2)
        output_polygon = []
        n = len(polygon)
        for i in range(n):
            current_vertex = polygon[i]
            previous_vertex = polygon[i - 1]
            current_side = evaluate_line(current_vertex, a, b, c)
            previous_side = evaluate_line(previous_vertex, a, b, c)
            if current_side >= -1e-10:
                if previous_side < -1e-10:
                    intersection = line_intersection(previous_vertex, current_vertex, line_p1, line_p2)
                    if intersection:
                        output_polygon.append(intersection)
                output_polygon.append(current_vertex)
            elif previous_side >= -1e-10:
                intersection = line_intersection(previous_vertex, current_vertex, line_p1, line_p2)
                if intersection:
                    output_polygon.append(intersection)
        return output_polygon
    initial_square = [[-extent, -extent], [extent, -extent], [extent, extent], [-extent, extent]]
    n_lines = len(valid_lines)
    polygons = []
    for region_idx in range(2 ** n_lines):
        current_polygon = initial_square[:]
        for line_idx in range(n_lines):
            if current_polygon:
                line = valid_lines[line_idx]
                if region_idx & 1 << line_idx:
                    current_polygon = clip_polygon_by_line(current_polygon, line[0], line[1])
                else:
                    current_polygon = clip_polygon_by_line(current_polygon, line[1], line[0])
        if len(current_polygon) >= 3:
            cleaned_polygon = []
            for vertex in current_polygon:
                is_duplicate = False
                for existing in cleaned_polygon:
                    if abs(vertex[0] - existing[0]) < 1e-08 and abs(vertex[1] - existing[1]) < 1e-08:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    cleaned_polygon.append(vertex)
            if len(cleaned_polygon) >= 3:
                polygons.append(cleaned_polygon)
    return polygons

def apply_relu_to_polygon(polygon):
    clipped_polygon = polygon.copy()
    clipped_polygon[:, 2] = np.maximum(clipped_polygon[:, 2], 0.0)
    return clipped_polygon

def apply_viz_scale_to_3d_polygons(polygons_3d, adaptive_viz_scales):
    scaled_polygons_3d = copy.deepcopy(polygons_3d)
    for neuron_idx, neuron_polygons in enumerate(scaled_polygons_3d):
        scale = adaptive_viz_scales[neuron_idx]
        for polygon_idx, polygon in enumerate(neuron_polygons):
            if len(polygon) > 0 and polygon.shape[1] >= 3:
                scaled_polygons_3d[neuron_idx][polygon_idx][:, 2] *= scale
    return scaled_polygons_3d

def split_polygons_with_relu(polygons):
    all_polygons = []
    merged_zero_polygons = []
    unmerged_polygons = []
    for neuron_idx, neuron_polygons in enumerate(polygons):
        neuron_all = []
        for polygon in neuron_polygons:
            if len(polygon) < 3:
                neuron_all.append(polygon)
                continue
            z_values = polygon[:, 2]
            min_z = np.min(z_values)
            max_z = np.max(z_values)
            if min_z >= 0 or max_z <= 0:
                clipped_polygon = apply_relu_to_polygon(polygon)
                neuron_all.append(clipped_polygon)
            else:
                split_polygons = split_polygon_at_z_zero(polygon)
                neuron_all.extend(split_polygons)
        all_polygons.append(neuron_all)
        zero_polygons = []
        nonzero_polygons = []
        for polygon in neuron_all:
            if is_zero_polygon(polygon):
                zero_polygons.append(polygon)
            else:
                nonzero_polygons.append(polygon)
        merged_zeros = merge_adjacent_polygons(zero_polygons)
        merged_zero_polygons.append(merged_zeros)
        unmerged_polygons.append(nonzero_polygons)
    return (all_polygons, merged_zero_polygons, unmerged_polygons)

def split_polygon_at_z_zero(polygon):
    n_points = len(polygon)
    if n_points < 3:
        return [polygon]
    intersection_points = []
    intersection_indices = []
    for i in range(n_points):
        curr_point = polygon[i]
        next_point = polygon[(i + 1) % n_points]
        curr_z = curr_point[2]
        next_z = next_point[2]
        if curr_z > 0 and next_z < 0 or (curr_z < 0 and next_z > 0):
            t = -curr_z / (next_z - curr_z)
            intersection = curr_point + t * (next_point - curr_point)
            intersection[2] = 0.0
            intersection_points.append(intersection)
            intersection_indices.append(i)
    if len(intersection_points) < 2:
        return [polygon]
    if len(intersection_points) > 2:
        intersection_points = intersection_points[:2]
        intersection_indices = intersection_indices[:2]
    positive_polygon = []
    negative_polygon = []
    int_point_1, int_point_2 = (intersection_points[0], intersection_points[1])
    for i in range(n_points):
        point = polygon[i]
        z_val = point[2]
        if z_val >= 0:
            positive_polygon.append(point)
        else:
            negative_polygon.append(point)
        if i in intersection_indices:
            intersection_idx = intersection_indices.index(i)
            intersection_point = intersection_points[intersection_idx]
            if z_val >= 0:
                negative_polygon.append(intersection_point)
            else:
                positive_polygon.append(intersection_point)
    for int_point in intersection_points:
        if len(positive_polygon) > 0 and (not any((np.allclose(int_point, p, atol=1e-08) for p in positive_polygon))):
            positive_polygon.append(int_point)
        if len(negative_polygon) > 0 and (not any((np.allclose(int_point, p, atol=1e-08) for p in negative_polygon))):
            negative_polygon.append(int_point)
    result_polygons = []
    if len(positive_polygon) >= 3:
        positive_polygon = np.array(positive_polygon)
        positive_polygon[:, 2] = np.maximum(positive_polygon[:, 2], 0.0)
        positive_polygon = sort_polygon_points_3d(positive_polygon)
        result_polygons.append(positive_polygon)
    if len(negative_polygon) >= 3:
        negative_polygon = np.array(negative_polygon)
        negative_polygon[:, 2] = np.maximum(negative_polygon[:, 2], 0.0)
        negative_polygon = sort_polygon_points_3d(negative_polygon)
        result_polygons.append(negative_polygon)
    return result_polygons if result_polygons else [apply_relu_to_polygon(polygon)]

def is_zero_polygon(polygon):
    return np.all(np.abs(polygon[:, 2]) < 1e-08)

def merge_adjacent_polygons(polygons):
    if len(polygons) <= 1:
        return polygons
    current_polygons = polygons[:]
    while True:
        merged_any = False
        new_polygons = []
        used = [False] * len(current_polygons)
        for i in range(len(current_polygons)):
            if used[i]:
                continue
            merge_group = [current_polygons[i]]
            used[i] = True
            added_to_group = True
            while added_to_group:
                added_to_group = False
                for j in range(len(current_polygons)):
                    if used[j]:
                        continue
                    for group_poly in merge_group:
                        if polygons_share_edge(group_poly, current_polygons[j]):
                            merge_group.append(current_polygons[j])
                            used[j] = True
                            added_to_group = True
                            merged_any = True
                            break
                    if added_to_group:
                        break
            if len(merge_group) == 1:
                new_polygons.append(merge_group[0])
            else:
                merged_polygon = merge_polygon_group(merge_group)
                new_polygons.append(merged_polygon)
        current_polygons = new_polygons
        if not merged_any:
            break
    return current_polygons

def polygons_share_edge(poly1, poly2, tolerance=1e-06):
    edges1 = get_polygon_edges(poly1)
    edges2 = get_polygon_edges(poly2)
    for edge1 in edges1:
        for edge2 in edges2:
            if edges_equal(edge1, edge2, tolerance) or edges_equal(edge1, (edge2[1], edge2[0]), tolerance):
                return True
    return False

def get_polygon_edges(polygon):
    edges = []
    n_points = len(polygon)
    for i in range(n_points):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n_points]
        edges.append((p1, p2))
    return edges

def edges_equal(edge1, edge2, tolerance=1e-06):
    p1_start, p1_end = edge1
    p2_start, p2_end = edge2
    return np.allclose(p1_start, p2_start, atol=tolerance) and np.allclose(p1_end, p2_end, atol=tolerance)

def merge_polygon_group(polygons):
    if len(polygons) == 1:
        return polygons[0]
    all_vertices = []
    for polygon in polygons:
        for vertex in polygon:
            is_duplicate = False
            for existing in all_vertices:
                if np.allclose(vertex, existing, atol=1e-08):
                    is_duplicate = True
                    break
            if not is_duplicate:
                all_vertices.append(vertex.copy())
    if len(all_vertices) < 3:
        return polygons[0]
    all_vertices = np.array(all_vertices)
    try:
        from scipy.spatial import ConvexHull
        hull_2d = ConvexHull(all_vertices[:, :2])
        boundary_indices = hull_2d.vertices
        boundary_vertices = all_vertices[boundary_indices]
        outer_boundary = find_outer_boundary_detailed(polygons)
        if outer_boundary is not None and len(outer_boundary) >= 3:
            return outer_boundary
        else:
            return boundary_vertices
    except Exception as e:
        return sort_polygon_points_3d(all_vertices)

def find_outer_boundary_detailed(polygons):
    edge_count = {}
    edge_to_vertices = {}
    for polygon in polygons:
        n_vertices = len(polygon)
        for i in range(n_vertices):
            v1 = polygon[i]
            v2 = polygon[(i + 1) % n_vertices]

            def vertex_key(v):
                return (round(v[0], 8), round(v[1], 8), round(v[2], 8))
            key1 = vertex_key(v1)
            key2 = vertex_key(v2)
            if key1 <= key2:
                edge_key = (key1, key2)
                edge_direction = (v1, v2)
            else:
                edge_key = (key2, key1)
                edge_direction = (v2, v1)
            if edge_key in edge_count:
                edge_count[edge_key] += 1
            else:
                edge_count[edge_key] = 1
                edge_to_vertices[edge_key] = edge_direction
    boundary_edges = []
    for edge_key, count in edge_count.items():
        if count == 1:
            boundary_edges.append(edge_to_vertices[edge_key])
    if len(boundary_edges) < 3:
        return None
    if len(boundary_edges) == 0:
        return None
    boundary_vertices = [boundary_edges[0][0], boundary_edges[0][1]]
    used_edges = {0}
    max_iterations = len(boundary_edges) * 2
    iterations = 0
    while len(used_edges) < len(boundary_edges) and iterations < max_iterations:
        iterations += 1
        current_end = boundary_vertices[-1]
        found_connection = False
        for i, (start, end) in enumerate(boundary_edges):
            if i in used_edges:
                continue
            if np.allclose(current_end, start, atol=1e-08):
                boundary_vertices.append(end)
                used_edges.add(i)
                found_connection = True
                break
            elif np.allclose(current_end, end, atol=1e-08):
                boundary_vertices.append(start)
                used_edges.add(i)
                found_connection = True
                break
        if not found_connection:
            if len(boundary_vertices) > 2 and np.allclose(boundary_vertices[-1], boundary_vertices[0], atol=1e-08):
                break
            else:
                remaining_edges = [i for i in range(len(boundary_edges)) if i not in used_edges]
                if remaining_edges:
                    next_edge_idx = remaining_edges[0]
                    start, end = boundary_edges[next_edge_idx]
                    boundary_vertices.extend([start, end])
                    used_edges.add(next_edge_idx)
                else:
                    break
    if len(boundary_vertices) > 1 and np.allclose(boundary_vertices[-1], boundary_vertices[0], atol=1e-08):
        boundary_vertices = boundary_vertices[:-1]
    unique_vertices = []
    for vertex in boundary_vertices:
        is_duplicate = False
        for existing in unique_vertices:
            if np.allclose(vertex, existing, atol=1e-08):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_vertices.append(vertex)
    if len(unique_vertices) >= 3:
        return np.array(unique_vertices)
    else:
        return None
    "\n    Apply ReLU operation to a polygon's z-values (clip negative values to 0).\n    \n    Args:\n        polygon: numpy array of shape (n_points, 3)\n    \n    Returns:\n        numpy array with z-values clipped to be >= 0\n    "
    clipped_polygon = polygon.copy()
    clipped_polygon[:, 2] = np.maximum(clipped_polygon[:, 2], 0.0)
    return clipped_polygon

def sort_polygon_points_3d(points):
    if len(points) < 3:
        return points
    centroid_x = np.mean(points[:, 0])
    centroid_y = np.mean(points[:, 1])
    angles = np.arctan2(points[:, 1] - centroid_y, points[:, 0] - centroid_x)
    sorted_indices = np.argsort(angles)
    return points[sorted_indices]
import numpy as np
import shapely.geometry as sg
from shapely.ops import unary_union

def find_polygon_intersections(all_polygons_after_merging_2d):
    if len(all_polygons_after_merging_2d) < 2:
        raise ValueError('Input must contain at least 2 sets of polygons')
    current_polygons = [sg.Polygon(coords) for coords in all_polygons_after_merging_2d[0]]
    for set_idx in range(1, len(all_polygons_after_merging_2d)):
        next_set_polygons = [sg.Polygon(coords) for coords in all_polygons_after_merging_2d[set_idx]]
        new_intersection_polygons = []
        for poly1 in current_polygons:
            for poly2 in next_set_polygons:
                intersection = poly1.intersection(poly2)
                if intersection.is_empty:
                    continue
                if isinstance(intersection, sg.Polygon):
                    if intersection.area > 1e-10:
                        new_intersection_polygons.append(intersection)
                elif isinstance(intersection, sg.MultiPolygon):
                    for geom in intersection.geoms:
                        if isinstance(geom, sg.Polygon) and geom.area > 1e-10:
                            new_intersection_polygons.append(geom)
        current_polygons = new_intersection_polygons
        if not current_polygons:
            break
    result = []
    for poly in current_polygons:
        coords = np.array(poly.exterior.coords[:-1])
        result.append(coords)
    return result

def find_polygon_intersections_pairwise(set1_coords, set2_coords):
    set1_polygons = [sg.Polygon(coords) for coords in set1_coords]
    set2_polygons = [sg.Polygon(coords) for coords in set2_coords]
    intersection_polygons = []
    for poly1 in set1_polygons:
        for poly2 in set2_polygons:
            intersection = poly1.intersection(poly2)
            if intersection.is_empty:
                continue
            if isinstance(intersection, sg.Polygon):
                if intersection.area > 1e-10:
                    intersection_polygons.append(intersection)
            elif isinstance(intersection, sg.MultiPolygon):
                for geom in intersection.geoms:
                    if isinstance(geom, sg.Polygon) and geom.area > 1e-10:
                        intersection_polygons.append(geom)
    result = []
    for poly in intersection_polygons:
        coords = np.array(poly.exterior.coords[:-1])
        result.append(coords)
    return result