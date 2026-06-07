from manimlib import *
from tqdm import tqdm
import re
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
games_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/bitter_lesson/games/less_wrong_reverse_engineer')
size = 19
padding = 0.5
board_width = 8
step = board_width / size

def parse_sgf(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    moves = re.findall('([BW])\\[([a-s]{2})\\]', content)
    parsed_moves = []
    for color_char, coords in moves:
        x = ord(coords[0]) - ord('a')
        y = ord(coords[1]) - ord('a')
        y = 18 - y
        color = BLACK if color_char == 'B' else WHITE
        parsed_moves.append((x, y, color))
    return parsed_moves

def create_stone(x, y, color=BLACK):
    stone_radius = step * 0.45
    pos = [(-(size - 1) / 2 + x) * step, (-(size - 1) / 2 + y) * step, 0]
    squash = 0.3
    if color == BLACK:
        stone = Sphere(radius=stone_radius)
        stone.set_color(BLACK)
        stone.set_shading(0.1, 0.4, 0.1)
    else:
        stone = Sphere(radius=stone_radius)
        stone.set_color('#B0B0B0')
        stone.set_shading(0.7, 0.9, 0.9)
    stone.scale([1, 1, squash])
    pos[2] = stone_radius * squash
    stone.move_to(pos)
    return stone

class GoHackingOne(InteractiveScene):

    def construct(self):
        board_rect = Square(side_length=board_width + padding)
        board_rect.set_fill(FRESH_TAN, opacity=1)
        board_rect.set_stroke(CHILL_BROWN, width=2)
        lines = VGroup()
        start_point = -(size - 1) / 2 * step
        for i in range(size):
            v_line = Line([start_point + i * step, start_point, 0], [start_point + i * step, -start_point, 0])
            h_line = Line([start_point, start_point + i * step, 0], [-start_point, start_point + i * step, 0])
            lines.add(v_line, h_line)
        lines.set_stroke(BLACK, width=1.5)
        hoshi_indices = [3, 9, 15]
        hoshi_dots = VGroup()
        for x in hoshi_indices:
            for y in hoshi_indices:
                dot = Circle(radius=0.05, fill_color=BLACK, fill_opacity=1, stroke_width=0)
                dot.move_to([start_point + x * step, start_point + y * step, 0])
                hoshi_dots.add(dot)
        self.add(board_rect)
        self.add(lines)
        self.add(hoshi_dots)
        p = sorted(list(games_dir.glob('*.sgf')))[0]
        moves = parse_sgf(p)
        self.wait()
        for i, (x, y, color) in enumerate(moves[:20]):
            stone = create_stone(x, y, color)
            self.add(stone)
        self.wait()
        self.wait()
        self.embed()

class GoHackingTwo(InteractiveScene):

    def construct(self):
        board_rect = Square(side_length=board_width + padding)
        board_rect.set_fill(FRESH_TAN, opacity=1)
        board_rect.set_stroke(CHILL_BROWN, width=2)
        lines = VGroup()
        start_point = -(size - 1) / 2 * step
        for i in range(size):
            v_line = Line([start_point + i * step, start_point, 0], [start_point + i * step, -start_point, 0])
            h_line = Line([start_point, start_point + i * step, 0], [-start_point, start_point + i * step, 0])
            lines.add(v_line, h_line)
        lines.set_stroke(BLACK, width=1.5)
        hoshi_indices = [3, 9, 15]
        hoshi_dots = VGroup()
        for x in hoshi_indices:
            for y in hoshi_indices:
                dot = Circle(radius=0.05, fill_color=BLACK, fill_opacity=1, stroke_width=0)
                dot.move_to([start_point + x * step, start_point + y * step, 0])
                hoshi_dots.add(dot)
        self.add(board_rect)
        self.add(lines)
        self.add(hoshi_dots)
        moves = [(3, 15, '#FFFFFF'), (2, 4, '#FFFFFF'), (11, 13, '#FFFFFF'), (10, 12, '#FFFFFF'), (11, 12, '#FFFFFF'), (10, 11, '#FFFFFF'), (11, 14, '#000000'), (10, 13, '#000000'), (12, 13, '#000000'), (9, 12, '#000000'), (12, 12, '#000000'), (11, 11, '#000000')]
        self.wait()
        for i, (x, y, color) in enumerate(moves):
            stone = create_stone(x, y, color)
            self.add(stone)
        self.wait()
        self.remove(board_rect, lines, hoshi_dots)
        self.wait(20)
        self.embed()