from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
from functools import partial
import numpy as np
import torch
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
GREEN = '#00a14b'
svg_path = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backprop2/graphics/to_manim'
data_path = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backprop2/hackin'
heatmap_path = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backprop2/graphics/to_manim/jun_6_1'

def format_number(num, total_chars=6, align='right'):
    abs_num = abs(num)
    if abs_num >= 100:
        formatted = f'{num:.0f}'
    elif abs_num >= 10:
        formatted = f'{num:.1f}'
    elif abs_num >= 1:
        formatted = f'{num:.2f}'
    else:
        formatted = f'{num:.2f}'
    if align == 'right':
        return formatted.rjust(total_chars)
    elif align == 'left':
        return formatted.ljust(total_chars)
    else:
        return formatted.center(total_chars)

def format_number_fixed_decimal(num, decimal_places=2, total_chars=6):
    formatted = f'{num:.{decimal_places}f}'
    return formatted.rjust(total_chars)

def get_numbers(i, xs, weights, logits, yhats):
    x = xs[i, -1]
    numbers = VGroup()
    tx = Tex(str(x) + '^\\circ')
    tx.scale(0.13)
    tx.move_to([-1.49, 0.02, 0])
    numbers.add(tx)
    w = weights[i, :]
    tm1 = Tex(format_number(w[0], total_chars=6)).set_color('#00FFFF')
    tm1.scale(0.16)
    tm1.move_to([-1.195, 0.205, 0])
    numbers.add(tm1)
    tm2 = Tex(format_number(w[1], total_chars=6)).set_color(YELLOW)
    tm2.scale(0.15)
    tm2.move_to([-1.155, 0.015, 0])
    numbers.add(tm2)
    tm3 = Tex(format_number(w[2], total_chars=6)).set_color(GREEN)
    tm3.scale(0.16)
    tm3.move_to([-1.19, -0.17, 0])
    numbers.add(tm3)
    tb1 = Tex(format_number(w[3], total_chars=6)).set_color('#00FFFF')
    tb1.scale(0.16)
    tb1.move_to([-0.875, 0.365, 0])
    numbers.add(tb1)
    tb2 = Tex(format_number(w[4], total_chars=6)).set_color(YELLOW)
    tb2.scale(0.16)
    tb2.move_to([-0.875, 0.015, 0])
    numbers.add(tb2)
    tb3 = Tex(format_number(w[5], total_chars=6)).set_color(GREEN)
    tb3.scale(0.16)
    tb3.move_to([-0.88, -0.335, 0])
    numbers.add(tb3)
    tl1 = Tex(format_number(logits[i, 0], total_chars=6)).set_color('#00FFFF')
    tl1.scale(0.16)
    tl1.move_to([-0.52, 0.37, 0])
    numbers.add(tl1)
    tl2 = Tex(format_number(logits[i, 1], total_chars=6)).set_color(YELLOW)
    tl2.scale(0.16)
    tl2.move_to([-0.52, 0.015, 0])
    numbers.add(tl2)
    tl3 = Tex(format_number(logits[i, 2], total_chars=6)).set_color(GREEN)
    tl3.scale(0.16)
    tl3.move_to([-0.52, -0.335, 0])
    numbers.add(tl3)
    yhat1 = Tex(format_number(yhats[i, 0], total_chars=6)).set_color('#00FFFF')
    yhat1.scale(0.16)
    yhat1.move_to([0.22, 0.37, 0])
    numbers.add(yhat1)
    yhat2 = Tex(format_number(yhats[i, 1], total_chars=6)).set_color(YELLOW)
    yhat2.scale(0.16)
    yhat2.move_to([0.22, 0.015, 0])
    numbers.add(yhat2)
    yhat3 = Tex(format_number(yhats[i, 2], total_chars=6)).set_color(GREEN)
    yhat3.scale(0.16)
    yhat3.move_to([0.22, -0.335, 0])
    numbers.add(yhat3)
    return numbers

def latlong_to_canvas(lat, long, label=None, map_min_x=0.38, map_max_x=1.54, map_min_y=-0.56, map_max_y=0.56, min_long=-7.0, max_long=18.0, min_lat=36.0, max_lat=56.0, paris_adjust=[0, 0, 0], madrid_adjust=[0, 0, 0], berlin_adjust=[-0.03, 0.06, 0], barcelona_adjust=[0, 0, 0]):
    long_normalized = (long - min_long) / (max_long - min_long)
    lat_normalized = (lat - min_lat) / (max_lat - min_lat)
    x = map_min_x + long_normalized * (map_max_x - map_min_x)
    y = map_min_y + lat_normalized * (map_max_y - map_min_y)
    if label is not None:
        if label == 0:
            x = x + madrid_adjust[0]
            y = y + madrid_adjust[1]
        if label == 1:
            x = x + paris_adjust[0]
            y = y + paris_adjust[1]
        if label == 2:
            x = x + berlin_adjust[0]
            y = y + berlin_adjust[1]
        if label == 3:
            x = x + barcelona_adjust[0]
            y = y + barcelona_adjust[1]
    return (x, y)

