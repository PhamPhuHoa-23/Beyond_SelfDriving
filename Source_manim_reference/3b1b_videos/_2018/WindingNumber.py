from manim_imports_ext import *
import warnings
warnings.warn('\n    Warning: This file makes use of\n    ContinualAnimation, which has since\n    been deprecated\n')
import time
import mpmath
mpmath.mp.dps = 7
UL = UP + LEFT
UR = UP + RIGHT
DL = DOWN + LEFT
DR = DOWN + RIGHT
standard_rect = np.array([UL, UR, DR, DL])
border_stroke_width = 10
cw_circle = Circle(color=WHITE).stretch(-1, 0)
WALKER_LIGHT_COLOR = GREY_D
ODOMETER_RADIUS = 1.5
ODOMETER_STROKE_WIDTH = 20

def rev_to_rgba(alpha):
    alpha = (0.5 - alpha) % 1
    hue_list = [0, 0.5 / 6.0, 1 / 6.0, 1.1 / 6.0, 2 / 6.0, 3 / 6.0, 4 / 6.0, 5 / 6.0]
    num_hues = len(hue_list)
    start_index = int(np.floor(num_hues * alpha)) % num_hues
    end_index = (start_index + 1) % num_hues
    beta = alpha % (1.0 / num_hues) * num_hues
    start_hue = hue_list[start_index]
    end_hue = hue_list[end_index]
    if end_hue < start_hue:
        end_hue = end_hue + 1
    hue = interpolate(start_hue, end_hue, beta)
    return color_to_rgba(Color(hue=hue, saturation=1, luminance=0.5))

def rev_to_color(alpha):
    return rgba_to_color(rev_to_rgba(alpha))

def point_to_rev(xxx_todo_changeme6, allow_origin=False):
    x, y = xxx_todo_changeme6
    if not allow_origin and (x, y) == (0, 0):
        print('Error! Angle of (0, 0) computed!')
        return
    return fdiv(np.arctan2(y, x), TAU)

def point_to_size(xxx_todo_changeme7):
    x, y = xxx_todo_changeme7
    return np.sqrt(x ** 2 + y ** 2)

def point_to_rescaled_size(p):
    base_size = point_to_size(p)
    return np.sqrt(fdiv(base_size, base_size + 1))

def point_to_rgba(point):
    rev = point_to_rev(point, allow_origin=True)
    rgba = rev_to_rgba(rev)
    rescaled_size = point_to_rescaled_size(point)
    return rgba * [rescaled_size, rescaled_size, rescaled_size, 1]
positive_color = rev_to_color(0)
negative_color = rev_to_color(0.5)
neutral_color = rev_to_color(0.25)

class EquationSolver1d(GraphScene, ZoomedScene):
    CONFIG = {'camera_config': {'use_z_coordinate_for_display_order': True}, 'func': lambda x: x, 'targetX': 0, 'targetY': 0, 'initial_lower_x': 0, 'initial_upper_x': 10, 'num_iterations': 10, 'iteration_at_which_to_start_zoom': None, 'graph_label': None, 'show_target_line': True, 'base_line_y': 0, 'show_y_as_deviation': False}

    def drawGraph(self):
        self.setup_axes()
        self.graph = self.get_graph(self.func)
        self.add(self.graph)
        if self.graph_label != None:
            curve_label = self.get_graph_label(self.graph, self.graph_label, x_val=4, direction=LEFT)
            curve_label.shift(LEFT)
            self.add(curve_label)
        if self.show_target_line:
            target_line_object = DashedLine(self.coords_to_point(self.x_min, self.targetY), self.coords_to_point(self.x_max, self.targetY), dash_length=0.1)
            self.add(target_line_object)
            target_label_num = 0 if self.show_y_as_deviation else self.targetY
            target_line_label = OldTex('y = ' + str(target_label_num))
            target_line_label.next_to(target_line_object.get_left(), UP + RIGHT)
            self.add(target_line_label)
        self.wait()
        if self.show_target_line:
            self.play(FadeOut(target_line_label))
        print('For reference, graphOrigin: ', self.coords_to_point(0, 0))
        print('targetYPoint: ', self.coords_to_point(0, self.targetY))

    def solveEquation(self):

        def color_by_comparison(val, ref):
            if val > ref:
                return positive_color
            elif val < ref:
                return negative_color
            else:
                return neutral_color
        lower_color = color_by_comparison(self.func(self.initial_lower_x), self.targetY)
        upper_color = color_by_comparison(self.func(self.initial_upper_x), self.targetY)
        if self.show_y_as_deviation:
            y_bias = -self.targetY
        else:
            y_bias = 0
        startBrace = OldTex('|', stroke_width=10)
        startBrace.set_color(lower_color)
        endBrace = startBrace.copy().stretch(-1, 0)
        endBrace.set_color(upper_color)
        genericBraces = Group(startBrace, endBrace)
        leftBrace = startBrace.copy()
        rightBrace = endBrace.copy()
        xBraces = Group(leftBrace, rightBrace)
        downBrace = startBrace.copy()
        upBrace = endBrace.copy()
        yBraces = Group(downBrace, upBrace)
        yBraces.rotate(TAU / 4)
        lowerX = self.initial_lower_x
        lowerY = self.func(lowerX)
        upperX = self.initial_upper_x
        upperY = self.func(upperX)
        leftBrace.move_to(self.coords_to_point(lowerX, self.base_line_y))
        leftBraceLabel = DecimalNumber(lowerX)
        leftBraceLabel.next_to(leftBrace, DOWN + LEFT, buff=SMALL_BUFF)
        leftBraceLabelAnimation = ContinualChangingDecimal(leftBraceLabel, lambda alpha: self.point_to_coords(leftBrace.get_center())[0], tracked_mobject=leftBrace)
        rightBrace.move_to(self.coords_to_point(upperX, self.base_line_y))
        rightBraceLabel = DecimalNumber(upperX)
        rightBraceLabel.next_to(rightBrace, DOWN + RIGHT, buff=SMALL_BUFF)
        rightBraceLabelAnimation = ContinualChangingDecimal(rightBraceLabel, lambda alpha: self.point_to_coords(rightBrace.get_center())[0], tracked_mobject=rightBrace)
        downBrace.move_to(self.coords_to_point(0, lowerY))
        downBraceLabel = DecimalNumber(lowerY)
        downBraceLabel.next_to(downBrace, LEFT + DOWN, buff=SMALL_BUFF)
        downBraceLabelAnimation = ContinualChangingDecimal(downBraceLabel, lambda alpha: self.point_to_coords(downBrace.get_center())[1] + y_bias, tracked_mobject=downBrace)
        upBrace.move_to(self.coords_to_point(0, upperY))
        upBraceLabel = DecimalNumber(upperY)
        upBraceLabel.next_to(upBrace, LEFT + UP, buff=SMALL_BUFF)
        upBraceLabelAnimation = ContinualChangingDecimal(upBraceLabel, lambda alpha: self.point_to_coords(upBrace.get_center())[1] + y_bias, tracked_mobject=upBrace)
        lowerDotPoint = self.input_to_graph_point(lowerX, self.graph)
        lowerDotXPoint = self.coords_to_point(lowerX, self.base_line_y)
        lowerDotYPoint = self.coords_to_point(0, self.func(lowerX))
        lowerDot = Dot(lowerDotPoint + OUT, color=lower_color)
        upperDotPoint = self.input_to_graph_point(upperX, self.graph)
        upperDot = Dot(upperDotPoint + OUT, color=upper_color)
        upperDotXPoint = self.coords_to_point(upperX, self.base_line_y)
        upperDotYPoint = self.coords_to_point(0, self.func(upperX))
        lowerXLine = Line(lowerDotXPoint, lowerDotPoint, color=lower_color)
        upperXLine = Line(upperDotXPoint, upperDotPoint, color=upper_color)
        lowerYLine = Line(lowerDotPoint, lowerDotYPoint, color=lower_color)
        upperYLine = Line(upperDotPoint, upperDotYPoint, color=upper_color)
        x_guess_line = Line(lowerDotXPoint, upperDotXPoint, color=WHITE, stroke_width=10)
        lowerGroup = Group(lowerDot, leftBrace, downBrace, lowerXLine, lowerYLine, x_guess_line)
        upperGroup = Group(upperDot, rightBrace, upBrace, upperXLine, upperYLine, x_guess_line)
        initialLowerXDot = Dot(lowerDotXPoint + OUT, color=lower_color)
        initialUpperXDot = Dot(upperDotXPoint + OUT, color=upper_color)
        initialLowerYDot = Dot(lowerDotYPoint + OUT, color=lower_color)
        initialUpperYDot = Dot(upperDotYPoint + OUT, color=upper_color)
        self.play(FadeIn(initialLowerXDot), FadeIn(leftBrace), FadeIn(leftBraceLabel))
        self.add_foreground_mobjects(initialLowerXDot, leftBrace)
        self.add(leftBraceLabelAnimation)
        self.play(ShowCreation(lowerXLine))
        self.add_foreground_mobject(lowerDot)
        self.play(ShowCreation(lowerYLine))
        self.play(FadeIn(initialLowerYDot), FadeIn(downBrace), FadeIn(downBraceLabel))
        self.add_foreground_mobjects(initialLowerYDot, downBrace)
        self.add(downBraceLabelAnimation)
        self.wait()
        self.play(FadeIn(initialUpperXDot), FadeIn(rightBrace), FadeIn(rightBraceLabel))
        self.add_foreground_mobjects(initialUpperXDot, rightBrace)
        self.add(rightBraceLabelAnimation)
        self.play(ShowCreation(upperXLine))
        self.add_foreground_mobject(upperDot)
        self.play(ShowCreation(upperYLine))
        self.play(FadeIn(initialUpperYDot), FadeIn(upBrace), FadeIn(upBraceLabel))
        self.add_foreground_mobjects(initialUpperYDot, upBrace)
        self.add(upBraceLabelAnimation)
        self.wait()
        self.play(FadeIn(x_guess_line))
        self.wait()
        for i in range(self.num_iterations):
            if i == self.iteration_at_which_to_start_zoom:
                self.activate_zooming()
                self.little_rectangle.move_to(self.coords_to_point(self.targetX, self.targetY))
                inverseZoomFactor = 1 / float(self.zoom_factor)
                self.play(lowerDot.scale, inverseZoomFactor, upperDot.scale, inverseZoomFactor)

            def makeUpdater(xAtStart, fixed_guess_x):

                def updater(group, alpha):
                    dot, xBrace, yBrace, xLine, yLine, guess_line = group
                    newX = interpolate(xAtStart, midX, alpha)
                    newY = self.func(newX)
                    graphPoint = self.input_to_graph_point(newX, self.graph)
                    dot.move_to(graphPoint)
                    xAxisPoint = self.coords_to_point(newX, self.base_line_y)
                    xBrace.move_to(xAxisPoint)
                    yAxisPoint = self.coords_to_point(0, newY)
                    yBrace.move_to(yAxisPoint)
                    xLine.put_start_and_end_on(xAxisPoint, graphPoint)
                    yLine.put_start_and_end_on(yAxisPoint, graphPoint)
                    fixed_guess_point = self.coords_to_point(fixed_guess_x, self.base_line_y)
                    guess_line.put_start_and_end_on(xAxisPoint, fixed_guess_point)
                    return group
                return updater
            midX = (lowerX + upperX) / float(2)
            midY = self.func(midX)
            in_negative_branch = midY < self.targetY
            sign_color = negative_color if in_negative_branch else positive_color
            midCoords = self.coords_to_point(midX, midY)
            midColor = neutral_color
            midXBrace = startBrace.copy()
            midXBrace.set_color(midColor)
            midXBrace.move_to(self.coords_to_point(midX, self.base_line_y) + OUT)
            midXPoint = Dot(self.coords_to_point(midX, self.base_line_y) + OUT, color=sign_color)
            x_guess_label_caption = OldTexText('New guess: x = ', fill_color=midColor)
            x_guess_label_num = DecimalNumber(midX, fill_color=midColor)
            x_guess_label_num.move_to(0.9 * FRAME_Y_RADIUS * DOWN)
            x_guess_label_caption.next_to(x_guess_label_num, LEFT)
            x_guess_label = Group(x_guess_label_caption, x_guess_label_num)
            y_guess_label_caption = OldTexText(', y = ', fill_color=midColor)
            y_guess_label_num = DecimalNumber(midY, fill_color=sign_color)
            y_guess_label_caption.next_to(x_guess_label_num, RIGHT)
            y_guess_label_num.next_to(y_guess_label_caption, RIGHT)
            y_guess_label = Group(y_guess_label_caption, y_guess_label_num)
            guess_labels = Group(x_guess_label, y_guess_label)
            self.play(ReplacementTransform(leftBrace.copy(), midXBrace), ReplacementTransform(rightBrace.copy(), midXBrace), FadeIn(x_guess_label))
            self.add_foreground_mobject(midXBrace)
            midXLine = DashedLine(self.coords_to_point(midX, self.base_line_y), midCoords, color=midColor)
            self.play(ShowCreation(midXLine))
            midDot = Dot(midCoords, color=sign_color)
            if self.iteration_at_which_to_start_zoom != None and i >= self.iteration_at_which_to_start_zoom:
                midDot.scale(inverseZoomFactor)
            self.add(midDot)
            midYLine = DashedLine(midCoords, self.coords_to_point(0, midY), color=sign_color)
            self.play(ShowCreation(midYLine), FadeIn(y_guess_label), ApplyMethod(midXBrace.set_color, sign_color), ApplyMethod(midXLine.set_color, sign_color), run_time=0.25)
            midYPoint = Dot(self.coords_to_point(0, midY), color=sign_color)
            self.add(midXPoint, midYPoint)
            if in_negative_branch:
                self.play(UpdateFromAlphaFunc(lowerGroup, makeUpdater(lowerX, fixed_guess_x=upperX)), FadeOut(guess_labels))
                lowerX = midX
                lowerY = midY
            else:
                self.play(UpdateFromAlphaFunc(upperGroup, makeUpdater(upperX, fixed_guess_x=lowerX)), FadeOut(guess_labels))
                upperX = midX
                upperY = midY
            self.remove(midXLine, midDot, midYLine, midXBrace)
        self.wait()

    def construct(self):
        self.drawGraph()
        self.solveEquation()

