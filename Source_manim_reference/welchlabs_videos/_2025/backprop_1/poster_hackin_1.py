from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
from functools import partial
from tqdm import tqdm
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
loss_curve_1 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_24_5/all_execpt_embedding_random_64.npy')
loss_curve_2 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_24_5/all_execpt_embedding_random_51.npy')
loss_curve_3 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_24_7/all_execpt_embedding_pretrained_19.npy')
loss_curve_4 = np.load('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/apr_24_7/all_execpt_embedding_pretrained_27.npy')
wormhole_dir = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/hackin/wormhole_merged/'
alphas_1 = np.linspace(-2.5, 2.5, 512)
loss_2d_1 = np.load(wormhole_dir + '000.npy')

class Dot3D(Sphere):

    def __init__(self, center=ORIGIN, radius=0.05, **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.move_to(center)

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

def get_pivot_and_scale(axis_min, axis_max, axis_end):
    scale = axis_end / (axis_max - axis_min)
    return (axis_min, scale)

class PosterHackinTwo(InteractiveScene):

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
        self.frame.reorient(90, 0, 0, (0.01, 0.03, -0.0), 6.45)
        self.wait()
        self.frame.reorient(90, 20, 0, (-0.09, 0.02, 0.04), 6.45)
        self.wait()
        self.frame.reorient(89, 32, 0, (-0.1, -0.0, 0.05), 5.89)
        self.wait()
        self.frame.reorient(135, 25, 0, (0.02, 0.1, -0.11), 7.56)
        self.wait()
        self.frame.reorient(137, 41, 0, (0.14, -0.04, -0.09), 6.81)
        self.wait()
        self.wait()
        self.embed()
        self.wait(20)
        self.embed()