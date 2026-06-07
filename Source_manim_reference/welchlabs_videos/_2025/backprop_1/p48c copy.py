from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
from functools import partial
from tqdm import tqdm
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
wormhole_dir = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_29_2/'
alphas_1 = np.linspace(-2.5, 2.5, 512)

class Dot3D(Sphere):

    def __init__(self, center=ORIGIN, radius=0.05, **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.move_to(center)

def param_surface_1(u, v):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = 0.25 * loss_2d_1[v_idx, u_idx] - 0.18 * np.mean(loss_2d_1)
    except IndexError:
        z = 0
    return np.array([u, v, z])

def param_surface_2(u, v, surf_array):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = 0.14 * surf_array[v_idx, u_idx] - 0.07 * np.mean(surf_array)
    except IndexError:
        z = 0
    return np.array([u, v, z])

def get_pivot_and_scale(axis_min, axis_max, axis_end):
    scale = axis_end / (axis_max - axis_min)
    return (axis_min, scale)

def get_numerical_gradient(surface_fn, u, v, epsilon=0.01):
    height = surface_fn(u, v)[2]
    height_du = surface_fn(u + epsilon, v)[2]
    du = (height_du - height) / epsilon
    height_dv = surface_fn(u, v + epsilon)[2]
    dv = (height_dv - height) / epsilon
    return (du, dv)

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

class P48cV3(InteractiveScene):

    def construct(self):
        loss_arrays_pre = []
        loss_arrays_post = []
        loss_arrays_interleaved = []
        num_time_steps = 4
        print('Loading Surface Arrays...')
        for i in tqdm(range(num_time_steps)):
            loss_arrays_pre.append(np.load(wormhole_dir + 'pre_step_' + str(i).zfill(3) + '.npy'))
            loss_arrays_post.append(np.load(wormhole_dir + 'post_step_' + str(i).zfill(3) + '.npy'))
            loss_arrays_interleaved.append(loss_arrays_pre[-1])
            loss_arrays_interleaved.append(loss_arrays_post[-1])
        self.wait()
        import matplotlib.pyplot as plt
        data_max = np.array(loss_arrays_interleaved).max()
        for i in range(len(loss_arrays_interleaved)):
            plt.clf()
            plt.figure(frameon=False)
            ax = plt.Axes(plt.gcf(), [0.0, 0.0, 1.0, 1.0])
            ax.set_axis_off()
            plt.gcf().add_axes(ax)
            plt.imshow(np.rot90(loss_arrays_interleaved[i].T), vmax=1.2 * data_max)
            plt.savefig(wormhole_dir + 'loss_arrays_interleaved_' + str(i).zfill(3) + '.png', bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()
        surfaces = Group()
        surf_functions = []
        grids = Group()
        print('Loading Surfaces and Gridlines...')
        for i in tqdm(range(len(loss_arrays_interleaved))):
            surf_func = partial(param_surface_2, surf_array=loss_arrays_interleaved[i])
            surf_functions.append(surf_func)
            surface = ParametricSurface(surf_func, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
            ts2 = TexturedSurface(surface, wormhole_dir + 'loss_arrays_interleaved_' + str(i).zfill(3) + '.png')
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
        starting_coords = [0.05, -0.9]
        starting_point = surf_functions[0](*starting_coords)
        s2 = Dot3D(center=starting_point, radius=0.06, color='$FF00FF')
        self.frame.reorient(180, 23, 0, (-0.06, 0.09, 0.43), 5.81)
        self.wait()
        self.play(ShowCreation(surfaces[0]), ShowCreation(grids[0]), run_time=6.0)
        self.add(s2)
        self.wait()
        self.play(self.frame.animate.reorient(135, 47, 0, (0.15, 0.28, -0.04), 5.61), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(143, 52, 0, (0.0, -0.33, 0.52), 3.09), run_time=4)
        self.wait()
        for i in range(1, len(surfaces)):
            self.remove(surfaces[i - 1])
            self.remove(grids[i - 1])
            self.add(surfaces[i])
            self.add(grids[i])
            new_point_coords = surf_functions[i](*starting_coords)
            s2.move_to(new_point_coords)
            self.wait()
        self.play(self.frame.animate.reorient(180, 23, 0, (-0.06, 0.09, 0.43), 5.81), run_time=4)
        self.wait()
        self.remove(surfaces[i])
        self.remove(grids[i])
        self.add(surfaces[0])
        self.add(grids[0])
        new_point_coords = surf_functions[0](*starting_coords)
        s2.move_to(new_point_coords)
        for i in range(1, len(surfaces)):
            self.remove(surfaces[i - 1])
            self.remove(grids[i - 1])
            self.add(surfaces[i])
            self.add(grids[i])
            new_point_coords = surf_functions[i](*starting_coords)
            s2.move_to(new_point_coords)
            self.wait()
        self.wait(20)
        self.embed()