def resit_near(x, m):
    frac_diff = (x - m) % 1
    if frac_diff > 0.5:
        frac_diff -= 1
    return m + frac_diff

def make_alpha_winder(func, start, end, num_checkpoints, cheap=False):
    check_points = [None for i in range(num_checkpoints)]
    check_points[0] = func(start)
    step_size = fdiv(end - start, num_checkpoints)
    for i in range(num_checkpoints - 1):
        check_points[i + 1] = resit_near(func(start + (i + 1) * step_size), check_points[i])

    def return_func(alpha):
        if cheap:
            return alpha
        index = np.clip(0, num_checkpoints - 1, int(alpha * num_checkpoints))
        x = interpolate(start, end, alpha)
        if cheap:
            return check_points[index]
        else:
            return resit_near(func(x), check_points[index])
    return return_func

def complex_to_pair(c):
    return np.array((c.real, c.imag))

def plane_func_from_complex_func(f):
    return lambda x_y4: complex_to_pair(f(complex(x_y4[0], x_y4[1])))

def point3d_func_from_plane_func(f):

    def g(xxx_todo_changeme):
        x, y, z = xxx_todo_changeme
        f_val = f((x, y))
        return np.array((f_val[0], f_val[1], 0))
    return g

def point3d_func_from_complex_func(f):
    return point3d_func_from_plane_func(plane_func_from_complex_func(f))

def plane_zeta(xxx_todo_changeme8):
    x, y = xxx_todo_changeme8
    CLAMP_SIZE = 1000
    z = complex(x, y)
    try:
        answer = mpmath.zeta(z)
    except ValueError:
        return (CLAMP_SIZE, 0)
    if abs(answer) > CLAMP_SIZE:
        answer = answer / abs(answer) * CLAMP_SIZE
    return (float(answer.real), float(answer.imag))

def rescaled_plane_zeta(xxx_todo_changeme9):
    x, y = xxx_todo_changeme9
    return plane_zeta((x / FRAME_X_RADIUS, 8 * y))

def plane_func_by_wind_spec(*specs):

    def embiggen(p):
        if len(p) == 3:
            return p
        elif len(p) == 2:
            return (p[0], p[1], 1)
        else:
            print('Error in plane_func_by_wind_spec embiggen!')
    specs = list(map(embiggen, specs))
    pos_specs = [x_y_z for x_y_z in specs if x_y_z[2] > 0]
    neg_specs = [x_y_z1 for x_y_z1 in specs if x_y_z1[2] < 0]
    neg_specs_made_pos = [(x_y_z2[0], x_y_z2[1], -x_y_z2[2]) for x_y_z2 in neg_specs]

    def poly(c, root_specs):
        return np.prod([(c - complex(x, y)) ** z for x, y, z in root_specs])

    def complex_func(c):
        return poly(c, pos_specs) * np.conjugate(poly(c, neg_specs_made_pos))
    return plane_func_from_complex_func(complex_func)

def scale_func(func, scale_factor):
    return lambda x: func(x) * scale_factor
example_plane_func_spec = [(-3, -1.3, 2), (0.1, 0.2, 1), (2.8, -2, -1)]
example_plane_func = plane_func_by_wind_spec(*example_plane_func_spec)
empty_animation = EmptyAnimation()

class WalkerAnimation(Animation):
    CONFIG = {'walk_func': None, 'remover': True, 'rate_func': None, 'coords_to_point': None}

    def __init__(self, walk_func, val_func, coords_to_point, show_arrows=True, scale_arrows=False, **kwargs):
        self.walk_func = walk_func
        self.val_func = val_func
        self.coords_to_point = coords_to_point
        self.compound_walker = VGroup()
        self.show_arrows = show_arrows
        self.scale_arrows = scale_arrows
        if 'walker_stroke_color' in kwargs:
            walker_stroke_color = kwargs['walker_stroke_color']
        else:
            walker_stroke_color = BLACK
        base_walker = Dot().scale(5 * 0.35).set_stroke(walker_stroke_color, 2)
        self.compound_walker.walker = base_walker
        if show_arrows:
            self.compound_walker.arrow = Arrow(ORIGIN, 0.5 * RIGHT, buff=0)
            self.compound_walker.arrow.match_style(self.compound_walker.walker)
        self.compound_walker.digest_mobject_attrs()
        Animation.__init__(self, self.compound_walker, **kwargs)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        submobject.set_points(starting_submobject.get_points())

    def interpolate_mobject(self, alpha):
        Animation.interpolate_mobject(self, alpha)
        cur_x, cur_y = cur_coords = self.walk_func(alpha)
        cur_point = self.coords_to_point(cur_x, cur_y)
        self.mobject.shift(cur_point - self.mobject.walker.get_center())
        val = self.val_func(cur_coords)
        rev = point_to_rev(val)
        self.mobject.walker.set_fill(rev_to_color(rev))
        if self.show_arrows:
            self.mobject.arrow.set_fill(rev_to_color(rev))
            self.mobject.arrow.rotate(rev * TAU, about_point=self.mobject.arrow.get_start())
            if self.scale_arrows:
                size = point_to_rescaled_size(val)
                self.mobject.arrow.scale(size * 0.3, about_point=self.mobject.arrow.get_start())

def walker_animation_with_display(walk_func, val_func, coords_to_point, number_update_func=None, show_arrows=True, scale_arrows=False, num_decimal_places=1, include_background_rectangle=True, **kwargs):
    walker_anim = WalkerAnimation(walk_func=walk_func, val_func=val_func, coords_to_point=coords_to_point, show_arrows=show_arrows, scale_arrows=scale_arrows, **kwargs)
    walker = walker_anim.compound_walker.walker
    if number_update_func != None:
        display = DecimalNumber(0, num_decimal_places=num_decimal_places, fill_color=WHITE if include_background_rectangle else BLACK, include_background_rectangle=include_background_rectangle)
        if include_background_rectangle:
            display.background_rectangle.fill_opacity = 0.5
            display.background_rectangle.fill_color = GREY
            display.background_rectangle.scale(1.2)
        displaycement = 0.5 * DOWN
        display.next_to(walker, DOWN + RIGHT, SMALL_BUFF)
        display_anim = ChangingDecimal(display, number_update_func, tracked_mobject=walker_anim.compound_walker.walker, **kwargs)
        anim_group = AnimationGroup(walker_anim, display_anim, rate_func=linear)
        return anim_group
    else:
        return walker_anim

def LinearWalker(start_coords, end_coords, coords_to_point, val_func, number_update_func=None, show_arrows=True, scale_arrows=False, include_background_rectangle=True, **kwargs):
    walk_func = lambda alpha: interpolate(start_coords, end_coords, alpha)
    return walker_animation_with_display(walk_func=walk_func, coords_to_point=coords_to_point, val_func=val_func, number_update_func=number_update_func, show_arrows=show_arrows, scale_arrows=scale_arrows, include_background_rectangle=include_background_rectangle, **kwargs)

