from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
from functools import partial
from tqdm import tqdm
import glob
import matplotlib.pyplot as plt
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
MAX_RENDERS = 100
data_dir = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backpropagation/poster/gpu_renders_4/'
alphas_1 = np.linspace(-2.5, 2.5, 512)

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

def param_surface_3(u, v, surf_array, scaling=0.07, surf_mean=0):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = scaling * (surf_array[v_idx, u_idx] - surf_mean)
    except IndexError:
        z = 0
    return np.array([u, v, z])

def get_pivot_and_scale(axis_min, axis_max, axis_end):
    scale = axis_end / (axis_max - axis_min)
    return (axis_min, scale)

class PosterHackinEight(InteractiveScene):

    def construct(self):
        loss_arrays = []
        paths = []
        texture_paths = []
        print('Loading Surface Arrays...')
        render_paths = glob.glob(data_dir + '*')
        for r in render_paths:
            for np_path in glob.glob(r + '/*.npy'):
                loss_arrays.append(np.load(np_path))
                print(np_path, loss_arrays[-1].shape)
                paths.append(np_path)
                plt.clf()
                plt.figure(frameon=False)
                ax = plt.Axes(plt.gcf(), [0.0, 0.0, 1.0, 1.0])
                ax.set_axis_off()
                plt.gcf().add_axes(ax)
                plt.imshow(np.rot90(loss_arrays[-1].T))
                texture_paths.append(r + '/' + np_path.split('/')[-1].split('.')[0] + '_texture.png')
                plt.savefig(texture_paths[-1], bbox_inches='tight', pad_inches=0, dpi=300)
                plt.close()
        self.wait()
        surfaces = Group()
        surf_functions = []
        grids = Group()
        texts = Group()
        print('Loading Surfaces and Gridlines...')
        for i in tqdm(range(len(paths[:MAX_RENDERS]))):
            if 'llama' in paths[i]:
                scaling = 0.07
            elif 'gpt' in paths[i]:
                scaling = 0.2
            elif 'qwen' in paths[i]:
                scaling = 0.07
            elif 'gemma' in paths[i]:
                scaling = 0.07
            else:
                scaling = 0.07
            surf_func = partial(param_surface_3, surf_array=loss_arrays[i], scaling=scaling, surf_mean=np.mean(loss_arrays[i]))
            surf_functions.append(surf_func)
            surface = ParametricSurface(surf_func, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
            ts2 = TexturedSurface(surface, texture_paths[i])
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
            t = Text(paths[i][-40:])
            t.scale(0.4)
            t.rotate(DEGREES * 180)
            t.move_to([0, 3, 0])
            texts.add(t)
        self.frame.reorient(137, 41, 0, (0.48, 0.32, -0.52), 6.81)
        self.add(surfaces[0])
        self.add(grids[0])
        self.wait()
        for i in range(1, np.min([len(paths), MAX_RENDERS])):
            self.remove(surfaces[i - 1])
            self.remove(grids[i - 1])
            self.remove(texts[i - 1])
            self.add(surfaces[i])
            self.add(grids[i])
            self.wait()
        self.wait()
        self.embed()

class SingleTest(InteractiveScene):

    def construct(self):
        loss_arrays = []
        paths = []
        texture_paths = []
        print('Loading Surface Arrays...')
        render_paths = glob.glob(data_dir + '*')
        for r in render_paths:
            for np_path in glob.glob(r + '/*.npy'):
                loss_arrays.append(np.load(np_path))
                print(np_path, loss_arrays[-1].shape)
                paths.append(np_path)
                plt.clf()
                plt.figure(frameon=False)
                ax = plt.Axes(plt.gcf(), [0.0, 0.0, 1.0, 1.0])
                ax.set_axis_off()
                plt.gcf().add_axes(ax)
                plt.imshow(np.rot90(loss_arrays[-1].T))
                texture_paths.append(r + '/' + np_path.split('/')[-1].split('.')[0] + '_texture.png')
                plt.savefig(texture_paths[-1], bbox_inches='tight', pad_inches=0, dpi=300)
                plt.close()
        self.wait()
        surfaces = Group()
        surf_functions = []
        grids = Group()
        texts = Group()
        print('Loading Surfaces and Gridlines...')
        i = -1
        print(paths[i])
        scaling = 0.07
        if 'llama' in paths[i]:
            scaling = 0.07
        if 'gpt' in paths[i]:
            scaling = 0.2
        if 'gpt' in paths[i] and 'may_7_1' in paths[i]:
            scaling = 0.02
        if 'qwen' in paths[i]:
            scaling = 0.07
        if 'gemma' in paths[i]:
            scaling = 0.07
        surf_func = partial(param_surface_3, surf_array=loss_arrays[i], scaling=scaling, surf_mean=np.mean(loss_arrays[i]))
        surf_functions.append(surf_func)
        surface = ParametricSurface(surf_func, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
        ts2 = TexturedSurface(surface, texture_paths[i])
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
        t = Text(paths[i][-40:])
        t.scale(0.4)
        t.rotate(DEGREES * 180)
        t.move_to([0, 3, 0])
        texts.add(t)
        self.frame.reorient(137, 41, 0, (0.48, 0.32, -0.52), 6.81)
        self.add(surfaces[0])
        self.add(grids[0])
        self.add(texts[0])
        self.wait()
        self.wait()
        self.embed()

class PosterHackinExploreColormapsTwo(InteractiveScene):

    def construct(self):
        for cmap in ['viridis_r', 'plasma_r', 'inferno_r', 'magma_r', 'jet_r', 'gist_earth_r', 'terrain_r', 'turbo_r', 'hsv_r', 'Greens_r', 'Oranges_r', 'Reds_r', 'Blues_r', 'Purples_r', 'cool_r', 'nipy_spectral_r', 'seismic_r', 'rainbow_r', 'gist_rainbow_r']:
            loss_arrays = []
            paths = []
            texture_paths = []
            print('Loading Surface Arrays...')
            render_paths = glob.glob(data_dir + '*')
            for r in render_paths:
                for np_path in glob.glob(r + '/*.npy'):
                    loss_arrays.append(np.load(np_path))
                    print(np_path, loss_arrays[-1].shape)
                    paths.append(np_path)
                    plt.clf()
                    plt.figure(frameon=False)
                    ax = plt.Axes(plt.gcf(), [0.0, 0.0, 1.0, 1.0])
                    ax.set_axis_off()
                    plt.gcf().add_axes(ax)
                    plt.imshow(np.rot90(loss_arrays[-1].T), cmap=cmap)
                    texture_paths.append(r + '/' + np_path.split('/')[-1].split('.')[0] + '_' + cmap + '_texture.png')
                    plt.savefig(texture_paths[-1], bbox_inches='tight', pad_inches=0, dpi=300)
                    plt.close()
            self.wait()
            surfaces = Group()
            surf_functions = []
            grids = Group()
            texts = Group()
            print('Loading Surfaces and Gridlines...')
            for i in tqdm(range(len(paths[:MAX_RENDERS]))):
                if 'llama' in paths[i]:
                    scaling = 0.07
                elif 'gpt' in paths[i]:
                    scaling = 0.2
                elif 'qwen' in paths[i]:
                    scaling = 0.07
                elif 'gemma' in paths[i]:
                    scaling = 0.07
                else:
                    scaling = 0.07
                surf_func = partial(param_surface_3, surf_array=loss_arrays[i], scaling=scaling, surf_mean=np.mean(loss_arrays[i]))
                surf_functions.append(surf_func)
                surface = ParametricSurface(surf_func, u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(512, 512))
                ts2 = TexturedSurface(surface, texture_paths[i])
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
                t = Text(paths[i][-40:])
                t.scale(0.4)
                t.rotate(DEGREES * 180)
                t.move_to([0, 3, 0])
                texts.add(t)
            self.frame.reorient(132, 30, 0, (0.24, 0.27, -0.23), 7.5)
            self.add(surfaces[0])
            self.add(grids[0])
            self.add(texts[0])
            self.wait()
            for i in range(1, np.min([len(paths), MAX_RENDERS])):
                self.remove(surfaces[i - 1])
                self.remove(grids[i - 1])
                self.remove(texts[i - 1])
                self.add(surfaces[i])
                self.add(grids[i])
                self.add(texts[i])
                self.wait()
            self.remove(surfaces[i])
            self.remove(grids[i])
            self.remove(texts[i])
        self.embed()