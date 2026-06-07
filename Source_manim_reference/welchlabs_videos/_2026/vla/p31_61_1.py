from manimlib import *
from tqdm import tqdm
from pathlib import Path
import matplotlib.pyplot as plt
import colorsys
import shutil
import tempfile
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
BLUE2 = '#00AEEF'
GREEN = '#00a14b'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
CYAN = '#00FFFF'
MAGENTA = '#FF00FF'
PINK = '#FAD0E2'
svg_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/vla/graphics/to_manim/')
hacking_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/vla/hackin')
SATURATION_BOOST = 1.5
MIN_SATURATION = 0.2
MIN_VALUE = 0.5

def patch_bright_average(img, exponent=2.0):
    patches = img.reshape(16, 14, 16, 14, 3)
    chroma = patches.max(axis=-1, keepdims=True) - patches.min(axis=-1, keepdims=True)
    weights = chroma ** exponent / (chroma ** exponent).sum(axis=(1, 3), keepdims=True)
    return (patches * weights).sum(axis=(1, 3))

def boost_colors_hsv(colors, saturation_boost=1.0, min_saturation=0.0, min_value=0.0):
    colors = np.asarray(colors, dtype=np.float32)
    out = np.empty_like(colors)
    for i in range(len(colors)):
        h, s, v = colorsys.rgb_to_hsv(*colors[i])
        s = min(1.0, s * saturation_boost)
        s = max(s, min_saturation)
        v = max(v, min_value)
        out[i] = colorsys.hsv_to_rgb(h, s, v)
    return out

class P61a(InteractiveScene):

    def construct(self):
        svgs_to_skip = [0, 2, 3, 8, 12, 13, 20, 21]
        svg_files = list(sorted(svg_dir.glob('*.svg')))
        all_svgs = Group()
        for i, svg_file in enumerate(svg_files):
            if i in svgs_to_skip:
                continue
            svg_image = SVGMobject(str(svg_file))
            svg_image.scale(3.9)
            all_svgs.add(svg_image[1:])
        self.frame.reorient(0, 0, 0, (4.04, -2.31, 0.0), 13.17)
        FRAME_IDX = 160
        total_height = 2.72
        grid_n = 16
        patch_size = total_height / grid_n
        gap_factor = 0.12
        vertical_spacing = 0.2
        UP_SHIFT = np.array([0, 0.5, 0])
        patch_centers = [[-5.23, 2.58, 0], [-5.23, 0.175, 0], [-5.23, -2.22, 0]]
        pixel_squares = Group()
        for k, image_name in enumerate(['base_0_rgb', 'left_wrist_0_rgb', 'right_wrist_0_rgb']):
            pixel_squares.add(Group())
            patch_dir = hacking_dir / f'p35/{FRAME_IDX}/{image_name}'
            for i in range(2, 14):
                for j in range(grid_n):
                    patch_mob = ImageMobject(str(patch_dir / f'patch_{i}_{j}.png'))
                    patch_mob.set_height(patch_size)
                    patch_mob.set_width(patch_size, stretch=True)
                    x_pos = (j - grid_n / 2 + 0.5) * patch_size * (1 + gap_factor)
                    y_pos = -(i - grid_n / 2 + 0.5) * patch_size * (1 + gap_factor)
                    patch_mob.move_to([x_pos, y_pos, 0])
                    pixel_squares[-1].add(patch_mob)
            pixel_squares[k].move_to(patch_centers[k])
        siglip_1 = all_svgs[2][:13]
        siglip_2 = all_svgs[2][13:26]
        siglip_3 = all_svgs[2][26:39]
        image_encoders_label = all_svgs[2][39:]
        siglip_1.scale(1.1).move_to([-3.0, 2.6, 0])
        siglip_2.scale(1.1).move_to([-3.0, 0.2, 0])
        siglip_3.scale(1.1).move_to([-3.0, -2.1, 0])
        image_encoders_label.scale(1.1).move_to([-3.0, 3.5, 0])
        lil_arrows_pair_1 = all_svgs[5]
        lil_arrows_pair_2 = lil_arrows_pair_1.copy()
        lil_arrows_pair_3 = lil_arrows_pair_1.copy()
        lil_arrows_pair_1.move_to([-3.0, 2.57, 0])
        lil_arrows_pair_2.move_to([-3.0, 0.18, 0])
        lil_arrows_pair_3.move_to([-3.0, -2.18, 0])
        self.add(pixel_squares, siglip_1, siglip_2, siglip_3, image_encoders_label, lil_arrows_pair_1, lil_arrows_pair_2, lil_arrows_pair_3)
        self.wait(20)
        self.embed()

class P61b(InteractiveScene):

    def construct(self):
        svgs_to_skip = [0, 2, 3, 8, 12, 13, 20, 21]
        svg_files = list(sorted(svg_dir.glob('*.svg')))
        all_svgs = Group()
        for i, svg_file in enumerate(svg_files):
            if i in svgs_to_skip:
                continue
            svg_image = SVGMobject(str(svg_file))
            svg_image.scale(3.9)
            all_svgs.add(svg_image[1:])
        self.frame.reorient(0, 0, 0, (4.04, -2.31, 0.0), 13.17)
        FRAME_IDX = 170
        total_height = 2.72
        grid_n = 16
        patch_size = total_height / grid_n
        gap_factor = 0.12
        vertical_spacing = 0.2
        UP_SHIFT = np.array([0, 0.5, 0])
        patch_centers = [[-5.23, 2.58, 0], [-5.23, 0.175, 0], [-5.23, -2.22, 0]]
        pixel_squares = Group()
        for k, image_name in enumerate(['base_0_rgb', 'left_wrist_0_rgb', 'right_wrist_0_rgb']):
            pixel_squares.add(Group())
            patch_dir = hacking_dir / f'p35/{FRAME_IDX}/{image_name}'
            for i in range(2, 14):
                for j in range(grid_n):
                    patch_mob = ImageMobject(str(patch_dir / f'patch_{i}_{j}.png'))
                    patch_mob.set_height(patch_size)
                    patch_mob.set_width(patch_size, stretch=True)
                    x_pos = (j - grid_n / 2 + 0.5) * patch_size * (1 + gap_factor)
                    y_pos = -(i - grid_n / 2 + 0.5) * patch_size * (1 + gap_factor)
                    patch_mob.move_to([x_pos, y_pos, 0])
                    pixel_squares[-1].add(patch_mob)
            pixel_squares[k].move_to(patch_centers[k])
        siglip_1 = all_svgs[2][:13]
        siglip_2 = all_svgs[2][13:26]
        siglip_3 = all_svgs[2][26:39]
        image_encoders_label = all_svgs[2][39:]
        siglip_1.scale(1.1).move_to([-3.0, 2.6, 0])
        siglip_2.scale(1.1).move_to([-3.0, 0.2, 0])
        siglip_3.scale(1.1).move_to([-3.0, -2.1, 0])
        image_encoders_label.scale(1.1).move_to([-3.0, 3.5, 0])
        lil_arrows_pair_1 = all_svgs[5]
        lil_arrows_pair_2 = lil_arrows_pair_1.copy()
        lil_arrows_pair_3 = lil_arrows_pair_1.copy()
        lil_arrows_pair_1.move_to([-3.0, 2.57, 0])
        lil_arrows_pair_2.move_to([-3.0, 0.18, 0])
        lil_arrows_pair_3.move_to([-3.0, -2.18, 0])
        self.add(pixel_squares, siglip_1, siglip_2, siglip_3, image_encoders_label, lil_arrows_pair_1, lil_arrows_pair_2, lil_arrows_pair_3)
        self.wait(20)
        self.embed()

