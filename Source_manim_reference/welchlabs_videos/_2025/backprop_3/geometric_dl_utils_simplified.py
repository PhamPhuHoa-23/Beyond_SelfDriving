import torch
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
import shapely.affinity
import copy
from tqdm import tqdm

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

def compute_top_polytope(model, tiling_2d):
    hyperspace_polygons = process_with_layers(model.model, tiling_2d)
    my_top_polygons = []
    my_indicator = []
    for p1, p2 in zip(hyperspace_polygons[0], hyperspace_polygons[1]):
        if np.all(p1[:, 2] > p2[:, 2]):
            my_top_polygons.append(p1)
            my_indicator.append(0)
        elif np.all(p2[:, 2] > p1[:, 2]):
            my_top_polygons.append(p2)
            my_indicator.append(1)
        elif np.max(p1[:, 2]) > np.max(p2[:, 2]):
            my_top_polygons.append(p1)
            my_indicator.append(0)
        elif np.max(p2[:, 2]) > np.max(p1[:, 2]):
            my_top_polygons.append(p2)
            my_indicator.append(1)
        else:
            my_top_polygons.append(p1)
            my_indicator.append(0)
    return (my_indicator, my_top_polygons)

def process_with_layers(model_layers, polygons_flat):
    with torch.no_grad():
        test_input = torch.tensor(polygons_flat[0][:, :2]).float()
        test_output = model_layers(test_input)
        num_neurons = test_output.shape[1]
    result = [[] for _ in range(num_neurons)]
    for i, p in enumerate(polygons_flat):
        with torch.no_grad():
            out = model_layers(torch.tensor(p[:, :2]).float())
            for neuron_idx in range(num_neurons):
                new_polygon = np.zeros((p.shape[0], 3))
                new_polygon[:, :2] = p[:, :2]
                new_polygon[:, 2] = out[:, neuron_idx].numpy()
                result[neuron_idx].append(new_polygon)
    return result

def clip_polygons(polygons):
    clipped_polygons = copy.deepcopy(polygons)
    for l1 in clipped_polygons:
        if isinstance(l1, np.ndarray):
            l1[:, 2] = np.maximum(0, l1[:, 2])
        else:
            for l2 in l1:
                if isinstance(l2, np.ndarray):
                    l2[:, 2] = np.maximum(0, l2[:, 2])
                else:
                    for l3 in l2:
                        if isinstance(l3, np.ndarray):
                            l3[:, 2] = np.maximum(0, l3[:, 2])
    return clipped_polygons

def split_polygons_with_relu_simple(polygons):

    def intersect_edge_with_z_plane(p1, p2, z=0):
        if abs(p1[2] - p2[2]) < 1e-10:
            return None
        t = (z - p1[2]) / (p2[2] - p1[2])
        if 0 <= t <= 1:
            intersection = p1 + t * (p2 - p1)
            intersection[2] = z
            return intersection
        return None

    def split_polygon_at_z_plane(polygon, z=0):
        points = polygon
        n = len(points)
        z_values = points[:, 2]
        if np.all(z_values >= z) or np.all(z_values <= z):
            return [polygon]
        above_points = []
        below_points = []
        intersection_points = []
        for i in range(n):
            curr_point = points[i]
            next_point = points[(i + 1) % n]
            if curr_point[2] >= z:
                above_points.append(curr_point.copy())
            if curr_point[2] <= z:
                below_points.append(curr_point.copy())
            intersection = intersect_edge_with_z_plane(curr_point, next_point, z)
            if intersection is not None:
                intersection_points.append(intersection)
                above_points.append(intersection.copy())
                below_points.append(intersection.copy())
        result_polygons = []
        if len(above_points) >= 3:
            result_polygons.append(np.array(above_points))
        if len(below_points) >= 3:
            result_polygons.append(np.array(below_points))
        return result_polygons if result_polygons else [polygon]
    split_polygons = []
    for neuron_polygons in polygons:
        neuron_split_polygons = []
        for polygon in neuron_polygons:
            split_parts = split_polygon_at_z_plane(polygon, z=0)
            neuron_split_polygons.append(split_parts)
        split_polygons.append(neuron_split_polygons)
    return split_polygons
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union, snap, polygonize
import numpy as np

def recompute_tiling_polygonize(polygons_nested, min_area=0, snap_tol=1e-08):
    if not polygons_nested:
        return []
    N_neurons = len(polygons_nested)
    M_inputs = len(polygons_nested[0])
    result = []

    def _polygonize_core(per_neuron_flat):
        shapely_polys = []
        for arr in per_neuron_flat:
            a = np.asarray(arr)
            if a.ndim == 2 and a.shape[0] >= 3:
                p = Polygon(a[:, :2])
                if p.is_valid and p.area > min_area:
                    shapely_polys.append(p)
        if not shapely_polys:
            return []
        master = unary_union(shapely_polys)
        snapped = [snap(p, master, snap_tol) for p in shapely_polys]
        lines = []
        for p in snapped:
            if not p.is_empty:
                lines.append(LineString(p.exterior.coords))
                for interior in p.interiors:
                    lines.append(LineString(interior.coords))
        merged = unary_union(lines)
        raw = [g for g in polygonize(merged) if g.area > min_area]
        square = Polygon([(-1, -1), (1, -1), (1, 1), (-1, 1)])
        out = []
        for g in raw:
            c = g.intersection(square)
            if not c.is_empty and c.area > min_area:
                pts = list(c.exterior.coords)[:-1]
                a3 = np.zeros((len(pts), 3), dtype=float)
                a3[:, :2] = pts
                out.append(a3)
        return out
    for i in range(M_inputs):
        per_neuron_flat = []
        for neuron_list in polygons_nested:
            entry = neuron_list[i]
            if isinstance(entry, list):
                per_neuron_flat.extend(entry)
            else:
                per_neuron_flat.append(entry)
        tiles = _polygonize_core(per_neuron_flat)
        result.append(tiles)
    return result