class ColorMappedByFuncScene(Scene):
    CONFIG = {'func': lambda p: p, 'num_plane': NumberPlane(), 'show_num_plane': True, 'show_output': False, 'hide_background': False}

    def short_path_to_long_path(self, filename_with_ext):
        return self.get_image_file_path(filename_with_ext)

    def setup(self):
        if self.show_output:
            self.input_to_pos_func = self.func
            self.pos_to_color_func = lambda p: p
        else:
            self.input_to_pos_func = lambda p: p
            self.pos_to_color_func = self.func
        self.pixel_pos_to_color_func = lambda x_y3: self.pos_to_color_func(self.num_plane.point_to_coords_cheap(np.array([x_y3[0], x_y3[1], 0])))
        jitter_val = 0.1
        line_coords = np.linspace(-10, 10) + jitter_val
        func_hash_points = it.product(line_coords, line_coords)

        def mini_hasher(p):
            rgba = point_to_rgba(self.pixel_pos_to_color_func(p))
            if rgba[3] != 1.0:
                print('Warning! point_to_rgba assigns fractional alpha', rgba[3])
            return tuple(rgba)
        to_hash = tuple((mini_hasher(p) for p in func_hash_points))
        func_hash = hash(to_hash)
        full_hash = hash((func_hash, self.camera.get_pixel_width()))
        self.background_image_file = self.short_path_to_long_path('color_mapped_bg_hash_' + str(full_hash) + '.png')
        self.in_background_pass = not os.path.exists(self.background_image_file)
        print('Background file: ' + self.background_image_file)
        if self.in_background_pass:
            print('The background file does not exist yet; this will be a background creation + video pass')
        else:
            print('The background file already exists; this will only be a video pass')

    def construct(self):
        if self.in_background_pass:
            self.camera.set_background_from_func(lambda x_y: point_to_rgba(self.pixel_pos_to_color_func((x_y[0], x_y[1]))))
            self.save_image(self.background_image_file, mode='RGBA')
        if self.hide_background:
            self.camera.background_image = None
        else:
            self.camera.background_image = self.background_image_file
        self.camera.init_background()
        if self.show_num_plane:
            self.num_plane.fade()
            self.add(self.num_plane)

class PureColorMap(ColorMappedByFuncScene):
    CONFIG = {'show_num_plane': False}

    def construct(self):
        ColorMappedByFuncScene.construct(self)
        self.wait()

class ColorMappedObjectsScene(ColorMappedByFuncScene):
    CONFIG = {'show_num_plane': False, 'hide_background': True}

class PiWalker(ColorMappedByFuncScene):
    CONFIG = {'walk_coords': [], 'step_run_time': 1, 'scale_arrows': False, 'display_wind': True, 'wind_reset_indices': [], 'display_size': False, 'display_odometer': False, 'color_foreground_not_background': False, 'show_num_plane': False, 'draw_lines': True, 'num_checkpoints': 10, 'num_decimal_places': 1, 'include_background_rectangle': False}

    def construct(self):
        ColorMappedByFuncScene.construct(self)
        if self.color_foreground_not_background or self.display_odometer:
            self.camera.background_image = None
            self.camera.init_background()
        num_plane = self.num_plane
        walk_coords = self.walk_coords
        points = [num_plane.coords_to_point(x, y) for x, y in walk_coords]
        polygon = Polygon(*points, color=WHITE)
        if self.color_foreground_not_background:
            polygon.stroke_width = border_stroke_width
            polygon.color_using_background_image(self.background_image_file)
        total_run_time = len(points) * self.step_run_time
        polygon_anim = ShowCreation(polygon, run_time=total_run_time, rate_func=linear)
        walker_anim = empty_animation
        start_wind = 0
        for i in range(len(walk_coords)):
            start_coords = walk_coords[i]
            end_coords = walk_coords[(i + 1) % len(walk_coords)]
            val_alpha_func = lambda a, start_coords=start_coords, end_coords=end_coords: self.func(interpolate(start_coords, end_coords, a))
            if self.display_wind:
                clockwise_val_func = lambda p: -point_to_rev(self.func(p))
                alpha_winder = make_alpha_winder(clockwise_val_func, start_coords, end_coords, self.num_checkpoints)
                number_update_func = lambda alpha, alpha_winder=alpha_winder, start_wind=start_wind: alpha_winder(alpha) - alpha_winder(0) + start_wind
                start_wind = 0 if i + 1 in self.wind_reset_indices else number_update_func(1)
            elif self.display_size:
                number_update_func = lambda a, val_alpha_func=val_alpha_func: point_to_rescaled_size(val_alpha_func(a))
            else:
                number_update_func = None
            new_anim = LinearWalker(start_coords=start_coords, end_coords=end_coords, coords_to_point=num_plane.coords_to_point, val_func=self.func, remover=i < len(walk_coords) - 1, show_arrows=not self.show_output, scale_arrows=self.scale_arrows, number_update_func=number_update_func, run_time=self.step_run_time, walker_stroke_color=WALKER_LIGHT_COLOR if self.color_foreground_not_background else BLACK, num_decimal_places=self.num_decimal_places, include_background_rectangle=self.include_background_rectangle)
            if self.display_odometer:
                rev_func = lambda a, val_alpha_func=val_alpha_func: point_to_rev(val_alpha_func(a))
                base_arrow = Arrow(ORIGIN, RIGHT, buff=0)
                new_anim = FuncRotater(base_arrow, rev_func=rev_func, run_time=self.step_run_time, rate_func=linear, remover=i < len(walk_coords) - 1)
            walker_anim = Succession(walker_anim, new_anim)
        if self.display_odometer:
            color_wheel = Circle(radius=ODOMETER_RADIUS)
            color_wheel.stroke_width = ODOMETER_STROKE_WIDTH
            color_wheel.color_using_background_image(self.short_path_to_long_path('pure_color_map.png'))
            self.add(color_wheel)
            self.play(walker_anim)
        elif self.draw_lines:
            self.play(polygon_anim, walker_anim)
        else:
            self.play(walker_anim)
        self.wait()

class PiWalkerRect(PiWalker):
    CONFIG = {'start_x': -1, 'start_y': 1, 'walk_width': 2, 'walk_height': 2, 'func': plane_func_from_complex_func(lambda c: c ** 2), 'double_up': False, 'display_wind': True}

    def setup(self):
        TL = np.array((self.start_x, self.start_y))
        TR = TL + (self.walk_width, 0)
        BR = TR + (0, -self.walk_height)
        BL = BR + (-self.walk_width, 0)
        self.walk_coords = [TL, TR, BR, BL]
        if self.double_up:
            self.walk_coords = self.walk_coords + self.walk_coords
        PiWalker.setup(self)

class PiWalkerCircle(PiWalker):
    CONFIG = {'radius': 1, 'num_steps': 100, 'step_run_time': 0.01}

    def setup(self):
        r = self.radius
        N = self.num_steps
        self.walk_coords = [r * np.array((np.cos(i * TAU / N), np.sin(i * TAU / N))) for i in range(N)]
        PiWalker.setup(self)

def split_interval(xxx_todo_changeme10):
    a, b = xxx_todo_changeme10
    mid = (a + b) / 2.0
    return ((a, mid), (mid, b))

class RectangleData:

    def __init__(self, x_interval, y_interval):
        self.rect = (x_interval, y_interval)

    def get_top_left(self):
        return np.array((self.rect[0][0], self.rect[1][1]))

    def get_top_right(self):
        return np.array((self.rect[0][1], self.rect[1][1]))

    def get_bottom_right(self):
        return np.array((self.rect[0][1], self.rect[1][0]))

    def get_bottom_left(self):
        return np.array((self.rect[0][0], self.rect[1][0]))

    def get_top(self):
        return (self.get_top_left(), self.get_top_right())

    def get_right(self):
        return (self.get_top_right(), self.get_bottom_right())

    def get_bottom(self):
        return (self.get_bottom_right(), self.get_bottom_left())

    def get_left(self):
        return (self.get_bottom_left(), self.get_top_left())

    def get_center(self):
        return interpolate(self.get_top_left(), self.get_bottom_right(), 0.5)

    def get_width(self):
        return self.rect[0][1] - self.rect[0][0]

    def get_height(self):
        return self.rect[1][1] - self.rect[1][0]

    def splits_on_dim(self, dim):
        x_interval = self.rect[0]
        y_interval = self.rect[1]
        if dim == 0:
            return_data = [RectangleData(new_interval, y_interval) for new_interval in split_interval(x_interval)]
        elif dim == 1:
            return_data = [RectangleData(x_interval, new_interval) for new_interval in split_interval(y_interval)[::-1]]
        else:
            print('RectangleData.splits_on_dim passed illegitimate dimension!')
        return tuple(return_data)

    def split_line_on_dim(self, dim):
        x_interval = self.rect[0]
        y_interval = self.rect[1]
        if dim == 0:
            sides = (self.get_top(), self.get_bottom())
        elif dim == 1:
            sides = (self.get_left(), self.get_right())
        else:
            print('RectangleData.split_line_on_dim passed illegitimate dimension!')
        return tuple([mid(x, y) for x, y in sides])

class EquationSolver2dNode(object):

    def __init__(self, first_anim, children=[]):
        self.first_anim = first_anim
        self.children = children

    def depth(self):
        if len(self.children) == 0:
            return 0
        return 1 + max([n.depth() for n in self.children])

    def nodes_at_depth(self, n):
        if n == 0:
            return [self]
        return sum([c.nodes_at_depth(n - 1) for c in self.children], [])

    def hacky_bfs(self):
        depth = self.depth()
        return sum([self.nodes_at_depth(i) for i in range(depth + 1)], [])

    def display_in_series(self):
        return Succession(self.first_anim, *[n.display_in_series() for n in self.children])

    def display_in_parallel(self):
        return Succession(self.first_anim, AnimationGroup(*[n.display_in_parallel() for n in self.children]))

    def display_in_bfs(self):
        bfs_nodes = self.hacky_bfs()
        return Succession(*[n.first_anim for n in bfs_nodes])

    def play_in_bfs(self, scene, border_anim):
        bfs_nodes = self.hacky_bfs()
        print('Number of nodes: ', len(bfs_nodes))
        if len(bfs_nodes) < 1:
            print('Less than 1 node! Aborting!')
            return
        scene.play(bfs_nodes[0].first_anim, border_anim)
        for node in bfs_nodes[1:]:
            scene.play(node.first_anim)