class P52_61(InteractiveScene):

    def construct(self):
        svgs_to_skip = [0, 2, 3, 8, 12, 13, 20, 21]
        svg_files = list(sorted(svg_dir.glob('*.svg')))
        all_svgs = Group()
        for i, svg_file in enumerate(svg_files):
            if i in svgs_to_skip:
                continue
            svg_image = SVGMobject(str(svg_file))
            svg_image.scale(3.9)
            all_svgs.add(svg_image[1:])
        self.frame.reorient(0, 0, 0, (-2.03, -6.66, 0.0), 5.33)
        FRAME_IDX = 150
        total_height = 2.72
        grid_n = 16
        patch_size = total_height / grid_n
        gap_factor = 0.12
        vertical_spacing = 0.2
        patch_centers = [[-5.23, 2.58, 0], [-5.23, 0.175, 0], [-5.23, -2.22, 0]]
        pixel_squares = Group()
        for k, image_name in enumerate(['base_0_rgb', 'left_wrist_0_rgb', 'right_wrist_0_rgb']):
            pixel_squares.add(Group())
            patch_dir = hacking_dir / f'p35/{FRAME_IDX}/{image_name}'
            for i in range(2, 14):
                for j in range(grid_n):
                    patch_mob = ImageMobject(str(patch_dir / f'patch_{i}_{j}.png'))
                    patch_mob.set_height(patch_size)
                    patch_mob.set_width(patch_size, stretch=True)
                    x_pos = (j - grid_n / 2 + 0.5) * patch_size * (1 + gap_factor)
                    y_pos = -(i - grid_n / 2 + 0.5) * patch_size * (1 + gap_factor)
                    patch_mob.move_to([x_pos, y_pos, 0])
                    pixel_squares[-1].add(patch_mob)
            pixel_squares[k].move_to(patch_centers[k])
        siglip_1 = all_svgs[2][:13]
        siglip_2 = all_svgs[2][13:26]
        siglip_3 = all_svgs[2][26:39]
        image_encoders_label = all_svgs[2][39:]
        siglip_1.scale(1.1).move_to([-3.0, 2.6, 0])
        siglip_2.scale(1.1).move_to([-3.0, 0.2, 0])
        siglip_3.scale(1.1).move_to([-3.0, -2.1, 0])
        image_encoders_label.scale(1.1).move_to([-3.0, 3.5, 0])
        lil_arrows_pair_1 = all_svgs[5]
        lil_arrows_pair_2 = lil_arrows_pair_1.copy()
        lil_arrows_pair_3 = lil_arrows_pair_1.copy()
        lil_arrows_pair_1.move_to([-3.0, 2.57, 0])
        lil_arrows_pair_2.move_to([-3.0, 0.18, 0])
        lil_arrows_pair_3.move_to([-3.0, -2.18, 0])
        all_svgs[6].shift([0.08, 0, 0])
        bracket_remnants = all_svgs[6][1:7]
        embedding_brackets_2 = all_svgs[7][2:8]
        embedding_brackets_2.shift([0.08, 0, 0])
        blue_text_embedding_arrow = all_svgs[7][:2]
        blue_text_embedding_arrow.shift([0.08, 0, 0])
        blue_text_embedding_arrow.shift([-0.1, 0.05, 0])
        blue_text_embedding_arrow.set_color(BLUE)
        embedding_out_arrow = all_svgs[7][-2:]
        embedding_out_arrow.move_to([-0.64, 0.28, 0])
        overhead_im = np.load(hacking_dir / 'p35/150_overhead.npy')
        left_im = np.load(hacking_dir / 'p35/150_left.npy')
        right_im = np.load(hacking_dir / 'p35/150_right.npy')
        overhead_colors = patch_bright_average(overhead_im, exponent=2.0).reshape(-1, 3)
        left_colors = patch_bright_average(left_im, exponent=2.0).reshape(-1, 3)
        right_colors = patch_bright_average(right_im, exponent=2.0).reshape(-1, 3)

        def make_embedding_row(color_arr, patch_index, y_pos):
            bc = rgb_to_color(boost_colors_hsv(color_arr[patch_index + 32].reshape(1, 3) / 255.0, saturation_boost=SATURATION_BOOST, min_saturation=MIN_SATURATION, min_value=MIN_VALUE).ravel())
            r = Rectangle(width=1.1, height=0.03)
            r.set_fill(bc, opacity=1).set_stroke(width=0)
            r.move_to([-1.5, y_pos, 0])
            return r
        embedding_rows_1 = VGroup()
        for i, pi in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8]):
            embedding_rows_1.add(make_embedding_row(overhead_colors, pi, 3.15 - i * vertical_spacing))
        ellipsis_dots = VGroup(*[Dot(radius=0.025).set_color(CHILL_BROWN) for _ in range(3)])
        ellipsis_dots.arrange(DOWN, buff=0.035)
        ellipsis_dots.next_to(embedding_rows_1[-1], DOWN, buff=0.15)
        embedding_rows_2 = VGroup()
        for i, pi in enumerate([82, 83, 84, 85, 86, 87, 88, 89, 90, 91]):
            embedding_rows_2.add(make_embedding_row(left_colors, pi, 1.0 - i * vertical_spacing))
        ellipsis_dots_2 = VGroup(*[Dot(radius=0.025).set_color(CHILL_BROWN) for _ in range(3)])
        ellipsis_dots_2.arrange(DOWN, buff=0.035)
        ellipsis_dots_2.next_to(embedding_rows_2[-1], DOWN, buff=0.1)
        embedding_rows_3 = VGroup()
        for i, pi in enumerate([186, 186, 187, 188, 189, 190, 191]):
            embedding_rows_3.add(make_embedding_row(right_colors, pi, -1.3 - i * vertical_spacing))
        embedding_rows_4 = VGroup()
        for i in range(4):
            l = Line(LEFT * 0.55, RIGHT * 0.55)
            l.set_stroke(BLUE, width=4)
            l.move_to([-1.5, -2.75 - i * vertical_spacing, 0])
            embedding_rows_4.add(l)
        tokenized_prompt = Text('Un  cap  the  pen', font='Myriad Pro', weight='bold', font_size=25)
        tokenized_prompt.set_color(BLUE)
        tokenized_prompt.set_stroke(BLUE, width=0.1)
        tokenized_prompt.move_to([-5.3, -3.64, 0])
        full_gemma = Group(all_svgs[8], all_svgs[9], all_svgs[10], all_svgs[11], all_svgs[12], all_svgs[13])
        full_gemma.shift([0.2, 0, 0])
        full_gemma_copy = Group(all_svgs[8].copy(), all_svgs[9].copy(), all_svgs[10].copy(), all_svgs[45], all_svgs[46], all_svgs[13].copy())
        all_svgs[26].shift([0.19, 0, 0])
        gemma = Group(all_svgs[8], all_svgs[9], all_svgs[10], all_svgs[13], all_svgs[26])
        action_expert_full = full_gemma.copy()
        action_expert_full_copy = full_gemma_copy.copy()
        all_attn_patterns = []
        for layer in range(18):
            all_attn_patterns.append([])
            for head in range(8):
                im = ImageMobject(str(hacking_dir / f'p47/attn_pattern_{layer}_{head}.png'))
                all_attn_patterns[-1].append(im)
        attn_patterns_to_show = Group()
        for i in range(8):
            all_attn_patterns[0][i].scale(0.096).move_to([0.25, 1.5 - 0.358 * i, 0])
            attn_patterns_to_show.add(all_attn_patterns[0][i])
        for i in range(8):
            if i == 6:
                continue
            all_attn_patterns[1][i].scale(0.096).move_to([2.65, 1.5 - 0.358 * i, 0])
            attn_patterns_to_show.add(all_attn_patterns[1][i])
        for i in range(8):
            all_attn_patterns[-1][i].scale(0.096).move_to([5.05, 1.5 - 0.358 * i, 0])
            attn_patterns_to_show.add(all_attn_patterns[-1][i])
        attn_pattern = ImageMobject(str(hacking_dir / 'p44/attn_pattern_1.png'))
        attn_pattern.scale(1.3 * 0.41 * 0.18)
        attn_pattern.move_to([2.65, 1.5 - 0.358 * 6, 0])
        all_svgs[27].move_to([-5.2, -6, 0])
        all_svgs[28].move_to([-5.2, -6, 0])
        all_svgs[29].move_to([-3.05, -4.7, 0])
        all_svgs[30].move_to([-1.53, -6.7, 0])
        all_svgs[31].move_to([-4.25, -6.765, 0])
        arm_img = ImageMobject(str(hacking_dir / 'arm_1.png'))
        arm_img.scale(0.52).move_to([-4.6, -5.97, 0])
        arm_img_flipped = ImageMobject(str(hacking_dir / 'arm_1_flipped.png'))
        arm_img_flipped.scale(0.52).move_to([-5.78, -5.97, 0])
        embedding_rows_action_expert = VGroup()
        for i in range(20):
            if i == 9:
                dots = VGroup(*[Dot(radius=0.02).set_color(CHILL_BROWN) for _ in range(3)])
                dots.arrange(DOWN, buff=0.03)
                dots.next_to(embedding_rows_action_expert[-1], DOWN, buff=0.09)
                embedding_rows_action_expert.add(dots)
                continue
            r = Rectangle(width=1.1, height=0.03)
            r.set_fill(RED if i == 0 else PINK, opacity=1)
            r.set_stroke(width=0)
            r.move_to([-1.5, -4.7 - i * vertical_spacing, 0])
            embedding_rows_action_expert.add(r)
        self.add(pixel_squares, siglip_1, siglip_2, siglip_3, image_encoders_label, lil_arrows_pair_1, lil_arrows_pair_2, lil_arrows_pair_3, bracket_remnants, embedding_brackets_2, blue_text_embedding_arrow, embedding_out_arrow, embedding_rows_1, ellipsis_dots, embedding_rows_2, ellipsis_dots_2, embedding_rows_3, embedding_rows_4, tokenized_prompt, gemma, attn_patterns_to_show, attn_pattern, all_svgs[27], all_svgs[28], all_svgs[29], all_svgs[30], all_svgs[31], arm_img, arm_img_flipped, embedding_rows_action_expert)
        self.remove(all_svgs[26])
        self.add(all_svgs[26])
        diffusion_images = Group()
        for i in range(11):
            im = ImageMobject(str(hacking_dir / ('p51b/' + str(i).zfill(2) + '.png')))
            diffusion_images.add(im)
        action_expert_box = RoundedRectangle(width=1.9, height=1.5, corner_radius=0.1, stroke_color=CHILL_BROWN, stroke_width=2, fill_opacity=0)
        manual_action_expert_box = all_svgs[4][-1].copy()
        manual_action_expert_box.scale(0.6)
        manual_action_expert_box.set_color(CHILL_BROWN)
        action_expert_label = Text('ACTION EXPERT', font='Myriad Pro', weight='bold', font_size=22)
        action_expert_label.set_color(CHILL_BROWN)
        action_expert_label.move_to(manual_action_expert_box)
        action_expert_label.shift([0, -0.05, 0])
        action_expert_box_group = Group(manual_action_expert_box, action_expert_label)
        action_expert_box_group.move_to([0.57, -6.45, 0])
        all_svgs[33].scale(0.7)
        all_svgs[33].move_to([-4.2, -6.9, 0])
        all_svgs[34].move_to([0.85, -6.5, 0])
        lil_arrow_2 = all_svgs[34][0]
        lil_arrow_2b = all_svgs[34][1]
        lil_arrow_2b.move_to([1.75, -6.5, 0])
        diffusion_images.scale(0.19)
        diffusion_images[0].move_to([-5.18, -8.0, 0])
        diffusion_images[1].move_to([3.53, -6.5, 0])
        all_svgs[35].move_to([3.2, -6.75, 0])
        all_svgs[35][5:].move_to([3.5, -7.05, 0])
        diffusion_images_copy = diffusion_images.copy()
        diffusion_images_copy_2 = diffusion_images.copy()
        diffusion_images_copy_3 = diffusion_images.copy()
        diffusion_images_copy_4 = diffusion_images.copy()
        self.remove(all_svgs[31])
        self.add(action_expert_box_group)
        self.add(all_svgs[33])
        self.add(diffusion_images[0])
        self.add(lil_arrow_2, lil_arrow_2b)
        self.frame.reorient(0, 0, 0, (-0.88, -7.24, 0.0), 6.82)
        self.wait()
        self.play(FadeIn(diffusion_images[1]), FadeIn(all_svgs[35]), run_time=3)
        self.wait()
        self.play(diffusion_images[1].animate.move_to(diffusion_images[0]), run_time=4)
        diffusion_images[1].set_opacity(0.5)
        diffusion_images[2].move_to([3.53, -6.5, 0])
        self.play(FadeIn(diffusion_images[2]), run_time=2)
        self.play(diffusion_images[2].animate.move_to(diffusion_images[0]), run_time=4)
        diffusion_images[2].set_opacity(0.2)
        self.remove(diffusion_images[2])
        self.add(diffusion_images[2])
        diffusion_images[3].move_to([3.53, -6.5, 0])
        self.play(FadeIn(diffusion_images[3]), run_time=2)
        tmp_diffusion_images = Group()
        for i in range(3, 10):
            tmp_1 = diffusion_images[i].copy()
            tmp_1.move_to([-5.18, -8.0, 0])
            tmp_diffusion_images.add(tmp_1)
            diffusion_images[i + 1].move_to([3.53, -6.5, 0])
            self.add(tmp_1, diffusion_images[i + 1])
            self.wait(0.5)
        action_expert_group_1 = Group(all_svgs[27], all_svgs[28], all_svgs[29], all_svgs[30], all_svgs[33], all_svgs[34], arm_img, arm_img_flipped, tmp_diffusion_images, embedding_rows_action_expert)
        gemma_group = Group(gemma, attn_patterns_to_show, attn_pattern)
        gemma_group.scale(1.5)
        gemma_group.move_to([5.1, 0.6, 0])
        all_svgs[8].set_color(BLUE2)
        action_expert_full.scale(1.5)
        action_expert_full.move_to([5.1, -5.4, 0])
        action_expert_full_2 = Group(*[action_expert_full[i] for i in [1, 2, 3, 4]])
        action_expert_full_copy[3].shift([0.2, 0, 0])
        action_expert_full_copy[4].shift([0.2, 0, 0])
        action_expert_full_copy.scale(1.5)
        action_expert_full_copy.move_to([5.1, -5.4, 0])
        all_svgs[36].scale([1.5, 1.4, 1])
        all_svgs[36].move_to([5.1, -5.5, 0])
        final_actions_text = Text('ACTIONS', font='Myriad Pro', weight='bold', font_size=26)
        final_actions_text.set_color(PINK)
        final_actions_text.move_to([12.4, -5.8, 0])
        self.remove(diffusion_images[:10])
        self.wait()
        self.remove(all_svgs[35])
        self.play(ReplacementTransform(action_expert_box_group[0], all_svgs[36][0]), action_expert_label.animate.scale(1.25).set_color(YELLOW).move_to([4.95, -8.28, 0]), action_expert_group_1.animate.shift([0, 0.5, 0]), self.frame.animate.reorient(0, 0, 0, (4.34, -2.34, 0.0), 13.0), all_svgs[34][1].animate.move_to([10.8, -5.2, 0]), diffusion_images[10].animate.move_to([12.4, -5.2, 0]), run_time=7)
        self.add(final_actions_text)
        self.wait()
        self.play(Write(action_expert_full_2[0]), Write(action_expert_full_2[1]), Write(action_expert_full_2[2]), Write(action_expert_full_2[3]), run_time=6)
        self.play(self.frame.animate.reorient(0, 0, 0, (5.13, -5.51, 0.0), 6.41), run_time=6)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (4.34, -2.34, 0.0), 13.0), run_time=6)
        self.wait()
        queries = Group()
        keys = Group()
        values = Group()
        attn_dots = VGroup()
        q_spacing = 0.135
        for i in range(11):
            q = ImageMobject(str(hacking_dir / ('p40_1/queries_' + str(i).zfill(2) + '.png')))
            q.scale(0.022)
            q.move_to([3.5, 2.8 - i * q_spacing, 0])
            queries.add(q)
            if i == 1 or i == 6:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(q)
                attn_dots.add(e)
        for i in range(11):
            k = ImageMobject(str(hacking_dir / ('p40_1/keys_' + str(i).zfill(2) + '.png')))
            k.scale(0.022)
            k.move_to([3.5, 1.0 - i * q_spacing, 0])
            keys.add(k)
            if i == 1 or i == 6:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(k)
                attn_dots.add(e)
        for i in range(11):
            v = ImageMobject(str(hacking_dir / ('p40_1/values_' + str(i).zfill(2) + '.png')))
            v.scale(0.022)
            v.move_to([3.5, -0.8 - i * q_spacing, 0])
            values.add(v)
            if i == 1 or i == 6:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(v)
                attn_dots.add(e)
        all_svgs[17].next_to(q, DOWN, buff=0.05)
        all_svgs[18].next_to(k, DOWN, buff=0.05)
        all_svgs[19].next_to(v, DOWN, buff=0.05)
        all_svgs[37].move_to([0.2, 0.3, 0])
        all_svgs[14].scale([0.95, 0.77, 1])
        all_svgs[14].move_to([2.88, 0.3, 0])
        gemma_h6_border = gemma_group[0][4][50].copy()
        self.add(gemma_h6_border)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (5.15, 0.71, 0.0), 7.01), run_time=4)
        self.remove(final_actions_text)
        gemma_attn_head_group = Group(all_svgs[37], queries, all_svgs[17], keys, all_svgs[18], values, all_svgs[19], attn_dots)
        gemma_attn_head_group.scale(0.08)
        gemma_attn_head_group.move_to([4.25, -0.48, 0])
        self.wait()
        self.play(FadeOut(gemma_group), FadeIn(gemma_attn_head_group), run_time=3)
        self.play(ReplacementTransform(gemma_h6_border, all_svgs[14][-1]), gemma_attn_head_group.animate.scale(1.0 / 0.08).move_to([2.7000403, 0.22694729, 0.0]), run_time=5)
        lil_arrow_2.shift([-0.05, 0, 0])
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (5.26, -5.43, 0.0), 6.99), run_time=4)
        action_expert_h6_border = action_expert_full_2[3][0].copy()
        self.add(action_expert_h6_border)
        action_expert_h6_border_copy = action_expert_h6_border.copy()
        action_expert_attn_head_border = all_svgs[14][-1].copy()
        action_expert_attn_head_border.move_to([2.88, -5.5, 0])
        action_expert_qkv_flow = all_svgs[38]
        action_expert_qkv_flow.move_to([0.2, -5.5, 0])
        queries_ae = Group()
        keys_ae = Group()
        values_ae = Group()
        attn_dots_ae = VGroup()
        q_spacing = 0.135
        for i in range(7):
            q = ImageMobject(str(hacking_dir / ('p58/queries_' + str(i).zfill(2) + '.png')))
            q.scale(0.022)
            q.move_to([3.5, -i * q_spacing, 0])
            queries_ae.add(q)
            if i == 3:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(q)
                attn_dots_ae.add(e)
        for i in range(7):
            k = ImageMobject(str(hacking_dir / ('p58/keys_' + str(i).zfill(2) + '.png')))
            k.scale(0.022)
            k.move_to([3.5, -i * q_spacing, 0])
            keys_ae.add(k)
            if i == 3:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(k)
                attn_dots_ae.add(e)
        for i in range(7):
            v = ImageMobject(str(hacking_dir / ('p58/values_' + str(i).zfill(2) + '.png')))
            v.scale(0.022)
            v.move_to([3.5, -i * q_spacing, 0])
            values_ae.add(v)
            if i == 3:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(v)
                attn_dots_ae.add(e)
        queries_ae.move_to([3.5, -3.7, 0])
        attn_dots_ae[0].move_to([3.5, -3.7, 0])
        keys_ae.move_to([3.5, -5.5, 0])
        attn_dots_ae[1].move_to([3.5, -5.5, 0])
        values_ae.move_to([3.5, -7.3, 0])
        attn_dots_ae[2].move_to([3.5, -7.3, 0])
        all_svgs[39].scale(0.88)
        all_svgs[39].move_to([3.5, -4.3, 0])
        all_svgs[40].scale(0.88)
        all_svgs[40].move_to([3.5, -6.1, 0])
        all_svgs[41].scale(0.88)
        all_svgs[41].move_to([3.5, -7.9, 0])
        all_svgs[42].scale(0.89)
        all_svgs[42].move_to([6.08, -5.5, 0])
        ae_attn_head_group = Group(action_expert_qkv_flow, queries_ae, keys_ae, values_ae, attn_dots_ae, all_svgs[39], all_svgs[40], all_svgs[41])
        self.wait()
        ae_attn_head_group.scale(0.08)
        ae_attn_head_group.move_to([4.3, -6.38, 0])
        self.wait()
        self.play(FadeOut(action_expert_full_2), FadeOut(action_expert_label), FadeOut(all_svgs[36][0]), FadeOut(all_svgs[34][1]), FadeOut(diffusion_images[10]), FadeIn(ae_attn_head_group), run_time=2)
        self.wait()
        self.play(ReplacementTransform(action_expert_h6_border, action_expert_attn_head_border), ae_attn_head_group.animate.scale(1 / 0.08).move_to([2.7, -5.6124, 0.0]), self.frame.animate.reorient(0, 0, 0, (-0.12, -5.59, 0.0), 7.51), run_time=5)
        self.wait()
        self.play(Write(all_svgs[42]), self.frame.animate.reorient(0, 0, 0, (3.41, -5.6, 0.0), 5.31), run_time=5)
        self.wait()
        self.play(FadeOut(all_svgs[42]), run_time=2)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-0.12, -5.59, 0.0), 7.51), run_time=5)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (4.14, -2.4, 0.0), 12.75), run_time=6)
        keys_to_move = Group(keys.copy(), attn_dots[2].copy(), attn_dots[3].copy())
        values_to_move = Group(values.copy(), attn_dots[4].copy(), attn_dots[5].copy())
        self.add(keys_to_move)
        self.add(values_to_move)
        self.wait()
        self.play(keys_to_move.animate.move_to([9, 0.325, 0]), values_to_move.animate.move_to([9, -1.474, 0]), run_time=4)
        WV_box = action_expert_qkv_flow[33:]
        all_svgs[43].scale(0.89)
        all_svgs[43].move_to([3.49996001, -7.58181244, 0.0])
        all_svgs[44].scale(0.89)
        all_svgs[44].move_to([3.5, -10.48167058, 0.0])
        self.wait()
        self.remove(all_svgs[40])
        self.remove(all_svgs[41])
        self.play(keys_to_move.animate.move_to([9, -6.717, 0]), values_to_move.animate.move_to([9, -9.62, 0]), values_ae.animate.move_to([3.5, -8.4, 0.0]), action_expert_attn_head_border.animate.scale([1, 1.35, 1]).move_to([2.88, -6.89, 0]), WV_box.animate.move_to([0.416, -8.4, 0]), action_expert_qkv_flow[31].animate.scale([1.0, 1.8, 1.0]).move_to([-0.2478, -6.83, 0]), action_expert_qkv_flow[32].animate.move_to([-0.134, -8.4, 0]), self.frame.animate.reorient(0, 0, 0, (5.87, -6.61, 0.0), 8.18), run_time=6)
        self.play(keys_to_move.animate.next_to(keys_ae, DOWN, buff=0.05), values_to_move.animate.move_to([3.5, -9.62, 0.0]), run_time=3)
        self.add(all_svgs[43], all_svgs[44])
        ae_attn_head_group_2 = Group(action_expert_qkv_flow, queries_ae, keys_ae, values_ae, values_to_move, keys_to_move, attn_dots_ae, all_svgs[39], all_svgs[43], all_svgs[44])
        self.wait()
        self.play(ReplacementTransform(action_expert_attn_head_border, action_expert_h6_border_copy), ae_attn_head_group_2.animate.scale(0.055).move_to([4.3, -6.47, 0]), self.frame.animate.reorient(0, 0, 0, (5.18, -5.78, 0.0), 6.52), run_time=6)
        self.play(FadeIn(action_expert_full_2), FadeIn(action_expert_label), FadeIn(all_svgs[36][0]), FadeIn(all_svgs[34][1]), FadeIn(diffusion_images[10]), FadeOut(ae_attn_head_group_2), run_time=3)
        self.remove(keys, queries, values, all_svgs[17], all_svgs[18], all_svgs[19], all_svgs[37], all_svgs[14][-1], attn_dots)
        self.add(full_gemma_copy)
        all_svgs[45].shift([0.2, 0, 0])
        all_svgs[46].shift([0.2, 0, 0])
        full_gemma_copy.scale(1.5)
        full_gemma_copy.move_to([5.1, 0.6, 0])
        full_gemma_copy[0].set_color(BLUE2)
        diffusion_images[-1].scale(1.3)
        diffusion_images[-1].move_to([12.8, -5.2, 0.0])
        final_actions_text.scale(1.1)
        final_actions_text.next_to(diffusion_images[-1], DOWN, buff=0.1)
        self.add(final_actions_text)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (4.04, -2.31, 0.0), 13.17), run_time=8)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (4.27, 0.69, 0.0), 7.52), FadeOut(all_svgs[46]), run_time=4)
        action_expert_full_copy_2 = VGroup(*[action_expert_full_copy[i] for i in [1, 2, 3, 4]])
        self.remove(action_expert_h6_border_copy)
        self.remove(action_expert_full)
        self.add(action_expert_full_copy_2)
        self.remove(action_expert_full_copy_2[3])
        llm_attn_rows_tmp = VGroup()
        for i in range(8):
            flat_line = Line(LEFT * 0.45, RIGHT * 0.45)
            flat_line.set_stroke(GREEN, width=3)
            llm_attn_rows_tmp.add(flat_line)
        llm_attn_rows_1 = VGroup(llm_attn_rows_tmp, llm_attn_rows_tmp.copy(), llm_attn_rows_tmp.copy())
        llm_attn_rows_1[0].arrange(DOWN, buff=0.53)
        llm_attn_rows_1[0].move_to([0.7, 0.98, 0])
        llm_attn_rows_1[1].arrange(DOWN, buff=0.53)
        llm_attn_rows_1[1].set_color(ORANGE)
        llm_attn_rows_1[1].move_to([0.7, 0.86, 0])
        llm_attn_rows_1[2].arrange(DOWN, buff=0.53)
        llm_attn_rows_1[2].set_color(BLUE)
        llm_attn_rows_1[2].move_to([0.7, 0.74, 0])
        llm_attn_rows_2 = llm_attn_rows_1.copy()
        llm_attn_rows_3 = llm_attn_rows_1.copy()
        llm_attn_rows_2.move_to([4.3, 0.86, 0])
        llm_attn_rows_3.move_to([7.9, 0.85, 0])
        ae_attn_rows_tmp = VGroup()
        for i in range(8):
            flat_line = Line(LEFT * 0.45, RIGHT * 0.45)
            flat_line.set_stroke(RED, width=3)
            ae_attn_rows_tmp.add(flat_line)
        ae_attn_rows_1 = VGroup(ae_attn_rows_tmp, ae_attn_rows_tmp.copy(), llm_attn_rows_tmp.copy(), ae_attn_rows_tmp.copy(), llm_attn_rows_tmp.copy())
        ae_attn_rows_1[0].arrange(DOWN, buff=0.53)
        ae_attn_rows_1[0].move_to([0.7, -4.98, 0])
        ae_attn_rows_1[1].arrange(DOWN, buff=0.53)
        ae_attn_rows_1[3].set_color(PINK)
        ae_attn_rows_1[1].move_to([0.7, -5.06, 0])
        ae_attn_rows_1[2].arrange(DOWN, buff=0.53)
        ae_attn_rows_1[3].set_color(GREEN)
        ae_attn_rows_1[2].move_to([0.7, -5.14, 0])
        ae_attn_rows_1[3].arrange(DOWN, buff=0.53)
        ae_attn_rows_1[3].set_color(ORANGE)
        ae_attn_rows_1[3].move_to([0.7, -5.22, 0])
        ae_attn_rows_1[4].arrange(DOWN, buff=0.53)
        ae_attn_rows_1[4].set_color(BLUE)
        ae_attn_rows_1[4].move_to([0.7, -5.3, 0])
        ae_attn_rows_2 = ae_attn_rows_1.copy()
        ae_attn_rows_3 = ae_attn_rows_1.copy()
        ae_attn_rows_2.move_to([4.3, -5.14, 0])
        ae_attn_rows_3.move_to([7.9, -5.15, 0])
        self.wait()
        self.remove(action_expert_full_copy[4])
        all_svgs[27].set_opacity(0.85)
        self.play(VGroup(*[full_gemma_copy[i] for i in [0, 1, 2, 3, 5]]).animate.set_opacity(0.6), VGroup(*[action_expert_full_copy[i] for i in [1, 2, 3]]).animate.set_opacity(0.6), all_svgs[36][0].animate.set_opacity(0.6), action_expert_label.animate.set_opacity(0.6), *[ShowCreation(llm_attn_rows_1[0][j]) for j in range(8)], *[ShowCreation(llm_attn_rows_1[1][j]) for j in range(8)], *[ShowCreation(llm_attn_rows_1[2][j]) for j in range(8)], run_time=4)
        self.play(*[ShowCreation(llm_attn_rows_2[0][j]) for j in range(8)], *[ShowCreation(llm_attn_rows_2[1][j]) for j in range(8)], *[ShowCreation(llm_attn_rows_2[2][j]) for j in range(8)], run_time=4)
        self.play(*[ShowCreation(llm_attn_rows_3[0][j]) for j in range(8)], *[ShowCreation(llm_attn_rows_3[1][j]) for j in range(8)], *[ShowCreation(llm_attn_rows_3[2][j]) for j in range(8)], run_time=4)
        self.add(ae_attn_rows_1[0], ae_attn_rows_2[0], ae_attn_rows_3[0])
        self.add(ae_attn_rows_1[1], ae_attn_rows_2[1], ae_attn_rows_3[1])
        self.play(self.frame.animate.reorient(0, 0, 0, (4.29, -5.41, 0.0), 7.52), *[ReplacementTransform(llm_attn_rows_1[0], ae_attn_rows_1[2])], *[ReplacementTransform(llm_attn_rows_1[1], ae_attn_rows_1[3])], *[ReplacementTransform(llm_attn_rows_1[2], ae_attn_rows_1[4])], *[ReplacementTransform(llm_attn_rows_2[0], ae_attn_rows_2[2])], *[ReplacementTransform(llm_attn_rows_2[1], ae_attn_rows_2[3])], *[ReplacementTransform(llm_attn_rows_2[2], ae_attn_rows_2[4])], *[ReplacementTransform(llm_attn_rows_3[0], ae_attn_rows_3[2])], *[ReplacementTransform(llm_attn_rows_3[1], ae_attn_rows_3[3])], *[ReplacementTransform(llm_attn_rows_3[2], ae_attn_rows_3[4])], run_time=7)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (4.16, -2.38, 0.0), 12.91), VGroup(*[full_gemma_copy[i] for i in [0, 1, 2, 3, 5]]).animate.set_opacity(1.0), VGroup(*[action_expert_full_copy[i] for i in [1, 2, 3]]).animate.set_opacity(1.0), all_svgs[36][0].animate.set_opacity(1.0), action_expert_label.animate.set_opacity(1.0), run_time=8)
        diffusion_images_copy.set_opacity(1.0)
        for i in range(len(diffusion_images_copy)):
            diffusion_images_copy[i].move_to(tmp_diffusion_images[-1])
        diffusion_images_copy_2.set_opacity(1.0)
        for i in range(len(diffusion_images_copy_2)):
            diffusion_images_copy_2[i].scale(1.3)
            diffusion_images_copy_2[i].move_to(diffusion_images[-1])
        self.remove(tmp_diffusion_images, diffusion_images)
        self.add(diffusion_images_copy[0])
        self.wait()
        self.play(FadeIn(diffusion_images_copy_2[1]))
        self.wait()
        self.play(diffusion_images_copy_2[1].animate.scale(1 / 1.3).move_to(diffusion_images_copy[0]), run_time=4)
        self.play(FadeIn(diffusion_images_copy_2[2]))
        for i in range(2, len(diffusion_images_copy_2)):
            self.add(diffusion_images_copy[i - 1])
            self.wait()
            self.add(diffusion_images_copy_2[i])
            self.wait()
        self.wait()
        self.remove(diffusion_images_copy_2)
        self.remove(diffusion_images_copy)
        self.add(diffusion_images_copy[0])
        self.remove(ae_attn_rows_1[4], ae_attn_rows_1[3], ae_attn_rows_1[2])
        self.remove(ae_attn_rows_2[4], ae_attn_rows_2[3], ae_attn_rows_2[2])
        self.remove(ae_attn_rows_3[4], ae_attn_rows_3[3], ae_attn_rows_3[2])

        def _make_lines(color, n=8):
            return VGroup(*[Line(LEFT * 0.45, RIGHT * 0.45).set_stroke(color, width=3) for _ in range(n)])
        _l1 = VGroup(_make_lines(GREEN), _make_lines(ORANGE), _make_lines(BLUE))
        _l1[0].arrange(DOWN, buff=0.53).move_to([0.7, 0.98, 0])
        _l1[1].arrange(DOWN, buff=0.53).move_to([0.7, 0.86, 0])
        _l1[2].arrange(DOWN, buff=0.53).move_to([0.7, 0.74, 0])
        _l2 = _l1.copy().move_to([4.3, 0.86, 0])
        _l3 = _l1.copy().move_to([7.9, 0.85, 0])
        self.wait()
        self.play(*[ShowCreation(_l1[c][j]) for c in range(3) for j in range(8)], run_time=3)
        self.play(*[ShowCreation(_l2[c][j]) for c in range(3) for j in range(8)], run_time=3)
        self.play(*[ShowCreation(_l3[c][j]) for c in range(3) for j in range(8)], run_time=3)
        _a1 = VGroup(_make_lines(RED), _make_lines(PINK), _make_lines(GREEN), _make_lines(ORANGE), _make_lines(BLUE))
        _a1[0].arrange(DOWN, buff=0.53).move_to([0.7, -4.98, 0])
        _a1[1].arrange(DOWN, buff=0.53).move_to([0.7, -5.06, 0])
        _a1[2].arrange(DOWN, buff=0.53).move_to([0.7, -5.14, 0])
        _a1[3].arrange(DOWN, buff=0.53).move_to([0.7, -5.22, 0])
        _a1[4].arrange(DOWN, buff=0.53).move_to([0.7, -5.3, 0])
        _a2 = _a1.copy().move_to([4.3, -5.14, 0])
        _a3 = _a1.copy().move_to([7.9, -5.15, 0])
        self.add(_a1[0], _a2[0], _a3[0])
        self.add(_a1[1], _a2[1], _a3[1])
        self.wait()
        self.play(*[ReplacementTransform(_l1[c], _a1[c + 2]) for c in range(3)], *[ReplacementTransform(_l2[c], _a2[c + 2]) for c in range(3)], *[ReplacementTransform(_l3[c], _a3[c + 2]) for c in range(3)], run_time=5)
        self.wait()
        diffusion_images_copy_3.set_opacity(1.0)
        for i in range(len(diffusion_images_copy)):
            diffusion_images_copy_3[i].move_to(tmp_diffusion_images[-1])
        diffusion_images_copy_4.set_opacity(1.0)
        for i in range(len(diffusion_images_copy_4)):
            diffusion_images_copy_4[i].scale(1.3)
            diffusion_images_copy_4[i].move_to(diffusion_images[-1])
        for i in range(1, len(diffusion_images_copy_4)):
            self.add(diffusion_images_copy_3[i - 1])
            self.wait()
            self.add(diffusion_images_copy_4[i])
            self.wait()
        self.wait(20)
        self.embed()

