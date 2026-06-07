import numpy as np
from typing import List, Tuple, Optional
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import split
from shapely.errors import TopologicalError

def intersect_polytopes(polygons_1: List[np.ndarray], polygons_2: List[np.ndarray]) -> Tuple[List[Tuple[np.ndarray, np.ndarray]], List[np.ndarray], List[np.ndarray], np.ndarray]:
    assert len(polygons_1) == len(polygons_2), 'Polygon lists must have same length'
    intersection_lines = []
    new_2d_tiling = []
    upper_polytope = []
    indicators = []
    for i, (poly1, poly2) in enumerate(zip(polygons_1, polygons_2)):
        poly_2d = poly1[:, :2]
        z1_values = poly1[:, 2]
        z2_values = poly2[:, 2]
        intersection_result = analyze_polygon_intersection(poly1, poly2)
        if intersection_result['type'] == 'no_intersection':
            new_2d_tiling.append(poly_2d)
            if intersection_result['poly1_above']:
                upper_polytope.append(poly1)
                indicators.append(0)
            else:
                upper_polytope.append(poly2)
                indicators.append(1)
        elif intersection_result['type'] == 'intersection':
            intersection_line = intersection_result['intersection_line']
            intersection_lines.append(intersection_line)
            split_polygons = split_polygon_along_line(poly_2d, intersection_line[:, :2])
            for split_poly in split_polygons:
                new_2d_tiling.append(split_poly)
                test_point = get_polygon_centroid(split_poly)
                z1_at_test = interpolate_z_value(poly1, test_point)
                z2_at_test = interpolate_z_value(poly2, test_point)
                if z1_at_test >= z2_at_test:
                    poly_3d = create_3d_polygon_from_2d(split_poly, poly1)
                    upper_polytope.append(poly_3d)
                    indicators.append(0)
                else:
                    poly_3d = create_3d_polygon_from_2d(split_poly, poly2)
                    upper_polytope.append(poly_3d)
                    indicators.append(1)
    return (intersection_lines, new_2d_tiling, upper_polytope, np.array(indicators))

def analyze_polygon_intersection(poly1: np.ndarray, poly2: np.ndarray) -> dict:
    z1_values = poly1[:, 2]
    z2_values = poly2[:, 2]
    if np.all(z1_values >= z2_values):
        if np.all(z1_values > z2_values):
            return {'type': 'no_intersection', 'poly1_above': True}
    if np.all(z2_values >= z1_values):
        if np.all(z2_values > z1_values):
            return {'type': 'no_intersection', 'poly1_above': False}
    intersection_points = []
    n_vertices = len(poly1)
    for i in range(n_vertices):
        j = (i + 1) % n_vertices
        z1_i, z1_j = (z1_values[i], z1_values[j])
        z2_i, z2_j = (z2_values[i], z2_values[j])
        diff_i = z1_i - z2_i
        diff_j = z1_j - z2_j
        if diff_i * diff_j < 0:
            t = diff_i / (diff_i - diff_j)
            intersection_point = poly1[i] + t * (poly1[j] - poly1[i])
            intersection_points.append(intersection_point)
    if len(intersection_points) >= 2:
        intersection_line = np.array([intersection_points[0], intersection_points[1]])
        return {'type': 'intersection', 'intersection_line': intersection_line}
    return {'type': 'no_intersection', 'poly1_above': np.mean(z1_values) > np.mean(z2_values)}

