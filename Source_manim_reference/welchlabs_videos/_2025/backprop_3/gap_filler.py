import numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely.validation import make_valid

def fill_gaps(polygons, indicator):
    shapely_polys = []
    valid_indices = []
    for i, poly in enumerate(polygons):
        try:
            poly_2d = Polygon(poly[:, :2])
            if not poly_2d.is_valid:
                poly_2d = make_valid(poly_2d)
            if poly_2d.is_valid and poly_2d.area > 1e-10:
                shapely_polys.append(poly_2d)
                valid_indices.append(i)
        except Exception as e:
            print(f'Warning: Could not process polygon {i}: {e}')
            continue
    if not shapely_polys:
        return (polygons, indicator)
    domain = box(-1, -1, 1, 1)
    covered_area = unary_union(shapely_polys)
    gaps = domain.difference(covered_area)
    gap_polygons = []
    if hasattr(gaps, 'geoms'):
        gap_polygons = [g for g in gaps.geoms if g.area > 1e-10]
    elif isinstance(gaps, Polygon) and gaps.area > 1e-10:
        gap_polygons = [gaps]
    if not gap_polygons:
        return (polygons, indicator)
    filled_polygons = list(polygons)
    filled_indicator = list(indicator)
    for gap in gap_polygons:
        gap_centroid = np.array([gap.centroid.x, gap.centroid.y])
        min_dist = float('inf')
        nearest_idx = 0
        for idx in valid_indices:
            poly = polygons[idx]
            poly_centroid = np.mean(poly[:, :2], axis=0)
            dist = np.linalg.norm(gap_centroid - poly_centroid)
            if dist < min_dist:
                min_dist = dist
                nearest_idx = idx
        gap_coords = np.array(gap.exterior.coords[:-1])
        nearest_z = np.mean(polygons[nearest_idx][:, 2])
        gap_3d = np.zeros((len(gap_coords), 3))
        gap_3d[:, :2] = gap_coords
        gap_3d[:, 2] = nearest_z
        filled_polygons.append(gap_3d)
        filled_indicator.append(indicator[nearest_idx])
    return (filled_polygons, filled_indicator)

def fill_gaps_advanced(polygons, indicator, k_neighbors=5):
    shapely_polys = []
    valid_indices = []
    for i, poly in enumerate(polygons):
        try:
            poly_2d = Polygon(poly[:, :2])
            if not poly_2d.is_valid:
                poly_2d = make_valid(poly_2d)
            if poly_2d.is_valid and poly_2d.area > 1e-10:
                shapely_polys.append(poly_2d)
                valid_indices.append(i)
        except Exception as e:
            print(f'Warning: Could not process polygon {i}: {e}')
            continue
    if not shapely_polys:
        return (polygons, indicator)
    domain = box(-1, -1, 1, 1)
    covered_area = unary_union(shapely_polys)
    gaps = domain.difference(covered_area)
    gap_polygons = []
    if hasattr(gaps, 'geoms'):
        gap_polygons = [g for g in gaps.geoms if g.area > 1e-10]
    elif isinstance(gaps, Polygon) and gaps.area > 1e-10:
        gap_polygons = [gaps]
    if not gap_polygons:
        return (polygons, indicator)
    print(f'Found {len(gap_polygons)} gaps to fill')
    filled_polygons = list(polygons)
    filled_indicator = list(indicator)
    for gap in gap_polygons:
        gap_centroid = np.array([gap.centroid.x, gap.centroid.y])
        distances = []
        for idx in valid_indices:
            poly = polygons[idx]
            poly_centroid = np.mean(poly[:, :2], axis=0)
            dist = np.linalg.norm(gap_centroid - poly_centroid)
            distances.append((dist, idx))
        distances.sort()
        k_nearest = distances[:min(k_neighbors, len(distances))]
        votes = [indicator[idx] for _, idx in k_nearest]
        gap_indicator = 1 if sum(votes) > len(votes) / 2 else 0
        gap_coords = np.array(gap.exterior.coords[:-1])
        total_weight = 0
        weighted_z = 0
        for dist, idx in k_nearest:
            weight = 1.0 / (dist + 1e-06)
            total_weight += weight
            weighted_z += weight * np.mean(polygons[idx][:, 2])
        interpolated_z = weighted_z / total_weight if total_weight > 0 else 0
        gap_3d = np.zeros((len(gap_coords), 3))
        gap_3d[:, :2] = gap_coords
        gap_3d[:, 2] = interpolated_z
        filled_polygons.append(gap_3d)
        filled_indicator.append(gap_indicator)
    return (filled_polygons, filled_indicator)