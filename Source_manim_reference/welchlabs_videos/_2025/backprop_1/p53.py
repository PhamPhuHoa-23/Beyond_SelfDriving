from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
import matplotlib.pyplot as plt
from tqdm import tqdm
save_dir = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/'
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'

class Dot3D(Sphere):

    def __init__(self, center=ORIGIN, radius=0.05, **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.move_to(center)

def manual_camera_interpolation(start_orientation, end_orientation, num_steps):
    result = []
    for step in range(num_steps):
        t = step / (num_steps - 1) if num_steps > 1 else 0
        interpolated = []
        for i in range(len(start_orientation)):
            if i == 3:
                start_tuple = start_orientation[i]
                end_tuple = end_orientation[i]
                interpolated_tuple = tuple((start_tuple[j] + t * (end_tuple[j] - start_tuple[j]) for j in range(len(start_tuple))))
                interpolated.append(interpolated_tuple)
            else:
                start_val = start_orientation[i]
                end_val = end_orientation[i]
                interpolated_val = start_val + t * (end_val - start_val)
                interpolated.append(interpolated_val)
        result.append(interpolated)
    return result
num_points = 20
true_slope = 0.61
true_intercept = 1
noise_level = 2.2
learning_rate = 0.01
num_iterations = 1000
np.random.seed(2)
x_values = np.random.uniform(0, 8, num_points)
y_values = true_slope * x_values + true_intercept + (np.random.random(num_points) - 0.5) * noise_level
slope = 0.5
intercept = 2.0
predictions = slope * x_values + intercept
errors = predictions - y_values
loss = np.mean(errors ** 2)
slopes = [slope]
intercepts = [intercept]
losses = [loss]
for iteration in range(num_iterations):
    slope_gradient = 2 * np.mean(errors * x_values)
    intercept_gradient = 2 * np.mean(errors)
    new_slope = slope - learning_rate * slope_gradient
    new_intercept = intercept - learning_rate * intercept_gradient
    new_predictions = new_slope * x_values + new_intercept
    new_errors = new_predictions - y_values
    new_loss = np.mean(new_errors ** 2)
    slope = new_slope
    intercept = new_intercept
    errors = new_errors
    loss = new_loss
    slopes.append(slope)
    intercepts.append(intercept)
    losses.append(loss)
slope_min = 0.0
slope_max = 1.0
y_int_min = 0.0
y_int_max = 2.0
landscape_slopes = np.linspace(slope_min, slope_max, 256)
landscape_intercepts = np.linspace(y_int_min, y_int_max, 256)
z = []
for s in tqdm(landscape_slopes):
    z.append([])
    for yi in landscape_intercepts:
        yhat = s * x_values + yi
        e = yhat - y_values
        l = np.mean(e ** 2)
        z[-1].append(l)
Z = np.array(z)
plt.figure(frameon=False)
ax = plt.Axes(plt.gcf(), [0.0, 0.0, 1.0, 1.0])
ax.set_axis_off()
plt.gcf().add_axes(ax)
plt.imshow(np.rot90(Z))
plt.savefig(save_dir + 'p53_2d.png', bbox_inches='tight', pad_inches=0, dpi=300)
plt.close()

class P53_3D_v3(InteractiveScene):

    def construct(self):
        surf = 3.5 * Z / Z.max()
        axes = ThreeDAxes(x_range=[slope_min, slope_max, 1], y_range=[y_int_min, y_int_max, 2], z_range=[0.0, 3.5, 1.0], height=5, width=5, depth=3.5, axis_config={'include_ticks': True, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'tip_config': {'fill_opacity': 1, 'width': 0.1, 'length': 0.1}})
        x_label = Tex('slope', font_size=40).set_color(CHILL_BROWN)
        y_label = Tex('y-intercept', font_size=40).set_color(CHILL_BROWN)
        z_label = Tex('Loss', font_size=30).set_color(CHILL_BROWN)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label.next_to(axes.y_axis, UP)
        z_label.next_to(axes.z_axis, OUT)
        z_label.rotate(90 * DEGREES, [1, 0, 0])

        def param_surface(u, v):
            u_idx = np.abs(landscape_slopes - u).argmin()
            v_idx = np.abs(landscape_intercepts - v).argmin()
            try:
                z_val = surf[u_idx, v_idx]
            except IndexError:
                z_val = 0
            return axes.c2p(u, v, z_val)
        surface = ParametricSurface(param_surface, u_range=[slope_min, slope_max], v_range=[y_int_min, y_int_max], resolution=(256, 256))
        ts = TexturedSurface(surface, save_dir + 'p53_2d.png')
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.7)
        num_lines = 20
        num_points = 256
        u_gridlines = VGroup()
        v_gridlines = VGroup()
        u_values = np.linspace(slope_min, slope_max, num_lines)
        v_points = np.linspace(y_int_min, y_int_max, num_points)
        for u in u_values:
            points = [axes.c2p(u, v, param_surface(u, v)[2]) for v in v_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            u_gridlines.add(line)
        v_values = np.linspace(y_int_min, y_int_max, num_lines)
        u_points = np.linspace(slope_min, slope_max, num_points)
        for v in v_values:
            points = [axes.c2p(u, v, param_surface(u, v)[2]) for u in u_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            v_gridlines.add(line)
        surface_group = Group(ts, u_gridlines, v_gridlines)
        self.add(axes[:2], x_label, y_label)
        self.add(surface_group)
        self.frame.reorient(0, 27, 0, (0.85, 1.29, 0.26), 9.73)
        self.wait()
        t = VMobject()
        t.set_stroke(width=5, color='#FF00FF', opacity=0.9)
        s1 = Dot3D(center=axes.c2p(slopes[0], intercepts[0], 3.5 * losses[0] / Z.max()), radius=0.09, color='$FF00FF')
        self.add(t)
        self.add(s1)
        start_orientation = [0, 8, 0, (0.06, -0.01, 0.09), 9.62]
        end_orientation = [0, 18, 0, (0.06, -0.01, 0.09), 9.62]
        interp_orientations = manual_camera_interpolation(start_orientation, end_orientation, num_steps=num_iterations)
        for iter_count in range(num_iterations):
            self.remove(t)
            t = VMobject()
            t.set_stroke(width=5, color='#FF00FF', opacity=0.9)
            trajectory_points = []
            for s, i, l in zip(slopes[:iter_count], intercepts[:iter_count], losses[:iter_count]):
                point = axes.c2p(s, i, 3.5 * l / Z.max())
                trajectory_points.append(point)
            t.set_points_smoothly(trajectory_points)
            self.add(t)
            s1.move_to(axes.c2p(slopes[iter_count], intercepts[iter_count], 3.5 * losses[iter_count] / Z.max()))
            self.frame.reorient(*interp_orientations[iter_count])
            self.wait(1 / 30.0)
        self.wait()
        self.play(FadeOut(axes[:2]), FadeOut(x_label), FadeOut(y_label), run_time=3)
        self.wait(20)
        self.embed()

class P53_2D(InteractiveScene):

    def construct(self):
        x_axis_1 = WelchXAxis(x_min=0, x_max=8.5, x_ticks=[2, 4, 6, 8], x_tick_height=0.15, x_label_font_size=22, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        y_axis_1 = WelchYAxis(y_min=0, y_max=8.5, y_ticks=[2, 4, 6, 8], y_tick_width=0.15, y_label_font_size=22, stroke_width=2.5, arrow_tip_scale=0.1, axis_length_on_canvas=4)
        x_label_1 = Tex('x', font_size=28).set_color(CHILL_BROWN)
        y_label_1 = Tex('y', font_size=28).set_color(CHILL_BROWN)
        x_label_1.next_to(x_axis_1, RIGHT, buff=0.05)
        y_label_1.next_to(y_axis_1, UP, buff=0.08)
        axes_1 = VGroup(x_axis_1, y_axis_1, x_label_1, y_label_1)
        self.add(axes_1)
        self.wait()
        mapped_x_1 = x_axis_1.map_to_canvas(x_values)
        mapped_y_1 = y_axis_1.map_to_canvas(y_values)
        dots = VGroup()
        for i in range(num_points):
            dot = Dot([mapped_x_1[i], mapped_y_1[i], 0], radius=0.06)
            dot.set_color(YELLOW)
            dot.set_opacity(0.95)
            dots.add(dot)
        self.add(dots)
        self.frame.reorient(0, 0, 0, (-1.29, 1.85, 0.0), 8.0)
        line_points = np.array([[0, intercepts[0], 0], [8, slopes[0] * 8 + intercepts[0], 0]])
        line_points_mapped = np.zeros_like(line_points)
        line_points_mapped[:, 0] = x_axis_1.map_to_canvas(line_points[:, 0])
        line_points_mapped[:, 1] = y_axis_1.map_to_canvas(line_points[:, 1])
        line = VGroup()
        line.set_points_smoothly(line_points_mapped)
        line.set_stroke(width=4, color=YELLOW, opacity=1.0)
        self.add(line)
        line_label = Tex(f'y = {slope:.2f}x + {intercept:.2f}', font_size=24)
        line_label.next_to(axes_1, UP).shift(0.3 * DOWN)
        line_label.set_color(YELLOW)
        self.add(line_label)
        for i in range(num_iterations):
            self.remove(line, line_label)
            line_points = np.array([[0, intercepts[i], 0], [8, slopes[i] * 8 + intercepts[i], 0]])
            line_points_mapped = np.zeros_like(line_points)
            line_points_mapped[:, 0] = x_axis_1.map_to_canvas(line_points[:, 0])
            line_points_mapped[:, 1] = y_axis_1.map_to_canvas(line_points[:, 1])
            line = VGroup()
            line.set_points_smoothly(line_points_mapped)
            line.set_stroke(width=4, color=YELLOW, opacity=1.0)
            self.add(line)
            line_label = Tex(f'y = {slopes[i]:.2f}x + {intercepts[i]:.2f}', font_size=24)
            line_label.next_to(axes_1, UP).shift(0.3 * DOWN)
            line_label.set_color(YELLOW)
            self.add(line_label)
            self.wait(1 / 30.0)
        self.wait()
        self.embed()