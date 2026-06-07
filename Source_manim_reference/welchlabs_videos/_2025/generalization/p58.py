from manimlib import *
from functools import partial
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
CHILL_BROWN = '#948979'
YELLOW = '#ffd35a'
BLUE = '#65c8d0'

class NeuralNetwork(nn.Module):

    def __init__(self, activation_function=nn.Sigmoid()):
        super(NeuralNetwork, self).__init__()
        self.w1 = nn.Parameter(torch.randn(2, 2))
        self.b1 = nn.Parameter(torch.randn(2))
        self.w2 = nn.Parameter(torch.randn(2, 1))
        self.b2 = nn.Parameter(torch.randn(1))
        self.activation_function = activation_function

    def forward(self, x):
        h = self.activation_function(torch.matmul(x, self.w1) + self.b1)
        y = self.activation_function(torch.matmul(h, self.w2) + self.b2)
        return y
X = torch.tensor([[-1, -1], [-1, 1], [1, -1], [1, 1]], dtype=torch.float)
y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float)

class StepFunction(nn.Module):

    def forward(self, x):
        return torch.where(x >= 0, 1.0, 0.0)

class NeuralNetworkTwoParam(nn.Module):

    def __init__(self, activation_function=nn.Sigmoid()):
        super(NeuralNetworkTwoParam, self).__init__()
        self.w10 = nn.Parameter(torch.tensor([-3, -1.5], dtype=torch.float32))
        self.w11 = torch.tensor([1, 1], dtype=torch.float32)
        self.b1 = torch.tensor([0.5, -1.5], dtype=torch.float32)
        self.w2 = torch.tensor([[1], [-1]], dtype=torch.float32)
        self.b2 = torch.tensor([-0.4], dtype=torch.float32)
        self.activation_function = activation_function

    def forward(self, x):
        w1 = torch.vstack((self.w10, self.w11))
        h = self.activation_function(torch.matmul(x, w1) + self.b1)
        y = self.activation_function(torch.matmul(h, self.w2) + self.b2)
        return y

class P66v3(InteractiveScene):

    def construct(self):
        model = NeuralNetwork(StepFunction())
        criterion = nn.MSELoss()
        model.w1 = torch.nn.Parameter(torch.tensor([[1, 1], [1, 1]], dtype=torch.float32))
        model.b1 = torch.nn.Parameter(torch.tensor([0.5, -1.5], dtype=torch.float32))
        model.w2 = torch.nn.Parameter(torch.tensor([[1], [-1]], dtype=torch.float32))
        model.b2 = torch.nn.Parameter(torch.tensor([-0.5], dtype=torch.float32))
        all_losses = []
        all_losses_batch = []
        x_range = np.linspace(-4, 4, 256)
        y_range = np.linspace(-4, 4, 256)
        with torch.no_grad():
            for v1 in tqdm(x_range):
                for v2 in y_range:
                    model.w1 = torch.nn.Parameter(torch.tensor([[v1, v2], [1, 1]], dtype=torch.float32))
                    outputs = model(X)
                    loss = criterion(outputs, y)
                    all_losses_batch.append(loss.item())
        all_losses_batch = np.array(all_losses_batch).reshape(256, 256)
        all_losses_batch = all_losses_batch * 2
        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[0, 2.0, 0.5], height=8, width=8, depth=3, axis_config={'include_ticks': True, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'tip_config': {'fill_opacity': 1, 'width': 0.1, 'length': 0.1}})
        x_label = Tex('w_{00}', font_size=28).set_color(CHILL_BROWN)
        y_label = Tex('w_{01}', font_size=28).set_color(CHILL_BROWN)
        z_label = Tex('Error^2', font_size=28).set_color(CHILL_BROWN)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label.next_to(axes.y_axis, UP)
        z_label.next_to(axes.z_axis, OUT)
        z_label.rotate(90 * DEGREES, [1, 0, 0])

        def param_surface(u, v):
            x = u
            y = v
            x_idx = int((x + 4) * 256 / 8)
            y_idx = int((y + 4) * 256 / 8)
            x_idx = np.clip(x_idx, 0, 255)
            y_idx = np.clip(y_idx, 0, 255)
            z = all_losses_batch[x_idx, y_idx]
            return np.array([x, y, z])
        surface = ParametricSurface(param_surface, u_range=[-4, 4], v_range=[-4, 4], resolution=(256, 256))
        ts = TexturedSurface(surface, 'step_function_activation_landscape_1.png')
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.7)
        num_lines = 20
        num_points = 256
        u_gridlines = VGroup()
        v_gridlines = VGroup()
        u_values = np.linspace(-4, 4, num_lines)
        v_points = np.linspace(-4, 4, num_points)
        for u in u_values:
            points = [param_surface(u, v) for v in v_points]
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            u_gridlines.add(line)
        u_points = np.linspace(-4, 4, num_points)
        for v in u_values:
            points = [param_surface(u, v) for u in u_points]
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            v_gridlines.add(line)
        self.frame.reorient(0, 0, 0, (0.05, -0.06, 0.0), 12)
        self.add(ts)
        self.add(u_gridlines, v_gridlines)
        self.add(axes, x_label, y_label, z_label)
        self.wait(1)
        self.play(self.frame.animate.reorient(35, 57, 0, (-0.02, -0.09, 0.03), 10.69), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(137, 56, 0, (-0.02, -0.09, 0.03), 10.69), run_time=16, rate_func=linear)
        self.wait()
        self.play(self.frame.animate.reorient(26, 45, 0, (-0.41, 0.51, 1.03), 10.85), run_time=4)
        self.wait()
        self.play(self.frame.animate.reorient(122, 66, 0, (-0.41, 0.51, 1.03), 10.85), run_time=4)
        self.wait()
        self.wait(20)