class EquationSolver2d(ColorMappedObjectsScene):
    CONFIG = {'camera_config': {'use_z_coordinate_for_display_order': True}, 'initial_lower_x': -5, 'initial_upper_x': 5, 'initial_lower_y': -3, 'initial_upper_y': 3, 'num_iterations': 0, 'num_checkpoints': 10, 'display_in_parallel': False, 'display_in_bfs': False, 'use_fancy_lines': True, 'line_color': WHITE, 'show_arrows': True, 'scale_arrows': False, 'show_winding_numbers': True, 'manual_wind_override': None, 'show_cursor': True, 'linger_parameter': 0.5, 'use_separate_plays': False, 'use_cheap_winding_numbers': False}

    def construct(self):
        if self.num_iterations == 0:
            print('You forgot to set num_iterations (maybe you meant to subclass something other than EquationSolver2d directly?)')
            return
        ColorMappedObjectsScene.construct(self)
        num_plane = self.num_plane
        clockwise_val_func = lambda p: -point_to_rev(self.func(p))
        base_line = Line(UP, RIGHT, stroke_width=border_stroke_width, color=self.line_color)
        if self.use_fancy_lines:
            base_line.color_using_background_image(self.background_image_file)

        def match_style_with_bg(obj1, obj2):
            obj1.match_style(obj2)
            bg = obj2.get_background_image_file()
            if bg != None:
                obj1.color_using_background_image(bg)
        run_time_base = 1
        run_time_with_lingering = run_time_base + self.linger_parameter
        base_rate = lambda t: t
        linger_rate = squish_rate_func(lambda t: t, 0, fdiv(run_time_base, run_time_with_lingering))
        cursor_base = OldTexText('?')
        cursor_base.scale(2)

        def head(m):
            if m == None:
                return None
            return m[0]

        def child(m, i):
            if m == None or m == 0:
                return None
            return m[i + 1]

        def Animate2dSolver(cur_depth, rect, dim_to_split, sides_to_draw=[0, 1, 2, 3], manual_wind_override=None):
            print('Solver at depth: ' + str(cur_depth))
            if cur_depth >= self.num_iterations:
                return EquationSolver2dNode(empty_animation)

            def draw_line_return_wind(start, end, start_wind, should_linger=False, draw_line=True):
                alpha_winder = make_alpha_winder(clockwise_val_func, start, end, self.num_checkpoints, cheap=self.use_cheap_winding_numbers)
                a0 = alpha_winder(0)
                rebased_winder = lambda alpha: alpha_winder(alpha) - a0 + start_wind
                colored_line = Line(num_plane.coords_to_point(*start) + IN, num_plane.coords_to_point(*end) + IN)
                match_style_with_bg(colored_line, base_line)
                walker_anim = LinearWalker(start_coords=start, end_coords=end, coords_to_point=num_plane.coords_to_point, val_func=self.func, number_update_func=rebased_winder if self.show_winding_numbers else None, remover=True, walker_stroke_color=WALKER_LIGHT_COLOR, show_arrows=self.show_arrows, scale_arrows=self.scale_arrows)
                if should_linger:
                    run_time = run_time_with_lingering
                    rate_func = linger_rate
                else:
                    run_time = run_time_base
                    rate_func = base_rate
                opt_line_anim = ShowCreation(colored_line) if draw_line else empty_animation
                line_draw_anim = AnimationGroup(opt_line_anim, walker_anim, run_time=run_time, rate_func=rate_func)
                return (line_draw_anim, rebased_winder(1))
            wind_so_far = 0
            anim = empty_animation
            sides = [rect.get_top(), rect.get_right(), rect.get_bottom(), rect.get_left()]
            for i, (start, end) in enumerate(sides):
                next_anim, wind_so_far = draw_line_return_wind(start, end, wind_so_far, should_linger=i == len(sides) - 1, draw_line=i in sides_to_draw)
                anim = Succession(anim, next_anim)
            if self.show_cursor:
                cursor = cursor_base.copy()
                center_x, center_y = rect.get_center()
                width = rect.get_width()
                height = rect.get_height()
                cursor.move_to(num_plane.coords_to_point(center_x, center_y) + 10 * IN)
                cursor.scale(min(width, height))
                cursor_anim = Succession(FadeIn(cursor, run_time=0.1), Animation(cursor, run_time=3.8), FadeOut(cursor, run_time=0.1))
                anim = AnimationGroup(anim, cursor_anim)
            override_wind = head(manual_wind_override)
            if override_wind != None:
                total_wind = override_wind
            else:
                total_wind = round(wind_so_far)
            if total_wind == 0:
                coords = [rect.get_top_left(), rect.get_top_right(), rect.get_bottom_right(), rect.get_bottom_left()]
                points = np.array([num_plane.coords_to_point(x, y) for x, y in coords]) + 3 * IN
                fill_rect = polygonObject = Polygon(*points, fill_opacity=0.8, color=GREY_D)
                return EquationSolver2dNode(Succession(anim, FadeIn(fill_rect)))
            else:
                sub_rect1, sub_rect2 = rect.splits_on_dim(dim_to_split)
                if dim_to_split == 0:
                    sub_rect_and_sides = [(sub_rect1, 1), (sub_rect2, 3)]
                else:
                    sub_rect_and_sides = [(sub_rect1, 2), (sub_rect2, 0)]
                children = [Animate2dSolver(cur_depth=cur_depth + 1, rect=sub_rect, dim_to_split=1 - dim_to_split, sides_to_draw=[side_to_draw], manual_wind_override=child(manual_wind_override, index)) for index, (sub_rect, side_to_draw) in enumerate(sub_rect_and_sides)]
                mid_line_coords = rect.split_line_on_dim(dim_to_split)
                mid_line_points = [num_plane.coords_to_point(x, y) + 2 * IN for x, y in mid_line_coords]
                mid_line = DashedLine(*mid_line_points)
                return EquationSolver2dNode(Succession(anim, ShowCreation(mid_line)), children)
        lower_x = self.initial_lower_x
        upper_x = self.initial_upper_x
        lower_y = self.initial_lower_y
        upper_y = self.initial_upper_y
        x_interval = (lower_x, upper_x)
        y_interval = (lower_y, upper_y)
        rect = RectangleData(x_interval, y_interval)
        print('Starting to compute anim')
        node = Animate2dSolver(cur_depth=0, rect=rect, dim_to_split=0, sides_to_draw=[], manual_wind_override=self.manual_wind_override)
        print('Done computing anim')
        if self.display_in_parallel:
            anim = node.display_in_parallel()
        elif self.display_in_bfs:
            anim = node.display_in_bfs()
        else:
            anim = node.display_in_series()
        rect_points = [rect.get_top_left(), rect.get_top_right(), rect.get_bottom_right(), rect.get_bottom_left()]
        border = Polygon(*[num_plane.coords_to_point(*x) + IN for x in rect_points])
        match_style_with_bg(border, base_line)
        rect_time_without_linger = 4 * run_time_base
        rect_time_with_linger = 3 * run_time_base + run_time_with_lingering

        def rect_rate(alpha):
            time_in = alpha * rect_time_with_linger
            if time_in < 3 * run_time_base:
                return fdiv(time_in, 4 * run_time_base)
            else:
                time_in_last_leg = time_in - 3 * run_time_base
                alpha_in_last_leg = fdiv(time_in_last_leg, run_time_with_lingering)
                return interpolate(0.75, 1, linger_rate(alpha_in_last_leg))
        border_anim = ShowCreation(border, run_time=rect_time_with_linger, rate_func=rect_rate)
        print('About to do the big Play; for reference, the current time is ', time.strftime('%H:%M:%S'))
        if self.use_separate_plays:
            node.play_in_bfs(self, border_anim)
        else:
            self.play(anim, border_anim)
        print('All done; for reference, the current time is ', time.strftime('%H:%M:%S'))
        self.wait()

class LinePulser(ContinualAnimation):

    def __init__(self, line, bullet_template, num_bullets, pulse_time, output_func=None, **kwargs):
        self.line = line
        self.num_bullets = num_bullets
        self.pulse_time = pulse_time
        self.bullets = [bullet_template.copy() for i in range(num_bullets)]
        self.output_func = output_func
        ContinualAnimation.__init__(self, VGroup(*self.bullets), **kwargs)

    def update_mobject(self, dt):
        alpha = self.external_time % self.pulse_time
        start = self.line.get_start()
        end = self.line.get_end()
        for i in range(self.num_bullets):
            position = interpolate(start, end, fdiv(i + alpha, self.num_bullets))
            self.bullets[i].move_to(position)
            if self.output_func:
                position_2d = (position[0], position[1])
                rev = point_to_rev(self.output_func(position_2d))
                color = rev_to_color(rev)
                self.bullets[i].set_color(color)

class ArrowCircleTest(Scene):

    def construct(self):
        circle_radius = 3
        circle = Circle(radius=circle_radius, color=WHITE)
        self.add(circle)
        base_arrow = Arrow(circle_radius * 0.7 * RIGHT, circle_radius * 1.3 * RIGHT)

        def rev_rotate(x, revs):
            x.rotate(revs * TAU, about_point=ORIGIN)
            x.set_color(rev_to_color(revs))
            return x
        num_arrows = 8 * 3
        arrows = [rev_rotate(base_arrow.copy(), 0.5 - fdiv(i, num_arrows)) for i in range(num_arrows)]
        arrows_vgroup = VGroup(*arrows)
        self.play(ShowCreation(arrows_vgroup), run_time=2.5, rate_func=linear)
        self.wait()

class FuncRotater(Animation):
    CONFIG = {'rev_func': lambda x: x}

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        submobject.set_points(starting_submobject.get_points())

    def interpolate_mobject(self, alpha):
        Animation.interpolate_mobject(self, alpha)
        angle_revs = self.rev_func(alpha)
        self.mobject.rotate(angle_revs * TAU, about_point=ORIGIN)
        self.mobject.set_color(rev_to_color(angle_revs))

class TestRotater(Scene):

    def construct(self):
        test_line = Line(ORIGIN, RIGHT)
        self.play(FuncRotater(test_line, rev_func=lambda x: x % 0.25, run_time=10))

class OdometerScene(ColorMappedObjectsScene):
    CONFIG = {'rotate_func': lambda x: 2 * np.sin(2 * x * TAU), 'run_time': 40, 'dashed_line_angle': None, 'biased_display_start': None, 'pure_odometer_background': False}

    def construct(self):
        ColorMappedObjectsScene.construct(self)
        radius = ODOMETER_RADIUS
        circle = Circle(center=ORIGIN, radius=radius)
        circle.stroke_width = ODOMETER_STROKE_WIDTH
        circle.color_using_background_image(self.background_image_file)
        self.add(circle)
        if self.pure_odometer_background:
            self.wait()
            return
        if self.dashed_line_angle:
            dashed_line = DashedLine(ORIGIN, radius * RIGHT)
            dashed_line.rotate(-self.dashed_line_angle * TAU, about_point=ORIGIN)
            self.add(dashed_line)
        num_display = DecimalNumber(0, include_background_rectangle=False)
        num_display.move_to(2 * DOWN)
        caption = OldTexText('turns clockwise')
        caption.next_to(num_display, DOWN)
        self.add(caption)
        display_val_bias = 0
        if self.biased_display_start != None:
            display_val_bias = self.biased_display_start - self.rotate_func(0)
        display_func = lambda alpha: self.rotate_func(alpha) + display_val_bias
        base_arrow = Arrow(ORIGIN, RIGHT, buff=0)
        self.play(FuncRotater(base_arrow, rev_func=lambda x: -self.rotate_func(x)), ChangingDecimal(num_display, display_func), run_time=self.run_time, rate_func=linear)

