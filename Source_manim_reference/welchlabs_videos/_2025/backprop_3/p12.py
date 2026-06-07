from functools import partial
import sys
sys.path.append('_2025/backprop_3')
from geometric_dl_utils import *
from plane_folding_utils import *
from geometric_dl_utils_simplified import *
from polytope_intersection_utils import intersect_polytopes
from manimlib import *
from gap_filler import fill_gaps
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

class p12b_flat_2(InteractiveScene):

    def construct(self):
        model_path = '_2025/backprop_3/models/32_32_32_32_1.pth'
        model = BaarleNet([32, 32, 32, 32])
        model.load_state_dict(torch.load(model_path))
        viz_scales = [0.07, 0.07, 0.04]
        num_neurons = [32, 32, 32, 32, 2]
        polygons = {}
        polygons['-1.new_tiling_unraveled'] = [np.array([[-1.0, -1, 0], [-1, 1, 0], [1, 1, 0], [1, -1, 0]])]
        for layer_id in range(len(model.model) // 2):
            polygons[str(layer_id) + '.linear_out'] = process_with_layers(model.model[:2 * layer_id + 1], polygons[str(layer_id - 1) + '.new_tiling_unraveled'])
            polygons[str(layer_id) + '.split_polygons_nested'] = split_polygons_with_relu_simple(polygons[str(layer_id) + '.linear_out'])
            polygons[str(layer_id) + '.split_polygons_nested_clipped'] = clip_polygons(polygons[str(layer_id) + '.split_polygons_nested'])
            polygons[str(layer_id) + '.new_tiling'] = recompute_tiling(polygons[str(layer_id) + '.split_polygons_nested'], min_area=0)
            polygons[str(layer_id) + '.new_tiling_unraveled'] = [item for sublist in polygons[str(layer_id) + '.new_tiling'] for item in sublist]
            print('Retiled plane into ', str(len(polygons[str(layer_id) + '.new_tiling_unraveled'])), ' polygons.')
        polygons[str(layer_id + 1) + '.linear_out'] = process_with_layers(model.model, polygons[str(layer_id) + '.new_tiling_unraveled'])
        intersection_lines, new_2d_tiling, upper_polytope, indicator = intersect_polytopes(*polygons[str(layer_id + 1) + '.linear_out'])
        my_indicator, my_top_polygons = compute_top_polytope(model, new_2d_tiling)
        print('finished computing polygons and surfaces')
        print(len(my_top_polygons), len(my_indicator))
        my_top_polygons, my_indicator = fill_gaps(my_top_polygons, my_indicator)
        print(len(my_top_polygons), len(my_indicator))
        with open('_2025/backprop_3/models/32_32_32_32_1_borders.p', 'rb') as file:
            borders_interp = pickle.load(file)
        lines = VGroup()
        for loop in borders_interp:
            loop = np.hstack((loop, np.zeros((len(loop), 1))))
            line = VMobject()
            line.set_points_as_corners(loop)
            line.set_stroke(color='#ec008c', width=5)
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
        self.add(flat_map, lines_flat_cleaner)
        self.wait()
        self.wait(20)
        self.embed()