class P34_Pickup(InteractiveScene):

    def construct(self):
        svgs_to_skip = [0, 2, 3, 8, 12, 13, 20, 21]
        svg_files = list(sorted(svg_dir.glob('*.svg')))
        all_svgs = Group()
        for i, svg_file in enumerate(svg_files):
            if i in svgs_to_skip:
                continue
            svg_image = SVGMobject(str(svg_file))
            svg_image.scale(3.9)
            all_svgs.add(svg_image[1:])
        final_time_series = ImageMobject(str(hacking_dir / 'p31/000/pred_tall/299.png'))
        final_time_series.scale(0.7)
        final_time_series.move_to([2.3, -2.1, 0])
        legend = ImageMobject(str(hacking_dir / 'p31/legend_2.png'))
        legend.scale(0.6)
        legend.move_to([6.1, -2.1, 0])
        legend.set_opacity(0.8)
        final_image_overhead = ImageMobject(str(hacking_dir / 'p31/000/high/299.jpg'))
        final_image_overhead.scale(0.78)
        final_image_overhead.move_to([-4.55, 1.83, 0])
        final_image_left = ImageMobject(str(hacking_dir / 'p31/000/left_wrist/299.jpg'))
        final_image_left.scale(0.78)
        final_image_left.move_to([-0.15, 1.83, 0])
        final_image_right = ImageMobject(str(hacking_dir / 'p31/000/right_wrist/299.jpg'))
        final_image_right.scale(0.78)
        final_image_right.move_to([4.21, 1.83, 0])
        prompt = Text('"Uncap the pen"', font='Myriad Pro', weight='bold', font_size=28)
        prompt.move_to([-5.6, -2.08, 0])
        pi0_box = RoundedRectangle(width=1.85, height=1.55, corner_radius=0.1, stroke_color=FRESH_TAN, stroke_width=2, fill_opacity=0)
        pi0_box.move_to([-2.76, -2.1, 0])
        pi0_logo = Tex('\\pi_0', font_size=60)
        pi0_logo.set_color(FRESH_TAN)
        pi0_logo.move_to(pi0_box)
        pi0_logo.shift([0, -0.05, 0])
        self.add(final_time_series, legend, final_image_overhead, final_image_left, final_image_right)
        self.add(prompt, pi0_box, pi0_logo)
        self.add(all_svgs[0])
        self.wait()
        pi0_box_2 = RoundedRectangle(width=5.1, height=4.0, corner_radius=0.1, stroke_color=CHILL_BROWN, stroke_width=1, fill_opacity=0)
        pi0_box_2.move_to([-0.25, 0.7, 0])
        self.wait()
        self.remove(all_svgs[0], legend)
        self.play(ReplacementTransform(pi0_box, pi0_box_2), prompt.animate.scale(0.9).move_to([-5.5, -3.34, 0]), final_image_overhead.animate.scale(0.66).move_to([-5.23, 2.58, 0]), final_image_left.animate.scale(0.66).move_to([-5.23, 0.35, 0]), final_image_right.animate.scale(0.66).move_to([-5.23, -1.82, 0]), final_time_series.animate.scale(0.6).move_to([4.7, 0.78, 0]), pi0_logo.animate.scale(0.7).move_to([2, -1.1, 0]), run_time=6)
        self.wait()
        self.play(Write(all_svgs[3]), self.frame.animate.reorient(0, 0, 0, (-0.24, 0.62, 0.0), 5.09), run_time=4)
        self.wait()
        self.play(Write(all_svgs[2]), run_time=4)
        self.play(Write(all_svgs[4]), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0, 0, 0), 8), Write(all_svgs[1]), run_time=5)
        action_expert_box = RoundedRectangle(width=3.2, height=1.5, corner_radius=0.1, stroke_color=YELLOW, stroke_width=2, fill_opacity=0)
        action_expert_box.move_to([0.33, -1.8, 0])
        pi0_box_3 = RoundedRectangle(width=5.1, height=5.7, corner_radius=0.1, stroke_color=CHILL_BROWN, stroke_width=1, fill_opacity=0)
        pi0_box_3.move_to([-0.25, -0.15, 0])
        action_expert_label = Text('ACTION EXPERT', font='Myriad Pro', weight='bold', font_size=24)
        action_expert_label.set_color(YELLOW)
        action_expert_label.move_to(action_expert_box)
        action_expert_sublabel = Text('gemma_expert = GemmaForCausalLM()', font='consolas', font_size=16)
        action_expert_sublabel.next_to(action_expert_label, DOWN, buff=0.13)
        self.wait()
        self.play(ReplacementTransform(pi0_box_2, pi0_box_3), pi0_logo.animate.move_to([2, -2.8, 0]), final_time_series.animate.move_to([4.7, -1.7, 0]), all_svgs[1][-2:].animate.move_to([2.5, -1.8, 0]), run_time=4)
        self.play(ShowCreation(action_expert_box), Write(action_expert_label), run_time=3)
        self.wait()
        self.frame.reorient(0, 0, 0, (0.38, -0.14, 0.0), 6.18)
        group_to_fade = Group(final_time_series, final_image_overhead, final_image_left, final_image_right, prompt, all_svgs[1], all_svgs[2])
        self.remove(group_to_fade)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0, 0, 0), 8), FadeIn(group_to_fade), run_time=16)
        self.wait(20)
        self.embed()