class FirstSqrtScene(EquationSolver1d):
    CONFIG = {'x_min': 0, 'x_max': 2.5, 'y_min': 0, 'y_max': 2.5 ** 2, 'graph_origin': 2.5 * DOWN + 5.5 * LEFT, 'x_axis_width': 12, 'zoom_factor': 3, 'zoomed_canvas_center': 2.25 * UP + 1.75 * LEFT, 'func': lambda x: x ** 2, 'targetX': np.sqrt(2), 'targetY': 2, 'initial_lower_x': 1, 'initial_upper_x': 2, 'num_iterations': 5, 'iteration_at_which_to_start_zoom': 3, 'graph_label': 'y = x^2', 'show_target_line': True, 'x_tick_frequency': 0.25}

class TestFirstSqrtScene(FirstSqrtScene):
    CONFIG = {'num_iterations': 1}
FirstSqrtSceneConfig = FirstSqrtScene.CONFIG
shiftVal = FirstSqrtSceneConfig['targetY']

class SecondSqrtScene(FirstSqrtScene):
    CONFIG = {'graph_label': FirstSqrtSceneConfig['graph_label'] + ' - ' + str(shiftVal), 'show_y_as_deviation': True}

class TestSecondSqrtScene(SecondSqrtScene):
    CONFIG = {'num_iterations': 1}

class GuaranteedZeroScene(SecondSqrtScene):
    CONFIG = {'initial_lower_x': 1.75, 'initial_upper_x': 2}

class TestGuaranteedZeroScene(GuaranteedZeroScene):
    CONFIG = {'num_iterations': 1}

class RewriteEquation(Scene):

    def construct(self):
        f_old = OldTex('f(x)')
        f_new = f_old.copy()
        equals_old = OldTex('=')
        equals_old_2 = equals_old.copy()
        equals_new = equals_old.copy()
        g_old = OldTex('g(x)')
        g_new = g_old.copy()
        minus_new = OldTex('-')
        zero_new = OldTex('0')
        f_old.next_to(equals_old, LEFT)
        g_old.next_to(equals_old, RIGHT)
        minus_new.next_to(g_new, LEFT)
        f_new.next_to(minus_new, LEFT)
        equals_new.next_to(g_new, RIGHT)
        zero_new.next_to(equals_new, RIGHT)
        self.add(f_old, equals_old, equals_old_2, g_old)
        self.wait()
        self.play(ReplacementTransform(f_old, f_new), ReplacementTransform(equals_old, equals_new), ReplacementTransform(g_old, g_new), ReplacementTransform(equals_old_2, minus_new), ShowCreation(zero_new))
        self.wait()

class SignsExplanation(Scene):

    def construct(self):
        num_line = NumberLine()
        largest_num = 10
        num_line.add_numbers(*list(range(-largest_num, largest_num + 1)))
        self.add(num_line)
        self.wait()
        pos_num = 3
        neg_num = -pos_num
        pos_arrow = Arrow(num_line.number_to_point(0), num_line.number_to_point(pos_num), buff=0, color=positive_color)
        neg_arrow = Arrow(num_line.number_to_point(0), num_line.number_to_point(neg_num), buff=0, color=negative_color)
        plus_sign = OldTex('+', fill_color=positive_color)
        minus_sign = OldTex('-', fill_color=negative_color)
        plus_sign.next_to(pos_arrow, UP)
        minus_sign.next_to(neg_arrow, UP)
        self.play(ShowCreation(pos_arrow), FadeIn(plus_sign))
        self.play(ShowCreation(neg_arrow), FadeIn(minus_sign))

class VectorField(Scene):
    CONFIG = {'func': example_plane_func, 'granularity': 10, 'arrow_scale_factor': 0.1, 'normalized_arrow_scale_factor': 5}

    def construct(self):
        num_plane = NumberPlane()
        self.add(num_plane)
        x_min, y_min = num_plane.point_to_coords(FRAME_X_RADIUS * LEFT + FRAME_Y_RADIUS * UP)
        x_max, y_max = num_plane.point_to_coords(FRAME_X_RADIUS * RIGHT + FRAME_Y_RADIUS * DOWN)
        x_points = np.linspace(x_min, x_max, self.granularity)
        y_points = np.linspace(y_min, y_max, self.granularity)
        points = it.product(x_points, y_points)
        sized_arrows = Group()
        unsized_arrows = Group()
        for x, y in points:
            output = self.func((x, y))
            output_size = np.sqrt(sum(output ** 2))
            normalized_output = output * fdiv(self.normalized_arrow_scale_factor, output_size)
            arrow = Vector(output * self.arrow_scale_factor)
            normalized_arrow = Vector(normalized_output * self.arrow_scale_factor)
            arrow.move_to(num_plane.coords_to_point(x, y))
            normalized_arrow.move_to(arrow)
            sized_arrows.add(arrow)
            unsized_arrows.add(normalized_arrow)
        self.add(sized_arrows)
        self.wait()
        self.play(ReplacementTransform(sized_arrows, unsized_arrows))
        self.wait()

class HasItsLimitations(Scene):
    CONFIG = {'camera_config': {'use_z_coordinate_for_display_order': True}}

    def construct(self):
        num_line = NumberLine()
        num_line.add_numbers()
        self.add(num_line)
        self.wait()
        base_point = num_line.number_to_point(2) + OUT
        dot_color = ORANGE
        DOT_Z = OUT
        input_dot = Dot(base_point + DOT_Z, color=dot_color)
        input_label = OldTexText('Input', fill_color=dot_color)
        input_label.next_to(input_dot, UP + LEFT)
        input_label.add_background_rectangle()
        self.add_foreground_mobject(input_dot)
        self.add(input_label)
        curved_arrow = Arc(0, color=MAROON_E)
        curved_arrow.set_bound_angles(np.pi, 0)
        curved_arrow.init_points()
        curved_arrow.add_tip()
        curved_arrow.move_arc_center_to(base_point + RIGHT)
        self.play(ShowCreation(curved_arrow))
        output_dot = Dot(base_point + 2 * RIGHT + DOT_Z, color=dot_color)
        output_label = OldTexText('Output', fill_color=dot_color)
        output_label.next_to(output_dot, UP + RIGHT)
        output_label.add_background_rectangle()
        self.add_foreground_mobject(output_dot)
        self.add(output_label)
        self.wait()
        num_plane = NumberPlane()
        num_plane.add_coordinates()
        new_base_point = base_point + 2 * UP
        new_input_dot = input_dot.copy().move_to(new_base_point)
        new_input_label = input_label.copy().next_to(new_input_dot, UP + LEFT)
        new_curved_arrow = Arc(0).match_style(curved_arrow)
        new_curved_arrow.set_bound_angles(np.pi * 3 / 4, 0)
        new_curved_arrow.init_points()
        new_curved_arrow.add_tip()
        input_diff = input_dot.get_center() - curved_arrow.get_points()[0]
        output_diff = output_dot.get_center() - curved_arrow.get_points()[-1]
        new_curved_arrow.shift(new_input_dot.get_center() - new_curved_arrow.get_points()[0] - input_diff)
        new_output_dot = output_dot.copy().move_to(new_curved_arrow.get_points()[-1] + output_diff)
        new_output_label = output_label.copy().next_to(new_output_dot, UP + RIGHT)
        dot_objects = Group(input_dot, input_label, output_dot, output_label, curved_arrow)
        new_dot_objects = Group(new_input_dot, new_input_label, new_output_dot, new_output_label, new_curved_arrow)
        self.play(FadeOut(num_line), FadeIn(num_plane), ReplacementTransform(dot_objects, new_dot_objects))
        self.wait()
        self.add_foreground_mobject(new_dot_objects)
        complex_plane = ComplexPlane()
        complex_plane.add_coordinates()
        self.play(FadeOut(num_plane), FadeIn(complex_plane))
        self.wait()

class ComplexPlaneIs2d(Scene):

    def construct(self):
        com_plane = ComplexPlane()
        self.add(com_plane)
        self.wait()

class NumberLineScene(Scene):

    def construct(self):
        num_line = NumberLine()
        self.add(num_line)
        self.wait()
        border_color = PURPLE_E
        inner_color = RED
        stroke_width = 10
        left_point = num_line.number_to_point(-1)
        right_point = num_line.number_to_point(1)
        interval_1d = Line(left_point, right_point, stroke_color=inner_color, stroke_width=stroke_width)
        rect_1d = Rectangle(stroke_width=0, fill_opacity=1, fill_color=inner_color)
        rect_1d.replace(interval_1d)
        rect_1d.stretch_to_fit_height(SMALL_BUFF)
        left_dot = Dot(left_point, stroke_width=stroke_width, color=border_color)
        right_dot = Dot(right_point, stroke_width=stroke_width, color=border_color)
        endpoints_1d = VGroup(left_dot, right_dot)
        full_1d = VGroup(rect_1d, endpoints_1d)
        self.play(ShowCreation(full_1d))
        self.wait()
        num_plane = NumberPlane()
        random_points = [UP + LEFT, UP + RIGHT, DOWN + RIGHT, DOWN + LEFT]
        border_2d = Polygon(*random_points, stroke_color=border_color, stroke_width=stroke_width)
        filling_2d = Polygon(*random_points, fill_color=inner_color, fill_opacity=0.8, stroke_width=stroke_width)
        full_2d = VGroup(filling_2d, border_2d)
        self.play(FadeOut(num_line), FadeIn(num_plane), ReplacementTransform(full_1d, full_2d))
        self.wait()

class Initial2dFuncSceneBase(Scene):
    CONFIG = {'func': point3d_func_from_complex_func(lambda c: c ** 2 - c ** 3 / 5 + 1)}

    def show_planes(self):
        print('Error! Unimplemented (pure virtual) show_planes')

    def shared_construct(self):
        points = [LEFT + DOWN, RIGHT + DOWN, LEFT + UP, RIGHT + UP]
        for i in range(len(points) - 1):
            line = Line(points[i], points[i + 1], color=RED)
            self.obj_draw(line)

        def wiggle_around(point):
            radius = 0.2
            small_circle = cw_circle.copy()
            small_circle.scale(radius)
            small_circle.move_to(point + radius * RIGHT)
            small_circle.set_color(RED)
            self.obj_draw(small_circle)
        wiggle_around(points[-1])

    def obj_draw(self, input_object):
        self.play(ShowCreation(input_object))

    def construct(self):
        self.show_planes()
        self.shared_construct()

