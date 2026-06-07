from manimlib import *
from manimlib.mobject.svg.old_tex_mobject import *
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib import cm
import sys
sys.path.append('/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/dark_matter_of_ai/animations/videos')
from helpers import *
import pickle
data_dir = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/dark_matter_of_ai/animations/videos'
with open(data_dir + '/gemma_cache_dict_1.p', 'rb') as f:
    cache = pickle.load(f)
with open(data_dir + '/w_u_reduced.p', 'rb') as f:
    w_u_reduced = pickle.load(f)
with open(data_dir + '/example_output.p', 'rb') as f:
    example_output = pickle.load(f)
with open(data_dir + '/top_activating_text_dec_19_2.p', 'rb') as f:
    top_activating_words, top_activating_word_activations = pickle.load(f)
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'

class P25b(InteractiveScene):

    def construct(self):
        layer_id = 25
        sampled_layer_out_matrix = np.hstack((cache['blocks.' + str(layer_id) + '.hook_resid_post'][1:, :3], cache['blocks.' + str(layer_id) + '.hook_resid_post'][1:, -2:]))
        layer_out_matrix = Matrix(sampled_layer_out_matrix.round(2), ellipses_col=3).scale(0.6)
        self.add(layer_out_matrix)
        self.frame.reorient(0, 0, 0, (0, 0, 0), 8)
        last_row = layer_out_matrix.get_entries()[-len(sampled_layer_out_matrix[0]) + 1:]
        surrounding_rect = RoundedRectangle(corner_radius=0.1, stroke_color='#ffd35a', stroke_width=3, width=last_row[-1].get_center()[0] - last_row[0].get_center()[0] + 1, height=0.6, fill_opacity=0)
        surrounding_rect.move_to(last_row[len(last_row) // 2])
        self.play(ShowCreation(surrounding_rect, run_time=1.5), FadeIn(surrounding_rect, rate_func=lambda t: smooth(t), run_time=1.2))
        last_row = layer_out_matrix[-7:-2].copy()
        self.remove(layer_out_matrix[-7:-2])
        self.add(last_row)
        sampled_layer_out_matrix_longer = np.hstack((cache['blocks.' + str(layer_id) + '.hook_resid_post'][-1:, :200], cache['blocks.' + str(layer_id) + '.hook_resid_post'][-1:, -200:]))
        last_row_longer = Matrix(sampled_layer_out_matrix_longer.round(2), ellipses_col=200).scale(0.6)
        diff = last_row[0].get_center() - last_row_longer[0].get_center()
        last_row_longer.shift(diff)
        self.play(FadeOut(surrounding_rect), FadeOut(layer_out_matrix), run_time=1)
        self.wait()
        self.play(FadeOut(last_row), FadeIn(last_row_longer), run_time=1)
        self.wait()
        self.play(last_row_longer.animate.scale(0.03).move_to(ORIGIN), run_time=4)
        self.wait()
        b = Brace(last_row_longer, UP, buff=0.1, stroke_width=0)
        b.set_color(CHILL_BROWN)
        bt = Text('2,304').scale(0.6).next_to(b, UP, buff=0.1).set_color(CHILL_BROWN)
        self.add(b, bt)
        self.wait()
        self.remove(b, bt)
        self.wait()
        groups = []
        for i in range(20):
            groups.append(VGroup([*last_row_longer[i * 20:(i + 1) * 20]]))
        initial_vertical_spacing = 0.3
        self.remove(last_row_longer[-3:])
        self.play(*[g.animate.scale(8).move_to(UP * initial_vertical_spacing * (10 - i)) for i, g in enumerate(groups)], run_time=4)
        self.wait()
        input_matrix = get_image_and_border(path='gemma_cached_images_dec_16_1/hook_embed_1.png', scale=1.5)
        input_matrix.shift(0.15 * UP)
        input_matrix_color_bar = ImageMobject('gemma_cached_images_dec_16_1/hook_embed_1_colorbar.png')
        input_matrix_color_bar.to_edge(RIGHT, buff=1.0)
        self.play(FadeIn(input_matrix))
        self.add(input_matrix_color_bar)
        self.wait()

class P25bMoreElements(InteractiveScene):

    def construct(self):
        layer_id = 25
        sampled_layer_out_matrix = np.hstack((cache['blocks.' + str(layer_id) + '.hook_resid_post'][1:, :3], cache['blocks.' + str(layer_id) + '.hook_resid_post'][1:, -2:]))
        layer_out_matrix = Matrix(sampled_layer_out_matrix.round(2), ellipses_col=3).scale(0.6)
        self.add(layer_out_matrix)
        self.frame.reorient(0, 0, 0, (0, 0, 0), 8)
        last_row = layer_out_matrix.get_entries()[-len(sampled_layer_out_matrix[0]) + 1:]
        surrounding_rect = RoundedRectangle(corner_radius=0.1, stroke_color='#ffd35a', stroke_width=3, width=last_row[-1].get_center()[0] - last_row[0].get_center()[0] + 1, height=0.6, fill_opacity=0)
        surrounding_rect.move_to(last_row[len(last_row) // 2])
        self.play(ShowCreation(surrounding_rect, run_time=1.5), FadeIn(surrounding_rect, rate_func=lambda t: smooth(t), run_time=1.2))
        last_row = layer_out_matrix[-7:-2].copy()
        self.remove(layer_out_matrix[-7:-2])
        self.add(last_row)
        sampled_layer_out_matrix_longer = cache['blocks.' + str(layer_id) + '.hook_resid_post'][-1:, :]
        last_row_longer = Matrix(sampled_layer_out_matrix_longer.round(2), ellipses_col=1152).scale(0.6)
        diff = last_row[0].get_center() - last_row_longer[0].get_center()
        last_row_longer.shift(diff)
        self.play(FadeOut(surrounding_rect), FadeOut(layer_out_matrix), run_time=1)
        self.wait()
        self.add(last_row_longer)
        self.play(FadeOut(last_row), FadeIn(last_row_longer), run_time=1)
        self.wait()
        self.play(last_row_longer.animate.scale(0.00458).move_to(ORIGIN), run_time=4)
        self.wait()
        b = Brace(last_row_longer, UP, buff=0.1, stroke_width=0)
        b.set_color(CHILL_BROWN)
        bt = Text('2,304').scale(0.6).next_to(b, UP, buff=0.1).set_color(CHILL_BROWN)
        self.add(b, bt)
        self.wait()
        self.remove(b, bt)
        self.wait()
        groups = []
        for i in range(48):
            groups.append(VGroup([*last_row_longer[i * 48:(i + 1) * 48]]))
        initial_vertical_spacing = 0.143
        self.remove(last_row_longer[-3:])
        self.play(*[g.animate.scale(24).move_to(UP * initial_vertical_spacing * (24 - i)) for i, g in enumerate(groups)], run_time=4)
        self.wait()
        input_matrix = get_image_and_border(path='gemma_cached_images_dec_16_1/hook_embed_1.png')
        input_matrix.scale(1.135)
        input_matrix.shift(0.09 * UP)
        input_matrix.set_opacity(0.5)
        self.add(input_matrix)
        self.remove(input_matrix)
        input_matrix_color_bar = ImageMobject('gemma_cached_images_dec_16_1/hook_embed_1_colorbar.png')
        input_matrix_color_bar.to_edge(RIGHT, buff=1.0)
        self.play(FadeIn(input_matrix))
        self.add(input_matrix_color_bar)
        self.wait()

class P26_P27(InteractiveScene):

    def construct(self):
        input_matrix = get_image_and_border(path='gemma_cached_images_dec_16_1/hook_embed_1.png', scale=1.5)
        input_matrix.shift(0.15 * UP)
        input_matrix_color_bar = ImageMobject('gemma_cached_images_dec_16_1/hook_embed_1_colorbar.png')
        input_matrix_color_bar.to_edge(RIGHT, buff=1.0)
        self.add(input_matrix, input_matrix_color_bar)
        self.wait()
        self.remove(input_matrix_color_bar)
        self.play(input_matrix.animate.move_to(3 * LEFT).scale(0.3), run_time=2.0)
        self.wait()
        square = RoundedRectangle(width=2, height=2, corner_radius=0.2, fill_opacity=0.0, stroke_color='#ffd35a', stroke_width=4)
        square_text = Text('Unembed', font='Myriad Pro').set_color('#ffd35a')
        square_text.scale(0.8)
        subtext = Text('norm>unembed \n >softcap>softmax', font='Myriad Pro').set_color('#555555')
        subtext.scale(0.3)
        subtext.next_to(square_text, DOWN, buff=0.1)
        square_group = VGroup(square, square_text, subtext)
        square_group.next_to(input_matrix, RIGHT, buff=1.0)
        self.add(square_group)
        arrow_1 = Arrow(start=input_matrix.get_right(), end=square_group.get_left(), buff=0.2, thickness=4).set_color(YELLOW)
        self.add(arrow_1)
        self.wait(1)
        top_tokens = {' very': 1.0, '': 0.0, '': 0.0, '': 0.0, '': 0.0, '': 0.0, '': 0.0, '': 0.0, '': 0.0, '': 0.0}
        cmap = plt.cm.viridis
        max_value = max(top_tokens.values())
        scale_factor = 1
        i = 0
        word = list(top_tokens.keys())[i]
        hex_color = rgb_to_hex(cmap(top_tokens[word] / max_value)[:3])
        first_word = Text(word, font='Myriad Pro').scale(0.8)
        first_word.set_color(hex_color)
        first_word_hex_color = hex_color
        first_word.next_to(square_group, RIGHT, buff=1.0)
        first_word.shift(0.8 * UP)
        first_bar = Rectangle(height=0.14, width=top_tokens[word] * scale_factor, fill_opacity=1, color=hex_color)
        first_bar.next_to(first_word, RIGHT, buff=0.3)
        first_bar.shift(0.05 * UP)
        first_value = Text(f'{top_tokens[word]:.4f}').set_color('#FFFFFF').scale(0.38)
        first_value.next_to(first_bar, RIGHT, buff=0.4)
        self.add(first_word, first_bar, first_value)
        arrow_2 = arrow_1.copy()
        arrow_2.move_to(square_group.get_right() + 0.5 * RIGHT)
        self.add(arrow_2)
        self.wait(1)
        words = ['The', 'reliability', 'of', 'Wikipedia', 'is', 'very']
        vertical_text = VGroup(*[Text(word, font='Myriad Pro').scale(0.8) for word in words]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        word_to_vector_arrows = VGroup()
        for i in range(len(vertical_text)):
            vert_pos = vertical_text[i].get_center()[1]
            arrow = Arrow(start=np.array([-4.5, vert_pos, 0]), end=np.array([-3.8, vert_pos, 0]), buff=0, thickness=3, tip_width_ratio=4)
            arrow.set_color('#948979')
            word_to_vector_arrows.add(arrow)
        vertical_text[2].shift([0, 0.07, 0.0])
        vertical_text[4].shift([0, 0.07, 0.0])
        vertical_text.to_edge(LEFT)
        sampled_embedding_matrix = np.hstack((cache['hook_embed'][1:, :3], cache['hook_embed'][1:, -2:]))
        embedding_matrix = Matrix(sampled_embedding_matrix.round(2), ellipses_col=3).scale(0.73)
        embedding_matrix.next_to(word_to_vector_arrows[i], RIGHT, buff=0.6)
        embedding_matrix.shift([0, 1.5, 0])
        last_row = embedding_matrix.get_entries()[-len(sampled_embedding_matrix[0]) + 1:]
        surrounding_rect = RoundedRectangle(corner_radius=0.1, stroke_color='#ffd35a', stroke_width=3, width=last_row[-1].get_center()[0] - last_row[0].get_center()[0] + 1, height=0.6, fill_opacity=0)
        surrounding_rect.move_to(last_row[len(last_row) // 2])
        text_matrix_arrows = VGroup(vertical_text, word_to_vector_arrows, embedding_matrix, surrounding_rect)
        text_matrix_arrows.scale(0.55)
        text_matrix_arrows.next_to(input_matrix, UP, buff=0.6)
        text_matrix_arrows.shift(LEFT * (embedding_matrix.get_center()[0] - input_matrix.get_center()[0]))
        self.add(text_matrix_arrows)
        arrow_3 = Arrow(start=embedding_matrix.get_bottom(), end=input_matrix.get_top(), buff=0.1, thickness=4).set_color(YELLOW)
        self.add(arrow_3)
        self.wait(1)
        self.remove(first_word, first_bar, first_value)
        top_tokens = {'_very': 0.006, 'very': 0.006, '_Very': 0.006, 'Very': 0.006, '_VERY': 0.006, '_très': 0.006, '_muy': 0.006, 'VERY': 0.006, '_extremely': 0.006, '_sehr': 0.0059}
        cmap = plt.cm.viridis
        max_value = max(top_tokens.values()) * 3
        scale_factor = 15
        word_group = VGroup()
        bar_group = VGroup()
        prob_group = VGroup()
        i = 0
        word = list(top_tokens.keys())[i]
        hex_color = rgb_to_hex(cmap(top_tokens[word] / max_value)[:3])
        first_word = Text(word, font='Myriad Pro').scale(0.8)
        first_word.set_color(hex_color)
        first_word_hex_color = hex_color
        first_word.next_to(square_group, RIGHT, buff=1.2)
        first_word.shift(2.5 * UP)
        first_bar = Rectangle(height=0.14, width=top_tokens[word] * scale_factor, fill_opacity=1, color=hex_color)
        first_bar.next_to(first_word, RIGHT, buff=1.2)
        first_value = Text(f'{top_tokens[word]:.4f}').set_color('#FFFFFF').scale(0.38)
        first_value.next_to(first_bar, RIGHT, buff=0.4)
        word_group.add(first_word)
        bar_group.add(first_bar)
        prob_group.add(first_value)
        word_bar_groups = VGroup()
        vertical_spacing = 0.55
        for i, (word, value) in enumerate(list(top_tokens.items())[1:], 1):
            word_text = Text(word, font='Myriad Pro', stroke_width=0).scale(0.8)
            hex_color = rgb_to_hex(cmap(top_tokens[word] / max_value)[:3])
            word_text.set_color(hex_color)
            word_text.next_to(square_group, RIGHT, buff=1.2)
            word_text.shift(2.5 * UP)
            word_text.shift(DOWN * i * vertical_spacing)
            bar = Rectangle(height=0.14, width=value * scale_factor, fill_opacity=1, color=hex_color)
            bar.next_to(first_word, RIGHT, buff=1.2)
            bar.shift(DOWN * i * vertical_spacing)
            value_text = Text(f'{value:.4f}').set_color('#FFFFFF').scale(0.38)
            value_text.next_to(first_bar, RIGHT, buff=0.4)
            value_text.shift(DOWN * i * vertical_spacing)
            word_group.add(word_text)
            bar_group.add(bar)
            prob_group.add(value_text)
        for bar in bar_group:
            bar.save_state()
            bar.stretch(0, 0, about_edge=LEFT)
        self.play(*[Restore(bar) for bar in bar_group] + [FadeIn(word_group)], run_time=2.0, rate_func=smooth)
        self.add(prob_group)
        self.wait()
        self.play(FadeOut(VGroup(word_group, bar_group, prob_group, arrow_1, arrow_2, arrow_3, square_group, text_matrix_arrows)), run_time=1.0)
        self.wait()

class P28_P30(InteractiveScene):

    def construct(self):
        input_matrix = get_image_and_border(path='gemma_cached_images_dec_16_1/hook_embed_1.png', scale=1.5)
        input_matrix.rotate(90 * DEGREES, np.array([1, 0, 0]))
        self.add(input_matrix)
        input_matrix_2 = input_matrix.copy()
        self.add(input_matrix_2)
        self.frame.reorient(0, 90, 0, (4.5, -0.06, -0.18), 13.47)
        self.wait(1)
        attention_block_width = 8
        attention_block_height = 6
        attention_block_depth = 1
        mlp_block_width = 8
        mlp_block_height = 6
        mlp_block_depth = 1
        block_orig = np.array([0, 0, 0])
        line_padding = 0.3
        residual_compute_block_spacing = 11
        line_thickness = 6
        circle_stroke_width = 3
        plus_stroke_width = 3
        attention_block_1 = create_prism(center=block_orig + np.array([11, -4, 0]), height=attention_block_depth, width=attention_block_width, depth=attention_block_height, face_colors=BLUE, opacity=0.2, label_text='Attention', label_size=80, label_opacity=0.5, label_face='bottom')
        a0 = Arrow(start=block_orig + np.array([residual_compute_block_spacing + line_padding, 0, 0]), end=block_orig + np.array([3.5, 0, 0]), fill_color=WHITE, thickness=line_thickness, tip_width_ratio=0)
        a1 = Arrow(start=block_orig + np.array([residual_compute_block_spacing, 0.3, 0]), end=block_orig + np.array([residual_compute_block_spacing, -3.0, 0]), fill_color=WHITE, thickness=line_thickness)
        self.play(FadeIn(attention_block_1), FadeIn(a0), FadeIn(a1), self.frame.animate.reorient(-43, 64, 0, (5.25, -5.09, -1.39), 17.08), run_time=2.0)
        input_matrix.set_opacity(0.3)
        self.play(input_matrix_2.animate.move_to(np.array([residual_compute_block_spacing, 0, 0])), run_time=2)
        self.play(input_matrix_2.animate.move_to(np.array([residual_compute_block_spacing, -3, 0])), run_time=1, rate_func=linear)
        attention_out_matrix = get_image_and_border(path='gemma_cached_images_dec_16_1/hook_attn_out_1.png', scale=1.5)
        attention_out_matrix.rotate(90 * DEGREES, np.array([1, 0, 0]))
        attention_out_matrix.move_to(np.array([residual_compute_block_spacing, -3, 0]))
        self.play(FadeOut(input_matrix_2), FadeIn(attention_out_matrix), input_matrix_2.animate.move_to(np.array([residual_compute_block_spacing, -5, 0])), attention_out_matrix.animate.move_to(np.array([residual_compute_block_spacing, -5, 0])), run_time=1, rate_func=linear)
        self.wait(1)
        a2 = Arrow(start=block_orig + np.array([residual_compute_block_spacing, -5.0, 0]), end=block_orig + np.array([residual_compute_block_spacing, -6.3, 0]), fill_color=WHITE, thickness=line_thickness, tip_width_ratio=0)
        a3 = Arrow(start=block_orig + np.array([residual_compute_block_spacing + line_padding, -6, 0]), end=block_orig + np.array([0.5, -6, 0]), fill_color=WHITE, thickness=line_thickness)
        c = circle_plus(circle_stroke_width=circle_stroke_width, plus_stroke_width=plus_stroke_width, overall_scale=0.6, position=block_orig + np.array([0, -6, 0]))
        a4 = Arrow(start=block_orig + np.array([0, -0.75, 0]), end=block_orig + np.array([0, -5.5, 0]), fill_color=WHITE, thickness=line_thickness)
        self.play(FadeIn(a2), FadeIn(a3), FadeIn(c), FadeIn(a4))
        self.wait(1)
        self.play(input_matrix.animate.move_to(np.array([0, -6, 0])), run_time=2)
        self.wait()
        self.remove(input_matrix_2)
        self.play(attention_out_matrix.animate.move_to(np.array([residual_compute_block_spacing, -6, 0])), run_time=1, rate_func=smooth)
        self.play(attention_out_matrix.animate.move_to(np.array([0, -6, 0])), run_time=2, rate_func=smooth)
        residual_matrix_1 = get_image_and_border(path='gemma_cached_images_dec_16_1/hook_resid_mid_1.png', scale=1.5)
        residual_matrix_1.rotate(90 * DEGREES, np.array([1, 0, 0]))
        residual_matrix_1.move_to(np.array([0, -6, 0]))
        self.add(residual_matrix_1)
        self.remove(input_matrix)
        self.remove(attention_out_matrix)
        self.wait(1)
        self.play(self.frame.animate.reorient(0, 78, 0, (0.45, -4.73, 0.05), 17.08))
        self.wait()
        top_tokens = {'_very': 0.0117, 'very': 0.0117, 'Very': 0.0117, '_Very': 0.0117, '_VERY': 0.0117, 'VERY': 0.0117, '_très': 0.0117, '_muy': 0.0117, '_sehr': 0.0116, '_extremely': 0.0115}
        word_group, bar_group, prob_group = show_top_tokens(top_tokens)
        top_tokens_group = VGroup(word_group, bar_group, prob_group)
        top_tokens_group.rotate(90 * DEGREES, np.array([1, 0, 0]))
        top_tokens_group.scale(1.8)
        top_tokens_group.next_to(residual_matrix_1, LEFT, buff=2.2)
        self.add(word_group, bar_group, prob_group)
        arrow_3 = Arrow(start=residual_matrix_1.get_left(), end=top_tokens_group.get_right(), buff=0.4, thickness=8).set_color(YELLOW)
        arrow_3.rotate(90 * DEGREES, np.array([1, 0, 0]))
        self.add(arrow_3)
        self.wait(1)
        t = Text('The reliability of Wikipedia is very very ...', font='Myriad Pro').set_color(CHILL_BROWN)
        t.rotate(90 * DEGREES, np.array([1, 0, 0]))
        t.scale(1.8)
        t.next_to(residual_matrix_1, OUT, buff=2.5)
        self.play(Write(t))
        self.wait(1)
        self.remove(t, top_tokens_group, arrow_3)
        self.play(self.frame.animate.reorient(-27, 58, 0, (5.02, -7.35, -0.51), 16.9), residual_matrix_1.animate.move_to(np.array([0, -7.5, 0])), run_time=2)
        a6 = Arrow(start=block_orig + np.array([residual_compute_block_spacing + line_padding, -7.5, 0]), end=block_orig + np.array([3.5, -7.5, 0]), fill_color=WHITE, thickness=line_thickness, tip_width_ratio=0)
        a7 = Arrow(start=block_orig + np.array([residual_compute_block_spacing, -7.2, 0]), end=block_orig + np.array([residual_compute_block_spacing, -9, 0]), fill_color=WHITE, thickness=line_thickness)
        self.add(a6, a7)
        mlp_block_1 = create_prism(center=block_orig + np.array([11, -10, 0]), height=mlp_block_depth, width=mlp_block_width, depth=mlp_block_height, face_colors=GREEN, opacity=0.2, label_text='MLP', label_size=80, label_opacity=0.5, label_face='bottom')
        self.add(mlp_block_1)
        residual_matrix_1b = residual_matrix_1.copy()
        self.add(residual_matrix_1b)
        residual_matrix_1.set_opacity(0.3)
        self.play(residual_matrix_1b.animate.move_to(np.array([residual_compute_block_spacing, -7.5, 0])), run_time=2)
        self.play(residual_matrix_1b.animate.move_to(np.array([residual_compute_block_spacing, -9, 0])), run_time=1, rate_func=linear)
        mlp_out_matrix = get_image_and_border(path='gemma_cached_images_dec_18_1/hook_mlp_out_1.png', scale=1.5)
        mlp_out_matrix.rotate(90 * DEGREES, np.array([1, 0, 0]))
        mlp_out_matrix.move_to(np.array([residual_compute_block_spacing, -9, 0]))
        self.play(FadeOut(residual_matrix_1b), FadeIn(mlp_out_matrix), residual_matrix_1b.animate.move_to(np.array([residual_compute_block_spacing, -12, 0])), mlp_out_matrix.animate.move_to(np.array([residual_compute_block_spacing, -12, 0])), run_time=1, rate_func=linear)
        self.wait(1)
        a8 = Arrow(start=block_orig + np.array([residual_compute_block_spacing, -11, 0]), end=block_orig + np.array([residual_compute_block_spacing, -12.3, 0]), fill_color=WHITE, thickness=line_thickness, tip_width_ratio=0)
        a9 = Arrow(start=block_orig + np.array([residual_compute_block_spacing + line_padding, -12, 0]), end=block_orig + np.array([0.5, -12, 0]), fill_color=WHITE, thickness=line_thickness)
        self.add(a8, a9)
        a5 = Arrow(start=block_orig + np.array([0, -6.5, 0]), end=block_orig + np.array([0, -11.5, 0]), fill_color=WHITE, thickness=line_thickness)
        self.add(a5)
        c2 = circle_plus(circle_stroke_width=circle_stroke_width, plus_stroke_width=plus_stroke_width, overall_scale=0.6, position=block_orig + np.array([0, -12, 0]))
        self.add(c2)
        self.play(residual_matrix_1.animate.move_to(np.array([0, -12, 0])), run_time=2)
        self.wait()
        self.remove(residual_matrix_1b)
        self.play(mlp_out_matrix.animate.move_to(np.array([0, -12, 0])), run_time=2, rate_func=smooth)
        residual_matrix_2 = get_image_and_border(path='gemma_cached_images_dec_18_1/hook_resid_post_1.png', scale=1.5)
        residual_matrix_2.rotate(90 * DEGREES, np.array([1, 0, 0]))
        residual_matrix_2.move_to(np.array([0, -12, 0]))
        self.add(residual_matrix_2)
        self.remove(mlp_out_matrix)
        self.remove(residual_matrix_1)
        self.wait(1)
        self.play(self.frame.animate.reorient(-1, 71, 0, (1.53, -5.14, -1.39), 22.37))
        self.wait()
        top_tokens = {'_very': 0.0161, 'very': 0.0161, 'Very': 0.0161, '_Very': 0.0161, '_VERY': 0.016, 'VERY': 0.0159, '_très': 0.0158, '_muy': 0.0158, '_sehr': 0.0154, '_extremely': 0.0151}
        word_group, bar_group, prob_group = show_top_tokens(top_tokens)
        top_tokens_group = VGroup(word_group, bar_group, prob_group)
        top_tokens_group.rotate(90 * DEGREES, np.array([1, 0, 0]))
        top_tokens_group.scale(1.8)
        top_tokens_group.next_to(residual_matrix_1, LEFT, buff=2.2)
        self.add(word_group, bar_group, prob_group)
        arrow_3 = Arrow(start=residual_matrix_1.get_left(), end=top_tokens_group.get_right(), buff=0.4, thickness=8).set_color(YELLOW)
        arrow_3.rotate(90 * DEGREES, np.array([1, 0, 0]))
        self.add(arrow_3)
        self.wait(1)

class P30_P31(InteractiveScene):

    def construct(self):
        data = TOKENS_BY_LAYER
        cell_height = 0.4
        cell_width = 1.0
        table = VGroup()
        all_values = [value for d in data for value in d.values()]
        min_val = min(all_values)
        max_val = max(all_values)
        colormap_scale = 1.0
        cmap = plt.cm.viridis
        scaled_colormap_max = max_val * colormap_scale
        header_row = VGroup()
        layer_header = Text('Layer', font='Helvetica', font_size=20).set_color(CHILL_BROWN)
        layer_cell = Rectangle(height=cell_height, width=0.6 * cell_width, fill_opacity=0.0, stroke_width=0)
        layer_header_group = VGroup(layer_cell, layer_header)
        header_row.add(layer_header_group)
        predictions_header = Text('Top Next Token Predictions', font='Helvetica', font_size=20).set_color(CHILL_BROWN)
        predictions_cell = Rectangle(height=cell_height, width=cell_width * 10, fill_opacity=0.0, stroke_width=0)
        predictions_header_group = VGroup(predictions_cell, predictions_header)
        header_row.add(predictions_header_group)
        header_row.arrange(RIGHT, buff=0)
        for i in range(16):
            row = VGroup()
            index_cell = Rectangle(height=cell_height, width=0.6 * cell_width, fill_opacity=0.0, stroke_width=0)
            index_text = Text(str(i + 1), font_size=20, font='Helvetica').set_color(CHILL_BROWN)
            index_cell = VGroup(index_cell, index_text)
            row.add(index_cell)
            dict_items = list(data[i].items())[:10]
            for key, value in dict_items:
                cell = Rectangle(height=cell_height, width=cell_width, stroke_width=0)
                hex_color = rgb_to_hex(cmap(value / scaled_colormap_max)[:3])
                cell.set_fill(hex_color, opacity=0.7)
                word_text = Text(key.strip(), font_size=16, font='Helvetica')
                value_text = Text(f'{value:.4f}', font_size=9).set_color('#CCCCCC')
                text_group = VGroup(word_text, value_text).arrange(DOWN, buff=0.05)
                cell_group = VGroup(cell, text_group)
                row.add(cell_group)
            row.arrange(RIGHT, buff=0)
            table.add(row)
        table.arrange(DOWN, buff=0)
        line = Line(start=table.get_left(), end=table.get_right(), stroke_color=CHILL_BROWN, stroke_width=1).move_to(table.get_top(), aligned_edge=DOWN)
        header_row.next_to(line, UP, buff=0.1)
        full_visualization = VGroup(header_row, line, table)
        self.add(full_visualization)
        self.wait(1)
        self.play(full_visualization.animate.shift(RIGHT))
        residual_matrix_1 = get_image_and_border(path='gemma_cached_images_dec_19_1/hook_resid_post_1.png')
        residual_matrix_1.scale(0.35)
        residual_matrix_1.to_edge(LEFT, buff=0.5)
        residual_matrix_1.shift(2 * UP)
        residual_matrix_1_title = Text('Layer 1 Residual Stream', font='Myriad Pro', font_size=15).set_color(CHILL_BROWN)
        residual_matrix_1_title.next_to(residual_matrix_1, UP, buff=0.1)
        residual_matrix_2 = get_image_and_border(path='gemma_cached_images_dec_19_1/hook_resid_post_15.png')
        residual_matrix_2.scale(0.35)
        residual_matrix_2.to_edge(LEFT, buff=0.5)
        residual_matrix_2.shift(2 * DOWN)
        residual_matrix_2_title = Text('Layer 15 Residual Stream', font='Myriad Pro', font_size=15).set_color(CHILL_BROWN)
        residual_matrix_2_title.next_to(residual_matrix_2, UP, buff=0.1)
        arrow_1 = Arrow(start=residual_matrix_1.get_bottom(), end=residual_matrix_2.get_top(), buff=0.6, thickness=4, tip_width_ratio=3.5).set_color(CHILL_BROWN)
        self.add(residual_matrix_1, residual_matrix_2, residual_matrix_1_title, residual_matrix_2_title, arrow_1)
        self.wait(1)
        self.remove(residual_matrix_1, residual_matrix_2, residual_matrix_1_title, residual_matrix_2_title, arrow_1)
        table = VGroup()
        header_row = VGroup()
        layer_header = Text('Layer', font='Helvetica', font_size=20).set_color(CHILL_BROWN)
        layer_cell = Rectangle(height=cell_height, width=0.6 * cell_width, fill_opacity=0.0, stroke_width=0)
        layer_header_group = VGroup(layer_cell, layer_header)
        header_row.add(layer_header_group)
        predictions_header = Text('Top Next Token Predictions', font='Helvetica', font_size=20).set_color(CHILL_BROWN)
        predictions_cell = Rectangle(height=cell_height, width=cell_width * 10, fill_opacity=0.0, stroke_width=0)
        predictions_header_group = VGroup(predictions_cell, predictions_header)
        header_row.add(predictions_header_group)
        header_row.arrange(RIGHT, buff=0)
        for i in range(22):
            row = VGroup()
            index_cell = Rectangle(height=cell_height, width=0.6 * cell_width, fill_opacity=0.0, stroke_width=0)
            index_text = Text(str(i + 1), font_size=20, font='Helvetica').set_color(CHILL_BROWN)
            index_cell = VGroup(index_cell, index_text)
            row.add(index_cell)
            dict_items = list(data[i].items())[:10]
            for key, value in dict_items:
                cell = Rectangle(height=cell_height, width=cell_width, stroke_width=0)
                hex_color = rgb_to_hex(cmap(value / scaled_colormap_max)[:3])
                cell.set_fill(hex_color, opacity=0.7)
                word_text = Text(key.strip(), font_size=16, font='Helvetica')
                value_text = Text(f'{value:.4f}', font_size=9).set_color('#CCCCCC')
                text_group = VGroup(word_text, value_text).arrange(DOWN, buff=0.05)
                cell_group = VGroup(cell, text_group)
                row.add(cell_group)
            row.arrange(RIGHT, buff=0)
            table.add(row)
        table.arrange(DOWN, buff=0)
        line = Line(start=table.get_left(), end=table.get_right(), stroke_color=CHILL_BROWN, stroke_width=1).move_to(table.get_top(), aligned_edge=DOWN)
        header_row.next_to(line, UP, buff=0.1)
        full_visualization_2 = VGroup(header_row, line, table)
        full_visualization_2.scale(0.82)
        full_visualization_2.move_to(ORIGIN)
        self.play(full_visualization.animate.move_to(0.98 * UP).scale(0.82))
        self.remove(full_visualization)
        self.add(full_visualization_2)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0.08, -1.3, 0.0), 5.4))
        self.wait()

class P32(InteractiveScene):

    def construct(self):
        all_transformer_blocks = VGroup()
        transformer_block_lines = VGroup()
        for i in range(26):
            tb, tb_lines = get_transformer_block(block_orig=np.array([0, i * -14.5, 0]), attention_block_width=8, attention_block_height=6, attention_block_depth=1, mlp_block_width=8, mlp_block_height=6, mlp_block_depth=1)
            all_transformer_blocks.add(tb)
            transformer_block_lines.add(tb_lines)
        self.add(all_transformer_blocks)
        self.frame.reorient(-89, 59, 0, (47.24, -192.2, -24.03), 284.51)
        self.play(self.frame.animate.reorient(-35, 66, 0, (30.84, -266.0, -17.62), 62.17), run_time=4)
        for i in range(21, 26):
            self.remove(all_transformer_blocks[i])
        residual_compute_block_spacing = 11
        mlp_out_matrix = get_image_and_border(path='gemma_cached_images_dec_19_2/hook_mlp_out_21.png', scale=1.5)
        mlp_out_matrix.rotate(90 * DEGREES, np.array([1, 0, 0]))
        mlp_out_matrix.move_to(np.array([residual_compute_block_spacing, -14.5 * 20 - 12, 0]))
        self.add(mlp_out_matrix)
        self.play(self.frame.animate.reorient(-0.8890242898859254, 78.324221446455, -1.6896696745274932e-15, (11.4431, -260.7836, -8.4289), 45.285), run_time=2)
        self.wait()
        self.remove(all_transformer_blocks)
        self.wait()

class P33(InteractiveScene):

    def construct(self):
        top_tokens_default = {'important': 0.2021, 'much': 0.125, 'high': 0.1116, 'low': 0.108, 'questionable': 0.0948, 'poor': 0.0547, 'good': 0.0455, 'well': 0.0196, 'controversial': 0.0187, 'often': 0.0142}
        top_tokens_clamp = {'important': 0.2263, 'high': 0.125, 'much': 0.1136, 'low': 0.0902, 'questionable': 0.0757, 'good': 0.0572, 'poor': 0.0366, 'well': 0.0226, 'controversial': 0.0196, 'often': 0.0138}
        top_tokens_reverse_clamp = {'much': 0.1862, 'important': 0.151, 'low': 0.1136, 'questionable': 0.1066, 'poor': 0.0887, 'high': 0.0692, 'good': 0.0299, 'often': 0.0186, 'well': 0.0165, 'dependent': 0.0142}
        t = Text('The reliability of Wikipedia is very', font='Myriad Pro').set_color(CHILL_BROWN)
        t.scale(0.7)
        t.to_edge(LEFT, buff=0.5)
        t.shift(1.5 * UP)
        self.add(t)
        word_group, bar_group, prob_group = show_top_tokens(top_tokens_default, bar_length_scale=3, colormap_scale=3, word_bar_buffer=0.8, bar_prob_buffer=0.3)
        default = VGroup(word_group, bar_group, prob_group)
        default.next_to(t, RIGHT, buff=0.2, aligned_edge=TOP).shift(0.01 * DOWN)
        self.add(default)
        mlp_out_matrix = get_image_and_border(path='gemma_cached_images_dec_19_3/hook_mlp_out_21.png')
        mlp_out_matrix_colorbar = ImageMobject('gemma_cached_images_dec_19_3/hook_mlp_out_21_colorbar.png')
        mlp_out_matrix.scale(0.4).next_to(default, UP, buff=0.5)
        mlp_out_matrix_colorbar.scale(0.55).next_to(mlp_out_matrix, RIGHT, buff=0.1)
        self.add(mlp_out_matrix, mlp_out_matrix_colorbar)
        title_1 = Text('DEFAULT LAYER 21 OUT', font='Myriad Pro').set_color(CHILL_BROWN)
        title_1.scale(0.55)
        title_1.next_to(mlp_out_matrix, UP, buff=0.25)
        self.add(title_1)
        self.frame.reorient(0, 0, 0, (1.0, 0.29, 0.0), 10.0)
        self.wait()
        word_group, bar_group, prob_group = show_top_tokens(top_tokens_clamp, bar_length_scale=3, colormap_scale=3, word_bar_buffer=0.8, bar_prob_buffer=0.3)
        clamped = VGroup(word_group, bar_group, prob_group)
        clamped.next_to(default, RIGHT, buff=1.0, aligned_edge=TOP).shift(0.01 * DOWN)
        self.add(clamped)
        mlp_out_matrix = get_image_and_border(path='gemma_cached_images_dec_19_3/hook_mlp_out_clamped_21.png')
        mlp_out_matrix_colorbar = ImageMobject('gemma_cached_images_dec_19_3/hook_mlp_out_clamped_21_colorbar.png')
        mlp_out_matrix.scale(0.4).next_to(clamped, UP, buff=0.5)
        mlp_out_matrix_colorbar.scale(0.55).next_to(mlp_out_matrix, RIGHT, buff=0.1)
        self.add(mlp_out_matrix, mlp_out_matrix_colorbar)
        title_2 = Text('CLAMPED LAYER 21 OUT', font='Myriad Pro').set_color(CHILL_BROWN)
        title_2.scale(0.55)
        title_2.next_to(mlp_out_matrix, UP, buff=0.25)
        self.add(title_2)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (2.71, 0.62, 0.0), 10.89), run_time=2)
        word_group, bar_group, prob_group = show_top_tokens(top_tokens_reverse_clamp, bar_length_scale=3, colormap_scale=3, word_bar_buffer=1.4, bar_prob_buffer=0.3)
        reverse_clamped = VGroup(word_group, bar_group, prob_group)
        reverse_clamped.next_to(clamped, RIGHT, buff=1.0, aligned_edge=TOP).shift(0.01 * DOWN)
        self.add(reverse_clamped)
        mlp_out_matrix = get_image_and_border(path='gemma_cached_images_dec_19_3/hook_mlp_out_reverse_clamped_21.png')
        mlp_out_matrix_colorbar = ImageMobject('gemma_cached_images_dec_19_3/hook_mlp_out_reverse_clamped_21_colorbar.png')
        mlp_out_matrix.scale(0.4).next_to(reverse_clamped, UP, buff=0.5)
        mlp_out_matrix_colorbar.scale(0.55).next_to(mlp_out_matrix, RIGHT, buff=0.1)
        self.add(mlp_out_matrix, mlp_out_matrix_colorbar)
        title_3 = Text('REVERSE CLAMPED LAYER 21 OUT', font='Myriad Pro').set_color(CHILL_BROWN)
        title_3.scale(0.55)
        title_3.next_to(mlp_out_matrix, UP, buff=0.25)
        self.add(title_3)
        self.wait()

class P35(InteractiveScene):

    def construct(self):
        all_transformer_blocks = VGroup()
        transformer_block_lines = VGroup()
        for i in range(26):
            tb, tb_lines = get_transformer_block(block_orig=np.array([0, i * -14.5, 0]), attention_block_width=8, attention_block_height=6, attention_block_depth=1, mlp_block_width=8, mlp_block_height=6, mlp_block_depth=1)
            all_transformer_blocks.add(tb)
            transformer_block_lines.add(tb_lines)
        self.add(all_transformer_blocks)
        self.frame.reorient(-89, 59, 0, (47.24, -192.2, -24.03), 284.51)
        self.wait(1)
        self.play(self.frame.animate.reorient(-35, 66, 0, (30.84, -266.0, -17.62), 62.17), run_time=4)
        for i in range(21, 26):
            self.remove(all_transformer_blocks[i])
        residual_compute_block_spacing = 11
        mlp_out_matrix = get_image_and_border(path='gemma_cached_images_dec_19_2/hook_mlp_out_21.png', scale=1.5)
        mlp_out_matrix.rotate(90 * DEGREES, np.array([1, 0, 0]))
        mlp_out_matrix.move_to(np.array([residual_compute_block_spacing, -14.5 * 20 - 12, 0]))
        self.add(mlp_out_matrix)
        self.wait()
        self.play(self.frame.animate.reorient(-0.8890242898859254, 78.324221446455, -1.6896696745274932e-15, (11.4431, -260.7836, -8.4289), 45.285), run_time=2)
        self.wait()

class P36(InteractiveScene):

    def construct(self):
        words = top_activating_words
        activations = top_activating_word_activations
        flat_activations = [item for sublist in activations for item in sublist]
        min_act = min(flat_activations)
        max_act = max(flat_activations)
        normalized_activations = [[(x - min_act) / (max_act - min_act) for x in row] for row in activations]
        all_line_groups = VGroup()
        for line_index in range(1, 11):
            text_line = Text(''.join(words[line_index]).replace('\n', ' '), font='Helvetica').scale(0.5).set_color('#000000')
            starting_char_index = 0
            line_highlights = VGroup()
            for i, word in enumerate(words[line_index]):
                num_chars = len(''.join(word).replace('\n', ' ').replace(' ', ''))
                word_chars = text_line[starting_char_index:starting_char_index + num_chars]
                activation = normalized_activations[line_index][i]
                color = rgb_to_hex(cm.viridis_r(activation)[:3])
                background = Rectangle(height=0.3, width=word_chars.get_width() + 0.0, fill_opacity=0.6, stroke_width=0)
                background.set_fill(color)
                background.move_to([word_chars.get_center()[0], 0, 0])
                line_highlights.add(background)
                starting_char_index += num_chars
            line_group = VGroup(line_highlights, text_line)
            line_group.move_to(DOWN * (5 + 1.0 * line_index))
            all_line_groups.add(line_group)
        title_1 = Text('Gemma 2B Layer 21 MLP Neuron 1393 Top Negative Activating Examples from The Pile Dataset', font='Myriad Pro').set_color(CHILL_BROWN)
        title_1.scale(0.55)
        title_1.to_edge(UP, buff=0.5)
        self.add(title_1)
        color_bar = ImageMobject(data_dir + '/top_activating_example_colorbar_dec_19_2.png')
        color_bar.scale(0.65)
        color_bar.to_edge(LEFT, buff=0.4)
        self.add(color_bar)
        color_bar_title = Text('Activation \n Value', font='Myriad Pro').set_color(CHILL_BROWN)
        color_bar_title.scale(0.45)
        color_bar_title.next_to(color_bar, DOWN, buff=0.1)
        color_bar_title.shift(0.2 * LEFT)
        self.add(color_bar_title)
        self.wait()
        self.play(*[all_line_groups[line_index].animate.move_to(UP * (3 - 0.6 * (line_index + 1))) for line_index in range(10)], run_time=10)
        self.wait(30)