class P58(InteractiveScene):

    def construct(self):
        model = NeuralNetworkTwoParam(nn.Sigmoid())
        criterion = nn.MSELoss()
        all_losses_batch = []
        x_range = np.linspace(-4, 4, 256)
        y_range = np.linspace(-4, 4, 256)
        with torch.no_grad():
            for v1 in tqdm(x_range):
                for v2 in y_range:
                    model.w10 = torch.nn.Parameter(torch.tensor([v1, v2], dtype=torch.float32))
                    outputs = model(X)
                    loss = criterion(outputs, y)
                    all_losses_batch.append(loss.item())
        all_losses_batch = np.array(all_losses_batch).reshape(256, 256)
        all_losses_batch = all_losses_batch * 50
        all_losses_batch = all_losses_batch - np.min(all_losses_batch)
        model = NeuralNetworkTwoParam(nn.Sigmoid())
        criterion = nn.MSELoss()
        optimizer = optim.SGD(model.parameters(), lr=3.0)
        history = []
        for i in range(500):
            outputs = model(X)
            loss = criterion(outputs, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            history.append([i, loss.item(), *model.w10.detach().numpy().tolist()])
        history = np.array(history)
        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[0, 2.0, 0.5], height=8, width=8, depth=3, axis_config={'include_ticks': True, 'color': CHILL_BROWN, 'stroke_width': 2, 'include_tip': True, 'tip_config': {'fill_opacity': 1, 'width': 0.1, 'length': 0.1}})
        x_label = Tex('w_{00}', font_size=28).set_color(CHILL_BROWN)
        y_label = Tex('w_{01}', font_size=28).set_color(CHILL_BROWN)
        z_label = Tex('Error^2', font_size=28).set_color(CHILL_BROWN)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label.next_to(axes.y_axis, UP)
        z_label.next_to(axes.z_axis, OUT)
        z_label.rotate(90 * DEGREES, [1, 0, 0])

        def param_surface(u, v):
            x = u
            y = v
            x_idx = int((x + 4) * 256 / 8)
            y_idx = int((y + 4) * 256 / 8)
            x_idx = np.clip(x_idx, 0, 255)
            y_idx = np.clip(y_idx, 0, 255)
            z = all_losses_batch[x_idx, y_idx]
            return np.array([x, y, z])
        surface = ParametricSurface(param_surface, u_range=[-4, 4], v_range=[-4, 4], resolution=(256, 256))
        ts = TexturedSurface(surface, '/Users/stephen/Stephencwelch Dropbox/welch_labs/double_descent/graphics/sigmoid_function_activation_landscape_1.png')
        ts.set_shading(0.0, 0.1, 0)
        ts.set_opacity(0.7)
        num_lines = 20
        num_points = 256
        u_gridlines = VGroup()
        v_gridlines = VGroup()
        u_values = np.linspace(-4, 4, num_lines)
        v_points = np.linspace(-4, 4, num_points)
        for u in u_values:
            points = [param_surface(u, v) for v in v_points]
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            u_gridlines.add(line)
        u_points = np.linspace(-4, 4, num_points)
        for v in u_values:
            points = [param_surface(u, v) for u in u_points]
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_stroke(width=1, color=WHITE, opacity=0.3)
            v_gridlines.add(line)
        path_points = []
        for step in history:
            _, loss, w0, w1 = step
            x_idx = int((w0 + 4) * 256 / 8)
            y_idx = int((w1 + 4) * 256 / 8)
            x_idx = np.clip(x_idx, 0, 255)
            y_idx = np.clip(y_idx, 0, 255)
            z = all_losses_batch[x_idx, y_idx]
            path_points.append([w0, w1, z])
        path_segments = Group()
        for i in range(len(path_points) - 1):
            start = np.array(path_points[i])
            end = np.array(path_points[i + 1])
            line = Line3D(start=start, end=end, width=0.05)
            line.set_color(WHITE)
            path_segments.add(line)
        start_point = Sphere(radius=0.05, color=YELLOW)
        start_point.move_to(path_points[0])
        end_point = Sphere(radius=0.125, color=RED)
        end_point.move_to(path_points[0])
        self.add(ts)
        self.add(u_gridlines, v_gridlines)
        self.add(axes, z_label)
        self.wait(1)
        self.frame.reorient(137, 56, 0, (-0.02, -0.09, 0.03), 10.69)
        self.wait(1)
        self.play(self.frame.animate.reorient(26, 45, 0, (-0.41, 0.51, 1.03), 10.85), run_time=10)
        self.wait()
        self.add(end_point)
        self.wait()
        total_points = len(path_segments)
        point_count = 0
        initial_orientation = (26, 45, 0)
        final_orientation = (122, 66, 0)
        for i in range(len(path_segments)):
            self.remove(end_point)
            self.add(path_segments[i])
            end_point.move_to(path_points[i])
            self.add(end_point)
            progress = point_count / total_points
            current_theta = initial_orientation[0] + (final_orientation[0] - initial_orientation[0]) * progress
            current_phi = initial_orientation[1] + (final_orientation[1] - initial_orientation[1]) * progress
            current_gamma = initial_orientation[2] + (final_orientation[2] - initial_orientation[2]) * progress
            self.frame.reorient(current_theta, current_phi, current_gamma, (-0.41, 0.51, 1.03), 10.85)
            self.wait(1.0 / 30)
            point_count += 1
        self.wait()
        self.wait()
        self.wait(20)