class Initial2dFuncSceneWithoutMorphing(Initial2dFuncSceneBase):

    def setup(self):
        left_camera = Camera(**self.camera_config)
        right_camera = MappingCamera(mapping_func=self.func, **self.camera_config)
        split_screen_camera = SplitScreenCamera(left_camera, right_camera, **self.camera_config)
        self.camera = split_screen_camera

    def show_planes(self):
        self.num_plane = NumberPlane()
        self.num_plane.prepare_for_nonlinear_transform()
        self.add(self.num_plane)

class Initial2dFuncSceneMorphing(Initial2dFuncSceneBase):
    CONFIG = {'num_needed_anchor_curves': 10}

    def setup(self):
        split_line = DashedLine(FRAME_Y_RADIUS * UP, FRAME_Y_RADIUS * DOWN)
        self.num_plane = NumberPlane(x_radius=FRAME_X_RADIUS / 2)
        self.num_plane.to_edge(LEFT, buff=0)
        self.num_plane.prepare_for_nonlinear_transform()
        self.add(self.num_plane, split_line)

    def squash_onto_left(self, object):
        object.shift(FRAME_X_RADIUS / 2 * LEFT)

    def squash_onto_right(self, object):
        object.shift(FRAME_X_RADIUS / 2 * RIGHT)

    def obj_draw(self, input_object):
        output_object = input_object.copy()
        if input_object.get_num_curves() < self.num_needed_anchor_curves:
            input_object.insert_n_curves(self.num_needed_anchor_curves)
        output_object.apply_function(self.func)
        self.squash_onto_left(input_object)
        self.squash_onto_right(output_object)
        self.play(ShowCreation(input_object), ShowCreation(output_object))

    def show_planes(self):
        right_plane = self.num_plane.copy()
        right_plane.center()
        right_plane.prepare_for_nonlinear_transform()
        right_plane.apply_function(self.func)
        right_plane.shift(FRAME_X_RADIUS / 2 * RIGHT)
        self.right_plane = right_plane
        crappy_cropper = FullScreenFadeRectangle(fill_opacity=1)
        crappy_cropper.stretch_to_fit_width(FRAME_X_RADIUS)
        crappy_cropper.to_edge(LEFT, buff=0)
        self.play(ReplacementTransform(self.num_plane.copy(), right_plane), FadeIn(crappy_cropper), Animation(self.num_plane), run_time=3)

class DemonstrateColorMapping(ColorMappedObjectsScene):
    CONFIG = {'show_num_plane': False, 'show_full_color_map': True}

    def construct(self):
        ColorMappedObjectsScene.construct(self)
        if self.show_full_color_map:
            bright_background = Rectangle(width=2 * FRAME_X_RADIUS + 1, height=2 * FRAME_Y_RADIUS + 1, fill_opacity=1)
            bright_background.color_using_background_image(self.background_image_file)
            dim_background = bright_background.copy()
            dim_background.fill_opacity = 0.3
            background = bright_background.copy()
            self.add(background)
            self.wait()
            self.play(ReplacementTransform(background, dim_background))
        self.wait()
        ray = Line(ORIGIN, 10 * LEFT)
        circle = cw_circle.copy()
        circle.color_using_background_image(self.background_image_file)
        self.play(ShowCreation(circle))
        self.wait()
        scale_up_factor = 5
        scale_down_factor = 20
        self.play(ApplyMethod(circle.scale, fdiv(1, scale_down_factor)))
        self.play(ApplyMethod(circle.scale, scale_up_factor * scale_down_factor))
        self.play(ApplyMethod(circle.scale, fdiv(1, scale_up_factor)))
        self.wait()
        self.remove(circle)
        ray = Line(ORIGIN, 10 * LEFT)
        ray.color_using_background_image(self.background_image_file)
        self.play(ShowCreation(ray))
        self.wait()
        self.play(Rotating(ray, about_point=ORIGIN, radians=-TAU / 2))
        self.wait()
        self.play(Rotating(ray, about_point=ORIGIN, radians=-TAU / 2))
        self.wait()
        if self.show_full_color_map:
            self.play(ReplacementTransform(background, bright_background))
            self.wait()

class LoopSplitScene(ColorMappedObjectsScene):
    CONFIG = {'func': plane_func_by_wind_spec((-2, 0, 2), (2, 0, 1)), 'use_fancy_lines': True}

    def PulsedLine(self, start, end, bullet_template, num_bullets=4, pulse_time=1, **kwargs):
        line = Line(start, end, color=WHITE, stroke_width=4, **kwargs)
        if self.use_fancy_lines:
            line.color_using_background_image(self.background_image_file)
        anim = LinePulser(line=line, bullet_template=bullet_template, num_bullets=num_bullets, pulse_time=pulse_time, output_func=self.func, **kwargs)
        return (line, VMobject(*anim.bullets), anim)

    def construct(self):
        ColorMappedObjectsScene.construct(self)
        scale_factor = 2
        shift_term = 0
        tl = (UP + 2 * LEFT) * scale_factor
        tm = UP * scale_factor
        tr = (UP + 2 * RIGHT) * scale_factor
        bl = (DOWN + 2 * LEFT) * scale_factor
        bm = DOWN * scale_factor
        br = (DOWN + 2 * RIGHT) * scale_factor
        top_line = Line(tl, tr)
        bottom_line = Line(br, bl)
        stroke_width = top_line.stroke_width
        default_bullet = PiCreature()
        default_bullet.scale(0.15)

        def pl(a, b):
            return self.PulsedLine(a, b, default_bullet)

        def indicate_circle(x, double_horizontal_stretch=False):
            circle = Circle(color=WHITE, radius=2 * np.sqrt(2))
            circle.move_to(x.get_center())
            if x.get_slope() == 0:
                circle.stretch(0.2, 1)
                if double_horizontal_stretch:
                    circle.stretch(2, 0)
            else:
                circle.stretch(0.2, 0)
            return circle
        tl_line_trip = pl(tl, tm)
        midline_left_trip = pl(tm, bm)
        bl_line_trip = pl(bm, bl)
        left_line_trip = pl(bl, tl)
        left_square_trips = [tl_line_trip, midline_left_trip, bl_line_trip, left_line_trip]
        left_square_lines = [x[0] for x in left_square_trips]
        left_square_lines_vmobject = VMobject(*left_square_lines)
        left_square_bullets = [x[1] for x in left_square_trips]
        left_square_anims = [x[2] for x in left_square_trips]
        tr_line_trip = pl(tm, tr)
        right_line_trip = pl(tr, br)
        br_line_trip = pl(br, bm)
        midline_right_trip = pl(bm, tm)
        right_square_trips = [tr_line_trip, right_line_trip, br_line_trip, midline_right_trip]
        right_square_lines = [x[0] for x in right_square_trips]
        right_square_lines_vmobject = VMobject(*right_square_lines)
        right_square_bullets = [x[1] for x in right_square_trips]
        right_square_anims = [x[2] for x in right_square_trips]
        midline_trips = [midline_left_trip, midline_right_trip]
        midline_lines = [x[0] for x in midline_trips]
        midline_lines_vmobject = VMobject(*midline_lines)
        midline_bullets = [x[1] for x in midline_trips]
        midline_anims = [x[1] for x in midline_trips]
        left_line = left_line_trip[0]
        right_line = right_line_trip[0]
        for b in left_square_bullets + right_square_bullets:
            b.set_fill(opacity=0)
        faded = 0.3

        def bullet_fade(start, end, mob):
            return UpdateFromAlphaFunc(mob, lambda m, a: m.set_fill(opacity=interpolate(start, end, a)))

        def bullet_list_fade(start, end, bullet_list):
            return [bullet_fade(start, end, b) for b in bullet_list]

        def line_fade(start, end, mob):
            return UpdateFromAlphaFunc(mob, lambda m, a: m.set_stroke(width=interpolate(start, end, a) * stroke_width))

        def play_combined_fade(start, end, lines_vmobject, bullets):
            self.play(line_fade(start, end, lines_vmobject), *bullet_list_fade(start, end, bullets))

        def play_fade_left(start, end):
            play_combined_fade(start, end, left_square_lines_vmobject, left_square_bullets)

        def play_fade_right(start, end):
            play_combined_fade(start, end, right_square_lines_vmobject, right_square_bullets)

        def play_fade_mid(start, end):
            play_combined_fade(start, end, midline_lines_vmobject, midline_bullets)

        def flash_circles(circles):
            self.play(LaggedStartMap(FadeIn, VGroup(circles)))
            self.wait()
            self.play(FadeOut(VGroup(circles)))
            self.wait()
        self.add(left_square_lines_vmobject, right_square_lines_vmobject)
        self.remove(*midline_lines)
        self.wait()
        self.play(ShowCreation(midline_lines[0]))
        self.add(midline_lines_vmobject)
        self.wait()
        self.add(*left_square_anims)
        self.play(line_fade(1, faded, right_square_lines_vmobject), *bullet_list_fade(0, 1, left_square_bullets))
        self.wait()
        flash_circles([indicate_circle(l) for l in left_square_lines])
        self.play(line_fade(faded, 1, right_square_lines_vmobject), *bullet_list_fade(1, 0, left_square_bullets))
        self.wait()
        self.add(*right_square_anims)
        self.play(line_fade(1, faded, left_square_lines_vmobject), *bullet_list_fade(0, 1, right_square_bullets))
        self.wait()
        flash_circles([indicate_circle(l) for l in right_square_lines])
        self.play(line_fade(faded, 1, left_square_lines_vmobject), *bullet_list_fade(1, 0, right_square_bullets))
        self.wait()
        self.play(*bullet_list_fade(0, 1, left_square_bullets + right_square_bullets))
        self.wait()
        outside_circlers = [indicate_circle(left_line), indicate_circle(right_line), indicate_circle(top_line, double_horizontal_stretch=True), indicate_circle(bottom_line, double_horizontal_stretch=True)]
        flash_circles(outside_circlers)
        inner_circle = indicate_circle(midline_lines[0])
        self.play(FadeIn(inner_circle))
        self.wait()
        self.play(FadeOut(inner_circle), line_fade(1, 0, midline_lines_vmobject), *bullet_list_fade(1, 0, midline_bullets))
        self.wait()
        self.play(FadeIn(inner_circle), line_fade(0, 1, midline_lines_vmobject), *bullet_list_fade(0, 1, midline_bullets))
        self.wait()
        self.play(FadeOut(inner_circle), line_fade(1, 0, midline_lines_vmobject), *bullet_list_fade(1, 0, midline_bullets))
        self.wait()