def get_grad_regions(i, ys, yhats, grads):
    max_region_width = 0.15
    min_region_width = 0.01
    region_scaling = 0.15
    grad_regions = VGroup()
    y_one_hot = torch.nn.functional.one_hot(torch.tensor(int(ys[i])), 3).numpy()
    dldh = yhats[i] - y_one_hot
    rh1_width = np.clip(region_scaling * np.abs(dldh[0]), min_region_width, max_region_width)
    rh1 = Rectangle(0.425, rh1_width, stroke_width=0).set_color('#00FFFF').set_opacity(0.2)
    rh1.move_to([-0.52, 0.37, 0])
    grad_regions.add(rh1)
    rh2_width = np.clip(region_scaling * np.abs(dldh[1]), min_region_width, max_region_width)
    rh2 = Rectangle(0.425, rh2_width, stroke_width=0).set_color(YELLOW).set_opacity(0.2)
    rh2.move_to([-0.52, 0.015, 0])
    grad_regions.add(rh2)
    rh3_width = np.clip(region_scaling * np.abs(dldh[2]), min_region_width, max_region_width)
    rh3 = Rectangle(0.425, rh3_width, stroke_width=0).set_color(GREEN).set_opacity(0.2)
    rh3.move_to([-0.52, -0.335, 0])
    grad_regions.add(rh3)
    rb1_width = np.clip(region_scaling * np.abs(grads[i, 3]), min_region_width, max_region_width)
    rb1 = Rectangle(0.24, rb1_width, stroke_width=0).set_color('#00FFFF').set_opacity(0.2)
    rb1.move_to([-0.875, 0.37, 0])
    grad_regions.add(rb1)
    rb2_width = np.clip(region_scaling * np.abs(grads[i, 4]), min_region_width, max_region_width)
    rb2 = Rectangle(0.24, rb2_width, stroke_width=0).set_color(YELLOW).set_opacity(0.2)
    rb2.move_to([-0.875, 0.015, 0])
    grad_regions.add(rb2)
    rb3_width = np.clip(region_scaling * np.abs(grads[i, 5]), min_region_width, max_region_width)
    rb3 = Rectangle(0.24, rb3_width, stroke_width=0).set_color(GREEN).set_opacity(0.2)
    rb3.move_to([-0.872, -0.335, 0])
    grad_regions.add(rb3)
    rm1_width = np.clip(region_scaling * np.abs(grads[i, 0]), min_region_width, max_region_width)
    rm1 = Rectangle(0.42, rm1_width, stroke_width=0).set_color('#00FFFF').set_opacity(0.2)
    rm1.rotate(33 * DEGREES)
    rm1.move_to([-1.18, 0.2, 0])
    grad_regions.add(rm1)
    rm2_width = np.clip(region_scaling * np.abs(grads[i, 1]), min_region_width, max_region_width)
    rm2 = Rectangle(0.33, rm2_width, stroke_width=0).set_color(YELLOW).set_opacity(0.2)
    rm2.move_to([-1.18, 0.015, 0])
    grad_regions.add(rm2)
    rm3_width = np.clip(region_scaling * np.abs(grads[i, 2]), min_region_width, max_region_width)
    rm3 = Rectangle(0.42, rm3_width, stroke_width=0).set_color(GREEN).set_opacity(0.2)
    rm3.rotate(-30.5 * DEGREES)
    rm3.move_to([-1.19, -0.175, 0])
    grad_regions.add(rm3)
    return grad_regions

def get_arrow_tip(line, color=None, scale=0.1, tip_position=1.0):
    tip_point = line.point_from_proportion(tip_position)
    direction_point = line.point_from_proportion(tip_position - 0.05)
    direction = tip_point - direction_point
    arrow_tip = ArrowTip().scale(scale)
    if color is None:
        color = line.get_color()
    arrow_tip.set_color(color)
    arrow_tip.move_to(tip_point)
    arrow_tip.rotate(angle_of_vector(direction))
    return arrow_tip

def create_plane_from_line_endpoints(line, color, depth=3.0, y_extension=2.0):
    start_point = line.get_start()
    end_point = line.get_end()
    bottom_left = start_point.copy()
    bottom_right = end_point.copy()
    top_left = start_point + np.array([0, y_extension, 0])
    top_right = end_point + np.array([0, y_extension, 0])

    class RectangularPlane(Surface):

        def __init__(self, corners, **kwargs):
            self.corners = corners
            super().__init__(u_range=(0, 1), v_range=(0, 1), resolution=(20, 10), **kwargs)

        def uv_func(self, u, v):
            bottom_point = interpolate(self.corners[0], self.corners[1], u)
            top_point = interpolate(self.corners[2], self.corners[3], u)
            point = interpolate(bottom_point, top_point, v)
            return point
    base_plane = RectangularPlane([bottom_left, bottom_right, top_left, top_right], color=color, shading=(0.2, 0.2, 0.6))

    class ExtrudedPlane(Surface):

        def __init__(self, base_corners, depth, **kwargs):
            self.base_corners = base_corners
            self.depth = depth
            super().__init__(u_range=(0, 1), v_range=(-1, 1), resolution=(20, 10), **kwargs)

        def uv_func(self, u, v):
            bottom_point = interpolate(self.base_corners[0], self.base_corners[1], u)
            top_point = interpolate(self.base_corners[2], self.base_corners[3], u)
            middle_point = interpolate(bottom_point, top_point, 0.5)
            z_offset = v * self.depth / 2
            final_point = middle_point + np.array([0, 0, z_offset])
            return final_point

    class LineExtensionPlane(Surface):

        def __init__(self, line_start, line_end, y_extension, depth, **kwargs):
            self.line_start = line_start
            self.line_end = line_end
            self.y_extension = y_extension
            self.depth = depth
            super().__init__(u_range=(0, 1), v_range=(0, 1), resolution=(15, 10), **kwargs)

        def uv_func(self, u, v):
            line_point = interpolate(self.line_start, self.line_end, u)
            extended_point = line_point + np.array([0, v * self.y_extension, 0])
            return extended_point
    return LineExtensionPlane(start_point, end_point, y_extension, depth, color=color, shading=(0.2, 0.2, 0.6))

def sample_points_from_curve(curve, num_points=128):
    points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        point = curve.point_from_proportion(t)
        points.append(point)
    return np.array(points)

def create_surface_from_curve_simple(curve, y_extension=0.5, color='#00FFFF'):
    curve_points = sample_points_from_curve(curve, num_points=32)
    extended_points = curve_points + np.array([0, y_extension, 0])

    class SimpleCurveSurface(Surface):

        def __init__(self, bottom_points, top_points, **kwargs):
            self.bottom_points = bottom_points
            self.top_points = top_points
            self.num_points = len(bottom_points)
            super().__init__(u_range=(0, 1), v_range=(0, 1), resolution=(self.num_points, 8), **kwargs)

        def uv_func(self, u, v):
            point_index = u * (self.num_points - 1)
            index_low = int(np.floor(point_index))
            index_high = min(index_low + 1, self.num_points - 1)
            t = point_index - index_low
            if index_low == index_high:
                bottom_point = self.bottom_points[index_low]
                top_point = self.top_points[index_low]
            else:
                bottom_point = (1 - t) * self.bottom_points[index_low] + t * self.bottom_points[index_high]
                top_point = (1 - t) * self.top_points[index_low] + t * self.top_points[index_high]
            final_point = (1 - v) * bottom_point + v * top_point
            return final_point
    surface = SimpleCurveSurface(bottom_points=curve_points, top_points=extended_points, color=color, shading=(0.2, 0.2, 0.6))
    surface.set_opacity(0.3)
    return surface