def recompute_tiling(polygons_nested, min_area=1e-10):
    import numpy as np
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    import shapely.affinity

    def numpy_to_shapely(poly_array):
        return Polygon(poly_array[:, :2])

    def shapely_to_numpy(shapely_poly, z_value=0):
        coords = list(shapely_poly.exterior.coords)[:-1]
        result = np.zeros((len(coords), 3))
        result[:, :2] = coords
        result[:, 2] = z_value
        return result

    def find_polygon_intersections(polygon_lists):
        if not polygon_lists or all((len(plist) == 0 for plist in polygon_lists)):
            return []
        current_regions = polygon_lists[0].copy()
        for neuron_polys in polygon_lists[1:]:
            new_regions = []
            for current_poly in current_regions:
                for neuron_poly in neuron_polys:
                    intersection = current_poly.intersection(neuron_poly)
                    if intersection.is_empty:
                        continue
                    elif hasattr(intersection, 'geoms'):
                        for geom in intersection.geoms:
                            if isinstance(geom, Polygon) and geom.area > min_area:
                                new_regions.append(geom)
                    elif isinstance(intersection, Polygon) and intersection.area > min_area:
                        new_regions.append(intersection)
            current_regions = new_regions
            if not current_regions:
                break
        return current_regions
    if not polygons_nested or not polygons_nested[0]:
        return []
    num_neurons = len(polygons_nested)
    num_input_polygons = len(polygons_nested[0])
    result = []
    for input_poly_idx in range(num_input_polygons):
        neuron_polygon_lists = []
        for neuron_idx in range(num_neurons):
            split_polys = polygons_nested[neuron_idx][input_poly_idx]
            shapely_polys = [numpy_to_shapely(poly) for poly in split_polys]
            neuron_polygon_lists.append(shapely_polys)
        split_counts = [len(plist) for plist in neuron_polygon_lists]
        num_splits = sum((1 for count in split_counts if count > 1))
        if num_splits == 0:
            original_poly = polygons_nested[0][input_poly_idx][0]
            result.append([original_poly])
        elif num_splits == 1:
            for plist in neuron_polygon_lists:
                if len(plist) > 1:
                    numpy_splits = [shapely_to_numpy(sp) for sp in plist]
                    result.append(numpy_splits)
                    break
        else:
            intersected_regions = find_polygon_intersections(neuron_polygon_lists)
            if intersected_regions:
                numpy_regions = [shapely_to_numpy(region) for region in intersected_regions]
                result.append(numpy_regions)
            else:
                original_poly = polygons_nested[0][input_poly_idx][0]
                result.append([original_poly])
    return result
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union, snap

def merge_zero_regions(polygons, snap_tol: float=1e-08, buffer_eps: float=1e-06, min_area: float=1e-08):

    def process_flat(flat_list):
        zero = [p for p in flat_list if np.allclose(p[:, 2], 0)]
        nonz = [p for p in flat_list if not np.allclose(p[:, 2], 0)]
        merged = []
        if zero:
            shapes = [Polygon(p[:, :2]) for p in zero]
            uni = unary_union(shapes)
            snapped = [snap(s, uni, snap_tol) for s in shapes]
            buff = [s.buffer(buffer_eps, join_style=2) for s in snapped]
            uni2 = unary_union(buff).buffer(-buffer_eps, join_style=2)
            geoms = uni2.geoms if hasattr(uni2, 'geoms') else [uni2]
            for g in geoms:
                if isinstance(g, Polygon) and g.area >= min_area:
                    coords = list(g.exterior.coords)[:-1]
                    arr = np.zeros((len(coords), 3), dtype=float)
                    arr[:, :2] = coords
                    merged.append(arr)
        return merged + nonz
    if isinstance(polygons, list) and all((isinstance(p, np.ndarray) for p in polygons)):
        return process_flat(polygons)
    out = []
    for neuron in polygons:
        if not neuron:
            out.append([])
            continue
        first = neuron[0]
        if isinstance(first, np.ndarray):
            flat = neuron
        else:
            flat = [poly for group in neuron for poly in group]
        out.append(process_flat(flat))
    return out
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union

def recompute_tiling_general(polygon_list, min_area=1e-10):
    tilings = []
    for neuron_polys in polygon_list:
        shapely_polys = []
        for p in neuron_polys:
            coords = p[:, :2]
            poly = Polygon(coords)
            if poly.is_valid and poly.area > min_area:
                shapely_polys.append(poly)
        tilings.append(shapely_polys)
    if not tilings:
        return []
    current = tilings[0]
    print('Retiling plane...')
    for next_tiling in tqdm(tilings[1:]):
        new_current = []
        for region in current:
            for tile in next_tiling:
                inter = region.intersection(tile)
                if inter.is_empty:
                    continue
                geoms = inter.geoms if hasattr(inter, 'geoms') else [inter]
                for g in geoms:
                    if isinstance(g, Polygon) and g.area > min_area:
                        new_current.append(g)
        current = new_current
        if not current:
            break
    result = []
    for poly in current:
        pts = list(poly.exterior.coords)[:-1]
        arr = np.zeros((len(pts), 3), dtype=float)
        arr[:, :2] = pts
        result.append(arr)
    return result

def filter_small_polygons(polygons, min_area=1e-06):
    filtered = []
    for p in polygons:
        coords = p[:, :2]
        poly = Polygon(coords)
        if poly.is_valid and poly.area >= min_area:
            filtered.append(p)
    return filtered