class FundThmAlg(EquationSolver2d):
    CONFIG = {'func': plane_func_by_wind_spec((1, 2), (-1, 1.5), (-1, 1.5)), 'num_iterations': 2}

class SolveX5MinusXMinus1(EquationSolver2d):
    CONFIG = {'func': plane_func_from_complex_func(lambda c: c ** 5 - c - 1), 'num_iterations': 10, 'show_cursor': True, 'display_in_bfs': True}

class PureColorMapOfX5Thing(PureColorMap):
    CONFIG = {'func': plane_func_from_complex_func(lambda c: c ** 5 - c - 1)}

class X5ThingWithRightHalfGreyed(SolveX5MinusXMinus1):
    CONFIG = {'num_iterations': 3, 'manual_wind_override': (1, None, (1, (0, None, None), (0, None, None)))}

class SolveX5MinusXMinus1_5Iterations(EquationSolver2d):
    CONFIG = {'func': plane_func_from_complex_func(lambda c: c ** 5 - c - 1), 'num_iterations': 5, 'show_cursor': True, 'display_in_bfs': True, 'manual_wind_override': (None, None, (None, (0, None, None), (0, None, None)))}

class X5_Monster_Red_Lines(SolveX5MinusXMinus1_5Iterations):
    CONFIG = {'use_separate_plays': True, 'use_fancy_lines': False, 'line_color': RED}

class X5_Monster_Green_Lines(X5_Monster_Red_Lines):
    CONFIG = {'line_color': GREEN}

class X5_Monster_Red_Lines_Long(X5_Monster_Red_Lines):
    CONFIG = {'num_iterations': 6}

class X5_Monster_Green_Lines_Long(X5_Monster_Green_Lines):
    CONFIG = {'num_iterations': 6}

class X5_Monster_Red_Lines_Little_More(X5_Monster_Red_Lines_Long):
    CONFIG = {'num_iterations': 7}

class X5_Monster_Green_Lines_Little_More(X5_Monster_Green_Lines_Long):
    CONFIG = {'num_iterations': 7}

class X5_Monster_Red_Lines_No_Numbers(X5_Monster_Red_Lines):
    CONFIG = {'num_iterations': 3, 'show_winding_numbers': False}

class X5_Monster_Green_Lines_No_Numbers(X5_Monster_Green_Lines):
    CONFIG = {'num_iterations': 3, 'show_winding_numbers': False}

class SolveX5MinusXMinus1_3Iterations(EquationSolver2d):
    CONFIG = {'func': plane_func_from_complex_func(lambda c: c ** 5 - c - 1), 'num_iterations': 3, 'show_cursor': True, 'display_in_bfs': True}

class Diagnostic(SolveX5MinusXMinus1_3Iterations):
    CONFIG = {'use_separate_plays': not False, 'use_fancy_lines': True, 'show_winding_numbers': True, 'camera_config': {'use_z_coordinate_for_display_order': True}}

class SolveX5MinusXMinus1Parallel(SolveX5MinusXMinus1):
    CONFIG = {'display_in_parallel': True}

class SolveX5MinusXMinus1BFS(SolveX5MinusXMinus1):
    CONFIG = {'display_in_bfs': True}

class PreviewClip(EquationSolver2d):
    CONFIG = {'func': example_plane_func, 'num_iterations': 5, 'display_in_parallel': True, 'use_fancy_lines': True}

class ParallelClip(EquationSolver2d):
    CONFIG = {'func': plane_func_by_wind_spec((-3, -1.3, 2), (0.1, 0.2, 1), (2.8, -2, 1)), 'num_iterations': 5, 'display_in_parallel': True}

class EquationSolver2dMatchBreakdown(EquationSolver2d):
    CONFIG = {'func': plane_func_by_wind_spec((-2, 0.3, 2), (2, -0.2, 1)), 'num_iterations': 5, 'display_in_parallel': True, 'show_cursor': True}

class EquationSolver2dMatchBreakdown_parallel(EquationSolver2dMatchBreakdown):
    CONFIG = {'display_in_parallel': True, 'display_in_bfs': False}

class EquationSolver2dMatchBreakdown_bfs(EquationSolver2dMatchBreakdown):
    CONFIG = {'display_in_parallel': False, 'display_in_bfs': True}

class QuickPreview(PreviewClip):
    CONFIG = {'num_iterations': 3, 'display_in_parallel': False, 'display_in_bfs': True, 'show_cursor': True}

class LongEquationSolver(EquationSolver2d):
    CONFIG = {'func': example_plane_func, 'num_iterations': 10, 'display_in_bfs': True, 'linger_parameter': 0.4, 'show_cursor': True}

class QuickPreviewUnfancy(LongEquationSolver):
    CONFIG = {}
left_func = lambda x: x ** 2 - x + 1
diff_func = lambda x: np.cos(1.4 * (x - 0.1) * (np.log(x + 0.1) - 0.3) * TAU) / 2.1

class LeftOdometer(OdometerScene):
    CONFIG = {'rotate_func': left_func, 'biased_display_start': 0}

class RightOdometer(OdometerScene):
    CONFIG = {'rotate_func': lambda x: left_func(x) + diff_func(x), 'biased_display_start': 0}

class DiffOdometer(OdometerScene):
    CONFIG = {'rotate_func': diff_func, 'dashed_line_angle': 0.5, 'biased_display_start': 0}

class CombineInterval(Scene):

    def construct(self):
        plus_sign = OldTex('+', fill_color=positive_color)
        minus_sign = OldTex('-', fill_color=negative_color)
        left_point = Dot(LEFT, color=positive_color)
        right_point = Dot(RIGHT, color=negative_color)
        line1 = Line(LEFT, RIGHT)
        interval1 = Group(line1, left_point, right_point)
        plus_sign.next_to(left_point, UP)
        minus_sign.next_to(right_point, UP)
        self.add(interval1, plus_sign, minus_sign)
        self.wait()
        self.play(CircleIndicate(plus_sign), CircleIndicate(minus_sign))
        self.wait()
        mid_point = Dot(ORIGIN, color=GREY)
        question_mark = OldTex('?', fill_color=GREY)
        plus_sign_copy = plus_sign.copy()
        minus_sign_copy = minus_sign.copy()
        new_signs = Group(question_mark, plus_sign_copy, minus_sign_copy)
        for sign in new_signs:
            sign.next_to(mid_point, UP)
        self.play(FadeIn(mid_point), FadeIn(question_mark))
        self.wait()
        self.play(ApplyMethod(mid_point.set_color, positive_color), ReplacementTransform(question_mark, plus_sign_copy))
        self.play(CircleIndicate(plus_sign_copy), CircleIndicate(minus_sign))
        self.wait()
        self.play(ApplyMethod(mid_point.set_color, negative_color), ReplacementTransform(plus_sign_copy, minus_sign_copy))
        self.play(CircleIndicate(minus_sign_copy), CircleIndicate(plus_sign))
        self.wait()

class CombineInterval2(Scene):

    def construct(self):
        plus_sign = OldTex('+', fill_color=positive_color)

        def make_interval(a, b):
            line = Line(a, b)
            start_dot = Dot(a, color=positive_color)
            end_dot = Dot(b, color=positive_color)
            start_sign = plus_sign.copy().next_to(start_dot, UP)
            end_sign = plus_sign.copy().next_to(end_dot, UP)
            return Group(start_sign, end_sign, line, start_dot, end_dot)

        def pair_indicate(a, b):
            self.play(CircleIndicate(a), CircleIndicate(b))
        left_interval = make_interval(2 * LEFT, LEFT)
        right_interval = make_interval(RIGHT, 2 * RIGHT)
        self.play(FadeIn(left_interval), FadeIn(right_interval))
        pair_indicate(left_interval[0], left_interval[1])
        pair_indicate(right_interval[0], right_interval[1])
        self.play(ApplyMethod(left_interval.shift, RIGHT), ApplyMethod(right_interval.shift, LEFT))
        pair_indicate(left_interval[0], right_interval[1])
        self.wait()
tiny_loop_func = scale_func(plane_func_by_wind_spec((-1, -2), (1, 1), (1, 1)), 0.3)

class TinyLoopScene(ColorMappedByFuncScene):
    CONFIG = {'func': tiny_loop_func, 'show_num_plane': False, 'loop_point': ORIGIN, 'circle_scale': 0.7}

    def construct(self):
        ColorMappedByFuncScene.construct(self)
        circle = cw_circle.copy()
        circle.scale(self.circle_scale)
        circle.move_to(self.loop_point)
        self.play(ShowCreation(circle))
        self.wait()

class TinyLoopInInputPlaneAroundNonZero(TinyLoopScene):
    CONFIG = {'loop_point': 0.5 * RIGHT}

class TinyLoopInInputPlaneAroundZero(TinyLoopScene):
    CONFIG = {'loop_point': UP + RIGHT}

class TinyLoopInOutputPlaneAroundNonZero(TinyLoopInInputPlaneAroundNonZero):
    CONFIG = {'camera_class': MappingCamera, 'camera_config': {'mapping_func': point3d_func_from_plane_func(tiny_loop_func)}, 'show_output': True, 'show_num_plane': False}

class TinyLoopInOutputPlaneAroundZero(TinyLoopInInputPlaneAroundZero):
    CONFIG = {'camera_class': MappingCamera, 'camera_config': {'mapping_func': point3d_func_from_plane_func(tiny_loop_func)}, 'show_output': True, 'show_num_plane': False}

class BorderOf2dRegionScene(Scene):

    def construct(self):
        num_plane = NumberPlane()
        self.add(num_plane)
        points = standard_rect + 1.5 * UP + 2 * RIGHT
        interior = Polygon(*points, fill_color=neutral_color, fill_opacity=1, stroke_width=0)
        self.play(FadeIn(interior))
        border = Polygon(*points, color=negative_color, stroke_width=border_stroke_width)
        self.play(ShowCreation(border))
big_loop_no_zeros_func = lambda x_y5: complex_to_pair(np.exp(complex(10, x_y5[1] * np.pi)))

class BigLoopNoZeros(ColorMappedObjectsScene):
    CONFIG = {'func': big_loop_no_zeros_func}

    def construct(self):
        ColorMappedObjectsScene.construct(self)
        points = 3 * np.array([UL, UR, DR, DL])
        polygon = Polygon(*points)
        polygon.color_using_background_image(self.background_image_file)
        self.play(ShowCreation(polygon))
        self.wait()
        polygon2 = polygon.copy()
        polygon2.fill_opacity = 1
        self.play(FadeIn(polygon2))
        self.wait()

