from manimlib import *
from functools import partial
from pathlib import Path
import matplotlib.cm as cm
import matplotlib.colors as colors
from tqdm import tqdm
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
resolution = 113
svg_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/grokking/graphics/to_manim')
data_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/grokking/from_linux/grok_1764706121')

def viridis_hex(value, vmin, vmax):
    norm = colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    rgba = cm.viridis(norm(value))
    return colors.to_hex(rgba)

def black_to_tan_hex(value, vmin, vmax=1):
    cmap = colors.LinearSegmentedColormap.from_list('black_tan', ['#000000', '#dfd0b9'])
    norm = colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    return colors.to_hex(cmap(norm(value)))

def softmax_with_temperature(logits, temperature=1.0, axis=-1):
    scaled = logits / temperature
    exp_scaled = np.exp(scaled - np.max(scaled, axis=axis, keepdims=True))
    return exp_scaled / np.sum(exp_scaled, axis=axis, keepdims=True)

def draw_inputs(self, activations, all_svgs, reset=False, example_index=0, wait=0.0):
    input_mapping_1a = [[0, 1], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18]]
    input_mapping_1b = [[19, 20], [21, 22]]
    input_mapping_2a = [[23, 24], [28, 29], [30, 31], [32, 33], [34, 35], [36, 37], [38, 39], [40, 41]]
    input_mapping_2b = [[42, 43], [44, 45]]
    input_mapping_3a = [[46, 47], [51, 52], [53, 54], [55, 56], [57, 58], [59, 60], [61, 62], [63, 64]]
    input_mapping_3b = [[65, 66], [67, 68]]
    for mapping, activations_index, offset in zip([input_mapping_1a, input_mapping_1b, input_mapping_2a, input_mapping_2b, input_mapping_3a, input_mapping_3b], [0, 0, 1, 1, 2, 2], [0, 112, 0, 112, 0, 112]):
        for i, idx in enumerate(mapping):
            if i + offset == activations['x'][example_index][activations_index]:
                all_svgs[2][idx[0]].set_color(FRESH_TAN)
            else:
                all_svgs[2][idx[0]].set_color(BLACK)
            if reset:
                all_svgs[2][idx[0]].set_color(BLACK)
        if wait != 0.0:
            self.wait(wait)

def draw_embeddings(self, activations, all_svgs, reset=False, example_index=0, wait=0, colormap=black_to_tan_hex):
    embedding_fill_indices_1 = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
    embedding_fill_indices_2 = [28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48]
    embedding_fill_indices_3 = [53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73]
    for i, indices in enumerate([embedding_fill_indices_1, embedding_fill_indices_2, embedding_fill_indices_3]):
        vmin = np.min(activations['blocks.0.hook_resid_pre'][example_index][i]) * 1.5
        vmax = np.max(activations['blocks.0.hook_resid_pre'][example_index][i]) * 1.5
        for j, idx in enumerate(indices):
            c = colormap(activations['blocks.0.hook_resid_pre'][example_index, i, j], vmin, vmax)
            all_svgs[4][idx].set_color(c)
            if reset:
                all_svgs[4][idx].set_color(BLACK)
            if wait != 0.0:
                self.wait(wait)

def draw_embeddings_2(self, activations, all_svgs, reset=False, example_index=0, wait=0, colormap=black_to_tan_hex):
    embedding_fill_indices_1 = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
    embedding_fill_indices_2 = [28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48]
    embedding_fill_indices_3 = [53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73]
    for i, indices in enumerate([embedding_fill_indices_1, embedding_fill_indices_2, embedding_fill_indices_3]):
        vmin = np.min(activations['blocks.0.hook_resid_pre'][example_index][i]) * 0.8
        vmax = np.max(activations['blocks.0.hook_resid_pre'][example_index][i]) * 0.8
        for j, idx in enumerate(indices):
            c = colormap(activations['blocks.0.hook_resid_pre'][example_index, i, j], vmin, vmax)
            all_svgs[4][idx].set_color(c)
            if reset:
                all_svgs[4][idx].set_color(BLACK)
            if wait != 0.0:
                self.wait(wait)

def draw_attention_values(self, activations, all_svgs, reset=False, example_index=0, wait=0, colormap=black_to_tan_hex):
    vmin = np.min(activations['blocks.0.attn.hook_v'][example_index]) * 0.25
    vmax = np.max(activations['blocks.0.attn.hook_v'][example_index]) * 0.25
    value_fill_indices_1 = [0, 2, 4, 6, 8]
    value_fill_indices_2 = [10, 12, 14, 16, 18]
    value_fill_indices_3 = [20, 22, 24, 26, 28]
    value_fill_indices_4 = [30, 32, 34, 36, 38]
    for head_id, indices in enumerate([value_fill_indices_1, value_fill_indices_2, value_fill_indices_3, value_fill_indices_4]):
        for j, idx in enumerate(indices):
            c = colormap(activations['blocks.0.attn.hook_v'][example_index, head_id, 1, j], vmin, vmax)
            all_svgs[12][idx].set_color(c)
            if reset:
                all_svgs[4][idx].set_color(BLACK)
            if wait != 0.0:
                self.wait(wait)

def draw_attention_patterns(self, activations, all_svgs, reset=False, example_index=0, wait=0, colormap=black_to_tan_hex):
    vmin = 0
    vmax = 0.8
    attn_fill_indices = [[0, 0], [1, 0], [1, 1], [2, 0], [2, 1], [2, 2]]
    head_id = 0
    for head_id, offset in enumerate([0, 6, 12, 18]):
        for j, idx in enumerate(attn_fill_indices):
            a = activations['blocks.0.attn.hook_attn'][example_index, head_id, idx[0], idx[1]]
            c = black_to_tan_hex(a, vmin, vmax)
            all_svgs[13][offset + j].set_color(c)
            if reset:
                all_svgs[13][offset + j].set_color(BLACK)
            self.remove(all_svgs[7])
            self.add(all_svgs[7])
            if wait != 0.0:
                self.wait(wait)

def draw_mlp_1(self, activations, all_svgs, reset=False, example_index=0, wait=0, colormap=black_to_tan_hex):
    vmin = np.min(activations['blocks.0.hook_resid_mid'][example_index]) * 0.85
    vmax = np.max(activations['blocks.0.hook_resid_mid'][example_index]) * 0.85
    mlp_indices_1 = [0, 2, 4, 6, 8, 10, 12]
    for i, idx in enumerate(mlp_indices_1):
        c = black_to_tan_hex(activations['blocks.0.hook_resid_mid'][example_index, 2, i], vmin, vmax)
        all_svgs[9][idx].set_color(c)
        if reset:
            all_svgs[9][idx].set_color(BLACK)
        if wait != 0.0:
            self.wait(wait)

def draw_mlp_2(self, activations, all_svgs, reset=False, example_index=0, wait=0, colormap=black_to_tan_hex):
    vmin = np.min(activations['blocks.0.mlp.hook_pre'][example_index]) * 0.85
    vmax = np.max(activations['blocks.0.mlp.hook_pre'][example_index]) * 0.85
    mlp_indices_2 = [14, 16, 18, 20, 22, 24, 26, 28, 30]
    for i, idx in enumerate(mlp_indices_2):
        c = black_to_tan_hex(activations['blocks.0.mlp.hook_pre'][example_index, 2, i], vmin, vmax)
        all_svgs[9][idx].set_color(c)
        if reset:
            all_svgs[9][idx].set_color(BLACK)
        if wait != 0.0:
            self.wait(wait)

