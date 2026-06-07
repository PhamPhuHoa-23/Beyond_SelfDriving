from manimlib import *
from tqdm import tqdm
import re
from pathlib import Path
import matplotlib.pyplot as plt
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
games_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/bitter_lesson/games/games_with_videos')
svg_dir = Path('/Users/stephen/Stephencwelch Dropbox/welch_labs/bitter_lesson/graphics/to_manim/')
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

def get_board():
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
    board = Group()
    board.add(board_rect)
    board.add(lines)
    board.add(hoshi_dots)
    return board

def get_neighbors(x, y, size=19):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = (x + dx, y + dy)
        if 0 <= nx < size and 0 <= ny < size:
            neighbors.append((nx, ny))
    return neighbors

def get_group(x, y, board_state):
    color = board_state.get((x, y))
    if color is None:
        return set()
    group = set()
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in group:
            continue
        if board_state.get((cx, cy)) == color:
            group.add((cx, cy))
            for nx, ny in get_neighbors(cx, cy):
                if (nx, ny) not in group:
                    stack.append((nx, ny))
    return group

def get_liberties(group, board_state):
    liberties = set()
    for x, y in group:
        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in board_state:
                liberties.add((nx, ny))
    return liberties

def find_captures(x, y, board_state):
    color = board_state.get((x, y))
    opponent = WHITE if color == BLACK else BLACK
    captured = set()
    for nx, ny in get_neighbors(x, y):
        if board_state.get((nx, ny)) == opponent:
            group = get_group(nx, ny, board_state)
            if len(get_liberties(group, board_state)) == 0:
                captured.update(group)
    return captured

class GameSanityCheck(InteractiveScene):

    def construct(self):
        board = get_board()
        games = sorted(list(games_dir.glob('*sgf')))
        p = games[1]
        print(p)
        moves = parse_sgf(p)
        board_state = {}
        stone_objects = {}
        self.add(board)
        for i, (x, y, color) in enumerate(moves):
            stone = create_stone(x, y, color)
            self.add(stone)
            board_state[x, y] = color
            stone_objects[x, y] = stone
            captured = find_captures(x, y, board_state)
            for cx, cy in captured:
                self.remove(stone_objects[cx, cy])
                del board_state[cx, cy]
                del stone_objects[cx, cy]
        self.wait()
        self.wait(20)
        self.embed()