class ExamplePlaneFunc(ColorMappedByFuncScene):
    CONFIG = {'show_num_plane': False, 'func': example_plane_func}

    def construct(self):
        ColorMappedByFuncScene.construct(self)
        radius = 0.5

        def circle_point(point):
            circle = cw_circle.copy().scale(radius).move_to(point)
            self.play(ShowCreation(circle))
            return circle

        def circle_spec(spec):
            point = spec[0] * RIGHT + spec[1] * UP
            return circle_point(point)
        nonzero_point = ORIGIN
        nonzero_point_circle = circle_point(nonzero_point)
        self.wait()
        self.play(FadeOut(nonzero_point_circle))
        self.wait()
        zero_circles = Group()
        for spec in example_plane_func_spec:
            zero_circles.add(circle_spec(spec))
        self.wait()
        self.play(FadeOut(zero_circles))
        self.wait()
        specific_spec_index = 0
        temp_circle = circle_spec(example_plane_func_spec[specific_spec_index])
        self.play(FadeOut(temp_circle))
        self.wait()

class PiWalkerExamplePlaneFunc(PiWalkerRect):
    CONFIG = {'show_num_plane': False, 'func': example_plane_func, 'start_x': -4, 'start_y': 3, 'walk_width': 8, 'walk_height': 6}

class NoticeHowOnThisLoop(PiWalkerRect):
    CONFIG = {'show_num_plane': False, 'func': example_plane_func, 'start_x': 0.5, 'start_y': -0.5, 'walk_width': -1, 'walk_height': -1}

class ButOnThisLoopOverHere(NoticeHowOnThisLoop):
    CONFIG = {'start_x': -1, 'start_y': 0, 'walk_width': 1, 'walk_height': 1}

class PiWalkerExamplePlaneFuncWithScaling(PiWalkerExamplePlaneFunc):
    CONFIG = {'scale_arrows': True, 'display_size': True}

class TinyLoopOfBasicallySameColor(PureColorMap):

    def construct(self):
        PureColorMap.construct(self)
        radius = 0.5
        circle = cw_circle.copy().scale(radius).move_to(UP + RIGHT)
        self.play(ShowCreation(circle))
        self.wait()

def uhOhFunc(xxx_todo_changeme11):
    x, y = xxx_todo_changeme11
    x = -np.clip(x, -5, 5) / 5
    y = -np.clip(y, -3, 3) / 3
    alpha = 0.5
    if x >= 0 and y >= x and (y <= 1):
        alpha = interpolate(0.5, 1, y - x)
    if x < 0 and y >= -2 * x and (y <= 1):
        alpha = interpolate(0.5, 1, y + 2 * x)
    if x >= -1 and y >= 2 * (x + 1) and (y <= 1):
        alpha = interpolate(0.5, 0, y - 2 * (x + 1))
    return complex_to_pair(100 * np.exp(complex(0, TAU * (0.5 - alpha))))

class UhOhFuncTest(PureColorMap):
    CONFIG = {'func': uhOhFunc}

class UhOhScene(EquationSolver2d):
    CONFIG = {'func': uhOhFunc, 'manual_wind_override': (1, None, (1, None, (1, None, None))), 'show_winding_numbers': False, 'num_iterations': 5}

class UhOhSceneWithWindingNumbers(UhOhScene):
    CONFIG = {'show_winding_numbers': True}

class UhOhSceneWithWindingNumbersNoOverride(UhOhSceneWithWindingNumbers):
    CONFIG = {'manual_wind_override': None, 'num_iterations': 2}

class UhOhSalientStill(ColorMappedObjectsScene):
    CONFIG = {'func': uhOhFunc}

    def construct(self):
        ColorMappedObjectsScene.construct(self)
        new_up = 3 * UP
        new_left = 5 * LEFT
        thin_line = Line(UP, RIGHT, color=WHITE)
        main_points = [new_left + new_up, new_up, ORIGIN, new_left]
        polygon = Polygon(*main_points, stroke_width=border_stroke_width)
        thin_polygon = polygon.copy().match_style(thin_line)
        polygon.color_using_background_image(self.background_image_file)
        midline = Line(new_up + 0.5 * new_left, 0.5 * new_left, stroke_width=border_stroke_width)
        thin_midline = midline.copy().match_style(thin_line)
        midline.color_using_background_image(self.background_image_file)
        self.add(polygon, midline)
        self.wait()
        everything_filler = FullScreenFadeRectangle(fill_opacity=1)
        everything_filler.color_using_background_image(self.background_image_file)
        thin_white_copy = Group(thin_polygon, thin_midline)
        self.play(FadeIn(everything_filler), FadeIn(thin_white_copy))
        self.wait()

def rect_to_circle(xxx_todo_changeme12):
    x, y, z = xxx_todo_changeme12
    size = np.sqrt(x ** 2 + y ** 2)
    max_abs_size = max(abs(x), abs(y))
    return fdiv(np.array((x, y, z)) * max_abs_size, size)

class MapPiWalkerRect(PiWalkerRect):
    CONFIG = {'camera_class': MappingCamera, 'camera_config': {'mapping_func': rect_to_circle}, 'show_output': True}

class ShowBack(PiWalkerRect):
    CONFIG = {'func': plane_func_by_wind_spec((1, 2), (-1, 1.5), (-1, 1.5))}

class PiWalkerOdometerTest(PiWalkerExamplePlaneFunc):
    CONFIG = {'display_odometer': True}

class PiWalkerFancyLineTest(PiWalkerExamplePlaneFunc):
    CONFIG = {'color_foreground_not_background': True}

class NotFoundScene(Scene):

    def construct(self):
        self.add(OldTexText('SCENE NOT FOUND!'))
        self.wait()
criticalStripYScale = 100
criticalStrip = Axes(x_min=-0.5, x_max=1.5, x_axis_config={'unit_size': FRAME_X_RADIUS, 'number_at_center': 0.5}, y_min=-criticalStripYScale, y_max=criticalStripYScale, y_axis_config={'unit_size': fdiv(FRAME_Y_RADIUS, criticalStripYScale)})

class ZetaViz(PureColorMap):
    CONFIG = {'func': plane_zeta, 'show_num_plane': True}

class TopLabel(Scene):
    CONFIG = {'text': 'Text'}

    def construct(self):
        label = OldTexText(self.text)
        label.move_to(3 * UP)
        self.add(label)
        self.wait()

class SpecifiedWinder(PiWalker):
    CONFIG = {'start_x': 0, 'start_y': 0, 'x_wind': 1, 'y_wind': 1, 'step_size': 0.1}

    def setup(self):
        rev_func = lambda p: point_to_rev(self.func(p))
        start_pos = np.array((self.start_x, self.start_y))
        cur_pos = start_pos.copy()
        start_rev = rev_func(start_pos)
        mid_rev = start_rev
        while abs(mid_rev - start_rev) < self.x_wind:
            cur_pos += (self.step_size, 0)
            mid_rev = rev_func(cur_pos)
        print('Reached ', cur_pos, ', with rev ', mid_rev - start_rev)
        mid_pos = cur_pos.copy()
        end_rev = mid_rev
        while abs(end_rev - mid_rev) < self.y_wind:
            cur_pos -= (0, self.step_size)
            end_rev = rev_func(cur_pos)
        end_pos = cur_pos.copy()
        print('Reached ', cur_pos, ', with rev ', end_rev - mid_rev)
        self.walk_coords = [start_pos, mid_pos, end_pos]
        print('Walk coords: ', self.walk_coords)
        PiWalker.setup(self)

class OneFifthTwoFifthWinder(SpecifiedWinder):
    CONFIG = {'func': example_plane_func, 'start_x': -2.0, 'start_y': 1.0, 'x_wind': 0.2, 'y_wind': 0.2, 'step_size': 0.01, 'show_num_plane': False, 'step_run_time': 6, 'num_decimal_places': 2}

class OneFifthOneFifthWinderWithReset(OneFifthTwoFifthWinder):
    CONFIG = {'wind_reset_indices': [1]}

class OneFifthTwoFifthWinderOdometer(OneFifthTwoFifthWinder):
    CONFIG = {'display_odometer': True}

class ForwardBackWalker(PiWalker):
    CONFIG = {'func': example_plane_func, 'walk_coords': [np.array((-2, 1)), np.array((1, 1))], 'step_run_time': 3}

class ForwardBackWalkerOdometer(ForwardBackWalker):
    CONFIG = {'display_odometer': True}

class PureOdometerBackground(OdometerScene):
    CONFIG = {'pure_odometer_background': True}

class CWColorWalk(PiWalkerRect):
    CONFIG = {'func': example_plane_func, 'start_x': example_plane_func_spec[0][0] - 1, 'start_y': example_plane_func_spec[0][1] + 1, 'walk_width': 2, 'walk_height': 2, 'draw_lines': False, 'display_wind': False, 'step_run_time': 2}

class CWColorWalkOdometer(CWColorWalk):
    CONFIG = {'display_odometer': True}

class CCWColorWalk(CWColorWalk):
    CONFIG = {'start_x': example_plane_func_spec[2][0] - 1, 'start_y': example_plane_func_spec[2][1] + 1}

class CCWColorWalkOdometer(CCWColorWalk):
    CONFIG = {'display_odometer': True}

class ThreeTurnWalker(PiWalkerRect):
    CONFIG = {'func': plane_func_from_complex_func(lambda c: c ** 3 * complex(1, 1) ** 3), 'double_up': True, 'wind_reset_indices': [4]}

class ThreeTurnWalkerOdometer(ThreeTurnWalker):
    CONFIG = {'display_odometer': True}

class FourTurnWalker(PiWalkerRect):
    CONFIG = {'func': plane_func_by_wind_spec((0, 0, 4))}

class FourTurnWalkerOdometer(FourTurnWalker):
    CONFIG = {'display_odometer': True}

class OneTurnWalker(PiWalkerRect):
    CONFIG = {'func': plane_func_from_complex_func(lambda c: np.exp(c) + c)}

class OneTurnWalkerOdometer(OneTurnWalker):
    CONFIG = {'display_odometer': True}

class ZeroTurnWalker(PiWalkerRect):
    CONFIG = {'func': plane_func_by_wind_spec((2, 2, 1), (-1, 2, -1))}

class ZeroTurnWalkerOdometer(ZeroTurnWalker):
    CONFIG = {'display_odometer': True}

class NegOneTurnWalker(PiWalkerRect):
    CONFIG = {'step_run_time': 2, 'func': plane_func_by_wind_spec((0, 0, -1))}

class NegOneTurnWalkerOdometer(NegOneTurnWalker):
    CONFIG = {'display_odometer': True}