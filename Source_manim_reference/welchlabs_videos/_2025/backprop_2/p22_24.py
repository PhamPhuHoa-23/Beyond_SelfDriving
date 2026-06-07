from manimlib import *
sys.path.append('/Users/stephen/manim/videos/welch_assets')
from welch_axes import *
from functools import partial
import numpy as np
import torch
import glob
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'
GREEN = '#00a14b'
svg_path = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backprop2/graphics/to_manim'
data_path = '/Users/stephen/Stephencwelch Dropbox/Stephen Welch/welch_labs/backprop2/hackin'

def format_number(num, total_chars=6, align='right'):
    abs_num = abs(num)
    if abs_num >= 100:
        formatted = f'{num:.0f}'
    elif abs_num >= 10:
        formatted = f'{num:.1f}'
    elif abs_num >= 1:
        formatted = f'{num:.2f}'
    else:
        formatted = f'{num:.2f}'
    if align == 'right':
        return formatted.rjust(total_chars)
    elif align == 'left':
        return formatted.ljust(total_chars)
    else:
        return formatted.center(total_chars)

def format_number_fixed_decimal(num, decimal_places=2, total_chars=6):
    formatted = f'{num:.{decimal_places}f}'
    return formatted.rjust(total_chars)

def get_numbers_2(x, w, logits, yhats):
    numbers = VGroup()
    tx = Tex(str(x) + '^\\circ')
    tx.scale(0.13)
    tx.move_to([-1.49, 0.02, 0])
    numbers.add(tx)
    tm1 = Tex(format_number(w[0], total_chars=6)).set_color('#00FFFF')
    tm1.scale(0.16)
    tm1.move_to([-1.195, 0.205, 0])
    numbers.add(tm1)
    tm2 = Tex(format_number(w[1], total_chars=6)).set_color(YELLOW)
    tm2.scale(0.15)
    tm2.move_to([-1.155, 0.015, 0])
    numbers.add(tm2)
    tm3 = Tex(format_number(w[2], total_chars=6)).set_color(GREEN)
    tm3.scale(0.16)
    tm3.move_to([-1.19, -0.17, 0])
    numbers.add(tm3)
    tb1 = Tex(format_number(w[3], total_chars=6)).set_color('#00FFFF')
    tb1.scale(0.16)
    tb1.move_to([-0.875, 0.365, 0])
    numbers.add(tb1)
    tb2 = Tex(format_number(w[4], total_chars=6)).set_color(YELLOW)
    tb2.scale(0.16)
    tb2.move_to([-0.875, 0.015, 0])
    numbers.add(tb2)
    tb3 = Tex(format_number(w[5], total_chars=6)).set_color(GREEN)
    tb3.scale(0.16)
    tb3.move_to([-0.88, -0.335, 0])
    numbers.add(tb3)
    tl1 = Tex(format_number(logits[0], total_chars=6)).set_color('#00FFFF')
    tl1.scale(0.16)
    tl1.move_to([-0.52, 0.37, 0])
    numbers.add(tl1)
    tl2 = Tex(format_number(logits[1], total_chars=6)).set_color(YELLOW)
    tl2.scale(0.16)
    tl2.move_to([-0.52, 0.015, 0])
    numbers.add(tl2)
    tl3 = Tex(format_number(logits[2], total_chars=6)).set_color(GREEN)
    tl3.scale(0.16)
    tl3.move_to([-0.52, -0.335, 0])
    numbers.add(tl3)
    yhat1 = Tex(f'{yhats[0]:.3f}').set_color('#00FFFF')
    yhat1.scale(0.16)
    yhat1.move_to([0.22, 0.37, 0])
    numbers.add(yhat1)
    yhat2 = Tex(f'{yhats[1]:.3f}').set_color(YELLOW)
    yhat2.scale(0.16)
    yhat2.move_to([0.22, 0.015, 0])
    numbers.add(yhat2)
    yhat3 = Tex(f'{yhats[2]:.3f}').set_color(GREEN)
    yhat3.scale(0.16)
    yhat3.move_to([0.22, -0.335, 0])
    numbers.add(yhat3)
    return numbers