def draw_mlp_3(self, activations, all_svgs, reset=False, example_index=0, wait=0, colormap=black_to_tan_hex):
    vmin = np.min(activations['blocks.0.hook_mlp_out'][example_index]) * 0.85
    vmax = np.max(activations['blocks.0.hook_mlp_out'][example_index]) * 0.85
    mlp_indices_3 = [32, 34, 36, 38, 40, 42, 44]
    for i, idx in enumerate(mlp_indices_3):
        c = black_to_tan_hex(activations['blocks.0.hook_mlp_out'][example_index, 2, i], vmin, vmax)
        all_svgs[9][idx].set_color(c)
        if reset:
            all_svgs[9][idx].set_color(BLACK)
        if wait != 0.0:
            self.wait(wait)

def draw_logits(self, activations, all_svgs, reset=False, example_index=0, wait=0, colormap=black_to_tan_hex, temperature=25.0):
    logit_indices_1 = [3, 5, 7, 9, 11, 13, 15, 17]
    logit_indices_2 = [19, 21]
    probs_sortof = softmax_with_temperature(activations['logits'][example_index], temperature=temperature, axis=0)
    vmin = np.min(probs_sortof) * 1.0
    vmax = np.max(probs_sortof) * 1.0
    for i, idx in enumerate(logit_indices_1):
        c = black_to_tan_hex(probs_sortof[i], vmin, vmax)
        all_svgs[11][idx].set_color(c)
        if reset:
            all_svgs[11][idx].set_color(BLACK)
        if wait != 0.0:
            self.wait(wait)
    for i, idx in enumerate(logit_indices_2):
        c = black_to_tan_hex(probs_sortof[i + 111], vmin, vmax)
        all_svgs[11][idx].set_color(c)
        if reset:
            all_svgs[11][idx].set_color(BLACK)
        if wait != 0.0:
            self.wait(wait)
alphas_1 = np.linspace(0, 1, resolution)

def param_surface(u, v, surf_array, scale=0.15):
    u_idx = np.abs(alphas_1 - u).argmin()
    v_idx = np.abs(alphas_1 - v).argmin()
    try:
        z = scale * surf_array[v_idx, u_idx]
    except IndexError:
        z = 0
    return np.array([u, v, z])

def surf_func(u, v, axes, surf_array, scale=1.0):
    i = int(u * (surf_array.shape[0] - 1))
    j = int(v * (surf_array.shape[1] - 1))
    x = u * 113
    y = v * 113
    z = surf_array[i, j] * scale
    return axes.c2p(x, y, z)

