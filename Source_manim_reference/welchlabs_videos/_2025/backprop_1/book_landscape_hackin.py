from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
from functools import partial
from tqdm import tqdm
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
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

def get_numerical_gradient(surface_fn, u, v, epsilon=0.01):
    height = surface_fn(u, v)[2]
    height_du = surface_fn(u + epsilon, v)[2]
    du = (height_du - height) / epsilon
    height_dv = surface_fn(u, v + epsilon)[2]
    dv = (height_dv - height) / epsilon
    return (du, dv)

def copy_frame_positioning_precise(frame):
    center = frame.get_center()
    height = frame.get_height()
    angles = frame.get_euler_angles()
    call = f'reorient('
    theta, phi, gamma = angles / DEG
    call += f'{theta}, {phi}, {gamma}'
    if any(center != 0):
        call += f', {tuple(center)}'
    if height != FRAME_HEIGHT:
        call += ', {:.2f}'.format(height)
    call += ')'
    print(call)
    pyperclip.copy(call)

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

class BookLanscapeOne(InteractiveScene):

    def construct(self):
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
        self.frame.reorient(0, 11, 0, (0.01, 0.03, 0.12), 6.37)
        self.wait()
        self.play(self.frame.animate.reorient(91, 44, 0, (-0.15, -0.0, 0.07), 5.78), run_time=10.0)
        self.wait()
        self.wait()
        self.frame.reorient(129, 35, 0, (-0.55, 0.57, -0.35), 3.75)
        self.wait()
        self.frame.reorient(133, 38, 0, (-0.7, 0.51, -0.24), 2.97)
        self.wait()
        self.embed()
        self.wait(20)
        self.embed()

class ending_moves(InteractiveScene):

    def construct(self):
        starting_coords = [0.05, -0.9]
        starting_point = param_surface_1(*starting_coords)
        s2 = Dot3D(center=starting_point, radius=0.06, color='$FF00FF')
        loss_arrays = []
        num_time_steps = 66
        print('Loading Surface Arrays')
        for i in tqdm(range(num_time_steps)):
            loss_arrays.append(np.load(wormhole_dir + str(i).zfill(3) + '.npy'))
        surfaces = Group()
        surf_functions = []
        grids = Group()
        print('Loading Surfaces and Gridlines...')
        i = 65
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
        new_point_coords = surf_func(*starting_coords)
        s2.move_to(new_point_coords)
        self.add(surfaces[0])
        self.add(grids[0])
        self.add(s2)
        self.frame.reorient(-179, 7, 0, (0.1, -0.43, 1.36), 0.48)
        self.wait()
        self.play(self.frame.animate.reorient(-180, 24, 0, (0.05, 0.3, 0.97), 5.17), run_time=12)
        self.wait(5)
        self.embed()