class P31_49b(InteractiveScene):

    def construct(self):
        svgs_to_skip = [0, 2, 3, 8, 12, 13, 20, 21]
        svg_files = list(sorted(svg_dir.glob('*.svg')))
        all_svgs = Group()
        for i, svg_file in enumerate(svg_files):
            if i in svgs_to_skip:
                continue
            svg_image = SVGMobject(str(svg_file))
            svg_image.scale(3.9)
            all_svgs.add(svg_image[1:])
        final_time_series = ImageMobject(str(hacking_dir / 'p31/000/pred_tall/299.png'))
        final_time_series.scale(0.7)
        final_time_series.move_to([2.3, -2.1, 0])
        legend = ImageMobject(str(hacking_dir / 'p31/legend_2.png'))
        legend.scale(0.6)
        legend.move_to([6.1, -2.1, 0])
        legend.set_opacity(0.8)
        final_image_overhead = ImageMobject(str(hacking_dir / 'p31/000/high/299.jpg'))
        final_image_overhead.scale(0.78)
        final_image_overhead.move_to([-4.55, 1.83, 0])
        final_image_left = ImageMobject(str(hacking_dir / 'p31/000/left_wrist/299.jpg'))
        final_image_left.scale(0.78)
        final_image_left.move_to([-0.15, 1.83, 0])
        final_image_right = ImageMobject(str(hacking_dir / 'p31/000/right_wrist/299.jpg'))
        final_image_right.scale(0.78)
        final_image_right.move_to([4.21, 1.83, 0])
        prompt = Text('"Uncap the pen"', font='Myriad Pro', weight='bold', font_size=28)
        prompt.move_to([-5.6, -2.08, 0])
        pi0_box = RoundedRectangle(width=1.85, height=1.55, corner_radius=0.1, stroke_color=FRESH_TAN, stroke_width=2, fill_opacity=0)
        pi0_box.move_to([-2.76, -2.1, 0])
        pi0_logo = Tex('\\pi_0', font_size=60)
        pi0_logo.set_color(FRESH_TAN)
        pi0_logo.move_to(pi0_box)
        pi0_logo.shift([0, -0.05, 0])
        self.add(final_time_series, legend, final_image_overhead, final_image_left, final_image_right)
        self.add(prompt, pi0_box, pi0_logo)
        self.add(all_svgs[0])
        self.wait()
        pi0_box_2 = RoundedRectangle(width=5.1, height=4.0, corner_radius=0.1, stroke_color=CHILL_BROWN, stroke_width=1, fill_opacity=0)
        pi0_box_2.move_to([-0.25, 0.7, 0])
        self.wait()
        self.remove(all_svgs[0], legend)
        self.play(ReplacementTransform(pi0_box, pi0_box_2), prompt.animate.scale(0.9).move_to([-5.5, -3.34, 0]), final_image_overhead.animate.scale(0.66).move_to([-5.23, 2.58, 0]), final_image_left.animate.scale(0.66).move_to([-5.23, 0.35, 0]), final_image_right.animate.scale(0.66).move_to([-5.23, -1.82, 0]), final_time_series.animate.scale(0.6).move_to([4.7, 0.78, 0]), pi0_logo.animate.scale(0.7).move_to([2, -1.1, 0]), run_time=6)
        self.wait()
        self.play(Write(all_svgs[3]), self.frame.animate.reorient(0, 0, 0, (-0.24, 0.62, 0.0), 5.09), run_time=4)
        self.wait()
        self.play(Write(all_svgs[2]), run_time=4)
        self.play(Write(all_svgs[4]), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0, 0, 0), 8), Write(all_svgs[1]), run_time=5)
        action_expert_box = RoundedRectangle(width=3.2, height=1.5, corner_radius=0.1, stroke_color=YELLOW, stroke_width=2, fill_opacity=0)
        action_expert_box.move_to([0.33, -1.8, 0])
        pi0_box_3 = RoundedRectangle(width=5.1, height=5.7, corner_radius=0.1, stroke_color=CHILL_BROWN, stroke_width=1, fill_opacity=0)
        pi0_box_3.move_to([-0.25, -0.15, 0])
        action_expert_label = Text('ACTION EXPERT', font='Myriad Pro', weight='bold', font_size=24)
        action_expert_label.set_color(YELLOW)
        action_expert_label.move_to(action_expert_box)
        action_expert_sublabel = Text('gemma_expert = GemmaForCausalLM()', font='consolas', font_size=16)
        action_expert_sublabel.next_to(action_expert_label, DOWN, buff=0.13)
        self.wait()
        self.play(ReplacementTransform(pi0_box_2, pi0_box_3), pi0_logo.animate.move_to([2, -2.8, 0]), final_time_series.animate.move_to([4.7, -1.7, 0]), all_svgs[1][-2:].animate.move_to([2.5, -1.8, 0]), run_time=4)
        self.play(ShowCreation(action_expert_box), Write(action_expert_label), run_time=3)
        self.wait()
        self.play(Write(action_expert_sublabel), self.frame.animate.reorient(0, 0, 0, (0.45, -1.81, 0.0), 4.13), run_time=3)
        self.wait()
        height, width = (224, 244)
        grid_n = 16
        patch_h = height // grid_n
        patch_w = width // grid_n
        total_height = 2.72
        patch_size = total_height / grid_n
        FRAME_IDX = 150
        pixel_squares = Group()
        for k, image_name in enumerate(['base_0_rgb', 'left_wrist_0_rgb', 'right_wrist_0_rgb']):
            pixel_squares.add(Group())
            patch_dir = hacking_dir / ('p35/' + str(FRAME_IDX) + '/' + image_name)
            for i in range(2, 14):
                for j in range(grid_n):
                    patch_path = os.path.join(patch_dir, f'patch_{i}_{j}.png')
                    patch_mob = ImageMobject(patch_path)
                    patch_mob.set_height(patch_size)
                    patch_mob.set_width(patch_size, stretch=True)
                    x_pos = (j - grid_n / 2 + 0.5) * patch_size
                    y_pos = -(i - grid_n / 2 + 0.5) * patch_size
                    patch_mob.move_to([x_pos, y_pos, 0])
                    pixel_squares[-1].add(patch_mob)
        pixel_squares[0].move_to([-5.23, 2.58, 0.0])
        pixel_squares[1].move_to([-5.23, 0.375, 0.0])
        pixel_squares[2].move_to([-5.23, -1.82, 0.0])
        self.add(pixel_squares)
        self.remove(final_image_overhead, final_image_left, final_image_right)
        self.remove(all_svgs[1])
        self.add(all_svgs[1])
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0, 0, 0), 8), run_time=3)
        self.wait()
        self.remove(action_expert_sublabel)
        self.wait()
        siglip_1 = all_svgs[2][:13]
        siglip_2 = all_svgs[2][13:26]
        siglip_3 = all_svgs[2][26:39]
        image_encoders_label = all_svgs[2][39:]
        self.wait()
        self.play(pi0_logo.animate.scale(0.85).set_color(CHILL_BROWN).to_corner(DOWN + RIGHT, buff=0.25), FadeOut(pi0_box_3), FadeOut(all_svgs[3]), FadeOut(all_svgs[1]), FadeOut(final_time_series), FadeOut(action_expert_label), FadeOut(action_expert_box), all_svgs[4].animate.set_color(CHILL_BROWN).move_to([2, 0.4, 0]), pixel_squares[1].animate.shift([0, -0.2, 0.0]), pixel_squares[2].animate.shift([0, -0.4, 0.0]), prompt.animate.shift([0.2, -0.3, 0.0]), siglip_1.animate.scale(1.1).move_to([-3.0, 2.6, 0]), siglip_2.animate.scale(1.1).move_to([-3.0, 0.2, 0]), siglip_3.animate.scale(1.1).move_to([-3.0, -2.1, 0]), image_encoders_label.animate.scale(1.1).move_to([-3.0, 3.5, 0]), run_time=4)
        animations = []
        gap_factor = 0.12
        for i in range(len(pixel_squares)):
            center = pixel_squares[i].get_center()
            for pixel in pixel_squares[i]:
                pixel_pos = pixel.get_center()
                direction_vector = pixel_pos - center
                distance = np.linalg.norm(direction_vector)
                if distance > 0:
                    unit_vector = direction_vector / distance
                    displacement = unit_vector * distance * gap_factor
                    new_position = pixel_pos + displacement
                    animations.append(ApplyMethod(pixel.move_to, new_position))
        self.wait()
        self.play(*animations, run_time=3.0)
        lil_arrows_pair_1 = all_svgs[5]
        lil_arrows_pair_2 = lil_arrows_pair_1.copy()
        lil_arrows_pair_3 = lil_arrows_pair_1.copy()
        lil_arrows_pair_1.move_to([-3.0, 2.57, 0])
        lil_arrows_pair_2.move_to([-3.0, 0.18, 0])
        lil_arrows_pair_3.move_to([-3.0, -2.18, 0])
        embedding_brackets_1 = all_svgs[6]
        embedding_brackets_1.shift([0.08, 0.0, 0])
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-3.4, 1.91, 0.0), 4.03), Write(embedding_brackets_1), Write(lil_arrows_pair_1), Write(lil_arrows_pair_2), Write(lil_arrows_pair_3), run_time=5)
        overhead_im_full = np.load(hacking_dir / 'p35/150_overhead.npy')
        left_im_full = np.load(hacking_dir / 'p35/150_left.npy')
        right_im_full = np.load(hacking_dir / 'p35/150_right.npy')
        overhead_colors = patch_bright_average(np.array(overhead_im_full), exponent=2.0).reshape(-1, 3)
        left_colors = patch_bright_average(np.array(left_im_full), exponent=2.0).reshape(-1, 3)
        right_colors = patch_bright_average(np.array(right_im_full), exponent=2.0).reshape(-1, 3)
        patches_indices_to_move_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        embedding_rows_1 = VGroup()
        starting_squares_1 = VGroup()
        vertical_spacing = 0.2
        for i, patch_index in enumerate(patches_indices_to_move_1):
            boosted_color = rgb_to_color(boost_colors_hsv(overhead_colors[patch_index + 32].reshape(1, 3) / 255.0, saturation_boost=SATURATION_BOOST, min_saturation=MIN_SATURATION, min_value=MIN_VALUE).ravel())
            flat_rect = Rectangle(width=1.1, height=0.03)
            flat_rect.set_fill(boosted_color, opacity=1)
            flat_rect.set_stroke(width=0)
            flat_rect.move_to([-1.5, 3.15 - i * vertical_spacing, 0])
            color_square = Square(side_length=patch_size)
            color_square.set_fill(rgb_to_color(overhead_colors[patch_index + 32] / 255.0), opacity=1)
            color_square.set_stroke(width=0)
            color_square.move_to(pixel_squares[0][patch_index])
            embedding_rows_1.add(flat_rect)
            starting_squares_1.add(color_square)
        self.wait()
        self.play(LaggedStart(*[Succession(FadeIn(starting_squares_1[i], run_time=0.1), ReplacementTransform(starting_squares_1[i], embedding_rows_1[i])) for i in range(len(embedding_rows_1))], lag_ratio=0.2), run_time=12)
        ellipsis_dots = VGroup(*[Dot(radius=0.025).set_color(CHILL_BROWN) for _ in range(3)])
        ellipsis_dots.arrange(DOWN, buff=0.035)
        ellipsis_dots.next_to(embedding_rows_1[-1], DOWN, buff=0.15)
        self.play(Write(ellipsis_dots), run_time=2)
        self.wait()
        patches_indices_to_move_2 = [82, 83, 84, 85, 86, 87, 88, 89, 90, 91]
        embedding_rows_2 = VGroup()
        starting_squares_2 = VGroup()
        vertical_spacing = 0.2
        for i, patch_index in enumerate(patches_indices_to_move_2):
            boosted_color = rgb_to_color(boost_colors_hsv(left_colors[patch_index + 32].reshape(1, 3) / 255.0, saturation_boost=SATURATION_BOOST, min_saturation=MIN_SATURATION, min_value=MIN_VALUE).ravel())
            flat_rect = Rectangle(width=1.1, height=0.03)
            flat_rect.set_fill(boosted_color, opacity=1)
            flat_rect.set_stroke(width=0)
            flat_rect.move_to([-1.5, 1.0 - i * vertical_spacing, 0])
            color_square = Square(side_length=patch_size)
            color_square.set_fill(rgb_to_color(left_colors[patch_index + 32] / 255.0), opacity=1)
            color_square.set_stroke(width=0)
            color_square.move_to(pixel_squares[1][patch_index])
            embedding_rows_2.add(flat_rect)
            starting_squares_2.add(color_square)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-2.39, 1.34, 0.0), 5.19), LaggedStart(*[Succession(FadeIn(starting_squares_2[i], run_time=0.1), ReplacementTransform(starting_squares_2[i], embedding_rows_2[i])) for i in range(len(embedding_rows_2))], lag_ratio=0.3), run_time=12)
        ellipsis_dots_2 = VGroup(*[Dot(radius=0.025).set_color(CHILL_BROWN) for _ in range(3)])
        ellipsis_dots_2.arrange(DOWN, buff=0.035)
        ellipsis_dots_2.next_to(embedding_rows_2[-1], DOWN, buff=0.1)
        self.play(Write(ellipsis_dots_2), run_time=2)
        patches_indices_to_move_3 = [186, 186, 187, 188, 189, 190, 191]
        embedding_rows_3 = VGroup()
        starting_squares_3 = VGroup()
        vertical_spacing = 0.2
        for i, patch_index in enumerate(patches_indices_to_move_3):
            boosted_color = rgb_to_color(boost_colors_hsv(right_colors[patch_index + 32].reshape(1, 3) / 255.0, saturation_boost=SATURATION_BOOST, min_saturation=MIN_SATURATION, min_value=MIN_VALUE).ravel())
            flat_rect = Rectangle(width=1.1, height=0.03)
            flat_rect.set_fill(boosted_color, opacity=1)
            flat_rect.set_stroke(width=0)
            flat_rect.move_to([-1.5, -1.3 - i * vertical_spacing, 0])
            color_square = Square(side_length=patch_size)
            color_square.set_fill(rgb_to_color(right_colors[patch_index + 32] / 255.0), opacity=1)
            color_square.set_stroke(width=0)
            color_square.move_to(pixel_squares[2][patch_index])
            embedding_rows_3.add(flat_rect)
            starting_squares_3.add(color_square)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0, 0, 0.0), 8.0), LaggedStart(*[Succession(FadeIn(starting_squares_3[i], run_time=0.1), ReplacementTransform(starting_squares_3[i], embedding_rows_3[i])) for i in range(len(embedding_rows_3))], lag_ratio=0.3), run_time=10)
        embedding_brackets_2 = all_svgs[7][2:8].shift([0.08, 0.0, 0])
        blue_text_embedding_arrow = all_svgs[7][:2].shift([0.08, 0.0, 0])
        embedding_exit_arrow = all_svgs[7][8:].shift([0.08, 0.0, 0])
        embedding_brackets_1_only = VGroup(*[embedding_brackets_1[i] for i in [0, 8, 7, 9, 10, 11]])
        embedding_rows_4 = VGroup()
        for i in range(4):
            flat_line = Line(LEFT * 0.55, RIGHT * 0.55)
            flat_line.set_stroke(BLUE, width=4)
            flat_line.move_to([-1.5, -2.75 - i * vertical_spacing, 0])
            embedding_rows_4.add(flat_line)
        tokenized_prompt = Text('Un  cap  the  pen', font='Myriad Pro', weight='bold', font_size=25)
        tokenized_prompt.set_color(BLUE)
        tokenized_prompt.set_stroke(BLUE, width=0.1)
        tokenized_prompt.move_to(prompt)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (-2.87, -1.71, 0.0), 4.66), run_time=3)
        self.wait()
        self.remove(prompt[0], prompt[-1])
        self.play(ReplacementTransform(prompt[1:3], tokenized_prompt[:2]), ReplacementTransform(prompt[3:6], tokenized_prompt[2:5]), ReplacementTransform(prompt[6:9], tokenized_prompt[5:8]), ReplacementTransform(prompt[9:12], tokenized_prompt[8:11]), run_time=2.5)
        self.wait()
        self.wait()
        self.play(ReplacementTransform(embedding_brackets_1_only, embedding_brackets_2), LaggedStart(ReplacementTransform(tokenized_prompt[:2].copy(), embedding_rows_4[0]), ReplacementTransform(tokenized_prompt[2:4].copy(), embedding_rows_4[1]), ReplacementTransform(tokenized_prompt[5:8].copy(), embedding_rows_4[2]), ReplacementTransform(tokenized_prompt[8:11].copy(), embedding_rows_4[3]), lag_ratio=0.5), run_time=5)
        blue_text_embedding_arrow.set_color(BLUE)
        blue_text_embedding_arrow.shift([-0.1, 0.05, 0])
        self.wait()
        self.play(Write(blue_text_embedding_arrow))
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0, 0, 0), 8), run_time=4)
        embedding_out_arrow = all_svgs[7][-2:]
        simple_llm_box = all_svgs[4]
        embedding_out_arrow.shift([-0.13, 0.18, 0])
        full_gemma = Group(all_svgs[8], all_svgs[9], all_svgs[10], all_svgs[11], all_svgs[12], all_svgs[13])
        full_gemma.shift([0.2, 0, 0])
        self.wait()
        self.play(ReplacementTransform(simple_llm_box[-1], all_svgs[8][0]), ReplacementTransform(simple_llm_box[0:3], all_svgs[8][1:4]), ReplacementTransform(simple_llm_box[3:-1], all_svgs[8][4:]), FadeIn(embedding_out_arrow), self.frame.animate.reorient(0, 0, 0, (3.08, 0.07, 0.0), 4.73), run_time=5)
        self.wait()
        self.play(Write(all_svgs[9]), Write(all_svgs[13]), run_time=3)
        self.wait()
        self.play(Write(all_svgs[10]), Write(all_svgs[11]), Write(all_svgs[12]), run_time=7)
        self.wait()
        self.remove(pi0_logo)
        self.play(FadeOut(all_svgs[8]), FadeOut(all_svgs[9]), FadeOut(all_svgs[10]), FadeOut(all_svgs[13]), run_time=3)
        h6_label = all_svgs[12][1:]
        self.wait()
        self.play(FadeOut(all_svgs[11]), run_time=1.5)
        self.play(ReplacementTransform(all_svgs[12][0], all_svgs[14][-1]), h6_label.animate.scale(1.5).move_to([6.4, -3.4, 0]), self.frame.animate.reorient(0, 0, 0, (0, 0, 0), 8), run_time=5)
        queries = Group()
        keys = Group()
        values = Group()
        attn_dots = VGroup()
        q_spacing = 0.15
        for i in range(11):
            q = ImageMobject(str(hacking_dir / ('p40_1/queries_' + str(i).zfill(2) + '.png')))
            q.scale(0.022)
            q.move_to([3.5, 3.2 - i * q_spacing, 0])
            queries.add(q)
            if i == 1 or i == 6:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(q)
                attn_dots.add(e)
        for i in range(11):
            k = ImageMobject(str(hacking_dir / ('p40_1/keys_' + str(i).zfill(2) + '.png')))
            k.scale(0.022)
            k.move_to([3.5, 0.9 - i * q_spacing, 0])
            keys.add(k)
            if i == 1 or i == 6:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(k)
                attn_dots.add(e)
        for i in range(11):
            v = ImageMobject(str(hacking_dir / ('p40_1/values_' + str(i).zfill(2) + '.png')))
            v.scale(0.022)
            v.move_to([3.5, -1.37 - i * q_spacing, 0])
            values.add(v)
            if i == 1 or i == 6:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(v)
                attn_dots.add(e)
        all_svgs[17].shift([0.04, 0.03, 0])
        all_svgs[18].shift([0.04, 0.0, 0])
        all_svgs[19].shift([0.04, 0.0, 0])
        self.wait()
        self.play(Write(all_svgs[15]), run_time=5)
        self.wait()
        self.play(FadeIn(queries), FadeIn(all_svgs[17]), FadeIn(attn_dots[:2]), run_time=2)
        self.play(FadeIn(keys), FadeIn(all_svgs[18]), FadeIn(attn_dots[2:4]), run_time=2)
        self.play(FadeIn(values), FadeIn(all_svgs[19]), FadeIn(attn_dots[4:]), run_time=2)
        all_svgs[20].scale(1.015)
        all_svgs[20].shift([0.2, 0.03, 0])
        self.wait()
        self.play(Write(all_svgs[20]))
        self.remove(all_svgs[20])
        self.play(self.frame.animate.reorient(0, 0, 0, (3.47, 2.5, 0.0), 2.97), run_time=5)
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0, 0, 0), 8), run_time=4)
        self.wait()
        self.remove(attn_dots)
        self.add(attn_dots)
        self.play(self.frame.animate.reorient(0, 0, 0, (3.63, 1.2, 0.0), 4.37), FadeOut(all_svgs[14][-1]), run_time=10)
        self.wait()
        self.play(Group(*[queries[i] for i in [0, 2, 3, 4, 5, 7, 8, 9]]).animate.set_opacity(0.35), run_time=3)
        dot_product_values = {0: '-27.49', 2: '-48.69', 3: ' 36.30', 4: ' 41.04', 5: '-42.65', 7: '-19.15', 8: '-19.71', 9: '-29.76', 10: '-43.39'}
        dp_x = 6.3
        dp_title = Text('DOT PRODUCT', font='Myriad Pro', weight='bold', font_size=14)
        dp_title.set_color(FRESH_TAN)
        dp_title.move_to([dp_x, 0.9 + 0.22, 0])
        dp_underline = Line(dp_title.get_left() + DOWN * 0.08, dp_title.get_right() + DOWN * 0.08)
        dp_underline.set_stroke(FRESH_TAN, width=2)
        dp_numbers = VGroup()
        for i in range(11):
            y = 0.9 - i * q_spacing
            if i in dot_product_values:
                num = Text(dot_product_values[i], font_size=14)
                num.set_color(MAGENTA)
                num.move_to([dp_x, y, 0])
                dp_numbers.add(num)
        self.play(Write(dp_title), ShowCreation(dp_underline), run_time=1.5)
        self.wait()
        query_copy = queries[-1].copy()
        query_copy.set_opacity(0.8)
        self.add(query_copy)
        self.play(query_copy.animate.move_to(keys[0]), run_time=3)
        self.play(Write(dp_numbers[0]))
        self.play(FadeOut(query_copy))
        animations = []
        query_copies = Group()
        for count, i in enumerate([2, 3, 4, 5, 7, 8, 9, 10]):
            query_copy = queries[-1].copy()
            query_copy.set_opacity(0.5)
            query_copies.add(query_copy)
            animations.append(query_copy.animate.move_to(keys[i]))
            animations.append(Write(dp_numbers[count + 1]))
        self.add(query_copies)
        self.play(LaggedStart(*animations, lag_ratio=0.4), run_time=10)
        self.wait()
        self.play(FadeOut(query_copies), run_time=3)
        attn_values = {0: '0.000', 2: '0.000', 3: '0.030', 4: '0.041', 5: '0.001', 7: '0.001', 8: '0.001', 9: '0.000', 10: '0.000'}
        attn_x = 7.5
        attn_title = Text('ATTENTION VALUE', font='Myriad Pro', weight='bold', font_size=14)
        attn_title.set_color(FRESH_TAN)
        attn_title.move_to([attn_x, 0.9 + 0.22, 0])
        attn_underline = Line(attn_title.get_left() + DOWN * 0.08, attn_title.get_right() + DOWN * 0.08)
        attn_underline.set_stroke(FRESH_TAN, width=2)
        attn_numbers = VGroup()
        for i in range(11):
            y = 0.9 - i * q_spacing
            if i in attn_values:
                num = Text(attn_values[i], font_size=14)
                num.set_color(MAGENTA)
                num.move_to([attn_x, y, 0])
                attn_numbers.add(num)
        all_svgs[21].scale(0.8)
        all_svgs[21].move_to([6.93, 0.1, 0])
        self.wait()
        self.add(all_svgs[21])
        self.play(self.frame.animate.reorient(0, 0, 0, (4.56, 1.1, 0.0), 4.22), Write(attn_title), ShowCreation(attn_underline), Write(attn_numbers))
        self.remove(h6_label)
        self.wait()
        all_attn_values = np.load(hacking_dir / 'p42_1/p42_1.npy')
        attn_row = all_attn_values[FRAME_IDX]
        cam_attn_1 = attn_row[:256].reshape(16, 16)
        cam_attn_2 = attn_row[256:512].reshape(16, 16)
        cam_attn_3 = attn_row[512:768].reshape(16, 16)
        cam_attns = [cam_attn_1, cam_attn_2, cam_attn_3]
        attn_scales = [cam_attn_1[2:14].max(), cam_attn_2[2:14].max(), cam_attn_3[2:14].max()]
        max_opacities = [0.5, 0.95, 0.95]
        magenta_overlays = Group()
        for k in range(3):
            cam = cam_attns[k][2:14, :]
            scale = attn_scales[k] if attn_scales[k] > 0 else 1.0
            mo = max_opacities[k]
            overlays_k = Group()
            for idx, patch_mob in enumerate(pixel_squares[k]):
                row = idx // 16
                col = idx % 16
                attn_val = cam[row, col]
                opacity = min(mo, mo * (attn_val / scale))
                sq = Square(side_length=patch_size)
                sq.set_fill(MAGENTA, opacity=float(opacity))
                sq.set_stroke(width=0)
                sq.move_to(patch_mob.get_center())
                overlays_k.add(sq)
            magenta_overlays.add(overlays_k)
        self.wait()
        self.play(ReplacementTransform(attn_numbers[0].copy(), magenta_overlays[0][0].set_opacity(0.2)), ReplacementTransform(attn_numbers[1].copy(), magenta_overlays[1][85]), ReplacementTransform(attn_numbers[2].copy(), magenta_overlays[1][86].set_opacity(0.7)), ReplacementTransform(attn_numbers[3].copy(), magenta_overlays[1][87].set_opacity(0.7)), ReplacementTransform(attn_numbers[4].copy(), magenta_overlays[1][88]), self.frame.animate.reorient(0, 0, 0, (0.67, 0.02, 0.0), 8.6), FadeIn(magenta_overlays[0][1:]), FadeIn(magenta_overlays[1][:85]), FadeIn(magenta_overlays[1][89:]), FadeIn(magenta_overlays[2]), run_time=5)
        background_stuff = Group(all_svgs[15], all_svgs[17], all_svgs[18], all_svgs[19], queries, keys, values, attn_dots, embedding_brackets_2, embedding_rows_1, embedding_rows_2, embedding_rows_3, embedding_rows_4, ellipsis_dots, ellipsis_dots_2, blue_text_embedding_arrow, embedding_out_arrow, lil_arrows_pair_1, lil_arrows_pair_2, lil_arrows_pair_3, siglip_1, siglip_2, siglip_3, image_encoders_label, tokenized_prompt, all_svgs[6][1:7])
        background_stuff_2 = Group(all_svgs[21], dp_title, dp_underline, dp_numbers, attn_title, attn_underline, attn_numbers)
        img_gap = 0.2
        img_y = 0.0
        combined_images = []
        combined_image_start_centers = []
        for k in range(3):
            combo = Group(pixel_squares[k], magenta_overlays[k])
            combined_images.append(combo)
            combined_image_start_centers.append(combo.get_center())
        combined_image_start_centers = copy.deepcopy(np.array(combined_image_start_centers))
        total_width = pixel_squares[0].get_width()
        center_x = 0.0
        target_xs = [center_x - total_width - img_gap, center_x, center_x + total_width + img_gap]
        self.wait()
        self.play(FadeOut(background_stuff), FadeOut(background_stuff_2), combined_images[0].animate.move_to([target_xs[0], img_y, 0]), combined_images[1].animate.move_to([target_xs[1], img_y, 0]), combined_images[2].animate.move_to([target_xs[2], img_y, 0]), self.frame.animate.reorient(0, 0, 0, (-0.02, -0.07, 0.0), 5.62), run_time=4)
        self.wait()
        all_svgs[12].set_opacity(0.6)
        self.play(FadeIn(background_stuff), FadeIn(all_svgs[12]), combined_images[0].animate.move_to(combined_image_start_centers[0]), combined_images[1].animate.move_to(combined_image_start_centers[1]), combined_images[2].animate.move_to(combined_image_start_centers[2]), self.frame.animate.reorient(0, 0, 0, (0, 0, 0.0), 8), run_time=4)
        self.play(queries[:-1].animate.set_opacity(1.0), run_time=3)
        self.remove(attn_dots)
        self.add(attn_dots)
        attn_pattern = ImageMobject(str(hacking_dir / 'p44/attn_pattern_1.png'))
        attn_pattern.scale(1.3)
        attn_pattern.move_to([3.3, 1.2, 0])
        all_svgs[22].scale(0.9)
        all_svgs[22].move_to([3.6, 1.38, 0])
        all_svgs[23].move_to([2.2, -1, 0])
        all_svgs[24].move_to([4.98, -0.98, 0])
        self.wait()
        self.play(FadeOut(queries), FadeOut(keys), FadeOut(all_svgs[17]), FadeOut(all_svgs[18]), FadeOut(attn_dots[:4]), run_time=3)
        self.play(FadeIn(attn_pattern), Write(all_svgs[22]), Write(all_svgs[23]), Write(all_svgs[24]), run_time=2)
        self.wait()
        self.play(FadeOut(all_svgs[22]), attn_pattern.animate.set_opacity(0.2))
        row_center_y = -0.81
        row_left_x = 1.37
        row_right_x = 5.35
        target_h = 0.02
        all_magenta_squares = [sq for k in range(3) for sq in magenta_overlays[k]]
        all_opacities = [sq.get_opacity() for sq in all_magenta_squares]
        n = len(all_magenta_squares)
        strip_w = row_right_x - row_left_x
        cell_w = strip_w / n
        move_anims = []
        for idx, sq in enumerate(all_magenta_squares):
            tx = row_left_x + (idx + 0.5) * cell_w
            move_anims.append(sq.animate.move_to([tx, row_center_y, 0]).set_height(target_h).set_width(cell_w, stretch=True).set_opacity(all_opacities[idx] * 5))
        self.wait()
        self.play(LaggedStart(*move_anims, lag_ratio=0.005), run_time=5)
        self.play(attn_pattern.animate.set_opacity(1.0), FadeOut(magenta_overlays))
        self.wait()
        self.play(FadeOut(attn_pattern), FadeOut(all_svgs[23]), FadeOut(all_svgs[24]), run_time=2)
        self.wait()
        self.play(FadeIn(queries), FadeIn(keys), FadeIn(all_svgs[17]), FadeIn(all_svgs[18]), FadeIn(attn_dots[:4]), run_time=3)
        self.wait()
        self.play(FadeOut(queries), FadeOut(keys), FadeOut(all_svgs[17]), FadeOut(all_svgs[18]), FadeOut(attn_dots[:4]), run_time=3)
        self.wait()
        self.play(FadeIn(attn_pattern), FadeIn(all_svgs[23]), FadeIn(all_svgs[24]), run_time=2)
        self.wait()
        self.play(FadeOut(all_svgs[12]), self.frame.animate.reorient(0, 0, 0, (4.1, -2.97, 0.0), 4.76), attn_dots.animate.move_to([5.5, 0.39, 0.0]), values.animate.move_to([5.5, -2.12, 0]), all_svgs[19].animate.move_to([5.5, -3.04, 0]), attn_pattern.animate.scale(0.41).move_to([2.1, -2.12, 0]), all_svgs[23].animate.scale(0.9).move_to([2.12, -1.15, 0]), all_svgs[24].animate.scale(0.9).move_to([2.6, -3.08, 0]), run_time=5)
        head_outs = Group()
        head_out_dots = VGroup()
        out_spacing = 0.15
        for i in range(11):
            o = ImageMobject(str(hacking_dir / ('p45/out_' + str(i).zfill(2) + '.png')))
            o.scale(0.022)
            o.move_to([5.5, -3.4 - i * out_spacing, 0])
            head_outs.add(o)
            if i == 1 or i == 6:
                e = VGroup(*[Dot(radius=0.01).set_color(CHILL_BROWN) for _ in range(3)])
                e.arrange(DOWN, buff=0.012)
                e.move_to(o)
                head_out_dots.add(e)
        all_svgs[25].move_to([5.5, -5.1, 0])
        big_erquals = Text('=', font='Myriad Pro', weight='bold', font_size=42)
        big_erquals.set_color(CHILL_BROWN)
        big_erquals.move_to([2.8, -4.2, 0])
        big_erquals.set_opacity(0.7)
        self.wait()
        self.play(FadeIn(head_outs), FadeIn(head_out_dots), FadeIn(all_svgs[25]), FadeIn(big_erquals), run_time=2)
        value_row_copy_1 = values[3].copy()
        value_row_copy_1.set_opacity(0.8)
        value_row_copy_2 = values[4].copy()
        value_row_copy_2.set_opacity(0.8)
        self.add(value_row_copy_1)
        self.add(value_row_copy_2)
        self.play(LaggedStart(value_row_copy_2.animate.move_to(head_outs[-1]), value_row_copy_1.animate.move_to(head_outs[-1]), lag_ratio=0.1), run_time=5)
        self.remove(value_row_copy_1, value_row_copy_2)
        self.wait()
        all_attn_patterns = []
        for layer in range(18):
            all_attn_patterns.append([])
            for head in range(8):
                im = ImageMobject(str(hacking_dir / ('p47/attn_pattern_' + str(layer) + '_' + str(head) + '.png')))
                all_attn_patterns[-1].append(im)
        all_svgs[26].shift([0.19, 0, 0])
        gemma = Group(all_svgs[8:11], all_svgs[13], all_svgs[26])
        attn_patterns_to_show = Group()
        for i in range(8):
            all_attn_patterns[0][i].scale(0.096)
            all_attn_patterns[0][i].move_to([0.25, 1.5 - 0.358 * i, 0])
            attn_patterns_to_show.add(all_attn_patterns[0][i])
        for i in range(8):
            if i == 6:
                continue
            all_attn_patterns[1][i].scale(0.096)
            all_attn_patterns[1][i].move_to([2.65, 1.5 - 0.358 * i, 0])
            attn_patterns_to_show.add(all_attn_patterns[1][i])
        for i in range(8):
            all_attn_patterns[-1][i].scale(0.096)
            all_attn_patterns[-1][i].move_to([5.05, 1.5 - 0.358 * i, 0])
            attn_patterns_to_show.add(all_attn_patterns[-1][i])
        fadeout_group_3 = Group(values, head_outs, all_svgs[25], big_erquals, all_svgs[23], all_svgs[24], all_svgs[19], all_svgs[15], attn_dots, head_out_dots)
        self.wait()
        self.remove(fadeout_group_3)
        self.play(self.frame.animate.reorient(0, 0, 0, (0, 0, 0), 8), attn_pattern.animate.scale(0.18).move_to([2.65, 1.5 - 0.358 * 6, 0]), FadeIn(gemma), FadeIn(attn_patterns_to_show), run_time=8)
        self.remove(all_svgs[26])
        self.add(all_svgs[26])
        action_expert_box.set_color(CHILL_BROWN)
        action_expert_label.set_color(CHILL_BROWN)
        action_expert_group = VGroup(action_expert_box, action_expert_label)
        action_expert_group.scale(0.9)
        action_expert_group.move_to([3.3, -2.9, 0])
        self.wait()
        self.play(ShowCreation(action_expert_box), Write(action_expert_label), FadeIn(pi0_logo), run_time=3)
        all_svgs[27].move_to([-5.2, -6, 0])
        lil_arrow = all_svgs[1][-2:].copy()
        lil_arrow.move_to([-3.6, -6, 0])
        arm_img = ImageMobject(str(hacking_dir / 'arm_1.png'))
        arm_img_flipped = ImageMobject(str(hacking_dir / 'arm_1_flipped.png'))
        arm_img_flipped.scale(0.52)
        arm_img_flipped.move_to([-5.78, -5.97, 0])
        arm_img.scale(0.52)
        arm_img.move_to([-4.6, -5.97, 0])
        all_svgs[28].move_to([-5.2, -6, 0])
        self.wait()
        self.play(FadeOut(pi0_logo), self.frame.animate.reorient(0, 0, 0, (-3.52, -5.97, 0.0), 3.73), FadeIn(all_svgs[27]), Write(lil_arrow), action_expert_group.animate.move_to([-1.9, -6, 0]), FadeIn(arm_img), FadeIn(arm_img_flipped), FadeIn(all_svgs[28][-40:-15]), FadeIn(all_svgs[28][-58:-40]), run_time=5)
        self.wait()
        self.add(all_svgs[28][-79:-76])
        self.wait()
        self.add(all_svgs[28][-61:-58])
        self.wait()
        self.add(all_svgs[28][-64:-61])
        self.wait()
        self.add(all_svgs[28][-67:-64])
        self.wait()
        self.add(all_svgs[28][-70:-67])
        self.wait()
        self.add(all_svgs[28][-73:-70])
        self.wait()
        self.add(all_svgs[28][-76:-73])
        self.wait()
        self.add(all_svgs[28][:-76])
        self.wait()
        self.play(Write(all_svgs[28][-15:]), run_time=3)
        self.wait()
        all_svgs[29].move_to([-3.05, -4.8, 0])
        all_svgs[30].move_to([-1.53, -6.7, 0])
        all_svgs[31].move_to([-4.25, -6.765, 0])
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (3.41, -1.81, 0.0), 12.27), run_time=5)
        self.wait()
        self.remove(action_expert_group, lil_arrow)
        self.play(self.frame.animate.reorient(0, 0, 0, (-2.03, -6.66, 0.0), 5.33), Write(all_svgs[29]), Write(all_svgs[30]), run_time=5)
        self.wait()
        embedding_rows_action_expert = VGroup()
        vertical_spacing = 0.2
        for i in range(20):
            if i == 9:
                ellipsis_dots_action_expert_1 = VGroup(*[Dot(radius=0.02).set_color(CHILL_BROWN) for _ in range(3)])
                ellipsis_dots_action_expert_1.arrange(DOWN, buff=0.03)
                ellipsis_dots_action_expert_1.next_to(flat_rect, DOWN, buff=0.09)
                embedding_rows_action_expert.add(ellipsis_dots_action_expert_1)
                continue
            flat_rect = Rectangle(width=1.1, height=0.03)
            if i == 0:
                flat_rect.set_fill(RED, opacity=1)
            else:
                flat_rect.set_fill(PINK, opacity=1)
            flat_rect.set_stroke(width=0)
            flat_rect.move_to([-1.5, -4.7 - i * vertical_spacing, 0])
            embedding_rows_action_expert.add(flat_rect)
        self.wait()
        self.play(ReplacementTransform(all_svgs[28][-15:].copy(), embedding_rows_action_expert[0]), run_time=3)
        self.wait()
        self.play(Write(all_svgs[31]), ShowCreation(embedding_rows_action_expert[1:]), run_time=5)
        self.wait()
        self.wait(20)
        self.embed()

