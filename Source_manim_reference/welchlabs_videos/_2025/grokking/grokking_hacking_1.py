from manimlib import *
from functools import partial
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#00a14b'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
CYAN = '#00FFFF'
MAGENTA = '#FF00FF'
data_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/grokking/from_linux/grokking/grok_1764101670/'
resolution = 113
alphas_1 = np.linspace(0, 1, resolution)

def param_surface(u, v, surf_array, scale=0.15):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = scale * surf_array[v_idx, u_idx]
    except IndexError:
        z = 0
    return np.array([u, v, z])

class GrokkingHackingOne(InteractiveScene):

    def construct(self):
        mlp_hook_pre = np.load(data_dir + 'mlp_hook_pre.npy')
        neuron_idx = 453
        surf_func = partial(param_surface, surf_array=mlp_hook_pre[:, :, 2, neuron_idx], scale=0.15)
        surface = ParametricSurface(surf_func, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, data_dir + 'activations_' + str(neuron_idx).zfill(3) + '.png')
        ts.set_shading(0.0, 0.1, 0)
        mlp_hook_post = np.load(data_dir + 'hook_mlp_out.npy')
        neuron_idx = 0
        surf_func = partial(param_surface, surf_array=mlp_hook_post[:, :, 2, neuron_idx], scale=0.01)
        surface = ParametricSurface(surf_func, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, data_dir + 'activations_post_' + str(neuron_idx).zfill(3) + '.png')
        ts.set_shading(0.0, 0.1, 0)
        logits = np.load(data_dir + 'logits.npy')
        logit_index = 2
        surf_func = partial(param_surface, surf_array=logits[:, :, logit_index], scale=0.001)
        surface = ParametricSurface(surf_func, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, data_dir + 'logit_' + str(logit_index) + '.png')
        ts.set_shading(0.0, 0.1, 0)
        probe_1 = np.load(data_dir + 'probe_1.npy')
        probe_2 = np.load(data_dir + 'probe_2.npy')
        axis_1 = Axes(x_range=[0, 1.0, 1], y_range=[-1.0, 1.0, 1], width=3, height=1, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 3, 'tip_config': {'width': 0.02, 'length': 0.02}})
        probe_1a_pts = [axis_1.c2p(i / len(probe_1), probe_1[i, 0]) for i in range(len(probe_1))]
        probe_1a_line = VMobject(stroke_width=3)
        probe_1a_line.set_points_smoothly(probe_1a_pts)
        probe_1a_line.set_color(CYAN)
        probe_1b_pts = [axis_1.c2p(i / len(probe_1), probe_1[i, 1]) for i in range(len(probe_1))]
        probe_1b_line = VMobject(stroke_width=3)
        probe_1b_line.set_points_smoothly(probe_1b_pts)
        probe_1b_line.set_color(RED)
        self.add(axis_1)
        self.add(probe_1a_line, probe_1b_line)
        probe_2a_pts = [axis_1.c2p(i / len(probe_2), probe_2[i, 0]) for i in range(len(probe_2))]
        probe_2a_line = VMobject(stroke_width=3)
        probe_2a_line.set_points_smoothly(probe_2a_pts)
        probe_2a_line.set_color(YELLOW)
        probe_2b_pts = [axis_1.c2p(i / len(probe_2), probe_2[i, 1]) for i in range(len(probe_2))]
        probe_2b_line = VMobject(stroke_width=3)
        probe_2b_line.set_points_smoothly(probe_2b_pts)
        probe_2b_line.set_color(MAGENTA)
        self.add(axis_1)
        self.add(probe_2a_line, probe_2b_line)
        self.wait()
        self.embed()
        self.wait(20)
        self.embed()