def split_polygon_along_line(polygon_2d: np.ndarray, line_2d: np.ndarray) -> List[np.ndarray]:
    try:
        if not np.allclose(polygon_2d[0], polygon_2d[-1]):
            closed_polygon = np.vstack([polygon_2d, polygon_2d[0]])
        else:
            closed_polygon = polygon_2d
        shapely_polygon = Polygon(closed_polygon)
        line_start, line_end = (line_2d[0], line_2d[1])
        line_direction = line_end - line_start
        line_length = np.linalg.norm(line_direction)
        if line_length < 1e-10:
            return [polygon_2d]
        line_direction_norm = line_direction / line_length
        polygon_bounds = shapely_polygon.bounds
        diagonal_length = np.sqrt((polygon_bounds[2] - polygon_bounds[0]) ** 2 + (polygon_bounds[3] - polygon_bounds[1]) ** 2)
        extension = diagonal_length * 2
        extended_start = line_start - line_direction_norm * extension
        extended_end = line_end + line_direction_norm * extension
        splitting_line = LineString([extended_start, extended_end])
        if not shapely_polygon.intersects(splitting_line):
            return [polygon_2d]
        split_result = split(shapely_polygon, splitting_line)
        split_polygons = []
        for geom in split_result.geoms:
            if geom.geom_type == 'Polygon' and (not geom.is_empty):
                coords = np.array(geom.exterior.coords)[:-1]
                if len(coords) >= 3:
                    split_polygons.append(coords)
        if len(split_polygons) == 0:
            return [polygon_2d]
        return split_polygons
    except (TopologicalError, ValueError, IndexError) as e:
        print(f'Warning: Polygon splitting failed: {e}. Returning original polygon.')
        return [polygon_2d]

def is_point_inside_polygon(point: np.ndarray, polygon_2d: np.ndarray) -> bool:
    try:
        if not np.allclose(polygon_2d[0], polygon_2d[-1]):
            closed_polygon = np.vstack([polygon_2d, polygon_2d[0]])
        else:
            closed_polygon = polygon_2d
        shapely_polygon = Polygon(closed_polygon)
        shapely_point = Point(point)
        return shapely_polygon.contains(shapely_point) or shapely_polygon.touches(shapely_point)
    except:
        return True

def get_polygon_centroid(polygon_2d: np.ndarray) -> np.ndarray:
    try:
        if not np.allclose(polygon_2d[0], polygon_2d[-1]):
            closed_polygon = np.vstack([polygon_2d, polygon_2d[0]])
        else:
            closed_polygon = polygon_2d
        shapely_polygon = Polygon(closed_polygon)
        centroid = shapely_polygon.centroid
        return np.array([centroid.x, centroid.y])
    except:
        return np.mean(polygon_2d, axis=0)

def interpolate_z_value(poly_3d: np.ndarray, test_point_2d: np.ndarray) -> float:
    if len(poly_3d) == 3:
        p1, p2, p3 = poly_3d[:, :2]
        z1, z2, z3 = poly_3d[:, 2]
        denom = (p2[1] - p3[1]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[1] - p3[1])
        if abs(denom) < 1e-10:
            return np.mean([z1, z2, z3])
        w1 = ((p2[1] - p3[1]) * (test_point_2d[0] - p3[0]) + (p3[0] - p2[0]) * (test_point_2d[1] - p3[1])) / denom
        w2 = ((p3[1] - p1[1]) * (test_point_2d[0] - p3[0]) + (p1[0] - p3[0]) * (test_point_2d[1] - p3[1])) / denom
        w3 = 1 - w1 - w2
        return w1 * z1 + w2 * z2 + w3 * z3
    elif len(poly_3d) >= 4:
        distances = np.linalg.norm(poly_3d[:, :2] - test_point_2d, axis=1)
        min_distance = np.min(distances)
        if min_distance < 1e-10:
            closest_idx = np.argmin(distances)
            return poly_3d[closest_idx, 2]
        weights = 1.0 / (distances + 1e-10)
        weights /= np.sum(weights)
        return np.sum(weights * poly_3d[:, 2])
    else:
        return np.mean(poly_3d[:, 2])

def create_3d_polygon_from_2d(polygon_2d: np.ndarray, reference_3d: np.ndarray) -> np.ndarray:
    result_3d = np.zeros((len(polygon_2d), 3))
    result_3d[:, :2] = polygon_2d
    for i, vertex_2d in enumerate(polygon_2d):
        result_3d[i, 2] = interpolate_z_value(reference_3d, vertex_2d)
    return result_3d