def create_matching_plane_and_surface(line, curve, y_extension=0.5, color='#00FFFF'):
    curve_points = sample_points_from_curve(curve, num_points=32)

    class MatchingPlane(Surface):

        def __init__(self, line_start, line_end, y_extension, **kwargs):
            self.line_start = line_start
            self.line_end = line_end
            self.y_extension = y_extension
            super().__init__(u_range=(0, 1), v_range=(0, 1), resolution=(32, 8), **kwargs)

        def uv_func(self, u, v):
            line_point = (1 - u) * self.line_start + u * self.line_end
            extended_point = line_point + np.array([0, v * self.y_extension, 0])
            return extended_point

    class MatchingSurface(Surface):

        def __init__(self, curve_points, y_extension, **kwargs):
            self.curve_points = curve_points
            self.y_extension = y_extension
            self.num_points = len(curve_points)
            super().__init__(u_range=(0, 1), v_range=(0, 1), resolution=(32, 8), **kwargs)

        def uv_func(self, u, v):
            point_index = u * (self.num_points - 1)
            index_low = int(np.floor(point_index))
            index_high = min(index_low + 1, self.num_points - 1)
            t = point_index - index_low
            if index_low == index_high:
                curve_point = self.curve_points[index_low]
            else:
                curve_point = (1 - t) * self.curve_points[index_low] + t * self.curve_points[index_high]
            extended_point = curve_point + np.array([0, v * self.y_extension, 0])
            return extended_point
    plane = MatchingPlane(line.get_start(), line.get_end(), y_extension, color=color, shading=(0.2, 0.2, 0.6))
    surface = MatchingSurface(curve_points, y_extension, color=color, shading=(0.2, 0.2, 0.6))
    plane.set_opacity(0.3)
    surface.set_opacity(0.3)
    return (plane, surface)

class p44(InteractiveScene):

    def construct(self):
        min_long = -9.8
        max_long = 17.2
        min_lat = 36.15
        max_lat = 54.7
        data = np.load(data_path + '/cities_1d_5.npy')
        xs = data[:, :2]
        ys = data[:, 2]
        weights = data[:, 3:9]
        grads = data[:, 9:15]
        logits = data[:, 15:18]
        yhats = data[:, 18:]
        net_background = SVGMobject(svg_path + '/p44_background_1.svg')
        i = 0
        nums = get_numbers(i, xs, weights, logits, yhats)
        grad_regions = get_grad_regions(i, ys, yhats, grads)
        heatmaps = Group()
        heatmap_yhat3 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_3.png')
        heatmap_yhat3.scale([0.29, 0.28, 0.28])
        heatmap_yhat3.move_to([0.96, 0, 0])
        heatmap_yhat3.set_opacity(0.5)
        heatmaps.add(heatmap_yhat3)
        heatmap_yhat1 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_1.png')
        heatmap_yhat1.scale([0.29, 0.28, 0.28])
        heatmap_yhat1.move_to([0.96, 0, 0])
        heatmap_yhat1.set_opacity(0.5)
        heatmaps.add(heatmap_yhat1)
        heatmap_yhat2 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_2.png')
        heatmap_yhat2.scale([0.29, 0.28, 0.28])
        heatmap_yhat2.move_to([0.96, 0, 0])
        heatmap_yhat2.set_opacity(0.5)
        heatmaps.add(heatmap_yhat2)
        canvas_x, canvas_y = latlong_to_canvas(xs[i][0], xs[i][1], label=ys[i], min_long=min_long, max_long=max_long, min_lat=min_lat, max_lat=max_lat, berlin_adjust=[-0.01, 0.02, 0])
        training_point = Dot([canvas_x, canvas_y, 0], radius=0.012)
        if ys[i] == 0.0:
            training_point.set_color('#00FFFF')
        elif ys[i] == 1.0:
            training_point.set_color(YELLOW)
        elif ys[i] == 2.0:
            training_point.set_color(GREEN)
        self.frame.reorient(0, 0, 0, (-0.61, 0.01, 0.0), 1.5)
        self.add(net_background, nums)
        self.wait()
        self.play(FadeIn(grad_regions))
        self.wait()
        self.play(grad_regions[0].animate.scale([1, 0.1, 1]), run_time=1.5)
        self.wait()
        self.play(grad_regions[0].animate.scale([1, 10, 1]), run_time=1.5)
        self.wait()
        europe_map = ImageMobject(svg_path + '/map_cropped_one.png')
        europe_map.scale(0.28)
        europe_map.move_to([0.96, 0, 0])
        map_tick_overlays = SVGMobject(svg_path + '/map_tick_overlays_1.svg')[1:]
        map_tick_overlays.scale([0.965, 0.96, 0.965])
        map_tick_overlays.shift([-0.077, 0.0185, 0])
        self.wait()
        self.play(FadeIn(europe_map), FadeIn(map_tick_overlays), self.frame.animate.reorient(0, 0, 0, (-0.04, 0.01, 0.0), 1.94), run_time=2)
        self.wait()
        self.add(training_point)
        self.wait()
        box = SurroundingRectangle(training_point, color=YELLOW, buff=0.025)
        self.play(ShowCreation(box))
        self.wait()
        self.play(FadeOut(box))
        self.add(heatmaps)
        heatmaps.set_opacity(0.0)
        self.remove(map_tick_overlays)
        self.add(map_tick_overlays)
        self.wait()
        self.play(heatmap_yhat1.animate.set_opacity(0.5))
        self.wait()
        self.play(heatmap_yhat2.animate.set_opacity(0.5))
        self.wait()
        self.play(heatmap_yhat3.animate.set_opacity(0.5))
        self.wait()
        step_label = Text('Step=')
        step_label.set_color(CHILL_BROWN)
        step_label.scale(0.12)
        step_label.move_to([1.3, -0.85, 0])
        step_count = Text(str(i).zfill(3))
        step_count.set_color(CHILL_BROWN)
        step_count.scale(0.12)
        step_count.move_to([1.43, -0.85, 0])
        self.play(FadeIn(step_label), FadeIn(step_count))
        self.wait()
        for i in range(1, len(xs)):
            if i > 0:
                self.remove(nums)
                self.remove(grad_regions)
                self.remove(heatmaps)
                self.remove(training_point)
                self.remove(map_tick_overlays)
                if step_label is not None:
                    self.remove(step_label, step_count)
            nums = get_numbers(i, xs, weights, logits, yhats)
            grad_regions = get_grad_regions(i, ys, yhats, grads)
            heatmaps = Group()
            heatmap_yhat3 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_3.png')
            heatmap_yhat3.scale([0.29, 0.28, 0.28])
            heatmap_yhat3.move_to([0.96, 0, 0])
            heatmap_yhat3.set_opacity(0.5)
            heatmaps.add(heatmap_yhat3)
            heatmap_yhat1 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_1.png')
            heatmap_yhat1.scale([0.29, 0.28, 0.28])
            heatmap_yhat1.move_to([0.96, 0, 0])
            heatmap_yhat1.set_opacity(0.5)
            heatmaps.add(heatmap_yhat1)
            heatmap_yhat2 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_2.png')
            heatmap_yhat2.scale([0.29, 0.28, 0.28])
            heatmap_yhat2.move_to([0.96, 0, 0])
            heatmap_yhat2.set_opacity(0.5)
            heatmaps.add(heatmap_yhat2)
            canvas_x, canvas_y = latlong_to_canvas(xs[i][0], xs[i][1], label=ys[i], min_long=min_long, max_long=max_long, min_lat=min_lat, max_lat=max_lat, berlin_adjust=[-0.01, 0.02, 0], paris_adjust=[-0.009, -0.002, 0], madrid_adjust=[-0.009, -0.002, 0])
            training_point = Dot([canvas_x, canvas_y, 0], radius=0.012)
            if ys[i] == 0.0:
                training_point.set_color('#00FFFF')
            elif ys[i] == 1.0:
                training_point.set_color(YELLOW)
            elif ys[i] == 2.0:
                training_point.set_color(GREEN)
            step_label = Text('Step=')
            step_label.set_color(CHILL_BROWN)
            step_label.scale(0.12)
            step_label.move_to([1.3, -0.85, 0])
            step_count = Text(str(i).zfill(3))
            step_count.set_color(CHILL_BROWN)
            step_count.scale(0.12)
            step_count.move_to([1.43, -0.85, 0])
            self.add(step_label, step_count)
            self.add(nums)
            self.add(grad_regions)
            self.add(heatmaps)
            self.add(training_point)
            self.add(map_tick_overlays)
            self.wait(0.1)
        self.wait(20)
        self.embed()

