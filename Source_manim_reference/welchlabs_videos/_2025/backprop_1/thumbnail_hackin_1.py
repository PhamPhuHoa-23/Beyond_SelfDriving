from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
from functools import partial
from tqdm import tqdm
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
save_dir = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/'
xy = np.linspace(-2.5, 2.5, 256)
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-2.5, 2.5, 256)
y = np.linspace(-2.5, 2.5, 256)
X, Y = np.meshgrid(x, y)
Z = 0.25 * (X ** 2 + Y ** 2)
plt.figure(frameon=False)
ax = plt.Axes(plt.gcf(), [0.0, 0.0, 1.0, 1.0])
ax.set_axis_off()
plt.gcf().add_axes(ax)
plt.imshow(np.rot90(Z))
plt.savefig(save_dir + 'thumnbail_simple_loss_1.png', bbox_inches='tight', pad_inches=0, dpi=300)
plt.close()
wormhole_dir = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/wormhole_merged/'
alphas_1 = np.linspace(-2.5, 2.5, 512)
loss_2d_1 = np.load(wormhole_dir + '000.npy')

def param_surface_1(u, v):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = 0.07 * loss_2d_1[v_idx, u_idx]
    except IndexError:
        z = 0
    return np.array([u, v, z])

def param_surface_2(u, v, surf_array):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = 0.07 * surf_array[v_idx, u_idx]
    except IndexError:
        z = 0
    return np.array([u, v, z])

def get_numerical_gradient(surface_fn, u, v, epsilon=0.01):
    height = surface_fn(u, v)[2]
    height_du = surface_fn(u + epsilon, v)[2]
    du = (height_du - height) / epsilon
    height_dv = surface_fn(u, v + epsilon)[2]
    dv = (height_dv - height) / epsilon
    return (du, dv)

class Dot3D(Sphere):

    def __init__(self, center=ORIGIN, radius=0.05, **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.move_to(center)

class ThumbnailOneV2(InteractiveScene):

    def construct(self):
        axes = ThreeDAxes(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[0.0, 3.5, 1.0], height=5, width=5, depth=3.5, axis_config={'include_ticks': True, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'tip_config': {'fill_opacity': 1, 'width': 0.1, 'length': 0.1}})

        def param_surface(u, v):
            u_idx = np.abs(xy - u).argmin()
            v_idx = np.abs(xy - v).argmin()
            try:
                z = Z[u_idx, v_idx]
            except IndexError:
                z = 0
            return np.array([u, v, z])
        surface = ParametricSurface(param_surface, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(256, 256))
        ts = TexturedSurface(surface, save_dir + 'thumnbail_simple_loss_1.png')
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(1.0)
        num_lines = 20
        num_points = 256
        u_gridlines = VGroup()
        v_gridlines = VGroup()
        u_values = np.linspace(-2.5, 2.5, num_lines)
        v_points = np.linspace(-2.5, 2.5, num_points)
        for u in u_values:
            points = [param_surface(u, v) for v in v_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=2, color=WHITE, opacity=0.3)
            u_gridlines.add(line)
        u_points = np.linspace(-2.5, 2.5, num_points)
        for v in u_values:
            points = [param_surface(u, v) for u in u_points]
            line = VMobject()
            line.set_points_smoothly(points)
            line.set_stroke(width=2, color=WHITE, opacity=0.3)
            v_gridlines.add(line)
        offset = surface.get_corner(BOTTOM + LEFT) - axes.get_corner(BOTTOM + LEFT)
        axes.shift(offset)
        self.frame.reorient(0, 0, 0, (0, 0, 0), 8.0)
        self.add(ts, u_gridlines, v_gridlines)
        self.wait()
        starting_coords = [-2.2, -1.5]
        starting_point = param_surface(*starting_coords)
        s1 = Dot3D(center=starting_point, radius=0.17, color=YELLOW)
        num_steps = 128
        learning_rate = 0.003
        momentum = 0.95
        trajectory = [[starting_point[0], starting_point[1], param_surface(starting_point[0], starting_point[1])[2]]]
        velocity = np.array([0.0, 0.08])
        for i in range(num_steps):
            g = get_numerical_gradient(param_surface, trajectory[-1][0], trajectory[-1][1], epsilon=0.01)
            velocity = momentum * velocity - learning_rate * np.array(g)
            new_x = trajectory[-1][0] + velocity[0]
            new_y = trajectory[-1][1] + velocity[1]
            trajectory.append([new_x, new_y, param_surface(new_x, new_y)[2]])
        t = VMobject()
        t.set_stroke(width=10, color=YELLOW, opacity=0.9)
        t.set_points_smoothly(trajectory)
        self.add(t)
        s1.move_to(trajectory[-1])
        self.add(s1)
        self.wait()
        self.embed()

class ThumbnailTwoV1(InteractiveScene):

    def construct(self):
        starting_coords = [0.05, -0.9]
        starting_point = param_surface_1(*starting_coords)
        s2 = Dot3D(center=starting_point, radius=0.06, color='$FF00FF')
        loss_arrays = []
        num_time_steps = 1
        print('Loading Surface Arrays')
        for i in tqdm(range(num_time_steps)):
            loss_arrays.append(np.load(wormhole_dir + str(i).zfill(3) + '.npy'))
        surfaces = Group()
        surf_functions = []
        grids = Group()
        print('Loading Surfaces and Gridlines...')
        for i in tqdm(range(num_time_steps)):
            surf_func = partial(param_surface_2, surf_array=loss_arrays[i])
            surf_functions.append(surf_func)
            surface = ParametricSurface(surf_func, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
            ts2 = TexturedSurface(surface, wormhole_dir + 'loss_2d_1_' + str(i).zfill(3) + '.png')
            ts2.set_shading(0.0, 0.1, 0)
            surfaces.add(ts2)
            num_lines = 64
            num_points = 512
            u_gridlines = VGroup()
            v_gridlines = VGroup()
            u_values = np.linspace(-2.5, 2.5, num_lines)
            v_points = np.linspace(-2.5, 2.5, num_points)
            for u in u_values:
                points = [surf_func(u, v) for v in v_points]
                line = VMobject()
                line.set_points_smoothly(points)
                line.set_stroke(width=1, color=WHITE, opacity=0.15)
                u_gridlines.add(line)
            u_points = np.linspace(-2.5, 2.5, num_points)
            for v in u_values:
                points = [surf_func(u, v) for u in u_points]
                line = VMobject()
                line.set_points_smoothly(points)
                line.set_stroke(width=1, color=WHITE, opacity=0.15)
                v_gridlines.add(line)
            grids.add(VGroup(u_gridlines, v_gridlines))
        self.wait()
        self.add(surfaces[0])
        self.add(grids[0])
        self.add(s2)
        self.remove(s2)
        self.frame.reorient(137, 20, 0, (0.15, 0.11, -0.02), 7.95)
        self.wait()
        self.frame.reorient(137, 20, 0, (0.15, 0.11, -0.02), 7.95)
        self.wait()
        self.frame.reorient(93, 41, 0, (-0.03, 0.01, 0.15), 6.0)
        self.wait()
        self.frame.reorient(0, 21, 0, (-0.03, 0.0, 0.12), 6.32)
        self.wait()
        self.frame.reorient(0, 42, 0, (0.06, 0.13, 0.25), 6.32)
        self.wait()
        self.wait()
        self.embed()
        self.wait(20)
        self.embed()