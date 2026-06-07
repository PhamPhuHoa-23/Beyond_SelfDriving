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
svg_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/grokking/graphics/to_manim')
data_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/grokking/from_linux/grok_1764706121')

class P28_31h(InteractiveScene):

    def construct(self):
        p = 113
        svg_files = list(sorted(svg_dir.glob('*network_to_manim*')))
        with open(data_dir / 'final_model_activations_sample.p', 'rb') as f:
            activations = pickle.load(f)
        all_svgs = Group()
        for svg_file in svg_files[1:17]:
            svg_image = SVGMobject(str(svg_file))
            all_svgs.add(svg_image[1:])
        all_svgs.scale(6.0)
        draw_inputs(self, activations, all_svgs, reset=True, example_index=0)
        draw_attention_patterns(self, activations, all_svgs, reset=True, example_index=0)
        np.random.seed(5)
        R = np.random.uniform(0.3, 0.75, len(all_svgs[8]))
        for i in range(len(all_svgs[8])):
            all_svgs[8][i].set_opacity(R[i])
        example_index = 115
        self.frame.reorient(0, 0, 0, (0.02, -0.06, 0.0), 7.58)
        draw_inputs(self, activations, all_svgs, reset=False, example_index=example_index, wait=0)
        draw_embeddings(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        draw_attention_values(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.1, colormap=black_to_tan_hex)
        draw_attention_patterns(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.1, colormap=black_to_tan_hex)
        draw_mlp_1(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.1, colormap=black_to_tan_hex)
        draw_mlp_2(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.1, colormap=black_to_tan_hex)
        draw_mlp_3(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.1, colormap=black_to_tan_hex)
        draw_logits(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.0, colormap=black_to_tan_hex, temperature=25.0)
        self.remove(all_svgs[7])
        self.add(all_svgs[7])
        self.add(all_svgs[:15])
        self.wait()
        p28_fade_group = Group(all_svgs[14][9], all_svgs[14][:3], all_svgs[10], all_svgs[11], all_svgs[0][7:14], all_svgs[0][-1], all_svgs[8][-105:], all_svgs[9][-14:], all_svgs[14][-20:])
        self.wait()
        self.play(FadeOut(p28_fade_group), run_time=3.0)
        self.wait()
        example_index = 0
        draw_inputs(self, activations, all_svgs, reset=False, example_index=example_index, wait=0.1)
        draw_embeddings(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        draw_attention_values(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        draw_attention_patterns(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        self.remove(all_svgs[7])
        self.add(all_svgs[7])
        draw_mlp_1(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        draw_mlp_2(self, activations, all_svgs, reset=False, example_index=example_index, wait=0, colormap=black_to_tan_hex)
        self.wait()
        activation_txt = VGroup()
        activation_arrows = VGroup()
        for i in range(7):
            val = activations['blocks.0.mlp.hook_pre'][example_index, 2, i]
            txt = Tex(f'{val:.2f}', font_size=24)
            activation_txt.add(txt)
        activation_txt.set_color(FRESH_TAN)
        activation_txt.arrange(DOWN, buff=0.128)
        activation_txt.move_to([3.6, 0.73, 0])
        for i in range(7):
            arr = Arrow(start=LEFT, end=RIGHT, buff=0.05, stroke_width=1.4, max_tip_length_to_length_ratio=0.3).scale(0.2)
            activation_arrows.add(arr)
        activation_arrows.set_color(CHILL_BROWN)
        activation_arrows.arrange(DOWN, buff=0.16)
        activation_arrows.move_to([3.0, 0.73, 0])
        self.wait()
        self.play(FadeIn(activation_arrows), Write(activation_txt), lag_ratio=0.5)
        self.play(FadeOut(activation_arrows), FadeOut(activation_txt))
        self.wait()
        axes = VGroup()
        for i in range(7):
            a = Axes(x_range=[0, 1.0, 1], y_range=[-1.0, 1.0, 1], width=2.4, height=0.8, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 1.2, 'tip_config': {'width': 0.02, 'length': 0.02}})
            axes.add(a)
        axes.arrange(DOWN, buff=0.2)
        axes.move_to([4.8, 0, 0])
        all_pts = VGroup()
        neuron_indices = [0, 3, 4, 5, 9, 2, 11]
        for i, neuron_idx in enumerate(neuron_indices):
            neuron_average = activations['blocks.0.mlp.hook_pre'][:p, 2, neuron_idx].mean()
            neuron_max = np.max(np.abs(activations['blocks.0.mlp.hook_pre'][:p, 2, neuron_idx] - neuron_average)) * 1.0
            dese_pts = VGroup()
            for j in range(p):
                x = j / p
                y = (activations['blocks.0.mlp.hook_pre'][j, 2, neuron_idx] - neuron_average) / neuron_max
                pt = Dot(axes[i].c2p(x, y), radius=0.02, color=FRESH_TAN, stroke_width=0)
                dese_pts.add(pt)
            all_pts.add(dese_pts)
        self.wait()
        self.play(Write(all_svgs[15]), Write(axes), run_time=4)
        self.wait()
        axes_2 = VGroup()
        for i in range(49):
            a = Axes(x_range=[-1.0, 1.0, 1], y_range=[-1.0, 1.0, 1], width=0.8, height=0.8, axis_config={'color': CHILL_BROWN, 'include_ticks': False, 'include_numbers': False, 'include_tip': True, 'stroke_width': 1.2, 'tip_config': {'width': 0.02, 'length': 0.02}})
            axes_2.add(a)
        axes_2.arrange_in_grid(n_rows=7, n_cols=7, buff=0.2)
        axes_2.move_to([10, 0, 0])
        all_pts_2 = VGroup()
        for i, neuron_idx_1 in enumerate(neuron_indices):
            for k, neuron_idx_2 in enumerate(neuron_indices):
                dese_pts = VGroup()
                neuron_average_x = activations['blocks.0.mlp.hook_pre'][:p, 2, neuron_idx_1].mean()
                neuron_average_y = activations['blocks.0.mlp.hook_pre'][:p, 2, neuron_idx_2].mean()
                neuron_max_x = np.max(np.abs(activations['blocks.0.mlp.hook_pre'][:p, 2, neuron_idx_1] - neuron_average_x)) * 1.0
                neuron_max_y = np.max(np.abs(activations['blocks.0.mlp.hook_pre'][:p, 2, neuron_idx_2] - neuron_average_y)) * 1.0
                for j in range(p):
                    x = (activations['blocks.0.mlp.hook_pre'][j, 2, neuron_idx_2] - neuron_average_y) / neuron_max_y
                    y = (activations['blocks.0.mlp.hook_pre'][j, 2, neuron_idx_1] - neuron_average_x) / neuron_max_x
                    pt = Dot(axes_2[len(neuron_indices) * i + k].c2p(x, y), radius=0.02, stroke_width=0)
                    pt.set_color(viridis_hex(j, 0, p))
                    dese_pts.add(pt)
                all_pts_2.add(dese_pts)
        self.wait()
        self.frame.reorient(0, 0, 0, (8.0, 1.98, 0.0), 3.06)
        self.play(self.frame.animate.reorient(0, 0, 0, (7.62, 0.06, 0.0), 7.58), Write(axes_2), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (6.27, 2.27, 0.0), 3.75), run_time=4)
        self.wait()
        self.play(ReplacementTransform(all_pts[0].copy(), all_pts_2[1]), ReplacementTransform(all_pts[1].copy(), all_pts_2[1]), lag_ratio=0.1, run_time=10)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (7.62, 0.06, 0.0), 7.58), FadeIn(all_pts_2[0]), FadeIn(all_pts_2[2:]), run_time=4)
        self.wait()
        activation_history = np.load(str(data_dir / 'time_history_mlp_hook_pre_1.npy'))
        self.frame.reorient(0, 0, 0, (9.28, 1.03, 0.0), 5.22)
        self.remove(axes_2)
        for step_count in tqdm(np.arange(999, -1, -1)):
            all_pts_old = all_pts
            all_pts_2_old = all_pts_2
            all_pts = VGroup()
            for i, neuron_idx in enumerate(neuron_indices):
                neuron_average = activation_history[step_count, :p, 2, neuron_idx].mean()
                neuron_max = np.max(np.abs(activation_history[step_count, :p, 2, neuron_idx] - neuron_average)) * 1.0
                dese_pts = VGroup()
                for j in range(p):
                    x = j / p
                    y = (activation_history[step_count, j, 2, neuron_idx] - neuron_average) / neuron_max
                    pt = Dot(axes[i].c2p(x, y), radius=0.02, color=FRESH_TAN, stroke_width=0)
                    pt.set_color(viridis_hex(j, 0, p))
                    dese_pts.add(pt)
                all_pts.add(dese_pts)
            all_pts_2 = VGroup()
            for i, neuron_idx_1 in enumerate(neuron_indices):
                for k, neuron_idx_2 in enumerate(neuron_indices):
                    dese_pts = VGroup()
                    neuron_average_x = activation_history[step_count, :p, 2, neuron_idx_1].mean()
                    neuron_average_y = activation_history[step_count, :p, 2, neuron_idx_2].mean()
                    neuron_max_x = np.max(np.abs(activation_history[step_count, :p, 2, neuron_idx_1] - neuron_average_x)) * 1.0
                    neuron_max_y = np.max(np.abs(activation_history[step_count, :p, 2, neuron_idx_2] - neuron_average_y)) * 1.0
                    for j in range(p):
                        x = (activation_history[step_count, j, 2, neuron_idx_2] - neuron_average_y) / neuron_max_y
                        y = (activation_history[step_count, j, 2, neuron_idx_1] - neuron_average_x) / neuron_max_x
                        pt = Dot(axes_2[len(neuron_indices) * i + k].c2p(x, y), radius=0.02, stroke_width=0)
                        pt.set_color(viridis_hex(j, 0, p))
                        dese_pts.add(pt)
                    all_pts_2.add(dese_pts)
            self.remove(all_pts_old, all_pts_2_old)
            self.add(all_pts, all_pts_2)
            self.wait(0.2)
        self.wait(20)
        self.embed()