class P43a1(InteractiveScene):

    def construct(self):
        hacking_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/vla/hackin')
        composited_dir = hacking_dir / 'p43_patchified'
        total_height = 2.72
        grid_n = 16
        patch_size = total_height / grid_n
        gap_factor = 0.12
        scale = 1 + gap_factor
        all_attn_values = np.load(hacking_dir / 'p42_1/p42_1.npy')
        max_opacities = [0.5, 0.95, 0.95]
        xs = [(j - 8 + 0.5) * patch_size * scale for j in range(16)]
        ys = [-(i - 8 + 0.5) * patch_size * scale for i in range(2, 14)]
        canvas_w_manim = max(xs) - min(xs) + patch_size
        canvas_h_manim = max(ys) - min(ys) + patch_size
        display_imgs = Group()
        img_gap = 0.3
        target_h = 3.5
        for k in range(3):
            img = ImageMobject(str(composited_dir / f'0_{k}.png'))
            img.set_height(target_h)
            display_imgs.add(img)
        w = display_imgs[0].get_width()
        display_imgs[0].move_to([-(w + img_gap), 0, 0])
        display_imgs[1].move_to([0, 0, 0])
        display_imgs[2].move_to([w + img_gap, 0, 0])
        s = target_h / canvas_h_manim
        scaled_patch = patch_size * s
        magenta_overlays = Group()
        for k in range(3):
            overlays_k = Group()
            img_center = display_imgs[k].get_center()
            for i in range(2, 14):
                for j in range(16):
                    cx = (j - 8 + 0.5) * patch_size * scale * s
                    cy = -(i - 8 + 0.5) * patch_size * scale * s
                    sq = Square(side_length=scaled_patch)
                    sq.set_fill(MAGENTA, opacity=0)
                    sq.set_stroke(width=0)
                    sq.move_to(img_center + np.array([cx, cy, 0]))
                    overlays_k.add(sq)
            magenta_overlays.add(overlays_k)
        self.add(display_imgs, magenta_overlays)
        self.frame.reorient(0, 0, 0, (0.01, 0.03, 0.0), 8.66)
        for frame_idx in range(150, 300):
            attn_row = all_attn_values[frame_idx]
            cams = [attn_row[:256].reshape(16, 16), attn_row[256:512].reshape(16, 16), attn_row[512:768].reshape(16, 16)]
            for k in range(3):
                path = composited_dir / f'{frame_idx}_{k}.png'
                if not path.exists():
                    continue
                pos = display_imgs[k].get_center()
                h = display_imgs[k].get_height()
                old_img = display_imgs[k]
                if hasattr(old_img, 'image') and hasattr(old_img.image, 'close'):
                    old_img.image.close()
                self.remove(old_img)
                new_img = ImageMobject(str(path))
                new_img.set_height(h)
                new_img.move_to(pos)
                display_imgs.submobjects[k] = new_img
                self.add(new_img)
                self.remove(magenta_overlays)
                self.add(magenta_overlays)
                del old_img
                cam = cams[k][2:14, :]
                sc = cam.max() if cam.max() > 0 else 1.0
                mo = max_opacities[k]
                for idx in range(len(magenta_overlays[k])):
                    row, col = (idx // 16, idx % 16)
                    attn_val = cam[row, col]
                    opacity = min(mo, mo * (attn_val / sc))
                    magenta_overlays[k][idx].set_fill(opacity=float(opacity))
            self.wait(1 / 15)
        self.wait()

class P43b2(InteractiveScene):

    def construct(self):
        hacking_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/vla/hackin')
        composited_dir = hacking_dir / 'p43_patchified'
        total_height = 2.72
        grid_n = 16
        patch_size = total_height / grid_n
        gap_factor = 0.12
        scale = 1 + gap_factor
        all_attn_values = np.load(hacking_dir / 'p42_1/p42_1.npy')
        max_opacities = [0.5, 0.95, 0.95]
        xs = [(j - 8 + 0.5) * patch_size * scale for j in range(16)]
        ys = [-(i - 8 + 0.5) * patch_size * scale for i in range(2, 14)]
        canvas_w_manim = max(xs) - min(xs) + patch_size
        canvas_h_manim = max(ys) - min(ys) + patch_size
        display_imgs = Group()
        img_gap = 0.3
        target_h = 3.5
        for k in range(3):
            img = ImageMobject(str(composited_dir / f'0_{k}.png'))
            img.set_height(target_h)
            display_imgs.add(img)
        w = display_imgs[0].get_width()
        display_imgs[0].move_to([-(w + img_gap), 0, 0])
        display_imgs[1].move_to([0, 0, 0])
        display_imgs[2].move_to([w + img_gap, 0, 0])
        s = target_h / canvas_h_manim
        scaled_patch = patch_size * s
        magenta_overlays = Group()
        for k in range(3):
            overlays_k = Group()
            img_center = display_imgs[k].get_center()
            for i in range(2, 14):
                for j in range(16):
                    cx = (j - 8 + 0.5) * patch_size * scale * s
                    cy = -(i - 8 + 0.5) * patch_size * scale * s
                    sq = Square(side_length=scaled_patch)
                    sq.set_fill(MAGENTA, opacity=0)
                    sq.set_stroke(width=0)
                    sq.move_to(img_center + np.array([cx, cy, 0]))
                    overlays_k.add(sq)
            magenta_overlays.add(overlays_k)
        self.frame.reorient(0, 0, 0, (0.01, 0.03, 0.0), 8.66)
        self.add(display_imgs, magenta_overlays)
        for frame_idx in range(0, 151):
            attn_row = all_attn_values[frame_idx]
            cams = [attn_row[:256].reshape(16, 16), attn_row[256:512].reshape(16, 16), attn_row[512:768].reshape(16, 16)]
            for k in range(3):
                path = composited_dir / f'{frame_idx}_{k}.png'
                if not path.exists():
                    continue
                pos = display_imgs[k].get_center()
                h = display_imgs[k].get_height()
                old_img = display_imgs[k]
                if hasattr(old_img, 'image') and hasattr(old_img.image, 'close'):
                    old_img.image.close()
                self.remove(old_img)
                new_img = ImageMobject(str(path))
                new_img.set_height(h)
                new_img.move_to(pos)
                display_imgs.submobjects[k] = new_img
                self.add(new_img)
                self.remove(magenta_overlays)
                self.add(magenta_overlays)
                del old_img
                cam = cams[k][2:14, :]
                sc = cam.max() if cam.max() > 0 else 1.0
                mo = max_opacities[k]
                for idx in range(len(magenta_overlays[k])):
                    row, col = (idx // 16, idx % 16)
                    attn_val = cam[row, col]
                    opacity = min(mo, mo * (attn_val / sc))
                    magenta_overlays[k][idx].set_fill(opacity=float(opacity))
            self.wait(1 / 15)
        self.wait()