def get_numbers_b(i, xs, weights, logits, yhats):
    nums = VGroup()
    x = xs[i, -1]
    tx = Tex(str(x) + '^\\circ')
    tx.scale(0.13)
    tx.move_to([-1.49, 0.02, 0])
    nums.add(tx)
    w = weights[i, :]
    tm1 = Tex(format_number(w[0], total_chars=6)).set_color('#00FFFF')
    tm1.scale(0.12)
    tm1.move_to([-1.185, 0.54, 0])
    nums.add(tm1)
    tm2 = Tex(format_number(w[1], total_chars=6)).set_color(YELLOW)
    tm2.scale(0.12)
    tm2.move_to([-1.185, 0.1, 0])
    nums.add(tm2)
    tm3 = Tex(format_number(w[2], total_chars=6)).set_color(GREEN)
    tm3.scale(0.12)
    tm3.move_to([-1.185, -0.33, 0])
    nums.add(tm3)
    tb1 = Tex(format_number(w[3], total_chars=6)).set_color('#00FFFF')
    tb1.scale(0.12)
    tb1.move_to([-1.185, 0.37, 0])
    nums.add(tb1)
    tb2 = Tex(format_number(w[4], total_chars=6)).set_color(YELLOW)
    tb2.scale(0.12)
    tb2.move_to([-1.185, -0.07, 0])
    nums.add(tb2)
    tb3 = Tex(format_number(w[5], total_chars=6)).set_color(GREEN)
    tb3.scale(0.12)
    tb3.move_to([-1.185, -0.51, 0])
    nums.add(tb3)
    tl1 = Tex(format_number(logits[i, 0], total_chars=6)).set_color('#00FFFF')
    tl1.scale(0.16)
    tl1.move_to([-0.52, 0.37, 0])
    nums.add(tl1)
    tl2 = Tex(format_number(logits[i, 1], total_chars=6)).set_color(YELLOW)
    tl2.scale(0.16)
    tl2.move_to([-0.52, 0.015, 0])
    nums.add(tl2)
    tl3 = Tex(format_number(logits[i, 2], total_chars=6)).set_color(GREEN)
    tl3.scale(0.16)
    tl3.move_to([-0.52, -0.335, 0])
    nums.add(tl3)
    yhat1 = Tex(format_number(yhats[i, 0], total_chars=6)).set_color('#00FFFF')
    yhat1.scale(0.16)
    yhat1.move_to([0.22, 0.37, 0])
    nums.add(yhat1)
    yhat2 = Tex(format_number(yhats[i, 1], total_chars=6)).set_color(YELLOW)
    yhat2.scale(0.16)
    yhat2.move_to([0.22, 0.015, 0])
    nums.add(yhat2)
    yhat3 = Tex(format_number(yhats[i, 2], total_chars=6)).set_color(GREEN)
    yhat3.scale(0.16)
    yhat3.move_to([0.22, -0.335, 0])
    nums.add(yhat3)
    return nums

