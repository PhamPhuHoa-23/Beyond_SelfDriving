from manimlib import *
import os
import scipy.special
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
YELLOW_FADE = '#7f6a2d'
BLUE = '#65c8d0'
GREEN = '#00a14b'
CHILL_GREEN = '#6c946f'
CHILL_BLUE = '#3d5c6f'
FRESH_TAN = '#dfd0b9'
CYAN = '#00FFFF'
TEST_BLUE = '#008080'
graphics_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/double_descent/graphics/'
svg_dir = '/Users/stephen/Stephencwelch Dropbox/welch_labs/double_descent/graphics/to_manim'

def fit_legendre_pinv(x_train, y_train, degree, x_min=-2, x_max=2):
    x_scaled = 2 * (x_train - x_min) / (x_max - x_min) - 1
    feature_degrees = np.arange(degree + 1)[:, None]
    X_train_poly = scipy.special.eval_legendre(feature_degrees, x_scaled).T
    beta_hat = np.linalg.pinv(X_train_poly) @ y_train
    return beta_hat

def eval_legendre_poly(beta, x, degree, x_min=-2, x_max=2):
    x_scaled = 2 * (x - x_min) / (x_max - x_min) - 1
    feature_degrees = np.arange(degree + 1)[:, None]
    X_poly = scipy.special.eval_legendre(feature_degrees, x_scaled).T
    return X_poly @ beta

def get_noisy_data(n_points=10, noise_level=0.2, random_seed=428):
    np.random.seed(random_seed)
    x = np.random.uniform(-2, 2, n_points)
    y = f(x) + noise_level * np.random.randn(n_points)
    return (x, y)

def f(x):
    return 0.5 * x ** 2

class p20_2(InteractiveScene):

    def construct(self):
        random_seed = 428
        n_points = 10
        noise_level = 0.2
        curve_fit_axis_svg = SVGMobject(svg_dir + '/p8_15_2a.svg')[1:]
        curve_fit_axis_svg.scale(4.0)
        curve_fit_axis_svg.move_to([-2.86, 0.6, 0])
        all_x = np.linspace(-2, 2, 128)
        all_y = f(all_x)
        n_train_points = int(np.floor(n_points * 0.5))
        n_test_points = n_points - n_train_points
        x, y = get_noisy_data(n_points, noise_level, random_seed)
        x_train, y_train = (x[:n_train_points], y[:n_train_points])
        x_test, y_test = (x[n_train_points:], y[n_train_points:])
        axes_1 = Axes(x_range=[-2.0, 2.0, 1], y_range=[-0.5, 2.0, 1], width=6, height=5, axis_config={'color': CHILL_BROWN, 'include_ticks': True, 'include_numbers': True, 'include_tip': True, 'stroke_width': 3, 'tip_config': {'width': 0.02, 'length': 0.02}})
        axes_1.move_to([-3, 0, 0])
        parabola = axes_1.get_graph(lambda x: f(x), x_range=[-2, 2], color=CHILL_BROWN)
        parabola.set_stroke(width=3)
        train_dots = VGroup(*[Dot(axes_1.c2p(x_train[i], y_train[i]), radius=0.08) for i in range(len(x_train))])
        test_dots = VGroup(*[Dot(axes_1.c2p(x_test[i], y_test[i]), radius=0.08) for i in range(len(x_test))])
        all_dots = VGroup(test_dots, train_dots)
        all_dots.set_color(YELLOW)
        test_dots.set_color('#008080')
        dots_with_x = []
        for i, dot in enumerate(train_dots):
            dots_with_x.append((x_train[i], dot, 'train'))
        for i, dot in enumerate(test_dots):
            dots_with_x.append((x_test[i], dot, 'test'))
        dots_with_x.sort(key=lambda item: item[0])
        sorted_dots = [item[1] for item in dots_with_x]
        legend = VGroup()
        legend_training_dot = Dot(radius=0.06).set_color(YELLOW)
        legend_training_text = Text('Training Data', font_size=20, font='myraid-pro').set_color(CHILL_BROWN)
        legend_training = VGroup(legend_training_dot, legend_training_text).arrange(RIGHT, buff=0.15, aligned_edge=ORIGIN)
        legend_testing_dot = Dot(radius=0.06).set_color(TEST_BLUE)
        legend_testing_text = Text('Testing Data', font_size=20, font='myraid-pro').set_color(CHILL_BROWN)
        legend_testing = VGroup(legend_testing_dot, legend_testing_text).arrange(RIGHT, buff=0.15, aligned_edge=ORIGIN)
        legend_target_line = Line(LEFT * 0.2, RIGHT * 0.2, color=CHILL_BROWN, stroke_width=3)
        legend_target_text = Text('Target Function', font_size=20, font='myraid-pro').set_color(CHILL_BROWN)
        legend_target = VGroup(legend_target_line, legend_target_text).arrange(RIGHT, buff=0.15, aligned_edge=ORIGIN)
        legend_items = VGroup(legend_training, legend_testing, legend_target).arrange(RIGHT, buff=0.4)
        legend_box = RoundedRectangle(width=legend_items.get_width() + 0.5, height=legend_items.get_height() + 0.35, corner_radius=0.08, stroke_color=CHILL_BROWN, stroke_width=2, fill_color=None, fill_opacity=0.0)
        legend_box.set_stroke(opacity=0.7)
        legend_items.move_to(legend_box.get_center())
        legend.add(legend_box, legend_items)
        legend.scale(0.85)
        legend.move_to([-3, -3.2, 0])
        self.frame.reorient(0, 0, 0, (-3.21, 0.36, 0.0), 7.45)
        self.add(curve_fit_axis_svg, parabola, all_dots)
        self.wait()
        all_fits = np.load('/Users/stephen/Stephencwelch Dropbox/welch_labs/double_descent/graphics/regularization_fits_oct_15_1.npy')
        all_fit_lines = VGroup()
        for fit in all_fits:
            fit_points = [axes_1.c2p(all_x[i], fit[i]) for i in range(len(all_x))]
            fit_line = VMobject(color=ORANGE, stroke_width=3)
            fit_line.set_points_smoothly(fit_points)
            all_fit_lines.add(fit_line)
        lambdas = np.arange(0, 0.31, 0.01)
        lambda_display = Tex('\\lambda = 0.00', font_size=36).set_color(ORANGE)
        lambda_display.move_to([1.5, 0.5, 0])
        self.add(lambda_display)
        self.play(ShowCreation(all_fit_lines[0]), run_time=2)
        self.wait()
        for i, (lambd, fit_line) in enumerate(zip(lambdas, all_fit_lines)):
            new_lambda_display = Tex(f'\\lambda = {lambd:.2f}', font_size=36).set_color(ORANGE)
            new_lambda_display.move_to([1.5, 0.5, 0])
            if i == 0:
                self.remove(all_fit_lines[0])
                self.add(fit_line)
                self.remove(lambda_display)
                self.add(new_lambda_display)
            else:
                prev_fit_line = all_fit_lines[i - 1]
                self.remove(lambda_display)
                self.add(new_lambda_display)
                self.play(prev_fit_line.animate.set_stroke(opacity=0.12), FadeIn(fit_line), run_time=0.3)
            lambda_display = new_lambda_display
            self.wait(0.1)
        self.wait(20)
        self.embed()