class Dot3D(Sphere):

    def __init__(self, center=ORIGIN, radius=0.05, **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.move_to(center)

def make_fourier_surf_func(axes, comp_func):

    def func(u, v):
        i = u * 113
        j = v * 113
        x = i
        y = j
        z = comp_func(i, j)
        return axes.c2p(x, y, z)
    return func

class P44_58b(InteractiveScene):

    def construct(self):
        p = 113
        svg_files = list(sorted(svg_dir.glob('*network_to_manim*')))
        with open(data_dir / 'final_model_activations.p', 'rb') as f:
            activations = pickle.load(f)
        all_svgs = Group()
        for svg_file in svg_files[1:28]:
            svg_image = SVGMobject(str(svg_file))
            all_svgs.add(svg_image[1:])
        all_svgs.scale(6.0)
        example_index = 0
        self.frame.reorient(0, 0, 0, (0, 0, 0), 8.0)
        draw_inputs(self, activations, all_svgs, reset=False, example_index=example_index, wait=0)
        draw_embeddings(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        draw_attention_values(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_attention_patterns(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_1(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_2(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_3(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_logits(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex, temperature=25.0)
        self.add(all_svgs[:15], all_svgs[16])
        self.remove(all_svgs[7])
        self.add(all_svgs[7])
        axis_1 = Axes(x_range=[0, 1.0, 1], y_range=[-1.0, 1.0, 1], width=2 * 2.4, height=2 * 0.56, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 1.8, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axis_2 = Axes(x_range=[0, 1.0, 1], y_range=[-1.0, 1.0, 1], width=2 * 2.4, height=2 * 0.56, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 1.8, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axis_1.move_to([-4, 3.05, 0])
        x_label = Tex('x', font_size=24)
        x_label.set_color(CHILL_BROWN)
        x_label.next_to(axis_1, RIGHT, buff=0.1)
        x_label.shift([0, -0.1, 0])
        axis_2.move_to([-4, -2.85, 0])
        y_label = Tex('y', font_size=24)
        y_label.set_color(CHILL_BROWN)
        y_label.next_to(axis_2, RIGHT, buff=0.1)
        y_label.shift([0, -0.1, 0])
        sparse_probe_1 = np.load(data_dir / 'sparse_probe_1.npy')
        sparse_probe_2 = np.load(data_dir / 'sparse_probe_2.npy')
        sparse_probe_3 = np.load(data_dir / 'sparse_probe_3.npy')
        sparse_probe_4 = np.load(data_dir / 'sparse_probe_4.npy')
        pts_curve_1 = []
        for j in range(p):
            x = j / p
            y = sparse_probe_1[j]
            pts_curve_1.append(axis_1.c2p(x, y))
        curve_1 = VMobject(stroke_width=3)
        curve_1.set_points_smoothly(pts_curve_1)
        curve_1.set_color(YELLOW)
        pts_curve_2 = []
        for j in range(p):
            x = j / p
            y = sparse_probe_2[j]
            pts_curve_2.append(axis_1.c2p(x, y))
        curve_2 = VMobject(stroke_width=3)
        curve_2.set_points_smoothly(pts_curve_2)
        curve_2.set_color(MAGENTA)
        pts_curve_3 = []
        for j in range(p):
            x = j / p
            y = sparse_probe_3[j]
            pts_curve_3.append(axis_2.c2p(x, y))
        curve_3 = VMobject(stroke_width=3)
        curve_3.set_points_smoothly(pts_curve_3)
        curve_3.set_color(CYAN)
        pts_curve_4 = []
        for j in range(p):
            x = j / p
            y = sparse_probe_4[j]
            pts_curve_4.append(axis_2.c2p(x, y))
        curve_4 = VMobject(stroke_width=3)
        curve_4.set_points_smoothly(pts_curve_4)
        curve_4.set_color(RED)
        wave_label_1 = Tex('\\cos \\big(\\tfrac{8\\pi}{113}x\\big)')
        wave_label_1.set_color(YELLOW)
        wave_label_1.scale(0.45 * 1.5)
        wave_label_1.move_to([-0.85, 3.5, 0])
        wave_label_2 = Tex('\\sin \\big(\\tfrac{8\\pi}{113}x\\big)')
        wave_label_2.set_color(MAGENTA)
        wave_label_2.scale(0.45 * 1.5)
        wave_label_2.move_to([-0.9, 2.5, 0])
        wave_label_3 = Tex('\\cos \\big(\\tfrac{8\\pi}{113}y\\big)')
        wave_label_3.set_color(CYAN)
        wave_label_3.scale(0.45 * 1.5)
        wave_label_3.move_to([-0.9, -2.5, 0])
        wave_label_4 = Tex('\\sin \\big(\\tfrac{8\\pi}{113}y\\big)')
        wave_label_4.set_color(RED)
        wave_label_4.scale(0.45 * 1.5)
        wave_label_4.move_to([-0.9, -3.6, 0])
        self.add(all_svgs[18])
        self.add(axis_1, axis_2, x_label, y_label)
        self.add(curve_1, curve_2, curve_3, curve_4)
        self.add(wave_label_1, wave_label_2, wave_label_3, wave_label_4)
        self.remove(all_svgs[7])
        self.add(all_svgs[7])
        self.remove(all_svgs[9])
        self.add(all_svgs[9])
        probe_group_1 = Group(axis_2, curve_3, curve_4, y_label)
        probe_group_1.shift([0, -0.3, 0])
        probe_group_2 = Group(axis_1, curve_1, curve_2, x_label)
        probe_group_2.shift([0, -0.15, 0])
        self.wait()
        mid_mlp_fade_group = Group(all_svgs[14][9], all_svgs[14][:3], all_svgs[10], all_svgs[11], all_svgs[0][7:14], all_svgs[0][-1], all_svgs[8][-105:], all_svgs[9][-14:], all_svgs[14][-20:])
        self.wait()
        self.play(FadeOut(mid_mlp_fade_group), self.frame.animate.reorient(0, 0, 0, (2.37, -0.07, 0.09), 10.33), run_time=4)
        self.wait()
        self.play(Write(all_svgs[25]))
        self.wait()
        magic_indices = np.arange(0, len(activations['x']), 113)
        for i in magic_indices:
            draw_inputs(self, activations, all_svgs, reset=False, example_index=i, wait=0)
            draw_embeddings(self, activations, all_svgs, reset=False, example_index=i, wait=0, colormap=black_to_tan_hex)
            draw_attention_values(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
            draw_attention_patterns(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
            draw_mlp_1(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
            draw_mlp_2(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
            self.wait(0.2)
        self.wait()
        for i in range(113):
            draw_inputs(self, activations, all_svgs, reset=False, example_index=i, wait=0)
            draw_embeddings(self, activations, all_svgs, reset=False, example_index=i, wait=0, colormap=black_to_tan_hex)
            draw_attention_values(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
            draw_attention_patterns(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
            draw_mlp_1(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
            draw_mlp_2(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
            self.wait(0.2)
        self.wait()
        self.wait()
        self.wait()
        self.remove(all_svgs[18], all_svgs[25])
        self.play(FadeIn(all_svgs[8][-105:]), FadeIn(all_svgs[9][-14:]), FadeIn(all_svgs[14][:9]), FadeIn(all_svgs[14][10:]), probe_group_1.animate.move_to([-6.7, -3.05, 0]), wave_label_3.animate.scale(1.2).move_to([-7.8, -4.1, 0]), wave_label_4.animate.scale(1.2).move_to([-5.7, -4.1, 0]), probe_group_2.animate.move_to([-6.7, 3.3, 0]), wave_label_2.animate.scale(1.2).move_to([-5.7, 2.3, 0]), wave_label_1.animate.scale(1.2).move_to([-7.8, 2.3, 0]), self.frame.animate.reorient(0, 0, 0, (1.46, 0.11, 0.2), 12.32), FadeIn(all_svgs[22][:2]), FadeIn(all_svgs[22][4:6]), run_time=6)
        self.add(all_svgs[21])
        self.remove(all_svgs[9])
        self.add(all_svgs[9])
        self.remove(all_svgs[22][:2])
        self.add(all_svgs[22][:2])
        self.wait()
        self.play(Write(all_svgs[26]))
        self.wait()
        self.play(Write(all_svgs[22][2]), Write(all_svgs[22][6:]), run_time=3)
        self.wait()
        self.wait()
        self.play(FadeOut(all_svgs[26]), FadeIn(all_svgs[14][9]), FadeIn(all_svgs[10]), FadeIn(all_svgs[11]), FadeIn(all_svgs[0][7:14]), FadeIn(all_svgs[0][-1]), FadeIn(all_svgs[23]), run_time=5)
        self.remove(all_svgs[9])
        self.add(all_svgs[9])
        self.wait()
        self.play(Write(all_svgs[24]), run_time=3)
        self.wait()
        self.wait(20)
        self.embed()

class P56a_neuron_100(InteractiveScene):

    def construct(self):
        p = 113
        mlp_out = np.load(data_dir / 'hook_mlp_out.npy')
        axes_1 = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-1, 1, 1], width=4, height=4, depth=1.4, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.05, 'length': 0.05}})
        x_label = Tex('x', font_size=32).next_to(axes_1.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
        y_label = Tex('y', font_size=32).next_to(axes_1.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
        axes_1_group = VGroup(axes_1, x_label, y_label)
        x_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [0, 0, 1])
        axes_1[0].rotate(DEGREES * 90, [1, 0, 0])
        axes_1[1].rotate(DEGREES * 90, [0, 1, 0])
        neuron_idx_1 = 100
        neuron_1_mean = np.mean(mlp_out[:, :, 2, neuron_idx_1])
        neuron_1_max = np.max(np.abs(mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean))
        surf_func_with_axes = partial(surf_func, axes=axes_1, surf_array=0.75 * (mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean) / neuron_1_max, scale=1.0)
        surface = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, str(data_dir / ('activations_post_' + str(neuron_idx_1).zfill(3) + '.png')))
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.8)
        self.frame.reorient(43, 57, 0, (-0.15, -0.07, -0.33), 6.6)
        self.wait()
        self.play(ShowCreation(axes_1), ShowCreation(x_label), ShowCreation(y_label), run_time=5)
        self.wait()
        self.play(ShowCreation(ts), run_time=5)
        self.wait()
        self.wait(20)
        self.embed()

class P56a_neuron_101(InteractiveScene):

    def construct(self):
        p = 113
        mlp_out = np.load(data_dir / 'hook_mlp_out.npy')
        axes_1 = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-1, 1, 1], width=4, height=4, depth=1.4, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.05, 'length': 0.05}})
        x_label = Tex('x', font_size=32).next_to(axes_1.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
        y_label = Tex('y', font_size=32).next_to(axes_1.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
        axes_1_group = VGroup(axes_1, x_label, y_label)
        x_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [0, 0, 1])
        axes_1[0].rotate(DEGREES * 90, [1, 0, 0])
        axes_1[1].rotate(DEGREES * 90, [0, 1, 0])
        neuron_idx_1 = 101
        neuron_1_mean = np.mean(mlp_out[:, :, 2, neuron_idx_1])
        neuron_1_max = np.max(np.abs(mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean))
        surf_func_with_axes = partial(surf_func, axes=axes_1, surf_array=0.75 * (mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean) / neuron_1_max, scale=1.0)
        surface = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, str(data_dir / ('activations_post_' + str(neuron_idx_1).zfill(3) + '.png')))
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.8)
        self.frame.reorient(43, 57, 0, (-0.15, -0.07, -0.33), 6.6)
        self.wait()
        self.play(ShowCreation(axes_1), ShowCreation(x_label), ShowCreation(y_label), run_time=5)
        self.wait()
        self.play(ShowCreation(ts), run_time=5)
        self.wait()
        self.wait(20)
        self.embed()

class P56a_neuron_102(InteractiveScene):

    def construct(self):
        p = 113
        mlp_out = np.load(data_dir / 'hook_mlp_out.npy')
        axes_1 = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-1, 1, 1], width=4, height=4, depth=1.4, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.05, 'length': 0.05}})
        x_label = Tex('x', font_size=32).next_to(axes_1.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
        y_label = Tex('y', font_size=32).next_to(axes_1.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
        axes_1_group = VGroup(axes_1, x_label, y_label)
        x_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [0, 0, 1])
        axes_1[0].rotate(DEGREES * 90, [1, 0, 0])
        axes_1[1].rotate(DEGREES * 90, [0, 1, 0])
        neuron_idx_1 = 102
        neuron_1_mean = np.mean(mlp_out[:, :, 2, neuron_idx_1])
        neuron_1_max = np.max(np.abs(mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean))
        surf_func_with_axes = partial(surf_func, axes=axes_1, surf_array=0.75 * (mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean) / neuron_1_max, scale=1.0)
        surface = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, str(data_dir / ('activations_post_' + str(neuron_idx_1).zfill(3) + '.png')))
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.8)
        self.frame.reorient(43, 57, 0, (-0.15, -0.07, -0.33), 6.6)
        self.wait()
        self.play(ShowCreation(axes_1), ShowCreation(x_label), ShowCreation(y_label), run_time=5)
        self.wait()
        self.play(ShowCreation(ts), run_time=5)
        self.wait()
        self.wait(20)
        self.embed()

class P56_logits(InteractiveScene):

    def construct(self):
        logits = np.load(data_dir / 'logits.npy')
        p = 113
        axes_1 = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-1, 1, 1], width=4, height=4, depth=1.4, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.05, 'length': 0.05}})
        x_label = Tex('x', font_size=32).next_to(axes_1.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
        y_label = Tex('y', font_size=32).next_to(axes_1.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
        x_label.rotate(DEGREES * 90, [1, 0, 0])
        x_label.rotate(DEGREES * 180, [0, 0, 1])
        y_label.rotate(DEGREES * 90, [0, 0, 1])
        y_label.rotate(DEGREES * 90, [0, 1, 0])
        axes_1[0].rotate(DEGREES * 90, [1, 0, 0])
        axes_1[1].rotate(DEGREES * 90, [0, 1, 0])
        neuron_idx = 7
        neuron_1_mean = np.mean(logits[:, :, neuron_idx])
        neuron_1_max = np.max(np.abs(logits[:, :, neuron_idx] - neuron_1_mean))
        surf_func_with_axes = partial(surf_func, axes=axes_1, surf_array=(logits[:, :, neuron_idx] - neuron_1_mean) / neuron_1_max, scale=1.0)
        surface = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, str(data_dir / ('logits_' + str(neuron_idx).zfill(3) + '.png')))
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.8)
        ts_copy = ts.copy()
        axes_1_group = Group(axes_1[:2], x_label, y_label, ts)
        self.frame.reorient(43, 57, 0, (-0.15, -0.07, -0.33), 6.6)
        self.wait()
        self.play(ShowCreation(axes_1), ShowCreation(x_label), ShowCreation(y_label), run_time=5)
        self.wait()
        self.play(ShowCreation(ts), run_time=5)
        self.wait()

        def flat_surf_func(u, v, axes):
            x = u * 113
            y = v * 113
            z = 0
            return axes.c2p(x, y, z)
        flat_surf_func_with_axes = partial(flat_surf_func, axes=axes_1)
        flat_surface = ParametricSurface(flat_surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        flat_ts = TexturedSurface(flat_surface, str(data_dir / ('logits_' + str(neuron_idx).zfill(3) + '.png')))
        flat_ts.set_shading(0.0, 0.1, 0)
        flat_ts.set_opacity(0.8)
        self.wait()
        self.play(ReplacementTransform(ts, flat_ts), FadeOut(axes_1[2]), y_label.animate.rotate(-90 * DEGREES, [0, 1, 0]), x_label.animate.rotate(90 * DEGREES, [1, 0, 0]).rotate(90 * DEGREES, [0, 0, 1]), self.frame.animate.reorient(90, 0, 0, (-0.03, -0.11, -0.33), 5.73), run_time=9)
        self.wait()
        self.wait()
        self.play(self.frame.animate.reorient(90, 0, 0, (-1.82, -1.77, -0.33), 0.88), run_time=5)
        self.wait()
        self.play(ReplacementTransform(flat_ts, ts_copy), y_label.animate.rotate(90 * DEGREES, [0, 1, 0]), x_label.animate.rotate(90 * DEGREES, [0, 0, 1]).rotate(-90 * DEGREES, [1, 0, 0]).rotate(180 * DEGREES, [0, 0, 1]), self.frame.animate.reorient(43, 57, 0, (-0.15, -0.07, -0.33), 6.6), run_time=9)
        self.wait()
        self.wait(20)
        self.embed()

class P52_54_3Df(InteractiveScene):

    def construct(self):
        mlp_hook_pre = np.load(data_dir / 'mlp_hook_pre.npy')
        p = 113
        axes_1 = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-1, 1, 1], width=4, height=4, depth=1.4, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.05, 'length': 0.05}})
        axes_2 = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-1, 1, 1], width=4, height=4, depth=1.4, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.05, 'length': 0.05}})
        x_label = Tex('x', font_size=32).next_to(axes_1.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
        y_label = Tex('y', font_size=32).next_to(axes_1.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
        x_label.rotate(DEGREES * 90, [1, 0, 0])
        x_label.rotate(DEGREES * 180, [0, 0, 1])
        y_label.rotate(DEGREES * 90, [0, 0, 1])
        y_label.rotate(DEGREES * 90, [0, 1, 0])
        axes_1[0].rotate(DEGREES * 90, [1, 0, 0])
        axes_1[1].rotate(DEGREES * 90, [0, 1, 0])
        x_label_2 = Tex('x', font_size=32).next_to(axes_2.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
        y_label_2 = Tex('y', font_size=32).next_to(axes_2.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
        x_label_2.rotate(DEGREES * 90, [1, 0, 0])
        x_label_2.rotate(DEGREES * 180, [0, 0, 1])
        y_label_2.rotate(DEGREES * 90, [0, 0, 1])
        y_label_2.rotate(DEGREES * 90, [0, 1, 0])
        axes_2[0].rotate(DEGREES * 90, [1, 0, 0])
        axes_2[1].rotate(DEGREES * 90, [0, 1, 0])
        neuron_idx_1 = 106
        neuron_1_mean = np.mean(mlp_hook_pre[:, :, 2, neuron_idx_1]) - 0.2
        surf_func_with_axes = partial(surf_func, axes=axes_1, surf_array=mlp_hook_pre[:, :, 2, neuron_idx_1] - neuron_1_mean, scale=1.0)
        surface = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, str(data_dir / ('activations_' + str(neuron_idx_1).zfill(3) + '.png')))
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.8)
        surf_1_component_eq = lambda i, j: 0.354 * np.cos(2 * np.pi * (4 * i / 113) - 0.516) * np.cos(2 * np.pi * (4 * j / 113) - 0.516)
        surf_1_component = ParametricSurface(make_fourier_surf_func(axes_1, surf_1_component_eq), u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        surf_1_component.set_color(ORANGE).set_shading(0.1, 0.5, 0.5)
        axes_1_group = Group(axes_1[:2], x_label, y_label, ts, surf_1_component)
        axes_1_group.rotate(3 * DEGREES, [-1, -1, 0])
        neuron_idx_2 = 341
        nueron_2_mean = np.mean(mlp_hook_pre[:, :, 2, neuron_idx_2])
        surf_func_with_axes = partial(surf_func, axes=axes_2, surf_array=mlp_hook_pre[:, :, 2, neuron_idx_2] - nueron_2_mean, scale=1.0)
        surface_2 = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts2 = TexturedSurface(surface_2, str(data_dir / ('activations_' + str(neuron_idx_2).zfill(3) + '.png')))
        ts2.set_shading(0.0, 0.1, 0)
        surf_2_component_eq = lambda i, j: 2 * 0.211 * np.cos(2 * np.pi * (4 * i / 113) + 1.068) * np.cos(2 * np.pi * (4 * j / 113) + 1.068)
        surf_2_component = ParametricSurface(make_fourier_surf_func(axes_2, surf_2_component_eq), u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        surf_2_component.set_color('#00AAAA').set_shading(0.1, 0.5, 0.5)
        surf_2_component_eq_flipped = lambda i, j: -2.4 * 0.211 * np.cos(2 * np.pi * (4 * i / 113) + 1.068) * np.cos(2 * np.pi * (4 * j / 113) + 1.068)
        surf_2_component_flipped = ParametricSurface(make_fourier_surf_func(axes_2, surf_2_component_eq_flipped), u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        surf_2_component_flipped.set_color('#00AAAA').set_shading(0.1, 0.5, 0.5)
        axes_2_group = Group(axes_2[:2], x_label_2, y_label_2, ts2, surf_2_component, surf_2_component_flipped)
        axes_2_group.move_to([1.7, -1.7, -17.5])
        axes_2_group.rotate(25 * DEGREES, [1, -1, 0])
        axes_2_group.rotate(7 * DEGREES, [-1, -1, 0])
        axes_2_group.scale(1.7)
        self.frame.reorient(132, 45, 0, (-0.72, 5.18, -3.92), 14.3)
        self.add(axes_1_group[:4])
        self.wait()
        self.play(ShowCreation(axes_2_group[:3]), run_time=4)
        self.play(ShowCreation(axes_2_group[3]), run_time=4)
        self.wait()
        ha = -1.2
        self.wait()
        self.add(surf_1_component)
        self.play(surf_1_component.animate.move_to([-7.0 - ha, 7.0 + ha, 0]).rotate(5 * DEGREES, [1, -1, 0]).rotate(5 * DEGREES, [1, 1, 0]).rotate(-10 * DEGREES, [0, 0, 1]), rate_func=linear, run_time=4)
        self.wait()
        self.wait()
        surf_2_component.shift([0, 0, -0.42])
        self.add(surf_2_component)
        self.play(surf_2_component.animate.move_to([-7.2 - ha, 7.2 + ha, -2.5]).scale(1 / 1.7).rotate(-20 * DEGREES, [1, -1, 0]).rotate(5 * DEGREES, [1, 1, 0]).rotate(-10 * DEGREES, [0, 0, 1]), rate_func=linear, run_time=4)
        surf_2_component_flipped.move_to([-7.2 - ha, 7.2 + ha, -2.5]).scale(1 / 1.7).rotate(-20 * DEGREES, [1, -1, 0]).rotate(5 * DEGREES, [1, 1, 0]).rotate(-10 * DEGREES, [0, 0, 1])
        self.wait()
        self.play(ReplacementTransform(surf_2_component, surf_2_component_flipped), run_time=4)
        self.wait()
        combined_surf_eq = lambda i, j: 0.354 * np.cos(2 * np.pi * (4 * i / 113) - 0.516) * np.cos(2 * np.pi * (4 * j / 113) - 0.516) + 0.354 * np.cos(2 * np.pi * (4 * i / 113) + 1.068) * np.cos(2 * np.pi * (4 * j / 113) + 1.068)
        combined_surf = ParametricSurface(make_fourier_surf_func(axes_1, combined_surf_eq), u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        combined_surf.set_color(GREEN).set_shading(0.1, 0.5, 0.5)
        combined_surf.scale(1.05)
        combined_surf.rotate(5 * DEGREES, [1, -1, 0]).rotate(5 * DEGREES, [1, 1, 0]).rotate(-10 * DEGREES, [0, 0, 1])
        combined_surf.move_to([-7.5 - ha, 7.5 + ha, -6])
        self.wait()
        self.play(ReplacementTransform(surf_1_component.copy(), combined_surf), ReplacementTransform(surf_2_component_flipped.copy(), combined_surf), run_time=6)
        self.wait()
        self.wait(20)
        self.embed()

class P49_51_3D(InteractiveScene):

    def construct(self):
        p = 113
        mlp_out = np.load(data_dir / 'hook_mlp_out.npy')
        axes_1 = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-1, 1, 1], width=4, height=4, depth=1.4, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.05, 'length': 0.05}})
        x_label = Tex('x', font_size=32).next_to(axes_1.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
        y_label = Tex('y', font_size=32).next_to(axes_1.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
        axes_1_group = VGroup(axes_1, x_label, y_label)
        x_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [0, 0, 1])
        axes_1[0].rotate(DEGREES * 90, [1, 0, 0])
        axes_1[1].rotate(DEGREES * 90, [0, 1, 0])
        neuron_idx_1 = 1
        neuron_1_mean = np.mean(mlp_out[:, :, 2, neuron_idx_1])
        neuron_1_max = np.max(np.abs(mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean))
        surf_func_with_axes = partial(surf_func, axes=axes_1, surf_array=0.75 * (mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean) / neuron_1_max, scale=1.0)
        surface = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, str(data_dir / ('activations_post_' + str(neuron_idx_1).zfill(3) + '.png')))
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.8)
        self.frame.reorient(51, 71, 0, (-0.8, -0.78, -0.3), 7.2)
        self.wait()
        self.play(ShowCreation(axes_1), ShowCreation(x_label), ShowCreation(y_label), run_time=5)
        self.wait()
        self.play(ShowCreation(ts), self.frame.animate.reorient(44, 53, 0, (-0.55, -0.54, -0.39), 7.2), run_time=5)
        self.wait()
        self.play(self.frame.animate.reorient(47, 84, 0, (-0.55, -0.54, -0.39), 7.2), run_time=3)
        self.wait()

        def flat_surf_func(u, v, axes):
            x = u * 113
            y = v * 113
            z = 0
            return axes.c2p(x, y, z)
        flat_surf_func_with_axes = partial(flat_surf_func, axes=axes_1)
        flat_surface = ParametricSurface(flat_surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        flat_ts = TexturedSurface(flat_surface, str(data_dir / ('activations_post_' + str(neuron_idx_1).zfill(3) + '.png')))
        flat_ts.set_shading(0.0, 0.1, 0)
        flat_ts.set_opacity(0.8)
        self.wait()
        self.play(ReplacementTransform(ts, flat_ts), FadeOut(axes_1[2]), y_label.animate.rotate(-90 * DEGREES, [0, 1, 0]), x_label.animate.rotate(-90 * DEGREES, [1, -0, 0]).rotate(90 * DEGREES, [0, 0, 1]), self.frame.animate.reorient(90, 0, 0, (-0.03, -0.11, -0.33), 5.73), run_time=9)
        surf_func_with_axes = partial(surf_func, axes=axes_1, surf_array=0.5 * (mlp_out[:, :, 2, neuron_idx_1] - neuron_1_mean) / neuron_1_max, scale=1.0)
        surface = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts2 = TexturedSurface(surface, str(data_dir / ('activations_post_' + str(neuron_idx_1).zfill(3) + '.png')))
        ts2.set_shading(0.0, 0.1, 0)
        ts2.set_opacity(0.8)
        self.wait()
        self.play(ReplacementTransform(flat_ts, ts2), FadeIn(axes_1[2]), y_label.animate.rotate(90 * DEGREES, [0, 1, 0]), x_label.animate.rotate(90 * DEGREES, [0, 0, 1]).rotate(90 * DEGREES, [1, 0, 0]), self.frame.animate.reorient(42, 52, 0, (-0.02, -0.06, -0.46), 7.2), run_time=6)
        self.wait()
        self.wait(20)
        self.embed()

class P45_3Db(InteractiveScene):

    def construct(self):
        mlp_hook_pre = np.load(data_dir / 'mlp_hook_pre.npy')
        p = 113
        axes_1 = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-1, 1, 1], width=4, height=4, depth=1.4, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.05, 'length': 0.05}})
        x_label = Tex('x', font_size=32).next_to(axes_1.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
        y_label = Tex('y', font_size=32).next_to(axes_1.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
        axes_1_group = VGroup(axes_1, x_label, y_label)
        x_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [1, 0, 0])
        y_label.rotate(DEGREES * 90, [0, 0, 1])
        axes_1[0].rotate(DEGREES * 90, [1, 0, 0])
        axes_1[1].rotate(DEGREES * 90, [0, 1, 0])
        neuron_idx_1 = 106
        neuron_1_mean = np.mean(mlp_hook_pre[:, :, 2, neuron_idx_1]) - 0.2
        pts_1_x = Group()
        for j in range(p):
            x = j
            y = mlp_hook_pre[j, 0, 2, neuron_idx_1] - neuron_1_mean
            pt = Dot3D(axes_1.c2p(x, 0, y), radius=0.02)
            pt.set_color(FRESH_TAN)
            pts_1_x.add(pt)
        pts_1_y = Group()
        for j in range(p):
            x = j
            y = mlp_hook_pre[0, j, 2, neuron_idx_1] - neuron_1_mean
            pt = Dot3D(axes_1.c2p(0, x, y), radius=0.02)
            pt.set_color(FRESH_TAN)
            pts_1_y.add(pt)
        self.frame.reorient(0, 90, 0)
        self.add(axes_1[0], x_label, axes_1[2])
        self.wait()
        self.wait()
        self.play(self.frame.animate.reorient(92, 79, 0, (-0.48, -0.58, -0.02), 6.58), ShowCreation(axes_1[1]), ShowCreation(y_label), x_label.animate.rotate(180 * DEGREES, [0, 0, 1]), run_time=5)
        self.wait()
        self.wait()
        surf_func_with_axes = partial(surf_func, axes=axes_1, surf_array=mlp_hook_pre[:, :, 2, neuron_idx_1] - neuron_1_mean, scale=1.0)
        surface = ParametricSurface(surf_func_with_axes, u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
        ts = TexturedSurface(surface, str(data_dir / ('activations_' + str(neuron_idx_1).zfill(3) + '.png')))
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.8)
        self.wait()
        self.play(self.frame.animate.reorient(31, 70, 0, (-0.19, -0.28, -0.29), 6.6), run_time=4)
        self.wait()
        self.play(ShowCreation(ts), self.frame.animate.reorient(132, 36, 0, (-0.4, -0.43, -0.72), 8.05), run_time=10)
        self.wait()
        self.play(self.frame.animate.reorient(61, 53, 0, (-0.4, -0.43, -0.72), 8.05), run_time=6)
        self.play(self.frame.animate.reorient(132, 36, 0, (-0.4, -0.43, -0.72), 8.05), run_time=6)
        self.remove(pts_1_y, pts_1_x)
        self.wait()
        fourier_funcs = [lambda i, j: 0.354 * np.cos(2 * np.pi * (4 * i / 113) - 0.516) * np.cos(2 * np.pi * (4 * j / 113) - 0.516), lambda i, j: 0.173 * np.cos(2 * np.pi * (8 * j / 113) + 2.653), lambda i, j: 0.173 * np.cos(2 * np.pi * (8 * i / 113) + 2.653)]
        vertical_spacing = 1.7
        axes_scale = 1.0
        component_axes = Group()
        labels = VGroup()
        for k in range(3):
            ax = ThreeDAxes(x_range=[0, p, 10], y_range=[0, p, 10], z_range=[-0.5, 0.5, 0.5], width=4 * axes_scale, height=4 * axes_scale, depth=1.4 * axes_scale, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2, 'tip_config': {'width': 0.04, 'length': 0.04}})
            x_label_temp = Tex('x', font_size=32).next_to(axes_1.x_axis.get_end(), RIGHT, buff=0.1).set_color(CHILL_BROWN)
            y_label_temp = Tex('y', font_size=32).next_to(axes_1.y_axis.get_end(), UP, buff=0.1).set_color(CHILL_BROWN)
            x_label_temp.rotate(DEGREES * 90, [1, 0, 0])
            y_label_temp.rotate(DEGREES * 90, [1, 0, 0])
            y_label_temp.rotate(DEGREES * 90, [0, 0, 1])
            x_label_temp.rotate(DEGREES * 180, [0, 0, 1])
            x_label_temp.shift([0, 0, -vertical_spacing * (k + 1)])
            y_label_temp.shift([0, 0, -vertical_spacing * (k + 1)])
            ax[0].rotate(DEGREES * 90, [1, 0, 0])
            ax[1].rotate(DEGREES * 90, [0, 1, 0])
            ax.move_to([0, 0, -vertical_spacing * (k + 1) + 0.0])
            component_axes.add(ax)
            labels.add(VGroup(x_label_temp, y_label_temp))
        surface_colors = [ORANGE, YELLOW, CYAN]
        component_surfaces = Group()
        for i, ax, func, color in zip(np.arange(len(component_axes)), component_axes, fourier_funcs, surface_colors):
            surf = ParametricSurface(make_fourier_surf_func(ax, func), u_range=[0, 1.0], v_range=[0, 1.0], resolution=(resolution, resolution))
            surf.set_color(color).set_shading(0.1, 0.5, 0.5)
            component_surfaces.add(surf)
        surf_copy_2 = surface.copy().set_color(YELLOW).shift([0, 0, -0.001])
        surf_copy_1 = surface.copy().set_color(CYAN).shift([0, 0, -0.001])
        surf_copy_0 = surface.copy().set_color(ORANGE).shift([0, 0, -0.001])
        self.wait()
        self.remove(axes_1, x_label, y_label)
        ts.set_shading(0.1, 0.3, 0.1)
        self.remove(ts)
        self.add(component_surfaces[2])
        self.frame.reorient(137, 55, 0, (0.25, 0.12, -1.87), 6.11)
        self.add(surf_copy_2, surf_copy_1, surf_copy_0)
        self.remove(ts)
        self.add(ts)
        self.play(ReplacementTransform(surf_copy_2, component_surfaces[2]), ReplacementTransform(axes_1.copy(), component_axes[2]), ReplacementTransform(surf_copy_1, component_surfaces[1]), ReplacementTransform(axes_1.copy(), component_axes[1]), ReplacementTransform(surf_copy_0, component_surfaces[0]), ReplacementTransform(axes_1.copy(), component_axes[0]), ReplacementTransform(x_label.copy(), labels[0][0]), ReplacementTransform(x_label.copy(), labels[1][0]), ReplacementTransform(x_label.copy(), labels[2][0]), ReplacementTransform(y_label.copy(), labels[0][1]), ReplacementTransform(y_label.copy(), labels[1][1]), ReplacementTransform(y_label.copy(), labels[2][1]), self.frame.animate.reorient(137, 59, 0, (0.28, 0.08, -2.34), 8.54), run_time=7)
        self.remove(component_surfaces)
        self.add(component_surfaces)
        self.wait()
        self.play(self.frame.animate.reorient(163, 84, 0, (-0.02, 0.17, -2.58), 8.54), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(89, 84, 0, (-0.02, 0.17, -2.58), 8.54), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(133, 68, 0, (-0.02, 0.17, -2.58), 8.54), run_time=4)
        self.wait()
        surf_copy_2b = surface.copy().set_color(YELLOW).shift([0, 0, -0.001])
        surf_copy_1b = surface.copy().set_color(CYAN).shift([0, 0, -0.001])
        surf_copy_0b = surface.copy().set_color(ORANGE).shift([0, 0, -0.001])
        self.wait()
        self.play(ReplacementTransform(component_surfaces[2], surf_copy_2b), ReplacementTransform(component_axes[2], axes_1.copy()), ReplacementTransform(component_surfaces[1], surf_copy_1b), ReplacementTransform(component_axes[1], axes_1.copy()), ReplacementTransform(component_surfaces[0], surf_copy_0b), ReplacementTransform(component_axes[0], axes_1.copy()), ReplacementTransform(labels[0][0], x_label.copy()), ReplacementTransform(labels[1][0], x_label.copy()), ReplacementTransform(labels[2][0], x_label.copy()), ReplacementTransform(labels[0][1], y_label.copy()), ReplacementTransform(labels[1][1], y_label.copy()), ReplacementTransform(labels[2][1], y_label.copy()), self.frame.animate.reorient(135, 39, 0, (-0.09, -0.17, -1.42), 8.05), run_time=7)
        self.remove(component_surfaces, surf_copy_2b, surf_copy_1b, surf_copy_0b, component_axes)
        self.remove(ts)
        self.add(ts)
        self.wait()
        self.play(self.frame.animate.reorient(134, 42, 0, (1.31, 1.43, -2.65), 11.48), run_time=5)
        self.wait()
        self.wait(20)
        self.embed()