class p46a(InteractiveScene):

    def construct(self):
        min_long = -9.8
        max_long = 17.2
        min_lat = 36.15
        max_lat = 54.7
        data = np.load(data_path + '/cities_1d_5.npy')
        xs = data[:, :2]
        ys = data[:, 2]
        weights = data[:, 3:9]
        grads = data[:, 9:15]
        logits = data[:, 15:18]
        yhats = data[:, 18:]
        net_background_0 = SVGMobject(svg_path + '/p44_background_1.svg')
        i = 0
        nums0 = get_numbers(i, xs, weights, logits, yhats)
        grad_regions = get_grad_regions(i, ys, yhats, grads)
        heatmaps = Group()
        heatmap_yhat3 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_3.png')
        heatmap_yhat3.scale([0.29, 0.28, 0.28])
        heatmap_yhat3.move_to([0.96, 0, 0])
        heatmap_yhat3.set_opacity(0.5)
        heatmaps.add(heatmap_yhat3)
        heatmap_yhat1 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_1.png')
        heatmap_yhat1.scale([0.29, 0.28, 0.28])
        heatmap_yhat1.move_to([0.96, 0, 0])
        heatmap_yhat1.set_opacity(0.5)
        heatmaps.add(heatmap_yhat1)
        heatmap_yhat2 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_2.png')
        heatmap_yhat2.scale([0.29, 0.28, 0.28])
        heatmap_yhat2.move_to([0.96, 0, 0])
        heatmap_yhat2.set_opacity(0.5)
        heatmaps.add(heatmap_yhat2)
        canvas_x, canvas_y = latlong_to_canvas(xs[i][0], xs[i][1], label=ys[i], min_long=min_long, max_long=max_long, min_lat=min_lat, max_lat=max_lat, berlin_adjust=[-0.01, 0.02, 0])
        training_point = Dot([canvas_x, canvas_y, 0], radius=0.012)
        if ys[i] == 0.0:
            training_point.set_color('#00FFFF')
        elif ys[i] == 1.0:
            training_point.set_color(YELLOW)
        elif ys[i] == 2.0:
            training_point.set_color(GREEN)
        europe_map = ImageMobject(svg_path + '/map_cropped_one.png')
        europe_map.scale(0.28)
        europe_map.move_to([0.96, 0, 0])
        map_tick_overlays = SVGMobject(svg_path + '/map_tick_overlays_1.svg')[1:]
        map_tick_overlays.scale([0.965, 0.96, 0.965])
        map_tick_overlays.shift([-0.077, 0.0185, 0])
        step_label = Text('Step=')
        step_label.set_color(CHILL_BROWN)
        step_label.scale(0.12)
        step_label.move_to([1.3, -0.85, 0])
        step_count = Text(str(i).zfill(3))
        step_count.set_color(CHILL_BROWN)
        step_count.scale(0.12)
        step_count.move_to([1.43, -0.85, 0])
        self.frame.reorient(0, 0, 0, (-0.04, 0.01, 0.0), 1.94)
        self.add(net_background_0, nums0)
        self.add(grad_regions)
        self.add(europe_map)
        self.add(heatmaps)
        self.add(training_point)
        self.add(step_label, step_count)
        self.add(map_tick_overlays)
        self.wait()
        net_background = SVGMobject(svg_path + '/p44_background_2.svg')[1:]
        axes_1 = Axes(x_range=[-15, 15, 1], y_range=[-15, 15, 1], width=0.32, height=0.32, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 3, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axes_2 = Axes(x_range=[-15, 15, 1], y_range=[-15, 15, 1], width=0.32, height=0.32, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 3, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axes_3 = Axes(x_range=[-15, 15, 1], y_range=[-15, 15, 1], width=0.32, height=0.32, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 3, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axes_1.move_to([-0.95, 0.44, 0])
        axes_2.move_to([-0.95, 0.0, 0])
        axes_3.move_to([-0.95, -0.44, 0])
        nums = get_numbers_b(i, xs, weights, logits, yhats)
        self.wait()
        self.play(FadeOut(grad_regions))
        self.play(FadeOut(net_background_0), FadeIn(net_background), *[ReplacementTransform(nums0[i], nums[i]) for i in range(len(nums))], run_time=2.5)
        self.add(axes_1, axes_2, axes_3)
        self.wait()

        def line_function_1(x):
            return weights[i, 0] * x + weights[i, 3]
        line_1 = axes_1.get_graph(line_function_1, color='#00FFFF', x_range=[-12, 12])
        arrow_tip_1 = get_arrow_tip(line_1, color='#00FFFF', scale=0.1)

        def line_function_2(x):
            return weights[i, 1] * x + weights[i, 4]
        line_2 = axes_2.get_graph(line_function_2, color=YELLOW, x_range=[-12, 12])
        arrow_tip_2 = get_arrow_tip(line_2, color=YELLOW, scale=0.1)

        def line_function_3(x):
            return weights[i, 2] * x + weights[i, 5]
        line_3 = axes_3.get_graph(line_function_3, color=GREEN, x_range=[-12, 12])
        arrow_tip_3 = get_arrow_tip(line_3, color=GREEN, scale=0.1)
        self.play(ShowCreation(VGroup(line_1, arrow_tip_1)))
        self.wait()
        self.play(ShowCreation(VGroup(line_2, arrow_tip_2)))
        self.wait()
        self.play(ShowCreation(VGroup(line_3, arrow_tip_3)))
        self.wait()
        for i in range(1, len(xs)):
            if i > 0:
                self.remove(line_1, arrow_tip_1)
                self.remove(line_2, arrow_tip_2)
                self.remove(line_3, arrow_tip_3)
                self.remove(nums)
                self.remove(step_label, step_count)
                self.remove(heatmaps)
                self.remove(map_tick_overlays)
            nums = get_numbers_b(i, xs, weights, logits, yhats)

            def line_function_1(x):
                return weights[i, 0] * x + weights[i, 3]
            line_1 = axes_1.get_graph(line_function_1, color='#00FFFF', x_range=[-12, 12])
            arrow_tip_1 = get_arrow_tip(line_1, color='#00FFFF', scale=0.1)

            def line_function_2(x):
                return weights[i, 1] * x + weights[i, 4]
            line_2 = axes_2.get_graph(line_function_2, color=YELLOW, x_range=[-12, 12])
            arrow_tip_2 = get_arrow_tip(line_2, color=YELLOW, scale=0.1)

            def line_function_3(x):
                return weights[i, 2] * x + weights[i, 5]
            line_3 = axes_3.get_graph(line_function_3, color=GREEN, x_range=[-12, 12])
            arrow_tip_3 = get_arrow_tip(line_3, color=GREEN, scale=0.1)
            heatmaps = Group()
            heatmap_yhat3 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_3.png')
            heatmap_yhat3.scale([0.29, 0.28, 0.28])
            heatmap_yhat3.move_to([0.96, 0, 0])
            heatmap_yhat3.set_opacity(0.5)
            heatmaps.add(heatmap_yhat3)
            heatmap_yhat1 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_1.png')
            heatmap_yhat1.scale([0.29, 0.28, 0.28])
            heatmap_yhat1.move_to([0.96, 0, 0])
            heatmap_yhat1.set_opacity(0.5)
            heatmaps.add(heatmap_yhat1)
            heatmap_yhat2 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_2.png')
            heatmap_yhat2.scale([0.29, 0.28, 0.28])
            heatmap_yhat2.move_to([0.96, 0, 0])
            heatmap_yhat2.set_opacity(0.5)
            heatmaps.add(heatmap_yhat2)
            step_label = Text('Step=')
            step_label.set_color(CHILL_BROWN)
            step_label.scale(0.12)
            step_label.move_to([1.3, -0.85, 0])
            step_count = Text(str(i).zfill(3))
            step_count.set_color(CHILL_BROWN)
            step_count.scale(0.12)
            step_count.move_to([1.43, -0.85, 0])
            self.add(step_label, step_count)
            self.add(axes_1, line_1, arrow_tip_1)
            self.add(axes_2, line_2, arrow_tip_2)
            self.add(axes_3, line_3, arrow_tip_3)
            self.add(nums)
            self.add(heatmaps)
            self.add(map_tick_overlays)
            self.wait(0.1)
        self.wait(20)
        self.embed()

class p46b_v2(InteractiveScene):

    def construct(self):
        data = np.load(data_path + '/cities_1d_5.npy')
        xs = data[:, :2]
        ys = data[:, 2]
        weights = data[:, 3:9]
        grads = data[:, 9:15]
        logits = data[:, 15:18]
        yhats = data[:, 18:]
        net_background = SVGMobject(svg_path + '/p44_background_2.svg')
        europe_map = ImageMobject(svg_path + '/map_cropped_one.png')
        europe_map.scale(0.28)
        europe_map.move_to([0.96, 0, 0])
        europe_map_2 = ImageMobject(svg_path + '/map_exports.00_00_01_13.Still001.png')
        europe_map_2.scale(0.28)
        europe_map_2.move_to([0.96, 0, 0])
        europe_map_2.scale(0.4)
        europe_map_2.move_to([-1.005, 0.25, -0.01])
        self.add(europe_map_2)
        europe_map_2.set_opacity(0.0)
        map_tick_overlays = SVGMobject(svg_path + '/map_tick_overlays_1.svg')[1:]
        map_tick_overlays.scale([0.965, 0.96, 0.965])
        map_tick_overlays.shift([-0.077, 0.0185, 0])
        axes_1 = Axes(x_range=[-15, 15, 1], y_range=[-15, 15, 1], width=0.32, height=0.32, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.015, 'length': 0.015}})
        axes_2 = Axes(x_range=[-15, 15, 1], y_range=[-15, 15, 1], width=0.32, height=0.32, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.015, 'length': 0.015}})
        axes_3 = Axes(x_range=[-15, 15, 1], y_range=[-15, 15, 1], width=0.32, height=0.32, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.015, 'length': 0.015}})
        axes_1.move_to([-0.95, 0.44, 0])
        axes_2.move_to([-0.95, 0.0, 0])
        axes_3.move_to([-0.95, -0.44, 0])
        i = 0
        nums = get_numbers_b(i, xs, weights, logits, yhats)

        def line_function_1(x):
            return weights[i, 0] * x + weights[i, 3]
        line_1 = axes_1.get_graph(line_function_1, stroke_width=3, color='#00FFFF', x_range=[-12, 12])
        arrow_tip_1 = get_arrow_tip(line_1, color='#00FFFF', scale=0.08)

        def line_function_2(x):
            return weights[i, 1] * x + weights[i, 4]
        line_2 = axes_2.get_graph(line_function_2, stroke_width=3, color=YELLOW, x_range=[-12, 12])
        arrow_tip_2 = get_arrow_tip(line_2, color=YELLOW, scale=0.08)

        def line_function_3(x):
            return weights[i, 2] * x + weights[i, 5]
        line_3 = axes_3.get_graph(line_function_3, stroke_width=3, color=GREEN, x_range=[-12, 12])
        arrow_tip_3 = get_arrow_tip(line_3, color=GREEN, scale=0.08)
        heatmaps = Group()
        heatmap_yhat3 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_3.png')
        heatmap_yhat3.scale([0.29, 0.28, 0.28])
        heatmap_yhat3.move_to([0.96, 0, 0])
        heatmap_yhat3.set_opacity(0.5)
        heatmaps.add(heatmap_yhat3)
        heatmap_yhat1 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_1.png')
        heatmap_yhat1.scale([0.29, 0.28, 0.28])
        heatmap_yhat1.move_to([0.96, 0, 0])
        heatmap_yhat1.set_opacity(0.5)
        heatmaps.add(heatmap_yhat1)
        heatmap_yhat2 = ImageMobject(heatmap_path + '/' + str(i) + '_yhat_2.png')
        heatmap_yhat2.scale([0.29, 0.28, 0.28])
        heatmap_yhat2.move_to([0.96, 0, 0])
        heatmap_yhat2.set_opacity(0.5)
        heatmaps.add(heatmap_yhat2)
        self.frame.reorient(0, 0, 0, (-0.04, 0.01, 0.0), 1.94)
        self.add(net_background)
        self.add(europe_map)
        self.add(axes_1, axes_2, axes_3)
        self.add(axes_1, line_1, arrow_tip_1)
        self.add(axes_2, line_2, arrow_tip_2)
        self.add(axes_3, line_3, arrow_tip_3)
        self.add(nums)
        self.add(heatmaps)
        self.add(map_tick_overlays)
        self.wait()
        top_plot_group = VGroup(axes_1, line_1, arrow_tip_1)
        middle_plot_group = VGroup(axes_2, line_2, arrow_tip_2)
        bottom_plot_group = VGroup(axes_3, line_3, arrow_tip_3)
        background_elements_to_remove = background_elements_to_remove = [31, 32, 33, 34, 35, 36, 45, 46, 47, 48, 49, 50, 82, 83, 84, 85, 86, 89, 90]
        background_elements_to_keep = [i for i in range(len(net_background)) if i not in background_elements_to_remove]
        self.wait()
        self.play(top_plot_group.animate.scale(1.5).move_to([-1.0, 0.025, 0]), middle_plot_group.animate.scale(1.5).move_to([-1.0, 0.025, 0]), bottom_plot_group.animate.scale(1.5).move_to([-1.0, 0.025, 0]), *[FadeOut(net_background[o]) for o in background_elements_to_remove], *[net_background[o].animate.set_opacity(0.5) for o in background_elements_to_keep], FadeOut(nums[1:7]), nums[0].animate.set_opacity(0.3), nums[7:].animate.set_opacity(0.3), self.frame.animate.reorient(0, 0, 0, (-0.64, 0.0, 0.0), 1.14), run_time=4.0)
        self.remove(axes_1, axes_3)
        self.remove(arrow_tip_2)
        self.add(arrow_tip_2)
        self.wait()
        overlays_1 = SVGMobject(svg_path + '/p46_overlays_1.svg')
        overlays_2 = SVGMobject(svg_path + '/p46_overlays_2.svg')
        overlays_1.scale(0.57)
        overlays_1.move_to([-0.64, 0.003, 0])
        self.wait()
        self.play(FadeIn(overlays_1[1:]), nums[0].animate.set_opacity(1.0), nums[7].animate.set_opacity(1.0))
        self.wait()
        box = SurroundingRectangle(nums[-3], color=YELLOW, buff=0.025)
        self.play(nums[-3].animate.set_opacity(1.0), ShowCreation(box))
        self.wait()
        self.play(nums[-3].animate.set_opacity(0.3), FadeOut(box))
        self.wait(0)
        overlays_2.scale(0.3)
        overlays_2.move_to([-1.02, 0.025, 0])
        madrid_label = overlays_2[1:18]
        madrid_label.shift([0.015, 0, 0])
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-1.02, 0.02, 0.0), 0.62), *[net_background[o].animate.set_opacity(0.0) for o in background_elements_to_keep], nums[0].animate.set_opacity(0.0), nums[7:].animate.set_opacity(0.0), overlays_1[1:].animate.set_opacity(0.0), run_time=3.0)
        self.add(overlays_2[1:])
        self.wait()
        step_label = Text('Step=')
        step_label.set_color(CHILL_BROWN)
        step_label.scale(0.04)
        step_label.move_to([-0.58, -0.25, 0])
        step_count = Text(str(i).zfill(3))
        step_count.set_color(CHILL_BROWN)
        step_count.scale(0.04)
        step_count.next_to(step_label, RIGHT, buff=0.003)
        self.play(FadeIn(step_label), FadeIn(step_count))
        for i in range(1, len(xs)):
            if i > 0:
                self.remove(line_1, arrow_tip_1)
                self.remove(line_2, arrow_tip_2)
                self.remove(line_3, arrow_tip_3)
                self.remove(step_label, step_count)
            nums = get_numbers_b(i, xs, weights, logits, yhats)

            def line_function_1(x):
                return weights[i, 0] * x + weights[i, 3]
            line_1 = axes_1.get_graph(line_function_1, color='#00FFFF', x_range=[-12, 12])
            arrow_tip_1 = get_arrow_tip(line_1, color='#00FFFF', scale=0.1)

            def line_function_2(x):
                return weights[i, 1] * x + weights[i, 4]
            line_2 = axes_2.get_graph(line_function_2, color=YELLOW, x_range=[-12, 12])
            arrow_tip_2 = get_arrow_tip(line_2, color=YELLOW, scale=0.1)

            def line_function_3(x):
                return weights[i, 2] * x + weights[i, 5]
            line_3 = axes_3.get_graph(line_function_3, color=GREEN, x_range=[-12, 12])
            arrow_tip_3 = get_arrow_tip(line_3, color=GREEN, scale=0.1)
            heatmaps.add(heatmap_yhat2)
            step_label = Text('Step=')
            step_label.set_color(CHILL_BROWN)
            step_label.scale(0.04)
            step_label.move_to([-0.58, -0.25, 0])
            step_count = Text(str(i).zfill(3))
            step_count.set_color(CHILL_BROWN)
            step_count.scale(0.04)
            step_count.next_to(step_label, RIGHT, buff=0.003)
            self.add(step_label, step_count)
            self.add(line_1, arrow_tip_1)
            self.add(line_2, arrow_tip_2)
            self.add(line_3, arrow_tip_3)
            self.wait(0.1)
        self.wait()

        def line_function_1(x):
            return weights[i, 0] * x + weights[i, 3]
        line_1_long = axes_1.get_graph(line_function_1, color='#00FFFF', x_range=[-14.5, 14.5])
        arrow_tip_1_long = get_arrow_tip(line_1_long, color='#00FFFF', scale=0.1)

        def line_function_2(x):
            return weights[i, 1] * x + weights[i, 4]
        line_2_long = axes_2.get_graph(line_function_2, color=YELLOW, x_range=[-14.5, 14.5])
        arrow_tip_2_long = get_arrow_tip(line_2_long, color=YELLOW, scale=0.1)

        def line_function_3(x):
            return weights[i, 2] * x + weights[i, 5]
        line_3_long = axes_3.get_graph(line_function_3, color=GREEN, x_range=[-14.5, 14.5])
        arrow_tip_3_long = get_arrow_tip(line_3_long, color=GREEN, scale=0.1)
        self.wait()
        self.remove(europe_map, heatmaps, map_tick_overlays, step_label, step_count)
        stuff_to_rotate = VGroup(axes_2, line_1_long, line_2_long, line_3_long, arrow_tip_1_long, arrow_tip_2_long, arrow_tip_3_long, line_1, line_2, line_3, arrow_tip_1, arrow_tip_2, arrow_tip_3)
        stuff_to_rotate.rotate(90 * DEGREES, [1, 0, 0])
        overlays_2.rotate(90 * DEGREES, [1, 0, 0])
        self.frame.reorient(0, 90, 0, (-1.02, 0.02, 0.0), 0.62)
        self.wait()
        europe_map_2.set_opacity(1.0)
        madrid_label = overlays_2[1:18]
        berlin_label = overlays_2[33:50]
        paris_label = overlays_2[18:33]
        plane_1_zero = create_plane_from_line_endpoints(line_1_long, '#00FFFF', y_extension=0.01)
        plane_1_full = create_plane_from_line_endpoints(line_1_long, '#00FFFF', y_extension=0.5)
        plane_1_zero.set_opacity(0.3)
        plane_1_full.set_opacity(0.3)
        plane_2_zero = create_plane_from_line_endpoints(line_2_long, YELLOW, y_extension=0.01)
        plane_2_full = create_plane_from_line_endpoints(line_2_long, YELLOW, y_extension=0.5)
        plane_2_zero.set_opacity(0.3)
        plane_2_full.set_opacity(0.3)
        plane_3_zero = create_plane_from_line_endpoints(line_3_long, GREEN, y_extension=0.01)
        plane_3_full = create_plane_from_line_endpoints(line_3_long, GREEN, y_extension=0.5)
        plane_3_zero.set_opacity(0.3)
        plane_3_full.set_opacity(0.3)
        self.wait()
        self.play(self.frame.animate.reorient(-30, 59, 0, (-1.02, 0.04, -0.0), 0.62), madrid_label.animate.move_to([-1.065, 0.12, -0.06620278]), paris_label.animate.move_to([-0.97, 0.295, -0.06596944]), berlin_label.animate.move_to([-0.805, 0.38, -0.06464722]), run_time=3.0)
        self.wait()
        self.play(self.frame.animate.reorient(18, 57, 0, (-0.95, 0.08, 0.05), 0.62), Transform(plane_1_zero, plane_1_full), Transform(plane_2_zero, plane_2_full), Transform(plane_3_zero, plane_3_full), run_time=3.0)
        self.wait()

        def softmax_function(x):
            logit_1 = weights[i][0] * x + weights[i][3]
            logit_2 = weights[i][1] * x + weights[i][4]
            logit_3 = weights[i][2] * x + weights[i][5]
            logits = np.array([logit_1, logit_2, logit_3])
            exp_logits = np.exp(logits - np.max(logits))
            probabilities = exp_logits / np.sum(exp_logits)
            return softmax_viz_scale * probabilities[neuron_index]
        softmax_viz_scale = 5.0
        neuron_index = 0
        softmax_curve_1 = axes_2.get_graph(softmax_function, x_range=(-14.5, 14.5), color='#00FFFF', stroke_width=3)
        neuron_index = 1
        softmax_curve_2 = axes_2.get_graph(softmax_function, x_range=(-14.5, 14.5), color=YELLOW, stroke_width=3)
        neuron_index = 2
        softmax_curve_3 = axes_2.get_graph(softmax_function, x_range=(-14.5, 14.5), color=GREEN, stroke_width=3)
        self.wait()
        softmax_curve_1.set_fill(opacity=0)
        softmax_curve_1.set_stroke(color='#00FFFF', width=3)
        softmax_curve_2.set_fill(opacity=0)
        softmax_curve_2.set_stroke(color=YELLOW, width=3)
        softmax_curve_3.set_fill(opacity=0)
        softmax_curve_3.set_stroke(color=GREEN, width=3)
        line_1_long.set_fill(opacity=0)
        line_1_long.set_stroke(color='#00FFFF', width=3)
        line_2_long.set_fill(opacity=0)
        line_2_long.set_stroke(color=YELLOW, width=3)
        line_3_long.set_fill(opacity=0)
        line_3_long.set_stroke(color=GREEN, width=3)
        line_1.set_fill(opacity=0)
        line_1.set_stroke(color='#00FFFF', width=3)
        line_2.set_fill(opacity=0)
        line_2.set_stroke(color=YELLOW, width=3)
        line_3.set_fill(opacity=0)
        line_3.set_stroke(color=GREEN, width=3)
        softmax_surface_1 = create_surface_from_curve_simple(curve=softmax_curve_1, y_extension=0.5)
        softmax_surface_2 = create_surface_from_curve_simple(curve=softmax_curve_2, y_extension=0.5)
        softmax_surface_3 = create_surface_from_curve_simple(curve=softmax_curve_3, y_extension=0.5)
        matching_plane_1, matching_surface_1 = create_matching_plane_and_surface(line_1_long, softmax_curve_1, y_extension=0.5, color='#00FFFF')
        matching_plane_2, matching_surface_2 = create_matching_plane_and_surface(line_2_long, softmax_curve_2, y_extension=0.5, color=YELLOW)
        matching_plane_3, matching_surface_3 = create_matching_plane_and_surface(line_3_long, softmax_curve_3, y_extension=0.5, color=GREEN)
        self.wait()
        self.remove(plane_1_zero, plane_2_zero, plane_3_zero)
        self.add(matching_plane_1, matching_plane_2, matching_plane_3)
        self.remove(arrow_tip_1, arrow_tip_2, arrow_tip_3)
        self.play(Transform(matching_plane_1, matching_surface_1), ReplacementTransform(line_1, softmax_curve_1), Transform(matching_plane_2, matching_surface_2), ReplacementTransform(line_2, softmax_curve_2), Transform(matching_plane_3, matching_surface_3), ReplacementTransform(line_3, softmax_curve_3), run_time=6)
        matching_plane_3.shift([0, 0, -0.0001])
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-1.03, 0.24, 0.1), 0.62), run_time=7)
        self.wait()
        self.wait(20)
        self.embed()