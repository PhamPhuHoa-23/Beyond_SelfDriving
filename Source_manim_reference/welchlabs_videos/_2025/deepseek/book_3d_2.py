from manimlib import *
from tqdm import tqdm
from pathlib import Path
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
from manimlib.mobject.svg.svg_mobject import _convert_point_to_3d
from manimlib.logger import log

def get_attention_head(svg_path='/Users/stephen/welch_labs/deepseek/graphics/to_manim', svg_file='mha_2d_segments-', img_path='/Users/stephen/welch_labs/deepseek/hackin/linux_workdir/deepseek/flowchart_graphics'):
    q1 = ImageMobject(str(img_path / 'q_1.png'))
    q1.scale([0.0415, 0.08, 1])
    q1.move_to([-0.2, 0.38, 0])
    k1 = ImageMobject(str(img_path / 'k_1.png'))
    k1.scale([0.0415, 0.08, 1])
    k1.move_to([-0.2, -0.06, 0])
    v1 = ImageMobject(str(img_path / 'v_1.png'))
    v1.scale([0.0415, 0.08, 1])
    v1.move_to([-0.2, -0.48, 0])
    kt = ImageMobject(str(img_path / 'k_1.png'))
    kt.scale([0.0215, 0.035, 1])
    kt.rotate([0, 0, -PI / 2])
    kt.move_to([0.405, 0.305, 0])
    a1 = ImageMobject(str(img_path / 'attention_scores.png'))
    a1.scale([0.055, 0.055, 1])
    a1.move_to([0.66, 0.37, 0])
    a2 = ImageMobject(str(img_path / 'attention_pattern.png'))
    a2.scale([0.13, 0.13, 1])
    a2.move_to([1.27, 0.25, 0])
    z1 = ImageMobject(str(img_path / 'z_1.png'))
    z1.scale([0.0425, 0.08, 1])
    z1.move_to([1.035, -0.48, 0])
    all_images = Group(q1, k1, v1, kt, a1, a2, z1)
    svg_files = list(sorted(svg_path.glob('*' + svg_file + '*')))
    all_labels = Group()
    for svg_file in svg_files:
        svg_image = SVGMobject(str(svg_file))
        all_labels.add(svg_image[1:])
    large_white_connectors = SVGMobject(str(svg_path / 'mha_2d_large_white_connectors_2.svg'))
    return Group(all_images, all_labels, large_white_connectors[1:])

class book_3d_2(InteractiveScene):

    def construct(self):
        img_path = Path('/Users/stephen/welch_labs/deepseek/hackin/linux_workdir/deepseek')
        svg_path = Path('/Users/stephen/welch_labs/deepseek/graphics/to_manim')
        attention_heads = Group()
        spacing = 0.25
        for i in range(12):
            a = get_attention_head(svg_path=svg_path, svg_file='mha_2d_segments-', img_path=img_path / 'gpt_2_attention_viz_1' / str(i))
            a.rotate([PI / 2, 0, 0], axis=RIGHT)
            a.move_to([0, spacing * i, 0])
            attention_heads.add(a)
        for i in range(11, 0, -1):
            self.add(attention_heads[i][1][13].set_opacity(1.0))
            self.add(attention_heads[i][0][0].set_opacity(1.0))
            self.add(attention_heads[i][0][1].set_opacity(1.0))
            self.add(attention_heads[i][0][2].set_opacity(1.0))
            self.add(attention_heads[i][0][3:].set_opacity(1.0))
        self.add(attention_heads[0][0][3:].set_opacity(1.0))
        self.add(attention_heads[0][1][13].set_opacity(1.0))
        self.add(attention_heads[0][0][0].set_opacity(1.0))
        self.add(attention_heads[0][0][1].set_opacity(1.0))
        self.add(attention_heads[0][0][2].set_opacity(1.0))
        self.add(attention_heads[0][1][3].set_opacity(1.0))
        self.add(attention_heads[0][1][4].set_opacity(1.0))
        self.add(attention_heads[0][1][5].set_opacity(1.0))
        self.add(attention_heads[0][1][14].set_opacity(1.0))
        self.frame.reorient(0, 82, 0, (0.45, -0.07, -0.02), 1.43)
        self.wait()
        self.play(self.frame.animate.reorient(0, 83, 0, (0.37, -0.06, 0.01), 2.04), run_time=3)
        self.wait()
        self.play(*[attention_heads[i][0][0].animate.set_opacity(0.0) for i in range(12)] + [attention_heads[0][1][3].animate.set_opacity(0.0)] + [attention_heads[i][0][1].animate.move_to([-0.6, 1.391, -0.08]) for i in range(12)] + [attention_heads[0][1][4].animate.move_to([-0.6, 1.391, -0.24])] + [attention_heads[i][0][2].animate.move_to([-0.6, 1.391, -0.48]) for i in range(12)] + [attention_heads[0][1][5].animate.move_to([-0.6, 1.391, -0.65])] + [self.frame.animate.reorient(-53, 71, 0, (-0.36, 0.7, 0.07), 1.81)], run_time=5)
        connector_1 = SVGMobject('/Users/stephen/welch_labs/deepseek/graphics/to_manim/thick_white_connector_1.svg')
        connector_1.scale([1.0, 1.39, 1])
        connector_1.move_to([0.2, 1.389, -0.11])
        connector_1b = SVGMobject('/Users/stephen/welch_labs/deepseek/graphics/to_manim/thick_white_connector_1.svg')
        connector_1b.scale([1.0, 1.39, 1])
        connector_1b.move_to([0.14, 1.386, -0.499])
        white_arrows = Group(*[attention_heads[i][2] for i in range(12)])
        self.play(FadeIn(connector_1b), FadeIn(connector_1), FadeIn(white_arrows), self.frame.animate.reorient(-34, 69, 0, (0.04, 0.58, 0.09), 2.1), run_time=3)
        self.add(attention_heads[0][0][1])
        self.add(attention_heads[0][0][2])
        self.wait()
        self.frame.reorient(-38, 59, 0, (0.12, 0.93, -0.18), 2.93)
        self.wait()
        self.frame.reorient(-33, 69, 0, (0.26, 0.84, -0.18), 2.42)
        self.wait()
        self.frame.reorient(-38, 66, 0, (0.28, 0.84, -0.15), 2.31)
        self.wait()
        self.wait(20)
        self.embed()