class P41_43(InteractiveScene):

    def construct(self):
        p = 113
        svg_files = list(sorted(svg_dir.glob('*network_to_manim*')))
        with open(data_dir / 'final_model_activations_sample.p', 'rb') as f:
            activations = pickle.load(f)
        all_svgs = Group()
        for svg_file in svg_files[1:20]:
            svg_image = SVGMobject(str(svg_file))
            all_svgs.add(svg_image[1:])
        all_svgs.scale(6.0)
        example_index = 0
        self.frame.reorient(0, 0, 0, (0, 0, 0), 8.0)
        draw_inputs(self, activations, all_svgs, reset=False, example_index=example_index, wait=0)
        draw_embeddings(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        draw_attention_values(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_attention_patterns(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_1(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_2(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_3(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_logits(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex, temperature=25.0)
        self.add(all_svgs[:15], all_svgs[16])
        self.remove(all_svgs[7])
        self.add(all_svgs[7])
        axis_1 = Axes(x_range=[0, 1.0, 1], y_range=[-1.0, 1.0, 1], width=2 * 2.4, height=2 * 0.56, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 1.8, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axis_2 = Axes(x_range=[0, 1.0, 1], y_range=[-1.0, 1.0, 1], width=2 * 2.4, height=2 * 0.56, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 1.8, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axis_1.move_to([-4, 3.05, 0])
        x_label = Tex('x', font_size=24)
        x_label.set_color(CHILL_BROWN)
        x_label.next_to(axis_1, RIGHT, buff=0.1)
        x_label.shift([0, -0.1, 0])
        axis_2.move_to([-4, -2.85, 0])
        y_label = Tex('y', font_size=24)
        y_label.set_color(CHILL_BROWN)
        y_label.next_to(axis_2, RIGHT, buff=0.1)
        y_label.shift([0, -0.1, 0])
        sparse_probe_1 = np.load(data_dir / 'sparse_probe_1.npy')
        sparse_probe_2 = np.load(data_dir / 'sparse_probe_2.npy')
        sparse_probe_3 = np.load(data_dir / 'sparse_probe_3.npy')
        sparse_probe_4 = np.load(data_dir / 'sparse_probe_4.npy')
        pts_curve_1 = []
        dots_curve_1 = VGroup()
        for j in range(p):
            x = j / p
            y = sparse_probe_1[j]
            pts_curve_1.append(axis_1.c2p(x, y))
            pt = Dot(axis_1.c2p(x, y), radius=0.02, stroke_width=0)
            pt.set_color(WHITE)
            dots_curve_1.add(pt)
        curve_1 = VMobject(stroke_width=3)
        curve_1.set_points_smoothly(pts_curve_1)
        curve_1.set_color(YELLOW)
        pts_curve_2 = []
        dots_curve_2 = VGroup()
        for j in range(p):
            x = j / p
            y = sparse_probe_2[j]
            pts_curve_2.append(axis_1.c2p(x, y))
            pt = Dot(axis_1.c2p(x, y), radius=0.02, stroke_width=0)
            pt.set_color(WHITE)
            dots_curve_2.add(pt)
        curve_2 = VMobject(stroke_width=3)
        curve_2.set_points_smoothly(pts_curve_2)
        curve_2.set_color(MAGENTA)
        pts_curve_3 = []
        dots_curve_3 = VGroup()
        for j in range(p):
            x = j / p
            y = sparse_probe_3[j]
            pts_curve_3.append(axis_2.c2p(x, y))
            pt = Dot(axis_2.c2p(x, y), radius=0.02, stroke_width=0)
            pt.set_color(WHITE)
            dots_curve_3.add(pt)
        curve_3 = VMobject(stroke_width=3)
        curve_3.set_points_smoothly(pts_curve_3)
        curve_3.set_color(CYAN)
        pts_curve_4 = []
        dots_curve_4 = VGroup()
        for j in range(p):
            x = j / p
            y = sparse_probe_4[j]
            pts_curve_4.append(axis_2.c2p(x, y))
            pt = Dot(axis_2.c2p(x, y), radius=0.02, stroke_width=0)
            pt.set_color(WHITE)
            dots_curve_4.add(pt)
        curve_4 = VMobject(stroke_width=3)
        curve_4.set_points_smoothly(pts_curve_4)
        curve_4.set_color(RED)
        wave_label_1 = Tex('\\cos \\big(\\tfrac{8\\pi}{113}x\\big)')
        wave_label_1.set_color(YELLOW)
        wave_label_1.scale(0.45 * 1.5)
        wave_label_1.move_to([-0.9, 3.65, 0])
        wave_label_2 = Tex('\\sin \\big(\\tfrac{8\\pi}{113}x\\big)')
        wave_label_2.set_color(MAGENTA)
        wave_label_2.scale(0.45 * 1.5)
        wave_label_2.move_to([-0.95, 2.65, 0])
        wave_label_3 = Tex('\\cos \\big(\\tfrac{8\\pi}{113}y\\big)')
        wave_label_3.set_color(CYAN)
        wave_label_3.scale(0.45 * 1.5)
        wave_label_3.move_to([-0.9, -2.2, 0])
        wave_label_4 = Tex('\\sin \\big(\\tfrac{8\\pi}{113}y\\big)')
        wave_label_4.set_color(RED)
        wave_label_4.scale(0.45 * 1.5)
        wave_label_4.move_to([-0.9, -3.2, 0])
        self.add(all_svgs[18])
        self.add(axis_1, axis_2, x_label, y_label)
        self.add(curve_1, curve_2, curve_3, curve_4)
        self.add(wave_label_1, wave_label_2, wave_label_3, wave_label_4)
        self.wait()
        self.wait()
        self.play(FadeOut(all_svgs[5:15]), FadeOut(all_svgs[0][15:]), FadeOut(all_svgs[0][5:14]), run_time=5)
        self.wait()
        axis_3 = Axes(x_range=[-1.1, 1.1, 1], y_range=[-1.1, 1.1, 1], width=3.5, height=3.5, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2.4, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axis_3[0].set_color(YELLOW)
        axis_3[1].set_color(MAGENTA)
        axis_3.move_to([3, 1.9, 0])
        axis_4 = Axes(x_range=[-1.1, 1.1, 1], y_range=[-1.1, 1.1, 1], width=3.5, height=3.5, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 2.4, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axis_4[0].set_color(CYAN)
        axis_4[1].set_color(RED)
        axis_4.move_to([3, -1.9, 0])
        dots_curve_5 = VGroup()
        for j in range(p):
            pt = Dot(axis_3.c2p(sparse_probe_1[j], sparse_probe_2[j]), radius=0.02, stroke_width=0)
            pt.set_color(WHITE)
            dots_curve_5.add(pt)
        dots_curve_6 = VGroup()
        for j in range(p):
            pt = Dot(axis_4.c2p(sparse_probe_3[j], sparse_probe_4[j]), radius=0.02, stroke_width=0)
            pt.set_color(WHITE)
            dots_curve_6.add(pt)
        wave_label_1_copy = wave_label_1.copy()
        wave_label_1_copy.next_to(axis_3, RIGHT, buff=0.2)
        wave_label_2_copy = wave_label_2.copy()
        wave_label_2_copy.next_to(axis_3, TOP, buff=0)
        wave_label_2_copy.shift([0.9, -0.2, 0])
        wave_label_3_copy = wave_label_3.copy()
        wave_label_3_copy.next_to(axis_4, RIGHT, buff=0.2)
        wave_label_4_copy = wave_label_4.copy()
        wave_label_4_copy.next_to(axis_4, TOP, buff=0)
        wave_label_4_copy.shift([0.9, -0.2, 0])
        self.wait()
        self.play(ShowCreation(axis_3), run_time=2)
        self.play(ReplacementTransform(wave_label_1.copy(), wave_label_1_copy), run_time=2)
        self.play(ReplacementTransform(wave_label_2.copy(), wave_label_2_copy), run_time=2)
        self.wait()
        self.play(FadeIn(dots_curve_1), FadeIn(dots_curve_2), run_time=2)
        self.play(ReplacementTransform(dots_curve_1, dots_curve_5), ReplacementTransform(dots_curve_2, dots_curve_5), run_time=5)
        self.wait()
        self.play(ShowCreation(axis_4), ReplacementTransform(wave_label_3.copy(), wave_label_3_copy), ReplacementTransform(wave_label_4.copy(), wave_label_4_copy), run_time=2)
        self.play(ReplacementTransform(dots_curve_3, dots_curve_6), ReplacementTransform(dots_curve_4, dots_curve_6), run_time=5)
        self.wait()
        self.play(FadeOut(wave_label_1_copy), FadeOut(wave_label_2_copy), FadeOut(wave_label_3_copy), FadeOut(wave_label_4_copy), FadeOut(axis_3), FadeOut(axis_4), FadeOut(dots_curve_5), FadeOut(dots_curve_6), run_time=2)
        self.play(FadeIn(all_svgs[5:15]), FadeIn(all_svgs[0][15:]), FadeIn(all_svgs[0][5:14]), run_time=2)
        self.add(all_svgs[:15], all_svgs[16])
        self.remove(all_svgs[7])
        self.add(all_svgs[7])
        self.wait()
        example_index = 226
        draw_inputs(self, activations, all_svgs, reset=False, example_index=example_index, wait=0)
        draw_embeddings(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        draw_attention_values(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_attention_patterns(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_1(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_2(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_mlp_3(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex)
        draw_logits(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex, temperature=25.0)
        self.add(all_svgs[:15], all_svgs[16])
        self.remove(all_svgs[7])
        self.add(all_svgs[7])
        self.wait()
        self.wait()
        addition_line = Line(start=[-1.13, -0.3, 0], end=[0.6, -0.3, 0])
        addition_line.set_stroke(width=2)
        addition_line.set_color(WHITE)
        plus_sign = Tex('+', font_size=28)
        plus_sign.set_color(WHITE)
        plus_sign.move_to([0.5, -0.1, 0])
        self.play(FadeOut(all_svgs[6:8]), FadeOut(all_svgs[12:14]), FadeOut(all_svgs[5][0]), FadeOut(all_svgs[5][11:]), run_time=2)
        self.play(wave_label_1.animate.move_to([-0.45, 0.5, 0]), wave_label_3.animate.move_to([-0.45, 0.0, 0]), run_time=3)
        self.play(ShowCreation(addition_line), ShowCreation(plus_sign), run_time=2)
        self.wait()
        self.wait(20)
        self.embed()