class p22_24(InteractiveScene):

    def construct(self):
        net_background = SVGMobject(svg_path + '/p44_background_1.svg')
        self.add(net_background)
        self.frame.reorient(0, 0, 0, (-0.56, 0.23, 0.0), 1.56)
        data = np.load(data_path + '/cities_1d_2.npy')
        xs = data[:, :2]
        ys = data[:, 2]
        weights = data[:, 3:9]
        grads = data[:, 9:15]
        logits = data[:, 15:18]
        yhats = data[:, 18:]
        x = 2.3514
        w = [1, 0, -1, 0, 0, 0]
        logits = [2.35, 0, -2.35]
        yhats = [0.905, 0.086, 0.008]
        nums = get_numbers_2(x, w, logits, yhats)
        self.add(nums)
        net_background.shift([0, 0.23, 0])
        nums.shift([0, 0.23, 0])
        layers = VGroup()
        for p in sorted(glob.glob(svg_path + '/p22_24/*.svg')):
            layers.add(SVGMobject(p)[1:])
        yhat2 = Tex('0.086').set_color(YELLOW)
        yhat2.scale(0.14)
        yhat2.move_to([1.205, 0.18, 0])
        loss = Tex(format_number(2.45, total_chars=6)).set_color(YELLOW)
        loss.scale(0.16)
        loss.move_to([1.5, 0.18, 0])
        self.wait()
        self.play(self.frame.animate.reorient(0, 0, 0, (0.0, 0.07, 0.0), 1.97), FadeIn(layers[:2]), FadeIn(yhat2), FadeIn(loss), run_time=3)
        self.wait()
        self.play(ShowCreation(layers[3]))
        m2_label = net_background[42:44].copy()
        loss_label = layers[1][:4].copy()
        self.add(m2_label, loss_label)
        self.play(loss_label.animate.scale(0.75).move_to([0.7, 0.05, 0]), run_time=1.0)
        self.play(m2_label.animate.scale(1.2).move_to([1.48, -0.67, 0]), run_time=4.0)
        self.wait()
        m0 = nums[2].copy()
        loss_copy = loss.copy()
        self.play(m0.animate.move_to([0.79, -0.68, 0]), run_time=3.0)
        self.play(loss_copy.animate.move_to([0.7, -0.05, 0]), run_time=1.2)
        self.add(layers[2])
        self.wait()
        box = SurroundingRectangle(nums[2], color=YELLOW, buff=0.025)
        self.play(ShowCreation(box))
        tm2 = Tex(format_number(0.1, total_chars=6)).set_color(YELLOW)
        tm2.scale(0.15)
        tm2.move_to([-1.155, 0.015 + 0.23, 0])
        self.play(Transform(nums[2], tm2))
        self.wait()
        w = [1, 0.1, -1, 0, 0, 0]
        logits = [2.35, 0.24, -2.35]
        yhats = [0.885, 0.107, 0.008]
        nums_2 = get_numbers_2(x, w, logits, yhats)
        nums_2.shift([0, 0.23, 0])
        self.play(*[Transform(nums[i], nums_2[i]) for i in [-6, -5, -4, -3, -2, -1]])
        self.wait()
        yhat2_new = nums_2[-2].copy()
        loss_new = Tex(format_number(2.24, total_chars=6)).set_color(YELLOW)
        loss_new.scale(0.16)
        loss_new.move_to([1.5, 0.18, 0])
        self.play(yhat2_new.animate.scale(0.9).move_to([1.205, 0.18, 0]), FadeOut(yhat2), run_time=2.0)
        self.play(Transform(loss, loss_new))
        self.wait()
        m1 = nums_2[2].copy()
        loss_copy_2 = loss_new.copy()
        self.play(m1.animate.move_to([1.25, -0.68, 0]), run_time=2.0)
        self.play(loss_copy_2.animate.move_to([0.7, -0.49, 0]), run_time=1.0)
        self.add(layers[4])
        self.wait()
        self.play(FadeIn(layers[5]))
        self.wait()
        self.play(FadeIn(layers[6]))
        self.wait()
        net = VGroup(net_background, nums)
        plot_to_move = VGroup(layers[2:5], m2_label, loss_label)
        self.wait()
        self.remove(box)
        nums[-6:].set_color(CHILL_BROWN)
        nums[0].set_color(CHILL_BROWN)
        self.play(FadeOut(layers[0:2]), FadeOut(layers[5:7]), FadeOut(loss_copy_2), FadeOut(m1), FadeOut(m0), FadeOut(loss_copy), FadeOut(loss_new), FadeOut(loss), FadeOut(yhat2_new), net.animate.scale(0.78).move_to([0.38, 0.018, 0]), plot_to_move.animate.scale(0.58).move_to([-0.68, 0.645, 0]), self.frame.animate.reorient(0, 0, 0, (-0.05, -0.02, 0.0), 2.0), run_time=3.0)
        self.add(layers[7])
        self.add(layers[8])
        self.remove(plot_to_move)
        self.wait()
        self.play(ShowCreation(layers[9]))
        self.wait()
        m2_plot = layers[8][-21:]
        self.play(FadeOut(layers[8][:-21]), FadeOut(layers[7]), FadeOut(layers[9]), FadeOut(net))
        self.play(m2_plot.animate.scale(2.2).move_to([-0.19, -0.015, 0]), run_time=1.5)
        self.add(layers[10])
        self.wait()
        self.wait()
        self.embed()