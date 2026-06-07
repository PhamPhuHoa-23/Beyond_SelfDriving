from manimlib import *
from tqdm import tqdm
from pathlib import Path
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

def create_cnn_layer(width=19, height=19, cell_size=0.15, depth=0.1, fill_color=BLUE, fill_opacity=0.8, line_width=0.02):
    layer_w = width * cell_size
    layer_h = height * cell_size
    box = Cube(side_length=1)
    box.set_width(layer_h, stretch=True)
    box.set_depth(depth, stretch=True)
    box.set_height(layer_w, stretch=True)
    grid_lines = Group()
    front_z = depth / 2 + 0.001
    back_z = -depth / 2 - 0.001
    for i in range(width + 1):
        x = -layer_w / 2 + i * cell_size
        line = Line3D(start=np.array([x, -layer_h / 2, front_z]), end=np.array([x, layer_h / 2, front_z]), width=line_width, color=WHITE)
        grid_lines.add(line)
    for j in range(height + 1):
        y = -layer_h / 2 + j * cell_size
        line = Line3D(start=np.array([-layer_w / 2, y, front_z]), end=np.array([layer_w / 2, y, front_z]), width=line_width, color=WHITE)
        grid_lines.add(line)
    for i in range(width + 1):
        x = -layer_w / 2 + i * cell_size
        line = Line3D(start=np.array([x, -layer_h / 2, back_z]), end=np.array([x, layer_h / 2, back_z]), width=line_width, color=WHITE)
        grid_lines.add(line)
    for j in range(height + 1):
        y = -layer_h / 2 + j * cell_size
        line = Line3D(start=np.array([-layer_w / 2, y, back_z]), end=np.array([layer_w / 2, y, back_z]), width=line_width, color=WHITE)
        grid_lines.add(line)
    for i in range(width + 1):
        x = -layer_w / 2 + i * cell_size
        line = Line3D(start=np.array([x, layer_h / 2, front_z]), end=np.array([x, layer_h / 2, back_z]), width=line_width, color=WHITE)
        grid_lines.add(line)
        line = Line3D(start=np.array([x, -layer_h / 2, front_z]), end=np.array([x, -layer_h / 2, back_z]), width=line_width, color=WHITE)
        grid_lines.add(line)
    for j in range(height + 1):
        y = -layer_h / 2 + j * cell_size
        line = Line3D(start=np.array([layer_w / 2, y, front_z]), end=np.array([layer_w / 2, y, back_z]), width=line_width, color=WHITE)
        grid_lines.add(line)
        line = Line3D(start=np.array([-layer_w / 2, y, front_z]), end=np.array([-layer_w / 2, y, back_z]), width=line_width, color=WHITE)
        grid_lines.add(line)
    layer = Group(box, grid_lines)
    return layer

class AlphaGoCNN(InteractiveScene):

    def construct(self):
        spacing = 0.8
        layers = Group()
        for i in range(4):
            layer = create_cnn_layer(width=19, height=19, cell_size=0.15, depth=0.15, fill_color=CHILL_BLUE)
            layer.rotate(90 * DEGREES, [1, 0, 0])
            layer[0].set_opacity(0.6)
            layer[1].set_opacity(0.6)
            layer.move_to([0, -spacing * i, 0])
            layers.add(layer)
        self.add(layers)
        self.frame.reorient(-59, 62, 0, (0.7, -0.79, -0.76), 6.99)
        self.wait()
        self.wait()
        self.wait()
        self.embed()

class AlphaGoValueNetwork(InteractiveScene):

    def construct(self):
        spacing = 0.8
        cell_size = 0.15
        layer_size = 19 * cell_size
        layers = Group()
        for i in range(3):
            layer = create_cnn_layer(width=19, height=19, cell_size=cell_size, depth=0.15, fill_color=CHILL_GREEN)
            layer.rotate(90 * DEGREES, [1, 0, 0])
            layer[0].set_color(CHILL_GREEN)
            layer[0].set_opacity(0.6)
            layer[1].set_opacity(0.6)
            layer.move_to([0, -spacing * i, 0])
            layers.add(layer)
        last_layer_y = -spacing * 2
        pyramid_base_y = last_layer_y - 0.15 / 2 - 0.01
        output_y = last_layer_y - spacing * 1.5
        output_size = 0.15
        pyramid_top_y = output_y + output_size / 2 + 0.01
        half_size = layer_size / 2
        half_output = output_size / 2
        base_corners = [np.array([-half_size, pyramid_base_y, -half_size]), np.array([half_size, pyramid_base_y, -half_size]), np.array([half_size, pyramid_base_y, half_size]), np.array([-half_size, pyramid_base_y, half_size])]
        top_corners = [np.array([-half_output, pyramid_top_y, -half_output]), np.array([half_output, pyramid_top_y, -half_output]), np.array([half_output, pyramid_top_y, half_output]), np.array([-half_output, pyramid_top_y, half_output])]
        pyramid_faces = Group()
        for i in range(4):
            next_i = (i + 1) % 4
            face = Polygon(base_corners[i], base_corners[next_i], top_corners[next_i], top_corners[i])
            face.set_fill(CHILL_GREEN, opacity=0.7)
            face.set_stroke(width=0)
            pyramid_faces.add(face)
        pyramid_edges = Group()
        line_width = 0.02
        for i in range(4):
            edge = Line3D(start=base_corners[i], end=top_corners[i], width=line_width, color=WHITE)
            pyramid_edges.add(edge)
        for i in range(4):
            next_i = (i + 1) % 4
            edge = Line3D(start=top_corners[i], end=top_corners[next_i], width=line_width, color=WHITE)
            pyramid_edges.add(edge)
        output_cube = Cube(side_length=output_size)
        output_cube.set_color(CHILL_GREEN)
        output_cube.move_to([0, output_y, 0])
        cube_edges = Group()
        s = output_size / 2
        cube_corners = [np.array([-s, output_y - s, -s]), np.array([s, output_y - s, -s]), np.array([s, output_y - s, s]), np.array([-s, output_y - s, s]), np.array([-s, output_y + s, -s]), np.array([s, output_y + s, -s]), np.array([s, output_y + s, s]), np.array([-s, output_y + s, s])]
        cube_edge_pairs = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        for start_idx, end_idx in cube_edge_pairs:
            edge = Line3D(start=cube_corners[start_idx], end=cube_corners[end_idx], width=line_width, color=WHITE)
            cube_edges.add(edge)
        self.add(layers, pyramid_faces, pyramid_edges, output_cube, cube_edges)
        self.remove(pyramid_faces)
        self.add(pyramid_faces)
        self.remove(cube_edges[6])
        self.add(cube_edges[6])
        self.remove(cube_edges[7])
        self.add(cube_edges[7])
        self.remove(cube_edges[11])
        self.add(cube_edges[11])
        self.frame.reorient(-58, 62, 0, (0.4, -0.59, -0.36), 6.51)
        self.wait()
        self.embed()