import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

def compute_polygon_features(polygon):
    vertices = polygon[:, :2]
    centroid = np.mean(vertices, axis=0)
    x = vertices[:, 0]
    y = vertices[:, 1]
    area = 0.5 * abs(sum((x[i] * y[i + 1] - x[i + 1] * y[i] for i in range(-1, len(x) - 1))))
    return (centroid, area)

def compute_polygon_distance(poly1, poly2, centroid_weight=1.0, area_weight=0.1):
    centroid1, area1 = compute_polygon_features(poly1)
    centroid2, area2 = compute_polygon_features(poly2)
    centroid_dist = np.linalg.norm(centroid1 - centroid2)
    area_diff = abs(area1 - area2) / max(area1, area2, 1e-08)
    return centroid_weight * centroid_dist + area_weight * area_diff

def reorder_polygons_greedy(prev_polygons, curr_polygons, centroid_weight=1.0, area_weight=0.1):
    if not prev_polygons or not curr_polygons:
        return curr_polygons
    n_prev = len(prev_polygons)
    n_curr = len(curr_polygons)
    distances = np.zeros((n_prev, n_curr))
    for i, prev_poly in enumerate(prev_polygons):
        for j, curr_poly in enumerate(curr_polygons):
            distances[i, j] = compute_polygon_distance(prev_poly, curr_poly, centroid_weight, area_weight)
    used_indices = set()
    reordered = []
    for i in range(n_prev):
        best_j = None
        best_dist = float('inf')
        for j in range(n_curr):
            if j not in used_indices and distances[i, j] < best_dist:
                best_dist = distances[i, j]
                best_j = j
        if best_j is not None:
            reordered.append(curr_polygons[best_j])
            used_indices.add(best_j)
        else:
            best_j = np.argmin(distances[i, :])
            reordered.append(curr_polygons[best_j])
    for j in range(n_curr):
        if j not in used_indices:
            reordered.append(curr_polygons[j])
    return reordered

def reorder_polygons_optimal(prev_polygons, curr_polygons, centroid_weight=1.0, area_weight=0.1):
    if not prev_polygons or not curr_polygons:
        return curr_polygons
    n_prev = len(prev_polygons)
    n_curr = len(curr_polygons)
    distances = np.zeros((n_prev, n_curr))
    for i, prev_poly in enumerate(prev_polygons):
        for j, curr_poly in enumerate(curr_polygons):
            distances[i, j] = compute_polygon_distance(prev_poly, curr_poly, centroid_weight, area_weight)
    if n_prev <= n_curr:
        row_ind, col_ind = linear_sum_assignment(distances)
        reordered = [None] * n_prev
        used_indices = set()
        for i, j in zip(row_ind, col_ind):
            reordered[i] = curr_polygons[j]
            used_indices.add(j)
        for j in range(n_curr):
            if j not in used_indices:
                reordered.append(curr_polygons[j])
    else:
        extended_distances = np.full((n_prev, n_prev), np.max(distances) * 2)
        extended_distances[:n_prev, :n_curr] = distances
        row_ind, col_ind = linear_sum_assignment(extended_distances)
        reordered = []
        for i, j in zip(row_ind, col_ind):
            if j < n_curr:
                reordered.append(curr_polygons[j])
    return reordered

def test_reordering():

    def make_square(center_x, center_y, size=0.5):
        return np.array([[center_x - size / 2, center_y - size / 2], [center_x + size / 2, center_y - size / 2], [center_x + size / 2, center_y + size / 2], [center_x - size / 2, center_y + size / 2]])
    prev_polygons = [make_square(0, 0), make_square(1, 0), make_square(0, 1)]
    curr_polygons = [make_square(0.1, 1.1), make_square(1.1, 0.1), make_square(0.1, 0.1), make_square(2, 2)]
    print('Original order - centroids:')
    for i, poly in enumerate(curr_polygons):
        centroid, _ = compute_polygon_features(poly)
        print(f'  Polygon {i}: {centroid}')
    reordered_greedy = reorder_polygons_greedy(prev_polygons, curr_polygons)
    print('\nGreedy reordered - centroids:')
    for i, poly in enumerate(reordered_greedy):
        centroid, _ = compute_polygon_features(poly)
        print(f'  Polygon {i}: {centroid}')
    reordered_optimal = reorder_polygons_optimal(prev_polygons, curr_polygons)
    print('\nOptimal reordered - centroids:')
    for i, poly in enumerate(reordered_optimal):
        centroid, _ = compute_polygon_features(poly)
        print(f'  Polygon {i}: {centroid}')
if __name__ == '__main__':
    test_reordering()